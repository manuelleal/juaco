"""construye_gramatica.py — CONSTRUYE POR ANCLAS el instrumento de ORGANELOS / GRAMATICA (Opus A, 24-sep-2026). No se edita a mano.

MISION: llegar a la AGI por este camino.

Origenes (SOLO se LEEN; sha fijado):
  experimentos/juaco_eco/motor_eco2.py            0921ee3a50ce7f7a -> motor_gramatica.py
  experimentos/juaco_eco/carros/FAMB_ORG_ECO.py   75d5f4118079ff15 -> carros/FAMB_GRAM_ECO.py
(motor_eco3.py 2eec9830792d9822 difiere de motor_eco2 SOLO en la tabla GENES: no tiene 'ensena'. El instrumento de ECO v2.1, el que paso,
 es motor_eco2 + FAMB_ORG_ECO; el arnes compara ademas motor_eco3 == motor_eco2 con los organos apagados.)

motor_gramatica = motor_eco2 + (solo con eco['gramatica'] != None):
  G1 cada cuerpo lleva una GRAMATICA (gr: tupla de slots, gramatica_def.py) y n_sombra gramaticas SOMBRA (gs) que derivan igual y no se
     expresan; el banco del vivero guarda (g, s, gr, gs); el hijo copia la gramatica del donante (padre, o banco al azar en AZAR) con
     errores de copia (gramatica_def.muta_gram) con rng propios [seed, linaje, 20|21, k]: NO toca ningun rng del motor_eco2.
  G2 el ctx del cerebro trae ctx['gramatica']; el carro la lee (con None el carro es FAMB_ORG_ECO).
  G3 entregas: al PARIR (antes de crear al hijo), EN VIDA (cada PER_VIDA pasos de edad, al final del turno de fase B del cuerpo) y al
     MORIR (antes de c.muere): el motor pide c.emite(evento) y entrega cada paquete al destinatario mas cercano en el anillo (hijo: hijo
     vivo del emisor; hermano: mismo linaje y mismo padre; vecino: cualquier cuerpo vivo); empate -> el primero en la lista de cuerpos;
     sin rng. El paquete hijo/nacer viaja por al_parir/nace (el camino de FAMB_ORG_ECO).
  G4 salida: r['gram'] (banco y vivos con sus gramaticas, en el corte y al final; contadores). r['eco'] no cambia.
FAMB_GRAM_ECO = FAMB_ORG_ECO + la gramatica (al_parir/nace por paquetes; emite; recibe; _funde aplica el COMO del emisor en el receptor).
Uso: python experimentos/organelos/gramatica/construye_gramatica.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')
ORIG_MOTOR = os.path.join(ECO, 'motor_eco2.py'); SHA_MOTOR = '0921ee3a50ce7f7a'
ORIG_CARRO = os.path.join(ECO, 'carros', 'FAMB_ORG_ECO.py'); SHA_CARRO = '75d5f4118079ff15'
DEST_MOTOR = os.path.join(AQUI, 'motor_gramatica.py')
DEST_CARRO = os.path.join(AQUI, 'carros', 'FAMB_GRAM_ECO.py')


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def h16s(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


def aplica(txt, anclas, nombre):
    for i, (a, b) in enumerate(anclas):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"CONSTRUYE {nombre}: ancla {i} aparece {n} veces (debe ser 1): {a[:70]!r}")
        txt = txt.replace(a, b)
    return txt


# ============================================================================================ MOTOR
ANCLAS_MOTOR = [
    ('"""motor_eco2.py (CONSTRUIDO',
     '"""motor_gramatica.py (CONSTRUIDO por experimentos/organelos/gramatica/construye_gramatica.py desde experimentos/juaco_eco/motor_eco2.py, '
     f'sha {SHA_MOTOR}; NO editar a mano).\nORGANELOS: + la GRAMATICA del organo de transmision (G1-G4, ver construye_gramatica.py). Con '
     "eco['gramatica'] = None es motor_eco2 BIT A BIT. Lo que sigue es el docstring del origen.\n\nmotor_eco2.py (CONSTRUIDO"),
    ("GEN = os.path.join(os.path.dirname(AQUI), 'generaciones')",
     "GEN = os.path.join(os.path.dirname(os.path.dirname(AQUI)), 'generaciones')"),
    ("               estado=None, ind_cb=None, mutables=None, banco=0, donante='padre', t_corte=None)\n",
     "               estado=None, ind_cb=None, mutables=None, banco=0, donante='padre', t_corte=None,\n"
     "               gramatica=None, g_pcampo=0.0, g_pdup=0.0, g_pdel=0.0, g_tope=4, g_alfabeto=None)   # ORGANELOS (G1)\n"),
    ("ETQ_BANCO = 18; ETQ_DONANTE = 19\n",
     "ETQ_BANCO = 18; ETQ_DONANTE = 19\n"
     "ETQ_GMUT = 20; ETQ_GSOMBRA = 21   # ORGANELOS: rng de los errores de copia de la gramatica (real y sombras); 22 = fundadores (runner)\n"
     "import gramatica_def as GD\n"),
    ("    E_['gs0'] = gs\n    return E_\n",
     "    E_['gs0'] = gs\n"
     "    if E_['gramatica'] is None: E_['gr0'] = None   # ORGANELOS (G1)\n"
     "    else:\n"
     "        _tp = int(E_['g_tope'])\n"
     "        if not 1 <= _tp <= 8: raise SystemExit('GRAMATICA: g_tope entre 1 y 8')\n"
     "        _grs = list(E_['gramatica'])\n"
     "        if len(_grs) != n: raise SystemExit(f'GRAMATICA: {len(_grs)} gramaticas para {n} fundadores')\n"
     "        E_['gr0'] = [GD.valida(x, _tp) for x in _grs]\n"
     "        E_['g_alf'] = GD.ALFABETO_TODO if E_['g_alfabeto'] is None else tuple(tuple(int(v) for v in a) for a in E_['g_alfabeto'])\n"
     "        E_['g_on'] = float(E_['g_pcampo']) > 0 or float(E_['g_pdup']) > 0 or float(E_['g_pdel']) > 0\n"
     "    return E_\n"),
    ("                 'ult_mordida', 'vol_kk', 'hijos', 'fund', 'vivo', 'hvivos', 'pc', 'g', 's')\n",
     "                 'ult_mordida', 'vol_kk', 'hijos', 'fund', 'vivo', 'hvivos', 'pc', 'g', 's', 'gr', 'gs')   # ORGANELOS: gr, gs\n"),
    ("self.pc = pc; self.g = None; self.s = None   # pc = cuerpo padre (vivo o no)\n",
     "self.pc = pc; self.g = None; self.s = None   # pc = cuerpo padre (vivo o no)\n"
     "        self.gr = None; self.gs = None   # ORGANELOS: gramatica real y sombras\n"),
    ("    E_ = None if eco is None else _eco_cfg(eco, CF, n)\n",
     "    E_ = None if eco is None else _eco_cfg(eco, CF, n)\n"
     "    _GR = E_ is not None and E_['gr0'] is not None   # ORGANELOS\n"),
    ("    def ctx_de(i, r, ident, g=None):\n",
     "    def ctx_de(i, r, ident, g=None, gr=None):\n"),
    ("        return _d if g is None else ctx_genoma(_d, g)\n",
     "        if gr is not None: _d['gramatica'] = gr   # ORGANELOS (G2)\n"
     "        return _d if g is None else ctx_genoma(_d, g)\n"),
    ("        c = mod.crea(ctx_de(i, rngs_fund[i], ids[i], (None if E_ is None else E_['gs0'][i])))\n",
     "        c = mod.crea(ctx_de(i, rngs_fund[i], ids[i], (None if E_ is None else E_['gs0'][i]), gr=(E_['gr0'][i] if _GR else None)))\n"),
    ("            cuerpos[-1].g = E_['gs0'][i].copy(); cuerpos[-1].s = np.tile(E_['gs0'][i], (int(E_['n_sombra']), 1))\n",
     "            cuerpos[-1].g = E_['gs0'][i].copy(); cuerpos[-1].s = np.tile(E_['gs0'][i], (int(E_['n_sombra']), 1))\n"
     "            if _GR: cuerpos[-1].gr = E_['gr0'][i]; cuerpos[-1].gs = (E_['gr0'][i],) * int(E_['n_sombra'])\n"),
    ("    def registra(b, tm, causa, vd):\n",
     "    def _muta_gr(gr, gs, i, k):   # ORGANELOS (G1): errores de copia de la gramatica real y de sus sombras (rng propios)\n"
     "        if not _GR: return None, None\n"
     "        if not E_['g_on']: return gr, gs\n"
     "        _a = (float(E_['g_pcampo']), float(E_['g_pdup']), float(E_['g_pdel']), int(E_['g_tope']), E_['g_alf'])\n"
     "        g2, nm = GD.muta_gram(gr, SE(i, ETQ_GMUT, k), *_a)\n"
     "        _rg = SE(i, ETQ_GSOMBRA, k); s2 = tuple(GD.muta_gram(x, _rg, *_a)[0] for x in gs)\n"
     "        ES['g_nmut'] = ES.get('g_nmut', 0) + nm\n"
     "        return g2, s2\n\n"
     "    def _destino(b, quien):   # ORGANELOS (G3): el destinatario mas cercano en el anillo; empate -> el primero de la lista; sin rng\n"
     "        best = None; bd = None\n"
     "        for z in cuerpos:\n"
     "            if z is b or not z.vivo: continue\n"
     "            if quien == 'hijo' and not (z.lin == b.lin and z.padre == b.k and not z.fund): continue\n"
     "            if quien == 'hermano' and not (b.padre >= 0 and not b.fund and z.lin == b.lin and z.padre == b.padre and not z.fund): continue\n"
     "            dd = abs(z.pos - b.pos); dd = min(dd, L - dd)\n"
     "            if bd is None or dd < bd: best = z; bd = dd\n"
     "        return best\n\n"
     "    def _entrega(b, paqs, ev):   # ORGANELOS (G3)\n"
     "        ce = ES.setdefault('g_ent', {})\n"
     "        for quien, paq in paqs:\n"
     "            z = _destino(b, quien); kk_ = f'{ev}/{quien}/{0 if z is None else 1}'; ce[kk_] = ce.get(kk_, 0) + 1\n"
     "            if z is not None: z.c.recibe(paq)\n\n"
     "    def registra(b, tm, causa, vd):\n"),
    ("    if E_ is not None and E_['banco']: ES['banco'] = [(b.g.copy(), b.s.copy()) for b in cuerpos][-int(E_['banco']):]   # E9\n",
     "    if E_ is not None and E_['banco']: ES['banco'] = [(b.g.copy(), b.s.copy(), b.gr, b.gs) for b in cuerpos][-int(E_['banco']):]   # E9 (+ ORGANELOS)\n"),
    ("                c.muere(dict(t=t, causa=_causa, causa_juez=cz, edad=edad, hijos=b.hijos))\n",
     "                if _GR and 'morir' in c.EV: _entrega(b, c.emite('morir'), 'morir')   # ORGANELOS (G3): antes de muere()\n"
     "                c.muere(dict(t=t, causa=_causa, causa_juez=cz, edad=edad, hijos=b.hijos))\n"),
    ("                _gf = _sf = None\n", "                _gf = _sf = _grf = _gsf = None\n"),
    ("                        _gb, _sb = ES['banco'][int(SE(i, ETQ_BANCO, l.nac).integers(len(ES['banco'])))]\n",
     "                        _gb, _sb, _grb, _gsb = ES['banco'][int(SE(i, ETQ_BANCO, l.nac).integers(len(ES['banco'])))]\n"),
    ("                        ES['n_banco'] += 1\n",
     "                        ES['n_banco'] += 1; _grf, _gsf = _muta_gr(_grb, _gsb, i, l.nac)\n"),
    ("                    else: _gf = E_['gs0'][i].copy(); _sf = np.tile(E_['gs0'][i], (int(E_['n_sombra']), 1))\n",
     "                    else:\n"
     "                        _gf = E_['gs0'][i].copy(); _sf = np.tile(E_['gs0'][i], (int(E_['n_sombra']), 1))\n"
     "                        if _GR: _grf = E_['gr0'][i]; _gsf = (_grf,) * int(E_['n_sombra'])\n"),
    ("                        ES['banco'].append((_gf.copy(), _sf.copy()))\n",
     "                        ES['banco'].append((_gf.copy(), _sf.copy(), _grf, _gsf))\n"),
    ("                cnew = mods[i][1].crea(ctx_de(i, rngs_fund[i], ids[i], _gf))\n",
     "                cnew = mods[i][1].crea(ctx_de(i, rngs_fund[i], ids[i], _gf, gr=_grf))\n"),
    ("                if E_ is not None: F.g = _gf; F.s = _sf\n",
     "                if E_ is not None: F.g = _gf; F.s = _sf; F.gr = _grf; F.gs = _gsf\n"),
    ("                    mem = c.al_parir(dict(t=t, k=l.desc))\n",
     "                    mem = c.al_parir(dict(t=t, k=l.desc))\n"
     "                    if _GR and 'nacer' in c.EV: _entrega(b, c.emite('nacer'), 'nacer')   # ORGANELOS (G3): hermano/vecino al parir\n"),
    ("                    _gh = _sh = None\n", "                    _gh = _sh = _grh = _gsh = None\n"),
    ("                        _dg, _ds = b.g, b.s\n", "                        _dg, _ds, _dgr, _dgs = b.g, b.s, b.gr, b.gs\n"),
    ("                            _dg, _ds = ES['banco'][int(SE(i, ETQ_DONANTE, k).integers(len(ES['banco'])))]\n",
     "                            _dg, _ds, _dgr, _dgs = ES['banco'][int(SE(i, ETQ_DONANTE, k).integers(len(ES['banco'])))]\n"),
    ("                        if E_['banco']:   # 'padre': el genoma del PADRE (fertilidad); 'azar': el genoma NUEVO\n"
     "                            ES['banco'].append((_dg.copy(), _ds.copy()) if E_['donante'] == 'padre' else (_gh.copy(), _sh.copy()))\n",
     "                        _grh, _gsh = _muta_gr(_dgr, _dgs, i, k)   # ORGANELOS (G1)\n"
     "                        if E_['banco']:   # 'padre': el genoma del PADRE (fertilidad); 'azar': el genoma NUEVO\n"
     "                            ES['banco'].append((_dg.copy(), _ds.copy(), _dgr, _dgs) if E_['donante'] == 'padre' else (_gh.copy(), _sh.copy(), _grh, _gsh))\n"),
    ("                    ch = mods[i][1].crea(ctx_de(i, SS(i, 'cuerpo', k), hid, _gh))\n",
     "                    ch = mods[i][1].crea(ctx_de(i, SS(i, 'cuerpo', k), hid, _gh, gr=_grh))\n"),
    ("H.g = _gh; H.s = _sh\n", "H.g = _gh; H.s = _sh; H.gr = _grh; H.gs = _gsh\n"),
    ("        if muertos or nuevos:\n",
     "            if _GR and b.vivo and 'vida' in b.c.EV and t > b.tn and (t - b.tn) % GD.PER_VIDA == 0:   # ORGANELOS (G3): en vida\n"
     "                _entrega(b, b.c.emite('vida'), 'vida')\n"
     "        if muertos or nuevos:\n"),
    ("                                   banco=[[round(float(x), 9) for x in e[0]] for e in ES['banco']])\n",
     "                                   banco=[[round(float(x), 9) for x in e[0]] for e in ES['banco']])\n"
     "                if _GR: ES['gcorte'] = dict(t=t + 1, banco_gr=[e[2] for e in ES['banco']], banco_gs=[e[3] for e in ES['banco']],\n"
     "                                            vivos_gr=[[z.lin, z.k, z.gen, z.tn, z.gr] for z in _vv])   # ORGANELOS (G4)\n"),
    ("    return dict(linajes=out, pizarra_log=piz_log,\n",
     "    _gout = {} if not _GR else dict(gram=dict(   # ORGANELOS (G4)\n"
     "        corte=ES.get('gcorte'), banco_final_gr=[e[2] for e in ES['banco']], banco_final_gs=[e[3] for e in ES['banco']],\n"
     "        vivos_gr=[[b.lin, b.k, b.gen, b.tn, b.gr] for b in cuerpos if b.vivo], g_nmut=ES.get('g_nmut', 0), entregas=dict(ES.get('g_ent', {})),\n"
     "        cfg=dict(p_campo=float(E_['g_pcampo']), p_dup=float(E_['g_pdup']), p_del=float(E_['g_pdel']), tope=int(E_['g_tope']),\n"
     "                 alfabeto=[list(a) for a in E_['g_alf']], per_vida=GD.PER_VIDA),\n"
     "        max_nac_linaje=max(l.nac for l in lin)))\n"
     "    return dict(linajes=out, pizarra_log=piz_log, **_gout,\n"),
]

