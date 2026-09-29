# PREREGISTRO (esqueleto, EXPLORATORIO) — 50 GENES: ¿más genes que la selección pueda mover suben el techo? (Opus G, 28-sep-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles
y réplicas); el método manda sobre el cómo. Principio del director: que la evolución construya el órgano, no nosotros, sólo con selección natural.

**Estado:** §1–§6 escritas ANTES de ver el humo y la exploración (19:25 del 28-sep). Lo de hoy es EXPLORATORIO (10 semillas, T 5e5,
3 procesos sin Pool); no decide. Si hay señal, la nube corre §7 con semillas nuevas.

## 1. Pregunta
Encargo del director: «el mismo experimento pero con 50 genes, una cosa alta». Base: ECO con hijos ingenuos (`eco_sel_ing`, FUNCIONA ×2),
vivero permanente, medida K, K_nac, fund_2a. Hoy mutan 15 genes del cerebro (ING_SEL_C). **¿Con 50 genes heredables la selección llega a
más K y menos fundadores repuestos? ¿O 50 genes = más carga mutacional y peor?**

## 2. Los 50 genes (memoria nueva: cero; mecanismo nuevo: cero — sólo constantes que ya existían pasan a ser por cuerpo)
- 18 de `motor_eco.GENES`: los 15 del cerebro + dote, rep_umbral, rep_X (historia de vida).
- 32 nuevos: constantes LITERALES que el gemelo usa de verdad (`frio/motor_frio_rapido.py`):
  marcha 14 (gan_patron 1.2, gan_lado 1.5, gan_aqui 1.0, ruido0 .15, ruido_h .5, umbral_m0 .8, umbral_m1 .8, ruido_motor .3, umbral_mov .5,
  traza .7, premio_acerca .2, clip_l 1.5, h_motor 2, x_eta_l 1) · arranque 3 (wl0_lo .1, wl0_hi .4, kw0_hi 1) · boca 5 (sesgo_boca .5,
  temp_boca .3, umbral_fam .2, puerta_pat 5, pat_min 1) · valor por necesidad 5 (R_bueno_E/A 1, R_malo_E/A 3, peso_sed 1) · aprendizaje 2
  (clip_e 3, x_aversion_s 1) · división 3 (decae_kw .05, clip_kw 5, umbral_div .2).
- Splits y pesos por necesidad, justificados: x_eta_l y x_aversion_s son MULTIPLICADORES (1.0 = la cuenta original aunque eta o aversion
  muten; la primera versión como genes sueltos rompió la identidad (A) de ING_SEL_C: error mío, corregido antes de cualquier número);
  umbral_m0/m1 y R por necesidad separan una constante que hoy se usa en dos neuronas o dos necesidades.
- **Excluidos (declarado):** costo, costo_a y el tope de reserva 1.5 (bajarlos sube K sin cerebro: almuerzo gratis, trampa 3); el alcance
  de la vista (ver no cuesta: sólo podría bajar); K = 3, NKMAX, n_nec (dimensiones compiladas); olvido y reposición (del mundo).
- Rango = el de ECO: [max(piso, G0/4), min(techo, 4·G0)]; mutación log-normal σ 0.15, p 0.05 por gen (la de ECO).

## 3. Brazos (todos: ECO w90, FABRICA_ECO, vivero permanente, banco 200, 8 sombras; mismas semillas)
| brazo | mutan | herencia | papel |
|---|---|---|---|
| ING_F1 | nada | — | base sin selección |
| ING_SEL_C | 15 | padre | **referencia** (hoy) |
| ING_SEL_25 | 15 + 10 del cerebro (boca y valor) | padre | dosis intermedia |
| ING_SEL_47 | 50 sin historia de vida | padre | separa cerebro de historia de vida |
| ING_SEL_50 | 50 | padre | hipótesis |
| ING_AZA_50 | 50 | azar (sin herencia) | control que puede fallar |

