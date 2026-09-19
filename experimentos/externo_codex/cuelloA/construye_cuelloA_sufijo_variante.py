"""Construye por ANCLAS el instrumento del cuello A desde organismo_familias_b4b.py.

MISION: avanzar hacia AGI por reglas locales comprobables. Este instrumento cambia UNA cosa: cuando se enciende
`memoria_variante`, la direccion de la tabla de pares incluye la firma local de los pixeles variables. Apagada,
la ruta de direccion es la de b4b y no usa RNG. No editar el destino a mano.
"""
import hashlib
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias', 'organismo_familias_b4b.py')
DESTINO = os.path.join(AQUI, 'organismo_cuelloA_sufijo_variante.py')
SHA_ORIGEN = 'b3dd1d7e66a2d147'


def h16(ruta):
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()[:16]


def sustituye(texto, ancla, reemplazo, etiqueta, veces=1):
    n = texto.count(ancla)
    if n != veces:
        raise SystemExit(f'ANCLA {etiqueta!r}: aparece {n}; se esperaba {veces}. Abortado sin escribir.')
    return texto.replace(ancla, reemplazo)


FIRMA = ',voraz=0.0,par_herm=None):'
VALIDA = ('    if memoria_pares not in (None,\'relevo\'): raise ValueError(f"memoria_pares={memoria_pares!r}")'
          '   # v15f: perilla mal escrita no cae en silencio\n')
TABLA_INI = ('    _PARv=[(i,j) for i in range(_D) for j in range(i+1,_D)]; _NP=len(_PARv)   # v15f/b3: C(_D,2) celdas = pares de pixeles (con _D=6 son 15: v15f EXACTO)\n'
             '    _MMv=np.zeros((_NP,4)); _MNv=np.zeros((_NP,4)); _MEv=np.full(_NP,1e9); _MGv=0   # v15f: R CRUDO por casilla, visitas, error propio por celda, ganadora\n')
BIN = ('    def _bin4(_g,_P):   # B4: la casilla (2 bits) que el par ganador _g le asigna al patron _P -- la RESOLUCION de la referencia\n'
       '        _i4,_j4=_PARv[_g]; return int(_P[_i4])*2+int(_P[_j4])\n')
LECTURA = ('    def _tabla_v15f(P):   # v15f: (valor, visto) de la casilla de la celda ganadora\n'
           '        _i,_j=_PARv[_MGv]; _c=int(P[_i])*2+int(P[_j])\n'
           '        return (float(_MMv[_MGv,_c]), True) if _MNv[_MGv,_c]>0 else (0.0, False)\n')
DIRECCION_ESCRITURA = '_dv=int(_Pv[_iv])*2+int(_Pv[_jv])'
RETORNO = '    return dict(voraz=float(voraz),par_herm='

CABECERA = '''"""Instrumento CUELLO A: sufijo local de variante.

Derivado por anclas de organismo_familias_b4b.py (b3dd1d7e66a2d147). UNA perilla nueva,
`memoria_variante=0` por defecto. Con 1, cada celda de pares escribe/lee R cruda en
(bin del par, firma de los ultimos fam_nvar pixeles). No cambia emisor, canal, boca,
ganadora, regla de error ni RNG. Con 0, la direccion es el bin literal de b4b.
Generado por construye_cuelloA_sufijo_variante.py; no editar a mano.
"""
'''


def main():
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f'ORIGEN cambio: {h16(ORIGEN)}; se esperaba {SHA_ORIGEN}. Abortado sin escribir.')
    texto = open(ORIGEN, encoding='utf-8').read()
    texto = CABECERA + texto
    texto = sustituye(texto, FIRMA, ',voraz=0.0,par_herm=None,memoria_variante=0):', 'firma run')
    texto = sustituye(texto, VALIDA, VALIDA +
                       '    if memoria_variante not in (0,1): raise ValueError(f"memoria_variante={memoria_variante!r}: se espera 0 o 1")\n',
                       'validacion perilla')
    nueva_ini = '''    _PARv=[(i,j) for i in range(_D) for j in range(i+1,_D)]; _NP=len(_PARv)   # v15f/b3: C(_D,2) celdas = pares de pixeles (con _D=6 son 15: v15f EXACTO)
    _NV=0
    if memoria_variante:
        _NV=int(fam_nvar)
        if _NV<1 or _NV>_D: raise ValueError(f"fam_nvar={fam_nvar!r}: se espera 1..{_D} al usar memoria_variante")
    _NC=4*(1<<_NV) if memoria_variante else 4
    _MMv=np.zeros((_NP,_NC)); _MNv=np.zeros((_NP,_NC)); _MEv=np.full(_NP,1e9); _MGv=0   # CUELLO A: R crudo por direccion local; apagado conserva 4 casillas
'''
    texto = sustituye(texto, TABLA_INI, nueva_ini, 'tabla y subcasillas')
    nueva_bin = BIN + '''    def _direccion_variante(_g,_P):
        _i4,_j4=_PARv[_g]; _base=int(_P[_i4])*2+int(_P[_j4])
        if not memoria_variante: return _base
        _suf=0
        for _q4 in range(_D-_NV,_D): _suf=_suf*2+int(_P[_q4])
        return _base*(1<<_NV)+_suf
'''
    texto = sustituye(texto, BIN, nueva_bin, 'direccion local de variante')
    nueva_lectura = '''    def _tabla_v15f(P):   # CUELLO A: misma lectura v15f, con direccion de variante solo al encenderse
        _c=_direccion_variante(_MGv,P)
        return (float(_MMv[_MGv,_c]), True) if _MNv[_MGv,_c]>0 else (0.0, False)
'''
    texto = sustituye(texto, LECTURA, nueva_lectura, 'lectura tabla')
    texto = sustituye(texto, DIRECCION_ESCRITURA, '_dv=_direccion_variante(_cv,_Pv)',
                       'escritura tabla (mensaje y mordida)', veces=2)
    texto = sustituye(texto, RETORNO,
                       '    return dict(memoria_variante=int(memoria_variante),memoria_slots=int(_NC),voraz=float(voraz),par_herm=',
                       'salida')
    if texto.count('def _direccion_variante') != 1 or texto.count('_dv=_direccion_variante(_cv,_Pv)') != 2:
        raise SystemExit('Postcondicion de anclas no satisfecha. Abortado sin escribir.')
    compile(texto, DESTINO, 'exec')
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as salida:
        salida.write(texto)
    print('ANCLAS OK: 7 sustituciones exactas; mensaje y mordida comparten direccion local.')
    print(f'origen  {SHA_ORIGEN}')
    print(f'destino {h16(DESTINO)}  {os.path.relpath(DESTINO, RAIZ)}')


if __name__ == '__main__':
    main()
