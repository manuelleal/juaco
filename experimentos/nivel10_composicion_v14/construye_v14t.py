"""Construye organismo_v14t.py = organismo_v14c.py (HIJA DISPERSA + PUERTA POR CODIGO, ya compuestas por
construye_v14c.py) + LA TERCERA PERILLA: "la sorpresa del mundo en la boca" (predictor de dE del bloque 6 entrando
en la BOCA, k_testE; registro/PROPUESTA_v14.md, segundo candidato, dosis 5 = el punto de organismo_v13E_k5.py).

Linaje del tercer parche (TODO leido, NUNCA editado -- son instrumentos YA CORRIDOS o CONGELADOS):
  organismo/organismo_v13.py                                                          (CONGELADO, cc8b16b492d4d324)
    -> experimentos/creacion_C/construye_selfmodel.py       -> organismo_v13s.py       AUTOMODELO (SELF/MUNDO/H_SHUF)
                                                                                         + k_test/test_fijo (I1/I2/I3)
    -> experimentos/nivel9_probar_si_mismo/construye_probar.py -> organismo_v13p.py    + predictor de dE en la BOCA
                                                                                         (k_testE) + MOMENTO + mord_post
    -> experimentos/nivel9_probar_si_mismo/construye_v13E.py --k 5 -> organismo_v13E_k5.py   dE-TEST fijo ON, k_testE=5

Los parches de ESOS DOS constructores (construye_selfmodel.py, construye_probar.py) se IMPORTAN como DATOS -- las
listas/constantes de texto CS.PERILLAS/ESTADO/BLOQUE/BLOQUE_H/SALIDA y CP.PERILLAS_EXTRA/ESTADO_EXTRA/
BLOQUE_PASO_EXTRA/bloque_pred()/SALIDA_EXTRA -- NUNCA reescritas a mano (se leen con `import construye_probar as
CP; CS = CP.CS`, exactamente los objetos que ya pasaron identidad_probar.py e identidad_v13E.py). Lo que SI se
reproduce a mano, leido linea a linea de construye_probar.py (iguales razones que construye_v14c.py reproduciendo
las anclas de pon_hija()/pon_puerta() que viven dentro de su __main__): la SECUENCIA de sust() que aplica esos
datos sobre el texto. construye_probar.py no expone un pon_X(texto)->texto reusable -- su construye() hace I/O de
archivo directo (lee con origen(), escribe con open().write()) -- asi que aqui se reescribe como pon_dE(), funcion
PURA de texto, para poder encadenarla DESPUES de compone() de construye_v14c.py (que tampoco es importable con la
firma que hace falta: opera sobre organismo_v13.py/v13g.py, no sobre organismo_v14c.py/v14gc.py ya compuestos).

DECLARADO (lo que pide el encargo): el automodelo SELF/MUNDO/H_SHUF de construye_selfmodel.py viene ENTRELAZADO
con el predictor de dE -- el propio construye() de construye_probar.py los aplica JUNTOS: CS.ESTADO se inserta en
el MISMO punto que ESTADO_EXTRA (tras la via lenta), y el `_sg` de la boca (que trae `k_testE*_sbarE`) esta escrito
en la MISMA insercion que CS.BLOQUE (que calcula `_sbar`, la sorpresa sobre si mismo -- solo la usa `k_test`, que
aqui se queda apagado). Separarlos exigiria reescribir construye_probar.py a mano (prohibido: instrumento ya
corrido, EQUIPO.md regla 1). Por eso el automodelo SELF entero viaja tambien aqui, con TODAS sus perillas en su
default APAGADO (eta_b, k_auto, ema_auto, k_test, test_fijo, buf_auto, clip_b, eta_e, h_pred, buf_e), mas las de
MOMENTO/ENMIENDA2 (n_traza, traza_ext, desfase, k_testM, resta_cota, resta_lenta, ema_lento) -- NINGUNA de estas
DIEZ SIETE se enciende jamas en organismo_v14t_on.py. Las TRES perillas propias de v14t son solo: `mask_rel`
(hija dispersa), `puerta_pat`+`pat_min` (puerta por codigo, PATC) y el TRIO que se mueve junto `eta_pred`+
`ema_pred`+`k_testE` (dE-TEST, dosis 5 -- el punto de organismo_v13E_k5.py).

COLISION DE ANCLAS (declarada y resuelta, verificada por CONTEO EXACTO tras cada parche -- una sola real, igual
que en construye_v14c.py): la FIRMA. construye_probar.py usa como ancla el ULTIMO texto de la firma de
organismo_v13.py/organismo_v13g.py ("...puerta=3):" / "...sonda_final=False):"), que ya NO EXISTE en
organismo_v14c.py/organismo_v14gc.py (compone() de construye_v14c.py ya lo reemplazo por
"...puerta=3,mask_rel=0,...,pat_min=0):" / "...sonda_final=False,mask_rel=0,...,pat_min=0):"). Se resuelve EXACTO
como compone() resolvio la suya: pon_dE() recibe el texto YA parchado por v14c/v14gc como SU ancla_firma (no el
original de v13/v13g). Las OTRAS NUEVE anclas de construye_probar.py se verificaron UNA A UNA leyendo
organismo_v14c.py y organismo_v14gc.py enteros ANTES de escribir este constructor: NINGUNA otra colisiona.
  - estado (Wps/Wns) y bocado (R=R_VAL[val[kk]];...;mord[kk][q(t)]+=1) son puntos de insercion COMPARTIDOS con
    hija dispersa/puerta por codigo -- ya resueltos por v14c (cada parche solo AGREGA texto justo tras el ancla,
    sin tocar el ancla misma; la ancla la sigue encontrando exactamente una vez la insercion siguiente). Aqui se
    reutiliza el MISMO patron: pon_dE() es la TERCERA insercion sobre esas dos anclas compartidas.
  - la linea de la boca (Vb=...;pb=...;mordio=...), la de "paso" (hambre=...;pat=PAT[k]/P_[k]), la de "dlt" (donde
    se ancla el predictor de dE), las CUATRO de eta->_eta, y las de t_ext_B/deaths_post/salida quedan BIT A BIT
    identicas a organismo_v13.py/organismo_v13g.py dentro de organismo_v14c.py/organismo_v14gc.py: ni hija dispersa
    ni puerta por codigo las tocan. pon_dE() las usa tal cual, sin adaptar nada.

Salidas (las TRES perillas APAGADAS por defecto en todo lo que no diga "_on" -> organismo_v13/v13g EXACTOS bit a
bit; arnes obligatorio: identidad_v14t.py):

  organismo_v14t.py          <- organismo_v14c.py                          (649851c0f10c3cd6)
  organismo_v14t_on.py       <- organismo_v14t.py, las TRES perillas fijas ON (mask_rel=2; puerta_pat=5,pat_min=1;
                                 eta_pred=0.03,ema_pred=0.05,k_testE=5.0 -- el punto de organismo_v13E_k5.py)
  organismo_v14gt.py         <- organismo_v14gc.py                         (dcca1ab79d86289b)   mundo de regla
  bateria_v14t.py            <- organismo/bateria_v13.py                   (1a027bcb37eb536e)   SOLO el modulo
                                 (organismo_v14t_on) + ERR-30 (criterio 5 apaga TAMBIEN k_testE/eta_pred, como
                                 bateria_v13E.py -- mask_rel/puerta_pat NO se apagan explicitamente: mismo
                                 argumento estructural (puerta_pat, con puerta=None) + empirico (mask_rel=2, ya
                                 validado por bateria_v14c.py en este mundo) que uso construye_v14c.py; sigue
                                 siendo PREDICCION para el trio, declarada como control que puede fallar)
  bateria_generaliza_v14t.py <- organismo/bateria_generaliza.py            (46772f5a582872c8)   SOLO el modulo

Uso:  python experimentos/nivel10_composicion_v14/construye_v14t.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
D9 = os.path.join(RAIZ, 'experimentos', 'nivel9_probar_si_mismo')
DC = os.path.join(RAIZ, 'experimentos', 'creacion_C')
# organismo/ PRIMERO en sys.path (ERR-28), aunque aqui no importamos organismo_v13 en tiempo de construccion
# (solo se lee como texto): es la regla para todo runner de este repo, sin excepcion.
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), D9, DC]

import construye_probar as CP   # trae PERILLAS_EXTRA, ESTADO_EXTRA, BLOQUE_PASO_EXTRA, bloque_pred(), SALIDA_EXTRA
CS = CP.CS                      # construye_selfmodel: PERILLAS, ESTADO, BLOQUE, BLOQUE_H, SALIDA (automodelo, ver docstring)

NL = chr(10)


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


SHA_V14C = '649851c0f10c3cd6'
SHA_V14GC = 'dcca1ab79d86289b'
SHA_BATERIA_V13 = '1a027bcb37eb536e'
SHA_BATERIA_GENERALIZA = '46772f5a582872c8'

# firma YA compuesta por compone() de construye_v14c.py (hija dispersa + puerta por codigo, las DOS apagadas) --
# es la ancla ADAPTADA que resuelve la (unica) colision declarada arriba.
FIRMA_V14C_OFF = "puerta=3,mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=0,pat_shuf=0,pat_min=0):"
FIRMA_V14GC_OFF = "sonda_final=False,mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=0,pat_shuf=0,pat_min=0):"


def pon_dE(s, ancla_firma_vieja, pat, etiqueta):
    """Aplica sobre `s` (ya compuesto por compone() de construye_v14c.py) la TERCERA perilla: automodelo
    (importado de CS, entrelazado, apagado por default) + predictor de dE en la boca (importado de CP). Reproduce,
    EN EL MISMO ORDEN, los pasos 2-10 de construye_probar.construye() (el paso 1, cabecera, lo hace el __main__ de
    este archivo -- igual que compone() de construye_v14c.py tampoco toca la cabecera). Los PAYLOADS se importan
    de CS/CP sin cambios; las anclas que no colisionan con v14c/v14gc se copian tal cual de construye_probar.py."""

    # 2) firma: la del automodelo (CS.PERILLAS) + las nuevas de dE (CP.PERILLAS_EXTRA) -- ANCLA ADAPTADA
    s = sust(s, ancla_firma_vieja, ancla_firma_vieja[:-2] + f",{CS.PERILLAS},{CP.PERILLAS_EXTRA}):",
             etiqueta=f'{etiqueta}: firma')

    # 3) estado: el del automodelo + el nuevo, tras la via LENTA (ancla COMPARTIDA con hija/puerta -- v14c ya
    #    demostro que agregar texto tras el ancla sin tocarla dejar la insercion SIGUIENTE encontrandola 1 vez)
    ancla_estado = "    Wps=np.zeros(6); Wns=np.zeros(6)"
    linea_estado = [l for l in s.splitlines() if l.startswith(ancla_estado)]
    if len(linea_estado) != 1:
        raise SystemExit(f"ANCLA {etiqueta}: estado: {len(linea_estado)} lineas, se esperaba 1. Abortado.")
    s = sust(s, linea_estado[0], linea_estado[0] + NL + NL.join(CS.ESTADO + CP.ESTADO_EXTRA),
             etiqueta=f'{etiqueta}: estado')

    # 4) boca: el sesgo _sg (k_testE*sbarE es la unica ganancia que se enciende en organismo_v14t_on.py; el resto
    #    de sumandos del automodelo quedan estructuralmente en 0 con sus perillas apagadas) + CS.BLOQUE con los
    #    MISMOS 4 reemplazos de texto que hace construye_probar.py (reproducidos aqui letra a letra)
    ancla_boca = "            Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb"
    nueva_boca = ("            _sg=(k_test*(max(0.,_sbar-_fbar) if resta_cota else (max(0.,_sbar-_sbarL) if resta_lenta else _sbar)) if k_test else 0.)"
                  "+(k_testE*_sbarE if k_testE else 0.)+test_fijo+_sm   "
                  "# v14t: GANAS DE PROBAR -- el sesgo de la boca (solo k_testE*sbarE se enciende en organismo_v14t_on.py)" + NL +
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
            raise SystemExit(f"ANCLA {etiqueta}: automodelo {_t!r}: {bloque.count(_t)} veces, se esperaba {_n}. Abortado.")
    s = sust(s, ancla_boca, nueva_boca + NL + bloque, etiqueta=f'{etiqueta}: boca')

    # 5) paso: traza/MOMENTO (solo lectura) + automodelo a h pasos (importado)
    ancla_paso = f"        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat={pat}[k]"
    bloque_h = NL.join(l.replace('{pat}', pat) for l in CS.BLOQUE_H)
    s = sust(s, ancla_paso, ancla_paso + NL + NL.join(CP.BLOQUE_PASO_EXTRA) + NL + bloque_h, etiqueta=f'{etiqueta}: paso')

    # 6) predictor de dE, dentro de if mordio/if learn, antes del reparto de error (funcion importada, ya
    #    parametrizada en `pat` -- nada que reproducir a mano aqui)
    ancla_dlt = "                    dlt=R-_wt if puerta is None else R-_wf"
    linea_dlt = [l for l in s.splitlines() if l.startswith(ancla_dlt)]
    if len(linea_dlt) != 1:
        raise SystemExit(f"ANCLA {etiqueta}: dlt: {len(linea_dlt)} lineas, se esperaba 1. Abortado.")
    s = sust(s, linea_dlt[0], NL.join(CP.bloque_pred(pat)) + NL + linea_dlt[0], etiqueta=f'{etiqueta}: predictor')

    # 7) contadores del bocado (automodelo) + mord_post -- ANCLA COMPARTIDA con la CUENTA de la puerta (v14c ya la
    #    deja encontrable 1 vez; aqui se agrega en LA MISMA linea via ';', antes de la CUENTA que sigue en la
    #    linea de abajo)
    ancla_nb = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1"
    s = sust(s, ancla_nb, ancla_nb + "; _nbw+=1; _etaq[q(t)]+=_eta/eta; _nqm[q(t)]+=1"
             "; mord_post[val[kk]]+=int(invertir_en is not None and t>=invertir_en)", etiqueta=f'{etiqueta}: bocado')

    # 8) eta -> _eta (las CUATRO del automodelo; k_auto queda apagado en organismo_v14t_on.py, pero la perilla existe)
    for viejo, nuevo, et in (
            ("if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())", "if dlt>0: _trunca=bool(((Wp[_ix]+_eta*dlt)>3.0).any())", 'trunca+'),
            ("else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())", "else:     _trunca=bool(((Wn[_ix]+_eta*aversion*(-dlt))>3.0).any())", 'trunca-'),
            ("if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)", "if dlt>0: Wp=np.clip(Wp+_eta*dlt*kc,0,3.)", 'Wp'),
            ("else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)", "else:     Wn=np.clip(Wn+_eta*aversion*(-dlt)*kc,0,3.)", 'Wn')):
        s = sust(s, viejo, nuevo, etiqueta=f'{etiqueta}: {et}')

    # 9) recuperacion (t_ext_B, mismo criterio del bloque 6) y muertes tras la inversion
    ancla_r = "        _prev_on=pos if pos in objs else -1"
    linea_r = [l for l in s.splitlines() if l.startswith(ancla_r)]
    if len(linea_r) != 1:
        raise SystemExit(f"ANCLA {etiqueta}: _prev_on: {len(linea_r)} lineas, se esperaba 1. Abortado.")
    s = sust(s, linea_r[0],
             f"        if invertir_en is not None and t>=invertir_en and t_ext_B is None and valor({pat}['B'])>=0: t_ext_B=t   # v13p: M1 del bloque 6 (no consume RNG)"
             + NL + linea_r[0], etiqueta=f'{etiqueta}: t_ext_B')
    ancla_d = "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))"
    s = sust(s, ancla_d, "        if E<=0:" + NL + "            deaths+=1; E=.6; pos=int(rng.integers(L))" + NL +
             "            if invertir_en is not None and t>=invertir_en: deaths_post+=1   # v13p", etiqueta=f'{etiqueta}: deaths_post')

    # 10) salidas: las del automodelo + las nuevas de dE
    ancla_sal = "Wns=[round(float(x),3) for x in Wns]"
    salida = NL.join(l.replace('{pat}', pat) for l in CS.SALIDA + CP.SALIDA_EXTRA)
    s = sust(s, ancla_sal, ancla_sal + "," + NL + salida.rstrip().rstrip(','), etiqueta=f'{etiqueta}: salida')

    return s


if __name__ == '__main__':
    salidas = []

    # ==== 1) organismo_v14t: organismo_v14c + la tercera perilla (automodelo entrelazado apagado + dE-TEST apagado) ====
    s = origen(os.path.join(AQUI, 'organismo_v14c.py'), SHA_V14C)
    s = pon_dE(s, FIRMA_V14C_OFF, 'PAT', 'v14t')
    cab = ('"""organismo_v14t = organismo_v14c.py (649851c0f10c3cd6: hija dispersa + puerta por codigo, ya apagadas)\n'
           '+ LA TERCERA PERILLA: "la sorpresa del mundo en la boca" (predictor de dE del bloque 6, k_testE; el punto\n'
           'de organismo_v13E_k5.py -- eta_pred=0.03, ema_pred=0.05, k_testE=5.0 cuando esta ON). Trae ADEMAS,\n'
           'apagado y DECLARADO (entrelazado en construye_probar.py, ver construye_v14t.py), el automodelo SELF/\n'
           'MUNDO/H_SHUF de construye_selfmodel.py (perillas eta_b,k_auto,ema_auto,k_test,test_fijo,buf_auto,clip_b,\n'
           'eta_e,h_pred,buf_e) y las de MOMENTO/ENMIENDA2 (n_traza,traza_ext,desfase,k_testM,resta_cota,resta_lenta,\n'
           'ema_lento): NINGUNA de estas se enciende jamas en organismo_v14t_on.py.\n'
           'Generado por construye_v14t.py. NO editar a mano.\n'
           'Con mask_rel=0, puerta_pat=0 y eta_pred=ema_pred=k_testE=0 es organismo_v13 EXACTO (arnes: identidad_v14t.py)."""\n')
    d = os.path.join(AQUI, 'organismo_v14t.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ==== 2) organismo_v14t_on: la misma, las TRES perillas fijas ON ====
    s2 = origen(d, h16(d))
    s2 = sust(s2, "mask_rel=0,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=0,pat_shuf=0,pat_min=0",
              "mask_rel=2,del_s=0.25,del_c=0.25,ema_c=0.05,puerta_pat=5,pat_shuf=0,pat_min=1",
              etiqueta='v14t_on: perillas 1+2 (hija dispersa + puerta por codigo, el punto de organismo_v14c_on)')
    s2 = sust(s2, "eta_pred=0.0,clip_e=3.0,ema_pred=0.0,k_testE=0.0,",
              "eta_pred=0.03,clip_e=3.0,ema_pred=0.05,k_testE=5.0,",
              etiqueta='v14t_on: perilla 3 (dE-TEST dosis 5, el punto de organismo_v13E_k5)')
    d2 = os.path.join(AQUI, 'organismo_v14t_on.py')
    open(d2, 'w', encoding='utf-8', newline='\n').write(
        '"""organismo_v14t_on = organismo_v14t.py con las TRES perillas fijas ON por defecto:\n'
        'mask_rel=2 (hija dispersa; el punto de organismo_v13Don / organismo_v14c_on), puerta_pat=5,pat_min=1\n'
        '(puerta por codigo PATC; el punto de organismo_v13Bn5c / organismo_v14c_on) y eta_pred=0.03,ema_pred=0.05,\n'
        'k_testE=5.0 (dE-TEST dosis 5; el punto de organismo_v13E_k5.py). El resto de perillas (automodelo SELF,\n'
        'MOMENTO, ENMIENDA2) se queda APAGADO -- nunca se enciende.\n'
        'Generado por construye_v14t.py. NO editar."""\n' + s2)
    salidas.append(d2)

    # ==== 3) organismo_v14gt: el mundo de regla (lo que usa bateria_generaliza_v14t) ====
    s = origen(os.path.join(AQUI, 'organismo_v14gc.py'), SHA_V14GC)
    s = pon_dE(s, FIRMA_V14GC_OFF, 'P_', 'v14gt')
    cab = ('"""organismo_v14gt = organismo_v14gc.py (dcca1ab79d86289b) + LA TERCERA PERILLA (dE-TEST, ver\n'
           'organismo_v14t.py). Es el instrumento del MUNDO DE REGLA que usa bateria_generaliza_v14t.py.\n'
           'Generado por construye_v14t.py. NO editar.\n'
           'Con mask_rel=0, puerta_pat=0 y eta_pred=ema_pred=k_testE=0 es organismo_v13g EXACTO."""\n')
    d = os.path.join(AQUI, 'organismo_v14gt.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ==== 4) bateria_v14t: la bateria del tronco (CONGELADA: solo se LEE) apuntando a organismo_v14t_on ====
    #      ERR-30 (igual que bateria_v13E.py): el criterio 5 (reduccion a v11/v10 con eta_s=0,puerta=None) NO
    #      alcanza para reducir a v13/v11 porque k_testE actua en la BOCA sin pasar por eta_s/puerta -- se apagan
    #      TAMBIEN k_testE y eta_pred, explicitos, en las DOS llamadas de reduccion (v11 y v10). mask_rel/puerta_pat
    #      NO se apagan explicitamente: mismo argumento que construye_v14c.py para su propio criterio 5 --
    #      puerta_pat queda ESTRUCTURALMENTE sin efecto con puerta=None (el ternario de pon_puerta() mira
    #      "puerta is None" ANTES de llamar a _fam()), y mask_rel=2 ya se demostro EMPIRICAMENTE inerte en este
    #      mundo (bateria_v14c.py corrio su propio criterio 5 con mask_rel=2 activo y el examen 8/8 completo
    #      registrado en datos/examen_v14c_* solo pudo producirse si paso). Sigue siendo una PREDICCION para el
    #      trio (nunca se probaron los tres mecanismos juntos en el criterio 5): se preregistra como control que
    #      puede fallar en PREREGISTRO_composicion_tres.md -- si falla, bateria_v14t.py aborta antes de la etapa 2.
    s = origen(os.path.join(RAIZ, 'organismo', 'bateria_v13.py'), SHA_BATERIA_V13)
    s = sust(s, "AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(AQUI)\n"
                "sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]\n",
             "_D14T = os.path.dirname(os.path.abspath(__file__))   # esta copia vive fuera de organismo/\n"
             "AQUI = os.path.join(os.path.dirname(os.path.dirname(_D14T)), 'organismo')\n"
             "RAIZ = os.path.dirname(AQUI)\n"
             "sys.path[:0] = [_D14T, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]\n", etiqueta='bateria_v14t: rutas')
    s = sust(s, "    import organismo_v13 as v13\n",
             "    import organismo_v14t_on as v13   # composicion de TRES: hija dispersa + puerta por codigo + dE-TEST dosis 5, las TRES ON\n",
             n=2, etiqueta='bateria_v14t: import')
    s = sust(s, "a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, **ESC_ID[esc])",
             "a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, k_testE=0.0, eta_pred=0.0, **ESC_ID[esc])   # ERR-30: v3'' (organos en la boca)",
             etiqueta='bateria_v14t: ERR-30 criterio 5 vs v11')
    s = sust(s, "a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, **ESC_ID[esc])",
             "a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, k_testE=0.0, eta_pred=0.0, **ESC_ID[esc])   # ERR-30: v3'' (organos en la boca)",
             etiqueta='bateria_v14t: ERR-30 criterio 5 vs v10')
    s = sust(s, "    for c, nombre in (('v11', 'v13(eta_s=0, puerta=None) == v11'), ('v10', 'v13(eta_s=0, puerta=None, div_signo=False) == v10')):\n",
             "    for c, nombre in (('v11', \"v14t(eta_s=0,puerta=None,k_testE=0,eta_pred=0) == v11  [v3'' ERR-30]\"), "
             "('v10', \"v14t(eta_s=0,puerta=None,div_signo=False,k_testE=0,eta_pred=0) == v10  [v3'' ERR-30]\")):\n",
             etiqueta='bateria_v14t: ERR-30 etiquetas de log')
    s = s.replace("h16(os.path.join(AQUI, 'organismo_v13.py'))", "h16(os.path.join(_D14T, 'organismo_v14t_on.py'))")
    s = s.replace("f'examen_v13_{stamp}", "f'examen_v14t_{stamp}")
    cab = ('"""bateria_v14t = organismo/bateria_v13.py (1a027bcb37eb536e, CONGELADO: solo se leyo) apuntando a\n'
           'organismo_v14t_on (composicion de TRES: hija dispersa + puerta por codigo + dE-TEST dosis 5, las TRES ON)\n'
           'en vez de organismo_v13. Las SEIS etapas, los CRIT importados y los umbrales del criterio v3\' quedan\n'
           'INTACTOS. Salida en datos/examen_v14t_<fecha>.\n'
           'ERR-30: el CRITERIO 5 esta ADAPTADO (v3\'\' para organos en la boca, precedente ERR-21/bateria_v13E.py):\n'
           'la reduccion a v11/v10 apaga TAMBIEN k_testE y eta_pred. mask_rel/puerta_pat NO se apagan (ver nota en\n'
           'construye_v14t.py: estructural + empiricamente inertes, PREDICCION declarada como control que puede\n'
           'fallar). Ver PREREGISTRO_composicion_tres.md.\n'
           'Generado por construye_v14t.py. NO editar. La bateria original NO se modifico."""\n')
    d = os.path.join(AQUI, 'bateria_v14t.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    # ==== 5) bateria_generaliza_v14t: con las dos entradas nuevas de INSTRUMENTOS, ambas sobre organismo_v14gt ====
    s = origen(os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py'), SHA_BATERIA_GENERALIZA)
    s = sust(s, "AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(AQUI)\n",
             "AQUI = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'organismo')   # esta copia vive fuera de organismo/\n"
             "RAIZ = os.path.dirname(AQUI)\n", etiqueta='bateria_generaliza_v14t: AQUI/RAIZ')
    s = sust(s, "REGLAS = ['px0', 'azar']\n",
             "REGLAS = ['px0', 'azar']\n_D14T = os.path.join(RAIZ, 'experimentos', 'nivel10_composicion_v14')\n",
             etiqueta='bateria_generaliza_v14t: _D14T')
    s = sust(s, "    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto\n",
             "    'organismo_v13_rapido': ('organismo_v13q_rapido', dict(eta_s=0.015, puerta=3)),   # gemelo compilado del mundo de regla (identidad 81/81+243/243); mismo punto\n"
             "    'organismo_v14t': ('organismo_v14gt', dict(eta_s=0.015, puerta=3)),   # composicion de TRES: las TRES perillas APAGADAS -> debe dar lo mismo que organismo_v13\n"
             "    'organismo_v14t_on': ('organismo_v14gt', dict(eta_s=0.015, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1, eta_pred=0.03, ema_pred=0.05, k_testE=5.0)),   # composicion de TRES: las TRES ON\n",
             etiqueta='bateria_generaliza_v14t: INSTRUMENTOS')
    s = sust(s, "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))\n",
             "sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'))\n"
             "sys.path.insert(0, _D14T)   # composicion de TRES: organismo_v14gt\n", etiqueta='bateria_generaliza_v14t: sys.path')
    s = sust(s, "    _dir = {'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),\n",
             "    _dir = {'organismo_v11g': GEN, 'organismo_v13g': os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),\n"
             "            'organismo_v14gt': _D14T,\n", etiqueta='bateria_generaliza_v14t: _dir')
    s = s.replace("h16(os.path.join(AQUI, (modulo if modulo != 'organismo_v13_rapido' else 'organismo_v13') + '.py'))",
                  "h16(os.path.join(AQUI, 'organismo_v13.py') if modulo == 'organismo_v13_rapido' else (os.path.join(AQUI, modulo + '.py') if os.path.exists(os.path.join(AQUI, modulo + '.py')) else os.path.join(_D14T, modulo.split('_on')[0] + '.py')))")
    s = s.replace("sha_organismo=h16(os.path.join(AQUI, modulo + '.py')),",
                  "sha_organismo=(h16(os.path.join(AQUI, modulo + '.py')) if os.path.exists(os.path.join(AQUI, modulo + '.py')) else h16(os.path.join(_D14T, modulo.split('_on')[0] + '.py'))),")
    cab = ('"""bateria_generaliza_v14t = organismo/bateria_generaliza.py (46772f5a582872c8) con DOS entradas mas en\n'
           'INSTRUMENTOS (organismo_v14t y organismo_v14t_on, ambas sobre organismo_v14gt) y las rutas corregidas por\n'
           'vivir fuera de organismo/. Los UMBRALES y los criterios G1/G2/K NO se tocan -- este es T2 del\n'
           'PREREGISTRO_composicion_tres.md (con organismo_v14t_on).\n'
           'Generado por construye_v14t.py. NO editar. La bateria original NO se modifico."""\n')
    d = os.path.join(AQUI, 'bateria_generaliza_v14t.py'); open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    salidas.append(d)

    print(f"=== construye_v14t.py: {len(salidas)} archivos ===")
    for d in salidas:
        print(f"  {os.path.relpath(d, RAIZ):55s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
