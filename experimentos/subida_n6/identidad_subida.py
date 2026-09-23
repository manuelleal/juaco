"""Arnes de identidad BIT A BIT de mundo_subida.py contra su origen mundo_muralla.py (6e515713c86d8bf4).

Regla 2 de EQUIPO.md: con las perillas nuevas APAGADAS (grad=0, filtro=0, brujula=0) mundo_subida.run debe devolver
EXACTAMENTE lo mismo que mundo_muralla.run, todas las claves, para:
  A) el ANILLO del tronco v13 (alto=1, sin mapa)
  B) el ANILLO con mapa (mundo_mapa)
  C) la REJILLA con prueba modo='2d' (nivel6_2d)
  D) el ANILLO con prueba modo='rodeo' (nivel6_rodeo, el 50 % replicado)
  E) la MURALLA con camino=0 (MAPA), camino=1 (CAMINO), camino=1 + placebo=3, + barajar, + invertir (los brazos del
     bloque rodeo obligado, 21-sep, tal como los pasa corre_muralla.py: r_vis=1, d_ini=5)
Y los CONTROLES, que DEBEN DIFERIR (si alguno sale igual, la perilla no esta conectada y el arnes falla):
  F) grad=1 en muralla (camino=1)       G) filtro=1 en muralla (camino=1)       H) brujula=1 con grad=1 y filtro=1
     contra grad=1 y filtro=1 (el control cambia el campo; en el mundo partido, T=20000)
  I) prueba cierre=5 (segunda muralla entera, alto=11) contra el mundo viejo (el mundo nuevo esta conectado)

Uso: python experimentos/subida_n6/identidad_subida.py   (un proceso; escribe datos/humo/identidad_subida_<sello>.json)
"""
import datetime, hashlib, json, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))          # ERR-28: organismo/ SIEMPRE primero
sys.path.insert(1, os.path.join(RAIZ, 'experimentos', 'nivel06_rodeo_obligado'))
sys.path.insert(2, AQUI)

import mundo_muralla as VIEJO                                 # noqa: E402
import mundo_subida as NUEVO                                  # noqa: E402

SHA_ORIGEN = '6e515713c86d8bf4'
SEEDS = (6642, 6643, 6644)   # semillas del arnes (fuera de la serie 6601-6620, de la replica 6621-6640 y del humo 6641)
T = 6000
T_H = 20000   # control H: el campo necesita una comida con valor>0 (depuracion, PREREGISTRO §9)

M2D = dict(sitios=('A', 'B', 'B', 'B', 'B'), xy=((0, 0), (2, -2), (2, -1), (2, 0), (2, 1)),
           casos=({'et': 'rodeo', 'S': (6, 0), 'ok': (0, 3)},))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def _norm(o):
    if isinstance(o, dict):
        return {str(k): _norm(v) for k, v in sorted(o.items(), key=lambda kv: str(kv[0]))}
    if isinstance(o, (list, tuple)):
        return [_norm(v) for v in o]
    if isinstance(o, float):
        return repr(float(o))
    if hasattr(o, 'tolist'):
        return _norm(o.tolist())
    return o


def sello(r):
    return hashlib.sha256(json.dumps(_norm(r), sort_keys=True).encode()).hexdigest()[:16]


def mur(**pex):
    pr = dict(modo='muralla', n_tel=8, max_pasos=60, E_test=0.3, d_ini=5); pr.update(pex)
    return dict(T=T, ancho=11, alto=9, r_vis=1, sitios=('B',), regen=50, usa_M=True, prueba=pr)


