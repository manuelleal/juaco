"""BLOQUE 5 -- VARIAS GANADORAS: que la referencia BAJE de la familia a la variante (H-4 de la sala 4; E-7).
Ejecuta PREREGISTRO_bloque5_ganadoras.md (su sha va en el meta del JSON).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy: que el mensaje
baje de la familia a la variante.

E-7 (el techo de 2 bits): la via lenta de v15f lee por UNA celda ganadora = UN par de pixeles = 2 bits, y esa
casilla agrupa 12 de los 32 estimulos (mediana medida en 641-660 y 661-680). Por eso el mensaje con el patron de
OTRO token arrastra la mitad del efecto (BAR-T- 9/18 y 6/19 contra CORTADO- 2/18 y 0/19) y el bloque 4b no pudo
declarar "comunicacion con referencia". La perilla `k_ganadoras` del instrumento b5 multiplica la resolucion:
k celdas de 2 bits. k = 1 es organismo_familias_b4b BIT A BIT -- el CONTROL DE OCCAM, no un competidor.

    python experimentos/nivel12_mundo_familias/corre_familias_b5.py --humo    (UN proceso, sin Pool: el creador)
    python experimentos/nivel12_mundo_familias/corre_familias_b5.py [--desde 681] [--T 100000] [--ks 1,3,5]
                                                                    [--brazos CANAL-k1,CORTADO-k1,...]

SOLO LA DIRECCION (-) (ERR-53: las dos direcciones tienen puntos ciegos distintos y no pueden compartir puerta):
  (-) "eso que evitas es COMIDA" -> el receptor NO lo aprende NUNCA solo, porque no lo muerde. Ahi el canal es
      IRREEMPLAZABLE. Puertas por direccion: P-I2 >= 18/20, P-I3 sin OTRO, P-I4, P-I5 >= 18/20.

EL EMISOR NO CAMBIA (decision declarada, preregistro 4.2): es b5 con k_ganadoras=1, o sea organismo_familias_b4b
bit a bit, con voraz = 1.0 (ERR-51). Un solo emisor por semilla, y su mensaje es el MISMO en los tres brazos k:
lo que se mide es LA LECTURA, no el habla. Lo comprueba el caso (L) del arnes.

REGLA 3 y 11: el `Pool` lo lanza SOLO el coordinador. `--humo` es UN proceso.
ERR-31: el mundo y las utilidades son los OBJETOS de los bloques 2, 3, 4 y 4b, importados, no recopiados.
ERR-44 / T-E: todo se mide sobre lo que LEE LA BOCA (`primera_b2`, `primera_b4`, `mord`), nunca sobre pesos.
ERR-52: OTRO queda fuera de P-I3 (vive en otro mundo; su prefijo difiere por construccion).
ERR-54: los datos CRUDOS se guardan ANTES del analisis, y el analisis no puede tumbar el registro.
"""
import sys, os, json, time, hashlib, platform, subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import numpy as np
import corre_familias_b4b as B4BR           # bloque 4b: el mundo, el canal, la lectura de la boca, la letra
B4R = B4BR.B4R
B3R = B4BR.B3R
B2R = B4BR.B2R
CF = B4BR.CF

T = 100000
T_ID = 20000
T_HUMO = 30000
N_PARALELO = 14
N_SEM = 20
DESDE = 681
VORAZ = B4BR.VORAZ                     # 1.0, FIJADO en el preregistro del 4b 3.2; el bloque 5 no lo toca
KS = (1, 3, 5)                         # k = 1 es el CONTROL DE OCCAM (b4b bit a bit)
SEMILLAS_ID = [1, 2, 3]
SEM_R = B4BR.SEM_R                     # desplazamiento del rng del RECEPTOR
SEM_OTRO = B4BR.SEM_OTRO               # desplazamiento del MUNDO del receptor en R-SIN-SAL
SHA_V14_ESPERADO = 'feefc88b1fd8d434'
SHA_B4B_ESPERADO = 'b3dd1d7e66a2d147'
SHA_ESCALA_ESPERADO = 'd8b8566bca77a0ae'

log, h16, N, med, cuartiles, razon, A12, cuenta = CF.log, CF.h16, CF.N, CF.med, CF.cuartiles, CF.razon, CF.A12, CF.cuenta
BASE = B2R.BASE
MUNDO, KW_E, KW_R = B4BR.MUNDO, B4BR.KW_E, B4BR.KW_R     # ERR-31: los OBJETOS del bloque 4b, no una copia
XPOS, XNEG = B4BR.XPOS, B4BR.XNEG
REF = {'neg': XNEG}                                      # ERR-53: SOLO la direccion (-)
BAR = B4BR.BAR
PATS = B4BR.PATS
prefijo = B4BR.prefijo
PAR_HERM = B4BR.PAR_HERM                                 # (1, 0): la hermana que sustituye al token en el brazo PAR

# ---------------------------------------------------------------- brazos: los 9 del 4b (-) x k
PLANTILLA = [('CANAL', 'sen', 'REF', False, None), ('CORTADO', 'mudo', 'REF', False, None),
             ('BAR-H', 'sen', 'H', False, None), ('BAR-T', 'sen', 'TK', False, None),
             ('VALOR', 'sen', 'CEROS', False, None), ('INM', 'inm', 'REF', False, None),
             ('OTRO', 'sen', 'REF', True, None),
             ('PAR', 'sen', 'REF', False, PAR_HERM), ('PAR0', 'mudo', 'REF', False, PAR_HERM)]
BRAZOS, ORDEN = {}, []
for _k in KS:
    for _n, _m, _p, _o, _ph in PLANTILLA:
        _b = '%s-k%d' % (_n, _k)
        BRAZOS[_b] = dict(dir='neg', modo=_m, pat=_p, otro=_o, par=_ph, k=_k, base=_n)
        ORDEN.append(_b)
BRAZOS_ACTIVOS = list(ORDEN)
# HUMO (declarado en el preregistro 9.1): la pregunta que decide (BAR-T) con el control de Occam y con k = 5.
BRAZOS_HUMO = ['CANAL-k1', 'CORTADO-k1', 'BAR-T-k1', 'CANAL-k5', 'CORTADO-k5', 'BAR-T-k5']
gemelo_de = lambda b: ('PAR0-k%d' % BRAZOS[b]['k']) if BRAZOS[b]['base'].startswith('PAR') \
    else ('CORTADO-k%d' % BRAZOS[b]['k'])

