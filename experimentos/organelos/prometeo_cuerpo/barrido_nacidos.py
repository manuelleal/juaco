# EXPLORATORIO, no es dato
"""barrido_nacidos.py — medida DESCRIPTIVA agregada despues de ver la tabla (no es la lectura preregistrada): una parte 'barre' en una
corrida si en alguna ventana de 2000 pasos con >= 20 nacidos la lleva >= 50 % de los nacidos (capta barridos TRANSITORIOS que el banco
del corte y del final no ve). Tambien el primer t de barrido y si sigue >= 50 % en la ultima ventana."""
import glob, json, os
AQUI = os.path.dirname(os.path.abspath(__file__))
P = ('PATA', 'ESCUDO', 'ESTOMAGO', 'OJO', 'MANDIBULA', 'LENGUA')
L = []
for m in ('quieto', 'veneno', 'niebla'):
    for b in ('CUERPO', 'CUERPO_MUDO'):
        fs = sorted(glob.glob(os.path.join(AQUI, 'datos', f'{m}_largo', f'{b}_s*.json')))
        cnt = [0] * 6; det = []
        for f in fs:
            x = json.load(open(f, encoding='utf-8')); nv = x['cuerpo']['nac_ventanas']
            for j, p in enumerate(P):
                w = [v for v in nv if v[1] >= 20 and v[2 + j] is not None and v[2 + j] >= 0.5]
                if w:
                    cnt[j] += 1; det.append(f"s{x['seed']}:{p}@{w[0][0]}" + ('(sigue)' if nv[-1][2 + j] and nv[-1][2 + j] >= 0.5 else '(se pierde)'))
        L.append(f"{m:<7} {b:<12} n {len(fs)} · barre (>=0.5 de los nacidos en alguna ventana): " + ', '.join(f"{p} {c}" for p, c in zip(P, cnt)))
        L.append('      ' + ' '.join(det))
open(os.path.join(AQUI, 'datos', 'BARRIDOS_largo.txt'), 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))
