"""f0_relojes.py — ficha F0 (ENTREGA_1_reactor.md): reloj (generaciones efectivas n), Ne y s implicita, desde los JSON crudos ya guardados.

SOLO LECTURA de los worktrees o1libre y organelos. Escribe SOLO en su propia carpeta: f0_relojes.json (la salida de texto la
redirige quien lo corre: python f0_relojes.py > f0_relojes_salida.txt). Un proceso, sin Pool, sin correr ninguna pista.
Determinista: bootstrap con semilla fija (SEMILLA_BOOT).

ESTIMADORES (declarados antes de mirar numeros; ver F0_relojes.md sec. 4):
  n (via i, reloj mutacional): en el brazo NEUTRO los genes no se leen, asi que cada gen es un paseo N(0, (sigma*escala_j)^2) por
      evento de mutacion (fundador o parto) y E[((g - fabrica)/(sigma*escala_j))^2] = n = numero de eventos de mutacion entre la
      fabrica y el genoma muestreado (generaciones + una por cada siembra). El recorte SOLO puede bajar el estimador.
      Conjuntos de genes fijados por distancia de la fabrica al recorte mas cercano, en sigmas del gen:
        LEJOS >= 25 sigmas (inmune al recorte incluso si n fuera 100) · MEDIO >= 10 sigmas (principal si n <= ~15) · TODOS.
  n (via ii): la genealogia encadenada NO ESTA en los JSON. Se dan (a) una COTA SUPERIOR demografica (1 + nacimientos reales por
      linaje; 0.75x en o1_libre porque la siembra muestrea partos de la segunda mitad) y (b) en o1_libre un PROXY por padres distintos
      de la siembra (cuerpos que de verdad paren, encadenados dentro del linaje): D/9 + (D/9 + 1)/2 por pasaje.
  Ne: Ne_linajes = 1/sum p_l^2 (aportes por linaje a la siembra; maximo 9) y Ne_padres = 1/sum p_k^2 (aportes por genoma de padre
      distinto dentro de la siembra; NO es un Ne por generacion: junta padres de 50k pasos).
  s (modelo: ecuacion del criador, gradiente lineal): D = media(sel) - media(neu) del gen en la siembra final (pareado por cadena);
      beta = D / (n * V), con V = varianza del gen DENTRO de la siembra del brazo con seleccion (media de pasajes) y n = reloj del
      neutro; s_sigma = beta * sigma_j (ventaja por generacion de un paso mutacional); s_nivel = beta * nivel alcanzado (ventaja del
      nivel evolucionado frente a 0). Incertidumbre: bootstrap sobre cadenas (remuestreo conjunto de D, V, n, Ne).
  s directa (solo o1_libre): (conquista mix - conquista mixA) / nacimientos del lado lib en mixA, pareado por indice.
"""
import glob, json, os, re, sys
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = r'C:\Users\User\Documents\PROYECTOS\JUACO'
OL = os.path.join(BASE, 'o1libre', 'experimentos', 'organelos', 'o1_libre', 'datos')
OE = os.path.join(BASE, 'organelos', 'experimentos', 'organelos', 'o1_evo', 'datos')
EL = os.path.join(BASE, 'organelos', 'experimentos', 'organelos', 'condiciones', 'entre_linajes', 'datos')
SEMILLA_BOOT = 20261001; NBOOT = 10000
SIGMA = 0.03

# o1_libre: construye_o1_lib.py:53-59 (GENES, FABRICA, CLIP, ESCALA); sigma corre_o1_libre.py:71
G_LIB = ('MARGEN', 'PRUEBA', 'PEN_OTRO', 'D0', 'PISO', 'U4', 'U2', 'U1', 'XURG', 'TOPE', 'MEM', 'SOC', 'RES', 'PAU')
F_LIB = (0.25, 0.5, 0.35, 3.0, 0.2, 4.0, 2.0, 1.0, 0.3, 0.5, 0.0, 0.0, 0.0, 0.0)
C_LIB = ((-0.5, 0.5), (0.0, 1.5), (0.0, 1.5), (0.5, 10.0), (0.0, 1.0), (0.0, 10.0), (0.0, 10.0), (0.0, 10.0), (0.0, 1.0), (0.0, 1.5),
         (0.0, 1.0), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0))
