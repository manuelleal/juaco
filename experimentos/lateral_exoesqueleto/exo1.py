"""EXO-1: JUACO como exoesqueleto de un LLM congelado. Ver PREREGISTRO_exo1.md (escrito antes de correr).

Uso:
  python exo1.py --humo                      # LLM falso (azar determinista), sin llamadas: prueba el arnes
  python exo1.py --desde 901 --n 3           # serie real (claude -p --model haiku)
  python exo1.py --desde 904 --n 3           # replica
"""
import argparse, json, math, os, re, subprocess, sys, tempfile, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import shutil
import numpy as np
CLAUDE = shutil.which("claude") or "claude"

HERR = ["vek", "tulo", "brim", "saf"]
FAM = ["latón", "roble", "cristal", "hierro"]
CAMBIAN = ["latón", "roble"]
S1 = dict(color=["roja", "azul", "verde"], tam=["pequeña", "grande"], marca=["Orla", "Treno", "Brisk"])
S2 = dict(color=["ocre", "violeta", "gris"], tam=["mediana", "alargada"], marca=["Quimo", "Vasti", "Pello"])
DIAS = [(1, 12, "S1"), (2, 8, "S1"), (3, 8, "S2"), (4, 12, "S1"), (5, 8, "MIX")]
BRAZOS_LLM = ["A", "B", "Bf", "C", "Cx"]
AQUI = os.path.dirname(os.path.abspath(__file__))
TXT_R = {1: "ABRIÓ (+1)", 0: "no abrió (0)", -1: "DAÑÓ la caja (-1)"}
PRED_V = {"abre": 1, "no_abre": 0, "dano": -1}


# ---------------------------------------------------------------- mundo
def mundo(seed):
    rng = np.random.default_rng(seed)
    regla = {}
    for f in FAM:
        p = list(rng.permutation(HERR))
        regla[f] = dict(abre=p[0], dano=p[1], neutras=[p[2], p[3]])
    tareas = []
    for dia, n, pool in DIAS:
        fams = [FAM[i % 4] for i in range(n)]
        fams = [fams[i] for i in rng.permutation(n)]
        for f in fams:
            P = S1 if pool == "S1" else S2 if pool == "S2" else (S1 if rng.random() < 0.5 else S2)
            tareas.append(dict(dia=dia, fam=f, color=str(rng.choice(P["color"])),
                               tam=str(rng.choice(P["tam"])), marca=str(rng.choice(P["marca"]))))
    return regla, tareas


def resultado(regla, t, h):
    r = regla[t["fam"]]
    abre = r["abre"]
    if t["dia"] >= 4 and t["fam"] in CAMBIAN:
        abre = r["neutras"][0]          # la vieja pasa a no abrir; una neutra pasa a abrir; la que dana sigue
    return 1 if h == abre else -1 if h == r["dano"] else 0


def desc(t):
    return f"caja de {t['fam']}, color {t['color']}, {t['tam']}, marca {t['marca']}"


# ---------------------------------------------------------------- memorias
class Nada:
    def contexto(self, t): return ""
    def actualiza(self, t, h, pred, r): pass


def tok(s):
    return [w for w in re.findall(r"\w+", s.lower()) if w not in ("caja", "de", "color", "marca")]


class RAG:
    """B: TF-IDF coseno sobre la descripcion; top-3; empate -> mas reciente."""
    def __init__(self): self.ep = []
    def contexto(self, t):
        if not self.ep: return ""
        docs = [tok(desc(e[0])) for e in self.ep]
        N = len(docs); df = Counter(w for d in docs for w in set(d))
        idf = lambda w: math.log((N + 1) / (df.get(w, 0) + 1)) + 1
        def vec(ws):
            c = Counter(ws); v = {w: c[w] * idf(w) for w in c}
            n = math.sqrt(sum(x * x for x in v.values())) or 1
            return {w: x / n for w, x in v.items()}
        q = vec(tok(desc(t)))
        sc = [(sum(q.get(w, 0) * x for w, x in vec(d).items()), i) for i, d in enumerate(docs)]
        top = sorted(sc, key=lambda s: (-s[0], -s[1]))[:3]
        return self._txt([self.ep[i] for _, i in top])
    def _txt(self, eps):
        l = [f"- [día {e[0]['dia']}] {desc(e[0])} → usó '{e[1]}': {TXT_R[e[2]]}" for e in eps]
        return "Memoria de experiencias (puede estar incompleta u obsoleta):\n" + "\n".join(l)
    def actualiza(self, t, h, pred, r): self.ep.append((t, h, r))


class RAGfam(RAG):
    """Bf: los 3 episodios mas recientes de la misma familia."""
    def contexto(self, t):
        eps = [e for e in self.ep if e[0]["fam"] == t["fam"]][-3:][::-1]
        return self._txt(eps) if eps else ""


