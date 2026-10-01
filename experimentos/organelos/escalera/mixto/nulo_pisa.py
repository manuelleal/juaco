"""nulo_pisa.py — NULO SIMULADO y POTENCIA de la letra de PREREGISTRO_pisa.md (no corre organismos). 1-oct-2026.
Modelo: la mediana por semilla de la latencia de lectores es lognormal; sd del log entre semillas = 0.25 (medido: 0.227 y 0.238 en el brazo
'sen' de las dos series de juntos, n 20 cada una, 36 latencias por semilla; aqui son 32 -> se redondea hacia arriba). rho = correlacion entre
brazos por semilla compartida (0 = sin pareo; 0.3 = algo de pareo). 200 000 series simuladas de n 20 por escenario.
Escenario = razones (mix, pmixbar, pmudo) / pmix verdaderas.
    python experimentos/organelos/escalera/mixto/nulo_pisa.py
"""
import numpy as np
SD = 0.25; N = 20; K = 200000; GP = 14; RZ = 0.85
ESC = [('NULO TOTAL: los 4 brazos iguales', 1.0, 1.0, 1.0),
       ('NULO DE LA VARIANTE: pmix = mix; antipoda x1.3 y mudo x1.8 peores', 1.0, 1.3, 1.8),
       ('NULO DE CONTENIDO: pmix = pmixbar; mix x1.3, mudo x1.8', 1.3, 1.0, 1.8),
       ('efecto en el borde: pmix/mix 0.85; antipoda x1.6; mudo x2.3', 1 / 0.85, 1.6, 2.3),
       ('efecto del humo: pmix/mix 0.77; antipoda x1.6; mudo x2.3', 1 / 0.77, 1.6, 2.3),
       ('efecto grande: pmix/mix 0.65; antipoda x1.6; mudo x2.3', 1 / 0.65, 1.6, 2.3)]
rng = np.random.default_rng(20261001)
print(f"sd log {SD} · n {N} · {K} series por escenario · letra: pares >= {GP}/20 (empate en contra) y mediana de pmix/mix <= {RZ}")
print("escenario | rho | P(FUNCIONA) | P(MODESTO) | P(NO) | P(pares var >= 14) | P(letra del coordinador da MODESTO o mas)")
for nombre, rm, rb, ru in ESC:
    for rho in (0.0, 0.3):
        s = rng.normal(0, SD * np.sqrt(rho), (K, N, 1)); e = rng.normal(0, SD * np.sqrt(1 - rho), (K, N, 4))
        x = s + e + np.log(np.array([1.0, rm, rb, ru]))          # log latencia: pmix, mix, pmixbar, pmudo
        gv = (x[:, :, 0] < x[:, :, 1]).sum(1) >= GP; gc = (x[:, :, 0] < x[:, :, 2]).sum(1) >= GP; gm = (x[:, :, 0] < x[:, :, 3]).sum(1) >= GP
        mg = np.median(x[:, :, 0] - x[:, :, 1], axis=1) <= np.log(RZ)
        F = gv & mg & gc & gm; M = gc & gv & ~F; co = F | (gc & (gv | gm))
        print(f"{nombre} | {rho} | {F.mean():.4f} | {M.mean():.4f} | {1 - F.mean() - M.mean():.4f} | {gv.mean():.4f} | {co.mean():.4f}")
