"""construye_g50.py — construye POR ANCLAS los tres archivos de 50 GENES (Opus G, 28-sep-2026, EXPLORATORIO).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como. Principio del director: que la evolucion construya el organo, no nosotros.

Encargo: "el mismo experimento (ECO con hijos ingenuos, eco_sel_ing) pero con 50 genes". Hoy mutan 15 (ING_SEL_C). Aqui 32 constantes
LITERALES que el cuerpo usa de verdad en el gemelo (frio/motor_frio_rapido.py) pasan a ser POR CUERPO y salen del genoma:
  marcha (14): gan_patron 1.2 · gan_lado 1.5 · gan_aqui 1.0 · ruido0 .15 · ruido_h .5 · umbral_m0 .8 · umbral_m1 .8 · ruido_motor .3 ·
               umbral_mov .5 · traza .7 · premio_acerca .2 · clip_l 1.5 · h_motor 2 (el 2 de 1 + 2*hambre) · x_eta_l 1 (MULTIPLICA a eta en el motor)
  arranque (3): wl0_lo .1 · wl0_hi .4 (Wl ~ U(.1,.4)) · kw0_hi 1.0 (KW ~ U(0,1))
  boca (5):    sesgo_boca .5 · temp_boca .3 · umbral_fam .2 · puerta_pat 5 (entero) · pat_min 1 (entero, <= K = 3)
  valor por necesidad (5): R_bueno_E 1 · R_bueno_A 1 · R_malo_E 3 · R_malo_A 3 (la R de la mordida; hoy +1 / -3 para las dos) · peso_sed 1
  aprendizaje (2): clip_e 3.0 (tope de Wp/Wn) · x_aversion_s 1 (MULTIPLICA a aversion en la via sensorial Wns)
  division (3): decae_kw .05 · clip_kw 5.0 · umbral_div .2
EXCLUIDOS (declarado): costo, costo_a y el tope de reserva 1.5 (bajarlos sube K sin cerebro: almuerzo gratis, trampa 3); el alcance de
la vista (ver no cuesta nada: solo podria bajar); K = 3, NKMAX, n_nec (dimensiones compiladas); olvido y reposicion (son del mundo).
Split y pesos por necesidad (justificados): x_eta_l, x_aversion_s (MULTIPLICADORES: con 1.0 la cuenta es la
original aunque eta o aversion muten), umbral_m0/m1 y R por necesidad separan una constante que HOY se usa en
dos organos o dos necesidades; en G0 valen lo mismo que la original (identidad bit a bit con p_mut = 0).

Archivos (cada ancla exacta con su cuenta):
  motor_eco50.py  <- experimentos/juaco_eco/motor_eco.py (bca3033878b59622): GENES 18 -> 50 (destino 'g50'); genoma0 lee G50_0; ctx_genoma
                     ignora 'g50'; muta gasta 2*18 numeros si NINGUN gen nuevo es mutable (asi ING_SEL_C / ING_AZA_C == la base BIT A BIT)
                     y 2*50 si alguno lo es; AQUI apunta a juaco_eco (carros).
  motor_g50.py    <- experimentos/organelos/frio/motor_frio_rapido.py (ff9d890a5cce9dec): 30 reales nuevos en bf, 2 enteros en bi; los
                     literales del tramo, _crea, _nace y _fam leen la ranura; importa motor_eco50; firma propia.
  nucleo_g50.py   <- experimentos/organelos/eco_sel_ing/nucleo_eco_sel_ing.py (c2189f9d22b72386): usa motor_g50; brazos ING_SEL_50,
                     ING_AZA_50, ING_SEL_25, ING_SEL_47; semillas 488xx.
Uso: python construye_g50.py            # escribe los tres
     python construye_g50.py --verifica # los de disco == los construidos (y los origenes con su sha)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))   # .../experimentos
ORI = {'motor_eco50.py': (os.path.join(EXP, 'juaco_eco', 'motor_eco.py'), 'bca3033878b59622'),
       'motor_g50.py': (os.path.join(EXP, 'organelos', 'frio', 'motor_frio_rapido.py'), 'ff9d890a5cce9dec'),
       'nucleo_g50.py': (os.path.join(EXP, 'organelos', 'eco_sel_ing', 'nucleo_eco_sel_ing.py'), 'c2189f9d22b72386')}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


# (nombre, G0, entero, piso, techo) en el ORDEN de bf (30 reales) y luego los 2 enteros. Rango efectivo (motor_eco.rangos) =
# [max(piso, G0/4), min(techo, 4*G0)].
G50 = (('gan_patron', 1.2, 0, 0.01, 20.0), ('gan_lado', 1.5, 0, 0.01, 20.0), ('gan_aqui', 1.0, 0, 0.01, 20.0),
       ('ruido0', 0.15, 0, 1e-3, 5.0), ('ruido_h', 0.5, 0, 1e-3, 5.0), ('umbral_m0', 0.8, 0, 0.01, 5.0), ('umbral_m1', 0.8, 0, 0.01, 5.0),
       ('ruido_motor', 0.3, 0, 1e-3, 5.0), ('umbral_mov', 0.5, 0, 0.01, 2.0), ('traza', 0.7, 0, 0.05, 0.99),
       ('premio_acerca', 0.2, 0, 1e-3, 5.0), ('clip_l', 1.5, 0, 0.1, 20.0), ('h_motor', 2.0, 0, 1e-3, 20.0), ('x_eta_l', 1.0, 0, 0.05, 20.0),
       ('wl0_lo', 0.1, 0, 1e-3, 2.0), ('wl0_hi', 0.4, 0, 1e-3, 2.0), ('kw0_hi', 1.0, 0, 0.05, 4.0),
       ('sesgo_boca', 0.5, 0, 0.01, 5.0), ('temp_boca', 0.3, 0, 0.01, 5.0), ('umbral_fam', 0.2, 0, 0.01, 5.0),
       ('R_bueno_E', 1.0, 0, 0.05, 20.0), ('R_bueno_A', 1.0, 0, 0.05, 20.0), ('R_malo_E', 3.0, 0, 0.05, 20.0), ('R_malo_A', 3.0, 0, 0.05, 20.0),
       ('peso_sed', 1.0, 0, 0.05, 20.0), ('clip_e', 3.0, 0, 0.1, 50.0), ('x_aversion_s', 1.0, 0, 0.05, 20.0),
       ('decae_kw', 0.05, 0, 1e-3, 0.5), ('clip_kw', 5.0, 0, 0.1, 50.0), ('umbral_div', 0.2, 0, 0.01, 5.0),
       ('puerta_pat', 5.0, 1, 2, 20), ('pat_min', 1.0, 1, 1, 3))

# ------------------------------------------------------------------------------------------------ motor_eco50.py
E1 = ('"""motor_eco.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco.py desde experimentos/generaciones/motor_convive.py,\n',
      '"""motor_eco50.py (CONSTRUIDO por experimentos/organelos/bloques/opusG/construye_g50.py desde experimentos/juaco_eco/motor_eco.py,\n'
      'sha bca3033878b59622; NO editar a mano). 50 GENES: GENES 18 -> 50 (32 constantes del cuerpo, destino \'g50\'; solo las lee el gemelo\n'
      'motor_g50.py); muta gasta 2*18 numeros si ningun gen nuevo es mutable. Lo que sigue es el docstring del origen.\n\n'
      'motor_eco.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco.py desde experimentos/generaciones/motor_convive.py,\n', 1)
