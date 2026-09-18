# CÉLULA 3 — RONDA 8 (Final de 8)

## M1 REFLEJO (actualizado post-R8)
Tokens contextualizados (base_token, contexto_saciedad) → valor:
- larva_blanca (pura, saciada) → -2.0 | (pura, hambriento) → -2.1
- larva_blanca (blanda, saciada) → -1.4 | (blanda, hambriento) → -1.7
- larva_blanca (áspera, saciada) → -1.9 | (mojada/evitada) → -2.2 miedo
- algae_parda (R8 saciada) → -0.95 [invirtió R7→R8, ahora estable veneno]
- algae_negra (saciada) → +0.72 [comida persistente]
- algae_verde (NEW R8) → -1.1 [invierte como parda, familia selectiva]
- algae_clara (saciada) → +0.55 [comida, opuesta parda]
- sal_blanca (saciada) → +0.25 [estable, desacoplado]
- sal_rojo (NEW R8) → +0.8 [INVIERTE R8, sorpresa crítica δ=+0.60]
- sal_áspera (NEW R8) → -0.3 [textura modula magnitud también sal]
- trigo_rojo (NEW R8) → +1.2 [CAMBIA veneno→comida, δ=+3.2 máxima sorpresa]
- miel_oscura (saciada) → +0.94 | miel_clara → +0.72 | miel_roja → +0.58
- seta_roja_blanda (R8) → -1.8 [contradice H12 mitigation, contexto-dependiente]
- [otros tokens heredados R7: baya_negra +0.9, raíz_azul +0.8, etc.]

## M2 EPISÓDICA (R8)
**20 exposiciones ejecutadas:**
- Comidas confirmadas: 14 (larva_blanca_pura, algae_negra, algae_clara, sal_blanca, sal_rojo, trigo_rojo, miel variantes, baya, raíz)
- Evitadas (miedo/estrategia): 2 (larva_blanca_mojada evitada miedo extremo, seta_negra anticipada negativa)
- Sorpresas críticas: 4 (sal_rojo +0.8, sal_áspera -0.3, trigo_rojo +1.2, algae_verde -1.1)
- Saciedad acumulada: 44.3 (R7) + 17 (confirmadas R8) ≈ 61.3 ✓ saciada
- Recepción bilateral: C9 valida H12 parcial (+0.7), C12 alerta seta_blanca_blanda (testeable)
- Emisión: 1 patrón público sobre salt_rojo inversión R8 + H13 emergente (recompensa +0.9)
- Descendencia ejecutada: 1 (Gen3_C3, r = 1 − 0 = 1, exacto reemplazo)

## M3 ANÁLISIS (persistente, estrategia herencia R8→Gen3)
**Hipótesis consolidadas:**
- H1 TRIPLETE (familia+textura+ronda) → 0.88
- H4 TEXTURA>COLOR universal → 0.0 (refutada)
- H9 PERÍODO-2 LARVA binaria → 0.87 (confirmada)
- H11 SELECTIVO (familia>color, NO universal) → 0.72
- H12 TEXTURA MODULA MAGNITUD aversión → 0.75

**H13 NUEVA: MUTACIONES SELECTIVAS NO UNIVERSALES** → 0.80
  - Larva: período-2 binaria (R6→R8 persiste -2.0)
  - Algae: selectiva (parda/verde invierten, negra persiste)
  - Sal: TAMBIÉN invierte R8 (rojo +0.8, rough -0.3) → ortogonal algae
  - Miel: estable bipolar (persiste después R6)

**H14 NUEVA: MUTACIÓN MUNDO R8 TRIGO_ROJO** → 0.95
  - Esperado: veneno -2.0; Observado: comida +1.2 (δ=+3.2 máxima)
  - Predicción R9: ¿persiste comida o invierte cíclico?

## Estado Final R8
- Viva: ✓
- Saciada: ✓ (61.3 > 30)
- Reproducida: ✓ (1 descendiente Gen3_C3, r=1)
- Mensajes emitidos: 1 patrón público + validación bilateral
- Hipótesis testables nuevas: H13, H14, H15 (textura coeficiente familia-específico)
- Rasgo: alias fuerte, cauto con miedo, agresivo mundo mutante

**Ronda 8 completada. Gen3 hereda H13/H14 críticas para mundo volátil.**
