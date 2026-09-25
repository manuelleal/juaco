"""construye_endo.py — CONSTRUYE POR ANCLAS el instrumento de ENDOSIMBIOSIS (equipo organelos, Opus B, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Origenes (SOLO se LEEN; sha fijado; nada existente se modifica):
  experimentos/juaco_eco/motor_eco3.py            2eec9830792d9822 -> darwin/motor_endo.py
  experimentos/juaco_eco/carros/FABRICA_ECO.py    f1163009cb5193a2 -> darwin/carros/FABRICA_SIMB.py
motor_endo = motor_eco3 + GANCHOS a simbiontes.py (codigo nuevo) + el argumento simb (None -> motor_eco3 BIT A BIT, arnes (A)):
  G1 rutas: la copia vive en experimentos/organelos/darwin; pista2 sigue en experimentos/generaciones y los carros de ECO en
     experimentos/juaco_eco/carros (se buscan despues de darwin/carros).
  G2 Cuerpo: tres ranuras nuevas (sm = simbionte de adentro, sm_nac = lo trajo al nacer, sm0 = su indice I al nacer).
  G3 simb=dict(...) crea la Ecologia (replicadores libres + tragar + herencia + canal) con su PROPIO rng [seed, 0, 30, 0].
  G4 ganchos: banco del vivero alineado (banco_ini, funda con el indice del banco, parto), canal en obs['simb'] (fase A), conteo de
     decisiones de boca, paso de la ecologia antes de la fase B, registro de individuos, muestra, salida d['simb'].
  G5 ERR-60 / nube-9: con simb, la guardia de 100000 cuerpos por linaje NO lanza SystemExit (dentro de un Pool colgaria la serie en
     silencio): se REGISTRA (ES['err60'], d['simb']['err60']) y la corrida termina en ese paso (t_trunc). Con simb=None lanza lo mismo que
     motor_eco3. El limite es la constante NAC_MAX (= 100000) para que el arnes pueda probar la guardia.
carros/FABRICA_SIMB = FABRICA_ECO + UNA linea: si obs['simb'] existe, Vb += obs['simb'][letra] (el canal). Sin obs['simb'] es FABRICA_ECO.
Uso: python experimentos/organelos/darwin/construye_endo.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')
ORIG_MOTOR = os.path.join(ECO, 'motor_eco3.py'); SHA_MOTOR = '2eec9830792d9822'
ORIG_CARRO = os.path.join(ECO, 'carros', 'FABRICA_ECO.py'); SHA_CARRO = 'f1163009cb5193a2'
DEST_MOTOR = os.path.join(AQUI, 'motor_endo.py')
DEST_CARRO = os.path.join(AQUI, 'carros', 'FABRICA_SIMB.py')


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def h16s(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


def aplica(txt, anclas, nombre):
    for i, (a, b) in enumerate(anclas):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"CONSTRUYE {nombre}: ancla {i} aparece {n} veces (debe ser 1): {a[:70]!r}")
        txt = txt.replace(a, b)
    return txt


E60 = "raise SystemExit('PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)')"
ANCLAS_MOTOR = [
    ('"""motor_eco3.py (CONSTRUIDO',
     '"""motor_endo.py (CONSTRUIDO por experimentos/organelos/darwin/construye_endo.py desde juaco_eco/motor_eco3.py, sha '
     f'{SHA_MOTOR}; NO editar a mano).\nENDOSIMBIOSIS: ganchos a simbiontes.py; con simb=None es motor_eco3 BIT A BIT. Lo que sigue es el docstring del origen.\n\n'
     'motor_eco3.py (CONSTRUIDO'),
    ("GEN = os.path.join(os.path.dirname(AQUI), 'generaciones')      # pista2 (mundo de la pista v2), solo se LEE\n",
     "GEN = os.path.join(os.path.dirname(os.path.dirname(AQUI)), 'generaciones')   # ENDO G1: la copia vive en experimentos/organelos/darwin\n"),
    ("CARROS_ECO = os.path.join(AQUI, 'carros')\n",
     "CARROS_ECO = os.path.join(AQUI, 'carros')\n"
     "CARROS_ECO0 = os.path.join(os.path.dirname(os.path.dirname(AQUI)), 'juaco_eco', 'carros')   # ENDO G1: FABRICA_ECO y los de ECO\n"
     "import simbiontes as SIM   # ENDO G3\n"
     "NAC_MAX = 100000   # ENDO G5: el limite de ERR-60 (el mismo); constante del modulo para que el arnes pruebe la guardia\n"),
    ('    ruta = os.path.join(CARROS_ECO, f"{ident}.py")\n    if not os.path.exists(ruta):\n',
     '    ruta = os.path.join(CARROS_ECO, f"{ident}.py")\n    if not os.path.exists(ruta): ruta = os.path.join(CARROS_ECO0, f"{ident}.py")   # ENDO G1\n'
     '    if not os.path.exists(ruta):\n'),
    ("'ult_mordida', 'vol_kk', 'hijos', 'fund', 'vivo', 'hvivos', 'pc', 'g', 's')",
     "'ult_mordida', 'vol_kk', 'hijos', 'fund', 'vivo', 'hvivos', 'pc', 'g', 's', 'sm', 'sm_nac', 'sm0')   # ENDO G2"),
    ("self.g = None; self.s = None   # pc = cuerpo padre",
     "self.g = None; self.s = None; self.sm = None; self.sm_nac = 0; self.sm0 = None   # ENDO G2 · pc = cuerpo padre"),
    ("muestra=MUESTRA, reposicion='fija', r_rep=R_REP, eco=None):",
     "muestra=MUESTRA, reposicion='fija', r_rep=R_REP, eco=None, simb=None):"),
    ("    E_ = None if eco is None else _eco_cfg(eco, CF, n)\n",
     "    E_ = None if eco is None else _eco_cfg(eco, CF, n)\n"
     "    SB = None if simb is None else SIM.Ecologia(seed, L, esc, simb, E_, CF['PAT'])   # ENDO G3 (rng propio [seed, 0, 30, 0])\n"),
    ("    def registra(b, tm, causa, vd):\n        L_ = lin[b.lin]\n",
     "    def registra(b, tm, causa, vd):\n        if SB is not None: SB.registra(b, tm)   # ENDO G4\n        L_ = lin[b.lin]\n"),
    ("[(b.g.copy(), b.s.copy()) for b in cuerpos][-int(E_['banco']):]   # E9\n",
     "[(b.g.copy(), b.s.copy()) for b in cuerpos][-int(E_['banco']):]   # E9\n"
     "    if SB is not None: SB.banco_ini(len(ES['banco']))   # ENDO G4: banco de simbiontes alineado con el de genomas\n"),
    ("            for l in lin: l.tam.append(l.vivos)\n            tam_total.append(total)\n",
     "            for l in lin: l.tam.append(l.vivos)\n            tam_total.append(total)\n"
     "            if SB is not None: SB.muestra(t, cuerpos)   # ENDO G4\n"),
    ("o['cuerpos'] = foto; o['pizarra'] = piz_t\n",
     "o['cuerpos'] = foto; o['pizarra'] = piz_t\n"
     "            if SB is not None: o['simb'] = SB.canal(b)   # ENDO G4: el canal (None sin simbionte o con el canal apagado)\n"),
    ("                kk = objs[pos]; mordio = bool(a.get('muerde', False)); q = l.q(t)\n",
     "                kk = objs[pos]; mordio = bool(a.get('muerde', False)); q = l.q(t)\n"
     "                if SB is not None: SB.decision(b, kk, mordio)   # ENDO G4 (solo cuenta)\n"),
    ("        # ---------------- fase B\n",
     "        if SB is not None: SB.paso(t, objs, cuerpos)   # ENDO G4: libres, tragar, costo de alojar, perdida interna\n"
     "        # ---------------- fase B\n"),
    ("                if l.nac >= 100000: " + E60 + "\n",
     "                if l.nac >= NAC_MAX:   # ENDO G5 (nube-9)\n"
     "                    if SB is None: " + E60 + "\n"
     "                    ES['err60'] = dict(t=int(t), lin=int(i), donde='fundador'); break\n"),
    ("                _gf = _sf = None\n", "                _gf = _sf = None; _ib = None\n"),
    ("                        _gb, _sb = ES['banco'][int(SE(i, ETQ_BANCO, l.nac).integers(len(ES['banco'])))]\n",
     "                        _ib = int(SE(i, ETQ_BANCO, l.nac).integers(len(ES['banco']))); _gb, _sb = ES['banco'][_ib]   # ENDO G4: el indice\n"),
    ("                if E_ is not None: F.g = _gf; F.s = _sf\n",
     "                if E_ is not None: F.g = _gf; F.s = _sf\n"
     "                if SB is not None: SB.funda(F, _ib, t)   # ENDO G4: el fundador del vivero hereda el simbionte de esa entrada\n"),
    ("                    if k >= 100000: " + E60 + "\n",
     "                    if k >= NAC_MAX:   # ENDO G5 (nube-9)\n"
     "                        if SB is None: " + E60 + "\n"
     "                        ES['err60'] = dict(t=int(t), lin=int(i), donde='parto'); break\n"),
    ("                    nuevos.append(H); l.vivos += 1; total += 1; id2lin[hid] = i\n",
     "                    nuevos.append(H); l.vivos += 1; total += 1; id2lin[hid] = i\n"
     "                    if SB is not None: SB.parto(b, H, t)   # ENDO G4: herencia del simbionte (y banco alineado)\n"),
    ("                ES['t_ext'] = t + 1; break\n",
     "                ES['t_ext'] = t + 1; break\n"
     "            if ES.get('err60') is not None: ES['t_trunc'] = t + 1; break   # ENDO G5 (nube-9): registrada, termina\n"),
    ("    return dict(linajes=out, pizarra_log=piz_log,\n",
     "    _simb = None if SB is None else SB.salida(T, cuerpos, ES)   # ENDO G4\n"
     "    return dict(linajes=out, pizarra_log=piz_log, **({} if SB is None else dict(simb=_simb)),\n"),
]

