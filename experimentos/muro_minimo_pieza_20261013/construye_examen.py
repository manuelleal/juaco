"""construye_examen.py — los REEMPLAZOS POR ANCLAS que llevan el corre_examen.py del bloque MURO MINIMO (sha d202bd621d2eb4ba) al de
este bloque. Lo usa construye.py (no se corre solo). Cada reemplazo es (texto viejo, texto nuevo); el viejo sale del ORIGEN por
`trozo(ini, fin)` (ini unico) o es literal, y construye.aplica exige que aparezca UNA vez. Lo que no se nombra aqui queda igual
byte a byte: `ruta`, `una` (la llamada a corre_carro.py, regla 14), el bucle de corridas, `guarda`, `anota`, el pool y el cierre.
"""
import os
import construye as C

V = C.origen(*C.ORIGEN_EXAMEN)

DOC = '''"""corre_examen.py — EXAMEN del bloque MURO MINIMO PIEZA (PREREGISTRO.md). 6 brazos x 20 semillas, T 100 000, fundador NO limpio
(ERR-191), corre_carro.py copiado del examen grande (pista y juez sin tocar). Construido por anclas (construye.py + construye_examen.py)
desde experimentos/muro_minimo_20261008/corre_examen.py (sha d202bd621d2eb4ba). Reanudable: salta los JSON que ya existen.
Log y resumen.json se escriben DESDE EL ARRANQUE y tras cada corrida. Antes de correr: construye --check, sha y filtro de cada
programa, y cotejo PREREGISTRO.md <-> PREREGISTRADO (coteja_preregistro.py copiado con sha fijado).

Uso (SOLO el coordinador usa --pool > 1):
  python -B corre_examen.py --serie --pool 3        (885001-885020)
  python -B corre_examen.py --replica --pool 3      (885021-885040)
  python -B corre_examen.py --combina               (lee las dos tandas y escribe examen/bloque.json con el veredicto del bloque)
  python -B corre_examen.py --humo [--desde 884901 --n 1 --T 20000 --brazos ...]   (humo de UN proceso; nunca semillas selladas)
"""
'''

CONST = '''BRAZOS = ["MINIMO", "M_PIZARRA", "M_RADIO", "M_RECICLA", "M_URGENCIA", "HUMO"]
PIEZAS = ["M_PIZARRA", "M_RADIO", "M_RECICLA", "M_URGENCIA"]   # un brazo por pieza de §2 del bloque anterior, en ese orden
SHAS = {"MINIMO": "b9cfbb3bb7cb", "M_PIZARRA": "@M_PIZARRA@", "M_RADIO": "@M_RADIO@", "M_RECICLA": "@M_RECICLA@",
        "M_URGENCIA": "@M_URGENCIA@", "HUMO": "69fcfcb2473f"}   # sha12 texto LF (los de las variantes los imprime construye.py)
SERIE = range(885001, 885021)
REPLICA = range(885021, 885041)
SELLADAS = range(SERIE.start, REPLICA.stop)
N_LETRA = 20
T_LETRA = 100000
MAY = 5               # semilla "con mayoria": cruzan_real >= 5 de 9 (cruza_real del juez: R0 real >= 0.90 y 0 fundadores tras t = 10 000)
CIERRA_MIN = 15       # una pieza CIERRA la brecha: su brazo con mayoria en >= 15/20
MUEVE_LIN = 20        # una pieza MUEVE: suma de linajes que cruzan del brazo >= la de MINIMO + 20 (misma tanda, mismas semillas)
C1_MINIMO_MAX = 14    # control bajo que puede fallar: MINIMO con mayoria en <= 14/20 (si cruza, no hay brecha que cerrar)
V_HUMO_MIN = 15       # control alto (validez): HUMO con mayoria en >= 15/20
HUMO_SEMILLA = 884901
HUMO_T = 20000
CAMPOS = ("persisten", "cruzan_real", "R0_real_med", "vida_med", "fund_post10k", "muertes", "nac_reales", "mordidas_malas",
          "limpiezas_fisicas", "frac_sin_bueno_mundo", "escrituras", "causas", "mord", "seg")
PREREGISTRADO = dict(BRAZOS=BRAZOS, PIEZAS=PIEZAS, SHAS=SHAS, SERIE=SERIE, REPLICA=REPLICA, N_LETRA=N_LETRA, T_LETRA=T_LETRA, MAY=MAY,
                     CIERRA_MIN=CIERRA_MIN, MUEVE_LIN=MUEVE_LIN, C1_MINIMO_MAX=C1_MINIMO_MAX, V_HUMO_MIN=V_HUMO_MIN,
                     HUMO_SEMILLA=HUMO_SEMILLA, HUMO_T=HUMO_T)'''

