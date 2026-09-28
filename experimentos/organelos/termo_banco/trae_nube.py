"""trae_nube.py — trae a esta carpeta, POR SHA, los archivos del bloque TERMO_EVO de la nube (termo_banco, 28-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros.

Origen: rama origin/nube/termo-evo-20260928, commit FIJADO c43e12a (se lee con `git show <commit>:<ruta>`; NO se hace merge).
Cada archivo se escribe tal cual (bytes) y su sha16 se compara con el FIJADO aqui (los del codigo son los de la tabla sec. 10 de
PREREGISTRO_termo_evo.md de la nube; los de los documentos se fijaron el 28-sep 17:10 al leerlos). Si uno no coincide: aborta.
  - El CODIGO va a termo_banco/ con el MISMO nombre y la MISMA posicion relativa que en termo_evo/ (construye_evo.py, corre_evo.py,
    identidad_evo.py, carros/V143_EVO_*.py): asi sus rutas (RAIZ = tres niveles arriba) y sus SHAS internos siguen valiendo.
  - Los DOCUMENTOS de la nube van a termo_banco/origen_nube/ (para no chocar con el ENCARGO_NUBE.md de este bloque).
  - Los datos de la nube NO se copian (se citan por sha en el preregistro).
Uso:  python experimentos/organelos/termo_banco/trae_nube.py [--verifica]
"""
import argparse, hashlib, os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
COMMIT = 'c43e12a'
RAMA = 'origin/nube/termo-evo-20260928'
ORIG = 'experimentos/organelos/termo_evo'
CODIGO = {'construye_evo.py': '6cdd7dd10e9a0594', 'corre_evo.py': '7d8e660a1b0e1a71', 'identidad_evo.py': '7e3f6fa48f83c387',
          'carros/V143_EVO_BAJO.py': '3187b373654e119f', 'carros/V143_EVO_ANCHO.py': '1ff17bf4c6e32382',
          'carros/V143_EVO_SINHER.py': 'a11989a3b04d13d6', 'carros/V143_EVO_M40.py': '713cd55ed465cc82'}
DOCS = {'PREREGISTRO_termo_evo.md': '7f45b1385d82ca23', 'INFORME.md': 'ccc542ed8329be9f', 'ENCARGO_NUBE.md': 'cdb5cff87322d37e',
        'identidad_evo_salida.txt': 'a42805033ad08f99', 'humo_salida.txt': '3f2a6ce5784e8429', 'lee_posthoc.py': '4137afe750bad9ee'}


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


def git_show(rel):
    return subprocess.run(['git', 'show', f'{COMMIT}:{ORIG}/{rel}'], cwd=RAIZ, capture_output=True, check=True).stdout


def destino(rel, doc):
    return os.path.join(AQUI, 'origen_nube', rel) if doc else os.path.join(AQUI, *rel.split('/'))


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true', help='solo compara el disco con los shas fijados (no usa git)')
    a = ap.parse_args(argv)
    ok = True
    if not a.verifica:
        full = subprocess.run(['git', 'rev-parse', COMMIT], cwd=RAIZ, capture_output=True, text=True, check=True).stdout.strip()
        tip = subprocess.run(['git', 'rev-parse', RAMA], cwd=RAIZ, capture_output=True, text=True).stdout.strip()
        print(f"origen {RAMA} commit fijado {full} (punta actual de la rama: {tip or 'no disponible'})")
    for doc, tabla in ((False, CODIGO), (True, DOCS)):
        for rel, sha in tabla.items():
            ruta = destino(rel, doc)
            if a.verifica:
                s = h16b(open(ruta, 'rb').read()) if os.path.exists(ruta) else 'NO EXISTE'
            else:
                b = git_show(rel); s = h16b(b)
                if s == sha:
                    os.makedirs(os.path.dirname(ruta), exist_ok=True)
                    with open(ruta, 'wb') as fh: fh.write(b)
            ok &= s == sha
            print(f"  {'doc ' if doc else 'cod '}{rel:32s} sha {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'} -> {os.path.relpath(ruta, RAIZ)}")
    print('TRAE_NUBE: ' + ('TODO OK' if ok else 'ALGO FALLA'))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
