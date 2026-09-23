"""identidad_convive.py — ARNES de la pista v2 (generaciones solapadas). Se corre ANTES de mirar numeros. Un proceso, sin Pool.

MISION: llegar a la AGI por este camino.

  (0) ORIGEN: carrera_escuderias/pista.py tiene el sha fijado y pista2.py es EXACTAMENTE lo que construye_pista2.py
      produce desde el (reconstruccion en memoria == archivo en disco).
  (I) IDENTIDAD solapadas=0: pista2.run(..., solapadas=0) == pista.run(...) del HEAD a170746 BIT A BIT en TODA la salida
      (linajes, pista con el estado final del rng del mundo, pizarra), en 7 configuraciones (compat=1, 9 FABRICA con diag,
      rep_acum=1, escala=0, mundo_n, 9 O1 con fundador limpio, mezcla O2/O3/O4 con fundador limpio).
  (S) SIN PARTOS v2 == v1: con TODOS los partos vetados (envoltorio VETO: quiere_parir -> False) la v2 (solapadas=1,
      reposicion='inmediata') reproduce la v1 (fundador_limpio=1) en la fisica: muertes, fundadores, t_fund, mordidas,
      visitas, causas, muertes_vol, vetos, vidas, pasos viables, olvidos, composicion y estado final del rng del mundo.
      Es la prueba de que el MOTOR nuevo (turno, fase A, costos, olvido, fase B, fundador) es el mismo mundo.
  (D) DETERMINISMO v2 (fija e inmediata).
  (C) CONTABILIDAD v2: individuos vs muertes/nacimientos/fundadores/vivos, hijos por padre, generaciones, tam final,
      objetos del quimiostato (36 + llegadas + pisos - mordidas - olvidos == objetos finales).
  (H) HERENCIA: crea/nace por cuerpo (espia): crea = fundadores + nacimientos (+9 iniciales), nace = nacimientos, la memoria
      del padre llega (O1: tabla no vacia en los hijos); quiere_parir recibe cola == vivos_linaje - 1.
  (K) CONTROL CTRL_O3_SINTERM: pasa el chequeo, TERMINAL = False, y == O3 bit a bit mientras TERMINAL no puede dispararse.
  (T) TOPE DE SEGURIDAD: con tope 12 nunca hay mas de 12 vivos; bloqueados > 0 y t_tope marcado.
  (G) GUARDIAS.
Uso: python experimentos/generaciones/identidad_convive.py   (escribe identidad_convive_salida.txt)
"""
import json, os, sys, time, types, importlib.util

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CARRERA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
sys.path[:0] = [AQUI]


