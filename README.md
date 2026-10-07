# 만듦 CS 콘텐츠 예시

매일 한 질문을 보내는 만듦 CS 메일을 위한 예시 10개입니다. 질문·답변·해설은 한국어로 작성했고, 각 질문에 **Codex 내장 이미지 생성 도구(image_gen)로 만든 비유 그림**과 참고 문서를 연결했습니다. 질문당 이미지는 최대 2개이며, 현재는 모두 1개씩 총 10개입니다.

**먼저 [전체 미리보기](preview.html)를 브라우저에서 열어보세요.** 로컬에서 인터넷 없이 본문과 이미지를 확인할 수 있습니다. GitHub에서는 아래 MD 링크를 열면 이미지와 함께 읽을 수 있습니다. GitHub Pages 설정은 필요하지 않습니다.

[생성형 이미지 10개 한눈에 보기](preview-contact-sheet.png) · [사용한 생성 프롬프트](image-prompts.json)

## 예시 질문 목록

| 예시 날짜 | 주제 | 질문 파일 |
| --- | --- | --- |
| 2026-10-08 | 운영체제 | [프로세스와 스레드](questions/process-and-thread.md) |
| 2026-10-09 | 운영체제 | [경쟁 상태와 원자성](questions/race-condition.md) |
| 2026-10-10 | 운영체제 | [교착 상태](questions/deadlock.md) |
| 2026-10-11 | 네트워크 | [TCP 3-way handshake](questions/tcp-three-way-handshake.md) |
| 2026-10-12 | 네트워크 | [DNS 조회와 캐시](questions/dns-resolution.md) |
| 2026-10-13 | 네트워크 | [HTTP 캐시와 304](questions/http-cache-validation.md) |
| 2026-10-14 | 데이터베이스 | [B-tree 인덱스](questions/database-btree-index.md) |
| 2026-10-15 | 데이터베이스 | [트랜잭션 격리 수준](questions/transaction-isolation.md) |
| 2026-10-16 | 자료구조 | [스택과 큐](questions/stack-and-queue.md) |
| 2026-10-17 | 자료구조 | [해시 충돌](questions/hash-table-collision.md) |

## 파일 구성

```text
index.json                 # 외부 조회용 목록과 이미지 메타데이터
questions/*.md             # 질문·정답·해설 10개
images/*.png               # 이미지 모델이 생성한 1536×1024 PNG 10개
image-prompts.json         # 생성 도구와 질문별 실제 프롬프트
archive/diagrams/          # 이전 코드 기반 SVG·PNG 도식 보관
preview.html               # 전체 콘텐츠 로컬 미리보기
preview-contact-sheet.png  # 개념도 10개 모아보기
scripts/                   # 미리보기 및 보관된 예전 도식 재생성 도구
```

## 일정과 게시 상태

- 날짜는 2026년 10월 8일부터 17일까지의 **예시**입니다.
- `index.json`의 모든 `status`는 `draft`입니다. 실제 메일은 발송하지 않았습니다.
- 실제 운영일로 바꿀 때는 목록의 `date`와 MD의 `date`를 함께 수정하세요.
- 외부 연동 기능 구현 시 `published`이면서 한국 날짜 기준 공개일이 지난 항목만 페이지에서 표시하고, 당일 항목만 발송하도록 연결하는 것을 제안합니다. 현재 앱에는 이 목록을 읽는 기능이 아직 없습니다.
- 공개 저장소에서는 초안 파일도 누구나 읽을 수 있습니다. `draft`는 향후 만듦의 노출·발송 제어용이며 GitHub 접근 제한 기능이 아닙니다.

## 제안하는 목록 형식

`index.json`은 이번 예시를 위해 정의한 외부 콘텐츠 계약입니다. 루트에는 `schemaVersion: 1`, `timezone: "Asia/Seoul"`, `maxImagesPerQuestion: 2`, `items`가 있습니다. 현재 각 항목의 `image`는 이미지 하나의 메타데이터입니다.

| 필드 | 의미 |
| --- | --- |
| `date` | 한국 시간 기준 발송일, MD의 `date`와 일치 |
| `slug` | 만듦 답변 주소 `/cs/{slug}`에 쓸 고유값 |
| `title` | 관리·목록용 제목 |
| `category`, `difficulty` | 주제와 난이도 (`beginner` / `intermediate`) |
| `status` | `draft` / `published`; 이 예시는 모두 `draft` |
| `file` | 저장소 루트 기준 MD 경로 |
| `image.src` | 저장소 루트 기준 생성형 PNG 경로 |
| `image.alt` | 이미지 대체 텍스트 |
| `image.caption` | 그림과 CS 개념을 연결하는 비유 설명 |
| `image.width`, `image.height` | 1536 × 1024 |
| `image.generator` | `image_gen` |
| `sources` | 사실 확인과 추가 학습용 참고 문서 |

