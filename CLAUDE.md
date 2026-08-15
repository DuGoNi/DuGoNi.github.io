# 지침 — 박두곤 사이트에 강의·실험·일기·소식·논문을 올리는 법

이 문서는 새 세션의 Claude가 "이 강의 올려줘", "실험 기록 추가해", "일기 써서 올려" 같은
요청을 **몇 분 안에, 사이트 편집기 없이** 끝내기 위한 지침이다. 사람이 읽어도 된다.

## 전체 그림 (30초)

- **본채**: https://sites.google.com/view/parkdugon — Google Sites. 페이지 겉면은 «투과» 조판의 임베드(iframe).
- **서고(이 저장소)**: https://dugoni.github.io — 글·강의의 **정본**. 루트가 전체 색인이다.
- 사이트의 게시판 다섯(강의·논문·소식·일기·실험)과 홈 «최근 소식»은 전부
  `boards/*.json`을 fetch해 스스로 행을 그린다.
- 따라서 **콘텐츠 업로드 = `pub.py` 한 줄**이다. Sites 편집기·재게시·브라우저 자동화가 전혀 필요 없다.
  push 뒤 1~3분(GitHub Pages 배포 + 임베드 캐시)이면 사이트에 반영된다.

## 유형별 절차 (전부 이 폴더에서 실행)

### 강의 — "○○ 강의 올려줘"
원본은 보통 `..\study\강의\...\*(강의).html` (자족 HTML — 손대지 말고 그대로 복사한다).
```bash
py _tools/pub.py lecture "<원본 경로>" 1-1-2 "미분이라는 관점" "Phase I 언어 · Part 1 수학 · 1.1 Functions"
```
- slug = 강의 번호의 하이픈화(`1.1.2` → `1-1-2`). yr 칸은 자동으로 `L1.1.2`.
- 부제 = Phase · Part · 절 경로 (게시판 행의 이탤릭).

### 소식 / 일기 / 논문 — "소식 올려줘", "일기 써서 올려"
글 본문이 필요하면 `_tools/post-template.html`을 복사해 작성한다
(수정할 곳: `<title>`·og 메타 2곳·journal 줄의 분류·h1·날짜·본문·봉인. 조판·CSS는 건드리지 않는다).
```bash
py _tools/pub.py news  "<글.html>" 2026-08-20-topic "제목" "부제(선택)"
py _tools/pub.py diary "<글.html>" 2026-08-20 "제목"
py _tools/pub.py paper "<글.html>" paper-slug "제목" "원제(선택)"
```
- slug = 날짜 기반 `YYYY-MM-DD[-주제]` (논문은 자유 영문 slug).
- 글 없이 목록에 한 줄만: `py _tools/pub.py note news "한 줄"` (news 자리에 diary/exp/papers/lectures 가능).

### 실험 — "실험 기록 추가해"
실험 기록은 대부분 글 없는 한 줄이다:
```bash
py _tools/pub.py note exp "온도 소인 다시 측정 — 300 K 위에서 직선성 회복." --yr 2026.09
```
관찰이 길어 글로 남길 때만: `py _tools/pub.py exp "<글.html>" 2026-09-01-iv "제목" "부제"`.

### pub.py가 자동으로 하는 일
파일 복사(`lectures/` 또는 `posts/`) → `boards/*.json` 맨 위에 행 삽입 → **링크 점검**(`_tools/check.py`,
죽은 링크가 있으면 push를 막는다) → `git add -A` + 커밋 → **push까지**. 막을 때만 `--no-push`.

### 확인 (업로드 후 항상)
1. `py _tools/check.py` 가 push 중 통과했는지 (pub이 이미 돌림).
2. 1~3분 뒤 게시판 페이지에서 새 행 확인 — 예: https://sites.google.com/view/parkdugon/소식
   (임베드가 JSON을 캐시 버스터로 부르므로 새로고침이면 뜬다. 안 뜨면 GitHub Pages 배포 대기 중.)
3. 글을 얹었다면 글 주소(pub 출력의 «주소:»)를 직접 열어 렌더 확인.

## 절대 규칙

