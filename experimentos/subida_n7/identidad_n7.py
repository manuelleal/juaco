"""identidad_n7.py -- arnes de identidad BIT A BIT del bloque N7-NL (se corre ANTES de mirar numeros de la serie).

  (A) mundo_n7(desambiguar=0, norm_lenta=0) == mundo_composicion_v14 (a9098933b1950e3d), TODAS las claves
      (salvo las nuevas de solo lectura): brazos C3/C3C, k = 1, 3, 5, semillas 1-2, con los kwargs de v14.0
      (eta_s 0.015) y con los del tronco v14.2 (eta_s 0.15, clip_s 10); + mask_rel=4 (control AZAR) k=5.
  (B) organismo_v142N(norm_lenta=0) == organismo_v142 (TRONCO, CONGELADO): los 12 escenarios de
      organismo/identidad_v142.py, semillas 1-2.
  (C) organismo_v142gN(norm_lenta=0) == organismo_v142g en el mundo de regla (px0, xor01, azar), semillas 1-2.
  (I) INERCIA predicha (perilla ENCENDIDA) en los mundos del tronco: organismo_v142N(norm_lenta=1) == organismo_v142
      y organismo_v142gN(norm_lenta=1) == organismo_v142g en los mismos escenarios (P.P = 3 -> factor 1.0 exacto).
  (K) kwargs del runner (corre_n7.TRONCO) == defaults de organismo_v142.run CAMPO A CAMPO; NKMAX 90; techo 3.
Uso: python experimentos/subida_n7/identidad_n7.py [T]   (T por defecto 20000). Sale con 1 si algo falla.
"""
import hashlib, inspect, json, os, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'nivel10_composicion_v14')]
import mundo_n7 as MN7
import mundo_composicion_v14 as MC14
import organismo_v142 as V142
import organismo_v142g as V142G
import organismo_v142N as V142N
import organismo_v142gN as V142GN
import corre_n7 as C

