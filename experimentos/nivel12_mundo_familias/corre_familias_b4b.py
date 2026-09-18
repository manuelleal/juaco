"""BLOQUE 4b -- EL EMISOR QUE SI DESCUBRE EN LA DIRECCION CIEGA, y la especificidad entre HERMANAS.
Ejecuta PREREGISTRO_bloque4b_emisor.md (su sha va en el meta del JSON).

ERR-51 (montaje del emisor, bloque 4): el emisor COMPARTE EL PUNTO CIEGO DEL RECEPTOR -- para decir "lo que evitas
es comida" alguien tiene que haberlo mordido, y el emisor lo evita por la misma razon. En el bloque 4 la puerta
P-I2 cayo en la direccion (-): 5/20 y 4/20 emisores sin mensaje. Aqui el emisor lleva `voraz` (una constante de su
propia boca) y P-I2 vuelve a ser puerta CON esa mecanica.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive, se reproduce y se COMUNICA, con evidencia
preregistrada. Hoy: que dos celulas se comuniquen SOBRE ALGO QUE AMBAS REPRESENTAN.

    python experimentos/nivel12_mundo_familias/corre_familias_b4.py --humo     (UN proceso, sin Pool: el disenador)
    python experimentos/nivel12_mundo_familias/corre_familias_b4.py [--desde 541] [--T 100000] [--brazos CANAL-,...]

DOS DIRECCIONES, y la que decide es la SEGUNDA (PROTOCOLO_canal_20260918.md 2.7 y 5.1):
  (+) "eso que comes es VENENO"  -> el receptor lo aprenderia SOLO en una mordida que cuesta -3 y no mata.
  (-) "eso que evitas es COMIDA" -> el receptor NO lo aprende NUNCA solo, porque no lo muerde. Ahi el canal es
      IRREEMPLAZABLE, y por eso el emisor es SIMETRICO (anota su primera mordida de cada estimulo marcado, con la
      R cruda de cualquier signo).

REGLA 3 y 11: el `Pool` lo lanza SOLO el coordinador. `--humo` es UN proceso (<= 6 corridas).
REGLA 10: log desde el arranque; el subconjunto de P-6 esta PREREGISTRADO y se calcula aqui, no en linea.
ERR-31: el mundo y las utilidades son los OBJETOS de los bloques 2 y 3, importados, no recopiados.
ERR-44 / T-E: todo se mide sobre lo que LEE LA BOCA (`primera_b2`, `primera_b4`, `mord`), nunca sobre pesos. La
tabla de pares (`canal_gan_*`, `canal_bin`, `canal_mismo_bin`) es DIAGNOSTICO OBSERVADO: la especificidad NO se
promete, se mide.
"""
import sys, os, json, time, hashlib, platform, subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import numpy as np
import corre_familias_b4 as B4R
B3R = B4R.B3R       # bloque 3: v15f en el mundo de familias
B2R = B4R.B2R                          # bloque 2: el mundo, `resuelve`, la letra
CF = B2R.CF                            # bloque 1: log, medianas, A12, cuenta, diagnostico, cruce de cod0

T = 100000
T_ID = 20000
N_PARALELO = 14
N_SEM = 20
DESDE = 581
VORAZ = 1.0                            # FIJADO en el preregistro 3.2 (calibracion declarada, semillas 1-2)
SEMILLAS_ID = [1, 2, 3]
SEM_R = 100000                         # desplazamiento del rng del RECEPTOR (el mundo lo fija fam_seed)
SEM_OTRO = 200000                      # desplazamiento del MUNDO del receptor en R-SIN-SAL
SHA_V14_ESPERADO = 'feefc88b1fd8d434'
SHA_B4_ESPERADO = 'ff9946ee2ffe27e6'
SHA_ESCALA_ESPERADO = 'd8b8566bca77a0ae'

log, h16, N, med, cuartiles, razon, A12, cuenta = CF.log, CF.h16, CF.N, CF.med, CF.cuartiles, CF.razon, CF.A12, CF.cuenta
BASE = B2R.BASE

# ---------------------------------------------------------------- el mundo: el del bloque 2/3 + exc_fija
# La EXCEPCION de cada token es la variante RETENIDA por la deriva (exc_fija=2) y la tienen los DOS primeros
# tokens (n_exc=2): T0 es familia COMIDA -> X+ = T0v2 es VENENO ; T1 es familia VENENO -> X- = T1v2 es COMIDA.
# Nada cambia nunca (cambio fuera del horizonte, vira=0). Las OTRAS SEIS Tkv2 son el control balanceado.
MUNDO = dict(BASE, cambio=10**9, vira=0, n_exc=2, exc_fija=2, fam_val='familia', memoria_pares='relevo')
KW_E = dict(MUNDO, deriva=5000)                         # el EMISOR: las tres variantes circulan -> las muerde
KW_R = dict(MUNDO, _deriva_tercio=True, reg_b4=1)       # el RECEPTOR: la tercera variante no existe hasta 2T/3
XPOS, XNEG = 'T0v2', 'T1v2'
REF = {'pos': XPOS, 'neg': XNEG}
# BARAJADO: la hermana es otra variante del MISMO token; el otro token es de la MISMA clase de valencia de familia
BAR = {'pos': dict(H='T0v0', TK='T2v2'), 'neg': dict(H='T1v0', TK='T3v2')}

PLANTILLA = [('CANAL', 'sen', 'REF', False), ('CORTADO', 'mudo', 'REF', False),
             ('BAR-H', 'sen', 'H', False), ('BAR-T', 'sen', 'TK', False),
             ('VALOR', 'sen', 'CEROS', False), ('INM', 'inm', 'REF', False),
             ('OTRO', 'sen', 'REF', True)]
PAR_HERM = (1, 0)   # B4b: en la familia del referente ciego (T1) el TOKEN se sustituye por su variante 0
BRAZOS, ORDEN = {}, []
for _d, _sg in (('pos', '+'), ('neg', '-')):
    for _n, _m, _p, _o in PLANTILLA:
        BRAZOS[_n + _sg] = dict(dir=_d, modo=_m, pat=_p, otro=_o, par=None)
        ORDEN.append(_n + _sg)
# ESPECIFICIDAD ENTRE HERMANAS (brazo nuevo del bloque 4b): el receptor ve DOS VARIANTES de la familia tras el
# mensaje (la excepcion T1v2 y su hermana T1v0), en vez de la excepcion y su token. EL CANAL NO CAMBIA.
BRAZOS['PAR-'] = dict(dir='neg', modo='sen', pat='REF', otro=False, par=PAR_HERM)
BRAZOS['PAR0-'] = dict(dir='neg', modo='mudo', pat='REF', otro=False, par=PAR_HERM)
ORDEN += ['PAR-', 'PAR0-']
BRAZOS_ACTIVOS = list(ORDEN)

