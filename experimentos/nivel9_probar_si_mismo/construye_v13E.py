"""Construye los instrumentos de "LA SORPRESA DEL MUNDO EN LA BOCA" (dE-TEST, segundo candidato a organo;
PROPUESTA_v14.md, REGISTRO_etapas_1_2.md "Bloque C-P1") como CANDIDATO A TRONCO, POR ANCLAS y sin tocar ningun
original (organismo/organismo_v13.py, organismo/bateria_v13.py y organismo/bateria_generaliza.py estan
CONGELADOS: solo se LEEN; organismo_v13p.py y organismo_v13pg.py estan generados por construye_probar.py, ya
pasaron su propio arnes de identidad [J1..J6, PREREGISTRO_probar_si_mismo.md] y aqui tambien solo se LEEN):

  organismo_v13E.py       <- organismo_v13p.py   (2dbed7ccac4dd736)  dE-TEST fijo ON por defecto
  organismo_v13gE.py      <- organismo_v13pg.py  (910f1f5fb64453bb)  idem, mundo de regla
  bateria_v13E.py         <- organismo/bateria_v13.py         (1a027bcb37eb536e)  criterios v3' INTACTOS
  bateria_generaliza_E.py <- organismo/bateria_generaliza.py  (46772f5a582872c8)  G1/G2/K INTACTOS

PERILLA (las TRES fijas ON; son EXACTAMENTE los kwargs de BRAZOS['dE-TEST'] en corre_probar_si_mismo.py:
K_TEST = 10.0 y `dict(eta_pred=0.03, ema_pred=0.05, k_testE=K_TEST)`; ese brazo NO toca `k_test` -- se queda en
su default 0.0, igual que el resto de perillas de organismo_v13p/pg, todas ya apagadas por defecto):
  eta_pred = 0.03   (era 0.0)   -- tasa del predictor de dE (bloque 6, copiado)
  ema_pred = 0.05   (era 0.0)   -- EMA del error del predictor -> sbarE (causal: la usa la boca del PROXIMO encuentro)
  k_testE  = 10.0   (era 0.0)   -- ganancia con la que sbarE entra en la BOCA (Vb += k_testE*sbarE)
  (k_test, test_fijo, eta_b, k_auto, n_traza, traza_ext, desfase, k_testM, resta_cota, resta_lenta: NO se tocan,
   se quedan en su default de organismo_v13p/pg -- ese brazo no los usa)

Con eta_pred=ema_pred=k_testE=0 organismo_v13E es organismo_v13p EXACTO, bit a bit (arnes: identidad_v13E.py).
A diferencia de la hija dispersa (nivel7_hija_dispersa: perilla predicha INERTE en el mundo del tronco), esta
perilla se predice ACTIVA aqui (es su razon de ser: acelerar la recuperacion tras una inversion, ya medido en
41-60, 61-80 y 81-100 con corre_probar_si_mismo.py).

ERR-30 (pedido del coordinador, tras el primer humo: criterio 5 dio 0/84 porque k_testE actua en la BOCA sin
pasar por eta_s/puerta): bateria_v13E.py lleva un parche por anclas en su propio criterio 5 -- la reduccion a
v11/v10 apaga TAMBIEN k_testE y eta_pred (precedente ERR-21, criterio 3 -> 3'/3''). El resto del examen (las seis
etapas, celdas<=45, 3'/3'', 4a-4d) queda INTACTO. Justificacion completa: PREREGISTRO_v13E.md, seccion "Criterio 5
adaptado (v3'' para organos en la boca)".

Uso:  python experimentos/nivel9_probar_si_mismo/construye_v13E.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


SHA_V13P = '2dbed7ccac4dd736'
SHA_V13PG = '910f1f5fb64453bb'
SHA_BATERIA_V13 = '1a027bcb37eb536e'
SHA_BATERIA_GENERALIZA = '46772f5a582872c8'

# la firma de organismo_v13p.py y de organismo_v13pg.py termina IGUAL en las perillas del bloque 6 (dE):
# esta es la sub-cadena exacta (1 sola aparicion en cada archivo, verificado antes de escribir este constructor).
DE_TEST_VIEJO = "eta_pred=0.0,clip_e=3.0,ema_pred=0.0,k_testE=0.0,"
DE_TEST_NUEVO = "eta_pred=0.03,clip_e=3.0,ema_pred=0.05,k_testE=10.0,"


if __name__ == '__main__':
    salidas = []

    # ---- 1) organismo_v13E: organismo_v13p con dE-TEST fijo ON (perilla unica: la firma) ----
    s = origen(os.path.join(AQUI, 'organismo_v13p.py'), SHA_V13P)
    s = sust(s, DE_TEST_VIEJO, DE_TEST_NUEVO, etiqueta='v13E: firma (dE-TEST fijo ON)')
    cab = ('"""organismo_v13E = organismo_v13p.py (%s) + dE-TEST FIJO ON por defecto: eta_pred=0.03, ema_pred=0.05,\n'
           'k_testE=10.0 -- EXACTAMENTE BRAZOS["dE-TEST"] de corre_probar_si_mismo.py (K_TEST=10.0). Generado por\n'
           'construye_v13E.py. NO editar a mano. Con eta_pred=ema_pred=k_testE=0 es organismo_v13p EXACTO\n'
           '(arnes: identidad_v13E.py)."""\n' % SHA_V13P)
    d = os.path.join(AQUI, 'organismo_v13E.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ---- 2) organismo_v13gE: organismo_v13pg con dE-TEST fijo ON (mundo de regla) ----
    s = origen(os.path.join(AQUI, 'organismo_v13pg.py'), SHA_V13PG)
    s = sust(s, DE_TEST_VIEJO, DE_TEST_NUEVO, etiqueta='v13gE: firma (dE-TEST fijo ON)')
    cab = ('"""organismo_v13gE = organismo_v13pg.py (%s) + dE-TEST FIJO ON por defecto: eta_pred=0.03, ema_pred=0.05,\n'
           'k_testE=10.0 (las mismas tres constantes que organismo_v13E). Es el instrumento del MUNDO DE REGLA\n'
           'que usa bateria_generaliza_E.py. Generado por construye_v13E.py. NO editar.\n'
           'Con eta_pred=ema_pred=k_testE=0 es organismo_v13pg EXACTO."""\n' % SHA_V13PG)
    d = os.path.join(AQUI, 'organismo_v13gE.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ---- 3) bateria_v13E: la bateria del tronco (CONGELADA: solo se LEE) apuntando a organismo_v13E ----
    s = origen(os.path.join(RAIZ, 'organismo', 'bateria_v13.py'), SHA_BATERIA_V13)
    s = sust(s, "AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(AQUI)\n"
                "sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]\n",
             "_D = os.path.dirname(os.path.abspath(__file__))   # esta copia vive fuera de organismo/\n"
             "AQUI = os.path.join(os.path.dirname(os.path.dirname(_D)), 'organismo')\n"
             "RAIZ = os.path.dirname(AQUI)\n"
             "sys.path[:0] = [_D, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]\n", etiqueta='bateria_v13E: rutas')
    s = sust(s, "    import organismo_v13 as v13\n", "    import organismo_v13E as v13   # dE-TEST (sorpresa del mundo en la boca) FIJO ON\n",
             n=2, etiqueta='bateria_v13E: import')
    # ERR-30 (18 sep 2026; pedido del coordinador tras el humo: criterio 5 dio 0/84, k_testE actua en la BOCA sin
    # pasar por eta_s/puerta, asi que apagar esas dos NO reduce v13E a v11/v10). CRITERIO 5 ADAPTADO (v3'' para
    # organos en la boca), precedente ERR-21 (criterio 3 -> 3'/3''): la reduccion a v11 y a v10 apaga TAMBIEN la
    # perilla nueva (k_testE=0, eta_pred=0). El resto del examen (etapas 1-4d, CRIT, umbrales) queda INTACTO.
    # Justificacion completa: PREREGISTRO_v13E.md, seccion "Criterio 5 adaptado (v3'' para organos en la boca)".
    s = sust(s, "a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, **ESC_ID[esc])",
             "a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, k_testE=0.0, eta_pred=0.0, **ESC_ID[esc])   # ERR-30: v3'' (organos en la boca)",
             etiqueta='bateria_v13E: ERR-30 criterio 5 vs v11')
    s = sust(s, "a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, **ESC_ID[esc])",
             "a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, k_testE=0.0, eta_pred=0.0, **ESC_ID[esc])   # ERR-30: v3'' (organos en la boca)",
             etiqueta='bateria_v13E: ERR-30 criterio 5 vs v10')
    s = sust(s, "    for c, nombre in (('v11', 'v13(eta_s=0, puerta=None) == v11'), ('v10', 'v13(eta_s=0, puerta=None, div_signo=False) == v10')):\n",
             "    for c, nombre in (('v11', \"v13E(eta_s=0,puerta=None,k_testE=0,eta_pred=0) == v11  [v3'' ERR-30]\"), "
             "('v10', \"v13E(eta_s=0,puerta=None,div_signo=False,k_testE=0,eta_pred=0) == v10  [v3'' ERR-30]\")):\n",
             etiqueta='bateria_v13E: ERR-30 etiquetas de log')
    s = s.replace("h16(os.path.join(AQUI, 'organismo_v13.py'))", "h16(os.path.join(_D, 'organismo_v13E.py'))")
    s = s.replace("f'examen_v13_{stamp}", "f'examen_v13E_{stamp}")
    cab = ('"""bateria_v13E = organismo/bateria_v13.py (1a027bcb37eb536e, CONGELADO: solo se leyo) apuntando a\n'
           'organismo_v13E (organismo_v13p + dE-TEST fijo ON) en vez de organismo_v13. Las SEIS etapas, los CRIT\n'
           'importados y los umbrales del criterio v3\' quedan INTACTOS. Salida en datos/examen_v13E_<fecha>.\n'
           'ERR-30: el CRITERIO 5 esta ADAPTADO (v3\'\' para organos en la boca, precedente ERR-21): la reduccion a\n'
           'v11/v10 apaga TAMBIEN k_testE y eta_pred (si no, un organo que actua en la boca sin pasar por eta_s/\n'
           'puerta nunca podria pasar el criterio 5, y no mide nada). Ver PREREGISTRO_v13E.md.\n'
           'Generado por construye_v13E.py. NO editar. La bateria original NO se modifico."""\n')
    d = os.path.join(AQUI, 'bateria_v13E.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ---- 4) bateria_generaliza_E: con DOS entradas mas en INSTRUMENTOS (referencia apagada + dE-TEST fijo ON) ----
    s = origen(os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'), SHA_BATERIA_GENERALIZA)
    s = sust(s, "AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(AQUI)\n",
             "AQUI = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'organismo')   # esta copia vive fuera de organismo/\n"
             "RAIZ = os.path.dirname(AQUI)\n", etiqueta='bateria_generaliza_E: AQUI/RAIZ')
    s = sust(s, "REGLAS = ['px0', 'azar']\n",
             "REGLAS = ['px0', 'azar']\n_D = os.path.join(RAIZ, 'experimentos', 'nivel9_probar_si_mismo')\n",
             etiqueta='bateria_generaliza_E: _D')
    s = sust(s, "    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto\n",
             "    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto\n"
             "    'organismo_v13p': ('organismo_v13pg', dict(eta_s=0.015, puerta=3)),   # E: instrumento base, dE-TEST APAGADO -> debe dar lo mismo que organismo_v13\n"
             "    'organismo_v13E': ('organismo_v13gE', dict(eta_s=0.015, puerta=3)),   # E: dE-TEST (sorpresa del mundo en la boca) FIJO ON\n",
             etiqueta='bateria_generaliza_E: INSTRUMENTOS')
    s = sust(s, "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))\n",
             "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))\n"
             "sys.path.insert(0, _D)   # E: organismo_v13pg / organismo_v13gE\n", etiqueta='bateria_generaliza_E: sys.path')
    s = sust(s, "    _dir = {'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),\n",
             "    _dir = {'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),\n"
             "            'organismo_v13pg': _D, 'organismo_v13gE': _D,\n", etiqueta='bateria_generaliza_E: _dir')
    s = s.replace("h16(os.path.join(AQUI, (modulo if modulo != 'organismo_v13_rapido' else 'organismo_v13') + '.py'))",
                  "h16(os.path.join(AQUI, 'organismo_v13.py') if modulo == 'organismo_v13_rapido' else (os.path.join(AQUI, modulo + '.py') if os.path.exists(os.path.join(AQUI, modulo + '.py')) else os.path.join(_D, modulo + '.py')))")
    s = s.replace("sha_organismo=h16(os.path.join(AQUI, modulo + '.py')),",
                  "sha_organismo=(h16(os.path.join(AQUI, modulo + '.py')) if os.path.exists(os.path.join(AQUI, modulo + '.py')) else h16(os.path.join(_D, modulo + '.py'))),")
    cab = ('"""bateria_generaliza_E = organismo/bateria_generaliza.py (46772f5a582872c8) con dos entradas mas en\n'
           'INSTRUMENTOS (organismo_v13p, dE-TEST apagado -> referencia, y organismo_v13E, dE-TEST fijo ON, cada una\n'
           'sobre su organismo_*g correspondiente) y las rutas corregidas por vivir fuera de organismo/. Los\n'
           'UMBRALES y los criterios G1/G2/K NO se tocan.\n'
           'Generado por construye_v13E.py. NO editar. La bateria original NO se modifico."""\n')
    d = os.path.join(AQUI, 'bateria_generaliza_E.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    for d in salidas:
        print(f"  {os.path.relpath(d, RAIZ):55s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
