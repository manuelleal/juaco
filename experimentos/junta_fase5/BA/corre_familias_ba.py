"""JUNTA FASE 5 -- CANDIDATO **BA**: la lectura CONJUNTIVA de B (por TIPO) sobre las DOS GANADORAS DE DISTINTO
TIPO de A. Humo de un proceso (`--humo`) y confirmatoria con Pool (`--serie ... --pool N`, ERR-86).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy, fase 5:
que el mensaje refiera a la FAMILIA Y a la VARIANTE con la MISMA tabla (BAR-T <= 5/20 Y PAR >= 15/20).

El mundo, el canal, EL EMISOR, las medidas de la boca y la letra son LOS OBJETOS del bloque 6, importados y no
recopiados (ERR-31): `corre_familias_b6` -> `corre_familias_b5` -> `corre_familias_b4b` -> ... -> bloque 1.
El EMISOR es el del bloque 6 SIN TOCAR (conj_tipo=0, dos_tipos=0, memoria_variante=0, k_ganadoras=1,
voraz=1.0 = b4b bit a bit): lo que se mide es LA LECTURA, no el habla.

REGLA 14 (ERR-38/41): la ENTRADA del receptor se compara CAMPO A CAMPO con la del bloque 6 antes de correr
(`verifica_entrada`), y el script se PARA si difiere en algo que no sea una perilla declarada de la celda.
ERR-54: los crudos se escriben ANTES de cualquier analisis. ERR-44: todo se mide sobre lo que hizo la BOCA.
ERR-42: el humo llega a ESCRIBIR su JSON.

CELDAS (factorial de LECTURA, con la MISMA tabla y el MISMO mensaje):
  b5k3  = k=3, sin sufijo, dos_tipos 0                -> bloque 5 BIT A BIT (familia exacta; BAR-T 3/2, PAR 7/6)
  b6suf = k=3, CON sufijo, dos_tipos 0                -> bloque 6 BIT A BIT (variante; BAR-T 12/8, PAR 15/15)
  A1    = dos tipos + min + `exige_dir` + msg_elige 0 -> el candidato del creador A (BAR-T 9/5, PAR 13/13)
  BA    = dos tipos + min + `conj_tipo`=1 + msg_elige 0 -> EL CANDIDATO (la conjuncion de B, POR TIPO)
  BA-v  = BA con `conj_tipo`=2                        -> ablacion 1: la VARIANTE incompleta vota con lo que sabe
  BA-c  = BA con `combina`='media'                    -> ablacion 2: sin la conjuncion de VALOR
  BA-e  = BA con `msg_elige`=1                        -> ablacion 3: el mensaje SI re-elige (la fuga de A)

    python experimentos/junta_fase5/BA/corre_familias_ba.py --humo
    python experimentos/junta_fase5/BA/corre_familias_ba.py --serie --desde 861 --celdas b5k3,b6suf,A1,BA --pool 5
"""
import sys, os, json, time, hashlib, platform

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
JA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A')
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, JA, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import numpy as np
import corre_familias_b6 as B6R              # bloque 6: mundo, canal, emisor, medidas y letra (ERR-31)

B5R, B4BR, B2R, CF = B6R.B5R, B6R.B4BR, B6R.B2R, B6R.CF
log, h16, N, med = CF.log, CF.h16, CF.N, CF.med
BASE, KW_E, KW_R = B2R.BASE, B6R.KW_E, B6R.KW_R
XNEG, BAR, PATS, prefijo = B6R.XNEG, B6R.BAR, B6R.PATS, B6R.prefijo
PLANTILLA = B6R.PLANTILLA                    # los 9 brazos de la direccion (-) del bloque 4b/5/6
SEM_R, SEM_OTRO, VORAZ = B6R.B5R.SEM_R, B6R.B5R.SEM_OTRO, B6R.VORAZ

