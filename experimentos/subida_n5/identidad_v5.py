"""Arnes de identidad del instrumento V-5 (experimentos/subida_n5/organismo_familias_v5.py =
organismo_familias_bav + `v5`). Reglas 2 y 14 de EQUIPO.md. Se corre ANTES de mirar ningun numero.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que se COMUNICA CON REFERENCIA. Hoy: familia Y variante con la MISMA tabla.

  APAGADO (v5=0)     : == organismo_familias_bav (EL ORIGEN, identidad 61/61) en TODAS sus claves, en mundo='AB',
                       en el mundo del receptor con las lecturas b4b / b5k3 / b6suf / A1 / BA-v, con el emisor voraz,
                       con el canal en sus tres modos, con el brazo PAR y con la memoria barajada.
  RNG NO CONSUMIDO   : lo mismo a T = 120000 (ancla larga).
  CADENA HASTA EL TRONCO: v5=0 + mundo='AB' == organismo_v14 (congelado) y, con el relevo, == organismo_v15f_on.
  INERCIA            : sin tabla (memoria_pares=None) v5=1 == v5=0.
  LA BARAJA NO TOCA EL AZAR: con v5=1, el PREFIJO hasta la entrega es identico con y sin baraja.
  EL MECANISMO HACE LO QUE DICE: con v5=1 hay partos por el mensaje y la hermana fija lee < 0 justo despues del
                       mensaje; con v5=0 (BA-v) se reporta lo que lee, sin juzgar.
  PERILLA MAL ESCRITA: lanza.
  CONTROLES QUE DEBEN DIFERIR (ERR-64b: >= 2 de 3 semillas): v5=1 != v5=0; CANAL != CORTADO; barajada != candidato.

Un proceso, sin Pool (regla 3). Importa los ayudantes del arnes de BA-v (identidad_familias_bav.py, cf7655b379014a55,
SOLO LECTURA) para no reescribir el emisor, el receptor ni la comparacion.
Uso:  python experimentos/subida_n5/identidad_v5.py > experimentos/subida_n5/identidad_v5_salida.txt
"""
import hashlib, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
NBAV = os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv')
sys.path[:0] = [AQUI, NBAV]

import identidad_familias_bav as H          # ayudantes (caso, uno, lanza, mensaje, receptor, mundos): SOLO LECTURA
import organismo_familias_bav as BAV        # EL ORIGEN
import organismo_familias_v5 as V5          # EL INSTRUMENTO NUEVO
V14, V15FON = H.V14, H.V15FON

SHAS = {'organismo_v14.py (TRONCO CONGELADO)': (os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), 'feefc88b1fd8d434'),
        'organismo_familias_bav.py (ORIGEN)': (os.path.join(NBAV, 'organismo_familias_bav.py'), '2dca0a3e239481f0'),
        'identidad_familias_bav.py (ayudantes)': (os.path.join(NBAV, 'identidad_familias_bav.py'), 'cf7655b379014a55'),
        'construye_v5.py': (os.path.join(AQUI, 'construye_v5.py'), None),
        'organismo_familias_v5.py': (os.path.join(AQUI, 'organismo_familias_v5.py'), None),
        'identidad_v5.py': (os.path.abspath(__file__), None)}
NUEVAS_V5 = ('v5', 'v5_split_msg', 'v5_split_mord', 'v5_t1', 'v5_sub', 'v5_lee_par')
SALTA_BAV = NUEVAS_V5
SALTA_TRONCO = NUEVAS_V5 + H.NUEVAS_BAV + H.NUEVAS_BA + H.NUEVAS_A1 + H.NUEVAS_B6 + H.NUEVAS_B5 + H.NUEVAS_B4B
T, T_LARGO, SEM = H.T, H.T_LARGO, H.SEM
KW_R, KW_E, BVP, A1P = H.KW_R, H.KW_E, H.BVP, H.A1P
LECTURAS = [('b4b (k=1)', dict(k_ganadoras=1)),
            ('b5k3 (k=3)', dict(k_ganadoras=3)),
            ('b6suf (k=3, sufijo)', dict(k_ganadoras=3, memoria_variante=1)),
            ('A1', dict(A1P, k_ganadoras=3)),
            ('BA-v (conj_tipo=2)', dict(BVP, k_ganadoras=3))]


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


