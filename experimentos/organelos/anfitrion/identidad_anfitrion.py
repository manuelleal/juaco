"""identidad_anfitrion.py — ARNES del paquete CONTROL DEL ANFITRION (organelos, Opus B, 24-sep-2026). Un proceso, sin Pool.

MISION: llegar a la AGI por este camino.

  (F)   construye_anf.py --verifica y construye_siembras.py --verifica (motor y siembras = lo que dan las anclas y las fuentes de sha fijado).
  (A1)  simb=None: motor_anf == motor_endo BIT A BIT (eco VIDA w30, vivero + corte).
  (A2)  brazo de hoy VIDA_S: motor_anf == motor_endo BIT A BIT (salida completa, d['simb'] incluido).
  (A3)  brazo de hoy AZAR_S: idem.
  (A4)  CONTROL APAGADO: SIN_CONTROL sin siembra == motor_endo VIDA_S bit a bit (quitando solo las claves nuevas del paquete).
  (A5)  CONTROL con mutacion 0 y sin siembra == motor_endo VIDA_S (el control que nace apagado y no se mueve no cambia nada).
  (S)   SIEMBRA: 30 fundadores con simbionte (primera muestra con 30 portadores), banco del vivero alineado; SIN_TRAGAR no siembra.
  (K1a) pieza tx: control fijo tx = 0 -> ningun PARTO transmite (rechazos > 0; toda transmision de parto es None).
  (K1b) pieza tx: tx = 1 -> cero rechazos y cero numeros del rng del control consumidos por tx.
  (K2a) pieza san: san = 1 -> cada candidato se sanciona (sanciones == candidatos > 0).
  (K2b) pieza san: san = 0 -> candidatos > 0 y cero sanciones; INERTE con san = 1 -> cero candidatos (sin canal no hay empuje).
  (M)   mutacion del control: CONTROL mueve tx/san (mut_ctl > 0, valores en [0, 1]); SIN_CONTROL deja todo en (1, 0).
  (Z)   AZAR: el control sale del anillo (mut_ctl > 0) y el simbionte del anillo de AZAR_S (azar_sorteos > 0).
  (E)   determinismo de CONTROL.
  (H)   contabilidad: tragados = digeridos + quedan; bancos alineados (simbiontes y control).
  (N9)  nube-9: corre_anf.trabajo con un brazo invalido NO lanza (devuelve 'error' y escribe su JSON).
Uso: python experimentos/organelos/anfitrion/identidad_anfitrion.py
"""
import json, os, subprocess, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
DARWIN = os.path.join(os.path.dirname(AQUI), 'darwin')
for _d in (os.path.join(RAIZ, 'experimentos', 'generaciones'), os.path.join(RAIZ, 'experimentos', 'juaco_eco'), DARWIN, AQUI):
    if _d in sys.path: sys.path.remove(_d)
    sys.path.insert(0, _d)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.dont_write_bytecode = True
import motor_endo as MD
import motor_anf as MA
import corre_eco as CR
import corre_anf as RA
import control_anfitrion as CA

SALIDA = os.path.join(AQUI, 'identidad_anfitrion_salida.txt')
S = 26994
T, TC = 6000, 3000
casos = []
flog = open(SALIDA, 'w', encoding='utf-8')
NUEVAS = ('brazo_anf', 'ctl_cfg', 'n_siembra_s', 'serie_ctl', 'ctl_final', 'ctl_banco', 'bank_c_alineado', 'ind10')
EV_NUEVOS = ('rechazos_tx', 'sanciones', 'sancion_candidatos', 'sembrados', 'mut_ctl')


def log(s):
    print(s, flush=True); flog.write(s + '\n'); flog.flush()


def caso(n, ok, det=''):
    casos.append((n, bool(ok))); log(f"[{time.strftime('%H:%M:%S')}] ({n}) {'PASA' if ok else 'FALLA'} {det}")


def J(r, limpia=False):
    r = json.loads(json.dumps(r, default=repr))
    if limpia and 'simb' in r:
        for k in NUEVAS: r['simb'].pop(k, None)
        for k in EV_NUEVOS: r['simb']['eventos'].pop(k, None)
    return json.dumps(r, sort_keys=True)


def run(mod, simb=None, siembra=False, seed=S, T_=T, tc=TC):
    e = CR.eco_cfg('VIDA', tc)
    kw = dict(T=T_, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=1000, eco=e)
    if simb is not None:
        simb = dict(simb)
        if siembra: simb['siembra_s'] = RA.siembras()['simbiontes']
        kw['simb'] = simb
    return mod.run_solapadas(seed, ['FABRICA_SIMB'] * 30, **kw)


