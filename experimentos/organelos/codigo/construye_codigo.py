"""construye_codigo.py — CONSTRUYE motor_codigo.py por ANCLAS desde experimentos/organelos/gramatica/motor_gramatica.py (no se toca el origen).

MISION: llegar a la AGI por este camino.

Cambios (C1-C6), cada uno con su ancla unica (si un ancla no aparece exactamente una vez, aborta):
 C1 eco['codigo'] = lista de CINTAS (una por fundador): la gramatica y las 18 perillas las DESARROLLA la cinta (codigo_def.desarrolla);
    exige gramatica=None, p_mut=0, n_sombra=0. eco['c_on'] (errores de copia de la cinta), eco['c_sos'] (la regla SOS se lee o no).
 C2 el cuerpo lleva su cinta (cin) y el registro fisico de sus ultimas 20 mordidas (mb: 1 si el dS nominal tuvo algun componente < 0).
 C3 PARTO (y fundador del vivero desde el banco): la cinta del donante se COPIA con errores (codigo_def.copia, rng [seed, lin, 23, k])
    leyendo TASA/SOS de la misma cinta y la fraccion de mordidas malas del PADRE; luego se DESARROLLA -> genoma numerico + gramatica.
    El banco guarda tambien la cinta.
 C4 eco['cambio'] = (t, X, Y): en el paso t el mundo INTERCAMBIA el valor de las letras X e Y (VAL_VIVO); el resto del mundo igual.
 C5 telemetria: por parto [t, lin, k, k_padre, errores, sos, fenotipo_cambio, largo, cambios, borrados, inserciones, duplicaciones, frac_mal del padre];
    mordidas por letra y signo antes/despues del cambio; cintas de los vivos en T.
 C6 salida: d['codigo'] (solo si hay codigo o cambio). Con codigo=None y cambio=None: motor_gramatica BIT A BIT (arnes I1).
"""
import hashlib, os

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(os.path.dirname(AQUI), 'gramatica', 'motor_gramatica.py')
DESTINO = os.path.join(AQUI, 'motor_codigo.py')
SHA_ORIGEN = '6b65dc5e32093424'

