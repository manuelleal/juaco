"""H-1 — R0 SIN EL REGALO: ¿SOSTIENE ESTE MUNDO UN LINAJE MORTAL? (mundo vivo, linea F; sala 4 §B E-1 y §C H-1)

MISION: llegar a la AGI por este camino — un organismo minimo con reglas locales (sin retropropagacion) que aprende,
sobrevive, se reproduce y EVOLUCIONA. Hoy: que la muerte mate de verdad, para que el linaje signifique algo.

Ejecuta PREREGISTRO_h1_muerte.md (escrito ANTES de correr; su sha va en el meta). Instrumento organismo_vivo_h1.py
(por anclas desde organismo_vivo_rep2.py 96feb4918dc5d694, que aqui SOLO SE LEE). Reutiliza corre_vivo_rep2.py y
corre_vivo_rep.py (brazos, MED, resumen, A12, medianas, cuartiles, alias) SIN copiarlos.

    python experimentos/nivel11_mundo_vivo/corre_vivo_h1.py [--desde 701] [--T 100000] [--brazos ...]
    python experimentos/nivel11_mundo_vivo/corre_vivo_h1.py --humo     (UN proceso, sin Pool, 4 corridas: el disenador)

Etapas con Pool (las corre el COORDINADOR, reglas 3 y 11):
  1/2 IDENTIDAD interna, 5 casos x 3 semillas (T=20000): (A) apagada == organismo_vivo_rep2 · (B) cadena == organismo_v14 ·
      (C) h1=1 con muerte_real=0: claves viejas == rep2 · (D) MUERE-NADA != RENACE (DEBE fallar) · (E) MUERE-M1 != MUERE-NADA
      (DEBE fallar: si la herencia es inerte, el instrumento esta roto). Si no es 15/15, ABORTA.
  2/2 principal: 10 brazos + 10 de RAMPA x 20 semillas (701-720; replica 721-740 con --desde 721).

BRAZOS PRINCIPALES (5 modos x 2 cuerpos): RENACE (control, como hoy: la muerte NO mata) · MUERE-NADA · MUERE-M1
(hereda el VECTOR Wps/Wns) · MUERE-M1+PARES (el vector Y el TOKEN) · MUERE-BARAJA (el vector con los pixeles
permutados: la prediccion que decide) x {VIVO, CUELLO_MIN}.
RAMPA (solo para la clausula de cierre de H-1, sobre CUELLO_MIN, NADA y M1): las cuatro perillas que H-1 nombra —
dote 0.3 / dote 0.9 / rep_X 250 / nobj 8 / costo 0.0005. LA RAMPA ES BUSQUEDA, NO EVIDENCIA (§6 del preregistro).

Vocabulario (regla 6): "la muerte borra la memoria del individuo", "descendientes por vida (R0)", "crecimiento neto
del linaje", "fundacion del mundo" (linaje extinto), "el vector", "el token". NO se dice "evoluciona", "selecciona",
"especie", "quiere", "generacion" (no hay solapamiento de cuerpos: el linaje es en serie, un cuerpo a la vez).

ERR-54: los datos CRUDOS se guardan ANTES de analizar nada.
"""
import sys, os, json, time, platform, subprocess, statistics as st
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import mini_vivo as MV
import corre_vivo_rep as C1        # BRAZOS, MED, resumen, A12, med, q, ge, le, h16, N, razon, alias_de: NO se copian
import corre_vivo_rep2 as C2       # MED2, BRAZOS del bloque 2, resumen2: NO se copian

T = 100000
T_ID = 20000
N_PARALELO = 14
N_SEM = 20
DESDE = 701
SEMILLAS_ID = [1, 2, 3]
DOTE = 0.6           # exactamente el tamano del regalo de hoy (E=Ag=0.6 al renacer): lo unico que cambia es QUIEN LO PAGA
SHA_ESPERADOS = dict(v14='feefc88b1fd8d434', vivo='20c0961c79de8825', rep='aa823d56c2d4213c', rep2='96feb4918dc5d694')

MED_H1 = dict(C2.MED2, h1=1)   # reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0, rep_coste=0, rep2=1, rep2_regalo=600, h1=1
CUERPO = {'VIVO': 'VIVO', 'CM': 'CUELLO_MIN'}
MODOS = {'RENACE': dict(muerte_real=0),
         'NADA':   dict(muerte_real=1, hereda='nada',     dote=DOTE),
         'M1':     dict(muerte_real=1, hereda='M1',       dote=DOTE),
         'PARES':  dict(muerte_real=1, hereda='M1+pares', dote=DOTE),
         'BARAJA': dict(muerte_real=1, hereda='baraja',   dote=DOTE)}
RAMPA_PTS = {'D03': dict(dote=0.3), 'D09': dict(dote=0.9), 'X250': dict(rep_X=250), 'N8': dict(nobj=8),
             'C05': dict(costo=0.0005, costo_a=0.0005, rep2_regalo=1200)}   # el regalo dura A_muerte/costo pasos: con costo 0.0005 son 1200

BRAZOS = {f'{m}_{c}': dict(C1.BRAZOS[CUERPO[c]]) | MED_H1 | MODOS[m] for m in MODOS for c in CUERPO}
BRAZOS.update({f'R{p}_{m}': dict(C1.BRAZOS['CUELLO_MIN']) | MED_H1 | MODOS[m] | RAMPA_PTS[p]
               for p in RAMPA_PTS for m in ('NADA', 'M1')})
