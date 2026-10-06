#!/bin/sh
# lanza_corrida.sh <NOMBRE> <config.yaml> <sem1,sem2,sem3> <iteraciones> <tope_llamadas>   (PREREGISTRO_serie.md)
cd "$(dirname "$0")"
export JUACO_OE_LIBRO="$PWD/gasto/libro_gasto.jsonl" JUACO_OE_TOPE_USD="${JUACO_OE_TOPE_USD:-20}" JUACO_OE_CORRIDA="$1" JUACO_OE_SEM="$3"
export JUACO_OE_VACIO="${TMPDIR:-/tmp}/juaco_oe_vacio_$1"
exec /root/venv-juaco/bin/python -B lanza.py raiz/programa_inicial.py evaluador.py "$2" "corridas/$1" "$4" "$5" > "corridas/$1.log" 2>&1
