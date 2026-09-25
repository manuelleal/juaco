"""identidad_eco_familia.py — ARNES del carro FAMB_RES0_ECO (ECO v1.2). Un proceso, sin Pool. Nube, 24-sep-2026.

MISION: llegar a la AGI por este camino.

  (K) construye_eco_familia.py --verifica: el carro en disco es el construido desde FAMB_RES.py (sha fijado).
  (0) con SIN0 = 0 el carro == FAMB_RES de subida_n10b en TODA la fisica (motor_eco con eco=None = motor_convive, 9 carros, T 5000,
      semillas de practica 19606 y 19607): el _see hacia afuera no cambia nada.
  (1) con SIN0 = 1 (el carro en disco) == RES_SIN0 de subida_n10c (carros_n10c.modulo) en TODA la fisica, mismas semillas.
  (T) con SIN0 = 1 ningun hijo instala una entrada neutra en B|hambre, D|sed, A|hambre, C|sed, y hubo partos con tabla (T 20000).
  (E) con eco=dict (vivero, mutacion, banco, corte) corre, y un checkpoint a mitad + --reanuda == la corrida entera (E7 de ECO).
Escribe identidad_eco_familia_salida.txt.
"""
import contextlib, importlib.util, io, json, os, pickle, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones'), os.path.join(RAIZ, 'experimentos', 'subida_n10c'),
                os.path.join(RAIZ, 'experimentos', 'subida_n10b')]
R_ = []


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def carga(ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def fisica(r):
    return (json.dumps([{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']], sort_keys=True, default=str),
            json.dumps({k: v for k, v in r['pista'].items() if k != 'pizarra_final'}, sort_keys=True, default=str))


def main():
    import motor_eco as ME
    import construye_eco_familia as CF
    import carros_n10c as C3
    t0 = time.time()
    print(f"IDENTIDAD FAMB_RES0_ECO · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · "
          f"construye {CF.CE.h16(os.path.join(AQUI, 'construye_eco_familia.py'))} · carro {CF.CE.h16(CF.DESTINO)} · FAMB_RES {CF.CE.h16(CF.ORIG)}")
    s = CF.texto(1)
    chk("(K) el carro en disco es el construido", open(CF.DESTINO, encoding='utf-8').read() == s)
    tmp = tempfile.mkdtemp(prefix='famb_eco_')
    p0 = os.path.join(tmp, 'FAMB_RES0_ECO_SIN0_0.py'); open(p0, 'w', encoding='utf-8').write(CF.texto(0))
    corre = lambda seed, mod, T, etq: ME.run_solapadas(seed, [(etq, mod)] * 9, T=T, diag=0)
    for seed in (19606, 19607):
        a = corre(seed, carga(CF.ORIG, 'famb_res_orig'), 5000, 'FAMB_RES')
        b = corre(seed, carga(p0, 'famb_res0_eco_0'), 5000, 'FAMB_RES')
        nac = sum(1 for d in a['linajes'] for x in d['individuos'] if not x[6])
        chk(f"(0) s{seed}: SIN0 = 0 == FAMB_RES en toda la fisica", fisica(a) == fisica(b), f"(nacidos {nac})")
        c = corre(seed, C3.modulo('RES_SIN0'), 5000, 'FAMB_RES')
        d = corre(seed, carga(CF.DESTINO, 'famb_res0_eco_1'), 5000, 'FAMB_RES')
        chk(f"(1) s{seed}: el carro (SIN0 = 1) == RES_SIN0 de n10c en toda la fisica", fisica(c) == fisica(d),
            f"(la fisica difiere de FAMB_RES: {fisica(a) != fisica(d)})")
    m = carga(CF.DESTINO, 'famb_res0_eco_t')
    corre(19608, m, 20000, 'FAMB_RES')
    T_ = getattr(m, '_TELE', [])
    neutra = sum(1 for x in T_ for v in x[2:6] if v is not None and v == 0.0)
    chk("(T) ningun hijo instala una entrada neutra y hubo partos con tabla", len(T_) > 0 and neutra == 0,
        f"(tablas {len(T_)}, neutras {neutra}, claves max {max((x[1] for x in T_), default=0)})")
    # (E) con eco: corrida entera contra checkpoint + reanuda
    G0 = ME.genoma0(__import__('pista2').cfg_fabrica())
    cfg = lambda **kw: dict(refunda=1, t_corte=3000, p_mut=0.05, sigma=0.15, banco=200, n_sombra=8, cada_gen=1000, mutables=None,
                            donante='padre', **kw)
    ck = {}

    def guarda(t, blob): ck[t] = blob
    # la corrida entera con el carro registrado en sys.modules (el checkpoint lo necesita para el pickle)
    mods = ('FAMB_RES0_ECO', )
    r1 = ME.run_solapadas(19609, ['FAMB_RES0_ECO'] * 30, T=6000, diag=0, mundo_n=30, eco=cfg(ckpt_cada=2000, ckpt_fn=guarda))
    r2 = ME.run_solapadas(19609, ['FAMB_RES0_ECO'] * 30, T=6000, diag=0, mundo_n=30, eco=cfg(estado=ck[4000]))
    q = lambda r: json.dumps({k: v for k, v in r['eco'].items()}, sort_keys=True, default=str)
    chk("(E) con eco: checkpoint en 4000 + reanuda == la corrida entera (eco y fisica)", q(r1) == q(r2) and fisica(r1) == fisica(r2),
        f"(t_ext {r1['eco']['t_ext']}, nacidos {r1['eco']['n_nac']}, corte {bool(r1['eco']['corte'])})")
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
    open(os.path.join(AQUI, 'identidad_eco_familia_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
