# gen1 / llm_1 — reparto del crédito RW por compromiso opuesto

**Operador:** LLM (Claude Fable 5.1). **Clase asignada:** consolidación de valor sin almacén nuevo. **Padre:** `organismo_v10m.py`.
**Escrito antes de evaluar** (16 sep 2026). Diff: 10 líneas (1 nueva en el docstring, 1 nueva de código, 4 tocadas × 2).

## Mecanismo (qué cambia y dónde)

En el padre, la regla RW reparte el error de un patrón **por igual** entre las K=3 celdas de su código
(`Wp += eta*dlt*kc`, líneas 97–98). Con solapamiento parcial de códigos eso es la vía de valor del olvido: cada
celda de D compartida con B recibe el incremento completo `(1+s)/3` de Wp (s = celdas compartidas), y B lo lee al
volver: s=1 → W_B ≈ −2.33, s=2 → W_B ≈ −1.0; A↔C con signo contrario: s'=1 → W_A ≈ −0.1.

Cambio: el incremento se **pondera por celda** con `w_c = 1/(1+20·opp_c)`, donde `opp_c` es el peso del signo
*contrario* que la celda ya tiene (`Wn[c]` si se aprende Wp, `Wp[c]` si se aprende Wn), renormalizado a `Σ w_c = K`.

- Línea nueva tras `_ix=kc>0` (era la 91): `_op=(Wn if dlt>0 else Wp)[_ix]; _w=1/(1+20.*_op); _wc=kc*1.; _wc[_ix]=K*_w/_w.sum()`.
- Líneas 97–98 (actualización RW): `kc` → `_wc`.
- Líneas 92–93 (instrumentación del techo `_trunca`): mismo `_wc`, para que `n_techo`/`t_techo` midan el incremento real.

Propiedades derivadas a mano (no medidas):
1. **La tasa a nivel de patrón se conserva exactamente** (`Σ w = K`): para un código fijo, la lectura `(Wp−Wn)@kc`
   evoluciona igual que en el padre; cambia sólo la *composición* por celda. No frena lo nuevo (a diferencia de K2).
2. **Con celdas igualmente comprometidas los pesos valen exactamente 1.0** (`K*w/(w+w+w)` = 1.0 en coma flotante):
   E1 (códigos disjuntos, opp = 0), la inversión de E2 (las 3 celdas de A con el mismo Wp), E2L y CTRL (3 celdas
   idénticas) son **bit-idénticos al padre** hasta la primera división que haga diferir los códigos.
3. Sólo actúa con **solapamiento parcial**: E2J (D∩B=1), E2K (D∩B=2), C∩D y el bloque M. Ahí desvía el crédito a
   las celdas libres: con s=2 y κ=20 la deriva de B baja de 2.0 a ≈0.26 (W_B ≈ −2.74); con s'=1 A queda ≈ 0.8.
4. Menos diálogo cruzado entre C y D durante la ausencia → menos error sostenido → **menos divisiones en la
   ausencia** (padre v10: mediana 4) → también menos toma de código por hijas (vía estructural), sin tocar la división.
5. Límite: si las 3 celdas del código están comprometidas (s=3, o D∩(B∪C)=3), el reparto vuelve a ser uniforme y el
   individuo se comporta como el padre (esas semillas siguen fallando).

## Hipótesis (una línea)

El olvido de valor en celdas compartidas se evita desviando el crédito RW hacia las celdas del código sin compromiso
de signo contrario, conservando la tasa total; retiene sin frenar el aprendizaje nuevo y sin almacén.

## Predicciones (semillas 1–10)

- **R = 0.7** (7/10; intervalo que aceptaría como "cumplió": 0.6–0.9). Padre v10 ≈ 0.5.
  W_B(100k) mediana de ≈ −2.1 a ≈ −2.6; W_A(100k) mediana ≥ 0.85. Fallos restantes: semillas con código de D
  totalmente comprometido (s=3) o toma estructural.
- **Guarda H3:** W_C(100k) ≤ −2.5 y W_D(100k) ≥ 0.85 en 10/10 (misma velocidad de patrón que el padre). Riesgo
  declarado: si D comparte 2 celdas ya cargadas (Wn ≈ 1 y 1.5), la celda libre toca el techo 3.0 y D se queda en
  ≈ 0.76–0.83 hasta que la fuga lenta a las celdas comprometidas lo lleve a ≥ 0.85 (≈ 50–100 mordidas de D). Si H3
  cae a 8/10 será por esto; `n_techo > 0` en el bloque M lo delataría.
- **E1:** bit-idéntico al padre (W, mordidas, muertes) → S igual. Si E1 no es idéntico, el instrumento está roto.
- **E2:** W_A → −3 y W_B → +1 con el mismo `t` a criterio que el padre (±10 %); mordidas B Q4 ≥ 50 en 10/10.
- **E2L:** 3 divisiones (igual que v10) → E igual; solap→0 en 10/10.
- **E2J/E2K:** divisiones ≤ las del padre (posiblemente 0), W_D ≥ 0.85/0.8 y W_B ≤ −2.7/−2.4 en 10/10.
- **Bloque M:** divisiones en la ausencia ≤ 2 (mediana), celdas ≤ 40.
- **Retenidas 11–20:** R ≥ 0.6 (el mecanismo no tiene nada que sobreajustar: 1 constante, κ=20, elegida a mano por
  el margen de A↔C con s'=1 frente al techo de la celda libre de D).

## Estado nuevo

**Ninguno.** `_op`, `_w`, `_wc` son temporales de la mordida, calculados de `Wp`, `Wn`, `kc`. Cero contadores, cero
copias de W, cero pares (patrón, R). Un parámetro implícito (κ = 20), literal en el cuerpo de `run()`.

## Qué lo haría pasar por la razón equivocada

1. **Retener por no aprender D:** la celda libre de D satura en el techo y D no llega a 0.85 → lo atrapa H3; auditar
   `n_techo`/`t_techo` en M (deberían ser 0 o casi) y `primer` de D.
2. **Retener sólo por menos divisiones** (vía estructural) y no por valor: se distingue con la sonda de "W_viejo"
   (valor sobre el código de 50k); mi mecanismo predice que **W_viejo(B) mejora** (≈ −2.6 frente a −2.3 del padre),
   no sólo el solapamiento de código.
3. **Aprendizaje más lento en general** (si `Σ w ≠ K` por un error mío): se vería como E2 más lento o mordidas B Q4
   < 50; la identidad de E1 con el padre y el `t` a criterio de E2 son el control.
4. **Suerte de semillas:** R en 11–20 < R_padre − 0.1 lo marca como sobreajustado; no espero ese resultado.

## Humo (única corrida, semilla 1)

`run(1,T=20000)`: mismas claves que el padre; W = {A 1.0, B −2.76}, 0 divisiones, 34 muertes, `n_techo` 0,
`err_max` 0.443 (coincide con el pico de err ≈ 0.44 derivado para aprendizaje sin conflicto, < θ). 0.8 s.
`run(1,T=30000,fases={10k: C,D; 20k: A,B})`: sondas presentes. En 10k C y D comparten las 3 celdas de código
(caso uniforme: separan por 2 divisiones, t=10213 y 12352); B comparte la celda 25 con ambos y deriva sólo +0.05
(−2.62 → −2.57); A no se mueve (0.988); C −2.44 y D +0.96 en 20k; `n_techo` 0; 32 celdas. 1.1 s.
