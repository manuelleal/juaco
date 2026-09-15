"""
PARTE 2d - la causa real de W==0: saturacion simultanea de los DOS canales en el tope del clip.

Wp y Wn se acumulan por separado y ambos estan recortados a [0,3]:
    if dlt>0: Wp=clip(Wp+...,0,3)   else: Wn=clip(Wn+...,0,3)
Una celda que recibe premio Y castigo muchas veces satura los dos canales a 3.0, y entonces
Wp-Wn = 0 EXACTO. No es 'sin aprender': es 'aprendido todo y cancelado'.
Se comprueba leyendo comp=(Wp.kc, Wn.kc) por estimulo al final de la corrida.
"""
import sys,os,json,datetime,hashlib,statistics as st,multiprocessing as mp
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
AQUI=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,AQUI)
import parte2_capacidad as P

def tarea(a):
    cond,s=a
    import organismo_cap as oc
    plast,pt=P.COND[cond]
    r=oc.run(s,T=P.T_de(pt),plan=P.plan_de(pt),pats=P.PATS,chk=[],plast=plast)
    return dict(cond=cond,seed=s,comp=r['comp'],W=r['W'],celdas=r['celdas'],splits=r['splits'],deaths=r['deaths'])

if __name__=='__main__':
    mp.set_start_method('spawn',force=True)
    trab=[(c,s) for c in ('v6_20k','v7_20k') for s in range(1,11)]
    with mp.Pool(min(14,mp.cpu_count())) as pool: res=pool.map(tarea,trab)
    print('=== comp = (Wp.kc , Wn.kc) al final. Tope del clip: 3.0 por celda, K=3 -> 9.0 por estimulo ===')
    for c in ('v6_20k','v7_20k'):
        g=[r for r in res if r['cond']==c]
        cero=[];nz=[];wp=[];wn=[];satp=0;satn=0;sat2=0;tot=0
        for r in g:
            for k,(p,n) in r['comp'].items():
                tot+=1; wp.append(p); wn.append(n)
                if p>=8.99: satp+=1
                if n>=8.99: satn+=1
                if p>=8.99 and n>=8.99: sat2+=1
                (cero if abs(r['W'][k])<1e-9 else nz).append((p,n))
        print('\n  %s  (%d estimulos x %d semillas)'%(c,20,len(g)))
        print('    Wp.kc mediana %.2f  max %.2f   |  Wn.kc mediana %.2f  max %.2f'%(st.median(wp),max(wp),st.median(wn),max(wn)))
        print('    saturados en el tope (>=8.99): Wp %d/%d (%.0f%%)   Wn %d/%d (%.0f%%)   LOS DOS %d/%d (%.0f%%)'%(
            satp,tot,100*satp/tot,satn,tot,100*satn/tot,sat2,tot,100*sat2/tot))
        if cero:
            print('    de los que tienen W==0 exacto (n=%d): Wp mediana %.2f, Wn mediana %.2f, ambos saturados %d (%.0f%%)'%(
                len(cero),st.median([x[0] for x in cero]),st.median([x[1] for x in cero]),
                sum(1 for x in cero if x[0]>=8.99 and x[1]>=8.99),100*sum(1 for x in cero if x[0]>=8.99 and x[1]>=8.99)/len(cero)))
    print('\n=== ejemplo v7_20k semilla 1: (Wp.kc, Wn.kc) por estimulo ===')
    r=[x for x in res if x['cond']=='v7_20k' and x['seed']==1][0]
    for k in P.NOMBRES: print('  %-5s R=%+g  Wp=%6.3f  Wn=%6.3f  W=%+6.3f'%(k,P.R[k],r['comp'][k][0],r['comp'][k][1],r['W'][k]))
    print('\n=== ejemplo v6_20k semilla 1 ===')
    r=[x for x in res if x['cond']=='v6_20k' and x['seed']==1][0]
    for k in P.NOMBRES: print('  %-5s R=%+g  Wp=%6.3f  Wn=%6.3f  W=%+6.3f'%(k,P.R[k],r['comp'][k][0],r['comp'][k][1],r['W'][k]))
    fn=os.path.join(AQUI,'parte2d_saturacion_%s.json'%datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    json.dump(dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),
        sha_este=hashlib.sha256(open(os.path.abspath(__file__),'rb').read()).hexdigest()[:16],
        sha_cap=hashlib.sha256(open(os.path.join(AQUI,'organismo_cap.py'),'rb').read()).hexdigest()[:16],
        corridas=res),open(fn,'w',encoding='utf-8'),indent=1,default=str)
    print('\n->',fn)
