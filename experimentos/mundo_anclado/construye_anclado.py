"""construye_anclado.py -- genera organismo_anclado.py POR ANCLAS desde
experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py (sha 9dd1fb91ecec35ae; SOLO SE LEE, no se edita).

MISION: llegar a la AGI por este camino. MUNDO ANCLADO (decision del director, 22-sep): un mundo donde la
ignorancia no sostiene un linaje y el conocimiento perfecto si. El CUERPO no se toca: todas las inserciones
son del MUNDO (reglas de los objetos) o de SOLO LECTURA.

PERILLA DEL MUNDO (b) -- DILUCION POR TIPO (quimiostato):
  olv_mal = h  ->  en cada paso, CADA objeto MALO presente (el que no mejora ninguna necesidad y empeora alguna,
                   leido de la tabla del mundo _EF[val[tipo]]: hoy B y D) desaparece con probabilidad h, sorteada
                   con un rng PROPIO (890000+1000000*seed; no toca el del mundo, ni el de los hijos 700000+, ni
                   800000/850000/860000/870000, ni seed+900000). El hueco lo repone spawn() como siempre
                   (UNIFORME, rng del mundo). Es POR OBJETO: escala sola con nobj y con cualquier tabla de tipos.
  olv_ciego=1  ->  PLACEBO de la perilla: MISMOS sorteos (uno por objeto malo, misma h, mismo rng propio) =
                   MISMO numero de desapariciones en ese estado del mundo, pero cada desaparicion se lleva un
                   objeto AL AZAR (cualquier tipo). Misma dosis, sin informacion de tipo.
  anc_mide=1   ->  SOLO LECTURA: presencia por tipo integrada en el tiempo y desapariciones. Clave 'anclado'.
La otra perilla admitida (c, rep_acum) YA EXISTE en organismo_f9c (F9) y no se reescribe.

ANCLA DE IDENTIDAD: olv_mal=0 y anc_mide=0 -> organismo_f9c BIT A BIT (mismo dict, igualdad exacta);
anc_mide=1 -> claves viejas bit a bit + UNA clave nueva 'anclado'. Arnes: identidad_anclado.py.
"""
import hashlib
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2', 'organismo_f9c.py')
DESTINO = os.path.join(AQUI, 'organismo_anclado.py')
SHA_ORIGEN_ESPERADO = '9dd1fb91ecec35ae'


def h16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def ancla(src, viejo, nuevo, etiqueta, veces=1):
    n = src.count(viejo)
    if n != veces:
        raise SystemExit(f"ANCLA ROTA ({etiqueta}): esperaba {veces}, encontre {n}.\n{viejo!r}")
    return src.replace(viejo, nuevo)


def construir():
    raw = open(ORIGEN, 'rb').read()
    sha = h16(raw)
    if sha != SHA_ORIGEN_ESPERADO:
        raise SystemExit(f"SHA de origen cambio: {sha} != {SHA_ORIGEN_ESPERADO}. NO se construye nada.")
    src = raw.decode('utf-8').replace('\r\n', '\n')

    # (1) firma: tres perillas nuevas AL FINAL, apagadas por defecto
    src = ancla(src, "sesgo_fijo=0.0,f9c=0):\n",
                "sesgo_fijo=0.0,f9c=0,olv_mal=0.0,olv_ciego=0,anc_mide=0):\n", 'firma')

    # (2) guardias + rng propio + contadores, justo tras el rng del mundo (crear un Generator no consume el del mundo)
    src = ancla(src, "    rng=np.random.default_rng(seed)\n",
                "    rng=np.random.default_rng(seed)\n"
                "    if not (0.0<=olv_mal<1.0): raise SystemExit('ANCLADO: olv_mal es una probabilidad POR OBJETO Y POR PASO en [0,1)')\n"
                "    if olv_ciego not in (0,1): raise SystemExit('ANCLADO: olv_ciego es 0 o 1')\n"
                "    if olv_ciego and not olv_mal: raise SystemExit('ANCLADO: olv_ciego (placebo) exige olv_mal>0 (misma dosis)')\n"
                "    _rolv=np.random.default_rng(890000+1000000*seed) if olv_mal else None   # ANCLADO: rng PROPIO de la dilucion (ERR-60)\n"
                "    _anc_ev=0; _anc_rem={}; _anc_pres={}; _anc_pasos=0   # ANCLADO: sorteos que dispararon, desapariciones por tipo, presencia por tipo. SOLO LECTURA\n",
                'rng propio')

    # (3) la dilucion por tipo y la medida de presencia, justo DESPUES del olvido original (que queda intacto)
    viejo3 = ("            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido\n")
    nuevo3 = (viejo3 +
              "        if olv_mal:   # ANCLADO (quimiostato): cada objeto MALO se diluye con prob olv_mal (rng propio); spawn() repone UNIFORME\n"
              "            _fire=[_xo for _xo in list(objs) if (min(_EF[val[objs[_xo]]])<0 and max(_EF[val[objs[_xo]]])<=0) and _rolv.random()<olv_mal]\n"
              "            if olv_ciego and _fire:   # PLACEBO: mismo numero de desapariciones, objeto AL AZAR (cualquier tipo)\n"
              "                _pool=list(objs); _fire=[_pool.pop(int(_rolv.integers(len(_pool)))) for _ in range(len(_fire))]\n"
              "            for _xo in _fire:\n"
              "                _anc_ev+=1; _anc_rem[objs[_xo]]=_anc_rem.get(objs[_xo],0)+1; del objs[_xo]; _rech.pop(_xo,None)\n"
              "            if _fire: spawn()\n"
              "        if anc_mide:   # ANCLADO: composicion del mundo al cerrar el paso (SOLO LECTURA)\n"
              "            _anc_pasos+=1\n"
              "            for _vo in objs.values(): _anc_pres[_vo]=_anc_pres.get(_vo,0)+1\n")
    src = ancla(src, viejo3, nuevo3, 'dilucion')

    # (4) el return agrega UNA clave, solo con alguna perilla nueva encendida
    viejo4 = ",Wns=[round(float(x),3) for x in Wns[_nm]],**_ext)"
    nuevo4 = (",Wns=[round(float(x),3) for x in Wns[_nm]],**_ext,"
              "**({'anclado':dict(olv_mal=float(olv_mal),olv_ciego=int(olv_ciego),eventos=int(_anc_ev),rem=dict(_anc_rem),"
              "pres=dict(_anc_pres),pasos=int(_anc_pasos),nobj=int(nobj),sem_olv='890000+1000000*seed')} "
              "if (olv_mal or anc_mide) else {}))")
    src = ancla(src, viejo4, nuevo4, 'return')

    cab = ('"""organismo_anclado.py -- GENERADO POR experimentos/mundo_anclado/construye_anclado.py DESDE\n'
           f'experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py (sha {SHA_ORIGEN_ESPERADO}, SOLO SE LEYO). NO EDITAR A MANO.\n'
           'MUNDO ANCLADO: olv_mal (dilucion POR OBJETO de lo malo, rng propio), olv_ciego (placebo: misma dosis, objeto al\n'
           'azar), anc_mide (presencia por tipo, solo lectura). Con olv_mal=0 y anc_mide=0 es organismo_f9c BIT A BIT.\n'
           'El CUERPO no se toca. Arnes: identidad_anclado.py."""\n')
    out = cab + src
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
    print(f"OK {DESTINO}\n  sha origen  {sha}\n  sha destino {h16(out.encode('utf-8'))}")


if __name__ == '__main__':
    construir()
