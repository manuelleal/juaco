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
      "    def __init__(self, rng, nobj, tipos, regen=None, fijos=None):",
      "        self.rng = rng; self.nobj = nobj; self.tipos = tipos; self.objs = {}; self.regen = regen; self.pend = {}   # N3c: regen",
      "        self.fijos = list(fijos) if fijos else None   # N3d: tipos iniciales fijos (en orden), en vez de sortearlos",
      "",
      "    def spawn(self):",
      "        while len(self.objs) + len(self.pend) < self.nobj:",
      "            x = int(self.rng.integers(L))",
      "            if x not in self.objs and x not in self.pend: self.objs[x] = self.fijos.pop(0) if self.fijos else self.tipos[int(self.rng.integers(len(self.tipos)))]",
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
     ["    mundo_ = Mundo(rng_mundo, nobj_por_org * n, tipos, regen=regen, fijos=tipos_fijos); mundo_.spawn()   # N3c / N3d"], 1, 'Mundo()'),
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
      "        mascaras=None, kw_por_org=None, regen=None, tipos_fijos=None, mudo_desde=None, **kw_org):   # N3: mascara de retina y kwargs por organismo; N3c: regen; N3d: tipos_fijos; N3d-mudo: mudo_desde"], 1, 'firma run'),
    (["        if senal is not None and n > 1:",
      "            for i, px, kk, signo in emitidas:"],
     ["        if senal is not None and n > 1 and (mudo_desde is None or t < mudo_desde):   # N3d-mudo: desde mudo_desde no se entrega nada",
      "            for i, px, kk, signo in emitidas:"], 1, 'mudo'),
    (["    orgs = [Organismo(rngs[i], T, estado=(estados[i] if estados else None), pats=pats, mundo=mundo, rng_q=rngs_q[i], K_sim=K_sim, **kw_org)",
      "            for i in range(n)]"],
     ["    _pats_i = lambda i: pats if (mascaras is None or mascaras[i] is None) else {k: v * np.asarray(mascaras[i], float) for k, v in pats.items()}   # N3",
      "    _kw_i = lambda i: dict(kw_org, **(kw_por_org[i] if kw_por_org else {}))",
      "    orgs = [Organismo(rngs[i], T, estado=(estados[i] if estados else None), pats=_pats_i(i), mundo=mundo, rng_q=rngs_q[i], K_sim=K_sim, **_kw_i(i))",
      "            for i in range(n)]"], 1, 'orgs'),

    # ---------------------------------------------------------------------------------------------------------------
    # N2f (bloque 5 del plan del dia 6). DOS perillas SEPARABLES, las dos apagadas por defecto:
    #   (1) MUNDO   regen_rota: al reaparecer un sitio, el tipo se vuelve a SORTEAR de self.tipos con el RNG del mundo.
    #       Asi hay reaparicion en el mismo sitio (visitas equilibradas, N3c) Y flujo de patrones (los 10 de test
    #       aparecen). Con regen_rota=False vuelve el mismo tipo: N3c/N3d bit a bit.
    #   (2) RECEPTOR escucha_si_no_sabe: el empujon vicario del simbolo NO se aplica si el receptor ya sabe del patron
    #       mas de lo que el simbolo dice (|valor(kk)| >= |R_hat|). Consecuencia directa del humo del 17-sep: con el
    #       simbolo en magnitud (C = +-1.28) el empujon rebajaba W de -2.45 a -1.29 y el veneno subia de 34 a 135.
    #       Con escucha_si_no_sabe=False, `valor(kk)` ni se evalua (cortocircuito): identico a lo actual.
    # Los anclas de este bloque muerden el texto YA PARCHEADO por los bloques N3/N3b/N3c/N3d de arriba.
    # ---------------------------------------------------------------------------------------------------------------
    (["    def __init__(self, rng, nobj, tipos, regen=None, fijos=None):",
      "        self.rng = rng; self.nobj = nobj; self.tipos = tipos; self.objs = {}; self.regen = regen; self.pend = {}   # N3c: regen",
      "        self.fijos = list(fijos) if fijos else None   # N3d: tipos iniciales fijos (en orden), en vez de sortearlos"],
     ["    def __init__(self, rng, nobj, tipos, regen=None, fijos=None, regen_rota=False):",
      "        self.rng = rng; self.nobj = nobj; self.tipos = tipos; self.objs = {}; self.regen = regen; self.pend = {}   # N3c: regen",
      "        self.fijos = list(fijos) if fijos else None   # N3d: tipos iniciales fijos (en orden), en vez de sortearlos",
      "        self.regen_rota = regen_rota   # N2f: al reaparecer, el tipo se vuelve a sortear (mismo sitio + FLUJO de patrones)",
      "",
      "    def _reaparece(self, kk):   # N2f: con regen_rota=False devuelve el MISMO tipo -> N3c/N3d bit a bit, sin tocar el RNG",
      "        return self.tipos[int(self.rng.integers(len(self.tipos)))] if self.regen_rota else kk"], 1, 'N2f Mundo init'),
    (["                x0 = min(self.pend, key=lambda y: self.pend[y][1]); kk0, _ = self.pend.pop(x0); self.objs[x0] = kk0"],
     ["                x0 = min(self.pend, key=lambda y: self.pend[y][1]); kk0, _ = self.pend.pop(x0); self.objs[x0] = self._reaparece(kk0)   # N2f"], 1, 'N2f retirar vacio'),
    (["    def regenerar(self, t):",
      "        for x in [x for x, (kk, tt) in self.pend.items() if tt <= t]:",
      "            kk, _ = self.pend.pop(x); self.objs[x] = kk"],
     ["    def regenerar(self, t):",
      "        for x in [x for x, (kk, tt) in self.pend.items() if tt <= t]:",
      "            kk, _ = self.pend.pop(x); self.objs[x] = self._reaparece(kk)   # N2f"], 1, 'N2f regenerar'),
    (["        mascaras=None, kw_por_org=None, regen=None, tipos_fijos=None, mudo_desde=None, **kw_org):   # N3: mascara de retina y kwargs por organismo; N3c: regen; N3d: tipos_fijos; N3d-mudo: mudo_desde"],
     ["        mascaras=None, kw_por_org=None, regen=None, tipos_fijos=None, mudo_desde=None, regen_rota=False, **kw_org):   # N3: mascara de retina y kwargs por organismo; N3c: regen; N3d: tipos_fijos; N3d-mudo: mudo_desde; N2f: regen_rota"], 1, 'N2f firma run'),
    (["    mundo_ = Mundo(rng_mundo, nobj_por_org * n, tipos, regen=regen, fijos=tipos_fijos); mundo_.spawn()   # N3c / N3d"],
     ["    mundo_ = Mundo(rng_mundo, nobj_por_org * n, tipos, regen=regen, fijos=tipos_fijos, regen_rota=regen_rota); mundo_.spawn()   # N3c / N3d / N2f"], 1, 'N2f Mundo()'),
    (["                 gamma_sim=0.0, baseline_q=False, rho_b=0.05, alinea=False, gamma_soc=0.0, tau_soc=400, escucha=True):   # N3 (+escucha: N3b, ERR-23)"],
     ["                 gamma_sim=0.0, baseline_q=False, rho_b=0.05, alinea=False, gamma_soc=0.0, tau_soc=400, escucha=True,",
      "                 escucha_si_no_sabe=False):   # N3 (+escucha: N3b, ERR-23); N2f: escucha_si_no_sabe"], 1, 'N2f firma init'),
    (["        self.gamma_soc = gamma_soc; self.tau_soc = tau_soc; self.s_ult = {}; self.n_sesgo_soc = 0; self.escucha = escucha   # N3: ultima senal honesta oida por patron; N3b: si no escucha, no recibe nada"],
     ["        self.gamma_soc = gamma_soc; self.tau_soc = tau_soc; self.s_ult = {}; self.n_sesgo_soc = 0; self.escucha = escucha   # N3: ultima senal honesta oida por patron; N3b: si no escucha, no recibe nada",
      "        self.escucha_si_no_sabe = escucha_si_no_sabe; self.no_desensena = 0   # N2f: el simbolo no reescribe un valor propio MAS informado que el"], 1, 'N2f init receptor'),
    (["        R_hat = float(self.M[s] - self.M.mean())",
      "        if self.learn and abs(R_hat) >= self.u_m:"],
     ["        R_hat = float(self.M[s] - self.M.mean())",
      "        # N2f: el que ya sabe del patron mas de lo que el simbolo dice no se deja desensenar (cortocircuito: con la",
      "        # perilla apagada `valor(kk)` ni se evalua, y `valor`/`kenyon`/`code` no tocan estado ni RNG).",
      "        _sabe_mas = self.escucha_si_no_sabe and abs(self.valor(kk)) >= abs(R_hat)",
      "        if _sabe_mas and abs(R_hat) >= self.u_m: self.no_desensena += 1",
      "        if self.learn and abs(R_hat) >= self.u_m and not _sabe_mas:"], 1, 'N2f puerta desensenar'),
    (["                    t_ext_B=self.t_ext_B, t_B_ok=self.t_B_ok, M=[round(float(x), 3) for x in self.M], simbolos_recibidos=self.simbolos_recibidos,"],
     ["                    t_ext_B=self.t_ext_B, t_B_ok=self.t_B_ok, M=[round(float(x), 3) for x in self.M], simbolos_recibidos=self.simbolos_recibidos, no_desensena=self.no_desensena,"], 1, 'N2f resultado'),

    # ---------------------------------------------------------------------------------------------------------------
    # N2f-v3 (tercera perilla, decidida por el coordinador tras el humo de la v2). MUNDO: `vida`.
    #   Causa medida en el humo de la v2: un objeto solo se retira CUANDO SE MUERDE, asi que la comida rota y el veneno
    #   rechazado se queda para siempre -> con regen_rota el mundo es una cadena ABSORBENTE que acaba en veneno
    #   (razon comida/veneno 0.037 -> 0.015 por cuarto). Balance y flujo eran incompatibles.
    #   `vida`: cada objeto caduca en t_nace + vida y se retira POR EL MISMO CAMINO que una mordida (`retirar` ->
    #   pend/regen y rotacion segun las otras perillas). Asi el veneno tambien sale del mundo.
    #   Con vida=None no se llama nunca a `caducar`; `self.t`/`self.nace` son contabilidad que no toca el RNG: identico.
    # ---------------------------------------------------------------------------------------------------------------
    (["    def __init__(self, rng, nobj, tipos, regen=None, fijos=None, regen_rota=False):",
      "        self.rng = rng; self.nobj = nobj; self.tipos = tipos; self.objs = {}; self.regen = regen; self.pend = {}   # N3c: regen",
      "        self.fijos = list(fijos) if fijos else None   # N3d: tipos iniciales fijos (en orden), en vez de sortearlos",
      "        self.regen_rota = regen_rota   # N2f: al reaparecer, el tipo se vuelve a sortear (mismo sitio + FLUJO de patrones)"],
     ["    def __init__(self, rng, nobj, tipos, regen=None, fijos=None, regen_rota=False, vida=None):",
      "        self.rng = rng; self.nobj = nobj; self.tipos = tipos; self.objs = {}; self.regen = regen; self.pend = {}   # N3c: regen",
      "        self.fijos = list(fijos) if fijos else None   # N3d: tipos iniciales fijos (en orden), en vez de sortearlos",
      "        self.regen_rota = regen_rota   # N2f: al reaparecer, el tipo se vuelve a sortear (mismo sitio + FLUJO de patrones)",
      "        self.vida = vida; self.nace = {}; self.t = 0; self.caducados = 0   # N2f-v3: el objeto caduca a t_nace + vida (el veneno tambien sale del mundo)"], 1, 'v3 Mundo init'),
    (["            if x not in self.objs and x not in self.pend: self.objs[x] = self.fijos.pop(0) if self.fijos else self.tipos[int(self.rng.integers(len(self.tipos)))]"],
     ["            if x not in self.objs and x not in self.pend:",
      "                self.objs[x] = self.fijos.pop(0) if self.fijos else self.tipos[int(self.rng.integers(len(self.tipos)))]",
      "                self.nace[x] = self.t   # N2f-v3: sello de nacimiento (con vida=None no se usa)"], 1, 'v3 spawn'),
    (["                x0 = min(self.pend, key=lambda y: self.pend[y][1]); kk0, _ = self.pend.pop(x0); self.objs[x0] = self._reaparece(kk0)   # N2f"],
     ["                x0 = min(self.pend, key=lambda y: self.pend[y][1]); kk0, _ = self.pend.pop(x0); self.objs[x0] = self._reaparece(kk0); self.nace[x0] = self.t   # N2f / N2f-v3"], 1, 'v3 retirar vacio'),
    (["    def regenerar(self, t):",
      "        for x in [x for x, (kk, tt) in self.pend.items() if tt <= t]:",
      "            kk, _ = self.pend.pop(x); self.objs[x] = self._reaparece(kk)   # N2f"],
     ["    def regenerar(self, t):",
      "        for x in [x for x, (kk, tt) in self.pend.items() if tt <= t]:",
      "            kk, _ = self.pend.pop(x); self.objs[x] = self._reaparece(kk); self.nace[x] = t   # N2f / N2f-v3",
      "",
      "    def caducar(self, t):   # N2f-v3: lo que lleva `vida` pasos sin que nadie lo muerda se retira igual que si lo hubieran mordido",
      "        for x in [x for x in self.objs if t - self.nace.get(x, 0) >= self.vida]:",
      "            if x in self.objs: self.retirar(x, t); self.caducados += 1"], 1, 'v3 regenerar+caducar'),
    (["        mascaras=None, kw_por_org=None, regen=None, tipos_fijos=None, mudo_desde=None, regen_rota=False, **kw_org):   # N3: mascara de retina y kwargs por organismo; N3c: regen; N3d: tipos_fijos; N3d-mudo: mudo_desde; N2f: regen_rota"],
     ["        mascaras=None, kw_por_org=None, regen=None, tipos_fijos=None, mudo_desde=None, regen_rota=False, vida=None, **kw_org):   # N3: mascara de retina y kwargs por organismo; N3c: regen; N3d: tipos_fijos; N3d-mudo: mudo_desde; N2f: regen_rota; N2f-v3: vida"], 1, 'v3 firma run'),
    (["    mundo_ = Mundo(rng_mundo, nobj_por_org * n, tipos, regen=regen, fijos=tipos_fijos, regen_rota=regen_rota); mundo_.spawn()   # N3c / N3d / N2f"],
     ["    mundo_ = Mundo(rng_mundo, nobj_por_org * n, tipos, regen=regen, fijos=tipos_fijos, regen_rota=regen_rota, vida=vida); mundo_.spawn()   # N3c / N3d / N2f / N2f-v3"], 1, 'v3 Mundo()'),
    (["        if mundo.pend: mundo.regenerar(t)   # N3c"],
     ["        mundo.t = t   # N2f-v3: reloj del mundo para el sello de nacimiento (con vida=None no cambia nada)",
      "        if mundo.pend: mundo.regenerar(t)   # N3c",
      "        if mundo.vida is not None: mundo.caducar(t)   # N2f-v3"], 1, 'v3 caducar en el bucle'),
    (["        out[i]['senales_emitidas'] = senales_emitidas[i]; out[i]['senales_recibidas'] = senales_recibidas[i]"],
     ["        out[i]['senales_emitidas'] = senales_emitidas[i]; out[i]['senales_recibidas'] = senales_recibidas[i]; out[i]['caducados'] = mundo.caducados   # N2f-v3"], 1, 'v3 caducados'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != '946ff1c71e375eba':
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != 946ff1c71e375eba")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_social_n3 = mundo_social.py (946ff1c71e375eba) + N3: mascaras de retina por organismo, kwargs por organismo y' + NL +
           'gamma_soc (la ultima senal honesta oida sobre el patron sesga la decision del receptor). Generado por construye_n3.py.' + NL +
           'NO editar. Con gamma_soc=0 y sin mascaras es mundo_social exacto (identidad obligatoria).' + NL +
           'N2f: + regen_rota (al reaparecer, el tipo se vuelve a sortear: mismo sitio Y flujo de patrones),' + NL +
           'escucha_si_no_sabe (el simbolo no reescribe un valor propio mas informado) y vida (el objeto caduca aunque' + NL +
           'nadie lo muerda: el veneno tambien sale). Las tres apagadas = N3c/N3d bit a bit."""' + NL)
    d = os.path.join(AQUI, 'mundo_social_n3.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
