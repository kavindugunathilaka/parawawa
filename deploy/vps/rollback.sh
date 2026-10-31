#!/usr/bin/env bash
# Undo 2-switch.sh: stop Caddy and give ports 80/443 back to DBM's nginx exactly as before.
# Parawewa containers keep running (they have no public ports). Run as root.
set -euo pipefail
DBM_DIR=/root/apps/dbm-system/react-node-architect
F=$DBM_DIR/docker-compose.prod.yml
PROXY=/root/apps/proxy

BACKUP=$(cat "$PROXY/.dbm-backup" 2>/dev/null || true)
[ -f "$BACKUP" ] || { echo "No backup recorded in $PROXY/.dbm-backup"; exit 1; }
FRONT=$(docker inspect dbm_frontend_nginx --format '{{index .Config.Labels "com.docker.compose.service"}}')

(cd "$PROXY" && docker compose down) || true
cp -p "$BACKUP" "$F"
cd "$DBM_DIR"
docker compose -f "$F" up -d --no-deps "$FRONT"
docker ps --format '{{.Names}}  {{.Ports}}'
echo "Rolled back to $BACKUP"