E2 = ('AQUI = os.path.dirname(os.path.abspath(__file__))\nif AQUI not in sys.path: sys.path.insert(0, AQUI)\n',
      'G50DIR = os.path.dirname(os.path.abspath(__file__))   # G50: este archivo vive en experimentos/organelos/bloques/opusG\n'
      'AQUI = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(G50DIR))), \'juaco_eco\')   # G50: carros y pista de juaco_eco\n'
      'if AQUI not in sys.path: sys.path.insert(0, AQUI)\n', 1)
E3 = ('NOMBRES = tuple(g[0] for g in GENES)\n',
      '# G50: las 32 constantes nuevas (nombre, G0, entero, piso, techo); orden = el de bf en motor_g50 (30 reales) y luego 2 enteros\n'
      'G50 = ' + repr(G50) + '\n'
      'N18 = len(GENES)   # G50: 18\n'
      'G50_0 = {n_: float(v_) for n_, v_, e_, lo_, hi_ in G50}\n'
      'NOMBRES50 = tuple(n_ for n_, v_, e_, lo_, hi_ in G50)\n'
      'GENES = GENES + tuple((n_, \'g50\', e_, lo_, hi_) for n_, v_, e_, lo_, hi_ in G50)\n'
      'NOMBRES = tuple(g[0] for g in GENES)\n', 1)
