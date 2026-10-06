"""construye_enriquecido.py — construye motor_enriquecido.py POR ANCLAS desde experimentos/organelos/bloques/opusM/motor_bloques.py
(sha ff782697e54585a5; el motor de BLOQUES = FUNCIONA x2). NO toca el origen. EXPLORATORIO (29-sep-2026, encargo MUNDO ENRIQUECIDO,
plan 3b de registro/ESTADO.md).

Mision: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros, y solo con seleccion natural.

LO NUEVO (todo apagado por defecto; apagado == motor_bloques bit a bit, arnes):
 1. NUEZ (tarea con SECUENCIA). Una fraccion f de la comida (A) que LLEGA por el quimiostato llega CERRADA (capa NZ[x] = 1 sobre la
    celda; la retina y el cerebro de fabrica ven una A). La nuez se abre SOLO si la mordida inmediatamente anterior del cuerpo fue la
    LLAVE (letra C, agua): orden C -> nuez. Abrir = la A de siempre + bonus (E y Ag), se consume. Morder la nuez sin llave (suelta o en
    orden inverso) = no abre, no se consume, cuesta c_fallo de E, BORRA la llave (la memoria de la ultima mordida queda en -1) y el
    cuerpo la DEJA: la celda entra a su memoria de rechazo de fabrica (memoria_rechazo pasos), como si la boca la hubiera rechazado.
    (Calibracion de viabilidad, 29-sep 10:58, declarada en el PREREGISTRO §9: sin esto los cuerpos se quedan pegados a la nuez
    mordiendo ~1/3 de sus pasos y el linaje se extingue al cerrar el vivero, con y sin c_fallo.)
    rng PROPIO del mundo de nueces ([seed, 0, 7705, 0]): con f = 0 el mundo es el de BLOQUES bit a bit (arnes).
 2. SENTIDO 6 de las reglas: "el foco es una nuez cerrada" (0/1). Solo lo leen las reglas (el cerebro de fabrica no).
 3. ACCION 4 de las reglas: IMPULSO DE COPIAR (suma de w de las reglas que se cumplen; memoria RM[s, 3]).
 4. CANAL SOCIAL (despues de la fase A de cada paso). Si un cuerpo con impulso > 0 tiene a <= radio celdas a un vecino que ABRIO una
    nuez en este paso, con prob min(1, impulso/3) copia UNA regla (al azar) de:
      social 1 SOC : el vecino que abrio (el mas cercano);
      social 2 DESF: un vecino al azar dentro del radio que NO abrio (si no hay, un vivo al azar); mismo disparo, misma moneda;
      social 3 OFF : nada (el canal esta apagado; se cuentan los disparos);
      social 0     : no se evalua (identidad).
    La regla copiada se agrega (o reemplaza una al azar si la lista esta llena) y se hereda con la lista del padre. rng PROPIO
    ([seed, 0, 7706, 0]).
 5. El kit de las reglas al azar y de la mutacion de campo se lee de BQ_CFG['nsen'] / ['nacc'] (por defecto 6 / 4 = kit 1 de BLOQUES).
 6. Memoria nueva por cuerpo: 2 numeros (RM[s, 3] impulso de copiar del paso, RM[s, 4] t de la ultima nuez abierta). Del mundo: la capa
    NZ (L enteros). Telemetria NZC (contadores) y NZ_OUT (serie cada cada_gen); todo viaja en el checkpoint (st y ES).

Uso:  python construye_enriquecido.py            # escribe motor_enriquecido.py
      python construye_enriquecido.py --verifica # reconstruye en memoria y compara con el archivo (IGUAL / DISTINTO)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
ORIGEN = os.path.join(ORG, 'bloques', 'opusM', 'motor_bloques.py')
SHA_ORIGEN = 'ff782697e54585a5'
DESTINO = os.path.join(AQUI, 'motor_enriquecido.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


ANCLAS = []   # (nombre, viejo, nuevo): cada viejo debe aparecer EXACTAMENTE una vez

ANCLAS.append(('E0 docstring', '"""motor_bloques.py (CONSTRUIDO por',
'''"""motor_enriquecido.py (CONSTRUIDO por experimentos/organelos/enriquecido/construye_enriquecido.py desde
experimentos/organelos/bloques/opusM/motor_bloques.py, sha ff782697e54585a5; NO editar a mano). MUNDO ENRIQUECIDO (29-sep-2026,
EXPLORATORIO): nuez que solo se abre con la secuencia C -> nuez, sentido 'nuez', accion 'copiar' y canal social. Ver
construye_enriquecido.py. Lo que sigue es el docstring del origen.

motor_bloques.py (CONSTRUIDO por'''))

