#!/bin/bash
# Cola desatendida (24-sep, ~17:15): espera a que termine cola_eco2.sh (ECO v1.2) y corre ECO v4 serie y replica, UNA A LA VEZ (Pool 3).
cd /home/user/juaco
S=/tmp/claude-0/-home-user-juaco/6d1e775c-b095-5b26-8db3-9ecb181a6645/scratchpad
PY=/root/venv-juaco/bin/python
FIRMA=$'\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01RQB2Z9Hj9yA4LEoLeUWGcA'
sube () {
  v=$(grep "VEREDICTO:" "$2" | tail -1 | sed -E 's/^\[[0-9:]+\] //' | cut -c1-200)
  [ -z "$v" ] && v="SIN VEREDICTO (ver $2)"
  cp "$2" "$1/salida_consola.txt" 2>/dev/null
  git add "$1" >/dev/null 2>&1
  git commit -q -m "Nube, 24-sep (cola desatendida): $3 terminada: $v$FIRMA" && echo "[$(date -u +%H:%M:%S)] commit $3" >> $S/cola_eco.log
  for i in 1 2 3 4; do git push -q -u origin nube/noche-20260924 >/dev/null 2>&1 && break; sleep $((2**i)); done
}
corre () {
  out=$1; dir=$2; etq=$3; shift 3
  echo "[$(date -u +%H:%M:%S)] cola: $etq" >> $S/cola_eco.log
  nohup "$@" > $out 2>&1
  sube $dir $out "$etq"
}
echo "[$(date -u +%H:%M:%S)] cola3: espero el FIN de la cola de ECO v1.2" >> $S/cola_eco.log
# (la cola de ECO v1.2 se detuvo a mano a las 17:15: ver bitacora; no hay nada que esperar)
R=--reanuda; [ -d experimentos/juaco_eco/datos/eco_v4_serie_s20311-20330 ] || R=
corre $S/eco_v4_serie.out   experimentos/juaco_eco/datos/eco_v4_serie_s20311-20330   "ECO v4 serie 20311-20330"   $PY experimentos/juaco_eco/corre_eco_v4.py --serie --ventana serie --pool 3 $R
R=--reanuda; [ -d experimentos/juaco_eco/datos/eco_v4_replica_s20331-20350 ] || R=
corre $S/eco_v4_replica.out experimentos/juaco_eco/datos/eco_v4_replica_s20331-20350 "ECO v4 replica 20331-20350" $PY experimentos/juaco_eco/corre_eco_v4.py --serie --ventana replica --pool 3 $R
echo "[$(date -u +%H:%M:%S)] cola3: FIN" >> $S/cola_eco.log
for f in eco_v4_serie eco_v4_replica; do echo "== $f"; grep "VEREDICTO" $S/$f.out | tail -2 | cut -c1-260; done
