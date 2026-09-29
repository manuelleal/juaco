"""corre_pasajes.py — PASAJES SERIADOS en ECO (reunion 28-sep-2026, Opus A; EXPLORATORIO, sin preregistro de bloque).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como. Principio del director: que la evolucion construya el organo, solo con seleccion.

Encargo del director: "apenas evolucione, seguir evolucionando al que evoluciono (pasajes cortos)".
Un PASAJE = una corrida de nucleo_pasajes.trabajo (== nucleo_eco_sel_ing: ECO w90, hijo INGENUO FABRICA_ECO, vivero permanente) de
T_p pasos. Al final, la TRANSFERENCIA toma 90 genomas AL AZAR de los cuerpos VIVOS en T_p (vivos_final[i][4:]; sin juez, sin mirar
hijos, edad ni linaje: solo el genoma) y siembra con ellos los 90 fundadores (y el banco inicial) del pasaje siguiente. La mutacion es
la de siempre (la del motor en cada parto y refundacion). Brazos (todos por cadena de pasajes, misma semilla base s):
  PAS_SEL   CEREBRO (15 genes, donante padre)            transfiere los vivos
  PAS_RES   CEREBRO                                      CONTROL: cada pasaje p >= 2 arranca de G0 mutado UNA vez por fundador
                                                         (motor_eco.muta, mismos p_mut/sigma): sin herencia entre pasajes
  PAS_AZA   CEREBRO_AZAR (sin herencia DENTRO del pasaje) transfiere los vivos
  PAS_SELM  CEREBRO_M (15 + rep_umbral)                  transfiere los vivos
  PAS_F1    MUT0 (base sin variacion)                    referencia por pasaje (no transfiere nada: G0)
Semilla de la corrida del pasaje p (1..n): 100*s + p (la MISMA en todos los brazos: pareado). Semillas base 47801-47805.
Medida por pasaje: fund_2a (fundadores repuestos en [T_p/2, T_p]) y su razon contra PAS_F1 pareado; fundadores_rep; K; K_nac; medias
de los genes mutables en los vivos en T_p.

Uso:  python corre_pasajes.py --humo                          # 1 proceso: semilla 47809, 2 pasajes de 20 000 en PAS_SEL y PAS_RES (4 corridas)
      python corre_pasajes.py --cadena PAS_SEL --s 47801 --n 8 --T 50000   # una cadena (un proceso)
      python corre_pasajes.py --cadena PAS_AZA --s 47801 --n 40 --T 50000 --continua   # sigue una cadena escrita hasta n
      python corre_pasajes.py --lee                             # tabla por pasaje de todo lo que hay en datos/
"""
import argparse, glob, hashlib, json, os, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import nucleo_pasajes as N
CR = N.CR
ME = N.ME_PY            # motor_eco (Python): muta, rangos, genoma0, NOMBRES (el gemelo usa las MISMAS funciones)
DATOS = os.path.join(AQUI, 'datos')
NF = 90                 # fundadores (MUNDO['n0'])
SHA_NUCLEO = '56c067e976b6b626'
FIJOS = {'eco_sel_ing/nucleo_eco_sel_ing.py': 'c2189f9d22b72386', 'frio/motor_frio_rapido.py': 'ff9d890a5cce9dec',
         'juaco_eco/motor_eco.py': 'bca3033878b59622', 'juaco_eco/carros/FABRICA_ECO.py': 'f1163009cb5193a2'}
