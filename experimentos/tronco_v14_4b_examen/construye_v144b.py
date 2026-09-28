"""construye_v144b.py -- CONSTRUCTOR POR ANCLAS del candidato v14.4b = v14.3 (TRONCO) + TERMO' (TERMO con la tabla que OLVIDA y
sin consigna donde no hay umbral de parto). Diseno decidido por el coordinador (28-sep-2026, tras el NO PASA de TERMO en la serie
47001-...: cae T-C ii y T-E); este archivo lo CONSTRUYE, no lo cambia.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

No corre nada. Los ORIGENES son los archivos del examen de TERMO (experimentos/tronco_v14_4_examen/, SOLO se leen) y el carro de la
carrera V143_TERMO; el sha de cada uno se verifica ANTES de escribir (si uno cambio, no se escribe nada). Cada ancla aparece EXACTAMENTE
las veces declaradas (n = 1 salvo los RENOMBRES de modulo, que llevan su cuenta exacta como tripwire).

LOS DOS CAMBIOS (y solo esos) respecto de v14.4:
  (1) LA TABLA OLVIDA. Donde TERMO guardaba por estimulo mordido la SUMA del dS nominal y el numero de mordidas (s = suma / n),
      TERMO' guarda el ULTIMO dS nominal sentido: _adS[k] = [dS_0, (dS_1,) 1]. La letra `termo_letra` es el MISMO texto que en
      v14.4 (lee s = m[j] / m[-1] = dS_j / 1 = dS_j). Con dS fijo por estimulo da la misma s que la media (salvo ulp) -> las mismas
      decisiones; tras una reversion, UNA mordida basta para que lo que fue bueno deje de ser "sentido bueno". Memoria: la misma
      forma que en v14.4 (2 o 3 numeros por estimulo), el contador de mordidas pasa a ser la constante 1.
  (2) SIN UMBRAL DE PARTO NO HAY CONSIGNA. En organismo_v144b y organismo_v144bg (UNA necesidad, sin medida de parto) el kwarg
      rep_umbral pasa a defecto None, y la pieza con rep_umbral None NO decide: devuelve la decision de v14.3 tal cual (sin tocar
      contadores). La guarda es el MISMO texto en los tres organismos; en organismo_v144bcal el defecto sigue siendo 1.0 (ahi la
      pieza ACTUA: T-A, T-C ii, T-D, T-G).
Todo lo demas: v14.4 (misma letra, mismo TERMOINV como control de T-G, mismos contadores de solo lectura).

Escribe en ESTA carpeta (experimentos/tronco_v14_4b_examen/):
  organismo_v144b.py            <- tronco_v14_4_examen/organismo_v144.py            (e3768f6eab05b964)
  organismo_v144bg.py           <- tronco_v14_4_examen/organismo_v144g.py           (1ea7fb43f41a69c5)
  organismo_v144bcal.py         <- tronco_v14_4_examen/organismo_v144cal.py         (a5a891e1d819e1bb)
  bateria_v144b.py              <- tronco_v14_4_examen/bateria_v144.py              (e928b202d9d66702)
  bateria_generaliza_v144b.py   <- tronco_v14_4_examen/bateria_generaliza_v144.py   (3263ab8d8f45e7cd)
  corre_examen_v144b.py         <- tronco_v14_4_examen/corre_examen_v144.py         (8bb63d3f421040dd)   el runner
  umbrales_examen_v144b.py      <- tronco_v14_4_examen/umbrales_examen_v144.py      (0df02bd6a4d548c4)   letra + semillas + PRED
  busca_semillas_v144b.py       <- tronco_v14_4_examen/busca_semillas_v144.py       (e3220d8311115207)
  carros/V143_TERMOB.py         <- organelos/termo/carros/V143_TERMO.py             (3db639cab75641fb)   carro de la pista (muro)

    python experimentos/tronco_v14_4b_examen/construye_v144b.py              (escribe; imprime los sha)
    python experimentos/tronco_v14_4b_examen/construye_v144b.py --verifica   (no escribe; sale 1 si algo en disco != construccion)
"""
import hashlib, os, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
V144EX = os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen')
TERMO = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')

