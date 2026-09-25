# EXPLORATORIO, no es dato — humo de velocidad: FABRICA_ECO sin vivero, w9, T 3000
import os, sys, time, json
AQUI = os.path.dirname(os.path.abspath(__file__))
ECO = r"C:\Users\User\Documents\PROYECTOS\JUACO\organelos\experimentos\juaco_eco"
GEN = r"C:\Users\User\Documents\PROYECTOS\JUACO\bundle\experimentos\generaciones"
for d in (AQUI, ECO, GEN):
    if d not in sys.path: sys.path.insert(0, d)
import motor_ecologia as M
esc = int(sys.argv[1]); T = int(sys.argv[2]); seed = int(sys.argv[3])
t0 = time.time()
r = M.run_solapadas(seed, ['FABRICA_ECO'] * esc, T=T, diag=0, mundo_n=esc, tope_cuerpos=3000, muestra=500,
                    eco=dict(refunda=0, p_mut=0.0, cada_gen=0))
E = r['eco']; P = r['pista']
print('seg', round(time.time() - t0, 1), 't_ext', E['t_ext'], 'vivos_T', len(E['vivos_final']), 'max', P['max_vivos'], 'n_nac', E['n_nac'])
print('tam_total', P['tam_total'])
ind = [row for l in r['linajes'] for row in l['individuos']]
nac = [x for x in ind if x[6] == 0]
print('nacidos', len(nac), 'hijos medios nacidos', (sum(x[5] for x in nac) / len(nac)) if nac else None)
print('vidas muertos (media)', sum(sum(l['vidas_muertos']) for l in r['linajes']) / max(1, sum(len(l['vidas_muertos']) for l in r['linajes'])))
print('causas', [l['_carrera']['causas'] for l in r['linajes']][:3])
