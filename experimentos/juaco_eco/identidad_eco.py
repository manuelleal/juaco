"""identidad_eco.py — ARNES de JUACO-ECO. Se corre ANTES de mirar numeros. Un proceso, sin Pool.

MISION: llegar a la AGI por este camino.

  (0) ORIGEN: sha de motor_convive / FABRICA / APR y los construidos == lo que produce construye_eco.py.
  (I) eco=None: motor_eco == motor_convive BIT A BIT en TODA la salida (4 configuraciones: FABRICA fija, O2 inmediata, mixta, APR).
  (F) _see rapido: FABRICA_ECO._see == FABRICA._see en 200000 casos al azar (incluye rechazos, empates y 'todos rechazados'),
      y corridas completas de la pista v2 con FABRICA_ECO / APR_ECO == FABRICA / APR.
  (E) plomeria del genoma con las perillas apagadas: eco=dict(refunda=1) con G0, sombras, banco, mutables=() y donante='azar'
      sin mutacion == pista v2 (el mundo no cambia por llevar genoma).
  (M) mutacion: determinista; tasa medida ~ p_mut; rangos respetados; genes no mutables quedan en G0.
  (R) refunda=0: nunca hay fundador repuesto; prefijo identico a refunda=1 hasta el primer fundador; si todo muere, para y marca.
  (V) vivero: ningun fundador despues de t_corte; el banco alimenta a los fundadores; la foto del corte existe.
  (C) checkpoint: corrida seguida == corrida cortada en un checkpoint y reanudada (TODA la salida); firma distinta aborta.
  (S) flujo de individuos: filas == muertes + vivos finales, y l.ind queda vacio.
  (G) guardias: clave eco desconocida, genoma fuera de rango, t_corte sin vivero; runner con bandera desconocida, abreviada,
      ventana de semillas no declarada.
Uso: python experimentos/juaco_eco/identidad_eco.py   (escribe identidad_eco_salida.txt; la ultima linea es RESULTADO: N/N)
"""
import json, os, pickle, subprocess, sys, time, types
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')]
import construye_eco as CE
import motor_convive as MC
import motor_eco as ME
import pista2 as P

N = lambda x: json.dumps(x, default=str, sort_keys=True)
OK = [0, 0]
SAL = open(os.path.join(AQUI, 'identidad_eco_salida.txt'), 'w', encoding='utf-8')


def out(s=''):
    print(s, flush=True); SAL.write(s + '\n'); SAL.flush()


def di(et, ok, extra=''):
    OK[1] += 1; OK[0] += int(bool(ok))
    out(f"  [{'OK ' if ok else 'FALLA'}] {et}{(' · ' + extra) if extra else ''}")


def sin_eco(r):
    r = dict(r); r.pop('eco', None); return r


def aborta(f):
    try: f()
    except SystemExit as e: return str(e)
    return None


t00 = time.time()
FAB = P.carga_carro('FABRICA'); APR = P.carga_carro('APR')
FE = ME.carga_eco('FABRICA_ECO'); AE = ME.carga_eco('APR_ECO')
CF = P.cfg_fabrica(); G0 = ME.genoma0(CF)

out('(0) ORIGEN')
for nom, p in (('motor_convive.py', CE.ORIG_MOTOR), ('FABRICA.py', os.path.join(CE.ORIG_CARROS, 'FABRICA.py')),
               ('APR.py', os.path.join(CE.ORIG_CARROS, 'APR.py'))):
    di(f"{nom} sha {CE.SHA[nom]}", CE.h16(p) == CE.SHA[nom])
arts = CE.construye()
di("motor_eco.py, FABRICA_ECO.py, APR_ECO.py == construccion por anclas", all(open(p, encoding='utf-8').read() == s for p, s in arts.items()))

out('(I) eco=None == motor_convive BIT A BIT')
for et, carros, kw in (("9 FABRICA fija T=3000", ['FABRICA'] * 9, dict(T=3000)),
                       ("9 O2 inmediata T=2000", ['O2'] * 9, dict(T=2000, reposicion='inmediata')),
                       ("O2*3+O3*3+O4*3 fija T=2000", ['O2'] * 3 + ['O3'] * 3 + ['O4'] * 3, dict(T=2000)),
                       ("9 APR fija T=1500", ['APR'] * 9, dict(T=1500))):
    a = MC.run_solapadas(10001, carros, diag=0, **kw); b = ME.run_solapadas(10001, carros, diag=0, **kw)
    di(et, N(a) == N(b))

