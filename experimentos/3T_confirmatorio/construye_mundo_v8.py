"""Genera mundo_temporal_v8.py por parcheo con anclas desde experimentos/ramas/3T_temporal/mundo_temporal.py.

Preregistro: PREREGISTRO_3T_confirmatorio.md, commiteado ANTES que este script.
Cada ancla aparece EXACTAMENTE una vez o el script aborta; el origen se comprueba por sha.

Cambios (y solo estos):
  - parametro lam=0.05 y la linea de drenaje de la parte comun, ARITMETICAMENTE IDENTICA a la de
    organismo/organismo_v8.py y en el mismo sitio: tras calcular dlt, antes del clip (20 esp., dentro de `if learn:`).
  - mordida del techo contra `wclip` (t_techo, n_techo), solo lectura.
  - claves nuevas en la salida: t_techo, n_techo, lam.
Con lam=0 es mundo_temporal.py campo a campo (control K1 de corre_3T_confirmatorio.py).

Uso:  python experimentos/3T_confirmatorio/construye_mundo_v8.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'ramas', '3T_temporal', 'mundo_temporal.py')
SHA_ORIGEN = '1f447657faf00ef8'
DESTINO = os.path.join(AQUI, 'mundo_temporal_v8.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sustituye(texto, viejo, nuevo, etiqueta):
    n = texto.count(viejo)
    if n != 1:
        raise SystemExit(f"ANCLA {etiqueta}: aparece {n} veces, se esperaba 1. Abortado.")
    return texto.replace(viejo, nuevo)


if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN: sha {h16(ORIGEN)}, se esperaba {SHA_ORIGEN}. Abortado.")
    src = open(ORIGEN, encoding='utf-8').read()

    src = sustituye(src, "theta=0.6, ema=0.02, paso=0.5, early=5000, nkmax=NKMAX, wclip=3.0):",
                    "theta=0.6, ema=0.02, paso=0.5, early=5000, nkmax=NKMAX, wclip=3.0, lam=0.05):", "firma")

    ancla = "    splits = 0; split_t = []; deaths = 0; Rtot = 0.0; t_pool = None\n"
    src = sustituye(src, ancla, ancla + "    t_techo = None; n_techo = 0   # mordida del techo (solo lectura)\n", "contadores")

    # 20 espacios = dentro de `if learn:`, tras dlt y antes del clip: el mismo sitio que en organismo_v8.py
    ancla = "                    dlt = R - Wb @ kc\n"
    src = sustituye(src, ancla, ancla +
        "                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom"
        "   # drenaje de la parte comun, identico a organismo_v8\n"
        "                    _ix = kc > 0\n"
        "                    if dlt > 0: _trunca = bool(((Wp[_ix] + eta * dlt) > wclip).any())\n"
        "                    else:       _trunca = bool(((Wn[_ix] + eta * aversion * (-dlt)) > wclip).any())\n"
        "                    if _trunca:\n"
        "                        n_techo += 1\n"
        "                        if t_techo is None: t_techo = t\n", "drenaje+techo")

    src = sustituye(src, "deaths=deaths, Rtot=round(Rtot, 2), E_fin=round(float(E), 3), snaps=snaps)",
                    "deaths=deaths, Rtot=round(Rtot, 2), E_fin=round(float(E), 3), snaps=snaps,\n"
                    "        t_techo=t_techo, n_techo=n_techo, lam=lam)", "return")

    cab = ('"""mundo_temporal_v8 = mundo_temporal.py (1f447657faf00ef8) + drenaje de la parte comun (lam=0.05, linea\n'
           'aritmeticamente identica a organismo/organismo_v8.py) + mordida del techo. Generado por\n'
           'construye_mundo_v8.py. NO editar a mano. Con lam=0 es mundo_temporal.py (control K1).\n'
           'Preregistro: experimentos/3T_confirmatorio/PREREGISTRO_3T_confirmatorio.md\n'
           '"""\n')
    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(cab + src)
    print(f"  mundo_temporal_v8.py  {h16(DESTINO)}  {sum(1 for _ in open(DESTINO, encoding='utf-8'))} lineas")
    print("Generado. Su correccion la demuestra K1 de corre_3T_confirmatorio.py.")
