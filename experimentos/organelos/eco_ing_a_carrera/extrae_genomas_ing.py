"""extrae_genomas_ing.py — saca de los JSON de ECO_SEL_ING (serie 46101-46120; replica 46121-46140 cuando este completa) los genomas
que produjo la seleccion con hijos INGENUOS (ING_SEL_C) y su control sin herencia (ING_AZA_C), para llevarlos a la pista de la carrera
(bloque eco_ing_a_carrera).

MISION: llegar a la AGI por este camino. Principio del director: que la evolucion construya el organo, no nosotros.

REGLA DE EXTRACCION = LA DE eco_a_carrera, SIN CAMBIOS (fijada ANTES de correr nada en la carrera): se IMPORTA la funcion medoide() de
eco_a_carrera/extrae_genomas.py (sha 1c8082d17d8e095f, verificado); no se reescribe.
  - Para cada semilla ECO y brazo (ING_SEL_C, ING_AZA_C): z = log(g / G0) de los 15 genes del cerebro de cada vivo en T.
  - Genoma de la semilla = el MEDOIDE (cuerpo vivo real mas cercano al z medio; empate -> el primero).
  - Historia de vida (dote, rep_umbral, rep_X) debe ser G0 en todos los vivos (se verifica; no se lleva).
  - Brazo extinto en una semilla: la SIGUIENTE semilla de la corrida con vivos (ciclica), marcada 'sustituye' (con vivero permanente
    no deberia pasar; se verifica y se cuenta).
Un archivo por corrida (sha propio): genomas_ing_serie.json (el exploratorio y la serie confirmatoria usan SOLO este);
genomas_ing_replica.json (se escribe cuando la replica 46121-46140 esta completa; lo usa solo la replica confirmatoria).

    python experimentos/organelos/eco_ing_a_carrera/extrae_genomas_ing.py --corrida serie [--verifica]
    python experimentos/organelos/eco_ing_a_carrera/extrae_genomas_ing.py --corrida replica [--verifica]
"""
import argparse, hashlib, json, math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EAC = os.path.join(os.path.dirname(AQUI), 'eco_a_carrera')
ECO = os.path.join(os.path.dirname(AQUI), 'eco_sel_ing', 'datos')
SHA_XG = '1c8082d17d8e095f'
CORRIDAS = {'serie': ('eco_sel_ing_serie_s46101-46120_T1000000', 46101), 'replica': ('eco_sel_ing_serie_s46121-46140_T1000000', 46121)}
BRAZOS = ('ING_SEL_C', 'ING_AZA_C')
NG = 15


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def xg():
    p = os.path.join(EAC, 'extrae_genomas.py')
    if h16(p) != SHA_XG: raise SystemExit(f"eco_a_carrera/extrae_genomas.py sha {h16(p)} != {SHA_XG}")
    if EAC not in sys.path: sys.path.insert(0, EAC)
    import extrae_genomas as XG
    if XG.NG != NG: raise SystemExit("NG distinto")
    return XG


def salida(corrida): return os.path.join(AQUI, f"genomas_ing_{corrida}.json")


def extrae(corrida):
    XG = xg()
    carpeta, s0 = CORRIDAS[corrida]
    out = dict(regla='medoide de los vivos en T (log(g/G0), 15 genes del cerebro; eco_a_carrera/extrae_genomas.medoide importada); '
                     'extinto -> siguiente semilla con vivos', corrida=corrida, carpeta=carpeta, brazos={}, fuentes={})
    genes = G0 = None
    for b in BRAZOS:
        por = {}
        for i in range(20):
            s = s0 + i; ruta = os.path.join(ECO, carpeta, f"{b}_s{s}.json")
            raw = open(ruta, 'rb').read(); d = json.loads(raw)
            out['fuentes'][f"{carpeta}/{b}_s{s}.json"] = h16b(raw)
            if genes is None: genes = d['genes']; G0 = d['G0']
            if d['genes'] != genes or d['G0'] != G0: raise SystemExit(f"{ruta}: genes/G0 distintos")
            if d['brazo'] != b or d['seed'] != s or d['mutables'] != genes[:NG] or d.get('aborto'): raise SystemExit(f"{ruta}: brazo/semilla/mutables/aborto")
            V = [v[4:] for v in d['vivos_final']]
            if len(d['vivos_final']) != d['vivos_T'] or d['vivos_T'] > 500: raise SystemExit(f"{ruta}: vivos_final truncado")
            if any(v[j] != G0[j] for v in V for j in range(NG, len(G0))): raise SystemExit(f"{ruta}: historia de vida fuera de G0")
            if not V: por[s] = None; continue
            k, zm, dk = XG.medoide(V, G0)
            ts = d['tam_total']; h = len(ts) // 2
            por[s] = dict(genoma={genes[j]: V[k][j] for j in range(NG)}, n_vivos=len(V), medoide_de=list(d['vivos_final'][k][:4]),
                          dist2_medoide=round(dk, 6), z_medio={genes[j]: round(zm[j], 5) for j in range(NG)},
                          z_medoide={genes[j]: round(math.log(V[k][j] / G0[j]), 5) for j in range(NG)},
                          K_eco=round(sum(ts[h:]) / len(ts[h:]), 3), K_nac_eco=d.get('K_nac'), fund_2a_eco=d.get('fund_2a'))
        sem = sorted(por)
        for s in sem:
            if por[s] is None:
                j = sem.index(s)
                for t in range(1, 20):
                    s2 = sem[(j + t) % 20]
                    if por[s2] is not None and 'sustituye' not in por[s2]:
                        por[s] = dict(por[s2]); por[s]['sustituye'] = s2; break
        out['brazos'][b] = {str(s): por[s] for s in sem}
    out['genes'] = genes[:NG]; out['G0'] = {genes[j]: G0[j] for j in range(NG)}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--corrida', choices=sorted(CORRIDAS), required=True)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    x = json.dumps(extrae(a.corrida), ensure_ascii=False, indent=1, sort_keys=True).encode('utf-8')
    S = salida(a.corrida)
    if a.verifica:
        ok = os.path.exists(S) and open(S, 'rb').read() == x
        print(f"{os.path.basename(S)} sha {h16b(x)} == disco: {ok}")
        return 0 if ok else 1
    with open(S, 'wb') as fh: fh.write(x)
    print(f"escrito {S} (sha {h16b(x)}) · extrae_genomas_ing.py sha {h16(os.path.abspath(__file__))}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
