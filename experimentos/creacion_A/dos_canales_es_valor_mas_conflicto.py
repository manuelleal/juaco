"""CREADOR A — los DOS CANALES no negativos + drenaje `lam` SON un valor con signo + una masa de conflicto.

TESIS (algebra, luego se comprueba con numeros). Para una celda con Wp,Wn >= 0 y tope C, definase
        W = Wp - Wn        (valor con signo)              m = min(Wp, Wn)   (masa de conflicto, >= 0)
La aplicacion (Wp,Wn) <-> (W,m) es una BIYECCION del cuadrante: Wp = m + max(W,0), Wn = m + max(-W,0).
En esas coordenadas las tres piezas de la regla de v13 son:
  (1) drenaje de la parte comun   Wp,Wn -= lam*min(Wp,Wn)      ==>   m <- (1-lam)*m ,   W SIN CAMBIO
  (2) refuerzo                    Wp <- clip(Wp+eta*d,0,C)     ==>   W <- W + min(eta*d, C - m - max(W,0))
      castigo                     Wn <- clip(Wn+eta*a*|d|,0,C) ==>   W <- W - min(eta*a*|d|, C - m - max(-W,0))
      (la parte del empujon que CANCELA valor de signo contrario se convierte en masa de conflicto: m crece)
  (3) fision de v11 (division por conflicto de signo)          ==>   la hija se lleva EXACTAMENTE m con el signo
      nuevo, y la madre se queda con W -/+ m, es decir con su valor PURGADO de la masa de conflicto.
COROLARIOS
  C1. El drenaje `lam` NO toca el valor: es la tasa de olvido de la MASA DE CONFLICTO.
  C2. m solo actua sobre el valor por el tope: |W| <= C - m. Si el tope nunca aprieta, `lam` y el segundo canal
      son INERTES para el valor y un solo vector con signo es equivalente. (Esto DEMUESTRA la ablacion del
      Agente B en PUENTE_xor: lam_lenta=0 y clip_s=10 no movian nada — no era casualidad, es identidad.)
  C3. En la via LENTA no hay fision, luego C2 aplica entera: la via lenta puede ser UN vector con signo.
      En la via RAPIDA no: la fision de v11 LEE m, asi que el segundo numero por celda tiene trabajo.
  C4. m es exactamente una variable de METAPLASTICIDAD ya presente en el tronco (evidencia contradictoria
      acumulada, con olvido lam) — no hay que inventarla para consolidar.
Este script comprueba (a) la biyeccion y las ecuaciones, (b) si el tope aprieta en corridas reales, (c) cuanta
masa de conflicto hay. Importa los originales sin tocarlos. Un proceso, sin Pool.
"""
import sys, os, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'nivel7_xor_lectura'))
sys.path.insert(0, os.path.join(AQUI, '..', '..', 'organismo'))
import organismo_v13q as Q   # original, NO se toca


# ---------------------------------------------------------------- (a) la biyeccion y las ecuaciones
def prueba_equivalencia(n=200000, C=3.0, lam=0.05, eta=0.03, aversion=1.0, seed=7):
    """Conduce los dos parametrizados con la MISMA secuencia de (delta, activo) y compara."""
    rng = np.random.default_rng(seed)
    Wp = Wn = 0.0; W = 0.0; m = 0.0
    peor_W = 0.0; peor_m = 0.0; topes = 0
    for t in range(n):
        d = float(rng.normal(0, 1.2))
        # --- parametrizacion original (dos canales)
        mc = min(Wp, Wn); Wp -= lam * mc; Wn -= lam * mc
        if d > 0: Wp = min(max(Wp + eta * d, 0.0), C)
        else:     Wn = min(max(Wn + eta * aversion * (-d), 0.0), C)
        # --- parametrizacion (W, m)
        m = (1 - lam) * m
        if d > 0:
            inc = min(eta * d, C - m - max(W, 0.0))
            Wm_ = W + inc
            m = m + (max(-W, 0.0) - max(-Wm_, 0.0)); W = Wm_
            if inc < eta * d - 1e-15: topes += 1
        else:
            dec = min(eta * aversion * (-d), C - m - max(-W, 0.0))
            Wm_ = W - dec
            m = m + (max(W, 0.0) - max(Wm_, 0.0)); W = Wm_
            if dec < eta * aversion * (-d) - 1e-15: topes += 1
        peor_W = max(peor_W, abs((Wp - Wn) - W)); peor_m = max(peor_m, abs(min(Wp, Wn) - m))
    return dict(pasos=n, max_dif_W=peor_W, max_dif_m=peor_m, topes=topes, W=W, m=m, Wp=Wp, Wn=Wn)


# ---------------------------------------------------------------- (b)+(c) en corridas reales
def sonda_real(seeds=(1, 2, 3), T=100000, **kw):
    filas = []
    for s in seeds:
        r = Q.run(s, T=T, **kw)
        Wps = np.array(r['Wps']); Wns = np.array(r['Wns'])
        filas.append(dict(seed=s, n_techo=r['n_techo'], t_techo=r['t_techo'], splits=r['splits'], celdas=r['celdas'],
                          max_Wps=float(Wps.max()), max_Wns=float(Wns.max()),
                          max_m_lenta=float(np.minimum(Wps, Wns).max()),
                          media_m_lenta=float(np.minimum(Wps, Wns).mean()),
                          max_absW_lenta=float(np.abs(Wps - Wns).max()),
                          rango_libre=float(3.0 - np.minimum(Wps, Wns).max())))
    return filas


if __name__ == '__main__':
    print('=== (a) biyeccion y ecuaciones: dos canales  ==  (valor, masa de conflicto) ===')
    for seed in (7, 11, 13):
        r = prueba_equivalencia(seed=seed)
        print(f'  semilla {seed}: max|dW| = {r["max_dif_W"]:.3e}   max|dm| = {r["max_dif_m"]:.3e}   '
              f'veces que el tope apreto = {r["topes"]}   (W={r["W"]:+.4f}, m={r["m"]:.4f})')

    print('\n=== (b)+(c) corridas reales del mundo de regla (organismo_v13q ORIGINAL, T=100000) ===')
    print(f'{"escenario":>26} {"s":>2} {"n_techo":>8} {"max Wps":>8} {"max Wns":>8} {"max m lenta":>12} '
          f'{"max|W| lenta":>13} {"rango libre":>12} {"splits":>7}')
    todo = []
    for etq, kw in (('regla/px0  cuadratica', dict(mundo='regla', regla='px0', lectura='cuadratica', eta_s=0.015, puerta=3)),
                    ('regla/xor01 cuadratica', dict(mundo='regla', regla='xor01', lectura='cuadratica', eta_s=0.015, puerta=3)),
                    ('regla/px0  lineal', dict(mundo='regla', regla='px0', lectura='lineal', eta_s=0.015, puerta=3))):
        for f in sonda_real((1, 2, 3), T=100000, **kw):
            print(f'{etq:>26} {f["seed"]:>2} {f["n_techo"]:>8} {f["max_Wps"]:>8.3f} {f["max_Wns"]:>8.3f} '
                  f'{f["max_m_lenta"]:>12.3f} {f["max_absW_lenta"]:>13.3f} {f["rango_libre"]:>12.3f} {f["splits"]:>7}')
            todo.append(dict(escenario=etq, **f))
    with open(os.path.join(AQUI, 'dos_canales_valor_conflicto.json'), 'w') as fh:
        json.dump(todo, fh, indent=1)
    print('\nOK -> dos_canales_valor_conflicto.json')
