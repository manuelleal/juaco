"""Construye experimentos/nivel09_cuerpo_nuevo/organismo_f9.py POR ANCLAS desde organismo_alma2.py
(4fd616aeaf535e61, que aqui SOLO SE LEE; cadena: organismo_alma 7c09cec391daa879 <- organismo_vivo_h1
9e99ff87b5e2db1e <- organismo_vivo_rep2 96feb4918dc5d694 <- organismo_vivo_rep aa823d56c2d4213c <-
organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo/organismo_v14.py v14.1 feefc88b1fd8d434).
No se edita ningun archivo existente (regla 1 de EQUIPO.md). NADA de organismo/ se toca.

POR QUE LA CADENA SIGUE ANCLADA EN v14.1 Y NO EN v14.2 (declarado antes de medir): todo el mundo vivo
(H-1, bloque 2, ALMA) esta medido sobre v14.1. El brazo NADA de la fase 9 TIENE que reproducir el
NADA_CM de H-1 (R0 0.148/0.140) para que las predicciones tengan ancla. v14.2 (= v14.1 + B-5, reparacion
del alias de codigo) MUEVE esa linea base. La fase 9 mide un MECANISMO, no juzga un candidato al tronco
(CRITERIO_TRONCO_v2 no aplica aqui): se queda en v14.1 y se dice.

MISION: llegar a la AGI por este camino. Hoy, FASE 9: ¿puede un CUERPO NUEVO aprender EN MENOS DE UNA VIDA
lo que su linaje ya sabe, por una regla LOCAL, y cambia eso r = descendientes - muertes o R0 frente a H-1?

LAS CUATRO PERILLAS NUEVAS (memoria nueva: CERO estructuras nuevas; todo se calcula y se tira)
  nodo_rel=0   COMO se eligen los `nodo_lee` mensajes que lee el recien nacido conectado.
               0 = RECENCIA (los ultimos `nodo_lee`): es organismo_alma2 BIT A BIT (el brazo CIEGO de ALMA).
               1 = RELEVANCIA VIVA (EL CANDIDATO): el alcance es TODO el nodo y el puntaje es el delta
                   LOCAL |R - (Wps-Wns)@P| con el vector del PROPIO lector, RECALCULADO DESPUES DE CADA
                   MENSAJE ABSORBIDO. "Relevante = lo que mas me cambiaria AHORA": en cuanto aprendio el
                   veneno, el veneno deja de ser relevante y pasa a serlo la comida. Empate por recencia.
                   No guarda nada: el puntaje se calcula y se descarta (memoria nueva CERO).
               3 = RELEVANCIA FIJA (control, y trampa 2 en carne propia): el mismo puntaje calculado UNA
                   SOLA VEZ, con el vector del recien nacido (que es 0) -> el ranking degenera en |R| y
                   se lee casi solo veneno (R=-3 contra +1). PREDICCION ESCRITA: gana p1 y HUNDE c1.
               2 = AZAR (control de ACCESO, no de orden): mismo alcance (todo el nodo), seleccion al azar
                   con rng PROPIO SEM_REL(seed)=870000+1000000*seed. Separa "rankear" de "no expirar".
  con_desde=0  0 = como estaba. c>=1 = el linaje se conecta al nodo recien DESPUES de la muerte numero c
               (los cuerpos 1..c son exactamente NADA). Es el control "nacimiento sin conexion" convertido
               en brazo que PUEDE fallar, con su propia linea base dentro del mismo brazo y la misma semilla.
  rep_acum=0   REPRODUCCION DESACOPLADA DE LA SACIEDAD, perilla APARTE (detras de rep_mide, no del alma).
               0 = la ventana exige rep_X pasos SEGUIDOS saciado (como siempre).
               1 = la ventana CUENTA pasos saciados sin exigir que sean seguidos; el contador `_gv` NO se
               reinicia al bajar de rep_umbral -- pero SI se reinicia AL MORIR: la acumulacion es DENTRO de
               un cuerpo; el recien nacido no hereda el avance de su padre. Sin memoria nueva (reusa `_gv`).
  f9=0         medidas de SOLO LECTURA del cuerpo que muere, calculadas de _exph/_mordh ANTES de limpiarlas:
               p1 (¿rechazo lo MALO para su necesidad activa en su PRIMER encuentro?), c1 (¿mordio lo BUENO
               en su PRIMER encuentro?), t_ok (pasos DESDE SU NACIMIENTO hasta su primera mordida con R>0),
               con_cuerpo (¿estaba conectado?). p1 y c1 van SIEMPRE juntos: es la trampa 2 (acierto sin
               balancear) -- un cuerpo generico-cauto gana p1 y pierde c1, y se muere de hambre.

ANCLA DE IDENTIDAD: con nodo_rel=0, con_desde=0, rep_acum=0 y f9=0 es organismo_alma2 BIT A BIT (y por su
cadena, organismo_alma, organismo_vivo_h1, organismo_vivo y el TRONCO organismo_v14). Con alma=None no
aparece ninguna clave nueva salvo las de rep_acum (que es perilla del mundo, no del alma) y con rep_acum=0
tampoco esa. Ninguna insercion consume el rng del mundo (este constructor lo comprueba con una regex).
Arnes: identidad_f9.py.

Uso:  python experimentos/nivel09_cuerpo_nuevo/construye_f9.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
sys.path[:0] = [AQUI, N13, N11, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

ORIGEN = os.path.join(N13, 'organismo_alma2.py')
DESTINO = os.path.join(AQUI, 'organismo_f9.py')
SHA_ALMA2 = '4fd616aeaf535e61'   # organismo_alma2.py (BLOQUE ALMA, identidad 114/114)
CADENA = {                        # origen del origen: la cadena entera, verificada antes de escribir nada
    os.path.join(N13, 'organismo_alma.py'): '7c09cec391daa879',
    os.path.join(N11, 'organismo_vivo_h1.py'): '9e99ff87b5e2db1e',
    os.path.join(N11, 'organismo_vivo_rep2.py'): '96feb4918dc5d694',
    os.path.join(N11, 'organismo_vivo_rep.py'): 'aa823d56c2d4213c',
    os.path.join(N11, 'organismo_vivo.py'): '20c0961c79de8825',
    os.path.join(RAIZ, 'organismo', 'organismo_v14.py'): 'feefc88b1fd8d434',
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


NUEVO = []
EN_LINEA = []


def sust(texto, viejo, nuevo, n=1, etiqueta='', en_linea=False):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    NUEVO.append(nuevo if en_linea else nuevo.replace(viejo, ''))
    if en_linea:
        EN_LINEA.append(viejo)
    return texto.replace(viejo, nuevo)


# ==================== ANCLAS (copiadas literalmente de organismo_alma2.py 4fd616aeaf535e61) ====================
A_FIRMA = "d_dote=0.1,d_umbral=0.1,menu='abcdef',nodo_baraja=0):"

A_GUARDIAS = ("    if alma is not None and nodo_baraja and not nodo: raise SystemExit"
              "('ALMA2: nodo_baraja=1 exige nodo=1 (no hay nodo que barajar)')\n")

A_INIT = ("    _nbar_n=0   # ALMA2: permutaciones IDENTIDAD del barajado del nodo "
          "(si son muchas, el control no baraja). SOLO LECTURA\n")

A_MUERTE = "            pos=int(rng.integers(L))\n"

A_CONDESDE = "                _nmu+=1\n                if nodo:\n"

A_MEDIDAS = "                _exph.clear(); _mordh.clear()\n"

A_LECTURA = "                    _msg=_nodo[-nodo_lee:]\n"

A_LOOP = "                    for _P7,_R7,_n7 in _msg:\n"

A_TRASLECT = "            if rep2:   # REP2: longitud de la vida que termina y marca del renacer (solo lectura)\n"

A_REPACUM = "            else: _gv=0\n"

A_SALIDA = ("                       baraja_nodo_identidad=int(_nbar_n),sem_baraja_nodo='860000+1000000*seed'))"
            "   # ALMA2: clave nueva SOLO con alma\n")

# ==================== INSERCIONES (ninguna consume el rng DEL MUNDO) ====================
N_FIRMA = "d_dote=0.1,d_umbral=0.1,menu='abcdef',nodo_baraja=0,nodo_rel=0,con_desde=0,rep_acum=0,f9=0):"

N_GUARDIAS = A_GUARDIAS + (
    "    if alma is None: nodo_rel=0; con_desde=0; f9=0   # F9: perillas del NODO, detras de la maestra (inerte: organismo_alma2 EXACTO)\n"
    "    if not rep_mide: rep_acum=0   # F9: rep_acum es perilla DEL MUNDO (detras de la medida), no del alma: vale tambien con alma=None\n"
    "    if nodo_rel not in (0,1,2,3): raise SystemExit('F9: nodo_rel es 0 (recencia), 1 (relevancia viva), 2 (azar sobre todo el nodo) o 3 (relevancia fija)')\n"
    "    if nodo_rel and not nodo: raise SystemExit('F9: nodo_rel exige nodo=1 (no hay nodo que leer)')\n"
    "    if con_desde and not nodo: raise SystemExit('F9: con_desde exige nodo=1 (no hay a que conectarse)')\n"
    "    if con_desde and conectado: raise SystemExit('F9: con_desde y conectado=1 son EXCLUYENTES (o nace conectado o se conecta despues)')\n"
    "    if f9 and not (h1 and rep2): raise SystemExit('F9: f9=1 exige h1=1 y rep2=1 (las medidas del cuerpo usan su nacimiento y su vida)')\n")

N_INIT = A_INIT + (
    "    _rrel=np.random.default_rng(870000+1000000*seed) if (alma is not None and nodo_rel==2) else None"
    "   # F9: rng PROPIO del control de ACCESO (ERR-60: no toca el rng del mundo, ni el de los hijos 700000+,\n"
    "    #        ni el de la herencia barajada 800000+, ni el del alma al azar 850000+, ni el del barajado del nodo 860000+).\n"
    "    _ldiv=0; _nlec=0   # F9: lecturas del nodo cuyo conjunto DIFIERE del de recencia, y lecturas totales. Si _ldiv=0 la perilla es INERTE (ERR-38). SOLO LECTURA\n"
    "    _p1=[]; _c1=[]; _tok=[]; _ncu=[]   # F9: por cuerpo que muere -- rechazo lo malo a la 1a / mordio lo bueno a la 1a / pasos hasta la 1a mordida con R>0 / estaba conectado. SOLO LECTURA (-1 = no hubo ocasion)\n")

N_MUERTE = A_MUERTE + (
    "            if rep_acum: _gv=0   # F9: la ventana ACUMULADA es DENTRO de un cuerpo: el recien nacido NO hereda el avance de su padre\n")

N_CONDESDE = (
    "                _nmu+=1\n"
    "                if con_desde and nodo and _nmu>=con_desde: _con=True   # F9: CONEXION TARDIA (control 'nacimiento sin conexion': los cuerpos 1..con_desde-1 son NADA)\n"
    "                if nodo:\n")

N_MEDIDAS = (
    "                if f9:   # F9: LAS MEDIDAS DEL CUERPO QUE MUERE, de _exph/_mordh ANTES de limpiarlas. Todo SOLO LECTURA.\n"
    "                    #   p1 y c1 van SIEMPRE juntos (trampa 2): lo malo para la necesidad activa es B con hambre y D con sed;\n"
    "                    #   lo bueno es A con hambre y C con sed. _tmu todavia es el instante en que ESTE cuerpo nacio (rep2 lo mueve despues).\n"
    "                    _mal9=[_x9 for _x9 in _exph if _x9[1]==('B' if _x9[2]==0 else 'D')]\n"
    "                    _bue9=[_x9 for _x9 in _exph if _x9[1]==('A' if _x9[2]==0 else 'C')]\n"
    "                    _p1.append(1-int(_mal9[0][3]) if _mal9 else -1)\n"
    "                    _c1.append(int(_bue9[0][3]) if _bue9 else -1)\n"
    "                    _ok9=[_x9 for _x9 in _mordh if _x9[3]>0]\n"
    "                    _tok.append(int(_ok9[0][0]-_tmu) if _ok9 else -1)\n"
    "                    _ncu.append(int(_con))\n") + A_MEDIDAS

N_LECTURA = A_LECTURA + (
    "                    if nodo_rel in (1,3): _msg=list(_nodo)   # F9: el ALCANCE es TODO el nodo (las lecciones no expiran); la SELECCION va abajo\n"
    "                    elif nodo_rel==2: _msg=[_nodo[_i9] for _i9 in sorted(int(_z9) for _z9 in _rrel.choice(len(_nodo),size=min(nodo_lee,len(_nodo)),replace=False))]   # F9: CONTROL DE ACCESO (mismo alcance, orden cronologico, seleccion al azar)\n")

N_LOOP = (
    "                    _sel9=[]\n"
    "                    if nodo_rel in (1,3):   # F9: el puntaje de relevancia = el DELTA LOCAL que la via lenta aplicaria a ese mensaje.\n"
    "                        #   Se calcula sobre el pool (vectorizado), no se guarda nada. lexsort: clave primaria -puntaje, desempate -indice (RECENCIA).\n"
    "                        _Pm9=np.asarray([_z9[0] for _z9 in _msg],float); _Rm9=np.asarray([_z9[1] for _z9 in _msg],float); _Nm9=np.asarray([_z9[2] for _z9 in _msg],int)\n"
    "                        if nodo_rel==3:   # RELEVANCIA FIJA (control): UNA sola vez, con el vector del recien nacido. Degenera en |R|.\n"
    "                            _sc9=np.abs(_Rm9-((Wps[_Nm9]-Wns[_Nm9])*_Pm9).sum(1))\n"
    "                            _sel9=sorted(int(_z9) for _z9 in np.lexsort((-np.arange(len(_msg)),-_sc9))[:min(nodo_lee,len(_msg))])\n"
    "                            _msg=[_msg[_i9] for _i9 in _sel9]\n"
    "                        else: _rst9=list(range(len(_msg)))   # RELEVANCIA VIVA: el puntaje se recalcula DESPUES de cada mensaje absorbido\n"
    "                    for _it9 in range(min(nodo_lee,len(_msg)) if nodo_rel==1 else len(_msg)):\n"
    "                        if nodo_rel==1:\n"
    "                            _sc9=np.abs(_Rm9[_rst9]-((Wps[_Nm9[_rst9]]-Wns[_Nm9[_rst9]])*_Pm9[_rst9]).sum(1))\n"
    "                            _b9=int(np.lexsort((-np.asarray(_rst9,float),-_sc9))[0]); _sel9.append(_rst9[_b9])\n"
    "                            _P7,_R7,_n7=_msg[_rst9.pop(_b9)]\n"
    "                        else: _P7,_R7,_n7=_msg[_it9]\n")

N_TRASLECT = (
    "                    _nlec+=1   # F9: lecturas del nodo (solo lectura)\n"
    "                    if nodo_rel: _ldiv+=int(len(_nodo)>nodo_lee or (nodo_rel==1 and _sel9!=sorted(_sel9)))"
    "   # F9: la seleccion NO PUDO ser la de recencia. Si lect_div=0 la perilla es INERTE (ERR-38)\n") + A_TRASLECT

N_REPACUM = ("            else: _gv=(_gv if rep_acum else 0)"
             "   # F9: rep_acum=1 -> la ventana CUENTA pasos saciados aunque no sean seguidos (rep_acum=0: identico)\n")

N_SALIDA = A_SALIDA + (
    "    if alma is not None and f9: _ext.update(f9=dict(nodo_rel=int(nodo_rel),con_desde=int(con_desde),\n"
    "                       lect_div=int(_ldiv),lecturas=int(_nlec),sem_rel='870000+1000000*seed',\n"
    "                       p1=[int(_x) for _x in _p1],c1=[int(_x) for _x in _c1],t_ok=[int(_x) for _x in _tok],\n"
    "                       con_cuerpo=[int(_x) for _x in _ncu]))   # F9: claves nuevas SOLO con alma y f9=1\n"
    "    if rep_acum: _ext.update(rep_acum=1)   # F9: perilla DEL MUNDO (vale con alma=None); con rep_acum=0 no aparece\n")

CABECERA = '''"""organismo_f9 = organismo_alma2.py (4fd616aeaf535e61; aqui solo se LEYO; cadena: organismo_alma
7c09cec391daa879 <- organismo_vivo_h1 9e99ff87b5e2db1e <- organismo_vivo_rep2 96feb4918dc5d694 <-
organismo_vivo_rep aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO
organismo/organismo_v14.py v14.1 feefc88b1fd8d434) + LAS CUATRO PERILLAS DE LA FASE 9.

  nodo_rel=0, con_desde=0, rep_acum=0, f9=0  ->  organismo_alma2 BIT A BIT (todos sus brazos)
  nodo_rel=1  ->  RELEVANCIA VIVA: el recien nacido lee TODO el nodo por puntaje local
                  |R - (Wps-Wns)@P| con SU PROPIO vector, sobre TODO el nodo; los nodo_lee mayores,
                  en orden cronologico, empate por recencia. Cero memoria nueva.
  nodo_rel=2  ->  CONTROL DE ACCESO: mismo alcance, seleccion AL AZAR (rng propio 870000+1000000*seed).
  con_desde=c ->  el linaje se conecta recien tras la muerte c (los cuerpos 1..c-1 son NADA).
  rep_acum=1  ->  la ventana de reproduccion cuenta pasos saciados SIN exigir que sean seguidos; se
                  reinicia AL MORIR (dentro de un cuerpo). Perilla DEL MUNDO, aparte del mecanismo.
  f9=1        ->  medidas de solo lectura del cuerpo que muere: p1, c1, t_ok, con_cuerpo.

