"""Genera mundo_largo_e.py = mundo_largo.py (9f74ff6b5941e5a5) + ESCALA DEL RECUERDO: en _sesgo_M el valor de cada sitio
recordado entra RECORTADO a [-sat_M,+sat_M] (saturacion), con dos controles: sat_barajada (el recorte que le tocaria a un
sitio se aplica en OTRO sitio, permutacion fija con RNG propio) y kappa_M (atenuacion uniforme, misma magnitud media sin
corregir la asimetria). Con sat_M=None, kappa_M=1.0, sat_barajada=False es mundo_largo EXACTO (identidad obligatoria).
Anclas con conteo exacto. Ejecuta PREREGISTRO_escala_mapa.md §1.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo', 'mundo_largo.py')
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    (["        pool=None,T_nuevo=None,reciclado=False,invertir_largo=None):   # mapa + largo"],
     ["        pool=None,T_nuevo=None,reciclado=False,invertir_largo=None,",
      "        sat_M=None,kappa_M=1.0,sat_barajada=False):   # mapa + largo + escala del recuerdo"], 1, 'firma'),
    (["    _Mpat=np.zeros((L,6)); _Mset=np.zeros(L,bool); _VACIO=np.zeros(6)   # mapa: tabla posicion -> ultimo patron visto"],
     ["    _Mpat=np.zeros((L,6)); _Mset=np.zeros(L,bool); _VACIO=np.zeros(6)   # mapa: tabla posicion -> ultimo patron visto",
      "    _nvis=np.zeros(L); _perm_s=None   # escala: pisadas por posicion (LECTURA, no entra en ninguna decision) y permutacion del control barajado",
      "    def _vM(p):   # escala: valor recordado de p tal como lo lee la BRUJULA (la boca sigue usando valor() entero)",
      "        _v=valor(_Mpat[p])",
      "        if sat_M is None: return _v   # sin recorte: exactamente el valor recordado (mundo_largo)",
      "        if _perm_s is None: return min(sat_M,max(-sat_M,_v))   # saturacion: un sitio recordado no pesa mas de una comida",
      "        _d=max(0.0,abs(valor(_Mpat[_perm_s[p]]))-sat_M)   # control: el RECORTE que le tocaria al sitio companero (mismo presupuesto total, atribucion rota)",
      "        return (1.0 if _v>=0 else -1.0)*max(0.0,abs(_v)-_d)"], 1, 'estado escala'),
    (["        _ren={x:0 for x in _SIT}; _vistos=list(dict.fromkeys(sitios))   # largo: ultima renovacion por sitio; patrones vistos en orden"],
     ["        _ren={x:0 for x in _SIT}; _vistos=list(dict.fromkeys(sitios))   # largo: ultima renovacion por sitio; patrones vistos en orden",
      "        if sat_barajada:   # control 1: permutacion fija de las 8 posiciones de sitio (M solo se escribe ahi); RNG propio, no toca el del organismo",
      "            _ps=np.array(sorted(_SIT)); _perm_s=np.arange(L); _perm_s[_ps]=_ps[np.random.default_rng(seed+950000).permutation(len(_ps))]"], 1, 'permutacion control'),
    (["    def _sesgo_M():   # mapa: con la retina vacia, valor recordado por direccion, descontado por distancia"],
     ["    def _sesgo_M():   # mapa: con la retina vacia, valor recordado por direccion, descontado por distancia",
      "        if sat_M is not None or kappa_M!=1.0:   # escala: mismo sesgo, pero el valor recordado entra recortado (y/o atenuado por kappa_M, control de lectura)",
      "            _si=sum(disc_M**h*_vM((pos-h)%L) for h in range(1,H_M+1) if _Mset[(pos-h)%L])",
      "            _sd=sum(disc_M**h*_vM((pos+h)%L) for h in range(1,H_M+1) if _Mset[(pos+h)%L])",
      "            return gamma_M*kappa_M*np.array([_si,_sd])"], 1, 'sesgo'),
    (["            if usa_M and escribe_M: _Mpat[pos]=PAT_L[objs[pos]]; _Mset[pos]=True   # mapa: recuerda lo que vio aqui"],
     ["            if usa_M and escribe_M: _Mpat[pos]=PAT_L[objs[pos]]; _Mset[pos]=True   # mapa: recuerda lo que vio aqui",
      "            _nvis[pos]+=1   # escala: lectura del mecanismo (pisar un sitio con el objeto presente; mismo evento que escribe el mapa)"], 1, 'pisada'),
    (["                curva=_curva,inyecciones=_iny,vistos=_vistos,comida_bin=_cbin,muertes_bin=_dbin,val_final=dict(val))   # largo"],
     ["                curva=_curva,inyecciones=_iny,vistos=_vistos,comida_bin=_cbin,muertes_bin=_dbin,val_final=dict(val),   # largo",
      "                esc_diag=dict(visitas={int(x):int(_nvis[x]) for x in _SIT}))   # escala: diagnostico (clave NUEVA, no criterio)"], 1, 'diagnostico'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != '9f74ff6b5941e5a5':
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != 9f74ff6b5941e5a5")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_largo_e = mundo_largo.py (9f74ff6b5941e5a5) + ESCALA DEL RECUERDO: en _sesgo_M el valor de cada sitio' + NL +
           'recordado entra recortado a [-sat_M,+sat_M], de modo que un veneno recordado deja de pesar 3 comidas en la brujula' + NL +
           '(la BOCA sigue decidiendo con valor() entero). Controles: sat_barajada (el recorte se aplica en otro sitio) y' + NL +
           'kappa_M (atenuacion uniforme, misma magnitud media con la asimetria intacta). Generado por construye_escala.py.' + NL +
           'NO editar. Con sat_M=None, kappa_M=1.0, sat_barajada=False es mundo_largo exacto (identidad obligatoria; clave' + NL +
           'extra esc_diag, diagnostico)."""' + NL)
    d = os.path.join(AQUI, 'mundo_largo_e.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
