import sys, os, json, time
RAIZ = "/home/user/juaco"
for d in ("experimentos/organelos/darwin", "experimentos/organelos/anfitrion",
          "experimentos/juaco_eco", "experimentos/generaciones"):
    sys.path.insert(0, os.path.join(RAIZ, d))
sys.dont_write_bytecode = True
import motor_endo as MD
import motor_anf as MA
import corre_eco as CR
SEED = 26995
T, TC = 100000, 40000
NUEVAS = ('brazo_anf', 'ctl_cfg', 'n_siembra_s', 'serie_ctl', 'ctl_final', 'ctl_banco', 'bank_c_alineado', 'ind10')
EV_NUEVOS = ('rechazos_tx', 'sanciones', 'sancion_candidatos', 'sembrados', 'mut_ctl')
def J(r, limpia=False):
    r = json.loads(json.dumps(r, default=repr))
    if limpia and 'simb' in r:
        for k in NUEVAS: r['simb'].pop(k, None)
        for k in EV_NUEVOS: r['simb']['eventos'].pop(k, None)
    return json.dumps(r, sort_keys=True)
def run(mod, simb):
    e = CR.eco_cfg('VIDA', TC)
    kw = dict(T=T, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=1000, r_rep=0.03, eco=e, simb=dict(simb))
    return mod.run_solapadas(SEED, ['FABRICA_SIMB'] * 30, **kw)
def P(*a): print(time.strftime('[%H:%M:%S]'), *a, flush=True)
P(f"escala anfitrion · semilla {SEED} · T {T} corte {TC}")
t0=time.time(); ref = run(MD, dict(brazo='VIDA_S')); P(f"motor_endo VIDA_S listo ({time.time()-t0:.0f} s)")
t0=time.time(); b_sc = run(MA, dict(brazo='SIN_CONTROL')); P(f"A4-escala SIN_CONTROL == motor_endo: {J(b_sc, True) == J(ref)} ({time.time()-t0:.0f} s)")
t0=time.time(); b_c0 = run(MA, dict(brazo='CONTROL', p_mut_ctl=0.0)); P(f"A5-escala CONTROL p_mut_ctl 0 == motor_endo: {J(b_c0, True) == J(ref)} ({time.time()-t0:.0f} s)")
P("FIN")
