"""NIVEL 5 -- CANDIDATO **BA-vm** (la variante vota con su PEOR casilla, no con la suma), junta del 21-sep,
creador B. CRITERIO: las puertas ABSOLUTAS P0-P7 y la MISION de `nivel05_familia_variante_BAv/PREREGISTRO_bav.md`
3 (ERR-90) COPIADAS SIN TOCAR UNA LETRA, tal como manda `PREREGISTRO_bavm.md` 1. No se recalibra nada.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA.

Copia por anclas del runner de BA-v (`nivel05_familia_variante_BAv/corre_familias_bav.py`, 4453754a9921e349).
BA-vm es un CANDIDATO APARTE con preregistro propio: **no reabre BA-v** (LINEA CERRADA, REGISTRO_etapas_1_2.md).
BA-v entra aqui como la FILA PAREADA que da el contraste, no como candidato.

El mundo, el canal, EL EMISOR, las medidas de la boca y los brazos son LOS OBJETOS del bloque 6, importados y
no recopiados (ERR-31): `corre_familias_b6` -> `corre_familias_b5` -> `corre_familias_b4b` -> ... -> bloque 1.
El EMISOR es el del bloque 6 SIN TOCAR (b4b bit a bit): lo que se mide es LA LECTURA, no el habla.

REGLA 14 (ERR-38/41): la ENTRADA del receptor se compara CAMPO A CAMPO con la del bloque 6 antes de correr
(`verifica_entrada`), y el script se PARA si difiere en algo que no sea una perilla declarada de la celda.
ERR-54: los crudos se escriben ANTES de cualquier analisis. ERR-44: todo se mide sobre lo que hizo la BOCA.
ERR-42: el humo llega a ESCRIBIR su JSON.  ERR-86: `--pool N` manda sobre `JUACO_POOL`.
ERR-87: este runner **NO LEE NINGUN JSON** (no hay `lee_json`): todo lo que usa lo calcula en la misma corrida.
ERR-89: `b4b` es obligatoria (es la base de R6). ERR-88: el arnes `identidad_familias_bavm.py` tiene que haber
dado 100% -- con los CONTROLES QUE DEBEN DIFERIR -- antes de correr esto.

CELDAS (la MISMA tabla y el MISMO mensaje; solo cambia COMO SE LEE):
  b4b      = k=1, sin sufijo, un tipo        -> bloque 4b BIT A BIT: **LA BASE DE R6** (obligatoria)
  b5k3     = k=3, sin sufijo                 -> bloque 5 BIT A BIT (familia exacta; control de instrumento)
  b6suf    = k=3, CON sufijo                 -> bloque 6 BIT A BIT (variante; control de instrumento)
  A1       = dos tipos + min + `exige_dir`   -> el candidato del creador A
  BA-v     = dos tipos + min + `conj_tipo`=2 -> la fila PAREADA (linea cerrada; da el contraste)
  BA-vm    = BA-v + `dentro`='minv'          -> **EL CANDIDATO** (el minimo escalado SOLO en el tipo VARIANTE)
  BA-vM    = BA-v + `dentro`='min'           -> **LA ABLACION PREREGISTRADA** (el minimo en los DOS tipos)
  BA-vm-sh = BA-vm + `baraja_msg`=1          -> **CONTROL: la MEMORIA BARAJADA** (misma R, casilla permutada)
  BA       = dos tipos + min + `conj_tipo`=1 -> el candidato de la junta (se puede pedir, no va por defecto)

SEMILLAS (PREREGISTRO_bavm.md 4): serie 1541-1560, replica 1561-1580; humo 918-920.
El runner RECHAZA 821-1000 (junta/C, BA, BA-v) y 1501-1540 (fase 9), en el humo Y en la serie.

    python experimentos/junta_20260921/B/corre_familias_bavm.py --humo --semillas 918,919,920
    python experimentos/junta_20260921/B/corre_familias_bavm.py --serie --desde 1541 --pool 6
"""
import sys, os, json, time, hashlib, platform

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))   # .../bundle
BAVD = os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv')   # el ORIGEN del instrumento
JBA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'BA')
JA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A')
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
HUMOS = os.path.join(RAIZ, 'datos', 'humo')
sys.path[:0] = [AQUI, BAVD, JBA, JA, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import numpy as np
import corre_familias_b6 as B6R              # bloque 6: mundo, canal, emisor, medidas y brazos (ERR-31)

B5R, B4BR, B2R, CF = B6R.B5R, B6R.B4BR, B6R.B2R, B6R.CF
log, h16, N, med = CF.log, CF.h16, CF.N, CF.med
BASE, KW_E, KW_R = B2R.BASE, B6R.KW_E, B6R.KW_R
XNEG, BAR, PATS, prefijo = B6R.XNEG, B6R.BAR, B6R.PATS, B6R.prefijo
PLANTILLA = B6R.PLANTILLA                    # los 9 brazos de la direccion (-) del bloque 4b/5/6
SEM_R, SEM_OTRO, VORAZ = B6R.B5R.SEM_R, B6R.B5R.SEM_OTRO, B6R.VORAZ

T_HUMO = 100000
SEM_HUMO = [918]                             # PREREGISTRO_bavm.md 4: el humo de este bloque va en 918-920
BANDA_HUMO = (918, 919, 920)                 # las UNICAS de la banda de humos que quedan libres (901-903
#   la junta, 912 el humo de BA-v, 913-915 la mini-prueba de hoy, 916-917 el bloque del alias de creacion_B)
# RECHAZADAS: 821-1000 = junta/C, BA, BA-v y sus replicas; 1501-1540 = fase 9. La SERIE las rechaza TODAS;
# el HUMO rechaza todas MENOS las tres de BANDA_HUMO, que es para lo que existe la banda 901-920.
PROHIBIDAS = set(range(821, 1001)) | set(range(1501, 1541))
SHA_BAV_ESPERADO = '2dca0a3e239481f0'        # organismo_familias_bav.py: EL ORIGEN del instrumento
SHA_BA_ESPERADO = '1f196ee786b2040d'         # organismo_familias_ba.py
SHA_B6_ESPERADO = 'b10cbd4ddd0c32a3'
SHA_B5_ESPERADO = 'e0b6b90f6f92d5c1'
SHA_B4B_ESPERADO = 'b3dd1d7e66a2d147'
SHA_V14_ESPERADO = 'feefc88b1fd8d434'
SHA_A1_ESPERADO = '8833e1dcfb62f26d'

# ---------------------------------------------------------------- celdas: SOLO cambia COMO LEE la tabla
_DT = dict(k_ganadoras=3, memoria_variante=0, dos_tipos=1, k_forma=3, var_cubre=1)
CELDAS = {
    'b4b':     dict(k_ganadoras=1, memoria_variante=0, dos_tipos=0),               # k1v0: b4b BIT A BIT -- LA BASE DE R6
    'b5k3':    dict(k_ganadoras=3, memoria_variante=0, dos_tipos=0),               # bloque 5 BIT A BIT
    'b6suf':   dict(k_ganadoras=3, memoria_variante=1, dos_tipos=0),               # bloque 6 BIT A BIT
    'A1':      dict(_DT, combina='min', msg_elige=0, exige_dir=1),                 # el candidato del creador A
    'BA':      dict(_DT, combina='min', msg_elige=0, conj_tipo=1),                 # el candidato de la junta
    'BA-v':    dict(_DT, combina='min', msg_elige=0, conj_tipo=2),                 # la fila PAREADA (cerrada)
    'BA-vm':   dict(_DT, combina='min', msg_elige=0, conj_tipo=2, dentro='minv'),  # **EL CANDIDATO**
    'BA-vM':   dict(_DT, combina='min', msg_elige=0, conj_tipo=2, dentro='min'),   # LA ABLACION preregistrada
    'BA-vm-sh': dict(_DT, combina='min', msg_elige=0, conj_tipo=2, dentro='minv',
                     baraja_msg=1),                                                # CONTROL: memoria BARAJADA
}
# el orden del PREREGISTRO_bavm.md 4. Orden de sacrificio declarado si hay que recortar: BA-vM y luego A1
CELDAS_SERIE = ['b4b', 'b5k3', 'b6suf', 'A1', 'BA-v', 'BA-vm', 'BA-vM', 'BA-vm-sh']   # b4b SIEMPRE (ERR-89)
BASE_R6 = 'b4b'
PLANT = {p[0]: p for p in PLANTILLA}
BRAZOS_BASE = ['CANAL', 'CORTADO', 'BAR-H', 'BAR-T', 'VALOR', 'PAR', 'PAR0']   # los 7 del bloque 6, sin tocar
# HUMO: 5 receptores + 1 emisor = 6 corridas (regla 3). Pares (celda, brazo) explicitos.
# El presupuesto del creador (regla 3) es de 6 corridas: len(semillas) * (1 emisor + len(plan)) <= 6.
# Con 3 semillas eso deja UN par (celda, brazo); con 1 semilla caben cinco. El plan se elige por el NUMERO
# DE SEMILLAS, declarado AQUI antes de correr, y siempre se puede fijar a mano con --plan.
PLAN_HUMO_1 = [('b4b', 'CANAL'), ('BA-v', 'CANAL'), ('BA-vm', 'CANAL'), ('BA-vm', 'CORTADO'),
               ('BA-vm-sh', 'CANAL')]
PLAN_HUMO_2 = [('BA-vm', 'CANAL'), ('BA-vm-sh', 'CANAL')]
PLAN_HUMO_3 = [('BA-vm', 'CANAL')]
PLAN_POR_SEM = {1: PLAN_HUMO_1, 2: PLAN_HUMO_2, 3: PLAN_HUMO_3}
PLAN_HUMO = PLAN_HUMO_1
# ---- ERR-90: LAS PUERTAS ABSOLUTAS (ninguna es relativa a CORTADO). Justificacion en PREREGISTRO_bav.md 3.
UMBRAL = dict(CANAL=15, CORTADO=5, BART=5, VALOR=5, BARH=10, PAR=15, PAR0=5, N_MIN=18,
              R6_MUERTES=1.5, R6_OKU=0.10)
CRITERIO = dict(CANAL=('>=', 15), CORTADO=('<=', 5), BARH=('<=', 10), BART=('<=', 5), PAR=('>=', 15),
                PAR0=('<=', 5), VALOR=('<=', 5), R6_muertes=('<=', 1.5), R6_okU=('>=', -0.10))
# perillas que SI pueden diferir de la entrada del bloque 6 (son la celda; regla 14)
PERILLAS_CELDA = set(('k_ganadoras', 'memoria_variante', 'dos_tipos', 'k_forma', 'k_var', 'var_cubre',
                      'pesos_tipo', 'eta_w', 'combina', 'msg_elige', 'exige_dir', 'dentro', 'conj_tipo',
                      'baraja_msg'))


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
    import organismo_familias_bavm as BAV   # BA-vm: el instrumento de ESTA carpeta
    kw = B2R.resuelve(KW_R, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    _n, _m, _p, _o, _ph = PLANT[base]
    fsr = seed + SEM_OTRO if _o else seed
    r = BAV.run(seed + SEM_R, T=Ti, fam_seed=fsr, canal=canal_de(base, msg), par_herm=_ph,
                **dict(CELDAS[cel], **kw))
    _mo = r['mord'] or {}
    _vm = r.get('val_mundo') or {}
    d = dict(tipo='R', brazo='%s-%s' % (base, cel), base=base, cel=cel, seed=seed, deaths=r['deaths'],
             celdas=r['celdas'], entregado=r['canal_entregado'], t_entrega=r['canal_t_entrega'],
             fam_seed=r['fam_seed'], lee_ref=r['canal_lee_ref'], baraja=r['baraja_msg'],
             lee_herm=r['canal_lee_herm'], dentro=r['dentro'],
             gan_forma=r['tipo_gan_forma'], gan_var=r['tipo_gan_var'],
             n_mismo_dos=(None if r['canal_mismo_dos'] is None else len(r['canal_mismo_dos'])),
             n_mismo_dir_k=(None if r['canal_mismo_dir_k'] is None else len(r['canal_mismo_dir_k'])),
             n_mismo_bin_k=(None if r['canal_mismo_bin_k'] is None else len(r['canal_mismo_bin_k'])),
             herm_en_grupo=(None if r['canal_mismo_dos'] is None else bool(BAR['neg']['H'] in r['canal_mismo_dos'])),
             abstiene=(None if r['W_tabla'] is None else sum(1 for k in r['W_tabla'] if r['W_tabla'][k] is None)),
             cobertura=r['mem_cobertura'], vistas=r['mem_vistas'], W_ref=(r['W_tabla'] or {}).get(XNEG),
             W_herm=(r['W_tabla'] or {}).get(BAR['neg']['H']), W_tk=(r['W_tabla'] or {}).get(BAR['neg']['TK']),
             # ---- DIAGNOSTICO DEL COSTE (ERR-89/DIAG_muertes): por que muere, no solo cuanto
             n_mord=int(sum(sum(v) for v in _mo.values())),
             n_com=int(sum(sum(v) for k, v in _mo.items() if _vm.get(k) == 'comida')),
             n_ven=int(sum(sum(v) for k, v in _mo.items() if _vm.get(k) == 'veneno')),
             frac_regalo=r.get('frac_regalo'), frac_veneno=r.get('frac_veneno'))
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
                    constructor=h16(os.path.join(AQUI, 'construye_familias_bavm.py')),
                    instrumento=h16(os.path.join(AQUI, 'organismo_familias_bavm.py')),
                    arnes=h16(os.path.join(AQUI, 'identidad_familias_bavm.py')),
                    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_bavm.md')),
                    preregistro_criterio=h16(os.path.join(BAVD, 'PREREGISTRO_bav.md')),
                    origen_bav=h16(os.path.join(BAVD, 'organismo_familias_bav.py')),
                    runner_bav=h16(os.path.join(BAVD, 'corre_familias_bav.py')),
                    origen_ba=h16(os.path.join(JBA, 'organismo_familias_ba.py')),
                    runner_ba=h16(os.path.join(JBA, 'corre_familias_ba.py')),
                    origen_a1=h16(os.path.join(JA, 'organismo_familias_a1.py')),
                    origen_b6=h16(os.path.join(N12, 'organismo_familias_b6.py')),
                    origen_b5=h16(os.path.join(N12, 'organismo_familias_b5.py')),
                    origen_b4b=h16(os.path.join(N12, 'organismo_familias_b4b.py')),
                    runner_bloque6=h16(os.path.join(N12, 'corre_familias_b6.py')),
                    preregistro_bloque6=h16(os.path.join(N12, 'PREREGISTRO_bloque6_sufijo.md')),
                    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))
