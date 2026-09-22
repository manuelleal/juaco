"""Runner del MUNDO DE LA FASE 10 (F0_fable_solo). Ejecuta PREREGISTRO_mundo_fase10.md (la LETRA esta en UMBRALES, ERR-31).

MISION: llegar a la AGI por este camino. FASE 10: ¿hay un mundo donde un linaje mortal SOLO se sostiene si transmite y
donde lo transmitido tiene que crecer? Este runner mide el mundo disenado con el tronco v14.2 dentro, sin tocarle una regla.

    python corre_mundo_fase10.py --humo                      UN proceso, 6 corridas de T = 100 000, JSON en datos/humo/ (regla 3, ERR-42)
    python corre_mundo_fase10.py --serie --desde 2401 --pool 7 [--n 20] [--T 100000] [--brazos A,B,...]   SOLO el coordinador

POOL (ERR-86): --pool o la variable JUACO_POOL; por defecto 6. Los agentes no corren Pool (regla 3 de EQUIPO.md).
ERR-54: el crudo se guarda ANTES de analizar. ERR-87: lee_json exige prefijo + SELLO EXACTO. ERR-89: una linea por puerta.
Regla 14: CUERPO y NODO son campo a campo los de corre_f9.py (el arnes identidad_mundo_fase10.py lo comprueba).

LOS DOCE BRAZOS (todos en el MISMO mundo salvo MUNDO_FIJO; todos mortales salvo RENACE):
  RENACE            inmortal en memoria (muerte_real=0), con mapa: la COTA SUPERIOR del mundo (ancla V-6: 0.80-1.30).
  NADA              el tronco solo: sin nodo, SIN mapa (ancla V-6: 0.10-0.30; M10-1: < 0.5).
  SIN_HERENCIA      sin nodo, CON mapa: cada cuerpo nace vacio pero recuerda donde vio las cosas (V-4: una vida < 50 %).
  REL               EL CANDIDATO: nodo por relevancia viva + mapa (M10-1: R0 >= 1.0 en >= 15/20 con fundadores <= 2).
  REL_SIN_MAPA      nodo por relevancia, sin mapa (se reporta: cuanto vale 'donde').
  NODO_BARAJADO     REL con las recompensas del nodo permutadas (M10-1: < 0.5; M10-2: <= 1.2x).
  ORACULO           nodo con la TABLA VERDADERA + mapa (V-2: >= 1; cota del conocimiento).
  ORACULO_SIN_MAPA  tabla verdadera, sin mapa (V-2: < 1).
  MAPA_SIN_TABLA    mapa, sin nodo y SIN aprendizaje (learn=False; tambien apaga la locomocion aprendida: declarado) (V-2: < 1).
  MUNDO_FIJO        REL en el mundo BLANDO: sin cambios de valencia, parches que ni se agotan ni se mudan (M10-3: <= 1.2x).
  PLACEBO           REL consumiendo y descartando UN sorteo por paso (el nulo exacto, ERR-91): valez de los margenes.
  REL_D0            REL con desambiguar=0 (v14.1): el alias sin reparar (V-3: alias cuesta vidas).

VOCABULARIO (regla 6): "cuerpo", "linaje", "nodo del linaje", "R0 del linaje", "cuerpo k-esimo de la corrida" (NO "generacion"
hasta que este medida), "cobertura de la tabla", "combinaciones explotadas". Prohibido: "poblacion", "cultura", "ensena",
"evoluciona", "planifica", "entiende".
"""
import sys, os, json, time, hashlib, platform, re, statistics as st

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
JUACO = r'C:\Users\User\Documents\PROYECTOS\JUACO\bundle'
EXP = os.path.join(JUACO, 'experimentos')
sys.path[:0] = [AQUI, os.path.join(JUACO, 'organismo'), os.path.join(EXP, 'nivel09_cuerpo_nuevo'), os.path.join(EXP, 'nivel13_alma'),
                os.path.join(EXP, 'nivel11_mundo_vivo')]   # organismo/ antes que los experimentos (ERR-28)
import mundo_fase10 as M10

T = 100000
T_HUMO = 100000
N_SEM = 20
DESDE = 2401                       # serie 2401-2420; replica 2421-2440 (grep en experimentos/, registro/, datos/: libres al 21-sep)
DATOS = os.path.join(AQUI, 'datos')
HUMO = os.path.join(DATOS, 'humo')
GRANDE = 10 ** 9
SHA_ESPERADOS = dict(f9='3a821884394d66c9', v142='17528d767fcebaf6', v14='feefc88b1fd8d434', vivo_codigo='839fa71f9c84cb26',
                     f9c='9dd1fb91ecec35ae', mundo_mapa='207d6a1954336b18', v3cal='148014f68cb01785', familias='b9dd561a0cf056b8',
                     alma2='4fd616aeaf535e61', h1='9e99ff87b5e2db1e', rep2='96feb4918dc5d694')

