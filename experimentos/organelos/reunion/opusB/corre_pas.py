"""corre_pas.py — PASAJES SERIADOS en la pista de la carrera (reunion 28-sep-2026, Opus B). EXPLORATORIO (no es serie; sin letra
confirmatoria). Carros: construye_pas.py (V143_PAS = V143_EVO_BAJO + genoma (g, 15 genes del cerebro) por cuerpo, fundador de SIEMBRA).

MISION: llegar a la AGI por este camino. Principio del director: que la evolucion construya el organo, no nosotros, solo con seleccion natural.
Encargo del director: "apenas evolucione, seguir evolucionando al que evoluciono (pasajes cortos)".

ENTRADA (regla 14): cada corrida ES experimentos/tronco_v14_3/corre_v143.tarea (se IMPORTA, no se toca) = juez.tarea(seed, 9 carros
iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador limpio 1) + juez.resumen_linaje. Lo unico agregado: antes de cada
run el runner fija en el modulo del carro SIEMBRA / PS_SEMILLA / PS_MUT y borra _TEL y _PS_CNT; despues copia _TEL (solo lectura).

PASAJE: una corrida corta (T 25 000) de la pista con semilla nueva por pasaje: semilla(c, p) = 58300 + 10 c + p (c = cadena 1..9,
p = pasaje 0..9; practica c = 0 -> 58300-58309). Al terminar el pasaje, la SIEMBRA del siguiente = los genomas (g, b) de los cuerpos
VIVOS muestreados cada 1000 pasos en los ultimos 5 000 pasos, en los 9 linajes (una entrada por muestra: el que vive mas aparece mas;
es seleccion por viabilidad, SIN juez: siembra() solo recibe la lista 'vivos_b', ni R0, ni hijos, ni cruza). Los fundadores del pasaje
siguiente (el primero y cada refundacion) toman una entrada al azar de la siembra + la mutacion de siempre.
BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, fundador limpio):
  pas    V143_PAS, transfiere, mutacion del cerebro ECO (p 0.05, sigma 0.15)       CANDIDATO
  ctl    V143_PAS, NO transfiere (cada pasaje: g ~ U[-0.1, 0.1], cerebro G0 mutado)  CONTROL (misma fisica, mismos pasajes)
  pasg   V143_PAS, transfiere, cerebro fijo en G0 (p 0): solo el gen g              secundario
  eco    V143_PAS, transfiere; pasaje 0 sembrado con genomas de ECO (si Opus A los deja; --eco <json>)   secundario
  termo  V143_TERMO (termo/carros) · o1 O1 · v143 V143: referencias por pasaje (misma semilla; sin genes)
En el pasaje 0, pas == ctl bit a bit (misma semilla, siembra None): se comprueba en cada cadena ('p0_pas_eq_ctl').

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN):
  python .../corre_pas.py --humo                                  # 1 proceso, 4 corridas, T 5 000, practica; escribe su JSON
  python .../corre_pas.py --cadena 1 [--npas 10] [--T 25000] [--brazos pas,ctl,pasg,termo,o1]   # 1 proceso, una cadena
  python .../corre_pas.py --lee <carpeta>[,<carpeta>...]          # tabla por pasaje
"""
import argparse, copy, hashlib, importlib.util, json, math, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
TERMOD = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')
for _d in (AQUI, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV          # tarea, med (se IMPORTA, no se toca)
import construye_pas as CB
P = CV.P; J = CV.J

CARROS = os.path.join(AQUI, 'carros')
DATOS = os.path.join(AQUI, 'datos')
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028',
        os.path.join(TERMOD, 'carros', 'V143_TERMO.py'): '3db639cab75641fb',
        os.path.join(RAIZ, 'experimentos', 'organelos', 'termo_banco', 'carros', 'V143_EVO_BAJO.py'): '3187b373654e119f'}
BRAZOS = {'pas': dict(carro='V143_PAS', trans=1, pmut=0.05), 'ctl': dict(carro='V143_PAS', trans=0, pmut=0.05),
          'pasg': dict(carro='V143_PAS', trans=1, pmut=0.0), 'eco': dict(carro='V143_PAS', trans=1, pmut=0.05, eco=1),
          'termo': dict(carro='V143_TERMO'), 'o1': dict(carro='O1'), 'v143': dict(carro='V143')}
PROPIOS = {'V143_PAS': os.path.join(CARROS, 'V143_PAS.py'), 'V143_PAS0': os.path.join(CARROS, 'V143_PAS0.py'),
           'V143_TERMO': os.path.join(TERMOD, 'carros', 'V143_TERMO.py')}
SIGMA_B = 0.15
T_DEF = 25000; NPAS_DEF = 10; VENT = 5000
GENES = CB.GENES


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def semilla(c, p): return 58300 + 10 * c + p


