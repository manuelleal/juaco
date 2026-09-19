"""Construye experimentos/nivel11_mundo_vivo/organismo_vivo_h1.py POR ANCLAS desde organismo_vivo_rep2.py
(96feb4918dc5d694, el instrumento del bloque 2 de reproduccion, que aqui SOLO SE LEE; cadena: organismo_vivo_rep
aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo/organismo_v14.py v14.1
feefc88b1fd8d434). No se edita ningun archivo existente (regla 1 de EQUIPO.md; manifiesto.py).

MISION: llegar a la AGI por este camino. Hoy: que la muerte mate de verdad, para que el linaje signifique algo.

H-1 (PREREGISTRO_h1_muerte.md; SALA4 §B E-1 y §C H-1): hoy la muerte NO mata. El renacer del tronco es
`if E<=0 or Ag<=0: deaths+=1; E=.6; Ag=.6; pos=azar` y CONSERVA Wp, Wn, KW, activa, Wps, Wns, ncod: el individuo es
inmortal en memoria y el renacer es un RECURSO (600 pasos de drenaje regalados) que financia el 34-77 % de las
ventanas de reproduccion del bloque 2. Este instrumento agrega la perilla `muerte_real`:

  muerte_real=0  ->  organismo_vivo_rep2 BIT A BIT (la ancla; toda la cadena hacia atras se conserva)
  muerte_real=1  ->  al morir, la memoria del individuo SE BORRA (valores rapidos Wp/Wn, valores lentos Wps/Wns,
                     tabla de codigos KW/activa, evidencia por codigo ncod, estadisticos de plasticidad mu/err/
                     mup/mun/zp/zn, predictor Wpe/Wke, trazas el/tr, politica de locomocion Wl, memoria de rechazo)
                     y el cuerpo siguiente NACE VACIO, con rng PROPIO derivado y con la DOTE que pago su padre.

PERILLAS NUEVAS
  muerte_real=0   la muerte borra al individuo (exige h1=1; detras de la maestra `reproduccion`)
  hereda='nada'   'nada' | 'M1' (los valores lentos Wps/Wns, el VECTOR sobre la retina) |
                  'M1+pares' (M1 + el TOKEN: KW/activa + los pares codigo<->valor Wp/Wn/ncod y sus estadisticos) |
                  'baraja' (M1 con los 6 pixeles PERMUTADOS: misma magnitud, contenido equivocado; el control que decide)
  dote=0.6        E y Ag con que nace el hijo, PAGADOS por el padre al cerrarse la ventana (0 < dote < rep_umbral).
                  Es exactamente el tamano del regalo de hoy (0.6): lo unico que cambia es QUIEN LO PAGA.
  cola_max=200    la cola de descendientes por nacer (FIFO; si desborda se descarta el mas viejo y se cuenta)
  h1=0            diagnosticos de solo lectura del bloque (exige rep2=1)

SEMILLAS DE LOS CUERPOS (ERR-60, escrito ANTES de correr nada): el encargo pedia `seed + 700000 + k`. Esa formula
COLISIONA entre semillas vecinas (seed=701,k=400 y seed=702,k=399 dan la misma semilla) — es el defecto I6 que
SALA2 §B.1 ya tenia y que la sala 4 recogio en E-4 ("los rng de los hijos colisionan entre semillas vecinas"). Se
corrige aqui, antes de medir:
        SEM_HIJO(seed, k)   = 700000 + 1000000*seed + k        (guarda dura: k < 100000)
        SEM_BARAJA(seed)    = 800000 + 1000000*seed            (un generador propio; permutacion NUEVA por parto)
Ninguno choca con el rng del mundo (`seed`) ni con el del control barajado del mundo vivo (`seed + 900000`).

ANCLA DE IDENTIDAD: con muerte_real=0 y h1=0 (por defecto) es organismo_vivo_rep2 BIT A BIT, clave por clave y con
el mismo consumo del rng DEL MUNDO; con h1=1 y muerte_real=0 las claves viejas salen bit a bit y solo aparecen las
claves nuevas; con reproduccion=0 todo lo de H-1 es inerte. NINGUNA insercion consume el rng del mundo (lo comprueba
este constructor con una expresion regular). Arnes: identidad_vivo_h1.py.

Uso:  python experimentos/nivel11_mundo_vivo/construye_vivo_h1.py
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

SHA_REP2 = '96feb4918dc5d694'   # organismo_vivo_rep2.py (bloque 2; instrumento de vivo_rep2_s261-280 y s281-300)
SHA_REP = 'aa823d56c2d4213c'    # organismo_vivo_rep.py
SHA_VIVO = '20c0961c79de8825'   # organismo_vivo.py
SHA_V14 = 'feefc88b1fd8d434'    # organismo/organismo_v14.py (v14.1, TRONCO CONGELADO)


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


# ==================== ANCLAS (copiadas literalmente de organismo_vivo_rep2.py 96feb4918dc5d694) ====================
A_FIRMA = "rep2=0,rep2_regalo=600):"
A_MAESTRA = ("    if not reproduccion: rep2=0   # REP2: detras de la maestra\n"
             "    if rep2 and not rep_mide: raise SystemExit('REP2: rep2=1 exige rep_mide=1 (la ventana es el nacimiento)')\n")
A_ESTADO = ("    _tmu=0; _vidas=[]; _dreg=0; _gv0=0   # REP2: marca del ultimo renacer (t=0 cuenta como nacimiento), "
            "longitudes de vida, ventanas financiadas por el regalo del renacer, primer paso saciado de la ventana en curso. SOLO LECTURA\n")
A_BUCLE = "        return best\n    for t in range(T):\n"
A_PAGO = ("                if rep_coste: E-=rep_coste; Ag-=rep_coste   # REP: el padre paga en los dos ejes; "
          "por construccion no mata (umbral - coste > 0)\n")
A_MUERTE = ("            if rep2:   # REP2: longitud de la vida que termina y marca del renacer (solo lectura)\n"
            "                if len(_vidas)<400: _vidas.append(t-_tmu)\n"
            "                _tmu=t\n")
A_EXT = ("    if rep2: _ext.update(desc_regalo=_dreg,vidas=list(_vidas),vida_final=T-_tmu,rep2=dict(regalo=rep2_regalo))"
         "   # REP2: claves nuevas SOLO con rep2=1\n")

# ==================== INSERCIONES ====================
I_FIRMA = "rep2=0,rep2_regalo=600,muerte_real=0,hereda='nada',dote=0.6,cola_max=200,h1=0):"

I_MAESTRA = (
    "    if not reproduccion: muerte_real=0; h1=0; hereda='nada'   # H1: detras de la maestra (inerte: organismo_vivo EXACTO)\n"
    "    if muerte_real and not h1: raise SystemExit('H1: muerte_real=1 exige h1=1 (los diagnosticos del linaje SON la medida)')\n"
    "    if h1 and not rep2: raise SystemExit('H1: h1=1 exige rep2=1 (la marca del nacimiento y las vidas vienen de rep2)')\n"
    "    if hereda not in ('nada','M1','M1+pares','baraja'): raise SystemExit(\"H1: hereda es 'nada', 'M1', 'M1+pares' o 'baraja'\")\n"
    "    if hereda!='nada' and not muerte_real: raise SystemExit('H1: hereda exige muerte_real=1 (sin muerte no hay parto)')\n"
    "    if muerte_real and rep_coste: raise SystemExit('H1: dote y rep_coste son EXCLUYENTES (el padre paga una sola vez)')\n"
    "    if muerte_real and not (0<dote<rep_umbral): raise SystemExit('H1: la dote debe cumplir 0 < dote < rep_umbral (pagarla no puede matar al padre)')\n")

I_ESTADO = (
    "    _cola=[]; _nac=0; _fund=0; _dfund=0; _dpv=[]; _dv=0; _cdes=0; _tfund=[]; _svid=0; _esfund=True; _nbar=0; _vh=[]; _org=[]   # H1: cola FIFO de descendientes por nacer (con la memoria que se lleva el hijo y su dote), partos, fundaciones del mundo (linaje extinto), ventanas financiadas por una fundacion NO pagada, descendientes por cuerpo, del cuerpo en curso, descartes por desborde, pasos de cada fundacion, suma de vidas SIN tope, si el cuerpo actual nacio de un regalo, permutaciones identidad en BARAJA, vidas SIN tope y origen de cada cuerpo (0 fundacion regalada, 1 dote pagada). SOLO LECTURA salvo la cola y la dote\n"
    "    _rb=np.random.default_rng(800000+1000000*seed) if (muerte_real and hereda=='baraja') else None   # H1: rng PROPIO del barajado (ERR-60); no toca el rng del mundo ni el del cuerpo\n")

I_BUCLE = (
    "        return best\n"
    "    def _snap():   # H1: la memoria que se lleva el hijo, congelada EN EL MOMENTO DEL PARTO (no en la muerte del padre)\n"
    "        _m={'dote':dote}\n"
    "        if hereda in ('M1','M1+pares','baraja'): _m['Wps']=Wps.copy(); _m['Wns']=Wns.copy()\n"
    "        if hereda=='M1+pares':\n"
    "            _m.update(KW=KW.copy(),activa=activa.copy(),Wp=Wp.copy(),Wn=Wn.copy(),mu=mu.copy(),err=err.copy(),\n"
    "                      mup=mup.copy(),mun=mun.copy(),zp=zp.copy(),zn=zn.copy(),ncod=dict(ncod),orden=list(_ord))\n"
    "        return _m\n"
    "    def _nace(_k,_m):   # H1: NACE UN CUERPO NUEVO. Memoria vacia + lo que `hereda` deje pasar. rng propio (ERR-60). El mundo (objs, tipos, val) NO se toca\n"
    "        nonlocal E,Ag,_prev_on,_nbar\n"
    "        if _k>=100000: raise SystemExit('H1: mas de 100000 partos: la semilla del hijo colisionaria (ERR-60)')\n"
    "        _rh=np.random.default_rng(700000+1000000*seed+_k)   # SEM_HIJO(seed,k); no consume el rng DEL MUNDO\n"
    "        Wl[:]=_rh.uniform(.1,.4,(2,9)); el[:]=0; tr[:]=0   # la politica de locomocion NO se hereda en ningun brazo\n"
    "        Wp[:]=0; Wn[:]=0; Wps[:]=0; Wns[:]=0; err[:]=0; mu[:]=0; mup[:]=0; mun[:]=0; zp[:]=0; zn[:]=0\n"
    "        Wpe[:]=0; Wke[:]=0; _sbE[:]=0; ncod.clear(); _ord.clear(); _rech.clear(); _prev_on=-1\n"
    "        if hereda=='M1+pares' and _m is not None and 'KW' in _m:\n"
    "            KW[:]=_m['KW']; activa[:]=_m['activa']   # el TOKEN viaja con los pares: los indices de celda significan lo mismo\n"
    "        else:   # cuerpo nuevo: las mismas cinco lineas del nacimiento del fundador, con el rng DEL HIJO\n"
    "            KW[:]=0; activa[:]=False; KW[:NK]=_rh.uniform(0,1,(NK,6)); activa[:NK]=True\n"
    "            if solap_AB: KW[:solap_AB]=0; KW[:solap_AB,0]=5.0\n"
    "            while not cond(): KW[objetivo_AB:NK]=_rh.uniform(0,1,(NK-objetivo_AB,6))\n"
    "        if _m is not None and 'Wps' in _m:\n"
    "            if hereda=='baraja':\n"
    "                _pm=_rb.permutation(6); _nbar+=int(bool((_pm==np.arange(6)).all()))   # misma magnitud, pixeles equivocados\n"
    "                Wps[:]=_m['Wps'][:,_pm]; Wns[:]=_m['Wns'][:,_pm]\n"
    "            else: Wps[:]=_m['Wps']; Wns[:]=_m['Wns']\n"
    "        if hereda=='M1+pares' and _m is not None and 'KW' in _m:\n"
    "            Wp[:]=_m['Wp']; Wn[:]=_m['Wn']; mu[:]=_m['mu']; err[:]=_m['err']; mup[:]=_m['mup']; mun[:]=_m['mun']\n"
    "            zp[:]=_m['zp']; zn[:]=_m['zn']; ncod.update(_m['ncod']); _ord.extend(_m['orden'])\n"
    "        E=(_m['dote'] if _m is not None else dote); Ag=E   # nace con su dote; el fundador de repuesto la recibe DEL MUNDO (regalo, se cuenta)\n"
    "    for t in range(T):\n")

I_PAGO = (
    "                if h1: _dv+=1   # H1: descendiente del cuerpo EN CURSO (solo lectura; con muerte_real=0 tambien se cuenta)\n"
    "                if muerte_real:   # H1: el padre PAGA la dote del hijo y lo pone en la cola; la memoria se congela AQUI, no en la muerte del padre\n"
    "                    E-=dote; Ag-=dote\n"
    "                    if _esfund and _gv0-_tmu<rep2_regalo: _dfund+=1   # ventana financiada por una fundacion NO pagada (el unico regalo que queda)\n"
    "                    if len(_cola)>=cola_max: _cola.pop(0); _cdes+=1\n"
    "                    _cola.append(_snap())\n")

I_MUERTE = (
    "            if h1:   # H1: se cierra el cuerpo que muere: su vida SIN tope, su origen y sus descendientes (solo lectura)\n"
    "                _svid+=t-_tmu; _vh.append(t-_tmu); _org.append(int(not _esfund)); _dpv.append(_dv); _dv=0\n"
    "            if muerte_real:   # H1: LA MUERTE BORRA AL INDIVIDUO. Nace el siguiente de la cola; si no hay, el linaje SE EXTINGUIO y el mundo pone un FUNDADOR\n"
    "                _nac+=1\n"
    "                _m=(_cola.pop(0) if _cola else None)\n"
    "                _esfund=_m is None\n"
    "                if _esfund:\n"
    "                    _fund+=1\n"
    "                    if len(_tfund)<200: _tfund.append(t)\n"
    "                _nace(_nac,_m)\n")

I_EXT = (
    "    if h1: _ext.update(muerte_real=int(muerte_real),hereda=hereda,dote=dote,nacimientos=_nac,fundadores=_fund,\n"
    "                       desc_fund=_dfund,desc_por_vida=list(_dpv)+[_dv],vidas_h1=list(_vh)+[T-_tmu],origen_cuerpo=list(_org)+[int(not _esfund)],\n"
    "                       suma_vidas=_svid,cola_final=len(_cola),cola_desborde=_cdes,t_fund=list(_tfund),baraja_identidad=_nbar,\n"
    "                       h1=dict(cola_max=cola_max,sem_hijo='700000+1000000*seed+k',sem_baraja='800000+1000000*seed'))   # H1: claves nuevas SOLO con h1=1\n")

CAB = '''"""organismo_vivo_h1 = organismo_vivo_rep2.py (96feb4918dc5d694; aqui solo se LEYO; cadena: organismo_vivo_rep
aa823d56c2d4213c <- organismo_vivo 20c0961c79de8825 <- TRONCO CONGELADO organismo_v14 v14.1 feefc88b1fd8d434) +
LA MUERTE QUE MATA (H-1 de la sala 4; PREREGISTRO_h1_muerte.md). Hoy el renacer conserva Wp, Wn, KW, activa, Wps,
Wns y ncod: el individuo es inmortal en memoria y el renacer REGALA 600 pasos de drenaje (E=Ag=0.6), que financian
el 34-77 % de las ventanas de reproduccion (SALA4 §B E-1).
  muerte_real=0  ->  organismo_vivo_rep2 BIT A BIT (todas las claves, mismo consumo del rng del mundo)
  muerte_real=1  ->  al morir se BORRA la memoria del individuo (valores, codigo activo, tabla, predictor, trazas,
                     locomocion) y el cuerpo siguiente nace VACIO, con rng propio SEM_HIJO(seed,k)=700000+1000000*seed+k
                     (ERR-60: la formula literal del encargo colisionaba entre semillas vecinas) y con la DOTE que
                     su padre pago al cerrarse la ventana. Si no hay descendiente en la cola, el linaje se EXTINGUIO
                     y el mundo pone un fundador: se cuenta (`fundadores`).
  hereda = 'nada' | 'M1' (el VECTOR: Wps/Wns sobre la retina) | 'M1+pares' (el vector Y el TOKEN: KW/activa + los
                     pares codigo<->valor) | 'baraja' (M1 con los 6 pixeles permutados: la prediccion que decide).