ORDEN = [f'{m}_{c}' for m in MODOS for c in ('CM', 'VIVO')] + [f'R{p}_{m}' for p in RAMPA_PTS for m in ('NADA', 'M1')]
PRINCIPALES = [f'{m}_{c}' for m in MODOS for c in ('CM', 'VIVO')]
RAMPA = [b for b in ORDEN if b.startswith('R') and b not in PRINCIPALES]
MUERE_CM = ['NADA_CM', 'M1_CM', 'PARES_CM', 'BARAJA_CM']
BRAZOS_ACTIVOS = list(ORDEN)
NUEVAS_H1 = {'muerte_real', 'hereda', 'dote', 'nacimientos', 'fundadores', 'desc_fund', 'desc_por_vida', 'vidas_h1',
             'origen_cuerpo', 'suma_vidas', 'cola_final', 'cola_desborde', 't_fund', 'baraja_identidad', 'h1'}
CASOS_ID = {   # (etiqueta, referencia, kw referencia, kw h1, debe_diferir, claves que se quitan)
    'A': ("(A) apagada (muerte_real=0, h1=0) == organismo_vivo_rep2 CUELLO_MIN", 'rep2', C2.BRAZOS['CUELLO_MIN'], C2.BRAZOS['CUELLO_MIN'], False, ()),
    'B': ("(B) cadena: h1(vivo=0, n_nec=1) == organismo_v14 (TRONCO)", 'v14', dict(), dict(vivo=0, n_nec=1), False, ()),
    'C': ("(C) h1=1 con muerte_real=0: claves viejas == organismo_vivo_rep2", 'rep2', C2.BRAZOS['VIVO'], BRAZOS['RENACE_VIVO'], False, NUEVAS_H1),
    'D': ("(D) MUERE-NADA != RENACE (DEBE fallar)", 'rep2', C2.BRAZOS['CUELLO_MIN'], BRAZOS['NADA_CM'], True, NUEVAS_H1),
    'E': ("(E) MUERE-M1 != MUERE-NADA (DEBE fallar: si la herencia es inerte, el instrumento esta roto)", 'h1', BRAZOS['NADA_CM'], BRAZOS['M1_CM'], True, ()),
}

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (ERR-31)
UMBRALES = {
    'H1-1': dict(frase="ANCLA DEL CONTROL (RENACE tiene que reproducir el bloque 2): mediana R0 RENACE_CM en [0.70, 1.40] y RENACE_VIVO en "
                       "[0.12, 0.32]; mediana r RENACE_CM en [-50, +25] y RENACE_VIVO en [-115, -45]; frac_regalo RENACE_CM en [0.20, 0.55]. "
                       "Si cae, el instrumento se movio y NO SE LEE NADA MAS",
                 r0_cm=(0.70, 1.40), r0_vivo=(0.12, 0.32), r_cm=(-50, 25), r_vivo=(-115, -45), reg_cm=(0.20, 0.55)),
    'H1-2': dict(frase="LA MUERTE MATA: mediana R0(NADA_CM) <= 0.35 y R0(NADA_VIVO) <= 0.20; A12(RENACE_CM > NADA_CM) >= 0.90 y "
                       "A12(RENACE_VIVO > NADA_VIVO) >= 0.85; vida mediana NADA_CM <= 0.60 x RENACE_CM. "
                       "REFUTA: R0(NADA_CM) >= 0.90 -> borrar la memoria no cambia el linaje: el regalo era energia, no memoria",
                 r0_cm=0.35, r0_vivo=0.20, a12_cm=0.90, a12_vivo=0.85, f_vida=0.60, refuta=0.90),
    'H1-3': dict(frase="LA HERENCIA PAGA: R0(M1_CM) >= 1.30 x R0(NADA_CM) y A12(M1_CM > NADA_CM) >= 0.80 (esto DECIDE, ERR-61); el conteo "
                       "pareado k/20 >= 15 se reporta AL LADO y no decide. REFUTA: A12 <= 0.60 -> heredar el vector de valores no compra nada",
                 razon=1.30, a12=0.80, pareado=15, refuta=0.60),
    'H1-4': dict(frase="LA PREDICCION QUE DECIDE — BARAJA ~ NADA: |R0(BARAJA_CM) - R0(NADA_CM)| <= 0.10 y 0.35 <= A12(BARAJA_CM > NADA_CM) "
                       "<= 0.65. REFUTA (a): BARAJA ~ M1 (A12(BARAJA > NADA) >= 0.80 y |R0(BARAJA) - R0(M1)| <= 0.10) -> lo heredable es la "
                       "MAGNITUD (una cautela), no el contenido: ERR y se dice. REFUTA (b): A12(BARAJA > NADA) <= 0.20 -> heredar valores en "
                       "los pixeles equivocados es PEOR que no heredar",
                 dif=0.10, a12_lo=0.35, a12_hi=0.65, ref_a=0.80, ref_b=0.20),
    'H1-5': dict(frase="¿EL VECTOR O EL TOKEN? (H-7): A12(PARES_CM > M1_CM) >= 0.65 y R0(PARES_CM) >= R0(M1_CM). Si A12 <= 0.50 -> el token "
                       "NO aporta sobre el vector: lo portable entre cuerpos es el VECTOR (las dos direcciones se declaran)",
                 a12=0.65, vector=0.50),
    'H1-6': dict(frase="CLAUSULA DE CIERRE DE H-1: algun brazo con muerte real (principal o rampa) alcanza mediana R0 >= 0.90 con mediana "
                       "fundadores <= 2 y con su NADA pareado por debajo de 1.0. Si NINGUNO lo alcanza: ERR-62 — este mundo NO SOSTIENE "
                       "LINAJES MORTALES con estas cuatro perillas, y la linea de evolucion no se corre hasta cambiar el MUNDO (no el umbral). "
                       "Si alguno lo alcanza, NO se declara aqui: la rampa es busqueda, no evidencia -> bloque nuevo con semillas nuevas",
                 r0=0.90, fund=2),
    'H1-7': dict(frase="SIN EL REGALO (obligatorio): frac_fund = desc_fund/descendientes, mediana <= 0.15 en los cuatro brazos MUERE_CM; "
                       "frac_regalo se reporta en los diez principales. REFUTA: frac_fund > 0.35 en algun MUERE -> el regalo del renacer "
                       "sigue financiando las ventanas y la medida no esta limpia",
                 max=0.15, refuta=0.35),
    'H1-8': dict(frase="SEGURIDAD Y CONTABILIDAD: coherencia contable 20/20 en los veinte brazos; cola_desborde 0 en 20/20; exposiciones[A] "
                       "NADA_CM >= 0.50 x RENACE_CM. xor01 se REPORTA sin puerta en los brazos MUERE (la tabla es de un MOSAICO de cuerpos, "
                       "no de un individuo: usarla de puerta seria vocabulario inflado)",
                 n_min=20, f_com=0.50),
}
HUMO = {'HH1': "r(RENACE_CM) > r(NADA_CM) en 2/2 (misma semilla)",
        'HH2': "R0(NADA_CM) < 1 en 2/2 y R0(RENACE_CM) > R0(NADA_CM) en 2/2",
        'HH3': "coherencia contable en 4/4 (nacimientos = muertes; suma(vidas_h1) = T; suma(desc_por_vida) = desc; fundaciones + 1 = origenes 0)",
        'HH4': "vida mediana NADA_CM < RENACE_CM en 2/2",
        'HH5': "fundadores(NADA_CM) >= 1 en 2/2 (el linaje se extingue al menos una vez)",
        'HH6': "(blanda) frac_fund(NADA_CM) <= 0.35 en 2/2"}

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