ORIGENES = [('origen_bav', SHA_BAV_ESPERADO), ('origen_ba', SHA_BA_ESPERADO), ('origen_a1', SHA_A1_ESPERADO), ('origen_b6', SHA_B6_ESPERADO),
            ('origen_b5', SHA_B5_ESPERADO), ('origen_b4b', SHA_B4B_ESPERADO),
            ('origen_organismo_v14', SHA_V14_ESPERADO)]


def cabecera(titulo, cel_act, brazos, semillas, Tb, extra=''):
    log(titulo)
    log("El mundo, el canal y el EMISOR son los del bloque 6, SIN TOCAR. Lo unico nuevo es COMO LEE la tabla,")
    log("y el CRITERIO: puertas ABSOLUTAS (ERR-90), nunca relativas a CORTADO.")
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


def resume(res, cel_act, brazos):
    """Los numeros por celda (sin juzgar): com/n por brazo, dist, muertes, okU y el diagnostico del coste."""
    out = {}
    for c in cel_act:
        fila = {}
        for b in brazos:
            rs = [r for r in res if r['cel'] == c and r['base'] == b]
            n = len([r for r in rs if r['B4']['evX'] is not None])
            fila[b] = (sum(1 for r in rs if r['B4']['evX'] == 0.0), n)
        dP = [r['B4']['dist'] for r in res if r['cel'] == c and r['base'] == 'PAR' and r['B4']['dist'] is not None]
        d0 = [r['B4']['dist'] for r in res if r['cel'] == c and r['base'] == 'PAR0' and r['B4']['dist'] is not None]
        ca = [r for r in res if r['cel'] == c and r['base'] == 'CANAL']
        mu = med([r['deaths'] for r in ca]) if ca else None
        ok = med([r['B4']['okU'] for r in ca if r['B4']['okU'] is not None]) if ca else None
        out[c] = dict(com=fila, dist=(int(sum(dP)), len(dP)), dist0=(int(sum(d0)), len(d0)), muertes=mu, okU=ok,
                      n_cat=sum(1 for r in ca if r['deaths'] >= 200),
                      n_com=(med([r['n_com'] for r in ca]) if ca else None),
                      n_ven=(med([r['n_ven'] for r in ca]) if ca else None),
                      regalo=(med([r['frac_regalo'] for r in ca if r['frac_regalo'] is not None]) if ca else None),
                      deaths=sorted((r['seed'], r['deaths']) for r in ca))
    return out


