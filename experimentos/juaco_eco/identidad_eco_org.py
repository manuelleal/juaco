"""identidad_eco_org.py — ARNES Python de ECO v2 (órganos como genes): motor_eco2 + carros/FAMB_ORG_ECO. Un proceso. Nube, 24-sep-2026.

MISION: llegar a la AGI por este camino.

  (K) construye_eco_org.py --verifica: lo que está en disco es lo construido desde los orígenes (sha fijado).
  (G) GENES de motor_eco2 = los 18 de motor_eco + ('ensena', 'filtra0'); G0 de los órganos 0.9 (apagados); rango [0.225, 3.6].
  (0) eco=None: FAMB_ORG_ECO (órganos apagados por defecto) == FABRICA_ECO en toda la física (motor_eco, 9 carros, T 4000).
  (1) eco MUT0 con los órganos en G0 (apagados): motor_eco2 + FAMB_ORG_ECO == motor_eco + FABRICA_ECO en la física (esc 30, T 5000).
  (2) eco MUT0 con ensena = filtra0 = 1.2 (prendidos): motor_eco2 + FAMB_ORG_ECO == motor_eco + FAMB_RES0_ECO en la física.
  (3) eco MUT0 con ensena = 1.2, filtra0 = 0.9: == motor_eco + FAMB_RES con _see de ECO y SIN0 = 0 en la física.
  (4) VIDA con mutación: en cada cuerpo creado, ENSENA == (gen ensena >= 1.0) y FILTRA0 == (gen filtra0 >= 1.0); la mutación prende
      órganos (hay cuerpos con ENSENA en True).
  (5) checkpoint a mitad + reanuda == corrida entera (VIDA, motor_eco2 + FAMB_ORG_ECO).
Escribe identidad_eco_org_salida.txt.
"""
import contextlib, importlib.util, io, json, os, sys, tempfile, time, types
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')]
R_ = []


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def fis(r):
    return (json.dumps([{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']], sort_keys=True, default=str),
            json.dumps({k: v for k, v in r['pista'].items() if k != 'pizarra_final'}, sort_keys=True, default=str))


def carga(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec); sys.modules[nombre] = m; spec.loader.exec_module(m); return m


def main():
    import motor_eco as ME
    import motor_eco2 as ME2
    import construye_eco_org as CO
    import construye_eco_familia as CF
    t0 = time.time()
    print(f"IDENTIDAD ECO v2 (organos) · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · motor_eco2 "
          f"{CO.CE.h16(CO.DEST_MOTOR)} · FAMB_ORG_ECO {CO.CE.h16(CO.DEST_CARRO)} · construye {CO.CE.h16(os.path.join(AQUI, 'construye_eco_org.py'))}")
    chk("(K) motor_eco2 y FAMB_ORG_ECO en disco == construidos", all(open(p, encoding='utf-8').read() == s for p, s in CO.textos().items()))
    G0 = ME2.genoma0(__import__('pista2').cfg_fabrica()); lo, hi = ME2.rangos(G0)
    chk("(G) genes = 18 de motor_eco + ensena, filtra0; G0 0.9; rango [0.225, 3.6]",
        ME2.NOMBRES == ME.NOMBRES + ('ensena', 'filtra0') and list(G0[-2:]) == [0.9, 0.9] and abs(lo[-1] - 0.225) < 1e-12 and abs(hi[-1] - 3.6) < 1e-12,
        f"({len(ME2.NOMBRES)} genes)")
    # (0) eco=None
    for s in (19905, 19906):
        a = ME.run_solapadas(s, [('X', ME.carga_eco('FABRICA_ECO'))] * 9, T=4000, diag=0)
        b = ME.run_solapadas(s, [('X', ME.carga_eco('FAMB_ORG_ECO'))] * 9, T=4000, diag=0)
        chk(f"(0) s{s} eco=None: FAMB_ORG_ECO (organos apagados) == FABRICA_ECO en toda la fisica", fis(a) == fis(b))
    cfg = lambda **kw: {**dict(refunda=1, t_corte=3000, p_mut=0.0, sigma=0.15, banco=50, n_sombra=8, cada_gen=1000, mutables=None,
                               donante='padre'), **kw}
    X = lambda nombre: [('X', ME.carga_eco(nombre))] * 30   # la MISMA etiqueta en las dos corridas: el nombre del carro va en el registro
    G0_18 = ME.genoma0(__import__('pista2').cfg_fabrica())
    # (1) organos en G0 (apagados) con MUT0
    a = ME.run_solapadas(19907, X('FABRICA_ECO'), T=5000, diag=0, mundo_n=30, eco=cfg())
    b = ME2.run_solapadas(19907, X('FAMB_ORG_ECO'), T=5000, diag=0, mundo_n=30, eco=cfg())
    chk("(1) MUT0, organos apagados: motor_eco2 + FAMB_ORG_ECO == motor_eco + FABRICA_ECO en la fisica (esc 30)",
        fis(a) == fis(b) and a['eco']['t_ext'] == b['eco']['t_ext'] and a['eco']['n_nac'] == b['eco']['n_nac'],
        f"(nacidos {a['eco']['n_nac']})")
    # (2) organos prendidos
    gon = np.concatenate([G0_18, [1.2, 1.2]])
    a = ME.run_solapadas(19907, X('FAMB_RES0_ECO'), T=5000, diag=0, mundo_n=30, eco=cfg())
    b = ME2.run_solapadas(19907, X('FAMB_ORG_ECO'), T=5000, diag=0, mundo_n=30, eco=cfg(genoma=gon.tolist()))
    chk("(2) MUT0, ensena y filtra0 prendidos: == motor_eco + FAMB_RES0_ECO en la fisica", fis(a) == fis(b) and a['eco']['n_nac'] == b['eco']['n_nac'],
        f"(nacidos {a['eco']['n_nac']})")
    # (3) ensena prendido, filtra0 apagado == FAMB_RES con _see de ECO y SIN0 = 0
    tmp = tempfile.mkdtemp(prefix='org_'); p0 = os.path.join(tmp, 'FAMB_RES_ECO_SIN0_0.py'); open(p0, 'w', encoding='utf-8').write(CF.texto(0))
    m0 = carga(p0, 'carro_eco_FAMB_RES_ECO_SIN0_0')
    g10 = np.concatenate([G0_18, [1.2, 0.9]])
    a = ME.run_solapadas(19907, [('X', m0)] * 30, T=5000, diag=0, mundo_n=30, eco=cfg())
    b = ME2.run_solapadas(19907, X('FAMB_ORG_ECO'), T=5000, diag=0, mundo_n=30, eco=cfg(genoma=g10.tolist()))
    chk("(3) MUT0, ensena prendido y filtra0 apagado: == FAMB_RES (con _see de ECO, SIN0 = 0) en la fisica", fis(a) == fis(b),
        f"(nacidos {a['eco']['n_nac']}; difiere de (2): {fis(a) != fis(ME2.run_solapadas(19907, X('FAMB_ORG_ECO'), T=5000, diag=0, mundo_n=30, eco=cfg(genoma=gon.tolist())))})")
    # (4) VIDA con mutacion: la expresion sigue al gen
    base = carga(CO.DEST_CARRO, 'carro_eco_FAMB_ORG_ECO_c'); vistos = []
    esp = types.ModuleType('carro_eco_ESPIA')

    def crea(ctx):
        c = base.crea(ctx); kw = ctx['fabrica']['kw']
        vistos.append((c.ENSENA, float(kw.get('ensena', 0.9)) >= 1.0, c.FILTRA0, float(kw.get('filtra0', 0.9)) >= 1.0)); return c
    esp.crea = crea
    sys.modules['carro_eco_ESPIA'] = esp
    ME2.run_solapadas(19908, [('ESPIA', esp)] * 30, T=12000, diag=0, mundo_n=30, eco=cfg(p_mut=0.05, t_corte=8000))
    coh = all(a_ == b_ and c_ == d_ for a_, b_, c_, d_ in vistos)
    chk("(4) VIDA con mutacion: el organo se expresa si y solo si su gen >= 1.0, y la mutacion lo prende en algunos cuerpos",
        coh and any(v[0] for v in vistos) and any(v[2] for v in vistos),
        f"(cuerpos {len(vistos)}; con ensena {sum(v[0] for v in vistos)}; con filtra0 {sum(v[2] for v in vistos)})")
    # (5) checkpoint
    ck = {}

    def guarda(t, blob): ck[t] = blob
    r1 = ME2.run_solapadas(19909, ['FAMB_ORG_ECO'] * 30, T=6000, diag=0, mundo_n=30, eco=cfg(p_mut=0.05, ckpt_cada=2000, ckpt_fn=guarda))
    r2 = ME2.run_solapadas(19909, ['FAMB_ORG_ECO'] * 30, T=6000, diag=0, mundo_n=30, eco=cfg(p_mut=0.05, estado=ck[4000]))   # por nombre: el pickle lo necesita
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
    open(os.path.join(AQUI, 'identidad_eco_org_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
