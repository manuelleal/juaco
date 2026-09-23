"""Arnes de IDENTIDAD BIT A BIT del bloque FANIN (se corre ANTES de mirar ningun numero). UN proceso, sin Pool.

A. organismo_v142_fanin(fanin=6)  ==  organismo/organismo_v142.py (TRONCO v14.2), en los 7 escenarios de identidad del
   examen (ESC_ID de bateria_v142: BUG, E1, E2, E2I, E2J, E2K, E2L), semillas 1 y 2, T = 100 000 (el del examen).
   + la instrumentacion `diag=True` es inerte (E1 y E2L, semilla 1).
B. organismo_v142g_fanin(fanin=6, mundo='regla')  ==  organismo/organismo_v142g.py con los kwargs EXACTOS de la entrada
   'organismo_v142' de bateria_generaliza_v142 (regla 14, leidos del archivo congelado), reglas px0 / azar / xor01,
   semillas 1 y 2, T = 200 000 (el de la bateria). + `diag=True` inerte (px0, semilla 1).
Se comparan TODAS las claves de la referencia con `!=` (como el criterio 5 del examen); la copia solo puede agregar
`fanin` y `diag_fanin`. Si algo difiere: el instrumento no es el que dice ser y no se corre nada.

    python experimentos/nivel07_fanin_expansion/identidad_fanin.py      (escribe identidad_fanin_salida.txt)
"""
import sys, os, time, hashlib, importlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
sys.path[:0] = [AQUI, ORG]
import numpy as np

_f = open(os.path.join(AQUI, 'identidad_fanin_salida.txt'), 'w', encoding='utf-8', newline='\n')
_t0 = time.time()


def log(m=''):
    l = f"[{time.strftime('%H:%M:%S')} +{time.time()-_t0:6.1f}s] {m}"
    print(l, flush=True); _f.write(l + '\n'); _f.flush()


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


EXTRA = {'fanin', 'diag_fanin'}


def compara(a, b):
    dif = [k for k in a if k not in b or a[k] != b[k]]
    sobra = sorted(set(b) - set(a) - EXTRA)
    return dif, sobra


def main():
    import organismo_v142 as ref, organismo_v142_fanin as cop
    import organismo_v142g as refg, organismo_v142g_fanin as copg
    bg = importlib.import_module('bateria_generaliza_v142')   # congelada: solo se lee la entrada del tronco
    KWT = dict(bg.INSTRUMENTOS['organismo_v142'][1])
    log('=== IDENTIDAD FANIN (fanin=6 == tronco, bit a bit) ===')
    for n, d in (('organismo_v142.py', ORG), ('organismo_v142g.py', ORG), ('bateria_generaliza_v142.py', ORG),
                 ('organismo_v142_fanin.py', AQUI), ('organismo_v142g_fanin.py', AQUI), ('identidad_fanin.py', AQUI)):
        log(f'  sha {h16(os.path.join(d, n))}  {n}')
    log(f'  numpy {np.__version__}  python {sys.version.split()[0]}')
    log(f'  kwargs del tronco (bateria_generaliza_v142, entrada organismo_v142): {KWT}')
    ESC = {'BUG': dict(plast=False, solap_AB=3), 'E1': dict(), 'E2': dict(invertir_en=50000),
           'E2I': dict(nuevo='C'), 'E2J': dict(nuevo='D', nuevo_val='comida', solap_B=1),
           'E2K': dict(nuevo='D', nuevo_val='comida', solap_B=2), 'E2L': dict(solap_AB=3)}
    ok = 0; tot = 0
    log('A. organismo_v142_fanin(fanin=6) vs organismo_v142, T=100000')
    casos = [(e, s, False) for e in ESC for s in (1, 2)] + [('E1', 1, True), ('E2L', 1, True)]
    for e, s, dg in casos:
        a = ref.run(s, **ESC[e]); b = cop.run(s, fanin=6, diag=dg, **ESC[e])
        dif, sobra = compara(a, b); bien = not dif and not sobra; ok += bien; tot += 1
        log(f'  {"IDENTICO" if bien else "DIFIERE "} {e:4s} semilla {s} diag={dg!s:5s} claves {len(a)}'
            f'  splits {a["splits"]}/{b["splits"]}  W {a["W"]}' + (f'  DIFIEREN {dif} SOBRAN {sobra}' if not bien else ''))
    log('B. organismo_v142g_fanin(fanin=6) vs organismo_v142g, mundo de regla, T=200000, kwargs del tronco')
    casos = [(rg, s, False) for rg in ('px0', 'azar', 'xor01') for s in (1, 2)] + [('px0', 1, True)]
    for rg, s, dg in casos:
        a = refg.run(s, T=200000, mundo='regla', regla=rg, **KWT); b = copg.run(s, T=200000, mundo='regla', regla=rg, fanin=6, diag=dg, **KWT)
        dif, sobra = compara(a, b); bien = not dif and not sobra; ok += bien; tot += 1
        log(f'  {"IDENTICO" if bien else "DIFIERE "} {rg:5s} semilla {s} diag={dg!s:5s} claves {len(a)}'
            f'  splits {a["splits"]}/{b["splits"]}  W_apriori[0:3] {list(a["W_apriori"].values())[:3]}' + (f'  DIFIEREN {dif} SOBRAN {sobra}' if not bien else ''))
    log()
    log(f'IDENTIDAD {ok}/{tot} {"-- TODO IDENTICO: fanin=6 es el tronco bit a bit (y diag es inerte)" if ok == tot else "-- *** FALLA: no se corre nada"}')
    _f.close()
    sys.exit(0 if ok == tot else 1)


if __name__ == '__main__':
    main()
