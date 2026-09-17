"""Genera los instrumentos de la re-verificacion sobre v13 (PREREGISTRO_reverificacion_v13.md):
  mundo_temporal_v13.py <- experimentos/v11_generaliza/mundo_temporal_v11.py (807f4b357f9eac1a) + via lenta sobre la
                           entrada completa (NIN dims) + puerta de familiaridad. Con eta_s=0, puerta=None es v11 exacto.
  organismo_capD13.py   <- experimentos/capacidad_grande/organismo_capD.py (85afad3f0769891f) + via lenta sobre los D
                           pixeles + puerta. Con eta_s=0, puerta=None es capD exacto.
Mismas reglas que organismo_v13 (tronco): cada via su error; la boca consulta la rapida solo si >= puerta celdas del
codigo tienen |Wp-Wn|>0.2; si no, la lenta. Anclas con conteo exacto; origenes por sha.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))


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


def temporal():
    s = origen(os.path.join(RAIZ, 'experimentos', 'v11_generaliza', 'mundo_temporal_v11.py'), '807f4b357f9eac1a')
    s = sust(s, "lam=0.05, memoria_rechazo=20, mu_norm=False, div_signo=False):",
             "lam=0.05, memoria_rechazo=20, mu_norm=False, div_signo=False, eta_s=0.0, clip_s=3.0, puerta=None):", etiqueta='firma')
    s = sust(s, "    Wp = np.zeros(nkmax); Wn = np.zeros(nkmax)\n",
             "    Wp = np.zeros(nkmax); Wn = np.zeros(nkmax)\n"
             "    Wps = np.zeros(NIN); Wns = np.zeros(NIN)   # v13: via LENTA lineal sobre la entrada completa (inerte si eta_s=0)\n"
             "    def valor(P):   # v13: valor que usa la boca: suma (sin puerta) o la rapida si el patron le es familiar, si no la lenta\n"
             "        _k = kenyon(P); _f = float((Wp - Wn) @ _k); _s = float((Wps - Wns) @ P)\n"
             "        return _f + _s if puerta is None else (_f if int((np.abs((Wp - Wn)[_k > 0]) > 0.2).sum()) >= puerta else _s)\n",
             etiqueta='estado lenta')
    s = sust(s, "                    W={f'{c}|{p}': round(float((Wp - Wn) @ kenyon(inp(c, p))), 3) for c, p in SIT})\n",
             "                    W={f'{c}|{p}': round(valor(inp(c, p)), 3) for c, p in SIT})   # v13: valor total\n", etiqueta='snapshot W')
    s = sust(s, "            P = inp(kk, prev_sent); kc = kenyon(P); Wb = Wp - Wn\n"
                "            Vb = alpha * (Wb @ kc) + hambre_boca * hambre + .5\n",
             "            P = inp(kk, prev_sent); kc = kenyon(P); Wb = Wp - Wn; _wf = float(Wb @ kc); _ws = float((Wps - Wns) @ P)   # v13\n"
             "            _wt = _wf + _ws if puerta is None else (_wf if int((np.abs(Wb[kc > 0]) > 0.2).sum()) >= puerta else _ws)   # v13\n"
             "            Vb = alpha * _wt + hambre_boca * hambre + .5\n", etiqueta='boca')
    s = sust(s, "                    dlt = R - Wb @ kc\n",
             "                    dlt = R - _wt if puerta is None else R - _wf   # v13: sin puerta un error compartido; con puerta cada via el suyo\n"
             "                    if eta_s:   # v13: via lenta\n"
             "                        _ds = dlt if puerta is None else R - _ws\n"
             "                        if lam: _mcs = np.minimum(Wps, Wns) * (P > 0); Wps = Wps - lam * _mcs; Wns = Wns - lam * _mcs\n"
             "                        if _ds > 0: Wps = np.clip(Wps + eta_s * _ds * P, 0, clip_s)\n"
             "                        else:       Wns = np.clip(Wns + eta_s * aversion * (-_ds) * P, 0, clip_s)\n", etiqueta='error')
    cab = ('"""mundo_temporal_v13 = mundo_temporal_v11.py (807f4b357f9eac1a) + via lenta lineal sobre la entrada completa + puerta\n'
           'de familiaridad (las reglas de organismo_v13). Generado por construye_reverificacion_v13.py. NO editar.\n'
           'Con eta_s=0 y puerta=None es mundo_temporal_v11 exacto (control de inercia)."""\n')
    d = os.path.join(AQUI, 'mundo_temporal_v13.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    return d


def capD13():
    s = origen(os.path.join(RAIZ, 'experimentos', 'capacidad_grande', 'organismo_capD.py'), '85afad3f0769891f')
    s = sust(s, "paso=0.5,lam=0.0,memoria_rechazo=20,mu_norm=False,div_signo=False):",
             "paso=0.5,lam=0.0,memoria_rechazo=20,mu_norm=False,div_signo=False,eta_s=0.0,clip_s=3.0,puerta=None):", etiqueta='firma')
    ancla = "mu=np.zeros((NKMAX,D)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(D+3)\n"
    s = sust(s, ancla, ancla +
             "    Wps=np.zeros(D); Wns=np.zeros(D)   # v13: via LENTA lineal sobre la retina (inerte si eta_s=0)\n"
             "    def valor(P):   # v13\n"
             "        _k=kenyon(P); _f=float((Wp-Wn)@_k); _s=float((Wps-Wns)@P)\n"
             "        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)\n"
             "    def nofam(P): return int((np.abs((Wp-Wn)[kenyon(P)>0])>0.2).sum())<3   # v13: lectura\n", etiqueta='estado lenta')
    s = sust(s, "            W={n:round(float(Wb@kenyon(pats[n])),3) for n in vivos},\n",
             "            W={n:round(valor(pats[n]),3) for n in vivos},   # v13: valor total\n", etiqueta='foto W')
    s = sust(s, "            kk=objs[pos]; kc=kenyon(pats[kk]); Wb=Wp-Wn\n"
                "            Vb=alpha*(Wb@kc)+hambre_boca*hambre+.5;",
             "            kk=objs[pos]; kc=kenyon(pats[kk]); Wb=Wp-Wn; _wf=float(Wb@kc); _ws=float((Wps-Wns)@pats[kk])   # v13\n"
             "            _wt=_wf+_ws if puerta is None else (_wf if int((np.abs(Wb[kc>0])>0.2).sum())>=puerta else _ws)   # v13\n"
             "            Vb=alpha*_wt+hambre_boca*hambre+.5;", etiqueta='boca')
    s = sust(s, "                    dlt=R-Wb@kc\n",
             "                    dlt=R-_wt if puerta is None else R-_wf   # v13\n"
             "                    if eta_s:   # v13: via lenta\n"
             "                        _ds=dlt if puerta is None else R-_ws\n"
             "                        if lam: _mcs=np.minimum(Wps,Wns)*(pats[kk]>0); Wps=Wps-lam*_mcs; Wns=Wns-lam*_mcs\n"
             "                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*pats[kk],0,clip_s)\n"
             "                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*pats[kk],0,clip_s)\n", etiqueta='error')
    s = sust(s, "    W={k:round(float((Wp-Wn)@kenyon(pats[k])),2) for k in pats}\n",
             "    W={k:round(valor(pats[k]),2) for k in pats}   # v13: valor total\n"
             "    nofam_fin=sum(nofam(pats[n]) for n in tipos)   # v13: estimulos vivos que la puerta manda a la lenta al final\n", etiqueta='W final')
    s = sust(s, "n_techo=n_techo,mv_tot=mv_tot,mc_tot=mc_tot)", "n_techo=n_techo,mv_tot=mv_tot,mc_tot=mc_tot,nofam_fin=nofam_fin)", etiqueta='return')
    cab = ('"""organismo_capD13 = organismo_capD.py (85afad3f0769891f) + via lenta lineal sobre la retina + puerta de familiaridad\n'
           '(las reglas de organismo_v13). Generado por construye_reverificacion_v13.py. NO editar.\n'
           'Con eta_s=0 y puerta=None es organismo_capD exacto (control de inercia)."""\n')
    d = os.path.join(AQUI, 'organismo_capD13.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    return d


if __name__ == '__main__':
    for f in (temporal, capD13):
        d = f()
        print(f"  {os.path.relpath(d, RAIZ):52s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
