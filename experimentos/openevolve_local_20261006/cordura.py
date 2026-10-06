"""cordura.py — CORDURA del instrumento local (PREREGISTRO_R.md sec. 3). Un proceso a la vez, 6 corridas de pista (2 de T 100 000, 4 de T 25 000).

Mision: llegar a la AGI por este camino.
  C1  FILTRO: O1, RAIZ, HUMO e INMORTAL_B pasan el filtro ampliado; los tramposos T1, T2, T4, T5 y T6 son RECHAZADOS.
  C2  ENVOLTURA (sin pista): con un ctx como el de la pista (trae `fabrica` y `PAT`), el tramposo que esquiva el texto (T3) LEE la tabla
      sin envoltura y REVIENTA (KeyError) con ella; T7 (estado en la clase) queda aislado con un modulo por linaje.
  C3  ANCLA: O1 con las perillas ENCENDIDAS, fundador no limpio, T 100 000, en 883001 y 883002 da el registro campo a campo
      (experimentos/openevolve_serie/cordura/O1_s88300x_T100000.json: cruzan 5/9 y 8/9).
  C4  ERR-195: en la etapa 2 nueva (2 semillas de practica) el INMORTAL que no pare (mejor de la replica B de la nube) NO pasa
      (puntaje < 0.20) y HUMO SI pasa (>= 0.20). Con la formula del origen el inmortal habria pasado.
Uso:  <python del venv> -B cordura.py [--sin-ancla]      Escribe cordura/cordura_salida.json y cordura/cordura.log.
"""
import importlib.util, json, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
SER = os.path.join(REPO, "experimentos", "openevolve_serie")
PISTA = os.path.join(REPO, "experimentos", "carrera_escuderias")
DEST = os.path.join(AQUI, "cordura"); TR = os.path.join(DEST, "tramposos")
os.environ.update(JUACO_OE_SEM="281950;281951,281952;281953", JUACO_OE_BRAZO="R", JUACO_OE_SERIAL="1", JUACO_OE_SALIDA=os.path.join(DEST, "eval"),
                  PYTHONUTF8="1")
os.environ.pop("JUACO_OE_CTX_LIMPIO", None); os.environ.pop("JUACO_OE_MOD_POR_LINAJE", None)   # por defecto: encendidas
sys.dont_write_bytecode = True
sys.path.insert(0, AQUI)
import evaluador as EV
import corre_carro as CC

LOG = os.path.join(DEST, "cordura.log")


def di(s=""):
    print(s, flush=True)
    with open(LOG, "a", encoding="utf-8") as fh: fh.write(s + "\n")


