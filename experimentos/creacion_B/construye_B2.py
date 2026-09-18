"""CREADOR B — bloque 2: HIJA CIEGA POR RELEVANCIA (dendrita de dos ramas).

Genera experimentos/creacion_B/mundo_k_B2.py = mundo_k_B.py (c123df80b77062d9, que es mundo_temporal_k
68736baafe7c8cdb + diagnostico) con:
  (a) TRAZA ERROR-FIRMADA por celda:  mus[c] <- (1-ema)*mus[c] + ema*(P if dlt>0 else -P).
      Es la misma EMA que ya lleva mu[c], pero firmada por el error. Coste: un vector NIN por celda (igual que mu).
      Lee sólo lo que la celda ya tiene delante (P) y el error que ya usa (dlt): regla LOCAL, sin gradiente ajeno.
  (b) PERILLA mask_rel: al nacer, la hija es ciega fuera de los pixeles RELEVANTES de P en vez de fuera de TODO P:
        relevante[i]  <=>  P[i] > 0  Y  ( |mus[c][i]| > del_s   O   mu_norm[c][i] > 1 - del_c )
      es decir, conserva (1) lo que DISCRIMINA el signo del error y (2) lo que la madre ya codifica de forma
      consistente; queda ciega a lo que es inconsistente Y no discrimina (los distractores de la historia).
      Con mask_rel=0 la mascara es (P > 0): mundo_k_B EXACTO.
  (c) Diagnostico de division (solo lectura): por cada division, pixeles conservados y perfil de |mus| por slot.

Por que deberia funcionar: a profundidad k hay 2^(k-1) rellenos distintos y el codigo de v13 es exacto por patron
compuesto, asi que la evidencia por codigo cae como 2^-(k-1). Una hija ciega a los distractores responde a TODOS los
rellenos: la evidencia se comparte en vez de repartirse. Es composicion barata por dendritas (dos ramas: lo que la
madre codifica AND el slot que discrimina), no por mas celdas — el pool ya se midio y NO es el techo.

Anclas con conteo exacto; origen por sha. NO edita originales.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(AQUI, 'mundo_k_B.py')
SHA_ORIGEN = 'c123df80b77062d9'


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

    # 1) firma
    s = sust(s, "kprof=1, recic=0, tau_r=0):",
             "kprof=1, recic=0, tau_r=0, mask_rel=0, del_s=0.25, del_c=0.25):", etiqueta='firma')

    # 2) estado: traza error-firmada + diagnostico de division
    s = sust(s, "    err = np.zeros(nkmax); mu = np.zeros((nkmax, NIN))\n",
             "    err = np.zeros(nkmax); mu = np.zeros((nkmax, NIN))\n"
             "    mus = np.zeros((nkmax, NIN)); div_diag = []   # B2: EMA de P firmada por el error; diagnostico de division\n",
             etiqueta='estado B2')

    # 3) actualizacion de la traza firmada (junto a mu, misma ema, mismo indice)
    s = sust(s, "                        mu[idx] = (1 - ema) * mu[idx] + ema * P\n",
             "                        mu[idx] = (1 - ema) * mu[idx] + ema * P\n"
             "                        mus[idx] = (1 - ema) * mus[idx] + ema * (P if dlt > 0 else -P)   # B2: traza error-firmada\n",
             etiqueta='traza firmada')

    # 4) mascara de la hija
    s = sust(s, "                                kj = np.clip(KW[c] * (1 - 0.05) + paso * dist, 0, 5) * (P > 0)\n",
             "                                if mask_rel:   # B2: ciega fuera de lo RELEVANTE (discrimina el signo o la madre lo codifica siempre)\n"
             "                                    _mnr = mu[c] * (P.sum() / max(float(mu[c].sum()), 1e-9))\n"
             "                                    _rel = (P > 0) & ((np.abs(mus[c]) > del_s) | (_mnr > 1.0 - del_c))\n"
             "                                else:\n"
             "                                    _rel = (P > 0)\n"
             "                                kj = np.clip(KW[c] * (1 - 0.05) + paso * dist, 0, 5) * _rel\n",
             etiqueta='mascara de la hija')

    # 5) diagnostico en la division efectiva (solo lectura)
    s = sust(s, "                                        mu[j] = P * (float(mu[c].sum()) / P.sum()); err[c] = err[j] = 0; splits += 1; t_act[j] = t\n",
             "                                        mu[j] = P * (float(mu[c].sum()) / P.sum()); err[c] = err[j] = 0; splits += 1; t_act[j] = t\n"
             "                                        mus[j] = mus[c].copy()   # B2: la hija hereda la traza firmada de la madre\n"
             "                                        if len(div_diag) < 400:\n"
             "                                            div_diag.append((t, int(_rel.sum()), int((P > 0).sum()),\n"
             "                                                             [round(float(np.abs(mus[c][6 * _i:6 * _i + 6]).max()), 3) for _i in range(NIN // 6)]))\n",
             etiqueta='diagnostico de division')

    # 6) salida
    s = sust(s, "        div_bloq=int(div_bloq), n_recic=int(n_recic), recic=recic, tau_r=tau_r,\n",
             "        div_bloq=int(div_bloq), n_recic=int(n_recic), recic=recic, tau_r=tau_r,\n"
             "        mask_rel=mask_rel, div_diag=div_diag,\n", etiqueta='salida B2')

    cab = ('"""mundo_k_B2 = mundo_k_B.py (c123df80b77062d9) + traza error-firmada mus[c] + perilla mask_rel\n'
           '(hija ciega fuera de lo relevante). Generado por construye_B2.py. NO editar a mano.\n'
           'Con mask_rel=0 es mundo_k_B EXACTO, y con recic=0 ademas mundo_temporal_k EXACTO."""\n')
    d = os.path.join(AQUI, 'mundo_k_B2.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):50s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
