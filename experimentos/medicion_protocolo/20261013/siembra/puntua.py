"""Puntaje de la medicion del protocolo (PREREGISTRO.md de esta carpeta madre, seccion Puntaje y Metricas).

Uso:
    python puntua.py RUTA/CLAVE.csv RUTA/HALLAZGOS.csv [--tabla salida.csv]

CLAVE.csv     : copia,tiene_defecto,tipo,archivo,linea,descripcion   (una fila por copia; limpias con tipo vacio)
HALLAZGOS.csv : copia,defecto,tipo,archivo,linea,descripcion,dato_que_confirma,confianza,argumento_contrario
                (cero o mas filas por copia)

Reglas, tal cual el preregistro:
- ACIERTO: copia con defecto que tiene al menos una fila de HALLAZGOS con defecto=si cuyo `archivo` coincide, por
  nombre base, con el `archivo` de la clave. No se exige linea ni tipo.
- FALSA ALARMA: copia limpia con alguna fila defecto=si de confianza alta o media.
- Sensibilidad total y por tipo (criterio, instrumento, lectura/otro) con intervalo de Wilson al 95 %.
- Tasa de falsas alarmas sobre las limpias.
El tiempo del auditor por copia no esta en HALLAZGOS: se lee de sus notas, fuera de este script.

Antes de puntuar comprueba el sha256 de CLAVE.csv contra CLAVE.sha256 (junto a este script) y avisa si no coincide.
"""
import csv, hashlib, math, os, re, sys, unicodedata

Z95 = 1.959963984540054
TIPOS = ("criterio", "instrumento", "lectura")


def sin_tildes(s):
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn").strip().lower()


def norm_copia(s):
    m = re.search(r"(\d+)", s or "")
    return f"c{int(m.group(1)):02d}" if m else (s or "").strip().lower()


def norm_si(s):
    return sin_tildes(s) in ("si", "s", "yes", "y", "true", "1")


def norm_tipo(s):
    t = sin_tildes(s)
    if t.startswith("crit"):
        return "criterio"
    if t.startswith("instr"):
        return "instrumento"
    if t.startswith("lect") or t.startswith("otro") or t == "lectura/otro":
        return "lectura"
    return t


def base(ruta):
    return os.path.basename((ruta or "").strip().replace("\\", "/")).lower()


def wilson(k, n, z=Z95):
    if n == 0:
        return (None, None, None)
    p = k / n
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    medio = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (p, max(0.0, centro - medio), min(1.0, centro + medio))


def fmt(t):
    p, lo, hi = t
    return "sin datos" if p is None else f"{p:.3f} [{lo:.3f}, {hi:.3f}]"


