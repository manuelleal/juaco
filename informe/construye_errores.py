"""Construye informe/errores.csv a partir de las definiciones de los ERR del repo y de una clasificacion hecha a mano.

Paso A del informe del protocolo (registro/RUTA.md). No corre simulaciones: solo lee archivos y git.

Qué hace, en orden:
  1. ESCANEO. Recorre todos los .md del repo (sin datos/, .git/, .claude/) y anota cada aparicion de "ERR-N".
     Esto da el inventario de numeros usados y los huecos.
  2. DEFINICION. Para cada numero 1..153, la tabla FUENTES (abajo) fija el archivo:linea donde se DEFINE el ERR
     (elegida a mano leyendo el contexto; la aparicion mas temprana no siempre es la definicion). El script VERIFICA
     que esa linea contiene el token ERR-N (o, para ERR-1..4, la palabra clave indicada), y aborta si no.
     Extrae el parrafo de la definicion (texto) de forma determinista.
  3. FECHA. Si el parrafo trae una fecha explicita (18 sep, 21-sep-2026, 2026-09-21...), se usa esa. Si no, la del
     primer commit de `main` que introduce el token en ese archivo (git log --reverse -G). Se anota el origen.
  4. UNION. Junta lo extraido con informe/clasificacion_errores.json (una entrada por ERR, hecha a mano) y escribe:
       informe/definiciones_errores.json  (numero, fuente, fecha, origen_fecha, texto extraido)
       informe/errores.csv                (las columnas del encargo + justificacion_tipo)
       informe/resumen_errores.md         (conteos y la X de la tesis)
       informe/muestra_20.csv             (20 ERR al azar, random.Random(20260929).sample, + columna vacia)

Uso:  python informe/construye_errores.py
"""
import csv
import collections
import datetime
import json
import os
import random
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INF = os.path.join(BASE, 'informe')
REG = 'registro/REGISTRO_etapas_1_2.md'
RAMA_NUBE = 'origin/nube/eco-sel-largo-20260928'

