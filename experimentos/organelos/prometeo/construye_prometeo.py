# EXPLORATORIO, no es dato
"""construye_prometeo.py — PROMETEO (Opus, equipo organelos, 24-sep-2026). MISION: llegar a la AGI por este camino.

Construye por ANCLAS de texto (los originales solo se LEEN):
  codigo_prometeo.py  <- ../codigo/codigo_def.py         (la cinta v0 + el KIT: CABLE y HGT en el alfabeto; ALF elegible por brazo)
  motor_prometeo.py   <- ../codigo/exploracion_fable/motor_fable.py   (el cuerpo LEE sus cables y su HGT; la fisica del mundo no se toca)

EL KIT (nace AUSENTE de la cinta inicial; solo entra por insercion/cambio/duplicacion de la copia, o por HGT):
  CABLE s d w   senal interna s (0..5) -> decision d (0 boca, 1 patas, 2 parto) con peso w (-3..3). Lo interpreta el LECTOR (entra en
                REP, DEF y LLAMA como cualquier gen: un REP 2 duplica el peso). Senales PRESENTES del cuerpo (las del cruce):
                s = (sesgo 1, reserva min(E,Ag)/1.5, la otra max(E,Ag)/1.5, ventana de parto recorrida gv/rep_X, edad/2000, hijos vivos/4).
                BOCA : z = 0.5 * W[0].s ; si el carro quiere morder y z < 0, NO muerde con prob 1 - e^z; si no quiere y z > 0, muerde con 1 - e^-z.
                PATAS: z = 0.5 * W[1].s ; si esta quieto y z > 0, da un paso (lado al azar) con prob 1 - e^-z; si se mueve y z < 0, se queda con 1 - e^z.
                PARTO: si W[2].s < 0 la ventana de parto se VETA (como el gen de parto del cruce; con pesos 0 pare siempre).
  HGT p l       transferencia horizontal: al NACER, con prob P_HGT[p], el hijo copia un tramo de largo L_HGT[l] de la cinta del VECINO
                vivo mas cercano (cualquier linaje; distancia en el anillo; sin rng para elegirlo) y lo INSERTA en un punto al azar de
                su cinta. Vale la PRIMERA HGT de la cinta (como SOS). La cinta decide si comparte y cuanto.
  ORG           el slot de transmision (cuando, que, a quien, como) YA esta en el alfabeto v0: el kit no lo agrega; se cuenta como organo nuevo
                cada slot distinto del de filtra0.
  (simbionte: NO entra; no es barato en este motor: no hay objeto que tragar. Declarado.)
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
SRC_CD = os.path.join(ORG, 'codigo', 'codigo_def.py')
SRC_MF = os.path.join(ORG, 'codigo', 'exploracion_fable', 'motor_fable.py')

A_CD = [
    ("OPS = ('SUM', 'EJE', 'ORG', 'REP', 'DEF', 'LLAMA', 'FIN', 'TASA', 'SOS')\n",
     "OPS = ('SUM', 'EJE', 'ORG', 'REP', 'DEF', 'LLAMA', 'FIN', 'TASA', 'SOS')\n"
     "KIT = ('CABLE', 'HGT')   # PROMETEO (K0): el material para sus organos\n"
     "ALF = [OPS]              # PROMETEO: alfabeto de las instrucciones AL AZAR (insercion, cambio entero); con OPS es v0 bit a bit\n"
     "N_SEN = 6; N_DEC = 3\n"
     "P_HGT = (0.02, 0.05, 0.1, 0.25); L_HGT = (1, 2, 4, 8)\n\n\n"
     "def pon_alfabeto(ops):\n    ops = tuple(ops)\n    for o in ops:\n        if o not in OPS + KIT: raise SystemExit(f'PROMETEO: op {o}')\n    ALF[0] = ops\n"),
    ("            'TASA': ((0, len(TASAS) - 1),), 'SOS': ((0, len(U_SOS) - 1), (0, len(F_SOS) - 1))}[op]",
     "            'TASA': ((0, len(TASAS) - 1),), 'SOS': ((0, len(U_SOS) - 1), (0, len(F_SOS) - 1)),\n"
     "            'CABLE': ((0, N_SEN - 1), (0, N_DEC - 1), (-3, 3)), 'HGT': ((0, len(P_HGT) - 1), (0, len(L_HGT) - 1))}[op]   # PROMETEO"),
    ("NUMERICO = {('SUM', 1), ('EJE', 1)}", "NUMERICO = {('SUM', 1), ('EJE', 1), ('CABLE', 2)}"),
    ("        if not ins or ins[0] not in OPS: raise", "        if not ins or ins[0] not in OPS + KIT: raise"),
    ("    x = [0.0] * N_RASGOS; gram = []; st = dict(pasos=0, llamadas=0, corte=0)",
     "    x = [0.0] * N_RASGOS; gram = []; st = dict(pasos=0, llamadas=0, corte=0, cable=None)   # PROMETEO: cable = W[d][s]"),
    ("            elif op == 'LLAMA':",
     "            elif op == 'CABLE':   # PROMETEO (K1)\n"
     "                if ins[3]:\n"
     "                    if st['cable'] is None: st['cable'] = [[0.0] * N_SEN for _ in range(N_DEC)]\n"
     "                    st['cable'][ins[2]][ins[1]] += ins[3]\n"
     "            elif op == 'LLAMA':"),
    ("    op = OPS[int(r.random() * len(OPS))]", "    op = ALF[0][int(r.random() * len(ALF[0]))]   # PROMETEO"),
]
CD_FIN = '''

# ================================================================= PROMETEO: lo que el cuerpo lee del kit
def regla_hgt(cinta):
    for ins in cinta:
        if ins[0] == 'HGT': return P_HGT[ins[1]], L_HGT[ins[2]]
    return None


def organos(cinta, G0, lo, hi, enteros):
    """(W o None, hgt o None, gram). W = None si ningun peso distinto de 0 (el cuerpo no lee nada nuevo)."""
    g, gram, st = desarrolla(cinta, G0, lo, hi, enteros)
    W = st['cable']
    if W is not None and not any(v != 0.0 for f in W for v in f): W = None
    return W, regla_hgt(cinta), gram
'''

A_MF = [
    ("_FABLE = os.path.dirname(os.path.abspath(__file__))   # FABLE (F0)\n",
     "_PROM = os.path.dirname(os.path.abspath(__file__))   # PROMETEO (P0)\nif _PROM not in sys.path: sys.path.insert(0, _PROM)\n"
     "_FABLE = os.path.join(os.path.dirname(_PROM), 'codigo', 'exploracion_fable')   # FABLE (F0)\n"),
    ("import codigo_def as CD   # CODIGO v0\n", "import codigo_prometeo as CD   # PROMETEO (antes codigo_def)\nimport random as _random\n"),
    ("'cin', 'mb')", "'cin', 'mb', 'kc')"),
    ("        self.cin = None; self.mb = None", "        self.cin = None; self.mb = None; self.kc = None"),
    ("            if _CO: cuerpos[-1].cin = E_['cod0'][i]; cuerpos[-1].mb = []   # CODIGO v0",
     "            if _CO: cuerpos[-1].cin = E_['cod0'][i]; cuerpos[-1].mb = []; cuerpos[-1].kc = _kc(E_['cod0'][i])   # CODIGO v0 + PROMETEO"),
    # funciones del kit: se definen justo antes de _fmal (dentro de run_solapadas; ven E_, ES, cuerpos por cierre)
    ("    cuerpos = []\n    for i, (e, mod) in enumerate(mods):",
     "    _KCC = {}; _RK = _random.Random(seed * 7919 + 24)   # PROMETEO (K2): cache cinta -> cables; rng propio del kit (no toca ningun otro)\n"
     "    def _kc(cin):\n"
     "        if cin is None: return None\n"
     "        w = _KCC.get(cin)\n"
     "        if w is None:\n"
     "            w = CD.organos(cin, E_['G0'], E_['lo'], E_['hi'], ENTEROS)[0] or 0\n"
     "            if len(_KCC) < 200000: _KCC[cin] = w\n"
     "        return w or None\n"
     "    def _sen(b, t):\n"
     "        _rx = M['rep_X'] if b.g is None else b.g[I_RX]; e1 = min(b.E, b.Ag); e2 = max(b.E, b.Ag)\n"
     "        return (1.0, e1 / 1.5, e2 / 1.5, b.gv / float(_rx), (t - b.tn) / 2000.0, b.hvivos / 4.0)\n"
     "    def _kit_actua(b, a, mov, t):\n"
     "        W = b.kc; s = _sen(b, t); KS = ES.setdefault('kit', dict(boca_si=0, boca_no=0, pata_mueve=0, pata_para=0, veto=0, hgt=0, hgt_ops={}))\n"
     "        zb = 0.5 * sum(W[0][q] * s[q] for q in range(6)); zp = 0.5 * sum(W[1][q] * s[q] for q in range(6))\n"
     "        if zb != 0.0:\n"
     "            u = _RK.random(); mu = bool(a.get('muerde', False))\n"
     "            if mu and zb < 0 and u < 1.0 - math.exp(zb): a = dict(a); a['muerde'] = False; KS['boca_no'] += 1\n"
     "            elif (not mu) and zb > 0 and u < 1.0 - math.exp(-zb): a = dict(a); a['muerde'] = True; KS['boca_si'] += 1\n"
     "        if zp != 0.0:\n"
     "            u = _RK.random()\n"
     "            if mov == 0 and zp > 0 and u < 1.0 - math.exp(-zp): mov = 1 if _RK.random() < 0.5 else -1; KS['pata_mueve'] += 1\n"
     "            elif mov != 0 and zp < 0 and u < 1.0 - math.exp(zp): mov = 0; KS['pata_para'] += 1\n"
     "        return a, mov\n"
     "    def _kit_veto(b, t):\n"
     "        W = b.kc; s = _sen(b, t)\n"
     "        v = sum(W[2][q] * s[q] for q in range(6)) < 0\n"
     "        if v: ES.setdefault('kit', dict(boca_si=0, boca_no=0, pata_mueve=0, pata_para=0, veto=0, hgt=0, hgt_ops={}))['veto'] += 1\n"
     "        return v\n"
     "    def _hgt(cin, g, gr, b, i, k, t):   # PROMETEO (K3): la cinta del hijo toma un tramo de la del vecino mas cercano\n"
     "        rh = CD.regla_hgt(cin)\n"
     "        if rh is None: return cin, g, gr\n"
     "        r = SE(i, 24, k)\n"
     "        if r.random() >= rh[0]: return cin, g, gr\n"
     "        best = None; bd = None\n"
     "        for z in cuerpos:\n"
     "            if z is b or not z.vivo or z.cin is None: continue\n"
     "            dd = abs(z.pos - b.pos); dd = min(dd, L - dd)\n"
     "            if bd is None or dd < bd: best = z; bd = dd\n"
     "        if best is None or not best.cin: return cin, g, gr\n"
     "        dc = best.cin; s0 = int(r.random() * len(dc)); tr = tuple(dc[s0:s0 + rh[1]]); q = int(r.random() * (len(cin) + 1))\n"
     "        c2 = tuple((cin[:q] + tr + cin[q:])[:CD.TOPE_CINTA])\n"
     "        g2, gr2, _dd = CD.desarrolla(c2, E_['G0'], E_['lo'], E_['hi'], ENTEROS); gr2 = GD.valida(gr2, int(E_['g_tope']))\n"
     "        KS = ES.setdefault('kit', dict(boca_si=0, boca_no=0, pata_mueve=0, pata_para=0, veto=0, hgt=0, hgt_ops={})); KS['hgt'] += 1\n"
     "        for x in tr: KS['hgt_ops'][x[0]] = KS['hgt_ops'].get(x[0], 0) + 1\n"
     "        ES.setdefault('hgt_ev', []).append([t, i, k, best.lin, len(tr), int(best.lin != i)]) if len(ES.get('hgt_ev', [])) < 20000 else None\n"
     "        return c2, g2, gr2\n"
     "    cuerpos = []\n    for i, (e, mod) in enumerate(mods):"),
    ("            mov = int(a.get('mov', 0))\n",
     "            mov = int(a.get('mov', 0))\n            if b.kc is not None: a, mov = _kit_actua(b, a, mov, t)   # PROMETEO (K2)\n"),
    ("                if hasattr(c, 'quiere_parir') and not c.quiere_parir(",
     "                if (b.kc is not None and _kit_veto(b, t)) or hasattr(c, 'quiere_parir') and not c.quiere_parir("),
    ("                        if _CO: _cih, _gh, _grh = _cod(_dci, SE(i, ETQ_CMUT, k), _fmal(b), _dg, _dgr, i, k, t, b.k)   # CODIGO v0 (C3)\n",
     "                        if _CO: _cih, _gh, _grh = _cod(_dci, SE(i, ETQ_CMUT, k), _fmal(b), _dg, _dgr, i, k, t, b.k)   # CODIGO v0 (C3)\n"
     "                        if _CO: _cih, _gh, _grh = _hgt(_cih, _gh, _grh, b, i, k, t)   # PROMETEO (K3)\n"
     "                        if _CO and len(ES.setdefault('kit_nac', [])) < 60000:   # PROMETEO: presencia del kit por nacimiento\n"
     "                            _w = _kc(_cih); ES['kit_nac'].append([t, len(_cih), (0 if _w is None else sum(1 for f in _w for v in f if v != 0.0)), int(CD.regla_hgt(_cih) is not None), sum(1 for s_ in _grh if tuple(s_[:4]) != (1, 3, 0, 0))])\n"),
    ("H.cin = _cih; H.mb = ([] if _CO else None)", "H.cin = _cih; H.mb = ([] if _CO else None); H.kc = (_kc(_cih) if _CO else None)"),
    ("F.cin = _cif; F.mb = ([] if _CO else None)", "F.cin = _cif; F.mb = ([] if _CO else None); F.kc = (_kc(_cif) if _CO else None)"),
    ("                if _GR: ES['gcorte'] = dict(",
     "                if _CO: ES['cod_corte'] = dict(banco=[list(e[4]) for e in ES['banco'] if e[4] is not None], vivos=[list(z.cin) for z in _vv if z.cin is not None][:200])   # PROMETEO\n"
     "                if _GR: ES['gcorte'] = dict("),
    ("        cintas_vivos=[[b.lin, b.k, b.gen, [list(x) for x in b.cin]] for b in cuerpos if b.vivo and b.cin is not None][:80]))",
     "        cintas_vivos=[[b.lin, b.k, b.gen, [list(x) for x in b.cin]] for b in cuerpos if b.vivo and b.cin is not None][:80],\n"
     "        prometeo=dict(kit=ES.get('kit'), kit_nac=ES.get('kit_nac', []), hgt_ev=ES.get('hgt_ev', []), cod_corte=ES.get('cod_corte'),\n"
     "                      banco_final=[list(e[4]) for e in ES['banco'] if e[4] is not None], alfabeto=list(CD.ALF[0]))))   # PROMETEO"),
]


def aplica(src, anclas, nombre):
    for viejo, nuevo in anclas:
        if src.count(viejo) != 1: raise SystemExit(f"PROMETEO: ancla no unica en {nombre} ({src.count(viejo)}): {viejo[:90]!r}")
        src = src.replace(viejo, nuevo)
    return src


def construye():
    for srcp, anclas, dst, extra in ((SRC_CD, A_CD, 'codigo_prometeo.py', CD_FIN), (SRC_MF, A_MF, 'motor_prometeo.py', '')):
        src = open(srcp, encoding='utf-8').read()
        if src.startswith('# EXPLORATORIO, no es dato\n'): src = src[len('# EXPLORATORIO, no es dato\n'):]
        out = aplica(src, anclas, os.path.basename(srcp)) + extra
        cab = (f"# EXPLORATORIO, no es dato\n# {dst}: CONSTRUIDO por construye_prometeo.py desde {os.path.basename(srcp)} "
               f"(sha {hashlib.sha256(open(srcp, 'rb').read()).hexdigest()[:16]}). NO EDITAR A MANO.\n")
        p = os.path.join(AQUI, dst); open(p, 'w', encoding='utf-8').write(cab + out)
        print('construido', p, hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16])


if __name__ == '__main__':
    construye()
