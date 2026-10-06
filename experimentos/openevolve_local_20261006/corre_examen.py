"""corre_examen.py — EXAMEN SELLADO de los brazos R y E (PREREGISTRO_R.md sec. 6, PREREGISTRO_E.md sec. 5). Imprime la letra.

Mision: llegar a la AGI por este camino. T 100 000, fundador NO limpio, instrumento local (ctx limpio, un modulo por linaje), pista y juez
sin tocar. Brazos: los MEJOR_* que existan (corridas/<B>/best/best_program.py, congelados en examen/programas/ con su sha), HUMO, O1, RAIZ.

Uso:  python -B corre_examen.py --humo                 humo de UN proceso: semilla de practica 281991, T 5 000, HUMO/O1/RAIZ; escribe su JSON
      python -B corre_examen.py --desde 282001 [--pool 4]    serie (20 semillas; la corre el COORDINADOR)
      python -B corre_examen.py --desde 282021 [--pool 4]    replica (solo si la serie no da NO en el brazo que se replica)
Reanudable: salta los JSON que ya existen.
"""
import argparse, hashlib, json, os, shutil, statistics as st, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("JUACO_OE_SEM", "0,0,0"); os.environ.setdefault("JUACO_OE_BRAZO", "R")
for _k in ("JUACO_OE_CTX_LIMPIO", "JUACO_OE_MOD_POR_LINAJE", "JUACO_OE_FILTRO_EXTRA"): os.environ.pop(_k, None)
sys.path.insert(0, AQUI); sys.dont_write_bytecode = True
import evaluador as EV

N = 20; VALIDAS = (282001, 282021); MAY = 5
R_MIN = 15                                   # R: MEJOR_Rk con mayoria en >= 15/20
E_P1, E_P2, E_P3 = 15, 13, 0.10              # E: mayoria >= 15/20; gana a O1 en >= 13/20; mediana de frac_sin_bueno <= 0.10
V_O1, V_RAIZ, V_HUMO = 6, 1, 15              # validez: O1 >= 6/20, RAIZ <= 1/20, HUMO >= 15/20 con mayoria
SHA_FIJOS = {"HUMO": "69fcfcb2473f", "RAIZ": "50b2fc3241da"}


def sha12(p):
    return hashlib.sha256(open(p, encoding="utf-8").read().encode("utf-8")).hexdigest()[:12]


def brazos(dest_prog):
    os.makedirs(dest_prog, exist_ok=True); B = []
    for nom in ("R1", "R2", "E"):
        src = os.path.join(AQUI, "corridas", nom, "best", "best_program.py"); fin = os.path.join(AQUI, "corridas", nom, "fin.json")
        dst = os.path.join(dest_prog, f"MEJOR_{nom}.py")
        if not os.path.exists(dst) and os.path.exists(src) and os.path.exists(fin): shutil.copyfile(src, dst)   # se congela al cerrar la busqueda
        if os.path.exists(dst): B.append((f"MEJOR_{nom}", dst))
    return B + [("HUMO", os.path.join(AQUI, "programas", "HUMO.py")), ("O1", "O1"), ("RAIZ", os.path.join(AQUI, "programas", "RAIZ.py"))]


def una(a):
    nom, ruta, seed, T, dest = a
    sal = os.path.join(dest, f"{nom}_s{seed}_T{T}.json")
    if not os.path.exists(sal):
        r = subprocess.run([sys.executable, "-B", os.path.join(AQUI, "corre_carro.py"), ruta, str(seed), str(T), sal],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=AQUI)
        if r.returncode != 0: return nom, seed, None, r.stderr[-800:]
    return nom, seed, json.load(open(sal, encoding="utf-8")), None


