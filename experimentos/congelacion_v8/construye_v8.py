"""Genera organismo/organismo_v8.py por parcheo con anclas desde experimentos/bug01/organismo_v7e.py.

Preregistro: experimentos/congelacion_v8/PREREGISTRO_congelacion_v8.md (sha d2924e69128fe0f6), commiteado ANTES.
Cada ancla tiene que aparecer EXACTAMENTE una vez o el script aborta. El origen se comprueba por sha.

v8 = v7e con lam=0.05 POR DEFECTO (unico cambio de comportamiento) + instrumentacion de solo lectura:
  err_max      tras actualizar err, antes de dividir (24 esp., dentro de `if plast:`)
  t_conflicto  primer paso con min(Wp,Wn)>0 en una celda del codigo mordido tras actualizar (20 esp., en `if learn:`)
  t_techo, n_techo  mordida del techo = truncacion del clip, igual que en la prueba de coste (20 esp., en `if learn:`)
Ninguna linea nueva llama al RNG ni escribe estado del organismo.

La correccion la demuestra el criterio 5 de bateria_v8.py (v8 == v7e(lam=0.05) y v8(lam=0) == v7), no este script.

Uso:  python experimentos/congelacion_v8/construye_v8.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'bug01', 'organismo_v7e.py')
SHA_ORIGEN = '3118c6d563542da2'
DESTINO = os.path.join(RAIZ, 'organismo', 'organismo_v8.py')


def h16(ruta):
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()[:16]


def sustituye(texto, viejo, nuevo, etiqueta):
    n = texto.count(viejo)
    if n != 1:
        raise SystemExit(f"ANCLA {etiqueta}: aparece {n} veces, se esperaba 1. Abortado.")
    return texto.replace(viejo, nuevo)


if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN {ORIGEN}: sha {h16(ORIGEN)}, se esperaba {SHA_ORIGEN}. Abortado.")
    src = open(ORIGEN, encoding='utf-8').read()

    # 1. el unico cambio de comportamiento
    src = sustituye(src, "solap_AB=None,lam=0.0):", "solap_AB=None,lam=0.05):", "firma lam=0.05")

    # 2. contadores: 4 espacios, cuerpo de run()
    ancla = "    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}\n"
    src = sustituye(src, ancla, ancla + "    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura\n",
                    "contadores")

    # 3. mordida del techo: tras el drenaje y antes del clip, 20 espacios = dentro de `if learn:`
    ancla = ("                    if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom"
             "   # BUG-01 exp2: decae solo la parte comun\n")
    src = sustituye(src, ancla, ancla +
        "                    _ix=kc>0\n"
        "                    if dlt>0: _trunca=bool(((Wp[_ix]+eta*dlt)>3.0).any())\n"
        "                    else:     _trunca=bool(((Wn[_ix]+eta*aversion*(-dlt))>3.0).any())\n"
        "                    if _trunca:\n"
        "                        n_techo+=1\n"
        "                        if t_techo is None: t_techo=t\n", "techo")

    # 4. conflicto: justo tras la actualizacion de canales, 20 espacios = dentro de `if learn:`, antes de `if plast:`
    ancla = "                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)\n"
    src = sustituye(src, ancla, ancla +
        "                    if t_conflicto is None and bool((np.minimum(Wp[_ix],Wn[_ix])>0).any()): t_conflicto=t\n",
        "conflicto")

    # 5. err_max: 24 espacios, dentro de `if plast:`, tras actualizar err y antes del bucle de division
    ancla = ("                        P=PAT[kk]; idx=np.where(kc>0)[0]; err[idx]=(1-ema)*err[idx]+ema*abs(dlt); "
             "mu[idx]=(1-ema)*mu[idx]+ema*P\n")
    src = sustituye(src, ancla, ancla + "                        err_max=max(err_max,float(err[idx].max()))\n",
                    "err_max")

    # 6. salida
    src = sustituye(src, "    return dict(split_t=split_t,",
                    "    return dict(err_max=err_max,t_conflicto=t_conflicto,t_techo=t_techo,n_techo=n_techo,split_t=split_t,",
                    "return")

    cab = ('"""\n'
           'Organismo v8 — TRONCO candidato (congelable sólo si pasa organismo/bateria_v8.py 20, criterio v3).\n'
           '\n'
           'v8 = v6 + 2L (plasticidad estructural) + drenaje de la parte común de Wp/Wn con lam=0.05.\n'
           'Linaje: organismo_v6.py (5f38f83cf49248a3) -> v7c (212f0746d52577c7) -> v7 (3db0475ef0ea95ce)\n'
           '        -> experimentos/bug01/organismo_v7e.py (3118c6d563542da2) -> v8 (este archivo).\n'
           'Generado por experimentos/congelacion_v8/construye_v8.py. NO editar a mano.\n'
           '\n'
           'Único cambio de comportamiento respecto de v7e: lam=0.05 por defecto. Con lam=0 es v7 exacto.\n'
           'El drenaje resta lam*min(Wp,Wn) a los dos canales al morder: Wp-Wn queda intacto, así que el valor\n'
           'y la conducta son idénticos a v7 hasta la primera truncación del clip (prueba de coste, S0/C0 20/20),\n'
           'y a partir de ahí v8 sigue aprendiendo donde v7 se bloquea (BUG-01).\n'
           '\n'
           'Instrumentación de sólo lectura (no toca RNG ni estado): err_max, t_conflicto, t_techo, n_techo.\n'
           'OJO (ERR-12): splits>0 <=> err_max>0.6 es una IDENTIDAD del código mientras haya celdas libres.\n'
           'Preregistro: experimentos/congelacion_v8/PREREGISTRO_congelacion_v8.md (d2924e69128fe0f6).\n'
           '"""\n')
    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(cab + src)
    n = sum(1 for _ in open(DESTINO, encoding='utf-8'))
    print(f"  organismo/organismo_v8.py  {h16(DESTINO)}  {n} lineas")
    print("\nGenerado. Su correccion la demuestra el criterio 5 de bateria_v8.py, no este script.")
