"""CONGELACION v14.2 — constructor POR ANCLAS de los cuatro archivos nuevos del tronco.

v14.2 = v14.1 + B-5 (DESAMBIGUAR CODIGOS, declarado en dos series el 18-sep 09:07 y 09:12; decision del
director 18-sep ~20:40 "corre las recomendaciones"). NO cambia ningun numero del tronco: la unica diferencia
con v14.1 es que la perilla `desambiguar` de B-5 viene ENCENDIDA por defecto. En los mundos del tronco
R in {+1,-3} y la condicion `R == 0` no puede darse: la regla es INERTE POR CONSTRUCCION ahi (medido:
examen 8/8 con splits identicos, generalizacion 40/40 identicas, coste 0 % exacto).

Genera (LEYENDO solo; no toca nada congelado ni ningun original):
  organismo/organismo_v142.py            <- experimentos/creacion_B/organismo_v14_codigo.py  (a4eeca90fb605c78)
  organismo/organismo_v142g.py           <- experimentos/creacion_B/organismo_v14g_codigo.py (ae9231070a95c801)
  organismo/bateria_v142.py              <- organismo/bateria_v14.py          (72216f5415de0c86, CONGELADA)
  organismo/bateria_generaliza_v142.py   <- organismo/bateria_generaliza.py   (9cf72581ebae7dea)

De los dos organismos SOLO se cambia el valor por defecto de `desambiguar` (0 -> 1) y la cabecera. De las dos
baterias, solo el modulo al que apuntan, los nombres de salida y (generaliza) UNA entrada nueva en INSTRUMENTOS
CAMPO A CAMPO igual a la de `organismo_v14` (regla 14 de EQUIPO.md). Los sha se leen desde `organismo/` porque
las baterias VIVEN en `organismo/` (AQUI == organismo/): ERR-42 no puede repetirse aqui.

Uso: python experimentos/creacion_B/construye_v142.py      (no corre nada)
"""
import hashlib, os, re, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')

