"""corre_examen.py — EXAMEN del bloque MURO MINIMO PIEZA (PREREGISTRO.md). 6 brazos x 20 semillas, T 100 000, fundador NO limpio
(ERR-191), corre_carro.py copiado del examen grande (pista y juez sin tocar). Construido por anclas (construye.py + construye_examen.py)
desde experimentos/muro_minimo_20261008/corre_examen.py (sha d202bd621d2eb4ba). Reanudable: salta los JSON que ya existen.
Log y resumen.json se escriben DESDE EL ARRANQUE y tras cada corrida. Antes de correr: construye --check, sha y filtro de cada
programa, y cotejo PREREGISTRO.md <-> PREREGISTRADO (coteja_preregistro.py copiado con sha fijado).

Uso (SOLO el coordinador usa --pool > 1):
  python -B corre_examen.py --serie --pool 3        (885001-885020)
  python -B corre_examen.py --replica --pool 3      (885021-885040)
  python -B corre_examen.py --combina               (lee las dos tandas y escribe examen/bloque.json con el veredicto del bloque)
  python -B corre_examen.py --humo [--desde 884901 --n 1 --T 20000 --brazos ...]   (humo de UN proceso; nunca semillas selladas)
"""
import argparse, hashlib, json, os, statistics as st, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("JUACO_OE_SEM", "0,0,0")
sys.path.insert(0, AQUI)
import construye as C
import evaluador as EV
import coteja_preregistro as CP

PROG = os.path.join(AQUI, "programas")
BRAZOS = ["MINIMO", "M_PIZARRA", "M_RADIO", "M_RECICLA", "M_URGENCIA", "HUMO"]
PIEZAS = ["M_PIZARRA", "M_RADIO", "M_RECICLA", "M_URGENCIA"]   # un brazo por pieza de §2 del bloque anterior, en ese orden
SHAS = {"MINIMO": "b9cfbb3bb7cb", "M_PIZARRA": "1f320504565f", "M_RADIO": "f886a5ff8c88", "M_RECICLA": "fbd7cfc330f2",
        "M_URGENCIA": "54a34b7207bc", "HUMO": "69fcfcb2473f"}   # sha12 texto LF (los de las variantes los imprime construye.py)
SERIE = range(885001, 885021)
REPLICA = range(885021, 885041)
SELLADAS = range(SERIE.start, REPLICA.stop)
N_LETRA = 20
T_LETRA = 100000
MAY = 5               # semilla "con mayoria": cruzan_real >= 5 de 9 (cruza_real del juez: R0 real >= 0.90 y 0 fundadores tras t = 10 000)
CIERRA_MIN = 15       # una pieza CIERRA la brecha: su brazo con mayoria en >= 15/20
MUEVE_LIN = 20        # una pieza MUEVE: suma de linajes que cruzan del brazo >= la de MINIMO + 20 (misma tanda, mismas semillas)
C1_MINIMO_MAX = 14    # control bajo que puede fallar: MINIMO con mayoria en <= 14/20 (si cruza, no hay brecha que cerrar)
V_HUMO_MIN = 15       # control alto (validez): HUMO con mayoria en >= 15/20
HUMO_SEMILLA = 884901
HUMO_T = 20000
CAMPOS = ("persisten", "cruzan_real", "R0_real_med", "vida_med", "fund_post10k", "muertes", "nac_reales", "mordidas_malas",
          "limpiezas_fisicas", "frac_sin_bueno_mundo", "escrituras", "causas", "mord", "seg")
