"""CREADOR B — bloque 1 (presupuesto de celdas).

Genera experimentos/creacion_B/mundo_k_B.py = mundo_temporal_k.py (68736baafe7c8cdb) con:
  (a) DIAGNOSTICO de solo lectura: reloj de ultima activacion por celda (t_act), cuenta de activaciones (n_act),
      divisiones BLOQUEADAS por pool lleno (div_bloq) e histograma de |Wp-Wn| sobre celdas activas al final.
  (b) PERILLA recic (RCI, reciclaje de celdas invisibles a la puerta). Con recic=0 el codigo es el original
      EXACTO (mismo flujo de azar, misma aritmetica): el unico anadido es contar div_bloq.

RCI, regla local: cuando la division por conflicto de signo debe disparar y NO hay celda libre, se recicla la celda
activa r que cumple (i) |Wp[r]-Wn[r]| <= 0.2 -> INVISIBLE A LA PUERTA de familiaridad por construccion (la puerta
cuenta celdas con |Wp-Wn| > 0.2), (ii) t - t_act[r] > tau_r (fria), (iii) r no esta en el codigo actual. Entre las
candidatas, la de activacion mas antigua (LRU); empate -> indice menor. DETERMINISTA: no toca el RNG.
Memoria que exige: un entero por celda (t_act). Ningun almacen de patrones ni de valores.

Anclas con conteo exacto; origen por sha. NO edita el original.
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

    cab = ('"""mundo_k_B = mundo_temporal_k.py (68736baafe7c8cdb) + diagnostico del presupuesto de celdas + perilla\n'
           'recic (RCI: reciclaje de celdas invisibles a la puerta). Generado por construye_B1.py. NO editar a mano.\n'
           'Con recic=0 es mundo_temporal_k EXACTO (identidad obligatoria: experimentos/creacion_B/identidad_B1.py)."""\n')
    d = os.path.join(AQUI, 'mundo_k_B.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):50s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
