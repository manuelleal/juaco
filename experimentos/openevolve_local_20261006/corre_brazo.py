"""corre_brazo.py — lanza UN brazo de la busqueda local del 6-oct-2026 (PREREGISTRO_R.md, PREREGISTRO_E.md).

Mision: llegar a la AGI por este camino. Evolucion de PROGRAMAS guiada por un modelo de lenguaje sobre un juez fijo (no es seleccion natural).

Uso (con el python del venv de JUACO-OPENEVOLVE):
  python -B corre_brazo.py R1 --humo            humo de tuberia: 1 iteracion, semillas de practica, una corrida de pista a la vez.
                                                 Escribe corridas/HUMO_TUBERIA_R1/verificacion.json (proponente >= 10 000 tokens de salida).
  python -B corre_brazo.py R1 --desacoplado     LA SERIE (30 iteraciones) como proceso suelto que sobrevive a la consola:
                                                 log en corridas/R1.log, pid en corridas/R1.pid. Sin --desacoplado corre en primer plano.
  Brazos: R1 (replica 1 desde la raiz), R2 (replica 2 desde la raiz), E (evolucionar a HUMO).
La serie NO arranca si el humo de tuberia de R1 no dejo verificacion.json con pasa = true (ERR-194), ni si la carpeta de salida ya existe.
"""
import hashlib, json, os, statistics as st, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
ITER = 30; TOPE_LLAMADAS = 33; MIN_TOKENS = 10000
BRAZOS = {
    "R1": dict(config="config_R1.yaml", programa=os.path.join("programas", "RAIZ.py"), brazo="R",
               sem="281101;281111,281112;281121,281122,281123", sem_humo="281901,281902,281903"),
    "R2": dict(config="config_R2.yaml", programa=os.path.join("programas", "RAIZ.py"), brazo="R",
               sem="281301;281311,281312;281321,281322,281323", sem_humo="281921,281922,281923"),
    "E": dict(config="config_E.yaml", programa=os.path.join("programas", "HUMO.py"), brazo="E",
              sem="281201;281211,281212;281221,281222,281223", sem_humo="281911,281912,281913"),
}


def h16(p):
    return hashlib.sha256(open(p, "rb").read().replace(b"\r\n", b"\n")).hexdigest()[:16]


