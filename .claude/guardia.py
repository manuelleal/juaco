"""Guardia de JUACO: hook PreToolUse de Claude Code (se activa desde .claude/settings.json, vía guardia.sh).

Frena mecánicamente los deslices que el 23-sep-2026 tuvo que atrapar el coordinador a mano, para que valga igual en la nube:
  - `python manifiesto.py` sin `--check`: reescribe MANIFEST.txt;
  - Edit/Write sobre un archivo congelado del tronco, sobre MANIFEST.txt o sobre manifiesto.py;
  - `git commit` con MANIFEST.txt modificado o con un congelado roto;
  - `git push --force`, `git reset --hard`, `git clean` y `rm -r` sobre datos/, experimentos/, registro/ u organismo/;
  - runners `corre_*.py` con `--help`/`-h` (ERR-115: no reconocen la bandera y lanzan la serie de verdad).

Salida 0 = permitir; 2 = bloquear (el motivo va por stderr y lo lee el agente). Si la guardia misma falla, permite:
no bloquea por un error propio.
Única llave: la variable de entorno JUACO_CONGELAR=1 en el entorno de la sesión (la pone un humano, no un comando).
Sirve para congelar una versión nueva del tronco con permiso del director.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

LLAVE = os.environ.get('JUACO_CONGELAR') == '1'
PY = r'\bpython[0-9.]*(?:\.exe)?\s+(?:-\S+\s+)*\S*'   # "python", "python3", "python.exe -u ..." antes del script


def bloquear(motivo):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')   # en Windows el stderr entubado no es UTF-8
    except Exception:
        pass
    sys.stderr.write('GUARDIA JUACO (bloqueado): ' + motivo + '\n')
    sys.exit(2)


def congelados(proyecto):
    """{ruta relativa './organismo/...': sha16} leído del texto de manifiesto.py (sin importarlo)."""
    texto = open(os.path.join(proyecto, 'manifiesto.py'), encoding='utf-8').read()
    bloque = texto.split('CONGELADOS', 1)[1].split('}', 1)[0]
    return dict(re.findall(r"'(\./[^']+)'\s*:\s*'([0-9a-f]{16})'", bloque))


def normal(ruta):
    return os.path.normcase(os.path.realpath(ruta))


def revisar_archivo(proyecto, ruta):
    if not ruta or LLAVE:
        return
    objetivo = normal(ruta if os.path.isabs(ruta) else os.path.join(proyecto, ruta))
    protegidos = {normal(os.path.join(proyecto, r)): r for r in congelados(proyecto)}
    protegidos[normal(os.path.join(proyecto, 'MANIFEST.txt'))] = 'MANIFEST.txt'
    protegidos[normal(os.path.join(proyecto, 'manifiesto.py'))] = 'manifiesto.py'
    if objetivo in protegidos:
        bloquear(f'{protegidos[objetivo]} está congelado o es el registro de congelados. Regla 1: el tronco no se edita; '
                 'una versión nueva se construye por anclas en un archivo nuevo y la congela el coordinador con permiso del director.')


def revisar_commit(proyecto):
    if LLAVE:
        return
    sucio = subprocess.run(['git', 'status', '--porcelain', '--', 'MANIFEST.txt'], cwd=proyecto,
                           capture_output=True, text=True, timeout=20).stdout.strip()
    if sucio:
        bloquear('MANIFEST.txt está modificado (¿alguien corrió manifiesto.py sin --check?). Restáuralo con '
                 '`git checkout -- MANIFEST.txt` antes de commitear.')
    for ruta, esperado in congelados(proyecto).items():
        real = hashlib.sha256(open(os.path.join(proyecto, ruta), 'rb').read()).hexdigest()[:16]
        if real != esperado:
            bloquear(f'el archivo congelado {ruta} cambió de hash ({real} != {esperado}). Detenerse y averiguar por qué; '
                     'no se commitea.')


def revisar_comando(proyecto, cmd):
    if re.search(PY + r'manifiesto\.py', cmd) and '--check' not in cmd and not LLAVE:
        bloquear('`manifiesto.py` sin `--check` reescribe MANIFEST.txt. Usa `python manifiesto.py --check`.')
    for seg in re.split(r'&&|\|\||[;|\n]', cmd):
        s = seg.strip()
        if re.search(PY + r'corre_\w*\.py', s) and re.search(r'(?:^|\s)(?:--help|-h)(?:\s|$)', s):
            bloquear('los runners corre_*.py no reconocen --help/-h y lanzan la serie de verdad (ERR-115). '
                     'Lee el docstring del runner o su preregistro.')
        git = re.match(r'(?:\S+=\S+\s+)*git\s+(?:-C\s+\S+\s+)?(\S+)(.*)$', s)
        if git:
            sub, resto = git.group(1), git.group(2)
            if sub == 'push' and re.search(r'(?:^|\s)(?:--force\S*|-f)(?:\s|$)', resto):
                bloquear('push forzado prohibido: reescribe historia compartida. Integra con merge o abre un PR.')
            if sub == 'reset' and '--hard' in resto:
                bloquear('`git reset --hard` descarta trabajo sin vuelta atrás. Usa `git stash` o una rama.')
            if sub == 'clean':
                bloquear('`git clean` borra archivos sin rastrear (humos, datos sin registrar). Nada destructivo (NUBE.md §4).')
            if sub == 'commit':
                revisar_commit(proyecto)
        if re.match(r'rm\s', s) and re.search(r'(?:^|\s)-\w*[rR]\w*|--recursive', s) and \
                re.search(r'(?:^|[\s/"\'])(datos|experimentos|registro|organismo)\b', s):
            bloquear('borrar recursivamente datos/, experimentos/, registro/ u organismo/ está prohibido (nada destructivo).')
        if re.match(r'Remove-Item\b', s, re.I) and re.search(r'-Recurse', s, re.I) and \
                re.search(r'(datos|experimentos|registro|organismo)', s):
            bloquear('borrar recursivamente datos/, experimentos/, registro/ u organismo/ está prohibido (nada destructivo).')


def main():
    try:
        datos = json.load(sys.stdin)
        proyecto = os.environ.get('CLAUDE_PROJECT_DIR') or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        herramienta = datos.get('tool_name', '')
        entrada = datos.get('tool_input') or {}
        if herramienta in ('Edit', 'Write', 'NotebookEdit', 'MultiEdit'):
            revisar_archivo(proyecto, entrada.get('file_path') or entrada.get('notebook_path') or '')
        elif herramienta in ('Bash', 'PowerShell'):
            revisar_comando(proyecto, entrada.get('command') or '')
    except Exception:   # la guardia nunca bloquea por un error propio (SystemExit de bloquear() sí pasa)
        return 0
    return 0


if __name__ == '__main__':
    sys.exit(main())
