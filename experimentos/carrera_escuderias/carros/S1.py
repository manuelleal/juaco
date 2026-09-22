"""carros/S1.py — EL CARRO DE LA ESCUDERIA S1 (Sonnet), carrera de escuderias.

MISION: llegar a la AGI por este camino.

PUNTO DE PARTIDA: el cerebro de carros/FABRICA.py (brazo REL de organismo_f9c), SIN TOCAR ni una linea de
aprendizaje, plasticidad ni decision de la boca. UN SOLO CAMBIO, quirurgico y localizado en la vista (`_see`):
al elegir a que objeto ir, entre los candidatos NO rechazados por memoria, S1 descarta los que estan
"disputados" (algun otro cuerpo visible en `obs['cuerpos']` esta MAS CERCA de ese objeto que yo) y va al mas
cercano de los que quedan LIBRES; si todos estan disputados, cae exactamente en la regla de FABRICA (el mas
cercano de todos). Con N=1 (sin rivales) `rivales` es la tupla vacia y el resultado es BIT A BIT el de FABRICA.

MOTIVO (dato, INFORME_PISTA.md v3 + ERR-98): con 9 cuerpos cada linaje pierde su objetivo bueno por ROBO
(otro cuerpo se lo come primero) ~100-200x mas seguido que por olvido del mundo (1612-3808 contra 6-17 cada
100k pasos), vive ~3x menos que un cuerpo SOLO y muerde veneno/sal un 36% mas con la MISMA composicion del
mundo. La hipotesis de trabajo (no medida alli, la que dejaron para medir antes de la ronda 1): la perdida del
objetivo por robo empuja el hambre, y el hambre empuja la boca a morder lo que tenga delante (H-BOCA, igual
mecanismo que en la fase 10). S1 ataca la CAUSA (perder el objetivo por robo), no el sintoma (que muerde la
boca), sin agregar memoria nueva: la decision usa solo lo que la pista YA entrega cada paso en `obs['cuerpos']`
(posicion de los demas cuerpos), nada de canal, nada de tabla verdadera, nada de rng del mundo.

Por que esto no puede ser PEOR que FABRICA (propiedad de diseno, no medida): si TODO esta disputado, el
resultado es identico al de FABRICA (mismo objeto, mismo `pat`, misma entrada a Wl). El unico riesgo es un
FALSO POSITIVO: creer disputado un objeto que el rival no iba a tocar (el rival puede estar mas cerca por ir a
OTRO objeto), lo que alarga el viaje sin necesidad. Ese es el control que puede fallar (ver bitacoras/S1.md).

Peldano biologico: bacteria — quimiotaxis de un paso (sin secuencia, sin planificacion, sin memoria persistente
nueva); la unica "decision" nueva es "no vayas donde ya hay alguien mas cerca que tu".

RAMAS y arquitectura: identicas a FABRICA.py (misma validacion H-4: si una perilla de rama no esta portada,
crea() ABORTA). Diferencia declarada de la ENMIENDA 1 opcion A (igual que FABRICA): el anillo es el de la
pista (ctx['L']) y S1 tambien ve TODOS los objetos (`obs['objs']`), no solo los cercanos.

INTERFAZ: identica a FABRICA.py (ver ese docstring). `salida()` agrega dos contadores PROPIOS de solo lectura
(elecciones, evitados) que van a d['carro'] (ERR-96: el juez NO los usa para puntuar; son telemetria de S1
para su propia bitacora).
"""
import numpy as np

# perillas que eligen RAMA en el monolito -> el valor que este archivo porta (identico a FABRICA.py).
RAMAS = dict(vivo=1, n_nec=2, rep_cuello=2, puerta=3, puerta_pat=5, pat_shuf=0, mask_rel=2, div_signo=True,
             mu_norm=True, eta_pred=0.0, k_sorp=0.0, sesgo_fijo=0.0, nodo_via=0, nodo_or=0, nodo_baraja=0,
             con_desde=0, nodo_rel=1, nodo=1, conectado=1, hereda='nada', learn=True, plast=True, val_esc=0,
             nec_shuf=0, rep_nec=0, hereda_nec=1, solap_AB=None, nuevo=None, invertir_en=None, log_cada=None,
             tabla=None, f9=1, f9c=1, muerte_real=1, h1=1, rep2=1, reproduccion=1, rep_mide=1,
             menu='f', alma_curita='f')


