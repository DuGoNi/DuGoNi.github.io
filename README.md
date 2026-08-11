# 개인 홈페이지

GitHub Pages로 배포하는 정적 홈페이지. 빌드 도구도 의존성도 없다.
파일을 고쳐서 push하면 1~2분 뒤 사이트에 반영된다.

## 구조

```
index.html      소개 (첫 화면)
research.html   연구 · 논문 · 발표
teaching.html   강의
notes.html      글 · 정리 자료
404.html        없는 주소로 들어왔을 때
assets/
  style.css     색 · 간격 · 글꼴 (맨 위 :root 변수만 바꾸면 전체 반영)
  theme.js      라이트/다크 토글
  favicon.svg   탭 아이콘
.nojekyll       GitHub이 Jekyll을 돌리지 않게 하는 표시 (지우지 말 것)
```

파일(PDF·PPT)은 `files/` 폴더를 만들어 넣고 `files/이름.pdf` 로 링크한다.

## 고치는 법

`[대괄호]`로 감싼 부분이 채워 넣을 자리다. 네 파일 전부에 이름·이메일이
들어가므로, 이름을 바꿀 때는 네 파일을 모두 고쳐야 한다.

색을 바꾸려면 `assets/style.css` 맨 위 `:root`의 `--accent` 값 하나만
바꾸면 링크·강조·아이콘 색이 함께 따라온다.

## 로컬에서 미리 보기

```
py -m http.server 8766 --directory .
```

브라우저에서 `http://localhost:8766` 을 연다.
(파일을 직접 더블클릭해서 열어도 대체로 보이지만, 절대경로를 쓰는
`404.html`은 서버로 열어야 제대로 나온다.)

## 배포

```
git add -A
git commit -m "내용 수정"
git push
```

푸시하면 GitHub이 알아서 다시 올린다. 저장소 이름이 `사용자이름.github.io`
라면 주소는 `https://사용자이름.github.io` 다.
