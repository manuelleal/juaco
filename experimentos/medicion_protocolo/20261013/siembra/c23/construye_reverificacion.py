"""Genera los instrumentos de la re-verificacion sobre v9 (PREREGISTRO_reverificacion_v9.md, sha 2708cb73ab8531e8).

  mundo_temporal_v9.py  <- experimentos/3T_confirmatorio/mundo_temporal_v8.py (ee7eac62ecab3313) + memoria de rechazo
  organismo_caph9.py    <- experimentos/bug01/organismo_caph.py            (38e259b0175d6375) + memoria de rechazo
Misma logica que organismo/organismo_v9.py: memoria por posicion; olvido al morder o al retirarse el objeto; fallback
sin filtro; sin RNG. Con memoria_rechazo=0 son exactamente sus origenes (controles KT1 y KK1).
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, etiqueta):
    c = texto.count(viejo)
    if c != 1:
        raise SystemExit(f"ANCLA {etiqueta}: aparece {c} veces, se esperaba 1. Abortado.")
    return texto.replace(viejo, nuevo)


def mundo_v9():
    org = os.path.join(RAIZ, 'experimentos', '3T_confirmatorio', 'mundo_temporal_v8.py')
    if h16(org) != 'ee7eac62ecab3313':
        raise SystemExit('ORIGEN mundo_temporal_v8 con sha inesperado. Abortado.')
    s = open(org, encoding='utf-8').read()
    s = sust(s, "wclip=3.0, lam=0.05):", "wclip=3.0, lam=0.05, memoria_rechazo=20):", 'firma')
    a = "    t_techo = None; n_techo = 0   # mordida del techo (solo lectura)\n"
    s = sust(s, a, a + "    _rech = {}   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)\n", 'estado')
    s = sust(s, ("    def see():\n"
                 "        best = None\n"
                 "        for x, k in objs.items():\n"
                 "            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)\n"
                 "            if best is None or d < best[0]: best = (d, k, dl < dr)\n"
                 "        return best\n"),
                ("    def see():\n"
                 "        best = None\n"
                 "        for x, k in objs.items():\n"
                 "            if memoria_rechazo and _rech.get(x, -1) > t: continue   # v9\n"
                 "            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)\n"
                 "            if best is None or d < best[0]: best = (d, k, dl < dr)\n"
                 "        if best is None:   # v9: todo filtrado -> regla original\n"
                 "            for x, k in objs.items():\n"
                 "                dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)\n"
                 "                if best is None or d < best[0]: best = (d, k, dl < dr)\n"
                 "        return best\n"), 'see')
    a = "            vis[kk][q(t)] += 1\n"
    s = sust(s, a, a + "            if memoria_rechazo and not mordio: _rech[pos] = t + memoria_rechazo   # v9\n", 'rechazo')
    a = "                del objs[pos]; spawn()\n"
    s = sust(s, a, a + "                _rech.pop(pos, None)   # v9\n", 'olvido al morder')
    s = sust(s, ("        if rng.random() < .003 and objs:\n"
                 "            del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()\n"),
                ("        if rng.random() < .003 and objs:\n"
                 "            _dx = list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx, None)   # v9\n"),
             'retirada')
    cab = ('"""mundo_temporal_v9 = mundo_temporal_v8.py (ee7eac62ecab3313) + memoria de trabajo de rechazo (v9).\n'
           'Generado por construye_reverificacion.py. NO editar. Con memoria_rechazo=0 es mundo_temporal_v8 (KT1)."""\n')
    d = os.path.join(AQUI, 'mundo_temporal_v9.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    return d


def caph9():
    org = os.path.join(RAIZ, 'experimentos', 'bug01', 'organismo_caph.py')
    if h16(org) != '38e259b0175d6375':
        raise SystemExit('ORIGEN organismo_caph con sha inesperado. Abortado.')
    s = open(org, encoding='utf-8').read()
    s = sust(s, "paso=0.5,lam=0.0):", "paso=0.5,lam=0.0,memoria_rechazo=20):", 'firma')
    a = "    t_techo=None; techo_primero=None; n_techo=0; mv_tot=0; mc_tot=0   # <-- prueba de coste (techo)\n"
    s = sust(s, a, a + "    _rech={}   # v9: memoria de trabajo de rechazo\n", 'estado')
    s = sust(s, ("    def see():\n"
                 "        best=None\n"
                 "        for x,k in objs.items():\n"
                 "            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)\n"
                 "            if best is None or d<best[0]: best=(d,k,dl<dr)\n"
                 "        return best\n"),
                ("    def see():\n"
                 "        best=None\n"
                 "        for x,k in objs.items():\n"
                 "            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9\n"
                 "            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)\n"
                 "            if best is None or d<best[0]: best=(d,k,dl<dr)\n"
                 "        if best is None:   # v9: todo filtrado -> regla original\n"
                 "            for x,k in objs.items():\n"
                 "                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)\n"
                 "                if best is None or d<best[0]: best=(d,k,dl<dr)\n"
                 "        return best\n"), 'see')
    a = "            vis[kk][q(t)]+=1; visc[kk]+=1\n"
    s = sust(s, a, a + "            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9\n", 'rechazo')
    a = "                del objs[pos]; spawn()\n"
    s = sust(s, a, a + "                _rech.pop(pos,None)   # v9\n", 'olvido al morder')
    s = sust(s, "        if rng.random()<.003 and objs: del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()\n",
             "        if rng.random()<.003 and objs:\n"
             "            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9\n", 'retirada')
    cab = ('"""organismo_caph9 = organismo_caph.py (38e259b0175d6375) + memoria de trabajo de rechazo (v9).\n'
           'Generado por construye_reverificacion.py. NO editar. Con memoria_rechazo=0 es organismo_caph (KK1)."""\n')
    d = os.path.join(AQUI, 'organismo_caph9.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    return d


if __name__ == '__main__':
    for f in (mundo_v9, caph9):
        d = f()
        print(f"  {os.path.basename(d):24s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
