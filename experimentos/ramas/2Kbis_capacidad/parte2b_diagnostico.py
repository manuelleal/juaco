"""
PARTE 2b - diagnostico del colapso de v7 y metrica correcta de celdas por estimulo (regla 5).

Tres cosas a verificar antes de reportar nada:
 A. Las medianas de |W-R| caen en 1.00 y 2.00 EXACTOS y alternan con la paridad de n. Si todos los W valen 0,
    con R=+1 (comida) y R=-3 (veneno) la mediana da exactamente 1 con n impar (mas comida) y (1+3)/2=2 con n par.
    Hipotesis: en v7 tras el agotamiento TODOS los W colapsan a 0. Se comprueba mirando los W crudos.
 B. Si los W son 0 porque los CODIGOS Kenyon han colapsado (todos los estimulos comparten las mismas celdas),
    solap_medio -> 3.0. Se mide.
 C. `incremento por estimulo 0 [0-54]` es una mediana sobre TODOS los intervalos, y la mayoria son 0 porque
    las celdas se saturan en 90 muy pronto. La metrica correcta es celdas gastadas / estimulos que las gastaron,
    contada HASTA el agotamiento.
"""
import json,glob,os,sys,statistics as st
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
d=os.path.dirname(os.path.abspath(__file__))
D=json.load(open(sorted(glob.glob(os.path.join(d,'parte2_capacidad_*.json')))[-1],encoding='utf-8'))
res=D['corridas']
def med(v): return '%g [%g-%g]'%(st.median(v),min(v),max(v)) if v else '-'

print('=== A. W crudos en el checkpoint final ===')
for c in ('v6_20k','v7_20k','v6_60k','v7_60k'):
    g=[r for r in res if r['cond']==c]; ceros=0; tot=0; vals=[]
    for r in g:
        fin=max(r['hist'],key=lambda h:h['t'])
        for k,v in fin['W'].items():
            tot+=1; vals.append(v)
            if abs(v)<1e-9: ceros+=1
    print('  %-8s W==0 exacto: %d/%d (%.1f%%)   W min %.2f max %.2f  mediana %.2f'%(
        c,ceros,tot,100*ceros/tot,min(vals),max(vals),st.median(vals)))
print('\n  ejemplo v7_20k semilla 1, W final por estimulo:')
r=[x for x in res if x['cond']=='v7_20k' and x['seed']==1][0]
fin=max(r['hist'],key=lambda h:h['t'])
print('   ',{k:fin['W'][k] for k in list(fin['W'])[:20]})
print('  ejemplo v6_20k semilla 1, W final por estimulo:')
r6=[x for x in res if x['cond']=='v6_20k' and x['seed']==1][0]
fin6=max(r6['hist'],key=lambda h:h['t'])
print('   ',{k:fin6['W'][k] for k in list(fin6['W'])[:20]})

print('\n=== B. solapamiento medio/maximo de codigos Kenyon entre estimulos vivos ===')
print('%-4s %-20s %-20s %-20s %-20s'%('n','v6_20k medio','v7_20k medio','v6_20k max','v7_20k max'))
for n in (2,4,6,8,10,12,14,16,18,20):
    f=[]
    for c in ('v6_20k','v7_20k'):
        v=[x['solap_medio'] for r in res if r['cond']==c for x in r['hist'] if x['n']==n]; f.append(med([round(y,2) for y in v]))
    for c in ('v6_20k','v7_20k'):
        v=[x['solap_max'] for r in res if r['cond']==c for x in r['hist'] if x['n']==n]; f.append(med(v))
    print('%-4d %-20s %-20s %-20s %-20s'%(n,*f))
print('  (3.0 = todos los estimulos comparten exactamente las mismas 3 celdas: el codigo deja de distinguir)')

print('\n=== C. CELDAS POR ESTIMULO, metrica correcta (contada hasta el agotamiento) ===')
for c in ('v7_20k','v7_60k'):
    g=[r for r in res if r['cond']==c]; cpe=[]; nag=[]; inc=[]
    for r in g:
        hs=sorted(r['hist'],key=lambda h:h['t'])
        ag=[h for h in hs if h['celdas']>=90]
        h0=ag[0] if ag else hs[-1]
        n_ag=h0['n']; nag.append(n_ag)
        if n_ag>2: cpe.append(round((h0['celdas']-30)/(n_ag-2),2))
        pre=[h for h in hs if h['celdas']<90]
        for i in range(len(pre)-1): inc.append(pre[i+1]['celdas']-pre[i]['celdas'])
    print('  %-8s estimulos vivos al agotarse: %-14s  celdas gastadas por estimulo: %-16s'%(c,med(nag),med(cpe)))
    print('           incremento de celdas por estimulo ANTES del agotamiento: %s'%med(inc))

print('\n=== D. e_n de v6 vs v7 lado a lado (la plasticidad, ayuda o estorba?) ===')
print('%-4s %-16s %-16s %-10s'%('n','v6_20k','v7_20k','v7-v6'))
for n in range(2,21):
    a=[st.median(x['dev'].values()) for r in res if r['cond']=='v6_20k' for x in r['hist'] if x['n']==n]
    b=[st.median(x['dev'].values()) for r in res if r['cond']=='v7_20k' for x in r['hist'] if x['n']==n]
    if a and b: print('%-4d %-16.3f %-16.3f %+.3f %s'%(n,st.median(a),st.median(b),st.median(b)-st.median(a),
        'v7 PEOR' if st.median(b)>st.median(a)+.05 else ('v7 mejor' if st.median(b)<st.median(a)-.05 else '~')))
