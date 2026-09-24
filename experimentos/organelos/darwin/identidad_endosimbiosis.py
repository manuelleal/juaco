"""identidad_endosimbiosis.py — ARNES de identidad del instrumento de ENDOSIMBIOSIS (organelos, Opus B, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Un proceso, sin Pool. Casos (cada uno PASA o FALLA; N/N o no hay humo):
  (F)  construye_endo.py --verifica: motor_endo.py y carros/FABRICA_SIMB.py son EXACTAMENTE lo que dan las anclas sobre los origenes
       de sha fijado.
  (A1) simb=None, FABRICA_ECO, eco VIDA (vivero + corte), w30:  motor_endo == motor_eco3 BIT A BIT (toda la salida).
  (A2) idem con eco AZAR (donante 'azar').
  (A3) idem con eco del juez (refunda 0, sin mutacion, genomas dados), w9.
  (A4) idem con eco=None (pista v2 pura, carro FABRICA de la carrera), 9 linajes.
  (B)  simb=None con FABRICA_SIMB == motor_eco3 con FABRICA_ECO (el nombre del carro normalizado): el carro copia es FABRICA_ECO sin canal.
  (C)  simb SIN_TRAGAR con FABRICA_SIMB: toda la salida del BICHO (sin d['simb']) == motor_eco3 + FABRICA_ECO, y los libres viven
       (nacen y siguen vivos): la ecologia de los simbiontes no toca el mundo del bicho (trampa 3: no se come la comida).
  (D1) INERTE con FABRICA_SIMB == INERTE con FABRICA_ECO (salida completa, d['simb'] incluido): el canal de INERTE esta APAGADO de verdad.
  (D2) VIDA_S con FABRICA_SIMB != VIDA_S con FABRICA_ECO y hubo decisiones de boca con canal: el canal ACTUA.
  (E)  determinismo: VIDA_S dos veces, salida identica.
  (G1) guardia de ERR-60 con NAC_MAX bajo y simb=None: lanza el SystemExit de motor_eco3 (mismo mensaje).
  (G2) idem con simb: NO lanza; registra err60 y t_trunc (nube-9).
  (H)  contabilidad de eventos: tragados = digeridos + quedan; banco de simbiontes alineado; libres >= 0.
  (I)  BARAJADO baraja (barajados > 0) y AZAR_S sortea del anillo (azar_sorteos > 0).
  (J)  la PERDIDA ocurre (trinquete de Fable): el simbionte muere adentro y falla en el parto (conteos > 0).
Uso: python experimentos/organelos/darwin/identidad_endosimbiosis.py
"""
import json, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')
for _d in (os.path.join(RAIZ, 'experimentos', 'generaciones'), ECO, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import motor_eco3 as M3
import motor_endo as MD
import corre_eco as CR

SALIDA = os.path.join(AQUI, 'identidad_endosimbiosis_salida.txt')
S = 22994      # practica (22990-22999)
casos = []
flog = open(SALIDA, 'w', encoding='utf-8')


def log(s):
    print(s, flush=True); flog.write(s + '\n'); flog.flush()


def J(r, norm=True, sin_simb=False):
    r = dict(r)
    if sin_simb: r.pop('simb', None)
    s = json.dumps(r, sort_keys=True, default=repr)
    return s.replace('FABRICA_SIMB', 'FABRICA_ECO') if norm else s


def caso(nombre, ok, detalle=''):
    casos.append((nombre, bool(ok)))
    log(f"[{time.strftime('%H:%M:%S')}] ({nombre}) {'PASA' if ok else 'FALLA'} {detalle}")


def w30(mod, carro, eco, T, simb=None, n=30, esc=30, seed=S):
    kw = dict(T=T, diag=0, mundo_n=esc, tope_cuerpos=3000, muestra=1000, eco=eco)
    if simb is not None: kw['simb'] = simb
    return mod.run_solapadas(seed, [carro] * n, **kw)


t0 = time.time()
log(f"ARNES identidad_endosimbiosis · python {sys.version.split()[0]} · semilla {S}")
# (F)
p = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_endo.py'), '--verifica'], capture_output=True, text=True)
caso('F', p.returncode == 0 and 'VERIFICA OK' in p.stdout, p.stdout.strip())
# (A1)-(A4)
r3 = w30(M3, 'FABRICA_ECO', CR.eco_cfg('VIDA', 3000), 6000); rd = w30(MD, 'FABRICA_ECO', CR.eco_cfg('VIDA', 3000), 6000)
caso('A1', J(r3, False) == J(rd, False), f"VIDA w30 T 6000 corte 3000 · nac {r3['eco']['n_nac']} refund {r3['eco']['n_refund']} vivos {len(r3['eco']['vivos_final'])}")
ref_vida = r3
r3 = w30(M3, 'FABRICA_ECO', CR.eco_cfg('AZAR', 2000), 3000); rd = w30(MD, 'FABRICA_ECO', CR.eco_cfg('AZAR', 2000), 3000)
caso('A2', J(r3, False) == J(rd, False), f"AZAR w30 T 3000 · nac {r3['eco']['n_nac']} refund {r3['eco']['n_refund']}")
import numpy as np
import pista2
G0 = M3.genoma0(pista2.cfg_fabrica())
gs = [list(G0 * np.exp(np.random.default_rng([S, 99, i]).normal(0, 0.1, len(G0)))) for i in range(9)]
lo, hi = M3.rangos(G0); gs = [list(np.clip(g, lo, hi)) for g in gs]
ej = dict(refunda=0, p_mut=0.0, genoma=gs)
r3 = w30(M3, 'FABRICA_ECO', ej, 4000, n=9, esc=9); rd = w30(MD, 'FABRICA_ECO', ej, 4000, n=9, esc=9)
caso('A3', J(r3, False) == J(rd, False), f"juez w9 T 4000 · t_ext {r3['eco']['t_ext']}")
r3 = M3.run_solapadas(S, ['FABRICA'] * 9, T=2000, diag=0); rd = MD.run_solapadas(S, ['FABRICA'] * 9, T=2000, diag=0)
caso('A4', J(r3, False) == J(rd, False), f"eco=None, 9 FABRICA, T 2000 · max_vivos {r3['pista']['max_vivos']}")
# (B)
rb = w30(MD, 'FABRICA_SIMB', CR.eco_cfg('VIDA', 3000), 6000)
caso('B', J(rb) == J(ref_vida), "FABRICA_SIMB sin simb == FABRICA_ECO (motor_eco3)")
# (C)
rc = w30(MD, 'FABRICA_SIMB', CR.eco_cfg('VIDA', 3000), 6000, simb=dict(brazo='SIN_TRAGAR'))
ev = rc['simb']['eventos']
caso('C', J(rc, sin_simb=True) == J(ref_vida) and ev['nac_libres'] > 0 and rc['simb']['n_libres_final'] > 0 and ev['tragados'] == 0,
     f"bicho == motor_eco3; libres nacidos {ev['nac_libres']}, vivos al final {rc['simb']['n_libres_final']}, tragados {ev['tragados']}")
# (D1)
ri1 = w30(MD, 'FABRICA_SIMB', CR.eco_cfg('VIDA', 3000), 6000, simb=dict(brazo='INERTE'))
ri2 = w30(MD, 'FABRICA_ECO', CR.eco_cfg('VIDA', 3000), 6000, simb=dict(brazo='INERTE'))
evi = ri1['simb']['eventos']
caso('D1', J(ri1) == J(ri2) and evi['quedan'] > 0 and evi['decisiones_canal'] == 0,
     f"INERTE: SIMB == ECO con simb · tragados {evi['tragados']} quedan {evi['quedan']} herencias {evi['herencias']} decisiones con canal {evi['decisiones_canal']}")
# (D2)
rv1 = w30(MD, 'FABRICA_SIMB', CR.eco_cfg('VIDA', 3000), 6000, simb=dict(brazo='VIDA_S'))
rv2 = w30(MD, 'FABRICA_ECO', CR.eco_cfg('VIDA', 3000), 6000, simb=dict(brazo='VIDA_S'))
evv = rv1['simb']['eventos']
caso('D2', J(rv1) != J(rv2) and evv['decisiones_canal'] > 0,
     f"VIDA_S: el canal cambia la corrida · decisiones con canal {evv['decisiones_canal']} · tragados {evv['tragados']} quedan {evv['quedan']} herencias {evv['herencias']}")
# (E)
rv3 = w30(MD, 'FABRICA_SIMB', CR.eco_cfg('VIDA', 3000), 6000, simb=dict(brazo='VIDA_S'))
caso('E', J(rv1) == J(rv3), "VIDA_S dos veces")
# (G1)/(G2)
MD.NAC_MAX = 5
try:
    w30(MD, 'FABRICA_ECO', CR.eco_cfg('VIDA', 3000), 6000); g1 = (False, 'no lanzo')
except SystemExit as e:
    g1 = ('ERR-60' in str(e), str(e))
caso('G1', g1[0], f"simb=None lanza: {g1[1]}")
try:
    rg = w30(MD, 'FABRICA_SIMB', CR.eco_cfg('VIDA', 3000), 6000, simb=dict(brazo='VIDA_S'))
    g2 = (rg['simb']['err60'] is not None and rg['simb']['t_trunc'] is not None, f"err60 {rg['simb']['err60']} t_trunc {rg['simb']['t_trunc']}")
except SystemExit as e:
    g2 = (False, f"lanzo {e}")
MD.NAC_MAX = 100000
caso('G2', g2[0], g2[1])
# (H)
okH = all(x['simb']['eventos']['tragados'] == x['simb']['eventos']['digeridos'] + x['simb']['eventos']['quedan'] and x['simb']['banco_alineado'] == 1
          for x in (ri1, rv1, rc))
caso('H', okH, f"tragados = digeridos + quedan y banco alineado en INERTE, VIDA_S, SIN_TRAGAR")
# (I)
# (I) y (J) prueban MECANICA: se sube p_trag a 0.05 para que haya portadores en 6000 pasos (no son los valores de la serie)
rbj = w30(MD, 'FABRICA_SIMB', CR.eco_cfg('VIDA', 3000), 6000, simb=dict(brazo='BARAJADO', p_trag=0.05))
raz = w30(MD, 'FABRICA_SIMB', CR.eco_cfg('VIDA', 3000), 6000, simb=dict(brazo='AZAR_S', p_trag=0.05))
caso('I', rbj['simb']['eventos']['barajados'] > 0 and raz['simb']['eventos']['azar_sorteos'] > 0,
     f"barajados {rbj['simb']['eventos']['barajados']} · sorteos AZAR_S {raz['simb']['eventos']['azar_sorteos']} (p_trag 0.05)")
rj = w30(MD, 'FABRICA_SIMB', CR.eco_cfg('VIDA', 3000), 6000, simb=dict(brazo='VIDA_S', p_trag=0.05))
ej_ = rj['simb']['eventos']
caso('J', ej_['perdidas_internas'] > 0 and ej_['fallas_herencia'] > 0 and ej_['herencias'] > 0,
     f"PERDIDA (trinquete de Fable): perdidas internas {ej_['perdidas_internas']} · fallas de herencia en el parto {ej_['fallas_herencia']} · herencias {ej_['herencias']} (p_trag 0.05)")
n_ok = sum(1 for _, o in casos if o)
log(f"RESULTADO: {n_ok}/{len(casos)} · {round(time.time() - t0)} s · {'N/N' if n_ok == len(casos) else 'FALLA: no hay humo'}")
flog.close()
sys.exit(0 if n_ok == len(casos) else 1)