CASOS_ID = {   # subconjunto critico del arnes de identidad_familias_b4.py (92/92)
    'a': ("(a) b4b apagado == organismo_familias_b3 (mundo=AB)", 'B3', T_ID),
    'g': ("(g) b4b apagado == organismo_familias_b3 (el mundo del bloque 4)", 'B3F', T_ID),
    'n': ("(n) b4b apagado + mundo=AB == organismo_v14 (TRONCO)", 'V14', T_ID),
    'o': ("(o) relevo ON + mundo=AB == organismo_v15f_on", 'V15FON', T_ID),
    'r': ("(r) canal='emite' == canal=None (el emisor SOLO MIRA)", 'EMI', T_ID),
    'w': ("(w) exc_fija no toca el rng del mundo (n_exc=0)", 'EXCF', 200),
    'v': ("(v) voraz=0.0 == el defecto (b4 bit a bit por la cadena)", 'VOR', 6000),
    'p': ("(p) par_herm no toca el rng del mundo", 'PARH', 6000),
    'K': ("(K) CANAL+ != CORTADO+ (DEBE diferir)", 'CAN', 30000),
}

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (seccion 6)
UMBRALES = {
    'PI2': dict(frase="PUERTA -- HAY MENSAJE: el emisor anota el referente de la direccion en >= 18/20, con la R "
                      "CRUDA del signo que le toca, y t_msg < 2*deriva(R) en todas. Las semillas sin mensaje se "
                      "EXCLUYEN de esa direccion y se reportan al lado (regla 10)", n_emite=18),
    'PI3': dict(frase="PUERTA -- GEMELO: cada brazo 'sen' comparte con su CORTADO el prefijo EXACTO de `log` hasta "
                      "la entrega, en >= 18/20 (INM hasta t_msg). Si cae, es el INSTRUMENTO y se para", n_min=18),
    'PI4': dict(frase="PUERTA -- NUNCA VISTO: en CORTADO, la primera exposicion de la VIDA al referente coincide "
                      "con el paso de la entrega, en 20/20", n_min=20),
    'PI5': dict(frase="PUERTA -- VIA POR LA QUE SE LEE: en la prueba, la boca usa la via LENTA (fam1 = 0) en "
                      ">= 18/20. Si el codigo del referente le resulta FAMILIAR por alias, el mensaje queda escrito "
                      "y no consultado, y esa semilla se reporta aparte", n_min=18),
    'P1': dict(frase="(+) LLEGA EL VALOR -- CONTAMINADA en CANAL+ (seccion 5.4: vi evX=1 en las semillas 1 y 2 del "
                     "arnes; lo ciego es CORTADO+ y el pareado): CANAL+ no muerde el veneno nunca visto en >= 15/20 "
                     "Y CORTADO+ <= 5/20; refuta si CANAL+ <= 10/20 o CORTADO+ >= 10/20",
               n_pasa=15, n_cort=5, n_refuta=10),
    'P2': dict(frase="LINEA BASE SIN MENSAJE, en las dos direcciones: CORTADO+ muerde el veneno nunca visto "
                     "(evX <= 5/20) Y CORTADO- NO muerde la comida nunca vista (evX >= 15/20) Y no la muerde en "
                     "TODA la corrida (nunca >= 15/20: ciego para siempre). Refuta si CORTADO- muerde en >= 10/20",
               n_pos=5, n_neg=15, n_nunca=15, n_refuta=10),
    'P3': dict(frase="LA DECISIVA (-) EL CANAL IRREEMPLAZABLE: CANAL- COME a la PRIMERA lo que habria evitado "
                     "(evX <= 5/20) contra CORTADO- (>= 15/20), pareado en >= 14/20. Refuta si CANAL- >= 10/20",
               n_pasa=5, n_cort=15, n_par=14, n_refuta=10),
    'P4': dict(frase="REFERENCIA CONTRA LAS HERMANAS: BAR-H se comporta como CORTADO con el referente (|BAR-H - "
                     "CORTADO| <= 3/20) en las dos direcciones; refuta si |BAR-H - CANAL| <= 3/20 (el mensaje no "
                     "nombra: da igual de quien se hable)", dif_pasa=3, dif_refuta=3),
    'P5': dict(frase="REFERENCIA CONTRA OTRO TOKEN: BAR-T como CORTADO (|BAR-T - CORTADO| <= 3/20); refuta si "
                     "|BAR-T - CANAL| <= 3/20", dif_pasa=3, dif_refuta=3),
    'P6': dict(frase="HACE FALTA EL CAMPO DE REFERENCIA: VALOR como CORTADO (|VALOR - CORTADO| <= 3/20); refuta si "
                     "|VALOR - CANAL| <= 3/20. SUBCONJUNTO PREREGISTRADO (regla 10): en las semillas donde la "
                     "casilla de los ceros NO es la del referente, VALOR debe ser CORTADO; se reporta con los "
                     "umbrales ORIGINALES y junto al completo", dif_pasa=3, dif_refuta=3),
    'P7': dict(frase="SENALAMIENTO CONTRA ENTREGA INMEDIATA: INM como CORTADO (|INM - CORTADO| <= 5/20) -- entre "
                     "t_msg y la prueba median ~30 000 pasos y cientos de mordidas que sobrescriben la casilla; "
                     "refuta si |INM - CANAL| <= 3/20 (el mensaje dura)", dif_pasa=5, dif_refuta=3),
    'P8': dict(frase="HACE FALTA COMPARTIR EL MUNDO, y el COLATERAL del relevo (R-SIN-SAL): OTRO como CORTADO con "
                     "el referente (|OTRO - CORTADO| <= 3/20) Y sin dano colateral -- okU y muertes de OTRO no "
                     "peores que CORTADO en >= 15/20. Refuta si |OTRO - CANAL| <= 3/20 -> el efecto no es "
                     "senalamiento, es un susto aversivo", dif_pasa=3, dif_refuta=3, n_col=15),
    'P9': dict(frase="CUANTO DURA: ret3 (la 3.a exposicion tras la entrega sigue movida por el mensaje) <= 8/20 en "
                     "CANAL; refuta si >= 15/20", n_pasa=8, n_refuta=15),
    'P10': dict(frase="SIRVE PARA VIVIR: muertes(CANAL) < muertes(CORTADO) pareado en >= 14/20; refuta si >= en "
                      ">= 14/20 -> el canal CUESTA", n_pasa=14, n_refuta=14),
    'P11': dict(frase="ESPECIFICIDAD ENTRE HERMANAS (brazo PAR; el canal NO cambia): el receptor ve la "
                      "excepcion T1v2 Y su hermana T1v0 tras el mensaje, en vez de la excepcion y su token. "
                      "`dist` = la boca las trata DISTINTO en su primera exposicion. PREDICCION ESCRITA ANTES: "
                      "con UNA sola celda ganadora de 2 bits NO las distingue -> dist <= 8/20. Refuta si dist "
                      ">= 15/20 (entonces la referencia SI llega al nivel de la variante y la lectura del bloque "
                      "4 cambia). DECLARADA CONTAMINADA en n = 2 (seccion 5.4). Covariable obligatoria: "
                      "`lag_par` (mordidas entre la entrega y la exposicion a la hermana): si es alta, el "
                      "mensaje ya se habia borrado y `dist` no mide especificidad sino olvido",
                n_pasa=8, n_refuta=15),
    'PC': dict(frase="PREDICCION DEL COORDINADOR: el canal lleva VALOR Y REFERENCIA en las dos direcciones -- "
                     "CANAL >= 15/20 contra CORTADO <= 5/20 (y en (-) al reves), BARAJADO <= 5/20 de efecto, "
                     "hermanas intactas comH >= 0.9, VALOR-SOLO sin efecto",
               n_canal=15, n_cort=5, n_bar=5, comH=0.9),
    'PD': dict(frase="PREDICCION DEL DISENADOR (al lado, y distinta): llega el VALOR y NO la REFERENCIA -- evU "
                     "mediana >= 0.6 en la direccion (+) (el receptor deja de morder tambien las otras variantes "
                     "nunca vistas de su clase), comH <= 0.6, y BAR-H y BAR-T indistinguibles de CANAL "
                     "(|CANAL - BAR| <= 4/20). Me refuta que BAR-H y BAR-T se comporten como CORTADO, o comH >= 0.9",
               evU_min=0.6, comH_max=0.6, dif_max=4),
    'PM': dict(frase="MECANISMO -- DIAGNOSTICO OBSERVADO, NO PROMETIDO (PROTOCOLO 5.2): celda ganadora antes y "
                     "despues del mensaje, si usa algun pixel VARIABLE (>= 9: la unica forma de que la tabla "
                     "distinga una variante de sus hermanas), casilla del referente y cuantos de los 32 estimulos "
                     "caen en ella. El techo es 2 bits: un mensaje no puede ser mas especifico que esa casilla"),
}


