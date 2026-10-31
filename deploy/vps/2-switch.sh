#!/usr/bin/env bash
# Step 2: hand ports 80/443 from DBM's nginx to Caddy. DBM is offline for a few seconds.
#   - backs up DBM's docker-compose.prod.yml
#   - DBM's nginx: drops its 80/443 ports and joins the "web" network (its code, database and settings are not touched)
#   - Prisma Studio: port 5555 bound to 127.0.0.1 only (reach it through an SSH tunnel)
#   - starts Caddy; if DBM does not answer through Caddy, everything is put back automatically
# Undo by hand any time: bash rollback.sh. Run as root.
set -euo pipefail
DBM_DIR=/root/apps/dbm-system/react-node-architect
F=$DBM_DIR/docker-compose.prod.yml
PROXY=/root/apps/proxy
HERE=$(cd "$(dirname "$0")" && pwd)

[ "$(id -u)" = 0 ] || { echo "Run as root"; exit 1; }
[ -f "$PROXY/docker-compose.yml" ] && docker ps --format '{{.Names}}' | grep -qx parawewa-web \
  || { echo "Run 1-prepare.sh first"; exit 1; }
grep -q '^# switched-to-caddy' "$F" && { echo "Already switched (see $F)"; exit 0; }

BACKUP=$F.before-caddy-$(date +%Y%m%d-%H%M%S)
cp -p "$F" "$BACKUP"
echo "$BACKUP" > "$PROXY/.dbm-backup"
echo "backup: $BACKUP"

# ---- edit the compose file (prints the nginx service name)
FRONT=$(python3 - "$F" <<'PY'
import re, sys
p = sys.argv[1]
L = open(p).read().rstrip('\n').split('\n')

def services():
    out, name, start, inside = [], None, None, False
    for i, l in enumerate(L):
        if re.match(r'^\S', l):
            if start is not None: out.append((name, start, i)); start = None
            inside = l.startswith('services:')
        elif inside and re.match(r'^  [\w.-]+:\s*$', l):
            if start is not None: out.append((name, start, i))
            name, start = l.strip()[:-1], i
    if start is not None: out.append((name, start, len(L)))
    return out

if any(l.startswith('networks:') for l in L): sys.exit('compose file already has top-level networks: edit by hand')
front = [s for s in services() if any('container_name: dbm_frontend_nginx' in l for l in L[s[1]:s[2]])]
if len(front) != 1: sys.exit('nginx service (container_name: dbm_frontend_nginx) not found')
name, a, b = front[0]
block = L[a:b]
if any(l.strip() == 'networks:' for l in block): sys.exit('nginx service already has networks: edit by hand')
new = []
i = 0
while i < len(block):
    l = block[i]
    if l.strip() == 'ports:':
        items = []
        i += 1
        while i < len(block) and block[i].strip().startswith('- '):
            if not re.search(r'["\']?(80:80|443:443)["\']?\s*$', block[i]): items.append(block[i])
            i += 1
        if items: new += [l] + items
        continue
    new.append(l)
    if 'container_name: dbm_frontend_nginx' in l:
        new += ['    networks:', '      - default', '      - web']
    i += 1
L[a:b] = new
L = [re.sub(r'(["\']?)5555:5555', r'\g<1>127.0.0.1:5555:5555', l) if '- ' in l and '5555:5555' in l and '127.0.0.1' not in l else l for l in L]
L = ['# switched-to-caddy: ports 80/443 belong to /root/apps/proxy (Caddy); backup next to this file'] + L
L += ['', 'networks:', '  web:', '    external: true']
open(p, 'w').write('\n'.join(L) + '\n')
print(name)
PY
)
echo "DBM nginx service: $FRONT"
cd "$DBM_DIR"
docker compose -f "$F" config -q 2>/dev/null || { echo "compose check failed - restoring"; cp -p "$BACKUP" "$F"; exit 1; }
diff -u "$BACKUP" "$F" || true

restore() {
  echo "!! problem - putting DBM back the way it was"
  (cd "$PROXY" && docker compose down) || true
  cp -p "$BACKUP" "$F"
  docker compose -f "$F" up -d --no-deps "$FRONT"
  exit 1
}

# latest site-file writer from this checkout, then check the whole Caddy config before anything stops
cp "$HERE/../proxy/write-sites.sh" "$PROXY/write-sites.sh"
bash "$PROXY/write-sites.sh"
[ -f "$PROXY/sites/dbm.caddy" ] || { echo "dbm.caddy missing - nothing switched"; cp -p "$BACKUP" "$F"; exit 1; }
MYIP=$(ip -4 route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++) if($i=="src") print $(i+1)}')

echo "== checking Caddy before the switch"
(cd "$PROXY" && docker compose pull -q) || { cp -p "$BACKUP" "$F"; echo "Caddy download failed - nothing switched"; exit 1; }
docker run --rm -v "$PROXY/Caddyfile:/etc/caddy/Caddyfile:ro" -v "$PROXY/sites:/etc/caddy/sites:ro" caddy:2.8-alpine \
  caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile >/dev/null \
  || { cp -p "$BACKUP" "$F"; echo "Caddy config invalid - nothing switched"; exit 1; }
echo "Caddy config OK"

echo "== switching (DBM offline for a few seconds)"
docker compose -f "$F" up -d --no-deps "$FRONT" || restore
(cd "$PROXY" && docker compose up -d) || restore

sleep 6
read -r code size < <(curl -s -o /dev/null -w '%{http_code} %{size_download}\n' -H "Host: $MYIP" http://127.0.0.1/ || echo "000 0")
echo "DBM through Caddy (http://$MYIP): HTTP $code, $size bytes"
case "$code" in 2*|3*|401|403) [ "${size%.*}" -gt 0 ] || [ "${code:0:1}" = 3 ] || restore ;; *) restore ;; esac

# ---- Prisma Studio: only recreate when the DB password is available, otherwise stop it
if [ -n "${DB_PASSWORD:-}" ] || grep -qs '^DB_PASSWORD=' "$DBM_DIR/.env"; then
  docker compose -f "$F" up -d --no-deps studio && echo "studio: now 127.0.0.1:5555 only"
else
  docker compose -f "$F" stop studio && echo "studio: stopped (port 5555 closed). Start later with DB_PASSWORD set."
fi

echo
docker ps --format '{{.Names}}  {{.Ports}}'
echo
echo "Done. Caddy now owns 80/443. Logs: docker logs -f caddy"
echo "Undo: bash $HERE/rollback.sh"
