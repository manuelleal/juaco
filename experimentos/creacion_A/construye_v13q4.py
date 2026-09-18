"""CREADOR A — construye `organismo_v13q4.py` POR ANCLAS desde `experimentos/nivel7_xor_lectura/organismo_v13q3.py`
(`aaebe073308a40c2`, que SOLO se lee) + la perilla `seleccion` del paquete A-1 (ii).

MECANISMO (cascade-correlation local; Fahlman & Lebiere 1989 segun la respuesta A-Q1 del explorador):
  - los rasgos ELEMENTALES de la lectura (los pixeles — P0,P1 en el oraculo — y la constante) son SIEMPRE plasticos;
  - cada rasgo CONJUNTIVO candidato lleva UN escalar `e_i` (correlacion acumulada con el residuo) y UN bit (abierto);
  - se abre UNO solo, el de mayor `|e_i|`, si supera `sel_theta`, y queda abierto (cupo `sel_cupo`, por defecto 1);
  - la via lenta SOLO aprende en los rasgos abiertos; los cerrados quedan en 0 y no entran en la lectura.
  Localidad: `e_i` ve su propia entrada `phi_i` y el residuo global `_ds` que ya llega (tercer factor). La competencia
  es un argmax sobre candidatos: la misma operacion que el top-K del codigo Kenyon que el organismo ya hace.
  Memoria: un flotante + un bit por candidato (15 en cuadratica, 1 en el oraculo, 0 en lineal).
  `sel_estad='cond'`  ->  e_i <- (1-rho)*e_i + rho*_ds   SOLO cuando phi_i > 0   (media del residuo bajo el rasgo)
  `sel_estad='cov'`   ->  e_i <- (1-rho)*e_i + rho*(_ds*phi_i)  en cada mordida  (covarianza, la de cascade-corr.)

`seleccion=None` (por defecto) toma EXACTAMENTE la rama original: identidad bit a bit obligatoria (`identidad_v13q4.py`).
NO edita el original. Sin commits.
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, '..', 'nivel7_xor_lectura', 'organismo_v13q3.py')
DEST = os.path.join(AQUI, 'organismo_v13q4.py')

src = open(ORIG, 'r', encoding='utf-8').read()
sha = hashlib.sha256(open(ORIG, 'rb').read()).hexdigest()[:16]
assert sha == 'aaebe073308a40c2', f'origen inesperado: {sha}'

# ------------------------------------------------------------------ ancla 1: firma
A1 = ",regla_lenta='dos_canales',constante=False,lam_lenta=0.002):   # xor: lectura de la via lenta; 3d: regla de la via lenta, termino constante y decaimiento"
B1 = (",regla_lenta='dos_canales',constante=False,lam_lenta=0.002,"
      "seleccion=None,sel_theta=0.6,sel_rho=0.05,sel_cupo=1,sel_calienta=0,sel_estad='cond'):"
      "   # xor: lectura de la via lenta; 3d: regla de la via lenta, termino constante y decaimiento; creacion_A A-1(ii): seleccion de rasgos conjuntivos por competencia")
assert src.count(A1) == 1, 'ancla 1'

# ------------------------------------------------------------------ ancla 2: estado de la seleccion
A2 = "    Ws=np.zeros(_NF)   # 3d: vector con signo de la via lenta; solo se mueve/lee si regla_lenta=='delta_signo'"
B2 = A2 + """
    if seleccion not in (None,'wta'): raise ValueError(f"seleccion={seleccion!r}")   # creacion_A: un knob mal escrito NO puede caer en silencio al brazo original
    if sel_estad not in ('cond','cov'): raise ValueError(f"sel_estad={sel_estad!r}")
    _e4=np.zeros(_NF); _ab4=np.ones(_NF,bool); _cand4=np.zeros(_NF,bool); _abre4=[]; _nsel4=0   # creacion_A A-1(ii): elegibilidad, bit de abierto, mascara de candidatos, historia de aperturas, contador de mordidas
    if seleccion is not None:
        _npx4=2 if lectura in ('oraculo01','oraculo01_ruido') else 6   # elementales: los pixeles (P0,P1 en el oraculo)
        _ncj4=0 if lectura=='lineal' else (1 if lectura in ('oraculo01','oraculo01_ruido') else 15)   # candidatos: los productos (o los 15 bits de random15, como control)
        _cand4[_npx4:_npx4+_ncj4]=True; _ab4=~_cand4   # elementales y constante ABIERTOS; conjuntivos CERRADOS"""
