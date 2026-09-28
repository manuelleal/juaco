"""analiza_potencia_v144.py -- nulo, margen y n de la puerta T-G del examen v4 de v14.4 (TERMO), con datos REALES que YA existian.
No simula un paso. Escrito ANTES del humo y de cualquier serie (regla 2 de forma de v3/v4: toda puerta declara nulo, margen y n).

Datos: los crudos del mundo vivo del examen de v14.3 (serie 43101-43180 y replica 43201-43280; brazos VIVO y CUELLO_MIN):
OFF (v14.2 == v14.3 bit a bit en el mundo vivo), TRONCO_B (el tronco en s + 100000: ley identica) y PLACEBO (inerte que mueve
el generador). Son 160 semillas por brazo en las que tres realizaciones de la MISMA ley comparten la etiqueta de semilla.

T-G (PREREGISTRO_examen_v144.md sec. 4), en el brazo CUELLO_MIN, n = 80, d = r_X - r_OFF pareado (nominal) por semilla:
  G-1  CAND gana: LI_95(d_CAND) = media - 1.645 * sd / sqrt(n) > m          (superioridad de una cola con margen m, abajo)
  G-2  el CONTROL no gana: LI_95(d_CTRL) <= m
  G-3  la pieza actua (telemetria a_no + a_si > 0) en >= 95 % de las corridas del CANDIDATO (validez, no estadistica)
Nulo de G-1 y G-2 a la vez: CAND := TRONCO_B y CTRL := PLACEBO contra el MISMO OFF (dos leyes identicas que comparten OFF).
Se reporta: P(G-1 | nulo), P(G-2 | nulo), P(T-G | nulo) y la potencia de G-1 con desplazamiento exacto delta (d + delta).
MARGEN DE SUPERIORIDAD m (G-1: LI > m; G-2: LI_CTRL <= m). Con m = 0 el nulo NO CENTRADO (la media muestral de d TRONCO_B - OFF en
CUELLO_MIN es +0.89, ruido) pasa G-1 0.107 > 0.05: incumple la regla 15. Se elige el MENOR m entero con P(G-1 | nulo NO centrado)
<= 0.05 en el brazo que decide (CUELLO_MIN); el nulo CENTRADO (media 0 por construccion: ley identica) se reporta al lado.

    python experimentos/tronco_v14_4_examen/analiza_potencia_v144.py       (escribe datos/humo/potencia_examen_v144_<sello>.json)
"""
import hashlib, json, os, sys, time

import numpy as np

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
EX = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3_examen', 'datos')
CRUDOS = {'serie': os.path.join(EX, 'examen_v143_serie_20260924_124413_crudo_TA.json'),
          'replica': os.path.join(EX, 'examen_v143_replica_20260924_131427_crudo_TA.json')}
Z = 1.645; N = 80; B = 20000; SEMILLA_BOOT = 20260928
DELTAS = [0, 2, 4, 5, 6, 8, 10, 15, 20]


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def LI(x):
    return x.mean(axis=-1) - Z * x.std(axis=-1, ddof=1) / np.sqrt(x.shape[-1])