A12, med, q, ge, le, h16, N, razon = C1.A12, C1.med, C1.q, C1.ge, C1.le, C1.h16, C1.N, C1.razon


def dentro(x, iv):
    return bool(x is not None and iv[0] <= x <= iv[1])


# ---------------------------------------------------------------- medidas por corrida
def resumen_h1(brazo, seed, r, kw, Ti):
    o = C2.resumen2(brazo, seed, r, kw, Ti)
    v, org, d = r['vidas_h1'], r['origen_cuerpo'], r['desc_por_vida']
    vf = [x for x, y in zip(v, org) if y == 0]; vh = [x for x, y in zip(v, org) if y == 1]
    dh = [x for x, y in zip(d, org) if y == 1]
    coh = dict(nac=(r['nacimientos'] == (r['deaths'] if r['muerte_real'] else 0)),
               largos=(len(v) == len(org) == len(d) == r['deaths'] + 1),
               vidas=(sum(v) == Ti and r['suma_vidas'] + r['vida_final'] == Ti),
               desc=(sum(d) == r['descendientes']),
               fund=(r['fundadores'] + 1 == org.count(0) if r['muerte_real'] else r['fundadores'] == 0),
               topes=(r['desc_fund'] <= r['descendientes'] and r['cola_desborde'] >= 0))
    o.update(muerte_real=r['muerte_real'], hereda=r['hereda'], dote=r['dote'],
             R0=round(r['descendientes'] / len(d), 4), cuerpos=len(d),
             vida_med_h1=round(float(st.median(v)), 1), vida_q75_h1=q(v, 2), vida_max_h1=max(v),
             fundadores=r['fundadores'], heredados=r['nacimientos'] - r['fundadores'],
             desc_fund=r['desc_fund'], frac_fund=(round(r['desc_fund'] / r['descendientes'], 3) if r['descendientes'] else None),
             vida_med_fund=(round(float(st.median(vf)), 1) if vf else None),
             vida_med_her=(round(float(st.median(vh)), 1) if vh else None),
             R0_her=(round(sum(dh) / len(dh), 4) if dh else None),
             t_fund1=(r['t_fund'][0] if r['t_fund'] else None), cola_final=r['cola_final'], cola_desborde=r['cola_desborde'],
             baraja_identidad=r['baraja_identidad'], coherente=bool(all(coh.values())), coherencia=coh)
    return o


def tarea(args):
    tipo = args[0]
    if tipo == 'ID':
        _, cual, seed, Ti = args
        import organismo_v14 as V14, organismo_vivo_rep2 as V2, organismo_vivo_h1 as OH
        etiq, ref, kwa, kwb, debe, quitar = CASOS_ID[cual]
        a = {'v14': V14, 'rep2': V2, 'h1': OH}[ref].run(seed, T=Ti, **kwa)
        b = OH.run(seed, T=Ti, **kwb)
        bb = {k: v for k, v in b.items() if k not in quitar}
        dif = [k for k in a if k in bb and N(a[k]) != N(bb[k])]
        falta = [k for k in a if k not in bb]
        extra = [k for k in bb if k not in a]
        igual = not dif and not falta and not extra
        return dict(tipo='ID', cual=cual, etiqueta=etiq, seed=seed, identico=igual, debe_diferir=debe, ok=bool(igual != debe),
                    difieren=dif[:6], faltan=falta, extra=extra[:6])
    _, brazo, seed, Ti = args
    import organismo_vivo_h1 as OH
    kw = BRAZOS[brazo]
    return resumen_h1(brazo, seed, OH.run(seed, T=Ti, **kw), kw, Ti)


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_h1_muerte.md')), script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_vivo_h1.py')), instrumento=h16(os.path.join(AQUI, 'organismo_vivo_h1.py')),
    arnes=h16(os.path.join(AQUI, 'identidad_vivo_h1.py')), origen_organismo_vivo_rep2=h16(os.path.join(AQUI, 'organismo_vivo_rep2.py')),
    origen_organismo_vivo_rep=h16(os.path.join(AQUI, 'organismo_vivo_rep.py')), origen_organismo_vivo=h16(os.path.join(AQUI, 'organismo_vivo.py')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')), corre_vivo_rep2=h16(os.path.join(AQUI, 'corre_vivo_rep2.py')),
    corre_vivo_rep=h16(os.path.join(AQUI, 'corre_vivo_rep.py')), mini=h16(os.path.join(AQUI, 'mini_vivo.py')))