CASOS_ID = {   # subconjunto critico del arnes de identidad_familias_b5.py (106/106)
    'a': ("(a) k=1 == organismo_familias_b4b (mundo=AB)", 'B4B', T_ID),
    'g': ("(g) k=1 == organismo_familias_b4b (el mundo del bloque 4)", 'B4BF', T_ID),
    'n': ("(n) k=1 + mundo=AB == organismo_v14 (TRONCO)", 'V14', T_ID),
    'o': ("(o) relevo ON + mundo=AB == organismo_v15f_on", 'V15FON', T_ID),
    'x': ("(x) memoria_pares=None: k=5 == k=1 (la perilla es INERTE sin tabla)", 'INERTE', T_ID),
    'z': ("(z) la 1.a de las k ES la ganadora de b4b, y son k sin repetir", 'TOPK', 6000),
    'e': ("(e) k mal escrito LANZA (0, -1, 2.5, '3', True)", 'LANZA', 100),
    'K': ("(K) k=5 != k=1 con el relevo ON (DEBE diferir)", 'KDIF', 20000),
    'C': ("(C) CANAL-k5 != CORTADO-k5 (DEBE diferir)", 'CAN', 30000),
}

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (seccion 6)
# CONVENCION (la del registro, no la del campo `evX`): `com` = la boca MORDIO en la PRIMERA exposicion de la vida
# al referente = n - evX_n. En la direccion (-) el referente es COMIDA que el receptor evitaria para siempre.
UMBRALES = {
    'PI2': dict(frase="PUERTA -- HAY MENSAJE: el emisor voraz anota el referente ciego (T1v2, R > 0) en >= 18/20, "
                      "con t_msg < 2*deriva(R). Las semillas sin mensaje se EXCLUYEN y se reportan (regla 10)",
                n_emite=18),
    'PI3': dict(frase="PUERTA -- GEMELO, POR k: cada brazo 'sen' comparte con SU gemelo (CORTADO-k / PAR0-k) el "
                      "prefijo EXACTO de `log` hasta la entrega, en >= 18/20 (INM hasta t_msg; OTRO excluido por "
                      "ERR-52). Si cae, es el INSTRUMENTO y se para", n_min=18),
    'PI4': dict(frase="PUERTA -- NUNCA VISTO, POR k: en CORTADO-k, la primera exposicion de la VIDA al referente "
                      "coincide con el paso de la entrega, en 20/20", n_min=20),
    'PI5': dict(frase="PUERTA -- VIA POR LA QUE SE LEE, POR k: en la prueba la boca usa la via LENTA (fam1 = 0) en "
                      ">= 18/20. Si el codigo del referente le resulta FAMILIAR, el mensaje queda escrito y no "
                      "consultado, y esa semilla se reporta aparte", n_min=18),
    'R1': dict(frase="EL CANAL SIGUE INTACTO (la del 4b, sin cambios): CANAL-k COME a la primera lo que habria "
                     "evitado en >= 15/20, contra CORTADO-k <= 5/20, pareado en >= 14/20. Si cae con k > 1, "
                     "`k_ganadoras` ROMPE el mensaje y el candidato muere aqui", n_pasa=15, n_cort=5, n_par=14),
    'R2': dict(frase="LA QUE DECIDE -- OTRO TOKEN: BAR-T-k <= CORTADO-k + 3. Con k = 1 se espera que NO pase (es "
                     "b4b: 9/18 y 6/19). REFUTA H-4 si con k = 5 sigue > CORTADO + 3: el techo no era de bits, la "
                     "referencia esta en la retina (3 pixeles de variable) y la linea pasa al MUNDO", margen=3),
    'R3': dict(frase="LA HERMANA -- LA VARIANTE: BAR-H-k <= CORTADO-k + 5 (umbral mas laxo que R2 porque la "
                     "hermana comparte los 9 pixeles de forma y solo se separa en los 3 de variable). Con k = 1 "
                     "no pasa (15/18 y 13/19)", margen=5),
    'R4': dict(frase="HACE FALTA EL CAMPO DE REFERENCIA: VALOR-k <= CORTADO-k + 3 (ya pasaba a k = 1; no puede "
                     "empeorar)", margen=3),
    'R5': dict(frase="ESPECIFICIDAD ENTRE HERMANAS (brazo PAR): `dist` = la boca trata DISTINTO a la excepcion y a "
                     "su hermana en su primera exposicion tras la entrega, en >= 12/20, Y dist(PAR-k) >= "
                     "dist(PAR0-k) + 5 (el gemelo mudo tiene hoy 4/18 y 7/19 de base). Covariable obligatoria "
                     "`lag_par`: si es alta, el mensaje ya se habia borrado y `dist` mide olvido, no referencia",
                n_pasa=12, sobre_gemelo=5),
    'R6': dict(frase="EL CANDIDATO NO PUEDE COSTAR EL ORGANISMO: muertes(CANAL-k) <= 1.5 x muertes(CANAL-k1) en "
                     "mediana Y okU (acierto en las 6 variantes de control, que NO son ninguna de las dos "
                     "excepciones) >= okU(CANAL-k1) - 0.10 en mediana", factor=1.5, caida_okU=0.10),
    'D1': dict(frase="DIAGNOSTICO -- LA RESOLUCION, observada y no prometida: `n_mismo_bin_k` = cuantos de los 32 "
                     "estimulos caen en LAS k casillas del mensaje. Con k = 1 la mediana medida es 12/32. Piso "
                     "estructural: si las k celdas son todas de FORMA, la interseccion no puede bajar de 4 (el "
                     "token y sus 3 variantes) -- o sea, de la FAMILIA. Bajar de 4 exige que entre en el top-k una "
                     "celda con pixel VARIABLE (`gan_var`, hoy 1/18 antes del mensaje)"),
    'D2': dict(frase="DIAGNOSTICO ESTRUCTURAL (T = 0, sin simular, seccion 5.4): de las 66 celdas, en cuantas NO "
                     "se distingue el referente del patron de BAR-T y de BAR-H, y lo mismo restringido a las 36 "
                     "celdas que solo usan pixeles de FORMA"),
}