TRANSFIERE = {'PAS_SEL': 'vivos', 'PAS_AZA': 'vivos', 'PAS_SELM': 'vivos', 'PAS_RES': 'resorteo', 'PAS_F1': 'nada'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica():
    import construye_pasajes as CP
    R = N.RAIZ; E = os.path.join(R, 'experimentos')
    rutas = {'eco_sel_ing/nucleo_eco_sel_ing.py': os.path.join(E, 'organelos', 'eco_sel_ing', 'nucleo_eco_sel_ing.py'),
             'frio/motor_frio_rapido.py': os.path.join(E, 'organelos', 'frio', 'motor_frio_rapido.py'),
             'juaco_eco/motor_eco.py': os.path.join(E, 'juaco_eco', 'motor_eco.py'),
             'juaco_eco/carros/FABRICA_ECO.py': os.path.join(E, 'juaco_eco', 'carros', 'FABRICA_ECO.py')}
    mal = {k: (h16(p), FIJOS[k]) for k, p in rutas.items() if h16(p) != FIJOS[k]}
    if mal: raise SystemExit(f"PASAJES: origenes con otro sha {mal}")
    if not CP.main(['--verifica']): raise SystemExit('PASAJES: nucleo_pasajes.py no es el construido por anclas')
    if h16(os.path.join(AQUI, 'nucleo_pasajes.py')) != SHA_NUCLEO: raise SystemExit('PASAJES: nucleo con otro sha')
    return dict(FIJOS, nucleo_pasajes=SHA_NUCLEO, corre_pasajes=h16(os.path.abspath(__file__)))


def G0_lo_hi():
    import pista2 as P
    G0 = ME.genoma0(P.cfg_fabrica()); lo, hi = ME.rangos(G0)
    return G0, lo, hi


def transfiere_vivos(vivos_final, rng, nf=NF):
    """LA TRANSFERENCIA (sin fitness): solo lee el GENOMA de cada vivo (v[4:]); ignora linaje, k, generacion y tn. 90 al azar, sin
    reemplazo si hay >= 90 vivos (con reemplazo si hay menos). Recorta a [lo, hi] (vivos_final viene redondeado a 6 decimales)."""
    G0, lo, hi = G0_lo_hi()
    V = np.array([v[4:] for v in vivos_final], float)
    if len(V) == 0: return None
    idx = rng.choice(len(V), size=nf, replace=len(V) < nf)
    return np.clip(V[idx], lo, hi)


def resorteo(rng_de, pv, sigma, nf=NF):
    """CONTROL: G0 mutado UNA vez por fundador (motor_eco.muta, la misma p por gen y sigma del brazo). Sin herencia entre pasajes."""
    G0, lo, hi = G0_lo_hi()
    return np.array([ME.muta(G0, rng_de(i), pv, sigma, lo, hi)[0] for i in range(nf)])


def pv_de(brazo):
    g = N.GENETICAS[N.BRAZOS[brazo][0]]
    mut = ME.NOMBRES if g['mutables'] is None else tuple(g['mutables'])
    p = N.SERIE['p_mut'] if g['p'] else 0.0
    return np.array([float(p) if nm in mut else 0.0 for nm in ME.NOMBRES]), float(N.SERIE['sigma'])


def kbar(x, T):
    """== corre_eco_sel_ing.kbar (copia textual del cuerpo)."""
    tt = x.get('tam_total')
    if tt is None: return None
    m = N.MUNDO['muestra']; n = T // m + 1; i0 = (T // 2) // m
    v = (list(tt) + [0] * max(0, n - len(tt)))[i0:n]
    return float(np.mean(v))


def pasaje(seed, brazo, T, carpeta, genoma=None):
    """UN pasaje: nucleo_pasajes.trabajo con t_corte = T (vivero permanente) y los genomas fundadores `genoma` (None = G0)."""
    g = None if genoma is None else np.asarray(genoma, float).tolist()
    return N.trabajo((seed, brazo, T, N.tc_de(brazo, T), N.FRIO['T_lect'], carpeta, False, g))


def resumen(r, T, p, s, genoma_in):
    gv = r.get('genes_vivos_T') or {}
    return dict(s=s, p=p, seed=r['seed'], brazo=r['brazo'], T=T, persiste=r.get('persiste'), vivos_T=r.get('vivos_T'),
                K=(None if r.get('tam_total') is None else round(kbar(r, T), 3)), K_nac=r.get('K_nac'), K_fund=r.get('K_fund'),
                fund_2a=r.get('fund_2a'), fundadores_rep=r.get('fundadores_rep'), n_nac=r.get('n_nac'), bloqueados=r.get('bloqueados'),
                aborto=r.get('aborto'), seg=r.get('seg'), genes=gv,
                genoma_in_medio=(None if genoma_in is None else [round(float(x), 6) for x in np.asarray(genoma_in).mean(0)]))


def _siguiente(modo, r, s, p, pv, sg):
    """El genoma que siembra el pasaje p + 1 a partir del resultado r del pasaje p (la MISMA regla en cadena y en --continua)."""
    if modo == 'vivos': return transfiere_vivos(r['vivos_final'], np.random.default_rng([s, p, 78, 1]))
    if modo == 'resorteo': return resorteo(lambda i: np.random.default_rng([s, p, 78, 2, i]), pv, sg)
    return None


def cadena(brazo, s, n, T, etq=None, log=print, continua=False):
    """n pasajes de T en el brazo, semilla base s. Escribe cada JSON del pasaje, su resumen, y el genoma del ultimo pasaje.
    continua=True: retoma una cadena ya escrita (RESUMEN.json con p0 pasajes) desde el JSON de su pasaje p0 y sigue hasta n."""
    etq = etq or f"pas_{brazo}_s{s}_T{T}"
    carpeta = os.path.join(DATOS, etq); os.makedirs(carpeta, exist_ok=True)
    modo = TRANSFIERE[brazo]; pv, sg = pv_de(brazo)
    genoma = None; filas = []; p0 = 0
    if continua:
        filas = json.load(open(os.path.join(carpeta, 'RESUMEN.json'), encoding='utf-8'))['filas']; p0 = len(filas)
        r0 = json.load(open(os.path.join(carpeta, f"{brazo}_s{100 * s + p0}.json"), encoding='utf-8'))
        if r0.get('aborto') or not r0.get('persiste'): return filas
        genoma = _siguiente(modo, r0, s, p0, pv, sg)
    for p in range(p0 + 1, n + 1):
        seed = 100 * s + p
        r = pasaje(seed, brazo, T, carpeta, genoma)
        f = resumen(r, T, p, s, genoma); filas.append(f)
        log(f"[{time.strftime('%H:%M:%S')}] {brazo} s{s} p{p}: fund_2a {f['fund_2a']} · rep {f['fundadores_rep']} · K {f['K']} · K_nac {f['K_nac']} · "
            f"vivos {f['vivos_T']} · alpha {f['genes'].get('alpha')} · aversion {f['genes'].get('aversion')} · tau_e {f['genes'].get('tau_e')} · "
            f"rep_umbral {f['genes'].get('rep_umbral')} · {f['seg']} s")
        json.dump(dict(filas=filas, brazo=brazo, s=s, n=n, T=T, transfiere=modo), open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'),
                  indent=1, default=str)
        if r.get('aborto') or not r.get('persiste'):
            log(f"  {brazo} s{s}: la cadena se corta en p{p} (aborto {r.get('aborto')}, persiste {r.get('persiste')})"); break
        genoma = _siguiente(modo, r, s, p, pv, sg)
    if modo == 'vivos' and genoma is not None:   # los genomas del ultimo pasaje (los que sembrarian el siguiente): para Opus B
        json.dump(dict(genes=list(ME.NOMBRES), brazo=brazo, s=s, pasajes=n, T=T, origen='90 vivos al azar en T del ultimo pasaje',
                       genomas=[[round(float(x), 6) for x in g] for g in genoma]),
                  open(os.path.join(carpeta, f"genomas_ultimo_{brazo}_s{s}.json"), 'w', encoding='utf-8'))
    return filas


def lee():
    Rs = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(DATOS, 'pas_*', 'RESUMEN.json')))]
    F1 = {(f['s'], f['p']): f for R in Rs if R['brazo'] == 'PAS_F1' for f in R['filas']}
    for R in Rs:
        print(f"== {R['brazo']} s{R['s']} T {R['T']} ({R['transfiere']})")
        for f in R['filas']:
            b = F1.get((f['s'], f['p']))
            rz = (None if not b or not b['fund_2a'] else round(f['fund_2a'] / b['fund_2a'] - 1, 3))
            print(f"  p{f['p']}: fund_2a {f['fund_2a']} (vs F1 {rz}) · K {f['K']} · K_nac {f['K_nac']} · alpha {f['genes'].get('alpha')} · "
                  f"aversion {f['genes'].get('aversion')} · tau_e {f['genes'].get('tau_e')} · rep_umbral {f['genes'].get('rep_umbral')}")


