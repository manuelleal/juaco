# Etapa 5, N1-asimétrico — experto y novato: señal de CONDUCTA (mordida o rechazo visible) y aprendizaje vicario

**Escrito ANTES de modificar el instrumento y ANTES de correr. 16 sep 2026, día 4.**

- **Dirección:** delegó ("decide tú"). Decisión: rediseñar N1 con asimetría de información, sin recalibrar `d_senal` ni
  `f_vicaria` (regla 3).
- **Base:** v10 si se congela; si no, v9. Se anota cuál en el log.

## 0. Qué se sabe y por qué este diseño

1. **N1 simétrico falló** (`datos/N1_20260916_174236`): dos novatos aprenden B en sus primeras ~19 mordidas, antes de
   que las señales del otro lleguen. El contenido de la señal **sí** importa (la barajada empeora).
2. **Problema de fondo, derivado de la política de la boca:** un experto con `W_B = −3` muerde B con p ≈ 0.0003. **Nunca
   emite "asco" sobre B porque nunca lo muerde.** Su conocimiento es visible en que lo **rechaza**, y la señal de N1
   (placer/asco al morder) es ciega a eso. Con esa señal, un experto sólo puede enseñar lo que come.
3. **Rediseño:** la señal es la **conducta visible en cada visita**: al pisar un objeto, el organismo emite
   `(patrón, +)` si lo muerde y `(patrón, −)` si lo rechaza. Es honesta por construcción (es un reflejo de la
   acción, no una decisión). El resultado de la mordida (comida/veneno) **no** se transmite: sólo la conducta.
   - El receptor a distancia ≤ 5 actualiza **su propio** valor del patrón con Rescorla-Wagner vicario, tasa `eta/3`,
     con `R̂ = +1` para mordida y `R̂ = −3` para rechazo, con drenaje, sin comer, sin divisiones. Nunca pesos ni códigos.
   - **Vigilado:** un novato con `W = 0` rechaza el 16% de todo (`pb = 0.84`), así que emite "−" sobre A a veces. Esa
     es la razón por la que la señal de un novato vale poco: se mide, no se filtra.
4. **Herencia del experto:** estado de un progenitor v10 que vivió E1 100.000 pasos (como en la Etapa 4), cuerpo nuevo.
5. **Qué hace la asimetría simbiótica:** en un mundo estable el experto enseña; en un mundo **invertido** el experto
   está **equivocado** y es el novato quien descubre que B es comida. Se miden las dos direcciones.

## 1. Instrumento

`mundo_social.py` gana dos parámetros, apagados por defecto (con n=1 sigue ≡ tronco):
- `estados=[None|estado, ...]`: estado inicial por organismo (herencia completa, con patas).
- `senal='conducta'` (además de `'honesta'` y `'barajada'`): emisión en cada visita, `+` mordió / `−` rechazó.
  `'barajada'` conserva el número de señales de conducta y baraja el signo.

## 2. Diseño (20 semillas; T = 100.000; novato = organismo 0, experto = organismo 1)

| condición | organismo 0 | organismo 1 | señal |
|---|---|---|---|
| NOV-SOLO | novato | — | — |
| PAR-N0 | novato | experto | ninguna |
| **PAR-N1** | novato | experto | **conducta** |
| PAR-BAR | novato | experto | barajada |

Dos mundos: **E1** (estable: el experto tiene razón) y **INV** (`invertir_en=0`: A veneno, B comida desde el primer
paso; el experto hereda el mundo viejo y está equivocado).

**Métricas**
- Novato en E1: `n_crit` = mordidas propias de B hasta `W_B ≤ −2.5` (censurado = total); veneno en Q1; muertes.
- Novato en INV: `t_B_ok` = primer paso con `W_B ≥ +0.5`; veneno (A) en Q1.
- Experto en INV: `t_ext_B` = primer paso con `W_B ≥ 0`.
- Señales recibidas por cada uno, separadas por patrón y signo.

## 3. Criterios y predicciones

