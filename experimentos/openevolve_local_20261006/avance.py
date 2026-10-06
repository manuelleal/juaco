"""avance.py — como va cada brazo (solo lee). Uso:  python -B avance.py        (no llama al modelo ni corre la pista)

Una iteracion TERMINADA es una linea del log  corridas/<BRAZO>.log  con el texto  "Iteration N: Program ... completed in".
El brazo termino cuando el log trae la linea que empieza por  FIN_BRAZO  (y existe corridas/<BRAZO>/fin.json).
"""
import json, os, re, statistics as st

AQUI = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(AQUI, "corridas")


def lineas(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if os.path.exists(p) else []


for nom in ("HUMO_TUBERIA_R1", "HUMO_TUBERIA_E", "R1", "R2", "E"):
    sal = os.path.join(C, nom); log = os.path.join(C, nom + ".log")
    if not os.path.exists(sal): continue
    txt = open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
    its = [int(x) for x in re.findall(r"Iteration (\d+): Program", txt)]
    L = lineas(os.path.join(sal, "registro_llm", "llamadas.jsonl")); tok = [x["tokens_salida"] for x in L if x.get("tokens_salida")]
    E = [e for e in lineas(os.path.join(sal, "evaluaciones.jsonl")) if "error" not in e and "rechazado" not in e]
    e3 = {}
    for e in E:
        if e["etapa"] == 3: e3.setdefault(e["sha"], {})[e["seed"]] = (e["cruzan_real"], e["persisten"], e["frac_sin_bueno_mundo"], e["escrituras"])
    pid = open(os.path.join(C, nom + ".pid")).read().strip() if os.path.exists(os.path.join(C, nom + ".pid")) else "?"
    print(f"{nom}: pid {pid} · iteraciones terminadas {max(its) if its else 0} · llamadas {len(L)} · tokens de salida mediana "
          f"{st.median(tok) if tok else '-'}{'  << MEDIANA BAJO 10 000: ERR-194, avisar' if len(tok) >= 5 and st.median(tok) < 10000 else ''} · "
          f"USD equiv {sum((x.get('costo_usd_equiv') or 0) for x in L):.2f} · {'TERMINADO' if 'FIN_BRAZO' in txt else 'en curso o cortado'}")
    for sha, d in e3.items():
        print(f"    etapa 3  {sha}  cruzan por semilla {[v[0] for v in d.values()]}  persisten {[v[1] for v in d.values()]}  "
              f"sin nada bueno {[v[2] for v in d.values()]}  escrituras {[v[3] for v in d.values()]}")
    m = re.findall(r"New best[^\n]*|best program[^\n]*combined_score=[0-9.]+", txt)
    if m: print("    ultimo mejor en el log:", m[-1][:200])
