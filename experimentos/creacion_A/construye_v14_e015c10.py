"""CREADOR A — PAQUETE A-4, pieza (3): el CONTROL QUE PUEDE FALLAR.

Las dos constantes de la vía lenta (`eta_s` 0.015 -> 0.15, `clip_s` 3 -> 10) tocan el TRONCO. Antes de que entren,
hay que pasar por el examen y por la regresión de generalización **con esas constantes puestas**. Este script genera,
POR ANCLAS y sin editar nada congelado (patrón de `construye_v14c.py` / `construye_v13E.py`):

  organismo_v14_e015c10.py   <- organismo/organismo_v14.py   (TRONCO CONGELADO, solo se LEE)
                                UNICO cambio: los VALORES POR DEFECTO `eta_s=.015 -> .15` y `clip_s=3.0 -> 10.0`.
                                Ni una linea de logica. Identidad: llamandolo con eta_s=0.015, clip_s=3.0
                                explicitos es organismo_v14 EXACTO (lo comprueba identidad_v14_e015c10.py).
  bateria_v14_e015c10.py     <- organismo/bateria_v14.py     (CONGELADA, solo se LEE)
                                UNICO cambio: el modulo que examina y los nombres de salida. Las SEIS etapas, los
                                CRIT importados y los umbrales del criterio v3' quedan INTACTOS.
  bateria_generaliza_A.py    <- organismo/bateria_generaliza.py (CONGELADA, solo se LEE)
                                UNICO cambio: UNA entrada nueva en INSTRUMENTOS
                                ('organismo_v14_e015c10' -> organismo_v14g con eta_s=0.15, clip_s=10.0). El
                                instrumento del mundo de regla NO se duplica: `organismo_v14g` ya acepta las dos
                                constantes como argumentos. Umbrales G1/G2/K sin tocar.

Uso: python construye_v14_e015c10.py     (no corre nada; solo escribe en experimentos/creacion_A/)
"""
import os, hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
ETA_NUEVA, CLIP_NUEVO = 0.15, 10.0


def origen(ruta, sha_esperado=None):
    s = open(ruta, 'rb').read(); h = hashlib.sha256(s).hexdigest()[:16]
    if sha_esperado and h != sha_esperado:
        raise SystemExit(f'*** {os.path.basename(ruta)}: sha {h} != esperado {sha_esperado}. No se escribe nada.')
    return s.decode('utf-8'), h


def sust(txt, ancla, nuevo, n=1, etq=''):
    c = txt.count(ancla)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return txt.replace(ancla, nuevo)


# ------------------------------------------------------------------ 1) el organismo
src, sha_org = origen(os.path.join(ORG, 'organismo_v14.py'))
A = ',eta_s=0.015,clip_s=3.0,puerta=3,mask_rel=2,'
B = f',eta_s={ETA_NUEVA},clip_s={CLIP_NUEVO},puerta=3,mask_rel=2,'
out = sust(src, A, B, etq='constantes de la via lenta')
cab = (f'"""organismo_v14_e015c10 = organismo/organismo_v14.py ({sha_org}, TRONCO CONGELADO: solo se leyo) con las\n'
       f'DOS CONSTANTES de la via lenta cambiadas por defecto: eta_s 0.015 -> {ETA_NUEVA} y clip_s 3.0 -> {CLIP_NUEVO}\n'
       f'(propuesta A-4 del creador A). NINGUNA linea de logica cambia. Llamandolo con eta_s=0.015, clip_s=3.0 es\n'
       f'organismo_v14 EXACTO (identidad obligatoria: identidad_v14_e015c10.py).\n'
       f'Generado por experimentos/creacion_A/construye_v14_e015c10.py. NO editar a mano."""\n')
open(os.path.join(AQUI, 'organismo_v14_e015c10.py'), 'w', encoding='utf-8').write(cab + out)

# ------------------------------------------------------------------ 2) la bateria del examen (criterio v3')
src, sha_bat = origen(os.path.join(ORG, 'bateria_v14.py'))
out = sust(src, 'import organismo_v14 as v13   # TRONCO v14: hija dispersa + puerta por codigo',
           'import organismo_v14_e015c10 as v13   # A-4: el tronco v14 con eta_s=0.15 y clip_s=10',
           n=2, etq='import del organismo')