# ---------------------------------------------------------------- el catalogo (el MISMO objeto del bloque 0)
def PATS(fam_seed, D=12, F=8, V=3):
    import escala_codigo as EC
    P, fm, ev, rz, _ = EC.catalogo(D, F, V, fam_seed)
    out = {}
    for i in range(P.shape[0]):
        k = int(fm[i])
        out[('T%d' % k) if not bool(ev[i]) else ('T%dv%d' % (k, i - int(rz[i]) - 1))] = [float(x) for x in P[i]]
    return out


def canal_de(brazo, msg, fam_seed_R, D=12):
    """El `canal` de cada brazo. Lo UNICO que cambia entre brazos de la misma direccion."""
    b = BRAZOS[brazo]
    if b['pat'] == 'CEROS':
        P = [0.0] * D
    elif b['pat'] == 'REF':
        P = msg['P']                      # el patron del referente TAL COMO LO VIO EL EMISOR
    else:
        P = PATS(msg['fam_seed'])[BAR[b['dir']][b['pat']]]
    return dict(modo=b['modo'], t=msg['t'], ref=msg['ref'], P=P, R=msg['R'])


# ---------------------------------------------------------------- lectura de una corrida (SOLO conducta de la boca)
def prefijo(r, hasta):
    return hashlib.sha256(json.dumps([f for f in r['log'] if f[0] < hasta]).encode()).hexdigest()[:16]


def lee_b4(r, ref):
    """Conducta de la boca en la PRIMERA exposicion de la VIDA a cada variante retenida (`primera_b2`) y en las
    tres primeras tras la entrega (`primera_b4`). `mordio` es el campo 4 en las dos.
    `evX` = 1 si la boca NO mordio.  `okX` = 1 si lo que hizo la boca ACIERTA con la valencia real del estimulo
    (no morder el veneno / morder la comida): asi las dos direcciones se leen con el mismo numero."""
    F, V = r['fam']['F'], r['fam']['V']
    ret = ['T%dv%d' % (k, V - 1) for k in range(F)]
    pb, p4, val = r['primera_b2'], (r['primera_b4'] or {}), r['val_mundo']
    ev, ok = {}, {}
    for n in ret:
        e = pb.get(n)
        if e is None:
            continue
        ev[n] = 0.0 if e[4] else 1.0
        ok[n] = 1.0 if ((e[4] and val[n] == 'comida') or ((not e[4]) and val[n] == 'veneno')) else 0.0
    evX, okX = ev.get(ref), ok.get(ref)
    otras = [n for n in ev if n not in (XPOS, XNEG)]   # las 6 de control: NINGUNA de las dos excepciones
    herm = r['herm'].get(ref, [])
    eh = [(0.0 if p4[h][0][4] else 1.0) for h in herm if p4.get(h)]
    oh = [(1.0 if ((p4[h][0][4] and val[h] == 'comida') or ((not p4[h][0][4]) and val[h] == 'veneno')) else 0.0)
          for h in herm if p4.get(h)]
    lX, e0 = (p4.get(ref) or []), pb.get(ref)
    pf = r.get('par_fijo')            # B4b: la hermana sustituida (brazo PAR); None en los demas brazos
    lp = (p4.get(pf) or []) if pf else []
    dist = okP = lagP = None
    if lX and lp:                      # 1.a exposicion de CADA UNA tras la entrega: la boca, nunca los pesos
        dist = 1.0 if (bool(lX[0][4]) != bool(lp[0][4])) else 0.0
        okP = 1.0 if ((lp[0][4] and val[pf] == 'comida') or ((not lp[0][4]) and val[pf] == 'veneno')) else 0.0
        lagP = lp[0][8]
    sg = 1.0 if (r['canal'] or {}).get('R', -1) < 0 else -1.0      # +1 si el mensaje dice "peligro"
    f = lambda xs: (round(float(np.mean(xs)), 4) if xs else None)
    return dict(ref=ref, val_ref=val.get(ref), signo=sg, evX=evX, okX=okX,
                evU=f([ev[n] for n in otras]), okU=f([ok[n] for n in otras]), n_U=len(otras),
                evH=f(eh), comH=(None if not eh else round(1.0 - float(np.mean(eh)), 4)), okH=f(oh), n_H=len(eh),
                esp=(None if (evX is None or not otras) else
                     round(sg * (evX - float(np.mean([ev[n] for n in otras]))), 4)),
                ret2=(None if len(lX) < 2 else (0.0 if lX[1][4] else 1.0)),
                ret3=(None if len(lX) < 3 else (0.0 if lX[2][4] else 1.0)),
                mord_ref=int(sum(r['mord'].get(ref, [0]))), nunca=(1.0 if sum(r['mord'].get(ref, [0])) == 0 else 0.0),
                t_X=(None if e0 is None else e0[0]), wt_X=(None if e0 is None else e0[1]),
                fam1=(None if e0 is None else e0[3]),
                lag_t=(None if (e0 is None or r['canal_t_entrega'] is None) else e0[0] - r['canal_t_entrega']),
                lag_m=(None if not lX else lX[0][8]), vistas=len(ev), n_ret=len(ret),
                par_fijo=pf, dist=dist, okP=okP, lag_par=lagP)


def mecanismo(r, D=12, n_var=3):
    gp, gq = r.get('canal_gan_pre'), r.get('canal_gan_post')
    var = lambda g: (None if not g else bool(max(g) >= D - n_var))
    return dict(gan_pre=gp, gan_post=gq, gan_var_pre=var(gp), gan_var_post=var(gq),
                cambio_gan=(None if (gp is None or gq is None) else bool(gp != gq)),
                bin_ref=r.get('canal_bin'), mismo_bin=r.get('canal_mismo_bin'),
                n_mismo_bin=(None if r.get('canal_mismo_bin') is None else len(r['canal_mismo_bin'])),
                cobertura=r.get('mem_cobertura'), vistas=r.get('mem_vistas'))


def resumen(brazo, seed, r, msg):
    d = dict(tipo='R', brazo=brazo, dir=BRAZOS[brazo]['dir'], seed=seed, mundo=r['mundo'], deaths=r['deaths'],
             celdas=r['celdas'], splits=r['splits'], fam_seed=r['fam_seed'], exc=r['exc'], cod0=r['cod0'],
             entregado=r['canal_entregado'], t_entrega=r['canal_t_entrega'], t_msg=r['canal_t_msg'],
             frac_regalo=r['frac_regalo'], renovados=r['renovados'])
    d['B4'] = lee_b4(r, msg['ref'])
    d['mem'] = mecanismo(r)
    d['prefijo'] = prefijo(r, r['canal_t_entrega'] if r['canal_t_entrega'] is not None else r['canal_t_msg'])
    d['prefijo_msg'] = prefijo(r, r['canal_t_msg'])
    d['bin0_igual'] = (None if r.get('canal_mismo_bin') is None else bool(msg['ref'] in r['canal_mismo_bin']))
    return d


# ---------------------------------------------------------------- tareas
NUEVAS_B4 = ('canal', 'canal_modo', 'canal_t_msg', 'canal_entregado', 'canal_t_entrega', 'canal_emitido',
             'canal_gan_pre', 'canal_gan_post', 'canal_bin', 'canal_mismo_bin', 'primera_b4', 'fam_seed')


