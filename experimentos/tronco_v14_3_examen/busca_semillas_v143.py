"""busca_semillas_v143.py -- ¿estan LIBRES las semillas del examen de v14.3? Busca, en TODO PROYECTOS/JUACO (repo, los ocho
worktrees, sandbox, anclado y respaldo; sin .git ni binarios), cada numero de los rangos del examen:
  (a) en .py y .md, cualquier aparicion;
  (b) en cualquier archivo, en contexto de semilla ("seed": N, semilla=N, --desde N, range(N, _sN, sN-, "semillas N");
  (c) en nombres de archivo.
No corre ningun organismo. Imprime cada aparicion con su contexto para clasificarla a mano (sello de hora HHMMSS, fragmento de
sha, URL, conteo de pasos... o SEMILLA). Resultado del 23-sep-2026 ~21:00 en PREREGISTRO_examen_v143.md §8.

    python experimentos/tronco_v14_3_examen/busca_semillas_v143.py            (rangos 43000-44600 y 143000-144600)
"""
import collections, os, re, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
AQUI = os.path.dirname(os.path.abspath(__file__))
JUACO = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))   # .../PROYECTOS/JUACO
RANGOS = [(43000, 44600), (143000, 144600)]
BIN = ('.bundle', '.png', '.jpg', '.pdf', '.pyc', '.zip', '.xlsx', '.npz', '.npy', '.pkl', '.gz')
num = re.compile(rb'(?<![0-9.])(\d{5,6})(?![0-9])')
ctx = re.compile(rb'(?:"seed"|"semilla"|"seed_real"|seed\s*=|semilla\s*=|--desde\s+|--semillas?\s+|range\(\s*|_s|\bs|semillas?\s+|seeds?\s+)'
                 rb'(\d{5,6})(?![0-9])', re.I)
en_rango = lambda v: any(lo <= v <= hi for lo, hi in RANGOS)

if __name__ == '__main__':
    if sys.argv[1:]:
        raise SystemExit(f'*** este script no toma argumentos: {sys.argv[1:]}')
    codigo = collections.defaultdict(set); semilla = collections.defaultdict(set); n = 0
    for raiz, dirs, archivos in os.walk(JUACO):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
        for a in archivos:
            p = os.path.join(raiz, a); rel = os.path.relpath(p, JUACO)
            if 'tronco_v14_3_examen' in rel:
                continue   # este bloque declara sus propias semillas
            for m in re.finditer(r'(\d{5,6})', a):
                if en_rango(int(m.group(1))):
                    semilla[int(m.group(1))].add(rel + '  [nombre de archivo]')
            if a.endswith(BIN):
                continue
            try:
                b = open(p, 'rb').read()
            except Exception:
                continue
            n += 1
            if a.endswith(('.py', '.md')):
                for m in num.finditer(b):
                    v = int(m.group(1))
                    if en_rango(v):
                        s0 = max(0, m.start() - 50)
                        codigo[v].add(f"{rel}: ...{b[s0:m.end() + 20].decode('utf-8', 'replace')!r}")
            for m in ctx.finditer(b):
                v = int(m.group(1))
                if en_rango(v):
                    semilla[v].add(rel + '  [contexto de semilla]')
    print(f'{n} archivos de texto leidos en {JUACO}; rangos {RANGOS}')
    print(f'(a) numeros de los rangos en .py/.md: {len(codigo)}')
    for v in sorted(codigo):
        print(f'   {v}: ' + ' | '.join(sorted(codigo[v])[:2]))
    print(f'(b)+(c) numeros de los rangos en contexto de semilla o en nombres de archivo: {len(semilla)}')
    for v in sorted(semilla):
        print(f'   {v}: ' + ' | '.join(sorted(semilla[v])[:2]))
