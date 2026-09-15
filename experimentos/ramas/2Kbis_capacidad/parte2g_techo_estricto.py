"""
PARTE 2g - metrica companera del techo. NO sustituye a la preregistrada, la acompana.

El preregistro define el techo con la MEDIANA de |W-R| (regla 6). La semilla 2 de v6_60k destapa el limite
de esa definicion: da N*=20 con la mediana <=0.3 mientras cuatro estimulos estan a |W-R| de 2.2 a 3.1.
La mediana puede estar bien con la mitad de los estimulos catastroficamente mal.

Metrica companera: fraccion de estimulos vivos con |W-R|<=0.3, y techo estricto = mayor n con esa fraccion
>= 0.9. Se reportan LAS DOS. La preregistrada no se toca (regla 3).
"""
import json,glob,os,sys,statistics as st
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
d=os.path.dirname(os.path.abspath(__file__))
TOL=0.3
D=json.load(open(sorted(glob.glob(os.path.join(d,'parte2_capacidad_*.json')))[-1],encoding='utf-8'))
res=D['corridas']
def med(v): return '%g [%g-%g]'%(st.median(v),min(v),max(v)) if v else '-'
def techo_med(h_):
    N=1
    for h in sorted(h_,key=lambda h:h['t']):
        if st.median(h['dev'].values())<=TOL: N=h['n']
        else: break
    return N
def techo_est(h_,frac=0.9):
    N=1
    for h in sorted(h_,key=lambda h:h['t']):
        ok=sum(1 for v in h['dev'].values() if v<=TOL)/len(h['dev'])
        if ok>=frac: N=h['n']
        else: break
    return N
print('=== Techo preregistrado (mediana<=%.1f) vs techo estricto (>=90%% de los estimulos dentro de %.1f) ==='%(TOL,TOL))
print('%-9s %-22s %-22s'%('cond','techo preregistrado','techo estricto'))
for c in ('v6_20k','v7_20k','v6_60k','v7_60k'):
    g=[r for r in res if r['cond']==c]
    print('%-9s %-22s %-22s'%(c,med([techo_med(r['hist']) for r in g]),med([techo_est(r['hist']) for r in g])))
print('\n=== fraccion de estimulos vivos dentro de %.1f, por n (mediana sobre semillas) ==='%TOL)
print('%-4s %-10s %-10s %-10s %-10s'%('n','v6_20k','v7_20k','v6_60k','v7_60k'))
for n in range(2,21):
    f=[]
    for c in ('v6_20k','v7_20k','v6_60k','v7_60k'):
        v=[sum(1 for x in h['dev'].values() if x<=TOL)/len(h['dev'])
           for r in res if r['cond']==c for h in r['hist'] if h['n']==n]
        f.append('%.2f'%st.median(v) if v else '-')
    print('%-4d %-10s %-10s %-10s %-10s'%(n,*f))
print('\n=== numero absoluto de estimulos bien aprendidos (|W-R|<=%.1f), mediana ==='%TOL)
print('%-4s %-10s %-10s %-10s %-10s'%('n','v6_20k','v7_20k','v6_60k','v7_60k'))
pico={}
for n in range(2,21):
    f=[]
    for c in ('v6_20k','v7_20k','v6_60k','v7_60k'):
        v=[sum(1 for x in h['dev'].values() if x<=TOL) for r in res if r['cond']==c for h in r['hist'] if h['n']==n]
        m=st.median(v) if v else None; f.append('%g'%m if m is not None else '-')
        if m is not None: pico.setdefault(c,[]).append((m,n))
    print('%-4d %-10s %-10s %-10s %-10s'%(n,*f))
print('\n=== MAXIMO de estimulos simultaneamente bien aprendidos (la cifra de capacidad util) ===')
for c,v in pico.items():
    m=max(v); print('  %-9s %g estimulos, alcanzado con n=%d en el mundo'%(c,m[0],m[1]))
