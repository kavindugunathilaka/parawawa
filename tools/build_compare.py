"""Build /compare/<slug>/index.html from content/compare.py. Run via tools/build.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_articles as ba  # noqa: E402
from compare import COMPARE  # noqa: E402

SITE, VER, esc, HEADER, FOOTER, ld_dump = ba.SITE, ba.VER, ba.esc, ba.HEADER, ba.FOOTER, ba.ld_dump


def page(c):
    url = f"{SITE}/compare/{c['slug']}/"
    img_abs = f"{SITE}/{c['img']}"
    w, h = ba.img_size(c['img'])
    facts = ''.join(f'<div><dt>{esc(k)}</dt><dd>{v}</dd></div>' for k, v in c['facts'])
    faq_html = ''.join(f'''
          <div class="accordion-item">
            <div class="accordion-header">
              <span>{esc(q)}</span>
              <i class="fas fa-plus accordion-icon"></i>
            </div>
            <div class="accordion-body"><p>{esc(a)}</p></div>
          </div>''' for q, a in c['faqs'])
    related = ''.join(ba.card_html(ba.BY_ID[r]) for r in c['related'])
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": url + "#page",
                "url": url,
                "name": c['name'],
                "description": c['metaDescription'],
                "inLanguage": "en",
                "datePublished": c['published'],
                "dateModified": c['modified'],
                "primaryImageOfPage": img_abs,
                "isPartOf": {"@type": "WebSite", "name": "Parawewa", "url": SITE + "/"},
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c['faqs']],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": c['crumb'], "item": url},
                ],
            },
        ],
    }
    header = HEADER.replace('nav-link active">Articles', 'nav-link">Articles').replace('class="nav-link">Technology', 'class="nav-link active">Technology')
    out = f'''<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(c['metaTitle'])}</title>
  <meta name="description" content="{esc(c['metaDescription'])}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{url}">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Parawewa">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{esc(c['name'])}">
  <meta property="og:description" content="{esc(c['metaDescription'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{img_abs}">
  <meta property="og:image:width" content="{w}">
  <meta property="og:image:height" content="{h}">
  <meta property="og:image:alt" content="{esc(c['imgAlt'])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(c['name'])}">
  <meta name="twitter:description" content="{esc(c['metaDescription'])}">
  <meta name="twitter:image" content="{img_abs}">

  <link rel="icon" type="image/png" href="/assets/real_logo.png">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="stylesheet" href="/style.css?v={VER}">

  <script type="application/ld+json">
{ld_dump(graph)}
  </script>
</head>
<body>

  {header.strip()}

  <main id="main">
    <header class="article-hero">
      <div class="container article-wrap">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li><a href="/#comparison">Comparison</a></li>
            <li aria-current="page">{esc(c['crumb'])}</li>
          </ol>
        </nav>
        <span class="section-tag">{esc(c['eyebrow'])}</span>
        <h1 class="article-h1">{esc(c['name'])}</h1>
        <p class="article-lede">{esc(c['lede'])}</p>
        <p class="article-byline">Updated {ba.fmt_date(c['modified'])}</p>
      </div>
    </header>

    <article class="container article-wrap article-main">
      <figure class="article-figure">
        <img src="/{c['img']}" alt="{esc(c['imgAlt'])}" width="{w}" height="{h}" fetchpriority="high" decoding="async">
      </figure>

      <dl class="fact-grid">{facts}</dl>

      <div class="article-body">
{c['body']}
      </div>

      <section class="system-faq" aria-labelledby="faq-heading">
        <h2 id="faq-heading" class="system-faq-title">Frequently asked questions</h2>
        <div class="accordion">{faq_html}
        </div>
      </section>

      <aside class="article-cta" aria-label="Request a quote">
        <div>
          <h2>Want a recommendation for your site?</h2>
          <p>Request a free site inspection. The Parawewa team will assess your ground, power situation and space, and tell you whether <a href="/systems/gravity-fed-bio-septic-tank/">Option A</a> or <a href="/systems/pump-seal-type-bio-septic-tank/">Option B</a> fits.</p>
        </div>
        <div class="article-cta-actions">
          <a href="/#contact" class="btn btn-primary open-quote-modal"><i class="fas fa-paper-plane"></i> Get Free Quote</a>
          <a href="tel:+94777347620" class="btn btn-secondary"><i class="fas fa-phone"></i> 0777 347 620</a>
        </div>
      </aside>
    </article>

    <section class="section section-alt article-related">
      <div class="container">
        <div class="section-header section-header-left">
          <span class="section-tag">KEEP READING</span>
          <h2 class="section-title">Related <span class="text-blue">guides</span></h2>
        </div>
        <div class="grid grid-auto-lg">
{related}        </div>
      </div>
    </section>
  </main>

  {FOOTER.strip()}

  <script src="/app.js?v={VER}" defer></script>
</body>
</html>
'''
    os.makedirs(f"compare/{c['slug']}", exist_ok=True)
    open(f"compare/{c['slug']}/index.html", 'w', encoding='utf-8', newline='\n').write(out)


def main():
    for c in COMPARE:
        assert len(c['metaTitle']) <= 62 and len(c['metaDescription']) <= 160, (len(c['metaTitle']), len(c['metaDescription']))
        page(c)
    print('built', len(COMPARE), 'comparison pages')


if __name__ == '__main__':
    main()
