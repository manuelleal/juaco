#!/bin/sh
# Lanzador portable de guardia.py (hook PreToolUse): python3 en la nube (Linux), python en el PC del director (Windows + Git Bash).
# exec conserva el stdin del hook y el código de salida (2 = bloquear).
F="$(dirname "$0")/guardia.py"
if command -v python3 >/dev/null 2>&1 && python3 -c "" >/dev/null 2>&1; then
  exec python3 "$F"
fi
exec python "$F"
