"""FASE 9, BLOQUE 2 — "leer llena la memoria; morder abre la puerta" + F9-4bis (J balanceado, ERR-93).

MISION: llegar a la AGI por este camino — organismo minimo, reglas locales, sin retropropagacion,
peldanos preregistrados con controles y replicas. El bloque 1 dejo medido que el cuerpo nuevo que lee
el nodo por relevancia rechaza lo malo en su primer encuentro sin dejar de comer (p1 0.96 contra 0.19)
y vive 6x mas, pero NINGUN brazo cruza R0 0.9: H-1 y ERR-62 siguen en pie. El bloque 2 mide (a) si
llenar la via rapida sin abrir la puerta compra vida, (b) la letra balanceada de F9-4 (J = p1+c1-1)
con el brazo CAUTELA que puede tumbarla, y (c) el NODO ORACULO como cota superior: si ni el oraculo
cruza R0 0.9, el muro es el MUNDO y no la herencia.

Ejecuta PREREGISTRO_bloque2.md. Instrumento organismo_f9c.py (por anclas desde organismo_f9.py
3a821884394d66c9 + las inserciones de organismo_f9b.py 6a57e9fa9514099b; cadena hasta el TRONCO
CONGELADO organismo/organismo_v14.py v14.1 feefc88b1fd8d434). Construido por construye_f9c.py.

    python experimentos/nivel09_cuerpo_nuevo_b2/corre_bloque2.py --humo        (UN proceso, 6 corridas: el disenador)
    python experimentos/nivel09_cuerpo_nuevo_b2/corre_bloque2.py --desde 1581  (LA SERIE: solo el COORDINADOR, con Pool)
    python experimentos/nivel09_cuerpo_nuevo_b2/corre_bloque2.py --desde 1601  (REPLICA, regla 12)

POOL (ERR-86): el tamano sale de --pool o de la variable de entorno JUACO_POOL; por defecto 6. Los
agentes no corren Pool (regla 3 de EQUIPO.md): --humo si.

ERR-89 (una puerta que el runner no imprime NO EXISTE): hay EXACTAMENTE una linea por cada puerta del
preregistro (F9-1, F9-2, F9-3, F9-4bis, F9-5, F9-6, F9-8, F9-9, F9-10, B2-1..B2-5) con su frase, su
umbral y su PASA/CAE, mas la linea REPORTADA de B2-CAUT y la de F9-7 (caida x3, se reporta, no juzga).
ERR-31: los umbrales de UMBRALES son los del preregistro, no los de ninguna bateria.
ERR-54: el crudo se guarda ANTES de analizar nada.  ERR-87: lee_json exige prefijo + SELLO EXACTO.
ERR-92: el rango del ancla F9-1 se recalibro con las CINCO series existentes de NADA (ver preregistro).
ERR-93: F9-4bis (J = p1 + c1 - 1) es letra NUEVA; F9-4 original NO se rejuzga.
Regla 14: `regla14()` compara CAMPO A CAMPO las ocho celdas heredadas contra corre_f9.BRAZOS y aborta
si algo difiere (aparte de las perillas nuevas declaradas).

LOS CATORCE BRAZOS (x 2 niveles de rep_acum = 28 celdas)
  RENACE     ancla con sha: el inmortal subsidiado (muerte_real=0).
  NADA       muerte real, sin nodo: es NADA_CM de H-1 cuerpo a cuerpo.
  M1         la mejor herencia de H-1 (el vector), sin nodo.
  REC        nodo por recencia (para F9-5).
  REL        el candidato del bloque 1 (relevancia viva, nodo_via=0).
  REL2b      EL CANDIDATO DE HOY: nodo_via=2 -- leer llena la via rapida y NO abre la puerta.
  REL2       nodo_via=1 -- el FALLO YA MEDIDO por C (vida 0.38x): se corre para que quede en el registro.
  REL2b_BAR  control de CONTENIDO del candidato (nodo barajado).
  REL_BAR    control de CONTENIDO del bloque 1 (la mitad de F9-4bis).
  CAUTELA    nodo APAGADO + empujon negativo constante en la boca, calibrado en el humo para igualar
             c1(REL_BAR). El brazo que puede TUMBAR el diagnostico "nodo barajado = cautela generica".
  DOSIS      REL con eta_s al DOBLE: el control que puede fallar de B2-3 (cantidad, no dos vias).
  ORACULO    nodo_or=1: el contenido es la TABLA VERDADERA. Cota superior de la herencia (voto de A).
  REL_FIJO   ranking congelado (para F9-10).
  REL_AZAR   control de acceso (para F9-6).
REL_TARDE NO se corre: F9-7 cayo en las TRES series del bloque 1 (A12 0.43/0.53/0.63, contraste
interno 9/20, 7/20, 5/20). Se declara refutada y no se rejuzga (regla 3); se dice en el log.

VOCABULARIO (regla 6): "cuerpo", "linaje", "nodo del linaje", "exposicion sin consecuencia", "R0 del
linaje", "rechaza lo malo en su primer encuentro", "indice de discriminacion J". NO se dice "ensena",
"cultura", "poblacion", "generacion", "evoluciona", "recuerda su vida pasada", "quiere".
"""
import argparse, hashlib, json, os, platform, re, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N09 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo')
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
sys.path[:0] = [AQUI, N09, N13, N11, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import corre_vivo_rep as C1        # med, A12, razon, N, h16: NO se copian
import corre_f9 as CF              # CUERPO, NODO, curita_f, resumen, ORDEN: NO se copian (regla 14 por construccion)
import organismo_f9c as F9C

med, A12, razon, N, h16 = C1.med, C1.A12, C1.razon, C1.N, C1.h16

T = 100000
T_HUMO = 100000
N_SEM = 20
DESDE = 1581
DATOS = os.path.join(RAIZ, 'datos')
HUMO = os.path.join(DATOS, 'humo')
SHA_ESPERADOS = dict(v14='feefc88b1fd8d434', vivo='20c0961c79de8825', rep='aa823d56c2d4213c',
                     rep2='96feb4918dc5d694', h1='9e99ff87b5e2db1e', alma='7c09cec391daa879',
                     alma2='4fd616aeaf535e61', f9='3a821884394d66c9', f9b='6a57e9fa9514099b')

# ------------------------------------------------------------------ EL CUERPO (regla 14: campo a campo)
# Se REUSAN los objetos de corre_f9.py: el cuerpo y el nodo son los MISMOS, constante por constante.
CUERPO = CF.CUERPO                 # CUELLO_MIN + MED2 + h1 + muerte_real + hereda='nada' + dote=0.6
NODO = dict(CF.NODO, f9c=1)        # alma nula + f9=1 + nodo_k=20 + nodo_lee=50, MAS las medidas pa/pn (SOLO LECTURA)
ETA_S_TRONCO = 0.15                # el valor del tronco v14.1 (default de organismo_f9c.run); DOSIS lo dobla

# CAUTELA: empujon NEGATIVO constante en la boca, SIN informacion (el brazo CONST de C-P1).
# CALIBRACION (regla escrita en el PREREGISTRO ANTES del humo, sec. 5 "B2-CAUT"): el humo corre la
# rejilla CAUT_GRID y c* = el valor que iguala c1(REL_BAR); si los dos puntos BRACKETEAN el objetivo,
# c* = interpolacion lineal redondeada a 0.1; si no, el mas cercano, y la brecha se declara.
CAUT_GRID = (-1.2, -2.0)
# FIJADO POR EL HUMO datos/humo/f9c_humo_20260921_171730.json (sha 49297b630c9ae46f), s=1, acum=1, T=100000:
#   c1(REL_BAR) = 0.5897 ; c1(CAUTELA, c=-1.2) = 0.6596 ; c1(CAUTELA, c=-2.0) = 0.1161 -> BRACKET, y la
#   interpolacion lineal de la regla del preregistro da -1.2 + (-0.8)*(0.6596-0.5897)/(0.6596-0.1161) = -1.3.
# La serie vuelve a comprobar la calibracion: si |c1(CAUTELA) - c1(REL_BAR)| > 0.10, B2-CAUT NO se lee y NO
# se recalibra (regla 3). El valor -1.3 no se corrio en el humo: se declara en el informe.
C_CAUT = -1.3

BRAZOS = {
    'RENACE':    dict(CUERPO, muerte_real=0, hereda='nada'),                                   # sin alma: f9/f9c no aplican
    'NADA':      dict(CUERPO, **NODO, nodo=0, conectado=0),
    'M1':        dict(CUERPO, hereda='M1', **NODO, nodo=0, conectado=0),
    'REC':       dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=0),
    'REL':       dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=1),
    'REL2b':     dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=1, nodo_via=2),
    'REL2':      dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=1, nodo_via=1),
    'REL2b_BAR': dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=1, nodo_via=2, nodo_baraja=1),
    'REL_BAR':   dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=1, nodo_baraja=1),
    'CAUTELA':   dict(CUERPO, **NODO, nodo=0, conectado=0, sesgo_fijo=C_CAUT),
    'DOSIS':     dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=1, eta_s=2 * ETA_S_TRONCO),
    'ORACULO':   dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=1, nodo_via=2, nodo_or=1),
    'REL_FIJO':  dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=3),
    'REL_AZAR':  dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=2),
}
ORDEN = ['RENACE', 'NADA', 'M1', 'REC', 'REL', 'REL2b', 'REL2', 'REL2b_BAR', 'REL_BAR',
         'CAUTELA', 'DOSIS', 'ORACULO', 'REL_FIJO', 'REL_AZAR']
