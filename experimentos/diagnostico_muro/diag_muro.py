"""diag_muro.py — DIAGNOSTICO DEL MURO (H-MURO, "pastoreo selectivo"), preregistrada en
PREREGISTRO_diag_muro.md. Corre organismo_f9c_muro.run (instrumento por anclas de organismo_f9c.py,
identidad_muro.py) con los BRAZOS EXACTOS de fase 9 bloque 2 (corre_bloque2.BRAZOS), rep_acum=0.

MISION: llegar a la AGI por este camino. PROBLEMA: R0 < 0.9 incluso con el nodo ORACULO (fase 9 bloque 2).
H-MURO: lo bueno sale del mundo al comerse; lo malo solo por renovacion (decay=0.003/paso); un cuerpo que
evita bien lo malo enriquece el mundo en lo malo.

Un solo proceso, SIN Pool, semillas 2941-2946, T=100000. Presupuesto de CPU declarado: <= 25 min.

    python diag_muro.py --humo      (UN proceso, 3 corridas cortas T=5000: sanity antes de la serie)
    python diag_muro.py             (LA SERIE: 3 brazos x 6 semillas x T=100000, serie DENTRO del proceso)
"""
import argparse
import json
import os
import statistics as st
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N09B2 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2')
sys.path[:0] = [N09B2]
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import corre_bloque2 as B2         # inserta N09B2, N09, N13, N11, organismo/ al frente de sys.path
sys.path.insert(0, AQUI)
import organismo_f9c_muro as F9M
import identidad_muro as IDM

N, h16, med = B2.N, B2.h16, B2.med
DATOS = os.path.join(RAIZ, 'datos')
HUMO = os.path.join(DATOS, 'humo')
BRAZOS_DIAG = ['NADA', 'REL', 'ORACULO']
SEMILLAS = list(range(2941, 2947))     # 6 semillas nuevas (verificadas libres: fuera de 2441-2940, 3001-3299,
                                        # 4001-4199, 5001-5020, 6001-6020)
T = 100000
W_VENTANA = 200                        # pasos previos a cada muerte que promedia mu9_fbw (ver organismo_f9c_muro.py)

LOG = [None]


def log(msg=""):
    print(msg, flush=True)
    if LOG[0]:
        LOG[0].write(msg + "\n"); LOG[0].flush(); os.fsync(LOG[0].fileno())


def sello():
    return time.strftime('%Y%m%d_%H%M%S')


# ------------------------------------------------------------------ regla 14 (entrada campo a campo)
def regla14():
    """Los BRAZOS que uso son el MISMO objeto dict que corre_bloque2.BRAZOS (importado, no copiado a mano):
    la comparacion campo a campo es trivial por construccion, pero se imprime para el registro."""
    filas = []
    for b in BRAZOS_DIAG:
        d = B2.BRAZOS[b]
        filas.append((b, len(d), True, f"= corre_bloque2.BRAZOS[{b!r}] (mismo objeto, {len(d)} campos)"))
        log(f"  OK  regla14 {b:8s} {len(d)} campos IDENTICOS a corre_bloque2.BRAZOS (importado, no copiado)")
    return filas


# ------------------------------------------------------------------ analisis de una corrida
def vida_util(r):
    """Reconstruye, de SOLO LECTURA sobre campos YA EXISTENTES (vidas_h1, desc_por_vida, t_desc), la EDAD
    al PRIMER PARTO de cada cuerpo. vidas_h1[i] y desc_por_vida[i] estan en ORDEN CRONOLOGICO (H1); t_desc es
    la lista GLOBAL (hasta 200) de los tiempos absolutos en que CUALQUIER cuerpo cerro una ventana. Un cuerpo
    con desc_por_vida[i]==0 no tuvo ningun t_desc en su ventana [nace_i, nace_i+vida_i) -- no hace falta
    buscarlo, ya lo dice esa cuenta. Para los que SI, el primer t_desc dentro de esa ventana es su primer parto."""
    vidas = r.get('vidas_h1') or []
    dpv = r.get('desc_por_vida') or []
    tdesc = sorted(r.get('t_desc') or [])
    n = min(len(vidas), len(dpv))
    nace = 0
    edades1 = []          # edad al primer parto, SOLO de los cuerpos que parieron
    q0 = 0                # cuerpos que murieron SIN parir ni una vez
    post = []             # (descendientes-1, tiempo_restante_tras_el_primer_parto) de los que parieron
    j = 0                 # puntero en tdesc (creciente, tdesc esta ordenado y las ventanas de los cuerpos son disjuntas y consecutivas)
    truncado = False
    for i in range(n):
        v, d = vidas[i], dpv[i]
        fin = nace + v
        if d == 0:
            q0 += 1
        else:
            while j < len(tdesc) and tdesc[j] < nace:
                j += 1     # no deberia pasar (las ventanas son consecutivas), defensivo
            primeros = []
            k = j
            while k < len(tdesc) and tdesc[k] < fin:
                primeros.append(tdesc[k]); k += 1
            if not primeros:
                truncado = True   # el cuerpo SI parió (d>0) pero su(s) t_desc cayeron fuera de los 200 guardados
            else:
                e1 = primeros[0] - nace
                edades1.append(e1)
                post.append((d - 1, max(v - e1, 0)))
                j = k
        nace = fin
    return dict(edades1=edades1, q0=q0, n=n, post=post, truncado=truncado)


