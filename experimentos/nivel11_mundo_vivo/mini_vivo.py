"""Mini-prueba del MUNDO VIVO (nivel 11) — UN proceso, sin Pool (regla 3 de EQUIPO.md), 3 semillas, T <= 100000.
No es un bloque preregistrado: es el humo que dice si lo que el mundo vivo PROMETE se ve, y con que numeros
escribir las predicciones del bloque real (PREREGISTRO_mundo_vivo.md, que se escribe ANTES de correr esto).

Mide las tres cosas que el mundo vivo promete:
  (a) EXPOSICIONES HASTA CRITERIO por estimulo y por necesidad (`exp_hasta`): cada encuentro, ¿informa a las DOS
      necesidades? La celda cruzada ("la comida no quita la sed") se aprende con la MISMA mordida.
  (b) El XOR natural NECESIDAD x ESTIMULO: el agua vale con sed y no sin sed. Dos lecturas:
        xor01  = acierto balanceado del signo del VALOR en las 4 celdas {hambre,sed} x {A,C} contra (1,0,0,1)
        contraste = diferencia de TASA DE MORDIDA de la misma imagen entre las dos necesidades (conducta)
      La verdad (1,0,0,1) no es representable como a_necesidad + b_estimulo: es XOR (paridad), no un sesgo.
  (c) SUPERVIVENCIA con DOS muertes posibles (`muertes_nec` = [por energia, por agua]).

Brazos (un cambio por brazo):
  VIVO        2 necesidades, 4 estimulos                          (el mundo vivo)
  UNA_NEC     el MISMO cuerpo (dos drenajes, dos muertes) con UNA necesidad en la MENTE   -> que compra la 2a necesidad
  ESCALAR     2 necesidades pero UN solo valor por celda (val_esc=1): la necesidad solo como contexto del impulso
              -> es la alternativa que el encargo pide argumentar; aqui puede ganar y refutar el diseno
  BARAJADA    la necesidad que indexa la memoria se sortea (rng propio): el control que debe destruirlo
  NO_INFORMA  la sal no informa a nadie (dE=dAg=0): el estimulo sin consecuencia no debe aprenderse nunca

Presupuesto del cuerpo (decidido ANTES de correr, con argumento, no por barrido): v14 gasta `costo`=0.002 por paso
en UN eje y la mitad de los objetos son comida. Con dos ejes y cuatro estimulos, la comida baja al 25 %. Para no
confundir "el mundo vivo no funciona" con "el mundo vivo mata de hambre", se CONSERVA el gasto total del cuerpo y
se reparte: costo = costo_a = 0.001. Es la unica constante que se mueve respecto del tronco y se declara aqui.

Uso:  python experimentos/nivel11_mundo_vivo/mini_vivo.py [--T 100000] [--sem 1 2 3]
Salida: mini_vivo_salida.json en esta carpeta + tabla por pantalla (linea por brazo con marca de tiempo, regla 10).
"""
import argparse, hashlib, json, os, statistics, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_vivo as VV

EST = ('A', 'B', 'C', 'D')          # comida, veneno, agua, sal
IDX = {k: i for i, k in enumerate(EST)}
CUERPO = dict(vivo=1, estims=EST, costo=0.001, costo_a=0.001)
SAL_MUDA = {'comida': (+0.8, 0.0), 'veneno': (-0.4, 0.0), 'agua': (0.0, +0.8), 'sal': (0.0, 0.0)}
BRAZOS = {
    'VIVO':       dict(CUERPO, n_nec=2),
    'UNA_NEC':    dict(CUERPO, n_nec=1),
    'ESCALAR':    dict(CUERPO, n_nec=2, val_esc=1),
    'BARAJA_POL': dict(CUERPO, n_nec=2, nec_shuf=1),
    'BARAJA_CON': dict(CUERPO, n_nec=2, nec_shuf=2),
    'NO_INFORMA': dict(CUERPO, n_nec=2, tabla=SAL_MUDA),
}
# celdas informativas (necesidad, estimulo) del mundo vivo, y el signo que la fisica del mundo obliga
INFORM = [(0, 'A', +1), (0, 'B', -1), (1, 'C', +1), (1, 'D', -1)]
# las cuatro celdas del XOR: {hambre,sed} x {comida,agua}; verdad = morder? (1,0,0,1)
XOR = [(0, 'A', 1), (0, 'C', 0), (1, 'A', 0), (1, 'C', 1)]
UMB = 0.3   # "vale la pena morder" = valor > +0.3 (declarado antes de correr)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.median(xs), 2) if xs else None