E4 = ("        v.append(float(CF['NK'] if dest == 'NK' else kw[nom]))\n",
      "        v.append(float(G50_0[nom] if dest == 'g50' else (CF['NK'] if dest == 'NK' else kw[nom])))   # G50\n", 1)
E5 = ("        else: d[dest] = v; kw[dest] = v\n",
      "        elif dest == 'g50': pass   # G50: el carro Python no las lee (solo el gemelo motor_g50)\n"
      "        else: d[dest] = v; kw[dest] = v\n", 1)
E6 = ("    NG = len(g); u = r.random(NG); z = r.normal(0.0, sigma, NG); h = g.copy(); nm = 0\n    for j in range(NG):\n",
      "    NG = len(g); NU = NG if (NG > N18 and bool(np.any(np.asarray(p)[N18:] > 0))) else min(NG, N18)   # G50: 2*18 si ningun nuevo muta\n"
      "    u = r.random(NU); z = r.normal(0.0, sigma, NU); h = g.copy(); nm = 0\n    for j in range(NU):\n", 1)
ANCLAS_E = [('E1', *E1), ('E2', *E2), ('E3', *E3), ('E4', *E4), ('E5', *E5), ('E6', *E6)]

# ------------------------------------------------------------------------------------------------ motor_g50.py
FN = ('F_GP, F_GL, F_GA, F_R0, F_RH, F_UM0, F_UM1, F_RM, F_UMOV, F_TRZ, F_PAC, F_CLL, F_HM, F_ETAL, F_WL0, F_WL1, F_KW0, F_SB, F_TB, '
      'F_UF, F_RBE, F_RBA, F_RME, F_RMA, F_PS, F_CLE, F_AVS, F_DKW, F_CKW, F_UD')
M = []
M.append(('M1', '"""motor_frio_rapido.py (CONSTRUIDO por experimentos/organelos/frio/construye_frio.py desde juaco_eco/motor_eco_rapido_fam.py,\n',
          '"""motor_g50.py (CONSTRUIDO por experimentos/organelos/bloques/opusG/construye_g50.py desde experimentos/organelos/frio/\n'
          'motor_frio_rapido.py, sha ff9d890a5cce9dec; NO editar a mano). 50 GENES: 32 constantes literales del cuerpo (marcha, arranque,\n'
          'boca, valor por necesidad, aprendizaje, division) pasan a ser POR CUERPO desde el genoma (motor_eco50.GENES). Con el genoma en G0\n'
          'es el origen bit a bit (arnes identidad_g50.py). El cerebro FAMB (_nace_fam) NO se adapto (aversion_s no llega alli): solo FABRICA_ECO.\n'
          'Lo que sigue es el docstring del origen.\n\n'
          'motor_frio_rapido.py (CONSTRUIDO por experimentos/organelos/frio/construye_frio.py desde juaco_eco/motor_eco_rapido_fam.py,\n', 1))
M.append(('M2', "FRIO = os.path.dirname(os.path.abspath(__file__))   # F1 FRIO: este archivo vive en experimentos/organelos/frio\n",
          "G50DIR = os.path.dirname(os.path.abspath(__file__))   # G50: este archivo vive en experimentos/organelos/bloques/opusG\n"
          "FRIO = os.path.join(os.path.dirname(os.path.dirname(G50DIR)), 'frio')   # G50: la carpeta del origen (carros/BAR0_ECO.py)\n", 1))
