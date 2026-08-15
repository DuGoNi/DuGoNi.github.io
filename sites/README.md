# Sites 임베드 정본

구글 사이트(sites.google.com/view/parkdugon) 각 페이지의 «퍼가기 소스 코드» 원본.

**규칙: 저장소가 원본, Sites 편집기가 사본이다.**
임베드를 고칠 때는 ① 여기 파일을 먼저 고치고 → ② Sites에서 블록 연필(코드 수정)로 전체 교체 → ③ 게시.
편집기에서 직접 고쳤다면 그 소스를 반드시 여기로 복사해 둔다 — Sites는 export가 없어서, 계정 사고가 나면 여기 없는 소스는 사라진다.

게시판(board-*.html)은 행을 하드코딩하지 않는다 — `boards/*.json`을 fetch해 그린다.
글 등록은 `py _tools/pub.py …` 한 줄로 끝나고 Sites는 손대지 않는다.
