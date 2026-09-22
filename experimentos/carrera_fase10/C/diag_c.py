"""EJECUCION 1 de la BACTERIA C — DIAGNOSTICO: ¿de que muere el cuerpo nuevo que YA sabe que comer?

MISION: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos
preregistrados con controles y replicas). Carrera: acercar el organismo a la fase 10.

NO es un instrumento nuevo: usa organismo_f9_rapido.py (93955a5315ce5f17, gemelo bit a bit de organismo_f9.py
3a821884394d66c9; arnes 138/138 x45 corrido en esta maquina, salida en arnes_f9_rapido_T4000.log) y el
resumen/los brazos de corre_f9.py SIN COPIARLOS (regla 14: no se reimplementa lo que ya tiene dueno).

Contesta P-C0 (ancla) y P-C1 (diagnostico) del PREREGISTRO_C.md, firmadas antes de correr esto.

UN proceso, sin Pool. 12 corridas de T = 100 000. Escribe su JSON (ERR-42) y una linea por pregunta (ERR-89).
Uso:  python experimentos/carrera_fase10/C/diag_c.py --humo
"""
import json, os, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N9 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo')
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
sys.path[:0] = [N9, N13, N11, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import corre_f9 as CF
import organismo_f9_rapido as R9

SEEDS = [3201, 3202, 3203]
ARMS = ['RENACE', 'NADA', 'M1', 'REL']
T = 100000


def h16(p):
    import hashlib
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def main():
    t0 = time.time()
    print('BACTERIA C — EJECUCION 1 (diagnostico). Un proceso, sin Pool.', flush=True)
    print('  gemelo organismo_f9_rapido.py sha %s (arnes 138/138 x45)' % h16(os.path.join(N9, 'organismo_f9_rapido.py')), flush=True)
    print('  tronco organismo_f9.py        sha %s' % h16(os.path.join(N9, 'organismo_f9.py')), flush=True)
    print('  brazos y resumen de corre_f9.py sha %s (no se copian)' % h16(os.path.join(N9, 'corre_f9.py')), flush=True)
    filas = []
    for brazo in ARMS:
        kw = dict(CF.BRAZOS[brazo], rep_acum=0)
        for s in SEEDS:
            ta = time.time()
            r = R9.run(s, T=T, **kw)
            o = CF.resumen(brazo, s, 0, r, time.time() - ta)
            # diagnostico extra, SOLO LECTURA sobre el crudo
            vidas = r.get('vidas_h1') or r.get('vidas') or []
            mn = r.get('muertes_nec') or [0, 0]
            o['mu_hambre'] = mn[0]
            o['mu_sed'] = mn[1]
            o['frac_sed'] = round(mn[1] / max(mn[0] + mn[1], 1), 4)
            o['vida_p10'] = int(st.quantiles(vidas, n=10)[0]) if len(vidas) >= 10 else None
            o['vida_p90'] = int(st.quantiles(vidas, n=10)[8]) if len(vidas) >= 10 else None
            o['vidas_n'] = len(vidas)
            o['exp_C'] = (r.get('exposiciones') or {}).get('C')
            o['exp_D'] = (r.get('exposiciones') or {}).get('D')
            f = r.get('f9') or {}
            tok = [x for x in (f.get('t_ok') or []) if x >= 0]
            o['t_ok_n'] = len(tok)
            o['t_ok_sin'] = len([x for x in (f.get('t_ok') or []) if x < 0])
            o['t_ok_frac_vida'] = round(st.median(tok) / st.median(vidas), 4) if tok and vidas else None
            filas.append(o)
            print('  %-8s s%-5d R0 %.3f  vida %7.1f  t_ok %s  sac %s  mu(hambre/sed) %d/%d  %.2fs'
                  % (brazo, s, o['R0'], o['vida_med'] or -1, o['t_ok'], o['sac_frac'],
                     o['mu_hambre'], o['mu_sed'], o['seg']), flush=True)

    def M(b, c):
        xs = [x[c] for x in filas if x['brazo'] == b and x[c] is not None]
        return round(st.median(xs), 4) if xs else None

    ver = {}
    # P-C0 (ancla firmada)
    p0 = dict(R0_NADA=M('NADA', 'R0'), vida_NADA=M('NADA', 'vida_med'), R0_RENACE=M('RENACE', 'R0'),
              R0_REL=M('REL', 'R0'), vida_REL=M('REL', 'vida_med'))
    ok0 = (0.10 <= (p0['R0_NADA'] or -1) <= 0.22 and 90 <= (p0['vida_NADA'] or -1) <= 170
           and 0.70 <= (p0['R0_RENACE'] or -1) <= 1.40 and 0.28 <= (p0['R0_REL'] or -1) <= 0.48
           and 300 <= (p0['vida_REL'] or -1) <= 900)
    ver['P-C0'] = dict(frase='ANCLA: el instrumento no se movio (NADA, RENACE y REL de la fase 9)',
                       medido=p0, pasa=bool(ok0))
    # P-C1 (diagnostico firmado)
    frs = M('REL', 'frac_sed')
    p1 = dict(t_ok_REL=M('REL', 't_ok'), t_ok_frac_vida=M('REL', 't_ok_frac_vida'), frac_sed_REL=frs,
              t_ok_NADA=M('NADA', 't_ok'), sac_REL=M('REL', 'sac_frac'), sac_RENACE=M('RENACE', 'sac_frac'))
    ok1 = ((p1['t_ok_REL'] or 0) >= 15 and frs is not None and 0.20 <= frs <= 0.80)
    ver['P-C1'] = dict(frase='DIAGNOSTICO: el que ya sabe que comer muere por no conseguir recurso (hambre Y sed), '
                             'y pierde pasos antes de su primera mordida buena', medido=p1, pasa=bool(ok1))
    for k, v in ver.items():
        print('[%s] %s -> %s  %s' % (k, v['frase'], 'PASA' if v['pasa'] else 'CAE', json.dumps(v['medido'])), flush=True)

    sello = time.strftime('%Y%m%d_%H%M%S')
    ruta = os.path.join(AQUI, 'C_E1_diagnostico_%s.json' % sello)
    json.dump(dict(ejecucion=1, bacteria='C', T=T, seeds=SEEDS, brazos=ARMS, acum=0,
                   gemelo=h16(os.path.join(N9, 'organismo_f9_rapido.py')),
                   tronco_f9=h16(os.path.join(N9, 'organismo_f9.py')),
                   runner_f9=h16(os.path.join(N9, 'corre_f9.py')),
                   filas=filas, veredicto=ver, seg=round(time.time() - t0, 2)),
              open(ruta, 'w', encoding='utf-8'), indent=1)
    print('JSON: %s  (%.1fs)' % (ruta, time.time() - t0), flush=True)


if __name__ == '__main__':
    main()
