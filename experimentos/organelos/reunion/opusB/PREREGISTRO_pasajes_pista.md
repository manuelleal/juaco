# PREREGISTRO (EXPLORATORIO) — PASAJES SERIADOS en la pista de la carrera (Opus B, reunión 28-sep-2026, escrito 18:52, cadenas ya lanzadas 18:49, SIN mirar sus números)

Misión: llegar a la AGI por este camino. Principio del director: que la evolución construya el órgano, sólo con selección natural.
**Todo es EXPLORATORIO.** No hay letra confirmatoria; decide sólo si se escribe el esqueleto del intento #7 del muro.

## Hipótesis
Si lo que quedó vivo al final de un pasaje corto siembra a los fundadores del siguiente (genoma = g del termostato + 15 genes del cerebro,
por cuerpo, heredables padre→hijo con la mutación de siempre), la refundación deja de volver a la zona letal y, pasaje tras pasaje, bajan
los fundadores por linaje y sube el R0 real hacia O1.

## Mecanismo y memoria nueva
- Carro `V143_PAS` (`construye_pas.py`, por anclas desde `termo_banco/carros/V143_EVO_BAJO.py` sha 3187b373654e119f): EVO_BAJO + 15 floats
  por cuerpo (cerebro) + fundador de SIEMBRA. Memoria nueva: 15 floats por cuerpo (genes, no aprendizaje). PASAJE 0 == EVO_BAJO bit a bit.
- Base: V143_EVO_BAJO (= V143 con g gen por cuerpo). Por qué no TERMO′ directo: TERMO′ == TERMO en la pista quieta, y TERMO == EVO con g
  fijo 0.40 en la física (arnés de termo_banco); el gen g hace falta para que la selección lo mueva. TERMO va como referencia por pasaje.
- Transferencia (`corre_pas.siembra`): los (g, cerebro) de los cuerpos VIVOS muestreados cada 1000 pasos en los últimos 5000 pasos, 9 linajes
  (≈45 entradas; el que vive más aparece más: selección por viabilidad leída, no juez). Firma `siembra(vivos_b, T, vent)`: no ve R0, hijos
  ni cruza.
- Límite del instrumento (declarado, Fable 18:42 punto 1): dentro del pasaje, el refundador sale de la siembra del pasaje ANTERIOR, no del
  último padre del pasaje en curso.

## Brazos, T, semillas
- `pas` (CANDIDATO: transfiere, cerebro muta p 0.05 σ 0.15), `ctl` (CONTROL: mismos pasajes y semillas, fundadores siempre de la inicial:
  g ~ U[−0.1, 0.1], cerebro G0 mutado), `pasg` (transfiere, cerebro fijo G0: sólo g), `termo` (V143_TERMO), `o1` (O1). Opcional `eco`.
- T 25 000 por pasaje, 10 pasajes. Semilla de pista del pasaje p de la cadena c: 58300 + 10c + p (c 1..8; práctica c 0 = 58300–58309;
  583xx libre al grep del 28-sep 18:47 en py/md/txt de experimentos y registro).
- **Advertencia de medida:** a T 25k `cruza_real` exige 0 fundadores en [10k, 25k), una ventana de 15k (a T 100k son 90k): es más FÁCIL que la
  letra del muro. Los números por pasaje sólo se comparan contra TERMO y O1 en la MISMA semilla y T, nunca contra 0.93 / 0.941 de 100k.

## Predicciones (firmadas 18:52, antes de ver cualquier pasaje ≥ 0 de c1–c4)
| # | predicción | rango | p |
|---|---|---|---|
| Q1 | pasaje 0: pas == ctl bit a bit en las 4 cadenas | | 0.99 |
| Q2 | g medio de la siembra de `pas` en p9 (mediana de cadenas) | [0.08, 0.30] | 0.60 |
| Q3 | g medio de la siembra de `ctl` en p9 | [−0.02, 0.07] | 0.80 |
| Q4 | fundadores por linaje (media de 9, mediana de cadenas), `pas` p5–p9 < `ctl` p5–p9 | ≤ 0.8 × ctl | 0.35 |
| Q5 | R0 real (mediana de 9) `pas` > `ctl` en ≥ 60 % de los pares (cadena, pasaje ≥ 3) | | 0.50 |
| Q6 | `pas` llega a R0 real ≥ 0.90 (mediana de cadenas) en algún pasaje ≥ 5 | | 0.12 |
| Q7 | `pasg` (sólo g) no se separa de `ctl` en fundadores (± 20 %) | | 0.65 |
| Q8 | TERMO (T 25k): mediana de R0 real por pasaje en [0.75, 0.97]; O1 en [0.85, 0.99] | | 0.70 |
| Q9 | SEÑAL CLARA (fundadores de `pas` bajan pasaje a pasaje en ≥ 3/4 cadenas Y R0 ≥ 0.90) | | 0.08 |

Por qué predigo poco: el fundador nace con `_adS` vacío y casi siempre muere de veneno o sal antes de que `g` decida (termo_banco §8 bis);
el cerebro sí actúa desde el primer paso, pero en 25k pasos hay pocas generaciones y en eco_a_carrera el genoma SEL de ECO no ayudó en la pista.

## Qué lo refuta
- Fundadores por linaje de `pas` no bajan frente a `ctl` en los pasajes ≥ 5 (Q4 falla) y el R0 no se separa (Q5 falla).
- Control que puede fallar: si `ctl` mejora igual que `pas` pasaje a pasaje, lo que cambia es la semilla de pista, no la herencia.

## Si hay señal clara
Esqueleto confirmatorio `PREREGISTRO_muro7_esqueleto.md` con la letra del muro SIN cambios (T 100k, `cruza_real`, P1 ≥ 15/20).
