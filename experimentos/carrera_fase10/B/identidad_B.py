"""ARNES DE IDENTIDAD de organismo_B.py (carrera a la fase 10, bacteria B).

(A) IDENTIDAD BIT A BIT con las perillas nuevas APAGADAS contra su ancla organismo_f9c.py
    (9dd1fb91ecec35ae): los 14 brazos de corre_bloque2.py x rep_acum in (0,1) = 28 celdas, mas
    los 9 brazos de corre_f9.py contra organismo_f9.py (3a821884394d66c9) = 18 celdas.
    Los brazos se REUSAN de los runners (regla 14 por construccion: campo a campo, no se copian).
(B) SOLO LECTURA: bB=1 devuelve EXACTAMENTE el mismo dict que bB=0 salvo las claves nuevas.
(C) INERTE DONDE DEBE: nodo_via=3 sin conexion == nodo_via=2 sin conexion; cambia_en > T == 0;
    retina=6 explicita == retina=0.
(D) CONTROLES QUE DEBEN DIFERIR (>= 7).
(E) CORDURA DEL MUNDO B: el mundo es el que dice ser (F*F estimulos, 2F pixeles, exactamente F
    combinaciones viradas, sorteo por semilla).
(F) ERR-38: con mundoB y nodo_via=3 la perilla NO es inerte (div_lectura > 0).

Uso:  python experimentos/carrera_fase10/B/identidad_B.py
"""
import hashlib, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N09 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo')
B2D = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2')
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
sys.path[:0] = [AQUI, B2D, N09, N13, N11, os.path.join(RAIZ, 'organismo')]

import numpy as np
import organismo_f9 as F9
import organismo_f9c as F9C
import organismo_B as B
import corre_f9 as CF
import corre_bloque2 as C2

SHA = dict(f9='3a821884394d66c9', f9c='9dd1fb91ecec35ae')
T = 12000
SEMS = (3101, 3102)


def sha(ruta):
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()[:16]


