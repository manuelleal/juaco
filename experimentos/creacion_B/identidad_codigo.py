"""CREADOR B — arnes de identidad de B-5 (desambiguar). UN proceso, sin Pool (regla 3 de EQUIPO.md).

I1  organismo_v14_codigo(desambiguar=0) == organismo/organismo_v14.py (TRONCO v14.1) en TODAS las claves de v14:
    12 escenarios x 2 semillas (T = 30000 por defecto).
I2  el rng NO se consume con la perilla apagada: T = 120000, 2 semillas (un numero de mas y todo diverge).
I3  organismo_v14g_codigo(desambiguar=0) == organismo/organismo_v14g.py (mundo de regla): 3 reglas x 2 semillas.
I4  organismo_vivo_codigo(desambiguar=0) == experimentos/nivel11_mundo_vivo/organismo_vivo.py: 5 montajes x 2 semillas
    (apagado; V14 = 1 necesidad y 2 estimulos; SIN-SED = 1 necesidad y 4 estimulos; NO_INFORMA; VIVO informativo).
I5  PREDICCION (no exigencia): con la perilla ENCENDIDA el tronco es INERTE POR CONSTRUCCION donde R nunca es 0:
    organismo_v14_codigo(desambiguar=1) == organismo_v14 en los 12 escenarios, y v14g_codigo(1) == v14g en las 3 reglas.
    Si esto falla, R == 0 ocurre donde no lo esperaba y la prediccion T1/T2 del preregistro cambia de naturaleza.
I6  CONTROL QUE DEBE FALLAR (no vacuidad): en el mundo vivo NO_INFORMA con la semilla ALIAS 326 (sal y veneno con el
    mismo codigo), desambiguar=1 != desambiguar=0 y des_splits >= 1 (T = 40000).
Uso: python experimentos/creacion_B/identidad_codigo.py [T]
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
NIV11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI, NIV11]   # organismo/ PRIMERO (ERR-28)

import organismo_v14 as V14
import organismo_v14_codigo as V14C
import organismo_v14g as V14G
import organismo_v14g_codigo as V14GC
import organismo_vivo as VV
import organismo_vivo_codigo as VVC

NUEV = {'desambiguar', 'des_splits', 'des_t'}   # claves nuevas de solo lectura (siempre presentes)

ESC = [('AB por defecto', dict()), ('AB invertido', dict(invertir_en=15000)),
       ('AB + patron nuevo C', dict(nuevo='C', nuevo_en=15000)), ('AB solap_AB=3 (E2L)', dict(solap_AB=3)),
       ('AB sin plasticidad', dict(plast=False)), ('AB via lenta apagada', dict(eta_s=0.0)),
       ('AB sin puerta', dict(puerta=None)), ('AB sin division por signo', dict(div_signo=False)),
       ('AB sin hija dispersa', dict(mask_rel=0)), ('AB sin puerta por codigo', dict(puerta_pat=0)),
       ('AB las dos perillas v14 off', dict(mask_rel=0, puerta_pat=0)),
       ('AB D comida solap_B=2 (E2K)', dict(nuevo='D', nuevo_val='comida', solap_B=2, nuevo_en=15000))]
ESCG = [('regla/px0', dict(mundo='regla', regla='px0', eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, puerta_pat=5, pat_min=1)),
        ('regla/xor01', dict(mundo='regla', regla='xor01', eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, puerta_pat=5, pat_min=1)),
        ('regla/azar', dict(mundo='regla', regla='azar', eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, puerta_pat=5, pat_min=1))]
SAL_MUDA = {'comida': (+0.8, 0.0), 'veneno': (-0.4, 0.0), 'agua': (0.0, +0.8), 'sal': (0.0, 0.0)}
CUERPO = dict(vivo=1, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001)
ESCV = [('vivo=0 (apagado)', dict(vivo=0, n_nec=1)),
        ('V14: 1 necesidad, 2 estimulos', dict(vivo=1, n_nec=1, estims=('A', 'B'), costo_a=0.0, A_ini=1.0)),
        ('SIN-SED: 1 necesidad, 4 estimulos, sal muda', dict(CUERPO, n_nec=1, tabla=SAL_MUDA)),
        ('NO_INFORMA: 2 necesidades, sal muda', dict(CUERPO, n_nec=2, tabla=SAL_MUDA)),
        ('VIVO: 2 necesidades, sal informa', dict(CUERPO, n_nec=2))]


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def comp(a, b):
    """claves de `a` (el original) que difieren o faltan en `b` (la copia); claves nuevas de la copia fuera de NUEV."""
    return ([k for k in a if k in b and N(a[k]) != N(b[k])] + [k for k in a if k not in b]
            + [k for k in b if k not in a and k not in NUEV])


if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    t0 = time.time()
    for nom, p in [('organismo_v14 (TRONCO)', os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
                   ('organismo_v14g', os.path.join(RAIZ, 'organismo', 'organismo_v14g.py')),
                   ('organismo_vivo (nivel 11)', os.path.join(NIV11, 'organismo_vivo.py')),
                   ('organismo_v14_codigo', os.path.join(AQUI, 'organismo_v14_codigo.py')),
                   ('organismo_v14g_codigo', os.path.join(AQUI, 'organismo_v14g_codigo.py')),
                   ('organismo_vivo_codigo', os.path.join(AQUI, 'organismo_vivo_codigo.py'))]:
        print(f'  sha {nom:28s} {h16(p)}')
    print(f'  modulos: v14 {V14.__file__}\n           vivo {VV.__file__}\n')
    ok = tot = 0
    ok5 = tot5 = 0
    print(f'--- I1: organismo_v14_codigo(desambiguar=0) == organismo_v14 (v14.1), T={T}; I5: con desambiguar=1 (prediccion de inercia) ---')
    for etq, kw in ESC:
        for s in (1, 2):
            tot += 1; tot5 += 1
            a = V14.run(s, T=T, **kw)
            d0 = comp(a, V14C.run(s, T=T, desambiguar=0, **kw)); ok += (not d0)
            d1 = comp(a, V14C.run(s, T=T, desambiguar=1, **kw)); ok5 += (not d1)
            print(f'  [{time.time()-t0:5.0f}s] {etq:>36} s{s}: off {"IDENTICO" if not d0 else "DIFIERE " + str(d0)}'
                  f'   on {"IDENTICO (inerte)" if not d1 else "DIFIERE " + str(d1)}')
    print('\n--- I2: el rng NO se consume con la perilla apagada (T=120000) ---')
    for s in (1, 2):
        tot += 1
        d = comp(V14.run(s, T=120000), V14C.run(s, T=120000, desambiguar=0)); ok += (not d)
        print(f'  [{time.time()-t0:5.0f}s] T=120000 s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}')
    print(f'\n--- I3: organismo_v14g_codigo(0) == organismo_v14g (mundo de regla), T={T}; I5 con (1) ---')
    for etq, kw in ESCG:
        for s in (1, 2):
            tot += 1; tot5 += 1
            a = V14G.run(s, T=T, **kw)
            d0 = comp(a, V14GC.run(s, T=T, desambiguar=0, **kw)); ok += (not d0)
            d1 = comp(a, V14GC.run(s, T=T, desambiguar=1, **kw)); ok5 += (not d1)
            print(f'  [{time.time()-t0:5.0f}s] {etq:>36} s{s}: off {"IDENTICO" if not d0 else "DIFIERE " + str(d0)}'
                  f'   on {"IDENTICO (inerte)" if not d1 else "DIFIERE " + str(d1)}')
    Tv = min(T, 20000)
    print(f'\n--- I4: organismo_vivo_codigo(0) == organismo_vivo (nivel 11), T={Tv} ---')
    for etq, kw in ESCV:
        for s in (1, 2):
            tot += 1
            d = comp(VV.run(s, T=Tv, **kw), VVC.run(s, T=Tv, desambiguar=0, **kw)); ok += (not d)
            print(f'  [{time.time()-t0:5.0f}s] {etq:>44} s{s}: {"IDENTICO" if not d else "DIFIERE " + str(d)}')
    print(f'\nIDENTIDAD exigida (I1+I2+I3+I4): {ok}/{tot}')
    print(f'INERCIA predicha en los mundos del tronco (I5, perilla ON): {ok5}/{tot5}')

    print('\n--- I6: CONTROL QUE DEBE FALLAR (no vacuidad): NO_INFORMA, semilla ALIAS 326, on != off, T=40000 ---')
    kw = dict(CUERPO, n_nec=2, tabla=SAL_MUDA)
    a = VVC.run(326, T=40000, desambiguar=0, **kw); b = VVC.run(326, T=40000, desambiguar=1, **kw)
    d = comp(a, b)
    okc = bool(d) and b['des_splits'] >= 1
    print(f'  [{time.time()-t0:5.0f}s] difieren: {bool(d)} (claves {d[:6]}); des_splits on={b["des_splits"]} off={a["des_splits"]};'
          f' W_nec hambre: off {a["W_nec"][0]}  on {b["W_nec"][0]}')
    print(f'  I6 {"DIFIERE (como debe)" if okc else "FALLA: la perilla no hace nada en la semilla alias"}')
    todo = (ok == tot) and okc
    print(f'\nVEREDICTO identidad_codigo: {"PASA" if todo else "NO PASA"}  ({ok}/{tot} exigidas; I5 {ok5}/{tot5}; I6 {"ok" if okc else "falla"})')
    sys.exit(0 if todo else 1)
