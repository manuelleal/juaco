"""corre_regimen.py — SONDA (nada se declara) del "otro regimen" que dejo la seleccion de perillas: (GW ~0.01, GV ~0.19) cruza igual que el
diseno (1, 1) pero deja el mundo A+C en 4.3 (diseno 7.2), muerde mas, se refunda mas y viaja menos. 1-oct-2026, biotecnologo.
Carpeta propia: experimentos/organelos/escalera/regimen/. NO edita nada de perillas/ ni de escalera/: importa corre_perillas por sha.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE CORRE (cada corrida ES corre_perillas.tarea = corre_v143.tarea con el mundo de P1; carro O1_LUGAR_GEN sha fijado; UN proceso):
  --rejilla --semilla A|B : 6 genomas FIJOS (sin mutacion, sin camara, monomorfico, T 100k): (GW, GV) en
                            (0, 0.2) (1, 0.2) (0, 1) (1, 1) (0.2, 0.2) (0, 0). Es exactamente la 'prueba' del runner de perillas
                            (corre_perillas.trabajo tipo 'fijo'). Semilla A 743801, B 743802 (NUEVAS, grep 1-oct).
  --mixta                 : pista MIXTA: SIEMBRA de DOS genomas ('seleccion' (0, 0.2) y 'diseno' (1, 1)), sin mutacion y sin camara:
                            cada fundador (los 9 primeros y cada refundacion) toma UNO de los dos al azar (50/50, azar propio del carro).
                            La moneda es la de la camara (persistir = refundarse menos) con fuente neutra: quien se establece cuando
                            comparten la comida. Dos paridades = el orden de la lista invertido (mismos sorteos -> asignaciones espejo).
                            Semillas 743811, 743812 x 2 paridades = 4 corridas.
  --identidad             : arnes (reutiliza corre_perillas.identidad_corta): (1,1) == O1_LUGAR y (0,0) == O1 bit a bit; mi envoltura
                            fija == la de perillas; mixta [g, g] == fija g; mixta [fab, o1] != fab; contabilidad por genoma.
  --humo                  : T 3 000, un punto de la rejilla + una mixta, escribe JSON (semilla 743890).
  --lee <carpeta>         : tablas.
REGLA DE CPU (PC compartido, tope 6): antes de correr cuenta los python.exe OCUPADOS (CPU que crece en 3 s) ajenos a este proceso;
con >= 6 NO corre (sale con mensaje). Un solo proceso; <= 6 corridas y <= 200k pasos por proceso.
"""
import argparse, glob, hashlib, json, os, platform, statistics as st, subprocess, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI); PER = os.path.join(ESC, 'perillas')
for _d in (PER, ESC):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_perillas as R   # por sha (abajo); NO se toca

SHA_RUNNER_PER = 'f98b98527155f029'   # perillas/corre_perillas.py (el de la serie)
SHA_CARRO = 'ecc996d2fecccc30'        # perillas/carros/O1_LUGAR_GEN.py
DATOS = os.path.join(AQUI, 'datos')
REJILLA = ['0:0.2', '1:0.2', '0:1', '1:1', '0.2:0.2', '0:0']
G_SEL = dict(GW=0.0, GV=0.2); G_FAB = dict(R.DISENO); G_O1 = dict(R.BASE)
SEM = dict(rejilla=(0, 743801), mixta=(0, 743811), humo=(0, 743890), identidad=743895)   # NUEVAS 7438xx (grep 1-oct en .py/.md/.txt/.log: no aparecen)
T_FIJO = 100000; T_HUMO = 3000; MAX_CORR = 6; MAX_PASOS = 200000; TOPE_CPU = 6


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None


# ------------------------------------------------------------------ regla de CPU
def python_ocupados(ventana=3.0):
    """python.exe ajenos a este proceso cuya CPU crece en la ventana (los de trabajo). None si no se puede medir (entonces NO se corre)."""
    cmd = ['powershell', '-NoProfile', '-Command', "Get-Process python -ErrorAction SilentlyContinue | ForEach-Object { \"$($_.Id) $($_.CPU)\" }"]
    def lee():
        try: out = subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout
        except Exception: return None
        d = {}
        for ln in out.splitlines():
            z = ln.split()
            if len(z) == 2:
                try: d[int(z[0])] = float(z[1].replace(',', '.'))
                except ValueError: pass
        return d
    a = lee(); time.sleep(ventana); b = lee()
    if a is None or b is None: return None, {}
    yo = os.getpid()
    oc = {p: round(b[p] - a[p], 2) for p in b if p != yo and p in a and b[p] - a[p] > 0.5}
    return len(oc), oc