def carga(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main():
    os.makedirs(DEST, exist_ok=True)
    R = dict(fecha=time.strftime("%Y-%m-%d %H:%M:%S")); ok = {}
    di(f"CORDURA {R['fecha']}  evaluador {EV.__file__}  perillas: ctx_limpio {CC.CTX_LIMPIO}, mod_por_linaje {CC.MOD_POR_LINAJE}, filtro_extra {EV.FILTRO_EXTRA}")
    # ---- C1 filtro
    honestos = {"O1": os.path.join(PISTA, "carros", "O1.py"), "RAIZ": os.path.join(AQUI, "programas", "RAIZ.py"),
                "HUMO": os.path.join(AQUI, "programas", "HUMO.py"), "INMORTAL_B": os.path.join(AQUI, "programas", "INMORTAL_B.py")}
    c1 = {}
    for n, p in honestos.items():
        v = EV._revisa(open(p, encoding="utf-8").read()); c1[n] = v; di(f"  C1 {n:18s} {'PASA' if not v else 'RECHAZADO ' + str(v[:2])}")
    for n in ("T1_fabrica", "T2_pat", "T3_fabrica_oculta", "T4_estado_numpy", "T5_np_load", "T6_bit_generator", "T7_estado_de_clase"):
        v = EV._revisa(open(os.path.join(TR, n + ".py"), encoding="utf-8").read()); c1[n] = v
        di(f"  C1 {n:18s} {'PASA el filtro' if not v else 'RECHAZADO: ' + v[0][:110]}")
    ok["C1_filtro"] = all(not c1[n] for n in honestos) and all(c1[n] for n in ("T1_fabrica", "T2_pat", "T4_estado_numpy", "T5_np_load", "T6_bit_generator")) \
        and not c1["T3_fabrica_oculta"] and not c1["T7_estado_de_clase"]
    R["C1"] = {k: v[:3] for k, v in c1.items()}
    # ---- C2 envoltura (sin correr la pista: solo crea(ctx) con un ctx como el de pista.run)
    import numpy as np
    sys.path.insert(0, PISTA)
    import pista as P
    CF = P.cfg_fabrica()
    ctx = dict(id="C#0", indice=0, n_linajes=9, T=1000, L=360, PAT={k: v.copy() for k, v in CF["PAT"].items()}, rng=np.random.default_rng([1, 0, 12, 0]),
               dote=0.6, rep_umbral=1.0, costo=0.001, costo_a=0.001, rep_X=500, cupo=16, ancho=8, fabrica=P.cfg_fabrica())
    t3 = carga("t3", os.path.join(TR, "T3_fabrica_oculta.py"))
    sin = t3.crea(dict(ctx)); lee_sin = sorted(sin.tabla)
    try: CC.Envoltura(t3).crea(dict(ctx)); con = "NO REVIENTA"
    except KeyError as e: con = f"KeyError {e}"
    di(f"  C2 T3 sin envoltura LEE la tabla (claves {lee_sin}); con envoltura: {con}")
    ms = [carga(f"t7_{i}", os.path.join(TR, "T7_estado_de_clase.py")) for i in range(3)]
    for i, m in enumerate(ms): CC.Envoltura(m).crea(dict(ctx, id=f"C#{i}"))
    aislado = [sorted(m.Carro.banco) for m in ms]
    uno = carga("t7_unico", os.path.join(TR, "T7_estado_de_clase.py"))
    for i in range(3): uno.crea(dict(ctx, id=f"C#{i}"))
    di(f"  C2 T7 un modulo por linaje: cada banco ve {aislado}; modulo compartido (origen): un banco con {sorted(uno.Carro.banco)}")
    ok["C2_envoltura"] = bool(lee_sin) and con.startswith("KeyError") and all(len(a) == 1 for a in aislado) and len(uno.Carro.banco) == 3
    R["C2"] = dict(T3_sin_envoltura=lee_sin, T3_con_envoltura=con, T7_aislado=aislado, T7_compartido=sorted(uno.Carro.banco))
    # ---- C3 ancla O1
    R["C3"] = {}
    if "--sin-ancla" not in sys.argv:
        bien = True
        for seed in (883001, 883002):
            sal = os.path.join(DEST, f"O1_s{seed}_T100000.json")
            if not os.path.exists(sal):
                r = subprocess.run([sys.executable, "-B", os.path.join(AQUI, "corre_carro.py"), "O1", str(seed), "100000", sal], capture_output=True, text=True,
                                   encoding="utf-8", errors="replace", cwd=AQUI)
                if r.returncode != 0: raise SystemExit("CORDURA: O1 revento: " + r.stderr[-800:])
            d = json.load(open(sal, encoding="utf-8")); reg = json.load(open(os.path.join(SER, "cordura", f"O1_s{seed}_T100000.json"), encoding="utf-8"))
            dif = [k for k in sorted(set(d) | set(reg)) if k not in ("seg", "ctx_limpio", "mod_por_linaje") and d.get(k, "<falta>") != reg.get(k, "<falta>")]
            bien = bien and not dif
            R["C3"][seed] = dict(cruzan_real=d["cruzan_real"], persisten=d["persisten"], R0_real_med=d["R0_real_med"], causas=d["causas"], difieren=dif, seg=d["seg"])
            di(f"  C3 O1 s{seed}: cruzan {d['cruzan_real']}/9, persisten {d['persisten']}/9, R0 med {d['R0_real_med']}, causas {d['causas']} "
               f"| registro: cruzan {reg['cruzan_real']}/9, R0 {reg['R0_real_med']} | campos que difieren: {dif or 'NINGUNO'} ({d['seg']} s)")
        ok["C3_ancla_O1"] = bien
    # ---- C4 ERR-195
    R["C4"] = {}
    for n in ("INMORTAL_B", "HUMO"):
        r = EV.evaluate_stage2(honestos[n]); m = r.metrics
        regs = [json.loads(l) for l in open(os.path.join(EV.SAL, "evaluaciones.jsonl"), encoding="utf-8")]
        sha = EV.hashlib.sha256(open(honestos[n], encoding="utf-8").read().encode("utf-8")).hexdigest()[:12]
        D = [x for x in regs if x.get("sha") == sha and x.get("etapa") == 2 and "error" not in x][-2:]
        viejo = [(0.20 if d["sin_extincion"] >= 5 else 0.05) + 0.10 * (0.7 * d["sin_extincion"] / 9 + 0.3 * min(d["R0_real_med"], 1.0)) * EV._fv(d) for d in D]
        R["C4"][n] = dict(puntaje=m["combined_score"], pasa=m["combined_score"] >= 0.20, crian=[EV._cria(d) for d in D], sin_extincion=[d["sin_extincion"] for d in D],
                          nac_reales_l=[d["nac_reales_l"] for d in D], puntaje_formula_origen=viejo, metricas=m)
        di(f"  C4 {n:11s} etapa 2 nueva: puntaje {m['combined_score']:.4f} -> {'PASA' if m['combined_score'] >= 0.20 else 'NO pasa'} a la etapa 3 "
           f"| sin extincion {[d['sin_extincion'] for d in D]}, crian {[EV._cria(d) for d in D]}, nacimientos por linaje {[d['nac_reales_l'] for d in D]} "
           f"| con la formula del origen, por semilla: {[round(x, 4) for x in viejo]}")
    ok["C4_ERR195"] = (not R["C4"]["INMORTAL_B"]["pasa"]) and R["C4"]["HUMO"]["pasa"]
    R["ok"] = ok; R["cordura"] = all(ok.values())
    with open(os.path.join(DEST, "cordura_salida.json"), "w", encoding="utf-8") as fh: json.dump(R, fh, ensure_ascii=False, indent=1)
    di(f"CORDURA: {ok} -> {'PASA' if R['cordura'] else 'FALLA'}   (cordura/cordura_salida.json)")
    return 0 if R["cordura"] else 1


if __name__ == "__main__":
    sys.exit(main())
