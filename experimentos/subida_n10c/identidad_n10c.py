"""identidad_n10c.py — ARNES de subida_n10c. Se corre ANTES del humo y de cualquier serie. Un proceso, sin Pool.

MISION: llegar a la AGI por este camino.

  (I) cada variante con el filtro APAGADO == su carro base de n10b BIT A BIT en toda la fisica (linajes sin el espacio 'carro',
      y la pista), T 5000 con partos, semillas de practica 12892 y 12893: RES_SIN0~RES, BAR_SIN0~BAR, ORA_SIN0~ORACULO.
  (F) sin_neutras() quita EXACTAMENTE las entradas con R == 0 y conserva el orden.
  (O) la tabla de ORA_SIN0 son las 4 entradas con R != 0 de la tabla verdadera del ORACULO, en su orden.
  (T) con el filtro ENCENDIDO ningun hijo de RES_SIN0 ni de BAR_SIN0 instala una entrada neutra (telemetria _TELE: B|hambre,
      D|sed, A|hambre, C|sed nunca valen 0), y hubo partos con tabla.
  (E) corre_n10c.tarea == corre_n10b.tarea (sin reasignar) en NADA y RES: mismo estr, semilla 12892, T 5000.
  (D) determinismo de RES_SIN0 y BAR_SIN0.
  (R) el parser aborta ante banderas malas (ERR-115) y un subproceso con bandera desconocida sale con codigo != 0 sin escribir nada.
Escribe identidad_n10c_salida.txt.
"""
import io, contextlib, glob, json, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'subida_n10b')); sys.path.insert(0, AQUI)
import corre_n10b as CN
ORIG = dict(carga=CN.carga, MONO=CN.MONO, MIX=list(CN.MIX), PARES=CN.PARES, PARES_MIX=CN.PARES_MIX)
import carros_n10c as C3
import corre_n10c as C10

R = []


def chk(nombre, ok, det=''):
    R.append(bool(ok)); print(f"  {'OK ' if ok else 'MAL'} {nombre} {det}", flush=True)


def corre(seed, mod, T, etiqueta):
    P2, MC, _ = CN._importa_mundo()
    return P2.run(seed, [(etiqueta, mod)] * 9, T=T, diag=0, solapadas=1, reposicion='fija', tope_cuerpos=MC.TOPE_DEF, r_rep=MC.R_REP)


