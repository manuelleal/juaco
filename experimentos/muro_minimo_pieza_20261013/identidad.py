"""identidad.py — ARNES DE IDENTIDAD del bloque MURO MINIMO PIEZA (13-oct-2026). UN proceso a la vez, sin Pool. Mision: llegar a la
AGI por este camino.

1. construye.py --check: todo el instrumento es igual a lo que sale de sus origenes (sha fijado) y de los parches de anclas.
2. Filtro de reglas (evaluador._revisa) sobre cada programa; diferencia en lineas de codigo de cada variante contra MINIMO.
3. Corridas cortas (T_ID pasos, semillas SEM_ID, fundador no limpio, 9 copias; todos los campos del JSON menos `seg`, incluido
   rng_mundo_estado, que resume toda la historia del mundo):
   a. MINIMO de esta carpeta (corre_carro.py copiado) == MINIMO del bloque anterior con SU corre_carro.py, bit a bit.
   b. cada variante con su llave en 0 (copia en identidad_tmp/) == MINIMO, bit a bit.            <- PUERTA (perillas apagadas)
   c. AUX_TODAS con las cuatro llaves en 0 == MINIMO.                                            <- PUERTA
   d. AUX_TODAS encendida == HUMO y AUX_TRES encendida == KO_PIZARRA, bit a bit.                 <- PUERTA (la lista de §2 es completa)
   e. (descriptivo) cada brazo encendido != MINIMO en la primera semilla: la pieza actua dentro de T_ID pasos.
Escribe identidad_salida.json. Sale con 1 si alguna puerta falla.

Uso:  python -B identidad.py            (todo)        python -B identidad.py --estatico   (pasos 1-2, sin corridas)
"""
import difflib, json, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
ANT = os.path.join(REPO, "experimentos", "muro_minimo_20261008")
os.environ.setdefault("JUACO_OE_SEM", "0,0,0")   # evaluador.py lo exige al importarse; solo se usa su filtro
sys.path.insert(0, AQUI)
import construye as C

PROG = os.path.join(AQUI, "programas")
TMP = os.path.join(AQUI, "identidad_tmp")
SAL = os.path.join(AQUI, "identidad_salida.json")
T_ID = 5000
SEM_ID = (884901, 884902, 884903)   # fuera de las selladas (884001-884040); la primera es tambien la del humo
BRAZOS_PIEZA = ["M_PIZARRA", "M_RADIO", "M_RECICLA", "M_URGENCIA"]


def codigo(txt):
    return [l.rstrip() for l in txt.splitlines() if l.strip() and not l.strip().startswith("#")]


def apaga(nombre):
    """copia de la variante con TODAS sus llaves en 0, escrita en identidad_tmp/ (ancla unica por llave)."""
    t = C.lf(os.path.join(PROG, nombre + ".py"))
    for p in C.VARIANTES[nombre]:
        a = f"{C.LLAVE[p]} = 1 "
        C.uno(t, a, f"llave {nombre}/{C.LLAVE[p]}")
        t = t.replace(a, f"{C.LLAVE[p]} = 0 ")
    os.makedirs(TMP, exist_ok=True)
    r = os.path.join(TMP, nombre + "_OFF.py")
    with open(r, "w", encoding="utf-8", newline="\n") as fh: fh.write(t)
    return r


CACHE = {}


