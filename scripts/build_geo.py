#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""일본 47개 도도부현 GeoJSON -> 단순화 + 투영 + SVG path 생성"""
import json, math, sys

SRC = "japan.geojson"
OUT = "japan_map.json"

# ---- 1. 도도부현 메타: JIS코드 -> (한글명, 일본어명, 인구(만명), 커버 도시 리스트) ----
PREF = {
 1: ("홋카이도","北海道",505,["삿포로","하코다테","오타루","아사히카와","후라노","비에이","노보리베츠"]),
 2: ("아오모리","青森県",118,[]),
 3: ("이와테","岩手県",116,[]),
 4: ("미야기","宮城県",226,["센다이"]),
 5: ("아키타","秋田県",91,[]),
 6: ("야마가타","山形県",102,[]),
 7: ("후쿠시마","福島県",176,[]),
 8: ("이바라키","茨城県",283,[]),
 9: ("도치기","栃木県",190,[]),
10: ("군마","群馬県",190,[]),
11: ("사이타마","埼玉県",734,[]),
12: ("지바","千葉県",627,[]),
13: ("도쿄","東京都",1408,["도쿄"]),
14: ("가나가와","神奈川県",924,["요코하마","하코네"]),
15: ("니가타","新潟県",213,[]),
16: ("도야마","富山県",100,[]),
17: ("이시카와","石川県",111,[]),
18: ("후쿠이","福井県",75,[]),
19: ("야마나시","山梨県",80,[]),
20: ("나가노","長野県",202,[]),
21: ("기후","岐阜県",195,[]),
22: ("시즈오카","静岡県",355,["시즈오카"]),
23: ("아이치","愛知県",748,["나고야"]),
24: ("미에","三重県",174,[]),
25: ("시가","滋賀県",141,[]),
26: ("교토","京都府",254,["교토"]),
27: ("오사카","大阪府",878,["오사카"]),
28: ("효고","兵庫県",540,["고베"]),
29: ("나라","奈良県",130,["나라"]),
30: ("와카야마","和歌山県",90,[]),
31: ("돗토리","鳥取県",54,["요나고"]),
32: ("시마네","島根県",65,[]),
33: ("오카야마","岡山県",186,["오카야마"]),
34: ("히로시마","広島県",276,["히로시마"]),
35: ("야마구치","山口県",131,["시모노세키"]),
36: ("도쿠시마","徳島県",70,[]),
37: ("가가와","香川県",93,["다카마쓰"]),
38: ("에히메","愛媛県",130,["마쓰야마"]),
39: ("고치","高知県",67,[]),
40: ("후쿠오카","福岡県",512,["후쿠오카","기타큐슈"]),
41: ("사가","佐賀県",80,["사가"]),
42: ("나가사키","長崎県",128,["나가사키","대마도"]),
43: ("구마모토","熊本県",171,["구마모토"]),
44: ("오이타","大分県",110,["오이타","벳푸","유후","히타"]),
45: ("미야자키","宮崎県",105,["미야자키"]),
46: ("가고시마","鹿児島県",156,["가고시마"]),
47: ("오키나와","沖縄県",146,["오키나와"]),
}

# ---- 2. 도시 좌표 (lon, lat) ----
CITIES = [
 ("삿포로",141.354,43.062,1),("하코다테",140.729,41.768,1),("오타루",141.002,43.191,1),
 ("아사히카와",142.365,43.771,1),("후라노",142.383,43.342,1),("비에이",142.466,43.589,1),
 ("노보리베츠",141.107,42.413,1),("센다이",140.870,38.268,4),("도쿄",139.692,35.690,13),
 ("요코하마",139.638,35.444,14),("하코네",139.024,35.233,14),("시즈오카",138.383,34.976,22),
 ("나고야",136.906,35.181,23),("교토",135.768,35.011,26),("오사카",135.502,34.694,27),
 ("고베",135.196,34.690,28),("나라",135.805,34.685,29),("요나고",133.331,35.428,31),
 ("오카야마",133.935,34.662,33),("히로시마",132.455,34.385,34),("시모노세키",130.941,33.958,35),
 ("다카마쓰",134.047,34.343,37),("마쓰야마",132.766,33.839,38),("후쿠오카",130.402,33.590,40),
 ("기타큐슈",130.875,33.883,40),("사가",130.299,33.249,41),("나가사키",129.878,32.750,42),
 ("대마도",129.291,34.203,42),("구마모토",130.708,32.803,43),("오이타",131.613,33.238,44),
 ("벳푸",131.491,33.285,44),("유후",131.427,33.180,44),("히타",130.941,33.321,44),
 ("미야자키",131.424,31.911,45),("가고시마",130.557,31.596,46),("오키나와",127.681,26.212,47),
]

