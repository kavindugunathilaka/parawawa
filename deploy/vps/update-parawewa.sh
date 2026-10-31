#!/usr/bin/env bash
# Pull the latest Parawewa site from GitHub and apply it (Docker setup). Run as root after each push:
#   bash /root/apps/parawewa/site/deploy/vps/update-parawewa.sh
set -euo pipefail
SITE=/root/apps/parawewa/site

git -C "$SITE" pull --ff-only
cd "$SITE/deploy/docker"
docker compose up -d
# nginx config is generated from vercel.json; test before reloading
docker compose exec -T web nginx -t && docker compose exec -T web nginx -s reload
docker compose restart quote >/dev/null
echo "Updated to $(git -C "$SITE" log --oneline -1)"
