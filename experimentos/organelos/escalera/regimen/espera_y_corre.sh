#!/bin/sh
# espera_y_corre.sh — regimen: UN proceso de trabajo a la vez; cada etapa pasa por la regla de CPU del runner (sale con 2 si hay >= 6
# python ocupados) y se reintenta cada 60 s. Orden: humo -> rejilla A -> mixta -> rejilla B. Tope de espera: 14:00 (apagado a las 16:00).
RAIZ=/c/Users/User/Documents/PROYECTOS/JUACO/organelos
RUN="python $RAIZ/experimentos/organelos/escalera/regimen/corre_regimen.py"
OUT=$RAIZ/experimentos/organelos/escalera/regimen
etapa() {   # $1 = nombre de salida, resto = banderas
  nombre=$1; shift
  while :; do
    h=$(date +%H%M)
    if [ "$h" -ge 1400 ]; then echo "[$(date +%T)] $nombre: pasadas las 14:00, no se corre" >> "$OUT/ola_salida.txt"; return 1; fi
    $RUN "$@" > "$OUT/${nombre}_salida.txt" 2>&1; rc=$?
    echo "[$(date +%T)] $nombre rc $rc" >> "$OUT/ola_salida.txt"
    if [ "$rc" -eq 2 ]; then sleep 60; continue; fi
    return $rc
  done
}
echo "[$(date +%T)] OLA arranca" > "$OUT/ola_salida.txt"
etapa humo_regimen --humo && etapa rejilla_A --rejilla --semilla A && etapa mixta --mixta && etapa rejilla_B --rejilla --semilla B
echo "[$(date +%T)] OLA termina" >> "$OUT/ola_salida.txt"