T_HUMO = 100000
SEM_HUMO = [911]                             # FUERA de 821-900 (las dos series de la junta y las mias)
PROHIBIDAS = range(821, 901)                 # ninguna semilla de confirmacion se gasta en humo
SHA_B6_ESPERADO = 'b10cbd4ddd0c32a3'
SHA_B5_ESPERADO = 'e0b6b90f6f92d5c1'
SHA_B4B_ESPERADO = 'b3dd1d7e66a2d147'
SHA_V14_ESPERADO = 'feefc88b1fd8d434'
SHA_A1_ORIGEN = '8833e1dcfb62f26d'

# ---------------------------------------------------------------- celdas: SOLO cambia COMO LEE la tabla
_DT = dict(k_ganadoras=3, memoria_variante=0, dos_tipos=1, k_forma=3, var_cubre=1)
CELDAS = {
    'b4b':   dict(k_ganadoras=1, memoria_variante=0, dos_tipos=0),                    # k1v0: b4b BIT A BIT (referencia de R6)
    'b5k3':  dict(k_ganadoras=3, memoria_variante=0, dos_tipos=0),                    # bloque 5 BIT A BIT
    'b6suf': dict(k_ganadoras=3, memoria_variante=1, dos_tipos=0),                    # bloque 6 BIT A BIT
    'A1':    dict(_DT, combina='min', msg_elige=0, exige_dir=1),                      # el candidato del creador A
    'A1-d':  dict(_DT, combina='min', msg_elige=0, exige_dir=0),                      # A sin regla de abstencion
    'BA':    dict(_DT, combina='min', msg_elige=0, conj_tipo=1),                      # EL CANDIDATO
    'BA-v':  dict(_DT, combina='min', msg_elige=0, conj_tipo=2),                      # ablacion 1: la VARIANTE incompleta vota con lo que sabe
    'BA-c':  dict(_DT, combina='media', msg_elige=0, conj_tipo=1),                    # ablacion 2: sin la conjuncion de VALOR
    'BA-e':  dict(_DT, combina='min', msg_elige=1, conj_tipo=1),                      # ablacion 3: el mensaje SI re-elige
}
PLANT = {p[0]: p for p in PLANTILLA}
BRAZOS_BASE = ['CANAL', 'CORTADO', 'BAR-H', 'BAR-T', 'VALOR', 'PAR', 'PAR0']   # la letra de la MISION
BRAZOS_HUMO = ['CANAL', 'CORTADO', 'BAR-H', 'BAR-T', 'PAR']                    # 5 brazos + 1 emisor = 6 corridas
CRITERIO = dict(CANAL=('>=', 15), CORTADO=('<=', 5), BARH=('<=', 5), BART=('<=', 5), PAR=('>=', 15),
                VALOR=('<=', 5))
# perillas que SI pueden diferir de la entrada del bloque 6 (son la celda; regla 14)
PERILLAS_CELDA = set(('k_ganadoras', 'memoria_variante', 'dos_tipos', 'k_forma', 'k_var', 'var_cubre',
                      'pesos_tipo', 'eta_w', 'combina', 'msg_elige', 'exige_dir', 'dentro', 'conj_tipo'))


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


