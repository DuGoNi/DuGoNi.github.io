// 라이트/다크 토글. 선택은 localStorage에 남고, 없으면 OS 설정을 따른다.
// 깜빡임(FOUC)을 막으려고 <head>에서 먼저 한 번 실행되고,
// 버튼 연결은 DOM이 준비된 뒤에 이뤄진다.
(function () {
  var KEY = "theme";
  var root = document.documentElement;

  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  if (saved === "dark" || saved === "light") root.setAttribute("data-theme", saved);

  function current() {
    var attr = root.getAttribute("data-theme");
    if (attr) return attr;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function paint(btn) {
    var dark = current() === "dark";
    btn.textContent = dark ? "☀" : "☾";
    btn.setAttribute("aria-label", dark ? "밝은 화면으로 전환" : "어두운 화면으로 전환");
  }

  function init() {
    var btn = document.querySelector(".theme-toggle");
    if (!btn) return;
    paint(btn);
    btn.addEventListener("click", function () {
      var next = current() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      try { localStorage.setItem(KEY, next); } catch (e) {}
      paint(btn);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
