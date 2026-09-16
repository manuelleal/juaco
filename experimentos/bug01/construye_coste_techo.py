"""Genera los dos organismos de la prueba de coste con el techo mordiendo, por parcheo con anclas.

Preregistro: PREREGISTRO_coste_techo.md (sha e0e2709f71dff15f), escrito y commiteado ANTES que este script.
No se escriben a mano: cada ancla tiene que aparecer EXACTAMENTE una vez o el script aborta.

  organismo_v7h.py   <- experimentos/bug01/organismo_v7e.py              (3118c6d563542da2)
                        + invertir_cada + contadores por fase + mordida del techo (sec. 2 del preregistro)
  organismo_caph.py  <- experimentos/ramas/2Kbis_capacidad/organismo_cap.py (dc058e0a43216bf3)
                        + lam con la linea de drenaje LITERAL de v7e + mordida del techo + mordidas veneno/comida

INDENTACION (leccion de T02): cada bloque insertado declara abajo en que bloque queda y por que.
La correccion la demuestra el control 1 de corre_coste_techo.py (bit-identidad con el original en valor
neutro), no este script.

Uso:  python experimentos/bug01/construye_coste_techo.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))

ESPERADO = {'organismo_v7e.py': '3118c6d563542da2', 'organismo_cap.py': 'dc058e0a43216bf3'}

# Linea de drenaje de v7e, literal. Se copia tal cual a caph.
DRENAJE = ("                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom"
           "   # BUG-01 exp2: decae solo la parte comun\n")

# Mordida del techo (sec. 2): despues del drenaje, antes del clip, solo lectura. 20 espacios = dentro de
# `if learn:` (16), al mismo nivel que `dlt=R-Wb@kc`. Registra fase en v7h; en caph no hay fases.
def techo_bloque(con_fase):
    donde = 'fase' if con_fase else 't'
    return ("                    _ix=kc>0\n"
            "                    if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())\n"
            "                    else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())\n"
            "                    if _trunca:\n"
            "                        n_techo+=1\n"
            "                        if t_techo is None: t_techo=t; techo_primero=(kk,'Wp' if dlt>0 else 'Wn',"
            + donde + ")\n")


def sustituye(texto, viejo, nuevo, etiqueta):
    n = texto.count(viejo)
    if n != 1:
        raise SystemExit(f"ANCLA {etiqueta}: aparece {n} veces, se esperaba 1. Abortado.")
    return texto.replace(viejo, nuevo)


def h16(ruta):
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()[:16]


def comprueba_origen(ruta):
    real, esp = h16(ruta), ESPERADO[os.path.basename(ruta)]
    if real != esp:
        raise SystemExit(f"ORIGEN {ruta}: sha {real}, se esperaba {esp}. Abortado.")


# --------------------------------------------------------------------------------------------------
# v7h = v7e + inversiones seriadas + contadores por fase + mordida del techo
# --------------------------------------------------------------------------------------------------
def construye_v7h():
    org = os.path.join(AQUI, 'organismo_v7e.py')
    comprueba_origen(org)
    src = open(org, encoding='utf-8').read()

    src = sustituye(src, "solap_AB=None,lam=0.0):",
                    "solap_AB=None,lam=0.0,invertir_cada=None,crit_v=-2.5,crit_c=0.5):", "firma v7h")

    # contadores: 4 espacios, cuerpo de run(), tras la linea de estado inicial.
    ancla = "    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}\n"
    src = sustituye(src, ancla, ancla +
        "    fase=0; NF=1 if not invertir_cada else -(-T//invertir_cada)   # <-- prueba de coste (techo)\n"
        "    FS={_k:dict(mord=[0]*NF,vis=[0]*NF,mv=[0]*NF,mc=[0]*NF,n=[None]*NF,W=[None]*NF) for _k in PAT}; dfase=[0]*NF\n"
        "    t_techo=None; techo_primero=None; n_techo=0; mv_tot=0; mc_tot=0; err_max=0.0\n",
        "contadores v7h")

    # inversion seriada: 8 espacios, dentro del for t, justo tras la inversion unica existente.
    ancla = "        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}\n"
    src = sustituye(src, ancla, ancla +
        "        if invertir_cada and t>0 and t%invertir_cada==0:\n"
        "            for _k in ('A','B'): FS[_k]['W'][fase]=float((Wp-Wn)@kenyon(PAT[_k]))\n"
        "            fase+=1; val={_k:('veneno' if _v=='comida' else 'comida') for _k,_v in val.items()}\n",
        "inversion seriada v7h")

    # visitas por fase: 12 espacios, dentro de `if pos in objs:`.
    ancla = "            vis[kk][q(t)]+=1\n"
    src = sustituye(src, ancla, ancla + "            FS[kk]['vis'][fase]+=1\n", "visitas v7h")

    # mordidas por fase: 16 espacios, dentro de `if mordio:`, tras contar la mordida original.
    ancla = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n"
    src = sustituye(src, ancla, ancla +
        "                FS[kk]['mord'][fase]+=1\n"
        "                if val[kk]=='veneno': mv_tot+=1; FS[kk]['mv'][fase]+=1\n"
        "                else: mc_tot+=1; FS[kk]['mc'][fase]+=1\n",
        "mordidas v7h")

    # mordida del techo: tras el drenaje, antes del clip (20 espacios, dentro de `if learn:`).
    src = sustituye(src, DRENAJE, DRENAJE + techo_bloque(con_fase=True), "techo v7h")

    # err_max: 24 espacios, dentro de `if plast:`, justo tras actualizar err (antes de que una division lo ponga a 0).
    ancla = ("                        P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); "
             "mu[idx]=(1-ema)*mu[idx]+ema*P\n")
    src = sustituye(src, ancla, ancla + "                        err_max=max(err_max,float(err[idx].max()))\n",
                    "err_max v7h")

    # criterio por fase: 16 espacios tras la ULTIMA linea de la division (32 espacios). A 16 espacios se cierran
    # `for c`, `if plast:` e `if learn:` y la linea queda dentro de `if mordio:` (12). Es lo que se quiere:
    # se lee W DESPUES de la actualizacion y de las divisiones de esta mordida. (T02 fallo justo aqui.)
    ancla = ("                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); "
             "err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n")
    src = sustituye(src, ancla, ancla +
        "                if FS[kk]['n'][fase] is None:\n"
        "                    _w=float((Wp-Wn)@kenyon(PAT[kk]))\n"
        "                    if (val[kk]=='veneno' and _w<=crit_v) or (val[kk]=='comida' and _w>=crit_c): "
        "FS[kk]['n'][fase]=FS[kk]['mord'][fase]\n",
        "criterio v7h")

    # muertes por fase: se sustituye la linea entera (el E=.6 de la misma linea impide contar despues).
    src = sustituye(src, "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))\n",
                    "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L)); dfase[fase]+=1\n", "muertes v7h")

    # W al final de la ultima fase: 4 espacios, tras el bucle.
    ancla = "    W={k:round(float((Wp-Wn)@kenyon(PAT[k])),2) for k in PAT}\n"
    src = sustituye(src, ancla,
        "    for _k in ('A','B'): FS[_k]['W'][fase]=float((Wp-Wn)@kenyon(PAT[_k]))\n" + ancla, "W final v7h")

    src = sustituye(src, "    return dict(split_t=split_t,",
        "    return dict(fases=FS,dfase=dfase,t_techo=t_techo,techo_primero=techo_primero,n_techo=n_techo,"
        "mv_tot=mv_tot,mc_tot=mc_tot,err_max=err_max,split_t=split_t,", "return v7h")

    cab = ('"""organismo_v7h = organismo_v7e.py (3118c6d563542da2) + inversiones seriadas + contadores por fase\n'
           '+ mordida del techo (truncacion del clip). Generado por construye_coste_techo.py. NO editar a mano.\n'
           'Con invertir_cada=None es v7e; con ademas lam=0 es v7 (control 1 de corre_coste_techo.py).\n'
           'Preregistro: PREREGISTRO_coste_techo.md (e0e2709f71dff15f)\n'
           '"""\n')
    dst = os.path.join(AQUI, 'organismo_v7h.py')
    open(dst, 'w', encoding='utf-8', newline='\n').write(cab + src)
    return dst


