"""corre_mundo_fase10.py -- EL MUNDO DE LA FASE 10: un linaje mortal solo se sostiene si transmite, y lo transmitido tiene que crecer.

MISION: llegar a la AGI por este camino -- organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas. Hoy: no se pide un organo; se pide un MUNDO. El organismo es el tronco v14.2 (B-5 encendido) con el cuerpo
de la fase 9 (mundo vivo + muerte real + nodo por relevancia) y el mapa de nivel 6, ninguno cambiado a mano. Se mide si el linaje
se sostiene (M10-1), si la generacion 5 come lo que la 1 no podia (M10-2), si eso lo exige el cambio (M10-3), sin regresion (M10-4).

Ejecuta PREREGISTRO_mundo_fase10.md. Instrumento mundo_fase10.py (construye_mundo_fase10.py, por anclas desde organismo_f9.py
3a821884394d66c9 + organismo_v142.py 17528d767fcebaf6 + mundo_mapa.py 207d6a1954336b18; arnes identidad_mundo_fase10.py).

    python corre_mundo_fase10.py --humo                       (UN proceso, 6 corridas de T=100000, escribe datos/humo/*.json: lo corre el disenador)
    python corre_mundo_fase10.py --serie --desde 2401 --pool 7  (LA SERIE: solo el COORDINADOR, con Pool; JUACO_POOL manda si no hay --pool, ERR-86)
    python corre_mundo_fase10.py --serie --desde 2421 --pool 7  (REPLICA, regla 12)

ERR-89: EXACTAMENTE una linea impresa por puerta M10-1..M10-5 y COSTE, con su frase, su umbral y PASA/CAE. UMBRALES trae la letra (ERR-31).
ERR-54: el crudo se guarda ANTES de analizar. ERR-87: lee_json exige prefijo + SELLO exacto. ERR-42: el humo abre el JSON que escribio.
Regla 15 (ERR-91): cada puerta declara su NULO, su MARGEN y la n que deja pasar al placebo >= 0.95; el brazo PLACEBO corre entre los brazos.

LOS BRAZOS (todos en el mundo 10, mismo cuerpo campo a campo = corre_f9.CUERPO; solo cambian las perillas del NODO/MAPA/MUNDO)
  INMORTAL          muerte_real=0: la cota superior del mundo (RENACE de la fase 9). ANCLA: R0 en [0.8, 1.3].
  NADA              muerte real, sin nodo: el tronco solo. ANCLA: R0 en [0.1, 0.3].
  PLACEBO           NADA + placebo=1 (un sorteo del rng del organismo por paso, descartado): el NULO EXACTO de la regla 15.
  SIN_HERENCIA      nodo escrito, nadie lo lee (conectado=0): cada cuerpo nace vacio.
  REL               nodo por relevancia (fase 9), SIN mapa: sabe QUE, no DONDE.
  MAPA              <- EL CANDIDATO: REL + mapa (r_vis=8, usa_M=1) + el sitio del mensaje entra en la tabla M del recien nacido (nodo_sitio=1): QUE y DONDE.
  NODO_BARAJADO     MAPA con las recompensas de los mensajes permutadas (mismo QUE marginal, asociacion destruida): control de CONTENIDO.
  SITIO_BARAJADO    MAPA con los sitios permutados entre mensajes: control de DONDE.
  ORACULO_SIN_MAPA  nodo con la TABLA VERDADERA actual (tipo,necesidad)->R, sin sitio, sin mapa: sabe QUE perfecto, no DONDE.
  MAPA_SIN_TABLA    MAPA con nodo_tabla=0: el recien nacido recibe DONDE y no QUE.
  MUNDO_FIJO        MAPA con cambio10=0: el mundo sin cambios de valencia (M10-3).
  NADA_FIJO         NADA con cambio10=0 (la base del mundo fijo, se reporta).

VOCABULARIO (regla 6): "cuerpo", "linaje", "generacion" (= partos desde el fundador), "nodo del linaje", "combinacion explotada",
"R0 del linaje". NO se dice "poblacion", "cultura", "ensena", "entiende", "planifica". Un solo cuerpo a la vez (mas de un cuerpo
queda como OPCION declarada, no medida).
"""
import argparse, hashlib, json, os, platform, re, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
JUACO = r"C:\Users\User\Documents\PROYECTOS\JUACO\bundle"
sys.path[:0] = [AQUI, os.path.join(JUACO, 'organismo'), os.path.join(JUACO, 'experimentos', 'nivel09_cuerpo_nuevo'),
                os.path.join(JUACO, 'experimentos', 'nivel13_alma'), os.path.join(JUACO, 'experimentos', 'nivel11_mundo_vivo')]   # organismo/ PRIMERO (ERR-28)

import corre_f9 as CF               # CUERPO, NODO, A12, med, razon, h16: NO se copian (campo a campo, regla 14)
import mundo_fase10 as M

med, A12, razon, N, h16 = CF.med, CF.A12, CF.razon, CF.N, CF.h16

