"""
PARTE 2 - 2K-bis redefinida: capacidad en numero de estimulos.
Preregistro: PREREGISTRO.md (escrito ANTES de correr). Modulo: organismo_cap.py (equivalencia probada
contra organismo_v6.py y organismo_v7.py, 306/306 campos).

Conjunto: los 20 patrones binarios de 6 pixeles con peso 3 (familia completa C(6,3)).
Orden: A,B,C,D (los canonicos del proyecto) y despues los 16 restantes en orden lexicografico.
Valencias ALTERNANDO desde el primero: comida, veneno, comida, veneno, ...
Cada estimulo n>=3 entra en t=(n-2)*paso_t. Checkpoint n en t=(n-1)*paso_t, justo antes de que entre el n+1:
todos los estimulos se miden exactamente paso_t pasos despues de la entrada del ultimo.
"""
import sys,os,json,csv,itertools,hashlib,datetime,statistics as st,multiprocessing as mp
import numpy as np
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
AQUI=os.path.dirname(os.path.abspath(__file__))
RAIZ=os.path.abspath(os.path.join(AQUI,'..','..','..'))
sys.path.insert(0,AQUI); sys.path.insert(0,os.path.join(RAIZ,'organismo'))
NS=20; N_EST=20; TOL=0.3; MIN_MORD=30

CANON=[('A',(0,1,3)),('B',(0,2,4)),('C',(1,2,5)),('D',(2,4,5))]
_usados={c for _,c in CANON}
_resto=[c for c in itertools.combinations(range(6),3) if c not in _usados]
NOMBRES=[n for n,_ in CANON]+['E%02d'%(i+5) for i in range(len(_resto))]
COMBOS=[c for _,c in CANON]+_resto
PATS={n:np.array([1. if i in c else 0. for i in range(6)]) for n,c in zip(NOMBRES,COMBOS)}
VAL={n:('comida' if i%2==0 else 'veneno') for i,n in enumerate(NOMBRES)}
R={n:(1.0 if VAL[n]=='comida' else -3.0) for n in NOMBRES}

def plan_de(paso_t,n_est=N_EST):
    p=[(0,NOMBRES[0],VAL[NOMBRES[0]]),(0,NOMBRES[1],VAL[NOMBRES[1]])]
    for i in range(2,n_est): p.append(((i-1)*paso_t,NOMBRES[i],VAL[NOMBRES[i]]))
    return p
def chks(paso_t,n_est=N_EST): return [(n-1)*paso_t for n in range(2,n_est+1)]
def T_de(paso_t,n_est=N_EST): return (n_est-1)*paso_t+paso_t

COND={'v6_20k':(False,20000),'v7_20k':(True,20000),'v6_60k':(False,60000),'v7_60k':(True,60000)}

def tarea(a):
    cond,s=a
    import organismo_cap as oc
    plast,pt=COND[cond]
    r=oc.run(s,T=T_de(pt),plan=plan_de(pt),pats=PATS,chk=chks(pt),plast=plast)
    for h in r['hist']:
        h['dev']={k:round(abs(v-R[k]),3) for k,v in h['W'].items()}
    return dict(cond=cond,seed=s,plast=plast,paso_t=pt,T=T_de(pt),hist=r['hist'],
                celdas=r['celdas'],splits=r['splits'],t_agot=r['t_agot'],deaths=r['deaths'],
                err_max=round(r['err_max'],4),split_t=r['split_t'],t_entra=r['t_entra'])

def med(v): return (st.median(v),min(v),max(v)) if v else (None,None,None)
def fmt(v): return '%g [%g-%g]'%med(v) if v else '-'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]

