"""lee_nicho.py — LECTOR de la hipotesis mecanistica H-NICHO de subida_n9c (PREREGISTRO_n9c.md sec. 5b). NO corre ninguna
simulacion: lee el JSON de una serie de corre_n9c.py y aplica la letra. Escrito ANTES de cualquier serie.

MISION: llegar a la AGI por este camino.

H-NICHO: con el MISMO organismo, la boca que se protege (PRED: predice su estado y no muerde lo que le sube el deficit)
TAPA EL MUNDO de lo malo y la que no se protege (NADA = FABRICA) lo mantiene limpio pero muere de lo que muerde.
Letra (pareado por semilla, umbral 15/20):
  N1  PRED > NADA en malos_mundo (objetos B+D medios en el mundo) en >= 15/20 y diferencia mediana >= +8
  N2  PRED < NADA en buenos_mundo (A+C medios) en >= 15/20
  N3  PRED > NADA en perdidas (llegadas del quimiostato perdidas por mundo lleno) en >= 15/20
  N4  PRED > NADA en vida_fund (mediana de vida de los fundadores) en >= 15/20   (informativa: no decide)
  H-NICHO SE SOSTIENE si N1, N2 y N3; si no, NO SE SOSTIENE.
Uso (exacto; cualquier otra forma ABORTA, ERR-115):
  python experimentos/subida_n9c/lee_nicho.py experimentos/subida_n9c/datos/n9c_serie_s14101-14120_T100000_<sello>.json
"""
import json, math, os, statistics as st, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, 'datos')
NEED = 15; DIF_MALOS = 8.0


def pareo(ps, a, b, k):
    xs = []
    for s in sorted({c['seed'] for c in ps}):
        ca = [c for c in ps if c['seed'] == s and c['brazo'] == a]; cb = [c for c in ps if c['seed'] == s and c['brazo'] == b]
        if ca and cb and ca[0]['estr'][k] is not None and cb[0]['estr'][k] is not None: xs.append(ca[0]['estr'][k] - cb[0]['estr'][k])
    return sum(1 for d in xs if d > 0), sum(1 for d in xs if d < 0), len(xs), (round(float(st.median(xs)), 3) if xs else None)


def main(argv):
    if len(argv) != 1 or argv[0].startswith('-'):
        raise SystemExit("lee_nicho: un solo argumento, la ruta del JSON de una serie (sin banderas) -> ABORTA (ERR-115)")
    f = os.path.abspath(argv[0])
    if not (os.path.dirname(f) == DATOS and os.path.basename(f).startswith('n9c_serie_s') and f.endswith('.json') and os.path.isfile(f)):
        raise SystemExit(f"lee_nicho: {argv[0]!r} no es un JSON de serie de subida_n9c/datos -> ABORTA")
    d = json.load(open(f, encoding='utf-8')); ps = d['por_semilla']; n = len(d['meta']['semillas'])
    need = NEED if n == 20 else math.ceil(0.75 * n)
    g1, p1, n1, m1 = pareo(ps, 'PRED', 'NADA', 'malos_mundo')
    g2, p2, n2, m2 = pareo(ps, 'PRED', 'NADA', 'buenos_mundo')
    g3, p3, n3, m3 = pareo(ps, 'PRED', 'NADA', 'perdidas')
    g4, p4, n4, m4 = pareo(ps, 'PRED', 'NADA', 'vida_fund')
    N1 = g1 >= need and m1 is not None and m1 >= DIF_MALOS; N2 = p2 >= need; N3 = g3 >= need; N4 = g4 >= need
    print(f"serie {d['meta']['etiqueta']} ({n} semillas)")
    print(f"  N1 PRED > NADA en malos_mundo: gana {g1}/{n1}, dif mediana {m1} (>= {need} y >= +{DIF_MALOS}): {'SE CUMPLE' if N1 else 'NO'}")
    print(f"  N2 PRED < NADA en buenos_mundo: pierde {p2}/{n2}, dif mediana {m2} (>= {need}): {'SE CUMPLE' if N2 else 'NO'}")
    print(f"  N3 PRED > NADA en perdidas: gana {g3}/{n3}, dif mediana {m3} (>= {need}): {'SE CUMPLE' if N3 else 'NO'}")
    print(f"  N4 (informativa) PRED > NADA en vida_fund: gana {g4}/{n4}, dif mediana {m4}: {'SE CUMPLE' if N4 else 'NO'}")
    print(f"H-NICHO por la letra: {'SE SOSTIENE' if (N1 and N2 and N3) else 'NO SE SOSTIENE'}")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
