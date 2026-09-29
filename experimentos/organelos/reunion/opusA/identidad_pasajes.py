"""identidad_pasajes.py — ARNES de corre_pasajes / nucleo_pasajes (Opus A, reunion 28-sep). Un proceso, sin Pool, T corto.
Semillas de practica 47806-47809. Salida: identidad_pasajes_salida.txt (la escribe quien lo corre con tee).
  (K) nucleo construido por anclas == disco; origenes con su sha.
  (A) 1 pasaje sin transferencia == ECO_SEL_ING bit a bit: nucleo_pasajes.trabajo(ING_SEL_C) == nucleo_eco_sel_ing.trabajo(ING_SEL_C)
      en TODAS las claves salvo seg; y corre_pasajes.pasaje(PAS_SEL, genoma None) == lo mismo salvo seg y brazo.
  (G0) genoma = G0 x 90 explicito == genoma None (bit a bit salvo seg).
  (G) el genoma entra: con genomas distintos por fundador, a T = 10 los vivos de cada linaje llevan el genoma de su fundador.
  (X) control que puede fallar: genoma transferido != G0 -> la corrida difiere.
  (F) la transferencia no usa fitness: con linaje/k/gen/tn borrados en vivos_final, el genoma transferido es el mismo.
  (R) el resorteo es G0 mutado una vez (no depende de los vivos); PAS_RES p2 != PAS_SEL p2.
  (D) determinismo: la cadena de 2 pasajes dos veces == igual.
"""
import json, os, shutil, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_pasajes as C
N = C.N
sys.path.insert(0, os.path.join(N.RAIZ, 'experimentos', 'organelos', 'eco_sel_ing'))
import nucleo_eco_sel_ing as NI

OK = []


def caso(nom, cond, det=''):
    OK.append(bool(cond)); print(f"[{'OK ' if cond else 'MAL'}] {nom} {det}", flush=True)


def sin(r, *claves):
    return {k: v for k, v in r.items() if k not in claves}


