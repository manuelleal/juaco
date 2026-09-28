"""construye_examen_v144c.py -- construye POR ANCLAS el runner y el arnes del examen v14.4c desde los del examen v14.4b
(experimentos/tronco_v14_4b_examen/, sha fijado). MISION: llegar a la AGI por este camino.

El examen v14.4c es el examen v14.4b (MISMO organismo v14.4b = v14.3 + TERMO', MISMA letra en todo) con UNA enmienda: T-C (ii)
se juzga POR VISITA (ERR-150: C = S4 - S2 con margen 0.125 y suelo S4 > 0.5). La letra vieja (rev absoluto) se sigue calculando
y se REPORTA al lado. Cambian ademas: las semillas (umbrales_examen_v144c), los nombres de salida (v144b -> v144c) y la carpeta
de donde se leen el organismo y sus baterias (se REUSAN de tronco_v14_4b_examen con sha fijado; no se copian).

    python experimentos/tronco_v14_4c_examen/construye_examen_v144c.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
V144B = os.path.join(RAIZ, 'experimentos', 'tronco_v14_4b_examen')
ORIGENES = {os.path.join(V144B, 'corre_examen_v144b.py'): '9fb2e22a392590c7',
            os.path.join(V144B, 'identidad_v144bex.py'): '23f5ed70d42399e0'}


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


def origen(p):
    b = open(p, 'rb').read()
    if h16b(b) != ORIGENES[p]: raise SystemExit(f'*** ORIGEN {p}: sha {h16b(b)} != {ORIGENES[p]}')
    return b.decode('utf-8')


def sust(t, a, b, etq, n=1):
    c = t.count(a)
    if (n is None and c < 1) or (n is not None and c != n):
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces (se esperaban {n if n is not None else ">= 1"})')
    return t.replace(a, b)


# el organismo y sus baterias CONSERVAN su nombre (organismo_v144b*, bateria_v144b, bateria_generaliza_v144b): se reusan
GLOBAL = [('umbrales_examen_v144b', 'umbrales_examen_v144c'), ('corre_examen_v144b', 'corre_examen_v144c'),
          ('identidad_v144bex', 'identidad_v144cex'), ('examen_v144b_', 'examen_v144c_'),
          ('PREREGISTRO_examen_v144b.md', 'PREREGISTRO_examen_v144c.md'),
          ('tronco_v14_4b_examen/corre_examen_v144c', 'tronco_v14_4c_examen/corre_examen_v144c'),
          ('tronco_v14_4b_examen/identidad_v144cex', 'tronco_v14_4c_examen/identidad_v144cex'),
          ('tronco_v14_4b_examen/PREREGISTRO_examen_v144c', 'tronco_v14_4c_examen/PREREGISTRO_examen_v144c')]


def globales(t, etq):
    for a, b in GLOBAL:
        t = t.replace(a, b)
    for a in ('umbrales_examen_v144b', 'corre_examen_v144b', 'identidad_v144bex', 'examen_v144b_', 'PREREGISTRO_examen_v144b'):
        if a in t: raise SystemExit(f'*** {etq}: quedo {a!r} sin reemplazar')
    return t


CAB_R = ('"""corre_examen_v144c.py = corre_examen_v144b.py (9fb2e22a392590c7) con T-C (ii) POR VISITA (ERR-150). MISMO organismo '
         '(v14.4b = v14.3 + TERMOP, reusado de tronco_v14_4b_examen con sha), MISMA letra en todo lo demas, semillas nuevas. GENERADO por '
         'experimentos/tronco_v14_4c_examen/construye_examen_v144c.py. NO editar a mano."""\n')
CAB_I = ('"""identidad_v144cex.py = identidad_v144bex.py (23f5ed70d42399e0) para el examen v14.4c. Igual, con el organismo y los carros '
         'leidos de tronco_v14_4b_examen, la construccion del runner verificada y un bloque nuevo (E): la T-C (ii) POR VISITA (ERR-150) '
         'contra el analisis del nulo, el examen de v14.4 (TERMO sigue cayendo) y controles que deben caer. GENERADO por '
         'construye_examen_v144c.py. NO editar a mano."""\n')

