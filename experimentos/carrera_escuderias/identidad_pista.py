"""identidad_pista.py — ANCLA OBLIGATORIA de la pista (REGLAMENTO sec. 3; regla 2 de EQUIPO.md).

MISION: llegar a la AGI por este camino. Se corre y se pega ENTERO en el informe ANTES de mirar un solo
numero de la carrera. Un proceso, sin Pool.

  (0) SHA: organismo_f9c.py es el que se leyo (pista.SHA_F9C).
  (A) UN carro FABRICA, pizarra apagada, compat=1 == organismo_f9c.run(**corre_bloque2.BRAZOS['REL'])
      BIT A BIT en TODAS las claves del monolito (la unica extra permitida es '_carrera', telemetria de la
      carrera) Y el rng del mundo queda en el MISMO estado final (mismo consumo). 6 semillas x T=20000.
  (B) idem a T=100000, 2 semillas (1601, 1602: la replica del bloque 2).
  (C) idem con rep_acum=1 (la perilla del mundo que la reglamento no fija), 2 semillas x T=20000.
  (D) EL CANAL NO TOCA NADA si nadie escribe: FABRICA con pizarra=1 == pizarra=0 (compat=0; n=1 y n=3).
  (E) DEBEN DIFERIR (ERR-38): compat=0 != compat=1 (otros rng); el linaje 0 con 3 cuerpos != solo
      (la competencia por la comida NO es inerte).
  (F) DETERMINISMO: 9 FABRICA, T=3000, dos llamadas -> mismo dict.
  (G) GUARDIAS: compat con 2 carros, compat con pizarra, 10 carros, escritura invalida, mov invalido -> SystemExit.
  (H) EL CANAL LLEGA: un carro de prueba que escribe; lo escrito en t aparece en la pizarra de t+1 (no en t),
      cupo 16 FIFO, y con pizarra=0 se descarta.
  (I) ENMIENDA 1: con N = 1, escala=1 == escala=0; con N = 9, L = 360 y nobj = 36; la pizarra COMPLETA se
      guarda aparte.
  (K) OPCION A: FABRICA toma L de la pista; con N = 9 la boca decide siempre sobre la celda real; determinista
      y contabilidad coherente.
  (L) El DIAGNOSTICO (objetivo robado, perdidas, distancias) es SOLO LECTURA: diag=1 == diag=0.
  (J) H-4: cfg_fabrica = firma de organismo_f9c.run + BRAZOS['REL']; una rama no portada aborta; la
      constante derivada se usa (eta distinta -> corrida distinta).
Desde ERR-96 la salida tiene dos espacios de nombres: se compara pista.plano(d) (fisica + d['carro']).
(D), (E2), (F) y (G) con varios FABRICA usan escala=0 (el mundo sin escalar, como en su primera version).
Uso:  python experimentos/carrera_escuderias/identidad_pista.py   (escribe identidad_pista_salida.txt)
"""
import json, os, sys, time, types

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2'),
                os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo'), os.path.join(RAIZ, 'experimentos', 'nivel13_alma'),
                os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo'), os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO de los del tronco (ERR-28)
_argv = sys.argv; sys.argv = [sys.argv[0]]
import numpy as np
import corre_bloque2 as CB
import organismo_f9c as F9C
import pista as P
sys.argv = _argv

N = lambda x: json.loads(json.dumps(x, default=str))
REL = CB.BRAZOS['REL']
OK = [0, 0]
SAL = open(os.path.join(AQUI, 'identidad_pista_salida.txt'), 'w', encoding='utf-8')


def out(s=''):
    print(s, flush=True); SAL.write(s + '\n'); SAL.flush()


def di(et, ok, extra=''):
    OK[1] += 1; OK[0] += int(bool(ok))
    out(f"  {'OK   ' if ok else 'FALLA'} {et}   {extra}")


