"""Agente A (trio XOR, bloque 3c) - mini-prueba de UN proceso (sin Pool), PUENTE_xor.md.
Hipotesis: regla delta con signo (Ws, un solo vector) en vez de Wps/Wns no negativos con drenaje.
Paso 1: chequeo de identidad barato (T chico) entre organismo_v13q_A.py (regla_lenta='dos_canales', el default)
        y el organismo_v13q.py ORIGINAL (sin tocar) - confirma que el knob nuevo no cambio nada cuando esta apagado.
Paso 2: 3 semillas x {xor01, px0}, T=100000, lectura='cuadratica', eta_s=0.015, puerta=3, regla_lenta='delta'.
        Mide acc_lenta = signo_acc(W_lenta_apriori, test, vr) - formula identica a corre_xor_3b.py:signo_acc.
Uso: python experimentos/nivel7_xor_lectura/trio_A/mini_prueba_A.py
"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
PADRE = os.path.dirname(AQUI)   # experimentos/nivel7_xor_lectura
sys.path[:0] = [AQUI, PADRE]
import organismo_v13q_A as m_a          # la copia con el knob (este agente)
import organismo_v13q as m_orig         # el original, SIN TOCAR (control de identidad)

t0 = time.time()


def log(msg=""):
    print(f"[{time.strftime('%H:%M:%S')} +{time.time()-t0:6.1f}s] {msg}", flush=True)


def N(x):
    return json.loads(json.dumps(x, default=str))


def signo_acc(Wd, test, vr):   # copiado literal de experimentos/nivel7_xor_lectura/corre_xor_3b.py (linea 36-39)
    f = [1.0 if Wd[k] > 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (0.5 if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


# ---------- Paso 1: identidad (T chico, no cuenta como "corrida de 100000") ----------
log("PASO 1 -- identidad organismo_v13q_A(regla_lenta='dos_canales', default) == organismo_v13q original")
ident_ok = True
for regla in ('xor01', 'px0'):
    for seed in (1, 2):
        kw = dict(T=2000, mundo='regla', regla=regla, lectura='cuadratica', eta_s=0.015, puerta=3, fase2_en=1000, sonda_final=True)
        ra = m_a.run(seed, **kw)                      # default regla_lenta='dos_canales'
        ro = m_orig.run(seed, **kw)
        # solo comparamos las claves que YA existian en el original (la copia añade Ws/regla_lenta, se ignoran)
        dif = [kk for kk in ro if N(ro[kk]) != N(ra[kk])]
        if dif:
            ident_ok = False
            log(f"  DIFIERE regla={regla} seed={seed}: {dif}")
        else:
            log(f"  ok regla={regla} seed={seed}: identico en {len(ro)} claves")
log(f"IDENTIDAD (dos_canales == original): {'OK' if ident_ok else '*** FALLA ***'}")
if not ident_ok:
    log("*** se para: la identidad con el knob apagado es obligatoria (EQUIPO.md regla 2) ***")
    sys.exit(1)

# ---------- Paso 2: hipotesis (regla_lenta='delta'), 3 semillas x 2 reglas, T=100000 ----------
SEEDS = [1, 2, 3]
REGLAS = ['xor01', 'px0']
BASE = dict(T=100000, mundo='regla', lectura='cuadratica', eta_s=0.015, puerta=3, regla_lenta='delta')
log(f"PASO 2 -- hipotesis delta: {BASE}, semillas {SEEDS}")
filas = []
for regla in REGLAS:
    log(f"  -- regla={regla} --")
    for seed in SEEDS:
        r = m_a.run(seed, regla=regla, **BASE)
        vr = m_a.split_regla(seed, regla)[3]
        test = r['test']
        acc_lenta = signo_acc(r['W_lenta_apriori'], test, vr)
        acc_total = signo_acc(r['W_apriori'], test, vr)
        fam = [r['familiar_apriori'][k] for k in test]
        Ws_prod01 = r['Ws'][6] if len(r['Ws']) > 6 else None   # peso del producto P0*P1 (indice 6 = primer par (0,1))
        fila = dict(seed=seed, regla=regla, acc_lenta=round(acc_lenta, 3), acc_total=round(acc_total, 3),
                    familiar=round(float(np.mean(fam)), 2) if fam else None, splits=r['splits'], celdas=r['celdas'],
                    deaths=r['deaths'], Ws_prod01=round(Ws_prod01, 3) if Ws_prod01 is not None else None)
        filas.append(fila)
        log(f"    seed={seed} acc_lenta={fila['acc_lenta']:.3f}  acc_total={fila['acc_total']:.3f}  "
            f"familiar={fila['familiar']}  Ws(P0*P1)={fila['Ws_prod01']}  splits={fila['splits']} celdas={fila['celdas']} deaths={fila['deaths']}")

log("")
log("RESUMEN por regla (mediana, min, max de acc_lenta):")
for regla in REGLAS:
    xs = [f['acc_lenta'] for f in filas if f['regla'] == regla]
    log(f"  {regla:6s} acc_lenta mediana={float(np.median(xs)):.3f}  [{min(xs):.3f},{max(xs):.3f}]  n={len(xs)}")

# ---------- controles rapidos (mismo presupuesto, ya corrido arriba con puerta=3 en px0 sirve de control de validez) ----------
out = dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), seeds=SEEDS, base=BASE, agente='A', hipotesis='delta_con_signo'),
           identidad_ok=ident_ok, filas=filas)
dest = os.path.join(AQUI, 'mini_prueba_A_resultado.json')
json.dump(out, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
log(f"guardado -> {dest}")