def emisor(seed, Ti, nk=30, ktop=3, nkmax=90):
    """Corre E y devuelve SUS MENSAJES, uno por direccion: (paso, referente, patron, R CRUDA)."""
    import organismo_familias_b4b as B4
    kw = B2R.resuelve(KW_E, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    r = B4.run(seed, T=Ti, fam_seed=seed, canal={'modo': 'emite'}, voraz=VORAZ, **kw)
    em = r['canal_emitido'] or {}
    out = {}
    for d, ref in REF.items():
        e = em.get(ref)
        out[d] = (None if e is None else dict(t=int(e[0]), ref=e[1], P=[float(x) for x in e[2]], R=float(e[3]),
                                              enc=int(e[4]), fam_seed=seed, muertes=r['deaths'],
                                              exc=list(r['exc']), voraz=float(r['voraz']),
                                              veneno=int(sum(sum(c) for k2, c in r['mord'].items()
                                                             if r['val_mundo'][k2] == 'veneno'))))
    out = {'pos': out['pos'], 'neg': out['neg']}
    out['cod0'] = dict(r['cod0']); out['seed'] = seed; out['deaths'] = r['deaths']; out['voraz'] = float(r['voraz'])
    return out


def tarea(args):
    tipo = args[0]
    if tipo == 'ID':
        _, cual, seed, Ti = args
        import organismo_v14 as V14, organismo_v15f_on as V15FON
        import organismo_familias_b3 as B3, organismo_familias_b4 as B4ORIG
        import organismo_familias_b4b as B4
        etiq, ref, Tc = CASOS_ID[cual]
        Tc = Tc or Ti
        salta, debe = tuple(NUEVAS_B4) + ('voraz', 'par_herm', 'par_fijo'), False
        if ref == 'B3':
            a, b = B3.run(seed, T=Tc), B4.run(seed, T=Tc)
        elif ref == 'B3F':
            k = dict(B2R.resuelve(KW_R, Tc)); k.pop('exc_fija'); k.pop('reg_b4')
            a, b = B3.run(seed, T=Tc, **k), B4.run(seed, T=Tc, **k)
        elif ref == 'V14':
            a, b = V14.run(seed, T=Tc), B4.run(seed, T=Tc)
        elif ref == 'V15FON':
            a, b = V15FON.run(seed, T=Tc), B4.run(seed, T=Tc, memoria_pares='relevo')
        elif ref == 'EMI':
            k = B2R.resuelve(KW_E, Tc)
            a = B4.run(seed, T=Tc, fam_seed=seed, **k)
            b = B4.run(seed, T=Tc, fam_seed=seed, canal={'modo': 'emite'}, **k)
            salta = ('canal', 'canal_modo', 'canal_emitido')
        elif ref == 'VOR':
            k = B2R.resuelve(KW_E, Tc)
            a = B4ORIG.run(seed, T=Tc, fam_seed=seed, **k)
            b = B4.run(seed, T=Tc, fam_seed=seed, voraz=0.0, **k)
        elif ref == 'PARH':
            k = B2R.resuelve(KW_R, Tc)
            a0 = B4.run(seed, T=Tc, fam_seed=seed, **k)
            b0 = B4.run(seed, T=Tc, fam_seed=seed, par_herm=PAR_HERM, **k)
            cl = ('val_mundo', 'exc_win', 'herm', 'exc', 'cod0')
            a = {kk: a0[kk] for kk in cl}; b = {kk: b0[kk] for kk in cl}
            salta = ()
        elif ref == 'EXCF':
            k = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=0, n_neu=0, fam_val='azar', deriva=1000)
            a = B4.run(seed, T=Tc, exc_fija=None, **k); b = B4.run(seed, T=Tc, exc_fija=2, **k)
            salta = tuple(NUEVAS_B4) + ('exc_win', 'herm', 't_exc', 'colateral', 'omision', 'colateral_tot')
        else:                                   # CAN: CANAL- contra su gemelo mudo (DEBE diferir)
            m = emisor(seed, Tc)['pos']
            if m is None:
                return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=False, debe_diferir=True,
                            ok=False, difieren=['sin mensaje (+)'], faltan=[])
            k = B2R.resuelve(KW_R, Tc)
            a = B4.run(seed + SEM_R, T=Tc, fam_seed=seed, canal=canal_de('CORTADO+', m, seed), **k)
            b = B4.run(seed + SEM_R, T=Tc, fam_seed=seed, canal=canal_de('CANAL+', m, seed), **k)
            debe = True; salta = ('canal', 'canal_modo')
        dif = [k2 for k2 in a if k2 not in salta and N(a[k2]) != N(b.get(k2))]
        falta = [k2 for k2 in a if k2 not in b and k2 not in salta]
        igual = not dif and not falta
        return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=igual, debe_diferir=debe,
                    ok=bool(igual != debe), difieren=dif[:6], faltan=falta)
    if tipo == 'D':
        _, seed, nk, ktop = args
        d = CF.diagnostico(seed, nk, ktop, BASE)
        d.pop('cod')
        return dict(tipo='D', **d)
    if tipo == 'E':
        _, seed, Ti, nk, ktop, nkmax = args
        return dict(tipo='E', seed=seed, msgs=emisor(seed, Ti, nk, ktop, nkmax))
    _, brazo, seed, msg, Ti, nk, ktop, nkmax = args
    import organismo_familias_b4b as B4
    kw = B2R.resuelve(KW_R, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    fsr = seed + SEM_OTRO if BRAZOS[brazo]['otro'] else seed
    r = B4.run(seed + SEM_R, T=Ti, fam_seed=fsr, canal=canal_de(brazo, msg, fsr),
               par_herm=BRAZOS[brazo]['par'], **kw)
    return resumen(brazo, seed, r, msg)


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_bloque4b_emisor.md')),
    script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_familias_b4b.py')),
    instrumento=h16(os.path.join(AQUI, 'organismo_familias_b4b.py')),
    arnes=h16(os.path.join(AQUI, 'identidad_familias_b4b.py')),
    origen_b4=h16(os.path.join(AQUI, 'organismo_familias_b4.py')),
    runner_bloque4=h16(os.path.join(AQUI, 'corre_familias_b4.py')),
    preregistro_bloque4=h16(os.path.join(AQUI, 'PREREGISTRO_bloque4_canal.md')),
    escala_codigo_bloque0=h16(os.path.join(AQUI, 'escala_codigo.py')),
    protocolo_sala3=h16(os.path.join(RAIZ, 'registro', 'investigacion', 'sala3_celulas',
                                     'PROTOCOLO_canal_20260918.md')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))


def guarda_origen():
    s, ok = SHAS(), True
    for k, esp in [('origen_organismo_v14', SHA_V14_ESPERADO), ('origen_b4', SHA_B4_ESPERADO),
                   ('escala_codigo_bloque0', SHA_ESCALA_ESPERADO)]:
        if s[k] != esp:
            log(f"*** ORIGEN CAMBIADO: {k} es {s[k]}, se esperaba {esp}. Reconstruir por anclas y repetir el arnes.")
            ok = False
    return ok