def llamadas(sal):
    p = os.path.join(sal, "registro_llm", "llamadas.jsonl")
    if not os.path.exists(p): return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def main():
    a = sys.argv[1:]
    if not a or a[0] not in BRAZOS: raise SystemExit(__doc__)
    nom = a[0]; B = BRAZOS[nom]; humo = "--humo" in a
    corr = os.path.join(AQUI, "corridas"); os.makedirs(corr, exist_ok=True)
    etiqueta = f"HUMO_TUBERIA_{nom}" if humo else nom
    sal = os.path.join(corr, etiqueta); log = os.path.join(corr, etiqueta + ".log")
    if os.path.exists(sal) and "--hijo" not in a: raise SystemExit(f"ya existe {sal}: no se pisa una corrida (apartala a mano si era un intento fallido)")
    if not humo:
        v = os.path.join(corr, "HUMO_TUBERIA_R1", "verificacion.json")
        if not (os.path.exists(v) and json.load(open(v, encoding="utf-8")).get("pasa")):
            raise SystemExit("ERR-194: falta corridas/HUMO_TUBERIA_R1/verificacion.json con pasa = true (proponente >= 10 000 tokens). No se lanza la serie.")
    if "--desacoplado" in a:
        os.makedirs(sal, exist_ok=True)
        fl = open(log, "a", encoding="utf-8")
        banderas = 0x00000008 | 0x00000200 | 0x01000000 if os.name == "nt" else 0   # DETACHED_PROCESS | NEW_PROCESS_GROUP | BREAKAWAY_FROM_JOB
        args = [PY, "-B", os.path.abspath(__file__), nom, "--hijo"] + (["--humo"] if humo else []) + (["--tras", a[a.index("--tras") + 1]] if "--tras" in a else [])
        try: p = subprocess.Popen(args, stdout=fl, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=AQUI, creationflags=banderas, close_fds=True)
        except OSError: p = subprocess.Popen(args, stdout=fl, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=AQUI, creationflags=banderas & ~0x01000000, close_fds=True)
        with open(os.path.join(corr, etiqueta + ".pid"), "w") as fh: fh.write(str(p.pid))
        print(f"LANZADO {etiqueta}  pid {p.pid}  log {log}")
        return 0
    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", JUACO_OE_BRAZO=B["brazo"], JUACO_OE_CORRIDA=etiqueta,
               JUACO_OE_SEM=(B["sem_humo"] if humo else B["sem"]), JUACO_OE_SERIAL=("1" if humo else "0"),
               JUACO_OE_LIBRO=os.path.join(AQUI, "gasto", "libro_gasto.jsonl"), JUACO_OE_TOPE_USD=os.environ.get("JUACO_OE_TOPE_USD", "40"))
    for k in ("JUACO_OE_CTX_LIMPIO", "JUACO_OE_MOD_POR_LINAJE", "JUACO_OE_FILTRO_EXTRA"): env.pop(k, None)   # perillas en su valor por defecto: encendidas
    n = 1 if humo else ITER; tope = 2 if humo else TOPE_LLAMADAS
    if "--tras" in a:   # encadenado: espera (sin gastar CPU) a que el otro brazo escriba FIN_BRAZO en su log
        otro = os.path.join(corr, a[a.index("--tras") + 1] + ".log")
        print(f"ESPERANDO a que termine {otro}  {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
        while not (os.path.exists(otro) and "FIN_BRAZO" in open(otro, encoding="utf-8", errors="replace").read()): time.sleep(60)

    def di(s):
        print(s, flush=True)
    vivos = subprocess.run("tasklist /FI \"IMAGENAME eq python.exe\" /NH" if os.name == "nt" else "pgrep -c python", shell=True, capture_output=True, text=True).stdout
    di(f"BRAZO {etiqueta}  {time.strftime('%Y-%m-%d %H:%M:%S')}  pid {os.getpid()}  iteraciones {n}  tope de llamadas {tope}  tope USD equiv {env['JUACO_OE_TOPE_USD']}")
    di(f"  semillas (etapa1;etapa2;etapa3) {env['JUACO_OE_SEM']}  brazo de puntaje {B['brazo']}  programa inicial {B['programa']} ({h16(os.path.join(AQUI, B['programa']))})")
    di("  shas: " + " ".join(f"{f} {h16(os.path.join(AQUI, f))}" for f in ("evaluador.py", "corre_carro.py", "lanza.py", "adaptador_libro.py", B["config"])))
    di(f"  CLAUDE_EFFORT del entorno: {os.environ.get('CLAUDE_EFFORT')}  python vivos al arrancar: {vivos.count('python')}")
    t0 = time.time()
    r = subprocess.run([PY, "-B", os.path.join(AQUI, "lanza.py"), os.path.join(AQUI, B["programa"]), os.path.join(AQUI, "evaluador.py"),
                        os.path.join(AQUI, B["config"]), sal, str(n), str(tope)], env=env, cwd=AQUI)
    L = llamadas(sal); tok = [x["tokens_salida"] for x in L if x.get("tokens_salida")]
    res = dict(brazo=etiqueta, codigo=r.returncode, segundos=round(time.time() - t0, 1), llamadas=len(L), llamadas_con_respuesta=len(tok),
               tokens_salida=tok, tokens_salida_mediana=(st.median(tok) if tok else None), modelos=sorted({m for x in L for m in (x.get("modelos") or [])}),
               usd_equiv=round(sum((x.get("costo_usd_equiv") or 0) for x in L), 4), errores=[(x.get("error") or "")[:200] for x in L if x.get("error")])
    if humo:
        res["minimo_exigido"] = MIN_TOKENS; res["pasa"] = bool(tok) and min(tok) >= MIN_TOKENS and r.returncode == 0
        with open(os.path.join(sal, "verificacion.json"), "w", encoding="utf-8") as fh: json.dump(res, fh, ensure_ascii=False, indent=1)
        di(f"VERIFICACION_PROPONENTE {etiqueta}: tokens de salida {tok} (minimo {MIN_TOKENS}) modelos {res['modelos']} -> {'PASA' if res['pasa'] else 'NO PASA'}")
    di(f"FIN_BRAZO {json.dumps(res, ensure_ascii=False)}")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
