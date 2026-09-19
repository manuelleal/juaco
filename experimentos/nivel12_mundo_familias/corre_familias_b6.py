"""BLOQUE 6 -- SUFIJO DE VARIANTE: que el mensaje distinga "sal rosa" de "sal" (E-8).
Ejecuta PREREGISTRO_bloque6_sufijo.md (su sha va en el meta del JSON).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy: que el mensaje
distinga la VARIANTE, no solo la familia.

E-8 (el techo de la FORMA): la via lenta direcciona la tabla por el bin de 2 bits de un par de pixeles, y las
celdas que ganan son de FORMA (px 0-8), ciegas por construccion a los 3 px de VARIANTE (9-11). El bloque 5 midio
que `k_ganadoras`=3 cierra el otro token (BAR-T 2/20 y 4/18) pero NO la hermana (BAR-H 15/20 y 13/18), y que k=5
rompe el cuerpo (muertes 199.5 y 152). H-4 cerrada: no es k. La perilla `memoria_variante` del instrumento b6
mete la firma de los 3 px de variante en LA DIRECCION de cada celda: 32 subcasillas en vez de 4.

    python experimentos/nivel12_mundo_familias/corre_familias_b6.py --humo    (UN proceso, sin Pool: el creador)
    python experimentos/nivel12_mundo_familias/corre_familias_b6.py [--desde 721] [--T 100000]
                                                                    [--celdas k1v0,k3v1] [--brazos ...]

FACTORIAL 2 x 2 (preregistro 3.3): k in {1, 3} x sufijo in {0, 1}.
  k1v0 = organismo_familias_b4b BIT A BIT (control de Occam, gratis)
  k3v0 = el k = 3 del bloque 5 BIT A BIT (la linea base de la que hay que mejorar)
  k1v1 = el sufijo SOLO
  k3v1 = EL BRAZO QUE DECIDE (objetivo O-6: BAR-H <= CORTADO + 5 con CANAL >= 15/20 y BAR-T <= CORTADO + 3)

SOLO LA DIRECCION (-) (ERR-53). EL EMISOR NO CAMBIA: corre con memoria_variante=0 y k_ganadoras=1, o sea b4b bit
a bit, y su mensaje es EL MISMO en las cuatro celdas: lo que se mide es LA LECTURA, no el habla.

REGLA 3 y 11: el `Pool` lo lanza SOLO el coordinador. `--humo` es UN proceso.
ERR-31: el mundo, el canal, el emisor y la letra son los OBJETOS de los bloques 4b y 5, importados, no recopiados.
ERR-44 / T-E: todo se mide sobre lo que LEE LA BOCA (`primera_b2`, `primera_b4`, `mord`), nunca sobre pesos.
ERR-52: OTRO queda fuera de P-I3 (vive en otro mundo; su prefijo difiere por construccion).
ERR-54: los datos CRUDOS se guardan ANTES del analisis, y el analisis no puede tumbar el registro.
ERR-64b: los controles de identidad que DEBEN diferir prueban no-vacuidad con >= 2 de 3 semillas.
ERR-70: P-I4 pasa de puerta todo-o-nada a EXCLUSION POR SEMILLA (ver el preregistro; escrito antes de la serie).
"""
import sys, os, json, time, hashlib, platform, subprocess

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import numpy as np
import corre_familias_b5 as B5R            # bloque 5: k_ganadoras, el diagnostico por k y la letra
B4BR = B5R.B4BR                            # bloque 4b: el mundo, el canal, la lectura de la boca
B4R, B3R, B2R, CF = B5R.B4R, B5R.B3R, B5R.B2R, B5R.CF

T = 100000
T_ID = 20000
T_HUMO = 30000
N_PARALELO = 14
N_SEM = 20
DESDE = 721                            # 681-720 las gasto el bloque 5; replica en 741-760
KS = (1, 3)                            # k = 5 NO entra: el bloque 5 lo refuto por coste (muertes 199.5 y 152)
MVS = (0, 1)                           # el sufijo de variante: apagado / encendido
VORAZ = B5R.VORAZ                      # 1.0, FIJADO en el preregistro del 4b 3.2
SEMILLAS_ID = [1, 2, 3]
SEM_R = B5R.SEM_R
SEM_OTRO = B5R.SEM_OTRO
NVAR = 3                               # fam_nvar: los pixeles 9, 10 y 11
SHA_V14_ESPERADO = 'feefc88b1fd8d434'
SHA_B4B_ESPERADO = 'b3dd1d7e66a2d147'
SHA_B5_ESPERADO = 'e0b6b90f6f92d5c1'
SHA_ESCALA_ESPERADO = 'd8b8566bca77a0ae'

log, h16, N, med, cuartiles, razon, A12, cuenta = CF.log, CF.h16, CF.N, CF.med, CF.cuartiles, CF.razon, CF.A12, CF.cuenta
BASE = B2R.BASE
MUNDO, KW_E, KW_R = B5R.MUNDO, B5R.KW_E, B5R.KW_R       # ERR-31: los OBJETOS del bloque 4b/5, no una copia
XPOS, XNEG = B5R.XPOS, B5R.XNEG
BAR = B5R.BAR
PATS = B5R.PATS
prefijo = B5R.prefijo
PAR_HERM = B5R.PAR_HERM
PARES12 = B5R.PARES12

# ---------------------------------------------------------------- brazos: los 9 del 4b (-) x k x sufijo = 36
PLANTILLA = B5R.PLANTILLA
CELDAS = ['k%dv%d' % (k, mv) for k in KS for mv in MVS]
BRAZOS, ORDEN = {}, []
for _k in KS:
    for _mv in MVS:
        for _n, _m, _p, _o, _ph in PLANTILLA:
            _b = '%s-k%dv%d' % (_n, _k, _mv)
            BRAZOS[_b] = dict(dir='neg', modo=_m, pat=_p, otro=_o, par=_ph, k=_k, mv=_mv,
                              cel='k%dv%d' % (_k, _mv), base=_n)
            ORDEN.append(_b)
BRAZOS_ACTIVOS = list(ORDEN)
CELDAS_ACTIVAS = list(CELDAS)
# HUMO (preregistro 9.1): la pregunta que decide (BAR-H) y la especificidad (PAR), con sufijo ON y OFF, a k = 3.
BRAZOS_HUMO = ['CANAL-k3v0', 'CORTADO-k3v0', 'BAR-H-k3v0', 'PAR-k3v0', 'PAR0-k3v0',
               'CANAL-k3v1', 'CORTADO-k3v1', 'BAR-H-k3v1', 'PAR-k3v1', 'PAR0-k3v1']
gemelo_de = lambda b: ('PAR0-%s' % BRAZOS[b]['cel']) if BRAZOS[b]['base'].startswith('PAR') \
    else ('CORTADO-%s' % BRAZOS[b]['cel'])

