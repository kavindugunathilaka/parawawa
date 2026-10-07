"""Build /systems/<slug>/index.html from content/systems.py. Run via tools/build.py."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_articles as ba  # noqa: E402
from systems import SYSTEMS  # noqa: E402

SITE, VER, esc, HEADER, FOOTER, ld_dump = ba.SITE, ba.VER, ba.esc, ba.HEADER, ba.FOOTER, ba.ld_dump


def page(sy):
    url = f"{SITE}/systems/{sy['slug']}/"
    other = next(x for x in SYSTEMS if x['slug'] == sy['other'])
    img_abs = f"{SITE}/{sy['img']}"
    w, h = ba.img_size(sy['img'])
    facts = ''.join(f'<div><dt>{esc(k)}</dt><dd>{v}</dd></div>' for k, v in sy['facts'])
    faq_html = ''.join(f'''
          <div class="accordion-item">
            <div class="accordion-header">
              <span>{esc(q)}</span>
              <i class="fas fa-plus accordion-icon"></i>
            </div>
            <div class="accordion-body"><p>{esc(a)}</p></div>
          </div>''' for q, a in sy['faqs'])
    related = ''.join(ba.card_html(ba.BY_ID[r]) for r in sy['related'])
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Product",
                "@id": url + "#product",
                "name": sy['productName'],
                "description": sy['metaDescription'],
                "image": img_abs,
                "url": url,
                "category": "Septic tank / wastewater treatment system",
                "brand": {"@type": "Brand", "name": "Parawewa"},
                "manufacturer": {"@type": "Organization", "name": "Parawewa", "url": SITE + "/"},
                "isRelatedTo": {"@type": "Product", "name": other['productName'], "url": f"{SITE}/systems/{other['slug']}/"},
            },
            {
                "@type": "FAQPage",
                "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in sy['faqs']],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": sy['name'], "item": url},
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
  <title>{esc(sy['metaTitle'])}</title>
  <meta name="description" content="{esc(sy['metaDescription'])}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <link rel="canonical" href="{url}">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Parawewa">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{esc(sy['name'])}">
  <meta property="og:description" content="{esc(sy['metaDescription'])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{img_abs}">
  <meta property="og:image:width" content="{w}">
  <meta property="og:image:height" content="{h}">
  <meta property="og:image:alt" content="{esc(sy['imgAlt'])}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(sy['name'])}">
  <meta name="twitter:description" content="{esc(sy['metaDescription'])}">
  <meta name="twitter:image" content="{img_abs}">

  <link rel="icon" type="image/png" href="/assets/real_logo.png">
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

  {header.strip()}

  <main id="main">
    <header class="article-hero">
      <div class="container article-wrap">
        <nav class="breadcrumbs" aria-label="Breadcrumb">
          <ol>
            <li><a href="/">Home</a></li>
            <li><a href="/#models">System options</a></li>
            <li aria-current="page">{esc(sy['name'].split(':')[0])}</li>
          </ol>
        </nav>
        <span class="section-tag">{esc(sy['eyebrow'])}</span>
        <h1 class="article-h1">{esc(sy['name'])}</h1>
        <p class="article-lede">{esc(sy['lede'])}</p>
        <div class="system-actions">
          <a href="/#contact" class="btn btn-primary open-quote-modal"><i class="fas fa-paper-plane"></i> Get Free Quote</a>
          <a href="/systems/{other['slug']}/" class="btn btn-secondary">See {esc(other['name'].split(':')[0])} <i class="fas fa-arrow-right"></i></a>
        </div>
      </div>
    </header>

    <article class="container article-wrap article-main">
      <figure class="article-figure">
        <img src="/{ba.webp(sy['img'])}" alt="{esc(sy['imgAlt'])}" width="{w}" height="{h}" fetchpriority="high" decoding="async">
      </figure>

      <dl class="fact-grid">{facts}</dl>

      <div class="article-body">
{sy['body']}
      </div>

      <section class="system-faq" aria-labelledby="faq-heading">
        <h2 id="faq-heading" class="system-faq-title">Frequently asked questions</h2>
        <div class="accordion">{faq_html}
        </div>
      </section>

      <aside class="article-cta" aria-label="Request a quote">
        <div>
          <h2>Not sure which option fits your plot?</h2>
          <p>Request a free site inspection. The Parawewa team will confirm whether Option A or Option B suits your ground and recommend a tank size for your property.</p>
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
    os.makedirs(f"systems/{sy['slug']}", exist_ok=True)
    open(f"systems/{sy['slug']}/index.html", 'w', encoding='utf-8', newline='\n').write(out)


def main():
    for sy in SYSTEMS:
        page(sy)
    print('built', len(SYSTEMS), 'system pages')


if __name__ == '__main__':
    main()
