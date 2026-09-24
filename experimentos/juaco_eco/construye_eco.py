"""construye_eco.py — CONSTRUYE POR ANCLAS el instrumento de JUACO-ECO (nivel 10). No se edita a mano lo construido.

MISION: llegar a la AGI por este camino.

Origenes (SOLO se LEEN; sha fijado):
  experimentos/generaciones/motor_convive.py     d10cb9021f5d0f41  -> juaco_eco/motor_eco.py
  experimentos/carrera_escuderias/carros/FABRICA.py 2ebee3e99ea5a33a -> juaco_eco/carros/FABRICA_ECO.py
  experimentos/carrera_escuderias/carros/APR.py     4402aa5142065c72 -> juaco_eco/carros/APR_ECO.py

motor_eco = motor_convive + el argumento eco (None -> motor_convive BIT A BIT, arnes (I)). Con eco:
  E1 mundo sin tope de 9: hasta ECO_NMAX linajes fundadores y mundo_n hasta ECO_ESC_MAX (L = 40*esc, nobj = 4*esc, esc sorteos
     de olvido, quimiostato r = 0.03*esc: el MISMO mundo de la pista v2, mas grande).
  E2 GENOMA por cuerpo (vector de perillas; lo expresa ctx: kw del carro, NK, dote, rep_umbral, rep_X). Memoria nueva en el
     organismo: CERO (el genoma vive en el registro del cuerpo en el mundo y entra por ctx como las constantes de fabrica).
  E3 MUTACION al nacer (rng propio [seed, linaje, 16, k]; no toca ningun rng del mundo ni del cuerpo).
  E4 GENOMAS SOMBRA (Bedau y Packard 1992): n_sombra copias que heredan y mutan IGUAL (rng [seed, linaje, 17, k]) pero no se
     expresan: la deriva con la MISMA genealogia. Control de 'mutacion sin seleccion' dentro de la misma corrida.
  E5 refunda=0: si un linaje se extingue NO se pone fundador (ERR-118); si todo muere, muere (la corrida para y lo marca).
  E6 historia de vida por cuerpo: el padre paga SU dote; la ventana usa SU rep_umbral y SU rep_X.
  E7 checkpoint reanudable (pickle de TODO el estado, rng incluidos) y registro de individuos por flujo.
  E8 memoria: el cuerpo muerto suelta la referencia a su padre (sin cadena de ancestros en memoria).
Carros *_ECO = el carro de origen con _see() reescrito como busqueda hacia afuera (misma salida, desempate por orden del dict):
  O(distancia) en vez de O(nobj). Arnes (F): == original en 200000 casos al azar y en corridas completas.
Uso: python experimentos/juaco_eco/construye_eco.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIG_MOTOR = os.path.join(RAIZ, 'experimentos', 'generaciones', 'motor_convive.py')
ORIG_CARROS = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros')
SHA = {'motor_convive.py': 'd10cb9021f5d0f41', 'FABRICA.py': '2ebee3e99ea5a33a', 'APR.py': '4402aa5142065c72'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def h16s(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


def aplica(txt, anclas, nombre):
    for i, (a, b) in enumerate(anclas):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"CONSTRUYE {nombre}: ancla {i} aparece {n} veces (debe ser 1): {a[:70]!r}")
        txt = txt.replace(a, b)
    return txt


# ============================================================================================ MOTOR
CABECERA = '''"""motor_eco.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco.py desde experimentos/generaciones/motor_convive.py,
sha d10cb9021f5d0f41; NO editar a mano). JUACO-ECO: con eco=None es motor_convive BIT A BIT; con eco=dict(...) agrega
E1-E8 (ver construye_eco.py). Lo que sigue es el docstring del origen.

