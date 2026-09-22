"""Arnes de identidad de la SONDA organismo_boca2 (perilla apagada == mundo_fase10 BIT A BIT == tronco v14.2 por la cadena) y
MINI-PRUEBA de un proceso (6 corridas) para el ESBOZO del candidato "la boca lee las dos filas". No es serie, no declara nada.

MISION: llegar a la AGI por este camino.
IDENTIDADES (DEBEN ser identicas):
  B1 boca2=0 == mundo_fase10 en el mundo del tronco (organismo_v142 por la cadena), 3 escenarios x 1 semilla, T = 30 000
  B2 boca2=0 == mundo_fase10 en el mundo vivo de la fase 9 (corre_f9 RENACE y REL), semilla 1, T = 20 000
  B3 boca2=0 == mundo_fase10 en el mundo F10 (ENMIENDA 1, REL), semilla 1, T = 20 000
  B4 INERCIA con n_nec = 1: boca2=1 == boca2=0 en el mundo del tronco (3 escenarios; sin la clave 'boca2'): el examen v3' y las
     baterias no ven la perilla -> T-B, T-C (i), T-E y T-F del examen quedarian por identidad (prediccion del esbozo)
CONTROLES QUE DEBEN DIFERIR:
  C1 boca2=1 != 0 en el mundo vivo de la fase 9 (RENACE s1)      C2 boca2=1 != 0 en el mundo F10 (RENACE s1)
MINI-PRUEBA (despues del arnes; 6 corridas, un proceso; los brazos OFF ya estan en diagnostico_boca_mapa y en el humo del repo):
  M1 mundo vivo fase 9, RENACE, s1, T = 20 000, boca2=1        (OFF: D1, veneno con SED 63/84, R0 1.154)
  M2 mundo F10 calib F0, RENACE, s1, T = 20 000, boca2=1        (OFF: D2, veneno con SED 60/68, R0 0.065)
  M3 mundo F10 ENMIENDA 1, RENACE, s1, T = 20 000, boca2=1      (OFF: D4, veneno con SED 18/27, R0 0.483)
  M4 mundo F10 ENMIENDA 1, RENACE, s5, T = 100 000, boca2=1     (OFF: humo, R0 0.306)
  M5 mundo F10 ENMIENDA 1, RENACE, s6, T = 100 000, boca2=1     (OFF: humo, R0 0.214)
  M6 mundo F10 ENMIENDA 1, NADA,   s5, T = 100 000, boca2=1     (OFF: humo, R0 0.146)
Uso: python identidad_y_mini_boca2.py  -> datos/humo/mini_boca2_<sello>.json + .log
"""
import os, sys, time, json

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_mundo_fase10 as CM
import mundo_fase10 as M10
import organismo_boca2 as B2
import corre_f9 as CF
from diagnostico_boca_mapa import tabla, cambiados_de

N, h16 = CM.N, CM.h16
OK = [0, 0]
t0 = time.time()
sel = time.strftime('%Y%m%d_%H%M%S')
os.makedirs(CM.HUMO, exist_ok=True)
logf = open(os.path.join(CM.HUMO, f'mini_boca2_{sel}.log'), 'w', encoding='utf-8')


def log(m=''):
    print(m, flush=True); logf.write(m + '\n'); logf.flush()


def comp(a, b, quitar=()):
    return ([k for k in a if k in b and N(a[k]) != N(b[k])] + [k for k in a if k not in b and k not in quitar]
            + [k for k in b if k not in a and k not in quitar])


def caso(etq, ok, det=''):
    OK[0] += bool(ok); OK[1] += 1
    log(f"  [{time.time()-t0:5.0f}s] {'OK   ' if ok else 'FALLA'} {etq}  {det}")


log(f"ARNES + MINI boca2 · {time.strftime('%Y-%m-%d %H:%M:%S')} · un proceso · mundo_fase10 {h16(os.path.join(AQUI,'mundo_fase10.py'))} · "
    f"organismo_boca2 {h16(os.path.join(AQUI,'organismo_boca2.py'))} · este script {h16(os.path.abspath(__file__))}")
ESC = [('AB por defecto', dict()), ('AB invertido', dict(invertir_en=15000)), ('AB solap_AB=3 (E2L)', dict(solap_AB=3))]
for etq, kw in ESC:
    d = comp(M10.run(1, T=30000, **kw), B2.run(1, T=30000, **kw)); caso(f'B1 tronco {etq} boca2=0', not d, d[:4] or 'IDENTICO')
for b in ('RENACE', 'REL'):
    d = comp(M10.run(1, T=20000, **CF.BRAZOS[b]), B2.run(1, T=20000, **CF.BRAZOS[b])); caso(f'B2 vivo fase 9 {b} boca2=0', not d, d[:4] or 'IDENTICO')
