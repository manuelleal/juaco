"""JUNTA FASE 5, CREADOR A -- HUMO del candidato A1 (lectura por DOS TIPOS DE GANADORA).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin
backprop) que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy, fase 5: que el
mensaje refiera a la FAMILIA Y a la VARIANTE con la MISMA tabla (BAR-T <= 5/20 Y PAR >= 15/20).

El mundo, el canal, EL EMISOR, las medidas de la boca y la letra son LOS OBJETOS del bloque 6, importados y no
recopiados (ERR-31): `corre_familias_b6` -> `corre_familias_b5` -> `corre_familias_b4b` -> ... -> bloque 1.
El EMISOR es el del bloque 6 SIN TOCAR (dos_tipos=0, memoria_variante=0, k_ganadoras=1, voraz=1.0 = b4b bit a
bit): lo que se mide es LA LECTURA, no el habla.

CELDAS (factorial de lectura, con la MISMA tabla y el MISMO mensaje):
  b5k3  = k_ganadoras 3, sin sufijo, dos_tipos 0  -> el bloque 5 BIT A BIT (familia exacta, no distingue variante)
  b6suf = k_ganadoras 3, CON sufijo,  dos_tipos 0  -> el bloque 6 BIT A BIT (variante, pierde familia y sube la base)
  A1    = dos_tipos 1 (3 ganadoras de FORMA + 1 mixta por pixel de variante), sin sufijo, pesos fijos
  A1w   = A1 + `pesos_tipo` 1 (los pesos de los dos tipos aprendidos por consecuencia)

REGLA 3 y 11: esto es HUMO de un creador -- UN proceso, sin Pool, <= 3 semillas de 901-910 (nunca 821-860, que
son de la confirmacion). Los numeros de 2-3 semillas NO son evidencia: son para ver si el mecanismo hace lo que
dice antes de gastar una serie.
ERR-44 / T-E: todo se mide sobre lo que LEE LA BOCA (`primera_b2`, `primera_b4`), nunca sobre pesos internos.
ERR-54: los crudos se guardan ANTES de cualquier analisis.

    python experimentos/junta_fase5/A/corre_familias_a1.py [--semillas 901,902] [--T 30000] [--celdas A1,b5k3]
"""
import sys, os, json, time, hashlib, platform

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import numpy as np
import corre_familias_b6 as B6R              # bloque 6: mundo, canal, emisor, medidas y letra (ERR-31)

B5R, B4BR, B2R, CF = B6R.B5R, B6R.B4BR, B6R.B2R, B6R.CF
log, h16, N, med = CF.log, CF.h16, CF.N, CF.med
BASE, KW_E, KW_R = B2R.BASE, B6R.KW_E, B6R.KW_R
XNEG, BAR, PATS, prefijo, PAR_HERM = B6R.XNEG, B6R.BAR, B6R.PATS, B6R.prefijo, B6R.PAR_HERM
PLANTILLA = B6R.PLANTILLA                    # los 9 brazos de la direccion (-) del bloque 4b/5/6
SEM_R, SEM_OTRO, VORAZ = B6R.B5R.SEM_R, B6R.B5R.SEM_OTRO, B6R.VORAZ

T_HUMO = 30000
SEMILLAS = [901, 902]                        # del rango 901-910 (humo del creador). NUNCA 821-860
SHA_B6_ESPERADO = 'b10cbd4ddd0c32a3'
SHA_B5_ESPERADO = 'e0b6b90f6f92d5c1'
SHA_B4B_ESPERADO = 'b3dd1d7e66a2d147'
SHA_V14_ESPERADO = 'feefc88b1fd8d434'

