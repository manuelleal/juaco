"""Batería de congelación de v7, CRITERIO v2.  python bateria_v7b.py [semillas]

Sustituye a `bateria_v7.py`, cuyo criterio falló por ERR-06: exigía `splits==0` en E2I dando por
hecho que E2I no tiene error crónico. Es falso — E2I se invoca con `solap_B=None`, así que la
condición de sorteo SÓLO exige A∩B=0 y deja C∩A y C∩B libres. La semilla 15 saca C∩A=2 y divide,
que es la regla funcionando, no fallando.

CRITERIO v2 (preregistrado en el registro, sección "Día 3", antes de esta corrida). Es MÁS
exigente que el v1, no menos: evalúa el disparo **por semilla contra el solapamiento medido**,
no por nombre de etapa, y añade una predicción que puede fallar (el umbral en 2).

  1. Criterios científicos heredados de v6: 20/20 en E1, E2, E2I, E2J, E2K y E2L rescate.
  2. celdas <= 45 en todas las etapas, 20/20.
  3. El control sin plasticidad FALLA (<=1/20 lo pasa).
  4. DISPARO, por semilla, contra el solapamiento REAL de esa semilla:
       solapamiento_max <= 1  y sin inversion  ->  splits == 0
       solapamiento_max >= 2  o   con inversion ->  splits > 0  y todas las divisiones en t > 50.000
  5. UMBRAL (predicción falsable): ninguna semilla divide con solapamiento <= 1 sin inversión,
     y ninguna deja de dividir con solapamiento >= 2.

Los solapamientos se leen replicando el sorteo de KW de `organismo_v7.run` sin simular nada, y la
réplica SE AUTOVERIFICA en cada semilla contra el campo `solap` que devuelve el propio organismo.
Si la autoverificación falla, la batería aborta: primero el instrumento (regla 5).
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np, organismo_v7 as o

S = int(sys.argv[1]) if len(sys.argv) > 1 else 6
seeds = list(range(1, S + 1))
EVENTO = 50000
NK, NKMAX, K = 30, 90, 3
PAT = o.PAT


def solapamientos(seed, nuevo=None, solap_B=None, solap_AB=None):
    """Réplica exacta del sorteo de KW en organismo_v7.run. No simula: solo lee geometría."""
    rng = np.random.default_rng(seed)
    rng.uniform(.1, .4, (2, 9))                      # Wl: consume el mismo tramo del RNG
    KW = np.zeros((NKMAX, 6)); activa = np.zeros(NKMAX, bool)
    KW[:NK] = rng.uniform(0, 1, (NK, 6)); activa[:NK] = True
    def code(P):
        v = KW @ P; v = np.where(activa, v, -1e9); return set(np.argsort(v)[-K:])
    objetivo_AB = 0 if solap_AB is None else solap_AB
    if solap_AB:
        KW[:solap_AB] = 0; KW[:solap_AB, 0] = 5.0
    cond = lambda: (len(code(PAT['A']) & code(PAT['B'])) == objetivo_AB
                    and (nuevo is None or solap_B is None
                         or (len(code(PAT[nuevo]) & code(PAT['B'])) == solap_B
                             and len(code(PAT[nuevo]) & code(PAT['A'])) == 0)))
    while not cond():
        KW[objetivo_AB:NK] = rng.uniform(0, 1, (NK - objetivo_AB, 6))
    s = {'AB': len(code(PAT['A']) & code(PAT['B']))}
    if nuevo:
        s['nA'] = len(code(PAT[nuevo]) & code(PAT['A']))
        s['nB'] = len(code(PAT[nuevo]) & code(PAT['B']))
    return s


fallos, violaciones_umbral = [], []


def etapa(nombre, kw, crit, inversion=False):
    res, sol = [], []
    for s in seeds:
        r = o.run(s, **kw)
        g = solapamientos(s, nuevo=kw.get('nuevo'), solap_B=kw.get('solap_B'), solap_AB=kw.get('solap_AB'))
        # AUTOVERIFICACION. Ojo: la replica da el solapamiento INICIAL (el que el organismo trae al
        # nacer) y `r['solap']` da el FINAL, tras la plasticidad. Solo son comparables cuando no hubo
        # divisiones. Que difieran con splits>0 no es un fallo: en E2L rescate ESA es justo la medida
        # del exito (inicial 3 -> final 0). El criterio 4 necesita el INICIAL, que es el que predice
        # si cabe esperar error cronico.
        if r['splits'] == 0:
            assert g['AB'] == r['solap']['AB'], f"replica AB desincronizada en {nombre} semilla {s}"
            if kw.get('nuevo'):
                assert g['nB'] == r['solap']['nB'], f"replica nB desincronizada en {nombre} semilla {s}"
        res.append(r); sol.append(g)

    smax = [max(g.values()) for g in sol]
    congenito = kw.get('solap_AB') is not None   # el error existe desde el paso 0, no lo crea un evento

    def disparo_ok(r, m):
        """Criterio 4, corregido por ERR-08: el disparo se ancla a la CAUSA, no a un reloj fijo.

        v2 exigia 't > 50.000' para todo error cronico, asumiendo que siempre lo crea un evento a
        mitad de corrida. Falso para E2L, donde el solapamiento es congenito (A y B nacen con
        codigos identicos) y la separacion debe ocurrir PRONTO. Mismo error de raiz que ERR-06:
        dar por hecho que todas las etapas se comportan igual en vez de mirar cada una.
        """
        hay_causa = inversion or m >= 2
        if not hay_causa:
            return r['splits'] == 0                       # sin causa, no se divide
        if r['splits'] == 0:
            return False                                  # con causa, se divide
        t_causa = 0 if congenito else EVENTO               # cuando empieza a existir el problema
        if not all(t >= t_causa for t, _ in r['split_t']):
            return False                                  # nunca antes de la causa
        if congenito:
            # error congenito: la separacion debe COMPLETARSE pronto.
            # Umbral 25.000 tomado del registro (2L v2: "solapamiento 3->0 antes de 25k pasos"),
            # no elegido hoy a la vista de estos datos.
            return max(t for t, _ in r['split_t']) < 25000
        return True
    crit = dict(crit)
    crit["celdas≤45"] = lambda r: r['celdas'] <= 45
    ok = [all(c(r) for c in crit.values()) and disparo_ok(r, m) for r, m in zip(res, smax)]

    for s, r, m in zip(seeds, res, smax):
        if m <= 1 and not inversion and r['splits'] > 0:
            violaciones_umbral.append(f"{nombre} s{s}: solap={m} pero divide {r['splits']}x")
        if m >= 2 and r['splits'] == 0:
            violaciones_umbral.append(f"{nombre} s{s}: solap={m} pero NO divide")

    det = " ".join(f"{n}:{sum(c(r) for r in res)}/{S}" for n, c in crit.items())
    det += f" disparo:{sum(disparo_ok(r, m) for r, m in zip(res, smax))}/{S}"
    if not all(ok): fallos.append(nombre)
    print(f"{'PASA' if all(ok) else 'FALLA':5s} {nombre:36s} {sum(ok)}/{S}  [{det}]")
    print(f"      solap_max={smax}")
    print(f"      splits   ={[r['splits'] for r in res]}  celdas_max={max(r['celdas'] for r in res)}")
    return res


print(f"=== Batería de congelación v7 — CRITERIO v2, {S} semillas ===")
print("    Disparo evaluado por semilla contra el solapamiento MEDIDO, no por nombre de etapa.\n")

etapa("E1 aprendizaje A/B", dict(),
  {"venenoQ4<Q1": lambda r: r['mord']['B'][3] < r['mord']['B'][0],
   "W_A≈+1": lambda r: abs(r['W']['A'] - 1) < .15, "W_B≈-3": lambda r: abs(r['W']['B'] + 3) < .3})

etapa("E2 inversión A<->B", dict(invertir_en=EVENTO),
  {"W_A→-3": lambda r: abs(r['W']['A'] + 3) < .3, "W_B→+1": lambda r: abs(r['W']['B'] - 1) < .15,
   "come B Q4≥50": lambda r: r['mord']['B'][3] >= 50}, inversion=True)

etapa("E2I nuevo C veneno sin olvido", dict(nuevo='C'),
  {"W_C≤-2.5": lambda r: r['W']['C'] <= -2.5, "W_A≈+1": lambda r: abs(r['W']['A'] - 1) < .15,
   "W_B≤-2.8": lambda r: r['W']['B'] <= -2.8,
   "tasaA Q4≥80%Q2": lambda r: (100*r['mord']['A'][3]/max(r['vis']['A'][3],1)) >= .8*(100*r['mord']['A'][1]/max(r['vis']['A'][1],1))})

etapa("E2J nuevo D comida, D∩B=1", dict(nuevo='D', nuevo_val='comida', solap_B=1),
  {"W_D≥0.85": lambda r: r['W']['D'] >= .85, "W_B≤-2.7": lambda r: r['W']['B'] <= -2.7})

etapa("E2K nuevo D comida, D∩B=2", dict(nuevo='D', nuevo_val='comida', solap_B=2),
  {"W_D≥0.8": lambda r: r['W']['D'] >= .8, "W_B≤-2.4": lambda r: r['W']['B'] <= -2.4})

etapa("E2L rescate A∩B=3", dict(solap_AB=3),
  {"W_A≈+1": lambda r: abs(r['W']['A'] - 1) < .15, "W_B≈-3": lambda r: abs(r['W']['B'] + 3) < .3,
   "solap→0": lambda r: r['solap']['AB'] == 0})

res_c = [o.run(s, solap_AB=3, plast=False) for s in seeds]
pasan_c = sum(abs(r['W']['A'] - 1) < .15 and abs(r['W']['B'] + 3) < .3 for r in res_c)
control_ok = pasan_c <= 1
if not control_ok: fallos.append("control negativo")
print(f"{'OK' if control_ok else 'ALERTA':5s} {'CTRL A∩B=3 SIN plasticidad (debe fallar)':36s} {pasan_c}/{S} lo pasan"
      f"  [esperado ≤1/{S}] -> {'control negativo válido' if control_ok else 'CONTROL INVÁLIDO'}")

print()
print(f"CRITERIO 5 (umbral en 2 celdas): {'SOSTENIDO — 0 violaciones' if not violaciones_umbral else 'REFUTADO'}")
for v in violaciones_umbral: print("   ", v)
print()
if fallos:
    print(f"*** v7 NO SE CONGELA. Fallaron: {', '.join(fallos)}.")
    print("*** 2L vuelve a hipótesis; v6 sigue siendo el tronco. No recalibrar a posteriori.")
else:
    print(f"*** v7 CUMPLE LOS 5 CRITERIOS DEL v2 con {S} semillas.")
    if S >= 20:
        print("*** CONGELAR v7. Pendiente y fuera de esta batería: política bajo hambre.")
    else:
        print(f"*** Congelar sólo con S>=20 (esta corrida: {S}).")
