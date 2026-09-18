"""Bloque 6 (rama) — constructor POR ANCLAS del instrumento de allostasis. Preregistro: PREREGISTRO_allostasis.md.

  organismo_v13a.py  <- organismo/organismo_v13.py                    (cc8b16b492d4d324, TRONCO CONGELADO: se lee, no se toca)
  organismo_v13ag.py <- experimentos/v13_dos_vias/organismo_v13g.py   (2a80e125f8593bf2, mundo de regla; mismas anclas)

Anade UNA lectura lineal mas (el predictor de dE: Wpe sobre la retina + Wke sobre las celdas de Kenyon), la sorpresa
|dE - dE_pred| y la modulacion eta_ef = eta*(1 + k_sorpresa*sorpresa) sobre la via RAPIDA. Con eta_pred=0 y
k_sorpresa=0 es v13/v13g EXACTO (identidad I1); con eta_pred>0 y k_sorpresa=0 el predictor SOLO MIDE y la conducta
sigue siendo la de v13 bit a bit (identidad I2). NO editar los generados a mano.

Uso:  python experimentos/nivel9_allostasis/construye_allostasis.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
NL = chr(10)

SHA_V13 = 'cc8b16b492d4d324'
SHA_V13G = '2a80e125f8593bf2'


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


PERILLAS = ("eta_pred=0.0,k_sorpresa=0.0,clip_e=3.0,buf_sorpresa=20,sorpresa_barajada=False,vent_sorpresa=2000")

# Estado nuevo (se inserta tras la via lenta). {pat} = PAT (v13) o P_ (v13g); {ext} = medidas de la inversion (solo v13a).
ESTADO = [
    "    Wpe=np.zeros(6); Wke=np.zeros(NKMAX)   # v13a: PREDICTOR de dE (modelo de si mismo). Inerte si eta_pred=0: no entra en valor() ni en la boca",
    "    _sq=[0.]*4; _eq=[0.]*4; _npq=[0]*4; _nq=[0]*4; _etaq=[0.]*4   # v13a: por cuarto — |e|, e con signo, bocados con predictor, bocados, factor eta_ef/eta",
    "    _vs=[0.,0.]; _ve=[0.,0.]; _vn=[0,0]   # v13a: ventana fina de vent_sorpresa pasos antes/despues de la inversion",
    "    _buf=[]; _rng_s=np.random.default_rng(seed+900000) if sorpresa_barajada else None   # v13a: control RUIDO, RNG PROPIO (no toca el del organismo)",
]
ESTADO_V13A = [
    "    t_ext_B=None; mord_post={'comida':0,'veneno':0}; deaths_post=0   # v13a: medidas tras la inversion (M1, M2)",
]

# Bloque del predictor: se inserta ANTES del reparto de error de v13, dentro de if mordio / if learn.
def predictor(pat):
    return [
        "                    _sr=0.; _sr0=0.   # v13a: sorpresa emitida (la que modula) y sorpresa real (la que se mide)",
        "                    if eta_pred:   # v13a: predice la energia que rinde el bocado y aprende de SU error (regla delta, tasa propia)",
        f"                        _dEp=float(Wpe@{pat}[kk])+float(Wke@kc); _ee=E_VAL[val[kk]]-_dEp; _sr0=abs(_ee); _sr=_sr0",
        f"                        Wpe=np.clip(Wpe+eta_pred*_ee*{pat}[kk],-clip_e,clip_e); Wke=np.clip(Wke+eta_pred*_ee*kc,-clip_e,clip_e)",
        "                        _sq[q(t)]+=_sr0; _eq[q(t)]+=_ee; _npq[q(t)]+=1",
        "                        if _rng_s is not None:   # RUIDO: misma magnitud, barajada en el tiempo (ventana de buf_sorpresa bocados)",
        "                            _buf.append(_sr)",
        "                            if len(_buf)>buf_sorpresa: _sr=float(_buf.pop(int(_rng_s.integers(len(_buf)))))",
        "                    _eta=eta*(1.+k_sorpresa*_sr) if k_sorpresa else eta   # v13a: eta_ef = eta*(1+k_sorpresa*sorpresa); con k_sorpresa=0 es eta EXACTO",
        "                    _nq[q(t)]+=1; _etaq[q(t)]+=_eta/eta",
        "                    if vent_sorpresa and invertir_en is not None and invertir_en-vent_sorpresa<=t<invertir_en+vent_sorpresa:",
        "                        _w=0 if t<invertir_en else 1; _vs[_w]+=_sr0; _ve[_w]+=_eta/eta; _vn[_w]+=1   # v13a: guarda G-b (misma eta media) y P3",
    ]


SALIDAS = [
    "                sorpresa_media=[round(_sq[i]/_npq[i],4) if (eta_pred and _npq[i]) else None for i in range(4)],",
    "                error_pred=[round(_eq[i]/_npq[i],4) if (eta_pred and _npq[i]) else None for i in range(4)],",
    "                eta_media=[round(_etaq[i]/_nq[i],4) if _nq[i] else None for i in range(4)],bocados=list(_nq),",
    "                sorpresa_pre=(round(_vs[0]/_vn[0],4) if (eta_pred and _vn[0]) else None),sorpresa_post=(round(_vs[1]/_vn[1],4) if (eta_pred and _vn[1]) else None),",
    "                eta_pre=(round(_ve[0]/_vn[0],4) if _vn[0] else None),eta_post=(round(_ve[1]/_vn[1],4) if _vn[1] else None),n_pre=_vn[0],n_post=_vn[1],",
]


def comun(s, pat):
    """Las cinco anclas que comparten v13 y v13g."""
    s = sust(s, "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)",
             "    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA, lineal sobre la retina (inerte si eta_s=0)" + NL + NL.join(ESTADO),
             etiqueta='estado del predictor')
    anc = "                    dlt=R-_wt if puerta is None else R-_wf   # v13: sin puerta UN error compartido; con puerta cada via el suyo"
    s = sust(s, anc, NL.join(predictor(pat)) + NL + anc, etiqueta='bloque del predictor')
    s = sust(s, "                    if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())" + NL +
                "                    else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())",
             "                    if dlt>0: _trunca=bool(((Wp[_ix]+_eta*dlt)>3.0).any())" + NL +
             "                    else:     _trunca=bool(((Wn[_ix]+_eta*aversion*(-dlt))>3.0).any())", etiqueta='techo con eta_ef')
    s = sust(s, "                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)" + NL +
                "                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)",
             "                    if dlt>0: Wp=np.clip(Wp+_eta*dlt*kc,0,3.)" + NL +
             "                    else:     Wn=np.clip(Wn+_eta*aversion*(-dlt)*kc,0,3.)", etiqueta='via rapida con eta_ef')
    return s


def v13a():
    s = origen(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'), SHA_V13)
    s = sust(s, "eta_s=0.015,clip_s=3.0,puerta=3):", "eta_s=0.015,clip_s=3.0,puerta=3," + PERILLAS + "):", etiqueta='firma v13a')
    s = comun(s, 'PAT')
    s = sust(s, NL.join(ESTADO), NL.join(ESTADO + ESTADO_V13A), etiqueta='estado de la inversion')
    s = sust(s, "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1",
             "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1" + NL +
             "                if invertir_en is not None and t>=invertir_en: mord_post[val[kk]]+=1   # v13a: M2, bocados tras la inversion",
             etiqueta='mord_post')
    s = sust(s, "        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas",
             "        if invertir_en is not None and t>=invertir_en and t_ext_B is None and valor(PAT['B'])>=0: t_ext_B=t   # v13a: M1, mismo criterio que mundo_social.py (lineas 156-157). No consume RNG" + NL +
             "        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas", etiqueta='t_ext_B')
    s = sust(s, "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))",
             "        if E<=0:" + NL +
             "            deaths+=1; E=.6; pos=int(rng.integers(L))" + NL +
             "            if invertir_en is not None and t>=invertir_en: deaths_post+=1   # v13a", etiqueta='deaths_post')
    s = sust(s, "W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns])",
             "W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns]," + NL +
             NL.join(SALIDAS) + NL +
             "                t_ext_B=t_ext_B,mord_post=mord_post,deaths_post=deaths_post," + NL +
             "                W_pred=({k:round(float(Wpe@PAT[k])+float(Wke@kenyon(PAT[k])),3) for k in PAT} if eta_pred else None),Wpe=[round(float(x),3) for x in Wpe])",
             etiqueta='salidas v13a')
    cab = ('"""organismo_v13a = organismo/organismo_v13.py (' + SHA_V13 + ', TRONCO) + MODELO DE SI MISMO minimo:' + NL +
           'un predictor lineal de la energia que rinde el bocado (dE_pred = Wpe@retina + Wke@kenyon, regla delta a tasa eta_pred)' + NL +
           'y la SORPRESA |dE - dE_pred| como senal interna que modula la tasa de la via RAPIDA: eta_ef = eta*(1 + k_sorpresa*sorpresa).' + NL +
           'El predictor NO entra en valor() ni en la decision de la boca y NO consume el RNG del organismo: por eso con' + NL +
           'eta_pred>0 y k_sorpresa=0 la conducta es la de v13 bit a bit (SOLO MIDE). Con eta_pred=0 y k_sorpresa=0 es v13 EXACTO.' + NL +
           'Control RUIDO (sorpresa_barajada=True): misma magnitud de modulacion, barajada en el tiempo con RNG propio.' + NL +
           'Salidas nuevas: sorpresa_media/error_pred/eta_media/bocados por cuarto, sorpresa_pre/post y eta_pre/post en ventana' + NL +
           'fina, t_ext_B, mord_post, deaths_post, W_pred.' + NL +
           'Preregistro: experimentos/nivel9_allostasis/PREREGISTRO_allostasis.md. Generado por construye_allostasis.py. NO editar.' + NL +
           'RAMA exploratoria del bloque 6: no es tronco ni candidato a tronco.' + NL + '"""' + NL)
    d = os.path.join(AQUI, 'organismo_v13a.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    return d


def v13ag():
    s = origen(os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py'), SHA_V13G)
    s = sust(s, "eta_s=0.0,clip_s=3.0,puerta=None,mundo='AB'", "eta_s=0.0,clip_s=3.0,puerta=None," + PERILLAS + ",mundo='AB'", etiqueta='firma v13ag')
    s = comun(s, 'P_')
    s = sust(s, "W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns],mundo=mundo",
             "W_lenta=W_lenta,Wps=[round(float(x),3) for x in Wps],Wns=[round(float(x),3) for x in Wns]," + NL +
             NL.join(SALIDAS) + NL + "                mundo=mundo", etiqueta='salidas v13ag')
    cab = ('"""organismo_v13ag = experimentos/v13_dos_vias/organismo_v13g.py (' + SHA_V13G + ', mundo de regla) + el mismo' + NL +
           'predictor de dE y la misma modulacion eta_ef que organismo_v13a.py (MISMAS ANCLAS). Sirve para medir' + NL +
           'generalizacion px0/azar (G1/G2 de organismo/bateria_generaliza.py) con las perillas de cada brazo.' + NL +
           'Con eta_pred=0 y k_sorpresa=0 es organismo_v13g EXACTO. Generado por construye_allostasis.py. NO editar.' + NL + '"""' + NL)
    d = os.path.join(AQUI, 'organismo_v13ag.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    return d


if __name__ == '__main__':
    print(f"  origen organismo_v13.py  {SHA_V13}   (congelado, solo lectura)")
    print(f"  origen organismo_v13g.py {SHA_V13G}")
    for f in (v13a, v13ag):
        d = f()
        print(f"  {os.path.relpath(d, RAIZ).replace(os.sep, '/'):48s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
