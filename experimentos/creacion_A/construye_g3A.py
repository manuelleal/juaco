"""CREADOR A — construye `organismo_g3A.py` POR ANCLAS desde `experimentos/enjambre/grupo3/organismo_g3.py`
(`91eb167023cb37b7`, del grupo 3; SOLO se lee, no se toca).

Dos perillas, las dos apagadas por defecto (identidad obligatoria con `organismo_g3`):

  `mem_apriori=True`    LECTURA pura: exporta, EN LA SONDA, el vector de errores `_ME`, la celda ganadora y
                        **cuantas celdas empatan en el minimo**. El informe del enjambre mide la ganadora al final
                        de T; el criterio del bloque 3 se juega en la sonda, y hay que poder verlo.

  `mem_desempate='azar'` CONTROL DE RIGGING. `organismo_g3` elige la celda con `int(np.argmin(_ME))`: ante un empate
                        gana el indice MAS BAJO, y el indice 0 de `_PAR` **es justamente (0,1)**, la respuesta
                        correcta. Con `'azar'` el empate se rompe con un RNG propio (no toca el del organismo).
                        Este control no es teorico: un desempate por indice ya me colo un 17/20 falso (PUENTE §A13),
                        y el propio informe del enjambre reporta el empate (0,1)/(1,4) en la semilla 3.

NO edita ningun original. Sin commits.
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIG = os.path.join(RAIZ, 'experimentos', 'enjambre', 'grupo3', 'organismo_g3.py')
DEST = os.path.join(AQUI, 'organismo_g3A.py')

src = open(ORIG, 'r', encoding='utf-8').read()
sha = hashlib.sha256(open(ORIG, 'rb').read()).hexdigest()[:16]


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


# ---- ancla 1: firma
A1 = "lab=False,memoria=None,mem_alfa=0.3,mem_rho=0.02):"
B1 = "lab=False,memoria=None,mem_alfa=0.3,mem_rho=0.02,mem_apriori=False,mem_desempate='indice'):"
out = sust(src, A1, B1, etq='firma de run')

# ---- ancla 2: estado (el RNG propio del desempate y el hueco de la sonda)
A2 = "    _ME=np.full(15,1e9)   # M3: error propio de cada celda (media movil de (R-prediccion)^2); gana la de menor error"
B2 = (A2 + "\n"
      "    if mem_desempate not in ('indice','azar'): raise ValueError(f\"mem_desempate={mem_desempate!r}\")   # creacion_A: un knob mal escrito no cae en silencio\n"
      "    _rngA=np.random.default_rng(seed+1300000)   # creacion_A: RNG PROPIO del desempate (no toca el del organismo)\n"
      "    _memA=None   # creacion_A: lectura de la sonda (errores, ganadora y empates)")
out = sust(out, A2, B2, etq='estado de creacion_A')

# ---- ancla 3: el desempate
A3 = "                            _MG=int(np.argmin(_ME))"
B3 = ("                            if mem_desempate=='azar':   # creacion_A: control de rigging (el indice 0 de _PAR es (0,1))\n"
      "                                _mn5=float(_ME.min()); _emp5=[int(_x) for _x in np.where(_ME<=_mn5+1e-12)[0]]\n"
      "                                _MG=int(_emp5[int(_rngA.integers(len(_emp5)))])\n"
      "                            else: _MG=int(np.argmin(_ME))")
out = sust(out, A3, B3, etq='desempate')

# ---- ancla 4: la sonda (lectura pura, junto a las demas sondas a priori)
A4 = "            Ws_apriori=[float(_x) for _x in _wvec()]   # 3d: lectura pura, no cambia ningun numero"
B4 = (A4 + "\n"
      "            if mem_apriori and memoria is not None:   # creacion_A: LECTURA pura de la memoria EN LA SONDA\n"
      "                _mn6=float(_ME.min()); _emp6=[int(_x) for _x in np.where(_ME<=_mn6+1e-12)[0]]\n"
      "                _memA=dict(ME=[float(_x) for _x in _ME], ganadora=list(_PAR[_MG]), n_empate=len(_emp6),\n"
      "                           empatadas=[list(_PAR[_x]) for _x in _emp6], vistas=int((_MN>0).sum()),\n"
      "                           tabla=[[float(_x) for _x in _f] for _f in _MM],\n"
      "                           cobertura_ganadora=int((_MN[_MG]>0).sum()))")
out = sust(out, A4, B4, etq='sonda')

# ---- ancla 5: el return
A5 = "    return dict(lab=lab,"
B5 = "    return dict(mem_apriori=_memA,mem_desempate=mem_desempate,lab=lab,"
out = sust(out, A5, B5, etq='return')

cab = (f'"""organismo_g3A = experimentos/enjambre/grupo3/organismo_g3.py ({sha}, del grupo 3; solo se leyo) + dos\n'
       f'perillas del CREADOR A, apagadas por defecto: `mem_apriori` (LECTURA de la memoria EN LA SONDA: errores,\n'
       f'ganadora, cuantas empatan) y `mem_desempate=\'azar\'` (CONTROL DE RIGGING: el indice 0 de _PAR es (0,1)).\n'
       f'Con las dos apagadas es organismo_g3 EXACTO (identidad obligatoria: identidad_g3A.py).\n'
       f'Generado por experimentos/creacion_A/construye_g3A.py. NO editar a mano."""\n')
open(DEST, 'w', encoding='utf-8').write(cab + out)
print(f'origen organismo_g3.py sha {sha}')
print(f'escrito organismo_g3A.py sha {hashlib.sha256(open(DEST,"rb").read()).hexdigest()[:16]}')