CASOS_ID = {   # subconjunto critico del arnes de identidad_familias_b6.py (59/59)
    'a': ("(a) sufijo OFF == organismo_familias_b5 (mundo=AB, k=3)", 'B5', T_ID),
    'g': ("(g) sufijo OFF == organismo_familias_b5 (el mundo del bloque 4, k=3)", 'B5F', T_ID),
    'b': ("(b) sufijo OFF + k=1 == organismo_familias_b4b (el mundo del bloque 4)", 'B4B', T_ID),
    'n': ("(n) sufijo OFF + k=1 + mundo=AB == organismo_v14 (TRONCO)", 'V14', T_ID),
    'o': ("(o) relevo ON + mundo=AB == organismo_v15f_on", 'V15FON', T_ID),
    'x': ("(x) memoria_pares=None: sufijo ON == sufijo OFF (la perilla es INERTE sin tabla)", 'INERTE', T_ID),
    'd': ("(d) la DIRECCION: 4 subcasillas OFF, 32 ON, y la hermana FUERA del grupo con sufijo", 'DIR', 8000),
    'e': ("(e) memoria_variante mal escrita LANZA (2, -1, 0.5, '1', True)", 'LANZA', 100),
    'K': ("(K) sufijo ON != sufijo OFF con el relevo ON (DEBE diferir)", 'VDIF', 20000),
    'C': ("(C) CANAL-k3v1 != CORTADO-k3v1 (DEBE diferir)", 'CAN', 60000),
    'H': ("(H) BAR-H-k3v1 != CANAL-k3v1 (DEBE diferir: es el brazo que decide)", 'HER', 60000),
}

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (seccion 6)
UMBRALES = {
    'PI2': dict(frase="PUERTA -- HAY MENSAJE: el emisor voraz (mv=0, k=1 = b4b bit a bit) anota el referente "
                      "ciego (T1v2, R > 0) en >= 18/20, con t_msg < 2*deriva(R). Las semillas sin mensaje se "
                      "EXCLUYEN y se reportan (regla 10)", n_emite=18),
    'PI3': dict(frase="PUERTA -- GEMELO, POR CELDA: cada brazo 'sen' comparte con SU gemelo de la MISMA celda "
                      "(CORTADO-kNvM / PAR0-kNvM) el prefijo EXACTO de `log` hasta la entrega, en >= 18/20 (INM "
                      "hasta t_msg; OTRO excluido por ERR-52). Si cae, es el INSTRUMENTO y se para", n_min=18),
    'PI4': dict(frase="PUERTA -- NUNCA VISTO (ERR-70): la primera exposicion de la VIDA al referente coincide "
                      "con el paso de la entrega. Ya NO es todo-o-nada: la semilla en la que no coincide se "
                      "EXCLUYE de los conteos pareados de TODOS los brazos y se reporta aparte; la puerta pide "
                      ">= 18/20 semillas utilizables, y el bloque se para si se excluyen mas de 4/20",
                n_min=18, max_excluidas=4),
    'PI5': dict(frase="PUERTA -- VIA POR LA QUE SE LEE, POR CELDA: en la prueba la boca usa la via LENTA "
                      "(fam1 = 0) en >= 18/20. Si el codigo del referente le resulta FAMILIAR, el mensaje queda "
                      "escrito y no consultado, y esa semilla se reporta aparte", n_min=18),
    'R1': dict(frase="EL CANAL SIGUE INTACTO: CANAL COME a la primera lo que habria evitado en >= 15/20, contra "
                     "CORTADO <= 5/20, pareado en >= 14/20. Si cae con el sufijo, la dispersion x8 ROMPIO el "
                     "mensaje y el candidato muere aqui", n_pasa=15, n_cort=5, n_par=14),
    'R2': dict(frase="OTRO TOKEN (lo que ya gano el bloque 5): BAR-T <= CORTADO + 3. Con k = 1 se espera que NO "
                     "pase; con k = 3 debe seguir pasando CON y SIN sufijo", margen=3),
    'R3': dict(frase="LA QUE DECIDE -- LA HERMANA: BAR-H <= CORTADO + 5. Hoy NO pasa en ninguna celda sin sufijo "
                     "(13-16/20). REFUTA el mecanismo si con sufijo sigue > CORTADO + 5: entonces la variante no "
                     "esta, para el receptor, en esos 3 pixeles, y se mide donde esta (preregistro 6.3)",
                margen=5),
    'R4': dict(frase="HACE FALTA EL CAMPO DE REFERENCIA: VALOR <= CORTADO + 3", margen=3),
    'R5': dict(frase="ESPECIFICIDAD ENTRE HERMANAS (brazo PAR): `dist` >= 12/20 Y dist(PAR) >= dist(PAR0) + 5. "
                     "Covariable obligatoria `lag_par`: si es alta, el mensaje ya se habia borrado y `dist` mide "
                     "olvido, no referencia", n_pasa=12, sobre_gemelo=5),
    'R6': dict(frase="EL CANDIDATO NO PUEDE COSTAR EL ORGANISMO: muertes(CANAL-celda) <= 1.5 x "
                     "muertes(CANAL-k1v0) en mediana Y okU >= okU(CANAL-k1v0) - 0.10 en mediana. Es la puerta "
                     "que mato a k = 5 en el bloque 5", factor=1.5, caida_okU=0.10),
    'O6': dict(frase="EL OBJETIVO DEL BLOQUE, en la celda k3v1 y en LAS DOS series: BAR-H <= CORTADO + 5 (hoy "
                     "13-16/20) CON CANAL >= 15/20, BAR-T <= CORTADO + 3 y dist(PAR) >= 12/20 INTACTOS",
                celda='k3v1'),
    'D1': dict(frase="DIAGNOSTICO -- LA RESOLUCION, observada y no prometida: `n_mismo_dir_k` = cuantos de los 32 "
                     "estimulos caen en LAS k DIRECCIONES del mensaje (con sufijo OFF es `n_mismo_bin_k`, 12-16 "
                     "medido en el bloque 5). Prediccion estructural: con sufijo, 1-3 de 32"),
    'D2': dict(frase="DIAGNOSTICO ESTRUCTURAL (T = 0, sin simular, preregistro 5.4): de las 66 celdas, en cuantas "
                     "NO se distingue el referente del patron de BAR-T / BAR-H / VALOR, CON y SIN sufijo, y lo "
                     "mismo restringido a las 36 celdas que solo usan pixeles de FORMA"),
    'D3': dict(frase="DIAGNOSTICO -- DONDE ESTA LA VARIANTE si R3 cae (preregistro 6.3): `fam1` (via rapida), "
                     "`mem_cobertura` (cuantas subcasillas de la ganadora se conocen) y `wv` (el peso LINEAL "
                     "sobre los 3 pixeles de variante). No decide ninguna prediccion; dice que se mide despues"),
}


# ---------------------------------------------------------------- diagnostico estructural (T = 0, no simula)
def dir_fuera(par, P, mv, nvar=NVAR, D=12):
    """La direccion local REIMPLEMENTADA FUERA del organismo (el arnes la compara contra la de dentro)."""
    b = int(P[par[0]]) * 2 + int(P[par[1]])
    if not mv:
        return b
    s = 0
    for q in range(D - nvar, D):
        s = s * 2 + int(P[q])
    return b * (1 << nvar) + s


