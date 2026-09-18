"""Refutador sala 2 (medibilidad) -- LA UNICA corrida permitida: UN proceso, T = 50 000, semilla 1.
Pregunta: en el mundo del TRONCO (V0 del DISENO_vivir: costo=0.002, nobj=4, comida/veneno) ¿se abre alguna vez la ventana
rep_X=500 pasos seguidos con E >= 1.0 que el diseno usa como unico disparador del nacimiento? Y ¿cae dentro de la PRIMERA vida
(la del fundador, E=1.0), que es la unica que existe con muerte real?
Instrumento: organismo_vivo_rep2.run(vivo=0, n_nec=1) == organismo_v14 bit a bit (arnes B 3/3 del runner del bloque 2); la medida
rep es de solo lectura (rep_coste=0). organismo/ primero en sys.path (ERR-28). Sin Pool."""
import sys, os, json, time
R=r"C:\Users\User\Documents\PROYECTOS\JUACO\bundle"
sys.path.insert(0, os.path.join(R,'organismo')); sys.path.insert(1, os.path.join(R,'experimentos','nivel11_mundo_vivo'))
import organismo_vivo_rep2 as M
t0=time.time()
r=M.run(1, T=50000, vivo=0, n_nec=1, costo=0.002, nobj=4, reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0, rep_coste=0.0, rep2=1, rep2_regalo=300)
dt=time.time()-t0
vidas=r['vidas']; td=r['t_desc']
fin=[]; acc=0
for v in vidas: acc+=v; fin.append(acc)
primera=vidas[0] if vidas else r['vida_final']
ventanas_en_primera=sum(1 for t in td if t<primera)
# ventanas por vida
por_vida=[]; ini=0
for f in fin:
    por_vida.append(sum(1 for t in td if ini<=t<f)); ini=f
por_vida.append(sum(1 for t in td if t>=ini))
out=dict(seed=1,T=50000,segundos=round(dt,2),deaths=r['deaths'],descendientes=r['descendientes'],pasos_viables=r['pasos_viables'],
         desc_regalo=r['desc_regalo'],t_desc=td,vida_primera=primera,vida_mediana=(sorted(vidas)[len(vidas)//2] if vidas else None),
         vida_max=(max(vidas) if vidas else None),vida_final=r['vida_final'],n_vidas=len(vidas)+1,ventanas_en_primera_vida=ventanas_en_primera,
         vidas_con_ventana=sum(1 for x in por_vida if x>0),vidas_ge_2000=sum(1 for v in vidas if v>=2000),W=r['W'],celdas=r['celdas'],splits=r['splits'])
print(json.dumps(out,indent=1))
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'refuta_vivir_calib_v0_s1.json'),'w'),indent=1)