def entrada(base, cel, seed, msg, Ti, nk=30, ktop=3, nkmax=90):
    """LA ENTRADA EXACTA del receptor (lo que se le pasa a run). Se compara campo a campo (regla 14)."""
    kw = B2R.resuelve(KW_R, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    _n, _m, _p, _o, _ph = PLANT[base]
    fsr = seed + SEM_OTRO if _o else seed
    return dict(kw, seed=seed + SEM_R, T=Ti, fam_seed=fsr, canal=canal_de(base, msg, ), par_herm=_ph,
                **CELDAS[cel])


def entrada_b6(brazo6, seed, msg, Ti, nk=30, ktop=3, nkmax=90):
    """LA ENTRADA DEL BLOQUE 6, reconstruida con SUS objetos (corre_familias_b6.tarea, linea a linea)."""
    kw = B2R.resuelve(KW_R, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    fsr = seed + SEM_OTRO if B6R.BRAZOS[brazo6]['otro'] else seed
    return dict(kw, seed=seed + SEM_R, T=Ti, fam_seed=fsr, canal=B6R.canal_de(brazo6, msg, fsr),
                par_herm=B6R.BRAZOS[brazo6]['par'], k_ganadoras=B6R.BRAZOS[brazo6]['k'],
                memoria_variante=B6R.BRAZOS[brazo6]['mv'])


def verifica_entrada(msg, Ti, cel_act):
    """REGLA 14 (ERR-38/41): campo a campo contra la entrada del BLOQUE 6. Si algo que no sea una perilla de
    celda difiere, se PARA. 'Por defecto' no existe cuando el modulo es una copia con sus propios defaults."""
    ok = True
    for base in BRAZOS_BASE:
        b6 = entrada_b6('%s-k3v1' % base, msg['fam_seed'], msg, Ti)
        for cel in cel_act:
            mia = entrada(base, cel, msg['fam_seed'], msg, Ti)
            faltan = [k for k in b6 if k not in mia]
            sobran = [k for k in mia if k not in b6 and k not in PERILLAS_CELDA]
            difs = [k for k in b6 if k in mia and k not in PERILLAS_CELDA and N(b6[k]) != N(mia[k])]
            if faltan or sobran or difs:
                ok = False
                log("    *** ENTRADA %s-%s difiere del bloque 6: faltan %s  sobran %s  distintos %s"
                    % (base, cel, faltan, sobran, difs))
    b6 = entrada_b6('CANAL-k3v1', msg['fam_seed'], msg, Ti)
    log("    REGLA 14 - entrada campo a campo contra el bloque 6: %d campos comunes, %s"
        % (len(b6), 'IDENTICOS' if ok else '*** DIFIEREN'))
    log("       campos: %s" % sorted(b6))
    log("       perillas de celda (las UNICAS que pueden diferir): %s" % sorted(PERILLAS_CELDA))
    return ok


def corre(base, cel, seed, msg, Ti, nk=30, ktop=3, nkmax=90):
    import organismo_familias_ba as BA
    kw = B2R.resuelve(KW_R, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    _n, _m, _p, _o, _ph = PLANT[base]
    fsr = seed + SEM_OTRO if _o else seed
    r = BA.run(seed + SEM_R, T=Ti, fam_seed=fsr, canal=canal_de(base, msg), par_herm=_ph,
               **dict(CELDAS[cel], **kw))
    d = dict(tipo='R', brazo='%s-%s' % (base, cel), base=base, cel=cel, seed=seed, deaths=r['deaths'],
             celdas=r['celdas'], entregado=r['canal_entregado'], t_entrega=r['canal_t_entrega'],
             fam_seed=r['fam_seed'], lee_ref=r['canal_lee_ref'],
             gan_forma=r['tipo_gan_forma'], gan_var=r['tipo_gan_var'],
             n_mismo_dos=(None if r['canal_mismo_dos'] is None else len(r['canal_mismo_dos'])),
             n_mismo_dir_k=(None if r['canal_mismo_dir_k'] is None else len(r['canal_mismo_dir_k'])),
             n_mismo_bin_k=(None if r['canal_mismo_bin_k'] is None else len(r['canal_mismo_bin_k'])),
             herm_en_grupo=(None if r['canal_mismo_dos'] is None else bool(BAR['neg']['H'] in r['canal_mismo_dos'])),
             abstiene=(None if r['W_tabla'] is None else sum(1 for k in r['W_tabla'] if r['W_tabla'][k] is None)),
             cobertura=r['mem_cobertura'], vistas=r['mem_vistas'], W_ref=(r['W_tabla'] or {}).get(XNEG),
             W_herm=(r['W_tabla'] or {}).get(BAR['neg']['H']), W_tk=(r['W_tabla'] or {}).get(BAR['neg']['TK']))
    d['B4'] = B4BR.lee_b4(r, msg['ref'])
    d['prefijo'] = prefijo(r, r['canal_t_entrega'] if r['canal_t_entrega'] is not None else r['canal_t_msg'])
    return d


def tarea(args):
    """Tarea de nivel de modulo: picklable para el Pool de la confirmatoria (spawn en Windows)."""
    if args[0] == 'E':
        _, seed, Ti = args
        return dict(tipo='E', seed=seed, msgs=B6R.emisor(seed, Ti))
    _, base, cel, seed, msg, Ti = args
    return corre(base, cel, seed, msg, Ti)


SHAS = lambda: dict(script=h16(os.path.abspath(__file__)),
                    constructor=h16(os.path.join(AQUI, 'construye_familias_ba.py')),
                    instrumento=h16(os.path.join(AQUI, 'organismo_familias_ba.py')),
                    arnes=h16(os.path.join(AQUI, 'identidad_familias_ba.py')),
                    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_ba.md')),
                    origen_a1=h16(os.path.join(JA, 'organismo_familias_a1.py')),
                    origen_b6=h16(os.path.join(N12, 'organismo_familias_b6.py')),
                    origen_b5=h16(os.path.join(N12, 'organismo_familias_b5.py')),
                    origen_b4b=h16(os.path.join(N12, 'organismo_familias_b4b.py')),
                    runner_bloque6=h16(os.path.join(N12, 'corre_familias_b6.py')),
                    preregistro_bloque6=h16(os.path.join(N12, 'PREREGISTRO_bloque6_sufijo.md')),
                    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))
ORIGENES = [('origen_a1', SHA_A1_ORIGEN), ('origen_b6', SHA_B6_ESPERADO), ('origen_b5', SHA_B5_ESPERADO),
            ('origen_b4b', SHA_B4B_ESPERADO), ('origen_organismo_v14', SHA_V14_ESPERADO)]


def cabecera(titulo, cel_act, brazos, semillas, Tb, extra=''):
    log(titulo)
    log("El mundo, el canal y el EMISOR son los del bloque 6, SIN TOCAR. Lo unico nuevo es COMO LEE la tabla.")
    log("celdas %s  brazos %s  semillas %s  T = %d %s" % (cel_act, brazos, semillas, Tb, extra))
    s = SHAS()
    for k, v in s.items():
        log("    sha %-24s %s" % (k, v))
    ok = True
    for k, esp in ORIGENES:
        if s[k] != esp:
            log("*** ORIGEN CAMBIADO: %s es %s, se esperaba %s." % (k, s[k], esp)); ok = False
    log("    origenes verificados -> %s" % ('OK' if ok else 'FALLA'))
    return ok


def tabla(res, cel_act, brazos):
    """La tabla de los brazos del bloque 6 y LA LETRA (R1-R5 + el objetivo de la MISION) por celda."""
    log("")
    log("%-7s " % 'celda' + ' '.join('%8s' % b for b in brazos) + '   dist(PAR)  dist(PAR0)  muertes  okU')
    out = {}
    for c in cel_act:
        fila = {}
        for b in brazos:
            rs = [r for r in res if r['cel'] == c and r['base'] == b]
            n = len([r for r in rs if r['B4']['evX'] is not None])
            fila[b] = (sum(1 for r in rs if r['B4']['evX'] == 0.0), n)
        dP = [r['B4']['dist'] for r in res if r['cel'] == c and r['base'] == 'PAR' and r['B4']['dist'] is not None]
        d0 = [r['B4']['dist'] for r in res if r['cel'] == c and r['base'] == 'PAR0' and r['B4']['dist'] is not None]
        mu = med([r['deaths'] for r in res if r['cel'] == c and r['base'] == 'CANAL'])
        ok = med([r['B4']['okU'] for r in res if r['cel'] == c and r['base'] == 'CANAL'
                  and r['B4']['okU'] is not None])
        out[c] = dict(com=fila, dist=(int(sum(dP)), len(dP)), dist0=(int(sum(d0)), len(d0)), muertes=mu, okU=ok)
        log("%-7s " % c + ' '.join('%4d/%-3d' % fila[b] for b in brazos)
            + '   %d/%d      %d/%d       %s     %s' % (int(sum(dP)), len(dP), int(sum(d0)), len(d0), mu, ok))
    for c in cel_act:
        if not all(b in out[c]['com'] for b in ('CANAL', 'CORTADO', 'BAR-T', 'BAR-H', 'VALOR')):
            continue
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


def humo(semillas, Tb, cel_act, brazos):
    """HUMO de un proceso, sin Pool (regla 3): <= 6 corridas, <= 200 000 pasos. ERR-42: ESCRIBE su JSON."""
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(AQUI, 'humo_ba_%s.log' % stamp), 'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    if not cabecera("HUMO del candidato BA (junta fase 5). UN proceso, sin Pool (regla 3).", cel_act, brazos,
                    semillas, Tb, "(<= 6 corridas, <= 200 000 pasos)"):
        sys.exit(1)
    n_cor = len(semillas) * (1 + len(cel_act) * len(brazos))
    log("    corridas previstas: %d emisor(es) + %d receptores = %d  (limite de la regla 3: 6)"
        % (len(semillas), n_cor - len(semillas), n_cor))
    if n_cor > 6 or Tb > 200000:
        log("*** El humo se pasa del presupuesto de un creador (6 corridas, 200 000 pasos). Se para.")
        sys.exit(1)

    log("1/4 DIAGNOSTICO ESTRUCTURAL (T = 0, sin simular)")
    diags = []
    for s in semillas:
        d = CF.diagnostico(s, 30, 3, BASE); d.pop('cod'); d['estructura'] = B6R.estructura_v(s)
        diags.append(dict(tipo='D', **d)); e = d['estructura']
        log("    semilla %d: alias_pares %.5f  piso de forma %s/32  px en que difieren referente y hermana %s "
            "(variante = %s); referente y otro token %s"
            % (s, d['alias_pares'], e['piso_forma_v0'], e['BAR_H_px_dif'], e['n_var_px'], e['BAR_T_px_dif']))

    log("2/4 EMISORES (los del bloque 6, sin tocar)")
    msgs = {}
    for s in semillas:
        t1 = time.time(); m = B6R.emisor(s, Tb); msgs[s] = m; q = m['neg']
        log("    E s%d %5.1fs  mensaje %s" % (s, time.time() - t1,
                                              q and (q['ref'], q['R'], 't=%d' % q['t'], 'tras %d exp' % q['enc'])))
    if not all((msgs[s] or {}).get('neg') for s in semillas):
        log("*** P-I2: alguna semilla del humo no emite. Se para (no hay nada que leer)."); sys.exit(1)

    log("3/4 REGLA 14 - la ENTRADA, campo a campo contra el bloque 6")
    if not verifica_entrada(msgs[semillas[0]]['neg'], Tb, cel_act):
        log("*** La entrada difiere del bloque 6 en algo que no es una perilla de celda. Se para (ERR-38)."); sys.exit(1)

    log("4/4 RECEPTORES")
    res = []
    for c in cel_act:
        for b in brazos:
            for s in semillas:
                t1 = time.time(); r = corre(b, c, s, msgs[s]['neg'], Tb); res.append(r); B = r['B4']
                log("    %-12s s%d %5.1fs  entrega t=%s  comio %d  dist %s  okU %s  via %s  muertes %s  "
                    "LEE(ref) %s  abstiene %s/32"
                    % (r['brazo'], s, time.time() - t1, r['t_entrega'], 1 - int(B['evX'] or 0), B['dist'],
                       B['okU'], 'RAPIDA' if B['fam1'] else 'lenta', r['deaths'], r['lee_ref'], r['abstiene']))

    crudo = os.path.join(AQUI, 'humo_ba_%s_crudo.json' % stamp)     # ERR-54 / ERR-42: el crudo, ANTES del analisis
    with open(crudo, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T=Tb, semillas=semillas,
                                 celdas={c: N(CELDAS[c]) for c in cel_act}, brazos=brazos, criterio=CRITERIO,
                                 kw_E=N(KW_E), kw_R=N(KW_R), shas=SHAS(), python=platform.python_version(),
                                 numpy=np.__version__),
                       diagnostico=diags, mensajes=N(msgs), brazos=res), f, ensure_ascii=False, default=str)
    log("CRUDO -> %s  sha256_16 = %s  (ERR-54/ERR-42: el humo ESCRIBE su JSON)" % (os.path.basename(crudo), h16(crudo)))
    tab = tabla(res, cel_act, brazos)
    dj = os.path.join(AQUI, 'humo_ba_%s.json' % stamp)
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T=Tb, semillas=semillas,
                                 celdas={c: N(CELDAS[c]) for c in cel_act}, brazos=brazos, criterio=CRITERIO,
                                 shas=SHAS(), crudo=os.path.basename(crudo), python=platform.python_version(),
                                 numpy=np.__version__),
                       tabla=N(tab), diagnostico=diags, mensajes=N(msgs), brazos=res), f,
                  ensure_ascii=False, default=str)
    log("datos -> %s  sha256_16 = %s" % (os.path.basename(dj), h16(dj)))
    log("")
    log("LECTURA (1 semilla: NO es evidencia; con n = 1 ni la linea base se reproduce). Lo que el humo SI "
        "decide es el MECANISMO: `LEE(ref)` = [valor, habla, exactas de FORMA, exactas de VARIANTE] en el paso "
        "de la entrega. Lo que hay que ver: CANAL positivo con 3/3 y 3/3; BAR-H y BAR-T negativos o sin las "
        "3 de FORMA; CORTADO negativo.")
    CF._log['f'].close()


