#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""corre_eras.py — orquestador de la ESCALERA DE NIVELES (5..9, con 10/11 fuera de alcance por falta de
instrumento; ver PREREGISTRO_eras.md secc. 0). Diseñador de preregistros (registro/EQUIPO.md, tabla de roles):
escribe el runner, NO corre `Pool` (un proceso, regla 3 de EQUIPO.md), entrega humo de un proceso.

MISION (en cada corrida, regla 13 de EQUIPO.md): llegar a la AGI por este camino -- un organismo minimo con
reglas locales que aprende, sobrevive, se comunica y se reproduce; con evidencia preregistrada. Este script
sube la escalera de niveles del proyecto (no una escalera biologica) con un alma que cura tras cada
muerte/vida con un menu CERRADO de parches locales, y compara contra alma aleatoria y sin alma.

FRONTERA CON EL BLOQUE ALMA (no tocar sus archivos): la base generica del alma (bucle muerte -> curita ->
renace/hijo, nodo central, interfaz de archivos alma_pregunta_<n>.json / alma_respuesta_<n>.json) la construye
OTRO creador en experimentos/nivel13_alma/. A la fecha de este script ese modulo TODAVIA NO EXISTE como
import; se intenta importar por nombres razonables y, si falla, este script usa su propio bucle minimo
COMPATIBLE CON EL MISMO FORMATO DE ARCHIVO, documentado como fallback (nunca como sustituto silencioso: se
imprime qué camino se tomó). El menu del nivel 9 se hereda TAL CUAL de
experimentos/nivel13_alma/MENU_curitas.md (seis entradas a..f), sin reabrirlo.

