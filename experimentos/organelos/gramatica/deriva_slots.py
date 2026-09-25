"""deriva_slots.py — LA DERIVA DEL LARGO que imponen los OPERADORES, sin mundo y sin seleccion (pedido del coordinador tras la ficha D1
de exploracion_fable: 'el tamano del genoma lo fijo el SESGO de los operadores'). Opus A, 24-sep-2026. Un proceso, segundos.

MISION: llegar a la AGI por este camino.

Cadenas NEUTRALES de copias con gramatica_def.muta_gram y las tasas de la serie (corre_gramatica.GRAM, ALFABETO), desde el fundador
silencioso de un slot. Por profundidad genealogica g: distribucion de slots TOTALES, slots ACTIVOS y fraccion con algun organo expresado.
Es la prediccion de la deriva que AZAR y las sombras miden en el mundo. Escribe datos/deriva_slots.json.
"""
import json, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gramatica_def as GD
import corre_gramatica as CG

N_CAD = 20000; GS = (10, 20, 40, 80, 160, 320)


def main():
    G = CG.GRAM; A = CG.ALFABETO
    r = np.random.default_rng([21999, 1])
    grs = GD.fundadores_silenciosos(21999, N_CAD, A)
    out = {}; g = 0
    for gmax in GS:
        while g < gmax:
            grs = [GD.muta_gram(x, r, G['p_campo'], G['p_dup'], G['p_del'], G['tope'], A)[0] for x in grs]; g += 1
        tot = np.array([len(x) for x in grs]); act = np.array([len(GD.activos(x)) for x in grs])
        out[g] = dict(total_media=round(float(tot.mean()), 3), total_dist=[round(float((tot == k).mean()), 4) for k in range(G['tope'] + 1)],
                      activos_media=round(float(act.mean()), 3), activos_dist=[round(float((act == k).mean()), 4) for k in range(G['tope'] + 1)],
                      con_organo=round(float((act > 0).mean()), 4), vacios=round(float((tot == 0).mean()), 4))
        print(f"g {g:>3}: slots totales {out[g]['total_media']} {out[g]['total_dist']} · activos {out[g]['activos_media']} "
              f"{out[g]['activos_dist']} · con organo {out[g]['con_organo']} · vacios {out[g]['vacios']}", flush=True)
    os.makedirs(os.path.join(AQUI, 'datos'), exist_ok=True)
    json.dump(dict(GRAM=G, alfabeto=[list(a) for a in A], cadenas=N_CAD, por_generacion=out),
              open(os.path.join(AQUI, 'datos', 'deriva_slots.json'), 'w', encoding='utf-8'), indent=1)


if __name__ == '__main__':
    main()
