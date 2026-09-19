"""Construye experimentos/nivel13_alma/organismo_alma2.py POR ANCLAS desde organismo_alma.py
(7c09cec391daa879, que aqui SOLO SE LEE; cadena: organismo_vivo_h1 9e99ff87b5e2db1e <- organismo_vivo_rep2
96feb4918dc5d694 <- organismo_vivo_rep aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO
organismo/organismo_v14.py v14.1 feefc88b1fd8d434). No se edita ningun archivo existente (regla 1 de EQUIPO.md).

MISION: llegar a la AGI por este camino, hasta la fase 10 y mas alla. Hoy: los CONTROLES que el preregistro del
BLOQUE ALMA exige ANTES de la serie (encargo del coordinador, 18 sep 2026).

LOS TRES BRAZOS QUE FALTABAN Y LO QUE CADA UNO SEPARA
  BARAJA-NODO   : el hijo lee el nodo con las RECOMPENSAS PERMUTADAS ENTRE MENSAJES (mismos patrones, mismas
                  recompensas, emparejadas al azar: las marginales se conservan, la ASOCIACION se destruye).
                  Separa "el nodo transmite CONTENIDO" de "el nodo transmite MAGNITUD (una cautela generica)".
                  Es el control que decidio H1-4 en H-1, traducido al canal.
  ALMA-SIN-NODO : el alma juega con el menu SIN (a) ni (b) -> el nodo se llena y NADIE se conecta nunca.
                  Separa "el efecto es del NODO" de "el efecto es de las perillas del mundo (c)/(d)/(e)".
  NODO-CIEGO    : el linaje nace CONECTADO desde el cuerpo 1 (`conectado=1`) y las curitas son AL AZAR sobre el
                  menu sin (a). Separa "el NODO" de "el ALMA que elige": es el nodo sin nadie que razone.

PERILLAS NUEVAS (las dos detras de la maestra `alma`; con menu='abcdef' y nodo_baraja=0 es organismo_alma BIT A BIT)
  menu='abcdef'   subconjunto no vacio y sin repeticiones de 'abcdef'. Es lo que el resumen le OFRECE al alma y
                  lo que el instrumento ACEPTA: una curita fuera del menu ABORTA (un error de programa no se
                  traga en silencio). La tolerancia a respuestas invalidas de un agente vive en el RUNNER, que
                  las registra como (f) y sigue: el instrumento es estricto, el buzon es paciente.
  nodo_baraja=0   1 -> en CADA nacimiento conectado, las recompensas de los `nodo_lee` mensajes que el hijo va a
                  leer se PERMUTAN entre si con un rng PROPIO SEM_BARAJA_NODO(seed) = 860000 + 1000000*seed
                  (no toca el rng del mundo, ni el de los hijos 700000+..., ni el de la herencia barajada
                  800000+..., ni el del alma al azar 850000+...; ERR-60). Los patrones y las necesidades NO se
                  tocan: el hijo ve exactamente los mismos patrones y exactamente las mismas recompensas, mal
                  emparejadas. Exige nodo=1.

ANCLA DE IDENTIDAD: con menu='abcdef' y nodo_baraja=0 es organismo_alma BIT A BIT en todos sus brazos (y por su
cadena, organismo_vivo_h1, organismo_vivo y el TRONCO organismo_v14); con alma=None ni siquiera aparece la clave
nueva `alma2`. Ninguna insercion consume el rng del mundo (lo comprueba este constructor con una regex).
Arnes: identidad_alma2.py.

Uso:  python experimentos/nivel13_alma/construye_alma2.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

ORIGEN = os.path.join(AQUI, 'organismo_alma.py')
DESTINO = os.path.join(AQUI, 'organismo_alma2.py')
SHA_ALMA = '7c09cec391daa879'   # organismo_alma.py (BLOQUE ALMA, identidad 64/64)
SHA_H1 = '9e99ff87b5e2db1e'     # organismo_vivo_h1.py (H-1)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


NUEVO = []
EN_LINEA = []   # anclas que SUSTITUYEN una linea del origen (se declaran para la guardia 2)


def sust(texto, viejo, nuevo, n=1, etiqueta='', en_linea=False):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:70]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    NUEVO.append(nuevo.replace(viejo, '') if not en_linea else nuevo)
    if en_linea:
        EN_LINEA.append(viejo)
    return texto.replace(viejo, nuevo)


# ==================== ANCLAS (copiadas literalmente de organismo_alma.py 7c09cec391daa879) ====================
A_FIRMA = "d_dote=0.1,d_umbral=0.1):"

A_GUARDIAS = ("    if alma is not None and not nodo and conectado: raise SystemExit"
              "('ALMA: conectado=1 exige nodo=1 (no hay a que conectarse)')\n")

A_INIT = ("    #        SOLO LECTURA salvo el nodo y las tres perillas declaradas (dote, rep_umbral, hereda). "
          "Ninguna linea de aqui consume el rng.\n")

A_MENU_RES = "                          R0=round(_desc/max(deaths,1),4),menu=['a','b','c','d','e','f'])\n"

A_GUARDA_C = ("                if _c9 not in ('a','b','c','d','e','f'): raise SystemExit"
              "(f'ALMA: curita {_c9!r} fuera del MENU CERRADO (a,b,c,d,e,f)')\n")

A_LEE = "                    for _P7,_R7,_n7 in _nodo[-nodo_lee:]:\n"

A_EXT = ("                                     d_dote=d_dote,d_umbral=d_umbral,conectado_ini=int(conectado)))"
         "   # ALMA: claves nuevas SOLO con alma\n")

# ==================== INSERCIONES (ninguna consume el rng del mundo) ====================
N_FIRMA = "d_dote=0.1,d_umbral=0.1,menu='abcdef',nodo_baraja=0):"

N_GUARDIAS = A_GUARDIAS + (
    "    if alma is None: nodo_baraja=0   # ALMA2: detras de la maestra (inerte: organismo_alma EXACTO)\n"
    "    if alma is not None and (not menu or len(set(menu))!=len(menu) or any(_z0 not in 'abcdef' for _z0 in menu)):\n"
    "        raise SystemExit(f'ALMA2: menu={menu!r} debe ser un subconjunto no vacio y sin repeticiones de abcdef')\n"
    "    if alma is not None and nodo_baraja and not nodo: raise SystemExit('ALMA2: nodo_baraja=1 exige nodo=1 (no hay nodo que barajar)')\n")

N_INIT = A_INIT + (
    "    _rbn=np.random.default_rng(860000+1000000*seed) if (alma is not None and nodo_baraja) else None"
    "   # ALMA2: rng PROPIO del barajado DEL NODO (ERR-60: no toca el rng del mundo, ni el de los hijos 700000+,\n"
    "    #        ni el de la herencia barajada 800000+, ni el del alma al azar 850000+). Permutacion NUEVA en cada nacimiento conectado.\n"
    "    _nbar_n=0   # ALMA2: permutaciones IDENTIDAD del barajado del nodo (si son muchas, el control no baraja). SOLO LECTURA\n")

N_MENU_RES = ("                          R0=round(_desc/max(deaths,1),4),menu=[_z1 for _z1 in menu],"
              "nodo_baraja=int(nodo_baraja))\n")

N_GUARDA_C = A_GUARDA_C + (
    "                if _c9 not in menu: raise SystemExit"
    "(f'ALMA2: curita {_c9!r} fuera del menu OFRECIDO {menu!r} (el runner es quien tolera y registra (f))')\n")

N_LEE = (
    "                    _msg=_nodo[-nodo_lee:]\n"
    "                    if nodo_baraja:   # ALMA2: CONTROL DE CONTENIDO. Las recompensas se permutan ENTRE mensajes: mismos patrones,\n"
    "                        #   mismas recompensas, mismas necesidades -- las MARGINALES se conservan y la ASOCIACION patron<->recompensa se destruye.\n"
    "                        _pn=_rbn.permutation(len(_msg)); _nbar_n+=int(bool((_pn==np.arange(len(_msg))).all()))\n"
    "                        _msg=[[_msg[_i7][0],_msg[int(_pn[_i7])][1],_msg[_i7][2]] for _i7 in range(len(_msg))]\n"
    "                    for _P7,_R7,_n7 in _msg:\n")

N_EXT = A_EXT + (
    "    if alma is not None: _ext.update(alma2=dict(menu=''.join(menu),nodo_baraja=int(nodo_baraja),\n"
    "                       baraja_nodo_identidad=int(_nbar_n),sem_baraja_nodo='860000+1000000*seed'))"
    "   # ALMA2: clave nueva SOLO con alma\n")

CABECERA = '''"""organismo_alma2 = organismo_alma.py (7c09cec391daa879, el instrumento del BLOQUE ALMA, identidad 64/64;
aqui solo se LEYO; cadena: organismo_vivo_h1 9e99ff87b5e2db1e <- organismo_vivo_rep2 96feb4918dc5d694 <-
organismo_vivo_rep aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo_v14 v14.1
feefc88b1fd8d434) + LOS TRES CONTROLES que el PREREGISTRO_alma.md exige ANTES de la serie.

  menu='abcdef', nodo_baraja=0  ->  organismo_alma BIT A BIT (con alma=None ni aparece la clave `alma2`)
  menu=<subconjunto>            ->  el resumen le OFRECE al alma ese menu y el instrumento ACEPTA solo ese menu.
                                    ALMA-SIN-NODO = menu sin (a) ni (b): el nodo se llena y nadie se conecta.
  nodo_baraja=1                 ->  en cada nacimiento conectado, las recompensas de los mensajes que el hijo va
                                    a leer se PERMUTAN entre si (rng propio 860000+1000000*seed): mismos patrones,
                                    mismas recompensas, mal emparejadas. Es el control de CONTENIDO (H1-4).
  conectado=1 (ya existia)      ->  NODO-CIEGO: el linaje nace conectado y las curitas van al azar sin (a).