def tabla(res, cel_act, brazos):
    """La tabla de los brazos + LA LETRA. ERR-90: puertas ABSOLUTAS. ERR-89: R6 SE IMPRIME, con su letra."""
    out = resume(res, cel_act, brazos)
    log("")
    log("%-9s " % 'celda' + ' '.join('%8s' % b for b in brazos)
        + '   dist(PAR)  dist(PAR0)  muertes  okU   >=200  mord_com  mord_ven  regalo')
    for c in cel_act:
        o = out[c]
        log("%-9s " % c + ' '.join('%4d/%-3d' % o['com'][b] for b in brazos)
            + '   %d/%d      %d/%d       %s     %s   %s     %s      %s      %s'
            % (o['dist'][0], o['dist'][1], o['dist0'][0], o['dist0'][1], o['muertes'], o['okU'],
               o['n_cat'], o['n_com'], o['n_ven'], o['regalo']))
    log("")
    log("LETRA DEL CRITERIO PROPIO (ERR-90): puertas ABSOLUTAS. Ninguna depende de CORTADO.")
    nd = lambda x: ('n/d' if x is None else x)
    ok = lambda b: 'pasa' if b else 'CAE'
    base = out.get(BASE_R6)
    for c in cel_act:
        o = out[c]
        g = lambda b: (o['com'][b] if b in o['com'] else None)
        C, CO, BT, BH, VA = g('CANAL'), g('CORTADO'), g('BAR-T'), g('BAR-H'), g('VALOR')
        dP, d0 = o['dist'], o['dist0']
        log("  [%s]" % c)
        log("     P0 montaje   N (semillas validas del brazo CANAL) = %s >= %d: %s"
            % (nd(C and C[1]), UMBRAL['N_MIN'], 'n/d' if C is None else ok(C[1] >= UMBRAL['N_MIN'])))
        log("     P1 CANAL     %s >= %d: %s" % (nd(C and C[0]), UMBRAL['CANAL'],
                                                'n/d' if C is None else ok(C[0] >= UMBRAL['CANAL'])))
        log("     P2 CORTADO   %s <= %d: %s" % (nd(CO and CO[0]), UMBRAL['CORTADO'],
                                                'n/d' if CO is None else ok(CO[0] <= UMBRAL['CORTADO'])))
        log("     P3 BAR-T     %s <= %d: %s" % (nd(BT and BT[0]), UMBRAL['BART'],
                                                'n/d' if BT is None else ok(BT[0] <= UMBRAL['BART'])))
        log("     P4 VALOR     %s <= %d: %s" % (nd(VA and VA[0]), UMBRAL['VALOR'],
                                                'n/d' if VA is None else ok(VA[0] <= UMBRAL['VALOR'])))
        log("     P5 BAR-H     %s <= %d: %s" % (nd(BH and BH[0]), UMBRAL['BARH'],
                                                'n/d' if BH is None else ok(BH[0] <= UMBRAL['BARH'])))
        log("     P6 dist(PAR) %d/%d >= %d y dist(PAR0) %d <= %d: %s"
            % (dP[0], dP[1], UMBRAL['PAR'], d0[0], UMBRAL['PAR0'],
               'n/d' if not dP[1] else ok(dP[0] >= UMBRAL['PAR'] and d0[0] <= UMBRAL['PAR0'])))
        if base is None or base['muertes'] is None or o['muertes'] is None:
            log("     P7 R6        n/d: falta la celda base `%s` en esta corrida (ERR-89). NO se lee coste." % BASE_R6)
        else:
            rz = (o['muertes'] / base['muertes']) if base['muertes'] else float('inf')
            d_ok = (o['okU'] - base['okU']) if (o['okU'] is not None and base['okU'] is not None) else None
            log("     P7 R6        muertes %s / %s(%s) = %.2fx <= %.2fx: %s  |  okU %s - %s = %s >= -%.2f: %s"
                % (o['muertes'], base['muertes'], BASE_R6, rz, UMBRAL['R6_MUERTES'],
                   ok(rz <= UMBRAL['R6_MUERTES']), o['okU'], base['okU'],
                   ('n/d' if d_ok is None else '%+.4f' % d_ok), UMBRAL['R6_OKU'],
                   'n/d' if d_ok is None else ok(d_ok >= -UMBRAL['R6_OKU'])))
            par = [(s, d) for s, d in o['deaths']]
            bd = dict(base['deaths'])
            peor = sum(1 for s, d in par if s in bd and d > UMBRAL['R6_MUERTES'] * max(bd[s], 1))
            log("        (diagnostico de R6, NO es la puerta: %d/%d semillas mueren > 1.5x su propia base;"
                " semillas en regimen de hambre (>=200): %d)" % (peor, len(par), o['n_cat']))
        mis = ('n/d' if (BT is None or not dP[1]) else
               ('SI' if (BT[0] <= 5 and dP[0] >= 15) else 'no'))
        log("     MISION (BAR-T <= 5 Y PAR >= 15): %s" % mis)
        if C and CO and BT and BH and VA:      # referencia historica: la letra RELATIVA del bloque 6
            log("     [referencia historica, NO decide] bloque 6: R2 BAR-T<=CORTADO+3 %s; R3 BAR-H<=CORTADO+5 %s;"
                " R4 VALOR<=CORTADO+3 %s; R5 dist>=12 y >=gemelo+5 %s"
                % (ok(BT[0] <= CO[0] + 3), ok(BH[0] <= CO[0] + 5), ok(VA[0] <= CO[0] + 3),
                   ok(dP[0] >= 12 and dP[0] >= d0[0] + 5)))
    return out


