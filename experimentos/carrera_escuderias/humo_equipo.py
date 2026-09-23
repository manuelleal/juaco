"""humo_equipo.py — EL UNICO GUION DE HUMO DE LOS EQUIPOS DE LA RONDA 2 (ENMIENDA 5). Los equipos no usan guiones propios.

MISION: llegar a la AGI por este camino. Un humo = UN proceso, UNA semilla, fundador limpio, con el mismo juez de la serie
(juez.tarea + el criterio de la ronda 2). Reglas que este guion IMPONE (no la buena fe):
  - equipo O2, O3 u O4; cada uno SOLO en su tercio de semillas de practica: O2 9001-9033, O3 9034-9066, O4 9067-9099;
  - T <= 30000;  tope de 12 humos por equipo (se cuentan los JSON ya escritos en datos/humos_r2/<X>/);
  - revisa_carro sobre cada carro distinto antes de correr; si falta un carro, error claro;
  - fundador limpio SIEMPRE (la pista lo impone en la ronda 2).
Modos:  mono = 9 del equipo · fab = 3 del equipo + 6 FABRICA · mix = 3 O2 + 3 O3 + 3 O4 (exige los tres carros).
Escribe en datos/humos_r2/<X>/: humo_<X>_<modo>_s<S>_T<T>_<sello>.json (+ .log y la pizarra completa .jsonl.gz).
Uso:  python experimentos/carrera_escuderias/humo_equipo.py --equipo O2 --modo mono --semilla 9001 --T 20000
"""
import argparse, gzip, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pista as P
import juez as J
import revisa_carro as RC

TERCIOS = {'O2': (9001, 9033), 'O3': (9034, 9066), 'O4': (9067, 9099)}
T_MAX = 30000
TOPE = 12


def carros_de(equipo, modo):
    return {'mono': [equipo] * 9, 'fab': [equipo] * 3 + ['FABRICA'] * 6, 'mix': ['O2'] * 3 + ['O3'] * 3 + ['O4'] * 3}[modo]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--equipo', required=True, choices=sorted(TERCIOS))
    ap.add_argument('--modo', required=True, choices=('mono', 'fab', 'mix'))
    ap.add_argument('--semilla', type=int, required=True)
    ap.add_argument('--T', type=int, required=True)
    a = ap.parse_args(argv)
    lo, hi = TERCIOS[a.equipo]
    if not lo <= a.semilla <= hi:
        raise SystemExit(f"HUMO: la semilla {a.semilla} esta FUERA del tercio de {a.equipo} ({lo}-{hi}). No se corre.")
    if not 1 <= a.T <= T_MAX:
        raise SystemExit(f"HUMO: T={a.T} fuera de 1..{T_MAX} (ENMIENDA 5, regla 6). No se corre.")
    carp = os.path.join(AQUI, 'datos', 'humos_r2', a.equipo)
    hechos = sorted(f for f in os.listdir(carp) if f.startswith('humo_') and f.endswith('.json')) if os.path.isdir(carp) else []
    if len(hechos) >= TOPE:
        raise SystemExit(f"HUMO: {a.equipo} ya uso sus {TOPE} humos ({len(hechos)} en {carp}). No se corre.")
    carros = carros_de(a.equipo, a.modo)
    falta = sorted({c for c in carros if not os.path.exists(os.path.join(P.CARROS, c + '.py'))})
    if falta:
        raise SystemExit(f"HUMO: falta {', '.join('carros/' + c + '.py' for c in falta)} (modo {a.modo}). No se corre.")
    rv = {c: RC.revisa(c) for c in sorted(set(carros))}
    if any(rv.values()):
        raise SystemExit("HUMO: chequeo estatico RECHAZADO: " + json.dumps(rv, ensure_ascii=False))
    os.makedirs(carp, exist_ok=True)   # recien aqui: un humo rechazado por los guardias no deja carpeta
    sel = time.strftime('%Y%m%d_%H%M%S'); pre = os.path.join(carp, f"humo_{a.equipo}_{a.modo}_s{a.semilla}_T{a.T}_{sel}")
    LOGF = open(pre + '.log', 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    shas = {c: P.h16(os.path.join(P.CARROS, c + '.py')) for c in sorted(set(carros))}
    log(f"HUMO RONDA 2 · equipo {a.equipo} · modo {a.modo} · semilla {a.semilla} · T={a.T} · fundador limpio · humo {len(hechos) + 1}/{TOPE}")
    log(f"  carros {carros} · sha {shas} · pista {P.h16(os.path.join(AQUI, 'pista.py'))} · juez {P.h16(os.path.join(AQUI, 'juez.py'))} · chequeo estatico PASA")
    x = J.tarea((a.semilla, carros, a.T, 1, 0, 1, None, 1))
    piz = x.pop('pizarra_log')
    with gzip.open(pre + '_pizarra.jsonl.gz', 'wt', encoding='utf-8') as fz:
        for e in piz: fz.write(json.dumps([a.semilla] + e) + chr(10))
    R = [x]
    tab, r0p = J.informe(R, dict(etiqueta=f"humo {a.equipo} {a.modo}", semillas=[a.semilla], T=a.T, pizarra=1, rep_acum=0), log)
    r2 = J.resumen_r2(R, log, f"r2{'mono' if a.modo == 'mono' else ('fab' if a.modo == 'fab' else 'mix3')}")
    json.dump(dict(meta=dict(equipo=a.equipo, modo=a.modo, semilla=a.semilla, T=a.T, fundador_limpio=1, carros=carros, sha_carros=shas,
                             sha_pista=P.h16(os.path.join(AQUI, 'pista.py')), sha_juez=P.h16(os.path.join(AQUI, 'juez.py')), sello=sel,
                             humo_n=len(hechos) + 1, tope=TOPE), corrida=x, tabla=tab, ronda2=r2),
              open(pre + '.json', 'w', encoding='utf-8'), ensure_ascii=False)
    log(f"  JSON {pre}.json · {time.time() - t0:.1f}s · te quedan {TOPE - len(hechos) - 1} humos")
    return 0


if __name__ == '__main__':
    sys.exit(main())
