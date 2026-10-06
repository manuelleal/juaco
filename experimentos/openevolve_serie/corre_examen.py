"""corre_examen.py — EXAMEN de la serie (PREREGISTRO_serie.md sec. 6): cada programa en las 5 semillas SELLADAS
275001-275005, T 100 000, fundador NO limpio, con corre_carro.py (pista y juez sin tocar). Pool 3. Antes de correr, cada
programa (salvo O1, que es de la pista) pasa el filtro de reglas; si no pasa, no se examina. Reanudable: salta los JSON que ya existen.

Uso:  python -B corre_examen.py NOMBRE=ruta.py [NOMBRE=ruta.py ...]      (O1 y RAIZ se agregan solos)
"""
import hashlib, json, os, subprocess, sys, time
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("JUACO_OE_SEM", "0,0,0")   # el evaluador lo exige; el examen solo usa su filtro y su base()
sys.path.insert(0, AQUI)
import evaluador as EV

SELLADAS = (275001, 275002, 275003, 275004, 275005); T = 100000
DEST = os.path.join(AQUI, "examen"); os.makedirs(DEST, exist_ok=True)
LOG = os.path.join(DEST, "examen.log")


def di(s=""):
    print(s, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh: fh.write(s + "\n")


def una(a):
    nom, ruta, seed = a
    sal = os.path.join(DEST, f"{nom}_s{seed}_T{T}.json")
    if not os.path.exists(sal):
        r = subprocess.run([sys.executable, "-B", os.path.join(AQUI, "corre_carro.py"), ruta, str(seed), str(T), sal],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=AQUI)
        if r.returncode != 0: return nom, seed, None, r.stderr[-800:]
    return nom, seed, json.load(open(sal, encoding="utf-8")), None


def main():
    brazos = [tuple(x.split("=", 1)) for x in sys.argv[1:]]
    brazos = [(n, os.path.abspath(p)) for n, p in brazos] + [("O1", "O1"), ("RAIZ", os.path.join(AQUI, "raiz", "programa_inicial.py"))]
    di(f"EXAMEN {time.strftime('%Y-%m-%d %H:%M:%S')} - semillas {SELLADAS} - T {T} - fundador no limpio - corre_examen.py "
       f"{hashlib.sha256(open(__file__, 'rb').read()).hexdigest()[:16]}")
    for nom, ruta in brazos:
        if nom == "O1": continue
        src = open(ruta, encoding="utf-8").read(); v = EV._revisa(src)
        di(f"  {nom}: {os.path.relpath(ruta, AQUI)} sha {hashlib.sha256(src.encode('utf-8')).hexdigest()[:12]} - filtro: {'PASA' if not v else v[:3]}")
        if v: raise SystemExit(f"{nom} no pasa el filtro: no se examina")
    t0 = time.time(); R = {}
    tareas = [(n, p, s) for s in SELLADAS for n, p in brazos]
    with Pool(3) as PL:
        for nom, seed, d, err in PL.imap_unordered(una, tareas):
            if d is None: di(f"  FALLA {nom} s{seed}: {err}"); continue
            R[f"{nom}_{seed}"] = {x: d[x] for x in ("persisten", "cruzan_real", "R0_real_med", "vida_med", "fund_post10k", "muertes",
                                                     "muertes_vol", "frac_sin_bueno_mundo", "mordidas_malas", "limpiezas_fisicas", "seg")}
            di(f"  [{time.time() - t0:6.0f}s] {nom:6s} s{seed} persisten {d['persisten']}/9 cruzan {d['cruzan_real']}/9 R0 med {d['R0_real_med']:.4f} "
               f"vida med {d['vida_med']:7.1f} fund>10k {d['fund_post10k']:4d} muertes {d['muertes']:4d} (vol {d['muertes_vol']}) "
               f"sin nada bueno {d['frac_sin_bueno_mundo']:.3f} mord malas {d['mordidas_malas']:5d} base {EV.base(d):.3f} ({d['seg']} s)")
    with open(os.path.join(DEST, "examen_resumen.json"), "w", encoding="utf-8") as fh: json.dump(R, fh, ensure_ascii=False, indent=1)
    di(f"total {time.time() - t0:.0f} s - {len(R)}/{len(tareas)} corridas")


if __name__ == "__main__":
    main()