def corre(etq, ruta_prog, seed, corre_carro=None, cwd=None):
    k = (etq, seed)
    if k in CACHE: return CACHE[k]
    cc = corre_carro or os.path.join(AQUI, "corre_carro.py")
    t0 = time.time()
    r = subprocess.run([sys.executable, "-B", cc, ruta_prog, str(seed), str(T_ID)], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", cwd=cwd or AQUI)
    if r.returncode != 0: raise SystemExit(f"{etq} s{seed} revento: {r.stderr[-800:]}")
    D = json.loads(r.stdout.strip().splitlines()[-1]); D["_pared"] = round(time.time() - t0, 1)
    CACHE[k] = D
    return D


def compara(A, B):
    campos = sorted((set(A) | set(B)) - {"seg", "_pared"})
    dif = [c for c in campos if A.get(c, "<falta>") != B.get(c, "<falta>")]
    return len(campos), dif


def main():
    out = dict(fecha=time.strftime("%Y-%m-%d %H:%M:%S"), python=sys.version.split()[0], T_ID=T_ID, semillas=list(SEM_ID))
    print(f"IDENTIDAD MURO MINIMO PIEZA {out['fecha']}  python {out['python']}  T_ID {T_ID}  semillas {SEM_ID}")
    mal = C.main(True)
    out["construye_check"] = "TODO IGUAL" if not mal else f"{mal} DIFERENCIAS"
    if mal: raise SystemExit("el instrumento no es igual a lo que sale de sus origenes: no se sigue")
    import evaluador as EV
    out["programas"] = {}
    M = codigo(C.lf(os.path.join(PROG, "MINIMO.py")))
    for n in ["MINIMO", "HUMO", "KO_PIZARRA"] + list(C.VARIANTES):
        src = C.lf(os.path.join(PROG, n + ".py")); v = EV._revisa(src)
        d = [l for l in difflib.unified_diff(M, codigo(src), lineterm="", n=0) if not l.startswith(("+++", "---", "@@"))]
        mas = sum(l.startswith("+") for l in d); menos = sum(l.startswith("-") for l in d)
        out["programas"][n] = dict(sha16=C.s16(src), filtro_pasa=not v, violaciones=v[:3], lineas_codigo=len(codigo(src)),
                                   vs_MINIMO=f"+{mas}/-{menos}")
        print(f"  {n:11s} sha16 {C.s16(src)}  filtro {'PASA' if not v else v[:2]}  lineas {len(codigo(src)):3d}  contra MINIMO +{mas}/-{menos}")
    if any(not x["filtro_pasa"] for x in out["programas"].values()): raise SystemExit("algun programa no pasa el filtro")
    sha_ant = C.s16(C.lf(os.path.join(ANT, "programas", "MINIMO.py")))
    out["MINIMO_texto_igual_bloque_anterior"] = sha_ant == out["programas"]["MINIMO"]["sha16"]
    print(f"  MINIMO de esta carpeta == MINIMO del bloque anterior (texto): {out['MINIMO_texto_igual_bloque_anterior']} (sha16 {sha_ant})")
    if "--estatico" in sys.argv:
        with open(SAL, "w", encoding="utf-8") as fh: json.dump(out, fh, indent=1, ensure_ascii=False)
        return 0
    checks = []

    def chk(nombre, puerta, A, B, seed, igual_esperado=True):
        nc, dif = compara(A, B)
        ok = (not dif) == igual_esperado
        checks.append(dict(check=nombre, semilla=seed, puerta=puerta, campos=nc, iguales=nc - len(dif), difieren=dif[:8],
                           cumple=ok, rng=[A["rng_mundo_estado"], B["rng_mundo_estado"]], cruzan=[A["cruzan_real"], B["cruzan_real"]],
                           nac=[A["nac_reales"], B["nac_reales"]], escrituras=[A["escrituras"], B["escrituras"]]))
        print(f"  [{time.strftime('%H:%M:%S')}] {'PUERTA' if puerta else 'descr.'} {nombre:34s} s{seed}: {nc - len(dif)}/{nc} iguales "
              f"{'-> IDENTICA' if not dif else '-> DIFIERE en ' + str(len(dif)) + ' campos'}  {'OK' if ok else 'FALLA'}  "
              f"rng {A['rng_mundo_estado']}|{B['rng_mundo_estado']}  nac {A['nac_reales']}|{B['nac_reales']}  "
              f"escr {A['escrituras']}|{B['escrituras']}", flush=True)
        with open(SAL, "w", encoding="utf-8") as fh: json.dump(dict(out, checks=checks), fh, indent=1, ensure_ascii=False)

    for s in SEM_ID:   # a
        A = corre("MINIMO", os.path.join(PROG, "MINIMO.py"), s)
        B = corre("MINIMO_ANT", os.path.join(ANT, "programas", "MINIMO.py"), s, os.path.join(ANT, "corre_carro.py"), ANT)
        chk("a MINIMO == MINIMO bloque anterior", True, A, B, s)
    for n in BRAZOS_PIEZA + ["AUX_TODAS"]:   # b, c
        r = apaga(n)
        for s in SEM_ID:
            chk(f"{'b' if n != 'AUX_TODAS' else 'c'} {n} llave 0 == MINIMO", True, corre(n + "_OFF", r, s), corre("MINIMO", None, s), s)
    for n, ref in (("AUX_TODAS", "HUMO"), ("AUX_TRES", "KO_PIZARRA")):   # d
        for s in SEM_ID:
            chk(f"d {n} encendida == {ref}", True, corre(n, os.path.join(PROG, n + ".py"), s), corre(ref, os.path.join(PROG, ref + ".py"), s), s)
    for n in BRAZOS_PIEZA:   # e
        s = SEM_ID[0]
        chk(f"e {n} encendida != MINIMO", False, corre(n, os.path.join(PROG, n + ".py"), s), corre("MINIMO", None, s), s, igual_esperado=False)
    puertas = [c for c in checks if c["puerta"]]
    ok = all(c["cumple"] for c in puertas)
    out.update(checks=checks, puertas_cumplen=f"{sum(c['cumple'] for c in puertas)}/{len(puertas)}",
               descriptivos_cumplen=f"{sum(c['cumple'] for c in checks if not c['puerta'])}/{len(checks) - len(puertas)}",
               corridas=len(CACHE), pasos_totales=len(CACHE) * T_ID, ARNES="PASA" if ok else "FALLA")
    with open(SAL, "w", encoding="utf-8") as fh: json.dump(out, fh, indent=1, ensure_ascii=False)
    print(f"IDENTIDAD: puertas {out['puertas_cumplen']} - descriptivos {out['descriptivos_cumplen']} - {len(CACHE)} corridas de {T_ID} pasos "
          f"- ARNES {out['ARNES']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
