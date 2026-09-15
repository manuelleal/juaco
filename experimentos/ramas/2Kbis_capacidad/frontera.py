"""Detalle de la frontera: las corridas mas cercanas a theta=0.6 y el desglose por semilla de AB1."""
import json,glob,os,sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
d=os.path.dirname(os.path.abspath(__file__))
p1=json.load(open(sorted(glob.glob(os.path.join(d,'parte1_umbral_*.json')))[-1],encoding='utf-8'))
p2=json.load(open(sorted(glob.glob(os.path.join(d,'parte1b_diagnostico_*.json')))[-1],encoding='utf-8'))
runs=p1['corridas']+p2['corridas']
T={(r['cond'],r['seed']):r for r in runs if r['plast']}
F={(r['cond'],r['seed']):r for r in runs if not r['plast']}
pares=sorted([(k[0],k[1],F[k]['err_max'],T[k]['splits']) for k in T],key=lambda x:x[2])
print('=== Frontera de theta=0.6 (err_max medido con plast=False, sin truncar) ===')
print('las 10 mas altas POR DEBAJO de 0.6 (ninguna debe dividir):')
for c,s,e,sp in [x for x in pares if x[2]<=0.6][-10:]: print('   %-22s sem %2d err_max %.4f splits %d'%(c,s,e,sp))
print('las 10 mas bajas POR ENCIMA de 0.6 (todas deben dividir):')
for c,s,e,sp in [x for x in pares if x[2]>0.6][:10]: print('   %-22s sem %2d err_max %.4f splits %d'%(c,s,e,sp))
for cond in ('AB1','REJ_AB1','D_comida_solB1_t0','D_comida_solB1'):
    print('\n%s, por semilla (err_max sin truncar -> splits):'%cond)
    print('   '+' '.join('%d:%.3f/%d'%(s,F[(cond,s)]['err_max'],T[(cond,s)]['splits']) for s in range(1,21)))
