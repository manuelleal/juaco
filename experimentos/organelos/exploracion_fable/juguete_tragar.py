# EXPLORATORIO, no es dato
"""juguete_tragar.py -- ENDOSIMBIOSIS de bolsillo: ¿la selección FIJA un cuerpo tragado como órgano (Margulis), sin que
nadie diga "esto es un órgano"?

Misión: llegar a la AGI por este camino. Mundo de bolsillo con la retina del bicho (organismo_f9c.py:143).
Lo que se DISEÑA aquí (y se declara): que hay dos linajes distintos y que uno puede tragar al otro por error de boca.
Lo que NO se diseña: si el tragado se queda, se hereda y se vuelve parte del cuerpo. Eso lo decide la energía.

MUNDO
- GRANDES (G): ven la retina con dos píxeles tapados (sólo los píxeles 0 y 2): A->(1,0), B->(1,1), C->(0,1), D->(0,1).
  NO pueden distinguir agua (C, +1) de sal (D, -1). Costo 0.02/paso, parto en E >= 2.0.
- CHICOS (S): ven la retina entera, pero son frágiles: costo 0.03/paso, E tope 1.5, parto en E >= 1.4 (hijo con 0.7).
- TRAGAR (sólo en los brazos con tragar): cada paso, un G sin simbionte se cruza con un S libre con p = 0.02; si el G
  MUERDE (su boca decide sobre la retina de S, que se le presenta como si fuera la letra (1,1,1,1,1,1): algo que no
  conoce), el S queda DENTRO: desde entonces la boca del G decide con la suma de sus órganos (retina tapada) y los del
  S (retina entera). El S dentro cobra 0.01/paso al G (upkeep). En el parto del G, el S se copia al hijo (con sus
  errores de copia): transmisión vertical. Si el G muere, el S muere. Un S tragado ya no pare por su cuenta.
- El linaje S libre sigue existiendo aparte (y puede extinguirse solo: es frágil).

BRAZOS
  SIN_TRAGAR    G y S conviven, nadie traga. Base.
  TRAGAR        con tragar y selección natural (muere quien se queda sin E).
  TRAGAR_DERIVA con tragar, pero muerte al azar y parto al azar (sin selección): mide cuánto simbionte deja el puro
                encuentro, sin que la energía lo premie.

PREDICCIONES ESCRITAS ANTES DE CORRER (pueden fallar):
  P1  en TRAGAR, la fracción de G con simbionte al final es >= 0.7 en >= 4 de 5 semillas.
  P2  en TRAGAR_DERIVA esa fracción es < 0.5 en >= 4 de 5 (el encuentro solo no lo fija; la energía sí).
  P3  en TRAGAR, los G con simbionte aciertan más sobre C/D que los G sin simbionte (>= +0.15) en >= 4 de 5.
  P4  en TRAGAR el linaje S LIBRE se extingue o queda por debajo de SIN_TRAGAR (el que traga lo come; también,
      el S de adentro le hace competencia al S de afuera por los G buenos: los G tragadores viven más).
  P5  el upkeep de 0.01 no alcanza para que la selección tire el simbionte: si la fracción de G con simbionte baja de
      0.7 a la mitad del tiempo al final, P5 cae y el costo manda.
Semillas 23021-23025. Un proceso. Previsto < 5 minutos; MEDIDO 418 s (se pasó: dos poblaciones de 150). Para repetir
dentro del límite: T 2500. No se volvió a correr (presupuesto).

RESULTADO (salida_tragar.txt): P1 REFUTADA (fracción con simbionte en TRAGAR 0.30-0.86, sólo 1/5 >= 0.7); P2 REFUTADA al
revés (TRAGAR_DERIVA llega a 1.00 en 5/5: el simbionte se hereda y NUNCA se pierde, así que sin selección se fija por
TRINQUETE; la medida "fracción con simbionte" no sirve sin un mecanismo de pérdida); P3 SE CUMPLE 5/5 (acierto sobre
C/D con simbionte 0.68-0.89 contra 0.50 sin él: el tragado sí le da al anfitrión lo que no podía ver); P4 REFUTADA (el S
libre sigue en su tope de 150); P5 SE CUMPLE (la fracción no cae de la mitad al final; sube despacio). Lectura: la selección
mantiene al simbionte en frecuencias intermedias mientras la deriva lo fija; el instrumento no separa las dos cosas hasta
que exista PÉRDIDA del simbionte (expulsión en el parto con p). Eso va a la ficha 2 como control obligatorio.
"""
import time
import numpy as np
from juguete_ohno import organo_azar, decide, muta, PAT0

PAT = np.array([PAT0[k] for k in 'ABCD'], float); VAL = np.array([1.0, -1.0, 1.0, -1.0])
MASK_G = np.array([1, 0, 1, 0, 0, 0], float)
TOPE_G = 150; TOPE_S = 150; N0 = 40; EDAD_MAX = 400; P_CRUCE = 0.02; UPKEEP = 0.01


def ret_pm(ret, mask=None):
    if mask is not None: ret = ret * mask
    return 2 * ret - 1