class Juaco:
    """C: valor por consecuencia; episodio de un golpe por sorpresa o contradiccion; relevo episodio>Q; 3 piezas."""
    def __init__(self, perm=None, rng=None):
        self.Q = defaultdict(lambda: {h: 0.0 for h in HERR}); self.n = defaultdict(Counter)
        self.E = defaultdict(dict); self.conf = defaultdict(Counter)
        self.perm = perm or {h: h for h in HERR}; self.rng = rng
    def V(self, f):
        return {h: (self.E[f][h] if h in self.E[f] else self.Q[f][h] if self.n[f][h] else None) for h in HERR}
    def actualiza(self, t, h, pred, r):
        f = t["fam"]
        self.Q[f][h] += 0.3 * (r - self.Q[f][h]); self.n[f][h] += 1
        sorpresa = abs(r - PRED_V.get(pred, 0)) >= 1
        contradice = h in self.E[f] and self.E[f][h] != r
        if sorpresa or contradice or h not in self.E[f]:
            if contradice: self.conf[f][h] = 0
            self.E[f][h] = r                       # escritura de un golpe (sobrescribe)
        self.conf[f][h] += 1
    def contexto(self, t):
        f = t["fam"]; V = self.V(f); P = self.perm
        prob = {h: v for h, v in V.items() if v is not None}
        if not prob: return ""
        neg = min(prob, key=prob.get); pos = max(prob, key=prob.get)
        l = []
        l.append(f"ADVERTENCIA ({f}): '{P[neg]}' {TXT_R[-1] if prob[neg] <= -0.5 else 'no ha dañado'} (valor {prob[neg]:+.2f})."
                 if prob[neg] < 0 else f"ADVERTENCIA ({f}): ninguna herramienta ha dañado aún.")
        l.append(f"EJEMPLO ({f}): '{P[pos]}' ABRIÓ la caja (valor {prob[pos]:+.2f})." if prob[pos] > 0
                 else f"EJEMPLO ({f}): ninguna herramienta abre según lo vivido ahora.")
        nop = [P[h] for h in HERR if V[h] is None]
        cero = [P[h] for h in HERR if V[h] is not None and -0.5 < V[h] <= 0]
        mal = [P[h] for h in HERR if V[h] is not None and V[h] <= -0.5]
        if prob[pos] > 0:
            l.append(f"ESTRATEGIA vigente ({f}): usar '{P[pos]}' (confianza: {self.conf[f][pos]} resultado(s) seguidos iguales).")
        else:
            l.append(f"ESTRATEGIA vigente ({f}): ninguna abre ahora; probar una no probada {nop or '(ninguna)'} "
                     f"o una que no hizo nada {cero or '(ninguna)'}; nunca {mal or '(ninguna)'}.")
        return "Memoria JUACO (seleccionada por valor):\n" + "\n".join(l)

def elige_J(mem, t, rng):
    V = mem.V(t["fam"])
    pos = [h for h in HERR if V[h] is not None and V[h] > 0]
    if pos: return max(pos, key=lambda h: V[h]), "abre"
    nop = [h for h in HERR if V[h] is None]
    if nop: return str(rng.choice(nop)), "no_abre"
    cero = [h for h in HERR if V[h] > -0.5]
    return (str(rng.choice(cero)) if cero else max(HERR, key=lambda h: V[h])), "no_abre"


# ---------------------------------------------------------------- LLM
SIS = "Eres un agente que resuelve tareas en un taller. Respondes solo con el JSON pedido."
def prompt(t, mem_txt):
    return ("Estás en un taller. Tu objetivo es abrir cajas sin dañarlas. Cada caja se abre con una de cuatro "
            "herramientas: vek, tulo, brim, saf. Una la abre, una la daña (lo peor) y las otras no hacen nada. Cuál es "
            "cuál depende de la caja, y puede cambiar con el tiempo.\n"
            + (mem_txt + "\n" if mem_txt else "") +
            f"Tarea de hoy (día {t['dia']}): {desc(t)}.\n"
            'Responde SOLO con JSON en una línea: {"herramienta": "<vek|tulo|brim|saf>", "prediccion": "<abre|no_abre|dano>"}')


def llama_claude(p):
    cmd = [CLAUDE, "-p", "--model", "haiku", "--tools", "", "--strict-mcp-config", "--no-session-persistence",
           "--setting-sources", "", "--system-prompt", SIS]
    r = subprocess.run(cmd, input=p, capture_output=True, text=True, encoding="utf-8", timeout=180,
                       cwd=tempfile.gettempdir())
    return r.stdout


def parse(s):
    m = re.search(r"\{.*?\}", s or "", re.S)
    if not m: return None
    try: d = json.loads(m.group(0))
    except Exception: return None
    h = str(d.get("herramienta", "")).strip().lower()
    p = str(d.get("prediccion", "")).strip().lower().replace("ñ", "n").replace(" ", "_")
    if h not in HERR: return None
    return h, (p if p in PRED_V else "no_abre")