# ---------------------------------------------------------------- diagnostico estructural (T = 0, no simula)
PARES12 = [(i, j) for i in range(12) for j in range(i + 1, 12)]


def estructura_k(fam_seed, D=12, n_var=3):
    """Cuantas de las 66 celdas NO distinguen el referente de cada barajado. NO simula: solo el catalogo."""
    Q = PATS(fam_seed)
    b = lambda c, P: int(P[PARES12[c][0]]) * 2 + int(P[PARES12[c][1]])
    forma = [c for c in range(len(PARES12)) if max(PARES12[c]) < D - n_var]
    X = Q[XNEG]
    out = dict(fam_seed=int(fam_seed), n_celdas=len(PARES12), n_forma=len(forma))
    for nom, otro in (('BAR_T', BAR['neg']['TK']), ('BAR_H', BAR['neg']['H']), ('VALOR', [0.0] * D)):
        P = Q[otro] if isinstance(otro, str) else otro
        col = [c for c in range(len(PARES12)) if b(c, X) == b(c, P)]
        out[nom] = round(len(col) / len(PARES12), 4)
        out[nom + '_forma'] = round(len([c for c in col if c in forma]) / len(forma), 4)
    # piso estructural de la interseccion si TODAS las k ganadoras usan solo pixeles de forma
    out['piso_forma'] = len([n for n in Q if all(b(c, Q[n]) == b(c, X) for c in forma)])
    return out


# ---------------------------------------------------------------- el canal de cada brazo
def canal_de(brazo, msg, fam_seed_R, D=12):
    b = BRAZOS[brazo]
    if b['pat'] == 'CEROS':
        P = [0.0] * D
    elif b['pat'] == 'REF':
        P = msg['P']                      # el patron del referente TAL COMO LO VIO EL EMISOR
    else:
        P = PATS(msg['fam_seed'])[BAR[b['dir']][b['pat']]]
    return dict(modo=b['modo'], t=msg['t'], ref=msg['ref'], P=P, R=msg['R'])


def mecanismo(r):
    """El diagnostico de b4b + lo que anade el bloque 5: las k ganadoras y quien comparte LAS k casillas."""
    d = B4BR.mecanismo(r)
    kp, kq = r.get('canal_gan_k_pre'), r.get('canal_gan_k_post')
    var = lambda L: (None if not L else sum(1 for g in L if max(g) >= 9))
    d.update(gan_k_pre=kp, gan_k_post=kq, k_var_pre=var(kp), k_var_post=var(kq),
             mismo_bin_k=r.get('canal_mismo_bin_k'),
             n_mismo_bin_k=(None if r.get('canal_mismo_bin_k') is None else len(r['canal_mismo_bin_k'])))
    return d


def resumen(brazo, seed, r, msg):
    d = dict(tipo='R', brazo=brazo, base=BRAZOS[brazo]['base'], k=BRAZOS[brazo]['k'], dir='neg', seed=seed,
             mundo=r['mundo'], deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'], fam_seed=r['fam_seed'],
             exc=r['exc'], cod0=r['cod0'], entregado=r['canal_entregado'], t_entrega=r['canal_t_entrega'],
             t_msg=r['canal_t_msg'], frac_regalo=r['frac_regalo'], renovados=r['renovados'],
             k_ganadoras=r['k_ganadoras'])
    d['B4'] = B4BR.lee_b4(r, msg['ref'])
    d['mem'] = mecanismo(r)
    d['prefijo'] = prefijo(r, r['canal_t_entrega'] if r['canal_t_entrega'] is not None else r['canal_t_msg'])
    d['prefijo_msg'] = prefijo(r, r['canal_t_msg'])
    d['bin0_igual'] = (None if r.get('canal_mismo_bin') is None else bool(msg['ref'] in r['canal_mismo_bin']))
    return d


# ---------------------------------------------------------------- tareas
NUEVAS_B5 = ('k_ganadoras', 'mem_ganadoras', 'canal_gan_k_pre', 'canal_gan_k_post', 'canal_mismo_bin_k')


