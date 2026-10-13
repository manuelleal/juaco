"""Construye experimentos/nivel7_hija_dispersa/mundo_hija_dispersa.py POR ANCLAS desde
experimentos/nivel7_3T_k/mundo_temporal_k.py (68736baafe7c8cdb), que NO se toca (solo se lee).

Es la cadena completa de los tres constructores del creador B (construye_B1 + construye_B2 + construye_B3 de
experimentos/creacion_B/) fundida en un solo paso, para que el bloque preregistrado dependa de UN origen y UN
constructor. El resultado es byte a byte el cuerpo de experimentos/creacion_B/mundo_k_B3.py (se comprueba al final).

Perillas que anade (TODAS apagadas por defecto -> mundo_temporal_k EXACTO):
  recic, tau_r   reciclaje LRU de celdas invisibles a la puerta (NO se usa en este bloque; queda en 0)
  mask_rel       0 = v11/v13 (la hija nace ciega solo FUERA de P)
                 1 = traza error-firmada (REFUTADA por perfil plano; se deja por trazabilidad)
                 2 = HIJA DISPERSA por relevancia: contexto O discriminador          [brazo (a)]
                 3 = control: la misma mascara con el bloque del slot profundo intercambiado con el de un
                     distractor (intercambio FORZADO, RNG aparte seed+200000)         [control (c)]
                 4 = control: misma CARDINALIDAD, posiciones al azar                  [control (b)]
  del_s, del_c   umbrales de discriminacion y de contexto (0.25 y 0.25, fijados ANTES de correr)
  n_cf, ema_c    division diferida por n_cf conflictos (1 = v11/v13) y tasa de las medias condicionadas (0.05)
Diagnostico de SOLO LECTURA anadido: div_bloq, n_recic, div_diag, diag (histograma de |Wp-Wn|, celdas frias,
celdas nunca activadas, mediana de activaciones).

Uso:  python experimentos/nivel7_hija_dispersa/construye_hija_dispersa.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'nivel7_3T_k', 'mundo_temporal_k.py')
SHA_ORIGEN = '68736baafe7c8cdb'


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

    # ---------- anclas de construye_B1.py ----------

    # 1) firma: dos perillas nuevas, apagadas por defecto
    s = sust(s, "eta_s=0.0, clip_s=3.0, puerta=None, kprof=1):",
             "eta_s=0.0, clip_s=3.0, puerta=None, kprof=1, recic=0, tau_r=0):", etiqueta='firma')

    # 2) estado nuevo (solo lectura si recic=0)
    s = sust(s, "    Wp = np.zeros(nkmax); Wn = np.zeros(nkmax)\n",
             "    Wp = np.zeros(nkmax); Wn = np.zeros(nkmax)\n"
             "    t_act = np.full(nkmax, -10**9, dtype=np.int64); n_act = np.zeros(nkmax, dtype=np.int64)   # B: reloj y cuenta de activacion por celda\n"
             "    div_bloq = 0; n_recic = 0   # B: divisiones que el pool lleno bloqueo / celdas recicladas\n",
             etiqueta='estado B')

    # 3) reloj de activacion (dentro de plast, sobre el codigo que acaba de morder)
    s = sust(s, "                        idx = np.where(kc > 0)[0]\n"
                "                        err[idx] = (1 - ema) * err[idx] + ema * abs(dlt)\n",
             "                        idx = np.where(kc > 0)[0]\n"
             "                        t_act[idx] = t; n_act[idx] += 1   # B: solo lectura si recic=0\n"
             "                        err[idx] = (1 - ema) * err[idx] + ema * abs(dlt)\n", etiqueta='reloj de activacion')

    # 4) la division: separar "no hay libre" de "no dividir", y reciclar si recic
    viejo = (
        "                                if Wb[c] * R < 0 and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(KW[c] @ P) and (~activa).any():\n"
        "                                    a1 = float(np.abs(dist).sum())\n"
        "                                    ft = float(np.abs(dist[6:]).sum()) / a1 if (a1 > 0 and NIN > 6) else 0.0\n"
        "                                    j = int(np.where(~activa)[0][0]); activa[j] = True; KW[j] = kj\n"
        "                                    if R > 0: Wp[j] = Wp[c]; Wn[j] = 0.; Wp[c] = 0.\n"
        "                                    else:     Wn[j] = Wn[c]; Wp[j] = 0.; Wn[c] = 0.\n"
        "                                    mu[j] = P * (float(mu[c].sum()) / P.sum()); err[c] = err[j] = 0; splits += 1\n"
        "                                    split_t.append((t, kk, (prev_sent[0] if kprof == 1 else prev_sent), round(ft, 3)))\n"
        "                                    if not (~activa).any() and t_pool is None: t_pool = t\n")
    nuevo = (
        "                                if Wb[c] * R < 0 and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(KW[c] @ P):\n"
        "                                    _libre = bool((~activa).any()); _j2 = -1\n"
        "                                    if not _libre:\n"
        "                                        div_bloq += 1\n"
        "                                        if recic:   # RCI: celda invisible a la puerta (|Wp-Wn|<=0.2), fria (t-t_act>tau_r), fuera del codigo; LRU\n"
        "                                            _msk = activa & (np.abs(Wp - Wn) <= 0.2) & ((t - t_act) > tau_r)\n"
        "                                            _msk[idx] = False\n"
        "                                            _cd = np.where(_msk)[0]\n"
        "                                            if _cd.size: _j2 = int(_cd[int(np.argmin(t_act[_cd]))]); n_recic += 1\n"
        "                                    if _libre or _j2 >= 0:\n"
        "                                        a1 = float(np.abs(dist).sum())\n"
        "                                        ft = float(np.abs(dist[6:]).sum()) / a1 if (a1 > 0 and NIN > 6) else 0.0\n"
        "                                        j = int(np.where(~activa)[0][0]) if _libre else _j2; activa[j] = True; KW[j] = kj\n"
        "                                        if R > 0: Wp[j] = Wp[c]; Wn[j] = 0.; Wp[c] = 0.\n"
        "                                        else:     Wn[j] = Wn[c]; Wp[j] = 0.; Wn[c] = 0.\n"
        "                                        mu[j] = P * (float(mu[c].sum()) / P.sum()); err[c] = err[j] = 0; splits += 1; t_act[j] = t\n"
        "                                        split_t.append((t, kk, (prev_sent[0] if kprof == 1 else prev_sent), round(ft, 3)))\n"
        "                                        if not (~activa).any() and t_pool is None: t_pool = t\n")
    s = sust(s, viejo, nuevo, etiqueta='division con reciclaje')

    # 5) salida: diagnostico del presupuesto
    s = sust(s, "        t_techo=t_techo, n_techo=n_techo, lam=lam)\n",
             "        t_techo=t_techo, n_techo=n_techo, lam=lam,\n"
             "        div_bloq=int(div_bloq), n_recic=int(n_recic), recic=recic, tau_r=tau_r,\n"
             "        diag=dict(act=int(activa.sum()),\n"
             "                  inv=int(((np.abs(Wp - Wn) <= 0.2) & activa).sum()),\n"
             "                  frias=int((activa & ((T - t_act) > 10000)).sum()),\n"
             "                  recic_ok=int((activa & (np.abs(Wp - Wn) <= 0.2) & ((T - t_act) > 10000)).sum()),\n"
             "                  nunca=int((activa & (t_act < 0)).sum()),\n"
             "                  n_act_med=float(np.median(n_act[activa])),\n"
             "                  hist=[int(((np.abs(Wp - Wn) > b0) & (np.abs(Wp - Wn) <= b1) & activa).sum())\n"
             "                        for b0, b1 in [(-1.0, 0.05), (0.05, 0.2), (0.2, 0.5), (0.5, 1.0), (1.0, 3.1)]]))\n",
             etiqueta='salida diagnostico')

    # ---------- anclas de construye_B2.py ----------

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

    # ---------- anclas de construye_B3.py ----------

    # 1) firma
    s = sust(s, "mask_rel=0, del_s=0.25, del_c=0.25):",
             "mask_rel=0, del_s=0.25, del_c=0.25, n_cf=1, ema_c=0.05):", etiqueta='firma')

    # 2) estado: medias condicionadas y contador de conflictos
    s = sust(s, "    mus = np.zeros((nkmax, NIN)); div_diag = []   # B2: EMA de P firmada por el error; diagnostico de division\n",
             "    mus = np.zeros((nkmax, NIN)); div_diag = []   # B2: EMA de P firmada por el error; diagnostico de division\n"
             "    mup = np.zeros((nkmax, NIN)); mun = np.zeros((nkmax, NIN))   # B3: medias condicionadas por el signo de R\n"
             "    zp = np.zeros(nkmax); zn = np.zeros(nkmax); ncf = np.zeros(nkmax, dtype=np.int64)   # B3: normalizadores y conflictos\n",
             etiqueta='estado B3')

    # 3) actualizacion de las medias condicionadas (clase por el signo de R; el neutro R=0 no entra en ninguna)
    s = sust(s, "                        mus[idx] = (1 - ema) * mus[idx] + ema * (P if dlt > 0 else -P)   # B2: traza error-firmada\n",
             "                        mus[idx] = (1 - ema) * mus[idx] + ema * (P if dlt > 0 else -P)   # B2: traza error-firmada\n"
             "                        if R > 0:   # B3: media condicionada de la clase positiva (con su normalizador)\n"
             "                            mup[idx] = (1 - ema_c) * mup[idx] + ema_c * P; zp[idx] = (1 - ema_c) * zp[idx] + ema_c\n"
             "                        elif R < 0:\n"
             "                            mun[idx] = (1 - ema_c) * mun[idx] + ema_c * P; zn[idx] = (1 - ema_c) * zn[idx] + ema_c\n",
             etiqueta='medias condicionadas')

    # 4) mascara de dos ramas (y su CONTROL BARAJADO: mask_rel=3, la misma mascara con los slots de historia permutados)
    s = sust(s, "                                if mask_rel:   # B2: ciega fuera de lo RELEVANTE (discrimina el signo o la madre lo codifica siempre)\n",
             "                                if mask_rel in (2, 3, 4) and zp[c] > 1e-6 and zn[c] > 1e-6:   # B3: contexto O discriminador\n"
             "                                    _mp = mup[c] / float(zp[c]); _mn = mun[c] / float(zn[c])\n"
             "                                    _rel = (np.abs(_mp - _mn) > del_s) | (np.minimum(_mp, _mn) > 1.0 - del_c)\n"
             "                                    if mask_rel == 3: _rel = _rel[_PERM]   # control A: el bloque del slot profundo se intercambia con el de un distractor (slot equivocado, misma forma)\n"
             "                                    elif mask_rel == 4:   # control B: misma CANTIDAD de pixeles, posiciones al azar (separa 'menos pixeles' de 'los pixeles correctos')\n"
             "                                        _nk = int(_rel.sum()); _rel = np.zeros(NIN, bool); _rel[_rng3.choice(NIN, _nk, replace=False)] = True\n"
             "                                    _rel = (P > 0) & _rel\n"
             "                                elif mask_rel == 1:   # B2: ciega fuera de lo RELEVANTE (traza firmada; refutada por plano)\n",
             etiqueta='mascara dos ramas')

    # 4b) permutacion del control, sorteada con un RNG APARTE (no toca el flujo de azar del organismo)
    s = sust(s, "    mup = np.zeros((nkmax, NIN)); mun = np.zeros((nkmax, NIN))   # B3: medias condicionadas por el signo de R\n",
             "    mup = np.zeros((nkmax, NIN)); mun = np.zeros((nkmax, NIN))   # B3: medias condicionadas por el signo de R\n"
             "    _rng3 = np.random.default_rng(seed + 200000)   # B3: solo para los controles (mask_rel=3 y 4); RNG aparte\n"
             "    _ns = NIN // 6; _bl = list(range(_ns))\n"
             "    if _ns > 2:   # control A: intercambio FORZADO del slot profundo con un distractor (nunca degenera en la identidad)\n"
             "        _a = 1 + int(_rng3.integers(_ns - 2)); _bl[_a], _bl[_ns - 1] = _bl[_ns - 1], _bl[_a]\n"
             "    _PERM = np.concatenate([np.arange(6 * b, 6 * b + 6) for b in _bl]).astype(np.int64)\n",
             etiqueta='permutacion del control')

    # 5) division diferida por conflictos
    s = sust(s, "                                if Wb[c] * R < 0 and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(KW[c] @ P):\n",
             "                                _conf = bool(Wb[c] * R < 0 and abs(float(Wb[c])) > 0.2)   # B3\n"
             "                                if _conf: ncf[c] += 1\n"
             "                                if _conf and ncf[c] >= n_cf and float(kj @ P) > float(KW[c] @ P):\n",
             etiqueta='division diferida')

    # 6) reset del contador y herencia de las medias en la division efectiva
    s = sust(s, "                                        mus[j] = mus[c].copy()   # B2: la hija hereda la traza firmada de la madre\n",
             "                                        mus[j] = mus[c].copy()   # B2: la hija hereda la traza firmada de la madre\n"
             "                                        mup[j] = mup[c].copy(); mun[j] = mun[c].copy(); zp[j] = zp[c]; zn[j] = zn[c]   # B3\n"
             "                                        ncf[c] = 0; ncf[j] = 0   # B3: el conflicto queda resuelto\n",
             etiqueta='herencia B3')

    # 7) diagnostico: perfil DISCRIMINATIVO por slot (|_mp - _mn|) y de contexto (min(_mp,_mn)), solo lectura
    s = sust(s, "                                                             [round(float(np.abs(mus[c][6 * _i:6 * _i + 6]).max()), 3) for _i in range(NIN // 6)]))\n",
             "                                                             [round(float(np.abs((mup[c] / max(float(zp[c]), 1e-9) - mun[c] / max(float(zn[c]), 1e-9))[6 * _i:6 * _i + 6]).max()), 3) for _i in range(NIN // 6)],\n"
             "                                                             [round(float(np.minimum(mup[c] / max(float(zp[c]), 1e-9), mun[c] / max(float(zn[c]), 1e-9))[6 * _i:6 * _i + 6].max()), 3) for _i in range(NIN // 6)],\n"
             "                                                             int(ncf[c])))\n", etiqueta='diagnostico discriminativo')

    # 8) salida
    s = sust(s, "        mask_rel=mask_rel, div_diag=div_diag,\n",
             "        mask_rel=mask_rel, div_diag=div_diag, n_cf=n_cf,\n", etiqueta='salida B3')

    cab = ('"""mundo_hija_dispersa = mundo_temporal_k.py (68736baafe7c8cdb) + HIJA DISPERSA (mask_rel) +'
           ' division diferida (n_cf) + reciclaje apagado (recic) + diagnostico del presupuesto de celdas.\n'
           'Generado por construye_hija_dispersa.py. NO editar a mano. Con recic=0, mask_rel=0 y n_cf=1 es\n'
           'mundo_temporal_k EXACTO (arnes: experimentos/nivel7_hija_dispersa/identidad_hija_dispersa.py)."""\n')
    d = os.path.join(AQUI, 'mundo_hija_dispersa.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):55s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
    ref = os.path.join(RAIZ, 'experimentos', 'creacion_B', 'mundo_k_B3.py')
    if os.path.exists(ref):
        a = open(ref, encoding='utf-8').read(); a = a[a.index('"""mundo_temporal_k = '):]
        print('  cuerpo identico al de creacion_B/mundo_k_B3.py:', a == s)