# ---------------------------------------------------------------------------------------------------------------
# FUENTES: numero -> (ruta, linea, token). token=None => se exige "ERR-N" en la linea.
#   ruta 'git:<ref>:<archivo>' => se lee con `git show` (sin merge).
#   ERR-1..4 no llevan numero escrito en el repo: el registro los enumera por ordinal (REGISTRO:192 y :333,
#   "los cuatro errores anteriores (unidades 2H, disponibilidad 2I, aliasing ANOM-01, aritmetica del techo 2K)").
#   Para ellos la fuente es la linea que describe cada error y el token es una palabra de esa linea.
#   None => el numero no aparece como ERR usado en ninguna parte (fila "no encontrado").
# ---------------------------------------------------------------------------------------------------------------
FUENTES = {
    1: (REG, 41, 'Error metodológico'),
    2: (REG, 83, 'Corrección de criterio'),
    3: (REG, 85, 'ANOM-01'),
    4: (REG, 93, 'error aritmético'),
    5: (REG, 172, None), 6: (REG, 227, None), 7: (REG, 428, None), 8: (REG, 312, None), 9: (REG, 737, None),
    10: (REG, 761, None), 11: (REG, 998, None), 12: (REG, 1384, None), 13: (REG, 1518, None), 14: (REG, 1711, None),
    15: (REG, 1780, None), 16: (REG, 1879, None), 17: (REG, 2247, None), 18: (REG, 2291, None), 19: (REG, 2325, None),
    20: (REG, 2524, None), 21: (REG, 2688, None), 22: (REG, 2772, None), 23: (REG, 3106, None), 24: (REG, 3494, None),
    25: (REG, 3710, None), 26: (REG, 3925, None), 27: (REG, 3929, None), 28: (REG, 3977, None), 29: (REG, 4043, None),
    30: (REG, 4051, None), 31: (REG, 4116, None), 32: (REG, 4400, None), 33: (REG, 4508, None), 34: (REG, 4509, None),
    35: (REG, 4559, None), 36: (REG, 4597, None),
    37: ('experimentos/nivel11_mundo_vivo/PREREGISTRO_mundo_vivo.md', 285, None),
    38: (REG, 4811, None),
    39: ('experimentos/nivel11_mundo_vivo/PREREGISTRO_reproduccion.md', 270, None),
    40: ('experimentos/nivel11_mundo_vivo/PREREGISTRO_reproduccion_2.md', 12, None),
    41: (REG, 4988, None), 42: (REG, 4992, None), 43: (REG, 5027, None), 44: (REG, 5146, None), 45: (REG, 5154, None),
    46: ('experimentos/nivel12_mundo_familias/PREREGISTRO_bloque1_familias_enm1.md', 1, None),
    47: ('experimentos/nivel12_mundo_familias/PREREGISTRO_bloque1_familias_enm1.md', 233, None),
    48: ('experimentos/nivel12_mundo_familias/PREREGISTRO_bloque1_familias_enm1.md', 257, None),
    49: ('experimentos/nivel12_mundo_familias/PREREGISTRO_bloque1_familias_enm1.md', 359, None),
    50: (REG, 5273, None),
    51: ('experimentos/nivel12_mundo_familias/PREREGISTRO_bloque4b_emisor.md', 19, None),
    52: (REG, 5283, None),
    53: (REG, 5304, None),
    54: (REG, 5311, None),
    55: None, 56: None, 57: None, 58: None, 59: None,
    60: ('experimentos/nivel11_mundo_vivo/PREREGISTRO_h1_muerte.md', 65, None),
    61: ('experimentos/nivel11_mundo_vivo/PREREGISTRO_h1_muerte.md', 130, None),
    62: (REG, 5349, None),
    63: ('experimentos/nivel12_mundo_familias/PREREGISTRO_bloque5_ganadoras.md', 370, None),
    64: ('experimentos/nivel12_mundo_familias/PREREGISTRO_bloque5_ganadoras.md', 372, None),
    65: None, 66: None, 67: None, 68: None, 69: None,
    70: ('experimentos/nivel12_mundo_familias/PREREGISTRO_bloque6_sufijo.md', 366, None),
    71: ('experimentos/nivel12_mundo_familias/PREREGISTRO_bloque6_sufijo.md', 391, None),
    72: None, 73: None, 74: None, 75: None, 76: None, 77: None, 78: None, 79: None,
    80: ('experimentos/nivel13_alma/PREREGISTRO_alma.md', 135, None),
    81: ('experimentos/nivel13_alma/PREREGISTRO_alma.md', 137, None),
    82: ('experimentos/nivel13_alma/PREREGISTRO_alma.md', 138, None),
    83: ('experimentos/nivel13_alma/PREREGISTRO_alma.md', 139, None),
    84: (REG, 5424, None),
    85: ('registro/HANDOFF.md', 821, None),
    86: ('registro/HANDOFF.md', 823, None),
    87: ('experimentos/nivel7_hija_dispersa/HALLAZGO_auditoria_ERR29.md', 1, None),
    88: (REG, 5537, None), 89: (REG, 5587, None),
    90: ('experimentos/nivel05_familia_variante_BAv/PREREGISTRO_bav.md', 49, None),
    91: (REG, 5757, None), 92: (REG, 5773, None),
    93: ('experimentos/nivel09_cuerpo_nuevo_b2/PREREGISTRO_bloque2.md', 18, None),
    94: ('registro/CRITERIO_TRONCO_v4.md', 1, None),
    95: ('experimentos/carrera_escuderias/REGLAMENTO.md', 86, None),
    96: ('experimentos/carrera_escuderias/REGLAMENTO.md', 88, None),
    97: ('experimentos/carrera_escuderias/REGLAMENTO.md', 94, None),
    98: ('experimentos/carrera_escuderias/REGLAMENTO.md', 103, None),
    99: ('experimentos/carrera_escuderias/REGLAMENTO.md', 243, None),
    100: ('experimentos/carrera_escuderias/REGLAMENTO.md', 172, None),
    101: ('experimentos/carrera_escuderias/REGLAMENTO.md', 178, None),
    102: ('experimentos/carrera_escuderias/REGLAMENTO.md', 116, None),
    103: (REG, 6375, None), 104: (REG, 6383, None),
    105: (REG, 6120, None), 106: (REG, 6121, None), 107: (REG, 6122, None), 108: (REG, 6123, None),
    109: (REG, 6124, None), 110: (REG, 6125, None), 111: (REG, 6291, None), 112: (REG, 6292, None),
    113: (REG, 6293, None), 114: (REG, 6421, None), 115: (REG, 6422, None), 116: (REG, 6441, None),
    117: (REG, 6520, None), 118: (REG, 6527, None), 119: (REG, 6556, None), 120: (REG, 6621, None),
    121: (REG, 6622, None),
    122: ('experimentos/tronco_v14_3_examen/PREREGISTRO_examen_v143.md', 9, None),
    123: ('experimentos/organelos/darwin/PREREGISTRO_endosimbiosis.md', 104, None),
    124: ('experimentos/organelos/cruce/PREREGISTRO_cruce.md', 154, None),
    125: ('experimentos/organelos/gramatica/PREREGISTRO_gramatica.md', 27, None),
    126: ('experimentos/organelos/ohno/PREREGISTRO_ohno.md', 153, None),
    127: None, 128: None, 129: None,
    130: ('experimentos/organelos/anfitrion/nube_20260924/ERR_130-132_anfitrion.md', 6, None),
    131: ('experimentos/organelos/anfitrion/nube_20260924/ERR_130-132_anfitrion.md', 13, None),
    132: ('experimentos/organelos/anfitrion/nube_20260924/ERR_130-132_anfitrion.md', 18, None),
    133: ('experimentos/organelos/ohno/nube_20260925/ERR_133-134_ohno.md', 6, None),
    134: ('experimentos/organelos/ohno/nube_20260925/ERR_133-134_ohno.md', 23, None),
    135: None, 136: None, 137: None, 138: None, 139: None,
    140: ('experimentos/organelos/codigo/PREREGISTRO_codigo.md', 68, None),
    141: ('experimentos/organelos/codigo/INFORME.md', 76, None),
    142: ('experimentos/organelos/codigo/v01/PREREGISTRO_v01.md', 182, None),
    143: ('experimentos/organelos/ohno/hplano_nube/PREREGISTRO_hplano_w90_PC.md', 100, None),
    144: ('experimentos/organelos/prometeo/serie/PREREGISTRO_serie.md', 97, None),
    145: None,
    146: ('experimentos/organelos/frio/PREREGISTRO_frio.md', 60, None),
    147: ('experimentos/organelos/frio/PREREGISTRO_frio.md', 134, None),
    148: ('experimentos/organelos/frio_carrera/PREREGISTRO_frio_carrera.md', 145, None),
    149: (REG, 6991, None),
    150: ('experimentos/tronco_v14_4c_examen/ERR_150.md', 1, None),
    # ERR-151: reservado en main para el "ERR-150" de la rama nube (colision de numeracion; ver
    # experimentos/organelos/eco_sel_largo/ENCARGO_NUBE.md:78-80). Se lee con git show, sin merge; el token es ERR-150.
    151: ('git:%s:experimentos/organelos/eco_sel_largo/PREREGISTRO_eco_sel_largo.md' % RAMA_NUBE, 204, 'ERR-150'),
    152: (REG, 7045, None), 153: (REG, 7137, None),
}
# Evidencia de que los huecos no se usaron (se cita en la fila "no encontrado").
EVIDENCIA_HUECO = {
    127: REG + ':6750', 128: REG + ':6750', 129: REG + ':6750',
    135: REG + ':6750', 136: REG + ':6750', 137: REG + ':6750', 138: REG + ':6750', 139: REG + ':6750',
    145: 'experimentos/organelos/prometeo_cuerpo/PREDICCIONES_previas.md:37',
}

