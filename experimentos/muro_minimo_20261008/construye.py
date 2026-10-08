"""construye.py — CONSTRUYE POR ANCLAS el instrumento del bloque MURO MINIMO (8-oct-2026). Mision: llegar a la AGI por este camino.

Nada del instrumento se escribe a mano: cada archivo sale de su ORIGEN con sha fijado (sha256[:16] del texto con saltos LF) y se
copia SIN reemplazos (cero anclas: esta carpeta esta a la misma profundidad que experimentos/openevolve_serie, asi que las rutas
relativas de corre_carro.py y evaluador.py a la pista y al juez valen tal cual). Si un origen cambio, aborta.

  origen (solo lectura)                                         ->  destino (esta carpeta)
  experimentos/openevolve_serie/corre_carro.py                  ->  corre_carro.py           (el del examen grande, fundador NO limpio)
  experimentos/openevolve_serie/evaluador.py                    ->  evaluador.py             (solo se usa su filtro _revisa)
  experimentos/openevolve_serie/examen/programas/HUMO.py        ->  programas/HUMO.py        (referencia; sha12 69fcfcb2473f)
  experimentos/openevolve_serie/raiz/programa_inicial.py        ->  programas/O1_SINLIMPIA.py (la raiz de la que partio HUMO; control)
  experimentos/openevolve_serie/diseccion/programas/KO_PIZARRA.py -> programas/KO_PIZARRA.py  (HUMO sin pizarra; referencia justa)
  O1 no se copia: corre_carro.py lo carga por ID de experimentos/carrera_escuderias/carros/O1.py (sha 99436afa2715f028).
  programas/MINIMO.py es lo UNICO escrito a mano (identidad.py mide su diferencia contra la raiz).

Uso:  python -B construye.py            (escribe)        python -B construye.py --check   (solo compara; sale con 1 si algo difiere)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
SER = os.path.join(REPO, "experimentos", "openevolve_serie")
PISTA = os.path.join(REPO, "experimentos", "carrera_escuderias")

COPIAS = [  # (origen, destino relativo, sha16 del texto LF)
    (os.path.join(SER, "corre_carro.py"), "corre_carro.py", "ddcfd0f06a7acc87"),
    (os.path.join(SER, "evaluador.py"), "evaluador.py", "6736985f4f42cdc5"),
    (os.path.join(SER, "examen", "programas", "HUMO.py"), os.path.join("programas", "HUMO.py"), "69fcfcb2473fdbf6"),
    (os.path.join(SER, "raiz", "programa_inicial.py"), os.path.join("programas", "O1_SINLIMPIA.py"), "50b2fc3241da510e"),
    (os.path.join(SER, "diseccion", "programas", "KO_PIZARRA.py"), os.path.join("programas", "KO_PIZARRA.py"), "965aaec1e366a098"),
]
SOLO_LEE = [  # no se copian; se fija su sha (BINARIO, el mismo h16 que la pista escribe en cada JSON, salvo O1 y revisa que son LF)
    (os.path.join(PISTA, "carros", "O1.py"), "99436afa2715f028"),
    (os.path.join(PISTA, "pista.py"), "9f47c65e438e0ff4"),
    (os.path.join(PISTA, "juez.py"), "6a68f640a7832f12"),
    (os.path.join(PISTA, "revisa_carro.py"), "1c8a789f7427ab96"),
]


def lf(ruta):
    return open(ruta, "rb").read().decode("utf-8").replace("\r\n", "\n")


def s16(txt):
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16]


def main(check):
    mal = 0
    for org, dst, sha in COPIAS:
        t = lf(org); h = s16(t)
        if h != sha: raise SystemExit(f"ORIGEN CAMBIO: {org} sha {h} != {sha}")
        d = os.path.join(AQUI, dst)
        if check:
            ok = os.path.exists(d) and lf(d) == t
            mal += not ok
            print(f"  {'IGUAL  ' if ok else 'DIFIERE'} {dst}  (origen sha {h})")
        else:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            with open(d, "w", encoding="utf-8", newline="\n") as fh: fh.write(t)
            print(f"  escrito {dst}  (origen sha {h})")
    for org, sha in SOLO_LEE:
        h = hashlib.sha256(open(org, "rb").read()).hexdigest()[:16]
        ok = h == sha; mal += not ok
        print(f"  {'IGUAL  ' if ok else 'DIFIERE'} {os.path.relpath(org, REPO)}  sha {h} (fijado {sha})")
    print("CONSTRUYE:", "TODO IGUAL" if not mal else f"{mal} DIFERENCIAS")
    return mal


if __name__ == "__main__":
    sys.exit(1 if main("--check" in sys.argv) else 0)