# --------------------------------------------------------------------------------------------------
# caph = cap + lam (linea literal de v7e) + mordida del techo + mordidas de veneno/comida
# --------------------------------------------------------------------------------------------------
def construye_caph():
    org = os.path.join(RAIZ, 'experimentos', 'ramas', '2Kbis_capacidad', 'organismo_cap.py')
    comprueba_origen(org)
    src = open(org, encoding='utf-8').read()

    src = sustituye(src, "        plast=True,theta=0.6,ema=0.02,paso=0.5):",
                    "        plast=True,theta=0.6,ema=0.02,paso=0.5,lam=0.0):", "firma caph")

    ancla = "    hist=[]; t_agot=None; chk=set(chk or [])\n"
    src = sustituye(src, ancla, ancla +
        "    t_techo=None; techo_primero=None; n_techo=0; mv_tot=0; mc_tot=0   # <-- prueba de coste (techo)\n",
        "contadores caph")

    # 16 espacios, dentro de `if mordio:`.
    ancla = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1; morc[kk]+=1\n"
    src = sustituye(src, ancla, ancla +
        "                if val[kk]=='veneno': mv_tot+=1\n"
        "                else: mc_tot+=1\n", "mordidas caph")

    # drenaje + techo: 20 espacios, dentro de `if learn:`, tras calcular dlt y antes del clip. Mismo sitio que v7e.
    ancla = "                    dlt=R-Wb@kc\n"
    src = sustituye(src, ancla, ancla + DRENAJE + techo_bloque(con_fase=False), "drenaje+techo caph")

    src = sustituye(src, "val=dict(val))",
        "val=dict(val),t_techo=t_techo,techo_primero=techo_primero,n_techo=n_techo,mv_tot=mv_tot,mc_tot=mc_tot)",
        "return caph")

    cab = ('"""organismo_caph = organismo_cap.py (dc058e0a43216bf3) + lam (drenaje de la parte comun, linea literal\n'
           'de organismo_v7e.py) + mordida del techo + mordidas de veneno/comida. Generado por construye_coste_techo.py.\n'
           'NO editar a mano. Con lam=0 es organismo_cap (control 1 de corre_coste_techo.py).\n'
           'Preregistro: PREREGISTRO_coste_techo.md (e0e2709f71dff15f)\n'
           '"""\n')
    dst = os.path.join(AQUI, 'organismo_caph.py')
    open(dst, 'w', encoding='utf-8', newline='\n').write(cab + src)
    return dst


if __name__ == '__main__':
    for f in (construye_v7h, construye_caph):
        dst = f()
        n = sum(1 for _ in open(dst, encoding='utf-8'))
        print(f"  {os.path.basename(dst):20s} {h16(dst)}  {n} lineas")
    print("\nGenerados. Su correccion la demuestra el control 1 de corre_coste_techo.py, no este script.")
