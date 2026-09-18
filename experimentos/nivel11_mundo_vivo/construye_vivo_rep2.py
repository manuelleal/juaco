"""Construye experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py POR ANCLAS desde organismo_vivo_rep.py
(aa823d56c2d4213c, el instrumento del bloque 1 de reproduccion, que aqui SOLO SE LEE; a su vez por anclas desde
organismo_vivo.py 20c0961c79de8825 y del TRONCO CONGELADO organismo/organismo_v14.py v14.1 feefc88b1fd8d434).
No se edita ningun archivo existente (regla 1 de EQUIPO.md; manifiesto.py).

BLOQUE 2 DE REPRODUCCION (PREREGISTRO_reproduccion_2.md; ERR-40: "la ventana de viabilidad no esta ligada a la
supervivencia: premia atracones que mueren mas"). La MEDIDA nueva NO necesita codigo en el organismo: es el
CRECIMIENTO NETO DEL LINAJE  r = descendientes - muertes  (nacimientos menos muertes por corrida; tipo de cambio 1:1,
el de la dinamica de poblaciones), calculada por el runner a partir de dos claves que ya existen. Lo que este
instrumento agrega, todo de SOLO LECTURA y detras de la perilla `rep2`, son los DIAGNOSTICOS que hacen comprobable el
diagnostico de ERR-40 y que miden lo que habrian quitado las candidatas (b) y (c) del encargo:
  desc_regalo  ventanas (descendientes) cuya cuenta EMPEZO antes de que el regalo del renacer se agotara: el cuerpo
               renace en E=Ag=0.6 y ese regalo dura 0.6/costo = 600 pasos (rep2_regalo). t=0 cuenta como nacimiento
               (E=Ag=1.0, el mismo regalo). Es exactamente lo que la candidata (b) habria excluido.
  vidas        longitudes de las vidas que terminaron (hasta 400) y vida_final (la que sigue viva al acabar T): la
               distribucion de vidas es lo que liga el conteo a la supervivencia.

ANCLA DE IDENTIDAD: con reproduccion=0 (por defecto) es organismo_vivo BIT A BIT (la cadena entera); con rep2=0 es
organismo_vivo_rep BIT A BIT en todas sus claves; con rep2=1 las claves viejas salen bit a bit y solo aparecen 4 nuevas.
Ninguna linea nueva llama al rng (lo comprueba este constructor). Arnes: identidad_vivo_rep2.py.

PERILLAS NUEVAS:
  rep2=0          diagnosticos de ERR-40 (exige reproduccion=1 y rep_mide=1)
  rep2_regalo=600 duracion del regalo del renacer en pasos = A_muerte / costo = 0.6 / 0.001

Uso:  python experimentos/nivel11_mundo_vivo/construye_vivo_rep2.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

SHA_REP = 'aa823d56c2d4213c'    # organismo_vivo_rep.py (bloque 1; instrumento del dato vivo_rep_s221-240_20260918_091428)
SHA_VIVO = '20c0961c79de8825'   # organismo_vivo.py
SHA_V14 = 'feefc88b1fd8d434'    # organismo/organismo_v14.py (v14.1)


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


# ============================ ANCLAS (copiadas literalmente de organismo_vivo_rep.py aa823d56c2d4213c) ============================
A_FIRMA = "rep_nec=0,rep_cuello=0):"
A_MAESTRA = ("    if not reproduccion: rep_mide=0; rep_nec=0; rep_cuello=0; rep_coste=0.0   # REP: perilla MAESTRA apagada -> "
             "todo lo de abajo es inerte: organismo_vivo EXACTO\n")
A_ESTADO = ("_dsac={k:0 for k in PAT}; _sac=False; _cue2=False   # REP: ventana de viabilidad, descendientes viables, pasos "
            "viables, tabla de decisiones/mordidas SACIADO (solo lectura si rep_coste=0); _cue2 = CUELLO_MIN activo\n")
A_VENTANA = "            if E>=rep_umbral and Ag>=rep_umbral: _gv+=1; _pv+=1\n"
A_DESC = "                _desc+=1; _dq[q(t)]+=1; _gv=0\n"
A_MUERTE = "            pos=int(rng.integers(L))\n"
A_EXT = ("                                 rep=dict(mide=int(rep_mide),X=rep_X,umbral=rep_umbral,coste=rep_coste,nec=int(rep_nec),"
         "cuello=int(rep_cuello)))   # REP: claves nuevas SOLO con reproduccion=1\n")

CAB = '''"""organismo_vivo_rep2 = organismo_vivo_rep.py (aa823d56c2d4213c; aqui solo se LEYO; cadena: organismo_vivo 20c0961c79de8825
<- TRONCO CONGELADO organismo_v14 v14.1 feefc88b1fd8d434) + DIAGNOSTICOS DE ERR-40 para el bloque 2 de reproduccion
(PREREGISTRO_reproduccion_2.md): la medida nueva es el crecimiento neto del linaje r = descendientes - muertes (la calcula el
runner con claves que ya existen); aqui solo se agregan, de SOLO LECTURA y detras de `rep2`, desc_regalo (ventanas que
empezaron dentro de los 600 pasos que dura el regalo del renacer) y las longitudes de las vidas.
ANCLA DE IDENTIDAD: reproduccion=0 -> organismo_vivo BIT A BIT; rep2=0 -> organismo_vivo_rep BIT A BIT; rep2=1 -> claves
viejas bit a bit + 4 nuevas. Arnes: identidad_vivo_rep2.py. Generado por construye_vivo_rep2.py. NO editar a mano."""
'''


if __name__ == '__main__':
    origen(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14)
    origen(os.path.join(AQUI, 'organismo_vivo.py'), SHA_VIVO)
    s = origen(os.path.join(AQUI, 'organismo_vivo_rep.py'), SHA_REP)

    s = sust(s, A_FIRMA, "rep_nec=0,rep_cuello=0,rep2=0,rep2_regalo=600):", etiqueta='firma: perillas rep2')
    s = sust(s, A_MAESTRA, A_MAESTRA +
             "    if not reproduccion: rep2=0   # REP2: detras de la maestra\n"
             "    if rep2 and not rep_mide: raise SystemExit('REP2: rep2=1 exige rep_mide=1 (la ventana es el nacimiento)')\n",
             etiqueta='guardias rep2')
    s = sust(s, A_ESTADO, A_ESTADO +
             "    _tmu=0; _vidas=[]; _dreg=0; _gv0=0   # REP2: marca del ultimo renacer (t=0 cuenta como nacimiento), longitudes de vida, ventanas financiadas por el regalo del renacer, primer paso saciado de la ventana en curso. SOLO LECTURA\n",
             etiqueta='estado rep2')
    s = sust(s, A_VENTANA,
             "            if E>=rep_umbral and Ag>=rep_umbral:\n"
             "                if rep2 and _gv==0: _gv0=t   # REP2: primer paso saciado de la ventana en curso\n"
             "                _gv+=1; _pv+=1\n", etiqueta='inicio de la ventana')
    s = sust(s, A_DESC, A_DESC +
             "                if rep2 and _gv0-_tmu<rep2_regalo: _dreg+=1   # REP2: la ventana empezo antes de que el regalo del renacer (0.6/0.6 = 600 pasos de drenaje) se agotara\n",
             etiqueta='descendiente financiado por el regalo')
    s = sust(s, A_MUERTE, A_MUERTE +
             "            if rep2:   # REP2: longitud de la vida que termina y marca del renacer (solo lectura)\n"
             "                if len(_vidas)<400: _vidas.append(t-_tmu)\n"
             "                _tmu=t\n", etiqueta='vidas')
    s = sust(s, A_EXT, A_EXT +
             "    if rep2: _ext.update(desc_regalo=_dreg,vidas=list(_vidas),vida_final=T-_tmu,rep2=dict(regalo=rep2_regalo))   # REP2: claves nuevas SOLO con rep2=1\n",
             etiqueta='claves rep2')

    malas = [x for x in NUEVO if 'rng' in x]
    if malas:
        raise SystemExit("Una insercion nombra al rng: " + repr(malas[:2]))
    d = os.path.join(AQUI, 'organismo_vivo_rep2.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(CAB + s)
    print(f"  escrito {d}")
    print(f"  sha organismo_v14.py (tronco, solo lectura)     {SHA_V14}")
    print(f"  sha organismo_vivo.py (solo lectura)            {SHA_VIVO}")
    print(f"  sha organismo_vivo_rep.py (origen, solo lectura) {SHA_REP}")
    print(f"  sha organismo_vivo_rep2.py                       {h16(d)}")
    print(f"  sha construye_vivo_rep2.py                       {h16(os.path.abspath(__file__))}")
    print(f"  inserciones: {len(NUEVO)}; ninguna nombra al rng.")
    print("  siguiente: python experimentos/nivel11_mundo_vivo/identidad_vivo_rep2.py")
