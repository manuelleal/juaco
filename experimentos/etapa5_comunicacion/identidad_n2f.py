"""Arnes de identidad de las perillas N2f (regen_rota, escucha_si_no_sabe) sobre mundo_social_n3.py.

Con las dos APAGADAS, el modulo regenerado por construye_n3.py debe dar EXACTAMENTE lo mismo que el anterior, en
las cuatro rutas que importan: tronco (regen=None), via de simbolos (regen=None), via de simbolos CON regen=50 y el
montaje de N3c/N3d (conducta + mascaras + regen=50). Se comparan TODAS las claves del resultado previo.

Uso:  python experimentos/etapa5_comunicacion/identidad_n2f.py <mundo_social_n3_anterior.py> [--T 60000]
"""
import sys, os, json, time, hashlib, importlib.util

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias')]
T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 60000
SEMILLAS = (81, 82)
KW_N2B = dict(gamma_sim=1.2, baseline_q=True, u_m=1.0)
MR = [0, 0, 0, 1, 1, 1.]; ME = [1, 1, 1, 0, 0, 0.]

ESCENARIOS = {
    'A tronco (regen=None)':        dict(n=1, mundo='regla', regla='azar', regen=None),
    'B simbolos (regen=None)':      dict(n=2, mundo='regla', regla='azar', regen=None, senal='simbolo', **KW_N2B),
    'C simbolos (regen=50)':        dict(n=2, mundo='regla', regla='azar', regen=50, senal='simbolo', **KW_N2B),
    'D N3c/N3d (conducta, regen=50)': dict(n=2, mundo='regla', regla='px0', regen=50, senal='conducta', mascaras=[MR, ME],
                                           kw_por_org=[dict(gamma_soc=1.5), dict(escucha=False)]),
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def carga(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec); sys.modules[nombre] = m; spec.loader.exec_module(m)
    return m


if __name__ == '__main__':
    prev_ruta = os.path.abspath(sys.argv[1])
    nuevo_ruta = os.path.join(AQUI, 'mundo_social_n3.py')
    print(f"anterior {os.path.basename(prev_ruta)} {h16(prev_ruta)}   nuevo mundo_social_n3.py {h16(nuevo_ruta)}   T={T}")
    prev = carga(prev_ruta, 'ms_n3_prev'); nuevo = carga(nuevo_ruta, 'ms_n3_nuevo')
    ok_total = 0; n_total = 0
    for nombre, kw in ESCENARIOS.items():
        for s in SEMILLAS:
            t0 = time.time()
            a = prev.run(s, T=T, **kw); b = nuevo.run(s, T=T, **kw)
            dif = [(j, k) for j in range(len(a)) for k in a[j] if N(a[j][k]) != N(b[j][k])]
            n_total += 1; ok_total += not dif
            print(f"  {nombre:32s} s{s}: {'IDENTICO' if not dif else 'DIFIERE ' + str(dif[:6])}   ({time.time()-t0:.0f}s)")
    print(f"\nIDENTIDAD perillas N2f apagadas: {ok_total}/{n_total}" + ("  OK" if ok_total == n_total else "  *** FALLA ***"))
    sys.exit(0 if ok_total == n_total else 1)
