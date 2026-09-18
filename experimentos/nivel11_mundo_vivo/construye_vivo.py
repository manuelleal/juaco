"""Construye experimentos/nivel11_mundo_vivo/organismo_vivo.py POR ANCLAS desde el TRONCO CONGELADO
organismo/organismo_v14.py (v14.1, feefc88b1fd8d434), que aqui SOLO SE LEE (regla 1 de EQUIPO.md; manifiesto.py).

MUNDO VIVO (linea (F) de registro/PLAN.md, idea del director 18-sep 06:10): el organismo como SER con varias
NECESIDADES y varios ESTIMULOS. Version minima legible:

  DOS necesidades   : 0 = hambre (energia E, la de v14)   1 = sed (agua Ag, nueva)
  CUATRO estimulos  : los CUATRO patrones que YA existen en el tronco (PAT A,B,C,D) -- no se toca la retina
      A comida (+0.8 E)   B veneno (-0.4 E)   C agua (+0.8 Ag)   D sal (-0.4 Ag)
  Estado interno    : vectorial (E, Ag), cada uno con su descenso (costo, costo_a) y SU MUERTE (E<=0 o Ag<=0)
  Boca              : decide con la NECESIDAD ACTIVA (la de mayor deficit): lee SU fila de valor y su deficit
  Valor aprendido   : POR ESTIMULO Y POR NECESIDAD -- Wp/Wn y Wps/Wns pasan de vector a MATRIZ (n_nec, ...)
  Sorpresa          : el predictor de dE del bloque 6 pasa a VECTOR (una salida por necesidad); sorpresa por necesidad
  Un encuentro      : ensena a TODAS las necesidades (la mordida tiene consecuencia VECTORIAL dS=(dE,dAg))

ANCLA DE IDENTIDAD (la exigencia central del encargo): con UNA necesidad (n_nec=1) y DOS estimulos (vivo=0 ->
tipos=['A','B']) esto es organismo_v14 BIT A BIT, mismo consumo del rng y MISMAS CLAVES DE SALIDA (el dict extra
del mundo vivo se agrega SOLO si vivo=1; con vivo=0 el return es literalmente el de v14). Se logra asi:
  (1) NINGUNA linea nueva consume el rng del organismo. El unico rng nuevo (nec_shuf, control barajado) es un
      Generator PROPIO (seed+900000) que solo se crea si la perilla esta encendida (convencion de v13s).
  (2) El unico sorteo que dependeria del mundo nuevo es spawn(): rng.integers(len(tipos)). Con dos estimulos
      len(tipos)=2, exactamente como v14 -> mismo stream. Por eso los CUATRO estimulos son los CUATRO patrones
      que ya existen: no cambia la retina (6 px), no cambia KW (NKMAX,6) ni el bucle de rechazo de cond(), que
      solo restringe code(A) & code(B). Cambiar la retina (p.ej. meter la necesidad como dos pixeles mas, la
      alternativa "codigo conjuntivo") SI cambiaria rng.uniform(0,1,(NK,6)) y romperia el ancla: ver el informe.
  (3) Todo lo que agrega el mundo vivo vive detras de un guardia (if vivo:, if n_nec>1:, if eta_pred:, if k_sorp:)
      o es una reindexacion inerte: Wp pasa de (NKMAX,) a (n_nec,NKMAX) y se lee Wp[_nm] con _nm=0 fijo cuando
      n_nec=1 -- misma vista 1-D, mismas operaciones elemento a elemento, mismos dobles IEEE.
  (4) La segunda muerte (Ag<=0) es imposible con vivo=0: Ag=A_ini=1.0 y no se drena (el drenaje esta guardado).
  (5) El eje de energia del mundo vivo ES el de v14: EFECTO['comida'][0]==E_VAL['comida'] y
      EFECTO['veneno'][0]==E_VAL['veneno'], y el mapa de recompensa (dS>0 -> +1, dS<0 -> -3) reproduce R_VAL.
El arnes identidad_vivo.py lo comprueba en >= 6 casos (un proceso, T <= 30000).

PERILLAS NUEVAS (todas inertes por defecto -> v14):
  vivo=0        mundo vivo encendido (consecuencia vectorial, 4 valencias, drenaje de agua, segunda muerte)
  n_nec=1       necesidades en la MENTE (filas de valor). n_nec>1 exige vivo=1
  estims=None   estimulos presentes; None -> ['A','B'] (v14). Mundo vivo: ('A','B','C','D')
  costo_a=0.002 descenso de agua por paso (solo si vivo)
  A_ini=1.0     agua inicial
  val_esc=0     CONTROL/alternativa: 1 -> UN solo escalar por celda para todas las necesidades (la necesidad
                queda solo como contexto del impulso). Es el control que decide si el valor DEBE ser por necesidad
  nec_shuf=0    CONTROL barajado, DOS modos (rng propio; el cuerpo nunca cambia):
                  1 = POLITICA barajada: la necesidad que la boca cree activa se sortea. NO destruye la tabla de
                      valor (cada fila sigue viendo SU componente): destruye la conducta y la supervivencia.
                  2 = CONTENIDO barajado: la componente de dS que ENSENA a cada necesidad se permuta en cada
                      bocado. Es el control decisivo del diseno: si la tabla necesidad x estimulo sobrevive a
                      esto, lo que la produce no es la necesidad. (Hallado por mini_vivo.py: con el modo 1 el
                      control pasaba por la razon equivocada.)
  hereda_nec=1  la hija hereda el valor de las OTRAS necesidades (la madre lo conserva); la fision es de la activa
  tabla=None    tabla (dE,dAg) por valencia; sirve para el control "estimulo que no informa" (sal -> (0,0))
  eta_pred=0.0  predictor VECTORIAL de dS (bloque 6, allostasis). Solo mide: no entra en la decision si k_sorp=0
  ema_pred/clip_e constantes del predictor
  k_sorp=0.0    la sorpresa de la necesidad ACTIVA entra en la boca (la dosis de v15, ahora especifica por necesidad)
  crit_exp=0.5  umbral de |valor| para "exposiciones hasta criterio" (solo lectura)

Uso:  python experimentos/nivel11_mundo_vivo/construye_vivo.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
# organismo/ PRIMERO en sys.path (ERR-28), sin excepcion, aunque aqui el tronco solo se lea como texto.
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

# El TRONCO se movio a v14.1 (eta_s=0.15, clip_s=10, bloque A-4) a las 05:55, mientras se construia esto.
# Por eso la ancla de la FIRMA no incluye eta_s/clip_s (que el tronco puede recalibrar sin cambiar de version):
# la constante que dispara el aborto es el sha, que es el tripwire correcto. Origen actual:
SHA_V14 = 'feefc88b1fd8d434'   # organismo/organismo_v14.py = v14.1 (18 sep 05:55)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


# ============================ ANCLAS (copiadas literalmente de organismo/organismo_v14.py) ============================
A_TABLAS = "R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}"
A_FIRMA = "puerta=3,mask_rel=2,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=5,pat_shuf=0,pat_min=1):"
A_WPWN = ("    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); "
          "splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)\n")
A_LENTA = "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n"
A_FAM = ("    def _fam(_k):   # B: la puerta. puerta_pat>0 -> evidencia del codigo exacto; si no, celdas consolidadas (v13 EXACTO)\n"
         "        if puerta_pat: return _ev(_k)>=puerta_pat and int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=pat_min\n"
         "        return int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta\n")
A_VALOR = "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)\n"
A_VALRET = ("        return _f+_s if puerta is None else (_f if _fam(_k) else _s)   # familiar = >= puerta celdas "
            "del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)\n")
A_POS = "    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}\n"
A_SOBRE = ("    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; "
           "sin_objetivo=[0]*4   # v9: lectura\n")
A_TIPOS = "    tipos=['A','B']\n"
A_HAMBRE = "        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k]\n"
A_WB = ("            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); "
        "_ws=float((Wps-Wns)@PAT[kk])   # v13: las dos vias\n")
A_VB = "            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb\n"
A_LLEG = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
A_MORD = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n"
A_LEARN = "                if learn:\n"
A_LENTAUPD = ("                        if lam: _mcs=np.minimum(Wps,Wns)*(PAT[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs\n"
              "                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*PAT[kk],0,clip_s)\n"
              "                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)\n")
A_LAMIX = ("                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom"
           "   # BUG-01 exp2: decae solo la parte comun\n")
A_TRUNCA = ("                    if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())\n"
            "                    else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())\n")
A_UPD = ("                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)\n"
         "                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)\n")
A_CONF = "                    if t_conflicto is None and bool((np.minimum(Wp[_ix],Wn[_ix])>0).any()): t_conflicto=t\n"
A_FISION = ("                                    if R>0: Wp[j]=Wp[c]; Wn[j]=0.; Wp[c]=0.\n"
            "                                    else:   Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.\n")
A_THETA = ("                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; "
           "splits+=1; split_t.append((t,kk))\n")
A_COSTO = "        E-=costo\n"
A_MUERTE = "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))\n"
A_WLENTA = "    W_lenta={k:round(float((Wps-Wns)@PAT[k]),3) for k in PAT}   # v13: lectura de la via lenta sola\n"
A_COMP = "    comp={k:(round(float(Wp@kenyon(PAT[k])),2),round(float(Wn@kenyon(PAT[k])),2)) for k in PAT}\n"
A_RET = "    return dict(sobre=sobre,"
A_RETFIN = "W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns])"

CAB = '''"""organismo_vivo = organismo/organismo_v14.py (v14.1, feefc88b1fd8d434, TRONCO CONGELADO: aqui solo se LEYO) +
MUNDO VIVO (nivel 11, linea (F) de PLAN.md): DOS necesidades (hambre/sed) y CUATRO estimulos (comida A, veneno B,
agua C, sal D = los cuatro patrones que ya existen), estado interno VECTORIAL con dos muertes posibles, boca que
decide con la NECESIDAD ACTIVA, valor aprendido POR ESTIMULO Y POR NECESIDAD (Wp/Wn/Wps/Wns pasan a matriz
(n_nec, ...)), predictor de dS VECTORIAL y sorpresa POR NECESIDAD.
ANCLA DE IDENTIDAD: con vivo=0 y n_nec=1 (una necesidad, dos estimulos) es organismo_v14 BIT A BIT -- mismo
consumo del rng y MISMAS claves de salida (el dict del mundo vivo se agrega solo si vivo=1).
Arnes: identidad_vivo.py.  Generado por construye_vivo.py. NO editar a mano."""
'''


if __name__ == '__main__':
    s = origen(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14)

    # ---- 1) tablas del mundo vivo (el eje de energia ES el de v14, por construccion) ----
    s = sust(s, A_TABLAS, A_TABLAS + "\n"
             "# --- MUNDO VIVO (nivel 11): DOS necesidades y CUATRO estimulos = los CUATRO patrones que YA existen.\n"
             "#     El eje de ENERGIA es exactamente el de v14: EFECTO['comida'][0]==E_VAL['comida'] y\n"
             "#     EFECTO['veneno'][0]==E_VAL['veneno']; el mapa de recompensa (dS>0->+1, dS<0->-3) reproduce R_VAL.\n"
             "NEC=('hambre','sed')   # 0 = energia (E), 1 = agua (Ag)\n"
             "VAL_VIVO={'A':'comida','B':'veneno','C':'agua','D':'sal'}\n"
             "EFECTO={'comida':(+0.8,0.0),'veneno':(-0.4,0.0),'agua':(0.0,+0.8),'sal':(0.0,-0.4)}   # (dE, dAgua) nominal",
             etiqueta='tablas del mundo vivo')

    # ---- 2) firma ----
    s = sust(s, A_FIRMA, A_FIRMA[:-2] +
             ",vivo=0,n_nec=1,estims=None,costo_a=0.002,A_ini=1.0,val_esc=0,nec_shuf=0,hereda_nec=1,tabla=None,"
             "eta_pred=0.0,ema_pred=0.05,clip_e=3.0,k_sorp=0.0,crit_exp=0.5):",
             etiqueta='firma: perillas del mundo vivo')
    s = sust(s, "    rng=np.random.default_rng(seed)\n",
             "    if n_nec>1 and not vivo: raise SystemExit('MUNDO VIVO: n_nec>1 exige vivo=1 (la mordida debe tener consecuencia vectorial)')\n"
             "    rng=np.random.default_rng(seed)\n", etiqueta='guardia n_nec/vivo')

    # ---- 3) el valor pasa a MATRIZ (n_nec, ...). Con n_nec=1, Wp[0] es la misma vista 1-D ----
    s = sust(s, A_WPWN, A_WPWN.replace("Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX);",
                                       "Wp=np.zeros((n_nec,NKMAX)); Wn=np.zeros((n_nec,NKMAX));"),
             etiqueta='Wp/Wn -> (n_nec, NKMAX)')
    s = sust(s, A_LENTA,
             "    Wps=np.zeros((n_nec,6)); Wns=np.zeros((n_nec,6))   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0). VIVO: una fila por necesidad\n"
             "    _na=0; _nm=0   # VIVO: necesidad ACTIVA (manda boca y division) y la que INDEXA la memoria (val_esc -> siempre 0). Con n_nec=1 nunca cambian\n"
             "    _EF=dict(EFECTO) if tabla is None else dict(tabla)   # VIVO: (dE,dAg) por valencia; `tabla` sirve para el control 'estimulo que no informa'\n"
             "    _rng_n=np.random.default_rng(seed+900000) if nec_shuf else None   # CONTROL barajado: rng PROPIO (v13s), no toca el del organismo\n"
             "    Wpe=np.zeros((n_nec,6)); Wke=np.zeros((n_nec,NKMAX)); _sbE=np.zeros(n_nec)   # VIVO: predictor VECTORIAL de dS y SORPRESA POR NECESIDAD (inerte con eta_pred=0)\n"
             "    _enc={k:0 for k in PAT}; _exp=[{k:None for k in PAT} for _ in range(n_nec)]   # VIVO: exposiciones y EXPOSICIONES HASTA CRITERIO (solo lectura)\n"
             "    _mnec=[0,0]; _bxor=[[0]*4 for _ in range(n_nec)]; _exor=[[0]*4 for _ in range(n_nec)]   # VIVO: muertes [por energia, por agua] y tabla NECESIDAD x ESTIMULO (solo lectura)\n"
             "    _IDX={_k2:_i2 for _i2,_k2 in enumerate('ABCD')}\n",
             etiqueta='via lenta -> matriz + estado del mundo vivo')

    # ---- 4) la puerta y el valor leen la FILA de la necesidad ----
    s = sust(s, A_FAM,
             "    def _fam(_k,_n=None):   # B: la puerta. puerta_pat>0 -> evidencia del codigo exacto; si no, celdas consolidadas (v13 EXACTO). VIVO: lee la fila de la necesidad\n"
             "        _w=Wp[_nm if _n is None else _n]-Wn[_nm if _n is None else _n]\n"
             "        if puerta_pat: return _ev(_k)>=puerta_pat and int((np.abs(_w[_k>0])>0.2).sum())>=pat_min\n"
             "        return int((np.abs(_w[_k>0])>0.2).sum())>=puerta\n", etiqueta='_fam por necesidad')
    s = sust(s, A_VALOR, "        _k=kenyon(P); _f=float((Wp[_nm]-Wn[_nm])@_k); _s=float((Wps[_nm]-Wns[_nm])@P)\n",
             etiqueta='valor() por necesidad')
    s = sust(s, A_VALRET, A_VALRET +
             "    def _vnec(_n,P,_k):   # VIVO: el valor que la boca usaria para la necesidad _n (mismo ruteo que valor()). SOLO LECTURA\n"
             "        _f=float((Wp[_n]-Wn[_n])@_k); _s=float((Wps[_n]-Wns[_n])@P)\n"
             "        return _f+_s if puerta is None else (_f if _fam(_k,_n) else _s)\n", etiqueta='_vnec')

    # ---- 5) cuerpo: agua, valencias, estimulos presentes ----
    s = sust(s, A_POS, "    pos=0; E=1.0; Ag=A_ini; objs={}; val=(dict(VAL_VIVO) if vivo else {'A':'comida','B':'veneno'})\n",
             etiqueta='estado del cuerpo: agua y valencias')
    s = sust(s, A_TIPOS, "    tipos=(list(estims) if estims else ['A','B'])   # VIVO: con dos estimulos, spawn() sortea igual que v14\n"
             "    if vivo:   # VIVO: una entrada por valencia PRESENTE; con dos estimulos no se agrega ninguna -> los dicts son los de v14\n"
             "        for _v in ('agua','sal'):\n"
             "            if _v in [val[_t] for _t in tipos]: sobre[_v]=[0]*4; llegadas[_v]=[0]*4\n",
             etiqueta='estimulos presentes + valencias de agua y sal')

    # ---- 6) paso: la necesidad ACTIVA manda ----
    s = sust(s, A_HAMBRE,
             "        hambre=np.clip(1-E,0,1)\n"
             "        if n_nec>1:   # VIVO: deficit por necesidad; manda la ACTIVA (la mas deficitaria). Con n_nec=1 esta rama no existe\n"
             "            _dfa=np.clip(1-Ag,0,1); _na=1 if _dfa>hambre else 0\n"
             "            if _na: hambre=_dfa\n"
             "            if nec_shuf==1: _na=int(_rng_n.integers(n_nec))   # CONTROL 1: la POLITICA se baraja (la tabla de valor SOBREVIVE: cada fila sigue viendo su componente)\n"
             "            _nm=0 if val_esc else _na   # val_esc=1: UN escalar por celda para todas las necesidades (alternativa a refutar)\n"
             "        d,k,left=see(contar=True); pat=PAT[k]\n", etiqueta='necesidad activa')

    # ---- 7) boca ----
    s = sust(s, A_WB, "            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp[_nm]-Wn[_nm]; _wf=float(Wb@kc); "
             "_ws=float((Wps[_nm]-Wns[_nm])@PAT[kk])   # v13: las dos vias (VIVO: las de la necesidad activa)\n",
             etiqueta='boca: valor de la necesidad activa')
    s = sust(s, A_VB, A_VB.replace("mordio=rng.random()<pb\n", "mordio=rng.random()<pb\n").replace(
             "            Vb=alpha*_wt+hambre_boca*hambre+.5; ",
             "            Vb=alpha*_wt+hambre_boca*hambre+.5\n"
             "            if k_sorp: Vb+=k_sorp*float(_sbE[_na])   # VIVO: la SORPRESA DE LA NECESIDAD ACTIVA en la boca (la dosis de v15, ahora especifica)\n"
             "            "), etiqueta='boca: sorpresa por necesidad')
    s = sust(s, A_LLEG, A_LLEG +
             "            if vivo and _prev_on!=pos:   # VIVO: EXPOSICIONES (llegadas) y EXPOSICIONES HASTA CRITERIO, por necesidad. SOLO LECTURA\n"
             "                _enc[kk]+=1; _exor[_na][_IDX[kk]]+=1\n"
             "                for _n in range(n_nec):\n"
             "                    _s0=_EF[val[kk]][_n]\n"
             "                    if _s0 and _exp[_n][kk] is None:\n"
             "                        _v0=_vnec(_n,PAT[kk],kc)\n"
             "                        if _v0*_s0>0 and abs(_v0)>=crit_exp: _exp[_n][kk]=_enc[kk]\n",
             etiqueta='exposiciones hasta criterio')

    # ---- 8) la mordida tiene consecuencia VECTORIAL ----
    s = sust(s, A_MORD,
             "                if vivo:   # VIVO: la mordida tiene consecuencia VECTORIAL -> UN encuentro ensena a TODAS las necesidades\n"
             "                    _dS=_EF[val[kk]]; _Rv=[(1.0 if _x>0 else (-3.0 if _x<0 else 0.0)) for _x in _dS]\n"
             "                    if nec_shuf>1: _Rv=[_Rv[_i] for _i in _rng_n.permutation(n_nec)]   # CONTROL 2: se baraja QUE componente ENSENA a cada necesidad; el cuerpo recibe dS intacto\n"
             "                    R=_Rv[_na]; E=min(E+_dS[0],1.5); Ag=min(Ag+_dS[1],1.5); _bxor[_na][_IDX[kk]]+=1\n"
             "                else: _dS=(E_VAL[val[kk]],0.0); _Rv=[R_VAL[val[kk]]]; R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5)\n"
             "                mord[kk][q(t)]+=1\n", etiqueta='consecuencia vectorial de la mordida')

    # ---- 9) predictor VECTORIAL de dS (bloque 6 -> una salida por necesidad) ----
    s = sust(s, A_LEARN, A_LEARN +
             "                    if eta_pred:   # VIVO: predictor VECTORIAL de dS (el de allostasis); la SORPRESA es POR NECESIDAD. No toca el rng\n"
             "                        _dp=Wpe@PAT[kk]+Wke@kc; _ep=np.array(_dS[:n_nec])-_dp\n"
             "                        Wpe=np.clip(Wpe+eta_pred*np.outer(_ep,PAT[kk]),-clip_e,clip_e); Wke=np.clip(Wke+eta_pred*np.outer(_ep,kc),-clip_e,clip_e)\n"
             "                        _sbE=(1.-ema_pred)*_sbE+ema_pred*np.abs(_ep)   # causal: la usa la boca del PROXIMO encuentro\n",
             etiqueta='predictor vectorial')

    # ---- 10) aprendizaje de la necesidad ACTIVA: misma regla, sobre su fila ----
    s = sust(s, A_LENTAUPD,
             "                        if lam: _mcs=np.minimum(Wps[_nm],Wns[_nm])*(PAT[kk]>0); Wps[_nm]=Wps[_nm]-lam*_mcs; Wns[_nm]=Wns[_nm]-lam*_mcs\n"
             "                        if _ds>0: Wps[_nm]=np.clip(Wps[_nm]+eta_s*_ds*PAT[kk],0,clip_s)\n"
             "                        else:     Wns[_nm]=np.clip(Wns[_nm]+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)\n",
             etiqueta='via lenta: fila activa')
    s = sust(s, A_LAMIX,
             "                    if lam: ix=kc>0; mcom=np.minimum(Wp[_nm][ix],Wn[_nm][ix]); Wp[_nm][ix]-=lam*mcom; Wn[_nm][ix]-=lam*mcom"
             "   # BUG-01 exp2: decae solo la parte comun\n", etiqueta='drenaje: fila activa')
    s = sust(s, A_TRUNCA,
             "                    if dlt>0: _trunca=bool(((Wp[_nm][_ix]+eta*dlt)>3.0).any())\n"
             "                    else:     _trunca=bool(((Wn[_nm][_ix]+eta*aversion*(-dlt))>3.0).any())\n",
             etiqueta='truncacion: fila activa')
    s = sust(s, A_UPD,
             "                    if dlt>0: Wp[_nm]=np.clip(Wp[_nm]+eta*dlt*kc,0,3.)\n"
             "                    else:     Wn[_nm]=np.clip(Wn[_nm]+eta*aversion*(-dlt)*kc,0,3.)\n",
             etiqueta='actualizacion: fila activa')
    s = sust(s, A_CONF, "                    if t_conflicto is None and bool((np.minimum(Wp[_nm][_ix],Wn[_nm][_ix])>0).any()): t_conflicto=t\n"
             "                    if n_nec>1:   # VIVO: las OTRAS necesidades aprenden de SU componente del MISMO bocado (esto es lo que compra el mundo vivo)\n"
             "                        for _n in range(n_nec):\n"
             "                            if _n==_nm: continue\n"
             "                            _Rn=_Rv[_n]; _wfn=float((Wp[_n]-Wn[_n])@kc); _wsn=float((Wps[_n]-Wns[_n])@PAT[kk])\n"
             "                            _dn=_Rn-(_wfn+_wsn) if puerta is None else _Rn-_wfn\n"
             "                            if eta_s:\n"
             "                                _dsn=_dn if puerta is None else _Rn-_wsn\n"
             "                                if lam: _mn2=np.minimum(Wps[_n],Wns[_n])*(PAT[kk]>0); Wps[_n]=Wps[_n]-lam*_mn2; Wns[_n]=Wns[_n]-lam*_mn2\n"
             "                                if _dsn>0: Wps[_n]=np.clip(Wps[_n]+eta_s*_dsn*PAT[kk],0,clip_s)\n"
             "                                else:      Wns[_n]=np.clip(Wns[_n]+eta_s*aversion*(-_dsn)*PAT[kk],0,clip_s)\n"
             "                            if lam: _mc2=np.minimum(Wp[_n][_ix],Wn[_n][_ix]); Wp[_n][_ix]-=lam*_mc2; Wn[_n][_ix]-=lam*_mc2\n"
             "                            if _dn>0: Wp[_n]=np.clip(Wp[_n]+eta*_dn*kc,0,3.)\n"
             "                            else:     Wn[_n]=np.clip(Wn[_n]+eta*aversion*(-_dn)*kc,0,3.)\n",
             etiqueta='aprendizaje de las otras necesidades')

    # ---- 11) division: fision de la fila activa, herencia de las demas ----
    s = sust(s, A_FISION,
             "                                    if R>0: Wp[_nm,j]=Wp[_nm,c]; Wn[_nm,j]=0.; Wp[_nm,c]=0.\n"
             "                                    else:   Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.\n"
             "                                    if n_nec>1 and hereda_nec:   # VIVO: la hija HEREDA el valor de las OTRAS necesidades (la madre lo conserva); la fision es solo de la activa\n"
             "                                        for _n in range(n_nec):\n"
             "                                            if _n!=_nm: Wp[_n,j]=Wp[_n,c]; Wn[_n,j]=Wn[_n,c]\n",
             etiqueta='fision del valor por necesidad')
    s = sust(s, A_THETA,
             "                                Wp[:,j]=Wp[:,c]; Wn[:,j]=Wn[:,c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; "
             "splits+=1; split_t.append((t,kk))\n", etiqueta='camino theta (v10) por necesidad')

    # ---- 12) cuerpo: drenaje y DOS muertes ----
    s = sust(s, A_COSTO, "        E-=costo\n        if vivo: Ag-=costo_a   # VIVO: el agua tambien baja sola\n",
             etiqueta='drenaje del agua')
    s = sust(s, A_MUERTE,
             "        if E<=0 or (vivo and Ag<=0):   # VIVO: DOS muertes posibles (con vivo=0 la segunda es imposible: Ag=A_ini y no baja)\n"
             "            deaths+=1; _mnec[0 if E<=0 else 1]+=1; E=.6\n"
             "            if vivo: Ag=.6\n"
             "            pos=int(rng.integers(L))\n", etiqueta='dos muertes')

    # ---- 13) lecturas finales ----
    s = sust(s, A_WLENTA, "    W_lenta={k:round(float((Wps[_nm]-Wns[_nm])@PAT[k]),3) for k in PAT}   # v13: lectura de la via lenta sola\n",
             etiqueta='W_lenta por necesidad')
    s = sust(s, A_COMP, "    comp={k:(round(float(Wp[_nm]@kenyon(PAT[k])),2),round(float(Wn[_nm]@kenyon(PAT[k])),2)) for k in PAT}\n",
             etiqueta='comp por necesidad')
    s = sust(s, A_RET,
             "    _ext=(dict(n_nec=n_nec,estims=list(tipos),agua=round(float(Ag),3),muertes_nec=list(_mnec),\n"
             "               exp_hasta=[dict(_exp[_n]) for _n in range(n_nec)],exposiciones=dict(_enc),\n"
             "               W_nec=[{_k3:round(_vnec(_n,PAT[_k3],kenyon(PAT[_k3])),2) for _k3 in PAT} for _n in range(n_nec)],\n"
             "               xor_mord=[list(_bxor[_n]) for _n in range(n_nec)],xor_enc=[list(_exor[_n]) for _n in range(n_nec)],\n"
             "               sorp_nec=[round(float(_x),4) for _x in _sbE]) if vivo else {})   # VIVO: claves nuevas SOLO si vivo=1 (con vivo=0 el dict es el de v14, clave por clave)\n"
             + A_RET, etiqueta='dict extra del mundo vivo')
    s = sust(s, A_RETFIN, "W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps[_nm]],Wns=[round(float(x),3) for x in Wns[_nm]],**_ext)",
             etiqueta='return con las claves del mundo vivo')

    d = os.path.join(AQUI, 'organismo_vivo.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(CAB + s)
    print(f"  escrito {d}")
    print(f"  sha organismo_v14.py (origen, solo lectura) {SHA_V14}")
    print(f"  sha organismo_vivo.py                       {h16(d)}")
    print(f"  sha construye_vivo.py                       {h16(os.path.abspath(__file__))}")
    print("  siguiente: python experimentos/nivel11_mundo_vivo/identidad_vivo.py")
