"""DIAGNOSTICO ESTRUCTURAL de los codigos de Kenyon — NO corre el organismo: construye `KW` con el rng de la
semilla, pasa el bucle de rechazo de `cond()` (el mismo de organismo_v14, copiado aqui y verificado contra el sha
del tronco) y lee los codigos de A, B, C y D. Cuesta milisegundos por semilla y no simula ni un paso.

Para que sirve (ERR-37, Enmienda 2 de PREREGISTRO_mundo_vivo.md y PREREGISTRO_supersticion_sal.md):
en 181-200, las DOS unicas semillas donde el valor de la sal muda se desvia de 0 (182: -1.83, 188: -1.34) son
EXACTAMENTE las dos donde |code(D) & code(B)| = 3, es decir donde **la sal y el veneno tienen el MISMO codigo**:
para la via rapida son el mismo estimulo. Esa condicion se puede calcular ANTES de correr, asi que sirve como
criterio de validez de un subconjunto PREREGISTRADO (regla 10 de EQUIPO.md: preregistrado antes de la serie
nueva, ejecutado por un script del repositorio, y el conjunto completo se reporta al lado).

    python experimentos/nivel11_mundo_vivo/diagnostico_codigos.py --desde 201 --n 20
    python experimentos/nivel11_mundo_vivo/diagnostico_codigos.py --desde 221 --n 200 --alias 3   (buscar semillas alias)

Salida: tabla por semilla con los solapamientos, las listas `alias` (|D&B| = 3) y `limpias` (|D&B| = 0), y un JSON
en esta carpeta si se pasa --json.
"""
import argparse, hashlib, json, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import organismo_v14 as V14
SHA_V14_ESPERADO = 'feefc88b1fd8d434'


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def codigos(seed, solap_AB=None):
    """Las mismas cinco lineas del arranque de organismo_v14.run (leidas, no importadas: `code` es local a run).
    Si el sha del tronco cambia, este script avisa: la copia hay que revisarla a mano."""
    L, NK, NKMAX, K, PAT = V14.L, V14.NK, V14.NKMAX, V14.K, V14.PAT
    rng = np.random.default_rng(seed)
    rng.uniform(.1, .4, (2, 9))                                  # Wl: consume el rng igual que el tronco
    KW = np.zeros((NKMAX, 6)); activa = np.zeros(NKMAX, bool)
    KW[:NK] = rng.uniform(0, 1, (NK, 6)); activa[:NK] = True

    def code(P):
        v = KW @ P; v = np.where(activa, v, -1e9); return set(np.argsort(v)[-K:])

    obj = 0 if solap_AB is None else solap_AB
    if solap_AB:
        KW[:solap_AB] = 0; KW[:solap_AB, 0] = 5.0
    while len(code(PAT['A']) & code(PAT['B'])) != obj:
        KW[obj:NK] = rng.uniform(0, 1, (NK - obj, 6))
    return {k: code(PAT[k]) for k in 'ABCD'}


def solapamientos(seed):
    c = codigos(seed)
    return {f'{a}&{b}': len(c[a] & c[b]) for a, b in (('D', 'A'), ('D', 'B'), ('D', 'C'), ('C', 'A'), ('C', 'B'))}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--desde', type=int, default=181)
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--alias', type=int, default=3, help="|D&B| que define ALIAS (3 = mismo codigo, K=3)")
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    s14 = h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'))
    print(f"  sha organismo_v14 {s14}" + ("" if s14 == SHA_V14_ESPERADO else
          f"  *** CAMBIO respecto de {SHA_V14_ESPERADO}: revisar a mano la copia de codigos()"))
    print(f"  diagnostico ESTRUCTURAL, sin correr el organismo. Semillas {a.desde}-{a.desde+a.n-1}\n")
    print("  seed   D&A D&B D&C   C&A C&B   marca")
    filas = {}
    for s in range(a.desde, a.desde + a.n):
        o = solapamientos(s); filas[s] = o
        m = 'ALIAS sal==veneno' if o['D&B'] >= a.alias else ('alias sal==agua' if o['D&C'] >= a.alias else '')
        print(f"  {s}    {o['D&A']}   {o['D&B']}   {o['D&C']}    {o['C&A']}   {o['C&B']}   {m}")
    alias = [s for s, o in filas.items() if o['D&B'] >= a.alias]
    limpias = [s for s, o in filas.items() if o['D&B'] == 0]
    print(f"\n  ALIAS   (|D&B| >= {a.alias}): {len(alias)}/{a.n}  {alias}")
    print(f"  LIMPIAS (|D&B| == 0):      {len(limpias)}/{a.n}  {limpias}")
    if a.json:
        d = os.path.join(AQUI, f'codigos_s{a.desde}-{a.desde+a.n-1}.json')
        json.dump(dict(sha_organismo_v14=s14, desde=a.desde, n=a.n, umbral_alias=a.alias,
                       solapamientos={str(k): v for k, v in filas.items()}, alias=alias, limpias=limpias),
                  open(d, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"  -> {os.path.basename(d)}  sha256_16 = {h16(d)}")
