"""CREADOR B — B-5 DESAMBIGUAR CODIGOS: division por AUSENCIA DE CONSECUENCIA bajo retina distinta.

EL PROBLEMA (bloque de la sal, 18-sep 08:16): con K=3 dos estimulos distintos reciben el MISMO codigo en ~2-3 % de
las semillas (sal y veneno). El que no informa (R=0) hereda el valor del que si, el veneno pierde la mitad del miedo,
y el organo que separa codigos (division por conflicto de signo, v11) NO puede dispararse: exige Wb[c]*R < 0 y con
R = 0 el producto es 0. Lo que le falta al organismo es leer "no paso nada" como desconfirmacion.

EL MECANISMO (una condicion y una rama, todo local a la celda que divide):
  v14.1 divide si   Wb[c]*R < 0                  y |Wb[c]|>0.2  y  kj@P > KW[c]@P  (y hay celda libre)
  B-5   divide si  (Wb[c]*R < 0  o  R == 0)      y |Wb[c]|>0.2  y  kj@P > KW[c]@P  (y hay celda libre)
  donde kj@P > KW[c]@P es la DISCREPANCIA DE RETINA que v11 ya exige: la hija (kj = 0.95*KW[c] + paso*(P - mu[c]))
  solo puede nacer si el patron actual P se aparta de la imagen media mu[c] con la que la celda gano su valor. Con
  P == mu[c] (la misma imagen) no hay division: por eso 4c (C veneno con C&B=3, misma valencia) sigue sin dividir, y
  por eso una inversion pura tampoco dispara por esta via.
  FISION con R == 0: la hija nace SIN valor (Wp[j]=Wn[j]=0: no hay signo nuevo que llevarse) y la madre CONSERVA el
  suyo; en el mundo vivo la hija hereda las otras necesidades igual que en v14.1 (hereda_nec).
  Memoria nueva: CERO. Constantes nuevas: CERO. rng: no se toca (con la perilla apagada ni encendida).

PERILLA `desambiguar=0` (por defecto): con 0 el organismo es organismo_v14 (v14.1) BIT A BIT y sin consumir rng
(identidad_codigo.py). Con 1, en los mundos del tronco (R in {+1,-3}) es INERTE POR CONSTRUCCION -> tambien bit a
bit (el arnes lo comprueba como prediccion, no como exigencia). Solo actua donde existe R == 0: el mundo vivo.

Genera, POR ANCLAS, sin tocar nada congelado (los originales SOLO se leen; el sha se verifica antes):
  organismo_v14_codigo.py       <- organismo/organismo_v14.py              (TRONCO v14.1 CONGELADO)
  organismo_v14_codigo_on.py    <- el mismo con desambiguar=1 por defecto (lo examinan las baterias)
  organismo_v14g_codigo.py/_on  <- organismo/organismo_v14g.py             (mundo de regla, para bateria_generaliza)
  organismo_vivo_codigo.py      <- experimentos/nivel11_mundo_vivo/organismo_vivo.py (mundo vivo; el runner enciende)
  bateria_v14_codigo.py         <- organismo/bateria_v14.py (CONGELADA) sobre organismo_v14_codigo_on
  bateria_generaliza_codigo.py  <- organismo/bateria_generaliza.py (CONGELADA) con UNA entrada nueva, con eta_s/clip_s
                                   EXPLICITOS (organismo_v14g tiene eta_s=0.0 por defecto: ver el aviso en el informe)
Uso: python experimentos/creacion_B/construye_codigo.py     (no corre nada)
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
NIV11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')

SHA = {   # origenes: si alguno cambia, se aborta (tripwire)
    'organismo_v14.py': 'feefc88b1fd8d434',
    'organismo_v14g.py': None,            # no esta en CONGELADOS: se registra el sha leido
    'organismo_vivo.py': None,            # instrumento del nivel 11 (no congelado): se registra el sha leido
    'bateria_v14.py': '72216f5415de0c86',
    'bateria_generaliza.py': None,
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def origen(ruta, esperado):
    s = h16(ruta)
    if esperado is not None and s != esperado:
        raise SystemExit(f'*** ORIGEN {ruta}: sha {s}, se esperaba {esperado}. No se escribe nada.')
    return open(ruta, 'rb').read().decode('utf-8'), s


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


COND_A = "if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():"
COND_B = ("if (Wb[c]*R<0 or (desambiguar and R==0)) and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():"
          "   # B-5 DESAMBIGUAR: tambien divide cuando una celda consolidada, bajo una retina distinta (kj@P>KW[c]@P), recibe R==0")


def pon(src, firma_fin, fis_a, fis_b, etq):
    out = sust(src, firma_fin, firma_fin[:-2] + ",desambiguar=0):", etq=f'{etq}: firma')
    out = sust(out, "mu=np.zeros((NKMAX,6)); splits=0;", "mu=np.zeros((NKMAX,6)); splits=0; _ndes=0; _des_t=[];", etq=f'{etq}: estado')
    out = sust(out, COND_A, COND_B, etq=f'{etq}: condicion')
    out = sust(out, fis_a, fis_b, etq=f'{etq}: fision')
    out = sust(out, "    return dict(sobre=sobre,",
               "    return dict(desambiguar=desambiguar,des_splits=_ndes,des_t=_des_t,sobre=sobre,", etq=f'{etq}: return')
    return out


FIS_A = ("                                    if R>0: Wp[j]=Wp[c]; Wn[j]=0.; Wp[c]=0.\n"
         "                                    else:   Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.\n")
FIS_B = ("                                    if R>0: Wp[j]=Wp[c]; Wn[j]=0.; Wp[c]=0.\n"
         "                                    elif R<0: Wn[j]=Wn[c]; Wp[j]=0.; Wn[c]=0.\n"
         "                                    else: Wp[j]=0.; Wn[j]=0.; _ndes+=1; _des_t.append((t,kk))   # B-5: con R==0 la hija nace SIN valor (no hay signo nuevo que llevarse) y la madre conserva el suyo\n")
FIS_VA = ("                                    if R>0: Wp[_nm,j]=Wp[_nm,c]; Wn[_nm,j]=0.; Wp[_nm,c]=0.\n"
          "                                    else:   Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.\n")
FIS_VB = ("                                    if R>0: Wp[_nm,j]=Wp[_nm,c]; Wn[_nm,j]=0.; Wp[_nm,c]=0.\n"
          "                                    elif R<0: Wn[_nm,j]=Wn[_nm,c]; Wp[_nm,j]=0.; Wn[_nm,c]=0.\n"
          "                                    else: Wp[_nm,j]=0.; Wn[_nm,j]=0.; _ndes+=1; _des_t.append((t,kk))   # B-5: con R==0 la hija nace SIN valor en la necesidad activa (las otras se heredan abajo) y la madre conserva el suyo\n")


def escribe(n, t, cab):
    open(os.path.join(AQUI, n), 'w', encoding='utf-8', newline='\n').write(cab + t)
    return h16(os.path.join(AQUI, n))


if __name__ == '__main__':
    H = {}
    # --- tronco ---
    src, s14 = origen(os.path.join(ORG, 'organismo_v14.py'), SHA['organismo_v14.py'])
    v = pon(src, ",pat_shuf=0,pat_min=1):", FIS_A, FIS_B, 'v14')
    cab = (f'"""organismo_v14_codigo = organismo/organismo_v14.py ({s14}, TRONCO v14.1 CONGELADO: solo se leyo) + perilla\n'
           f'`desambiguar` (B-5): la division por conflicto de signo de v11 se dispara TAMBIEN cuando una celda consolidada,\n'
           f'bajo una retina distinta (kj@P > KW[c]@P), recibe R == 0 (ausencia de consecuencia); la hija nace sin valor y la\n'
           f'madre conserva el suyo. Con desambiguar=0 es organismo_v14 EXACTO y no se toca el rng (identidad_codigo.py).\n'
           f'Generado por construye_codigo.py. NO editar a mano."""\n')
    H['organismo_v14_codigo.py'] = escribe('organismo_v14_codigo.py', v, cab)
    H['organismo_v14_codigo_on.py'] = escribe('organismo_v14_codigo_on.py',
        sust(v, ",pat_min=1,desambiguar=0):", ",pat_min=1,desambiguar=1):", etq='on: tronco'),
        '"""organismo_v14_codigo_on = organismo_v14_codigo.py con `desambiguar=1` POR DEFECTO. Las baterias examinan ESTE\n'
        'modulo (la perilla ENCENDIDA). En los mundos del tronco R nunca es 0, asi que la prediccion es IDENTIDAD con v14.1.\n'
        'Generado por construye_codigo.py. NO editar."""\n')
    # --- mundo de regla ---
    srcg, s14g = origen(os.path.join(ORG, 'organismo_v14g.py'), SHA['organismo_v14g.py'])
    vg = pon(srcg, ",pat_shuf=0,pat_min=0):", FIS_A, FIS_B, 'v14g')
    H['organismo_v14g_codigo.py'] = escribe('organismo_v14g_codigo.py', vg,
        f'"""organismo_v14g_codigo = organismo/organismo_v14g.py ({s14g}, solo se leyo) + perilla `desambiguar` (B-5).\n'
        f'Con desambiguar=0 es organismo_v14g EXACTO. Generado por construye_codigo.py. NO editar."""\n')
    H['organismo_v14g_codigo_on.py'] = escribe('organismo_v14g_codigo_on.py',
        sust(vg, ",pat_min=0,desambiguar=0):", ",pat_min=0,desambiguar=1):", etq='on: regla'),
        '"""organismo_v14g_codigo_on = organismo_v14g_codigo.py con la perilla FIJA en 1. Generado por construye_codigo.py."""\n')
    # --- mundo vivo ---
    srcv, sv = origen(os.path.join(NIV11, 'organismo_vivo.py'), SHA['organismo_vivo.py'])
    vv = pon(srcv, ",k_sorp=0.0,crit_exp=0.5):", FIS_VA, FIS_VB, 'vivo')
    H['organismo_vivo_codigo.py'] = escribe('organismo_vivo_codigo.py', vv,
        f'"""organismo_vivo_codigo = experimentos/nivel11_mundo_vivo/organismo_vivo.py ({sv}, solo se leyo) + perilla\n'
        f'`desambiguar` (B-5): division tambien por R == 0 bajo retina distinta; la hija nace sin valor en la necesidad\n'
        f'activa y hereda las otras (hereda_nec, como en v14.1). Con desambiguar=0 es organismo_vivo EXACTO (y con\n'
        f'vivo=0, n_nec=1 es organismo_v14 EXACTO, como su origen). El runner corre_codigo.py enciende la perilla por brazo.\n'
        f'Generado por construye_codigo.py. NO editar."""\n')
    # --- bateria del examen v3' ---
    srcb, sb = origen(os.path.join(ORG, 'bateria_v14.py'), SHA['bateria_v14.py'])
    b = sust(srcb, 'import organismo_v14 as v13   # TRONCO v14: hija dispersa + puerta por codigo',
             'import organismo_v14_codigo_on as v13   # B-5: la perilla ENCENDIDA (el examen mide AL CANDIDATO)', n=2, etq='bat: import')
    b = sust(b, "'organismo_v14.py'", "'organismo_v14_codigo_on.py'", n=2, etq='bat: sha')
    b = sust(b, "f'examen_v14_{stamp}.log'", "f'examen_codigo_{stamp}.log'", etq='bat: log')
    b = sust(b, "f'examen_v14_{stamp}.json'", "f'examen_codigo_{stamp}.json'", etq='bat: json')
    b = sust(b, "RAIZ = os.path.dirname(AQUI)   # tronco: organismo/ -> bundle/",
             "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # B-5: experimentos/creacion_B/ -> bundle/", etq='bat: RAIZ')
    b = sust(b, "sys.path[:0] = [_D14, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]",
             "sys.path[:0] = [os.path.join(RAIZ, 'organismo'), _D14, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]   # organismo/ PRIMERO (ERR-28)",
             etq='bat: sys.path')
    b = sust(b, "sha_organismo_v11=h16(os.path.join(AQUI, 'organismo_v11.py')), sha_organismo_v10=h16(os.path.join(AQUI, 'organismo_v10.py'))",
             "sha_organismo_v11=h16(os.path.join(RAIZ, 'organismo', 'organismo_v11.py')), sha_organismo_v10=h16(os.path.join(RAIZ, 'organismo', 'organismo_v10.py'))",
             etq='bat: sha v11/v10')
    H['bateria_v14_codigo.py'] = escribe('bateria_v14_codigo.py', b,
        f'"""bateria_v14_codigo = organismo/bateria_v14.py ({sb}, CONGELADA: solo se leyo) sobre **organismo_v14_codigo_on**\n'
        f'(la perilla ENCENDIDA). Las SEIS etapas, los CRIT y los umbrales del criterio v3\' INTACTOS. Salida datos/examen_codigo_*.\n'
        f'Generado por construye_codigo.py. NO editar."""\n')
    # --- bateria de generalizacion ---
    srcg2, sg = origen(os.path.join(ORG, 'bateria_generaliza.py'), SHA['bateria_generaliza.py'])
    m = re.search(r"^ *'organismo_v14': \(.*$", srcg2, re.M)
    if not m:
        raise SystemExit('*** no encuentro la entrada organismo_v14 en INSTRUMENTOS')
    A = m.group(0)
    g = sust(srcg2, A, A + "\n    'organismo_v14_codigo_on': ('organismo_v14g_codigo_on', dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, "
             "del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)),   # B-5: los MISMOS kwargs que organismo_v14 (eta_s/clip_s explicitos: v14g los tiene apagados por defecto)",
             etq='gen: INSTRUMENTOS')
    g = sust(g, "RAIZ = os.path.dirname(AQUI)", "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # B-5", etq='gen: RAIZ')
    g = sust(g, "f'regresion_generaliza_{modulo}_{stamp}.log'", "f'regresion_generaliza_codigo_{modulo}_{stamp}.log'", etq='gen: log')
    g = sust(g, "f'regresion_generaliza_{modulo}_{stamp}.json'", "f'regresion_generaliza_codigo_{modulo}_{stamp}.json'", etq='gen: json')
    g = sust(g, "sys.path[:0] = [AQUI, GEN, os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]",
             "sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI, GEN, os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]   # organismo/ PRIMERO (ERR-28)",
             etq='gen: sys.path')
    g = re.sub(r"_dir = \{'organismo_v14g': [^,]+,", "_dir = {'organismo_v14g': os.path.join(RAIZ, 'organismo'), 'organismo_v14g_codigo_on': AQUI,", g, count=1)
    H['bateria_generaliza_codigo.py'] = escribe('bateria_generaliza_codigo.py', g,
        f'"""bateria_generaliza_codigo = organismo/bateria_generaliza.py ({sg}, CONGELADA: solo se leyo) con UNA entrada nueva:\n'
        f'organismo_v14_codigo_on -> organismo_v14g_codigo_on, con los MISMOS kwargs que la entrada del tronco (eta_s=0.15,\n'
        f'clip_s=10.0 explicitos). Umbrales G1/G2/K sin tocar. Salida datos/regresion_generaliza_codigo_*.\n'
        f'Generado por construye_codigo.py. NO editar."""\n')
    print(f'origen organismo_v14.py {s14}  organismo_v14g.py {s14g}  organismo_vivo.py {sv}  bateria_v14.py {sb}  bateria_generaliza.py {sg}')
    for k, val in H.items():
        print(f'escrito {k:32s} {val}')
