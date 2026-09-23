"""NIVEL 5 -- SUBIDA (equipo n5, 23-sep-2026): **V-5 = B-5 trasplantado a la tabla de referencia**.
Construye POR ANCLAS, sin editar ningun original:
  organismo_familias_v5.py  <-  experimentos/nivel05_familia_variante_BAv/organismo_familias_bav.py (2dca0a3e239481f0)
  corre_v5.py               <-  experimentos/nivel05_familia_variante_BAv/corre_familias_bav.py   (4453754a9921e349)

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy: que el
mensaje refiera a la FAMILIA **Y** a la VARIANTE con LA MISMA tabla (BAR-T <= 5 Y dist(PAR) >= 15).

EL MECANISMO (preregistro de C, junta_20260921/C/PROPUESTA.md 6, "V-5"; aqui se escribe por primera vez):
  `v5` (0): con 1, cada ESCRITURA en la tabla de pares (la del MENSAJE y la de la EXPERIENCIA PROPIA) mira la
       casilla de la FAMILIA (la direccion de siempre: el bin de 2 bits del par). Si esa casilla ya consta y su
       valor CONTRADICE en signo a la R que llega (|valor| > 0.2, el umbral de B-5 en el tronco), la casilla
       NO se sobrescribe: SE PARTE -- la R va a una SUBCASILLA de variante (bin, firma de los 3 px de variante
       de la retina PRESENTE) y la de la familia conserva su valor. Si la subcasilla ya existe, las escrituras
       de ese (bin, firma) van a ella. Mientras la variante se porte como su familia no se crea nada.
       LECTURA: si la subcasilla de la retina presente existe, se lee ella; si no, la de la familia.
  Por que ataca la colision medida (REGISTRO 5829; B 37/37): con BA-v el mensaje "T1v2 es comida" y el primer
  bocado de T1v2 SOBRESCRIBEN con +1 las casillas que la hermana T1v0 comparte (todas las de FORMA y una de
  VARIANTE), y la hermana hereda el valor. Con `v5` esas casillas guardaban -3 (la familia T1 es veneno):
  hay contradiccion, se parten, y la hermana sigue leyendo -3 mientras T1v2 lee +1.
MEMORIA NUEVA (declarada, no es cero): una tabla de subcasillas 66 x 32 con sus visitas -- la MISMA forma que
el sufijo del bloque 6 --, poblada SOLO por conflicto de signo. El numero de subcasillas ocupadas sale en
cada corrida (`v5_sub`). Sin rng nuevo, sin gradiente, sin supervisor: el disparo es local (la casilla y la R).
DESVIOS DECLARADOS respecto de B-5 del tronco: (1) no se exige "retina distinta" por separado (la subcasilla
ya la direcciona la firma de la retina presente; guardar la procedencia seria memoria nueva); (2) R = 0 no
dispara (en este mundo no hay neutros: n_neu = 0); (3) la firma usa los px de variante declarados por el
mundo (fam_nvar = 3, los ultimos): el mismo supuesto estructural que el sufijo del bloque 6.

CERO LINEAS NUEVAS con v5 = 0: el organismo es organismo_familias_bav BIT A BIT (arnes identidad_v5.py).

Uso:  python experimentos/subida_n5/construye_v5.py   (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
NBAV = os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv')

SHA_BAV = '2dca0a3e239481f0'          # organismo_familias_bav.py (identidad 61/61): EL ORIGEN del instrumento
SHA_BAV_RUNNER = '4453754a9921e349'   # corre_familias_bav.py: EL ORIGEN del runner
SHA_BAV_ARNES = 'cf7655b379014a55'    # identidad_familias_bav.py (se IMPORTA en el arnes nuevo)
SHA_V14 = 'feefc88b1fd8d434'          # EL TRONCO (congelado)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado (no se escribe nada).")
    return open(p, encoding='utf-8').read()


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


# =============================================================================== EL ORGANISMO
CAB_ORG = '''"""organismo_familias_v5 = organismo_familias_bav.py (nivel 5, BA-v + control `baraja_msg`, 2dca0a3e239481f0)
+ V-5, inerte por defecto:
  `v5` (0): con 1, B-5 TRASPLANTADO A LA TABLA DE REFERENCIA. Toda escritura (mensaje y experiencia propia) que
            CONTRADICE en signo a una casilla de familia que ya consta (|valor| > 0.2) no la sobrescribe: la parte
            en una SUBCASILLA de variante (bin, firma de los px de variante de la retina presente). La lectura
            usa la subcasilla si existe y, si no, la de la familia. Memoria nueva: 66 x 32 subcasillas pobladas
            SOLO por conflicto. Sin rng nuevo.
  Diagnosticos (no deciden nada): `v5_split_msg`, `v5_split_mord`, `v5_t1` (primer parto), `v5_sub` (subcasillas
            ocupadas al final), `v5_lee_par` (lo que lee la tabla para la hermana fija en el paso de la entrega,
            DESPUES de escribir el mensaje: [valor, habla]).
