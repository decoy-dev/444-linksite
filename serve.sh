#!/usr/bin/env bash
# Serve the 444 build (WebGL + audio need HTTP, not file://).
cd "$(dirname "$0")" || exit 1
PORT="${1:-8779}"
echo "444 build -> http://localhost:${PORT}/"
python3 -m http.server "$PORT"
