"""identidad_v01.py — ARNES del CODIGO v0.1. Un proceso. Semilla 29002.

MISION: llegar a la AGI por este camino.

I0  motor_fable.py y fable_mundos.py (exploracion_fable/) NO cambiaron (sha fijado); motor_v01 se construye desde motor_fable por anclas.
I1  motor_v01 == motor_fable BIT A BIT (salida entera menos las claves nuevas codigo.per_nac y codigo.banco_corte) en CODIGO_SIN_SOS/onda8k,
    PERILLAS/quieto, AZAR/onda8k y CODIGO/quieto.
I2  LA PEDIDA: PERILLAS_ROBUSTA con la mutacion en cero == PERILLAS con la mutacion en cero, BIT A BIT (salida entera).
I2b PERILLAS_ROBUSTA con lambda 1 == PERILLAS, bit a bit (ROBUSTA difiere de PERILLAS SOLO en la tasa).
I3  la telemetria nueva de PERILLAS: con mutacion 0 el fenotipo es identico en el 100 % de los partos; con la de hoy, la fraccion identica
    medida esta cerca de la analitica (f_ident_perillas); con lambda 0.5 esta entre las dos.
I4  el banco de cintas en el corte: tantas cintas como el banco en el corte, todas validas; MUT0 -> todas == CINTA0.
I5  el mundo 'quieto' (spec fijo con tabla vacia) == sin cambio, en la fisica (linajes y pista).
I6  AZAR sigue al brazo principal: sin SOS (la SOS no se prende nunca).
"""
import hashlib, json, os, sys, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
COD = os.path.dirname(AQUI); FAB = os.path.join(COD, 'exploracion_fable')
sys.path.insert(0, AQUI)
import corre_v01 as RV
import codigo_def as CD
import importlib.util
_sp = importlib.util.spec_from_file_location('motor_fable_ref', os.path.join(FAB, 'motor_fable.py'))
MF = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(MF)
MV = RV.MV

SEED = 29002; N0 = RV.MUNDO['n0']
TLI = dict(T=6000, t_cambio=1000, t_corte=4000, r0_margen=500)
OK = []


def chk(nombre, cond, extra=''):
    OK.append((nombre, bool(cond))); print(f"[{'OK ' if cond else 'MAL'}] {nombre} {extra}", flush=True)


def canon(x): return json.dumps(x, sort_keys=True, default=repr)


def corre(M, eco):
    return M.run_solapadas(SEED, [RV.CARRO] * N0, T=TLI['T'], diag=0, mundo_n=RV.MUNDO['esc'], tope_cuerpos=RV.MUNDO['tope'], muestra=100, eco=eco)


def sin_nuevas(r):
    r = json.loads(canon(r)); c = r.get('codigo')
    if c is not None: c.pop('per_nac', None); c.pop('banco_corte', None)
    return canon(r)


