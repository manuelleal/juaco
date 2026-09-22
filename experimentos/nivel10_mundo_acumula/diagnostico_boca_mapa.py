"""Diagnostico de UN proceso (6 corridas, <= 100 000 pasos cada una) para verificar en el repo el HALLAZGO EXTERNO de la fase 10.

MISION: llegar a la AGI por este camino. Lo externo es HIPOTESIS, no dato: aqui se intenta reproducir con el instrumento del repo.

Hipotesis externas (F0_fable_solo, REGISTRO 20:08; PARA_JUACO_mundo_fase10.md §2):
  H-BOCA  "el conocimiento heredado llega y NO se usa porque la boca decide con la fila de la necesidad ACTIVA": el inmortal muerde
          veneno con SED 57/63 exposiciones y sal con HAMBRE 85/259 en el mundo F10; en el mundo del tronco 75/83 y 101/508.
          Mecanismo declarado: EFECTO['veneno'] = (-0.4, 0.0) -> la fila de la SED recibe R = 0 al morder veneno y nunca aprende que es malo
          (idem sal para la fila del HAMBRE). La boca lee Wp[_nm]-Wn[_nm] con _nm = necesidad activa (CUELLO_MIN solo actua saciado).
  H-MAPA  "el mapa del nivel 6 no sirve como canal del DONDE" (F0: ORACULO con mapa 0.058 vs sin mapa 0.086; F1: MAPA 0.237 vs REL 0.503).

Medida (SOLO LECTURA, claves que el organismo ya devuelve): xor_mord[n][i] = mordidas con necesidad activa n del tipo i;
xor_enc[n][i] = exposiciones (llegadas) con necesidad activa n. Se agrega por VALENCIA. Con cambios de valencia en la corrida, la
cuenta EXACTA usa solo los tipos que nunca cambiaron (f10.cambios); la cuenta por valencia INICIAL de todos los tipos se da al lado
y se marca aproximada.

Corridas (un proceso, sin Pool, regla 3):
  D1 mundo vivo del tronco (corre_f9.BRAZOS['RENACE'], v14.2), semilla 1, T = 20 000
  D2 mundo F10 con la calibracion LITERAL de F0 (MUNDO_F0), RENACE, semilla 1, T = 20 000 (con cambios: exacto sobre tipos sin cambio)
  D3 mundo F10 con la calibracion F0 SIN cambios (cambia_cada=0), RENACE, semilla 1, T = 20 000 (exacto)
  D4 mundo F10 con la calibracion de la ENMIENDA 1, RENACE, semilla 1, T = 20 000
  D5 / D6 mundo F10 ENMIENDA 1: REL y REL_SIN_MAPA, semilla 5, T = 100 000 (H-MAPA; n = 1: solo direccion)
Uso: python diagnostico_boca_mapa.py      -> datos/humo/diagnostico_boca_mapa_<sello>.json + .log
"""
import os, sys, json, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_mundo_fase10 as CM   # pone organismo/ y los experimentos en sys.path (mismo orden que el runner, ERR-28)
import mundo_fase10 as M10
import corre_f9 as CF

HUMO = CM.HUMO
EF = {'comida': (0.8, 0.0), 'veneno': (-0.4, 0.0), 'agua': (0.0, 0.8), 'sal': (0.0, -0.4)}


def tabla(r, tipos, val_ini, cambiados):
    """(necesidad, valencia) -> [mordidas, exposiciones], exacta (tipos sin cambio) y aproximada (valencia inicial, todos)."""
    xm, xe = r['xor_mord'], r['xor_enc']
    out = {}
    for modo, incl in (('exacta', lambda k: k not in cambiados), ('aprox_val_inicial', lambda k: True)):
        d = {}
        for n, nn in ((0, 'HAMBRE'), (1, 'SED')):
            for v in ('comida', 'veneno', 'agua', 'sal'):
                b = sum(xm[n][i] for i, k in enumerate(tipos) if val_ini[k] == v and incl(k))
                e = sum(xe[n][i] for i, k in enumerate(tipos) if val_ini[k] == v and incl(k))
                d[f'{nn}x{v}'] = [int(b), int(e)]
        out[modo] = d
    return out