def analiza_uno(brazo, seed, r):
    o = dict(B2.resumen(brazo, seed, 0, r, 0.0))
    m = r['muro']
    pres = m['pres']; pasos = m['pasos']; nobj = m['nobj']
    total_pres = sum(pres.values())
    f = {k: pres[k] / total_pres for k in 'ABCD'}       # fraccion de PRESENCIA (tiempo x objeto), suma 1
    f_mala = f['B'] + f['D']
    bites = {k: sum(r['mord'][k]) for k in 'ABCD'}
    d_por_obj = m['decay_p'] / nobj
    lam = {k: d_por_obj + (bites[k] / pres[k] if pres[k] else 0.0) for k in 'ABCD'}
    inv = {k: 1.0 / lam[k] if lam[k] > 0 else 0.0 for k in 'ABCD'}
    s_inv = sum(inv.values())
    f_pred = {k: inv[k] / s_inv for k in 'ABCD'} if s_inv else {k: 0.25 for k in 'ABCD'}
    pdb = [x for x in m['pre_death_bad'] if x is not None]
    causas = m['pre_death_causa']
    vt = vida_util(r)
    R0_vt = (sum(vt['post'][i][0] + 1 for i in range(len(vt['post']))) / vt['n']) if vt['n'] else None
    # elasticidad (b), SOLO cuerpos que parieron: tasa AGREGADA de fecundidad DESPUES del primer parto
    # (offspring extra por paso de vida restante, sumado sobre todos los cuerpos que parieron -- NO la media
    # de vida_med de la poblacion, que mezcla los q0 de vida corta y sesgaria la tasa hacia arriba).
    edad1_total = sum(vt['edades1']) if vt['edades1'] else 0.0
    tiempo_post_total = sum(p[1] for p in vt['post']) if vt['post'] else 0.0
    extra_total = sum(p[0] for p in vt['post']) if vt['post'] else 0.0
    tasa_post = (extra_total / tiempo_post_total) if tiempo_post_total > 0 else None
    o.update(
        f_bad_medido=round(f_mala, 4), f_por_tipo=f, bites_por_tipo=bites, pasos_muro=pasos,
        f_pred_analitico=f_pred, f_bad_pred=round(f_pred['B'] + f_pred['D'], 4),
        pre_death_bad_media=round(med(pdb), 4) if pdb else None, n_muertes_con_ventana=len(pdb),
        causa_energia=causas.count('energia'), causa_agua=causas.count('agua'),
        q0=vt['q0'], n_cuerpos_vt=vt['n'], frac_q0=round(vt['q0'] / vt['n'], 4) if vt['n'] else None,
        edad1_media=round(med(vt['edades1']), 2) if vt['edades1'] else None,
        edad1_total=round(edad1_total, 2), n_repro=len(vt['edades1']),
        tiempo_post_total=round(tiempo_post_total, 2), extra_total=extra_total,
        tasa_post_parto=round(tasa_post, 6) if tasa_post is not None else None,
        R0_reconstruido=round(R0_vt, 4) if R0_vt is not None else None,
        fecund_post_media=round(med([p[0] for p in vt['post']]), 4) if vt['post'] else None,
        truncado_t_desc=vt['truncado'],
    )
    return o