ANCLAS.append(('E1 ruta FRIO',
"FRIO = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frio')   # BLOQUES: vive en bloques/opusM",
"FRIO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'frio')   # ENRIQUECIDO: vive en organelos/enriquecido"))

ANCLAS.append(('E2 firma', "FIRMA_GEMELO = 'motor_bloques v0'", "FIRMA_GEMELO = 'motor_enriquecido v0'"))

ANCLAS.append(('E3 constantes', "NRMAX = 12; NRC = 6; NRM = 3\n",
"""NRMAX = 12; NRC = 6; NRM = 5   # ENRIQUECIDO: RM[s, 3] impulso de copiar del paso, RM[s, 4] t de la ultima nuez abierta
# ENRIQUECIDO: la nuez y el canal social (apagados por defecto)
NZ_CFG = dict(nuez=0, f=0.5, bonus=0.8, c_fallo=0.005, llave=2, social=0, radio=10)
NZ_OUT = {}
NNZC = 16   # contadores: 0 intentos de nuez, 1 abre, 2 falla, 3 A comun mordida, 4 A comun mordida con llave, 5 (libre),
            # 6 A llegadas, 7 nueces creadas, 8 disparos (vecino abrio cerca y hay impulso), 9 pasan la moneda, 10 copias hechas,
            # 11 fuente sin reglas, 12 DESF sin vecino (fuente = vivo al azar), 13 copias que reemplazan, 14-15 libres
"""))

ANCLAS.append(('E4 kit en BQ_CFG', "              inicial=None, forzada=None)\n",
"              inicial=None, forzada=None, nsen=6, nacc=4)   # ENRIQUECIDO: kit (6/4 = kit 1 de BLOQUES)\n"))

ANCLAS.append(('E5 firma del tramo', "           LFAM, tbR, tbH, mdR, mdH, dado, tn, tk, tR, sce, rst, tni, tnf, RG, RN, RM, BQ):",
"           LFAM, tbR, tbH, mdR, mdH, dado, tn, tk, tR, sce, rst, tni, tnf, RG, RN, RM, BQ,\n"
"           NZ, NZP, NZF, NZC, rng_nz, rng_soc):"))

ANCLAS.append(('E6 llamada del tramo', "                  st['tni'], st['tnf'], st['RG'], st['RN'], st['RM'], st['BQ'])",
"                  st['tni'], st['tnf'], st['RG'], st['RN'], st['RM'], st['BQ'],\n"
"                  st['NZ'], st['NZP'], st['NZF'], st['NZC'], st['rng_nz'], st['rng_soc'])"))

ANCLAS.append(('E7 patas (foco nuez)', "                _reglas_mov(s, RG, RN, RM, V, E, Ag, d, k, left, PATM)\n",
"""                fzm = 0.0   # ENRIQUECIDO: el foco (lo que mira) es una nuez cerrada
                if NZP[0] != 0 and k >= 0 and d >= 0:
                    xf = pos - d if left else pos + d
                    if xf < 0: xf += L
                    elif xf >= L: xf -= L
                    if NZ[xf] == 1: fzm = 1.0
                _reglas_mov(s, RG, RN, RM, V, E, Ag, d, k, left, PATM, fzm)
"""))

ANCLAS.append(('E8 boca (foco nuez)', "                    Vb += _reglas_boca(s, RG, RN, RM, E, Ag, d, kk, PATM)\n",
"                    Vb += _reglas_boca(s, RG, RN, RM, E, Ag, d, kk, PATM, (1.0 if (NZP[0] != 0 and NZ[pos2] == 1) else 0.0))\n"))

ANCLAS.append(('E9 nuez: resultado de la mordida', "            # --- la pista: mover y morder\n            bi[s, I_POS] = pos2\n",
"""            nzf = 0   # ENRIQUECIDO: 1 abre la nuez (la mordida anterior fue la llave), 2 falla (suelta o en orden inverso)
            if NZP[0] != 0 and mordio and kk == 0:
                if NZ[pos2] == 1:
                    NZC[0] += 1
                    if RM[s, 0] == NZP[2]:
                        nzf = 1; NZC[1] += 1
                    else:
                        nzf = 2; NZC[2] += 1
                else:
                    NZC[3] += 1
                    if RM[s, 0] == NZP[2]: NZC[4] += 1
            # --- la pista: mover y morder
            bi[s, I_POS] = pos2
"""))