# ============================================================================================ CARRO
METODOS = '''
    # ------------------------------------------------------------ ORGANELOS: LA GRAMATICA (construye_gramatica.py)
    def _tabla(self, que):
        """La TABLA de FAMB_ORG_ECO (lo heredado y encima lo vivido, por (patron, necesidad); orden del ORACULO), filtrada por el QUE."""
        _tab = {}
        if que != 4:
            for _p7, _r7, _n7 in self._nodo: _tab[(tuple(float(_z) for _z in _p7), int(_n7))] = float(_r7)
            _src = self._mordh
        else: _src = self._mordh[-self.NODO_K:]   # 'reciente': las ultimas NODO_K mordidas VIVIDAS, nada heredado
        for _t9, _k9, _n9, _R9 in _src: _tab[(tuple(float(_z9) for _z9 in self.PAT[_k9]), int(_n9))] = float(_R9)
        _o7 = {tuple(float(_z) for _z in self.PAT[_q7]): _i7 for _i7, _q7 in enumerate('ABCD')}   # orden del ORACULO: necesidad, letra
        _msg = [[list(_c7[0]), _tab[_c7], _c7[1]] for _c7 in sorted(_tab, key=lambda _c7: (_c7[1], _o7.get(_c7[0], 99), _c7[0]))]
        if que == 1: _msg = [_e for _e in _msg if _e[1] < 0]
        elif que == 2: _msg = [_e for _e in _msg if _e[1] > 0]
        elif que == 3: _msg = [_e for _e in _msg if _e[1] != 0]
        return _msg

    def _parir_gram(self):
        """Paquetes (como, tabla) de los slots nacer/hijo: viajan al hijo por la memoria del parto (el camino de FAMB_ORG_ECO)."""
        _pq = [(_s[3], self._tabla(_s[1])) for _s in self.GRAM if _s[0] == 1 and _s[2] == 0]
        if not _pq: return None
        self._n10['partos'] += 1; self._n10['dado'].append(sum(len(_x[1]) for _x in _pq))
        return _pq

    def emite(self, evento):
        """Paquetes para el MOTOR (todos menos nacer/hijo): [(quien, (como, tabla)), ...] de los slots de ese evento, en orden del genoma."""
        _ev = _GD.CUANDO.index(evento); _out = []
        for _s in self.GRAM:
            if _s[0] != _ev or (_ev == 1 and _s[2] == 0): continue
            _m = self._tabla(_s[1])
            if _m: _out.append((_GD.QUIEN[_s[2]], (_s[3], _m)))
        self._nemi += len(_out)
        return _out

    def _funde(self, paqs):
        """El COMO de cada paquete, aplicado por el RECEPTOR con su estado actual; una sola tabla (clave unica, el ultimo gana)."""
        _d = {}; _viv = None
        for _como, _ents in paqs:
            for _p7, _r7, _n7 in _ents:
                _k = (tuple(float(_z) for _z in _p7), int(_n7)); _r = float(_r7)
                if _como == 1: _r = (_r + float((self.Wps[int(_n7)] - self.Wns[int(_n7)]) @ np.asarray(_p7, float))) / 2.0
                elif _como == 2: _r = -_r
                elif _como == 3:
                    if _viv is None: _viv = {(tuple(float(_z9) for _z9 in self.PAT[_k9]), int(_n9)): float(_R9) for _t9, _k9, _n9, _R9 in self._mordh}
                    if _k in _viv and _viv[_k] != _r: continue
                _d[_k] = [list(_p7), _r, int(_n7)]
        return list(_d.values())

    def recibe(self, paq):
        """Un paquete recibido EN VIDA: entra al nodo (para pasarlo despues) y se LEE por la via lenta como en nace()."""
        _ents = self._funde([paq]); self._nrec += 1
        if not _ents: return
        _d = {}
        for _p7, _r7, _n7 in self._nodo: _d[(tuple(float(_z) for _z in _p7), int(_n7))] = [list(_p7), float(_r7), int(_n7)]
        for _e in _ents: _d[(tuple(float(_z) for _z in _e[0]), int(_e[2]))] = [list(_e[0]), float(_e[1]), int(_e[2])]
        self._nodo = [[list(_e[0]), _e[1], _e[2]] for _e in _d.values()] * max(1, self.NODO_LEE)
        self._lee([[list(_e[0]), _e[1], _e[2]] for _e in _ents] * max(1, self.NODO_LEE))

    def _lee(self, _msg):
        """La lectura del NODO de nace() (via lenta, relevancia viva), sobre el mensaje recibido."""
        if not (self._con and _msg): return
        ETA_S = self.ETA_S; AVERSION = self.AVERSION; LAM = self.LAM; CLIP_S = self.CLIP_S
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
        self._ldiv += int(len(_msg) > self.NODO_LEE or (_sel9 != sorted(_sel9)))

    def salida(self):
'''

