"""identidad.py — ARNES DE IDENTIDAD del bloque MURO MINIMO. UN proceso a la vez, sin Pool.

1. construye.py --check: el instrumento copiado es igual a su origen y la pista/juez/O1 tienen el sha fijado.
2. Filtro de reglas (evaluador._revisa) sobre MINIMO, HUMO y O1_SINLIMPIA; diferencia de MINIMO contra la raiz (difflib).
3. Corridas ancla a T 100 000: el corre_carro.py copiado debe dar BIT A BIT lo registrado (todos los campos del JSON menos `seg`,
   incluido rng_mundo_estado):
     O1            s883001  contra  openevolve_serie/cordura/O1_s883001_T100000.json
     HUMO          s276001  contra  openevolve_serie/examen_grande/s276001-276020/HUMO_s276001_T100000.json
     O1_SINLIMPIA  s883001  contra  openevolve_serie/cordura/CTRL_O1_SINLIMPIA_s883001_T100000.json
       (el control de este bloque es la RAIZ de HUMO; el ancla es carros/CTRL_O1_SINLIMPIA.py: mismo codigo salvo comentarios y
        contadores `st`, asi que debe dar la misma fisica; si no, se declara.)

Uso:  python -B identidad.py                 (pasos 1-2, sin corridas)
      python -B identidad.py O1 HUMO O1_SINLIMPIA      (pasos 1-2 y las anclas pedidas, una tras otra)
Escribe identidad_salida.json (acumula las anclas ya corridas).
"""
import difflib, hashlib, json, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
SER = os.path.join(REPO, "experimentos", "openevolve_serie")
os.environ.setdefault("JUACO_OE_SEM", "0,0,0")
sys.path.insert(0, AQUI)
import construye as C

PROG = os.path.join(AQUI, "programas")
ANCLAS = {
    "O1": ("O1", 883001, os.path.join(SER, "cordura", "O1_s883001_T100000.json")),
    "HUMO": (os.path.join(PROG, "HUMO.py"), 276001, os.path.join(SER, "examen_grande", "s276001-276020", "HUMO_s276001_T100000.json")),
    "O1_SINLIMPIA": (os.path.join(PROG, "O1_SINLIMPIA.py"), 883001, os.path.join(SER, "cordura", "CTRL_O1_SINLIMPIA_s883001_T100000.json")),
}
SAL = os.path.join(AQUI, "identidad_salida.json")


def codigo(txt):
    """lineas de codigo: sin vacias, sin comentarios de linea completa (los docstrings SI cuentan)."""
    return [l.rstrip() for l in txt.splitlines() if l.strip() and not l.strip().startswith("#")]


def main():
    out = json.load(open(SAL, encoding="utf-8")) if os.path.exists(SAL) else {}
    print(f"IDENTIDAD MURO MINIMO {time.strftime('%Y-%m-%d %H:%M:%S')}  python {sys.version.split()[0]}")
    mal = C.main(True)
    out["construye_check"] = "TODO IGUAL" if not mal else f"{mal} DIFERENCIAS"
    if mal: raise SystemExit("el instrumento copiado no es igual a su origen: no se sigue")
    import evaluador as EV
    out["filtro"] = {}
    for n in ("MINIMO", "HUMO", "O1_SINLIMPIA"):
        src = C.lf(os.path.join(PROG, n + ".py")); v = EV._revisa(src)
        out["filtro"][n] = dict(sha12=C.s16(src)[:12], pasa=not v, violaciones=v[:5])
        print(f"  filtro {n}: sha12 {C.s16(src)[:12]} - {'PASA' if not v else v[:3]}")
    a = codigo(C.lf(os.path.join(PROG, "O1_SINLIMPIA.py"))); b = codigo(C.lf(os.path.join(PROG, "MINIMO.py")))
    d = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if not l.startswith(("+++", "---", "@@"))]
    mas = [l for l in d if l.startswith("+")]; menos = [l for l in d if l.startswith("-")]
    out["diff_MINIMO_vs_raiz"] = dict(lineas_raiz=len(a), lineas_MINIMO=len(b), agregadas=len(mas), quitadas=len(menos))
    print(f"  MINIMO contra la raiz (lineas de codigo, docstrings incluidos): raiz {len(a)}, MINIMO {len(b)}, +{len(mas)} / -{len(menos)}")
    for l in d: print("      " + l)
    out.setdefault("anclas", {})
    for nom in sys.argv[1:]:
        ruta, seed, ref = ANCLAS[nom]
        R = json.load(open(ref, encoding="utf-8"))
        print(f"  [{time.strftime('%H:%M:%S')}] ancla {nom} s{seed} T {R['T']} ...", flush=True)
        t0 = time.time()
        r = subprocess.run([sys.executable, "-B", os.path.join(AQUI, "corre_carro.py"), ruta, str(seed), str(R["T"])],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=AQUI)
        if r.returncode != 0: raise SystemExit(f"ancla {nom} revento: {r.stderr[-800:]}")
        D = json.loads(r.stdout.strip().splitlines()[-1])
        campos = sorted((set(R) | set(D)) - {"seg"})
        dif = [k for k in campos if R.get(k, "<falta>") != D.get(k, "<falta>")]
        out["anclas"][nom] = dict(seed=seed, T=R["T"], referencia=os.path.relpath(ref, REPO).replace("\\", "/"), campos=len(campos),
                                  iguales=len(campos) - len(dif), difieren=dif, cruzan_real=D["cruzan_real"],
                                  rng_mundo_estado=D["rng_mundo_estado"], seg_aqui=D["seg"], seg_registro=R["seg"],
                                  pared=round(time.time() - t0, 1))
        print(f"  [{time.strftime('%H:%M:%S')}] ancla {nom} s{seed}: {len(campos) - len(dif)}/{len(campos)} campos iguales "
              f"{'-> IDENTICA' if not dif else '-> DIFIERE en ' + str(dif)} · cruzan {D['cruzan_real']}/9 (registro {R['cruzan_real']}) · "
              f"rng {D['rng_mundo_estado']} (registro {R['rng_mundo_estado']}) · {D['seg']} s (registro {R['seg']} s)", flush=True)
        for k in dif: print(f"      {k}: aqui {D.get(k)} | registro {R.get(k)}")
        with open(SAL, "w", encoding="utf-8") as fh: json.dump(out, fh, indent=1, ensure_ascii=False)
    with open(SAL, "w", encoding="utf-8") as fh: json.dump(out, fh, indent=1, ensure_ascii=False)
    ok = all(not x["difieren"] for x in out["anclas"].values())
    print(f"IDENTIDAD: {len(out['anclas'])} anclas corridas, {'TODAS IDENTICAS' if ok and out['anclas'] else ('ninguna corrida' if not out['anclas'] else 'HAY DIFERENCIAS')}")


if __name__ == "__main__":
    main()
