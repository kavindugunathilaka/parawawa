"""llms.txt, 404.html and feed.xml. Run via tools/build.py."""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_articles as ba  # noqa: E402
from compare import COMPARE  # noqa: E402
from systems import SYSTEMS  # noqa: E402

SITE, VER, esc, HEADER, FOOTER = ba.SITE, ba.VER, ba.esc, ba.HEADER, ba.FOOTER


def llms():
    lines = [
        '# Parawewa',
        '',
        '> Parawewa is a Sri Lankan manufacturer and installer of the patented layer-base eco bio septic tank system (Sri Lanka Patent #10848, invented in 1996). '
        'It comes in two options: Option A, a gravity-fed system that uses 0% electricity, and Option B, a sealed submersible pump seal type for high water table land. '
        'Every installation carries a 10-year written manufacturer warranty. Parawewa won 1st place at the 2018 Presidential Innovation Awards (Sri Lanka) and a Silver Medal at iCAN 2019 (Canada).',
        '',
        'Head office: 143/2 Kesbewa Kindelpitiya, Bandaragama Rd, Piliyandala 10300, Sri Lanka.',
        'Phone: 0777 347 620, 074 060 4936. Email: info@parawawa.lk. WhatsApp: +94 77 734 7620.',
        'Prices are not published; quotes follow a free site inspection. The site is in English.',
        '',
        '## Systems',
    ]
    for sy in SYSTEMS:
        lines.append(f"- [{sy['name']}]({SITE}/systems/{sy['slug']}/): {sy['metaDescription']}")
    lines += ['', '## Comparisons']
    for c in COMPARE:
        lines.append(f"- [{c['name']}]({SITE}/compare/{c['slug']}/): {c['metaDescription']}")
    lines += ['', '## Knowledge articles']
    for a in ba.ARTICLES:
        lines.append(f"- [{a['title']}]({ba.url_of(a)}): {a['metaDescription']}")
    lines += [
        '',
        '## Company and tools',
        f'- [Home page]({SITE}/): system options, why Parawewa, who it suits, projects, team, certificates, tank-size calculator, FAQ and quote form.',
        f'- [Knowledge hub]({SITE}/articles.html): all 20 articles.',
        f'- [Team]({SITE}/#team): managing director, directors and engineering lead.',
        f'- [FAQ]({SITE}/#faq): answers on electricity, warranty, high water table, CEA compliance and sizing.',
        '',
    ]
    open('llms.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))


def not_found():
    header = HEADER.replace('nav-link active">Articles', 'nav-link">Articles')
    out = f'''<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page not found | Parawewa</title>
  <meta name="robots" content="noindex, follow">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" type="image/png" sizes="192x192" href="/assets/icons/icon-192.png">
  <link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
  <link rel="preload" href="/assets/fonts/inter-tight-2.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/instrument-sans-1.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/fonts/fonts.css?v={VER}">
  <link rel="stylesheet" href="/assets/fa/fa-subset.css?v={VER}">
  <link rel="stylesheet" href="/style.css?v={VER}">
</head>
<body>

  {header.strip()}

  <main id="main">
    <section class="section">
      <div class="container article-wrap">
        <span class="section-tag">ERROR 404</span>
        <h1 class="article-h1">That page isn&rsquo;t here</h1>
        <p class="article-lede">The link may be old or mistyped. These pages will get you back on track.</p>
        <div class="system-actions">
          <a href="/" class="btn btn-primary"><i class="fas fa-home"></i> Home page</a>
          <a href="/articles.html" class="btn btn-secondary"><i class="fas fa-book-open"></i> Knowledge hub</a>
          <a href="/#contact" class="btn btn-secondary open-quote-modal"><i class="fas fa-paper-plane"></i> Get a free quote</a>
        </div>
        <ul class="notfound-links">
          <li><a href="/systems/gravity-fed-bio-septic-tank/">Option A: gravity-fed bio septic tank</a></li>
          <li><a href="/systems/pump-seal-type-bio-septic-tank/">Option B: pump seal type for high water table land</a></li>
          <li><a href="/compare/parawewa-vs-aerated-package-plants/">Parawewa vs Aerated Package Plants</a></li>
        </ul>
      </div>
    </section>
  </main>

  {FOOTER.strip()}

  <script src="/app.js?v={VER}" defer></script>
</body>
</html>
'''
    open('404.html', 'w', encoding='utf-8', newline='\n').write(out)


def feed():
    def rfc822(iso):
        return datetime.strptime(iso, '%Y-%m-%d').strftime('%a, %d %b %Y 08:00:00 +0530')

    items = ''
    for a in sorted(ba.ARTICLES, key=lambda x: x['published'], reverse=True):
        items += f'''    <item>
      <title>{esc(a['title'])}</title>
      <link>{ba.url_of(a)}</link>
      <guid isPermaLink="true">{ba.url_of(a)}</guid>
      <pubDate>{rfc822(a['published'])}</pubDate>
      <category>{esc(ba.category(a).title())}</category>
      <description>{esc(a['metaDescription'])}</description>
    </item>
'''
    out = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Parawewa Knowledge Hub</title>
    <link>{SITE}/articles.html</link>
    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Guides on eco bio septic tanks, groundwater protection, gravity and pump options, and Sri Lanka Patent #10848.</description>
    <language>en</language>
    <lastBuildDate>{rfc822(max(a['modified'] for a in ba.ARTICLES))}</lastBuildDate>
{items}  </channel>
</rss>
'''
    open('feed.xml', 'w', encoding='utf-8', newline='\n').write(out)


def main():
    llms()
    not_found()
    feed()
    print('built llms.txt, 404.html, feed.xml')


if __name__ == '__main__':
    main()
