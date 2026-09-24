# EXPLORATORIO, no es dato
"""juguete_ohno.py -- ¿los ERRORES DE COPIA estructurales (duplicar, borrar, invertir) y la transferencia horizontal
hacen aparecer órganos que nadie escribió, más rápido que la mutación de perillas sola?

Misión: llegar a la AGI por este camino. Este juguete NO usa el motor de ECO ni los carros: es un mundo de bolsillo
con la misma retina de 6 píxeles (PAT de organismo_f9c.py:143) para que la idea se lea en el vocabulario del bicho.

MUNDO DE BOLSILLO
- Cada paso, cada cuerpo ve UNA letra (retina de 6 bits) y decide morder o no. Morder suma el valor de la letra
  (+1 comida/agua, -1 veneno/sal). Vivir cuesta 0.02 por paso. E <= 0 -> muere. Edad > 400 -> muere.
- Parto: E >= 2.0 -> el hijo nace con la mitad de E y el genoma copiado CON ERRORES. Tope de 300 cuerpos: si se
  alcanza, la ventana no produce hijo (como P4 de motor_convive). Ningún juez: nace quien junta energía, muere quien no.
- A t = T/2 el mundo CAMBIA: aparecen 4 letras nuevas (patrones nuevos, valores nuevos) y las viejas se van.
  Lo que se mide es cuánto tarda la población en volver a comer bien (aceleración sin juez: el mundo cambia).

GENOMA = LISTA de órganos de largo VARIABLE. Un órgano = (patrón en {-1,0,+1}^6, peso w). Un órgano "dispara" si
  patrón · (2*retina-1) >= umbral fijo 3 (tres píxeles de acuerdo). La boca muerde si la suma de los pesos de los que
  disparan es > 0; si ninguno dispara, muerde con probabilidad 0.5 (curiosidad tonta).
BRAZOS (mismo mundo, mismas semillas):
  PUNTO       genoma fijo de 4 órganos; sólo cambian un elemento del patrón o el peso (perillas). = ECO hoy.
  ESTRUCTURA  además: DUPLICAR un órgano (Ohno), BORRAR uno, INVERTIR el peso, FUSIONAR dos (OR de patrones).
  ESTRUCTURA_HGT  además: al morir, el cuerpo deja UN órgano en el suelo; el siguiente que nace ahí lo toma (0.2).
  DERIVA      = ESTRUCTURA pero la muerte es al azar (misma tasa media) y el parto no depende de E: control sin selección.

PREDICCIONES ESCRITAS ANTES DE CORRER (pueden fallar):
  P1  tras el cambio del mundo, ESTRUCTURA recupera acierto >= 0.8 en menos pasos que PUNTO en >= 4 de 5 semillas.
  P2  al final, ESTRUCTURA tiene más órganos por genoma que al inicio (crece), y DERIVA crece MÁS que ESTRUCTURA
      (sin selección nada poda: el genoma se hincha; con selección la poda existe aunque sea débil).
  P3  ESTRUCTURA_HGT no mejora sobre ESTRUCTURA (el órgano del suelo suele ser del mundo viejo).
  P4  DERIVA no recupera acierto (< 0.6) nunca.
Semillas 23001-23005. Un proceso. T 4000, tope 200 (recortado tras medir 4.7 s por 1500 pasos). < 5 minutos.
"""
import sys, time
import numpy as np

PAT0 = {'A': [1, 1, 0, 1, 0, 0], 'B': [1, 0, 1, 0, 1, 0], 'C': [0, 1, 1, 0, 0, 1], 'D': [0, 0, 1, 0, 1, 1]}   # organismo_f9c.py:143
VAL0 = {'A': +1.0, 'B': -1.0, 'C': +1.0, 'D': -1.0}
UMBRAL = 3; COSTO = 0.02; E_PARTO = 2.0; E_NACE = 1.0; EDAD_MAX = 400; TOPE = 200; N0 = 60
P_PUNTO = 0.3; P_ESTR = 0.15; P_HGT = 0.2; NORG0 = 4


def letras_nuevas(r):
    """4 patrones nuevos de 6 bits (3 encendidos, distintos de los viejos y entre sí), valores +1,-1,+1,-1 barajados."""
    viejos = set(tuple(v) for v in PAT0.values()); nuevos = []
    while len(nuevos) < 4:
        p = [0] * 6
        for i in r.choice(6, 3, replace=False): p[i] = 1
        if tuple(p) not in viejos and tuple(p) not in set(map(tuple, nuevos)): nuevos.append(p)
    vals = [1.0, -1.0, 1.0, -1.0]; r.shuffle(vals)
    return np.array(nuevos, float), np.array(vals)


def organo_azar(r):
    return (r.integers(-1, 2, 6).astype(float), float(r.normal(0, 1)))


def decide(genoma, ret_pm, r):
    s = 0.0; disparo = False
    for pat, w in genoma:
        if float(pat @ ret_pm) >= UMBRAL: s += w; disparo = True
    if not disparo: return r.random() < 0.5
    return s > 0


