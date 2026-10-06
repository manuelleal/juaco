"""corre_mm.py — CONDICIONES / LA MONEDA DEL MURO (30-sep-2026, creador; EXPLORATORIO). Preregistro: PREREGISTRO_moneda_muro.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

PREGUNTA (director, 30-sep noche): en condiciones/mutacion (tasas / 10) la seleccion por pasajes PURGA la regla de riesgo de forzada3
(0.26 vs 0.64 la neutra) aunque la cadena sembrada con ella cruza 24/45 a 100k. La transferencia vieja (bancos finales de los 9 linajes
de un pasaje de 25k) premia sobrevivir al muestreo; la letra (cruza_real) pide establecerse: R0 real >= 0.9 y 0 fundadores tras 10k en
100k. Si la transferencia paga el ESTABLECIMIENTO (0 fundadores tras 10k: la MITAD de la letra; no paga R0 real >= 0.9), la seleccion
deberia CONSERVAR o SUBIR la regla.

UNICO CAMBIO (opcion (a) del encargo): pasajes de T 100 000 y la siembra del pasaje siguiente = union de los bancos finales SOLO de los
linajes ESTABLECIDOS (0 fundadores tras t = 10 000, contado con los instantes de fundacion del propio linaje: telem.t_fund y fundadores;
no se lee R0, ni cruza_real, ni ningun veredicto del juez). Si ningun linaje se establecio: los de menos fundadores tras 10k (respaldo,
se cuenta y entra en la validez). El carro, el banco, las tasas / 10 y la siembra inicial (225 x [A] + 225 x [B]) son los de mutacion.
La opcion (b) (ponderar por partos) NO se usa: el banco del carro YA es eso (cada parto mete la lista del padre; FIFO de 50).

ENTRADA (regla 14): TODA corrida ES condiciones/mutacion/corre_mut._corrida -> corre_mut.tarea(seed, 'moneda' | 'neutra', T, siembra,
'div10') = bloques_pista/corre_bp.tarea(seed, 'V143_BQ3', T, cfg=CFG10, forzada=None, siembra). corre_mut se IMPORTA y no se toca (sha
fijado). Con MONEDA 'vieja' y T_pas 25 000 (SOLO arnes) este runner ES corre_mut bit a bit (arnes F).

BRAZOS: moneda_L (A = fila de forzada3 + B; moneda nueva; CANDIDATO) · neutra_L (A0 = la misma fila con w 0 + B; moneda nueva; CONTROL
que puede fallar: deriva y arrastre del pasaje nuevo) · moneda_25 y neutra_25 = GUARDADOS de condiciones/mutacion (sha16; no se recorren).
SEMILLAS NUEVAS (grep 30-sep 22:35: 638xxx no aparece en .py/.md de PROYECTOS/JUACO; en .txt solo como cifras de floats de logs):
  pasaje p del indice i (1..5): 638100 + 10 i + p (638110-638155), LAS MISMAS en los dos brazos (pareado)
  prueba (los dos brazos, descriptiva): 59201-59205 a T 100 000 = las de moneda / mutacion / forzada3 / bq3_pas GUARDADOS (pareada, a proposito)
  humo: pasajes 638180-638181, prueba 638191 · arnes 638193.
Pool: MAXIMO 2. Cada trabajo registra los carros y fija cfg al entrar (cfg explicito por worker), atrapa TODO y escribe cada JSON ANTES
de volver (ERR-54). --reanuda sigue la ultima carpeta y REINTENTA los JSON con aborto (los buenos no se recorren). ERR-115: banderas exactas.

  python experimentos/organelos/condiciones/moneda_muro/identidad_mm.py                  # arnes (escribe identidad_mm_salida.txt)
  python experimentos/organelos/condiciones/moneda_muro/corre_mm.py --humo               # 1 proceso, 6 corridas, 160 000 pasos
  python experimentos/organelos/condiciones/moneda_muro/corre_mm.py --explora --pool 2   # 10 cadenas (6 x 100k) + 10 pruebas 100k
  python experimentos/organelos/condiciones/moneda_muro/corre_mm.py --explora --pool 2 --reanuda
  python experimentos/organelos/condiciones/moneda_muro/corre_mm.py --lee datos/explora_<fecha>
"""
import argparse, hashlib, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
MUTD = os.path.join(RAIZ, 'experimentos', 'organelos', 'condiciones', 'mutacion')
for _d in (AQUI, MUTD):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_mut as MU   # tarea, _corrida, siembra0, intacta, CFG10, verifica (se IMPORTA, no se toca; sha fijado)
M = MU.M; SM = MU.SM; CBP = MU.CBP