def cambiados_de(r):
    f = r.get('f10') or {}
    s = set()
    for c in f.get('cambios', []):
        if c[1] == 'variante':
            s |= {c[2], c[3]}
        else:   # familia: todos los tipos de las dos valencias del eje cambian
            s |= {'*' + c[2], '*' + c[3]}
    return s


def main():
    os.makedirs(HUMO, exist_ok=True)
    sel = time.strftime('%Y%m%d_%H%M%S')
    logf = open(os.path.join(HUMO, f'diagnostico_boca_mapa_{sel}.log'), 'w', encoding='utf-8')

    def log(m=''):
        print(m, flush=True); logf.write(m + '\n'); logf.flush()

    t0 = time.time()
    log(f"DIAGNOSTICO boca/mapa · {time.strftime('%Y-%m-%d %H:%M:%S')} · UN proceso, 6 corridas · mundo_fase10 sha {CM.h16(os.path.join(AQUI, 'mundo_fase10.py'))} · "
        f"runner sha {CM.h16(os.path.join(AQUI, 'corre_mundo_fase10.py'))} · este script sha {CM.h16(os.path.abspath(__file__))}")
    log(f"  MUNDO (enmienda 1): { {k: v for k, v in CM.MUNDO.items() if k not in ('pats', 'vals', 'estims')} }")
    log(f"  MUNDO_F0 (literal F0): { {k: v for k, v in CM.MUNDO_F0.items() if k not in ('pats', 'vals', 'estims')} }")
    PLAN = [
        ('D1_tronco_vivo_RENACE', 1, 20000, dict(CF.BRAZOS['RENACE']), ('A', 'B', 'C', 'D'), dict(M10.VAL_VIVO)),
        ('D2_F10_calibF0_RENACE', 1, 20000, dict(CM.BRAZOS_F0['RENACE']), CM.TIPOS, dict(CM.VAL16)),
        ('D3_F10_calibF0_sin_cambios_RENACE', 1, 20000, dict(CM.BRAZOS_F0['RENACE'], cambia_cada=0), CM.TIPOS, dict(CM.VAL16)),
        ('D4_F10_enmienda1_RENACE', 1, 20000, dict(CM.BRAZOS['RENACE']), CM.TIPOS, dict(CM.VAL16)),
        ('D5_F10_enmienda1_REL', 5, 100000, dict(CM.BRAZOS['REL']), CM.TIPOS, dict(CM.VAL16)),
        ('D6_F10_enmienda1_REL_SIN_MAPA', 5, 100000, dict(CM.BRAZOS['REL_SIN_MAPA']), CM.TIPOS, dict(CM.VAL16)),
    ]
    OUT = []
    for etq, s, Ti, kw, tipos, vini in PLAN:
        t1 = time.time()
        r = M10.run(s, T=Ti, **kw)
        cam = cambiados_de(r)
        fam = {x[1:] for x in cam if x.startswith('*')}
        cam = {k for k in cam if not k.startswith('*')} | {k for k in tipos if vini[k] in fam}
        tb = tabla(r, list(tipos), vini, cam)
        d, mu = r['descendientes'], r['deaths']
        o = dict(etq=etq, seed=s, T=Ti, seg=round(time.time() - t1, 1), R0=round(d / (mu + 1), 4), desc=d, muertes=mu,
                 muertes_nec=r.get('muertes_nec'), tipos_cambiados=sorted(cam), n_cambios=(r.get('f10') or {}).get('n_cambios'), tabla=tb,
                 vida_med=(CM.med(r.get('vidas_h1') or r.get('vidas') or []) if (r.get('vidas_h1') or r.get('vidas')) else None))
        if 'f9' in r and r['f9']:
            o.update(p1=CM.med([x for x in r['f9'].get('p1', []) if x >= 0]), c1=CM.med([x for x in r['f9'].get('c1', []) if x >= 0]),
                     lect_div=r['f9'].get('lect_div'))
        OUT.append(o)
        ex = tb['exacta']; ap = tb['aprox_val_inicial']
        log(f"\n[{time.time()-t0:6.1f}s] {etq} s{s} T={Ti}: R0 {o['R0']} (desc {d}, muertes {mu}, muertes_nec {o['muertes_nec']}) vida_med {o['vida_med']} "
            f"cambios {o['n_cambios']} tipos cambiados {len(cam)}")
        for modo, t in (('exacta', ex), ('aprox', ap)):
            log(f"   {modo:6s} mordidas/exposiciones  " + "  ".join(f"{k} {v[0]}/{v[1]}" for k, v in t.items()))
        log(f"   H-BOCA: veneno con SED {ex['SEDxveneno'][0]}/{ex['SEDxveneno'][1]} vs veneno con HAMBRE {ex['HAMBRExveneno'][0]}/{ex['HAMBRExveneno'][1]} · "
            f"sal con HAMBRE {ex['HAMBRExsal'][0]}/{ex['HAMBRExsal'][1]} vs sal con SED {ex['SEDxsal'][0]}/{ex['SEDxsal'][1]}")
    # veredicto de reproduccion, escrito ANTES de ver los numeros (criterio de este diagnostico):
    #  H-BOCA se REPRODUCE en una corrida si tasa(veneno|SED) >= 2x tasa(veneno|HAMBRE) Y tasa(sal|HAMBRE) >= 2x tasa(sal|SED), con >= 10 exposiciones en cada celda
    #  (exacta). Se REPRODUCE en el diagnostico si pasa en D1 (tronco) y en al menos una de D2/D3/D4 (mundo F10).
    def tasa(bv):
        return None if bv[1] < 10 else bv[0] / bv[1]
    rep = {}
    for o in OUT[:4]:
        ex = o['tabla']['exacta']
        a, b, c, e = tasa(ex['SEDxveneno']), tasa(ex['HAMBRExveneno']), tasa(ex['HAMBRExsal']), tasa(ex['SEDxsal'])
        ok = None if None in (a, b, c, e) else bool(a >= 2 * max(b, 1e-9) and c >= 2 * max(e, 1e-9))
        rep[o['etq']] = dict(ok=ok, veneno_SED=a, veneno_HAMBRE=b, sal_HAMBRE=c, sal_SED=e)
        log(f"  H-BOCA {o['etq']}: {'REPRODUCE' if ok else ('n/a (<10 exposiciones)' if ok is None else 'NO')} · "
            f"veneno SED {a if a is None else round(a,3)} vs HAMBRE {b if b is None else round(b,3)} · sal HAMBRE {c if c is None else round(c,3)} vs SED {e if e is None else round(e,3)}")
    hb = bool(rep[OUT[0]['etq']]['ok']) and any(rep[o['etq']]['ok'] for o in OUT[1:4])
    log(f"\nH-BOCA en el diagnostico: {'REPRODUCIDA' if hb else 'NO REPRODUCIDA'} (criterio: D1 y al menos una de D2..D4)")
    r5, r6 = OUT[4]['R0'], OUT[5]['R0']
    log(f"H-MAPA (n = 1, solo direccion): REL con mapa R0 {r5} vs REL_SIN_MAPA {r6} -> {'el mapa NO ayuda (consistente con H-MAPA)' if r5 <= r6 else 'el mapa ayuda en esta semilla (NO consistente con H-MAPA)'}")
    ruta = os.path.join(HUMO, f'diagnostico_boca_mapa_{sel}.json')
    json.dump(dict(bloque='diagnostico_boca_mapa', sello=sel, corridas=OUT, H_BOCA=dict(reproducida=hb, por_corrida=rep),
                   H_MAPA=dict(R0_REL=r5, R0_REL_SIN_MAPA=r6, mapa_no_ayuda=bool(r5 <= r6)),
                   sha_mundo=CM.h16(os.path.join(AQUI, 'mundo_fase10.py')), sha_runner=CM.h16(os.path.join(AQUI, 'corre_mundo_fase10.py')),
                   sha_script=CM.h16(os.path.abspath(__file__)), seg=round(time.time() - t0, 1)),
              open(ruta, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"JSON {ruta} (sha {CM.h16(ruta)}) · {time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