MESES = {'sep': 9, 'sept': 9, 'septiembre': 9, 'oct': 10}
RE_ISO = re.compile(r'\b(2026)-(\d{2})-(\d{2})\b')
RE_DIA = re.compile(r'\b(\d{1,2})[- ](sep|sept|septiembre)\b(?:[- ](2026))?', re.I)


def git(*args):
    return subprocess.run(['git', '-C', BASE] + list(args), capture_output=True, text=True, encoding='utf-8').stdout


def lee_lineas(ruta):
    if ruta.startswith('git:'):
        _, ref, archivo = ruta.split(':', 2)
        return git('show', '%s:%s' % (ref, archivo)).split('\n')
    with open(os.path.join(BASE, ruta), encoding='utf-8') as f:
        return f.read().split('\n')


def escanea():
    occ = collections.defaultdict(list)
    for raiz, dirs, archivos in os.walk(BASE):
        rel = os.path.relpath(raiz, BASE).replace(os.sep, '/')
        if rel.split('/')[0] in ('datos', '.git', '.claude') or '__pycache__' in rel:
            continue
        for a in archivos:
            if not a.endswith('.md'):
                continue
            p = os.path.join(raiz, a)
            rp = os.path.relpath(p, BASE).replace(os.sep, '/')
            if rp.startswith('informe/'):
                continue
            try:
                lineas = open(p, encoding='utf-8').read().split('\n')
            except (UnicodeDecodeError, OSError):
                continue
            for i, l in enumerate(lineas, 1):
                for m in re.finditer(r'ERR-0*(\d+)(?!\d)', l):
                    occ[int(m.group(1))].append('%s:%d' % (rp, i))
    return occ


