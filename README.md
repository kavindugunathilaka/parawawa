# Parawewa website

Static site (HTML, CSS, vanilla JS). No framework. Deployed to Vercel from `main`.

## How it is organised

| Path | What it is | Edit by hand? |
|---|---|---|
| `index.html` | Home page | Yes |
| `articles.html` | Knowledge hub page (header and footer only; the grid is generated) | Yes, except between the `BUILD:` markers |
| `style.css`, `app.js` | Site styles and behaviour | Yes |
| `content/articles.json` | **Source of truth for the 20 articles** | Yes |
| `content/systems.py` | Option A and Option B pages | Yes |
| `content/compare.py` | Comparison pages | Yes |
| `articles/`, `systems/`, `compare/` | Generated pages | **No** |
| `articles-meta.js`, `sitemap.xml`, `feed.xml`, `llms.txt`, `404.html` | Generated | **No** |
| `assets/fa/`, `assets/fonts/`, `assets/*.webp`, `assets/icons/`, `favicon.ico` | Generated | **No** |
| `tools/` | Build scripts | Only when changing the build |
| `vercel.json` | Redirects from the old WordPress site, cache and security headers | Yes |

## Build

```bash
python tools/build.py
```

Needs Python 3 with `pillow`, `fonttools` and `brotli` (`pip install pillow fonttools brotli`). It:

1. builds the favicon set, the icon subset, the self-hosted fonts and the WebP copies of photos
2. stamps a cache-busting `?v=<hash>` into the pages, so visitors never get stale CSS or JS
3. regenerates every article, system and comparison page, the hub grid, the home page featured cards, the sitemap, the feed, `llms.txt` and the 404 page

Run it after every change to `content/`, `style.css`, `app.js` or the header and footer in `index.html`, then commit everything it changed.

## Common tasks

**Edit article text:** change it in `content/articles.json`, run the build.

**Add an article:** add an entry to `content/articles.json` (copy an existing one: `id`, `slug`, `title`, `metaTitle` up to 62 characters, `metaDescription` up to 160, `summary`, `img`, `imgAlt`, `published`, `modified`, `related`, `content`). Also add the new id to the `AUTOLINKS`/related lists if useful, update the "20" in the hub heading and homepage button text, and run the build.

**Add a photo:** put the JPG or PNG in `assets/`, reference it as `.jpg`/`.png` in your content; the build creates the `.webp` copy and pages use it.

**Add an icon:** use `<i class="fas fa-name">` as usual. The build adds it to the icon subset automatically (it fails loudly if the icon name does not exist in Font Awesome 6.4 Free).

**Change contact details:** edit the header, contact section and footer in `index.html` and the schema in its `<head>`, update `build_extras.py` (`llms.txt`) and `build_articles.py` (article call-to-action phone), then build.

## Going live on parawawa.lk

All canonical URLs, the sitemap and the structured data already assume `https://parawawa.lk/`.

1. In Vercel, add `parawawa.lk` (and `www`) to this project and update the DNS records it asks for.
2. The old WordPress URLs (`/en/...`, `/si/`, `/wp-sitemap.xml`) redirect through `vercel.json`.
3. In Google Search Console add a **Domain** property for `parawawa.lk` (verify with a DNS TXT record), submit `https://parawawa.lk/sitemap.xml`, and request indexing of the home page.
4. Repeat in Bing Webmaster Tools if wanted.

## Content rules

- No prices, capacities or specifications that the client has not confirmed.
- No testimonials or ratings that are not real.
- Option A: gravity-fed, 0% electricity. Option B: sealed submersible pump (uses electricity). Both: 10-year written warranty, Sri Lanka Patent #10848.
