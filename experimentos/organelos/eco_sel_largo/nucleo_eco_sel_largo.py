"""nucleo_eco_sel_largo.py (CONSTRUIDO por experimentos/organelos/eco_sel_largo/construye_eco_sel_largo.py desde
experimentos/organelos/eco_sel/nucleo_eco_sel.py, sha 6a36e47ce61db3e1; NO editar a mano). ECO_SEL LARGO: + brazos SEL_MC y AZA_MC
(rep_umbral + 15 genes del cerebro, con y sin herencia), telemetria por ventanas de T/10 (_Tel, _extra_largo) y checkpoint cada
100 000 pasos. La LETRA esta en corre_eco_sel_largo.py; la del docstring de abajo NO rige aqui. Lo que sigue es el docstring del origen.

nucleo_eco_sel.py (CONSTRUIDO por experimentos/organelos/eco_sel/construye_eco_sel.py desde experimentos/organelos/frio/corre_frio.py,
sha 3ba8b0f5cf1fbbfa; NO editar a mano). ECO_SEL: F1 ARRANQUE EN FRIO + SELECCION NATURAL ENCIMA (sin vivero, sin fundadores
repuestos). Cambios: brazos y genetica de ECO_SEL (eco_de), vida y causas de la segunda mitad (vid), seleccion contra sombras
en T_SEL y en T (_extra_sel). La LETRA de ECO_SEL esta en corre_eco_sel.py; el uso y la letra que describe el docstring del
origen (abajo) NO rigen aqui. Lo que sigue es el docstring del origen.

corre_frio.py — RUNNER y LETRA de F1 ARRANQUE EN FRIO (comite de linaje, ficha F1; 25-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Meta del director: MANTENER EL LINAJE SIN ANDAMIO.

Preregistro: PREREGISTRO_frio.md (la letra esta AQUI, en veredicto(), y alli).
Envoltorio de experimentos/juaco_eco/corre_eco_v12.py (sha 1340d268e1fd93d8; se IMPORTA, no se toca): mismo mundo (w90: esc 90,
90 fundadores, quimiostato, tope 3000), misma plomeria de ECO (eco_cfg de corre_eco, banco, checkpoint cada 10 000), la misma
genetica MUT0 (sin mutacion) en todos los brazos. Lo unico que cambia por brazo es el CARRO y t_corte (fin del vivero):
  RES0_FRIO  MUT0 + FAMB_RES0_ECO, t_corte = 1      (sin vivero desde el inicio: el vivero solo podria refundar en t = 0)
  RES0_10k   MUT0 + FAMB_RES0_ECO, t_corte = 10 000 (dosis de vivero)
  RES0_60k   MUT0 + FAMB_RES0_ECO, t_corte = 60 000 (ANCLA: == MUT0_T de ECO v1.2 bit a bit; arnes bloque B)
  BAR0_FRIO  MUT0 + BAR0_ECO,      t_corte = 1      (control de contenido: la misma tabla con las R permutadas)
  FAB_FRIO   MUT0 + FABRICA_ECO,   t_corte = 1      (sin familia)
Motor: motor_frio_rapido.py (gemelo del arnes 132/132 copiado por anclas; + BAR0; ERR-146 guardia a 1e9). El motor Python solo en
el arnes.
nube-9 / ERR-60 (declarado ANTES de correr): trabajo() atrapa TODA excepcion del motor (SystemExit incluida) y devuelve un
resultado marcado en vez de matar al trabajador del Pool. Si el mensaje es la guardia ERR-60 (un linaje paso el limite de cuerpos):
el linaje estaba VIVO -> persiste = 1 con marca guardia = 1 (su R0 se calcula con la cohorte registrada hasta el aborto). Cualquier
otro aborto: persiste = None y la serie queda NO EVALUABLE.

Uso (ERR-115: banderas desconocidas o abreviadas abortan; --help no existe; SOLO el coordinador lanza --serie):
  python experimentos/organelos/frio/corre_frio.py --humo                                   # 1 proceso, 35905, 5 brazos, T 200 000
  python experimentos/organelos/frio/corre_frio.py --serie --desde 35001 --n 20 --pool 6    # serie
  python experimentos/organelos/frio/corre_frio.py --serie --desde 35021 --n 20 --pool 6    # replica
  python experimentos/organelos/frio/corre_frio.py --serie --desde 35001 --n 20 --pool 6 --reanuda
  python experimentos/organelos/frio/corre_frio.py --lee <carpeta de la serie>
"""
import argparse, glob, hashlib, importlib.util, json, os, pickle, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')
FRIO_DIR = os.path.join(RAIZ, 'experimentos', 'organelos', 'frio')   # ECO_SEL: el gemelo de F1 (motor_frio_rapido) se IMPORTA de alli
for _d in (ECO, FRIO_DIR, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_eco_v12 as V12      # importarlo deja CR.ME = motor Python (como en v1.2)
CR = V12.CR
ME_PY = V12.ME_PY
MUNDO = V12.MUNDO
SERIE = V12.SERIE
FAM = 'FAMB_RES0_ECO'; FAB = 'FABRICA_ECO'; BAR = 'BAR0_ECO'
FRIO = dict(T=1_000_000, T_lect=V12.V12['T_lect'], gen_largo=V12.V12['gen_largo'], coh_desde=10000, coh_margen=20000)
# ECO_SEL: los cinco brazos, TODOS en frio (t_corte = 1) con el carro de la familia (FAMB_RES0_ECO); solo cambia la genetica.
BRAZOS = {'F1': ('MUT0', FAM, 1), 'SEL_M': ('MARGEN', FAM, 1), 'AZA_M': ('MARGEN_AZAR', FAM, 1),
          'SEL_C': ('CEREBRO', FAM, 1), 'AZA_C': ('CEREBRO_AZAR', FAM, 1),
          'SEL_MC': ('MC', FAM, 1), 'AZA_MC': ('MC_AZAR', FAM, 1)}   # LARGO: margen + cerebro, con y sin herencia
FRIOS = tuple(BRAZOS)
VENTANAS = (45401, 45421)                 # LARGO: serie y replica
PRACTICA = tuple(range(45491, 45500))    # LARGO: humo 45491; el arnes usa 45492-45496
HUMO = dict(semilla=45491, T=200000)
# ECO_SEL: la genetica de cada brazo; la expresion es la de corre_eco.eco_cfg (banco 200, 8 sombras, p_mut 0.05, sigma 0.15, genes
# cada 2000). MUT0 = corre_eco.BRAZOS['MUT0'] (el F1). CEREBRO = corre_eco.BRAZOS['CEREBRO'] (15 genes: todos menos dote, rep_umbral
# y rep_X). MARGEN = SOLO rep_umbral: el margen m = 1 - rep_umbral entre la consigna del hambre del carro (hambre = clip(1 - E)) y el
# umbral de parto. *_AZAR = el mismo gen sin herencia: el genoma de todo cuerpo nuevo sale de una entrada AL AZAR del banco, mutada
# (donante 'azar' de motor_eco: el banco guarda el genoma NUEVO; el genoma nunca influye en su propia copia).
GENETICAS = {'MUT0': dict(mutables=None, donante='padre', p=False),
             'MARGEN': dict(mutables=('rep_umbral',), donante='padre', p=True),
             'MARGEN_AZAR': dict(mutables=('rep_umbral',), donante='azar', p=True),
             'CEREBRO': dict(mutables=CR.BRAZOS['CEREBRO']['mutables'], donante='padre', p=True),
             'CEREBRO_AZAR': dict(mutables=CR.BRAZOS['CEREBRO']['mutables'], donante='azar', p=True),
             # LARGO: MC = rep_umbral + los 15 del cerebro (dote y rep_X fijos), en el orden de motor_eco.NOMBRES
             'MC': dict(mutables=tuple(g for g in CR.ME.NOMBRES if g not in ('dote', 'rep_X')), donante='padre', p=True),
             'MC_AZAR': dict(mutables=tuple(g for g in CR.ME.NOMBRES if g not in ('dote', 'rep_X')), donante='azar', p=True)}
_SIGMA = [None]   # ECO_SEL: SOLO el arnes lo fija (sigma 0 -> el gen fijo == F1 bit a bit); None = SERIE['sigma']
_PMUT = [None]    # ECO_SEL: SOLO el arnes lo fija (p_mut 1 -> prueba de herencia); None = SERIE['p_mut']


def eco_de(gen, t_corte, **extra):
    """ECO_SEL: la expresion de corre_eco.eco_cfg con la genetica GENETICAS[gen] (arnes: == eco_cfg en MUT0 y CEREBRO)."""
    b = GENETICAS[gen]
    pm = SERIE['p_mut'] if _PMUT[0] is None else float(_PMUT[0])
    return dict(refunda=1, t_corte=t_corte, p_mut=(pm if b['p'] else 0.0), sigma=(SERIE['sigma'] if _SIGMA[0] is None else float(_SIGMA[0])),
                banco=SERIE['banco'], n_sombra=SERIE['n_sombra'], cada_gen=SERIE['cada_gen'], mutables=b['mutables'],
                donante=b['donante'], **extra)
DATOS = os.path.join(AQUI, 'datos')
_BAR0 = [None]


class BanderaMala(SystemExit):
    pass


def carga_bar0():
    """carros/BAR0_ECO.py por ruta, UNA vez por proceso, registrado en sys.modules (el pickle del checkpoint Python lo necesita)."""
    if _BAR0[0] is None:
        p = os.path.join(AQUI, 'carros', 'BAR0_ECO.py')
        spec = importlib.util.spec_from_file_location('BAR0_ECO', p)
        m = importlib.util.module_from_spec(spec); sys.modules['BAR0_ECO'] = m; spec.loader.exec_module(m)
        _BAR0[0] = m
    return _BAR0[0]


def carros_de(carro):
    """La lista de carros de run_solapadas: la de corre_eco_v12 (cadenas) para FAMB_RES0_ECO y FABRICA_ECO; (etiqueta, modulo) para BAR0."""
    if carro == BAR: return [(BAR, carga_bar0())] * MUNDO['n0']
    return [carro] * MUNDO['n0']


def usa_gemelo():
    """Enchufa motor_frio_rapido en CR.ME, como corre_eco_v12.usa_gemelo hace con motor_eco_rapido_fam."""
    import types
    import motor_frio_rapido as MF
    g = types.ModuleType('motor_frio_gemelo')
    g.__dict__.update({k: v for k, v in ME_PY.__dict__.items() if not k.startswith('__')})
    g.run_solapadas = MF.run_solapadas
    g._MF = MF
    CR.ME = g
    return MF


def nombre_motor():
    if CR.ME is ME_PY: return 'PYTHON motor_eco'
    return 'GEMELO motor_frio_rapido' if hasattr(CR.ME, '_MF') else 'GEMELO otro'


def trabajo(args):
    """UNA corrida (semilla, brazo) hasta T con el t_corte dado. Las claves de corre_eco_v12.trabajo (mismas expresiones) + las de F1.
    Atrapa toda excepcion del motor (nube-9). Checkpoint reanudable. Escribe su JSON."""
    seed, brazo, T, t_corte, T_lect, carpeta, reanuda = args
    gen_brazo, carro, _tc = BRAZOS[brazo]
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin): return json.load(open(fin, encoding='utf-8'))
    ck = os.path.join(carpeta, 'ckpt', f"{brazo}_s{seed}.pkl"); os.makedirs(os.path.dirname(ck), exist_ok=True)
    filas = []      # las de v1.2: nacidos (y refundados) con tn >= t_corte
    coh = []        # F1: (tn, hijos) de los NACIDOS (fund == 0) con tn >= coh_desde
    c0 = FRIO['coh_desde']
    vid = []        # ECO_SEL: (tn, tm, causa) de los NACIDOS (fund == 0) con tn >= T // 2 (vida y causas; descriptivo)
    tel = _Tel(T)   # LARGO: telemetria por ventanas de T/10

    def cb(li, row, g):
        if row[3] >= t_corte: filas.append([li] + row)
        if row[3] >= c0 and not row[6]: coh.append((row[3], row[5]))
        if row[3] >= T // 2 and not row[6]: vid.append((row[3], row[4], row[7]))   # ECO_SEL
        tel.cb(row, g)   # LARGO

    def guarda(t, blob):
        tmp = ck + '.tmp'
        with open(tmp, 'wb') as f: pickle.dump(dict(t=t, blob=blob, filas=filas, coh=coh, vid=vid, tel=tel.estado()), f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, ck)

    estado = None
    if reanuda and os.path.exists(ck):
        d = pickle.load(open(ck, 'rb')); estado = d['blob']; filas[:] = d['filas']; coh[:] = d['coh']; vid[:] = d['vid']; tel.carga(d['tel'])   # LARGO
    t0 = time.time()
    base = dict(seed=seed, brazo=brazo, genetica=gen_brazo, carro=carro, T=T, t_corte=t_corte, T_lect=T_lect)
    try:
        r = CR.ME.run_solapadas(seed, carros_de(carro), T=T, diag=0, mundo_n=MUNDO['esc'], tope_cuerpos=MUNDO['tope'],
                                muestra=MUNDO['muestra'],
                                eco=eco_de(gen_brazo, t_corte, ckpt_cada=CKPT_LARGO, ckpt_fn=guarda, estado=estado, ind_cb=cb))   # ECO_SEL
    except KeyboardInterrupt:
        raise
    except BaseException as ex:   # nube-9: NUNCA dejar que un SystemExit mate al trabajador del Pool
        msg = f"{type(ex).__name__}: {ex}"
        g60 = int('ERR-60' in msg)
        hasta = T - FRIO['coh_margen']
        cc = [h for tn, h in coh if tn <= hasta]
        res = dict(base, seg=round(time.time() - t0, 1), aborto=msg, guardia=g60, persiste=(1 if g60 else None), t_ext=None,
                   r0_nac=(round(float(np.mean(cc)), 4) if cc else None), n_coh_nac=len(cc), coh_nac=[c0, hasta],
                   bloqueados=0, n_refund=None, fundadores_rep=None, motor=nombre_motor(), lim_nac=_lim_nac())
        tmp = fin + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
        os.replace(tmp, fin)
        return res
    E = r['eco']; P = r['pista']
    fila_corte = next((f for f in E['gen_t'] if f[0] == t_corte), None)
    fila_lect = next((f for f in E['gen_t'] if f[0] == T_lect), None)
    te = E['t_ext']
    pers_lect = int(te is None or te > T_lect)
    cohv = [f for f in filas if f[4] <= T - 20000]
    vivos_t = [[f[0], f[1]] for f in E['gen_t'] if f[0] >= t_corte and f[0] % FRIO['gen_largo'] == 0]
    # ---- las claves de corre_eco_v12.trabajo, en su orden y con sus expresiones (arnes bloque B)
    res = dict(seed=seed, brazo=brazo, genetica=gen_brazo, carro=carro, T=T, t_corte=t_corte, T_lect=T_lect, seg=round(time.time() - t0, 1),
               t_ext=te, persiste=int(te is None and len(E['vivos_final']) > 0), persiste_lect=pers_lect,
               vivos_lect=(fila_lect[1] if fila_lect is not None else (0 if not pers_lect else None)),
               vivos_T=len(E['vivos_final']), linajes_T=len(set(v[0] for v in E['vivos_final'])),
               gen_max_T=(max(v[2] for v in E['vivos_final']) if E['vivos_final'] else None), vivos_t=vivos_t,
               bloqueados=P['bloqueados'], max_vivos=P['max_vivos'], n_nac=E['n_nac'], n_refund=E['n_refund'], n_banco=E['n_banco'],
               tasa_mut=(E['n_mut'] / max(1, (E['n_nac'] + E['n_banco'])) / len(E['genes'])),
               nac_post=len(filas), r0_post=(round(float(np.mean([f[6] for f in cohv])), 4) if cohv else None), n_coh_post=len(cohv),
               corte=E['corte'], sel_corte=CR.sel_genes(fila_corte),
               gen_t=[f for f in E['gen_t'] if f[0] <= T_lect or f[0] % FRIO['gen_largo'] == 0], tam_total=P['tam_total'],
               genes=E['genes'], G0=E['G0'], vivos_final=E['vivos_final'][:500], juez=None, juez_placebo=None,
               motor=nombre_motor())
    # ---- lo de F1
    hasta = T - FRIO['coh_margen']
    cc = [h for tn, h in coh if tn <= hasta]
    res.update(aborto=None, guardia=0, r0_nac=(round(float(np.mean(cc)), 4) if cc else None), n_coh_nac=len(cc), coh_nac=[c0, hasta],
               fundadores_rep=int(sum(d['fundadores'] for d in r['linajes'])),
               t_fund_primero=min((x for d in r['linajes'] for x in d['t_fund']), default=None),
               vivos_1k=[int(x) for x in P['tam_total'][:11]], lim_nac=_lim_nac(), **_extra_sel(vid, T, E), **_extra_largo(tel, E))   # ECO_SEL + LARGO
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck): os.remove(ck)
    return res


