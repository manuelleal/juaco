"""Calibracion de instrumento PREVIA al preregistro de 3T.
NO mide aprendizaje: solo geometria de codigos Kenyon en la inicializacion.
Pregunta: con NIN=12 y KW~U(0,1), que tan raro es que los 4 codigos de situacion
(A|A, A|B, B|A, B|B) sean disjuntos dos a dos? Determina si el muestreo por
rechazo del arm C2 es viable.
"""
import sys, numpy as np
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
NK=30; K=3
PAT={'A':np.array([1,1,0,1,0,0.]),'B':np.array([1,0,1,0,1,0.])}
SIT=[('A','A'),('A','B'),('B','A'),('B','B')]

def vec(cur,prev): return np.concatenate([PAT[cur],PAT[prev]])

def prueba(n=20000,seed=0):
    rng=np.random.default_rng(seed)
    ok_todos=0; ok_AA_AB=0; hist={}
    for _ in range(n):
        KW=rng.uniform(0,1,(NK,12))
        cods=[set(np.argsort(KW@vec(c,p))[-K:]) for c,p in SIT]
        pares=[(i,j) for i in range(4) for j in range(i+1,4)]
        solaps=[len(cods[i]&cods[j]) for i,j in pares]
        if max(solaps)==0: ok_todos+=1
        if len(cods[0]&cods[1])==0: ok_AA_AB+=1
        hist[solaps[0]]=hist.get(solaps[0],0)+1
    print(f"NIN=12  n={n}")
    print(f"  4 codigos disjuntos dos a dos : {ok_todos/n:.4f}")
    print(f"  solo code(A|A) n code(A|B)==0 : {ok_AA_AB/n:.4f}")
    print(f"  histograma de |code(A|A) n code(A|B)|: {dict(sorted(hist.items()))}")

def prueba6(n=20000,seed=0):
    rng=np.random.default_rng(seed)
    ok=0
    for _ in range(n):
        KW=rng.uniform(0,1,(NK,6))
        ca=set(np.argsort(KW@PAT['A'])[-K:]); cb=set(np.argsort(KW@PAT['B'])[-K:])
        if len(ca&cb)==0: ok+=1
    print(f"NIN=6 (regla de v6)  code(A) n code(B)==0: {ok/n:.4f}")

if __name__=='__main__':
    prueba6(); prueba()