ANCLA DE IDENTIDAD: muerte_real=0 y h1=0 -> organismo_vivo_rep2 bit a bit; h1=1 -> claves viejas bit a bit + 13
nuevas; reproduccion=0 -> todo H-1 inerte. Arnes: identidad_vivo_h1.py. Generado por construye_vivo_h1.py. NO editar a mano."""
'''

RNG_MUNDO = re.compile(r'(?<![_A-Za-z0-9])rng\s*\.')   # el rng DEL MUNDO: `rng.uniform`, `rng.integers`, `rng.random`, ...


if __name__ == '__main__':
    origen(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), SHA_V14)
    origen(os.path.join(AQUI, 'organismo_vivo.py'), SHA_VIVO)
    origen(os.path.join(AQUI, 'organismo_vivo_rep.py'), SHA_REP)
    s = origen(os.path.join(AQUI, 'organismo_vivo_rep2.py'), SHA_REP2)

    s = sust(s, A_FIRMA, I_FIRMA, etiqueta='firma: perillas de H-1')
    s = sust(s, A_MAESTRA, A_MAESTRA + I_MAESTRA, etiqueta='guardias de H-1')
    s = sust(s, A_ESTADO, A_ESTADO + I_ESTADO, etiqueta='estado de H-1 (cola, fundaciones, rng del barajado)')
    s = sust(s, A_BUCLE, I_BUCLE, etiqueta='_snap y _nace (el parto) antes del bucle')
    s = sust(s, A_PAGO, A_PAGO + I_PAGO, etiqueta='el padre paga la dote y encola al hijo')
    # OJO: el bloque de H-1 va ANTES del de rep2, porque rep2 pisa `_tmu` con el paso actual y `_svid` necesita la marca vieja
    s = sust(s, A_MUERTE, I_MUERTE + A_MUERTE, etiqueta='la muerte borra al individuo')
    s = sust(s, A_EXT, A_EXT + I_EXT, etiqueta='claves de H-1')

    malas = [x for x in NUEVO if RNG_MUNDO.search(x)]
    if malas:
        raise SystemExit("Una insercion consume el rng DEL MUNDO: " + repr(malas[:2]))
    d = os.path.join(AQUI, 'organismo_vivo_h1.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(CAB + s)
    print(f"  escrito {d}")
    print(f"  sha organismo_v14.py (tronco, solo lectura)       {SHA_V14}")
    print(f"  sha organismo_vivo.py (solo lectura)              {SHA_VIVO}")
    print(f"  sha organismo_vivo_rep.py (solo lectura)          {SHA_REP}")
    print(f"  sha organismo_vivo_rep2.py (origen, solo lectura) {SHA_REP2}")
    print(f"  sha organismo_vivo_h1.py                          {h16(d)}")
    print(f"  sha construye_vivo_h1.py                          {h16(os.path.abspath(__file__))}")
    print(f"  inserciones: {len(NUEVO)}; ninguna consume el rng del mundo.")
    print("  siguiente: python experimentos/nivel11_mundo_vivo/identidad_vivo_h1.py")