def serie(desde, n_sem, Tb, cel_act, npool):
    """LA CONFIRMATORIA. La lanza el COORDINADOR (reglas 3 y 11). Pool por --pool o JUACO_POOL (ERR-86)."""
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    SEEDS = list(range(desde, desde + n_sem))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(AQUI, 'serie_ba_s%d-%d_%s.log' % (SEEDS[0], SEEDS[-1], stamp)),
                        'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    if not cabecera("SERIE del candidato BA (junta fase 5), Pool(%d)." % npool, cel_act, BRAZOS_BASE,
                    '%d-%d' % (SEEDS[0], SEEDS[-1]), Tb):
        sys.exit(1)
    with mp.Pool(npool) as pool:
        log("ETAPA 1/4 - DIAGNOSTICO ESTRUCTURAL (T = 0, %d semillas)" % len(SEEDS))
        diags = []
        for s in SEEDS:
            d = CF.diagnostico(s, 30, 3, BASE); d.pop('cod'); d['estructura'] = B6R.estructura_v(s)
            diags.append(dict(tipo='D', **d))
        log("    alias por par mediana %s  piso de forma %s/32"
            % (med([d['alias_pares'] for d in diags]), med([d['estructura']['piso_forma_v0'] for d in diags])))
        log("ETAPA 2/4 - EMISORES (%d corridas de %d pasos; son los del bloque 6 bit a bit)" % (len(SEEDS), Tb))
        em = pool.map(tarea, [('E', s, Tb) for s in SEEDS], chunksize=1)
        msgs = {d['seed']: d['msgs'] for d in em}
        sin = [s for s in SEEDS if not (msgs.get(s) or {}).get('neg')]
        log("    emiten %d/%d; sin mensaje (se EXCLUYEN, P-I2): %s" % (len(SEEDS) - len(sin), len(SEEDS), sin))
        util = [s for s in SEEDS if (msgs.get(s) or {}).get('neg')]
        if not util:
            log("*** Ninguna semilla emite. Se para."); sys.exit(1)
        log("ETAPA 3/4 - REGLA 14: la ENTRADA, campo a campo contra el bloque 6")
        if not verifica_entrada(msgs[util[0]]['neg'], Tb, cel_act):
            log("*** La entrada difiere del bloque 6. Se para ANTES de gastar la serie (ERR-38)."); sys.exit(1)
        tr = [('R', b, c, s, msgs[s]['neg'], Tb) for c in cel_act for b in BRAZOS_BASE for s in util]
        log("ETAPA 4/4 - RECEPTORES: %d corridas de %d pasos..." % (len(tr), Tb))
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(tr):
                log("          %d/%d" % (i, len(tr)))
    crudo = os.path.join(AQUI, 'serie_ba_s%d-%d_%s_crudo.json' % (SEEDS[0], SEEDS[-1], stamp))
    with open(crudo, 'w', encoding='utf-8') as f:      # ERR-54: los crudos, ANTES del analisis
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='serie', T=Tb, semillas=SEEDS,
                                 celdas={c: N(CELDAS[c]) for c in cel_act}, brazos=BRAZOS_BASE,
                                 criterio=CRITERIO, kw_E=N(KW_E), kw_R=N(KW_R), shas=SHAS(), pool=npool,
                                 python=platform.python_version(), numpy=np.__version__),
                       diagnostico=diags, mensajes=N(msgs), brazos=res), f, ensure_ascii=False, default=str)
    log("CRUDO -> %s  sha256_16 = %s  (ERR-54)" % (os.path.basename(crudo), h16(crudo)))
    pi5 = {b: sorted(r['seed'] for r in res if r['base'] == b and r['cel'] == cel_act[-1] and r['B4']['fam1'])
           for b in BRAZOS_BASE}
    log("    P-I5 por brazo en %s (semillas con fam1 = 1: el mensaje escrito y NO consultado): %s"
        % (cel_act[-1], {k: len(v) for k, v in pi5.items()}))
    tabla(res, cel_act, BRAZOS_BASE)
    CF._log['f'].close()


