"""[CONSTRUIDO por construye_instrumento.py desde openevolve_serie/evaluador.py 6736985f4f42cdc5; NO editar a mano]
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

evaluador.py — evaluador de JUACO para OpenEvolve. Envuelve la pista y el juez SIN tocarlos (solo los lee por ruta).

PUNTAJE (preregistrado en PREREGISTRO_humo.md). Para una corrida (9 copias del programa, fundador NO limpio):
    base = [ 0.5 * (linajes que PERSISTEN / 9) + 0.4 * (linajes que CRUZAN con R0 real / 9) + 0.1 * min(mediana R0 real, 1) ]
           * (1 - fraccion de muertes voluntarias)
  persiste / cruza_real / R0_real / muertes_vol los calcula juez.resumen_linaje de la FISICA de la pista (ERR-96, ERR-99/100/102).
  El R0 solo pesa 0.1 (desempate): nunca decide.
CASCADA (cada etapa en SU proceso, una a la vez, con tiempo limite duro):
    etapa 1  filtro estatico (revisa_carro + regla de tabla) y T = 5 000, semilla 271001      -> 0.05 si corre; 0 si no
    etapa 2  T = 25 000, semilla 271002   -> base2 = [0.7 * (linajes SIN EXTINCION tras t = 10 000 / 9) + 0.3 * min(mediana R0 real, 1)]
                                              * (1 - fraccion de muertes voluntarias)
                                             0.05 + 0.10*base2 si sin extincion < 5/9;  0.20 + 0.10*base2 si >= 5/9
             (ENMIENDA de la cordura, antes del humo: a T 25 000 el "persiste" del juez exige >= 5 nacimientos reales y O1 de
              fabrica solo lo cumple en 2/9 aunque no se extingue ninguno; con esa puerta O1 no habria llegado a la etapa 3.)
    etapa 3  T = 100 000, semilla 271003  -> 0.30 + 0.70*base            (solo llegan los de >= 5/9 sin extincion en la etapa 2)
  Umbrales de OpenEvolve (cascade_thresholds): [0.04, 0.20].
Programa tramposo, que no pasa el filtro o que revienta -> puntaje 0 y el motivo en los artefactos.
Lo que vuelve al modelo (artefactos) es SOLO fisica: persistencia, cruce, R0, vida, causas de muerte, composicion del mundo.
NO vuelve ningun contador con nombre del mecanismo buscado.
"""
import hashlib, json, os, re, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
JUACO = os.path.dirname(os.path.dirname(AQUI))   # raiz del repo (serie nube 6-oct; el humo usaba ruta absoluta de Windows)
PISTA = os.path.join(JUACO, "experimentos", "carrera_escuderias")
CORRE = os.path.join(AQUI, "corre_carro.py")
SAL = os.environ.get("JUACO_OE_SALIDA", os.path.join(AQUI, "salida_sin_nombre"))
def _semillas():
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
EXTRA = [r"\bfabrica\b", r"\bPAT\b", r"\bEFECTO\b", r"\bVAL_VIVO\b", r"\bbit_generator\b", r"\bfromfile\b", r"\bmemmap\b",
         r"\bDataSource\b", r"\b(np|numpy)\s*\.\s*(load|loadtxt|genfromtxt|fromregex|lib|ctypeslib|core|testing|f2py)\b"]


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


TT = {1: 5000, 2: 25000, 3: 100000}
LIMITE = {1: 180, 2: 600, 3: 1800}      # segundos, tiempo limite duro por etapa
TABLA = re.compile(r"""['"][ABCD]['"]""")   # regla de tabla: el programa no puede nombrar letras del mundo (seria el oraculo)
MAX_LINEA = 400


def _revisa(src):
    """revisa_carro.revisa_fuente (del repo, sin tocar) + la regla de tabla. Devuelve la lista de violaciones."""
    sys.dont_write_bytecode = True
    if PISTA not in sys.path: sys.path.insert(0, PISTA)
    import revisa_carro as RC
    v = list(RC.revisa_fuente(src, "candidato"))
    if FILTRO_EXTRA: v += _extra(src)
    for n, linea in enumerate(src.splitlines(), 1):
        if TABLA.search(linea): v.append(f"TABLA candidato:{n} nombra una letra del mundo (prohibido: se aprende mordiendo): {linea.strip()[:80]}")
        if len(linea) > MAX_LINEA: v.append(f"LARGO candidato:{n} linea de mas de {MAX_LINEA} caracteres")
    return v