if __name__ == '__main__':
    t0 = time.time()
    malo = False
    for nom, (p, esp) in SHAS.items():
        s = h16(p)
        aviso = '' if esp is None else ('  OK' if s == esp else f'  *** ESPERADO {esp}')
        malo = malo or (esp is not None and s != esp)
        print(f"  sha {nom:44s} {s}{aviso}")
    if malo:
        raise SystemExit("Un origen cambio. Reconstruir por anclas antes de seguir.")
    tot = [0, 0]
    caso, uno, lanza = H.caso, H.uno, H.lanza

    print("\nAPAGADO (v5=0): organismo_familias_v5 == organismo_familias_bav (EL ORIGEN)")
    caso('(a) mundo=AB base', lambda s: BAV.run(s, T=T), lambda s: V5.run(s, T=T, v5=0), t0, tot=tot, salta=SALTA_BAV)
    caso('(b) mundo=AB, relevo encendido, k=3', lambda s: BAV.run(s, T=T, memoria_pares='relevo', k_ganadoras=3),
         lambda s: V5.run(s, T=T, memoria_pares='relevo', k_ganadoras=3), t0, semillas=SEM[:2], tot=tot, salta=SALTA_BAV)
    for etiq, p in LECTURAS:
        caso(f'(c) mundo del RECEPTOR, lectura {etiq}',
             (lambda x: lambda s: BAV.run(s, T=T, **dict(KW_R, fam_seed=s, **x)))(p),
             (lambda x: lambda s: V5.run(s, T=T, v5=0, **dict(KW_R, fam_seed=s, **x)))(p),
             t0, semillas=SEM[:2], tot=tot, salta=SALTA_BAV)
    caso('(d) el EMISOR voraz del bloque 4b (canal emite)',
         lambda s: BAV.run(s, T=T, voraz=H.VORAZ, canal={'modo': 'emite'}, **dict(KW_E, fam_seed=s)),
         lambda s: V5.run(s, T=T, voraz=H.VORAZ, canal={'modo': 'emite'}, **dict(KW_E, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=SALTA_BAV)

    m0 = {s: H.mensaje(s) for s in SEM}
    SM = tuple(s for s in SEM if m0[s] is not None)
    print(f"  emisores con mensaje (-): {len(SM)}/{len(SEM)} -> {SM}  [{time.time()-t0:.1f}s]")
    for etiq, modo, ph, extra in [('(e) canal sen, BA-v', 'sen', None, {}),
                                  ('(f) canal mudo (CORTADO), BA-v', 'mudo', None, {}),
                                  ('(g) canal inm, BA-v', 'inm', None, {}),
                                  ('(h) brazo PAR (par_herm=(1,0)), BA-v', 'sen', (1, 0), {}),
                                  ('(i) canal sen, BA-v con memoria BARAJADA', 'sen', None, dict(baraja_msg=1)),
                                  ('(j) canal sen, b5k3', 'sen', None, 'b5k3')]:
        kw = dict(k_ganadoras=3) if extra == 'b5k3' else dict(BVP, k_ganadoras=3, **extra)
        caso(etiq, (lambda mo, p2, k2: lambda s: H.receptor(s, m0[s], mo, par_herm=p2, mod=BAV, **k2))(modo, ph, kw),
             (lambda mo, p2, k2: lambda s: H.receptor(s, m0[s], mo, par_herm=p2, mod=V5, v5=0, **k2))(modo, ph, kw),
             t0, semillas=SM[:2], tot=tot, salta=SALTA_BAV)

    print("\nRNG NO CONSUMIDO (ancla larga)")
    caso(f'(k) mundo=AB a T = {T_LARGO}, relevo, BA-v, v5=0',
         lambda s: BAV.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=3, **BVP),
         lambda s: V5.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=3, v5=0, **BVP),
         t0, semillas=SEM[:2], tot=tot, salta=SALTA_BAV)

    print("\nCADENA HASTA EL TRONCO (se comprueba, no se supone)")
    caso('(l) v5=0 + mundo=AB == organismo_v14 (TRONCO CONGELADO)', lambda s: V14.run(s, T=T),
         lambda s: V5.run(s, T=T, v5=0), t0, tot=tot, salta=SALTA_TRONCO)
    caso('(m) relevo ON + mundo=AB == organismo_v15f_on', lambda s: V15FON.run(s, T=T),
         lambda s: V5.run(s, T=T, memoria_pares='relevo'), t0, tot=tot, salta=SALTA_TRONCO)

    print("\nINERCIA: sin tabla no hay casilla que partir")
    caso('(n) memoria_pares=None: v5=1 == v5=0 (mundo=AB)', lambda s: V5.run(s, T=T, v5=0),
         lambda s: V5.run(s, T=T, v5=1), t0, tot=tot, salta=('v5',))   # 'v5' es el ECO de la perilla (intento 1: 31/33 por no saltarlo)
    caso('(n2) memoria_pares=None, mundo del receptor sin relevo: v5=1 == v5=0',
         lambda s: V5.run(s, T=T, **dict(KW_R, fam_seed=s, memoria_pares=None)),
         lambda s: V5.run(s, T=T, v5=1, **dict(KW_R, fam_seed=s, memoria_pares=None)), t0, semillas=SEM[:2], tot=tot, salta=('v5',))

    print("\nLA BARAJA NO TOCA EL AZAR (con V-5 encendido): el PREFIJO hasta la entrega es identico")
    caso('(o) v5=1, canal sen: todo lo calculado ANTES de escribir el mensaje, con y sin baraja',
         lambda s: H.receptor(s, m0[s], 'sen', mod=V5, k_ganadoras=3, v5=1, **BVP),
         lambda s: H.receptor(s, m0[s], 'sen', mod=V5, k_ganadoras=3, v5=1, baraja_msg=1, **BVP),
         t0, semillas=SM, tot=tot, solo=H.PREFIJO_CANAL)

    print("\nCONTROLES QUE DEBEN DIFERIR (sin ellos el arnes pasaria por vacuidad)")
    caso('(p) v5=1 != v5=0 (mundo del receptor, BA-v, sin canal)',
         lambda s: V5.run(s, T=T, v5=0, **dict(KW_R, fam_seed=s, k_ganadoras=3, **BVP)),
         lambda s: V5.run(s, T=T, v5=1, **dict(KW_R, fam_seed=s, k_ganadoras=3, **BVP)),
         t0, debe_diferir=True, tot=tot, salta=NUEVAS_V5)
    R_CAN = {s: H.receptor(s, m0[s], 'sen', mod=V5, k_ganadoras=3, v5=1, **BVP) for s in SM}
    R_COR = {s: H.receptor(s, m0[s], 'mudo', mod=V5, k_ganadoras=3, v5=1, **BVP) for s in SM}
    R_SH = {s: H.receptor(s, m0[s], 'sen', mod=V5, k_ganadoras=3, v5=1, baraja_msg=1, **BVP) for s in SM}
    caso('(q) BA-v5: CANAL != CORTADO', lambda s: R_CAN[s], lambda s: R_COR[s], t0, debe_diferir=True,
         semillas=SM, tot=tot, salta=('canal', 'canal_modo', 'canal_emitido'))
    caso('(r) BA-v5: BARAJADA != candidato', lambda s: R_CAN[s], lambda s: R_SH[s], t0, debe_diferir=True,
         semillas=SM, tot=tot, salta=('baraja_msg', 'baraja_perm'))

    print("\nEL MECANISMO HACE LO QUE DICE (brazo PAR, T = %d)" % H.T_CANAL)
    R_P5 = {s: H.receptor(s, m0[s], 'sen', par_herm=(1, 0), mod=V5, k_ganadoras=3, v5=1, **BVP) for s in SM}
    R_P0 = {s: H.receptor(s, m0[s], 'sen', par_herm=(1, 0), mod=V5, k_ganadoras=3, v5=0, **BVP) for s in SM}
    for s in SM:
        a, b = R_P5[s], R_P0[s]
        print(f"      s{s}: v5=1 partos msg/bocado {a['v5_split_msg']}/{a['v5_split_mord']} (1.o t={a['v5_t1']}) "
              f"subcasillas {a['v5_sub']}  lee(hermana) {a['v5_lee_par']}  lee(ref) {a['canal_lee_ref']} | "
              f"v5=0 lee(hermana) {b['v5_lee_par']}  lee(ref) {b['canal_lee_ref']}")
    uno('(s) con v5=1 el MENSAJE parte casillas (v5_split_msg > 0) en todas las semillas con mensaje',
        all(R_P5[s]['v5_split_msg'] > 0 for s in SM), t0, tot)
    uno('(t) con v5=1 la hermana fija lee < 0 justo DESPUES del mensaje (>= 2 de 3 semillas con mensaje)',
        sum(1 for s in SM if R_P5[s]['v5_lee_par'] and R_P5[s]['v5_lee_par'][1] and R_P5[s]['v5_lee_par'][0] < 0)
        >= min(2, len(SM)), t0, tot)
    uno('(u) con v5=1 el referente lee > 0 tras el mensaje (canal_lee_ref[0] > 0, todas)',
        all(R_P5[s]['canal_lee_ref'] and R_P5[s]['canal_lee_ref'][0] > 0 for s in SM), t0, tot)
    uno('(v) con v5=0 no hay partos ni subcasillas (contadores a 0 / None)',
        all(R_P0[s]['v5_split_msg'] == 0 and R_P0[s]['v5_split_mord'] == 0 and R_P0[s]['v5_sub'] is None for s in SM),
        t0, tot)

    print("\nPERILLA MAL ESCRITA: lanza")
    for bad in (2, -1, 0.5, '1', True):
        lanza(f'(w) v5={bad!r} lanza', (lambda b: lambda: V5.run(1, T=50, memoria_pares='relevo', v5=b))(bad), t0, tot)
    lanza('(x) v5=1 con memoria_variante=1 lanza (el sufijo ya direcciona todo)',
          lambda: V5.run(1, T=50, memoria_pares='relevo', memoria_variante=1, v5=1), t0, tot)

    print(f"\nIDENTIDAD V-5: {tot[0]}/{tot[1]}  ({time.time()-t0:.0f} s, un proceso)")
    if tot[0] != tot[1]:
        sys.exit(1)