ANCLAS.append(('E10 nuez: energia', "                if mordio:\n"
"                    v = bf[s, F_E] + EFF[kk, 0]; bf[s, F_E] = 1.5 if 1.5 < v else v\n"
"                    v = bf[s, F_AG] + EFF[kk, 1]; bf[s, F_AG] = 1.5 if 1.5 < v else v\n",
"""                if nzf == 2:   # ENRIQUECIDO: nuez sin llave: no abre, no se consume, cuesta y borra la llave
                    bf[s, F_E] -= NZF[1]; RM[s, 0] = -1.0; RM[s, 1] = 0.0
                    if MRs != 0:   # y la DEJA: la celda entra a la memoria de rechazo de fabrica (como un rechazo de la boca)
                        if not _rset(rpos, rexp, bi, s, pos2, t + MRs, t):
                            wi[W_ERR] = ERR_RECH; return ST_ERR, t
                if mordio and nzf != 2:
                    v = bf[s, F_E] + EFF[kk, 0]
                    if nzf == 1: v += NZF[0]
                    bf[s, F_E] = 1.5 if 1.5 < v else v
                    v = bf[s, F_AG] + EFF[kk, 1]
                    if nzf == 1: v += NZF[0]
                    bf[s, F_AG] = 1.5 if 1.5 < v else v
                    if nzf == 1:
                        NZ[pos2] = 0; RM[s, 4] = t
"""))

ANCLAS.append(('E11 olvido limpia la capa', "                olv[nolv] = dx; nolv += 1; wi[W_OLV] += 1\n",
"                olv[nolv] = dx; nolv += 1; wi[W_OLV] += 1\n                NZ[dx] = 0   # ENRIQUECIDO\n"))

ANCLAS.append(('E12 llegada: nuez cerrada', "                            _pon(x2, rng.integers(0, 4), grid, oseq, seqpos, bit, wi, C); break\n",
"""                            _pon(x2, rng.integers(0, 4), grid, oseq, seqpos, bit, wi, C)
                            if NZP[0] != 0 and grid[x2] == 0:   # ENRIQUECIDO: la A que llega, cerrada con prob f (rng propio)
                                NZC[6] += 1
                                if rng_nz.random() < NZF[2]:
                                    NZ[x2] = 1; NZC[7] += 1
                            break
"""))

ANCLAS.append(('E13 canal social', "        # ------------------------------------------------ costos\n",
"""        if NZP[1] != 0:   # ENRIQUECIDO: canal social (despues de la fase A)
            _social(t, nb, cuer, orden, bi, RG, RN, RM, NZP, NZC, rng_soc, L)
        # ------------------------------------------------ costos
"""))

ANCLAS.append(('E14 refundacion', "                RM[s2, 0] = -1.0; RM[s2, 1] = 0.0; RM[s2, 2] = 0.0; RN[s2] = 0   # BLOQUES\n",
"                RM[s2, 0] = -1.0; RM[s2, 1] = 0.0; RM[s2, 2] = 0.0; RN[s2] = 0   # BLOQUES\n"
"                RM[s2, 3] = 0.0; RM[s2, 4] = -1.0   # ENRIQUECIDO\n"))

ANCLAS.append(('E15 parto', "                    RM[s3, 0] = -1.0; RM[s3, 1] = 0.0; RM[s3, 2] = 0.0; RN[s3] = 0   # BLOQUES\n",
"                    RM[s3, 0] = -1.0; RM[s3, 1] = 0.0; RM[s3, 2] = 0.0; RN[s3] = 0   # BLOQUES\n"
"                    RM[s3, 3] = 0.0; RM[s3, 4] = -1.0   # ENRIQUECIDO\n"))

ANCLAS.append(('E16 memoria fresca', "    if '_bq_ok' not in st: st['RM'][:, 0] = -1.0   # arranque fresco (en un checkpoint ya viene)\n",
"    if '_bq_ok' not in st: st['RM'][:, 0] = -1.0; st['RM'][:, 4] = -1.0   # arranque fresco (en un checkpoint ya viene)\n"))

