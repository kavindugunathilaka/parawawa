"""Client logos: trim, whiten light backgrounds, resize and save as assets/clients/<slug>.webp.

Run when the client sends new or changed logos: python tools/build_client_logos.py
Then update the logo wall in index.html (section #client-logos) and run python tools/build.py.
"""
import json, os, shutil
from PIL import Image, ImageChops

ROOT = r'D:\VOYAGE\parawewa\parawawa'
SRC = os.path.join(ROOT, 'tools', 'source', 'client-logos')   # originals as supplied by the client
OUT = os.path.join(ROOT, 'assets', 'clients')
KEEP_SRC = os.path.join(ROOT, 'tools', 'source', 'client-logos')
os.makedirs(OUT, exist_ok=True)

# (source file prefix, slug, display name)
LOGOS = [
    ('Nithya Papers', 'nithya-papers', 'Nithya Papers & Board Lanka (Pvt) Ltd – BOI Zone, Horana'),
    ('Commercial Credit', 'commercial-credit', 'Commercial Credit – Kiribathgoda'),
    ('Jaykay', 'jaykay-keells', 'Jaykay Marketing Services (Pvt) Ltd – Keells'),
    ('JSW', 'jsw-apparels', 'JSW Apparels (Pvt) Ltd – Panadura'),
    ('Access Engineering', 'access-engineering', 'Access Engineering – Port of Colombo'),
    ('ITD Cementation', 'itd-cementation', 'ITD Cementation India Limited – Port of Colombo'),
    ('MAGA', 'maga-engineering', 'MAGA Engineering (Pvt) Ltd – KMTT Project, Ampitiya'),
    ('Wish', 'wish-fertility-hospital', 'Wish Fertility Hospital – Maharagama'),
    ('Lanka Tiles', 'lanka-tiles', 'Lanka Tiles – Ranala'),
    ('Cisco', 'cisco-speciality-packaging', 'Cisco Speciality Packaging (Pvt) Ltd'),
    ('Elastomeric', 'elastomeric-engineering', 'Elastomeric Engineering Co. Ltd – Horana'),
    ('Gislaved', 'gislaved-gummi', 'Gislaved Gummi Lanka (Pvt) Ltd – Bokundara'),
    ('Lanka Precision', 'lanka-precision-engineering', 'Lanka Precision Engineering (Pvt) Ltd – Mulleriyawa'),
    ('LOTEK', 'lotek', 'LOTEK (Pvt) Ltd'),
    ('Atire', 'atire', 'Atire (Pvt) Ltd'),
    ('Ethimale', 'ethimale-plantation', 'Ethimale Plantation – Siyambalanduwa, Monaragala'),
    ('avid Pieris', 'david-pieris', 'David Pieris Holdings (Pvt) Ltd – GLO Camp, Welikanda'),
    ('Roo Mansala', 'roo-mansala', 'Roo Mansala Boutique Villa – Sigiriya'),
    ('Kottawa', 'kottawa-dharmapala-mv', 'WP/JP/ Kottawa Dharmapala Maha Vidyalaya'),
    ('Methodist', 'methodist-college', 'Methodist College – Rawathawatta, Moratuwa'),
]


def trim(im, tol=28):
    """Crop away a uniform border (the colour of the top-left corner)."""
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
    diff = ImageChops.difference(im, bg).convert('L').point(lambda v: 255 if v > tol else 0)
    box = diff.getbbox()
    if not box:
        return im
    w, h = im.size
    pad = int(max(box[2] - box[0], box[3] - box[1]) * 0.06)
    return im.crop((max(0, box[0] - pad), max(0, box[1] - pad), min(w, box[2] + pad), min(h, box[3] + pad)))


def whiten(im, tol=38):
    """Light, off-white or grey backgrounds become pure white so the logo sits cleanly on a white card."""
    w, h = im.size
    corners = [im.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    if min(sum(c) / 3 for c in corners) < 200:
        return im                                   # dark or coloured backgrounds are part of the logo
    px = im.load()
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y]
            if min(r, g, b) > 255 - 60 and max(r, g, b) - min(r, g, b) < tol:
                px[x, y] = (255, 255, 255)
    return im


files = os.listdir(SRC)
result = {}
for prefix, slug, name in LOGOS:
    src = [f for f in files if f.startswith(prefix)]
    assert len(src) == 1, (prefix, src)
    im = Image.open(os.path.join(SRC, src[0])).convert('RGB')
    im = whiten(im)
    im = trim(im)
    im.thumbnail((360, 160), Image.LANCZOS)
    out = os.path.join(OUT, slug + '.webp')
    im.save(out, 'WEBP', quality=86, method=6)
    result[slug] = {'name': name, 'w': im.size[0], 'h': im.size[1], 'kb': round(os.path.getsize(out) / 1024, 1), 'src': src[0]}

json.dump(result, open(os.path.join(ROOT, 'tools', 'source', 'client-logos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in result.items():
    print(f"{k:30} {v['w']}x{v['h']}  {v['kb']} KB")
print('total KB', round(sum(v['kb'] for v in result.values()), 1))
