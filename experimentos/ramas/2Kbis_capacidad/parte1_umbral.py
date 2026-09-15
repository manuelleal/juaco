"""
PARTE 1 - Barrido forzado de solapamiento. Ataca la prediccion del umbral de disparo de 2L.
Preregistrado en registro/REGISTRO_etapas_1_2.md, "Criterio de congelacion de v7, VERSION 2", punto 5:

  "en un barrido forzado de solapamiento 0,1,2,3 (2K-bis), la fraccion de semillas que divide debe ser
   0 en 0 y 1, y 1 en 2 y 3. Si alguna semilla divide con solapamiento 1, o alguna no divide con
   solapamiento 2, el umbral no esta en 2 y la afirmacion se retira."

Condiciones (20 semillas, T=100000, organismo_v7i.py == organismo_v7.py + instrumentacion inerte):
  D_comida_solB{0,1,2} : run(s,nuevo='D',nuevo_val='comida',solap_B=N)   -- D&A forzado a 0 por la condicion de sorteo
  AB{0,1,2,3}          : run(s,solap_AB=N)                                -- solapamiento A&B forzado
  E2I_C_libre          : run(s,nuevo='C')                                 -- solapamientos por sorteo, se MIDEN
  CTRL D_veneno_solB{1,2}: misma valencia que B. Control de valencia, no forma parte del criterio.

Cada condicion se corre DOS veces: plast=True (natural) y plast=False (la division no trunca el error,
de modo que err_max mide el maximo que ALCANZARIA la media movil del |error| sin plasticidad).
"""
import sys,os,json,csv,hashlib,datetime,statistics as st,multiprocessing as mp
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
AQUI=os.path.dirname(os.path.abspath(__file__))
RAIZ=os.path.abspath(os.path.join(AQUI,'..','..','..'))
sys.path.insert(0,AQUI); sys.path.insert(0,os.path.join(RAIZ,'organismo'))
NS=20

# nombre -> (kwargs, par de estimulos cuyo solapamiento manda, valencia opuesta?)
COND={
 'D_comida_solB0': (dict(nuevo='D',nuevo_val='comida',solap_B=0),'BD',0),
 'D_comida_solB1': (dict(nuevo='D',nuevo_val='comida',solap_B=1),'BD',1),
 'D_comida_solB2': (dict(nuevo='D',nuevo_val='comida',solap_B=2),'BD',2),
 'AB0'           : (dict(),                                      'AB',0),
 'AB1'           : (dict(solap_AB=1),                            'AB',1),
 'AB2'           : (dict(solap_AB=2),                            'AB',2),
 'AB3'           : (dict(solap_AB=3),                            'AB',3),
 'E2I_C_libre'   : (dict(nuevo='C'),                             'AC',None),
 'CTRL_D_veneno_solB1':(dict(nuevo='D',nuevo_val='veneno',solap_B=1),'BD',1),
 'CTRL_D_veneno_solB2':(dict(nuevo='D',nuevo_val='veneno',solap_B=2),'BD',2),
}

def tarea(a):
    cond,s,plast=a
    import organismo_v7i as o
    kw,par,nom=COND[cond]
    r=o.run(s,plast=plast,**kw)
    si=r['solap_ini']
    prim=min(r['split_t'])[0] if r['split_t'] else None
    est=sorted({k for _,k in r['split_t']})
    return dict(cond=cond,seed=s,plast=plast,kwargs={k:str(v) for k,v in kw.items()},
        solap_nominal=nom,solap_par=par,solap_medido=si[par],
        solap_AB=si['AB'],solap_AC=si['AC'],solap_AD=si['AD'],solap_BC=si['BC'],solap_BD=si['BD'],solap_CD=si['CD'],
        splits=r['splits'],celdas=r['celdas'],primer_split=prim,estimulos_split=''.join(est),
        W_A=r['W']['A'],W_B=r['W']['B'],W_C=r['W']['C'],W_D=r['W']['D'],
        err_max=round(r['err_max'],4),
        err_max_A=round(r['err_max_k']['A'],4),err_max_B=round(r['err_max_k']['B'],4),
        err_max_C=round(r['err_max_k']['C'],4),err_max_D=round(r['err_max_k']['D'],4),
        deaths=r['deaths'],split_t=r['split_t'],solap_fin=r['solap_fin'])

def med(v): return (round(st.median(v),3),min(v),max(v)) if v else (None,None,None)
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]