PRERREGISTRO = 'PREREGISTRO_moneda_muro.md'
DATOS = os.path.join(AQUI, 'datos')
MUEXP = os.path.join(MUTD, 'datos', 'explora_20260930_191833')
SHAS = {os.path.join(MUTD, 'corre_mut.py'): '8912e9d77f397e40', os.path.join(MUTD, 'identidad_mut.py'): 'b08e1410de201065'}
# GUARDADOS de condiciones/mutacion (commit ff09fac3): la lectura (finales p9 de moneda_25 y neutra_25, sumas de cruzan), las 5 pruebas
# de moneda / 10 a 100k y los dos primeros pasajes de la cadena moneda i1 (arnes F: reproduccion bit a bit con la moneda vieja).
REF_LECT = (os.path.join(MUEXP, 'lectura_mut.json'), 'af53bdfadf5c9668')
REF_PRU = ['41cd6e8a48b54799', 'fb4b30bbc4e10cd3', '982b5ab3bc1b88b9', 'e00d62919783ce34', '91b43d82d4c9137f']   # moneda_s59201..05
REF_PAS = [(os.path.join(MUEXP, 'pasaje_moneda_i1_p0.json'), 'c478fc760bcc584a'),
           (os.path.join(MUEXP, 'pasaje_moneda_i1_p1.json'), 'dc9effc75ab57059')]

CFG10 = dict(MU.CFG10)
T_EST = 10000   # = juez.T_CORTE (arnes J): "establecido" = 0 fundadores despues de este instante
# brazo -> (brazo de corre_mut (fila marcada y cfg), moneda de la siembra)
BRAZOS = {'moneda_L': ('moneda', 'L'), 'neutra_L': ('neutra', 'L'),
          'moneda_25': ('moneda', 'vieja'), 'neutra_25': ('neutra', 'vieja')}   # *_25: SOLO arnes (los datos son los GUARDADOS)
MODOS = {'explora': dict(ind=[1, 2, 3, 4, 5], npas=6, T_pas=100000, T_pru=100000, base_pas=638100, base_pru=59200,
                         brazos=('moneda_L', 'neutra_L')),
         'humo': dict(ind=[8], npas=2, T_pas=30000, T_pru=20000, base_pas=638100, base_pru=638183, brazos=('moneda_L', 'neutra_L'))}
SEM_ARNES = 638193
POOL_MAX = 2
# LA LETRA (PREREGISTRO sec. 6 y 12). ERR-176 (auditoria, antes de datos): CONSERVA exige 5/5 (con 4/5 el falso positivo nulo era ~0.28; con 5/5 ~0.07)
CONSERVA_N = 5; CONSERVA_MED = 0.40; PURGA_N = 4; MITAD = 0.5; RESPALDO_MAX = 0.25; FIJA = 0.95; PIERDE = 0.05


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sem_pas(m, i, p): return m['base_pas'] + 10 * i + p
def sem_pru(m, i): return m['base_pru'] + i


def post10k(x):
    """Por linaje (indice): fundadores DESPUES de T_EST, con los instantes de fundacion del PROPIO linaje (fisica de la pista:
    fundadores y telem.t_fund). No se lee fund_post10k ni ningun veredicto del juez (el arnes J comprueba que coinciden)."""
    return {int(l['indice']): int(l['fundadores']) - sum(1 for t in l['telem']['t_fund'] if t <= T_EST) for l in x['linajes']}


def elige(x):
    """Linajes que dan siembra con la moneda nueva: los ESTABLECIDOS (0 fundadores tras T_EST) con banco no vacio. Respaldo si no hay
    ninguno: los de MENOS fundadores tras T_EST con banco no vacio. Devuelve (indices, respaldo)."""
    post = post10k(x); ban = x['bq']['banco']
    con = [i for i in sorted(post) if any(R for R in (ban.get(str(i)) or []))]
    est = [i for i in con if post[i] == 0]
    if est: return est, False
    if not con: return [], True
    mn = min(post[i] for i in con)
    return [i for i in con if post[i] == mn], True


