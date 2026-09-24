#!/bin/bash
# Cola desatendida de la nube (24-sep): espera la serie de ECO v3 y luego corre, UNA A LA VEZ (un solo Pool), lo preregistrado.
# Tras cada paso: commit y push SOLO de los resultados (los checkpoints en curso estan excluidos). Sin turnos del coordinador.
cd /home/user/juaco
S=/tmp/claude-0/-home-user-juaco/6d1e775c-b095-5b26-8db3-9ecb181a6645/scratchpad
PY=/root/venv-juaco/bin/python
FIRMA=$'\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01RQB2Z9Hj9yA4LEoLeUWGcA'

sube () {   # $1 = carpeta de datos, $2 = archivo de salida, $3 = etiqueta
  v=$(grep "VEREDICTO:" "$2" | tail -1 | sed -E 's/^\[[0-9:]+\] //' | cut -c1-200)
  [ -z "$v" ] && v="SIN VEREDICTO (ver $2)"
  cp "$2" "$1/salida_consola.txt" 2>/dev/null
  git add "$1" >/dev/null 2>&1
  git commit -q -m "Nube, 24-sep (cola desatendida): $3 terminada: $v$FIRMA" && echo "[$(date -u +%H:%M:%S)] commit $3" >> $S/cola_eco.log
  for i in 1 2 3 4; do git push -q -u origin nube/noche-20260924 >/dev/null 2>&1 && break; sleep $((2**i)); done
}

echo "[$(date -u +%H:%M:%S)] cola RELANZADA tras el reinicio del contenedor (14:3x UTC)" >> $S/cola_eco.log

corre () {  # $1 = salida, $2 = carpeta, $3 = etiqueta, resto = comando
  out=$1; dir=$2; etq=$3; shift 3
  echo "[$(date -u +%H:%M:%S)] cola: $etq" >> $S/cola_eco.log
  nohup "$@" > $out 2>&1
  sube $dir $out "$etq"
}

corre $S/eco_v21_serie.out   experimentos/juaco_eco/datos/eco_v21_serie_s20211-20230   "ECO v2.1 serie 20211-20230"   $PY experimentos/juaco_eco/corre_eco_v21.py --serie --ventana serie --pool 3 --reanuda
corre $S/eco_v21_replica.out experimentos/juaco_eco/datos/eco_v21_replica_s20231-20250 "ECO v2.1 replica 20231-20250" $PY experimentos/juaco_eco/corre_eco_v21.py --serie --ventana replica --pool 3
corre $S/eco_v3_replica.out  experimentos/juaco_eco/datos/eco_v3_replica_s20131-20150  "ECO v3 replica 20131-20150"   $PY experimentos/juaco_eco/corre_eco_v3.py --serie --ventana replica --pool 3
corre $S/eco_v12_serie.out   experimentos/juaco_eco/datos/eco_v12_serie_s19701-19720   "ECO v1.2 serie 19701-19720"   $PY experimentos/juaco_eco/corre_eco_v12.py --serie --desde 19701 --n 20 --pool 3
corre $S/eco_v12_replica.out experimentos/juaco_eco/datos/eco_v12_serie_s19721-19740   "ECO v1.2 replica 19721-19740" $PY experimentos/juaco_eco/corre_eco_v12.py --serie --desde 19721 --n 20 --pool 3
echo "[$(date -u +%H:%M:%S)] cola: FIN" >> $S/cola_eco.log
for f in eco_v21_serie eco_v21_replica eco_v3_replica eco_v12_serie eco_v12_replica; do echo "== $f"; grep "VEREDICTO" $S/$f.out | tail -2 | cut -c1-260; done
