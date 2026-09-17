"""Genera los instrumentos para re-verificar Etapa 3 (generalizacion) y 3T (composicion temporal) sobre v11.

  organismo_v11g.py      <- organismo/organismo_v11.py (f69e24063be1b194) + mundo de regla, sonda a priori,
                            primer encuentro y sonda final de 64 patrones. MISMAS anclas que
                            experimentos/etapa3_v9/construye_v9g.py (5a2af... ver ese archivo), aplicadas a v11.
                            Con mundo='AB' es v11 exacto; con mu_norm=False y div_signo=False debe ser v9g exacto.
  mundo_temporal_v11.py  <- experimentos/v9_reverificacion/mundo_temporal_v9.py (18d96a1c79863bb0) + mu_norm + div_signo
                            (ambos False por defecto = mundo_temporal_v9 exacto, control KT1).

Preregistro: PREREGISTRO_v11_generaliza.md. Anclas con conteo exacto; origenes por sha.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))

HELPERS = open(os.path.join(RAIZ, 'experimentos', 'etapa3_v9', 'construye_v9g.py'), encoding='utf-8').read()
HELPERS = HELPERS.split("HELPERS = '''", 1)[1].split("'''", 1)[0]


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


def v11g():
    """Mismas anclas que construye_v9g.py, sobre organismo_v11.py."""
    src = origen(os.path.join(RAIZ, 'organismo', 'organismo_v11.py'), 'f69e24063be1b194')
    cab, cuerpo = src.split("def run(", 1)
    cuerpo = "def run(" + cuerpo
    cab = cab + HELPERS.lstrip('\n')
    n_pat = cuerpo.count("PAT")
    if n_pat != 21:
        raise SystemExit(f"PAT aparece {n_pat} veces en run(), se esperaban 21 (como en v9g). Abortado.")
    cuerpo = cuerpo.replace("PAT", "P_")
    cuerpo = sust(cuerpo, "lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True):",
                  "lam=0.05,memoria_rechazo=20,mu_norm=True,div_signo=True,mundo='AB',regla='px0',fase2_en=None,sonda_final=False):",
                  etiqueta='firma')
    ancla = "    rng=np.random.default_rng(seed)\n"
    cuerpo = sust(cuerpo, ancla,
        "    if mundo=='AB': P_=PAT; tren=['A','B']; test=[]   # v11g: con 'AB' es v11 exacto\n"
        "    else: P_,tren,test,val_regla=split_regla(seed,regla); fase2_en=T//2 if fase2_en is None else fase2_en\n" + ancla,
        etiqueta='mundo')
    cuerpo = sust(cuerpo, "    while not cond(): KW[objetivo_AB:NK]=", "    while mundo=='AB' and not cond(): KW[objetivo_AB:NK]=",
                  etiqueta='rechazo solo en AB')
    cuerpo = sust(cuerpo, "pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}\n",
                  "pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'} if mundo=='AB' else dict(val_regla)\n", etiqueta='val')
    cuerpo = sust(cuerpo, "    tipos=['A','B']\n",
                  "    tipos=['A','B'] if mundo=='AB' else list(tren)\n"
                  "    W_apriori=None; codigos_f2=None; primer={}   # v11g: sonda y primer encuentro (lectura)\n", etiqueta='tipos')
    ancla = "        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val\n"
    cuerpo = sust(cuerpo, ancla, ancla +
        "        if mundo!='AB' and t==fase2_en:   # v11g: sonda a priori ANTES de que existan los de test, y entrada\n"
        "            _Wb=Wp-Wn; W_apriori={_k:float(_Wb@kenyon(P_[_k])) for _k in P_}\n"
        "            codigos_f2={_k:sorted(int(_i) for _i in code(P_[_k])) for _k in P_}\n"
        "            tipos.extend(test); primer={_k:None for _k in test}\n", etiqueta='fase 2')
    ancla = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
    cuerpo = sust(cuerpo, ancla, ancla +
        "            if kk in primer and primer[kk] is None: primer[kk]=dict(t=t,W=float(Wb@kc),pb=float(pb),hambre=float(hambre),mordio=bool(mordio))   # v11g\n",
        etiqueta='primer encuentro')
    ancla = "    W={k:round(float((Wp-Wn)@kenyon(P_[k])),2) for k in P_}\n"
    cuerpo = sust(cuerpo, ancla,
        "    _sonda=None; _cod_fin=None\n"
        "    if sonda_final:   # v11g: W y codigo de los 64 patrones al final (lectura)\n"
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
    cabecera = ('"""organismo_v11g = organismo/organismo_v11.py (f69e24063be1b194) + mundo de regla (20 patrones de peso 3) +\n'
                'sonda a priori + primer encuentro + sonda final de 64 patrones. MISMAS anclas que organismo_v9g.\n'
                "Generado por construye_v11_generaliza.py. NO editar. Con mundo='AB' es v11 exacto; con mu_norm=False y\n"
                'div_signo=False es organismo_v9g exacto (control de identidad).\n'
                '"""\n')
    d = os.path.join(AQUI, 'organismo_v11g.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cabecera + cab + cuerpo)
    return d


def mundo_temporal_v11():
    s = origen(os.path.join(RAIZ, 'experimentos', 'v9_reverificacion', 'mundo_temporal_v9.py'), '18d96a1c79863bb0')
    s = sust(s, "wclip=3.0, lam=0.05, memoria_rechazo=20):", "wclip=3.0, lam=0.05, memoria_rechazo=20, mu_norm=False, div_signo=False):",
             etiqueta='firma')
    viejo = ("                        for c in idx:\n"
             "                            if err[c] > theta and (~activa).any():\n"
             "                                j = int(np.where(~activa)[0][0]); activa[j] = True\n"
             "                                dist = P - mu[c]\n"
             "                                a1 = float(np.abs(dist).sum())\n"
             "                                ft = float(np.abs(dist[6:]).sum()) / a1 if (a1 > 0 and NIN == 12) else 0.0\n"
             "                                KW[j] = np.clip(KW[c] + paso * dist, 0, 5)\n"
             "                                KW[c] = np.clip(KW[c] - paso * dist, 0, 5)\n"
             "                                Wp[j] = Wp[c]; Wn[j] = Wn[c]; mu[j] = mu[c].copy()\n"
             "                                err[c] = err[j] = 0; splits += 1\n"
             "                                split_t.append((t, kk, prev_sent, round(ft, 3)))\n"
             "                                if not (~activa).any() and t_pool is None: t_pool = t\n")
    nuevo = ("                        for c in idx:\n"
             "                            if div_signo:   # v11: conflicto de signo, hija ciega fuera de P, madre fija, fision del valor\n"
             "                                dist = P - (mu[c] * (P.sum() / max(float(mu[c].sum()), 1e-9)) if mu_norm else mu[c])\n"
             "                                kj = np.clip(KW[c] * (1 - 0.05) + paso * dist, 0, 5) * (P > 0)\n"
             "                                if Wb[c] * R < 0 and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(KW[c] @ P) and (~activa).any():\n"
             "                                    a1 = float(np.abs(dist).sum())\n"
             "                                    ft = float(np.abs(dist[6:]).sum()) / a1 if (a1 > 0 and NIN == 12) else 0.0\n"
             "                                    j = int(np.where(~activa)[0][0]); activa[j] = True; KW[j] = kj\n"
             "                                    if R > 0: Wp[j] = Wp[c]; Wn[j] = 0.; Wp[c] = 0.\n"
             "                                    else:     Wn[j] = Wn[c]; Wp[j] = 0.; Wn[c] = 0.\n"
             "                                    mu[j] = P * (float(mu[c].sum()) / P.sum()); err[c] = err[j] = 0; splits += 1\n"
             "                                    split_t.append((t, kk, prev_sent, round(ft, 3)))\n"
             "                                    if not (~activa).any() and t_pool is None: t_pool = t\n"
             "                            elif err[c] > theta and (~activa).any():\n"
             "                                j = int(np.where(~activa)[0][0]); activa[j] = True\n"
             "                                dist = P - (mu[c] * (P.sum() / max(float(mu[c].sum()), 1e-9)) if mu_norm else mu[c])   # v10\n"
             "                                a1 = float(np.abs(dist).sum())\n"
             "                                ft = float(np.abs(dist[6:]).sum()) / a1 if (a1 > 0 and NIN == 12) else 0.0\n"
             "                                KW[j] = np.clip(KW[c] + paso * dist, 0, 5)\n"
             "                                KW[c] = np.clip(KW[c] - paso * dist, 0, 5)\n"
             "                                Wp[j] = Wp[c]; Wn[j] = Wn[c]; mu[j] = mu[c].copy()\n"
             "                                err[c] = err[j] = 0; splits += 1\n"
             "                                split_t.append((t, kk, prev_sent, round(ft, 3)))\n"
             "                                if not (~activa).any() and t_pool is None: t_pool = t\n")
    s = sust(s, viejo, nuevo, etiqueta='bloque de division temporal')
    cab = ('"""mundo_temporal_v11 = mundo_temporal_v9.py (18d96a1c79863bb0) + mu_norm (v10) + div_signo (v11).\n'
           'Generado por construye_v11_generaliza.py. NO editar. Con mu_norm=False y div_signo=False es\n'
           'mundo_temporal_v9 exacto (control KT1)."""\n')
    d = os.path.join(AQUI, 'mundo_temporal_v11.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    return d


if __name__ == '__main__':
    for f in (v11g, mundo_temporal_v11):
        d = f()
        print(f"  {os.path.relpath(d, RAIZ):50s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
