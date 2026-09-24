import sys, os, time, resource
sys.path.insert(0, '/home/user/juaco/experimentos/juaco_eco')
import corre_eco_v12 as V
V.usa_gemelo()
S = sys.argv[1]
T, tc, tl = V.V12['T'], V.V12['t_corte'], V.V12['T_lect']
print('reanudo VIDA_T s19701 desde el checkpoint', flush=True); t0 = time.time()
x = V.trabajo((19701, 'VIDA_T', T, tc, tl, S, len(V.JUEZ3['semillas']), V.JUEZ3['T_b'], True))
print('TERMINO', round(time.time() - t0, 1), 's', 'max_vivos', x.get('max_vivos'), 'maxrss MB', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss // 1024, flush=True)