# ---------------------------------------------------------------- veredicto (la letra de la seccion 6)
def veredicto(res, msgs, SEEDS, diags):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    val = {d: [s for s in SEEDS if (msgs.get(s) or {}).get(d)] for d in REF}
    bb = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('B4') or {}).get(c)
                       for s in val[BRAZOS[b]['dir']] if s in G.get(b, {})}
    mm = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('mem') or {}).get(c)
                       for s in val[BRAZOS[b]['dir']] if s in G.get(b, {})}
    gg = lambda b, c: {s: G.get(b, {}).get(s, {}).get(c) for s in val[BRAZOS[b]['dir']] if s in G.get(b, {})}
    n1 = lambda d: sum(1 for v in d.values() if v == 1.0)
    V = {'umbrales': UMBRALES, 'n_validas': {d: len(v) for d, v in val.items()},
         'excluidas': {d: [s for s in SEEDS if s not in val[d]] for d in REF}}
    V['alias'] = dict(pares_mediana=med([d['alias_pares'] for d in diags]),
                      semillas_con_alias=sum(d['alias_semilla'] for d in diags), n=len(diags),
                      U3_mediana=med([d['U3'] for d in diags]))

    # --- puertas
    derR = B2R.resuelve(KW_R, T)['deriva']
    u = UMBRALES['PI2']
    V['PI2'] = {d: dict(n_emite=len(val[d]), n=len(SEEDS), deriva_R=derR,
                        signo_ok=sum(1 for s in val[d] if (msgs[s][d]['R'] < 0) == (d == 'pos')),
                        n_antes=sum(1 for s in val[d] if msgs[s][d]['t'] < 2 * derR),
                        t_msg_med=med([msgs[s][d]['t'] for s in val[d]]),
                        enc_med=med([msgs[s][d]['enc'] for s in val[d]])) for d in REF}
    for d in REF:
        V['PI2'][d]['pasa'] = bool(V['PI2'][d]['n_emite'] >= min(u['n_emite'], len(SEEDS))
                                   and V['PI2'][d]['signo_ok'] == len(val[d])
                                   and V['PI2'][d]['n_antes'] == len(val[d]))
    V['PI2']['pasa'] = bool(all(V['PI2'][d]['pasa'] for d in REF))
    u = UMBRALES['PI3']
    V['PI3'] = {}
    for b in BRAZOS_ACTIVOS:
        sg = b[-1]; d = BRAZOS[b]['dir']; cor = 'PAR0-' if b.startswith('PAR') else 'CORTADO' + sg
        if b == cor or b.startswith('OTRO'):   # ERR-52: OTRO (R-SIN-SAL) vive en otro mundo; su gemelo no es CORTADO y el prefijo difiere por construccion
            continue
        k = 'prefijo_msg' if b.startswith('INM') else 'prefijo'
        pc = gg(cor, k)
        V['PI3'][b] = sum(1 for s in val[d] if gg(b, k).get(s) is not None and gg(b, k).get(s) == pc.get(s))
    V['PI3']['pasa'] = bool(all(v >= min(u['n_min'], max(len(val['pos']), len(val['neg'])))
                                for kk, v in V['PI3'].items() if kk != 'pasa'))
    u = UMBRALES['PI4']
    V['PI4'] = {d: dict(n=sum(1 for s in val[d] if bb('CORTADO' + sg, 't_X').get(s) is not None
                              and bb('CORTADO' + sg, 't_X').get(s) == gg('CORTADO' + sg, 't_entrega').get(s)),
                        n_val=len(val[d]))
                for d, sg in (('pos', '+'), ('neg', '-'))}
    V['PI4']['pasa'] = bool(all(V['PI4'][d]['n'] >= min(u['n_min'], len(val[d])) for d in REF))
    u = UMBRALES['PI5']
    V['PI5'] = {d: dict(lenta=sum(1 for v in bb('CORTADO' + sg, 'fam1').values() if v == 0),
                        n=len(val[d])) for d, sg in (('pos', '+'), ('neg', '-'))}
    V['PI5']['pasa'] = bool(all(V['PI5'][d]['lenta'] >= min(u['n_min'], len(val[d])) for d in REF))

    # --- por brazo
    V['brazos'] = {}
    for b in BRAZOS_ACTIVOS:
        eX = bb(b, 'evX')
        V['brazos'][b] = dict(
            n=len([v for v in eX.values() if v is not None]), evX_n=n1(eX), okX_n=n1(bb(b, 'okX')),
            evU_med=med([v for v in bb(b, 'evU').values() if v is not None]),
            okU_med=med([v for v in bb(b, 'okU').values() if v is not None]),
            comH_med=med([v for v in bb(b, 'comH').values() if v is not None]),
            okH_med=med([v for v in bb(b, 'okH').values() if v is not None]),
            esp_med=med([v for v in bb(b, 'esp').values() if v is not None]),
            ret2_n=n1(bb(b, 'ret2')), ret3_n=n1(bb(b, 'ret3')), nunca_n=n1(bb(b, 'nunca')),
            mord_ref_med=med([v for v in bb(b, 'mord_ref').values() if v is not None]),
            lag_t_med=med([v for v in bb(b, 'lag_t').values() if v is not None]),
            lag_m_med=med([v for v in bb(b, 'lag_m').values() if v is not None]),
            fam1_n=sum(1 for v in bb(b, 'fam1').values() if v == 1),
            dist_n=n1(bb(b, 'dist')), okP_n=n1(bb(b, 'okP')),
            n_dist=len([v for v in bb(b, 'dist').values() if v is not None]),
            lag_par_med=med([v for v in bb(b, 'lag_par').values() if v is not None]),
            muertes_med=med([v for v in gg(b, 'deaths').values() if v is not None]),
            celdas_med=med([v for v in gg(b, 'celdas').values() if v is not None]),
            gan_var_pre=sum(1 for v in mm(b, 'gan_var_pre').values() if v),
            gan_var_post=sum(1 for v in mm(b, 'gan_var_post').values() if v),
            cambio_gan=sum(1 for v in mm(b, 'cambio_gan').values() if v),
            n_mismo_bin_med=med([v for v in mm(b, 'n_mismo_bin').values() if v is not None]))
    Bz = V['brazos']
    ev = lambda b: Bz[b]['evX_n']

    # --- P1, P2, P3
    u = UMBRALES['P1']; n = len(val['pos'])
    V['P1'] = dict(canal=ev('CANAL+'), cortado=ev('CORTADO+'), n=n, contaminada_en='CANAL+',
                   pasa=bool(ev('CANAL+') >= min(u['n_pasa'], n) and ev('CORTADO+') <= u['n_cort']),
                   refuta=bool(ev('CANAL+') <= u['n_refuta'] or ev('CORTADO+') >= u['n_refuta']))
    u = UMBRALES['P2']
    V['P2'] = dict(cortado_pos=ev('CORTADO+'), cortado_neg=ev('CORTADO-'), nunca_neg=Bz['CORTADO-']['nunca_n'],
                   mord_ref_neg=Bz['CORTADO-']['mord_ref_med'], n_pos=len(val['pos']), n_neg=len(val['neg']))
    V['P2']['pasa'] = bool(ev('CORTADO+') <= u['n_pos'] and ev('CORTADO-') >= min(u['n_neg'], len(val['neg']))
                           and Bz['CORTADO-']['nunca_n'] >= min(u['n_nunca'], len(val['neg'])))
    V['P2']['refuta'] = bool(ev('CORTADO-') <= (len(val['neg']) - u['n_refuta']))
    u = UMBRALES['P3']; n = len(val['neg'])
    dk, dc = bb('CANAL-', 'evX'), bb('CORTADO-', 'evX')
    par = sum(1 for s in val['neg'] if dk.get(s) is not None and dc.get(s) is not None and dk[s] < dc[s])
    V['P3'] = dict(canal=ev('CANAL-'), cortado=ev('CORTADO-'), n_menor=par, n=n,
                   A12=A12(list(dk.values()), list(dc.values())),
                   pasa=bool(ev('CANAL-') <= u['n_pasa'] and ev('CORTADO-') >= min(u['n_cort'], n)
                             and par >= min(u['n_par'], n)),
                   refuta=bool(ev('CANAL-') >= u['n_refuta']))

    # --- P4..P8: cada control contra SU cortado y contra SU canal, en las dos direcciones
    for k, nom in (('P4', 'BAR-H'), ('P5', 'BAR-T'), ('P6', 'VALOR'), ('P7', 'INM'), ('P8', 'OTRO')):
        u = UMBRALES[k]; V[k] = {}
        for d, sg in (('pos', '+'), ('neg', '-')):
            b, c, a = nom + sg, 'CORTADO' + sg, 'CANAL' + sg
            V[k][d] = dict(brazo=b, evX=ev(b), cortado=ev(c), canal=ev(a), n=len(val[d]),
                           dif_cortado=abs(ev(b) - ev(c)), dif_canal=abs(ev(b) - ev(a)))
            V[k][d]['pasa'] = bool(V[k][d]['dif_cortado'] <= u['dif_pasa'])
            V[k][d]['refuta'] = bool(V[k][d]['dif_canal'] <= u['dif_refuta'])
        if k == 'P6':   # subconjunto PREREGISTRADO: semillas donde la casilla de los ceros NO es la del referente
            for d, sg in (('pos', '+'), ('neg', '-')):
                sub = [s for s in val[d] if G.get('VALOR' + sg, {}).get(s, {}).get('bin0_igual') is False]
                V[k][d]['subconjunto'] = dict(criterio="bin(ceros) != bin(referente)", n=len(sub), semillas=sub,
                                              evX=sum(1 for s in sub if bb('VALOR' + sg, 'evX').get(s) == 1.0),
                                              cortado=sum(1 for s in sub
                                                          if bb('CORTADO' + sg, 'evX').get(s) == 1.0))
        if k == 'P8':   # colateral del relevo: okU y muertes de OTRO contra CORTADO, pareado
            for d, sg in (('pos', '+'), ('neg', '-')):
                uo, uc = bb('OTRO' + sg, 'okU'), bb('CORTADO' + sg, 'okU')
                mo, mc = gg('OTRO' + sg, 'deaths'), gg('CORTADO' + sg, 'deaths')
                V[k][d]['colateral'] = dict(
                    okU_no_peor=sum(1 for s in val[d] if uo.get(s) is not None and uc.get(s) is not None
                                    and uo[s] >= uc[s]),
                    muertes_no_peor=sum(1 for s in val[d] if mo.get(s) is not None and mc.get(s) is not None
                                        and mo[s] <= mc[s]),
                    okU_OTRO=med([v for v in uo.values() if v is not None]),
                    okU_CORTADO=med([v for v in uc.values() if v is not None]), n=len(val[d]))
                V[k][d]['colateral']['pasa'] = bool(
                    V[k][d]['colateral']['okU_no_peor'] >= min(u['n_col'], len(val[d]))
                    and V[k][d]['colateral']['muertes_no_peor'] >= min(u['n_col'], len(val[d])))
    u = UMBRALES['P9']
    V['P9'] = {d: dict(ret2=Bz['CANAL' + sg]['ret2_n'], ret3=Bz['CANAL' + sg]['ret3_n'], n=len(val[d]),
                       lag_m=Bz['CANAL' + sg]['lag_m_med'],
                       pasa=bool(Bz['CANAL' + sg]['ret3_n'] <= u['n_pasa']),
                       refuta=bool(Bz['CANAL' + sg]['ret3_n'] >= min(u['n_refuta'], len(val[d]))))
               for d, sg in (('pos', '+'), ('neg', '-'))}
    u = UMBRALES['P10']
    V['P10'] = {}
    for d, sg in (('pos', '+'), ('neg', '-')):
        dk2, dc2 = gg('CANAL' + sg, 'deaths'), gg('CORTADO' + sg, 'deaths')
        men = sum(1 for s in val[d] if dk2.get(s) is not None and dc2.get(s) is not None and dk2[s] < dc2[s])
        may = sum(1 for s in val[d] if dk2.get(s) is not None and dc2.get(s) is not None and dk2[s] >= dc2[s])
        V['P10'][d] = dict(muertes_CANAL=Bz['CANAL' + sg]['muertes_med'],
                           muertes_CORTADO=Bz['CORTADO' + sg]['muertes_med'], n_menor=men, n_mayor_igual=may,
                           n=len(val[d]), A12=A12(list(dk2.values()), list(dc2.values())),
                           pasa=bool(men >= min(u['n_pasa'], len(val[d]))),
                           refuta=bool(may >= min(u['n_refuta'], len(val[d]))))

    # --- P11: el brazo PAR (especificidad entre hermanas)
    u = UMBRALES['P11']
    if 'PAR-' in V['brazos'] and 'PAR0-' in V['brazos']:
        d0 = V['brazos']['PAR0-']
        V['P11'] = dict(dist=Bz['PAR-']['dist_n'], n=Bz['PAR-']['n_dist'], dist_gemelo=d0['dist_n'],
                        n_gemelo=d0['n_dist'], okP=Bz['PAR-']['okP_n'], okP_gemelo=d0['okP_n'],
                        evX=ev('PAR-'), evX_gemelo=ev('PAR0-'), lag_par=Bz['PAR-']['lag_par_med'],
                        contaminada=True)
        V['P11']['pasa'] = bool(Bz['PAR-']['dist_n'] <= u['n_pasa'])
        V['P11']['refuta'] = bool(Bz['PAR-']['dist_n'] >= min(u['n_refuta'], max(Bz['PAR-']['n_dist'], 1)))

    # --- PC contra PD
    uc, ud = UMBRALES['PC'], UMBRALES['PD']
    V['PC'] = dict(canal_pos=ev('CANAL+'), cortado_pos=ev('CORTADO+'), canal_neg=ev('CANAL-'),
                   cortado_neg=ev('CORTADO-'), barH_pos=ev('BAR-H+'), barT_pos=ev('BAR-T+'),
                   barH_neg=ev('BAR-H-'), barT_neg=ev('BAR-T-'), comH=Bz['CANAL+']['comH_med'])
    V['PC']['pasa'] = bool(V['P1']['pasa'] and V['P3']['pasa']
                           and all(V[k][d]['pasa'] for k in ('P4', 'P5', 'P6') for d in REF)
                           and Bz['CANAL+']['comH_med'] is not None and Bz['CANAL+']['comH_med'] >= uc['comH'])
    V['PD'] = dict(evU=Bz['CANAL+']['evU_med'], comH=Bz['CANAL+']['comH_med'], esp=Bz['CANAL+']['esp_med'],
                   dif=max(abs(ev('CANAL+') - ev('BAR-H+')), abs(ev('CANAL+') - ev('BAR-T+'))))
    V['PD']['pasa'] = bool(V['PD']['evU'] is not None and V['PD']['evU'] >= ud['evU_min']
                           and V['PD']['comH'] is not None and V['PD']['comH'] <= ud['comH_max']
                           and V['PD']['dif'] <= ud['dif_max'])
    V['PD']['refuta'] = bool((V['P4']['pos']['pasa'] and V['P5']['pos']['pasa'])
                             or (V['PD']['comH'] is not None and V['PD']['comH'] >= uc['comH']))
    V['zona'] = bool(not V['PC']['pasa'] and not V['PD']['pasa'] and not V['PD']['refuta'])
    return V


