"""corre_carro.py — UNA corrida de la pista de JUACO con 9 copias de un carro, en su propio proceso. SOLO LEE el repo JUACO.

Es la misma llamada que experimentos/tronco_v14_3/corre_v143.py::tarea (9 carros iguales, pizarra=1, rep_acum=0, escala=1,
mundo_n=None) y el mismo juez.resumen_linaje por linaje, con UNA diferencia pedida por el director: fundador_limpio = 0
(ERR-191: con fundador limpio la pista regala limpieza). La pista y el juez se importan por ruta; no se copian ni se tocan.
Se lanza con `python -B` para no escribir ni un .pyc dentro del repo.

Uso:  python -B corre_carro.py <ruta_del_carro.py | ID de carros/> <semilla> <T> [salida.json]
Imprime UNA linea JSON (ultima linea de la salida) con el resumen fisico.
"""
import importlib.util, json, os, statistics as st, sys, time

JUACO = r"C:\Users\User\Documents\PROYECTOS\JUACO\organelos"
PISTA = os.path.join(JUACO, "experimentos", "carrera_escuderias")
FL = 0   # fundador NO limpio (ERR-191)


def corre(ruta, seed, T):
    sys.dont_write_bytecode = True
    sys.path.insert(0, PISTA)
    import pista as P
    import juez as J
    if not os.path.exists(ruta): ruta = os.path.join(PISTA, "carros", ruta + ".py")
    spec = importlib.util.spec_from_file_location("carro_candidato", ruta)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    t0 = time.time()
    r = P.run(seed, [("C", mod)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=FL)
    L = [J.resumen_linaje(d, seed) for d in r["linajes"]]
    seg = round(time.time() - t0, 1)
    cz = {k: sum(l["causas"][k] for l in L) for k in ("hambre", "sed", "veneno", "sal")}
    mu = sum(l["muertes"] for l in L); mv = sum((l.get("muertes_vol") or 0) for l in L)
    dg = [l["diag"] for l in L if l.get("diag")]
    return dict(
        seed=seed, T=T, seg=seg, fundador_limpio=FL, n=len(L),
        persisten=sum(int(l["persiste"]) for l in L), cruzan_real=sum(int(l["cruza_real"]) for l in L),
        cruzan_letra=sum(int(l["cruza"]) for l in L), casi_inmortales=sum(int(l["casi_inmortal"]) for l in L),
        R0_real=[l["R0_real"] for l in L], R0_real_med=round(float(st.median([l["R0_real"] for l in L])), 4),
        vida_med=round(float(st.median([l["vida_med"] for l in L])), 1), muertes=mu, muertes_vol=mv,
        frac_vol=(round(mv / mu, 4) if mu else 0.0),
        fundadores=sum(l["fundadores"] for l in L), fund_post10k=sum(l["fund_post10k"] for l in L),
        sin_extincion=sum(int(l["fund_post10k"] == 0) for l in L),   # linajes con 0 fundadores despues de t = 10000
        fund_post10k_l=[l["fund_post10k"] for l in L], nac_reales_l=[l["nac_reales"] for l in L],
        nac_reales=sum(l["nac_reales"] for l in L), causas=cz,
        mord={k: sum(l["mord"][k] for l in L) for k in "ABCD"},
        escrituras=sum(l["escrituras"] for l in L), vetos=sum(l["vetos"] for l in L),
        coherente=sum(int(l["coherente"]) for l in L),
        frac_sin_bueno_mundo=r["pista"]["frac_sin_bueno_mundo"], comp_mundo=r["pista"]["comp_mundo"],
        comp_mundo_q=r["pista"]["comp_mundo_q"],
        # SOLO para el informe humano (NUNCA va al modelo): mordidas malas a sabiendas contadas por la pista
        limpiezas_fisicas=sum(d["limpiezas"] for d in dg), mordidas_malas=sum(d["mordidas_malas"] for d in dg),
        sha_pista=P.h16(os.path.join(PISTA, "pista.py")), sha_juez=P.h16(os.path.join(PISTA, "juez.py")),
        rng_mundo_estado=r["pista"]["rng_mundo_estado"])


if __name__ == "__main__":
    ruta, seed, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    out = corre(ruta, seed, T)
    txt = json.dumps(out, ensure_ascii=False)
    if len(sys.argv) > 4:
        with open(sys.argv[4], "w", encoding="utf-8") as fh: fh.write(txt)
    print(txt)