# ---------------------------------------------------------------- celdas: SOLO cambia COMO LEE la tabla
_DT = dict(k_ganadoras=3, memoria_variante=0, dos_tipos=1, k_forma=3, var_cubre=1)
CELDAS = {
    'b4b':   dict(k_ganadoras=1, memoria_variante=0, dos_tipos=0),                      # k1v0: b4b BIT A BIT (referencia de R6)
    'b5k3':  dict(k_ganadoras=3, memoria_variante=0, dos_tipos=0),                      # bloque 5 BIT A BIT
    'b6suf': dict(k_ganadoras=3, memoria_variante=1, dos_tipos=0),                      # bloque 6 BIT A BIT
    'b5k3e': dict(k_ganadoras=3, memoria_variante=0, dos_tipos=0, msg_elige=0),         # b5 + el mensaje NO re-elige
    'A1m':   dict(_DT, combina='media', msg_elige=1),                                   # dos tipos, promedio
    'A1e':   dict(_DT, combina='media', msg_elige=0),                                   # dos tipos, promedio, sin re-eleccion
    'A1min': dict(_DT, combina='min', msg_elige=1),                                     # dos tipos, conjuncion
    'A1me':  dict(_DT, combina='min', msg_elige=0),                                     # conjuncion + sin re-eleccion
    'A1':    dict(_DT, combina='min', msg_elige=0, exige_dir=1),      # EL CANDIDATO: dos tipos + conjuncion + direccion completa + el mensaje no re-elige
    'A1-c':  dict(_DT, combina='media', msg_elige=0, exige_dir=1),    # ablacion 1: sin la CONJUNCION (promedio)
    'A1-d':  dict(_DT, combina='min', msg_elige=0, exige_dir=0),      # ablacion 2: sin la DIRECCION COMPLETA
    'A1-e':  dict(_DT, combina='min', msg_elige=1, exige_dir=1),      # ablacion 3: el mensaje SI re-elige (como b4/b5/b6)
}
PLANT = {p[0]: p for p in PLANTILLA}
BRAZOS_BASE = ['CANAL', 'CORTADO', 'BAR-H', 'BAR-T', 'VALOR', 'PAR', 'PAR0']   # la letra de la MISION
# el criterio de la MISION (sobre 20 semillas; aqui se mira la DIRECCION, no el numero)
CRITERIO = dict(CANAL=('>=', 15), CORTADO=('<=', 5), BARH=('<=', 5), BART=('<=', 5), PAR=('>=', 15),
                VALOR=('<=', 5))


def canal_de(base, msg, D=12):
    """El `canal` de cada brazo: la MISMA expresion del bloque 4/5/6, con la PLANTILLA importada."""
    _n, _m, _p, _o, _ph = PLANT[base]
    if _p == 'CEROS':
        P = [0.0] * D
    elif _p == 'REF':
        P = msg['P']
    else:
        P = PATS(msg['fam_seed'])[BAR['neg'][_p]]
    return dict(modo=_m, t=msg['t'], ref=msg['ref'], P=P, R=msg['R'])


