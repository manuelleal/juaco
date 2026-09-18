"""Arnes de identidad del instrumento del BLOQUE 2 (organismo_familias_b2.py). Regla 2 de registro/EQUIPO.md: un
instrumento construido por anclas debe ser su origen BIT A BIT con las perillas apagadas, y el arnes se corre y se
entrega con el trabajo.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin backprop
en el runtime, que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada.

  APAGADO TOTAL      : vira=0, exc_evita=-1, reg_b2=0  ==  organismo_familias.py (b9dd561a0cf056b8) en TODAS sus
                       claves, con mundo='AB' y con mundo='familias'.
  HERENCIA           : con mundo='AB'  ==  organismo_v14 (TRONCO, feefc88b1fd8d434) y, con desambiguar=1,
                       ==  organismo_v14_codigo_on (B-5). Lo hereda por la cadena, pero se COMPRUEBA aqui.
  RNG NO CONSUMIDO   : lo mismo a T = 120000 (si una sola linea nueva sorteara, los flujos divergirian).
  reg_b2 NO ALTERA   : reg_b2=1 no cambia NINGUNA clave compartida (es registro, no estado). Es la guarda que hace
                       legitimo medir con reg_b2=1 lo que se declaro identico con reg_b2=0.
  GEMELO DEL BLOQUE 2: con `cambio` por delante del horizonte, vira=8 y vira=-8 son la MISMA corrida bit a bit
                       (la base de P-S1: el brazo y su control comparten prefijo exacto).
  CONTROLES QUE DEBEN FALLAR: sin ellos el arnes pasaria por vacuidad (vira, exc_evita, mundo, renov, el gemelo
                       pasado el cambio).

Un proceso, sin Pool (regla 3 de EQUIPO.md). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/nivel12_mundo_familias/identidad_familias_b2.py
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREB, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_v14_codigo_on as B5ON
import organismo_familias as MF
import organismo_familias_b2 as B2

T = 20000
T_LARGO = 120000
T_CAMBIO = 60000                 # el gemelo del bloque 2 se comprueba a los dos lados de `cambio`
SEM = (1, 2, 3)
SHA_V14 = 'feefc88b1fd8d434'
SHA_B5ON = '2f7794d92e68cc89'
SHA_MF = 'b9dd561a0cf056b8'

# Perillas del mundo puestas pero INERTES porque mundo='AB'.
PERILLAS = dict(fam_D=12, fam_nvar=3, fam_F=8, fam_V=3, n_exc=4, n_neu=2, fam_val='barajado', deriva=1000,
                cambio=5000, vent=3000, crit_exp=0.5)
# El mundo de familias del bloque 1 (L y nobj derivados: PREREGISTRO_bloque1 2.7).
FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)
# Los dos escenarios del bloque 2, con `cambio` DENTRO del horizonte corto para que el gemelo se pueda romper.
GEN = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=8, n_neu=0, costo=0.008,
           deriva=max(T_CAMBIO // 3, 1), exc_evita=2, log_cada=250)
SAL = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=0, n_neu=0, costo=0.008,
           deriva=5000, cambio=T_CAMBIO // 2, log_cada=250)

NUEVAS_B2 = {'reg_b2', 'vira', 'exc_evita', 'cambio_b2', 'log_cada', 'viradas', 'val_post', 'primera_b2',
             'sep_exp', 'enc_post'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def compara(a, b, salta=()):
    """Devuelve la lista de claves de `a` que difieren en `b` (o faltan)."""
    return [k for k in a if k not in salta and N(a[k]) != N(b.get(k))] + \
           [k for k in a if k not in b and k not in salta]


def caso(etiq, fa, fb, t0, debe_diferir=False, semillas=SEM, tot=None, puerta=True, salta=()):
    ok = 0
    detalle = ''
    for s in semillas:
        a, b = fa(s), fb(s)
        dif = compara(a, b, salta)
        igual = not dif
        ok += int(igual != debe_diferir)
        if dif and not detalle:
            detalle = ' ' + str(dif[:5])
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    est = marca if ok == len(semillas) else ('FALLA' + detalle if puerta else 'NO DIFIERE' + detalle)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:60s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None and puerta:
        tot[0] += ok; tot[1] += len(semillas)
    return ok


if __name__ == '__main__':
    t0 = time.time()
    for nom, p, esp in [('organismo_v14.py (TRONCO CONGELADO)', os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                        ('organismo_v14_codigo_on.py (B-5)', os.path.join(CREB, 'organismo_v14_codigo_on.py'), SHA_B5ON),
                        ('organismo_familias.py (bloque 1, 43/43)', os.path.join(AQUI, 'organismo_familias.py'), SHA_MF),
                        ('escala_codigo.py (bloque 0)', os.path.join(AQUI, 'escala_codigo.py'), 'd8b8566bca77a0ae'),
                        ('construye_familias_b2.py', os.path.join(AQUI, 'construye_familias_b2.py'), None),
                        ('organismo_familias_b2.py', os.path.join(AQUI, 'organismo_familias_b2.py'), None)]:
        s = h16(p)
        aviso = '' if esp is None else ('  OK' if s == esp else f'  *** ESPERADO {esp}')
        print(f"  sha {nom:42s} {s}{aviso}")
    print(f"  T = {T} (ancla del rng: {T_LARGO}; gemelo: cambio = {T_CAMBIO//2} y {T_CAMBIO}), semillas {SEM}, UN proceso\n")

    tot = [0, 0]

    print("APAGADO TOTAL (vira=0, exc_evita=-1, reg_b2=0): organismo_familias_b2 == organismo_familias")
    for etiq, kw, Ti in [('(a) mundo=AB base', dict(), T),
                         ('(b) mundo=AB, inversion en T/2', dict(invertir_en=T // 2), T),
                         ('(c) mundo=AB, sin puerta', dict(puerta=None), T),
                         ('(d) mundo=AB, linaje v13 (mask_rel=0, puerta_pat=0)', dict(mask_rel=0, puerta_pat=0), T),
                         ('(e) mundo=AB, B-5 encendido (desambiguar=1)', dict(desambiguar=1), T),
                         ('(f) mundo=familias (bloque 1) tal cual', dict(FAM), T),
                         ('(g) mundo=familias con B-5 y neutros', dict(FAM, n_neu=2, desambiguar=1), T),
                         ('(h) mundo=familias con cambio y deriva del bloque 2', dict(SAL), T)]:
        caso(etiq, (lambda k, ti: lambda s: MF.run(s, T=ti, **k))(kw, Ti),
             (lambda k, ti: lambda s: B2.run(s, T=ti, **k))(kw, Ti), t0, tot=tot)

    print("\nRNG NO CONSUMIDO por ninguna linea nueva (ancla larga)")
    caso(f'(i) mundo=AB a T = {T_LARGO}', lambda s: MF.run(s, T=T_LARGO), lambda s: B2.run(s, T=T_LARGO),
         t0, semillas=SEM[:2], tot=tot)
    caso(f'(j) perillas del bloque 2 puestas, mundo=AB', lambda s: MF.run(s, T=T, **PERILLAS),
         lambda s: B2.run(s, T=T, vira=0, exc_evita=-1, reg_b2=0, **PERILLAS), t0, tot=tot)

    print("\nHERENCIA DE LA CADENA (se comprueba, no se supone)")
    caso('(k) mundo=AB == organismo_v14 (TRONCO)', lambda s: V14.run(s, T=T), lambda s: B2.run(s, T=T), t0, tot=tot)
    caso('(l) mundo=AB, desambiguar=1 == organismo_v14_codigo_on',
         lambda s: B5ON.run(s, T=T, desambiguar=1), lambda s: B2.run(s, T=T, desambiguar=1), t0, tot=tot)

    print("\nreg_b2 ES REGISTRO, NO ESTADO: reg_b2=1 no cambia ninguna clave compartida")
    for etiq, kw in [('(m) mundo=familias (bloque 1)', dict(FAM)),
                     ('(n) escenario G (deriva retenida, exc_evita=2)', dict(GEN)),
                     ('(o) escenario S con vira=8', dict(SAL, vira=8)),
                     ('(p) escenario S con vira=-8', dict(SAL, vira=-8))]:
        caso(etiq, (lambda k: lambda s: B2.run(s, T=T, reg_b2=0, **k))(kw),
             (lambda k: lambda s: B2.run(s, T=T, reg_b2=1, **k))(kw), t0, tot=tot, salta=tuple(NUEVAS_B2))

    print(f"\nGEMELO DEL BLOQUE 2 (base de P-S1): antes de `cambio` = {SAL['cambio']}, vira=8 y vira=-8 son LA MISMA corrida")
    caso('(q) T = cambio-1: vira=8 == vira=-8 (nunca se llega)',
         lambda s: B2.run(s, T=SAL['cambio'] - 1, reg_b2=1, vira=8, **SAL),
         lambda s: B2.run(s, T=SAL['cambio'] - 1, reg_b2=1, vira=-8, **SAL), t0, semillas=SEM[:2], tot=tot,
         salta=('vira', 'val_post'))

    print("\nCLAVES")
    kmf = set(MF.run(1, T=2000, **FAM))
    kb2 = set(B2.run(1, T=2000, **FAM))
    kb2r = set(B2.run(1, T=2000, reg_b2=1, **FAM))
    ok1 = (kb2 == kmf)
    ok2 = (kb2r - kb2 == NUEVAS_B2)
    print(f"  [{time.time()-t0:6.1f}s] {'(r) reg_b2=0: claves == organismo_familias':60s} "
          f"{'1/1 IDENTICO' if ok1 else '0/1 FALLA ' + str(kb2 ^ kmf)}", flush=True)
    print(f"  [{time.time()-t0:6.1f}s] {'(s) reg_b2=1: anade EXACTAMENTE las declaradas':60s} "
          f"{'1/1 IDENTICO' if ok2 else '0/1 FALLA ' + str((kb2r - kb2) ^ NUEVAS_B2)}", flush=True)
    tot[0] += int(ok1) + int(ok2); tot[1] += 2

    print("\nCONTROLES QUE DEBEN FALLAR (sin ellos el arnes pasaria por vacuidad)")
    caso('(t) vira=8 != vira=0 pasado el cambio (DEBE diferir)',
         lambda s: B2.run(s, T=T_CAMBIO, **SAL), lambda s: B2.run(s, T=T_CAMBIO, vira=8, **SAL),
         t0, debe_diferir=True, semillas=SEM[:2], tot=tot)
    caso('(u) vira=-8 != vira=0 pasado el cambio (DEBE diferir)',
         lambda s: B2.run(s, T=T_CAMBIO, **SAL), lambda s: B2.run(s, T=T_CAMBIO, vira=-8, **SAL),
         t0, debe_diferir=True, semillas=SEM[:2], tot=tot)
    caso('(v) vira=8 != vira=-8 pasado el cambio (DEBE diferir)',
         lambda s: B2.run(s, T=T_CAMBIO, vira=8, **SAL), lambda s: B2.run(s, T=T_CAMBIO, vira=-8, **SAL),
         t0, debe_diferir=True, semillas=SEM[:2], tot=tot)
    caso('(w) exc_evita=2 != exc_evita=-1 (DEBE diferir)',
         lambda s: B2.run(s, T=T, **{k: v for k, v in GEN.items() if k != 'exc_evita'}),
         lambda s: B2.run(s, T=T, **GEN), t0, debe_diferir=True, tot=tot)
    caso('(x) mundo=familias != mundo=AB (DEBE diferir)',
         lambda s: V14.run(s, T=T), lambda s: B2.run(s, T=T, **FAM), t0, debe_diferir=True, tot=tot)

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el paquete puede correr." if tot[0] == tot[1] else
                                              "  -> NO se corre nada hasta que sea 100%."))

    print("\nDIAGNOSTICO (NO es puerta): exc_evita=2 saca a la variante 2 de exc_win")
    r = B2.run(1, T=3000, reg_b2=1, **GEN)
    print(f"  exc_win con exc_evita=2: {r['exc_win']}   (ninguna debe terminar en v2)")
    r0 = B2.run(1, T=3000, reg_b2=1, **{k: v for k, v in GEN.items() if k != 'exc_evita'})
    print(f"  exc_win con exc_evita=-1: {r0['exc_win']}")
    rs = B2.run(1, T=3000, reg_b2=1, vira=8, **SAL)
    print(f"  viradas con vira=8: {rs['viradas']}")
    print(f"  val_post con vira=8: {rs['val_post']}")

    sys.exit(0 if tot[0] == tot[1] else 1)