T = 100000
N_SEM = 20
DESDE = 2401                        # semillas libres al 21-sep (>= 2361; grep en experimentos/, registro/ y datos/: ninguna 24xx usada)
DATOS = os.path.join(AQUI, 'datos')
HUMO = os.path.join(DATOS, 'humo')
SHA_ESPERADOS = dict(f9='3a821884394d66c9', v142='17528d767fcebaf6', v14='feefc88b1fd8d434', mapa='207d6a1954336b18',
                     vivo_codigo='839fa71f9c84cb26', alma2='4fd616aeaf535e61')
GEN5 = 5                            # "generacion 5" = quinto cuerpo del linaje por parto (el fundador es la 1)
MIN_G5 = 10                         # E-14: un control con menos de 10 cuerpos de generacion >= 5 en toda la serie NO se lee (se declara NO EVALUABLE)

# ------------------------------------------------------------------ EL CUERPO (regla 14: campo a campo con corre_f9)
CUERPO = dict(CF.CUERPO)            # CUELLO_MIN + MED2 + h1 + muerte_real=1 + hereda='nada' + dote=0.6 (los numeros de H-1 y de la fase 9, sin tocar)
NODO = dict(CF.NODO)                # alma nula (curita f), menu='f', f9=1, nodo_k=20, nodo_lee=50
MUNDO = dict(desambiguar=1, mundo10=1, npx=9, estims=None, L10=None, nsit10=6, stock10=25, regen10=50, cambio10=12500, flip10=1,
             nfam10=4, nvar10=2, r_vis=8, f10=1)   # EL MUNDO (fijado tras las sondas del 21-sep, ANTES del humo; ver PREREGISTRO §2)
MAPA = dict(usa_M=1, nodo_sitio=1, escribe_M=1, gamma_M=0.6, H_M=20, disc_M=0.9)   # mundo_mapa, sus defaults EXPLICITOS (regla 14)
BRAZOS = {
    'INMORTAL':         dict(CUERPO, **MUNDO, muerte_real=0, hereda='nada'),
    'NADA':             dict(CUERPO, **MUNDO, **NODO, nodo=0, conectado=0),
    'PLACEBO':          dict(CUERPO, **MUNDO, **NODO, nodo=0, conectado=0, placebo=1),
    'SIN_HERENCIA':     dict(CUERPO, **MUNDO, **NODO, nodo=1, conectado=0),
    'REL':              dict(CUERPO, **MUNDO, **NODO, nodo=1, conectado=1, nodo_rel=1),
    'MAPA':             dict(CUERPO, **MUNDO, **NODO, nodo=1, conectado=1, nodo_rel=1, **MAPA),
    'NODO_BARAJADO':    dict(CUERPO, **MUNDO, **NODO, nodo=1, conectado=1, nodo_rel=1, **MAPA, nodo_baraja=1),
    'SITIO_BARAJADO':   dict(CUERPO, **MUNDO, **NODO, nodo=1, conectado=1, nodo_rel=1, **MAPA, sitio_baraja=1),
    'ORACULO_SIN_MAPA': dict(CUERPO, **MUNDO, **NODO, nodo=1, conectado=1, nodo_rel=1, nodo_or=1),
    'MAPA_SIN_TABLA':   dict(CUERPO, **MUNDO, **NODO, nodo=1, conectado=1, nodo_rel=1, **MAPA, nodo_tabla=0),
    'MUNDO_FIJO':       dict(dict(CUERPO, **MUNDO, **NODO, nodo=1, conectado=1, nodo_rel=1, **MAPA), cambio10=0),
    'NADA_FIJO':        dict(dict(CUERPO, **MUNDO, **NODO, nodo=0, conectado=0), cambio10=0),
}
ORDEN = ['INMORTAL', 'NADA', 'PLACEBO', 'SIN_HERENCIA', 'REL', 'MAPA', 'NODO_BARAJADO', 'SITIO_BARAJADO', 'ORACULO_SIN_MAPA',
         'MAPA_SIN_TABLA', 'MUNDO_FIJO', 'NADA_FIJO']

