"""parche (5-oct): compuerta ADAPTATIVA por celula + sueno mas barato. Se aplica una vez sobre mini_llm.py."""
src = open('mini_llm.py', encoding='utf-8').read()
if 'adaptativa' in src: raise SystemExit('ya aplicado')
R = [
("""                 barajar=False, compuerta=True, E0=1.0):
        super().__init__(model, C, seed)
        self.W = np.zeros((0, KD)); self.Vv = np.zeros(0, int); self.E = np.zeros(0); self.conf = np.zeros(0)""",
"""                 barajar=False, compuerta=True, E0=1.0, adaptativa=False, th0=0.9):
        super().__init__(model, C, seed); self.adaptativa, self.th0 = adaptativa, th0
        self.W = np.zeros((0, KD)); self.Vv = np.zeros(0, int); self.E = np.zeros(0); self.conf = np.zeros(0); self.th = np.zeros(0)"""),
("""            s = self.W @ x; self.ops += 2 * self.W.size; cand = s > self.theta
            act = (cand & (self.Vv != yf) & (self.conf > 0)) if self.compuerta else np.ones(self.N, bool)""",
"""            s = self.W @ x; self.ops += 2 * self.W.size; cand = s > (self.th if self.adaptativa else self.theta)
            act = (cand & (self.Vv != yf) & (self.conf > 0)) if self.compuerta else np.ones(self.N, bool)"""),
("""        self.mue += int((~viva).sum()); self.W, self.Vv, self.E, self.conf = self.W[viva], self.Vv[viva], self.E[viva], self.conf[viva]
        self.origen""",
"""        self.mue += int((~viva).sum()); self.W, self.Vv, self.E, self.conf, self.th = self.W[viva], self.Vv[viva], self.E[viva], self.conf[viva], self.th[viva]
        self.origen"""),
("""                elif r != c and yf == c:                                 # pise donde la base ACERTABA: suelto y muero
                    self.conf[k] = 0.0; self.E[k] = -1.0
                elif r != c:                                             # fallamos las dos: corrijo mi valor
                    self.E[k] -= self.castigo; self.Vv[k] = c
                    if win is not None: self.ep[k] = (win, c)
                    self.W[k] += self.eta * (x - self.W[k]); self.W[k] /= np.linalg.norm(self.W[k])""",
"""                elif r != c and yf == c:                                 # pise donde la base ACERTABA
                    if self.adaptativa and float(self.W[k] @ x) < 0.995:  # estrecho mi radio hasta dejar fuera este estado
                        self.th[k] = max(self.th[k], float(self.W[k] @ x) + 0.002); self.E[k] -= self.castigo; self.estrechadas += 1
                    else: self.conf[k] = 0.0; self.E[k] = -1.0            # suelto y muero
                elif r != c:                                             # fallamos las dos
                    if self.adaptativa and float(self.W[k] @ x) < 0.995:  # otro contexto parecido: estrecho, no cambio de valor
                        self.th[k] = max(self.th[k], float(self.W[k] @ x) + 0.002); self.E[k] -= self.castigo; self.estrechadas += 1
                    else:                                                # el mismo contexto: el hecho cambio, corrijo mi valor
                        self.E[k] -= self.castigo; self.Vv[k] = c
                        if win is not None: self.ep[k] = (win, c)
                        self.W[k] += self.eta * (x - self.W[k]); self.W[k] /= np.linalg.norm(self.W[k])"""),
("""            self.conf = np.append(self.conf, 1.0); self.origen.append(maestro); self.ep.append((win, c))
            self.nac += 1; self.nac_por[maestro] = self.nac_por.get(maestro, 0) + 1
    def procesa""",
"""            self.conf = np.append(self.conf, 1.0); self.th = np.append(self.th, self.th0); self.origen.append(maestro); self.ep.append((win, c))
            self.nac += 1; self.nac_por[maestro] = self.nac_por.get(maestro, 0) + 1
    def procesa"""),
("self.nac = self.mue = self.pisadas = self.pisadas_ok = 0; self.nac_por = {}",
 "self.nac = self.mue = self.pisadas = self.pisadas_ok = self.estrechadas = 0; self.nac_por = {}"),
("""            s = self.W @ x; self.ops += 2 * self.W.size; cand = s > self.theta
            act = cand & (self.Vv != yf) & self.val""",
"""            s = self.W @ x; self.ops += 2 * self.W.size; cand = s > (self.th if self.adaptativa else self.theta)
            act = cand & (self.Vv != yf) & self.val"""),
("""            self.conf = np.append(self.conf, 0.0); self.val = np.append(self.val, False); self.confirm = np.append(self.confirm, 0.0)""",
"""            self.conf = np.append(self.conf, 0.0); self.val = np.append(self.val, False); self.confirm = np.append(self.confirm, 0.0); self.th = np.append(self.th, self.th0)"""),
("""                else:                                                     # validada que falla: vuelve a hipotesis (registro de errores)
                    self.reversiones += 1""",
"""                elif self.adaptativa and float(self.W[k] @ x) < 0.995:    # otro contexto parecido: estrecho el radio, sigo validada
                    self.th[k] = max(self.th[k], float(self.W[k] @ x) + 0.002); self.E[k] -= self.castigo; self.estrechadas += 1
                else:                                                     # validada que falla EN SU contexto: vuelve a hipotesis (registro de errores)
                    self.reversiones += 1"""),
("""                else:
                    self.sombra_mal += 1; self.confirm[i] -= 1; self.E[i] -= self.pierde_sombra
                    if len(vals_ok): self.confirm[i] -= 1                 # contradice a una validada que acerto""",
"""                elif self.adaptativa and float(self.W[i] @ x) < 0.995:
                    self.th[i] = max(self.th[i], float(self.W[i] @ x) + 0.002); self.estrechadas += 1
                else:
                    self.sombra_mal += 1; self.confirm[i] -= 1; self.E[i] -= self.pierde_sombra
                    if len(vals_ok): self.confirm[i] -= 1                 # contradice a una validada que acerto"""),
("""    if nombre == 'colonia': return Colonia(model, C, seed, theta=theta)
    if nombre == 'col_barajada': return Colonia(model, C, seed, theta=theta, barajar=True)
    if nombre == 'col_sin_compuerta': return Colonia(model, C, seed, theta=theta, compuerta=False)
    if nombre == 'cuarentena': return Cuarentena(model, C, seed, theta=theta)
    if nombre == 'cuarentena_k3': return Cuarentena(model, C, seed, theta=theta, k=3)
    if nombre == 'sueno': return Sueno(model, C, seed, corpus_tok=corpus_tok, theta=theta)
    if nombre == 'sueno_cuarentena': return SuenoCuarentena(model, C, seed, corpus_tok=corpus_tok, theta=theta)""",
"""    if nombre == 'colonia': return Colonia(model, C, seed, theta=theta, adaptativa=True)
    if nombre == 'col_fija': return Colonia(model, C, seed, theta=theta)
    if nombre == 'col_barajada': return Colonia(model, C, seed, theta=theta, adaptativa=True, barajar=True)
    if nombre == 'col_sin_compuerta': return Colonia(model, C, seed, theta=theta, compuerta=False)
    if nombre == 'cuarentena': return Cuarentena(model, C, seed, theta=theta, adaptativa=True)
    if nombre == 'cuarentena_fija': return Cuarentena(model, C, seed, theta=theta)
    if nombre == 'sueno': return Sueno(model, C, seed, corpus_tok=corpus_tok, theta=theta, adaptativa=True)
    if nombre == 'sueno_cuarentena': return SuenoCuarentena(model, C, seed, corpus_tok=corpus_tok, theta=theta, adaptativa=True)"""),
("def __init__(self, model, C, seed, cada=1500, pasos=20, lr=1e-3, ensayo=True, corpus_tok=None, **kw):",
 "def __init__(self, model, C, seed, cada=1500, pasos=10, lr=1e-3, ensayo=True, corpus_tok=None, **kw):"),
("""        if not sel: return
        X = np.array([self.ep[i][0] for i in sel]); y = np.array([self.ep[i][1] for i in sel])""",
"""        if not sel: return
        if len(sel) > 96: sel = sorted(self.rng.choice(sel, 96, replace=False).tolist())      # tope por sueno (costo)
        X = np.array([self.ep[i][0] for i in sel]); y = np.array([self.ep[i][1] for i in sel])"""),
("xr, _ = lote(self.rng, self.corpus_tok, max(len(y), 32))", "xr, _ = lote(self.rng, self.corpus_tok, min(max(len(y), 32), 64))"),
("r['pisadas_ok'] = getattr(br, 'pisadas_ok', 0);", "r['pisadas_ok'] = getattr(br, 'pisadas_ok', 0); r['estrechadas'] = getattr(br, 'estrechadas', 0);"),
("ap.add_argument('--lam', type=float, default=0.3)", "ap.add_argument('--lam', type=float, default=0.4)"),
("ap.add_argument('--theta', type=float, default=0.9)", "ap.add_argument('--theta', type=float, default=0.98)"),
]
for a, b in R:
    assert src.count(a) == 1, a[:80]
    src = src.replace(a, b)
open('mini_llm.py', 'w', encoding='utf-8').write(src); print('parche aplicado')
