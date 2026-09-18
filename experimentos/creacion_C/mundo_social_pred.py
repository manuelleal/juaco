"""mundo_social_pred = experimentos/etapa5_comunicacion/mundo_social_n3.py (ef227f833c5bf46a) + N2 POR PREDICCION:
el receptor aprende que va a SENTIR a partir de la CONDUCTA VISIBLE del emisor (u[c], regla delta sobre su propia
dE al morder) y con eso aprende el valor de un objeto SIN morderlo. Con eta_sym=0, gamma_pred=0 y theta_a=0 es
mundo_social_n3 EXACTO. Mide exposiciones y mordidas del receptor hasta criterio (solo lectura).
Generado por experimentos/creacion_C/construye_n2pred.py. NO editar. RAMA de creacion: no es tronco.
"""
"""
mundo_social.py — N organismos v9 en el MISMO anillo, compartiendo los objetos. Etapa 5 (comunicación), nivel N1.

Cada organismo es v9 (organismo/organismo_v9.py, d3b72fb8819fbe8e) línea por línea: patas R-STDP, boca con valor +
hambre, canales Wp/Wn con drenaje (lam=0.05), plasticidad 2L, memoria de trabajo de rechazo. El mundo (objetos,
reposición, retirada aleatoria) es compartido.

SEÑAL (N1, apagada por defecto): al morder, el organismo emite placer (+) o asco (−) según el resultado. Los demás
organismos a distancia de anillo <= d_senal ven (patrón mordido, signo) y actualizan SU PROPIO valor de ese patrón con
Rescorla-Wagner vicario (tasa eta*f_vicaria, con drenaje, sin comer, sin energía, sin divisiones). El signo se mapea a
la escala innata (+ -> +1, − -> −3). Nunca se transmiten pesos ni códigos: cada receptor usa SU código Kenyon.
  senal=None       sin señal (N0 si hay 2 o más organismos)
  senal='honesta'  N1
  senal='barajada' mismo número de señales, signo al azar (RNG propio seed_mundo+300000): control de contenido

RNG: un generador por organismo (patas, boca, sorteo de Kenyon, reaparición al morir) y uno del mundo (reposición y
retirada). Con n=1 y compat=True el mundo usa EL MISMO generador que el organismo, en el mismo orden de llamadas que v9:
con n=1 y senal=None el resultado es bit a bit el de organismo_v9.run(seed) (control de identidad).
Orden dentro de cada paso: fase A de cada organismo (percibir, mover, morder, aprender, gastar energía) -> entrega de
señales -> retirada aleatoria del mundo -> fase B de cada organismo (aprendizaje de patas, muerte). Con n>=2 el orden
de los organismos alterna por paridad del paso.
"""
import numpy as np

L = 40; NK = 30; NKMAX = 90; K = 3
PAT = {'A': np.array([1, 1, 0, 1, 0, 0.]), 'B': np.array([1, 0, 1, 0, 1, 0.]),
       'C': np.array([0, 1, 1, 0, 0, 1.]), 'D': np.array([0, 0, 1, 0, 1, 1.])}
R_VAL = {'comida': 1.0, 'veneno': -3.0}; E_VAL = {'comida': +0.8, 'veneno': -0.4}


class Mundo:
    def __init__(self, rng, nobj, tipos, regen=None, fijos=None, regen_rota=False, vida=None):
        self.rng = rng; self.nobj = nobj; self.tipos = tipos; self.objs = {}; self.regen = regen; self.pend = {}   # N3c: regen
        self.fijos = list(fijos) if fijos else None   # N3d: tipos iniciales fijos (en orden), en vez de sortearlos
        self.regen_rota = regen_rota   # N2f: al reaparecer, el tipo se vuelve a sortear (mismo sitio + FLUJO de patrones)
        self.vida = vida; self.nace = {}; self.t = 0; self.caducados = 0   # N2f-v3: el objeto caduca a t_nace + vida (el veneno tambien sale del mundo)

    def _reaparece(self, kk):   # N2f: con regen_rota=False devuelve el MISMO tipo -> N3c/N3d bit a bit, sin tocar el RNG
        return self.tipos[int(self.rng.integers(len(self.tipos)))] if self.regen_rota else kk

    def spawn(self):
        while len(self.objs) + len(self.pend) < self.nobj:
            x = int(self.rng.integers(L))
            if x not in self.objs and x not in self.pend:
                self.objs[x] = self.fijos.pop(0) if self.fijos else self.tipos[int(self.rng.integers(len(self.tipos)))]
                self.nace[x] = self.t   # N2f-v3: sello de nacimiento (con vida=None no se usa)

    def retirar(self, x, t):   # N3c: al morder (o al olvido) el objeto se va; con regen vuelve al MISMO sitio con el mismo tipo
        kk = self.objs.pop(x)
        if self.regen is not None:
            self.pend[x] = (kk, t + self.regen)
            if not self.objs:   # nunca vacio: si se agotaron todos, el pendiente mas antiguo vuelve ya (see() no admite mundo vacio)
                x0 = min(self.pend, key=lambda y: self.pend[y][1]); kk0, _ = self.pend.pop(x0); self.objs[x0] = self._reaparece(kk0); self.nace[x0] = self.t   # N2f / N2f-v3
        self.spawn()

    def regenerar(self, t):
        for x in [x for x, (kk, tt) in self.pend.items() if tt <= t]:
            kk, _ = self.pend.pop(x); self.objs[x] = self._reaparece(kk); self.nace[x] = t   # N2f / N2f-v3

    def caducar(self, t):   # N2f-v3: lo que lleva `vida` pasos sin que nadie lo muerda se retira igual que si lo hubieran mordido
        for x in [x for x in self.objs if t - self.nace.get(x, 0) >= self.vida]:
            if x in self.objs: self.retirar(x, t); self.caducados += 1


