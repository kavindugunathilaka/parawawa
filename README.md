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
| `content/si_strings.py` | **Sinhala wording** for the Sinhala home page (English text -> Sinhala) | Yes |
| `articles/`, `systems/`, `compare/`, `si/` | Generated pages (`si/index.html` is built from `index.html` + `content/si_strings.py`) | **No** |
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

**Sinhala page (`/si/`):** same design and content as the home page. After changing English text on `index.html`, add or update its Sinhala in `content/si_strings.py`; the build prints any English text still untranslated. Articles, system and comparison pages are English only; the Sinhala page links to them and says so.

## Common tasks

**Edit article text:** change it in `content/articles.json`, run the build.

**Add an article:** add an entry to `content/articles.json` (copy an existing one: `id`, `slug`, `title`, `metaTitle` up to 62 characters, `metaDescription` up to 160, `summary`, `img`, `imgAlt`, `published`, `modified`, `related`, `content`). Also add the new id to the `AUTOLINKS`/related lists if useful, update the "20" in the hub heading and homepage button text, and run the build.

**Add a photo:** put the JPG or PNG in `assets/`, reference it as `.jpg`/`.png` in your content; the build creates the `.webp` copy and pages use it.

**Add an icon:** use `<i class="fas fa-name">` as usual. The build adds it to the icon subset automatically (it fails loudly if the icon name does not exist in Font Awesome 6.4 Free).

**Change contact details:** edit the header, contact section and footer in `index.html` and the schema in its `<head>`, update `build_extras.py` (`llms.txt`) and `build_articles.py` (article call-to-action phone), then build.

## Design system (v3, green)