assert src.count(A2) == 1, 'ancla 2'

# ------------------------------------------------------------------ ancla 3: la actualizacion de la via lenta
A3 = """                        if regla_lenta=='delta_signo':   # 3d (A+B+C): UN vector con signo, decaimiento multiplicativo de TODO el vector, tope simetrico. Sin aversion (todas las corridas de 3d usan aversion=1.0)
                            Ws=np.clip(Ws*(1-lam_lenta)+eta_s*_ds*phi(P_[kk]),-clip_s,clip_s)
                        else:   # 'dos_canales': la regla original de v13/v13q, sin tocar (identidad obligatoria)"""
B3 = """                        if seleccion is not None:   # creacion_A A-1(ii): elegibilidad por rasgo, competencia entre candidatos, y la via lenta aprende SOLO lo abierto
                            _ph4=phi(P_[kk]); _act4=_ph4>0; _nsel4+=1
                            if sel_estad=='cond': _e4[_act4]=(1-sel_rho)*_e4[_act4]+sel_rho*_ds   # media movil del residuo BAJO el rasgo
                            else:                 _e4=(1-sel_rho)*_e4+sel_rho*(_ds*_ph4)          # correlacion acumulada (cascade-correlation)
                            if _nsel4>=sel_calienta and int((_ab4&_cand4).sum())<sel_cupo:
                                _c4=_cand4&~_ab4
                                if _c4.any():
                                    _j4=int(np.argmax(np.where(_c4,np.abs(_e4),-1.0)))
                                    if abs(float(_e4[_j4]))>sel_theta: _ab4[_j4]=True; _abre4.append((int(t),int(_j4),round(float(_e4[_j4]),4),int(_nsel4)))
                            _phm4=_ph4*_ab4   # los cerrados no reciben error y quedan en 0
                            if regla_lenta=='delta_signo':
                                Ws=np.clip(Ws*(1-lam_lenta)+eta_s*_ds*_phm4,-clip_s,clip_s)
                            else:
                                if lam: _mcs=np.minimum(Wps,Wns)*(_phm4>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs
                                if _ds>0: Wps=np.clip(Wps+eta_s*_ds*_phm4,0,clip_s)
                                else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*_phm4,0,clip_s)
                        elif regla_lenta=='delta_signo':   # 3d (A+B+C): UN vector con signo, decaimiento multiplicativo de TODO el vector, tope simetrico. Sin aversion (todas las corridas de 3d usan aversion=1.0)
                            Ws=np.clip(Ws*(1-lam_lenta)+eta_s*_ds*phi(P_[kk]),-clip_s,clip_s)
                        else:   # 'dos_canales': la regla original de v13/v13q, sin tocar (identidad obligatoria)"""
assert src.count(A3) == 1, 'ancla 3'

# ------------------------------------------------------------------ ancla 4: el return (lecturas nuevas)
A4 = "    return dict(sobre=sobre,"
B4 = ("    return dict(seleccion=seleccion,sel_estad=sel_estad,sel_theta=sel_theta,sel_rho=sel_rho,sel_cupo=sel_cupo,\n"
      "                sel_abre=_abre4,sel_abiertos=[int(_i) for _i in np.where(_ab4&_cand4)[0]],\n"
      "                sel_e=[round(float(_x),4) for _x in _e4],sel_n=int(_nsel4),sobre=sobre,")
assert src.count(A4) == 1, 'ancla 4'

cab = ('"""organismo_v13q4 = organismo_v13q3.py (%s) + perilla `seleccion` (A-1 ii del CREADOR A):\n'
       'cascade-correlation local sobre los rasgos conjuntivos de la via lenta. Knobs: seleccion=None|\'wta\',\n'
       'sel_theta, sel_rho, sel_cupo, sel_calienta, sel_estad=\'cond\'|\'cov\'.\n'
       'Generado por experimentos/creacion_A/construye_v13q4.py. NO editar a mano.\n'
       'Con seleccion=None es organismo_v13q3 EXACTO (identidad obligatoria: identidad_v13q4.py)."""\n' % sha)
out = cab + src.replace(A1, B1).replace(A2, B2).replace(A3, B3).replace(A4, B4)
open(DEST, 'w', encoding='utf-8').write(out)
print(f'origen organismo_v13q3.py sha {sha}')
print(f'escrito organismo_v13q4.py  sha {hashlib.sha256(open(DEST,"rb").read()).hexdigest()[:16]}')
