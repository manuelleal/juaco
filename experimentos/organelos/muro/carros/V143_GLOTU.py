"""V143_GLOTU.py — muro: V143 + UNA pieza local del bloque MURO (la de sus perillas; ver construye_muro.py). Cero memoria nueva.
GENERADO por experimentos/organelos/muro/construye_muro.py desde tronco_v14_3/carros_v143/V143.py (sha 2a03048a7f1525e5).
NO editar a mano. Perillas: PAGA = 0; GLOT = 3; PATAS = 0; TELEM = 1. Con PAGA = GLOT = PATAS = TELEM = 0 es V143 bit a bit. Sigue el docstring de V143.

V143.py — tronco_v14_3 (candidato a tronco v14.3): FABRICA + B-5 + FILTRO con META + boca TD de APR.
GENERADO por experimentos/tronco_v14_3/construye_v143.py desde carros/APR.py (sha 4402aa5142065c72). NO editar a mano.
Perillas: DESAMB 1 FILTRO 1 META 1 INVIERTE 0 OPCION 1. Con DESAMB = FILTRO = OPCION = 0 es FABRICA bit a bit. Sigue el docstring de APR.

carros/APR.py — APR (camino A, experimentos/aprende_barrer): FABRICA + la OPCION APRENDIDA de morder lo malo conocido.
GENERADO por experimentos/aprende_barrer/construye_apr.py desde carros/FABRICA.py (sha 2ebee3e99ea5a33a). NO editar a mano.
MODO aprende. Con OPCION = 0 es FABRICA bit a bit (identidad_apr.py). Lo que sigue es el docstring de FABRICA.

carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.

Es la MITAD CEREBRO del brazo REL de experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py (sha fijado en
pista.SHA_F9C; aqui solo se LEYO): CUELLO_MIN + MED2 + h1 + muerte_real=1 + hereda='nada' + dote=0.6 +
alma nula (curita 'f') + nodo=1, conectado=1, nodo_rel=1 (relevancia viva), nodo_k=20, nodo_lee=50, f9=1, f9c=1.
La otra mitad (el MUNDO) vive en pista.py. Con UN carro, pizarra apagada y compat=1 la pista + este carro
reproducen organismo_f9c.run(**REL) BIT A BIT (arnes: identidad_pista.py).

H-4: NINGUNA constante escrita a mano. Todas salen de ctx['fabrica'] (pista.cfg_fabrica(): firma de
organismo_f9c.run + corre_bloque2.BRAZOS['REL'] + L/NK/NKMAX/K/PAT del monolito, resueltos en tiempo de
ejecucion). Las lineas son las del monolito SOLO en las ramas vivas del brazo REL; si una perilla de rama no
tiene el valor portado, crea() ABORTA (RAMAS) en vez de correr otra cosa en silencio.

ENMIENDA 1, OPCION A (REGLAMENTO, decision del coordinador tras ERR-97): el anillo es el de la PISTA (ctx['L'],
= 40 con N = 1 -> identico al monolito) y el carro sigue viendo TODOS los objetos (see() busca el mas cercano
sobre el anillo entero). Con N = 9 (L = 360, 36 objetos) puede ir a un objeto a mas de 20 celdas, cosa imposible
en L = 40: la pista mide esa fraccion de pasos (diag 'frac_sin_obj20').

INTERFAZ DE CARRO (la misma para las nueve escuderias):
  crea(ctx) -> objeto con
    actua(obs)       -> dict(mov in {-1,0,1}, muerde: bool, escribe: None | tupla de <= ANCHO numeros)
    resultado(res)   -> None      (consecuencia de ESTE paso: si mordio, que letra y el dS nominal)
    fin_paso(info)   -> None      (olvidos del mundo en este paso)
    muere(info)      -> None      (el cuerpo en curso murio: causa, edad, hijos)
    nace(info)       -> None      (nace el siguiente cuerpo: memoria del padre o None si es fundador; rng_hijo)
    al_parir(info)   -> memoria   (lo que se lleva el hijo; la pista la guarda opaca en la cola con la dote)
    [opcional] quiere_parir(info) -> bool   (vetar/posponer el parto de ESTA ventana; por defecto True)
    [opcional] valor_nec(n, letra) -> float (SOLO LECTURA para la telemetria exp_hasta del juez)
    [opcional] salida() -> dict   (telemetria PROPIA: va a d['carro'], el juez NO la usa para puntuar; ERR-96)
"""
import numpy as np

