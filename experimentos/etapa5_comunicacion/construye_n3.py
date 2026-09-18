"""Genera mundo_social_n3.py = mundo_social.py (946ff1c71e375eba) + N3: mascaras de retina por organismo, kwargs por
organismo y gamma_soc (la ultima senal honesta oida sobre el patron sesga la DECISION del receptor). Con gamma_soc=0 y
sin mascaras es mundo_social EXACTO (identidad obligatoria). Anclas con conteo exacto.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(AQUI, 'mundo_social.py')
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    (["                 gamma_sim=0.0, baseline_q=False, rho_b=0.05, alinea=False):"],
     ["                 gamma_sim=0.0, baseline_q=False, rho_b=0.05, alinea=False, gamma_soc=0.0, tau_soc=400, escucha=True):   # N3 (+escucha: N3b, ERR-23)"], 1, 'firma init'),
    (["        self.alinea = alinea; self.alineaciones = 0   # N2e: el simbolo toma el valor de lo que el receptor ya conoce"],
     ["        self.alinea = alinea; self.alineaciones = 0   # N2e: el simbolo toma el valor de lo que el receptor ya conoce",
      "        self.gamma_soc = gamma_soc; self.tau_soc = tau_soc; self.s_ult = {}; self.n_sesgo_soc = 0; self.escucha = escucha   # N3: ultima senal honesta oida por patron; N3b: si no escucha, no recibe nada"], 1, 'init N3'),
    (["                        else: orgs[j].recibir(kk, s, f_vicaria, val, t, invertir_en)"],
     ["                        elif orgs[j].escucha: orgs[j].recibir(kk, s, f_vicaria, val, t, invertir_en)   # N3b (ERR-23): el que no escucha no recibe"], 1, 'escucha'),
    # N3c: mundo con reaparicion en el MISMO sitio (regen): equilibra visitas a comida y veneno. regen=None -> identico.
    (["class Mundo:",
      "    def __init__(self, rng, nobj, tipos):",
      "        self.rng = rng; self.nobj = nobj; self.tipos = tipos; self.objs = {}",
      "",
      "    def spawn(self):",
      "        while len(self.objs) < self.nobj:",
      "            x = int(self.rng.integers(L))",
      "            if x not in self.objs: self.objs[x] = self.tipos[int(self.rng.integers(len(self.tipos)))]"],
     ["class Mundo:",
      "    def __init__(self, rng, nobj, tipos, regen=None):",
      "        self.rng = rng; self.nobj = nobj; self.tipos = tipos; self.objs = {}; self.regen = regen; self.pend = {}   # N3c: regen",
      "",
      "    def spawn(self):",
      "        while len(self.objs) + len(self.pend) < self.nobj:",
      "            x = int(self.rng.integers(L))",
      "            if x not in self.objs and x not in self.pend: self.objs[x] = self.tipos[int(self.rng.integers(len(self.tipos)))]",
      "",
      "    def retirar(self, x, t):   # N3c: al morder (o al olvido) el objeto se va; con regen vuelve al MISMO sitio con el mismo tipo",
      "        kk = self.objs.pop(x)",
      "        if self.regen is not None:",
      "            self.pend[x] = (kk, t + self.regen)",
      "            if not self.objs:   # nunca vacio: si se agotaron todos, el pendiente mas antiguo vuelve ya (see() no admite mundo vacio)",
      "                x0 = min(self.pend, key=lambda y: self.pend[y][1]); kk0, _ = self.pend.pop(x0); self.objs[x0] = kk0",
      "        self.spawn()",
      "",
      "    def regenerar(self, t):",
      "        for x in [x for x, (kk, tt) in self.pend.items() if tt <= t]:",
      "            kk, _ = self.pend.pop(x); self.objs[x] = kk"], 1, 'Mundo regen'),
    (["                del objs[self.pos]; mundo.spawn()"], ["                mundo.retirar(self.pos, t)   # N3c (regen=None: identico a del + spawn)"], 1, 'retirar mordida'),
    (["            _dx = list(mundo.objs)[int(mundo.rng.integers(len(mundo.objs)))]; del mundo.objs[_dx]; mundo.spawn()"],
     ["            _dx = list(mundo.objs)[int(mundo.rng.integers(len(mundo.objs)))]; mundo.retirar(_dx, t)   # N3c"], 1, 'retirar olvido'),
    (["    mundo_ = Mundo(rng_mundo, nobj_por_org * n, tipos); mundo_.spawn()"],
     ["    mundo_ = Mundo(rng_mundo, nobj_por_org * n, tipos, regen=regen); mundo_.spawn()   # N3c"], 1, 'Mundo()'),
    (["    for t in range(T):",
      "        if invertir_en is not None and t == invertir_en and 'A' in val and 'B' in val: val = {'A': 'veneno', 'B': 'comida'}"],
     ["    for t in range(T):",
      "        if mundo.pend: mundo.regenerar(t)   # N3c",
      "        if invertir_en is not None and t == invertir_en and 'A' in val and 'B' in val: val = {'A': 'veneno', 'B': 'comida'}"], 1, 'regenerar'),
    (["                _wt = _wt + self.gamma_sim * float(self.M[self.ultimo[kk][0]] - self.M.mean())"],
     ["                _wt = _wt + self.gamma_sim * float(self.M[self.ultimo[kk][0]] - self.M.mean())",
      "            if self.gamma_soc and kk in self.s_ult and t - self.s_ult[kk][1] <= self.tau_soc:   # N3: la conducta ajena reciente sesga la decision",
      "                _wt = _wt + self.gamma_soc * self.s_ult[kk][0]; self.n_sesgo_soc += 1"], 1, 'boca N3'),
    (["        \"\"\"Aprendizaje vicario: la señal dice +/− del patron kk; escala innata + -> +1, − -> −3. Sin divisiones.\"\"\"",
      "        if not self.learn: return"],
     ["        \"\"\"Aprendizaje vicario: la señal dice +/− del patron kk; escala innata + -> +1, − -> −3. Sin divisiones.\"\"\"",
      "        if self.gamma_soc: self.s_ult[kk] = (1.0 if signo > 0 else -1.0, t)   # N3",
      "        if not self.learn: return"], 1, 'recibir N3'),
    (["        return dict(W=W, comp=comp, W_lenta=W_lenta, mord=self.mord, vis=self.vis, deaths=self.deaths, splits=self.splits, split_t=self.split_t,"],
     ["        return dict(W=W, comp=comp, W_lenta=W_lenta, mord=self.mord, vis=self.vis, deaths=self.deaths, splits=self.splits, split_t=self.split_t, n_sesgo_soc=self.n_sesgo_soc,"], 1, 'resultado'),
    (["        estados=None, devolver_estado=False, mundo='AB', regla='azar', tau_s=200, K_sim=2, estado_emisor='conducta', u_v=0.5, **kw_org):"],
     ["        estados=None, devolver_estado=False, mundo='AB', regla='azar', tau_s=200, K_sim=2, estado_emisor='conducta', u_v=0.5,",
      "        mascaras=None, kw_por_org=None, regen=None, **kw_org):   # N3: mascara de retina y kwargs por organismo; N3c: regen"], 1, 'firma run'),
    (["    orgs = [Organismo(rngs[i], T, estado=(estados[i] if estados else None), pats=pats, mundo=mundo, rng_q=rngs_q[i], K_sim=K_sim, **kw_org)",
      "            for i in range(n)]"],
     ["    _pats_i = lambda i: pats if (mascaras is None or mascaras[i] is None) else {k: v * np.asarray(mascaras[i], float) for k, v in pats.items()}   # N3",
      "    _kw_i = lambda i: dict(kw_org, **(kw_por_org[i] if kw_por_org else {}))",
      "    orgs = [Organismo(rngs[i], T, estado=(estados[i] if estados else None), pats=_pats_i(i), mundo=mundo, rng_q=rngs_q[i], K_sim=K_sim, **_kw_i(i))",
      "            for i in range(n)]"], 1, 'orgs'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != '946ff1c71e375eba':
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != 946ff1c71e375eba")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_social_n3 = mundo_social.py (946ff1c71e375eba) + N3: mascaras de retina por organismo, kwargs por organismo y' + NL +
           'gamma_soc (la ultima senal honesta oida sobre el patron sesga la decision del receptor). Generado por construye_n3.py.' + NL +
           'NO editar. Con gamma_soc=0 y sin mascaras es mundo_social exacto (identidad obligatoria)."""' + NL)
    d = os.path.join(AQUI, 'mundo_social_n3.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