def parrafo(lineas, i0, tope=1500):
    """Texto de la definicion desde la linea i0 (1-based), determinista."""
    primera = lineas[i0 - 1]
    if primera.lstrip().startswith('|'):
        return primera.strip()[:tope]
    out = [primera.strip()]
    es_titulo = primera.lstrip().startswith('#')
    sangria = len(primera) - len(primera.lstrip())
    vistos_blancos = 0
    for l in lineas[i0:i0 + 40]:
        s = l.strip()
        if s.startswith('#'):
            break
        if not s:
            vistos_blancos += 1
            if not es_titulo or vistos_blancos >= 2 or len(out) > 1:
                break
            continue
        ind = len(l) - len(l.lstrip())
        if not es_titulo and (s.startswith('- ') or re.match(r'\d+\. ', s)) and ind <= sangria and len(out) >= 1 \
                and primera.lstrip().startswith(('- ', '* ')) :
            break
        if re.match(r'^[-*]?\s*\**ERR-\d+', s) and len(out) > 1:
            break
        out.append(s)
        if sum(len(x) for x in out) > tope:
            break
    return ' '.join(out)[:tope]


def fecha_de_texto(t):
    m = RE_ISO.search(t)
    if m:
        return '%s-%s-%s' % m.groups()
    m = RE_DIA.search(t)
    if m:
        return '2026-%02d-%02d' % (MESES[m.group(2).lower()], int(m.group(1)))
    return None


def fecha_junto_al_token(texto, patron_token):
    """Sólo cuenta la fecha escrita en el PRIMER paréntesis que abre a <= 70 caracteres del token
    (p. ej. 'ERR-25 (18 sep, 00:35; ...)', 'ERR-150 (28-sep-2026, ...)'). Una fecha en otra parte del párrafo
    suele ser la de otro hecho (la etapa que se cerró, la serie de otro día, el ERR siguiente) y no se usa."""
    m = re.search(patron_token, texto)
    if not m:
        return None
    resto = texto[m.end():]
    p = resto.find('(')
    if p < 0 or p > 70:
        return None
    q = resto.find(')', p)
    dentro = resto[p + 1:q if q > 0 else p + 160]
    return fecha_de_texto(dentro)


def fecha_de_commit(ruta, n, token, linea_txt):
    """Fecha del primer commit que introduce la DEFINICION. Primero busca (git log -S, cadena literal) el fragmento
    de la linea de definicion que empieza en el token (40 caracteres): asi no cuenta menciones previas del numero
    como "el siguiente libre es ERR-N". Si ese fragmento no aparece en la historia (la linea se edito despues),
    cae a la primera aparicion del token en ese archivo (git log -G)."""
    if ruta.startswith('git:'):
        _, ref, archivo = ruta.split(':', 2)
        refs = [ref]
    else:
        archivo, refs = ruta, ['main']
    es_err = token is None or token.startswith('ERR-')
    num = int(token.split('-')[1]) if token and token.startswith('ERR-') else n
    m = re.search(r'ERR-0*%d(?!\d)' % num, linea_txt) if es_err else re.search(re.escape(token), linea_txt)
    intentos = []
    if m:
        intentos.append(('-S', linea_txt[m.start():m.start() + 40]))
    intentos.append(('-G', 'ERR-0*%d([^0-9]|$)' % num if es_err else token))
    for flag, patron in intentos:
        out = git('log', *refs, '--reverse', '--format=%ad %h', '--date=short', flag + patron, '--', archivo)
        out = [x for x in out.split('\n') if x.strip()]
        if out:
            return out[0].split() + [flag]
    return (None, None, None)