def estructura_v(fam_seed, D=12, n_var=NVAR):
    """Cuantas de las 66 celdas NO distinguen el referente de cada barajado, CON y SIN sufijo. NO simula."""
    Q = PATS(fam_seed)
    forma = [c for c in range(len(PARES12)) if max(PARES12[c]) < D - n_var]
    X = Q[XNEG]
    out = B5R.estructura_k(fam_seed, D, n_var)          # el calculo del bloque 5, sin sufijo, tal cual
    out['n_var_px'] = list(range(D - n_var, D))
    for nom, otro in (('BAR_T', BAR['neg']['TK']), ('BAR_H', BAR['neg']['H']), ('VALOR', [0.0] * D)):
        P = Q[otro] if isinstance(otro, str) else otro
        for mv in (0, 1):
            col = [c for c in range(len(PARES12)) if dir_fuera(PARES12[c], X, mv) == dir_fuera(PARES12[c], P, mv)]
            out[f'{nom}_v{mv}'] = round(len(col) / len(PARES12), 4)
            out[f'{nom}_v{mv}_forma'] = round(len([c for c in col if c in forma]) / max(len(forma), 1), 4)
        # en que pixeles difieren de verdad el referente y este barajado (el hecho del preregistro 0)
        out[nom + '_px_dif'] = [i for i in range(D) if int(X[i]) != int(P[i])]
    # piso estructural de la interseccion si TODAS las k ganadoras usan solo pixeles de forma, con y sin sufijo
    for mv in (0, 1):
        out['piso_forma_v%d' % mv] = len([n for n in Q if all(dir_fuera(PARES12[c], Q[n], mv)
                                                              == dir_fuera(PARES12[c], X, mv) for c in forma)])
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
    """El diagnostico del bloque 5 + lo que anade el bloque 6: el grupo por DIRECCION (bin + firma)."""
    d = B5R.mecanismo(r)
    md = r.get('canal_mismo_dir_k')
    d.update(memoria_variante=r.get('memoria_variante'), memoria_slots=r.get('memoria_slots'),
             mismo_dir_k=md, n_mismo_dir_k=(None if md is None else len(md)),
             # OJO al leerlo: `canal_mismo_dir_k` es el grupo del PATRON ENTREGADO, no el del referente. En el
             # brazo BAR-H el patron entregado ES la hermana, asi que `herm_en_dir` es trivialmente cierto; el
             # informativo ahi es `ref_en_dir`: si el mensaje de la hermana alcanza o no la direccion de T1v2.
             herm_en_dir=(None if md is None else bool(BAR['neg']['H'] in md)),
             ref_en_dir=(None if md is None else bool(XNEG in md)),
             cobertura=r.get('mem_cobertura'), vistas=r.get('mem_vistas'))
    return d


def resumen(brazo, seed, r, msg):
    b = BRAZOS[brazo]
    d = dict(tipo='R', brazo=brazo, base=b['base'], k=b['k'], mv=b['mv'], cel=b['cel'], dir='neg', seed=seed,
             mundo=r['mundo'], deaths=r['deaths'], celdas=r['celdas'], splits=r['splits'], fam_seed=r['fam_seed'],
             exc=r['exc'], cod0=r['cod0'], entregado=r['canal_entregado'], t_entrega=r['canal_t_entrega'],
             t_msg=r['canal_t_msg'], frac_regalo=r['frac_regalo'], renovados=r['renovados'],
             k_ganadoras=r['k_ganadoras'], memoria_variante=r['memoria_variante'],
             wv=r.get('w_var_med'), w_var=r.get('w_var'))
    d['B4'] = B4BR.lee_b4(r, msg['ref'])
    d['mem'] = mecanismo(r)
    d['prefijo'] = prefijo(r, r['canal_t_entrega'] if r['canal_t_entrega'] is not None else r['canal_t_msg'])
    d['prefijo_msg'] = prefijo(r, r['canal_t_msg'])
    d['bin0_igual'] = (None if r.get('canal_mismo_bin') is None else bool(msg['ref'] in r['canal_mismo_bin']))
    return d


# ---------------------------------------------------------------- tareas
NUEVAS_B6 = ('memoria_variante', 'memoria_slots', 'memoria_nvar', 'canal_mismo_dir_k')
NUEVAS_B5 = B5R.NUEVAS_B5


