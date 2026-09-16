"""Genera los dos organismos de la prueba de ahorro por parcheo con anclas.

No se escriben a mano: se derivan de los archivos de origen con sustituciones exactas, y cada ancla
tiene que aparecer EXACTAMENTE una vez o el script aborta. Asi el diff es demostrablemente minimo.

  organismo_v6s.py  <- organismo/organismo_v6.py            (5f38f83cf49248a3)  + instrumentacion 3 fases
  organismo_v7g.py  <- experimentos/bug01/organismo_v7e.py  (3118c6d563542da2)  + piso + instrumentacion

La correccion de ambos la demuestra el control 1 de corre_ahorro.py (bit-identidad con el original
cuando los parametros nuevos estan en su valor neutro), no este script.

Uso:  python experimentos/bug01/construye_ahorro.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))

# --------------------------------------------------------------------------------------------------
# Los cinco bloques de instrumentacion. Identicos para los dos organismos salvo donde se indica.
# --------------------------------------------------------------------------------------------------

CONTADORES = ("    nB=0; nB3=0; n1=None; n3=None; wB_ext=None; wB_pre=None; wB_post=None"
              "   # <-- prueba de ahorro\n")

FASES = """        if revertir_en is not None and t==revertir_en: val={'A':'comida','B':'veneno'}; wB_ext=float((Wp-Wn)@kenyon(PAT['B']))
        if sin_B is not None and t==sin_B[0]:
            wB_pre=float((Wp-Wn)@kenyon(PAT['B'])); tipos=[z for z in tipos if z!='B']
            for z in [z for z,kz in list(objs.items()) if kz=='B']: del objs[z]
            spawn()
        if sin_B is not None and t==sin_B[1]:
            wB_post=float((Wp-Wn)@kenyon(PAT['B']))
            if 'B' not in tipos: tipos.append('B')
"""

CUENTA_B = """                if kk=='B':
                    nB+=1; wb=float((Wp-Wn)@kenyon(PAT['B']))
                    if revertir_en is not None and t>=revertir_en: nB3+=1
                    if n1 is None and (invertir_en is None or t<invertir_en) and wb<=crit_miedo: n1=nB
                    if n3 is None and revertir_en is not None and t>=revertir_en and wb<=crit_miedo: n3=nB3
"""

CLAVES = "nB=nB,nB3=nB3,n1=n1,n3=n3,wB_ext=wB_ext,wB_pre=wB_pre,wB_post=wB_post,"

ANCLA_CONTADORES = "    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}\n"
ANCLA_INVERTIR = "        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}\n"


def sustituye(texto, viejo, nuevo, etiqueta):
    n = texto.count(viejo)
    if n != 1:
        raise SystemExit(f"ANCLA {etiqueta}: aparece {n} veces, se esperaba 1. Abortado.")
    return texto.replace(viejo, nuevo)


def h16(ruta):
    return hashlib.sha256(open(ruta, 'rb').read()).hexdigest()[:16]


# --------------------------------------------------------------------------------------------------
# v6s = v6 + instrumentacion
# --------------------------------------------------------------------------------------------------
def construye_v6s():
    src = open(os.path.join(RAIZ, 'organismo', 'organismo_v6.py'), encoding='utf-8').read()

    src = sustituye(src, "costo=.002,nobj=4,log_cada=None):",
                    "costo=.002,nobj=4,log_cada=None,revertir_en=None,sin_B=None,crit_miedo=-2.5):",
                    "firma v6")
    src = sustituye(src, ANCLA_CONTADORES, ANCLA_CONTADORES + CONTADORES, "contadores v6")
    src = sustituye(src, ANCLA_INVERTIR, ANCLA_INVERTIR + FASES, "fases v6")
    # en v6 el bloque `if learn:` termina en la linea del canal aversivo: se inserta justo despues.
    ancla = "                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)\n"
    src = sustituye(src, ancla, ancla + CUENTA_B, "cuenta_B v6")
    src = sustituye(src, "    return dict(mord=mord,", "    return dict(" + CLAVES + "mord=mord,",
                    "return v6")

    cab = ('"""organismo_v6s = organismo_v6.py (5f38f83cf49248a3) + instrumentacion de 3 fases.\n'
           'Generado por construye_ahorro.py. NO editar a mano.\n'
           'Con revertir_en=None y sin_B=None es bit-identico a v6 (control 1 de corre_ahorro.py).\n'
           'Preregistro: PREREGISTRO_ahorro.md\n'
           '"""\n')
    dst = os.path.join(AQUI, 'organismo_v6s.py')
    open(dst, 'w', encoding='utf-8', newline='\n').write(cab + src)
    return dst


# --------------------------------------------------------------------------------------------------
# v7g = v7e + piso + instrumentacion
# --------------------------------------------------------------------------------------------------
def construye_v7g():
    src = open(os.path.join(AQUI, 'organismo_v7e.py'), encoding='utf-8').read()

    src = sustituye(src, "solap_AB=None,lam=0.0):",
                    "solap_AB=None,lam=0.0,piso=0.0,revertir_en=None,sin_B=None,crit_miedo=-2.5):",
                    "firma v7g")
    # piso: se decae solo el EXCESO de la parte comun sobre el piso. Con piso=0 es identico a v7e.
    src = sustituye(
        src,
        "if lam: ix=kc>0; mcom=np.minimum(Wp[ix],Wn[ix]); Wp[ix]-=lam*mcom; Wn[ix]-=lam*mcom   "
        "# BUG-01 exp2: decae solo la parte comun",
        "if lam: ix=kc>0; mcom=np.maximum(np.minimum(Wp[ix],Wn[ix])-piso,0.0); Wp[ix]-=lam*mcom; "
        "Wn[ix]-=lam*mcom   # BUG-01: decae el EXCESO de la parte comun sobre el piso",
        "piso v7g")
    src = sustituye(src, ANCLA_CONTADORES, ANCLA_CONTADORES + CONTADORES, "contadores v7g")
    src = sustituye(src, ANCLA_INVERTIR, ANCLA_INVERTIR + FASES, "fases v7g")
    # en v7e, despues del canal aversivo viene el bloque `if plast:`. La cuenta va al FINAL de
    # `if mordio:`, es decir tras la ultima linea de la division.
    ancla = ("                                Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); "
             "err[c]=err[j]=0; splits+=1; split_t.append((t,kk))\n")
    src = sustituye(src, ancla, ancla + CUENTA_B, "cuenta_B v7g")
    src = sustituye(src, "    return dict(split_t=split_t,", "    return dict(" + CLAVES + "split_t=split_t,",
                    "return v7g")

    cab = ('"""organismo_v7g = organismo_v7e.py (3118c6d563542da2) + piso del decaimiento + 3 fases.\n'
           'Generado por construye_ahorro.py. NO editar a mano.\n'
           'Con lam=0 es bit-identico a v7; con piso=0 el decaimiento es identico al del exp. 2.\n'
           'Preregistro: PREREGISTRO_ahorro.md\n'
           '"""\n')
    dst = os.path.join(AQUI, 'organismo_v7g.py')
    open(dst, 'w', encoding='utf-8', newline='\n').write(cab + src)
    return dst


if __name__ == '__main__':
    for f in (construye_v6s, construye_v7g):
        dst = f()
        n = sum(1 for _ in open(dst, encoding='utf-8'))
        print(f"  {os.path.basename(dst):20s} {h16(dst)}  {n} lineas")
    print("\nGenerados. Su correccion la demuestra el control 1 de corre_ahorro.py, no este script.")