def sospechas(nom, D, raiz_malas):
    """Senales preregistradas de 'sospechoso de trampa': si hay alguna, PRIMERO se lee el codigo y el veredicto queda en suspenso."""
    s = []
    if sum(d["cruzan_real"] == 9 for d in D) >= 0.9 * len(D): s.append("cruzan 9/9 en >= 90 % de las semillas")
    if any(d["R0_real_med"] > 1.15 for d in D): s.append("mediana de R0 real > 1.15 en alguna semilla")
    if any(d["muertes_vol"] > 0 for d in D): s.append("muertes voluntarias > 0")
    if any(d["coherente"] < d["n"] for d in D): s.append("contabilidad del juez no coherente en algun linaje")
    may = [d for d in D if d["cruzan_real"] >= MAY]
    if may and st.median(d["mordidas_malas"] for d in may) < 10 * max(raiz_malas, 1): s.append("cruza SIN la firma de limpieza (mordidas malas < 10 x RAIZ)")
    if may and st.median(d["vida_med"] for d in may) > 20000: s.append("cruza con vida mediana > 20 000 pasos")
    if may and st.median(d["frac_sin_bueno_mundo"] for d in may) < 0.01: s.append("cruza con el mundo casi nunca sin comida (< 0.01; O1 da 0.04)")
    return s