# ------------------------------------------------------------------ LA LETRA DEL PREREGISTRO (ERR-31); nulo/margen/n en el PREREGISTRO §4
UMBRALES = {
    'M10-0': dict(frase="ANCLA (BLOQUEANTE) y REQUISITOS DEL MUNDO: NADA en [0.1, 0.3], INMORTAL en [0.8, 1.3] (§2.1.6); la comida por sitio "
                        "se agota en <= T/4 (§2.1.1); el alias existe (§2.1.3)",
                 R0_NADA=(0.10, 0.30), R0_INMORTAL=(0.80, 1.30), vida_sitio_max=T / 4, alias_min=0.5),
    'M10-1': dict(frase="SOSTEN: con nodo por relevancia + mapa el linaje cruza R0 >= 1.0 (fundadores <= 2) en >= 15/20 semillas; "
                        "sin nodo (NADA) y con nodo barajado, R0 < 0.5; el PLACEBO no cruza",
                 R0=1.0, fund=2, k=15, R0_ctrl=0.5),
    'M10-2': dict(frase="ACUMULACION: la generacion 5 come lo que la 1 no podia -- cobertura de combinaciones (tipo x necesidad) explotadas por "
                        "cuerpos de generacion >= 5 >= 2x la de la generacion 1, A12 >= 0.85; con nodo barajado <= 1.2x",
                 razon=2.0, A12=0.85, razon_ctrl=1.2),
    'M10-3': dict(frase="NO ES EL MUNDO BLANDO: el mundo sin cambios (MUNDO_FIJO) NO produce M10-2 (razon gen5/gen1 <= 1.2x)",
                 razon_max=1.2),
    'M10-4': dict(frase="NO REGRESION: perillas apagadas == tronco v14.2 BIT A BIT (arnes I2/I3, 12 escenarios + T=120000); el mapa con vision "
                        "ilimitada es inerte en el mundo del tronco (I4) -> G1 >= 0.80 / G2 >= 0.85 heredados por identidad",
                 arnes='identidad_mundo_fase10_salida.txt'),
    'M10-5': dict(frase="REPRESENTACION (exploratoria, SE REPORTA, no es puerta): celdas, divisiones B-5 (R==0) y selectividad de celdas por tipo, por brazo",
                 ),
    'COSTE': dict(frase="COSTE: muertes y celdas de MAPA <= 1.25x las de NADA en el mundo 10 (en el mundo del tronco el coste es 0 por identidad)",
                  razon=1.25),
    'SEG':   dict(frase="SEGURIDAD: contabilidad H1-8; la relevancia releva (lect_div > 0) y el mapa recibe sitios (sitios_leidos > 0); "
                        "exposiciones por brazo >= 0.5x NADA (trampa 3); cobertura de celdas de cambio >= 2 por tipo (E-10)",
                  frac_div=0.5, exp_min=0.5),
}


# ------------------------------------------------------------------ utilidades
LOG = [None]


def log(msg=""):
    print(msg, flush=True)
    if LOG[0]:
        LOG[0].write(msg + "\n"); LOG[0].flush(); os.fsync(LOG[0].fileno())


def sello():
    return time.strftime('%Y%m%d_%H%M%S')


def lee_json(carpeta, prefijo, sel):
    """ERR-87: prefijo + SELLO EXACTO (nunca 'el ultimo que empiece por')."""
    ruta = os.path.join(carpeta, f"{prefijo}_{sel}.json")
    if not os.path.exists(ruta):
        raise SystemExit(f"lee_json: no existe {ruta} (prefijo + sello EXACTO, ERR-87)")
    return json.load(open(ruta, encoding='utf-8')), ruta


def ge(x, u): return x is not None and x >= u
def le(x, u): return x is not None and x <= u
def dentro(x, lo, hi): return x is not None and lo <= x <= hi


# ------------------------------------------------------------------ una corrida
def resumen(brazo, seed, r, Ti):
    """SOLO LECTURA sobre el crudo. R0 = desc / (muertes + 1) (H-1 sec. 3, la misma de la fase 9)."""
    d, mu = r['descendientes'], r['deaths']
    vidas = r.get('vidas_h1') or r.get('vidas') or []
    f9 = r.get('f9') or {}; f10 = r.get('f10') or {}
    cu = f10.get('cuerpos') or []            # [gen, comb, combu, cob, lin, vida, veneno_reciente] por cuerpo que murio
    g1 = [c[3] for c in cu if c[0] == 1]; g5 = [c[3] for c in cu if c[0] >= GEN5]
    lin5 = [c[4] for c in cu if c[0] >= GEN5]
    cerr = r.get('sitios_cerrados') or []    # [x, tipo, t_apertura, t_cierre, bocados, causa]
    vs = [c[3] - c[2] for c in cerr if c[5] == 'agotado']
    al = f10.get('alias') or []
    o = dict(brazo=brazo, seed=seed, seg=round(Ti, 1), descendientes=d, muertes=mu, R0=round(d / (mu + 1), 4), r=d - mu,
             vida_med=med(vidas), cuerpos=len(vidas), fundadores=r.get('fundadores'), muertes_nec=r.get('muertes_nec'),
             p1=CF.frac(f9.get('p1', [])), c1=CF.frac(f9.get('c1', [])),
             J=(None if CF.frac(f9.get('p1', [])) is None or CF.frac(f9.get('c1', [])) is None
                else round(CF.frac(f9.get('p1', [])) + CF.frac(f9.get('c1', [])) - 1, 4)),
             sac_frac=razon(r.get('pasos_viables'), r.get('T_efectivo') or T),
             lect_div=f9.get('lect_div'), lecturas=f9.get('lecturas'), frac_div=razon(f9.get('lect_div'), f9.get('lecturas')),
             exposiciones=sum((r.get('exposiciones') or {}).values()) or None,
             gen_max=max([c[0] for c in cu], default=None), n_gen5=len(g5), cob_g1=med(g1), cob_g5=med(g5), lin_g5=med(lin5),
             cob_g1_lista=g1[:200], cob_g5_lista=g5[:200],
             agotados=r.get('agotados'), trasladados=r.get('trasladados'), vida_sitio=med(vs), n_cambios=len(r.get('cambios') or []),
             cambios_por_tipo=[sum(1 for c in (r.get('cambios') or []) if c[1] == k) for k in sorted((r.get('patrones') or {}))],
             alias_med=med(al), alias_frac=(round(sum(1 for a in al if a > 0) / len(al), 4) if al else None),
             muertes_veneno_reciente=f10.get('muertes_veneno_reciente'),
             sitios_leidos=r.get('sitios_leidos'), M_llenas=r.get('M_llenas'),
             celdas=r.get('celdas'), splits=r.get('splits'), des_splits=r.get('des_splits'),
             selectividad=f10.get('selectividad'), celdas_sin_tipo=f10.get('celdas_sin_tipo'),
             cola_desborde=r.get('cola_desborde'), T_efectivo=r.get('T_efectivo'))
    org = r.get('origen_cuerpo') or []
    ok = (r.get('nacimientos') == mu and len(vidas) == mu + 1 and len(r.get('desc_por_vida') or []) == mu + 1 and len(org) == mu + 1
          and sum(vidas) == (r.get('T_efectivo') or T) and sum(r.get('desc_por_vida') or []) == d
          and (r.get('fundadores') or 0) + 1 == sum(1 for g in org if not g))
    o['coherente'] = bool(ok) if r.get('muerte_real') else None
    return o