def guarda_origen():
    s = SHAS(); ok = True
    for k, esp in (('origen_organismo_v14', SHA_ESPERADOS['v14']), ('origen_organismo_vivo', SHA_ESPERADOS['vivo']),
                   ('origen_organismo_vivo_rep', SHA_ESPERADOS['rep']), ('origen_organismo_vivo_rep2', SHA_ESPERADOS['rep2'])):
        if s[k] != esp:
            log(f"*** ORIGEN CAMBIADO: {k} es {s[k]}, se esperaba {esp}. Reconstruir por anclas y repetir el arnes ANTES de correr."); ok = False
    return ok


def guarda_err38():
    """ERR-38: la entrada nueva se compara CAMPO A CAMPO con la del bloque anterior antes de correr. RENACE (muerte_real=0)
    tiene que ser, campo por campo, el brazo del bloque 2 mas las perillas de H-1 y nada mas."""
    ok = True
    for nuevo, viejo in (('RENACE_VIVO', 'VIVO'), ('RENACE_CM', 'CUELLO_MIN')):
        a = {k: v for k, v in BRAZOS[nuevo].items() if k not in ('h1', 'muerte_real', 'hereda', 'dote', 'cola_max')}
        b = dict(C2.BRAZOS[viejo])
        dif = {k: (b.get(k, '<falta>'), a.get(k, '<falta>')) for k in set(a) | set(b) if N(a.get(k)) != N(b.get(k))}
        log(f"    ERR-38 {nuevo:12s} vs bloque 2 {viejo:12s} -> {'IDENTICO campo a campo' if not dif else '*** DIFIERE ' + str(dif)}")
        ok &= not dif
    for b in MUERE_CM + [x for x in RAMPA]:
        kw = BRAZOS[b]
        if not (kw['muerte_real'] == 1 and 0 < kw['dote'] < kw['rep_umbral'] and kw['rep_coste'] == 0 and kw['h1'] == 1 and kw['rep2'] == 1):
            log(f"    *** ERR-38 {b}: perillas incoherentes {kw}"); ok = False
    return ok


# ---------------------------------------------------------------- veredicto (letra EXACTA del preregistro)
def veredicto(res, SEEDS, log=log):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in BRAZOS_ACTIVOS}
    alias = C1.alias_de(SEEDS)
    limpias = [s for s in SEEDS if s not in alias]
    V = {'umbrales': UMBRALES, 'alias': alias, 'limpias': limpias, 'completo': serie(G, SEEDS, "CONJUNTO COMPLETO", log)}
    if alias and len(limpias) >= 0.6 * len(SEEDS):
        V['limpias_veredicto'] = serie(G, limpias, f"SUBCONJUNTO LIMPIAS (sin {alias}; regla 10)", log)
    return V