EL INSTRUMENTO ES ESTRICTO, EL BUZON ES PACIENTE: una curita fuera del menu ABORTA aqui; la tolerancia a las
respuestas invalidas de un agente externo vive en corre_alma.py, que las registra como (f) y sigue.

Arnes: identidad_alma2.py. Generado por construye_alma2.py. NO editar a mano."""
'''


def main():
    src = origen(ORIGEN, SHA_ALMA)
    h1 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo', 'organismo_vivo_h1.py')
    if h16(h1) != SHA_H1:
        raise SystemExit(f"ORIGEN DEL ORIGEN {h1}: sha {h16(h1)}, se esperaba {SHA_H1}. Abortado.")
    t = src
    t = sust(t, A_FIRMA, N_FIRMA, 1, 'FIRMA', en_linea=True)
    t = sust(t, A_GUARDIAS, N_GUARDIAS, 1, 'GUARDIAS')
    t = sust(t, A_INIT, N_INIT, 1, 'INIT')
    t = sust(t, A_MENU_RES, N_MENU_RES, 1, 'MENU_RESUMEN', en_linea=True)
    t = sust(t, A_GUARDA_C, N_GUARDA_C, 1, 'GUARDA_CURITA')
    t = sust(t, A_LEE, N_LEE, 1, 'BARAJA_NODO', en_linea=True)
    t = sust(t, A_EXT, N_EXT, 1, 'SALIDA')
    t = CABECERA + t

    # --- GUARDIA 1: ninguna insercion consume el rng del mundo
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
    print(f"  origen  organismo_alma.py   sha {SHA_ALMA}")
    print(f"  destino organismo_alma2.py  sha {h16(DESTINO)}")
    print(f"  anclas 7/7 · sustituciones en linea {len(EN_LINEA)} · lineas {len(src.splitlines())} -> {len(t.splitlines())}")
    print("  guardias: rng OK · lineas del origen intactas OK · compila OK")


if __name__ == '__main__':
    main()
