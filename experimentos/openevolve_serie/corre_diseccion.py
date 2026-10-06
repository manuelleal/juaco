"""corre_diseccion.py — DISECCION de HUMO (PREREGISTRO_diseccion.md): HUMO y sus 4 ablaciones (KO_RECICLA, KO_BANCO, KO_CAP,
KO_PIZARRA), 10 semillas por tanda, T 100 000, fundador NO limpio, corre_carro.py (pista y juez sin tocar), Pool 3. Reanudable.

Uso:  python -B corre_diseccion.py --desde 277001     (serie)
      python -B corre_diseccion.py --desde 277011     (replica)
"""
import argparse, hashlib, json, os, subprocess, sys, time
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("JUACO_OE_SEM", "0,0,0")
sys.path.insert(0, AQUI)
import evaluador as EV

T = 100000; N = 10; MAY = 5
PROG = os.path.join(AQUI, "diseccion", "programas")
SHAS = {"HUMO": "69fcfcb2473f", "KO_RECICLA": "46d85155fe5d", "KO_BANCO": "1ea29d0db707", "KO_CAP": "c8cb69d88184",
        "KO_PIZARRA": "965aaec1e366"}
KOS = ["KO_RECICLA", "KO_BANCO", "KO_CAP", "KO_PIZARRA"]
VALIDAS = (277001, 277011)
NEC_MAX = 5       # NECESARIA: el KO tiene mayoria en <= 5/10
CONTRIB_MIN = 7   # CONTRIBUYE: el KO cruza MENOS linajes que HUMO en >= 7/10 (empates no cuentan)
V_HUMO = 8        # validez: HUMO con mayoria en >= 8/10


def una(a):
    nom, seed, dest = a
    sal = os.path.join(dest, f"{nom}_s{seed}_T{T}.json")
    if not os.path.exists(sal):
        r = subprocess.run([sys.executable, "-B", os.path.join(AQUI, "corre_carro.py"), os.path.join(PROG, nom + ".py"), str(seed), str(T), sal],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=AQUI)
        if r.returncode != 0: return nom, seed, None, r.stderr[-800:]
    return nom, seed, json.load(open(sal, encoding="utf-8")), None


def letra(R, semillas):
    c = {(n, s): R[(n, s)]["cruzan_real"] for (n, s) in R}
    may = {n: sum(c[(n, s)] >= MAY for s in semillas) for n in SHAS}
    out = dict(validez=dict(V1_completa=len(R) == len(SHAS) * len(semillas), V2_HUMO_cruza=may["HUMO"] >= V_HUMO), mayoria=may,
               suma={n: sum(c[(n, s)] for s in semillas) for n in SHAS}, piezas={})
    for k in KOS:
        pierde = sum(c[(k, s)] < c[("HUMO", s)] for s in semillas); gana = sum(c[(k, s)] > c[("HUMO", s)] for s in semillas)
        if may[k] <= NEC_MAX: cl = "NECESARIA"
        elif pierde >= CONTRIB_MIN: cl = "CONTRIBUYE"
        else: cl = "SOBRA"
        out["piezas"][k] = dict(clase=cl, mayoria=may[k], KO_pierde_vs_HUMO=pierde, KO_gana_vs_HUMO=gana)
    out["valida"] = all(out["validez"].values())
    return out


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument("--desde", type=int, required=True)
    a = ap.parse_args()
    if a.desde not in VALIDAS: raise SystemExit(f"--desde debe ser una de {VALIDAS} (preregistro)")
    semillas = list(range(a.desde, a.desde + N))
    dest = os.path.join(AQUI, "diseccion", f"s{semillas[0]}-{semillas[-1]}"); os.makedirs(dest, exist_ok=True)
    LOG = os.path.join(dest, "log.txt")

    def di(s=""):
        print(s, flush=True)
        with open(LOG, "a", encoding="utf-8") as fh: fh.write(s + "\n")
    di(f"DISECCION {time.strftime('%Y-%m-%d %H:%M:%S')} - semillas {semillas[0]}-{semillas[-1]} - T {T} - fundador no limpio - "
       f"corre_diseccion.py {hashlib.sha256(open(__file__, 'rb').read()).hexdigest()[:16]}")
    for n, sh in SHAS.items():
        src = open(os.path.join(PROG, n + ".py"), encoding="utf-8").read(); s2 = hashlib.sha256(src.encode("utf-8")).hexdigest()[:12]; v = EV._revisa(src)
        di(f"  {n}: sha {s2} - filtro {'PASA' if not v else v[:2]}")
        if s2 != sh or v: raise SystemExit(f"{n}: sha o filtro no coinciden con el preregistro: no se corre")
    t0 = time.time(); R = {}
    with Pool(3) as PL:
        for nom, seed, d, err in PL.imap_unordered(una, [(n, s, dest) for s in semillas for n in SHAS]):
            if d is None: di(f"  FALLA {nom} s{seed}: {err}"); continue
            R[(nom, seed)] = d
            di(f"  [{time.time() - t0:6.0f}s] {nom:10s} s{seed} persisten {d['persisten']}/9 cruzan {d['cruzan_real']}/9 R0 med {d['R0_real_med']:.4f} "
               f"vida med {d['vida_med']:7.1f} fund>10k {d['fund_post10k']:3d} muertes {d['muertes']:4d} mord malas {d['mordidas_malas']:5d} "
               f"sin nada bueno {d['frac_sin_bueno_mundo']:.3f} escrituras {d['escrituras']} ({d['seg']} s)")
    L = letra(R, semillas)
    di("\nPOR SEMILLA (cruzan): " + " | ".join(f"{s}: " + " ".join(f"{n}={R[(n, s)]['cruzan_real']}" for n in SHAS) for s in semillas))
    di(f"LETRA: {json.dumps(L, ensure_ascii=False)}")
    with open(os.path.join(dest, "resumen.json"), "w", encoding="utf-8") as fh:
        json.dump(dict(letra=L, semillas=semillas, por_semilla={f"{k[0]}_{k[1]}": {x: d[x] for x in ("persisten", "cruzan_real", "R0_real_med",
                       "vida_med", "fund_post10k", "muertes", "mordidas_malas", "frac_sin_bueno_mundo", "escrituras")} for k, d in R.items()}), fh, indent=1)
    di(f"FIN DE LA TANDA ({time.time() - t0:.0f} s) - valida {L['valida']} - " + ", ".join(f"{k}: {v['clase']}" for k, v in L["piezas"].items()))


if __name__ == "__main__":
    main()