def emisor(seed, Ti, nk=30, ktop=3, nkmax=90):
    """El emisor del bloque 5 = b5 con k=1 = organismo_familias_b4b bit a bit. UN mensaje: la direccion (-)."""
    import organismo_familias_b5 as B5
    kw = B2R.resuelve(KW_E, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    r = B5.run(seed, T=Ti, fam_seed=seed, canal={'modo': 'emite'}, voraz=VORAZ, k_ganadoras=1, **kw)
    em = r['canal_emitido'] or {}
    e = em.get(XNEG)
    out = {'neg': (None if e is None else dict(t=int(e[0]), ref=e[1], P=[float(x) for x in e[2]], R=float(e[3]),
                                               enc=int(e[4]), fam_seed=seed, muertes=r['deaths'],
                                               exc=list(r['exc']), voraz=float(r['voraz']),
                                               veneno=int(sum(sum(c) for k2, c in r['mord'].items()
                                                              if r['val_mundo'][k2] == 'veneno'))))}
    out['cod0'] = dict(r['cod0']); out['seed'] = seed; out['deaths'] = r['deaths']; out['voraz'] = float(r['voraz'])
    return out


def tarea(args):
    tipo = args[0]
    if tipo == 'ID':
        _, cual, seed, Ti = args
        import organismo_v14 as V14, organismo_v15f_on as V15FON
        import organismo_familias_b4b as B4B
        import organismo_familias_b5 as B5
        etiq, ref, Tc = CASOS_ID[cual]
        Tc = Tc or Ti
        salta, debe = NUEVAS_B5, False
        if ref == 'B4B':
            a, b = B4B.run(seed, T=Tc), B5.run(seed, T=Tc)
        elif ref == 'B4BF':
            k = dict(B2R.resuelve(KW_R, Tc))
            a, b = B4B.run(seed, T=Tc, fam_seed=seed, **k), B5.run(seed, T=Tc, fam_seed=seed, **k)
        elif ref == 'V14':
            a, b = V14.run(seed, T=Tc), B5.run(seed, T=Tc)
            salta = NUEVAS_B5 + ('voraz', 'par_herm', 'par_fijo')
        elif ref == 'V15FON':
            a, b = V15FON.run(seed, T=Tc), B5.run(seed, T=Tc, memoria_pares='relevo')
            salta = NUEVAS_B5 + ('voraz', 'par_herm', 'par_fijo')
        elif ref == 'INERTE':
            k = dict(B2R.resuelve(KW_R, Tc)); k['memoria_pares'] = None
            a = B5.run(seed, T=Tc, fam_seed=seed, k_ganadoras=1, **k)
            b = B5.run(seed, T=Tc, fam_seed=seed, k_ganadoras=5, **k)
            salta = ('k_ganadoras',)
        elif ref == 'TOPK':
            k = dict(B2R.resuelve(KW_R, Tc))
            ok = True
            for kk in KS:
                r = B5.run(seed, T=Tc, fam_seed=seed, k_ganadoras=kk, **k)
                ok &= (len(r['mem_ganadoras']) == kk and r['mem_ganadoras'][0] == r['mem_ganadora']
                       and len({tuple(g) for g in r['mem_ganadoras']}) == kk)
            return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=ok, debe_diferir=False,
                        ok=bool(ok), difieren=[] if ok else ['mem_ganadoras'], faltan=[])
        elif ref == 'LANZA':
            ok = True
            for mala in (0, -1, 2.5, '3', True):
                try:
                    B5.run(seed, T=Tc, k_ganadoras=mala); ok = False
                except (ValueError, TypeError):
                    pass
                except Exception:
                    ok = False
            return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=ok, debe_diferir=False,
                        ok=bool(ok), difieren=[] if ok else ['no lanza'], faltan=[])
        elif ref == 'KDIF':
            k = dict(B2R.resuelve(KW_R, Tc))
            a = B5.run(seed, T=Tc, fam_seed=seed, k_ganadoras=1, **k)
            b = B5.run(seed, T=Tc, fam_seed=seed, k_ganadoras=5, **k)
            debe = True; salta = ('k_ganadoras',)
        else:                                   # CAN: CANAL-k5 contra su gemelo mudo (DEBE diferir)
            m = emisor(seed, Tc)['neg']
            if m is None:
                return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=False, debe_diferir=True,
                            ok=False, difieren=['sin mensaje (-)'], faltan=[])
            k = B2R.resuelve(KW_R, Tc)
            a = B5.run(seed + SEM_R, T=Tc, fam_seed=seed, canal=canal_de('CORTADO-k5', m, seed),
                       k_ganadoras=5, **k)
            b = B5.run(seed + SEM_R, T=Tc, fam_seed=seed, canal=canal_de('CANAL-k5', m, seed),
                       k_ganadoras=5, **k)
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
        d['estructura'] = estructura_k(seed)
        return dict(tipo='D', **d)
    if tipo == 'E':
        _, seed, Ti, nk, ktop, nkmax = args
        return dict(tipo='E', seed=seed, msgs=emisor(seed, Ti, nk, ktop, nkmax))
    _, brazo, seed, msg, Ti, nk, ktop, nkmax = args
    import organismo_familias_b5 as B5
    kw = B2R.resuelve(KW_R, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    fsr = seed + SEM_OTRO if BRAZOS[brazo]['otro'] else seed
    r = B5.run(seed + SEM_R, T=Ti, fam_seed=fsr, canal=canal_de(brazo, msg, fsr),
               par_herm=BRAZOS[brazo]['par'], k_ganadoras=BRAZOS[brazo]['k'], **kw)
    return resumen(brazo, seed, r, msg)


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_bloque5_ganadoras.md')),
    script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_familias_b5.py')),
    instrumento=h16(os.path.join(AQUI, 'organismo_familias_b5.py')),
    arnes=h16(os.path.join(AQUI, 'identidad_familias_b5.py')),
    origen_b4b=h16(os.path.join(AQUI, 'organismo_familias_b4b.py')),
    runner_bloque4b=h16(os.path.join(AQUI, 'corre_familias_b4b.py')),
    preregistro_bloque4b=h16(os.path.join(AQUI, 'PREREGISTRO_bloque4b_emisor.md')),
    escala_codigo_bloque0=h16(os.path.join(AQUI, 'escala_codigo.py')),
    sala4_H4=h16(os.path.join(RAIZ, 'registro', 'investigacion', 'sala4_evolucion',
                              'SALA4_evolucion_20260918.md')),
    protocolo_sala3=h16(os.path.join(RAIZ, 'registro', 'investigacion', 'sala3_celulas',
                                     'PROTOCOLO_canal_20260918.md')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))


def guarda_origen():
    s, ok = SHAS(), True
    for k, esp in [('origen_organismo_v14', SHA_V14_ESPERADO), ('origen_b4b', SHA_B4B_ESPERADO),
                   ('escala_codigo_bloque0', SHA_ESCALA_ESPERADO)]:
        if s[k] != esp:
            log(f"*** ORIGEN CAMBIADO: {k} es {s[k]}, se esperaba {esp}. Reconstruir por anclas y repetir el arnes.")
            ok = False
    return ok


