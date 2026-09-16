"""Genera experimentos/etapa3_v9/organismo_v9g.py desde organismo/organismo_v9.py (congelado, d3b72fb8819fbe8e).

Preregistro: PREREGISTRO_etapa3_v9.md (sha 5a2af284ee73ae76), commiteado ANTES que este script.
Anclas con conteo exacto; origen comprobado por sha. Con mundo='AB' (defecto) es v9 exacto: ninguna llamada nueva al
RNG principal (las particiones usan RNG propios 10000+semilla y 30000+semilla).

Anade:
  mundo='regla' con regla in {'px0','xor01','azar'}: 20 patrones de peso 3, particion train/test, sin rechazo de KW,
      entrada de los patrones de test en fase2_en (T/2 por defecto).
  Sonda en fase2_en: W a priori y codigo de los 20 patrones.  Primer encuentro de cada patron de test:
      t, W, pb, hambre, mordio.  sonda_final=True (mundo 'AB'): W y codigo de los 64 patrones al final.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'organismo', 'organismo_v9.py')
SHA_ORIGEN = 'd3b72fb8819fbe8e'
DESTINO = os.path.join(AQUI, 'organismo_v9g.py')

HELPERS = '''
import itertools   # v9g


def patrones_regla():
    """v9g: los C(6,3)=20 patrones binarios de 6 px con exactamente 3 px activos."""
    pats = {}
    for combo in itertools.combinations(range(6), 3):
        v = np.zeros(6); v[list(combo)] = 1.
        pats[''.join('1' if v[j] else '0' for j in range(6))] = v
    return pats


def split_regla(seed, regla):
    """v9g: valencias por regla y particion train/test con RNG propios (no tocan el RNG del organismo)."""
    pats = patrones_regla(); nombres = sorted(pats)
    if regla == 'px0':
        vr = {k: ('comida' if k[0] == '1' else 'veneno') for k in nombres}; ntr = (5, 5)
    elif regla == 'xor01':
        vr = {k: ('comida' if k[0] != k[1] else 'veneno') for k in nombres}; ntr = (4, 4)
    elif regla == 'azar':
        r0 = np.random.default_rng(30000 + seed); perm = r0.permutation(len(nombres))
        com = set(nombres[i] for i in perm[:10])
        vr = {k: ('comida' if k in com else 'veneno') for k in nombres}; ntr = (5, 5)
    else:
        raise ValueError(regla)
    food = [k for k in nombres if vr[k] == 'comida']; pois = [k for k in nombres if vr[k] == 'veneno']
    r = np.random.default_rng(10000 + seed); fi = r.permutation(len(food)); pi = r.permutation(len(pois))
    food = [food[i] for i in fi]; pois = [pois[i] for i in pi]
    tren = sorted(food[:ntr[0]] + pois[:ntr[1]]); test = sorted(food[ntr[0]:] + pois[ntr[1]:])
    return pats, tren, test, vr

'''


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
    src = open(ORIGEN, encoding='utf-8').read()

    cab, cuerpo = src.split("def run(", 1)
    cuerpo = "def run(" + cuerpo
    # helpers a nivel de modulo, antes de run()
    cab = cab + HELPERS.lstrip('\n')
    # PAT -> P_ dentro de run(): 21 apariciones exactas
    n_pat = cuerpo.count("PAT")
    if n_pat != 21:
        raise SystemExit(f"PAT aparece {n_pat} veces en run(), se esperaban 21. Abortado.")
    cuerpo = cuerpo.replace("PAT", "P_")

    cuerpo = sust(cuerpo, "lam=0.05,memoria_rechazo=20):",
                  "lam=0.05,memoria_rechazo=20,mundo='AB',regla='px0',fase2_en=None,sonda_final=False):", etiqueta='firma')
    ancla = "    rng=np.random.default_rng(seed)\n"
    cuerpo = sust(cuerpo, ancla,
        "    if mundo=='AB': P_=PAT; tren=['A','B']; test=[]   # v9g: con 'AB' es v9 exacto\n"
        "    else: P_,tren,test,val_regla=split_regla(seed,regla); fase2_en=T//2 if fase2_en is None else fase2_en\n" + ancla,
        etiqueta='mundo')
    cuerpo = sust(cuerpo, "    while not cond(): KW[objetivo_AB:NK]=", "    while mundo=='AB' and not cond(): KW[objetivo_AB:NK]=",
                  etiqueta='rechazo solo en AB')
    cuerpo = sust(cuerpo, "pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}\n",
                  "pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'} if mundo=='AB' else dict(val_regla)\n", etiqueta='val')
    cuerpo = sust(cuerpo, "    tipos=['A','B']\n",
                  "    tipos=['A','B'] if mundo=='AB' else list(tren)\n"
                  "    W_apriori=None; codigos_f2=None; primer={}   # v9g: sonda y primer encuentro (lectura)\n", etiqueta='tipos')
    ancla = "        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val\n"
    cuerpo = sust(cuerpo, ancla, ancla +
        "        if mundo!='AB' and t==fase2_en:   # v9g: sonda a priori ANTES de que existan los de test, y entrada\n"
        "            _Wb=Wp-Wn; W_apriori={_k:float(_Wb@kenyon(P_[_k])) for _k in P_}\n"
        "            codigos_f2={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}\n"
        "            tipos.extend(test); primer={_k:None for _k in test}\n", etiqueta='fase 2')
    ancla = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
    cuerpo = sust(cuerpo, ancla, ancla +
        "            if kk in primer and primer[kk] is None: primer[kk]=dict(t=t,W=float(Wb@kc),pb=float(pb),hambre=float(hambre),mordio=bool(mordio))   # v9g\n",
        etiqueta='primer encuentro')
    ancla = "    W={k:round(float((Wp-Wn)@kenyon(P_[k])),2) for k in P_}\n"
    cuerpo = sust(cuerpo, ancla,
        "    _sonda=None; _cod_fin=None\n"
        "    if sonda_final:   # v9g: W y codigo de los 64 patrones al final (lectura)\n"
        "        _Wb=Wp-Wn; _sonda={}\n"
        "        for _n in range(64):\n"
        "            _P=np.array([(_n>>(5-_j))&1 for _j in range(6)],float); _nm=''.join(str(int(_v)) for _v in _P)\n"
        "            _sonda[_nm]=dict(W=float(_Wb@kenyon(_P)),codigo=sorted(int(_i) for _i in code(_P)))\n"
        "        _cod_fin={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}\n" + ancla, etiqueta='sonda final')
    cuerpo = sust(cuerpo, "                solap={'AB':", "                solap=None if mundo!='AB' else {'AB':", etiqueta='solap')
    cuerpo = sust(cuerpo, "if nuevo else None})",
                  "if nuevo else None},mundo=mundo,regla=regla,tren=tren,test=test,W_apriori=W_apriori,codigos_f2=codigos_f2,"
                  "primer=primer,W_final=({_k:float((Wp-Wn)@kenyon(P_[_k])) for _k in P_} if mundo!='AB' else None),"
                  "sonda=_sonda,codigos_fin=_cod_fin)", etiqueta='return')

    cabecera = ('"""organismo_v9g = organismo/organismo_v9.py (d3b72fb8819fbe8e) + mundo de regla (20 patrones de peso 3) +\n'
                'sonda a priori + primer encuentro + sonda final de 64 patrones. Generado por construye_v9g.py. NO editar.\n'
                "Con mundo='AB' es v9 exacto (control K). Preregistro: experimentos/etapa3_v9/PREREGISTRO_etapa3_v9.md\n"
                '"""\n')
    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(cabecera + cab + cuerpo)
    print(f"  organismo_v9g.py  {h16(DESTINO)}  {sum(1 for _ in open(DESTINO, encoding='utf-8'))} lineas")
