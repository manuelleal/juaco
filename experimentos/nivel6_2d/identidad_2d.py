"""Arnes de identidad de mundo_2d.py (el ANCLA del nivel 6 en 2D).

Con alto=1 (una sola fila, toroidal) el mundo 2D tiene que ser BIT A BIT el mundo del anillo, en todas las claves de
salida y con el mismo consumo del generador aleatorio:
  REJILLA 1 (mapa on/off)  mundo_2d.run(seed, **kw)                    == mundo_mapa.run(seed, **kw)
  REJILLA 2 (rodeo)        mundo_2d.run(seed, prueba=dict(modo='rodeo')) == mundo_mapa_rodeo.run(seed, ...)
  REJILLA 3 (tronco)       mundo_2d.run(seed) con las perillas apagadas == organismo_v13.run(seed) en las claves de v13
                           (v13 no trae 'tel' ni 'M_llenas'; se comprueba aparte que valgan None y 0)
Compara los diccionarios completos tras ida y vuelta por JSON (como identidad_mapa_rapido.py), no una metrica resumen.
UN SOLO PROCESO, sin Pool (regla 3 de registro/EQUIPO.md). T corto por defecto (20000).

Uso: python experimentos/nivel6_2d/identidad_2d.py [--T 20000] [--semillas 3]
"""
import sys, os, json, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI,
                os.path.join(RAIZ, 'experimentos', 'nivel6_mapa'),
                os.path.join(RAIZ, 'experimentos', 'nivel6_rodeo'),
                os.path.join(RAIZ, 'organismo')]
import mundo_2d as dos
import mundo_mapa as mapa
import mundo_mapa_rodeo as rodeo
import organismo_v13 as v13

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 20000
NS = int(sys.argv[sys.argv.index('--semillas') + 1]) if '--semillas' in sys.argv else 3
SEEDS = list(range(1, NS + 1))
N = lambda x: json.loads(json.dumps(x, default=str))

MUNDO = dict(r_vis=3, sitios=('A', 'B'))
PRUEBA = dict(n_tel=40, E_test=0.3, max_pasos=30)
ROD = dict(r_vis=3, sitios=('A', 'B', 'A'), usa_M=True)
PROD = dict(modo='rodeo', n_tel=40, E_test=0.3, max_pasos=60, g1=5, g2=20)

# REJILLA 1: contra mundo_mapa (mapa ENCENDIDO y APAGADO, mas los caminos que no tocan los brazos)
G1 = {
    'apagadas':        dict(),                                                    # = organismo_v13
    'apagadas_invert': dict(invertir_en=T // 2),
    'MAPA':            dict(MUNDO, usa_M=True, prueba=dict(PRUEBA)),              # mapa ON
    'SINMAPA':         dict(MUNDO, usa_M=False, prueba=dict(PRUEBA)),             # mapa OFF, mismo mundo
    'CONGELADA':       dict(MUNDO, usa_M=True, escribe_M=False, prueba=dict(PRUEBA)),
    'BARAJADO':        dict(MUNDO, usa_M=True, prueba=dict(PRUEBA, barajar=True)),
    'INVERTIDO':       dict(MUNDO, usa_M=True, prueba=dict(PRUEBA, invertir=True)),
    'M_sin_sitios':    dict(r_vis=3, usa_M=True, nobj=6),                         # M con MUCHAS celdas: exige el mismo ORDEN DE SUMA
    'M_perillas':      dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), H_M=7, disc_M=0.75, gamma_M=1.3, regen=17),
    'M_splits':        dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), solap_AB=1),  # divisiones vivas con la tabla M
    'solo_rvis':       dict(r_vis=1),                                             # vista limitada, sin mapa ni sitios
}
# REJILLA 2: contra mundo_mapa_rodeo (la prueba del rodeo, que es 1D por construccion)
G2 = {
    'RODEO':     dict(ROD, prueba=dict(PROD)),
    'RODEO_inv': dict(ROD, prueba=dict(PROD, invertir=True)),
    'RODEO_g':   dict(ROD, prueba=dict(PROD, g1=4, g2=18, dps=(4, 6), aas=(5, 7))),
}
# REJILLA 3: contra el tronco v13 (claves de v13; 'tel' y 'M_llenas' se comprueban aparte)
G3 = {
    'v13_base':   dict(),
    'v13_nuevo':  dict(nuevo='C', nuevo_en=T // 3),
    'v13_v11':    dict(eta_s=0.0, puerta=None),
}


def rejilla(titulo, configs, ref, solo_claves_de_ref=False):
    fallos = []; n = 0
    print(f"--- {titulo} ({len(configs)} configuraciones x {len(SEEDS)} semillas, T={T}) ---", flush=True)
    for nombre, kw in configs.items():
        malas = 0
        for s in SEEDS:
            a = ref.run(s, T=T, **kw)
            b = dos.run(s, T=T, **kw)          # alto=1, ancho=None: el anillo
            claves = list(a) if solo_claves_de_ref else sorted(set(a) | set(b))
            dif = [k for k in claves if N(a.get(k)) != N(b.get(k))]
            if solo_claves_de_ref:
                if b.get('tel') is not None or b.get('M_llenas') != 0: dif.append('extra(tel/M_llenas)')
            n += 1
            if dif:
                malas += 1; fallos.append((nombre, s, dif))
                print(f"  DIFIERE {nombre} s{s}: {dif[:6]}", flush=True)
        print(f"  {nombre:16s} {len(SEEDS) - malas}/{len(SEEDS)} identicas", flush=True)
    return n, len(fallos)


if __name__ == '__main__':
    t0 = time.time(); tot = mal = 0
    for tit, cfg, ref, solo in [('REJILLA 1  mundo_2d(alto=1) == mundo_mapa', G1, mapa, False),
                                ('REJILLA 2  mundo_2d(alto=1,modo=rodeo) == mundo_mapa_rodeo', G2, rodeo, False),
                                ('REJILLA 3  mundo_2d(perillas apagadas) == organismo_v13', G3, v13, True)]:
        a, b = rejilla(tit, cfg, ref, solo); tot += a; mal += b
    print(f"=> IDENTIDAD {tot - mal}/{tot} corridas identicas   ({time.time() - t0:.0f} s, un proceso)", flush=True)
    sys.exit(1 if mal else 0)
