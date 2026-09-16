"""JUACO-EVO — operador de mutacion CIEGA (control). Escala UNA constante de coma flotante del cuerpo de run() por un
factor U(0.5, 2) con RNG propio. No sabe nada del organismo. Reintenta si el resultado no compila.

v1 (ERR-18, 16 sep 18:55): quedan PROTEGIDAS las constantes de CONSTITUCION y de MUNDO, que cambian la supervivencia
sin cambiar el aprendizaje (energia tras morir E=.6, energia inicial E=1.0, tope 1.5, costo metabolico, renovacion
del mundo .003). Base del RNG 8000 (v0 usaba 7000).

Uso:  python muta_ciega.py <padre.py> <destino_dir> <gen> <k>
Escribe <destino_dir>/organismo.py y <destino_dir>/hipotesis.md.
"""
import sys, os, re, hashlib
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
FLOAT = re.compile(r'(?<![\w.])(\d*\.\d+|\d+\.)(?![\w.])')   # .03  0.85  3.  1.5  (no enteros, no dentro de nombres)
PROTEGIDAS = ('E=.6', 'E=1.0', 'min(E+', 'costo', '.003')   # v1: constitucion y mundo, fuera del alcance del operador
VERSION = 'v1'; BASE_RNG = 8000


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def muta(src, rng):
    ini = src.index('def run(')
    cab, cuerpo = src[:ini], src[ini:]
    lineas = cuerpo.splitlines(keepends=True)
    def protegida(l, m):
        seg = l[max(0, m.start() - 12):m.end() + 1]
        return any(p in seg for p in PROTEGIDAS) or any(p in l for p in ('E=.6', 'E=1.0', 'min(E+', '.003'))
    cands = [(i, m) for i, l in enumerate(lineas) if not l.lstrip().startswith('#') for m in FLOAT.finditer(l) if not protegida(l, m)]
    if not cands: raise SystemExit('sin constantes flotantes')
    i, m = cands[int(rng.integers(len(cands)))]
    viejo = m.group(0); f = float(rng.uniform(0.5, 2.0)); nuevo = repr(round(float(viejo) * f, 6))
    l = lineas[i]; lineas[i] = l[:m.start()] + nuevo + l[m.end():]
    return cab + ''.join(lineas), (i, viejo, nuevo, round(f, 3), l.strip()[:100])


if __name__ == '__main__':
    padre, dest, gen, k = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    os.makedirs(dest, exist_ok=True)
    src = open(padre, encoding='utf-8').read()
    for intento in range(20):
        rng = np.random.default_rng(BASE_RNG + 100 * gen + 10 * k + intento)
        hijo, info = muta(src, rng)
        try:
            compile(hijo, 'hijo', 'exec'); break
        except SyntaxError:
            continue
    else:
        raise SystemExit('20 intentos sin compilar')
    p = os.path.join(dest, 'organismo.py'); open(p, 'w', encoding='utf-8', newline='\n').write(hijo)
    open(os.path.join(dest, 'hipotesis.md'), 'w', encoding='utf-8').write(
        f"# Mutacion CIEGA gen{gen} k{k}\n\noperador: muta_ciega {VERSION} (escala una constante flotante; constitucion y mundo protegidas), rng {BASE_RNG}+100*gen+10*k+intento (intento {intento})\n"
        f"padre: {os.path.basename(padre)} ({h16(padre)})\nlinea del cuerpo de run() #{info[0]}: `{info[4]}`\n"
        f"constante {info[1]} -> {info[2]} (factor {info[3]})\n\nHipotesis: ninguna (control ciego).\n")
    print(f"  gen{gen} ciega k{k}: {info[1]} -> {info[2]} (x{info[3]}) en `{info[4][:60]}`  sha {h16(p)}")