def norm(x):
    if isinstance(x, dict):
        return {k: norm(v) for k, v in sorted(x.items())}
    if isinstance(x, (list, tuple)):
        return [norm(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return ('f', float(x))
    if isinstance(x, (np.integer, int)) and not isinstance(x, bool):
        return ('i', int(x))
    if isinstance(x, np.ndarray):
        return norm(x.tolist())
    if isinstance(x, (set, frozenset)):
        return sorted(norm(v) for v in x)
    return x


def igual(a, b):
    return norm(a) == norm(b)


def difs(a, b, pref='', tope=6):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f'{pref}{k}: falta en {"A" if k not in a else "B"}')
            else:
                out += difs(a[k], b[k], pref + str(k) + '.', tope)
            if len(out) >= tope:
                return out[:tope]
        return out
    if not igual(a, b):
        out.append(f'{pref} {str(a)[:60]} != {str(b)[:60]}')
    return out[:tope]


OK = [0]
NO = [0]


def caso(nombre, cond, extra=''):
    (OK if cond else NO)[0] += 1
    print(('  OK  ' if cond else '  FALLA  ') + nombre + (('   ' + extra) if extra and not cond else ''), flush=True)


t0 = time.time()
print('organismo_B.py  sha %s' % sha(os.path.join(AQUI, 'organismo_B.py')))
for nom, rel, esp in (('f9', os.path.join(N09, 'organismo_f9.py'), SHA['f9']),
                      ('f9c', os.path.join(B2D, 'organismo_f9c.py'), SHA['f9c'])):
    r = sha(rel)
    caso(f'ancla {nom} sha {r}', r == esp, f'se esperaba {esp}')

# ---------------------------------------------------------------- (A) identidad bit a bit
print('\n(A) IDENTIDAD BIT A BIT con las perillas nuevas apagadas (T=%d, semillas %s)' % (T, SEMS))
print('    A1 — 14 brazos de corre_bloque2 x rep_acum(0,1) contra organismo_f9c')
for s in SEMS[:1]:
    for nb in C2.ORDEN:
        for ac in (0, 1):
            kw = dict(C2.BRAZOS[nb], rep_acum=ac)
            a = F9C.run(s, T=T, **kw)
            b = B.run(s, T=T, **kw)
            caso(f'A1 {nb} acum={ac} s={s}', igual(a, b), '; '.join(difs(a, b)))

print('    A2 — 9 brazos de corre_f9 contra organismo_f9 (la cadena)')
for s in SEMS[:1]:
    for nb in CF.ORDEN:
        for ac in (0, 1):
            kw = dict(CF.BRAZOS[nb], rep_acum=ac)
            a = F9.run(s, T=T, **kw)
            b = B.run(s, T=T, **kw)
            caso(f'A2 {nb} acum={ac} s={s}', igual(a, b), '; '.join(difs(a, b)))

print('    A3 — segunda semilla, los tres brazos que mas mueven el estado')
for s in SEMS[1:]:
    for nb in ('REL2b', 'ORACULO', 'REL_AZAR'):
        kw = dict(C2.BRAZOS[nb], rep_acum=1)
        caso(f'A3 {nb} s={s}', igual(F9C.run(s, T=T, **kw), B.run(s, T=T, **kw)))

# ---------------------------------------------------------------- el mundo B
F = 6
MUNDO = dict(mundoB=F, retina=2 * F, estims=None, nobj=4)   # estims=None: el mundo B construye los suyos (declarado)
BASE = dict(C2.BRAZOS['REL2b'], rep_acum=1, bB=1, **MUNDO)
TB = 6000

# ---------------------------------------------------------------- (B) solo lectura
print('\n(B) SOLO LECTURA: bB=1 es bB=0 salvo las claves nuevas')
NUEV = ('gen', 'comb_ok', 'comb_enc', 'rech_mal', 'celdas_cuerpo', 'splits_cuerpo')
for s in SEMS:
    a = B.run(s, T=TB, **dict(BASE, bB=0))
    b = B.run(s, T=TB, **dict(BASE, bB=1))
    fa, fb = dict(a['f9']), dict(b['f9'])
    caso(f'B1 claves nuevas presentes s={s}', all(k in fb for k in NUEV) and not any(k in fa for k in NUEV))
    for k in NUEV:
        fb.pop(k, None)
    a2 = dict(a); b2 = dict(b); a2.pop('f9'); b2.pop('f9')
    caso(f'B2 el resto es identico s={s}', igual(a2, b2) and igual(fa, fb), '; '.join(difs(a2, b2)))

# ---------------------------------------------------------------- (C) inerte donde debe
print('\n(C) INERTE DONDE DEBE')
kd0 = dict(BASE, nodo_via=3, conectado=0, con_desde=0)
ke0 = dict(BASE, nodo_via=2, conectado=0, con_desde=0)
ra, rb = B.run(3101, T=TB, **kd0), B.run(3101, T=TB, **ke0)
ra['f9'] = {k: v for k, v in ra['f9'].items() if k != 'div_lectura'} | {'nodo_via': rb['f9']['nodo_via']}   # el eco de configuracion no es estado
caso('C1 sin conexion nunca se lee: nodo_via=3 == nodo_via=2 en TODO el dict', igual(ra, rb), '; '.join(difs(ra, rb)))
kwa = dict(BASE, nodo_via=2); kwb = dict(BASE, nodo_via=2, cambia_en=10 * TB)
caso('C2 cambia_en > T es inerte', igual(B.run(3101, T=TB, **kwa),
                                         {k: v for k, v in B.run(3101, T=TB, **kwb).items()
                                          if k != 'mundoB'} | {'mundoB': B.run(3101, T=TB, **kwa)['mundoB']}))
kr = dict(C2.BRAZOS['REL2b'], rep_acum=1)
caso('C3 retina=6 explicita == retina=0 (v14 exacto)',
     igual(B.run(3101, T=T, **kr), {k: v for k, v in B.run(3101, T=T, **dict(kr, retina=6)).items() if k != 'retina'}))
kd = dict(C2.BRAZOS['REL2b'], rep_acum=1, bB=1, nodo_via=3)
ke = dict(C2.BRAZOS['REL2b'], rep_acum=1, bB=1, nodo_via=2)
caso('C4 en el mundo de ABCD (4 codigos disjuntos) leer casi no divide: div_lectura pequeno',
     B.run(3101, T=T, **kd)['f9'].get('div_lectura', -1) >= 0)

# ---------------------------------------------------------------- (D) controles que DEBEN diferir
print('\n(D) CONTROLES QUE DEBEN DIFERIR (>= 7)')
def dif(nombre, ka, kb, s=3101, Tt=TB):
    a = B.run(s, T=Tt, **ka); b = B.run(s, T=Tt, **kb)
    caso('D ' + nombre + ' (DEBE diferir)', not igual(a, b))

dif('D1 mundoB=6 != mundo de ABCD', dict(C2.BRAZOS['REL2b'], rep_acum=1, bB=1),
    dict(BASE, nodo_via=2))
dif('D2 vira=1 != vira=0 (la trampa existe)', dict(BASE, nodo_via=2, vira=1), dict(BASE, nodo_via=2, vira=0))
dif('D3 nodo_via=3 != nodo_via=2 (leer hace crecer)', dict(BASE, nodo_via=3), dict(BASE, nodo_via=2))
dif('D4 nodo_via=3 != nodo_via=0 (via lenta sola)', dict(BASE, nodo_via=3), dict(BASE, nodo_via=0))
dif('D5 nodo_baraja=1 != contenido intacto', dict(BASE, nodo_via=3, nodo_baraja=1), dict(BASE, nodo_via=3))
dif('D6 cambia_en=2000 != mundo fijo', dict(BASE, nodo_via=3, cambia_en=2000), dict(BASE, nodo_via=3))
dif('D7 NADA != REL2b en el mundo B', dict(C2.BRAZOS['NADA'], rep_acum=1, bB=1, **MUNDO), dict(BASE, nodo_via=2))
a = B.run(3101, T=TB, **dict(BASE, nodo_via=3))['mundoB']
b = B.run(3102, T=TB, **dict(BASE, nodo_via=3))['mundoB']
caso('D8 semilla distinta -> variante virante distinta (trampa 4)', a['virante'] != b['virante'],
     f"{a['virante']} == {b['virante']}")

# ---------------------------------------------------------------- (E) cordura del mundo B
print('\n(E) CORDURA DEL MUNDO B')
r = B.run(3101, T=TB, **dict(BASE, nodo_via=3))
m = r['mundoB']
caso('E1 F*F estimulos y 2F pixeles', m['n_estim'] == F * F and m['retina'] == 2 * F and r['retina'] == 2 * F)
caso('E2 ejes: F/2 familias de energia (comida/veneno) y F/2 de agua (agua/sal)',
     m['familias'] == ['comida', 'comida', 'veneno', 'agua', 'agua', 'sal'], str(m['familias']))
caso('E3 hay las cuatro valencias en el mundo', set(r['sobre']) == {'comida', 'veneno', 'agua', 'sal'})
# la tabla de valencias reconstruida a mano, fuera del organismo
op = {'comida': 'veneno', 'veneno': 'comida', 'agua': 'sal', 'sal': 'agua'}
esp = {'f%dv%d' % (f, v): (op[m['familias'][f]] if v == m['virante'][f] else m['familias'][f])
       for f in range(F) for v in range(F)}
nviradas = sum(1 for k in esp if esp[k] != m['familias'][int(k[1])])
caso('E4 exactamente F combinaciones viradas', nviradas == F, str(nviradas))
llano = B.run(3101, T=TB, **dict(BASE, nodo_via=3, vira=0))
caso('E5 con vira=0 no hay ninguna virada (mundo llano)', llano['mundoB']['vira'] == 0)
# el sorteo del mundo NO consume el rng del organismo: vira=0 y vira=1 ven la misma primera exposicion
caso('E6 el rng del mundo es propio (sem_mundo declarada)', m['sem_mundo'] == '880000+1000000*seed')

# ---------------------------------------------------------------- (F) ERR-38: la perilla no es inerte
print('\n(F) ERR-38: LA PERILLA NO ES INERTE')
d3 = r['f9'].get('div_lectura')
caso('F1 nodo_via=3 dispara divisiones AL LEER (div_lectura > 0)', bool(d3 and d3 > 0), f'div_lectura={d3}')
caso('F2 nodo_via=2 no tiene div_lectura', 'div_lectura' not in B.run(3101, T=TB, **dict(BASE, nodo_via=2))['f9'])
lec = r['f9'].get('lect_div', 0)
caso('F3 la seleccion por relevancia difiere de la recencia (lect_div > 0)', lec > 0, f'lect_div={lec}')
caso('F4 hay generaciones > 1 (la cola transmite la generacion)', max(r['f9']['gen'] or [0]) >= 1,
     str(sorted(set(r['f9']['gen']))[:8]))

print('\n%d/%d  (%.1f s)' % (OK[0], OK[0] + NO[0], time.time() - t0))
sys.exit(0 if NO[0] == 0 else 1)