# ------------------------------------------------------------------ EL MUNDO: 4 familias x 4 variantes = 16 tipos en 10 pixeles
FAM = {'A': [1, 1, 0, 1, 0, 0], 'B': [1, 0, 1, 0, 1, 0], 'C': [0, 1, 1, 0, 0, 1], 'D': [0, 0, 1, 0, 1, 1]}   # los 4 patrones del tronco
VAR = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]                                                  # variante one-hot
VAL_FAM = {'A': 'comida', 'B': 'veneno', 'C': 'agua', 'D': 'sal'}
PAT16, VAL16 = {}, {}
for _f, _p in FAM.items():
    for _i, _v in enumerate(VAR):
        _k = _f if _i == 0 else _f + str(_i)          # 'A','A1','A2','A3',...: la variante 0 conserva el nombre del tronco (cond() usa 'A' y 'B')
        PAT16[_k] = np.array(_p + _v, float); VAL16[_k] = VAL_FAM[_f]
TIPOS = tuple(PAT16)
MUNDO = dict(pats=PAT16, vals=VAL16, estims=TIPOS, r_vis=8, usa_M=1, escribe_M=1, olvida_M=1, parches=6, cap=5, regen=30,
             vida_parche=8000, cambia_cada=5000, cambia_fam=4, f10=1, desambiguar=1)   # fijado tras la calibracion (REGISTRO 20:08-20:13)

# ------------------------------------------------------------------ EL CUERPO (regla 14: campo a campo = corre_f9.CUERPO / NODO)
CUERPO = dict(vivo=1, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001, n_nec=2, rep_cuello=2, reproduccion=1, rep_mide=1,
              rep_X=500, rep_umbral=1.0, rep_coste=0.0, rep2=1, rep2_regalo=600, h1=1, muerte_real=1, hereda='nada', dote=0.6)


def curita_f(res):
    """El alma NULA (fase 9): el nodo y la conexion son MECANISMO, no curita elegida."""
    return {'curita': 'f', 'motivo': 'fase 10: sin alma, el mecanismo es el nodo'}


NODO = dict(alma=curita_f, alma_muertes=GRANDE, menu='f', f9=1, nodo_k=20, nodo_lee=50)


def brazo(**kw):
    b = dict(CUERPO); b.update(MUNDO); b.update(NODO); b.update(nodo=1, conectado=1, nodo_rel=1); b.update(kw)
    return b


BRAZOS = {
    'RENACE':           dict(dict(CUERPO, **MUNDO), muerte_real=0, hereda='nada'),
    'NADA':             brazo(nodo=0, conectado=0, nodo_rel=0, usa_M=0, olvida_M=0),
    'SIN_HERENCIA':     brazo(nodo=0, conectado=0, nodo_rel=0),
    'REL':              brazo(),
    'REL_SIN_MAPA':     brazo(usa_M=0, olvida_M=0),
    'NODO_BARAJADO':    brazo(nodo_baraja=1),
    'ORACULO':          brazo(nodo_or=1),
    'ORACULO_SIN_MAPA': brazo(nodo_or=1, usa_M=0, olvida_M=0),
    'MAPA_SIN_TABLA':   brazo(nodo=0, conectado=0, nodo_rel=0, learn=False),
    'MUNDO_FIJO':       brazo(cambia_cada=0, vida_parche=0, cap=GRANDE),
    'PLACEBO':          brazo(placebo=1),
    'REL_D0':           brazo(desambiguar=0),
}
ORDEN = list(BRAZOS)
CUERPOS_G1 = (1,)            # "la 1.a generacion": el primer cuerpo de la corrida (el unico que con certeza no leyo nada)
CUERPOS_G5 = tuple(range(5, 13))   # "la 5.a generacion": los cuerpos 5..12 de la corrida (mediana), que leen lo que dejaron >= 4 cuerpos

# ------------------------------------------------------------------ LA LETRA (ERR-31): umbrales escritos ANTES de correr
UMBRALES = {
    'V-1': dict(frase="RECURSOS QUE SE AGOTAN Y SE MUEVEN: ningun parche se queda mas de T/4 en su sitio (todos los brazos salvo MUNDO_FIJO, "
                      "que DEBE fallar)", frac_T=0.25),
    'V-2': dict(frase="SABER DONDE VALE TANTO COMO SABER QUE: R0(ORACULO_SIN_MAPA) < 1 y R0(MAPA_SIN_TABLA) < 1 y R0(ORACULO) >= 1 (medianas)",
                R0_uno=1.0),
    'V-3': dict(frase="EL ALIAS CUESTA VIDAS: sin desambiguar (REL_D0), tasa de mordida de lo malo CON alias >= 2x la de lo malo SIN alias "
                      "(mordidas/exposiciones agregadas; exposiciones reportadas, trampa 3)", razon=2.0, exp_min=20),
    'V-4': dict(frase="UNA VIDA NO ALCANZA, UN LINAJE SI: cobertura de la tabla al morir, mediana de SIN_HERENCIA < 0.50; cuerpos 5..12 de REL > 0.80",
                una_vida=0.50, linaje=0.80),
    'V-5': dict(frase="MAS DE UN CUERPO A LA VEZ: opcion DECLARADA (cola de descendientes, un cuerpo vivo); no se mide ni se nombra hasta medirla"),
    'V-6': dict(frase="ANCLA (BLOQUEANTE): el coste de vida conserva el ancla del mundo vivo -- R0 NADA en [0.10, 0.30] y R0 RENACE en [0.80, 1.30]",
                R0_NADA=(0.10, 0.30), R0_RENACE=(0.80, 1.30)),
    'M10-1': dict(frase="SOSTEN: REL cruza R0 >= 1.0 con fundadores <= 2 en >= 15/20 semillas; NADA < 0.5; NODO_BARAJADO < 0.5 (medianas)",
                  R0=1.0, fund=2, k=15, ctl=0.5),
    'M10-2': dict(frase="ACUMULACION: combinaciones (tipo x cuarto) explotadas por los cuerpos 5..12 >= 2x las del cuerpo 1, pareado por semilla "
                        "(mediana de razones >= 2.0 y A12 pareado >= 0.85, n >= 15); NODO_BARAJADO <= 1.2x", razon=2.0, A12=0.85, n_min=15, ctl=1.2),
    'M10-3': dict(frase="NO ES EL MUNDO BLANDO: en MUNDO_FIJO la razon cuerpos 5..12 / cuerpo 1 <= 1.2x", ctl=1.2),
    'M10-4': dict(frase="NO REGRESION: perillas apagadas == tronco v14.2 BIT A BIT y el mapa INERTE sin r_vis (identidad_mundo_fase10.py, "
                        "pegado en el preregistro); las baterias las corre el coordinador; coste 1.00x por identidad"),
    'M10-5': dict(frase="REPRESENTACION (se reporta, no es puerta): celdas al morir, divisiones B-5, pares alias (bueno,malo) al nacer y al morir"),
    'PLAC': dict(frase="VALIDEZ DEL NULO: |R0 PLACEBO - R0 REL| <= 0.15 y A12(R0 PLACEBO vs REL) en [0.35, 0.65]; razon M10-2 de PLACEBO en "
                       "[0.8, 1.25] x la de REL", d_R0=0.15, A12=(0.35, 0.65), rz=(0.8, 1.25)),
}

