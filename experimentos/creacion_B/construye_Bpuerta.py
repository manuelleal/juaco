"""CREADOR B — frente 3: PUERTA POR EVIDENCIA DEL CODIGO EXACTO (en vez de por celdas consolidadas).

Genera experimentos/creacion_B/organismo_capB.py = organismo_capD13.py (fd8e10435801646c) con:
  (a) ncod: un contador de mordidas por CODIGO EXACTO (clave = el conjunto de las K celdas activas).
      Coste de memoria: un entero por codigo visto (<= un entero por estimulo aprendido), nada por celda.
  (b) perilla puerta_pat: con puerta_pat>0 la boca consulta la via RAPIDA si el codigo exacto ya fue mordido
      >= puerta_pat veces; con puerta_pat=0 rige la puerta de v13 (>= `puerta` celdas con |Wp-Wn|>0.2): EXACTO.
  (c) diagnostico: nofam_est (que estimulos manda la puerta a la lenta, con la puerta vigente) y ncod_est
      (evidencia acumulada del codigo de cada estimulo).

Por que deberia funcionar: la puerta de v13 mezcla DOS cosas distintas — "he visto esto" y "he aprendido cuanto
vale". Un estimulo mordido cien veces cuyo valor quedo repartido o fisionado entre celdas (|Wp-Wn| <= 0.2 en dos de
sus tres celdas) es declarado DESCONOCIDO y va a la via lenta, que sabe la regla pero no el caso: ahi se paga la
capacidad (v13 35/60 contra v11 50/60). Contar el codigo exacto separa las dos cosas: lo nunca visto sigue yendo a
la lenta (generalizacion intacta, porque un codigo nuevo tiene evidencia 0) y lo ya visto vuelve a la rapida aunque
su valor este repartido (capacidad recuperada).

Anclas con conteo exacto; origen por sha. NO edita originales.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'v13_reverificacion', 'organismo_capD13.py')
SHA_ORIGEN = 'fd8e10435801646c'


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

    s = sust(s, ",eta_s=0.0,clip_s=3.0,puerta=None):", ",eta_s=0.0,clip_s=3.0,puerta=None,puerta_pat=0):", etiqueta='firma')

    s = sust(s, "    Wps=np.zeros(D); Wns=np.zeros(D)   # v13: via LENTA lineal sobre la retina (inerte si eta_s=0)\n",
             "    Wps=np.zeros(D); Wns=np.zeros(D)   # v13: via LENTA lineal sobre la retina (inerte si eta_s=0)\n"
             "    ncod={}   # B: evidencia del CODIGO EXACTO (mordidas por codigo); un entero por codigo visto\n"
             "    def _fam(_k):   # B: la puerta. puerta_pat>0 -> evidencia del codigo exacto; si no, celdas consolidadas (v13 EXACTO)\n"
             "        if puerta_pat: return ncod.get(frozenset(np.flatnonzero(_k).tolist()),0)>=puerta_pat\n"
             "        return int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta\n", etiqueta='estado puerta')

    s = sust(s, "        return _f+_s if puerta is None else (_f if int((np.abs((Wp-Wn)[_k>0])>0.2).sum())>=puerta else _s)\n",
             "        return _f+_s if puerta is None else (_f if _fam(_k) else _s)\n", etiqueta='valor_tot')

    s = sust(s, "            _wt=_wf+_ws if puerta is None else (_wf if int((np.abs(Wb[kc>0])>0.2).sum())>=puerta else _ws)   # v13\n",
             "            _wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)   # v13\n", etiqueta='boca')

    s = sust(s, "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1; morc[kk]+=1\n",
             "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1; morc[kk]+=1\n"
             "                _ky=frozenset(np.flatnonzero(kc).tolist()); ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto\n",
             etiqueta='contador de codigo')

    s = sust(s, "    nofam_fin=sum(nofam(pats[n]) for n in tipos)   # v13: estimulos vivos que la puerta manda a la lenta al final\n",
             "    nofam_fin=sum(nofam(pats[n]) for n in tipos)   # v13: estimulos vivos que la puerta manda a la lenta al final\n"
             "    nofam_est={n:(0 if (puerta is None or _fam(kenyon(pats[n]))) else 1) for n in tipos}   # B: 1 = la puerta VIGENTE lo manda a la lenta\n"
             "    ncod_est={n:int(ncod.get(frozenset(np.flatnonzero(kenyon(pats[n])).tolist()),0)) for n in tipos}   # B: evidencia por estimulo\n",
             etiqueta='diagnostico por estimulo')

    s = sust(s, "mv_tot=mv_tot,mc_tot=mc_tot,nofam_fin=nofam_fin)",
             "mv_tot=mv_tot,mc_tot=mc_tot,nofam_fin=nofam_fin,nofam_est=nofam_est,ncod_est=ncod_est,puerta_pat=puerta_pat)",
             etiqueta='salida')

    cab = ('"""organismo_capB = organismo_capD13.py (fd8e10435801646c) + contador de evidencia por CODIGO EXACTO y\n'
           'perilla puerta_pat (puerta de familiaridad por patron). Generado por construye_Bpuerta.py. NO editar.\n'
           'Con puerta_pat=0 es organismo_capD13 EXACTO (arnes: experimentos/creacion_B/identidad_Bpuerta.py)."""\n')
    d = os.path.join(AQUI, 'organismo_capB.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):50s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
