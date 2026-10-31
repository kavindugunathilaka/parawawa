#!/usr/bin/env bash
# Pull the latest site from GitHub and apply it. Run as root:  bash /var/www/parawawa/current/deploy/update.sh
set -euo pipefail
SITE=/var/www/parawawa/current

git -C "$SITE" pull --ff-only
chmod -R a+rX "$SITE"

# nginx settings follow vercel.json via tools/build_nginx.py; only reload when they changed
if ! cmp -s "$SITE/deploy/nginx/parawawa.conf" /etc/nginx/sites-available/parawawa.conf; then
  cp /etc/nginx/sites-available/parawawa.conf /etc/nginx/sites-available/parawawa.conf.bak
  cp "$SITE/deploy/nginx/parawawa.conf" /etc/nginx/sites-available/parawawa.conf
  # certbot's HTTPS lines live in the live file; re-run certbot to put them back
  certbot --nginx -d parawawa.lk -d www.parawawa.lk --redirect --non-interactive --reinstall >/dev/null 2>&1 || true
  if nginx -t; then
    systemctl reload nginx
  else
    echo "nginx config test failed - restoring the previous config"
    cp /etc/nginx/sites-available/parawawa.conf.bak /etc/nginx/sites-available/parawawa.conf
    systemctl reload nginx
    exit 1
  fi
fi

cmp -s "$SITE/deploy/parawewa-quote.service" /etc/systemd/system/parawewa-quote.service || {
  cp "$SITE/deploy/parawewa-quote.service" /etc/systemd/system/parawewa-quote.service
  systemctl daemon-reload
}
systemctl restart parawewa-quote
echo "Updated to $(git -C "$SITE" log --oneline -1)"
