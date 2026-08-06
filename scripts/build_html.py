#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""japan_map.json -> japan_coverage.html"""
import json

D = json.load(open("japan_map.json", encoding="utf-8"))
main, inset, meta = D["main"], D["inset"], D["meta"]
PAYLOAD = json.dumps(D, ensure_ascii=False, separators=(",", ":"))

SEIREI_COV = ["삿포로","센다이","요코하마","시즈오카","나고야","교토","오사카",
              "고베","오카야마","히로시마","기타큐슈","후쿠오카","구마모토"]
SEIREI_MIS = ["사이타마","지바","가와사키","사가미하라","니가타","하마마쓰","사카이"]

HTML = f"""<title>일본 도시 리스트 행정구역 커버리지</title>
<style>
:root {{
  color-scheme: light;
  --bg:#e4e8eb; --surface:#f8f9fa; --sea:#dce2e7;
  --ink:#11171c; --ink2:#4d5761; --muted:#7c8791;
  --line:#ced5db; --line-soft:#dde3e8;
  --s0:#e8ebee; --s1:#86b6ef; --s2:#3987e5; --s3:#256abf; --s4:#104281;
  --bar:#2a78d6; --pt:#eb6834;
  --focus:#2a78d6;
  --sans:-apple-system,BlinkMacSystemFont,"Pretendard Variable",Pretendard,
         "Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
}}
@media (prefers-color-scheme:dark) {{
  :root:where(:not([data-theme="light"])) {{
    color-scheme: dark;
    --bg:#101315; --surface:#1b1f23; --sea:#15191c;
    --ink:#eef1f4; --ink2:#a5afb8; --muted:#78838c;
    --line:#2b3136; --line-soft:#23282c;
    --s0:#3a4249; --s1:#1c5cab; --s2:#3987e5; --s3:#86b6ef; --s4:#cde2fb;
    --bar:#3987e5; --pt:#d95926;
    --focus:#86b6ef;
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --bg:#101315; --surface:#1b1f23; --sea:#15191c;
  --ink:#eef1f4; --ink2:#a5afb8; --muted:#78838c;
  --line:#2b3136; --line-soft:#23282c;
  --s0:#3a4249; --s1:#1c5cab; --s2:#3987e5; --s3:#86b6ef; --s4:#cde2fb;
  --bar:#3987e5; --pt:#d95926;
  --focus:#86b6ef;
}}

* {{ box-sizing:border-box; }}
body {{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:var(--sans); font-size:15px; line-height:1.65;
  -webkit-font-smoothing:antialiased;
  word-break:keep-all;            /* 한글: 단어 중간에서 끊지 않음 */
  overflow-wrap:break-word;       /* 단, 컨테이너보다 긴 낱말은 예외적으로 허용 */
}}
.wrap {{ max-width:1240px; margin:0 auto; padding:40px 24px 72px; }}
@media (max-width:640px) {{ .wrap {{ padding:28px 16px 56px; }} }}

.eyebrow {{
  font-family:var(--mono); font-size:11px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--muted); margin:0 0 14px;
}}
h1 {{
  font-size:clamp(26px,4.4vw,42px); line-height:1.18; letter-spacing:-.022em;
  font-weight:680; margin:0 0 16px; text-wrap:balance; max-width:22ch;
}}
.dek {{ font-size:17px; color:var(--ink2); margin:0; max-width:64ch; }}
.dek b {{ color:var(--ink); font-weight:620; }}

h2 {{
  font-size:19px; letter-spacing:-.012em; font-weight:640;
  margin:0 0 4px; text-wrap:balance;
}}
.sub {{ font-size:13.5px; color:var(--muted); margin:0 0 18px; }}

section {{ margin-top:52px; }}
.rule {{ height:1px; background:var(--line); border:0; margin:0; }}

/* ---- headline stats ---- */
.stats {{
  display:grid; gap:1px; background:var(--line);
  border:1px solid var(--line); border-radius:3px; overflow:hidden;
  grid-template-columns:repeat(3,1fr); margin:32px 0 0;
}}
@media (max-width:720px) {{ .stats {{ grid-template-columns:1fr; }} }}
.stat {{ background:var(--surface); padding:20px 20px 18px; }}
.stat .k {{
  font-family:var(--mono); font-size:10.5px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--muted); display:block; margin-bottom:10px;
}}
.stat .v {{
  font-family:var(--mono); font-size:38px; font-weight:600; letter-spacing:-.03em;
  font-variant-numeric:tabular-nums; line-height:1; display:block;
}}
.stat .f {{ font-size:12.5px; color:var(--ink2); display:block; margin-top:9px; font-family:var(--mono); }}
.stat .d {{ font-size:13px; color:var(--muted); display:block; margin-top:7px; }}
.meter {{ height:3px; background:var(--s0); margin-top:14px; border-radius:2px; overflow:hidden; }}
.meter i {{ display:block; height:100%; background:var(--bar); border-radius:2px; }}

/* ---- controls ---- */
.controls {{
  display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin:0 0 16px;
}}
.tg {{
  display:inline-flex; align-items:center; gap:7px; cursor:pointer;
  font-family:var(--mono); font-size:11.5px; letter-spacing:.04em;
  padding:7px 12px; border:1px solid var(--line); border-radius:3px;
  background:var(--surface); color:var(--ink2); user-select:none;
}}
.tg:hover {{ border-color:var(--muted); color:var(--ink); }}
.tg input {{ accent-color:var(--bar); margin:0; width:13px; height:13px; }}
.tg:focus-within {{ outline:2px solid var(--focus); outline-offset:2px; }}

/* ---- map ---- */
.mapgrid {{ display:grid; grid-template-columns:1.55fr 1fr; gap:28px; align-items:start; }}
@media (max-width:900px) {{ .mapgrid {{ grid-template-columns:1fr; }} }}

.figure {{
  position:relative; background:var(--sea);
  border:1px solid var(--line); border-radius:3px; overflow:hidden;
}}
.figure svg.mainmap {{ display:block; width:100%; height:auto; }}
.pref {{ stroke:var(--surface); stroke-width:1.6; vector-effect:non-scaling-stroke;
         transition:opacity .1s linear; }}
.pref.hot {{ stroke:var(--ink); stroke-width:2.2; }}
.n0 {{ fill:var(--s0); }} .n1 {{ fill:var(--s1); }} .n2 {{ fill:var(--s2); }}
.n3 {{ fill:var(--s3); }} .n4 {{ fill:var(--s4); }}
.hatch {{ fill:url(#hatch); opacity:0; pointer-events:none; transition:opacity .12s linear; }}
body.mark-gaps .hatch {{ opacity:1; }}
/* 직접 라벨은 항목 2개 이상인 5곳에만. 색은 아래 칠 밝기에 맞춰 모드별로 지정. */
.clab {{
  font-family:var(--mono); font-size:19px; font-weight:640;
  font-variant-numeric:tabular-nums; text-anchor:middle; dominant-baseline:central;
  pointer-events:none; paint-order:stroke fill;
  stroke-width:3.6px; stroke-linejoin:round;
}}
.clab.lab-mid {{ fill:#fff; stroke:#0d366b; }}
.clab.lab-hi  {{ fill:#fff; stroke:#0d366b; }}
@media (prefers-color-scheme:dark) {{
  :root:where(:not([data-theme="light"])) .clab.lab-hi {{ fill:#0d2444; stroke:#dceafd; }}
}}
:root[data-theme="dark"] .clab.lab-hi {{ fill:#0d2444; stroke:#dceafd; }}
.dot {{ fill:var(--pt); stroke:var(--surface); stroke-width:2; vector-effect:non-scaling-stroke; }}
.dots {{ opacity:0; pointer-events:none; transition:opacity .12s linear; }}
body.show-dots .dots {{ opacity:1; pointer-events:auto; }}

.insetbox {{
  position:absolute; left:2%; top:2%; width:20.5%;
  border:1px solid var(--line); border-radius:2px;
  background:var(--sea); padding:6px 6px 4px;
}}
.insetbox svg {{ display:block; width:100%; height:auto; }}
.insetbox .cap {{
  font-family:var(--mono); font-size:9.5px; letter-spacing:.06em;
  color:var(--ink2); text-align:center; margin-top:2px; line-height:1.3;
}}
@media (max-width:520px) {{ .insetbox {{ width:30%; }} .insetbox .cap {{ font-size:8px; }} }}

.tip {{
  position:absolute; z-index:6; pointer-events:none; opacity:0;
  transform:translate(-50%,-100%); transition:opacity .08s linear;
  background:var(--surface); border:1px solid var(--line); border-radius:3px;
  padding:9px 11px; min-width:132px; max-width:230px;
  box-shadow:0 4px 16px rgba(0,0,0,.14);
}}
.tip.on {{ opacity:1; }}
.tip .t {{ font-size:13.5px; font-weight:640; letter-spacing:-.01em; }}
.tip .t span {{ font-family:var(--mono); font-size:10.5px; color:var(--muted); font-weight:400; margin-left:5px; }}
.tip .m {{ font-family:var(--mono); font-size:11px; color:var(--ink2); margin-top:5px;
           font-variant-numeric:tabular-nums; }}
.tip .c {{ font-size:12px; color:var(--ink2); margin-top:6px; padding-top:6px;
           border-top:1px solid var(--line-soft); line-height:1.5; }}
.tip .none {{ color:var(--muted); font-style:normal; }}

/* ---- legend: 지도 우하단 빈 해역에 배치 (충돌 검증: left66% top74% 무충돌) ---- */
.legend {{
  position:absolute; left:66%; top:74%; right:2.5%;
  background:color-mix(in srgb, var(--sea) 88%, transparent);
  backdrop-filter:blur(2px);
}}
@supports not (backdrop-filter:blur(2px)) {{ .legend {{ background:var(--sea); }} }}
@media (max-width:620px) {{
  .legend {{ position:static; left:auto; top:auto; right:auto;
             padding:12px 12px 14px; border-top:1px solid var(--line);
             background:var(--surface); backdrop-filter:none; }}
}}
.lgt {{ font-family:var(--mono); font-size:10.5px; letter-spacing:.12em;
        text-transform:uppercase; color:var(--muted); margin-bottom:8px; }}
.ramp {{ display:flex; gap:2px; }}
.ramp div {{ flex:1; }}
.ramp i {{ display:block; height:14px; border-radius:1px; }}
.ramp span {{ display:block; font-family:var(--mono); font-size:10.5px;
              color:var(--ink2); margin-top:5px; text-align:center;
              font-variant-numeric:tabular-nums; }}
.lgnote {{ display:flex; align-items:center; gap:7px; margin-top:12px;
           font-family:var(--mono); font-size:11px; color:var(--ink2); }}
.lgnote .sw {{ width:11px; height:11px; border-radius:50%; background:var(--pt);
               border:2px solid var(--surface); box-shadow:0 0 0 1px var(--line); flex:none; }}

/* ---- rail: bars ---- */
.rail {{ display:flex; flex-direction:column; gap:26px; }}
.bars {{ display:flex; flex-direction:column; gap:3px; margin:0; padding:0; list-style:none; }}
.bars li {{ display:grid; grid-template-columns:78px 1fr 22px; gap:9px; align-items:center;
            cursor:default; padding:1px 3px; border-radius:2px; }}
.bars li:hover, .bars li:focus-visible {{ background:var(--s0); outline:none; }}
.bars li:focus-visible {{ box-shadow:0 0 0 2px var(--focus); }}
.bars .nm {{ font-size:12.5px; color:var(--ink2); text-align:right; white-space:nowrap;
             overflow:hidden; text-overflow:ellipsis; }}
.bars li:hover .nm {{ color:var(--ink); }}
.bars .tr {{ background:var(--line-soft); height:9px; border-radius:2px; overflow:hidden; }}
.bars .tr i {{ display:block; height:100%; background:var(--bar); border-radius:2px; }}
.bars .ct {{ font-family:var(--mono); font-size:11.5px; color:var(--ink2);
             font-variant-numeric:tabular-nums; text-align:right; }}

.chips {{ display:flex; flex-wrap:wrap; gap:5px; margin:0; padding:0; list-style:none; }}
.chips li {{
  font-family:var(--mono); font-size:11.5px; color:var(--ink2);
  border:1px solid var(--line); border-radius:2px; padding:3px 7px;
  background:var(--surface);
}}
.chips li.big {{ border-color:var(--pt); color:var(--ink); }}

/* ---- callout ---- */
.callout {{
  border-left:2px solid var(--bar); background:var(--surface);
  padding:16px 18px; border-radius:0 3px 3px 0; margin-top:20px;
}}
.callout p {{ margin:0; font-size:14px; color:var(--ink2); }}
.callout p + p {{ margin-top:9px; }}
.callout b {{ color:var(--ink); font-weight:620; }}

/* ---- table ---- */
.tscroll {{ overflow-x:auto; border:1px solid var(--line); border-radius:3px; background:var(--surface); }}
table {{ border-collapse:collapse; width:100%; min-width:640px; font-size:13px; }}
caption {{ text-align:left; padding:0 0 12px; font-size:13.5px; color:var(--muted); }}
th, td {{ padding:8px 12px; text-align:left; border-bottom:1px solid var(--line-soft); }}
thead th {{
  font-family:var(--mono); font-size:10.5px; letter-spacing:.08em; text-transform:uppercase;
  color:var(--muted); font-weight:500; border-bottom:1px solid var(--line);
  position:sticky; top:0; background:var(--surface); z-index:1;
}}
tbody tr:last-child td {{ border-bottom:0; }}
tbody tr:hover {{ background:var(--s0); }}
td.num {{ font-family:var(--mono); font-variant-numeric:tabular-nums; text-align:right; color:var(--ink2); }}
td.ja {{ font-size:12px; color:var(--muted); }}
td.cl {{ font-size:12.5px; color:var(--ink2); }}
.pill {{
  display:inline-block; font-family:var(--mono); font-size:10px; letter-spacing:.06em;
  padding:2px 6px; border-radius:2px; white-space:nowrap;
}}
.pill.y {{ background:var(--bar); color:#fff; }}
.pill.n {{ background:var(--s0); color:var(--ink2); }}
:root[data-theme="dark"] .pill.y, :root:where(:not([data-theme="light"])) .pill.y {{ color:#0b1017; }}

footer {{ margin-top:56px; padding-top:22px; border-top:1px solid var(--line); }}
footer p {{ font-family:var(--mono); font-size:11.5px; color:var(--muted);
            margin:0 0 6px; line-height:1.7; }}
@media (prefers-reduced-motion:reduce) {{ * {{ transition:none !important; }} }}
</style>

<div class="wrap">

<p class="eyebrow">260804 해외국가·도시 리스트 · 일본 37행 분석</p>
<h1>일본 도시 리스트는 행정구역을 얼마나 덮고 있나</h1>
<p class="dek">
  리스트의 일본 항목은 국가 1행 + 도시 36행입니다. "몇 %를 커버하나"는
  <b>어느 계층을 분모로 두느냐에 따라 2%에서 66%까지</b> 달라집니다.
  세 숫자를 함께 봐야 하는 이유가 여기 있습니다.
</p>

<div class="stats">
  <div class="stat">
    <span class="k">광역 · 도도부현</span>
    <span class="v">51.1<span style="font-size:19px">%</span></span>
    <span class="f">24 / 47</span>
    <span class="d">한국의 17개 시·도에 대응하는 실제 최상위 행정단위</span>
    <div class="meter"><i style="width:51.1%"></i></div>
  </div>
  <div class="stat">
    <span class="k">인구 가중</span>
    <span class="v">66.2<span style="font-size:19px">%</span></span>
    <span class="f">8,246 / 12,456 만명</span>
    <span class="d">커버된 24개 도도부현의 인구 합계 (2023년 기준 추정)</span>
    <div class="meter"><i style="width:66.2%"></i></div>
  </div>
  <div class="stat">
    <span class="k">기초 · 시정촌</span>
    <span class="v">2.0<span style="font-size:19px">%</span></span>
    <span class="f">35 / 1,718</span>
    <span class="d">한국의 226개 시·군·구에 대응하는 기초자치단체</span>
    <div class="meter"><i style="width:2%"></i></div>
  </div>
</div>

<section>
  <h2>커버 영역 지도</h2>
  <p class="sub">
    색 농도는 해당 도도부현에 포함된 도시 항목 수입니다. 회색은 항목이 하나도 없는 지역입니다.
    지도와 목록은 서로 연동됩니다 — 한쪽을 가리키면 다른 쪽도 함께 표시됩니다.
  </p>

  <div class="controls">
    <label class="tg"><input type="checkbox" id="t-dots" checked> 도시 마커 36개</label>
    <label class="tg"><input type="checkbox" id="t-gaps"> 미커버 23개 지역 강조</label>
  </div>

  <div class="mapgrid">
    <div>
      <div class="figure" id="fig">
        <svg class="mainmap" viewBox="0 0 {main['w']} {main['h']}" role="img"
             aria-label="일본 도도부현 커버리지 지도. 47개 도도부현 중 24개에 도시 항목이 있습니다. 정확한 수치는 아래 표를 참고하세요.">
          <defs>
            <pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse"
                     patternTransform="rotate(45)">
              <rect width="6" height="6" fill="transparent"/>
              <line x1="0" y1="0" x2="0" y2="6" stroke="currentColor"
                    stroke-width="1.5" opacity=".5"/>
            </pattern>
          </defs>
          <g id="g-pref"></g>
          <g id="g-hatch" style="color:var(--pt)"></g>
          <g id="g-dots" class="dots"></g>
          <g id="g-lab"></g><!-- 라벨은 마커 위에 -->

        </svg>

        <div class="insetbox">
          <svg viewBox="0 0 {inset['w']} {inset['h']}" role="img" aria-label="오키나와 본도 인셋">
            <g id="g-oki"></g>
            <g id="g-oki-dot" class="dots"></g>
          </svg>
          <div class="cap">오키나와<br>별도 축척</div>
        </div>

        <div class="legend">
          <div class="lgt">도시 항목 수</div>
          <div class="ramp">
            <div><i style="background:var(--s0)"></i><span>0</span></div>
            <div><i style="background:var(--s1)"></i><span>1</span></div>
            <div><i style="background:var(--s2)"></i><span>2</span></div>
            <div><i style="background:var(--s3)"></i><span>3–4</span></div>
            <div><i style="background:var(--s4)"></i><span>5+</span></div>
          </div>
          <div class="lgnote"><span class="sw"></span> 도시 항목 위치 (36개)</div>
        </div>

        <div class="tip" id="tip" aria-hidden="true"></div>
      </div>
    </div>

    <div class="rail">
      <div>
        <h2 style="font-size:16px">항목이 몰린 5곳</h2>
        <p class="sub" style="margin-bottom:12px">
          커버된 24곳 중 2개 이상을 가진 곳은 다섯 곳뿐입니다.
        </p>
        <ul class="bars" id="bars"></ul>
      </div>
      <div>
        <h2 style="font-size:16px">1개씩 있는 19곳</h2>
        <p class="sub" style="margin-bottom:12px">광역 대표 도시 하나로만 대표되는 지역입니다.</p>
        <ul class="chips" id="chips-one"></ul>
      </div>
      <div>
        <h2 style="font-size:16px">항목이 없는 23곳</h2>
        <p class="sub" style="margin-bottom:12px">
          테두리 표시는 인구 200만 이상 — 규모 대비 누락이 큰 지역입니다. 숫자는 인구(만).
        </p>
        <ul class="chips" id="chips"></ul>
      </div>
    </div>
  </div>

  <div class="callout">
    <p><b>지도가 보여주는 건 편중입니다.</b> 규슈·홋카이도·간사이는 촘촘하고,
      도호쿠 6개 현은 센다이 하나로 끝납니다. 혼슈 중앙부(나가노·기후·이시카와·도야마·니가타)는
      통째로 비어 있는데, 이 띠가 지도에서 가장 넓은 회색 덩어리입니다.</p>
    <p>수도권에서도 <b>사이타마와 지바가 빠져 있습니다.</b> 두 곳 모두 인구 600만 이상이고,
      특히 지바는 나리타 공항과 도쿄 디즈니리조트를 품고 있어 실제 방문 규모가 큽니다.</p>
  </div>
</section>

<section>
  <h2>정령지정도시 기준 — 13 / 20</h2>
  <p class="sub">일본의 광역시급 대도시 20곳 중 리스트에 있는 곳과 없는 곳.</p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px" class="seirei">
    <div>
      <div class="lgt" style="margin-bottom:8px">포함 13곳</div>
      <ul class="chips">{''.join(f'<li>{c}</li>' for c in SEIREI_COV)}</ul>
    </div>
    <div>
      <div class="lgt" style="margin-bottom:8px">누락 7곳</div>
      <ul class="chips">{''.join(f'<li class="big">{c}</li>' for c in SEIREI_MIS)}</ul>
    </div>
  </div>
</section>

<section>
  <h2>전체 47개 도도부현</h2>
  <div class="tscroll">
    <table>
      <caption>지도와 동일한 데이터입니다. JIS 코드 순.</caption>
      <thead><tr>
        <th style="width:38px">코드</th><th>도도부현</th><th>일본어</th>
        <th style="text-align:right">인구(만)</th><th style="text-align:right">항목</th>
        <th>포함된 도시</th><th style="width:60px">상태</th>
      </tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>
</section>

<footer>
  <p>폴리곤 · dataofjapan/land japan.geojson (47 features, MultiPolygon) — RDP 단순화 ε=0.006°, 면적 0.0012°² 미만 도서 생략</p>
  <p>투영 · 등거리 원통도법, 경도에 cos(중위도) 압축 적용. 오키나와는 별도 축척 인셋. 아마미 군도(가고시마현)는 본토 지도 범위 밖으로 생략</p>
  <p>인구 · 2023년 기준 도도부현 추계 반올림값의 합계이므로 총계는 실제와 수십만 단위 차이가 있을 수 있음</p>
  <p>분모 · 시정촌 1,718 = 시 792 + 정 743 + 촌 183 (도쿄 23특별구 제외). 도시 항목 36개 중 오키나와는 광역·지역 단위로 보여 기초자치단체 집계에서 제외</p>
</footer>
</div>

<script>
const D = {PAYLOAD};
const {{main, inset, meta}} = D;

const cls = n => n===0?'n0':n===1?'n1':n===2?'n2':n<=4?'n3':'n4';
const esc = s => String(s).replace(/[&<>"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));

/* ---------- 지도: 폴리곤 ---------- */
const gP = document.getElementById('g-pref');
const gH = document.getElementById('g-hatch');
const gL = document.getElementById('g-lab');
gP.innerHTML = main.prefs.map(p =>
  `<path class="pref ${{cls(p.n)}}" d="${{p.d}}" data-id="${{p.id}}"></path>`).join('');
gH.innerHTML = main.prefs.filter(p => p.n===0).map(p =>
  `<path class="hatch" d="${{p.d}}"></path>`).join('');
/* 직접 라벨은 항목 2개 이상인 곳만 (선택적 라벨링 — 1개짜리 19곳은 색으로만) */
gL.innerHTML = main.prefs.filter(p => p.n>=2).map(p =>
  `<text class="clab ${{p.n>=3?'lab-hi':'lab-mid'}}" x="${{p.lx}}" y="${{p.ly}}">${{p.n}}</text>`).join('');

/* 오키나와 인셋 */
const oki = inset.prefs[0];
document.getElementById('g-oki').innerHTML =
  `<path class="pref ${{cls(oki.n)}}" d="${{oki.d}}" data-id="47"></path>`;
document.getElementById('g-oki-dot').innerHTML =
  inset.cities.map(c => `<circle class="dot" cx="${{c.x}}" cy="${{c.y}}" r="4"></circle>`).join('');

/* 도시 마커 */
document.getElementById('g-dots').innerHTML = main.cities.map(c =>
  `<circle class="dot" cx="${{c.x}}" cy="${{c.y}}" r="6"
     data-city="${{esc(c.name)}}" data-pid="${{c.pid}}"></circle>`).join('');

/* ---------- 우측 레일 ---------- */
const byId = Object.fromEntries(meta.all.map(p => [p.id, p]));
const multi = meta.all.filter(p => p.n>=2).sort((a,b) => b.n-a.n || b.pop-a.pop);
const ones  = meta.all.filter(p => p.n===1).sort((a,b) => b.pop-a.pop);
const mx = Math.max(...multi.map(p => p.n));
document.getElementById('bars').innerHTML = multi.map(p =>
  `<li tabindex="0" data-id="${{p.id}}" aria-label="${{p.ko}} ${{p.n}}개">
     <span class="nm">${{p.ko}}</span>
     <span class="tr"><i style="width:${{p.n/mx*100}}%"></i></span>
     <span class="ct">${{p.n}}</span>
   </li>`).join('');

document.getElementById('chips-one').innerHTML = ones.map(p =>
  `<li data-id="${{p.id}}">${{p.ko}}</li>`).join('');

document.getElementById('chips').innerHTML = meta.all.filter(p => p.n===0)
  .sort((a,b) => b.pop-a.pop)
  .map(p => `<li class="${{p.pop>=200?'big':''}}" data-id="${{p.id}}">${{p.ko}}<span style="opacity:.55;margin-left:5px">${{p.pop}}</span></li>`).join('');

/* ---------- 표 ---------- */
document.getElementById('tbody').innerHTML = meta.all.map(p => `<tr data-id="${{p.id}}">
  <td class="num">${{String(p.id).padStart(2,'0')}}</td>
  <td>${{p.ko}}</td><td class="ja">${{p.ja}}</td>
  <td class="num">${{p.pop.toLocaleString()}}</td>
  <td class="num">${{p.n}}</td>
  <td class="cl">${{p.cities.length ? p.cities.join(', ') : '—'}}</td>
  <td><span class="pill ${{p.n?'y':'n'}}">${{p.n?'포함':'없음'}}</span></td>
</tr>`).join('');

/* ---------- 토글 ---------- */
const body = document.body;
const bind = (id, cn) => {{
  const el = document.getElementById(id);
  const sync = () => body.classList.toggle(cn, el.checked);
  el.addEventListener('change', sync); sync();
}};
bind('t-dots','show-dots'); bind('t-gaps','mark-gaps');

/* ---------- 호버 연동 + 툴팁 ---------- */
const fig = document.getElementById('fig'), tip = document.getElementById('tip');
let hot = null;

function paint(id) {{
  if (hot === id) return;
  hot = id;
  document.querySelectorAll('.pref.hot').forEach(e => e.classList.remove('hot'));
  document.querySelectorAll('.bars li[aria-current]').forEach(e => e.removeAttribute('aria-current'));
  if (id == null) return;
  document.querySelectorAll(`.pref[data-id="${{id}}"]`).forEach(e => e.classList.add('hot'));
  const li = document.querySelector(`.bars li[data-id="${{id}}"]`);
  if (li) {{ li.setAttribute('aria-current','true'); li.style.background='var(--s0)'; }}
}}
function unpaintBars() {{
  document.querySelectorAll('.bars li').forEach(e => e.style.background='');
}}

function showTip(html, cx, cy) {{
  tip.innerHTML = html;
  const r = fig.getBoundingClientRect();
  let x = cx - r.left, y = cy - r.top - 12;
  x = Math.max(72, Math.min(r.width - 72, x));
  if (y < 78) y = cy - r.top + 96;
  tip.style.left = x + 'px'; tip.style.top = y + 'px';
  tip.classList.add('on');
}}
const hideTip = () => {{ tip.classList.remove('on'); }};

function prefTip(p) {{
  return `<div class="t">${{p.ko}}<span>${{p.ja}}</span></div>
    <div class="m">인구 ${{p.pop.toLocaleString()}}만 · 항목 ${{p.n}}개</div>
    <div class="c">${{p.cities.length
      ? p.cities.join(', ')
      : '<span class="none">리스트에 항목 없음</span>'}}</div>`;
}}

fig.addEventListener('pointermove', e => {{
  const dot = e.target.closest('.dot[data-city]');
  if (dot) {{
    const p = byId[dot.dataset.pid];
    paint(p.id);
    showTip(`<div class="t">${{dot.dataset.city}}</div>
             <div class="m">${{p.ko}} · ${{p.ja}}</div>`, e.clientX, e.clientY);
    return;
  }}
  const pa = e.target.closest('.pref');
  if (pa) {{
    const p = byId[pa.dataset.id];
    paint(p.id); showTip(prefTip(p), e.clientX, e.clientY);
  }} else {{ paint(null); unpaintBars(); hideTip(); }}
}});
fig.addEventListener('pointerleave', () => {{ paint(null); unpaintBars(); hideTip(); }});

document.querySelectorAll('.bars li, .chips li, #tbody tr').forEach(el => {{
  const id = el.dataset.id;
  if (!id) return;
  const on = () => paint(+id);
  const off = () => {{ paint(null); unpaintBars(); }};
  el.addEventListener('pointerenter', on);
  el.addEventListener('pointerleave', off);
  el.addEventListener('focus', on);
  el.addEventListener('blur', off);
}});
</script>
"""

open("japan_coverage.html", "w", encoding="utf-8").write(HTML)
import os
print(f"japan_coverage.html {os.path.getsize('japan_coverage.html')/1024:.0f} KB")
print(f"커버 {meta['prefCovered']}/47 = {meta['prefPct']}% · 인구 {meta['popPct']}%")
print(f"막대 {len([p for p in meta['all'] if p['n']>0])}개 · 칩 {len([p for p in meta['all'] if p['n']==0])}개")