motor_convive.py'''

ECO_MODULO = '''
# ============================================================================ JUACO-ECO (E1-E8; solo con eco=dict)
GEN = os.path.join(os.path.dirname(AQUI), 'generaciones')      # pista2 (mundo de la pista v2), solo se LEE
if GEN not in sys.path: sys.path.insert(1, GEN)
CARROS_ECO = os.path.join(AQUI, 'carros')
ECO_NMAX = 400        # linajes fundadores
ECO_ESC_MAX = 2000    # escala del mundo (L = 40*esc)
ETQ_MUT = 16; ETQ_SOMBRA = 17
# GENES: (nombre, destino, entero, piso_duro, techo_duro). Rango efectivo = [max(piso, G0/4), min(techo, 4*G0)].
# destino 'kw' = perilla del cerebro (ctx['fabrica']['kw']); 'NK' = celdas de Kenyon activas al nacer (estructura);
# 'dote'/'rep_umbral'/'rep_X' = historia de vida (la pista las aplica al cuerpo).
GENES = (('eta', 'kw', 0, 1e-4, 1.0), ('tau_e', 'kw', 0, 0.05, 0.99), ('alpha', 'kw', 0, 0.01, 20.0),
         ('hambre_boca', 'kw', 0, 0.01, 20.0), ('aversion', 'kw', 0, 0.01, 20.0), ('ema', 'kw', 0, 1e-3, 0.5),
         ('paso', 'kw', 0, 1e-3, 2.0), ('lam', 'kw', 0, 1e-3, 0.5), ('memoria_rechazo', 'kw', 1, 1, 200),
         ('eta_s', 'kw', 0, 1e-3, 2.0), ('clip_s', 'kw', 0, 0.5, 50.0), ('del_s', 'kw', 0, 0.01, 1.0),
         ('del_c', 'kw', 0, 0.01, 1.0), ('ema_c', 'kw', 0, 1e-3, 0.5), ('NK', 'NK', 1, 6, 90),
         ('dote', 'dote', 0, 0.15, 1.2), ('rep_umbral', 'rep_umbral', 0, 0.5, 1.45), ('rep_X', 'rep_X', 1, 100, 2000))
NOMBRES = tuple(g[0] for g in GENES)
I_DOTE = NOMBRES.index('dote'); I_RU = NOMBRES.index('rep_umbral'); I_RX = NOMBRES.index('rep_X')
ECO_DEF = dict(refunda=1, p_mut=0.0, sigma=0.15, genoma=None, n_sombra=0, cada_gen=0, ckpt_cada=0, ckpt_fn=None,
               estado=None, ind_cb=None, mutables=None, banco=0, donante='padre', t_corte=None)
ETQ_BANCO = 18; ETQ_DONANTE = 19
# VIVERO (E9, solo con refunda=1 y t < t_corte): si un linaje se extingue, el mundo pone un fundador cuyo genoma sale del
# BANCO (anillo de los ultimos `banco` genomas DONANTES de un parto), mutado; banco vacio -> genoma inicial del linaje.
# Desde t_corte: refunda = 0 (nadie pone nada; si todo muere, muere). donante='padre': el hijo copia el genoma del padre
# (seleccion natural; el banco guarda el genoma del PADRE en cada parto). donante='azar' (control 'mutacion sin seleccion'):
# el genoma de TODO cuerpo nuevo (hijo o fundador) sale de una entrada AL AZAR del banco, mutada, y el banco guarda el genoma
# NUEVO al crearse: el genoma nunca influye en su propia copia (ni por fertilidad ni por viabilidad). Candidato a ERR (humo
# exploratorio del 23-sep): la primera version del control copiaba el genoma de un cuerpo VIVO al azar, y eso es seleccion
# por viabilidad (el que vive mas dona mas): alpha subio +0.39 tambien en ese 'control'. El banco arranca con los fundadores.


def genoma0(CF):
    """G0 = los valores de fabrica (ctx), en el orden de GENES."""
    kw = CF['kw']; v = []
    for nom, dest, ent, lo, hi in GENES:
        v.append(float(CF['NK'] if dest == 'NK' else kw[nom]))
    return np.array(v, float)


def rangos(G0):
    lo = np.array([max(g[3], G0[j] / 4) for j, g in enumerate(GENES)]); hi = np.array([min(g[4], G0[j] * 4) for j, g in enumerate(GENES)])
    return lo, hi