R = [
 ('"""motor_gramatica.py (CONSTRUIDO',
  '"""motor_codigo.py (CONSTRUIDO por experimentos/organelos/codigo/construye_codigo.py desde experimentos/organelos/gramatica/motor_gramatica.py, '
  'sha 6b65dc5e32093424; NO editar a mano).\nCODIGO v0: + LA CINTA (codigo_def.py): el cuerpo DESARROLLA su cinta al nacer y el parto la COPIA con errores que la '
  'propia cinta regula (TASA, SOS); + el mundo que CAMBIA (eco[\'cambio\']). Con codigo=None y cambio=None es motor_gramatica BIT A BIT.\n\n'
  'motor_gramatica.py (CONSTRUIDO'),
 ("import gramatica_def as GD\n",
  "import gramatica_def as GD\nimport codigo_def as CD   # CODIGO v0\nETQ_CMUT = 23   # CODIGO: rng de los errores de copia de la cinta\n"
  "ENTEROS = tuple(g[2] for g in GENES)\n"),
 ("gramatica=None, g_pcampo=0.0, g_pdup=0.0, g_pdel=0.0, g_tope=4, g_alfabeto=None)",
  "gramatica=None, g_pcampo=0.0, g_pdup=0.0, g_pdel=0.0, g_tope=4, g_alfabeto=None,\n"
  "               codigo=None, c_on=True, c_sos=True, cambio=None)   # CODIGO v0 (C1, C4)"),
 ("        E_['g_on'] = float(E_['g_pcampo']) > 0 or float(E_['g_pdup']) > 0 or float(E_['g_pdel']) > 0\n    return E_\n",
  "        E_['g_on'] = float(E_['g_pcampo']) > 0 or float(E_['g_pdup']) > 0 or float(E_['g_pdel']) > 0\n"
  "    E_['cod0'] = None   # CODIGO v0 (C1)\n"
  "    if E_['codigo'] is not None:\n"
  "        if E_['gramatica'] is not None: raise SystemExit('CODIGO: con codigo la gramatica la DESARROLLA la cinta (gramatica=None)')\n"
  "        if float(E_['p_mut']) != 0.0 or int(E_['n_sombra']) != 0: raise SystemExit('CODIGO: con codigo, p_mut = 0 y n_sombra = 0')\n"
  "        _cs = list(E_['codigo'])\n"
  "        if len(_cs) != n: raise SystemExit(f'CODIGO: {len(_cs)} cintas para {n} fundadores')\n"
  "        E_['cod0'] = [CD.valida(c) for c in _cs]; _tp = int(E_['g_tope'])\n"
  "        E_['g_alf'] = GD.ALFABETO_TODO if E_['g_alfabeto'] is None else tuple(tuple(int(v) for v in a) for a in E_['g_alfabeto']); E_['g_on'] = False\n"
  "        _dv = [CD.desarrolla(c, G0, E_['lo'], E_['hi'], ENTEROS) for c in E_['cod0']]\n"
  "        E_['gs0'] = [d[0] for d in _dv]; E_['gr0'] = [GD.valida(d[1], _tp) for d in _dv]\n"
  "    if E_['cambio'] is not None:   # CODIGO v0 (C4)\n"
  "        _c = tuple(E_['cambio'])\n"
  "        if len(_c) != 3 or _c[1] == _c[2] or _c[1] not in 'ABCD' or _c[2] not in 'ABCD' or int(_c[0]) < 0: raise SystemExit('CODIGO: cambio = (t, X, Y)')\n"
  "    return E_\n"),
 ("'pc', 'g', 's', 'gr', 'gs')   # ORGANELOS: gr, gs", "'pc', 'g', 's', 'gr', 'gs', 'cin', 'mb')   # ORGANELOS: gr, gs; CODIGO: cin, mb"),
 ("        self.gr = None; self.gs = None   # ORGANELOS: gramatica real y sombras",
  "        self.gr = None; self.gs = None   # ORGANELOS: gramatica real y sombras\n        self.cin = None; self.mb = None   # CODIGO v0 (C2): la cinta y las ultimas 20 mordidas (1 = mala)"),
 ("    _GR = E_ is not None and E_['gr0'] is not None   # ORGANELOS\n",
  "    _GR = E_ is not None and E_['gr0'] is not None   # ORGANELOS\n"
  "    _CO = E_ is not None and E_['cod0'] is not None   # CODIGO v0\n"
  "    _CB = None if E_ is None or E_['cambio'] is None else (int(E_['cambio'][0]), str(E_['cambio'][1]), str(E_['cambio'][2]))\n"),
 ("            if _GR: cuerpos[-1].gr = E_['gr0'][i]; cuerpos[-1].gs = (E_['gr0'][i],) * int(E_['n_sombra'])\n",
  "            if _GR: cuerpos[-1].gr = E_['gr0'][i]; cuerpos[-1].gs = (E_['gr0'][i],) * int(E_['n_sombra'])\n"
  "            if _CO: cuerpos[-1].cin = E_['cod0'][i]; cuerpos[-1].mb = []   # CODIGO v0\n"),
 ("ES['banco'] = [(b.g.copy(), b.s.copy(), b.gr, b.gs) for b in cuerpos]", "ES['banco'] = [(b.g.copy(), b.s.copy(), b.gr, b.gs, b.cin) for b in cuerpos]"),
 ("    def registra(b, tm, causa, vd):\n",
  "    def _cod(cin, r, fm, prev_g, prev_gr, i, k, t, pk):   # CODIGO v0 (C3): COPIA (con la regla de la cinta) y DESARROLLO\n"
  "        c2, st = CD.copia(cin, r, fm, bool(E_['c_sos']), bool(E_['c_on']))\n"
  "        g2, gr2, _dd = CD.desarrolla(c2, E_['G0'], E_['lo'], E_['hi'], ENTEROS); gr2 = GD.valida(gr2, int(E_['g_tope']))\n"
  "        ch = int(not (np.array_equal(g2, prev_g) and tuple(gr2) == tuple(prev_gr)))\n"
  "        ES.setdefault('cod_nac', []).append([t, i, k, pk, st['n'], st['sos'], ch, len(c2)] + list(st['tipos']) + [(-1.0 if fm is None else round(float(fm), 3))])\n"
  "        return c2, g2, gr2\n\n"
  "    def _fmal(b): return (sum(b.mb) / len(b.mb)) if b.mb else 0.0   # CODIGO v0: lo VIVIDO por el padre (fisica)\n\n"
  "    def registra(b, tm, causa, vd):\n"),
 ("                _gf = _sf = _grf = _gsf = None\n", "                _gf = _sf = _grf = _gsf = _cif = None\n"),
 ("                        _gb, _sb, _grb, _gsb = ES['banco'][int(SE(i, ETQ_BANCO, l.nac).integers(len(ES['banco'])))]\n",
  "                        _gb, _sb, _grb, _gsb, _cib = ES['banco'][int(SE(i, ETQ_BANCO, l.nac).integers(len(ES['banco'])))]\n"),
 ("                        ES['n_banco'] += 1; _grf, _gsf = _muta_gr(_grb, _gsb, i, l.nac)\n",
  "                        ES['n_banco'] += 1; _grf, _gsf = _muta_gr(_grb, _gsb, i, l.nac)\n"
  "                        if _CO: _cif, _gf, _grf = _cod(_cib, SE(i, ETQ_CMUT, l.nac), None, _gb, _grb, i, l.nac, t, -1)   # CODIGO v0\n"),
 ("                        if _GR: _grf = E_['gr0'][i]; _gsf = (_grf,) * int(E_['n_sombra'])\n",
  "                        if _GR: _grf = E_['gr0'][i]; _gsf = (_grf,) * int(E_['n_sombra'])\n"
  "                        if _CO: _cif = E_['cod0'][i]\n"),
 ("                        ES['banco'].append((_gf.copy(), _sf.copy(), _grf, _gsf))\n",
  "                        ES['banco'].append((_gf.copy(), _sf.copy(), _grf, _gsf, _cif))\n"),
 ("                if E_ is not None: F.g = _gf; F.s = _sf; F.gr = _grf; F.gs = _gsf\n",
  "                if E_ is not None: F.g = _gf; F.s = _sf; F.gr = _grf; F.gs = _gsf; F.cin = _cif; F.mb = ([] if _CO else None)\n"),
 ("                    _gh = _sh = _grh = _gsh = None\n", "                    _gh = _sh = _grh = _gsh = _cih = None\n"),
 ("                        _dg, _ds, _dgr, _dgs = b.g, b.s, b.gr, b.gs\n", "                        _dg, _ds, _dgr, _dgs, _dci = b.g, b.s, b.gr, b.gs, b.cin\n"),
 ("                            _dg, _ds, _dgr, _dgs = ES['banco'][int(SE(i, ETQ_DONANTE, k).integers(len(ES['banco'])))]\n",
  "                            _dg, _ds, _dgr, _dgs, _dci = ES['banco'][int(SE(i, ETQ_DONANTE, k).integers(len(ES['banco'])))]\n"),
 ("                        _grh, _gsh = _muta_gr(_dgr, _dgs, i, k)   # ORGANELOS (G1)\n",
  "                        _grh, _gsh = _muta_gr(_dgr, _dgs, i, k)   # ORGANELOS (G1)\n"
  "                        if _CO: _cih, _gh, _grh = _cod(_dci, SE(i, ETQ_CMUT, k), _fmal(b), _dg, _dgr, i, k, t, b.k)   # CODIGO v0 (C3)\n"),
 ("ES['banco'].append((_dg.copy(), _ds.copy(), _dgr, _dgs) if E_['donante'] == 'padre' else (_gh.copy(), _sh.copy(), _grh, _gsh))",
  "ES['banco'].append((_dg.copy(), _ds.copy(), _dgr, _dgs, _dci) if E_['donante'] == 'padre' else (_gh.copy(), _sh.copy(), _grh, _gsh, _cih))"),
 ("H.g = _gh; H.s = _sh; H.gr = _grh; H.gs = _gsh\n", "H.g = _gh; H.s = _sh; H.gr = _grh; H.gs = _gsh; H.cin = _cih; H.mb = ([] if _CO else None)\n"),
 ("                    _dS = EFECTO[VAL_VIVO[kk]]\n",
  "                    _dS = EFECTO[VAL_VIVO[kk]]\n"
  "                    if _CO:   # CODIGO v0 (C2): registro fisico de lo vivido\n"
  "                        b.mb.append(1 if min(_dS) < 0 else 0)\n"
  "                        if len(b.mb) > 20: del b.mb[0]\n"
  "                    if _CB is not None:   # CODIGO v0 (C5)\n"
  "                        _ms = ES.setdefault('mord_signo', {}); _kq = f\"{kk}/{'post' if t >= _CB[0] else 'pre'}\"\n"
  "                        _ms.setdefault(_kq, [0, 0]); _ms[_kq][1 if min(_dS) < 0 else 0] += 1\n"),
 ("    for t in range(_t0, T):\n",
  "    if _CB is not None and _t0 > _CB[0]: VAL_VIVO = dict(VAL_VIVO); VAL_VIVO[_CB[1]], VAL_VIVO[_CB[2]] = VAL_VIVO[_CB[2]], VAL_VIVO[_CB[1]]   # reanudar\n"
  "    for t in range(_t0, T):\n"
  "        if _CB is not None and t == _CB[0]:   # CODIGO v0 (C4): EL MUNDO CAMBIA (se intercambia el valor de dos letras)\n"
  "            VAL_VIVO = dict(VAL_VIVO); VAL_VIVO[_CB[1]], VAL_VIVO[_CB[2]] = VAL_VIVO[_CB[2]], VAL_VIVO[_CB[1]]\n"),
 ("    return dict(linajes=out, pizarra_log=piz_log, **_gout,\n",
  "    _cout = {} if not (_CO or _CB is not None) else dict(codigo=dict(   # CODIGO v0 (C6)\n"
  "        cod_nac=ES.get('cod_nac', []), mord_signo=ES.get('mord_signo', {}), cambio=(None if _CB is None else list(_CB)),\n"
  "        c_on=(None if E_['cod0'] is None else bool(E_['c_on'])), c_sos=(None if E_['cod0'] is None else bool(E_['c_sos'])),\n"
  "        cintas_vivos=[[b.lin, b.k, b.gen, [list(x) for x in b.cin]] for b in cuerpos if b.vivo and b.cin is not None][:80]))\n"
  "    return dict(linajes=out, pizarra_log=piz_log, **_gout, **_cout,\n"),
]


def main():
    src = open(ORIGEN, encoding='utf-8').read()
    sha = hashlib.sha256(src.encode('utf-8')).hexdigest()[:16]
    b = open(ORIGEN, 'rb').read(); sha = hashlib.sha256(b).hexdigest()[:16]
    if sha != SHA_ORIGEN: raise SystemExit(f"CONSTRUYE: el origen cambio ({sha} != {SHA_ORIGEN})")
    for a, n_ in R:
        k = src.count(a)
        if k != 1: raise SystemExit(f"CONSTRUYE: ancla aparece {k} veces: {a[:80]!r}")
        src = src.replace(a, n_)
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f: f.write(src)
    print(f"motor_codigo.py construido ({len(R)} anclas) sha {hashlib.sha256(open(DESTINO, 'rb').read()).hexdigest()[:16]}")


if __name__ == '__main__':
    main()
