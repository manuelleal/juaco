"""EXPLORATORIO, no es dato. Escuela de bacterias: medio sumador por comida (Skinner) con y sin sabia.
Mini-mundo propio en Python puro (la pista de la carrera no se usa: aqui no hay espacio, solo ensayos).
Uso: python escuela.py [--humo] [--bits]   (t90 del nombre interno = ensayos hasta 85% en ventana de 50)
"""
import random, json, sys, os

RESP = [0, 1, 2]            # 0, 1, "10" (=2)
COMBOS = [(0, 0), (0, 1), (1, 0), (1, 1)]
KC = ['0+0', '0+1', '1+0', '1+1']
COMIDA, VENENO = 1.0, -0.2
CABEZAS = {'CLASES': {'X': [0, 1, 2]}, 'BITS': {'S': [0, 1], 'C': [0, 1]}}
TAREA = 'CLASES'


def correcta(a, b):
    return {'X': a + b} if TAREA == 'CLASES' else {'S': a ^ b, 'C': a & b}



def feats(a, b, sabia):
    """Estimulo -> rasgos activos: unarios, par conjuntivo, sesgo y (si hay) la senal de la sabia en la pizarra."""
    f = ['bias', 'a%d' % a, 'b%d' % b, 'p%d%d' % (a, b)]
    if sabia is not None:
        f.append('s%d' % sabia)
    return f


class Alumna:
    """REGLA:
       'RW'  = Rescorla-Wagner: error compartido entre rasgos (los rasgos compiten; puede haber bloqueo).
       'IND' = cada rasgo aprende su propio valor (sin competencia); el valor es el promedio.
       'LIN' = RW sin el rasgo de par (solo unarios + sabia): no puede representar la suma sola."""

    def __init__(self, regla, rng, eta=0.15, eps=0.1, w=None, cabezas=None):
        self.regla, self.rng, self.eta, self.eps = regla, rng, eta, eps
        self.w = dict(w) if w else {}
        self.cab = cabezas or CABEZAS['CLASES']

    def _f(self, f):
        return [x for x in f if not x.startswith('p')] if self.regla == 'LIN' else f

    def valor(self, f, r, h='X'):
        f = self._f(f)
        s = sum(self.w.get((x, h, r), 0.0) for x in f)
        return s / len(f) if self.regla == 'IND' else s

    def elige(self, f, codicia=False):
        """Una respuesta por cabeza. CLASES: una cabeza X con 0/1/10. BITS: cabeza S (bit suma) y C (acarreo)."""
        out = {}
        for h, R in self.cab.items():
            if not codicia and self.rng.random() < self.eps:
                out[h] = self.rng.choice(R)
                continue
            v = [self.valor(f, r, h) for r in R]
            m = max(v)
            out[h] = self.rng.choice([r for r in R if v[r] == m])
        return out

    def aprende(self, f, resp, rec):
        """La comida es UNA sola para todas las cabezas (en BITS: comida solo si aciertan las dos)."""
        for h, r in resp.items():
            ff = self._f(f)
            if self.regla == 'IND':
                for x in ff:
                    k = (x, h, r)
                    self.w[k] = self.w.get(k, 0.0) + self.eta * (rec - self.w.get(k, 0.0))
            else:
                err = rec - self.valor(f, r, h)
                for x in ff:
                    k = (x, h, r)
                    self.w[k] = self.w.get(k, 0.0) + self.eta * err


def examen(al):
    """Acierto codicioso (sin exploracion, sin aprender) en las 4 combinaciones, SIN sabia."""
    return {'%d+%d' % c: int(al.elige(feats(c[0], c[1], None), codicia=True) == correcta(*c)) for c in COMBOS}


def corre(regla, brazo, semilla, N=2000, retiro=1000, w0=None):
    rng = random.Random(semilla)
    al = Alumna(regla, rng, w=w0, cabezas=CABEZAS[TAREA])
    ac = []
    por_combo = {k: [] for k in KC}
    examen_retiro = None
    for t in range(N):
        a, b = rng.randint(0, 1), rng.randint(0, 1)
        ok = a + b
        bien = correcta(a, b)
        if brazo == 'SABIA' or (brazo == 'SABIA_RETIRO' and t < retiro):
            s = ok
        elif brazo == 'MENTIROSA':
            s = rng.choice(RESP)
        else:
            s = None
        if brazo == 'SABIA_RETIRO' and t == retiro:
            examen_retiro = examen(al)
        f = feats(a, b, s)
        r = al.elige(f)
        acierto = int(r == bien)
        al.aprende(f, r, COMIDA if acierto else VENENO)
        ac.append(acierto)
        por_combo['%d+%d' % (a, b)].append((t, acierto))
    t90 = None
    s = sum(ac[:50])
    for t in range(50, N):
        if s / 50 >= 0.85:  # techo con eps=0.1: 0.93 (CLASES), 0.90 (BITS)
            t90 = t
            break
        s += ac[t] - ac[t - 50]
    bloques = [sum(ac[i:i + 100]) / len(ac[i:i + 100]) for i in range(0, N, 100)]
    fin = {}
    for k, v in por_combo.items():
        u = [x for tt, x in v if tt >= N - 500]
        fin[k] = sum(u) / max(1, len(u))
    out = dict(regla=regla, brazo=brazo, semilla=semilla, t90=t90, bloques=bloques, combo_final=fin,
               examen_final=examen(al), w=al.w)
    if brazo == 'SABIA_RETIRO':
        out['examen_retiro'] = examen_retiro
        out['ac_pre_retiro'] = sum(ac[retiro - 100:retiro]) / 100
        out['ac_post_100'] = sum(ac[retiro:retiro + 100]) / 100
    return out


