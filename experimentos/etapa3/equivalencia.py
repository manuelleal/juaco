"""
Prueba de equivalencia: organismo_v6_sonda.py vs organismo/organismo_v6.py (congelado, 5f38f83cf49248a3).
Escenarios E1, E2 (invertir_en=50000), E2I (nuevo='C') x semillas 1..6.
Exige que TODOS los campos comunes del dict de retorno sean identicos (comparacion exacta, no tolerancia).
Uso:  python equivalencia.py [nsemillas]
"""
import sys, os, importlib.util, hashlib, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
V6_PATH = os.path.join(RAIZ, 'organismo', 'organismo_v6.py')
SONDA_PATH = os.path.join(AQUI, 'organismo_v6_sonda.py')


def carga(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha16(ruta):
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()[:16]


ESCENARIOS = {
    'E1':  {},
    'E2':  {'invertir_en': 50000},
    'E2I': {'nuevo': 'C'},
}


def norm(x):
    """Representacion canonica comparable exactamente (json de estructuras anidadas)."""
    return json.dumps(x, sort_keys=True, default=str)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    v6 = carga('v6_ref', V6_PATH)
    sonda = carga('v6_sonda_ref', SONDA_PATH)
    print(f"v6    : {V6_PATH}  sha256[:16]={sha16(V6_PATH)}")
    print(f"sonda : {SONDA_PATH}  sha256[:16]={sha16(SONDA_PATH)}")
    print(f"Semillas 1..{n} x {len(ESCENARIOS)} escenarios = {n*len(ESCENARIOS)} comparaciones\n")

    total = 0
    iguales = 0
    fallos = []
    for esc, kw in ESCENARIOS.items():
        for s in range(1, n + 1):
            ra = v6.run(s, **kw)
            rb = sonda.run(s, **kw)
            comunes = sorted(set(ra) & set(rb))
            extra = sorted(set(rb) - set(ra))
            difs = [c for c in comunes if norm(ra[c]) != norm(rb[c])]
            total += 1
            if not difs and set(ra) <= set(rb):
                iguales += 1
                estado = 'IDENTICO'
            else:
                estado = 'DIFIERE ' + ','.join(difs)
                fallos.append((esc, s, difs))
            print(f"  {esc:4s} seed={s}  campos_comunes={len(comunes)}  extra_sonda={extra}  {estado}")

    print(f"\n=== {iguales}/{total} escenarios x semillas identicos en TODOS los campos comunes ===")
    if fallos:
        print("FALLOS:", fallos)
        sys.exit(1)
    print("EQUIVALENCIA VERIFICADA.")


if __name__ == '__main__':
    main()