out('(F) _see rapido')
rng = np.random.default_rng(424242); malos = 0; empates = 0; todos_rech = 0
for caso in range(200000):
    L = int(rng.choice([7, 40, 41, 360, 3600])); no = int(rng.integers(1, min(L, 40) + 1))
    xs = rng.choice(L, size=no, replace=False); objs = {int(x): 'ABCD'[int(rng.integers(4))] for x in xs}
    t = int(rng.integers(0, 1000)); pos = int(rng.integers(L))
    rech = {int(x): t + int(rng.integers(-5, 30)) for x in xs if rng.random() < float(rng.choice([0.0, 0.3, 1.0]))}
    mr = int(rng.choice([0, 20]))
    def dummy():
        return types.SimpleNamespace(L=L, MEMORIA_RECHAZO=mr, _rech=dict(rech), sin_objetivo=[0] * 4, T=4000,
                                     _q=lambda tt: min(tt // 1000, 3))
    d1, d2 = dummy(), dummy(); contar = bool(rng.random() < 0.5)
    r1 = FAB.Carro._see(d1, pos, objs, t, contar); r2 = FE.Carro._see(d2, pos, objs, t, contar)
    if r1 != r2 or d1.sin_objetivo != d2.sin_objetivo: malos += 1
    if r1 is not None and r1[0] > 0 and ((pos - r1[0]) % L in objs) and ((pos + r1[0]) % L in objs) and (pos - r1[0]) % L != (pos + r1[0]) % L: empates += 1
    todos_rech += int(d1.sin_objetivo != [0] * 4)
di("FABRICA_ECO._see == FABRICA._see en 200000 casos", malos == 0, f"distintos {malos}; empates a igual distancia {empates}; 'todos rechazados' {todos_rech}")
a = MC.run_solapadas(10002, ['FABRICA'] * 9, T=3000, diag=0); b = MC.run_solapadas(10002, [('FABRICA', FE)] * 9, T=3000, diag=0)
di("pista v2: 9 FABRICA_ECO == 9 FABRICA (T=3000, toda la salida)", N(a) == N(b))
a = MC.run_solapadas(10003, ['APR'] * 9, T=2000, diag=0); b = MC.run_solapadas(10003, [('APR', AE)] * 9, T=2000, diag=0)
di("pista v2: 9 APR_ECO == 9 APR (T=2000, toda la salida)", N(a) == N(b))
a = MC.run_solapadas(10004, ['FABRICA'] * 9, T=2000, diag=0, mundo_n=9, reposicion='inmediata')
b = MC.run_solapadas(10004, [('FABRICA', FE)] * 9, T=2000, diag=0, mundo_n=9, reposicion='inmediata')
di("pista v2 inmediata: FABRICA_ECO == FABRICA", N(a) == N(b))

out('(E) plomeria del genoma, perillas apagadas == pista v2')
base = MC.run_solapadas(10005, [('FABRICA', FE)] * 9, T=3000, diag=0)
for et, eco in (("eco=dict(refunda=1) con G0", dict(refunda=1)),
                ("+ 8 sombras, cada_gen 500, banco 50", dict(refunda=1, n_sombra=8, cada_gen=500, banco=50)),
                ("p_mut 0.3 con mutables=() (ningun gen muta)", dict(refunda=1, p_mut=0.3, mutables=(), n_sombra=2, banco=50)),
                ("donante='azar' sin mutacion", dict(refunda=1, donante='azar', n_sombra=2, banco=50)),
                ("genoma explicito = G0", dict(refunda=1, genoma=list(G0)))):
    r = ME.run_solapadas(10005, [('FABRICA', FE)] * 9, T=3000, diag=0, eco=eco)
    di(et, N(sin_eco(r)) == N(base), f"nacimientos {r['eco']['n_nac']}, fundadores del banco {r['eco']['n_banco']}")

out('(M) mutacion')
kwm = dict(T=6000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500)
ecm = dict(refunda=1, p_mut=0.2, n_sombra=4, cada_gen=1000, banco=100)
r1 = ME.run_solapadas(10006, ['FABRICA_ECO'] * 18, eco=ecm, **kwm); r2 = ME.run_solapadas(10006, ['FABRICA_ECO'] * 18, eco=ecm, **kwm)
di("determinista (dos corridas iguales)", N(r1) == N(r2))
E = r1['eco']; eventos = E['n_nac'] + E['n_banco']; NG = len(E['genes'])
tasa = E['n_mut'] / max(1, eventos * NG); tasa_s = E['n_mut_s'] / max(1, E['n_nac'] * NG * 4)
sd = (0.2 * 0.8 / max(1, eventos * NG)) ** 0.5
di("tasa de mutacion por gen ~ p_mut (0.2; los enteros pueden quedar en el tope)", eventos > 20 and abs(tasa - 0.2) < max(4 * sd, 0.03) + 0.02,
   f"eventos {eventos}, tasa {tasa:.4f}, sombras {tasa_s:.4f}")
lo, hi = np.array(E['lo']), np.array(E['hi'])
V = np.array([v[4:] for v in E['vivos_final']]) if E['vivos_final'] else np.zeros((0, NG))
di("rangos respetados en los vivos finales", len(V) > 0 and bool(((V >= lo - 1e-12) & (V <= hi + 1e-12)).all()), f"vivos {len(V)}")
ecc = dict(ecm, mutables=('alpha', 'eta_s'))
r3 = ME.run_solapadas(10007, ['FABRICA_ECO'] * 18, eco=ecc, **kwm)
V3 = np.array([v[4:] for v in r3['eco']['vivos_final']]); jm = [ME.NOMBRES.index('alpha'), ME.NOMBRES.index('eta_s')]
otros = [j for j in range(NG) if j not in jm]
di("mutables=(alpha, eta_s): los otros genes quedan en G0", len(V3) > 0 and bool((V3[:, otros] == G0[otros]).all()) and bool((V3[:, jm] != G0[jm]).any()),
   f"vivos {len(V3)}; cambian {int((V3[:, jm] != G0[jm]).any(1).sum())}")

out('(R) refunda=0 (ERR-118: nadie repone fundadores)')
kwr = dict(T=6000, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=100)
ra = ME.run_solapadas(10008, ['FABRICA_ECO'] * 9, eco=dict(refunda=1), **kwr)
rb = ME.run_solapadas(10008, ['FABRICA_ECO'] * 9, eco=dict(refunda=0), **kwr)
di("refunda=0: cero fundadores repuestos", sum(l['fundadores'] for l in rb['linajes']) == 0 and rb['eco']['n_refund'] == 0)
tf = min([t for l in ra['linajes'] for t in l['t_fund']] or [10 ** 9])
kwp = dict(kwr, T=tf)   # con T = primer fundador, ninguna de las dos corridas llega a reponer: deben ser IGUALES en todo
pa = ME.run_solapadas(10008, ['FABRICA_ECO'] * 9, eco=dict(refunda=1), **kwp); pb = ME.run_solapadas(10008, ['FABRICA_ECO'] * 9, eco=dict(refunda=0), **kwp)
di("refunda=0 == refunda=1 (TODA la salida fisica) hasta el primer fundador", 0 < tf < 6000 and N(sin_eco(pa)) == N(sin_eco(pb))
   and sum(sum(v) for l in pa['linajes'] for v in l['mord'].values()) > 0,
   f"primer fundador en t={tf}; mordidas antes {sum(sum(v) for l in pa['linajes'] for v in l['mord'].values())}")
te = rb['eco']['t_ext']
di("si todo muere, muere (t_ext marcado y cero vivos) o hay vivos en T", (te is not None and rb['eco']['vivos_final'] == []) or (te is None and len(rb['eco']['vivos_final']) > 0),
   f"t_ext {te}")

out('(V) vivero y corte')
rv = ME.run_solapadas(10009, ['FABRICA_ECO'] * 18, T=6000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500,
                      eco=dict(refunda=1, t_corte=3000, p_mut=0.05, banco=100, n_sombra=4, cada_gen=1000))
tfs = [t for l in rv['linajes'] for t in l['t_fund']]
di("ningun fundador despues de t_corte", len(tfs) > 0 and max(tfs) < 3000, f"fundadores {len(tfs)}, ultimo t={max(tfs) if tfs else None}")
di("el banco alimenta fundadores y la foto del corte existe", rv['eco']['n_banco'] > 0 and rv['eco']['corte'] is not None and rv['eco']['corte']['t'] == 3000,
   f"desde banco {rv['eco']['n_banco']}; corte {rv['eco']['corte'] and {k2: rv['eco']['corte'][k2] for k2 in ('vivos', 'n_banco')}}")

out('(C) checkpoint reanudable')
ck = {}
kwc = dict(T=4000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500)
ecc = dict(refunda=1, t_corte=2500, p_mut=0.1, banco=100, n_sombra=4, cada_gen=500)
seguida = ME.run_solapadas(10010, ['FABRICA_ECO'] * 18, eco=ecc, **kwc)
ME.run_solapadas(10010, ['FABRICA_ECO'] * 18, eco=dict(ecc, ckpt_cada=1000, ckpt_fn=lambda t, b: ck.__setitem__(t, b)), **kwc)
blob = pickle.loads(pickle.dumps(ck[2000]))   # como si viniera de disco
reanudada = ME.run_solapadas(10010, ['FABRICA_ECO'] * 18, eco=dict(ecc, estado=blob), **kwc)
di("seguida == cortada en t=2000 y reanudada (TODA la salida)", N(seguida) == N(reanudada), f"checkpoints {sorted(ck)}; {len(blob) // 1024} KB")
msg = aborta(lambda: ME.run_solapadas(10011, ['FABRICA_ECO'] * 18, eco=dict(ecc, estado=blob), **kwc))
di("checkpoint de otra corrida aborta", msg is not None and 'firma' in msg, str(msg))

out('(S) flujo de individuos')
filas = []
rs = ME.run_solapadas(10008, ['FABRICA_ECO'] * 9, eco=dict(refunda=1, ind_cb=lambda li, row, g: filas.append((li, row))), **kwr)
muertes = sum(l['deaths'] for l in rs['linajes']); vivos = sum(l['vivos_final'] for l in rs['linajes'])
di("filas == muertes + vivos y l.ind vacio", len(filas) == muertes + vivos and all(l['individuos'] == [] for l in rs['linajes']),
   f"filas {len(filas)} = {muertes} + {vivos}")

out('(G) guardias')
di("clave eco desconocida aborta", aborta(lambda: ME.run_solapadas(1, ['FABRICA_ECO'], T=10, diag=0, eco=dict(refnda=0))) is not None)
di("genoma fuera de rango aborta", aborta(lambda: ME.run_solapadas(1, ['FABRICA_ECO'], T=10, diag=0, eco=dict(genoma=list(G0 * 10)))) is not None)
di("t_corte sin vivero (refunda=0) aborta", aborta(lambda: ME.run_solapadas(1, ['FABRICA_ECO'], T=10, diag=0, eco=dict(refunda=0, t_corte=5))) is not None)
RUN = os.path.join(AQUI, 'corre_eco.py')
for et, args in (("runner: bandera desconocida aborta", ['--humo', '--bandera_rara']),
                 ("runner: bandera abreviada aborta (--hum)", ['--hum']),
                 ("runner: --humo con --pool aborta", ['--humo', '--pool', '2']),
                 ("runner: --lee y --humo juntos abortan", ['--humo', '--lee', 'x']),
                 ("runner: --largo fuera de su ventana aborta", ['--largo', '--desde', '19101', '--n', '3', '--pool', '6'])):
    p = subprocess.run([sys.executable, RUN] + args, capture_output=True, text=True, timeout=120)
    di(et, p.returncode != 0, (p.stderr.strip().splitlines() or [''])[-1][:110])
import corre_eco as CR
out('(J) juez automatico (enmienda tras el humo: el banco, no la mediana)')
jb0 = CR.juez(list(G0), (19011, 19012), 3000); jbl = CR.juez([list(G0)] * 200, (19011, 19012), 3000)
di("juez: G0 como genoma == G0 como banco de 200 copias", N(jb0) == N(jbl), str([d['vive'] for d in jb0]))
Gm = G0.copy(); Gm[ME.NOMBRES.index('rep_umbral')] = 0.6; Gm[ME.NOMBRES.index('dote')] = 0.3
jbm = CR.juez([list(Gm)] * 200, (19011, 19012), 3000)
di("juez: un banco distinto de G0 cambia la bateria (el genoma SE expresa)", N(jbm) != N(jb0), f"G0 {[(d['vive'], d['nac']) for d in jb0]} · mutante {[(d['vive'], d['nac']) for d in jbm]}")
bk = [list(G0 * np.exp(0.01 * k)) for k in range(-5, 6)]
f1 = CR.fundadores_juez(bk, 19011); f2 = CR.fundadores_juez(bk, 19011)
di("juez: fundadores del banco deterministas y distintos entre si", bool((f1 == f2).all()) and len({tuple(x) for x in f1}) == 9)
di("runner: ventanas de semillas declaradas (19101 serie, 19121 replica) y bateria 19201-19220",
   CR.VENTANAS == (19101, 19121) and CR.JUEZ['semillas'] == tuple(range(19201, 19221)) and CR.HUMO['semilla'] == 19001)

out(f"tiempo {round(time.time() - t00)} s")
out(f"RESULTADO: {OK[0]}/{OK[1]}")
SAL.close()
