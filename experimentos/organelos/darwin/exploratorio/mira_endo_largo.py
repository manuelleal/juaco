# EXPLORATORIO, no es dato (coordinador, 24-sep-2026, pedido del director: "córrelo solo a ese en un pool pequeño, quiero ver qué hace").
"""Mira la endosimbiosis por más tiempo: VIDA_S contra INERTE, 3 semillas de práctica (22996-22998), w30, T 300 000.
El vivero sigue encendido todo el tiempo (t_corte = T): es para VER la trayectoria de la domesticación sin que el mundo chico
se extinga tras el corte. NO mide selección natural pura y NO decide nada. Pool 3.
Salida: un JSON por corrida en esta carpeta y `mira_endo_largo.png` con la trayectoria.
"""
import json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); DARWIN = os.path.dirname(AQUI)
sys.path.insert(0, DARWIN); sys.dont_write_bytecode = True
import corre_endo as CE

T = 300000; SEMILLAS = (22996, 22997, 22998); BRAZOS = ('VIDA_S', 'INERTE')


def uno(args):
    seed, brazo = args
    fin = os.path.join(AQUI, f"mira_{brazo}_s{seed}.json")
    if os.path.exists(fin): return json.load(open(fin, encoding='utf-8'))
    t0 = time.time()
    r = CE.MD.run_solapadas(seed, [CE.CARRO] * CE.MUNDO['n0'], T=T, diag=0, mundo_n=CE.MUNDO['esc'], tope_cuerpos=CE.MUNDO['tope'],
                            muestra=CE.MUNDO['muestra'], eco=CE.CR.eco_cfg('VIDA', T), simb=dict(brazo=brazo))
    res = dict(seed=seed, brazo=brazo, T=T, seg=round(time.time() - t0, 1), serie_simb=r['simb']['serie'], tam_total=r['pista']['tam_total'],
               eventos=r['simb']['eventos'], don=r['simb']['don'])
    json.dump(res, open(fin, 'w', encoding='utf-8'))
    print(f"[{time.strftime('%H:%M:%S')}] {brazo} s{seed} listo ({res['seg']} s)", flush=True)
    return res


if __name__ == '__main__':
    from multiprocessing import Pool
    with Pool(3) as p: R = p.map(uno, [(s, b) for b in BRAZOS for s in SEMILLAS])
    print("LISTO", flush=True)
