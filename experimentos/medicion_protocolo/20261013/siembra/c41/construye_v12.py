"""Genera los instrumentos de v12 = v11 + ceguera GRADUADA de la hija (beta) + hija que MADURA (madura, u_madura).
Preregistro: PREREGISTRO_v12.md + ENMIENDA 1. Anclas con conteo exacto; origenes por sha.

  organismo_v12.py   <- organismo/organismo_v11.py (f69e24063be1b194)
  organismo_v12m.py  <- organismo_v12.py + instrumentacion de fases (anclas de v10m/v11m)
  organismo_v12g.py  <- organismo_v12.py + mundo de regla (anclas de v9g/v11g)

Con beta=0.0 y madura=False es v11 EXACTO; con div_signo=False es v10 EXACTO (controles I1 e I2).
  beta:   sintonia que la hija conserva FUERA de los pixeles de su patron. 0 = ciega (v11); 1 = sin ceguera.
  madura: si True, una HIJA (indice >= NK) deja de aprender para siempre cuando |Wp-Wn| >= u_madura.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
HELPERS = open(os.path.join(RAIZ, 'experimentos', 'etapa3_v9', 'construye_v9g.py'), encoding='utf-8').read()
HELPERS = HELPERS.split("HELPERS = '''", 1)[1].split("'''", 1)[0]


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


FIRMA_V11 = "memoria_rechazo=20,mu_norm=True,div_signo=True):"
FIRMA_V12 = "memoria_rechazo=20,mu_norm=True,div_signo=True,beta=0.0,madura=False,u_madura=1.0):"


def v12():
    s = origen(os.path.join(ORG, 'organismo_v11.py'), 'f69e24063be1b194')
    s = sust(s, FIRMA_V11, FIRMA_V12, etiqueta='firma')
    # estado nuevo: mascara de celdas congeladas (vacia si madura=False -> inercia exacta)
    ancla = "    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)\n"
    s = sust(s, ancla, ancla + "    _cong=np.zeros(NKMAX,bool); _es_hija=np.arange(NKMAX)>=NK   # v12: hijas congeladas al madurar (vacio si madura=False)\n",
             etiqueta='estado congelada')
    # la actualizacion RW salta las celdas congeladas (con madura=False, _kcu es kc)
    s = sust(s, "                    _ix=kc>0\n", "                    _kcu=kc*(~_cong) if madura else kc; _ix=_kcu>0   # v12: una hija madura ya no aprende\n",
             etiqueta='mascara de aprendizaje')
    s = sust(s, "                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom",
             "                    if lam: ix=(kc*(~_cong) if madura else kc)>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom",
             etiqueta='drenaje sin congeladas')
    s = sust(s, "                    if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())\n"
                "                    else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())\n",
             "                    if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())\n"
             "                    else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())\n", etiqueta='techo (sin cambio)')
    s = sust(s, "                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)\n"
                "                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)\n",
             "                    if dlt>0: Wp=np.clip(Wp+eta*dlt*(_kcu if madura else kc),0,3.)\n"
             "                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*(_kcu if madura else kc),0,3.)\n"
             "                    if madura: _cong|=_es_hija&(np.abs(Wp-Wn)>=u_madura)   # v12: la hija que consolido su valor deja de aprender\n",
             etiqueta='actualizacion y maduracion')
    # la perilla de ceguera
    s = sust(s, "if nuevo else None})", "if nuevo else None},congeladas=int(_cong.sum()),t_cong=_t_cong)   # v12: lectura",
             etiqueta='contador de congeladas')
    s = sust(s, "    _cong=np.zeros(NKMAX,bool); _es_hija=np.arange(NKMAX)>=NK",
             "    _cong=np.zeros(NKMAX,bool); _t_cong=None; _es_hija=np.arange(NKMAX)>=NK", etiqueta='marca de tiempo')
    s = sust(s, "                    if madura: _cong|=_es_hija&(np.abs(Wp-Wn)>=u_madura)   # v12: la hija que consolido su valor deja de aprender\n",
             "                    if madura:   # v12: la hija que consolido su valor deja de aprender\n"
             "                        _cong|=_es_hija&(np.abs(Wp-Wn)>=u_madura)\n"
             "                        if _t_cong is None and _cong.any(): _t_cong=t\n", etiqueta='marca de tiempo 2')
    s = sust(s, "                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*(P>0)",
             "                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*((P>0)+beta*(P==0))   # v12: beta = sintonia que conserva FUERA de P (0 = v11)",
             etiqueta='ceguera graduada')
    cab, cuerpo = s.split('"""\nimport numpy as np', 1)
    cab = ('"""\n'
           'Organismo v12 — INSTRUMENTO de la superficie del canje (no es tronco). Preregistro PREREGISTRO_v12.md.\n'
           '\n'
           'v12 = v11 + dos perillas:\n'
           '  beta   : sintonia que la hija conserva FUERA de los pixeles de su patron. beta=0 es v11 EXACTO (hija ciega);\n'
           '           beta=1 es la regla de v11 SIN ceguera (no es v10: el disparo por signo, la madre fija y la fision siguen).\n'
           '  madura : si True, una HIJA deja de aprender para siempre cuando |Wp-Wn| >= u_madura (rama hija-madura).\n'
           'Con div_signo=False es v10 EXACTO; con mu_norm=False y div_signo=False, v9 EXACTO.\n'
           'Generado por experimentos/v12_ceguera_graduada/construye_v12.py. NO editar a mano.\n')
    d = os.path.join(AQUI, 'organismo_v12.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + '"""\nimport numpy as np' + cuerpo)
    return d


def v12m():
    s = open(os.path.join(AQUI, 'organismo_v12.py'), encoding='utf-8').read()
    s = sust(s, FIRMA_V12, FIRMA_V12[:-2] + ",fases=None,congelar=None,estado_inicial=None,heredar_patas=True,devolver_estado=False):",
             etiqueta='firma')
    ancla = ("    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; "
             "el=np.zeros_like(Wl); tr=np.zeros(9)\n")
    s = sust(s, ancla, ancla +
        "    if estado_inicial is not None:   # v12m: herencia\n"
        "        KW[:]=estado_inicial['KW']; activa[:]=estado_inicial['activa']; Wp[:]=estado_inicial['Wp']; Wn[:]=estado_inicial['Wn']\n"
        "        err[:]=estado_inicial['err']; mu[:]=estado_inicial['mu']\n"
        "        if heredar_patas: Wl[:]=estado_inicial['Wl']\n"
        "    sondas={}; codigos={}; primer={}; _t_fase=0; dq=[0]*4   # v12m: lectura\n", etiqueta='herencia')
    ancla = "        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val\n"
    s = sust(s, ancla, ancla +
        "        if fases is not None and t in fases:   # v12m: cambio del conjunto de estimulos\n"
        "            tipos[:]=list(fases[t][0]); val.update(fases[t][1]); _t_fase=t\n"
        "            for _x in [_xx for _xx,_kz in list(objs.items()) if _kz not in tipos]: del objs[_x]; _rech.pop(_x,None)\n"
        "            spawn(); sondas[t]={_k:float((Wp-Wn)@kenyon(PAT[_k])) for _k in PAT}\n"
        "            codigos[t]={_k:sorted(int(_i) for _i in code(PAT[_k])) for _k in PAT}\n"
        "        _ap=learn and not (congelar is not None and congelar[0]<=t<congelar[1])   # v12m\n", etiqueta='fases')
    s = sust(s, "if learn:", "if _ap:", n=3, etiqueta='compuerta de aprendizaje')
    ancla = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
    s = sust(s, ancla, ancla +
        "            if (_t_fase,kk) not in primer: primer[(_t_fase,kk)]=dict(t=t,W=float(Wb@kc),pb=float(pb),mordio=bool(mordio))   # v12m\n",
        etiqueta='primer encuentro')
    s = sust(s, "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))\n",
             "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L)); dq[q(t)]+=1\n", etiqueta='muertes por cuarto')
    s = sust(s, "congeladas=int(_cong.sum()),t_cong=_t_cong)",
             "congeladas=int(_cong.sum()),t_cong=_t_cong,sondas=sondas,codigos=codigos,primer={f'{_a}|{_b}':_v for (_a,_b),_v in primer.items()},dq=dq,"
             "estado=(dict(KW=KW.copy(),activa=activa.copy(),Wp=Wp.copy(),Wn=Wn.copy(),err=err.copy(),mu=mu.copy(),Wl=Wl.copy()) "
             "if devolver_estado else None))", etiqueta='return')
    cab = ('"""organismo_v12m = organismo_v12.py + fases, sondas de W y de CODIGOS, herencia y primer encuentro\n'
           '(mismas anclas que v10m y v11m). Generado por construye_v12.py. NO editar.\n'
           'Con beta=0 y madura=False es v11m exacto."""\n')
    d = os.path.join(AQUI, 'organismo_v12m.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    return d


def v12g():
    src = open(os.path.join(AQUI, 'organismo_v12.py'), encoding='utf-8').read()
    cab, cuerpo = src.split("def run(", 1)
    cuerpo = "def run(" + cuerpo
    cab = cab + HELPERS.lstrip('\n')
    n_pat = cuerpo.count("PAT")
    if n_pat != 21:
        raise SystemExit(f"PAT aparece {n_pat} veces en run(), se esperaban 21. Abortado.")
    cuerpo = cuerpo.replace("PAT", "P_")
    cuerpo = sust(cuerpo, FIRMA_V12, FIRMA_V12[:-2] + ",mundo='AB',regla='px0',fase2_en=None,sonda_final=False):", etiqueta='firma')
    ancla = "    rng=np.random.default_rng(seed)\n"
    cuerpo = sust(cuerpo, ancla,
        "    if mundo=='AB': P_=PAT; tren=['A','B']; test=[]   # v12g: con 'AB' es v12 exacto\n"
        "    else: P_,tren,test,val_regla=split_regla(seed,regla); fase2_en=T//2 if fase2_en is None else fase2_en\n" + ancla,
        etiqueta='mundo')
    cuerpo = sust(cuerpo, "    while not cond(): KW[objetivo_AB:NK]=", "    while mundo=='AB' and not cond(): KW[objetivo_AB:NK]=",
                  etiqueta='rechazo solo en AB')
    cuerpo = sust(cuerpo, "pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}\n",
                  "pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'} if mundo=='AB' else dict(val_regla)\n", etiqueta='val')
    cuerpo = sust(cuerpo, "    tipos=['A','B']\n",
                  "    tipos=['A','B'] if mundo=='AB' else list(tren)\n"
                  "    W_apriori=None; codigos_f2=None; primer={}   # v12g: sonda y primer encuentro (lectura)\n", etiqueta='tipos')
    ancla = "        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val\n"
    cuerpo = sust(cuerpo, ancla, ancla +
        "        if mundo!='AB' and t==fase2_en:   # v12g: sonda a priori y entrada de los de test\n"
        "            _Wb=Wp-Wn; W_apriori={_k:float(_Wb@kenyon(P_[_k])) for _k in P_}\n"
        "            codigos_f2={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}\n"
        "            tipos.extend(test); primer={_k:None for _k in test}\n", etiqueta='fase 2')
    ancla = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
    cuerpo = sust(cuerpo, ancla, ancla +
        "            if kk in primer and primer[kk] is None: primer[kk]=dict(t=t,W=float(Wb@kc),pb=float(pb),hambre=float(hambre),mordio=bool(mordio))   # v12g\n",
        etiqueta='primer encuentro')
    ancla = "    W={k:round(float((Wp-Wn)@kenyon(P_[k])),2) for k in P_}\n"
    cuerpo = sust(cuerpo, ancla,
        "    _sonda=None; _cod_fin=None\n"
        "    if sonda_final:   # v12g: sonda final de 64 patrones\n"
        "        _Wb=Wp-Wn; _sonda={}\n"
        "        for _n in range(64):\n"
        "            _P=np.array([(_n>>(5-_j))&1 for _j in range(6)],float); _nm=''.join(str(int(_v)) for _v in _P)\n"
        "            _sonda[_nm]=dict(W=float(_Wb@kenyon(_P)),codigo=sorted(int(_i) for _i in code(_P)))\n"
        "        _cod_fin={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}\n" + ancla, etiqueta='sonda final')
    cuerpo = sust(cuerpo, "                solap={'AB':", "                solap=None if mundo!='AB' else {'AB':", etiqueta='solap')
    cuerpo = sust(cuerpo, "congeladas=int(_cong.sum()),t_cong=_t_cong)",
                  "congeladas=int(_cong.sum()),t_cong=_t_cong,mundo=mundo,regla=regla,tren=tren,test=test,W_apriori=W_apriori,codigos_f2=codigos_f2,"
                  "primer=primer,W_final=({_k:float((Wp-Wn)@kenyon(P_[_k])) for _k in P_} if mundo!='AB' else None),"
                  "sonda=_sonda,codigos_fin=_cod_fin)", etiqueta='return')
    cabecera = ('"""organismo_v12g = organismo_v12.py + mundo de regla, sonda a priori, primer encuentro y sonda final\n'
                '(mismas anclas que v9g y v11g). Generado por construye_v12.py. NO editar.\n'
                "Con beta=0, madura=False y mundo='regla' es organismo_v11g exacto.\n"
                '"""\n')
    d = os.path.join(AQUI, 'organismo_v12g.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cabecera + cab + cuerpo)
    return d


if __name__ == '__main__':
    for f in (v12, v12m, v12g):
        d = f()
        print(f"  {os.path.relpath(d, RAIZ):52s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