# ---------------------------------------------------------------- veredicto (la letra de la seccion 6)
def veredicto(res, msgs, SEEDS, diags, ks=KS):
    """TOLERA brazos de UNA direccion y subconjuntos de k: nada se indexa a ciegas (ERR-54)."""
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    val = [s for s in SEEDS if (msgs.get(s) or {}).get('neg')]
    hay = lambda b: b in G and len(G[b]) > 0
    bb = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('B4') or {}).get(c) for s in val if s in G.get(b, {})}
    mm = lambda b, c: {s: (G.get(b, {}).get(s, {}).get('mem') or {}).get(c) for s in val if s in G.get(b, {})}
    gg = lambda b, c: {s: G.get(b, {}).get(s, {}).get(c) for s in val if s in G.get(b, {})}
    n1 = lambda d: sum(1 for v in d.values() if v == 1.0)
    n0 = lambda d: sum(1 for v in d.values() if v == 0.0)
    ks = [k for k in ks if hay('CANAL-k%d' % k) and hay('CORTADO-k%d' % k)]
    V = {'umbrales': UMBRALES, 'direccion': 'neg (ERR-53)', 'ks': ks, 'n_validas': len(val),
         'excluidas': [s for s in SEEDS if s not in val]}
    V['alias'] = dict(pares_mediana=med([d['alias_pares'] for d in diags]),
                      semillas_con_alias=sum(d['alias_semilla'] for d in diags), n=len(diags),
                      U3_mediana=med([d['U3'] for d in diags]))
    es = [d['estructura'] for d in diags if d.get('estructura')]
    V['D2'] = dict(frase=UMBRALES['D2']['frase'], n=len(es),
                   BAR_T=med([d['BAR_T'] for d in es]), BAR_T_forma=med([d['BAR_T_forma'] for d in es]),
                   BAR_H=med([d['BAR_H'] for d in es]), BAR_H_forma=med([d['BAR_H_forma'] for d in es]),
                   VALOR=med([d['VALOR'] for d in es]), VALOR_forma=med([d['VALOR_forma'] for d in es]),
                   piso_forma=med([d['piso_forma'] for d in es]))

    # --- puertas
    derR = B2R.resuelve(KW_R, T)['deriva']
    u = UMBRALES['PI2']
    V['PI2'] = dict(n_emite=len(val), n=len(SEEDS), deriva_R=derR,
                    signo_ok=sum(1 for s in val if msgs[s]['neg']['R'] > 0),
                    n_antes=sum(1 for s in val if msgs[s]['neg']['t'] < 2 * derR),
                    t_msg_med=med([msgs[s]['neg']['t'] for s in val]),
                    enc_med=med([msgs[s]['neg']['enc'] for s in val]))
    V['PI2']['pasa'] = bool(V['PI2']['n_emite'] >= min(u['n_emite'], len(SEEDS))
                            and V['PI2']['signo_ok'] == len(val) and V['PI2']['n_antes'] == len(val))
    u = UMBRALES['PI3']
    V['PI3'] = {}
    for b in BRAZOS_ACTIVOS:
        g = gemelo_de(b)
        if b == g or BRAZOS[b]['base'] == 'OTRO' or BRAZOS[b]['modo'] == 'mudo' or not hay(b) or not hay(g):
            continue      # ERR-52: OTRO vive en otro mundo; su gemelo no es CORTADO
        kk = 'prefijo_msg' if BRAZOS[b]['base'] == 'INM' else 'prefijo'
        pc = gg(g, kk)
        V['PI3'][b] = sum(1 for s in val if gg(b, kk).get(s) is not None and gg(b, kk).get(s) == pc.get(s))
    V['PI3']['pasa'] = bool(V['PI3'] and all(v >= min(u['n_min'], len(val))
                                             for kk, v in V['PI3'].items() if kk != 'pasa'))
    u = UMBRALES['PI4']
    V['PI4'] = {}
    for k in ks:
        c = 'CORTADO-k%d' % k
        V['PI4']['k%d' % k] = dict(n=sum(1 for s in val if bb(c, 't_X').get(s) is not None
                                         and bb(c, 't_X').get(s) == gg(c, 't_entrega').get(s)), n_val=len(val))
    V['PI4']['pasa'] = bool(V['PI4'] and all(v['n'] >= min(u['n_min'], len(val))
                                             for kk, v in V['PI4'].items() if kk != 'pasa'))
    u = UMBRALES['PI5']
    V['PI5'] = {}
    for k in ks:
        c = 'CORTADO-k%d' % k
        V['PI5']['k%d' % k] = dict(lenta=sum(1 for v in bb(c, 'fam1').values() if v == 0), n=len(val))
    V['PI5']['pasa'] = bool(V['PI5'] and all(v['lenta'] >= min(u['n_min'], len(val))
                                             for kk, v in V['PI5'].items() if kk != 'pasa'))

    # --- por brazo (`com` = mordio a la 1.a; la convencion del registro)
    V['brazos'] = {}
    for b in BRAZOS_ACTIVOS:
        if not hay(b):
            continue
        eX = bb(b, 'evX')
        V['brazos'][b] = dict(
            k=BRAZOS[b]['k'], base=BRAZOS[b]['base'],
            n=len([v for v in eX.values() if v is not None]), com_n=n0(eX), evX_n=n1(eX), okX_n=n1(bb(b, 'okX')),
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
            k_var_pre_med=med([v for v in mm(b, 'k_var_pre').values() if v is not None]),
            k_var_post_med=med([v for v in mm(b, 'k_var_post').values() if v is not None]),
            n_mismo_bin_med=med([v for v in mm(b, 'n_mismo_bin').values() if v is not None]),
            n_mismo_bin_k_med=med([v for v in mm(b, 'n_mismo_bin_k').values() if v is not None]))
    Bz = V['brazos']
    com = lambda b: Bz[b]['com_n'] if b in Bz else None

    # --- R1..R6, por k
    for nom in ('R1', 'R2', 'R3', 'R4', 'R5', 'R6'):
        V[nom] = {}
    for k in ks:
        kk = 'k%d' % k
        CA, CO = 'CANAL-k%d' % k, 'CORTADO-k%d' % k
        u = UMBRALES['R1']
        dk, dc = bb(CA, 'evX'), bb(CO, 'evX')
        par = sum(1 for s in val if dk.get(s) is not None and dc.get(s) is not None and dk[s] < dc[s])
        V['R1'][kk] = dict(canal=com(CA), cortado=com(CO), n=Bz[CA]['n'], n_menor=par,
                           A12=A12(list(dk.values()), list(dc.values())),
                           pasa=bool(com(CA) >= min(u['n_pasa'], Bz[CA]['n']) and com(CO) <= u['n_cort']
                                     and par >= min(u['n_par'], Bz[CA]['n'])))
        for nom, base in (('R2', 'BAR-T'), ('R3', 'BAR-H'), ('R4', 'VALOR')):
            b = '%s-k%d' % (base, k)
            if not hay(b):
                continue
            u = UMBRALES[nom]
            V[nom][kk] = dict(brazo=b, com=com(b), cortado=com(CO), canal=com(CA), n=Bz[b]['n'],
                              margen=u['margen'], exceso=com(b) - com(CO) - u['margen'],
                              pasa=bool(com(b) <= com(CO) + u['margen']))
        u = UMBRALES['R5']
        PA, P0 = 'PAR-k%d' % k, 'PAR0-k%d' % k
        if hay(PA) and hay(P0):
            V['R5'][kk] = dict(dist=Bz[PA]['dist_n'], n=Bz[PA]['n_dist'], dist_gemelo=Bz[P0]['dist_n'],
                               n_gemelo=Bz[P0]['n_dist'], okP=Bz[PA]['okP_n'], com=com(PA), com_gemelo=com(P0),
                               lag_par=Bz[PA]['lag_par_med'])
            V['R5'][kk]['pasa'] = bool(Bz[PA]['dist_n'] >= min(u['n_pasa'], max(Bz[PA]['n_dist'], 1))
                                       and Bz[PA]['dist_n'] >= Bz[P0]['dist_n'] + u['sobre_gemelo'])
        u = UMBRALES['R6']
        ref1 = 'CANAL-k1'
        if hay(ref1):
            m1, mk = Bz[ref1]['muertes_med'], Bz[CA]['muertes_med']
            o1, ok_ = Bz[ref1]['okU_med'], Bz[CA]['okU_med']
            V['R6'][kk] = dict(muertes=mk, muertes_k1=m1, okU=ok_, okU_k1=o1, celdas=Bz[CA]['celdas_med'],
                               pasa=bool(mk is not None and m1 is not None and mk <= u['factor'] * max(m1, 1)
                                         and ok_ is not None and o1 is not None
                                         and ok_ >= o1 - u['caida_okU']))
    V['D1'] = {('k%d' % k): dict(n_mismo_bin=Bz['CANAL-k%d' % k]['n_mismo_bin_med'],
                                 n_mismo_bin_k=Bz['CANAL-k%d' % k]['n_mismo_bin_k_med'],
                                 k_var_pre=Bz['CANAL-k%d' % k]['k_var_pre_med'],
                                 k_var_post=Bz['CANAL-k%d' % k]['k_var_post_med'])
              for k in ks}
    V['DECLARA'] = {('k%d' % k): bool(V['PI2']['pasa'] and V['PI3']['pasa'] and V['PI4']['pasa']
                                      and V['PI5']['pasa'] and V['R1'].get('k%d' % k, {}).get('pasa')
                                      and V['R2'].get('k%d' % k, {}).get('pasa')
                                      and V['R3'].get('k%d' % k, {}).get('pasa')
                                      and V['R4'].get('k%d' % k, {}).get('pasa')) for k in ks}
    return V


