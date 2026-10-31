#!/usr/bin/env bash
# Step 1 of moving to the Caddy multi-site setup. Does NOT touch DBM; nothing goes offline.
#   - creates the shared Docker network "web"
#   - clones the Parawewa site to /root/apps/parawewa/site and starts its containers (no public ports yet)
#   - puts the Caddy proxy files in /root/apps/proxy (not started yet)
# Safe to re-run. Run as root.
set -euo pipefail
REPO=https://github.com/kavindugunathilaka/parawawa.git
APP=/root/apps/parawewa
PROXY=/root/apps/proxy

[ "$(id -u)" = 0 ] || { echo "Run as root"; exit 1; }
command -v docker >/dev/null || { echo "Docker not found"; exit 1; }

echo "== network"
docker network inspect web >/dev/null 2>&1 && echo "web exists" || docker network create web

echo "== Parawewa site"
mkdir -p "$APP"
if [ -d "$APP/site/.git" ]; then git -C "$APP/site" pull --ff-only; else git clone --depth 1 "$REPO" "$APP/site"; fi
if [ ! -f "$APP/quote.env" ]; then
  cp "$APP/site/deploy/quote.env.example" "$APP/quote.env"
  echo "created $APP/quote.env (fill in the Resend key later: nano $APP/quote.env)"
fi
chmod 600 "$APP/quote.env"
# the quote container runs as user "node" (uid 1000) and reads the env through Docker, not the file itself
(cd "$APP/site/deploy/docker" && docker compose up -d)

echo "== proxy files"
mkdir -p "$PROXY/sites"
for f in docker-compose.yml Caddyfile write-sites.sh; do
  [ -f "$PROXY/$f" ] || cp "$APP/site/deploy/proxy/$f" "$PROXY/$f"
done
chmod +x "$PROXY/write-sites.sh"

echo "== checks"
sleep 3
docker ps --filter name=parawewa --format '{{.Names}}  {{.Status}}'
printf 'site:  '; docker exec parawewa-web wget -q -O- http://127.0.0.1/ | grep -o '<title>[^<]*' | head -1
printf 'quote: '; docker exec parawewa-web wget -q -O- http://parawewa-quote:3005/api/quote 2>&1 | head -1 || true
echo
echo "Step 1 done. Nothing public changed yet. Next: bash $APP/site/deploy/vps/2-switch.sh"