M.append(('M3', "import motor_eco as ME    # el ORIGINAL (solo se LEE: guardias, _eco_cfg, muta, ctx_genoma, GENES)\n",
          "if G50DIR not in sys.path: sys.path.insert(0, G50DIR)   # G50\n"
          "import motor_eco50 as ME    # G50: la copia de 50 genes (guardias, _eco_cfg, muta, ctx_genoma, GENES)\n", 1))
M.append(('M4', "FIRMA_GEMELO = 'motor_frio_rapido v1'\n", "FIRMA_GEMELO = 'motor_g50 v1'\n", 1))
M.append(('M5', "NBI = 33   # I_SO0..I_SO0+3 = sin_objetivo\n",
          "(I_PP, I_PM) = (33, 34)   # G50: puerta_pat y pat_min por cuerpo\nNBI = 35   # I_SO0..I_SO0+3 = sin_objetivo\n", 1))
M.append(('M6', "NBF = 22\n", f"({FN}) = range(22, 52)   # G50: las 30 reales nuevas (orden de motor_eco50.G50)\nNBF = 52\n", 1))
M.append(('M7', "    bf[s, F_DOTE] = g[GI[15]]; bf[s, F_RU] = g[GI[16]]; bf[s, F_RX] = g[GI[17]]\n",
          "    bf[s, F_DOTE] = g[GI[15]]; bf[s, F_RU] = g[GI[16]]; bf[s, F_RX] = g[GI[17]]\n"
          "    for m_ in range(30): bf[s, 22 + m_] = g[GI[18 + m_]]   # G50\n"
          "    bi[s, I_PP] = int(np.rint(g[GI[48]])); bi[s, I_PM] = int(np.rint(g[GI[49]]))   # G50\n", 1))
M.append(('M8', "    bi[s, I_MR] = C0i[0]; bi[s, I_NK] = C0i[1]\n",
          "    bi[s, I_MR] = C0i[0]; bi[s, I_NK] = C0i[1]; bi[s, I_PP] = C0i[2]; bi[s, I_PM] = C0i[3]   # G50\n", 1))
M.append(('M9', "def _fam(Wp, Wn, s, n, c3, key, nck, ncc, bi, ppat, pmin):\n", "def _fam(Wp, Wn, s, n, c3, key, nck, ncc, bi, ppat, pmin, uf):   # G50: + uf\n", 1))
M.append(('M10', "        if abs(Wp[s, n, i] - Wn[s, n, i]) > 0.2: c += 1\n", "        if abs(Wp[s, n, i] - Wn[s, n, i]) > uf: c += 1   # G50: umbral_fam\n", 1))
# _crea / _nace: el arranque de Wl y KW
M.append(('M11', "    u = r.uniform(.1, .4, (2, 9))\n", "    u = r.uniform(bf[s, F_WL0], bf[s, F_WL1], (2, 9))   # G50\n", 1))
M.append(('M12', "    u2 = r.uniform(0, 1, (NK, 6))\n", "    u2 = r.uniform(0, bf[s, F_KW0], (NK, 6))   # G50\n", 1))
M.append(('M13', "        u2 = r.uniform(0, 1, (NK - 0, 6))\n", "        u2 = r.uniform(0, bf[s, F_KW0], (NK - 0, 6))   # G50\n", 1))
M.append(('M14', "def _nace(s, rh, bi, Wl, el, tr, KW, act, ccode, cval, PATM, wbuf, mdot, wi):\n",
          "def _nace(s, rh, bi, Wl, el, tr, KW, act, ccode, cval, PATM, wbuf, mdot, wi, bf):   # G50: + bf\n", 1))