if __name__ == '__main__':
    if sys.argv[1:]:
        raise SystemExit(f'*** este script no toma argumentos: {sys.argv[1:]}')
    out = dict(fuente={k: dict(archivo=os.path.relpath(p, RAIZ).replace(os.sep, '/'), sha=h16(p)) for k, p in CRUDOS.items()},
               z=Z, n=N, B=B, semilla_boot=SEMILLA_BOOT, brazos={})
    rows = []
    for k, p in CRUDOS.items():
        rows += [dict(r, _serie=k) for r in json.load(open(p, encoding='utf-8'))['corridas']]
    g = np.random.default_rng(SEMILLA_BOOT)
    for brazo in ('CUELLO_MIN', 'VIVO'):
        por = {}
        for r in rows:
            if r['brazo'] == brazo:
                por.setdefault((r['_serie'], r['seed']), {})[r['arm']] = r['r']
        claves = sorted(k for k, v in por.items() if all(a in v for a in ('OFF', 'TRONCO_B', 'PLACEBO')))
        off = np.array([por[k]['OFF'] for k in claves], float)
        dB = np.array([por[k]['TRONCO_B'] for k in claves], float) - off
        dP = np.array([por[k]['PLACEBO'] for k in claves], float) - off
        idx = g.integers(0, len(claves), size=(B, N))
        liB, liP = LI(dB[idx]), LI(dP[idx])
        liBc = LI((dB - dB.mean())[idx])   # nulo CENTRADO (ley identica: E[d] = 0 por construccion)
        tabla_m = {str(m): dict(G1_nulo_no_centrado=round(float(np.mean(liB > m)), 4), G1_nulo_centrado=round(float(np.mean(liBc > m)), 4),
                                G2_nulo=round(float(np.mean(liP <= m)), 4)) for m in (0, 1, 2, 3, 4)}
        M = next(m for m in (0, 1, 2, 3, 4) if tabla_m[str(m)]['G1_nulo_no_centrado'] <= 0.05)
        g1 = liB > M; g2 = liP <= M
        pot = {}
        for dl in DELTAS:
            pot[str(dl)] = round(float(np.mean(LI(dB[idx] + dl) > M)), 4)
        # el margen: el menor delta entero con potencia >= 0.80 (el nulo de TRONCO_B, NO centrado, desplazado delta)
        marg = next((dl for dl in range(0, 41) if np.mean(LI(dB[idx] + dl) > M) >= 0.80), None)
        R = dict(n_semillas=len(claves), r_OFF=dict(mediana=float(np.median(off)), p10=float(np.percentile(off, 10)),
                                                     p90=float(np.percentile(off, 90))),
                 sd_d_TRONCO_B=round(float(dB.std(ddof=1)), 3), sd_d_PLACEBO=round(float(dP.std(ddof=1)), 3),
                 media_d_TRONCO_B=round(float(dB.mean()), 3), media_d_PLACEBO=round(float(dP.mean()), 3),
                 tabla_margen_m=tabla_m, m_elegido=M,
                 P_G1_nulo=round(float(g1.mean()), 4), P_G2_nulo=round(float(g2.mean()), 4),
                 P_TG_nulo=round(float((g1 & g2).mean()), 4),
                 potencia_G1=pot, margen_80=marg,
                 potencia_TG_en_margen=round(float(np.mean((LI(dB[idx] + (marg or 0)) > M) & g2)), 4))
        out['brazos'][brazo] = R
        print(f"{brazo:10s} semillas {R['n_semillas']}  r OFF mediana {R['r_OFF']['mediana']} (p10 {R['r_OFF']['p10']}, p90 {R['r_OFF']['p90']})  "
              f"sd(d) TRONCO_B {R['sd_d_TRONCO_B']} PLACEBO {R['sd_d_PLACEBO']}")
        print(f"           media d TRONCO_B {R['media_d_TRONCO_B']} PLACEBO {R['media_d_PLACEBO']}; tabla por margen m: {tabla_m}")
        print(f"           m elegido {M} (menor m con P(G-1 | nulo NO centrado) <= 0.05)")
        print(f"           con m = {M}: P(G-1 | nulo) {R['P_G1_nulo']}  P(G-2 | nulo) {R['P_G2_nulo']}  P(T-G | nulo, sin G-3) {R['P_TG_nulo']}")
        print(f"           potencia de G-1 con d + delta: {pot}")
        print(f"           margen (menor delta con potencia >= 0.80): {marg}; P(G-1 y G-2) en el margen, CTRL nulo: {R['potencia_TG_en_margen']}")
    os.makedirs(os.path.join(RAIZ, 'datos', 'humo'), exist_ok=True)
    f = os.path.join(RAIZ, 'datos', 'humo', f"potencia_examen_v144_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(out, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"datos -> {os.path.relpath(f, RAIZ)}  sha256_16 = {h16(f)}  (script {h16(os.path.abspath(__file__))})")
