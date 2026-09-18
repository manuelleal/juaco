"""Arnes de identidad del MUNDO DE FAMILIAS (bloque 1, nivel 12). Regla 2 de registro/EQUIPO.md: un instrumento nuevo
construido por anclas debe ser su origen BIT A BIT con las perillas apagadas, y el arnes se corre y se entrega con el
trabajo. El encargo pide >= 24 comprobaciones; aqui hay 43 de puerta + 3 de diagnostico.

  APAGADO (mundo='AB')      : organismo_familias == organismo_v14 en TODAS las claves de v14.
  RNG NO CONSUMIDO          : lo mismo a T = 120000 (si una sola linea nueva sorteara, los flujos divergirian).
  PERILLAS DECLARADAS       : con todas las perillas del mundo puestas pero mundo='AB', sigue siendo v14 bit a bit.
  CLAVES                    : con mundo='AB' el conjunto de claves es el de organismo_v14_codigo_on (= v14 + las TRES
                              de solo lectura de B-5: desambiguar, des_splits, des_t); las del mundo de familias
                              aparecen SOLO con mundo='familias'.
  B-5 COMPUESTO             : mundo='AB', desambiguar=1  ==  experimentos/creacion_B/organismo_v14_codigo_on.py.
  INERCIA DE B-5 (P7a)      : mundo='familias', n_neu=0, desambiguar=1 == el mismo con desambiguar=0 (el disparador
                              de B-5 es R == 0, y con n_neu=0 toda mordida tiene consecuencia).
  CONTROLES QUE DEBEN FALLAR: sin ellos el arnes pasaria por vacuidad.
  DIAGNOSTICO (no puerta)   : con n_neu=2, desambiguar=1 deberia DIFERIR; si no difiere, es P7b(i) cayendo -- un
                              RESULTADO, no un fallo del instrumento. Por eso se reporta y no bloquea.

Un proceso, sin Pool (regla 3 de EQUIPO.md). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/nivel12_mundo_familias/identidad_familias.py
"""
import hashlib, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREB, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_v14_codigo_on as B5ON
import organismo_familias as MF

T = 20000
T_LARGO = 120000                 # ancla del rng (PREREGISTRO 3)
SEM = (1, 2, 3)
SHA_V14 = 'feefc88b1fd8d434'
SHA_B5ON = '2f7794d92e68cc89'

# Perillas del mundo puestas pero INERTES porque mundo='AB' (caso J).
PERILLAS = dict(fam_D=12, fam_nvar=3, fam_F=8, fam_V=3, n_exc=4, n_neu=2, fam_val='barajado', deriva=1000,
                cambio=5000, vent=3000, crit_exp=0.5)
# El mundo de familias, con los valores preregistrados (L y nobj derivados: PREREGISTRO 2.7).
FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)

