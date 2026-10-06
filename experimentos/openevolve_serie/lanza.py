"""lanza.py — lanza OpenEvolve 0.4.0 con el CLI de Claude Code (sesion del director, sin clave) por el adaptador.

Uso:  python -B lanza.py <programa_inicial.py> <evaluador.py> <config.yaml> <carpeta_salida> <iteraciones> [tope_llamadas]
Un solo trabajador (parallel_evaluations: 1 en el YAML) -> una evaluacion a la vez.
"""
import asyncio, json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))


def main():
    prog, evalf, cfgf, sal, n = sys.argv[1], sys.argv[2], sys.argv[3], os.path.abspath(sys.argv[4]), int(sys.argv[5])
    tope = sys.argv[6] if len(sys.argv) > 6 else str(n + 5)   # tope duro de llamadas al modelo (iteraciones + margen de reintentos)
    os.makedirs(sal, exist_ok=True)
    os.environ["PYTHONPATH"] = AQUI + os.pathsep + os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["JUACO_OE_REGISTRO"] = os.path.join(sal, "registro_llm")
    os.environ["JUACO_OE_TOPE_LLAMADAS"] = tope
    os.environ["JUACO_OE_SALIDA"] = sal
    sys.path.insert(0, AQUI)
    import adaptador_claude as A
    from openevolve.config import load_config
    from openevolve.controller import OpenEvolve
    cfg = load_config(cfgf)
    for m in cfg.llm.models + cfg.llm.evaluator_models:
        m.init_client = A.init_client
    t0 = time.time()
    oe = OpenEvolve(os.path.abspath(prog), os.path.abspath(evalf), cfg, output_dir=sal)
    best = asyncio.run(oe.run(iterations=n))
    seg = round(time.time() - t0, 1)
    res = dict(segundos_reloj=seg, iteraciones=n, mejor_id=getattr(best, "id", None), mejor_metricas=getattr(best, "metrics", None))
    with open(os.path.join(sal, "fin.json"), "w", encoding="utf-8") as fh: json.dump(res, fh, ensure_ascii=False, indent=1)
    print("FIN", json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
