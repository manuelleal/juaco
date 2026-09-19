"""CREADOR A (completado por el CREADOR de relevo, 18-sep 20:40) — arnes de identidad de `organismo_vivo_relevo.py`
(perilla `memoria_pares=None`). Un proceso, sin Pool. Los kwargs de los brazos se IMPORTAN de los runners del mundo
vivo (no se copian): corre_vivo_rep2.BRAZOS (VIVO, CUELLO_MIN), mini_vivo.BRAZOS (VIVO), corre_sal.BASE/ALIAS/LIMPIAS.

IDENTIDADES (la perilla apagada tiene que ser el origen BIT A BIT, y no consumir rng)
  I1  relevo(None) == organismo_vivo_rep2, brazo VIVO (semillas 1-3)                          3
  I2  relevo(None) == organismo_vivo_rep2, brazo CUELLO_MIN (semillas 1-3)                    3
  I3  relevo(None, reproduccion=0) == organismo_vivo, brazo VIVO de mini_vivo                 3
  I4  relevo(None, vivo=0, n_nec=1) == organismo/organismo_v14 (E1 s1-2; E2 invertido s3)     3
  I4b relevo(None, vivo=0, n_nec=1) == organismo_v14 en E2I (nuevo='C') y E2L (solap_AB=3)    2
  I5  relevo(None) == organismo_vivo con corre_sal.BASE (sal muda), 9 semillas ALIAS          9
  I5b idem en 3 semillas LIMPIAS (el control del bloque de la sal)                            3
  I6  el rng no se consume: T=100000, brazo VIVO de rep2, semilla 1                           1
  I7  `invertir_vivo_en` > T (nunca dispara) es INERTE: == rep2 VIVO                          1
                                                                              identidades   28

CONTROLES QUE DEBEN FALLAR (si alguno sale IDENTICO, el arnes no mide nada y se para)
  M1  la perilla ENCENDIDA cambia la conducta: relevo('relevo') != rep2, brazo VIVO s1
  M2  v15g != v15f: relevo_boca=1 != relevo_boca=0 con la perilla ON, semilla ALIAS 326 (T fijo 20000)
  M3  `invertir_vivo_en` = T//2 SI dispara: != rep2 VIVO s1
  M4  paja del comparador: relevo(None) CUELLO_MIN != rep2 VIVO s1 (dos brazos distintos)
  M5  perilla mal escrita: memoria_pares='xxx' lanza ValueError (no cae en silencio)
                                                                              controles      5
                                                                              TOTAL         33

I8 (NO es comprobacion) la perilla ENCENDIDA en la semilla ALIAS 326: v15f y v15g-explorador contra apagada.
Uso: python identidad_vivo_relevo.py [T]        (T por defecto 20000; los controles M2/M3 usan su propio T fijo)
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
T_CTRL = 20000   # los controles M2/M3 no dependen del T de la linea de ordenes (M2 necesita que la tabla se consolide)


def N(x):
    return json.loads(json.dumps(x, default=str))


def comp(a, b):
    """Claves que difieren + claves que faltan + claves extra que NO son de la perilla nueva."""
    return ([k for k in a if k in b and N(a[k]) != N(b[k])] + [k for k in a if k not in b]
            + [k for k in b if k not in a and k not in NUEV])


def comp_par(a, b):
    """Comparador entre dos corridas del MISMO modulo (los dos llevan las claves nuevas): se ignora la perilla declarada."""
    return [k for k in a if k in b and k not in ('memoria_pares', 'relevo_boca', 'invertir_vivo_en') and N(a[k]) != N(b[k])]


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    ok = tot = 0
    ctrl_ok = ctrl_tot = 0

    def caso(etq, a, b):
        global ok, tot
        tot += 1; d = comp(a, b); ok += (not d)
        print(f'  {etq:>52}: {"IDENTICO" if not d else "DIFIERE " + str(d[:8])}', flush=True)

    def control(etq, difieren, detalle=''):
        """DEBE fallar (difieren=True significa que el control hace su trabajo)."""
        global ctrl_ok, ctrl_tot
        ctrl_tot += 1; ctrl_ok += bool(difieren)
        print(f'  {etq:>52}: {"DIFIERE (ok, el control fallo como debe)" if difieren else "*** IDENTICO — EL CONTROL NO FALLA"}'
              f'{("  " + detalle) if detalle else ""}', flush=True)

    print(f'--- I1/I2: relevo(None) == organismo_vivo_rep2 (VIVO, CUELLO_MIN), T={T} ---', flush=True)
    for b in ('VIVO', 'CUELLO_MIN'):
        kw = CR2.BRAZOS[b]
        for s in (1, 2, 3):
            caso(f'rep2 {b} s{s}', V2.run(s, T=T, **kw), VR.run(s, T=T, memoria_pares=None, **kw))
    print(f'--- I3: relevo(None, reproduccion=0) == organismo_vivo (VIVO de mini_vivo), T={T} ---', flush=True)
    for s in (1, 2, 3):
        caso(f'organismo_vivo VIVO s{s}', VV.run(s, T=T, **MV.BRAZOS['VIVO']), VR.run(s, T=T, memoria_pares=None, reproduccion=0, **MV.BRAZOS['VIVO']))
    print(f'--- I4/I4b: relevo(None, vivo=0, n_nec=1) == organismo_v14 (E1, E2, E2I, E2L), T={T} ---', flush=True)
    for etq, s, kw in (('E1', 1, dict()), ('E1', 2, dict()), ('E2', 3, dict(invertir_en=T // 2)),
                       ('E2I', 4, dict(nuevo='C')), ('E2L', 5, dict(solap_AB=3))):
        caso(f'v14.1 {etq} s{s}', V14.run(s, T=T, **kw), VR.run(s, T=T, memoria_pares=None, vivo=0, n_nec=1, **kw))
    print(f'--- I5/I5b: relevo(None) == organismo_vivo con corre_sal.BASE (9 ALIAS + 3 LIMPIAS), T={T} ---', flush=True)
    for s in CS.ALIAS:
        caso(f'sal ALIAS s{s}', VV.run(s, T=T, **CS.BASE), VR.run(s, T=T, memoria_pares=None, **CS.BASE))
    for s in CS.LIMPIAS[:3]:
        caso(f'sal LIMPIA s{s}', VV.run(s, T=T, **CS.BASE), VR.run(s, T=T, memoria_pares=None, **CS.BASE))
    print('--- I6: el rng no se consume (T=100000, rep2 VIVO s1) ---', flush=True)
    caso('rep2 VIVO s1 T=100000', V2.run(1, T=100000, **CR2.BRAZOS['VIVO']), VR.run(1, T=100000, memoria_pares=None, **CR2.BRAZOS['VIVO']))
    print(f'--- I7: `invertir_vivo_en` > T (nunca dispara) es inerte, T={T} ---', flush=True)
    caso('rep2 VIVO s1 + invertir_vivo_en=T+1', V2.run(1, T=T, **CR2.BRAZOS['VIVO']),
         VR.run(1, T=T, memoria_pares=None, invertir_vivo_en=T + 1, **CR2.BRAZOS['VIVO']))

    print(f'\nIDENTIDAD (I1-I7): {ok}/{tot}', flush=True)

    print(f'\n--- CONTROLES QUE DEBEN FALLAR (M1-M5; M2/M3 con su T fijo {T_CTRL}) ---', flush=True)
    kwV = CR2.BRAZOS['VIVO']
    base = V2.run(1, T=T, **kwV)
    control('M1 relevo ON != rep2 VIVO s1', bool(comp(base, VR.run(1, T=T, memoria_pares='relevo', **kwV))))
    a15f = VR.run(326, T=T_CTRL, **CS.BASE, memoria_pares='relevo')
    a15g = VR.run(326, T=T_CTRL, **CS.BASE, memoria_pares='relevo', relevo_boca=1)
    control('M2 v15g != v15f (ALIAS 326)', bool(comp_par(a15f, a15g)),
            f"|W[sal]| v15f {CS.resumen('M2', 326, a15f)['w_sal']} / v15g {CS.resumen('M2', 326, a15g)['w_sal']}")
    baseC = V2.run(1, T=T_CTRL, **kwV)
    control('M3 invertir_vivo_en=T//2 != rep2 VIVO s1',
            bool(comp(baseC, VR.run(1, T=T_CTRL, memoria_pares=None, invertir_vivo_en=T_CTRL // 2, **kwV))))
    control('M4 paja: CUELLO_MIN != VIVO s1', bool(comp(base, VR.run(1, T=T, memoria_pares=None, **CR2.BRAZOS['CUELLO_MIN']))))
    try:
        VR.run(1, T=100, memoria_pares='xxx', **kwV); lanzo = False; msg = 'no lanzo'
    except ValueError as e:
        lanzo = True; msg = str(e)
    control('M5 memoria_pares mal escrita lanza ValueError', lanzo, msg)

    print(f'\nCONTROLES (M1-M5): {ctrl_ok}/{ctrl_tot} fallan como deben', flush=True)
    print(f'ARNES TOTAL: {ok + ctrl_ok}/{tot + ctrl_tot}', flush=True)

    print(f'\n--- I8 (NO es comprobacion): semilla ALIAS 326, sal muda, T={T}: apagada / v15f (relevo en la lenta) / v15g (casilla antes de la puerta) ---', flush=True)
    for etq, kw in (('apagada', dict(memoria_pares=None)), ('v15f relevo', dict(memoria_pares='relevo')), ('v15g relevo_boca', dict(memoria_pares='relevo', relevo_boca=1))):
        r = VR.run(326, T=T, **CS.BASE, **kw)
        o = CS.resumen(etq, 326, r)
        print(f'  {etq:18s} |W[sal]| {o["w_sal"]} por nec {o["w_sal_por_nec"]}  W[veneno] {o["w_veneno"]} por nec {o["w_veneno_por_nec"]}  '
              f'exp sal {o["exp_sal"]} veneno {o["exp_veneno"]}  splits {o["splits"]} celdas {o["celdas"]} muertes {o["deaths"]}  '
              f'tabla {r.get("W_tabla")}  ganadora {r.get("mem_ganadora")}', flush=True)
    print('  Lo que se busca: sin excepcion; la tabla de hambre lee 0.0 en la sal y -3.0 en el veneno; v15f la sabe pero la puerta lee la rapida.')
    sys.exit(0 if (ok == tot and ctrl_ok == ctrl_tot) else 1)