# ---------------------------------------------------------------- lo nuevo del runner: LA LETRA POR VISITA (ERR-150)
LETRA_VISITA = '''

# ------------------------------------------------------------------ ERR-150: T-C (ii) POR VISITA (la letra que DECIDE en v14.4c)
def _tasa(m, v):
    """Tasa de mordida por visita con el +1/+2 de Laplace (vis = pasos sobre el objeto = decisiones de la boca)."""
    return (m + 1.0) / (v + 2.0)


def _pref(r, q, bueno, malo):
    pb, pm = _tasa(r['mord' + bueno][q], r['vis' + bueno][q]), _tasa(r['mord' + malo][q], r['vis' + malo][q])
    return pb / (pb + pm)


def S4_visita(r):
    """DESPUES de la reversion (Q4): preferencia por visita por lo que AHORA es bueno (B)."""
    return _pref(r, U.ERR150['cuarto_despues'], 'B', 'A')


def S2_visita(r):
    """ANTES de la reversion (Q2): la misma preferencia por lo que ENTONCES era bueno (A)."""
    return _pref(r, U.ERR150['cuarto_antes'], 'A', 'B')


def C_visita(r):
    """Cuanto se desdice, contra si mismo: 0 = distingue despues tan bien como antes."""
    return S4_visita(r) - S2_visita(r)


def letra_TC_visita(off, cand):
    """ERR-150: (a) NO INFERIORIDAD (corre_criterio_v3.no_inferior, la de v4) sobre C con margen 0.125; (b) mediana S4 > 0.5.
    off, cand: listas ordenadas por semilla-etiqueta (C4.G)."""
    u = U.ERR150
    ni_ = C4.no_inferior([C_visita(r) for r in cand], [C_visita(r) for r in off], u['margen'], u['z'])
    s4 = med([S4_visita(r) for r in cand]); s4o = med([S4_visita(r) for r in off])
    s2 = med([S2_visita(r) for r in cand]); s2o = med([S2_visita(r) for r in off])
    suelo = bool(s4 is not None and s4 > u['suelo_S4'])
    return bool(ni_['pasa'] and suelo and len(cand) == len(off) == u['n']), dict(
        NI_C=ni_, suelo=suelo, S4=(s4, s4o), S2=(s2, s2o), C=(med([C_visita(r) for r in cand]), med([C_visita(r) for r in off])),
        n=(len(cand), len(off)))


def tc_err150(Vc, res_rev, cand):
    """Sustituye la T-C (ii) de corre_criterio_v4.juzga (rev absoluto) por la POR VISITA; la vieja queda como informe."""
    if 'T-C_ii' not in Vc:
        return
    p, det = letra_TC_visita(C4.G(res_rev, 'OFF'), C4.G(res_rev, cand))
    Vc['T-C_ii']['rev_absoluto_v4'] = dict(pasa=Vc['T-C_ii']['v4'], det=Vc['T-C_ii']['det_v4'], solo_informe=True)
    Vc['T-C_ii']['v4'] = p
    Vc['T-C_ii']['det_visita'] = det
    Vc['T-C_ii']['letra'] = 'ERR-150'
    Vc['v4'] = bool(Vc.get('T-A', {}).get('v4', True) and p and Vc.get('T-F_vivo_TA', True) and Vc.get('T-F_vivo_TC', True))
    ni_ = det['NI_C']
    log(f"   T-C ii POR VISITA (ERR-150) [{cand:8s}] S2 {_n(det['S2'][0])}/{_n(det['S2'][1])} S4 {_n(det['S4'][0])}/{_n(det['S4'][1])} "
        f"C {_n(det['C'][0], '+.4f')}/{_n(det['C'][1], '+.4f')} | NI sobre C media {ni_['media']} sd {ni_.get('sd')} LI {ni_['LI']} > "
        f"-{U.ERR150['margen']} -> {ni_['pasa']} | suelo S4 > {U.ERR150['suelo_S4']} -> {det['suelo']} => {'PASA' if p else 'NO'} "
        f"(rev absoluto, SOLO INFORME: {'PASA' if Vc['T-C_ii']['rev_absoluto_v4']['pasa'] else 'NO'})")
    log(f"   >>> {cand}: v4 del mundo vivo con ERR-150 (T-A, T-C ii POR VISITA, T-F vivo) {'PASA' if Vc['v4'] else 'NO PASA'}")

'''