def frase_final(V):
    p = lambda k: ('pasa' if V.get(k, {}).get('pasa') else ('REFUTA' if V.get(k, {}).get('refuta') else 'indeciso'))
    pd = lambda k, d: ('pasa' if V[k][d]['pasa'] else ('REFUTA' if V[k][d]['refuta'] else 'indeciso'))
    for g in ('PI2', 'PI3', 'PI4', 'PI5'):
        if not V[g].get('pasa'):
            return f"{g} CAE -- es el INSTRUMENTO o el montaje. Nada se declara (preregistro 5.2)."
    B, np_, nn = V['brazos'], V['n_validas']['pos'], V['n_validas']['neg']
    s = (f"(+) AVISO DE VENENO: CANAL+ evita el veneno nunca visto en {B['CANAL+']['evX_n']}/{np_} contra CORTADO+ "
         f"{B['CORTADO+']['evX_n']}/{np_} -> P1 {p('P1')} (CANAL+ contaminada, 5.4). ")
    s += (f"(-) LA DECISIVA -- EL CANAL IRREEMPLAZABLE: CANAL- COME a la primera lo que habria evitado en "
          f"{nn - B['CANAL-']['evX_n']}/{nn} contra CORTADO- {nn - B['CORTADO-']['evX_n']}/{nn} (y CORTADO- no la "
          f"muerde en TODA la corrida en {B['CORTADO-']['nunca_n']}/{nn}) -> P3 {p('P3')}; linea base P2 {p('P2')}. ")
    s += (f"REFERENCIA (observada, no prometida): BAR-H {pd('P4','pos')}/{pd('P4','neg')}, BAR-T "
          f"{pd('P5','pos')}/{pd('P5','neg')}, VALOR-SOLO {pd('P6','pos')}/{pd('P6','neg')}; esp(+) "
          f"{B['CANAL+']['esp_med']} (evU {B['CANAL+']['evU_med']}), hermanas comH {B['CANAL+']['comH_med']}; "
          f"comparten la casilla del referente {B['CANAL+']['n_mismo_bin_med']} de 32 estimulos. ")
    s += (f"MONTAJE: senalamiento contra inmediata {pd('P7','pos')}/{pd('P7','neg')}; mundo compartido "
          f"{pd('P8','pos')}/{pd('P8','neg')}; via lenta en la prueba {V['PI5']['pos']['lenta']}/{np_} y "
          f"{V['PI5']['neg']['lenta']}/{nn}; dura ret3 {B['CANAL+']['ret3_n']}/{np_} -> P9 "
          f"{pd('P9','pos')}; muertes {B['CANAL-']['muertes_med']} contra {B['CORTADO-']['muertes_med']} -> P10 "
          f"{pd('P10','neg')}. ")
    if 'P11' in V:
        s += (f"HERMANAS (brazo PAR, declarado contaminado): la boca trata DISTINTO a la excepcion y a su hermana "
              f"en {V['P11']['dist']}/{V['P11']['n']} (gemelo {V['P11']['dist_gemelo']}/{V['P11']['n_gemelo']}), "
              f"con {V['P11']['lag_par']} mordidas de por medio -> P11 {p('P11')}. ")
    s += ("VEREDICTO: " + ("se cumple la prediccion del COORDINADOR (el mensaje lleva valor Y referencia)."
                           if V['PC']['pasa'] else
                           ("se cumple la prediccion del DISENADOR (llega el valor, no la referencia)."
                            if V['PD']['pasa'] else
                            ("la prediccion del DISENADOR queda REFUTADA y la del coordinador no se cumple entera."
                             if V['PD']['refuta'] else "ZONA DECLARADA: no gana ninguna de las dos."))))
    s += (f" Alias por par {V['alias']['pares_mediana']} ({V['alias']['semillas_con_alias']}/{V['alias']['n']} "
          f"semillas), covariable declarada. 20 semillas no cierran nada: replica en el rango siguiente (regla 12).")
    return s