def muta(genoma, r, brazo):
    g = [(p.copy(), w) for p, w in genoma]
    if r.random() < P_PUNTO and g:                       # perilla: un elemento del patrón o el peso
        i = int(r.integers(len(g)))
        if r.random() < 0.5:
            p, w = g[i]; j = int(r.integers(6)); p[j] = float(r.integers(-1, 2)); g[i] = (p, w)
        else:
            p, w = g[i]; g[i] = (p, w + float(r.normal(0, 0.5)))
    if brazo != 'PUNTO' and r.random() < P_ESTR and g:  # ERRORES DE COPIA estructurales
        op = r.choice(['dup', 'del', 'inv', 'fus'])
        i = int(r.integers(len(g)))
        if op == 'dup' and len(g) < 24: g.append((g[i][0].copy(), g[i][1]))               # Ohno: la copia diverge libre
        elif op == 'del' and len(g) > 1: g.pop(i)
        elif op == 'inv': g[i] = (g[i][0], -g[i][1])
        elif op == 'fus' and len(g) > 1:
            k = int(r.integers(len(g)))
            if k != i:
                p = np.where(g[i][0] != 0, g[i][0], g[k][0]); g[i] = (p, g[i][1] + g[k][1]); g.pop(k)
    return g


def corre(seed, brazo, T=6000):
    r = np.random.default_rng(seed)
    PAT = np.array([PAT0[k] for k in 'ABCD'], float); VAL = np.array([VAL0[k] for k in 'ABCD'])
    PATn, VALn = letras_nuevas(np.random.default_rng(seed + 500))
    cuerpos = [dict(g=[organo_azar(r) for _ in range(NORG0)], E=E_NACE, edad=0) for _ in range(N0)]
    suelo = None; acierto = []; norgs = []; t_rec = None; cambio = T // 2; muertos_total = 0
    for t in range(T):
        if t == cambio: PAT, VAL = PATn, VALn
        vivos = []; nuevos = []; ok = 0; n = 0
        for b in cuerpos:
            li = int(r.integers(4)); ret_pm = 2 * PAT[li] - 1
            m = decide(b['g'], ret_pm, r)
            if m: b['E'] += VAL[li]
            ok += int(m == (VAL[li] > 0)); n += 1
            b['E'] -= COSTO; b['edad'] += 1
            if brazo == 'DERIVA':
                muere = r.random() < (1.0 / 60)                       # tasa fija (≈ la mortalidad media medida en los otros brazos)
                pare = r.random() < (1.0 / 45) and len(cuerpos) + len(nuevos) < TOPE
                b['E'] = max(b['E'], 0.5)
            else:
                muere = b['E'] <= 0 or b['edad'] > EDAD_MAX
                pare = (not muere) and b['E'] >= E_PARTO and len(cuerpos) + len(nuevos) < TOPE
            if muere:
                muertos_total += 1
                if brazo == 'ESTRUCTURA_HGT' and b['g']: suelo = b['g'][int(r.integers(len(b['g'])))]
                continue
            if pare:
                if brazo != 'DERIVA': b['E'] /= 2
                gh = muta(b['g'], r, brazo)
                if brazo == 'ESTRUCTURA_HGT' and suelo is not None and r.random() < P_HGT:
                    gh.append((suelo[0].copy(), suelo[1])); suelo = None    # transferencia horizontal: toma el órgano del muerto
                nuevos.append(dict(g=gh, E=E_NACE if brazo == 'DERIVA' else b['E'], edad=0))
            vivos.append(b)
        cuerpos = vivos + nuevos
        if not cuerpos:
            return dict(extinto=t, acierto=acierto, norgs=norgs, t_rec=None)
        if t % 50 == 0:
            acierto.append(ok / max(n, 1)); norgs.append(float(np.mean([len(b['g']) for b in cuerpos])))
        if t >= cambio and t_rec is None and t % 50 == 0 and acierto[-1] >= 0.8 and t > cambio + 50: t_rec = t - cambio
    return dict(extinto=None, acierto=acierto, norgs=norgs, t_rec=t_rec, n_final=len(cuerpos), muertos=muertos_total,
                genomas=[b['g'] for b in cuerpos])


def organos_distintos(genomas):
    s = set()
    for g in genomas:
        for p, w in g: s.add((tuple(int(x) for x in p), int(np.sign(w))))
    return len(s)


if __name__ == '__main__':
    t0 = time.time(); T = 4000
    print("EXPLORATORIO, no es dato -- juguete_ohno: errores de copia estructurales contra perillas")
    print(f"{'brazo':16s} {'seed':>6s} {'ac_pre':>7s} {'ac_min':>7s} {'ac_fin':>7s} {'t_rec':>6s} {'norg0':>6s} {'norgF':>6s} {'distintos':>9s} {'vivos':>5s}")
    res = {}
    for brazo in ('PUNTO', 'ESTRUCTURA', 'ESTRUCTURA_HGT', 'DERIVA'):
        for seed in range(23001, 23006):
            d = corre(seed, brazo, T); res[(brazo, seed)] = d
            ac = d['acierto']; c = len(ac) // 2
            if d['extinto'] is not None:
                print(f"{brazo:16s} {seed:6d}  EXTINTO en t={d['extinto']}"); continue
            print(f"{brazo:16s} {seed:6d} {ac[c-1]:7.2f} {min(ac[c:c+20]):7.2f} {ac[-1]:7.2f} {str(d['t_rec']):>6s} {d['norgs'][0]:6.1f} {d['norgs'][-1]:6.1f} {organos_distintos(d['genomas']):9d} {d['n_final']:5d}")
    print()
    for p in ('P1', 'P2', 'P3', 'P4'):
        pass
    tr = lambda b: [res[(b, s)]['t_rec'] for s in range(23001, 23006)]
    print("t_rec PUNTO      :", tr('PUNTO'))
    print("t_rec ESTRUCTURA :", tr('ESTRUCTURA'))
    print("t_rec ESTR_HGT   :", tr('ESTRUCTURA_HGT'))
    print("t_rec DERIVA     :", tr('DERIVA'))
    print(f"{time.time()-t0:.0f} s")