ANCLAS.append(('E17 arranque NZ', "    _bq_arranque(st, n)   # BLOQUES\n",
"    _bq_arranque(st, n)   # BLOQUES\n    _nz_arranque(st, seed)   # ENRIQUECIDO\n"))

ANCLAS.append(('E18 muestra NZ',
"            if BQ_CFG['on'] and E_['cada_gen'] and t % E_['cada_gen'] == 0: _bq_muestra(st, t)   # BLOQUES\n",
"            if BQ_CFG['on'] and E_['cada_gen'] and t % E_['cada_gen'] == 0: _bq_muestra(st, t)   # BLOQUES\n"
"            if (NZ_CFG['nuez'] or NZ_CFG['social']) and E_['cada_gen'] and t % E_['cada_gen'] == 0: _nz_muestra(st, t)   # ENRIQUECIDO\n"))

ANCLAS.append(('E19 final NZ', "    if BQ_CFG['on']: _bq_final(st, vivos)   # BLOQUES\n",
"    if BQ_CFG['on']: _bq_final(st, vivos)   # BLOQUES\n    if NZ_CFG['nuez'] or NZ_CFG['social']: _nz_final(st)   # ENRIQUECIDO\n"))

# ---- las funciones de las reglas: sentido 6 (foco nuez) y accion 4 (copiar); con el kit 1 son las de BLOQUES operacion a operacion
ANCLAS.append(('E20 _sentido', """def _sentido(sid, par, E, Ag, d, foco, lk, lr, PATM):
    if sid == 0: return _clip(1 - E, 0.0, 1.0)""",
"""def _sentido(sid, par, E, Ag, d, foco, lk, lr, PATM, fz):
    if sid == 6: return fz   # ENRIQUECIDO: el foco es una nuez cerrada
    if sid == 0: return _clip(1 - E, 0.0, 1.0)"""))

ANCLAS.append(('E21 _cumple', """def _cumple(s, r, RG, RM, E, Ag, d, foco, PATM):
    x = _sentido(int(RG[s, r, 0]), int(RG[s, r, 1]), E, Ag, d, foco, int(RM[s, 0]), RM[s, 1], PATM)""",
"""def _cumple(s, r, RG, RM, E, Ag, d, foco, PATM, fz):
    x = _sentido(int(RG[s, r, 0]), int(RG[s, r, 1]), E, Ag, d, foco, int(RM[s, 0]), RM[s, 1], PATM, fz)"""))

ANCLAS.append(('E22 _reglas_mov', """def _reglas_mov(s, RG, RN, RM, V, E, Ag, d, k, left, PATM):
    pb = 0.0
    for r in range(RN[s]):
        a = int(RG[s, r, 4])
        if a == 0: continue
        if not _cumple(s, r, RG, RM, E, Ag, d, k, PATM): continue
        w = RG[s, r, 5]
        if a == 1:
            if k >= 0 and d > 0:
                if left: V[0] += w
                else: V[1] += w
        elif a == 2:
            V[0] -= w; V[1] -= w
        else:
            pb += w
    RM[s, 2] = pb""",
"""def _reglas_mov(s, RG, RN, RM, V, E, Ag, d, k, left, PATM, fz):
    pb = 0.0; pc = 0.0
    for r in range(RN[s]):
        a = int(RG[s, r, 4])
        if a == 0: continue
        if not _cumple(s, r, RG, RM, E, Ag, d, k, PATM, fz): continue
        w = RG[s, r, 5]
        if a == 1:
            if k >= 0 and d > 0:
                if left: V[0] += w
                else: V[1] += w
        elif a == 2:
            V[0] -= w; V[1] -= w
        elif a == 3:
            pb += w
        else:
            pc += w   # ENRIQUECIDO: accion 4, impulso de copiar
    RM[s, 2] = pb
    RM[s, 3] = pc"""))

ANCLAS.append(('E23 _reglas_boca', """def _reglas_boca(s, RG, RN, RM, E, Ag, d, kk, PATM):
    b = 0.0
    for r in range(RN[s]):
        if int(RG[s, r, 4]) != 0: continue
        if _cumple(s, r, RG, RM, E, Ag, d, kk, PATM): b += RG[s, r, 5]""",
"""def _reglas_boca(s, RG, RN, RM, E, Ag, d, kk, PATM, fz):
    b = 0.0
    for r in range(RN[s]):
        if int(RG[s, r, 4]) != 0: continue
        if _cumple(s, r, RG, RM, E, Ag, d, kk, PATM, fz): b += RG[s, r, 5]"""))

