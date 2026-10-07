"""Create a local, responsive HTML preview from index.json and Markdown.

This small renderer supports only this repository's template. No dependencies.
Run: python scripts/build-preview.py
"""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'index.json').read_text(encoding='utf-8'))
image_metadata = {item['image']['src']: item['image'] for item in data['items']}

def inline(text):
    text = escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return re.sub(r'\[([^\]]+)\]\((https://[^)]+)\)', r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', text)

def render(text):
    html = []
    for block in text.strip().split('\n\n'):
        image = re.fullmatch(r'!\[([^\]]+)\]\(\.\./(images/[^)]+)\)', block)
        if image:
            alt, src = image.groups()
            meta = image_metadata[src]
            html.append(f'<figure><a href="{escape(src)}"><img src="{escape(src)}" alt="{escape(alt)}" width="{meta["width"]}" height="{meta["height"]}" loading="lazy"></a></figure>')
        elif block.startswith('### '):
            html.append('<h4>'+inline(block[4:])+'</h4>')
        elif block.startswith('- '):
            html.append('<ul>'+''.join('<li>'+inline(line[2:])+'</li>' for line in block.splitlines())+'</ul>')
        else:
            html.append('<p>'+inline(block)+'</p>')
    return '\n'.join(html)

cards=[]
nav=[]
for n,item in enumerate(data['items'],1):
    text=(ROOT/item['file']).read_text(encoding='utf-8')
    image_count = len(re.findall(r'!\[[^\]]*\]\([^)]+\)', text))
    if not 1 <= image_count <= min(2, data.get('maxImagesPerQuestion', 2)):
        raise ValueError(f'{item["slug"]}: 질문당 이미지는 1~2개로 제한합니다.')
    sections=dict(re.findall(r'^## (질문|정답|해설)\n([\s\S]*?)(?=^## |\Z)',text,re.M))
    slug=escape(item['slug'])
    nav.append(f'<a href="#{slug}">{n:02d} {escape(item["title"])}</a>')
    cards.append(f'''<article id="{slug}">
    <div class="meta">{n:02d} / {escape(item['category'])} · 예시 날짜 {escape(item['date'])} · {"게시 예약 / 공개" if item['status'] == 'published' else "초안"}</div>
    <h2>{inline(sections['질문'].strip())}</h2>
    <section class="answer"><h3>짧은 답변</h3>{render(sections['정답'])}</section>
    <section><h3>더 알아보기</h3>{render(sections['해설'])}</section>
    <div class="files"><a href="{escape(item['file'])}">MD 원본</a><a href="{escape(item['image']['src'])}">생성형 이미지 원본</a><a href="#top">처음으로 ↑</a></div>
    </article>''')

document='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>만듦 · CS 예시 10선</title><style>
:root{color-scheme:light;font-family:'Malgun Gothic',sans-serif;color:#172b35;background:#f4f7f7}*{box-sizing:border-box}body{margin:0}header,main{max-width:1040px;margin:auto;padding:48px 28px}header{padding-bottom:0}.eyebrow,.meta{color:#087f73;font-size:14px;font-weight:700;letter-spacing:.03em}h1{font-size:44px;letter-spacing:-2px;margin:20px 0}header p{color:#5c7079;line-height:1.9}nav{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:28px 0}nav a{padding:13px 18px;border:1px solid #d8e5e0;border-radius:10px;background:white;text-decoration:none}a{color:#087f73;overflow-wrap:anywhere}article{background:white;border:1px solid #e0e9e8;border-radius:20px;padding:42px;margin-bottom:32px;scroll-margin:20px}h2{font-size:29px;line-height:1.55;letter-spacing:-.8px}h3{font-size:20px;margin:30px 0 16px}h4{font-size:18px;margin:28px 0 12px}p,li{font-size:17px;line-height:1.95;word-break:keep-all;overflow-wrap:anywhere}.answer{padding:4px 24px 12px;background:#eef7f3;border-radius:14px}.answer h3{color:#087f73}figure{margin:28px 0}img{width:100%;height:auto;border-radius:12px;display:block}code{background:#edf1f4;padding:2px 6px;border-radius:4px;font-size:.9em}.files{display:flex;flex-wrap:wrap;gap:20px;border-top:1px solid #e1e8e8;padding-top:24px;margin-top:30px;font-size:14px}.files a{text-decoration:none}@media(max-width:640px){header,main{padding:26px 16px}h1{font-size:32px}nav{grid-template-columns:1fr}article{padding:24px 18px}h2{font-size:23px}p,li{font-size:16px}.answer{padding:1px 16px 8px}}
</style></head><body><header id="top"><div class="eyebrow">MANDEUM / DAILY CS</div><h1>하루 한 질문, CS 예시 10선</h1><p>질문 · 핵심 답변 · 해설 · 이미지 생성 모델로 만든 쉬운 비유 그림<br>질문마다 이미지 1장씩, 최대 2장 원칙으로 구성했습니다.<br>2026년 10월 8~17일은 예시 일정이며, 10개 모두 해당 날짜부터 공개되도록 게시 예약했습니다. 실제 메일 발송은 만듦의 운영 연동 이후 진행됩니다.</p><nav>'''+''.join(nav)+'''</nav></header><main>'''+''.join(cards)+'''</main></body></html>'''
(ROOT/'preview.html').write_text(document,encoding='utf-8')
print('Generated preview.html')