def med(x):
    x = sorted(x)
    n = len(x)
    return x[n // 2] if n % 2 else (x[n // 2 - 1] + x[n // 2]) / 2


def resumen(res, hijas):
    L = ['EXPLORATORIO, no es dato. TAREA=%s' % TAREA]
    L.append('%-5s %-13s %5s %5s %5s %6s  %-23s %s' % ('regla', 'brazo', 'b1', 'b5', 'bfin', 't85med',
                                                        'fin 00/01/10/11', 'llegan85'))
    for regla in ['RW', 'IND', 'LIN']:
        for brazo in ['SOLA', 'SABIA', 'MENTIROSA', 'SABIA_RETIRO']:
            R = [r for r in res if r['regla'] == regla and r['brazo'] == brazo]
            m = lambda i: sum(r['bloques'][i] for r in R) / len(R)
            t9 = [r['t90'] for r in R if r['t90'] is not None]
            c = [sum(r['combo_final'][k] for r in R) / len(R) for k in KC]
            L.append('%-5s %-13s %5.2f %5.2f %5.2f %6s  %-23s %d/%d' % (
                regla, brazo, m(0), m(min(4, len(R[0]['bloques']) - 1)), m(-1),
                med(t9) if t9 else '-', '/'.join('%.2f' % x for x in c), len(t9), len(R)))
            if brazo == 'SABIA_RETIRO':
                ex = [sum(r['examen_retiro'].values()) / 4 for r in R]
                L.append('      retiro: acierto 100 antes=%.2f | 100 despues=%.2f | examen sin sabia al irse=%.2f | examen final=%.2f' % (
                    sum(r['ac_pre_retiro'] for r in R) / len(R), sum(r['ac_post_100'] for r in R) / len(R),
                    sum(ex) / len(ex), sum(sum(r['examen_final'].values()) / 4 for r in R) / len(R)))
                L.append('      examen al irse por combo: ' + ' '.join(
                    '%s=%.2f' % (k, sum(r['examen_retiro'][k] for r in R) / len(R)) for k in KC))
            if brazo == 'SOLA':
                L.append('      examen final sin sabia: %.2f' % (sum(sum(r['examen_final'].values()) / 4 for r in R) / len(R)))
    for regla in ['RW', 'IND']:
        for frac in [0.0, 0.5, 1.0]:
            H = [h for h in hijas if h['regla'] == regla and h['frac'] == frac]
            L.append('HIJA %-4s hereda %.1f de la madre SOLA: acierto primeros 100=%.2f' % (
                regla, frac, sum(h['ac_100'] for h in H) / len(H)))
    return '\n'.join(L)


def main():
    global TAREA
    humo = '--humo' in sys.argv
    TAREA = 'BITS' if '--bits' in sys.argv else 'CLASES'
    semillas = list(range(7001, 7004 if humo else 7031))
    N = 400 if humo else 2000
    ret = N // 2
    res = []
    for regla in ['RW', 'IND', 'LIN']:
        for brazo in ['SOLA', 'SABIA', 'MENTIROSA', 'SABIA_RETIRO']:
            for s in semillas:
                res.append(corre(regla, brazo, s, N, ret))
    hijas = []
    for regla in ['RW', 'IND']:
        for s in semillas:
            madre = corre(regla, 'SOLA', s, N, ret)
            for frac in [0.0, 0.5, 1.0]:
                w0 = {k: v * frac for k, v in madre['w'].items()}
                h = corre(regla, 'SOLA', s + 100000, 200, 100, w0=w0)
                hijas.append(dict(regla=regla, frac=frac, semilla=s, ac_100=h['bloques'][0], t90=h['t90']))
    for r in res:
        r['w'] = None
    txt = resumen(res, hijas)
    print(txt)
    base = os.path.dirname(os.path.abspath(__file__))
    nombre = ('resultados_humo' if humo else 'resultados') + '_' + TAREA
    with open(os.path.join(base, nombre + '.json'), 'w') as fh:
        json.dump(dict(EXPLORATORIO=True, N=N, retiro=ret, semillas=semillas, res=res, hijas=hijas), fh)
    with open(os.path.join(base, nombre + '.txt'), 'w', encoding='utf-8') as fh:
        fh.write(txt + '\n')


if __name__ == '__main__':
    main()
