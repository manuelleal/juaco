"""CREADOR B — bloque 3: DENDRITA DE DOS RAMAS (contexto AND discriminador), con division diferida.

Genera experimentos/creacion_B/mundo_k_B3.py = mundo_k_B2.py (e7f8d22b599a8f16) con:
  (a) DOS MEDIAS CONDICIONADAS por celda, con normalizador (EMA con correccion de sesgo):
        R > 0:  mup[c] <- (1-ec)*mup[c] + ec*P ;  zp[c] <- (1-ec)*zp[c] + ec
        R < 0:  mun[c] <- (1-ec)*mun[c] + ec*P ;  zn[c] <- (1-ec)*zn[c] + ec
      medias: _mp = mup[c]/zp[c],  _mn = mun[c]/zn[c].  Coste: dos vectores NIN y dos escalares por celda.
      Todo local: la celda ve su propia entrada P y el refuerzo R que ya recibe.
  (b) CONTADOR DE CONFLICTOS ncf[c]: la division por conflicto de signo espera a n_cf conflictos (n_cf=1 = v11/v13).
      Motivo medido: con UN solo conflicto hay dos patrones y los slots que difieren son el que manda Y la mitad de
      los distractores; la causa NO es identificable. Con varios conflictos, el slot que manda difiere SIEMPRE y los
      distractores difieren la mitad de las veces: las medias condicionadas los cancelan.
  (c) mask_rel=2: la hija nace ciega fuera de  CONTEXTO  O  DISCRIMINADOR:
        rel[i] <=> P[i]>0  Y  ( |_mp[i]-_mn[i]| > del_s   O   min(_mp[i],_mn[i]) > 1-del_c )
      dos ramas: lo que esta presente en las DOS clases (contexto: el objeto actual) y lo que separa las clases (el
      slot profundo). Los distractores, que valen ~0.5 en las dos clases, no cumplen ninguna: la hija es ciega a
      ellos y responde a TODOS los rellenos -> la evidencia se comparte en vez de repartirse entre 2^(k-1) codigos.

Con n_cf=1 y mask_rel=0 es mundo_k_B2 EXACTO (y con recic=0, mundo_temporal_k EXACTO).
Anclas con conteo exacto; origen por sha. NO edita originales.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(AQUI, 'mundo_k_B2.py')
SHA_ORIGEN = 'e7f8d22b599a8f16'


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

    cab = ('"""mundo_k_B3 = mundo_k_B2.py (e7f8d22b599a8f16) + medias condicionadas por clase (mup/mun con\n'
           'normalizador), division diferida por n_cf conflictos y mascara de dos ramas (mask_rel=2).\n'
           'Generado por construye_B3.py. NO editar a mano. Con n_cf=1 y mask_rel=0 es mundo_k_B2 EXACTO."""\n')
    d = os.path.join(AQUI, 'mundo_k_B3.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):50s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
