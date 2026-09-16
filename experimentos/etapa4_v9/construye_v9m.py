"""Genera experimentos/etapa4_v9/organismo_v9m.py desde organismo/organismo_v9.py (congelado, d3b72fb8819fbe8e).

Preregistro: PREREGISTRO_etapa4_v9.md, commiteado ANTES que este script. Anclas con conteo exacto; origen por sha.
Todo apagado por defecto -> v9 exacto (ninguna llamada nueva al RNG si fases=None).
  fases={t: (tipos, valencias)}   cambio del conjunto de estimulos en t (retira los objetos de tipos ausentes y repone),
                                  con sonda de W de A,B,C,D en ese instante.
  congelar=(t0,t1)                sin aprendizaje (boca, canales, divisiones, patas) en [t0,t1).
  estado_inicial, heredar_patas   la cria arranca con copia de KW, activa, Wp, Wn, err, mu (+ Wl si heredar_patas).
  devolver_estado                 devuelve ese estado al final.
  Lectura: muertes por cuarto (dq); primer encuentro con cada estimulo tras cada cambio de fase.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'organismo', 'organismo_v9.py')
SHA_ORIGEN = 'd3b72fb8819fbe8e'
DESTINO = os.path.join(AQUI, 'organismo_v9m.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN: sha {h16(ORIGEN)}, se esperaba {SHA_ORIGEN}. Abortado.")
    s = open(ORIGEN, encoding='utf-8').read()
    s = sust(s, "lam=0.05,memoria_rechazo=20):",
             "lam=0.05,memoria_rechazo=20,fases=None,congelar=None,estado_inicial=None,heredar_patas=True,devolver_estado=False):",
             etiqueta='firma')
    ancla = ("    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; "
             "el=np.zeros_like(Wl); tr=np.zeros(9)\n")
    s = sust(s, ancla, ancla +
        "    if estado_inicial is not None:   # v9m: herencia (copias; los contadores empiezan en cero)\n"
        "        KW[:]=estado_inicial['KW']; activa[:]=estado_inicial['activa']; Wp[:]=estado_inicial['Wp']; Wn[:]=estado_inicial['Wn']\n"
        "        err[:]=estado_inicial['err']; mu[:]=estado_inicial['mu']\n"
        "        if heredar_patas: Wl[:]=estado_inicial['Wl']\n"
        "    sondas={}; primer={}; _t_fase=0; dq=[0]*4   # v9m: lectura\n", etiqueta='herencia')
    ancla = "        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val\n"
    s = sust(s, ancla, ancla +
        "        if fases is not None and t in fases:   # v9m: cambio del conjunto de estimulos\n"
        "            tipos[:]=list(fases[t][0]); val.update(fases[t][1]); _t_fase=t\n"
        "            for _x in [_xx for _xx,_kz in list(objs.items()) if _kz not in tipos]: del objs[_x]; _rech.pop(_x,None)\n"
        "            spawn(); sondas[t]={_k:float((Wp-Wn)@kenyon(PAT[_k])) for _k in PAT}\n"
        "        _ap=learn and not (congelar is not None and congelar[0]<=t<congelar[1])   # v9m\n", etiqueta='fases')
    s = sust(s, "if learn:", "if _ap:", n=3, etiqueta='compuerta de aprendizaje')
    ancla = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
    s = sust(s, ancla, ancla +
        "            if (_t_fase,kk) not in primer: primer[(_t_fase,kk)]=dict(t=t,W=float(Wb@kc),pb=float(pb),mordio=bool(mordio))   # v9m\n",
        etiqueta='primer encuentro')
    s = sust(s, "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))\n",
             "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L)); dq[q(t)]+=1\n", etiqueta='muertes por cuarto')
    s = sust(s, "if nuevo else None})",
             "if nuevo else None},sondas=sondas,primer={f'{_a}|{_b}':_v for (_a,_b),_v in primer.items()},dq=dq,"
             "estado=(dict(KW=KW.copy(),activa=activa.copy(),Wp=Wp.copy(),Wn=Wn.copy(),err=err.copy(),mu=mu.copy(),Wl=Wl.copy()) "
             "if devolver_estado else None))", etiqueta='return')
    cab = ('"""organismo_v9m = organismo/organismo_v9.py (d3b72fb8819fbe8e) + fases de mundo, congelar aprendizaje, herencia de\n'
           'estado y lectura de primer encuentro y muertes por cuarto. Generado por construye_v9m.py. NO editar.\n'
           'Con los valores por defecto es v9 exacto. Preregistro: experimentos/etapa4_v9/PREREGISTRO_etapa4_v9.md\n'
           '"""\n')
    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(cab + s)
    print(f"  organismo_v9m.py  {h16(DESTINO)}  {sum(1 for _ in open(DESTINO, encoding='utf-8'))} lineas")
