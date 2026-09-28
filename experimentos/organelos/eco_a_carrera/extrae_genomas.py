"""extrae_genomas.py — saca de los JSON de ECO_SEL (serie 45301-45320 y replica 45321-45340) los genomas que produjo la seleccion
natural (SEL_C) y su control sin herencia (AZA_C), para llevarlos a la pista de la carrera (bloque eco_a_carrera).

MISION: llegar a la AGI por este camino. Principio del director: que la evolucion construya el organo, no nosotros.

QUE GUARDA ECO_SEL: cada JSON trae 'vivos_final' = [linaje, k, indice, t_nac, 18 genes] de TODOS los cuerpos vivos en T = 1e6 (tope 500;
el maximo medido fue 90). Es decir: SI guarda los genomas completos. No hace falta re-correr nada.

REGLA DE EXTRACCION (fijada ANTES de correr nada en la carrera; no se cambia despues):
  - Para cada semilla ECO y brazo (SEL_C, AZA_C): z = log(g / G0) de los 15 genes del cerebro de cada vivo en T.
  - Genoma de la semilla = el MEDOIDE: el cuerpo vivo real cuyo z esta mas cerca (euclidea) del z medio de los vivos; empate -> el primero.
    Razon: es un genoma que EXISTIO y vivio (coadaptado), con los enteros (memoria_rechazo, NK) ya enteros. El genoma medio
    geometrico se guarda solo como descriptivo.
  - Los 3 genes de historia de vida (dote, rep_umbral, rep_X) no mutaron en C (fuera_mutables = 0): se verifica que son G0 y no se llevan.
  - AZA_C extinto en una semilla: se usa el de la SIGUIENTE semilla de la misma corrida (ciclica) con vivos; se marca 'sustituye'.
  - SEL_M no se lleva: su unico gen (rep_umbral) es historia de vida que en la carrera aplica la PISTA (cambiarlo cambia el mundo y la
    letra del muro). Se declara.

    python experimentos/organelos/eco_a_carrera/extrae_genomas.py            # escribe genomas_eco_sel.json
    python experimentos/organelos/eco_a_carrera/extrae_genomas.py --verifica # re-extrae y compara con el disco
"""
import argparse, hashlib, json, math, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ECO = os.path.join(os.path.dirname(AQUI), 'eco_sel', 'datos')
CORRIDAS = (('serie', 'eco_sel_serie_s45301-45320', 45301), ('replica', 'eco_sel_serie_s45321-45340', 45321))
BRAZOS = ('SEL_C', 'AZA_C')
NG = 15   # genes del cerebro (los mutables de C), en el orden de motor_eco.GENES
SALIDA = os.path.join(AQUI, 'genomas_eco_sel.json')


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]
def h16(p): return h16b(open(p, 'rb').read())


def medoide(V, G0):
    Z = [[math.log(v[j] / G0[j]) for j in range(NG)] for v in V]
    zm = [sum(z[j] for z in Z) / len(Z) for j in range(NG)]
    d = [sum((z[j] - zm[j]) ** 2 for j in range(NG)) for z in Z]
    i = min(range(len(d)), key=lambda k: (d[k], k))
    return i, zm, d[i]


def extrae():
    out = dict(regla='medoide de los vivos en T (log(g/G0), 15 genes del cerebro); AZA extinto -> siguiente semilla con vivos',
               corridas={}, fuentes={})
    genes = G0 = None
    for nom, carpeta, s0 in CORRIDAS:
        out['corridas'][nom] = {}
        for b in BRAZOS:
            por = {}
            for i in range(20):
                s = s0 + i; ruta = os.path.join(ECO, carpeta, f"{b}_s{s}.json")
                raw = open(ruta, 'rb').read(); d = json.loads(raw)
                out['fuentes'][f"{carpeta}/{b}_s{s}.json"] = h16b(raw)
                if genes is None: genes = d['genes']; G0 = d['G0']
                if d['genes'] != genes or d['G0'] != G0: raise SystemExit(f"{ruta}: genes/G0 distintos")
                if d['brazo'] != b or d['seed'] != s or d['mutables'] != genes[:NG]: raise SystemExit(f"{ruta}: brazo/semilla/mutables")
                V = [v[4:] for v in d['vivos_final']]
                if len(d['vivos_final']) != d['vivos_T'] or d['vivos_T'] > 500: raise SystemExit(f"{ruta}: vivos_final truncado")
                if any(v[j] != G0[j] for v in V for j in range(NG, len(G0))): raise SystemExit(f"{ruta}: historia de vida fuera de G0")
                if not V: por[s] = None; continue
                k, zm, dk = medoide(V, G0)
                por[s] = dict(genoma={genes[j]: V[k][j] for j in range(NG)}, n_vivos=len(V), medoide_de=list(d['vivos_final'][k][:4]),
                              dist2_medoide=round(dk, 6), z_medio={genes[j]: round(zm[j], 5) for j in range(NG)},
                              z_medoide={genes[j]: round(math.log(V[k][j] / G0[j]), 5) for j in range(NG)}, K_eco=None)
                ts = d['tam_total']; h = len(ts) // 2
                por[s]['K_eco'] = round(sum(ts[h:]) / len(ts[h:]), 3)
            sem = sorted(por)
            for s in sem:
                if por[s] is None:
                    j = sem.index(s)
                    for t in range(1, 20):
                        s2 = sem[(j + t) % 20]
                        if por[s2] is not None and 'sustituye' not in por[s2]:
                            por[s] = dict(por[s2]); por[s]['sustituye'] = s2; break
            out['corridas'][nom][b] = {str(s): por[s] for s in sem}
    out['genes'] = genes[:NG]; out['G0'] = {genes[j]: G0[j] for j in range(NG)}
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args(argv)
    x = json.dumps(extrae(), ensure_ascii=False, indent=1, sort_keys=True).encode('utf-8')
    if a.verifica:
        ok = os.path.exists(SALIDA) and open(SALIDA, 'rb').read() == x
        print(f"genomas_eco_sel.json sha {h16b(x)} == disco: {ok}")
        return 0 if ok else 1
    with open(SALIDA, 'wb') as fh: fh.write(x)
    print(f"escrito {SALIDA} (sha {h16b(x)}) · extrae_genomas.py sha {h16(os.path.abspath(__file__))}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