M.append(('M15', "    u = rh.uniform(.1, .4, (2, 9))\n", "    u = rh.uniform(bf[s, F_WL0], bf[s, F_WL1], (2, 9))   # G50\n", 1))
M.append(('M16', "    u2 = rh.uniform(0, 1, (NK, 6))\n", "    u2 = rh.uniform(0, bf[s, F_KW0], (NK, 6))   # G50\n", 1))
M.append(('M17', "        u2 = rh.uniform(0, 1, (NK - 0, 6))\n", "        u2 = rh.uniform(0, bf[s, F_KW0], (NK - 0, 6))   # G50\n", 1))
M.append(('M18', "    _nace(s3, ghi, bi, Wl, el, tr, KW, act, ccode, cval, PATM, wbuf, mdot, wi)\n",
          "    _nace(s3, ghi, bi, Wl, el, tr, KW, act, ccode, cval, PATM, wbuf, mdot, wi, bf)   # G50\n", 2))
M.append(('M19', "    _nace(0, r_hijo, st['bi'], st['Wl'], st['el'], st['tr'], st['KW'], st['act'], st['ccode'], st['cval'], PATM, wbuf, mdot, wi)\n",
          "    _nace(0, r_hijo, st['bi'], st['Wl'], st['el'], st['tr'], st['KW'], st['act'], st['ccode'], st['cval'], PATM, wbuf, mdot, wi, st['bf'])   # G50\n", 1))
# el R de la mordida por necesidad
M.append(('M20', "# ================================================================ EL TRAMO: pasos [t0, t1)\n",
          "@njit(cache=True)\n"
          "def _rv(rv, n, s, bf):\n"
          "    \"\"\"G50: la R de la mordida (hoy RV = +1 / -3 / 0) con el peso por necesidad del cuerpo (R_bueno_E/A, R_malo_E/A).\"\"\"\n"
          "    if rv > 0: return bf[s, F_RBE + n]\n"
          "    if rv < 0: return -bf[s, F_RME + n]\n"
          "    return 0.0\n\n\n"
          "# ================================================================ EL TRAMO: pasos [t0, t1)\n", 1))
# _tramo, fase A
M.append(('M21', "            na = 1 if dfa > hambre else 0\n", "            na = 1 if bf[s, F_PS] * dfa > hambre else 0   # G50: peso_sed\n", 1))
M.append(('M22', "            for j in range(6): x9[j] = PATM[k, j] * 1.2\n"
                 "            x9[6] = 1.5 if left else 0.0; x9[7] = 0.0 if left else 1.5; x9[8] = 1.0 if d == 0 else 0.0\n"
                 "            noise = .15 + .5 * hambre\n",
          "            for j in range(6): x9[j] = PATM[k, j] * bf[s, F_GP]   # G50\n"
          "            x9[6] = bf[s, F_GL] if left else 0.0; x9[7] = 0.0 if left else bf[s, F_GL]; x9[8] = bf[s, F_GA] if d == 0 else 0.0\n"
          "            noise = bf[s, F_R0] + bf[s, F_RH] * hambre\n", 1))
M.append(('M23', "            e0, e1 = _exp2(-(V[0] - .8) / noise, -(V[1] - .8) / noise, lp, xin, xout, dims, adr, mexp)\n",
          "            e0, e1 = _exp2(-(V[0] - bf[s, F_UM0]) / noise, -(V[1] - bf[s, F_UM1]) / noise, lp, xin, xout, dims, adr, mexp)   # G50\n", 1))
M.append(('M24', "            z = r.normal(0, .3, 2)\n", "            z = r.normal(0, bf[s, F_RM], 2)   # G50\n", 1))
M.append(('M25', "            if umax > .5:\n", "            if umax > bf[s, F_UMOV]:   # G50\n", 1))
M.append(('M26', "            for j in range(9): tr[s, j] = tr[s, j] * .7 + x9[j]\n", "            for j in range(9): tr[s, j] = tr[s, j] * bf[s, F_TRZ] + x9[j]   # G50\n", 1))
M.append(('M27', "            Rp = .2 if d2 < d else 0.\n", "            Rp = bf[s, F_PAC] if d2 < d else 0.   # G50\n", 1))
M.append(('M28', "                fa9 = _fam(Wp, Wn, s, nm, c3, key, nck, ncc, bi, ppat, pmin)\n",
          "                fa9 = _fam(Wp, Wn, s, nm, c3, key, nck, ncc, bi, bi[s, I_PP], bi[s, I_PM], bf[s, F_UF])   # G50\n", 1))