LETRA = '''def letra(R, semillas, brazos):
    """La letra de PREREGISTRO.md §5 para UNA tanda. Si falta algun brazo o corrida, V1 cae y el veredicto es NO SE LEE."""
    c = {k: d["cruzan_real"] for k, d in R.items()}
    tiene = {n: [s for s in semillas if (n, s) in c] for n in brazos}
    may = {n: sum(c[(n, s)] >= MAY for s in tiene[n]) for n in brazos}
    suma = {n: sum(c[(n, s)] for s in tiene[n]) for n in brazos}
    med = {n: {x: (round(float(st.median([R[(n, s)][x] for s in tiene[n]])), 4) if tiene[n] else None)
               for x in ("R0_real_med", "vida_med", "muertes", "mordidas_malas", "limpiezas_fisicas", "frac_sin_bueno_mundo", "fund_post10k")}
           for n in brazos}
    out = dict(mayoria=may, suma_cruzan=suma, medianas=med, n_semillas=len(semillas))
    completa = set(brazos) == set(BRAZOS) and len(semillas) == N_LETRA and len(R) == len(BRAZOS) * len(semillas)
    if not completa:
        out.update(validez=dict(V1_completa=False), veredicto="NO SE LEE"); return out
    par = lambda a, b: dict(gana=sum(c[(a, s)] > c[(b, s)] for s in semillas), pierde=sum(c[(a, s)] < c[(b, s)] for s in semillas))
    v = dict(V1_completa=True, V2_shas_filtro_cotejo=True, V3_HUMO_cruza=may["HUMO"] >= V_HUMO_MIN)
    ctrl = dict(C1_MINIMO_no_cruza=may["MINIMO"] <= C1_MINIMO_MAX)
    pz = {}
    for n in PIEZAS:
        dl = suma[n] - suma["MINIMO"]; ci = may[n] >= CIERRA_MIN; mu = dl >= MUEVE_LIN
        pz[n] = dict(mayoria=may[n], linajes=suma[n], dif_linajes_vs_MINIMO=dl, cierra=ci, mueve=mu,
                     estado="CIERRA" if ci else ("MUEVE" if mu else "NADA"), vs_MINIMO=par(n, "MINIMO"), vs_HUMO=par(n, "HUMO"),
                     frac_linajes_de_HUMO=(round(suma[n] / suma["HUMO"], 4) if suma["HUMO"] else 0.0))
    if not all(v.values()) or not all(ctrl.values()): ver = "NO SE LEE"
    elif any(p["cierra"] for p in pz.values()): ver = "FUNCIONA"
    elif any(p["mueve"] for p in pz.values()): ver = "HAY ALGO MODESTO"
    else: ver = "NO"
    out.update(validez=v, control=ctrl, piezas=pz, cierran=[n for n in PIEZAS if pz[n]["estado"] == "CIERRA"],
               mueven=[n for n in PIEZAS if pz[n]["estado"] == "MUEVE"], descriptivo=dict(MINIMO_vs_HUMO=par("MINIMO", "HUMO")),
               veredicto=ver)
    return out


def combina():
    """El bloque (PREREGISTRO.md §5): una pieza vale lo MENOR de sus dos estados; el bloque se lee de las piezas, no de las tandas."""
    est = {"NADA": 0, "MUEVE": 1, "CIERRA": 2}
    L = {}
    for nom, t in (("serie", SERIE), ("replica", REPLICA)):
        f = os.path.join(AQUI, "examen", f"s{t.start}-{t.stop - 1}", "resumen.json")
        if not os.path.exists(f): raise SystemExit(f"--combina: falta {f}")
        d = json.load(open(f, encoding="utf-8"))
        if not d.get("terminado"): raise SystemExit(f"--combina: {f} no termino")
        L[nom] = d["letra"]
    out = dict(veredicto_serie=L["serie"]["veredicto"], veredicto_replica=L["replica"]["veredicto"], piezas={})
    if "NO SE LEE" in (out["veredicto_serie"], out["veredicto_replica"]):
        out["veredicto_bloque"] = "NO SE LEE"
    else:
        for n in PIEZAS:
            e = [L[k]["piezas"][n]["estado"] for k in ("serie", "replica")]
            out["piezas"][n] = dict(serie=e[0], replica=e[1], bloque=min(e, key=lambda x: est[x]),
                                    mayoria=[L[k]["piezas"][n]["mayoria"] for k in ("serie", "replica")],
                                    linajes=[L[k]["piezas"][n]["linajes"] for k in ("serie", "replica")])
        b = [p["bloque"] for p in out["piezas"].values()]
        out["cierran_x2"] = [n for n in PIEZAS if out["piezas"][n]["bloque"] == "CIERRA"]
        out["mueven_x2"] = [n for n in PIEZAS if out["piezas"][n]["bloque"] == "MUEVE"]
        out["veredicto_bloque"] = "FUNCIONA" if "CIERRA" in b else ("HAY ALGO MODESTO" if "MUEVE" in b else "NO")
    with open(os.path.join(AQUI, "examen", "bloque.json"), "w", encoding="utf-8") as fh: json.dump(out, fh, indent=1, ensure_ascii=False)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"VEREDICTO DEL BLOQUE: {out['veredicto_bloque']}")'''

