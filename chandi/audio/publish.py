"""Publish finished section renders: WAV -> audio/<nn>_<section>.mp3 + audio/README.md, commit, push.

  python -m chandi.audio.publish [--watch]   (--watch: poll every 5 minutes until all are done)
"""
import argparse
import json
import pathlib
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
ENGINE = 'parler-aryan'
# Gita Press order: angas, 13 adhyayas, rahasya-traya, kshamapana
SECTIONS = (['pre', 'kavacha', 'argala', 'kilaka'] + [f'ch{i}' for i in range(1, 14)]
            + ['pradhanika', 'vaikritika', 'murti', 'aparadha'])
NAMES = {'pre': 'Chandika-dhyana', 'kavacha': 'Devi-kavacha', 'argala': 'Argala-stotra',
         'kilaka': 'Kilaka-stotra', 'pradhanika': 'Pradhanika-rahasya', 'vaikritika': 'Vaikritika-rahasya',
         'murti': 'Murti-rahasya', 'aparadha': 'Aparadha-kshamapana'}
REPORTS = ROOT / 'audio' / 'reports'
BRANCH = 'claude/elegant-mccarthy-kl0egn'
TRAILER = ('\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'
           'Claude-Session: https://claude.ai/code/session_01TeGCasX6TcHUQRyqZHNLTk')


def mp3_name(sec):
    i = SECTIONS.index(sec)
    return f'{i:02d}_{NAMES.get(sec, "Adhyaya-" + sec[2:].zfill(2))}.mp3'


def run(*cmd):
    return subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True).stdout


def stats(sec):
    rep = json.loads((REPORTS / f'{sec}.json').read_text(encoding='utf-8'))
    ok = sum(x['ok'] for x in rep)
    worst = max((x['max_err'] for x in rep), default=0)
    bad = [f"{x['id']} pada {x['pada']}" for x in rep if not x['ok']]
    return ok, len(rep), worst, bad


def duration(path):
    out = run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path))
    return float(out.strip())


def write_readme():
    rows = []
    for sec in SECTIONS:
        if not (REPORTS / f'{sec}.json').exists() or not (ROOT / 'audio' / mp3_name(sec)).exists():
            continue
        ok, n, worst, bad = stats(sec)
        mins = duration(ROOT / 'audio' / mp3_name(sec)) / 60
        rows.append(f'| [{mp3_name(sec)}]({mp3_name(sec)}) | {mins:.1f} min | {ok}/{n} | {worst:.0%} | '
                    f'{", ".join(bad) or "—"} |')
    (ROOT / 'audio' / 'README.md').write_text(
        '# Recitation audio\n\n'
        'Voice: AI4Bharat Indic Parler-TTS (speaker "Aryan"). Tempo: 1 mātrā = 0.2 s.\n'
        'Every metrical pāda is time-set to its chandas (laghu 1, guru 2 mātrās, pāda-final held as guru)\n'
        'and verified by re-alignment: the measured laghu/guru pattern must equal the metre and each\n'
        'syllable must be within ±20% of its target. The table lists the result per file; pādas that\n'
        'failed after retries are named. The check covers rhythm only, not pronunciation.\n\n'
        '| File | Length | Pādas compliant | Worst syllable error | Non-compliant pādas |\n'
        '|---|---|---|---|---|\n' + '\n'.join(rows) + '\n', encoding='utf-8')


def publish_ready(readme=True, only=None):
    """Encode finished sections to audio/*.mp3 (+ audio/reports/<sec>.json), commit and push.

    Several sessions may publish to the same branch: each commits only its own files and
    rebases before pushing. Use readme=False there; the summary table is rebuilt from the
    reports by one session (`python -m chandi.audio.publish --readme-only`)."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    new = []
    for sec in SECTIONS:
        if only and sec not in only:
            continue
        wav = ROOT / 'out' / f'{sec}_{ENGINE}.wav'
        if not wav.exists() or not wav.with_suffix('.json').exists():
            continue
        mp3 = ROOT / 'audio' / mp3_name(sec)
        if not mp3.exists() or mp3.stat().st_mtime < wav.stat().st_mtime:
            run('ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-ac', '1', '-b:a', '96k',
                '-metadata', f'title={mp3_name(sec)[3:-4]}', '-metadata', 'album=Durga Saptashati (chandas)',
                str(mp3))
            (REPORTS / f'{sec}.json').write_text(wav.with_suffix('.json').read_text(encoding='utf-8'), encoding='utf-8')
            new.append(sec)
    if new or readme:
        commit(new, readme)
    return new


def commit(new, readme):
    paths = [str(ROOT / 'audio' / mp3_name(s)) for s in new] + [str(REPORTS / f'{s}.json') for s in new]
    if readme:
        write_readme()
        paths.append(str(ROOT / 'audio' / 'README.md'))
    run('git', 'add', *paths)
    if not subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=ROOT).returncode:
        return
    msg = f'Add recitation audio: {", ".join(new)}' if new else 'Update audio compliance table'
    run('git', 'commit', '-m', msg + TRAILER)
    for attempt in range(6):
        try:
            run('git', 'pull', '--rebase', 'origin', BRANCH)
            run('git', 'push', 'origin', f'HEAD:{BRANCH}')
            print('published', new or 'README', flush=True)
            return
        except subprocess.CalledProcessError as e:
            print('push retry', attempt + 1, e.stderr.strip()[-200:], flush=True)
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError('push failed after retries')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--no-readme', action='store_true', help='do not touch audio/README.md (parallel sessions)')
    ap.add_argument('--readme-only', action='store_true')
    ap.add_argument('--sections', default='', help='comma-separated; default all')
    a = ap.parse_args()
    if a.readme_only:
        commit([], True)
    else:
        publish_ready(readme=not a.no_readme, only=[x for x in a.sections.split(',') if x] or None)