# ---- 3. Ramer-Douglas-Peucker (반복 구현) ----
def rdp(pts, eps):
    n = len(pts)
    if n < 4:
        return pts
    keep = [False]*n
    keep[0] = keep[n-1] = True
    stack = [(0, n-1)]
    e2 = eps*eps
    while stack:
        a, b = stack.pop()
        if b <= a+1:
            continue
        ax, ay = pts[a]; bx, by = pts[b]
        dx = bx-ax; dy = by-ay
        den = dx*dx + dy*dy
        best = -1.0; bi = -1
        for i in range(a+1, b):
            px, py = pts[i]
            if den == 0.0:
                d2 = (px-ax)**2 + (py-ay)**2
            else:
                t = ((px-ax)*dx + (py-ay)*dy)/den
                if t < 0.0: t = 0.0
                elif t > 1.0: t = 1.0
                qx = ax + t*dx; qy = ay + t*dy
                d2 = (px-qx)**2 + (py-qy)**2
            if d2 > best:
                best = d2; bi = i
        if best > e2:
            keep[bi] = True
            stack.append((a, bi)); stack.append((bi, b))
    return [pts[i] for i in range(n) if keep[i]]

def ring_area(pts):
    s = 0.0
    n = len(pts)
    for i in range(n):
        x1,y1 = pts[i]; x2,y2 = pts[(i+1)%n]
        s += x1*y2 - x2*y1
    return abs(s)/2.0

# ---- 4. 로드 & 링 추출 ----
data = json.load(open(SRC, encoding="utf-8"))
raw = {}   # id -> list of rings (lon,lat)
for f in data["features"]:
    pid = f["properties"]["id"]
    g = f["geometry"]
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    rings = []
    for poly in polys:
        for ring in poly:
            rings.append([(float(c[0]), float(c[1])) for c in ring])
    raw[pid] = rings

EPS       = float(sys.argv[1]) if len(sys.argv) > 1 else 0.006
MIN_AREA  = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0012

def prep(rings, bbox):
    """bbox=(lonmin,lonmax,latmin,latmax) 안의 링만 단순화하여 반환"""
    lo0, lo1, la0, la1 = bbox
    out = []
    for r in rings:
        xs = [p[0] for p in r]; ys = [p[1] for p in r]
        cx = sum(xs)/len(xs); cy = sum(ys)/len(ys)
        if not (lo0 <= cx <= lo1 and la0 <= cy <= la1):
            continue
        if ring_area(r) < MIN_AREA:
            continue
        s = rdp(r, EPS)
        if len(s) >= 4:
            out.append(s)
    return out

MAIN_BBOX  = (128.0, 146.5, 30.4, 46.2)   # 본토 (오키나와/아마미 제외)
INSET_BBOX = (126.4, 128.6, 25.6, 27.0)   # 오키나와 본도 인셋

main_rings  = {pid: prep(rings, MAIN_BBOX)  for pid, rings in raw.items()}
inset_rings = {47: prep(raw[47], INSET_BBOX)}

# 라벨 위치 수동 보정 (투영 px). 알고리즘 결과를 눈으로 확인한 뒤에만 채운다.
LABEL_NUDGE = {}

def inside(pt, ring):
    """ray casting point-in-polygon"""
    x, y = pt; c = False; n = len(ring)
    j = n-1
    for i in range(n):
        xi, yi = ring[i]; xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj-xi)*(y-yi)/((yj-yi) or 1e-12) + xi:
            c = not c
        j = i
    return c

