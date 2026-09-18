"""Arnes de identidad del MUNDO VIVO (nivel 11). Regla 2 de registro/EQUIPO.md: un instrumento nuevo construido
por anclas debe ser su origen BIT A BIT con las perillas apagadas, y el arnes se corre y se entrega con el trabajo.

Aqui la exigencia es mas fuerte que "apagado": el encargo pide que **con UNA necesidad (hambre) y DOS estimulos
(comida/veneno) el mundo vivo sea organismo_v14 bit a bit, mismo consumo del rng y mismas claves de salida**. Por eso
hay dos familias de casos:

  APAGADO (vivo=0)      : organismo_vivo == organismo_v14 en TODAS las claves y con el MISMO conjunto de claves.
  ENCENDIDO CON 1+2 (I,J): vivo=1, n_nec=1, estims=('A','B'), costo_a=0 -> toda la maquinaria del mundo vivo
                           ACTIVA (consecuencia vectorial de la mordida, dos muertes posibles, drenaje de agua,
                           contadores de exposiciones) y aun asi TODAS las claves de v14 salen bit a bit; lo unico
                           que aparece es el registro de solo lectura del mundo vivo (10 claves nuevas).

  (A) base                         (B) inversion en 10k          (C) estimulo nuevo C veneno
  (D) solapamiento A/B = 2         (E) sin puerta (puerta=None)  (F) camino theta de v10 (div_signo=False)
  (G) linaje v13 (mask_rel=0, puerta_pat=0)                      (H) predictor VECTORIAL de dS encendido: SOLO MIDE
  (I) ANCLA DEL ENCARGO: mundo vivo con 1 necesidad y 2 estimulos == v14, clave por clave
  (J) lo mismo con inversion       (K) conjunto de claves identico con vivo=0
  (L) sin memoria de rechazo (memoria_rechazo=0)
  (M) CONTROL QUE PUEDE FALLAR (y debe): con CUATRO estimulos y DOS necesidades el organismo NO es v14.
      Sin este caso el arnes podria pasar por vacuidad (todo apagado siempre).

Un proceso, sin Pool (regla 3 de EQUIPO.md). T = 20000 en todos los casos (<= 30000).
OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/nivel11_mundo_vivo/identidad_vivo.py
"""
import hashlib, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_vivo as VV

T = 20000
SEM = (1, 2, 3)
NUEVAS = {'n_nec', 'estims', 'agua', 'muertes_nec', 'exp_hasta', 'exposiciones', 'W_nec', 'xor_mord', 'xor_enc',
          'sorp_nec'}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def solo_v14(d):
    return {k: v for k, v in d.items() if k not in NUEVAS}


def caso(etiq, kw_v14, kw_vv, t0, debe_diferir=False, semillas=SEM):
    ok = 0
    detalle = ''
    for s in semillas:
        a = V14.run(s, T=T, **kw_v14)
        b = VV.run(s, T=T, **kw_vv)
        dif = [k for k in a if a[k] != solo_v14(b).get(k)]
        falta = [k for k in a if k not in b]
        igual = not dif and not falta
        ok += int(igual != debe_diferir)
        if dif and not detalle:
            detalle = ' ' + str(dif[:5])
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    print(f"  [{time.time()-t0:6.1f}s] {etiq:52s} {ok}/{len(semillas)} {marca if ok == len(semillas) else 'FALLA' + detalle}",
          flush=True)
    return ok, len(semillas)


if __name__ == '__main__':
    t0 = time.time()
    for nom, p in [('organismo_v14 (TRONCO congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
                   ('construye_vivo.py', os.path.join(AQUI, 'construye_vivo.py')),
                   ('organismo_vivo.py', os.path.join(AQUI, 'organismo_vivo.py'))]:
        print(f"  sha {nom:34s} {h16(p)}")
    print(f"  modulo organismo_v14 importado desde: {V14.__file__}")
    print(f"  T = {T}, semillas {SEM}, UN proceso\n")

    APAG = dict(vivo=0, n_nec=1)
    VIVO1 = dict(vivo=1, n_nec=1, estims=('A', 'B'), costo_a=0.0, A_ini=1.0)
    ok = tot = 0
    print("APAGADO (vivo=0): organismo_vivo == organismo_v14")
    for etiq, kw in [('(A) base', dict()),
                     ('(B) inversion en 10k', dict(invertir_en=10000)),
                     ('(C) estimulo nuevo C veneno en 10k', dict(nuevo='C', nuevo_en=10000, nuevo_val='veneno')),
                     ('(D) solapamiento A/B = 2', dict(solap_AB=2)),
                     ('(E) sin puerta (puerta=None)', dict(puerta=None)),
                     ('(F) camino theta de v10 (div_signo=False)', dict(div_signo=False)),
                     ('(G) linaje v13 (mask_rel=0, puerta_pat=0)', dict(mask_rel=0, puerta_pat=0)),
                     ('(L) sin memoria de rechazo', dict(memoria_rechazo=0))]:
        a, b = caso(etiq, kw, dict(kw, **APAG), t0)
        ok += a; tot += b

    print("\nPREDICTOR VECTORIAL DE dS: solo mide (no toca el rng ni la decision)")
    a, b = caso('(H) eta_pred=0.05, k_sorp=0', dict(), dict(APAG, eta_pred=0.05), t0); ok += a; tot += b

    print("\nANCLA DEL ENCARGO: mundo vivo con UNA necesidad y DOS estimulos == organismo_v14")
    for etiq, kw in [('(I) base', dict()), ('(J) inversion en 10k', dict(invertir_en=10000))]:
        a, b = caso(etiq, kw, dict(kw, **VIVO1), t0)
        ok += a; tot += b

    print("\nCONJUNTO DE CLAVES")
    k14 = set(V14.run(1, T=2000))
    kvv = set(VV.run(1, T=2000, **APAG))
    kv1 = set(VV.run(1, T=2000, **VIVO1))
    igual = (k14 == kvv)
    print(f"  [{time.time()-t0:6.1f}s] {'(K) claves con vivo=0 identicas a v14':52s} "
          f"{'1/1 IDENTICO' if igual else '0/1 FALLA ' + str(k14 ^ kvv)}", flush=True)
    ok += int(igual); tot += 1
    print(f"       claves nuevas con vivo=1 (solo lectura): {sorted(kv1 - k14)}")
    if kv1 - k14 != NUEVAS:
        print(f"       AVISO: la lista NUEVAS del arnes no coincide con lo que devuelve el instrumento")

    print("\nCONTROL QUE PUEDE FALLAR (y debe fallar: si no, el arnes pasaria por vacuidad)")
    a, b = caso('(M) 4 estimulos y 2 necesidades != v14', dict(),
                dict(vivo=1, n_nec=2, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001), t0,
                debe_diferir=True)
    ok += a; tot += b

    print(f"\nIDENTIDAD {ok}/{tot}" + ("  -> el paquete puede correr." if ok == tot else
                                       "  -> NO se corre nada hasta que sea 100%."))
    sys.exit(0 if ok == tot else 1)
