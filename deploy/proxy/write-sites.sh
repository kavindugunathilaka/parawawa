#!/usr/bin/env bash
# Writes /root/apps/proxy/sites/{dbm,parawewa}.caddy and reloads Caddy.
# Only domains whose DNS already points to this server are included, so Caddy never
# asks for a certificate it cannot get. Safe to re-run after each DNS change.
#
#   bash write-sites.sh            (run as root on the VPS)
set -euo pipefail
SITES=/root/apps/proxy/sites

# Parawewa: the main address + the addresses that redirect to it
PARAWEWA_PRIMARY=${PARAWEWA_PRIMARY:-parawawa.lk}
PARAWEWA_ALL="parawawa.lk www.parawawa.lk parawewa.lk www.parawewa.lk parawewa.com www.parawewa.com"
# DBM: served over both http and https, no forced redirect until its app is checked on https
DBM_ALL="dbm.lk www.dbm.lk"

MYIP=$(ip -4 route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++) if($i=="src") print $(i+1)}')
here() { [ "$(getent ahostsv4 "$1" | awk 'NR==1{print $1}')" = "$MYIP" ]; }
pick() { local out=""; for d in "$@"; do if here "$d"; then out="$out $d"; else echo "  skip $d (DNS not pointing to $MYIP yet)" >&2; fi; done; echo "$out"; }
join() { local p=$1 s=""; shift; for d in "$@"; do s="${s:+$s, }$p$d"; done; echo "$s"; }

mkdir -p "$SITES"
echo "Server IP: $MYIP"

# ---- DBM
dbm=$(pick $DBM_ALL)
if [ -n "$dbm" ]; then
  cat > "$SITES/dbm.caddy" <<EOF
# DBM (react-node-architect). Container: dbm_frontend_nginx
$(join http:// $dbm), $(join https:// $dbm) {
	import common
	reverse_proxy dbm_frontend_nginx:80
}
EOF
  echo "dbm.caddy:$dbm"
fi

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