if __name__=='__main__':
    mp.set_start_method('spawn',force=True)
    trabajos=[(c,s,p) for c in COND for s in range(1,NS+1) for p in (True,False)]
    t0=datetime.datetime.now()
    with mp.Pool(min(14,mp.cpu_count())) as pool: res=pool.map(tarea,trabajos)
    print('=== PARTE 1 - barrido forzado de solapamiento, %d semillas, T=100000 ==='%NS)
    print('corridas: %d  tiempo: %s\n'%(len(res),datetime.datetime.now()-t0))
    PL=[r for r in res if r['plast']]
    hdr='%-21s %4s %6s %8s %14s %8s %8s %9s %8s %8s'%('condicion','sol','frac','n_div','1er split','celdas','estim','W_A','W_B','W_nuevo')
    print(hdr); print('-'*len(hdr))
    resumen={}
    for c in COND:
        g=[r for r in PL if r['cond']==c]
        sm=sorted({r['solap_medido'] for r in g}); sm='/'.join(map(str,sm))
        frac=sum(r['splits']>0 for r in g)/len(g)
        sp=[r['splits'] for r in g]; ps=[r['primer_split'] for r in g if r['primer_split'] is not None]
        ce=[r['celdas'] for r in g]; es=sorted({r['estimulos_split'] for r in g if r['estimulos_split']})
        wn='D' if 'D' in c else ('C' if 'C' in c else 'B')
        print('%-21s %4s %6.2f %8s %14s %8s %8s %8.2f %8.2f %8.2f'%(c,sm,frac,
            '%g[%g-%g]'%med(sp),('%g[%g-%g]'%med(ps)) if ps else '-','%g[%g-%g]'%med(ce),','.join(es) or '-',
            st.median([r['W_A'] for r in g]),st.median([r['W_B'] for r in g]),st.median([r['W_'+wn] for r in g])))
        resumen[c]=dict(solap=sm,frac_divide=frac,n_div=med(sp),primer_split=med(ps) if ps else None,celdas=med(ce),
            estimulos=es,W_A=med([r['W_A'] for r in g]),W_B=med([r['W_B'] for r in g]),
            W_C=med([r['W_C'] for r in g]),W_D=med([r['W_D'] for r in g]),
            err_max_plastT=med([r['err_max'] for r in g]),
            err_max_plastF=med([r['err_max'] for r in res if r['cond']==c and not r['plast']]))
    print('\n=== err_max (maximo historico de la media movil |error| por celda; theta=0.6) ===')
    print('%-21s %5s %26s %26s'%('condicion','sol','plast=True (truncado)','plast=False (sin truncar)'))
    for c in COND:
        a=resumen[c]; print('%-21s %5s %26s %26s'%(c,a['solap'],'%g [%g-%g]'%a['err_max_plastT'],'%g [%g-%g]'%a['err_max_plastF']))
    # E2I: cruce solapamiento real x splits
    print('\n=== E2I run(s,nuevo="C") : solapamiento REAL por semilla x splits ===')
    g=sorted([r for r in PL if r['cond']=='E2I_C_libre'],key=lambda r:r['seed'])
    print('semilla: '+' '.join('%3d'%r['seed'] for r in g))
    print('C&A    : '+' '.join('%3d'%r['solap_AC'] for r in g))
    print('C&B    : '+' '.join('%3d'%r['solap_BC'] for r in g))
    print('splits : '+' '.join('%3d'%r['splits'] for r in g))
    for n in (0,1,2,3):
        h=[r for r in g if r['solap_AC']==n]
        if h: print('  C&A=%d -> %2d semillas, dividen %d, err_max plastT %s / plastF %s'%(n,len(h),
              sum(r['splits']>0 for r in h),'%g[%g-%g]'%med([r['err_max'] for r in h]),
              '%g[%g-%g]'%med([r['err_max'] for r in res if r['cond']=='E2I_C_libre' and not r['plast'] and r['solap_AC']==n])))
    # VEREDICTO
    print('\n=== VEREDICTO DEL CRITERIO PREREGISTRADO (punto 5) ===')
    f0=[c for c in COND if not c.startswith('CTRL') and resumen[c]['solap'] in ('0',)]
    viol=[]
    for r in PL:
        if r['cond'].startswith('CTRL'): continue
        n=r['solap_medido']
        if n<=1 and r['splits']>0: viol.append(('divide con solap %d'%n,r['cond'],r['seed'],r['splits']))
        if n>=2 and r['splits']==0: viol.append(('NO divide con solap %d'%n,r['cond'],r['seed'],r['splits']))
    if viol:
        print('REFUTADO. %d violaciones:'%len(viol))
        for v in viol: print('   ',v)
    else: print('SOSTENIDA: 0 violaciones en %d corridas del barrido.'%len([r for r in PL if not r['cond'].startswith('CTRL')]))
    # salida
    ts=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    meta=dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),python=sys.version.split()[0],
        numpy=__import__('numpy').__version__,sha_v7=sha(os.path.join(RAIZ,'organismo','organismo_v7.py')),
        sha_v7i=sha(os.path.join(AQUI,'organismo_v7i.py')),sha_este=sha(os.path.abspath(__file__)),
        NS=NS,T=100000,condiciones={k:(str(v[0]),v[1],v[2]) for k,v in COND.items()},resumen=resumen,violaciones=viol)
    fj=os.path.join(AQUI,'parte1_umbral_%s.json'%ts)
    json.dump(dict(meta=meta,corridas=res),open(fj,'w',encoding='utf-8'),indent=1,default=str)
    fc=os.path.join(AQUI,'parte1_umbral_%s.csv'%ts)
    with open(fc,'w',newline='',encoding='utf-8') as f:
        for k,v in meta.items():
            if k not in ('resumen','violaciones','condiciones'): f.write('# %s: %s\n'%(k,v))
        f.write('# condiciones: %s\n'%json.dumps({k:(str(v[0]),v[1],v[2]) for k,v in COND.items()}))
        cols=[k for k in res[0] if k not in ('split_t','solap_fin','kwargs')]
        w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore'); w.writeheader()
        for r in sorted(res,key=lambda r:(r['cond'],not r['plast'],r['seed'])): w.writerow(r)
    print('\n->',fj,'\n->',fc)