def monolito(seed, T, **kw):
    """organismo_f9c.run con el rng del mundo CAPTURADO (se envuelve default_rng solo durante la llamada)."""
    orig = np.random.default_rng; cap = []
    def w(*a, **k):
        r = orig(*a, **k); cap.append((a, r)); return r
    np.random.default_rng = w
    try:
        r = F9C.run(seed, T=T, **dict(REL, **kw))
    finally:
        np.random.default_rng = orig
    mundo = [g for a, g in cap if a == (seed,)]
    hijos = sum(1 for a, g in cap if a and isinstance(a[0], int) and a[0] >= 700000 + 1000000 * seed)
    return r, (P._estado(mundo[0]) if len(mundo) == 1 else None), hijos


def compara(a, b):
    falta = [k for k in a if k not in b]
    dif = [k for k in a if k in b and N(a[k]) != N(b[k])]
    extra = [k for k in b if k not in a and k != '_carrera']
    return falta, dif, extra


def ancla(et, seed, T, **kw):
    t0 = time.time(); a, est_a, nh = monolito(seed, T, **kw); t1 = time.time()
    rb = P.run(seed, ['FABRICA'], T=T, pizarra=0, compat=1, **kw); t2 = time.time()
    b = P.plano(rb['linajes'][0]); est_b = rb['pista']['rng_mundo_estado']   # ERR-96: fisica + d['carro'] sin choques
    falta, dif, extra = compara(a, b)
    ok = not falta and not dif and not extra and est_a is not None and est_a == est_b and b['nacimientos'] == nh
    R0a = round(a['descendientes'] / (a['deaths'] + 1), 4); R0b = round(b['descendientes'] / (b['deaths'] + 1), 4)
    di(f"{et} s={seed} T={T} {kw if kw else ''}", ok,
       f"claves {len(a)} · falta {falta[:3]} dif {dif[:3]} extra {extra[:3]} · R0 {R0a}/{R0b} desc {a['descendientes']}/{b['descendientes']} "
       f"muertes {a['deaths']}/{b['deaths']} vidas {len(a['vidas_h1'])}/{len(b['vidas_h1'])} fund {a['fundadores']}/{b['fundadores']} · "
       f"rng mundo {est_a}/{est_b} · rng hijos {nh}/{b['nacimientos']} · {t1-t0:.1f}s monolito / {t2-t1:.1f}s pista")
    return a, b


class _Escritor:
    """Carro de PRUEBA (solo del arnes): se mueve como quiera el rng, no muerde, escribe (t, indice) cada paso
    y guarda lo que leyo."""
    def __init__(self, ctx, malo=None): self.rng = ctx['rng']; self.i = ctx['indice']; self.leido = []; self.malo = malo
    def actua(self, o):
        self.leido.append((o['t'], tuple(e[0] for e in o['pizarra'])))
        self.vistos = getattr(self, 'vistos', []); self.vistos.extend(o['cuerpos'])
        if self.malo == 'escr': return dict(mov=0, muerde=False, escribe=('x',))
        if self.malo == 'mov': return dict(mov=2, muerde=False)
        return dict(mov=int(self.rng.integers(3)) - 1, muerde=False, escribe=(o['t'], self.i))
    def resultado(self, r): pass
    def fin_paso(self, i): pass
    def muere(self, i): pass
    def nace(self, i): pass
    def al_parir(self, i): return None


def mod_escritor(malo=None, guarda=None):
    m = types.SimpleNamespace()
    def crea(ctx):
        c = _Escritor(ctx, malo)
        if guarda is not None: guarda.append(c)
        return c
    m.crea = crea
    return m


def aborta(f):
    try:
        f(); return False, 'NO aborto'
    except SystemExit as e:
        return True, str(e)[:90]