def construye():
    out = {}
    r = globales(origen(os.path.join(V144B, 'corre_examen_v144b.py')), 'runner')
    # el organismo y sus baterias: de tronco_v14_4b_examen (con sha); esta carpeta solo tiene runner, umbrales, arnes y datos
    r = sust(r, "TERMO_DIR = os.path.join(EXP, 'organelos', 'termo')\n",
             "TERMO_DIR = os.path.join(EXP, 'organelos', 'termo')\n"
             "V144B = os.path.join(EXP, 'tronco_v14_4b_examen')   # v14.4c: el ORGANISMO v14.4b y sus baterias, reusados con sha fijado\n",
             'runner: V144B')
    r = sust(r, "for _p in reversed([AQUI, ORG, VIVO_DIR, V3_DIR, V4_DIR, CREB, DE5]):",
             "for _p in reversed([AQUI, V144B, ORG, VIVO_DIR, V3_DIR, V4_DIR, CREB, DE5]):", 'runner: sys.path')
    r = sust(r, "    os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'umbrales_examen_v144.py'): '0df02bd6a4d548c4',   # T-G y letra (v14.4)\n",
             "    os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'umbrales_examen_v144.py'): '0df02bd6a4d548c4',   # T-G y letra (v14.4)\n"
             "    # v14.4c: el examen v14.4b (organismo, baterias, constructor, carros, umbrales y los ORIGENES de este runner y su arnes)\n"
             "    os.path.join(V144B, 'organismo_v144b.py'): 'c8f0c25302f20fd9',\n"
             "    os.path.join(V144B, 'organismo_v144bg.py'): '19106bea564d4a94',\n"
             "    os.path.join(V144B, 'organismo_v144bcal.py'): 'b9c2cf7b73007a96',\n"
             "    os.path.join(V144B, 'bateria_v144b.py'): '01e00e0d3c283561',\n"
             "    os.path.join(V144B, 'bateria_generaliza_v144b.py'): '3bbd29d3d71b022a',\n"
             "    os.path.join(V144B, 'construye_termop.py'): '81f63fd59d168759',\n"
             "    os.path.join(V144B, 'carros', 'V143_TERMOP.py'): 'edf5dfc9c5e498da',\n"
             "    os.path.join(V144B, 'carros', 'V143_TERMOPINV.py'): '63edcafcc569a0d7',\n"
             "    os.path.join(V144B, 'umbrales_examen_v144b.py'): 'ddc96fa8038c3719',\n"
             "    os.path.join(V144B, 'corre_examen_v144b.py'): '9fb2e22a392590c7',\n"
             "    os.path.join(V144B, 'identidad_v144bex.py'): '23f5ed70d42399e0',\n"
             "    # ERR-150: el analisis del nulo y los crudos del examen de v14.4 (TERMO: la condicion anti-TERMO del arnes (E))\n"
             "    os.path.join(AQUI, 'analiza_nulo_err150.py'): '@@SHA_ANALIZA@@',\n"
             "    os.path.join(AQUI, 'datos', 'nulo_err150_20260928_161728.json'): 'a394a03bf9241b40',\n"
             "    os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'datos', 'examen_v144_serie_20260928_123734.json'): '25458f0f470b25e6',\n"
             "    os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'datos', 'examen_v144_serie_20260928_123734_crudo_TCii.json'): 'd7b018cfd63d8eb6',\n"
             "    os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'datos', 'examen_v144_serie_20260928_123734_crudo_TA.json'): '@@SHA_TA144@@',\n",
             'runner: anclas v14.4b y ERR-150')
    r = sust(r, "    r = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_termop.py'), '--verifica'], capture_output=True, text=True,",
             "    r = subprocess.run([sys.executable, os.path.join(V144B, 'construye_termop.py'), '--verifica'], capture_output=True, text=True,",
             'runner: construye_termop en V144B')
    r = sust(r, "    return {n: h16(os.path.join(AQUI, n)) for n in CONSTRUIDOS}\n",
             "    r = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_examen_v144c.py'), '--verifica'], capture_output=True, text=True,\n"
             "                       encoding='utf-8', errors='replace')\n"
             "    if r.returncode != 0:\n"
             "        raise SystemExit(f'*** el runner o el arnes NO son la construccion por anclas desde el examen v14.4b:\\n{r.stdout[-1500:]}')\n"
             "    return {n: h16(os.path.join(V144B, n)) for n in CONSTRUIDOS}\n", 'runner: construidos en V144B + verifica v144c')
    r = sust(r, "                construye=h16(os.path.join(AQUI, 'construye_termop.py')),\n",
             "                construye=h16(os.path.join(V144B, 'construye_termop.py')),\n"
             "                construye_v144c=h16(os.path.join(AQUI, 'construye_examen_v144c.py')),\n", 'runner: SHAS construye')
    # regla 14: la letra de T-C (ii) es la de ERR-150; lo demas, identico a v14.3
    r = sust(r, "    R.append(('R5 LETRA de T-A, T-B, T-C, T-D, T-E, T-F y T-H == umbrales_examen_v143.LETRA (texto identico)',\n"
                "              all(U.LETRA[k] == U143.LETRA[k] for k in ('T-A', 'T-B', 'T-C_i', 'T-C_ii', 'T-D', 'T-E', 'T-F', 'T-H'))))\n",
             "    R.append(('R5 LETRA de T-A, T-B, T-C (i), T-D, T-E, T-F y T-H == umbrales_examen_v143.LETRA (texto identico)',\n"
             "              all(U.LETRA[k] == U143.LETRA[k] for k in ('T-A', 'T-B', 'T-C_i', 'T-D', 'T-E', 'T-F', 'T-H'))))\n"
             "    R.append(('R5 ERR-150: LETRA[T-C_ii] == la frase de ERR-150; la VIEJA (rev absoluto) == umbrales_examen_v143.LETRA[T-C_ii] '\n"
             "              '(se reporta) == umbrales_examen_v144b; T-G == la de v14.4b',\n"
             "              U.LETRA['T-C_ii'] == U.ERR150['frase'] and U.LETRA_TC_ii_REV_V4 == U143.LETRA['T-C_ii'] == U.ERR150['rev_v4_solo_informe']\n"
             "              and U.LETRA['T-G'] == U.U144B.LETRA['T-G'] and N_(U.TG) == N_(U.U144B.TG)))\n"
             "    jn150 = json.load(open(os.path.join(RAIZ, U.ERR150['nulo']['fuente']), encoding='utf-8'))\n"
             "    R.append(('R5 ERR-150: margen 0.125 == el del JSON del nulo (0.30 x (mediana S4 - 0.5)); z == NUM[z]; n == NUM[n_vivo]; '\n"
             "              'suelo 0.5; el JSON dice que la regla se sostiene y que tumba a TERMO; sha del JSON == el declarado',\n"
             "              U.ERR150['margen'] == jn150['margen']['C'] and U.ERR150['z'] == U.NUM['z'] == jn150['z'] and U.ERR150['n'] == U.NUM['n_vivo'] == jn150['n']\n"
             "              and U.ERR150['suelo_S4'] == 0.5 and all(jn150['condiciones'].values()) and jn150['anti_TERMO']['tumba'] is True\n"
             "              and h16(os.path.join(RAIZ, U.ERR150['nulo']['fuente'])) == U.ERR150['nulo']['sha']))\n",
             'runner: R5 ERR-150')
    r = sust(r, "and C4.semilla_real(49201, 'TRONCO_B') == 149201 and C4.semilla_real(49201, 'OFF') == 49201",
             "and C4.semilla_real(53201, 'TRONCO_B') == 153201 and C4.semilla_real(53201, 'OFF') == 53201", 'runner: semilla_real')
    r = sust(r, "              | set(range(47000, 48601)) | set(range(49001, 49100)) | set(range(49941, 49995)))",
             "              | set(range(47000, 48601)) | set(range(49001, 50000)) | set(range(149000, 150000)))", 'runner: usadas')
    r = sust(r, "all(49100 <= s <= 49940 or 149500 <= s <= 149999 for s in ss)", "all(53100 <= s <= 53999 or 153500 <= s <= 153999 for s in ss)",
             'runner: rango')
    r = sust(r, "dentro de 49100-49940 / 149500-149999, ninguna de V4-CAL, subida_n7, tronco_v14_3, los '\n"
                "              'examenes de v14.3 y v14.4, TERMO, el exploratorio de TERMO\\' ni la carrera de TERMO\\'; TRONCO_B s+100000 libre",
             "dentro de 53100-53999 / 153500-153999, ninguna de V4-CAL, subida_n7, tronco_v14_3, los '\n"
             "              'examenes de v14.3, v14.4 y v14.4b (49xxx y 149xxx enteros), TERMO ni TERMO\\'; TRONCO_B s+100000 libre", 'runner: frase R6')
    # la letra por visita, antes del veredicto del mundo vivo
    r = sust(r, "\n\ndef veredicto_vivo(res_vivo, res_rev):\n", LETRA_VISITA + "\ndef veredicto_vivo(res_vivo, res_rev):\n", 'runner: funciones ERR-150')
    r = sust(r, "    V = {c: C4.juzga(res_vivo, res_rev, c) for c in ('CAND', 'TRONCO_B', 'PLACEBO')}\n",
             "    V = {c: C4.juzga(res_vivo, res_rev, c) for c in ('CAND', 'TRONCO_B', 'PLACEBO')}\n"
             "    log(\"   (ERR-150) las lineas 'T-C ii' y '>>>' de arriba (corre_criterio_v4.juzga) usan rev ABSOLUTO: SOLO INFORME. \"\n"
             "        \"DECIDE la T-C (ii) POR VISITA:\")\n"
             "    for c in ('CAND', 'TRONCO_B', 'PLACEBO'):\n"
             "        tc_err150(V[c], res_rev, c)\n", 'runner: veredicto_vivo ERR-150')
    r = sust(r, "    log(f\"   T-H: NO MEDIDA — {U.LETRA['T-H']}\")\n",
             "    if viv is not None and 'T-C_ii' in viv['CAND'] and 'rev_absoluto_v4' in viv['CAND']['T-C_ii']:\n"
             "        rv_ = viv['CAND']['T-C_ii']['rev_absoluto_v4']\n"
             "        log(f\"   T-C (ii) letra VIEJA, rev absoluto (SOLO INFORME, ERR-150): {dl(rv_['pasa'])} [{U.LETRA_TC_ii_REV_V4}] \"\n"
             "            f\"rev {rv_['det']['rev_c']}/{rv_['det']['rev_o']} LI {rv_['det']['NI']['LI']}\")\n"
             "    log(f\"   T-H: NO MEDIDA — {U.LETRA['T-H']}\")\n", 'runner: etapa8 informe rev')
    # sinteticos: mordidas y visitas por cuarto (la letra por visita las lee); el MALO muerde A en Q4 como si no se desdijera
    r = sust(r, "        base = dict(rev=float(g.normal(42, 20)), deaths=float(g.normal(97, 10)), celdas=37.0, splits=float(g.integers(4, 10)),\n"
                "                    visA=[0, 0, 0, 1700], visB=[0, 0, 0, 220])\n"
                "        for arm in U.ARMS_VIVO:\n"
                "            x = dict(base) if arm in ('OFF', 'CAND') else dict(base, rev=float(g.normal(42, 20)))\n"
                "            if malo and arm == 'CAND':\n"
                "                x['rev'] -= 40.0\n",
             "        base = dict(rev=float(g.normal(42, 20)), deaths=float(g.normal(97, 10)), celdas=37.0, splits=float(g.integers(4, 10)),\n"
             "                    visA=[210, 210, 1700, 1700], visB=[1600, 1600, 220, 220],\n"
             "                    mordA=[205, 205, 160, int(g.integers(140, 180))], mordB=[150, 150, 190, int(g.integers(200, 218))])\n"
             "        for arm in U.ARMS_VIVO:\n"
             "            x = (dict(base) if arm in ('OFF', 'CAND') else\n"
             "                 dict(base, rev=float(g.normal(42, 20)), mordA=base['mordA'][:3] + [int(g.integers(140, 180))]))\n"
             "            if malo and arm == 'CAND':\n"
             "                x['rev'] -= 40.0\n"
             "                x['mordA'] = x['mordA'][:3] + [1100]   # ERR-150: en Q4 sigue mordiendo A (ahora veneno): S4 ~ 0.6, C ~ -0.3\n",
             'runner: sinteticos')
    r = sust(r, "        f\"termo {({k: v for k, v in o_rev['termo'].items()} if o_rev.get('termo') else None)} ({o_rev['seg']} s)\")\n",
             "        f\"termo {({k: v for k, v in o_rev['termo'].items()} if o_rev.get('termo') else None)} ({o_rev['seg']} s)\")\n"
             "    log(f\"   T-C ii CAND s{h[1]} POR VISITA (ERR-150; T = {Th}, UNA corrida, no es evidencia): S2 {S2_visita(o_rev):.4f} \"\n"
             "        f\"S4 {S4_visita(o_rev):.4f} C {C_visita(o_rev):+.4f}; visitas A {o_rev['visA']} B {o_rev['visB']}\")\n",
             'runner: humo por visita')
    r = sust(r, "VEREDICTO DEL EXAMEN: PASA -- v14.4b (v14.3 + TERMOP) cruza la letra de CRITERIO_TRONCO_v4 en serie y replica, en ",
             "VEREDICTO DEL EXAMEN: PASA -- v14.4b (v14.3 + TERMOP) cruza la letra de CRITERIO_TRONCO_v4 con T-C (ii) POR VISITA (ERR-150) en serie y replica, en ",
             'runner: combina PASA')
    r = sust(r, "ARRANQUE examen v4 sobre v14.4b = v14.3 + TERMOP — modo", "ARRANQUE examen v14.4c (v4 con T-C ii POR VISITA, ERR-150) sobre v14.4b = v14.3 + TERMOP — modo",
             'runner: arranque')
    r = sust(r, "letra=U.LETRA, err122=U.ERR122, tg=U.TG,", "letra=U.LETRA, err122=U.ERR122, err150=U.ERR150, tg=U.TG,", 'runner: meta err150', n=2)
    r = sust(r, "    log(f\"   letra: la del examen de v14.3 (T-B decide azar G2 con {list(U.NUM['TB_azar2'])}, ERR-122); T-G: {U.LETRA['T-G']}\")\n",
             "    log(f\"   letra: la del examen de v14.3 (T-B decide azar G2 con {list(U.NUM['TB_azar2'])}, ERR-122); T-G: {U.LETRA['T-G']}\")\n"
             "    log(f\"   T-C (ii) DECIDE: {U.LETRA['T-C_ii']}. La VIEJA se reporta: {U.LETRA_TC_ii_REV_V4}\")\n", 'runner: log letra')
    r = sust(r, "description='Examen del criterio de tronco v4 sobre v14.4b = v14.3 + TERMOP (ver PREREGISTRO_examen_v144c.md).')",
             "description='Examen v14.4c: criterio de tronco v4 con T-C (ii) POR VISITA (ERR-150) sobre v14.4b = v14.3 + TERMOP (ver PREREGISTRO_examen_v144c.md).')",
             'runner: descripcion')
    sha_an = hashlib.sha256(open(os.path.join(AQUI, 'analiza_nulo_err150.py'), 'rb').read()).hexdigest()[:16]
    ta144 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'datos', 'examen_v144_serie_20260928_123734_crudo_TA.json')
    r = sust(r, '@@SHA_ANALIZA@@', SHA_ANALIZA, 'runner: sha analiza')
    r = sust(r, '@@SHA_TA144@@', SHA_TA144, 'runner: sha TA v14.4')
    if sha_an != SHA_ANALIZA or hashlib.sha256(open(ta144, 'rb').read()).hexdigest()[:16] != SHA_TA144:
        raise SystemExit('*** analiza_nulo_err150.py o el crudo TA de v14.4 cambiaron de sha')
    out['corre_examen_v144c.py'] = CAB_R + r

    i = globales(origen(os.path.join(V144B, 'identidad_v144bex.py')), 'arnes')
    i = sust(i, "S = 49905 ", "S = 53955 ", 'arnes: semilla')
    i = sust(i, "R.tarea_vivo(('VIVO', 49906, ", "R.tarea_vivo(('VIVO', 53956, ", 'arnes: semilla K', n=3)
    i = sust(i, "        s_ = importlib.util.spec_from_file_location(n, os.path.join(AQUI, 'carros', n + '.py'))",
             "        s_ = importlib.util.spec_from_file_location(n, os.path.join(R.V144B, 'carros', n + '.py'))", 'arnes: carros en V144B')
    i = sust(i, "        p = os.path.join(AQUI, n_)\n", "        p = os.path.join(R.V144B, n_)\n", 'arnes: construidos en V144B')
    i = sust(i, "    anota('0', f'las {len(R.ANCLAS)} anclas reusadas tienen su sha (incluidos los dos carros de la carrera y el examen de v14.3)', not malas, str(malas))\n",
             "    anota('0', f'las {len(R.ANCLAS)} anclas reusadas tienen su sha (incluidos los dos carros de la carrera y el examen de v14.3)', not malas, str(malas))\n"
             "    import construye_examen_v144c as CX\n"
             "    for n_, txt in CX.construye().items():\n"
             "        p = os.path.join(AQUI, n_)\n"
             "        anota('0', f'{n_} en disco == construye_examen_v144c (por anclas desde el examen v14.4b)', os.path.exists(p) and open(p, 'rb').read().decode('utf-8') == txt)\n"
             "    anota('0', 'el organismo que corre es el de tronco_v14_4b_examen (no hay copia en esta carpeta)',\n"
             "          all(os.path.dirname(os.path.abspath(m_.__file__)) == os.path.abspath(R.V144B) for m_ in (V144, V144G, V144C, R.B144, R.G144))\n"
             "          and not any(os.path.exists(os.path.join(AQUI, f_)) for f_ in R.CONSTRUIDOS))\n",
             'arnes: (0) construccion v144c')
    i = sust(i, "    print('--- (K) controles que DEBEN fallar o diferir')\n", BLOQUE_E + "    print('--- (K) controles que DEBEN fallar o diferir')\n", 'arnes: bloque E')
    out['identidad_v144cex.py'] = CAB_I + i
    return out