def siembra_L(x):
    """MONEDA NUEVA: union de los bancos finales de los linajes elegidos (elige), en orden de indice."""
    idx, _ = elige(x); ban = x['bq']['banco']
    return [R for i in idx for R in ban[str(i)] if R]


def siembra(x, moneda):
    return siembra_L(x) if moneda == 'L' else CBP.siembra_de(x)


def tarea(seed, brazo, T, sb):
    """UNA corrida: corre_mut.tarea(seed, 'moneda' | 'neutra', T, siembra, 'div10') (la entrada de mutacion; cfg CFG10 explicito)."""
    return MU.tarea(seed, BRAZOS[brazo][0], T, sb, 'div10')


def _corrida(fin, seed, brazo, T, sb, extra):
    bm, mon = BRAZOS[brazo]
    return MU._corrida(fin, seed, bm, T, sb, dict(extra, brazo_mm=brazo, moneda_siembra=mon), 'div10')


def trabajo(args):
    """UN trabajo = una cadena (brazo, indice): NPAS pasajes + la prueba. cfg fijado en CADA worker (registra + cfg explicito)."""
    brazo, i, carpeta, modo = args
    m = MODOS[modo]; bm, mon = BRAZOS[brazo]; t0 = time.time(); fr = []; aborto = None; out = dict(brazo=brazo, i=i)
    try:
        SM.registra()
        sb = MU.siembra0(bm); fr.append(M.frac(sb))
        for p in range(m['npas']):
            x = _corrida(os.path.join(carpeta, f"pasaje_{brazo}_i{i}_p{p}.json"), sem_pas(m, i, p), brazo, m['T_pas'], sb,
                         dict(i=i, p=p, tipo='pasaje'))
            if x.get('aborto'): aborto = f"pasaje {p}: {x['aborto']}"; break
            sb = siembra(x, mon); fr.append(M.frac(sb))
            if not sb: aborto = f"pasaje {p}: siembra vacia"; break
        if aborto is None and not m.get('sin_prueba'):
            x = _corrida(os.path.join(carpeta, f"{brazo}_s{sem_pru(m, i)}.json"), sem_pru(m, i), brazo, m['T_pru'], sb,
                         dict(i=i, tipo='prueba', siembra_final=sb))
            aborto = x.get('aborto'); L = x.get('linajes', [])
            out.update(cruzan=sum(int(l['cruza_real']) for l in L), R0=[l['R0_real'] for l in L])
        out.update(aborto=aborto, frac_A=fr)
    except BaseException as e:   # noqa: nube-9
        out.update(aborto=f"{type(e).__name__}: {e}"[:300], frac_A=fr)
    out['seg'] = round(time.time() - t0, 1)
    return out


# ------------------------------------------------------------------ lectura y LA LETRA
def _med(xs):
    xs = [x for x in xs if x is not None]; return round(float(st.median(xs)), 4) if xs else None


def cadena(carpeta, m, brazo, i):
    """Lee una cadena de sus JSON. Por pasaje: fraccion A de la siembra que sale (la moneda del brazo), la SOMBRA con la moneda vieja
    sobre el mismo pasaje, linajes elegidos, respaldo, listas, intacta, arrastre (cota), partos, cruzan del pasaje (descriptivo)."""
    bm, mon = BRAZOS[brazo]; sb = MU.siembra0(bm); f_ini = M.frac(sb)
    c = dict(f_ini=f_ini, f=[], f_sombra_vieja=[], n_ele=[], respaldo=[], n_listas=[], intacta=[], arrastre=[], partos=[], cruzan_pas=[],
             est_fracA=[], est_n=[], mutadas=0)
    g = {json.dumps(L) for L in sb}
    for p in range(m['npas']):
        fin = os.path.join(carpeta, f"pasaje_{brazo}_i{i}_p{p}.json")
        if not os.path.exists(fin): return None, f"falta {os.path.basename(fin)}"
        x = json.load(open(fin, encoding='utf-8'))
        if x.get('aborto'): return None, f"{brazo} i{i} p{p}: {x['aborto']}"
        nb = min(int(x['bq']['cfg']['banco']), len(sb))
        idx, resp = elige(x) if mon == 'L' else (sorted(post10k(x)), False)
        sb = siembra(x, mon)
        if not sb: return None, f"{brazo} i{i} p{p}: siembra vacia"
        post = post10k(x); tel = x['bq']['tel']
        c['f'].append(M.frac(sb)); c['f_sombra_vieja'].append(M.frac(CBP.siembra_de(x))); c['n_ele'].append(len(idx)); c['respaldo'].append(bool(resp))
        c['est_n'].append(sum(1 for v in post.values() if v == 0))
        c['n_listas'].append(len(sb)); c['intacta'].append(MU.intacta(sb, bm)); c['mutadas'] += sum(1 for R in sb if json.dumps(R) not in g)
        pp = {k: int(tel[str(k)]['partos']) for k in idx if str(k) in tel}; c['partos'].append(sum(int(t['partos']) for t in tel.values()))
        c['arrastre'].append(round(sum(max(0, nb - q) for q in pp.values()) / max(1, len(sb)), 3))
        c['cruzan_pas'].append(sum(int(l['cruza_real']) for l in x['linajes']))
        c['est_fracA'].append([M.frac([R for R in x['bq']['banco'][str(k)] if R]) for k in idx])   # por linaje elegido: casi siempre 0 o 1 (clon)
    c['siembra_final'] = sb
    return c, None