def corre(base, cel, seed, msg, Ti, nk=30, ktop=3, nkmax=90):
    import organismo_familias_a1 as A1
    kw = B2R.resuelve(KW_R, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    _n, _m, _p, _o, _ph = PLANT[base]
    fsr = seed + SEM_OTRO if _o else seed
    r = A1.run(seed + SEM_R, T=Ti, fam_seed=fsr, canal=canal_de(base, msg), par_herm=_ph,
               **dict(CELDAS[cel], **kw))
    d = dict(tipo='R', brazo='%s-%s' % (base, cel), base=base, cel=cel, seed=seed, deaths=r['deaths'],
             celdas=r['celdas'], entregado=r['canal_entregado'], t_entrega=r['canal_t_entrega'],
             fam_seed=r['fam_seed'], w_forma=r['w_forma'], w_variante=r['w_variante'],
             gan_forma=r['tipo_gan_forma'], gan_var=r['tipo_gan_var'],
             n_mismo_dos=(None if r['canal_mismo_dos'] is None else len(r['canal_mismo_dos'])),
             n_mismo_dir_k=(None if r['canal_mismo_dir_k'] is None else len(r['canal_mismo_dir_k'])),
             n_mismo_bin_k=(None if r['canal_mismo_bin_k'] is None else len(r['canal_mismo_bin_k'])),
             herm_en_grupo=(None if r['canal_mismo_dos'] is None else bool(BAR['neg']['H'] in r['canal_mismo_dos'])),
             cobertura=r['mem_cobertura'], vistas=r['mem_vistas'], W_ref=(r['W_tabla'] or {}).get(XNEG),
             W_herm=(r['W_tabla'] or {}).get(BAR['neg']['H']), W_tk=(r['W_tabla'] or {}).get(BAR['neg']['TK']))
    d['B4'] = B4BR.lee_b4(r, msg['ref'])
    d['prefijo'] = prefijo(r, r['canal_t_entrega'] if r['canal_t_entrega'] is not None else r['canal_t_msg'])
    return d


def tarea(args):
    """Tarea de nivel de modulo: picklable para el Pool de la confirmatoria (spawn en Windows)."""
    if args[0] == 'E':
        _, seed, Ti = args
        return dict(tipo='E', seed=seed, msgs=emisor(seed, Ti))
    _, base, cel, seed, msg, Ti = args
    return corre(base, cel, seed, msg, Ti)


def emisor(seed, Ti, nk=30, ktop=3, nkmax=90):
    """EL EMISOR NO CAMBIA: es el del bloque 6 (dos_tipos=0 -> b4b bit a bit). Se llama al objeto importado."""
    return B6R.emisor(seed, Ti, nk, ktop, nkmax)


SHAS = lambda: dict(script=h16(os.path.abspath(__file__)),
                    constructor=h16(os.path.join(AQUI, 'construye_familias_a1.py')),
                    instrumento=h16(os.path.join(AQUI, 'organismo_familias_a1.py')),
                    arnes=h16(os.path.join(AQUI, 'identidad_familias_a1.py')),
                    origen_b6=h16(os.path.join(N12, 'organismo_familias_b6.py')),
                    origen_b5=h16(os.path.join(N12, 'organismo_familias_b5.py')),
                    origen_b4b=h16(os.path.join(N12, 'organismo_familias_b4b.py')),
                    runner_bloque6=h16(os.path.join(N12, 'corre_familias_b6.py')),
                    preregistro_bloque6=h16(os.path.join(N12, 'PREREGISTRO_bloque6_sufijo.md')),
                    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))


