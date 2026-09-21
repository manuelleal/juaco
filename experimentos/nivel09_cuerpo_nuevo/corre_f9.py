"""FASE 9 — EL CUERPO NUEVO: ¿aprende en MENOS DE UNA VIDA lo que su linaje ya sabe?

MISION: llegar a la AGI por este camino — organismo minimo, reglas locales, sin retropropagacion, peldanos
preregistrados con controles y replicas. Hoy: H-1 dejo escrito que con muerte real ningun modo de herencia
sostiene el linaje (R0 0.14-0.17, ERR-62) porque "el hijo nace vacio y muere antes de aprender". La fase 9
prueba el unico camino que queda sin herencia lamarckiana de pesos: que el recien nacido LEA el nodo del
linaje POR RELEVANCIA y desde su primer paso.

Ejecuta PREREGISTRO_cuerpo_nuevo.md. Instrumento organismo_f9.py (por anclas desde organismo_alma2.py
4fd616aeaf535e61, que solo se leyo; cadena hasta el TRONCO CONGELADO organismo_v14 v14.1 feefc88b1fd8d434).

    python experimentos/nivel09_cuerpo_nuevo/corre_f9.py --humo          (UN proceso, 6 corridas: lo corre el disenador)
    python experimentos/nivel09_cuerpo_nuevo/corre_f9.py --desde 1501    (LA SERIE: solo el COORDINADOR, con Pool)
    python experimentos/nivel09_cuerpo_nuevo/corre_f9.py --desde 1521    (REPLICA, regla 12)

POOL (ERR-86): el tamano sale de --pool o de la variable de entorno JUACO_POOL; por defecto 6. NUNCA se fija
a mano un Pool grande con otras corridas vivas. Los agentes no corren Pool (regla 3 de EQUIPO.md): --humo si.

ERR-89 (una puerta que el runner no imprime NO EXISTE): hay EXACTAMENTE una linea de salida por cada puerta
F9-1..F9-10 del preregistro, con su frase, su umbral y su PASA/CAE. UMBRALES trae la letra (ERR-31).
ERR-54: el crudo se guarda ANTES de analizar nada. ERR-87: lee_json exige prefijo + SELLO EXACTO.

LOS NUEVE BRAZOS DE LECTURA (x 2 niveles de rep_acum = 18 celdas)
  RENACE    muerte_real=0  -- el ANCLA con sha: la muerte de hoy (inmortal subsidiado). Si no reproduce el
            bloque 2 / H-1, el instrumento se movio y NO SE LEE NADA (puerta F9-1, bloqueante).
  NADA      muerte real, sin nodo, sin herencia  -- es NADA_CM de H-1 cuerpo a cuerpo: la linea base.
  M1        muerte real, hereda el VECTOR Wps/Wns  -- "linaje sin nodo" CON la mejor herencia de H-1.
  REC       nodo + conectado desde el cuerpo 1, lectura por RECENCIA  -- el mecanismo de ALMA/CIEGO, sin alma.
  REL       igual pero lectura por RELEVANCIA VIVA: |R - (Wps-Wns)@P| del propio lector, RECALCULADO tras
            cada mensaje absorbido, sobre TODO el nodo  <- EL CANDIDATO
  REL_FIJO  el mismo puntaje calculado UNA SOLA VEZ (con el vector del recien nacido, que es 0): degenera
            en |R| y lee casi solo veneno  <- LA TRAMPA 2 EN CARNE PROPIA: prediccion escrita = gana p1
            (evita el veneno) y PIERDE en saciedad, comida y R0. Separa "saber" de "tener miedo a todo".
  REL_BAR   REL con las recompensas del mensaje PERMUTADAS (mismas marginales, asociacion destruida)
            <- CONTROL DE CONTENIDO: separa "conocimiento" de "cautela generica"
  REL_AZAR  mismo alcance que REL (todo el nodo) pero seleccion AL AZAR  <- separa RANKEAR de NO EXPIRAR
  REL_TARDE REL pero conectado recien tras la muerte 5  <- "nacimiento SIN conexion", con su propia base
            dentro del mismo brazo y la misma semilla (cuerpos 1-4 son exactamente NADA)

VOCABULARIO (regla 6): "cuerpo", "linaje", "nodo del linaje", "exposicion sin consecuencia", "R0 del linaje",
"rechaza lo malo en su primer encuentro". NO se dice "ensena", "cultura", "recuerda su vida pasada",
"evoluciona", "quiere". Nada nace: `descendientes` sigue siendo un contador de ventanas de viabilidad.
"""
import argparse, hashlib, json, os, platform, re, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
sys.path[:0] = [AQUI, N13, N11, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import corre_vivo_rep as C1        # med, A12, razon, N, h16: NO se copian
import corre_vivo_rep2 as C2       # MED2: NO se copia
import organismo_f9 as F9

med, A12, razon, N, h16 = C1.med, C1.A12, C1.razon, C1.N, C1.h16

T = 100000
T_HUMO = 100000
N_SEM = 20
DESDE = 1501
DATOS = os.path.join(RAIZ, 'datos')
HUMO = os.path.join(DATOS, 'humo')
GRANDE = 10 ** 9                   # alma_muertes: la corrida NUNCA se corta por numero de muertes; manda T
SHA_ESPERADOS = dict(v14='feefc88b1fd8d434', vivo='20c0961c79de8825', rep='aa823d56c2d4213c',
                     rep2='96feb4918dc5d694', h1='9e99ff87b5e2db1e', alma='7c09cec391daa879',
                     alma2='4fd616aeaf535e61')

# ------------------------------------------------------------------ EL CUERPO (regla 14: campo a campo)
MED_H1 = dict(C2.MED2, h1=1)
# CUELLO_MIN es el MISMO brazo en el que H-1 midio R0 0.148/0.140 (NADA) y 0.160/0.170 (M1) y en el que el
# BLOQUE ALMA midio NINGUNA / CIEGO / BARAJA. No se cambia ni una constante del cuerpo.
CUERPO = dict(C1.BRAZOS['CUELLO_MIN']) | MED_H1 | dict(muerte_real=1, hereda='nada', dote=0.6)


def curita_f(res):
    """El alma NULA. La fase 9 no tiene alma: el nodo y la conexion son MECANISMO, no curita elegida.
    Siempre (f) = no hacer nada, con menu='f': el instrumento no puede mover dote, umbral ni herencia."""
    return {'curita': 'f', 'motivo': 'fase 9: sin alma, el mecanismo es el nodo'}


NODO = dict(alma=curita_f, alma_muertes=GRANDE, menu='f', f9=1, nodo_k=20, nodo_lee=50)
BRAZOS = {
    'RENACE':    dict(CUERPO, muerte_real=0, hereda='nada'),                                  # sin alma: f9 no aplica
    'NADA':      dict(CUERPO, **NODO, nodo=0, conectado=0),
    'M1':        dict(CUERPO, hereda='M1', **NODO, nodo=0, conectado=0),
    'REC':       dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=0),
    'REL':       dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=1),
    'REL_FIJO':  dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=3),
    'REL_BAR':   dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=1, nodo_baraja=1),
    'REL_AZAR':  dict(CUERPO, **NODO, nodo=1, conectado=1, nodo_rel=2),
    'REL_TARDE': dict(CUERPO, **NODO, nodo=1, conectado=0, nodo_rel=1, con_desde=5),
}
ORDEN = ['RENACE', 'NADA', 'M1', 'REC', 'REL', 'REL_FIJO', 'REL_BAR', 'REL_AZAR', 'REL_TARDE']
CON_DESDE_TARDE = 5
ACUM = [0, 1]