E_LIB = tuple(max(1.0, abs(f)) for f in F_LIB)
# o1_evo y entre_linajes (mismo carro O1_PAS): construye_o1_pas.py:45-47; mutacion SIN escala (:68); sigma corre_o1_evo.py:63
G_PAS = ('MARGEN', 'PRUEBA', 'PEN_OTRO', 'PISO'); F_PAS = (0.25, 0.5, 0.35, 0.2)
C_PAS = ((-0.5, 0.5), (0.0, 1.5), (0.0, 1.5), (0.0, 1.0)); E_PAS = (1.0, 1.0, 1.0, 1.0)

EXPS = [
    dict(nombre='o1_libre SERIE', carpeta=os.path.join(OL, 'serie_i734201-734210_20260930_182134'), sel='lib', neu='neu', otros=(),
         G=G_LIB, F=F_LIB, C=C_LIB, E=E_LIB, tipo='libre', npas=3, T=100000, frac_muestra=0.75),
    dict(nombre='o1_libre REPLICA', carpeta=os.path.join(OL, 'replica_i734501-734510_20260930_225227'), sel='lib', neu='neu', otros=(),
         G=G_LIB, F=F_LIB, C=C_LIB, E=E_LIB, tipo='libre', npas=3, T=100000, frac_muestra=0.75),
    dict(nombre='o1_evo SERIE', carpeta=os.path.join(OE, 'serie_i617201-617220_20260929_193426'), sel='o1pas', neu='o1neu', otros=(),
         G=G_PAS, F=F_PAS, C=C_PAS, E=E_PAS, tipo='evo', npas=10, T=25000, frac_muestra=1.0),
    dict(nombre='entre_linajes EXPLORA', carpeta=os.path.join(EL, 'explora_i624201-624205_20260930_174213'), sel='sel', neu='neu',
         otros=('igual',), G=G_PAS, F=F_PAS, C=C_PAS, E=E_PAS, tipo='camara', npas=10, T=25000, frac_muestra=1.0),
]


def r(x, k=3):
    if x is None: return None
    if isinstance(x, (list, tuple, np.ndarray)): return [r(v, k) for v in x]
    try:
        return None if not np.isfinite(x) else round(float(x), k)
    except Exception:
        return x


def q(x, a): return float(np.quantile(np.asarray(x, float), a))
def resumen(x):
    x = np.asarray([v for v in x if v is not None and np.isfinite(v)], float)
    if not len(x): return dict(n=0, med=None, min=None, max=None, media=None)
    return dict(n=int(len(x)), med=r(np.median(x)), min=r(x.min()), max=r(x.max()), media=r(x.mean()))


def boot_idx(n, rng): return rng.integers(0, n, size=(NBOOT, n))


def ic(est, lo=0.025, hi=0.975):
    est = np.asarray(est, float); est = est[np.isfinite(est)]
    return [r(q(est, lo), 4), r(q(est, hi), 4)] if len(est) else [None, None]


def lee(exp):
    """-> PAS[brazo][i][p] = dict(fila, S = matriz genomas x genes de siembra_sig), y numero de archivos leidos."""
    PAS = {}; n_arch = 0
    for f in sorted(glob.glob(os.path.join(exp['carpeta'], 'pasaje_i*_*_p*.json'))):
        m = re.match(r'pasaje_i(\d+)_([a-z0-9A-Z]+)_p(\d+)\.json$', os.path.basename(f))
        if not m: continue
        with open(f, encoding='utf-8') as fh: d = json.load(fh)
        n_arch += 1
        S = np.array([[e[k] for k in exp['G']] for e in (d['siembra_sig'] or [])], float)
        PAS.setdefault(m.group(2), {}).setdefault(int(m.group(1)), {})[int(m.group(3))] = dict(fila=d['fila'], S=S)
    PRU = {}
    for f in sorted(glob.glob(os.path.join(exp['carpeta'], 'prueba_i*_*.json'))):
        m = re.match(r'prueba_i(\d+)_([a-z0-9A-Z]+)\.json$', os.path.basename(f))
        with open(f, encoding='utf-8') as fh: d = json.load(fh)
        n_arch += 1
        PRU.setdefault(m.group(2), {})[int(m.group(1))] = d
    return PAS, PRU, n_arch


def ne_inv(c):
    c = np.asarray(c, float); c = c[c > 0]
    return float(c.sum() ** 2 / (c ** 2).sum()) if len(c) else None