# ------------------------------------------------------------------ utilidades
LOG = [None]


def log(msg=""):
    print(msg, flush=True)
    if LOG[0]:
        LOG[0].write(msg + "\n"); LOG[0].flush(); os.fsync(LOG[0].fileno())


def sello():
    return time.strftime('%Y%m%d_%H%M%S')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def lee_json(carpeta, prefijo, sel):
    """ERR-87: prefijo + SELLO EXACTO. Sin sello no se lee nada."""
    ruta = os.path.join(carpeta, f"{prefijo}_{sel}.json")
    if not os.path.exists(ruta):
        raise SystemExit(f"lee_json: no existe {ruta} (prefijo + sello EXACTO, ERR-87)")
    return json.load(open(ruta, encoding='utf-8')), ruta


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 3) if xs else None


def razon(x, y):
    return None if (x is None or not y) else round(x / y, 3)


def A12(a, b):
    """P(a > b) + 0.5 P(a = b) sobre TODOS los pares (n x m), sin parear (la de corre_vivo_rep / corre_f9)."""
    a = [x for x in a if x is not None]; b = [y for y in b if y is not None]
    if not a or not b:
        return None
    return round(sum((x > y) + 0.5 * (x == y) for x in a for y in b) / (len(a) * len(b)), 3)


def A12_par(pares):
    """PAREADO por semilla: fraccion de semillas con x > y (+0.5 empates). Nulo = 0.50."""
    p = [(x, y) for x, y in pares if x is not None and y is not None]
    return round(sum((x > y) + 0.5 * (x == y) for x, y in p) / len(p), 3) if p else None


def ge(x, u): return x is not None and x >= u
def le(x, u): return x is not None and x <= u
def lt(x, u): return x is not None and x < u
def dentro(x, lo, hi): return x is not None and lo <= x <= hi


