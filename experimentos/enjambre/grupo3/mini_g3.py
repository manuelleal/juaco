"""MINI-EQUIPO 3 (sala de enjambre) -- mini-prueba de UN proceso (EQUIPO.md regla 3: sin multiprocessing.Pool,
<= 200000 pasos por corrida) del mecanismo M3 (memoria de un golpe por combinacion) sobre organismo_g3.py.

NO es la serie (esa la corre el coordinador con Pool y 20 semillas nuevas). Esto es humo declarado: semillas 1-3,
T=100000, con las CONSTANTES DEL TRONCO v14.1 (eta_s=0.15, clip_s=10, regla_lenta='delta_signo', constante=True,
puerta=3) y lectura='cuadratica' (NUNCA 'oraculo01' como brazo principal, por instruccion del jefe de investigacion;
en M3 la lectura es de hecho INERTE -- ver nota mas abajo -- pero se respeta la instruccion igual).

Que mide, por regla (xor01/px0/azar) x semilla (1-3) x brazo (memoria='combi'|'combi1'):
  - acc_lenta a priori (sonda en fase2_en=T//2, SOLO con lo aprendido de las `tren` patrones): puntuacion del
    registro (empate=0.5, signo_acc de corre_xor_4.py) y puntuacion ESTRICTA (empate=0).
  - EXPOSICIONES: replay del flujo real (t,patron,R) que el organismo grabo con lab=True, recortado a los
    primeros n encuentros PRE-sonda, para cada n de una rejilla -- el mismo metodo de corre_xor_4.py
    (`exposiciones()`), pero con la regla de ACTUALIZACION de M3 (escritura de un golpe por celda x combinacion)
    en vez de la regla delta. n* = primer n con la MEDIANA (3 semillas) >= 0.75.
  - mem_ganadora EN LA SONDA (no al final de T): que celda (par de pixeles) gano, calculada con el MISMO replay
    sobre TODOS los eventos pre-sonda -- y verificada contra W_lenta_apriori del organismo (deben coincidir
    EXACTO; si no, el replay no sirve y se declara asi, no se usan sus numeros).
  - "abre el rasgo conjuntivo" en xor01 = la celda ganadora en la sonda es exactamente (0,1) (los DOS pixeles que
    definen xor01).

NOTA declarada: en M3, `lenta(P)` lee P[i],P[j] CRUDOS (no phi(P)) -- por diseno, `lectura` no cambia ni la
regla de escritura ni la de lectura de M3 (solo el tamano de Wps/Wns/Ws, que M3 no usa). Se reporta para que
quede escrito, no para reclamar nada.

Sin Pool. Sin commits. Solo escribe dentro de experimentos/enjambre/grupo3/. Uso:
  python experimentos/enjambre/grupo3/mini_g3.py
"""
import json, os, sys, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]   # ERR-28: organismo/ primero
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import organismo_g3 as G3

STAMP = time.strftime('%Y%m%d_%H%M%S')
LOGP = os.path.join(AQUI, f'mini_g3_{STAMP}.log')
_LOG = open(LOGP, 'w', encoding='utf-8', newline='\n')
_T0 = time.time()


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_T0:7.1f}s] {msg}"
    print(linea, flush=True)
    _LOG.write(linea + "\n"); _LOG.flush(); os.fsync(_LOG.fileno())


SEEDS = [1, 2, 3]
REGLAS = ['xor01', 'px0', 'azar']
BRAZOS = ['combi', 'combi1']
BASE = dict(T=100000, mundo='regla', lectura='cuadratica', regla_lenta='delta_signo', constante=True,
            eta_s=0.15, clip_s=10.0, puerta=3, lab=True)   # constantes del tronco v14.1
MEM_ALFA = 0.3; MEM_RHO = 0.02
PAR = [(i, j) for i in range(6) for j in range(i + 1, 6)]
REJ = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16, 20, 25, 30, 40, 60, 80, 100, 150, 200, 300, 400, 600]


