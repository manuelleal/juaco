"""Genera los instrumentos de v13 = v11 + VIA LENTA lineal sobre la retina (eta_s). Preregistro: PREREGISTRO_v13.md.
Anclas con conteo exacto; origenes por sha.

  organismo_v13.py   <- organismo/organismo_v11.py (f69e24063be1b194)
  organismo_v13m.py  <- organismo_v13.py + fases (anclas de v10m/v11m/v12m), sondas con el valor TOTAL
  organismo_v13g.py  <- organismo_v13.py + mundo de regla (anclas de v9g/v11g/v12g), W_apriori con el valor TOTAL

valor(P) = (Wp-Wn)@kenyon(P) + (Wps-Wns)@P ; un solo error dlt = R - valor para las dos vias.
Con eta_s=0 la via lenta queda en cero y v13 es v11 EXACTO (control de inercia; sumar 0.0 es exacto en coma flotante).
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
FIRMA_V13 = "memoria_rechazo=20,mu_norm=True,div_signo=True,eta_s=0.0,clip_s=3.0,puerta=None):"
VALOR = ("    def valor(P):   # v13: el valor que usa la boca. Sin puerta: rapida+lenta (un error). Con puerta: la rapida si el patron le es FAMILIAR, si no la lenta\n"
         "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)\n"
         "        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)   # familiar = >= puerta celdas del codigo con valor consolidado (|W|>0.2, el mismo umbral de v11)\n")


def v13():
    s = origen(os.path.join(ORG, 'organismo_v11.py'), 'f69e24063be1b194')
    s = sust(s, FIRMA_V11, FIRMA_V13, etiqueta='firma')
    ancla = "    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)\n"
    s = sust(s, ancla, ancla +
        "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)\n"
        + VALOR, etiqueta='estado via lenta')
    s = sust(s, "            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn\n"
                "            Vb=alpha*(Wb@kc)+hambre_boca*hambre+.5;",
             "            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@PAT[kk])   # v13: las dos vias\n"
             "            _wt=_wf+_ws if puerta is None else (_wf if int((np.abs(Wb[kc>0])>0.2).sum())>=puerta else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)\n"
             "            Vb=alpha*_wt+hambre_boca*hambre+.5;", etiqueta='boca')
    s = sust(s, "                    dlt=R-Wb@kc\n",
             "                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo\n"
             "                    if eta_s:   # v13: actualizacion de la via lenta (su tasa, mismo drenaje)\n"
             "                        _ds=dlt if puerta is None else R-_ws\n"
             "                        if lam: _mcs=np.minimum(Wps,Wns)*(PAT[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs\n"
             "                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*PAT[kk],0,clip_s)\n"
             "                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)\n", etiqueta='error unico')
    s = sust(s, "        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(float((Wp-Wn)@kenyon(PAT[k])),2) for k in 'ABCD'))\n",
             "        if log_cada and t%log_cada==0: log.append((t,)+tuple(round(valor(PAT[k]),2) for k in 'ABCD'))\n", etiqueta='log')
    s = sust(s, "    W={k:round(float((Wp-Wn)@kenyon(PAT[k])),2) for k in PAT}\n",
             "    W={k:round(valor(PAT[k]),2) for k in PAT}   # v13: valor total\n"
             "    W_lenta={k:round(float((Wps-Wns)@PAT[k]),3) for k in PAT}   # v13: lectura de la via lenta sola\n", etiqueta='W')
    s = sust(s, "if nuevo else None})", "if nuevo else None},W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns])",
             etiqueta='return')
    cab, cuerpo = s.split('"""\nimport numpy as np', 1)
    cab = ('"""\n'
           'Organismo v13 — CANDIDATO (no es tronco): v11 + VIA LENTA lineal sobre la retina. Preregistro PREREGISTRO_v13.md.\n'
           '\n'
           'Dos vias con UN solo error (esquema CLS minimo): la rapida es v11 sin tocar (Kenyon + division por conflicto de\n'
           'signo); la lenta es una lectura lineal directa de los 6 pixeles con dos canales Wps/Wns (>=0, tope clip_s) a tasa\n'
           'eta_s < eta, con el mismo drenaje de la parte comun. valor(P) = (Wp-Wn)@kenyon(P) + (Wps-Wns)@P; la boca decide\n'
           'con ese valor y dlt = R - valor entrena a las dos. Con eta_s=0 es v11 EXACTO.\n'
           'Generado por experimentos/v13_dos_vias/construye_v13.py. NO editar a mano.\n')
    d = os.path.join(AQUI, 'organismo_v13.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + '"""\nimport numpy as np' + cuerpo)
    return d


def v13m():
    s = open(os.path.join(AQUI, 'organismo_v13.py'), encoding='utf-8').read()
    s = sust(s, FIRMA_V13, FIRMA_V13[:-2] + ",fases=None,congelar=None,estado_inicial=None,heredar_patas=True,devolver_estado=False):",
             etiqueta='firma')
    ancla = VALOR
    s = sust(s, ancla, ancla +
        "    if estado_inicial is not None:   # v13m: herencia\n"
        "        KW[:]=estado_inicial['KW']; activa[:]=estado_inicial['activa']; Wp[:]=estado_inicial['Wp']; Wn[:]=estado_inicial['Wn']\n"
        "        err[:]=estado_inicial['err']; mu[:]=estado_inicial['mu']\n"
        "        if heredar_patas: Wl[:]=estado_inicial['Wl']\n"
        "    sondas={}; codigos={}; primer={}; _t_fase=0; dq=[0]*4   # v13m: lectura\n", etiqueta='herencia')
    ancla = "        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val\n"
    s = sust(s, ancla, ancla +
        "        if fases is not None and t in fases:   # v13m: cambio del conjunto de estimulos\n"
        "            tipos[:]=list(fases[t][0]); val.update(fases[t][1]); _t_fase=t\n"
        "            for _x in [_xx for _xx,_kz in list(objs.items()) if _kz not in tipos]: del objs[_x]; _rech.pop(_x,None)\n"
        "            spawn(); sondas[t]={_k:valor(PAT[_k]) for _k in PAT}   # v13m: valor TOTAL\n"
        "            codigos[t]={_k:sorted(int(_i) for _i in code(PAT[_k])) for _k in PAT}\n"
        "        _ap=learn and not (congelar is not None and congelar[0]<=t<congelar[1])   # v13m\n", etiqueta='fases')
    s = sust(s, "if learn:", "if _ap:", n=3, etiqueta='compuerta de aprendizaje')
    ancla = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
    s = sust(s, ancla, ancla +
        "            if (_t_fase,kk) not in primer: primer[(_t_fase,kk)]=dict(t=t,W=_wt,pb=float(pb),mordio=bool(mordio))   # v13m: valor TOTAL\n",
        etiqueta='primer encuentro')
    s = sust(s, "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))\n",
             "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L)); dq[q(t)]+=1\n", etiqueta='muertes por cuarto')
    s = sust(s, "Wns=[round(float(x),3) for x in Wns])",
             "Wns=[round(float(x),3) for x in Wns],sondas=sondas,codigos=codigos,primer={f'{_a}|{_b}':_v for (_a,_b),_v in primer.items()},dq=dq,"
             "estado=(dict(KW=KW.copy(),activa=activa.copy(),Wp=Wp.copy(),Wn=Wn.copy(),err=err.copy(),mu=mu.copy(),Wl=Wl.copy()) "
             "if devolver_estado else None))", etiqueta='return')
    cab = ('"""organismo_v13m = organismo_v13.py + fases, sondas (valor TOTAL rapida+lenta), herencia y primer encuentro\n'
           '(mismas anclas que v10m/v11m/v12m). Generado por construye_v13.py. NO editar. Con eta_s=0 es v11m exacto."""\n')
    d = os.path.join(AQUI, 'organismo_v13m.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    return d


def v13g():
    src = open(os.path.join(AQUI, 'organismo_v13.py'), encoding='utf-8').read()
    cab, cuerpo = src.split("def run(", 1)
    cuerpo = "def run(" + cuerpo
    cab = cab + HELPERS.lstrip('\n')
    n_pat = cuerpo.count("PAT")
    print(f"    (v13g: PAT aparece {n_pat} veces en run(); v9g tenia 21, v13 anade las de la via lenta)")
    cuerpo = cuerpo.replace("PAT", "P_")
    cuerpo = sust(cuerpo, FIRMA_V13, FIRMA_V13[:-2] + ",mundo='AB',regla='px0',fase2_en=None,sonda_final=False):", etiqueta='firma')
    ancla = "    rng=np.random.default_rng(seed)\n"
    cuerpo = sust(cuerpo, ancla,
        "    if mundo=='AB': P_=PAT; tren=['A','B']; test=[]   # v13g: con 'AB' es v13 exacto\n"
        "    else: P_,tren,test,val_regla=split_regla(seed,regla); fase2_en=T//2 if fase2_en is None else fase2_en\n" + ancla,
        etiqueta='mundo')
    cuerpo = sust(cuerpo, "    while not cond(): KW[objetivo_AB:NK]=", "    while mundo=='AB' and not cond(): KW[objetivo_AB:NK]=",
                  etiqueta='rechazo solo en AB')
    cuerpo = sust(cuerpo, "pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}\n",
                  "pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'} if mundo=='AB' else dict(val_regla)\n", etiqueta='val')
    cuerpo = sust(cuerpo, "    tipos=['A','B']\n",
                  "    tipos=['A','B'] if mundo=='AB' else list(tren)\n"
                  "    W_apriori=None; codigos_f2=None; primer={}   # v13g: sonda y primer encuentro (lectura)\n", etiqueta='tipos')
    ancla = "        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val\n"
    cuerpo = sust(cuerpo, ancla, ancla +
        "        if mundo!='AB' and t==fase2_en:   # v13g: sonda a priori (valor TOTAL) y entrada de los de test\n"
        "            W_apriori={_k:valor(P_[_k]) for _k in P_}\n"
        "            codigos_f2={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}\n"
        "            tipos.extend(test); primer={_k:None for _k in test}\n", etiqueta='fase 2')
    ancla = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
    cuerpo = sust(cuerpo, ancla, ancla +
        "            if kk in primer and primer[kk] is None: primer[kk]=dict(t=t,W=_wt,pb=float(pb),hambre=float(hambre),mordio=bool(mordio))   # v13g\n",
        etiqueta='primer encuentro')
    ancla = "    W={k:round(valor(P_[k]),2) for k in P_}   # v13: valor total\n"
    cuerpo = sust(cuerpo, ancla,
        "    _sonda=None; _cod_fin=None\n"
        "    if sonda_final:   # v13g: valor TOTAL y codigo de los 64 patrones al final (lectura)\n"
        "        _sonda={}\n"
        "        for _n in range(64):\n"
        "            _P=np.array([(_n>>(5-_j))&1 for _j in range(6)],float); _nm=''.join(str(int(_v)) for _v in _P)\n"
        "            _sonda[_nm]=dict(W=valor(_P),codigo=sorted(int(_i) for _i in code(_P)))\n"
        "        _cod_fin={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}\n" + ancla, etiqueta='sonda final')
    cuerpo = sust(cuerpo, "                solap={'AB':", "                solap=None if mundo!='AB' else {'AB':", etiqueta='solap')
    cuerpo = sust(cuerpo, "Wns=[round(float(x),3) for x in Wns])",
                  "Wns=[round(float(x),3) for x in Wns],mundo=mundo,regla=regla,tren=tren,test=test,W_apriori=W_apriori,codigos_f2=codigos_f2,"
                  "primer=primer,W_final=({_k:valor(P_[_k]) for _k in P_} if mundo!='AB' else None),"
                  "sonda=_sonda,codigos_fin=_cod_fin)", etiqueta='return')
    cabecera = ('"""organismo_v13g = organismo_v13.py + mundo de regla, sonda a priori (valor TOTAL), primer encuentro y sonda final\n'
                '(mismas anclas que v9g/v11g/v12g). Generado por construye_v13.py. NO editar. Con eta_s=0 es organismo_v11g exacto.\n'
                '"""\n')
    d = os.path.join(AQUI, 'organismo_v13g.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cabecera + cab + cuerpo)
    return d


if __name__ == '__main__':
    for f in (v13, v13m, v13g):
        d = f()
        print(f"  {os.path.relpath(d, RAIZ):48s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