SHA_ANALIZA = '29b268b0e1a56a86'   # analiza_nulo_err150.py (si cambia el analisis, el constructor se niega)
SHA_TA144 = '73014ef4831b957b'     # crudo TA del examen de v14.4 (lo lee el arnes (E))

BLOQUE_E = '''    print('--- (E) ERR-150: la T-C (ii) POR VISITA (sin simular)')
    import analiza_nulo_err150 as AN
    D150 = AN.carga()
    todas = [r_ for k_ in D150 for r_ in D150[k_]]
    anota('E', f'S2, S4 y C del runner == los de analiza_nulo_err150 en las {len(todas)} corridas de las siete fuentes del nulo (mismo numero, bit a bit)',
          all(R.S2_visita(r_) == AN.S2(r_) and R.S4_visita(r_) == AN.S4(r_) and R.C_visita(r_) == AN.C(r_) for r_ in todas))
    J150 = json.load(open(os.path.join(RAIZ, R.U.ERR150['nulo']['fuente']), encoding='utf-8'))
    mal150 = []
    for k_ in AN.CON_TB:   # las cinco series con n = 80 por brazo (A-CAL tiene 40: su numero lo da solo el analisis)
        off_ = R.C4.G(D150[k_], 'OFF')
        for a_ in ('TRONCO_B', 'PLACEBO', 'PEOR'):
            c_ = R.C4.G(D150[k_], a_)
            if not c_:
                continue
            p_, d_ = R.letra_TC_visita(off_, c_)
            ref_ = J150['realizaciones'][f'{k_}/{a_}']
            if p_ != ref_['letra'] or abs(d_['NI_C']['LI'] - ref_['det']['NI_C']['LI']) > 1e-3 or not p_:
                mal150.append((k_, a_, p_, d_['NI_C']['LI'], ref_['det']['NI_C']['LI']))
    anota('E', 'el juez del runner PASA a TRONCO_B, PLACEBO y PEOR en las cinco series con n = 80, con los mismos LI que el analisis del nulo', not mal150, str(mal150[:3]))
    D144 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen', 'datos'); s144 = 'examen_v144_serie_20260928_123734'
    Vr144 = json.load(open(os.path.join(D144, s144 + '.json'), encoding='utf-8'))['veredictos']
    lee144 = lambda etq: json.load(open(os.path.join(D144, f'{s144}_crudo_{etq}.json'), encoding='utf-8'))['corridas']
    vv = callado(R.veredicto_vivo, lee144('TA'), lee144('TCii'))
    anota('E', 'examen de v14.4 (TERMO): la T-C (ii) VIEJA que el juez reporta == la registrada (CAND NO, TRONCO_B y PLACEBO PASA; mismas NI)',
          all(vv[a_]['T-C_ii']['rev_absoluto_v4']['pasa'] == Vr144['vivo'][a_]['T-C_ii']['v4']
              and N(vv[a_]['T-C_ii']['rev_absoluto_v4']['det']['NI']) == N(Vr144['vivo'][a_]['T-C_ii']['det_v4']['NI'])
              for a_ in ('CAND', 'TRONCO_B', 'PLACEBO')) and Vr144['vivo']['CAND']['T-C_ii']['v4'] is False)
    dT = vv['CAND']['T-C_ii']['det_visita']
    anota('E', f"ANTI-TERMO: con la letra POR VISITA TERMO SIGUE CAYENDO T-C (ii) (C LI {dT['NI_C']['LI']} <= -0.125 Y S4 {dT['S4'][0]:.3f} <= 0.5) "
               f"y su v4 del mundo vivo sigue NO; el LI == el del analisis ({J150['anti_TERMO']['det']['NI_C']['LI']})",
          vv['CAND']['T-C_ii']['v4'] is False and dT['NI_C']['pasa'] is False and dT['suelo'] is False and vv['CAND']['v4'] is False
          and abs(dT['NI_C']['LI'] - J150['anti_TERMO']['det']['NI_C']['LI']) < 1e-3)
    anota('E', 'examen de v14.4: TRONCO_B y PLACEBO PASAN la T-C (ii) por visita y la serie se sigue leyendo (legible == lo registrado)',
          vv['TRONCO_B']['T-C_ii']['v4'] and vv['PLACEBO']['T-C_ii']['v4'] and vv['legible'] == Vr144['vivo']['legible'] is True)
    anota('E', 'examen de v14.4: T-A de CAND, TRONCO_B y PLACEBO == lo registrado (ERR-150 no toca T-A)',
          all(vv[a_]['T-A']['v4'] == Vr144['vivo'][a_]['T-A']['v4'] for a_ in ('CAND', 'TRONCO_B', 'PLACEBO')))
    off_ = R.C4.G(D150['v144_serie'], 'OFF'); tb_ = R.C4.G(D150['v144_serie'], 'TRONCO_B'); te_ = R.C4.G(D150['v144_serie'], 'CAND')
    sw_ = [dict(r_, mordA=r_['mordA'][:3] + [r_['mordB'][3]], mordB=r_['mordB'][:3] + [r_['mordA'][3]],
                visA=r_['visA'][:3] + [r_['visB'][3]], visB=r_['visB'][:3] + [r_['visA'][3]]) for r_ in tb_]
    ind_ = [dict(r_, mordA=[v_ // 2 for v_ in r_['visA']], mordB=[v_ // 2 for v_ in r_['visB']]) for r_ in tb_]
    g150 = np.random.default_rng(150)
    fl_ = [AN.adelgaza(r_, 0.5, g150, True) for r_ in tb_]
    fl_ = [dict(r_, rev=r_['mordB'][3] - r_['mordA'][3]) for r_ in fl_]   # la letra vieja lee la clave 'rev' (tarea_rev la calcula asi)
    p_sw, d_sw = R.letra_TC_visita(off_, sw_); p_in, d_in = R.letra_TC_visita(off_, ind_); p_fl, d_fl = R.letra_TC_visita(off_, fl_)
    anota('E', f"control que DEBE caer: A y B intercambiados en Q4 (no se desdice) -> NO (C LI {d_sw['NI_C']['LI']})", p_sw is False)
    anota('E', f"control que DEBE caer: organismo INDIFERENTE (muerde la mitad de todo): la NI sola pasa (LI {d_in['NI_C']['LI']}) y el SUELO lo "
               f"tumba (S4 {d_in['S4'][0]:.3f})", p_in is False and d_in['NI_C']['pasa'] is True and d_in['suelo'] is False)
    anota('E', f"'come menos' (lo BUENO mordido la mitad, antes y despues) PASA la letra nueva (C LI {d_fl['NI_C']['LI']}) y CAE la vieja",
          p_fl is True and R.C4.letra_TC(off_, fl_, R.C4.U.V4['T-C_ii'])[0] is False)
    u0 = dict(R.U.ERR150)
    try:
        R.U.ERR150['suelo_S4'] = -1.0; R.U.ERR150['margen'] = 0.49
        p_mut, _ = R.letra_TC_visita(off_, te_)
    finally:
        R.U.ERR150.clear(); R.U.ERR150.update(u0)
    anota('E', 'una letra MUTADA (margen 0.49, sin suelo) deja pasar a TERMO: son el margen 0.125 y el suelo los que lo tumban (dientes de (E))',
          p_mut is True and R.letra_TC_visita(off_, te_)[0] is False)
'''


if __name__ == '__main__':
    ver = '--verifica' in sys.argv
    if [a for a in sys.argv[1:] if a != '--verifica']: raise SystemExit('*** uso: construye_examen_v144c.py [--verifica]')
    malo = 0
    for n, t in construye().items():
        p = os.path.join(AQUI, n); b = t.encode('utf-8')
        if ver:
            ok = os.path.exists(p) and open(p, 'rb').read() == b; malo += not ok
            print(f"{'OK  ' if ok else 'DIFIERE'} {n:24s} {h16b(b)}")
        else:
            open(p, 'wb').write(b); print(f'escrito {n:24s} {h16b(b)}')
    sys.exit(1 if malo else 0)