ANCLA DE IDENTIDAD: con v5=0 es organismo_familias_bav BIT A BIT y por su cadena ba, a1, b6, b5, b4b,
organismo_familias, organismo_v14 (TRONCO) y organismo_v15f_on.
Arnes: experimentos/subida_n5/identidad_v5.py.  Generado por construye_v5.py. NO editar a mano."""
'''

O_FIRMA = ",conj_tipo=0,baraja_msg=0):"
O_BARAJA = ("        _BMv=np.stack([_bmg.permutation(_NCv) for _ in range(_NP)])   # una permutacion de las casillas "
            "POR CELDA: misma R, misma cantidad, direccion destruida\n")
O_V5_DEF = (
    '    if (not isinstance(v5,int)) or isinstance(v5,bool) or v5 not in (0,1): raise ValueError(f"v5={v5!r}: se espera 0 (apagado) o 1 (V-5: la casilla de familia se PARTE cuando una escritura la contradice)")   # V-5: perilla mal escrita no cae en silencio\n'
    '    _V5=int(v5) if memoria_pares is not None else 0   # V-5: sin tabla no hay nada que partir (INERTE)\n'
    '    if _V5 and _MVv: raise ValueError("v5=1 y memoria_variante=1: el sufijo ya direcciona TODAS las casillas por variante; V-5 lo hace solo cuando hay conflicto. Se pide uno.")   # V-5\n'
    '    if _V5 and not (1<=_NVA<_D): raise ValueError(f"v5=1 con fam_nvar={fam_nvar!r}: la firma de variante necesita 1 <= fam_nvar < {_D}")   # V-5\n'
    '    _MMs=np.zeros((_NP,(4<<_NVA) if _V5 else 1)); _MNs=np.zeros_like(_MMs); _S5=[0,0,None]; _v5lp=None   # V-5: SUBCASILLAS (bin, firma) por celda, visitas; partos por mensaje / por bocado; paso del primer parto\n'
    '    def _sub5(_c,_P):   # V-5: la subcasilla de VARIANTE de la casilla de familia _c para la retina PRESENTE _P (sin estado, sin rng)\n'
    '        _s5=0\n'
    '        for _q5 in range(_D-_NVA,_D): _s5=_s5*2+int(_P[_q5])\n'
    '        return _c*(1<<_NVA)+_s5\n'
    '    def _lee5(_g,_c,_P):   # V-5: (valor, consta) -- la subcasilla si existe; si no, la casilla de la familia\n'
    '        _s5=_sub5(_c,_P)\n'
    '        if _MNs[_g,_s5]>0: return (float(_MMs[_g,_s5]), True)\n'
    '        return (float(_MMv[_g,_c]), True) if _MNv[_g,_c]>0 else (0.0, False)\n'
    '    def _esc5(_g,_c,_P,_R,_m):   # V-5: LA ESCRITURA. _m=1 mensaje, 0 experiencia propia\n'
    '        _s5=_sub5(_c,_P)\n'
    '        if _MNs[_g,_s5]>0:   # la variante ya se partio: sus consecuencias van a SU subcasilla\n'
    '            if mem_alfa>=1.0: _MMs[_g,_s5]=_R\n'
    '            else: _MMs[_g,_s5]+=mem_alfa*(_R-_MMs[_g,_s5])\n'
    '            _MNs[_g,_s5]+=1; return\n'
    '        if _MNv[_g,_c]>0 and float(_MMv[_g,_c])*_R<0 and abs(float(_MMv[_g,_c]))>0.2:   # CONTRADICE a la familia: SE PARTE (B-5 en la tabla)\n'
    '            _MMs[_g,_s5]=_R; _MNs[_g,_s5]=1; _S5[0 if _m else 1]+=1\n'
    '            if _S5[2] is None: _S5[2]=int(t)\n'
    '            return\n'
    '        if _MNv[_g,_c]==0 or mem_alfa>=1.0: _MMv[_g,_c]=_R   # sin conflicto: la escritura de siempre\n'
    '        else: _MMv[_g,_c]+=mem_alfa*(_R-_MMv[_g,_c])\n'
    '        _MNv[_g,_c]+=1\n')

O_LEE_TIPO = "            if _MNv[_g7,_c7]>0: _s7+=float(_MMv[_g7,_c7]); _n7+=1\n"
N_LEE_TIPO = ("            if _V5:   # V-5: la subcasilla de variante si existe\n"
              "                _v5a,_v5b=_lee5(_g7,_c7,P)\n"
              "                if _v5b: _s7+=_v5a; _n7+=1\n"
              "            elif _MNv[_g7,_c7]>0: _s7+=float(_MMv[_g7,_c7]); _n7+=1\n")
O_LEE_K1 = "            return (float(_MMv[_MGv,_c]), True) if _MNv[_MGv,_c]>0 else (0.0, False)\n"
N_LEE_K1 = ("            if _V5: return _lee5(_MGv,_c,P)   # V-5\n" + O_LEE_K1)
O_LEE_K = "            if _MNv[_g5,_c]>0: _sv+=float(_MMv[_g5,_c]); _nv+=1\n"
N_LEE_K = ("            if _V5:   # V-5\n"
           "                _v5a,_v5b=_lee5(_g5,_c,P)\n"
           "                if _v5b: _sv+=_v5a; _nv+=1\n"
           "            elif _MNv[_g5,_c]>0: _sv+=float(_MMv[_g5,_c]); _nv+=1\n")

O_ESC_MSG = ("                        _pv=float(_MMv[_cv,_dv]) if _MNv[_cv,_dv]>0 else 0.0   # lo que ESA casilla habria dicho (0.0 si no se vio: M3)\n"
             "                        _erv=_R4-_pv; _prv=bool(_MNv[_cv].sum()==0)\n")
N_ESC_MSG = ("                        _pv=float(_MMv[_cv,_dv]) if _MNv[_cv,_dv]>0 else 0.0   # lo que ESA casilla habria dicho (0.0 si no se vio: M3)\n"
             "                        if _V5: _pv=_lee5(_cv,_dv,_Pv)[0]   # V-5: lo que la tabla habria LEIDO (subcasilla si existe)\n"
             "                        _erv=_R4-_pv; _prv=bool(_MNv[_cv].sum()==0)\n")
O_ESC_MSG2 = ("                        if _MNv[_cv,_dv]==0 or mem_alfa>=1.0: _MMv[_cv,_dv]=_R4   # SOBRESCRITURA: la casilla sigue a la ultima recompensa\n"
              "                        else: _MMv[_cv,_dv]+=mem_alfa*(_R4-_MMv[_cv,_dv])\n"
              "                        _MNv[_cv,_dv]+=1\n")
N_ESC_MSG2 = ("                        if _V5: _esc5(_cv,_dv,_Pv,_R4,1)   # V-5: el MENSAJE que contradice a la familia PARTE la casilla\n"
              "                        else:\n"
              "                            if _MNv[_cv,_dv]==0 or mem_alfa>=1.0: _MMv[_cv,_dv]=_R4   # SOBRESCRITURA: la casilla sigue a la ultima recompensa\n"
              "                            else: _MMv[_cv,_dv]+=mem_alfa*(_R4-_MMv[_cv,_dv])\n"
              "                            _MNv[_cv,_dv]+=1\n")
O_ESC_MOR = ("                                _pv=float(_MMv[_cv,_dv]) if _MNv[_cv,_dv]>0 else 0.0   # lo que ESA casilla habria dicho (0.0 si no se vio: M3)\n"
             "                                _erv=R-_pv; _prv=bool(_MNv[_cv].sum()==0)\n")
N_ESC_MOR = ("                                _pv=float(_MMv[_cv,_dv]) if _MNv[_cv,_dv]>0 else 0.0   # lo que ESA casilla habria dicho (0.0 si no se vio: M3)\n"
             "                                if _V5: _pv=_lee5(_cv,_dv,_Pv)[0]   # V-5\n"
             "                                _erv=R-_pv; _prv=bool(_MNv[_cv].sum()==0)\n")
O_ESC_MOR2 = ("                                if _MNv[_cv,_dv]==0 or mem_alfa>=1.0: _MMv[_cv,_dv]=R   # SOBRESCRITURA: la casilla sigue a la ultima recompensa\n"
              "                                else: _MMv[_cv,_dv]+=mem_alfa*(R-_MMv[_cv,_dv])\n"
              "                                _MNv[_cv,_dv]+=1\n")
N_ESC_MOR2 = ("                                if _V5: _esc5(_cv,_dv,_Pv,R,0)   # V-5: la EXPERIENCIA PROPIA que contradice a la familia PARTE la casilla\n"
              "                                else:\n"
              "                                    if _MNv[_cv,_dv]==0 or mem_alfa>=1.0: _MMv[_cv,_dv]=R   # SOBRESCRITURA: la casilla sigue a la ultima recompensa\n"
              "                                    else: _MMv[_cv,_dv]+=mem_alfa*(R-_MMv[_cv,_dv])\n"
              "                                    _MNv[_cv,_dv]+=1\n")
O_C4LP = "            _c4lp=([round(float(_tabla_dos(PAT[_c4r])[0]),4)"
N_C4LP = ("            if memoria_pares is not None and _MF and _FA.get('par_fijo') is not None: _v5lp=[round(float(_tabla_v15f(PAT[_FA['par_fijo']])[0]),4),bool(_tabla_v15f(PAT[_FA['par_fijo']])[1])]   # V-5: DIAGNOSTICO -- lo que la tabla lee para la HERMANA fija justo despues del mensaje (pura lectura: sin estado ni rng)\n"
          + O_C4LP)
O_RET = "    return dict(baraja_msg=int(baraja_msg),"
N_RET = ("    return dict(v5=int(v5),v5_split_msg=int(_S5[0]),v5_split_mord=int(_S5[1]),v5_t1=_S5[2],"
         "v5_sub=(int((_MNs>0).sum()) if _V5 else None),v5_lee_par=_v5lp,baraja_msg=int(baraja_msg),")


def construye_organismo():
    t0 = origen(os.path.join(NBAV, 'organismo_familias_bav.py'), SHA_BAV)
    t = CAB_ORG + t0
    t = sust(t, O_FIRMA, O_FIRMA[:-2] + ",v5=0):", etiqueta='firma de run')
    t = sust(t, O_BARAJA, O_BARAJA + O_V5_DEF, etiqueta='definicion de V-5 (tras la baraja)')
    t = sust(t, O_LEE_TIPO, N_LEE_TIPO, etiqueta='lectura por tipo (_suma_tipo)')
    t = sust(t, O_LEE_K1, N_LEE_K1, etiqueta='lectura k=1')
    t = sust(t, O_LEE_K, N_LEE_K, etiqueta='lectura k>1')
    t = sust(t, O_ESC_MSG, N_ESC_MSG, etiqueta='prediccion en la escritura del mensaje')
    t = sust(t, O_ESC_MSG2, N_ESC_MSG2, etiqueta='escritura del mensaje')
    t = sust(t, O_ESC_MOR, N_ESC_MOR, etiqueta='prediccion en la escritura del bocado')
    t = sust(t, O_ESC_MOR2, N_ESC_MOR2, etiqueta='escritura del bocado')
    t = sust(t, O_C4LP, N_C4LP, etiqueta='diagnostico de la hermana en la entrega')
    t = sust(t, O_RET, N_RET, etiqueta='diccionario de salida')
    # ---- POSTCONDICIONES
    if t.count('rng.') != t0.count('rng.'):
        raise SystemExit("POSTCONDICION: cambio el uso del rng DEL ORGANISMO. Abortado.")
    if t.count('np.random.default_rng') != t0.count('np.random.default_rng'):
        raise SystemExit("POSTCONDICION: V-5 no puede traer un Generator nuevo. Abortado.")
    if t.count('_esc5(') != 3 or t.count('_lee5(') != 6:
        raise SystemExit(f"POSTCONDICION: _esc5 {t.count('_esc5(')} (esperado 3), _lee5 {t.count('_lee5(')} (esperado 6). Abortado.")
    if t.count('if _CTv:') != 1 or t.count('if _BMv is not None: _dv=') != 1:
        raise SystemExit("POSTCONDICION: la lectura de BA y la baraja tienen que quedar INTACTAS. Abortado.")
    return t


# =============================================================================== EL RUNNER
CAB_RUN = '''"""NIVEL 5 -- SUBIDA (equipo n5): **V-5** (B-5 trasplantado a la tabla de referencia) sobre el candidato BA-v, con
EL MISMO criterio absoluto (ERR-90, P0-P7 + MISION) y el mismo mundo, canal, EMISOR y brazos del bloque 6.
Generado por experimentos/subida_n5/construye_v5.py desde corre_familias_bav.py (4453754a9921e349). NO editar.
Preregistro: experimentos/subida_n5/PREREGISTRO_n5.md.