LAS MEDIDAS p1 Y c1 VAN SIEMPRE JUNTAS (trampa 2 de la noche del 17-sep): un cuerpo generico-cauto sube
p1 y hunde c1, y se muere de hambre. Ningun veredicto se lee sobre p1 solo.

Arnes: identidad_f9.py. Generado por construye_f9.py. NO editar a mano."""
'''


def main():
    if h16(ORIGEN) != SHA_ALMA2:
        raise SystemExit(f"ORIGEN {ORIGEN}: sha {h16(ORIGEN)}, se esperaba {SHA_ALMA2}. Abortado.")
    for p, s in CADENA.items():
        if h16(p) != s:
            raise SystemExit(f"CADENA {p}: sha {h16(p)}, se esperaba {s}. Abortado.")
    src = open(ORIGEN, encoding='utf-8').read()
    t = src
    t = sust(t, A_FIRMA, N_FIRMA, 1, 'FIRMA', en_linea=True)
    t = sust(t, A_GUARDIAS, N_GUARDIAS, 1, 'GUARDIAS')
    t = sust(t, A_INIT, N_INIT, 1, 'INIT')
    t = sust(t, A_MUERTE, N_MUERTE, 1, 'REP_ACUM_MUERTE')
    t = sust(t, A_CONDESDE, N_CONDESDE, 1, 'CON_DESDE')
    t = sust(t, A_MEDIDAS, N_MEDIDAS, 1, 'MEDIDAS_DEL_CUERPO')
    t = sust(t, A_LECTURA, N_LECTURA, 1, 'ALCANCE_DEL_NODO')
    t = sust(t, A_LOOP, N_LOOP, 1, 'SELECCION_Y_LECTURA', en_linea=True)
    t = sust(t, A_TRASLECT, N_TRASLECT, 1, 'CUENTA_DE_LECTURAS')
    t = sust(t, A_REPACUM, N_REPACUM, 1, 'REP_ACUM', en_linea=True)
    t = sust(t, A_SALIDA, N_SALIDA, 1, 'SALIDA')
    t = CABECERA + t

    # --- GUARDIA 1: ninguna insercion consume el rng DEL MUNDO
    for i, ins in enumerate(NUEVO):
        limpio = '\n'.join(l for l in ins.split('\n') if not l.strip().startswith('#'))
        limpio = re.sub(r'\s{2,}#.*$', '', limpio, flags=re.M)
        if re.search(r'\brng\.', limpio):
            raise SystemExit(f"INSERCION {i}: consume el rng DEL MUNDO. Abortado.\n{ins}")
    # --- GUARDIA 2: solo desaparecen las lineas declaradas como sustitucion EN LINEA
    viejas = [l for l in src.split('\n') if l.strip() and not any(a.strip() in l for a in EN_LINEA)]
    nuevas = set(l for l in t.split('\n') if l.strip())
    perdidas = [l for l in viejas if l not in nuevas]
    if perdidas:
        raise SystemExit(f"GUARDIA 2: {len(perdidas)} lineas del origen desaparecieron. Ejemplo:\n{perdidas[0][:160]}")
    # --- GUARDIA 3: compila
    compile(t, DESTINO, 'exec')

    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(t)
    print(f"ESCRITO {DESTINO}")
    print(f"  origen  organismo_alma2.py  sha {SHA_ALMA2}")
    print(f"  destino organismo_f9.py     sha {h16(DESTINO)}")
    print(f"  cadena verificada: {len(CADENA)} shas hasta el TRONCO v14.1 feefc88b1fd8d434")
    print(f"  anclas 11/11 · sustituciones en linea {len(EN_LINEA)} · lineas {len(src.splitlines())} -> {len(t.splitlines())}")
    print("  guardias: rng DEL MUNDO OK · lineas del origen intactas OK · compila OK")


if __name__ == '__main__':
    main()
