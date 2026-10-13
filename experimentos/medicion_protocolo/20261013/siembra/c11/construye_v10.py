"""Genera organismo/organismo_v10.py, organismo/bateria_v10.py y experimentos/v10_direccion_division/organismo_v10m.py.

Preregistro: PREREGISTRO_v10.md (commiteado ANTES que este script). Anclas con conteo exacto; origenes por sha.

v10 = organismo_v9.py (d3b72fb8819fbe8e) + parametro mu_norm=True: la direccion de division usa mu[c] NORMALIZADA a la
     masa del patron, dist = P - mu[c]*(sum(P)/sum(mu[c])). Con mu_norm=False es v9 exacto. Unica linea de comportamiento.
bateria_v10 = bateria_v9.py (c6496196990f6774) con sustituciones contadas: identidad v10(mu_norm=False)==v9; ningun
     criterio ni umbral cambia (el diff lo demuestra).
v10m = v10 + la instrumentacion de fases de organismo_v9m.py (mismas anclas) + sonda de CODIGOS en cada cambio de fase.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def origen(nombre, sha):
    p = os.path.join(ORG, nombre)
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {nombre}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


LINEA_V9 = "                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-mu[c]\n"
LINEA_V10 = ("                                j=int(np.where(~activa)[0][0]); activa[j]=True; "
             "dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])   # v10: mu normalizada a la masa del patron\n")


def v10():
    s = origen('organismo_v9.py', 'd3b72fb8819fbe8e')
    s = sust(s, "lam=0.05,memoria_rechazo=20):", "lam=0.05,memoria_rechazo=20,mu_norm=True):", etiqueta='firma')
    s = sust(s, LINEA_V9, LINEA_V10, etiqueta='direccion de division')
    cab, cuerpo = s.split('"""\nimport numpy as np', 1)
    cab = ('"""\n'
           'Organismo v10 — CANDIDATO a tronco (congelable solo si pasa PREREGISTRO_v10.md: confirmatorio 21-40 y bateria_v10.py 20).\n'
           '\n'
           'v10 = v9 + DIRECCION DE DIVISION con mu NORMALIZADA: dist = P - mu[c]*(sum P / sum mu[c]). La media movil mu\n'
           'arranca en cero y no converge (~0.63*P), asi que en v9 la celda hija quedaba tan activa para el patron viejo como\n'
           'la madre y lo suplantaba (via estructural del olvido, Etapa 4). Con mu_norm=False es v9 exacto.\n'
           'Linaje: v6 -> v7 -> v7e -> v8 (dca7d5c3a162f5d4) -> v9 (d3b72fb8819fbe8e) -> v10 (este archivo).\n'
           'Generado por experimentos/v10_direccion_division/construye_v10.py. NO editar a mano.\n')
    d = os.path.join(ORG, 'organismo_v10.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + '"""\nimport numpy as np' + cuerpo)
    return d


def bateria_v10():
    s = origen('bateria_v9.py', 'c6496196990f6774')
    s = sust(s, '"""Batería de v9 — examen de congelación (CRITERIO v3, sin cambiar un umbral)',
             '"""Batería de v10 — examen de congelación (CRITERIO v3, sin cambiar un umbral)')
    s = sust(s, 'datos/examen_v9_<fecha>', 'datos/examen_v10_<fecha>')
    s = sust(s, 'Preregistro: experimentos/v9_memoria_rechazo/PREREGISTRO_v9.md (sha f68841597adb55d8).',
             'Preregistro: experimentos/v10_direccion_division/PREREGISTRO_v10.md.')
    s = sust(s, '       v9(memoria_rechazo=0) == v8 en claves de v8;  7 escenarios x semillas 1..6.',
             '       v10(mu_norm=False) == v9 en claves de v9;  7 escenarios x semillas 1..6.')
    s = sust(s, '  6. (fuera de esta batería) organismo/bateria_v8.py 6 PASA y manifiesto.py --check.',
             '  6. (fuera de esta batería) organismo/bateria_v9.py 6 PASA y manifiesto.py --check.')
    s = sust(s, "    import organismo_v8 as ref, organismo_v9 as v9\n    a, b = ref.run(seed, **ESC_ID[esc]), v9.run(seed, memoria_rechazo=0, **ESC_ID[esc])\n",
             "    import organismo_v9 as ref, organismo_v10 as v10\n    a, b = ref.run(seed, **ESC_ID[esc]), v10.run(seed, mu_norm=False, **ESC_ID[esc])\n")
    s = sust(s, "    import organismo_v9 as v9\n    r = v9.run(seed, **ETAPAS[etapa])\n",
             "    import organismo_v10 as v10\n    r = v10.run(seed, **ETAPAS[etapa])\n")
    s = sust(s, "f'examen_v9_{stamp}.log'", "f'examen_v10_{stamp}.log'")
    s = sust(s, "prereg = os.path.join(RAIZ, 'experimentos', 'v9_memoria_rechazo', 'PREREGISTRO_v9.md')",
             "prereg = os.path.join(RAIZ, 'experimentos', 'v10_direccion_division', 'PREREGISTRO_v10.md')")
    s = sust(s, 'log(f"=== Batería v9 — CRITERIO v3,', 'log(f"=== Batería v10 — CRITERIO v3,')
    s = sust(s, "log(f\"sha organismo_v9 {h16(os.path.join(AQUI, 'organismo_v9.py'))}  bateria_v9",
             "log(f\"sha organismo_v10 {h16(os.path.join(AQUI, 'organismo_v10.py'))}  bateria_v10")
    s = sust(s, "for c in ('v8',) for e in ESC_ID", "for c in ('v9',) for e in ESC_ID")
    s = sust(s, "for c, nombre in (('v8', 'v9(memoria=0) == v8'),):", "for c, nombre in (('v9', 'v10(mu_norm=False) == v9'),):")
    s = sust(s, "CRITERIO 5 FALLIDO: v9 no es", "CRITERIO 5 FALLIDO: v10 no es")
    s = sust(s, 'VEREDICTO bateria_v9', 'VEREDICTO bateria_v10')
    s = sust(s, "*** v9 CUMPLE EL CRITERIO v3 con 20 semillas. Por el preregistro: CONGELAR v9 como tronco (si pasa tambien el confirmatorio).",
             "*** v10 CUMPLE EL CRITERIO v3 con 20 semillas. Por el preregistro: CONGELAR v10 como tronco (si pasa tambien Q2-Q5).")
    s = sust(s, "*** v9 cumple el criterio v3 con", "*** v10 cumple el criterio v3 con")
    s = sust(s, "*** v9 NO cumple el criterio v3. No se congela; v8 sigue siendo el tronco.",
             "*** v10 NO cumple el criterio v3. No se congela; v9 sigue siendo el tronco.")
    s = sust(s, "f'examen_v9_{stamp}.json'", "f'examen_v10_{stamp}.json'")
    s = sust(s, "sha_organismo_v9=h16(os.path.join(AQUI, 'organismo_v9.py')), sha_bateria_v9=h16(os.path.abspath(__file__)),",
             "sha_organismo_v10=h16(os.path.join(AQUI, 'organismo_v10.py')), sha_bateria_v10=h16(os.path.abspath(__file__)),")
    s = sust(s, "sha_preregistro=h16(prereg), sha_organismo_v8=h16(os.path.join(AQUI, 'organismo_v8.py')),",
             "sha_preregistro=h16(prereg), sha_organismo_v9=h16(os.path.join(AQUI, 'organismo_v9.py')),")
    d = os.path.join(ORG, 'bateria_v10.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(s)
    return d


def v10m():
    """Mismas anclas que experimentos/etapa4_v9/construye_v9m.py, aplicadas a v10, mas la sonda de codigos."""
    s = open(os.path.join(ORG, 'organismo_v10.py'), encoding='utf-8').read()
    s = sust(s, "lam=0.05,memoria_rechazo=20,mu_norm=True):",
             "lam=0.05,memoria_rechazo=20,mu_norm=True,fases=None,congelar=None,estado_inicial=None,heredar_patas=True,devolver_estado=False):",
             etiqueta='firma')
    ancla = ("    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; "
             "el=np.zeros_like(Wl); tr=np.zeros(9)\n")
    s = sust(s, ancla, ancla +
        "    if estado_inicial is not None:   # v10m: herencia (copias; los contadores empiezan en cero)\n"
        "        KW[:]=estado_inicial['KW']; activa[:]=estado_inicial['activa']; Wp[:]=estado_inicial['Wp']; Wn[:]=estado_inicial['Wn']\n"
        "        err[:]=estado_inicial['err']; mu[:]=estado_inicial['mu']\n"
        "        if heredar_patas: Wl[:]=estado_inicial['Wl']\n"
        "    sondas={}; codigos={}; primer={}; _t_fase=0; dq=[0]*4   # v10m: lectura\n", etiqueta='herencia')
    ancla = "        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val\n"
    s = sust(s, ancla, ancla +
        "        if fases is not None and t in fases:   # v10m: cambio del conjunto de estimulos\n"
        "            tipos[:]=list(fases[t][0]); val.update(fases[t][1]); _t_fase=t\n"
        "            for _x in [_xx for _xx,_kz in list(objs.items()) if _kz not in tipos]: del objs[_x]; _rech.pop(_x,None)\n"
        "            spawn(); sondas[t]={_k:float((Wp-Wn)@kenyon(PAT[_k])) for _k in PAT}\n"
        "            codigos[t]={_k:sorted(int(_i) for _i in code(PAT[_k])) for _k in PAT}\n"
        "        _ap=learn and not (congelar is not None and congelar[0]<=t<congelar[1])   # v10m\n", etiqueta='fases')
    s = sust(s, "if learn:", "if _ap:", n=3, etiqueta='compuerta de aprendizaje')
    ancla = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
    s = sust(s, ancla, ancla +
        "            if (_t_fase,kk) not in primer: primer[(_t_fase,kk)]=dict(t=t,W=float(Wb@kc),pb=float(pb),mordio=bool(mordio))   # v10m\n",
        etiqueta='primer encuentro')
    s = sust(s, "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))\n",
             "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L)); dq[q(t)]+=1\n", etiqueta='muertes por cuarto')
    s = sust(s, "if nuevo else None})",
             "if nuevo else None},sondas=sondas,codigos=codigos,primer={f'{_a}|{_b}':_v for (_a,_b),_v in primer.items()},dq=dq,"
             "estado=(dict(KW=KW.copy(),activa=activa.copy(),Wp=Wp.copy(),Wn=Wn.copy(),err=err.copy(),mu=mu.copy(),Wl=Wl.copy()) "
             "if devolver_estado else None))", etiqueta='return')
    cab = ('"""organismo_v10m = organismo/organismo_v10.py + fases de mundo (con sonda de W y de CODIGOS), congelar aprendizaje,\n'
           'herencia de estado, primer encuentro y muertes por cuarto. Generado por construye_v10.py. NO editar.\n'
           'Con los valores por defecto es v10 exacto; con mu_norm=False es v9 con la misma instrumentacion.\n'
           '"""\n')
    d = os.path.join(AQUI, 'organismo_v10m.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    return d


if __name__ == '__main__':
    for f in (v10, bateria_v10, v10m):
        d = f()
        print(f"  {os.path.relpath(d, RAIZ):52s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
