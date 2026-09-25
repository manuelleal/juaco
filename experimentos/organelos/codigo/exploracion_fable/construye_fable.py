# EXPLORATORIO, no es dato
"""construye_fable.py — construye motor_fable.py desde ../motor_codigo.py (SOLO LECTURA) por ANCLAS de texto (Fable, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Cinco anclas. Con eco['cambio'] = tupla (t, X, Y) el motor construido es motor_codigo BIT A BIT (lo verifica identidad_fable.py).
Con eco['cambio'] = dict (spec de fable_mundos) el efecto de cada letra en cada paso lo da fable_mundos.efecto(spec, t, EF0, L).
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(os.path.dirname(AQUI), 'motor_codigo.py')
DESTINO = os.path.join(AQUI, 'motor_fable.py')

ANCLAS = [
    # A1: validacion del cambio: se acepta un dict (spec de fable_mundos)
    ("    if E_['cambio'] is not None:   # CODIGO v0 (C4)\n        _c = tuple(E_['cambio'])",
     "    if isinstance(E_['cambio'], dict): FB.valida(E_['cambio'])   # FABLE (F1)\n"
     "    elif E_['cambio'] is not None:   # CODIGO v0 (C4)\n        _c = tuple(E_['cambio'])"),
    # A2: _CB (tiempo del primer cambio, para mord_signo pre/post) y _FB (el spec)
    ("    _CB = None if E_ is None or E_['cambio'] is None else (int(E_['cambio'][0]), str(E_['cambio'][1]), str(E_['cambio'][2]))",
     "    _FB = E_['cambio'] if (E_ is not None and isinstance(E_['cambio'], dict)) else None   # FABLE (F2)\n"
     "    _CB = None if E_ is None or E_['cambio'] is None else ((int(_FB['t']), str(_FB.get('X', 'A')), str(_FB.get('Y', 'B'))) if _FB is not None else (int(E_['cambio'][0]), str(E_['cambio'][1]), str(E_['cambio'][2])))\n"
     "    _EF0 = {k: tuple(EFECTO[VAL_VIVO[k]]) for k in 'ABCD'}   # FABLE: la tabla de fabrica"),
    # A3: reanudar: el intercambio viejo solo si NO es spec
    ("    if _CB is not None and _t0 > _CB[0]: VAL_VIVO = dict(VAL_VIVO); VAL_VIVO[_CB[1]], VAL_VIVO[_CB[2]] = VAL_VIVO[_CB[2]], VAL_VIVO[_CB[1]]   # reanudar",
     "    if _FB is None and _CB is not None and _t0 > _CB[0]: VAL_VIVO = dict(VAL_VIVO); VAL_VIVO[_CB[1]], VAL_VIVO[_CB[2]] = VAL_VIVO[_CB[2]], VAL_VIVO[_CB[1]]   # reanudar"),
    # A4: el paso: con spec, la tabla vigente se calcula en cada paso (pura, sin rng)
    ("        if _CB is not None and t == _CB[0]:   # CODIGO v0 (C4): EL MUNDO CAMBIA (se intercambia el valor de dos letras)\n"
     "            VAL_VIVO = dict(VAL_VIVO); VAL_VIVO[_CB[1]], VAL_VIVO[_CB[2]] = VAL_VIVO[_CB[2]], VAL_VIVO[_CB[1]]",
     "        _EFT = None if _FB is None else FB.efecto(_FB, t, _EF0, L)   # FABLE (F4)\n"
     "        if _FB is None and _CB is not None and t == _CB[0]:   # CODIGO v0 (C4): EL MUNDO CAMBIA (se intercambia el valor de dos letras)\n"
     "            VAL_VIVO = dict(VAL_VIVO); VAL_VIVO[_CB[1]], VAL_VIVO[_CB[2]] = VAL_VIVO[_CB[2]], VAL_VIVO[_CB[1]]"),
    # A5: la mordida lee la tabla vigente (por letra y posicion)
    ("                    _dS = EFECTO[VAL_VIVO[kk]]\n",
     "                    _dS = EFECTO[VAL_VIVO[kk]] if _EFT is None else _EFT(kk, pos)   # FABLE (F5)\n"),
    # A6: import
    ("import codigo_def as CD   # CODIGO v0\n",
     "import codigo_def as CD   # CODIGO v0\nimport fable_mundos as FB   # FABLE\n"),
    # A0: AQUI = codigo/ (carros, gramatica_def, codigo_def); la carpeta de la exploracion entra a sys.path para fable_mundos
    ("AQUI = os.path.dirname(os.path.abspath(__file__))\nif AQUI not in sys.path: sys.path.insert(0, AQUI)\n",
     "_FABLE = os.path.dirname(os.path.abspath(__file__))   # FABLE (F0)\nif _FABLE not in sys.path: sys.path.insert(0, _FABLE)\n"
     "AQUI = os.path.dirname(_FABLE)   # FABLE: la carpeta codigo/\nif AQUI not in sys.path: sys.path.insert(0, AQUI)\n"),
]


def construye():
    src = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo in ANCLAS:
        if src.count(viejo) != 1: raise SystemExit(f"FABLE: ancla no unica ({src.count(viejo)}): {viejo[:80]!r}")
        src = src.replace(viejo, nuevo)
    cab = ('# EXPLORATORIO, no es dato\n# motor_fable.py: CONSTRUIDO por construye_fable.py desde motor_codigo.py (sha %s). NO EDITAR A MANO.\n'
           % hashlib.sha256(open(ORIGEN, 'rb').read()).hexdigest()[:16])
    open(DESTINO, 'w', encoding='utf-8').write(cab + src)
    print('construido', DESTINO, hashlib.sha256(open(DESTINO, 'rb').read()).hexdigest()[:16])


if __name__ == '__main__':
    construye()