def muta(g, r, p, sigma, lo, hi):
    """Mutacion log-normal por gen con probabilidad p[j] (0 en los genes no mutables). Consume SIEMPRE 2*NG numeros."""
    NG = len(g); u = r.random(NG); z = r.normal(0.0, sigma, NG); h = g.copy(); nm = 0
    for j in range(NG):
        if u[j] < p[j]:
            v = h[j] * math.exp(z[j])
            if GENES[j][2]:
                v = float(round(v))
                if v == h[j]: v = h[j] + (1.0 if z[j] > 0 else -1.0)
            v = min(max(v, lo[j]), hi[j])
            nm += int(v != h[j]); h[j] = v
    return h, nm


def carga_eco(ident):
    """carro por ruta: primero juaco_eco/carros, luego los de la carrera. Se REGISTRA en sys.modules (pickle del checkpoint)."""
    import importlib.util
    ruta = os.path.join(CARROS_ECO, f"{ident}.py")
    if not os.path.exists(ruta):
        import pista2 as P
        ruta = os.path.join(P.CARROS, f"{ident}.py")
    if not os.path.exists(ruta): raise SystemExit(f"ECO: no existe el carro {ident}")
    nom = f"carro_eco_{ident}"
    if nom in sys.modules: return sys.modules[nom]
    spec = importlib.util.spec_from_file_location(nom, ruta); mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod; spec.loader.exec_module(mod)
    if not hasattr(mod, 'crea'): raise SystemExit(f"ECO: el carro {ident} no define crea(ctx)")
    return mod


def _eco_cfg(eco, CF, n):
    mal = set(eco) - set(ECO_DEF)
    if mal: raise SystemExit(f"ECO: claves desconocidas en eco: {sorted(mal)}")
    E_ = dict(ECO_DEF); E_.update(eco)
    if E_['refunda'] not in (0, 1): raise SystemExit("ECO: refunda 0 o 1")
    if not 0.0 <= float(E_['p_mut']) <= 1.0: raise SystemExit("ECO: p_mut en [0, 1]")
    G0 = genoma0(CF); E_['G0'] = G0; E_['lo'], E_['hi'] = rangos(G0)
    mut = NOMBRES if E_['mutables'] is None else tuple(E_['mutables'])
    if set(mut) - set(NOMBRES): raise SystemExit(f"ECO: genes desconocidos {sorted(set(mut) - set(NOMBRES))}")
    E_['pv'] = np.array([float(E_['p_mut']) if nm_ in mut else 0.0 for nm_ in NOMBRES])
    if E_['donante'] not in ('padre', 'azar'): raise SystemExit("ECO: donante 'padre' o 'azar'")
    if not (isinstance(E_['banco'], int) and E_['banco'] >= 0): raise SystemExit("ECO: banco entero >= 0")
    if E_['t_corte'] is not None and not E_['refunda']: raise SystemExit("ECO: t_corte exige refunda=1 (vivero)")
    g = E_['genoma']
    if g is None: gs = [G0.copy() for _ in range(n)]
    else:
        a = np.asarray(g, float)
        if a.ndim == 1: a = np.tile(a, (n, 1))
        if a.shape != (n, len(GENES)): raise SystemExit(f"ECO: genoma con forma {a.shape}; se espera ({n}, {len(GENES)})")
        gs = [a[i].copy() for i in range(n)]
        for x in gs:
            if (x < E_['lo'] - 1e-12).any() or (x > E_['hi'] + 1e-12).any(): raise SystemExit("ECO: genoma fuera de rango")
    E_['gs0'] = gs
    return E_


def ctx_genoma(d, g):
    """Aplica el genoma g al ctx d (in situ). Con g == G0 el ctx queda IGUAL al de fabrica (arnes (E))."""
    kw = d['fabrica']['kw']
    for j, (nom, dest, ent, lo, hi) in enumerate(GENES):
        v = int(round(g[j])) if ent else float(g[j])
        if dest == 'kw': kw[nom] = v
        elif dest == 'NK': d['fabrica']['NK'] = v
        else: d[dest] = v; kw[dest] = v
    return d