def padres(S):
    """genomas distintos de la siembra y Ne por genoma (1/sum p^2)."""
    if not len(S): return 0, None
    _, cnt = np.unique(np.round(S, 12), axis=0, return_counts=True)
    return int(len(cnt)), ne_inv(cnt)


def conjuntos(exp):
    sd = [SIGMA * e for e in exp['E']]
    dist = [min(f - c[0], c[1] - f) / s for f, c, s in zip(exp['F'], exp['C'], sd)]
    lejos = [j for j, d in enumerate(dist) if d >= 25]; medio = [j for j, d in enumerate(dist) if d >= 10]
    c = dict(LEJOS=lejos, MEDIO=medio, TODOS=list(range(len(sd))))
    if len(sd) == 14: c['O1x10'] = list(range(10)); c['PODERES'] = [10, 11, 12, 13]   # contraste: los 10 genes de O1 (ficha F0) y los 4 poderes (recorte en 0)
    return c, dist, sd


def z2(S, exp):
    sd = np.array([SIGMA * e for e in exp['E']]); return ((S - np.array(exp['F'])) / sd) ** 2


def analiza(exp, rng, log):
    PAS, PRU, n_arch = lee(exp)
    G = exp['G']; npas = exp['npas']; sel = exp['sel']; neu = exp['neu']
    brazos = [sel, neu] + list(exp['otros'])
    I = sorted(PAS[neu]); nI = len(I)
    conj, dist, sd = conjuntos(exp)
    principal = 'MEDIO'
    log(f"\n{'=' * 118}\n{exp['nombre']}  ·  {exp['carpeta']}")
    log(f"  ARCHIVOS LEIDOS: {n_arch} (pasajes {sum(len(PAS[b][i]) for b in PAS for i in PAS[b])}, pruebas {sum(len(v) for v in PRU.values())}) · "
        f"cadenas por brazo {dict((b, len(PAS[b])) for b in PAS)} · pasajes por cadena {npas} x T {exp['T']}")
    log(f"  genes y distancia de la fabrica al recorte mas cercano, en sigmas del gen: " + ' '.join(f"{g}:{d:.1f}" for g, d in zip(G, dist)))
    log(f"  conjuntos: LEJOS(>=25s) {[G[j] for j in conj['LEJOS']]} · MEDIO(>=10s) {[G[j] for j in conj['MEDIO']]} · principal = {principal}")
    out = dict(nombre=exp['nombre'], carpeta=exp['carpeta'], archivos_leidos=n_arch, indices=I, genes=list(G), dist_recorte_sigmas=r(dist, 2),
               conjuntos={k: [G[j] for j in v] for k, v in conj.items()})

    # ---------------- demografia por pasaje y por cadena
    dem = {}
    for b in brazos:
        filas = []
        for p in range(npas):
            rec = dict(partos=[], partos_tarde=[], fund_n=[], fund_siembra=[], fund_colonia=[], nac_lin=[], padres=[], ne_lin=[], ne_pad=[],
                       n_siembra=[], linajes=[], colonos=[])
            for i in I:
                d = PAS[b][i].get(p)
                if d is None: continue
                f = d['fila']; si = f.get('siembra_info') or {}
                rec['partos'].append(f.get('partos_tel'))
                rec['partos_tarde'].append(si.get('tarde'))
                rec['fund_n'].append(f.get('fund_n')); rec['fund_siembra'].append(f.get('fund_de_siembra'))
                rec['fund_colonia'].append(f.get('fund_colonia') if exp['tipo'] == 'libre' else (f.get('camara') or {}).get('colonos_total'))
                rec['nac_lin'].append(float(np.mean(f['nac_reales'])))
                np_, nep = padres(d['S'])
                rec['padres'].append(np_); rec['ne_pad'].append(nep); rec['n_siembra'].append(len(d['S']))
                if exp['tipo'] == 'libre':
                    rec['ne_lin'].append(ne_inv(list(si['por_linaje'].values()))); rec['linajes'].append(si.get('linajes'))
                    if si.get('padres_distintos') != np_: log(f"   AVISO {b} i{i} p{p}: padres_distintos JSON {si.get('padres_distintos')} != recontado {np_}")
                    if abs(si.get('Ne_linajes') - rec['ne_lin'][-1]) > 0.006: log(f"   AVISO {b} i{i} p{p}: Ne_linajes JSON != recontado")
                elif si.get('prop') == 1:
                    rec['ne_lin'].append(ne_inv(list(si['n_por_linaje'].values()))); rec['linajes'].append(si.get('linajes_con_entradas'))
                else:
                    rec['ne_lin'].append(None)   # NO ESTA: siembra igualada, el JSON no guarda de que linaje sale cada entrada
            filas.append(rec)
        dem[b] = filas
    out['demografia'] = {b: [{k: resumen(v) for k, v in rec.items()} for rec in dem[b]] for b in brazos}
    log("\n  DEMOGRAFIA POR PASAJE (mediana [min-max] sobre cadenas)")
    log(f"  {'brazo':6s} {'p':>2s} {'partos':>16s} {'tarde':>14s} {'fund_n':>14s} {'de_siembra':>12s} {'colonos':>14s} {'nac/linaje':>16s} "
        f"{'padres dist.':>13s} {'Ne_linajes':>17s} {'Ne_padres':>17s}")
    fm = lambda s: ('NO ESTA' if s['n'] == 0 else f"{s['med']:g} [{s['min']:g}-{s['max']:g}]")
    for b in brazos:
        for p, rec in enumerate(out['demografia'][b]):
            log(f"  {b:6s} {p:2d} {fm(rec['partos']):>16s} {fm(rec['partos_tarde']):>14s} {fm(rec['fund_n']):>14s} {fm(rec['fund_siembra']):>12s} "
                f"{fm(rec['fund_colonia']):>14s} {fm(rec['nac_lin']):>16s} {fm(rec['padres']):>13s} {fm(rec['ne_lin']):>17s} {fm(rec['ne_pad']):>17s}")
    tot = {}
    for b in brazos:
        allv = lambda k: [v for rec in dem[b] for v in rec[k] if v is not None]
        tot[b] = {k: resumen(allv(k)) for k in ('partos', 'fund_n', 'fund_siembra', 'fund_colonia', 'nac_lin', 'padres', 'ne_lin', 'ne_pad')}
        log(f"  TODOS LOS PASAJES {b}: partos {fm(tot[b]['partos'])} · fundadores {fm(tot[b]['fund_n'])} (de siembra {fm(tot[b]['fund_siembra'])}) · "
            f"padres distintos {fm(tot[b]['padres'])} · Ne_linajes {fm(tot[b]['ne_lin'])} · Ne_padres {fm(tot[b]['ne_pad'])}")
    out['demografia_total'] = tot

    # ---------------- n via (i): reloj mutacional
    def n_cadena(b, p, cols):   # por cadena: media sobre genomas y genes
        return np.array([z2(PAS[b][i][p]['S'], exp)[:, cols].mean() if p in PAS[b][i] else np.nan for i in I])
    reloj = {}
    log("\n  RELOJ via (i): n acumulado = E[((g - fabrica)/sigma_j)^2] en la siembra tras el pasaje p (por cadena; mediana [min-max]; media e IC95 bootstrap sobre cadenas)")
    B = boot_idx(nI, rng)
    for b in brazos:
        reloj[b] = {}
        for cn, cols in conj.items():
            if not cols: reloj[b][cn] = None; continue
            filas = []
            for p in range(npas):
                x = n_cadena(b, p, cols); s = resumen(x); bm = np.nanmean(x[B], axis=1)
                filas.append(dict(p=p, por_cadena=r(x, 2), med=s['med'], min=s['min'], max=s['max'], media=r(np.nanmean(x), 2), ic95=ic(bm)))
            reloj[b][cn] = filas
        for cn in conj:
            if reloj[b][cn] is None: log(f"  {b:6s} {cn:6s}: sin genes en el conjunto"); continue
            log(f"  {b:6s} {cn:6s}: " + ' | '.join(f"p{f['p']} {f['med']:.1f} [{f['min']:.1f}-{f['max']:.1f}] media {f['media']:.1f} IC {f['ic95'][0]:.1f}-{f['ic95'][1]:.1f}"
                                                 for f in reloj[b][cn] if f['p'] in (0, 1, 2, npas - 1)))
    out['reloj_mutacional'] = reloj
    # por gen (neutro, siembra final, todas las cadenas juntas) y fraccion pegada al recorte
    Sfin = np.vstack([PAS[neu][i][npas - 1]['S'] for i in I if npas - 1 in PAS[neu][i]])
    por_gen = z2(Sfin, exp).mean(axis=0)
    pegado = [float(np.mean((Sfin[:, j] <= exp['C'][j][0]) | (Sfin[:, j] >= exp['C'][j][1]))) for j in range(len(G))]
    out['n_por_gen_neutro_final'] = {g: dict(n=r(v, 2), frac_en_recorte=r(pg, 4)) for g, v, pg in zip(G, por_gen, pegado)}
    log(f"  n POR GEN (neutro, siembra final, todas las cadenas): " + ' '.join(f"{g}:{v:.1f}" for g, v in zip(G, por_gen)))
    log(f"  fraccion de genomas EN el recorte (neutro, final): " + ' '.join(f"{g}:{v:.2f}" for g, v in zip(G, pegado)))
    cp = conj[principal]
    log(f"  n por gen del conjunto {principal}: mediana {np.median(por_gen[cp]):.1f} [min {por_gen[cp].min():.1f} - max {por_gen[cp].max():.1f}] ({len(cp)} genes)")
    out['n_por_gen_principal'] = dict(mediana=r(np.median(por_gen[cp]), 2), min=r(por_gen[cp].min(), 2), max=r(por_gen[cp].max(), 2))
    # incremento por pasaje (neutro, principal)
    acum = np.array([n_cadena(neu, p, cp) for p in range(npas)])        # p x cadena
    inc = np.diff(np.vstack([np.zeros(nI), acum]), axis=0)
    out['n_incremento_por_pasaje_neutro'] = [dict(p=p, **resumen(inc[p])) for p in range(npas)]
    log(f"  incremento de n por pasaje (neutro, {principal}; mediana [min-max]): " + ' | '.join(f"p{p} {np.nanmedian(inc[p]):.1f} [{np.nanmin(inc[p]):.1f}-{np.nanmax(inc[p]):.1f}]" for p in range(npas)))
    n_fin = acum[-1]

    # ---------------- n via (ii): genealogia NO ESTA; cota demografica y proxy por padres
    nac = np.array([[np.mean(PAS[neu][i][p]['fila']['nac_reales']) for i in I] for p in range(npas)])
    cota = (1 + exp['frac_muestra'] * nac).sum(axis=0)
    out['n_via_ii'] = dict(genealogia='NO ESTA: la fila guarda conteos y siembra_sig, no los partos encadenados (tel[partos] con t y padre no se escribe)',
                           cota_superior_demografica=resumen(cota))
    log(f"\n  RELOJ via (ii): genealogia encadenada NO ESTA en los JSON (solo conteos por linaje y la siembra).")
    log(f"    COTA SUPERIOR demografica (neutro): sum_p [1 + {exp['frac_muestra']} x nacimientos reales por linaje] = {fm(resumen(cota))}  (supone 1 generacion por nacimiento)")
    if exp['tipo'] == 'libre':
        D = np.array([[padres(PAS[neu][i][p]['S'])[0] for i in I] for p in range(npas)], float)
        lin = np.array([[PAS[neu][i][p]['fila']['siembra_info']['linajes'] for i in I] for p in range(npas)], float)
        k = D / lin; prox = (k + (k + 1) / 2).sum(axis=0)
        out['n_via_ii']['proxy_padres_distintos'] = dict(resumen(prox), por_cadena=r(prox, 2), formula='sum_p [D/L + (D/L + 1)/2], D = padres distintos, L = linajes en la siembra')
        log(f"    PROXY por padres distintos (neutro): sum_p [D/L + (D/L+1)/2] = {fm(resumen(prox))}   ·   via (i) {principal}: {fm(resumen(n_fin))}")
        log(f"    razon nacimientos/padres: {np.median(nac):.0f} nacimientos por linaje y pasaje frente a ~{2 * np.median(k):.1f} cuerpos que paren por linaje y pasaje")

    # ---------------- seleccion por gen (criador)
    log(f"\n  SELECCION POR GEN ({sel} contra {neu}; siembra final; modelo del criador; IC95 bootstrap sobre {nI} cadenas; n = reloj del neutro, conjunto {principal})")
    log(f"  {'gen':9s} {'media sel':>9s} {'media neu':>9s} {'D':>8s} {'IC95 D':>19s} {'gana':>5s} {'V dentro':>9s} {'s_sigma':>8s} {'IC95':>19s} {'s_nivel':>8s} {'IC95':>19s}")
    _nl = [[v for v in [dem[sel][p]['ne_lin'][c] for p in range(npas)] if v is not None] for c in range(nI)]
    ne_lin_c = np.array([float(np.mean(v)) if v else np.nan for v in _nl])
    ne_pad_c = np.array([np.nanmean([dem[sel][p]['ne_pad'][c] for p in range(npas)]) for c in range(nI)])
    if not np.isfinite(ne_lin_c).any(): ne_lin_c = np.full(nI, 9.0)   # siembra igualada: 9 por construccion (corre_o1_evo.py:130-137)
    selg = {}
    for j, g in enumerate(G):
        zs = np.array([PAS[sel][i][npas - 1]['S'][:, j].mean() for i in I]); zn = np.array([PAS[neu][i][npas - 1]['S'][:, j].mean() for i in I])
        V = np.array([np.mean([PAS[sel][i][p]['S'][:, j].var() for p in range(npas)]) for i in I])
        Dm = (zs - zn)[B].mean(axis=1); nb = n_fin[B].mean(axis=1); Vb = V[B].mean(axis=1)
        beta_b = Dm / (nb * Vb); beta = (zs - zn).mean() / (n_fin.mean() * V.mean())
        nivel = zs.mean() - exp['F'][j] if exp['F'][j] != 0 else zs.mean()
        nivel_b = (zs[B].mean(axis=1) - exp['F'][j])
        s_sig = beta * sd[j]; s_niv = beta * nivel
        d = dict(media_sel=r(zs.mean(), 4), media_neu=r(zn.mean(), 4), D=r((zs - zn).mean(), 4), D_ic95=ic(Dm), gana=int((zs > zn).sum()),
                 V_dentro=r(V.mean(), 6), beta=r(beta, 3), s_sigma=r(s_sig, 4), s_sigma_ic95=ic(beta_b * sd[j]),
                 s_nivel=r(s_niv, 4), s_nivel_ic95=ic(beta_b * nivel_b),
                 Ne_linajes_x_s_sigma=r(np.nanmean(ne_lin_c) * s_sig, 3), Ne_linajes_x_s_sigma_ic95=ic(np.nanmean(ne_lin_c[B], axis=1) * beta_b * sd[j]),
                 Ne_linajes_x_s_nivel=r(np.nanmean(ne_lin_c) * s_niv, 3), Ne_linajes_x_s_nivel_ic95=ic(np.nanmean(ne_lin_c[B], axis=1) * beta_b * nivel_b),
                 Ne_padres_x_s_sigma=r(ne_pad_c.mean() * s_sig, 3), Ne_padres_x_s_sigma_ic95=ic(ne_pad_c[B].mean(axis=1) * beta_b * sd[j]),
                 Ne_padres_x_s_nivel=r(ne_pad_c.mean() * s_niv, 3), Ne_padres_x_s_nivel_ic95=ic(ne_pad_c[B].mean(axis=1) * beta_b * nivel_b))
        selg[g] = d
        log(f"  {g:9s} {d['media_sel']:9.4f} {d['media_neu']:9.4f} {d['D']:8.4f} {str(d['D_ic95']):>19s} {d['gana']:2d}/{nI:<2d} {d['V_dentro']:9.5f} "
            f"{d['s_sigma']:8.4f} {str(d['s_sigma_ic95']):>19s} {d['s_nivel']:8.4f} {str(d['s_nivel_ic95']):>19s}")
    out['seleccion_por_gen'] = selg
    out['Ne_usados'] = dict(Ne_linajes_media=r(np.nanmean(ne_lin_c), 2), Ne_padres_media=r(ne_pad_c.mean(), 2), brazo=sel)
    log(f"  Ne usados (brazo {sel}, media de cadenas y pasajes): Ne_linajes {np.nanmean(ne_lin_c):.2f} · Ne_padres {ne_pad_c.mean():.2f}")
    for g in (['MEM', 'PISO'] if 'MEM' in G else ['PISO']):
        d = selg[g]
        if g == 'PISO':
            log(f"  >>> PISO (contraste: el gen de O1 que mas se mueve): Ne_linajes x s_sigma = {d['Ne_linajes_x_s_sigma']} IC {d['Ne_linajes_x_s_sigma_ic95']} · Ne_padres x s_sigma = {d['Ne_padres_x_s_sigma']} IC {d['Ne_padres_x_s_sigma_ic95']}")
            continue
        log(f"  >>> MEM: Ne_linajes x s_sigma = {d['Ne_linajes_x_s_sigma']} IC {d['Ne_linajes_x_s_sigma_ic95']} · Ne_linajes x s_nivel = {d['Ne_linajes_x_s_nivel']} IC {d['Ne_linajes_x_s_nivel_ic95']}")
        log(f"  >>> MEM: Ne_padres  x s_sigma = {d['Ne_padres_x_s_sigma']} IC {d['Ne_padres_x_s_sigma_ic95']} · Ne_padres  x s_nivel = {d['Ne_padres_x_s_nivel']} IC {d['Ne_padres_x_s_nivel_ic95']}")
    if 'MEM' not in G:
        log("  s de MEM: NO ESTA (el carro O1_PAS no tiene gen de memoria: 4 genes, construye_o1_pas.py:45). Se dan los 4 genes que si existen.")
        mej = max(G, key=lambda g: abs(selg[g]['s_sigma']))
        d = selg[mej]
        log(f"  >>> gen con mayor |s_sigma| (ELEGIDO DESPUES DE MIRAR: sesgado hacia arriba): {mej} · Ne_linajes x s_sigma = {d['Ne_linajes_x_s_sigma']} IC {d['Ne_linajes_x_s_sigma_ic95']} "
            f"· Ne_padres x s_sigma = {d['Ne_padres_x_s_sigma']} IC {d['Ne_padres_x_s_sigma_ic95']}")
        out['gen_mayor_s'] = mej

    # ---------------- trayectoria de MEM por pasaje (o1_libre)
    if 'MEM' in G:
        j = G.index('MEM'); tr = []
        for p in range(npas):
            a = np.array([PAS[sel][i][p]['S'][:, j].mean() for i in I]); b_ = np.array([PAS[neu][i][p]['S'][:, j].mean() for i in I])
            tr.append(dict(p=p, lib=r(a.mean(), 4), neu=r(b_.mean(), 4), D=r((a - b_).mean(), 4), D_ic95=ic((a - b_)[B].mean(axis=1)), gana=int((a > b_).sum()),
                           lib_mediana=r(np.median(a), 4), neu_mediana=r(np.median(b_), 4)))
        out['trayectoria_MEM'] = tr
        log("  trayectoria de MEM (media de cadenas; D = lib - neu pareado): " + ' | '.join(f"p{t['p']} lib {t['lib']:.3f} neu {t['neu']:.3f} D {t['D']:+.3f} IC {t['D_ic95']} gana {t['gana']}/{nI}" for t in tr))
        # s directa: mix - mixA
        if 'mix' in PRU and 'mixA' in PRU:
            ii = [i for i in I if i in PRU['mix'] and i in PRU['mixA'] and PRU['mix'][i].get('grupo') and PRU['mixA'][i].get('grupo')]
            dq = np.array([PRU['mix'][i]['grupo']['conquista'] - PRU['mixA'][i]['grupo']['conquista'] for i in ii])
            dl = np.array([np.mean(PRU['mix'][i]['grupo']['lib']['nac']) - np.mean(PRU['mixA'][i]['grupo']['lib']['nac']) for i in ii])
            ba = np.array([np.mean(PRU['mixA'][i]['grupo']['lib']['nac']) for i in ii])
            Bd = boot_idx(len(ii), rng)
            s_dir = dq.mean() / ba.mean(); s_dir_b = dq[Bd].mean(axis=1) / ba[Bd].mean(axis=1)
            s_lado = dl.mean() / ba.mean(); s_lado_b = dl[Bd].mean(axis=1) / ba[Bd].mean(axis=1)
            nl = float(np.nanmean(ne_lin_c)); npd = float(ne_pad_c.mean())
            out['s_directa_mix_menos_mixA'] = dict(indices=len(ii), dif_conquista_por_indice=r(dq, 2), dif_mediana=r(np.median(dq), 3), dif_media=r(dq.mean(), 3),
                                                  nac_lado_lib_mixA_media=r(ba.mean(), 2), nac_lado_lib_mixA_mediana=r(np.median(ba), 2),
                                                  s_investigador_mediana_sobre_mediana=r(np.median(dq) / np.median(ba), 4),
                                                  s=r(s_dir, 4), s_ic95=ic(s_dir_b), mix_gana_mixA=int((dq > 0).sum()),
                                                  s_solo_lado_lib=r(s_lado, 4), s_solo_lado_lib_ic95=ic(s_lado_b),
                                                  Ne_linajes_x_s=r(nl * s_dir, 3), Ne_linajes_x_s_ic95=ic(nl * s_dir_b),
                                                  Ne_padres_x_s=r(npd * s_dir, 3), Ne_padres_x_s_ic95=ic(npd * s_dir_b))
            o = out['s_directa_mix_menos_mixA']
            log(f"  s DIRECTA (prueba 100k; los 4 poderes a la vez, no solo MEM): conquista mix - mixA por indice {o['dif_conquista_por_indice']}")
            log(f"    mediana {o['dif_mediana']} · media {o['dif_media']} · mix > mixA en {o['mix_gana_mixA']}/{len(ii)} · nacimientos lado lib en mixA: media {o['nac_lado_lib_mixA_media']}, mediana {o['nac_lado_lib_mixA_mediana']}")
            log(f"    s (media/media) = {o['s']} IC95 {o['s_ic95']} · al modo del investigador (mediana/mediana) = {o['s_investigador_mediana_sobre_mediana']} · solo lado lib = {o['s_solo_lado_lib']} IC95 {o['s_solo_lado_lib_ic95']}")
            log(f"  >>> Ne_linajes x s_directa = {o['Ne_linajes_x_s']} IC {o['Ne_linajes_x_s_ic95']} · Ne_padres x s_directa = {o['Ne_padres_x_s']} IC {o['Ne_padres_x_s_ic95']}")

    # ---------------- resumen para la tabla
    cp_ = reloj[neu][principal]
    out['tabla'] = dict(n_total_neutro=dict(med=cp_[-1]['med'], min=cp_[-1]['min'], max=cp_[-1]['max'], media=cp_[-1]['media'], ic95=cp_[-1]['ic95']),
                        n_total_sel=dict(med=reloj[sel][principal][-1]['med'], min=reloj[sel][principal][-1]['min'], max=reloj[sel][principal][-1]['max']),
                        n_LEJOS_neutro=(None if reloj[neu]['LEJOS'] is None else dict(med=reloj[neu]['LEJOS'][-1]['med'], media=reloj[neu]['LEJOS'][-1]['media'], ic95=reloj[neu]['LEJOS'][-1]['ic95'])),
                        n_por_pasaje_neutro=r(float(np.nanmedian(inc)), 2))
    return out


