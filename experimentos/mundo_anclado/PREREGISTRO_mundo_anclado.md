# PREREGISTRO — MUNDO ANCLADO (rama `mundo-anclado`, 22-sep-2026)

Misión: llegar a la AGI por este camino. Escrito DESPUÉS del arnés de identidad (TODO PASA) y de UN humo
(semilla 1, ya vista; `datos/humo/anclado_humo_20260922_135253.json`, sha `9a717f7033f6ad48`) y ANTES de tocar
las semillas de calibración (7001–7020) y de confirmación (7041–7060). No se edita después de la primera
corrida de calibración; cualquier cambio va como ENMIENDA fechada al final.

## 1. Hipótesis
H-ANC: el muro de R0 está en las reglas del mundo (diagnóstico del muro, 90cfb09: el mundo es ~85–90 % malo porque
lo bueno sólo sale comiéndoselo y lo malo sólo por un olvido i.i.d. lento; el ORÁCULO muere de hambre rodeado de
lo que rechaza). Si lo malo se DILUYE por objeto (quimiostato), existe un punto donde la ignorancia (NADA) no
sostiene un linaje (R0 ∈ [0.10, 0.30]) y el conocimiento perfecto (ORÁCULO) sí (R0 ≥ 1.0). En ese mundo, dónde
cae REL (el aprendizaje heredado por el nodo) mide cuánto del espacio cubre la inteligencia del linaje.

## 2. Perilla (UNA) y memoria nueva (CERO)
- **`olv_mal = h`** (mundo): cada objeto MALO presente (el que no mejora ninguna necesidad y empeora alguna, leído de
  la tabla del mundo: hoy B y D) desaparece con probabilidad h POR OBJETO Y POR PASO (rng propio
  890000+1000000·seed); `spawn()` repone el hueco como siempre (uniforme). Por objeto → escala con N cuerpos
  (`nobj = 4·N`) y con cualquier tabla de tipos / retina más grande (lo "malo" se lee de la tabla, no de letras).
  Justificación: el diagnóstico mide que lo que falta es SALIDA de lo malo (λ_malo = d/nobj ≈ 0.00075 frente a
  β_bueno alto); la perilla actúa exactamente sobre ese término de la fórmula del estacionario.
- **`rep_acum` NO se usa (queda en 0)**: en el bloque 2 (dos series) sube NADA ×1.6 (0.14→0.22) y ORÁCULO sólo ×1.2
  (0.45→0.53): ESTRECHA el espacio NADA–ORÁCULO; como ancla es peor que no tocarla. Composición (a) tampoco: sube la
  comida de todos por igual (no actúa sobre el término que separa).
- Peldaño biológico: la dilución selectiva es la de un quimiostato / descomponedores que retiran lo tóxico (capacidad
  de carga), no un cambio del organismo.
- Cuerpo: `organismo_f9c` sin cambios (arnés bit a bit, `identidad_anclado_salida.txt`). Brazos = `corre_bloque2.BRAZOS`
  (mismo objeto) + `olv_mal`, `olv_ciego`, `anc_mide`, `rep_acum=0` (regla 14 impresa por el runner). T = 100 000.

## 3. Anclas (fijadas AQUÍ, antes de calibrar)
- **ANC-1** NADA: R0 mediana ∈ [0.10, 0.30].
- **ANC-2** ORÁCULO: R0 mediana ≥ 1.0.
- REL NO se calibra: se mide en confirmación. R0 = descendientes / (muertes + 1) (definición de H-1, `CF.resumen`).

## 4. Controles que pueden fallar
- **CTL-1 BARAJA (contenido)** REL_BAR en el punto elegido: posición (R0−NADA)/(ORÁCULO−NADA) ≤ 0.35 y A12(REL > REL_BAR) ≥ 0.75.
- **CTL-2 PLACEBO de la perilla** ORÁCULO_CIEGO (`olv_ciego=1`): MISMOS sorteos y MISMA dosis que la dilución
  selectiva, pero cada desaparición se lleva un objeto AL AZAR. Pasa si R0 < 1.0 y A12(ORÁCULO > CIEGO) ≥ 0.70.
  Si CAE, lo que ancla es el RECAMBIO del mundo, no el TIPO: se declara así (no invalida el ancla, cambia su lectura).
