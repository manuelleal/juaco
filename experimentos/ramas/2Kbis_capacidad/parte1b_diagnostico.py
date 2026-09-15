"""
PARTE 1b - Diagnostico de la REFUTACION del umbral (regla 5: la primera hipotesis es el instrumento).

El barrido (parte1_umbral.py) refuta el punto 5: con A&B=1 FORZADO dividen 8/20 semillas.
Antes de aceptarlo hay que descartar tres explicaciones de instrumento y una de diseno:

 C1. El truco de forzado. solap_AB pone KW[:N]=[5,0,0,0,0,0]: celdas detectoras del pixel 0, extremas y
     todas iguales. CONTROL: mismo solapamiento obtenido por PURO RECHAZO sobre KW aleatoria (forzar_KW=False).
     Si la fraccion que divide se mantiene, el truco no es la causa.
 C2. El momento. En AB{N} el conflicto existe desde t=0 y ambos estimulos se aprenden a la vez desde cero;
     en D_comida_solB{N} el estimulo nuevo entra en t=50.000 contra una B ya aprendida y ya evitada.
     CONTROL: D_comida_solB{N} con nuevo_en=0 (mismo par, misma valencia opuesta, aprendizaje simultaneo).
 C3. La valencia. CTRL_D_veneno_solB2 (D veneno, B veneno, solapamiento 2) dio 0/20 divisiones.
     Ya medido en parte1. Se recoge aqui para el cuadro completo.
 M.  La cantidad mecanica. Contraste err_max(plast=False) > theta=0.6  <->  splits>0, corrida a corrida.
"""
import sys,os,json,csv,glob,hashlib,datetime,statistics as st,multiprocessing as mp
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
AQUI=os.path.dirname(os.path.abspath(__file__))
RAIZ=os.path.abspath(os.path.join(AQUI,'..','..','..'))
sys.path.insert(0,AQUI); sys.path.insert(0,os.path.join(RAIZ,'organismo'))
NS=20; THETA=0.6

COND={
 # C1: mismo solapamiento, sin el truco KW=[5,0,...]
 'REJ_AB1':dict(solap_AB=1,forzar_KW=False),
 'REJ_AB2':dict(solap_AB=2,forzar_KW=False),
 'REJ_AB3':dict(solap_AB=3,forzar_KW=False),
 # C2: mismo par B(veneno)/D(comida), solapamiento 0/1/2, pero co-aprendidos desde t=0
 'D_comida_solB0_t0':dict(nuevo='D',nuevo_val='comida',solap_B=0,nuevo_en=0),
 'D_comida_solB1_t0':dict(nuevo='D',nuevo_val='comida',solap_B=1,nuevo_en=0),
 'D_comida_solB2_t0':dict(nuevo='D',nuevo_val='comida',solap_B=2,nuevo_en=0),
}
PAR={'REJ_AB1':'AB','REJ_AB2':'AB','REJ_AB3':'AB','D_comida_solB0_t0':'BD','D_comida_solB1_t0':'BD','D_comida_solB2_t0':'BD'}

def tarea(a):
    cond,s,plast=a
    import organismo_v7i as o
    r=o.run(s,plast=plast,**COND[cond])
    return dict(cond=cond,seed=s,plast=plast,solap_medido=r['solap_ini'][PAR[cond]],
        splits=r['splits'],celdas=r['celdas'],primer_split=(min(r['split_t'])[0] if r['split_t'] else None),
        estimulos_split=''.join(sorted({k for _,k in r['split_t']})),
        W_A=r['W']['A'],W_B=r['W']['B'],W_C=r['W']['C'],W_D=r['W']['D'],
        err_max=round(r['err_max'],4),err_max_k={k:round(v,4) for k,v in r['err_max_k'].items()},deaths=r['deaths'])

def med(v): return '%g [%g-%g]'%(st.median(v),min(v),max(v)) if v else '-'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]

