"""construye_instrumento.py — CONSTRUYE POR ANCLAS el instrumento local del 6-oct-2026 (PREREGISTRO_R.md / PREREGISTRO_E.md).

Mision: llegar a la AGI por este camino; el metodo manda. Nada se escribe a mano sobre una copia: cada archivo sale de su ORIGEN
(sha fijado, sobre el texto con saltos LF) por reemplazos de ancla que deben aparecer EXACTAMENTE una vez. Si un origen cambio, aborta.

  origen (solo lectura)                                              ->  destino (esta carpeta)
  experimentos/openevolve_serie/corre_carro.py                       ->  corre_carro.py   (+ ctx limpio, + un modulo por linaje)
  experimentos/openevolve_serie/evaluador.py                         ->  evaluador.py     (+ filtro extra, + varias semillas, + cria)
  experimentos/openevolve_serie/lanza.py                             ->  lanza.py         (+ adaptador con libro)
  exploratorio/openevolve_humo_20261005/adaptador_claude.py          ->  adaptador_claude_ORIGINAL.py (copia byte a byte, testigo)
  exploratorio/openevolve_humo_20261005/config_humo.yaml             ->  config_R1.yaml, config_R2.yaml, config_E.yaml
  experimentos/openevolve_serie/raiz/programa_inicial.py             ->  programas/RAIZ.py
  experimentos/openevolve_serie/examen/programas/{HUMO,MEJOR_B}.py   ->  programas/HUMO.py, programas/INMORTAL_B.py

Uso:  python -B construye_instrumento.py            (escribe)      python -B construye_instrumento.py --check   (solo compara)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
SER = os.path.join(REPO, "experimentos", "openevolve_serie")
HUM = os.path.join(REPO, "exploratorio", "openevolve_humo_20261005")

SHA = {   # sha256[:16] del texto del origen con saltos LF (utf-8)
    "corre_carro": "ddcfd0f06a7acc87", "evaluador": "6736985f4f42cdc5", "lanza": "4402123932d74531",
    "adaptador": "b1ae88ae6b769bfb", "config": "657f8d504f4a074e", "raiz": "50b2fc3241da510e", "humo": "69fcfcb2473fdbf6", "inmortal": "2520d1d74549d6c4",
}


def lee(p):
    return open(p, encoding="utf-8", newline="").read().replace("\r\n", "\n")


def h(txt, n=16):
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()[:n]


def origen(clave, ruta):
    t = lee(ruta)
    if h(t) != SHA[clave]:
        raise SystemExit(f"CONSTRUYE: el origen {ruta} cambio (sha {h(t)}, esperado {SHA[clave]}): no se construye")
    return t


def una(src, viejo, nuevo, nombre):
    if src.count(viejo) != 1:
        raise SystemExit(f"CONSTRUYE: el ancla [{nombre}] aparece {src.count(viejo)} veces (debe ser 1)")
    return src.replace(viejo, nuevo)


def tramo(src, desde, hasta, nuevo, nombre):
    """Reemplaza desde el ancla `desde` (incluida) hasta el ancla `hasta` (excluida; None = fin del archivo)."""
    if src.count(desde) != 1 or (hasta is not None and src.count(hasta) != 1):
        raise SystemExit(f"CONSTRUYE: anclas de tramo [{nombre}] no unicas")
    i = src.index(desde); j = len(src) if hasta is None else src.index(hasta)
    if j <= i: raise SystemExit(f"CONSTRUYE: tramo [{nombre}] al reves")
    return src[:i] + nuevo + src[j:]


# ------------------------------------------------------------------------------------------------------------ corre_carro.py
def hace_corre_carro():
    s = origen("corre_carro", os.path.join(SER, "corre_carro.py"))
    s = una(s, '"""corre_carro.py — UNA corrida',
            '"""[CONSTRUIDO por construye_instrumento.py desde openevolve_serie/corre_carro.py ddcfd0f06a7acc87; NO editar a mano]\n'
            'PERILLAS (variables de entorno; con las dos en 0 es el origen bit a bit, ver identidad.py):\n'
            '  JUACO_OE_CTX_LIMPIO=1      el carro recibe un ctx SIN `fabrica` ni `PAT` (la tabla verdadera): solo las claves de CTX_OK.\n'
            '  JUACO_OE_MOD_POR_LINAJE=1  cada linaje carga SU PROPIA instancia del modulo (sin estado de modulo compartido entre linajes).\n'
            'La pista no se toca: la limpieza va en una envoltura que solo define crea(ctx).\n\n'
            'corre_carro.py — UNA corrida', "cabecera")
    s = una(s, "FL = 0   # fundador NO limpio (ERR-191)\n",
            "FL = 0   # fundador NO limpio (ERR-191)\n"
            'CTX_LIMPIO = int(os.environ.get("JUACO_OE_CTX_LIMPIO", "1"))\n'
            'MOD_POR_LINAJE = int(os.environ.get("JUACO_OE_MOD_POR_LINAJE", "1"))\n'
            'CTX_OK = ("id", "indice", "n_linajes", "T", "L", "rng", "dote", "rep_umbral", "costo", "costo_a", "rep_X", "cupo", "ancho")\n'
            "\n\n"
            "class Envoltura:\n"
            '    """Lo unico que la pista usa de un carro-modulo es .crea(ctx). Aqui se le entrega al candidato un ctx sin la tabla."""\n'
            "\n"
            "    def __init__(self, mod): self.mod = mod\n"
            "\n"
            "    def crea(self, ctx): return self.mod.crea({k: ctx[k] for k in CTX_OK})\n", "perillas")
    s = una(s,
            '    spec = importlib.util.spec_from_file_location("carro_candidato", ruta)\n'
            "    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)\n"
            "    t0 = time.time()\n"
            '    r = P.run(seed, [("C", mod)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=FL)\n',
            "    def carga(nombre):\n"
            "        spec = importlib.util.spec_from_file_location(nombre, ruta)\n"
            "        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod\n"
            '    mods = [carga(f"carro_candidato_{i}") for i in range(9)] if MOD_POR_LINAJE else [carga("carro_candidato")] * 9\n'
            '    carros = [("C", (Envoltura(m) if CTX_LIMPIO else m)) for m in mods]\n'
            "    t0 = time.time()\n"
            "    r = P.run(seed, carros, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=FL)\n", "carga y run")
    s = una(s, "        seed=seed, T=T, seg=seg, fundador_limpio=FL, n=len(L),\n",
            "        seed=seed, T=T, seg=seg, fundador_limpio=FL, n=len(L), ctx_limpio=CTX_LIMPIO, mod_por_linaje=MOD_POR_LINAJE,\n", "salida")
    return s