ACUM = [0, 1]
# Las ocho celdas HEREDADAS del bloque 1: tienen que ser corre_f9.BRAZOS[b] + las perillas nuevas apagadas.
HEREDADOS = ('RENACE', 'NADA', 'M1', 'REC', 'REL', 'REL_BAR', 'REL_FIJO', 'REL_AZAR')
NUEVAS_PERILLAS = ('nodo_via', 'nodo_or', 'sesgo_fijo', 'f9c')


# ------------------------------------------------------------------ LA LETRA DEL PREREGISTRO (ERR-31)
# F9-1: ERR-92 + recalibrado del bloque 2. Regla DECLARADA: rango = [0.75*min, 1.25*max] sobre TODAS
# las series existentes de esa cantidad (aditivo si la cantidad cruza el cero), UNIDO al rango vigente
# (nunca se estrecha lo ya declarado y superado). Cinco series de NADA: vida 125, 119, 94.0, 88.5, 95.5;
# R0 0.148, 0.140, 0.141, 0.130, 0.142; RENACE R0 1.03, 0.96, 0.804, 1.0, 0.92; r +3, -2, -15.5, +1.0, -5.0.
UMBRALES = {
    'F9-1': dict(frase="ANCLA (BLOQUEANTE): el instrumento no se movio -- NADA reproduce NADA_CM de H-1 y "
                       "RENACE reproduce el inmortal del bloque 2 (rango recalibrado con las CINCO series, ERR-92/93)",
                 R0_NADA=(0.097, 0.22), vida_NADA=(66.0, 170.0), R0_RENACE=(0.60, 1.40), r_RENACE=(-50.0, 25.0)),
    'F9-2': dict(frase="EL NODO POR RELEVANCIA ALARGA LA VIDA DEL CUERPO NUEVO (heredada, misma letra)",
                 razon_vida=2.5, A12_vida=0.85),
    'F9-3': dict(frase="MENOS DE UNA VIDA: el recien nacido RECHAZA lo malo en su PRIMER encuentro y NO a "
                       "costa de dejar de comer (heredada, misma letra)",
                 p1_REL=0.60, dif_p1=0.30, A12_p1=0.85, c1_margen=0.10, sac_margen=0.95),
    'F9-4bis': dict(frase="CONTENIDO, NO CAUTELA GENERICA -- con el indice BALANCEADO J = p1 + c1 - 1 (ERR-93; "
                          "F9-4 original NO se rejuzga)",
                    A12_J=0.85, J_margen=0.10, A12_vida=0.80),
    'F9-5': dict(frase="RELEVANCIA > RECENCIA (las lecciones no expiran) (heredada, misma letra)",
                 A12_vida=0.65, razon_R0=1.15),
    'F9-6': dict(frase="RANKEAR, NO SOLO ACCEDER (heredada, misma letra)", A12_vida=0.65),
    'F9-8': dict(frase="REPRODUCCION DESACOPLADA DE LA SACIEDAD (perilla APARTE) (heredada, misma letra)",
                 razon_R0_NADA=1.30, spearman=0.80, R0_cierre=0.90, fund_cierre=2),
    'F9-9': dict(frase="SEGURIDAD: contabilidad, las perillas NO son inertes (ERR-38) y el mundo no se comio "
                       "la comida (heredada + las tres pruebas del mecanismo nuevo)",
                 frac_div=0.50, exp_min=0.50, exentos=('REL_FIJO', 'CAUTELA')),
    'F9-10': dict(frase="LA RELEVANCIA VIVA NO ES MIEDO A TODO (heredada, misma letra)",
                  p1_fijo=0.60, razon_R0=1.15, A12_sac=0.65),
    'B2-1': dict(frase="LEER LLENA LA MEMORIA, MORDER ABRE LA PUERTA: el candidato vive mas que REL y NO "
                       "pierde discriminacion (no volvio la sustitucion)",
                 razon_vida=1.10, dJ=0.03),
    'B2-2': dict(frase="R0 DEL LINAJE con la reproduccion desacoplada: el candidato con acum=1",
                 R0_min=0.50, R0_rango=(0.50, 0.80), R0_cierre=0.90, fund_cierre=2),
    'B2-3': dict(frase="DOSIS (REL con eta_s al DOBLE) NO iguala al candidato: lo que paga son las DOS VIAS, "
                       "no la cantidad de aprendizaje (SOLO SE LEE si B2-1 pasa)",
                 A12_vida=0.70, razon_R0=1.10),
    'B2-4': dict(frase="EL FALLO MEDIDO SE REPRODUCE EN SEMILLAS NUEVAS: nodo_via=1 (REL2) acorta la vida a "
                       "~0.38x REL y hunde J (la puerta de v14 SUSTITUYE, no suma)",
                 razon=(0.25, 0.55), dJ=0.10),
    'B2-5': dict(frase="NODO ORACULO como COTA SUPERIOR (voto de A): (i) cordura de la cota; (ii) se REPORTA "
                       "si ni el oraculo cruza R0 0.9 -- entonces el muro es el MUNDO, no la herencia",
                 dR0=0.02, razon_vida=0.95, R0_cierre=0.90, fund_cierre=2),
}
# B2-CAUT: NO es puerta de paso/caida; es el control que puede REFUTAR el diagnostico de C.
CAUT_VIDA_TOL = 0.25     # |vida(CAUTELA)/vida(REL_BAR) - 1| <= 0.25
CAUT_J_TOL = 0.10        # |J(CAUTELA) - J(REL_BAR)| <= 0.10
CAUT_C1_TOL = 0.10       # calibracion valida en la serie: |c1(CAUTELA) - c1(REL_BAR)| <= 0.10