# ------------------------------------------------------------------ humo (UN proceso, 3 corridas cortas)
def humo():
    os.makedirs(HUMO, exist_ok=True)
    sel = sello(); pre = 'diagmuro_humo'
    LOG[0] = open(os.path.join(HUMO, f"{pre}_{sel}.log"), 'w', encoding='utf-8')
    t0 = time.time()
    log(f"HUMO DIAGNOSTICO MURO · {time.strftime('%Y-%m-%d %H:%M:%S')} · UN proceso, sin Pool · T=5000, semilla 1")
    log(f"  organismo_f9c_muro.py sha {h16(os.path.join(AQUI,'organismo_f9c_muro.py'))} · "
        f"origen organismo_f9c.py sha {h16(os.path.join(N09B2,'organismo_f9c.py'))} (se espera 9dd1fb91ecec35ae)")
    log("\nETAPA 1/3 — regla 14 (BRAZOS = corre_bloque2.BRAZOS, mismo objeto)")
    regla14()
    log("\nETAPA 2/3 — arnes de identidad (identidad_muro.py), ANTES de mirar ningun numero")
    ok_id = (IDM.main() == 0)
    log(f"  identidad_muro: {'PASA' if ok_id else 'FALLA'}")
    if not ok_id:
        raise SystemExit("IDENTIDAD FALLA: el humo NO sigue.")
    log("\nETAPA 3/3 — 3 corridas cortas (NADA, REL, ORACULO; T=5000; semilla 1)")
    R = []
    for b in BRAZOS_DIAG:
        r = F9M.run(1, T=5000, **dict(B2.BRAZOS[b], rep_acum=0))
        a = analiza_uno(b, 1, r)
        R.append(a)
        log(f"  [{time.time()-t0:6.1f}s] {b:8s} s1  R0 {a['R0']} vida {a['vida_med']} f_bad_medido "
            f"{a['f_bad_medido']} f_bad_pred {a['f_bad_pred']} pres {a['f_por_tipo']} bites {a['bites_por_tipo']} "
            f"muertes {a['muertes']} q0 {a['q0']}/{a['n_cuerpos_vt']}")
    ruta = os.path.join(HUMO, f"{pre}_{sel}.json")
    json.dump(dict(bloque='diagnostico_muro_humo', sello=sel, T=5000, semillas=[1],
                   sha_muro=h16(os.path.join(AQUI, 'organismo_f9c_muro.py')),
                   sha_origen=h16(os.path.join(N09B2, 'organismo_f9c.py')),
                   sha_runner=h16(os.path.abspath(__file__)), identidad_ok=ok_id, corridas=R,
                   seg=round(time.time() - t0, 1)),
              open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\nJSON {ruta} (sha {h16(ruta)})")
    log(f"HUMO terminado en {time.time()-t0:.1f}s")
    return 0


# ------------------------------------------------------------------ la serie (proceso UNICO, en serie)
def serie():
    os.makedirs(HUMO, exist_ok=True)
    sel = sello(); pre = 'diagmuro_s2941-2946'
    LOG[0] = open(os.path.join(HUMO, f"{pre}_{sel}.log"), 'w', encoding='utf-8')
    t0 = time.time()
    log(f"DIAGNOSTICO DEL MURO · {time.strftime('%Y-%m-%d %H:%M:%S')} · semillas {SEMILLAS} · T={T} · "
        f"{len(BRAZOS_DIAG)} brazos x {len(SEMILLAS)} semillas = {len(BRAZOS_DIAG)*len(SEMILLAS)} corridas, "
        f"UN proceso, SIN Pool")
    log(f"  organismo_f9c_muro.py sha {h16(os.path.join(AQUI,'organismo_f9c_muro.py'))} · "
        f"origen organismo_f9c.py sha {h16(os.path.join(N09B2,'organismo_f9c.py'))} (se espera 9dd1fb91ecec35ae) · "
        f"runner sha {h16(os.path.abspath(__file__))}")
    log("\nETAPA 1/3 — regla 14 (BRAZOS = corre_bloque2.BRAZOS, mismo objeto)")
    regla14()
    log("\nETAPA 2/3 — arnes de identidad (identidad_muro.py), ANTES de mirar ningun numero")
    ok_id = (IDM.main() == 0)
    log(f"  identidad_muro: {'PASA' if ok_id else 'FALLA'}")
    if not ok_id:
        raise SystemExit("IDENTIDAD FALLA: la serie NO se corre.")
    log(f"\nETAPA 3/3 — {len(BRAZOS_DIAG)*len(SEMILLAS)} corridas en SERIE (dentro de este proceso, sin Pool)")
    R = []
    i = 0
    for brazo in BRAZOS_DIAG:
        for seed in SEMILLAS:
            i += 1
            r = F9M.run(seed, T=T, **dict(B2.BRAZOS[brazo], rep_acum=0))
            a = analiza_uno(brazo, seed, r)
            R.append(a)
            log(f"  [{time.time()-t0:6.1f}s] {i:2d}/{len(BRAZOS_DIAG)*len(SEMILLAS)}  {brazo:8s} s{seed}  "
                f"R0 {a['R0']:<7} vida {a['vida_med']:<8} f_bad_medido {a['f_bad_medido']:<7} "
                f"f_bad_pred {a['f_bad_pred']:<7} p1 {a['p1']} c1 {a['c1']} q0 {a['q0']}/{a['n_cuerpos_vt']} "
                f"edad1 {a['edad1_media']} R0_vt {a['R0_reconstruido']}")
    crudo = os.path.join(HUMO, f"{pre}_{sel}.json")
    json.dump(dict(bloque='diagnostico_muro', sello=sel, semillas=SEMILLAS, T=T, brazos=BRAZOS_DIAG,
                   sha_muro=h16(os.path.join(AQUI, 'organismo_f9c_muro.py')),
                   sha_origen=h16(os.path.join(N09B2, 'organismo_f9c.py')),
                   sha_runner=h16(os.path.abspath(__file__)), sha_prereg=h16(os.path.join(AQUI, 'PREREGISTRO_diag_muro.md')),
                   identidad_ok=ok_id, ventana=W_VENTANA, corridas=R, seg=round(time.time() - t0, 1)),
              open(crudo, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\nCRUDO {crudo} (sha {h16(crudo)})")
    log(f"\nTerminado en {time.time()-t0:.1f}s")
    return 0, R, crudo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    a = ap.parse_args()
    if a.humo:
        return humo()
    codigo, R, crudo = serie()
    return codigo


if __name__ == '__main__':
    sys.exit(main())