M.append(('M29', "                    v2 = f2 if _fam(Wp, Wn, s, o, c3, key, nck, ncc, bi, ppat, pmin) else sv2\n",
          "                    v2 = f2 if _fam(Wp, Wn, s, o, c3, key, nck, ncc, bi, bi[s, I_PP], bi[s, I_PM], bf[s, F_UF]) else sv2   # G50\n", 1))
M.append(('M30', "                Vb = bf[s, F_ALPHA] * wt + bf[s, F_HB] * hambre + .5\n"
                 "                pb = 1 / (1 + _exp1(-Vb / .3, lp, xin, xout, dims, adr, mexp))\n",
          "                Vb = bf[s, F_ALPHA] * wt + bf[s, F_HB] * hambre + bf[s, F_SB]   # G50\n"
          "                pb = 1 / (1 + _exp1(-Vb / bf[s, F_TB], lp, xin, xout, dims, adr, mexp))\n", 1))
M.append(('M31', "                    R = RV[kk, na]; bf[s, F_R] = R\n", "                    R = _rv(RV[kk, na], na, s, bf); bf[s, F_R] = R   # G50\n", 1))
M.append(('M32', "                    EMA = bf[s, F_EMA]; EMAC = bf[s, F_EMAC]; PASO = bf[s, F_PASO]; DELS = bf[s, F_DELS]; DELC = bf[s, F_DELC]\n",
          "                    EMA = bf[s, F_EMA]; EMAC = bf[s, F_EMAC]; PASO = bf[s, F_PASO]; DELS = bf[s, F_DELS]; DELC = bf[s, F_DELC]\n"
          "                    CLE = bf[s, F_CLE]; AVS = AV * bf[s, F_AVS]; DKW = bf[s, F_DKW]; CKW = bf[s, F_CKW]; UD = bf[s, F_UD]   # G50\n", 1))
M.append(('M33', "                        cc = ETAS * AV * (-ds)\n", "                        cc = ETAS * AVS * (-ds)   # G50\n", 1))
M.append(('M34', "                            cc = ETAS * AV * (-dsn)\n", "                            cc = ETAS * AVS * (-dsn)   # G50\n", 1))
M.append(('M35', ") > 3.0: trunca = True\n", ") > CLE: trunca = True   # G50\n", 2))
M.append(('M36', " + cc * 1.0, 0.0, 3.0)\n", " + cc * 1.0, 0.0, CLE)   # G50\n", 4))
M.append(('M37', "                        Rn = RV[kk, n]\n", "                        Rn = _rv(RV[kk, n], n, s, bf)   # G50\n", 1))
M.append(('M38', "                            kj[j] = _clip(KW[s, c, j] * (1 - 0.05) + PASO * dist[j], 0.0, 5.0) * (1.0 if rel[j] else 0.0)\n",
          "                            kj[j] = _clip(KW[s, c, j] * (1 - DKW) + PASO * dist[j], 0.0, CKW) * (1.0 if rel[j] else 0.0)   # G50\n", 1))
M.append(('M39', "                        if wbc * R < 0 and abs(wbc) > 0.2:\n", "                        if wbc * R < 0 and abs(wbc) > UD:   # G50\n", 1))
# fase B: el aprendizaje del motor
M.append(('M40', "            sc = bf[s, F_ETA] * (1 + 2 * bf[s, F_HAMB]) * (mxr + bf[s, F_RP])\n",
          "            sc = (bf[s, F_ETA] * bf[s, F_ETAL]) * (1 + bf[s, F_HM] * bf[s, F_HAMB]) * (mxr + bf[s, F_RP])   # G50\n", 1))
M.append(('M41', "                    for b in range(9): Wl[s, a, b] = _clip(Wl[s, a, b] + sc * el[s, a, b], 0.0, 1.5)\n",
          "                    for b in range(9): Wl[s, a, b] = _clip(Wl[s, a, b] + sc * el[s, a, b], 0.0, bf[s, F_CLL])   # G50\n", 1))