- **공개한 slug는 바꾸지 않는다** — 공유된 링크가 죽는다. 오타를 냈으면 새 slug로 다시 올리고 옛 파일은 남겨 둔다.
- 이름은 **박두곤 (Park Dugon)**. 박도곤 아님.
- «투과» 조판 문법: 색을 쓰지 않는다(잉크 농도만), 세리프(Noto Serif KR)+모노(IBM Plex Mono)+이탤릭 세리프(Palatino), 감쇠 세선. 새 문서는 기존 템플릿을 복사해서 시작한다 — CSS를 새로 쓰지 않는다.
- 한 글은 한 곳: 밖에 알릴 것 → **소식**, 하루의 기록 → **일기**, 잰 것과 어긋남 → **실험**, 강의·번역 → **학습**.
- `boards/*.json`을 손으로 고칠 때는 새 항목을 **배열 맨 앞**에 넣는다 (`{"yr","t","s"(선택),"href"(선택)}` — href 없으면 회색 무링크 행).

## Sites 편집기를 열어야 하는 드문 경우 (조판 수정, 새 페이지)

콘텐츠가 아니라 **겉면(임베드 HTML)** 을 고칠 때만 해당한다. 규칙: **저장소가 원본, 편집기가 사본.**

1. `sites/` 의 해당 정본 파일을 먼저 고치고 커밋·push한다.
   | 페이지 | 정본 | 페이지 문서 ID (편집 URL 조각) |
   |---|---|---|
   | 홈 | sites/home.html | `1ImFAMfEPO_-PPIFpna9VSnmmgG0XAvu6` |
   | 소식 | sites/board-news.html | `1vmuy-G6Y1XgUZ8sh882R1P_fDCg6XUdS` |
   | 일기 | sites/board-diary.html | `1QuvRmhWXeCzDK9ZVS9dsh9xupQYudymM` |
   | 강의(게시판) | sites/board-lectures.html | `1cx7G7NoV5232k7oz4KBE3Gsqc2nUS29n` |
   | 논문(게시판) | sites/board-papers.html | `1BRR9cAC44szvwJNnx2-eRaEnzPR-0Qpy` |
   | 실험 | sites/board-exp.html | `1bhhrl0eMdK96xEkL_Mz9fKPzMvxFCznd` |
   편집 URL: `https://sites.google.com/d/1rHVdG-HCeWSRLVQrFA5mMGOOMPpHcXy4/p/<문서ID>/edit`
   (연구·메인연구1~3·이전연구·학습·갤러리·숨긴 1.1.1은 아직 정본이 없다 — 고치러 들어가면
   **먼저 편집기의 코드를 sites/에 복사해 정본화**한 뒤 수정하라.)
2. 편집기에서 반영 (브라우저 자동화 레시피 — claude-in-chrome):
   - 블록 클릭 → 연필(코드 수정) → 대화상자의 textarea에
     `fetch('https://dugoni.github.io/sites/<파일>?v='+Date.now())` 로 정본을 받아
     value 세터 + input 이벤트로 주입 → «다음» → «저장».
   - **함정**: 대화상자가 10~30초 늦게 뜬다(스크린샷으로 확인 후 진행). 페이지 복제·저장 직후
     렌더러가 30~90초 얼 수 있다(리로드로 회복). 임베드 안 링크는 `_top`이 차단되므로 전부
     `target="_blank" rel="noopener"`.
3. **게시 버튼 → 검토 → 게시** (콘텐츠와 달리 임베드 수정은 재게시해야 반영된다).

## 저장소 지도

`lectures/` 강의 정본 · `posts/` 글 정본 · `boards/` 게시판 JSON(사이트가 이걸 그린다) ·
`sites/` 임베드 정본 · `_tools/` pub.py(게시)·check.py(링크 점검)·post-template.html(글 틀) ·
`index.html` 서고 색인 · `404.html`

## 미해결 권고 (요청받으면 이어서)

강의 head에 og 메타 주입(pub 후처리) · 계기 localStorage 내보내기/이관(파이프라인 셸) ·
KaTeX 폰트 공용화로 강의 파일 경량화 · RSS 생성 · Sites 파비콘 업로드(수동) · 소식 상한+아카이브 페이지
