#!/usr/bin/env bash
# Step 3: basic server protection + daily DBM database backup. Run as root, after 2-switch.sh.
#   - firewall (ufw): only SSH, 80 and 443 open
#   - fail2ban: blocks IPs that keep guessing SSH passwords
#   - automatic Ubuntu security updates
#   - DBM database dump every night 02:30 to /root/backups/dbm (kept 14 days)
# Does not change SSH login settings (it only reports them).
set -euo pipefail
[ "$(id -u)" = 0 ] || { echo "Run as root"; exit 1; }

echo "== packages"
DEBIAN_FRONTEND=noninteractive apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ufw fail2ban unattended-upgrades >/dev/null

echo "== firewall"
SSH_PORTS=$(ss -tlnpH 2>/dev/null | awk '/sshd/ {n=split($4,a,":"); print a[n]}' | sort -u)
[ -n "$SSH_PORTS" ] || SSH_PORTS=22
for p in $SSH_PORTS; do ufw allow "$p/tcp" comment ssh >/dev/null; done
ufw allow 80/tcp comment http >/dev/null
ufw allow 443/tcp comment https >/dev/null
ufw allow 443/udp comment http3 >/dev/null
ufw default deny incoming >/dev/null
ufw default allow outgoing >/dev/null
ufw --force enable
ufw status verbose | sed -n '1,20p'
echo "(note: ports published by Docker skip ufw; 2-switch.sh already left only Caddy's 80/443 public)"

echo "== fail2ban"
systemctl enable --now fail2ban >/dev/null
fail2ban-client status sshd 2>/dev/null | head -3 || echo "fail2ban running"

echo "== automatic security updates"
echo 'unattended-upgrades unattended-upgrades/enable_auto_updates boolean true' | debconf-set-selections
dpkg-reconfigure -f noninteractive unattended-upgrades
grep -h 'APT::Periodic::Unattended-Upgrade' /etc/apt/apt.conf.d/20auto-upgrades

echo "== DBM nightly backup"
mkdir -p /root/backups/dbm && chmod 700 /root/backups
cat > /usr/local/bin/dbm-backup <<'EOF'
#!/usr/bin/env bash
# Dump the DBM database (container dbm_postgres) and keep 14 days of copies.
set -euo pipefail
OUT=/root/backups/dbm/dbm_hrm-$(date +%F-%H%M).sql.gz
docker exec dbm_postgres pg_dump -U postgres -d dbm_hrm | gzip > "$OUT.tmp"
mv "$OUT.tmp" "$OUT"
find /root/backups/dbm -name '*.sql.gz' -mtime +14 -delete
EOF
chmod 700 /usr/local/bin/dbm-backup
echo '30 2 * * * root /usr/local/bin/dbm-backup >> /var/log/dbm-backup.log 2>&1' > /etc/cron.d/dbm-backup
/usr/local/bin/dbm-backup && ls -lh /root/backups/dbm | tail -3

echo "== SSH login (report only)"
sshd -T 2>/dev/null | grep -E '^(port|permitrootlogin|passwordauthentication) '
echo
echo "Done. Backups stay on this server only - copy them off-server too (ask Claude for the off-site step)."
