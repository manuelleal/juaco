# EXPLORATORIO, no es dato — diagnostico: que muerde el bicho de fabrica sin vivero
import os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import motor_ecologia as M
esc = int(sys.argv[1]); T = int(sys.argv[2]); seed = int(sys.argv[3]); rep = sys.argv[4] if len(sys.argv) > 4 else 'fija'
t0 = time.time()
r = M.run_solapadas(seed, ['FABRICA_ECO'] * esc, T=T, diag=0, mundo_n=esc, tope_cuerpos=3000, muestra=500, reposicion=rep,
                    eco=dict(refunda=0, p_mut=0.0, cada_gen=0))
E = r['eco']; P = r['pista']
print(f'esc {esc} T {T} rep {rep}: seg', round(time.time() - t0, 1), 't_ext', E['t_ext'], 'vivos_T', len(E['vivos_final']), 'max', P['max_vivos'], 'n_nac', E['n_nac'])
print('tam_total', P['tam_total'][:40])
mord = {k: 0 for k in 'ABCD'}; vis = {k: 0 for k in 'ABCD'}; causas = {}
for l in r['linajes']:
    for k in 'ABCD': mord[k] += sum(l['mord'][k]); vis[k] += sum(l['vis'][k])
    for k, v in l['_carrera']['causas'].items(): causas[k] = causas.get(k, 0) + v
print('mord', mord, 'vis', vis, 'causas', causas)
ind = [row for l in r['linajes'] for row in l['individuos']]
nac = [x for x in ind if x[6] == 0]
print('nacidos', len(nac), 'R0 nacidos', (sum(x[5] for x in nac) / len(nac)) if nac else None)
vidas = [v for l in r['linajes'] for v in l['vidas_muertos']]
print('vidas media', sum(vidas)/max(1,len(vidas)), 'n', len(vidas), 'comp_mundo', P['comp_mundo'], 'nobj_medio', P['nobj_medio'], 'llegadas', P['llegadas'])
