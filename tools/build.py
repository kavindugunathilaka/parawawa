"""Build everything: python tools/build.py

1. generated performance assets (icon subset, self-hosted fonts, WebP copies)
2. cache-busting stamp (?v=<hash of the shipped css/js/content>) in index.html and articles.html
3. article pages, hub, home cards, system pages, comparison pages, sitemap
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.chdir(ROOT)
sys.path.insert(0, HERE)

import build_assets  # noqa: E402

build_assets.main()


def stamp():
    h = hashlib.sha1()
    for p in ('style.css', 'app.js', 'assets/fa/fa-subset.css', 'assets/fonts/fonts.css', 'content/articles.json'):
        h.update(open(p, 'rb').read())
    ver = h.hexdigest()[:10]
    for p in ('index.html', 'articles.html'):
        s = open(p, encoding='utf-8', newline='').read()
        s2 = re.sub(r'(\.(?:css|js))\?v=[0-9A-Za-z]+', r'\1?v=' + ver, s)
        if s2 != s:
            open(p, 'w', encoding='utf-8', newline='').write(s2)
    print('version:', ver)


stamp()

import build_articles  # noqa: E402  (reads the stamped version from index.html)
import build_systems  # noqa: E402
import build_compare  # noqa: E402

build_articles.main()
build_systems.main()
build_compare.main()
