# EXPLORATORIO, no es dato (instrumento de la SERIE preregistrada; lo que decide es la letra de corre_serie.py)
"""construye_serie.py — PROMETEO SERIE (Opus, equipo organelos, 25-sep-2026). MISION: llegar a la AGI por este camino.

Construye motor_serie.py desde ../motor_prometeo.py (SOLO LECTURA) por ANCLAS. Tres cambios:
  S1 MUDO (eco['mudo'] = 1): el control neutro. La cinta se copia, crece, recibe HGT y ARMA organos igual que en PROMETEO, pero los organos
     NO actuan: los CABLE no tocan boca/patas/parto (no se consume el rng del kit) y el organo de transmision EXPRESADO es siempre FILTRA0
     (el de la cinta inicial), diga lo que diga la cinta. Lo que se fije en MUDO se fija por deriva o por arrastre, no por lo que hace.
     Con mudo = 0 (defecto) es motor_prometeo BIT A BIT.
  S2 el estado del rng del kit (_RK) entra al checkpoint: reanudar == correr de un tiron (antes no: el rng del kit volvia a su semilla).
  S3 import de codigo_prometeo desde la carpeta de arriba (prometeo/).
  S4 (ERR-144, tras el humo) kit_nac mide el suministro de organos armados EN LA CINTA y DE NOVO (organos_serie.armados).
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(AQUI), 'motor_prometeo.py')
DST = os.path.join(AQUI, 'motor_serie.py')

ANCLAS = [
    # S3: rutas. _PROM pasa a ser prometeo/ (codigo_prometeo); serie/ tambien entra
    ("_PROM = os.path.dirname(os.path.abspath(__file__))   # PROMETEO (P0)\n",
     "_SERIE = os.path.dirname(os.path.abspath(__file__))   # SERIE (S3)\nif _SERIE not in sys.path: sys.path.insert(0, _SERIE)\n"
     "_PROM = os.path.dirname(_SERIE)   # PROMETEO (P0)\n"),
    # S1: la clave del eco
    ("codigo=None, c_on=True, c_sos=True, cambio=None)", "codigo=None, c_on=True, c_sos=True, cambio=None, mudo=0)"),
    ("        E_['gs0'] = [d[0] for d in _dv]; E_['gr0'] = [GD.valida(d[1], _tp) for d in _dv]",
     "        if E_['mudo'] not in (0, 1): raise SystemExit('SERIE: mudo 0 o 1')\n"
     "        E_['gs0'] = [d[0] for d in _dv]; E_['gr0'] = [GD.valida((GD.FILTRA0 if E_['mudo'] else d[1]), _tp) for d in _dv]   # SERIE (S1)"),
    ("    _CO = E_ is not None and E_['cod0'] is not None   # CODIGO v0",
     "    _CO = E_ is not None and E_['cod0'] is not None   # CODIGO v0\n    _MUDO = bool(_CO and E_['mudo'])   # SERIE (S1)"),
    ("            if b.kc is not None: a, mov = _kit_actua(b, a, mov, t)   # PROMETEO (K2)",
     "            if b.kc is not None and not _MUDO: a, mov = _kit_actua(b, a, mov, t)   # PROMETEO (K2) + SERIE (S1)"),
    ("                if (b.kc is not None and _kit_veto(b, t)) or",
     "                if (b.kc is not None and not _MUDO and _kit_veto(b, t)) or"),
    # S2: el rng del kit en el checkpoint
    ("    def _estado(tn):   # E7: TODO el estado en un solo pickle (los rng compartidos siguen compartidos)\n        import pickle\n",
     "    def _estado(tn):   # E7: TODO el estado en un solo pickle (los rng compartidos siguen compartidos)\n        import pickle\n"
     "        ES['_rk'] = _RK.getstate()   # SERIE (S2)\n"),
    # S4 (ERR-144, tras el humo): el SUMINISTRO se mide en la CINTA y DE NOVO. Antes la columna 4 de kit_nac contaba los slots del organo
    # EXPRESADO, que en MUDO es siempre FILTRA0 (-> 0): la guardia comparaba cosas distintas. Columnas nuevas: [5] el hijo lleva un organo
    # armado que la cinta del donante NO llevaba (creado por error de copia o HGT en ESTE parto); [6] el hijo lleva algun organo armado (cinta).
    ("_grh if tuple(s_[:4]) != (1, 3, 0, 0))])\n",
     "_grh if tuple(s_[:4]) != (1, 3, 0, 0)), int(bool(OS.armados(_cih) - OS.armados(_dci))), int(bool(OS.armados(_cih)))])   # SERIE (S4, ERR-144)\n"),
    ("import codigo_prometeo as CD   # PROMETEO (antes codigo_def)\n",
     "import codigo_prometeo as CD   # PROMETEO (antes codigo_def)\nimport organos_serie as OS   # SERIE (S4, ERR-144)\n"),
    ("ES.clear(); ES.update(st['ES'])",
     "ES.clear(); ES.update(st['ES'])\n        if '_rk' in ES: _RK.setstate(ES['_rk'])   # SERIE (S2)"),
]
# S1: el organo EXPRESADO en MUDO (dos sitios con el mismo texto: _cod y _hgt)
A_GR = ("        g2, gr2, _dd = CD.desarrolla(c2, E_['G0'], E_['lo'], E_['hi'], ENTEROS); gr2 = GD.valida(gr2, int(E_['g_tope']))\n",
        "        g2, gr2, _dd = CD.desarrolla(c2, E_['G0'], E_['lo'], E_['hi'], ENTEROS); gr2 = GD.valida(gr2, int(E_['g_tope']))\n"
        "        if _MUDO: gr2 = GD.valida(GD.FILTRA0, int(E_['g_tope']))   # SERIE (S1): el organo no se expresa\n")


def construye():
    src = open(SRC, encoding='utf-8').read()
    for viejo, nuevo in ANCLAS:
        if src.count(viejo) != 1: raise SystemExit(f"SERIE: ancla no unica ({src.count(viejo)}): {viejo[:90]!r}")
        src = src.replace(viejo, nuevo)
    if src.count(A_GR[0]) != 2: raise SystemExit(f"SERIE: ancla A_GR aparece {src.count(A_GR[0])} veces (se esperan 2)")
    src = src.replace(A_GR[0], A_GR[1])
    if src.startswith('# EXPLORATORIO, no es dato\n'): src = src[len('# EXPLORATORIO, no es dato\n'):]
    cab = (f"# EXPLORATORIO, no es dato (instrumento de la serie)\n# motor_serie.py: CONSTRUIDO por construye_serie.py desde motor_prometeo.py "
           f"(sha {hashlib.sha256(open(SRC, 'rb').read()).hexdigest()[:16]}). NO EDITAR A MANO.\n")
    open(DST, 'w', encoding='utf-8').write(cab + src)
    print('construido', DST, hashlib.sha256(open(DST, 'rb').read()).hexdigest()[:16])


if __name__ == '__main__':
    construye()