# ------------------------------------------------------------------ utilidades
LOG = [None]


def log(msg=""):
    print(msg, flush=True)
    if LOG[0]:
        LOG[0].write(msg + "\n"); LOG[0].flush(); os.fsync(LOG[0].fileno())


def sello():
    return time.strftime('%Y%m%d_%H%M%S')


def lee_json(carpeta, prefijo, sel):
    """ERR-87: prefijo + SELLO EXACTO. Sin sello no se lee nada (no se adivina el 'ultimo')."""
    if not re.fullmatch(r'\d{8}_\d{6}', sel or ''):
        raise SystemExit(f"lee_json: sello {sel!r} invalido (se exige AAAAMMDD_HHMMSS, ERR-87)")
    ruta = os.path.join(carpeta, f"{prefijo}_{sel}.json")
    if not os.path.exists(ruta):
        raise SystemExit(f"lee_json: no existe {ruta} (prefijo + sello EXACTO, ERR-87)")
    return json.load(open(ruta, encoding='utf-8')), ruta


def ge(x, u):
    return x is not None and x >= u


def le(x, u):
    return x is not None and x <= u


def dentro(x, lo, hi):
    return x is not None and lo <= x <= hi


def spearman(a, b):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v)
        for p, i in enumerate(o):
            r[i] = p
        return r
    if len(a) < 3:
        return None
    ra, rb = rk(a), rk(b); n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** .5
    return round(num / den, 3) if den else None


# ------------------------------------------------------------------ REGLA 14 (campo a campo, ERR-38)
def regla14(log=log):
    """Las ocho celdas HEREDADAS tienen que ser corre_f9.BRAZOS[b] campo a campo, mas las perillas
    nuevas APAGADAS (y f9c=1, que es SOLO LECTURA y el arnes lo prueba en el caso K). Si algo mas
    difiere, la serie NO se corre: un brazo heredado con una constante movida no es el brazo heredado."""
    filas, malo = [], []
    for b in HEREDADOS:
        a, n = CF.BRAZOS[b], BRAZOS[b]
        falta = [k for k in a if k not in n]
        dif = [k for k in a if k in n and a[k] != n[k]]
        extra = [k for k in n if k not in a and k not in NUEVAS_PERILLAS]
        enc = [k for k in NUEVAS_PERILLAS if n.get(k) not in (None, 0, 0.0) and k != 'f9c']
        ok = not (falta or dif or extra or enc)
        filas.append((b, len(a), ok, f"falta {falta} dif {dif} extra {extra} perillas encendidas {enc}"))
        if not ok:
            malo.append(b)
    for b, nc, ok, det in filas:
        log(f"  {'OK  ' if ok else 'FALLA'} regla14 {b:10s} {nc} campos identicos a corre_f9.BRAZOS   {det}")
    if malo:
        raise SystemExit(f"REGLA 14: celdas heredadas que NO coinciden con corre_f9: {malo}. La serie NO se corre.")
    return filas


# ------------------------------------------------------------------ una corrida
def resumen(brazo, seed, acum, r, Ti):
    """Todo de SOLO LECTURA. Se REUSA corre_f9.resumen (misma definicion de R0, vidas y contabilidad)
    y se le anaden J (el indice balanceado de F9-4bis) y las medidas del bloque 2."""
    o = CF.resumen(brazo, seed, acum, r, Ti)
    f = r.get('f9') or {}
    o['J'] = (round(o['p1'] + o['c1'] - 1.0, 4) if (o['p1'] is not None and o['c1'] is not None) else None)
    o['via_msg'] = f.get('via_msg')
    fn = f.get('fam_nac') or []
    o['fam_nac'] = (round(sum(fn) / len(fn), 3) if fn else None)
    o['fam_nac_max'] = (max(fn) if fn else None)
    o['pa'] = f.get('pa'); o['pn'] = f.get('pn')
    o['frac_pa'] = razon(f.get('pa'), f.get('pn'))
    o['nodo_via'] = f.get('nodo_via', 0)
    o['sesgo_fijo'] = r.get('sesgo_fijo')
    return o


def tarea(args):
    brazo, seed, acum, Ti, extra = args
    kw = dict(BRAZOS[brazo], rep_acum=acum, **(extra or {}))
    t0 = time.time()
    r = F9C.run(seed, T=Ti, **kw)
    o = resumen(brazo, seed, acum, r, time.time() - t0)
    if extra:
        o['extra'] = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in extra.items()}
    return o


# ------------------------------------------------------------------ las puertas (ERR-89: una linea por puerta)
def cel(R, brazo, acum, campo):
    return [x[campo] for x in R if x['brazo'] == brazo and x['acum'] == acum and x[campo] is not None]


def m(R, brazo, acum, campo):
    return med(cel(R, brazo, acum, campo))


