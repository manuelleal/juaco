"""corre_trasp.py — EXPLORATORIO, no es dato. UNA corrida por proceso: 9 carros iguales en la pista de la carrera (motor_cruce == pista
bit a bit), fundador limpio, T 100 000, juez.resumen_linaje (sólo física). El genoma de cableado se pone A MANO (fijo, p_mut 0, sin
banco: los hijos lo copian sin error y el fundador limpio nace con el genotipo del linaje). ENSENA es una perilla del carro TRASP.
MISION: llegar a la AGI por este camino.
    python corre_trasp.py --brazo sac2 --semilla 33001 [--T 100000]
Escribe datos/<brazo>_s<semilla>_T<T>.json. Semillas sólo 33001-33999. Sin Pool. Importa los motores en solo lectura (sin bytecode)."""
import argparse, hashlib, importlib.util, json, os, sys, time

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
ORGANELOS = os.path.normpath(os.path.join(AQUI, '..', '..'))
CRUCE = os.path.join(ORGANELOS, 'cruce')
PISTA = r'C:\Users\User\Documents\PROYECTOS\JUACO\bundle\experimentos\carrera_escuderias'
sys.path[:0] = [CRUCE, PISTA]
import motor_cruce as MC
import juez as J

DATOS = os.path.join(AQUI, 'datos')
NG = 36
_MODS = {}


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def genoma(**kv):
    """genes por nombre (los de CRUCE.NOMBRES_GEN); el resto 0. Sin recorte a [-4, 4]: declarado."""
    nom = list(modulo('TRASP').NOMBRES_GEN)
    g = [0] * NG
    for k, v in kv.items():
        if k not in nom: raise SystemExit(f"gen desconocido {k}")
        g[nom.index(k)] = int(v)
    return g


def suma(*gs):
    return [sum(x) for x in zip(*gs)]


# ------------------------------------------------------------------ BRAZOS (ver PREDICCIONES_previas.md)
def brazos():
    SAC = lambda w: genoma(boca_bueno_reserva=-w, boca_neutro_reserva=-w, boca_malo_reserva=-w)
    MARGEN = genoma(boca_bueno_sesgo=6, boca_bueno_reserva=-12)
    NOMALO = genoma(boca_malo_sesgo=-8)
    LIMPIA = genoma(boca_malo_sesgo=-6, boca_malo_otra=8)
    NEOF = genoma(boca_neutro_sesgo=-6, boca_neutro_reserva=15)
    PATAS = genoma(pata_act_sesgo=2, pata_otra_sesgo=1)
    O1G = suma(MARGEN, LIMPIA, NEOF, PATAS)
    B = {
        'v143': dict(g=[0] * NG, ensena=0),
        'sac2': dict(g=SAC(2), ensena=0),
        'sac6': dict(g=SAC(6), ensena=0),
        'margen': dict(g=MARGEN, ensena=0),
        'nomalo': dict(g=NOMALO, ensena=0),
        'limpia': dict(g=LIMPIA, ensena=0),
        'neofobia': dict(g=NEOF, ensena=0),
        'patas': dict(g=PATAS, ensena=0),
        'o1genes': dict(g=O1G, ensena=0),
        'ensena1': dict(g=[0] * NG, ensena=1),
        'ensena2': dict(g=[0] * NG, ensena=2),
        # segunda ola (se agregan tras leer la primera; ver HALLAZGOS.md)
        'ens2_limpia': dict(g=LIMPIA, ensena=2),
        'ens2_neof': dict(g=NEOF, ensena=2),
        'ens2_patas': dict(g=PATAS, ensena=2),
        'ens2_o1genes': dict(g=O1G, ensena=2),
        'ens2_sac2': dict(g=SAC(2), ensena=2),
        'ens1_o1genes': dict(g=O1G, ensena=1),
        'ens2_limpia_neof': dict(g=suma(LIMPIA, NEOF), ensena=2),
        'ens2_limpia_patas': dict(g=suma(LIMPIA, PATAS), ensena=2),
        # segunda ola REAL (tras leer la ola 1: patas fue la unica pieza con senal; o1genes peor que patas solo)
        'patas4': dict(g=genoma(pata_act_sesgo=4, pata_otra_sesgo=2), ensena=0),
        'patas_act': dict(g=genoma(pata_act_sesgo=2), ensena=0),
        'patas_limpia': dict(g=suma(PATAS, LIMPIA), ensena=0),
        'patas_neof': dict(g=suma(PATAS, NEOF), ensena=0),
        'patas_margen': dict(g=suma(PATAS, MARGEN), ensena=0),
        'patas_malosuave': dict(g=suma(PATAS, genoma(boca_malo_sesgo=-4, boca_malo_otra=4)), ensena=0),
        # tercera ola (tras ver que el fundador de v14.3 necesita ~8 intentos y el de O1 uno): PRUEBA de O1 con dosis de verdad
        # (cero en min(E,Ag) = 0.5: +4 al nacer con dote 0.6, -12 a 0.2 contra el logit +7 de FABRICA)
        'neof_fuerte': dict(g=genoma(boca_neutro_sesgo=-20, boca_neutro_reserva=60), ensena=0),
        'patas_neof_fuerte': dict(g=suma(PATAS, genoma(boca_neutro_sesgo=-20, boca_neutro_reserva=60)), ensena=0),
        'o1': dict(g=None, ensena=None),
    }
    return B