def _lim_nac():
    MF = getattr(CR.ME, '_MF', None)
    return int(MF.LIM_NAC) if MF is not None else 100000


# ================================================================================ ECO_SEL (anadido por construye_eco_sel.py)
T_SEL = 100000   # la prueba contra sombras se lee en t = 100 000 (~60 generaciones); a 1e6 la deriva de las sombras llena el rango


def _extra_sel(vid, T, E):
    """ECO_SEL: vida y causas de los NACIDOS en la segunda mitad; seleccion del BANCO contra sus 8 sombras (corre_eco.sel_genes) en T_SEL y
    en T; media de los genes mutables en los vivos en T; cuantos valores de genes NO mutables difieren de G0 en los vivos (debe ser 0)."""
    G = list(E['genes']); mut = list(E['mutables']); g0r = [round(float(x), 6) for x in E['G0']]
    fil = {f[0]: f for f in E['gen_t']}
    muertos = [tm - tn for tn, tm, c in vid if tm >= 0]
    cz = [0, 0, 0, 0]
    for tn, tm, c in vid:
        if tm >= 0 and 0 <= c < 4: cz[c] += 1
    V = [v[4:] for v in E['vivos_final']]
    fuera = sum(1 for g in V for j in range(len(G)) if G[j] not in mut and g[j] != g0r[j])
    movidos = sum(1 for g in V for j in range(len(G)) if G[j] in mut and g[j] != g0r[j])
    med = ({G[j]: round(float(np.mean([g[j] for g in V])), 6) for j in range(len(G)) if G[j] in mut} if V else None)
    return dict(mutables=mut, p_mut=E['p_mut'], sigma=E['sigma'], donante=E['donante'], n_mut=E['n_mut'],
                nac_2a=len(vid), vida_media_muertos_2a=(round(float(np.mean(muertos)), 1) if muertos else None),
                vivos_T_de_2a=sum(1 for tn, tm, c in vid if tm < 0), causas_2a=cz,
                sel_100k=CR.sel_genes(fil.get(T_SEL)), sel_T=CR.sel_genes(fil.get(T)),
                genes_vivos_T=med, fuera_mutables=int(fuera), movidos_mutables=int(movidos))