def puertas(R, log=log):
    V, U = {}, UMBRALES

    def linea(p, ok, txt):
        V[p] = dict(pasa=bool(ok), detalle=txt, frase=U[p]['frase'])
        log(f"  {p:8s} {'PASA' if ok else 'CAE '}  {U[p]['frase']}")
        log(f"          {txt}")

    def nota(p, txt, frase):
        V[p] = dict(pasa=None, detalle=txt, frase=frase)
        log(f"  {p:8s} ----  {frase}")
        log(f"          {txt}")

    u = U['F9-1']
    a = dict(R0_NADA=m(R, 'NADA', 0, 'R0'), vida_NADA=m(R, 'NADA', 0, 'vida_med'),
             R0_RENACE=m(R, 'RENACE', 0, 'R0'), r_RENACE=m(R, 'RENACE', 0, 'r'))
    linea('F9-1', all(dentro(a[k], *u[k]) for k in a),
          " · ".join(f"{k} {a[k]} en [{u[k][0]}, {u[k][1]}]" for k in a))

    u = U['F9-2']
    rv = razon(m(R, 'REL', 0, 'vida_med'), m(R, 'NADA', 0, 'vida_med'))
    av = A12(cel(R, 'REL', 0, 'vida_med'), cel(R, 'NADA', 0, 'vida_med'))
    linea('F9-2', ge(rv, u['razon_vida']) and ge(av, u['A12_vida']),
          f"vida REL {m(R,'REL',0,'vida_med')} / NADA {m(R,'NADA',0,'vida_med')} = {rv} (>= {u['razon_vida']}) · "
          f"A12 {av} (>= {u['A12_vida']})")

    u = U['F9-3']
    p_rel, p_nada = m(R, 'REL', 0, 'p1'), m(R, 'NADA', 0, 'p1')
    c_rel, c_nada = m(R, 'REL', 0, 'c1'), m(R, 'NADA', 0, 'c1')
    ap = A12(cel(R, 'REL', 0, 'p1'), cel(R, 'NADA', 0, 'p1'))
    s_rel, s_nada = m(R, 'REL', 0, 'sac_frac'), m(R, 'NADA', 0, 'sac_frac')
    bal = (c_rel is not None and c_nada is not None and c_rel >= c_nada - u['c1_margen']
           and s_rel is not None and s_nada is not None and s_rel >= s_nada * u['sac_margen'])
    linea('F9-3', (ge(p_rel, u['p1_REL']) and p_nada is not None and ge(p_rel - p_nada, u['dif_p1'])
                   and ge(ap, u['A12_p1']) and bal),
          f"p1 REL {p_rel} vs NADA {p_nada} (>= {u['p1_REL']}, dif >= {u['dif_p1']}, A12 {ap} >= {u['A12_p1']}) · "
          f"BALANCE: c1 {c_rel} vs {c_nada} (>= NADA-{u['c1_margen']}) y saciedad {s_rel} vs {s_nada} "
          f"(>= {u['sac_margen']}x): {'si' if bal else 'NO'}")

    # ---- F9-4bis (ERR-93): el indice BALANCEADO. J = p1 + c1 - 1 POR CORRIDA, no J de medianas.
    u = U['F9-4bis']
    J_rel, J_bar, J_nada = m(R, 'REL', 0, 'J'), m(R, 'REL_BAR', 0, 'J'), m(R, 'NADA', 0, 'J')
    aJ = A12(cel(R, 'REL', 0, 'J'), cel(R, 'REL_BAR', 0, 'J'))
    ab = A12(cel(R, 'REL', 0, 'vida_med'), cel(R, 'REL_BAR', 0, 'vida_med'))
    ok4 = (ge(aJ, u['A12_J']) and J_bar is not None and J_nada is not None
           and J_bar <= J_nada + u['J_margen'] and ge(ab, u['A12_vida']))
    linea('F9-4bis', ok4,
          f"J REL {J_rel} · J REL_BAR {J_bar} (<= J NADA {J_nada} + {u['J_margen']}) · "
          f"A12(J REL > REL_BAR) {aJ} (>= {u['A12_J']}) · A12(vida REL > REL_BAR) {ab} (>= {u['A12_vida']}) · "
          f"p1/c1 REL_BAR {m(R,'REL_BAR',0,'p1')}/{m(R,'REL_BAR',0,'c1')} (la cautela generica sube p1 y hunde c1)")

    u = U['F9-5']
    a5 = A12(cel(R, 'REL', 0, 'vida_med'), cel(R, 'REC', 0, 'vida_med'))
    r5 = razon(m(R, 'REL', 0, 'R0'), m(R, 'REC', 0, 'R0'))
    linea('F9-5', ge(a5, u['A12_vida']) and ge(r5, u['razon_R0']),
          f"A12(vida REL > REC) {a5} (>= {u['A12_vida']}) · R0 REL {m(R,'REL',0,'R0')} / REC {m(R,'REC',0,'R0')} = {r5} (>= {u['razon_R0']})")

    u = U['F9-6']
    a6 = A12(cel(R, 'REL', 0, 'vida_med'), cel(R, 'REL_AZAR', 0, 'vida_med'))
    linea('F9-6', ge(a6, u['A12_vida']),
          f"A12(vida REL > REL_AZAR) {a6} (>= {u['A12_vida']}) · vida REL_AZAR {m(R,'REL_AZAR',0,'vida_med')}")

    u = U['F9-8']
    r8 = razon(m(R, 'NADA', 1, 'R0'), m(R, 'NADA', 0, 'R0'))
    br = [b for b in ORDEN if cel(R, b, 0, 'R0') and cel(R, b, 1, 'R0')]
    sp = spearman([m(R, b, 0, 'R0') for b in br], [m(R, b, 1, 'R0') for b in br])
    cierre = [(b, ac, m(R, b, ac, 'R0'), m(R, b, ac, 'fundadores')) for b in ORDEN for ac in ACUM
              if b != 'RENACE' and ge(m(R, b, ac, 'R0'), u['R0_cierre']) and le(m(R, b, ac, 'fundadores'), u['fund_cierre'])]
    linea('F9-8', ge(r8, u['razon_R0_NADA']) and ge(sp, u['spearman']),
          f"R0 NADA acum1 {m(R,'NADA',1,'R0')} / acum0 {m(R,'NADA',0,'R0')} = {r8} (>= {u['razon_R0_NADA']}) · "
          f"Spearman del orden entre niveles {sp} (>= {u['spearman']}, {len(br)} brazos) · CLAUSULA H1-6 "
          f"(R0 >= {u['R0_cierre']} con fundadores <= {u['fund_cierre']}): "
          f"{cierre if cierre else 'NINGUN brazo -- H-1 y ERR-62 siguen en pie'}")

    u = U['F9-9']
    coh = [x for x in R if x['coherente'] is False]
    flen = [x for x in R if x['f9_len'] is False]
    fd = m(R, 'REL', 0, 'frac_div')
    fd_rec = m(R, 'REC', 0, 'lect_div')
    eA = m(R, 'NADA', 0, 'exp_A')
    pobres = [(b, ac, m(R, b, ac, 'exp_A')) for b in ORDEN for ac in ACUM
              if b not in u['exentos'] and eA and m(R, b, ac, 'exp_A') is not None
              and m(R, b, ac, 'exp_A') < u['exp_min'] * eA]
    # las TRES pruebas del mecanismo nuevo (ERR-38: "inerte" se mide, no se supone)
    vm2b, vm2 = m(R, 'REL2b', 0, 'via_msg'), m(R, 'REL2', 0, 'via_msg')
    fn2b, fn2 = m(R, 'REL2b', 0, 'fam_nac_max'), m(R, 'REL2', 0, 'fam_nac')
    pa2b = m(R, 'REL2b', 0, 'frac_pa')
    mec = (ge(vm2b, 1) and fn2b == 0 and ge(fn2, 0.0001) and ge(pa2b, 0.0001))
    ok9 = (not coh and not flen and ge(fd, u['frac_div']) and fd_rec == 0 and not pobres and mec)
    linea('F9-9', ok9,
          f"contabilidad {len(R)-len(coh)}/{len(R)} · listas por cuerpo OK {len(R)-len(flen)}/{len(R)} · "
          f"frac_div REL {fd} (>= {u['frac_div']}) · lect_div REC {fd_rec} (= 0) · exposiciones A (ref NADA {eA}, "
          f"exentos {u['exentos']}) pobres {pobres if pobres else 'ninguna'} · MECANISMO NUEVO: via_msg REL2b {vm2b} "
          f"(> 0) · fam_nac_max REL2b {fn2b} (= 0: LEER NO ABRE LA PUERTA) · fam_nac REL2 {fn2} (> 0: con evidencia SI "
          f"la abre) · frac_pa REL2b {pa2b} (> 0: MORDER SI la abre) -> {'si' if mec else 'NO'}")

    u = U['F9-10']
    pf = m(R, 'REL_FIJO', 0, 'p1')
    r10 = razon(m(R, 'REL', 0, 'R0'), m(R, 'REL_FIJO', 0, 'R0'))
    a10 = A12(cel(R, 'REL', 0, 'sac_frac'), cel(R, 'REL_FIJO', 0, 'sac_frac'))
    linea('F9-10', ge(pf, u['p1_fijo']) and ge(r10, u['razon_R0']) and ge(a10, u['A12_sac']),
          f"REL_FIJO p1 {pf} (>= {u['p1_fijo']}) pero R0 REL {m(R,'REL',0,'R0')} / REL_FIJO "
          f"{m(R,'REL_FIJO',0,'R0')} = {r10} (>= {u['razon_R0']}) y A12(saciedad REL > REL_FIJO) {a10} (>= {u['A12_sac']})")

    # ------------------------------------------------ LAS PUERTAS NUEVAS DEL BLOQUE 2
    u = U['B2-1']
    v2b, vrel = m(R, 'REL2b', 0, 'vida_med'), m(R, 'REL', 0, 'vida_med')
    rv1 = razon(v2b, vrel)
    J2b, Jrel = m(R, 'REL2b', 0, 'J'), m(R, 'REL', 0, 'J')
    a1 = A12(cel(R, 'REL2b', 0, 'vida_med'), cel(R, 'REL', 0, 'vida_med'))
    ok_b1 = (ge(rv1, u['razon_vida']) and J2b is not None and Jrel is not None and J2b >= Jrel - u['dJ'])
    linea('B2-1', ok_b1,
          f"vida REL2b {v2b} / REL {vrel} = {rv1} (>= {u['razon_vida']}) · J REL2b {J2b} vs J REL {Jrel} "
          f"(>= REL - {u['dJ']}) · A12(vida REL2b > REL) {a1} (se reporta) · p1/c1 REL2b "
          f"{m(R,'REL2b',0,'p1')}/{m(R,'REL2b',0,'c1')} · saciedad {m(R,'REL2b',0,'sac_frac')} vs REL {m(R,'REL',0,'sac_frac')}")

    u = U['B2-2']
    R0_2b1, R0_2b0 = m(R, 'REL2b', 1, 'R0'), m(R, 'REL2b', 0, 'R0')
    fnd = m(R, 'REL2b', 1, 'fundadores')
    cruza = ge(R0_2b1, u['R0_cierre']) and le(fnd, u['fund_cierre'])
    linea('B2-2', ge(R0_2b1, u['R0_min']),
          f"R0 REL2b acum=1 {R0_2b1} (>= {u['R0_min']}; rango predicho {u['R0_rango']}) · acum=0 {R0_2b0} · "
          f"r acum=1 {m(R,'REL2b',1,'r')} · fundadores {fnd} · CLAUSULA H1-6 (R0 >= {u['R0_cierre']} con "
          f"fundadores <= {u['fund_cierre']}): {'CRUZA -- H-1 dejaria de estar en pie' if cruza else 'NO cruza -- H-1 y ERR-62 SIGUEN EN PIE'} · "
          f"techo del mundo: RENACE acum=1 {m(R,'RENACE',1,'R0')}")

    u = U['B2-3']
    a3 = A12(cel(R, 'REL2b', 0, 'vida_med'), cel(R, 'DOSIS', 0, 'vida_med'))
    r3 = razon(m(R, 'REL2b', 0, 'R0'), m(R, 'DOSIS', 0, 'R0'))
    ok_b3 = ge(a3, u['A12_vida']) and ge(r3, u['razon_R0'])
    linea('B2-3', ok_b3,
          f"A12(vida REL2b > DOSIS) {a3} (>= {u['A12_vida']}) · R0 REL2b {m(R,'REL2b',0,'R0')} / DOSIS "
          f"{m(R,'DOSIS',0,'R0')} = {r3} (>= {u['razon_R0']}) · vida DOSIS {m(R,'DOSIS',0,'vida_med')} · J DOSIS "
          f"{m(R,'DOSIS',0,'J')} · LECTURA CONDICIONADA (preregistro sec. 5): "
          f"{'B2-1 paso -> B2-3 se lee' if ok_b1 else 'B2-1 CAYO -> B2-3 se REPORTA y NO se interpreta'}")

    u = U['B2-4']
    v2 = m(R, 'REL2', 0, 'vida_med')
    r4 = razon(v2, vrel)
    J2 = m(R, 'REL2', 0, 'J')
    ok_b4 = (dentro(r4, *u['razon']) and J2 is not None and Jrel is not None and J2 <= Jrel - u['dJ'])
    linea('B2-4', ok_b4,
          f"vida REL2 {v2} / REL {vrel} = {r4} (en {u['razon']}; C midio 0.38x en su humo) · J REL2 {J2} "
          f"(<= J REL {Jrel} - {u['dJ']}) · p1/c1 REL2 {m(R,'REL2',0,'p1')}/{m(R,'REL2',0,'c1')} · "
          f"fam_nac REL2 {m(R,'REL2',0,'fam_nac')} (la puerta se abre AL NACER) · exposiciones A REL2 "
          f"{m(R,'REL2',0,'exp_A')} vs REL {m(R,'REL',0,'exp_A')} (come MAS y vive MENOS)")

    u = U['B2-5']
    R0o1, R0o0 = m(R, 'ORACULO', 1, 'R0'), m(R, 'ORACULO', 0, 'R0')
    vo = m(R, 'ORACULO', 0, 'vida_med')
    fndo = m(R, 'ORACULO', 1, 'fundadores')
    cordura = (R0o0 is not None and m(R, 'REL2b', 0, 'R0') is not None
               and R0o0 >= m(R, 'REL2b', 0, 'R0') - u['dR0']
               and vo is not None and v2b is not None and vo >= v2b * u['razon_vida'])
    cruza_or = ge(R0o1, u['R0_cierre']) and le(fndo, u['fund_cierre'])
    linea('B2-5', cordura,
          f"(i) CORDURA DE LA COTA: R0 ORACULO acum=0 {R0o0} >= R0 REL2b {m(R,'REL2b',0,'R0')} - {u['dR0']} y "
          f"vida ORACULO {vo} >= {u['razon_vida']}x vida REL2b {v2b} -> {'si' if cordura else 'NO (si el oraculo pierde contra el candidato, se para y se abre ERR)'} · "
          f"(ii) EL MURO: R0 ORACULO acum=1 {R0o1} (fundadores {fndo}) -> "
          f"{'CRUZA 0.9: el muro era la herencia' if cruza_or else 'NO cruza 0.9 -> EL MURO ES EL MUNDO, no la herencia (H-1 y ERR-62 en pie)'} · "
          f"p1/c1/J ORACULO {m(R,'ORACULO',0,'p1')}/{m(R,'ORACULO',0,'c1')}/{m(R,'ORACULO',0,'J')}")

    # ------------------------------------------------ REPORTADAS (no juzgan)
    vb, vc = m(R, 'REL_BAR', 0, 'vida_med'), m(R, 'CAUTELA', 0, 'vida_med')
    Jc, c1c, c1b = m(R, 'CAUTELA', 0, 'J'), m(R, 'CAUTELA', 0, 'c1'), m(R, 'REL_BAR', 0, 'c1')
    calib = (c1c is not None and c1b is not None and abs(c1c - c1b) <= CAUT_C1_TOL)
    repro = (calib and vb and vc and abs(vc / vb - 1) <= CAUT_VIDA_TOL
             and Jc is not None and J_bar is not None and abs(Jc - J_bar) <= CAUT_J_TOL)
    nota('B2-CAUT',
         f"calibracion c*={C_CAUT} (rejilla {CAUT_GRID}, humo): c1 CAUTELA {c1c} vs REL_BAR {c1b} "
         f"(|dif| <= {CAUT_C1_TOL}): {'VALIDA' if calib else 'FALLIDA -> la clausula NO se lee y no se recalibra (regla 3)'} · "
         f"vida CAUTELA {vc} vs REL_BAR {vb} · J CAUTELA {Jc} vs REL_BAR {J_bar} · p1 CAUTELA {m(R,'CAUTELA',0,'p1')} · "
         f"VEREDICTO DEL DIAGNOSTICO: {'REPRODUCE -> el nodo barajado ES cautela generica (medido, no inferido)' if repro else 'NO reproduce -> lo que REL_BAR aporta NO es solo cautela: el diagnostico de C queda REFUTADO'}",
         "B2-CAUT (REPORTADA, no es puerta): el brazo que puede refutar el diagnostico de F9-4bis")
    nota('B2-2bBAR',
         f"vida REL2b_BAR {m(R,'REL2b_BAR',0,'vida_med')} vs REL2b {v2b} · J {m(R,'REL2b_BAR',0,'J')} vs {J2b} · "
         f"A12(vida REL2b > REL2b_BAR) {A12(cel(R,'REL2b',0,'vida_med'), cel(R,'REL2b_BAR',0,'vida_med'))} · "
         f"p1/c1 {m(R,'REL2b_BAR',0,'p1')}/{m(R,'REL2b_BAR',0,'c1')}",
         "CONTENIDO DEL CANDIDATO (REPORTADA): el candidato con el nodo barajado")
    nota('F9-7',
         "NO se corre REL_TARDE: F9-7 cayo en las TRES series del bloque 1 (A12 0.426 / 0.53 / 0.626; contraste "
         "interno 9/20, 7/20, 5/20). Queda declarada REFUTADA por el bloque 1 y no se rejuzga (regla 3).",
         "F9-7 (REFUTADA x3 en el bloque 1; no es puerta de este bloque)")
    return V


