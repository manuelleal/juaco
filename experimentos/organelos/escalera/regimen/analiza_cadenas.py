"""analiza_cadenas.py — regimen (1-oct-2026). SIN correr nada. En las 20 cadenas sel de la serie de perillas:
(1) la moneda de la camara por pasaje: rho(GV de la siembra, refundaciones por camara) y rho(GV, establecidos) en p1..p4 (¿la seleccion aun
    empuja GV por encima de 0.19?); (2) ¿meseta? signo de GV(p4) - GV(p3) por cadena y tamano del paso; (3) GV de la siembra vs GV de los
    fundadores de la camara dentro del pasaje (quien dona).
    python experimentos/organelos/escalera/regimen/analiza_cadenas.py
"""
import glob, json, os, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analiza_serie import SERIE, spearman, med


def main():
    C = {}
    for f in sorted(glob.glob(os.path.join(SERIE, 'cadena_i*_sel.json'))):
        d = json.load(open(f, encoding='utf-8')); C[d['i']] = d
    I = sorted(C)
    print("(1) sel por pasaje: rho(GV siembra del pasaje ANTERIOR -> refundaciones por camara, establecidos, cruzan, mundo AC, fund de camara) n 20")
    for p in range(1, 5):
        g = [C[i]['pasajes'][p - 1]['genes_siembra']['GV'] for i in I]
        q = [C[i]['pasajes'][p] for i in I]
        print(f"  p{p}: GV_prev med {med(g)} · refund {spearman(g, [z['fund_de_camara'] for z in q]):+.2f} · est {spearman(g, [z['moneda']['n_est'] for z in q]):+.2f} · "
              f"cruzan {spearman(g, [z['cruzan'] for z in q]):+.2f} · AC {spearman(g, [z['mundo_AC'] for z in q]):+.2f} · refund med {med([z['fund_de_camara'] for z in q])}")
    print("\n(1b) mismo pasaje: rho(GV siembra final del pasaje p -> refundaciones de p)")
    for p in range(5):
        g = [C[i]['pasajes'][p]['genes_siembra']['GV'] for i in I]; q = [C[i]['pasajes'][p] for i in I]
        print(f"  p{p}: refund {spearman(g, [z['fund_de_camara'] for z in q]):+.2f} · est {spearman(g, [z['moneda']['n_est'] for z in q]):+.2f}")
    print("\n(2) meseta: GV(p) - GV(p-1) por cadena: sube / baja, mediana del paso")
    for p in range(1, 5):
        d = [C[i]['pasajes'][p]['genes_siembra']['GV'] - C[i]['pasajes'][p - 1]['genes_siembra']['GV'] for i in I]
        print(f"  p{p-1}->p{p}: sube {sum(z > 0 for z in d)} baja {sum(z < 0 for z in d)} · mediana {med(d):+.4f} · |paso| med {med([abs(z) for z in d])}")
    print("\n(3) dispersion de GV dentro de la siembra final (p4): mediana del rango intercuartil y del maximo - mediana por cadena")
    iq = []; mx = []
    for i in I:
        s = sorted(z['GV'] for z in C[i]['siembra_final']); n = len(s)
        iq.append(s[3 * n // 4] - s[n // 4]); mx.append(s[-1] - st.median(s))
    print(f"  IQR med {med(iq)} · max - mediana med {med(mx)} · n siembra med {med([len(C[i]['siembra_final']) for i in I])}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