ANCLAS_CARRO = [
    ('"""carros/FABRICA_ECO.py (CONSTRUIDO',
     '"""carros/FABRICA_SIMB.py (CONSTRUIDO por experimentos/organelos/darwin/construye_endo.py desde juaco_eco/carros/FABRICA_ECO.py, sha '
     f'{SHA_CARRO}; NO editar a mano).\nUNICO cambio: el CANAL del simbionte (obs[\'simb\'] = letra -> numero) se SUMA a la entrada de la boca Vb. '
     'Sin obs[\'simb\'] es FABRICA_ECO bit a bit.\nLo que sigue es el docstring del origen.\n\ncarros/FABRICA_ECO.py (CONSTRUIDO'),
    ("            Vb = self.ALPHA * _wt + self.HAMBRE_BOCA * hambre + .5\n",
     "            Vb = self.ALPHA * _wt + self.HAMBRE_BOCA * hambre + .5\n"
     "            _simb = obs.get('simb')\n"
     "            if _simb is not None: Vb = Vb + _simb[kk]   # ENDO: canal del simbionte (organelos, darwin)\n"),
]


def textos():
    if h16(ORIG_MOTOR) != SHA_MOTOR: raise SystemExit(f"CONSTRUYE: motor_eco3.py cambio ({h16(ORIG_MOTOR)})")
    if h16(ORIG_CARRO) != SHA_CARRO: raise SystemExit(f"CONSTRUYE: FABRICA_ECO.py cambio ({h16(ORIG_CARRO)})")
    m = aplica(open(ORIG_MOTOR, encoding='utf-8').read(), ANCLAS_MOTOR, 'motor_endo')
    c = aplica(open(ORIG_CARRO, encoding='utf-8').read(), ANCLAS_CARRO, 'FABRICA_SIMB')
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