def serie(G, S, etiqueta, log):
    v = lambda b, f: [f(G[b][s]) for s in S if s in G.get(b, {})]
    R0 = lambda b: v(b, lambda r: r['R0'])
    rr = lambda b: v(b, lambda r: r['r'])
    hay = lambda *bs: all(b in G and any(s in G[b] for s in S) for b in bs)
    log(f"--- {etiqueta}: semillas {S[0]}-{S[-1]} (n={len(S)}) ---")
    M = {}
    for b in BRAZOS_ACTIVOS:
        g = [G[b][s] for s in S if s in G.get(b, {})]
        if not g:
            continue
        M[b] = dict(n=len(g), R0=med(R0(b)), R0_q25=q(R0(b), 0), R0_q75=q(R0(b), 2), R0_her=med(v(b, lambda r: r['R0_her'])),
                    r=med(rr(b)), r_ge0=sum(x >= 0 for x in rr(b)), desc=med(v(b, lambda r: r['descendientes'])),
                    muertes=med(v(b, lambda r: r['deaths'])), cuerpos=med(v(b, lambda r: r['cuerpos'])),
                    vida=med(v(b, lambda r: r['vida_med_h1'])), vida_fund=med(v(b, lambda r: r['vida_med_fund'])),
                    vida_her=med(v(b, lambda r: r['vida_med_her'])), fundadores=med(v(b, lambda r: r['fundadores'])),
                    heredados=med(v(b, lambda r: r['heredados'])), frac_regalo=med(v(b, lambda r: r['frac_regalo'])),
                    frac_fund=med(v(b, lambda r: r['frac_fund'])), t_fund1=med(v(b, lambda r: r['t_fund1'])),
                    sac_sal=med(v(b, lambda r: r['sac_tasa']['D'])), xor01=med(v(b, lambda r: r['xor01'])),
                    coherentes=sum(v(b, lambda r: int(r['coherente']))), desborde=sum(v(b, lambda r: r['cola_desborde'])),
                    exposiciones={k: med(v(b, lambda r, k=k: r['exposiciones'][k])) for k in MV.EST})
        m = M[b]
        log(f"   {b:13s} n={m['n']:<3d} R0 {m['R0']} [q25 {m['R0_q25']}, q75 {m['R0_q75']}]  r {m['r']} (r>=0 en {m['r_ge0']})  desc {m['desc']}  "
            f"muertes {m['muertes']}  cuerpos {m['cuerpos']}  vida {m['vida']} (fund {m['vida_fund']} / her {m['vida_her']})")
        log(f"        fundaciones {m['fundadores']} (1.a en {m['t_fund1']})  heredados {m['heredados']} (R0_her {m['R0_her']})  regalo {m['frac_regalo']} / "
            f"fund {m['frac_fund']}  saciado sal {m['sac_sal']}  xor01 {m['xor01']} (se reporta)  coherentes {m['coherentes']}/{m['n']}  exposiciones {m['exposiciones']}")
    P = {'medianas': M}

    u = UMBRALES['H1-1']
    if hay('RENACE_CM', 'RENACE_VIVO'):
        d = dict(r0_cm=dentro(M['RENACE_CM']['R0'], u['r0_cm']), r0_vivo=dentro(M['RENACE_VIVO']['R0'], u['r0_vivo']),
                 r_cm=dentro(M['RENACE_CM']['r'], u['r_cm']), r_vivo=dentro(M['RENACE_VIVO']['r'], u['r_vivo']),
                 reg_cm=dentro(M['RENACE_CM']['frac_regalo'], u['reg_cm']))
        P['H1-1'] = dict(**d, valores=dict(R0_cm=M['RENACE_CM']['R0'], R0_vivo=M['RENACE_VIVO']['R0'], r_cm=M['RENACE_CM']['r'],
                                           r_vivo=M['RENACE_VIVO']['r'], regalo_cm=M['RENACE_CM']['frac_regalo']), pasa=bool(all(d.values())))
        log(f"   H1-1 {u['frase']}\n        -> R0 CM {M['RENACE_CM']['R0']} / VIVO {M['RENACE_VIVO']['R0']}; r {M['RENACE_CM']['r']} / {M['RENACE_VIVO']['r']}; "
            f"regalo {M['RENACE_CM']['frac_regalo']}  {'PASA (el control ancla)' if P['H1-1']['pasa'] else 'NO -> EL INSTRUMENTO SE MOVIO: no se lee nada mas'}")

    u = UMBRALES['H1-2']
    if hay('RENACE_CM', 'RENACE_VIVO', 'NADA_CM', 'NADA_VIVO'):
        a1, a2 = A12(R0('RENACE_CM'), R0('NADA_CM')), A12(R0('RENACE_VIVO'), R0('NADA_VIVO'))
        fv = razon(M['NADA_CM']['vida'], M['RENACE_CM']['vida'])
        P['H1-2'] = dict(R0_nada_cm=M['NADA_CM']['R0'], R0_nada_vivo=M['NADA_VIVO']['R0'], a12_cm=a1, a12_vivo=a2, f_vida=fv,
                         pasa=bool(le(M['NADA_CM']['R0'], u['r0_cm']) and le(M['NADA_VIVO']['R0'], u['r0_vivo']) and
                                   ge(a1, u['a12_cm']) and ge(a2, u['a12_vivo']) and le(fv, u['f_vida'])),
                         refutada=bool(ge(M['NADA_CM']['R0'], u['refuta'])))
        log(f"   H1-2 {u['frase']}\n        -> R0 NADA_CM {M['NADA_CM']['R0']}, NADA_VIVO {M['NADA_VIVO']['R0']}; A12 {a1} / {a2}; vida x{fv}  "
            f"{'PASA (la muerte mata)' if P['H1-2']['pasa'] else ('REFUTADA: borrar la memoria no cambia el linaje' if P['H1-2']['refutada'] else 'NO')}")

    u = UMBRALES['H1-3']
    if hay('M1_CM', 'NADA_CM'):
        a = A12(R0('M1_CM'), R0('NADA_CM')); rz = razon(M['M1_CM']['R0'], M['NADA_CM']['R0'])
        par = sum(1 for s in S if s in G['M1_CM'] and s in G['NADA_CM'] and G['M1_CM'][s]['R0'] > G['NADA_CM'][s]['R0'])
        P['H1-3'] = dict(a12=a, razon=rz, pareado=par, n=len(S), pasa=bool(ge(a, u['a12']) and ge(rz, u['razon'])), refutada=bool(le(a, u['refuta'])))
        log(f"   H1-3 {u['frase']}\n        -> A12 {a}; razon de medianas x{rz}; pareado {par}/{len(S)} (se reporta, no decide: ERR-61)  "
            f"{'PASA (heredar el vector compra vidas)' if P['H1-3']['pasa'] else ('REFUTADA: la herencia del vector no compra nada' if P['H1-3']['refutada'] else 'NO')}")

    u = UMBRALES['H1-4']
    if hay('BARAJA_CM', 'NADA_CM', 'M1_CM'):
        a = A12(R0('BARAJA_CM'), R0('NADA_CM')); dif = (None if M['BARAJA_CM']['R0'] is None else round(abs(M['BARAJA_CM']['R0'] - M['NADA_CM']['R0']), 4))
        dm = (None if M['BARAJA_CM']['R0'] is None else round(abs(M['BARAJA_CM']['R0'] - M['M1_CM']['R0']), 4))
        P['H1-4'] = dict(a12_baraja_nada=a, dif_nada=dif, dif_m1=dm,
                         pasa=bool(le(dif, u['dif']) and a is not None and u['a12_lo'] <= a <= u['a12_hi']),
                         refuta_a=bool(ge(a, u['ref_a']) and le(dm, u['dif'])), refuta_b=bool(le(a, u['ref_b'])))
        log(f"   H1-4 {u['frase']}\n        -> A12(BARAJA > NADA) {a}; |R0 BARAJA - NADA| {dif}; |R0 BARAJA - M1| {dm}  "
            + ('PASA: lo que se hereda es el CONTENIDO (la baraja lo destruye)' if P['H1-4']['pasa'] else
               ('REFUTA (a): lo heredable es la MAGNITUD, no el contenido' if P['H1-4']['refuta_a'] else
                ('REFUTA (b): heredar en los pixeles equivocados es PEOR que no heredar' if P['H1-4']['refuta_b'] else 'NO concluyente'))))

    u = UMBRALES['H1-5']
    if hay('PARES_CM', 'M1_CM'):
        a = A12(R0('PARES_CM'), R0('M1_CM'))
        P['H1-5'] = dict(a12=a, R0_pares=M['PARES_CM']['R0'], R0_m1=M['M1_CM']['R0'],
                         pasa=bool(ge(a, u['a12']) and ge(M['PARES_CM']['R0'], M['M1_CM']['R0'])), vector=bool(le(a, u['vector'])))
        log(f"   H1-5 {u['frase']}\n        -> A12(PARES > M1) {a}; R0 {M['PARES_CM']['R0']} contra {M['M1_CM']['R0']}  "
            + ('PASA: el TOKEN viaja y aporta' if P['H1-5']['pasa'] else
               ('lo portable entre cuerpos es el VECTOR (el token no aporta)' if P['H1-5']['vector'] else 'NO concluyente')))

    u = UMBRALES['H1-6']
    cand = [b for b in M if BRAZOS[b].get('muerte_real', 0) == 1 and ge(M[b]['R0'], u['r0']) and le(M[b]['fundadores'], u['fund'])]
    P['H1-6'] = dict(candidatos=cand, r0={b: M[b]['R0'] for b in M}, pasa=bool(cand))
    log(f"   H1-6 {u['frase']}\n        -> brazos con muerte real y R0 >= {u['r0']} y fundaciones <= {u['fund']}: {cand or 'NINGUNO'}  "
        + ('-> candidato a bloque nuevo con semillas nuevas (la rampa es busqueda, NO evidencia)' if cand else
           '-> ERR-62: ESTE MUNDO NO SOSTIENE LINAJES MORTALES con estas cuatro perillas'))

    u = UMBRALES['H1-7']
    d = {b: M[b]['frac_fund'] for b in MUERE_CM if b in M}
    if d:
        P['H1-7'] = dict(frac_fund=d, frac_regalo={b: M[b]['frac_regalo'] for b in PRINCIPALES if b in M},
                         pasa=bool(all(le(x, u['max']) for x in d.values())), refutada=bool(any(x is not None and x > u['refuta'] for x in d.values())))
        log(f"   H1-7 {u['frase']}\n        -> frac_fund {d}  {'PASA (el regalo ya no financia)' if P['H1-7']['pasa'] else ('REFUTADA: el regalo sigue financiando' if P['H1-7']['refutada'] else 'NO')}")

    u = UMBRALES['H1-8']
    if hay('NADA_CM', 'RENACE_CM'):
        ncoh = {b: M[b]['coherentes'] for b in M}; ndes = {b: M[b]['desborde'] for b in M}
        fc = razon(M['NADA_CM']['exposiciones']['A'], M['RENACE_CM']['exposiciones']['A'])
        P['H1-8'] = dict(coherentes=ncoh, desborde=ndes, comida=fc,
                         pasa=bool(all(x >= min(u['n_min'], len(S)) for x in ncoh.values()) and all(x == 0 for x in ndes.values()) and ge(fc, u['f_com'])))
        log(f"   H1-8 {u['frase']}\n        -> coherentes min {min(ncoh.values())}/{len(S)}; desbordes {sum(ndes.values())}; comida x{fc}  "
            f"{'PASA' if P['H1-8']['pasa'] else 'NO'}")
    return P