def main():
    t0 = time.time(); sg = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    print(f"shas {RV.SHAS()}")
    chk('I0 motor_fable y fable_mundos sin cambios (sha)', sg(os.path.join(FAB, 'motor_fable.py')) == '46750da69ef8cce1' and sg(os.path.join(FAB, 'fable_mundos.py')) == 'ccb39d6de1cd62d3')
    for b, m in (('CODIGO_SIN_SOS', 'onda8k'), ('PERILLAS', 'quieto'), ('AZAR', 'onda8k'), ('CODIGO', 'quieto')):
        a = corre(MF, RV.eco_de(b, m, TLI, lam=1.0)); v = corre(MV, RV.eco_de(b, m, TLI, lam=1.0))
        chk(f'I1 motor_v01 == motor_fable ({b}/{m})', sin_nuevas(a) == sin_nuevas(v), f"nac {a['eco']['n_nac']} refund {a['eco']['n_refund']}")
        if b == 'PERILLAS': rP = v
        if b == 'CODIGO_SIN_SOS': rC = v
        if b == 'AZAR': rA = v
    # I2 la pedida
    e_per0 = RV.eco_de('PERILLAS', 'quieto', TLI); e_per0.update(p_mut=0.0, g_pcampo=0.0, g_pdup=0.0, g_pdel=0.0)
    p0 = corre(MV, e_per0); r0 = corre(MV, RV.eco_de('PERILLAS_ROBUSTA', 'quieto', TLI, lam=0.0))
    chk('I2 PERILLAS_ROBUSTA (mutacion 0) == PERILLAS (mutacion 0), BIT A BIT', canon(p0) == canon(r0), f"nac {p0['eco']['n_nac']}")
    r1 = corre(MV, RV.eco_de('PERILLAS_ROBUSTA', 'quieto', TLI, lam=1.0))
    chk('I2b PERILLAS_ROBUSTA (lambda 1) == PERILLAS, BIT A BIT', canon(r1) == canon(rP))
    # I3
    pn0 = p0['codigo']['per_nac']; pn1 = rP['codigo']['per_nac']
    f0 = 1 - np.mean([x[4] for x in pn0]); f1 = 1 - np.mean([x[4] for x in pn1])
    rh = corre(MV, RV.eco_de('PERILLAS_ROBUSTA', 'quieto', TLI, lam=0.5)); fh = 1 - np.mean([x[4] for x in rh['codigo']['per_nac']])
    chk('I3 fenotipo identico en PERILLAS: 1.0 con mutacion 0; ~analitico con la de hoy; intermedio con lambda 0.5',
        f0 == 1.0 and len(pn0) == p0['eco']['n_nac'] and abs(f1 - RV.f_ident_perillas(1.0)) < 0.10 and f1 < fh < 1.0,
        f"mut0 {f0:.3f} (n {len(pn0)}) · hoy {f1:.3f} vs analitico {RV.f_ident_perillas(1.0):.3f} (n {len(pn1)}) · lam 0.5 {fh:.3f} vs {RV.f_ident_perillas(0.5):.3f}")
    # I4
    bc = rC['codigo']['banco_corte']; nb = rC['eco']['corte']['n_banco']
    ok4 = bc is not None and len(bc) == nb and all(CD.valida([tuple(i) for i in c]) for c in bc)
    m0 = corre(MV, RV.eco_de('MUT0', 'quieto', TLI)); bm = m0['codigo']['banco_corte']
    chk('I4 banco de cintas en el corte: una por entrada del banco, validas; MUT0 -> todas CINTA0', ok4 and all(tuple(tuple(i) for i in c) == RV.CINTA0 for c in bm),
        f"{len(bc)} cintas (n_banco {nb}); largo medio {np.mean([len(c) for c in bc]):.2f}; MUT0 identica {1 - np.mean([x[6] for x in m0['codigo']['cod_nac']]):.3f}")
    # I5 quieto == sin cambio (fisica)
    e_nc = RV.eco_de('CODIGO_SIN_SOS', 'quieto', TLI); e_nc['cambio'] = None
    q = corre(MV, RV.eco_de('CODIGO_SIN_SOS', 'quieto', TLI)); nc = corre(MV, e_nc)
    chk("I5 mundo 'quieto' == sin cambio (linajes, pista, eco)", canon([q['linajes'], q['pista'], q['eco']]) == canon([nc['linajes'], nc['pista'], nc['eco']]))
    chk('I6 AZAR sin SOS (sigue al brazo principal)', all(x[5] == 0 for x in rA['codigo']['cod_nac']) and rA['codigo']['c_sos'] is False)
    print(f"\nARNES v0.1: {sum(o for _, o in OK)}/{len(OK)} · {round(time.time() - t0, 1)} s")
    os.makedirs(os.path.join(AQUI, 'datos'), exist_ok=True)
    json.dump(dict(ok=[list(x) for x in OK], shas=RV.SHAS(), seg=round(time.time() - t0, 1)), open(os.path.join(AQUI, 'datos', 'identidad_v01.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
