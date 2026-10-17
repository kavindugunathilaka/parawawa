"""Sinhala home page: si/index.html, generated from index.html + content/si_strings.py.

The English page is the source: every text node and alt/placeholder/aria-label is swapped for its Sinhala string,
relative URLs are made root-absolute, and the head/meta/JSON-LD are localised. Untranslated English left in the page
is listed at the end (run `python tools/build_si.py`); fix by adding the string to content/si_strings.py.
Run via tools/build.py after the article build (the featured article cards are generated there).
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'content'))
import si_strings as S  # noqa: E402

SITE = 'https://parawawa.lk'
SI_URL = SITE + '/si/'
SINHALA = re.compile('[඀-෿]')
LATIN = re.compile('[A-Za-z]{3}')
NAME = 'Ranjith Dharmakeerthi Mannage'


def norm(t):
    t = html.unescape(t).replace('\xa0', ' ')
    t = t.replace('’', "'").replace('—', '-').replace('–', '-')
    return re.sub(r'\s+', ' ', t).strip()


TEXT = {norm(k): v for k, v in S.TEXT}
ATTR = {norm(k): v for k, v in S.ATTR}
KEEP = {norm(k) for k in S.KEEP}
missing_text, missing_attr = [], []


def translate_text(m):
    if m.group(1) is None:
        return m.group(0)
    raw = m.group(1)
    key = norm(raw)
    if not key:
        return raw
    if key in TEXT:
        lead = re.match(r'\s*', raw).group(0)
        trail = re.search(r'\s*$', raw).group(0)
        return lead + html.escape(TEXT[key], quote=False) + trail
    if key not in KEEP and LATIN.search(key) and not SINHALA.search(key) and not re.fullmatch(r'[\w.+-]+@[\w.-]+', key):
        missing_text.append(key)
    return raw


def translate_attr(m):
    key = norm(m.group(2))
    if key in ATTR:
        return f'{m.group(1)}="{html.escape(ATTR[key], quote=True)}"'
    if LATIN.search(key) and not SINHALA.search(key) and key not in KEEP:
        missing_attr.append(key)
    return m.group(0)


def set_meta(s, attr, name, value):
    pat = re.compile(r'(<meta\s+' + attr + r'="' + re.escape(name) + r'"\s+content=")[^"]*(")')
    assert pat.search(s), name
    return pat.sub(lambda m: m.group(1) + html.escape(value, quote=True) + m.group(2), s, count=1)


# --------------------------------------------------------------------------- JSON-LD
FAQ_ANSWERS = [  # English fragment keys, in the order they appear in each FAQ answer
    ["Unlike imported mechanical STPs which require continuous 24/7 electricity to run air blowers and need frequent mechanical servicing, Parawewa engineered by Parawewa provides two flexible options:",
     "Option A (100% Gravity-Fed with no electricity for normal ground)", "and",
     "Option B (Seal Type Parawewa System for high ground water table)", ", both featuring a",
     "10-Year written manufacturer guarantee", "and no gully bowser emptying."],
    ["Option A (Gravity-Fed)", "operates on 100% passive natural gravity flow with no electricity, ideal for standard ground levels.",
     "Option B (Seal Type Parawewa System)", "is a water-sealed system designed specifically for high water table lands (such as Negombo, Ja-Ela, Wattala or Mathugama) where natural gravity discharge is restricted. It uses some electricity, but less than mechanical STPs."],
    ["Parawewa issues an official", "10-Year written manufacturer guarantee certificate",
     "covering structural tank integrity, chamber sealing, and multi-stage biological layer filtration performance."],
    ["Yes! Parawewa Option B is specifically engineered for high groundwater tables, wetlands, and coastal soils (Negombo, Ja-Ela, Wattala, Mathugama, Galle). The hermetically sealed composite body prevents inward water seepage and flood backflow."],
    ["Yes, Parawewa effluent discharge is laboratory-tested to meet all Sri Lanka Central Environmental Authority (CEA) discharge guidelines (BOD & COD limits), making it suitable for commercial buildings, hotels, and apartments."],
    ["The Parawewa bio septic system was invented in 1996 by", NAME,
     ", Managing Director of Parawewa in Sri Lanka. The technology holds Sri Lanka Patent #16371."],
    ["Recommended capacity depends on your property type and number of occupants. Use our", "interactive tank sizer",
     "above for an instant approximate estimate, then request a free site inspection from Parawewa for an exact recommendation and quote."],
    ["Both. Parawewa is installed across residential, industrial, and commercial sites islandwide — including factories, retail outlets, and housing developments — with capacity sized to each site's occupancy and wastewater load. See our",
     "real project case studies", "for examples."],
]


def si_join(keys):
    return ' '.join(NAME if k == NAME else TEXT[norm(k)] for k in keys)


def localise_jsonld(block):
    data = json.loads(block)
    jd = {norm(k): v for k, v in S.JSONLD.items()}
    faq_i = [0]

    def walk(o):
        if isinstance(o, dict):
            if o.get('@type') == 'Question':
                i = faq_i[0]
                faq_i[0] += 1
                q = norm(o['name'])
                assert q in TEXT, ('FAQ question not translated', q)
                o['name'] = TEXT[q]
                o['acceptedAnswer']['text'] = si_join(FAQ_ANSWERS[i])
                return
            for k, v in list(o.items()):
                if k == 'item' and v == SITE + '/':
                    o[k] = SI_URL
                elif isinstance(v, str):
                    nv = jd.get(norm(v))
                    if nv:
                        o[k] = nv
                else:
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    assert faq_i[0] == len(FAQ_ANSWERS), faq_i[0]
    data['@graph'].append({
        '@type': 'WebPage', '@id': SI_URL + '#webpage', 'url': SI_URL, 'name': S.TITLE, 'description': S.DESCRIPTION,
        'inLanguage': 'si-LK', 'about': {'@id': SITE + '/#organization'},
    })
    return json.dumps(data, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------- page
I18N_JS = '''<script>
  window.I18N = {
    thanks: 'ස්තූතියි! ඔබගේ පණිවිඩය ලැබුණි. පරවැව ඉංජිනේරු කණ්ඩායම පැය 2ක් ඇතුළත ඔබ හා සම්බන්ධ වනු ඇත.',
    capacity: 'ලීටර් {n}',
    water: 'ලීටර් {n} / වසරකට'
  };
  </script>
  '''

FONT_LINKS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Sinhala:wght@400;500;600;700&display=swap">
  '''


def main():
    s = open('index.html', encoding='utf-8', newline='').read().replace('\r\n', '\n')
    missing_text.clear()
    missing_attr.clear()

    # --- head
    s = s.replace('<html lang="en-US">', '<html lang="si">')
    s = re.sub(r'<title>.*?</title>', '<title>' + html.escape(S.TITLE) + '</title>', s, count=1, flags=re.S)
    s = set_meta(s, 'name', 'description', S.DESCRIPTION)
    s = set_meta(s, 'name', 'keywords', S.KEYWORDS)
    s = set_meta(s, 'property', 'og:title', S.OG_TITLE)
    s = set_meta(s, 'property', 'og:description', S.DESCRIPTION)
    s = set_meta(s, 'property', 'og:url', SI_URL)
    s = set_meta(s, 'property', 'og:image:alt', S.OG_IMAGE_ALT)
    s = set_meta(s, 'property', 'og:locale', 'si_LK')
    s = set_meta(s, 'property', 'og:site_name', S.OG_SITE_NAME)
    s = set_meta(s, 'name', 'twitter:title', S.OG_TITLE)
    s = set_meta(s, 'name', 'twitter:description', S.DESCRIPTION)
    canon = '<link rel="canonical" href="' + SITE + '/">'
    assert canon in s
    s = s.replace(canon, '<link rel="canonical" href="' + SI_URL + '">\n  '
                  '<link rel="alternate" hreflang="si-LK" href="' + SI_URL + '">\n  '
                  '<link rel="alternate" hreflang="en" href="' + SITE + '/">\n  '
                  '<link rel="alternate" hreflang="x-default" href="' + SITE + '/">')
    s = s.replace('<meta property="og:locale" content="si_LK">',
                  '<meta property="og:locale" content="si_LK">\n  <meta property="og:locale:alternate" content="en_US">')
    s = s.replace('<link rel="preload" href="/assets/fonts/inter-tight-2.woff2"', FONT_LINKS + '<link rel="preload" href="/assets/fonts/inter-tight-2.woff2"', 1)

    # --- JSON-LD
    s = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)',
               lambda m: m.group(1) + '\n' + localise_jsonld(m.group(2)) + '\n  ' + m.group(3), s, count=1, flags=re.S)

    # --- visible text and attributes (script, style, comments and <title> left alone)
    body_start = s.index('<body')
    head, body = s[:body_start], s[body_start:]
    body = re.sub(r'<script.*?</script>|<style.*?</style>|<!--.*?-->|(?<=>)([^<>]+)(?=<)', translate_text, body, flags=re.S)
    body = re.sub(r'\b(alt|aria-label|placeholder|title)="([^"]*)"', translate_attr, body)

    # --- links and assets: the page lives in /si/, so make relative URLs root-absolute
    body = re.sub(r'(?<=[\s"\'(,])assets/', '/assets/', body)
    for a in ('href="style.css', 'src="app.js', 'src="articles-meta.js'):
        body = body.replace(a, a.replace('="', '="/'))
    head = head.replace('href="style.css', 'href="/style.css')
    body = body.replace('href="articles.html"', 'href="/articles.html" hreflang="en"')
    body = body.replace('<a href="#" class="logo"', '<a href="/si/" class="logo"')

    # --- the full article list is English: link to the hub instead of loading it into the page
    body, n = re.subn(r'<button class="btn btn-secondary" id="toggleAllArticlesBtn"([^>]*)>(.*?)</button>',
                      r'<a class="btn btn-secondary" href="/articles.html" hreflang="en"\1>\2</a>', body, flags=re.S)
    assert n == 1, 'article toggle button'

    # --- language switch (header + drawer) and the Sinhala UI strings for app.js
    toggle = re.compile(r'<div class="lang-toggle"[^>]*>.*?</div>')
    assert len(toggle.findall(body)) == 1, 'lang toggle'
    body = toggle.sub('<div class="lang-toggle" aria-label="භාෂාව"><a href="/" lang="en" hreflang="en" title="English">En</a>'
                      '<span class="lang-current" lang="si">සිං</span></div>', body)
    drawer = '<li><a href="/si/" class="mobile-nav-link" lang="si" hreflang="si-LK">සිංහල</a></li>'
    assert body.count(drawer) == 1, 'drawer language link'
    body = body.replace(drawer, '<li><a href="/" class="mobile-nav-link" lang="en" hreflang="en">English version</a></li>')
    foot = '<li><a href="#founder">'
    assert body.count(foot) == 1
    body = body.replace(foot, '<li><a href="/" lang="en" hreflang="en">English version</a></li>\n            ' + foot)
    body = body.replace('<script src="/articles-meta.js', I18N_JS + '<script src="/articles-meta.js', 1)

    out = head + body
    os.makedirs('si', exist_ok=True)
    open('si/index.html', 'w', encoding='utf-8', newline='\n').write(out)

    left = sorted(set(missing_text))
    print('built si/index.html')
    if left or missing_attr:
        print('UNTRANSLATED text:', len(left))
        for t in left:
            print('  T|', t[:140])
        for t in sorted(set(missing_attr)):
            print('  A|', t[:140])
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