def frase_final(V):
    P = V['completo']
    p = {k: (P.get(k) or {}).get('pasa') for k in UMBRALES}
    if not p['H1-1']:
        return ("EL CONTROL NO ANCLA (H1-1): RENACE no reproduce el bloque 2 -> el instrumento se movio y NO SE LEE NADA MAS. "
                "Se revisa el arnes y los shas antes de volver a correr.")
    s = ("Con la muerte que BORRA la memoria del individuo, el linaje no se reemplaza: R0 cae muy por debajo de 1 (H1-2). " if p['H1-2'] else
         ("REFUTADA H1-2: borrar la memoria NO cambia el linaje — el regalo del renacer era energia, no memoria. " if (P.get('H1-2') or {}).get('refutada')
          else "H1-2 no concluyente: la muerte real no baja R0 tanto como se predijo. "))
    s += ("Heredar el VECTOR de valores (M1) sube R0 sobre no heredar nada (H1-3). " if p['H1-3'] else
          ("REFUTADA H1-3: heredar el vector no compra nada. " if (P.get('H1-3') or {}).get('refutada') else "H1-3 no concluyente. "))
    q4 = P.get('H1-4') or {}
    s += ("BARAJA ~ NADA: lo que se hereda es el CONTENIDO del vector, no su magnitud (H1-4, la prediccion que decide). " if p['H1-4'] else
          ("H1-4 refuta (a): lo heredable es la MAGNITUD (una cautela heredada), no el contenido. " if q4.get('refuta_a') else
           ("H1-4 refuta (b): heredar valores en los pixeles equivocados es PEOR que no heredar. " if q4.get('refuta_b') else "H1-4 no concluyente. ")))
    q5 = P.get('H1-5') or {}
    s += ("El TOKEN (codigo + pares) aporta sobre el vector solo (H1-5). " if p['H1-5'] else
          ("Lo portable entre cuerpos es el VECTOR: el token no aporta (H1-5). " if q5.get('vector') else "H1-5 no concluyente. "))
    s += ("Hay al menos un ajuste con muerte real en el filo del reemplazo: " + str((P.get('H1-6') or {}).get('candidatos')) +
          " — NO se declara aqui (la rampa es busqueda): bloque nuevo con semillas nuevas. " if p['H1-6'] else
          "NINGUNA de las cuatro perillas lleva el linaje mortal a R0 ~ 1: ERR-62 — este mundo NO SOSTIENE LINAJES MORTALES y la linea de evolucion no se corre hasta cambiar el MUNDO. ")
    s += ("El regalo del renacer ya no financia las ventanas (H1-7). " if p['H1-7'] else "H1-7 cae: el regalo sigue financiando, la medida no esta limpia. ")
    s += ("Contabilidad y mundo intactos (H1-8). " if p['H1-8'] else "H1-8 cae (contabilidad o mundo). ")
    return s + "20 semillas no cierran nada: piden la replica en 721-740 (regla 12)."