ANCLAS_CARRO = [
    ('"""carros/FAMB_ORG_ECO.py (CONSTRUIDO',
     '"""carros/FAMB_GRAM_ECO.py (CONSTRUIDO por experimentos/organelos/gramatica/construye_gramatica.py desde '
     f'experimentos/juaco_eco/carros/FAMB_ORG_ECO.py, sha {SHA_CARRO}; NO editar a mano).\nORGANELOS: el organo de transmision lo describe '
     "la GRAMATICA del cuerpo (ctx['gramatica'], gramatica_def.py); sin ella es FAMB_ORG_ECO. Lo que sigue es el docstring del origen.\n\n"
     'carros/FAMB_ORG_ECO.py (CONSTRUIDO'),
    ("import numpy as np\n",
     "import numpy as np\n"
     "import os as _os, sys as _sys   # ORGANELOS: la gramatica vive en la carpeta de arriba\n"
     "_AQG = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))\n"
     "if _AQG not in _sys.path: _sys.path.insert(0, _AQG)\n"
     "import gramatica_def as _GD\n"),
    ("        self.ENSENA = float(kw.get('ensena', 0.9)) >= 1.0; self.FILTRA0 = float(kw.get('filtra0', 0.9)) >= 1.0   # ECO v2: ORGANOS\n",
     "        self.ENSENA = float(kw.get('ensena', 0.9)) >= 1.0; self.FILTRA0 = float(kw.get('filtra0', 0.9)) >= 1.0   # ECO v2: ORGANOS\n"
     "        self.GRAM = ctx.get('gramatica'); self._nemi = 0; self._nrec = 0   # ORGANELOS: None -> los organos numericos de FAMB_ORG_ECO\n"
     "        if self.GRAM is not None:\n"
     "            self.GRAM = _GD.activos(self.GRAM); self.ENSENA = False; self.FILTRA0 = False\n"
     "            self.EV = frozenset(_GD.CUANDO[_s[0]] for _s in self.GRAM if not (_s[0] == 1 and _s[2] == 0))\n"
     "        else: self.EV = frozenset()\n"),
    ("        if MODO == 'nada' or not self.ENSENA: return None   # ECO v2: sin el organo 'ensena', el hijo no se lleva nada (FABRICA)\n",
     "        if self.GRAM is not None: return self._parir_gram()   # ORGANELOS\n"
     "        if MODO == 'nada' or not self.ENSENA: return None   # ECO v2: sin el organo 'ensena', el hijo no se lleva nada (FABRICA)\n"),
    ("        _mem = info.get('memoria')\n",
     "        _mem = info.get('memoria')\n"
     "        if self.GRAM is not None and _mem is not None: _mem = self._funde(_mem)   # ORGANELOS: paquetes -> una tabla (el COMO del emisor)\n"),
    ("\n    def salida(self):\n", METODOS),
]


