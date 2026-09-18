"""Mini-prueba de UN PROCESO del bloque 2D (regla 3 de registro/EQUIPO.md: sin Pool, <= 6 corridas).
No declara nada: solo dice si el diseno es MEDIBLE (los sitios se recuerdan, el valor se aprende, el teletransporte
cae ciego, y el primer paso se reparte como predice el mecanismo).

Mundos (rejilla 17x13, r_vis=3, sitios fijos con regeneracion; coordenadas relativas a un origen azaroso por semilla,
y reflejadas en las semillas pares):
  M1 barrera   F1 comida (0,0); veneno (2,-2),(2,-1),(2,0),(2,1)          -> T1 rodeo VERDADERO   S=(6,0)
  M2 sombra    F1 comida (0,0); veneno (2,0),(3,0); F2 comida (-4,-4)     -> T4 rodeo FALSO       S=(-4,0)
  M3 flanco    F1 comida (4,0); veneno (1,6) [el del flanco] + (0,5),(0,-5) [dieta: dx=0, no tocan +x/-x]
                                                                          -> T2 horizonte 2       S=(0,0)
  M4 secuencia F1 comida (0,0); F2 comida (0,6); veneno (-4,4)            -> T3 secuencia A->B    S=(-4,0)
Acciones: 0=-x (izq), 1=+x (der), 2=-y (arriba), 3=+y (abajo).

Uso: python experimentos/nivel6_2d/mini_2d.py [--mundo M1] [--T 50000] [--semillas 3] [--brazos MAPA,SINMAPA]
"""
import sys, os, json, time, datetime

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI]
import mundo_2d as m2

ANCHO, ALTO, R_VIS = 17, 13, 3
NOM = {0: '-x', 1: '+x', 2: '-y', 3: '+y'}

MUNDOS = {
    'M1': dict(sitios=('A', 'B', 'B', 'B', 'B'), xy=((0, 0), (2, -2), (2, -1), (2, 0), (2, 1)),
               casos=({'et': 'rodeo', 'S': (6, 0), 'ok': (0, 3)},), max_pasos=60),
    'M2': dict(sitios=('A', 'B', 'B', 'A'), xy=((0, 0), (2, 0), (3, 0), (-4, -4)),
               casos=({'et': 'falso', 'S': (-4, 0), 'ok': (1,)},), max_pasos=60),
    'M3': dict(sitios=('A', 'B', 'B', 'B'), xy=((4, 0), (1, 6), (0, 5), (0, -5)),
               casos=({'et': 'h2', 'S': (0, 0), 'ok': (1,)},), max_pasos=60),
    'M4': dict(sitios=('A', 'A', 'B'), xy=((0, 0), (0, 6), (-4, 4)),
               casos=({'et': 'sec', 'S': (-4, 0), 'ok': (1,), 'consume': True},), max_pasos=80),
}
BRAZOS = {  # perillas de cada brazo (sobre el mundo elegido)
    'MAPA':      dict(usa_M=True),
    'MAPA_h2':   dict(usa_M=True, _p=dict(h2=True)),
    'MAPA_borra': dict(usa_M=True, _p=dict(borra_M=True)),
    'SINMAPA':   dict(usa_M=False),
    'CONGELADA': dict(usa_M=True, escribe_M=False),
    'INVERTIDO': dict(usa_M=True, _p=dict(invertir=True)),
}


def corre(mundo, brazo, seed, T, n_tel=40):
    mu = MUNDOS[mundo]; br = dict(BRAZOS[brazo]); pex = br.pop('_p', {})
    prueba = dict(modo='2d', xy=mu['xy'], casos=mu['casos'], n_tel=n_tel,
                  max_pasos=mu['max_pasos'], E_test=0.3, **pex)
    return m2.run(seed, T=T, ancho=ANCHO, alto=ALTO, r_vis=R_VIS, sitios=mu['sitios'],
                  regen=50, prueba=prueba, **br)


if __name__ == '__main__':
    arg = lambda k, d: (sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d)
    MUNDO = arg('--mundo', 'M1'); T = int(arg('--T', 50000)); NS = int(arg('--semillas', 3))
    brazos = arg('--brazos', 'MAPA,SINMAPA').split(',')
    NT = int(arg('--n_tel', 40))
    print(f"mini 2D  mundo={MUNDO}  rejilla {ANCHO}x{ALTO}  T={T}  semillas 1..{NS}  brazos={brazos}  "
          f"({datetime.datetime.now():%H:%M:%S})", flush=True)
    res = {}
    for br in brazos:
        for s in range(1, NS + 1):
            t0 = time.time(); r = corre(MUNDO, br, s, T, NT); dt = time.time() - t0
            te = r['tel']; cs = te['casos']
            rep = {NOM[a]: round(sum(c['primer'] == a for c in cs) / len(cs), 3) for a in range(4)}
            mec = {NOM[a]: round(sum(c['mec1'] == a for c in cs if c['mec1'] is not None) / len(cs), 3) for a in range(4)}
            et = sorted(te['R'])[0]
            res[(br, s)] = dict(R=te['R'][et], llega=te['llega'][et], limpio=te['llega_limpio'][et],
                                pisa=te['pisa'][et], come2=te['come2'][et], sigue=te['sigue_mec1'][et],
                                vA=te['v_A'], vB=te['v_B'], M=r['M_llenas'], muertes=r['deaths'],
                                W=r['W'], ciego=te['ciego_al_llegar'], quieto=te['sin_mover'], rep=rep, mec=mec,
                                B1=cs[0]['B1'], B2=cs[0]['B2'], orient=te['orientacion'], seg=round(dt, 1))
            x = res[(br, s)]
            print(f"  {br:10s} s{s}  {dt:5.1f}s  R={x['R']}  llega={x['llega']} limpio={x['limpio']} pisa={x['pisa']} "
                  f"come2={x['come2']}  sigue_mec={x['sigue']}  v_A={x['vA']} v_B={x['vB']}  M={x['M']}/{len(MUNDOS[MUNDO]['xy'])} "
                  f"muertes={x['muertes']} ciego={x['ciego']}/{NT} quieto={x['quieto']}", flush=True)
            print(f"             primer paso {rep}   mecanismo(argmax B1) {mec}   B1(ep0)={x['B1']}", flush=True)
    for br in brazos:
        vs = [res[(br, s)]['R'] for s in range(1, NS + 1) if res[(br, s)]['R'] is not None]
        print(f"  == {br:10s} R mediana {sorted(vs)[len(vs)//2] if vs else None}  ({vs})", flush=True)
    d = os.path.join(AQUI, f'mini_{MUNDO}.json')
    json.dump({f"{k[0]}_s{k[1]}": v for k, v in res.items()}, open(d, 'w'), indent=1)
    print(f"  -> {os.path.relpath(d, RAIZ)}", flush=True)