def refs_mutacion():
    """GUARDADOS de condiciones/mutacion: finales p9 de moneda_25 / neutra_25, pruebas a 100k (moneda_25) y sumas de referencia."""
    ok = True; txt = []; out = dict(final={}, prueba={}, sumas={})
    s = h16(REF_LECT[0]) if os.path.exists(REF_LECT[0]) else None
    if s != REF_LECT[1]: return False, [f"lectura_mut sha {s} != {REF_LECT[1]}"], out
    L = json.load(open(REF_LECT[0], encoding='utf-8'))
    out['final'] = {'moneda_25': L['letra']['final']['moneda'], 'neutra_25': L['letra']['final']['neutra']}
    out['sumas'] = dict(L['sumas']); out['veredicto_mutacion'] = L['letra']['veredicto']
    for i, sh in zip([1, 2, 3, 4, 5], REF_PRU):
        f = os.path.join(MUEXP, f"moneda_s{59200 + i}.json"); s = h16(f) if os.path.exists(f) else None
        if s != sh: ok = False; txt.append(f"moneda_25 s{59200 + i} sha {s} != {sh}"); continue
        out['prueba'][i] = L['prueba'][str(i)]
    return ok, txt, out


def carga(carpeta, modo):
    m = MODOS[modo]; C = {}; abortos = []; P_ = {b: {} for b in m['brazos']}
    for b in m['brazos']:
        C[b] = {}
        for i in m['ind']:
            c, ab = cadena(carpeta, m, b, i)
            if c is None: abortos.append(ab); continue
            C[b][i] = c
            fin = os.path.join(carpeta, f"{b}_s{sem_pru(m, i)}.json")
            if not os.path.exists(fin): abortos.append(f"falta prueba {b} i{i}"); continue
            x = json.load(open(fin, encoding='utf-8'))
            if x.get('aborto'): abortos.append(f"prueba {b} i{i}: {x['aborto']}"); continue
            P_[b][i] = M.fila_prueba(x)
    ref_ok, ref_txt, refs = refs_mutacion() if modo == 'explora' else (True, [], dict(final={}, prueba={}, sumas={}))
    return C, P_, refs, abortos, ref_ok, ref_txt