질문과 해설 본문은 MD에만 저장합니다. 목록에는 조회·분류·이미지 표시에 필요한 메타데이터가 있습니다. `slug`와 날짜는 항목마다 중복되지 않게 관리하세요.

MD 상단 정보는 기존 만듦 파서가 허용하는 `date`, `slug`, `title`만 사용했습니다. 본문은 `## 질문`, `## 정답`, `## 해설`로 구분합니다. 이미지 경로는 MD 위치 기준 `../images/...png`이며 GitHub에서 바로 표시됩니다.

## 만듦에 연결할 때

1. 만듦 서버에서 공개 저장소의 목록과 MD 원문을 읽습니다.
2. 날짜·게시 상태·파일 형식을 검사하고, 구독 정보와 발송 기록은 기존 만듦 DB에서 관리합니다.
3. 메일에는 질문과 만듦의 `/cs/{slug}` 링크를 넣습니다.
4. 답변 페이지에서 같은 MD의 정답·해설과 이미지를 표시합니다.

**기존 앱 코드는 이번 작업에서 변경하지 않았습니다.** 현재의 MD 파서는 이 질문 파일을 읽을 수 있지만, 현재 화면 렌더러는 Markdown 이미지와 일반 링크 문법을 렌더링하지 않습니다. 연동 작업에서 이미지·링크 지원과 외부 파일 조회를 추가해야 합니다. 이미지는 MD와 목록에 함께 연결되어 있으므로, 렌더링할 때 두 경로를 중복 표시하지 않도록 한 방식을 선택하세요.

발송 기록에 저장소 커밋 ID와 파일 경로를 남기고, 답변 페이지도 해당 버전을 읽으면 발송 당시 내용을 유지할 수 있습니다. 외부 본문을 DB에 복제할 필요는 없습니다. 캐시와 조회 실패 처리는 연동 시 함께 구성하세요.

## 이미지와 미리보기 수정

현재 본문에서 사용하는 PNG 10개는 **이미지 생성 모델의 출력 원본**입니다. SVG를 변환해 만든 이미지가 아닙니다. 같은 그림의 SVG 원본은 없습니다. [image-prompts.json](image-prompts.json)에 실제 생성 프롬프트를 기록했습니다. 그림을 수정하려면 이미지 생성 도구로 편집하거나 재생성한 다음 경로·대체 텍스트·설명을 함께 갱신하세요.

이전 버전의 코드 기반 도식은 `archive/diagrams/`에 보관했습니다. 아래 명령은 보관된 예전 SVG만 다시 생성합니다.

```shell
python scripts/generate-diagrams.py
```

보관된 예전 SVG를 PNG로 다시 렌더링하려면 Playwright와 Chromium이 준비된 환경에서 실행합니다. 현재 생성형 이미지는 덮어쓰지 않습니다.

```shell
node scripts/render-images.cjs
```

기존 프로젝트의 Playwright를 사용할 수도 있습니다.

```shell
node scripts/render-images.cjs D:/mandeum/mandeum-front/node_modules/playwright
```

MD와 목록을 수정한 뒤 HTML 미리보기를 갱신하려면 다음 명령을 실행합니다.

```shell
python scripts/build-preview.py
```

스크립트는 저장소 파일을 GitHub에 올리거나 메일을 보내지 않습니다. SVG 생성·PNG 렌더링은 `archive/diagrams/`만, 미리보기 생성은 `preview.html`을 갱신합니다. 질문 파일과 목록은 수정하지 않습니다. 미리보기 생성기는 질문당 이미지가 2개를 넘으면 중단합니다. 추후 두 번째 이미지를 추가하려면 목록의 이미지 메타데이터와 미리보기의 메타데이터 조회 방식도 확장하세요.

## 확인한 항목

- 기존 만듦의 `parseCsMarkdown`으로 질문 10개 모두 파싱 성공, 각 파일 UTF-8 32KB 이내
- 날짜·slug 중복 없음, 목록과 MD 메타데이터 일치, 모든 항목 초안
- MD 상대 이미지 경로·목록 이미지 경로·대체 텍스트 일치
- 생성형 PNG 10개 모두 1536×1024, 질문당 1개로 최대 2개 제한 충족
- 생성형 그림 10개의 글자·수치·화살표 방향·본문과의 일치 여부 시각 검토
- HTML 미리보기 1440px·390px 화면에서 본문 10개와 이미지 10개 표시, 가로 넘침 없음

기존 만듦 앱의 소스·DB·발송 설정은 변경하지 않았습니다. 앱 전체 테스트나 실제 메일 발송 테스트는 이 콘텐츠 작업의 검증 범위에 포함되지 않습니다.