# ---------------------------------------------------------------- humo (UN proceso, sin Pool, regla 3)
def humo(nk, ktop, nkmax, Tb, brazos):
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_b4b_humo_{stamp}.log'), 'w',
                        encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log(f"HUMO del disenador del bloque 4b, UN proceso, sin Pool (regla 3, <= 6 corridas). voraz = {VORAZ}.")
    log("PREREGISTRO_bloque4b_emisor.md (ERR-51) + PROTOCOLO_canal_20260918.md (sala 3).")
    log("Semillas 1-2: NINGUNA de las 581-620 del bloque queda expuesta.")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    log(f"    origenes verificados -> {'OK' if guarda_origen() else 'FALLA'}")
    sem = [1, 2]

    log("1/4 IDENTIDAD (subconjunto; el arnes completo, 95/95, va en identidad_familias_b4b.py).")
    ident = []
    for cual in CASOS_ID:
        for s in sem:
            ident.append(tarea(('ID', cual, s, 6000)))
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {CASOS_ID[cual][0]:60s} {sum(r['ok'] for r in g)}/{len(g)}"
            + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']}"))
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)}")

    log("2/4 DIAGNOSTICO ESTRUCTURAL (antes de simular): alias exacto por par y por semilla, U3.")
    diags = []
    for s in sem:
        d = CF.diagnostico(s, nk, ktop, BASE)
        diags.append(d)
        log(f"    semilla {s}: alias_pares {d['alias_pares']:.5f}  alias_semilla {d['alias_semilla']}  U3 {d['U3']}")

    log(f"3/4 EMISORES: {len(sem)} corridas de {Tb} pasos (de cada una salen los DOS mensajes).")
    msgs, t_b = {}, {}
    for s in sem:
        t1 = time.time(); m = emisor(s, Tb, nk, ktop, nkmax); dt = time.time() - t1
        t_b['E'] = round(t_b.get('E', 0.0) + dt, 2); msgs[s] = m
        for d in ('pos', 'neg'):
            q = m[d]
            log(f"    E s{s} ({d:3s}) {dt:5.1f}s  mensaje "
                f"{q and (q['ref'], q['R'], 't=%d' % q['t'], 'tras %d exposiciones' % q['enc'])}")

    log(f"4/4 HUMO: {len(brazos)} brazos x {len(sem)} semillas = {len(brazos)*len(sem)} corridas de {Tb} pasos.")
    res = []
    for b in brazos:
        for s in sem:
            m = msgs[s][BRAZOS[b]['dir']]
            if m is None:
                log(f"    {b:9s} s{s}  SIN MENSAJE en esa direccion: excluida (P-I2)"); continue
            t1 = time.time(); r = tarea(('R', b, s, m, Tb, nk, ktop, nkmax)); dt = time.time() - t1
            res.append(r); t_b[b] = round(t_b.get(b, 0.0) + dt, 2)
            B, M = r['B4'], r['mem']
            log(f"    {b:9s} s{s} {dt:5.1f}s  entrega t={r['t_entrega']}  {B['ref']} es {B['val_ref']}  "
                f"evX {B['evX']} (okX {B['okX']}, via {'RAPIDA' if B['fam1'] else 'lenta'})  evU {B['evU']} "
                f"okU {B['okU']}  comH {B['comH']}  esp {B['esp']}  ret2/3 {B['ret2']}/{B['ret3']}  "
                f"mord_ref {B['mord_ref']}  muertes {r['deaths']}"
                + (f"  | PAR hermana {B['par_fijo']}: dist {B['dist']} okP {B['okP']} lag {B['lag_par']}"
                   if B['par_fijo'] else ''))
            log(f"              MECANISMO ganadora {M['gan_pre']} -> {M['gan_post']} (variable "
                f"{M['gan_var_pre']}->{M['gan_var_post']})  casilla {M['bin_ref']}  comparten "
                f"{M['n_mismo_bin']}/32  lag {B['lag_t']} pasos / {B['lag_m']} mordidas  prefijo {r['prefijo']}")
    for sg in ('+', '-'):
        pe = {r['brazo']: r['prefijo'] for r in res
              if r['seed'] == sem[0] and r['brazo'] in ('CANAL' + sg, 'CORTADO' + sg)}
        if len(pe) == 2:
            log(f"  GEMELO (P-I3) semilla {sem[0]}, CANAL{sg}/CORTADO{sg}: {list(pe.values())} -> "
                f"{'IDENTICOS' if len(set(pe.values())) == 1 else '*** DIFIEREN'}")
    mal = CF.cruza_cod0([dict(tipo='R', seed=s, cod0=msgs[s]['cod0']) for s in sem if msgs[s].get('cod0')],
                        [dict(d, cod=CF.diagnostico(d['seed'], nk, ktop, BASE)['cod']) for d in diags])
    log(f"  CRUCE cod0 del EMISOR contra escala_codigo (bloque 0): "
        f"{'IDENTICO campo a campo' if not mal else '*** DIFIERE en ' + str(mal[:5])}")
    n_corr = len(sem) + len(res)
    seg = sum(t_b.values()) / max(n_corr, 1) * (T / Tb)
    n_tot = (len(ORDEN) + 1) * N_SEM
    log(f"ESTIMACION del bloque: {n_tot} corridas de {T} pasos, ~{seg:.1f} s/corrida en serie -> "
        f"~{n_tot*seg/N_PARALELO/60:.1f} min de pared con Pool({N_PARALELO}).")
    log("HUMO: numeros observados, sin ajustar nada. n<=2 y semillas vistas: NO son evidencia.")

    dj = os.path.join(RAIZ, 'datos', f'familias_b4b_humo_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_brazo=Tb, semillas=sem,
                                 T_bloque=T, nk=nk, ktop=ktop, nkmax=nkmax, brazos=N(BRAZOS), umbrales=UMBRALES,
                                 mundo=N(MUNDO), kw_E=N(KW_E), kw_R=N(KW_R), shas=SHAS(),
                                 segundos_por_brazo=t_b, cruce_cod0_ok=(not mal),
                                 python=platform.python_version(), numpy=np.__version__),
                       identidades=ident, diagnostico=diags, mensajes=N(msgs), brazos=res), f,
                  ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    CF._log['f'].close()