def tarea(args):
    brazo, seed, Ti = args
    t0 = time.time()
    r = M.run(seed, T=Ti, **BRAZOS[brazo])
    return resumen(brazo, seed, r, time.time() - t0)


# ------------------------------------------------------------------ las puertas (ERR-89: una linea por puerta)
def cel(R, brazo, campo):
    return [x[campo] for x in R if x['brazo'] == brazo and x[campo] is not None]


def m(R, brazo, campo):
    return med(cel(R, brazo, campo))


def razon_gen(R, brazo):
    """M10-2: mediana (sobre cuerpos, toda la serie) de la cobertura de la generacion >= 5 / la de la generacion 1; y cuantos cuerpos g5 hay."""
    g5 = [v for x in R if x['brazo'] == brazo for v in x['cob_g5_lista']]
    g1 = [v for x in R if x['brazo'] == brazo for v in x['cob_g1_lista']]
    if len(g5) < MIN_G5 or not g1:
        return None, len(g5), len(g1), (med(g1) if g1 else None), (med(g5) if g5 else None)
    return razon(med(g5), med(g1)), len(g5), len(g1), med(g1), med(g5)


def puertas(R, log=log):
    V, U = {}, UMBRALES
    n = len({x['seed'] for x in R})

    def linea(p, ok, txt):
        V[p] = dict(pasa=(None if ok is None else bool(ok)), detalle=txt, frase=U[p]['frase'])
        log(f"  {p}  {'PASA' if ok else ('n/a ' if ok is None else 'CAE ')}  {U[p]['frase']}")
        log(f"          {txt}")

    u = U['M10-0']
    a = dict(R0_NADA=m(R, 'NADA', 'R0'), R0_INMORTAL=m(R, 'INMORTAL', 'R0'))
    vs = m(R, 'NADA', 'vida_sitio'); ag = m(R, 'NADA', 'agotados'); al = m(R, 'NADA', 'alias_frac')
    ok0 = all(dentro(a[k], *u[k]) for k in a) and le(vs, u['vida_sitio_max']) and ge(ag, 1) and ge(al, u['alias_min'])
    linea('M10-0', ok0, " · ".join(f"{k} {a[k]} en {u[k]}" for k in a) + f" · vida mediana de un sitio hasta agotarse {vs} (<= T/4 = {u['vida_sitio_max']:.0f}), "
          f"sitios agotados {ag} · fraccion de cuerpos que mueren con >= 1 alias de codigo entre tipos {al} (>= {u['alias_min']}) · "
          f"muertes NADA [energia, agua] {m(R,'NADA','muertes_nec')} · cambios por corrida {m(R,'NADA','n_cambios')}")

    u = U['M10-1']
    k1 = sum(1 for x in R if x['brazo'] == 'MAPA' and x['R0'] >= u['R0'] and (x['fundadores'] or 0) <= u['fund'])
    kp = sum(1 for x in R if x['brazo'] == 'PLACEBO' and x['R0'] >= u['R0'] and (x['fundadores'] or 0) <= u['fund'])
    ok1 = k1 >= u['k'] and le(m(R, 'NADA', 'R0'), u['R0_ctrl'] - 1e-9) and le(m(R, 'NODO_BARAJADO', 'R0'), u['R0_ctrl'] - 1e-9) and kp < u['k']
    linea('M10-1', ok1, f"MAPA R0 >= {u['R0']} con fundadores <= {u['fund']}: {k1}/{n} (>= {u['k']}); R0 mediana MAPA {m(R,'MAPA','R0')} · "
          f"NADA {m(R,'NADA','R0')} (< {u['R0_ctrl']}) · NODO_BARAJADO {m(R,'NODO_BARAJADO','R0')} (< {u['R0_ctrl']}) · PLACEBO cruza {kp}/{n} (debe ser < {u['k']}) · "
          f"REL {m(R,'REL','R0')} · SITIO_BARAJADO {m(R,'SITIO_BARAJADO','R0')} · ORACULO_SIN_MAPA {m(R,'ORACULO_SIN_MAPA','R0')} · MAPA_SIN_TABLA {m(R,'MAPA_SIN_TABLA','R0')} · "
          f"fundadores MAPA {m(R,'MAPA','fundadores')} · vida MAPA {m(R,'MAPA','vida_med')} vs NADA {m(R,'NADA','vida_med')}")

    u = U['M10-2']
    rz, n5, n1, c1_, c5_ = razon_gen(R, 'MAPA')
    a2 = A12([x['cob_g5'] for x in R if x['brazo'] == 'MAPA' and x['cob_g5'] is not None], [x['cob_g1'] for x in R if x['brazo'] == 'MAPA' and x['cob_g1'] is not None])
    rb, nb5, nb1, _, _ = razon_gen(R, 'NODO_BARAJADO'); rp, np5, np1, _, _ = razon_gen(R, 'PLACEBO')
    ctrl_ok = (rb is None or rb <= u['razon_ctrl']) and (rp is None or rp <= u['razon_ctrl'])
    ok2 = ge(rz, u['razon']) and ge(a2, u['A12']) and ctrl_ok
    linea('M10-2', ok2, f"MAPA cobertura gen>=5 {c5_} / gen 1 {c1_} = {rz} (>= {u['razon']}; cuerpos g5 {n5}, g1 {n1}) · A12 por semilla {a2} (>= {u['A12']}) · "
          f"NODO_BARAJADO razon {rb} (<= {u['razon_ctrl']}; g5 {nb5}: {'NO EVALUABLE, < ' + str(MIN_G5) + ' cuerpos g5' if rb is None else 'evaluable'}) · "
          f"PLACEBO razon {rp} (g5 {np5}) · linaje: union de combinaciones al llegar a g5, MAPA {m(R,'MAPA','lin_g5')} (§2.1.4: > 0.8) vs cuerpo solo g1 {c1_} (< 0.5) · gen max MAPA {m(R,'MAPA','gen_max')}")

    u = U['M10-3']
    rf, nf5, nf1, cf1, cf5 = razon_gen(R, 'MUNDO_FIJO')
    ok3 = None if rf is None else (rf <= u['razon_max'])
    linea('M10-3', ok3, f"MUNDO_FIJO cobertura gen>=5 {cf5} / gen 1 {cf1} = {rf} (<= {u['razon_max']}; g5 {nf5}, g1 {nf1}) · R0 MUNDO_FIJO {m(R,'MUNDO_FIJO','R0')} vs "
          f"NADA_FIJO {m(R,'NADA_FIJO','R0')} · si MUNDO_FIJO no llega a g5 se declara n/a y M10-3 se juzga por la serie siguiente")

    u = U['M10-4']
    arn = os.path.join(AQUI, u['arnes'])
    txt = open(arn, encoding='utf-8').read() if os.path.exists(arn) else ''
    ok4 = ('VEREDICTO identidad_mundo_fase10: PASA' in txt)
    linea('M10-4', ok4, f"arnes {u['arnes']} {'PASA' if ok4 else 'no pasa o no existe'} (sha {h16(arn) if os.path.exists(arn) else None}); "
          f"G1/G2 del tronco v14.2 heredados por identidad (I2, I3, I4); comando del coordinador si quiere rehacerlos: "
          f"python organismo/bateria_generaliza_v142.py organismo_v142 20 --desde 101 --log")

    linea('M10-5', True, " · ".join(f"{b}: celdas {m(R,b,'celdas')} divB5 {m(R,b,'des_splits')} selectividad {m(R,b,'selectividad')} sin_tipo {m(R,b,'celdas_sin_tipo')}"
                                   for b in ('NADA', 'REL', 'MAPA', 'NODO_BARAJADO', 'INMORTAL')))

    u = U['COSTE']
    rm = razon(m(R, 'MAPA', 'muertes'), m(R, 'NADA', 'muertes')); rc = razon(m(R, 'MAPA', 'celdas'), m(R, 'NADA', 'celdas'))
    linea('COSTE', le(rm, u['razon']) and le(rc, u['razon']), f"muertes MAPA/NADA {rm} (<= {u['razon']}) · celdas MAPA/NADA {rc} (<= {u['razon']})")

    u = U['SEG']
    coh = [x for x in R if x['coherente'] is False]
    fd = m(R, 'MAPA', 'frac_div'); sl = m(R, 'MAPA', 'sitios_leidos')
    eN = m(R, 'NADA', 'exposiciones')
    pobres = [(b, m(R, b, 'exposiciones')) for b in ORDEN if eN and m(R, b, 'exposiciones') is not None and m(R, b, 'exposiciones') < u['exp_min'] * eN]
    cob = [x['cambios_por_tipo'] for x in R if x['brazo'] == 'NADA']
    e10 = min((min(c) for c in cob if c), default=None)
    linea('SEG', not coh and ge(fd, u['frac_div']) and ge(sl, 1) and not pobres,
          f"contabilidad {len(R)-len(coh)}/{len(R)} · frac_div MAPA {fd} (>= {u['frac_div']}) · sitios leidos MAPA {sl} · exposiciones (ref NADA {eN}) pobres {pobres or 'ninguna'} · "
          f"minimo de cambios por tipo en una corrida {e10} (E-10: se reporta; con cambio10=12500 y T={T} hay {2*(T//12500)} cambios entre 8 tipos)")
    return V


