# EXPLORATORIO, no es dato
"""identidad_fable.py — arnes minimo del motor construido (Fable, 24-sep-2026). MISION: llegar a la AGI por este camino.

IF1: motor_fable con cambio=TUPLA (t, 'A', 'B') == motor_codigo con la misma tupla, BIT A BIT (salida entera, T corto).
IF2: motor_fable con spec 'golpe' (dict) == motor_codigo con la tupla, BIT A BIT (el spec de golpe ES el intercambio).
IF3: spec 'gradual' con dur=1 == golpe en t0+1 (el lerp llega a 1 en un paso): mismo mundo desde t0+1; ANTES de t0+1 difiere solo en t0.
IF4: tabla_en: en gradual a mitad de camino, A vale (+0.2, 0) y B (+0.2, 0); en alterna vuelve a la fabrica en el 2o periodo.
"""
import os, sys, json, hashlib
AQUI = os.path.dirname(os.path.abspath(__file__)); CODIGO = os.path.dirname(AQUI)
for d in (AQUI, CODIGO): sys.path.insert(0, d)
import corre_codigo as CC
import motor_codigo as MC
import motor_fable as MF
import fable_mundos as FB


def firma(r):
    s = json.dumps(dict(lin=[(l['deaths'], l['nacimientos'], l['tam'], l['mord']) for l in r['linajes']], eco=r['eco']['n_nac'], t_ext=r['eco']['t_ext'],
                        cod=r.get('codigo', {}).get('cod_nac')), sort_keys=True, default=str)
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def corre(mod, brazo, cambio, seed=28001, T=6000):
    eco = CC.eco_de(brazo, 4500, 2000); eco['cambio'] = cambio
    return mod.run_solapadas(seed, [CC.CARRO] * CC.MUNDO['n0'], T=T, diag=0, mundo_n=CC.MUNDO['esc'], tope_cuerpos=CC.MUNDO['tope'], muestra=CC.BASE['muestra'], eco=eco)


ok = 0; tot = 0
def chk(nombre, cond):
    global ok, tot
    tot += 1; ok += int(bool(cond)); print(('OK  ' if cond else 'MAL ') + nombre, flush=True)

for brazo in ('CODIGO', 'PERILLAS'):
    a = firma(corre(MC, brazo, (2000, 'A', 'B'))); b = firma(corre(MF, brazo, (2000, 'A', 'B'))); c = firma(corre(MF, brazo, dict(tipo='golpe', t=2000)))
    chk(f'IF1 {brazo} tupla: fable == codigo ({a})', a == b)
    chk(f'IF2 {brazo} spec golpe == tupla ({c})', a == c)
a = firma(corre(MC, 'CODIGO', (2001, 'A', 'B'))); d = firma(corre(MF, 'CODIGO', dict(tipo='gradual', t=2000, dur=1)))
chk('IF3 gradual dur=1 desde 2000 == golpe en 2001 (en 2000 el lerp es 0: fabrica)', a == d)
EF0 = {'A': (0.8, 0.0), 'B': (-0.4, 0.0), 'C': (0.0, 0.8), 'D': (0.0, -0.4)}
g = FB.tabla_en(dict(tipo='gradual', t=100, dur=1000), 600, EF0)
chk(f'IF4a gradual a mitad: A {g["A"]} B {g["B"]}', abs(g['A'][0] - 0.2) < 1e-9 and abs(g['B'][0] - 0.2) < 1e-9)
al = FB.tabla_en(dict(tipo='alterna', t=100, periodo=500), 700, EF0)
chk(f'IF4b alterna 2o periodo = fabrica {al["A"]}', al == EF0)
z = FB.efecto(dict(tipo='zona', t=0, frac=0.5), 5, EF0, 1200)
chk(f'IF4c zona: A en pos 10 {z("A", 10)}, A en pos 1000 {z("A", 1000)}', z('A', 10) == EF0['B'] and z('A', 1000) == EF0['A'])
print(f'IDENTIDAD FABLE: {ok}/{tot}')