# -------------------------------------------------------------------------------------------------------------- evaluador.py
EV_CABECERA = '''"""[CONSTRUIDO por construye_instrumento.py desde openevolve_serie/evaluador.py 6736985f4f42cdc5; NO editar a mano]
INSTRUMENTO LOCAL 6-oct-2026 (PREREGISTRO_R.md y PREREGISTRO_E.md). Cambios sobre el origen, todos por perilla de entorno:
  JUACO_OE_SEM          "a,b,c" (origen: una semilla por etapa)  o  "a;b,c;d,e,f" (varias por etapa, corridas A LA VEZ, una por proceso)
  JUACO_OE_BRAZO        ORIGEN (formulas del origen, para la identidad) | R | E
  JUACO_OE_FILTRO_EXTRA 1 = ademas de revisa_carro y la regla de tabla, veta fabrica/PAT/EFECTO/VAL_VIVO, bit_generator, np.load,
                        np.fromfile y parientes, y toda ESCRITURA sobre un modulo importado (canal oculto entre linajes)
  JUACO_OE_SERIAL       1 = las semillas de una etapa corren una tras otra (humos de un proceso); 0 = a la vez (serie)
PUNTAJE (brazos R y E; por semilla y luego se agrega):
  etapa 1  filtro + T 5 000, 1 semilla            -> 0.05 si corre; 0 si no
  etapa 2  T 25 000, 2 semillas. cria = linajes con 0 extinciones tras t 10 000 Y >= 2 nacimientos reales (ERR-195)
           b2 = media_semillas{ [0.4*sin_extincion/9 + 0.4*cria/9 + 0.2*min(med R0 real, 1)] * (1 - frac. muertes voluntarias) }
           pasa si la media de cria >= 5/9 :  0.20 + 0.10*b2 ;  si no: 0.05 + 0.10*b2      (un inmortal que no pare NO pasa)
  etapa 3  T 100 000, 3 semillas
           R:  0.30 + 0.70 * media{ base }        base = la del humo: [0.5*persisten/9 + 0.4*cruzan/9 + 0.1*min(R0,1)] * (1 - fv)
           E:  0.30 + 0.70 * (0.7*media{bE} + 0.3*min{bE}) - 0.02*[escribe en la pizarra]
               bE = [0.20*persisten/9 + 0.10*min(R0,1) + (cruzan/9)*(0.45 + 0.25*comida)] * (1 - fv)
               comida = recorte(1 - frac_sin_bueno_mundo/0.25, 0, 1)     (HUMO ~0.04; O1 ~0.84; mundo siempre con algo bueno 1.0)
Lo que sigue es la cabecera del origen.

evaluador.py'''