## 4. Instrumento y anclas
`construye_g50.py` construye por anclas (cuenta exacta por ancla): `motor_eco50.py` ← `juaco_eco/motor_eco.py` (bca3033878b59622);
`motor_g50.py` ← `frio/motor_frio_rapido.py` (ff9d890a5cce9dec); `nucleo_g50.py` ← `eco_sel_ing/nucleo_eco_sel_ing.py` (c2189f9d22b72386).
`muta` gasta 2·18 números si ningún gen nuevo es mutable → los brazos de la base quedan bit a bit. kbar se IMPORTA de `corre_eco_sel_ing.py`.
Arnés `identidad_g50.py` (salida `identidad_g50_salida.txt`): (K) anclas; (M) muta; (A) ING_F1/SEL_C/AZA_C == base bit a bit;
(B) p_mut 0 == ING_F1 en los 4 brazos nuevos; (Z) controles; (D) determinismo; (U) cada gen nuevo cambia la física.
**Guardia:** tope computacional 600 cuerpos (base 3000; la base no pasa de ~120). bloqueados > 0 = la historia de vida se disparó →
esa corrida NO EVALUABLE, se cuenta y se dice.

## 5. Medidas y lectura exploratoria (pareado por semilla contra ING_SEL_C)
K (media de vivos en [T/2, T]), K_nac, fund_2a; n_nac y max_vivos (guardia); genes de los vivos en T (log g/G0).
**Lectura de hoy:** HAY SEÑAL si SEL_50 (o SEL_47) supera a SEL_C en K y K_nac en ≥ 8/10 semillas evaluables con mediana de ΔK ≥ +1.5
**y** supera a AZA_50 en ≥ 8/10. NO HAY SEÑAL si gana ≤ 5/10. NO SE LEE si > 2 corridas del brazo son NO EVALUABLES o si el arnés falla.

## 6. Predicciones firmadas (antes del humo y de la exploración)
| # | cantidad | rango / suceso | p |
|---|---|---|---|
| G1 | K(ING_SEL_C), mediana, T 5e5 | [100, 115] | 0.70 |
| G2 | K(ING_SEL_50), mediana | [100, 140] | 0.65 |
| G3 | SEL_50 > SEL_C en K, ≥ 8/10 | — | 0.50 |
| G4 | SEL_50 > SEL_C en K_nac, ≥ 8/10 | — | 0.50 |
| G5 | fund_2a(SEL_50) < fund_2a(SEL_C), ≥ 8/10 | — | 0.45 |
| G6 | SEL_50 > AZA_50 en K, ≥ 8/10 | — | 0.80 |
| G7 | AZA_50 < SEL_C en K (carga de 50 genes sin selección), mediana | — | 0.70 |
| G8 | alguna corrida de SEL_50 alcanza el tope 600 (guardia) | — | 0.25 |
| G9 | temp_boca y/o sesgo_boca entre los 5 genes que más se mueven en SEL_50 | — | 0.60 |

## 7. Para la nube (si hay señal): serie 48811–48830, réplica 48831–48850; 20 semillas, T 1e6, mismos brazos; letra = §5 con 15/20.

## 8. Lo que salió (se escribió DESPUÉS de los números; §1–§6 quedan como estaban. EXPLORATORIO)
**Instrumento (sha 16):** construye_g50 61a396d184779906 · motor_eco50 d85bbcda7b40fa19 · motor_g50 32f9e5dd4ddd20dd · nucleo_g50 6f01bd7ec241e185
(las corridas de 19:28 usaron nucleo 8e21e3bc7a6e33b0, anterior a los brazos AZA_47 y *_V; la física de los brazos comunes es la misma: arnés (A)/(B)
repetido con el nucleo nuevo) · corre_g50 6c4acde142cb3b05 · identidad_g50 206809a3fc3dd6ca.
**Arnés:** corrida entera 16/17 (`identidad_g50_salida.txt`; lo único que falla es (U): **clip_kw es MUDO**, 49 genes efectivos); corrida de brazos
22/22 (`identidad_g50_salida_brazos.txt`: (A) base bit a bit, (V) vivero finito bit a bit con la base, (B), (Z), (D)).