PREREGISTRADO = dict(BRAZOS=BRAZOS, PIEZAS=PIEZAS, SHAS=SHAS, SERIE=SERIE, REPLICA=REPLICA, N_LETRA=N_LETRA, T_LETRA=T_LETRA, MAY=MAY,
                     CIERRA_MIN=CIERRA_MIN, MUEVE_LIN=MUEVE_LIN, C1_MINIMO_MAX=C1_MINIMO_MAX, V_HUMO_MIN=V_HUMO_MIN,
                     HUMO_SEMILLA=HUMO_SEMILLA, HUMO_T=HUMO_T)


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
    """La letra de PREREGISTRO.md §5 para UNA tanda. Si falta algun brazo o corrida, V1 cae y el veredicto es NO SE LEE."""
    c = {k: d["cruzan_real"] for k, d in R.items()}
    tiene = {n: [s for s in semillas if (n, s) in c] for n in brazos}
    may = {n: sum(c[(n, s)] >= MAY for s in tiene[n]) for n in brazos}
    suma = {n: sum(c[(n, s)] for s in tiene[n]) for n in brazos}
    med = {n: {x: (round(float(st.median([R[(n, s)][x] for s in tiene[n]])), 4) if tiene[n] else None)
               for x in ("R0_real_med", "vida_med", "muertes", "mordidas_malas", "limpiezas_fisicas", "frac_sin_bueno_mundo", "fund_post10k")}
           for n in brazos}
    out = dict(mayoria=may, suma_cruzan=suma, medianas=med, n_semillas=len(semillas))
    completa = set(brazos) == set(BRAZOS) and len(semillas) == N_LETRA and len(R) == len(BRAZOS) * len(semillas)
    if not completa:
        out.update(validez=dict(V1_completa=False), veredicto="NO SE LEE"); return out
    par = lambda a, b: dict(gana=sum(c[(a, s)] > c[(b, s)] for s in semillas), pierde=sum(c[(a, s)] < c[(b, s)] for s in semillas))
    v = dict(V1_completa=True, V2_shas_filtro_cotejo=True, V3_HUMO_cruza=may["HUMO"] >= V_HUMO_MIN)
    ctrl = dict(C1_MINIMO_no_cruza=may["MINIMO"] <= C1_MINIMO_MAX)
    pz = {}
    for n in PIEZAS:
        dl = suma[n] - suma["MINIMO"]; ci = may[n] >= CIERRA_MIN; mu = dl >= MUEVE_LIN
        pz[n] = dict(mayoria=may[n], linajes=suma[n], dif_linajes_vs_MINIMO=dl, cierra=ci, mueve=mu,
                     estado="CIERRA" if ci else ("MUEVE" if mu else "NADA"), vs_MINIMO=par(n, "MINIMO"), vs_HUMO=par(n, "HUMO"),
                     frac_linajes_de_HUMO=(round(suma[n] / suma["HUMO"], 4) if suma["HUMO"] else 0.0))
    if not all(v.values()) or not all(ctrl.values()): ver = "NO SE LEE"
    elif any(p["cierra"] for p in pz.values()): ver = "FUNCIONA"
    elif any(p["mueve"] for p in pz.values()): ver = "HAY ALGO MODESTO"
    else: ver = "NO"
    out.update(validez=v, control=ctrl, piezas=pz, cierran=[n for n in PIEZAS if pz[n]["estado"] == "CIERRA"],
               mueven=[n for n in PIEZAS if pz[n]["estado"] == "MUEVE"], descriptivo=dict(MINIMO_vs_HUMO=par("MINIMO", "HUMO")),
               veredicto=ver)
    return out