EV_SEM = '''def _semillas():
    s = os.environ["JUACO_OE_SEM"]   # sin valor por defecto
    p = [[int(x) for x in e.split(",")] for e in s.split(";")] if ";" in s else [[int(x)] for x in s.split(",")]
    if len(p) != 3 or not all(p): raise SystemExit(f"JUACO_OE_SEM mal formada: {s!r}")
    return {1: p[0], 2: p[1], 3: p[2]}


SEM = _semillas()
BRAZO = os.environ.get("JUACO_OE_BRAZO", "ORIGEN")
if BRAZO not in ("ORIGEN", "R", "E"): raise SystemExit(f"JUACO_OE_BRAZO desconocido: {BRAZO!r}")
FILTRO_EXTRA = int(os.environ.get("JUACO_OE_FILTRO_EXTRA", "1"))
SERIAL = int(os.environ.get("JUACO_OE_SERIAL", "0"))
NB2 = 2   # nacimientos reales minimos por linaje para contar como "cria" en la etapa 2 (ERR-195)
EXTRA = [r"\\bfabrica\\b", r"\\bPAT\\b", r"\\bEFECTO\\b", r"\\bVAL_VIVO\\b", r"\\bbit_generator\\b", r"\\bfromfile\\b", r"\\bmemmap\\b",
         r"\\bDataSource\\b", r"\\b(np|numpy)\\s*\\.\\s*(load|loadtxt|genfromtxt|fromregex|lib|ctypeslib|core|testing|f2py)\\b"]


def _extra(src):
    """Hallazgos (a) y (b) del auditor del 5-oct: la tabla por el ctx, lectura de archivos por numpy, el estado del rng y el
    estado compartido en modulos importados (numpy, math... son UNA instancia para los 9 linajes)."""
    import ast
    v = []
    for n, linea in enumerate(src.splitlines(), 1):
        for pat in EXTRA:
            if re.search(pat, linea): v.append(f"X candidato:{n} prohibido /{pat}/: {linea.strip()[:80]}")
    try: arbol = ast.parse(src)
    except SyntaxError: return v
    alias = set()
    for nd in ast.walk(arbol):
        if isinstance(nd, ast.Import): alias.update((a.asname or a.name.split(".")[0]) for a in nd.names)
        elif isinstance(nd, ast.ImportFrom): alias.update((a.asname or a.name) for a in nd.names)
    for nd in ast.walk(arbol):
        if isinstance(nd, (ast.Attribute, ast.Subscript)) and isinstance(nd.ctx, (ast.Store, ast.Del)):
            r = nd
            while isinstance(r, (ast.Attribute, ast.Subscript)): r = r.value
            if isinstance(r, ast.Name) and r.id in alias:
                v.append(f"X candidato:{nd.lineno} escribe sobre el modulo importado `{r.id}` (estado compartido entre linajes)")
    return v
'''

