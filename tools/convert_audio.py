"""
Convert MP3 files to OGG using ffmpeg. If pydub is installed, use it; otherwise fall back to `ffmpeg` CLI.
Usage:
    python tools/convert_audio.py img/music.mp3 img/music.ogg

"""
import sys
import os

try:
    from pydub import AudioSegment
    HAVE_PYDUB = True
except Exception:
    HAVE_PYDUB = False


def convert(src, dst):
    if HAVE_PYDUB:
        sound = AudioSegment.from_file(src)
        sound.export(dst, format='ogg')
        print(f'Converted {src} -> {dst} using pydub')
        return
    # fallback to ffmpeg commandline
    cmd = f'ffmpeg -y -i "{src}" "{dst}"'
    print('Running:', cmd)
    os.system(cmd)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: convert_audio.py <src> <dst>')
        sys.exit(1)
    src = sys.argv[1]
    dst = sys.argv[2]
    convert(src, dst)
