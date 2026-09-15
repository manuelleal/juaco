"""
Prueba de equivalencia de organismo_cap.py (Parte 2):
  plast=False  debe reproducir organismo/organismo_v6.py (5f38f83cf49248a3)
  plast=True   debe reproducir organismo/organismo_v7.py (3db0475ef0ea95ce)
con el PAT canonico de 4 patrones y planes equivalentes a los escenarios de v6/v7.
6 semillas x 3 escenarios x 2 versiones. Todos los campos comunes, exactos.
"""
import sys,os,json,hashlib,datetime,multiprocessing as mp
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
AQUI=os.path.dirname(os.path.abspath(__file__))
RAIZ=os.path.abspath(os.path.join(AQUI,'..','..','..'))
sys.path.insert(0,AQUI); sys.path.insert(0,os.path.join(RAIZ,'organismo'))

PLAN0=[(0,'A','comida'),(0,'B','veneno')]
ESC={
 'E1'          :(dict(),                                       dict(plan=PLAN0)),
 'C_veneno_50k':(dict(nuevo='C'),                              dict(plan=PLAN0+[(50000,'C','veneno')])),
 'D_comida_50k':(dict(nuevo='D',nuevo_val='comida'),           dict(plan=PLAN0+[(50000,'D','comida')])),
}
C6=['mord','vis','W','comp','deaths','log','solap']
C7=C6+['split_t','splits','celdas']

def tarea(a):
    esc,s,ver=a
    import organismo_v6 as o6, organismo_v7 as o7, organismo_cap as oc
    kw_ref,kw_cap=ESC[esc]
    if ver=='v6': ref=o6.run(s,**kw_ref); cols=C6; cap=oc.run(s,plast=False,**kw_cap)
    else:         ref=o7.run(s,**kw_ref); cols=C7; cap=oc.run(s,plast=True,**kw_cap)
    dif=[c for c in cols if json.dumps(ref.get(c),sort_keys=True,default=str)!=json.dumps(cap.get(c),sort_keys=True,default=str)]
    return dict(esc=esc,seed=s,ver=ver,ncol=len(cols),dif=dif)

def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]

if __name__=='__main__':
    mp.set_start_method('spawn',force=True)
    trabajos=[(e,s,v) for e in ESC for s in range(1,7) for v in ('v6','v7')]
    with mp.Pool(min(12,mp.cpu_count())) as pool: res=pool.map(tarea,trabajos)
    n=sum(r['ncol'] for r in res); bad=sum(len(r['dif']) for r in res)
    print('=== EQUIVALENCIA organismo_cap vs organismo_v6 / organismo_v7 ===')
    print('corridas: %d (3 escenarios x 6 semillas x 2 versiones)'%len(res))
    print('campos comparados: %d   discrepantes: %d'%(n,bad))
    for r in res:
        if r['dif']: print('  DIFIERE',r['esc'],r['ver'],'semilla',r['seed'],r['dif'])
    print('VEREDICTO:','EQUIVALENTE - %d/%d campos identicos'%(n-bad,n) if bad==0 else 'NO EQUIVALENTE')
    meta=dict(fecha=datetime.datetime.now().isoformat(timespec='seconds'),python=sys.version.split()[0],
        numpy=__import__('numpy').__version__,sha_v6=sha(os.path.join(RAIZ,'organismo','organismo_v6.py')),
        sha_v7=sha(os.path.join(RAIZ,'organismo','organismo_v7.py')),sha_cap=sha(os.path.join(AQUI,'organismo_cap.py')),
        sha_este=sha(os.path.abspath(__file__)),escenarios={k:(str(v[0]),str(v[1])) for k,v in ESC.items()},
        ncampos=n,ndif=bad,resultados=res)
    fn=os.path.join(AQUI,'equivalencia_cap_%s.json'%datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    json.dump(meta,open(fn,'w',encoding='utf-8'),indent=1,default=str); print('->',fn)