# run_solapadas: GI de 50, enteros, C0f / C0i
M.append(('M42', "                                                  'dote', 'rep_umbral', 'rep_X')], np.int64)\n"
                 "    if [ME.NOMBRES[j] for j in range(len(ME.GENES)) if ME.GENES[j][2]] != ['memoria_rechazo', 'NK', 'rep_X']:\n",
          "                                                  'dote', 'rep_umbral', 'rep_X') + ME.NOMBRES50], np.int64)   # G50: + 32\n"
          "    if [ME.NOMBRES[j] for j in range(len(ME.GENES)) if ME.GENES[j][2]] != ['memoria_rechazo', 'NK', 'rep_X', 'puerta_pat', 'pat_min']:\n", 1))
M.append(('M43', "    C0i = np.array([int(kw['memoria_rechazo']), int(CF['NK'])], np.int64)\n",
          "    for m_ in range(30): C0f[22 + m_] = ME.G50_0[ME.NOMBRES50[m_]]   # G50\n"
          "    C0i = np.array([int(kw['memoria_rechazo']), int(CF['NK']), int(ME.G50_0['puerta_pat']), int(ME.G50_0['pat_min'])], np.int64)   # G50\n", 1))
ANCLAS_M = M

# ------------------------------------------------------------------------------------------------ nucleo_g50.py
N_ = []
N_.append(('N1', '"""nucleo_eco_sel_ing.py (CONSTRUIDO por experimentos/organelos/eco_sel_ing/construye_eco_sel_ing.py desde experimentos/organelos/eco_sel/\n',
           '"""nucleo_g50.py (CONSTRUIDO por experimentos/organelos/bloques/opusG/construye_g50.py desde experimentos/organelos/eco_sel_ing/\n'
           'nucleo_eco_sel_ing.py, sha c2189f9d22b72386; NO editar a mano). 50 GENES (exploratorio): el gemelo es motor_g50 (50 genes; con los\n'
           'brazos de la base, la base bit a bit) y se agregan ING_SEL_50 / ING_AZA_50 / ING_SEL_25 / ING_SEL_47. Lo que sigue es el docstring del origen.\n\n'
           'nucleo_eco_sel_ing.py (CONSTRUIDO por experimentos/organelos/eco_sel_ing/construye_eco_sel_ing.py desde experimentos/organelos/eco_sel/\n', 1))
N_.append(('N2', "    import motor_frio_rapido as MF\n", "    import motor_g50 as MF   # G50\n", 1))
N_.append(('N3', "          'ING_F1': ('MUT0', FAB, None), 'ING_SEL_C': ('CEREBRO', FAB, None), 'ING_AZA_C': ('CEREBRO_AZAR', FAB, None)}\n",
           "          'ING_F1': ('MUT0', FAB, None), 'ING_SEL_C': ('CEREBRO', FAB, None), 'ING_AZA_C': ('CEREBRO_AZAR', FAB, None),\n"
           "          # G50: los 50 genes (15 + dote, rep_umbral, rep_X + 32 nuevos); 25 = 15 + 10 del cerebro; 47 = 50 sin historia de vida\n"
           "          'ING_SEL_50': ('G50', FAB, None), 'ING_AZA_50': ('G50_AZAR', FAB, None), 'ING_SEL_25': ('G25', FAB, None),\n"
           "          'ING_SEL_47': ('G47', FAB, None), 'ING_AZA_47': ('G47_AZAR', FAB, None),\n"
           "          # G50 (19:55): VIVERO FINITO hasta 100 000 (sin subsidio despues; la lectura de Opus M, candidato E3: con vivero permanente K\n"
           "          # no es monotono en la calidad del organismo)\n"
           "          'ING_SEL_C_V': ('CEREBRO', FAB, 100000), 'ING_SEL_47_V': ('G47', FAB, 100000), 'ING_AZA_47_V': ('G47_AZAR', FAB, 100000)}\n", 1))
