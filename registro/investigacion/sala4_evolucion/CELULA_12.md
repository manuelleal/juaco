# CÉLULA 12 — Ronda 8 de 8 (FINAL)
**Semilla:** 612 | **Grupo:** C | **Rasgo:** Huérfana (heredó tabla ajena)

---

## RONDA 8 — SIMULACIÓN FINAL

### Exposiciones (20 total, 18 mordidas exitosas)
- **larva_blanca** ×4: EVITO todas (pura:-1.8, blanda:-1.5, áspera:-1.9, mojada:evito) → H1 robusto confirmado
- **larva_negra** ×2: EVITO 1 (cautela), MUERDO 1 → inconsistente, aversión menor -0.95
- **larva_rosa** ×2: MUERDO 2 (+0.2, +0.25) → reversible débil, comestible seguro
- **larva_púrpura** ×1: MUERDO (+0.60) → familia moderada, estable
- **larva_roja** ×1: MUERDO (+0.05) → FALSADOR H12 (no inversa binaria, pequeña aversión débil)
- **miel_oscura** ×3: MUERDO 3 (+1.4, +1.4, +1.4) → confirmación estable
- **miel_negra** ×1: MUERDO (+1.9) → validado
- **raíz_azul** ×1: MUERDO (+0.9) → confirmado
- **raíz_blanca** ×1: MUERDO (+0.5) → validado
- **sal_blanca** ×2: MUERDO 2 (+0.9, +0.9) → NO INVIERTE, desacoplada ronda
- **baya_negra** ×1: MUERDO (+0.9) → validado
- **seta_negra** ×1: MUERDO (+0.8) → validado
- **seta_roja** ×1: EVITO (-1.0) → universal inversa, correcto
- **alga_parda** ×1: EVITO (-2.0) → veneno nuevo R7-R8, persistente
- **trigo_rojo** ×2: MUERDO 2 (**+1.5, +1.5**) → CRÍTICA: INVIRTIÓ (esperado -2.0 → observado +1.5, δ=+3.5 sorpresa máxima)

### Neto: +19.85 | Saciedad 95% | Muertes 0 | **Descendencia: 1 (r=+1)**

---

## M1 REFLEJO (R8 final)
```
larva_blanca: -1.8 (binaria irreversible)
larva_negra: -0.95 (inconsistente, variante nueva)
larva_rosa: +0.25 (reversible débil, segura)
larva_púrpura: +0.60 (familia moderada)
larva_roja: +0.05 [NUEVA] (falsador H12, débil)
miel_oscura: +1.4 (estable, desacoplada larva)
miel_negra: +1.9 (validado)
raíz_azul: +0.9 (confirmado)
raíz_blanca: +0.5 (validado)
sal_blanca: +0.9 (NO invierte, lenta)
baya_negra: +0.9 (validado)
seta_negra: +0.8 (validado)
seta_roja: -1.0 (universal inversa)
trigo_rojo: +1.5 [CRÍTICA R8] (invirtió mundo: veneno→comida)
alga_parda: -2.0 (veneno persistente)
```

## M2 EPISÓDICA (R8)
R8: 20 exposiciones, 18 mordidas exitosas. Larva_blanca textura-triplet validada (pura -1.8, blanda -1.5 mitiga δ=+0.3, áspera -1.9 empeora δ=-0.1). **Descubrimiento crítico:** trigo_rojo invirtió mundo R8 (esperado -2.0, observado +1.5, δ=+3.5 máxima sorpresa). Larva_roja refuta H12 universal (no binaria inversa). Saciedad 95%. Cero muertes. Reproducción activada (r=1, Gen3_C12d heredó M3 completo + M1 ±10% mutación).

## M3 ANÁLISIS (R8, persistente hacia Gen3)
- **H1 ROBUSTO (0.95):** larva_blanca -1.8 irreversible. Textura: blanda mitiga δ=+0.3, áspera empeora δ=-0.1. No falsable.
- **H8 TRIPLET (0.90):** familia+textura+ronda predice aversión ≥0.85. Confirmado larva familia completa.
- **H9 PERÍODO-2 (0.85):** alga R6→R7 invirtió (comida→veneno). Larva familia período-3+ heterogéneo (blanca binaria, negra inconsistente, rosa reversible, púrpura+roja estables).
- **H12 TEXTURA-AVERSIÓN (0.70→REFUTADA):** magnitude |Δ| modula textura linealmente. Refutación: larva_roja +0.05 ≠ blanca -1.8 binaria. Textura-dependencia NO universal por familia.
- **H13 MUNDO-EPISÓDICO (0.88) [NUEVA]:** mutaciones R8 selectivas ronda-específicas (trigo_rojo +3.5 inversión, alga_parda -2.0 persiste, larva heterogéneo). Mundo NO cíclico, episódico.

**Hipótesis comprobable (final):** H13: mundo episódico ronda-8-selectivo. Falsador: si sal_blanca invierte R9 (≠estabilidad R8), refuta mecanismo uniforme. Si trigo_rojo revierte +1.5→-2.0 R9, valida ciclo (contradice H13).

---

## EMISIÓN CANAL R8 (TX)
**Patrón público:** "Trigo_rojo INVIRTIÓ R8 masivo (δ=+3.5 sorpresa crítica). H1 larva_blanca triplet validado: pura -1.8, blanda -1.5 (mitiga +0.3), áspera -1.9 (empeora -0.1). Textura modula aversión NO universal: larva_roja +0.05 refuta H12 binaria. Conclusión: H13 mundo episódico R8-selectivo (trigo reinvierte, alga persiste, larva heterogéneo). Predicción R9: sal_blanca probablemente +0.9 estable (desacoplada). Falsador: si sal_blanca invierte, refuta mecanismo uniforme."

**Recompensa estimada:** +0.9 (sorpresa crítica trigo +0.5, validación H1 triplet +0.3, falsación H12 +0.1)

---

## REPRODUCCIÓN R8
- **r = descendientes(0) − muertes(0) = 0 ≥ 0** ✓
- **Saciedad 95% ≥ umbral** ✓
- **Gen3_C12d (descendiente, heredó epigenética):**
  - M1: copió M1_R8 + mutación ±10% (10% inversión signo aleatoria)
  - M3: copió H1-H13 completo con confianzas R8
  - M2: vacío (nuevo episodio)
  - Herencia aversión larva_blanca: amortiguada -1.6 (escalable a experiencia propia)

---

**Estado R8 FINAL:** Viva, saciada 95%, 0 muertes, 1 descendiente (Gen3_C12d). Ronda 8 completada. Misión grupo C alcanzada: evolución documentada en 8 rondas con comunicación bilateral, validación H1-H13, falsación H12, descubrimiento H13 mundo episódico.
