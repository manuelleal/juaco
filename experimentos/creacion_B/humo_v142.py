"""HUMO de las dos baterias de v14.2 (regla 14 ampliada, ERR-42: toda bateria copiada pasa un humo que llegue a
ESCRIBIR su JSON antes de la serie). Dos semillas, UN SOLO PROCESO: `multiprocessing.Pool` queda sustituido por
un Pool en serie (el repo no puede abrir un Pool aqui; la regla 1 la corre el coordinador).

NO cambia ni un umbral ni un criterio: ejecuta `bateria_v142.py 2 --log` y
`bateria_generaliza_v142.py organismo_v142 2 --desde 101 --log` tal cual, con el argv que les toca.
Lo unico que se mira es que el JSON exista y tenga sha.

Uso: python experimentos/creacion_B/humo_v142.py [semillas]
"""
import multiprocessing, os, runpy, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
DAT = os.path.join(RAIZ, 'datos')


class PoolSerie:
    """Pool de un proceso: misma interfaz que usan las baterias, sin abrir procesos."""

    def __init__(self, n=1, *a, **k):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def imap_unordered(self, f, it, chunksize=1):
        return map(f, it)

    def map(self, f, it, chunksize=1):
        return list(map(f, it))

    def close(self):
        pass

    def join(self):
        pass


def nuevos(patron, antes):
    return sorted(f for f in os.listdir(DAT) if f.startswith(patron) and f not in antes)


def corre(script, argv, patron):
    antes = set(os.listdir(DAT))
    print(f'\n=== HUMO {script} {" ".join(argv)} (un proceso) ===', flush=True)
    sys.argv = [os.path.join(ORG, script)] + argv
    cwd = os.getcwd()
    os.chdir(ORG)
    try:
        runpy.run_path(os.path.join(ORG, script), run_name='__main__')
    except SystemExit as e:
        print(f'  (SystemExit {e.code})')
    finally:
        os.chdir(cwd)
    hechos = nuevos(patron, antes)
    js = [f for f in hechos if f.endswith('.json')]
    print(f'  archivos nuevos: {hechos}')
    print(f"  {'JSON ESCRITO' if js else '*** NO SE ESCRIBIO JSON (ERR-42)'}: {js}")
    return bool(js)


if __name__ == '__main__':
    S = sys.argv[1] if len(sys.argv) > 1 else '2'
    multiprocessing.Pool = PoolSerie          # el humo no abre Pool
    sys.path[:0] = [ORG, os.path.join(RAIZ, 'experimentos', 'bug01')]
    t0 = time.time()
    a = corre('bateria_v142.py', [S, '--log'], 'examen_v142_')
    b = corre('bateria_generaliza_v142.py', ['organismo_v142', S, '--desde', '101', '--log'], 'regresion_generaliza_organismo_v142_')
    print(f'\nHUMO v14.2: bateria_v142 JSON {"OK" if a else "FALLA"} | bateria_generaliza_v142 JSON {"OK" if b else "FALLA"}'
          f'   ({time.time()-t0:.0f}s)')
    sys.exit(0 if (a and b) else 1)