def emisor(seed, Ti, nk=30, ktop=3, nkmax=90):
    """El emisor del bloque 6 = b6 con mv=0 y k=1 = organismo_familias_b4b bit a bit. UN mensaje: la dir. (-)."""
    import organismo_familias_b6 as B6
    kw = B2R.resuelve(KW_E, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    r = B6.run(seed, T=Ti, fam_seed=seed, canal={'modo': 'emite'}, voraz=VORAZ, k_ganadoras=1,
               memoria_variante=0, **kw)
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
        import organismo_familias_b6 as B6
        etiq, ref, Tc = CASOS_ID[cual]
        Tc = Tc or Ti
        salta, debe = NUEVAS_B6, False
        if ref == 'B5':
            a, b = B5.run(seed, T=Tc, k_ganadoras=3), B6.run(seed, T=Tc, k_ganadoras=3)
        elif ref == 'B5F':
            k = dict(B2R.resuelve(KW_R, Tc))
            a = B5.run(seed, T=Tc, fam_seed=seed, k_ganadoras=3, **k)
            b = B6.run(seed, T=Tc, fam_seed=seed, k_ganadoras=3, **k)
        elif ref == 'B4B':
            k = dict(B2R.resuelve(KW_R, Tc))
            a, b = B4B.run(seed, T=Tc, fam_seed=seed, **k), B6.run(seed, T=Tc, fam_seed=seed, **k)
            salta = NUEVAS_B6 + NUEVAS_B5
        elif ref == 'V14':
            a, b = V14.run(seed, T=Tc), B6.run(seed, T=Tc)
            salta = NUEVAS_B6 + NUEVAS_B5 + ('voraz', 'par_herm', 'par_fijo')
        elif ref == 'V15FON':
            a, b = V15FON.run(seed, T=Tc), B6.run(seed, T=Tc, memoria_pares='relevo')
            salta = NUEVAS_B6 + NUEVAS_B5 + ('voraz', 'par_herm', 'par_fijo')
        elif ref == 'INERTE':
            k = dict(B2R.resuelve(KW_R, Tc)); k['memoria_pares'] = None
            a = B6.run(seed, T=Tc, fam_seed=seed, k_ganadoras=3, memoria_variante=0, **k)
            b = B6.run(seed, T=Tc, fam_seed=seed, k_ganadoras=3, memoria_variante=1, **k)
            salta = NUEVAS_B6
        elif ref == 'DIR':
            m = emisor(seed, 60000)['neg']
            if m is None:
                return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=False, debe_diferir=False,
                            ok=False, difieren=['sin mensaje (-)'], faltan=[])
            k = B2R.resuelve(KW_R, 60000)
            ok, Q, H = True, PATS(seed), BAR['neg']['H']
            for mv in (0, 1):
                r = B6.run(seed + SEM_R, T=60000, fam_seed=seed, canal=canal_de('CANAL-k3v%d' % mv, m, seed),
                           k_ganadoras=3, memoria_variante=mv, **k)
                esp = sorted(n for n in Q if all(dir_fuera(g, Q[n], mv) == dir_fuera(g, Q[XNEG], mv)
                                                 for g in r['canal_gan_k_post']))
                ok &= (r['memoria_slots'] == (4 << NVAR if mv else 4)
                       and len(r['mem_tabla'][0]) == r['memoria_slots']
                       and r['canal_mismo_dir_k'] == esp          # la direccion de dentro == la de fuera
                       and (XNEG in r['canal_mismo_dir_k'])       # el referente esta en su propia direccion
                       and ((H not in r['canal_mismo_dir_k']) if mv else True))   # CON sufijo, la hermana NO
            return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=ok, debe_diferir=False,
                        ok=bool(ok), difieren=[] if ok else ['direccion'], faltan=[])
        elif ref == 'LANZA':
            ok = True
            for mala in (2, -1, 0.5, '1', True):
                try:
                    B6.run(seed, T=Tc, memoria_variante=mala); ok = False
                except (ValueError, TypeError):
                    pass
                except Exception:
                    ok = False
            return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=ok, debe_diferir=False,
                        ok=bool(ok), difieren=[] if ok else ['no lanza'], faltan=[])
        elif ref == 'VDIF':
            k = dict(B2R.resuelve(KW_R, Tc))
            a = B6.run(seed, T=Tc, fam_seed=seed, k_ganadoras=3, memoria_variante=0, **k)
            b = B6.run(seed, T=Tc, fam_seed=seed, k_ganadoras=3, memoria_variante=1, **k)
            debe = True; salta = NUEVAS_B6
        else:                                   # CAN / HER: los dos controles de no-vacuidad del canal
            m = emisor(seed, Tc)['neg']
            if m is None:
                return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=False, debe_diferir=True,
                            ok=False, difieren=['sin mensaje (-)'], faltan=[])
            k = B2R.resuelve(KW_R, Tc)
            otro = 'CORTADO-k3v1' if ref == 'CAN' else 'BAR-H-k3v1'
            a = B6.run(seed + SEM_R, T=Tc, fam_seed=seed, canal=canal_de(otro, m, seed),
                       k_ganadoras=3, memoria_variante=1, **k)
            b = B6.run(seed + SEM_R, T=Tc, fam_seed=seed, canal=canal_de('CANAL-k3v1', m, seed),
                       k_ganadoras=3, memoria_variante=1, **k)
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
        d['estructura'] = estructura_v(seed)
        return dict(tipo='D', **d)
    if tipo == 'E':
        _, seed, Ti, nk, ktop, nkmax = args
        return dict(tipo='E', seed=seed, msgs=emisor(seed, Ti, nk, ktop, nkmax))
    _, brazo, seed, msg, Ti, nk, ktop, nkmax = args
    import organismo_familias_b6 as B6
    kw = B2R.resuelve(KW_R, Ti)
    kw.update(nk=nk, ktop=ktop, nkmax=nkmax)
    fsr = seed + SEM_OTRO if BRAZOS[brazo]['otro'] else seed
    r = B6.run(seed + SEM_R, T=Ti, fam_seed=fsr, canal=canal_de(brazo, msg, fsr),
               par_herm=BRAZOS[brazo]['par'], k_ganadoras=BRAZOS[brazo]['k'],
               memoria_variante=BRAZOS[brazo]['mv'], **kw)
    return resumen(brazo, seed, r, msg)


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_bloque6_sufijo.md')),
    script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_familias_b6.py')),
    instrumento=h16(os.path.join(AQUI, 'organismo_familias_b6.py')),
    arnes=h16(os.path.join(AQUI, 'identidad_familias_b6.py')),
    origen_b5=h16(os.path.join(AQUI, 'organismo_familias_b5.py')),
    origen_b4b=h16(os.path.join(AQUI, 'organismo_familias_b4b.py')),
    runner_bloque5=h16(os.path.join(AQUI, 'corre_familias_b5.py')),
    preregistro_bloque5=h16(os.path.join(AQUI, 'PREREGISTRO_bloque5_ganadoras.md')),
    escala_codigo_bloque0=h16(os.path.join(AQUI, 'escala_codigo.py')),
    externo_codex=h16(os.path.join(RAIZ, 'experimentos', 'externo_codex', 'cuelloA',
                                   'PREREGISTRO_cuelloA_sufijo_variante.md')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))


def guarda_origen():
    s, ok = SHAS(), True
    for k, esp in [('origen_organismo_v14', SHA_V14_ESPERADO), ('origen_b4b', SHA_B4B_ESPERADO),
                   ('origen_b5', SHA_B5_ESPERADO), ('escala_codigo_bloque0', SHA_ESCALA_ESPERADO)]:
        if s[k] != esp:
            log(f"*** ORIGEN CAMBIADO: {k} es {s[k]}, se esperaba {esp}. Reconstruir por anclas y repetir el arnes.")
            ok = False
    return ok


