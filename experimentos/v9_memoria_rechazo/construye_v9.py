"""Genera organismo/organismo_v9.py (candidato a tronco) y experimentos/v9_memoria_rechazo/organismo_v9c.py (control C1).

Preregistro: PREREGISTRO_v9.md (sha f68841597adb55d8), commiteado ANTES que este script.
Anclas unicas; origen comprobado por sha.

v9 = organismo_v8.py (dca7d5c3a162f5d4) + memoria de trabajo de rechazo (O3 de la exploracion, tau por defecto 20):
  - si la boca NO muerde un objeto, esa posicion deja de ser objetivo de see() durante `memoria_rechazo` pasos;
  - la memoria de una posicion se borra cuando su objeto desaparece (mordido o retirado por el mundo);
  - si todo esta filtrado, see() vuelve a la regla original (fallback) y se cuenta una vez por paso;
  - ninguna linea nueva llama al RNG. Con memoria_rechazo=0 es v8 exacto.
  Instrumentacion de solo lectura por cuarto: `sobre` (pasos sobre objeto) y `llegadas`, por valencia vigente;
  `sin_objetivo` (pasos en fallback).
v9c = v9 + memoria_modo ('rechazado' = v9; 'azar' = tras un rechazo se recuerda OTRO objeto al azar, con un RNG
  separado seed+200000 que no toca el flujo principal).
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'organismo', 'organismo_v8.py')
SHA_ORIGEN = 'dca7d5c3a162f5d4'
DEST_V9 = os.path.join(RAIZ, 'organismo', 'organismo_v9.py')
DEST_V9C = os.path.join(AQUI, 'organismo_v9c.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sustituye(texto, viejo, nuevo, etiqueta):
    n = texto.count(viejo)
    if n != 1:
        raise SystemExit(f"ANCLA {etiqueta}: aparece {n} veces, se esperaba 1. Abortado.")
    return texto.replace(viejo, nuevo)


SEE_V8 = ("    def see():\n"
          "        best=None\n"
          "        for x,k in objs.items():\n"
          "            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)\n"
          "            if best is None or d<best[0]: best=(d,k,dl<dr)\n"
          "        return best\n")
SEE_V9 = ("    def see(contar=False):\n"
          "        best=None\n"
          "        for x,k in objs.items():\n"
          "            if memoria_rechazo and _rech.get(x,-1)>t: continue   # v9: rechazado hace poco, no es objetivo\n"
          "            dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)\n"
          "            if best is None or d<best[0]: best=(d,k,dl<dr)\n"
          "        if best is None:   # v9: todo filtrado -> regla original (fallback)\n"
          "            if contar: sin_objetivo[q(t)]+=1\n"
          "            for x,k in objs.items():\n"
          "                dl=(pos-x)%L; dr=(x-pos)%L; d=min(dl,dr)\n"
          "                if best is None or d<best[0]: best=(d,k,dl<dr)\n"
          "        return best\n")


def construye_v9():
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN: sha {h16(ORIGEN)}, se esperaba {SHA_ORIGEN}. Abortado.")
    src = open(ORIGEN, encoding='utf-8').read()
    src = sustituye(src, "solap_AB=None,lam=0.05):", "solap_AB=None,lam=0.05,memoria_rechazo=20):", "firma")
    ancla = "    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura\n"
    src = sustituye(src, ancla, ancla +
        "    _rech={}; _prev_on=-1   # v9: memoria de trabajo de rechazo (posicion -> paso hasta el que no es objetivo)\n"
        "    sobre={'veneno':[0]*4,'comida':[0]*4}; llegadas={'veneno':[0]*4,'comida':[0]*4}; sin_objetivo=[0]*4   # v9: lectura\n",
        "estado v9")
    src = sustituye(src, SEE_V8, SEE_V9, "see")
    src = sustituye(src, "        hambre=np.clip(1-E,0,1); d,k,left=see(); pat=PAT[k]\n",
                    "        hambre=np.clip(1-E,0,1); d,k,left=see(contar=True); pat=PAT[k]\n", "see del paso")
    # 12 espacios: dentro de `if pos in objs:`, tras decidir mordio y contar la visita
    ancla = "            vis[kk][q(t)]+=1\n"
    src = sustituye(src, ancla, ancla +
        "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
        "            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo\n",
        "rechazo")
    # 16 espacios: dentro de `if mordio:`, tras retirar el objeto mordido y reponer
    ancla = "                del objs[pos]; spawn()\n"
    src = sustituye(src, ancla, ancla + "                _rech.pop(pos,None)   # v9: ese objeto ya no existe\n", "olvido al morder")
    # retirada aleatoria: mismas llamadas al RNG en el mismo orden, y olvido de la posicion retirada
    src = sustituye(src, "        if rng.random()<.003 and objs: del objs[list(objs)[int(rng.integers(len(objs)))]]; spawn()\n",
                    "        if rng.random()<.003 and objs:\n"
                    "            _dx=list(objs)[int(rng.integers(len(objs)))]; del objs[_dx]; spawn(); _rech.pop(_dx,None)   # v9: olvido\n",
                    "retirada aleatoria")
    src = sustituye(src, "        E-=costo\n", "        _prev_on=pos if pos in objs else -1   # v9: para contar llegadas\n        E-=costo\n",
                    "prev_on")
    src = sustituye(src, "    return dict(err_max=err_max,",
                    "    return dict(sobre=sobre,llegadas=llegadas,sin_objetivo=sin_objetivo,memoria_rechazo=memoria_rechazo,err_max=err_max,",
                    "return")
    cab = ('"""\n'
           'Organismo v9 — CANDIDATO a tronco (congelable solo si pasa el confirmatorio de PREREGISTRO_v9.md y bateria_v9.py 20).\n'
           '\n'
           'v9 = v8 + MEMORIA DE TRABAJO DE RECHAZO: lo que la boca acaba de rechazar deja de ser objetivo de las patas\n'
           'durante `memoria_rechazo` pasos (20). Con memoria_rechazo=0 es v8 exacto.\n'
           'Linaje: v6 (5f38f83cf49248a3) -> v7 -> v7e -> v8 (dca7d5c3a162f5d4) -> v9 (este archivo).\n'
           'Generado por experimentos/v9_memoria_rechazo/construye_v9.py. NO editar a mano.\n'
           'Preregistro: experimentos/v9_memoria_rechazo/PREREGISTRO_v9.md (f68841597adb55d8).\n'
           '"""\n')
    open(DEST_V9, 'w', encoding='utf-8', newline='\n').write(cab + src)
    return DEST_V9