CELDAS DE LA SERIE (la MISMA tabla y el MISMO mensaje):
  b4b      = base de R6 (obligatoria, ERR-89)
  b6suf    = el sufijo en todas las casillas (control de instrumento: debe reproducir dist alta y BAR-T alto)
  BA-v     = el candidato cerrado el 21-sep (control de instrumento Y linea base de la que hay que mejorar)
  BA-v5    = **EL CANDIDATO**: BA-v + v5=1
  BA-v5-sh = CONTROL que debe fallar: BA-v5 con la memoria BARAJADA (misma R, casilla permutada)
  b5k3-v5  = CONTROL DE OCCAM que puede GANAR al candidato: k=3, un tipo, suma (bloque 5) + v5=1

    python experimentos/subida_n5/corre_v5.py --humo                       (UN proceso: el creador)
    python experimentos/subida_n5/corre_v5.py --serie --desde 25701 --pool 6  (el COORDINADOR)
"""
'''

R_PATH = "sys.path[:0] = [AQUI, JBA, JA, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]"
R_HUMOS = "HUMOS = os.path.join(RAIZ, 'datos', 'humo')"
R_SEM = ("SEM_HUMO = [912]                             # banda de HUMOS (901-920); 911 la gasto BA, 901-903 la junta\n"
         "PROHIBIDAS = set(range(821, 901)) | set(range(921, 1001))   # las SERIES: junta/C (821-900), BA (921-960) y las mias (961-1000)\n")
N_SEM = ("SEM_HUMO = [25791]                           # banda de HUMOS de V-5: 25781-25799 (sin uso en el repo, grep 23-sep)\n"
         "BANDA_HUMO = set(range(25781, 25800))\n"
         "SERIES_V5 = (25701, 25721, 25741)            # serie 25701-25720, replica 25721-25740, TERCERA 25741-25760 (regla 12, solo si el preregistro 7 la pide); sin uso en el repo (grep 23-sep)\n"
         "PROHIBIDAS = set(range(821, 901)) | set(range(921, 1001)) | set(range(25701, 25761))\n")
R_SHA = "SHA_A1_ESPERADO = '8833e1dcfb62f26d'\n"
N_SHA = R_SHA + ("SHA_BAV_ESPERADO = '2dca0a3e239481f0'         # organismo_familias_bav.py: EL ORIGEN del instrumento V-5\n"
                 "SHA_BAV_RUNNER = '4453754a9921e349'           # corre_familias_bav.py: EL ORIGEN de este runner\n"
                 "NBAV = os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv')\n")
R_CEL = ("    'BA-v-sh': dict(_DT, combina='min', msg_elige=0, conj_tipo=2, baraja_msg=1),   # CONTROL: memoria BARAJADA\n"
         "}\n"
         "CELDAS_SERIE = ['b4b', 'b5k3', 'b6suf', 'A1', 'BA-v', 'BA-v-sh']   # b4b SIEMPRE (ERR-89)\n")
N_CEL = ("    'BA-v-sh': dict(_DT, combina='min', msg_elige=0, conj_tipo=2, baraja_msg=1),   # CONTROL: memoria BARAJADA\n"
         "    'BA-v5':   dict(_DT, combina='min', msg_elige=0, conj_tipo=2, v5=1),                 # **EL CANDIDATO V-5**\n"
         "    'BA-v5-sh': dict(_DT, combina='min', msg_elige=0, conj_tipo=2, v5=1, baraja_msg=1),  # CONTROL que debe fallar\n"
         "    'b5k3-v5': dict(k_ganadoras=3, memoria_variante=0, dos_tipos=0, v5=1),              # CONTROL DE OCCAM (puede ganar)\n"
         "}\n"
         "CELDAS_SERIE = ['b4b', 'b6suf', 'BA-v', 'BA-v5', 'BA-v5-sh', 'b5k3-v5']   # b4b SIEMPRE (ERR-89)\n")
R_PLAN = ("PLAN_HUMO = [('b4b', 'CANAL'), ('BA-v', 'CANAL'), ('BA-v', 'CORTADO'),\n"
          "             ('BA-v-sh', 'CANAL'), ('BA-v-sh', 'CORTADO')]\n")
N_PLAN = ("PLAN_HUMO = [('BA-v5', 'CANAL'), ('BA-v5', 'PAR'), ('BA-v5', 'BAR-T'),\n"
          "             ('BA-v5-sh', 'CANAL'), ('BA-v', 'PAR')]\n")
R_PER = "                      'baraja_msg'))\n"
N_PER = "                      'baraja_msg', 'v5'))\n"
R_IMP = "    import organismo_familias_bav as BAV\n"
N_IMP = "    import organismo_familias_v5 as BAV   # V-5: el instrumento nuevo (con v5=0 es organismo_familias_bav bit a bit)\n"
R_DIAG = "             frac_regalo=r.get('frac_regalo'), frac_veneno=r.get('frac_veneno'))\n"
N_DIAG = ("             frac_regalo=r.get('frac_regalo'), frac_veneno=r.get('frac_veneno'),\n"
          "             # ---- V-5 (DIAGNOSTICO, no decide nada): partos, subcasillas, lo que lee la hermana y su 1.a exposicion\n"
          "             v5=r.get('v5'), v5_split_msg=r.get('v5_split_msg'), v5_split_mord=r.get('v5_split_mord'),\n"
          "             v5_t1=r.get('v5_t1'), v5_sub=r.get('v5_sub'), v5_lee_par=r.get('v5_lee_par'),\n"
          "             par1=((r.get('primera_b4') or {}).get(r.get('par_fijo')) or [None])[0])\n")
R_SHAS_INI = "SHAS = lambda: dict(script=h16(os.path.abspath(__file__)),\n"
R_SHAS_FIN = ("ORIGENES = [('origen_ba', SHA_BA_ESPERADO), ('origen_a1', SHA_A1_ESPERADO), ('origen_b6', SHA_B6_ESPERADO),\n"
              "            ('origen_b5', SHA_B5_ESPERADO), ('origen_b4b', SHA_B4B_ESPERADO),\n"
              "            ('origen_organismo_v14', SHA_V14_ESPERADO)]\n")
N_SHAS = ("SHAS = lambda: dict(script=h16(os.path.abspath(__file__)),\n"
          "                    constructor=h16(os.path.join(AQUI, 'construye_v5.py')),\n"
          "                    instrumento=h16(os.path.join(AQUI, 'organismo_familias_v5.py')),\n"
          "                    arnes=h16(os.path.join(AQUI, 'identidad_v5.py')),\n"
          "                    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_n5.md')),\n"
          "                    origen_bav=h16(os.path.join(NBAV, 'organismo_familias_bav.py')),\n"
          "                    runner_bav=h16(os.path.join(NBAV, 'corre_familias_bav.py')),\n"
          "                    origen_ba=h16(os.path.join(JBA, 'organismo_familias_ba.py')),\n"
          "                    origen_a1=h16(os.path.join(JA, 'organismo_familias_a1.py')),\n"
          "                    origen_b6=h16(os.path.join(N12, 'organismo_familias_b6.py')),\n"
          "                    origen_b5=h16(os.path.join(N12, 'organismo_familias_b5.py')),\n"
          "                    origen_b4b=h16(os.path.join(N12, 'organismo_familias_b4b.py')),\n"
          "                    runner_bloque6=h16(os.path.join(N12, 'corre_familias_b6.py')),\n"
          "                    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))\n"
          "ORIGENES = [('origen_bav', SHA_BAV_ESPERADO), ('runner_bav', SHA_BAV_RUNNER),\n"
          "            ('origen_ba', SHA_BA_ESPERADO), ('origen_a1', SHA_A1_ESPERADO), ('origen_b6', SHA_B6_ESPERADO),\n"
          "            ('origen_b5', SHA_B5_ESPERADO), ('origen_b4b', SHA_B4B_ESPERADO),\n"
          "            ('origen_organismo_v14', SHA_V14_ESPERADO)]\n")
R_HUMO_DEF = "def humo(semillas, Tb, plan):\n"
N_CONTRASTES = '''def contrastes(out):
    """V-5: los CONTRASTES PAREADOS DE LA MISMA SERIE, preregistrados en PREREGISTRO_n5.md 5 (no son puertas del
    criterio ERR-90; el veredicto FUNCIONA / ALGO MODESTO / NO los usa como dice el preregistro 7)."""
    g = lambda c, b: (out.get(c, {}).get('com', {}).get(b))
    log("")
    log("CONTRASTES V-5 (misma serie, mismas semillas; preregistro 5):")
    if 'BA-v5' in out and 'BA-v' in out:
        d5, d0 = out['BA-v5']['dist'], out['BA-v']['dist']
        log("  K1 dist(PAR): BA-v5 %d/%d contra BA-v %d/%d -> diferencia %+d (se pide >= +3): %s"
            % (d5[0], d5[1], d0[0], d0[1], d5[0] - d0[0], 'pasa' if d5[0] - d0[0] >= 3 else 'CAE'))
        t5, t0 = g('BA-v5', 'BAR-T'), g('BA-v', 'BAR-T')
        if t5 and t0:
            log("  K3 BAR-T: BA-v5 %d contra BA-v %d (se pide BA-v5 <= BA-v + 2): %s"
                % (t5[0], t0[0], 'pasa' if t5[0] <= t0[0] + 2 else 'CAE'))
        m5, m0 = out['BA-v5']['muertes'], out['BA-v']['muertes']
        if m5 is not None and m0:
            log("  K4 muertes: BA-v5 %s / BA-v %s = %.2fx (diagnostico; la puerta es P7 contra b4b)" % (m5, m0, m5 / m0))
    if 'BA-v5-sh' in out:
        c, co = g('BA-v5-sh', 'CANAL'), g('BA-v5-sh', 'CORTADO')
        if c and co:
            log("  K2 BARAJADA: CANAL(BA-v5-sh) %d <= CORTADO(BA-v5-sh) %d + 3: %s"
                % (c[0], co[0], 'pasa' if c[0] <= co[0] + 3 else 'CAE (la lectura NO es referencial)'))
        elif c:
            log("  K2 BARAJADA: CANAL(BA-v5-sh) %d (sin CORTADO de la celda en esta corrida: n/d)" % c[0])
    if 'b6suf' in out:
        d6, t6 = out['b6suf']['dist'], g('b6suf', 'BAR-T')
        log("  I1 instrumento b6suf: dist %d/%d (previas 19/19, 18/18, 14/16) BAR-T %s (previas 8-12)"
            % (d6[0], d6[1], t6 and t6[0]))
    if 'BA-v' in out:
        log("  I2 instrumento BA-v: dist %d/%d (previas 13/19, 14/18, 11/16)" % tuple(out['BA-v']['dist']))


'''
R_HUMO_TAB = "    tab = tabla(res, cel_act, brazos)\n"
N_HUMO_TAB = "    tab = tabla(res, cel_act, brazos)\n    contrastes(tab)\n"
R_SERIE_TAB = "    tabla(res, cel_act, BRAZOS_BASE)\n    CF._log['f'].close()\n"
N_SERIE_TAB = "    contrastes(tabla(res, cel_act, BRAZOS_BASE))\n    CF._log['f'].close()\n"
R_HUMO_LOG = "                   r['n_mord'], r['n_com'], r['n_ven'], r['frac_regalo']))\n"
N_HUMO_LOG = (R_HUMO_LOG +
              "            log(\"        V-5: v5=%s  partos msg/bocado %s/%s (1.o en t=%s)  subcasillas %s  lee(hermana) tras el "
              "mensaje %s  1.a exposicion de la hermana [t, valor, o, fam, mordio, ...] %s\"\n"
              "                % (r['v5'], r['v5_split_msg'], r['v5_split_mord'], r['v5_t1'], r['v5_sub'], r['v5_lee_par'], r['par1']))\n")
R_TIT_H = 'HUMO del candidato BA-v (nivel 5, criterio ERR-90). UN proceso, sin Pool (regla 3).'
N_TIT_H = 'HUMO del candidato V-5 (nivel 5, subida_n5, criterio ERR-90). UN proceso, sin Pool (regla 3).'
R_TIT_S = '"SERIE del candidato BA-v (nivel 5, criterio ERR-90), Pool(%d)."'
N_TIT_S = '"SERIE del candidato V-5 (nivel 5, subida_n5, criterio ERR-90), Pool(%d)."'
R_DESDE = "        serie(arg('--desde', 961), arg('--n', 20), arg('--T', 100000), cel_act, npool)\n"
N_DESDE = ("        _d5 = arg('--desde', SERIES_V5[0])\n"
           "        if _d5 not in SERIES_V5:\n"
           "            raise SystemExit('--desde %d: las semillas preregistradas de V-5 son %s (y 20 cada una).' % (_d5, SERIES_V5))\n"
           "        serie(_d5, arg('--n', 20), arg('--T', 100000), cel_act, npool)\n")
R_HCHK = ("    if any(s in PROHIBIDAS for s in sem):\n"
          "        raise SystemExit(\"HUMO: %s cae en una serie (821-900 o 921-1000). La banda de humos es 901-920.\" % sem)\n")
N_HCHK = ("    if any(s in PROHIBIDAS or s not in BANDA_HUMO for s in sem):\n"
          "        raise SystemExit(\"HUMO: %s fuera de la banda de humos de V-5 (25781-25799).\" % sem)\n")


def construye_runner():
    t0 = origen(os.path.join(NBAV, 'corre_familias_bav.py'), SHA_BAV_RUNNER)
    t = CAB_RUN + t0
    t = sust(t, R_PATH, "sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv'), JBA, JA, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]", etiqueta='sys.path')
    t = sust(t, R_HUMOS, "HUMOS = os.path.join(AQUI, 'datos', 'humo')   # V-5: los humos en experimentos/subida_n5/datos/humo/", etiqueta='carpeta de humos')
    t = sust(t, R_SEM, N_SEM, etiqueta='semillas')
    t = sust(t, R_SHA, N_SHA, etiqueta='shas de origen')
    t = sust(t, R_CEL, N_CEL, etiqueta='celdas')
    t = sust(t, R_PLAN, N_PLAN, etiqueta='plan del humo')
    t = sust(t, R_PER, N_PER, etiqueta='perillas de celda (regla 14)')
    t = sust(t, R_IMP, N_IMP, etiqueta='import del instrumento')
    t = sust(t, R_DIAG, N_DIAG, etiqueta='diagnostico V-5 por corrida')
    i, j = t.find(R_SHAS_INI), t.find(R_SHAS_FIN)
    if i < 0 or j < 0 or t.count(R_SHAS_INI) != 1 or t.count(R_SHAS_FIN) != 1:
        raise SystemExit("ANCLA SHAS/ORIGENES: no encontrada exactamente una vez. Abortado.")
    t = t[:i] + N_SHAS + t[j + len(R_SHAS_FIN):]
    t = sust(t, R_HUMO_DEF, N_CONTRASTES + R_HUMO_DEF, etiqueta='contrastes')
    t = sust(t, R_HUMO_TAB, N_HUMO_TAB, etiqueta='contrastes en el humo')
    t = sust(t, R_SERIE_TAB, N_SERIE_TAB, etiqueta='contrastes en la serie')
    t = sust(t, R_HUMO_LOG, N_HUMO_LOG, etiqueta='log V-5 del humo')
    t = sust(t, R_TIT_H, N_TIT_H, etiqueta='titulo del humo')
    t = sust(t, R_TIT_S, N_TIT_S, etiqueta='titulo de la serie')
    t = sust(t, "'humo_bav_%s", "'humo_v5_%s", n=3, etiqueta='nombres de humo')
    t = sust(t, "'serie_bav_s%d-%d_%s", "'serie_v5_s%d-%d_%s", n=2, etiqueta='nombres de serie')
    t = sust(t, R_DESDE, N_DESDE, etiqueta='semillas de la serie')
    t = sust(t, R_HCHK, N_HCHK, etiqueta='banda de humos')
    if 'organismo_familias_bav as' in t:
        raise SystemExit("POSTCONDICION: el runner sigue importando el instrumento viejo. Abortado.")
    return t


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(NBAV, 'identidad_familias_bav.py'), SHA_BAV_ARNES)]:
        if h16(p) != sha:
            raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    org, run = construye_organismo(), construye_runner()
    for nom, txt in (('organismo_familias_v5.py', org), ('corre_v5.py', run)):
        p = os.path.join(AQUI, nom)
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            f.write(txt)
        print(f"  escrito {nom:28s} sha256_16 {h16(p)}")
    compile(org, 'organismo_familias_v5.py', 'exec'); compile(run, 'corre_v5.py', 'exec')
    print("  compilan los dos. Siguiente: python experimentos/subida_n5/identidad_v5.py (ANTES de mirar numeros)")


if __name__ == '__main__':
    main()