# ------------------------------------------------------------------ una corrida -> resumen de solo lectura
def resumen(brazo, seed, r, Ti, seg):
    d, mu = r['descendientes'], r['deaths']
    vidas = r.get('vidas_h1') or r.get('vidas') or []
    f = r.get('f9') or {}
    f10 = r.get('f10') or {}
    C = f10.get('cuerpos') or []
    c1 = [c for c in C if c['cuerpo'] in CUERPOS_G1]
    c5 = [c for c in C if c['cuerpo'] in CUERPOS_G5]
    fr = lambda c: round(c['expl'] / max(4 * c['n_bue'], 1), 4)
    pe = [sum(c['pe'][i] for c in C) for i in (0, 1)]; pb = [sum(c['pb'][i] for c in C) for i in (0, 1)]
    causas = {k: sum(1 for c in C if c['causa'] == k) for k in ('alias', 'limpio', 'drenaje')}
    o = dict(brazo=brazo, seed=seed, seg=round(seg, 2), descendientes=d, muertes=mu, R0=round(d / (mu + 1), 4), r=d - mu,
             vida_med=med(vidas), cuerpos=len(vidas), fundadores=r.get('fundadores'), muertes_nec=r.get('muertes_nec'),
             p1=med([x for x in f.get('p1', []) if x >= 0]) if f else None, c1=med([x for x in f.get('c1', []) if x >= 0]) if f else None,
             sac_frac=razon(r.get('pasos_viables'), r.get('T_efectivo') or Ti),
             lect_div=f.get('lect_div'), lecturas=f.get('lecturas'), frac_div=razon(f.get('lect_div'), f.get('lecturas')),
             # F10
             n_cuerpos_f10=len(C), pmax=f10.get('parche_max_estancia'), n_cambios=f10.get('n_cambios'),
             cob1=med([c['cob_s'] for c in c1]), cob5=med([c['cob_s'] for c in c5]), cob_c5=med([c['cob_c'] for c in c5]),
             cob_todos=med([c['cob_s'] for c in C]),
             expl1=med([fr(c) for c in c1]), expl5=med([fr(c) for c in c5]), expl_t5=med([c['expl_t'] for c in c5]),
             enc1=med([c['enc'] for c in c1]), enc5=med([c['enc'] for c in c5]), vida1=med([c['vida'] for c in c1]), vida5=med([c['vida'] for c in c5]),
             pe_alias=pe[0], pe_limpio=pe[1], pb_alias=pb[0], pb_limpio=pb[1],
             tasa_alias=razon(pb[0], pe[0]), tasa_limpio=razon(pb[1], pe[1]), causas=causas,
             celdas=med([c['celdas'] for c in C]), des=sum(c['des'] for c in C), alias_nac=med([c['alias_nac'] for c in C]),
             alias_fin=med([c['alias_fin'] for c in C]), sep=med([c['alias_nac'] - c['alias_fin'] for c in C]),
             alias_fundador=f10.get('alias_nac_fundador'), M_llenas=f10.get('M_llenas'),
             exposiciones=sum((r.get('exposiciones') or {}).values()), mordidas=sum(sum(v) for v in r['mord'].values()),
             T_efectivo=r.get('T_efectivo'))
    o['rz'] = (razon(o['expl5'], o['expl1']) if (o['expl1'] not in (None, 0) and o['expl5'] is not None) else None)
    org = r.get('origen_cuerpo') or []
    ok = (r.get('nacimientos') == mu and len(vidas) == mu + 1 and len(r.get('desc_por_vida') or []) == mu + 1 and len(org) == mu + 1
          and sum(vidas) == (r.get('T_efectivo') or Ti) and sum(r.get('desc_por_vida') or []) == d
          and (r.get('fundadores') or 0) + 1 == sum(1 for g in org if not g))
    o['coherente'] = bool(ok) if r.get('muerte_real') else None
    o['f10_len'] = (len(C) == mu)
    return o


def tarea(args):
    brazo_, seed, Ti = args
    t0 = time.time()
    r = M10.run(seed, T=Ti, **BRAZOS[brazo_])
    return resumen(brazo_, seed, r, Ti, time.time() - t0)


# ------------------------------------------------------------------ las puertas (ERR-89: una linea por puerta)
def cel(R, b, campo):
    return [x[campo] for x in R if x['brazo'] == b and x.get(campo) is not None]


def m(R, b, campo):
    return med(cel(R, b, campo))


