"""Genera organismo_v8p.py = organismo/organismo_v8.py (congelado) + contadores de la frontera hambre-supervivencia.

Preregistro: PREREGISTRO_frontera_hambre.md (sha 902f1f0223ef597b), commiteado ANTES que este script.
Anclas unicas, origen comprobado por sha. Solo contadores de lectura (sin RNG, sin estado del organismo):
  VH, MH, PH  visitas, mordidas y suma de pb por valencia vigente x 5 tramos de hambre, en t >= T/2
  dq          muertes por cuarto
  t_ext       primer paso tras la inversion con W_B >= 0 despues de una mordida de B
Su correccion la demuestra F0 de corre_frontera_hambre.py (v8p == v8, y reproduce el examen de v8).
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'organismo', 'organismo_v8.py')
SHA_ORIGEN = 'dca7d5c3a162f5d4'
DESTINO = os.path.join(AQUI, 'organismo_v8p.py')


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

    # 4 espacios, cuerpo de run()
    ancla = "    err_max=0.0; t_conflicto=None; t_techo=None; n_techo=0   # instrumentacion v8, solo lectura\n"
    src = sustituye(src, ancla, ancla +
        "    VH={'veneno':[0]*5,'comida':[0]*5}; MH={'veneno':[0]*5,'comida':[0]*5}; PH={'veneno':[0.0]*5,'comida':[0.0]*5}"
        "; dq=[0]*4; t_ext=None   # frontera hambre (lectura)\n", "contadores")

    # 12 espacios, dentro de `if pos in objs:`, tras contar la visita (pb y hambre ya calculados en este paso)
    ancla = "            vis[kk][q(t)]+=1\n"
    src = sustituye(src, ancla, ancla +
        "            if t>=T//2: _b=min(int(hambre*5),4); VH[val[kk]][_b]+=1; PH[val[kk]][_b]+=float(pb)\n", "visitas")

    # 16 espacios, dentro de `if mordio:`; val[kk] es la valencia vigente de esta mordida
    ancla = "                R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n"
    src = sustituye(src, ancla, ancla +
        "                if t>=T//2: MH[val[kk]][min(int(hambre*5),4)]+=1\n", "mordidas")

    # 16 espacios tras la ULTIMA linea de la division (32 esp.): cierra for/if plast/if learn, queda en `if mordio:`
    ancla = ("                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); err[c]=err[j]=0; splits+=1; "
             "split_t.append((t,kk))\n")
    src = sustituye(src, ancla, ancla +
        "                if invertir_en is not None and t>=invertir_en and t_ext is None and kk=='B' and "
        "float((Wp-Wn)@kenyon(PAT['B']))>=0: t_ext=t\n", "t_ext")

    src = sustituye(src, "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))\n",
                    "        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L)); dq[q(t)]+=1\n", "muertes por cuarto")

    src = sustituye(src, "    return dict(err_max=err_max,", "    return dict(VH=VH,MH=MH,PH=PH,dq=dq,t_ext=t_ext,err_max=err_max,",
                    "return")

    cab = ('"""organismo_v8p = organismo/organismo_v8.py (dca7d5c3a162f5d4) + contadores de la frontera hambre-supervivencia.\n'
           'Generado por construye_v8p.py. NO editar a mano. Mismo organismo (F0).\n'
           'Preregistro: experimentos/etapa2_politica/PREREGISTRO_frontera_hambre.md (902f1f0223ef597b)\n'
           '"""\n')
    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(cab + src)
    print(f"  organismo_v8p.py  {h16(DESTINO)}  {sum(1 for _ in open(DESTINO, encoding='utf-8'))} lineas")
