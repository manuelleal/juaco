"""Construye experimentos/nivel11_mundo_vivo/organismo_vivo_rep.py POR ANCLAS desde el instrumento del mundo vivo
experimentos/nivel11_mundo_vivo/organismo_vivo.py (20c0961c79de8825; construido a su vez por anclas desde el TRONCO
CONGELADO organismo/organismo_v14.py = v14.1 feefc88b1fd8d434). Aqui organismo_vivo.py SOLO SE LEE: no se edita
ningun archivo existente (regla 1 de EQUIPO.md; manifiesto.py).

PROPOSITO Y REPRODUCCION, peldano minimo (linea F de registro/PLAN.md; PREREGISTRO_reproduccion.md):

  (a) REPRODUCCION COMO MEDIDA (rep_mide): una VENTANA DE VIABILIDAD son rep_X pasos SEGUIDOS con E >= rep_umbral y
      Ag >= rep_umbral (las DOS necesidades en o sobre el punto de saciedad, donde sus deficits son 0). Cada ventana
      completa cuenta UN DESCENDIENTE VIABLE (`descendientes`); ademas `pasos_viables` (pasos saciado en las dos) y la
      tabla de decisiones y mordidas de la boca ESTANDO SACIADO (`sac_dec`, `sac_mord`, por estimulo). Con rep_coste=0 es
      SOLO LECTURA: no toca el rng ni la conducta -> las claves viejas salen bit a bit (arnes, caso C).
      No se hereda nada: el descendiente se CUENTA, no se instancia (un cuerpo, memoria que sobrevive a la muerte).
  (b) PROPOSITO COMO TERCERA NECESIDAD (rep_nec, n_nec=3): la fila 2 de valor es la necesidad de REPRODUCIRSE. Su
      variable de cuerpo es el CUELLO DE BOTELLA S2 = min(E, Ag): la componente del bocado para esa fila es el cambio de
      ese minimo (dS2 = min(E',Ag') - min(E,Ag), calculado del propio cuerpo antes y despues del bocado: local, sin
      mirar al futuro), y su recompensa sigue el mismo mapa que las otras (dS>0 -> +1, dS<0 -> -3, 0 -> 0). Aprende como
      cualquier fila (un encuentro ensena a todas). Su deficit es clip(1 - min(E,Ag)) = max(hambre, sed): nunca gana a
      las primarias; MANDA en la boca SOLO cuando las dos primarias callan (E >= 1 y Ag >= 1), como desempate de
      prioridad local. Por que no 1-G (la reserva) como deficit: con deficit alto la boca de v14 muerde cualquier cosa
      (enmienda 1 del mundo vivo: "el impulso tapa el valor cero"); el proposito debe entrar por el VALOR, no por el impulso.
      Con rep_coste>0, cada ventana completa (= descendiente) CONSUME rep_coste de E y de Ag (el mecanismo paga).
  (c) CUELLO (rep_cuello=1, control): saciado, la boca lee la fila del recurso MAS ESCASO (E<=Ag -> hambre, si no sed).
      Sin fila nueva ni aprendizaje nuevo. El humo (18-sep 09:00) mostro su defecto: al leer UNA fila primaria el dano
      del otro recurso vale 0 (la fila de la sed no ve el veneno) y muerde veneno saciado el 27 %. Se conserva como estaba
      preregistrado.
      CUELLO_MIN (rep_cuello=2, control que puede ganar; ERR-38 provisional, anadido tras el humo y ANTES del bloque):
      saciado, la boca lee el MINIMO de las dos filas primarias (la lectura pesimista: rechaza lo que dana a cualquiera
      de las dos). Sin fila nueva, sin aprendizaje nuevo (con la puerta encendida `_wt` solo entra en la boca; por eso
      exige puerta). Si rinde lo mismo que (b), la tercera fila sobra y el proposito saciado es "leer las dos y quedarse
      con la peor".

ANCLA DE IDENTIDAD: con reproduccion=0 (perilla MAESTRA, por defecto) TODO lo anterior es inerte y organismo_vivo_rep es
organismo_vivo BIT A BIT, mismo consumo del rng (ninguna linea nueva llama al rng: lo comprueba este constructor) y
MISMAS claves de salida (las claves nuevas se agregan solo con reproduccion=1). Arnes: identidad_vivo_rep.py.

PERILLAS NUEVAS (todas detras de `reproduccion`):
  reproduccion=0  perilla maestra. 0 -> organismo_vivo exacto (rep_* se ignoran)
  rep_mide=1      cuenta ventanas de viabilidad, pasos viables y la tabla SACIADO (solo lectura si rep_coste=0)
  rep_X=500       longitud de la ventana en pasos = (1.5 - 1.0) / costo: lo que tarda un cuerpo lleno en volver al punto
                  de saciedad; una ventana exige volver a comer Y beber estando ya saciado (provision sostenida)
  rep_umbral=1.0  el punto de saciedad del tronco (deficit = clip(1 - S) = 0 en o sobre 1.0)
  rep_coste=0.0   lo que paga el padre en E y en Ag por cada descendiente (0.4 = un bocado de veneno + uno de sal)
  rep_nec=0       la tercera necesidad (exige n_nec=3 y vivo=1)
  rep_cuello=0    controles: 1 = CUELLO (fila del recurso mas escaso), 2 = CUELLO_MIN (minimo de las dos filas; exige puerta);
                  ambos exigen n_nec=2 y rep_nec=0

Uso:  python experimentos/nivel11_mundo_vivo/construye_vivo_rep.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28), aunque aqui solo se lea texto

SHA_VIVO = '20c0961c79de8825'   # experimentos/nivel11_mundo_vivo/organismo_vivo.py (construido desde v14.1 feefc88b1fd8d434)
SHA_V14 = 'feefc88b1fd8d434'    # organismo/organismo_v14.py: se verifica tambien (la cadena de origen entera)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


NUEVO = []   # todo texto insertado, para comprobar que ninguna linea nueva llama al rng


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    NUEVO.append(nuevo.replace(viejo, ''))
    return texto.replace(viejo, nuevo)


# ============================ ANCLAS (copiadas literalmente de organismo_vivo.py 20c0961c79de8825) ============================
A_FIRMA = "k_sorp=0.0,crit_exp=0.5):"
A_GUARDIA = ("    if n_nec>1 and not vivo: raise SystemExit('MUNDO VIVO: n_nec>1 exige vivo=1 "
             "(la mordida debe tener consecuencia vectorial)')\n")
A_IDX = "    _IDX={_k2:_i2 for _i2,_k2 in enumerate('ABCD')}\n"
A_HAMBRE = "        hambre=np.clip(1-E,0,1)\n        if n_nec>1:"
A_NA = ("            _dfa=np.clip(1-Ag,0,1); _na=1 if _dfa>hambre else 0\n"
        "            if _na: hambre=_dfa\n")
A_VIS = "            vis[kk][q(t)]+=1\n"
A_DS = "                    _dS=_EF[val[kk]]; _Rv=[(1.0 if _x>0 else (-3.0 if _x<0 else 0.0)) for _x in _dS]\n"
A_MORDQ = "                mord[kk][q(t)]+=1\n"
A_S0 = "                    _s0=_EF[val[kk]][_n]\n"
A_MUERTE = "            pos=int(rng.integers(L))\n"
A_WT = ("            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13: valor total (sin puerta: suma; "
        "con puerta: la rapida si le es familiar)\n")
A_EXT = ("               sorp_nec=[round(float(_x),4) for _x in _sbE]) if vivo else {})   # VIVO: claves nuevas SOLO si "
         "vivo=1 (con vivo=0 el dict es el de v14, clave por clave)\n")

CAB = '''"""organismo_vivo_rep = experimentos/nivel11_mundo_vivo/organismo_vivo.py (20c0961c79de8825, el mundo vivo; aqui solo se
LEYO; a su vez por anclas desde el TRONCO CONGELADO organismo/organismo_v14.py v14.1 feefc88b1fd8d434) + PROPOSITO Y
REPRODUCCION (peldano minimo, PREREGISTRO_reproduccion.md): (a) REPRODUCCION COMO MEDIDA: ventanas de viabilidad
(rep_X pasos seguidos con E y Ag >= rep_umbral) = descendientes viables, pasos viables y tabla de la boca SACIADO, todo
de solo lectura; (b) PROPOSITO como TERCERA NECESIDAD (fila 2 de valor: reproducirse; su cuerpo es el cuello de botella
min(E,Ag); manda solo cuando las dos primarias callan; con rep_coste paga E y Ag por cada descendiente);
(c) CUELLO, control: saciado, lee la fila del recurso mas escaso, sin fila nueva.
ANCLA DE IDENTIDAD: con reproduccion=0 (por defecto) es organismo_vivo BIT A BIT, mismo consumo del rng y mismas claves.
Arnes: identidad_vivo_rep.py.  Generado por construye_vivo_rep.py. NO editar a mano."""
'''


if __name__ == '__main__':
    origen(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14)   # la cadena de origen entera, solo lectura
    s = origen(os.path.join(AQUI, 'organismo_vivo.py'), SHA_VIVO)

    # ---- 1) firma: perillas detras de la maestra ----
    s = sust(s, A_FIRMA, "k_sorp=0.0,crit_exp=0.5,reproduccion=0,rep_mide=1,rep_X=500,rep_umbral=1.0,rep_coste=0.0,"
             "rep_nec=0,rep_cuello=0):", etiqueta='firma: perillas de reproduccion')

    # ---- 2) guardias: la maestra apaga todo; la tercera necesidad exige n_nec=3; el control CUELLO exige n_nec=2 ----
    s = sust(s, A_GUARDIA, A_GUARDIA +
             "    if not reproduccion: rep_mide=0; rep_nec=0; rep_cuello=0; rep_coste=0.0   # REP: perilla MAESTRA apagada -> todo lo de abajo es inerte: organismo_vivo EXACTO\n"
             "    if rep_nec and n_nec!=3: raise SystemExit('REP: rep_nec=1 exige n_nec=3 (la tercera fila de valor ES la necesidad de reproducirse)')\n"
             "    if n_nec==3 and not rep_nec: raise SystemExit('REP: n_nec=3 exige rep_nec=1 (sin la tercera necesidad no hay tercera componente de dS)')\n"
             "    if n_nec>3: raise SystemExit('REP: n_nec maximo 3')\n"
             "    if rep_cuello not in (0,1,2): raise SystemExit('REP: rep_cuello es 0, 1 (CUELLO) o 2 (CUELLO_MIN)')\n"
             "    if rep_cuello and (n_nec!=2 or rep_nec): raise SystemExit('REP: rep_cuello (control) exige n_nec=2 y rep_nec=0')\n"
             "    if rep_cuello==2 and puerta is None: raise SystemExit('REP: rep_cuello=2 exige puerta (con puerta=None el valor de la boca entra en el aprendizaje)')\n",
             etiqueta='guardias de reproduccion')

    # ---- 3) estado: ventana, descendientes, pasos viables, tabla SACIADO ----
    s = sust(s, A_IDX, A_IDX +
             "    _gv=0; _desc=0; _pv=0; _tdesc=[]; _dq=[0]*4; _bsac={k:0 for k in PAT}; _dsac={k:0 for k in PAT}; _sac=False; _cue2=False   # REP: ventana de viabilidad, descendientes viables, pasos viables, tabla de decisiones/mordidas SACIADO (solo lectura si rep_coste=0); _cue2 = CUELLO_MIN activo\n",
             etiqueta='estado de reproduccion')

    # ---- 4) paso: saciado en las dos = los dos deficits en 0 ----
    s = sust(s, A_HAMBRE,
             "        hambre=np.clip(1-E,0,1)\n"
             "        _sac=bool(rep_mide) and E>=rep_umbral and Ag>=rep_umbral   # REP: SACIADO en las dos necesidades (deficits 0). Solo lectura\n"
             "        if n_nec>1:", etiqueta='saciado')

    # ---- 5) necesidad activa: la tercera manda solo cuando las primarias callan; CUELLO lee la fila del recurso mas escaso ----
    s = sust(s, A_NA, A_NA +
             "            if rep_nec and hambre==0 and _dfa==0: _na=2   # REP: la TERCERA necesidad (reproducirse) manda SOLO cuando las dos primarias callan; su deficit clip(1-min(E,Ag)) es 0 aqui. Prioridad local, sin planificador\n"
             "            if rep_cuello==1 and hambre==0 and _dfa==0: _na=0 if E<=Ag else 1   # CUELLO (control): saciado, la boca lee la fila del recurso MAS ESCASO; sin fila nueva\n"
             "            _cue2=bool(rep_cuello==2 and hambre==0 and _dfa==0)   # CUELLO_MIN (control que puede ganar): saciado, la boca leera el MINIMO de las dos filas (ver la boca)\n",
             etiqueta='prioridad de la tercera necesidad / cuello')

    # ---- 5b) CUELLO_MIN: saciado, la boca lee el minimo de las dos filas primarias (con puerta, _wt solo entra en la boca) ----
    s = sust(s, A_WT, A_WT +
             "            if _cue2: _wt=min(_wt,_vnec(1-_na,PAT[kk],kc))   # CUELLO_MIN (control que puede ganar; ERR-38 provisional): saciado, la lectura PESIMISTA de las dos filas; sin fila nueva, sin aprendizaje nuevo\n",
             etiqueta='cuello_min en la boca')

    # ---- 6) decisiones y mordidas estando saciado (solo lectura) ----
    s = sust(s, A_VIS, A_VIS + "            if _sac: _dsac[kk]+=1   # REP: decision de la boca estando SACIADO (solo lectura)\n",
             etiqueta='decisiones saciado')
    s = sust(s, A_MORDQ, A_MORDQ + "                if _sac: _bsac[kk]+=1   # REP: mordida estando SACIADO (solo lectura)\n",
             etiqueta='mordidas saciado')

    # ---- 7) la tercera componente del bocado: el cambio del CUELLO DE BOTELLA min(E,Ag), leido del propio cuerpo ----
    s = sust(s, A_DS, A_DS +
             "                    if rep_nec:   # REP: la tercera necesidad lee el CUELLO DE BOTELLA del cuerpo, min(E,Ag): su componente es el cambio de ese minimo con ESTE bocado (local, sin mirar al futuro)\n"
             "                        _m0=min(E,Ag); _m1=min(min(E+_dS[0],1.5),min(Ag+_dS[1],1.5)); _dS=(_dS[0],_dS[1],_m1-_m0); _Rv.append(1.0 if _dS[2]>0 else (-3.0 if _dS[2]<0 else 0.0))\n",
             etiqueta='componente del cuello de botella')

    # ---- 8) exposiciones hasta criterio de la tercera fila: el signo que la fisica obliga es el de dE+dAg ----
    s = sust(s, A_S0, "                    _s0=(_EF[val[kk]][_n] if _n<2 else _EF[val[kk]][0]+_EF[val[kk]][1])   # REP: para la tercera fila, el signo que la fisica obliga es el de dE+dAg (el minimo solo puede moverse en esa direccion)\n",
             etiqueta='signo de la tercera fila')

    # ---- 9) la ventana de viabilidad y el descendiente (tras el drenaje y las muertes); el coste del mecanismo ----
    s = sust(s, A_MUERTE, A_MUERTE +
             "        if rep_mide:   # REP: VENTANA DE VIABILIDAD = rep_X pasos SEGUIDOS con E y Ag >= rep_umbral -> un DESCENDIENTE VIABLE (la medida). Con rep_coste>0 reproducirse CONSUME los dos recursos (el mecanismo)\n"
             "            if E>=rep_umbral and Ag>=rep_umbral: _gv+=1; _pv+=1\n"
             "            else: _gv=0\n"
             "            if _gv>=rep_X:\n"
             "                _desc+=1; _dq[q(t)]+=1; _gv=0\n"
             "                if len(_tdesc)<200: _tdesc.append(t)\n"
             "                if rep_coste: E-=rep_coste; Ag-=rep_coste   # REP: el padre paga en los dos ejes; por construccion no mata (umbral - coste > 0)\n",
             etiqueta='ventana de viabilidad')

    # ---- 10) claves nuevas SOLO con la perilla maestra encendida ----
    s = sust(s, A_EXT, A_EXT +
             "    if reproduccion: _ext.update(descendientes=_desc,pasos_viables=_pv,desc_q=list(_dq),t_desc=list(_tdesc),sac_mord=dict(_bsac),sac_dec=dict(_dsac),\n"
             "                                 rep=dict(mide=int(rep_mide),X=rep_X,umbral=rep_umbral,coste=rep_coste,nec=int(rep_nec),cuello=int(rep_cuello)))   # REP: claves nuevas SOLO con reproduccion=1\n",
             etiqueta='claves de reproduccion')

    # ---- comprobacion: ninguna linea nueva consume el rng del organismo (ni el propio del control barajado) ----
    malas = [x for x in NUEVO if 'rng' in x]
    if malas:
        raise SystemExit("Una insercion nombra al rng: " + repr(malas[:2]))

    d = os.path.join(AQUI, 'organismo_vivo_rep.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(CAB + s)
    print(f"  escrito {d}")
    print(f"  sha organismo_v14.py (origen del origen, solo lectura) {SHA_V14}")
    print(f"  sha organismo_vivo.py (origen, solo lectura)           {SHA_VIVO}")
    print(f"  sha organismo_vivo_rep.py                               {h16(d)}")
    print(f"  sha construye_vivo_rep.py                               {h16(os.path.abspath(__file__))}")
    print(f"  inserciones: {len(NUEVO)}; ninguna nombra al rng.")
    print("  siguiente: python experimentos/nivel11_mundo_vivo/identidad_vivo_rep.py")
