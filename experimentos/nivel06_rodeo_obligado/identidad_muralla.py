"""Arnes de identidad BIT A BIT de mundo_muralla.py contra su origen mundo_2d.py (24da4ab1644eb92a).

Regla 2 de EQUIPO.md: con las perillas nuevas APAGADAS (camino=0, placebo=0, prueba sin modo 'muralla')
mundo_muralla.run debe devolver EXACTAMENTE lo mismo que mundo_2d.run, todas las claves, para:
  A) el ANILLO del tronco (alto=1, sin mapa)            -> el organismo v13 exacto
  B) el ANILLO con mapa (r_vis, sitios, usa_M=True)     -> mundo_mapa exacto
  C) la REJILLA con prueba modo='2d'                    -> el bloque nivel6_2d exacto
  D) el ANILLO con prueba modo='rodeo'                  -> el bloque nivel6_rodeo exacto
Y los CONTROLES, que DEBEN DIFERIR (si alguno sale igual, la perilla no esta conectada y el arnes falla):
  E) camino=1 con mapa (la lectura de M cambia)
  F) placebo=3 dentro de un episodio de muralla (misma ley, otra trayectoria)
  G) modo='muralla' con camino=1 contra camino=0 (el mundo nuevo distingue las dos lecturas)

Uso: python experimentos/nivel06_rodeo_obligado/identidad_muralla.py
"""
import hashlib, json, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))          # ERR-28: organismo/ SIEMPRE primero
sys.path.insert(1, os.path.join(RAIZ, 'experimentos', 'nivel6_2d'))
sys.path.insert(2, AQUI)

import mundo_2d as VIEJO                                      # noqa: E402
import mundo_muralla as NUEVO                                 # noqa: E402

SHA_ORIGEN = '24da4ab1644eb92a'
SEEDS = (1701, 1702, 1703)
T = 6000

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


CASOS = []
for s in SEEDS:
    CASOS.append(('A anillo v13 (sin mapa)', s, dict(T=T)))
    CASOS.append(('B anillo con mapa', s, dict(T=T, r_vis=3, sitios=('A', 'B'), usa_M=True)))
    CASOS.append(('C rejilla modo=2d', s, dict(T=T, ancho=17, alto=13, r_vis=3, sitios=M2D['sitios'], regen=50, usa_M=True,
                                               prueba=dict(modo='2d', xy=M2D['xy'], casos=M2D['casos'],
                                                           n_tel=8, max_pasos=60, E_test=0.3))))
    CASOS.append(('D anillo modo=rodeo', s, dict(T=T, r_vis=3, sitios=('A', 'B', 'A'), usa_M=True,
                                                 prueba=dict(modo='rodeo', g1=5, g2=20, n_tel=8, max_pasos=60, E_test=0.3))))

MUR = dict(T=T, ancho=11, alto=9, r_vis=2, sitios=('B',), regen=50, usa_M=True,
           prueba=dict(modo='muralla', n_tel=8, max_pasos=60, E_test=0.3, d_ini=3))

if __name__ == '__main__':
    print(f"origen mundo_2d.py sha {h16(os.path.join(RAIZ, 'experimentos', 'nivel6_2d', 'mundo_2d.py'))} (esperado {SHA_ORIGEN})")
    print(f"copia  mundo_muralla.py sha {h16(os.path.join(AQUI, 'mundo_muralla.py'))}")
    ok = tot = 0
    for et, s, kw in CASOS:
        a = sello(VIEJO.run(s, **kw)); b = sello(NUEVO.run(s, **kw))
        tot += 1; ok += int(a == b)
        print(f"  [{'OK ' if a == b else 'DIF'}] IDENT  {et:26s} seed {s}  {a}  {b}")
    # controles: DEBEN DIFERIR
    for s in SEEDS:
        kw = dict(T=T, r_vis=3, sitios=('A', 'B'), usa_M=True)
        a = sello(NUEVO.run(s, **kw)); b = sello(NUEVO.run(s, camino=1, **kw))
        tot += 1; ok += int(a != b)
        print(f"  [{'OK ' if a != b else 'DIF'}] CONTROL E camino=1 difiere    seed {s}  {a}  {b}")
        a = sello(NUEVO.run(s, camino=1, **MUR)); b = sello(NUEVO.run(s, camino=1, placebo=3, **MUR))
        tot += 1; ok += int(a != b)
        print(f"  [{'OK ' if a != b else 'DIF'}] CONTROL F placebo=3 difiere   seed {s}  {a}  {b}")
        a = sello(NUEVO.run(s, camino=0, **MUR)); b = sello(NUEVO.run(s, camino=1, **MUR))
        tot += 1; ok += int(a != b)
        print(f"  [{'OK ' if a != b else 'DIF'}] CONTROL G muralla H1 vs CAM   seed {s}  {a}  {b}")
    print(f"IDENTIDAD {ok}/{tot}")
    sys.exit(0 if ok == tot else 1)