def guarda_cpu(log):
    n, oc = python_ocupados()
    log(f"  CPU: python.exe ocupados ajenos = {n} {oc} (tope {TOPE_CPU})")
    if n is None or n >= TOPE_CPU: log("  NO SE CORRE: hay 6 o mas procesos python de trabajo (o no se pudo medir). Esperar."); return False
    return True


# ------------------------------------------------------------------ corridas
def genoma(s): return dict(zip(R.GENES, [float(z) for z in s.split(':')]))


def mixta(seed, T, orden):
    """SIEMBRA de dos genomas, sigma 0, delta 0, camara 0, genes leidos: cada fundador toma uno al azar (50/50). Contabilidad por genoma."""
    sie = [dict(g) for g in orden]
    y = R.tarea(seed, T, siembra=sie, sigma=0.0, lee=1, delta=0.0, camara=0)
    f = R.fila(y, T); tel = y['tel_ps']; L = y['linajes']
    nom = {tuple(float(g[k]) for k in R.GENES): ('sel' if g == G_SEL else 'fab' if g == G_FAB else 'o1' if g == G_O1 else 'otro') for g in sie}
    def quien(genes): return nom.get(tuple(float(z) for z in genes), 'ajeno')
    por = {}
    for i in sorted(tel, key=int):
        v = tel[i] or {}
        fu = [quien(q[1]) for q in v.get('fund', [])]; vi = [quien(q[1]) for q in v.get('vivos', [])]
        fin = vi[-1] if vi else None
        li = L[int(i)]
        por[int(i)] = dict(fund=fu.count('sel'), fund_fab=fu.count('fab'), fund_n=len(fu), ocup_sel=round(vi.count('sel') / max(1, len(vi)), 3), n_muestras=len(vi),
                           final=fin, primero=(fu[0] if fu else None), cruza=int(li['cruza_real']), fund_post10k=li['fund_post10k'], R0=li['R0_real'],
                           ajenos=fu.count('ajeno') + vi.count('ajeno'), oasis_pasos=(li.get('_oasis') or {}).get('pasos_dentro'))
    res = {}
    for g in ('sel', 'fab'):
        res[g] = dict(fund=sum(p['fund'] if g == 'sel' else p['fund_fab'] for p in por.values()),
                      ocup=round(sum((p['ocup_sel'] if g == 'sel' else 1 - p['ocup_sel']) * p['n_muestras'] for p in por.values()) / max(1, sum(p['n_muestras'] for p in por.values())), 3),
                      finales=sum(p['final'] == g for p in por.values()), primeros=sum(p['primero'] == g for p in por.values()),
                      cruzan_final=sum(p['cruza'] for p in por.values() if p['final'] == g),
                      establecidos_final=sum(int(p['fund_post10k'] == 0 and p['final'] == g) for p in por.values()))
    f.update(tipo='mixta', orden=[('sel' if g == G_SEL else 'fab' if g == G_FAB else str(g)) for g in sie], siembra=sie, por_linaje=por, por_genoma=res,
             ajenos=sum(p['ajenos'] for p in por.values()))
    return f


def corre_mixta(seed, T, orden, carpeta, etiqueta, reanuda):
    fin = os.path.join(carpeta, f"mixta_{etiqueta}.json")
    if reanuda and os.path.exists(fin):
        x = json.load(open(fin, encoding='utf-8'))
        if not x.get('aborto'): return x
    t0 = time.time()
    try: x = dict(aborto=None, **mixta(seed, T, orden))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo='mixta', aborto=f"{type(e).__name__}: {e}"[:300], seed=seed)
    x['seg'] = round(time.time() - t0, 1); x['etiqueta'] = etiqueta
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


