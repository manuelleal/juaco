"""corre_examen.py — EXAMEN del bloque MURO MINIMO (PREREGISTRO.md). 5 brazos x N semillas, T 100 000, fundador NO limpio (ERR-191),
corre_carro.py copiado del examen grande (pista y juez sin tocar). Reanudable: salta los JSON que ya existen. Imprime la letra.
Log y resumen.json se escriben DESDE EL ARRANQUE y tras cada corrida.

Uso (SOLO el coordinador usa --pool > 1):
  python -B corre_examen.py --desde 283001 --n 20 --pool 3      (serie)
  python -B corre_examen.py --desde 283021 --n 20 --pool 3      (replica)
  python -B corre_examen.py --humo --desde 276001 --n 1 --brazos MINIMO [--T 100000]     (humo de UN proceso; nunca semillas selladas)
"""
import argparse, hashlib, json, os, statistics as st, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("JUACO_OE_SEM", "0,0,0")
sys.path.insert(0, AQUI)
import construye as C
import evaluador as EV

PROG = os.path.join(AQUI, "programas")
BRAZOS = ["MINIMO", "HUMO", "KO_PIZARRA", "O1", "O1_SINLIMPIA"]
SHAS = {"MINIMO": "b9cfbb3bb7cb", "HUMO": "69fcfcb2473f", "KO_PIZARRA": "965aaec1e366", "O1_SINLIMPIA": "50b2fc3241da"}   # sha12 texto LF
SHA_O1 = "99436afa2715f028"
SELLADAS = range(283001, 283041); VALIDAS = (283001, 283021); N_LETRA = 20
MAY = 5            # semilla "con mayoria": cruzan_real >= 5 de 9
P1_MIN = 15        # MINIMO con mayoria en >= 15/20
P2_FRAC = 0.85     # linajes que cruzan MINIMO >= 0.85 x los de HUMO
MOD_MIN = 10       # MODESTO: MINIMO con mayoria en >= 10/20
C1_MAX = 3         # control: O1_SINLIMPIA con mayoria en <= 3/20
V3_MIN = 6         # cordura: O1 con mayoria en >= 6/20
V4_MIN = 15        # cordura: HUMO con mayoria en >= 15/20
CAMPOS = ("persisten", "cruzan_real", "R0_real_med", "vida_med", "fund_post10k", "muertes", "nac_reales", "mordidas_malas",
          "frac_sin_bueno_mundo", "escrituras", "seg")


def ruta(nom):
    return "O1" if nom == "O1" else os.path.join(PROG, nom + ".py")


def una(a):
    nom, seed, T, dest = a
    sal = os.path.join(dest, f"{nom}_s{seed}_T{T}.json")
    if not os.path.exists(sal):
        r = subprocess.run([sys.executable, "-B", os.path.join(AQUI, "corre_carro.py"), ruta(nom), str(seed), str(T), sal],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=AQUI)
        if r.returncode != 0: return nom, seed, None, r.stderr[-800:]
    return nom, seed, json.load(open(sal, encoding="utf-8")), None


