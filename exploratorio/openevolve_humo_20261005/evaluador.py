"""evaluador.py — evaluador de JUACO para OpenEvolve. Envuelve la pista y el juez SIN tocarlos (solo los lee por ruta).

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
JUACO = r"C:\Users\User\Documents\PROYECTOS\JUACO\organelos"
PISTA = os.path.join(JUACO, "experimentos", "carrera_escuderias")
CORRE = os.path.join(AQUI, "corre_carro.py")
SAL = os.environ.get("JUACO_OE_SALIDA", os.path.join(AQUI, "salida_sin_nombre"))
SEM = {1: 271001, 2: 271002, 3: 271003}
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
    """Una corrida en su proceso. Devuelve (dict | None, texto_de_error | None)."""
    src = open(ruta, encoding="utf-8").read(); sha = hashlib.sha256(src.encode("utf-8")).hexdigest()[:12]
    dprog = os.path.join(SAL, "programas_evaluados"); os.makedirs(dprog, exist_ok=True)
    copia = os.path.join(dprog, f"{sha}.py")
    if not os.path.exists(copia):
        with open(copia, "w", encoding="utf-8") as fh: fh.write(src)
    t0 = time.time()
    try:
        r = subprocess.run([sys.executable, "-B", CORRE, ruta, str(SEM[etapa]), str(TT[etapa])], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=LIMITE[etapa], cwd=AQUI)
    except subprocess.TimeoutExpired:
        _anota(dict(sha=sha, etapa=etapa, error="tiempo limite", seg=round(time.time() - t0, 1)))
        return None, f"tiempo limite ({LIMITE[etapa]} s) en la etapa {etapa}: el programa es demasiado lento"
    if r.returncode != 0:
        err = (r.stderr or r.stdout or "")[-1500:]
        _anota(dict(sha=sha, etapa=etapa, error=err, seg=round(time.time() - t0, 1)))
        return None, "el programa revento al correr:\n" + err
    d = json.loads(r.stdout.strip().splitlines()[-1]); d["sha"] = sha; d["etapa"] = etapa
    _anota(d)
    return d, None


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
    d, err = _corre(ruta, 1)
    if d is None: return _res({"combined_score": 0.0, "etapa": 0.0}, {"fallo_etapa_1": err})
    return _res({"combined_score": 0.05, "etapa": 1.0, "vida_med": float(d["vida_med"])}, {"etapa_1_corta": _texto(d)})


def evaluate_stage2(ruta):
    d, err = _corre(ruta, 2)
    if d is None: return _res({"combined_score": 0.0, "etapa": 1.0}, {"fallo_etapa_2": err})
    b = (0.7 * d["sin_extincion"] / d["n"] + 0.3 * min(d["R0_real_med"], 1.0)) * (1.0 - min(max(d["frac_vol"], 0.0), 1.0))
    pasa = d["sin_extincion"] >= 5
    return _res({"combined_score": (0.20 if pasa else 0.05) + 0.10 * b, "etapa": 2.0, "persisten_frac": d["persisten"] / 9,
                 "sin_extincion_frac": d["sin_extincion"] / 9,
                 "cruzan_frac": d["cruzan_real"] / 9, "R0_real_med": float(d["R0_real_med"]), "vida_med": float(d["vida_med"])},
                {"etapa_2_media": _texto(d)})


def evaluate_stage3(ruta):
    d, err = _corre(ruta, 3)
    if d is None: return _res({"combined_score": 0.0, "etapa": 2.0}, {"fallo_etapa_3": err})
    b = base(d)
    return _res({"combined_score": 0.30 + 0.70 * b, "etapa": 3.0, "persisten_frac": d["persisten"] / 9,
                 "cruzan_frac": d["cruzan_real"] / 9, "R0_real_med": float(d["R0_real_med"]), "vida_med": float(d["vida_med"])},
                {"etapa_3_larga": _texto(d)})


def evaluate(ruta):
    """Sin cascada (no se usa en el humo): corre las tres etapas con las mismas reglas."""
    r1 = evaluate_stage1(ruta)
    if r1.metrics["combined_score"] < 0.04: return r1
    r2 = evaluate_stage2(ruta)
    if r2.metrics["combined_score"] < 0.20: return r2
    return evaluate_stage3(ruta)


if __name__ == "__main__":   # uso manual: python -B evaluador.py <programa.py>   (imprime el puntaje de cada etapa)
    for f in (evaluate_stage1, evaluate_stage2, evaluate_stage3):
        r = f(sys.argv[1]); print(f.__name__, r.metrics); print("   ", "\n    ".join(str(x) for x in r.artifacts.values()))
        if r.metrics["combined_score"] < {"evaluate_stage1": 0.04, "evaluate_stage2": 0.20, "evaluate_stage3": 9}[f.__name__]: break