# ------------------------------------------------------------------ identidad dentro del runner (regla 14)
def identidad_corta(Ti=20000, sem=(1,)):
    """Las CINCO comprobaciones que no pueden faltar antes de una serie, dentro del propio runner
    (el arnes completo, con los >= 7 controles que DEBEN diferir, esta en identidad_f9c.py):
      (1) apagado == organismo_f9 BIT A BIT en el brazo REL (la cadena no se movio);
      (2) nodo_via=1 == organismo_f9b BIT A BIT (salvo las claves nuevas declaradas pa/pn);
      (3) REL2b != REL y REL2b != REL2 (ERR-38: la perilla no es inerte);
      (4) CAUTELA != NADA y DOSIS != REL y ORACULO != REL2b;
      (5) rep_acum=1 != rep_acum=0 en REL2b."""
    import organismo_f9 as F9
    import sys as _s
    _s.path.insert(0, os.path.join(RAIZ, 'experimentos', 'junta_20260921', 'C'))
    import organismo_f9b as F9B
    out = []
    NUEV = {'pa', 'pn'}
    for s in sem:
        a = F9.run(s, T=Ti, **CF.BRAZOS['REL'])
        b = F9C.run(s, T=Ti, **dict(BRAZOS['REL'], f9c=0))
        dif = [k for k in a if k not in b or N(a[k]) != N(b[k])]
        out.append(('(1) apagado == organismo_f9 BIT A BIT (brazo REL)', not dif and set(b) == set(a), f"dif {dif[:4]}"))
        kb = dict(CF.BRAZOS['REL'], nodo_via=1)
        a2 = F9B.run(s, T=Ti, **kb)
        b2 = F9C.run(s, T=Ti, **BRAZOS['REL2'])
        d2 = [k for k in a2 if k not in b2 or N(a2[k]) != N(b2[k])]
        f9a, f9b_ = a2.get('f9') or {}, b2.get('f9') or {}
        d2b = [k for k in f9a if k not in f9b_ or N(f9a[k]) != N(f9b_[k])]
        ex = set(f9b_) - set(f9a)
        out.append(('(2) nodo_via=1 == organismo_f9b BIT A BIT (salvo pa/pn, SOLO LECTURA)',
                    not [k for k in d2 if k != 'f9'] and not d2b and ex <= NUEV, f"dif {d2[:4]} f9 {d2b[:4]} extra {sorted(ex-NUEV)}"))
        r2b = F9C.run(s, T=Ti, **BRAZOS['REL2b'])
        rel = F9C.run(s, T=Ti, **BRAZOS['REL'])
        out.append(('(3) REL2b != REL y REL2b != REL2 (DEBEN diferir, ERR-38)',
                    N(r2b) != N(rel) and N(r2b) != N(b2),
                    f"via_msg {r2b['f9'].get('via_msg')} · fam_nac max REL2b "
                    f"{max(r2b['f9'].get('fam_nac') or [0])} (debe ser 0) · REL2 {max(b2['f9'].get('fam_nac') or [0])} (> 0) · "
                    f"pa/pn REL2b {r2b['f9'].get('pa')}/{r2b['f9'].get('pn')}"))
        cau = F9C.run(s, T=Ti, **BRAZOS['CAUTELA']); nad = F9C.run(s, T=Ti, **BRAZOS['NADA'])
        dos = F9C.run(s, T=Ti, **BRAZOS['DOSIS']); ora = F9C.run(s, T=Ti, **BRAZOS['ORACULO'])
        out.append(('(4) CAUTELA != NADA, DOSIS != REL, ORACULO != REL2b (DEBEN diferir)',
                    N(cau) != N(nad) and N(dos) != N(rel) and N(ora) != N(r2b),
                    f"mordidas CAUTELA {sum(sum(v) for v in cau['mord'].values())} vs NADA "
                    f"{sum(sum(v) for v in nad['mord'].values())}"))
        n0 = F9C.run(s, T=Ti, **BRAZOS['REL2b']); n1 = F9C.run(s, T=Ti, **dict(BRAZOS['REL2b'], rep_acum=1))
        out.append(('(5) rep_acum=1 != rep_acum=0 en REL2b (DEBE diferir)',
                    N(n0) != N(n1), f"desc {n0['descendientes']} -> {n1['descendientes']}"))
    return out