# ---------------------------------------------------------------- veredicto (la letra de la seccion 6)
def veredicto(res, msgs, SEEDS, diags, celdas=None):
    """TOLERA subconjuntos de celdas y brazos: nada se indexa a ciegas (ERR-54)."""
    celdas = [c for c in (celdas or CELDAS_ACTIVAS)
              if any(b in BRAZOS_ACTIVOS for b in ('CANAL-' + c, 'CORTADO-' + c))]
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    hay = lambda b: b in G and len(G[b]) > 0
    con_msg = [s for s in SEEDS if (msgs.get(s) or {}).get('neg')]
    # --- ERR-70: exclusion POR SEMILLA. Una semilla en la que el receptor YA habia visto el referente antes de
    #     la entrega sale del numerador Y del denominador de TODOS los brazos (mas estricto que bajar el umbral).
    mal_pi4 = set()
    for c in celdas:
        b = 'CORTADO-' + c
        for s in con_msg:
            r = G.get(b, {}).get(s)
            if r is None:
                continue
            tx = (r.get('B4') or {}).get('t_X')
            if tx is None or tx != r.get('t_entrega'):
                mal_pi4.add(s)
    val = [s for s in con_msg if s not in mal_pi4]
    bb = lambda b, c2: {s: (G.get(b, {}).get(s, {}).get('B4') or {}).get(c2) for s in val if s in G.get(b, {})}
    mm = lambda b, c2: {s: (G.get(b, {}).get(s, {}).get('mem') or {}).get(c2) for s in val if s in G.get(b, {})}
    gg = lambda b, c2: {s: G.get(b, {}).get(s, {}).get(c2) for s in val if s in G.get(b, {})}
    n1 = lambda d: sum(1 for v in d.values() if v == 1.0)
    n0 = lambda d: sum(1 for v in d.values() if v == 0.0)
    V = {'umbrales': UMBRALES, 'direccion': 'neg (ERR-53)', 'celdas': celdas, 'n_validas': len(val),
         'n_semillas': len(SEEDS), 'n_con_mensaje': len(con_msg),
         'sin_mensaje': [s for s in SEEDS if s not in con_msg],
         'excluidas_pi4_ERR70': sorted(mal_pi4)}
    V['alias'] = dict(pares_mediana=med([d['alias_pares'] for d in diags]),
                      semillas_con_alias=sum(d['alias_semilla'] for d in diags), n=len(diags),
                      U3_mediana=med([d['U3'] for d in diags]))
    es = [d['estructura'] for d in diags if d.get('estructura')]
    V['D2'] = dict(frase=UMBRALES['D2']['frase'], n=len(es))
    if es:
        for nom in ('BAR_T', 'BAR_H', 'VALOR'):
            for mv in (0, 1):
                V['D2'][f'{nom}_v{mv}'] = med([d[f'{nom}_v{mv}'] for d in es])
                V['D2'][f'{nom}_v{mv}_forma'] = med([d[f'{nom}_v{mv}_forma'] for d in es])
            V['D2'][nom + '_px_dif_fuera_de_variante'] = sum(
                1 for d in es if any(i < 12 - NVAR for i in d[nom + '_px_dif']))
        V['D2']['piso_forma_v0'] = med([d['piso_forma_v0'] for d in es])
        V['D2']['piso_forma_v1'] = med([d['piso_forma_v1'] for d in es])

    # --- puertas
    derR = B2R.resuelve(KW_R, T)['deriva']
    u = UMBRALES['PI2']
    V['PI2'] = dict(n_emite=len(con_msg), n=len(SEEDS), deriva_R=derR,
                    signo_ok=sum(1 for s in con_msg if msgs[s]['neg']['R'] > 0),
                    n_antes=sum(1 for s in con_msg if msgs[s]['neg']['t'] < 2 * derR),
                    t_msg_med=med([msgs[s]['neg']['t'] for s in con_msg]),
                    enc_med=med([msgs[s]['neg']['enc'] for s in con_msg]))
    V['PI2']['pasa'] = bool(V['PI2']['n_emite'] >= min(u['n_emite'], len(SEEDS))
                            and V['PI2']['signo_ok'] == len(con_msg) and V['PI2']['n_antes'] == len(con_msg))
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
    V['PI4'] = dict(n_utilizables=len(val), n=len(SEEDS), excluidas=sorted(mal_pi4),
                    n_excluidas=len(mal_pi4), max_excluidas=u['max_excluidas'])
    V['PI4']['pasa'] = bool(len(val) >= min(u['n_min'], len(SEEDS)) and len(mal_pi4) <= u['max_excluidas'])
    u = UMBRALES['PI5']
    V['PI5'] = {}
    for c in celdas:
        b = 'CORTADO-' + c
        if hay(b):
            V['PI5'][c] = dict(lenta=sum(1 for v in bb(b, 'fam1').values() if v == 0), n=len(val))
    V['PI5']['pasa'] = bool(V['PI5'] and all(v['lenta'] >= min(u['n_min'], len(val))
                                             for kk, v in V['PI5'].items() if kk != 'pasa'))

    # --- por brazo (`com` = mordio a la 1.a; la convencion del registro)
    V['brazos'] = {}
    for b in BRAZOS_ACTIVOS:
        if not hay(b):
            continue
        eX = bb(b, 'evX')
        V['brazos'][b] = dict(
            k=BRAZOS[b]['k'], mv=BRAZOS[b]['mv'], cel=BRAZOS[b]['cel'], base=BRAZOS[b]['base'],
            n=len([v for v in eX.values() if v is not None]), com_n=n0(eX), evX_n=n1(eX), okX_n=n1(bb(b, 'okX')),
            evU_med=med([v for v in bb(b, 'evU').values() if v is not None]),
            okU_med=med([v for v in bb(b, 'okU').values() if v is not None]),
            comH_med=med([v for v in bb(b, 'comH').values() if v is not None]),
            esp_med=med([v for v in bb(b, 'esp').values() if v is not None]),
            ret2_n=n1(bb(b, 'ret2')), ret3_n=n1(bb(b, 'ret3')), nunca_n=n1(bb(b, 'nunca')),
            lag_t_med=med([v for v in bb(b, 'lag_t').values() if v is not None]),
            lag_m_med=med([v for v in bb(b, 'lag_m').values() if v is not None]),
            fam1_n=sum(1 for v in bb(b, 'fam1').values() if v == 1),
            dist_n=n1(bb(b, 'dist')), okP_n=n1(bb(b, 'okP')),
            n_dist=len([v for v in bb(b, 'dist').values() if v is not None]),
            lag_par_med=med([v for v in bb(b, 'lag_par').values() if v is not None]),
            muertes_med=med([v for v in gg(b, 'deaths').values() if v is not None]),
            celdas_med=med([v for v in gg(b, 'celdas').values() if v is not None]),
            # D3: donde esta la variante si R3 cae (preregistro 6.3)
            cobertura_med=med([v for v in mm(b, 'cobertura').values() if v is not None]),
            vistas_med=med([v for v in mm(b, 'vistas').values() if v is not None]),
            k_var_post_med=med([v for v in mm(b, 'k_var_post').values() if v is not None]),
            n_mismo_bin_k_med=med([v for v in mm(b, 'n_mismo_bin_k').values() if v is not None]),
            n_mismo_dir_k_med=med([v for v in mm(b, 'n_mismo_dir_k').values() if v is not None]),
            herm_en_dir_n=sum(1 for v in mm(b, 'herm_en_dir').values() if v),
            ref_en_dir_n=sum(1 for v in mm(b, 'ref_en_dir').values() if v))
    Bz = V['brazos']
    com = lambda b: Bz[b]['com_n'] if b in Bz else None

    # --- R1..R6, por celda del factorial
    for nom in ('R1', 'R2', 'R3', 'R4', 'R5', 'R6'):
        V[nom] = {}
    for c in celdas:
        CA, CO = 'CANAL-' + c, 'CORTADO-' + c
        if not (hay(CA) and hay(CO)):
            continue
        u = UMBRALES['R1']
        dk, dc = bb(CA, 'evX'), bb(CO, 'evX')
        par = sum(1 for s in val if dk.get(s) is not None and dc.get(s) is not None and dk[s] < dc[s])
        V['R1'][c] = dict(canal=com(CA), cortado=com(CO), n=Bz[CA]['n'], n_menor=par,
                          A12=A12(list(dk.values()), list(dc.values())),
                          pasa=bool(com(CA) >= min(u['n_pasa'], Bz[CA]['n']) and com(CO) <= u['n_cort']
                                    and par >= min(u['n_par'], Bz[CA]['n'])))
        for nom, base in (('R2', 'BAR-T'), ('R3', 'BAR-H'), ('R4', 'VALOR')):
            b = '%s-%s' % (base, c)
            if not hay(b):
                continue
            u = UMBRALES[nom]
            V[nom][c] = dict(brazo=b, com=com(b), cortado=com(CO), canal=com(CA), n=Bz[b]['n'],
                             margen=u['margen'], exceso=com(b) - com(CO) - u['margen'],
                             n_mismo_dir_k=Bz[b]['n_mismo_dir_k_med'], herm_en_dir_n=Bz[b]['herm_en_dir_n'],
                             pasa=bool(com(b) <= com(CO) + u['margen']))
        u = UMBRALES['R5']
        PA, P0 = 'PAR-' + c, 'PAR0-' + c
        if hay(PA) and hay(P0):
            V['R5'][c] = dict(dist=Bz[PA]['dist_n'], n=Bz[PA]['n_dist'], dist_gemelo=Bz[P0]['dist_n'],
                              n_gemelo=Bz[P0]['n_dist'], okP=Bz[PA]['okP_n'], com=com(PA), com_gemelo=com(P0),
                              lag_par=Bz[PA]['lag_par_med'])
            V['R5'][c]['pasa'] = bool(Bz[PA]['dist_n'] >= min(u['n_pasa'], max(Bz[PA]['n_dist'], 1))
                                      and Bz[PA]['dist_n'] >= Bz[P0]['dist_n'] + u['sobre_gemelo'])
        u = UMBRALES['R6']
        ref1 = 'CANAL-k1v0'                      # el control de Occam: b4b bit a bit, en la MISMA serie
        if hay(ref1):
            m1, mk = Bz[ref1]['muertes_med'], Bz[CA]['muertes_med']
            o1, ok_ = Bz[ref1]['okU_med'], Bz[CA]['okU_med']
            V['R6'][c] = dict(muertes=mk, muertes_k1v0=m1, okU=ok_, okU_k1v0=o1, celdas=Bz[CA]['celdas_med'],
                              pasa=bool(mk is not None and m1 is not None and mk <= u['factor'] * max(m1, 1)
                                        and ok_ is not None and o1 is not None and ok_ >= o1 - u['caida_okU']))
    V['D1'] = {c: dict(n_mismo_bin_k=Bz['CANAL-' + c]['n_mismo_bin_k_med'],
                       n_mismo_dir_k=Bz['CANAL-' + c]['n_mismo_dir_k_med'],
                       k_var_post=Bz['CANAL-' + c]['k_var_post_med'],
                       cobertura=Bz['CANAL-' + c]['cobertura_med'])
               for c in celdas if hay('CANAL-' + c)}
    # D3: si R3 cae, DONDE esta la variante (preregistro 6.3). `ref_en_dir_n` = en cuantas semillas el mensaje
    # de la HERMANA cae en la direccion del REFERENTE: si es 0 y aun asi BAR-H muerde, el efecto NO viaja por la
    # tabla y hay que mirarlo en la lineal (`wv`) o en la via rapida (`fam1`).
    V['D3'] = {c: dict(fam1_n=Bz['BAR-H-' + c]['fam1_n'], cobertura=Bz['BAR-H-' + c]['cobertura_med'],
                       wv=med([v for v in gg('BAR-H-' + c, 'wv').values() if v is not None]),
                       ref_en_dir_n=Bz['BAR-H-' + c]['ref_en_dir_n'], n=Bz['BAR-H-' + c]['n'])
               for c in celdas if hay('BAR-H-' + c)}
    puertas = bool(V['PI2']['pasa'] and V['PI3']['pasa'] and V['PI4']['pasa'] and V['PI5']['pasa'])
    V['DECLARA'] = {c: bool(puertas and V['R1'].get(c, {}).get('pasa') and V['R2'].get(c, {}).get('pasa')
                            and V['R3'].get(c, {}).get('pasa') and V['R4'].get(c, {}).get('pasa'))
                    for c in celdas}
    co = UMBRALES['O6']['celda']
    V['O6'] = dict(frase=UMBRALES['O6']['frase'], celda=co, puertas=puertas,
                   R3=V['R3'].get(co, {}).get('pasa'), R1=V['R1'].get(co, {}).get('pasa'),
                   R2=V['R2'].get(co, {}).get('pasa'), R5=V['R5'].get(co, {}).get('pasa'),
                   BAR_H=V['R3'].get(co, {}).get('com'), CORTADO=V['R3'].get(co, {}).get('cortado'),
                   CANAL=V['R1'].get(co, {}).get('canal'))
    V['O6']['pasa'] = bool(puertas and V['O6']['R1'] and V['O6']['R2'] and V['O6']['R3'] and V['O6']['R5'])
    return V


