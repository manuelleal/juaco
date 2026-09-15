"""Batería de congelación de v7 = v6 + 2L (plasticidad estructural).  python bateria_v7.py [semillas]

CRITERIOS PREREGISTRADOS (fijados el 15 sep 2026, ANTES de correr 20 semillas).

Corrigen dos defectos de `bateria_v7c.py`, documentados en el registro:

  (a) Su última etapa, "control sin plasticidad", lleva los MISMOS criterios de éxito que el
      rescate, de modo que su resultado correcto es FALLA. Con esa redacción, "todo PASA" era
      literalmente insatisfacible y v7 no podía congelarse nunca. Aquí el control se evalúa
      invertido: se espera que FALLE, y sólo entonces cuenta como control negativo válido.

  (b) El registro afirmaba "divisiones en etapas normales: 0 en 6/6". Es FALSO. Medido con
      instrumentación (organismo_v7.py devuelve split_t): E1, E2I y E2J dan 0 divisiones, pero
      E2 (inversión) da 3-5 y E2K (D con solapamiento 2) da 2-4, en 6/6 semillas. Todas ocurren
      DESPUÉS del evento de t=50.000, sobre el estímulo que genera el error.
      El enunciado correcto, y el que se exige aquí, es más fuerte y más falsable:
          la regla no dispara sin error de predicción crónico;
          cuando lo hay, dispara sobre el estímulo que lo causa y nunca antes del evento.

CRITERIO DE CONGELACIÓN. v7 se congela si y sólo si, con 20 semillas:
  1. Las 5 etapas heredadas (E1, E2, E2I, E2J, E2K) pasan 20/20 los criterios idénticos a v6.
  2. E2L rescate (A∩B=3, códigos idénticos) pasa 20/20: separa solo, W_A=+1, W_B=-3.
  3. splits == 0 en E1, E2I, E2J (20/20) -- sin error crónico no hay división.
  4. splits > 0 en E2 y E2K (20/20) Y todas las divisiones en t > 50.000 (20/20).
  5. celdas <= 45 en TODAS las etapas (20/20) -- el crecimiento está acotado.
  6. El control sin plasticidad FALLA (<=1/20 lo pasa) -- si pasara, la plasticidad sobra.
Si algo falla, 2L vuelve a hipótesis y v6 sigue siendo el tronco. No se recalibra a posteriori.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # la consola Windows es cp1252
import numpy as np, organismo_v7 as o

S = int(sys.argv[1]) if len(sys.argv) > 1 else 6
seeds = range(1, S + 1)
EVENTO = 50000

tasa = lambda r, k, i: 100 * r['mord'][k][i] / max(r['vis'][k][i], 1)
sin_division   = lambda r: r['splits'] == 0
con_division   = lambda r: r['splits'] > 0
tras_evento    = lambda r: all(t > EVENTO for t, _ in r['split_t'])
crecimiento_ok = lambda r: r['celdas'] <= 45

fallos = []

def etapa(nombre, fn, crit):
    res = [fn(s) for s in seeds]
    ok = [all(c(r) for c in crit.values()) for r in res]
    det = " ".join(f"{n}:{sum(c(r) for r in res)}/{S}" for n, c in crit.items())
    if not all(ok): fallos.append(nombre)
    sp = [r['splits'] for r in res]
    print(f"{'PASA' if all(ok) else 'FALLA':5s} {nombre:38s} {sum(ok)}/{S}  [{det}]")
    print(f"      splits={sp}  celdas_max={max(r['celdas'] for r in res)}")
    return res

print(f"=== Batería de congelación v7 (v6 + 2L), {S} semillas ===")
print(f"    organismo_v7.py = organismo_v7c.py + registro de split_t (instrumentación inerte,")
print(f"    equivalencia verificada 21/21 escenarios x semillas)\n")

etapa("E1 aprendizaje A/B", lambda s: o.run(s),
  {"venenoQ4<Q1": lambda r: r['mord']['B'][3] < r['mord']['B'][0],
   "W_A≈+1": lambda r: abs(r['W']['A'] - 1) < .15,
   "W_B≈-3": lambda r: abs(r['W']['B'] + 3) < .3,
   "splits=0": sin_division, "celdas≤45": crecimiento_ok})

ctrl = [o.run(s, learn=False) for s in seeds]
print(f"      (control sin aprendizaje: muertes medianas {np.median([r['deaths'] for r in ctrl]):.0f})")

etapa("E2 inversión A<->B", lambda s: o.run(s, invertir_en=EVENTO),
  {"W_A→-3": lambda r: abs(r['W']['A'] + 3) < .3,
   "W_B→+1": lambda r: abs(r['W']['B'] - 1) < .15,
   "come B Q4≥50": lambda r: r['mord']['B'][3] >= 50,
   "splits>0": con_division, "divide tras evento": tras_evento, "celdas≤45": crecimiento_ok})

etapa("E2I nuevo C veneno sin olvido", lambda s: o.run(s, nuevo='C'),
  {"W_C≤-2.5": lambda r: r['W']['C'] <= -2.5,
   "W_A≈+1": lambda r: abs(r['W']['A'] - 1) < .15,
   "W_B≤-2.8": lambda r: r['W']['B'] <= -2.8,
   "tasaA Q4≥80%Q2": lambda r: tasa(r, 'A', 3) >= .8 * tasa(r, 'A', 1),
   "splits=0": sin_division, "celdas≤45": crecimiento_ok})

etapa("E2J nuevo D comida, D∩B=1", lambda s: o.run(s, nuevo='D', nuevo_val='comida', solap_B=1),
  {"W_D≥0.85": lambda r: r['W']['D'] >= .85, "W_B≤-2.7": lambda r: r['W']['B'] <= -2.7,
   "splits=0": sin_division, "celdas≤45": crecimiento_ok})

etapa("E2K nuevo D comida, D∩B=2", lambda s: o.run(s, nuevo='D', nuevo_val='comida', solap_B=2),
  {"W_D≥0.8": lambda r: r['W']['D'] >= .8, "W_B≤-2.4": lambda r: r['W']['B'] <= -2.4,
   "splits>0": con_division, "divide tras evento": tras_evento, "celdas≤45": crecimiento_ok})

etapa("E2L rescate A∩B=3 (códigos idénticos)", lambda s: o.run(s, solap_AB=3),
  {"W_A≈+1": lambda r: abs(r['W']['A'] - 1) < .15,
   "W_B≈-3": lambda r: abs(r['W']['B'] + 3) < .3,
   "solap→0": lambda r: r['solap']['AB'] == 0, "celdas≤45": crecimiento_ok})

# CONTROL NEGATIVO: se espera que FALLE. Si pasara, la plasticidad no aporta nada.
res_c = [o.run(s, solap_AB=3, plast=False) for s in seeds]
pasan_c = sum(abs(r['W']['A'] - 1) < .15 and abs(r['W']['B'] + 3) < .3 for r in res_c)
control_ok = pasan_c <= 1
if not control_ok: fallos.append("control negativo")
print(f"{'OK' if control_ok else 'ALERTA':5s} {'CTRL A∩B=3 SIN plasticidad (debe fallar)':38s} "
      f"{pasan_c}/{S} lo pasan  [esperado ≤1/{S}] -> "
      f"{'control negativo válido' if control_ok else 'CONTROL INVÁLIDO: la plasticidad no aporta'}")
print(f"      W_A mediana {np.median([r['W']['A'] for r in res_c]):+.2f}  "
      f"W_B mediana {np.median([r['W']['B'] for r in res_c]):+.2f}  (sin plasticidad los valores colapsan)")

print()
if fallos:
    print(f"*** v7 NO SE CONGELA. Fallaron: {', '.join(fallos)}.")
    print("*** 2L vuelve a hipótesis; v6 sigue siendo el tronco. No recalibrar a posteriori.")
else:
    print(f"*** v7 CUMPLE LOS {6} CRITERIOS PREREGISTRADOS con {S} semillas.")
    print("*** Congelar sólo si S>=20. Pendiente conocido y fuera de esta batería:")
    print("*** política bajo hambre (mordidas de veneno ~1-4% por visita en inanición).")
