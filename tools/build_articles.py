"""Build the knowledge-hub pages from content/articles.json.

Generates:
  articles/<slug>/index.html   one real, indexable page per article
  articles-meta.js             light metadata used by the homepage grid
  articles.html                hub grid + JSON-LD (between the BUILD markers)
  index.html                   3 featured cards (between the BUILD markers)
  sitemap.xml                  home, hub and every article

Run:  python tools/build_articles.py
Edit articles in content/articles.json, never in the generated files.
"""
import html, json, os, re, struct
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SITE = 'https://parawawa.lk'
ARTICLES = json.load(open('content/articles.json', encoding='utf-8'))
BY_ID = {a['id']: a for a in ARTICLES}

import sys
sys.path.insert(0, os.path.join(ROOT, 'content'))
from systems import SYSTEMS  # noqa: E402
from compare import COMPARE  # noqa: E402

index_html = open('index.html', encoding='utf-8', newline='').read().replace('\r\n', '\n')
VER = re.search(r'style\.css\?v=([0-9A-Za-z]+)', index_html).group(1)


def esc(s):
    return html.escape(s, quote=True)


def fmt_date(iso):
    d = datetime.strptime(iso, '%Y-%m-%d')
    return d.strftime('%b ') + str(d.day) + d.strftime(', %Y')