def letra(C, ind, abortos, ref_ok, arnes_ok, n_pru=None):
    """PREREGISTRO sec. 6. C[brazo][i] = cadena. Veredicto: CONSERVA / PURGA / INDETERMINADO / NO SE LEE."""
    n = len(ind); mo = 'moneda_L'; ne = 'neutra_L'
    fin = {b: {i: C[b][i]['f'][-1] for i in C.get(b, {})} for b in C}
    pas = [c for b in (mo, ne) for c in C.get(b, {}).values()]
    n_pas = sum(len(c['f']) for c in pas); n_resp = sum(sum(c['respaldo']) for c in pas)
    actua = sum(1 for c in pas for a, b in zip(c['f'], c['f_sombra_vieja']) if a != b)
    val = dict(abortos_0=(len(abortos) == 0),
               completas=all(len(C.get(b, {})) == n for b in (mo, ne)) and (n_pru is None or n_pru == 2 * n),
               f_ini_05=all(c['f_ini'] == 0.5 for c in pas),
               moneda_actua=(actua > 0),
               respaldo_raro=(n_pas > 0 and n_resp / n_pas <= RESPALDO_MAX),
               refs_sha=bool(ref_ok), arnes=bool(arnes_ok))
    valido = all(val.values())
    I = [i for i in ind if i in fin.get(mo, {}) and i in fin.get(ne, {})]
    ge = sum(1 for i in I if fin[mo][i] >= fin[ne][i])
    mayor = sum(1 for i in I if fin[mo][i] > fin[ne][i])   # descriptivo (estricto)
    mitad = sum(1 for i in I if fin[ne][i] > 0 and fin[mo][i] <= MITAD * fin[ne][i])   # 0 <= 0.5 x 0 NO cuenta (sec. 6)
    mo_med = _med(list(fin.get(mo, {}).values())); ne_med = _med(list(fin.get(ne, {}).values()))
    if not valido: ver = 'NO SE LEE'
    elif ge >= CONSERVA_N and mo_med is not None and mo_med >= CONSERVA_MED: ver = 'CONSERVA'
    elif mitad >= PURGA_N: ver = 'PURGA'
    else: ver = 'INDETERMINADO'
    def cuenta(b, f): return sum(1 for v in fin.get(b, {}).values() if f(v))
    def delta(b):   # descriptivo: cambio medio de la fraccion A por pasaje (sale - entra), sobre los pasajes que entran con 0 < f < 1
        d = [y - x for c in C.get(b, {}).values() for x, y in zip([c['f_ini']] + c['f'][:-1], c['f']) if 0 < x < 1]
        return round(st.mean(d), 4) if d else None
    return dict(validez=val, veredicto=ver, moneda_ge_neutra=f"{ge}/{len(I)}", moneda_mayor_estricto=f"{mayor}/{len(I)}",
                moneda_le_mitad_neutra=f"{mitad}/{len(I)}", moneda_L_mediana=mo_med, neutra_L_mediana=ne_med,
                moneda_L_media=(round(st.mean(fin[mo].values()), 4) if fin.get(mo) else None),
                neutra_L_media=(round(st.mean(fin[ne].values()), 4) if fin.get(ne) else None),
                moneda_L_fijadas=cuenta(mo, lambda v: v >= FIJA), neutra_L_fijadas=cuenta(ne, lambda v: v >= FIJA),
                moneda_L_perdidas=cuenta(mo, lambda v: v <= PIERDE), neutra_L_perdidas=cuenta(ne, lambda v: v <= PIERDE),
                moneda_L_delta_pasaje=delta(mo), neutra_L_delta_pasaje=delta(ne),
                pasajes=n_pas, pasajes_con_respaldo=n_resp, pasajes_donde_la_moneda_difiere=actua,
                elegidos_por_pasaje_mediana=_med([v for c in pas for v in c['n_ele']]),
                final={b: {str(i): v for i, v in d.items()} for b, d in fin.items()})


def predicciones(C, P_, L):
    mo = 'moneda_L'; ne = 'neutra_L'
    cz = {b: (sum(f['cruzan'] for f in P_[b].values()) if P_.get(b) else None) for b in (mo, ne)}
    def p0(b): return _med([c['f'][0] for c in C.get(b, {}).values()])
    czp = {b: [v for c in C.get(b, {}).values() for v in c['cruzan_pas']] for b in (mo, ne)}
    mp = {b: (round(st.mean(v), 3) if v else None) for b, v in czp.items()}
    ext = sum(1 for b in (mo, ne) for c in C.get(b, {}).values() if c['f'][-1] <= PIERDE or c['f'][-1] >= FIJA)
    nx = sum(len(C.get(b, {})) for b in (mo, ne))
    return [('Q1', 'veredicto CONSERVA (la hipotesis del encargo)', L['veredicto'], L['veredicto'] == 'CONSERVA', 0.10),
            ('Q2', 'veredicto INDETERMINADO', L['veredicto'], L['veredicto'] == 'INDETERMINADO', 0.65),
            ('Q3', 'veredicto PURGA', L['veredicto'], L['veredicto'] == 'PURGA', 0.22),
            ('Q4', 'moneda_L: mediana de la fraccion A final <= 0.20', L['moneda_L_mediana'],
             L['moneda_L_mediana'] is not None and L['moneda_L_mediana'] <= 0.20, 0.55),
            ('Q5', 'deriva: >= 6 de las 10 cadenas terminan fijadas (>= 0.95) o perdidas (<= 0.05)', f"{ext}/{nx}", ext >= 6, 0.55),
            ('Q6', 'elegidos por pasaje (mediana, los dos brazos) en [5, 7]', L['elegidos_por_pasaje_mediana'],
             L['elegidos_por_pasaje_mediana'] is not None and 5 <= L['elegidos_por_pasaje_mediana'] <= 7, 0.75),
            ('Q7', 'prueba moneda_L: suma de cruzan (de 45) en [15, 27]', cz[mo], cz[mo] is not None and 15 <= cz[mo] <= 27, 0.60),
            ('Q8', 'prueba: moneda_L cruza MAS que moneda_25 guardada (24/45), es decir >= 25', cz[mo], cz[mo] is not None and cz[mo] >= 25, 0.30),
            ('Q9', 'cruzan por pasaje (media de linajes de 9): moneda_L > neutra_L', mp, mp[mo] is not None and mp[ne] is not None and mp[mo] > mp[ne], 0.50),
            ('Q10', 'delta medio de la fraccion A por pasaje: moneda_L < neutra_L', [L['moneda_L_delta_pasaje'], L['neutra_L_delta_pasaje']],
             L['moneda_L_delta_pasaje'] is not None and L['neutra_L_delta_pasaje'] is not None and L['moneda_L_delta_pasaje'] < L['neutra_L_delta_pasaje'], 0.70)]


