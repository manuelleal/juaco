"""Bloque "PROBAR CUANDO NO ME RECONOZCO" (C-P1) — constructor POR ANCLAS del instrumento del experimento.

  organismo_v13p.py  <- organismo/organismo_v13.py                    (cc8b16b492d4d324, TRONCO CONGELADO: se lee, no se toca)
  organismo_v13pg.py <- experimentos/v13_dos_vias/organismo_v13g.py   (2a80e125f8593bf2, mundo de regla; MISMAS anclas)

Linaje del instrumento (cada eslabon con sha y con identidad bit a bit):
  organismo_v13.py (cc8b16b492d4d324)
    -> experimentos/creacion_C/organismo_v13s.py (2eaba8dde27f05bd)  AUTOMODELO + `k_test` + `test_fijo`   [I1/I2/I3 18/18]
    -> organismo_v13p.py                                              + predictor de dE en la BOCA + traza MOMENTO + mord_post

Los bloques del AUTOMODELO se IMPORTAN de experimentos/creacion_C/construye_selfmodel.py (no se copian): asi el codigo
que se corre aqui es, byte a byte, el que paso I1/I2/I3. Lo que este constructor anade encima es SOLO:

  1. **Predictor de dE del bloque 6** (`Wpe`, `Wke`, regla delta a `eta_pred`, copiado de organismo_v13a) con su EMA
     `_sbarE`, que aqui **NO modula eta**: entra en la BOCA con ganancia `k_testE`. Sirve para separar
     "QUE sorpresa" (la del mundo o la de si mismo) de "DONDE entra" (la tasa o la boca).
  2. **Traza temporal** `traza_s`: la media de `s_barra` en `n_traza` cubetas de `T/n_traza` pasos (solo lectura), y su
     inyeccion `traza_ext` desplazada `desfase` cubetas con ganancia `k_testM` -> es el control **MOMENTO**:
     exactamente la MISMA cantidad de sesgo que aplico el brazo SELF-TEST de esa misma semilla, fuera de tiempo.
  3. `mord_post` (bocados de comida/veneno tras la inversion), para P6.

Perillas nuevas, todas apagadas por defecto: eta_pred=0, clip_e=3.0, ema_pred=0, k_testE=0, n_traza=0,
traza_ext=None, desfase=0, k_testM=0. Con TODAS apagadas el instrumento es v13s, y v13s es v13, bit a bit.

NO editar los generados a mano.  Uso:  python experimentos/nivel9_probar_si_mismo/construye_probar.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'creacion_C'))
import construye_selfmodel as CS

NL = chr(10)
SHA_V13 = 'cc8b16b492d4d324'
SHA_V13G = '2a80e125f8593bf2'
SHA_V13S = '2eaba8dde27f05bd'

h16 = CS.h16
sust = CS.sust
origen = CS.origen

PERILLAS_EXTRA = ("eta_pred=0.0,clip_e=3.0,ema_pred=0.0,k_testE=0.0,n_traza=0,traza_ext=None,desfase=0,k_testM=0.0"
                  ",resta_cota=False,resta_lenta=False,ema_lento=0.0025")

ESTADO_EXTRA = [
    "    Wpe=np.zeros(6); Wke=np.zeros(NKMAX); _sbarE=0.; _srE=0.   # v13p: predictor de dE (bloque 6, copiado). Aqui NO modula eta: entra en la BOCA",
    "    _trzs=[0.]*max(n_traza,1); _trzn=[0]*max(n_traza,1); _sm=0.   # v13p: traza de s_barra por cubeta y sesgo inyectado (control MOMENTO)",
    "    mord_post={'comida':0,'veneno':0}   # v13p: bocados tras la inversion (P6)",
    "    _fbar=0.; _fS=0.   # v13p (ENMIENDA 2): cota de oraculo 2b(1-b) y su EMA, con la MISMA ema_auto. Inerte si resta_cota=False",
    "    _sbarL=0.   # v13p (ENMIENDA 2): linea base LENTA de la propia sorpresa (ema_lento). Inerte si resta_lenta=False",
    "    t_primer_sesgo=None; _encps=0; _mordps=0   # v13p (ENMIENDA 2): latencia del primer sesgo > 0.05 tras la inversion (solo lectura)",
]

# Se inserta al INICIO del paso, antes del bloque de h pasos: la traza y el sesgo inyectado dependen solo de t.
BLOQUE_PASO_EXTRA = [
    "        if n_traza:   # v13p: traza de la sorpresa sobre si mismo en n_traza cubetas de T/n_traza pasos (solo lectura)",
    "            _ib=min(t*n_traza//T,n_traza-1); _trzs[_ib]+=_sbar; _trzn[_ib]+=1",
    "            if traza_ext is not None: _sm=k_testM*float(traza_ext[(_ib+desfase)%n_traza])   # MOMENTO: el mismo sesgo, desplazado `desfase` cubetas",
]

# Se inserta dentro de `if mordio:` / `if learn:`, justo antes del reparto de error de v13 (el predictor solo existe al morder).
def bloque_pred(pat):
    return [
        "                    if eta_pred:   # v13p: predictor de dE (bloque 6): objetivo E_VAL nominal, regla delta, tasa propia",
        f"                        _dEp=float(Wpe@{pat}[kk])+float(Wke@kc); _ee=E_VAL[val[kk]]-_dEp; _srE=abs(_ee)",
        f"                        Wpe=np.clip(Wpe+eta_pred*_ee*{pat}[kk],-clip_e,clip_e); Wke=np.clip(Wke+eta_pred*_ee*kc,-clip_e,clip_e)",
        "                        if ema_pred: _sbarE=(1.-ema_pred)*_sbarE+ema_pred*_srE   # causal: lo usa la boca del PROXIMO encuentro",
    ]

SALIDA_EXTRA = [
    "                traza_s=([round(_trzs[i]/_trzn[i],6) if _trzn[i] else 0.0 for i in range(n_traza)] if n_traza else None),",
    "                mord_post=mord_post,sbarE=round(float(_sbarE),5),fbar=round(float(_fbar),6),sbarL=round(float(_sbarL),6),",
    "                t_primer_sesgo=t_primer_sesgo,enc_post_hasta_sesgo=_encps,mord_post_hasta_sesgo=_mordps,",
]

CAB = ('"""organismo_v13p = organismo_v13s (2eaba8dde27f05bd) + predictor de dE del bloque 6 entrando en la BOCA' + NL +
       '(k_testE), traza temporal de la sorpresa sobre si mismo e inyeccion desplazada (control MOMENTO), y mord_post.' + NL +
       'Linaje: organismo_v13.py (cc8b16b492d4d324) -> organismo_v13s.py (2eaba8dde27f05bd) -> este.' + NL +
       'Con TODAS las perillas nuevas apagadas es v13s, y v13s con las suyas apagadas es v13, bit a bit (J1..J6).' + NL +
       'ENMIENDA 2: perillas resta_cota (excede la cota de oraculo 2b(1-b)) y resta_lenta (excede una linea base' + NL +
       'lenta de la propia sorpresa, ema_lento), y el campo' + NL +
       't_primer_sesgo (latencia del primer sesgo > 0.05 tras la inversion; solo lectura).' + NL +
       'Preregistro: experimentos/nivel9_probar_si_mismo/PREREGISTRO_probar_si_mismo.md.' + NL +
       'Generado por experimentos/nivel9_probar_si_mismo/construye_probar.py. NO editar a mano.' + NL + '"""' + NL)


