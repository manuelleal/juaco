"""cordura_err195_registros.py — ERR-195 sobre los REGISTROS (no corre la pista ni llama al modelo).

Mision: llegar a la AGI por este camino. Aplica la puerta NUEVA de la etapa 2 (cria = 0 extinciones tras t 10 000 y >= 2 nacimientos reales;
pasa con >= 5/9) a todos los resumenes fisicos de etapa 2 ya registrados (humo del 5-oct y corridas A, B, H de la nube) y la compara con la
puerta del ORIGEN (sin extincion >= 5/9):
  - la meseta: programas que el origen dejaba pasar y la nueva NO (deben ser los inmortales que no paren);
  - falsos negativos: programas que la nueva NO deja pasar y que en la etapa 3 llegaron a cruzar con mayoria (debe ser 0).
Uso:  python -B cordura_err195_registros.py      Escribe cordura/err195_registros.json
"""
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
FUENTES = {"humo_5oct": r"C:\Users\User\Documents\PROYECTOS\JUACO-OPENEVOLVE\humo\salida\evaluaciones.jsonl",
           "nube_A": os.path.join(REPO, "experimentos", "openevolve_serie", "corridas", "A", "evaluaciones.jsonl"),
           "nube_B": os.path.join(REPO, "experimentos", "openevolve_serie", "corridas", "B", "evaluaciones.jsonl"),
           "nube_H": os.path.join(REPO, "experimentos", "openevolve_serie", "corridas", "H", "evaluaciones.jsonl")}
NB2 = 2


def cria(d): return sum(1 for f, nb in zip(d["fund_post10k_l"], d["nac_reales_l"]) if f == 0 and nb >= NB2)


out = {}
for nom, p in FUENTES.items():
    if not os.path.exists(p): print(f"{nom}: no esta {p}"); continue
    E = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    E = [e for e in E if "error" not in e and "rechazado" not in e]
    e2 = {e["sha"]: e for e in E if e["etapa"] == 2}; e3 = {e["sha"]: e for e in E if e["etapa"] == 3}
    viejo = {s for s, d in e2.items() if d["sin_extincion"] >= 5}; nuevo = {s for s, d in e2.items() if cria(d) >= 5}
    meseta = sorted(viejo - nuevo); falsos = sorted(s for s in e2 if s not in nuevo and s in e3 and e3[s]["cruzan_real"] >= 5)
    out[nom] = dict(programas_etapa2=len(e2), pasan_origen=len(viejo), pasan_nueva=len(nuevo), meseta_cerrada=len(meseta), falsos_negativos=falsos,
                    meseta=[dict(sha=s, sin_extincion=e2[s]["sin_extincion"], nac_reales=e2[s]["nac_reales"], vida_med=e2[s]["vida_med"],
                                 cruzan_etapa3=(e3[s]["cruzan_real"] if s in e3 else None)) for s in meseta],
                    nueva_pasa_y_origen_no=sorted(nuevo - viejo))
    print(f"{nom}: {len(e2)} programas con etapa 2 · pasaban con la puerta del origen {len(viejo)} · pasan con la nueva {len(nuevo)} · "
          f"meseta cerrada (origen si, nueva no) {len(meseta)}: nacimientos reales {[e2[s]['nac_reales'] for s in meseta]}, "
          f"cruzan en su etapa 3 {[e3[s]['cruzan_real'] if s in e3 else None for s in meseta]} · "
          f"falsos negativos (la nueva frena a uno que cruzo con mayoria) {len(falsos)} · nueva si y origen no {len(nuevo - viejo)}")
os.makedirs(os.path.join(AQUI, "cordura"), exist_ok=True)
with open(os.path.join(AQUI, "cordura", "err195_registros.json"), "w", encoding="utf-8") as fh: json.dump(out, fh, ensure_ascii=False, indent=1)
print("ESCRITO cordura/err195_registros.json")