def registra():
    for n, ruta in PROPIOS.items():
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", ruta)
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    return CV._MODS


def tarea(seed, carro, T, siembra=None, pmut=0.05):
    """corre_v143.tarea tal cual (regla 14) + 'tel_ps' (copia de _TEL del carro PAS, solo lectura)."""
    registra()
    m = CV._MODS.get(carro) if carro in ('V143_PAS', 'V143_PAS0') else None
    cap = []; orig = P.run
    if m is not None:
        m.SIEMBRA = copy.deepcopy(siembra); m.PS_SEMILLA = int(seed); m.PS_MUT = (float(pmut), SIGMA_B)

    def run2(*a, **k):
        if m is not None: m._TEL.clear(); m._PS_CNT.clear()
        r = orig(*a, **k)
        cap.append(copy.deepcopy({str(i): v for i, v in m._TEL.items()}) if m is not None else None)
        return r
    P.run = run2
    try:
        x = CV.tarea((seed, carro, T))
    finally:
        P.run = orig
        if m is not None: m.SIEMBRA = None; m.PS_SEMILLA = 0; m.PS_MUT = (0.05, 0.15)
    x['tel_ps'] = cap[0] if cap else None
    return x


def siembra(vivos_b, T, vent=VENT):
    """SOLO de los VIVOS: vivos_b = {indice: [[t, g, b], ...]} -> lista de genomas {'g', 'b'} de las muestras con t >= T - vent.
    No recibe (ni puede leer) R0, hijos, cruza ni nada del juez: la transferencia no usa fitness."""
    out = []
    for i in sorted(vivos_b, key=lambda z: int(z)):
        for t, g, b in vivos_b[i]:
            if t >= T - vent: out.append(dict(g=float(g), b={k: float(v) for k, v in zip(GENES, b)}))
    return out or None


def _q(xs, p):
    xs = sorted(xs); return round(xs[min(len(xs) - 1, int(p * len(xs)))], 4) if xs else None


def g0_fabrica():
    cf = P.cfg_fabrica() if hasattr(P, 'cfg_fabrica') else None
    if cf is None: return None
    return {k: float(cf['NK'] if k == 'NK' else cf['kw'][k]) for k in GENES}


def resumen_pasaje(x, sem_sig, T):
    L = x['linajes']
    r = dict(seed=x['seed'], seg=x.get('seg'), R0_real=[l['R0_real'] for l in L], fund=[l['fundadores'] for l in L],
             fund_post10k=[l['fund_post10k'] for l in L], cruza=[int(l['cruza_real']) for l in L])
    r['R0_med'] = CV.med(r['R0_real']); r['fund_med'] = CV.med(r['fund']); r['cruzan'] = sum(r['cruza'])
    r['mayoria'] = int(r['cruzan'] * 2 > len(L)); r['fund_tot'] = sum(r['fund'])
    tel = x.get('tel_ps')
    if tel:
        fp = [f for v in tel.values() for f in v.get('fund_ps', [])]
        r['fundadores_de_siembra'] = sum(f[0] for f in fp); r['fundadores_n'] = len(fp)
        r['g_fund_media'] = round(sum(f[1] for f in fp) / len(fp), 4) if fp else None
    if sem_sig:
        gs = [s['g'] for s in sem_sig]
        r['siembra_n'] = len(gs); r['g_media'] = round(sum(gs) / len(gs), 4)
        r['g_q'] = [_q(gs, .1), _q(gs, .5), _q(gs, .9)]
        G0 = g0_fabrica()
        if G0: r['b_log_med'] = {k: round(float(st.median([math.log(s['b'][k] / G0[k]) for s in sem_sig])), 3) for k in GENES}
    return r


def cadena(c, brazos, npas, T, dest, log, eco=None):
    """Una cadena: npas pasajes; en cada pasaje corre cada brazo en la misma semilla de pista. Escribe un JSON por pasaje y brazo
    (ERR-54) y la cadena completa al final."""
    sem = {b: None for b in brazos}
    if 'eco' in brazos: sem['eco'] = eco
    filas = []
    for p in range(npas):
        s = semilla(c, p)
        for b in brazos:
            cfg = BRAZOS[b]; t0 = time.time()
            try:
                x = tarea(s, cfg['carro'], T, siembra=(sem.get(b) if cfg.get('trans') else None), pmut=cfg.get('pmut', 0.05))
                ab = None
            except BaseException as e:   # noqa: nube-9
                x = None; ab = f"{type(e).__name__}: {e}"[:300]
            if x is None:
                fila = dict(c=c, p=p, brazo=b, aborto=ab); filas.append(fila); log(f"  c{c} p{p} {b}: ABORTO {ab}"); continue
            sig = siembra({i: v.get('vivos_b', []) for i, v in x['tel_ps'].items()}, T) if x.get('tel_ps') else None
            fila = dict(c=c, p=p, brazo=b, aborto=None, sembrado=int(sem.get(b) is not None and bool(cfg.get('trans'))),
                        **resumen_pasaje(x, sig, T))
            if cfg.get('trans'): sem[b] = sig
            filas.append(fila)
            with open(os.path.join(dest, f"c{c}_p{p}_{b}.json"), 'w', encoding='utf-8') as fh:
                json.dump(dict(fila=fila, siembra_sig=sig), fh, ensure_ascii=False)
            log(f"  [{time.time()-t0:6.1f}s] c{c} p{p} s{s} {b:5s} R0med {fila['R0_med']} cruzan {fila['cruzan']}/9 fund {fila['fund']} "
                f"g_siembra {fila.get('g_media')} {fila.get('g_q')} de_siembra {fila.get('fundadores_de_siembra')}/{fila.get('fundadores_n')}")
    return filas


