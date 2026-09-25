"""identidad_escala_endo.py — identidad A1 y C a la ESCALA de la serie (T 120 000, corte 60 000), hallazgo H-2 del auditor
(coordinador, 24-sep-2026). El arnés del creador corre a T <= 6000; esto comprueba que a la duración real no aparece divergencia.
Un proceso, sin Pool, semilla de práctica 22995 (fuera de serie 22001-22020 y réplica 22021-22040).
  (A1-escala) simb=None, FABRICA_ECO, VIDA w30: motor_endo == motor_eco3 bit a bit.
  (C-escala)  SIN_TRAGAR con FABRICA_SIMB: la salida del bicho (sin d['simb']) == motor_eco3 + FABRICA_ECO; libres vivos.
Uso: python experimentos/organelos/darwin/identidad_escala_endo.py
"""
import json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')
for _d in (os.path.join(RAIZ, 'experimentos', 'generaciones'), ECO, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.dont_write_bytecode = True
import motor_eco3 as M3
import motor_endo as MD
import corre_eco as CR

S, T, TC = 22995, 120000, 60000


def J(r, sin_simb=False):
    r = dict(r)
    if sin_simb: r.pop('simb', None)
    return json.dumps(r, sort_keys=True, default=repr).replace('FABRICA_SIMB', 'FABRICA_ECO')


def w30(mod, carro, simb=None):
    kw = dict(T=T, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=1000, eco=CR.eco_cfg('VIDA', TC))
    if simb is not None: kw['simb'] = simb
    return mod.run_solapadas(S, [carro] * 30, **kw)


t0 = time.time()
r3 = w30(M3, 'FABRICA_ECO'); print(f"motor_eco3 listo {time.time() - t0:.0f} s", flush=True)
rd = w30(MD, 'FABRICA_ECO'); print(f"motor_endo listo {time.time() - t0:.0f} s", flush=True)
a1 = J(r3) == J(rd)
print(f"(A1-escala) {'PASA' if a1 else 'FALLA'} nac {r3['eco']['n_nac']} refund {r3['eco']['n_refund']} vivos {len(r3['eco']['vivos_final'])}", flush=True)
rc = w30(MD, 'FABRICA_SIMB', simb=dict(brazo='SIN_TRAGAR'))
ev = rc['simb']['eventos']
c = J(rc, sin_simb=True) == J(r3) and ev['nac_libres'] > 0 and ev['tragados'] == 0
print(f"(C-escala) {'PASA' if c else 'FALLA'} libres nacidos {ev['nac_libres']} vivos al final {rc['simb']['n_libres_final']} tragados {ev['tragados']}", flush=True)
print(f"RESULTADO: {int(a1) + int(c)}/2 · {time.time() - t0:.0f} s", flush=True)
