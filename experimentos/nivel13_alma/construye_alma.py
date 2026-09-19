"""Construye experimentos/nivel13_alma/organismo_alma.py POR ANCLAS desde
experimentos/nivel11_mundo_vivo/organismo_vivo_h1.py (9e99ff87b5e2db1e, el instrumento de H-1 "QUE LA MUERTE
MATE", que aqui SOLO SE LEE; cadena: organismo_vivo_rep2 96feb4918dc5d694 <- organismo_vivo_rep aa823d56c2d4213c
<- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo/organismo_v14.py v14.1 feefc88b1fd8d434).
No se edita ningun archivo existente (regla 1 de EQUIPO.md; manifiesto.py). Archivos nuevos SOLO en nivel13_alma/.

MISION: llegar a la AGI por este camino — un organismo minimo con reglas locales que aprende, sobrevive, se
comunica y se reproduce; con evidencia preregistrada. Hoy: un ALMA externa (evolucion guiada, como v11/JUACO-EVO)
que parcha al cuerpo cada vez que muere, sin confundir el buscador con el resultado.

IDEA DEL DIRECTOR (textual): "una celula en un mundo, Haiku de alma del experimento; comienza a interactuar; si
muere, Haiku la revive y le pone una curita, un puente para que no muera por lo mismo; despues se reproduce, tiene
hijos, y un nodo central de conocimiento como en Avatar: las celulas que quieren vivir se conectan y reciben los
datos, las que no, que se mueran solas; cada vez que muera, parcharla, hasta lograr que evolucione".

ANTECEDENTE MEDIDO (no se re-deriva aqui):
  · H-1 (REGISTRO, 18 sep 19:24 y replica): con muerte real R0 cae de 0.87-0.98 a 0.14-0.17 en TODOS los modos de
    herencia; vida mediana ~100-130 pasos; heredar valores paga 10-20 %, no el 500 % que falta. ERR-62.
  · BLOQUE 4b (REGISTRO, 18 sep 18:22 y bloque 5): el mensaje (patron de referencia + recompensa) CAMBIA LA
    CONDUCTA DEL RECEPTOR SIN EXPERIENCIA PROPIA (CANAL- 19/20, 17/18, 19/19 contra CORTADO- 3/20, 0/18, 2/19).
  · NOTA_entrelazamiento_20260918.md (1b02767f7cba7d7c): "la informacion sobrevive al cuerpo solo si vive en otro
    sitio y para pasar de un cuerpo a otro necesita un canal" -> HERENCIA POR MENSAJE. El NODO CENTRAL de este
    bloque es exactamente ese "otro sitio" hecho poblacional.

PERILLAS NUEVAS (todas detras de la maestra `alma`; con alma=None es organismo_vivo_h1 BIT A BIT)
  alma=None        None | invocable. Se llama UNA vez por muerte con un dict-resumen y devuelve
                   {'curita': 'a'|'b'|'c'|'d'|'e'|'f', 'motivo': str}. MENU CERRADO (MENU_curitas.md): fuera de
                   esas seis letras el instrumento ABORTA. Exige muerte_real=1 y alma_muertes>=1.
  alma_muertes=0   la corrida TERMINA despues de esta muerte numero N (la serie de cuerpos ES la medida)
  nodo=1           1 = el NODO CENTRAL existe y se llena; 0 = no hay nodo (control `alma_ninguna`)
  conectado=0      el cuerpo NACE leyendo el nodo (la curita (a) lo pone a 1 para todos los cuerpos siguientes)
  nodo_k=20        cuantas mordidas con consecuencia del que muere se escriben en el nodo
  nodo_lee=50      cuantos mensajes (los mas recientes) lee al nacer un cuerpo conectado
  miedo_n=5        copias del mensaje que escribe la curita (b)
  miedo_R=-3.0     la recompensa de ese mensaje (la R cruda de veneno/sal en este mundo: R_VAL['veneno'])
  d_dote=0.1       paso de la curita (c)
  d_umbral=0.1     paso de la curita (d)

EL NODO CENTRAL Y LA EXPOSICION SIN CONSECUENCIA (decision de diseno, declarada, con su limitacion)
  El canal del BLOQUE 4/4b escribe el mensaje en la TABLA DE PARES (`memoria_pares`, organo de v15f). Ese organo
  NO EXISTE en la cadena del mundo vivo (organismo_vivo <- v14.1): h1 no tiene tabla de pares. Portarlo aqui seria
  un organo nuevo, no un canal. Lo que SI se traduce literalmente es el CONTRATO de b4: "el receptor RECIBE el
  mensaje como una EXPOSICION SIN CONSECUENCIA con la valencia recibida; no toca energia, ni objetos, ni `ncod`,
  ni la via rapida, ni la plasticidad". Aqui esa exposicion se ejecuta con el BLOQUE DE LA VIA LENTA EXTRAIDO
  LITERALMENTE de la mordida de organismo_vivo_h1 (drenaje `lam` de la parte comun + error propio R - _ws +
  clip a [0, clip_s]), con el patron y la R cruda del mensaje, sobre la FILA de la necesidad que el emisor tenia
  activa cuando mordio. NO consume rng, no toca E/Ag, objs, ncod, la via rapida ni la plasticidad.
  LIMITACION QUE SE DECLARA: esto NO es el canal de b4b bit a bit (otro organo, otra cadena); es el mismo
  contrato en el lenguaje de esta cadena. Cualquier comparacion con los numeros de b4b es ilegitima.

ANCLA DE IDENTIDAD: con alma=None (por defecto) es organismo_vivo_h1 BIT A BIT, clave por clave y con el mismo
consumo del rng DEL MUNDO, en TODOS los brazos de H-1 (RENACE, NADA, M1, M1+PARES, BARAJA). Ninguna insercion
consume el rng (lo comprueba este constructor con una expresion regular). Arnes: identidad_alma.py.

Uso:  python experimentos/nivel13_alma/construye_alma.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo', 'organismo_vivo_h1.py')
DESTINO = os.path.join(AQUI, 'organismo_alma.py')
SHA_H1 = '9e99ff87b5e2db1e'    # organismo_vivo_h1.py (H-1, la muerte que mata)
SHA_REP2 = '96feb4918dc5d694'  # organismo_vivo_rep2.py
SHA_V14 = 'feefc88b1fd8d434'   # organismo/organismo_v14.py (v14.1, TRONCO CONGELADO)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


NUEVO = []


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    NUEVO.append(nuevo.replace(viejo, ''))
    return texto.replace(viejo, nuevo)


# ==================== ANCLAS (copiadas literalmente de organismo_vivo_h1.py 9e99ff87b5e2db1e) ====================
A_FIRMA = "muerte_real=0,hereda='nada',dote=0.6,cola_max=200,h1=0):"

A_MAESTRA = "    if not reproduccion: muerte_real=0; h1=0; hereda='nada'   # H1: detras de la maestra (inerte: organismo_vivo EXACTO)\n"

A_RB = ("    _rb=np.random.default_rng(800000+1000000*seed) if (muerte_real and hereda=='baraja') else None"
        "   # H1: rng PROPIO del barajado (ERR-60); no toca el rng del mundo ni el del cuerpo\n")

A_EXPO = "                _enc[kk]+=1; _exor[_na][_IDX[kk]]+=1\n"

A_MORD = "                mord[kk][q(t)]+=1\n"

A_MUERE = "            deaths+=1; _mnec[0 if E<=0 else 1]+=1; E=.6\n"

A_BORRA = ("            if muerte_real:   # H1: LA MUERTE BORRA AL INDIVIDUO. Nace el siguiente de la cola; "
           "si no hay, el linaje SE EXTINGUIO y el mundo pone un FUNDADOR\n")

A_NACE = "                _nace(_nac,_m)\n"

A_REP2D = ("                if len(_vidas)<400: _vidas.append(t-_tmu)\n"
           "                _tmu=t\n")

A_EXT_H1 = ("                       h1=dict(cola_max=cola_max,sem_hijo='700000+1000000*seed+k',"
            "sem_baraja='800000+1000000*seed'))   # H1: claves nuevas SOLO con h1=1\n")

# ==================== INSERCIONES (ninguna consume el rng del mundo) ====================
N_FIRMA = ("muerte_real=0,hereda='nada',dote=0.6,cola_max=200,h1=0,"
           "alma=None,alma_muertes=0,nodo=1,conectado=0,nodo_k=20,nodo_lee=50,miedo_n=5,miedo_R=-3.0,"
           "d_dote=0.1,d_umbral=0.1):")

N_MAESTRA = A_MAESTRA + (
    "    if not muerte_real: alma=None; alma_muertes=0   # ALMA: detras de la muerte real (inerte: organismo_vivo_h1 EXACTO)\n"
    "    if alma is not None and not callable(alma): raise SystemExit('ALMA: alma es None o un invocable (resumen -> {curita, motivo})')\n"
    "    if alma is not None and not alma_muertes: raise SystemExit('ALMA: alma exige alma_muertes>=1 (la serie de cuerpos ES la medida)')\n"
    "    if alma is not None and not nodo and conectado: raise SystemExit('ALMA: conectado=1 exige nodo=1 (no hay a que conectarse)')\n")

N_RB = A_RB + (
    "    _nodo=[]; _cur=[]; _mordh=[]; _exph=[]; _con=bool(conectado); _nmu=0; _causa=None; _Tef=T; _inerte=0"
    "   # ALMA: el NODO CENTRAL (mensajes (patron, R cruda, necesidad)), las curitas elegidas, la historia del cuerpo EN CURSO,\n"
    "    #        si el linaje esta conectado, muertes atendidas por el alma, la necesidad que llego a cero, los pasos efectivos y las curitas (b) inertes.\n"
    "    #        SOLO LECTURA salvo el nodo y las tres perillas declaradas (dote, rep_umbral, hereda). Ninguna linea de aqui consume el rng.\n")

N_EXPO = A_EXPO + (
    "                if alma is not None: _exph.append([int(t),kk,int(_na),int(mordio)])"
    "   # ALMA: EXPOSICION del cuerpo en curso (t, estimulo, necesidad activa, mordio) -- solo lectura\n")

N_MORD = A_MORD + (
    "                if alma is not None: _mordh.append([int(t),kk,int(_na),float(R)])"
    "   # ALMA: MORDIDA CON CONSECUENCIA del cuerpo en curso (lo que este cuerpo aprendio) -- solo lectura\n")

N_MUERE = (
    "            if alma is not None: _causa=('energia' if E<=0 else 'agua')"
    "   # ALMA: la necesidad que llego a cero, ANTES de que el renacer la reponga (solo lectura)\n") + A_MUERE

N_BORRA = (
    "            if alma is not None:   # ALMA: (1) el NODO se llena con lo que el cuerpo que muere aprendio; (2) el alma elige UNA curita del MENU CERRADO\n"
    "                _nmu+=1\n"
    "                if nodo:\n"
    "                    for _t9,_k9,_n9,_R9 in _mordh[-nodo_k:]: _nodo.append([[float(_z9) for _z9 in PAT[_k9]],float(_R9),int(_n9)])\n"
    "                _res=dict(cuerpo=_nmu,t=int(t),causa=_causa,edad=int(_vh[-1]),hijos=int(_dpv[-1]),fundador=int(_esfund),\n"
    "                          conectado=int(_con),nodo_n=len(_nodo),dote=round(float(dote),4),rep_umbral=round(float(rep_umbral),4),\n"
    "                          hereda=hereda,exposiciones=[list(_x) for _x in _exph[-20:]],mordidas=[list(_x) for _x in _mordh[-20:]],\n"
    "                          descendientes=int(_desc),muertes=int(deaths),fundadores=int(_fund),\n"
    "                          R0=round(_desc/max(deaths,1),4),menu=['a','b','c','d','e','f'])\n"
    "                _r9=alma(_res) or {}\n"
    "                _c9=_r9.get('curita','f')\n"
    "                if _c9 not in ('a','b','c','d','e','f'): raise SystemExit(f'ALMA: curita {_c9!r} fuera del MENU CERRADO (a,b,c,d,e,f)')\n"
    "                if _c9=='a': _con=True   # (a) CONECTAR AL NODO: los cuerpos siguientes nacen leyendo el nodo\n"
    "                elif _c9=='b':   # (b) SUBIR EL MIEDO al estimulo que precedio a la muerte, ESCRIBIENDOLO EN EL NODO\n"
    "                    _u9=(_mordh[-1] if _mordh else (_exph[-1] if _exph else None))\n"
    "                    if _u9 is not None and nodo:\n"
    "                        for _ in range(miedo_n): _nodo.append([[float(_z8) for _z8 in PAT[_u9[1]]],float(miedo_R),int(_u9[2])])\n"
    "                    else: _inerte+=1\n"
    "                elif _c9=='c': dote=round(min(dote+d_dote,rep_umbral-0.05),6)   # (c) DOTE MAYOR (perilla declarada del mundo; acotada por 0<dote<rep_umbral)\n"
    "                elif _c9=='d': rep_umbral=round(max(rep_umbral-d_umbral,dote+0.05),6)   # (d) BAJAR EL UMBRAL DE REPRODUCCION (perilla declarada)\n"
    "                elif _c9=='e': hereda='M1'   # (e) HEREDAR VALORES del padre (el VECTOR Wps/Wns; el brazo M1 de H-1)\n"
    "                _cur.append([_nmu,_c9,str(_r9.get('motivo',''))[:240],round(float(dote),4),round(float(rep_umbral),4),hereda,int(_con),len(_nodo),_causa,int(_vh[-1]),int(_dpv[-1])])\n"
    "                _exph.clear(); _mordh.clear()\n") + A_BORRA

N_NACE = A_NACE + (
    "                if alma is not None and _con and nodo and _nodo:   # ALMA: EL NODO CENTRAL. El cuerpo CONECTADO nace con los mensajes de los que\n"
    "                    #   murieron como EXPOSICIONES SIN CONSECUENCIA (contrato del BLOQUE 4: no toca energia, ni objetos, ni ncod, ni la via\n"
    "                    #   rapida, ni la plasticidad, ni el rng). El bloque de abajo es la VIA LENTA de la mordida, extraida LITERALMENTE.\n"
    "                    for _P7,_R7,_n7 in _nodo[-nodo_lee:]:\n"
    "                        _Pv=np.asarray(_P7,float)\n"
    "                        if lam: _mc7=np.minimum(Wps[_n7],Wns[_n7])*(_Pv>0); Wps[_n7]=Wps[_n7]-lam*_mc7; Wns[_n7]=Wns[_n7]-lam*_mc7\n"
    "                        _ds7=_R7-float((Wps[_n7]-Wns[_n7])@_Pv)\n"
    "                        if _ds7>0: Wps[_n7]=np.clip(Wps[_n7]+eta_s*_ds7*_Pv,0,clip_s)\n"
    "                        else:      Wns[_n7]=np.clip(Wns[_n7]+eta_s*aversion*(-_ds7)*_Pv,0,clip_s)\n")

N_REP2D = A_REP2D + (
    "            if alma is not None and _nmu>=alma_muertes: _Tef=t+1; break"
    "   # ALMA: la serie de cuerpos ES la medida; se para en la muerte numero alma_muertes\n")

N_EXT_H1 = A_EXT_H1 + (
    "    if alma is not None: _ext.update(alma_muertes=alma_muertes,curitas=[list(_c) for _c in _cur],nodo_n=len(_nodo),\n"
    "                       conectado_final=int(_con),dote_final=round(float(dote),4),umbral_final=round(float(rep_umbral),4),\n"
    "                       hereda_final=hereda,T_efectivo=int(_Tef),miedo_inerte=int(_inerte),\n"
    "                       vidas_cuerpo=[int(_x) for _x in _vh],desc_cuerpo=[int(_x) for _x in _dpv],\n"
    "                       nodo_cola=[[list(_p7),float(_r7),int(_n7)] for _p7,_r7,_n7 in _nodo[-60:]],\n"
    "                       alma_cfg=dict(nodo=int(nodo),nodo_k=nodo_k,nodo_lee=nodo_lee,miedo_n=miedo_n,miedo_R=miedo_R,\n"
    "                                     d_dote=d_dote,d_umbral=d_umbral,conectado_ini=int(conectado)))   # ALMA: claves nuevas SOLO con alma\n")

CABECERA = '''"""organismo_alma = experimentos/nivel11_mundo_vivo/organismo_vivo_h1.py (9e99ff87b5e2db1e, el instrumento de
H-1 "QUE LA MUERTE MATE"; aqui solo se LEYO; cadena: organismo_vivo_rep2 96feb4918dc5d694 <- organismo_vivo_rep
aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo_v14 v14.1 feefc88b1fd8d434)
+ EL BLOQUE ALMA (nivel 13): UN NODO CENTRAL y UN ALMA EXTERNA QUE PARCHA AL CUERPO CADA VEZ QUE MUERE.

  alma=None   ->  organismo_vivo_h1 BIT A BIT (todas las claves, mismo consumo del rng del mundo)
  alma=fn     ->  cada muerte: (1) el NODO CENTRAL recibe las ultimas `nodo_k` mordidas CON CONSECUENCIA del cuerpo
                  que muere, como mensajes (patron, R cruda, necesidad activa); (2) se llama a `fn(resumen)` con la
                  causa (la necesidad que llego a cero), la edad, los hijos, las ultimas 20 exposiciones y mordidas
                  y el estado del linaje; (3) `fn` devuelve UNA curita del MENU CERRADO de MENU_curitas.md
                  ('a' conectar al nodo / 'b' subir el miedo escribiendolo en el nodo / 'c' dote mayor /
                   'd' bajar el umbral de reproduccion / 'e' heredar valores (M1) / 'f' nada) y se aplica;
                  (4) el cuerpo siguiente, si el linaje esta CONECTADO, nace leyendo el nodo como EXPOSICIONES SIN
                  CONSECUENCIA (contrato del BLOQUE 4: via lenta, sin energia, sin objetos, sin ncod, sin via
                  rapida, sin plasticidad, sin rng). La corrida termina en la muerte numero `alma_muertes`.