def combina():
    """El bloque (PREREGISTRO.md §5): una pieza vale lo MENOR de sus dos estados; el bloque se lee de las piezas, no de las tandas."""
    est = {"NADA": 0, "MUEVE": 1, "CIERRA": 2}
    L = {}
    for nom, t in (("serie", SERIE), ("replica", REPLICA)):
        f = os.path.join(AQUI, "examen", f"s{t.start}-{t.stop - 1}", "resumen.json")
        if not os.path.exists(f): raise SystemExit(f"--combina: falta {f}")
        d = json.load(open(f, encoding="utf-8"))
        if not d.get("terminado"): raise SystemExit(f"--combina: {f} no termino")
        L[nom] = d["letra"]
    out = dict(veredicto_serie=L["serie"]["veredicto"], veredicto_replica=L["replica"]["veredicto"], piezas={})
    if "NO SE LEE" in (out["veredicto_serie"], out["veredicto_replica"]):
        out["veredicto_bloque"] = "NO SE LEE"
    else:
        for n in PIEZAS:
            e = [L[k]["piezas"][n]["estado"] for k in ("serie", "replica")]
            out["piezas"][n] = dict(serie=e[0], replica=e[1], bloque=min(e, key=lambda x: est[x]),
                                    mayoria=[L[k]["piezas"][n]["mayoria"] for k in ("serie", "replica")],
                                    linajes=[L[k]["piezas"][n]["linajes"] for k in ("serie", "replica")])
        b = [p["bloque"] for p in out["piezas"].values()]
        out["cierran_x2"] = [n for n in PIEZAS if out["piezas"][n]["bloque"] == "CIERRA"]
        out["mueven_x2"] = [n for n in PIEZAS if out["piezas"][n]["bloque"] == "MUEVE"]
        out["veredicto_bloque"] = "FUNCIONA" if "CIERRA" in b else ("HAY ALGO MODESTO" if "MUEVE" in b else "NO")
    with open(os.path.join(AQUI, "examen", "bloque.json"), "w", encoding="utf-8") as fh: json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"VEREDICTO DEL BLOQUE: {out['veredicto_bloque']}")


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument("--desde", type=int, default=None); ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--pool", type=int, default=1); ap.add_argument("--humo", action="store_true")
    ap.add_argument("--serie", action="store_true"); ap.add_argument("--replica", action="store_true")
    ap.add_argument("--combina", action="store_true")
    ap.add_argument("--brazos", default=",".join(BRAZOS)); ap.add_argument("--T", type=int, default=None)
    a = ap.parse_args()
    if a.combina: return combina()
    if a.humo + a.serie + a.replica != 1: raise SystemExit("elige UNO: --humo, --serie o --replica (o --combina)")
    brazos = a.brazos.split(",")
    if any(b not in BRAZOS for b in brazos): raise SystemExit(f"--brazos: solo {BRAZOS}")
    if a.humo:
        a.desde = HUMO_SEMILLA if a.desde is None else a.desde; a.n = 1 if a.n is None else a.n; a.T = HUMO_T if a.T is None else a.T
        semillas = list(range(a.desde, a.desde + a.n))
        if any(s in SELLADAS for s in semillas): raise SystemExit(f"--humo no puede tocar las semillas selladas {SELLADAS.start}-{SELLADAS.stop - 1}")
        if a.pool != 1: raise SystemExit("--humo es de UN proceso (--pool 1)")
        if a.T > 200000 or len(semillas) * len(brazos) > 6: raise SystemExit("--humo: regla 3 de EQUIPO (<= 6 corridas, <= 200 000 pasos cada una)")
        dest = os.path.join(AQUI, "humo", f"s{semillas[0]}-{semillas[-1]}_T{a.T}")
    else:
        tanda = SERIE if a.serie else REPLICA
        if a.desde not in (None, tanda.start) or a.n not in (None, N_LETRA) or a.T not in (None, T_LETRA) or brazos != BRAZOS:
            raise SystemExit(f"sin --humo: las {N_LETRA} semillas de la tanda, T {T_LETRA} y los {len(BRAZOS)} brazos (preregistro)")
        semillas = list(tanda); a.T = T_LETRA
        dest = os.path.join(AQUI, "examen", f"s{semillas[0]}-{semillas[-1]}")
    os.makedirs(dest, exist_ok=True)
    LOG = os.path.join(dest, "log.txt")

    def di(s=""):
        print(s, flush=True)
        with open(LOG, "a", encoding="utf-8") as fh: fh.write(s + "\n")
    di(f"MURO MINIMO PIEZA {'HUMO-DE-RUNNER' if a.humo else ('SERIE' if a.serie else 'REPLICA')} {time.strftime('%Y-%m-%d %H:%M:%S')} - "
       f"semillas {semillas[0]}-{semillas[-1]} - T {a.T} - fundador no limpio - pool {a.pool} - brazos {brazos} - "
       f"corre_examen.py {hashlib.sha256(open(__file__, 'rb').read()).hexdigest()[:16]}")
    if C.main(True): raise SystemExit("construye.py --check: el instrumento no es igual a su origen: no se corre")
    for n, sh in SHAS.items():
        src = C.lf(os.path.join(PROG, n + ".py")); s2 = C.s16(src)[:12]; v = EV._revisa(src)
        di(f"  {n}: sha {s2} - filtro {'PASA' if not v else v[:2]}")
        if s2 != sh or v: raise SystemExit(f"{n}: sha o filtro no coinciden con el preregistro: no se corre")
    filas, difs = CP.coteja(os.path.join(AQUI, "PREREGISTRO.md"), PREREGISTRADO)
    di(f"  cotejo PREREGISTRO.md <-> PREREGISTRADO: {len(filas)} nombres - " + ("TODO IGUAL" if not difs else f"{len(difs)} DIFERENCIAS {difs[:3]}"))
    if difs: raise SystemExit("cotejo preregistro <-> runner con diferencias: no se corre")
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
