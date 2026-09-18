"""MINI-EQUIPO 3 (sala de enjambre) -- construye `organismo_g3.py` POR ANCLAS desde
`experimentos/creacion_A/organismo_v13q5.py` (`fae9c32b146fdbb4`, SOLO SE LEE).

MISION DEL EQUIPO (no opcional, EQUIPO.md regla 13): llegar a la AGI por este camino -- un organismo minimo con
reglas locales (sin retropropagacion en tiempo de ejecucion), que sube la escalera del brief con cada peldano
preregistrado, medido con controles y replicado. El metodo manda sobre el como.

MECANISMO M3 -- MEMORIA DE UN GOLPE POR COMBINACION (jefe de investigacion, mini-equipo 3):
cada una de las 15 celdas de DOS canales (todos los pares no ordenados de los 6 pixeles binarios de la retina)
tiene 4 casillas de valor, una por combinacion (P_i,P_j) in {0,1}x{0,1}. En cada mordida, CADA celda actualiza
SU casilla correspondiente: si nunca se habia visto esa combinacion, escribe R DE UN GOLPE (un solo ensayo, sin
tasa); si ya se habia visto, promedia con `mem_alfa` (brazo 'combi') o no hace nada (brazo 'combi1', binario
literal: se queda con el primer valor para siempre). Cada celda lleva tambien un error propio E_c (media movil
de (R-prediccion)^2); la celda GANADORA (la que lee la boca) es la de menor error, `argmin_c E_c`. Una
combinacion nunca vista se ABSTIENE devolviendo 0.0 en vez de inventar un valor.

Fundamento (ver PREREGISTRO_g3.md para las citas completas): Bittner, Milstein, Grienberger, Romani & Magee 2017
(BTSP: una sola coincidencia entre traza y meseta escribe un campo de lugar de novo, en UN ensayo, sin repeticion
hebbiana) y Milstein et al. 2024 (BTSP con sinapsis BINARIAS = memoria direccionable por contenido, aprendizaje
de una pasada); Hernandez-Cano, Matsumoto, Ping & Imani 2021 (OnlineHD: prototipos por clase en UNA pasada). La
traduccion es exacta y diminuta: una celda que mira 2 pixeles BINARIOS solo tiene 4 entradas posibles, asi que su
"traza de elegibilidad + meseta" se reduce a una casilla por combinacion. El tercer factor es la mordida misma.

UNICA perilla nueva: `memoria=None|'combi'|'combi1'` (+ `mem_alfa=0.3`, `mem_rho=0.02`, sin efecto si memoria=None).
Con `memoria=None` (por defecto) es organismo_v13q5.py EXACTO: identidad bit a bit obligatoria (identidad_g3.py).
NO edita el original. Sin commits. Sin multiprocessing.Pool. Trabaja SOLO en experimentos/enjambre/grupo3/.
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))                                    # experimentos/enjambre/grupo3/
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))                       # bundle/
ORIG = os.path.join(RAIZ, 'experimentos', 'creacion_A', 'organismo_v13q5.py')
DEST = os.path.join(AQUI, 'organismo_g3.py')

src = open(ORIG, 'r', encoding='utf-8').read()
sha = hashlib.sha256(open(ORIG, 'rb').read()).hexdigest()[:16]
assert sha == 'fae9c32b146fdbb4', f'origen inesperado: {sha}'

# ---- ancla 1: firma -- anade la perilla `memoria` (+ mem_alfa, mem_rho) al final de la firma de run()
A1 = "sel_estad='cond',lab=False):"
B1 = "sel_estad='cond',lab=False,memoria=None,mem_alfa=0.3,mem_rho=0.02):"
assert src.count(A1) == 1, 'ancla 1'

# ---- ancla 2: estado -- las 15 celdas de dos canales, ANTES de `Ws=np.zeros(_NF)` (que _IJ/_R15 aun no existen aqui)
A2 = "    Ws=np.zeros(_NF)   # 3d: vector con signo de la via lenta; solo se mueve/lee si regla_lenta=='delta_signo'"
B2 = ('    if memoria not in (None,\'combi\',\'combi1\'): raise ValueError(f"memoria={memoria!r}")   # M3: perilla mal escrita no cae en silencio\n'
      '    _PAR=[(i,j) for i in range(6) for j in range(i+1,6)]   # M3: las 15 celdas de dos canales (pares de pixeles binarios)\n'
      '    _MM=np.zeros((15,4))   # M3: valor escrito por celda x combinacion (P_i,P_j) in 00,01,10,11\n'
      '    _MN=np.zeros((15,4))   # M3: veces visitada esa celda x combinacion (0 = abstencion explicita)\n'
      '    _ME=np.full(15,1e9)   # M3: error propio de cada celda (media movil de (R-prediccion)^2); gana la de menor error\n'
      '    _MG=0   # M3: celda ganadora vigente (indice en _PAR); la que lee la boca\n'
      + A2)
assert src.count(A2) == 1, 'ancla 2'

# ---- ancla 3: lectura -- dentro de `def lenta(P):`, ANTES de la linea original (que queda intacta, memoria=None no la toca)
A3 = "_ph=phi(P); return float(Ws@_ph) if regla_lenta=='delta_signo' else float((Wps-Wns)@_ph)"
B3 = ("if memoria is not None: _i,_j=_PAR[_MG]; _c=int(P[_i])*2+int(P[_j]); return float(_MM[_MG,_c]) if _MN[_MG,_c]>0 else 0.0   # M3: lectura de la celda ganadora, abstencion explicita\n"
      "        " + A3)
assert src.count(A3) == 1, 'ancla 3'

# ---- ancla 4: regla -- rama nueva ANTES de `if seleccion is not None:` (que pasa a `elif`); vive dentro de `if eta_s:`,
#      igual que las otras reglas de la via lenta (asi entra con los mismos knobs del tronco v14.1 sin tocar el resto)
A4 = "if seleccion is not None:   # creacion_A A-1(ii): elegibilidad por rasgo, competencia entre candidatos, y la via lenta aprende SOLO lo abierto"
B4 = ("if memoria is not None:   # M3: memoria de un golpe por combinacion (BTSP; Milstein 2024; OnlineHD): las 15 celdas escriben en cada mordida, ninguna tasa\n"
      "                            for _c5m in range(15):\n"
      "                                _i5m,_j5m=_PAR[_c5m]; _dir5m=int(P_[kk][_i5m])*2+int(P_[kk][_j5m])\n"
      "                                _p5m=float(_MM[_c5m,_dir5m]) if _MN[_c5m,_dir5m]>0 else 0.0\n"
      "                                _d5m=R-_p5m; _prim5m=bool(_MN[_c5m].sum()==0)   # primera vez que ESTA celda ve cualquier combinacion\n"
      "                                _ME[_c5m]=(_d5m*_d5m) if _prim5m else (1-mem_rho)*_ME[_c5m]+mem_rho*(_d5m*_d5m)\n"
      "                                if _MN[_c5m,_dir5m]==0: _MM[_c5m,_dir5m]=R   # DE UN GOLPE: la primera vez que se ve ESA combinacion\n"
      "                                elif memoria=='combi': _MM[_c5m,_dir5m]+=mem_alfa*(R-_MM[_c5m,_dir5m])   # 'combi1': no hace nada (binario literal, Milstein 2024)\n"
      "                                _MN[_c5m,_dir5m]+=1\n"
      "                            _MG=int(np.argmin(_ME))\n"
      "                        elif seleccion is not None:   # creacion_A A-1(ii): elegibilidad por rasgo, competencia entre candidatos, y la via lenta aprende SOLO lo abierto")
assert src.count(A4) == 1, 'ancla 4'

# ---- ancla 5: return -- lecturas nuevas (mem_ganadora, mem_tabla, mem_vistas), lectura pura, no cambia ningun numero previo
A5 = "return dict(lab=lab,lenta_eventos=_ev5,"
B5 = "return dict(lab=lab,lenta_eventos=_ev5,mem_ganadora=list(_PAR[_MG]),mem_tabla=[[round(float(x),3) for x in f] for f in _MM],mem_vistas=int((_MN>0).sum()),"
assert src.count(A5) == 1, 'ancla 5'

cab = ('"""organismo_g3 = organismo_v13q5.py (%s) + perilla `memoria` (MINI-EQUIPO 3 de la sala de enjambre;\n'
       'mecanismo M3 -- MEMORIA DE UN GOLPE POR COMBINACION): cada una de las 15 celdas de DOS canales (todos los\n'
       'pares de los 6 pixeles binarios de la retina) escribe, DE UN GOLPE en la primera mordida que ve esa\n'
       'combinacion de 2 bits, el valor R que recibio (BTSP, Bittner et al. 2017; Milstein et al. 2024; OnlineHD,\n'
       'Hernandez-Cano et al. 2021); sin repeticion, sin gradiente, sin tasa de aprendizaje. Gana y lee la boca la\n'
       'celda de MENOR error propio (media movil de (R-prediccion)^2); una combinacion nunca vista se ABSTIENE\n'
       'devolviendo 0.0. `memoria=\'combi\'` promedia con `mem_alfa` tras la primera escritura; `memoria=\'combi1\'`\n'
       'se queda con el PRIMER valor, para siempre (binario literal, Milstein 2024).\n'
       'Generado por experimentos/enjambre/grupo3/construye_grupo3.py. NO editar a mano.\n'
       'Con memoria=None es organismo_v13q5.py EXACTO (identidad obligatoria: identidad_g3.py)."""\n' % sha)

out = cab + src.replace(A1, B1).replace(A2, B2).replace(A3, B3).replace(A4, B4).replace(A5, B5)
open(DEST, 'w', encoding='utf-8').write(out)
print(f'origen organismo_v13q5.py sha {sha}')
print(f'escrito organismo_g3.py    sha {hashlib.sha256(open(DEST,"rb").read()).hexdigest()[:16]}')