def base(d):
    b = 0.5 * d["persisten"] / d["n"] + 0.4 * d["cruzan_real"] / d["n"] + 0.1 * min(d["R0_real_med"], 1.0)
    return b * (1.0 - min(max(d["frac_vol"], 0.0), 1.0))


def _anota(reg):
    os.makedirs(SAL, exist_ok=True)
    with open(os.path.join(SAL, "evaluaciones.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(reg, ensure_ascii=False) + "\n")


def _corre(ruta, etapa):
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
            error = error or ("el programa revento al correr:\n" + err)
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
    cola = (lambda d: f"\nescrituras de los 9 linajes en la pizarra publica: {d['escrituras']}") if BRAZO == "E" else (lambda d: "")
    if len(D) == 1: return _texto(D[0]) + cola(D[0])
    return "\n\n".join(f"CORRIDA {i + 1} de {len(D)} (cada corrida es un mundo distinto, con otro azar):\n" + _texto(d) + cola(d) for i, d in enumerate(D))


def _texto(d):
    c = d["causas"]; m = d["comp_mundo"]
    return (f"T = {d['T']} pasos, 9 linajes con este mismo programa.\n"
            f"linajes sin ninguna extincion despues del paso 10000: {d['sin_extincion']}/9 · "
            f"linajes que persisten: {d['persisten']}/9 · linajes que cruzan (R0 real >= 0.9): {d['cruzan_real']}/9 · "
            f"R0 real por linaje: {d['R0_real']} (mediana {d['R0_real_med']})\n"
            f"vida mediana de un cuerpo: {d['vida_med']} pasos · muertes: {d['muertes']} · nacimientos reales: {d['nac_reales']} · "
            f"extinciones de linaje (fundadores puestos por el mundo): {d['fundadores']} (despues del paso 10000: {d['fund_post10k']})\n"
            f"causas de muerte: hambre {c['hambre']}, sed {c['sed']}, tras morder algo que baja E {c['veneno']}, tras morder algo que baja Ag {c['sal']} · "
            f"muertes causadas por la propia mordida: {d['muertes_vol']}\n"
            f"numero medio de objetos de cada letra presentes en el mundo (de 36): "
            + ", ".join(f"letra{i + 1} {m[k]:.1f}" for i, k in enumerate(sorted(m))) + "\n"
            f"fraccion de pasos en que no habia en todo el mundo NINGUN objeto de los que suben una reserva: {d['frac_sin_bueno_mundo']}\n"
            f"mordidas totales por letra: " + ", ".join(f"letra{i + 1} {d['mord'][k]}" for i, k in enumerate(sorted(d['mord']))))


def _res(metrics, artifacts):
    from openevolve.evaluation_result import EvaluationResult
    return EvaluationResult(metrics=metrics, artifacts=artifacts)


def evaluate_stage1(ruta):
    src = open(ruta, encoding="utf-8").read()
    v = _revisa(src)
    if v:
        sha = hashlib.sha256(src.encode("utf-8")).hexdigest()[:12]
        dprog = os.path.join(SAL, "programas_evaluados"); os.makedirs(dprog, exist_ok=True)
        with open(os.path.join(dprog, f"{sha}.py"), "w", encoding="utf-8") as fh: fh.write(src)
        _anota(dict(sha=sha, etapa=1, rechazado=v[:20]))
        return _res({"combined_score": 0.0, "etapa": 0.0}, {"rechazado_por_el_filtro_de_reglas": "\n".join(v[:20])})
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
        r = f(sys.argv[1]); print(f.__name__, r.metrics); print("   ", "\n    ".join(str(x) for x in r.artifacts.values()))
        if r.metrics["combined_score"] < {"evaluate_stage1": 0.04, "evaluate_stage2": 0.20, "evaluate_stage3": 9}[f.__name__]: break
