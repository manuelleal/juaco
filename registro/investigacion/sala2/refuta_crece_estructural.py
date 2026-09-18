"""Sala 2 / REFUTADOR (lente medibilidad) del diseno crece_codigo. Dato ESTRUCTURAL sin simular un paso del organismo
(misma clase que coactividad_tren_xor01.py del propio diseno): lee el reparto tren/test con organismo_v14g.split_regla
(solo lectura; organismo/ PRIMERO en sys.path, ERR-28) y cuenta, por semilla:
  pares_veneno_tren : pares co-activos en los patrones VENENO del tren. Bajo la regla del §2.1/§2.5 del diseno (todo
                      estimulo veneno nuevo produce >= 2 sorpresas, g_rec = 2) son los pares que se reclutan SOLO con
                      veneno: cota INFERIOR de la ocupacion antes de contar ninguna sorpresa de comida.
  pares_tren        : pares co-activos en todo el tren (el numero del §4.5 del diseno): cota SUPERIOR.
  tablas_consistentes: pares (i,j) cuya tabla de 2 bits casilla -> valencia es CONSISTENTE con los 8 patrones de tren
                      (ningun casillero recibe comida y veneno). Un nodo consistente tiene error 0 sobre el tren con
                      R crudo y sobrescritura: si hay mas de uno, la lectura en la sonda se decide por empate (boleto),
                      no por 'consistencia'. (0,1) es siempre consistente en xor01.
  casillas_01_tren  : cuantas de las 4 casillas del par (0,1) aparecen en el tren (las que el nodo puede llenar antes de la sonda).
Uso: python refuta_crece_estructural.py [desde] [n]
"""
import sys, os, json, itertools
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)
import organismo_v14g as G

PARES = [(i, j) for i in range(6) for j in range(i + 1, 6)]


def fila(s, regla):
    pats, tren, test, vr = G.split_regla(s, regla)
    act = {k: [i for i in range(6) if k[i] == '1'] for k in tren}
    p_ven = set(); p_all = set()
    for k in tren:
        pp = set(itertools.combinations(act[k], 2)); p_all |= pp
        if vr[k] == 'veneno': p_ven |= pp
    cons = []
    for (i, j) in PARES:
        cas = {}
        ok = True
        for k in tren:
            c = int(k[i]) * 2 + int(k[j])
            if c in cas and cas[c] != vr[k]: ok = False; break
            cas[c] = vr[k]
        if ok: cons.append((i, j))
    cas01 = len({int(k[0]) * 2 + int(k[1]) for k in tren})
    return dict(seed=s, regla=regla, pares_veneno_tren=len(p_ven), pares_tren=len(p_all),
                tablas_consistentes=len(cons), consistentes=cons, par01_consistente=(0, 1) in cons,
                casillas_01_tren=cas01, n11=sum(1 for k in tren if k[0] == '1' and k[1] == '1'))


def med(xs): xs = sorted(xs); return xs[len(xs) // 2]


if __name__ == '__main__':
    desde = int(sys.argv[1]) if len(sys.argv) > 1 else 1101
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    out = {}
    for regla in ('xor01', 'px0'):
        F = [fila(s, regla) for s in range(desde, desde + n)]
        out[regla] = dict(
            pares_veneno_tren_mediana=med([f['pares_veneno_tren'] for f in F]),
            pares_veneno_tren_min_max=[min(f['pares_veneno_tren'] for f in F), max(f['pares_veneno_tren'] for f in F)],
            pares_tren_mediana=med([f['pares_tren'] for f in F]),
            tablas_consistentes_mediana=med([f['tablas_consistentes'] for f in F]),
            tablas_consistentes_min_max=[min(f['tablas_consistentes'] for f in F), max(f['tablas_consistentes'] for f in F)],
            semillas_con_mas_de_1_consistente=sum(1 for f in F if f['tablas_consistentes'] > 1),
            semillas_veneno_pares_ge_10=sum(1 for f in F if f['pares_veneno_tren'] >= 10),
            semillas_veneno_pares_ge_13=sum(1 for f in F if f['pares_veneno_tren'] >= 13),
            casillas_01_tren_mediana=med([f['casillas_01_tren'] for f in F]) if regla == 'xor01' else None,
            filas=F)
    print(json.dumps(dict(desde=desde, n=n, resumen={r: {k: v for k, v in out[r].items() if k != 'filas'} for r in out}), indent=1))
    json.dump(dict(desde=desde, n=n, **out), open(os.path.join(AQUI, f'refuta_crece_estructural_s{desde}-{desde + n - 1}.json'), 'w',
                                                  encoding='utf-8'), indent=1, default=str)
