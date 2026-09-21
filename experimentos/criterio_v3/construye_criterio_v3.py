"""A-CAL (criterio v3, ERR-91) — CONSTRUCTOR POR ANCLAS del paquete de calibracion. No corre nada.

MISION: llegar a la AGI por este camino. Este bloque NO juzga un mecanismo del organismo: juzga el INSTRUMENTO
que juzga a los mecanismos. Mide con que probabilidad la letra del CRITERIO DE TRONCO (v2 y v3) deja pasar a un
PLACEBO (un candidato cuya ley es exactamente la del tronco) y rechaza a un candidato PEOR por un margen declarado.

QUE SE CONSTRUYE (los originales SOLO se leen; el sha se verifica antes de escribir nada):

  organismo_v3cal.py   <- experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py  (96feb4918dc5d694)
        cadena: organismo_vivo_rep (aa823d56c2d4213c) <- organismo_vivo (20c0961c79de8825) <- organismo/organismo_v14.py
        (feefc88b1fd8d434, v14.1 CONGELADO).  SE LE ANADE, por anclas, SOLO TRES COSAS:
          (1) B-5 `desambiguar` (el organo de v14.2), con el MISMO texto que experimentos/creacion_B/construye_codigo.py
              y que experimentos/tronco_v15_dE5/construye_v15_dE5.py (COND_A->COND_B, FIS_VA->FIS_VB, literales).
              POR DEFECTO `desambiguar=1`, como el TRONCO v14.2 (organismo/organismo_v142.py, 17528d767fcebaf6).
          (2) `invertir_vivo_en` (la reversion del mundo vivo, T-C ii): en t se intercambian los EFECTOS de comida y
              veneno. Mismo texto que construye_v15_dE5.py. Inerte por defecto (None).
          (3) LA PERILLA DEL BLOQUE: `placebo = k` (entero >= 0). Consume k sorteos del MISMO generador por paso y
              DESCARTA el valor: ninguna decision los mira. Es la definicion operativa de "candidato cuya ley es la
              del tronco": la trayectoria cambia (el flujo de numeros se desplaza) y la LEY no.
        NO se anade ningun mecanismo, ninguna memoria, ninguna estructura. Memoria nueva: CERO.

  El brazo PEOR no necesita perilla nueva: usa `costo` y `costo_a`, que YA son argumentos del tronco (el coste de
  vida del mundo vivo, 0.001 en mini_vivo.CUERPO). PEOR = el mismo organismo con coste de vida mayor.

IDENTIDAD (arnes: identidad_criterio_v3.py):
  placebo=0, desambiguar=1, vivo=0, n_nec=1, reproduccion=0, rep2=0  ->  organismo/organismo_v142.py BIT A BIT.
  placebo=0, desambiguar=0                                           ->  organismo_vivo_rep2.py BIT A BIT.
  CONTROL QUE DEBE DIFERIR: placebo=1 != placebo=0 en la trayectoria.

Uso:  python experimentos/criterio_v3/construye_criterio_v3.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
NIV11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')

SHA = {   # tripwire: si un origen cambia, se aborta sin escribir nada
    os.path.join(NIV11, 'organismo_vivo_rep2.py'): '96feb4918dc5d694',
    os.path.join(NIV11, 'organismo_vivo_rep.py'): 'aa823d56c2d4213c',
    os.path.join(NIV11, 'organismo_vivo.py'): '20c0961c79de8825',
    os.path.join(ORG, 'organismo_v142.py'): '17528d767fcebaf6',
    os.path.join(ORG, 'organismo_v14.py'): 'feefc88b1fd8d434',
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(ruta):
    s = h16(ruta)
    esperado = SHA.get(ruta)
    if esperado is not None and s != esperado:
        raise SystemExit(f'*** ORIGEN {ruta}: sha {s}, se esperaba {esperado}. No se escribe nada.')
    return open(ruta, 'rb').read().decode('utf-8'), s


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


# ---------------------------------------------------------------- B-5 (texto LITERAL de creacion_B/construye_codigo.py)
COND_A = "if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():"
COND_B = ("if (Wb[c]*R<0 or (desambiguar and R==0)) and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():"
          "   # B-5 DESAMBIGUAR: tambien divide cuando una celda consolidada, bajo una retina distinta (kj@P>KW[c]@P), recibe R==0")
FIS_VA = ("                                    if R>0: Wp[_nm,j]=Wp[_nm,c]; Wn[_nm,j]=0.; Wp[_nm,c]=0.\n"
          "                                    else:   Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.\n")
FIS_VB = ("                                    if R>0: Wp[_nm,j]=Wp[_nm,c]; Wn[_nm,j]=0.; Wp[_nm,c]=0.\n"
          "                                    elif R<0: Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.\n"
          "                                    else: Wp[_nm,j]=0.; Wn[_nm,j]=0.; _ndes+=1; _des_t.append((t,kk))   # B-5: con R==0 la hija nace SIN valor en la necesidad activa (las otras se heredan abajo) y la madre conserva el suyo\n")


def pon(src):
    # 1) firma: B-5 (defecto 1, como el TRONCO v14.2) + la reversion del mundo vivo + LA PERILLA placebo
    out = sust(src, ",rep2=0,rep2_regalo=600):", ",rep2=0,rep2_regalo=600,desambiguar=1,invertir_vivo_en=None,placebo=0):", etq='firma')
    # 1b) la perilla es un entero >= 0 y se valida al arrancar (nunca un float, nunca negativo)
    out = sust(out, "    rng=np.random.default_rng(seed)\n",
               "    placebo=int(placebo)\n"
               "    if placebo<0: raise SystemExit('PLACEBO: k debe ser un entero >= 0')\n"
               "    rng=np.random.default_rng(seed)\n", etq='placebo: validacion')
    # 2) estado: contadores de B-5 (solo lectura)
    A = "    Wp=np.zeros((n_nec,NKMAX)); Wn=np.zeros((n_nec,NKMAX)); err=np.zeros(NKMAX); mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)"
    out = sust(out, A, A.replace("splits=0;", "splits=0; _ndes=0; _des_t=[];"), etq='estado')
    # 3) B-5: la condicion y la fision (texto literal)
    out = sust(out, COND_A, COND_B, etq='B-5 condicion')
    out = sust(out, FIS_VA, FIS_VB, etq='B-5 fision')
    # 4) LA PERILLA: k sorteos por paso, DESCARTADOS. Primera sentencia del bucle, antes de cualquier decision.
    out = sust(out, "    for t in range(T):\n",
               "    for t in range(T):\n"
               "        for _ in range(placebo): rng.random()   # PLACEBO (criterio v3, A-CAL): consume k sorteos por paso y DESCARTA el valor. Ninguna decision los mira: la LEY no cambia, la TRAYECTORIA si. placebo=0 -> el tronco BIT A BIT\n",
               etq='placebo: sorteos')
    # 5) T-C (ii) en el mundo vivo: los EFECTOS de comida y veneno se intercambian en t (texto de construye_v15_dE5.py)
    A = "        if invertir_en is not None and t==invertir_en: val={'A':'veneno','B':'comida'}\n"
    out = sust(out, A, A + "        if invertir_vivo_en is not None and t==invertir_vivo_en: _EF=dict(_EF,comida=_EF['veneno'],veneno=_EF['comida'])   # T-C vivo: la comida pasa a quitar energia y el veneno a darla\n",
               etq='invertir_vivo')
    # 6) return: las claves nuevas (todas de solo lectura o ecos del argumento)
    out = sust(out, "    return dict(sobre=sobre,",
               "    return dict(desambiguar=desambiguar,des_splits=_ndes,des_t=_des_t,"
               "invertir_vivo_en=invertir_vivo_en,placebo=placebo,sobre=sobre,", etq='return')
    return out


if __name__ == '__main__':
    src, s0 = origen(os.path.join(NIV11, 'organismo_vivo_rep2.py'))
    _, s_rep = origen(os.path.join(NIV11, 'organismo_vivo_rep.py'))
    _, s_vivo = origen(os.path.join(NIV11, 'organismo_vivo.py'))
    _, s142 = origen(os.path.join(ORG, 'organismo_v142.py'))
    _, s14 = origen(os.path.join(ORG, 'organismo_v14.py'))
    txt = pon(src)
    cab = (f'"""organismo_v3cal = experimentos/nivel11_mundo_vivo/organismo_vivo_rep2.py ({s0}; SOLO se leyo; cadena\n'
           f'organismo_vivo_rep {s_rep} <- organismo_vivo {s_vivo} <- organismo/organismo_v14.py {s14} = v14.1)\n'
           f'+ B-5 `desambiguar` (el organo de v14.2, texto literal; por defecto 1, como el TRONCO organismo_v142 {s142})\n'
           f'+ `invertir_vivo_en` (la reversion del mundo vivo, T-C ii)\n'
           f'+ `placebo = k`: consume k sorteos del MISMO rng por paso y DESCARTA el valor (LA PERILLA DEL BLOQUE A-CAL).\n'
           f'  placebo=0, desambiguar=1, vivo=0, n_nec=1  ->  organismo/organismo_v142.py BIT A BIT (claves de v14.2)\n'
           f'  placebo=0, desambiguar=0                   ->  organismo_vivo_rep2.py BIT A BIT (claves de rep2)\n'
           f'  placebo=1                                  ->  DEBE diferir de placebo=0 (control del arnes)\n'
           f'El brazo PEOR no usa perilla nueva: `costo`/`costo_a` ya son argumentos del tronco.\n'
           f'Memoria nueva: CERO. Arnes: identidad_criterio_v3.py. Generado por construye_criterio_v3.py. NO editar a mano."""\n')
    ruta = os.path.join(AQUI, 'organismo_v3cal.py')
    open(ruta, 'w', encoding='utf-8', newline='\n').write(cab + txt)
    print(f'origen organismo_vivo_rep2 {s0}  organismo_vivo_rep {s_rep}  organismo_vivo {s_vivo}  organismo_v142 {s142}  organismo_v14 {s14}')
    print(f'escrito organismo_v3cal.py  {h16(ruta)}')
    print('Arnes:  python experimentos/criterio_v3/identidad_criterio_v3.py')