# ---------------------------------------------------------------- principal
if __name__ == '__main__':
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    nk, ktop, nkmax = arg('--nk', 30), arg('--k', 3), arg('--nkmax', 90)
    if '--brazos' in sys.argv:
        BRAZOS_ACTIVOS = [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_ACTIVOS if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--brazos: desconocido(s) {malos}. Validos: {ORDEN}")
        for b in list(BRAZOS_ACTIVOS):
            g = 'PAR0-' if b.startswith('PAR') else 'CORTADO' + b[-1]
            if g not in BRAZOS_ACTIVOS:
                raise SystemExit(f"--brazos: {g} es obligatorio (es el GEMELO de {b}).")
    if '--humo' in sys.argv:
        humo(nk, ktop, nkmax, arg('--T', T), BRAZOS_ACTIVOS); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    T = arg('--T', T)
    desde = arg('--desde', DESDE)
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_b4b_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'),
                        'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log(f"ARRANQUE BLOQUE 4b (emisor que SI descubre en la direccion ciega, voraz={VORAZ}): "
        f"brazos {BRAZOS_ACTIVOS}, "
        f"semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log("El mundo y el CANAL son los del bloque 4, sin tocar. Lo nuevo: el emisor lleva `voraz` (ERR-51) y el "
        "brazo PAR sustituye el TOKEN por una HERMANA en la presentacion del receptor.")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    if not guarda_origen():
        sys.exit(1)
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | "
                             "ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V, res = {}, []
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('ID', c, s, T_ID) for c in CASOS_ID for s in SEMILLAS_ID]
        log(f"ETAPA 1/4 — IDENTIDAD ({len(CASOS_ID)} casos x {len(SEMILLAS_ID)} = {len(ctrl)}). "
            f"(K) DEBE fallar: sin el la etapa pasa por vacuidad.")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CASOS_ID[cual][0]:60s} {sum(r['ok'] for r in g)}/{len(g)}"
                + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']} faltan {g[0]['faltan']}"))
            V[f'ID_{cual}'] = all(r['ok'] for r in g)
        V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CASOS_ID))
        log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
        if not V['G_IDENTIDAD']:
            log("*** GUARDA DE IDENTIDAD FALLIDA. Se para (P-I1).")
            sys.exit(1)

        log(f"ETAPA 2/4 — DIAGNOSTICO ESTRUCTURAL, ANTES de simular ({len(SEEDS)} semillas, T = 0).")
        diags = pool.map(tarea, [('D', s, nk, ktop) for s in SEEDS], chunksize=1)
        log(f"    alias por par mediana {med([d['alias_pares'] for d in diags])}  "
            f"semillas con algun par identico {sum(d['alias_semilla'] for d in diags)}/{len(diags)}  "
            f"U3 mediana {med([d['U3'] for d in diags])}")

        log(f"ETAPA 3/4 — EMISORES ({len(SEEDS)} corridas de {T} pasos; de cada una salen los DOS mensajes).")
        em = pool.map(tarea, [('E', s, T, nk, ktop, nkmax) for s in SEEDS], chunksize=1)
        msgs = {d['seed']: d['msgs'] for d in em}
        for d in ('pos', 'neg'):
            sin = [s for s in SEEDS if not (msgs.get(s) or {}).get(d)]
            log(f"    ({d}) emiten {len(SEEDS)-len(sin)}/{len(SEEDS)}; sin mensaje (excluidas, P-I2): {sin}; "
                f"t_msg mediana {med([m[d]['t'] for m in msgs.values() if m.get(d)])}")

        tr = [('R', b, s, msgs[s][BRAZOS[b]['dir']], T, nk, ktop, nkmax) for b in BRAZOS_ACTIVOS for s in SEEDS
              if (msgs.get(s) or {}).get(BRAZOS[b]['dir'])]
        log(f"ETAPA 4/4 — RECEPTORES: {len(tr)} corridas de {T} pasos ({len(BRAZOS_ACTIVOS)} brazos)...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    log()
    mal = CF.cruza_cod0([dict(tipo='R', seed=s, cod0=msgs[s]['cod0']) for s in SEEDS if (msgs.get(s) or {}).get('cod0')],
                        [dict(d, cod=CF.diagnostico(d['seed'], nk, ktop, BASE)['cod']) for d in diags])
    log(f"CRUCE cod0 del EMISOR contra escala_codigo (bloque 0): "
        f"{'IDENTICO campo a campo' if not mal else '*** DIFIERE en ' + str(mal[:5])}")
    V['cruce_cod0_ok'] = (not mal)
    # ERR-54: los datos crudos se guardan ANTES del analisis (dos series se perdieron por una excepcion en el analisis con --brazos)
    dcr = os.path.join(RAIZ, 'datos', f'familias_b4b_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}_crudo.json')
    with open(dcr, 'w', encoding='utf-8') as f:
        json.dump(dict(semillas=SEEDS, brazos=BRAZOS_ACTIVOS, mensajes=N(msgs), diagnostico=diags, principal=res), f, ensure_ascii=False, default=str)
    log(f"datos crudos -> {os.path.basename(dcr)}")
    log("ANALISIS — medianas, cuartiles y los umbrales EXACTOS de la seccion 6 del preregistro.")
    try:
        V.update(veredicto(res, msgs, SEEDS, diags))
    except Exception as e:   # ERR-54: el analisis no puede tumbar el registro de los datos
        import traceback; log("*** ANALISIS CAYO (ERR-54): " + traceback.format_exc().splitlines()[-1]); V['brazos'] = V.get('brazos', {}); V['analisis_error'] = str(e)
    for b in ORDEN:
        d = V['brazos'].get(b)
        if not d:
            continue
        log(f"    {b:9s} evX {d['evX_n']}/{d['n']}  okX {d['okX_n']}/{d['n']}  evU {d['evU_med']}  okU "
            f"{d['okU_med']}  comH {d['comH_med']}  esp {d['esp_med']}  ret2/3 {d['ret2_n']}/{d['ret3_n']}  "
            f"nunca {d['nunca_n']}  muertes {d['muertes_med']}  via_rapida {d['fam1_n']}  "
            f"mismo_bin {d['n_mismo_bin_med']}")
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, nk=nk, ktop=ktop, nkmax=nkmax,
                brazos={b: N(BRAZOS[b]) for b in BRAZOS_ACTIVOS}, mundo=N(MUNDO), kw_E=N(KW_E), kw_R=N(KW_R),
                veredicto=ver, veredictos=N(V), identidades=rc, diagnostico=diags, mensajes=N(msgs),
                procesos_python=ps, shas=SHAS(), python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'familias_b4b_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=meta, principal=res), f, ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    CF._log['f'].close()
