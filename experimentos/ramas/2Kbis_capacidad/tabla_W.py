"""W (mediana y rango) de los cuatro estimulos en cada condicion del barrido de la Parte 1."""
import json,glob,os,sys,statistics as st
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
d=os.path.dirname(os.path.abspath(__file__))
runs=[]
for pat in ('parte1_umbral_*.json','parte1b_diagnostico_*.json'):
    runs+=json.load(open(sorted(glob.glob(os.path.join(d,pat)))[-1],encoding='utf-8'))['corridas']
def f(v): return '%+.2f[%+.2f,%+.2f]'%(st.median(v),min(v),max(v))
conds=[]
for r in runs:
    if r['cond'] not in conds: conds.append(r['cond'])
print('%-22s %6s %22s %22s %22s %22s'%('condicion','frac','W_A','W_B','W_C','W_D'))
for c in conds:
    g=[r for r in runs if r['cond']==c and r['plast']]
    print('%-22s %6.2f %22s %22s %22s %22s'%(c,sum(r['splits']>0 for r in g)/len(g),
        f([r['W_A'] for r in g]),f([r['W_B'] for r in g]),f([r['W_C'] for r in g]),f([r['W_D'] for r in g])))
print('\n(A=comida +1, B=veneno -3. C y D solo tienen valor si el escenario los introduce;')
print(' si no aparecen en el mundo su W es el valor a priori por solapamiento de codigo.)')
