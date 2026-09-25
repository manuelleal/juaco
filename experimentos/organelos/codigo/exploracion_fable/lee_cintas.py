# EXPLORATORIO, no es dato
"""lee_cintas.py — que eligio la seleccion: en los VIVOS en T de cada corrida, el organo de transmision (ORG / gramatica) y las perillas.
(Fable, 24-sep-2026). MISION: llegar a la AGI por este camino.
Uso: python lee_cintas.py <carpeta de datos/...> [mas carpetas]
"""
import glob, json, os, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gramatica_def as GD

for carpeta in sys.argv[1:]:
    print(f"\n== {os.path.basename(carpeta)}")
    for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json'))):
        x = json.load(open(p, encoding='utf-8'))
        if x.get('abortado') or not x.get('persiste'): continue
        gr = Counter(); cin_ops = Counter(); largos = []
        for v in x.get('vivos_gr') or []:
            for s in v[4]:
                gr[f"{GD.CUANDO[s[0]]}/{GD.QUE[s[1]]}/{GD.QUIEN[s[2]]}/{GD.COMO[s[3]]}"] += 1
            if not v[4]: gr['(vacio)'] += 1
        for c in x.get('cintas_vivos') or []:
            largos.append(len(c[3]))
            for ins in c[3]:
                if ins[0] in ('TASA', 'SOS', 'EJE', 'REP', 'DEF', 'LLAMA'): cin_ops[tuple(ins)] += 1
                elif ins[0] == 'SUM' and ins[2] != 0: cin_ops[('SUM', ins[1], ins[2])] += 1
        nv = x.get('vivos_T')
        print(f"  {x['brazo']:<15} s{x['seed']} vivos {nv} · organo: {dict(gr.most_common(6))}")
        if cin_ops: print(f"      cinta (largo {min(largos)}-{max(largos)}): {dict(cin_ops.most_common(10))}")
        if x.get('mundo_fable', {}).get('estado'): print(f"      reina cambios: {x['mundo_fable']['estado'].get('cambios')}")