def puertas(R, Ti, log=log):
    V, U = {}, UMBRALES

    def linea(p, ok, txt):
        V[p] = dict(pasa=(None if ok is None else bool(ok)), detalle=txt, frase=U[p]['frase'])
        log(f"  {p:6s} {'REPORTA' if ok is None else ('PASA' if ok else 'CAE ')}  {U[p]['frase']}")
        log(f"          {txt}")

    hay = lambda *bs: all(cel(R, b, 'R0') for b in bs)
    # V-6 ANCLA (bloqueante)
    u = U['V-6']; a = dict(R0_NADA=m(R, 'NADA', 'R0'), R0_RENACE=m(R, 'RENACE', 'R0'))
    ok6 = all(dentro(a[k], *u[k]) for k in a)
    linea('V-6', ok6, " · ".join(f"{k} {a[k]} en [{u[k][0]}, {u[k][1]}]" for k in a)
          + f" · vida NADA {m(R,'NADA','vida_med')} · vida RENACE {m(R,'RENACE','vida_med')} · muertes_nec NADA {m(R,'NADA','muertes_nec') if False else [x['muertes_nec'] for x in R if x['brazo']=='NADA'][:3]}")
    # V-1
    lim = int(U['V-1']['frac_T'] * Ti)
    mov = [b for b in ORDEN if b != 'MUNDO_FIJO' and cel(R, b, 'pmax')]
    viol = [(b, x['seed'], x['pmax']) for b in mov for x in R if x['brazo'] == b and x['pmax'] is not None and x['pmax'] > lim]
    fijo = cel(R, 'MUNDO_FIJO', 'pmax')
    ok1 = (bool(mov) and not viol) and (not fijo or all(p > lim for p in fijo))
    linea('V-1', ok1, f"estancia maxima de un parche <= {lim}: violaciones {viol[:4] or 'ninguna'} en {len(mov)} brazos · MUNDO_FIJO (debe fallar) {fijo[:3]}")
    # V-2
    u = U['V-2']
    ok2 = lt(m(R, 'ORACULO_SIN_MAPA', 'R0'), u['R0_uno']) and lt(m(R, 'MAPA_SIN_TABLA', 'R0'), u['R0_uno']) and ge(m(R, 'ORACULO', 'R0'), u['R0_uno']) if hay('ORACULO', 'ORACULO_SIN_MAPA', 'MAPA_SIN_TABLA') else None
    linea('V-2', ok2, f"R0 ORACULO_SIN_MAPA {m(R,'ORACULO_SIN_MAPA','R0')} (< 1) · MAPA_SIN_TABLA {m(R,'MAPA_SIN_TABLA','R0')} (< 1) · ORACULO {m(R,'ORACULO','R0')} (>= 1) · "
                       f"vidas {m(R,'ORACULO_SIN_MAPA','vida_med')} / {m(R,'MAPA_SIN_TABLA','vida_med')} / {m(R,'ORACULO','vida_med')} · REL_SIN_MAPA R0 {m(R,'REL_SIN_MAPA','R0')} · muertes_nec ORACULO {[x['muertes_nec'] for x in R if x['brazo']=='ORACULO'][:3]}")
    # V-3
    u = U['V-3']
    pea, pel = sum(cel(R, 'REL_D0', 'pe_alias')), sum(cel(R, 'REL_D0', 'pe_limpio'))
    pba, pbl = sum(cel(R, 'REL_D0', 'pb_alias')), sum(cel(R, 'REL_D0', 'pb_limpio'))
    ta, tl = razon(pba, pea), razon(pbl, pel)
    ok3 = (ge(razon(ta, tl), u['razon']) if (pea >= u['exp_min'] and pel >= u['exp_min']) else None) if hay('REL_D0') else None
    ta1, tl1 = razon(sum(cel(R, 'REL', 'pb_alias')), sum(cel(R, 'REL', 'pe_alias'))), razon(sum(cel(R, 'REL', 'pb_limpio')), sum(cel(R, 'REL', 'pe_limpio')))
    linea('V-3', ok3, f"REL_D0: tasa de mordida de lo malo CON alias {ta} ({pba}/{pea}) vs SIN alias {tl} ({pbl}/{pel}) -> razon {razon(ta, tl)} (>= {u['razon']}) · "
                       f"REL (B-5): {ta1} vs {tl1} · muertes por causa REL_D0 {[x['causas'] for x in R if x['brazo']=='REL_D0'][:2]}")
    # V-4
    u = U['V-4']
    v4a, v4b = m(R, 'SIN_HERENCIA', 'cob_todos'), m(R, 'REL', 'cob5')
    ok4 = (lt(v4a, u['una_vida']) and ge(v4b, u['linaje'])) if hay('SIN_HERENCIA', 'REL') else None
    linea('V-4', ok4, f"cobertura al morir (signo): SIN_HERENCIA todos los cuerpos {v4a} (< {u['una_vida']}) · REL cuerpos 5..12 {v4b} (> {u['linaje']}) · "
                       f"REL con criterio |v|>=0.5 {m(R,'REL','cob_c5')} · NADA {m(R,'NADA','cob_todos')} · NODO_BARAJADO 5..12 {m(R,'NODO_BARAJADO','cob5')} · ORACULO 5..12 {m(R,'ORACULO','cob5')}")
    linea('V-5', None, "opcion declarada en el preregistro (cola FIFO de descendientes, un cuerpo vivo a la vez); nada medido, nada nombrado")
    # M10-1
    u = U['M10-1']
    rel = [x for x in R if x['brazo'] == 'REL']
    k = sum(1 for x in rel if x['R0'] >= u['R0'] and (x['fundadores'] or 0) <= u['fund'])
    okm1 = (k >= u['k'] and lt(m(R, 'NADA', 'R0'), u['ctl']) and lt(m(R, 'NODO_BARAJADO', 'R0'), u['ctl'])) if hay('REL', 'NADA', 'NODO_BARAJADO') else None
    linea('M10-1', okm1, f"REL: R0 >= {u['R0']} con fundadores <= {u['fund']} en {k}/{len(rel)} (>= {u['k']}) · mediana R0 REL {m(R,'REL','R0')} fund {m(R,'REL','fundadores')} vida {m(R,'REL','vida_med')} · "
                          f"NADA {m(R,'NADA','R0')} (< {u['ctl']}) · NODO_BARAJADO {m(R,'NODO_BARAJADO','R0')} (< {u['ctl']}) · SIN_HERENCIA {m(R,'SIN_HERENCIA','R0')} · REL_SIN_MAPA {m(R,'REL_SIN_MAPA','R0')} · ORACULO {m(R,'ORACULO','R0')}")
    # M10-2
    u = U['M10-2']
    pares = [(x['expl5'], x['expl1']) for x in rel]
    rz = [x['rz'] for x in rel if x['rz'] is not None]
    a12 = A12_par(pares)
    okm2 = (ge(med(rz), u['razon']) and ge(a12, u['A12']) and len(rz) >= u['n_min'] and le(m(R, 'NODO_BARAJADO', 'rz'), u['ctl'])) if hay('REL', 'NODO_BARAJADO') else None
    linea('M10-2', okm2, f"REL: razon explotadas cuerpos 5..12 / cuerpo 1: mediana {med(rz)} (>= {u['razon']}), n {len(rz)} (>= {u['n_min']}), A12 pareado {a12} (>= {u['A12']}) · "
                          f"expl1 {m(R,'REL','expl1')} expl5 {m(R,'REL','expl5')} · exposiciones cuerpo 1 {m(R,'REL','enc1')} vs 5..12 {m(R,'REL','enc5')} (trampa 3) · vidas {m(R,'REL','vida1')} vs {m(R,'REL','vida5')} · "
                          f"NODO_BARAJADO razon {m(R,'NODO_BARAJADO','rz')} (<= {u['ctl']}) · NADA {m(R,'NADA','rz')} · SIN_HERENCIA {m(R,'SIN_HERENCIA','rz')} · ORACULO {m(R,'ORACULO','rz')}")
    # M10-3
    u = U['M10-3']
    okm3 = le(m(R, 'MUNDO_FIJO', 'rz'), u['ctl']) if hay('MUNDO_FIJO') else None
    linea('M10-3', okm3, f"MUNDO_FIJO: razon 5..12 / 1 {m(R,'MUNDO_FIJO','rz')} (<= {u['ctl']}) · R0 {m(R,'MUNDO_FIJO','R0')} vida {m(R,'MUNDO_FIJO','vida_med')} cob 5..12 {m(R,'MUNDO_FIJO','cob5')} · "
                          f"(razon 5..12 / 2..4 se reporta como M10-3': no calculada aqui, ver crudo)")
    linea('M10-4', None, "identidad y coste por arnes (identidad_mundo_fase10.py, pegado en el preregistro); bateria_v142 y bateria_generaliza_v142 las corre el coordinador")
    linea('M10-5', None, f"celdas al morir REL {m(R,'REL','celdas')} vs NADA {m(R,'NADA','celdas')} vs RENACE {m(R,'RENACE','celdas')} · divisiones B-5 (suma) REL {m(R,'REL','des')} REL_D0 {m(R,'REL_D0','des')} · "
                          f"pares alias (bueno,malo) al nacer {m(R,'REL','alias_nac')} al morir {m(R,'REL','alias_fin')} sep {m(R,'REL','sep')} · RENACE sep {m(R,'RENACE','sep')}")
    # PLACEBO
    u = U['PLAC']
    d = (abs(m(R, 'PLACEBO', 'R0') - m(R, 'REL', 'R0')) if hay('PLACEBO', 'REL') else None)
    ap = A12(cel(R, 'PLACEBO', 'R0'), cel(R, 'REL', 'R0'))
    rzp = razon(m(R, 'PLACEBO', 'rz'), m(R, 'REL', 'rz'))
    okp = (le(d, u['d_R0']) and dentro(ap, *u['A12']) and (rzp is None or dentro(rzp, *u['rz']))) if hay('PLACEBO', 'REL') else None
    linea('PLAC', okp, f"|R0 PLACEBO - REL| {None if d is None else round(d, 4)} (<= {u['d_R0']}) · A12 {ap} en {list(u['A12'])} · razon M10-2 PLACEBO/REL {rzp} en {list(u['rz'])} · "
                        f"PLACEBO pasa M10-1 como REL: {sum(1 for x in R if x['brazo']=='PLACEBO' and x['R0']>=1.0 and (x['fundadores'] or 0)<=2)}/{len(cel(R,'PLACEBO','R0'))}")
    return V