EV_CORRE = '''def _corre(ruta, etapa):
    """Las corridas de la etapa (una por semilla), cada una en SU proceso y todas a la vez. Devuelve (lista de dict | None, error | None)."""
    import tempfile
    src = open(ruta, encoding="utf-8").read(); sha = hashlib.sha256(src.encode("utf-8")).hexdigest()[:12]
    dprog = os.path.join(SAL, "programas_evaluados"); os.makedirs(dprog, exist_ok=True)
    copia = os.path.join(dprog, f"{sha}.py")
    if not os.path.exists(copia):
        with open(copia, "w", encoding="utf-8") as fh: fh.write(src)
    t0 = time.time(); procs = []
    for s in SEM[etapa]:
        fo = tempfile.TemporaryFile(mode="w+", encoding="utf-8", errors="replace"); fe = tempfile.TemporaryFile(mode="w+", encoding="utf-8", errors="replace")
        procs.append((s, subprocess.Popen([sys.executable, "-B", CORRE, ruta, str(s), str(TT[etapa])], stdout=fo, stderr=fe, cwd=AQUI), fo, fe))
        if SERIAL:   # JUACO_OE_SERIAL=1: una corrida a la vez (humos y cordura de un agente; regla de un proceso)
            try: procs[-1][1].wait(timeout=LIMITE[etapa])
            except subprocess.TimeoutExpired: pass
    D = []; error = None
    for s, p, fo, fe in procs:
        try:
            p.wait(timeout=max(1.0, LIMITE[etapa] - (time.time() - t0)))
        except subprocess.TimeoutExpired:
            p.kill(); p.wait()   # solo el hijo propio que se paso del tiempo limite (lo mismo que hacia subprocess.run en el origen)
            _anota(dict(sha=sha, etapa=etapa, seed=s, error="tiempo limite", seg=round(time.time() - t0, 1)))
            error = error or f"tiempo limite ({LIMITE[etapa]} s) en la etapa {etapa}: el programa es demasiado lento"
            continue
        fo.seek(0); fe.seek(0); so = fo.read(); se = fe.read(); fo.close(); fe.close()
        if p.returncode != 0:
            err = (se or so or "")[-1500:]
            _anota(dict(sha=sha, etapa=etapa, seed=s, error=err, seg=round(time.time() - t0, 1)))
            error = error or ("el programa revento al correr:\\n" + err)
            continue
        d = json.loads(so.strip().splitlines()[-1]); d["sha"] = sha; d["etapa"] = etapa
        _anota(d); D.append(d)
    if error: return None, error
    return D, None


def _fv(d): return 1.0 - min(max(d["frac_vol"], 0.0), 1.0)


def _cria(d): return sum(1 for f, nb in zip(d["fund_post10k_l"], d["nac_reales_l"]) if f == 0 and nb >= NB2)


def _b2(d): return (0.4 * d["sin_extincion"] / d["n"] + 0.4 * _cria(d) / d["n"] + 0.2 * min(d["R0_real_med"], 1.0)) * _fv(d)


def _comida(d): return min(max(1.0 - d["frac_sin_bueno_mundo"] / 0.25, 0.0), 1.0)


def base_E(d):
    return (0.20 * d["persisten"] / d["n"] + 0.10 * min(d["R0_real_med"], 1.0) + (d["cruzan_real"] / d["n"]) * (0.45 + 0.25 * _comida(d))) * _fv(d)


def _med(xs): return float(sum(xs) / len(xs))


def _textos(D):
    if len(D) == 1 and BRAZO != "E": return _texto(D[0])
    cola = (lambda d: f"\\nescrituras de los 9 linajes en la pizarra publica: {d['escrituras']}") if BRAZO == "E" else (lambda d: "")
    if len(D) == 1: return _texto(D[0]) + cola(D[0])
    return "\\n\\n".join(f"CORRIDA {i + 1} de {len(D)} (cada corrida es un mundo distinto, con otro azar):\\n" + _texto(d) + cola(d) for i, d in enumerate(D))


'''