# ------------------------------------------------------------------ LA LETRA DEL PREREGISTRO (ERR-31)
UMBRALES = {
    'F9-1': dict(frase="ANCLA (BLOQUEANTE): el instrumento no se movio -- NADA reproduce NADA_CM de H-1 y "
                       "RENACE reproduce el inmortal del bloque 2",
                 R0_NADA=(0.10, 0.22), vida_NADA=(float(os.environ.get('F9_VIDA_NADA_MIN', '90.0')), 170.0), R0_RENACE=(0.70, 1.40), r_RENACE=(-50.0, 25.0)  # ERR-92: minimo por F9_VIDA_NADA_MIN (ENMIENDA_ERR92_ancla.md); 90.0 = letra original),
    'F9-2': dict(frase="EL NODO POR RELEVANCIA ALARGA LA VIDA DEL CUERPO NUEVO",
                 razon_vida=2.5, A12_vida=0.85),
    'F9-3': dict(frase="MENOS DE UNA VIDA (la pregunta): el recien nacido RECHAZA lo malo en su PRIMER "
                       "encuentro, y NO a costa de dejar de comer (p1 y c1 juntos, trampa 2)",
                 p1_REL=0.60, dif_p1=0.30, A12_p1=0.85, c1_margen=0.10, sac_margen=0.95),
    'F9-4': dict(frase="CONTENIDO, NO CAUTELA GENERICA: el nodo barajado no compra la vida",
                 A12_vida=0.80, p1_margen=0.15),
    'F9-5': dict(frase="RELEVANCIA > RECENCIA (la lecciones no expiran)",
                 A12_vida=0.65, razon_R0=1.15),
    'F9-6': dict(frase="RANKEAR, NO SOLO ACCEDER: la relevancia le gana al azar sobre el mismo nodo",
                 A12_vida=0.65),
    'F9-7': dict(frase="CONEXION DESDE EL NACIMIENTO: conectarse tarde cuesta, y dentro del mismo brazo los "
                       "cuerpos conectados viven mas que los cuerpos 1..4",
                 A12_vida=0.65, razon_dentro=2.0, k_dentro=15),
    'F9-8': dict(frase="REPRODUCCION DESACOPLADA DE LA SACIEDAD (perilla APARTE): sube R0 en todos los brazos "
                       "sin cambiar el orden entre mecanismos",
                 razon_R0_NADA=1.30, spearman=0.80, R0_cierre=0.90, fund_cierre=2),
    'F9-9': dict(frase="SEGURIDAD: contabilidad, la perilla NO es inerte (ERR-38) y el mundo no se comio la comida",
                 frac_div=0.50, exp_min=0.50, exentos=('REL_FIJO',)),
    'F9-10': dict(frase="LA RELEVANCIA VIVA NO ES MIEDO A TODO: el ranking calculado UNA sola vez (REL_FIJO) "
                        "sube p1 y HUNDE c1; el vivo no",
                  p1_fijo=0.60, razon_R0=1.15, A12_sac=0.65),
}


# ------------------------------------------------------------------ utilidades
LOG = [None]


def log(msg=""):
    print(msg, flush=True)
    if LOG[0]:
        LOG[0].write(msg + "\n"); LOG[0].flush(); os.fsync(LOG[0].fileno())


def sello():
    return time.strftime('%Y%m%d_%H%M%S')


def ultimo_sello(carpeta, prefijo):
    """ERR-87: NUNCA `startswith(prefijo)` a secas (el prefijo de un brazo es prefijo de otro).
    Se exige el nombre COMPLETO `<prefijo>_<AAAAMMDD_HHMMSS>.json` con una expresion regular ANCLADA."""
    pat = re.compile(r'^' + re.escape(prefijo) + r'_(\d{8}_\d{6})\.json$')
    sellos = sorted(m.group(1) for m in (pat.match(f) for f in os.listdir(carpeta)) if m)
    return sellos[-1] if sellos else None


def lee_json(carpeta, prefijo, sel):
    """ERR-87: prefijo + SELLO EXACTO. Sin sello no se lee nada (no se adivina el 'ultimo')."""
    ruta = os.path.join(carpeta, f"{prefijo}_{sel}.json")
    if not os.path.exists(ruta):
        raise SystemExit(f"lee_json: no existe {ruta} (prefijo + sello EXACTO, ERR-87)")
    return json.load(open(ruta, encoding='utf-8')), ruta


def frac(xs):
    """Media sobre los cuerpos que TUVIERON la ocasion (-1 = no la tuvieron: no cuenta ni arriba ni abajo)."""
    ys = [x for x in xs if x >= 0]
    return round(sum(ys) / len(ys), 4) if ys else None


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


def ge(x, u):
    return x is not None and x >= u


def le(x, u):
    return x is not None and x <= u


def dentro(x, lo, hi):
    return x is not None and lo <= x <= hi


# ------------------------------------------------------------------ una corrida
def resumen(brazo, seed, acum, r, Ti):
    """Todo de SOLO LECTURA sobre el crudo. R0 = descendientes / vidas = desc / (muertes + 1), la
    definicion de H-1 (PREREGISTRO_h1_muerte.md sec. 3), no la del instrumento."""
    d, mu = r['descendientes'], r['deaths']
    vidas = r.get('vidas_h1') or r.get('vidas') or []
    org = r.get('origen_cuerpo') or []
    f = r.get('f9') or {}
    p1, c1, tok, ncu = f.get('p1', []), f.get('c1', []), f.get('t_ok', []), f.get('con_cuerpo', [])
    # F9-7: dentro de REL_TARDE, los cuerpos 1..con_desde-1 son NADA y los >= con_desde estan conectados
    v_pre = [v for i, v in enumerate(vidas[:len(p1)]) if i < CON_DESDE_TARDE - 1]
    v_pos = [v for i, v in enumerate(vidas[:len(p1)]) if i >= CON_DESDE_TARDE - 1]
    o = dict(brazo=brazo, seed=seed, acum=acum, seg=round(Ti, 2),
             descendientes=d, muertes=mu, R0=round(d / (mu + 1), 4), r=d - mu,
             vida_med=med(vidas), vida_med_fund=med([v for v, g in zip(vidas, org) if not g]),
             vida_med_her=med([v for v, g in zip(vidas, org) if g]),
             cuerpos=len(vidas), fundadores=r.get('fundadores'), t_fund1=(r.get('t_fund') or [None])[0],
             frac_fund=razon(r.get('desc_fund'), d), frac_regalo=razon(r.get('desc_regalo'), d),
             p1=frac(p1), c1=frac(c1), t_ok=med([x for x in tok if x >= 0]),
             sac_frac=razon(r.get('pasos_viables'), r.get('T_efectivo') or T),
             p1_n=len([x for x in p1 if x >= 0]), c1_n=len([x for x in c1 if x >= 0]),
             con_frac=frac(ncu) if ncu else None,
             lect_div=f.get('lect_div'), lecturas=f.get('lecturas'),
             frac_div=razon(f.get('lect_div'), f.get('lecturas')),
             nodo_n=r.get('nodo_n'), conectado_final=r.get('conectado_final'),
             exp_A=(r.get('exposiciones') or {}).get('A'), exp_B=(r.get('exposiciones') or {}).get('B'),
             muertes_nec=r.get('muertes_nec'), celdas=r.get('celdas'), splits=r.get('splits'),
             vida_pre=med(v_pre), vida_pos=med(v_pos),
             cola_desborde=r.get('cola_desborde'), T_efectivo=r.get('T_efectivo'))
    # contabilidad (H1-8, traida entera)
    ok = (r.get('nacimientos') == mu and len(vidas) == mu + 1
          and len(r.get('desc_por_vida') or []) == mu + 1 and len(org) == mu + 1
          and sum(vidas) == (r.get('T_efectivo') or T) and sum(r.get('desc_por_vida') or []) == d
          and (r.get('fundadores') or 0) + 1 == sum(1 for g in org if not g))
    o['coherente'] = bool(ok) if r.get('muerte_real') else None
    o['f9_len'] = (len(p1) == len(c1) == len(tok) == mu) if f else None
    return o


def tarea(args):
    brazo, seed, acum, Ti = args
    kw = dict(BRAZOS[brazo], rep_acum=acum)
    t0 = time.time()
    r = F9.run(seed, T=Ti, **kw)
    return resumen(brazo, seed, acum, r, time.time() - t0)


# ------------------------------------------------------------------ las nueve puertas (ERR-89: una linea por puerta)
def cel(R, brazo, acum, campo):
    return [x[campo] for x in R if x['brazo'] == brazo and x['acum'] == acum and x[campo] is not None]


def m(R, brazo, acum, campo):
    return med(cel(R, brazo, acum, campo))


def puertas(R, log=log):
    V, U = {}, UMBRALES

    def linea(p, ok, txt):
        V[p] = dict(pasa=bool(ok), detalle=txt, frase=U[p]['frase'])
        log(f"  {p}  {'PASA' if ok else 'CAE '}  {U[p]['frase']}")
        log(f"          {txt}")

    u = U['F9-1']
    a = dict(R0_NADA=m(R, 'NADA', 0, 'R0'), vida_NADA=m(R, 'NADA', 0, 'vida_med'),
             R0_RENACE=m(R, 'RENACE', 0, 'R0'), r_RENACE=m(R, 'RENACE', 0, 'r'))
    ok1 = all(dentro(a[k], *u[k]) for k in a)
    linea('F9-1', ok1, " · ".join(f"{k} {a[k]} en [{u[k][0]}, {u[k][1]}]" for k in a))

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
    ok3 = (ge(p_rel, u['p1_REL']) and p_nada is not None and ge(p_rel - p_nada, u['dif_p1'])
           and ge(ap, u['A12_p1']) and bal)
    linea('F9-3', ok3,
          f"p1 REL {p_rel} vs NADA {p_nada} (>= {u['p1_REL']}, dif >= {u['dif_p1']}, A12 {ap} >= {u['A12_p1']}) · "
          f"BALANCE (trampa 2): c1 REL {c_rel} vs NADA {c_nada} (>= NADA-{u['c1_margen']}) y saciedad REL {s_rel} "
          f"vs NADA {s_nada} (>= {u['sac_margen']}x): {'si' if bal else 'NO'} · "
          f"t_ok REL {m(R,'REL',0,'t_ok')} vs NADA {m(R,'NADA',0,'t_ok')} (se REPORTA: el que muerde todo llega "
          f"antes a su primera comida; t_ok solo no mide aprender) · exposiciones A REL {m(R,'REL',0,'exp_A')} "
          f"vs NADA {m(R,'NADA',0,'exp_A')}")

    u = U['F9-4']
    ab = A12(cel(R, 'REL', 0, 'vida_med'), cel(R, 'REL_BAR', 0, 'vida_med'))
    pb = m(R, 'REL_BAR', 0, 'p1')
    ok4 = ge(ab, u['A12_vida']) and (pb is not None and p_nada is not None and pb <= p_nada + u['p1_margen'])
    linea('F9-4', ok4, f"A12(vida REL > REL_BAR) {ab} (>= {u['A12_vida']}) · p1 REL_BAR {pb} "
                       f"(<= NADA {p_nada} + {u['p1_margen']}) · vida REL_BAR {m(R,'REL_BAR',0,'vida_med')}")

    u = U['F9-5']
    a5 = A12(cel(R, 'REL', 0, 'vida_med'), cel(R, 'REC', 0, 'vida_med'))
    r5 = razon(m(R, 'REL', 0, 'R0'), m(R, 'REC', 0, 'R0'))
    linea('F9-5', ge(a5, u['A12_vida']) and ge(r5, u['razon_R0']),
          f"A12(vida REL > REC) {a5} (>= {u['A12_vida']}) · R0 REL {m(R,'REL',0,'R0')} / REC {m(R,'REC',0,'R0')} "
          f"= {r5} (>= {u['razon_R0']})")

    u = U['F9-6']
    a6 = A12(cel(R, 'REL', 0, 'vida_med'), cel(R, 'REL_AZAR', 0, 'vida_med'))
    linea('F9-6', ge(a6, u['A12_vida']),
          f"A12(vida REL > REL_AZAR) {a6} (>= {u['A12_vida']}) · vida REL_AZAR {m(R,'REL_AZAR',0,'vida_med')}")

    u = U['F9-7']
    a7 = A12(cel(R, 'REL', 0, 'vida_med'), cel(R, 'REL_TARDE', 0, 'vida_med'))
    par = [(x['vida_pos'], x['vida_pre']) for x in R
           if x['brazo'] == 'REL_TARDE' and x['acum'] == 0 and x['vida_pos'] and x['vida_pre']]
    k7 = sum(1 for po, pr in par if po / pr >= u['razon_dentro'])
    linea('F9-7', ge(a7, u['A12_vida']) and k7 >= u['k_dentro'],
          f"A12(vida REL > REL_TARDE) {a7} (>= {u['A12_vida']}) · DENTRO del brazo: cuerpos >= {CON_DESDE_TARDE} "
          f"viven >= {u['razon_dentro']}x los cuerpos 1..{CON_DESDE_TARDE-1} en {k7}/{len(par)} (>= {u['k_dentro']})")

    u = U['F9-8']
    r8 = razon(m(R, 'NADA', 1, 'R0'), m(R, 'NADA', 0, 'R0'))
    br = [b for b in ORDEN if cel(R, b, 0, 'R0') and cel(R, b, 1, 'R0')]
    sp = spearman([m(R, b, 0, 'R0') for b in br], [m(R, b, 1, 'R0') for b in br])
    cierre = [(b, ac, m(R, b, ac, 'R0'), m(R, b, ac, 'fundadores')) for b in ORDEN for ac in ACUM
              if b != 'RENACE' and ge(m(R, b, ac, 'R0'), u['R0_cierre']) and le(m(R, b, ac, 'fundadores'), u['fund_cierre'])]
    linea('F9-8', ge(r8, u['razon_R0_NADA']) and ge(sp, u['spearman']),
          f"R0 NADA acum1 {m(R,'NADA',1,'R0')} / acum0 {m(R,'NADA',0,'R0')} = {r8} (>= {u['razon_R0_NADA']}) · "
          f"Spearman del orden entre niveles {sp} (>= {u['spearman']}) · CLAUSULA H1-6 (R0 >= {u['R0_cierre']} con "
          f"fundadores <= {u['fund_cierre']}): {cierre if cierre else 'NINGUN brazo -- H-1 y ERR-62 siguen en pie'}")

    u = U['F9-9']
    coh = [x for x in R if x['coherente'] is False]
    flen = [x for x in R if x['f9_len'] is False]
    fd = m(R, 'REL', 0, 'frac_div')
    fd_rec = m(R, 'REC', 0, 'lect_div')
    # Referencia = NADA (el mismo mundo mortal), no RENACE. REL_FIJO queda EXENTO y se REPORTA: su hipotesis
    # escrita ES que come menos (trampa 2 en carne propia); castigarlo aqui confundiria "el mundo se quedo sin
    # comida" con "este brazo eligio no comer". Declarado en el preregistro ANTES de correr.
    eA = m(R, 'NADA', 0, 'exp_A')
    pobres = [(b, ac, m(R, b, ac, 'exp_A')) for b in ORDEN for ac in ACUM
              if b not in u['exentos'] and eA and m(R, b, ac, 'exp_A') is not None
              and m(R, b, ac, 'exp_A') < u['exp_min'] * eA]
    ok9 = (not coh and not flen and ge(fd, u['frac_div']) and fd_rec == 0 and not pobres)
    linea('F9-9', ok9, f"contabilidad {len(R)-len(coh)}/{len(R)} · listas por cuerpo OK {len(R)-len(flen)}/{len(R)} · "
                       f"frac_div REL {fd} (>= {u['frac_div']}; 0 = perilla INERTE, ERR-38) · lect_div REC {fd_rec} (= 0) · "
                       f"exposiciones A (ref NADA {eA}, exentos {u['exentos']}) pobres "
                       f"{pobres if pobres else 'ninguna'} · REL_FIJO se REPORTA: {m(R,'REL_FIJO',0,'exp_A')}")

    u = U['F9-10']
    pf = m(R, 'REL_FIJO', 0, 'p1')
    r10 = razon(m(R, 'REL', 0, 'R0'), m(R, 'REL_FIJO', 0, 'R0'))
    a10 = A12(cel(R, 'REL', 0, 'sac_frac'), cel(R, 'REL_FIJO', 0, 'sac_frac'))
    ok10 = ge(pf, u['p1_fijo']) and ge(r10, u['razon_R0']) and ge(a10, u['A12_sac'])
    linea('F9-10', ok10, f"REL_FIJO p1 {pf} (>= {u['p1_fijo']}: el ranking congelado TAMBIEN evita) pero "
                         f"R0 REL {m(R,'REL',0,'R0')} / REL_FIJO {m(R,'REL_FIJO',0,'R0')} = {r10} "
                         f"(>= {u['razon_R0']}) y A12(saciedad REL > REL_FIJO) {a10} (>= {u['A12_sac']}) · "
                         f"exposiciones A REL {m(R,'REL',0,'exp_A')} vs REL_FIJO {m(R,'REL_FIJO',0,'exp_A')}")
    return V


# ------------------------------------------------------------------ identidad dentro del runner (regla 14)
def identidad_corta(Ti=20000, sem=(1,)):
    """Las tres comprobaciones que NO pueden faltar antes de una serie, dentro del propio runner:
    (1) NADA (con el alma nula y sin nodo) == organismo_alma2 con alma=None -> es NADA_CM de H-1;
    (2) REL != REC (si no difieren, la perilla es INERTE: ERR-38);
    (3) rep_acum=1 != rep_acum=0 en NADA. El arnes completo esta en identidad_f9.py."""
    import organismo_alma2 as A2
    out = []
    for s in sem:
        base = dict(CUERPO)
        a = A2.run(s, T=Ti, **base)
        b = F9.run(s, T=Ti, **BRAZOS['NADA'])
        nuevas = {'alma_muertes', 'curitas', 'nodo_n', 'conectado_final', 'dote_final', 'umbral_final',
                  'hereda_final', 'T_efectivo', 'miedo_inerte', 'vidas_cuerpo', 'desc_cuerpo', 'nodo_cola',
                  'alma_cfg', 'alma2', 'f9'}
        falta = [k for k in a if k not in b]
        dif = [k for k in a if k in b and N(a[k]) != N(b[k])]
        extra = set(b) - set(a)
        out.append(('(1) NADA con alma nula == organismo_alma2 (alma=None) = NADA_CM de H-1',
                    not falta and not dif and extra <= nuevas, f"falta {falta[:3]} dif {dif[:4]} extra {sorted(extra-nuevas)[:3]}"))
        rel = F9.run(s, T=Ti, **BRAZOS['REL']); rec = F9.run(s, T=Ti, **BRAZOS['REC'])
        out.append(('(2) REL != REC (DEBE diferir: si no, la relevancia es inerte, ERR-38)',
                    N(rel) != N(rec), f"lect_div REL {rel['f9']['lect_div']}/{rel['f9']['lecturas']} · REC {rec['f9']['lect_div']}"))
        n0 = F9.run(s, T=Ti, **BRAZOS['NADA']); n1 = F9.run(s, T=Ti, **dict(BRAZOS['NADA'], rep_acum=1))
        out.append(('(3) rep_acum=1 != rep_acum=0 en NADA (DEBE diferir)',
                    N(n0) != N(n1), f"desc {n0['descendientes']} -> {n1['descendientes']}"))
    return out


# ------------------------------------------------------------------ humo (UN proceso, 6 corridas)
def humo(Ti=T_HUMO):
    os.makedirs(HUMO, exist_ok=True)
    sel = sello()
    pre = 'f9_humo'
    LOG[0] = open(os.path.join(HUMO, f"{pre}_{sel}.log"), 'w', encoding='utf-8')
    t0 = time.time()
    log(f"HUMO FASE 9 — cuerpo nuevo · {time.strftime('%Y-%m-%d %H:%M:%S')} · UN proceso, sin Pool (regla 3)")
    log(f"  organismo_f9.py sha {h16(os.path.join(AQUI,'organismo_f9.py'))} · origen alma2 "
        f"{h16(os.path.join(N13,'organismo_alma2.py'))} (se espera {SHA_ESPERADOS['alma2']})")
    log(f"  python {platform.python_version()} · T={Ti} · 6 corridas (3 brazos x 2 semillas YA VISTAS 1,2)")
    log("\nETAPA 1/3 — identidad dentro del runner (regla 14, ERR-38)")
    ide = identidad_corta(20000, (1,))
    for et, ok, det in ide:
        log(f"  {'OK  ' if ok else 'FALLA'} {et}   {det}")
    if not all(ok for _, ok, _ in ide):
        log("  IDENTIDAD FALLA -> el humo NO sigue.")
        json.dump(dict(identidad=[[e, bool(o), d] for e, o, d in ide], ok=False),
                  open(os.path.join(HUMO, f"{pre}_{sel}.json"), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return 1
    log("\nETAPA 2/3 — 6 corridas (NADA, REC, REL x semillas 1, 2)")
    R = []
    for s in (1, 2):
        for b in ('NADA', 'REC', 'REL'):
            x = tarea((b, s, 0, Ti)); R.append(x)
            log(f"  [{time.time()-t0:6.1f}s] {b:10s} s{s}  R0 {x['R0']:<7} r {x['r']:<6} vida {x['vida_med']:<8} "
                f"cuerpos {x['cuerpos']:<5} p1 {x['p1']} c1 {x['c1']} t_ok {x['t_ok']} div {x['frac_div']} "
                f"fund {x['fundadores']} coh {x['coherente']}")
    log("\nETAPA 3/3 — predicciones del humo (HH1..HH5; escritas en el PREREGISTRO ANTES de correrlo)")
    hh = {}
    hh['HH1'] = all(next(x for x in R if x['brazo'] == 'REL' and x['seed'] == s)['vida_med'] >
                    next(x for x in R if x['brazo'] == 'NADA' and x['seed'] == s)['vida_med'] for s in (1, 2))
    hh['HH2'] = all(next(x for x in R if x['brazo'] == 'REL' and x['seed'] == s)['p1'] >
                    next(x for x in R if x['brazo'] == 'NADA' and x['seed'] == s)['p1'] for s in (1, 2))
    hh['HH3'] = all(x['coherente'] for x in R) and all(x['f9_len'] for x in R)
    hh['HH4'] = all(x['frac_div'] and x['frac_div'] > 0 for x in R if x['brazo'] == 'REL') and \
                all(x['lect_div'] == 0 for x in R if x['brazo'] == 'REC')
    hh['HH5'] = all(next(x for x in R if x['brazo'] == 'REL' and x['seed'] == s)['c1'] >=
                    next(x for x in R if x['brazo'] == 'NADA' and x['seed'] == s)['c1'] - 0.10 for s in (1, 2))
    for k, v in hh.items():
        log(f"  {k}: {'SI' if v else 'NO'}")
    log("  Solo HH3 y HH4 BLOQUEAN (son el instrumento). HH1, HH2 y HH5 son la HIPOTESIS: si fallan se escriben")
    log("  en el preregistro y la serie corre con esta letra. NINGUN umbral se cambia despues del humo (regla 4).")
    ruta = os.path.join(HUMO, f"{pre}_{sel}.json")
    json.dump(dict(bloque='fase9_cuerpo_nuevo_humo', sello=sel, T=Ti, semillas=[1, 2],
                   sha_f9=h16(os.path.join(AQUI, 'organismo_f9.py')), sha_runner=h16(os.path.abspath(__file__)),
                   sha_origen=SHA_ESPERADOS, identidad=[[e, bool(o), d] for e, o, d in ide],
                   corridas=R, HH=hh, ok=bool(hh['HH3'] and hh['HH4']),
                   seg=round(time.time() - t0, 1)),
              open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\nJSON  {ruta}  (sha {h16(ruta)})")
    log(f"HUMO terminado en {time.time()-t0:.1f}s")
    return 0 if (hh['HH3'] and hh['HH4']) else 1


# ------------------------------------------------------------------ la serie (SOLO el coordinador)
def serie(desde, n, Ti, pool, brazos, acums, etiqueta):
    from multiprocessing import Pool
    os.makedirs(DATOS, exist_ok=True)
    sel = sello()
    pre = f"f9_cuerpo_nuevo_s{desde}-{desde+n-1}{etiqueta}"
    LOG[0] = open(os.path.join(DATOS, f"{pre}_{sel}.log"), 'w', encoding='utf-8')
    t0 = time.time()
    SEEDS = list(range(desde, desde + n))
    tareas = [(b, s, a, Ti) for b in brazos for a in acums for s in SEEDS]
    log(f"FASE 9 — CUERPO NUEVO · {time.strftime('%Y-%m-%d %H:%M:%S')} · semillas {SEEDS[0]}-{SEEDS[-1]} · "
        f"{len(brazos)} brazos x {len(acums)} niveles de rep_acum x {n} = {len(tareas)} corridas de T={Ti}")
    log(f"  organismo_f9.py sha {h16(os.path.join(AQUI,'organismo_f9.py'))} · runner sha {h16(os.path.abspath(__file__))}")
    log(f"  Pool {pool} (ERR-86: --pool o JUACO_POOL; nunca un Pool grande con otras corridas vivas)")
    log("\nETAPA 1/3 — identidad dentro del runner (regla 14, ERR-38)")
    ide = identidad_corta(20000, (1, 2))
    for et, ok, det in ide:
        log(f"  {'OK  ' if ok else 'FALLA'} {et}   {det}")
    if not all(ok for _, ok, _ in ide):
        raise SystemExit("IDENTIDAD FALLA: la serie NO se corre.")
    log("\nETAPA 2/3 — series")
    with Pool(pool) as P:
        R = []
        for i, x in enumerate(P.imap_unordered(tarea, tareas), 1):
            R.append(x)
            if i % max(1, len(tareas) // 20) == 0:
                log(f"  [{time.time()-t0:6.1f}s] {i}/{len(tareas)}")
    crudo = os.path.join(DATOS, f"{pre}_{sel}.json")     # ERR-54: el crudo ANTES de analizar nada
    json.dump(dict(bloque='fase9_cuerpo_nuevo', sello=sel, desde=desde, n=n, T=Ti, brazos=brazos, acums=acums,
                   sha_f9=h16(os.path.join(AQUI, 'organismo_f9.py')), sha_runner=h16(os.path.abspath(__file__)),
                   sha_origen=SHA_ESPERADOS, sha_prereg=h16(os.path.join(AQUI, 'PREREGISTRO_cuerpo_nuevo.md')),
                   identidad=[[e, bool(o), d] for e, o, d in ide], umbrales=UMBRALES, corridas=R),
              open(crudo, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"  CRUDO {crudo} (sha {h16(crudo)})")
    log("\nETAPA 3/3 — LAS NUEVE PUERTAS (ERR-89: una linea por puerta del preregistro)")
    V = puertas(R)
    log("\nTABLA (mediana por celda; acum = reproduccion desacoplada de la saciedad)")
    log(f"  {'brazo':10s} {'ac':2s} {'R0':>7} {'r':>7} {'vida':>8} {'cuerpos':>7} {'p1':>6} {'c1':>6} "
        f"{'t_ok':>7} {'sac':>6} {'expA':>6} {'fund':>6} {'div':>6}")
    for b in brazos:
        for a in acums:
            log(f"  {b:10s} {a:<2d} {str(m(R,b,a,'R0')):>7} {str(m(R,b,a,'r')):>7} {str(m(R,b,a,'vida_med')):>8} "
                f"{str(m(R,b,a,'cuerpos')):>7} {str(m(R,b,a,'p1')):>6} {str(m(R,b,a,'c1')):>6} "
                f"{str(m(R,b,a,'t_ok')):>7} {str(m(R,b,a,'sac_frac')):>6} {str(m(R,b,a,'exp_A')):>6} "
                f"{str(m(R,b,a,'fundadores')):>6} {str(m(R,b,a,'frac_div')):>6}")
    ver = os.path.join(DATOS, f"{pre}_veredicto_{sel}.json")
    json.dump(dict(sello=sel, crudo=os.path.basename(crudo), puertas=V,
                   pasan=[k for k, v in V.items() if v['pasa']], caen=[k for k, v in V.items() if not v['pasa']]),
              open(ver, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\nPUERTAS QUE PASAN: {[k for k,v in V.items() if v['pasa']]}")
    log(f"PUERTAS QUE CAEN : {[k for k,v in V.items() if not v['pasa']]}")
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