def frase_final(V):
    for g in ('PI2', 'PI3', 'PI4', 'PI5'):
        if not V.get(g, {}).get('pasa'):
            return f"{g} CAE -- es el INSTRUMENTO o el montaje. Nada se declara (preregistro 5.2)."
    s = ("DIRECCION (-) SOLA (ERR-53). `com` = comio a la 1.a exposicion de la vida al referente. "
         f"Utilizables {V['n_validas']}/{V['n_semillas']} "
         f"(sin mensaje {V['sin_mensaje']}, excluidas por ERR-70 {V['excluidas_pi4_ERR70']}). ")
    for c in V['celdas']:
        R = lambda n: V.get(n, {}).get(c, {})
        s += (f"[{c}] CANAL {R('R1').get('canal')}/{R('R1').get('n')} contra CORTADO {R('R1').get('cortado')} -> "
              f"R1 {'pasa' if R('R1').get('pasa') else 'CAE'}; BAR-H {R('R3').get('com')} -> R3 "
              f"{'pasa' if R('R3').get('pasa') else 'CAE'}; BAR-T {R('R2').get('com')} -> R2 "
              f"{'pasa' if R('R2').get('pasa') else 'CAE'}; VALOR {R('R4').get('com')} -> R4 "
              f"{'pasa' if R('R4').get('pasa') else 'CAE'}; PAR dist {R('R5').get('dist')}/{R('R5').get('n')} "
              f"(gemelo {R('R5').get('dist_gemelo')}) -> R5 {'pasa' if R('R5').get('pasa') else 'CAE'}; coste R6 "
              f"{'pasa' if R('R6').get('pasa') else 'CAE'}; comparten LAS k DIRECCIONES "
              f"{V['D1'].get(c, {}).get('n_mismo_dir_k')}/32 (por BIN "
              f"{V['D1'].get(c, {}).get('n_mismo_bin_k')}/32). ")
    dec = [c for c in V['celdas'] if V['DECLARA'].get(c)]
    s += ("DECLARA (R1-R4 con todas las puertas) en " + str(dec) if dec else
          "NINGUNA celda cumple R1-R4: no se declara nada")
    s += (f". OBJETIVO O-6 (k3v1): {'PASA' if V['O6']['pasa'] else 'NO PASA'} "
          f"(BAR-H {V['O6']['BAR_H']} contra CORTADO {V['O6']['CORTADO']} + 5, CANAL {V['O6']['CANAL']}). "
          f"Piso estructural de la interseccion si el top-k es todo de FORMA: sin sufijo "
          f"{V['D2'].get('piso_forma_v0')} de 32, con sufijo {V['D2'].get('piso_forma_v1')} de 32. "
          f"20 semillas no cierran nada: replica en el rango siguiente (regla 12).")
    return s