def humo(semillas, Tb, plan):
    """HUMO de un proceso, sin Pool (regla 3): <= 6 corridas, <= 200 000 pasos. ERR-42: ESCRIBE su JSON."""
    os.makedirs(HUMOS, exist_ok=True)
    cel_act = list(dict.fromkeys(c for c, _ in plan))
    brazos = list(dict.fromkeys(b for _, b in plan))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(HUMOS, 'humo_bavm_%s.log' % stamp), 'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    if not cabecera("HUMO del candidato BA-vm (nivel 5, criterio ERR-90 SIN TOCAR). UN proceso, sin Pool.",
                    cel_act, brazos, semillas, Tb, "(<= 6 corridas, <= 200 000 pasos)"):
        sys.exit(1)
    log("    plan (celda, brazo): %s" % plan)
    n_cor = len(semillas) * (1 + len(plan))
    log("    corridas previstas: %d emisor(es) + %d receptores = %d  (limite de la regla 3: 6)"
        % (len(semillas), len(semillas) * len(plan), n_cor))
    log("    (es el PLAN. El GASTO REAL puede ser menor: la semilla que no emite no gasta receptor, P-I2.)")
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
    util = [s for s in semillas if (msgs[s] or {}).get('neg')]   # P-I2 IGUAL QUE EN LA SERIE: la semilla
    #   que no emite se EXCLUYE y se reporta; solo se para si NO emite ninguna.
    log("    P-I2: emiten %d/%d; sin mensaje (se EXCLUYEN): %s"
        % (len(util), len(semillas), [s for s in semillas if s not in util] or 'ninguna'))
    if not util:
        log("*** P-I2: ninguna semilla del humo emite. Se para (no hay nada que leer)."); sys.exit(1)

    log("3/4 REGLA 14 - la ENTRADA, campo a campo contra el bloque 6")
    if not verifica_entrada(msgs[util[0]]['neg'], Tb, cel_act):
        log("*** La entrada difiere del bloque 6 en algo que no es una perilla de celda. Se para (ERR-38)."); sys.exit(1)

    log("4/4 RECEPTORES")
    res = []
    for c, b in plan:
        for s in util:   # P-I2: solo las que emitieron
            t1 = time.time(); r = corre(b, c, s, msgs[s]['neg'], Tb); res.append(r); B = r['B4']
            log("    %-16s s%d %5.1fs  entrega t=%s  comio %d  dist %s  okU %s  via %s  muertes %s  "
                "LEE(ref) %s  abstiene %s/32  mord %s (com %s, ven %s)  regalo %s"
                % (r['brazo'], s, time.time() - t1, r['t_entrega'], 1 - int(B['evX'] or 0), B['dist'],
                   B['okU'], 'RAPIDA' if B['fam1'] else 'lenta', r['deaths'], r['lee_ref'], r['abstiene'],
                   r['n_mord'], r['n_com'], r['n_ven'], r['frac_regalo']))
            log("                     dentro=%s  LEE(herm) %s" % (r['dentro'], r['lee_herm']))

    crudo = os.path.join(HUMOS, 'humo_bavm_%s_crudo.json' % stamp)   # ERR-54 / ERR-42: el crudo, ANTES del analisis
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T=Tb, semillas=semillas, plan=plan,
                celdas={c: N(CELDAS[c]) for c in cel_act}, brazos=brazos, criterio=CRITERIO, umbral=UMBRAL,
                kw_E=N(KW_E), kw_R=N(KW_R), shas=SHAS(), python=platform.python_version(), numpy=np.__version__)
    with open(crudo, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=meta, diagnostico=diags, mensajes=N(msgs), brazos=res), f, ensure_ascii=False,
                  default=str)
    log("CRUDO -> %s  sha256_16 = %s  (ERR-54/ERR-42: el humo ESCRIBE su JSON)" % (os.path.basename(crudo), h16(crudo)))
    tab = tabla(res, cel_act, brazos)
    dj = os.path.join(HUMOS, 'humo_bavm_%s.json' % stamp)
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(meta, crudo=os.path.basename(crudo)), tabla=N(tab), diagnostico=diags,
                       mensajes=N(msgs), brazos=res), f, ensure_ascii=False, default=str)
    log("datos -> %s  sha256_16 = %s" % (os.path.basename(dj), h16(dj)))
    log("")
    log("LECTURA (1 semilla: NO es evidencia; con n = 1 ni la linea base se reproduce). Lo que el humo SI "
        "decide es el MONTAJE (P-I2/P-I3/P-I4, la regla 14, que R6 tenga base y que las siete puertas se "
        "imprima) y el MECANISMO: `LEE(ref)` y `LEE(herm)` = [valor, habla, exactas de FORMA, exactas de "
        "VARIANTE]. Lo que hay que ver: BA-vm CANAL positivo con 3/3 y 3/3 y comiendo, y `dentro` = minv "
        "en la celda del candidato. Con 1-3 semillas NO se lee ningun brazo ni ninguna puerta: eso es la serie.")
    CF._log['f'].close()