'''

ANCLAS_MOTOR = [
    ('"""motor_convive.py', CABECERA),
    ("VOL_DECL = {'O3': 'cuerpos_term'", ECO_MODULO + "\n\nVOL_DECL = {'O3': 'cuerpos_term'"),
    ("'ult_mordida', 'vol_kk', 'hijos', 'fund', 'vivo', 'hvivos', 'pc')",
     "'ult_mordida', 'vol_kk', 'hijos', 'fund', 'vivo', 'hvivos', 'pc', 'g', 's')"),
    ("self.hijos = 0; self.fund = fund; self.vivo = True; self.hvivos = 0; self.pc = pc",
     "self.hijos = 0; self.fund = fund; self.vivo = True; self.hvivos = 0; self.pc = pc; self.g = None; self.s = None"),
    ("fundador_limpio=0, tope_cuerpos=TOPE_DEF, muestra=MUESTRA, reposicion='fija', r_rep=R_REP):",
     "fundador_limpio=0, tope_cuerpos=TOPE_DEF, muestra=MUESTRA, reposicion='fija', r_rep=R_REP, eco=None):"),
    ("    if not 1 <= n <= P.N_MAX: raise SystemExit",
     "    NMX = P.N_MAX if eco is None else ECO_NMAX\n    if not 1 <= n <= NMX: raise SystemExit"),
    ("    if mundo_n is not None and (int(mundo_n) != mundo_n or not 1 <= mundo_n <= P.N_MAX):",
     "    EMX = P.N_MAX if eco is None else ECO_ESC_MAX\n    if mundo_n is not None and (int(mundo_n) != mundo_n or not 1 <= mundo_n <= EMX):"),
    ("    mods = [(c, P.carga_carro(c)) if isinstance(c, str) else c for c in carros]",
     "    mods = [(c, (P.carga_carro(c) if eco is None else carga_eco(c))) if isinstance(c, str) else c for c in carros]\n"
     "    E_ = None if eco is None else _eco_cfg(eco, CF, n)\n"
     "    ES = dict(t_ext=None, gen_t=[], n_mut=0, n_mut_s=0, n_nac=0, banco=[], n_banco=0, n_refund=0, corte=None)\n"
     "    SE = lambda i, etq, k: np.random.default_rng([seed, i, etq, k])"),
    ("    def ctx_de(i, r, ident):\n        return dict(",
     "    def ctx_de(i, r, ident, g=None):\n        _d = dict("),
    ("rep_X=M['rep_X'], cupo=P.CUPO, ancho=P.ANCHO, fabrica=P.cfg_fabrica())",
     "rep_X=M['rep_X'], cupo=P.CUPO, ancho=P.ANCHO, fabrica=P.cfg_fabrica())\n"
     "        return _d if g is None else ctx_genoma(_d, g)"),
    ("        c = mod.crea(ctx_de(i, rngs_fund[i], ids[i]))\n        cuerpos.append(Cuerpo(i, 0, 0, -1, 0, c, ids[i], vista, 0, M['dote'], 1))",
     "        c = mod.crea(ctx_de(i, rngs_fund[i], ids[i], (None if E_ is None else E_['gs0'][i])))\n"
     "        cuerpos.append(Cuerpo(i, 0, 0, -1, 0, c, ids[i], vista, 0, M['dote'], 1))\n"
     "        if E_ is not None:\n"
     "            cuerpos[-1].g = E_['gs0'][i].copy(); cuerpos[-1].s = np.tile(E_['gs0'][i], (int(E_['n_sombra']), 1))"),
    ("        L_.ind.append([b.k, b.gen, b.padre, b.tn, tm, b.hijos, b.fund, causa, vd])",
     "        _row = [b.k, b.gen, b.padre, b.tn, tm, b.hijos, b.fund, causa, vd]\n"
     "        if E_ is not None and E_['ind_cb'] is not None: E_['ind_cb'](b.lin, _row, b.g)\n"
     "        else: L_.ind.append(_row)"),
    ("    for t in range(T):\n",
     "    _t0 = 0\n"
     "    if E_ is not None and E_['banco']: ES['banco'] = [(b.g.copy(), b.s.copy()) for b in cuerpos][-int(E_['banco']):]   # E9\n"
     "    def _muestra_gen(tt):   # E4: genoma real y sombras (log(g/G0)): media sobre los VIVOS [4],[5] y sobre el BANCO [6],[7]\n"
     "        G0 = E_['G0']; R5 = lambda v: [round(float(x), 5) for x in v]\n"
     "        if ES['banco']:\n"
     "            Br = R5(np.log(np.array([x[0] for x in ES['banco']]) / G0).mean(0))\n"
     "            Bs = ([R5(f) for f in np.log(np.array([x[1] for x in ES['banco']]) / G0).mean(0)] if int(E_['n_sombra']) else [])\n"
     "        else: Br = None; Bs = None\n"
     "        vv = [b for b in cuerpos if b.vivo]\n"
     "        if not vv: ES['gen_t'].append([tt, 0, 0, 0, None, None, Br, Bs]); return\n"
     "        Gr = np.log(np.array([b.g for b in vv]) / G0).mean(0)\n"
     "        Sr = (np.log(np.array([b.s for b in vv]) / G0).mean(0) if int(E_['n_sombra']) else np.zeros((0, len(G0))))\n"
     "        ES['gen_t'].append([tt, len(vv), len(set(b.lin for b in vv)), int(max(b.gen for b in vv)),\n"
     "                            R5(Gr), [R5(f) for f in Sr], Br, Bs])\n"
     "\n"
     "    def _estado(tn):   # E7: TODO el estado en un solo pickle (los rng compartidos siguen compartidos)\n"
     "        import pickle\n"
     "        for b in cuerpos: b.obs['objs'] = None\n"
     "        try:\n"
     "            st = dict(t=tn, objs=dict(objs), rng=rng, rng_pista=rng_pista, rngs_fund=rngs_fund, rngs_muerte=rngs_muerte,\n"
     "                      lin=lin, id2lin=id2lin, cuerpos=cuerpos, banco=banco, pisos=pisos, llegadas=llegadas, perdidas=perdidas,\n"
     "                      piz=piz, piz_t=piz_t, n_escr_desc=n_escr_desc, piz_log=piz_log, olv_n=olv_n, comp=comp,\n"
     "                      nobj_suma=nobj_suma, total=total, max_vivos=max_vivos, t_tope=t_tope, tam_total=tam_total, orden=orden, ES=ES,\n"
     "                      firma=(seed, T, n, ids, L, M['nobj'], reposicion, float(r_rep), tope_cuerpos, muestra))\n"
     "            return pickle.dumps(st, protocol=pickle.HIGHEST_PROTOCOL)\n"
     "        finally:\n"
     "            for b in cuerpos: b.obs['objs'] = vista\n"
     "\n"
     "    if E_ is not None and E_['estado'] is not None:   # E7: reanudar\n"
     "        import pickle\n"
     "        st = pickle.loads(E_['estado'])\n"
     "        if st['firma'] != (seed, T, n, ids, L, M['nobj'], reposicion, float(r_rep), tope_cuerpos, muestra):\n"
     "            raise SystemExit('ECO: el checkpoint es de otra corrida (firma distinta)')\n"
     "        objs.clear(); objs.update(st['objs'])\n"
     "        rng = st['rng']; rng_pista = st['rng_pista']; rngs_fund[:] = st['rngs_fund']; rngs_muerte[:] = st['rngs_muerte']\n"
     "        lin[:] = st['lin']; id2lin.clear(); id2lin.update(st['id2lin']); cuerpos = st['cuerpos']\n"
     "        banco[:] = st['banco']; pisos[:] = st['pisos']; llegadas[:] = st['llegadas']; perdidas[:] = st['perdidas']\n"
     "        piz = st['piz']; piz_t = st['piz_t']; n_escr_desc = st['n_escr_desc']; piz_log = st['piz_log']; olv_n = st['olv_n']\n"
     "        comp = st['comp']; nobj_suma = st['nobj_suma']; total = st['total']; max_vivos = st['max_vivos']; t_tope = st['t_tope']\n"
     "        tam_total = st['tam_total']; orden = st['orden']; ES.clear(); ES.update(st['ES'])\n"
     "        for b in cuerpos: b.obs['objs'] = vista\n"
     "        _t0 = st['t']; del st\n"
     "    for t in range(_t0, T):\n"),
    ("                if b.pc is not None: b.pc.hvivos -= 1\n",
     "                if b.pc is not None: b.pc.hvivos -= 1\n"
     "                if E_ is not None: b.pc = None   # E8\n"),
    ("                if l.vivos > 0: continue\n",
     "                if l.vivos > 0 or (E_ is not None and (not E_['refunda'] or (E_['t_corte'] is not None and t >= E_['t_corte']))): continue   # E5\n"),
    ("                cnew = mods[i][1].crea(ctx_de(i, rngs_fund[i], ids[i]))",
     "                _gf = _sf = None\n"
     "                if E_ is not None:   # E9 vivero: genoma del fundador = entrada del banco al azar, mutada (o el inicial)\n"
     "                    if ES['banco']:\n"
     "                        _gb, _sb = ES['banco'][int(SE(i, ETQ_BANCO, l.nac).integers(len(ES['banco'])))]\n"
     "                        _gf, _nm = muta(_gb, SE(i, ETQ_MUT, l.nac), E_['pv'], float(E_['sigma']), E_['lo'], E_['hi']); ES['n_mut'] += _nm\n"
     "                        _rs = SE(i, ETQ_SOMBRA, l.nac); _sf = _sb.copy()\n"
     "                        for _q in range(_sf.shape[0]): _sf[_q], _nm = muta(_sb[_q], _rs, E_['pv'], float(E_['sigma']), E_['lo'], E_['hi'])\n"
     "                        ES['n_banco'] += 1\n"
     "                    else: _gf = E_['gs0'][i].copy(); _sf = np.tile(E_['gs0'][i], (int(E_['n_sombra']), 1))\n"
     "                    ES['n_refund'] += 1\n"
     "                    if E_['donante'] == 'azar' and E_['banco']:   # control: el banco guarda el genoma NUEVO\n"
     "                        ES['banco'].append((_gf.copy(), _sf.copy()))\n"
     "                        if len(ES['banco']) > E_['banco']: ES['banco'].pop(0)\n"
     "                cnew = mods[i][1].crea(ctx_de(i, rngs_fund[i], ids[i], _gf))"),
    ("                cuerpos[j] = F; b = F; c = cnew; l.vivos = 1; total += 1; id2lin[F.id] = i\n",
     "                cuerpos[j] = F; b = F; c = cnew; l.vivos = 1; total += 1; id2lin[F.id] = i\n"
     "                if E_ is not None: F.g = _gf; F.s = _sf\n"),
    ("            if b.E >= M['rep_umbral'] and b.Ag >= M['rep_umbral']:",
     "            _ru = M['rep_umbral'] if b.g is None else b.g[I_RU]\n"
     "            if b.E >= _ru and b.Ag >= _ru:"),
    ("            if b.gv >= M['rep_X']:", "            if b.gv >= (M['rep_X'] if b.g is None else b.g[I_RX]):"),
    ("                    b.E -= M['dote']; b.Ag -= M['dote']",
     "                    _dt = M['dote'] if b.g is None else float(b.g[I_DOTE])\n"
     "                    b.E -= _dt; b.Ag -= _dt"),
    ("                    ch = mods[i][1].crea(ctx_de(i, SS(i, 'cuerpo', k), hid))",
     "                    _gh = _sh = None\n"
     "                    if E_ is not None:   # E3/E4: mutacion del hijo y de sus sombras (rng propios)\n"
     "                        _dg, _ds = b.g, b.s\n"
     "                        if E_['donante'] == 'azar' and ES['banco']:   # control sin seleccion: entrada del banco al azar\n"
     "                            _dg, _ds = ES['banco'][int(SE(i, ETQ_DONANTE, k).integers(len(ES['banco'])))]\n"
     "                        _gh, _nm = muta(_dg, SE(i, ETQ_MUT, k), E_['pv'], float(E_['sigma']), E_['lo'], E_['hi'])\n"
     "                        ES['n_mut'] += _nm; ES['n_nac'] += 1\n"
     "                        _rs = SE(i, ETQ_SOMBRA, k); _sh = _ds.copy()\n"
     "                        for _q in range(_sh.shape[0]):\n"
     "                            _sh[_q], _nm = muta(_ds[_q], _rs, E_['pv'], float(E_['sigma']), E_['lo'], E_['hi']); ES['n_mut_s'] += _nm\n"
     "                        if E_['banco']:   # 'padre': el genoma del PADRE (fertilidad); 'azar': el genoma NUEVO\n"
     "                            ES['banco'].append((_dg.copy(), _ds.copy()) if E_['donante'] == 'padre' else (_gh.copy(), _sh.copy()))\n"
     "                            if len(ES['banco']) > E_['banco']: ES['banco'].pop(0)\n"
     "                    ch = mods[i][1].crea(ctx_de(i, SS(i, 'cuerpo', k), hid, _gh))"),
    ("                    H = Cuerpo(i, k, b.gen + 1, b.k, t, ch, hid, vista, b.pos, M['dote'], 0, pc=b)",
     "                    H = Cuerpo(i, k, b.gen + 1, b.k, t, ch, hid, vista, b.pos, _dt, 0, pc=b); H.g = _gh; H.s = _sh"),
    ("            piz_t = tuple(piz)\n\n    for l in lin: l.tam.append(l.vivos)",
     "            piz_t = tuple(piz)\n"
     "        if E_ is not None:\n"
     "            if E_['cada_gen'] and (t + 1) % E_['cada_gen'] == 0: _muestra_gen(t + 1)\n"
     "            if E_['t_corte'] is not None and t + 1 == E_['t_corte']:   # E9: foto del genoma en el corte (lo que examina el juez)\n"
     "                _vv = [z for z in cuerpos if z.vivo]\n"
     "                ES['corte'] = dict(t=t + 1, vivos=len(_vv), n_banco=len(ES['banco']),\n"
     "                                   med_vivos=([float(x) for x in np.median(np.array([z.g for z in _vv]), 0)] if _vv else None),\n"
     "                                   med_banco=([float(x) for x in np.median(np.array([x[0] for x in ES['banco']]), 0)] if ES['banco'] else None),\n"
     "                                   med_sombra_banco=([float(x) for x in np.median(np.array([x[1][0] for x in ES['banco']]), 0)]\n"
     "                                                     if ES['banco'] and int(E_['n_sombra']) else None),\n"
     "                                   banco=[[round(float(x), 9) for x in e[0]] for e in ES['banco']])\n"
     "            if total == 0:   # E5: si todo muere, muere\n"
     "                ES['t_ext'] = t + 1; break\n"
     "            if E_['ckpt_cada'] and (t + 1) % E_['ckpt_cada'] == 0 and t + 1 < T: E_['ckpt_fn'](t + 1, _estado(t + 1))\n"
     "\n    for l in lin: l.tam.append(l.vivos)"),
    ("                           rng_mundo_estado=P._estado(rng)))",
     "                           rng_mundo_estado=P._estado(rng)),\n"
     "                **({} if E_ is None else dict(eco=dict(\n"
     "                    genes=list(NOMBRES), G0=[float(x) for x in E_['G0']], lo=[float(x) for x in E_['lo']], hi=[float(x) for x in E_['hi']],\n"
     "                    refunda=int(E_['refunda']), t_corte=E_['t_corte'], banco=int(E_['banco']), donante=E_['donante'], n_banco=ES['n_banco'],\n"
     "                    n_refund=ES['n_refund'], corte=ES['corte'], mutables=[x for x, q in zip(NOMBRES, E_['pv']) if q > 0], p_mut=float(E_['p_mut']), sigma=float(E_['sigma']), n_sombra=int(E_['n_sombra']),\n"
     "                    cada_gen=int(E_['cada_gen']), t_ext=ES['t_ext'], n_nac=ES['n_nac'], n_mut=ES['n_mut'], n_mut_s=ES['n_mut_s'],\n"
     "                    gen_t=ES['gen_t'], vivos_final=[[b.lin, b.k, b.gen, b.tn] + [round(float(x), 6) for x in b.g] for b in cuerpos if b.vivo]))))"),
]

# ============================================================================================ CARROS (_see rapido)
SEE_ORIG = '''    def _see(self, pos, objs, t, contar=False):
        L = self.L; best = None
        for x, k in objs.items():
            if self.MEMORIA_RECHAZO and self._rech.get(x, -1) > t: continue
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
            if best is None or d < best[0]: best = (d, k, dl < dr)
        if best is None:
            if contar: self.sin_objetivo[self._q(t)] += 1
            for x, k in objs.items():
                dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
                if best is None or d < best[0]: best = (d, k, dl < dr)
        return best