def tabla(filas, log):
    brazos = sorted({f['brazo'] for f in filas}, key=lambda z: list(BRAZOS).index(z))
    ps = sorted({f['p'] for f in filas})
    log("pasaje | " + " | ".join(f"{b}: R0 med (por cadena) · fundadores por linaje (media de 9 / mediana de 9; mediana de cadenas) · "
                                 f"linajes establecidos = 0 fundadores tras 10k (mediana de cadenas) · g siembra" for b in brazos))
    for p in ps:
        cel = []
        for b in brazos:
            F = [f for f in filas if f['p'] == p and f['brazo'] == b and not f.get('aborto')]
            if not F: cel.append('-'); continue
            r0 = CV.med([f['R0_med'] for f in F]); fu = CV.med([st.mean(f['fund']) for f in F]); my = sum(f['mayoria'] for f in F)
            g = CV.med([f['g_media'] for f in F if f.get('g_media') is not None])
            es = CV.med([sum(1 for z in f['fund_post10k'] if z == 0) for f in F]); fm = CV.med([CV.med(f['fund']) for f in F])
            cel.append(f"R0 {r0} ({'/'.join(str(f['R0_med']) for f in F)}) · fund media {fu} mediana {fm} · estab {es}/9 · g {g}")
        log(f"  p{p} | " + " | ".join(cel))


MURO_SEM = list(range(58391, 58399)) + list(range(58401, 58409))   # prueba del muro EXPLORATORIA (T 100k): 58391-58398 y 58401-58408 (584xx libre al grep 19:15)