def fmt_fijo(x):
    oz = x.get('oasis') or {}
    return (f"  fijo {x['brazo']:8s} s{x.get('seed')} ({x.get('seg')}s) aborto {x['aborto']} · cruzan {x.get('cruzan')}/9 R0 {x.get('R0_med')} · mundo AC {x.get('mundo_AC')} · "
            f"mord AC {x.get('mord_AC')} (dentro {oz.get('mord_AC_dentro')} fuera {oz.get('mord_AC_fuera')}) BD {x.get('mord_BD')} · ratio pasos {oz.get('ratio_pasos')} · "
            f"viajes {(x.get('lugar') or {}).get('viajes')} · fund {sum(x.get('fund') or [])} · nac {sum(z or 0 for z in (x.get('nac_reales') or []))} · vida {x.get('vida_med')} · est {sum(int(z == 0) for z in (x.get('fund_post10k') or []))}")


def fmt_mixta(x):
    if x.get('aborto'): return f"  mixta {x.get('etiqueta')} ABORTO {x['aborto']}"
    g = x['por_genoma']; oz = x.get('oasis') or {}
    return (f"  mixta {x['etiqueta']} s{x['seed']} orden {x['orden']} ({x['seg']}s) · cruzan {x['cruzan']}/9 R0 {x['R0_med']} · mundo AC {x['mundo_AC']} · mord AC {x['mord_AC']} BD {x['mord_BD']} · ratio {oz.get('ratio_pasos')} · "
            f"sel: fund {g['sel']['fund']} ocup {g['sel']['ocup']} finales {g['sel']['finales']} est {g['sel']['establecidos_final']} cruzan {g['sel']['cruzan_final']} · "
            f"fab: fund {g['fab']['fund']} ocup {g['fab']['ocup']} finales {g['fab']['finales']} est {g['fab']['establecidos_final']} cruzan {g['fab']['cruzan_final']} · primeros sel/fab {g['sel']['primeros']}/{g['fab']['primeros']} · ajenos {x['ajenos']}")


# ------------------------------------------------------------------ arnes
def identidad(log):
    ok = True
    def chk(nombre, c):
        nonlocal ok; ok &= bool(c); log(f"  {'OK   ' if c else 'FALLA'} {nombre}")
    chk(f"sha corre_perillas.py == {SHA_RUNNER_PER}", h16(os.path.join(PER, 'corre_perillas.py')) == SHA_RUNNER_PER)
    chk(f"sha carros/O1_LUGAR_GEN.py == {SHA_CARRO}", h16(R.CARROS[R.CARRO]) == SHA_CARRO)
    chk("corre_perillas.verifica (shas de escalera, carros == construye_perillas)", R.verifica(lambda s: None))
    chk("corre_perillas.identidad_corta: GEN (1,1) == O1_LUGAR · GEN (0,0) == O1 · neutro == O1 · control", R.identidad_corta(log, seed=SEM['identidad'], T=1500))
    m = R.CV._MODS[R.CARRO]; lug = R.CV._MODS['O1_LUGAR']; o1 = R.CV.modulo('O1'); W = R.MUNDO; S = SEM['identidad']; T = 1500
    rl = R._run(lug, S, T, **W); ro = R._run(o1, S, T, **W)
    # mi envoltura fija = corre_perillas.trabajo('fijo'); aqui se comprueba que el camino (siembra [g], sigma 0, delta 0, camara 0, lee 1) da O1_LUGAR / O1
    chk("envoltura FIJA (1:1) [siembra [g], sigma 0, delta 0, camara 0, lee 1] == O1_LUGAR bit a bit (salida ENTERA)", R._con(m, [genoma('1:1')], 0.0, 1, S, T, camara=0, **W) == rl)
    chk("envoltura FIJA (0:0) == O1 bit a bit (salvo telemetria 'lugar')", R.CO.sin_tel(R._con(m, [genoma('0:0')], 0.0, 1, S, T, camara=0, **W)) == ro)
    chk("envoltura FIJA (0:0.2) != O1 y != O1_LUGAR (control)", R.CO.sin_tel(R._con(m, [genoma('0:0.2')], 0.0, 1, S, T, camara=0, **W)) != ro and R._con(m, [genoma('0:0.2')], 0.0, 1, S, T, camara=0, **W) != rl)
    chk("MIXTA [fab, fab] == O1_LUGAR bit a bit (la lista de dos iguales no cambia nada)", R._con(m, [dict(G_FAB), dict(G_FAB)], 0.0, 1, S, T, camara=0, **W) == rl)
    chk("MIXTA [o1, o1] == O1 bit a bit (salvo telemetria)", R.CO.sin_tel(R._con(m, [dict(G_O1), dict(G_O1)], 0.0, 1, S, T, camara=0, **W)) == ro)
    # control a T 6000: a T 1500 la mixta [fab, o1] AUN es == O1_LUGAR (el modulo actua poco y tarde; PREREGISTRO_perillas sec. 11.1), no es cableado
    T2 = 6000; rl2 = R._run(lug, S, T2, **W); ro2 = R._run(o1, S, T2, **W); X2 = R._con(m, [dict(G_FAB), dict(G_O1)], 0.0, 1, S, T2, camara=0, **W)
    chk(f"MIXTA [fab, o1] != O1_LUGAR y != O1 (control, T {T2}; a T 1500 aun coincide con O1_LUGAR: el modulo actua tarde)", X2 != rl2 and R.CO.sin_tel(X2) != ro2)
    chk(f"MIXTA [fab, fab] == O1_LUGAR tambien a T {T2}", R._con(m, [dict(G_FAB), dict(G_FAB)], 0.0, 1, S, T2, camara=0, **W) == rl2)
    a = mixta(S, 4000, [G_SEL, G_FAB]); b = mixta(S, 4000, [G_FAB, G_SEL]); g = a['por_genoma']
    chk(f"MIXTA contabilidad (T 4000): fundadores sel + fab == fund_n ({g['sel']['fund']} + {g['fab']['fund']} == {a['fund_n']}), ajenos 0, los dos presentes, 9 primeros",
        g['sel']['fund'] + g['fab']['fund'] == a['fund_n'] and a['ajenos'] == 0 and g['sel']['fund'] > 0 and g['fab']['fund'] > 0 and g['sel']['primeros'] + g['fab']['primeros'] == 9)
    chk(f"MIXTA paridad: el orden invertido da la asignacion ESPEJO de los 9 primeros (sel {g['sel']['primeros']} <-> fab {b['por_genoma']['sel']['primeros']}) y el mundo es el mismo (oasis z0)",
        g['sel']['primeros'] == b['por_genoma']['fab']['primeros'] and g['fab']['primeros'] == b['por_genoma']['sel']['primeros'] and a['oasis']['z0'] == b['oasis']['z0'])
    chk("MIXTA estado: sigma 0, delta 0, camara 0, lee 1, siembra_n 2, carro O1_LUGAR_GEN, mundo de P1",
        a['estado']['sigma'] == 0.0 and a['estado']['delta'] == 0.0 and a['estado']['camara'] == 0 and a['estado']['lee'] == 1 and a['estado']['siembra_n'] == 2 and a['estado']['carro'] == R.CARRO and a['estado']['mundo'] == R.MUNDO)
    return ok


