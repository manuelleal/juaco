"""JUACO-EVO — evalua todos los candidatos de una generacion y aplica la REGLA DE SELECCION de PREREGISTRO_evo.md §3.
No decide nada que no este alli. La auditoria del diff del ganador (P4) es humana/agente y va DESPUES de este script.

Uso:  python selecciona.py <gen> <padre.py> <padre_train.json> <padre_heldout.json>
Lee gen{gen}/*/organismo.py (+ hipotesis.md), escribe gen{gen}/<cand>/train.json, gen{gen}/puntuaciones.json y, si hay
ganador, gen{gen}/<ganador>/heldout.json. Regla: reemplaza al padre si (a) H1-H3, (b) R >= R_padre+0.1 o
(R >= R_padre y SEC mejora >= 0.05), (c) R en retenidas >= R_padre_retenidas - 0.1. Empates: mayor R, luego mayor SEC.
"""
import sys, os, json, time, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evalua import evalua, h16

AQUI = os.path.dirname(os.path.abspath(__file__))
TRAIN = list(range(1, 11)); HELD = list(range(11, 21))


def log(msg=""):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


if __name__ == '__main__':
    gen = sys.argv[1]; padre = os.path.abspath(sys.argv[2])   # etiqueta de generacion: '1', '2', '1c' (linaje ciego)...
    pt = json.load(open(sys.argv[3], encoding='utf-8')); ph = json.load(open(sys.argv[4], encoding='utf-8'))
    Rp, SECp, Rph = pt['R'], pt['SEC'], ph['R']
    log(f"gen{gen}: padre {os.path.basename(padre)} ({h16(padre)}) R={Rp} SEC={SECp} R_retenidas={Rph}")
    cands = sorted(glob.glob(os.path.join(AQUI, f'gen{gen}', '*', 'organismo.py')))
    tabla = []
    for p in cands:
        nombre = os.path.basename(os.path.dirname(p))
        hip = os.path.join(os.path.dirname(p), 'hipotesis.md')
        log(f"  evaluando {nombre} ({h16(p)})...")
        o = evalua(p, padre, TRAIN)
        o['candidato'] = nombre; o['operador'] = 'llm' if nombre.startswith('llm') else 'ciega'
        o['hipotesis'] = open(hip, encoding='utf-8').read()[:600] if os.path.exists(hip) else None
        json.dump(o, open(os.path.join(os.path.dirname(p), 'train.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        elegible = bool(o.get('valido')) and (o['R'] >= Rp + 0.1 or (o['R'] >= Rp and o['SEC'] - SECp >= 0.05))
        o['elegible'] = elegible
        tabla.append(o)
        log(f"    valido={o.get('valido')} H1={o.get('H1')} H2={o.get('H2')} H3={o.get('H3')} R={o.get('R')} S={o.get('S')} E={o.get('E')} C={o.get('C')} SEC={o.get('SEC')}"
            f" W_B100={o.get('W_B100_mediana')} muertesE1={o.get('muertes_E1')} splitsE2L={o.get('splits_E2L')} elegible={elegible}"
            + (f"  ROTO: {o['error'][-120:]}" if o.get('error') else ""))
    eleg = sorted([o for o in tabla if o['elegible']], key=lambda o: (o['R'], o['SEC']), reverse=True)
    ganador = None
    for o in eleg:
        p = os.path.join(AQUI, f'gen{gen}', o['candidato'], 'organismo.py')
        log(f"  candidato a ganador {o['candidato']}: evaluando en semillas retenidas 11-20...")
        h = evalua(p, padre, HELD)
        json.dump(h, open(os.path.join(os.path.dirname(p), 'heldout.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        o['R_retenidas'] = h.get('R'); o['valido_retenidas'] = h.get('valido')
        if h.get('valido') and h['R'] >= Rph - 0.1:
            ganador = o['candidato']; log(f"  GANADOR gen{gen}: {ganador} (R train {o['R']}, R retenidas {h['R']})"); break
        log(f"    {o['candidato']} SOBREAJUSTADO o invalido en retenidas (R={h.get('R')}, valido={h.get('valido')}): se descarta (P3)")
    res = dict(gen=gen, padre=os.path.relpath(padre, AQUI), sha_padre=h16(padre), R_padre=Rp, SEC_padre=SECp, R_padre_retenidas=Rph,
               candidatos=[{k: v for k, v in o.items() if k != 'error'} for o in tabla], ganador=ganador)
    json.dump(res, open(os.path.join(AQUI, f'gen{gen}', 'puntuaciones.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"gen{gen} terminada. ganador = {ganador}. -> gen{gen}/puntuaciones.json")