def _carga(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = m; spec.loader.exec_module(m); return m


P1 = _carga('pista', os.path.join(CARRERA, 'pista.py'))        # v1 (HEAD a170746), solo se LEE
import pista2 as P2
import construye_pista2 as CP
import motor_convive as MC

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [0, 0]
SAL = open(os.path.join(AQUI, 'identidad_convive_salida.txt'), 'w', encoding='utf-8')


def out(s=''):
    print(s, flush=True); SAL.write(s + '\n'); SAL.flush()


def di(et, ok, extra=''):
    OK[1] += 1; OK[0] += int(bool(ok))
    out(f"  [{'OK ' if ok else 'FALLA'}] {et}{(' · ' + extra) if extra else ''}")


def veto(ident):
    """carro envoltorio: el de ident con TODOS los partos vetados (lo demas, delegado)."""
    base = P1.carga_carro(ident)

    class V:
        def __init__(self, ctx): self._c = base.crea(ctx)
        def __getattr__(self, k): return getattr(self._c, k)
        def quiere_parir(self, info): return False
    m = types.SimpleNamespace(crea=lambda ctx: V(ctx))
    return (ident, m)


def espia(ident, reg):
    base = P1.carga_carro(ident)

    class E:
        def __init__(self, ctx):
            reg['crea'] += 1; self._c = base.crea(ctx)
        def __getattr__(self, k): return getattr(self._c, k)
        def nace(self, info):
            reg['nace'] += 1; m = info.get('memoria'); reg['mem_no_vacia'] += int(bool(m))
            return self._c.nace(info)
        def quiere_parir(self, info):
            reg['qp'] += 1; reg['cola_ok'] += int(info['cola'] == info['vivos_linaje'] - 1 and info['cola'] >= 0)
            f = getattr(self._c, 'quiere_parir', None)
            return True if f is None else f(info)
    return (ident, types.SimpleNamespace(crea=lambda ctx: E(ctx)))


def main():
    t0 = time.time()
    out(f"IDENTIDAD PISTA v2 (generaciones solapadas) · {time.strftime('%Y-%m-%d %H:%M:%S')}")
    # (0)
    src = open(CP.ORIGEN, 'rb').read(); sha = P1.h16(CP.ORIGEN)
    rec = src
    for a, b in CP.ANCLAS: rec = rec.replace(a, b)
    di("(0) origen pista.py sha fijado", sha == CP.SHA_ORIGEN, f"{sha}")
    di("(0) pista2.py == construccion por anclas desde el origen", rec == open(os.path.join(AQUI, 'pista2.py'), 'rb').read(),
       f"pista2 {P1.h16(os.path.join(AQUI, 'pista2.py'))} · motor {P1.h16(os.path.join(AQUI, 'motor_convive.py'))}")
    # (I)
    out("(I) solapadas=0 == pista v1 (HEAD a170746) en TODA la salida")
    confs = [("1 FABRICA compat=1 pizarra=0 s=1 T=5000", 1, ['FABRICA'], dict(T=5000, compat=1, pizarra=0)),
             ("9 FABRICA diag=1 s=4001 T=1500", 4001, ['FABRICA'] * 9, dict(T=1500)),
             ("9 FABRICA rep_acum=1 s=4002 T=1500", 4002, ['FABRICA'] * 9, dict(T=1500, rep_acum=1)),
             ("3 FABRICA escala=0 s=7 T=2000", 7, ['FABRICA'] * 3, dict(T=2000, escala=0)),
             ("1 O1 mundo_n=9 s=8 T=2000", 8, ['O1'], dict(T=2000, mundo_n=9)),
             ("9 O1 fundador_limpio s=10001 T=2000", 10001, ['O1'] * 9, dict(T=2000, fundador_limpio=1)),
             ("O2*3+O3*3+O4*3 fundador_limpio s=10002 T=2000", 10002, ['O2'] * 3 + ['O3'] * 3 + ['O4'] * 3, dict(T=2000, fundador_limpio=1))]
    for et, s, car, kw in confs:
        a = N(P1.run(s, car, **kw)); b = N(P2.run(s, car, solapadas=0, **kw))
        dif = [k for k in ('linajes', 'pista', 'pizarra_log') if a[k] != b[k]]
        di(f"(I) {et}", not dif and a == b, f"rng {b['pista']['rng_mundo_estado']}" + (f" DIF {dif}" if dif else ''))
    # (S)
    out("(S) sin partos (todos vetados): v2 solapadas=1 reposicion='inmediata' == v1 fundador_limpio=1 en la FISICA")
    FIS = ('deaths', 'fundadores', 't_fund', 'mord', 'vis', 'vetos', 'muertes_nec', 'descendientes', 'pasos_viables')
    confs = [("9 FABRICA s=10003 T=3000", 10003, ['FABRICA'] * 9, 3000), ("9 O1 s=10004 T=3000", 10004, ['O1'] * 9, 3000),
             ("O2*3+O3*3+O4*3 s=10005 T=3000", 10005, ['O2'] * 3 + ['O3'] * 3 + ['O4'] * 3, 3000),
             ("1 FABRICA s=10006 T=6000", 10006, ['FABRICA'], 6000)]
    for et, s, car, T in confs:
        a = P1.run(s, [veto(c) for c in car], T=T, diag=0, fundador_limpio=1)
        b = P2.run(s, [veto(c) for c in car], T=T, diag=0, solapadas=1, reposicion='inmediata')
        dif = []
        for la, lb in zip(a['linajes'], b['linajes']):
            for k in FIS:
                va = la['_carrera'][k] if k == 'vetos' else la[k]   # v1 guarda vetos en _carrera
                if N(va) != N(lb[k]): dif.append(k)
            if N(la['_carrera']['causas']) != N(lb['_carrera']['causas']): dif.append('causas')
            if la['_carrera']['muertes_vol'] != lb['_carrera']['muertes_vol']: dif.append('muertes_vol')
            if N(la['vidas_h1'][:-1]) != N(lb['vidas_muertos']): dif.append('vidas')
        for k in ('rng_mundo_estado', 'olvidos', 'comp_mundo', 'L', 'nobj'):
            if N(a['pista'][k]) != N(b['pista'][k]): dif.append('pista.' + k)
        mu = sum(l['deaths'] for l in b['linajes']); ve = sum(l['vetos'] for l in b['linajes'])
        di(f"(S) {et}", not dif, f"muertes {mu} · fundadores {sum(l['fundadores'] for l in b['linajes'])} · vetos {ve} · "
                                 f"rng {b['pista']['rng_mundo_estado']}" + (f" DIF {sorted(set(dif))}" if dif else ''))
        if et.startswith('9 FABRICA'): di("(S) el control no es vacio (hubo muertes y vetos)", mu > 0 and ve > 0)
    # (D)
    out("(D) determinismo v2")
    for rep in ('fija', 'inmediata'):
        a = N(P2.run(10007, ['O1'] * 9, T=2500, diag=0, solapadas=1, reposicion=rep))
        b = N(P2.run(10007, ['O1'] * 9, T=2500, diag=0, solapadas=1, reposicion=rep))
        di(f"(D) 9 O1 {rep} s=10007 T=2500 dos llamadas iguales", a == b, f"max vivos {a['pista']['max_vivos']}")
    # (C) + (H)
    out("(C) contabilidad v2 y (H) herencia por cuerpo")
    for et, s, car, T, rep in [("9 O1 fija s=10008 T=6000", 10008, 'O1', 6000, 'fija'),
                               ("9 FABRICA fija s=10009 T=6000", 10009, 'FABRICA', 6000, 'fija'),
                               ("9 O3 inmediata s=10010 T=4000", 10010, 'O3', 4000, 'inmediata')]:
        reg = dict(crea=0, nace=0, mem_no_vacia=0, qp=0, cola_ok=0)
        r = P2.run(s, [espia(car, reg) for _ in range(9)], T=T, diag=0, solapadas=1, reposicion=rep)
        prob = []
        nac = fun = 0
        for l in r['linajes']:
            ind = l['individuos']; nac += l['nacimientos']; fun += l['fundadores']
            muertos = [x for x in ind if x[4] >= 0]; vivos = [x for x in ind if x[4] < 0]
            if len(muertos) != l['deaths']: prob.append('muertes')
            if len(vivos) != l['vivos_final'] or l['tam'][-1] != l['vivos_final']: prob.append('vivos')
            if sum(1 for x in ind if x[6] == 0) != l['nacimientos']: prob.append('nacimientos')
            if sum(1 for x in ind if x[6] == 1) != l['fundadores'] + 1: prob.append('fundadores')
            if sum(x[5] for x in ind) != l['nacimientos']: prob.append('hijos')
            por_k = {x[0]: x for x in ind}
            for x in ind:
                if x[6] == 0:
                    p = por_k.get(x[2])
                    if p is None or p[1] + 1 != x[1] or not (p[3] <= x[3]) or (p[4] >= 0 and p[4] < x[3]): prob.append('genealogia'); break
            if sum(1 for x in ind if x[6] == 0 and x[3] >= 0) != l['nacimientos']: prob.append('t_nace')
        ps = r['pista']
        if ps['tam_total'][-1] != sum(l['vivos_final'] for l in r['linajes']): prob.append('tam_total')
        mb = sum(sum(sum(v) for v in l['mord'].values()) for l in r['linajes'])
        if rep == 'fija' and 36 + ps['llegadas'] + ps['pisos'] - mb - ps['olvidos'] != ps['nobj_final']: prob.append('objetos')
        if rep == 'inmediata' and ps['nobj_final'] != 36: prob.append('objetos')
        di(f"(C) {et}", not prob, f"nacimientos {nac} · fundadores {fun} · max vivos {ps['max_vivos']} · gen max "
                                   f"{max(x[1] for l in r['linajes'] for x in l['individuos'])}" + (f" PROBLEMAS {sorted(set(prob))}" if prob else ''))
        di(f"(H) {et}: crea = 9 + nacimientos + fundadores; nace = nacimientos", reg['crea'] == 9 + nac + fun and reg['nace'] == nac,
           f"crea {reg['crea']} nace {reg['nace']}")
        di(f"(H) {et}: quiere_parir recibe cola == vivos_linaje - 1", reg['qp'] > 0 and reg['cola_ok'] == reg['qp'], f"{reg['cola_ok']}/{reg['qp']}")
        if car in ('O1', 'O3'):
            di(f"(H) {et}: la memoria del padre llega al hijo (tabla no vacia)", reg['mem_no_vacia'] > 0, f"{reg['mem_no_vacia']}/{reg['nace']}")
        if car == 'FABRICA':
            di(f"(H) {et}: FABRICA hereda 'nada' (memoria None en todos los partos)", reg['mem_no_vacia'] == 0 and reg['nace'] > 0,
               f"{reg['mem_no_vacia']}/{reg['nace']}")
    # (K) control CTRL_O3_SINTERM
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location('carro_CTRL_O3_SINTERM', os.path.join(AQUI, 'carros_ctrl', 'CTRL_O3_SINTERM.py'))
    _m = _iu.module_from_spec(_sp); _sp.loader.exec_module(_m)
    RCm = _carga('revisa_carro', os.path.join(CARRERA, 'revisa_carro.py'))
    di("(K) CTRL_O3_SINTERM pasa el chequeo estatico y tiene TERMINAL = False", not RCm.revisa_fuente(open(_sp.origin, encoding='utf-8').read(), 'CTRL')
       and _m.TERMINAL is False and P1.carga_carro('O3').TERMINAL is True)
    a = N(P2.run(10014, ['O3'] * 9, T=1500, diag=0, solapadas=1)); b = N(P2.run(10014, [('O3', _m)] * 9, T=1500, diag=0, solapadas=1))
    for d in a['linajes'] + b['linajes']: d.pop('carro')
    di("(K) CTRL_O3_SINTERM == O3 bit a bit en la fisica mientras TERMINAL no puede dispararse (9 cuerpos, T=1500)", a == b,
       f"nacimientos {sum(l['nacimientos'] for l in b['linajes'])}")
    # (T)
    r = P2.run(10011, ['O2'] * 9, T=3000, diag=0, solapadas=1, reposicion='inmediata', tope_cuerpos=12)
    ps = r['pista']
    di("(T) tope 12 (9 O2 inmediata s=10011 T=3000): max vivos <= 12, bloqueados > 0, t_tope marcado",
       ps['max_vivos'] <= 12 and ps['bloqueados'] > 0 and ps['t_tope'] is not None and max(ps['tam_total']) <= 12,
       f"max {ps['max_vivos']} · bloqueados {ps['bloqueados']} · t_tope {ps['t_tope']}")
    # (G)
    def aborta(f):
        try: f(); return False
        except SystemExit: return True
    di("(G) solapadas=1 con compat=1 aborta", aborta(lambda: P2.run(1, ['FABRICA'], T=10, compat=1, pizarra=0, diag=0, solapadas=1)))
    di("(G) solapadas=1 con diag=1 aborta", aborta(lambda: P2.run(1, ['FABRICA'], T=10, solapadas=1)))
    di("(G) opciones de v2 con solapadas=0 abortan", aborta(lambda: P2.run(1, ['FABRICA'], T=10, tope_cuerpos=50)))
    di("(G) tope < n aborta", aborta(lambda: P2.run(1, ['FABRICA'] * 9, T=10, diag=0, solapadas=1, tope_cuerpos=5)))
    di("(G) reposicion desconocida aborta", aborta(lambda: P2.run(1, ['FABRICA'], T=10, diag=0, solapadas=1, reposicion='x')))
    out(f"\nRESULTADO: {OK[0]}/{OK[1]} · {time.time() - t0:.1f}s")
    SAL.close()
    return 0 if OK[0] == OK[1] else 1


if __name__ == '__main__':
    sys.exit(main())
