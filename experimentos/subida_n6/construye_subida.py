"""Genera mundo_subida.py = mundo_muralla.py (6e515713c86d8bf4, experimentos/nivel06_rodeo_obligado) + TRES perillas
de LECTURA de la misma tabla M (el organismo v13 no cambia: ni valor(), ni la boca, ni el aprendizaje).

Diagnostico (analitico, escrito ANTES de correr nada; PREREGISTRO_n6.md §2) de por que CAMINO rodeo limpio solo 0.35:
  (a) SENAL DEBIL: CAMINO suma gamma_M*U[vecino] con U = v_A*disc_M^d. La diferencia entre el vecino bueno y el malo es
      gamma_M*v_A*disc_M^(d-1)*(1-disc_M^2) ~ 0.114*0.9^(d-1): a d=8 es 0.055, contra ruido motor N(0, 0.3) por accion.
      El campo sabe el camino, pero su voz queda enterrada en el ruido (por eso tambien atajo limpio 0.25).
  (b) LA RETINA ATRAE AL VENENO: con r_vis=1, al costear la muralla la retina ve veneno a d=1, deja de estar 'vacia',
      y el mapa se CALLA justo donde hay que rodear; Wl aprendio a acercarse a lo que ve (Rp=0.2 por acercarse a
      cualquier objeto), asi que costear la muralla es pisarla.

QUE CAMBIA (y nada mas):
  1) firma: grad=0, filtro=0, brujula=0 (las tres apagadas por defecto); y la clave de mundo prueba['cierre'] (ausente por defecto).
  2) grad=1   : con camino=1, el sesgo es gamma_M*signo(U[vecino]-U[aqui]) (sube por el campo). Misma M, misma U,
                misma gamma_M. Es la regla de Ponulak & Hopfield (2013): seguir el gradiente local de un frente de onda.
  3) filtro=1 : CON META RECORDADA (alguna celda de M con valor()>0), el veneno RECORDADO (M[x] con valor()<0) no es
                objetivo de la retina: es obstaculo. Sin meta no actua (el humo de depuracion mostro el bloqueo: una comida
                que empieza con valor<0 quedaba filtrada para siempre y el organismo no la volvia a probar). Misma tabla M,
                misma valor(); es la memoria de rechazo v9 (_rech) leida desde M en vez de desde los ultimos 20 pasos.
                Se aplica en los dos lazos de see() (tambien en el 'fallback' v9, si no el veneno vuelve a ser objetivo).
  4) brujula=1: CONTROL. El veneno recordado NO bloquea la difusion (el campo cruza la muralla): el organismo sabe
                donde esta la comida pero no que el veneno corta el paso. Es el control que puede ganarle al candidato.
  5) prueba['cierre']=c (mundo): SEGUNDA muralla de veneno ENTERA (sin hueco) en la fila relativa -c. Una sola fila de
                veneno en un toro NO lo parte (toro menos una fila = cilindro): en el bloque del 21-sep la 'vuelta del toro'
                era un camino limpio, mas corto que cruzar en 240 de 400 episodios 'rodeo' (candidato a ERR, PREREGISTRO §1).
                Con cierre el toro queda partido en dos bandas y el hueco es el UNICO cruce. Sin 'cierre' es el mundo viejo.
  _Nb: array derivado (celdas recordadas con valor<0), calculado en _campo() junto a U; se invalida con U.
  MEMORIA NUEVA PERSISTENTE: CERO.

ANCLA DE IDENTIDAD (obligatoria, identidad_subida.py): con grad=0, filtro=0, brujula=0  ->  mundo_subida.run ==
mundo_muralla.run BIT A BIT, todas las claves, en los cuatro modos viejos y en el modo muralla (camino 0 y 1, placebo).
Anclas con conteo exacto. NO editar mundo_subida.py a mano.
Uso: python experimentos/subida_n6/construye_subida.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel06_rodeo_obligado', 'mundo_muralla.py')
SHA_ORIGEN = '6e515713c86d8bf4'
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    # 1) firma: tres perillas nuevas, apagadas por defecto
    (["        ancho=None,alto=1,camino=0,placebo=0):"],
     ["        ancho=None,alto=1,camino=0,placebo=0,grad=0,filtro=0,brujula=0):   # subida_n6: grad=signo del gradiente local de U; filtro=el veneno RECORDADO no es objetivo de la retina; brujula=CONTROL (el veneno recordado no bloquea la difusion)"],
     1, 'firma'),

    # 2) cache derivado de 'veneno recordado' junto al campo
    (["    _Uc=[None]   # muralla: campo DERIVADO de M (no persiste: se invalida cuando M o el valor cambian y se recalcula por relajacion local)"],
     ["    _Uc=[None]   # muralla: campo DERIVADO de M (no persiste: se invalida cuando M o el valor cambian y se recalcula por relajacion local)",
      "    _Nb=[None,False]   # subida_n6: celdas recordadas con valor<0 y si hay META (alguna celda recordada con valor>0); DERIVADO de M, se recalcula con U; no persiste"],
     1, '_Nb'),
    (["        _U=np.full(L,-1e18); _bl=np.zeros(L,bool); _fr=[]"],
     ["        _U=np.full(L,-1e18); _bl=np.zeros(L,bool); _fr=[]; _ng=_Nb[0]=np.zeros(L,bool)   # subida_n6: _ng = veneno recordado"],
     1, '_ng'),
    (["            if _v>0: _U[int(_i)]=_v; _bl[int(_i)]=False; _fr.append(int(_i))"],
     ["            if _v>0: _U[int(_i)]=_v; _bl[int(_i)]=False; _fr.append(int(_i))",
      "        _Nb[1]=len(_fr)>0   # subida_n6: hay META recordada (sin meta, el filtro no actua: evita el bloqueo de una comida que empezo mala)"],
     1, 'meta'),
    (["            if _v<0: _bl[int(_i)]=True; _U[int(_i)]=_v"],
     ["            if _v<0: _bl[int(_i)]=(not brujula); _U[int(_i)]=_v; _ng[int(_i)]=True   # subida_n6: brujula=1 (CONTROL) el veneno recordado NO bloquea la difusion"],
     1, 'brujula'),

    # 2b) el mundo que SI parte el toro: una segunda muralla ENTERA (sin hueco). Candidato a ERR sobre el bloque del 21-sep:
    #     UNA fila de veneno en un toro NO lo parte (toro menos una fila = cilindro): la vuelta del toro es un camino limpio.
    (["            _SIT={_relm(_x,0):'B' for _x in range(_W) if _x!=_gx}; _SIT[_relm(_fx,_fy)]='A'"],
     ["            _SIT={_relm(_x,0):'B' for _x in range(_W) if _x!=_gx}; _SIT[_relm(_fx,_fy)]='A'",
      "            if _mu.get('cierre'): _SIT.update({_relm(_x,-int(_mu['cierre'])):'B' for _x in range(_W)})   # subida_n6: SEGUNDA muralla ENTERA en la fila -cierre: el toro queda PARTIDO y el hueco es el UNICO cruce"],
     1, 'cierre'),

    # 3) lectura por signo del gradiente local
    (["            return gamma_M*np.array(_b)"],
     ["            if grad: _u0=(0.0 if _U[_q]<-1e17 else float(_U[_q])); return gamma_M*np.sign(np.array(_b)-_u0)   # subida_n6: sube por el campo (signo de U[vecino]-U[aqui]); misma gamma_M",
      "            return gamma_M*np.array(_b)"],
     1, 'grad'),
    (["    q=lambda t:min(t//(T//4),3)"],
     ["    def _obst(_x):   # subida_n6: el veneno RECORDADO es obstaculo, no objetivo (misma M, misma valor())",
      "        if _Uc[0] is None: _Uc[0]=_campo()",
      "        return bool(_Nb[1] and _Nb[0][_x])   # solo con META recordada: sin meta todo lo visible sigue siendo objetivo (v9)",
      "    q=lambda t:min(t//(T//4),3)"],
     1, '_obst'),

    # 4) filtro en los DOS lazos de see()
    (["            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo"],
     ["            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo",
      "            if filtro and _obst(x): continue   # subida_n6: el veneno recordado no es objetivo"],
     1, 'filtro 1'),
    (["            for x,k in objs.items():",
      "                _d,_s=_ret(x)   # 2d"],
     ["            for x,k in objs.items():",
      "                if filtro and _obst(x): continue   # subida_n6: tampoco en el fallback v9 (si no, el veneno recordado vuelve a ser objetivo)",
      "                _d,_s=_ret(x)   # 2d"],
     1, 'filtro 2'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN (mundo_muralla.py) sha {h16(ORIGEN)} != {SHA_ORIGEN}")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_subida = mundo_muralla.py (' + SHA_ORIGEN + ') + tres perillas de LECTURA de la misma tabla M:' + NL +
           'grad (signo del gradiente local del campo), filtro (el veneno recordado no es objetivo de la retina) y' + NL +
           'brujula (CONTROL: el veneno recordado no bloquea la difusion). El organismo v13 NO cambia. Memoria nueva persistente: cero.' + NL +
           'Generado por experimentos/subida_n6/construye_subida.py. ANCLA: con grad=filtro=brujula=0 es mundo_muralla BIT A BIT' + NL +
           '(identidad_subida.py). NO editar."""' + NL)
    d = os.path.join(AQUI, 'mundo_subida.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  origen {os.path.relpath(ORIGEN, RAIZ)} {h16(ORIGEN)}")
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