# ------------------------------------------------------------------ identidad corta dentro del runner (regla 14)
def identidad_corta(Ti=20000, sem=(1,)):
    import organismo_f9 as F9, organismo_v142 as V142
    out = []
    for s in sem:
        a = F9.run(s, T=Ti, **CF.BRAZOS['NADA']); b = M.run(s, T=Ti, **CF.BRAZOS['NADA'])
        dif = [k for k in a if N(a[k]) != N(b.get(k))]
        out.append(('(1) perillas apagadas == organismo_f9 (NADA de la fase 9, claves viejas)', not dif, f"dif {dif[:4]}"))
        a = V142.run(s, T=Ti); b = M.run(s, T=Ti, desambiguar=1)
        dif = [k for k in set(a) | set(b) if N(a.get(k)) != N(b.get(k))]
        out.append(('(2) vivo=0, n_nec=1, desambiguar=1 == organismo_v142 (TRONCO, todas las claves)', not dif, f"dif {dif[:4]}"))
        r1 = M.run(s, T=Ti, **BRAZOS['MAPA']); r0 = M.run(s, T=Ti, **BRAZOS['REL'])
        out.append(('(3) MAPA != REL y el mapa recibe sitios (DEBE diferir; ERR-38)', N(r1) != N(r0) and r1['sitios_leidos'] > 0, f"sitios leidos {r1['sitios_leidos']} · lect_div {r1['f9']['lect_div']}"))
        p1 = M.run(s, T=Ti, **BRAZOS['PLACEBO']); p0 = M.run(s, T=Ti, **BRAZOS['NADA'])
        out.append(('(4) PLACEBO != NADA (el nulo exacto consume el rng)', N(p1) != N(p0), f"R0 {p1['descendientes']}/{p1['deaths']+1} vs {p0['descendientes']}/{p0['deaths']+1}"))
    return out