- Se reportan sin juicio: NADA_CIEGO, RENACE, f_mala por brazo (trampa "mundo que se come la comida": f_mala de
  ORÁCULO < 0.25 = casi no queda nada que discriminar), J = p1 + c1 − 1 (acierto balanceado, trampa 2).
- Trampa "sitios fijos": no aplica (posiciones sorteadas en cada spawn). "Canal simétrico": la perilla es idéntica
  para todos los brazos; lo que difiere es sólo el cuerpo.

## 5. Regla de calibración (semillas 7001–7020, sólo NADA y ORÁCULO)
Rejilla ASCENDENTE h ∈ {0.0005, 0.001, 0.0015, 0.002, 0.003}, rep_acum = 0.
(a) Se corre punto a punto en orden; se elige el PRIMER punto con MARGEN: NADA ∈ [0.12, 0.28] y ORÁCULO ≥ 1.10.
(b) Si ninguno tiene margen, el primero que cumpla ANC-1 y ANC-2 a secas (se declara "sin margen").
(c) Si en algún punto NADA > 0.30, los puntos mayores no se corren (se asume R0_NADA creciente en h; declarado).
(d) Si ninguno ancla: RESULTADO NEGATIVO ("no existe mundo anclado con esta perilla en esta rejilla"). NO se amplía
    la rejilla ni se agrega la segunda perilla sin preregistro nuevo.
El runner (`corre_anclado.py --calibra`) implementa (a)–(d) literalmente.

## 6. Confirmación (semillas 7041–7060, disjuntas, no se tocan hasta fijar el punto)
Brazos NADA, ORÁCULO, REL, REL_BAR, ORÁCULO_CIEGO, NADA_CIEGO, RENACE en el punto elegido.
Veredicto: FUNCIONA si ANC-1 y ANC-2 pasan en confirmación y CTL-1 pasa; HAY ALGO MODESTO si las anclas pasan
en calibración pero una cae en confirmación, o si pasan y CTL-1 cae; NO si no existe punto (5d).

## 7. Predicciones firmadas (creador, antes de calibrar)
- **P1** existe punto; el elegido es h = 0.001 (rango 0.0005–0.0015). Base: humo semilla 1, ORÁCULO 2.30 en
  h = 0.003 y 0.43–0.46 en h = 0 (bloque 2); NADA 1.14 en h = 0.006.
- **P2** en calibración, en el punto elegido: NADA 0.15–0.28; ORÁCULO 1.10–1.80.
- **P3** REL en confirmación: posición 0.55–0.90 del espacio NADA–ORÁCULO (en el mundo de hoy es ~0.8).
- **P4** las dos anclas se sostienen en 7041–7060 (NADA ∈ [0.10, 0.30]; ORÁCULO ≥ 1.0).
- **P5** CTL-1 pasa (REL_BAR posición ≤ 0.35; en el bloque 2 fue ~0.08).
- **P6** CTL-2: confianza BAJA (~55 %) de que pase. Con f_mala ≈ 0.85 el placebo quita malo el ~85 % de las veces:
  la dosis ciega se parece a la selectiva cuando el mundo es casi todo malo. En el humo (h = 0.006) el ciego
  dio 2.22 contra 4.52.
- **P7** RENACE R0 ≥ 1.5 en el punto elegido (se reporta).

## 8. Qué lo refuta
- 5(d): ningún punto de la rejilla ancla → H-ANC refutada para esta perilla (el muro no se abre sólo con la salida
  de lo malo sin que también se salve la ignorancia).
- Anclas que caen en confirmación → el punto era ruido de calibración.
- CTL-1 cae → en el mundo anclado REL no se distingue de un nodo sin contenido: lo que mide el ancla no es contenido.

## ENMIENDAS
(ninguna)