ARGS = '''    ap.add_argument("--desde", type=int, default=None); ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--pool", type=int, default=1); ap.add_argument("--humo", action="store_true")
    ap.add_argument("--serie", action="store_true"); ap.add_argument("--replica", action="store_true")
    ap.add_argument("--combina", action="store_true")
    ap.add_argument("--brazos", default=",".join(BRAZOS)); ap.add_argument("--T", type=int, default=None)
    a = ap.parse_args()
    if a.combina: return combina()
    if a.humo + a.serie + a.replica != 1: raise SystemExit("elige UNO: --humo, --serie o --replica (o --combina)")
    brazos = a.brazos.split(",")
    if any(b not in BRAZOS for b in brazos): raise SystemExit(f"--brazos: solo {BRAZOS}")
    if a.humo:
        a.desde = HUMO_SEMILLA if a.desde is None else a.desde; a.n = 1 if a.n is None else a.n; a.T = HUMO_T if a.T is None else a.T
        semillas = list(range(a.desde, a.desde + a.n))
        if any(s in SELLADAS for s in semillas): raise SystemExit(f"--humo no puede tocar las semillas selladas {SELLADAS.start}-{SELLADAS.stop - 1}")
        if a.pool != 1: raise SystemExit("--humo es de UN proceso (--pool 1)")
        if a.T > 200000 or len(semillas) * len(brazos) > 6: raise SystemExit("--humo: regla 3 de EQUIPO (<= 6 corridas, <= 200 000 pasos cada una)")
        dest = os.path.join(AQUI, "humo", f"s{semillas[0]}-{semillas[-1]}_T{a.T}")
    else:
        tanda = SERIE if a.serie else REPLICA
        if a.desde not in (None, tanda.start) or a.n not in (None, N_LETRA) or a.T not in (None, T_LETRA) or brazos != BRAZOS:
            raise SystemExit(f"sin --humo: las {N_LETRA} semillas de la tanda, T {T_LETRA} y los {len(BRAZOS)} brazos (preregistro)")
        semillas = list(tanda); a.T = T_LETRA
        dest = os.path.join(AQUI, "examen", f"s{semillas[0]}-{semillas[-1]}")
'''

CABECERA = '''    di(f"MURO MINIMO PIEZA {'HUMO-DE-RUNNER' if a.humo else ('SERIE' if a.serie else 'REPLICA')} {time.strftime('%Y-%m-%d %H:%M:%S')} - "
       f"semillas {semillas[0]}-{semillas[-1]} - T {a.T} - fundador no limpio - pool {a.pool} - brazos {brazos} - "
       f"corre_examen.py {hashlib.sha256(open(__file__, 'rb').read()).hexdigest()[:16]}")
    if C.main(True): raise SystemExit("construye.py --check: el instrumento no es igual a su origen: no se corre")
    for n, sh in SHAS.items():
        src = C.lf(os.path.join(PROG, n + ".py")); s2 = C.s16(src)[:12]; v = EV._revisa(src)
        di(f"  {n}: sha {s2} - filtro {'PASA' if not v else v[:2]}")
        if s2 != sh or v: raise SystemExit(f"{n}: sha o filtro no coinciden con el preregistro: no se corre")
    filas, difs = CP.coteja(os.path.join(AQUI, "PREREGISTRO.md"), PREREGISTRADO)
    di(f"  cotejo PREREGISTRO.md <-> PREREGISTRADO: {len(filas)} nombres - " + ("TODO IGUAL" if not difs else f"{len(difs)} DIFERENCIAS {difs[:3]}"))
    if difs: raise SystemExit("cotejo preregistro <-> runner con diferencias: no se corre")
'''


def reemplazos(shas12):
    const = CONST
    for n, h in shas12.items(): const = const.replace(f"@{n}@", h)
    if "@" in const: raise SystemExit("construye_examen: falta el sha de alguna variante")
    return [
        (C.trozo(V, '"""corre_examen.py', "import argparse", "doc"), DOC),
        ("import construye as C\nimport evaluador as EV\n", "import construye as C\nimport evaluador as EV\nimport coteja_preregistro as CP\n"),
        (C.trozo(V, "BRAZOS = [", "\n\n\ndef ruta(nom):", "constantes"), const),
        (C.trozo(V, "def letra(R, semillas, brazos):", "\n\n\ndef main():", "letra"), LETRA),
        (C.trozo(V, '    ap.add_argument("--desde", type=int, required=True)', "    os.makedirs(dest, exist_ok=True)\n", "args"), ARGS),
        (C.trozo(V, '    di(f"MURO MINIMO {', "    t0 = time.time(); R = {}\n", "cabecera"), CABECERA),
    ]