# ---------------------------------------------------------------- humo (UN proceso, 4 corridas)
def humo():
    stamp = time.strftime('%Y%m%d_%H%M%S')
    os.makedirs(os.path.join(RAIZ, 'datos'), exist_ok=True)
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'vivo_h1_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO del disenador, UN proceso, sin Pool (regla 3: 4 corridas de 100000). PREREGISTRO_h1_muerte.md §8.")
    log("MISION: llegar a la AGI por este camino. Hoy: que la muerte mate de verdad, para que el linaje signifique algo.")
    log("Semillas 1-2: NINGUNA de las 701-740 del bloque queda expuesta.")
    for k, v in SHAS().items():
        log(f"    sha {k:28s} {v}")
    log(f"    origenes -> {'OK' if guarda_origen() else 'FALLA'}")
    log(f"    ERR-38 (campo a campo) -> {'OK' if guarda_err38() else 'FALLA'}")
    log(f"    alias estructurales 701-720: {C1.alias_de(range(701, 721))}; 721-740: {C1.alias_de(range(721, 741))}")
    Ti, sem = 5000, [1, 2]
    log(f"1/2 IDENTIDAD dentro del runner, {len(CASOS_ID)} casos x {len(sem)} semillas, T={Ti}.")
    ident = []
    for cual in CASOS_ID:
        for s in sem:
            ident.append(tarea(('ID', cual, s, Ti)))
        g = [r for r in ident if r['cual'] == cual]
        log(f"    {CASOS_ID[cual][0]:78s} {sum(r['ok'] for r in g)}/{len(g)}" + ("" if all(r['ok'] for r in g) else f"   {g[0]['difieren']} {g[0]['faltan']} {g[0]['extra']}"))
    log(f"  IDENTIDAD {sum(r['ok'] for r in ident)}/{len(ident)}")
    if sum(r['ok'] for r in ident) != len(ident):
        log("*** IDENTIDAD FALLIDA: no se corre el humo."); _log['f'].close(); sys.exit(1)
    plan = [('RENACE_CM', 1), ('NADA_CM', 1), ('RENACE_CM', 2), ('NADA_CM', 2)]
    log(f"2/2 {len(plan)} corridas de T={T}: {plan}")
    log(f"    {'brazo':11s} s {'seg':>5s} {'R0':>6s} {'r':>5s} {'desc':>4s} {'muertes':>7s} {'cuerpos':>7s} {'vida med (f/h)':>20s} {'fund':>5s} {'regalo/fund':>12s} {'coh':>4s}")
    res, tb = [], {}
    for b, s in plan:
        t1 = time.time(); r = tarea(('R', b, s, T)); tb[f'{b}_s{s}'] = round(time.time() - t1, 1); res.append(r)
        log(f"    {b:11s} {s} {tb[f'{b}_s{s}']:5.1f} {r['R0']:6.3f} {r['r']:5d} {r['descendientes']:4d} {r['deaths']:7d} {r['cuerpos']:7d} "
            f"{str(r['vida_med_h1'])+' ('+str(r['vida_med_fund'])+'/'+str(r['vida_med_her'])+')':>20s} {r['fundadores']:5d} "
            f"{str(r['frac_regalo'])+'/'+str(r['frac_fund']):>12s} {str(r['coherente']):>4s}")
        log(f"                desc por cuarto {r['desc_q']}; 1.a fundacion en t={r['t_fund1']}; heredados {r['heredados']} (R0_her {r['R0_her']}); "
            f"saciado sal {r['sac_tasa']['D']}; xor01 {r['xor01']} (se reporta); coherencia {r['coherencia']}")
    R = {(r['brazo'], r['seed']): r for r in res}
    H = {}
    H['HH1'] = all(R[('RENACE_CM', s)]['r'] > R[('NADA_CM', s)]['r'] for s in (1, 2))
    H['HH2'] = all(R[('NADA_CM', s)]['R0'] < 1.0 and R[('RENACE_CM', s)]['R0'] > R[('NADA_CM', s)]['R0'] for s in (1, 2))
    H['HH3'] = all(r['coherente'] for r in res)
    H['HH4'] = all(R[('NADA_CM', s)]['vida_med_h1'] < R[('RENACE_CM', s)]['vida_med_h1'] for s in (1, 2))
    H['HH5'] = all(R[('NADA_CM', s)]['fundadores'] >= 1 for s in (1, 2))
    H['HH6'] = all(le(R[('NADA_CM', s)]['frac_fund'], 0.35) for s in (1, 2))
    for k in HUMO:
        log(f"   {k} {HUMO[k]:106s} -> {'SI' if H[k] else 'NO'}")
    seg = sum(tb.values()) / len(tb)
    log(f"ESTIMACION del bloque: {len(ORDEN)}x{N_SEM} = {len(ORDEN)*N_SEM} corridas de {T}, ~{seg:.1f} s/corrida -> "
        f"~{len(ORDEN)*N_SEM*seg/N_PARALELO/60:.1f} min con Pool({N_PARALELO}).")
    log("HUMO: numeros observados, sin ajustar nada. n = 1-2 y semillas ya vistas: NO son evidencia.")
    dj = os.path.join(RAIZ, 'datos', f'vivo_h1_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T_identidad=Ti, T_brazo=T, plan=plan, umbrales=UMBRALES,
                             humo_predicciones=HUMO, humo_resultado=H, shas=SHAS(), segundos=tb, dote=DOTE,
                             brazos={b: {k: (list(v) if isinstance(v, tuple) else v) for k, v in BRAZOS[b].items()} for b in BRAZOS},
                             python=platform.python_version(), numpy=np.__version__),
                   identidades=ident, brazos=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


