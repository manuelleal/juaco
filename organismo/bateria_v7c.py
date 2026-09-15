"""Batería de regresión v6: corre las etapas con sus criterios preregistrados. python3 bateria.py [semillas]"""
import sys, numpy as np, organismo_v7c as o
S=int(sys.argv[1]) if len(sys.argv)>1 else 6; seeds=range(1,S+1)
tasa=lambda r,k,i:100*r['mord'][k][i]/max(r['vis'][k][i],1)
def etapa(nombre,fn,crit):
    res=[fn(s) for s in seeds]; ok=[all(c(r) for c in crit.values()) for r in res]
    det=" ".join(f"{n}:{sum(c(r) for r in res)}/{S}" for n,c in crit.items())
    print(f"{'PASA' if all(ok) else 'FALLA':5s} {nombre:38s} {sum(ok)}/{S}  [{det}]"); return res
print(f"=== Batería v7 CANDIDATO (v6 + 2L), {S} semillas ===")
etapa("E1 aprendizaje A/B", lambda s:o.run(s),
  {"venenoQ4<Q1":lambda r:r['mord']['B'][3]<r['mord']['B'][0], "W_A≈+1":lambda r:abs(r['W']['A']-1)<.15, "W_B≈-3":lambda r:abs(r['W']['B']+3)<.3})
ctrl=[o.run(s,learn=False) for s in seeds]
print(f"      (control sin aprendizaje: muertes medianas {np.median([r['deaths'] for r in ctrl]):.0f})")
etapa("E2 inversión A<->B (valor y extinción)", lambda s:o.run(s,invertir_en=50000),
  {"W_A→-3":lambda r:abs(r['W']['A']+3)<.3, "W_B→+1":lambda r:abs(r['W']['B']-1)<.15, "come B Q4≥50":lambda r:r['mord']['B'][3]>=50})
etapa("E2I nuevo C veneno sin olvido", lambda s:o.run(s,nuevo='C'),
  {"W_C≤-2.5":lambda r:r['W']['C']<=-2.5, "W_A≈+1":lambda r:abs(r['W']['A']-1)<.15, "W_B≤-2.8":lambda r:r['W']['B']<=-2.8, "tasaA Q4≥80%Q2":lambda r:tasa(r,'A',3)>=.8*tasa(r,'A',1)})
etapa("E2J nuevo D comida, D∩B=1", lambda s:o.run(s,nuevo='D',nuevo_val='comida',solap_B=1),
  {"W_D≥0.85":lambda r:r['W']['D']>=.85, "W_B≤-2.7":lambda r:r['W']['B']<=-2.7})
etapa("E2K nuevo D comida, D∩B=2", lambda s:o.run(s,nuevo='D',nuevo_val='comida',solap_B=2),
  {"W_D≥0.8":lambda r:r['W']['D']>=.8, "W_B≤-2.4":lambda r:r['W']['B']<=-2.4})
etapa("E2L rescate A∩B=3 (códigos idénticos)", lambda s:o.run(s,solap_AB=3),
  {"W_A≈+1":lambda r:abs(r['W']['A']-1)<.15, "W_B≈-3":lambda r:abs(r['W']['B']+3)<.3, "solap→0":lambda r:r['solap']['AB']==0})
etapa("E2L control A∩B=3 SIN plasticidad", lambda s:o.run(s,solap_AB=3,plast=False),
  {"W_A≈+1":lambda r:abs(r['W']['A']-1)<.15, "W_B≈-3":lambda r:abs(r['W']['B']+3)<.3})
print("\nPendiente conocido: política bajo hambre (mordidas de veneno ~1-4% por visita en inanición). No es criterio de esta batería.")
