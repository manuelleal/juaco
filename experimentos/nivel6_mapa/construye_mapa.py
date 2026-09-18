"""Genera mundo_mapa.py = organismo_v13.py (cc8b16b492d4d324) + vision limitada (r_vis) + sitios fijos con regeneracion
+ tabla M posicion->patron con simulacion hacia adelante + prueba de teletransporte. Con las perillas apagadas
(r_vis=None, sitios=None, usa_M=False, prueba=None) es organismo_v13 EXACTO (identidad obligatoria). Anclas con conteo exacto.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'organismo', 'organismo_v13.py')
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


PARCHES = [
    (["mu_norm=True,div_signo=True,eta_s=0.015,clip_s=3.0,puerta=3):"],
     ["mu_norm=True,div_signo=True,eta_s=0.015,clip_s=3.0,puerta=3,",
      "        r_vis=None,sitios=None,regen=50,usa_M=False,escribe_M=True,gamma_M=0.6,H_M=20,disc_M=0.9,prueba=None):   # mapa"], 1, 'firma'),
    (["    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)"],
     ["    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)",
      "    _Mpat=np.zeros((L,6)); _Mset=np.zeros(L,bool); _VACIO=np.zeros(6)   # mapa: tabla posicion -> ultimo patron visto"], 1, 'M'),
    (["    def spawn():",
      "        while len(objs)<nobj:",
      "            x=int(rng.integers(L))",
      "            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]",
      "    spawn()"],
     ["    _SIT={}; _pend={}   # mapa: sitio -> tipo fijo; sitio -> paso en que reaparece",
      "    if sitios is not None:",
      "        _F0=int(rng.integers(L)); _SIT={(_F0+i*(L//len(sitios)))%L:kk for i,kk in enumerate(sitios)}",
      "    def spawn():",
      "        if sitios is not None:   # mapa: los objetos viven en sitios fijos",
      "            for x,kk in _SIT.items():",
      "                if x not in objs and x not in _pend: objs[x]=kk",
      "            return",
      "        while len(objs)<nobj:",
      "            x=int(rng.integers(L))",
      "            if x not in objs: objs[x]=tipos[int(rng.integers(len(tipos)))]",
      "    spawn()",
      "    def _sesgo_M():   # mapa: con la retina vacia, valor recordado por direccion, descontado por distancia",
      "        _bi=sum(disc_M**h*valor(_Mpat[(pos-h)%L]) for h in range(1,H_M+1) if _Mset[(pos-h)%L])",
      "        _bd=sum(disc_M**h*valor(_Mpat[(pos+h)%L]) for h in range(1,H_M+1) if _Mset[(pos+h)%L])",
      "        return gamma_M*np.array([_bi,_bd])"], 1, 'spawn/sitios/sesgo'),
    (["            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo"],
     ["            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo",
      "            if r_vis is not None and min((pos-x)%L,(x-pos)%L)>r_vis: continue   # mapa: fuera de la vista"], 1, 'vista 1'),
    (["                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)"],
     ["                if r_vis is not None and min((pos-x)%L,(x-pos)%L)>r_vis: continue   # mapa: fuera de la vista",
      "                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)"], 1, 'vista 2 (fallback)'),
    (["        return best"], ["        return best if best is not None else (None,'vacio',None)   # mapa: nada a la vista"], 1, 'see vacio'),
    (["    for t in range(T):",
      "        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}"],
     ["    for t in range(T):",
      "        if _pend:   # mapa: reaparecen en su sitio los objetos maduros",
      "            _mad=[x for x,tt in _pend.items() if tt<=t]",
      "            if _mad:",
      "                for x in _mad: del _pend[x]",
      "                spawn()",
      "        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}"], 1, 'regeneracion'),
    (["        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k]",
      "        x=np.concatenate([pat*1.2,[1.5 if left else 0,0 if left else 1.5,1.0 if d==0 else 0.]]); noise=.15+.5*hambre",
      "        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)"],
     ["        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k] if k!='vacio' else _VACIO",
      "        x=np.concatenate([pat*1.2,[1.5 if left else 0,1.5 if left is False else 0,1.0 if d==0 else 0.]]); noise=.15+.5*hambre",
      "        V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)",
      "        if usa_M and k=='vacio': u=u+_sesgo_M()   # mapa: solo desempata sin senal directa"], 1, 'politica'),
    (["        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if d2<d else 0."],
     ["        pos=(pos+int(m[1]-m[0]))%L; d2,_,_=see(); Rp=.2 if (d is not None and d2 is not None and d2<d) else 0."], 1, 'Rp'),
    (["            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@PAT[kk])   # v13: las dos vias"],
     ["            if usa_M and escribe_M: _Mpat[pos]=PAT[objs[pos]]; _Mset[pos]=True   # mapa: recuerda lo que vio aqui",
      "            kk=objs[pos]; kc=kenyon(PAT[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@PAT[kk])   # v13: las dos vias"], 1, 'escritura M'),
    (["                del objs[pos]; spawn()"],
     ["                if sitios is not None: _pend[pos]=t+regen   # mapa: reaparece en su sitio",
      "                del objs[pos]; spawn()"], 1, 'mordida'),
    (["            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido"],
     ["            _dx=list(objs)[int(rng.integers(len(objs)))]",
      "            if sitios is not None: _pend[_dx]=t+regen   # mapa",
      "            del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido"], 1, 'olvido'),
    (["    W={k:round(valor(PAT[k]),2) for k in PAT}   # v13: valor total"],
     ["    _tel=None",
      "    if prueba is not None:   # mapa: prueba de teletransporte, sin aprendizaje",
      "        _Fs=[x for x,kk in _SIT.items() if val[kk]=='comida']; _F=_Fs[0] if _Fs else int(rng.integers(L))",
      "        if prueba.get('barajar'):",
      "            _pi=rng.permutation(NKMAX); Wp=Wp[_pi]; Wn=Wn[_pi]; _pj=rng.permutation(6); Wps=Wps[_pj]; Wns=Wns[_pj]",
      "        if prueba.get('invertir'): Wp,Wn=Wn,Wp; Wps,Wns=Wns,Wps   # control decisivo: el valor con el signo cambiado (la puerta no cambia)",
      "        _ac=[]; _nn=0; _ciego=0; _pasos=[]",
      "        for i in range(prueba.get('n_tel',40)):",
      "            _dn=int(rng.integers(r_vis+1,13)); _lado=-1 if i%2==0 else 1   # la comida queda a _dn casillas hacia _lado",
      "            pos=(_F-_lado*_dn)%L; E=prueba.get('E_test',0.3); tr=np.zeros(9); _rech.clear()",
      "            for x in list(_pend): del _pend[x]",
      "            spawn(); _dir=0",
      "            for _s in range(prueba.get('max_pasos',30)):",
      "                hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k] if k!='vacio' else _VACIO",
      "                if _s==0 and k=='vacio': _ciego+=1",
      "                x=np.concatenate([pat*1.2,[1.5 if left else 0,1.5 if left is False else 0,1.0 if d==0 else 0.]]); noise=.15+.5*hambre",
      "                V=Wl@x; p=1/(1+np.exp(-(V-.8)/noise)); u=p+rng.normal(0,.3,2); m=np.zeros(2)",
      "                if usa_M and k=='vacio': u=u+_sesgo_M()",
      "                if u.max()>.5: m[np.argmax(u)]=1",
      "                if m.any(): _dir=int(m[1]-m[0]); break",
      "            _pasos.append(_s+1)",
      "            if _dir==0: _nn+=1",
      "            else: _ac.append(int(_dir==_lado))",
      "        _tel=dict(acierto=(round(sum(_ac)/len(_ac),3) if _ac else None),n=len(_ac),sin_mover=_nn,ciego_al_llegar=_ciego,",
      "                  pasos_medio=round(sum(_pasos)/len(_pasos),2),F=_F,sitios={int(x):kk for x,kk in _SIT.items()})",
      "    W={k:round(valor(PAT[k]),2) for k in PAT}   # v13: valor total"], 1, 'prueba'),
    (["W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns])"],
     ["W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],",
      "                tel=_tel,M_llenas=int(_Mset.sum()))   # mapa"], 1, 'return'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != 'cc8b16b492d4d324':
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != cc8b16b492d4d324")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_mapa = organismo_v13.py (cc8b16b492d4d324) + vision limitada r_vis + sitios fijos con regeneracion + tabla M' + NL +
           '(posicion -> ultimo patron visto) con simulacion hacia adelante + prueba de teletransporte. Generado por construye_mapa.py.' + NL +
           'NO editar. Con r_vis=None, sitios=None, usa_M=False, prueba=None es organismo_v13 exacto (identidad obligatoria)."""' + NL)
    d = os.path.join(AQUI, 'mundo_mapa.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