# perillas que eligen RAMA en el monolito -> el valor que este archivo porta (si difiere, crea() aborta).
# rep_acum NO esta: es perilla del MUNDO (la aplica la pista).
RAMAS = dict(vivo=1, n_nec=2, rep_cuello=2, puerta=3, puerta_pat=5, pat_shuf=0, mask_rel=2, div_signo=True,
             mu_norm=True, eta_pred=0.0, k_sorp=0.0, sesgo_fijo=0.0, nodo_via=0, nodo_or=0, nodo_baraja=0,
             con_desde=0, nodo_rel=1, nodo=1, conectado=1, hereda='nada', learn=True, plast=True, val_esc=0,
             nec_shuf=0, rep_nec=0, hereda_nec=1, solap_AB=None, nuevo=None, invertir_en=None, log_cada=None,
             tabla=None, f9=1, f9c=1, muerte_real=1, h1=1, rep2=1, reproduccion=1, rep_mide=1,
             menu='f', alma_curita='f')
# ================================================================ APR (camino A, aprende_barrer) -- constantes
# OPCION = 0 -> este archivo es FABRICA bit a bit (arnes identidad_apr.py). MODO y P_AZAR son lo UNICO que cambia
# entre APR, APR_SIN_HERENCIA y APR_AZAR. ALFA_Q, GAMMA, BETA, R_*: hiperparametros del aprendizaje (NO umbrales de cuando
# limpiar; la decision sale de Q aprendido). Historia (PREREGISTRO_aprende.md): v1 humo 8001, v2 humo 8002 (GAMMA 0.99 -> 0.998,
# recompensa real, rasgo de ventana), v3 humo 8003 (la opcion CORRIGE la boca de FABRICA en vez de reemplazarla). Desde v3,
# congelados hasta la serie (v3 + telemetria de quitadas por edad / indice del cuerpo, sin tocar la conducta).
OPCION = 1
MODO = 'aprende'
P_AZAR = None
ALFA_Q = 0.05      # paso del aprendizaje TD de los dos valores lineales Q(no morder), Q(morder)
GAMMA = 0.998      # descuento POR PASO (horizonte ~500 pasos = la ventana de parto)
BETA = 10.0        # temperatura de la politica: p(morder) = sigmoide(BETA * (Q_morder - Q_no))
R_PARTO = 1.0      # v2: recompensa REAL sentida: +1 cuando el cuerpo pare (al_parir), -1 cuando muere (terminal):
R_MUERTE = -1.0    #     el retorno sigue (nacimientos - muertes), la misma cantidad que mide H-1 (r = desc - muertes)
NF = 6             # rasgos: [1, u=min(E,Ag), u tras morder (con lo SENTIDO de esa letra), 0 bueno en el mundo, distancia al bueno,
                   #          progreso propio en la ventana de parto (pasos seguidos con E y Ag >= umbral / rep_X)]