def construye_v9c():
    src = open(DEST_V9, encoding='utf-8').read()
    src = sustituye(src, "memoria_rechazo=20):", "memoria_rechazo=20,memoria_modo='rechazado'):", "firma v9c")
    ancla = "    rng=np.random.default_rng(seed)\n"
    src = sustituye(src, ancla, ancla + "    rng2=np.random.default_rng(seed+200000)   # v9c: RNG separado para el control C1\n", "rng2")
    src = sustituye(src,
        "            if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo   # v9: la boca rechazo -> no es objetivo por un tiempo\n",
        "            if memoria_rechazo and not mordio:\n"
        "                if memoria_modo=='rechazado': _rech[pos]=t+memoria_rechazo\n"
        "                else:   # C1: se recuerda OTRO objeto al azar, no el rechazado\n"
        "                    _otros=[xx for xx in objs if xx!=pos]\n"
        "                    if _otros: _rech[_otros[int(rng2.integers(len(_otros)))]]=t+memoria_rechazo\n",
        "modo")
    cab = '"""organismo_v9c = organismo_v9 + memoria_modo (control C1 de PREREGISTRO_v9.md). NO es tronco."""\n'
    open(DEST_V9C, 'w', encoding='utf-8', newline='\n').write(cab + src)
    return DEST_V9C


if __name__ == '__main__':
    for f in (construye_v9, construye_v9c):
        d = f()
        print(f"  {os.path.relpath(d, RAIZ):48s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