EV_ETAPAS = '''def evaluate_stage1(ruta):
    src = open(ruta, encoding="utf-8").read()
    v = _revisa(src)
    if v:
        sha = hashlib.sha256(src.encode("utf-8")).hexdigest()[:12]
        dprog = os.path.join(SAL, "programas_evaluados"); os.makedirs(dprog, exist_ok=True)
        with open(os.path.join(dprog, f"{sha}.py"), "w", encoding="utf-8") as fh: fh.write(src)
        _anota(dict(sha=sha, etapa=1, rechazado=v[:20]))
        return _res({"combined_score": 0.0, "etapa": 0.0}, {"rechazado_por_el_filtro_de_reglas": "\\n".join(v[:20])})
    D, err = _corre(ruta, 1)
    if D is None: return _res({"combined_score": 0.0, "etapa": 0.0}, {"fallo_etapa_1": err})
    return _res({"combined_score": 0.05, "etapa": 1.0, "vida_med": _med([float(d["vida_med"]) for d in D])}, {"etapa_1_corta": _textos(D)})


def evaluate_stage2(ruta):
    D, err = _corre(ruta, 2)
    if D is None: return _res({"combined_score": 0.0, "etapa": 1.0}, {"fallo_etapa_2": err})
    if BRAZO == "ORIGEN":
        d = D[0]
        b = (0.7 * d["sin_extincion"] / d["n"] + 0.3 * min(d["R0_real_med"], 1.0)) * (1.0 - min(max(d["frac_vol"], 0.0), 1.0))
        pasa = d["sin_extincion"] >= 5
    else:
        b = _med([_b2(d) for d in D]); pasa = sum(_cria(d) for d in D) >= 5 * len(D)
    m = {"combined_score": (0.20 if pasa else 0.05) + 0.10 * b, "etapa": 2.0, "persisten_frac": _med([d["persisten"] / 9 for d in D]),
         "sin_extincion_frac": _med([d["sin_extincion"] / 9 for d in D]),
         "cruzan_frac": _med([d["cruzan_real"] / 9 for d in D]), "R0_real_med": _med([float(d["R0_real_med"]) for d in D]),
         "vida_med": _med([float(d["vida_med"]) for d in D])}
    if BRAZO != "ORIGEN": m["crian_frac"] = _med([_cria(d) / 9 for d in D])
    return _res(m, {"etapa_2_media": _textos(D)})


def evaluate_stage3(ruta):
    D, err = _corre(ruta, 3)
    if D is None: return _res({"combined_score": 0.0, "etapa": 2.0}, {"fallo_etapa_3": err})
    if BRAZO == "E":
        bs = [base_E(d) for d in D]
        s = 0.30 + 0.70 * (0.7 * _med(bs) + 0.3 * min(bs)) - (0.02 if any(d["escrituras"] > 0 for d in D) else 0.0)
    else:
        s = 0.30 + 0.70 * _med([base(d) for d in D])
    m = {"combined_score": s, "etapa": 3.0, "persisten_frac": _med([d["persisten"] / 9 for d in D]),
         "cruzan_frac": _med([d["cruzan_real"] / 9 for d in D]), "R0_real_med": _med([float(d["R0_real_med"]) for d in D]),
         "vida_med": _med([float(d["vida_med"]) for d in D])}
    if BRAZO == "E": m["sin_bueno_frac"] = _med([float(d["frac_sin_bueno_mundo"]) for d in D])
    return _res(m, {"etapa_3_larga": _textos(D)})


def evaluate(ruta):
    """Sin cascada (no se usa): corre las tres etapas con las mismas reglas."""
    r1 = evaluate_stage1(ruta)
    if r1.metrics["combined_score"] < 0.04: return r1
    r2 = evaluate_stage2(ruta)
    if r2.metrics["combined_score"] < 0.20: return r2
    return evaluate_stage3(ruta)


if __name__ == "__main__":   # uso manual: python -B evaluador.py <programa.py>   (imprime el puntaje de cada etapa)
    for f in (evaluate_stage1, evaluate_stage2, evaluate_stage3):
        r = f(sys.argv[1]); print(f.__name__, r.metrics); print("   ", "\\n    ".join(str(x) for x in r.artifacts.values()))
        if r.metrics["combined_score"] < {"evaluate_stage1": 0.04, "evaluate_stage2": 0.20, "evaluate_stage3": 9}[f.__name__]: break
'''


