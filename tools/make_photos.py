"""Make web sizes for every home photo on skyrundenver.com.

Usage: python3 tools/make_photos.py <source_dir> [name ...]   (names limit the run to those outputs)

<source_dir> holds the originals (kept out of this public repo, in Drive). Each entry below maps an
output name to a source file. Every photo gets the shared grade (tools/grade.py), a 3:2 crop, and
WebP files at 800 and 1440 pixels wide (plus 2400 for the hero once a large original is in hand).
Rule: SkyRun Denver homes only, nothing that appears on gostayready.com.
"""
import sys
from pathlib import Path
from PIL import Image, ImageFilter
try:
    import pillow_avif  # noqa: F401  (AVIF sources from the shortlist)
except ImportError:
    pass
sys.path.insert(0, str(Path(__file__).parent))
from grade import grade

OUT = Path(__file__).resolve().parent.parent / 'assets/img/homes'
# output name: (source file, horizontal focus 0..1, vertical focus 0..1)
SOURCES = {
    'parker-twilight':    ('hero-parker-twilight.jpg', .5, .5, 'twilight'),  # 6795 (Parker), hero. Track copy is 1280px; swap in the photographer's original when it arrives
    'living-kitchen':     ('ogden-int.bin', .5, .5),          # Ogden
    'townhome-exterior':  ('ogden-ext.bin', .5, .5),          # Ogden
    'backyard-hot-tub':   ('bannock-ext-avif.bin', .5, .5),   # Bannock
    'patio-firepit':      ('bannock-ext-patio.jpg', .5, .5),  # Bannock
    'brick-living':       ('west34-int.bin', .5, .5),         # West 34th
    'brick-reading-nook': ('brick-reading-nook-1440.webp', .5, .5),  # West 34th (crop made in PR 6)
    'living-lounge':      ('west45-int.bin', .5, .5),         # West 45th
    'madison-kitchen':    ('192smadison-8.jpg', .5, .5),      # 192 S Madison (Cabin Door Media)
    'madison-bedroom':    ('192smadison-24.jpg', .5, .5),
    'madison-dining':     ('192smadison-5.jpg', .5, .5),
    'madison-primary':    ('192smadison-22.jpg', .5, .5),
    'madison-bath':       ('192smadison-28.jpg', .5, .5),
    'madison-courtyard':  ('192smadison-18.jpg', .5, .5),
}

def crop32(im, fx, fy):
    w, h = im.size
    if w / h > 1.5:
        nw = round(h * 1.5); x = round((w - nw) * fx); return im.crop((x, 0, x + nw, h))
    nh = round(w / 1.5); y = round((h - nh) * fy); return im.crop((0, y, w, y + nh))

def main(src, only=()):
    src = Path(src)
    for name, (f, fx, fy, *mode) in SOURCES.items():
        if only and name not in only:
            continue
        p = src / f
        if not p.exists():
            print(f'skip {name}: {f} not in {src}'); continue
        im = crop32(Image.open(p).convert('RGB'), fx, fy)
        if mode == ['twilight']:
            # Twilight keeps its own color: the daylight grade would neutralize the sunset. Light sharpening only.
            im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=2))
        else:
            im = grade(im)
        sizes = [w for w in ((800, 1440, 2400) if name == 'parker-twilight' else (800, 1440)) if w <= max(im.width, 1440)]
        for w in sizes:
            out = im.resize((w, round(w / 1.5)), Image.LANCZOS)
            out.save(OUT / f'{name}-{w}.webp', 'WEBP', quality=82, method=6)
        print(f'{name}: {im.width}px source, sizes {sizes}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
