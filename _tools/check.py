# 링크 점검기 — boards/*.json의 모든 href를 찔러 비-200을 뱉는다.
# pub.py가 push 직전에 부른다. 단독 실행: py _tools/check.py
import json, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
bad = []
checked = 0
for p in sorted((ROOT / 'boards').glob('*.json')):
    for e in json.loads(p.read_text(encoding='utf-8')):
        href = e.get('href')
        if not href:
            continue
        checked += 1
        try:
            req = urllib.request.Request(href, method='HEAD')
            with urllib.request.urlopen(req, timeout=10) as r:
                if r.status != 200:
                    bad.append((p.name, href, r.status))
        except Exception as ex:
            # 로컬에만 있고 아직 push 안 된 파일이면 저장소 안에 실물이 있는지로 대신 판정
            local = ROOT / href.split('dugoni.github.io/')[-1] if 'dugoni.github.io/' in href else None
            if local is not None and local.is_file():
                print(f'  (아직 미배포, 로컬 실물 확인: {href})')
            else:
                bad.append((p.name, href, str(ex)))

if bad:
    print(f'죽은 링크 {len(bad)}건 / 검사 {checked}건:')
    for b in bad:
        print('  -', *b)
    sys.exit(1)
print(f'링크 점검 통과 — {checked}건 모두 살아 있음.')
