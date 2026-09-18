"""Replica del bloque B-5 (desambiguar codigos) en SEMILLAS NUEVAS (regla 12: C4 quedo a una semilla del umbral en la serie 1).

Enmienda 1 del PREREGISTRO_codigo.md (coordinador, 18 sep 09:12), escrita ANTES de correr:
  - Mismos brazos, mismos kwargs, mismos umbrales C1-C9 (la LETRA de corre_codigo.py: se reutilizan sus funciones tal cual).
  - Semillas nuevas elegidas ESTRUCTURALMENTE antes de correr con diagnostico_codigos.py --desde 701 --n 400 --alias 3:
      ALIAS   (|code(D) & code(B)| = 3): las 9 primeras del rango 701-1100 -> 779, 796, 822, 852, 895, 916, 917, 926, 944
      LIMPIAS (|code(D) & code(B)| = 0): las 9 primeras del rango 701-1100 -> 703, 712, 717, 725, 728, 744, 746, 751, 764
  - T1/T2 (tronco) NO se repiten: la serie 1 mostro identidad exacta con v14.1 (6/6 etapas de splits; 40/40 filas): inercia por construccion.
  - La guarda G (identidad con el JSON del bloque de la sal) no aplica a semillas nuevas; en su lugar G' (precondicion, de S1 del bloque
    de la sal): D0-ALIAS |W[sal]| > 0.3 en >= 8/9 y D0-LIMPIA |W[sal]| <= 0.3 en 9/9. Si G' no se cumple, las semillas no reproducen
    el alias y la replica no interpreta C1-C9.
  - Veredicto de la replica: PASA si G' y C1, C2, C3, C5, C6, C7, C8, C9 pasan; C4 se reporta con su letra (9/9 y >= 8/9).
Uso: python experimentos/creacion_B/corre_codigo_replica.py   (un solo Pool; ningun otro Pool vivo)
"""
import os, sys, json, time, platform
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))   # ERR-28: organismo/ primero
sys.path.insert(1, AQUI)
import corre_codigo as m

ALIAS_R = [779, 796, 822, 852, 895, 916, 917, 926, 944]
LIMPIAS_R = [703, 712, 717, 725, 728, 744, 746, 751, 764]


def brazos_replica():
    b = {}
    for nombre, (kw, seeds) in m.BRAZOS.items():
        b[nombre] = (kw, ALIAS_R if seeds is m.ALIAS else LIMPIAS_R)
    return b


def guarda_estructural():
    ok_a = all(m.DC.solapamientos(s)['D&B'] >= 3 for s in ALIAS_R)
    ok_l = all(m.DC.solapamientos(s)['D&B'] == 0 for s in LIMPIAS_R)
    a = [s for s in range(701, 1101) if m.DC.solapamientos(s)['D&B'] >= 3][:9]
    l = [s for s in range(701, 1101) if m.DC.solapamientos(s)['D&B'] == 0][:9]
    m.log(f"    ALIAS |D&B|>=3: {'9/9' if ok_a else '*** no'}; LIMPIAS |D&B|=0: {'9/9' if ok_l else '*** no'}; "
          f"primeras 9 del rango 701-1100 recalculadas: ALIAS {a} {'coinciden' if a == ALIAS_R else '*** NO COINCIDEN'}, "
          f"LIMPIAS {l} {'coinciden' if l == LIMPIAS_R else '*** NO COINCIDEN'}")
    return ok_a and ok_l and a == ALIAS_R and l == LIMPIAS_R


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    T = m.T
    if '--T' in sys.argv:
        T = int(sys.argv[sys.argv.index('--T') + 1])
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'codigo_replica_alias{len(ALIAS_R)}_{stamp}'
    m._log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    BR = brazos_replica()
    m.log(f"ARRANQUE B-5 REPLICA (regla 12; enmienda 1): brazos {list(BR)}, ALIAS {ALIAS_R}, LIMPIAS {LIMPIAS_R}, T={T}.")
    for k, v in m.SHAS().items():
        m.log(f"    sha {k:26s} {v}")
    m.log(f"    sha corre_codigo_replica    {m.h16(os.path.abspath(__file__))}")
    if not guarda_estructural():
        m.log("*** La seleccion estructural de semillas no se reproduce. Se para."); sys.exit(1)
    m.log(f"ETAPA 1/2 — mundo vivo: {sum(len(v[1]) for v in BR.values())} corridas de {T} pasos ({len(BR)} brazos). Pool({m.N_PARALELO}) aqui. T1/T2 no se repiten (inercia exacta en la serie 1).")
    res = []
    with mp.Pool(m.N_PARALELO) as pool:
        tr = [('R', b, s, T) for b, (_, ss) in BR.items() for s in ss]
        for i, r in enumerate(pool.imap_unordered(m.tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 9 == 0 or i == len(tr):
                m.log(f"          {i}/{len(tr)}")
    m.log()
    m.log("ETAPA 2/2 — umbrales EXACTOS de PREREGISTRO_codigo.md (ERR-31) con las funciones de corre_codigo.py; G' en vez de G.")
    m.REF_SAL = ''   # G no aplica a semillas nuevas
    V = m.veredicto(res)
    A0 = [r for r in res if r['brazo'] == 'D0-ALIAS']; L0 = [r for r in res if r['brazo'] == 'D0-LIMPIA']
    ga = sum(r['w_sal'] > 0.3 for r in A0); gl = sum(r['w_sal'] <= 0.3 for r in L0)
    V['Gp'] = dict(alias_muestra=ga, limpias_sin=gl, pasa=bool(ga >= 8 and gl == 9))
    m.log(f"   G' D0-ALIAS |W[sal]| > 0.3 en >= 8/9 y D0-LIMPIA |W[sal]| <= 0.3 en 9/9  -> {ga}/9 y {gl}/9  {'PASA' if V['Gp']['pasa'] else 'NO'}")
    nucleo = ['C1', 'C2', 'C3', 'C5', 'C6', 'C7', 'C8', 'C9']
    pasa = V['Gp']['pasa'] and all((V.get(c) or {}).get('pasa') for c in nucleo)
    c4 = (V.get('C4') or {})
    ver = (f"REPLICA {'PASA' if pasa else 'NO PASA'}: G' {'ok' if V['Gp']['pasa'] else 'no'}; "
           + ', '.join(f"{c} {'ok' if (V.get(c) or {}).get('pasa') else 'NO'}" for c in nucleo)
           + f"; C4 (causa) {c4.get('n1')}/9 y {c4.get('n2')}/9 -> {'ok' if c4.get('pasa') else 'NO'}")
    m.log(); m.log(f"VEREDICTO: {ver}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), T=T, alias=ALIAS_R, limpias=LIMPIAS_R, replica_de='codigo_alias9_20260918_085958',
                brazos={b: {k: (list(v) if isinstance(v, tuple) else v) for k, v in kw.items()} for b, (kw, _) in BR.items()},
                veredicto=ver, veredictos=V, shas=dict(m.SHAS(), corre_codigo_replica=m.h16(os.path.abspath(__file__))),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta, principal=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    m.log(f"datos -> {os.path.basename(dj)}  sha256_16 = {m.h16(dj)}")
    m._log['f'].close()
