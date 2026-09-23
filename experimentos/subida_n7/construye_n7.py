"""construye_n7.py -- genera mundo_n7.py POR ANCLAS desde
experimentos/nivel10_composicion_v14/mundo_composicion_v14.py (a9098933b1950e3d; instrumento YA CORRIDO, solo se lee).

Dos perillas nuevas, las dos APAGADAS por defecto (con las dos en 0 mundo_n7 == mundo_composicion_v14 BIT A BIT;
arnes: identidad_n7.py):

  desambiguar (B-5 del tronco v14.2): la division por conflicto de signo se dispara TAMBIEN cuando una celda
      consolidada (|Wb|>0.2), bajo una retina distinta (kj@P > KW[c]@P), recibe R == 0; la hija nace sin valor y
      la madre conserva el suyo. Linea transcrita de organismo/organismo_v142.py (17528d767fcebaf6, CONGELADO).
      En 3T-k B es NEUTRO (R = 0): aqui B-5 NO es inerte (en los mundos del tronco R in {+1,-3} y si lo es).
  norm_lenta (candidato de este bloque, "via lenta normalizada por masa"): el paso de la via lenta se multiplica
      por M0 / (P.P), M0 = 3.0 = masa de UN estimulo en todos los mundos del tronco (PAT A-D y los 20 patrones de
      peso 3 del mundo de regla). En esos mundos P.P = 3 -> factor 1.0 exacto -> INERTE por construccion. En 3T-k
      P.P = 3(k+1): el paso por pixel se reparte. Memoria nueva: CERO. Constante nueva: M0 (no se ajusta).

Uso: python experimentos/subida_n7/construye_n7.py   (aborta si un ancla no aparece exactamente una vez)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIG = os.path.join(RAIZ, 'experimentos', 'nivel10_composicion_v14', 'mundo_composicion_v14.py')
SHA_ORIG = 'a9098933b1950e3d'
TRONCO = os.path.join(RAIZ, 'organismo', 'organismo_v142.py')
SHA_TRONCO = '17528d767fcebaf6'
DEST = os.path.join(AQUI, 'mundo_n7.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(txt, viejo, nuevo, n=1):
    c = txt.count(viejo)
    if c != n:
        sys.exit(f'ANCLA con {c} apariciones (se esperaban {n}): {viejo[:90]!r}')
    return txt.replace(viejo, nuevo)


if __name__ == '__main__':
    if h16(ORIG) != SHA_ORIG: sys.exit(f'origen cambio: {h16(ORIG)} != {SHA_ORIG}')
    if h16(TRONCO) != SHA_TRONCO: sys.exit(f'tronco cambio: {h16(TRONCO)} != {SHA_TRONCO}')
    tr = open(TRONCO, encoding='utf-8').read()
    # la condicion de B-5 que se transcribe tiene que estar en el tronco congelado, literal
    sust(tr, "if (Wb[c]*R<0 or (desambiguar and R==0)) and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():", "X")
    sust(tr, "else: Wp[j]=0.; Wn[j]=0.; _ndes+=1;", "X")
    t = open(ORIG, encoding='utf-8').read()
    cab = ('"""mundo_n7 = experimentos/nivel10_composicion_v14/mundo_composicion_v14.py (a9098933b1950e3d, solo se leyo)\n'
           '+ B-5 (desambiguar, transcrito de organismo/organismo_v142.py 17528d767fcebaf6) + norm_lenta (via lenta normalizada\n'
           'por masa, M0 = 3.0). Generado por experimentos/subida_n7/construye_n7.py. NO editar a mano. Con desambiguar=0 y\n'
           'norm_lenta=0 es mundo_composicion_v14 EXACTO (arnes: experimentos/subida_n7/identidad_n7.py)."""\n')
    t = cab + t
    # 1) firma
    t = sust(t, "puerta_pat=0, pat_shuf=0, pat_min=0):", "puerta_pat=0, pat_shuf=0, pat_min=0, desambiguar=0, norm_lenta=0):")
    # 2) contador de divisiones B-5
    t = sust(t, "div_bloq = 0; n_recic = 0", "div_bloq = 0; n_recic = 0; n_des = 0; M0 = 3.0   # n7: divisiones B-5 y masa de referencia de norm_lenta")
    # 3) via lenta normalizada por masa (factor 1.0 exacto si P.P == M0)
    t = sust(t, "                        if _ds > 0: Wps = np.clip(Wps + eta_s * _ds * P, 0, clip_s)\n"
                "                        else:       Wns = np.clip(Wns + eta_s * aversion * (-_ds) * P, 0, clip_s)\n",
                "                        _Pl = P * (M0 / float(P @ P)) if norm_lenta else P   # n7: norm_lenta (paso repartido por la masa de la entrada)\n"
                "                        if _ds > 0: Wps = np.clip(Wps + eta_s * _ds * _Pl, 0, clip_s)\n"
                "                        else:       Wns = np.clip(Wns + eta_s * aversion * (-_ds) * _Pl, 0, clip_s)\n")
    # 4) B-5: conflicto tambien con R == 0
    t = sust(t, "_conf = bool(Wb[c] * R < 0 and abs(float(Wb[c])) > 0.2)   # B3",
                "_conf = bool((Wb[c] * R < 0 or (desambiguar and R == 0)) and abs(float(Wb[c])) > 0.2)   # B3 + B-5 (tronco v14.2)")
    t = sust(t, "                                        else:     Wn[j] = Wn[c]; Wp[j] = 0.; Wn[c] = 0.\n",
                "                                        elif R < 0: Wn[j] = Wn[c]; Wp[j] = 0.; Wn[c] = 0.\n"
                "                                        else: Wp[j] = 0.; Wn[j] = 0.; n_des += 1   # B-5: con R==0 la hija nace SIN valor y la madre conserva el suyo\n")
    # 5) salida
    t = sust(t, "        puerta_pat=puerta_pat, pat_shuf=pat_shuf, pat_min=pat_min, n_cod=len(ncod),\n",
                "        puerta_pat=puerta_pat, pat_shuf=pat_shuf, pat_min=pat_min, n_cod=len(ncod),\n"
                "        desambiguar=desambiguar, norm_lenta=norm_lenta, n_des=int(n_des),\n"
                "        Wps_sum=round(float(Wps.sum()), 4), Wns_sum=round(float(Wns.sum()), 4),\n")
    with open(DEST, 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)
    print(f'origen {SHA_ORIG}  tronco {SHA_TRONCO}  -> mundo_n7.py {h16(DEST)}')

    # --- copias del TRONCO con la perilla norm_lenta (para probar la INERCIA en los mundos del tronco) ---
    for org, sha, pvar, dest in [('organismo_v142.py', SHA_TRONCO, 'PAT[kk]', 'organismo_v142N.py'),
                                 ('organismo_v142g.py', '9e5f566cd6a7a4d2', 'P_[kk]', 'organismo_v142gN.py')]:
        src = os.path.join(RAIZ, 'organismo', org)
        if h16(src) != sha: sys.exit(f'{org} cambio: {h16(src)} != {sha}')
        u = open(src, encoding='utf-8').read()
        u = (f'"""{dest[:-3]} = organismo/{org} ({sha}, CONGELADO: solo se leyo) + perilla norm_lenta (via lenta normalizada\n'
             f'por masa: el paso se multiplica por 3.0/(P.P)). Generado por experimentos/subida_n7/construye_n7.py. NO editar.\n'
             f'Con norm_lenta=0 es {org} EXACTO; con norm_lenta=1 se PREDICE identico en los mundos del tronco (P.P = 3).\n'
             f'Arnes: experimentos/subida_n7/identidad_n7.py."""\n') + u
        u = sust(u, "desambiguar=1):", "desambiguar=1,norm_lenta=0):")
        u = sust(u, f"                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*{pvar},0,clip_s)\n"
                    f"                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*{pvar},0,clip_s)\n",
                    f"                        _Pl={pvar}*(3.0/float({pvar}@{pvar})) if norm_lenta else {pvar}   # n7: norm_lenta\n"
                    f"                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*_Pl,0,clip_s)\n"
                    f"                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*_Pl,0,clip_s)\n")
        d = os.path.join(AQUI, dest)
        with open(d, 'w', encoding='utf-8', newline='\n') as f:
            f.write(u)
        print(f'origen {sha} {org} -> {dest} {h16(d)}')
