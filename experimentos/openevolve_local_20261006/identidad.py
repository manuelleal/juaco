"""identidad.py — ARNES DE IDENTIDAD del instrumento local (un proceso a la vez; 6 corridas de T = 5 000).

Mision: llegar a la AGI por este camino. Se corre ANTES de mirar ningun numero.
  (1) corre_carro.py: con las dos perillas en 0 (JUACO_OE_CTX_LIMPIO=0, JUACO_OE_MOD_POR_LINAJE=0) la salida es IGUAL CAMPO A CAMPO a la del
      origen (experimentos/openevolve_serie/corre_carro.py), incluido el estado final del rng del mundo. Programas: RAIZ y HUMO.
      Ademas (no es identidad, es un dato): con las perillas en 1 un programa honesto debe dar la MISMA fisica. Si HUMO cambiara, es que
      usaba la tabla del ctx o estado de modulo compartido, y eso se reporta antes de seguir.
  (2) evaluador.py: con JUACO_OE_BRAZO=ORIGEN y una semilla por etapa, las tres etapas devuelven las MISMAS metricas y artefactos que el
      evaluador del origen sobre los mismos resumenes fisicos (los de experimentos/openevolve_serie/corridas/A/evaluaciones.jsonl; sin
      correr la pista: se sustituye _corre por el registro).
Uso:  <python del venv> -B identidad.py        Escribe identidad_salida.json. Codigo de salida 0 = identidad.
"""
import importlib.util, json, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
SER = os.path.join(REPO, "experimentos", "openevolve_serie")
SEED = 281990; T = 5000   # semilla de practica (nunca examen ni busqueda)
FUERA = ("seg", "ctx_limpio", "mod_por_linaje")   # reloj y las dos claves nuevas


def corre(script, prog, ctx, mod):
    env = dict(os.environ, JUACO_OE_CTX_LIMPIO=str(ctx), JUACO_OE_MOD_POR_LINAJE=str(mod), PYTHONUTF8="1")
    r = subprocess.run([sys.executable, "-B", script, prog, str(SEED), str(T)], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env, cwd=os.path.dirname(script))
    if r.returncode != 0: raise SystemExit(f"IDENTIDAD: revento {script} {prog}:\n{r.stderr[-1500:]}")
    return json.loads(r.stdout.strip().splitlines()[-1])


def difiere(a, b):
    ks = sorted((set(a) | set(b)) - set(FUERA))
    return [k for k in ks if a.get(k, "<falta>") != b.get(k, "<falta>")]


def carga(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main():
    out = dict(fecha=time.strftime("%Y-%m-%d %H:%M:%S"), seed=SEED, T=T, corre_carro={}, evaluador={}); ok = True
    print(f"IDENTIDAD {out['fecha']}  semilla {SEED}  T {T}", flush=True)
    for nom in ("RAIZ", "HUMO"):
        prog = os.path.join(AQUI, "programas", nom + ".py")
        o = corre(os.path.join(SER, "corre_carro.py"), prog, 0, 0)
        a = corre(os.path.join(AQUI, "corre_carro.py"), prog, 0, 0)
        e = corre(os.path.join(AQUI, "corre_carro.py"), prog, 1, 1)
        d0 = difiere(o, a); d1 = difiere(o, e); ok = ok and not d0
        out["corre_carro"][nom] = dict(campos=len(o), difieren_apagado=d0, difieren_encendido=d1, rng_mundo_igual=o["rng_mundo_estado"] == a["rng_mundo_estado"],
                                       muertes=o["muertes"], nac_reales=o["nac_reales"], mord=o["mord"])
        print(f"  corre_carro {nom}: origen vs copia con perillas APAGADAS: {len(o) - len(FUERA) + 1} campos, difieren {d0 or 'NINGUNO'} -> "
              f"{'IDENTICO' if not d0 else 'DISTINTO'}   | con perillas ENCENDIDAS difieren {d1 or 'NINGUNO'} "
              f"(muertes {o['muertes']}, nacimientos reales {o['nac_reales']}, mordidas {o['mord']})", flush=True)
    # (2) evaluador: mismas metricas y artefactos sobre los mismos resumenes
    os.environ["JUACO_OE_SEM"] = "1,2,3"; os.environ["JUACO_OE_BRAZO"] = "ORIGEN"; os.environ["JUACO_OE_SALIDA"] = os.path.join(AQUI, "identidad_tmp")
    EO = carga("ev_origen", os.path.join(SER, "evaluador.py")); EN = carga("ev_copia", os.path.join(AQUI, "evaluador.py"))
    regs = [json.loads(l) for l in open(os.path.join(SER, "corridas", "A", "evaluaciones.jsonl"), encoding="utf-8")]
    regs = [r for r in regs if "error" not in r and "rechazado" not in r]
    raiz = os.path.join(AQUI, "programas", "RAIZ.py"); n = 0; mal = 0
    for r in regs:
        EO._corre = lambda ruta, etapa, r=r: (dict(r), None)
        EN._corre = lambda ruta, etapa, r=r: ([dict(r)], None)
        f = {1: "evaluate_stage1", 2: "evaluate_stage2", 3: "evaluate_stage3"}[r["etapa"]]
        a = getattr(EO, f)(raiz); b = getattr(EN, f)(raiz); n += 1
        if a.metrics != b.metrics or a.artifacts != b.artifacts: mal += 1
    ok = ok and mal == 0 and n > 0
    out["evaluador"] = dict(registros=n, distintos=mal, por_etapa={e: sum(1 for r in regs if r["etapa"] == e) for e in (1, 2, 3)})
    print(f"  evaluador (BRAZO=ORIGEN, una semilla por etapa): {n} resumenes fisicos de la corrida A de la nube "
          f"({out['evaluador']['por_etapa']}), metricas o artefactos distintos: {mal} -> {'IDENTICO' if mal == 0 and n else 'DISTINTO'}", flush=True)
    out["identidad"] = bool(ok)
    with open(os.path.join(AQUI, "identidad_salida.json"), "w", encoding="utf-8") as fh: json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"IDENTIDAD: {'PASA' if ok else 'FALLA'}   (identidad_salida.json)", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