def construye(src_rel, dst_rel, sha, pat, firma_vieja, cab_extra=''):
    txt = origen(os.path.join(RAIZ, src_rel), sha)

    # 1) cabecera
    fin = txt.index('"""', 3) + 3
    txt = CAB[:-4] + cab_extra + '"""' + NL + txt[fin:].lstrip(NL)

    # 2) firma: perillas del automodelo (importadas) + las nuevas
    txt = sust(txt, firma_vieja, firma_vieja[:-2] + f",{CS.PERILLAS},{PERILLAS_EXTRA}):", etiqueta='firma')

    # 3) estado: el del automodelo (importado) + el nuevo
    ancla_estado = "    Wps=np.zeros(6); Wns=np.zeros(6)"
    linea_estado = [l for l in txt.splitlines() if l.startswith(ancla_estado)]
    if len(linea_estado) != 1:
        raise SystemExit(f"ANCLA estado: {len(linea_estado)} lineas, se esperaba 1. Abortado.")
    txt = sust(txt, linea_estado[0], linea_estado[0] + NL + NL.join(CS.ESTADO + ESTADO_EXTRA), etiqueta='estado')

    # 4) boca + bloque del automodelo (importado), con los dos sumandos nuevos
    ancla_boca = "            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb"
    nueva_boca = ("            _sg=(k_test*(max(0.,_sbar-_fbar) if resta_cota else (max(0.,_sbar-_sbarL) if resta_lenta else _sbar)) if k_test else 0.)"
                  "+(k_testE*_sbarE if k_testE else 0.)+test_fijo+_sm   "
                  "# v13p: GANAS DE PROBAR — el sesgo de la boca. resta_cota: EXCESO sobre la cota de oraculo 2b(1-b)" + NL +
                  "            Vb=alpha*_wt+hambre_boca*hambre+.5+_sg; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb" + NL +
                  "            if invertir_en is not None and t>=invertir_en and t_primer_sesgo is None:   # v13p (ENMIENDA 2): latencia, solo lectura" + NL +
                  "                _encps+=1; _mordps+=int(mordio)" + NL +
                  "                if _sg>0.05: t_primer_sesgo=t")
    bloque = NL.join(l.replace('{pat}', pat) for l in CS.BLOQUE)
    bloque = bloque.replace("_tq[q(t)]+=(k_test*_sbar if k_test else 0.)+test_fijo", "_tq[q(t)]+=_sg")
    bloque = bloque.replace("            _sa=0.", "            _sa=0.; _fS=0.")
    bloque = bloque.replace("_bd=0 if (_BLO<=_wt<=_BHI) else 1; _cl=int(_y)",
                            "_bd=0 if (_BLO<=_wt<=_BHI) else 1; _cl=int(_y); _fS=2.*float(_bS)*(1.-float(_bS))")
    bloque = bloque.replace("if ema_auto: _sbar=(1.-ema_auto)*_sbar+ema_auto*_sa",
                            "if ema_auto: _sbar=(1.-ema_auto)*_sbar+ema_auto*_sa; _fbar=(1.-ema_auto)*_fbar+ema_auto*_fS; _sbarL=(1.-ema_lento)*_sbarL+ema_lento*_sa")
    for _t, _n in (("_tq[q(t)]+=_sg", 1), ("_sa=0.; _fS=0.", 1), ("_fS=2.*float(_bS)", 1), ("_fbar=(1.-ema_auto)*_fbar", 1)):
        if bloque.count(_t) != _n:
            raise SystemExit(f"ANCLA del automodelo {_t!r}: {bloque.count(_t)} veces, se esperaba {_n}. Abortado.")
    txt = sust(txt, ancla_boca, nueva_boca + NL + bloque, etiqueta='boca')

    # 5) paso: traza/sesgo inyectado + automodelo a h pasos (importado)
    ancla_paso = f"        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat={pat}[k]"
    bloque_h = NL.join(l.replace('{pat}', pat) for l in CS.BLOQUE_H)
    txt = sust(txt, ancla_paso, ancla_paso + NL + NL.join(BLOQUE_PASO_EXTRA) + NL + bloque_h, etiqueta='paso')

    # 6) predictor de dE, dentro de if mordio / if learn, antes del reparto de error
    ancla_dlt = "                    dlt=R-_wt if puerta is None else R-_wf"
    linea_dlt = [l for l in txt.splitlines() if l.startswith(ancla_dlt)][0]
    txt = sust(txt, linea_dlt, NL.join(bloque_pred(pat)) + NL + linea_dlt, etiqueta='predictor')

    # 7) contadores del bocado (automodelo, importado) + mord_post
    ancla_nb = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1"
    txt = sust(txt, ancla_nb, ancla_nb + "; _nbw+=1; _etaq[q(t)]+=_eta/eta; _nqm[q(t)]+=1"
               + "; mord_post[val[kk]]+=int(invertir_en is not None and t>=invertir_en)", etiqueta='bocado')

    # 8) eta -> _eta (las CUATRO del automodelo; aqui k_auto queda apagado en todos los brazos, pero la perilla existe)
    for viejo, nuevo, et in (
            ("if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())", "if dlt>0: _trunca=bool(((Wp[_ix]+_eta*dlt)>3.0).any())", 'trunca+'),
            ("else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())", "else:     _trunca=bool(((Wn[_ix]+_eta*aversion*(-dlt))>3.0).any())", 'trunca-'),
            ("if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)", "if dlt>0: Wp=np.clip(Wp+_eta*dlt*kc,0,3.)", 'Wp'),
            ("else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)", "else:     Wn=np.clip(Wn+_eta*aversion*(-dlt)*kc,0,3.)", 'Wn')):
        txt = sust(txt, viejo, nuevo, etiqueta=et)

    # 9) recuperacion (t_ext_B, mismo criterio del bloque 6) y muertes tras la inversion
    ancla_r = "        _prev_on=pos if pos in objs else -1"
    linea_r = [l for l in txt.splitlines() if l.startswith(ancla_r)][0]
    txt = sust(txt, linea_r,
               f"        if invertir_en is not None and t>=invertir_en and t_ext_B is None and valor({pat}['B'])>=0: t_ext_B=t   # v13p: M1 del bloque 6 (no consume RNG)"
               + NL + linea_r, etiqueta='t_ext_B')
    ancla_d = "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))"
    txt = sust(txt, ancla_d, "        if E<=0:" + NL + "            deaths+=1; E=.6; pos=int(rng.integers(L))" + NL +
               "            if invertir_en is not None and t>=invertir_en: deaths_post+=1   # v13p", etiqueta='deaths_post')

    # 10) salidas: las del automodelo (importadas) + las nuevas
    ancla_sal = "Wns=[round(float(x),3) for x in Wns]"
    salida = NL.join(l.replace('{pat}', pat) for l in CS.SALIDA + SALIDA_EXTRA)
    txt = sust(txt, ancla_sal, ancla_sal + "," + NL + salida.rstrip().rstrip(','), etiqueta='salida')

    dst = os.path.join(RAIZ, dst_rel)
    open(dst, 'w', encoding='utf-8', newline=NL).write(txt)
    print(f"  {dst_rel}  sha {h16(dst)}  ({len(txt.splitlines())} lineas)")


