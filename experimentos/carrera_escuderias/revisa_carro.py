"""revisa_carro.py — CHEQUEO ESTATICO de un carro (ERR-96; REGLAMENTO sec. 4). El juez lo corre antes de cada ronda.

MISION: llegar a la AGI por este camino. No hay sandbox (H-5): las prohibiciones del sec. 4 (no leer el rng del
mundo ni la tabla verdadera, no tocar la pista ni el juez) se hacen cumplir por (1) este chequeo y (2) la revision
del auditor. El chequeo es DELIBERADAMENTE estricto: ante la duda rechaza, y el equipo reescribe.

Rechaza un carros/<ID>.py si:
  T  (texto crudo, incluso en comentarios y cadenas) aparece: sys._getframe, _getframe, inspect, gc, globals(,
     locals(, vars(, __builtins__, __import__, __globals__, __dict__, __class__, __subclasses__, __code__,
     __closure__, f_back, f_locals, f_globals, gi_frame, tb_frame, importlib, exec(, eval(, compile(, open(,
     breakpoint(, getattr(, setattr(, delattr(, np.random / numpy.random, default_rng.
  I  importa algo fuera de la LISTA BLANCA (numpy, math, collections, itertools, functools, heapq, bisect,
     statistics, copy, dataclasses, typing, enum, operator) -- en particular sys, os, inspect, gc, importlib,
     pista, juez, organismo_*, corre_*, pickle, json, pathlib, shutil, random, ctypes, subprocess, threading.
     Tambien `from numpy import random` / `numpy.random`.
  A  accede a un atributo dunder (x.__algo__) o llama a un metodo de ESCRITURA de archivos (write, writelines,
     write_text, write_bytes, save, savez, savez_compressed, savetxt, tofile, dump).
  C  no define crea(ctx) a nivel de modulo.
Uso:  python experimentos/carrera_escuderias/revisa_carro.py [ID ...]   (sin argumentos: todos los de carros/)
"""
import ast, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CARROS = os.path.join(AQUI, 'carros')
TEXTO = [r'sys\._getframe', r'_getframe', r'\binspect\b', r'\bgc\b', r'\bglobals\s*\(', r'\blocals\s*\(', r'\bvars\s*\(',
         r'__builtins__', r'__import__', r'__globals__', r'__dict__', r'__class__', r'__subclasses__', r'__code__',
         r'__closure__', r'\bf_back\b', r'\bf_locals\b', r'\bf_globals\b', r'\bgi_frame\b', r'\btb_frame\b',
         r'\bimportlib\b', r'\bexec\s*\(', r'\beval\s*\(', r'\bcompile\s*\(', r'\bopen\s*\(', r'\bbreakpoint\s*\(',
         r'\bgetattr\s*\(', r'\bsetattr\s*\(', r'\bdelattr\s*\(', r'\b(np|numpy)\s*\.\s*random\b', r'\bdefault_rng\b']
BLANCA = {'numpy', 'math', 'collections', 'itertools', 'functools', 'heapq', 'bisect', 'statistics', 'copy',
          'dataclasses', 'typing', 'enum', 'operator'}
ESCRITURA = {'write', 'writelines', 'write_text', 'write_bytes', 'save', 'savez', 'savez_compressed', 'savetxt', 'tofile', 'dump'}
DUNDER_OK = {'__init__'}


def revisa_fuente(src, nombre='<carro>'):
    """Devuelve la lista de violaciones (vacia = pasa)."""
    v = []
    for n, linea in enumerate(src.splitlines(), 1):
        for pat in TEXTO:
            if re.search(pat, linea): v.append(f"T {nombre}:{n} prohibido /{pat}/: {linea.strip()[:80]}")
    try:
        arbol = ast.parse(src)
    except SyntaxError as e:
        return v + [f"S {nombre}: no compila ({e})"]
    for nd in ast.walk(arbol):
        if isinstance(nd, ast.Import):
            for a in nd.names:
                if a.name.split('.')[0] not in BLANCA or a.name.startswith('numpy.random'):
                    v.append(f"I {nombre}:{nd.lineno} import {a.name} fuera de la lista blanca")
        elif isinstance(nd, ast.ImportFrom):
            mod = nd.module or ''
            if nd.level or mod.split('.')[0] not in BLANCA or mod.startswith('numpy.random') or \
                    (mod == 'numpy' and any(a.name == 'random' for a in nd.names)):
                v.append(f"I {nombre}:{nd.lineno} from {'.' * nd.level}{mod} import ... fuera de la lista blanca")
        elif isinstance(nd, ast.Attribute):
            if nd.attr.startswith('__') and nd.attr.endswith('__') and nd.attr not in DUNDER_OK:
                v.append(f"A {nombre}:{nd.lineno} atributo dunder .{nd.attr}")
        elif isinstance(nd, ast.Call):
            f = nd.func
            if isinstance(f, ast.Attribute) and f.attr in ESCRITURA:
                v.append(f"A {nombre}:{nd.lineno} llamada de escritura .{f.attr}(...)")
            if isinstance(f, ast.Name) and f.id in ('__import__', 'exec', 'eval', 'compile', 'open', 'getattr', 'setattr', 'delattr',
                                                     'globals', 'locals', 'vars', 'breakpoint', 'input'):
                v.append(f"A {nombre}:{nd.lineno} llamada prohibida {f.id}(...)")
        elif isinstance(nd, ast.Name) and nd.id in ('__builtins__', '__import__'):
            v.append(f"A {nombre}:{nd.lineno} nombre prohibido {nd.id}")
    if not any(isinstance(nd, ast.FunctionDef) and nd.name == 'crea' for nd in arbol.body):
        v.append(f"C {nombre}: no define crea(ctx) a nivel de modulo")
    return v


def revisa(ident):
    ruta = os.path.join(CARROS, f"{ident}.py")
    if not os.path.exists(ruta): return [f"C {ident}: no existe {ruta}"]
    return revisa_fuente(open(ruta, encoding='utf-8').read(), ident)


def main():
    ids = sys.argv[1:] or sorted(f[:-3] for f in os.listdir(CARROS) if f.endswith('.py'))
    malo = 0
    for i in ids:
        v = revisa(i)
        print(f"{'PASA ' if not v else 'RECHAZADO'} {i}" + ('' if not v else ''.join('\n   ' + x for x in v)))
        malo += bool(v)
    return 1 if malo else 0


if __name__ == '__main__':
    sys.exit(main())