def humo():
    sh = verifica(); N.usa_gemelo()
    os.makedirs(os.path.join(DATOS, 'humo'), exist_ok=True)
    t0 = time.time(); out = {}
    for b in ('PAS_SEL', 'PAS_RES'):
        out[b] = cadena(b, 47809, 2, 20000, etq=f"humo/pas_{b}_s47809_T20000")
    ruta = os.path.join(DATOS, 'humo', f"humo_pasajes_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(dict(shas=sh, filas=out, seg=round(time.time() - t0, 1)), open(ruta, 'w', encoding='utf-8'), indent=1, default=str)
    print(f"HUMO: {round(time.time() - t0, 1)} s · JSON {ruta}")


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--lee', action='store_true')
    ap.add_argument('--cadena', nargs='+', default=None); ap.add_argument('--s', type=int, nargs='+'); ap.add_argument('--n', type=int)
    ap.add_argument('--T', type=int); ap.add_argument('--continua', action='store_true')
    a = ap.parse_args()
    if a.humo: return humo()
    if a.lee: return lee()
    if not a.cadena or not a.s or not a.n or not a.T: raise SystemExit('PASAJES: --cadena BRAZO.. --s S.. --n N --T T')
    for b in a.cadena:
        if b not in TRANSFIERE: raise SystemExit(f"PASAJES: brazo {b}?")
    for s in a.s:
        if not (47801 <= s <= 47808 or 47811 <= s <= 47815 or 47851 <= s <= 47890):
            raise SystemExit('PASAJES: semillas base 47801-47808 (serie) o 47811-47815 (replica) de la reunion; 47851-47890 (nube)')
    sh = verifica(); N.usa_gemelo()
    fl = open(os.path.join(DATOS, f"log_{'_'.join(a.cadena)}_{'_'.join(map(str, a.s))}.txt"), 'a', encoding='utf-8')

    def log(x):
        print(x, flush=True); fl.write(x + '\n'); fl.flush()
    log(f"[{time.strftime('%H:%M:%S')}] PASAJES {a.cadena} s {a.s} n {a.n} T {a.T} · shas {sh}")
    for s in a.s:
        for b in a.cadena:
            cadena(b, s, a.n, a.T, log=log, continua=a.continua)
    fl.close()


if __name__ == '__main__':
    os.makedirs(DATOS, exist_ok=True)
    main()