**Vivero permanente, T 5e5, 10 semillas 48801–48810 (AZA_47: 5), pareado contra ING_SEL_C:**
| brazo | K | K_nac | fund_2a | K > SEL_C | K_nac > SEL_C | fund_2a < SEL_C |
|---|---|---|---|---|---|---|
| ING_F1 | 96.28 | 12.45 | 64 305 | 0/10 | 0/10 | 0/10 |
| ING_SEL_C (15) | 101.05 | 16.28 | 43 725 | — | — | — |
| ING_SEL_25 | 102.57 | 19.85 | 37 249 | **10/10** (+1.41) | **10/10** (+3.24) | **10/10** (−6 214) |
| ING_SEL_47 | 102.29 | 18.86 | 37 035 | **10/10** (+1.20) | **10/10** (+2.21) | **10/10** (−6 876) |
| ING_AZA_47 (5) | 93.85 | 4.51 | 49 303 | 0/5 | 0/5 | 2/5 |
| ING_SEL_50 | 92.02 | 2.56 | 33 795 | 0/10 (−9.02) | 0/10 (−13.97) | 10/10 (−9 418) |
| ING_AZA_50 | 92.67 | 5.11 | 56 911 | 0/10 | 0/10 | 0/10 |
SEL_47 > AZA_47: K 5/5 (+8.34), K_nac 5/5 (+14.25), fund_2a menor 5/5. SEL_25 contra SEL_47: K 8/10 (+0.28), K_nac 9/10 (+1.03).
SEL_50 contra AZA_50: K 4/10 → sin herencia da lo mismo: la selección de SEL_50 no suma K.

**Vivero FINITO hasta 1e5, T 2e5, 10 semillas (sin subsidio en la ventana de K; la lectura que propone Opus M por su candidato E3):**
ING_SEL_C_V K 9.60 · K_nac 7.71 · persiste 10/10 — ING_SEL_47_V K **14.90** · K_nac 12.65 · 10/10 (**10/10** contra SEL_C_V, +5.49) —
ING_AZA_47_V K 2.62 · persiste 4/10 (SEL_47_V > AZA_47_V 10/10, +11.9).

**Genes (vivos en T, mediana de log g/G0):** en SEL_25 y SEL_47 el líder es **temp_boca ↓** (0.30 → ~0.11; −0.9 a −1.0) y luego tau_e ↓, pat_min ↑,
alpha ↑, peso_sed ↓. En SEL_50 el líder es **dote ↓ (0.6 → 0.20)**, rep_X ↓: los hijos viven 26 pasos (SEL_47: 406; SEL_C: 381); n_nac 35.7k (SEL_C 22.5k).
No toca el tope 600 (max_vivos ≤ 127).

**Predicciones de §6:** G1 ✓ · **G2 REFUTADA** (92.0) · **G3 REFUTADA** (0/10) · **G4 REFUTADA** (0/10) · G5 ✓ pero por la razón equivocada
(la historia de vida) · **G6 REFUTADA** (SEL_50 > AZA_50 sólo 4/10) · G7 ✓ · G8 no ocurrió (lo favorecido) · G9 ✓.

**Lectura exploratoria:** HAY SEÑAL para «más genes del CEREBRO → techo más alto»: con 25 o 47 genes la selección da más K, más K_nac y ~15 % menos
fundadores repuestos que con 15, en 10/10, y sin herencia no pasa (AZA_47); se repite sin subsidio (vivero finito: +55 % de K, 10/10).
NO es monótono: 25 ≈ 47 (25 un poco mejor) — los 22 genes de marcha, arranque y división no suman; el aporte está en boca y valor, con temp_boca a la cabeza.
**Con la historia de vida libre (50) es PEOR** y la herencia no ayuda (SEL_50 ≈ AZA_50): lo trato como NO EVALUABLE para la pregunta del cerebro
(la guardia del director), aunque no toque el tope. Mecanismo probable, candidato a ERR de instrumento: con donante 'padre' el banco del vivero guarda
al PADRE en cada parto → premia PARIR, no hijos que viven; la dote colapsa y los refundados salen de ese banco.

## 9. Esqueleto para la nube (semillas NUEVAS; grep hecho: 488xx libre)
- Brazos: ING_SEL_C · ING_SEL_25 · **ING_AZA_25** (falta construirlo: el control propio de 25) · ING_SEL_47 · ING_AZA_47 · **ING_SEL_16T**
  (15 + temp_boca: ¿es UN gen o es la cantidad? falta construirlo) · ING_F1. Dos regímenes: vivero permanente T 1e6 y vivero finito 1e5 con T 5e5.
- Serie 48811–48830, réplica 48831–48850; 20 semillas; Pool lo lanza sólo el coordinador.
- Letra (15/20): P2 SEL_25 > SEL_C en K y K_nac y fund_2a menor; P3 SEL_25 > AZA_25 en K y K_nac; P5 SEL_16T contra SEL_25 (si SEL_16T ≥ SEL_25 en
  ≥ 10/20, el techo lo sube UN gen, no la cantidad).
- SEL_50 NO va a la nube hasta arreglar el banco (que el banco pese hijos que VIVEN, o sacar la historia de vida del banco): es otro experimento.
