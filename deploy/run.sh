#!/usr/bin/env bash
set -euo pipefail
umask 077

cd "$(dirname -- "${BASH_SOURCE[0]}")/.."
config_file="${CODE_DOJO_ENV_FILE:-deploy/.env}"
[[ "$config_file" = /* ]] || config_file="$PWD/$config_file"
if [[ -f "$config_file" ]]; then
  set -a
  source "$config_file"
  set +a
elif [[ -n "${CODE_DOJO_ENV_FILE:-}" ]]; then
  echo "找不到部署配置：$config_file" >&2
  exit 1
fi

export CODE_DOJO_AUTH="${CODE_DOJO_AUTH:-on}"
export CODE_DOJO_DATA="${CODE_DOJO_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/code-dojo}"
if [[ "$CODE_DOJO_AUTH" != on ]]; then
  echo '部署需要 CODE_DOJO_AUTH=on' >&2
  exit 1
fi

case "${1:-}" in
  --set-password) exec server/.venv/bin/python server/scripts/set_password.py ;;
  --build|'') ;;
  *) echo '用法：deploy/run.sh [--build | --set-password]' >&2; exit 2 ;;
esac

export CODE_DOJO_WEB_DIST="$(realpath -m "${CODE_DOJO_WEB_DIST:-web/dist}")"
if [[ "${1:-}" == --build ]]; then
  (cd web && npm run build -- --outDir "$CODE_DOJO_WEB_DIST")
fi

exec server/.venv/bin/python -m uvicorn app.main:app --app-dir server \
  --host 127.0.0.1 --port "${CODE_DOJO_PORT:-8001}" --workers 1 \
  --proxy-headers --forwarded-allow-ips 127.0.0.1 --no-server-header