def lee(ruta):
    with open(ruta, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main(argv):
    args = list(argv[1:])
    salida = None
    if "--tabla" in args:
        i = args.index("--tabla")
        if i + 1 >= len(args):
            print(__doc__); return 2
        salida = args[i + 1]
        del args[i:i + 2]
    pos = [a for a in args if not a.startswith("--")]
    if len(pos) != 2:
        print(__doc__); return 2
    r_clave, r_hall = pos

    sello = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CLAVE.sha256")
    real = hashlib.sha256(open(r_clave, "rb").read()).hexdigest()
    if os.path.exists(sello):
        esperado = open(sello, encoding="utf-8").read().split()[0].strip().lower()
        print(f"sha256(CLAVE.csv) = {real}  ->  {'COINCIDE con CLAVE.sha256' if real == esperado else '*** NO COINCIDE con CLAVE.sha256 (' + esperado + ') ***'}")
    else:
        print(f"sha256(CLAVE.csv) = {real}  (no se encontro CLAVE.sha256 para comparar)")

    clave = {}
    for r in lee(r_clave):
        c = norm_copia(r["copia"])
        clave[c] = dict(defecto=norm_si(r["tiene_defecto"]), tipo=norm_tipo(r.get("tipo")), archivo=base(r.get("archivo")),
                        linea=(r.get("linea") or "").strip(), desc=(r.get("descripcion") or "").strip())
    hall = {}
    ajenas = set()
    for r in lee(r_hall):
        c = norm_copia(r.get("copia"))
        if c not in clave:
            ajenas.add(r.get("copia")); continue
        hall.setdefault(c, []).append(dict(defecto=norm_si(r.get("defecto")), archivo=base(r.get("archivo")),
                                           linea=(r.get("linea") or "").strip(), tipo=norm_tipo(r.get("tipo")),
                                           confianza=sin_tildes(r.get("confianza"))))
    if ajenas:
        print(f"AVISO: filas de HALLAZGOS con copias que no estan en la clave (ignoradas): {sorted(ajenas)}")
    sin_fila = sorted(c for c in clave if c not in hall)
    if sin_fila:
        print(f"AVISO: copias sin ninguna fila en HALLAZGOS ({len(sin_fila)}): {' '.join(sin_fila)}")

    tabla = []
    for c in sorted(clave):
        k = clave[c]; filas = hall.get(c, [])
        pos_ = [f for f in filas if f["defecto"]]
        if k["defecto"]:
            acierta = any(f["archivo"] and f["archivo"] == k["archivo"] for f in pos_)
            linea_ok = any(f["archivo"] == k["archivo"] and f["linea"] and f["linea"] == k["linea"] for f in pos_)
            res = "ACIERTO" if acierta else "FALLO"
            fa = False
        else:
            acierta = linea_ok = None
            fa = any(f["confianza"] in ("alta", "media") for f in pos_)
            res = "FALSA ALARMA" if fa else ("limpia, sin alarma" if not pos_ else "limpia, alarma de confianza baja")
        tabla.append(dict(copia=c, tiene_defecto="si" if k["defecto"] else "no", tipo=k["tipo"], archivo_clave=k["archivo"],
                          linea_clave=k["linea"], filas_auditor=len(filas), filas_defecto_si=len(pos_),
                          archivos_auditor=";".join(sorted({f["archivo"] for f in pos_ if f["archivo"]})),
                          resultado=res, misma_linea=("" if linea_ok is None else ("si" if linea_ok else "no"))))

    con = [t for t in tabla if t["tiene_defecto"] == "si"]
    limpias = [t for t in tabla if t["tiene_defecto"] == "no"]
    aciertos = sum(t["resultado"] == "ACIERTO" for t in con)
    fas = sum(t["resultado"] == "FALSA ALARMA" for t in limpias)

    print()
    print(f"Copias: {len(tabla)}  (con defecto {len(con)}, limpias {len(limpias)})")
    print()
    print("| medida | aciertos / n | proporcion [Wilson 95 %] |")
    print("|---|---|---|")
    sens = {}
    print(f"| sensibilidad total | {aciertos}/{len(con)} | {fmt(wilson(aciertos, len(con)))} |")
    for t in TIPOS:
        g = [x for x in con if x["tipo"] == t]
        a = sum(x["resultado"] == "ACIERTO" for x in g)
        sens[t] = (a, len(g))
        print(f"| sensibilidad {t if t != 'lectura' else 'lectura/otro'} | {a}/{len(g)} | {fmt(wilson(a, len(g)))} |")
    otros = sorted({x["tipo"] for x in con} - set(TIPOS))
    if otros:
        print(f"AVISO: tipos en la clave fuera de {TIPOS}: {otros}")
    print(f"| falsas alarmas (limpias con defecto=si de confianza alta o media) | {fas}/{len(limpias)} | {fmt(wilson(fas, len(limpias)))} |")
    misma = sum(t["misma_linea"] == "si" for t in con)
    print(f"| (descriptivo) aciertos que ademas dan la misma linea | {misma}/{len(con)} | |")

    print()
    print("Tabla copia a copia")
    print()
    print("| copia | defecto | tipo | archivo (clave) | linea | filas | defecto=si | archivos del auditor | resultado |")
    print("|---|---|---|---|---|---|---|---|---|")
    for t in tabla:
        print(f"| {t['copia']} | {t['tiene_defecto']} | {t['tipo']} | {t['archivo_clave']} | {t['linea_clave']} | {t['filas_auditor']} | "
              f"{t['filas_defecto_si']} | {t['archivos_auditor']} | {t['resultado']} |")

    # criterios de decision del preregistro, evaluados mecanicamente (la declaracion la hace quien corresponda)
    st = aciertos / len(con) if con else float("nan")
    print()
    print("Umbrales del preregistro, evaluados sin interpretar:")
    a, n = sens["instrumento"]
    print(f"- sensibilidad en instrumento < 0.50: {'SI' if n and a / n < 0.50 else 'no'} ({a}/{n})")
    print(f"- falsas alarmas > 5 de {len(limpias)}: {'SI' if fas > 5 else 'no'} ({fas})")
    print(f"- sensibilidad total < 0.30: {'SI' if st < 0.30 else 'no'} ({aciertos}/{len(con)})")
    todos70 = all(n_ and a_ / n_ >= 0.70 for a_, n_ in sens.values())
    print(f"- >= 0.70 en todos los tipos y falsas alarmas <= 3: {'SI' if todos70 and fas <= 3 else 'no'}")
    # regla de replica: el lado de un umbral cambia si se mueve UNA copia (k -> k-1 o k+1, dentro de [0, n])
    def fragil(k, n, lado):
        return any(0 <= k2 <= n and lado(k2, n) != lado(k, n) for k2 in (k - 1, k + 1))
    cerca = []
    if n and fragil(a, n, lambda k_, n_: k_ / n_ < 0.50):
        cerca.append("instrumento < 0.50")
    if fragil(fas, len(limpias), lambda k_, n_: k_ > 5):
        cerca.append("falsas alarmas > 5")
    if fragil(fas, len(limpias), lambda k_, n_: k_ <= 3):
        cerca.append("falsas alarmas <= 3")
    if con and fragil(aciertos, len(con), lambda k_, n_: k_ / n_ < 0.30):
        cerca.append("total < 0.30")
    for t_, (a_, n_) in sens.items():
        if n_ and fragil(a_, n_, lambda k_, m_: k_ / m_ >= 0.70):
            cerca.append(f"{t_} >= 0.70")
    print(f"- umbrales que cambian de lado moviendo UNA copia (regla de replica): {', '.join(cerca) if cerca else 'ninguno'}")

    if salida:
        with open(salida, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(tabla[0].keys()))
            w.writeheader(); w.writerows(tabla)
        print(f"\ntabla -> {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