ANCLAS.append(('E24 _regla_azar', """def _regla_azar(rr):
    return [float(rr.integers(0, 6)), float(rr.integers(0, 6)), float(rr.integers(0, 2)), float(rr.random()),
            float(rr.integers(0, 4)), float(rr.uniform(-3.0, 3.0))]""",
"""def _regla_azar(rr, C):
    return [float(rr.integers(0, int(C['nsen']))), float(rr.integers(0, 6)), float(rr.integers(0, 2)), float(rr.random()),
            float(rr.integers(0, int(C['nacc']))), float(rr.uniform(-3.0, 3.0))]"""))

ANCLAS.append(('E25 mutar sentido', "            if f == 0: x[0] = float(rr.integers(0, 6))\n",
"            if f == 0: x[0] = float(rr.integers(0, int(C['nsen'])))\n"))
ANCLAS.append(('E26 mutar accion', "            elif f == 4: x[4] = float(rr.integers(0, 4))\n",
"            elif f == 4: x[4] = float(rr.integers(0, int(C['nacc'])))\n"))
ANCLAS.append(('E27 insertar', "        R.append(_regla_azar(rr)); O['n_ins'] += 1\n", "        R.append(_regla_azar(rr, C)); O['n_ins'] += 1\n"))
ANCLAS.append(('E28 inicial', "                R = np.array([_regla_azar(rr) for _ in range(int(C['inicial']))], np.float64).reshape(-1, NRC)\n",
"                R = np.array([_regla_azar(rr, C) for _ in range(int(C['inicial']))], np.float64).reshape(-1, NRC)\n"))

