#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""japan_coverage.html (아티팩트용 조각) -> index.html (독립 실행 문서)

아티팩트는 호스트가 <!doctype>/<head>/<body>와 테마 토글을 붙여준다.
GitHub 저장소에서 파일을 그대로 열 때는 그게 없으므로 직접 채운다.
"""
FRAG = open("japan_coverage.html", encoding="utf-8").read()

EXTRA_CSS = """
/* --- 독립 문서 전용: 테마 토글 --- */
.wrap { position:relative; }
.themebtn {
  position:absolute; top:38px; right:24px;
  font-family:var(--mono); font-size:11px; letter-spacing:.06em;
  padding:6px 11px; border:1px solid var(--line); border-radius:3px;
  background:var(--surface); color:var(--ink2); cursor:pointer;
}
.themebtn:hover { border-color:var(--muted); color:var(--ink); }
.themebtn:focus-visible { outline:2px solid var(--focus); outline-offset:2px; }
@media (max-width:640px) { .themebtn { top:26px; right:16px; } }
@media print { .themebtn, .controls { display:none; } }
"""

TOGGLE_HTML = """
<button class="themebtn" id="themebtn" type="button">테마 전환</button>
"""

TOGGLE_JS = """
/* ---------- 테마 토글 (독립 문서에는 호스트 토글이 없음) ---------- */
(function () {
  var KEY = 'jp-coverage-theme', root = document.documentElement,
      btn = document.getElementById('themebtn');
  function store(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function read()   { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function isDark() {
    var t = root.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  function label() { btn.textContent = isDark() ? '라이트 모드로' : '다크 모드로'; }
  function apply(dark) { root.setAttribute('data-theme', dark ? 'dark' : 'light'); label(); }
  var saved = read();
  if (saved === 'dark' || saved === 'light') apply(saved === 'dark'); else label();
  btn.addEventListener('click', function () {
    var d = !isDark(); apply(d); store(d ? 'dark' : 'light');
  });
})();
"""

# 1) CSS 주입 (마지막 </style> 앞)
i = FRAG.rindex("</style>")
FRAG = FRAG[:i] + EXTRA_CSS + FRAG[i:]

# 2) 버튼 주입 (.wrap 바로 뒤)
anchor = '<div class="wrap">'
j = FRAG.index(anchor) + len(anchor)
FRAG = FRAG[:j] + TOGGLE_HTML + FRAG[j:]

# 3) 토글 JS 주입 (마지막 </script> 앞)
k = FRAG.rindex("</script>")
FRAG = FRAG[:k] + TOGGLE_JS + FRAG[k:]

# 4) <title>은 head로 옮기므로 본문에서 제거
TITLE = "일본 도시 리스트 행정구역 커버리지"
FRAG = FRAG.replace(f"<title>{TITLE}</title>\n", "", 1)

DESC = ("해외 도시 리스트의 일본 항목 36개가 일본 행정구역을 얼마나 덮는지 "
        "47개 도도부현 폴리곤 지도로 분석한 결과.")
FAVI = ("data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 "
        "viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>"
        "%F0%9F%97%BE</text></svg>")

DOC = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<meta name="description" content="{DESC}">
<meta name="robots" content="noindex, nofollow">
<title>{TITLE}</title>
<link rel="icon" href="{FAVI}">
<style>
*, *::before, *::after {{ box-sizing:border-box; }}
html {{ -webkit-text-size-adjust:100%; }}
body {{ margin:0; }}
</style>
</head>
<body>
{FRAG}
</body>
</html>
"""

open("index.html", "w", encoding="utf-8").write(DOC)

import os
n = os.path.getsize("index.html")
print(f"index.html {n/1024:.0f} KB")
for need in ("<!doctype html>", "<html lang=\"ko\">", "<head>", "</head>",
             "themebtn", "jp-coverage-theme", "</body>", "</html>"):
    assert need in DOC, need
print("필수 구조 확인 OK")
print("본문 <title> 중복:", DOC.count(f"<title>{TITLE}</title>"))
