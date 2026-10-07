/* Render only ARCHIVED SVG diagrams; never replace the active generated images.
 * Run with a Playwright installation:
 *   node scripts/render-images.cjs
 * Or provide an existing Playwright module path as the first argument.
 *   node scripts/render-images.cjs D:/path/to/node_modules/playwright
 * Requires the Playwright Chromium browser. No network requests are made.
 */
const fs = require('node:fs/promises');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require(process.argv[2] || 'playwright');

(async () => {
  const root = path.resolve(__dirname, '..');
  const { items } = JSON.parse(await fs.readFile(path.join(root, 'index.json'), 'utf8'));
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1400, height: 900 }, deviceScaleFactor: 1 });
    for (const item of items) {
      const svg = path.join(root, 'archive', 'diagrams', `${item.slug}.svg`);
      const png = path.join(root, 'archive', 'diagrams', `${item.slug}.png`);
      await page.goto(pathToFileURL(svg).href);
      await page.evaluate(() => document.fonts.ready);
      const issues = await page.locator('text').evaluateAll(nodes => nodes.flatMap(el => {
        const box = el.getBBox();
        return box.x < 0 || box.y < 0 || box.x + box.width > 1400 || box.y + box.height > 900
          ? [el.textContent] : [];
      }));
      if (issues.length) throw new Error(`${item.slug}: text outside canvas: ${issues.join(', ')}`);
      await page.screenshot({ path: png });
      console.log(`Rendered archived diagram: ${item.slug}`);
    }
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