NUEVAS = {'desambiguar', 'norm_lenta', 'n_des', 'Wps_sum', 'Wns_sum'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(d):
    return json.loads(json.dumps({k: v for k, v in d.items() if k not in NUEVAS}, default=str))


def dif(a, b):
    a, b = N(a), N(b)
    return [k for k in set(a) | set(b) if a.get(k, '<falta>') != b.get(k, '<falta>')]


if __name__ == '__main__':
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    t0 = time.time()
    for nom, p in [('mundo_composicion_v14 (origen)', MC14.__file__), ('mundo_n7', MN7.__file__),
                   ('organismo_v142 (TRONCO)', V142.__file__), ('organismo_v142g', V142G.__file__),
                   ('organismo_v142N', V142N.__file__), ('organismo_v142gN', V142GN.__file__),
                   ('corre_n7', C.__file__), ('este arnes', os.path.abspath(__file__))]:
        print(f'  sha {nom:32s} {h16(p)}')
    cuenta = {}

    def anota(bloque, etq, d):
        o, t = cuenta.get(bloque, (0, 0)); cuenta[bloque] = (o + (not d), t + 1)
        print(f'  [{time.time()-t0:5.0f}s] {bloque} {etq:58s} {"IDENTICO" if not d else "DIFIERE " + str(sorted(d)[:6])}', flush=True)

    print(f'\n--- (A) mundo_n7 apagado == mundo_composicion_v14, T={T} ---')
    base = dict(C.TRONCO); base.update(C.MUNDO); base.pop('desambiguar')
    v140 = dict(base, eta_s=0.015, clip_s=3.0)
    for cfg_n, cfg in [('v14.0', v140), ('v14.2', base)]:
        for arm in ('C3', 'C3C'):
            for k in (1, 3, 5):
                for s in (1, 2):
                    a = MN7.run(s, arm=arm, kprof=k, T=T, desambiguar=0, norm_lenta=0, **cfg)
                    b = MC14.run(s, arm=arm, kprof=k, T=T, **cfg)
                    anota('A', f'{cfg_n} {arm} k={k} s{s}', dif(a, b))
    for s in (1, 2):
        a = MN7.run(s, arm='C3', kprof=5, T=T, desambiguar=0, norm_lenta=0, **dict(v140, mask_rel=4))
        b = MC14.run(s, arm='C3', kprof=5, T=T, **dict(v140, mask_rel=4))
        anota('A', f'v14.0 C3 mask_rel=4 k=5 s{s}', dif(a, b))

    ESC = [('AB por defecto', dict()), ('AB invertido', dict(invertir_en=15000)),
           ('AB + patron nuevo C', dict(nuevo='C', nuevo_en=15000)), ('AB solap_AB=3 (E2L)', dict(solap_AB=3)),
           ('AB sin plasticidad', dict(plast=False)), ('AB via lenta apagada', dict(eta_s=0.0)),
           ('AB sin puerta', dict(puerta=None)), ('AB sin division por signo', dict(div_signo=False)),
           ('AB sin hija dispersa', dict(mask_rel=0)), ('AB sin puerta por codigo', dict(puerta_pat=0)),
           ('AB las dos perillas v14 off', dict(mask_rel=0, puerta_pat=0)),
           ('AB D comida solap_B=2 (E2K)', dict(nuevo='D', nuevo_val='comida', solap_B=2, nuevo_en=15000))]
    print(f'\n--- (B) organismo_v142N(0) == organismo_v142  y  (I) organismo_v142N(1) == organismo_v142, T={T} ---')
    for etq, kw in ESC:
        for s in (1, 2):
            ref = V142.run(s, T=T, **kw)
            anota('B', f'{etq} s{s}', dif(ref, V142N.run(s, T=T, norm_lenta=0, **kw)))
            anota('I', f'{etq} s{s} (perilla ON)', dif(ref, V142N.run(s, T=T, norm_lenta=1, **kw)))
    KWG = dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, puerta_pat=5, pat_min=1)
    print(f'\n--- (C) organismo_v142gN(0) == organismo_v142g  y  (I) con la perilla ON, mundo de regla, T={T} ---')
    for regla in ('px0', 'xor01', 'azar'):
        for s in (1, 2):
            ref = V142G.run(s, T=T, mundo='regla', regla=regla, **KWG)
            anota('C', f'regla/{regla} s{s}', dif(ref, V142GN.run(s, T=T, mundo='regla', regla=regla, norm_lenta=0, **KWG)))
            anota('I', f'regla/{regla} s{s} (perilla ON)', dif(ref, V142GN.run(s, T=T, mundo='regla', regla=regla, norm_lenta=1, **KWG)))

    print('\n--- (K) kwargs del runner campo a campo contra organismo_v142.run ---')
    sig = inspect.signature(V142.run).parameters
    for c, v in C.TRONCO.items():
        d = [] if (c in sig and sig[c].default == v) else [f'{c}: runner {v} / tronco {sig[c].default if c in sig else "<no existe>"}']
        anota('K', f'{c} = {v}', d)
    anota('K', 'NKMAX del tronco == nkmax del mundo (90)', [] if V142.NKMAX == C.MUNDO['nkmax'] else ['NKMAX'])
    txt = open(V142.__file__, encoding='utf-8').read()
    anota('K', 'techo de Wp/Wn del tronco == wclip del mundo (3.)', [] if ('np.clip(Wp+eta*dlt*kc,0,3.)' in txt and C.MUNDO['wclip'] == 3.0) else ['wclip'])
    anota('K', 'K=3 celdas por codigo (tronco == mundo)', [] if V142.K == MN7.K == 3 else ['K'])

    print()
    todo = True
    for b, (o, t) in sorted(cuenta.items()):
        todo &= (o == t)
        print(f'  {"PASA" if o == t else "FALLA":5s} ({b}) {o}/{t}')
    ot = sum(o for o, _ in cuenta.values()); tt = sum(t for _, t in cuenta.values())
    print(f'\nVEREDICTO identidad_n7: {"PASA" if todo else "NO PASA"}  {ot}/{tt}  ({time.time()-t0:.0f}s)')
    sys.exit(0 if todo else 1)