def serie(desde, n_sem, Tb, cel_act, npool):
    """LA CONFIRMATORIA. La lanza el COORDINADOR (reglas 3 y 11). Pool por --pool o JUACO_POOL (ERR-86)."""
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    SEEDS = list(range(desde, desde + n_sem))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(AQUI, 'serie_bavm_s%d-%d_%s.log' % (SEEDS[0], SEEDS[-1], stamp)),
                        'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    if not cabecera("SERIE del candidato BA-vm (nivel 5, criterio ERR-90 SIN TOCAR), Pool(%d)." % npool, cel_act,
                    BRAZOS_BASE, '%d-%d' % (SEEDS[0], SEEDS[-1]), Tb):
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
    crudo = os.path.join(AQUI, 'serie_bavm_s%d-%d_%s_crudo.json' % (SEEDS[0], SEEDS[-1], stamp))
    with open(crudo, 'w', encoding='utf-8') as f:      # ERR-54: los crudos, ANTES del analisis
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='serie', T=Tb, semillas=SEEDS,
                                 celdas={c: N(CELDAS[c]) for c in cel_act}, brazos=BRAZOS_BASE,
                                 criterio=CRITERIO, umbral=UMBRAL, kw_E=N(KW_E), kw_R=N(KW_R), shas=SHAS(),
                                 pool=npool, python=platform.python_version(), numpy=np.__version__),
                       diagnostico=diags, mensajes=N(msgs), brazos=res), f, ensure_ascii=False, default=str)
    log("CRUDO -> %s  sha256_16 = %s  (ERR-54)" % (os.path.basename(crudo), h16(crudo)))
    pi5 = {c: {b: sorted(r['seed'] for r in res if r['base'] == b and r['cel'] == c and r['B4']['fam1'])
               for b in BRAZOS_BASE} for c in cel_act}
    for c in cel_act:      # P-I5 en TODAS las celdas, no solo en la ultima (en BA se reportaba una sola)
        log("    P-I5 en %-9s (semillas con fam1 = 1: el mensaje escrito y NO consultado): %s  -> %s"
            % (c, {k: len(v) for k, v in pi5[c].items()},
               sorted({s for v in pi5[c].values() for s in v}) or 'ninguna'))
    tabla(res, cel_act, BRAZOS_BASE)
    CF._log['f'].close()