def hace_evaluador():
    s = origen("evaluador", os.path.join(SER, "evaluador.py"))
    s = una(s, '"""evaluador.py', EV_CABECERA, "cabecera")
    s = tramo(s, '_S = [int(x) for x in os.environ["JUACO_OE_SEM"].split(",")]', "TT = {1: 5000, 2: 25000, 3: 100000}", EV_SEM + "\n\n", "semillas")
    s = una(s, '    v = list(RC.revisa_fuente(src, "candidato"))\n',
            '    v = list(RC.revisa_fuente(src, "candidato"))\n    if FILTRO_EXTRA: v += _extra(src)\n', "filtro extra")
    s = tramo(s, "def _corre(ruta, etapa):", "def _texto(d):", EV_CORRE, "_corre")
    s = tramo(s, "def evaluate_stage1(ruta):", None, EV_ETAPAS, "etapas")
    return s


# ------------------------------------------------------------------------------------------------------------------ lanza.py
def hace_lanza():
    s = origen("lanza", os.path.join(SER, "lanza.py"))
    s = una(s, '"""lanza.py —', '"""[CONSTRUIDO por construye_instrumento.py desde openevolve_serie/lanza.py 4402123932d74531; NO editar a mano]\n'
            'Unico cambio: el cliente es adaptador_libro (el adaptador ORIGINAL del humo, sin tocar, mas el libro de gasto).\n\nlanza.py —', "cabecera")
    s = una(s, "    import adaptador_claude as A\n", "    import adaptador_libro as A\n", "adaptador")
    return s


# ------------------------------------------------------------------------------------------------------------------- configs
OBJ_VIEJO = '''    El puntaje (FITNESS) crece con esas tres medidas. La evaluacion va por etapas: una corrida corta (si el programa falla,
    0), una media (25 000 pasos) y, solo si al menos 5 de 9 linajes pasan la media sin ninguna extincion despues del
    paso 10 000, una larga (100 000 pasos).
    Matar al propio cuerpo a proposito se penaliza. Despues de cada evaluacion veras un resumen fisico de lo que paso.
'''
OBJ_R = '''    El puntaje (FITNESS) crece con esas tres medidas. La evaluacion va por etapas: una corrida corta (si el programa falla,
    0), dos corridas medias (25 000 pasos, dos mundos distintos) y, solo si en promedio al menos 5 de 9 linajes pasan la
    media sin ninguna extincion despues del paso 10 000 Y con al menos 2 nacimientos reales cada uno, tres corridas largas
    (100 000 pasos, tres mundos distintos; el puntaje es el promedio). Un cuerpo que vive mucho pero no se reproduce NO
    pasa a la etapa larga.
    Matar al propio cuerpo a proposito se penaliza. Despues de cada evaluacion veras un resumen fisico de lo que paso.
'''
OBJ_E = '''    El puntaje (FITNESS) crece con esas tres medidas Y con que el mundo no se quede sin comida: en el resumen veras la
    "fraccion de pasos en que no habia en todo el mundo NINGUN objeto de los que suben una reserva". El programa actual
    ya persiste y cruza, pero deja el mundo sin nada bueno cerca de 0.24 del tiempo; se premia que crucen MAS linajes
    con esa fraccion cerca de 0 (por debajo de 0.05 es muy bueno; por encima de 0.25 no suma nada). Ese premio solo
    cuenta en proporcion a los linajes que cruzan: dejar de reproducirse para no gastar el mundo no sirve.
    La evaluacion va por etapas: una corrida corta (si el programa falla, 0), dos corridas medias (25 000 pasos, dos
    mundos distintos) y, solo si en promedio al menos 5 de 9 linajes pasan la media sin ninguna extincion despues del
    paso 10 000 Y con al menos 2 nacimientos reales cada uno, tres corridas largas (100 000 pasos, tres mundos
    distintos). El puntaje largo mezcla el promedio de las tres con la PEOR de las tres: un programa que solo va bien en
    un mundo vale poco. Escribir en la pizarra publica tiene un costo pequeno y fijo en el puntaje: usala solo si de
    verdad hace cruzar a mas linajes; si no aporta, quitala y deja el programa mas simple.
    Matar al propio cuerpo a proposito se penaliza. Despues de cada evaluacion veras un resumen fisico de lo que paso.
'''


