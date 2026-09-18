"""CREADOR C — constructor POR ANCLAS del instrumento de APRENDER SIN MORDER (codificacion predictiva).

  organismo_v14pc.py <- organismo/organismo_v14g.py   (1f1318480cd34cde: mundo de regla sobre el TRONCO v14; se lee, no se toca)

Que anade, y nada mas:

1. **Predictor de dE** (el del bloque 6, copiado literal): `dE_pred(P) = Wpe@P + Wke@kenyon(P)`, regla delta a `eta_pred`
   sobre el objetivo NOMINAL `E_VAL[valencia]`, y **solo al morder** (es donde existe dE). No decide nada.

2. **CONSOLIDACION POR CODIFICACION PREDICTIVA (`eta_c`), en CADA ENCUENTRO, muerda o no.** La via LENTA deja de
   aprender solo de los bocados: su objetivo pasa a ser lo que el predictor dice que va a SENTIR, llevado a unidades de
   R con las constantes del propio mundo (sin ningun parametro libre):

       obj_R(P) = (R_VAL['comida']/E_VAL['comida']) * dE_pred(P)   si dE_pred > 0      (+0.8 -> +1.0)
                  (R_VAL['veneno']/E_VAL['veneno']) * dE_pred(P)   si dE_pred <= 0     (-0.4 -> -3.0)
       eps      = obj_R(P) - (Wps-Wns)@P            <- error de codificacion predictiva de la via lenta
       Wps/Wns += eta_c * eps * CREDITO             <- con el MISMO drenaje lam y el MISMO tope clip_s de la via lenta

   El predictor esta anclado en consecuencias REALES (se entrena con lo que el cuerpo sintio al morder) y generaliza a
   patrones no mordidos: por eso esto no es auto-confirmacion. Guarda: no consolida hasta que el predictor tenga
   `n_pred_min` bocados (por defecto 20; el orden en que W_pred llega al 93.5% del objetivo, medido en la mini-prueba
   C2-a del puente: 14 bocados). Declarado, no buscado.

3. **CANAL DE RETORNO (`canal`) — la pregunta de feedback alignment.** El maestro vive en el espacio de las CELDAS
   (90) y el alumno en el de los PIXELES (6). Quien lleva el error de un espacio al otro:

       'directo'  CREDITO = P                 el gradiente exacto en una capa (linea base)
       'transp'   CREDITO = KW.T @ kenyon(P)  los pesos transpuestos: lo que haria backprop
       'fa'       CREDITO = B @ kenyon(P)     canal FIJO y ALEATORIO (6xNKMAX, RNG propio seed+600000): feedback alignment
       'fa_shuf'  CREDITO = B @ kenyon(P_previo)   CONTROL: misma magnitud, emparejamiento codigo<->credito equivocado

4. **EXPOSICIONES HASTA CRITERIO** (la medida que manda, decision del director 05:10): cada `probe_cada` pasos de la
   fase 1 se sondea, SIN tocar nada, el acierto de signo BALANCEADO de la via lenta sobre los patrones de TEST (nunca
   vistos) y se anota cuantos ENCUENTROS y cuantos BOCADOS de entrenamiento se llevaban. `expo_criterio` = los
   encuentros de la primera sonda que cruza `crit_expo` **y se sostiene en la siguiente** (dos seguidas, para que un
   cruce con suerte no cuente).

Con `eta_c=0`, `eta_pred=0` y `probe_cada=0` es organismo_v14g EXACTO (identidad K1).
NO editar el generado a mano.  Uso:  python experimentos/creacion_C/construye_codpred.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
NL = chr(10)
SHA_V14G = '1f1318480cd34cde'


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


CAB = ('"""organismo_v14pc = organismo/organismo_v14g.py (1f1318480cd34cde, mundo de regla sobre el TRONCO v14)' + NL +
       '+ APRENDER SIN MORDER: predictor de dE (bloque 6) + CONSOLIDACION POR CODIFICACION PREDICTIVA de la via lenta' + NL +
       'en CADA ENCUENTRO, con canal de retorno elegible (directo / transpuesta / feedback alignment / control), y la' + NL +
       'medida EXPOSICIONES HASTA CRITERIO. Con eta_c=0, eta_pred=0 y probe_cada=0 es organismo_v14g EXACTO.' + NL +
       'Generado por experimentos/creacion_C/construye_codpred.py. NO editar. RAMA de creacion: no es tronco.' + NL + '"""' + NL)

