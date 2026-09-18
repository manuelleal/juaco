"""REFUTADOR sala 2 (lente localidad), calculo ESTRUCTURAL con T = 0 (no simula un paso) para DISENO_mundo_grande.md P8:
el diseno predice que `bateria_generaliza` ON dara "filas identicas a v14.1 (identidad por construccion: 1a visita = v14.1)".
Pero la regla `_tok` (A3) dispara en la 2a visita de cualquier patron ENTRENADO cuyo codigo comparta K-1 = 2 celdas con el
codigo (distinto) de otro patron entrenado ya familiar. Aqui se cuenta, en el mundo de regla px0 de organismo/organismo_v14g.py
(solo se lee), con KW sorteada EXACTAMENTE como run() (Wl uniform(.1,.4,(2,9)) y luego KW uniform(0,1,(NK,6)); sin cond() fuera
de 'AB'), cuantos patrones de TREN tienen un companero de tren con codigo distinto y solapamiento == 2, y cuantos de esos
companeros tienen la valencia OPUESTA (la lectura por el token tendria el signo contrario al del mundo). Semillas 101-120
(las de la bateria) y 1-200. organismo/ primero en sys.path (ERR-28)."""
import sys, os, json, itertools
AQUI=os.path.dirname(os.path.abspath(__file__)); RAIZ=os.path.abspath(os.path.join(AQUI,'..','..','..'))
sys.path[:0]=[os.path.join(RAIZ,'organismo')]
import numpy as np
from organismo_v14g import split_regla, NK, K
def codigo(KW,P): v=KW@P; return frozenset(np.argsort(v)[-K:].tolist())
def semilla(seed,regla='px0'):
    rng=np.random.default_rng(seed); rng.uniform(.1,.4,(2,9)); KW=rng.uniform(0,1,(NK,6))
    pats,tren,test,vr=split_regla(seed,regla)
    cod={n:codigo(KW,pats[n]) for n in tren}
    con_tok=0; con_tok_opuesto=0; pares2=0; pares_id=0
    for a in tren:
        cands=[b for b in tren if b!=a and cod[a]!=cod[b] and len(cod[a]&cod[b])>=K-1]
        if cands:
            con_tok+=1
            if any(vr[b]!=vr[a] for b in cands): con_tok_opuesto+=1
    for a,b in itertools.combinations(tren,2):
        if cod[a]==cod[b]: pares_id+=1
        elif len(cod[a]&cod[b])==K-1: pares2+=1
    return dict(seed=seed,n_tren=len(tren),tren_con_companero_K1=con_tok,tren_con_companero_K1_valencia_opuesta=con_tok_opuesto,
                pares_tren_solap2=pares2,pares_tren_codigo_identico=pares_id)
if __name__=='__main__':
    out={}
    for etiqueta,rango in (('bateria_101-120',range(101,121)),('s1-200',range(1,201))):
        R=[semilla(s) for s in rango]
        f=lambda k:[r[k] for r in R]
        res=dict(n=len(R),n_tren=R[0]['n_tren'],
                 semillas_con_algun_tren_con_companero_K1=sum(r['tren_con_companero_K1']>0 for r in R),
                 semillas_con_companero_K1_valencia_opuesta=sum(r['tren_con_companero_K1_valencia_opuesta']>0 for r in R),
                 mediana_tren_con_companero_K1=float(np.median(f('tren_con_companero_K1'))),
                 mediana_tren_con_companero_opuesto=float(np.median(f('tren_con_companero_K1_valencia_opuesta'))),
                 mediana_pares_solap2=float(np.median(f('pares_tren_solap2'))),
                 semillas_con_par_identico=sum(r['pares_tren_codigo_identico']>0 for r in R))
        out[etiqueta]=res; out[etiqueta+'_por_semilla']=R
        print(etiqueta, {k:v for k,v in res.items()})
    json.dump(out,open(__file__.replace('.py','_salida.json'),'w'),indent=0)
