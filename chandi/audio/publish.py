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
SECTIONS = ['pre', 'kavacha', 'argala', 'kilaka'] + [f'ch{i}' for i in range(1, 14)] + ['aparadha']
NAMES = {'pre': 'Chandika-dhyana', 'kavacha': 'Devi-kavacha', 'argala': 'Argala-stotra',
         'kilaka': 'Kilaka-stotra', 'aparadha': 'Aparadha-kshamapana'}
BRANCH = 'claude/elegant-mccarthy-kl0egn'
TRAILER = ('\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n'
           'Claude-Session: https://claude.ai/code/session_01TeGCasX6TcHUQRyqZHNLTk')


def mp3_name(sec):
    i = SECTIONS.index(sec)
    return f'{i:02d}_{NAMES.get(sec, "Adhyaya-" + sec[2:].zfill(2))}.mp3'


def run(*cmd):
    return subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True).stdout


def stats(sec):
    rep = json.loads((ROOT / 'out' / f'{sec}_{ENGINE}.json').read_text(encoding='utf-8'))
    ok = sum(x['ok'] for x in rep)
    worst = max((x['max_err'] for x in rep), default=0)
    bad = [f"{x['id']} pada {x['pada']}" for x in rep if not x['ok']]
    return ok, len(rep), worst, bad


def duration(path):
    out = run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path))
    return float(out.strip())


def write_readme(done):
    rows = []
    for sec in SECTIONS:
        if sec not in done:
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


def publish_ready():
    (ROOT / 'audio').mkdir(exist_ok=True)
    done, new = [], []
    for sec in SECTIONS:
        wav = ROOT / 'out' / f'{sec}_{ENGINE}.wav'
        if not wav.exists() or not wav.with_suffix('.json').exists():
            continue
        done.append(sec)
        mp3 = ROOT / 'audio' / mp3_name(sec)
        if not mp3.exists() or mp3.stat().st_mtime < wav.stat().st_mtime:
            run('ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-ac', '1', '-b:a', '96k',
                '-metadata', f'title={mp3_name(sec)[3:-4]}', '-metadata', 'album=Durga Saptashati (chandas)',
                str(mp3))
            new.append(sec)
    if new:
        write_readme(done)
        run('git', 'add', 'audio')
        run('git', 'commit', '-m', f'Add recitation audio: {", ".join(new)}' + TRAILER)
        for attempt in range(4):
            try:
                run('git', 'push', 'origin', BRANCH)
                break
            except subprocess.CalledProcessError:
                time.sleep(2 ** (attempt + 1))
        print('published', new, flush=True)
    return done


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--watch', action='store_true')
    a = ap.parse_args()
    while True:
        done = publish_ready()
        if not a.watch or len(done) == len(SECTIONS):
            break
        time.sleep(300)