def hace_config(brazo):
    s = origen("config", os.path.join(HUM, "config_humo.yaml"))
    rs, obj, que = {"R1": (45, OBJ_R, "BRAZO R, replica 1"), "R2": (47, OBJ_R, "BRAZO R, replica 2"), "E": (46, OBJ_E, "BRAZO E")}[brazo]
    s = una(s, "# Humo principal JUACO x OpenEvolve (5-oct-2026). Preregistro: PREREGISTRO_humo.md. Tope: 30 iteraciones.\n",
            f"# [CONSTRUIDO por construye_instrumento.py desde config_humo.yaml del 5-oct; NO editar a mano] {que}, local 6-oct-2026.\n"
            f"# Cambia SOLO: random_seed y el parrafo final de EL OBJETIVO (etapas con varias semillas y nacimientos reales"
            f"{'; objetivo del brazo E' if brazo == 'E' else ''}).\n", "cabecera")
    s = una(s, "random_seed: 42\n", f"random_seed: {rs}\n", "random_seed")
    s = una(s, OBJ_VIEJO, obj, "objetivo")
    return s


def main():
    chequea = "--check" in sys.argv
    if "LLENAR" in "".join(SHA.values()): raise SystemExit("faltan shas")
    sal = {
        "corre_carro.py": hace_corre_carro(), "evaluador.py": hace_evaluador(), "lanza.py": hace_lanza(),
        "adaptador_claude_ORIGINAL.py": origen("adaptador", os.path.join(HUM, "adaptador_claude.py")),
        "config_R1.yaml": hace_config("R1"), "config_R2.yaml": hace_config("R2"), "config_E.yaml": hace_config("E"),
        os.path.join("programas", "RAIZ.py"): origen("raiz", os.path.join(SER, "raiz", "programa_inicial.py")),
        os.path.join("programas", "HUMO.py"): origen("humo", os.path.join(SER, "examen", "programas", "HUMO.py")),
        os.path.join("programas", "INMORTAL_B.py"): origen("inmortal", os.path.join(SER, "examen", "programas", "MEJOR_B.py")),
    }
    mal = 0
    for nombre, txt in sal.items():
        dst = os.path.join(AQUI, nombre)
        if chequea:
            ok = os.path.exists(dst) and lee(dst) == txt; mal += not ok
            print(f"{'IGUAL   ' if ok else 'DISTINTO'} {nombre}  sha {h(txt)}")
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, "w", encoding="utf-8", newline="\n") as fh: fh.write(txt)
            print(f"ESCRITO  {nombre}  sha {h(txt)}")
    return 1 if mal else 0


if __name__ == "__main__":
    sys.exit(main())
