"""
Prueba de equivalencia: organismo_v7i.py (instrumentado) vs organismo/organismo_v7.py (3db0475ef0ea95ce).
6 semillas x 6 escenarios. Compara TODOS los campos comunes del dict de salida, exactamente.
Si un solo campo difiere en una sola corrida, la instrumentacion NO es inerte y hay que parar.
"""
import sys,os,json,hashlib,datetime,multiprocessing as mp
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
AQUI=os.path.dirname(os.path.abspath(__file__))
RAIZ=os.path.abspath(os.path.join(AQUI,'..','..','..'))
sys.path.insert(0,AQUI); sys.path.insert(0,os.path.join(RAIZ,'organismo'))

ESCENARIOS={
 'E1'          : dict(),
 'E2_inversion': dict(invertir_en=50000),
 'E2I_C'       : dict(nuevo='C'),
 'E2K_DsolB2'  : dict(nuevo='D',solap_B=2),
 'E2L_AB3'     : dict(solap_AB=3),
 'sin_plast'   : dict(solap_AB=3,plast=False),
}
COMUNES=['split_t','mord','vis','W','comp','deaths','log','splits','celdas','solap']

def tarea(a):
    esc,s=a
    import organismo_v7 as ov7, organismo_v7i as ovi
    r7=ov7.run(s,**ESCENARIOS[esc]); ri=ovi.run(s,**ESCENARIOS[esc])
    dif=[]
    for c in COMUNES:
        x=r7.get(c); y=ri.get(c)
        if json.dumps(x,sort_keys=True,default=str)!=json.dumps(y,sort_keys=True,default=str): dif.append(c)
    return dict(esc=esc,seed=s,dif=dif,err_max=ri['err_max'],splits=ri['splits'],celdas=ri['celdas'])

def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]

if __name__=='__main__':
    mp.set_start_method('spawn',force=True)
    trabajos=[(e,s) for e in ESCENARIOS for s in range(1,7)]
    with mp.Pool(min(12,mp.cpu_count())) as pool: res=pool.map(tarea,trabajos)
    ncmp=len(res)*len(COMUNES); nmal=sum(len(r['dif']) for r in res)
    print('=== EQUIVALENCIA organismo_v7i vs organismo_v7 ===')
    print('corridas comparadas :',len(res),' escenarios:',len(ESCENARIOS),' semillas: 1..6')
    print('campos comparados   :',ncmp,'(',len(COMUNES),'campos x',len(res),'corridas )')
    print('campos discrepantes :',nmal)
    for r in res:
        if r['dif']: print('  DIFIERE',r['esc'],'semilla',r['seed'],r['dif'])
    print('VEREDICTO:','INERTE - %d/%d campos identicos'%(ncmp-nmal,ncmp) if nmal==0 else 'NO INERTE')
    print()
    print('err_max por escenario (semillas 1..6):')
    for e in ESCENARIOS:
        v=[round(r['err_max'],4) for r in res if r['esc']==e]; sp=[r['splits'] for r in res if r['esc']==e]
        print('  %-13s err_max=%s splits=%s'%(e,v,sp))
    meta=dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),python=sys.version.split()[0],
              numpy=__import__('numpy').__version__,
              sha_v7=sha(os.path.join(RAIZ,'organismo','organismo_v7.py')),
              sha_v7i=sha(os.path.join(AQUI,'organismo_v7i.py')),
              sha_este=sha(os.path.abspath(__file__)),
              escenarios=ESCENARIOS,campos=COMUNES,ncmp=ncmp,ndif=nmal,resultados=res)
    fn=os.path.join(AQUI,'equivalencia_v7i_%s.json'%datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    json.dump(meta,open(fn,'w',encoding='utf-8'),indent=1,default=str); print('->',fn)