# ------------------------------------------------------------------ identidad dentro del runner (regla 14, ERR-38)
def identidad_corta(Ti=20000, sem=(1,)):
    import organismo_f9 as F9, organismo_v142 as V142, corre_f9 as CF
    out = []
    for k in set(CF.CUERPO) | set(CUERPO):
        if N(CF.CUERPO.get(k)) != N(CUERPO.get(k)):
            out.append((f'(0) regla 14: CUERPO campo {k}', False, f"{CF.CUERPO.get(k)} vs {CUERPO.get(k)}"))
    for k in ('alma_muertes', 'menu', 'f9', 'nodo_k', 'nodo_lee'):
        if N(CF.NODO[k]) != N(NODO[k]):
            out.append((f'(0) regla 14: NODO campo {k}', False, f"{CF.NODO[k]} vs {NODO[k]}"))
    out.append(('(0) regla 14: CUERPO y NODO campo a campo == corre_f9', not out, f"{len(CF.CUERPO)} + {len(CF.NODO)} campos"))
    NUEV = {'desambiguar', 'des_splits', 'des_t'}
    for s in sem:
        a = F9.run(s, T=Ti, **CF.BRAZOS['NADA']); b = M10.run(s, T=Ti, desambiguar=0, **CF.BRAZOS['NADA'])
        dif = [k for k in a if k in b and N(a[k]) != N(b[k])] + [k for k in a if k not in b] + [k for k in b if k not in a and k not in NUEV]
        out.append(('(1) mundo del tronco: NADA (desambiguar=0) == organismo_f9 NADA (= NADA_CM de H-1)', not dif, f"dif {dif[:4]}"))
        a = V142.run(s, T=Ti); b = M10.run(s, T=Ti)
        dif = [k for k in a if k in b and N(a[k]) != N(b[k])] + [k for k in a if k not in b] + [k for k in b if k not in a]
        out.append(('(2) mundo del tronco: perillas apagadas == organismo_v142 (TRONCO v14.2), todas las claves', not dif, f"dif {dif[:4]}"))
        rel = M10.run(s, T=Ti, **BRAZOS['REL']); nada = M10.run(s, T=Ti, **BRAZOS['NADA']); bar = M10.run(s, T=Ti, **BRAZOS['NODO_BARAJADO'])
        out.append(('(3) mundo F10: REL != NADA y REL != NODO_BARAJADO (DEBEN diferir, ERR-38)', N(rel) != N(nada) and N(rel) != N(bar),
                    f"lect_div REL {rel['f9']['lect_div']}/{rel['f9']['lecturas']} · R0 REL {rel['descendientes']}/{rel['deaths']+1} NADA {nada['descendientes']}/{nada['deaths']+1}"))
        smp = M10.run(s, T=Ti, **BRAZOS['REL_SIN_MAPA'])
        out.append(('(4) mundo F10: el mapa actua (REL != REL_SIN_MAPA) y el mundo cambia (n_cambios > 0)', N(rel) != N(smp) and rel['f10']['n_cambios'] > 0,
                    f"n_cambios {rel['f10']['n_cambios']} · M_llenas {rel['f10']['M_llenas']}"))
    return out


