#!/usr/bin/env bash
# Writes /root/apps/proxy/sites/{dbm,parawewa}.caddy and reloads Caddy.
# Only domains whose DNS already points to this server are included, so Caddy never
# asks for a certificate it cannot get. Safe to re-run after each DNS change.
#
#   bash write-sites.sh            (run as root on the VPS)
set -euo pipefail
SITES=${SITES:-/root/apps/proxy/sites}

# Parawewa: the main address + the addresses that redirect to it
PARAWEWA_PRIMARY=${PARAWEWA_PRIMARY:-parawewa.lk}
PARAWEWA_ALL="parawawa.lk www.parawawa.lk parawewa.lk www.parawewa.lk parawewa.com www.parawewa.com"
# DBM system: always on http://<server IP> (how users reach it today), plus its own domain once
# DNS points here (http and https, no forced redirect until the app is checked on https).
# dbm.lk itself is kept free for the DBM company website.
DBM_ALL="app.dbm.lk"

MYIP=$(ip -4 route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++) if($i=="src") print $(i+1)}')
here() { [ "$(getent ahostsv4 "$1" | awk 'NR==1{print $1}')" = "$MYIP" ]; }
pick() { local out=""; for d in "$@"; do if here "$d"; then out="$out $d"; else echo "  skip $d (DNS not pointing to $MYIP yet)" >&2; fi; done; echo "$out"; }
join() { local p=$1 s=""; shift; for d in "$@"; do s="${s:+$s, }$p$d"; done; echo "$s"; }

mkdir -p "$SITES"
echo "Server IP: $MYIP"

# ---- DBM system
dbm=$(pick $DBM_ALL)
# 127.0.0.1/localhost: DBM's own scripts/deploy.sh health check calls http://127.0.0.1/ on the server
addr="http://$MYIP, http://127.0.0.1, http://localhost"
[ -n "$dbm" ] && addr="$addr, $(join http:// $dbm), $(join https:// $dbm)"
cat > "$SITES/dbm.caddy" <<EOF
# DBM system (react-node-architect). Container: dbm_frontend_nginx
$addr {
	import common
	reverse_proxy dbm_frontend_nginx:80
}
EOF
echo "dbm.caddy: $addr"

# ---- Parawewa
pw=$(pick $PARAWEWA_ALL)
others=""; for d in $pw; do [ "$d" = "$PARAWEWA_PRIMARY" ] || others="$others $d"; done
if [[ " $pw " == *" $PARAWEWA_PRIMARY "* ]]; then
  {
    echo "# Parawewa website (deploy/docker/). Main address: $PARAWEWA_PRIMARY"
    echo "$PARAWEWA_PRIMARY {"
    echo "	import common"
    echo "	header Strict-Transport-Security \"max-age=31536000\""
    echo "	reverse_proxy parawewa-web:80"
    echo "}"
    if [ -n "$others" ]; then
      echo
      echo "# Other Parawewa addresses -> main address"
      echo "$(join "" $others) {"
      echo "	redir https://$PARAWEWA_PRIMARY{uri} permanent"
      echo "}"
    fi
  } > "$SITES/parawewa.caddy"
  echo "parawewa.caddy: $PARAWEWA_PRIMARY (+$others redirect)"
else
  rm -f "$SITES/parawewa.caddy"
  echo "parawewa.caddy: not written - $PARAWEWA_PRIMARY does not point to $MYIP yet"
fi

if docker ps --format '{{.Names}}' | grep -qx caddy; then
  docker exec caddy caddy reload --config /etc/caddy/Caddyfile && echo "Caddy reloaded"
fi