class Organismo:
    def __init__(self, rng, T, eta=.03, tau_e=.85, alpha=1.2, hambre_boca=2.0, aversion=1.0, costo=.002, plast=True,
                 theta=0.6, ema=0.02, paso=0.5, lam=0.05, memoria_rechazo=20, learn=True, mu_norm=True, estado=None,
                 div_signo=True, eta_s=0.015, clip_s=3.0, puerta=3, pats=None, mundo='AB',
                 rng_q=None, K_sim=2, beta_q=2.0, eta_q=0.1, eta_m=0.1, tau_m=200, u_m=0.5,
                 gamma_sim=0.0, baseline_q=False, rho_b=0.05, alinea=False, gamma_soc=0.0, tau_soc=400, escucha=True,
                 escucha_si_no_sabe=False, eta_sym=0.0, gamma_pred=0.0, theta_a=0.0, tau_pred=400, win_crit=0, crit_rec=0.75):   # N3 (+escucha: N3b, ERR-23); N2f: escucha_si_no_sabe; C: N2 por prediccion
        """Replica linea a linea a organismo/organismo_v13.py (v11 + via lenta lineal + puerta de familiaridad).
        Con div_signo=False, eta_s=0, puerta=None es v10; ademas mu_norm=False, v9.
        pats/mundo: 'AB' (A,B) o 'regla' (los 20 patrones de peso 3, como organismo_v13g). N2: simbolos aprendidos
        (Pq del emisor, M del receptor) solo si rng_q no es None; nunca tocan el RNG del organismo."""
        self.rng = rng; self.T = T; self.eta = eta; self.tau_e = tau_e; self.alpha = alpha; self.hambre_boca = hambre_boca
        self.aversion = aversion; self.costo = costo; self.plast = plast; self.theta = theta; self.ema = ema; self.paso = paso
        self.lam = lam; self.memoria_rechazo = memoria_rechazo; self.learn = learn; self.mu_norm = mu_norm
        self.div_signo = div_signo; self.eta_s = eta_s; self.clip_s = clip_s; self.puerta = puerta
        self.P_ = PAT if pats is None else pats; self.mundo = mundo
        self.Wl = rng.uniform(.1, .4, (2, 9)); self.KW = np.zeros((NKMAX, 6)); self.activa = np.zeros(NKMAX, bool)
        self.KW[:NK] = rng.uniform(0, 1, (NK, 6)); self.activa[:NK] = True
        while mundo == 'AB' and not (len(self.code(PAT['A']) & self.code(PAT['B'])) == 0):
            self.KW[0:NK] = rng.uniform(0, 1, (NK, 6))
        # N2: simbolos. Pq[estado][simbolo] preferencias del emisor (nacen al azar, RNG propio); M[simbolo] valor que
        # el receptor cree que predice cada simbolo (nace en 0); traza (simbolo, patron) -> t de la ultima vez oido.
        self.rng_q = rng_q; self.K_sim = K_sim; self.beta_q = beta_q; self.eta_q = eta_q; self.eta_m = eta_m; self.tau_m = tau_m; self.u_m = u_m
        self.Pq = rng_q.uniform(-0.1, 0.1, (2, K_sim)) if rng_q is not None else None
        self.M = np.zeros(K_sim); self.traza = {}; self.emis = np.zeros((2, K_sim), int); self.emis_q4 = np.zeros((2, K_sim), int)
        self.refuerzos = [0, 0]; self.simbolos_recibidos = 0; self.decodificados = 0
        # N2b: el simbolo entra en la DECISION (gamma_sim * contraste, sin puerta) y el emisor aprende por VENTAJA (r - b[st])
        self.gamma_sim = gamma_sim; self.baseline_q = baseline_q; self.rho_b = rho_b; self.b = np.zeros(2); self.ultimo = {}
        self.alinea = alinea; self.alineaciones = 0   # N2e: el simbolo toma el valor de lo que el receptor ya conoce
        self.gamma_soc = gamma_soc; self.tau_soc = tau_soc; self.s_ult = {}; self.n_sesgo_soc = 0; self.escucha = escucha   # N3: ultima senal honesta oida por patron; N3b: si no escucha, no recibe nada
        self.escucha_si_no_sabe = escucha_si_no_sabe; self.no_desensena = 0   # N2f: el simbolo no reescribe un valor propio MAS informado que el
        self.eta_sym = eta_sym; self.gamma_pred = gamma_pred; self.theta_a = theta_a; self.tau_pred = tau_pred   # C: N2 POR PREDICCION
        self.u = np.zeros(2); self.c_ult = {}; self.n_u = [0, 0]; self.n_pred_vic = 0; self.n_callado = 0   # C: u[c] = dE que predice la conducta ajena c (0 rechaza, 1 muerde)
        self.win_crit = win_crit; self.crit_rec = crit_rec; self._wq = []   # C: ventana movil del acierto balanceado (SOLO LECTURA)
        self.expo_rec = 0; self.mord_rec = 0; self.expo_crit = None; self.mord_crit = None; self.curva_rec = []   # C: exposiciones y mordidas hasta criterio
        self.Wp = np.zeros(NKMAX); self.Wn = np.zeros(NKMAX); self.err = np.zeros(NKMAX); self.mu = np.zeros((NKMAX, 6))
        self.splits = 0; self.el = np.zeros_like(self.Wl); self.tr = np.zeros(9)
        self.Wps = np.zeros(6); self.Wns = np.zeros(6)   # v13: via lenta lineal sobre la retina
        if estado is not None:   # herencia completa (experto): copias del estado de un progenitor; los contadores en cero
            self.KW[:] = estado['KW']; self.activa[:] = estado['activa']; self.Wp[:] = estado['Wp']; self.Wn[:] = estado['Wn']
            self.err[:] = estado['err']; self.mu[:] = estado['mu']; self.Wl[:] = estado['Wl']
            self.Wps[:] = estado.get('Wps', 0.); self.Wns[:] = estado.get('Wns', 0.)
        self.pos = 0; self.E = 1.0; self._rech = {}; self._prev_on = -1
        self.split_t = []; self.mord = {k: [0] * 4 for k in self.P_}; self.vis = {k: [0] * 4 for k in self.P_}; self.deaths = 0
        self.dq = [0] * 4; self.veneno_propio = {k: 0 for k in self.P_}; self.n_crit = {}; self.vicarias = {k: 0 for k in self.P_}
        self.vicarias_signo = {k: [0, 0] for k in self.P_}; self.avisos_B_antes_crit = 0; self.t_B_ok = None
        self.t_ext_B = None; self.R = 0.; self.Rp = 0.; self.hambre = 0.

    def q(self, t): return min(t // (self.T // 4), 3)

    def code(self, P):
        v = self.KW @ P; v = np.where(self.activa, v, -1e9); return set(np.argsort(v)[-K:])

    def kenyon(self, P):
        k = np.zeros(NKMAX); k[list(self.code(P))] = 1; return k

    def _total(self, P, kc, Wb):
        """v13: el valor que usa la boca. Sin puerta: rapida + lenta. Con puerta: la rapida si el patron le es familiar
        (>= puerta celdas del codigo con |Wp-Wn|>0.2), si no la lenta."""
        _wf = float(Wb @ kc); _ws = float((self.Wps - self.Wns) @ P)
        if self.puerta is None: return _wf + _ws, _wf, _ws
        return (_wf if int((np.abs(Wb[kc > 0]) > 0.2).sum()) >= self.puerta else _ws), _wf, _ws

    def valor(self, kk):
        kc = self.kenyon(self.P_[kk]); return self._total(self.P_[kk], kc, self.Wp - self.Wn)[0]

    # ---- N2: simbolos aprendidos ----
    def emitir(self, st, t):
        """El emisor elige un simbolo segun su propio estado (1 muerde / 0 rechaza): softmax(beta_q * Pq[st]), RNG propio."""
        p = np.exp(self.beta_q * self.Pq[st]); p = p / p.sum()
        s = int(self.rng_q.choice(self.K_sim, p=p)); self.emis[st][s] += 1
        if self.q(t) == 3: self.emis_q4[st][s] += 1
        return s

    def reforzar(self, st, s, r):
        """Ganancia compartida operacionalizada: +1 si la conducta del receptor coincidio con el estado del emisor, -1 si no."""
        adv = r - float(self.b[st]) if self.baseline_q else r   # N2b: ventaja sobre la linea base del estado
        if self.baseline_q: self.b[st] += self.rho_b * (r - self.b[st])
        self.Pq[st][s] = float(np.clip(self.Pq[st][s] + self.eta_q * adv, -3, 3)); self.refuerzos[0 if r > 0 else 1] += 1

    def recibir_simbolo(self, kk, s, f_vicaria, val, t, invertir_en):
        """El receptor oye el simbolo s sobre un objeto de patron kk: deja traza y, si ya cree saber que significa s
        (|M[s]| >= u_m), actualiza su propio valor de kk con R = M[s] (las dos vias, sin dividir, sin comer)."""
        self.traza[(s, kk)] = t; self.simbolos_recibidos += 1; self.ultimo[kk] = (s, t)
        if self.alinea and self.learn:   # N2e: alineacion con lo ya conocido (familiar a la via rapida = la prueba de la puerta)
            _kc = self.kenyon(self.P_[kk]); _Wb = self.Wp - self.Wn
            if int((np.abs(_Wb[_kc > 0]) > 0.2).sum()) >= 3:
                self.M[s] += self.eta_m * (float(_Wb @ _kc) - self.M[s]); self.alineaciones += 1
        # ENMIENDA 1 de N2: el significado es CONTRASTE, no magnitud. Con simbolos al azar cada M[s] tiende al promedio de
        # consecuencias (-1 con 10 venenos y 10 comidas) y el receptor devaluaria todo lo senalado; lo que informa es
        # cuanto se aparta un simbolo de la media de los simbolos.
        R_hat = float(self.M[s] - self.M.mean())
        # N2f: el que ya sabe del patron mas de lo que el simbolo dice no se deja desensenar (cortocircuito: con la
        # perilla apagada `valor(kk)` ni se evalua, y `valor`/`kenyon`/`code` no tocan estado ni RNG).
        _sabe_mas = self.escucha_si_no_sabe and abs(self.valor(kk)) >= abs(R_hat)
        if _sabe_mas and abs(R_hat) >= self.u_m: self.no_desensena += 1
        if self.learn and abs(R_hat) >= self.u_m and not _sabe_mas:
            kc = self.kenyon(self.P_[kk]); Wb = self.Wp - self.Wn
            self._aprender(kk, kc, Wb, R_hat, f_vicaria, t, dividir=False)
            self.decodificados += 1; self.vicarias[kk] += 1; self.vicarias_signo[kk][0 if R_hat > 0 else 1] += 1
        self._criterios(val, t, invertir_en)

    def _actualizar_M(self, kk, R, t):
        """Tras morder kk el mismo con consecuencia R: todo simbolo oido sobre kk hace <= tau_m pasos aprende R."""
        for s in range(self.K_sim):
            tk = self.traza.get((s, kk))
            if tk is not None and t - tk <= self.tau_m:
                self.M[s] += self.eta_m * (R - self.M[s])

    def see(self, objs, t):
        best = None
        for x, k in objs.items():
            if self.memoria_rechazo and self._rech.get(x, -1) > t: continue
            dl = (self.pos - x) % L; dr = (x - self.pos) % L; d = min(dl, dr)
            if best is None or d < best[0]: best = (d, k, dl < dr)
        if best is None:
            for x, k in objs.items():
                dl = (self.pos - x) % L; dr = (x - self.pos) % L; d = min(dl, dr)
                if best is None or d < best[0]: best = (d, k, dl < dr)
        return best

    def _criterios(self, val, t, invertir_en):
        if self.mundo != 'AB': return   # en el mundo de regla las metricas se leen al final (mord, vis, W)
        for kk in ('A', 'B'):
            if (kk not in self.n_crit) and val[kk] == 'veneno' and self.valor(kk) <= -2.5:
                self.n_crit[kk] = self.veneno_propio[kk]
        if invertir_en is not None and t >= invertir_en and self.t_ext_B is None and self.valor('B') >= 0:
            self.t_ext_B = t
        if self.t_B_ok is None and self.valor('B') >= 0.5:
            self.t_B_ok = t

    def fase_A(self, mundo, val, t, invertir_en):
        """Percibir, mover, morder, aprender (boca y valor), gastar energia.
        Devuelve None si no piso objeto; si lo piso, (pos, kk, mordio, R): la conducta visible de la visita."""
        rng = self.rng; objs = mundo.objs; emitida = None
        hambre = np.clip(1 - self.E, 0, 1); self.hambre = hambre; d, k, left = self.see(objs, t); pat = self.P_[k]
        x = np.concatenate([pat * 1.2, [1.5 if left else 0, 0 if left else 1.5, 1.0 if d == 0 else 0.]]); noise = .15 + .5 * hambre
        V = self.Wl @ x; p = 1 / (1 + np.exp(-(V - .8) / noise)); u = p + rng.normal(0, .3, 2); m = np.zeros(2)
        if u.max() > .5: m[np.argmax(u)] = 1
        self.tr = self.tr * .7 + x
        if self.learn: self.el = self.el * self.tau_e + np.outer(m - p, self.tr)
        self.pos = (self.pos + int(m[1] - m[0])) % L; d2, _, _ = self.see(objs, t); self.Rp = .2 if d2 < d else 0.
        self.R = 0.
        if self.pos in objs:
            kk = objs[self.pos]; kc = self.kenyon(self.P_[kk]); Wb = self.Wp - self.Wn
            _wt, _, _ = self._total(self.P_[kk], kc, Wb)   # v13
            if self.gamma_sim and kk in self.ultimo and t - self.ultimo[kk][1] <= self.tau_m:   # N2b: el simbolo sesga la decision
                _wt = _wt + self.gamma_sim * float(self.M[self.ultimo[kk][0]] - self.M.mean())
            if self.gamma_soc and kk in self.s_ult and t - self.s_ult[kk][1] <= self.tau_soc:   # N3: la conducta ajena reciente sesga la decision
                _wt = _wt + self.gamma_soc * self.s_ult[kk][0]; self.n_sesgo_soc += 1
            Vb = self.alpha * _wt + self.hambre_boca * hambre + .5; pb = 1 / (1 + np.exp(-Vb / .3)); mordio = rng.random() < pb
            self.vis[kk][self.q(t)] += 1
            self.expo_rec += 1
            if self.win_crit:   # C: sonda movil del acierto BALANCEADO de conducta (la misma formula de acierto_q4, en ventana)
                self._wq.append((1 if val[kk] == 'comida' else 0, 1 if mordio else 0))
                if len(self._wq) > self.win_crit: self._wq.pop(0)
                if self.expo_crit is None and len(self._wq) >= self.win_crit and self.expo_rec % 100 == 0:
                    _c = [m for f, m in self._wq if f]; _v = [m for f, m in self._wq if not f]
                    if _c and _v:
                        _ac = 0.5 * (sum(_c) / len(_c)) + 0.5 * (1 - sum(_v) / len(_v))
                        self.curva_rec.append((t, self.expo_rec, self.mord_rec, round(_ac, 4)))
                        if _ac >= self.crit_rec and len(self.curva_rec) >= 2 and self.curva_rec[-2][3] >= self.crit_rec:
                            self.expo_crit = self.curva_rec[-2][1]; self.mord_crit = self.curva_rec[-2][2]
            if self.memoria_rechazo and not mordio: self._rech[self.pos] = t + self.memoria_rechazo
            emitida = (self.pos, kk, bool(mordio), 0.)
            if mordio:
                self.R = R_VAL[val[kk]]; self.E = min(self.E + E_VAL[val[kk]], 1.5); self.mord[kk][self.q(t)] += 1
                self.mord_rec += 1
                if self.eta_sym and kk in self.c_ult and t - self.c_ult[kk][1] <= self.tau_pred:   # C: que dE predice la conducta ajena, medido con SU cuerpo
                    _cc = self.c_ult[kk][0]; self.u[_cc] += self.eta_sym * (E_VAL[val[kk]] - self.u[_cc]); self.n_u[_cc] += 1
                if val[kk] == 'veneno': self.veneno_propio[kk] += 1
                emitida = (self.pos, kk, True, self.R)
                mundo.retirar(self.pos, t)   # N3c (regen=None: identico a del + spawn)
                self._rech.pop(self.pos, None)
                if self.learn:
                    self._aprender(kk, kc, Wb, self.R, 1.0, t, dividir=True)
                    self._actualizar_M(kk, self.R, t)   # N2 (no-op sin simbolos: la traza esta vacia)
            self._criterios(val, t, invertir_en)
        self._prev_on = self.pos if self.pos in objs else -1
        self.E -= self.costo
        return emitida

    def _aprender(self, kk, kc, Wb, R, factor, t, dividir):
        """Una experiencia con refuerzo R sobre el patron kk (propia: factor 1; vicaria: factor f_vicaria, sin dividir).
        Replica el bloque de aprendizaje de organismo_v13: cada via su error; division por conflicto de signo."""
        P = self.P_[kk]; eta = self.eta * factor
        _wt, _wf, _ws = self._total(P, kc, Wb)
        dlt = R - _wt if self.puerta is None else R - _wf   # v13
        if self.eta_s:   # v13: via lenta
            _ds = dlt if self.puerta is None else R - _ws
            if self.lam: _mcs = np.minimum(self.Wps, self.Wns) * (P > 0); self.Wps = self.Wps - self.lam * _mcs; self.Wns = self.Wns - self.lam * _mcs
            if _ds > 0: self.Wps = np.clip(self.Wps + self.eta_s * factor * _ds * P, 0, self.clip_s)
            else:       self.Wns = np.clip(self.Wns + self.eta_s * factor * self.aversion * (-_ds) * P, 0, self.clip_s)
        if self.lam: ix = kc > 0; mcom = np.minimum(self.Wp[ix], self.Wn[ix]); self.Wp[ix] -= self.lam * mcom; self.Wn[ix] -= self.lam * mcom
        if dlt > 0: self.Wp = np.clip(self.Wp + eta * dlt * kc, 0, 3.)
        else:       self.Wn = np.clip(self.Wn + eta * self.aversion * (-dlt) * kc, 0, 3.)
        if dividir and self.plast:
            idx = np.where(kc > 0)[0]; self.err[idx] = (1 - self.ema) * self.err[idx] + self.ema * abs(dlt)
            self.mu[idx] = (1 - self.ema) * self.mu[idx] + self.ema * P
            for c in idx:
                if self.div_signo:   # v11: conflicto de signo, hija ciega fuera de P, madre fija, fision del valor
                    dist = P - (self.mu[c] * (P.sum() / max(float(self.mu[c].sum()), 1e-9)) if self.mu_norm else self.mu[c])
                    kj = np.clip(self.KW[c] * (1 - 0.05) + self.paso * dist, 0, 5) * (P > 0)
                    if Wb[c] * R < 0 and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(self.KW[c] @ P) and (~self.activa).any():
                        j = int(np.where(~self.activa)[0][0]); self.activa[j] = True; self.KW[j] = kj
                        if R > 0: self.Wp[j] = self.Wp[c]; self.Wn[j] = 0.; self.Wp[c] = 0.
                        else:     self.Wn[j] = self.Wn[c]; self.Wp[j] = 0.; self.Wn[c] = 0.
                        self.mu[j] = P * (float(self.mu[c].sum()) / P.sum()); self.err[c] = self.err[j] = 0
                        self.splits += 1; self.split_t.append((t, kk))
                elif self.err[c] > self.theta and (~self.activa).any():
                    j = int(np.where(~self.activa)[0][0]); self.activa[j] = True
                    dist = P - (self.mu[c] * (P.sum() / max(float(self.mu[c].sum()), 1e-9)) if self.mu_norm else self.mu[c])   # v10: mu normalizada
                    self.KW[j] = np.clip(self.KW[c] + self.paso * dist, 0, 5); self.KW[c] = np.clip(self.KW[c] - self.paso * dist, 0, 5)
                    self.Wp[j] = self.Wp[c]; self.Wn[j] = self.Wn[c]; self.mu[j] = self.mu[c].copy(); self.err[c] = self.err[j] = 0
                    self.splits += 1; self.split_t.append((t, kk))

    def recibir(self, kk, signo, f_vicaria, val, t, invertir_en):
        """Aprendizaje vicario. Sin gamma_pred: escala INNATA (+ -> +1, − -> −3), como N3d. Con gamma_pred: el valor
        vicario es lo que el receptor PREDICE que va a sentir (u[c], aprendido con su propio cuerpo). Sin divisiones."""
        if self.gamma_soc: self.s_ult[kk] = (1.0 if signo > 0 else -1.0, t)   # N3
        self.c_ult[kk] = (1 if signo > 0 else 0, t)   # C: la CONDUCTA ajena observada sobre este patron (para aprender u[c])
        if not self.learn: return
        kc = self.kenyon(self.P_[kk]); Wb = self.Wp - self.Wn
        if not self.gamma_pred:
            self._aprender(kk, kc, Wb, 1.0 if signo > 0 else -3.0, f_vicaria, t, dividir=False)
        elif self.theta_a and abs(self.valor(kk)) >= self.theta_a:   # C: ya lo sabe por su cuenta -> no escucha
            self.n_callado += 1
            self._criterios(val, t, invertir_en); return
        else:   # C: N2 POR PREDICCION — el valor vicario sale de u[c], en unidades de R con las constantes del mundo
            _cc = 1 if signo > 0 else 0; _u = float(self.u[_cc])
            _R = (R_VAL['comida'] / E_VAL['comida']) * _u if _u > 0 else (R_VAL['veneno'] / E_VAL['veneno']) * _u
            self._aprender(kk, kc, Wb, _R, self.gamma_pred, t, dividir=False); self.n_pred_vic += 1
        self.vicarias[kk] += 1; self.vicarias_signo[kk][0 if signo > 0 else 1] += 1
        if kk == 'B' and signo < 0 and 'B' not in self.n_crit: self.avisos_B_antes_crit += 1
        self._criterios(val, t, invertir_en)

    def estado(self):
        return dict(KW=self.KW.copy(), activa=self.activa.copy(), Wp=self.Wp.copy(), Wn=self.Wn.copy(), err=self.err.copy(),
                    mu=self.mu.copy(), Wl=self.Wl.copy(), Wps=self.Wps.copy(), Wns=self.Wns.copy())

    def fase_B(self, t):
        if self.learn: self.Wl = np.clip(self.Wl + self.eta * (1 + 2 * self.hambre) * (max(self.R, 0) + self.Rp) * self.el, 0, 1.5)
        if self.E <= 0: self.deaths += 1; self.E = .6; self.pos = int(self.rng.integers(L)); self.dq[self.q(t)] += 1

    def resultado(self):
        W = {k: round(self.valor(k), 2) for k in self.P_}   # v13: valor total
        comp = {k: (round(float(self.Wp @ self.kenyon(self.P_[k])), 2), round(float(self.Wn @ self.kenyon(self.P_[k])), 2)) for k in self.P_}
        W_lenta = {k: round(float((self.Wps - self.Wns) @ self.P_[k]), 3) for k in self.P_}
        sim = None
        if self.Pq is not None:   # N2: lectura del codigo
            pref = [int(np.argmax(self.Pq[st])) for st in (0, 1)]
            tot4 = int(self.emis_q4.sum()); cons = (int(self.emis_q4[0][pref[0]] + self.emis_q4[1][pref[1]]) / tot4) if tot4 else None
            sim = dict(Pq=[[round(float(x), 3) for x in fila] for fila in self.Pq], simbolo_rechazo=pref[0], simbolo_muerde=pref[1],
                       distintos=pref[0] != pref[1], consistencia_q4=cons, emis=self.emis.tolist(), emis_q4=self.emis_q4.tolist(),
                       refuerzos=list(self.refuerzos), b=[round(float(x), 3) for x in self.b], alineaciones=self.alineaciones)
        return dict(W=W, comp=comp, W_lenta=W_lenta, mord=self.mord, vis=self.vis, deaths=self.deaths, splits=self.splits, split_t=self.split_t, n_sesgo_soc=self.n_sesgo_soc,
                    celdas=int(self.activa.sum()), dq=self.dq, n_crit=self.n_crit, veneno_propio=self.veneno_propio,
                    u=[round(float(x), 4) for x in self.u], n_u=list(self.n_u), n_pred_vic=self.n_pred_vic, n_callado=self.n_callado,
                    expo_rec=self.expo_rec, mord_rec=self.mord_rec, expo_crit=self.expo_crit, mord_crit=self.mord_crit, curva_rec=self.curva_rec,
                    vicarias=self.vicarias, vicarias_signo=self.vicarias_signo, avisos_B_antes_crit=self.avisos_B_antes_crit,
                    t_ext_B=self.t_ext_B, t_B_ok=self.t_B_ok, M=[round(float(x), 3) for x in self.M], simbolos_recibidos=self.simbolos_recibidos, no_desensena=self.no_desensena,
                    decodificados=self.decodificados, simbolos=sim)


SIMBOLOS = ('simbolo', 'simbolo_barajado')


def run(seed, n=1, T=100000, invertir_en=None, senal=None, d_senal=5, f_vicaria=1/3, nobj_por_org=4, compat=True,
        estados=None, devolver_estado=False, mundo='AB', regla='azar', tau_s=200, K_sim=2, estado_emisor='conducta', u_v=0.5,
        mascaras=None, kw_por_org=None, regen=None, tipos_fijos=None, mudo_desde=None, regen_rota=False, vida=None, **kw_org):   # N3: mascara de retina y kwargs por organismo; N3c: regen; N3d: tipos_fijos; N3d-mudo: mudo_desde; N2f: regen_rota; N2f-v3: vida
    """senal: None | 'honesta' (al morder: + comida, - veneno) | 'conducta' (en cada visita: + mordio, - rechazo)
              | 'barajada' (como honesta, signo al azar) | 'barajada_conducta' (como conducta, signo al azar)
              | 'simbolo' (N2: K_sim simbolos sin significado; el emisor aprende cual emitir, el receptor que significa)
              | 'simbolo_barajado' (N2 control: el receptor oye un simbolo al azar).
    mundo: 'AB' (A comida, B veneno) o 'regla' (20 patrones de peso 3 con valencias de `regla`, como organismo_v13g con
    fase2_en=0: los 10 de entrenamiento desde el sorteo inicial y los 10 de test anadidos en t=0)."""
    if mundo == 'AB':
        pats, tren, test, val = PAT, ['A', 'B'], [], {'A': 'comida', 'B': 'veneno'}
    else:
        import os as _os, sys as _sys
        _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'v13_dos_vias'))
        from organismo_v13g import split_regla
        pats, tren, test, val = split_regla(seed, regla); val = dict(val)
    rngs = [np.random.default_rng(seed + 100000 * i) for i in range(n)]
    rngs_q = [np.random.default_rng(seed + 500000 * i + 7) if senal in SIMBOLOS else None for i in range(n)]
    _pats_i = lambda i: pats if (mascaras is None or mascaras[i] is None) else {k: v * np.asarray(mascaras[i], float) for k, v in pats.items()}   # N3
    _kw_i = lambda i: dict(kw_org, **(kw_por_org[i] if kw_por_org else {}))
    orgs = [Organismo(rngs[i], T, estado=(estados[i] if estados else None), pats=_pats_i(i), mundo=mundo, rng_q=rngs_q[i], K_sim=K_sim, **_kw_i(i))
            for i in range(n)]
    rng_mundo = rngs[0] if (n == 1 and compat) else np.random.default_rng(seed + 900000)
    rng_senal = np.random.default_rng(seed + 300000)
    tipos = list(tren)
    mundo_ = Mundo(rng_mundo, nobj_por_org * n, tipos, regen=regen, fijos=tipos_fijos, regen_rota=regen_rota, vida=vida); mundo_.spawn()   # N3c / N3d / N2f / N2f-v3
    tipos.extend(test)   # como v13g con fase2_en=0: los de test entran en t=0, tras el sorteo inicial
    mundo = mundo_
    senales_emitidas = [0] * n; senales_recibidas = [0] * n
    pendientes = []   # N2: emisiones que esperan la conducta del receptor sobre el mismo patron (refuerzo del emisor)
    for t in range(T):
        mundo.t = t   # N2f-v3: reloj del mundo para el sello de nacimiento (con vida=None no cambia nada)
        if mundo.pend: mundo.regenerar(t)   # N3c
        if mundo.vida is not None: mundo.caducar(t)   # N2f-v3
        if invertir_en is not None and t == invertir_en and 'A' in val and 'B' in val: val = {'A': 'veneno', 'B': 'comida'}
        orden = range(n) if t % 2 == 0 else range(n - 1, -1, -1)
        emitidas = []
        for i in orden:
            e = orgs[i].fase_A(mundo, val, t, invertir_en)
            if e is None: continue
            px, kk, mordio, R = e
            if senal in SIMBOLOS and n > 1:
                if estado_emisor == 'valor':   # N2c: el estado es lo que el emisor SABE; si no sabe, calla
                    _v = orgs[i].valor(kk)
                    if _v >= u_v: st = 1
                    elif _v <= -u_v: st = 0
                    else: st = None
                elif estado_emisor == 'valor_rapido':   # N2d: habla solo de lo que su via RAPIDA conoce (familiar = la prueba de la puerta)
                    _o = orgs[i]; _kc = _o.kenyon(_o.P_[kk]); _Wb = _o.Wp - _o.Wn
                    _fam = int((np.abs(_Wb[_kc > 0]) > 0.2).sum()) >= 3; _v = float(_Wb @ _kc)
                    if _fam and _v >= u_v: st = 1
                    elif _fam and _v <= -u_v: st = 0
                    else: st = None
                else:
                    st = 1 if mordio else 0
                quedan = []
                _c = 1 if mordio else 0   # la CONDUCTA del visitante es lo que resuelve las emisiones ajenas (acuerdo)
                for p in pendientes:   # la visita de i resuelve emisiones ajenas sobre este patron (una por emision)
                    if p['i'] != i and p['kk'] == kk and t - p['t'] <= tau_s and not p.get('hecho'):
                        orgs[p['i']].reforzar(p['st'], p['s'], +1 if _c == p['st'] else -1); p['hecho'] = True
                    if not p.get('hecho') and t - p['t'] <= tau_s: quedan.append(p)
                pendientes = quedan
                if st is not None:
                    s = orgs[i].emitir(st, t); emitidas.append((i, px, kk, s)); senales_emitidas[i] += 1
                    pendientes.append(dict(i=i, kk=kk, st=st, s=s, t=t))
            elif senal in ('honesta', 'barajada'):
                if mordio: emitidas.append((i, px, kk, 1 if R > 0 else -1)); senales_emitidas[i] += 1
            elif senal in ('conducta', 'barajada_conducta'):
                emitidas.append((i, px, kk, 1 if mordio else -1)); senales_emitidas[i] += 1
        if senal is not None and n > 1 and (mudo_desde is None or t < mudo_desde):   # N3d-mudo: desde mudo_desde no se entrega nada
            for i, px, kk, signo in emitidas:
                if senal in SIMBOLOS:
                    s = signo if senal == 'simbolo' else int(rng_senal.integers(K_sim))
                else:
                    s = signo if senal in ('honesta', 'conducta') else (1 if rng_senal.random() < .5 else -1)
                for j in range(n):
                    if j == i: continue
                    dl = (orgs[j].pos - px) % L; dist = min(dl, L - dl)
                    if dist <= d_senal:
                        if senal in SIMBOLOS: orgs[j].recibir_simbolo(kk, s, f_vicaria, val, t, invertir_en)
                        elif orgs[j].escucha: orgs[j].recibir(kk, s, f_vicaria, val, t, invertir_en)   # N3b (ERR-23): el que no escucha no recibe
                        senales_recibidas[j] += 1
        if mundo.rng.random() < .003 and mundo.objs:
            _dx = list(mundo.objs)[int(mundo.rng.integers(len(mundo.objs)))]; mundo.retirar(_dx, t)   # N3c
            for o in orgs: o._rech.pop(_dx, None)
        for i in orden:
            orgs[i].fase_B(t)
    out = [o.resultado() for o in orgs]
    for i in range(n):
        out[i]['senales_emitidas'] = senales_emitidas[i]; out[i]['senales_recibidas'] = senales_recibidas[i]; out[i]['caducados'] = mundo.caducados   # N2f-v3
        if devolver_estado: out[i]['estado'] = orgs[i].estado()
    return out