def letra(R, semillas, B):
    noms = [n for n, _ in B]; cz = {n: {s: R[(n, s)]["cruzan_real"] for s in semillas if (n, s) in R} for n in noms}
    M = {n: sum(v >= MAY for v in cz[n].values()) for n in noms}; S = {n: sum(cz[n].values()) for n in noms}
    val = dict(V1_completo=all(len(cz[n]) == len(semillas) for n in noms), V2_O1=M["O1"] >= V_O1, V3_RAIZ=M["RAIZ"] <= V_RAIZ, V4_HUMO=M["HUMO"] >= V_HUMO)
    raiz_malas = st.median(R[("RAIZ", s)]["mordidas_malas"] for s in semillas if ("RAIZ", s) in R) if cz["RAIZ"] else 0
    out = dict(validez=val, mayoria=M, suma_cruzan=S, sospechas={}, R={}, E={})
    for n in noms:
        if n.startswith("MEJOR_"): out["sospechas"][n] = sospechas(n, [R[(n, s)] for s in semillas if (n, s) in R], raiz_malas)
    lee = all(val.values())
    cumple = {n: M[n] >= R_MIN for n in ("MEJOR_R1", "MEJOR_R2") if n in M}
    if cumple:
        if not lee: v = "NO SE LEE"
        elif len(cumple) == 2: v = "FUNCIONA" if all(cumple.values()) else ("HAY ALGO MODESTO" if any(cumple.values()) or all(M[n] >= MAY for n in cumple) else "NO")
        else: v = "HAY ALGO MODESTO (una sola replica: falta R2)" if cumple.get("MEJOR_R1") else "NO (con una sola replica; R2 puede subirlo a MODESTO)"
        out["R"] = dict(cumple=cumple, veredicto=v)
    if "MEJOR_E" in M:
        e = cz["MEJOR_E"]; o = cz["O1"]; gana = sum(e[s] > o[s] for s in semillas if s in e and s in o); pierde = sum(e[s] < o[s] for s in semillas if s in e and s in o)
        fsb = st.median(R[("MEJOR_E", s)]["frac_sin_bueno_mundo"] for s in semillas if ("MEJOR_E", s) in R)
        fsb_h = st.median(R[("HUMO", s)]["frac_sin_bueno_mundo"] for s in semillas if ("HUMO", s) in R)
        P = dict(P1_mayoria=M["MEJOR_E"] >= E_P1, P2_gana_O1=gana >= E_P2, P3_mundo_con_comida=fsb <= E_P3, P4_no_pierde_contra_HUMO=S["MEJOR_E"] >= S["HUMO"])
        igual = sha12(dict(B)["MEJOR_E"]) == SHA_FIJOS["HUMO"]
        if not lee: v = "NO SE LEE"
        elif igual: v = "NO (el mejor del brazo E ES HUMO: la busqueda no movio nada)"
        elif all(P.values()): v = "FUNCIONA"
        elif P["P1_mayoria"] and (P["P2_gana_O1"] or P["P3_mundo_con_comida"]): v = "HAY ALGO MODESTO"
        else: v = "NO"
        out["E"] = dict(puertas=P, gana=gana, pierde=pierde, empata=len(semillas) - gana - pierde, frac_sin_bueno_mediana=fsb, frac_sin_bueno_HUMO=fsb_h,
                        escrituras_mediana=st.median(R[("MEJOR_E", s)]["escrituras"] for s in semillas if ("MEJOR_E", s) in R), veredicto=v)
    if any(out["sospechas"].values()):
        out["AVISO"] = "HAY SENALES DE SOSPECHA: el veredicto queda EN SUSPENSO hasta leer el codigo del programa (preregistro)."
    return out


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument("--desde", type=int); ap.add_argument("--pool", type=int, default=4); ap.add_argument("--humo", action="store_true")
    a = ap.parse_args()
    if a.humo:
        semillas = [281991]; T = 5000; dest = os.path.join(AQUI, "examen", "humo"); B = [b for b in brazos(os.path.join(AQUI, "examen", "programas")) if not b[0].startswith("MEJOR_")]
    else:
        if a.desde not in VALIDAS: raise SystemExit(f"--desde debe ser una de {VALIDAS} (preregistro)")
        semillas = list(range(a.desde, a.desde + N)); T = 100000
        dest = os.path.join(AQUI, "examen", f"s{semillas[0]}-{semillas[-1]}"); B = brazos(os.path.join(AQUI, "examen", "programas"))
    os.makedirs(dest, exist_ok=True); LOG = os.path.join(dest, "log.txt")

    def di(s=""):
        print(s, flush=True)
        with open(LOG, "a", encoding="utf-8") as fh: fh.write(s + "\n")
    di(f"EXAMEN {time.strftime('%Y-%m-%d %H:%M:%S')} - semillas {semillas[0]}-{semillas[-1]} - T {T} - fundador no limpio - ctx limpio, un modulo por linaje - "
       f"corre_examen.py {hashlib.sha256(open(__file__, 'rb').read()).hexdigest()[:16]}")
    for n, p in B:
        if n == "O1": continue
        v = EV._revisa(open(p, encoding="utf-8").read()); s = sha12(p); di(f"  programa {n}: sha {s} - filtro {'PASA' if not v else 'RECHAZADO ' + str(v[:2])}")
        if v or (n in SHA_FIJOS and s != SHA_FIJOS[n]): raise SystemExit(f"{n}: sha o filtro no coinciden con el preregistro: no se corre")
    tareas = [(n, p, s, T, dest) for s in semillas for n, p in B]; t0 = time.time(); R = {}

    def anota(nom, seed, d, err):
        if d is None: di(f"  FALLA {nom} s{seed}: {err}"); return
        R[(nom, seed)] = d
        di(f"  [{time.time() - t0:6.0f}s] {nom:9s} s{seed} persisten {d['persisten']}/9 cruzan {d['cruzan_real']}/9 R0 med {d['R0_real_med']:.4f} vida med {d['vida_med']:8.1f} "
           f"fund>10k {d['fund_post10k']:3d} muertes {d['muertes']:4d} mord malas {d['mordidas_malas']:5d} sin bueno {d['frac_sin_bueno_mundo']:.3f} escrituras {d['escrituras']} ({d['seg']} s)")
    if a.humo:
        for t in tareas: anota(*una(t))          # un proceso a la vez
    else:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(una, tareas): anota(*x)
    L = letra(R, semillas, B) if not a.humo else dict(humo=True, nota="humo de tuberia del examen: no hay letra con 1 semilla y T 5 000")
    with open(os.path.join(dest, "resumen.json"), "w", encoding="utf-8") as fh:
        json.dump(dict(letra=L, semillas=semillas, T=T, por_corrida={f"{k[0]}_{k[1]}": {x: d[x] for x in ("persisten", "cruzan_real", "R0_real_med", "vida_med",
                  "fund_post10k", "muertes", "muertes_vol", "mordidas_malas", "frac_sin_bueno_mundo", "escrituras", "coherente")} for k, d in R.items()}), fh, ensure_ascii=False, indent=1)
    di(f"LETRA: {json.dumps(L, ensure_ascii=False)}")
    di(f"ESCRITO {os.path.join(dest, 'resumen.json')}   ({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
