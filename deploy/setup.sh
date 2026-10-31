#!/usr/bin/env bash
# One-time setup of a fresh Ubuntu 22.04/24.04 VPS (e.g. Contabo) for parawawa.lk.
# Run as root:   bash setup.sh https://github.com/kavindugunathilaka/parawawa.git
# Safe to re-run.
set -euo pipefail

REPO="${1:-https://github.com/kavindugunathilaka/parawawa.git}"
WEB=/var/www/parawawa
SITE=$WEB/current
DOMAIN=parawawa.lk

echo "==> Packages (nginx, certbot, git, firewall)"
apt-get update -y
apt-get install -y nginx certbot python3-certbot-nginx git ufw curl ca-certificates

echo "==> Node.js 20 (for the quote form)"
if ! command -v node >/dev/null || [ "$(node -p 'process.versions.node.split(".")[0]')" -lt 18 ]; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
  apt-get install -y nodejs
fi
node --version

echo "==> Service user"
id parawewa >/dev/null 2>&1 || useradd --system --no-create-home --shell /usr/sbin/nologin parawewa

echo "==> Website files from GitHub"
mkdir -p "$WEB"
if [ -d "$SITE/.git" ]; then
  git -C "$SITE" pull --ff-only
else
  git clone --depth 1 "$REPO" "$SITE"
fi
chown -R root:root "$SITE"
chmod -R a+rX "$SITE"

echo "==> Quote form settings"
mkdir -p /etc/parawewa
if [ ! -f /etc/parawewa/quote.env ]; then
  cp "$SITE/deploy/quote.env.example" /etc/parawewa/quote.env
  echo "   !! Edit /etc/parawewa/quote.env (RESEND_API_KEY, QUOTE_TO) then: systemctl restart parawewa-quote"
fi
chown root:parawewa /etc/parawewa/quote.env
chmod 640 /etc/parawewa/quote.env

echo "==> Quote form service"
cp "$SITE/deploy/parawewa-quote.service" /etc/systemd/system/parawewa-quote.service
systemctl daemon-reload
systemctl enable --now parawewa-quote
systemctl restart parawewa-quote

echo "==> nginx"
cp "$SITE/deploy/nginx/parawawa.conf" /etc/nginx/sites-available/parawawa.conf
ln -sf /etc/nginx/sites-available/parawawa.conf /etc/nginx/sites-enabled/parawawa.conf
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "==> Firewall (SSH + web only)"
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

cat <<EOF

Done. Next:
  1. Point DNS for $DOMAIN and www.$DOMAIN (A records) to this server's IP. Keep the MX records for email.
  2. When DNS works:   certbot --nginx -d $DOMAIN -d www.$DOMAIN --redirect -m you@example.com --agree-tos
  3. Fill in /etc/parawewa/quote.env, then:   systemctl restart parawewa-quote
  4. Later updates:    bash $SITE/deploy/update.sh
EOF