EL NODO NO ES EL CANAL DE b4b: b4b escribe en la TABLA DE PARES (organo de v15f) que esta cadena NO tiene. Lo que
se traduce es su CONTRATO ("exposicion sin consecuencia con la valencia recibida"), ejecutado con el bloque de la
VIA LENTA extraido literalmente de la mordida de h1. Comparar numeros con b4b seria ilegitimo.

EL ALMA ES EL BUSCADOR, NO EL RESULTADO (como JUACO-EVO): lo que encuentre es una HIPOTESIS que hay que volver a
correr SIN alma, con las perillas fijas desde el paso 0, preregistro nuevo y semillas nuevas.

ANCLA DE IDENTIDAD: alma=None -> organismo_vivo_h1 bit a bit en los cinco modos de H-1; ninguna insercion consume
el rng del mundo. Arnes: identidad_alma.py. Generado por construye_alma.py. NO editar a mano."""
'''


def main():
    src = origen(ORIGEN, SHA_H1)
    t = src
    t = sust(t, A_FIRMA, N_FIRMA, 1, 'FIRMA')
    t = sust(t, A_MAESTRA, N_MAESTRA, 1, 'MAESTRA')
    t = sust(t, A_RB, N_RB, 1, 'INIT')
    t = sust(t, A_EXPO, N_EXPO, 1, 'EXPOSICION')
    t = sust(t, A_MORD, N_MORD, 1, 'MORDIDA')
    t = sust(t, A_MUERE, N_MUERE, 1, 'CAUSA')
    t = sust(t, A_BORRA, N_BORRA, 1, 'CURITA')
    t = sust(t, A_NACE, N_NACE, 1, 'NODO')
    t = sust(t, A_REP2D, N_REP2D, 1, 'PARADA')
    t = sust(t, A_EXT_H1, N_EXT_H1, 1, 'SALIDA')
    t = CABECERA + t

    # --- GUARDIA 1: ninguna insercion consume el rng del mundo
    for i, ins in enumerate(NUEVO):
        limpio = '\n'.join(l for l in ins.split('\n') if not l.strip().startswith('#'))
        limpio = re.sub(r'\s{2,}#.*$', '', limpio, flags=re.M)
        if re.search(r'\brng\.', limpio):
            raise SystemExit(f"INSERCION {i}: consume el rng DEL MUNDO. Abortado.\n{ins}")
    # --- GUARDIA 2: no se toca NINGUNA linea de H-1 salvo la firma de run() (la unica sustitucion en linea)
    viejas = [l for l in src.split('\n') if l.strip() and A_FIRMA not in l]
    nuevas = set(l for l in t.split('\n') if l.strip())
    perdidas = [l for l in viejas if l not in nuevas]
    if perdidas:
        raise SystemExit(f"GUARDIA 2: {len(perdidas)} lineas del origen desaparecieron. Ejemplo:\n{perdidas[0][:160]}")
    # --- GUARDIA 3: compila
    compile(t, DESTINO, 'exec')

    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(t)
    print(f"ESCRITO {DESTINO}")
    print(f"  origen  organismo_vivo_h1.py  sha {SHA_H1}")
    print(f"  destino organismo_alma.py     sha {h16(DESTINO)}")
    print(f"  anclas 10/10 · inserciones {len(NUEVO)} · lineas {len(src.splitlines())} -> {len(t.splitlines())}")
    print("  guardias: rng OK · lineas del origen intactas OK · compila OK")


if __name__ == '__main__':
    main()
