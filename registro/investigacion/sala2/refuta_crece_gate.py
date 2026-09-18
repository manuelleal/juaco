"""Sala 2 / REFUTADOR (medibilidad) del diseno crece_codigo. ARITMETICA CERRADA del pseudocodigo §2.3 (Ancla B/E): NO corre el
organismo ni el mundo, no usa rng. Reproduce solo la via lenta lineal de v14.1 (eta_s=0.15, clip_s=10, lam=0.05, aversion=1),
la EMA del error de la lineal `_EL` (g_rho=0.02) y el error propio `_GE` de UN nodo que nace en la segunda sorpresa de B con
`_GE=(R-_lb)**2` (instantaneo, `_nace`), y aplica la compuerta de lectura `_GE[n] < _EL` (`_lector`) y la poda
`_GN>=6 and _GE>=_EL` (`_crece_paso`). Pregunta: en E1 del tronco (A comida +1, B veneno -3), ¿lee el nodo alguna vez?
Depende de QUE se mordio primero. Uso: python refuta_crece_gate.py
"""
import numpy as np
A = np.array([1, 1, 0, 1, 0, 0.]); B = np.array([1, 0, 1, 0, 1, 0.])
R = {'A': 1.0, 'B': -3.0}
ETA, CLIP, LAM, RHO, THETA, REC, MINVIS = 0.15, 10.0, 0.05, 0.02, 1.5, 2, 6


def corre(seq):
    Wps = np.zeros(6); Wns = np.zeros(6); EL = np.inf; GS = 0; nodo = None; hist = []
    for t, k in enumerate(seq, 1):
        P = A if k == 'A' else B; r = R[k]
        lb = float((Wps - Wns) @ P)                       # lectura lineal ANTES del paso (lo que la boca leeria si no hay nodo)
        e = r - lb
        # paso de la lineal (L116-L120 de v14.1, D2: su propio error)
        if LAM: m = np.minimum(Wps, Wns) * (P > 0); Wps = Wps - LAM * m; Wns = Wns - LAM * m
        if e > 0: Wps = np.clip(Wps + ETA * e * P, 0, CLIP)
        else:     Wns = np.clip(Wns + ETA * (-e) * P, 0, CLIP)
        # _crece_paso(P, R, _ws_boca, _lb): _EL con el error de la lineal en la mordida (antes del paso)
        el = e * e; EL = el if not np.isfinite(EL) else (1 - RHO) * EL + RHO * el
        lee = None; poda = False
        if nodo is not None:                              # el nodo vivo actualiza su error con lo que HABRIA leido
            c = int(P[nodo['i']]) * 2 + int(P[nodo['j']])
            pred = nodo['T'][c] if nodo['V'][c] > 0 else lb
            en = (r - pred) ** 2; nodo['GE'] = (1 - RHO) * nodo['GE'] + RHO * en
            nodo['T'][c] = r; nodo['V'][c] += 1; nodo['GN'] += 1
            lee = bool(nodo['V'][c] > 0 and nodo['GE'] < EL)  # lo que _lector devolveria para ESTE patron en la mordida siguiente
            if nodo['GN'] >= MINVIS and nodo['GE'] >= EL: poda = True
        if nodo is None and k == 'B' and abs(e) > THETA:  # sorpresa de la lenta -> traza Hebb del par (0,2) de B
            GS += 1
            if GS >= REC:                                 # _nace: hereda el error INSTANTANEO de la lineal en esta mordida
                nodo = dict(i=0, j=2, T=np.zeros(4), V=np.zeros(4, int), GE=el, GN=1)
                nodo['T'][3] = r; nodo['V'][3] = 1
                lee = bool(nodo['GE'] < EL)
        hist.append((t, k, round(lb, 3), round(e, 3), round(EL, 3), None if nodo is None else round(nodo['GE'], 3), lee, poda))
        if poda: nodo = None
    return hist


if __name__ == '__main__':
    casos = {'B primero (veneno)': 'BBBBBBBB',
             'A primero, luego B': 'ABBBBBBBB',
             'A x5 primero, luego B': 'AAAAABBBBBBBB',
             'alternado A,B': 'ABABABABABABAB'}
    for nombre, seq in casos.items():
        print(f"\n=== {nombre}: {seq}")
        print("  t k   lineal(P)  e=R-lin   _EL(EMA)  _GE(nodo)  lee?  poda?")
        for (t, k, lb, e, EL, GE, lee, poda) in corre(seq):
            print(f"  {t:2d} {k}   {lb:8.3f}  {e:8.3f}   {EL:8.3f}  {'   --  ' if GE is None else f'{GE:8.3f}'}  {'' if lee is None else ('SI ' if lee else 'NO ')}  {'PODA' if poda else ''}")