# ---------------------------------------------------------------- corrida
def corre(brazo, seed, humo):
    regla, tareas = mundo(seed)
    rng = np.random.default_rng(seed * 100 + BRAZOS_LLM.index(brazo) if brazo in BRAZOS_LLM else seed * 100 + 9)
    if brazo == "Cx":
        p = list(HERR)
        while any(a == b for a, b in zip(p, HERR)): p = list(rng.permutation(HERR))
        mem = Juaco(perm=dict(zip(HERR, p)))
    else:
        mem = {"A": Nada, "B": RAG, "Bf": RAGfam, "C": Juaco, "J": Juaco}[brazo]()
    reg = []
    for t in tareas:
        ctx = mem.contexto(t); inval = 0; t0 = time.time()
        if brazo == "J":
            h, pred = elige_J(mem, t, rng)
        else:
            out = None
            for _ in range(2):
                raw = str(rng.choice(HERR)) if humo else llama_claude(prompt(t, ctx))
                out = (raw, "no_abre") if humo else parse(raw)
                if out: break
            if not out: out = (str(rng.choice(HERR)), "no_abre"); inval = 1
            h, pred = out
        r = resultado(regla, t, h)
        mem.actualiza(t, h, pred, r)
        reg.append(dict(**t, h=h, pred=pred, r=r, ctx_chars=len(ctx), lat=round(time.time() - t0, 2), inval=inval))
    return dict(brazo=brazo, seed=seed, regla=regla, reg=reg)


def metricas(runs):
    out = {}
    for b in sorted({x["brazo"] for x in runs}, key=lambda z: (BRAZOS_LLM + ["J"]).index(z)):
        R = [x for x in runs if x["brazo"] == b]
        m = {}
        for d in range(1, 6):
            v = [e["r"] == 1 for x in R for e in x["reg"] if e["dia"] == d]; m[f"acierto_d{d}"] = round(np.mean(v), 3)
        v = [e["r"] == 1 for x in R for e in x["reg"] if e["dia"] == 4 and e["fam"] in CAMBIAN]
        m["acierto_d4_cambiadas"] = round(np.mean(v), 3)
        v = [e["r"] == 1 for x in R for e in x["reg"] if e["dia"] >= 2]; m["acierto_d2a5"] = round(np.mean(v), 3)
        rep = 0; vuelta = 0
        for x in R:
            danadas = defaultdict(set); fallo_viejo = set()
            for e in x["reg"]:
                if e["h"] in danadas[e["fam"]]: rep += 1
                if e["r"] == -1: danadas[e["fam"]].add(e["h"])
                if e["dia"] == 4 and e["fam"] in CAMBIAN and e["h"] == x["regla"][e["fam"]]["abre"]:
                    if e["fam"] in fallo_viejo: vuelta += 1
                    fallo_viejo.add(e["fam"])
        m["M2_errores_repetidos"] = rep; m["M3_vuelve_a_vieja_d4"] = vuelta
        m["M5_ctx_chars_media"] = round(np.mean([e["ctx_chars"] for x in R for e in x["reg"]]), 1)
        m["M6_latencia_media_s"] = round(np.mean([e["lat"] for x in R for e in x["reg"]]), 2)
        m["M7_invalidas"] = sum(e["inval"] for x in R for e in x["reg"])
        out[b] = m
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--desde", type=int, default=901); ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--humo", action="store_true"); ap.add_argument("--hilos", type=int, default=8)
    ap.add_argument("--brazos", default=",".join(BRAZOS_LLM + ["J"]))
    a = ap.parse_args()
    seeds = list(range(a.desde, a.desde + a.n)); brazos = a.brazos.split(",")
    trabajos = [(b, s) for s in seeds for b in brazos]
    with ThreadPoolExecutor(a.hilos) as ex:
        runs = list(ex.map(lambda bs: corre(bs[0], bs[1], a.humo), trabajos))
    M = metricas(runs)
    sello = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom = f"exo1_{'humo_' if a.humo else ''}s{seeds[0]}-{seeds[-1]}_{sello}"
    os.makedirs(os.path.join(AQUI, "datos"), exist_ok=True)
    json.dump(dict(seeds=seeds, metricas=M, runs=runs), open(os.path.join(AQUI, "datos", nom + ".json"), "w",
              encoding="utf-8"), ensure_ascii=False, indent=1)
    cols = ["acierto_d1", "acierto_d2", "acierto_d3", "acierto_d4", "acierto_d4_cambiadas", "acierto_d5", "acierto_d2a5",
            "M2_errores_repetidos", "M3_vuelve_a_vieja_d4", "M5_ctx_chars_media", "M6_latencia_media_s", "M7_invalidas"]
    print(nom); print("brazo " + " ".join(c.replace("acierto_", "")[:10].rjust(10) for c in cols))
    for b, m in M.items(): print(f"{b:5} " + " ".join(str(m[c]).rjust(10) for c in cols))