NUEVAS = {'mundo', 'fam', 'val_mundo', 'exc', 'exc_win', 'herm', 'cod0', 'exposiciones', 'exp_asoc', 'primera',
          'ultima', 'ruta', 'colateral', 'omision', 'colateral_tot', 't_exc', 'w_var', 'w_var_med', 'renovados',
          'frac_veneno', 'frac_regalo'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def solo_base(d):
    return {k: v for k, v in d.items() if k not in NUEVAS}


def caso(etiq, mod_ref, kw_ref, kw_mf, t0, debe_diferir=False, semillas=SEM, Ti=T, tot=None):
    ok = 0
    detalle = ''
    for s in semillas:
        a = mod_ref.run(s, T=Ti, **kw_ref)
        b = MF.run(s, T=Ti, **kw_mf)
        base = solo_base(b)
        dif = [k for k in a if a[k] != base.get(k)]
        falta = [k for k in a if k not in b]
        igual = not dif and not falta
        ok += int(igual != debe_diferir)
        if dif and not detalle:
            detalle = ' ' + str(dif[:5])
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    print(f"  [{time.time()-t0:6.1f}s] {etiq:56s} {ok}/{len(semillas)} "
          f"{marca if ok == len(semillas) else 'FALLA' + detalle}", flush=True)
    if tot is not None:
        tot[0] += ok; tot[1] += len(semillas)
    return ok, len(semillas)


def caso_mf(etiq, kw_a, kw_b, t0, debe_diferir=False, semillas=SEM, Ti=T, tot=None, puerta=True):
    """Compara organismo_familias consigo mismo (dos juegos de perillas). Para P7a y el diagnostico Q."""
    ok = 0
    detalle = ''
    for s in semillas:
        a = MF.run(s, T=Ti, **kw_a)
        b = MF.run(s, T=Ti, **kw_b)
        dif = [k for k in a if k not in ('des_splits', 'des_t', 'desambiguar') and a[k] != b.get(k)]
        igual = not dif
        ok += int(igual != debe_diferir)
        if dif and not detalle:
            detalle = ' ' + str(dif[:5])
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    est = marca if ok == len(semillas) else ('FALLA' + detalle if puerta else 'NO DIFIERE' + detalle)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:56s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None and puerta:
        tot[0] += ok; tot[1] += len(semillas)
    return ok, len(semillas)


if __name__ == '__main__':
    t0 = time.time()
    for nom, p, esp in [('organismo_v14.py (TRONCO CONGELADO)', os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                        ('organismo_v14_codigo_on.py (B-5)', os.path.join(CREB, 'organismo_v14_codigo_on.py'), SHA_B5ON),
                        ('escala_codigo.py (bloque 0)', os.path.join(AQUI, 'escala_codigo.py'), None),
                        ('construye_familias.py', os.path.join(AQUI, 'construye_familias.py'), None),
                        ('organismo_familias.py', os.path.join(AQUI, 'organismo_familias.py'), None)]:
        s = h16(p)
        aviso = '' if esp is None else ('  OK' if s == esp else f'  *** ESPERADO {esp}')
        print(f"  sha {nom:38s} {s}{aviso}")
    print(f"  modulo organismo_v14 importado desde: {V14.__file__}")
    print(f"  T = {T} (ancla del rng: {T_LARGO}), semillas {SEM}, UN proceso\n")

    tot = [0, 0]

    print("APAGADO (mundo='AB'): organismo_familias == organismo_v14 en todas las claves de v14")
    for etiq, kw in [('(A) base', dict()),
                     ('(B) inversion en T/2', dict(invertir_en=T // 2)),
                     ('(C) estimulo nuevo C veneno en T/2', dict(nuevo='C', nuevo_en=T // 2, nuevo_val='veneno')),
                     ('(D) solapamiento A/B = 2', dict(solap_AB=2)),
                     ('(E) sin puerta (puerta=None)', dict(puerta=None)),
                     ('(F) camino theta de v10 (div_signo=False)', dict(div_signo=False)),
                     ('(G) linaje v13 (mask_rel=0, puerta_pat=0)', dict(mask_rel=0, puerta_pat=0)),
                     ('(H) sin memoria de rechazo', dict(memoria_rechazo=0))]:
        caso(etiq, V14, kw, dict(kw), t0, tot=tot)

    print("\nRNG NO CONSUMIDO: el ancla larga (si una linea nueva sorteara, los flujos divergirian)")
    caso(f'(I) mundo=AB a T = {T_LARGO}', V14, dict(), dict(), t0, Ti=T_LARGO, tot=tot)

    print("\nPERILLAS DEL MUNDO DECLARADAS PERO APAGADAS POR mundo='AB'")
    caso('(J) todas las perillas del mundo puestas', V14, dict(), dict(PERILLAS), t0, tot=tot)

    print("\nB-5 COMPUESTO: mundo='AB', desambiguar=1 == organismo_v14_codigo_on")
    caso('(N) == organismo_v14_codigo_on (2f7794d92e68cc89)', B5ON, dict(desambiguar=1), dict(desambiguar=1), t0, tot=tot)

    print("\nINERCIA DE B-5 EN EL MUNDO NUEVO (P7a comprobada a T corto, antes de gastar Pool)")
    caso_mf('(P) familias n_neu=0: desambiguar=1 == desambiguar=0',
            dict(FAM, desambiguar=1), dict(FAM, desambiguar=0), t0, tot=tot)

    print("\nCONJUNTO DE CLAVES")
    k14 = set(V14.run(1, T=2000))
    kb5 = set(B5ON.run(1, T=2000))
    kab = set(MF.run(1, T=2000))
    kfa = set(MF.run(1, T=2000, **FAM))
    igual = (kab == kb5) and (k14 <= kab) and (kab - k14 == {'desambiguar', 'des_splits', 'des_t'})
    print(f"  [{time.time()-t0:6.1f}s] {'(K) claves con mundo=AB == organismo_v14_codigo_on':56s} "
          f"{'1/1 IDENTICO' if igual else '0/1 FALLA ' + str(kab ^ kb5)}", flush=True)
    tot[0] += int(igual); tot[1] += 1
    print(f"       sobre v14, mundo='AB' anade solo las de B-5: {sorted(kab - k14)}")
    print(f"       claves nuevas con mundo='familias' (solo lectura): {sorted(kfa - kab)}")
    if kfa - kab != NUEVAS:
        print(f"       AVISO: la lista NUEVAS del arnes no coincide con lo que devuelve el instrumento: "
              f"{sorted((kfa - kab) ^ NUEVAS)}")

    print("\nCONTROLES QUE DEBEN FALLAR (sin ellos el arnes pasaria por vacuidad)")
    caso('(L) mundo=familias != v14', V14, dict(), dict(FAM), t0, debe_diferir=True, tot=tot)
    caso('(M) mundo=AB con renov=1.0 != v14', V14, dict(), dict(renov=1.0), t0, debe_diferir=True, tot=tot)

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el paquete puede correr." if tot[0] == tot[1] else
                                              "  -> NO se corre nada hasta que sea 100%."))

    print("\nDIAGNOSTICO (NO es puerta): B-5 con estimulos que NO informan (n_neu=2)")
    print("  si NO difiere, es P7b(i) cayendo -- un RESULTADO del bloque, no un fallo del instrumento.")
    caso_mf('(Q) familias n_neu=2: desambiguar=1 vs desambiguar=0',
            dict(FAM, n_neu=2, desambiguar=1), dict(FAM, n_neu=2, desambiguar=0), t0,
            debe_diferir=True, puerta=False)

    sys.exit(0 if tot[0] == tot[1] else 1)
