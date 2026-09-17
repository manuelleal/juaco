"""Genera los instrumentos de v11 = v10 + REGLA DE DIVISION POR CONFLICTO DE SIGNO (nacida en JUACO-EVO, gen1/llm_2).
Anclas con conteo exacto; origenes comprobados por sha. Preregistro: PREREGISTRO_v11.md.

  organismo/organismo_v11.py      <- organismo/organismo_v10.py (219d5033fe15b5b9) + div_signo=True
  organismo/bateria_v11.py        <- organismo/bateria_v10.py   (d354813d3fa9d0f1) + identidades v9 y v10, --desde, 4a'
  experimentos/v11_evo_division/organismo_v11m.py  <- organismo_v11.py + instrumentacion de fases (anclas de v10m)
  experimentos/v11_evo_division/organismo_caph11.py <- experimentos/v9_reverificacion/organismo_caph9.py (1b113605dc803435)
                                                       + mu_norm + div_signo (ambos False por defecto = caph9)

Con div_signo=False, v11 es v10 exacto; con mu_norm=False y div_signo=False, es v9 exacto.
El genoma evolucionado experimentos/evo/gen1/llm_2/organismo.py (f9cce63d371977ed) NO se edita: v11m debe ser igual a el.
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


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


# --- bloque de division de v10 (4 lineas) y su sustituto con la regla evolucionada, literal de gen1/llm_2 ---
DIV_V10 = (
    "                        for c in idx:\n"
    "                            if err[c]>theta and (~activa).any():\n"
    "                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])   # v10: mu normalizada a la masa del patron\n"
    "                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)\n"
    "                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n")
DIV_V11 = (
    "                        for c in idx:\n"
    "                            if div_signo:   # v11 (JUACO-EVO gen1/llm_2): divide por CONFLICTO DE SIGNO, hija ciega fuera de P, madre fija, fision del valor\n"
    "                                dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])\n"
    "                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*(P>0)\n"
    "                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():\n"
    "                                    j=int(np.where(~activa)[0][0]); activa[j]=True; KW[j]=kj\n"
    "                                    if R>0: Wp[j]=Wp[c]; Wn[j]=0.; Wp[c]=0.\n"
    "                                    else:   Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.\n"
    "                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n"
    "                            elif err[c]>theta and (~activa).any():\n"
    "                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])   # v10: mu normalizada a la masa del patron\n"
    "                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)\n"
    "                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n")


def v11():
    s = origen(os.path.join(ORG, 'organismo_v10.py'), '219d5033fe15b5b9')
    s = sust(s, "memoria_rechazo=20,mu_norm=True):", "memoria_rechazo=20,mu_norm=True,div_signo=True):", etiqueta='firma')
    s = sust(s, DIV_V10, DIV_V11, etiqueta='bloque de division')
    cab, cuerpo = s.split('"""\nimport numpy as np', 1)
    cab = ('"""\n'
           'Organismo v11 — CANDIDATO a tronco (congelable solo si pasa experimentos/v11_evo_division/PREREGISTRO_v11.md).\n'
           '\n'
           'v11 = v10 + REGLA DE DIVISION POR CONFLICTO DE SIGNO. Es el primer organo NACIDO POR EVOLUCION GUIADA (JUACO-EVO,\n'
           'generacion 1, operador LLM llm_2, genoma f9cce63d371977ed): una celda cuyo valor consolidado (|Wp-Wn|>0.2) recibe\n'
           'un refuerzo de signo contrario se divide en esa misma mordida; la hija nace ciega fuera de los pixeles del patron\n'
           'que la dispara (95% de la sintonia de la madre dentro de ellos), la madre NO se mueve y el valor se fisiona (la\n'
           'hija se lleva el signo nuevo, la madre conserva el viejo). La regla err>theta de v7-v10 queda detras de\n'
           'div_signo=False. Con div_signo=False es v10 exacto; con mu_norm=False y div_signo=False, v9 exacto.\n'
           'Linaje: v6 -> v7 -> v7e -> v8 (dca7d5c3a162f5d4) -> v9 (d3b72fb8819fbe8e) -> v10 (219d5033fe15b5b9) -> v11.\n'
           'Generado por experimentos/v11_evo_division/construye_v11.py. NO editar a mano.\n')
    d = os.path.join(ORG, 'organismo_v11.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + '"""\nimport numpy as np' + cuerpo)
    return d


def bateria_v11():
    s = origen(os.path.join(ORG, 'bateria_v10.py'), 'd354813d3fa9d0f1')
    s = sust(s, '"""Batería de v10 — examen de congelación', '"""Batería de v11 — examen de congelación')
    s = sust(s, "    python bateria_v8.py [semillas] [--log]        (desde organismo/)\n"
                "    --log  escribe datos/examen_v10_<fecha>.log y .json (regla 10: log desde el arranque)\n",
                "    python bateria_v11.py [semillas] [--desde N] [--log]        (desde organismo/)\n"
                "    --desde N  primera semilla (por defecto 1); el confirmatorio de v11 usa --desde 41\n"
                "    --log  escribe datos/examen_v11_<fecha>.log y .json (regla 10: log desde el arranque)\n")
    s = sust(s, 'Preregistro: experimentos/v10_direccion_division/PREREGISTRO_v10.md.',
             'Preregistro: experimentos/v11_evo_division/PREREGISTRO_v11.md.')
    s = sust(s, '       v10(mu_norm=False) == v9 en claves de v9;  7 escenarios x semillas 1..6.',
             '       v11(mu_norm=False, div_signo=False) == v9 en claves de v9, y v11(div_signo=False) == v10 en claves de v10;\n'
             '       7 escenarios x semillas 1..6 cada una.')
    s = sust(s, '  4a. [IDENTIDAD, NO EVIDENCIA — ERR-12] splits>0 <=> err_max>0.6 con celdas<90. Si falla: instrumento roto.',
             "  4a'. [IDENTIDAD, NO EVIDENCIA] cada division activa exactamente una celda: celdas == 30 + splits y\n"
             "       len(split_t) == splits, con celdas<90. (La 4a de v8-v10, splits<=>err_max>0.6, era una identidad de la\n"
             "       regla err>theta, que v11 ya no usa; se sustituye por la identidad de contabilidad, declarado en el\n"
             "       preregistro antes de correr.) Si falla: instrumento roto.")
    s = sust(s, '  6. (fuera de esta batería) organismo/bateria_v9.py 6 PASA y manifiesto.py --check.',
             '  6. (fuera de esta batería) organismo/bateria_v9.py 6 PASA y manifiesto.py --check.')
    s = sust(s, "def tarea_id(args):\n    cual, esc, seed = args\n"
                "    import organismo_v9 as ref, organismo_v10 as v10\n"
                "    a, b = ref.run(seed, **ESC_ID[esc]), v10.run(seed, mu_norm=False, **ESC_ID[esc])\n",
             "def tarea_id(args):\n    cual, esc, seed = args\n"
             "    import organismo_v11 as v11\n"
             "    if cual == 'v9':\n"
             "        import organismo_v9 as ref\n"
             "        a, b = ref.run(seed, **ESC_ID[esc]), v11.run(seed, mu_norm=False, div_signo=False, **ESC_ID[esc])\n"
             "    else:\n"
             "        import organismo_v10 as ref\n"
             "        a, b = ref.run(seed, **ESC_ID[esc]), v11.run(seed, div_signo=False, **ESC_ID[esc])\n")
    s = sust(s, "    import organismo_v10 as v10\n    r = v10.run(seed, **ETAPAS[etapa])\n",
             "    import organismo_v11 as v11\n    r = v11.run(seed, **ETAPAS[etapa])\n")
    s = sust(s, "    argv = [a for a in sys.argv[1:] if a != '--log']\n    S = int(argv[0]) if argv else 6\n    seeds = list(range(1, S + 1))\n",
             "    desde = 1\n"
             "    if '--desde' in sys.argv:\n"
             "        desde = int(sys.argv[sys.argv.index('--desde') + 1])\n"
             "    argv = [a for i, a in enumerate(sys.argv[1:], 1) if a not in ('--log', '--desde') and sys.argv[i - 1] != '--desde']\n"
             "    S = int(argv[0]) if argv else 6\n    seeds = list(range(desde, desde + S))\n")
    s = sust(s, "f'examen_v10_{stamp}.log'", "f'examen_v11_{stamp}.log'")
    s = sust(s, "prereg = os.path.join(RAIZ, 'experimentos', 'v10_direccion_division', 'PREREGISTRO_v10.md')",
             "prereg = os.path.join(RAIZ, 'experimentos', 'v11_evo_division', 'PREREGISTRO_v11.md')")
    s = sust(s, 'log(f"=== Batería v10 — CRITERIO v3, {S} semillas, Pool({N_PARALELO}) ===")',
             'log(f"=== Batería v11 — CRITERIO v3, {S} semillas ({seeds[0]}..{seeds[-1]}), Pool({N_PARALELO}) ===")')
    s = sust(s, "log(f\"sha organismo_v10 {h16(os.path.join(AQUI, 'organismo_v10.py'))}  bateria_v10",
             "log(f\"sha organismo_v11 {h16(os.path.join(AQUI, 'organismo_v11.py'))}  bateria_v11")
    s = sust(s, "for c in ('v9',) for e in ESC_ID", "for c in ('v9', 'v10') for e in ESC_ID")
    s = sust(s, "for c, nombre in (('v9', 'v10(mu_norm=False) == v9'),):",
             "for c, nombre in (('v9', 'v11(mu_norm=False, div_signo=False) == v9'), ('v10', 'v11(div_signo=False) == v10')):")
    s = sust(s, "CRITERIO 5 FALLIDO: v10 no es", "CRITERIO 5 FALLIDO: v11 no es")
    s = sust(s, "    disc = [(r['etapa'], r['seed'], r['splits'], r['err_max']) for r in con_plast if (r['splits'] > 0) != (r['err_max'] > 0.6)]\n"
                "    V['4a_identidad'] = not disc\n"
                "    log(f\"  {'OK' if not disc else 'ROTO':5s} 4a [identidad, NO evidencia] splits<=>err_max>0.6: \"\n",
             "    disc = [(r['etapa'], r['seed'], r['splits'], r['celdas'], len(r['split_t'])) for r in con_plast\n"
             "            if r['celdas'] != 30 + r['splits'] or len(r['split_t']) != r['splits']]\n"
             "    V['4a_identidad'] = not disc\n"
             "    log(f\"  {'OK' if not disc else 'ROTO':5s} 4a' [identidad, NO evidencia] celdas==30+splits y len(split_t)==splits: \"\n")
    s = sust(s, "*** 4a FALLIDA: la instrumentación", "*** 4a' FALLIDA: la instrumentación")
    s = sust(s, 'VEREDICTO bateria_v10', 'VEREDICTO bateria_v11')
    s = sust(s, "*** v10 CUMPLE EL CRITERIO v3 con 20 semillas. Por el preregistro: CONGELAR v10 como tronco (si pasa tambien Q2-Q5).",
             "*** v11 CUMPLE EL CRITERIO v3 con 20 semillas. Por el preregistro: CONGELAR v11 como tronco (si pasa tambien R y K).")
    s = sust(s, "*** v10 cumple el criterio v3 con", "*** v11 cumple el criterio v3 con")
    s = sust(s, "*** v10 NO cumple el criterio v3. No se congela; v9 sigue siendo el tronco.",
             "*** v11 NO cumple el criterio v3. No se congela; v9 sigue siendo el tronco.")
    s = sust(s, "f'examen_v10_{stamp}.json'", "f'examen_v11_{stamp}.json'")
    s = sust(s, "meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=S,",
             "meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=S, semilla_inicial=seeds[0],")
    s = sust(s, "sha_organismo_v10=h16(os.path.join(AQUI, 'organismo_v10.py')), sha_bateria_v10=h16(os.path.abspath(__file__)),",
             "sha_organismo_v11=h16(os.path.join(AQUI, 'organismo_v11.py')), sha_bateria_v11=h16(os.path.abspath(__file__)),")
    s = sust(s, "sha_preregistro=h16(prereg), sha_organismo_v9=h16(os.path.join(AQUI, 'organismo_v9.py')),",
             "sha_preregistro=h16(prereg), sha_organismo_v9=h16(os.path.join(AQUI, 'organismo_v9.py')), sha_organismo_v10=h16(os.path.join(AQUI, 'organismo_v10.py')),")
    d = os.path.join(ORG, 'bateria_v11.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(s)
    return d


def v11m():
    """Mismas anclas que construye_v10.v10m(), aplicadas a organismo_v11.py."""
    s = open(os.path.join(ORG, 'organismo_v11.py'), encoding='utf-8').read()
    s = sust(s, "memoria_rechazo=20,mu_norm=True,div_signo=True):",
             "memoria_rechazo=20,mu_norm=True,div_signo=True,fases=None,congelar=None,estado_inicial=None,heredar_patas=True,devolver_estado=False):",
             etiqueta='firma')
    ancla = ("    Wp=np.zeros(NKMAX); Wn=np.zeros(NKMAX); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; "
             "el=np.zeros_like(Wl); tr=np.zeros(9)\n")
    s = sust(s, ancla, ancla +
        "    if estado_inicial is not None:   # v11m: herencia (copias; los contadores empiezan en cero)\n"
        "        KW[:]=estado_inicial['KW']; activa[:]=estado_inicial['activa']; Wp[:]=estado_inicial['Wp']; Wn[:]=estado_inicial['Wn']\n"
        "        err[:]=estado_inicial['err']; mu[:]=estado_inicial['mu']\n"
        "        if heredar_patas: Wl[:]=estado_inicial['Wl']\n"
        "    sondas={}; codigos={}; primer={}; _t_fase=0; dq=[0]*4   # v11m: lectura\n", etiqueta='herencia')
    ancla = "        if nuevo is not None and t==nuevo_en: tipos.append(nuevo); val[nuevo]=nuevo_val\n"
    s = sust(s, ancla, ancla +
        "        if fases is not None and t in fases:   # v11m: cambio del conjunto de estimulos\n"
        "            tipos[:]=list(fases[t][0]); val.update(fases[t][1]); _t_fase=t\n"
        "            for _x in [_xx for _xx,_kz in list(objs.items()) if _kz not in tipos]: del objs[_x]; _rech.pop(_x,None)\n"
        "            spawn(); sondas[t]={_k:float((Wp-Wn)@kenyon(PAT[_k])) for _k in PAT}\n"
        "            codigos[t]={_k:sorted(int(_i) for _i in code(PAT[_k])) for _k in PAT}\n"
        "        _ap=learn and not (congelar is not None and congelar[0]<=t<congelar[1])   # v11m\n", etiqueta='fases')
    s = sust(s, "if learn:", "if _ap:", n=3, etiqueta='compuerta de aprendizaje')
    ancla = "            sobre[val[kk]][q(t)]+=1; llegadas[val[kk]][q(t)]+=int(_prev_on!=pos)\n"
    s = sust(s, ancla, ancla +
        "            if (_t_fase,kk) not in primer: primer[(_t_fase,kk)]=dict(t=t,W=float(Wb@kc),pb=float(pb),mordio=bool(mordio))   # v11m\n",
        etiqueta='primer encuentro')
    s = sust(s, "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))\n",
             "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L)); dq[q(t)]+=1\n", etiqueta='muertes por cuarto')
    s = sust(s, "if nuevo else None})",
             "if nuevo else None},sondas=sondas,codigos=codigos,primer={f'{_a}|{_b}':_v for (_a,_b),_v in primer.items()},dq=dq,"
             "estado=(dict(KW=KW.copy(),activa=activa.copy(),Wp=Wp.copy(),Wn=Wn.copy(),err=err.copy(),mu=mu.copy(),Wl=Wl.copy()) "
             "if devolver_estado else None))", etiqueta='return')
    cab = ('"""organismo_v11m = organismo/organismo_v11.py + fases de mundo (sonda de W y de CODIGOS), congelar aprendizaje,\n'
           'herencia, primer encuentro y muertes por cuarto (mismas anclas que v10m). Generado por construye_v11.py. NO editar.\n'
           'Con los valores por defecto debe ser igual al genoma evolucionado gen1/llm_2; con div_signo=False es v10m.\n'
           '"""\n')
    d = os.path.join(AQUI, 'organismo_v11m.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    return d


def caph11():
    s = origen(os.path.join(RAIZ, 'experimentos', 'v9_reverificacion', 'organismo_caph9.py'), '1b113605dc803435')
    s = sust(s, "paso=0.5,lam=0.0,memoria_rechazo=20):", "paso=0.5,lam=0.0,memoria_rechazo=20,mu_norm=False,div_signo=False):", etiqueta='firma')
    viejo = (
        "                    if plast:\n"
        "                        for c in idx:\n"
        "                            if err[c]>theta and (~activa).any():\n"
        "                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-mu[c]\n"
        "                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)\n"
        "                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n"
        "                                if t_agot is None and activa.sum()>=NKMAX: t_agot=t\n")
    nuevo = (
        "                    if plast:\n"
        "                        for c in idx:\n"
        "                            if div_signo:   # v11: conflicto de signo, hija ciega fuera de P, madre fija, fision del valor\n"
        "                                dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])\n"
        "                                kj=np.clip(KW[c]*(1-0.05)+paso*dist,0,5)*(P>0)\n"
        "                                if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():\n"
        "                                    j=int(np.where(~activa)[0][0]); activa[j]=True; KW[j]=kj\n"
        "                                    if R>0: Wp[j]=Wp[c]; Wn[j]=0.; Wp[c]=0.\n"
        "                                    else:   Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.\n"
        "                                    mu[j]=P*(float(mu[c].sum())/P.sum()); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n"
        "                                    if t_agot is None and activa.sum()>=NKMAX: t_agot=t\n"
        "                            elif err[c]>theta and (~activa).any():\n"
        "                                j=int(np.where(~activa)[0][0]); activa[j]=True; dist=P-(mu[c]*(P.sum()/max(float(mu[c].sum()),1e-9)) if mu_norm else mu[c])   # v10\n"
        "                                KW[j]=np.clip(KW[c]+paso*dist,0,5); KW[c]=np.clip(KW[c]-paso*dist,0,5)\n"
        "                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n"
        "                                if t_agot is None and activa.sum()>=NKMAX: t_agot=t\n")
    s = sust(s, viejo, nuevo, etiqueta='bloque de division caph')
    cab = ('"""organismo_caph11 = organismo_caph9.py (1b113605dc803435) + mu_norm (v10) + div_signo (v11). Generado por\n'
           'construye_v11.py. NO editar. Con mu_norm=False y div_signo=False es organismo_caph9 (control KK1)."""\n')
    d = os.path.join(AQUI, 'organismo_caph11.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    return d


if __name__ == '__main__':
    for f in (v11, bateria_v11, v11m, caph11):
        d = f()
        print(f"  {os.path.relpath(d, RAIZ):55s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
