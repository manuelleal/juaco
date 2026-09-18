"""Genera mundo_largo_n.py = mundo_largo.py (9f74ff6b5941e5a5) + novedad de sitio (reloj t_visita por posicion, sesgo
gamma_N con la retina vacia sobre los sitios que M ya conoce) + dos controles (novedad barajada entre sitios, novedad
constante). Con gamma_N=0 es mundo_largo EXACTO (identidad obligatoria). Anclas con conteo exacto.
Ejecuta PREREGISTRO_novedad_sitio.md §1.
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
      "        gamma_N=0.0,tau_N=4000.0,nov_barajada=False,nov_cte=False):   # mapa + largo + novedad de sitio"], 1, 'firma'),
    (["    _Mpat=np.zeros((L,6)); _Mset=np.zeros(L,bool); _VACIO=np.zeros(6)   # mapa: tabla posicion -> ultimo patron visto"],
     ["    _Mpat=np.zeros((L,6)); _Mset=np.zeros(L,bool); _VACIO=np.zeros(6)   # mapa: tabla posicion -> ultimo patron visto",
      "    _tvis=np.zeros(L); _nvis=np.zeros(L); _perm_n=None   # novedad: ultimo paso en que se piso cada posicion, cuantas veces (lectura), permutacion del control",
      "    def _nov(p):   # novedad de sitio: tiempo sin pisar normalizado a tau_N y topado en 1 (fija en 1.0 en el control constante)",
      "        return 1.0 if nov_cte else min(1.0,float(t-_tvis[p if _perm_n is None else _perm_n[p]])/tau_N)"], 1, 'estado novedad'),
    (["        _ren={x:0 for x in _SIT}; _vistos=list(dict.fromkeys(sitios))   # largo: ultima renovacion por sitio; patrones vistos en orden"],
     ["        _ren={x:0 for x in _SIT}; _vistos=list(dict.fromkeys(sitios))   # largo: ultima renovacion por sitio; patrones vistos en orden",
      "        if nov_barajada:   # control 1: la novedad de cada sitio se lee en OTRO sitio (misma magnitud y dinamica, atribucion rota); RNG propio, no toca el del organismo",
      "            _ps=np.array(sorted(_SIT)); _perm_n=np.arange(L); _perm_n[_ps]=_ps[np.random.default_rng(seed+900000).permutation(len(_ps))]"], 1, 'permutacion control'),
    (["        return gamma_M*np.array([_bi,_bd])"],
     ["        if gamma_N:   # novedad de sitio: sesgo hacia el sitio CONOCIDO (_Mset: pisado alguna vez) que lleva mas tiempo sin pisarse",
      "            _ni=sum(disc_M**h*_nov((pos-h)%L) for h in range(1,H_M+1) if _Mset[(pos-h)%L])",
      "            _nd=sum(disc_M**h*_nov((pos+h)%L) for h in range(1,H_M+1) if _Mset[(pos+h)%L])",
      "            return gamma_M*np.array([_bi,_bd])+gamma_N*np.array([_ni,_nd])",
      "        return gamma_M*np.array([_bi,_bd])"], 1, 'sesgo'),
    (["            if usa_M and escribe_M: _Mpat[pos]=PAT_L[objs[pos]]; _Mset[pos]=True   # mapa: recuerda lo que vio aqui"],
     ["            if usa_M and escribe_M: _Mpat[pos]=PAT_L[objs[pos]]; _Mset[pos]=True   # mapa: recuerda lo que vio aqui",
      "            _tvis[pos]=t; _nvis[pos]+=1   # novedad: PISAR el sitio con el objeto presente lo pone 'visto ahora' (mismo evento que escribe el mapa; no hace falta morder)"], 1, 'pisada'),
    (["                curva=_curva,inyecciones=_iny,vistos=_vistos,comida_bin=_cbin,muertes_bin=_dbin,val_final=dict(val))   # largo"],
     ["                curva=_curva,inyecciones=_iny,vistos=_vistos,comida_bin=_cbin,muertes_bin=_dbin,val_final=dict(val),   # largo",
      "                nov_diag=dict(tvis={int(x):int(_tvis[x]) for x in _SIT},visitas={int(x):int(_nvis[x]) for x in _SIT}))   # novedad: diagnostico (clave NUEVA, no criterio)"], 1, 'diagnostico'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != '9f74ff6b5941e5a5':
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != 9f74ff6b5941e5a5")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_largo_n = mundo_largo.py (9f74ff6b5941e5a5) + NOVEDAD DE SITIO (reloj t_visita por posicion, novedad' + NL +
           'min(1,(t-t_visita)/tau_N), sesgo gamma_N por direccion con la retina vacia sobre los sitios que M conoce) + controles' + NL +
           'nov_barajada (novedad de otro sitio) y nov_cte (novedad constante). Generado por construye_novedad.py. NO editar.' + NL +
           'Con gamma_N=0 es mundo_largo exacto (identidad obligatoria; clave extra nov_diag, diagnostico)."""' + NL)
    d = os.path.join(AQUI, 'mundo_largo_n.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