NUEVO = '''
# ================================================================ ENRIQUECIDO (anadido por construye_enriquecido.py)
@njit(cache=True)
def _dist_anillo(a, b, L):
    x = a - b
    if x < 0: x = -x
    if L - x < x: x = L - x
    return x


@njit(cache=True)
def _social(t, nb, cuer, orden, bi, RG, RN, RM, NZP, NZC, rs, L):
    """Canal social (despues de la fase A del paso t). Disparo: el cuerpo tiene impulso de copiar > 0 y un vecino a <= radio ABRIO una
    nuez en este paso. Moneda: prob min(1, impulso / 3) (rng propio). Fuente: SOC el que abrio (el mas cercano; empate: el primero de
    la lista); DESF un vecino al azar a <= radio que NO abrio (si no hay: un vivo al azar distinto de el); OFF ninguna. Copia UNA
    regla al azar de la fuente (se agrega; con la lista llena reemplaza una al azar)."""
    modo = NZP[1]; rad = NZP[3]
    hay = False
    for jj in range(nb):
        if RM[cuer[jj], 4] == t:
            hay = True; break
    if not hay: return
    for jj in range(nb):
        js = orden[jj]; s = cuer[js]
        dr = RM[s, 3]
        if dr <= 0.0 or RM[s, 4] == t: continue
        p = bi[s, I_POS]; v = -1; dv = rad + 1
        for kk in range(nb):
            u = cuer[kk]
            if u == s or RM[u, 4] != t: continue
            a = _dist_anillo(bi[u, I_POS], p, L)
            if a < dv:
                dv = a; v = u
        if v < 0: continue
        NZC[8] += 1
        pr = dr / 3.0
        if pr < 1.0 and rs.random() >= pr: continue
        NZC[9] += 1
        if modo == 3: continue
        if modo == 2:
            m = 0
            for kk in range(nb):
                u = cuer[kk]
                if u == s or RM[u, 4] == t: continue
                if _dist_anillo(bi[u, I_POS], p, L) <= rad: m += 1
            if m > 0:
                r_ = rs.integers(0, m); m2 = 0
                for kk in range(nb):
                    u = cuer[kk]
                    if u == s or RM[u, 4] == t: continue
                    if _dist_anillo(bi[u, I_POS], p, L) <= rad:
                        if m2 == r_:
                            v = u; break
                        m2 += 1
            else:
                NZC[12] += 1
                i_ = rs.integers(0, nb - 1)
                if i_ >= js: i_ += 1
                v = cuer[i_]
        if RN[v] == 0:
            NZC[11] += 1; continue
        r = rs.integers(0, RN[v])
        if RN[s] < NRMAX:
            m = RN[s]
            for c in range(NRC): RG[s, m, c] = RG[v, r, c]
            RN[s] = m + 1
        else:
            i = rs.integers(0, NRMAX)
            for c in range(NRC): RG[s, i, c] = RG[v, r, c]
            NZC[13] += 1
        NZC[10] += 1


def _nz_arranque(st, seed):
    """La capa de nueces, los parametros, los contadores y los rng propios. Con --reanuda vienen del blob y la cfg DEBE coincidir
    (la de NZ y la de BQ): si no, aborta (leccion de pista_pob: la cfg se fija en cada trabajador y se comprueba al reanudar)."""
    C = dict(NZ_CFG)
    P_ = np.array([int(C['nuez']), int(C['social']), int(C['llave']), int(C['radio'])], np.int64)
    F_ = np.array([float(C['bonus']), float(C['c_fallo']), float(C['f'])])
    ES = _CTX['ES']
    if 'NZ' in st:
        if not (np.array_equal(st['NZP'], P_) and np.array_equal(st['NZF'], F_)):
            raise SystemExit('ENRIQUECIDO: el checkpoint es de otra cfg de NZ')
        bqo = ES.get('_BQO', {}).get('cfg')
        if bqo is not None and {k: bqo.get(k) for k in BQ_CFG} != dict(BQ_CFG):
            raise SystemExit('ENRIQUECIDO: el checkpoint es de otra cfg de BQ')
        NZ_OUT.clear(); NZ_OUT.update(ES['_NZO']); ES['_NZO'] = NZ_OUT
        return
    st['NZ'] = np.zeros(st['grid'].shape[0], np.int64); st['NZP'] = P_; st['NZF'] = F_; st['NZC'] = np.zeros(NNZC, np.int64)
    st['rng_nz'] = np.random.default_rng([seed, 0, 7705, 0]); st['rng_soc'] = np.random.default_rng([seed, 0, 7706, 0])
    NZ_OUT.clear(); NZ_OUT.update(cfg={k: v for k, v in C.items()}, serie=[])
    ES['_NZO'] = NZ_OUT


def _tiene(R, sen=None, acc=None, wpos=None):
    for x in R:
        if sen is not None and int(x[0]) != sen: continue
        if acc is not None and int(x[4]) != acc: continue
        if wpos is not None and ((x[5] > 0) != wpos): continue
        return True
    return False


def _nz_muestra(st, t):
    v = _vivos(st)
    RG = st['RG']; RN = st['RN']
    nc = sum(1 for s in v if _tiene(RG[s, :RN[s]], acc=4, wpos=True))
    nn = sum(1 for s in v if _tiene(RG[s, :RN[s]], sen=6))
    NZ_OUT['serie'].append([int(t), len(v)] + [int(x) for x in st['NZC']] + [nc, nn, int(st['NZ'].sum())])


def _nz_final(st):
    NZ_OUT['NZC_T'] = [int(x) for x in st['NZC']]
    NZ_OUT['nueces_T'] = int(st['NZ'].sum())


# ================================================================ BLOQUES (anadido por construye_bloques.py)'''

ANCLAS.append(('E29 bloque nuevo', "\n# ================================================================ BLOQUES (anadido por construye_bloques.py)", NUEVO))


def construye():
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f'origen cambio: {h16(ORIGEN)} != {SHA_ORIGEN}')
    txt = open(ORIGEN, encoding='utf-8').read()
    for nom, viejo, nuevo in ANCLAS:
        c = txt.count(viejo)
        if c != 1: raise SystemExit(f'ancla {nom}: aparece {c} veces (debe ser 1)')
        txt = txt.replace(viejo, nuevo)
    return txt


if __name__ == '__main__':
    t = construye()
    if '--verifica' in sys.argv:
        print('IGUAL' if open(DESTINO, encoding='utf-8').read() == t else 'DISTINTO', h16(DESTINO))
    else:
        with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f: f.write(t)
        print('escrito', DESTINO, h16(DESTINO), f'({len(ANCLAS)} anclas, origen {SHA_ORIGEN})')