t0 = time.time()
log(f"ARNES identidad_anfitrion · python {sys.version.split()[0]} · semilla {S} · T {T} corte {TC}")
p1 = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_anf.py'), '--verifica'], capture_output=True, text=True)
p2 = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_siembras.py'), '--verifica'], capture_output=True, text=True)
caso('F', 'VERIFICA OK' in p1.stdout and 'VERIFICA OK' in p2.stdout, f"motor {p1.stdout.strip()} · siembras {p2.stdout.strip()}")
a, b = run(MD), run(MA)
caso('A1', J(a) == J(b), f"simb=None · nac {a['eco']['n_nac']} refund {a['eco']['n_refund']}")
a, b = run(MD, dict(brazo='VIDA_S')), run(MA, dict(brazo='VIDA_S'))
ref_vida = a
caso('A2', J(a) == J(b), f"VIDA_S · tragados {a['simb']['eventos']['tragados']} quedan {a['simb']['eventos']['quedan']}")
a, b = run(MD, dict(brazo='AZAR_S')), run(MA, dict(brazo='AZAR_S'))
caso('A3', J(a) == J(b), f"AZAR_S · sorteos {a['simb']['eventos']['azar_sorteos']}")
b = run(MA, dict(brazo='SIN_CONTROL'))
caso('A4', J(b, True) == J(ref_vida), "SIN_CONTROL sin siembra == motor_endo VIDA_S")
b = run(MA, dict(brazo='CONTROL', p_mut_ctl=0.0))
caso('A5', J(b, True) == J(ref_vida), f"CONTROL p_mut_ctl 0 sin siembra == motor_endo VIDA_S (rechazos {b['simb']['eventos']['rechazos_tx']}, sanciones {b['simb']['eventos']['sanciones']})")
rs = run(MA, dict(brazo='CONTROL'), siembra=True)
e = rs['simb']['eventos']; s0 = rs['simb']['serie'][0]
rst = run(MA, dict(brazo='SIN_TRAGAR'), siembra=True)
caso('S', e['sembrados'] == 30 and s0[2] == 30 and rs['simb']['banco_alineado'] == 1 and rst['simb']['eventos']['sembrados'] == 0 and rst['simb']['serie'][0][2] == 0,
     f"sembrados {e['sembrados']} · portadores en t=0 {s0[2]} · SIN_TRAGAR sembrados {rst['simb']['eventos']['sembrados']}")
k1 = run(MA, dict(brazo='CONTROL', p_mut_ctl=0.0, ctl0=(0.0, 0.0)), siembra=True)
dp = [d for d in k1['simb']['don'] if d[2] == 1]
caso('K1a', k1['simb']['eventos']['rechazos_tx'] > 0 and all(d[1] is None for d in dp),
     f"tx 0: rechazos {k1['simb']['eventos']['rechazos_tx']} · transmisiones de parto no nulas {sum(1 for d in dp if d[1] is not None)} de {len(dp)}")
k1b = run(MA, dict(brazo='CONTROL', p_mut_ctl=0.0, ctl0=(1.0, 0.0)), siembra=True)
k1c = run(MA, dict(brazo='SIN_CONTROL'), siembra=True)
caso('K1b', k1b['simb']['eventos']['rechazos_tx'] == 0 and J(k1b, True).replace('"CONTROL"', '"X"') == J(k1c, True).replace('"SIN_CONTROL"', '"X"'),
     "tx 1 y san 0 fijos (CONTROL sin mutacion) == SIN_CONTROL con siembra: el rng del control no se toca")
k2 = run(MA, dict(brazo='CONTROL', p_mut_ctl=0.0, ctl0=(1.0, 1.0)), siembra=True)
e2 = k2['simb']['eventos']
caso('K2a', e2['sanciones'] == e2['sancion_candidatos'] > 0, f"san 1: candidatos {e2['sancion_candidatos']} sanciones {e2['sanciones']}")
e3 = k1b['simb']['eventos']
ki = run(MA, dict(brazo='INERTE', p_mut_ctl=0.0, ctl0=(1.0, 1.0)), siembra=True)
caso('K2b', e3['sancion_candidatos'] > 0 and e3['sanciones'] == 0 and ki['simb']['eventos']['sancion_candidatos'] == 0,
     f"san 0: candidatos {e3['sancion_candidatos']} sanciones {e3['sanciones']} · INERTE san 1: candidatos {ki['simb']['eventos']['sancion_candidatos']}")
cf = rs['simb']['ctl_final'] + rs['simb']['ctl_banco']; cfs = k1c['simb']['ctl_final'] + k1c['simb']['ctl_banco']
caso('M', e['mut_ctl'] > 0 and any(tuple(c) != CA.CTL0 for c in cf) and all(0 <= x <= 1 for c in cf for x in c) and all(tuple(c) == CA.CTL0 for c in cfs),
     f"CONTROL mut_ctl {e['mut_ctl']} · distintos de (1,0): {sum(1 for c in cf if tuple(c) != CA.CTL0)}/{len(cf)} · SIN_CONTROL todos (1,0): {all(tuple(c) == CA.CTL0 for c in cfs)}")
rz = run(MA, dict(brazo='AZAR'), siembra=True)
caso('Z', rz['simb']['eventos']['mut_ctl'] > 0 and rz['simb']['eventos']['azar_sorteos'] > 0,
     f"AZAR mut_ctl {rz['simb']['eventos']['mut_ctl']} · sorteos {rz['simb']['eventos']['azar_sorteos']}")
rs2 = run(MA, dict(brazo='CONTROL'), siembra=True)
caso('E', J(rs) == J(rs2), "CONTROL dos veces")
okH = all(x['simb']['eventos']['tragados'] == x['simb']['eventos']['digeridos'] + x['simb']['eventos']['quedan'] and x['simb']['banco_alineado'] == 1
          and x['simb']['bank_c_alineado'] == 1 for x in (rs, rz, k2, ki))
caso('H', okH, "tragados = digeridos + quedan; bancos de simbionte y de control alineados (CONTROL, AZAR, K2, INERTE)")
with tempfile.TemporaryDirectory() as td:
    try:
        x = RA.trabajo((S, 'NO_EXISTE', 2000, 1000, td, False)); ok9 = bool(x.get('error')) and os.path.exists(os.path.join(td, f'NO_EXISTE_s{S}.json'))
        det = x.get('error')
    except BaseException as ex:
        ok9 = False; det = f"lanzo {type(ex).__name__}: {ex}"
caso('N9', ok9, f"trabajo con brazo invalido devuelve error sin lanzar: {det}")
n_ok = sum(1 for _, o in casos if o)
log(f"RESULTADO: {n_ok}/{len(casos)} · {round(time.time() - t0)} s · {'N/N' if n_ok == len(casos) else 'FALLA: no hay humo'}")
flog.close()
sys.exit(0 if n_ok == len(casos) else 1)
