# 게시 도구 — 파일 복사 + 게시판 JSON 갱신 + 커밋(+push)을 한 번에.
# 구글 사이트의 게시판·홈 소식은 boards/*.json을 fetch해 그리므로,
# 이 스크립트만 돌리면 사이트 편집기를 열 필요가 없다.
#
# 사용:
#   py _tools/pub.py lecture "강의.html" 1-1-2 "미분이라는 관점" "Phase I 언어 · Part 1 수학" [--push]
#   py _tools/pub.py news    "글.html"  2026-08-20-topic "제목" ["부제"] [--yr 2026.08.20] [--push]
#   py _tools/pub.py diary   "글.html"  2026-08-20       "제목"          [--push]
#   py _tools/pub.py paper   "글.html"  paper-slug       "제목" ["부제"] [--push]
#   py _tools/pub.py note    news "글 없는 한 줄 소식" [--yr 2026.08] [--push]
#
# 규약: slug는 영문·숫자·하이픈. 날짜 slug는 YYYY-MM-DD(-주제). 글 본문은 «투과» 글 틀
# (_tools/post-template.html)을 복사해 쓰면 조판이 맞는다.
import sys, json, shutil, subprocess, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = 'https://dugoni.github.io'
BOARDS = {'lecture': 'lectures', 'news': 'news', 'diary': 'diary', 'paper': 'papers', 'exp': 'exp'}
DEST = {'lecture': 'lectures', 'news': 'posts', 'diary': 'posts', 'paper': 'posts', 'exp': 'posts'}


def die(msg):
    sys.exit('오류: ' + msg + '\n(사용법은 파일 머리 주석 참조)')


def load(board):
    p = ROOT / 'boards' / (board + '.json')
    return p, json.loads(p.read_text(encoding='utf-8')) if p.exists() else (p, [])


def save(p, rows):
    p.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def commit(msg, push):
    # push 직전에 링크 점검 — 죽은 링크를 실은 채 나가지 않는다
    chk = subprocess.run([sys.executable, str(ROOT / '_tools' / 'check.py')])
    if chk.returncode != 0:
        die('링크 점검 실패 — 위 목록을 고친 뒤 다시 실행')
    subprocess.run(['git', '-C', str(ROOT), 'add', '-A'], check=True)
    r = subprocess.run(['git', '-C', str(ROOT), 'commit', '-m', msg])
    if r.returncode != 0:
        print('커밋할 변경 없음 — 이미 최신.')
    if push:
        subprocess.run(['git', '-C', str(ROOT), 'push'], check=True)
        print('push 완료 — 몇 분 안에 반영된다. 게시된 주소를 브라우저에서 한 번 확인할 것.')
    else:
        print('남은 일: git push')


def main(argv):
    # 기본이 push다 — "남은 일"을 만들지 않는다. 막고 싶을 때만 --no-push.
    push = '--no-push' not in argv
    argv = [a for a in argv if a not in ('--push', '--no-push')]
    yr = None
    if '--yr' in argv:
        i = argv.index('--yr'); yr = argv[i + 1]; del argv[i:i + 2]
    if not argv:
        die('종류가 없다 (lecture/news/diary/paper/note)')
    kind = argv[0]

    if kind == 'note':
        if len(argv) < 3:
            die('note <게시판:news|diary|papers|lectures> "한 줄"')
        board = argv[1] if argv[1] in ('news', 'diary', 'papers', 'lectures', 'exp') else BOARDS.get(argv[1])
        if not board:
            die('모르는 게시판: ' + argv[1])
        p, rows = load(board)
        rows.insert(0, {'yr': yr or datetime.date.today().strftime('%Y.%m'), 't': argv[2]})
        save(p, rows)
        commit(f'{board} 한 줄: {argv[2][:30]}', push)
        return

    if kind not in BOARDS:
        die('모르는 종류: ' + kind)
    if len(argv) < 4:
        die(f'{kind} <파일> <slug> "<제목>" ["<부제>"]')
    src, slug, title = pathlib.Path(argv[1]), argv[2], argv[3]
    sub = argv[4] if len(argv) > 4 else None
    if not src.is_file():
        die('파일 없음: ' + str(src))

    dest_dir = DEST[kind]
    dst = ROOT / dest_dir / (slug + '.html')
    dst.parent.mkdir(exist_ok=True)
    shutil.copyfile(src, dst)

    if yr is None:
        yr = ('L' + slug.replace('-', '.')) if kind == 'lecture' else datetime.date.today().strftime('%Y.%m.%d')
    entry = {'yr': yr, 't': title}
    if sub:
        entry['s'] = sub
    entry['href'] = f'{BASE}/{dest_dir}/{slug}.html'

    p, rows = load(BOARDS[kind])
    rows.insert(0, entry)
    save(p, rows)

    print('복사:', dst)
    print('주소:', entry['href'])
    commit(f'{BOARDS[kind]} 게시: {title[:40]} ({slug})', push)


if __name__ == '__main__':
    main(sys.argv[1:])
