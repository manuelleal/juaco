"""corre_examen_grande.py — EXAMEN GRANDE de HUMO contra O1 (PREREGISTRO_examen_grande.md). 20 semillas por tanda, T 100 000,
fundador NO limpio, corre_carro.py (pista y juez sin tocar), Pool 3. Reanudable (salta los JSON que ya existen). Imprime la letra.

Uso:  python -B corre_examen_grande.py --desde 276001     (serie)
      python -B corre_examen_grande.py --desde 276021     (replica; solo si la serie no da NO)
"""
import argparse, hashlib, json, os, subprocess, sys, time
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("JUACO_OE_SEM", "0,0,0")
sys.path.insert(0, AQUI)
import evaluador as EV

T = 100000; N = 20
BRAZOS = [("HUMO", os.path.join(AQUI, "examen", "programas", "HUMO.py")), ("O1", "O1")]
SHA_HUMO = "69fcfcb2473f"; SHA_O1 = "99436afa2715f028"
VALIDAS = (276001, 276021)
MAY = 5          # mayoria: cruzan_real >= 5 de 9
P1_MIN = 15      # HUMO con mayoria en >= 15/20
P2_MIN = 12      # HUMO > O1 (linajes que cruzan) en >= 12/20; empates no cuentan
V3_MIN = 6       # cordura: O1 con mayoria en >= 6/20


def una(a):
    nom, ruta, seed, dest = a
    sal = os.path.join(dest, f"{nom}_s{seed}_T{T}.json")
    if not os.path.exists(sal):
        r = subprocess.run([sys.executable, "-B", os.path.join(AQUI, "corre_carro.py"), ruta, str(seed), str(T), sal],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=AQUI)
        if r.returncode != 0: return nom, seed, None, r.stderr[-800:]
    return nom, seed, json.load(open(sal, encoding="utf-8")), None


def letra(R, semillas):
    h = {s: R[("HUMO", s)]["cruzan_real"] for s in semillas}; o = {s: R[("O1", s)]["cruzan_real"] for s in semillas}
    v = dict(V1_completa=len(R) == 2 * len(semillas), V3_O1_cordura=sum(o[s] >= MAY for s in semillas) >= V3_MIN)
    p1 = sum(h[s] >= MAY for s in semillas); gana = sum(h[s] > o[s] for s in semillas); pierde = sum(h[s] < o[s] for s in semillas)
    p = dict(P1_HUMO_mayoria=p1 >= P1_MIN, P2_HUMO_gana_O1=gana >= P2_MIN)
    if not all(v.values()): ver = "NO SE LEE"
    elif all(p.values()): ver = "FUNCIONA"
    elif p["P1_HUMO_mayoria"]: ver = "HAY ALGO MODESTO"
    else: ver = "NO"
    return dict(validez=v, puertas=p, HUMO_mayoria=p1, O1_mayoria=sum(o[s] >= MAY for s in semillas), gana=gana, pierde=pierde,
                empata=len(semillas) - gana - pierde, suma_HUMO=sum(h.values()), suma_O1=sum(o.values()), veredicto=ver)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument("--desde", type=int, required=True)
    a = ap.parse_args()
    if a.desde not in VALIDAS: raise SystemExit(f"--desde debe ser una de {VALIDAS} (preregistro)")
    semillas = list(range(a.desde, a.desde + N))
    dest = os.path.join(AQUI, "examen_grande", f"s{semillas[0]}-{semillas[-1]}"); os.makedirs(dest, exist_ok=True)
    LOG = os.path.join(dest, "log.txt")

    def di(s=""):
        print(s, flush=True)
        with open(LOG, "a", encoding="utf-8") as fh: fh.write(s + "\n")
    sh = hashlib.sha256(open(BRAZOS[0][1], encoding="utf-8").read().encode("utf-8")).hexdigest()[:12]
    so = hashlib.sha256(open(os.path.join(EV.PISTA, "carros", "O1.py"), "rb").read()).hexdigest()[:16]
    v = EV._revisa(open(BRAZOS[0][1], encoding="utf-8").read())
    di(f"EXAMEN GRANDE {time.strftime('%Y-%m-%d %H:%M:%S')} - semillas {semillas[0]}-{semillas[-1]} - T {T} - fundador no limpio - "
       f"corre_examen_grande.py {hashlib.sha256(open(__file__, 'rb').read()).hexdigest()[:16]} - HUMO sha {sh} - O1 sha {so} - filtro HUMO {'PASA' if not v else v[:2]}")
    if sh != SHA_HUMO or so != SHA_O1 or v: raise SystemExit("sha o filtro no coinciden con el preregistro: no se corre")
    t0 = time.time(); R = {}
    with Pool(3) as PL:
        for nom, seed, d, err in PL.imap_unordered(una, [(n, p, s, dest) for s in semillas for n, p in BRAZOS]):
            if d is None: di(f"  FALLA {nom} s{seed}: {err}"); continue
            R[(nom, seed)] = d
            di(f"  [{time.time() - t0:6.0f}s] {nom:4s} s{seed} persisten {d['persisten']}/9 cruzan {d['cruzan_real']}/9 R0 med {d['R0_real_med']:.4f} "
               f"vida med {d['vida_med']:7.1f} fund>10k {d['fund_post10k']:3d} muertes {d['muertes']:4d} mord malas {d['mordidas_malas']:5d} ({d['seg']} s)")
    L = letra(R, semillas)
    di("\nPOR SEMILLA (cruzan HUMO / O1): " + " · ".join(f"{s}: {R[('HUMO', s)]['cruzan_real']}/{R[('O1', s)]['cruzan_real']}"
                                                       for s in semillas if ('HUMO', s) in R and ('O1', s) in R))
    di(f"LETRA: {json.dumps(L, ensure_ascii=False)}")
    with open(os.path.join(dest, "resumen.json"), "w", encoding="utf-8") as fh:
        json.dump(dict(letra=L, semillas=semillas, por_semilla={f"{k[0]}_{k[1]}": {x: d[x] for x in ("persisten", "cruzan_real", "R0_real_med",
                       "vida_med", "fund_post10k", "muertes", "mordidas_malas", "frac_sin_bueno_mundo")} for k, d in R.items()}), fh, indent=1)
    di(f"VEREDICTO DE LA TANDA: {L['veredicto']}   ({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