def serie(desde, n_sem, Tb, cel_act, npool):
    """LA CONFIRMATORIA. La lanza el COORDINADOR (reglas 3 y 11). Pool configurable: --pool o JUACO_POOL."""
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    SEEDS = list(range(desde, desde + n_sem))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(AQUI, 'serie_a1_s%d-%d_%s.log' % (SEEDS[0], SEEDS[-1], stamp)),
                        'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log("SERIE A1 (creador A, junta fase 5): celdas %s, brazos %s, semillas %d-%d, T=%d, Pool(%d)."
        % (cel_act, BRAZOS_BASE, SEEDS[0], SEEDS[-1], Tb, npool))
    log("El mundo, el canal y el EMISOR son los del bloque 6, SIN TOCAR. Lo unico nuevo es COMO LEE la tabla.")
    for k, v in SHAS().items():
        log("    sha %-24s %s" % (k, v))
    for k, esp in [('origen_b6', SHA_B6_ESPERADO), ('origen_b5', SHA_B5_ESPERADO),
                   ('origen_b4b', SHA_B4B_ESPERADO), ('origen_organismo_v14', SHA_V14_ESPERADO)]:
        if SHAS()[k] != esp:
            log("*** ORIGEN CAMBIADO: %s. Se para." % k); sys.exit(1)
    with mp.Pool(npool) as pool:
        log("ETAPA 1/3 - DIAGNOSTICO ESTRUCTURAL (T = 0, %d semillas)" % len(SEEDS))
        diags = []
        for s in SEEDS:
            d = CF.diagnostico(s, 30, 3, BASE); d.pop('cod'); d['estructura'] = B6R.estructura_v(s)
            diags.append(dict(tipo='D', **d))
        log("    alias por par mediana %s  piso de forma %s/32"
            % (med([d['alias_pares'] for d in diags]), med([d['estructura']['piso_forma_v0'] for d in diags])))
        log("ETAPA 2/3 - EMISORES (%d corridas de %d pasos; son los del bloque 6 bit a bit)" % (len(SEEDS), Tb))
        em = pool.map(tarea, [('E', s, Tb) for s in SEEDS], chunksize=1)
        msgs = {d['seed']: d['msgs'] for d in em}
        sin = [s for s in SEEDS if not (msgs.get(s) or {}).get('neg')]
        log("    emiten %d/%d; sin mensaje (se EXCLUYEN, P-I2): %s" % (len(SEEDS) - len(sin), len(SEEDS), sin))
        tr = [('R', b, c, s, msgs[s]['neg'], Tb) for c in cel_act for b in BRAZOS_BASE for s in SEEDS
              if (msgs.get(s) or {}).get('neg')]
        log("ETAPA 3/3 - RECEPTORES: %d corridas de %d pasos..." % (len(tr), Tb))
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(tr):
                log("          %d/%d" % (i, len(tr)))
    crudo = os.path.join(AQUI, 'serie_a1_s%d-%d_%s_crudo.json' % (SEEDS[0], SEEDS[-1], stamp))
    with open(crudo, 'w', encoding='utf-8') as f:      # ERR-54: los crudos, ANTES del analisis
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='serie', T=Tb, semillas=SEEDS,
                                 celdas={c: N(CELDAS[c]) for c in cel_act}, brazos=BRAZOS_BASE,
                                 criterio=CRITERIO, kw_E=N(KW_E), kw_R=N(KW_R), shas=SHAS(), pool=npool,
                                 python=platform.python_version(), numpy=np.__version__),
                       diagnostico=diags, mensajes=N(msgs), brazos=res), f, ensure_ascii=False, default=str)
    log("CRUDO -> %s  sha256_16 = %s  (ERR-54)" % (os.path.basename(crudo), h16(crudo)))
    tabla(res, cel_act)
    CF._log['f'].close()


def tabla(res, cel_act):
    """La tabla de los brazos del bloque 6 y LA LETRA (R1-R5 + el objetivo de la MISION) por celda."""
    log("")
    log("%-7s " % 'celda' + ' '.join('%8s' % b for b in BRAZOS_BASE) + '   dist(PAR)  dist(PAR0)  muertes  okU')
    out = {}
    for c in cel_act:
        fila = {}
        for b in BRAZOS_BASE:
            rs = [r for r in res if r['cel'] == c and r['base'] == b]
            n = len([r for r in rs if r['B4']['evX'] is not None])
            fila[b] = (sum(1 for r in rs if r['B4']['evX'] == 0.0), n)
        dP = [r['B4']['dist'] for r in res if r['cel'] == c and r['base'] == 'PAR' and r['B4']['dist'] is not None]
        d0 = [r['B4']['dist'] for r in res if r['cel'] == c and r['base'] == 'PAR0' and r['B4']['dist'] is not None]
        mu = med([r['deaths'] for r in res if r['cel'] == c and r['base'] == 'CANAL'])
        ok = med([r['B4']['okU'] for r in res if r['cel'] == c and r['base'] == 'CANAL'
                  and r['B4']['okU'] is not None])
        out[c] = dict(com=fila, dist=(int(sum(dP)), len(dP)), dist0=(int(sum(d0)), len(d0)), muertes=mu, okU=ok)
        log("%-7s " % c + ' '.join('%4d/%-3d' % fila[b] for b in BRAZOS_BASE)
            + '   %d/%d      %d/%d       %s     %s' % (int(sum(dP)), len(dP), int(sum(d0)), len(d0), mu, ok))
    for c in cel_act:
        C, CO = out[c]['com']['CANAL'], out[c]['com']['CORTADO']
        BT, BH, VA = out[c]['com']['BAR-T'], out[c]['com']['BAR-H'], out[c]['com']['VALOR']
        dP, d0 = out[c]['dist'], out[c]['dist0']
        ok = lambda b: 'pasa' if b else 'CAE'
        log("  [%s] R1 CANAL %d/%d >= 15 y CORTADO %d <= 5: %s; R2 BAR-T %d <= CORTADO+3: %s; "
            "R3 BAR-H %d <= CORTADO+5: %s; R4 VALOR %d <= CORTADO+3: %s; R5 dist %d/%d >= 12 y >= gemelo+5 "
            "(%d): %s  |  MISION (BAR-T <= 5 Y PAR >= 15): %s"
            % (c, C[0], C[1], CO[0], ok(C[0] >= 15 and CO[0] <= 5), BT[0], ok(BT[0] <= CO[0] + 3),
               BH[0], ok(BH[0] <= CO[0] + 5), VA[0], ok(VA[0] <= CO[0] + 3), dP[0], dP[1], d0[0],
               ok(dP[0] >= 12 and dP[0] >= d0[0] + 5),
               'SI' if (BT[0] <= 5 and dP[0] >= 15) else 'no'))
    return out


