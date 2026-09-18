"""CREADOR A — arnes de identidad de `organismo_vivo_relevo.py` (perilla `memoria_pares=None`). Un proceso, sin Pool.
Los kwargs de los brazos se IMPORTAN de los runners del mundo vivo (no se copian): corre_vivo_rep2.BRAZOS (VIVO, CUELLO_MIN),
mini_vivo.BRAZOS (VIVO), corre_sal.BASE y corre_sal.ALIAS.

I1  relevo(None) == organismo_vivo_rep2 en el brazo VIVO (T=20000, semillas 1-3)            3
I2  relevo(None) == organismo_vivo_rep2 en el brazo CUELLO_MIN                               3
I3  relevo(None, reproduccion=0) == organismo_vivo en el brazo VIVO de mini_vivo              3
I4  relevo(None, vivo=0, n_nec=1) == organismo/organismo_v14 (E1 s1-2; E2 invertido s3)      3
I5  relevo(None) == organismo_vivo con corre_sal.BASE (sal muda) en las 9 semillas ALIAS     9
I6  el rng no se consume: T=100000, brazo VIVO de rep2, semilla 1                            1
                                                                                     total 22
I7  (NO es identidad) la perilla ENCENDIDA en la semilla ALIAS 326 (T=20000): v15f y v15g-explorador contra apagada.
Uso: python identidad_vivo_relevo.py [T]
"""
import sys, os, json
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
VIVO = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), VIVO, AQUI]   # organismo/ PRIMERO (ERR-28)
import organismo_v14 as V14
import organismo_vivo as VV
import organismo_vivo_rep2 as V2
import organismo_vivo_relevo as VR
import mini_vivo as MV
import corre_vivo_rep2 as CR2
import corre_sal as CS

NUEV = {'memoria_pares', 'relevo_boca', 'invertir_vivo_en', 'mem_ganadora', 'W_tabla', 'mem_vistas'}


def N(x):
    return json.loads(json.dumps(x, default=str))


def comp(a, b):
    return ([k for k in a if k in b and N(a[k]) != N(b[k])] + [k for k in a if k not in b]
            + [k for k in b if k not in a and k not in NUEV])


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    ok = tot = 0
    def caso(etq, a, b):
        global ok, tot
        tot += 1; d = comp(a, b); ok += (not d)
        print(f'  {etq:>52}: {"IDENTICO" if not d else "DIFIERE " + str(d[:8])}', flush=True)
    print(f'--- I1/I2: relevo(None) == organismo_vivo_rep2 (VIVO, CUELLO_MIN), T={T} ---', flush=True)
    for b in ('VIVO', 'CUELLO_MIN'):
        kw = CR2.BRAZOS[b]
        for s in (1, 2, 3):
            caso(f'rep2 {b} s{s}', V2.run(s, T=T, **kw), VR.run(s, T=T, memoria_pares=None, **kw))
    print(f'--- I3: relevo(None, reproduccion=0) == organismo_vivo (VIVO de mini_vivo), T={T} ---', flush=True)
    for s in (1, 2, 3):
        caso(f'organismo_vivo VIVO s{s}', VV.run(s, T=T, **MV.BRAZOS['VIVO']), VR.run(s, T=T, memoria_pares=None, reproduccion=0, **MV.BRAZOS['VIVO']))
    print(f'--- I4: relevo(None, vivo=0, n_nec=1) == organismo_v14 (E1, E2), T={T} ---', flush=True)
    for s, kw in ((1, dict()), (2, dict()), (3, dict(invertir_en=T // 2))):
        caso(f'v14.1 {"E2" if kw else "E1"} s{s}', V14.run(s, T=T, **kw), VR.run(s, T=T, memoria_pares=None, vivo=0, n_nec=1, **kw))
    print(f'--- I5: relevo(None) == organismo_vivo con corre_sal.BASE en las 9 ALIAS, T={T} ---', flush=True)
    for s in CS.ALIAS:
        caso(f'sal ALIAS s{s}', VV.run(s, T=T, **CS.BASE), VR.run(s, T=T, memoria_pares=None, **CS.BASE))
    print('--- I6: el rng no se consume (T=100000, rep2 VIVO s1) ---', flush=True)
    caso('rep2 VIVO s1 T=100000', V2.run(1, T=100000, **CR2.BRAZOS['VIVO']), VR.run(1, T=100000, memoria_pares=None, **CR2.BRAZOS['VIVO']))
    print(f'\nIDENTIDAD (I1-I6): {ok}/{tot}', flush=True)

    print(f'\n--- I7 (NO es identidad): semilla ALIAS 326, sal muda, T={T}: apagada / v15f (relevo en la lenta) / v15g (casilla antes de la puerta) ---', flush=True)
    for etq, kw in (('apagada', dict(memoria_pares=None)), ('v15f relevo', dict(memoria_pares='relevo')), ('v15g relevo_boca', dict(memoria_pares='relevo', relevo_boca=1))):
        r = VR.run(326, T=T, **CS.BASE, **kw)
        o = CS.resumen(etq, 326, r)
        print(f'  {etq:18s} |W[sal]| {o["w_sal"]} por nec {o["w_sal_por_nec"]}  W[veneno] {o["w_veneno"]} por nec {o["w_veneno_por_nec"]}  '
              f'exp sal {o["exp_sal"]} veneno {o["exp_veneno"]}  splits {o["splits"]} celdas {o["celdas"]} muertes {o["deaths"]}  '
              f'tabla {r.get("W_tabla")}  ganadora {r.get("mem_ganadora")}', flush=True)
    print('  Lo que se busca: sin excepcion; la tabla de hambre lee 0.0 en la sal y -3.0 en el veneno; v15f la sabe pero la puerta lee la rapida.')