def main():
    rng = np.random.default_rng(SEMILLA_BOOT)
    L = []
    def log(s=''): print(s, flush=True); L.append(s)
    log(f"F0_RELOJES · semilla bootstrap {SEMILLA_BOOT} · {NBOOT} remuestreos · sigma {SIGMA} · numpy {np.__version__}")
    R = []
    for exp in EXPS:
        if not os.path.isdir(exp['carpeta']): log(f"\n{exp['nombre']}: NO ESTA la carpeta {exp['carpeta']}"); continue
        R.append(analiza(exp, rng, log))
    log(f"\n{'=' * 118}\nRESUMEN (n = reloj mutacional del neutro, conjunto MEDIO; por cadena)")
    for o in R:
        t = o['tabla']
        log(f"  {o['nombre']:24s} archivos {o['archivos_leidos']:4d} · n total mediana {t['n_total_neutro']['med']} [{t['n_total_neutro']['min']}-{t['n_total_neutro']['max']}] "
            f"media {t['n_total_neutro']['media']} IC95 {t['n_total_neutro']['ic95']} · n LEJOS {t['n_LEJOS_neutro']} · por pasaje {t['n_por_pasaje_neutro']} · "
            f"Ne_linajes {o['Ne_usados']['Ne_linajes_media']} · Ne_padres {o['Ne_usados']['Ne_padres_media']}")
    pred = [o for o in R if o['nombre'].startswith('o1_libre')]
    ok = all(o['tabla']['n_total_neutro']['ic95'][1] <= 15 for o in pred)
    log(f"\nPREDICCION F0 (n <= 15 en 3 pasajes, serie y replica; se exige IC95 superior de la media <= 15): {'SE CUMPLE' if ok else 'CAE o NO DECIDE (ver intervalos)'}")
    log(f"CONTROL (n >= 100): {'GANA' if any(o['tabla']['n_total_neutro']['ic95'][0] >= 100 for o in pred) else 'NO GANA'}")
    with open(os.path.join(AQUI, 'f0_relojes.json'), 'w', encoding='utf-8') as fh:
        json.dump(dict(semilla_boot=SEMILLA_BOOT, nboot=NBOOT, sigma=SIGMA, experimentos=R), fh, ensure_ascii=False, indent=1)
    log(f"escrito {os.path.join(AQUI, 'f0_relojes.json')}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