def label_point(ring, dots):
    """폴리곤 내부에서 (경계까지 거리, 마커까지 거리) 중 최솟값을 최대화하는 점.
    도시 마커 뭉치에 라벨이 가려지는 것을 막는다."""
    xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
    x0, x1 = min(xs), max(xs); y0, y1 = min(ys), max(ys)
    G = 46
    best = None; bestscore = -1.0
    for gi in range(1, G):
        px = x0 + (x1-x0)*gi/G
        for gj in range(1, G):
            py = y0 + (y1-y0)*gj/G
            if not inside((px, py), ring):
                continue
            db = min((px-rx)**2 + (py-ry)**2 for rx, ry in ring) ** 0.5
            if dots:
                dd = min((px-dx)**2 + (py-dy)**2 for dx, dy in dots) ** 0.5
                score = min(db, dd * 0.85)      # 마커 회피에 약간 더 가중
            else:
                score = db
            if score > bestscore:
                bestscore = score; best = (px, py)
    return best

def build(ringmap, width, pad, cities_filter):
    allpts = [p for rs in ringmap.values() for r in rs for p in r]
    lo = min(p[0] for p in allpts); hi = max(p[0] for p in allpts)
    la = min(p[1] for p in allpts); lb = max(p[1] for p in allpts)
    k = math.cos(math.radians((la+lb)/2.0))          # 경도 압축계수
    sx = (hi-lo)*k; sy = (lb-la)
    scale = (width - 2*pad)/sx
    height = sy*scale + 2*pad
    def proj(lon, lat):
        return (pad + (lon-lo)*k*scale, pad + (lb-lat)*scale)
    def centroid(pr):
        """투영좌표 링의 폴리곤 중심(shoelace). 퇴화 시 점 평균."""
        a = 0.0; cx = 0.0; cy = 0.0; n = len(pr)
        for i in range(n):
            x1,y1 = pr[i]; x2,y2 = pr[(i+1)%n]
            cr = x1*y2 - x2*y1
            a += cr; cx += (x1+x2)*cr; cy += (y1+y2)*cr
        if abs(a) < 1e-9:
            return (sum(p[0] for p in pr)/n, sum(p[1] for p in pr)/n)
        a *= 0.5
        return (cx/(6*a), cy/(6*a))

    prefs = []
    for pid, rs in sorted(ringmap.items()):
        if not rs:
            continue
        d = []; projected = []
        for r in rs:
            pr = [proj(lon,lat) for lon,lat in r]
            projected.append(pr)
            seg = [("M" if i==0 else "L") + f"{x:.1f} {y:.1f}" for i,(x,y) in enumerate(pr)]
            d.append(" ".join(seg) + "Z")
        big = max(projected, key=ring_area)          # 최대 링 = 본섬/본토
        ko, ja, pop, cl = PREF[pid]
        if len(cl) >= 2:
            # 라벨을 실제로 그리는 곳만 마커 회피 계산 (5곳)
            dots_p = [proj(lon, lat) for nm, lon, lat, cp in CITIES if cp == pid]
            lp = label_point(big, dots_p)
            lx, ly = lp if lp else centroid(big)
        else:
            lx, ly = centroid(big)
        dxy = LABEL_NUDGE.get(pid, (0.0, 0.0))
        prefs.append({"id":pid,"ko":ko,"ja":ja,"pop":pop,"n":len(cl),
                      "cities":cl,"d":" ".join(d),
                      "lx":round(lx+dxy[0],1),"ly":round(ly+dxy[1],1)})
    pts = []
    for nm, lon, lat, pid in CITIES:
        if not cities_filter(pid): continue
        x,y = proj(lon,lat)
        pts.append({"name":nm,"pid":pid,"x":round(x,1),"y":round(y,1)})
    return {"w":round(width,1),"h":round(height,1),"prefs":prefs,"cities":pts}

main  = build(main_rings,  1000, 14, lambda pid: pid != 47)
inset = build(inset_rings,  190,  8, lambda pid: pid == 47)

# 본토 지도에서 오키나와(47) 폴리곤 제거
main["prefs"] = [p for p in main["prefs"] if p["id"] != 47]

# 미커버 도도부현도 전부 포함되어야 함 -> 누락 확인
have = {p["id"] for p in main["prefs"]} | {47}
missing = sorted(set(PREF) - have)

covered = sorted([pid for pid in PREF if PREF[pid][3]])
tot_pop = sum(PREF[p][2] for p in PREF)
cov_pop = sum(PREF[p][2] for p in covered)