# ---------------------------------------------------------------- principal (Pool: SOLO el coordinador)
if __name__ == '__main__':
    if '--humo' in sys.argv:
        humo(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else DESDE
    if '--T' in sys.argv:
        T = int(sys.argv[sys.argv.index('--T') + 1])
    if '--brazos' in sys.argv:
        BRAZOS_ACTIVOS = [b.strip() for b in sys.argv[sys.argv.index('--brazos') + 1].split(',') if b.strip()]
        malos = [b for b in BRAZOS_ACTIVOS if b not in BRAZOS]
        if malos:
            raise SystemExit(f"--brazos: desconocidos {malos}. Validos: {ORDEN}")
        for req in ('RENACE_CM', 'NADA_CM'):
            if req not in BRAZOS_ACTIVOS:
                raise SystemExit(f"--brazos: {req} es referencia obligatoria (H1-1 y H1-2).")
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    os.makedirs(os.path.join(RAIZ, 'datos'), exist_ok=True)
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'vivo_h1_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE H-1 (la muerte que mata; R0 = descendientes por vida): brazos {BRAZOS_ACTIVOS}, semillas {SEEDS[0]}-{SEEDS[-1]}, T={T}. Pool({N_PARALELO}).")
    log("MISION: llegar a la AGI por este camino. Hoy: que la muerte mate de verdad, para que el linaje signifique algo.")
    log("20 semillas no cierran nada: cierran o refutan ESTA hipotesis y piden la replica (721-740).")
    for k, v in SHAS().items():
        log(f"    sha {k:28s} {v}")
    if not guarda_origen() or not guarda_err38():
        sys.exit(1)
    alias = C1.alias_de(SEEDS)
    log(f"REGLA 10 — alias estructurales en {SEEDS[0]}-{SEEDS[-1]}: {alias} (preregistro: 701-720 -> [715]; 721-740 -> [])")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V, res = {}, []
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('ID', c, s, T_ID) for c in CASOS_ID for s in SEMILLAS_ID]
        log(f"ETAPA 1/2 — IDENTIDAD interna ({len(ctrl)} comprobaciones de 2 x {T_ID} pasos). (D) y (E) DEBEN fallar.")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in CASOS_ID:
            g = [r for r in rc if r['cual'] == cual]
            log(f"    {CASOS_ID[cual][0]:78s} {sum(r['ok'] for r in g)}/{len(g)}" + ("" if all(r['ok'] for r in g) else f"   {g[0]['difieren']} {g[0]['faltan']} {g[0]['extra']}"))
            V[f'ID_{cual}'] = all(r['ok'] for r in g)
        V['G_IDENTIDAD'] = bool(all(V[f'ID_{c}'] for c in CASOS_ID))
        log(f"  IDENTIDAD {sum(r['ok'] for r in rc)}/{len(rc)}")
        if not V['G_IDENTIDAD']:
            log("*** GUARDA DE IDENTIDAD FALLIDA. Se para."); sys.exit(1)
        tr = [('R', b, s, T) for b in BRAZOS_ACTIVOS for s in SEEDS]
        log(f"ETAPA 2/2 — principal: {len(tr)} corridas de {T} pasos...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 40 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    # ERR-54: los datos CRUDOS se guardan ANTES de analizar nada
    meta0 = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, alias=alias, dote=DOTE, umbrales=UMBRALES,
                 brazos={b: {k: (list(v) if isinstance(v, tuple) else v) for k, v in BRAZOS[b].items()} for b in BRAZOS_ACTIVOS},
                 identidades=rc, procesos_python=ps, shas=SHAS(), origenes_esperados=SHA_ESPERADOS,
                 python=platform.python_version(), numpy=np.__version__)
    dc = os.path.join(RAIZ, 'datos', f'vivo_h1_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}_crudo.json')
    json.dump(dict(meta=meta0, principal=res), open(dc, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"ERR-54 — CRUDO guardado ANTES del analisis -> {os.path.basename(dc)}  sha256_16 = {h16(dc)}")
    log(); log("ANALISIS — medianas por brazo y la letra del preregistro (A12 sin parear, medianas, cuartiles).")
    V.update(veredicto(res, SEEDS))
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")
    dj = os.path.join(RAIZ, 'datos', f'vivo_h1_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=dict(meta0, veredicto=ver, veredictos=V, crudo=os.path.basename(dc)), principal=res),
              open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