def img_size(path):
    with open(path, 'rb') as f:
        head = f.read(26)
        if head[:8] == b'\x89PNG\r\n\x1a\n':
            return struct.unpack('>II', head[16:24])
        f.seek(0)
        data = f.read()
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack('>HH', data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack('>H', data[i + 2:i + 4])[0]
    return 800, 450


def url_of(a):
    return f"{SITE}/articles/{a['slug']}/"


def path_of(a):
    return f"/articles/{a['slug']}/"


def category(a):
    return a['badge'].split('•')[-1].strip()


# ---------------------------------------------------------------- shared header / footer
def between(s, start, end):
    i = s.index(start)
    j = s.index(end, i)
    return s[i:j]


HEADER = between(index_html, '<!-- ==========================================================================\n       CORPORATE TOP CONTACT BAR',
                 '<!-- ==========================================================================\n       HERO SECTION')
FOOTER = between(index_html, '<!-- ==========================================================================\n       MOBILE STICKY BOTTOM ACTION BAR',
                 '<!-- Main JavaScript File -->')


def rootify(s):
    s = s.replace('href="#"', 'href="/"')
    s = s.replace('href="#', 'href="/#')
    s = s.replace('href="/#main"', 'href="#main"')   # skip link targets the page's own <main>
    s = s.replace('href="articles.html"', 'href="/articles.html"')
    s = s.replace('src="assets/', 'src="/assets/')
    s = s.replace('class="nav-link active"', 'class="nav-link"')
    s = s.replace('<a href="/#blog" class="nav-link">Articles', '<a href="/articles.html" class="nav-link active">Articles')
    return s


HEADER = re.sub(r'\s*<main id="main">\s*$', '\n', HEADER)   # index.html opens <main> right after the header; each page adds its own
HEADER = rootify(HEADER)
FOOTER = rootify(FOOTER)


# ---------------------------------------------------------------- content transforms
AUTOLINKS = [
    (r'\bOption A\b', '/systems/gravity-fed-bio-septic-tank/', 'gravity-fed-bio-septic-tank'),
    (r'\bOption B\b', '/systems/pump-seal-type-bio-septic-tank/', 'pump-seal-type-bio-septic-tank'),
    (r'\bgully bowser\b', '/articles/gully-bowser-emptying-not-needed-bio-septic/', 'gully-bowser-emptying-not-needed-bio-septic'),
    (r'\bCEA\b', '/articles/cea-compliance-septic-tank-sri-lanka/', 'cea-compliance-septic-tank-sri-lanka'),
    (r'\bhigh water table\b', '/articles/bio-septic-tank-high-water-table-sri-lanka/', 'bio-septic-tank-high-water-table-sri-lanka'),
    (r'Patent #10848', '/articles/sri-lanka-patent-10848-parawewa-story/', 'sri-lanka-patent-10848-parawewa-story'),
    (r'\blayer-base\b', '/articles/how-layer-base-bio-septic-tank-works/', 'how-layer-base-bio-septic-tank-works'),
    (r'\bsoakage pit\b', '/articles/septic-tank-vs-soakage-pit-sri-lanka/', 'septic-tank-vs-soakage-pit-sri-lanka'),
]
NO_LINK_TAGS = {'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'th', 'button', 'script', 'style'}


def autolink(html_str, self_slug, limit=6):
    """Link the first mention of a few key terms to the page that covers them.
    Skips headings, table headers and existing links; at most one link per text node."""
    parts = re.split(r'(<[^>]+>)', html_str)
    depth = 0
    done = {self_slug}
    n = 0
    for i, part in enumerate(parts):
        if part.startswith('<'):
            m = re.match(r'<(/?)\s*([a-zA-Z0-9]+)', part)
            if m and m.group(2).lower() in NO_LINK_TAGS and not part.endswith('/>'):
                depth = max(0, depth + (-1 if m.group(1) else 1))
            continue
        if depth or n >= limit or not part.strip():
            continue
        for pattern, href, key in AUTOLINKS:
            if key in done:
                continue
            m = re.search(pattern, part)
            if m:
                parts[i] = part[:m.start()] + f'<a href="{href}">{m.group(0)}</a>' + part[m.end():]
                done.add(key)
                n += 1
                break
    return ''.join(parts)


def body_html(a):
    c = a['content']
    c = re.sub(r'<h4[^>]*>', '<h2>', c)
    c = c.replace('</h4>', '</h2>')
    c = c.replace('href="#calculator"', 'href="/#calculator"').replace('href="#blog"', 'href="/articles.html"')
    c = re.sub(r'<i class="fas fa-robot"></i>\s*AI ANSWER CAPSULE \(AEO / GEO SUMMARY\)', '<i class="fas fa-bolt"></i> QUICK ANSWER', c)
    c = c.replace('<table', '<div class="table-scroll"><table').replace('</table>', '</table></div>')
    return autolink(c, a['slug'])


def webp(path):
    return re.sub(r'\.(jpg|jpeg|png)$', '.webp', path, flags=re.I)


def card_html(a):
    w, h = img_size(a['img'])
    contain = ' contain' if a['img'].lower().endswith('.png') else ''
    return f'''          <article class="article-card" data-article="{a['id']}">
            <div class="article-card-img{contain}">
              <img src="/{webp(a['img'])}" alt="{esc(a['imgAlt'])}" width="{w}" height="{h}" loading="lazy" decoding="async">
              <span class="article-badge badge-blue">{esc(category(a))}</span>
            </div>
            <div class="article-card-body">
              <div class="article-meta"><i class="far fa-clock"></i> {esc(a['readTime'])}</div>
              <h3 class="article-title"><a class="card-link" href="{path_of(a)}">{esc(a['title'])}</a></h3>
              <p class="article-summary">{esc(a['summary'])}</p>
              <span class="btn btn-secondary btn-block btn-sm" aria-hidden="true"><i class="fas fa-book-reader"></i> Read Full Article</span>
            </div>
          </article>
'''


def ld_dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2).replace('</', '<\\/')


# ---------------------------------------------------------------- article pages
def page(a):
    url = url_of(a)
    img_abs = f"{SITE}/{a['img']}"
    w, h = img_size(a['img'])
    author = {"@type": "Person", "@id": SITE + "/#founder", "name": "Ranjith Dharmakeerthi Mannage", "jobTitle": "Managing Director"}
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "@id": url + "#article",
                "headline": a['title'],
                "description": a['metaDescription'],
                "image": img_abs,
                "datePublished": a['published'],
                "dateModified": a['modified'],
                "inLanguage": "en",
                "articleSection": category(a).title(),
                "keywords": a['keywords'],
                "author": author,
                "publisher": {"@type": "Organization", "name": "Parawewa", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/real_logo.png"}},
                "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Knowledge Hub", "item": SITE + "/articles.html"},
                    {"@type": "ListItem", "position": 3, "name": a['title'], "item": url},
                ],
            },
        ],
    }
    related = ''.join(card_html(BY_ID[r]) for r in a['related'])
    prev_a = BY_ID.get(a['id'] - 1)
    next_a = BY_ID.get(a['id'] + 1)
    prev_link = f'<a class="article-pn" href="{path_of(prev_a)}"><span>Previous guide</span><strong>{esc(prev_a["title"])}</strong></a>' if prev_a else '<span></span>'
    next_link = f'<a class="article-pn article-pn-next" href="{path_of(next_a)}"><span>Next guide</span><strong>{esc(next_a["title"])}</strong></a>' if next_a else '<span></span>'
    head = f'''<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(a['metaTitle'])}</title>
  <meta name="description" content="{esc(a['metaDescription'])}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{url}">

  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Parawewa">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{esc(a['title'])}">
  <meta property="og:description" content="{esc(a['metaDescription'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{img_abs}">
  <meta property="og:image:width" content="{w}">
  <meta property="og:image:height" content="{h}">
  <meta property="og:image:alt" content="{esc(a['imgAlt'])}">
  <meta property="article:published_time" content="{a['published']}">
  <meta property="article:modified_time" content="{a['modified']}">
  <meta property="article:section" content="{esc(category(a).title())}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(a['title'])}">
  <meta name="twitter:description" content="{esc(a['metaDescription'])}">
  <meta name="twitter:image" content="{img_abs}">

  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="192x192" href="/assets/icons/icon-192.png">
  <link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
  <link rel="alternate" type="application/rss+xml" title="Parawewa Knowledge Hub" href="/feed.xml">
  <link rel="preload" href="/assets/fonts/inter-tight-2.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/instrument-sans-1.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fa/fa-solid.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/fonts/fonts.css?v={VER}">
  <link rel="stylesheet" href="/assets/fa/fa-subset.css?v={VER}">
  <link rel="stylesheet" href="/style.css?v={VER}">

  <script type="application/ld+json">
{ld_dump(graph)}
  </script>
</head>
<body>

  {HEADER.strip()}

  <main id="main">
    <header class="article-hero">
      <div class="container article-wrap">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li><a href="/articles.html">Knowledge Hub</a></li>
            <li aria-current="page">{esc(a['metaTitle'].split(' | ')[0])}</li>
          </ol>
        </nav>
        <span class="section-tag">{esc(category(a))}</span>
        <h1 class="article-h1">{esc(a['title'])}</h1>
        <p class="article-lede">{esc(a['summary'])}</p>
        <p class="article-byline">By <a href="/#team">Ranjith Dharmakeerthi Mannage</a> &middot; Updated {fmt_date(a['modified'])} &middot; {esc(a['readTime'])}</p>
      </div>
    </header>

    <article class="container article-wrap article-main">
      <figure class="article-figure">
        <img src="/{webp(a['img'])}" alt="{esc(a['imgAlt'])}" width="{w}" height="{h}" fetchpriority="high" decoding="async">
      </figure>

      <div class="article-body">
{body_html(a)}
      </div>

      <aside class="article-cta" aria-label="Request a quote">
        <div>
          <h2>Planning a septic system for your site?</h2>
          <p>Talk to the Parawewa team about <a href="/systems/gravity-fed-bio-septic-tank/">Option A (gravity-fed)</a> or <a href="/systems/pump-seal-type-bio-septic-tank/">Option B (pump seal type)</a> for your property. Every installation comes with a 10-year written warranty.</p>
        </div>
        <div class="article-cta-actions">
          <a href="/#contact" class="btn btn-primary open-quote-modal"><i class="fas fa-paper-plane"></i> Get Free Quote</a>
          <a href="tel:+94777347620" class="btn btn-secondary"><i class="fas fa-phone"></i> 0777 347 620</a>
        </div>
      </aside>

      <nav class="article-pn-row" aria-label="More guides">
        {prev_link}
        {next_link}
      </nav>
    </article>

    <section class="section section-alt article-related">
      <div class="container">
        <div class="section-header section-header-left">
          <span class="section-tag">KEEP READING</span>
          <h2 class="section-title">Related <span class="text-blue">guides</span></h2>
        </div>
        <div class="grid grid-auto-lg">
{related}        </div>
        <p style="margin-top: 1.5rem;"><a href="/articles.html" class="btn btn-secondary"><i class="fas fa-th-large"></i> All 20 knowledge articles</a></p>
      </div>
    </section>
  </main>

  {FOOTER.strip()}

  <script src="/app.js?v={VER}" defer></script>
</body>
</html>
'''
    os.makedirs(f"articles/{a['slug']}", exist_ok=True)
    open(f"articles/{a['slug']}/index.html", 'w', encoding='utf-8', newline='\n').write(head)