**K [instrumento]. Si falla, se para.**
- K1: `mundo_social.run(s, n=1)` ≡ tronco (E1 y E2 × semillas 1..3), con `estados=None`.
- K2: en PAR-N1 (E1), el novato recibe ≥ 5 señales `−` sobre B **antes de su propio criterio** en ≥ 15/20. Si no, el
  canal no llega a tiempo y A1/A2 no se leen (se declara "no evaluable", no "refutado").
- K3: PAR-BAR recibe un número de señales dentro de ±50% de PAR-N1.

**Mundo estable (E1) — el experto enseña:**
- **A1:** mediana de `n_crit` del novato en PAR-N1 ≤ **0.7 ×** la de PAR-N0.
- **A2:** novato de PAR-N1 < novato de PAR-N0, pareado, en ≥ **15/20**.
- **A3:** mediana de PAR-BAR ≥ mediana de PAR-N0.
- **A3b (sin voto):** el experto en E1 no se degrada: `W_B` final ≤ −2.5 en ≥ 18/20 en PAR-N1.

**Mundo invertido (INV) — el experto se equivoca y el novato enseña:**
- **A4 [coste de la confianza]:** el novato de PAR-N1 tarda **más** en aprender que B es comida que el de PAR-N0:
  `t_B_ok` mayor, pareado, en ≥ **13/20**.
- **A5 [simbiosis inversa]:** el experto de PAR-N1 extingue su miedo a B **antes** que el de PAR-N0: `t_ext_B` menor,
  pareado, en ≥ **13/20**.

## 4. ¿Qué lo haría pasar por la razón equivocada?

| riesgo | control |
|---|---|
| ser dos cambia la ecología | PAR-N0 es la línea base |
| cualquier señal acelera | PAR-BAR |
| el experto "enseña" sólo por ocupar los B (los muerde él) | no los muerde (p ≈ 0.0003); además se cuentan mordidas de B del experto |
| el novato llega al criterio sin experiencia propia | `n_crit` cuenta **sus** mordidas de B; llegar con menos **es** el beneficio, y se reporta `W_B` final y veneno Q1 |
| A4/A5 por azar de la inversión | se leen pareados y sólo como par: la lectura simbiótica exige A4 **y** A5 |

## 5. Qué se decide

- **K, A1, A2, A3 sostenidas:** **transmisión social de valor por conducta visible: demostrada.** Vocabulario: *"el
  novato aprende del rechazo visible del experto"*. Nada de lenguaje.
- **Además A4 y A5:** la relación es **simbiótica en el tiempo**: el que sabe enseña y el que descubre corrige. Eso es lo
  que dirección pidió medir.
- **Falla A1 o A3:** se registra y se diagnostica (alcance, tasa, tiempos). Nada se recalibra.
- **A1 y A2 pasan pero A5 no:** hay enseñanza, no simbiosis. Se registra así.

---

## ENMIENDA 1 (17 sep, tarde; ANTES de correr) — base v13 y aprendizaje vicario en las dos vías

- **Base: el tronco v13** (`organismo/organismo_v13.py`, `cc8b16b492d4d324`), no v10 ni v9. `mundo_social.py` pasa a
  replicar v13 línea a línea (división por conflicto de signo, vía lenta lineal, puerta de familiaridad); con las
  perillas apagadas sigue siendo v11/v10/v9. **K1** compara `mundo_social.run(s, n=1)` con `organismo_v13.run(s)`.
- **Aprendizaje vicario:** una señal recibida sobre el patrón `kk` se trata **como una experiencia propia con refuerzo
  R̂** (+1 si mordió, −3 si rechazó), a tasa `f_vicaria` en **las dos vías** (rápida y lenta, cada una con su error, como
  en v13), **sin división** y sin comer. Se declara que la lenta también aprende de lo vicario: es lo que permitiría que
  lo que enseña un experto sobre A y B se **generalice** en el novato a patrones parecidos (no se mide aquí; se anota).
- **Por qué importa v13 aquí:** con v11 el novato no generalizaba (0.60) y el experto olvidaba poco; con v13 ambos
  recuerdan y generalizan. Criterios, predicciones y refutación de A1–A5 **no cambian**.
- El experto hereda **también** `Wps`/`Wns` (su vía lenta), porque son parte de su estado.
