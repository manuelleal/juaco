"""
PARTE 2c - por que W==0 en el 82% de los estimulos de v7 si los codigos estan MAS separados que en v6.
Regla 5: antes de llamar a esto 'colapso', hay que saber que cantidad es la que vale cero.
Se cruzan W finales con mordidas acumuladas y visitas acumuladas.
"""
import json,glob,os,sys,statistics as st
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
d=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(sorted(glob.glob(os.path.join(d,'parte2_capacidad_*.json')))[-1],encoding='utf-8'))
res=D['corridas']
def med(v): return '%g [%g-%g]'%(st.median(v),min(v),max(v)) if v else '-'

print('=== W final vs mordidas acumuladas ===')
for c in ('v6_20k','v7_20k'):
    cero_m=[]; nocero_m=[]; cero_v=[]; nocero_v=[]
    for r in res:
        if r['cond']!=c: continue
        fin=max(r['hist'],key=lambda h:h['t'])
        for k,v in fin['W'].items():
            (cero_m if abs(v)<1e-9 else nocero_m).append(fin['mord_ac'][k])
            (cero_v if abs(v)<1e-9 else nocero_v).append(fin['vis_ac'][k])
    print('  %-8s W==0  : n=%-4d mordidas %-18s visitas %s'%(c,len(cero_m),med(cero_m),med(cero_v)))
    print('  %-8s W!=0  : n=%-4d mordidas %-18s visitas %s'%(c,len(nocero_m),med(nocero_m),med(nocero_v)))

print('\n=== tasa de mordida (mordidas/visitas) al final, por version ===')
for c in ('v6_20k','v7_20k'):
    t=[]
    for r in res:
        if r['cond']!=c: continue
        fin=max(r['hist'],key=lambda h:h['t'])
        for k in fin['W']:
            if fin['vis_ac'][k]>0: t.append(round(100*fin['mord_ac'][k]/fin['vis_ac'][k],1))
    print('  %-8s %%mordida por visita: %s'%(c,med(t)))

print('\n=== visitas totales por corrida (suma sobre estimulos) ===')
for c in ('v6_20k','v7_20k','v6_60k','v7_60k'):
    tv=[];tm=[];dm=[]
    for r in res:
        if r['cond']!=c: continue
        fin=max(r['hist'],key=lambda h:h['t'])
        tv.append(sum(fin['vis_ac'].values())); tm.append(sum(fin['mord_ac'].values())); dm.append(r['deaths'])
    print('  %-8s visitas %-22s mordidas %-22s muertes %s'%(c,med(tv),med(tm),med(dm)))

print('\n=== detalle v7_20k semilla 1: W, mordidas, visitas por estimulo ===')
r=[x for x in res if x['cond']=='v7_20k' and x['seed']==1][0]
fin=max(r['hist'],key=lambda h:h['t'])
print('%-5s %-8s %-6s %-8s %-8s'%('est','W','R','mord','vis'))
for k in fin['W']: print('%-5s %-8.3f %-6g %-8d %-8d'%(k,fin['W'][k],fin['R'][k],fin['mord_ac'][k],fin['vis_ac'][k]))
print('\nsplits totales: %d  celdas: %d  t_agot: %s  muertes: %d'%(r['splits'],r['celdas'],r['t_agot'],r['deaths']))

print('\n=== los mismos numeros para v6_20k semilla 1 ===')
r=[x for x in res if x['cond']=='v6_20k' and x['seed']==1][0]
fin=max(r['hist'],key=lambda h:h['t'])
print('%-5s %-8s %-6s %-8s %-8s'%('est','W','R','mord','vis'))
for k in fin['W']: print('%-5s %-8.3f %-6g %-8d %-8d'%(k,fin['W'][k],fin['R'][k],fin['mord_ac'][k],fin['vis_ac'][k]))
print('muertes: %d'%r['deaths'])
