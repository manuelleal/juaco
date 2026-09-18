"""Arnes de identidad del instrumento del BLOQUE 3 (organismo_familias_b3.py = organismo_familias_b2 + la memoria de
pares con relevo de v15f). Regla 2 de registro/EQUIPO.md.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin backprop
en el runtime, que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada.

  APAGADO (memoria_pares=None): == organismo_familias_b2 en TODAS sus claves, con mundo='AB' y con mundo='familias',
                       y con las perillas del bloque 2 (vira, exc_evita, reg_b2) puestas.
  RNG NO CONSUMIDO   : lo mismo a T = 120000 con la perilla apagada.
  CADENA COMPLETA    : apagada y mundo='AB' == organismo_v14 (TRONCO feefc88b1fd8d434) y, con desambiguar=1,
                       == organismo_v14_codigo_on; y == organismo_familias (bloque 1) en su mundo.
  **RELEVO ON EN 'AB' == organismo_v15f_on (54d6efe0b564113c) BIT A BIT** -- la comprobacion que hace legitimo usar
                       el mecanismo de v15f en otra retina: con _D = 6, _NP = 15 y el modulo es v15f exacto,
                       incluido el consumo del rng en el desempate de la celda ganadora.
  GEMELO DEL BLOQUE 2: sigue valiendo con el relevo ENCENDIDO (vira=8 == vira=-8 antes de `cambio`): es la base de
                       P-S1, y sin ella el brazo S-REL no tendria control pareado.
  CONTROLES QUE DEBEN FALLAR: sin ellos el arnes pasaria por vacuidad.

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/nivel12_mundo_familias/identidad_familias_b3.py
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_v14_codigo_on as B5ON
import organismo_v15f_on as V15FON
import organismo_familias as MF
import organismo_familias_b2 as B2
import organismo_familias_b3 as B3

T = 20000
T_LARGO = 120000
T_CAMBIO = 60000
SEM = (1, 2, 3)
SHAS = {'organismo_v14.py (TRONCO CONGELADO)': (os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), 'feefc88b1fd8d434'),
        'organismo_v14_codigo_on.py (B-5)': (os.path.join(CREB, 'organismo_v14_codigo_on.py'), '2f7794d92e68cc89'),
        'organismo_v15f.py (creador A)': (os.path.join(CREA, 'organismo_v15f.py'), '96fc5c5262107850'),
        'organismo_v15f_on.py (perilla ON)': (os.path.join(CREA, 'organismo_v15f_on.py'), '54d6efe0b564113c'),
        'organismo_familias.py (bloque 1)': (os.path.join(AQUI, 'organismo_familias.py'), 'b9dd561a0cf056b8'),
        'organismo_familias_b2.py (bloque 2)': (os.path.join(AQUI, 'organismo_familias_b2.py'), '30200bea6a41c3c8'),
        'construye_familias_b3.py': (os.path.join(AQUI, 'construye_familias_b3.py'), None),
        'organismo_familias_b3.py': (os.path.join(AQUI, 'organismo_familias_b3.py'), None)}

FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)
GEN = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=8, n_neu=0, costo=0.008,
           deriva=max(T_CAMBIO // 3, 1), exc_evita=2, cambio=10**9, log_cada=250)
SAL = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=0, n_neu=0, costo=0.008,
           deriva=5000, cambio=T_CAMBIO // 2, log_cada=250)
PERILLAS = dict(fam_D=12, fam_nvar=3, fam_F=8, fam_V=3, n_exc=4, n_neu=2, fam_val='barajado', deriva=1000,
                cambio=5000, vent=3000, crit_exp=0.5)
# Las 10 claves que v15f anade SIEMPRE (tambien con la perilla apagada): identidad_v15f.py las declara igual.
NUEVAS_V15F = {'memoria_pares', 'mem_alfa', 'mem_ganadora', 'mem_tabla', 'mem_vistas', 'mem_cobertura',
               'mem_err_tabla', 'W_tabla', 'mem_fam', 'mem_ev'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def compara(a, b, salta=()):
    """Claves de `a` que difieren en `b` o faltan. Las claves EXTRA de `b` se declaran aparte (caso de conjunto)."""
    return [k for k in a if k not in salta and N(a[k]) != N(b.get(k))] + \
           [k for k in a if k not in b and k not in salta]


def caso(etiq, fa, fb, t0, debe_diferir=False, semillas=SEM, tot=None, puerta=True, salta=()):
    ok, detalle = 0, ''
    for s in semillas:
        dif = compara(fa(s), fb(s), salta)
        ok += int((not dif) != debe_diferir)
        if dif and not detalle:
            detalle = ' ' + str(dif[:5])
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    est = marca if ok == len(semillas) else ('FALLA' + detalle if puerta else 'NO DIFIERE' + detalle)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:62s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None and puerta:
        tot[0] += ok; tot[1] += len(semillas)
    return ok


if __name__ == '__main__':
    t0 = time.time()
    malo = False
    for nom, (p, esp) in SHAS.items():
        s = h16(p)
        aviso = '' if esp is None else ('  OK' if s == esp else f'  *** ESPERADO {esp}')
        malo = malo or (esp is not None and s != esp)
        print(f"  sha {nom:38s} {s}{aviso}")
    if malo:
        raise SystemExit("Un origen cambio. Reconstruir por anclas antes de seguir.")
    print(f"  T = {T} (ancla del rng: {T_LARGO}; gemelo: cambio = {T_CAMBIO//2}), semillas {SEM}, UN proceso\n")

    tot = [0, 0]

    print("APAGADO (memoria_pares=None): organismo_familias_b3 == organismo_familias_b2 en todas sus claves")
    for etiq, kw in [('(a) mundo=AB base', dict()),
                     ('(b) mundo=AB, inversion en T/2', dict(invertir_en=T // 2)),
                     ('(c) mundo=AB, sin puerta', dict(puerta=None)),
                     ('(d) mundo=AB, linaje v13 (mask_rel=0, puerta_pat=0)', dict(mask_rel=0, puerta_pat=0)),
                     ('(e) mundo=AB, B-5 encendido', dict(desambiguar=1)),
                     ('(f) mundo=familias (bloque 1)', dict(FAM)),
                     ('(g) escenario G del bloque 2 (reg_b2=1)', dict(GEN, reg_b2=1)),
                     ('(h) escenario S del bloque 2, vira=8, reg_b2=1', dict(SAL, vira=8, reg_b2=1)),
                     ('(i) escenario S del bloque 2, vira=-8, reg_b2=1', dict(SAL, vira=-8, reg_b2=1)),
                     ('(j) perillas del bloque 2 puestas, mundo=AB', dict(PERILLAS, vira=0, exc_evita=-1, reg_b2=0))]:
        caso(etiq, (lambda k: lambda s: B2.run(s, T=T, **k))(kw),
             (lambda k: lambda s: B3.run(s, T=T, memoria_pares=None, **k))(kw), t0, tot=tot)

    print("\nRNG NO CONSUMIDO por la memoria de pares apagada (ancla larga)")
    caso(f'(k) mundo=AB a T = {T_LARGO}', lambda s: B2.run(s, T=T_LARGO),
         lambda s: B3.run(s, T=T_LARGO, memoria_pares=None), t0, semillas=SEM[:2], tot=tot)

    print("\nCADENA COMPLETA (se comprueba hasta el TRONCO, no se supone)")
    caso('(l) apagada + mundo=AB == organismo_v14 (TRONCO)', lambda s: V14.run(s, T=T),
         lambda s: B3.run(s, T=T, memoria_pares=None), t0, tot=tot)
    caso('(m) apagada + mundo=AB + B-5 == organismo_v14_codigo_on', lambda s: B5ON.run(s, T=T, desambiguar=1),
         lambda s: B3.run(s, T=T, memoria_pares=None, desambiguar=1), t0, tot=tot)
    caso('(n) apagada + mundo=familias == organismo_familias (bloque 1)', lambda s: MF.run(s, T=T, **FAM),
         lambda s: B3.run(s, T=T, memoria_pares=None, **FAM), t0, tot=tot)

    print("\nRELEVO ENCENDIDO EN LA RETINA DE 6 px == organismo_v15f_on BIT A BIT (_D=6 -> _NP=15)")
    for etiq, kw in [("(o) v15f-ON base", dict()),
                     ("(p) v15f-ON, inversion en T/2", dict(invertir_en=T // 2)),
                     ("(q) v15f-ON, solap_AB=3 (E2L)", dict(solap_AB=3)),
                     ("(r) v15f-ON, sin puerta", dict(puerta=None)),
                     ("(s) v15f-ON, patron nuevo C", dict(nuevo='C', nuevo_en=T // 2))]:
        caso(etiq, (lambda k: lambda s: V15FON.run(s, T=T, **k))(kw),
             (lambda k: lambda s: B3.run(s, T=T, memoria_pares='relevo', **k))(kw), t0, tot=tot)
    caso(f'(t) v15f-ON a T = {T_LARGO} (el rng del desempate tambien)', lambda s: V15FON.run(s, T=T_LARGO),
         lambda s: B3.run(s, T=T_LARGO, memoria_pares='relevo'), t0, semillas=SEM[:2], tot=tot)

    print(f"\nGEMELO DEL BLOQUE 2 CON EL RELEVO ENCENDIDO (base de P-S1 para el brazo S-REL)")
    caso('(u) relevo ON: vira=8 == vira=-8 ANTES del cambio',
         lambda s: B3.run(s, T=SAL['cambio'] - 1, memoria_pares='relevo', reg_b2=1, vira=8, **SAL),
         lambda s: B3.run(s, T=SAL['cambio'] - 1, memoria_pares='relevo', reg_b2=1, vira=-8, **SAL),
         t0, semillas=SEM[:2], tot=tot, salta=('vira', 'val_post'))

    print("\nCLAVES")
    kb2 = set(B2.run(1, T=2000, reg_b2=1, **FAM))
    kb3 = set(B3.run(1, T=2000, memoria_pares=None, reg_b2=1, **FAM))
    ok1 = (kb3 - kb2 == NUEVAS_V15F)
    r0 = B3.run(1, T=2000, memoria_pares=None, reg_b2=1, **FAM)
    ok2 = all(r0[k] is None for k in ('memoria_pares', 'mem_ganadora', 'mem_tabla', 'mem_vistas', 'mem_cobertura',
                                      'mem_err_tabla', 'W_tabla'))
    r1 = B3.run(1, T=2000, memoria_pares='relevo', reg_b2=1, **FAM)
    ok3 = (len(r1['mem_tabla']) == 12 * 11 // 2) and (r1['mem_ganadora'] is not None)
    for et, ok in [('(v) apagada anade EXACTAMENTE las 10 claves de v15f', ok1),
                   ('(w) apagada: esas claves son None (inerte, no estado)', ok2),
                   ('(x) encendida con D=12: 66 celdas = C(12,2)', ok3)]:
        print(f"  [{time.time()-t0:6.1f}s] {et:62s} {'1/1 IDENTICO' if ok else '0/1 FALLA'}", flush=True)
        tot[0] += int(ok); tot[1] += 1

    print("\nCONTROLES QUE DEBEN FALLAR (sin ellos el arnes pasaria por vacuidad)")
    caso('(y) relevo != apagada en el mundo de familias (DEBE diferir)',
         lambda s: B3.run(s, T=T, memoria_pares=None, reg_b2=1, **SAL),
         lambda s: B3.run(s, T=T, memoria_pares='relevo', reg_b2=1, **SAL), t0, debe_diferir=True,
         tot=tot, salta=tuple(NUEVAS_V15F))
    caso('(z) relevo != v14.1 en mundo=AB (DEBE diferir)', lambda s: V14.run(s, T=T),
         lambda s: B3.run(s, T=T, memoria_pares='relevo'), t0, debe_diferir=True, tot=tot)
    caso('(A) relevo ON: vira=8 != vira=-8 PASADO el cambio (DEBE diferir)',
         lambda s: B3.run(s, T=T_CAMBIO, memoria_pares='relevo', reg_b2=1, vira=8, **SAL),
         lambda s: B3.run(s, T=T_CAMBIO, memoria_pares='relevo', reg_b2=1, vira=-8, **SAL),
         t0, debe_diferir=True, semillas=SEM[:2], tot=tot)

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el paquete puede correr." if tot[0] == tot[1] else
                                              "  -> NO se corre nada hasta que sea 100%."))

    print("\nDIAGNOSTICO (NO es puerta): que hace la memoria de pares con D = 12")
    r = B3.run(1, T=30000, memoria_pares='relevo', reg_b2=1, **SAL)
    vist = sum(1 for v in (r['W_tabla'] or {}).values() if v is not None)
    print(f"  celdas (pares) {len(r['mem_tabla'])}   ganadora {r['mem_ganadora']}   "
          f"casillas vistas en total {r['mem_vistas']}   cobertura de la ganadora {r['mem_cobertura']}/4")
    print(f"  estimulos cuya combinacion CONOCE la ganadora (leen la TABLA, no la lineal): {vist}/{len(r['W_tabla'])}")
    print(f"  error propio de la ganadora {r['mem_err_tabla']:.4f}")

    sys.exit(0 if tot[0] == tot[1] else 1)