# ---------------------------------------------------------------- humo (UN proceso, sin Pool, regla 3)
def humo(nk, ktop, nkmax, Tb, brazos):
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_b6_humo_{stamp}.log'), 'w',
                        encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log("HUMO del creador del bloque 6 (SUFIJO DE VARIANTE), UN proceso, sin Pool (regla 3). "
        f"celdas {sorted({BRAZOS[b]['cel'] for b in brazos})}.")
    log("PREREGISTRO_bloque6_sufijo.md (E-8; completa el cuello A del creador externo Codex).")
    log("Semillas 1-2: NINGUNA de las 721-760 del bloque queda expuesta.")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    log(f"    origenes verificados -> {'OK' if guarda_origen() else 'FALLA'}")
    sem = [1, 2]

    log("1/4 IDENTIDAD (subconjunto; el arnes completo, 59/59, va en identidad_familias_b6.py).")
    ident = []
    for cual in CASOS_ID:
        for s in sem:
            ident.append(tarea(('ID', cual, s, 6000)))
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {CASOS_ID[cual][0]:70s} {sum(r['ok'] for r in g)}/{len(g)}"
            + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']}"))
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)}")

    log("2/4 DIAGNOSTICO ESTRUCTURAL (antes de simular, T = 0): alias, U3 y la resolucion CON y SIN sufijo.")
    diags = []
    for s in sem:
        d = CF.diagnostico(s, nk, ktop, BASE)
        d.pop('cod'); d['estructura'] = estructura_v(s)
        diags.append(dict(tipo='D', **d))
        e = d['estructura']
        log(f"    semilla {s}: alias_pares {d['alias_pares']:.5f}  U3 {d['U3']}  |  celdas que NO distinguen: "
            f"BAR-H {e['BAR_H_v0']} -> {e['BAR_H_v1']} (con sufijo), BAR-T {e['BAR_T_v0']} -> {e['BAR_T_v1']}, "
            f"VALOR {e['VALOR_v0']} -> {e['VALOR_v1']}")
        log(f"                 piso de forma {e['piso_forma_v0']}/32 -> {e['piso_forma_v1']}/32 con sufijo  |  "
            f"px en que difieren referente y hermana: {e['BAR_H_px_dif']} (variante = {e['n_var_px']})")

    log(f"3/4 EMISORES (mv = 0, k = 1 = b4b bit a bit): {len(sem)} corridas de {Tb} pasos.")
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
                log(f"    {b:14s} s{s}  SIN MENSAJE: excluida (P-I2)"); continue
            t1 = time.time(); r = tarea(('R', b, s, m, Tb, nk, ktop, nkmax)); dt = time.time() - t1
            res.append(r); t_b[b] = round(t_b.get(b, 0.0) + dt, 2)
            B, M = r['B4'], r['mem']
            log(f"    {b:14s} s{s} {dt:5.1f}s  entrega t={r['t_entrega']}  {B['ref']} es {B['val_ref']}  "
                f"comio {1-int(B['evX'] or 0)} (okX {B['okX']}, via {'RAPIDA' if B['fam1'] else 'lenta'})  "
                f"dist {B['dist']}  evU {B['evU']} okU {B['okU']}  ret2/3 {B['ret2']}/{B['ret3']}  "
                f"muertes {r['deaths']}")
            log(f"                   MECANISMO k={r['k_ganadoras']} sufijo={r['memoria_variante']} "
                f"({M['memoria_slots']} subcasillas)  ganadoras {M['gan_k_post']}  con px variable "
                f"{M['k_var_post']}/{r['k_ganadoras']}  comparten LAS k DIRECCIONES {M['n_mismo_dir_k']}/32 "
                f"(por BIN {M['n_mismo_bin_k']}/32)  hermana dentro: {M['herm_en_dir']}  cobertura "
                f"{M['cobertura']}/{M['memoria_slots']}  lag {B['lag_t']} pasos / {B['lag_m']} mordidas")
    for c in sorted({BRAZOS[b]['cel'] for b in brazos}):
        pe = {r['brazo']: r['prefijo'] for r in res
              if r['seed'] == sem[0] and r['brazo'] in ('CANAL-' + c, 'CORTADO-' + c)}
        if len(pe) == 2:
            log(f"  GEMELO (P-I3) semilla {sem[0]}, CANAL-{c}/CORTADO-{c}: {list(pe.values())} -> "
                f"{'IDENTICOS' if len(set(pe.values())) == 1 else '*** DIFIEREN'}")
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

    dj = os.path.join(RAIZ, 'datos', f'familias_b6_humo_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_brazo=Tb, semillas=sem,
                                 T_bloque=T, nk=nk, ktop=ktop, nkmax=nkmax, ks=list(KS), mvs=list(MVS),
                                 celdas=CELDAS, brazos=N(BRAZOS), umbrales=UMBRALES, mundo=N(MUNDO),
                                 kw_E=N(KW_E), kw_R=N(KW_R), shas=SHAS(), segundos_por_brazo=t_b,
                                 cruce_cod0_ok=(not mal), python=platform.python_version(), numpy=np.__version__),
                       identidades=ident, diagnostico=diags, mensajes=N(msgs), brazos=res), f,
                  ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    CF._log['f'].close()