# ------------------------------------------------------------------ humo (UN proceso, 6 corridas)
def humo(Ti=T_HUMO):
    """SEIS corridas, UN proceso, sin Pool (regla 3), semillas 1-2 YA VISTAS.
      1-2  REL2b s=1, s=2 (acum=1)  -- EL CANDIDATO, lo que mas importa medir (no lo corrio nadie)
      3    REL_BAR s=1 (acum=1)     -- el objetivo de calibracion c1(REL_BAR)
      4-5  CAUTELA s=1 con la rejilla CAUT_GRID (acum=1)  -- la calibracion declarada
      6    ORACULO s=1 (acum=1)     -- la cota superior
    Las referencias REL y REL2 NO se re-corren: la identidad (1) y (2) las hace EXACTAS contra
    organismo_f9 y organismo_f9b, y sus numeros a T=100000, acum=1, semillas 1-2 estan en
    datos/humo/f9b_humo_20260921_160425.json (REL R0 0.423/0.484, vida 549.5/601, J 0.960/0.934;
    REL2 R0 0.415/0.450, vida 209/208, J 0.738/0.771)."""
    os.makedirs(HUMO, exist_ok=True)
    sel = sello(); pre = 'f9c_humo'
    LOG[0] = open(os.path.join(HUMO, f"{pre}_{sel}.log"), 'w', encoding='utf-8')
    t0 = time.time()
    log(f"HUMO FASE 9 BLOQUE 2 · {time.strftime('%Y-%m-%d %H:%M:%S')} · UN proceso, sin Pool (regla 3)")
    log(f"  organismo_f9c.py sha {h16(os.path.join(AQUI,'organismo_f9c.py'))} · origen f9 "
        f"{h16(os.path.join(N09,'organismo_f9.py'))} (se espera {SHA_ESPERADOS['f9']}) · f9b "
        f"{h16(os.path.join(RAIZ,'experimentos','junta_20260921','C','organismo_f9b.py'))} (se espera {SHA_ESPERADOS['f9b']})")
    log(f"  python {platform.python_version()} · T={Ti} · 6 corridas (semillas 1-2 YA VISTAS)")
    log("\nETAPA 1/4 — REGLA 14 (campo a campo contra corre_f9.BRAZOS)")
    r14 = regla14()
    log("\nETAPA 2/4 — identidad dentro del runner (regla 14, ERR-38)")
    ide = identidad_corta(20000, (1,))
    for et, ok, det in ide:
        log(f"  {'OK  ' if ok else 'FALLA'} {et}   {det}")
    if not all(ok for _, ok, _ in ide):
        log("  IDENTIDAD FALLA -> el humo NO sigue.")
        json.dump(dict(identidad=[[e, bool(o), d] for e, o, d in ide], ok=False),
                  open(os.path.join(HUMO, f"{pre}_{sel}.json"), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return 1
    log("\nETAPA 3/4 — 6 corridas (REL2b x2 · REL_BAR · CAUTELA x2 de rejilla · ORACULO)")
    tareas = [('REL2b', 1, 1, Ti, None), ('REL2b', 2, 1, Ti, None), ('REL_BAR', 1, 1, Ti, None),
              ('CAUTELA', 1, 1, Ti, dict(sesgo_fijo=CAUT_GRID[0])),
              ('CAUTELA', 1, 1, Ti, dict(sesgo_fijo=CAUT_GRID[1])),
              ('ORACULO', 1, 1, Ti, None)]
    R = []
    for tk in tareas:
        x = tarea(tk); R.append(x)
        log(f"  [{time.time()-t0:6.1f}s] {x['brazo']:10s} s{x['seed']} acum{x['acum']} "
            f"{str(x.get('extra') or ''):22s} R0 {x['R0']:<7} r {x['r']:<6} vida {str(x['vida_med']):<8} "
            f"cuerpos {x['cuerpos']:<5} p1 {x['p1']} c1 {x['c1']} J {x['J']} sac {x['sac_frac']} "
            f"expA {x['exp_A']} via {x['via_msg']} famnac {x['fam_nac']}/{x['fam_nac_max']} "
            f"pa {x['frac_pa']} fund {x['fundadores']} coh {x['coherente']}")
    log("\nETAPA 4/4 — predicciones del humo (HC1..HC6, escritas en el PREREGISTRO ANTES de correrlo) y calibracion")
    g = {x['brazo']: x for x in R}
    b2b = [x for x in R if x['brazo'] == 'REL2b']
    cau = [x for x in R if x['brazo'] == 'CAUTELA']
    hc = {}
    hc['HC1'] = all(x['coherente'] and x['f9_len'] for x in R)                                   # BLOQUEA (instrumento)
    hc['HC2'] = all(x['fam_nac_max'] == 0 for x in b2b) and all(x['via_msg'] and x['via_msg'] > 0 for x in b2b)  # BLOQUEA
    hc['HC3'] = all(x['frac_pa'] is not None and x['frac_pa'] > 0 for x in b2b)                  # BLOQUEA
    hc['HC4'] = all(x['vida_med'] is not None and x['vida_med'] > 250 for x in b2b)              # hipotesis
    hc['HC5'] = all(x['J'] is not None and x['J'] >= 0.90 for x in b2b)                          # hipotesis
    hc['HC6'] = (len(cau) == 2 and cau[0]['c1'] is not None and cau[1]['c1'] is not None
                 and min(cau[0]['c1'], cau[1]['c1']) <= g['REL_BAR']['c1'] <= max(cau[0]['c1'], cau[1]['c1']))  # calibracion
    for k, v in hc.items():
        log(f"  {k}: {'SI' if v else 'NO'}")
    log("  Solo HC1, HC2 y HC3 BLOQUEAN (son el instrumento). HC4 y HC5 son la HIPOTESIS: si fallan se escriben")
    log("  en el preregistro y la serie corre con esta letra. NINGUN umbral se cambia despues del humo (regla 4).")
    # calibracion declarada
    c_obj = g['REL_BAR']['c1']; cs = None
    if len(cau) == 2 and all(x['c1'] is not None for x in cau) and c_obj is not None:
        (x1, y1), (x2, y2) = (CAUT_GRID[0], cau[0]['c1']), (CAUT_GRID[1], cau[1]['c1'])
        if min(y1, y2) <= c_obj <= max(y1, y2) and y1 != y2:
            cs = round(x1 + (x2 - x1) * (y1 - c_obj) / (y1 - y2), 1)
            log(f"  CALIBRACION: c1(REL_BAR) {c_obj} BRACKETEADO por {y1} (c={x1}) y {y2} (c={x2}) -> "
                f"c* = {cs} (interpolacion lineal, regla del preregistro)")
        else:
            cs = x1 if abs(y1 - c_obj) <= abs(y2 - c_obj) else x2
            log(f"  CALIBRACION: SIN bracket (c1 REL_BAR {c_obj}; rejilla {y1}, {y2}) -> c* = {cs} (el mas cercano); "
                f"la brecha se DECLARA y B2-CAUT se lee como control debil")
    log(f"  -> escribir C_CAUT = {cs} en corre_bloque2.py ANTES de la serie (con la cita de este JSON)")
    ruta = os.path.join(HUMO, f"{pre}_{sel}.json")
    json.dump(dict(bloque='fase9_bloque2_humo', sello=sel, T=Ti, semillas=[1, 2],
                   sha_f9c=h16(os.path.join(AQUI, 'organismo_f9c.py')), sha_runner=h16(os.path.abspath(__file__)),
                   sha_origen=SHA_ESPERADOS, regla14=[[b, n, bool(o), d] for b, n, o, d in r14],
                   identidad=[[e, bool(o), d] for e, o, d in ide], corridas=R, HC=hc,
                   caut_grid=list(CAUT_GRID), c_objetivo=c_obj, c_estrella=cs,
                   ok=bool(hc['HC1'] and hc['HC2'] and hc['HC3']), seg=round(time.time() - t0, 1)),
              open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\nJSON  {ruta}  (sha {h16(ruta)})")
    log(f"HUMO terminado en {time.time()-t0:.1f}s")
    return 0 if (hc['HC1'] and hc['HC2'] and hc['HC3']) else 1


# ------------------------------------------------------------------ la serie (SOLO el coordinador)
def serie(desde, n, Ti, pool, brazos, acums, etiqueta):
    from multiprocessing import Pool
    os.makedirs(DATOS, exist_ok=True)
    sel = sello()
    pre = f"f9b2_s{desde}-{desde+n-1}{etiqueta}"
    LOG[0] = open(os.path.join(DATOS, f"{pre}_{sel}.log"), 'w', encoding='utf-8')
    t0 = time.time()
    SEEDS = list(range(desde, desde + n))
    tareas = [(b, s, a, Ti, None) for b in brazos for a in acums for s in SEEDS]
    log(f"FASE 9 — BLOQUE 2 · {time.strftime('%Y-%m-%d %H:%M:%S')} · semillas {SEEDS[0]}-{SEEDS[-1]} · "
        f"{len(brazos)} brazos x {len(acums)} niveles de rep_acum x {n} = {len(tareas)} corridas de T={Ti}")
    log(f"  organismo_f9c.py sha {h16(os.path.join(AQUI,'organismo_f9c.py'))} · runner sha {h16(os.path.abspath(__file__))}")
    log(f"  CAUTELA c* = {C_CAUT} (calibrado en el humo; rejilla {CAUT_GRID}) · DOSIS eta_s = {2*ETA_S_TRONCO}")
    log(f"  Pool {pool} (ERR-86: --pool o JUACO_POOL; nunca un Pool grande con otras corridas vivas)")
    log("\nETAPA 1/4 — REGLA 14 (campo a campo contra corre_f9.BRAZOS)")
    r14 = regla14()
    log("\nETAPA 2/4 — identidad dentro del runner (regla 14, ERR-38)")
    ide = identidad_corta(20000, (1, 2))
    for et, ok, det in ide:
        log(f"  {'OK  ' if ok else 'FALLA'} {et}   {det}")
    if not all(ok for _, ok, _ in ide):
        raise SystemExit("IDENTIDAD FALLA: la serie NO se corre.")
    log("\nETAPA 3/4 — series")
    with Pool(pool) as P:
        R = []
        for i, x in enumerate(P.imap_unordered(tarea, tareas), 1):
            R.append(x)
            if i % max(1, len(tareas) // 20) == 0:
                log(f"  [{time.time()-t0:6.1f}s] {i}/{len(tareas)}")
    crudo = os.path.join(DATOS, f"{pre}_{sel}.json")     # ERR-54: el crudo ANTES de analizar nada
    json.dump(dict(bloque='fase9_bloque2', sello=sel, desde=desde, n=n, T=Ti, brazos=brazos, acums=acums,
                   sha_f9c=h16(os.path.join(AQUI, 'organismo_f9c.py')), sha_runner=h16(os.path.abspath(__file__)),
                   sha_origen=SHA_ESPERADOS, sha_prereg=h16(os.path.join(AQUI, 'PREREGISTRO_bloque2.md')),
                   c_cautela=C_CAUT, caut_grid=list(CAUT_GRID), eta_s_dosis=2 * ETA_S_TRONCO,
                   regla14=[[b, nc, bool(o), d] for b, nc, o, d in r14],
                   identidad=[[e, bool(o), d] for e, o, d in ide], umbrales=UMBRALES, corridas=R),
              open(crudo, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"  CRUDO {crudo} (sha {h16(crudo)})")
    log("\nETAPA 4/4 — LAS PUERTAS (ERR-89: una linea por puerta del preregistro)")
    V = puertas(R)
    log("\nTABLA (mediana por celda; acum = reproduccion desacoplada de la saciedad)")
    log(f"  {'brazo':10s} {'ac':2s} {'R0':>7} {'r':>7} {'vida':>8} {'cuerp':>6} {'p1':>6} {'c1':>6} {'J':>7} "
        f"{'sac':>6} {'expA':>6} {'fund':>6} {'div':>5} {'via':>7} {'famn':>5} {'pa':>5}")
    for b in brazos:
        for a in acums:
            log(f"  {b:10s} {a:<2d} {str(m(R,b,a,'R0')):>7} {str(m(R,b,a,'r')):>7} {str(m(R,b,a,'vida_med')):>8} "
                f"{str(m(R,b,a,'cuerpos')):>6} {str(m(R,b,a,'p1')):>6} {str(m(R,b,a,'c1')):>6} "
                f"{str(m(R,b,a,'J')):>7} {str(m(R,b,a,'sac_frac')):>6} {str(m(R,b,a,'exp_A')):>6} "
                f"{str(m(R,b,a,'fundadores')):>6} {str(m(R,b,a,'frac_div')):>5} {str(m(R,b,a,'via_msg')):>7} "
                f"{str(m(R,b,a,'fam_nac')):>5} {str(m(R,b,a,'frac_pa')):>5}")
    ver = os.path.join(DATOS, f"{pre}_veredicto_{sel}.json")
    json.dump(dict(sello=sel, crudo=os.path.basename(crudo), puertas=V,
                   pasan=[k for k, v in V.items() if v['pasa'] is True],
                   caen=[k for k, v in V.items() if v['pasa'] is False],
                   reportadas=[k for k, v in V.items() if v['pasa'] is None]),
              open(ver, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\nPUERTAS QUE PASAN: {[k for k,v in V.items() if v['pasa'] is True]}")
    log(f"PUERTAS QUE CAEN : {[k for k,v in V.items() if v['pasa'] is False]}")
    log(f"REPORTADAS       : {[k for k,v in V.items() if v['pasa'] is None]}")
    log(f"VEREDICTO {ver} (sha {h16(ver)})")
    log(f"\nTerminado en {time.time()-t0:.1f}s")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--desde', type=int, default=DESDE)
    ap.add_argument('--n', type=int, default=N_SEM)
    ap.add_argument('--T', type=int, default=T)
    ap.add_argument('--pool', type=int, default=int(os.environ.get('JUACO_POOL', 6)))   # ERR-86
    ap.add_argument('--brazos', default=','.join(ORDEN))
    ap.add_argument('--acum', default='0,1')
    ap.add_argument('--etiqueta', default='')
    a = ap.parse_args()
    if a.humo:
        return humo(a.T)
    return serie(a.desde, a.n, a.T, a.pool, [b for b in a.brazos.split(',') if b],
                 [int(x) for x in a.acum.split(',')], a.etiqueta)


if __name__ == '__main__':
    sys.exit(main())
