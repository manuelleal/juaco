"""CREADOR B — ORGANO DE ASOCIACION EN UNA EXPOSICION (ligar al parecido, desligar con una mordida).

Genera experimentos/creacion_B/organismo_v14L.py = organismo/organismo_v14.py (9bab8ac0685b1f21, CONGELADO: solo
se LEE) + perilla `sem`. Con sem=0 es organismo_v14 EXACTO (arnes identidad_B4.py).

MEDIDA PRINCIPAL (nueva, de solo lectura, activa siempre): `exp_hasta[patron]` = numero de MORDIDAS de ese patron
tras las cuales el valor que usa la boca cae a <= tol_sem del valor real del mundo, por primera vez.
"EXPOSICIONES HASTA ASOCIAR". v14 hoy necesita 7-19 mordidas (dato N1).

EL ORGANO (perilla `sem`):
  Cuando el organismo muerde un patron cuyo CODIGO EXACTO es nuevo (evidencia 1: primera mordida), en vez de
  arrancar su valor en CERO lo LIGA a lo previo mas parecido y HEREDA su valor:
      Wp[codigo] += v0/K   (o Wn, si v0 < 0)      -> (Wp-Wn) @ codigo == v0 al instante
  y anota el prestamo en `_sembrado`. En la MORDIDA SIGUIENTE de ese mismo codigo:
      si el signo del refuerzo CONTRADICE el prestamo, se DESLIGA entero (se resta lo prestado) y el patron
      sigue aprendiendo desde cero con la regla normal.   UNA mordida basta para desligar.
      si lo confirma, el prestamo deja de ser hipotesis y se queda.

  De donde sale "lo mas parecido" (`sem` elige):
    sem=1  VIA LENTA: v0 = (Wps-Wns) @ P. Parecido = solapamiento de pixeles, leido por el organo que v13 ya tiene.
           MEMORIA NUEVA: **CERO**. Es el control barato que hay que correr ANTES de pagar por un almacen.
    sem=2  CANAL HIPERDIMENSIONAL (Kanerva): una expansion aparte HW (nh x 6, nh >> NKMAX) con codigo disperso
           top-kh; el almacen guarda, por cada codigo HD visto, el valor que el organismo ya tenia; v0 = el valor
           del item con mayor solapamiento si sim >= theta_sim, si no 0.
           MEMORIA NUEVA DECLARADA: nh*6 flotantes (proyeccion) + por item kh enteros y un flotante.
    sem=3  CONTROL BARAJADO: v0 al azar entre los valores del mundo (+1 / -3), con un RNG APARTE. Si la ganancia
           sobrevive a esto, lo que actua es "arrancar lejos de cero", no el PARECIDO.

Perillas: sem, nh=2000, kh=40, theta_sim=0.5, sem_min=0.3, tol_sem=0.5. Los RNG de sem=2 y sem=3 son APARTE
(seed+400000, seed+500000): no tocan el flujo de azar del organismo.

Anclas con conteo exacto; origen por sha. NO edita ningun original.
Uso:  python experimentos/creacion_B/construye_B4.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'organismo', 'organismo_v14.py')
SHA_ORIGEN = '9bab8ac0685b1f21'


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

    # 1) firma
    s = sust(s, "pat_shuf=0,pat_min=1):",
             "pat_shuf=0,pat_min=1,sem=0,nh=2000,kh=40,theta_sim=0.15,sem_min=0.3,tol_sem=0.5):", etiqueta='firma')

    # 2) estado del organo + medida de exposiciones (la medida es de solo lectura y va siempre)
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
    s = sust(s, "            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)\n",
             "            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)\n"
             "            if exp_hasta.get(kk) is None and _nmord.get(kk,0)>0 and abs(_wt-R_VAL[val[kk]])<=tol_sem: exp_hasta[kk]=_nmord[kk]   # B: EXPOSICIONES HASTA ASOCIAR\n",
             etiqueta='medida de exposiciones')

    # 4) ligar / desligar, en la mordida, junto al contador de evidencia del codigo
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
             "                        _v0,_tp=_arista(PAT[kk]) if sem==4 else (_prior(PAT[kk]),None)\n"
             "                        if abs(_v0)>=sem_min:\n"
             "                            if _v0>0: Wp[kc>0]=np.clip(Wp[kc>0]+_v0/K,0,3.)\n"
             "                            else:     Wn[kc>0]=np.clip(Wn[kc>0]+(-_v0)/K,0,3.)\n"
             "                            _sembrado[_ky]=_v0; n_sem+=1; sem_log.append((t,kk,'liga',round(_v0,3),_tp))\n"
             "                            if _tp is not None: _qui[_ky]=_tp\n"
             "                    if sem in (2,4): almacen[_hcode(PAT[kk])]=float(valor(PAT[kk]))   # NODO: lo que el organismo YA SABE de ese patron\n"
             "                if sem==4: _ult=float(valor(PAT[kk]))   # B: el nodo recien mordido, para la arista de co-ocurrencia\n",
             etiqueta='ligar y desligar')

    # 5) salida
    s = sust(s, "puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),",
             "puerta_pat=puerta_pat,pat_shuf=pat_shuf,pat_min=pat_min,n_cod=len(ncod),"
             "sem=sem,exp_hasta=dict(exp_hasta),n_mord=dict(_nmord),n_sem=int(n_sem),n_des=int(n_des),sem_log=sem_log,"
             "rel_arista=dict(_relia),n_nodos=len(almacen),",
             etiqueta='salida')

    cab = ('"""organismo_v14L = organismo/organismo_v14.py (9bab8ac0685b1f21, CONGELADO: solo se leyo) + ORGANO DE\n'
           'ASOCIACION EN UNA EXPOSICION (perilla sem: ligar al mas parecido, heredar su valor, desligar con una\n'
           'mordida) y la medida EXPOSICIONES HASTA ASOCIAR (exp_hasta, solo lectura, siempre activa).\n'
           'Generado por construye_B4.py. NO editar a mano. Con sem=0 es organismo_v14 EXACTO."""\n')
    d = os.path.join(AQUI, 'organismo_v14L.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):50s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