SHA = {   # tripwire: si un origen cambio, no se escribe nada
    'organismo_v14_codigo.py':  'a4eeca90fb605c78',
    'organismo_v14g_codigo.py': 'ae9231070a95c801',
    'bateria_v14.py':           '72216f5415de0c86',
    'bateria_generaliza.py':    '9cf72581ebae7dea',
    'organismo_v14.py':         'feefc88b1fd8d434',   # v14.1, solo para la cabecera
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


def escribe(n, t, cab):
    p = os.path.join(ORG, n)
    if os.path.exists(p):
        print(f'  (sobrescribe {n}, sha previo {h16(p)})')
    open(p, 'w', encoding='utf-8', newline='\n').write(cab + t)
    return h16(p)


if __name__ == '__main__':
    H = {}
    s141 = h16(os.path.join(ORG, 'organismo_v14.py'))
    if s141 != SHA['organismo_v14.py']:
        raise SystemExit(f'*** organismo_v14.py (v14.1) sha {s141}: el tronco cambio. No se escribe nada.')

    # --- 1) el tronco v14.2 ---
    src, sc = origen(os.path.join(AQUI, 'organismo_v14_codigo.py'), SHA['organismo_v14_codigo.py'])
    v = sust(src, ',pat_min=1,desambiguar=0):', ',pat_min=1,desambiguar=1):', etq='v142: default')
    cab = (f'"""organismo_v142 = TRONCO v14.2 desde el 18 sep 2026 (noche). v14.2 = v14.1 + B-5.\n'
           f'v14.1 = organismo/organismo_v14.py ({s141}, CONGELADO: solo se leyo).\n'
           f'B-5 DESAMBIGUAR CODIGOS (nivel 4, declarado en dos series el 18-sep 09:07 y 09:12): la division por\n'
           f'conflicto de signo de v11 se dispara TAMBIEN cuando una celda consolidada (|Wb[c]|>0.2), bajo una retina\n'
           f'distinta (kj@P > KW[c]@P), recibe R == 0 (ausencia de consecuencia); la hija nace SIN valor y la madre\n'
           f'conserva el suyo. Memoria nueva: CERO. Constantes nuevas: CERO. El rng no se toca.\n'
           f'LO UNICO QUE CAMBIA respecto de v14.1 es el defecto de la perilla: `desambiguar=1`. Con desambiguar=0\n'
           f'es organismo_v14 EXACTO bit a bit (organismo/identidad_v142.py). En los mundos del tronco R in (+1,-3):\n'
           f'la regla es INERTE POR CONSTRUCCION (examen 8/8 con splits identicos, generalizacion 40/40 identicas,\n'
           f'coste 0 % exacto). Donde SI actua: el mundo vivo, donde repara el alias de codigo (18/18 semillas ALIAS:\n'
           f'|W[sal]| 0.0, veneno -3.0, evitacion x7 -> x1, muertes a la mitad).\n'
           f'Generado POR ANCLAS desde experimentos/creacion_B/organismo_v14_codigo.py ({sc}) por construye_v142.py.\n'
           f'CONGELADO: NO editar a mano. Evidencia: registro/REGISTRO_etapas_1_2.md (B-5 y replica), PROPUESTA_v14.md."""\n')
    H['organismo_v142.py'] = escribe('organismo_v142.py', v, cab)

    # --- 2) el mundo de regla de v14.2 ---
    srcg, scg = origen(os.path.join(AQUI, 'organismo_v14g_codigo.py'), SHA['organismo_v14g_codigo.py'])
    vg = sust(srcg, ',pat_min=0,desambiguar=0):', ',pat_min=0,desambiguar=1):', etq='v142g: default')
    cabg = (f'"""organismo_v142g = instrumento de MUNDO DE REGLA del tronco v14.2 (lo usa bateria_generaliza_v142.py).\n'
            f'= organismo/organismo_v14g.py ({h16(os.path.join(ORG, "organismo_v14g.py"))}, solo se leyo) + B-5 con\n'
            f'`desambiguar=1` POR DEFECTO, igual que el tronco. Con desambiguar=0 es organismo_v14g EXACTO.\n'
            f'AVISO (regla 14): sus defectos de via lenta son eta_s=0.0, clip_s=3.0, puerta=None, mask_rel=0,\n'
            f'puerta_pat=0 -- la entrada de INSTRUMENTOS los pasa EXPLICITOS, campo a campo como la de organismo_v14.\n'
            f'Generado POR ANCLAS desde experimentos/creacion_B/organismo_v14g_codigo.py ({scg}) por construye_v142.py.\n'
            f'CONGELADO: NO editar a mano."""\n')
    H['organismo_v142g.py'] = escribe('organismo_v142g.py', vg, cabg)

    # --- 3) el examen v3' del tronco v14.2 ---
    srcb, sb = origen(os.path.join(ORG, 'bateria_v14.py'), SHA['bateria_v14.py'])
    b = sust(srcb, 'import organismo_v14 as v13   # TRONCO v14: hija dispersa + puerta por codigo',
             'import organismo_v142 as v13   # TRONCO v14.2 = v14.1 + B-5 (desambiguar=1 por defecto)', n=2, etq='bat: import')
    b = sust(b, "h16(os.path.join(_D14, 'organismo_v14.py'))", "h16(os.path.join(_D14, 'organismo_v142.py'))", n=2, etq='bat: sha')
    b = sust(b, "f'examen_v14_{stamp}.log'", "f'examen_v142_{stamp}.log'", etq='bat: log')
    b = sust(b, "f'examen_v14_{stamp}.json'", "f'examen_v142_{stamp}.json'", etq='bat: json')
    H['bateria_v142.py'] = escribe('bateria_v142.py', b,
        '"""bateria_v142 = organismo/bateria_v14.py (' + sb + ', CONGELADA: solo se leyo) apuntando a **organismo_v142**\n'
        "(TRONCO v14.2 = v14.1 + B-5, la perilla ENCENDIDA por defecto). Las SEIS etapas, los CRIT importados y los\n"
        "umbrales del criterio v3' quedan INTACTOS; solo cambian el modulo examinado y los nombres de salida\n"
        "(datos/examen_v142_<fecha>.log/.json). Vive en organismo/, asi que AQUI == organismo/ y los sha de\n"
        "organismo_v11/organismo_v10 se leen de su sitio real (ERR-42 no aplica).\n"
        '    python bateria_v142.py 6                      (regla 1, desde organismo/)\n'
        'Generado POR ANCLAS por experimentos/creacion_B/construye_v142.py. CONGELADA: NO editar."""\n')

    # --- 4) la regresion de generalizacion del tronco v14.2 ---
    srcg2, sg = origen(os.path.join(ORG, 'bateria_generaliza.py'), SHA['bateria_generaliza.py'])
    m = re.search(r"^ *'organismo_v14': \(.*$", srcg2, re.M)
    if not m:
        raise SystemExit('*** no encuentro la entrada organismo_v14 en INSTRUMENTOS. No se escribe nada.')
    A = m.group(0)
    # REGLA 14: la entrada nueva es CAMPO A CAMPO la del tronco; solo cambia el instrumento.
    kw14 = re.search(r"dict\((.*?)\)\),", A).group(1)
    KW_ESPERADO = ("eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, "
                   "puerta_pat=5, pat_shuf=0, pat_min=1")
    if kw14.strip() != KW_ESPERADO:
        raise SystemExit(f'*** los kwargs de organismo_v14 cambiaron: {kw14!r}. No se escribe nada.')
    NUEVA = ("    'organismo_v142': ('organismo_v142g', dict(" + KW_ESPERADO + ")),"
             "   # TRONCO v14.2 (18 sep, noche) = v14.1 + B-5: kwargs CAMPO A CAMPO iguales a los de organismo_v14 (regla 14)")
    g = sust(srcg2, A, A + "\n" + NUEVA, etq='gen: INSTRUMENTOS')
    g = sust(g, "_dir = {'organismo_v14g': AQUI,", "_dir = {'organismo_v14g': AQUI, 'organismo_v142g': AQUI,", etq='gen: _dir')
    H['bateria_generaliza_v142.py'] = escribe('bateria_generaliza_v142.py', g,
        '"""bateria_generaliza_v142 = organismo/bateria_generaliza.py (' + sg + ', solo se leyo) con UNA entrada nueva en\n'
        'INSTRUMENTOS: organismo_v142 -> organismo_v142g, con los kwargs CAMPO A CAMPO iguales a los de la entrada\n'
        'del tronco organismo_v14 (regla 14 de EQUIPO.md; eta_s=0.15 y clip_s=10.0 EXPLICITOS porque el instrumento\n'
        'de mundo de regla los trae apagados por defecto). Umbrales G1/G2/K sin tocar. Vive en organismo/, asi que\n'
        'los sha del organismo y del instrumento se leen desde organismo/ (ERR-42).\n'
        '    python bateria_generaliza_v142.py organismo_v142 20 --desde 101 --log      (desde organismo/)\n'
        'Generada POR ANCLAS por experimentos/creacion_B/construye_v142.py. CONGELADA: NO editar."""\n')

    print(f'\norigen organismo_v14_codigo.py {sc}  organismo_v14g_codigo.py {scg}'
          f'  bateria_v14.py {sb}  bateria_generaliza.py {sg}  (v14.1 {s141})')
    for k, val in H.items():
        print(f'escrito organismo/{k:28s} {val}')