out = sust(out, "'organismo_v14.py'", "'organismo_v14_e015c10.py'", n=2, etq='sha del organismo')
out = sust(out, "f'examen_v14_{stamp}.log'", "f'examen_v14_e015c10_{stamp}.log'", etq='log')
out = sust(out, "f'examen_v14_{stamp}.json'", "f'examen_v14_e015c10_{stamp}.json'", etq='json')
out = sust(out, "_D14 = os.path.dirname(os.path.abspath(__file__))   # tronco: organismo/",
           "_D14 = os.path.dirname(os.path.abspath(__file__))   # A-4: experimentos/creacion_A/", etq='_D14')
out = sust(out, "RAIZ = os.path.dirname(AQUI)   # tronco: organismo/ -> bundle/",
           "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # A-4: experimentos/creacion_A/ -> bundle/",
           etq='RAIZ de la bateria')
out = sust(out, "sys.path[:0] = [_D14, AQUI, os.path.join(RAIZ, 'experimentos', 'bug01')]",
           "sys.path[:0] = [_D14, AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'bug01')]",
           etq='sys.path')
cab = (f'"""bateria_v14_e015c10 = organismo/bateria_v14.py ({sha_bat}, CONGELADA: solo se leyo) apuntando a\n'
       f'organismo_v14_e015c10 (las dos constantes de A-4). Las SEIS etapas, los CRIT y los umbrales del criterio\n'
       f'v3\' quedan INTACTOS. Salida en datos/examen_v14_e015c10_<fecha>.\n'
       f'Generado por experimentos/creacion_A/construye_v14_e015c10.py. NO editar. La bateria original NO se toco."""\n')
open(os.path.join(AQUI, 'bateria_v14_e015c10.py'), 'w', encoding='utf-8').write(cab + out)

# ------------------------------------------------------------------ 3) la regresion de generalizacion
src, sha_gen = origen(os.path.join(ORG, 'bateria_generaliza.py'))
A = "    'organismo_v14': ('organismo_v14g', dict(eta_s=0.015, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)),   # TRONCO v14 (18 sep): hija dispersa + puerta por codigo, las DOS ON"
B = (A + "\n    'organismo_v14_e015c10': ('organismo_v14g', dict(eta_s=" + str(ETA_NUEVA) + ", clip_s=" + str(CLIP_NUEVO) +
     ", puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)),   # A-4: v14 con las dos constantes de la via lenta")
out = sust(src, A, B, etq='INSTRUMENTOS')
out = sust(out, "f'regresion_generaliza_{modulo}_{stamp}.log'", "f'regresion_generaliza_A_{modulo}_{stamp}.log'", etq='log gen')
out = sust(out, "RAIZ = os.path.dirname(AQUI)", "RAIZ = os.path.dirname(os.path.dirname(AQUI))   # A-4: experimentos/creacion_A/ -> bundle/", etq='RAIZ de generaliza')
out = sust(out, "sys.path[:0] = [AQUI, GEN, os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]",
           "sys.path[:0] = [AQUI, GEN, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'etapa3_v9')]",
           etq='sys.path de generaliza')
out = sust(out, "_dir = {'organismo_v14g': AQUI,", "_dir = {'organismo_v14g': os.path.join(RAIZ, 'organismo'),",
           etq='_dir: organismo_v14g vive en organismo/, no en mi carpeta')
out = sust(out, "h16(os.path.join(AQUI, (modulo if modulo != 'organismo_v13_rapido' else 'organismo_v13') + '.py'))",
           "h16(os.path.join(AQUI, (modulo if modulo != 'organismo_v13_rapido' else 'organismo_v13') + '.py'))",
           etq='sha del modulo (se comprueba que sigue ahi)')
cab = (f'"""bateria_generaliza_A = organismo/bateria_generaliza.py ({sha_gen}, CONGELADA: solo se leyo) con UNA\n'
       f'entrada nueva en INSTRUMENTOS para el brazo A-4 (organismo_v14_e015c10 -> organismo_v14g con eta_s={ETA_NUEVA},\n'
       f'clip_s={CLIP_NUEVO}). Umbrales G1/G2/K sin tocar. El instrumento del mundo de regla NO se duplica.\n'
       f'Generado por experimentos/creacion_A/construye_v14_e015c10.py. NO editar."""\n')
open(os.path.join(AQUI, 'bateria_generaliza_A.py'), 'w', encoding='utf-8').write(cab + out)

h = lambda n: hashlib.sha256(open(os.path.join(AQUI, n), 'rb').read()).hexdigest()[:16]
print(f'origen  organismo_v14.py {sha_org}   bateria_v14.py {sha_bat}   bateria_generaliza.py {sha_gen}')
for n in ('organismo_v14_e015c10.py', 'bateria_v14_e015c10.py', 'bateria_generaliza_A.py'):
    print(f'escrito {n:28s} {h(n)}')
