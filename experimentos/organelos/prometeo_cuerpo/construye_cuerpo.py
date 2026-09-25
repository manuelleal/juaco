# EXPLORATORIO, no es dato
"""construye_cuerpo.py — PROMETEO-CUERPO (Opus, equipo JUACO, 25-sep-2026). MISION: llegar a la AGI por este camino.

Pedido del director: "que en el codigo puedan crear lo que quieran al azar: un pie, un escudo... a ver si asi sobreviven" (Karl Sims 1994).

Construye por ANCLAS de texto (los originales solo se LEEN; nada fuera de prometeo_cuerpo/ se escribe):
  codigo_cuerpo.py          <- ../prometeo/codigo_prometeo.py        (+ la instruccion PARTE p en el alfabeto)
  motor_cuerpo.py           <- ../prometeo/motor_prometeo.py         (el cuerpo LEE sus partes; efecto fisico + costo por paso)
  carros/FAMB_GRAM_ECO.py   <- ../codigo/carros/FAMB_GRAM_ECO.py     (solo: si NO ve ningun objeto (niebla) no revienta; con vista
                                                                       completa es el mismo carro bit a bit)

LAS PARTES (nacen AUSENTES; entran por insercion/cambio entero de la copia o por HGT; REP/DEF/LLAMA las multiplican como a un gen).
k = copias leidas (tope 8). Rendimiento decreciente R(k) = 1 - 0.5^k (1 copia 0.5, 2: 0.75, 3: 0.875). Costo LINEAL: k * costo[p] de E por paso.
  0 PATA       si el cuerpo se mueve, no muerde y cae en celda vacia, da OTRO paso en la misma direccion con prob MAG.pata * R(k).
  1 ESCUDO     cada componente NEGATIVA del efecto de una mordida (veneno B en E, sal D en Ag) se multiplica por 1 - MAG.escudo * R(k).
  2 ESTOMAGO   la reserva maxima de E y de Ag pasa de 1.5 a 1.5 + MAG.estomago * R(k).
  3 OJO        radio de vista = niebla + MAG.ojo * R(k). SIN niebla (quieto, onda8k, veneno) el carro ya ve el anillo entero
               (ENMIENDA 1, opcion A): el OJO es INERTE por construccion (cuesta y no hace nada) -> control neutro interno.
  4 MANDIBULA  cada componente POSITIVA del efecto de una mordida se multiplica por 1 + MAG.mandibula * R(k) (digiere mejor).
  5 LENGUA     antes de tragar, si el bocado dana (alguna componente < 0), lo ESCUPE con prob MAG.lengua * R(k): no hay efecto ni
               aprendizaje y el objeto queda en el mundo.
El carro (cerebro) NO sabe que partes tiene: el efecto lo aplica el mundo (fisica). Las senales de la mordida al carro son las NOMINALES.
partes_on=False (CUERPO_MUDO): las partes se leen y COBRAN, pero no hacen nada. partes_costo=False: no cobran (solo para el arnes).
Rng propio de las partes (random.Random(seed*7919+31)): solo se consume si un cuerpo tiene PATA o LENGUA con efecto.
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
SRC_CD = os.path.join(ORG, 'prometeo', 'codigo_prometeo.py')
SRC_MP = os.path.join(ORG, 'prometeo', 'motor_prometeo.py')
SRC_CA = os.path.join(ORG, 'codigo', 'carros', 'FAMB_GRAM_ECO.py')

A_CD = [
    ("KIT = ('CABLE', 'HGT')   # PROMETEO (K0): el material para sus organos\n",
     "KIT = ('CABLE', 'HGT')   # PROMETEO (K0): el material para sus organos\n"
     "CUERPO = ('PARTE',)      # CUERPO (B0): el material para su cuerpo\n"
     "PARTES = ('PATA', 'ESCUDO', 'ESTOMAGO', 'OJO', 'MANDIBULA', 'LENGUA')\n"
     "TOPE_PARTE = 8           # copias leidas por parte (efecto y costo se calculan con min(k, 8))\n"),
    ("        if o not in OPS + KIT: raise SystemExit(f'PROMETEO: op {o}')",
     "        if o not in OPS + KIT + CUERPO: raise SystemExit(f'PROMETEO: op {o}')"),
    ("'HGT': ((0, len(P_HGT) - 1), (0, len(L_HGT) - 1))}[op]   # PROMETEO",
     "'HGT': ((0, len(P_HGT) - 1), (0, len(L_HGT) - 1)),\n            'PARTE': ((0, len(PARTES) - 1),)}[op]   # PROMETEO + CUERPO"),
    ("        if not ins or ins[0] not in OPS + KIT: raise", "        if not ins or ins[0] not in OPS + KIT + CUERPO: raise"),
    ("st = dict(pasos=0, llamadas=0, corte=0, cable=None)   # PROMETEO: cable = W[d][s]",
     "st = dict(pasos=0, llamadas=0, corte=0, cable=None, parte=None)   # PROMETEO: cable = W[d][s]; CUERPO: parte = copias por parte"),
    ("            elif op == 'CABLE':   # PROMETEO (K1)\n",
     "            elif op == 'PARTE':   # CUERPO (B1): cada lectura suma una copia de la parte\n"
     "                if st['parte'] is None: st['parte'] = [0] * len(PARTES)\n"
     "                st['parte'][ins[1]] += 1\n"
     "            elif op == 'CABLE':   # PROMETEO (K1)\n"),
]
CD_FIN = '''

# ================================================================= CUERPO: lo que el cuerpo lee de sus partes
def partes(cinta, G0, lo, hi, enteros):
    """Copias LEIDAS de cada parte (tope TOPE_PARTE), o None si la cinta no expresa ninguna."""
    if not any(ins[0] == 'PARTE' for ins in cinta): return None
    p = desarrolla(cinta, G0, lo, hi, enteros)[2]['parte']
    if p is None or not any(p): return None
    return tuple(min(int(v), TOPE_PARTE) for v in p)
'''

A_MP = [
    ("CARROS_ECO = os.path.join(AQUI, 'carros')",
     "CARROS_ECO = os.path.join(_PROM, 'carros')   # CUERPO: la copia del carro (niebla); con vista completa es el mismo carro bit a bit"),
    ("    nom = f\"carro_eco_{ident}\"", "    nom = f\"carro_cuerpo_{ident}\"   # CUERPO: nombre propio (no choca con el carro original en el mismo proceso)"),
    ("import codigo_prometeo as CD   # PROMETEO (antes codigo_def)", "import codigo_cuerpo as CD   # CUERPO (antes codigo_prometeo)"),
    ("codigo=None, c_on=True, c_sos=True, cambio=None)   # CODIGO v0 (C1, C4)",
     "codigo=None, c_on=True, c_sos=True, cambio=None,\n"
     "               partes_on=True, partes_costo=True, niebla=None, partes_mag=None)   # CODIGO v0 (C1, C4) + CUERPO"),
    ("ETQ_CMUT = 23   # CODIGO: rng de los errores de copia de la cinta\n",
     "ETQ_CMUT = 23   # CODIGO: rng de los errores de copia de la cinta\n"
     "# CUERPO (B0): efecto MAXIMO de cada parte (k copias dan max * (1 - 0.5^k)) y costo en E por paso y por copia (en el orden de CD.PARTES)\n"
     "MAG = dict(pata=0.6, escudo=0.6, estomago=1.0, ojo=40.0, mandibula=0.5, lengua=0.8, costo=(0.0002,) * 6)\n"),
    ("    if isinstance(E_['cambio'], dict): FB.valida(E_['cambio'])   # FABLE (F1)\n",
     "    if E_['niebla'] is not None and not (isinstance(E_['niebla'], int) and E_['niebla'] >= 1): raise SystemExit('CUERPO: niebla None o entero >= 1')\n"
     "    if E_['partes_mag'] is not None and set(E_['partes_mag']) - set(MAG): raise SystemExit(f\"CUERPO: partes_mag con claves {sorted(set(E_['partes_mag']) - set(MAG))}\")\n"
     "    if isinstance(E_['cambio'], dict) and E_['cambio'].get('tipo') == 'reina' and 'PARTE' in CD.ALF[0]: raise SystemExit('CUERPO: la LENGUA mira el efecto sin morder; no va con reina')\n"
     "    if isinstance(E_['cambio'], dict): FB.valida(E_['cambio'])   # FABLE (F1)\n"),
    ("'cin', 'mb', 'kc')", "'cin', 'mb', 'kc', 'pt')"),
    ("        self.cin = None; self.mb = None; self.kc = None", "        self.cin = None; self.mb = None; self.kc = None; self.pt = None"),
    ("    def _sen(b, t):\n",
     "    _PCC = {}; _RP = _random.Random(seed * 7919 + 31)   # CUERPO (B2): cache cinta -> partes; rng propio de las partes\n"
     "    _MG = dict(MAG)\n"
     "    if E_ is not None and E_['partes_mag']: _MG.update(E_['partes_mag'])\n"
     "    _PON = E_ is not None and bool(E_['partes_on']); _PCO = E_ is not None and bool(E_['partes_costo']); _NB = None if E_ is None else E_['niebla']\n"
     "    def _CSD():\n"
     "        cs = ES.get('cuerpo')\n"
     "        if cs is None: cs = ES['cuerpo'] = dict(pata=0, escudo=0.0, estomago=0.0, mandibula=0.0, lengua=0, costo=0.0, ciego=0, ve=0, ciego_ojo=0, ve_ojo=0)\n"
     "        return cs\n"
     "    def _pc(cin):   # fenotipo corporal: (p_pata, f_escudo, tope_reserva, radio_ojo_extra, f_mandibula, p_lengua, costo_por_paso, copias)\n"
     "        if cin is None: return None\n"
     "        w = _PCC.get(cin)\n"
     "        if w is None:\n"
     "            n = CD.partes(cin, E_['G0'], E_['lo'], E_['hi'], ENTEROS)\n"
     "            if n is None: w = 0\n"
     "            else:\n"
     "                R = [1.0 - 0.5 ** v for v in n]\n"
     "                w = (_MG['pata'] * R[0], _MG['escudo'] * R[1], 1.5 + _MG['estomago'] * R[2], _MG['ojo'] * R[3], _MG['mandibula'] * R[4],\n"
     "                     _MG['lengua'] * R[5], float(sum(float(_MG['costo'][j]) * n[j] for j in range(len(n)))), tuple(n))\n"
     "            if len(_PCC) < 200000: _PCC[cin] = w\n"
     "        return w or None\n"
     "    def _vista_niebla(b):   # CUERPO (B4): el cuerpo solo ve los objetos a distancia <= niebla (+ lo que agrega su OJO)\n"
     "        pt = b.pt; ojo = pt is not None and pt[7][3] > 0; r = _NB + (pt[3] if (pt is not None and _PON) else 0.0)\n"
     "        p = b.pos; out = {}\n"
     "        for x, v in objs.items():\n"
     "            dd = abs(x - p); dd = min(dd, L - dd)\n"
     "            if dd <= r: out[x] = v\n"
     "        cs = _CSD()\n"
     "        if out: cs['ve'] += 1; cs['ve_ojo'] += int(ojo)\n"
     "        else: cs['ciego'] += 1; cs['ciego_ojo'] += int(ojo)\n"
     "        return out\n"
     "    def _aplica(b, dS):   # CUERPO (B7): ESCUDO (negativo), MANDIBULA (positivo), ESTOMAGO (tope de la reserva)\n"
     "        pt = b.pt; cs = _CSD(); v2 = []\n"
     "        for v in (dS[0], dS[1]):\n"
     "            if v < 0 and pt[1] > 0.0: cs['escudo'] += -v * pt[1]; v = v * (1.0 - pt[1])\n"
     "            elif v > 0 and pt[4] > 0.0: cs['mandibula'] += v * pt[4]; v = v * (1.0 + pt[4])\n"
     "            v2.append(v)\n"
     "        tp = pt[2]; e2 = b.E + v2[0]; a2 = b.Ag + v2[1]\n"
     "        if tp > 1.5: cs['estomago'] += max(0.0, min(e2, tp) - max(b.E, 1.5)) + max(0.0, min(a2, tp) - max(b.Ag, 1.5))\n"
     "        b.E = min(e2, tp); b.Ag = min(a2, tp)\n"
     "    def _sen(b, t):\n"),
    ("            if _CO: cuerpos[-1].cin = E_['cod0'][i]; cuerpos[-1].mb = []; cuerpos[-1].kc = _kc(E_['cod0'][i])   # CODIGO v0 + PROMETEO",
     "            if _CO: cuerpos[-1].cin = E_['cod0'][i]; cuerpos[-1].mb = []; cuerpos[-1].kc = _kc(E_['cod0'][i]); cuerpos[-1].pt = _pc(E_['cod0'][i])   # CODIGO v0 + PROMETEO + CUERPO"),
    ("F.kc = (_kc(_cif) if _CO else None)", "F.kc = (_kc(_cif) if _CO else None); F.pt = (_pc(_cif) if _CO else None)"),
    ("H.kc = (_kc(_cih) if _CO else None)", "H.kc = (_kc(_cih) if _CO else None); H.pt = (_pc(_cih) if _CO else None)"),
    ("            o['t'] = t; o['pos'] = b.pos; o['E'] = b.E; o['Ag'] = b.Ag; o['cuerpos'] = foto; o['pizarra'] = piz_t\n",
     "            o['t'] = t; o['pos'] = b.pos; o['E'] = b.E; o['Ag'] = b.Ag; o['cuerpos'] = foto; o['pizarra'] = piz_t\n"
     "            if _NB is not None: o['objs'] = _vista_niebla(b)   # CUERPO (B4): niebla\n"),
    ("            b.pos = (b.pos + mov) % L; pos = b.pos\n",
     "            b.pos = (b.pos + mov) % L; pos = b.pos\n"
     "            if mov != 0 and b.pt is not None and _PON and b.pt[0] > 0.0 and pos not in objs and not a.get('muerde', False) and _RP.random() < b.pt[0]:   # CUERPO (B5): PATA\n"
     "                b.pos = (b.pos + mov) % L; pos = b.pos; _CSD()['pata'] += 1\n"),
    ("                kk = objs[pos]; mordio = bool(a.get('muerde', False)); q = l.q(t)\n",
     "                kk = objs[pos]; mordio = bool(a.get('muerde', False)); q = l.q(t)\n"
     "                if mordio and b.pt is not None and _PON and b.pt[5] > 0.0:   # CUERPO (B6): LENGUA: prueba y escupe lo que dana (el objeto queda)\n"
     "                    _d0 = EFECTO[VAL_VIVO[kk]] if _EFT is None else _EFT(kk, pos)\n"
     "                    if min(_d0) < 0 and _RP.random() < b.pt[5]: mordio = False; _CSD()['lengua'] += 1\n"),
    ("                    b.E = min(b.E + _dS[0], 1.5); b.Ag = min(b.Ag + _dS[1], 1.5)\n",
     "                    if b.pt is None or not _PON: b.E = min(b.E + _dS[0], 1.5); b.Ag = min(b.Ag + _dS[1], 1.5)\n"
     "                    else: _aplica(b, _dS)   # CUERPO (B7)\n"),
    ("            b.E -= M['costo']; b.Ag -= M['costo_a']\n",
     "            b.E -= M['costo']; b.Ag -= M['costo_a']\n"
     "            if b.pt is not None and _PCO: b.E -= b.pt[6]; _CSD()['costo'] += b.pt[6]   # CUERPO (B3): mantenimiento de las partes\n"),
    ("                        if E_['banco']:   # 'padre': el genoma del PADRE (fertilidad); 'azar': el genoma NUEVO\n",
     "                        if _CO and len(ES.setdefault('cuerpo_nac', [])) < 80000:   # CUERPO: copias de cada parte por nacimiento\n"
     "                            _pp = _pc(_cih); ES['cuerpo_nac'].append([t] + ([0] * len(CD.PARTES) if _pp is None else list(_pp[7])))\n"
     "                        if E_['banco']:   # 'padre': el genoma del PADRE (fertilidad); 'azar': el genoma NUEVO\n"),
    ("alfabeto=list(CD.ALF[0]))))   # PROMETEO",
     "alfabeto=list(CD.ALF[0])),\n"
     "        cuerpo=dict(cont=ES.get('cuerpo'), nac=ES.get('cuerpo_nac', []), mag={k: (list(v) if isinstance(v, tuple) else v) for k, v in _MG.items()},\n"
     "                    partes_on=_PON, partes_costo=_PCO, niebla=_NB, partes=list(CD.PARTES))))   # PROMETEO + CUERPO"),
]

A_CA = [
    ("        d, k, left = self._see(pos, objs, t, contar=True); pat = PAT[k]\n"
     "        x = np.concatenate([pat * 1.2, [1.5 if left else 0, 0 if left else 1.5, 1.0 if d == 0 else 0.]]); noise = .15 + .5 * hambre\n",
     "        _sv = self._see(pos, objs, t, contar=True)   # CUERPO (niebla): None = no ve ningun objeto\n"
     "        if _sv is None: d = None; x = np.zeros(9)\n"
     "        else:\n"
     "            d, k, left = _sv; pat = PAT[k]\n"
     "            x = np.concatenate([pat * 1.2, [1.5 if left else 0, 0 if left else 1.5, 1.0 if d == 0 else 0.]])\n"
     "        noise = .15 + .5 * hambre\n"),
    ("d2, _, _ = self._see(pos, objs, t); Rp = .2 if d2 < d else 0.",
     "_sv2 = self._see(pos, objs, t); Rp = .2 if (_sv2 is not None and d is not None and _sv2[0] < d) else 0.   # CUERPO (niebla)"),
    ("        L = self.L; rech = self._rech if self.MEMORIA_RECHAZO else None; fb = None\n",
     "        if not objs:   # CUERPO (niebla): nada a la vista (con vista completa nunca pasa: el mundo tiene piso de 1 objeto)\n"
     "            if contar: self.sin_objetivo[self._q(t)] += 1\n"
     "            return None\n"
     "        L = self.L; rech = self._rech if self.MEMORIA_RECHAZO else None; fb = None\n"),
]


def aplica(src, anclas, nombre):
    for viejo, nuevo in anclas:
        if src.count(viejo) != 1: raise SystemExit(f"CUERPO: ancla no unica en {nombre} ({src.count(viejo)}): {viejo[:90]!r}")
        src = src.replace(viejo, nuevo)
    return src


def construye():
    for srcp, anclas, dst, extra in ((SRC_CD, A_CD, 'codigo_cuerpo.py', CD_FIN), (SRC_MP, A_MP, 'motor_cuerpo.py', ''),
                                     (SRC_CA, A_CA, os.path.join('carros', 'FAMB_GRAM_ECO.py'), '')):
        src = open(srcp, encoding='utf-8').read()
        if src.startswith('# EXPLORATORIO, no es dato\n'): src = src[len('# EXPLORATORIO, no es dato\n'):]
        out = aplica(src, anclas, os.path.basename(srcp)) + extra
        cab = (f"# EXPLORATORIO, no es dato\n# {dst}: CONSTRUIDO por construye_cuerpo.py desde {os.path.relpath(srcp, ORG)} "
               f"(sha {hashlib.sha256(open(srcp, 'rb').read()).hexdigest()[:16]}). NO EDITAR A MANO.\n")
        p = os.path.join(AQUI, dst); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(cab + out)
        print('construido', p, hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16])


if __name__ == '__main__':
    construye()
