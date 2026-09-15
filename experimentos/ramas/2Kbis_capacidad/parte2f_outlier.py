"""
PARTE 2f - la semilla anomala: en v6_60k una semilla da techo N*=20 (mantiene los 20 estimulos dentro de 0.3).
Regla 5: antes de creerlo, comprobar el instrumento. Si el organismo apenas muerde, |W-R| pequeno puede ser
un artefacto de disponibilidad, no aprendizaje.
"""
import json,glob,os,sys,statistics as st
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
d=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(sorted(glob.glob(os.path.join(d,'parte2_capacidad_*.json')))[-1],encoding='utf-8'))
res=D['corridas']
sys.path.insert(0,d)
def techo(hist):
    N=1
    for h in sorted(hist,key=lambda h:h['t']):
        if st.median(h['dev'].values())<=0.3: N=h['n']
        else: break
    return N
for c in ('v6_60k','v6_20k'):
    g=[(techo(r['hist']),r['seed'],r) for r in res if r['cond']==c]
    g.sort(key=lambda x:-x[0])
    print('=== %s : techos por semilla (mayor a menor) ==='%c)
    print('  '+' '.join('s%d:%d'%(s,t) for t,s,_ in g))
    t,s,r=g[0]
    fin=max(r['hist'],key=lambda h:h['t'])
    print('  semilla con techo maximo: %d (N*=%d)  muertes=%d'%(s,t,r['deaths']))
    print('  %-5s %-8s %-6s %-8s %-8s %-8s'%('est','W','R','|W-R|','mord','vis'))
    for k in fin['W']:
        print('  %-5s %-8.3f %-6g %-8.3f %-8d %-8d'%(k,fin['W'][k],fin['R'][k],fin['dev'][k],fin['mord_ac'][k],fin['vis_ac'][k]))
    print('  mordidas totales %d, visitas totales %d'%(sum(fin['mord_ac'].values()),sum(fin['vis_ac'].values())))
    print()