def muro(carpeta, semillas, brazos, T, log, eco=None):
    """PRUEBA DEL MURO (EXPLORATORIA): T 100k, la letra del muro por corrida (cruza_real, mayoria = >= 5/9). Los fundadores de 'pas' y
    'pasg' salen de la siembra FIJA del ULTIMO pasaje de su cadena (la que habria sembrado el pasaje siguiente); dentro de la corrida no
    hay transferencia (es un pasaje largo). ctl, termo, o1: como siempre."""
    fil = [f for f in os.listdir(carpeta) if f.endswith('.json') and f.startswith('c') and '_p' in f]
    S = {}
    for b in ('pas', 'pasg', 'eco'):
        ps = sorted(int(f.split('_p')[1].split('_')[0]) for f in fil if f.endswith(f'_{b}.json'))
        if ps:
            d = json.load(open(os.path.join(carpeta, [f for f in fil if f.endswith(f'_p{ps[-1]}_{b}.json')][0]), encoding='utf-8'))
            S[b] = d['siembra_sig']; log(f"  siembra de {b}: pasaje {ps[-1]} de {os.path.basename(carpeta)} · n {len(S[b] or [])} · g medio "
                                           f"{round(sum(z['g'] for z in S[b]) / len(S[b]), 4) if S[b] else None}")
    if eco is not None:
        S['eco'] = eco; log(f"  siembra de eco: genomas ECO de Opus A (--eco) · n {len(eco)} · g medio {round(sum(z['g'] for z in eco) / len(eco), 4)}")
    if 'eco' in brazos and 'eco' not in S: raise SystemExit("--muro con brazo eco: falta --eco <siembra_eco_*.json>")
    filas = []
    dest = os.path.join(carpeta, f"muro_T{T}")
    os.makedirs(dest, exist_ok=True)
    for s in semillas:
        for b in brazos:
            cfg = BRAZOS[b]; t0 = time.time()
            x = tarea(s, cfg['carro'], T, siembra=(S.get(b) if cfg.get('trans') else None), pmut=cfg.get('pmut', 0.05))
            fila = dict(brazo=b, **resumen_pasaje(x, None, T))
            filas.append(fila)
            with open(os.path.join(dest, f"muro_s{s}_{b}.json"), 'w', encoding='utf-8') as fh: json.dump(fila, fh, ensure_ascii=False)
            log(f"  [{time.time()-t0:6.1f}s] MURO s{s} {b:5s} R0med {fila['R0_med']} cruzan {fila['cruzan']}/9 mayoria {fila['mayoria']} "
                f"fund {fila['fund']} de_siembra {fila.get('fundadores_de_siembra')}/{fila.get('fundadores_n')} g_fund {fila.get('g_fund_media')}")
    return filas


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true')
    g.add_argument('--cadena', type=int, default=None)
    g.add_argument('--lee', default=None)
    g.add_argument('--muro', default=None)
    ap.add_argument('--semillas', default=None)
    ap.add_argument('--brazos', default=None)
    ap.add_argument('--npas', type=int, default=None)
    ap.add_argument('--T', type=int, default=None)
    ap.add_argument('--eco', default=None)
    a = ap.parse_args(argv)
    if a.lee:
        filas = []
        for d in a.lee.split(','):
            for fn in sorted(os.listdir(d.strip())):
                if fn.endswith('.json') and fn.startswith('c') and '_p' in fn:
                    filas.append(json.load(open(os.path.join(d.strip(), fn), encoding='utf-8'))['fila'])
        tabla(filas, print); return 0
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha
    for n, bts in CB.todas().items():
        ok &= open(os.path.join(CARROS, n + '.py'), 'rb').read() == bts
    if not ok: raise SystemExit("shas o carros != construye_pas: no se corre")
    eco = json.load(open(a.eco, encoding='utf-8')) if a.eco else None
    if a.muro:
        sem = [int(z) for z in (a.semillas or '').split(',') if z]
        if not sem or not all(z in MURO_SEM for z in sem): raise SystemExit("--muro: --semillas en 58391-58398 o 58401-58408")
        brazos = (a.brazos or 'pas,ctl,pasg,termo,o1').split(','); T = a.T or 100000
        LOGM = open(os.path.join(a.muro, f"muro_{time.strftime('%Y%m%d_%H%M%S')}.log"), 'a', encoding='utf-8')

        def logm(s=''):
            print(s, flush=True); LOGM.write(s + chr(10)); LOGM.flush()
        logm(f"CORRE_PAS --muro {a.muro} · semillas {sem} · brazos {brazos} · T {T} · corre_pas {h16(os.path.abspath(__file__))} · EXPLORATORIO")
        muro(a.muro, sem, brazos, T, logm, eco=eco); return 0
    if a.humo:
        c = 0; npas = a.npas or 2; T = a.T or 5000; brazos = (a.brazos or 'pas,ctl').split(',')
        if npas * len(brazos) > 6 or npas * len(brazos) * T > 200000: raise SystemExit("--humo: <= 6 corridas y <= 200 000 pasos")
    else:
        c = a.cadena; npas = a.npas or NPAS_DEF; T = a.T or T_DEF; brazos = (a.brazos or 'pas,ctl,pasg,termo,o1').split(',')
        if not 1 <= c <= 9: raise SystemExit("--cadena 1..9 (0 es practica)")
    for b in brazos:
        if b not in BRAZOS: raise SystemExit(f"brazo desconocido {b!r}")
    if 'eco' in brazos and not eco: raise SystemExit("brazo eco sin --eco <json>")
    sel = time.strftime('%Y%m%d_%H%M%S')
    dest = os.path.join(DATOS, f"{'humo_' if a.humo else ''}c{c}_T{T}_n{npas}_{sel}"); os.makedirs(dest, exist_ok=True)
    LOGF = open(os.path.join(dest, 'log.txt'), 'a', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    log(f"CORRE_PAS · cadena {c} · T {T} · pasajes {npas} · brazos {brazos} · semillas {semilla(c, 0)}-{semilla(c, npas-1)} · "
        f"python {platform.python_version()} · corre_pas {h16(os.path.abspath(__file__))} · carros "
        f"{ {n: h16(r) for n, r in PROPIOS.items()} } · EXPLORATORIO")
    t0 = time.time()
    filas = cadena(c, brazos, npas, T, dest, log, eco=eco)
    if 'pas' in brazos and 'ctl' in brazos:
        a0 = [f for f in filas if f['p'] == 0 and f['brazo'] in ('pas', 'ctl') and not f.get('aborto')]
        if len(a0) == 2:
            k = ('R0_real', 'fund', 'cruza', 'fund_post10k')
            log(f"  p0_pas_eq_ctl (pasaje 0: pas == ctl en el juez): {all(a0[0][z] == a0[1][z] for z in k)}")
    tabla(filas, log)
    json.dump(dict(filas=filas, T=T, npas=npas, brazos=brazos, c=c, seg=round(time.time() - t0, 1)),
              open(os.path.join(dest, 'cadena.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"Terminado en {time.time()-t0:.1f}s · {dest}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
