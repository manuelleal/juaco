"""CREADOR C — constructor POR ANCLAS del instrumento de AUTOMODELO (modelo de si mismo minimo).

  organismo_v13s.py <- organismo/organismo_v13.py   (cc8b16b492d4d324, TRONCO CONGELADO: se lee, NO se toca)

Que anade (y nada mas):
  - TRES lecturas logisticas que predicen la PROPIA ACCION del organismo (morder / no morder) en cada encuentro con un
    objeto, cada una con regla delta local sobre la accion realizada:
        SELF  : b = sig((Wbr@P + Wbk@kenyon(P) + Wbh*hambre + Wb0)/0.3)   <- ve su estado interno
        MUNDO : b = sig((Wmr@P + Wmk@kenyon(P)          + Wm0)/0.3)       <- control: SOLO el estimulo
        H_SHUF: b = sig((Whr@P + Whk@kenyon(P) + Whh*h~ + Wh0)/0.3)       <- control: hambre BARAJADA en el tiempo
    Las tres viajan en LA MISMA corrida sobre LOS MISMOS encuentros: la comparacion es pareada por construccion.
  - SORPRESA SOBRE SI MISMO  s_a = |mordio - b_SELF|  y, opcionalmente, la modulacion
        eta_ef = eta*(1 + k_auto*s_a)   sobre la via RAPIDA (y sobre el predicado _trunca, para no mentir en la
        instrumentacion), exactamente como el bloque 6 hace con la sorpresa de dE.
  - Lecturas separadas DENTRO y FUERA de la banda sensible al hambre, derivada de las constantes del propio organismo:
        |alpha*w + hambre_boca*h + 0.5| <= 0.9  para algun h en [0,1]
        =>  w en [ (-0.9-0.5-hambre_boca)/alpha , (0.9-0.5)/alpha ]   (con v13: [-2.8333, +0.3333])
    Fuera de esa banda el hambre NO puede cambiar la decision (sig(+-3) = 0.953/0.047): ahi el automodelo no puede
    ganarle al modelo del mundo. Es la prediccion que distingue "modelo de si mismo" de "predictor del mundo".

Identidades que hacen valida la lectura:
  I1  eta_b=0, k_auto=0            == organismo_v13  (bit a bit, todas las claves de v13)
  I2  eta_b>0, k_auto=0            == organismo_v13  (bit a bit): las tres lecturas SOLO MIDEN
      (el control H_SHUF usa un Generator PROPIO, seed+800000; no toca el rng del organismo)

NO editar el generado a mano.  Uso:  python experimentos/creacion_C/construye_selfmodel.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
NL = chr(10)

SHA_V13 = 'cc8b16b492d4d324'


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def origen(p, sha):
    real = h16(p)
    if real != sha:
        raise SystemExit(f"ORIGEN {p}: sha {real}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


CAB = '"""organismo_v13s = organismo/organismo_v13.py (cc8b16b492d4d324, TRONCO) + AUTOMODELO MINIMO:\n' \
      'tres lecturas logisticas que predicen la PROPIA ACCION (morder/no morder) en cada encuentro, con regla delta\n' \
      'local sobre la accion realizada: SELF (retina + codigo + HAMBRE), MUNDO (control: solo el estimulo) y H_SHUF\n' \
      '(control: hambre barajada en el tiempo, RNG propio seed+800000). Las tres viajan en la misma corrida sobre los\n' \
      'mismos encuentros. Sorpresa sobre si mismo s_a = |mordio - b_SELF|; con k_auto>0 modula eta de la via RAPIDA.\n' \
      'Con eta_b=0 y k_auto=0 es v13 EXACTO (I1). Con eta_b>0 y k_auto=0 las lecturas SOLO MIDEN y la conducta es la\n' \
      'de v13 bit a bit (I2). Banda sensible al hambre derivada de las constantes: [(-1.4-hambre_boca)/alpha, 0.4/alpha].\n' \
      'Generado por experimentos/creacion_C/construye_selfmodel.py. NO editar. RAMA de creacion: no es tronco.\n"""\n'

PERILLAS = "eta_b=0.0,k_auto=0.0,ema_auto=0.0,k_test=0.0,test_fijo=0.0,buf_auto=1000,clip_b=3.0,eta_e=0.0,h_pred=100,buf_e=200"

ESTADO = [
    "    Wbr=np.zeros(6); Wbk=np.zeros(NKMAX); Wbh=0.; Wb0=0.   # v13s: AUTOMODELO (SELF) — predice la propia accion desde retina+codigo+HAMBRE",
    "    Wmr=np.zeros(6); Wmk=np.zeros(NKMAX); Wm0=0.           # v13s: control MUNDO — lo mismo SIN hambre (solo el estimulo)",
    "    Whr=np.zeros(6); Whk=np.zeros(NKMAX); Whh=0.; Wh0=0.   # v13s: control H_SHUF — hambre barajada en el tiempo",
    "    _rng_h=np.random.default_rng(seed+800000) if (eta_b or eta_e) else None; _bufh=[]; _bufe=[]   # v13s: RNG PROPIO de los controles (no toca el del organismo)",
    "    _BLO=(-0.9-0.5-hambre_boca)/alpha; _BHI=(0.9-0.5)/alpha   # v13s: banda sensible al hambre, derivada de las constantes",
    "    _LL=np.zeros((4,2)); _HIT=np.zeros((4,2,2)); _NC=np.zeros((2,2)); _aq=[0.]*4; _naq=[0]*4; _encq=[0]*4   # v13s: lecturas [S,M,H,ORACULO] x [dentro,fuera] x [no muerde,muerde]",
    "    _tq=[0.]*4   # v13s: sesgo medio aplicado a la boca por cuarto",
    "    _sbar=0.; _etaq=[0.]*4; _nqm=[0]*4; t_ext_B=None; deaths_post=0   # v13s: sorpresa media sobre si mismo (EMA), factor eta por cuarto EN LOS BOCADOS, y recuperacion tras la inversion (mismo criterio que el bloque 6)",
    "    Wem=np.zeros((2,7)); bem=np.zeros(2); Wes=np.zeros((2,8)); bes=np.zeros(2); bec=np.zeros(2)   # v13s: AUTOMODELO A h PASOS, dos objetivos: [dE, n_bocados]",
    "    Wez=np.zeros((2,8)); bez=np.zeros(2)   # v13s: control SELF_h con el HAMBRE BARAJADA entre ventanas (misma distribucion, momento equivocado)",
    "    _xe=None; _Ee=0.; _nbw=0; _SE=np.zeros((2,4)); _ne=0; _sy=np.zeros(2); _sy2=np.zeros(2)   # v13s: [objetivo] x [CONST, MUNDO, SELF, SELF_SHUF]",
]

BLOQUE = [
    "            _sa=0.",
    "            if eta_b:   # v13s: AUTOMODELO — tres lecturas que SOLO MIDEN (no entran en la decision ni consumen el rng del organismo)",
    "                _hh=hambre",
    "                _bufh.append(hambre)",
    "                if len(_bufh)>buf_auto: _hh=float(_bufh.pop(int(_rng_h.integers(len(_bufh)))))   # H_SHUF: misma distribucion de hambre, momentos equivocados",
    "                _Pb={pat}[kk]",
    "                _bS=1/(1+np.exp(-(float(Wbr@_Pb)+float(Wbk@kc)+Wbh*hambre+Wb0)/.3))",
    "                _bM=1/(1+np.exp(-(float(Wmr@_Pb)+float(Wmk@kc)+Wm0)/.3))",
    "                _bH=1/(1+np.exp(-(float(Whr@_Pb)+float(Whk@kc)+Whh*_hh+Wh0)/.3))",
    "                _y=1. if mordio else 0.; _sa=abs(_y-_bS); _bd=0 if (_BLO<=_wt<=_BHI) else 1; _cl=int(_y)",
    "                for _i,_bb in enumerate((_bS,_bM,_bH,pb)):   # el 4o es el ORACULO: la propia pb que genero la accion (log-loss irreducible)",
    "                    _LL[_i,_bd]-=np.log(max(_bb if _y>0 else 1-_bb,1e-12)); _HIT[_i,_bd,_cl]+=int((_bb>.5)==(_y>0))",
    "                _NC[_bd,_cl]+=1; _aq[q(t)]+=_sa; _naq[q(t)]+=1",
    "                _eS=_y-_bS; _eM=_y-_bM; _eH=_y-_bH",
    "                Wbr=np.clip(Wbr+eta_b*_eS*_Pb,-clip_b,clip_b); Wbk=np.clip(Wbk+eta_b*_eS*kc,-clip_b,clip_b); Wbh=float(np.clip(Wbh+eta_b*_eS*hambre,-clip_b,clip_b)); Wb0=float(np.clip(Wb0+eta_b*_eS,-clip_b,clip_b))",
    "                Wmr=np.clip(Wmr+eta_b*_eM*_Pb,-clip_b,clip_b); Wmk=np.clip(Wmk+eta_b*_eM*kc,-clip_b,clip_b); Wm0=float(np.clip(Wm0+eta_b*_eM,-clip_b,clip_b))",
    "                Whr=np.clip(Whr+eta_b*_eH*_Pb,-clip_b,clip_b); Whk=np.clip(Whk+eta_b*_eH*kc,-clip_b,clip_b); Whh=float(np.clip(Whh+eta_b*_eH*_hh,-clip_b,clip_b)); Wh0=float(np.clip(Wh0+eta_b*_eH,-clip_b,clip_b))",
    "            if ema_auto: _sbar=(1.-ema_auto)*_sbar+ema_auto*_sa   # v13s: sorpresa media sobre si mismo — usa TODOS los encuentros, no solo los bocados",
    "            _eta=eta*(1.+k_auto*(_sbar if ema_auto else _sa)) if k_auto else eta   # v13s: CURRICULO POR EL CUERPO — la sorpresa sobre SI MISMO modula la tasa de la via rapida",
    "            _encq[q(t)]+=1; _tq[q(t)]+=(k_test*_sbar if k_test else 0.)+test_fijo",
]

BLOQUE_H = [
    "        if eta_e and t%h_pred==0:   # v13s: AUTOMODELO A h PASOS — cierra la ventana anterior (y = [E(t)-E(t-h), bocados]) y abre otra. SOLO MIDE",
    "            _xs=np.concatenate([pat,[1. if d==0 else 0.],[hambre]])   # [retina(6), sobre un objeto] + HAMBRE (el ultimo SOLO lo ven SELF_h y su control)",
    "            if _xe is not None:",
    "                _xz=_xe.copy(); _bufe.append(_xe[7])",
    "                if len(_bufe)>buf_e: _xz[7]=float(_bufe.pop(int(_rng_h.integers(len(_bufe)))))   # SELF_SHUF: hambre de OTRA ventana",
    "                _ye=np.array([E-_Ee,float(_nbw)])",
    "                _pr=np.stack([bec,Wem@_xe[:7]+bem,Wes@_xe+bes,Wez@_xz+bez],axis=1)   # [objetivo] x [C,M,S,Z]",
    "                _SE+=(_ye[:,None]-_pr)**2; _ne+=1; _sy+=_ye; _sy2+=_ye*_ye",
    "                bec=bec+eta_e*(_ye-_pr[:,0])",
    "                _em=_ye-_pr[:,1]; Wem=Wem+eta_e*np.outer(_em,_xe[:7]); bem=bem+eta_e*_em",
    "                _es=_ye-_pr[:,2]; Wes=Wes+eta_e*np.outer(_es,_xe);     bes=bes+eta_e*_es",
    "                _ez=_ye-_pr[:,3]; Wez=Wez+eta_e*np.outer(_ez,_xz);     bez=bez+eta_e*_ez",
    "            _xe=_xs; _Ee=E; _nbw=0",
]

SALIDA = [
    "                auto_banda=(round(float(_BLO),4),round(float(_BHI),4)),",
    "                t_ext_B=t_ext_B,deaths_post=deaths_post,sbar=round(float(_sbar),5),",
    "                sesgo_boca=[round(_tq[i]/_encq[i],5) if _encq[i] else None for i in range(4)],",
    "                eta_media=[round(_etaq[i]/_nqm[i],4) if _nqm[i] else None for i in range(4)],bocados_q=list(_nqm),",
    "                auto_h=({'n':int(_ne),'h':int(h_pred),",
    "                         'mse':[[round(float(_SE[y,i]/_ne),6) for i in range(4)] for y in range(2)],",
    "                         'r2':[[round(float(1-_SE[y,i]/max(_SE[y,0],1e-12)),4) for i in range(4)] for y in range(2)],",
    "                         'var_y':[round(float(_sy2[y]/_ne-(_sy[y]/_ne)**2),6) for y in range(2)],",
    "                         'media_y':[round(float(_sy[y]/_ne),6) for y in range(2)],",
    "                         'W_hambre':[round(float(Wes[y,7]),4) for y in range(2)],",
    "                         'W_hambre_shuf':[round(float(Wez[y,7]),4) for y in range(2)]} if (eta_e and _ne) else None),",
    "                auto_n=[[int(_NC[b,c]) for c in range(2)] for b in range(2)],",
    "                auto_ll=[[round(float(_LL[i,b]/_NC[b].sum()),4) if _NC[b].sum() else None for b in range(2)] for i in range(4)],",
    "                auto_ba=[[round(float(np.mean([_HIT[i,b,c]/_NC[b,c] for c in range(2) if _NC[b,c]])),4) if _NC[b].sum() else None for b in range(2)] for i in range(4)],",
    "                sorpresa_auto=[round(_aq[i]/_naq[i],4) if _naq[i] else None for i in range(4)],",
    "                encuentros=list(_encq),n_auto=list(_naq),",
    "                W_auto=({k:round(float(1/(1+np.exp(-(float(Wbr@{pat}[k])+float(Wbk@kenyon({pat}[k]))+Wb0)/.3))),3) for k in {pat}} if eta_b else None),",
    "                Wbh=round(float(Wbh),4),Whh=round(float(Whh),4),Wb0=round(float(Wb0),4),Wm0=round(float(Wm0),4),",
]


def construye(src_rel, dst_rel, sha, pat):
    src = os.path.join(RAIZ, src_rel)
    txt = origen(src, sha)

    # 1) cabecera
    fin = txt.index('"""', 3) + 3
    txt = CAB + txt[fin:].lstrip(NL)

    # 2) perillas nuevas en la firma
    txt = sust(txt, "eta_s=0.015,clip_s=3.0,puerta=3):", f"eta_s=0.015,clip_s=3.0,puerta=3,{PERILLAS}):",
               etiqueta='firma')

    # 3) estado nuevo, justo tras la via lenta
    ancla_estado = "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)"
    txt = sust(txt, ancla_estado, ancla_estado + NL + NL.join(ESTADO), etiqueta='estado')

    # 4) bloque del automodelo, justo tras el sorteo de la accion
    ancla_mordio = "            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb"
    nueva_boca = ("            Vb=alpha*_wt+hambre_boca*hambre+.5+(k_test*_sbar if k_test else 0.)+test_fijo   "
                  "# v13s: GANAS DE PROBAR — la sorpresa sobre SI MISMO (EMA de encuentros anteriores, causal) entra en la BOCA, no en eta" + NL +
                  "            pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb")
    bloque = NL.join(l.replace('{pat}', pat) for l in BLOQUE)
    txt = sust(txt, ancla_mordio, nueva_boca + NL + bloque, etiqueta='mordio')

    # 4b) automodelo a h pasos, justo tras leer la retina y el hambre del paso (fuera del encuentro)
    ancla_h = "        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k]"
    txt = sust(txt, ancla_h, ancla_h + NL + NL.join(BLOQUE_H), etiqueta='paso')

    # 4c) contador de bocados de la ventana (segundo objetivo del automodelo a h pasos)
    ancla_nb = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1"
    txt = sust(txt, ancla_nb, ancla_nb + "; _nbw+=1; _etaq[q(t)]+=_eta/eta; _nqm[q(t)]+=1", etiqueta='nbw')

    # 4d) recuperacion tras la inversion (M1 del bloque 6, mismo criterio; no consume RNG)
    ancla_r = "        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas"
    txt = sust(txt, ancla_r,
               "        if invertir_en is not None and t>=invertir_en and t_ext_B is None and valor(PAT['B'])>=0: t_ext_B=t   # v13s: M1 del bloque 6" + NL + ancla_r,
               etiqueta='t_ext_B')
    ancla_d = "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))"
    txt = sust(txt, ancla_d,
               "        if E<=0:" + NL + "            deaths+=1; E=.6; pos=int(rng.integers(L))" + NL +
               "            if invertir_en is not None and t>=invertir_en: deaths_post+=1   # v13s", etiqueta='deaths_post')

    # 5) eta -> _eta en las CUATRO apariciones de la via rapida (2 del predicado _trunca, 2 de la actualizacion)
    txt = sust(txt, "if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())",
               "if dlt>0: _trunca=bool(((Wp[_ix]+_eta*dlt)>3.0).any())", etiqueta='trunca+')
    txt = sust(txt, "else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())",
               "else:     _trunca=bool(((Wn[_ix]+_eta*aversion*(-dlt))>3.0).any())", etiqueta='trunca-')
    txt = sust(txt, "if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)",
               "if dlt>0: Wp=np.clip(Wp+_eta*dlt*kc,0,3.)", etiqueta='Wp')
    txt = sust(txt, "else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)",
               "else:     Wn=np.clip(Wn+_eta*aversion*(-dlt)*kc,0,3.)", etiqueta='Wn')

    # 6) salidas nuevas
    ancla_sal = "W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns])"
    salida = NL.join(l.replace('{pat}', pat) for l in SALIDA)
    txt = sust(txt, ancla_sal,
               ancla_sal[:-1] + "," + NL + salida.rstrip(',') + ")", etiqueta='salida')

    dst = os.path.join(RAIZ, dst_rel)
    open(dst, 'w', encoding='utf-8', newline=NL).write(txt)
    print(f"  {dst_rel}  sha {h16(dst)}  ({len(txt.splitlines())} lineas)")


if __name__ == '__main__':
    print("Constructor por anclas — AUTOMODELO (creador C)")
    print(f"  origen organismo/organismo_v13.py  sha {SHA_V13} OK")
    construye('organismo/organismo_v13.py', 'experimentos/creacion_C/organismo_v13s.py', SHA_V13, 'PAT')
    print("Listo. Identidades: python experimentos/creacion_C/identidad_selfmodel.py")