def letra(R, semillas, brazos):
    """La letra de PREREGISTRO.md §4. Si falta algun brazo o corrida, V1 cae y el veredicto es NO SE LEE."""
    c = {k: d["cruzan_real"] for k, d in R.items()}
    tiene = {n: [s for s in semillas if (n, s) in c] for n in brazos}
    may = {n: sum(c[(n, s)] >= MAY for s in tiene[n]) for n in brazos}
    suma = {n: sum(c[(n, s)] for s in tiene[n]) for n in brazos}
    med = {n: {x: (round(float(st.median([R[(n, s)][x] for s in tiene[n]])), 4) if tiene[n] else None)
               for x in ("R0_real_med", "vida_med", "mordidas_malas", "frac_sin_bueno_mundo", "fund_post10k")} for n in brazos}
    out = dict(mayoria=may, suma_cruzan=suma, medianas=med, n_semillas=len(semillas))
    completa = set(brazos) == set(BRAZOS) and len(semillas) == N_LETRA and len(R) == len(BRAZOS) * len(semillas)
    if not completa:
        out.update(validez=dict(V1_completa=False), veredicto="NO SE LEE"); return out
    par = lambda a, b: dict(gana=sum(c[(a, s)] > c[(b, s)] for s in semillas), pierde=sum(c[(a, s)] < c[(b, s)] for s in semillas))
    v = dict(V1_completa=True, V2_shas_y_filtro=True, V3_O1_cordura=may["O1"] >= V3_MIN, V4_HUMO_cruza=may["HUMO"] >= V4_MIN)
    ctrl = dict(C1_sin_limpieza_falla=may["O1_SINLIMPIA"] <= C1_MAX)
    frac = suma["MINIMO"] / suma["HUMO"] if suma["HUMO"] else 0.0
    fracb = suma["MINIMO"] / suma["KO_PIZARRA"] if suma["KO_PIZARRA"] else 0.0
    p = dict(P1_MINIMO_mayoria=may["MINIMO"] >= P1_MIN, P2_linajes_vs_HUMO=frac >= P2_FRAC)
    if not all(v.values()) or not ctrl["C1_sin_limpieza_falla"]: ver = "NO SE LEE"
    elif all(p.values()): ver = "FUNCIONA"
    elif may["MINIMO"] >= MOD_MIN: ver = "HAY ALGO MODESTO"
    else: ver = "NO"
    out.update(validez=v, control=ctrl, puertas=p, frac_linajes_MINIMO_sobre_HUMO=round(frac, 4),
               descriptivo=dict(P2b_frac_linajes_MINIMO_sobre_KO_PIZARRA=round(fracb, 4), MINIMO_vs_HUMO=par("MINIMO", "HUMO"),
                                MINIMO_vs_KO_PIZARRA=par("MINIMO", "KO_PIZARRA"), MINIMO_vs_O1=par("MINIMO", "O1")), veredicto=ver)
    return out


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument("--desde", type=int, required=True); ap.add_argument("--n", type=int, default=N_LETRA)
    ap.add_argument("--pool", type=int, default=1); ap.add_argument("--humo", action="store_true")
    ap.add_argument("--brazos", default=",".join(BRAZOS)); ap.add_argument("--T", type=int, default=100000)
    a = ap.parse_args()
    semillas = list(range(a.desde, a.desde + a.n)); brazos = a.brazos.split(",")
    if any(b not in BRAZOS for b in brazos): raise SystemExit(f"--brazos: solo {BRAZOS}")
    if a.humo:
        if any(s in SELLADAS for s in semillas): raise SystemExit("--humo no puede tocar las semillas selladas 283001-283040")
        if a.pool != 1: raise SystemExit("--humo es de UN proceso (--pool 1)")
        dest = os.path.join(AQUI, "humo", f"s{semillas[0]}-{semillas[-1]}_T{a.T}")
    else:
        if a.desde not in VALIDAS or a.n != N_LETRA or a.T != 100000 or brazos != BRAZOS:
            raise SystemExit(f"sin --humo: --desde debe ser una de {VALIDAS}, --n {N_LETRA}, T 100000 y los 5 brazos (preregistro)")
        dest = os.path.join(AQUI, "examen", f"s{semillas[0]}-{semillas[-1]}")
    os.makedirs(dest, exist_ok=True)
    LOG = os.path.join(dest, "log.txt")

    def di(s=""):
        print(s, flush=True)
        with open(LOG, "a", encoding="utf-8") as fh: fh.write(s + "\n")
    di(f"MURO MINIMO {'HUMO-DE-RUNNER' if a.humo else 'EXAMEN'} {time.strftime('%Y-%m-%d %H:%M:%S')} - semillas {semillas[0]}-{semillas[-1]} - T {a.T} - "
       f"fundador no limpio - pool {a.pool} - brazos {brazos} - corre_examen.py {hashlib.sha256(open(__file__, 'rb').read()).hexdigest()[:16]}")
    if C.main(True): raise SystemExit("construye.py --check: el instrumento no es igual a su origen: no se corre")
    for n, sh in SHAS.items():
        src = C.lf(os.path.join(PROG, n + ".py")); s2 = C.s16(src)[:12]; v = EV._revisa(src)
        di(f"  {n}: sha {s2} - filtro {'PASA' if not v else v[:2]}")
        if s2 != sh or v: raise SystemExit(f"{n}: sha o filtro no coinciden con el preregistro: no se corre")
    so = hashlib.sha256(open(os.path.join(EV.PISTA, "carros", "O1.py"), "rb").read()).hexdigest()[:16]
    di(f"  O1: sha {so}")
    if so != SHA_O1: raise SystemExit("O1: sha no coincide con el preregistro: no se corre")
    t0 = time.time(); R = {}
    tareas = [(n, s, a.T, dest) for s in semillas for n in brazos]

    def guarda(fin=False):
        L = letra(R, semillas, brazos)
        with open(os.path.join(dest, "resumen.json"), "w", encoding="utf-8") as fh:
            json.dump(dict(terminado=fin, hechas=len(R), total=len(tareas), T=a.T, humo=a.humo, semillas=semillas, brazos=brazos, letra=L,
                           por_semilla={f"{k[0]}_{k[1]}": {x: d[x] for x in CAMPOS} for k, d in sorted(R.items())}), fh, indent=1, ensure_ascii=False)
        return L

    def anota(nom, seed, d, err):
        if d is None: di(f"  FALLA {nom} s{seed}: {err}"); return
        R[(nom, seed)] = d
        di(f"  [{time.strftime('%H:%M:%S')} {time.time() - t0:6.0f}s {len(R):3d}/{len(tareas)}] {nom:12s} s{seed} persisten {d['persisten']}/9 cruzan {d['cruzan_real']}/9 "
           f"R0 med {d['R0_real_med']:.4f} vida med {d['vida_med']:8.1f} fund>10k {d['fund_post10k']:3d} muertes {d['muertes']:4d} "
           f"nac {d['nac_reales']:4d} mord malas {d['mordidas_malas']:5d} sin nada bueno {d['frac_sin_bueno_mundo']:.3f} ({d['seg']} s)")
        guarda()
    guarda()
    if a.pool == 1:
        for x in tareas: anota(*una(x))
    else:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for res in PL.imap_unordered(una, tareas): anota(*res)
    L = guarda(fin=True)
    di("\nPOR SEMILLA (cruzan): " + " | ".join(f"{s}: " + " ".join(f"{n}={R[(n, s)]['cruzan_real']}" for n in brazos if (n, s) in R) for s in semillas))
    di(f"LETRA: {json.dumps(L, ensure_ascii=False)}")
    di(f"VEREDICTO DE LA TANDA: {L['veredicto']}{'  (humo: no es veredicto)' if a.humo else ''}   ({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