def frase_final(V):
    for g in ('PI2', 'PI3', 'PI4', 'PI5'):
        if not V.get(g, {}).get('pasa'):
            return f"{g} CAE -- es el INSTRUMENTO o el montaje. Nada se declara (preregistro 5.2)."
    s = "DIRECCION (-) SOLA (ERR-53). `com` = comio a la 1.a exposicion de la vida al referente. "
    for k in V['ks']:
        kk = 'k%d' % k
        R = lambda n: V.get(n, {}).get(kk, {})
        s += (f"[k={k}] CANAL {R('R1').get('canal')}/{R('R1').get('n')} contra CORTADO "
              f"{R('R1').get('cortado')} -> R1 {'pasa' if R('R1').get('pasa') else 'CAE'}; "
              f"BAR-T {R('R2').get('com')} -> R2 {'pasa' if R('R2').get('pasa') else 'CAE'}; "
              f"BAR-H {R('R3').get('com')} -> R3 {'pasa' if R('R3').get('pasa') else 'CAE'}; "
              f"VALOR {R('R4').get('com')} -> R4 {'pasa' if R('R4').get('pasa') else 'CAE'}; "
              f"PAR dist {R('R5').get('dist')}/{R('R5').get('n')} (gemelo {R('R5').get('dist_gemelo')}) -> R5 "
              f"{'pasa' if R('R5').get('pasa') else 'CAE'}; coste R6 "
              f"{'pasa' if R('R6').get('pasa') else 'CAE'}; comparten LAS k casillas "
              f"{V['D1'][kk]['n_mismo_bin_k']}/32 (una sola: {V['D1'][kk]['n_mismo_bin']}/32), celdas con pixel "
              f"variable en el top-k {V['D1'][kk]['k_var_post']}. ")
    dec = [k for k in V['ks'] if V['DECLARA'].get('k%d' % k)]
    s += ("DECLARA (R1-R4 con todas las puertas) en k = " + str(dec) if dec else
          "NINGUNA k cumple R1-R4: no se declara nada")
    s += (f". Piso estructural de la interseccion si el top-k es todo de FORMA: {V['D2']['piso_forma']} de 32 "
          f"(la FAMILIA). Alias por par {V['alias']['pares_mediana']} "
          f"({V['alias']['semillas_con_alias']}/{V['alias']['n']} semillas). 20 semillas no cierran nada: "
          f"replica en el rango siguiente (regla 12).")
    return s


