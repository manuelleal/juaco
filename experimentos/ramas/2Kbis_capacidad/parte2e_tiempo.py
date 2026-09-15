"""
PARTE 2e - TERCER punto de tiempo (paso_t=180000), exigido por el propio preregistro.

El control 6.2 anulo el techo de v6 medido con paso_t=20000: subio +3 al pasar a 60000, y el preregistro
dice que en ese caso el numero no es un techo. Pero 60000 tampoco esta validado: si el techo sigue subiendo,
tampoco lo es. Se anade un tercer punto con el MISMO criterio preregistrado (delta>=2 => sigue siendo muestreo).
No se cambia ningun criterio: se aplica el que ya estaba escrito a un punto mas.
"""
import sys,os,json,datetime,hashlib,statistics as st,multiprocessing as mp
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
AQUI=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,AQUI)
import parte2_capacidad as P
PT=180000; NS=20
def tarea(a):
    plast,s=a
    import organismo_cap as oc
    r=oc.run(s,T=P.T_de(PT),plan=P.plan_de(PT),pats=P.PATS,chk=P.chks(PT),plast=plast)
    for h in r['hist']: h['dev']={k:round(abs(v-P.R[k]),3) for k,v in h['W'].items()}
    return dict(cond=('v7_180k' if plast else 'v6_180k'),seed=s,hist=r['hist'],celdas=r['celdas'],
                splits=r['splits'],t_agot=r['t_agot'],deaths=r['deaths'],comp=r['comp'],W=r['W'])
def med(v): return '%g [%g-%g]'%(st.median(v),min(v),max(v)) if v else '-'
if __name__=='__main__':
    mp.set_start_method('spawn',force=True)
    t0=datetime.datetime.now()
    with mp.Pool(min(14,mp.cpu_count())) as pool: res=pool.map(tarea,[(p,s) for p in (False,True) for s in range(1,NS+1)])
    print('=== PARTE 2e - tercer punto de tiempo, paso_t=%d, T=%d, %d semillas ==='%(PT,P.T_de(PT),NS))
    print('tiempo: %s\n'%(datetime.datetime.now()-t0))
    techos={}
    for c in ('v6_180k','v7_180k'):
        g=[r for r in res if r['cond']==c]; N=[P.techo(r['hist']) for r in g]; techos[c]=N
        print('%-9s techo N* %-16s celdas_fin %-13s splits %-12s agotan 90: %d/%d  muertes %s'%(
            c,med(N),med([r['celdas'] for r in g]),med([r['splits'] for r in g]),
            sum(r['t_agot'] is not None for r in g),len(g),med([r['deaths'] for r in g])))
    print('\n=== CONTROL 6.2 aplicado a los tres puntos (criterio preregistrado: delta>=2 = muestreo) ===')
    prev=json.load(open(sorted(__import__('glob').glob(os.path.join(AQUI,'parte2_capacidad_*.json')))[-1],encoding='utf-8'))
    R0=prev['meta']['resumen']
    for v in ('v6','v7'):
        a=R0[v+'_20k']['techo'][0]; b=R0[v+'_60k']['techo'][0]; c=st.median(techos[v+'_180k'])
        print('  %s: 20k=%g  60k=%g  180k=%g   delta(60k->180k)=%+g  -> %s'%(v,a,b,c,c-b,
            'SIGUE SUBIENDO: el techo NO esta establecido, es muestreo' if c-b>=2 else 'ESTABILIZADO: limite representacional/de valor'))
    print('\n=== saturacion de los dos canales (W==0 exacto) en el punto de 180k ===')
    for c in ('v6_180k','v7_180k'):
        g=[r for r in res if r['cond']==c]; tot=0; cero=0; sat=0
        for r in g:
            for k,(p,n) in r['comp'].items():
                tot+=1
                if abs(r['W'][k])<1e-9: cero+=1
                if p>=8.99 and n>=8.99: sat+=1
        print('  %-9s W==0: %d/%d (%.0f%%)   ambos canales en el tope: %d/%d (%.0f%%)'%(c,cero,tot,100*cero/tot,sat,tot,100*sat/tot))
    print('\n=== e_n por numero de estimulos (180k) ===')
    print('%-4s %-20s %-20s'%('n','v6_180k','v7_180k'))
    for n in range(2,21):
        f=[]
        for c in ('v6_180k','v7_180k'):
            v=[st.median(x['dev'].values()) for r in res if r['cond']==c for x in r['hist'] if x['n']==n]
            f.append('%5.2f [%.2f-%.2f]'%(st.median(v),min(v),max(v)) if v else '-')
        print('%-4d %-20s %-20s'%(n,*f))
    ts=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    fn=os.path.join(AQUI,'parte2e_tiempo_%s.json'%ts)
    json.dump(dict(meta=dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),python=sys.version.split()[0],
        numpy=__import__('numpy').__version__,paso_t=PT,T=P.T_de(PT),NS=NS,
        sha_cap=hashlib.sha256(open(os.path.join(AQUI,'organismo_cap.py'),'rb').read()).hexdigest()[:16],
        sha_este=hashlib.sha256(open(os.path.abspath(__file__),'rb').read()).hexdigest()[:16],techos=techos),
        corridas=res),open(fn,'w',encoding='utf-8'),indent=1,default=str)
    print('\n->',fn)