# ------------------------------------------------------------------ lectura
def lee(carpeta, log):
    F = [json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob(os.path.join(carpeta, 'fijo_i*_*.json')))]
    M = [json.load(open(f, encoding='utf-8')) for f in sorted(glob.glob(os.path.join(carpeta, 'mixta_*.json')))]
    if F:
        log(f"  REJILLA (genomas fijos, monomorficos) en {os.path.relpath(carpeta, AQUI)}")
        log(f"  {'genoma':9s}{'seed':>8s}{'cruz':>5s}{'R0':>7s}{'AC':>6s}{'mAC':>6s}{'mBD':>6s}{'mACin':>6s}{'mACout':>7s}{'ratio':>7s}{'viajes':>8s}{'fund':>5s}{'nac':>5s}{'vida':>6s}{'est':>4s}{'AC_pred':>8s}")
        for x in sorted(F, key=lambda x: (x['brazo'], x.get('seed') or 0)):
            if x.get('aborto'): log(f"  {x['brazo']} ABORTO {x['aborto']}"); continue
            oz = x['oasis']; O = 0.003 * 9 * x['T']; pred = 18 * (x['mord_BD'] - x['mord_AC'] + O) / O
            log(f"  {x['brazo']:9s}{x['seed']:8d}{x['cruzan']:5d}{x['R0_med']:7.3f}{x['mundo_AC']:6.2f}{x['mord_AC']:6d}{x['mord_BD']:6d}{oz['mord_AC_dentro']:6d}{oz['mord_AC_fuera']:7d}{oz['ratio_pasos']:7.2f}{x['lugar']['viajes']:8d}{sum(x['fund']):5d}{sum(x['nac_reales']):5d}{x['vida_med']:6.0f}{sum(int(z == 0) for z in x['fund_post10k']):4d}{pred:8.2f}")
    for x in M: log(fmt_mixta(x))
    if M and all(not x.get('aborto') for x in M):
        s = {g: dict(fund=sum(x['por_genoma'][g]['fund'] for x in M), ocup=round(st.mean(x['por_genoma'][g]['ocup'] for x in M), 3), finales=sum(x['por_genoma'][g]['finales'] for x in M),
                     est=sum(x['por_genoma'][g]['establecidos_final'] for x in M), cruzan=sum(x['por_genoma'][g]['cruzan_final'] for x in M), primeros=sum(x['por_genoma'][g]['primeros'] for x in M)) for g in ('sel', 'fab')}
        log(f"  MIXTA suma de {len(M)} corridas: {s} · mundo AC mediana {med([x['mundo_AC'] for x in M])} · cruzan {[x['cruzan'] for x in M]}")
    return F, M