def signo_acc(Wd, test, vr, estricto=False):
    """Acierto BALANCEADO por signo sobre los nunca vistos. Empate: 0.5 (registro) o 0.0 (estricto).
    Formula identica a corre_xor_4.py, con la unica diferencia declarada del empate."""
    empate = 0.0 if estricto else 0.5
    f = [1.0 if Wd[k] > 0 else (empate if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if Wd[k] < 0 else (empate if Wd[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    if not f or not p:
        return None
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


def replay_memoria(eventos, memoria, mem_alfa=MEM_ALFA, mem_rho=MEM_RHO):
    """Repite la regla local de M3 (organismo_g3.py, ancla 4) FUERA del organismo, sobre una secuencia de eventos
    (t, patron, R, _ds) ya ordenada. `patron` es la clave de 6 caracteres ('0'/'1') que graba el organismo con
    lab=True. Devuelve (MM, MN, ME, MG) -- el mismo estado que tendria el organismo tras esos eventos."""
    MM = np.zeros((15, 4)); MN = np.zeros((15, 4)); ME = np.full(15, 1e9); MG = 0
    for (_t, patron, R, _ds) in eventos:
        Pk = np.array([float(c) for c in patron])
        for c in range(15):
            i, j = PAR[c]; dirn = int(Pk[i]) * 2 + int(Pk[j])
            p = float(MM[c, dirn]) if MN[c, dirn] > 0 else 0.0
            d = R - p; primera = bool(MN[c].sum() == 0)
            ME[c] = (d * d) if primera else (1 - mem_rho) * ME[c] + mem_rho * (d * d)
            if MN[c, dirn] == 0: MM[c, dirn] = R
            elif memoria == 'combi': MM[c, dirn] += mem_alfa * (R - MM[c, dirn])
            MN[c, dirn] += 1
        MG = int(np.argmin(ME))
    return MM, MN, ME, MG


def leer_memoria(MM, MN, MG, P):
    i, j = PAR[MG]; dirn = int(P[i]) * 2 + int(P[j])
    return float(MM[MG, dirn]) if MN[MG, dirn] > 0 else 0.0


if __name__ == '__main__':
    sha_g3 = __import__('hashlib').sha256(open(G3.__file__, 'rb').read()).hexdigest()[:16]
    log(f"ARRANQUE mini_g3 (UN proceso, sin Pool). organismo_g3.py sha {sha_g3}. "
        f"semillas {SEEDS}, reglas {REGLAS}, brazos {BRAZOS}, BASE={BASE}")
    filas = []          # una fila por (regla, seed, brazo): todo lo medido
    verif_fallos = []   # (regla, seed, brazo): el replay no coincidio con el organismo
    for regla in REGLAS:
        for brazo in BRAZOS:
            for seed in SEEDS:
                t1 = time.time()
                kw = dict(BASE, regla=regla)
                r = G3.run(seed, memoria=brazo, mem_alfa=MEM_ALFA, mem_rho=MEM_RHO, **kw)
                pats, tren, test, vr = G3.split_regla(seed, regla)
                acc_reg = signo_acc(r['W_lenta_apriori'], test, vr, estricto=False)
                acc_estr = signo_acc(r['W_lenta_apriori'], test, vr, estricto=True)
                pre = [e for e in r['lenta_eventos'] if e[0] < r['fase2_en']]
                MM, MN, ME, MG = replay_memoria(pre, brazo)
                # verificacion: el replay sobre TODOS los eventos pre-sonda debe dar EXACTO lo mismo que W_lenta_apriori
                pred_replay = {k: leer_memoria(MM, MN, MG, v) for k, v in pats.items()}
                dif = {k: (pred_replay[k], r['W_lenta_apriori'][k]) for k in pats
                       if abs(pred_replay[k] - r['W_lenta_apriori'][k]) > 1e-9}
                replay_ok = not dif
                if not replay_ok:
                    verif_fallos.append((regla, seed, brazo, dif))
                acc_replay = signo_acc(pred_replay, test, vr)
                # 4 clases (P0,P1) presentes en tren: sub-analisis declarado en el mecanismo (control de abstencion)
                clases_tren = {(int(pats[k][0]), int(pats[k][1])) for k in tren}
                clases_4 = len(clases_tren) == 4
                # exposiciones: replay de PREFIJOS de la misma secuencia pre-sonda
                curva = {}
                for n in REJ:
                    if n > len(pre):
                        curva[n] = None; continue
                    MMn, MNn, MEn, MGn = replay_memoria(pre[:n], brazo)
                    predn = {k: leer_memoria(MMn, MNn, MGn, v) for k, v in pats.items()}
                    curva[n] = signo_acc(predn, test, vr)
                fila = dict(regla=regla, seed=seed, brazo=brazo, T=BASE['T'], fase2_en=r['fase2_en'],
                            n_pre=len(pre), acc_lenta=acc_reg, acc_lenta_estricta=acc_estr, acc_total=signo_acc(r['W_apriori'], test, vr),
                            mem_ganadora_sonda=list(PAR[MG]), mem_ganadora_final=r['mem_ganadora'],
                            mem_vistas_final=r['mem_vistas'], abre_conjuntivo=bool(list(PAR[MG]) == [0, 1]),
                            clases_4_en_tren=clases_4, n_tren=len(tren), n_test=len(test),
                            replay_ok=replay_ok, curva=curva, splits=r['splits'], celdas=r['celdas'], deaths=r['deaths'])
                filas.append(fila)
                log(f"  {regla:5s} s{seed} {brazo:7s}: acc_lenta {acc_reg} (estricta {acc_estr})  "
                    f"ganadora_sonda {list(PAR[MG])}  vistas_fin {r['mem_vistas']}  eventos_pre {len(pre)}  "
                    f"4clases_tren {clases_4}  replay_ok {replay_ok}  ({time.time()-t1:.1f}s)")

    log("\n=== TABLA: acc_lenta por regla x brazo (mediana [min,max] sobre 3 semillas) ===")
    resumen = {}
    for regla in REGLAS:
        for brazo in BRAZOS:
            g = [f for f in filas if f['regla'] == regla and f['brazo'] == brazo]
            reg_vals = [f['acc_lenta'] for f in g]
            estr_vals = [f['acc_lenta_estricta'] for f in g]
            ge75 = sum(1 for x in reg_vals if x is not None and x >= 0.75)
            ge75_estr = sum(1 for x in estr_vals if x is not None and x >= 0.75)
            abre = sum(f['abre_conjuntivo'] for f in g)
            c4 = sum(f['clases_4_en_tren'] for f in g)
            med = lambda xs: (float(np.median(xs)), float(min(xs)), float(max(xs))) if xs and all(x is not None for x in xs) else (None, None, None)
            mr, minr, maxr = med(reg_vals); me, mine, maxe = med(estr_vals)
            resumen[f'{regla}/{brazo}'] = dict(acc_lenta_mediana=mr, acc_lenta_rango=[minr, maxr],
                                                acc_lenta_estricta_mediana=me, acc_lenta_estricta_rango=[mine, maxe],
                                                n_ge_075=f"{ge75}/{len(g)}", n_ge_075_estricta=f"{ge75_estr}/{len(g)}",
                                                abre_conjuntivo=f"{abre}/{len(g)}", clases_4_en_tren=f"{c4}/{len(g)}")
            log(f"  {regla:5s}/{brazo:7s}: acc_lenta {mr} [{minr},{maxr}]  estricta {me} [{mine},{maxe}]  "
                f">=0.75: {ge75}/{len(g)} (estricta {ge75_estr}/{len(g)})  abre(0,1): {abre}/{len(g)}  4clases_tren: {c4}/{len(g)}")

    log("\n=== EXPOSICIONES: curva mediana (3 semillas) por regla x brazo; n* = primer n con mediana >= 0.75 ===")
    curvas_resumen = {}
    for regla in REGLAS:
        for brazo in BRAZOS:
            g = [f for f in filas if f['regla'] == regla and f['brazo'] == brazo]
            curva_med = {}
            for n in REJ:
                vals = [f['curva'][n] for f in g if f['curva'][n] is not None]
                curva_med[n] = float(np.median(vals)) if len(vals) == len(g) else None
            n75 = next((n for n in REJ if curva_med[n] is not None and curva_med[n] >= 0.75), None)
            curvas_resumen[f'{regla}/{brazo}'] = dict(curva=curva_med, n_estrella_075=n75)
            log(f"  {regla:5s}/{brazo:7s}: n*(>=0.75) = {n75 if n75 is not None else '>' + str(REJ[-1])}   "
                + ' '.join(f'{n}:{curva_med[n]:.2f}' if curva_med[n] is not None else f'{n}:--' for n in REJ if n <= 30))

    log("\n=== CONTROLES: px0 debe ser 1.000 en todos; azar debe caer en [0.35,0.65] ===")
    px0_vals = [f['acc_lenta'] for f in filas if f['regla'] == 'px0']
    azar_vals = [f['acc_lenta'] for f in filas if f['regla'] == 'azar']
    px0_ok = all(x is not None and abs(x - 1.0) < 1e-9 for x in px0_vals)
    azar_med = float(np.median(azar_vals)) if azar_vals else None
    azar_ok = azar_med is not None and 0.35 <= azar_med <= 0.65
    log(f"  px0: {px0_vals}  -> {'OK 1.000 en todos' if px0_ok else 'FALLA'}")
    log(f"  azar: {azar_vals}  mediana {azar_med}  -> {'OK en [0.35,0.65]' if azar_ok else 'FUERA DE RANGO'}")

    if verif_fallos:
        log(f"\n*** VERIFICACION DEL REPLAY: {len(verif_fallos)} casos donde el replay NO coincidio con el organismo (no se confia en esos numeros de exposiciones):")
        for regla, seed, brazo, dif in verif_fallos:
            log(f"    {regla} s{seed} {brazo}: {dif}")
    else:
        log(f"\nVERIFICACION DEL REPLAY: {len(filas)}/{len(filas)} casos coinciden EXACTO con W_lenta_apriori del organismo (0 diferencias).")

    dj = os.path.join(AQUI, f'mini_g3_{STAMP}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), seeds=SEEDS, reglas=REGLAS, brazos=BRAZOS,
                             base=BASE, mem_alfa=MEM_ALFA, mem_rho=MEM_RHO, sha_organismo_g3=sha_g3,
                             python_numpy=np.__version__),
                   filas=filas, resumen=resumen, curvas=curvas_resumen,
                   controles=dict(px0_ok=px0_ok, px0_vals=px0_vals, azar_ok=azar_ok, azar_mediana=azar_med, azar_vals=azar_vals),
                   verificacion_replay=dict(fallos=len(verif_fallos), total=len(filas))),
              open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str, indent=1)
    log(f"\ndatos -> {os.path.basename(dj)}")
    log(f"FIN mini_g3 ({time.time()-_T0:.1f}s total)")
    _LOG.close()
