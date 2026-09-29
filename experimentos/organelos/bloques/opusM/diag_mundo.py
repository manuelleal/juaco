"""diag_mundo.py — diagnostico (Opus M): composicion del mundo (comp_mundo, llegadas perdidas) con y sin el instinto 'no morder B/D'.
Un proceso, 2 corridas, T 60 000, semilla 48494. Pregunta: el instinto deja el anillo lleno de veneno y sal (tope de objetos)?"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQUI)
import corre_bloques as CB
NS = CB.NS
T = 60000
out = {}
for nom, brazo, extra in (('ING_F1', 'ING_F1', {}), ('BLOQ_forzada', 'BLOQ', dict(p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0,
                                                                                    forzada=[[3, 4, 1, 0.5, 0, -3.0]]))):
    MB = CB.usa_bloques(); MB.BQ_CFG.clear(); MB.BQ_CFG.update(CB.DEF); MB.BQ_CFG.update(CB.BQ[brazo]); MB.BQ_CFG.update(extra)
    gen, carro, _ = NS.BRAZOS[brazo]
    r = NS.CR.ME.run_solapadas(48494, NS.carros_de(carro), T=T, diag=0, mundo_n=NS.MUNDO['esc'], tope_cuerpos=NS.MUNDO['tope'],
                               muestra=NS.MUNDO['muestra'], eco=NS.eco_de(gen, T))
    P = r['pista']
    out[nom] = dict(comp_mundo=P['comp_mundo'], nobj_medio=P['nobj_medio'], nobj=P['nobj'], llegadas=P['llegadas'],
                    perdidas=P['llegadas_perdidas'], olvidos=P['olvidos'], K2=sum(P['tam_total'][len(P['tam_total']) // 2:]) / (len(P['tam_total']) - len(P['tam_total']) // 2))
    print(nom, out[nom], flush=True)
json.dump(out, open(os.path.join(AQUI, 'datos', 'diag_mundo_s48494_T60000.json'), 'w'), indent=1)
