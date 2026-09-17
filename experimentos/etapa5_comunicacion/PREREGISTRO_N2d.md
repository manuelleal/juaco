# Etapa 5, N2d — cuarto intento: el emisor habla sólo de lo que CONOCE por experiencia (vía rápida), no de lo que extrapola

**Escrito ANTES de modificar el instrumento y ANTES de correr. 17 sep 2026, noche del día 5.** Regla 12.

## 0. Qué dijo N2c (`N2c_s1-20_20260917_183901`) y por qué la predicción de N2c cayó

| criterio | N2b | N2c | umbral |
|---|---|---|---|
| E1 convención | 13/20 | 11/20 | ≥ 15 |
| E2 contraste (`C[s_rech]` / `C[s_mord]`) | −0.42 / +0.36 (2/20) | **−0.35 / +0.20 (3/20)** | ≥ 15 con \\|C\\| ≥ 1 |
| E3 arbitrariedad | 10/20 ✅ | 13/20 ✅ | 5–15 |
| E4 veneno CONV / N0 | 0.77 | **0.92** | ≤ 0.70 |
| E5 barajar destruye | ✅ | ✅ | |

La pureza de la señal (estado = valor, silencio si no sabe; experto de 400k) **no** subió la magnitud. Cláusula de
refutación de N2c cumplida: el problema está en el receptor. Y los números dicen **dónde**: con convención limpia en
13/20 semillas, `M[s_mord]` queda en **−1.85** (M crudo −2.70 / −1.85). El símbolo "positivo" **precede a mordidas de
veneno**. La fuente es el propio experto: conoce 7–8 de 10 venenos incluso a 400k, y los 2–3 restantes no es que no los
haya visto: es que **su código rápido no está consolidado** (3/3 celdas) y la puerta de v13 los lee por la **vía lenta
lineal**, que en el mundo `azar` (valencias arbitrarias) devuelve un valor cualquiera; cuando sale ≥ +0.5 el experto emite
"positivo" sobre un veneno **con confianza**. El novato, sesgado por el símbolo, lo muerde más, `M[s_mord]` se hunde y el
contraste no pasa de ±0.4. Es el canje puerta/capacidad (ERR-22 y la re-verificación de v13) reapareciendo como
**extrapolación confiada del emisor**.

## 1. Qué cambia (una cosa)

`estado_emisor = 'valor_rapido'`: el emisor sólo emite si el patrón le es **familiar a la vía rápida** (≥ 3 celdas de
su código con `|Wp − Wn| > 0.2`, **exactamente la prueba de la puerta de v13**, sin constante nueva) y su estado es el
signo del valor rápido: 1 si `(Wp − Wn)·kc ≥ u_v`, 0 si `≤ −u_v` (`u_v = 0.5`); si no es familiar, **silencio**. Habla de
lo que vivió; calla de lo que sólo extrapola. Todo lo demás igual que N2c (ventaja, sesgo en la decisión, puerta de
valor 1.0, experto de 400k, mundo, semillas, T, condiciones).

## 2. Criterios: los mismos de N2/N2b/N2c, sin tocar un umbral. Réplica en 21–40 si pasa.

## 3. Predicción
- `M[s_mord]` sube por encima de 0 (los "positivos" ya no preceden veneno salvo por errores propios del novato) y el
  contraste alcanza ±1 en **≥ 12/20** (E2). E1 ≥ 15/20 (menos emisiones contradictorias). E4 ≤ 0.7 × N0 (incierto).
- **Refutación:** si E2 sigue < 10/20 con E1 ≥ 13/20, el cuello es cómo aprende `M` el receptor (sólo cuando muerde, y
  deja de morder lo que ya sabe). En ese caso **se cierra la línea N2 por hoy**: se registra "con percepción directa y
  este receptor el significado emerge en signo pero no en magnitud", y se sigue el plan del debate de niveles 5–10
  (`registro/investigacion/DEBATE_y_plan_5a10.md`). Nada se recalibra.