# ---------------------------------------------------------------- humo (UN proceso, sin Pool, regla 3)
def humo(nk, ktop, nkmax, Tb, brazos):
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_b5_humo_{stamp}.log'), 'w',
                        encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log(f"HUMO del creador del bloque 5 (VARIAS GANADORAS), UN proceso, sin Pool (regla 3). k = {KS}.")
    log("PREREGISTRO_bloque5_ganadoras.md (H-4 de la sala 4; E-7) + PROTOCOLO_canal_20260918.md (sala 3).")
    log("Semillas 1-2: NINGUNA de las 681-720 del bloque queda expuesta.")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    log(f"    origenes verificados -> {'OK' if guarda_origen() else 'FALLA'}")
    sem = [1, 2]

    log("1/4 IDENTIDAD (subconjunto; el arnes completo, 106/106, va en identidad_familias_b5.py).")
    ident = []
    for cual in CASOS_ID:
        for s in sem:
            ident.append(tarea(('ID', cual, s, 6000)))
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {CASOS_ID[cual][0]:62s} {sum(r['ok'] for r in g)}/{len(g)}"
            + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']}"))
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)}")

    log("2/4 DIAGNOSTICO ESTRUCTURAL (antes de simular, T = 0): alias, U3 y la resolucion de las 66 celdas.")
    diags = []
    for s in sem:
        d = CF.diagnostico(s, nk, ktop, BASE)
        d.pop('cod'); d['estructura'] = estructura_k(s)
        diags.append(dict(tipo='D', **d))
        e = d['estructura']
        log(f"    semilla {s}: alias_pares {d['alias_pares']:.5f}  alias_semilla {d['alias_semilla']}  "
            f"U3 {d['U3']}  |  celdas que NO distinguen: BAR-T {e['BAR_T']} (forma {e['BAR_T_forma']}), "
            f"BAR-H {e['BAR_H']} (forma {e['BAR_H_forma']}), VALOR {e['VALOR']}; piso de forma {e['piso_forma']}/32")

    log(f"3/4 EMISORES (k = 1 = b4b bit a bit): {len(sem)} corridas de {Tb} pasos.")
    msgs, t_b = {}, {}
    for s in sem:
        t1 = time.time(); m = emisor(s, Tb, nk, ktop, nkmax); dt = time.time() - t1
        t_b['E'] = round(t_b.get('E', 0.0) + dt, 2); msgs[s] = m
        q = m['neg']
        log(f"    E s{s} (neg) {dt:5.1f}s  mensaje "
            f"{q and (q['ref'], q['R'], 't=%d' % q['t'], 'tras %d exposiciones' % q['enc'])}")

    log(f"4/4 HUMO: {len(brazos)} brazos x {len(sem)} semillas = {len(brazos)*len(sem)} corridas de {Tb} pasos.")
    res = []
    for b in brazos:
        for s in sem:
            m = msgs[s]['neg']
            if m is None:
                log(f"    {b:12s} s{s}  SIN MENSAJE: excluida (P-I2)"); continue
            t1 = time.time(); r = tarea(('R', b, s, m, Tb, nk, ktop, nkmax)); dt = time.time() - t1
            res.append(r); t_b[b] = round(t_b.get(b, 0.0) + dt, 2)
            B, M = r['B4'], r['mem']
            log(f"    {b:12s} s{s} {dt:5.1f}s  entrega t={r['t_entrega']}  {B['ref']} es {B['val_ref']}  "
                f"comio {1-int(B['evX'] or 0)} (okX {B['okX']}, via {'RAPIDA' if B['fam1'] else 'lenta'})  "
                f"evU {B['evU']} okU {B['okU']}  comH {B['comH']}  ret2/3 {B['ret2']}/{B['ret3']}  "
                f"muertes {r['deaths']}  celdas {r['celdas']}")
            log(f"                 MECANISMO k={r['k_ganadoras']} ganadoras {M['gan_k_post']}  con pixel "
                f"variable {M['k_var_post']}/{r['k_ganadoras']}  comparten LAS k casillas {M['n_mismo_bin_k']}/32 "
                f"(una sola: {M['n_mismo_bin']}/32)  lag {B['lag_t']} pasos / {B['lag_m']} mordidas  "
                f"prefijo {r['prefijo']}")
    for k in sorted({BRAZOS[b]['k'] for b in brazos}):
        pe = {r['brazo']: r['prefijo'] for r in res
              if r['seed'] == sem[0] and r['brazo'] in ('CANAL-k%d' % k, 'CORTADO-k%d' % k)}
        if len(pe) == 2:
            log(f"  GEMELO (P-I3) semilla {sem[0]}, CANAL-k{k}/CORTADO-k{k}: {list(pe.values())} -> "
                f"{'IDENTICOS' if len(set(pe.values())) == 1 else '*** DIFIEREN'}")
    # OJO (candidato a ERR): `CF.cruza_cod0` SALTA toda fila con `mundo` in (None,'AB'); en corre_familias_b4.py
    # y corre_familias_b4b.py las filas se construyen SIN `mundo`, asi que el cruce era VACUO. Aqui va el campo.
    mal = CF.cruza_cod0([dict(tipo='R', seed=s, mundo='familias', cod0=msgs[s]['cod0'])
                         for s in sem if msgs[s].get('cod0')],
                        [dict(d, cod=CF.diagnostico(d['seed'], nk, ktop, BASE)['cod']) for d in diags])
    log(f"  CRUCE cod0 del EMISOR contra escala_codigo (bloque 0): "
        f"{'IDENTICO campo a campo' if not mal else '*** DIFIERE en ' + str(mal[:5])}")
    n_corr = len(sem) + len(res)
    seg = sum(t_b.values()) / max(n_corr, 1) * (T / Tb)
    n_tot = (len(ORDEN) + 1) * N_SEM
    log(f"ESTIMACION del bloque: {n_tot} corridas de {T} pasos, ~{seg:.1f} s/corrida en serie -> "
        f"~{n_tot*seg/N_PARALELO/60:.1f} min de pared con Pool({N_PARALELO}).")
    log("HUMO: numeros observados, sin ajustar nada. n<=2 y semillas vistas: NO son evidencia.")

    dj = os.path.join(RAIZ, 'datos', f'familias_b5_humo_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_brazo=Tb, semillas=sem,
                                 T_bloque=T, nk=nk, ktop=ktop, nkmax=nkmax, ks=list(KS), brazos=N(BRAZOS),
                                 umbrales=UMBRALES, mundo=N(MUNDO), kw_E=N(KW_E), kw_R=N(KW_R), shas=SHAS(),
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
    if '--ks' in sys.argv:
        KS = tuple(int(x) for x in sys.argv[sys.argv.index('--ks') + 1].split(',') if x.strip())
        BRAZOS_ACTIVOS = [b for b in ORDEN if BRAZOS[b]['k'] in KS]
    if '--brazos' in sys.argv:
        BRAZOS_ACTIVOS = [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_ACTIVOS if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--brazos: desconocido(s) {malos}. Validos: {ORDEN}")
        for b in list(BRAZOS_ACTIVOS):
            g = gemelo_de(b)
            if g not in BRAZOS_ACTIVOS:
                raise SystemExit(f"--brazos: {g} es obligatorio (es el GEMELO de {b}).")
        KS = tuple(sorted({BRAZOS[b]['k'] for b in BRAZOS_ACTIVOS}))
    if '--humo' in sys.argv:
        bh = BRAZOS_ACTIVOS if '--brazos' in sys.argv else BRAZOS_HUMO
        humo(nk, ktop, nkmax, arg('--T', T_HUMO), bh); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    T = arg('--T', T)
    desde = arg('--desde', DESDE)
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_b5_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'),
                        'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log(f"ARRANQUE BLOQUE 5 (VARIAS GANADORAS; H-4 de la sala 4, E-7): k = {KS}, brazos {BRAZOS_ACTIVOS}, "
        f"semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log("El mundo, el canal y el emisor son los del bloque 4b, sin tocar (el emisor es k = 1 = b4b bit a bit). "
        "Lo unico nuevo es CUANTAS celdas LEE la via lenta del RECEPTOR.")
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
            f"(K) y (C) DEBEN fallar: sin ellos la etapa pasa por vacuidad.")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CASOS_ID[cual][0]:62s} {sum(r['ok'] for r in g)}/{len(g)}"
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
        log(f"    celdas de las 66 que NO distinguen el referente: BAR-T "
            f"{med([d['estructura']['BAR_T'] for d in diags])} (solo forma "
            f"{med([d['estructura']['BAR_T_forma'] for d in diags])}), BAR-H "
            f"{med([d['estructura']['BAR_H'] for d in diags])} (solo forma "
            f"{med([d['estructura']['BAR_H_forma'] for d in diags])}); piso de forma "
            f"{med([d['estructura']['piso_forma'] for d in diags])}/32")

        log(f"ETAPA 3/4 — EMISORES ({len(SEEDS)} corridas de {T} pasos; k = 1 = b4b bit a bit).")
        em = pool.map(tarea, [('E', s, T, nk, ktop, nkmax) for s in SEEDS], chunksize=1)
        msgs = {d['seed']: d['msgs'] for d in em}
        sin = [s for s in SEEDS if not (msgs.get(s) or {}).get('neg')]
        log(f"    (neg) emiten {len(SEEDS)-len(sin)}/{len(SEEDS)}; sin mensaje (excluidas, P-I2): {sin}; "
            f"t_msg mediana {med([m['neg']['t'] for m in msgs.values() if m.get('neg')])}")

        tr = [('R', b, s, msgs[s]['neg'], T, nk, ktop, nkmax) for b in BRAZOS_ACTIVOS for s in SEEDS
              if (msgs.get(s) or {}).get('neg')]
        log(f"ETAPA 4/4 — RECEPTORES: {len(tr)} corridas de {T} pasos ({len(BRAZOS_ACTIVOS)} brazos)...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    log()
    mal = CF.cruza_cod0([dict(tipo='R', seed=s, mundo='familias', cod0=msgs[s]['cod0'])
                         for s in SEEDS if (msgs.get(s) or {}).get('cod0')],
                        [dict(d, cod=CF.diagnostico(d['seed'], nk, ktop, BASE)['cod']) for d in diags])
    log(f"CRUCE cod0 del EMISOR contra escala_codigo (bloque 0): "
        f"{'IDENTICO campo a campo' if not mal else '*** DIFIERE en ' + str(mal[:5])}")
    V['cruce_cod0_ok'] = (not mal)
    # ERR-54: los datos crudos se guardan ANTES del analisis. El analisis NO puede tumbar el registro de datos.
    dcr = os.path.join(RAIZ, 'datos', f'familias_b5_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}_crudo.json')
    with open(dcr, 'w', encoding='utf-8') as f:
        json.dump(dict(semillas=SEEDS, ks=list(KS), brazos=BRAZOS_ACTIVOS, mensajes=N(msgs), diagnostico=diags,
                       identidades=rc, principal=res, shas=SHAS()), f, ensure_ascii=False, default=str)
    log(f"datos crudos -> {os.path.basename(dcr)}  sha256_16 = {h16(dcr)}")
    log("ANALISIS — medianas y los umbrales EXACTOS de la seccion 6 del preregistro.")
    try:
        V.update(veredicto(res, msgs, SEEDS, diags, KS))
    except Exception as e:   # ERR-54: el analisis no puede tumbar el registro de los datos
        import traceback
        log("*** ANALISIS CAYO (ERR-54): " + traceback.format_exc().splitlines()[-1])
        V['brazos'] = V.get('brazos', {}); V['analisis_error'] = str(e)
    for b in ORDEN:
        d = V.get('brazos', {}).get(b)
        if not d:
            continue
        log(f"    {b:12s} com {d['com_n']}/{d['n']}  okX {d['okX_n']}/{d['n']}  evU {d['evU_med']}  okU "
            f"{d['okU_med']}  comH {d['comH_med']}  ret2/3 {d['ret2_n']}/{d['ret3_n']}  nunca {d['nunca_n']}  "
            f"muertes {d['muertes_med']}  celdas {d['celdas_med']}  via_rapida {d['fam1_n']}  "
            f"mismo_bin {d['n_mismo_bin_med']}  mismo_bin_k {d['n_mismo_bin_k_med']}  "
            f"var_en_topk {d['k_var_post_med']}  dist {d['dist_n']}/{d['n_dist']}")
    try:
        ver = frase_final(V)
    except Exception as e:
        ver = f"(frase final no calculable: {e})"
    log(); log(f"VEREDICTO: {ver}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, nk=nk, ktop=ktop, nkmax=nkmax,
                ks=list(KS), brazos={b: N(BRAZOS[b]) for b in BRAZOS_ACTIVOS}, mundo=N(MUNDO), kw_E=N(KW_E),
                kw_R=N(KW_R), veredicto=ver, veredictos=N(V), identidades=rc, diagnostico=diags,
                mensajes=N(msgs), procesos_python=ps, shas=SHAS(), python=platform.python_version(),
                numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'familias_b5_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=meta, principal=res), f, ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    CF._log['f'].close()
