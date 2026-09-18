"""CREADOR A — construye `organismo_v13q5.py` POR ANCLAS desde `organismo_v13q4.py` (`3cc732dd2b2519cd`, solo se lee;
que a su vez viene por anclas de `organismo_v13q3.py` `aaebe073308a40c2`).

UNICA perilla nueva: `lab=False|True`. Con `lab=True` el organismo REGISTRA, sin tocar nada, la secuencia exacta de
eventos de aprendizaje de la via lenta: `(t, patron, R)` en cada mordida en que la via lenta se actualiza, mas el
paso de la sonda. Con eso, FUERA del organismo se puede repetir ESE MISMO flujo con cualquier lector — la regla
delta del tronco, minimos cuadrados exactos, gradiente, un MLP con retropropagacion — porque la actualizacion de la
via lenta esta completamente determinada por la secuencia ordenada de `(patron, R)`.

Esto es el CONTROL POSITIVO pedido: el lector de laboratorio ve **los mismos encuentros, el mismo muestreo real y
los mismos rasgos**, y no puede tocar la conducta porque no existe dentro del bucle: solo se graba.
`lab=False` (por defecto) no ejecuta ni una linea nueva dentro del bucle: identidad bit a bit obligatoria.
NO edita ningun original. Sin commits.
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, 'organismo_v13q4.py')
DEST = os.path.join(AQUI, 'organismo_v13q5.py')

src = open(ORIG, 'r', encoding='utf-8').read()
sha = hashlib.sha256(open(ORIG, 'rb').read()).hexdigest()[:16]
assert sha == '3cc732dd2b2519cd', f'origen inesperado: {sha}'

# ---- ancla 1: firma
A1 = "seleccion=None,sel_theta=0.6,sel_rho=0.05,sel_cupo=1,sel_calienta=0,sel_estad='cond'):"
B1 = "seleccion=None,sel_theta=0.6,sel_rho=0.05,sel_cupo=1,sel_calienta=0,sel_estad='cond',lab=False):"
assert src.count(A1) == 1, 'ancla 1'

# ---- ancla 2: estado
A2 = "    _e4=np.zeros(_NF); _ab4=np.ones(_NF,bool); _cand4=np.zeros(_NF,bool); _abre4=[]; _nsel4=0   # creacion_A A-1(ii)"
B2 = ("    _ev5=[]   # creacion_A (control positivo): (t, patron, R) de cada actualizacion de la via lenta; solo se graba si lab=True\n" + A2)
assert src.count(A2) == 1, 'ancla 2'

# ---- ancla 3: el registro, dentro del bloque de la via lenta y ANTES de cualquier regla
A3 = "                        _ds=dlt if puerta is None else R-_ws\n"
B3 = A3 + "                        if lab: _ev5.append((int(t),kk,float(R),float(_ds)))   # creacion_A: LECTURA pura (no cambia ningun numero)\n"
assert src.count(A3) == 1, 'ancla 3'

# ---- ancla 4: el return
A4 = "    return dict(seleccion=seleccion,"
B4 = "    return dict(lab=lab,lenta_eventos=_ev5,fase2_en=fase2_en,seleccion=seleccion,"
assert src.count(A4) == 1, 'ancla 4'

cab = ('"""organismo_v13q5 = organismo_v13q4.py (%s) + perilla `lab` (registro del flujo de encuentros de la via\n'
       'lenta: (t, patron, R, residuo) por mordida, y el paso de la sonda). Sirve para el CONTROL POSITIVO: repetir\n'
       'ESE flujo fuera del organismo con minimos cuadrados exactos, gradiente o retropropagacion.\n'
       'Generado por experimentos/creacion_A/construye_v13q5.py. NO editar a mano.\n'
       'Con lab=False es organismo_v13q4 EXACTO (y con seleccion=None, organismo_v13q3 exacto)."""\n' % sha)
open(DEST, 'w', encoding='utf-8').write(cab + src.replace(A1, B1).replace(A2, B2).replace(A3, B3).replace(A4, B4))
print(f'origen organismo_v13q4.py sha {sha}')
print(f'escrito organismo_v13q5.py  sha {hashlib.sha256(open(DEST,"rb").read()).hexdigest()[:16]}')