# ------------------------------------------------------------------ main
def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--identidad', action='store_true'); g.add_argument('--humo', action='store_true')
    g.add_argument('--rejilla', action='store_true'); g.add_argument('--mixta', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--semilla', default=None, choices=['A', 'B']); ap.add_argument('--reanuda', action='store_true'); ap.add_argument('--T', type=int, default=None)
    a = ap.parse_args(argv)
    def log(s=''): print(f"[{time.strftime('%H:%M:%S')}] {s}", flush=True)
    if a.lee: lee(os.path.abspath(a.lee), log); return 0
    log(f"CORRE_REGIMEN · python {platform.python_version()} · corre_regimen.py {h16(os.path.abspath(__file__))} · corre_perillas.py {h16(os.path.join(PER, 'corre_perillas.py'))} · carro {h16(R.CARROS[R.CARRO])} · mundo {R.MUNDO}")
    if a.identidad:
        ok = identidad(log); log(f"ARNES REGIMEN: {'PASA' if ok else 'FALLA'}"); return 0 if ok else 1
    if not (R.verifica(lambda s: None) and R.identidad_corta(log, seed=SEM['identidad'], T=1500)): log("  ALGO FALLA en el arnes corto -> no se corre"); return 1
    if not guarda_cpu(log): return 2
    if a.humo:
        T = T_HUMO; carpeta = os.path.join(DATOS, 'humo'); os.makedirs(carpeta, exist_ok=True); base = SEM['humo']
        x = R.trabajo(('fijo', 0, '0:0.2', base, 0, 0, T, carpeta, a.reanuda)); log(fmt_fijo(x))
        y = corre_mixta(base[1], T, [G_SEL, G_FAB], carpeta, f"s{base[1]}_selfab", a.reanuda); log(fmt_mixta(y))
        log(f"HUMO (no cuenta): JSON en {os.path.relpath(carpeta, AQUI)} · abortos {int(bool(x.get('aborto'))) + int(bool(y.get('aborto')))}"); return 0
    T = a.T or T_FIJO
    if T > MAX_PASOS: raise SystemExit(f"T {T} > {MAX_PASOS}")
    if a.rejilla:
        if not a.semilla: raise SystemExit("--rejilla exige --semilla A|B (6 corridas por proceso)")
        i = 0 if a.semilla == 'A' else 1; base = SEM['rejilla']; carpeta = os.path.join(DATOS, f"rejilla_T{T}"); os.makedirs(carpeta, exist_ok=True)
        log(f"  REJILLA semilla {a.semilla} = {R.sem_pru(base, i)} · T {T} · genomas {REJILLA} · 6 corridas, un proceso")
        for s in REJILLA:
            x = R.trabajo(('fijo', i, s, base, 0, 0, T, carpeta, a.reanuda)); log(fmt_fijo(x))
        lee(carpeta, log); return 0
    if a.mixta:
        base = SEM['mixta']; carpeta = os.path.join(DATOS, f"mixta_T{T}"); os.makedirs(carpeta, exist_ok=True)
        log(f"  MIXTA semillas {base[1]}, {base[1] + 1} x 2 paridades · T {T} · sel {G_SEL} fab {G_FAB} · 4 corridas, un proceso")
        for j in (0, 1):
            seed = base[1] + j
            for orden, et in (([G_SEL, G_FAB], 'selfab'), ([G_FAB, G_SEL], 'fabsel')):
                x = corre_mixta(seed, T, orden, carpeta, f"s{seed}_{et}", a.reanuda); log(fmt_mixta(x))
        lee(carpeta, log); return 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