meta = {
  "prefTotal": 47, "prefCovered": len(covered),
  "cityCount": len(CITIES),
  "popTotal": tot_pop, "popCovered": cov_pop,
  "popPct": round(cov_pop/tot_pop*100, 1),
  "prefPct": round(len(covered)/47*100, 1),
  "muniTotal": 1718,
  "all": [{"id":pid,"ko":PREF[pid][0],"ja":PREF[pid][1],
           "pop":PREF[pid][2],"n":len(PREF[pid][3]),
           "cities":PREF[pid][3]} for pid in sorted(PREF)],
}
json.dump({"main":main,"inset":inset,"meta":meta}, open(OUT,"w",encoding="utf-8"),
          ensure_ascii=False, separators=(",",":"))

# --- 검증 1: 오키나와 인셋 박스가 본토 폴리곤과 겹치는지 ---
INSET_BOX = (0.02*main["w"], 0.02*main["h"],
             0.02*main["w"] + inset["w"] + 16, 0.02*main["h"] + inset["h"] + 30)
hits = []
for pid, rs in main_rings.items():
    for r in rs:
        for lon, lat in r:
            allp = [p for rr in main_rings.values() for q in rr for p in q]
            break
        break
    break
lo = min(p[0] for p in [q for rr in main_rings.values() for r in rr for q in r])
hi = max(p[0] for p in [q for rr in main_rings.values() for r in rr for q in r])
la = min(p[1] for p in [q for rr in main_rings.values() for r in rr for q in r])
lb = max(p[1] for p in [q for rr in main_rings.values() for r in rr for q in r])
k = math.cos(math.radians((la+lb)/2.0))
scale = (main["w"] - 2*14)/((hi-lo)*k)
for pid, rs in main_rings.items():
    for r in rs:
        for lon, lat in r:
            x = 14 + (lon-lo)*k*scale; y = 14 + (lb-lat)*scale
            if INSET_BOX[0] <= x <= INSET_BOX[2] and INSET_BOX[1] <= y <= INSET_BOX[3]:
                hits.append((pid, round(x), round(y)))
print(f"인셋박스 {tuple(round(v) for v in INSET_BOX)} 충돌점: {len(hits)}"
      + (f" -> {sorted(set(h[0] for h in hits))}" if hits else " (없음)"))

# --- 검증 1b: 그려지는 라벨(n>=2)과 해당 도시 마커 간 최소거리 ---
print("라벨-마커 간격 (n>=2, 목표 >14px):")
for p in main["prefs"]:
    if p["n"] < 2: continue
    ds = [math.dist((p["lx"],p["ly"]),(c["x"],c["y"]))
          for c in main["cities"] if c["pid"] == p["id"]]
    flag = "OK " if ds and min(ds) > 14 else "!! "
    print(f"  {flag}{p['ko']:5s} n={p['n']}  최근접 {min(ds):5.1f}px")

# --- 검증 2: 라벨끼리 너무 가까운 쌍 (커버된 것만, r<22px) ---
lab = [(p["ko"], p["lx"], p["ly"]) for p in main["prefs"] if p["n"] >= 2]  # 실제로 그리는 것만
close = [(a[0], b[0], round(math.dist((a[1],a[2]),(b[1],b[2]))))
         for i,a in enumerate(lab) for b in lab[i+1:]
         if math.dist((a[1],a[2]),(b[1],b[2])) < 22]
print(f"라벨 근접쌍(<22px): {close if close else '없음'}")

npts = sum(len(r) for rs in main_rings.values() for r in rs)
print(f"eps={EPS} minarea={MIN_AREA}")
print(f"본토 폴리곤 {len(main['prefs'])}개 / 인셋 {len(inset['prefs'])}개 / 점 {npts}")
print(f"본토 viewBox {main['w']} x {main['h']}  인셋 {inset['w']} x {inset['h']}")
print(f"누락 도도부현: {missing}")
print(f"커버 {len(covered)}/47 = {meta['prefPct']}%  인구 {cov_pop}/{tot_pop} = {meta['popPct']}%")
import os; print(f"출력 {os.path.getsize(OUT)/1024:.0f} KB")
