"""Construye experimentos/nivel12_mundo_familias/organismo_familias_b2.py POR ANCLAS desde el INSTRUMENTO DEL
BLOQUE 1 experimentos/nivel12_mundo_familias/organismo_familias.py (b9dd561a0cf056b8, identidad 43/43), que aqui
SOLO SE LEE. El tronco organismo/organismo_v14.py (feefc88b1fd8d434) tampoco se toca: se hereda por la cadena.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada.

BLOQUE 2 -- CAPACIDAD DIRECTA (PREREGISTRO_bloque2_variante.md). NO hay organo nuevo: el organismo sigue siendo
v14.1 tal cual. Lo unico que se agrega son TRES PERILLAS DEL MUNDO / DEL REGISTRO, todas APAGADAS por defecto:

  vira        int. En `cambio` cambia de consecuencia SOLO un conjunto declarado de variantes ("la sal rosa que
              envenena"), sin tocar a sus hermanas.
                vira = 0  (POR DEFECTO)  -> legado: val_post = la familia T0 entera se invierte (organismo_familias).
                vira > 0                 -> val_post = invierten las `vira` primeras de exc_win (una por token), y
                                            NADA MAS: el token y las otras V-1 variantes conservan su valencia.
                vira < 0                 -> val_post = {}: en `cambio` NO cambia nada, pero DECLARA las mismas
                                            |vira| variantes (el gemelo de control: mide a las MISMAS hermanas).
  exc_evita   int. Variante que las excepciones NUNCA pueden ocupar (-1 = ninguna, POR DEFECTO). Sirve para que la
              variante RETENIDA por la deriva (la nunca vista) no sea ademas una excepcion. Con exc_evita >= 0 el
              sorteo de exc_win sigue consumiendo EXACTAMENTE UN entero del rng propio del mundo por token.
  reg_b2      0/1 (POR DEFECTO 0). Solo REGISTRO: no toca ninguna variable de estado, no consume rng y no altera
              ninguna decision. Con 1 el instrumento devuelve ademas:
                primera_b2[k] = [t, valor_leido_por_la_boca, obj, ruta_rapida, mordio, hambre, lenta, rapida]
                                -- la PRIMERA exposicion a cada estimulo, con la CONDUCTA (mordio) incluida.
                sep_exp[e]    = exposiciones a la virada `e` DESPUES de `cambio` hasta que la boca la lee con su
                                valencia NUEVA (|v| >= crit_exp) Y con signo distinto al de >= 2 de sus 3 hermanas.
                enc_post[k]   = exposiciones a cada estimulo desde `cambio`.
                viradas, val_post, vira, exc_evita, reg_b2, cambio_b2, log_cada.

ANCLA DE IDENTIDAD (regla 2 de EQUIPO.md): con vira=0, exc_evita=-1 y reg_b2=0 esto es organismo_familias.py BIT A
BIT -- mismas claves, mismos dobles, mismo consumo de rng -- y por lo tanto, con mundo='AB', organismo_v14 bit a bit.
Se logra asi:
  (1) exc_evita = -1 deja la comprension de exc_win LITERALMENTE como estaba (misma expresion, mismo sorteo).
  (2) vira = 0 deja val_post LITERALMENTE como estaba.
  (3) reg_b2 = 0 no ejecuta ni una linea nueva dentro del bucle, y `_ext` no recibe ninguna clave nueva: las claves
      del diccionario de salida son EXACTAMENTE las de organismo_familias.
  (4) Ninguna linea nueva llama al rng del organismo ni al rng propio del mundo mas veces que el original.
  (5) `valor(PAT[h])` (la lectura de las hermanas) es la MISMA funcion que usa la boca y NO consume rng.
El arnes identidad_familias_b2.py lo comprueba, y ademas repite el arnes del bloque 1 sobre el modulo nuevo.

Uso:  python experimentos/nivel12_mundo_familias/construye_familias_b2.py     (no corre el organismo)
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREB, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

SHA_ORIGEN = 'b9dd561a0cf056b8'      # experimentos/nivel12_mundo_familias/organismo_familias.py (bloque 1, 43/43)
SHA_V14 = 'feefc88b1fd8d434'         # organismo/organismo_v14.py (TRONCO CONGELADO; solo se comprueba)
SHA_ESCALA = 'd8b8566bca77a0ae'      # escala_codigo.py (bloque 0: catalogo + KW)
DESTINO = os.path.join(AQUI, 'organismo_familias_b2.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado (no se escribe nada).")
    return open(p, encoding='utf-8').read()


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


# ===================== ANCLAS (copiadas literalmente de organismo_familias.py) =====================
A_DEF = "def _familias(seed,D,n_var,F,V,n_exc,fam_val,n_neu):"
A_EXCWIN = "    exc_win=['T%dv%d'%(_k,int(g.integers(V))) for _k in range(F)]"
A_VALPOST = ("    val_post={_n:_op[val[_n]] for _n in PAT if fam[_n]==0 and _n not in exc}   "
             "# CAMBIO: la familia 0 invierte; su excepcion NO")
A_RETFAM = ("    return dict(PAT=PAT,fam=fam,var=var,val=val,exc=exc,exc_win=exc_win,herm=herm,pres=pres,"
            "val_post=val_post,")
A_FIRMA = ",fam_val='familia',deriva=5000,cambio=None,renov=0.0,vent=10000,crit_exp=0.5):"
A_LLAMA = ("    _FA=_familias(seed,fam_D,fam_nvar,fam_F,fam_V,n_exc,fam_val,n_neu) if _MF else None   "
           "# rng PROPIO: no toca el del organismo")
A_INIT = "    _enc={}; _exp={}; _ult={}; _prim={}; _rut=[0,0]; _texc={}; _col=0; _omi=0; _nren=0; _fv=[[],[],[],[]]"
A_ULT = "                _ult[kk]=[t,round(float(_wt),3),_o0]"
A_EXT = ("               frac_regalo=round(0.6*deaths/max(T*costo,1e-9),4)) if _MF else {})   "
         "# FAMILIAS: claves nuevas SOLO si mundo!='AB'")

CABECERA = '''"""organismo_familias_b2 = experimentos/nivel12_mundo_familias/organismo_familias.py (b9dd561a0cf056b8,
identidad 43/43; que a su vez es el TRONCO organismo/organismo_v14.py, v14.1, feefc88b1fd8d434) + TRES PERILLAS
DEL MUNDO/REGISTRO para el BLOQUE 2 (capacidad directa): `vira` (una variante -- y solo ella -- cambia de
consecuencia en `cambio`), `exc_evita` (las excepciones no ocupan la variante retenida) y `reg_b2` (registro de la
CONDUCTA de la boca en la primera exposicion y de la separacion tras el cambio).
NO hay organo nuevo: el organismo sigue siendo v14.1 tal cual.
ANCLA DE IDENTIDAD: con vira=0, exc_evita=-1, reg_b2=0 es organismo_familias BIT A BIT (mismas claves, mismo rng);
y por herencia, con mundo='AB', organismo_v14 bit a bit.  Arnes: identidad_familias_b2.py.
Generado por construye_familias_b2.py. NO editar a mano."""
'''

# --------------------------------------------------------------- las tres perillas, escritas
N_DEF = "def _familias(seed,D,n_var,F,V,n_exc,fam_val,n_neu,exc_evita=-1,vira=0):"

N_EXCWIN = """    if int(exc_evita)<0: exc_win=['T%dv%d'%(_k,int(g.integers(V))) for _k in range(F)]
    else:   # B2: la variante RETENIDA por la deriva no puede ser ademas excepcion. UN entero del rng por token, igual que arriba.
        _al=[_v for _v in range(V) if _v!=int(exc_evita)]
        exc_win=['T%dv%d'%(_k,_al[int(g.integers(len(_al)))]) for _k in range(F)]"""

N_VALPOST = """    if int(vira)>0:     _vp={_n:_op[val[_n]] for _n in exc_win[:int(vira)]}          # B2 SAL ROSA: cambia la variante, NO sus hermanas
    elif int(vira)<0:   _vp={}                                                          # B2 gemelo de control: en `cambio` no cambia NADA
    else:               _vp={_n:_op[val[_n]] for _n in PAT if fam[_n]==0 and _n not in exc}   # CAMBIO: la familia 0 invierte; su excepcion NO
    val_post=_vp"""

N_RETFAM = ("    return dict(PAT=PAT,fam=fam,var=var,val=val,exc=exc,exc_win=exc_win,herm=herm,pres=pres,"
            "val_post=val_post,viradas=list(exc_win[:abs(int(vira))]),")

N_FIRMA = (",fam_val='familia',deriva=5000,cambio=None,renov=0.0,vent=10000,crit_exp=0.5,"
           "vira=0,exc_evita=-1,reg_b2=0):")

N_LLAMA = ("    _FA=_familias(seed,fam_D,fam_nvar,fam_F,fam_V,n_exc,fam_val,n_neu,exc_evita,vira) if _MF else None   "
           "# rng PROPIO: no toca el del organismo")

N_INIT = ("    _enc={}; _exp={}; _ult={}; _prim={}; _rut=[0,0]; _texc={}; _col=0; _omi=0; _nren=0; _fv=[[],[],[],[]]\n"
          "    _pb2={}; _sep={}; _en2={}; _vir=(set(_FA['viradas']) if _MF else set())   "
          "# B2: registro (reg_b2). Dicts vacios: no consumen rng ni cambian ninguna decision.")

N_ULT = """                _ult[kk]=[t,round(float(_wt),3),_o0]
                if reg_b2:   # B2: CONDUCTA de la boca (nunca pesos: ERR-44). `mordio` ya esta decidido arriba; `valor` no consume rng.
                    if kk not in _pb2: _pb2[kk]=[t,round(float(_wt),3),_o0,int(bool(_fam(kc))),int(bool(mordio)),round(float(hambre),3),round(float(_ws),3),round(float(_wf),3)]
                    if t>=_tcam:
                        _en2[kk]=_en2.get(kk,0)+1
                        if kk in _vir and kk not in _sep and _o0 and _wt*_o0>0 and abs(_wt)>=crit_exp:
                            _vh=[float(valor(PAT[_h])) for _h in _FA['herm'][kk]]   # SEPARACION: signo distinto al de >= 2 de sus 3 hermanas
                            if sum(1 for _z in _vh if _z*_wt<=0)>=2: _sep[kk]=_en2[kk]"""

N_EXT = ("               frac_regalo=round(0.6*deaths/max(T*costo,1e-9),4)) if _MF else {})   "
         "# FAMILIAS: claves nuevas SOLO si mundo!='AB'\n"
         "    if _MF and reg_b2: _ext.update(reg_b2=1,vira=int(vira),exc_evita=int(exc_evita),cambio_b2=_tcam,"
         "log_cada=log_cada,viradas=list(_FA['viradas']),val_post=dict(_FA['val_post']),primera_b2=dict(_pb2),"
         "sep_exp=dict(_sep),enc_post=dict(_en2))   # B2: claves nuevas SOLO con reg_b2=1 (identidad)")


def main():
    for p, sha in [(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14),
                   (os.path.join(AQUI, 'escala_codigo.py'), SHA_ESCALA)]:
        if h16(p) != sha:
            raise SystemExit(f"ORIGEN {os.path.basename(p)}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    t = origen(os.path.join(AQUI, 'organismo_familias.py'), SHA_ORIGEN)

    t = CABECERA + t
    t = sust(t, A_DEF, N_DEF, etiqueta='firma de _familias')
    t = sust(t, A_EXCWIN, N_EXCWIN, etiqueta='sorteo de exc_win')
    t = sust(t, A_VALPOST, N_VALPOST, etiqueta='val_post (la sal rosa)')
    t = sust(t, A_RETFAM, N_RETFAM, etiqueta='return de _familias')
    t = sust(t, A_FIRMA, N_FIRMA, etiqueta='firma de run')
    t = sust(t, A_LLAMA, N_LLAMA, etiqueta='llamada a _familias')
    t = sust(t, A_INIT, N_INIT, etiqueta='inicializacion del registro')
    t = sust(t, A_ULT, N_ULT, etiqueta='registro en la exposicion')
    t = sust(t, A_EXT, N_EXT, etiqueta='_ext')

    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print(f"  escrito {os.path.relpath(DESTINO, RAIZ)}")
    print(f"  sha origen  organismo_familias.py    {SHA_ORIGEN}")
    print(f"  sha destino organismo_familias_b2.py {h16(DESTINO)}")
    print("  ahora: python experimentos/nivel12_mundo_familias/identidad_familias_b2.py")


if __name__ == '__main__':
    main()