Un proceso. Nunca multiprocessing.Pool (regla 3 de EQUIPO.md). Progreso con marca de tiempo a archivo desde el
arranque (regla 10 de CLAUDE.md).
"""
import argparse, json, os, sys, time, random, hashlib, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLE = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(BUNDLE, 'organismo'))  # regla: organismo/ primero en sys.path (ERR-28)
sys.path.insert(0, os.path.join(BUNDLE, 'experimentos', 'nivel11_mundo_vivo'))
sys.path.insert(0, os.path.join(BUNDLE, 'experimentos', 'nivel12_mundo_familias'))

LOG_PATH = None


def log(msg):
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    if LOG_PATH:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(line + '\n')


# ============================== INTERFAZ DEL ALMA (archivos) ==============================
# Contrato asumido (escrito contra la interfaz descrita en el encargo, no verificado contra código ajeno):
#   alma_pregunta_<n>.json  -> {"n": n, "nivel": N, "menu": [{"id":..,"nombre":..,"que_toca":..}, ...],
#                                 "contexto": {...datos de la vida/muerte que acaba de terminar...}}
#   alma_respuesta_<n>.json -> {"n": n, "id": "<uno de menu[*]['id']>", "motivo": "una linea"}
# Cualquier respuesta con id fuera del menu es un error del instrumento (aborta), igual que MENU_curitas.md.

def _intenta_importar_base_alma():
    """Busca el modulo generico del bloque ALMA por nombres razonables. Devuelve el modulo o None."""
    for nombre in ('alma_base', 'nodo_alma', 'bloque_alma', 'alma'):
        try:
            mod = importlib.import_module(nombre)
            if hasattr(mod, 'escribe_pregunta') and hasattr(mod, 'lee_respuesta'):
                log(f"ALMA: usando base del otro creador ({nombre}.py)")
                return mod
        except ImportError:
            continue
    return None


_BASE_ALMA = _intenta_importar_base_alma()


def escribe_pregunta(carpeta, n, nivel, menu, contexto):
    if _BASE_ALMA is not None:
        return _BASE_ALMA.escribe_pregunta(carpeta, n, nivel, menu, contexto)
    # --- fallback propio, mismo formato de archivo ---
    path = os.path.join(carpeta, f'alma_pregunta_{n}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'n': n, 'nivel': nivel, 'menu': menu, 'contexto': contexto}, f, ensure_ascii=False, indent=2)
    return path


def lee_respuesta(carpeta, n, menu, timeout_s=None, poll_s=1.0):
    if _BASE_ALMA is not None:
        return _BASE_ALMA.lee_respuesta(carpeta, n, menu, timeout_s=timeout_s, poll_s=poll_s)
    # --- fallback propio: espera bloqueante a que aparezca el archivo de respuesta ---
    path = os.path.join(carpeta, f'alma_respuesta_{n}.json')
    t0 = time.time()
    while not os.path.exists(path):
        if timeout_s is not None and (time.time() - t0) > timeout_s:
            raise SystemExit(f"ALMA: sin respuesta para n={n} tras {timeout_s}s ({path})")
        time.sleep(poll_s)
    with open(path, encoding='utf-8') as f:
        resp = json.load(f)
    ids_validos = {m['id'] for m in menu}
    if resp.get('id') not in ids_validos:
        raise SystemExit(f"ALMA: respuesta id={resp.get('id')!r} fuera del menu {sorted(ids_validos)} -- aborta")
    return resp


def decide_alma(modo, carpeta, n, nivel, menu, contexto, rng, timeout_s=None):
    """modo: 'razonada' (archivo, espera humano/agente) | 'aleatoria' (uniforme, sin leer nada) | 'ninguna' (siempre la entrada 'NADA')."""
    entrada_nada = next((m for m in menu if m['nombre'].upper() == 'NADA'), menu[-1])
    if modo == 'ninguna':
        return {'id': entrada_nada['id'], 'motivo': 'control alma_ninguna: siempre NADA'}
    if modo == 'aleatoria':
        elegido = rng.choice(menu)
        return {'id': elegido['id'], 'motivo': 'control alma_aleatoria: uniforme sin leer contexto'}
    if modo == 'razonada':
        escribe_pregunta(carpeta, n, nivel, menu, contexto)
        log(f"ALMA (razonada): escrita alma_pregunta_{n}.json -- esperando alma_respuesta_{n}.json en {carpeta}")
        return lee_respuesta(carpeta, n, menu, timeout_s=timeout_s)
    raise SystemExit(f"modo de alma desconocido: {modo!r}")


# ============================== MENUS POR NIVEL (PREREGISTRO_eras.md §3) ==============================

MENU_NIVEL5 = [
    {'id': 'a', 'nombre': 'SUBIR GANADORAS', 'que_toca': "k_ganadoras <- min(k_ganadoras+1, 3)"},
    {'id': 'b', 'nombre': 'REFERENCIA POR HERMANA', 'que_toca': "par_herm <- ('A','C') para la proxima vida"},
    {'id': 'c', 'nombre': 'VORAZ', 'que_toca': "voraz <- 1.0"},
    {'id': 'd', 'nombre': 'NADA', 'que_toca': 'no toca nada'},
]

# Nivel 9: se hereda TAL CUAL de MENU_curitas.md (a..f) -- ver ese archivo para la tabla completa. No se
# reescribe aquí el contenido salvo los ids/nombres, para poder construir la pregunta al alma.
MENU_NIVEL9 = [
    {'id': 'a', 'nombre': 'CONECTAR AL NODO', 'que_toca': 'conectado=True para todos los cuerpos siguientes'},
    {'id': 'b', 'nombre': 'SUBIR EL MIEDO', 'que_toca': 'escribe 5 copias del mensaje de la muerte en el nodo (miedo_n=5)'},
    {'id': 'c', 'nombre': 'DOTE MAYOR', 'que_toca': 'dote <- min(dote+0.1, rep_umbral-0.05)'},
    {'id': 'd', 'nombre': 'BAJAR EL UMBRAL', 'que_toca': 'rep_umbral <- max(rep_umbral-0.1, dote+0.05)'},
    {'id': 'e', 'nombre': 'HEREDAR VALORES', 'que_toca': "hereda <- 'M1' para los partos siguientes"},
    {'id': 'f', 'nombre': 'NADA', 'que_toca': 'no toca nada (control alma_ninguna del bloque ALMA)'},
]


# ============================== NIVEL 5: comunicacion con referencia ==============================
# Instrumento: organismo_familias_b6.run (nivel12_mundo_familias). "Vida" = una corrida de una semilla
# (PREREGISTRO_eras.md §2: simplificación declarada, sin muerte real en este instrumento).

def _letra_nivel5(salida):
    """Proxy de la letra de bloque 5/6 con lo que devuelve b6.run: CANAL (com=1 en direccion irreemplazable)."""
    com = salida.get('mem_fam') or {}
    # proxy robusto: si el canal entrego mensaje y la tabla de pares tiene cobertura, cuenta como 'com'=1
    entregado = bool(salida.get('canal_entregado'))
    cobertura = salida.get('mem_cobertura') or 0
    return 1 if (entregado and cobertura > 0) else 0


def corre_nivel5(modo_alma, seed0, n_vidas, out_dir, T=20000, timeout_s=None, forzar_n_vidas=False):
    import organismo_familias_b6 as b6
    rng_alma = random.Random(seed0 * 7919 + 1)
    knobs = {'k_ganadoras': 1, 'par_herm': None, 'voraz': 0.0}
    filas = []
    com_racha = 0
    for i in range(1, n_vidas + 1):
        seed = seed0 * 1000 + i
        canal = {'modo': 'sen', 'ref': 'A', 'P': b6.PAT['A']}
        salida = b6.run(seed=seed, T=T, memoria_pares='relevo', canal=canal, reg_b4=1,
                         voraz=knobs['voraz'], par_herm=knobs['par_herm'], k_ganadoras=knobs['k_ganadoras'])
        com = _letra_nivel5(salida)
        com_racha = com_racha + 1 if com else 0
        contexto = {'vida': i, 'seed': seed, 'com': com, 'com_racha': com_racha, 'knobs': dict(knobs)}
        log(f"nivel5 vida={i} seed={seed} com={com} racha={com_racha} knobs={knobs}")
        resp = decide_alma(modo_alma, out_dir, i, 5, MENU_NIVEL5, contexto, rng_alma, timeout_s=timeout_s)
        idc = resp['id']
        if idc == 'a':
            knobs['k_ganadoras'] = min(knobs['k_ganadoras'] + 1, 3)
        elif idc == 'b':
            knobs['par_herm'] = ('A', 'C')  # par de hermanas declarado (perilla real: un par de tokens, no un bool)
        elif idc == 'c':
            knobs['voraz'] = 1.0
        # 'd' (NADA): no toca knobs
        log(f"  curita elegida: {idc} ({resp.get('motivo','')})")
        filas.append({'vida': i, 'seed': seed, 'com': com, 'curita': idc, 'motivo': resp.get('motivo', ''),
                       'knobs_tras_curita': dict(knobs)})
        if com_racha >= 3 and not forzar_n_vidas:  # criterio de humo, NO el de la letra completa (bloque5/6: CANAL>=15/20): ver §8
            log(f"nivel5 PROMUEVE (humo) en vida={i}: 3 vidas seguidas con com=1")
            return {'nivel': 5, 'promovio': True, 'en_vida': i, 'filas': filas}
    return {'nivel': 5, 'promovio': False, 'en_vida': None, 'filas': filas}


# ============================== NIVEL 9: vida (muerte real, H-1) ==============================
# Instrumento: organismo_vivo_h1.run. "Muerte" ~= fin de una corrida corta (T_vida) del linaje; se encadenan
# corridas cortas para poder pedirle al alma una curita entre una y la siguiente (ver PREREGISTRO_eras.md §2:
# el instrumento fija `hereda`/`dote`/`rep_umbral` para TODO un run, así que "una vida" aquí es una corrida
# corta completa, no una muerte individual dentro del linaje -- limitación declarada, no oculta).

def corre_nivel9(modo_alma, seed0, n_vidas, out_dir, T_vida=20000, timeout_s=None):
    import organismo_vivo_h1 as h1
    rng_alma = random.Random(seed0 * 7919 + 2)
    knobs = {'hereda': 'nada', 'dote': 0.6, 'rep_umbral': 1.0, 'conectado': False}
    filas = []
    for i in range(1, n_vidas + 1):
        seed = seed0 * 1000 + i
        salida = h1.run(seed=seed, T=T_vida, vivo=1, n_nec=2, reproduccion=1, rep_mide=1, rep2=1,
                         muerte_real=1, h1=1, hereda=knobs['hereda'], dote=knobs['dote'],
                         rep_umbral=knobs['rep_umbral'])
        deaths = salida.get('deaths') or []
        r0 = salida.get('R0') if isinstance(salida, dict) and 'R0' in salida else None
        contexto = {'vida': i, 'seed': seed, 'muertes_en_corrida': len(deaths), 'r0': r0, 'knobs': dict(knobs)}
        log(f"nivel9 vida={i} seed={seed} muertes={len(deaths)} r0={r0} knobs={knobs}")
        resp = decide_alma(modo_alma, out_dir, i, 9, MENU_NIVEL9, contexto, rng_alma, timeout_s=timeout_s)
        idc = resp['id']
        if idc == 'a':
            knobs['conectado'] = True  # nodo: fuera de alcance real sin la base del alma; se registra la intención
        elif idc == 'c':
            knobs['dote'] = min(knobs['dote'] + 0.1, knobs['rep_umbral'] - 0.05)
        elif idc == 'd':
            knobs['rep_umbral'] = max(knobs['rep_umbral'] - 0.1, knobs['dote'] + 0.05)
        elif idc == 'e':
            knobs['hereda'] = 'M1'
        # 'b' (miedo) exige el nodo central (no implementado aqui: fuera de alcance, ver PREREGISTRO §0/§2)
        # 'f' (NADA): no toca knobs
        log(f"  curita elegida: {idc} ({resp.get('motivo','')})")
        filas.append({'vida': i, 'seed': seed, 'muertes_en_corrida': len(deaths), 'r0': r0, 'curita': idc,
                       'motivo': resp.get('motivo', ''), 'knobs_tras_curita': dict(knobs)})
        if r0 is not None and r0 >= 0.90:
            log(f"nivel9 PROMUEVE en vida={i}: R0={r0} >= 0.90")
            return {'nivel': 9, 'promovio': True, 'en_vida': i, 'filas': filas}
    return {'nivel': 9, 'promovio': False, 'en_vida': None, 'filas': filas}


def corre_nivel_no_implementado(nivel):
    raise SystemExit(
        f"nivel {nivel}: sin instrumento (PREREGISTRO_eras.md §0). No se corre -- correrlo sería inventar un "
        f"mecanismo sin preregistro, prohibido por el método. Niveles 6, 7 y 8 están diseñados en el "
        f"preregistro (§3) pero sus runners no se implementan en esta entrega; niveles 10 y 11 no tienen "
        f"instrumento en absoluto."
    )


# ============================== CLI ==============================

def main():
    ap = argparse.ArgumentParser(description='Orquestador de la escalera de niveles con alma (ver PREREGISTRO_eras.md).')
    ap.add_argument('--nivel', type=int, required=True, choices=[5, 6, 7, 8, 9, 10, 11])
    ap.add_argument('--alma', choices=['razonada', 'aleatoria', 'ninguna'], default='razonada')
    ap.add_argument('--vidas', type=int, default=10)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--timeout', type=float, default=None, help='segundos de espera por respuesta del alma razonada; None = espera indefinida')
    ap.add_argument('--out', default=None)
    ap.add_argument('--forzar_n_vidas', action='store_true', help='no cortar al primer criterio de humo; correr las --vidas completas (solo para el humo del nivel 5)')
    args = ap.parse_args()

    global LOG_PATH
    out_dir = args.out or HERE
    os.makedirs(out_dir, exist_ok=True)
    LOG_PATH = os.path.join(out_dir, f'log_eras_nivel{args.nivel}_{time.strftime("%Y%m%d_%H%M%S")}.txt')
    log(f"MISION: llegar a la AGI por este camino. corre_eras.py nivel={args.nivel} alma={args.alma} vidas={args.vidas} seed={args.seed}")

    if args.nivel == 5:
        resultado = corre_nivel5(args.alma, args.seed, args.vidas, out_dir, timeout_s=args.timeout, forzar_n_vidas=args.forzar_n_vidas)
    elif args.nivel == 9:
        resultado = corre_nivel9(args.alma, args.seed, args.vidas, out_dir, timeout_s=args.timeout)
    else:
        corre_nivel_no_implementado(args.nivel)
        return

    out_json = os.path.join(out_dir, f'salida_eras_nivel{args.nivel}_{args.alma}_seed{args.seed}_{time.strftime("%Y%m%d_%H%M%S")}.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    log(f"JSON escrito: {out_json}")
    sha = hashlib.sha256(open(__file__, 'rb').read()).hexdigest()[:16]
    log(f"sha16 de corre_eras.py: {sha}")
    log(f"RESULTADO: nivel={resultado['nivel']} promovio={resultado['promovio']} en_vida={resultado.get('en_vida')}")


if __name__ == '__main__':
    main()