N_.append(('N4', "VENTANAS = (46101, 46121)                 # ECO_SEL_ING: serie y replica\n"
                 "PRACTICA = tuple(range(46191, 46200))    # ECO_SEL_ING: humo 46195; el arnes usa 46191-46194\n"
                 "HUMO = dict(semilla=46195, T=200000)\n",
           "VENTANAS = (48801, 48811)                 # G50: exploracion 48801-48810; 48811-48850 reservadas para la nube\n"
           "PRACTICA = tuple(range(48891, 48896))    # G50: arnes 48891-48894, humo 48895\n"
           "HUMO = dict(semilla=48895, T=200000)\n", 1))
N_.append(('N5', "_SIGMA = [None]   # ECO_SEL: SOLO el arnes lo fija (sigma 0 -> el gen fijo == F1 bit a bit); None = SERIE['sigma']\n",
           "import motor_eco50 as ME50   # G50 (vive junto a este archivo)\n"
           "G25_MUT = tuple(CR.BRAZOS['CEREBRO']['mutables']) + ('sesgo_boca', 'temp_boca', 'umbral_fam', 'R_bueno_E', 'R_bueno_A', 'R_malo_E',\n"
           "                                                     'R_malo_A', 'peso_sed', 'clip_e', 'x_aversion_s')\n"
           "G47_MUT = tuple(g for g in ME50.NOMBRES if g not in ('dote', 'rep_umbral', 'rep_X'))\n"
           "GENETICAS.update({'G50': dict(mutables=tuple(ME50.NOMBRES), donante='padre', p=True),\n"
           "                  'G50_AZAR': dict(mutables=tuple(ME50.NOMBRES), donante='azar', p=True),\n"
           "                  'G25': dict(mutables=G25_MUT, donante='padre', p=True), 'G47': dict(mutables=G47_MUT, donante='padre', p=True),\n"
           "                  'G47_AZAR': dict(mutables=G47_MUT, donante='azar', p=True)})   # G50: anadido 19:45 (control de SEL_47)\n"
           "_SIGMA = [None]   # ECO_SEL: SOLO el arnes lo fija (sigma 0 -> el gen fijo == F1 bit a bit); None = SERIE['sigma']\n", 1))
N_.append(('N6', "                donante=b['donante'], **extra)\n",
           "                donante=b['donante'], **{**extra, **_GENOMA[0]})   # G50: SOLO el arnes fija un genoma inicial\n"
           "_GENOMA = [{}]   # G50: SOLO el arnes (dict(genoma=...)): la prueba de que cada gen nuevo se usa\n", 1))
N_.append(('N7', "RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))\n",
           "RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))   # G50: un nivel mas hondo (bloques/opusG)\n", 1))
ANCLAS_N = N_


def _aplica(txt, anclas, etq):
    for nom, old, new, n_esp in anclas:
        n = txt.count(old)
        if n != n_esp: raise SystemExit(f"construye_g50 [{etq}]: el ancla {nom} aparece {n} veces (se esperan {n_esp})")
        txt = txt.replace(old, new)
    return txt


def construye():
    out = {}
    for dst, anc in (('motor_eco50.py', ANCLAS_E), ('motor_g50.py', ANCLAS_M), ('nucleo_g50.py', ANCLAS_N)):
        p, sh = ORI[dst]
        if h16(p) != sh: raise SystemExit(f"construye_g50: {p} tiene sha {h16(p)}, se esperaba {sh}")
        out[dst] = _aplica(open(p, encoding='utf-8', newline='').read(), anc, dst)
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    out = construye()
    if '--verifica' in argv:
        ok = True
        for dst, txt in out.items():
            p = os.path.join(AQUI, dst); igual = os.path.exists(p) and open(p, encoding='utf-8', newline='').read() == txt
            ok = ok and igual
            print(f"construye_g50 --verifica {dst}: {'IGUAL' if igual else 'DISTINTO'} (origen {ORI[dst][1]}; destino {h16(p) if os.path.exists(p) else None})")
        return ok
    for dst, txt in out.items():
        p = os.path.join(AQUI, dst)
        with open(p, 'w', encoding='utf-8', newline='') as f: f.write(txt)
        print(f"escrito {dst} (sha {h16(p)}) desde {ORI[dst][0]} ({ORI[dst][1]})")
    return True


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