if __name__=='__main__':
    mp.set_start_method('spawn',force=True)
    prev=sorted(glob.glob(os.path.join(AQUI,'parte1_umbral_*.json')))[-1]
    P1=json.load(open(prev,encoding='utf-8'))
    trabajos=[(c,s,p) for c in COND for s in range(1,NS+1) for p in (True,False)]
    with mp.Pool(min(14,mp.cpu_count())) as pool: res=pool.map(tarea,trabajos)
    print('=== PARTE 1b - controles de la refutacion (%d corridas nuevas) ==='%len(res))
    print('base previa:',os.path.basename(prev),'\n')
    hdr='%-20s %4s %6s %9s %14s %9s %24s %24s'%('condicion','sol','frac','n_div','1er split','celdas','err_max plast=True','err_max plast=False')
    print(hdr); print('-'*len(hdr))
    filas={}
    def linea(nombre,g,gf):
        sm='/'.join(map(str,sorted({r['solap_medido'] for r in g})))
        frac=sum(r['splits']>0 for r in g)/len(g)
        ps=[r['primer_split'] for r in g if r['primer_split'] is not None]
        print('%-20s %4s %6.2f %9s %14s %9s %24s %24s'%(nombre,sm,frac,med([r['splits'] for r in g]),
            med(ps) if ps else '-',med([r['celdas'] for r in g]),med([r['err_max'] for r in g]),med([r['err_max'] for r in gf])))
        filas[nombre]=dict(solap=sm,frac=frac,n_div=med([r['splits'] for r in g]),primer=med(ps) if ps else None,
            celdas=med([r['celdas'] for r in g]),errT=med([r['err_max'] for r in g]),errF=med([r['err_max'] for r in gf]),
            W_A=med([r['W_A'] for r in g]),W_B=med([r['W_B'] for r in g]),W_D=med([r['W_D'] for r in g]))
    # bloque previo (para comparar lado a lado)
    for c in ['AB1','AB2','AB3','D_comida_solB1','D_comida_solB2','CTRL_D_veneno_solB2']:
        g=[r for r in P1['corridas'] if r['cond']==c and r['plast']]; gf=[r for r in P1['corridas'] if r['cond']==c and not r['plast']]
        linea('(p1) '+c,g,gf)
    print('-'*len(hdr))
    for c in COND:
        linea(c,[r for r in res if r['cond']==c and r['plast']],[r for r in res if r['cond']==c and not r['plast']])

    print('\n=== M. err_max(plast=False) vs splits, corrida a corrida (theta=%.1f) ==='%THETA)
    pares=[]
    for src,lst in (('p1',P1['corridas']),('p1b',res)):
        T={(r['cond'],r['seed']):r for r in lst if r['plast']}
        F={(r['cond'],r['seed']):r for r in lst if not r['plast']}
        for k in T: pares.append((src,k[0],k[1],F[k]['err_max'],T[k]['splits']>0))
    tp=[p for p in pares if p[3]>THETA and p[4]]; fp=[p for p in pares if p[3]>THETA and not p[4]]
    fn=[p for p in pares if p[3]<=THETA and p[4]]; tn=[p for p in pares if p[3]<=THETA and not p[4]]
    print('  err_max>%.1f  y divide : %3d      err_max>%.1f  y NO divide: %3d'%(THETA,len(tp),THETA,len(fp)))
    print('  err_max<=%.1f y divide : %3d      err_max<=%.1f y NO divide: %3d'%(THETA,len(fn),THETA,len(tn)))
    print('  concordancia: %d/%d = %.4f'%(len(tp)+len(tn),len(pares),(len(tp)+len(tn))/len(pares)))
    for p in fp[:10]+fn[:10]: print('    discrepa:',p)
    d=sorted(p[3] for p in pares if p[4]); nd=sorted(p[3] for p in pares if not p[4])
    print('  err_max(plast=False) de las que DIVIDEN   : min %.4f  max %.4f  (n=%d)'%(d[0],d[-1],len(d)))
    print('  err_max(plast=False) de las que NO dividen: min %.4f  max %.4f  (n=%d)'%(nd[0],nd[-1],len(nd)))
    print('  -> separacion perfecta' if d[0]>nd[-1] else '  -> se solapan en [%.4f,%.4f]'%(d[0],nd[-1]))

    ts=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    meta=dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),python=sys.version.split()[0],
        numpy=__import__('numpy').__version__,sha_v7i=sha(os.path.join(AQUI,'organismo_v7i.py')),
        sha_este=sha(os.path.abspath(__file__)),base_previa=os.path.basename(prev),NS=NS,T=100000,theta=THETA,
        condiciones={k:str(v) for k,v in COND.items()},filas=filas,
        concordancia=dict(tp=len(tp),fp=len(fp),fn=len(fn),tn=len(tn),n=len(pares)))
    fj=os.path.join(AQUI,'parte1b_diagnostico_%s.json'%ts)
    json.dump(dict(meta=meta,corridas=res,pares=pares),open(fj,'w',encoding='utf-8'),indent=1,default=str)
    fc=os.path.join(AQUI,'parte1b_diagnostico_%s.csv'%ts)
    with open(fc,'w',newline='',encoding='utf-8') as f:
        for k,v in meta.items():
            if k not in ('filas',): f.write('# %s: %s\n'%(k,v))
        cols=[k for k in res[0] if k!='err_max_k']
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore'); w.writeheader()
        for r in sorted(res,key=lambda r:(r['cond'],not r['plast'],r['seed'])): w.writerow(r)
    print('\n->',fj,'\n->',fc)