def lee(r, kw):
    """Todas las medidas del brazo, a partir de UNA corrida. `kw` dice que fila LEE la boca: con val_esc=1 la
    boca lee SIEMPRE la fila 0 (la necesidad es solo contexto del impulso), aunque las otras filas existan."""
    n = r['n_nec']
    fila = (lambda nn: 0) if kw.get('val_esc') else (lambda nn: nn)
    W = [r['W_nec'][fila(i)] for i in range(n)]
    o = dict(deaths=r['deaths'], muertes_nec=r['muertes_nec'], celdas=r['celdas'], splits=r['splits'],
             exposiciones=r['exposiciones'], W_nec=W, exp_hasta=r['exp_hasta'])
    # (a) exposiciones hasta criterio, celda a celda + la tabla completa
    o['exp_celda'] = {f'{nn}x{s}': (r['exp_hasta'][fila(nn)][s] if nn < n else None) for nn, s, _ in INFORM}
    hechas = [v for v in o['exp_celda'].values() if v is not None]
    o['exp_tabla'] = max(hechas) if len(hechas) == len(INFORM) else None   # None = tabla incompleta (censurada)
    o['celdas_ok'] = len(hechas)
    # (b) XOR necesidad x estimulo, por valor y por conducta
    acc = []
    for nn, s, v in XOR:
        w = W[nn][s] if nn < n else W[0][s]
        acc.append(int((1 if w > UMB else 0) == v))
    o['xor01'] = round((acc[0] + acc[3]) / 2 * 0.5 + (acc[1] + acc[2]) / 2 * 0.5, 3)   # balanceado: 2 positivos, 2 negativos
    o['xor_celdas'] = {f'{nn}x{s}': (round(W[nn][s], 2) if nn < n else round(W[0][s], 2)) for nn, s, _ in XOR}
    tasa = {}
    for nn in range(n):
        for s in ('A', 'C'):
            e = r['xor_enc'][nn][IDX[s]]
            tasa[f'{nn}x{s}'] = round(r['xor_mord'][nn][IDX[s]] / e, 3) if e >= 20 else None
    o['tasa'] = tasa
    if n > 1 and all(tasa.get(k) is not None for k in ('0xA', '1xA', '0xC', '1xC')):
        o['contraste'] = round(((tasa['1xC'] - tasa['0xC']) + (tasa['0xA'] - tasa['1xA'])) / 2, 3)
    else:
        o['contraste'] = None
    return o


