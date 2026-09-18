"""CREADOR C — constructor POR ANCLAS de N2 POR PREDICCION (encargo (2) del coordinador, 18-sep).

  mundo_social_pred.py <- experimentos/etapa5_comunicacion/mundo_social_n3.py   (ef227f833c5bf46a; SOLO SE LEE)

QUE CAMBIA, y nada mas. Hoy, en N3d, el receptor ciego aprende del emisor con una escala INNATA: la conducta ajena
(+ mordio / - rechazo) se traduce a R = +1 / -3 por construccion. El significado esta DADO. Aqui el receptor **lo
aprende con su propio cuerpo**:

  u[c]  = lo que el receptor PREDICE que va a SENTIR cuando la conducta ajena sobre ese patron fue c (0 rechaza, 1 muerde)
  al MORDER un patron del que oyo la conducta c hace <= tau_pred pasos:
          u[c] <- u[c] + eta_sym * (E_VAL[valencia] - u[c])          <- regla delta local, sobre lo que SINTIO
  al OIR la conducta c sobre un patron (sin morderlo):
          R_hat = (R_VAL/E_VAL) * u[c]   con las constantes del mundo (sin parametro libre: +0.8 -> +1.0, -0.4 -> -3.0)
          se aprende el valor del objeto con R_hat y factor gamma_pred, SIN morderlo
  puerta `theta_a`: si el receptor ya sabe por su cuenta (|valor propio| >= theta_a), no escucha. Con theta_a = 0 no hay puerta.

MEMORIA QUE EXIGE: **2 escalares** (u[0], u[1]) y una marca (patron -> conducta oida, paso). Nada mas.
El significado converge al innato (+1 / -3) si el mundo lo sostiene: la diferencia es que aqui **se aprende**, y por eso
se puede medir cuanto cuesta aprenderlo.

MEDIDA NUEVA (decision del director, 05:10): **exposiciones y MORDIDAS hasta criterio**. Ventana movil de `win_crit`
encuentros; acierto BALANCEADO de conducta (muerde comida / rechaza veneno), el mismo de `acierto_q4` de corre_N3d.py
pero movil; `expo_crit` / `mord_crit` = los contadores de la primera sonda que cruza `crit_rec` **y se sostiene en la
siguiente**. Es SOLO LECTURA: no toca el RNG ni ninguna decision.

Con eta_sym = 0, gamma_pred = 0 y theta_a = 0 es mundo_social_n3 EXACTO (y con win_crit > 0 tambien: solo lee).
NO editar el generado a mano.  Uso:  python experimentos/creacion_C/construye_n2pred.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
NL = chr(10)
SHA_N3 = 'ef227f833c5bf46a'


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


CAB = ('"""mundo_social_pred = experimentos/etapa5_comunicacion/mundo_social_n3.py (ef227f833c5bf46a) + N2 POR PREDICCION:' + NL +
       'el receptor aprende que va a SENTIR a partir de la CONDUCTA VISIBLE del emisor (u[c], regla delta sobre su propia' + NL +
       'dE al morder) y con eso aprende el valor de un objeto SIN morderlo. Con eta_sym=0, gamma_pred=0 y theta_a=0 es' + NL +
       'mundo_social_n3 EXACTO. Mide exposiciones y mordidas del receptor hasta criterio (solo lectura).' + NL +
       'Generado por experimentos/creacion_C/construye_n2pred.py. NO editar. RAMA de creacion: no es tronco.' + NL + '"""' + NL)

PERILLAS = ("eta_sym=0.0, gamma_pred=0.0, theta_a=0.0, tau_pred=400, win_crit=0, crit_rec=0.75")

ESTADO = [
    "        self.eta_sym = eta_sym; self.gamma_pred = gamma_pred; self.theta_a = theta_a; self.tau_pred = tau_pred   # C: N2 POR PREDICCION",
    "        self.u = np.zeros(2); self.c_ult = {}; self.n_u = [0, 0]; self.n_pred_vic = 0; self.n_callado = 0   # C: u[c] = dE que predice la conducta ajena c (0 rechaza, 1 muerde)",
    "        self.win_crit = win_crit; self.crit_rec = crit_rec; self._wq = []   # C: ventana movil del acierto balanceado (SOLO LECTURA)",
    "        self.expo_rec = 0; self.mord_rec = 0; self.expo_crit = None; self.mord_crit = None; self.curva_rec = []   # C: exposiciones y mordidas hasta criterio",
]

# En fase_A, tras contar la visita: contador de exposiciones + sonda movil del criterio (solo lectura, no toca el RNG)
SONDA = [
    "            self.expo_rec += 1",
    "            if self.win_crit:   # C: sonda movil del acierto BALANCEADO de conducta (la misma formula de acierto_q4, en ventana)",
    "                self._wq.append((1 if val[kk] == 'comida' else 0, 1 if mordio else 0))",
    "                if len(self._wq) > self.win_crit: self._wq.pop(0)",
    "                if self.expo_crit is None and len(self._wq) >= self.win_crit and self.expo_rec % 100 == 0:",
    "                    _c = [m for f, m in self._wq if f]; _v = [m for f, m in self._wq if not f]",
    "                    if _c and _v:",
    "                        _ac = 0.5 * (sum(_c) / len(_c)) + 0.5 * (1 - sum(_v) / len(_v))",
    "                        self.curva_rec.append((t, self.expo_rec, self.mord_rec, round(_ac, 4)))",
    "                        if _ac >= self.crit_rec and len(self.curva_rec) >= 2 and self.curva_rec[-2][3] >= self.crit_rec:",
    "                            self.expo_crit = self.curva_rec[-2][1]; self.mord_crit = self.curva_rec[-2][2]",
]