PERILLAS = "eta_pred=0.0,clip_e=3.0,eta_c=0.0,canal='directo',n_pred_min=20,probe_cada=0,crit_expo=0.90"

ESTADO = [
    "    Wpe=np.zeros(6); Wke=np.zeros(NKMAX); _npred=0   # v14pc: predictor de dE (bloque 6). Solo aprende al morder; no decide nada",
    "    _kprev=np.zeros(NKMAX); _B=None   # v14pc: codigo anterior (control fa_shuf) y CANAL DE RETORNO fijo y aleatorio",
    "    if eta_c and canal in ('fa','fa_shuf'):   # RNG PROPIO: no toca el del organismo",
    "        _B=np.random.default_rng(seed+600000).normal(0.,1.,(6,NKMAX))/np.sqrt(float(NKMAX))",
    "    _enc_tr=0; _mor_tr=0; _curva=[]; _expo=None; _expo_m=None; acc_lenta_f2=None   # v14pc: exposiciones hasta criterio (solo lectura)",
    "    def _acc_lenta():   # v14pc: acierto de signo BALANCEADO de la via LENTA sobre los patrones de TEST (nunca vistos). No consume RNG",
    "        if mundo=='AB' or not test: return None",
    "        _W=Wps-Wns",
    "        _f=[1.0 if float(_W@P_[_k])>0 else (0.5 if float(_W@P_[_k])==0 else 0.0) for _k in test if val_regla[_k]=='comida']",
    "        _p=[1.0 if float(_W@P_[_k])<0 else (0.5 if float(_W@P_[_k])==0 else 0.0) for _k in test if val_regla[_k]=='veneno']",
    "        return (0.5*float(np.mean(_f))+0.5*float(np.mean(_p))) if (_f and _p) else None",
]

# Sonda de exposiciones: al inicio del paso, solo en la fase 1 (antes de que entren los de test)
BLOQUE_SONDA = [
    "        if probe_cada and mundo!='AB' and t%probe_cada==0 and t<fase2_en:   # v14pc: EXPOSICIONES HASTA CRITERIO (solo lectura)",
    "            _ac=_acc_lenta()",
    "            if _ac is not None:",
    "                _curva.append((t,_enc_tr,_mor_tr,round(_ac,4)))",
    "                if _expo is None and _ac>=crit_expo and len(_curva)>=2 and _curva[-2][3]>=crit_expo:",
    "                    _expo=_curva[-2][1]; _expo_m=_curva[-2][2]   # dos sondas seguidas sobre el criterio: cuenta la PRIMERA",
]

# Consolidacion: en el encuentro, con kc/_wf/_ws ya calculados y ANTES de que la boca decida
BLOQUE_CONSOL = [
    "            if mundo!='AB' and t<fase2_en: _enc_tr+=1   # v14pc: exposicion de entrenamiento",
    "            if eta_c and _npred>=n_pred_min:   # v14pc: CONSOLIDACION POR CODIFICACION PREDICTIVA, en CADA encuentro (muerda o no)",
    "                _dEp=float(Wpe@P_[kk])+float(Wke@kc)",
    "                _obj=(R_VAL['comida']/E_VAL['comida'])*_dEp if _dEp>0 else (R_VAL['veneno']/E_VAL['veneno'])*_dEp",
    "                _eps=_obj-_ws",
    "                if canal=='directo': _cr=P_[kk]",
    "                elif canal=='transp': _cr=KW.T@kc",
    "                elif canal=='fa': _cr=_B@kc",
    "                else: _cr=_B@_kprev   # control: el credito del codigo ANTERIOR (misma magnitud, emparejamiento equivocado)",
    "                if lam: _mc=np.minimum(Wps,Wns)*(P_[kk]>0); Wps=Wps-lam*_mc; Wns=Wns-lam*_mc",
    "                if _eps>0: Wps=np.clip(Wps+eta_c*_eps*_cr,0,clip_s)",
    "                else:      Wns=np.clip(Wns+eta_c*aversion*(-_eps)*_cr,0,clip_s)",
    "            _kprev=kc",
]