def corre(seed, brazo, T=4000):
    r = np.random.default_rng(seed)
    G = [dict(g=[organo_azar(r) for _ in range(4)], s=None, E=1.0, edad=0) for _ in range(N0)]
    S = [dict(g=[organo_azar(r) for _ in range(4)], E=0.7, edad=0) for _ in range(N0)]
    frac = []; tragados = 0; acCD_con = [0, 0]; acCD_sin = [0, 0]
    deriva = brazo == 'TRAGAR_DERIVA'
    for t in range(T):
        # ---- chicos libres
        vivosS = []; nuevosS = []
        for s in S:
            li = int(r.integers(4)); m = decide(s['g'], ret_pm(PAT[li]), r)
            if m: s['E'] += VAL[li]
            s['E'] = min(s['E'], 1.5) - 0.03; s['edad'] += 1
            if deriva:
                if r.random() < 1 / 60: continue
                if r.random() < 1 / 45 and len(S) + len(nuevosS) < TOPE_S: nuevosS.append(dict(g=muta(s['g'], r, 'ESTRUCTURA'), E=0.7, edad=0))
                s['E'] = max(s['E'], 0.5)
            else:
                if s['E'] <= 0 or s['edad'] > EDAD_MAX: continue
                if s['E'] >= 1.4 and len(S) + len(nuevosS) < TOPE_S:
                    s['E'] -= 0.7; nuevosS.append(dict(g=muta(s['g'], r, 'ESTRUCTURA'), E=0.7, edad=0))
            vivosS.append(s)
        S = vivosS + nuevosS
        # ---- grandes
        vivosG = []; nuevosG = []
        for g in G:
            li = int(r.integers(4))
            if g['s'] is None: m = decide(g['g'], ret_pm(PAT[li], MASK_G), r)
            else:
                # boca conjunta: suma de los órganos propios (retina tapada) y los del simbionte (retina entera)
                s1 = sum(w for p, w in g['g'] if float(p @ ret_pm(PAT[li], MASK_G)) >= 3)
                s2 = sum(w for p, w in g['s']['g'] if float(p @ ret_pm(PAT[li])) >= 3)
                d1 = any(float(p @ ret_pm(PAT[li], MASK_G)) >= 3 for p, w in g['g'])
                d2 = any(float(p @ ret_pm(PAT[li])) >= 3 for p, w in g['s']['g'])
                m = (s1 + s2 > 0) if (d1 or d2) else (r.random() < 0.5)
            if m: g['E'] += VAL[li]
            if li >= 2 and t >= T // 2:
                a = acCD_con if g['s'] is not None else acCD_sin
                a[0] += int(m == (VAL[li] > 0)); a[1] += 1
            g['E'] -= 0.02 + (UPKEEP if g['s'] is not None else 0.0); g['edad'] += 1
            # tragar: cruce con un S libre
            if brazo != 'SIN_TRAGAR' and g['s'] is None and S and r.random() < P_CRUCE:
                if decide(g['g'], ret_pm(np.ones(6), MASK_G), r):
                    k = int(r.integers(len(S))); g['s'] = dict(g=[(p.copy(), w) for p, w in S[k]['g']]); S.pop(k); tragados += 1
            if deriva:
                if r.random() < 1 / 60: continue
                pare = r.random() < 1 / 45 and len(G) + len(nuevosG) < TOPE_G; g['E'] = max(g['E'], 0.5)
                if pare: nuevosG.append(dict(g=muta(g['g'], r, 'ESTRUCTURA'), s=(None if g['s'] is None else dict(g=muta(g['s']['g'], r, 'ESTRUCTURA'))), E=1.0, edad=0))
            else:
                if g['E'] <= 0 or g['edad'] > EDAD_MAX: continue
                if g['E'] >= 2.0 and len(G) + len(nuevosG) < TOPE_G:
                    g['E'] /= 2
                    nuevosG.append(dict(g=muta(g['g'], r, 'ESTRUCTURA'), s=(None if g['s'] is None else dict(g=muta(g['s']['g'], r, 'ESTRUCTURA'))), E=g['E'], edad=0))
            vivosG.append(g)
        G = vivosG + nuevosG
        if not G: return dict(extinto=t, frac=frac)
        if t % 100 == 0: frac.append(np.mean([g['s'] is not None for g in G]))
    return dict(extinto=None, frac=frac, nG=len(G), nS=len(S), tragados=tragados,
                acCD_con=(acCD_con[0] / acCD_con[1] if acCD_con[1] else float('nan')),
                acCD_sin=(acCD_sin[0] / acCD_sin[1] if acCD_sin[1] else float('nan')))


if __name__ == '__main__':
    t0 = time.time()
    print("EXPLORATORIO, no es dato -- juguete_tragar: endosimbiosis de bolsillo")
    print(f"{'brazo':14s} {'seed':>6s} {'frac_mitad':>10s} {'frac_fin':>8s} {'nG':>4s} {'nS_libre':>8s} {'tragados':>8s} {'acCD_con':>8s} {'acCD_sin':>8s}")
    for brazo in ('SIN_TRAGAR', 'TRAGAR', 'TRAGAR_DERIVA'):
        for seed in range(23021, 23026):
            d = corre(seed, brazo)
            if d['extinto'] is not None: print(f"{brazo:14s} {seed:6d}  G EXTINTO en t={d['extinto']}"); continue
            f = d['frac']
            print(f"{brazo:14s} {seed:6d} {f[len(f)//2]:10.2f} {f[-1]:8.2f} {d['nG']:4d} {d['nS']:8d} {d['tragados']:8d} {d['acCD_con']:8.2f} {d['acCD_sin']:8.2f}")
    print(f"{time.time()-t0:.0f} s")