# ------------------------------------------------------------------ humo (UN proceso, 6 corridas)
HUMO_CORRIDAS = [('RENACE', 1), ('NADA', 1), ('REL', 1), ('REL', 2), ('ORACULO', 1), ('ORACULO_SIN_MAPA', 1)]


def humo(Ti=T_HUMO):
    os.makedirs(HUMO, exist_ok=True)
    sel = sello(); pre = 'mundo_fase10_humo'
    LOG[0] = open(os.path.join(HUMO, f"{pre}_{sel}.log"), 'w', encoding='utf-8')
    t0 = time.time()
    log(f"HUMO MUNDO FASE 10 · {time.strftime('%Y-%m-%d %H:%M:%S')} · UN proceso, sin Pool (regla 3) · 6 corridas de T={Ti}")
    log(f"  mundo_fase10.py sha {h16(os.path.join(AQUI,'mundo_fase10.py'))} · runner sha {h16(os.path.abspath(__file__))} · origen f9 {SHA_ESPERADOS['f9']} · python {platform.python_version()} numpy {np.__version__}")
    log(f"  MUNDO: {', '.join(f'{k}={v}' for k, v in MUNDO.items() if k not in ('pats', 'vals', 'estims'))} · {len(PAT16)} tipos en {len(next(iter(PAT16.values())))} pixeles")
    log("\nETAPA 1/3 — identidad dentro del runner (regla 14, ERR-38)")
    ide = identidad_corta(20000, (1,))
    for et, ok, det in ide:
        log(f"  {'OK  ' if ok else 'FALLA'} {et}   {det}")
    if not all(ok for _, ok, _ in ide):
        log("  IDENTIDAD FALLA -> el humo NO sigue.")
        json.dump(dict(identidad=[[e, bool(o), d] for e, o, d in ide], ok=False), open(os.path.join(HUMO, f"{pre}_{sel}.json"), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return 1
    log(f"\nETAPA 2/3 — 6 corridas: {HUMO_CORRIDAS}")
    R = []
    for b, s in HUMO_CORRIDAS:
        x = tarea((b, s, Ti)); R.append(x)
        log(f"  [{time.time()-t0:6.1f}s] {b:17s} s{s}  R0 {x['R0']:<7} desc {x['descendientes']:<4} muertes {x['muertes']:<4} fund {x['fundadores']} vida {x['vida_med']:<7} "
            f"mnec {x['muertes_nec']} cob1 {x['cob1']} cob5 {x['cob5']} expl1 {x['expl1']} expl5 {x['expl5']} rz {x['rz']} enc1/5 {x['enc1']}/{x['enc5']} "
            f"causas {x['causas']} pmax {x['pmax']} cambios {x['n_cambios']} alias t {x['tasa_alias']}/{x['tasa_limpio']} coh {x['coherente']} f10 {x['f10_len']}")
    log("\nETAPA 3/3 — predicciones del humo (HH1..HH6, escritas en el PREREGISTRO antes de lanzarlo)")
    g = lambda b, s: next(x for x in R if x['brazo'] == b and x['seed'] == s)
    hh = {}
    hh['HH1'] = all(x['coherente'] is not False for x in R) and all(x['f10_len'] for x in R)
    hh['HH2'] = all(x['lect_div'] and x['lect_div'] > 0 for x in R if x['brazo'] in ('REL', 'ORACULO', 'ORACULO_SIN_MAPA'))
    hh['HH3'] = g('RENACE', 1)['R0'] < 0.8
    hh['HH4'] = 0.03 <= g('NADA', 1)['R0'] <= 0.30
    hh['HH5'] = all(g('REL', s)['cob5'] is not None and g('REL', s)['cob1'] is not None and g('REL', s)['cob5'] > g('REL', s)['cob1'] for s in (1, 2))
    hh['HH6'] = all(x['pmax'] is not None and x['pmax'] <= Ti // 4 for x in R)
    for k, v in hh.items():
        log(f"  {k}: {'SI' if v else 'NO'}")
    log("  Solo HH1, HH2 y HH6 BLOQUEAN (son el instrumento). HH3, HH4 y HH5 son la HIPOTESIS: si fallan se anotan; NINGUN umbral cambia (regla 4).")
    log("\nPUERTAS sobre el humo (orientativo: n = 1-2 semillas, sin valor de veredicto)")
    puertas(R, Ti)
    ruta = os.path.join(HUMO, f"{pre}_{sel}.json")
    json.dump(dict(bloque='mundo_fase10_humo', sello=sel, T=Ti, corridas_plan=HUMO_CORRIDAS, mundo={k: v for k, v in MUNDO.items() if k not in ('pats', 'vals')},
                   tipos=list(PAT16), pixeles=len(next(iter(PAT16.values()))), sha_mundo=h16(os.path.join(AQUI, 'mundo_fase10.py')), sha_runner=h16(os.path.abspath(__file__)),
                   sha_origen=SHA_ESPERADOS, identidad=[[e, bool(o), d] for e, o, d in ide], corridas=R, HH=hh, ok=bool(hh['HH1'] and hh['HH2'] and hh['HH6']),
                   seg=round(time.time() - t0, 1)), open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\nJSON  {ruta}  (sha {h16(ruta)})")
    log(f"HUMO terminado en {time.time()-t0:.1f}s")
    return 0 if (hh['HH1'] and hh['HH2'] and hh['HH6']) else 1


# ------------------------------------------------------------------ la serie (SOLO el coordinador)
def serie(desde, n, Ti, pool, brazos):
    from multiprocessing import Pool
    os.makedirs(DATOS, exist_ok=True)
    sel = sello(); pre = f"mundo_fase10_s{desde}-{desde+n-1}"
    LOG[0] = open(os.path.join(DATOS, f"{pre}_{sel}.log"), 'w', encoding='utf-8')
    t0 = time.time()
    SEEDS = list(range(desde, desde + n))
    tareas = [(b, s, Ti) for b in brazos for s in SEEDS]
    log(f"MUNDO FASE 10 · {time.strftime('%Y-%m-%d %H:%M:%S')} · semillas {SEEDS[0]}-{SEEDS[-1]} · {len(brazos)} brazos x {n} = {len(tareas)} corridas de T={Ti}")
    log(f"  mundo_fase10.py sha {h16(os.path.join(AQUI,'mundo_fase10.py'))} · runner sha {h16(os.path.abspath(__file__))} · preregistro sha {h16(os.path.join(AQUI,'PREREGISTRO_mundo_fase10.md'))}")
    log(f"  Pool {pool} (ERR-86: --pool o JUACO_POOL)")
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
    json.dump(dict(bloque='mundo_fase10', sello=sel, desde=desde, n=n, T=Ti, brazos=brazos, mundo={k: v for k, v in MUNDO.items() if k not in ('pats', 'vals')}, tipos=list(PAT16),
                   sha_mundo=h16(os.path.join(AQUI, 'mundo_fase10.py')), sha_runner=h16(os.path.abspath(__file__)), sha_origen=SHA_ESPERADOS,
                   sha_prereg=h16(os.path.join(AQUI, 'PREREGISTRO_mundo_fase10.md')), identidad=[[e, bool(o), d] for e, o, d in ide], umbrales=N(UMBRALES), corridas=R),
              open(crudo, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"  crudo -> {crudo} (sha {h16(crudo)})")
    log("\nETAPA 3/3 — puertas (una linea por puerta, ERR-89)")
    V = puertas(R, Ti)
    bloq = V['V-6']['pasa']
    if not bloq:
        log("\n*** V-6 (ANCLA) CAE: el mundo no conserva el ancla del mundo vivo; las demas puertas se REPORTAN pero NO se declaran (como F9-1).")
    dec = [p for p in ('V-1', 'V-2', 'V-3', 'V-4', 'M10-1', 'M10-2', 'M10-3', 'PLAC') if V[p]['pasa'] is not None]
    log("\nVEREDICTO mundo_fase10: " + " ".join(f"{p}={'PASA' if V[p]['pasa'] else 'CAE'}" for p in ['V-6'] + dec) + f"  (ancla {'PASA' if bloq else 'CAE'})")
    vj = os.path.join(DATOS, f"{pre}_veredicto_{sel}.json")
    json.dump(dict(bloque='mundo_fase10_veredicto', sello=sel, crudo=os.path.basename(crudo), sha_crudo=h16(crudo), puertas=N(V), ancla=bool(bloq),
                   por_brazo={b: {c: m(R, b, c) for c in ('R0', 'r', 'vida_med', 'fundadores', 'cob1', 'cob5', 'expl1', 'expl5', 'rz', 'enc1', 'enc5', 'tasa_alias', 'tasa_limpio', 'celdas', 'sep', 'pmax')} for b in brazos},
                   sha_mundo=h16(os.path.join(AQUI, 'mundo_fase10.py')), sha_runner=h16(os.path.abspath(__file__)), seg=round(time.time() - t0, 1)),
              open(vj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"veredicto -> {vj} (sha {h16(vj)}) · {time.time()-t0:.0f}s")


if __name__ == '__main__':
    argv = sys.argv[1:]
    if '--humo' in argv:
        Ti = int(argv[argv.index('--T') + 1]) if '--T' in argv else T_HUMO
        sys.exit(humo(Ti))
    elif '--serie' in argv:
        desde = int(argv[argv.index('--desde') + 1]) if '--desde' in argv else DESDE
        n = int(argv[argv.index('--n') + 1]) if '--n' in argv else N_SEM
        Ti = int(argv[argv.index('--T') + 1]) if '--T' in argv else T
        pool = int(argv[argv.index('--pool') + 1]) if '--pool' in argv else int(os.environ.get('JUACO_POOL', '6'))
        brazos = argv[argv.index('--brazos') + 1].split(',') if '--brazos' in argv else ORDEN
        serie(desde, n, Ti, pool, brazos)
    else:
        print(__doc__)