d = comp(M10.run(1, T=20000, **CM.BRAZOS['REL']), B2.run(1, T=20000, **CM.BRAZOS['REL'])); caso('B3 F10 enmienda REL boca2=0', not d, d[:4] or 'IDENTICO')
for etq, kw in ESC:
    d = comp(B2.run(1, T=30000, **kw), B2.run(1, T=30000, boca2=1, **kw), {'boca2'}); caso(f'B4 INERCIA n_nec=1 {etq} boca2=1 == 0', not d, d[:4] or 'IDENTICO (inerte)')
a, b = B2.run(1, T=20000, **CF.BRAZOS['RENACE']), B2.run(1, T=20000, boca2=1, **CF.BRAZOS['RENACE'])
caso('C1 vivo fase 9 RENACE boca2=1 != 0 (DEBE diferir)', N(a) != N(b))
a, b = B2.run(1, T=20000, **CM.BRAZOS['RENACE']), B2.run(1, T=20000, boca2=1, **CM.BRAZOS['RENACE'])
caso('C2 F10 enmienda RENACE boca2=1 != 0 (DEBE diferir)', N(a) != N(b))
log(f"ARNES boca2: {'PASA' if OK[0] == OK[1] else 'NO PASA'} {OK[0]}/{OK[1]}")
if OK[0] != OK[1]:
    sys.exit(1)

PLAN = [('M1_vivo_f9_RENACE', 1, 20000, CF.BRAZOS['RENACE'], ('A', 'B', 'C', 'D'), dict(M10.VAL_VIVO), dict(R0=1.1538, vSED=[63, 84], sHAM=[77, 487])),
        ('M2_F10_calibF0_RENACE', 1, 20000, CM.BRAZOS_F0['RENACE'], CM.TIPOS, dict(CM.VAL16), dict(R0=0.0645, vSED=[60, 68], sHAM=[44, 101])),
        ('M3_F10_enm1_RENACE', 1, 20000, CM.BRAZOS['RENACE'], CM.TIPOS, dict(CM.VAL16), dict(R0=0.4828, vSED=[18, 27], sHAM=[121, 353])),
        ('M4_F10_enm1_RENACE', 5, 100000, CM.BRAZOS['RENACE'], CM.TIPOS, dict(CM.VAL16), dict(R0=0.3059)),
        ('M5_F10_enm1_RENACE', 6, 100000, CM.BRAZOS['RENACE'], CM.TIPOS, dict(CM.VAL16), dict(R0=0.2143)),
        ('M6_F10_enm1_NADA', 5, 100000, CM.BRAZOS['NADA'], CM.TIPOS, dict(CM.VAL16), dict(R0=0.1457))]
OUT = []
log("\nMINI-PRUEBA boca2=1 (los OFF son los del diagnostico y del humo del repo)")
for etq, s, Ti, kw, tipos, vini, off in PLAN:
    r = B2.run(s, T=Ti, boca2=1, **kw)
    cam = cambiados_de(r); fam = {x[1:] for x in cam if x.startswith('*')}
    cam = {k for k in cam if not k.startswith('*')} | {k for k in tipos if vini[k] in fam}
    ex = tabla(r, list(tipos), vini, cam)['exacta']
    R0 = round(r['descendientes'] / (r['deaths'] + 1), 4)
    o = dict(etq=etq, seed=s, T=Ti, R0_on=R0, R0_off=off['R0'], muertes=r['deaths'], muertes_nec=r.get('muertes_nec'), tabla_exacta=ex, off=off)
    OUT.append(o)
    log(f"  [{time.time()-t0:5.0f}s] {etq} s{s}: R0 ON {R0} vs OFF {off['R0']} · muertes {r['deaths']} {r.get('muertes_nec')} · veneno con SED {ex['SEDxveneno']} (OFF {off.get('vSED')}) · "
        f"sal con HAMBRE {ex['HAMBRExsal']} (OFF {off.get('sHAM')}) · comida con HAMBRE {ex['HAMBRExcomida']} · agua con SED {ex['SEDxagua']}")
ruta = os.path.join(CM.HUMO, f'mini_boca2_{sel}.json')
json.dump(dict(bloque='mini_boca2', sello=sel, arnes=f'{OK[0]}/{OK[1]}', corridas=OUT, sha_boca2=h16(os.path.join(AQUI, 'organismo_boca2.py')),
               sha_script=h16(os.path.abspath(__file__)), seg=round(time.time() - t0, 1)), open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
log(f"JSON {ruta} (sha {h16(ruta)}) · {time.time()-t0:.0f}s")