CASOS = []
for s in SEEDS:
    CASOS.append(('A anillo v13 (sin mapa)', s, dict(T=T)))
    CASOS.append(('B anillo con mapa', s, dict(T=T, r_vis=3, sitios=('A', 'B'), usa_M=True)))
    CASOS.append(('C rejilla modo=2d', s, dict(T=T, ancho=17, alto=13, r_vis=3, sitios=M2D['sitios'], regen=50, usa_M=True,
                                               prueba=dict(modo='2d', xy=M2D['xy'], casos=M2D['casos'],
                                                           n_tel=8, max_pasos=60, E_test=0.3))))
    CASOS.append(('D anillo modo=rodeo', s, dict(T=T, r_vis=3, sitios=('A', 'B', 'A'), usa_M=True,
                                                 prueba=dict(modo='rodeo', g1=5, g2=20, n_tel=8, max_pasos=60, E_test=0.3))))
    CASOS.append(('E muralla CIEGO', s, dict(mur(), usa_M=False)))
    CASOS.append(('E muralla MAPA camino=0', s, dict(mur(), camino=0)))
    CASOS.append(('E muralla CAMINO', s, dict(mur(), camino=1)))
    CASOS.append(('E muralla CAMINO placebo=3', s, dict(mur(), camino=1, placebo=3)))
    CASOS.append(('E muralla CAMINO barajar', s, dict(mur(barajar=True), camino=1)))
    CASOS.append(('E muralla CAMINO invertir', s, dict(mur(invertir=True), camino=1)))

if __name__ == '__main__':
    so = h16(os.path.join(RAIZ, 'experimentos', 'nivel06_rodeo_obligado', 'mundo_muralla.py'))
    sn = h16(os.path.join(AQUI, 'mundo_subida.py'))
    print(f"origen mundo_muralla.py sha {so} (esperado {SHA_ORIGEN})")
    print(f"copia  mundo_subida.py  sha {sn}")
    if so != SHA_ORIGEN:
        raise SystemExit('ORIGEN cambiado: abortado')
    filas = []; ok = tot = 0
    for et, s, kw in CASOS:
        a = sello(VIEJO.run(s, **kw)); b = sello(NUEVO.run(s, **kw))
        tot += 1; ok += int(a == b); filas.append(dict(tipo='IDENT', caso=et, seed=s, viejo=a, nuevo=b, ok=a == b))
        print(f"  [{'OK ' if a == b else 'DIF'}] IDENT   {et:30s} seed {s}  {a}  {b}")
    for s in SEEDS:
        a = sello(NUEVO.run(s, camino=1, **mur())); b = sello(NUEVO.run(s, camino=1, **dict(mur(cierre=5), alto=11)))
        tot += 1; ok += int(a != b); filas.append(dict(tipo='CONTROL', caso='I cierre=5 difiere', seed=s, viejo=a, nuevo=b, ok=a != b))
        print(f"  [{'OK ' if a != b else 'DIF'}] CONTROL {'I cierre=5 (mundo partido)':30s} seed {s}  {a}  {b}")
        base = sello(NUEVO.run(s, camino=1, **mur()))
        for et, kw in (('F grad=1 difiere', dict(camino=1, grad=1)),
                       ('G filtro=1 difiere', dict(camino=1, filtro=1))):
            b = sello(NUEVO.run(s, **kw, **mur()))
            tot += 1; ok += int(b != base); filas.append(dict(tipo='CONTROL', caso=et, seed=s, viejo=base, nuevo=b, ok=b != base))
            print(f"  [{'OK ' if b != base else 'DIF'}] CONTROL {et:30s} seed {s}  {base}  {b}")
        PART = dict(mur(cierre=5, d_ini=4), alto=11, T=T_H)   # H en el mundo PARTIDO y con T_H: a T=6000 valor(A) puede seguir <0,
        #                                                       sin fuente positiva el campo no existe y brujula no puede diferir
        a = sello(NUEVO.run(s, camino=1, grad=1, filtro=1, **PART))
        b = sello(NUEVO.run(s, camino=1, grad=1, filtro=1, brujula=1, **PART))
        tot += 1; ok += int(a != b); filas.append(dict(tipo='CONTROL', caso='H brujula=1 difiere', seed=s, viejo=a, nuevo=b, ok=a != b))
        print(f"  [{'OK ' if a != b else 'DIF'}] CONTROL {'H brujula=1 difiere':30s} seed {s}  {a}  {b}")
    print(f"IDENTIDAD {ok}/{tot}")
    dest = os.path.join(AQUI, 'datos', 'humo', 'identidad_subida_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.json')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    json.dump(dict(origen=so, copia=sn, ok=ok, tot=tot, filas=filas), open(dest, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"JSON {os.path.relpath(dest, RAIZ)}  sha {h16(dest)}")
    sys.exit(0 if ok == tot else 1)
