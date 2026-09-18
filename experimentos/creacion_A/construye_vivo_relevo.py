"""CREADOR A — `organismo_vivo_relevo.py`: el organismo del MUNDO VIVO + la memoria de pares con RELEVO de v15f
(R crudo, sobrescritura, relevo a la lineal por abstencion, cada via con su propio error), UNA TABLA POR NECESIDAD.
Paquete de v15f para el CRITERIO DE TRONCO v2 (registro/CRITERIO_TRONCO_v2.md).

ORIGEN (por anclas; SOLO se lee): experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py, que es organismo_vivo_rep.py
<- organismo_vivo.py <- organismo/organismo_v14.py (v14.1) por anclas. Se deriva de rep2 y no de organismo_vivo porque la
puerta T-A (r = descendientes - muertes) exige las perillas de reproduccion de los brazos VIVO y CUELLO_MIN de
corre_vivo_rep2.py; con `reproduccion=0` rep2 ES organismo_vivo bit a bit (identidad (A) del disenador), y con
`vivo=0, n_nec=1` es organismo_v14. El arnes identidad_vivo_relevo.py lo comprueba con la perilla apagada en las
cuatro cadenas (rep2 VIVO/CUELLO_MIN, organismo_vivo, v14.1, y las 9 semillas ALIAS del bloque de la sal).

PERILLAS NUEVAS (todas inertes por defecto; con `memoria_pares=None` nada nuevo se evalua y no se toca el rng):
  memoria_pares = None | 'relevo'    la tabla de pares (15 pares x 4 casillas) POR NECESIDAD, con R CRUDO de la
                                     componente de esa necesidad y SOBRESCRITURA (mem_alfa=1.0); la via lenta de cada
                                     necesidad lee la casilla de su celda ganadora si conoce la combinacion, si no su
                                     lineal; la lineal aprende de SU error; la rapida de SU error (sin tocar).
  relevo_boca = 0 | 1                0 = v15f (el relevo vive DENTRO de la via lenta; la puerta de v14.1 decide antes).
                                     1 = BRAZO EXPLORATORIO declarado (v15g): la casilla VISTA manda ANTES que la puerta
                                     (exacto si lo conoce; si no, la puerta de v14.1). NO es el candidato: se mide
                                     pareado para saber si T-D (alias) depende del orden de la puerta.
  invertir_vivo_en = None | t        T-C en el mundo vivo (corre_vivo no la tiene con 4 estimulos): en t los EFECTOS de
                                     comida y veneno se intercambian (A pasa a quitar energia, B a darla).
Uso: python construye_vivo_relevo.py     (no corre nada)
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
VIVO = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')


def origen(ruta):
    b = open(ruta, 'rb').read()
    return b.decode('utf-8'), hashlib.sha256(b).hexdigest()[:16]


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


def pon(src):
    out = sust(src, ",rep2=0,rep2_regalo=600):",
               ",rep2=0,rep2_regalo=600,memoria_pares=None,mem_alfa=1.0,mem_rho=0.02,relevo_boca=0,invertir_vivo_en=None):", etq='firma')
    # 1) estado + lecturas (una tabla por necesidad)
    A = "    Wps=np.zeros((n_nec,6)); Wns=np.zeros((n_nec,6))   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0). VIVO: una fila por necesidad"
    B = (A + "\n"
         "    if memoria_pares not in (None,'relevo'): raise ValueError(f\"memoria_pares={memoria_pares!r}\")   # RELEVO: perilla mal escrita no cae en silencio\n"
         "    _PARv=[(i,j) for i in range(6) for j in range(i+1,6)]   # RELEVO: las 15 celdas = pares de pixeles\n"
         "    _MMv=np.zeros((n_nec,15,4)); _MNv=np.zeros((n_nec,15,4)); _MEv=np.full((n_nec,15),1e9); _MGv=[0]*n_nec   # RELEVO: R CRUDO por casilla, visitas, error propio, ganadora — POR NECESIDAD\n"
         "    def _lin_v15(_n,P): return float((Wps[_n]-Wns[_n])@P)   # RELEVO: la lectura lineal sola de la necesidad _n (la expresion literal)\n"
         "    def _tabla_v15(_n,P):   # RELEVO: (valor, visto) de la casilla de la celda ganadora de la necesidad _n\n"
         "        _i,_j=_PARv[_MGv[_n]]; _c=int(P[_i])*2+int(P[_j])\n"
         "        return (float(_MMv[_n,_MGv[_n],_c]), True) if _MNv[_n,_MGv[_n],_c]>0 else (0.0, False)\n"
         "    def _lenta_v15(_n,P):   # RELEVO: apagada = literalmente la lectura lineal; 'relevo' = la casilla si conoce la combinacion, si no la lineal\n"
         "        if memoria_pares is None: return float((Wps[_n]-Wns[_n])@P)\n"
         "        _tv,_vv=_tabla_v15(_n,P)\n"
         "        return _tv if _vv else _lin_v15(_n,P)\n"
         "    def _escribe_v15(_n,P,_R):   # RELEVO: las 15 celdas de la necesidad _n escriben R CRUDO (sobrescritura); ganadora por menor error propio de la casilla sola; desempate al azar con el rng del organismo\n"
         "        for _cv in range(15):\n"
         "            _iv,_jv=_PARv[_cv]; _dv=int(P[_iv])*2+int(P[_jv])\n"
         "            _pv=float(_MMv[_n,_cv,_dv]) if _MNv[_n,_cv,_dv]>0 else 0.0\n"
         "            _erv=_R-_pv; _prv=bool(_MNv[_n,_cv].sum()==0)\n"
         "            _MEv[_n,_cv]=(_erv*_erv) if _prv else (1-mem_rho)*_MEv[_n,_cv]+mem_rho*(_erv*_erv)\n"
         "            if _MNv[_n,_cv,_dv]==0 or mem_alfa>=1.0: _MMv[_n,_cv,_dv]=_R\n"
         "            else: _MMv[_n,_cv,_dv]+=mem_alfa*(_R-_MMv[_n,_cv,_dv])\n"
         "            _MNv[_n,_cv,_dv]+=1\n"
         "        _mnv=float(_MEv[_n].min()); _empv=[int(_x) for _x in np.where(_MEv[_n]<=_mnv+1e-12)[0]]\n"
         "        _MGv[_n]=_empv[0] if len(_empv)==1 else int(_empv[int(rng.integers(len(_empv)))])   # solo consume rng si HAY empate y la perilla esta ON")
    out = sust(out, A, B, etq='estado')
    # 2) valor() y _vnec(): la lectura lenta por necesidad; con relevo_boca=1 la casilla vista manda antes que la puerta
    A = ("        _k=kenyon(P); _f=float((Wp[_nm]-Wn[_nm])@_k); _s=float((Wps[_nm]-Wns[_nm])@P)\n"
         "        return _f+_s if puerta is None else (_f if _fam(_k) else _s)")
    B = ("        _k=kenyon(P); _f=float((Wp[_nm]-Wn[_nm])@_k); _s=_lenta_v15(_nm,P)\n"
         "        if memoria_pares is not None and relevo_boca and _tabla_v15(_nm,P)[1]: return _s   # v15g (brazo exploratorio): la casilla VISTA manda antes que la puerta\n"
         "        return _f+_s if puerta is None else (_f if _fam(_k) else _s)")
    out = sust(out, A, B, etq='valor')
    A = ("        _f=float((Wp[_n]-Wn[_n])@_k); _s=float((Wps[_n]-Wns[_n])@P)\n"
         "        return _f+_s if puerta is None else (_f if _fam(_k,_n) else _s)")
    B = ("        _f=float((Wp[_n]-Wn[_n])@_k); _s=_lenta_v15(_n,P)\n"
         "        if memoria_pares is not None and relevo_boca and _tabla_v15(_n,P)[1]: return _s   # v15g (brazo exploratorio)\n"
         "        return _f+_s if puerta is None else (_f if _fam(_k,_n) else _s)")
    out = sust(out, A, B, etq='_vnec')
    # 3) la mordida: lectura lenta de la necesidad activa (+ el brazo exploratorio)
    out = sust(out, "_ws=float((Wps[_nm]-Wns[_nm])@PAT[kk])   # v13: las dos vias (VIVO: las de la necesidad activa)",
               "_ws=_lenta_v15(_nm,PAT[kk])   # v13: las dos vias (VIVO: las de la necesidad activa; RELEVO: la casilla si la conoce, si no la lineal)", etq='mordida')
    A = "            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; con puerta: la rapida si le es familiar)\n"
    B = A + "            if memoria_pares is not None and relevo_boca and _tabla_v15(_nm,PAT[kk])[1]: _wt=_ws   # v15g (brazo exploratorio): la casilla vista manda antes que la puerta\n"
    out = sust(out, A, B, etq='_wt')
    # 4) la lineal de la necesidad activa aprende de SU error; la tabla escribe tras su paso
    out = sust(out, "                        _ds=dlt if puerta is None else R-_ws\n",
               "                        _lbv=_lin_v15(_nm,PAT[kk]); _ds=dlt if puerta is None else R-_lbv   # RELEVO: la lineal aprende de SU error (apagada: _lbv == _ws)\n", etq='_ds')
    A = "                        else:     Wns[_nm]=np.clip(Wns[_nm]+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)\n"
    B = A + "                        if memoria_pares is not None: _escribe_v15(_nm,PAT[kk],R)   # RELEVO: la tabla de la necesidad activa escribe R crudo\n"
    out = sust(out, A, B, etq='escritura activa')
    # 5) las OTRAS necesidades: su lineal con su error; su tabla con su componente
    out = sust(out, "_wsn=float((Wps[_n]-Wns[_n])@PAT[kk])", "_wsn=_lenta_v15(_n,PAT[kk])", etq='_wsn')
    out = sust(out, "                                _dsn=_dn if puerta is None else _Rn-_wsn\n",
               "                                _lbn=_lin_v15(_n,PAT[kk]); _dsn=_dn if puerta is None else _Rn-_lbn   # RELEVO: su lineal aprende de SU error\n", etq='_dsn')
    A = "                                else:      Wns[_n]=np.clip(Wns[_n]+eta_s*aversion*(-_dsn)*PAT[kk],0,clip_s)\n"
    B = A + "                                if memoria_pares is not None: _escribe_v15(_n,PAT[kk],_Rn)   # RELEVO: la tabla de la otra necesidad escribe SU componente\n"
    out = sust(out, A, B, etq='escritura otras')
    # 6) T-C en el mundo vivo: los efectos de comida y veneno se intercambian en t
    A = "        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}\n"
    B = A + "        if invertir_vivo_en is not None and t==invertir_vivo_en: _EF=dict(_EF,comida=_EF['veneno'],veneno=_EF['comida'])   # T-C vivo: la comida pasa a quitar energia y el veneno a darla\n"
    out = sust(out, A, B, etq='invertir_vivo')
    # 7) el return (lecturas; None con la perilla apagada)
    out = sust(out, "    return dict(sobre=sobre,",
               "    return dict(memoria_pares=memoria_pares,relevo_boca=relevo_boca,invertir_vivo_en=invertir_vivo_en,"
               "mem_ganadora=([list(_PARv[_g]) for _g in _MGv] if memoria_pares is not None else None),"
               "W_tabla=([{k:(round(_tabla_v15(_n,PAT[k])[0],3) if _tabla_v15(_n,PAT[k])[1] else None) for k in PAT} for _n in range(n_nec)] if memoria_pares is not None else None),"
               "mem_vistas=(int((_MNv>0).sum()) if memoria_pares is not None else None),sobre=sobre,", etq='return')
    return out


if __name__ == '__main__':
    src, s0 = origen(os.path.join(VIVO, 'organismo_vivo_rep2.py'))
    _, s_vivo = origen(os.path.join(VIVO, 'organismo_vivo.py'))
    _, s14 = origen(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'))
    t = pon(src)
    cab = (f'"""organismo_vivo_relevo = experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py ({s0}; solo se leyo; cadena organismo_vivo\n'
           f'{s_vivo} <- organismo_v14 {s14}) + memoria de pares con RELEVO (v15f) por necesidad, brazo exploratorio `relevo_boca` y la\n'
           f'inversion del mundo vivo `invertir_vivo_en`. Con memoria_pares=None es organismo_vivo_rep2 EXACTO (y organismo_vivo con\n'
           f'reproduccion=0; organismo_v14 con vivo=0, n_nec=1) sin consumir rng. Generado por construye_vivo_relevo.py. NO editar."""\n')
    ruta = os.path.join(AQUI, 'organismo_vivo_relevo.py')
    open(ruta, 'w', encoding='utf-8', newline='\n').write(cab + t)
    print(f'origen organismo_vivo_rep2 {s0}  organismo_vivo {s_vivo}  organismo_v14 {s14}')
    print(f'escrito organismo_vivo_relevo.py {hashlib.sha256(open(ruta, "rb").read()).hexdigest()[:16]}')