if __name__ == '__main__':
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    cel_act = list(CELDAS_SERIE)
    if '--celdas' in sys.argv:
        cel_act = [c.strip() for c in sys.argv[sys.argv.index('--celdas') + 1].split(',') if c.strip()]
        malas = [c for c in cel_act if c not in CELDAS]
        if malas:
            raise SystemExit("--celdas: desconocida(s) %s. Validas: %s" % (malas, list(CELDAS)))
    if '--serie' in sys.argv:          # LA CONFIRMATORIA LA LANZA EL COORDINADOR (reglas 3 y 11)
        if BASE_R6 not in cel_act:     # ERR-89: sin la base no hay R6, y R6 es una puerta
            cel_act = [BASE_R6] + cel_act
            print("  [ERR-89] la celda base `%s` no estaba en --celdas: se ANADE (R6 es una puerta y necesita "
                  "con que dividir)." % BASE_R6)
        npool = arg('--pool', int(os.environ.get('JUACO_POOL', 6)))
        d0, n0 = arg('--desde', 1541), arg('--n', 20)
        if any(s in PROHIBIDAS for s in range(d0, d0 + n0)):
            raise SystemExit('SERIE: %d-%d pisa una serie ya corrida (821-1000) o la fase 9 (1501-1540). '
                             'El PREREGISTRO_bavm.md 4 fija 1541-1560 y 1561-1580.' % (d0, d0 + n0 - 1))
        serie(d0, n0, arg('--T', 100000), cel_act, npool)
        sys.exit(0)
    if '--humo' not in sys.argv:
        raise SystemExit("Hace falta --humo (un proceso) o --serie (coordinador). Ver la cabecera.")
    sem = SEM_HUMO if '--semillas' not in sys.argv else \
        [int(x) for x in sys.argv[sys.argv.index('--semillas') + 1].split(',')]
    malas_s = [s for s in sem if s in PROHIBIDAS and s not in BANDA_HUMO]
    if malas_s:
        raise SystemExit("HUMO: %s cae en una serie ya corrida (821-1000) o en la fase 9 (1501-1540) y no "
                         "esta en la banda declarada de este bloque %s." % (malas_s, list(BANDA_HUMO)))
    plan = PLAN_POR_SEM.get(len(sem), PLAN_HUMO_3) if '--plan' not in sys.argv else \
        [tuple(p.split(':')) for p in sys.argv[sys.argv.index('--plan') + 1].split(',') if p.strip()]
    malas = [p for p in plan if p[0] not in CELDAS or p[1] not in BRAZOS_BASE]
    if malas:
        raise SystemExit("--plan: par(es) desconocido(s) %s. Formato celda:brazo." % malas)
    humo(sem, arg('--T', T_HUMO), plan)