BIN_EDAD = (50, 100, 200, 400, 800, 1600)          # edad del cuerpo al decidir (pasos desde que nacio)
BIN_GEN = (1, 5, 20, 50, 100, 200, 400)             # indice del cuerpo dentro del linaje (0 = el primero)
BIN_POST = (0.0, 0.3, 0.6, 1.0)                     # min(E,Ag) PREDICHO tras morder
# ================================================================ tronco_v14_3 (candidato v14.3) -- perillas
# Con DESAMB = FILTRO = OPCION = 0 este archivo es FABRICA bit a bit (arnes experimentos/tronco_v14_3/identidad_v143.py).
# DESAMB: B-5 de v14.2 (literal de organismo/organismo_v142.py, port de dos necesidades de creacion_B/organismo_vivo_codigo.py).
# FILTRO: pieza 1 (subida_n6): lo recordado como malo en alguna fila no es objetivo ni se muerde, SOLO con META (algo a la vista
#         con valor > 0 en la fila activa). META = 0: actua siempre (lesion). INVIERTE = 1: lee la letra pareja (control).
DESAMB = 1; FILTRO = 1; META = 1; INVIERTE = 0   # tronco_v14_3: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (con OPCION)
PAGA = 0; GLOT = 3; PATAS = 0; TELEM = 1   # muro: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0/0/0/0 = V143 bit a bit)
PAREJA = {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'}   # solo para INVIERTE (control de contenido)
CACHE = 1   # tras el humo: las dos filas por letra solo cambian al morder o al nacer -> se guardan hasta entonces (arnes: CACHE 0 == 1 bit a bit)


class Carro:
    def __init__(self, ctx):
        cf = ctx['fabrica']; kw = cf['kw']
        mal = {k: (kw.get(k), v) for k, v in RAMAS.items() if kw.get(k) != v}
        if mal: raise SystemExit(f"FABRICA: ramas no portadas {mal}")
        self.L = ctx['L']   # OPCION A (ERR-97, decision del coordinador): L de la pista; sigue viendo el mundo ENTERO
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
        self.Wpe = np.zeros((N_NEC, 6)); self.Wke = np.zeros((N_NEC, NKMAX)); self._sbE = np.zeros(N_NEC)
        self._nodo = []; self._cur = []; self._mordh = []; self._con = True; self._nmu = 0
        self._ldiv = 0; self._nlec = 0; self._gpa = 0; self._gpn = 0; self._ncu = []; self._nbar = 0
        self.ncod = {}; self._ord = []
        self.mup = np.zeros((NKMAX, 6)); self.mun = np.zeros((NKMAX, 6)); self.zp = np.zeros(NKMAX); self.zn = np.zeros(NKMAX)
        self.err_max = 0.0; self.t_conflicto = None; self.t_techo = None; self.n_techo = 0
        self._rech = {}
        self.sin_objetivo = [0] * 4
        self.split_t = []
        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = None
        self._apr_init(ctx)
        self._v3_init(ctx)
        self._pg_init(ctx)   # muro: solo estado propio y contadores (sin rng)

    # ------------------------------------------------------------ piezas del monolito
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

    def _see(self, pos, objs, t, contar=False):
        L = self.L; best = None
        _pq = bool(PATAS and FILTRO and self._v3m and any(self._pg_sirve(_k) for _k in set(objs.values())))   # muro PATAS
        if _pq and contar and TELEM: self._pg["patas_meta"] += 1
        for x, k in objs.items():
            if self.MEMORIA_RECHAZO and self._rech.get(x, -1) > t: continue
            if FILTRO and k in self._v3o: continue   # tronco_v14_3 FILTRO (subida_n6): lo recordado malo no es objetivo
            if _pq and not self._pg_sirve(k): continue   # muro PATAS: con meta, solo lo que sirve (1: a la activa; 2: a la otra)
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
            if best is None or d < best[0]: best = (d, k, dl < dr)
        if best is None:
            if contar: self.sin_objetivo[self._q(t)] += 1
            for x, k in objs.items():
                if FILTRO and k in self._v3o: continue   # tronco_v14_3: tampoco en el fallback (n6)
                dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
                if best is None or d < best[0]: best = (d, k, dl < dr)
        if best is None and FILTRO:   # tronco_v14_3: TODO es obstaculo (solo posible con META = 0): las patas vuelven a lo mas cercano
            self._v3['todo_obst'] += 1   # (la boca sigue vetando; lo hallo el arnes (7e) antes del humo)
            for x, k in objs.items():
                dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
                if best is None or d < best[0]: best = (d, k, dl < dr)
        return best

    # ------------------------------------------------------------ INTERFAZ
    def valor_nec(self, n, letra):
        """SOLO LECTURA (la usa la telemetria exp_hasta de la pista, antes de resultado())."""
        return self._vnec(n, self.PAT[letra], self._kenyon(self.PAT[letra]))

    def actua(self, obs):
        PAT = self.PAT
        t = obs['t']; pos = obs['pos']; E = obs['E']; Ag = obs['Ag']; objs = obs['objs']; rng = self.rng
        if OPCION: self._apr_paso(E, Ag)
        hambre = np.clip(1 - E, 0, 1)
        _dfa = np.clip(1 - Ag, 0, 1); self._na = _na = 1 if _dfa > hambre else 0
        if _na: hambre = _dfa
        _cue2 = bool(hambre == 0 and _dfa == 0)   # rep_cuello == 2 (RAMAS)
        self._nm = _na
        if PAGA or GLOT or TELEM: self._pg_lev = (float(E), float(Ag))   # muro: estado presente (solo lectura)
        if FILTRO: self._v3_prep(objs, _na)
        d, k, left = self._see(pos, objs, t, contar=True); pat = PAT[k]
        x = np.concatenate([pat * 1.2, [1.5 if left else 0, 0 if left else 1.5, 1.0 if d == 0 else 0.]]); noise = .15 + .5 * hambre
        V = self.Wl @ x; p = 1 / (1 + np.exp(-(V - .8) / noise)); u = p + rng.normal(0, .3, 2); m = np.zeros(2)
        if u.max() > .5: m[np.argmax(u)] = 1
        self.tr = self.tr * .7 + x
        self.el = self.el * self.TAU_E + np.outer(m - p, self.tr)
        mov = int(m[1] - m[0]); pos = (pos + mov) % self.L; d2, _, _ = self._see(pos, objs, t); Rp = .2 if d2 < d else 0.
        self._R = 0.; self._Rp = Rp; self._hambre = hambre; self._enc = None
        mordio = False
        if pos in objs:
            kk = objs[pos]; kc = self._kenyon(PAT[kk]); Wb = self.Wp[self._nm] - self.Wn[self._nm]; _wf = float(Wb @ kc); _ws = float((self.Wps[self._nm] - self.Wns[self._nm]) @ PAT[kk])
            _fa9 = bool(self._fam(kc))   # puerta is not None (RAMAS)
            _wt = (_wf if _fa9 else _ws)
            self._gpn += 1; self._gpa += int(_fa9)
            if _cue2: _wt = min(_wt, self._vnec(1 - _na, PAT[kk], kc))
            Vb = self.ALPHA * _wt + self.HAMBRE_BOCA * hambre + .5
            pb = 1 / (1 + np.exp(-Vb / .3)); _u9 = rng.random(); mordio = bool(_u9 < pb)
            if PAGA or GLOT or TELEM: self._pg_boca(kk, mordio)   # muro: telemetria (solo lectura)
            if FILTRO and kk in (self._pgv if (PAGA or GLOT) else self._v3o):   # tronco_v14_3 FILTRO / muro: veto (mismo sorteo consumido)
                self._v3['vetos'] += int(mordio); mordio = False
            elif OPCION: mordio = self._opcion(obs, kk, mordio, _u9, pb)
            if (PAGA or GLOT or TELEM) and mordio: self._pg_mord(kk)   # muro: telemetria (solo lectura)
            if FILTRO and mordio and not self._v3m:
                self._v3['mord_sin_meta'] += 1; self._v3['limpia_propia'] += int(min(self._v3v[kk]) < 0)
            if self.MEMORIA_RECHAZO and not mordio: self._rech[pos] = t + self.MEMORIA_RECHAZO
            self._enc = (pos, kk, kc, Wb, _wf, _ws)
        return dict(mov=mov, muerde=mordio, escribe=None)

    def resultado(self, res):
        """res: t, pos, letra, mordio, dS (nominal, solo si mordio). Aprendizaje de la mordida (sin rng)."""
        if res['mordio']: self._v3c = None   # tronco_v14_3 CACHE: morder cambia las filas
        if OPCION and res['mordio']: self._apr_dS(res['letra'], res['dS'])
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
            if (Wb[c] * R < 0 or (DESAMB and R == 0)) and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(KW[c] @ P) and (~activa).any():   # B-5 (v14.2)
                j = int(np.where(~activa)[0][0]); activa[j] = True; KW[j] = kj
                if R > 0: Wp[_nm, j] = Wp[_nm, c]; Wn[_nm, j] = 0.; Wp[_nm, c] = 0.
                elif R < 0: Wn[_nm, j] = Wn[_nm, c]; Wp[_nm, j] = 0.; Wn[_nm, c] = 0.
                else:   # B-5: con R == 0 la hija nace SIN valor en la necesidad activa (hereda las otras abajo); la madre conserva
                    Wp[_nm, j] = 0.; Wn[_nm, j] = 0.; self._v3['des_splits'] += 1
                    if len(self._v3['des_t']) < 200: self._v3['des_t'].append((int(t), kk, int(_nm)))
                for _n in range(N_NEC):
                    if _n != _nm: Wp[_n, j] = Wp[_n, c]; Wn[_n, j] = Wn[_n, c]
                mu[j] = P * (float(mu[c].sum()) / P.sum()); err[c] = err[j] = 0; self.splits += 1; self.split_t.append((t, kk))
                mup[j] = mup[c].copy(); mun[j] = mun[c].copy(); zp[j] = zp[c]; zn[j] = zn[c]

    def fin_paso(self, info):
        for _dx in info['olvido']: self._rech.pop(_dx, None)
        self.Wl = np.clip(self.Wl + self.ETA * (1 + 2 * self._hambre) * (max(self._R, 0) + self._Rp) * self.el, 0, 1.5)

    def muere(self, info):
        """El alma NULA del brazo REL (curita 'f') + el NODO que se llena con las ultimas nodo_k mordidas."""
        self._nmu += 1
        if OPCION: self._apr_muere(info)
        for _t9, _k9, _n9, _R9 in self._mordh[-self.NODO_K:]: self._nodo.append([[float(_z9) for _z9 in self.PAT[_k9]], float(_R9), int(_n9)])
        self._cur.append([self._nmu, self.KW0['alma_curita'], self.MOTIVO[:240], round(float(self.dote), 4), round(float(self.rep_umbral), 4),
                          self.KW0['hereda'], int(self._con), len(self._nodo), info['causa'], int(info['edad']), int(info['hijos'])])
        self._ncu.append(int(self._con))
        self._mordh.clear()

    def al_parir(self, info):
        if OPCION: self._areal += R_PARTO; self._avent = 0   # APR v2: parir se SIENTE (+1)
        return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)

    def nace(self, info):
        NK = self.NK; ETA_S = self.ETA_S; AVERSION = self.AVERSION; LAM = self.LAM; CLIP_S = self.CLIP_S
        _rh = info['rng_hijo']
        if OPCION: self._apr_nace(info)
        self._v3c = None   # tronco_v14_3 CACHE: nacer reinicia las filas
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

    # ================================================================ APR (camino A): LA OPCION APRENDIDA
    # Alcance de la opcion: SOLO cuando el cuerpo esta sobre una letra "mala conocida" (el linaje ya la mordio y lo que
    # SINTIO -el dS que la pista devuelve en resultado()- tiene alguna componente negativa). Ahi decide la opcion (v3):
    # logit p(morder) = logit(pb de la boca de FABRICA) + BETA * (Q1 - Q0), con el MISMO uniforme que FABRICA ya saco
    # (ningun sorteo extra). Con Q1 = Q0 (al nacer el linaje) muerde EXACTAMENTE cuando FABRICA morderia: lo aprendido
    # es solo la CORRECCION, en los dos sentidos (morder mas = limpiar; morder menos = contenerse). v2 reemplazaba la
    # boca (p = sigmoide(BETA * (Q1 - Q0)), 0.5 al nacer) y en el humo 8002 rompio la ventana de parto (R0 0.005).
    # Q lineal en rasgos que el cuerpo siente. Q se aprende por TD (SARSA esperado, semi-Markov entre decisiones) con la recompensa SENTIDA (v2):
    # +R_PARTO cuando pare y R_MUERTE cuando muere (terminal), mas moldeo por potencial con u = min(E, Ag) (no cambia la
    # politica optima; solo acelera). v1 (solo el cambio de u, sin recompensa real) aprendio al reves en el humo 8001:
    # mordia MAS cuanto mas cerca de morir (retorno sin objetivo real). Ninguna regla dice "si esta lleno y
    # no hay nada util, limpia": eso solo puede salir de los pesos aprendidos.
    # Herencia (DECLARADA, el mismo camino que el nodo de FABRICA): Q y la memoria de letras viven en el carro (el
    # cerebro del linaje) y pasan al cuerpo siguiente del linaje (hijo de la cola o fundador). MODO 'sin_herencia': cada
    # cuerpo nuevo empieza con Q = 0 (la memoria de letras SI pasa: es lo que el linaje sabe de las letras, no de limpiar).
    # Prohibido y no usado: el rng de la pista y la tabla verdadera de valencias que viaja en ctx['fabrica'].
    def _apr_init(self, ctx):
        if OPCION and MODO not in ('aprende', 'sin_herencia', 'azar'): raise SystemExit(f"APR: MODO invalido {MODO!r}")
        if OPCION and MODO == 'azar' and P_AZAR is None: raise SystemExit("APR_AZAR: P_AZAR sin fijar (construye_apr.py --p_azar)")
        self._aL = int(ctx['L'])
        self._adS = {}                       # letra -> [suma dE sentido, suma dAg sentido, mordidas] (del LINAJE)
        self._aw = np.zeros((2, NF))         # Q lineal: fila 0 = no morder, fila 1 = morder
        self._apend = None; self._areal = 0.0; self._anace = 0; self._agen = 0; self._avent = 0
        self._aU = float(ctx['rep_umbral']); self._aX = float(ctx['rep_X'])
        z = lambda n: [0] * n
        self._ast = dict(opp_edad=z(len(BIN_EDAD) + 1), mord_edad=z(len(BIN_EDAD) + 1),
                         opp_gen=z(len(BIN_GEN) + 1), mord_gen=z(len(BIN_GEN) + 1),
                         opp_q=z(4), mord_q=z(4), opp_g0=z(2), mord_g0=z(2),
                         opp_post=[z(len(BIN_POST) + 1) for _ in range(2)], mord_post=[z(len(BIN_POST) + 1) for _ in range(2)],
                         anad_q=z(4), quit_q=z(4), anad_g0=z(2), quit_g0=z(2), anad_edad=z(len(BIN_EDAD) + 1), anad_gen=z(len(BIN_GEN) + 1),
                         quit_edad=z(len(BIN_EDAD) + 1), quit_gen=z(len(BIN_GEN) + 1),
                         fab_mord=0, ambas=0, td_n=0, td_abs=0.0, terminales=0, suma_p=0.0, cuerpos=1)

    def _apr_dS(self, k, dS):
        m = self._adS.setdefault(k, [0.0, 0.0, 0])
        m[0] += float(dS[0]); m[1] += float(dS[1]); m[2] += 1

    def _apr_paso(self, E, Ag):
        self._avent = self._avent + 1 if (E >= self._aU and Ag >= self._aU) else 0   # lo que el cuerpo siente de su saciedad

    def _apr_q(self, phi):
        q = self._aw @ phi
        return q, float(1.0 / (1.0 + np.exp(-BETA * (q[1] - q[0]))))

    def _apr_td(self, y):
        phi0, a0 = self._apend[0], self._apend[1]
        d = y - float(self._aw[a0] @ phi0)
        self._aw[a0] = self._aw[a0] + ALFA_Q * d * phi0
        self._ast['td_n'] += 1; self._ast['td_abs'] += abs(d)

    def _opcion(self, obs, kk, mf, u9, pb):
        m = self._adS.get(kk)
        if m is None or not (m[0] < 0 or m[1] < 0): return mf        # no es MALO CONOCIDO: decide la boca de FABRICA
        t = int(obs['t']); pos = obs['pos']; E = float(obs['E']); Ag = float(obs['Ag']); u = min(E, Ag)
        na = self._na
        buenas = {k for k, z in self._adS.items() if z[na] / z[2] > 0}   # lo que el linaje SINTIO bueno para la necesidad activa
        dmin = None; L = self._aL
        for x, k in obs['objs'].items():
            if x != pos and k in buenas:
                d = min((pos - x) % L, (x - pos) % L)
                if dmin is None or d < dmin: dmin = d
        g0 = 1.0 if dmin is None else 0.0
        post = min(E + m[0] / m[2], Ag + m[1] / m[2])
        phi = np.array([1.0, u, post, g0, (1.0 if dmin is None else dmin / (L / 2.0)), min(self._avent / self._aX, 1.0)])
        q, _ = self._apr_q(phi)
        if MODO == 'azar': p = float(P_AZAR)
        elif q[1] == q[0]: p = float(pb)
        else:
            pc = min(max(float(pb), 1e-12), 1 - 1e-12)
            p = float(1.0 / (1.0 + np.exp(-(np.log(pc / (1 - pc)) + BETA * (q[1] - q[0])))))
        if self._apend is not None:          # cierra la decision anterior (semi-Markov, SARSA esperado):
            g = GAMMA ** (t - self._apend[3])  # y = recompensa real + [g*u - u0] (moldeo por potencial u) + g * V(phi)
            y = self._areal + (g * u - self._apend[2]) + g * (p * float(q[1]) + (1 - p) * float(q[0]))
            self._apr_td(y)
        self._areal = 0.0
        b = bool(mf) if (MODO != 'azar' and q[1] == q[0]) else bool(u9 < p)   # el uniforme de FABRICA: con Q1 = Q0, b = mf
        self._apend = (phi, int(b), u, t)
        st = self._ast; ib = int(b)
        e = t - self._anace
        ie = sum(1 for c in BIN_EDAD if e >= c); ig = sum(1 for c in BIN_GEN if self._agen >= c); ip = sum(1 for c in BIN_POST if post >= c)
        st['opp_edad'][ie] += 1; st['mord_edad'][ie] += ib; st['opp_gen'][ig] += 1; st['mord_gen'][ig] += ib
        qq = self._q(t); st['opp_q'][qq] += 1; st['mord_q'][qq] += ib
        st['opp_g0'][int(g0)] += 1; st['mord_g0'][int(g0)] += ib
        st['opp_post'][int(g0)][ip] += 1; st['mord_post'][int(g0)][ip] += ib
        an = int(b and not mf); qu = int(mf and not b)   # anadida (morderia FABRICA? no; APR si) / quitada (FABRICA si; APR no)
        st['anad_q'][qq] += an; st['quit_q'][qq] += qu; st['anad_g0'][int(g0)] += an; st['quit_g0'][int(g0)] += qu
        st['anad_edad'][ie] += an; st['anad_gen'][ig] += an; st['quit_edad'][ie] += qu; st['quit_gen'][ig] += qu
        st['fab_mord'] += int(mf); st['ambas'] += int(mf and b); st['suma_p'] += p
        return b

    def _apr_muere(self, info):
        if self._apend is not None:          # terminal: el cuerpo murio antes de la siguiente decision (potencial final 0)
            self._apr_td(self._areal + R_MUERTE - self._apend[2]); self._ast['terminales'] += 1
        self._apend = None; self._areal = 0.0; self._avent = 0

    def _apr_nace(self, info):
        self._apend = None; self._areal = 0.0; self._avent = 0; self._anace = int(info['t']); self._agen += 1; self._ast['cuerpos'] += 1
        if MODO == 'sin_herencia': self._aw[:] = 0.0

    def _apr_salida(self):
        grid = {}
        for g0 in (0, 1):
            for post in (-0.2, 0.1, 0.4, 0.8, 1.2):
                u = min(1.4, post + 0.4)
                q = self._apr_q(np.array([1.0, u, post, float(g0), (1.0 if g0 else 0.15), 0.0]))[0]
                grid[f"g0={g0} post={post}"] = round(BETA * float(q[1] - q[0]), 3)   # CORRECCION al logit de la boca de FABRICA
        st = dict(self._ast); st['td_abs'] = round(st['td_abs'], 4); st['suma_p'] = round(st['suma_p'], 4)
        return dict(modo=MODO, p_azar=P_AZAR, alfa=ALFA_Q, gamma=GAMMA, beta=BETA, r_parto=R_PARTO, r_muerte=R_MUERTE, bin_edad=list(BIN_EDAD), bin_gen=list(BIN_GEN),
                    bin_post=list(BIN_POST), w=[[round(float(v), 4) for v in f] for f in self._aw], politica=grid,
                    letras={k: [round(z[0] / z[2], 3), round(z[1] / z[2], 3), int(z[2])] for k, z in sorted(self._adS.items())}, **st)

    # ================================================================ tronco_v14_3: PIEZA 1 (FILTRO con META) y telemetria
    # Lee SOLO las dos filas de valor del propio organismo (_vnec: via rapida si el codigo es familiar, via lenta si no; la
    # misma lectura que usa la boca). Nada del mundo que el cuerpo no vea: la pista ya le entrega los objetos a la vista.
    def _v3_init(self, ctx):
        self._v3o = frozenset()          # letras que HOY son obstaculo (se recalcula cada paso; no persiste)
        self._v3m = False                # hay meta a la vista en este paso
        self._v3c = None                 # CACHE de las dos filas por letra (se invalida al morder y al nacer)
        self._v3 = dict(pasos=0, pasos_meta=0, vetos=0, limpia_propia=0, mord_sin_meta=0, todo_obst=0, des_splits=0, des_t=[])

    def _v3_prep(self, objs, na):
        PAT = self.PAT
        if CACHE and self._v3c is not None: v = self._v3c
        else:
            v = {}
            for k in PAT:
                kr = PAREJA[k] if INVIERTE else k
                kc = self._kenyon(PAT[kr])
                v[k] = (self._vnec(0, PAT[kr], kc), self._vnec(1, PAT[kr], kc))
            if CACHE: self._v3c = v
        letras = set(objs.values())
        meta = any(v[k][na] > 0 for k in letras)
        self._v3m = meta
        self._v3v = v
        if meta or not META: self._v3o = frozenset(k for k in PAT if v[k][na] <= 0 and min(v[k]) < 0)
        else: self._v3o = frozenset()
        if PAGA or GLOT or TELEM: self._pg_prep(v, na, meta)   # muro (con PAGA = GLOT = 0 solo lee: veto = _v3o)
        self._v3['pasos'] += 1; self._v3['pasos_meta'] += int(meta)

    def _v3_salida(self):
        st = dict(self._v3); st['des_t'] = list(self._v3['des_t'][:200])
        return dict(desamb=DESAMB, filtro=FILTRO, meta=META, invierte=INVIERTE, opcion=OPCION, **st)

    def salida(self):
        """Telemetria PROPIA del carro (va a d['carro'] -- ERR-96: el juez no la usa para puntuar)."""
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
            _rep_cuello=int(kw['rep_cuello']), **({'apr': self._apr_salida()} if OPCION else {}),
            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {}),
            **({'muro': self._pg_salida()} if (PAGA or GLOT or TELEM) else {}))   # muro: telemetria (ERR-96: no puntua)

    # ================================================================ muro: CTA ("no vuelvas a morder lo que te hizo dano en lo que mas te falta")
    # Lee lo SENTIDO por el linaje (_adS) y el estado presente. Solo la boca, solo sin meta (PAGA 2: tambien limpieza con meta). Sin rng.
    def _pg_init(self, ctx):
        self._pg_lev = (1.0, 1.0); self._pgv = frozenset(); self._pg_act = frozenset(); self._pg_otra = frozenset(); self._pg_nop = frozenset()
        self._pg_glot = frozenset()
        self._pg = dict(pasos=0, sin_meta=0, veto_act=0, veto_otra=0, libera=0, mord_act=0, mord_otra_paga=0, mord_otra_nopaga=0,
                        mord_act_sinmeta=0, mord_otra_sinmeta=0, veto_glot=0, mord_solo_otra=0, patas_meta=0, patas_cambia=0)

    def _pg_prep(self, v, na, meta):
        lev = self._pg_lev; o = 1 - na; act = set(); otra = set(); nop = set(); glot = set()
        for k, m in self._adS.items():
            if m[2] <= 0: continue
            s0 = m[na] / m[2]; s1 = m[o] / m[2]
            if GLOT in (3, 4):   # GLOTU: por NIVELES (j = la necesidad que la letra sube, sola)
                e0 = m[0] / m[2]; e1 = m[1] / m[2]
                j = 0 if (e0 > 0 and e1 <= 0) else (1 if (e1 > 0 and e0 <= 0) else None)
                if j is not None and lev[j] >= self._aU and ((lev[j] > lev[1 - j]) if GLOT == 3 else (lev[j] < lev[1 - j])): glot.add(k)
            elif s1 > 0 and s0 <= 0: glot.add(k)   # lo SENTIDO solo sirve a la necesidad que no es la activa
            if s0 < 0: act.add(k)
            elif s1 < 0:
                otra.add(k)
                if lev[o] + s1 < lev[na]: nop.add(k)
        act = frozenset(act); otra = frozenset(otra); nop = frozenset(nop)
        self._pg_act = act; self._pg_otra = otra; self._pg_nop = nop
        if PAGA == 0: veto = self._v3o
        elif meta: veto = (self._v3o - (otra - nop)) if PAGA == 2 else self._v3o
        elif PAGA == 1 or PAGA == 2: veto = act | nop
        elif PAGA == 3: veto = act | otra
        else: veto = otra
        if GLOT == 2: glot = set(k for k in self.PAT if v[k][o] > 0 and v[k][na] <= 0)   # control: las FILAS (generalizan)
        self._pg_glot = frozenset(glot)
        if GLOT: veto = veto | self._pg_glot
        self._pgv = veto
        if TELEM: self._pg['pasos'] += 1; self._pg['sin_meta'] += int(not meta)

    def _pg_boca(self, kk, mordio_fab):
        if not TELEM: return
        g = self._pg
        if kk in self._pgv and kk not in self._v3o and mordio_fab: g['veto_act' if kk in self._pg_act else 'veto_otra'] += 1
        if kk in self._v3o and kk not in self._pgv and mordio_fab: g['libera'] += 1
        if GLOT and kk in self._pg_glot and kk not in self._v3o and mordio_fab: g['veto_glot'] += 1

    def _pg_mord(self, kk):
        if not TELEM: return
        g = self._pg; sm = not self._v3m
        if kk in self._pg_glot: g['mord_solo_otra'] += 1
        if kk in self._pg_act: g['mord_act'] += 1; g['mord_act_sinmeta'] += int(sm)
        elif kk in self._pg_otra:
            g['mord_otra_nopaga' if kk in self._pg_nop else 'mord_otra_paga'] += 1; g['mord_otra_sinmeta'] += int(sm)

    def _pg_salida(self):
        return dict(paga=PAGA, glot=GLOT, patas=PATAS, telem=TELEM, **self._pg)

    def _pg_sirve(self, k):
        """PATAS: la letra k es objetivo si, con meta, tiene valor > 0 en la fila activa (1) o en la de la otra necesidad (2, control)."""
        n = self._na if PATAS == 1 else 1 - self._na
        return self._v3v[k][n] > 0


def crea(ctx):
    return Carro(ctx)