def main():
    occ = escanea()
    clasif = json.load(open(os.path.join(INF, 'clasificacion_errores.json'), encoding='utf-8'))
    clasif = {int(k): v for k, v in clasif.items() if not k.startswith('_')}
    defs = {}
    for n in range(1, 154):
        f = FUENTES[n]
        if f is None:
            defs[n] = dict(numero=n, fuente=EVIDENCIA_HUECO.get(n, 'no_determinable'), fecha='no_determinable',
                           origen_fecha='no_determinable', texto='', apariciones=len(occ.get(n, [])))
            continue
        ruta, linea, token = f
        lineas = lee_lineas(ruta)
        l = lineas[linea - 1]
        esperado = token if token else None
        if esperado:
            ok = esperado in l
        else:
            ok = re.search(r'ERR-0*%d(?!\d)' % n, l) is not None
        if not ok:
            sys.exit('ABORTO: %s:%d no contiene %s' % (ruta, linea, esperado or 'ERR-%d' % n))
        texto = parrafo(lineas, linea)
        num = int(token.split('-')[1]) if token and token.startswith('ERR-') else n
        ft = fecha_junto_al_token(texto, r'ERR-0*%d(?!\d)' % num) if (token is None or token.startswith('ERR-')) \
            else None
        if ft:
            fecha, origen = ft, 'texto'
        else:
            fc, h, via = fecha_de_commit(ruta, n, token, l)
            fecha, origen = (fc, 'commit %s (%s)' % (h, via)) if fc else ('no_determinable', 'no_determinable')
        fuente = '%s:%d' % (ruta, linea)
        defs[n] = dict(numero=n, fuente=fuente, fecha=fecha, origen_fecha=origen, texto=texto,
                       apariciones=len(occ.get(n, [])))
    # sobrescrituras de fecha declaradas en la clasificacion (con motivo)
    for n, c in clasif.items():
        if c.get('fecha_manual'):
            defs[n]['fecha'] = c['fecha_manual']
            defs[n]['origen_fecha'] = 'manual: ' + c.get('motivo_fecha', '')
    json.dump(defs, open(os.path.join(INF, 'definiciones_errores.json'), 'w', encoding='utf-8'), ensure_ascii=False,
              indent=1)

    cols = ['numero', 'fecha', 'tipo', 'quien_lo_cometio', 'quien_lo_atrapo', 'tiempo_hasta_detectarlo',
            'altero_conclusion', 'resumen', 'fuente', 'justificacion_tipo']
    filas = []
    faltan = [n for n in range(1, 154) if n not in clasif]
    if faltan:
        sys.exit('ABORTO: faltan clasificaciones para %s' % faltan)
    VOC_T = {'instrumento', 'criterio', 'generalizacion_indebida_del_criterio', 'fabricacion_o_fuera_de_mandato',
             'concurrencia', 'otro', 'no encontrado'}
    VOC_Q = {'coordinador', 'creador', 'auditor', 'compilador', 'cronista', 'probador', 'agente_externo', 'director',
             'nube', 'no_determinable'}
    VOC_A = VOC_Q | {'arnes', 'humo'}
    VOC_TI = {'misma_sesion', 'antes_de_la_serie', 'despues_de_la_serie', 'dias', 'no_determinable'}
    VOC_AC = {'si', 'no', 'no_determinable'}
    for n in range(1, 154):
        c, d = clasif[n], defs[n]
        if c['tipo'] not in VOC_T or c['quien_lo_cometio'] not in VOC_Q or c['quien_lo_atrapo'] not in VOC_A \
                or c['tiempo_hasta_detectarlo'] not in VOC_TI or c['altero_conclusion'] not in VOC_AC:
            sys.exit('ABORTO: vocabulario fuera de lista en ERR-%d: %s' % (n, c))
        if len(c['resumen'].split()) > 20:
            sys.exit('ABORTO: resumen de ERR-%d pasa de 20 palabras' % n)
        if len(c['justificacion_tipo'].split()) > 15:
            sys.exit('ABORTO: justificacion de ERR-%d pasa de 15 palabras' % n)
        if (FUENTES[n] is None) != (c['tipo'] == 'no encontrado'):
            sys.exit('ABORTO: ERR-%d: tipo "no encontrado" no coincide con la tabla de fuentes' % n)
        filas.append({'numero': n, 'fecha': d['fecha'], 'tipo': c['tipo'], 'quien_lo_cometio': c['quien_lo_cometio'],
                      'quien_lo_atrapo': c['quien_lo_atrapo'], 'tiempo_hasta_detectarlo': c['tiempo_hasta_detectarlo'],
                      'altero_conclusion': c['altero_conclusion'], 'resumen': c['resumen'], 'fuente': d['fuente'],
                      'justificacion_tipo': c['justificacion_tipo']})
    with open(os.path.join(INF, 'errores.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(filas)

    existentes = [r['numero'] for r in filas if r['tipo'] != 'no encontrado']
    muestra = random.Random(20260929).sample(existentes, 20)
    with open(os.path.join(INF, 'muestra_20.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=cols + ['clasificacion_director'])
        w.writeheader()
        por_n = {r['numero']: r for r in filas}
        for n in muestra:
            w.writerow(dict(por_n[n], clasificacion_director=''))

    escribe_resumen(filas, existentes, muestra, occ, clasif)
    print('ERR con definicion: %d; no encontrados: %d; muestra: %s' % (
        len(existentes), 153 - len(existentes), sorted(muestra)))


VOCABULARIO = """## Vocabulario y convenciones de la clasificación (decididas antes de contar)
- **tipo**
  - `instrumento`: el código, la copia, el runner, el arnés o el montaje del mundo producen números falsos, perdidos o
    vacíos (comparadores, claves, rutas, kwargs perdidos, casos de arnés mal hechos, mundos que no hacen la prueba).
  - `criterio`: la letra escrita (umbral, banda, puerta, control, medida) no mide lo que dice o no puede fallar o pasar;
    incluye los cambios de letra tras ver datos que se numeraron por la regla 11.
  - `generalizacion_indebida_del_criterio`: un criterio, control o calibración válido en un organismo, etapa o
    instrumento se aplica a otro donde su premisa ya no vale. Nombre tomado del registro (`REGISTRO_etapas_1_2.md:333`).
  - `fabricacion_o_fuera_de_mandato`: afirmación sin la medición que la respalde, o agente que actúa fuera de su mandato
    (matar procesos, lanzar una serie, cambiar la letra por su cuenta).
  - `concurrencia`: choque de procesos o recursos compartidos (Pool, CPU).
  - `otro`: aritmética de una predicción, erratas, omisiones de informe, defecto del organismo (no del método), y los
    números usados para reservas o cláusulas de cierre (`no_es_error`).
- **quien_lo_cometio / quien_lo_atrapo**: sólo se llenan si el texto lo dice ("mío", "creador A", "auditor",
  "cronista", "director"...). `coordinador` = la sesión principal de Claude, incluidos los días 1–4, antes de que
  existieran los roles; cuando el registro habla en primera persona ("mío", "lo encontré"), se asigna a ella.
  `arnes` / `humo` = el fallo lo destapó la corrida de identidad o el humo. Todo lo demás, `no_determinable`.
- **tiempo_hasta_detectarlo**: `antes_de_la_serie` (antes de la serie cuyo resultado habría tocado),
  `despues_de_la_serie` (tras correrla, el mismo día), `dias` (uno o más días después), `misma_sesion` (sin serie de
  por medio: afirmaciones, procedimiento, procesos).
- **altero_conclusion**: `si` sólo si un veredicto o una lectura ya declarada tuvo que corregirse (incluye magnitudes
  y reservas sobre un resultado ya declarado). Las entradas `no_es_error` llevan `no_determinable`: no aplica.
"""


def tabla_cruzada(L, filas, f1, f2):
    v1 = sorted(set(r[f1] for r in filas))
    v2 = sorted(set(r[f2] for r in filas))
    L.append('| %s / %s | %s |' % (f1, f2, ' | '.join(v2)))
    L.append('|---|' + '---|' * len(v2))
    for a in v1:
        L.append('| %s | %s |' % (a, ' | '.join(str(sum(1 for r in filas if r[f1] == a and r[f2] == b)) for b in v2)))
    L.append('')


def escribe_resumen(filas, existentes, muestra, occ, clasif):
    ex = [r for r in filas if r['tipo'] != 'no encontrado']
    no_err = {n for n, c in clasif.items() if c.get('no_es_error')}
    L = ['# Resumen de errores ERR-1 … ERR-153 (generado por `informe/construye_errores.py`; no editar a mano)', '',
         'Generado: %s. Fuente de verdad: `informe/errores.csv` (definiciones en `definiciones_errores.json`, '
         'clasificación en `clasificacion_errores.json`).' % datetime.date.today().isoformat(), '']
    L.append('## Inventario')
    L.append('- Números 1..153: **%d con definición**, **%d "no encontrado"**: %s.' % (
        len(ex), 153 - len(ex), ', '.join(str(r['numero']) for r in filas if r['tipo'] == 'no encontrado')))
    L.append('  Ninguno de esos números aparece en ninguna rama local ni remota (git grep sobre todas las refs). '
             '`REGISTRO_etapas_1_2.md:6750` declara sin uso 127–129 y 135–139; ERR-145 sólo aparece como '
             '"desde ERR-145" en `experimentos/organelos/prometeo_cuerpo/PREDICCIONES_previas.md:37`.')
    L.append('- ERR-1..4 no llevan número escrito: se reconstruyen por el ordinal del registro '
             '(`REGISTRO_etapas_1_2.md:192` y `:333`: "unidades 2H, disponibilidad 2I, aliasing ANOM-01, aritmética '
             'del techo 2K"). `registro/investigacion/sala2/DIAG_metodo.md:361` ya lo notaba ("ERR-01/02/04 con otro formato").')
    L.append('- ERR-151 vive sólo en la rama `%s` (allí se llama "ERR-150"); leído con `git show`.' % RAMA_NUBE)
    mas = sorted(n for n in occ if n > 153)
    L.append('- Números por encima de 153 citados en el árbol: %s (sólo como "siguiente libre").' % (mas or 'ninguno'))
    L.append('- Entradas numeradas que NO describen un error cometido (reservas condicionales, cláusulas de cierre): '
             '%d → %s.' % (len(no_err), ', '.join('ERR-%d' % n for n in sorted(no_err))))
    L.append('- Duplicados e inconsistencias de numeración: ERR-07 dos veces (los artefactos del exp. 2b llaman "ERR-07" '
             'al ERR-09, `REGISTRO_etapas_1_2.md:737-743`); "ERR-150" dos veces (main = T-C ii; rama nube = ERR-151, '
             '`experimentos/organelos/eco_sel_largo/ENCARGO_NUBE.md:78-80`); ERR-151 y ERR-152 son el mismo defecto de '
             'fondo (σ = 0 no apaga los genes enteros); ERR-50 y ERR-51 son el mismo suceso (parada del bloque 4); '
             'ERR-64 tiene variante "ERR-64b" y ERR-37 tiene a/b/c; "ERR-3" se cita como "recalibrar tras ver datos" '
             '(es la regla 3) en `experimentos/criterio_v3/PREREGISTRO_calibracion_v3.md:181`, '
             '`experimentos/criterio_v4/PREREGISTRO_calibracion_v4.md:82` y `experimentos/junta_20260921/A/PROPUESTA.md:91,190`.')
    L.append('')
    L.append(VOCABULARIO)
    for campo in ['tipo', 'quien_lo_cometio', 'quien_lo_atrapo', 'altero_conclusion', 'tiempo_hasta_detectarlo']:
        cnt = collections.Counter(r[campo] for r in ex)
        L.append('## Por %s (n = %d)' % (campo, len(ex)))
        L.append('| valor | n |')
        L.append('|---|---|')
        for k, v in cnt.most_common():
            L.append('| %s | %d |' % (k, v))
        L.append('')
    ex_e = [r for r in ex if r['numero'] not in no_err]
    no_alt = [r for r in ex if r['altero_conclusion'] == 'no']
    si_alt = [r for r in ex if r['altero_conclusion'] == 'si']
    nd_alt = [r for r in ex if r['altero_conclusion'] == 'no_determinable']
    no_alt_e = [r for r in ex_e if r['altero_conclusion'] == 'no']
    si_alt_e = [r for r in ex_e if r['altero_conclusion'] == 'si']
    nd_alt_e = [r for r in ex_e if r['altero_conclusion'] == 'no_determinable']
    antes = [r for r in no_alt_e if r['tiempo_hasta_detectarlo'] == 'antes_de_la_serie']
    L.append('## La X de la tesis')
    L.append('**Cómo se calcula.** X = número de ERR con definición que describen un error (se excluyen las %d '
             'reservas/cláusulas marcadas `no_es_error`) y cuyo `altero_conclusion` es "no": el error se atrapó (en el '
             'arnés, el humo, la auditoría, el registro o una revisión posterior) antes de que un veredicto o una '
             'lectura ya declarada tuviera que corregirse. "si" = hubo que corregir un veredicto o una lectura '
             'declarada. "no_determinable" = el texto no permite decidirlo; no cuenta en X.' % len(no_err))
    L.append('')
    L.append('| universo | n | X (no alteró) | alteró | no determinable |')
    L.append('|---|---|---|---|---|')
    L.append('| **errores (sin reservas/cláusulas)** | %d | **%d** | %d | %d |' % (
        len(ex_e), len(no_alt_e), len(si_alt_e), len(nd_alt_e)))
    L.append('| todos los números con definición | %d | %d | %d | %d |' % (len(ex), len(no_alt), len(si_alt), len(nd_alt)))
    L.append('')
    dud_no = [r for r in no_alt_e if clasif[r['numero']].get('dudoso_altero')]
    dud_si = [r for r in si_alt_e if clasif[r['numero']].get('dudoso_altero')]
    reconstruidos = [r for r in no_alt_e if r['numero'] <= 4]
    L.append('**X = %d de %d errores** (%.0f %%; %d de %d con altero determinable). Sensibilidad a los casos con '
             '`dudoso_altero`: X entre %d (si %s fueran "si") y %d (si %s fueran "no"). Sin los ERR-1..4 '
             'reconstruidos: X = %d de %d. Versión estricta (atrapados antes de correr la serie que habrían tocado): '
             '%d.' % (
                 len(no_alt_e), len(ex_e), 100.0 * len(no_alt_e) / len(ex_e), len(no_alt_e),
                 len(no_alt_e) + len(si_alt_e),
                 len(no_alt_e) - len(dud_no), ', '.join('ERR-%d' % r['numero'] for r in dud_no) or 'ninguno',
                 len(no_alt_e) + len(dud_si), ', '.join('ERR-%d' % r['numero'] for r in dud_si) or 'ninguno',
                 len(no_alt_e) - len(reconstruidos), len(ex_e) - 4, len(antes)))
    L.append('')
    L.append('**Aviso para la tesis:** "153 errores registrados" no es exacto: hay %d números con definición, de los '
             'cuales %d son errores; %d números no se usaron.' % (len(ex), len(ex_e), 153 - len(ex)))
    L.append('')
    L.append('ERR que alteraron una conclusión: %s.' % ', '.join('ERR-%d' % r['numero'] for r in si_alt))
    L.append('')
    L.append('ERR no determinables: %s.' % ', '.join('ERR-%d' % r['numero'] for r in nd_alt))
    L.append('')
    L.append('### Cruces (sólo errores, n = %d)' % len(ex_e))
    tabla_cruzada(L, ex_e, 'tiempo_hasta_detectarlo', 'altero_conclusion')
    tabla_cruzada(L, ex_e, 'tipo', 'altero_conclusion')
    tabla_cruzada(L, ex_e, 'quien_lo_atrapo', 'altero_conclusion')
    L.append('## Casos dudosos (marcados en `clasificacion_errores.json`)')
    for r in ex:
        d = clasif[r['numero']].get('dudoso')
        if d:
            L.append('- ERR-%d (%s, altero %s): %s' % (r['numero'], r['tipo'], r['altero_conclusion'], d))
    L.append('')
    L.append('## Muestra para el director')
    L.append('`informe/muestra_20.csv`: random.Random(20260929).sample(existentes, 20) sobre los %d números con '
             'definición, en ese orden: %s.' % (len(ex), ', '.join(str(n) for n in muestra)))
    L.append('')
    open(os.path.join(INF, 'resumen_errores.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    main()