# ================================================================================ ECO_SEL LARGO (anadido por construye_eco_sel_largo.py)
CKPT_LARGO = 100000   # checkpoint cada 100 000 pasos (multiplo de cada_gen 2000: mismos tramos del gemelo)
N_VENT = 10           # ventanas de T/10 (a T = 1e7: ventanas de 1e6)


class _Tel:
    """Telemetria por ventanas, alimentada por ind_cb (cada individuo pasa UNA vez: al morir, o vivo en T con tm = -1).
    Ventana k (1..N_VENT) = pasos [W_{k-1}, W_k - 1], W_k = k*T/N_VENT. 'Vivo en el borde W' = el estado tras el paso W - 1 (el mismo
    instante que la fila de gen_t de t = W y que tam_total[W // muestra]): tn <= W - 1 y (tm == -1 o tm >= W).
    Guarda: genomas de los vivos en cada borde; nacimientos (fund == 0) por ventana de tn; muertes por causa y suma de vidas por ventana
    de tm (todo cuerpo, fundadores incluidos)."""

    def __init__(self, T):
        if T % N_VENT: raise SystemExit(f"LARGO: T = {T} no es multiplo de {N_VENT}")
        self.T = int(T); self.V = self.T // N_VENT
        self.W = [self.V * k for k in range(1, N_VENT + 1)]
        self.viv = [[] for _ in self.W]
        self.nac = [0] * N_VENT
        self.mue = [[0, 0, 0, 0] for _ in self.W]
        self.vida = [0] * N_VENT

    def cb(self, row, g):
        tn, tm, fund, cz = int(row[3]), int(row[4]), int(row[6]), int(row[7])
        if not fund and 0 <= tn < self.T: self.nac[tn // self.V] += 1
        if tm >= 0:
            k = min(tm // self.V, N_VENT - 1)
            if 0 <= cz < 4: self.mue[k][cz] += 1
            self.vida[k] += tm - tn
        for k, W in enumerate(self.W):
            if tn <= W - 1 and (tm == -1 or tm >= W): self.viv[k].append([float(x) for x in g])

    def estado(self):
        return dict(T=self.T, viv=self.viv, nac=self.nac, mue=self.mue, vida=self.vida)

    def carga(self, d):
        if d['T'] != self.T: raise SystemExit('LARGO: checkpoint de otro T')
        self.viv = d['viv']; self.nac = d['nac']; self.mue = d['mue']; self.vida = d['vida']


def _extra_largo(tel, E):
    """LARGO: la telemetria por ventana. Genes: SOLO los mutables del brazo (los demas son G0 por construccion; V3 lo comprueba), en valor
    crudo: media y cuantiles 10/50/90 (np.quantile, lineal) sobre los vivos en el borde; media_log = media de log(g/G0) de los 18 genes
    (la misma cantidad que la columna [4] de gen_t en t = W: el arnes la compara). Sin vivos: None."""
    G = list(E['genes']); mut = list(E['mutables']); G0 = np.array(E['G0'], float)
    genes = {g: dict(media=[], q10=[], q50=[], q90=[]) for g in mut}
    media_log = []
    for V in tel.viv:
        A = np.array(V, float) if V else None
        media_log.append([round(float(x), 5) for x in np.log(A / G0).mean(0)] if V else None)
        for g in mut:
            j = G.index(g)
            if V:
                q = np.quantile(A[:, j], [0.1, 0.5, 0.9])
                genes[g]['media'].append(round(float(A[:, j].mean()), 6))
                genes[g]['q10'].append(round(float(q[0]), 6)); genes[g]['q50'].append(round(float(q[1]), 6)); genes[g]['q90'].append(round(float(q[2]), 6))
            else:
                for c in ('media', 'q10', 'q50', 'q90'): genes[g][c].append(None)
    nm = [sum(m) for m in tel.mue]
    return dict(ventanas=dict(W=list(tel.W), vivos=[len(V) for V in tel.viv], nac=list(tel.nac), muertes=[list(m) for m in tel.mue],
                              vida_media=[(round(tel.vida[k] / nm[k], 1) if nm[k] else None) for k in range(N_VENT)],
                              genes=genes, media_log=media_log))