# ---------------------------------------------------------------- principal
if __name__ == '__main__':
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    nk, ktop, nkmax = arg('--nk', 30), arg('--k', 3), arg('--nkmax', 90)
    if '--celdas' in sys.argv:
        CELDAS_ACTIVAS = [c.strip() for c in sys.argv[sys.argv.index('--celdas') + 1].split(',') if c.strip()]
        malas = [c for c in CELDAS_ACTIVAS if c not in CELDAS]
        if malas:
            raise SystemExit(f"--celdas: desconocida(s) {malas}. Validas: {CELDAS}")
        BRAZOS_ACTIVOS = [b for b in ORDEN if BRAZOS[b]['cel'] in CELDAS_ACTIVAS]
    if '--brazos' in sys.argv:
        BRAZOS_ACTIVOS = [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_ACTIVOS if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--brazos: desconocido(s) {malos}. Validos: {ORDEN}")
        for b in list(BRAZOS_ACTIVOS):
            g = gemelo_de(b)
            if g not in BRAZOS_ACTIVOS:
                raise SystemExit(f"--brazos: {g} es obligatorio (es el GEMELO de {b}).")
        CELDAS_ACTIVAS = sorted({BRAZOS[b]['cel'] for b in BRAZOS_ACTIVOS})
    if '--humo' in sys.argv:
        bh = BRAZOS_ACTIVOS if ('--brazos' in sys.argv or '--celdas' in sys.argv) else BRAZOS_HUMO
        humo(nk, ktop, nkmax, arg('--T', T_HUMO), bh); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    T = arg('--T', T)
    desde = arg('--desde', DESDE)
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CF._log['f'] = open(os.path.join(RAIZ, 'datos', f'familias_b6_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'),
                        'w', encoding='utf-8', newline='\n')
    CF._log['t0'] = time.time()
    log(f"ARRANQUE BLOQUE 6 (SUFIJO DE VARIANTE; E-8): celdas {CELDAS_ACTIVAS}, {len(BRAZOS_ACTIVOS)} brazos, "
        f"semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log("El mundo, el canal y el emisor son los del bloque 4b/5, sin tocar (el emisor es mv=0, k=1 = b4b bit a "
        "bit). Lo unico nuevo es DONDE escribe y lee cada celda de la tabla del RECEPTOR.")
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
    log(f"REGLA 11 - procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V, res = {}, []
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('ID', c, s, T_ID) for c in CASOS_ID for s in SEMILLAS_ID]
        log(f"ETAPA 1/4 - IDENTIDAD ({len(CASOS_ID)} casos x {len(SEMILLAS_ID)} = {len(ctrl)}). "
            f"(K), (C) y (H) DEBEN fallar: sin ellos la etapa pasa por vacuidad.")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CASOS_ID[cual][0]:70s} {sum(r['ok'] for r in g)}/{len(g)}"
                + ("" if all(r['ok'] for r in g) else f"   difieren {g[0]['difieren']} faltan {g[0]['faltan']}"))
            # ERR-64b: los controles que DEBEN diferir prueban no-vacuidad con >= 2 de 3 semillas
            V[f'ID_{cual}'] = (sum(r['ok'] for r in g) >= 2) if (g and g[0].get('debe_diferir')) else all(r['ok'] for r in g)
        V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CASOS_ID))
        log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
        if not V['G_IDENTIDAD']:
            log("*** GUARDA DE IDENTIDAD FALLIDA. Se para (P-I1).")
            sys.exit(1)

        log(f"ETAPA 2/4 - DIAGNOSTICO ESTRUCTURAL, ANTES de simular ({len(SEEDS)} semillas, T = 0).")
        diags = pool.map(tarea, [('D', s, nk, ktop) for s in SEEDS], chunksize=1)
        log(f"    alias por par mediana {med([d['alias_pares'] for d in diags])}  U3 mediana "
            f"{med([d['U3'] for d in diags])}")
        log(f"    celdas de las 66 que NO distinguen el referente, SIN sufijo -> CON sufijo: BAR-H "
            f"{med([d['estructura']['BAR_H_v0'] for d in diags])} -> "
            f"{med([d['estructura']['BAR_H_v1'] for d in diags])}; BAR-T "
            f"{med([d['estructura']['BAR_T_v0'] for d in diags])} -> "
            f"{med([d['estructura']['BAR_T_v1'] for d in diags])}; piso de forma "
            f"{med([d['estructura']['piso_forma_v0'] for d in diags])}/32 -> "
            f"{med([d['estructura']['piso_forma_v1'] for d in diags])}/32")
        log(f"    semillas en que referente y hermana difieren en ALGUN pixel de FORMA (0-8): "
            f"{sum(1 for d in diags if any(i < 12 - NVAR for i in d['estructura']['BAR_H_px_dif']))}/{len(diags)} "
            f"(si no es 0, el sufijo de 3 px no puede separarlas del todo)")

        log(f"ETAPA 3/4 - EMISORES ({len(SEEDS)} corridas de {T} pasos; mv = 0, k = 1 = b4b bit a bit).")
        em = pool.map(tarea, [('E', s, T, nk, ktop, nkmax) for s in SEEDS], chunksize=1)
        msgs = {d['seed']: d['msgs'] for d in em}
        sin = [s for s in SEEDS if not (msgs.get(s) or {}).get('neg')]
        log(f"    (neg) emiten {len(SEEDS)-len(sin)}/{len(SEEDS)}; sin mensaje (excluidas, P-I2): {sin}; "
            f"t_msg mediana {med([m['neg']['t'] for m in msgs.values() if m.get('neg')])}")

        tr = [('R', b, s, msgs[s]['neg'], T, nk, ktop, nkmax) for b in BRAZOS_ACTIVOS for s in SEEDS
              if (msgs.get(s) or {}).get('neg')]
        log(f"ETAPA 4/4 - RECEPTORES: {len(tr)} corridas de {T} pasos ({len(BRAZOS_ACTIVOS)} brazos)...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    # ---- ERR-54: los datos CRUDOS se guardan ANTES del analisis
    crudo = os.path.join(RAIZ, 'datos', f'familias_b6_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}_crudo.json')
    with open(crudo, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='crudo', T=T, semillas=SEEDS,
                                 nk=nk, ktop=ktop, nkmax=nkmax, ks=list(KS), mvs=list(MVS), celdas=CELDAS_ACTIVAS,
                                 brazos=N(BRAZOS), umbrales=UMBRALES, mundo=N(MUNDO), kw_E=N(KW_E), kw_R=N(KW_R),
                                 shas=SHAS(), python=platform.python_version(), numpy=np.__version__),
                       identidades=rc, diagnostico=diags, mensajes=N(msgs), brazos=res), f,
                  ensure_ascii=False, default=str)
    log(f"CRUDO -> {os.path.basename(crudo)}  sha256_16 = {h16(crudo)}  (ERR-54: guardado ANTES del analisis)")

    try:
        V.update(veredicto(res, msgs, SEEDS, diags))
        log()
        log(frase_final(V))
    except Exception as e:
        log(f"*** EL ANALISIS FALLO ({type(e).__name__}: {e}). El CRUDO ya esta en disco (ERR-54): el veredicto "
            f"se calcula aparte sobre {os.path.basename(crudo)}.")
        V['analisis_error'] = f"{type(e).__name__}: {e}"

    dj = os.path.join(RAIZ, 'datos', f'familias_b6_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    with open(dj, 'w', encoding='utf-8') as f:
        json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='serie', T=T, semillas=SEEDS,
                                 nk=nk, ktop=ktop, nkmax=nkmax, ks=list(KS), mvs=list(MVS), celdas=CELDAS_ACTIVAS,
                                 brazos=N(BRAZOS), umbrales=UMBRALES, mundo=N(MUNDO), kw_E=N(KW_E), kw_R=N(KW_R),
                                 shas=SHAS(), crudo=os.path.basename(crudo),
                                 python=platform.python_version(), numpy=np.__version__),
                       veredicto=N(V), identidades=rc, diagnostico=diags, mensajes=N(msgs), brazos=res), f,
                  ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    CF._log['f'].close()