def resume(rs):
    o = {}
    for k in ('deaths', 'celdas', 'splits', 'xor01', 'contraste', 'exp_tabla', 'celdas_ok'):
        o[k] = med([r[k] for r in rs])
    o['muertes_nec'] = [med([r['muertes_nec'][i] for r in rs]) for i in range(2)]
    o['exp_celda'] = {k: med([r['exp_celda'][k] for r in rs]) for k in rs[0]['exp_celda']}
    o['cens_celda'] = {k: sum(r['exp_celda'][k] is None for r in rs) for k in rs[0]['exp_celda']}
    o['xor_celdas'] = {k: med([r['xor_celdas'][k] for r in rs]) for k in rs[0]['xor_celdas']}
    o['tasa'] = {k: med([r['tasa'].get(k) for r in rs]) for k in rs[0]['tasa']}
    o['exposiciones'] = {k: med([r['exposiciones'][k] for r in rs]) for k in EST}
    return o


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--T', type=int, default=100000)
    ap.add_argument('--sem', type=int, nargs='+', default=[1, 2, 3])
    a = ap.parse_args()
    t0 = time.time()
    print(f"  sha organismo_v14 (tronco) {h16(os.path.join(RAIZ,'organismo','organismo_v14.py'))}   "
          f"organismo_vivo {h16(os.path.join(AQUI,'organismo_vivo.py'))}   "
          f"mini_vivo {h16(os.path.abspath(__file__))}")
    print(f"  T = {a.T}, semillas {a.sem}, UN proceso, sin Pool\n", flush=True)

    # ancla dentro del runner (convencion del repo): con 1 necesidad y 2 estimulos, esto ES v14
    anc = sum(V14.run(s, T=20000) == {k: v for k, v in VV.run(s, T=20000, vivo=1, n_nec=1, estims=('A', 'B'),
                                                              costo_a=0.0).items()
                                      if k in V14.run(s, T=20000)} for s in a.sem[:2])
    print(f"  [{time.time()-t0:6.1f}s] ancla dentro del runner (1 necesidad, 2 estimulos == v14): "
          f"{anc}/{len(a.sem[:2])}\n", flush=True)
    if anc != len(a.sem[:2]):
        raise SystemExit('ANCLA ROTA: no se corre nada.')

    salida = {'T': a.T, 'sem': a.sem, 'umbral_morder': UMB, 'brazos': {}, 'crudo': {},
              'brazos_kw': {k: {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in v.items()}
                            for k, v in BRAZOS.items()}}
    for nom, kw in BRAZOS.items():
        rs = []
        for s in a.sem:
            rs.append(lee(VV.run(s, T=a.T, **kw), kw))
        salida['brazos'][nom] = resume(rs)
        salida['crudo'][nom] = rs
        r = salida['brazos'][nom]
        print(f"  [{time.time()-t0:6.1f}s] {nom:11s} xor01 {str(r['xor01']):5s}  contraste {str(r['contraste']):6s}  "
              f"exp_tabla {str(r['exp_tabla']):6s} ({r['celdas_ok']}/4 celdas)  muertes {str(r['deaths']):6s} "
              f"{r['muertes_nec']}  celdas {r['celdas']}", flush=True)

    d = os.path.join(AQUI, 'mini_vivo_salida.json')
    json.dump(salida, open(d, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"\n  escrito {d}")

    print("\n(a) EXPOSICIONES HASTA CRITERIO por celda (necesidad x estimulo; mediana de 3; * = censuradas)")
    print(f"  {'brazo':11s} " + ' '.join(f"{k:>9s}" for k in salida['brazos']['VIVO']['exp_celda']) + "   exposiciones A/B/C/D")
    for nom in BRAZOS:
        r = salida['brazos'][nom]
        cel = ' '.join(f"{str(r['exp_celda'][k]) + ('*' * r['cens_celda'][k]):>9s}" for k in r['exp_celda'])
        print(f"  {nom:11s} {cel}   " + '/'.join(str(r['exposiciones'][k]) for k in EST))

    print("\n(b) XOR necesidad x estimulo — VALOR de las 4 celdas y TASA DE MORDIDA (mediana de 3)")
    print(f"  {'brazo':11s} {'xor01':>6s} " + ' '.join(f"W[{k}]".rjust(9) for k in salida['brazos']['VIVO']['xor_celdas'])
          + "  " + ' '.join(f"t[{k}]".rjust(8) for k in salida['brazos']['VIVO']['tasa']) + "  contraste")
    for nom in BRAZOS:
        r = salida['brazos'][nom]
        print(f"  {nom:11s} {str(r['xor01']):>6s} " + ' '.join(f"{str(r['xor_celdas'][k]):>9s}" for k in r['xor_celdas'])
              + "  " + ' '.join(f"{str(r['tasa'].get(k)):>8s}" for k in r['tasa']) + f"  {r['contraste']}")

    print("\n(c) SUPERVIVENCIA con dos muertes posibles (mediana de 3)")
    for nom in BRAZOS:
        r = salida['brazos'][nom]
        print(f"  {nom:11s} muertes {str(r['deaths']):>6s}  [energia {r['muertes_nec'][0]}, agua {r['muertes_nec'][1]}]"
              f"  celdas {r['celdas']}  divisiones {r['splits']}")
    print(f"\n  total {time.time()-t0:.1f} s")