if __name__ == '__main__':
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    Tb = arg('--T', T_HUMO)
    if '--semillas' in sys.argv:
        SEMILLAS = [int(x) for x in sys.argv[sys.argv.index('--semillas') + 1].split(',')]
    cel_act = list(CELDAS)
    if '--celdas' in sys.argv:
        cel_act = [c.strip() for c in sys.argv[sys.argv.index('--celdas') + 1].split(',') if c.strip()]
        malas = [c for c in cel_act if c not in CELDAS]
        if malas:
            raise SystemExit(f"--celdas: desconocida(s) {malas}. Validas: {list(CELDAS)}")
    if '--serie' not in sys.argv and (len(SEMILLAS) > 3 or any(not (901 <= s <= 910) for s in SEMILLAS)):
        raise SystemExit(f"HUMO: <= 3 semillas del rango 901-910 (la nave de la junta). Pedidas: {SEMILLAS}")

    if '--serie' in sys.argv:      # LA CONFIRMATORIA LA LANZA EL COORDINADOR (reglas 3 y 11)
        npool = arg('--pool', int(os.environ.get('JUACO_POOL', 6)))
        serie(arg('--desde', 821), arg('--n', 20), arg('--T', 100000), cel_act, npool)
        sys.exit(0)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(AQUI, f'humo_a1_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log(f"HUMO del CREADOR A (junta fase 5): lectura por DOS TIPOS DE GANADORA. UN proceso, sin Pool (regla 3).")
    log(f"celdas {cel_act}  brazos {BRAZOS_BASE}  semillas {SEMILLAS}  T = {Tb}")
    log("Criterio de la MISION (sobre 20 semillas, no sobre esto): CANAL >= 15, CORTADO <= 5, BAR-H <= 5, "
        "BAR-T <= 5, PAR >= 15, VALOR <= 5.")
    ok_sha = True
    for k, v in SHAS().items():
        log(f"    sha {k:24s} {v}")
    for k, esp in [('origen_b6', SHA_B6_ESPERADO), ('origen_b5', SHA_B5_ESPERADO),
                   ('origen_b4b', SHA_B4B_ESPERADO), ('origen_organismo_v14', SHA_V14_ESPERADO)]:
        if SHAS()[k] != esp:
            log(f"*** ORIGEN CAMBIADO: {k} es {SHAS()[k]}, se esperaba {esp}."); ok_sha = False
    log(f"    origenes verificados -> {'OK' if ok_sha else 'FALLA'}")
    if not ok_sha:
        sys.exit(1)

    log("1/4 IDENTIDAD (subconjunto; el arnes completo, 68/68, es identidad_familias_a1.py)")
    import organismo_familias_a1 as A1
    import organismo_familias_b6 as B6
    NUEVAS = ('dos_tipos', 'k_forma', 'k_var', 'var_cubre', 'pesos_tipo', 'eta_w', 'n_forma', 'n_mixtas',
              'tipo_gan_forma', 'tipo_gan_var', 'w_forma', 'w_variante', 'canal_mismo_dos')
    kid = B2R.resuelve(KW_R, 8000)
    n_id = n_ok = 0
    for s in SEMILLAS:
        a = B6.run(s, T=8000, fam_seed=s, k_ganadoras=3, memoria_variante=0, **kid)
        b = A1.run(s, T=8000, fam_seed=s, k_ganadoras=3, memoria_variante=0, dos_tipos=0, **kid)
        dif = [k for k in a if k not in NUEVAS and N(a[k]) != N(b.get(k))]
        n_id += 1; n_ok += int(not dif)
        c = A1.run(s, T=8000, fam_seed=s, k_ganadoras=3, memoria_variante=0, dos_tipos=1, **kid)
        dif2 = [k for k in a if k not in NUEVAS and N(a[k]) != N(c.get(k))]
        n_id += 1; n_ok += int(bool(dif2))          # DEBE diferir (ERR-64b: no-vacuidad)
        log(f"    semilla {s}: apagado == b6 {'SI' if not dif else '*** NO ' + str(dif[:4])}   |   "
            f"encendido != b6 {'SI' if dif2 else '*** NO'}")
    log(f"  IDENTIDAD DEL HUMO {n_ok}/{n_id}")
    if n_ok != n_id:
        log("*** La identidad del humo falla: no se mide nada (P-I1).")
        sys.exit(1)

    log("2/4 DIAGNOSTICO ESTRUCTURAL (T = 0, sin simular): alias del mundo y resolucion de la referencia")
    diags = []
    for s in SEMILLAS:
        d = CF.diagnostico(s, 30, 3, BASE); d.pop('cod')
        d['estructura'] = B6R.estructura_v(s)
        diags.append(dict(tipo='D', **d))
        e = d['estructura']
        log(f"    semilla {s}: alias_pares {d['alias_pares']:.5f}  U3 {d['U3']}  |  celdas que NO distinguen "
            f"al referente: BAR-H {e['BAR_H_v0']} (solo forma {e['BAR_H_v0_forma']}), BAR-T {e['BAR_T_v0']} "
            f"(solo forma {e['BAR_T_v0_forma']})  |  piso de forma {e['piso_forma_v0']}/32")
        log(f"                 px en que difieren referente y hermana {e['BAR_H_px_dif']} "
            f"(variante = {e['n_var_px']}); referente y otro token {e['BAR_T_px_dif']}")

    log(f"3/4 EMISORES (los del bloque 6, sin tocar): {len(SEMILLAS)} corridas de {Tb} pasos")
    msgs = {}
    for s in SEMILLAS:
        t1 = time.time(); m = emisor(s, Tb); dt = time.time() - t1
        msgs[s] = m; q = m['neg']
        log(f"    E s{s} {dt:5.1f}s  mensaje {q and (q['ref'], q['R'], 't=%d' % q['t'], 'tras %d exp' % q['enc'])}")

    tareas = [(b, c, s) for c in cel_act for b in BRAZOS_BASE for s in SEMILLAS if (msgs[s] or {}).get('neg')]
    log(f"4/4 RECEPTORES: {len(tareas)} corridas de {Tb} pasos ({len(cel_act)} celdas x {len(BRAZOS_BASE)} brazos)")
    res = []
    for b, c, s in tareas:
        t1 = time.time(); r = corre(b, c, s, msgs[s]['neg'], Tb); dt = time.time() - t1
        res.append(r); B = r['B4']
        log(f"    {r['brazo']:14s} s{s} {dt:5.1f}s  entrega t={r['t_entrega']}  comio {1-int(B['evX'] or 0)}  "
            f"dist {B['dist']}  okU {B['okU']}  via {'RAPIDA' if B['fam1'] else 'lenta'}  muertes {r['deaths']}  "
            f"W(ref) {r['W_ref']} W(herm) {r['W_herm']} W(otro) {r['W_tk']}")
        if r['base'] == 'CANAL':
            log(f"                   MECANISMO {c}: ganadoras forma {r['gan_forma']} variante {r['gan_var']}  "
                f"grupo del mensaje: CONJUNTO {r['n_mismo_dos']}/32, por DIRECCION k {r['n_mismo_dir_k']}/32, "
                f"por BIN k {r['n_mismo_bin_k']}/32  hermana dentro {r['herm_en_grupo']}  pesos "
                f"({r['w_forma']}, {r['w_variante']})  cobertura {r['cobertura']}")

    # ---- ERR-54: crudos ANTES del analisis
    crudo = os.path.join(AQUI, f'humo_a1_{stamp}_crudo.json')
    with open(crudo, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T=Tb, semillas=SEMILLAS,
                                 celdas={c: N(CELDAS[c]) for c in cel_act}, brazos=BRAZOS_BASE, criterio=CRITERIO,
                                 kw_E=N(KW_E), kw_R=N(KW_R), shas=SHAS(), python=platform.python_version(),
                                 numpy=np.__version__),
                       diagnostico=diags, mensajes=N(msgs), brazos=res), f, ensure_ascii=False, default=str)
    log(f"CRUDO -> {os.path.basename(crudo)}  sha256_16 = {h16(crudo)}  (ERR-54: antes del analisis)")

    # ---- tabla por celda (los brazos del bloque 6; `com` = mordio a la 1.a exposicion de la vida al referente)
    log("")
    log("TABLA (com = comio a la 1.a exposicion de la VIDA al referente / n; dist = trata distinto a la hermana)")
    log(f"{'celda':7s} " + ' '.join(f'{b:>8s}' for b in BRAZOS_BASE) + '   dist(PAR)  dist(PAR0)  muertes  okU')
    tab = {}
    for c in cel_act:
        fila, g = {}, {r['brazo']: r for r in res if r['cel'] == c}
        for b in BRAZOS_BASE:
            rs = [r for r in res if r['cel'] == c and r['base'] == b]
            n = len([r for r in rs if r['B4']['evX'] is not None])
            fila[b] = (sum(1 for r in rs if r['B4']['evX'] == 0.0), n)
        dP = [r['B4']['dist'] for r in res if r['cel'] == c and r['base'] == 'PAR' and r['B4']['dist'] is not None]
        d0 = [r['B4']['dist'] for r in res if r['cel'] == c and r['base'] == 'PAR0' and r['B4']['dist'] is not None]
        mu = med([r['deaths'] for r in res if r['cel'] == c and r['base'] == 'CANAL'])
        ok = med([r['B4']['okU'] for r in res if r['cel'] == c and r['base'] == 'CANAL'
                  and r['B4']['okU'] is not None])
        tab[c] = dict(com={b: fila[b] for b in BRAZOS_BASE}, dist=(int(sum(dP)), len(dP)),
                      dist0=(int(sum(d0)), len(d0)), muertes=mu, okU=ok)
        log(f"{c:7s} " + ' '.join(f'{fila[b][0]:>4d}/{fila[b][1]:<3d}' for b in BRAZOS_BASE)
            + f'   {int(sum(dP))}/{len(dP)}      {int(sum(d0))}/{len(d0)}       {mu}     {ok}')
    log("")
    log("LECTURA (humo, 2-3 semillas: NO es evidencia). Lo que hay que mirar: (1) CANAL alto y CORTADO bajo en "
        "A1; (2) BAR-T y BAR-H a la vez bajos -- eso es lo que ninguna celda anterior consiguio; (3) dist(PAR) "
        "alto con dist(PAR0) bajo; (4) muertes de A1 <= 1.5 x las de b5k3 (R6, la puerta que mato a k = 5).")

    dj = os.path.join(AQUI, f'humo_a1_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T=Tb, semillas=SEMILLAS,
                                 celdas={c: N(CELDAS[c]) for c in cel_act}, brazos=BRAZOS_BASE, criterio=CRITERIO,
                                 shas=SHAS(), crudo=os.path.basename(crudo), python=platform.python_version(),
                                 numpy=np.__version__),
                       tabla=N(tab), diagnostico=diags, mensajes=N(msgs), brazos=res), f,
                  ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    CF._log['f'].close()