def main():
    t0 = time.time()
    sh = C.verifica(); caso('(K) nucleo por anclas y origenes con sha', True, str(sh))
    N.usa_gemelo()
    caso('(K) el gemelo es el mismo modulo en los dos nucleos', NI.CR is N.CR and 'GEMELO' in N.nombre_motor())
    tmp = tempfile.mkdtemp(prefix='idpas_')
    T = 20000; s = 47806
    a = NI.trabajo((s, 'ING_SEL_C', T, T, NI.FRIO['T_lect'], os.path.join(tmp, 'a'), False))
    b = N.trabajo((s, 'ING_SEL_C', T, T, N.FRIO['T_lect'], os.path.join(tmp, 'b'), False))
    caso('(A) nucleo_pasajes.trabajo(ING_SEL_C) == nucleo_eco_sel_ing.trabajo bit a bit (salvo seg)',
         json.dumps(sin(a, 'seg'), sort_keys=True, default=str) == json.dumps(sin(b, 'seg'), sort_keys=True, default=str),
         f"(claves {len(a)}; fund_2a {a['fund_2a']} / {b['fund_2a']}; K_nac {a['K_nac']} / {b['K_nac']})")
    c = C.pasaje(s, 'PAS_SEL', T, os.path.join(tmp, 'c'), None)
    caso('(A) corre_pasajes.pasaje(PAS_SEL, sin transferencia) == ECO_SEL_ING (salvo seg, brazo)',
         json.dumps(sin(a, 'seg', 'brazo'), sort_keys=True, default=str) == json.dumps(sin(c, 'seg', 'brazo'), sort_keys=True, default=str))
    G0, lo, hi = C.G0_lo_hi()
    d = C.pasaje(s, 'PAS_SEL', T, os.path.join(tmp, 'd'), np.tile(G0, (C.NF, 1)))
    caso('(G0) genoma = G0 x 90 explicito == None', json.dumps(sin(c, 'seg'), sort_keys=True, default=str) == json.dumps(sin(d, 'seg'), sort_keys=True, default=str))
    # (G) el genoma entra
    rng = np.random.default_rng(47807)
    Gx = np.array([C.ME.muta(G0, rng, C.pv_de('PAS_SEL')[0] * 0 + 1.0 * (C.pv_de('PAS_SEL')[0] > 0), 0.3, lo, hi)[0] for _ in range(C.NF)])
    e = C.pasaje(47807, 'PAS_SEL', 10, os.path.join(tmp, 'e'), Gx)
    buenos = [v for v in e['vivos_final'] if v[2] == 0 and np.allclose(v[4:], np.round(Gx[v[0]], 6), atol=1e-9)]
    fund = [v for v in e['vivos_final'] if v[2] == 0]
    caso('(G) a T = 10 los fundadores vivos llevan el genoma dado a su linaje', len(fund) > 0 and len(buenos) == len(fund),
         f"({len(buenos)}/{len(fund)} fundadores; genomas distintos entre si: {len({tuple(np.round(g, 6)) for g in Gx})})")
    # (X) control que puede fallar
    f_ = C.pasaje(s, 'PAS_SEL', T, os.path.join(tmp, 'f'), Gx)
    caso('(X) con genomas transferidos distintos de G0 la corrida difiere', f_['tam_total'] != c['tam_total'] or f_['fund_2a'] != c['fund_2a'],
         f"(fund_2a {f_['fund_2a']} vs {c['fund_2a']})")
    # (F) sin fitness
    V = c['vivos_final']; V0 = [[0, 0, 0, 0] + list(v[4:]) for v in V]
    t1 = C.transfiere_vivos(V, np.random.default_rng([1, 2, 78, 1])); t2 = C.transfiere_vivos(V0, np.random.default_rng([1, 2, 78, 1]))
    caso('(F) la transferencia solo lee el genoma (linaje/k/gen/tn borrados: igual)', np.array_equal(t1, t2), f"(vivos {len(V)} -> {t1.shape})")
    caso('(F) la transferencia devuelve genomas de vivos (cada fila es un vivo)', all(any(np.allclose(r, np.clip(v[4:], lo, hi)) for v in V) for r in t1))
    # (R) resorteo
    pv, sg = C.pv_de('PAS_RES')
    r1 = C.resorteo(lambda i: np.random.default_rng([47808, 2, 78, 2, i]), pv, sg)
    difG0 = int(sum(1 for g in r1 if not np.array_equal(g, G0)))
    caso('(R) resorteo = G0 mutado una vez (no todos iguales a G0; genes no mutables intactos)',
         0 < difG0 < C.NF and all(g[j] == G0[j] for g in r1 for j in range(len(G0)) if pv[j] == 0), f"({difG0}/90 distintos de G0)")
    # (D) determinismo de la cadena + (R) RES p2 != SEL p2
    x1 = C.cadena('PAS_SEL', 47808, 2, 10000, etq=os.path.relpath(os.path.join(tmp, 'x1'), C.DATOS), log=lambda z: None)
    x2 = C.cadena('PAS_SEL', 47808, 2, 10000, etq=os.path.relpath(os.path.join(tmp, 'x2'), C.DATOS), log=lambda z: None)
    caso('(D) cadena de 2 pasajes dos veces: igual', json.dumps([sin(f, 'seg') for f in x1]) == json.dumps([sin(f, 'seg') for f in x2]))
    y = C.cadena('PAS_RES', 47808, 2, 10000, etq=os.path.relpath(os.path.join(tmp, 'y'), C.DATOS), log=lambda z: None)
    caso('(R) PAS_RES p1 == PAS_SEL p1 (misma semilla, G0) y p2 difiere',
         json.dumps(sin(y[0], 'seg', 'brazo')) == json.dumps(sin(x1[0], 'seg', 'brazo')) and y[1]['fund_2a'] != x1[1]['fund_2a'],
         f"(p1 fund_2a {x1[0]['fund_2a']}/{y[0]['fund_2a']}; p2 {x1[1]['fund_2a']}/{y[1]['fund_2a']})")
    # (C) --continua: 2 pasajes + continuar a 3 == 3 pasajes de una vez (bit a bit salvo seg)
    z3 = C.cadena('PAS_SEL', 47808, 3, 10000, etq=os.path.relpath(os.path.join(tmp, 'z3'), C.DATOS), log=lambda z: None)
    C.cadena('PAS_SEL', 47808, 3, 10000, etq=os.path.relpath(os.path.join(tmp, 'x2'), C.DATOS), log=lambda z: None, continua=True)
    zc = json.load(open(os.path.join(tmp, 'x2', 'RESUMEN.json'), encoding='utf-8'))['filas']
    caso('(C) continuar una cadena de 2 hasta 3 == la cadena de 3 de una vez', json.dumps([sin(f, 'seg') for f in z3]) == json.dumps([sin(f, 'seg') for f in zc]),
         f"(p3 fund_2a {z3[-1]['fund_2a']} / {zc[-1]['fund_2a']})")
    gj = os.path.join(tmp, 'x1', 'genomas_ultimo_PAS_SEL_s47808.json')
    caso('(J) la cadena escribe el genoma del ultimo pasaje (90 x 18)', os.path.exists(gj) and np.array(json.load(open(gj))['genomas']).shape == (90, 18))
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"ARNES PASAJES: {sum(OK)}/{len(OK)} en {round(time.time() - t0, 1)} s")


if __name__ == '__main__':
    main()