def textos():
    if h16(ORIG_MOTOR) != SHA_MOTOR: raise SystemExit(f"CONSTRUYE: motor_eco2.py cambio ({h16(ORIG_MOTOR)})")
    if h16(ORIG_CARRO) != SHA_CARRO: raise SystemExit(f"CONSTRUYE: FAMB_ORG_ECO.py cambio ({h16(ORIG_CARRO)})")
    m = aplica(open(ORIG_MOTOR, encoding='utf-8').read(), ANCLAS_MOTOR, 'motor_gramatica')
    c = aplica(open(ORIG_CARRO, encoding='utf-8').read(), ANCLAS_CARRO, 'FAMB_GRAM_ECO')
    return {DEST_MOTOR: m, DEST_CARRO: c}


if __name__ == '__main__':
    arts = textos()
    if '--verifica' in sys.argv[1:]:
        ok = all(os.path.exists(p) and open(p, encoding='utf-8').read() == s for p, s in arts.items())
        print('VERIFICA', 'OK' if ok else 'FALLA'); sys.exit(0 if ok else 1)
    if set(sys.argv[1:]) - {'--verifica'}: raise SystemExit(f"CONSTRUYE: banderas desconocidas {sys.argv[1:]}")
    os.makedirs(os.path.dirname(DEST_CARRO), exist_ok=True)
    for p, s in arts.items():
        with open(p, 'w', encoding='utf-8', newline='\n') as f: f.write(s)
        print(os.path.relpath(p, RAIZ), h16s(s))