'''
SEE_ECO = '''    def _see(self, pos, objs, t, contar=False):
        # JUACO-ECO (construye_eco.py): busqueda HACIA AFUERA desde pos, O(distancia). MISMA salida que el barrido del
        # monolito: el mas cercano no rechazado; empate a igual distancia -> el primero en el orden del dict; si todos
        # estan rechazados, el mas cercano de todos (y cuenta sin_objetivo). Arnes (F) de identidad_eco.py.
        L = self.L; rech = self._rech if self.MEMORIA_RECHAZO else None; fb = None
        for d in range(L // 2 + 1):
            xl = (pos - d) % L; xr = (pos + d) % L
            kl = objs.get(xl); kr = objs.get(xr) if xr != xl else None
            if kl is None and kr is None: continue
            el = kl is not None and (rech is None or rech.get(xl, -1) <= t)
            er = kr is not None and (rech is None or rech.get(xr, -1) <= t)
            if el or er:
                return _elige(pos, L, d, xl if el else None, kl, xr if er else None, kr, objs)
            if fb is None: fb = _elige(pos, L, d, xl if kl is not None else None, kl, xr if kr is not None else None, kr, objs)
        if contar: self.sin_objetivo[self._q(t)] += 1
        return fb
'''
ELIGE = '''

def _elige(pos, L, d, xl, kl, xr, kr, objs):
    """JUACO-ECO: entre los candidatos a distancia d, el primero en el orden del dict (el barrido del monolito usa '<')."""
    if xl is not None and xr is not None:
        for x in objs:
            if x == xl or x == xr: break
    else: x = xl if xl is not None else xr
    k = kl if x == xl else kr
    return (d, k, (pos - x) % L < (x - pos) % L)


def crea(ctx):'''


def carro_eco(nombre):
    ruta = os.path.join(ORIG_CARROS, nombre)
    txt = open(ruta, encoding='utf-8').read()
    cab = (f'"""carros/{nombre[:-3]}_ECO.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco.py desde '
           f'carrera_escuderias/carros/{nombre}, sha {SHA[nombre]}; NO editar a mano). Unico cambio: _see() hacia afuera\n'
           f'(O(distancia), misma salida; arnes (F)) y la funcion _elige. Lo que sigue es el docstring del origen.\n\n')
    return aplica(txt, [(f'"""carros/{nombre}', cab + f'carros/{nombre}'), (SEE_ORIG, SEE_ECO), ('\n\ndef crea(ctx):', ELIGE)], nombre)


def construye():
    for nom, p in (('motor_convive.py', ORIG_MOTOR), ('FABRICA.py', os.path.join(ORIG_CARROS, 'FABRICA.py')),
                   ('APR.py', os.path.join(ORIG_CARROS, 'APR.py'))):
        if h16(p) != SHA[nom]: raise SystemExit(f"CONSTRUYE: {nom} cambio (sha {h16(p)} != {SHA[nom]})")
    motor = aplica(open(ORIG_MOTOR, encoding='utf-8').read(), ANCLAS_MOTOR, 'motor')
    return {os.path.join(AQUI, 'motor_eco.py'): motor,
            os.path.join(AQUI, 'carros', 'FABRICA_ECO.py'): carro_eco('FABRICA.py'),
            os.path.join(AQUI, 'carros', 'APR_ECO.py'): carro_eco('APR.py')}


if __name__ == '__main__':
    arts = construye()
    if '--verifica' in sys.argv[1:]:
        ok = all(os.path.exists(p) and open(p, encoding='utf-8').read() == s for p, s in arts.items())
        print('VERIFICA', 'OK' if ok else 'FALLA'); sys.exit(0 if ok else 1)
    if set(sys.argv[1:]) - {'--verifica'}: raise SystemExit(f"CONSTRUYE: banderas desconocidas {sys.argv[1:]}")
    for p, s in arts.items():
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='\n') as f: f.write(s)
        print(os.path.relpath(p, RAIZ), h16s(s))
