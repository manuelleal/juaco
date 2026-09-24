"""identidad_eco_frank.py — ARNES Python de ECO v3 (los órganos del Frankenstein como genes): motor_eco3 + carros/FRANK_ECO.
Un proceso. Nube, 24-sep-2026.

MISION: llegar a la AGI por este camino.

  (K) construye_eco_frank.py --verifica: lo que está en disco es lo construido desde los orígenes (sha fijado).
  (G) GENES de motor_eco3 = los 18 de motor_eco + las 7 perillas del Frankenstein; G0 de los órganos 0.9 (apagados).
  (0) eco=None: FRANK_ECO (órganos apagados por defecto) == FABRICA_ECO en toda la física (motor_eco, 9 carros, T 4000, dos semillas).
  (1) eco MUT0 con los órganos en G0 (apagados): motor_eco3 + FRANK_ECO == motor_eco + FABRICA_ECO en la física (esc 30, T 5000).
  (2) eco MUT0 con los 7 órganos en 1.2: == motor_eco + el Frankenstein TODO del PC en la física.
  (3) eco MUT0 con sólo 'herencia' en 1.2: == el Frankenstein con sólo herencia; y distinto de (1).
  (4) VIDA con mutación: en cada cuerpo, cada perilla == (su gen >= 1.0); la mutación prende órganos.
  (5) checkpoint a mitad + reanuda == corrida entera (VIDA, motor_eco3 + FRANK_ECO).
Escribe identidad_eco_frank_salida.txt.
"""
import contextlib, io, json, os, sys, time, types
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones'), os.path.join(RAIZ, 'experimentos', 'frankenstein')]
R_ = []


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def fis(r):
    return (json.dumps([{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']], sort_keys=True, default=str),
            json.dumps({k: v for k, v in r['pista'].items() if k != 'pizarra_final'}, sort_keys=True, default=str))


def main():
    import motor_eco as ME
    import motor_eco3 as ME3
    import construye_eco_frank as CF3
    import organismo_frankenstein as OF
    t0 = time.time()
    print(f"IDENTIDAD ECO v3 (Frankenstein) · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · motor_eco3 "
          f"{CF3.CE.h16(CF3.DEST_MOTOR)} · FRANK_ECO {CF3.CE.h16(CF3.DEST_CARRO)} · organismo_frankenstein {CF3.CE.h16(OF.__file__)} · "
          f"construye {CF3.CE.h16(os.path.join(AQUI, 'construye_eco_frank.py'))}")
    chk("(K) motor_eco3 y FRANK_ECO en disco == construidos", all(open(p, encoding='utf-8').read() == s for p, s in CF3.textos().items()))
    G0 = ME3.genoma0(__import__('pista2').cfg_fabrica())
    chk("(G) genes = 18 de motor_eco + las 7 perillas del Frankenstein; G0 0.9", ME3.NOMBRES == ME.NOMBRES + tuple(OF.PERILLAS) and
        all(abs(x - 0.9) < 1e-12 for x in G0[18:]), f"({len(ME3.NOMBRES)} genes)")

    def modulo(nombre, per):
        m = types.ModuleType(nombre); m.crea = lambda ctx, _p=per: OF.Carro(ctx, _p); sys.modules[nombre] = m; return m
    X = lambda m: [('X', m)] * 30   # la MISMA etiqueta en las dos corridas
    for s in (20191, 20192):
        a = ME.run_solapadas(s, [('X', ME.carga_eco('FABRICA_ECO'))] * 9, T=4000, diag=0)
        b = ME.run_solapadas(s, [('X', ME.carga_eco('FRANK_ECO'))] * 9, T=4000, diag=0)
        chk(f"(0) s{s} eco=None: FRANK_ECO (organos apagados) == FABRICA_ECO en toda la fisica", fis(a) == fis(b))
    cfg = lambda **kw: {**dict(refunda=1, t_corte=3000, p_mut=0.0, sigma=0.15, banco=50, n_sombra=8, cada_gen=1000, mutables=None,
                               donante='padre'), **kw}
    G0_18 = ME.genoma0(__import__('pista2').cfg_fabrica())
    a = ME.run_solapadas(20193, X(ME.carga_eco('FABRICA_ECO')), T=5000, diag=0, mundo_n=30, eco=cfg())
    b = ME3.run_solapadas(20193, X(ME3.carga_eco('FRANK_ECO')), T=5000, diag=0, mundo_n=30, eco=cfg())
    chk("(1) MUT0, organos apagados: motor_eco3 + FRANK_ECO == motor_eco + FABRICA_ECO en la fisica (esc 30)",
        fis(a) == fis(b) and a['eco']['n_nac'] == b['eco']['n_nac'], f"(nacidos {a['eco']['n_nac']})")
    gall = np.concatenate([G0_18, [1.2] * 7])
    a = ME.run_solapadas(20193, X(modulo('carro_eco_FRANK_TODO', OF.TODO)), T=5000, diag=0, mundo_n=30, eco=cfg())
    b = ME3.run_solapadas(20193, X(ME3.carga_eco('FRANK_ECO')), T=5000, diag=0, mundo_n=30, eco=cfg(genoma=gall.tolist()))
    chk("(2) MUT0, los 7 organos prendidos == el Frankenstein TODO en la fisica", fis(a) == fis(b), f"(nacidos {a['eco']['n_nac']})")
    gher = np.concatenate([G0_18, [0.9] * 5, [1.2], [0.9]])
    a = ME.run_solapadas(20193, X(modulo('carro_eco_FRANK_HER', {'herencia': 1})), T=5000, diag=0, mundo_n=30, eco=cfg())
    b = ME3.run_solapadas(20193, X(ME3.carga_eco('FRANK_ECO')), T=5000, diag=0, mundo_n=30, eco=cfg(genoma=gher.tolist()))
    c = ME3.run_solapadas(20193, X(ME3.carga_eco('FRANK_ECO')), T=5000, diag=0, mundo_n=30, eco=cfg())
    chk("(3) MUT0, solo herencia prendida == el Frankenstein con solo herencia, y distinto de todo apagado", fis(a) == fis(b) and fis(b) != fis(c),
        f"(nacidos {a['eco']['n_nac']} contra {c['eco']['n_nac']} apagado)")
    vistos = []
    esp = types.ModuleType('carro_eco_ESPIA3')

    def crea(ctx):
        car = ME3.carga_eco('FRANK_ECO').crea(ctx); kw = ctx['fabrica']['kw']
        vistos.append(all(car.PK[k] == int(float(kw.get(k, 0.9)) >= 1.0) for k in OF.PERILLAS) and 'herencia' in kw)
        vistos.append(dict(car.PK)); return car
    esp.crea = crea; sys.modules['carro_eco_ESPIA3'] = esp
    ME3.run_solapadas(20194, [('ESPIA', esp)] * 30, T=12000, diag=0, mundo_n=30, eco=cfg(p_mut=0.05, t_corte=8000))
    coh = all(v for v in vistos[0::2]); pk = vistos[1::2]
    prend = {k: sum(p[k] for p in pk) for k in OF.PERILLAS}
    chk("(4) VIDA con mutacion: cada perilla == (su gen >= 1.0) en cada cuerpo, y la mutacion prende organos", coh and sum(prend.values()) > 0,
        f"(cuerpos {len(pk)}; con cada organo {prend})")
    ck = {}

    def guarda(t, blob): ck[t] = blob
    r1 = ME3.run_solapadas(20195, ['FRANK_ECO'] * 30, T=6000, diag=0, mundo_n=30, eco=cfg(p_mut=0.05, ckpt_cada=2000, ckpt_fn=guarda))
    r2 = ME3.run_solapadas(20195, ['FRANK_ECO'] * 30, T=6000, diag=0, mundo_n=30, eco=cfg(p_mut=0.05, estado=ck[4000]))
    q = lambda r: json.dumps(r['eco'], sort_keys=True, default=str)
    chk("(5) checkpoint en 4000 + reanuda == corrida entera (eco y fisica)", q(r1) == q(r2) and fis(r1) == fis(r2), f"(nacidos {r1['eco']['n_nac']})")
    n = sum(R_)
    print(f"RESULTADO: {n}/{len(R_)}  ({time.time() - t0:.0f} s)")
    return n == len(R_)


if __name__ == '__main__':
    buf = io.StringIO()

    class Tee:
        def write(self, x): sys.__stdout__.write(x); buf.write(x)
        def flush(self): sys.__stdout__.flush()
        def reconfigure(self, **kw): pass
    with contextlib.redirect_stdout(Tee()):
        ok = main()
    open(os.path.join(AQUI, 'identidad_eco_frank_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
