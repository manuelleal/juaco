# Etapa 5, N2c — tercer intento: el símbolo refleja lo que el emisor SABE, y calla cuando no sabe

**Escrito ANTES de modificar el instrumento y ANTES de correr. 17 sep 2026, noche del día 5.** Regla 12 del proyecto:
se decide, se preregistra y se corre en la misma sesión; dirección audita después.

## 0. Qué dijo N2b (`N2b_s1-20_20260917_183004`) y qué eslabón falta

| eslabón | N2 | N2b | qué falta |
|---|---|---|---|
| convención en el emisor (E1) | 1/20 | **13/20** (consistencia 0.99; símbolos distintos 14/20) | 2 semillas |
| arbitrariedad (E3) | desempate | **10/20** ✅ | — |
| decodificación (E2, contraste ≥ 1) | 0.00 | **±0.42**, signo correcto, 2/20 | **magnitud** |
| beneficio (E4, ≤ 0.7 × N0) | peor (375) | **246 = 0.77 × N0**, pareado 12/20 | 7 puntos |
| barajar destruye (E5) | vacío | **real**: 334 frente a 246 ✅ | — |

El bucle cierra por los dos lados pero el contraste del receptor se queda en ±0.4 porque `M` se contamina por dos vías
que se ven en los datos: (a) el **estado del emisor es su conducta**, y "rechazo" incluye rechazar comida **por
saciedad** (ya observado en N2: INNATO deja 0/10 comidas conocidas), así que el símbolo de rechazo precede a veces a
comida y `M[s_rech]` sube; (b) el experto **no conoce 2 de 10 venenos** (mediana 8/10 a 200k) y **los muerde** emitiendo
"muerde", así que `M[s_mord]` recibe −3 y se queda en −1.75. El código es correcto en signo y débil en magnitud.

## 1. Qué cambia (dos cosas, derivadas de (a) y (b); todo lo demás igual que N2b)

1. **El estado del emisor es su VALOR, no su conducta** (`estado_emisor = 'valor'`): al pisar un objeto de patrón `kk`,
   si su valor total `v = valor(kk)` cumple `v ≥ u_v` el estado es 1 ("positivo"); si `v ≤ −u_v`, 0 ("negativo");
   si `|v| < u_v` **no emite nada** (silencio: no sabe). `u_v = 0.5` (una comida consolidada vale ≈ +1; un veneno, −3).
   Sigue siendo un reflejo del estado interno —no una decisión estratégica— y quita la saciedad de la señal.
2. **El experto es experto:** progenitor con `T = 400.000` (en vez de 200.000) para que conozca los 10 venenos.

Refuerzo por ventaja, sesgo en la decisión (`gamma = 1.2`), puerta de valor `u_m = 1.0`, `K = 2`, `tau_s`, `tau_m`,
semillas 1–20, T = 200.000, mundo `azar`, condiciones SOLO / N0 / INNATO / CONV / SHUF: **sin cambios**.

## 2. Criterios: **los mismos de N2 y N2b, sin tocar un umbral**
K1, K2, E1 (≥ 15/20), E2 (contraste ≤ −1.0 / ≥ +0.3 en ≥ 15/20), E3 (5–15), E4 (≤ 0.7 × N0 y pareado ≥ 14/20),
E5 (SHUF sin contraste y sin beneficio). Réplica en 21–40 si pasa.

## 3. Predicción
- **E1 ≥ 15/20** (ya está en 13 y el silencio quita emisiones contradictorias). **E3 ≈ 10/20.**
- **E2: la magnitud sube;** apuesto a `C[s_rech]` mediana ≤ −1.0 y **12–17/20** cumpliendo. Es el criterio más incierto.
- **E4: veneno CONV ≤ 0.7 × N0** (N2b estaba en 0.77 con el código a medias). **E5** se sostiene.
- **Refutación:** si E2 < 10/20 o E4 no baja de 0.77 × N0, la magnitud del significado **no** depende de la pureza de la
  señal, y el problema es otro (probablemente que `M` aprende sólo cuando el receptor muerde, y deja de morder lo que ya
  sabe). Entonces el cuarto diseño cambia cómo aprende `M` (por ejemplo, de su propio valor final del patrón, no sólo de
  la mordida), preregistrado aparte. **Nada se recalibra.**

## 4. Qué se decide
- E1–E5 y réplica: N2 cerrado ("emerge un código de dos símbolos, arbitrario, que transmite valor y muere al barajarlo").
- Falla: se registra el eslabón y se pasa al cuarto diseño en la misma sesión.
