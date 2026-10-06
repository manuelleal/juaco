"""corre_examen.py — EXAMEN del humo: el mejor programa del bucle (congelado) junto a O1 (techo) y a la raiz (suelo), en las
semillas SELLADAS 272001-272003, T 100 000, fundador NO limpio. Un proceso a la vez. Antes de correr pasa el filtro de reglas.

Uso:  python -B examen/corre_examen.py <mejor_programa.py> [otro_programa.py ...]
"""
import hashlib, json, os, subprocess, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(AQUI)
sys.path.insert(0, BASE)
import evaluador as EV
SELLADAS = (272001, 272002, 272003); T = 100000
PY = sys.executable
log = open(os.path.join(AQUI, "examen.log"), "a", encoding="utf-8")


def di(s=""):
    print(s, flush=True); log.write(s + "\n"); log.flush()


def main():
    brazos = [("MEJOR" if i == 0 else f"OTRO{i}", os.path.abspath(p)) for i, p in enumerate(sys.argv[1:])]
    brazos += [("O1", "O1"), ("RAIZ", os.path.join(BASE, "raiz", "programa_inicial.py"))]
    for nom, ruta in brazos:
        if os.path.exists(ruta):
            src = open(ruta, encoding="utf-8").read()
            v = EV._revisa(src) if nom != "O1" else []
            di(f"{nom}: {ruta} sha {hashlib.sha256(src.encode('utf-8')).hexdigest()[:12]} · filtro de reglas: {'PASA' if not v else v[:3]}")
            if v: raise SystemExit("el programa no pasa el filtro: no se examina")
    t00 = time.time(); R = {}
    for seed in SELLADAS:
        for nom, ruta in brazos:
            sal = os.path.join(AQUI, f"{nom}_s{seed}_T{T}.json")
            if not os.path.exists(sal):
                r = subprocess.run([PY, "-B", os.path.join(BASE, "corre_carro.py"), ruta, str(seed), str(T), sal],
                                   capture_output=True, text=True, encoding="utf-8", errors="replace")
                if r.returncode != 0:
                    di(f"FALLA {nom} s{seed}: {r.stderr[-800:]}"); continue
            d = json.load(open(sal, encoding="utf-8")); R[(nom, seed)] = d
            di(f"{nom:6s} s{seed}  persisten {d['persisten']}/9  cruzan {d['cruzan_real']}/9  R0 real med {d['R0_real_med']:.4f}  vida med {d['vida_med']:8.1f}  "
               f"fund>10k {d['fund_post10k']:4d}  muertes {d['muertes']:4d} (vol {d['muertes_vol']})  sin nada bueno {d['frac_sin_bueno_mundo']:.3f}  "
               f"mord malas {d['mordidas_malas']:5d}  base {EV.base(d):.3f}  ({d['seg']} s)")
    di(f"total {time.time() - t00:.0f} s")
    with open(os.path.join(AQUI, "examen_resumen.json"), "w", encoding="utf-8") as fh:
        json.dump({f"{k[0]}_{k[1]}": {x: v[x] for x in ("persisten", "cruzan_real", "R0_real_med", "vida_med", "fund_post10k", "muertes",
                                                         "muertes_vol", "frac_sin_bueno_mundo", "mordidas_malas", "limpiezas_fisicas", "seg")}
                   for k, v in R.items()}, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