def fisica(r):
    return json.dumps([{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']], sort_keys=True, default=str), \
        json.dumps({k: v for k, v in r['pista'].items() if k != 'pizarra_final'}, sort_keys=True, default=str)


def main():
    t0 = time.time()
    print(f"IDENTIDAD n10c · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]}")
    # (I) filtro apagado == base
    for s in (12892, 12893):
        for var, b in (('RES_SIN0', 'RES'), ('BAR_SIN0', 'BAR'), ('ORA_SIN0', 'ORACULO')):
            a = corre(s, C3.modulo(b), 5000, f'FAMB_{b}'); c = corre(s, C3.modulo(var, filtro=False), 5000, f'FAMB_{b}')
            nac = sum(1 for d in a['linajes'] for x in d['individuos'] if not x[6])
            chk(f"(I) s{s} {var} con filtro apagado == {b} en toda la fisica", fisica(a) == fisica(c), f"(nacidos {nac})")
    # (F)
    tab = [[[1, 0], 1.0, 0], [[0, 1], 0.0, 1], [[1, 1], -3.0, 0], [[0, 0], 0.0, 0], [[1, 0], -3.0, 1]]
    chk("(F) sin_neutras quita exactamente las R == 0 y conserva el orden", C3.sin_neutras(tab) == [tab[0], tab[2], tab[4]])
    # (O)
    mo = C3.modulo('ORACULO'); m0 = C3.modulo('ORA_SIN0')
    P2, MC, _ = CN._importa_mundo()
    r = corre(12892, m0, 50, 'FAMB_ORA_SIN0')   # solo para tener un ctx real; la tabla se lee de una instancia nueva
    ctxs = []
    class Espia:
        pass
    # instancia directa: los carros solo necesitan el ctx que arma la pista; se reconstruye con una corrida minima
    import importlib
    tabla_ora = None; tabla_sin0 = None
    try:
        orig_crea_o, orig_crea_0 = mo.crea, m0.crea
        cap = {}
        mo.crea = lambda ctx, _f=orig_crea_o: cap.setdefault('o', _f(ctx))
        m0.crea = lambda ctx, _f=orig_crea_0: cap.setdefault('s', _f(ctx))
        corre(12892, mo, 5, 'FAMB_ORACULO'); corre(12892, m0, 5, 'FAMB_ORA_SIN0')
        tabla_ora = cap['o']._ORA; tabla_sin0 = cap['s']._ORA
    finally:
        mo.crea, m0.crea = orig_crea_o, orig_crea_0
    esperado = [e for e in tabla_ora if e[1] != 0.0]
    chk("(O) ORA_SIN0 = las 4 entradas con R != 0 de la tabla verdadera, en su orden",
        len(tabla_ora) == 8 and len(tabla_sin0) == 4 and tabla_sin0 == esperado, f"R {[e[1] for e in tabla_sin0]}")
    # (T) telemetria con el filtro encendido
    for var in ('RES_SIN0', 'BAR_SIN0'):
        m = C3.modulo(var); corre(12893, m, 20000, f'FAMB_{var}'); T_ = getattr(C3.ULTIMO[var], '_TELE', [])
        neutra = sum(1 for x in T_ for v in x[2:6] if v is not None and v == 0.0)
        chk(f"(T) {var}: ningun hijo instala una entrada neutra y hubo partos con tabla", len(T_) > 0 and neutra == 0,
            f"(tablas instaladas {len(T_)}, neutras {neutra}, claves max {max((x[1] for x in T_), default=0)})")
    # (E) corre_n10c.tarea == corre_n10b.tarea sin reasignar
    for b in ('NADA', 'RES'):
        CN.carga, CN.MONO, CN.MIX, CN.PARES, CN.PARES_MIX = ORIG['carga'], ORIG['MONO'], list(ORIG['MIX']), ORIG['PARES'], ORIG['PARES_MIX']
        x = CN.tarea((12892, b, 5000))
        y = C10.tarea((12892, b, 5000))
        ex = json.dumps(x['estr'], sort_keys=True, default=str); ey = json.dumps(y['estr'], sort_keys=True, default=str)
        chk(f"(E) corre_n10c.tarea == corre_n10b.tarea en {b} (estr completo, s12892, T 5000)", ex == ey)
    # (D)
    for var in ('RES_SIN0', 'BAR_SIN0'):
        a = corre(12892, C3.modulo(var), 5000, f'FAMB_{var}'); c = corre(12892, C3.modulo(var), 5000, f'FAMB_{var}')
        chk(f"(D) determinismo {var}", fisica(a) == fisica(c))
    # (R) parser
    malas = [['--help'], ['-h'], ['--serie'], ['--humo', '--serie'], ['--serie', '--desde', '12801', '--n', '20'],
             ['--serie', '--desde=12801', '--n', '20', '--pool', '3'], ['--serie', '--des', '12801', '--n', '20', '--pool', '3'],
             ['--serie', '--desde', '12701', '--n', '20', '--pool', '3'], ['--serie', '--desde', '12801', '--n', '19', '--pool', '3'],
             ['--serie', '--desde', '12801', '--n', '20', '--pool', '9'], ['--humo', '--pool', '2'], ['--humo', '--humo'],
             ['--serie', '--desde', 'x', '--n', '20', '--pool', '3']]
    n_ab = 0
    for m in malas:
        try: C10.parsea(m)
        except C10.BanderaMala: n_ab += 1
    chk("(R) el parser aborta ante 13 formas de bandera mala", n_ab == len(malas), f"({n_ab}/{len(malas)})")
    antes = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    pr = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_n10c.py'), '--serie', '--desde', '12801', '--n', '20', '--pool', '3', '--nada'],
                        capture_output=True, text=True, timeout=120)
    despues = set(glob.glob(os.path.join(AQUI, 'datos', '**', '*'), recursive=True))
    chk("(R) subproceso con bandera desconocida: codigo != 0 y no escribe nada", pr.returncode != 0 and antes == despues, f"(codigo {pr.returncode})")
    n = sum(R)
    print(f"RESULTADO: {n}/{len(R)}  ({time.time() - t0:.0f} s)")
    return n == len(R)


if __name__ == '__main__':
    buf = io.StringIO()

    class Tee:
        def write(self, x): sys.__stdout__.write(x); buf.write(x)
        def flush(self): sys.__stdout__.flush()
        def reconfigure(self, **kw): pass   # corre_convive llama a sys.stdout.reconfigure al importarse
    with contextlib.redirect_stdout(Tee()):
        ok = main()
    open(os.path.join(AQUI, 'identidad_n10c_salida.txt'), 'w', encoding='utf-8').write(buf.getvalue())
    sys.exit(0 if ok else 1)