# Al morder: contador de mordidas + aprendizaje de u[c] con el propio cuerpo
BOCADO = [
    "                self.mord_rec += 1",
    "                if self.eta_sym and kk in self.c_ult and t - self.c_ult[kk][1] <= self.tau_pred:   # C: que dE predice la conducta ajena, medido con SU cuerpo",
    "                    _cc = self.c_ult[kk][0]; self.u[_cc] += self.eta_sym * (E_VAL[val[kk]] - self.u[_cc]); self.n_u[_cc] += 1",
]

RECIBIR_VIEJO = """    def recibir(self, kk, signo, f_vicaria, val, t, invertir_en):
        \"\"\"Aprendizaje vicario: la señal dice +/− del patron kk; escala innata + -> +1, − -> −3. Sin divisiones.\"\"\"
        if self.gamma_soc: self.s_ult[kk] = (1.0 if signo > 0 else -1.0, t)   # N3
        if not self.learn: return
        kc = self.kenyon(self.P_[kk]); Wb = self.Wp - self.Wn
        self._aprender(kk, kc, Wb, 1.0 if signo > 0 else -3.0, f_vicaria, t, dividir=False)
        self.vicarias[kk] += 1; self.vicarias_signo[kk][0 if signo > 0 else 1] += 1"""

RECIBIR_NUEVO = """    def recibir(self, kk, signo, f_vicaria, val, t, invertir_en):
        \"\"\"Aprendizaje vicario. Sin gamma_pred: escala INNATA (+ -> +1, − -> −3), como N3d. Con gamma_pred: el valor
        vicario es lo que el receptor PREDICE que va a sentir (u[c], aprendido con su propio cuerpo). Sin divisiones.\"\"\"
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
        self.vicarias[kk] += 1; self.vicarias_signo[kk][0 if signo > 0 else 1] += 1"""

SALIDA = ("                    u=[round(float(x), 4) for x in self.u], n_u=list(self.n_u), n_pred_vic=self.n_pred_vic, n_callado=self.n_callado,"
          + NL +
          "                    expo_rec=self.expo_rec, mord_rec=self.mord_rec, expo_crit=self.expo_crit, mord_crit=self.mord_crit, curva_rec=self.curva_rec,")


def construye():
    src = os.path.join(RAIZ, 'experimentos', 'etapa5_comunicacion', 'mundo_social_n3.py')
    real = h16(src)
    if real != SHA_N3:
        raise SystemExit(f"ORIGEN mundo_social_n3.py: sha {real}, se esperaba {SHA_N3}. Abortado.")
    txt = open(src, encoding='utf-8').read()

    fin = txt.index('"""', 3) + 3
    txt = CAB + txt[fin:].lstrip(NL)

    # 1) perillas nuevas en la firma de Organismo
    ancla_firma = "                 escucha_si_no_sabe=False):   # N3 (+escucha: N3b, ERR-23); N2f: escucha_si_no_sabe"
    txt = sust(txt, ancla_firma,
               "                 escucha_si_no_sabe=False, " + PERILLAS + "):   # N3 (+escucha: N3b, ERR-23); N2f: escucha_si_no_sabe; C: N2 por prediccion",
               etiqueta='firma')

    # 2) estado nuevo
    ancla_est = "        self.escucha_si_no_sabe = escucha_si_no_sabe; self.no_desensena = 0"
    linea = [l for l in txt.splitlines() if l.startswith(ancla_est)][0]
    txt = sust(txt, linea, linea + NL + NL.join(ESTADO), etiqueta='estado')

    # 3) sonda de exposiciones (tras contar la visita)
    ancla_vis = "            self.vis[kk][self.q(t)] += 1"
    txt = sust(txt, ancla_vis, ancla_vis + NL + NL.join(SONDA), etiqueta='sonda')

    # 4) al morder: contador y aprendizaje de u[c]
    ancla_bocado = "                self.R = R_VAL[val[kk]]; self.E = min(self.E + E_VAL[val[kk]], 1.5); self.mord[kk][self.q(t)] += 1"
    txt = sust(txt, ancla_bocado, ancla_bocado + NL + NL.join(BOCADO), etiqueta='bocado')

    # 5) recibir: la rama de prediccion
    txt = sust(txt, RECIBIR_VIEJO, RECIBIR_NUEVO, etiqueta='recibir')

    # 6) salidas nuevas
    ancla_sal = "                    celdas=int(self.activa.sum()), dq=self.dq, n_crit=self.n_crit, veneno_propio=self.veneno_propio,"
    txt = sust(txt, ancla_sal, ancla_sal + NL + SALIDA, etiqueta='salida')

    dst = os.path.join(AQUI, 'mundo_social_pred.py')
    open(dst, 'w', encoding='utf-8', newline=NL).write(txt)
    print(f"  experimentos/creacion_C/mundo_social_pred.py  sha {h16(dst)}  ({len(txt.splitlines())} lineas)")


if __name__ == '__main__':
    print("Constructor por anclas — N2 POR PREDICCION (creador C)")
    print(f"  origen experimentos/etapa5_comunicacion/mundo_social_n3.py  sha {SHA_N3} OK")
    construye()
    print("Listo. Identidad: python experimentos/creacion_C/identidad_n2pred.py")