ORIGENES = {   # tripwire: si un origen cambio, no se escribe nada
    os.path.join(V144EX, 'organismo_v144.py'): 'e3768f6eab05b964',
    os.path.join(V144EX, 'organismo_v144g.py'): '1ea7fb43f41a69c5',
    os.path.join(V144EX, 'organismo_v144cal.py'): 'a5a891e1d819e1bb',
    os.path.join(V144EX, 'bateria_v144.py'): 'e928b202d9d66702',
    os.path.join(V144EX, 'bateria_generaliza_v144.py'): '3263ab8d8f45e7cd',
    os.path.join(V144EX, 'corre_examen_v144.py'): '8bb63d3f421040dd',
    os.path.join(V144EX, 'umbrales_examen_v144.py'): '0df02bd6a4d548c4',
    os.path.join(V144EX, 'busca_semillas_v144.py'): 'e3220d8311115207',
    os.path.join(V144EX, 'construye_v144.py'): '91b7d110780f336e',          # solo se lee: el constructor de v14.4 (su --verifica)
    os.path.join(TERMO, 'carros', 'V143_TERMO.py'): '3db639cab75641fb',
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def h16t(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()[:16]


def origen(ruta):
    s = h16(ruta)
    if s != ORIGENES[ruta]:
        raise SystemExit(f'*** ORIGEN {os.path.relpath(ruta, RAIZ)}: sha {s}, se esperaba {ORIGENES[ruta]}. No se escribe nada.')
    return open(ruta, 'rb').read().decode('utf-8')


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


def renombra(t, pares, etq):
    """RENOMBRES de modulo/archivo: cada par (viejo, nuevo, n) con su cuenta EXACTA (tripwire). Los PROTEGIDOS (artefactos de v14.4
    que se siguen leyendo tal cual: el nulo de T-G) se sacan antes y se devuelven despues."""
    PROT = [('potencia_examen_v144_20260928_121917', '\x00P1\x00'), ('analiza_potencia_v144', '\x00P2\x00')]
    for a, b in PROT:
        t = t.replace(a, b)
    for a, b, n in pares:
        t = sust(t, a, b, n=n, etq=f'{etq}: renombre {a!r}')
    for a, b in PROT:
        t = t.replace(b, a)
    return t


# ================================================================ (1) y (2): el MISMO texto en los tres organismos
EST_144 = ("    _adS={}; _tm=dict(dec=0,a_no=0,a_si=0,mord=0)   # v14.4 TERMO: MEMORIA NUEVA (lo SENTIDO por estimulo mordido: sumas de dS "
           "nominal por necesidad y mordidas; como APR._apr_dS, sin olvido) y contadores de SOLO LECTURA\n"
           "    def _tm_boca(_k,_lev,_mf):   # v14.4 TERMO: decide sobre lo sentido bueno (despues del sorteo de la boca, que no cambia)\n")
EST_144B = ("    _adS={}; _tm=dict(dec=0,a_no=0,a_si=0,mord=0)   # v14.4b TERMO': MEMORIA (lo SENTIDO por estimulo mordido: el ULTIMO dS "
            "nominal por necesidad y la constante 1 -> la tabla OLVIDA) y contadores de SOLO LECTURA\n"
            "    def _tm_boca(_k,_lev,_mf):   # v14.4 TERMO: decide sobre lo sentido bueno (despues del sorteo de la boca, que no cambia)\n"
            "        if rep_umbral is None: return _mf   # v14.4b (2): SIN UMBRAL DE PARTO NO HAY CONSIGNA -> la boca de v14.3 tal cual (ni contadores)\n")
MEM1_144 = ("                if termo: _m9=_adS.setdefault(kk,[0.0,0]); _m9[0]+=float(E_VAL[val[kk]]); _m9[1]+=1   "
            "# v14.4 TERMO: lo SENTIDO (dS nominal)\n")
MEM1_144B = ("                if termo: _adS[kk]=[float(E_VAL[val[kk]]),1]   # v14.4b (1) LA TABLA OLVIDA: el ULTIMO dS nominal sentido "
             "(la letra lee s = dS / 1)\n")
MEM2_144 = ("                if termo: _m9=_adS.setdefault(kk,[0.0,0.0,0]); _m9[0]+=float(_dS[0]); _m9[1]+=float(_dS[1]); _m9[2]+=1   "
            "# v14.4 TERMO: lo SENTIDO (dS nominal)\n")
MEM2_144B = ("                if termo: _adS[kk]=[float(_dS[0]),float(_dS[1]),1]   # v14.4b (1) LA TABLA OLVIDA: el ULTIMO dS nominal sentido "
             "(la letra lee s = dS / 1)\n")

CAB_144B = '''"""organismo_v144b = v14.4b (CANDIDATO) = TRONCO v14.3 + TERMO' . Entra al tronco SOLO si pasa el examen del CRITERIO DE TRONCO
v4 en serie y replica, con la puerta nueva T-R (experimentos/tronco_v14_4b_examen/PREREGISTRO_examen_v144b.md).
Origen: experimentos/tronco_v14_4_examen/organismo_v144.py (e3768f6eab05b964 = v14.3 + TERMO; solo se leyo). Cambia DOS cosas:
  (1) la tabla de lo sentido OLVIDA: _adS[k] = [ultimo dS nominal, 1] (TERMO: [suma, mordidas]);
  (2) UNA necesidad, sin medida de parto: rep_umbral por defecto None -> la pieza NO decide (la boca de v14.3 tal cual). Con los
      defectos, termo=1 es organismo_v143 en la FISICA bit a bit (arnes identidad_v144bex.py). Con rep_umbral=1.0 explicito la pieza
      actua como en TERMO, con la tabla que olvida.
Con termo=0 es organismo_v143 EXACTO. Generado POR ANCLAS por experimentos/tronco_v14_4b_examen/construye_v144b.py. NO editar a mano.
Lo que sigue es el docstring del origen (v14.4)."""
'''
CAB_144BG = '''"""organismo_v144bg = instrumento de MUNDO DE REGLA de v14.4b (lo usa bateria_generaliza_v144b.py). Origen:
experimentos/tronco_v14_4_examen/organismo_v144g.py (1ea7fb43f41a69c5; solo se leyo) con los DOS cambios de TERMO' (tabla que olvida;
rep_umbral None por defecto -> la pieza no decide: con los defectos es organismo_v143g en la FISICA). Generado POR ANCLAS por
experimentos/tronco_v14_4b_examen/construye_v144b.py. NO editar a mano. Lo que sigue es el docstring del origen."""
'''
CAB_144BCAL = '''"""organismo_v144bcal = v14.4b en el MUNDO VIVO del criterio v4 (instrumento del examen, no se congela con el tronco). Origen:
experimentos/tronco_v14_4_examen/organismo_v144cal.py (a5a891e1d819e1bb; solo se leyo) con la TABLA QUE OLVIDA ((1): _adS[k] =
[ultimo dE, ultimo dAg, 1]) y la guarda de (2) (rep_umbral None -> no decide). Aqui rep_umbral sigue con defecto 1.0: la pieza ACTUA
(T-A, T-C ii, T-D, T-G), tambien donde reproduccion=0 (T-C ii y T-D; ver PREREGISTRO_examen_v144b.md sec. 7). termo=2 = TERMOINV.
Con termo=0 es organismo_v143cal EXACTO. Generado POR ANCLAS por experimentos/tronco_v14_4b_examen/construye_v144b.py. NO editar a
mano. Lo que sigue es el docstring del origen."""
'''
CAB_BAT = '''"""bateria_v144b = experimentos/tronco_v14_4_examen/bateria_v144.py (e928b202d9d66702; solo se leyo) con el modulo examinado
renombrado a organismo_v144b (y sus salidas a examen_v144b_*). Etapas, CRIT y umbrales del criterio v3' INTACTOS. Generado POR ANCLAS
por experimentos/tronco_v14_4b_examen/construye_v144b.py. NO editar a mano. Lo que sigue es el docstring del origen (renombrado)."""
'''
CAB_GEN = '''"""bateria_generaliza_v144b = experimentos/tronco_v14_4_examen/bateria_generaliza_v144.py (3263ab8d8f45e7cd; solo se leyo) con la
entrada del candidato renombrada: organismo_v144b -> organismo_v144bg, kwargs CAMPO A CAMPO == los de organismo_v143 (regla 14). Las
entradas del tronco intactas; umbrales intactos. Generada POR ANCLAS por experimentos/tronco_v14_4b_examen/construye_v144b.py. NO
editar a mano. Lo que sigue es el docstring del origen (renombrado)."""
'''


def organismo(t, cab, una, etq):
    if una:
        t = sust(t, "termo=1,rep_umbral=1.0):", "termo=1,rep_umbral=None):", etq=f'{etq}: firma (2)')
        t = sust(t, MEM1_144, MEM1_144B, etq=f'{etq}: la tabla olvida (1)')
    else:
        t = sust(t, MEM2_144, MEM2_144B, etq=f'{etq}: la tabla olvida (1)')
    t = sust(t, EST_144, EST_144B, etq=f'{etq}: estado y guarda (2)')
    return cab + t


# ================================================================ el RUNNER (corre_examen_v144 -> corre_examen_v144b)
DOC_RUN = '''"""corre_examen_v144b.py -- EXAMEN DEL CRITERIO DE TRONCO v4 sobre v14.4b = v14.3 + TERMO' (TERMO con la tabla que OLVIDA y sin
consigna donde no hay umbral de parto), con la PUERTA NUEVA T-R. Copia POR ANCLAS de experimentos/tronco_v14_4_examen/corre_examen_v144.py
(8bb63d3f421040dd) hecha por construye_v144b.py. Cambia SOLO: los modulos (v144 -> v144b), las semillas (umbrales_examen_v144b), las
comprobaciones R de defectos (organismo_v144b/v144bg: rep_umbral None), las anclas y la puerta T-R:
  T-R (mas estricta; no reemplaza nada): T-C (ii) pasa por la letra v4 Y la pieza ACTUA (a_no + a_si > 0) en >= 95 % de las
  corridas CAND de T-C (ii) (G-3 analogo). Una reversion que se pasa con la pieza muda no cuenta.
La letra T-A..T-G es la de v14.4 (T-A..T-F y T-H importadas de umbrales_examen_v143) sin tocar un numero. NO editar a mano.
Lo que sigue es el docstring del origen (renombrado)."""
'''


def runner(t):
    t = renombra(t, [('v14.4', 'v14.4b', 9), ("v14.4b = v14.3 + TERMO", "v14.4b = v14.3 + TERMO′", 3),
                     ('experimentos/tronco_v14_4_examen/', 'experimentos/tronco_v14_4b_examen/', 6), ('v144', 'v144b', 74)], 'runner')
    t = sust(t, "V143EX = os.path.join(EXP, 'tronco_v14_3_examen')\n",
             "V143EX = os.path.join(EXP, 'tronco_v14_3_examen')\n"
             "V144EX = os.path.join(EXP, 'tronco_v14_4_examen')   # v14.4b: el examen de TERMO (origen por anclas; su serie se relee en el arnes)\n",
             etq='runner: V144EX')
    t = sust(t, "for _p in (V143EX, os.path.join(TERMO_DIR, 'carros')):   # AL FINAL: solo organismo_v143cal, umbrales_examen_v143 y los carros\n",
             "for _p in (V143EX, os.path.join(TERMO_DIR, 'carros'), V144EX):   # AL FINAL: solo organismo_v143cal, umbrales_examen_v143, "
             "los carros y (v14.4b) los modulos de TERMO para compararlos\n", etq='runner: sys.path')
    t = sust(t, "    os.path.join(RAIZ, 'datos', 'humo', 'potencia_examen_v144_20260928_121917.json'): '4e4df40a5c3cc67d',\n}\n",
             "    os.path.join(RAIZ, 'datos', 'humo', 'potencia_examen_v144_20260928_121917.json'): '4e4df40a5c3cc67d',\n"
             "    # v14.4b: los ORIGENES (TERMO, solo se leen) y la serie de TERMO (el juez la reproduce: identidad_v144bex (J))\n"
             "    os.path.join(V144EX, 'organismo_v144.py'): 'e3768f6eab05b964',\n"
             "    os.path.join(V144EX, 'organismo_v144g.py'): '1ea7fb43f41a69c5',\n"
             "    os.path.join(V144EX, 'organismo_v144cal.py'): 'a5a891e1d819e1bb',\n"
             "    os.path.join(V144EX, 'corre_examen_v144.py'): '8bb63d3f421040dd',\n"
             "    os.path.join(V144EX, 'umbrales_examen_v144.py'): '0df02bd6a4d548c4',\n"
             "    os.path.join(V144EX, 'datos', 'examen_v144_serie_20260928_123734.json'): '25458f0f470b25e6',\n"
             "    os.path.join(V144EX, 'datos', 'examen_v144_serie_20260928_123734_crudo_TB.json'): '97fa7727869cec27',\n"
             "    os.path.join(V144EX, 'datos', 'examen_v144_serie_20260928_123734_crudo_EX.json'): 'd1c8521ecbf7410e',\n"
             "    os.path.join(V144EX, 'datos', 'examen_v144_serie_20260928_123734_crudo_TD.json'): '0bd40d8d5b58afa3',\n"
             "    os.path.join(V144EX, 'datos', 'examen_v144_serie_20260928_123734_crudo_TCii.json'): 'd7b018cfd63d8eb6',\n"
             "    os.path.join(V144EX, 'datos', 'examen_v144_serie_20260928_123734_crudo_TA.json'): '73014ef4831b957b',\n}\n",
             etq='runner: ANCLAS')
    t = sust(t, "CONSTRUIDOS = ('organismo_v144b.py', 'organismo_v144bg.py', 'organismo_v144bcal.py', 'bateria_v144b.py', 'bateria_generaliza_v144b.py')\n",
             "CONSTRUIDOS = ('organismo_v144b.py', 'organismo_v144bg.py', 'organismo_v144bcal.py', 'bateria_v144b.py', 'bateria_generaliza_v144b.py',\n"
             "               'corre_examen_v144b.py', 'umbrales_examen_v144b.py', 'busca_semillas_v144b.py', 'carros/V143_TERMOB.py')\n",
             etq='runner: CONSTRUIDOS')
    # ---- regla 14: la nueva verdad de los defectos, la letra == la de TERMO, semillas
    t = sust(t, "and C4.semilla_real(47101, 'TRONCO_B') == 147101 and C4.semilla_real(47101, 'OFF') == 47101))",
             "and C4.semilla_real(49101, 'TRONCO_B') == 149101 and C4.semilla_real(49101, 'OFF') == 49101))", etq='runner: R1 TRONCO_B')
    t = sust(t, "    R.append(('R3 organismo_v144bg: mismos defectos que organismo_v143g + termo=1 y rep_umbral=1.0 (la pieza, encendida por defecto)',\n"
                "              all(d144g[k] == v for k, v in d143g.items()) and set(d144g) - set(d143g) == {'termo', 'rep_umbral'}\n"
                "              and d144g['termo'] == 1 and d144g['rep_umbral'] == 1.0))\n",
             "    R.append(('R3 organismo_v144bg: mismos defectos que organismo_v143g + termo=1 y rep_umbral=None (v14.4b (2): una necesidad, '\n"
             "              'sin umbral de parto -> la pieza no decide)',\n"
             "              all(d144g[k] == v for k, v in d143g.items()) and set(d144g) - set(d143g) == {'termo', 'rep_umbral'}\n"
             "              and d144g['termo'] == 1 and d144g['rep_umbral'] is None))\n", etq='runner: R3 defectos')
    t = sust(t, "    R.append(('R4 organismo_v144b: mismos defectos que organismo_v143 + termo=1 y rep_umbral=1.0',\n"
                "              all(d144[k] == v for k, v in d143.items()) and set(d144) - set(d143) == {'termo', 'rep_umbral'}\n"
                "              and d144['termo'] == 1 and d144['rep_umbral'] == 1.0))\n",
             "    R.append(('R4 organismo_v144b: mismos defectos que organismo_v143 + termo=1 y rep_umbral=None (v14.4b (2))',\n"
             "              all(d144[k] == v for k, v in d143.items()) and set(d144) - set(d143) == {'termo', 'rep_umbral'}\n"
             "              and d144['termo'] == 1 and d144['rep_umbral'] is None))\n", etq='runner: R4 defectos')
    t = sust(t, "              inspect.getsource(V144.termo_letra) == inspect.getsource(V144G.termo_letra) == inspect.getsource(V144C.termo_letra)))\n",
             "              inspect.getsource(V144.termo_letra) == inspect.getsource(V144G.termo_letra) == inspect.getsource(V144C.termo_letra)))\n"
             "    import organismo_v144 as T144, organismo_v144g as T144G, organismo_v144cal as T144C   # TERMO (v14.4; solo se leen)\n"
             "    R.append(('R4 v14.4b: la letra de la pieza es EXACTAMENTE la de TERMO (v14.4): mismo texto de termo_letra en los seis organismos',\n"
             "              all(inspect.getsource(m.termo_letra) == inspect.getsource(V144C.termo_letra) for m in (T144, T144G, T144C))))\n"
             "    R.append(('R4 v14.4b: organismo_v144bcal tiene los MISMOS defectos que organismo_v144cal (TERMO en el mundo vivo; rep_umbral 1.0)',\n"
             "              _defectos(V144C.run) == _defectos(T144C.run)))\n"
             "    R.append(('R4 v14.4b T-R: letra declarada y umbral de actuacion == el de G-3 (0.95), n == n_vivo (80)',\n"
             "              'T-R' in U.LETRA and U.TR['actua_frac'] == U.TG['actua_frac'] == 0.95 and U.TR['n'] == U.NUM['n_vivo']))\n",
             etq='runner: R4 letra de TERMO')
    t = sust(t, "              | set(range(43000, 44601)) | set(range(39001, 39141)) | set(range(39901, 39915)))\n"
                "    R.append(('R6 semillas: todas distintas entre papeles, dentro de 47000-48600, ninguna de V4-CAL, subida_n7, tronco_v14_3, el '\n"
                "              'examen de v14.3 ni TERMO; TRONCO_B s+100000 (147xxx) libre',\n"
                "              len(ss) == len(set(ss)) and not (set(ss) & usadas) and all(47000 <= s <= 48600 for s in ss)))\n",
             "              | set(range(43000, 44601)) | set(range(39001, 39141)) | set(range(39901, 39915))\n"
             "              | set(range(47000, 48601)) | set(range(41001, 41051)))   # v14.4b: + el examen de TERMO (47000-48600) y TERMO_EVO\n"
             "    viv = [s for m_ in ('serie', 'replica', 'reserva') for s in U.SEMILLAS[m_]['VIVO']]\n"
             "    R.append(('R6 semillas: todas distintas entre papeles, dentro de 49001-50600 sin 50000, ninguna de V4-CAL, subida_n7, '\n"
             "              'tronco_v14_3, el examen de v14.3, TERMO, TERMO_EVO ni el examen de TERMO; TRONCO_B s+100000 (149xxx) sin choque',\n"
             "              len(ss) == len(set(ss)) and not (set(ss) & usadas) and all(49001 <= s <= 50600 and s != 50000 for s in ss)\n"
             "              and not ({s + U.DESPL_TRONCO_B for s in viv} & set(ss)) and all(149001 <= s + U.DESPL_TRONCO_B <= 149999 for s in viv)))\n",
             etq='runner: R6 semillas')
    # ---- T-R: la puerta nueva
    t = sust(t, "    V['termo_TC'] = _tele([r for r in res_rev if r['arm'] == 'CAND'])\n",
             "    V['termo_TC'] = _tele([r for r in res_rev if r['arm'] == 'CAND'])\n"
             "    _cii = V['CAND'].get('T-C_ii'); _tc = V['termo_TC'] or dict(n=0, actua=0)   # v14.4b T-R: T-C (ii) con la pieza ACTUANDO\n"
             "    _fr = (round(_tc['actua'] / _tc['n'], 3) if _tc['n'] else None)\n"
             "    V['T_R'] = dict(T_C_ii=(None if _cii is None else bool(_cii['v4'])), actua=_tc['actua'], n=_tc['n'], frac=_fr,\n"
             "                    pasa=bool(_cii is not None and _cii['v4'] and _tc['n'] == U.TR['n'] and _fr is not None and _fr >= U.TR['actua_frac']))\n"
             "    log(f\"   T-R [{U.LETRA['T-R']}] -> T-C (ii) {V['T_R']['T_C_ii']}, la pieza actua en {_tc['actua']}/{_tc['n']} corridas CAND \"\n"
             "        f\"(>= {U.TR['actua_frac']}, n == {U.TR['n']}) -> {'PASA' if V['T_R']['pasa'] else 'NO'}\")\n",
             etq='runner: T-R en veredicto_vivo')
    t = sust(t, "SUB = ('T-A', 'T-B', 'T-C_i', 'T-C_ii', 'T-D', 'T-E', 'T-F_examen', 'T-F_vivo', 'T-G')\n"
                "PUERTAS = ('T-A', 'T-B', 'T-C', 'T-D', 'T-E', 'T-F', 'T-G')\n",
             "SUB = ('T-A', 'T-B', 'T-C_i', 'T-C_ii', 'T-D', 'T-E', 'T-F_examen', 'T-F_vivo', 'T-G', 'T-R')\n"
             "PUERTAS = ('T-A', 'T-B', 'T-C', 'T-D', 'T-E', 'T-F', 'T-G', 'T-R')   # v14.4b: + T-R (mas estricta; no reemplaza nada)\n",
             etq='runner: SUB y PUERTAS')
    t = sust(t, "        'T-G': None if 'TG' not in V else bool(V['TG']['pasa']),\n    }\n",
             "        'T-G': None if 'TG' not in V else bool(V['TG']['pasa']),\n"
             "        'T-R': None if viv is None or 'T_R' not in viv else bool(viv['T_R']['pasa']),   # v14.4b\n    }\n",
             etq='runner: subpuertas T-R')
    t = sust(t, "    \"\"\"Las siete puertas eliminatorias de v4 (una caida -> no entra); T-H reportada aparte.\"\"\"\n",
             "    \"\"\"Las siete puertas eliminatorias de v4 + T-R (v14.4b; una caida -> no entra); T-H reportada aparte.\"\"\"\n",
             etq='runner: puertas_de doc')
    t = sust(t, "            'T-E': sub['T-E'], 'T-F': _y(sub['T-F_examen'], sub['T-F_vivo']), 'T-G': sub['T-G']}\n",
             "            'T-E': sub['T-E'], 'T-F': _y(sub['T-F_examen'], sub['T-F_vivo']), 'T-G': sub['T-G'], 'T-R': sub['T-R']}\n",
             etq='runner: puertas_de T-R')
    t = sust(t, "VIVAS = ('T-A', 'T-C_ii', 'T-F_vivo', 'T-G')   # lo que la RESERVA sustituye (todo lo que sale del mundo vivo)\n",
             "VIVAS = ('T-A', 'T-C_ii', 'T-F_vivo', 'T-G', 'T-R')   # lo que la RESERVA sustituye (todo lo que sale del mundo vivo; v14.4b: + T-R)\n",
             etq='runner: VIVAS')
    t = sust(t, "las siete puertas eliminatorias pasan (T-H no medida, reportada)",
             "las ocho puertas eliminatorias pasan (siete de v4 + T-R; T-H no medida, reportada)", etq='runner: frase PASA')
    t = sust(t, "\"VEREDICTO DEL EXAMEN: PASA -- v14.4b (v14.3 + TERMO) cruza la letra de CRITERIO_TRONCO_v4 en serie y replica, en \"",
             "\"VEREDICTO DEL EXAMEN: PASA -- v14.4b (v14.3 + TERMO') cruza la letra de CRITERIO_TRONCO_v4 y T-R en serie y replica, en \"",
             etq='runner: combina PASA')
    t = sust(t, "            if malo and arm == 'CAND':\n                x['rev'] -= 40.0\n",
             "            if malo and arm == 'CAND':\n                x['rev'] -= 40.0\n"
             "            if arm == 'CAND':\n                x['termo'] = dict(tele)   # v14.4b T-R: la pieza actua en T-C (ii)\n",
             etq='runner: sinteticos T-R')
    t = sust(t, "    actua = bool(t_c and t_k and t_c['a_no'] + t_c['a_si'] > 0 and t_k['a_no'] + t_k['a_si'] > 0)\n",
             "    actua = bool(t_c and t_k and t_c['a_no'] + t_c['a_si'] > 0 and t_k['a_no'] + t_k['a_si'] > 0)\n"
             "    t_r = o_rev.get('termo'); actua_rev = bool(t_r and t_r['a_no'] + t_r['a_si'] > 0)   # v14.4b T-R: la pieza actua en T-C (ii)\n"
             "    log(f\"   v14.4b T-R: la pieza ACTUA en T-C (ii) CAND s{h[1]} (a_no + a_si > 0): {actua_rev}\")\n"
             "    actua = bool(actua and actua_rev)\n", etq='runner: humo actua T-C ii')
    t = sust(t, "and not any(cab['malo']['puertas'][k] for k in ('T-A', 'T-B', 'T-C', 'T-D', 'T-G')))",
             "and not any(cab['malo']['puertas'][k] for k in ('T-A', 'T-B', 'T-C', 'T-D', 'T-G', 'T-R')))", etq='runner: cableado malo')
    t = sust(t, "(el bueno DEBE pasar todo; el malo DEBE caer T-A, T-B, T-C, T-D y T-G)",
             "(el bueno DEBE pasar todo; el malo DEBE caer T-A, T-B, T-C, T-D, T-G y T-R)", etq='runner: cableado texto')
    return DOC_RUN + t


# ================================================================ UMBRALES (letra + semillas + predicciones)
DOC_UMB = '''"""umbrales_examen_v144b = experimentos/tronco_v14_4_examen/umbrales_examen_v144.py (0df02bd6a4d548c4; solo se leyo) con: la
letra T-R (nueva, mas estricta), SEMILLAS NUEVAS (49001-50600, sin 50000; busca_semillas_v144b.py), el arnes esperado y las
PREDICCIONES de TERMO' (escritas ANTES del arnes y del humo). La letra T-A..T-G y T-H: la de v14.4 sin tocar. Generado POR ANCLAS por
experimentos/tronco_v14_4b_examen/construye_v144b.py. NO editar a mano. Lo que sigue es el docstring del origen (renombrado)."""
'''
SEM_144 = '''_r = lambda a, b: list(range(a, b + 1))
SEMILLAS = {
    'serie': dict(EX=_r(47001, 47020), VIVO=_r(47101, 47180),
                  TD_rango=(47501, 48000),
                  ALIAS=[47518, 47575, 47597, 47608, 47621, 47686, 47713, 47714, 47725],
                  LIMPIAS=[47501, 47508, 47516, 47521, 47530, 47554, 47556, 47559, 47568]),
    'replica': dict(EX=_r(47021, 47040), VIVO=_r(47201, 47280),
                    TD_rango=(48001, 48500),
                    ALIAS=[48011, 48031, 48070, 48071, 48074, 48094, 48101, 48116, 48117],
                    LIMPIAS=[48009, 48012, 48017, 48020, 48028, 48029, 48030, 48043, 48051]),
    # RESERVA: SOLO si TRONCO_B no pasa (serie del mundo vivo que "no se lee", letra v4 4'): T-A + T-C (ii) + T-F vivo + T-G
    'reserva': dict(VIVO=_r(47301, 47380)),
    'humo': [47041, 47042, 47043],   # + la ALIAS historica 326 (ya publica) para el camino de B-5 en el humo
    'identidad': [47045, 47046, 47047],
}
'''
SEM_144B = '''# v14.4b: SEMILLAS NUEVAS (busca_semillas_v144b.py, 28-sep-2026, repo entero: los numeros 49001-49999, 50001-50600 y 149001-149999 no
# aparecen en ningun .py/.md, ni en contexto de semilla, ni en nombres de archivo; en los datos solo como pasos de tiempo). 50000 (T/2
# de medio repo) se excluye. T-D: la seleccion ESTRUCTURAL (diagnostico_codigos.solapamientos, sin simular) sobre sus rangos; el runner
# la recalcula y se para si no coincide. TRONCO_B = s + 100000 -> 149101-149380.
_r = lambda a, b: list(range(a, b + 1))
SEMILLAS = {
    'serie': dict(EX=_r(49001, 49020), VIVO=_r(49101, 49180),
                  TD_rango=(49401, 49999),
                  ALIAS=[49449, 49492, 49509, 49528, 49563, 49597, 49621, 49652, 49718],
                  LIMPIAS=[49407, 49418, 49431, 49444, 49450, 49451, 49457, 49464, 49466]),
    'replica': dict(EX=_r(49021, 49040), VIVO=_r(49201, 49280),
                    TD_rango=(50001, 50600),
                    ALIAS=[50004, 50054, 50181, 50208, 50212, 50235, 50250, 50294, 50296],
                    LIMPIAS=[50001, 50005, 50008, 50011, 50019, 50020, 50030, 50031, 50040]),
    # RESERVA: SOLO si TRONCO_B no pasa (serie del mundo vivo que "no se lee", letra v4 4'): T-A + T-C (ii) + T-F vivo + T-G + T-R
    'reserva': dict(VIVO=_r(49301, 49380)),
    'humo': [49041, 49042, 49043],   # + la ALIAS historica 326 (ya publica) para el camino de B-5 en el humo
    'identidad': [49045, 49046, 49047],
}
'''
TR_UMB = '''NUM = dict(U143.NUM)
# ---------------------------------------------------------------- v14.4b: T-R, la reversion con la pieza ACTUANDO (mas estricta; no reemplaza nada)
LETRA['T-R'] = ("v14.4b: T-C (ii) pasa por la letra v4 (NI en rev, margen 12.5) Y la pieza ACTUA (a_no + a_si > 0) en >= 95 % de las "
                "80 corridas CAND de T-C (ii) (G-3 analogo): una reversion aprobada con la pieza muda no cuenta")
TR = dict(actua_frac=0.95, n=80)
'''
PRED_144_INI = "# ---------------------------------------------------------------- predicciones firmadas (PREREGISTRO sec. 5), ANTES del humo\n"
PRED_144B = '''# ---------------------------------------------------------------- predicciones firmadas de TERMO' (PREREGISTRO_examen_v144b sec. 5)
# Escritas el 28-sep-2026 ANTES del arnes y del humo de v14.4b, desde el mecanismo y los crudos de la SERIE de TERMO (47101-47180, que ya
# existian): (2) hace a v14.4b y v14.4bg la FISICA de v14.3 -> T-B, T-E, T-C (i) y T-F examen son el tronco contra si mismo. Sin
# inversion (T-A, T-D, T-G) la tabla que olvida da las mismas decisiones que TERMO -> se esperan los numeros de TERMO. En T-C (ii) la
# tabla deja de gobernar A a la primera mordida mala, PERO la pieza pasa a gobernar B (la comida nueva) y lo come ~25 % menos (TERMO,
# antes de invertir: A 152 contra 204 del OFF por cuarto, y B-veneno 119 contra 156); rev = mordB_Q4 - mordA_Q4 es una DIFERENCIA DE
# CONTEOS: si todo baja ~25 %, rev baja de ~44 a ~33 y d ~ -11 contra el margen -12.5 (LI ~ -15). Por eso T-C (ii) y T-R son las
# puertas en riesgo aun con la tabla que olvida (trampa 3: el mundo que se come la comida).
PRED = {
    'legible': dict(p=0.97, frase="TRONCO_B pasa T-A, T-C (ii) y T-F vivo (las tareas calibradas; en TERMO y en v14.3 pasaron)"),
    'T-A': dict(p=0.95, frase="como TERMO: r VIVO CAND mediana en [-45, -20] (OFF ~ -75), CUELLO_MIN en [0, +15] (OFF ~ -6); muertes 0.6-0.95 x"),
    'T-B': dict(p=0.95, frase="CAND == TRONCO en la fisica (40/40 identicas): G1 1.000, G2 >= 0.95, azar G2 = el del tronco en [0.31, 0.60]"),
    'T-C': dict(p=0.33, frase="(i) == tronco (p 0.97); (ii) rev CAND mediana en [15, 40] (OFF ~ 44), d media en [-20, -3]: LI > -12.5 con p 0.35"),
    'T-D': dict(p=0.95, frase="como TERMO: C1, C2, C6 pasan (la sal muda tiene s nula; la pieza no gobierna B ni D)"),
    'T-E': dict(p=0.97, frase="CAND == TRONCO en la fisica (120/120 identicas): cada escenario 20/20 salvo las clausulas absolutas del tronco"),
    'T-F': dict(p=0.90, frase="examen: razon 1.0 (identico); vivo: muertes T-C (ii) 0.9-1.1 x, T-A <= 1.0 x (como TERMO)"),
    'T-G': dict(p=0.90, frase="como TERMO: G-1 d media en [+8, +22] (LI > 1 con p 0.92), G-2 TERMOINV no gana (p 0.98), G-3 80/80"),
    'T-R': dict(p=0.34, frase="la pieza actua en T-C (ii) en 80/80 (gobierna A antes de invertir y B despues): T-R ~ T-C (ii)"),
    'serie': dict(p=0.25, frase="producto (T-C ii y T-R casi la misma apuesta) ~ 0.25; P(serie y replica) ~ 0.15: VEREDICTO previsto NO PASA (p ~ 0.85), por T-C (ii) y T-R"),
}
'''


def umbrales(t):
    t = renombra(t, [("v14.4 = v14.3 + TERMO", "v14.4b = v14.3 + TERMO′", 1), ('v144', 'v144b', 3)], 'umbrales')
    t = sust(t, "NUM = dict(U143.NUM)\n", TR_UMB, etq='umbrales: T-R')
    t = sust(t, SEM_144, SEM_144B, etq='umbrales: SEMILLAS')
    t = sust(t, "ARNES_ESPERADO = 'RESULTADO: 126/126'   # (0) 6 (A) 21 (A') 5 (P) 10 (L) 5 (X) 2 (D) 7 (R) 41 (J) 10 (K) 19; primera corrida limpia\n",
             "ARNES_ESPERADO = 'RESULTADO: 151/151'   # v14.4b identidad_v144bex.py: (0) 10 (A) 15 (I) 16 (T) 12 (V) 4 (P) 9 (L) 3 (D) 6 (R) 44 (J) 16 (K) 16\n", etq='umbrales: arnes')
    i = t.index(PRED_144_INI)
    if t.count(PRED_144_INI) != 1 or not t.rstrip().endswith('}'):
        raise SystemExit('*** umbrales: el bloque PRED no es el esperado. No se escribe nada.')
    return DOC_UMB + t[:i] + PRED_144B


# ================================================================ busca_semillas
def busca(t):
    t = renombra(t, [('RANGOS = [(47000, 48600), (147000, 148600)]', 'RANGOS = [(49000, 50600), (149000, 150600)]', 1),
                     ("if 'tronco_v14_4_examen' in rel:", "if 'tronco_v14_4b_examen' in rel:", 1),
                     ('(rangos 47000-48600 y 147000-148600)', '(rangos 49000-50600 y 149000-150600)', 1), ('v144', 'v144b', 3),
                     ('experimentos/tronco_v14_4_examen/', 'experimentos/tronco_v14_4b_examen/', 1)], 'busca')
    return ('"""busca_semillas_v144b = experimentos/tronco_v14_4_examen/busca_semillas_v144.py (e3220d8311115207) con los rangos de v14.4b.\n'
            'Generado POR ANCLAS por construye_v144b.py. NO editar a mano. Lo que sigue es el docstring del origen."""\n' + t)


# ================================================================ el CARRO de la pista (para el muro): V143_TERMO -> V143_TERMOB
def carro(t):
    if t.count('\n') != t.count('\r\n'):   # el origen es CRLF entero (como lo escribio construye_termo): se conserva byte a byte
        raise SystemExit('*** carro: finales de linea mezclados. No se escribe nada.')
    t = t.replace('\r\n', '\n')
    t = sust(t, '"""V143_TERMO.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.\n',
             '"""V143_TERMOB.py — termo\': V143_TERMO (organelos/termo/carros, 3db639cab75641fb; solo se leyo) con la tabla de la pieza que\n'
             'OLVIDA: la pieza ya no lee _adS de APR (suma sin olvido) sino una tabla PROPIA _tmS[letra] = [ultimo dE, ultimo dAg, 1] (el ULTIMO\n'
             'dS nominal sentido por el linaje), actualizada donde APR actualiza _adS (resultado, al morder). _adS (de APR) NO se toca. Memoria\n'
             'nueva: 2 numeros por letra (TERMO: cero). TERMO = 2 da TERMOINV con la misma tabla. GENERADO POR ANCLAS por\n'
             'experimentos/tronco_v14_4b_examen/construye_v144b.py. NO editar a mano. Arnes: identidad_termob.py (== V143_TERMO en la fisica\n'
             'de la pista mientras el dS por letra sea fijo). Lo que sigue es el docstring del origen.\n\n'
             'V143_TERMO.py — termo: V143 + UNA pieza de boca (termostato de dos necesidades; ver construye_termo.py). Cero memoria nueva.\n',
             etq='carro: docstring')
    t = sust(t, "        self._tm = dict(dec=0, a_no=0, a_si=0, mord=0)\n",
             "        self._tm = dict(dec=0, a_no=0, a_si=0, mord=0)\n"
             "        self._tmS = {}   # termo': letra -> [ultimo dE sentido, ultimo dAg sentido, 1] (del LINAJE; tabla PROPIA de la pieza, OLVIDA)\n",
             etq='carro: tabla propia')
    t = sust(t, "    def _tm_boca(self, kk, E, Ag, mf):\n        m = self._adS.get(kk)\n",
             "    def _tm_boca(self, kk, E, Ag, mf):\n        m = self._tmS.get(kk)   # termo': lee SU tabla (el ultimo dS), no la suma de APR\n",
             etq='carro: la pieza lee su tabla')
    t = sust(t, "        if OPCION and res['mordio']: self._apr_dS(res['letra'], res['dS'])\n",
             "        if OPCION and res['mordio']: self._apr_dS(res['letra'], res['dS'])\n"
             "        if TERMO and res['mordio']: self._tmS[res['letra']] = [float(res['dS'][0]), float(res['dS'][1]), 1]   # termo': el ULTIMO dS nominal\n",
             etq='carro: actualiza donde APR')
    return t.replace('\n', '\r\n')


def construye():
    """Devuelve {nombre: texto}. No escribe. Antes, TODOS los origenes con su sha (tripwire)."""
    for ruta in ORIGENES:
        origen(ruta)
    out = {}
    o = lambda n: origen(os.path.join(V144EX, n))
    out['organismo_v144b.py'] = organismo(o('organismo_v144.py'), CAB_144B, True, 'v144b')
    out['organismo_v144bg.py'] = organismo(o('organismo_v144g.py'), CAB_144BG, True, 'v144bg')
    out['organismo_v144bcal.py'] = organismo(o('organismo_v144cal.py'), CAB_144BCAL, False, 'v144bcal')
    b = renombra(o('bateria_v144.py'), [("v14.4 = v14.3 + TERMO", "v14.4b = v14.3 + TERMO′", 3), ('v144', 'v144b', 12),
                                         ('experimentos/tronco_v14_4_examen/', 'experimentos/tronco_v14_4b_examen/', 1)], 'bateria')
    out['bateria_v144b.py'] = CAB_BAT + b
    g = renombra(o('bateria_generaliza_v144.py'), [("v14.4 = v14.3 + TERMO", "v14.4b = v14.3 + TERMO′", 1), ('v144', 'v144b', 11),
                                                    ('experimentos/tronco_v14_4_examen/', 'experimentos/tronco_v14_4b_examen/', 1)], 'generaliza')
    out['bateria_generaliza_v144b.py'] = CAB_GEN + g
    out['corre_examen_v144b.py'] = runner(o('corre_examen_v144.py'))
    out['umbrales_examen_v144b.py'] = umbrales(o('umbrales_examen_v144.py'))
    out['busca_semillas_v144b.py'] = busca(o('busca_semillas_v144.py'))
    out['carros/V143_TERMOB.py'] = carro(origen(os.path.join(TERMO, 'carros', 'V143_TERMO.py')))
    return out


def main(argv):
    VERIFICA = '--verifica' in argv
    extra = [a for a in argv if a != '--verifica']
    if extra:
        raise SystemExit(f'*** banderas desconocidas: {extra} (ERR-115). Uso: construye_v144b.py [--verifica]')
    T = construye()
    malo = 0
    for n, t in T.items():
        p = os.path.join(AQUI, n)
        if VERIFICA:
            en_disco = open(p, 'rb').read().decode('utf-8') if os.path.exists(p) else None
            ok = en_disco == t
            malo += not ok
            print(f"{'OK  ' if ok else 'DIFIERE'} {n:30s} construccion {h16t(t)}  disco {h16(p) if os.path.exists(p) else '(falta)'}")
        else:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write(t)
            print(f'escrito {n:30s} {h16(p)}')
    print('origenes: ' + '  '.join(f'{os.path.basename(k)} {v}' for k, v in ORIGENES.items()))
    if VERIFICA:
        print(f"VERIFICA: {'todo en disco == construccion' if not malo else f'*** {malo} archivo(s) distintos'}")
    return 1 if (VERIFICA and malo) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