def arnes_pasado():
    f = os.path.join(AQUI, 'identidad_mm_salida.txt')
    if not os.path.exists(f): return False, 'sin salida del arnes'
    t = open(f, encoding='utf-8').read()
    need = [h16(os.path.abspath(__file__)), h16(os.path.join(AQUI, 'identidad_mm.py'))]
    ok = 'ARNES: PASA' in t and all(s in t for s in need)
    return ok, ('PASA con los shas actuales' if ok else f'no PASA o no cita los shas actuales {need}')


def lee(carpeta, log=print, modo=None):
    modo = modo or ('humo' if os.path.basename(carpeta).startswith('humo') else 'explora')
    m = MODOS[modo]; C, P_, refs, abortos, ref_ok, ref_txt = carga(carpeta, modo)
    aok, atxt = arnes_pasado()
    L = letra(C, m['ind'], abortos, ref_ok, aok, n_pru=sum(len(v) for v in P_.values()))
    log(f"\n================ LECTURA moneda del muro · {modo} · {carpeta}")
    log(f"  arnes: {atxt} · refs: {'sha OK' if ref_ok else ref_txt} · abortos: {abortos}")
    for b in m['brazos']:
        for i in sorted(C.get(b, {})):
            c = C[b][i]
            log(f"  {b:8s} i{i}: fraccion A  ini {c['f_ini']} -> p0..p{len(c['f'])-1} {c['f']}")
            log(f"  {'':8s}     sombra (moneda vieja sobre el mismo pasaje) {c['f_sombra_vieja']} · elegidos {c['n_ele']} · establecidos {c['est_n']} · respaldo {[int(r) for r in c['respaldo']]}")
            log(f"  {'':8s}     fraccion A por linaje elegido {c['est_fracA']}")
            log(f"  {'':8s}     listas {c['n_listas']} · intacta {c['intacta']} · mutadas (suma) {c['mutadas']} · arrastre>= {c['arrastre']} · partos {c['partos']} · cruzan en el pasaje {c['cruzan_pas']}")
    sumas = {}
    for b in m['brazos']:
        for i in sorted(P_[b]):
            f = P_[b][i]; g = refs['prueba'].get(i)
            log(f"  prueba {b} i{i} s{f['seed']}: cruzan {f['cruzan']}/9 · mayoria {f['mayoria']} · R0 med {f['R0_med']} · fund med {f['fund_med']} "
                f"· descendientes {f['desc']}" + (f" || moneda_25 guardada: {g['cruzan']}/9" if g else ''))
        sumas[b] = sum(f['cruzan'] for f in P_[b].values())
    sumas.update({('moneda_25' if k == 'moneda_div10' else k): v for k, v in refs['sumas'].items()})
    log(f"  suma cruzan (de {9 * len(m['ind'])}): {sumas}")
    if refs['final']: log(f"  GUARDADO mutacion (moneda vieja, 10 x 25k), fraccion A en p9: {refs['final']} · veredicto alli: {refs.get('veredicto_mutacion')}")
    for k in ('validez', 'final', 'moneda_ge_neutra', 'moneda_mayor_estricto', 'moneda_le_mitad_neutra', 'moneda_L_mediana', 'neutra_L_mediana',
              'moneda_L_media', 'neutra_L_media', 'moneda_L_fijadas', 'neutra_L_fijadas', 'moneda_L_perdidas', 'neutra_L_perdidas', 'moneda_L_delta_pasaje', 'neutra_L_delta_pasaje', 'pasajes',
              'pasajes_con_respaldo', 'pasajes_donde_la_moneda_difiere', 'elegidos_por_pasaje_mediana'):
        log(f"  {k}: {L[k]}")
    pq = predicciones(C, P_, L) if modo == 'explora' else []
    for q in pq: log(f"  {q[0]} {q[1]} (p {q[4]}): medido {q[2]} -> {'CUMPLE' if q[3] else 'REFUTADA'}")
    ver = ('HUMO (no cuenta; 2 pasajes de 30k, sin referencias): ' if modo == 'humo' else '') + L['veredicto']
    out = os.path.join(carpeta, 'lectura_mm.json')
    json.dump(dict(modo=modo, letra=L, cadenas={b: {str(i): {k: v for k, v in c.items() if k != 'siembra_final'} for i, c in d.items()}
                                                 for b, d in C.items()},
                   prueba={b: {str(i): f for i, f in d.items()} for b, d in P_.items()},
                   refs=dict(final=refs['final'], prueba={str(i): f for i, f in refs['prueba'].items()}, sumas=refs['sumas']),
                   sumas=sumas, abortos=abortos, predicciones=[[q[0], q[1], q[2], bool(q[3]), q[4]] for q in pq],
                   preregistro=PRERREGISTRO, sha_runner=h16(os.path.abspath(__file__))),
              open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    log(f"  LECTURA {out}")
    log(f"VEREDICTO ({PRERREGISTRO} sec. 6): {ver}")
    return L


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    log("  -- verifica de corre_mut (corre_moneda, sentidos_muro, corre_bp, V143_BQ3, pista, juez, carros):")
    ok &= MU.verifica(lambda s: log('  ' + s))
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115
    if a.pool > POOL_MAX: raise SystemExit(f"--pool: maximo {POOL_MAX}")
    if a.humo and a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
    if a.lee:
        c = a.lee if os.path.isabs(a.lee) else os.path.join(AQUI, a.lee)
        LOGF = open(os.path.join(c, 'lectura.txt'), 'w', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        lee(c, log); return 0
    modo = 'humo' if a.humo else 'explora'
    m = MODOS[modo]; os.makedirs(DATOS, exist_ok=True)
    prev = sorted(d for d in os.listdir(DATOS) if d.startswith(modo + '_'))
    carpeta = os.path.join(DATOS, prev[-1] if (a.reanuda and prev) else time.strftime(f'{modo}_%Y%m%d_%H%M%S'))
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time()
    log(f"CORRE_MM · {modo} · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {platform.python_version()} · pool {a.pool or 'NO'} · "
        f"runner {h16(os.path.abspath(__file__))} · {PRERREGISTRO} · indices {m['ind']} · npas {m['npas']} · T_pas {m['T_pas']} · T_pru {m['T_pru']} · "
        f"T_EST {T_EST} · pasajes {sem_pas(m, m['ind'][0], 0)}.. · prueba {[sem_pru(m, i) for i in m['ind']]} · CFG10 {CFG10} · "
        f"{'REANUDA · ' if a.reanuda else ''}{carpeta}")
    if not verifica(log): log("  ALGO FALLA -> no se corre."); return 1
    if modo == 'explora':
        aok, atxt = arnes_pasado(); log(f"  arnes: {atxt}")
        if not aok: log("  el arnes no esta pasado con los shas actuales -> no se corre."); return 1
    tareas = [(b, i, carpeta, modo) for i in m['ind'] for b in m['brazos']]   # pareadas: los dos brazos del mismo indice juntos
    X = []

    def informa(x):
        X.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} i{x['i']} ({x['seg']}s) aborto {x['aborto']} · fraccion A {x.get('frac_A')} · "
                         f"cruzan {x.get('cruzan')}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): informa(x)
    else:
        for t in tareas: informa(trabajo(t))
    log(f"  {len(X)} trabajos · abortos {sum(1 for x in X if x['aborto'])} · {time.time()-t0:.1f}s")
    lee(carpeta, log, modo)
    return 0


if __name__ == '__main__':
    sys.exit(main())