# ------------------------------------------------------------------ humo (UN proceso, 6 corridas, ESCRIBE su JSON)
HUMO_CORRIDAS = [('NADA', 1), ('MAPA', 1), ('REL', 1), ('INMORTAL', 1), ('NODO_BARAJADO', 1), ('MAPA', 2)]


def humo(Ti=T):
    os.makedirs(HUMO, exist_ok=True)
    sel = sello(); pre = 'mundo_fase10_humo'
    LOG[0] = open(os.path.join(HUMO, f"{pre}_{sel}.log"), 'w', encoding='utf-8')
    t0 = time.time()
    log(f"HUMO MUNDO FASE 10 · {time.strftime('%Y-%m-%d %H:%M:%S')} · UN proceso, sin Pool (regla 3) · T={Ti} · {len(HUMO_CORRIDAS)} corridas (semillas YA VISTAS 1, 2)")
    log(f"  mundo_fase10.py sha {h16(os.path.join(AQUI,'mundo_fase10.py'))} · runner {h16(os.path.abspath(__file__))} · origen f9 "
        f"{h16(os.path.join(JUACO,'experimentos','nivel09_cuerpo_nuevo','organismo_f9.py'))} (se espera {SHA_ESPERADOS['f9']}) · v142 "
        f"{h16(os.path.join(JUACO,'organismo','organismo_v142.py'))} (se espera {SHA_ESPERADOS['v142']})")
    log(f"  MUNDO = {json.dumps(MUNDO, sort_keys=True)}\n  MAPA = {json.dumps(MAPA, sort_keys=True)}\n  CUERPO = {json.dumps(CUERPO, sort_keys=True, default=str)}")
    log("\nETAPA 1/3 -- identidad dentro del runner (regla 14, ERR-38)")
    ide = identidad_corta(20000, (1,))
    for et, ok, det in ide:
        log(f"  {'OK   ' if ok else 'FALLA'} {et}   {det}")
    if not all(ok for _, ok, _ in ide):
        log("  IDENTIDAD FALLA -> el humo NO sigue.")
        json.dump(dict(identidad=[[e, bool(o), d] for e, o, d in ide], ok=False), open(os.path.join(HUMO, f"{pre}_{sel}.json"), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return 1
    log(f"\nETAPA 2/3 -- {len(HUMO_CORRIDAS)} corridas")
    R = []
    for b, s in HUMO_CORRIDAS:
        x = tarea((b, s, Ti)); R.append(x)
        log(f"  [{time.time()-t0:6.1f}s] {b:14s} s{s}  R0 {x['R0']:<7} r {x['r']:<5} vida {x['vida_med']:<7} cuerpos {x['cuerpos']:<4} fund {x['fundadores']} "
            f"mnec {x['muertes_nec']} J {x['J']} sac {x['sac_frac']} gen_max {x['gen_max']} g5 {x['n_gen5']} cob_g1 {x['cob_g1']} cob_g5 {x['cob_g5']} lin_g5 {x['lin_g5']} "
            f"agot {x['agotados']} vida_sitio {x['vida_sitio']} alias {x['alias_frac']} camb {x['n_cambios']} sit_leidos {x['sitios_leidos']} celdas {x['celdas']} divB5 {x['des_splits']} coh {x['coherente']}")
    log("\nETAPA 3/3 -- predicciones del humo (HH1..HH6; escritas en el PREREGISTRO §6 ANTES de correrlo)")
    g = lambda b, s: next(x for x in R if x['brazo'] == b and x['seed'] == s)
    hh = {}
    hh['HH1 ancla: NADA s1 R0 en [0.05, 0.45] e INMORTAL s1 en [0.5, 2.0] (rango ancho: una semilla)'] = dentro(g('NADA', 1)['R0'], 0.05, 0.45) and dentro(g('INMORTAL', 1)['R0'], 0.5, 2.0)
    hh['HH2 el mundo se agota: sitios agotados > 0 y vida mediana de un sitio <= T/4 en las 6 corridas'] = all(x['agotados'] and x['agotados'] > 0 and le(x['vida_sitio'], Ti / 4) for x in R)
    hh['HH3 MAPA vive mas que NADA (s1) y su R0 es mayor'] = g('MAPA', 1)['vida_med'] > g('NADA', 1)['vida_med'] and g('MAPA', 1)['R0'] > g('NADA', 1)['R0']
    hh['HH4 MAPA > REL en R0 (s1): saber DONDE aporta sobre saber QUE'] = g('MAPA', 1)['R0'] > g('REL', 1)['R0']
    hh['HH5 MAPA > NODO_BARAJADO en R0 (s1): es el contenido'] = g('MAPA', 1)['R0'] > g('NODO_BARAJADO', 1)['R0']
    hh['HH6 instrumento: contabilidad OK en todas; sitios_leidos > 0 y lect_div > 0 en MAPA; alias_frac > 0 en NADA'] = (all(x['coherente'] for x in R if x['coherente'] is not None)
        and all(x['sitios_leidos'] > 0 and (x['lect_div'] or 0) > 0 for x in R if x['brazo'] == 'MAPA') and (g('NADA', 1)['alias_frac'] or 0) > 0)
    for k, v in hh.items():
        log(f"  {'SI' if v else 'NO'}  {k}")
    log("  Solo HH2 y HH6 BLOQUEAN (son el mundo y el instrumento). HH1 es el ancla con una semilla (se reporta). HH3-HH5 son la HIPOTESIS: si caen,")
    log("  se escriben en el preregistro y la serie corre con esta letra. NINGUN umbral se cambia despues del humo (regla 4).")
    ruta = os.path.join(HUMO, f"{pre}_{sel}.json")
    json.dump(dict(bloque='mundo_fase10_humo', sello=sel, T=Ti, corridas_humo=HUMO_CORRIDAS, MUNDO=MUNDO, MAPA=MAPA, CUERPO=N(CUERPO),
                   sha_mundo=h16(os.path.join(AQUI, 'mundo_fase10.py')), sha_runner=h16(os.path.abspath(__file__)), sha_origen=SHA_ESPERADOS,
                   identidad=[[e, bool(o), d] for e, o, d in ide], corridas=R, HH={k: bool(v) for k, v in hh.items()},
                   ok=bool(list(hh.values())[1] and list(hh.values())[5]), seg=round(time.time() - t0, 1),
                   python=platform.python_version()),
              open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    j, _ = lee_json(HUMO, pre, sel)   # ERR-42: el humo ABRE el JSON que escribio
    log(f"\nJSON  {ruta}  (sha {h16(ruta)}; releido: {len(j['corridas'])} corridas)")
    log(f"HUMO terminado en {time.time()-t0:.1f}s")
    return 0 if j['ok'] else 1


# ------------------------------------------------------------------ la serie (SOLO el coordinador)
def serie(desde, n, Ti, pool, brazos, etiqueta):
    from multiprocessing import Pool
    os.makedirs(DATOS, exist_ok=True)
    sel = sello(); pre = f"mundo_fase10_s{desde}-{desde+n-1}{etiqueta}"
    LOG[0] = open(os.path.join(DATOS, f"{pre}_{sel}.log"), 'w', encoding='utf-8')
    t0 = time.time(); SEEDS = list(range(desde, desde + n))
    tareas = [(b, s, Ti) for b in brazos for s in SEEDS]
    log(f"MUNDO FASE 10 · {time.strftime('%Y-%m-%d %H:%M:%S')} · semillas {SEEDS[0]}-{SEEDS[-1]} · {len(brazos)} brazos x {n} = {len(tareas)} corridas de T={Ti} · Pool {pool} (ERR-86)")
    log(f"  mundo_fase10.py sha {h16(os.path.join(AQUI,'mundo_fase10.py'))} · runner {h16(os.path.abspath(__file__))} · preregistro {h16(os.path.join(AQUI,'PREREGISTRO_mundo_fase10.md'))}")
    log("\nETAPA 1/3 -- identidad dentro del runner")
    ide = identidad_corta(20000, (1, 2))
    for et, ok, det in ide:
        log(f"  {'OK   ' if ok else 'FALLA'} {et}   {det}")
    if not all(ok for _, ok, _ in ide):
        raise SystemExit("IDENTIDAD FALLA: la serie NO se corre.")
    log("\nETAPA 2/3 -- series")
    with Pool(pool) as P:
        R = []
        for i, x in enumerate(P.imap_unordered(tarea, tareas), 1):
            R.append(x)
            if i % max(1, len(tareas) // 20) == 0:
                log(f"  [{time.time()-t0:6.1f}s] {i}/{len(tareas)}")
    crudo = os.path.join(DATOS, f"{pre}_{sel}.json")   # ERR-54: el crudo ANTES de analizar
    json.dump(dict(bloque='mundo_fase10', sello=sel, desde=desde, n=n, T=Ti, brazos=brazos, MUNDO=MUNDO, MAPA=MAPA, CUERPO=N(CUERPO),
                   sha_mundo=h16(os.path.join(AQUI, 'mundo_fase10.py')), sha_runner=h16(os.path.abspath(__file__)), sha_origen=SHA_ESPERADOS,
                   sha_prereg=h16(os.path.join(AQUI, 'PREREGISTRO_mundo_fase10.md')), identidad=[[e, bool(o), d] for e, o, d in ide],
                   umbrales=UMBRALES, corridas=R), open(crudo, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"  CRUDO {crudo} (sha {h16(crudo)})")
    log("\nETAPA 3/3 -- LAS PUERTAS (ERR-89: una linea por puerta)")
    V = puertas(R)
    log("\nTABLA (mediana por brazo)")
    log(f"  {'brazo':17s} {'R0':>6} {'r':>6} {'vida':>7} {'cuerpos':>7} {'fund':>5} {'J':>6} {'sac':>6} {'expos':>6} {'gmax':>5} {'g5':>4} {'cob1':>6} {'cob5':>6} {'lin5':>6} {'celdas':>6}")
    for b in brazos:
        log(f"  {b:17s} {str(m(R,b,'R0')):>6} {str(m(R,b,'r')):>6} {str(m(R,b,'vida_med')):>7} {str(m(R,b,'cuerpos')):>7} {str(m(R,b,'fundadores')):>5} {str(m(R,b,'J')):>6} "
            f"{str(m(R,b,'sac_frac')):>6} {str(m(R,b,'exposiciones')):>6} {str(m(R,b,'gen_max')):>5} {str(m(R,b,'n_gen5')):>4} {str(m(R,b,'cob_g1')):>6} {str(m(R,b,'cob_g5')):>6} {str(m(R,b,'lin_g5')):>6} {str(m(R,b,'celdas')):>6}")
    ver = os.path.join(DATOS, f"{pre}_veredicto_{sel}.json")
    json.dump(dict(sello=sel, crudo=os.path.basename(crudo), sha_crudo=h16(crudo), sha_mundo=h16(os.path.join(AQUI, 'mundo_fase10.py')), puertas=V,
                   pasan=[k for k, v in V.items() if v['pasa']], caen=[k for k, v in V.items() if v['pasa'] is False], na=[k for k, v in V.items() if v['pasa'] is None]),
              open(ver, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\nPUERTAS QUE PASAN: {[k for k,v in V.items() if v['pasa']]}\nPUERTAS QUE CAEN : {[k for k,v in V.items() if v['pasa'] is False]}\nNO EVALUABLES: {[k for k,v in V.items() if v['pasa'] is None]}")
    log(f"VEREDICTO {ver} (sha {h16(ver)})\nTerminado en {time.time()-t0:.1f}s")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--serie', action='store_true')
    ap.add_argument('--desde', type=int, default=DESDE)
    ap.add_argument('--n', type=int, default=N_SEM)
    ap.add_argument('--T', type=int, default=T)
    ap.add_argument('--pool', type=int, default=int(os.environ.get('JUACO_POOL', 6)))   # ERR-86
    ap.add_argument('--brazos', default=','.join(ORDEN))
    ap.add_argument('--etiqueta', default='')
    a = ap.parse_args()
    if a.humo:
        return humo(a.T)
    if a.serie:
        return serie(a.desde, a.n, a.T, a.pool, [b for b in a.brazos.split(',') if b], a.etiqueta)
    ap.print_help(); return 2


if __name__ == '__main__':
    sys.exit(main())
