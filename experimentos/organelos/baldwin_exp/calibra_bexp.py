"""calibra_bexp.py — CALIBRACION de eps_exp con la exploracion APAGADA (PREREGISTRO_baldwin_exp.md sec. 4; regla escrita ANTES de correr).
UN proceso, 4 corridas: PLAST_V_P22k (plast 1, exp 0 == motor_baldwin bit a bit) en las semillas 56681 y 56682, cada una a T 50 000 y
T 100 000 (= t_corte: el tramo con vivero, antes del colapso). La ventana [50 000, 100 000) es la DIFERENCIA de los contadores (el organo
de rechazo ya existe; en [0, 50 000) todavia se esta armando). Comprobacion: la corrida corta es el PREFIJO exacto de la larga (serie de
BLOQUES y serie_pl cada 2 000 pasos iguales hasta 50 000). Mide SOLO contadores de instrumento: vetos de las reglas de boca con reserva
>= th_exp por paso-cuerpo. Regla: eps_exp = 4 / (media de las 2 semillas de vetos con reserva por vida en la ventana), VIDA = 2270,
redondeado a 2 cifras significativas y acotado a [0.001, 0.5]. Escribe calibra_salida.json y calibra_salida.txt.
Mision: llegar a la AGI por este camino.
"""
import json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_bexp as C   # noqa: E402

N_OBJ = 4   # mordidas exploratorias por vida buscadas (sec. 4)
T1, T2 = 50000, 100000


def main():
    t0 = time.time(); L = []
    car = os.path.join(C.DATOS, 'calibra')
    fil = []
    for s in C.CALIBRA:
        a = C.corre(s, 'PLAST_V_P22k', T1, os.path.join(car, f'T{T1}')); b = C.corre(s, 'PLAST_V_P22k', T2, os.path.join(car, f'T{T2}'))
        xa, xb = a['bexp'], b['bexp']
        pref = (b['bloques']['serie'][:len(a['bloques']['serie'])] == a['bloques']['serie']
                and b['bloques']['serie_pl'][:len(a['bloques']['serie_pl'])] == a['bloques']['serie_pl'])
        dv = xb['n_veto_res'] - xa['n_veto_res']; dvt = xb['n_veto'] - xa['n_veto']; dc = xb['n_cuerpo_paso'] - xa['n_cuerpo_paso']
        f = dict(seed=s, prefijo_exacto=pref, veto_res_ventana=dv, veto_ventana=dvt, cuerpo_paso_ventana=dc,
                 veto_res_por_vida=(round(dv / dc * C.VIDA, 4) if dc else None), veto_por_vida=(round(dvt / dc * C.VIDA, 4) if dc else None),
                 veto_res_por_vida_0_100k=xb['veto_res_por_vida'], n_mord_exp=[xa['n_mord_exp'], xb['n_mord_exp']], vivos_T2=b['baldwin']['vivos_T'])
        fil.append(f); L.append(f"s{s}: {f}")
    m = sum(f['veto_res_por_vida'] for f in fil) / len(fil)
    eps = min(0.5, max(0.001, float(f"{N_OBJ / m:.2g}"))) if m > 0 else None
    L.append(f"media de vetos con reserva por vida en [{T1}, {T2}) = {m:.4f} -> eps_exp = {N_OBJ}/{m:.4f} = {N_OBJ / m if m else None} -> 2 cifras, acotado: {eps}")
    L.append(f"prefijo exacto {[f['prefijo_exacto'] for f in fil]} · mordidas exploratorias con exp = 0: {[f['n_mord_exp'] for f in fil]} (deben ser 0) · {time.time() - t0:.0f} s")
    for s in L: print(s)
    json.dump(dict(filas=fil, media=m, eps_exp=eps, n_obj=N_OBJ, ventana=[T1, T2], semillas=list(C.CALIBRA)),
              open(os.path.join(AQUI, 'calibra_salida.json'), 'w'), indent=1)
    open(os.path.join(AQUI, 'calibra_salida.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