if __name__ == '__main__':
    print("Constructor por anclas — PROBAR CUANDO NO ME RECONOZCO (C-P1)")
    print(f"  bloques del automodelo importados de construye_selfmodel.py  sha {h16(os.path.join(RAIZ, 'experimentos', 'creacion_C', 'construye_selfmodel.py'))}")
    print(f"  origen organismo/organismo_v13.py  sha {SHA_V13} OK")
    construye('organismo/organismo_v13.py', 'experimentos/nivel9_probar_si_mismo/organismo_v13p.py',
              SHA_V13, 'PAT', "eta_s=0.015,clip_s=3.0,puerta=3):")
    print(f"  origen experimentos/v13_dos_vias/organismo_v13g.py  sha {SHA_V13G} OK")
    construye('experimentos/v13_dos_vias/organismo_v13g.py', 'experimentos/nivel9_probar_si_mismo/organismo_v13pg.py',
              SHA_V13G, 'P_', "eta_s=0.0,clip_s=3.0,puerta=None,mundo='AB',regla='px0',fase2_en=None,sonda_final=False):",
              cab_extra='NOTA: en mundo="regla" `invertir_en` es None en todos los brazos, asi que la linea de t_ext_B'
                        + NL + '(que mira P_["B"]) nunca se evalua. Es la misma premisa que usa el bloque 6 con v13ag.' + NL)
    print("Listo. Identidades: python experimentos/nivel9_probar_si_mismo/identidad_probar.py")