class Carro:
    def __init__(self, ctx):
        cf = ctx['fabrica']; kw = cf['kw']
        mal = {k: (kw.get(k), v) for k, v in RAMAS.items() if kw.get(k) != v}
        if mal: raise SystemExit(f"S1: ramas no portadas {mal}")
        self.L = ctx['L']   # OPCION A: L de la pista; sigue viendo el mundo ENTERO (igual que FABRICA)
        self.NK = cf['NK']; self.NKMAX = cf['NKMAX']; self.K = cf['K']; self.PAT = cf['PAT']
        self.ETA = kw['eta']; self.TAU_E = kw['tau_e']; self.ALPHA = kw['alpha']; self.HAMBRE_BOCA = kw['hambre_boca']
        self.AVERSION = kw['aversion']; self.EMA = kw['ema']; self.PASO = kw['paso']; self.LAM = kw['lam']
        self.MEMORIA_RECHAZO = kw['memoria_rechazo']; self.ETA_S = kw['eta_s']; self.CLIP_S = kw['clip_s']
        self.DEL_S = kw['del_s']; self.DEL_C = kw['del_c']; self.EMA_C = kw['ema_c']; self.PUERTA_PAT = kw['puerta_pat']
        self.PAT_MIN = kw['pat_min']; self.N_NEC = kw['n_nec']; self.NODO_K = kw['nodo_k']; self.NODO_LEE = kw['nodo_lee']
        self.ALMA_MUERTES = kw['alma_muertes']; self.MOTIVO = kw['alma_motivo']; self.KW0 = kw
        NK, NKMAX, N_NEC = self.NK, self.NKMAX, self.N_NEC
        rng = ctx['rng']; self.rng = rng; self.T = ctx['T']
        self.dote = ctx['dote']; self.rep_umbral = ctx['rep_umbral']
        self.Wl = rng.uniform(.1, .4, (2, 9)); self.KW = np.zeros((NKMAX, 6)); self.activa = np.zeros(NKMAX, bool)
        self.KW[:NK] = rng.uniform(0, 1, (NK, 6)); self.activa[:NK] = True
        while not self._cond(): self.KW[0:NK] = rng.uniform(0, 1, (NK - 0, 6))
        self.Wp = np.zeros((N_NEC, NKMAX)); self.Wn = np.zeros((N_NEC, NKMAX)); self.err = np.zeros(NKMAX)
        self.mu = np.zeros((NKMAX, 6)); self.splits = 0; self.el = np.zeros_like(self.Wl); self.tr = np.zeros(9)
        self.Wps = np.zeros((N_NEC, 6)); self.Wns = np.zeros((N_NEC, 6))
        self._na = 0; self._nm = 0
        self.Wpe = np.zeros((N_NEC, NKMAX)); self.Wke = np.zeros((N_NEC, NKMAX)); self._sbE = np.zeros(N_NEC)
        self._nodo = []; self._cur = []; self._mordh = []; self._con = True; self._nmu = 0
        self._ldiv = 0; self._nlec = 0; self._gpa = 0; self._gpn = 0; self._ncu = []; self._nbar = 0
        self.ncod = {}; self._ord = []
        self.mup = np.zeros((NKMAX, 6)); self.mun = np.zeros((NKMAX, 6)); self.zp = np.zeros(NKMAX); self.zn = np.zeros(NKMAX)
        self.err_max = 0.0; self.t_conflicto = None; self.t_techo = None; self.n_techo = 0
        self._rech = {}
        self.sin_objetivo = [0] * 4
        self.split_t = []
        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None
        # --- S1: telemetria PROPIA de la evitacion de disputa (solo lectura, no altera la fisica) ---
        self._elecciones = 0; self._evitados = 0

    # ------------------------------------------------------------ piezas del monolito (identicas a FABRICA)
    def _code(self, P):
        v = self.KW @ P; v = np.where(self.activa, v, -1e9); return set(np.argsort(v)[-self.K:])

    def _cond(self):
        return len(self._code(self.PAT['A']) & self._code(self.PAT['B'])) == 0

    def _kenyon(self, P):
        k = np.zeros(self.NKMAX); k[list(self._code(P))] = 1; return k

    @staticmethod
    def _key(_k): return frozenset(np.flatnonzero(_k).tolist())

    def _ev(self, _k):
        return self.ncod.get(self._key(_k), 0)

    def _fam(self, _k, _n=None):
        _w = self.Wp[self._nm if _n is None else _n] - self.Wn[self._nm if _n is None else _n]
        return self._ev(_k) >= self.PUERTA_PAT and int((np.abs(_w[_k > 0]) > 0.2).sum()) >= self.PAT_MIN

    def _valor(self, P):
        _k = self._kenyon(P); _f = float((self.Wp[self._nm] - self.Wn[self._nm]) @ _k); _s = float((self.Wps[self._nm] - self.Wns[self._nm]) @ P)
        return (_f if self._fam(_k) else _s)

    def _vnec(self, _n, P, _k):
        _f = float((self.Wp[_n] - self.Wn[_n]) @ _k); _s = float((self.Wps[_n] - self.Wns[_n]) @ P)
        return (_f if self._fam(_k, _n) else _s)

    def _q(self, t): return min(t // (self.T // 4), 3)

    # ------------------------------------------------------------ EL UNICO CAMBIO: vista con evitacion de disputa
    def _disputado(self, x, d, rivales, L):
        """True si algun rival (posicion, no yo) esta ESTRICTAMENTE mas cerca de x que yo (distancia d)."""
        for _id, rpos, _letra, _mord in rivales:
            dl = (rpos - x) % L; dr = (x - rpos) % L
            if min(dl, dr) < d: return True
        return False

    def _see(self, pos, objs, t, contar=False, rivales=()):
        """Identico a FABRICA salvo por `rivales`: entre los candidatos NO rechazados, prefiere el mas cercano
        de los que NADIE mas cerca que yo disputa. Si no hay ninguno libre (o no hay rivales, ej. N=1), cae
        EXACTAMENTE en la regla de FABRICA (el objeto mas cercano de todos, disputado o no)."""
        L = self.L; cand = []
        for x, k in objs.items():
            if self.MEMORIA_RECHAZO and self._rech.get(x, -1) > t: continue
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
            cand.append((d, x, k, dl < dr))
        if not cand:
            if contar: self.sin_objetivo[self._q(t)] += 1
            for x, k in objs.items():
                dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
                cand.append((d, x, k, dl < dr))
        if not cand: return None
        d0, x0, k0, left0 = min(cand, key=lambda c: c[0])
        self._elecciones += 1
        if not rivales: return (d0, k0, left0)
        libres = [c for c in cand if not self._disputado(c[1], c[0], rivales, L)]
        if not libres: return (d0, k0, left0)
        d1, x1, k1, left1 = min(libres, key=lambda c: c[0])
        if x1 != x0: self._evitados += 1
        return (d1, k1, left1)

    # ------------------------------------------------------------ INTERFAZ
    def valor_nec(self, n, letra):
        """SOLO LECTURA (la usa la telemetria exp_hasta de la pista, antes de resultado())."""
        return self._vnec(n, self.PAT[letra], self._kenyon(self.PAT[letra]))

    def actua(self, obs):
        PAT = self.PAT
        t = obs['t']; pos = obs['pos']; E = obs['E']; Ag = obs['Ag']; objs = obs['objs']; rng = self.rng
        # --- S1: rivales = los demas cuerpos vivos, tal cual los entrega la pista (sin canal, sin tabla verdadera) ---
        yo = obs['yo']; rivales = tuple(cu for cu in obs['cuerpos'] if cu[0] != yo)
        hambre = np.clip(1 - E, 0, 1)
        _dfa = np.clip(1 - Ag, 0, 1); self._na = _na = 1 if _dfa > hambre else 0
        if _na: hambre = _dfa
        _cue2 = bool(hambre == 0 and _dfa == 0)   # rep_cuello == 2 (RAMAS)
        self._nm = _na
        d, k, left = self._see(pos, objs, t, contar=True, rivales=rivales); pat = PAT[k]
        x = np.concatenate([pat * 1.2, [1.5 if left else 0, 0 if left else 1.5, 1.0 if d == 0 else 0.]]); noise = .15 + .5 * hambre
        V = self.Wl @ x; p = 1 / (1 + np.exp(-(V - .8) / noise)); u = p + rng.normal(0, .3, 2); m = np.zeros(2)
        if u.max() > .5: m[np.argmax(u)] = 1
        self.tr = self.tr * .7 + x
        self.el = self.el * self.TAU_E + np.outer(m - p, self.tr)
        mov = int(m[1] - m[0]); pos = (pos + mov) % self.L; d2, _, _ = self._see(pos, objs, t, rivales=rivales); Rp = .2 if d2 < d else 0.
        self._R = 0.; self._Rp = Rp; self._hambre = hambre; self._enc = None
        mordio = False
        if pos in objs:
            kk = objs[pos]; kc = self._kenyon(PAT[kk]); Wb = self.Wp[self._nm] - self.Wn[self._nm]; _wf = float(Wb @ kc); _ws = float((self.Wps[self._nm] - self.Wns[self._nm]) @ PAT[kk])
            _fa9 = bool(self._fam(kc))   # puerta is not None (RAMAS)
            _wt = (_wf if _fa9 else _ws)
            self._gpn += 1; self._gpa += int(_fa9)
            if _cue2: _wt = min(_wt, self._vnec(1 - _na, PAT[kk], kc))
            Vb = self.ALPHA * _wt + self.HAMBRE_BOCA * hambre + .5
            pb = 1 / (1 + np.exp(-Vb / .3)); mordio = bool(rng.random() < pb)
            if self.MEMORIA_RECHAZO and not mordio: self._rech[pos] = t + self.MEMORIA_RECHAZO
            self._enc = (pos, kk, kc, Wb, _wf, _ws)
        return dict(mov=mov, muerde=mordio, escribe=None)

    def resultado(self, res):
        """res: t, pos, letra, mordio, dS (nominal, solo si mordio). Aprendizaje de la mordida (sin rng). Identico a FABRICA."""
        if not res['mordio']: return
        PAT = self.PAT; ETA = self.ETA; ETA_S = self.ETA_S; AVERSION = self.AVERSION; LAM = self.LAM; CLIP_S = self.CLIP_S
        EMA = self.EMA; EMA_C = self.EMA_C; PASO = self.PASO; DEL_S = self.DEL_S; DEL_C = self.DEL_C; N_NEC = self.N_NEC
        t = res['t']; pos, kk, kc, Wb, _wf, _ws = self._enc
        _nm = self._nm; _na = self._na
        _dS = res['dS']; _Rv = [(1.0 if _x > 0 else (-3.0 if _x < 0 else 0.0)) for _x in _dS]
        R = _Rv[_na]; self._R = R
        self._mordh.append([int(t), kk, int(_na), float(R)])
        _ky = self._key(kc)
        if _ky not in self.ncod: self._ord.append(_ky)
        self.ncod[_ky] = self.ncod.get(_ky, 0) + 1
        self._rech.pop(pos, None)
        Wp, Wn, Wps, Wns = self.Wp, self.Wn, self.Wps, self.Wns
        dlt = R - _wf
        _ds = R - _ws
        if LAM: _mcs = np.minimum(Wps[_nm], Wns[_nm]) * (PAT[kk] > 0); Wps[_nm] = Wps[_nm] - LAM * _mcs; Wns[_nm] = Wns[_nm] - LAM * _mcs
        if _ds > 0: Wps[_nm] = np.clip(Wps[_nm] + ETA_S * _ds * PAT[kk], 0, CLIP_S)
        else:       Wns[_nm] = np.clip(Wns[_nm] + ETA_S * AVERSION * (-_ds) * PAT[kk], 0, CLIP_S)
        if LAM: ix = kc > 0; mcom = np.minimum(Wp[_nm][ix], Wn[_nm][ix]); Wp[_nm][ix] -= LAM * mcom; Wn[_nm][ix] -= LAM * mcom
        _ix = kc > 0
        if dlt > 0: _trunca = bool(((Wp[_nm][_ix] + ETA * dlt) > 3.0).any())
        else:       _trunca = bool(((Wn[_nm][_ix] + ETA * AVERSION * (-dlt)) > 3.0).any())
        if _trunca:
            self.n_techo += 1
            if self.t_techo is None: self.t_techo = t
        if dlt > 0: Wp[_nm] = np.clip(Wp[_nm] + ETA * dlt * kc, 0, 3.)
        else:       Wn[_nm] = np.clip(Wn[_nm] + ETA * AVERSION * (-dlt) * kc, 0, 3.)
        if self.t_conflicto is None and bool((np.minimum(Wp[_nm][_ix], Wn[_nm][_ix]) > 0).any()): self.t_conflicto = t
        for _n in range(N_NEC):
            if _n == _nm: continue
            _Rn = _Rv[_n]; _wfn = float((Wp[_n] - Wn[_n]) @ kc); _wsn = float((Wps[_n] - Wns[_n]) @ PAT[kk])
            _dn = _Rn - _wfn
            _dsn = _Rn - _wsn
            if LAM: _mn2 = np.minimum(Wps[_n], Wns[_n]) * (PAT[kk] > 0); Wps[_n] = Wps[_n] - LAM * _mn2; Wns[_n] = Wns[_n] - LAM * _mn2
            if _dsn > 0: Wps[_n] = np.clip(Wps[_n] + ETA_S * _dsn * PAT[kk], 0, CLIP_S)
            else:        Wns[_n] = np.clip(Wns[_n] + ETA_S * AVERSION * (-_dsn) * PAT[kk], 0, CLIP_S)
            if LAM: _mc2 = np.minimum(Wp[_n][_ix], Wn[_n][_ix]); Wp[_n][_ix] -= LAM * _mc2; Wn[_n][_ix] -= LAM * _mc2
            if _dn > 0: Wp[_n] = np.clip(Wp[_n] + ETA * _dn * kc, 0, 3.)
            else:       Wn[_n] = np.clip(Wn[_n] + ETA * AVERSION * (-_dn) * kc, 0, 3.)
        # plasticidad (v11 div_signo + hija dispersa D, mask_rel == 2)
        err, mu, mup, mun, zp, zn, KW, activa = self.err, self.mu, self.mup, self.mun, self.zp, self.zn, self.KW, self.activa
        P = PAT[kk]; idx = np.where(kc > 0)[0]; err[idx] = (1 - EMA) * err[idx] + EMA * abs(dlt); mu[idx] = (1 - EMA) * mu[idx] + EMA * P
        if R > 0: mup[idx] = (1 - EMA_C) * mup[idx] + EMA_C * P; zp[idx] = (1 - EMA_C) * zp[idx] + EMA_C
        elif R < 0: mun[idx] = (1 - EMA_C) * mun[idx] + EMA_C * P; zn[idx] = (1 - EMA_C) * zn[idx] + EMA_C
        self.err_max = max(self.err_max, float(err[idx].max()))
        for c in idx:
            dist = P - (mu[c] * (P.sum() / max(float(mu[c].sum()), 1e-9)))
            if zp[c] > 1e-6 and zn[c] > 1e-6:
                _mp = mup[c] / float(zp[c]); _mn = mun[c] / float(zn[c])
                _rel = (P > 0) & ((np.abs(_mp - _mn) > DEL_S) | (np.minimum(_mp, _mn) > 1.0 - DEL_C))
            else: _rel = (P > 0)
            kj = np.clip(KW[c] * (1 - 0.05) + PASO * dist, 0, 5) * _rel
            if Wb[c] * R < 0 and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(KW[c] @ P) and (~activa).any():
                j = int(np.where(~activa)[0][0]); activa[j] = True; KW[j] = kj
                if R > 0: Wp[_nm, j] = Wp[_nm, c]; Wn[_nm, j] = 0.; Wp[_nm, c] = 0.
                else:     Wn[_nm, j] = Wn[_nm, c]; Wp[_nm, j] = 0.; Wn[_nm, c] = 0.
                for _n in range(N_NEC):
                    if _n != _nm: Wp[_n, j] = Wp[_n, c]; Wn[_n, j] = Wn[_n, c]
                mu[j] = P * (float(mu[c].sum()) / P.sum()); err[c] = err[j] = 0; self.splits += 1; self.split_t.append((t, kk))
                mup[j] = mup[c].copy(); mun[j] = mun[c].copy(); zp[j] = zp[c]; zn[j] = zn[c]

    def fin_paso(self, info):
        for _dx in info['olvido']: self._rech.pop(_dx, None)
        self.Wl = np.clip(self.Wl + self.ETA * (1 + 2 * self._hambre) * (max(self._R, 0) + self._Rp) * self.el, 0, 1.5)

    def muere(self, info):
        """El alma NULA del brazo REL (curita 'f') + el NODO que se llena con las ultimas nodo_k mordidas. Identico a FABRICA."""
        self._nmu += 1
        for _t9, _k9, _n9, _R9 in self._mordh[-self.NODO_K:]: self._nodo.append([[float(_z9) for _z9 in self.PAT[_k9]], float(_R9), int(_n9)])
        self._cur.append([self._nmu, self.KW0['alma_curita'], self.MOTIVO[:240], round(float(self.dote), 4), round(float(self.rep_umbral), 4),
                          self.KW0['hereda'], int(self._con), len(self._nodo), info['causa'], int(info['edad']), int(info['hijos'])])
        self._ncu.append(int(self._con))
        self._mordh.clear()

    def al_parir(self, info):
        return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista) -- igual que FABRICA

    def nace(self, info):
        NK = self.NK; ETA_S = self.ETA_S; AVERSION = self.AVERSION; LAM = self.LAM; CLIP_S = self.CLIP_S
        _rh = info['rng_hijo']
        self.Wl[:] = _rh.uniform(.1, .4, (2, 9)); self.el[:] = 0; self.tr[:] = 0
        for a in (self.Wp, self.Wn, self.Wps, self.Wns, self.err, self.mu, self.mup, self.mun, self.zp, self.zn,
                  self.Wpe, self.Wke, self._sbE): a[:] = 0
        self.ncod.clear(); self._ord.clear(); self._rech.clear()
        self.KW[:] = 0; self.activa[:] = False; self.KW[:NK] = _rh.uniform(0, 1, (NK, 6)); self.activa[:NK] = True
        while not self._cond(): self.KW[0:NK] = _rh.uniform(0, 1, (NK - 0, 6))
        # EL NODO: exposiciones sin consecuencia por la VIA LENTA, relevancia viva (nodo_rel=1)
        if self._con and self._nodo:
            _msg = list(self._nodo)
            Wps, Wns = self.Wps, self.Wns
            _Pm9 = np.asarray([_z9[0] for _z9 in _msg], float); _Rm9 = np.asarray([_z9[1] for _z9 in _msg], float); _Nm9 = np.asarray([_z9[2] for _z9 in _msg], int)
            _rst9 = list(range(len(_msg))); _sel9 = []
            for _it9 in range(min(self.NODO_LEE, len(_msg))):
                _sc9 = np.abs(_Rm9[_rst9] - ((Wps[_Nm9[_rst9]] - Wns[_Nm9[_rst9]]) * _Pm9[_rst9]).sum(1))
                _b9 = int(np.lexsort((-np.asarray(_rst9, float), -_sc9))[0]); _sel9.append(_rst9[_b9])
                _P7, _R7, _n7 = _msg[_rst9.pop(_b9)]
                _Pv = np.asarray(_P7, float)
                if LAM: _mc7 = np.minimum(Wps[_n7], Wns[_n7]) * (_Pv > 0); Wps[_n7] = Wps[_n7] - LAM * _mc7; Wns[_n7] = Wns[_n7] - LAM * _mc7
                _ds7 = _R7 - float((Wps[_n7] - Wns[_n7]) @ _Pv)
                if _ds7 > 0: Wps[_n7] = np.clip(Wps[_n7] + ETA_S * _ds7 * _Pv, 0, CLIP_S)
                else:        Wns[_n7] = np.clip(Wns[_n7] + ETA_S * AVERSION * (-_ds7) * _Pv, 0, CLIP_S)
            self._nlec += 1
            self._ldiv += int(len(self._nodo) > self.NODO_LEE or (_sel9 != sorted(_sel9)))

    def salida(self):
        """Telemetria PROPIA del carro (va a d['carro'] -- ERR-96: el juez no la usa para puntuar). Identica a
        FABRICA + dos contadores de S1 (elecciones, evitados: cuantas veces la evitacion de disputa cambio el
        blanco elegido respecto al mas cercano de FABRICA)."""
        PATk = self.PAT; _nm = self._nm; kw = self.KW0
        W = {k: round(self._valor(PATk[k]), 2) for k in PATk}
        W_lenta = {k: round(float((self.Wps[_nm] - self.Wns[_nm]) @ PATk[k]), 3) for k in PATk}
        comp = {k: (round(float(self.Wp[_nm] @ self._kenyon(PATk[k])), 2), round(float(self.Wn[_nm] @ self._kenyon(PATk[k])), 2)) for k in PATk}
        return dict(
            sin_objetivo=self.sin_objetivo, memoria_rechazo=self.MEMORIA_RECHAZO, err_max=self.err_max, t_conflicto=self.t_conflicto,
            t_techo=self.t_techo, n_techo=self.n_techo, split_t=self.split_t, W=W, comp=comp, log=[], splits=self.splits,
            celdas=int(self.activa.sum()), puerta_pat=self.PUERTA_PAT, pat_shuf=kw['pat_shuf'], pat_min=self.PAT_MIN, n_cod=len(self.ncod),
            solap={'AB': len(self._code(PATk['A']) & self._code(PATk['B'])), 'nB': None}, W_lenta=W_lenta,
            Wps=[round(float(x), 3) for x in self.Wps[_nm]], Wns=[round(float(x), 3) for x in self.Wns[_nm]],
            n_nec=self.N_NEC,
            W_nec=[{_k3: round(self._vnec(_n, PATk[_k3], self._kenyon(PATk[_k3])), 2) for _k3 in PATk} for _n in range(self.N_NEC)],
            sorp_nec=[round(float(_x), 4) for _x in self._sbE],
            hereda=kw['hereda'], baraja_identidad=self._nbar,
            alma_muertes=self.ALMA_MUERTES, curitas=[list(_c) for _c in self._cur], nodo_n=len(self._nodo),
            conectado_final=int(self._con), dote_final=round(float(self.dote), 4), umbral_final=round(float(self.rep_umbral), 4),
            hereda_final=kw['hereda'], miedo_inerte=0,
            nodo_cola=[[list(_p7), float(_r7), int(_n7)] for _p7, _r7, _n7 in self._nodo[-60:]],
            alma_cfg=dict(nodo=int(kw['nodo']), nodo_k=self.NODO_K, nodo_lee=self.NODO_LEE, miedo_n=kw['miedo_n'], miedo_R=kw['miedo_R'],
                          d_dote=kw['d_dote'], d_umbral=kw['d_umbral'], conectado_ini=int(kw['conectado'])),
            alma2=dict(menu=''.join(kw['menu']), nodo_baraja=int(kw['nodo_baraja']), baraja_nodo_identidad=0, sem_baraja_nodo='860000+1000000*seed'),
            f9=dict(nodo_rel=int(kw['nodo_rel']), con_desde=int(kw['con_desde']), lect_div=int(self._ldiv), lecturas=int(self._nlec),
                    sem_rel='870000+1000000*seed', con_cuerpo=[int(_x) for _x in self._ncu], pa=int(self._gpa), pn=int(self._gpn)),
            _rep_cuello=int(kw['rep_cuello']),
            # --- S1: telemetria propia de la evitacion de disputa (solo lectura) ---
            s1_evita=dict(elecciones=int(self._elecciones), evitados=int(self._evitados)))


def crea(ctx):
    return Carro(ctx)
