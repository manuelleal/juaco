"""Diagnostico ESTRUCTURAL (T = 0, no simula un paso del organismo) para DISENO_mundo_grande.md (sala 2).
Construye KW exactamente como organismo_v14.py (rng: Wl uniform(.1,.4,(2,D+3)) y luego KW uniform(0,1,(NK,D)))
con la retina de D pixeles (anclas de capD) y lee code(P) = top-K de KW@P sobre las NK celdas iniciales.
Mundo de familias: F tokens (peso 3 sobre los primeros D-V pixeles) x V variables (un pixel extra cada una).
Mide, por semilla: (a) cuantas variantes comparten >= K-1 celdas con SU token (tokeniza), (b) cuantas comparten
>= K-1 con OTRO token (familia falsa), (c) alias exacto entre los 32 estimulos, (d) idem con intensidad 0.5 del pixel
variable (para decir si el techo es del codigo o de la intensidad). Sin rechazo cond() (solo restringe A y B).
Uso: python diagnostico_familias_sala2.py [D=12] [V=3] [F=8] [semillas=200]"""
import sys, itertools, json
import numpy as np
NK=30; K=3
def codigo(KW,P):
    v=KW@P; return frozenset(np.argsort(v)[-K:].tolist())
def mundo(D,V,F,r):
    shape=D-V; combos=list(itertools.combinations(range(shape),3)); r.shuffle(combos)
    toks={}; i=0
    while len(toks)<F: toks['T%d'%len(toks)]=combos[i]; i+=1
    pats={}
    for n,c in toks.items():
        P=np.zeros(D); P[list(c)]=1.; pats[n]=P
        for v in range(V):
            Q=P.copy(); Q[shape+v]=1.; pats[n+'v%d'%v]=Q
    return toks,pats
def main(D=12,V=3,F=8,S=200,inten=1.0):
    res=dict(D=D,V=V,F=F,S=S,inten=inten,tokeniza=[],falsa=[],ninguna=[],alias_tok=[],alias_any=[],exacto=[])
    for seed in range(1,S+1):
        rng=np.random.default_rng(seed); rng.uniform(.1,.4,(2,D+3)); KW=rng.uniform(0,1,(NK,D))
        rw=np.random.default_rng(50000+seed); toks,pats=mundo(D,V,F,rw)
        if inten!=1.0:
            for n in list(pats):
                if 'v' in n: pats[n]=pats[n].copy(); pats[n][D-V:]*=inten
        cod={n:codigo(KW,P) for n,P in pats.items()}
        tk=[n for n in pats if 'v' not in n]; nt=0; nf=0; nn=0; ex=0
        for n in pats:
            if 'v' in n:
                base=n.split('v')[0]; propio=len(cod[n]&cod[base])
                otros=max(len(cod[n]&cod[t]) for t in tk if t!=base)
                if propio==K: ex+=1
                if propio>=K-1 and propio>=otros: nt+=1
                elif otros>=K-1: nf+=1
                else: nn+=1
        nv=F*V
        res['tokeniza'].append(nt/nv); res['falsa'].append(nf/nv); res['ninguna'].append(nn/nv); res['exacto'].append(ex/nv)
        res['alias_tok'].append(int(any(cod[a]==cod[b] for a,b in itertools.combinations(tk,2))))
        res['alias_any'].append(int(any(cod[a]==cod[b] for a,b in itertools.combinations(list(pats),2))))
    q=lambda x:(round(float(np.median(x)),3),round(float(np.mean(x)),3))
    print(f"D={D} V={V} F={F} K={K} NK={NK} semillas={S} intensidad_variable={inten}")
    print(f"  variante comparte >=K-1 celdas con SU token (tokeniza): mediana/media {q(res['tokeniza'])}")
    print(f"  variante con codigo EXACTO = token (alias variante-token): {q(res['exacto'])}")
    print(f"  variante comparte >=K-1 con OTRO token (familia falsa):   {q(res['falsa'])}")
    print(f"  variante sin token (<=K-2 con todos):                     {q(res['ninguna'])}")
    print(f"  semillas con alias exacto entre dos TOKENS: {sum(res['alias_tok'])}/{S}; entre dos estimulos cualesquiera: {sum(res['alias_any'])}/{S}")
    return res
if __name__=='__main__':
    a=sys.argv[1:]; D=int(a[0]) if a else 12; V=int(a[1]) if len(a)>1 else 3; F=int(a[2]) if len(a)>2 else 8; S=int(a[3]) if len(a)>3 else 200
    out={}
    for inten in (1.0,0.5):
        out['inten_%s'%inten]=main(D,V,F,S,inten)
    json.dump(out,open(__file__.replace('.py','_salida.json'),'w'),indent=0)