def modulo(ident):
    if ident not in _MODS:
        if ident == 'O1': _MODS[ident] = MC.carga_carro('O1')
        else:
            ruta = os.path.join(AQUI, 'carros', 'TRASP.py')
            spec = importlib.util.spec_from_file_location('carro_TRASP', ruta)
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); _MODS[ident] = m
    return _MODS[ident]


def corre(brazo, seed, T):
    B = brazos()[brazo]
    if brazo == 'o1':
        r = MC.run(seed, [('O1', modulo('O1'))] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, cruce=None)
    else:
        m = modulo('TRASP'); m.ENSENA = int(B['ensena'])
        cr = dict(NG=NG, p_mut=0.0, t_corte=0, banco_max=0, donante='padre', n_sombra=0, g_max=4, cada=0, genomas_ini=[list(B['g'])] * 9)
        r = MC.run(seed, [('V143', m)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, cruce=cr)
    L = [J.resumen_linaje(d, seed) for d in r['linajes']]
    for x in L:
        tf, qf, nr = J.t_fund_reconstruido(x['telem']['vidas'], x['telem']['desc_por_vida'])
        x['t_fund_rec_ok'] = bool(tf[:200] == x['telem']['t_fund'] and qf == x['cola_final'] and nr == x['nac_reales'])
        x.pop('diag', None)
    tel = [dict(v143=d['carro'].get('v143'), cruce={k: v for k, v in (d['carro'].get('cruce') or {}).items() if k not in ('genoma', 'nombres')},
                ensena=d['carro'].get('ensena'), apr_pol=(d['carro'].get('apr') or {}).get('politica')) for d in r['linajes']]
    sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
    return dict(brazo=brazo, seed=seed, T=T, genoma=B['g'], ensena=B['ensena'], linajes=L, pista=r['pista'],
                R0_pista=round(sd / (sm + len(L)), 4), pizarra_n=len(r['pizarra_log']), tel=tel)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--brazo', required=True); ap.add_argument('--semilla', type=int, required=True); ap.add_argument('--T', type=int, default=100000)
    a = ap.parse_args()
    if not 33001 <= a.semilla <= 33999: raise SystemExit('semillas sólo 33001-33999')
    if a.brazo not in brazos(): raise SystemExit(f"brazo desconocido {a.brazo}; válidos {list(brazos())}")
    os.makedirs(DATOS, exist_ok=True)
    out = os.path.join(DATOS, f"{a.brazo}_s{a.semilla}_T{a.T}.json")
    t0 = time.time()
    r = corre(a.brazo, a.semilla, a.T)
    r['seg'] = round(time.time() - t0, 1)
    r['sha'] = dict(motor=h16(os.path.join(CRUCE, 'motor_cruce.py')), carro=h16(os.path.join(AQUI, 'carros', 'TRASP.py')) if a.brazo != 'o1' else h16(os.path.join(PISTA, 'carros', 'O1.py')),
                    juez=h16(os.path.join(PISTA, 'juez.py')), corre=h16(os.path.abspath(__file__)))
    json.dump(r, open(out, 'w', encoding='utf-8'), default=str)
    import statistics as st
    R0 = [l['R0_real'] for l in r['linajes']]
    print(f"{a.brazo} s{a.semilla} T{a.T} {r['seg']}s · R0 real med {st.median(R0):.3f} · cruzan {sum(l['cruza_real'] for l in r['linajes'])}/9 · persisten {sum(l['persiste'] for l in r['linajes'])}/9 · "
          f"vida {st.median([l['vida_med'] for l in r['linajes']])} · fund {st.median([l['fundadores'] for l in r['linajes']])} · {out}")


if __name__ == '__main__':
    main()