if __name__ == '__main__':
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    cel_act = ['BA']
    if '--celdas' in sys.argv:
        cel_act = [c.strip() for c in sys.argv[sys.argv.index('--celdas') + 1].split(',') if c.strip()]
        malas = [c for c in cel_act if c not in CELDAS]
        if malas:
            raise SystemExit("--celdas: desconocida(s) %s. Validas: %s" % (malas, list(CELDAS)))
    if '--serie' in sys.argv:          # LA CONFIRMATORIA LA LANZA EL COORDINADOR (reglas 3 y 11)
        if cel_act == ['BA']:
            cel_act = ['b5k3', 'b6suf', 'A1', 'BA']
        npool = arg('--pool', int(os.environ.get('JUACO_POOL', 6)))
        serie(arg('--desde', 861), arg('--n', 20), arg('--T', 100000), cel_act, npool)
        sys.exit(0)
    if '--humo' not in sys.argv:
        raise SystemExit("Hace falta --humo (un proceso) o --serie (coordinador). Ver la cabecera.")
    sem = SEM_HUMO if '--semillas' not in sys.argv else \
        [int(x) for x in sys.argv[sys.argv.index('--semillas') + 1].split(',')]
    if any(s in PROHIBIDAS for s in sem):
        raise SystemExit("HUMO: %s cae en 821-900 (las series de confirmacion). Se usan 901-920." % sem)
    brazos = BRAZOS_HUMO if '--brazos' not in sys.argv else \
        [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
    humo(sem, arg('--T', T_HUMO), cel_act, brazos)
