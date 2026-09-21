"""corre_b21_lectura.py -- MINI-PRUEBA de UN PROCESO del creador B (junta del 21-sep-2026), Q2.

QUE HACE
  Corre el instrumento `organismo_familias_bav.py` **SIN TOCAR NI UNA LINEA** (copia BYTE A BYTE en esta
  carpeta, sha verificado contra el origen preregistrado `2dca0a3e239481f0`) en el brazo PAR de la celda
  `BA-v`, y luego **reimplementa FUERA** las reglas de lectura y las compara **SOBRE LA MISMA TABLA**
  (`mem_tabla`, `mem_visto`, `tipo_gan_forma`, `tipo_gan_var`), que es el metodo que el creador B dejo escrito
  en la bitacora de la junta de la fase 5 ("las reglas de lectura se comparan sobre el mismo estado").

  Regla medida hoy (la del candidato que corrio):   DENTRO del tipo = SUMA   ·  ENTRE tipos = min
  Reglas comparadas (nunca medidas, ERR-88 dice literalmente que `dentro` era codigo muerto):
        MIN     DENTRO del tipo = min de las casillas conocidas        · ENTRE tipos = min
        MINESC  DENTRO del tipo = (n conocidas) x min  (escala de k=3)  · ENTRE tipos = min

  CONTROL DE VACUIDAD DEL PROPIO ANALISIS: la regla SUMA reimplementada fuera tiene que coincidir con
  `W_tabla` (calculada DENTRO del organismo) en los 32 estimulos, semilla a semilla. Si no coincide, el
  script se para y no escribe veredicto ninguno.

COSTE DECLARADO (regla 3): UN proceso, sin Pool. 3 semillas x (1 emisor + 1 receptor) = **6 corridas** de
  **33 000 pasos** = 198 000 pasos <= 200 000. Semillas 913, 914, 915 (banda de humo 901-920; 901-903 las uso
  la junta, 912 el humo de BA-v; NINGUNA de 821-900 ni de 921-1000).

LO QUE ESTO **NO** DICE: conducta. Con n = 3 y T = 33 000 las lineas base NO se reproducen (leccion registrada
  del propio creador B). Esto decide MECANISMO (que leeria cada regla para el referente, la hermana y el otro
  token sobre la misma tabla), no brazos.

USO:  python experimentos/junta_20260921/B/corre_b21_lectura.py --humo
"""
import argparse, hashlib, json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
BAV = os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv')
JBA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'BA')
JA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A')
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
HUMOS = os.path.join(RAIZ, 'datos', 'humo')
sys.path[:0] = [AQUI, BAV, JBA, JA, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import corre_familias_bav as BAVR                 # runner de BA-v: SOLO LECTURA (entrada exacta, regla 14)
import corre_familias_b6 as B6R                   # bloque 6: emisor, mundo, brazos
import organismo_bav_b21 as ORG                   # COPIA BYTE A BYTE del instrumento (sha verificado abajo)

SHA_ORIGEN = '2dca0a3e239481f0'
SEMILLAS = [913, 914, 915]
T_HUMO = 33000
PROHIBIDAS = set(range(821, 901)) | set(range(921, 1001))
XNEG, BAR, PATS = B6R.XNEG, B6R.BAR, B6R.PATS
D, NVAR = 12, 3
PARES = [(i, j) for i in range(D) for j in range(i + 1, D)]
IDX = {p: k for k, p in enumerate(PARES)}
LINEAS = []


def log(s=''):
    print(s, flush=True)
    LINEAS.append(str(s))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def bin4(par, P):
    return int(P[par[0]]) * 2 + int(P[par[1]])


# ------------------------------------------------------------------ las tres reglas, FUERA del organismo
def suma_tipo(gan, P, tab, vis, modo):
    """DENTRO del tipo. modo: 'suma' (la medida), 'min' (pura), 'minesc' (n x min, escala de k=3)."""
    vals = []
    for par in gan:
        g = IDX[tuple(par)]
        c = bin4(tuple(par), P)                    # memoria_variante=0 -> la direccion ES el bin de 2 bits
        if vis[g][c]:
            vals.append(float(tab[g][c]))
    if not vals:
        return 0.0, 0
    if modo == 'suma':
        return float(sum(vals)), len(vals)
    if modo == 'min':
        return float(min(vals)), len(vals)
    return float(len(vals) * min(vals)), len(vals)


def lee(P, gf, gv, tab, vis, modo):
    """conj_tipo=2 (la celda BA-v) con `dentro` = modo. ENTRE tipos: min (combina='min')."""
    sf, nf = suma_tipo(gf, P, tab, vis, modo)
    sv, nv = suma_tipo(gv, P, tab, vis, modo)
    if nf < len(gf):
        return None, nf, nv                        # la FORMA no consta -> la tabla CALLA (releva a la lineal)
    if nv < len(gv) and not nv:
        return sf, nf, nv                          # la VARIANTE no consta EN ABSOLUTO -> manda la FORMA
    return min(sf, sv), nf, nv


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--T', type=int, default=T_HUMO)
    ap.add_argument('--semillas', default=','.join(str(s) for s in SEMILLAS))
    a = ap.parse_args()
    if not a.humo:
        raise SystemExit('Este script solo tiene modo --humo (un proceso, 6 corridas, <= 200 000 pasos).')
    sem = [int(x) for x in a.semillas.split(',') if x.strip()]
    if any(s in PROHIBIDAS for s in sem):
        raise SystemExit('Semilla de SERIE pedida en un humo: %s' % sorted(set(sem) & PROHIBIDAS))
    if len(sem) * 2 > 6 or len(sem) * 2 * a.T > 200000:
        raise SystemExit('Presupuesto: %d corridas x %d pasos = %d. Maximo 6 corridas y 200 000 pasos.'
                         % (len(sem) * 2, a.T, len(sem) * 2 * a.T))

    t0 = time.time()
    sha_copia = h16(os.path.join(AQUI, 'organismo_bav_b21.py'))
    sha_orig = h16(os.path.join(BAV, 'organismo_familias_bav.py'))
    log('MINI-PRUEBA B (Q2, junta 21-sep): las reglas de lectura comparadas SOBRE LA MISMA TABLA.')
    log('  copia del instrumento  %s   origen %s   esperado %s   -> %s'
        % (sha_copia, sha_orig, SHA_ORIGEN,
           'IDENTICA' if (sha_copia == sha_orig == SHA_ORIGEN) else '*** NO COINCIDE'))
    if not (sha_copia == sha_orig == SHA_ORIGEN):
        raise SystemExit('El instrumento no es el preregistrado. Parado antes de gastar una corrida.')
    log('  runner BA-v (solo lectura) %s   corre_familias_b6 %s'
        % (h16(os.path.join(BAV, 'corre_familias_bav.py')), h16(os.path.join(N12, 'corre_familias_b6.py'))))
    log('  presupuesto: %d corridas x T = %d  ->  %d pasos' % (len(sem) * 2, a.T, len(sem) * 2 * a.T))
    log('  celda BA-v = %s' % BAVR.CELDAS['BA-v'])
    log('  referente %s   hermana %s   otro token %s' % (XNEG, BAR['neg']['H'], BAR['neg']['TK']))
    log('')

    filas = []
    for s in sem:
        t1 = time.time()
        msg = B6R.emisor(s, a.T)['neg']
        if msg is None:
            log('  s%d: el emisor NO emitio a T=%d -> semilla sin mensaje, se reporta y se sigue' % (s, a.T))
            filas.append(dict(seed=s, emitido=False))
            continue
        kw = BAVR.entrada('PAR', 'BA-v', s, msg, a.T)      # LA ENTRADA EXACTA del runner registrado
        r = ORG.run(**kw)
        tab, vis = r['mem_tabla'], r['mem_visto']
        gf, gv = r['tipo_gan_forma'], r['tipo_gan_var']
        P = PATS(r['fam_seed'])
        # --- control de vacuidad del analisis: la SUMA reimplementada fuera == W_tabla de dentro (32/32)
        okc, malos = 0, []
        for k in P:
            v, _, _ = lee(P[k], gf, gv, tab, vis, 'suma')
            w = r['W_tabla'].get(k)
            if (v is None and w is None) or (v is not None and w is not None and abs(v - w) < 1e-6):
                okc += 1
            else:
                malos.append((k, v, w))
        fila = dict(seed=s, emitido=True, T=a.T, fam_seed=r['fam_seed'], deaths=r['deaths'],
                    t_entrega=r['canal_t_entrega'], lee_ref=r['canal_lee_ref'],
                    gan_forma=gf, gan_var=gv, control_32=okc, control_malos=malos[:4],
                    R_msg=msg['R'], seg=round(time.time() - t1, 1))
        for nom, modo in (('SUMA', 'suma'), ('MIN', 'min'), ('MINESC', 'minesc')):
            d = {}
            for et, nk in (('X', XNEG), ('H', BAR['neg']['H']), ('TK', BAR['neg']['TK'])):
                v, nf, nv = lee(P[nk], gf, gv, tab, vis, modo)
                d[et] = dict(valor=v, nf=nf, nv=nv, muerde_hambre1=(None if v is None else bool(1.2 * v + 2.5 > 0)))
            # cuantos de los 32 estimulos quedarian por encima del umbral de mordida con hambre = 1
            n_si = sum(1 for k in P
                       if (lambda z: z is not None and 1.2 * z + 2.5 > 0)(lee(P[k], gf, gv, tab, vis, modo)[0]))
            d['n_muerde_32'] = n_si
            fila[nom] = d
        # --- estructura: cuantas ganadoras de VARIANTE colisionan entre X y su hermana
        fila['col_var'] = sum(1 for par in gv if bin4(tuple(par), P[XNEG]) == bin4(tuple(par), P[BAR['neg']['H']]))
        filas.append(fila)
        log('  s%-4d  %5.1fs  entrega t=%s  muertes %s  control SUMA==W_tabla %d/32  ganadoras VARIANTE que '
            'COLISIONAN entre %s y %s: %d/%d'
            % (s, fila['seg'], fila['t_entrega'], fila['deaths'], okc, XNEG, BAR['neg']['H'],
               fila['col_var'], len(gv)))

    log('')
    log('--- QUE LEE LA TABLA (al final de la vida, MISMA tabla, tres reglas) ---')
    log('%-6s %-8s %-22s %-22s %-22s %-10s' % ('seed', 'regla', 'X=%s' % XNEG, 'H=%s' % BAR['neg']['H'],
                                               'TK=%s' % BAR['neg']['TK'], 'muerde/32'))
    for f in filas:
        if not f.get('emitido'):
            continue
        for nom in ('SUMA', 'MIN', 'MINESC'):
            d = f[nom]
            fmt = lambda e: '%-7s nf=%d nv=%d %s' % (d[e]['valor'], d[e]['nf'], d[e]['nv'],
                                                    'MUERDE' if d[e]['muerde_hambre1'] else 'no')
            log('%-6d %-8s %-22s %-22s %-22s %-10d' % (f['seed'], nom, fmt('X'), fmt('H'), fmt('TK'),
                                                       d['n_muerde_32']))

    log('')
    log('--- RESUMEN (mecanismo, NO conducta) ---')
    for nom in ('SUMA', 'MIN', 'MINESC'):
        ok = [f for f in filas if f.get('emitido')]
        mx = sum(1 for f in ok if f[nom]['X']['muerde_hambre1'])
        mh = sum(1 for f in ok if f[nom]['H']['muerde_hambre1'])
        mt = sum(1 for f in ok if f[nom]['TK']['muerde_hambre1'])
        log('  %-8s  muerde X %d/%d   muerde HERMANA %d/%d   muerde OTRO TOKEN %d/%d   mediana muerde/32 %s'
            % (nom, mx, len(ok), mh, len(ok), mt, len(ok),
               sorted(f[nom]['n_muerde_32'] for f in ok)[len(ok) // 2] if ok else '-'))

    os.makedirs(HUMOS, exist_ok=True)
    sello = time.strftime('%Y%m%d_%H%M%S')
    out = os.path.join(HUMOS, 'humo_b21_lectura_%s.json' % sello)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(script=h16(os.path.abspath(__file__)), instrumento=sha_copia,
                                 origen=sha_orig, T=a.T, semillas=sem, corridas=len(sem) * 2,
                                 pasos=len(sem) * 2 * a.T, sello=sello, seg=round(time.time() - t0, 1),
                                 celda=BAVR.N(BAVR.CELDAS['BA-v']), ref=XNEG, herm=BAR['neg']['H'],
                                 tk=BAR['neg']['TK']),
                       filas=filas, log=LINEAS), f, indent=1)
    log('')
    log('HUMO -> %s  (%.1f s)' % (out, time.time() - t0))
    with open(os.path.join(AQUI, 'humo_b21_salida.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(LINEAS) + '\n')


if __name__ == '__main__':
    main()