def techo(hist,excl_nuevo=False):
    """mayor n tal que e_m<=TOL para todo m<=n, con e_m = mediana de |W-R| sobre los vivos."""
    N=1
    for h in sorted(hist,key=lambda h:h['t']):
        d=dict(h['dev'])
        if excl_nuevo and len(d)>2:
            ult=max(h['W'],key=lambda k:NOMBRES.index(k)); d.pop(ult,None)
        if not d: continue
        if st.median(d.values())<=TOL: N=h['n']
        else: break
    return N

if __name__=='__main__':
    mp.set_start_method('spawn',force=True)
    print('=== PARTE 2 - capacidad en numero de estimulos (2K-bis redefinida) ===')
    print('estimulos (orden, patron, valencia):')
    for i,n in enumerate(NOMBRES):
        print('  %2d %-4s %s %s'%(i+1,n,''.join(str(int(x)) for x in PATS[n]),VAL[n]),end='\n' if i%2 else '   ')
    print('\nsolapamiento de pixel dentro de la familia peso-3: cada patron tiene 1 vecino a 0, 9 a 1, 9 a 2.')
    trabajos=[(c,s) for c in COND for s in range(1,NS+1)]
    t0=datetime.datetime.now()
    with mp.Pool(min(14,mp.cpu_count())) as pool: res=pool.map(tarea,trabajos)
    print('\ncorridas: %d  tiempo: %s\n'%(len(res),datetime.datetime.now()-t0))

    resumen={}
    for c in COND:
        g=[r for r in res if r['cond']==c]
        N=[techo(r['hist']) for r in g]; Nx=[techo(r['hist'],True) for r in g]
        ce=[r['celdas'] for r in g]; sp=[r['splits'] for r in g]
        agot=[r for r in g if r['t_agot'] is not None]
        resumen[c]=dict(techo=med(N),techo_sin_ultimo=med(Nx),techos=N,celdas=med(ce),splits=med(sp),
                        n_agotan=len(agot),err_max=med([r['err_max'] for r in g]))
        print('%-8s techo N* %-14s (excl. ultimo %-14s) celdas_fin %-13s splits %-12s agotan 90: %d/%d'%(
            c,fmt(N),fmt(Nx),fmt(ce),fmt(sp),len(agot),len(g)))

    print('\n=== e_n = mediana de |W-R| sobre los estimulos vivos, por numero de estimulos ===')
    print('%-4s %-22s %-22s %-22s %-22s'%('n','v6_20k','v7_20k','v6_60k','v7_60k'))
    curva={c:{} for c in COND}
    for n in range(2,N_EST+1):
        fila=[]
        for c in COND:
            v=[]
            for r in res:
                if r['cond']!=c: continue
                h=[x for x in r['hist'] if x['n']==n]
                if h: v.append(st.median(h[0]['dev'].values()))
            curva[c][n]=med(v); fila.append('%5.2f [%.2f-%.2f]'%med(v) if v else '-')
        print('%-4d %-22s %-22s %-22s %-22s'%(n,*fila))

    print('\n=== celdas activas por numero de estimulos (v7) ===')
    print('%-4s %-22s %-22s   %-10s %-10s'%('n','v7_20k celdas','v7_60k celdas','d_celdas20k','d_celdas60k'))
    cel={c:{} for c in ('v7_20k','v7_60k')}
    for n in range(2,N_EST+1):
        f=[]
        for c in ('v7_20k','v7_60k'):
            v=[x['celdas'] for r in res if r['cond']==c for x in r['hist'] if x['n']==n]
            cel[c][n]=med(v); f.append('%5.1f [%d-%d]'%med(v) if v else '-')
        d=[('%+.1f'%(cel[c][n][0]-cel[c][n-1][0]) if n>2 and cel[c].get(n-1) else '-') for c in ('v7_20k','v7_60k')]
        print('%-4d %-22s %-22s   %-10s %-10s'%(n,f[0],f[1],d[0],d[1]))

    print('\n=== CELDAS POR ESTIMULO (metrica central) ===')
    cpe={}
    for c in ('v7_20k','v7_60k'):
        g=[r for r in res if r['cond']==c]; pend=[]; inc=[]
        for r in g:
            hs=sorted(r['hist'],key=lambda h:h['t']); xs=[h['n'] for h in hs]; ys=[h['celdas'] for h in hs]
            pend.append(round(float(np.polyfit(xs,ys,1)[0]),3))
            inc+= [ys[i+1]-ys[i] for i in range(len(ys)-1)]
        tot=[(r['celdas']-30)/(N_EST-2) for r in g]
        cpe[c]=dict(pendiente=med(pend),incremento=med(inc),total_medio=med([round(x,3) for x in tot]))
        print('%-8s pendiente MC %-16s  incremento por estimulo %-14s  (celdas_fin-30)/18 %-16s'%(
            c,fmt(pend),fmt(inc),fmt([round(x,3) for x in tot])))

    print('\n=== AGOTAMIENTO DE LAS 90 CELDAS ===')
    agot={}
    for c in ('v7_20k','v7_60k'):
        g=[r for r in res if r['cond']==c]; a=[r for r in g if r['t_agot'] is not None]
        print('%-8s agotan: %d/%d'%(c,len(a),len(g)))
        if not a: continue
        na=[]; ant=[]; des=[]; ant_antes=[]
        for r in a:
            te=r['t_entra']; ta=r['t_agot']; fin=max(r['hist'],key=lambda h:h['t'])
            pre=[h for h in r['hist'] if h['t']<=ta]; pre=max(pre,key=lambda h:h['t']) if pre else None
            A=[k for k in fin['dev'] if te[k]<ta]; D=[k for k in fin['dev'] if te[k]>=ta]
            na.append(len(A))
            if A: ant.append(st.median([fin['dev'][k] for k in A]))
            if D: des.append(st.median([fin['dev'][k] for k in D]))
            if A and pre: ant_antes.append(st.median([pre['dev'][k] for k in A if k in pre['dev']]))
        print('   t_agot %-20s  estimulos vivos al agotarse %-12s'%(fmt([r['t_agot'] for r in a]),fmt(na)))
        print('   |W-R| al final, estimulos ANTERIORES al agotamiento : %s'%fmt([round(x,3) for x in ant]))
        print('   |W-R| de esos mismos ANTES del agotamiento          : %s'%fmt([round(x,3) for x in ant_antes]))
        print('   |W-R| al final, estimulos POSTERIORES               : %s'%fmt([round(x,3) for x in des]))
        print('   -> %s'%('DEGRADACION SUAVE (los antiguos aguantan <=%.1f)'%TOL if ant and st.median(ant)<=TOL
                          else 'COLAPSO (los antiguos se degradan por encima de %.1f)'%TOL))
        agot[c]=dict(n=len(a),t_agot=med([r['t_agot'] for r in a]),n_vivos=med(na),
                     ant_fin=med([round(x,3) for x in ant]),ant_pre=med([round(x,3) for x in ant_antes]),
                     post_fin=med([round(x,3) for x in des]))

    print('\n=== CONTROL 6.2 muestreo (paso_t 20000 vs 60000) ===')
    for v in ('v6','v7'):
        a=resumen[v+'_20k']['techo'][0]; b=resumen[v+'_60k']['techo'][0]
        print('  %s: techo %g -> %g  (delta %+g)  %s'%(v,a,b,b-a,
              'ANULA el resultado (delta>=2): es muestreo, no capacidad' if b-a>=2 else 'el techo no se mueve: limite representacional'))
    print('\n=== CONTROL 6.3 disponibilidad (estimulos con <%d mordidas acumuladas en su checkpoint) ==='%MIN_MORD)
    for c in COND:
        pobres=[]; tot=0
        for r in res:
            if r['cond']!=c: continue
            for h in r['hist']:
                for k,m in h['mord_ac'].items():
                    tot+=1
                    if m<MIN_MORD: pobres.append((r['seed'],h['n'],k,m))
        print('  %-8s %d/%d pares (estimulo x checkpoint) con <%d mordidas = %.1f%%'%(c,len(pobres),tot,MIN_MORD,100*len(pobres)/tot))
    print('\n=== CRITERIOS DEL PREREGISTRO ===')
    n6=resumen['v6_20k']['techos']; n7=resumen['v7_20k']['techos']
    mejor=sum(b>a for a,b in zip(n6,n7))
    print('  P1 techo v6 <= 6 en >=15/20 : %d/20  -> %s'%(sum(x<=6 for x in n6),'CUMPLE' if sum(x<=6 for x in n6)>=15 else 'FALLA'))
    print('  P2 v7>v6 en >=15/20 semillas: %d/20  -> %s'%(mejor,'CUMPLE' if mejor>=15 else 'H2 REFUTADA'))
    print('     medianas: v6 %g  v7 %g  (P2 pide v7 >= v6+2: %s)'%(st.median(n6),st.median(n7),
          'CUMPLE' if st.median(n7)>=st.median(n6)+2 else 'FALLA'))
    cp=cpe['v7_20k']['incremento'][0]
    print('  P3 celdas/estimulo en [1,4]  : %g -> %s'%(cp,'CUMPLE' if 1<=cp<=4 else 'P3 REFUTADA'))
    print('  P4 degradacion suave         : ver bloque AGOTAMIENTO')

    ts=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    meta=dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),python=sys.version.split()[0],
        numpy=np.__version__,sha_cap=sha(os.path.join(AQUI,'organismo_cap.py')),sha_este=sha(os.path.abspath(__file__)),
        sha_v6=sha(os.path.join(RAIZ,'organismo','organismo_v6.py')),sha_v7=sha(os.path.join(RAIZ,'organismo','organismo_v7.py')),
        NS=NS,N_EST=N_EST,TOL=TOL,condiciones={k:str(v) for k,v in COND.items()},
        estimulos={n:dict(patron=''.join(str(int(x)) for x in PATS[n]),valencia=VAL[n],R=R[n]) for n in NOMBRES},
        resumen=resumen,curva_e_n={c:{str(k):v for k,v in d.items()} for c,d in curva.items()},
        celdas_n={c:{str(k):v for k,v in d.items()} for c,d in cel.items()},celdas_por_estimulo=cpe,agotamiento=agot)
    fj=os.path.join(AQUI,'parte2_capacidad_%s.json'%ts)
    json.dump(dict(meta=meta,corridas=res),open(fj,'w',encoding='utf-8'),indent=1,default=str)
    fc=os.path.join(AQUI,'parte2_capacidad_%s.csv'%ts)
    with open(fc,'w',newline='',encoding='utf-8') as f:
        for k,v in meta.items():
            if k in ('fecha','python','numpy','sha_cap','sha_este','sha_v6','sha_v7','NS','N_EST','TOL','condiciones','estimulos'):
                f.write('# %s: %s\n'%(k,json.dumps(v,default=str) if isinstance(v,dict) else v))
        w=csv.writer(f); w.writerow(['cond','seed','paso_t','n','t','celdas','splits','solap_medio','solap_max',
                                     'e_n_mediana','estimulo','W','R','dev','vis_ac','mord_ac'])
        for r in sorted(res,key=lambda r:(r['cond'],r['seed'])):
            for h in sorted(r['hist'],key=lambda h:h['t']):
                e=round(st.median(h['dev'].values()),3)
                for k in h['W']:
                    w.writerow([r['cond'],r['seed'],r['paso_t'],h['n'],h['t'],h['celdas'],h['splits'],
                                h['solap_medio'],h['solap_max'],e,k,h['W'][k],h['R'][k],h['dev'][k],
                                h['vis_ac'][k],h['mord_ac'][k]])
    print('\n->',fj,'\n->',fc)
