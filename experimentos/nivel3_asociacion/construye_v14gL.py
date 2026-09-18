"""experimentos/nivel3_asociacion/construye_v14gL.py -- IMPLEMENTADOR, a partir de la propuesta B-4 del creador B
(registro/investigacion/PUENTE_creacion.md, "Propuestas para el coordinador") -- ORGANO DE ASOCIACION EN UNA
EXPOSICION sobre el MUNDO DE REGLA.

Genera organismo_v14gL.py = organismo/organismo_v14g.py (1f1318480cd34cde, CONGELADO: solo se LEE) + la MISMA
perilla `sem` y la MISMA medida `exp_hasta` que experimentos/creacion_B/construye_B4.py le puso a organismo_v14
(-> organismo_v14L.py, d6d550aec83f775a). Son las CINCO anclas de construye_B4.py, verificadas una a una contra
organismo_v14g.py. TRES son bit a bit identicas (ni el texto buscado ni el insertado mencionan PAT). DOS se
adaptan porque el mundo de regla difiere del mundo AB, y se declaran aqui (regla del encargo: "si una ancla no
existe en v14g, resuelvelo y declaralo"):

  ANCLA 1 (firma). organismo_v14g.py trae las perillas del tronco APAGADAS por defecto -- es organismo_v13g con
  ropa de v14; `bateria_generaliza.py` las ENCIENDE con kwargs explicitos (INSTRUMENTOS['organismo_v14']:
  eta_s=0.015, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1).
  Por eso el ULTIMO default de la firma es `pat_min=0`, no `pat_min=1` como en organismo_v14.py. El texto del
  ancla se adapta de "pat_shuf=0,pat_min=1):" a "pat_shuf=0,pat_min=0):"; los kwargs NUEVOS que agrega
  (sem=0,nh=2000,kh=40,theta_sim=0.15,sem_min=0.3,tol_sem=0.5) son EXACTAMENTE los mismos six, con el mismo
  default, en el mismo orden -- sem=0 sigue siendo "el organo apagado" con independencia de en que valor esten
  las perillas del tronco.

  ANCLA 4 (ligar y desligar). El texto que construye_B4.py inserta llama tres veces a `PAT[kk]` -- 5 ocurrencias
  contando `_arista(PAT[kk])`, `_prior(PAT[kk])`, `_hcode(PAT[kk])`, `valor(PAT[kk])` (x2 mas la de _ult) --
  donde `PAT` es el diccionario GLOBAL de 4 patrones A/B/C/D del mundo AB (linea 22 del propio organismo_v14g.py).
  `organismo_v14g.py` NO usa `PAT` a secas dentro de `run()`: usa la variable local `P_`, que es `PAT` cuando
  `mundo=='AB'` pero el diccionario de los 20 patrones de `patrones_regla()` (claves como '110100') cuando
  `mundo!='AB'` (linea 58: `if mundo=='AB': P_=PAT ... else: P_,tren,test,val_regla=split_regla(...)`). Con
  `PAT[kk]` a secas, CUALQUIER patron de la regla levanta KeyError apenas se muerde por primera vez con `sem!=0`.
  Las CINCO ocurrencias de `PAT[kk]` en el texto insertado se cambian a `P_[kk]`; el resto del bloque (`Wp`, `Wn`,
  `_sembrado`, `_relia`, `K`, `R`, `kc` -- todos genericos o globales, ninguno referencia PAT) queda IDENTICO.
  Con `mundo='AB'`, `P_ is PAT` (misma referencia de objeto), asi que el cambio es transparente tambien ahi:
  `P_[kk] == PAT[kk]` siempre que `mundo=='AB'`.

  Anclas 2 (estado del organo), 3 (medida de exposiciones) y 5 (salida) son BIT A BIT las de construye_B4.py:
  ninguna referencia a PAT/P_ en su texto (`_prior`, `_hcode`, `_arista`, `exp_hasta` y el diccionario de salida
  toman `P`/`kc`/`val[kk]`/`R_VAL` como parametro o global, no el diccionario de patrones por nombre).

Con sem=0, organismo_v14gL.py es organismo_v14g.py EXACTO en TODAS las claves (arnes: identidad_v14gL.py).
Anclas con conteo exacto (aborta si una cuenta distinto de lo esperado); origen verificado por sha. NO edita
ningun original.

Uso:  python experimentos/nivel3_asociacion/construye_v14gL.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'organismo', 'organismo_v14g.py')
SHA_ORIGEN = '1f1318480cd34cde'


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN: sha {h16(ORIGEN)}, se esperaba {SHA_ORIGEN}. Abortado.")
    s = open(ORIGEN, encoding='utf-8').read()

    # 1) firma -- ADAPTADA: el ultimo default de organismo_v14g.py es pat_min=0 (perillas del tronco apagadas),
    #    no pat_min=1 como en organismo_v14.py. Los kwargs nuevos son identicos a construye_B4.py.
    s = sust(s, "pat_shuf=0,pat_min=0):",
             "pat_shuf=0,pat_min=0,sem=0,nh=2000,kh=40,theta_sim=0.15,sem_min=0.3,tol_sem=0.5):", etiqueta='firma')

    # 2) estado del organo + medida de exposiciones (IDENTICA a construye_B4.py: no referencia PAT)
    s = sust(s, "    ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO (mordidas por codigo) y orden de aparicion\n",
             "    ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO (mordidas por codigo) y orden de aparicion\n"
             "    _nmord={}; exp_hasta={}   # B: MEDIDA — mordidas por patron y EXPOSICIONES HASTA ASOCIAR (solo lectura)\n"
             "    _sembrado={}; n_sem=0; n_des=0; sem_log=[]   # B: prestamos vivos, ligaduras y desligaduras\n"
             "    _HW=np.random.default_rng(seed+400000).uniform(0,1,(nh,6)) if sem in (2,4) else None   # B: canal HD (nodos), RNG APARTE\n"
             "    _rng4=np.random.default_rng(seed+500000)   # B: control barajado (sem=3), RNG APARTE\n"
             "    almacen={}   # B: codigo HD -> valor ya sabido (solo sem=2)\n"
             "    def _hcode(P): _v=_HW@P; return frozenset(np.argsort(_v)[-kh:].tolist())\n"
             "    def _prior(P):   # el valor de LO PREVIO MAS PARECIDO\n"
             "        if sem==1: return float((Wps-Wns)@P)\n"
             "        if sem==2:\n"
             "            if not almacen: return 0.0\n"
             "            _h=_hcode(P); _m=max(almacen, key=lambda q: len(q&_h))\n"
             "            return float(almacen[_m]) if len(_m&_h)/kh>=theta_sim else 0.0\n"
             "        if sem==3: return float(_rng4.choice(np.array([-3.0,1.0])))\n"
             "        return 0.0\n"
             "    _relia={'sim':0.5,'co':0.5}; _ult=None; _qui={}   # B: GRAFO — fiabilidad por TIPO DE ARISTA, ultimo nodo mordido, arista usada por codigo\n"
             "    def _arista(P):   # B: candidatos por tipo de arista; se recorre la MAS FIABLE, y si ninguna lo es, NO hereda\n"
             "        _c={}\n"
             "        if almacen:\n"
             "            _h=_hcode(P); _m=max(almacen, key=lambda q: len(q&_h))\n"
             "            if len(_m&_h)/kh>=theta_sim: _c['sim']=float(almacen[_m])   # arista de PARECIDO\n"
             "        if _ult is not None: _c['co']=float(_ult)   # arista de CO-OCURRENCIA (el nodo mordido justo antes)\n"
             "        if not _c: return 0.0,None\n"
             "        _tt=max(_c, key=lambda tp:_relia[tp])\n"
             "        return (_c[_tt],_tt) if _relia[_tt]>=0.5 else (0.0,None)\n", etiqueta='estado del organo')

    # 3) la medida: tras n mordidas de ese patron, el valor que usa la boca ya esta a <= tol del real
    #    (IDENTICA a construye_B4.py: usa R_VAL global y val[kk], genericos; ninguno referencia PAT)
    s = sust(s, "            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)\n",
             "            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)\n"
             "            if exp_hasta.get(kk) is None and _nmord.get(kk,0)>0 and abs(_wt-R_VAL[val[kk]])<=tol_sem: exp_hasta[kk]=_nmord[kk]   # B: EXPOSICIONES HASTA ASOCIAR\n",
             etiqueta='medida de exposiciones')

    # 4) ligar / desligar -- ADAPTADA: PAT[kk] (global, solo A/B/C/D) -> P_[kk] (el diccionario ACTIVO: PAT en
    #    mundo AB, los 20 patrones de la regla si no). 5 ocurrencias; ver nota de cabecera.
    s = sust(s, "                ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto\n",
             "                ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto\n"
             "                _nmord[kk]=_nmord.get(kk,0)+1   # B: medida\n"
             "                if sem:   # B: ASOCIACION EN UNA EXPOSICION\n"
             "                    if _ky in _sembrado:\n"
             "                        _v0=_sembrado.pop(_ky); _tp=_qui.pop(_ky,None)\n"
             "                        if _tp is not None: _relia[_tp]=0.7*_relia[_tp]+0.3*(1.0 if _v0*R>0 else 0.0)   # B: la ARISTA se gana o se pierde la confianza\n"
             "                        if _v0*R<0:   # la primera evidencia propia CONTRADICE el prestamo -> se desliga entero\n"
             "                            if _v0>0: Wp[kc>0]=np.clip(Wp[kc>0]-_v0/K,0,3.)\n"
             "                            else:     Wn[kc>0]=np.clip(Wn[kc>0]-(-_v0)/K,0,3.)\n"
             "                            n_des+=1; sem_log.append((t,kk,'desliga',round(_v0,3)))\n"
             "                    elif ncod[_ky]==1:   # CODIGO NUEVO: hereda el valor de lo previo mas parecido\n"
             "                        _v0,_tp=_arista(P_[kk]) if sem==4 else (_prior(P_[kk]),None)\n"
             "                        if abs(_v0)>=sem_min:\n"
             "                            if _v0>0: Wp[kc>0]=np.clip(Wp[kc>0]+_v0/K,0,3.)\n"
             "                            else:     Wn[kc>0]=np.clip(Wn[kc>0]+(-_v0)/K,0,3.)\n"
             "                            _sembrado[_ky]=_v0; n_sem+=1; sem_log.append((t,kk,'liga',round(_v0,3),_tp))\n"
             "                            if _tp is not None: _qui[_ky]=_tp\n"
             "                    if sem in (2,4): almacen[_hcode(P_[kk])]=float(valor(P_[kk]))   # NODO: lo que el organismo YA SABE de ese patron\n"
             "                if sem==4: _ult=float(valor(P_[kk]))   # B: el nodo recien mordido, para la arista de co-ocurrencia\n",
             etiqueta='ligar y desligar')

    # 5) salida (IDENTICA a construye_B4.py)
    s = sust(s, "puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),",
             "puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),"
             "sem=sem,exp_hasta=dict(exp_hasta),n_mord=dict(_nmord),n_sem=int(n_sem),n_des=int(n_des),sem_log=sem_log,"
             "rel_arista=dict(_relia),n_nodos=len(almacen),",
             etiqueta='salida')

    cab = ('"""organismo_v14gL = organismo/organismo_v14g.py (1f1318480cd34cde, CONGELADO: solo se leyo) + ORGANO\n'
           'DE ASOCIACION EN UNA EXPOSICION (perilla sem: ligar al mas parecido, heredar su valor, desligar con\n'
           'una mordida) y la medida EXPOSICIONES HASTA ASOCIAR (exp_hasta, solo lectura, siempre activa) -- las\n'
           'MISMAS que experimentos/creacion_B/organismo_v14L.py, aplicadas al MUNDO DE REGLA. Generado por\n'
           'construye_v14gL.py (mismas 5 anclas que construye_B4.py; 2 adaptadas porque el mundo de regla usa P_\n'
           'en vez de PAT y arranca con las perillas del tronco apagadas -- ver la cabecera del constructor).\n'
           'NO editar a mano. Con sem=0 es organismo_v14g EXACTO."""\n')
    d = os.path.join(AQUI, 'organismo_v14gL.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):50s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