def main():
    t0 = time.time()
    out(f"IDENTIDAD DE LA PISTA · {time.strftime('%Y-%m-%d %H:%M:%S')} · UN proceso, sin Pool · python {sys.version.split()[0]} · numpy {np.__version__}")
    out(f"  pista.py sha {P.h16(os.path.join(AQUI,'pista.py'))} · carros/FABRICA.py sha {P.h16(os.path.join(AQUI,'carros','FABRICA.py'))}")
    out("\n(0) SHA DEL ORIGEN")
    s = P.h16(P.ORIGEN); di('organismo_f9c.py', s == P.SHA_F9C, f"{s} (se espera {P.SHA_F9C})")
    out(f"\n(A) ANCLA: 1 FABRICA, pizarra 0, compat 1 == organismo_f9c REL (rep_acum 0) · T=20000 · 6 semillas")
    for sd in (1, 2, 3, 4, 5, 6): ancla('(A)', sd, 20000)
    out("\n(B) ANCLA a T=100000 · 2 semillas (replica del bloque 2)")
    for sd in (1601, 1602): ancla('(B)', sd, 100000)
    out("\n(C) ANCLA con rep_acum=1 · T=20000")
    for sd in (1, 2): ancla('(C)', sd, 20000, rep_acum=1)
    out("\n(D) EL CANAL NO TOCA NADA si nadie escribe (compat 0)")
    for n in (1, 3):
        a = P.run(7, ['FABRICA'] * n, T=5000, pizarra=0, escala=0); b = P.run(7, ['FABRICA'] * n, T=5000, pizarra=1, escala=0)
        # se compara TODO salvo el eco de configuracion pista['pizarra'] (1a corrida del arnes: 23/25 por comparar ese eco)
        pa = {k: v for k, v in a['pista'].items() if k != 'pizarra'}; pb = {k: v for k, v in b['pista'].items() if k != 'pizarra'}
        di(f"(D) n={n} pizarra 1 == 0 (linajes + pista salvo el eco 'pizarra')", N(a['linajes']) == N(b['linajes']) and N(pa) == N(pb),
           f"R0 linaje 0 {a['linajes'][0]['descendientes']}/{a['linajes'][0]['deaths']+1} · rng mundo {pa['rng_mundo_estado']}/{pb['rng_mundo_estado']}")
    out("\n(E) DEBEN DIFERIR (ERR-38)")
    a = P.run(1, ['FABRICA'], T=20000, pizarra=0, compat=1)['linajes'][0]
    b = P.run(1, ['FABRICA'], T=20000, pizarra=0, compat=0)['linajes'][0]
    di('(E1) compat 0 != compat 1 (rng separados)', N(a) != N(b), f"muertes {a['deaths']} vs {b['deaths']}")
    s1 = P.run(1, ['FABRICA'], T=20000, pizarra=0)['linajes'][0]
    s3 = P.run(1, ['FABRICA'] * 3, T=20000, pizarra=0, escala=0)['linajes'][0]
    di('(E2) linaje 0 con 3 cuerpos != solo (la comida compartida no es inerte)', N(s1) != N(s3),
       f"exposiciones A solo {s1['exposiciones']['A']} vs con 3 {s3['exposiciones']['A']}")
    out("\n(F) DETERMINISMO")
    a = P.run(11, ['FABRICA'] * 9, T=3000, escala=0); b = P.run(11, ['FABRICA'] * 9, T=3000, escala=0)
    di('(F) 9 FABRICA T=3000 dos veces', N(a) == N(b), f"muertes {[l['deaths'] for l in a['linajes']]}")
    out("\n(G) GUARDIAS (deben abortar)")
    for et, f in [('compat con 2 carros', lambda: P.run(1, ['FABRICA'] * 2, T=10, pizarra=0, compat=1, escala=0)),
                  ('compat con pizarra', lambda: P.run(1, ['FABRICA'], T=10, pizarra=1, compat=1)),
                  ('10 carros', lambda: P.run(1, ['FABRICA'] * 10, T=10, escala=0)),
                  ('escritura invalida', lambda: P.run(1, [('X', mod_escritor('escr'))], T=10)),
                  ('mov invalido', lambda: P.run(1, [('X', mod_escritor('mov'))], T=10)),
                  ('carro inexistente', lambda: P.run(1, ['NO_EXISTE'], T=10))]:
        ok, msg = aborta(f); di(f"(G) {et}", ok, msg)
    out("\n(H) EL CANAL LLEGA")
    g = []
    r = P.run(3, [('W', mod_escritor(guarda=g)), ('W', mod_escritor(guarda=g))], T=40, pizarra=1, escala=0)
    le = g[0].leido
    ok1 = all(all(tt < t for tt in ts) for t, ts in le) and any(ts and max(ts) == t - 1 for t, ts in le if t > 0)
    ok2 = max(len(ts) for _, ts in le) == P.CUPO and len(r['pista']['pizarra_final']) == P.CUPO
    di('(H1) lo escrito en t se lee en t+1, nunca en t', ok1, f"t=5 lee {le[5][1]}")
    di('(H2) cupo 16 FIFO', ok2, f"max leido {max(len(ts) for _, ts in le)} · final {len(r['pista']['pizarra_final'])} · escrituras {[l['_carrera']['escrituras'] for l in r['linajes']]}")
    g = []
    r = P.run(3, [('W', mod_escritor(guarda=g))], T=40, pizarra=0)
    di('(H3) pizarra=0: nada se lee, todo se descarta', all(not ts for _, ts in g[0].leido) and r['pista']['escrituras_descartadas'] == 40,
       f"descartadas {r['pista']['escrituras_descartadas']}")
    out("\n(I) ENMIENDA 1 (escala): con N = 1, escala=1 == escala=0 (la pista original)")
    a = P.run(5, ['FABRICA'], T=20000, pizarra=0, escala=1); b = P.run(5, ['FABRICA'], T=20000, pizarra=0, escala=0)
    pa = {k: v for k, v in a['pista'].items() if k != 'escala'}; pb = {k: v for k, v in b['pista'].items() if k != 'escala'}
    di('(I1) N=1: escala 1 == escala 0 (linajes + pista salvo el eco)', N(a['linajes']) == N(b['linajes']) and N(pa) == N(pb),
       f"L {a['pista']['L']} nobj {a['pista']['nobj']}")
    g = []
    r = P.run(3, [('W', mod_escritor(guarda=g))] * 9, T=200, pizarra=1, escala=1)
    di('(I2) N=9 escala 1: L = 360, nobj = 36, siempre 36 objetos en el mundo', r['pista']['L'] == 360 and r['pista']['nobj'] == 36
       and abs(sum(r['pista']['comp_mundo'].values()) - 36) < 1e-9 and max(c[1] for c in g[0].vistos) < 360 and max(c[1] for c in g[0].vistos) >= 40,
       f"L {r['pista']['L']} nobj {r['pista']['nobj']} comp {r['pista']['comp_mundo']} · pos max vista {max(c[1] for c in g[0].vistos)}")
    di('(I3) la pizarra COMPLETA se guarda aparte (pizarra_log = todas las escrituras, sin tope)',
       r['pista']['pizarra_n'] == 1800 == len(r['pizarra_log']), f"{len(r['pizarra_log'])} entradas (9 x 200); primera {r['pizarra_log'][0]}")
    out("\n(K) OPCION A: FABRICA toma L de la pista (N = 1: L = 40 -> las anclas A/B/C de arriba siguen bit a bit)")
    FAB0 = P.carga_carro('FABRICA')
    class Espia(FAB0.Carro):
        """SOLO del arnes: comprueba que la celda donde el carro decidio la boca es la celda donde la pista lo puso."""
        malas = 0; decis = 0
        def resultado(self, res):
            if res['letra'] is not None:
                Espia.decis += 1; Espia.malas += int(self._enc is None or self._enc[0] != res['pos'])
            super().resultado(res)
    r9 = P.run(4001, [('FABRICA', types.SimpleNamespace(crea=lambda ctx: Espia(ctx)))] * 9, T=3000, escala=1)
    di('(K1) N=9, L=360: la boca decide SIEMPRE sobre la celda real (0 desajustes de L)', Espia.decis > 0 and Espia.malas == 0,
       f"decisiones de boca {Espia.decis} · desajustes {Espia.malas} · L {r9['pista']['L']}")
    import juez as J
    coh = [J.resumen_linaje(d, 4001)['coherente'] for d in r9['linajes']]
    r9b = P.run(4001, [('FABRICA', types.SimpleNamespace(crea=lambda ctx: Espia(ctx)))] * 9, T=3000, escala=1)
    di('(K2) N=9 escala 1: determinista y contabilidad fisica coherente 9/9', N(r9) == N(r9b) and all(coh),
       f"muertes {[d['deaths'] for d in r9['linajes']]} · mordidas {[sum(sum(v) for v in d['mord'].values()) for d in r9['linajes']]}")
    out("\n(L) EL DIAGNOSTICO ES SOLO LECTURA: diag=1 == diag=0 salvo _carrera['diag']")
    for et, kw in (('N=1 compat', dict(carros=['FABRICA'], compat=1, pizarra=0)), ('N=9 escala', dict(carros=['FABRICA'] * 9, escala=1)),
                   ('N=9 sin escala', dict(carros=['FABRICA'] * 9, escala=0))):
        a = P.run(2, T=3000, diag=1, **kw); b = P.run(2, T=3000, diag=0, **kw)
        for d in a['linajes']: d['_carrera'].pop('diag')
        di(f"(L) {et}", N(a) == N(b), f"rng mundo {a['pista']['rng_mundo_estado']}/{b['pista']['rng_mundo_estado']}")
    out("\n(J) H-4: las constantes de FABRICA se DERIVAN de BRAZOS['REL'] y una rama no portada ABORTA")
    cf = P.cfg_fabrica(); kw = cf['kw']
    di('(J1) cfg_fabrica = firma de organismo_f9c.run + corre_bloque2.BRAZOS[REL]',
       all(kw[k] == v for k, v in CB.BRAZOS['REL'].items() if k != 'alma') and kw['eta'] == 0.03 and kw['nobj'] == 4 and cf['L'] == 40,
       f"{len(kw)} perillas · costo {kw['costo']} · rep_X {kw['rep_X']} · nodo_lee {kw['nodo_lee']} · motivo {kw['alma_motivo']!r}")
    FAB = P.carga_carro('FABRICA')
    for k, v in (('nodo_rel', 2), ('nodo_via', 2), ('puerta_pat', 0), ('eta_pred', 0.1)):
        def crea(ctx, k=k, v=v):
            ctx['fabrica']['kw'][k] = v; return FAB.crea(ctx)
        ok, msg = aborta(lambda crea=crea: P.run(1, [('F', types.SimpleNamespace(crea=crea))], T=10))
        di(f"(J2) {k}={v} -> FABRICA aborta", ok, msg)
    def crea_eta(ctx):
        ctx['fabrica']['kw']['eta'] = 0.06; return FAB.crea(ctx)
    a = P.run(1, ['FABRICA'], T=5000, pizarra=0); b = P.run(1, [('FABRICA', types.SimpleNamespace(crea=crea_eta))], T=5000, pizarra=0)
    di('(J3) la constante derivada SE USA: eta 0.06 cambia la corrida (ERR-38)', N(a['linajes'][0]['carro']) != N(b['linajes'][0]['carro']),
       f"splits {a['linajes'][0]['carro']['splits']} vs {b['linajes'][0]['carro']['splits']}")
    out(f"\nTOTAL {OK[0]}/{OK[1]} en {time.time()-t0:.1f}s")
    SAL.close()
    return 0 if OK[0] == OK[1] else 1


if __name__ == '__main__':
    sys.exit(main())