# ---------------------------------------------------------------- patch helpers
def patch(path, start, end, new):
    s = open(path, encoding='utf-8', newline='').read()
    crlf = '\r\n' in s
    s = s.replace('\r\n', '\n')
    i = s.index(start) + len(start)
    j = s.index(end, i)
    s = s[:i] + '\n' + new + '        ' + s[j:]
    if crlf:
        s = s.replace('\n', '\r\n')
    open(path, 'w', encoding='utf-8', newline='').write(s)


def hub_card(a):
    return f'''        <article class="article-hub-card" data-article="{a['id']}">
          <span class="article-hub-badge" style="background: var(--accent-blue-light); color: var(--accent-blue-dark);">{esc(a['badge'])}</span>
          <h3 class="article-hub-title"><a class="card-link" href="{path_of(a)}">{esc(a['title'])}</a></h3>
          <p class="article-hub-desc">{esc(a['summary'])}</p>
          <span class="btn btn-secondary btn-sm" aria-hidden="true"><i class="fas fa-book-reader"></i> Read Full Guide</span>
        </article>
'''


def main():
    for a in ARTICLES:
        page(a)

    # light metadata for the homepage "show all 20" grid
    meta = {str(a['id']): {'slug': a['slug'], 'badge': category(a), 'title': a['title'], 'img': a['img'], 'imgAlt': a['imgAlt'], 'readTime': a['readTime'], 'summary': a['summary']} for a in ARTICLES}
    open('articles-meta.js', 'w', encoding='utf-8', newline='\n').write(
        '/* Generated by tools/build_articles.py - do not edit. */\nwindow.ARTICLES_META = ' + json.dumps(meta, ensure_ascii=False) + ';\n')

    # homepage featured cards
    patch('index.html', '<!-- BUILD:FEATURED:START -->', '<!-- BUILD:FEATURED:END -->',
          ''.join(card_html(BY_ID[i]) for i in (1, 2, 3)))

    # hub: shared header and footer (same markup as every other page)
    patch('articles.html', '<!-- BUILD:HEADER:START -->', '<!-- BUILD:HEADER:END -->', HEADER.strip() + '\n\n  ')
    patch('articles.html', '<!-- BUILD:FOOTER:START -->', '<!-- BUILD:FOOTER:END -->', FOOTER.strip() + '\n\n  ')

    # hub grid + schema
    patch('articles.html', '<!-- BUILD:HUB:START -->', '<!-- BUILD:HUB:END -->', ''.join(hub_card(a) for a in ARTICLES))
    hub_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "CollectionPage", "@id": SITE + "/articles.html#page", "url": SITE + "/articles.html", "name": "20 Essential Articles on Eco Bio Septic Systems", "inLanguage": "en", "isPartOf": {"@id": SITE + "/#organization"}},
            {"@type": "ItemList", "name": "Parawewa Knowledge Hub Articles", "itemListElement": [
                {"@type": "ListItem", "position": a['id'], "name": a['title'], "url": url_of(a)} for a in ARTICLES]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Knowledge Hub", "item": SITE + "/articles.html"}]},
        ],
    }
    patch('articles.html', '<!-- BUILD:HUBLD:START -->\n  <script type="application/ld+json">', '</script>\n  <!-- BUILD:HUBLD:END -->', ld_dump(hub_ld) + '\n  ')

    # sitemap
    urls = [
        (SITE + '/', '2026-10-06', 'weekly', '1.0', f'''
    <image:image>
      <image:loc>{SITE}/assets/real_hero.jpg</image:loc>
      <image:title>Parawewa Patented Eco Bio Septic Tank System Sri Lanka</image:title>
    </image:image>'''),
        (SITE + '/articles.html', '2026-10-06', 'weekly', '0.9', ''),
    ] + [(f"{SITE}/compare/{c['slug']}/", c['modified'], 'monthly', '0.9', f'''
    <image:image>
      <image:loc>{SITE}/{c['img']}</image:loc>
      <image:title>{esc(c['imgAlt'])}</image:title>
    </image:image>''') for c in COMPARE] + [(f"{SITE}/systems/{sy['slug']}/", sy['modified'], 'monthly', '0.9', f'''
    <image:image>
      <image:loc>{SITE}/{sy['img']}</image:loc>
      <image:title>{esc(sy['imgAlt'])}</image:title>
    </image:image>''') for sy in SYSTEMS] + [(url_of(a), a['modified'], 'monthly', '0.8', f'''
    <image:image>
      <image:loc>{SITE}/{a['img']}</image:loc>
      <image:title>{esc(a['imgAlt'])}</image:title>
    </image:image>''') for a in ARTICLES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    for loc, lm, cf, pr, extra in urls:
        sm += f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lm}</lastmod>\n    <changefreq>{cf}</changefreq>\n    <priority>{pr}</priority>{extra}\n  </url>\n'
    sm += '</urlset>\n'
    open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(sm)
    print('built', len(ARTICLES), 'article pages + hub + featured + sitemap + articles-meta.js')


if __name__ == '__main__':
    main()
