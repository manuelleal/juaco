# EXPLORATORIO, no es dato
"""corre_ecologia.py — UNA corrida del comite de ecologia (explorador B, 25-sep-2026). Sin vivero, sin mutacion, quimiostato.
Uso: python corre_ecologia.py <MEC> <seed> <esc> <T> [carpeta]
MEC en MECS (abajo). El bicho es FAMB_ORG_ECO con los organos apagados (= FABRICA_ECO, el bicho real, con hereda='nada'); ENSENA y
ENSENA_F0 prenden sus organos por kw_extra. Escribe <carpeta>/<MEC>_w<esc>_s<seed>.json.
Misión: llegar a la AGI por este camino.
"""
import json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import motor_ecologia as M

T_COLA = 10000   # la cohorte para R0: nacidos (no fundadores) hasta T - T_COLA
CARRO = 'FAMB_ORG_ECO'
MECS = {
    'SIN': dict(),
    'ENSENA': dict(kw_extra=dict(ensena=1.0)),
    'ENSENA_F0': dict(kw_extra=dict(ensena=1.0, filtra0=1.0)),
    'VIDA': dict(social=dict(vida=3)),
    'CADAVER': dict(social=dict(cadaver=1)),
    'BOLSA': dict(social=dict(bolsa=1)),
    'BOLSA_TODOS': dict(social=dict(bolsa=1, bolsa_kin='todos')),
    'NICHO': dict(social=dict(nicho='limpia')),
    'NICHO_AZAR': dict(social=dict(nicho='azar')),
    'ENSENA+CADAVER': dict(kw_extra=dict(ensena=1.0), social=dict(cadaver=1)),
    'ENSENA+CADAVER+BOLSA': dict(kw_extra=dict(ensena=1.0), social=dict(cadaver=1, bolsa=1)),
    'ENSENA_F0+CADAVER': dict(kw_extra=dict(ensena=1.0, filtra0=1.0), social=dict(cadaver=1)),
    'VIDA+ENSENA': dict(kw_extra=dict(ensena=1.0), social=dict(vida=3)),
    'ENSENA+NICHO': dict(kw_extra=dict(ensena=1.0), social=dict(nicho='limpia')),
    'ENSENA+BOLSA': dict(kw_extra=dict(ensena=1.0), social=dict(bolsa=1)),
    'ENSENA+VIDA+CADAVER': dict(kw_extra=dict(ensena=1.0), social=dict(vida=3, cadaver=1)),
    'SIN_FABRICA': dict(carro='FABRICA_ECO'),   # comprobacion: el bicho de fabrica tal cual
    # descomposicion (agregados tras ver el barrido w9: el mundo se llena de B/D y las llegadas se pierden)
    'COMPOST': dict(social=dict(compost=500)),
    'BORRA': dict(social=dict(compost=500, compost_modo='borra')),
    'ENSENA+COMPOST': dict(kw_extra=dict(ensena=1.0), social=dict(compost=500)),
    'ENSENA_F0+COMPOST': dict(kw_extra=dict(ensena=1.0, filtra0=1.0), social=dict(compost=500)),
    'ENSENA_F0+BORRA': dict(kw_extra=dict(ensena=1.0, filtra0=1.0), social=dict(compost=500, compost_modo='borra')),
    'ENSENA_F0+CADAVER+COMPOST': dict(kw_extra=dict(ensena=1.0, filtra0=1.0), social=dict(cadaver=1, compost=500)),
    'CADAVER+COMPOST': dict(social=dict(cadaver=1, compost=500)),
    # control de "regalo": el doble de flujo del quimiostato (r_rep 0.06), sin descomposicion. Si esto rescata igual que COMPOST,
    # COMPOST es solo mas comida; si no, lo que importa es que lo toxico deje de tapar el mundo.
    'FLUJO2': dict(r_rep=0.06),
    'ENSENA_F0+FLUJO2': dict(kw_extra=dict(ensena=1.0, filtra0=1.0), r_rep=0.06),
}


def corre(mec, seed, esc, T, carpeta):
    cfg = dict(MECS[mec]); carro = cfg.pop('carro', CARRO); r_rep = cfg.pop('r_rep', M.R_REP)
    eco = dict(refunda=0, p_mut=0.0, cada_gen=0); eco.update(cfg)
    t0 = time.time()
    r = M.run_solapadas(seed, [carro] * esc, T=T, diag=0, mundo_n=esc, tope_cuerpos=3000, muestra=1000, r_rep=r_rep, eco=eco)
    E = r['eco']; P = r['pista']
    ind = [row for l in r['linajes'] for row in l['individuos']]   # [k, gen, padre, t_nace, t_muere, hijos, fundador, causa, vol]
    coh = [x for x in ind if x[6] == 0 and x[3] <= T - T_COLA]
    nac = [x for x in ind if x[6] == 0]
    mord = {k: 0 for k in 'ABCD'}; vis = {k: 0 for k in 'ABCD'}; causas = {}
    for l in r['linajes']:
        for k in 'ABCD': mord[k] += sum(l['mord'][k]); vis[k] += sum(l['vis'][k])
        for k, v in l['_carrera']['causas'].items(): causas[k] = causas.get(k, 0) + v
    vidas = [v for l in r['linajes'] for v in l['vidas_muertos']]
    res = dict(mec=mec, seed=seed, esc=esc, T=T, carro=carro, r_rep=r_rep, seg=round(time.time() - t0, 1), t_ext=E['t_ext'],
               persiste=int(E['t_ext'] is None and len(E['vivos_final']) > 0), vivos_T=len(E['vivos_final']),
               linajes_vivos_T=len(set(v[0] for v in E['vivos_final'])), max_vivos=P['max_vivos'], n_nac=E['n_nac'],
               nacidos=len(nac), n_coh=len(coh), R0=(round(sum(x[5] for x in coh) / len(coh), 4) if coh else None),
               vida_media=(round(sum(vidas) / len(vidas), 1) if vidas else None), causas=causas, mord=mord, vis=vis,
               comp_mundo=P['comp_mundo'], nobj_medio=P['nobj_medio'], llegadas=P['llegadas'], llegadas_perdidas=P['llegadas_perdidas'],
               cadaveres=P['cadaveres'], cadaveres_perdidos=P['cadaveres_perdidos'], bolsas=P['bolsas'], ensenanzas_vida=P['ensenanzas_vida'],
               llegadas_nicho=P['llegadas_nicho'], compostados=P['compostados'], social=P['social'], kw_extra=cfg.get('kw_extra'), tam_total=P['tam_total'],
               gen_max=max([x[1] for x in ind] or [0]))
    os.makedirs(carpeta, exist_ok=True)
    fin = os.path.join(carpeta, f"{mec}_w{esc}_s{seed}.json")
    with open(fin + '.tmp', 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(fin + '.tmp', fin)
    return res


if __name__ == '__main__':
    mec, seed, esc, T = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    carpeta = sys.argv[5] if len(sys.argv) > 5 else os.path.join(AQUI, 'datos')
    x = corre(mec, seed, esc, T, carpeta)
    print(f"{mec} w{esc} s{seed}: {x['seg']} s · persiste {x['persiste']} (vivos {x['vivos_T']}, max {x['max_vivos']}) · t_ext {x['t_ext']} · "
          f"nacidos {x['nacidos']} · R0 {x['R0']} (coh {x['n_coh']}) · vida {x['vida_media']} · causas {x['causas']} · cad {x['cadaveres']} · bolsas {x['bolsas']} · vida_n {x['ensenanzas_vida']} · nicho {x['llegadas_nicho']}")
