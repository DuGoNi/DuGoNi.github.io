# 박두곤 — 연구와 강의 · 저장소

- **본채(사이트)**: https://sites.google.com/view/parkdugon (Google Sites)
- **서고(이 저장소)**: https://dugoni.github.io — 글·강의의 정본이 사는 곳. 루트가 전체 색인이다.
- 사이트 게시판(강의·논문·소식·일기)과 홈 «최근 소식»은 `boards/*.json`을 fetch해 그린다.
  **글을 얹을 때 Sites 편집기를 열 일이 없다.**

## 글 얹기 (전부 한 줄)

```bash
py _tools/pub.py lecture "1.1.2 강의.html" 1-1-2 "미분이라는 관점" "Phase I 언어 · Part 1 수학"
py _tools/pub.py news   "글.html" 2026-08-20-topic "제목" "부제(선택)"
py _tools/pub.py diary  "글.html" 2026-08-20 "제목"
py _tools/pub.py paper  "글.html" paper-slug "제목" "원제(선택)"
py _tools/pub.py note   news "글 없는 한 줄 소식"
```

- 복사 → `boards/*.json` 갱신 → 링크 점검(`_tools/check.py`) → 커밋 → **push까지 자동**. 막으려면 `--no-push`.
- 글 본문은 `_tools/post-template.html`을 복사해 쓰면 «투과» 조판이 맞는다.
- slug 규약: 영문·숫자·하이픈만. 강의는 번호(`1-1-2`), 글은 날짜(`YYYY-MM-DD[-주제]`). **한번 공개한 slug는 바꾸지 않는다** — 공유된 링크가 죽는다.

## 폴더

- `lectures/` 강의 정본 · `posts/` 글 정본 · `boards/` 게시판 색인 JSON
- `sites/` **구글 사이트 임베드 소스의 정본** — 편집기보다 여기가 먼저다 (`sites/README.md`)
- `_tools/` pub.py(게시) · check.py(링크 점검) · post-template.html(글 틀)

## 규칙 (3년 뒤의 나에게)

- 한 글은 한 곳: 밖에 알릴 것은 **소식**, 하루의 기록은 **일기**, 잰 것과 어긋남은 **실험**, 강의·번역은 **학습**.
- 연구 항목을 접을 때는 페이지를 지우지 말고 **이전연구**로 옮겨 적는다 — 닫힌 결론과 «원인 아님» 목록째.
- 분기마다 한 번: `git push` 되어 있는지, 사이트 게시판이 JSON을 제대로 무는지, `py _tools/check.py` 통과하는지 본다.