Palette (sampled from the client's reference design): brand `#1a8245`, lime `#6eb444`, mint `#f0f8f0`, deep green `#0c3b21`. Tokens are CSS variables at the top of `style.css`; the redesign layer is the last section ("REDESIGN v3").

- **Hero** (`.hx`): rounded photo card with a white notch tab (the navigation) cut into its top edge, a lime phone pill, and a white fact card. The blurred backdrop is a pre-rendered `assets/hero-bg.webp` (built from the real photo by `tools/build_assets.py`).
- **Navigation** (`.navbar`): a zero-height sticky wrapper; the white pill is absolutely positioned over the page top and becomes a floating pill after scrolling (`.scrolled`). Pages without a hero card keep their content clear of it with extra top padding (`.article-hero`, `main > .section:first-child`).
- **Panels:** `.section-alt` sections are rounded mint panels; consecutive panels get a gap.
- **Buttons:** pills; a leading `<i>` in `.btn-primary` renders inside a white circle.
- **Illustrations** in "How the system is built" are conceptual drawings supplied by the client, cropped from their source sheet; keep the "Illustration" label and the disclaimer.

## Quote form emails

Both quote forms (contact section and the pop-up on every page) post to `api/quote.js`, a Vercel serverless function that emails the request through [Resend](https://resend.com) to every address in `QUOTE_TO`. Set these in Vercel > Project > Settings > Environment Variables, then redeploy:

| Variable | Value |
|---|---|
| `RESEND_API_KEY` | API key from the Resend dashboard (keep it secret) |
| `QUOTE_TO` | Recipients, comma-separated, e.g. `info@parawawa.lk, someone@gmail.com` |
| `QUOTE_FROM` | Optional. e.g. `Parawewa Website <quotes@parawewa.lk>`, only after `parawewa.lk` is verified in Resend (DNS records). Without it, Resend's test sender delivers only to the Resend account owner's own address. |

Until the variables are set the form shows "could not be sent, please call or WhatsApp". Spam protection: a hidden field and a minimum fill-in time. When moving the domain's DNS to Vercel, keep the existing MX records so info@parawawa.lk keeps receiving mail.

## Hosting on a Linux VPS (Contabo or any Ubuntu server)

Everything the server needs is in `deploy/`:

| File | What it is |
|---|---|
| `deploy/nginx/parawawa.conf` | nginx site: redirects, cache and security headers, quote-form proxy. **Generated from `vercel.json`** by `tools/build_nginx.py` (part of the build), so both stay in sync |
| `deploy/quote-server.js` | Runs `api/quote.js` as a small Node service on `127.0.0.1:3005` |
| `deploy/parawewa-quote.service` | systemd unit that keeps the quote service running |
| `deploy/quote.env.example` | Template for `/etc/parawewa/quote.env` (Resend key, recipients) |
| `deploy/setup.sh` | One-time server setup (nginx, certbot, Node 20, firewall, service) |
| `deploy/update.sh` | Pull the latest site from GitHub and apply it |

First time (Ubuntu 22.04/24.04, as root):

```bash
curl -fsSL https://raw.githubusercontent.com/kavindugunathilaka/parawawa/main/deploy/setup.sh -o setup.sh
bash setup.sh
```

Then point the `A` records for `parawewa.lk` and `www.parawewa.lk` at the server IP (keep the MX records), run
`certbot --nginx -d parawewa.lk -d www.parawewa.lk --redirect`, fill in `/etc/parawewa/quote.env` and
`systemctl restart parawewa-quote`. After each push to GitHub: `bash /var/www/parawawa/current/deploy/update.sh`.

The site files need no build on the server: the generated pages are committed.

### Shared Docker VPS (several sites on one server, Caddy in front)

Use this instead of `setup.sh` when the server already runs other sites in Docker (the current VPS runs DBM).
Caddy owns ports 80/443, gets HTTPS certificates for every domain automatically and sends each domain to
its own containers over a shared Docker network called `web`.

| File | What it is |
|---|---|
| `deploy/proxy/` | Caddy compose file, `Caddyfile` (imports `sites/*.caddy`) and `write-sites.sh`, which writes a site file for every domain whose DNS already points to the server |
| `deploy/docker/docker-compose.yml` | Parawewa: nginx container (`deploy/docker/nginx.conf`, generated from `vercel.json`) + the quote-form Node container. No public ports |
| `deploy/vps/1-prepare.sh` | Network, site clone in `/root/apps/parawewa/site`, Parawewa containers, proxy files in `/root/apps/proxy`. Touches nothing else |
| `deploy/vps/2-switch.sh` | Backs up DBM's compose file, moves 80/443 from DBM's nginx to Caddy, binds Prisma Studio to 127.0.0.1; puts everything back on its own if DBM does not answer |
| `deploy/vps/rollback.sh` | Undo `2-switch.sh` |
| `deploy/vps/3-harden.sh` | Firewall, fail2ban, automatic security updates, nightly DBM database dump |
| `deploy/vps/update-parawewa.sh` | After each push: pull and reload |

Order: `1-prepare.sh`, `2-switch.sh`, `3-harden.sh`. After any DNS change run `bash /root/apps/proxy/write-sites.sh`.
To add another website later: give it its own compose project on the `web` network (no host ports) and a
`sites/<name>.caddy` file:

```
example.com {
	import common
	reverse_proxy <container>:<port>
}
```

then `docker exec caddy caddy reload --config /etc/caddy/Caddyfile`.

## Going live on parawewa.lk

All canonical URLs, the sitemap and the structured data already assume `https://parawewa.lk/`.

1. In Vercel, add `parawewa.lk` (and `www`) to this project and update the DNS records it asks for.
2. The old WordPress URLs (`/en/...`, `/si/`, `/wp-sitemap.xml`) redirect through `vercel.json`.
3. In Google Search Console add a **Domain** property for `parawewa.lk` (verify with a DNS TXT record), submit `https://parawewa.lk/sitemap.xml`, and request indexing of the home page.
4. Repeat in Bing Webmaster Tools if wanted.

## Content rules

- No prices, capacities or specifications that the client has not confirmed.
- No testimonials or ratings that are not real.
- Option A: gravity-fed, no electricity ("Standard Parawewa system", low groundwater). Option B: "Seal Type Parawewa System" (water-sealed, high groundwater; uses some electricity, less than mechanical STPs). Both: 10-year written warranty, Sri Lanka Patent #16371.
- Client wording rules (2026-10-17): never write "layer-base"; never put "pump"/"submersible pump" in Option B titles, headings or labels; write "No" instead of "0"/"0%"/"Zero"; treated water is absorbed into the ground (never "irrigation", "recycled", "to turf/drains").