# Predictor de dE: dentro de if mordio / if learn, antes del reparto de error de v13
BLOQUE_PRED = [
    "                    if eta_pred:   # v14pc: predictor de dE (bloque 6), objetivo NOMINAL E_VAL. Solo al morder",
    "                        _dEq=float(Wpe@P_[kk])+float(Wke@kc); _ee=E_VAL[val[kk]]-_dEq",
    "                        Wpe=np.clip(Wpe+eta_pred*_ee*P_[kk],-clip_e,clip_e); Wke=np.clip(Wke+eta_pred*_ee*kc,-clip_e,clip_e)",
    "                        _npred+=1",
]

SALIDA = [
    "                expo_criterio=_expo,expo_criterio_bocados=_expo_m,curva_expo=_curva,",
    "                acc_lenta_f2=acc_lenta_f2,acc_lenta_fin=_acc_lenta(),enc_tren=_enc_tr,mord_tren=_mor_tr,",
    "                n_pred=_npred,W_pred=({_k:round(float(Wpe@P_[_k])+float(Wke@kenyon(P_[_k])),3) for _k in P_} if eta_pred else None),",
    "                canal=canal",
]


def construye():
    src = os.path.join(RAIZ, 'organismo', 'organismo_v14g.py')
    real = h16(src)
    if real != SHA_V14G:
        raise SystemExit(f"ORIGEN organismo_v14g.py: sha {real}, se esperaba {SHA_V14G}. Abortado.")
    txt = open(src, encoding='utf-8').read()

    fin = txt.index('"""', 3) + 3
    txt = CAB + txt[fin:].lstrip(NL)

    txt = sust(txt, "pat_shuf=0,pat_min=0):", f"pat_shuf=0,pat_min=0,{PERILLAS}):", etiqueta='firma')

    ancla_estado = "    Wps=np.zeros(6); Wns=np.zeros(6)"
    linea = [l for l in txt.splitlines() if l.startswith(ancla_estado)][0]
    txt = sust(txt, linea, linea + NL + NL.join(ESTADO), etiqueta='estado')

    ancla_paso = "        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=P_[k]"
    txt = sust(txt, ancla_paso, NL.join(BLOQUE_SONDA) + NL + ancla_paso, etiqueta='sonda')

    ancla_enc = "            kk=objs[pos]; kc=kenyon(P_[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@P_[kk])"
    linea_enc = [l for l in txt.splitlines() if l.startswith(ancla_enc)][0]
    txt = sust(txt, linea_enc, linea_enc + NL + NL.join(BLOQUE_CONSOL), etiqueta='consolidacion')

    ancla_dlt = "                    dlt=R-_wt if puerta is None else R-_wf"
    linea_dlt = [l for l in txt.splitlines() if l.startswith(ancla_dlt)][0]
    txt = sust(txt, linea_dlt, NL.join(BLOQUE_PRED) + NL + linea_dlt, etiqueta='predictor')

    ancla_bocado = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1"
    txt = sust(txt, ancla_bocado, ancla_bocado + "; _mor_tr+=int(mundo!='AB' and t<fase2_en)", etiqueta='bocado')

    ancla_f2 = "            W_apriori={_k:valor(P_[_k]) for _k in P_}"
    txt = sust(txt, ancla_f2, ancla_f2 + NL + "            acc_lenta_f2=_acc_lenta()   # v14pc: el acierto de la via LENTA justo antes de que entren los de test",
               etiqueta='fase2')

    ancla_sal = "Wns=[round(float(x),3) for x in Wns]"
    txt = sust(txt, ancla_sal, ancla_sal + "," + NL + NL.join(SALIDA), etiqueta='salida')

    dst = os.path.join(AQUI, 'organismo_v14pc.py')
    open(dst, 'w', encoding='utf-8', newline=NL).write(txt)
    print(f"  experimentos/creacion_C/organismo_v14pc.py  sha {h16(dst)}  ({len(txt.splitlines())} lineas)")


if __name__ == '__main__':
    print("Constructor por anclas — APRENDER SIN MORDER (codificacion predictiva), creador C")
    print(f"  origen organismo/organismo_v14g.py  sha {SHA_V14G} OK")
    construye()
    print("Listo. Identidad: python experimentos/creacion_C/identidad_codpred.py")
