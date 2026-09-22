# ESBOZO DE PREREGISTRO — candidato al tronco "la boca lee las dos filas" (boca2 = VETO por cualquier necesidad)

**Estado: ESBOZO del integrador (22-sep-2026). No es preregistro vigente: lo convierte el coordinador (preregistro + commit antes de correr).**
**Misión:** llegar a la AGI por este camino; el método manda sobre el cómo.
**Origen de la idea:** hallazgo externo de F0 (`externo/F0_fable_solo/REGISTRO.md` 20:08), decisión 1 de §6 de
`externo/_evaluacion/PARA_JUACO_mundo_fase10.md`. **Reproducido en el repo** por `diagnostico_boca_mapa.py` (INFORME_INTEGRACION §3).

## 1. Hipótesis
La boca del tronco decide con la fila de valor de la **necesidad activa** (`Wp[_nm]-Wn[_nm]`, `_nm = _na`). El veneno sólo tiene efecto en
la energía (`EFECTO['veneno'] = (-0.4, 0.0)`): la fila de la SED recibe R = 0 al morderlo y nunca aprende que es malo (ídem sal para la fila
del HAMBRE). Resultado medido: con sed, el tronco muerde el veneno que ya sabe malo en la otra fila. **H-B2:** si la otra necesidad puede
VETAR (nunca atraer), el cuerpo deja de morder lo que sabe malo en cualquier fila, sin dejar de comer, y vive más; en el mundo de la fase 10,
el inmortal recupera el ancla (el muro era la boca).

## 2. Mecanismo mínimo — memoria nueva CERO, regla de aprendizaje nueva NINGUNA
Una línea en la boca, con dos necesidades y fuera de CUELLO_MIN (que ya lee el mínimo de las dos filas estando saciado):
`_wt = _wt(fila activa) + min(0, v(fila de la otra necesidad))`, con `v = _vnec(...)` (ya existía, sólo lectura, mismo ruteo puerta/lenta
que la boca). No consume sorteos. **Con n_nec = 1 no hay otra fila: inerte por construcción** en el examen v3′ y en las baterías.
Variante alternativa (NO se corre a la vez, regla 2): `MIN` = CUELLO_MIN siempre (pierde la atracción de la fila activa).

## 3. Instrumento y anclas
- Candidato real: `organismo_v15_boca2.py` construido como dE5 (`experimentos/tronco_v15_dE5/construye_v15_dE5.py`): desde
  `nivel11_mundo_vivo/organismo_vivo_rep2.py` (`96feb4918dc5d694`) + B-5 literal de `creacion_B/construye_codigo.py`, `desambiguar=1` por
  defecto; gemelo `organismo_v15_boca2g.py` desde `organismo/organismo_v142g.py` (`9e5f566cd6a7a4d2`) para T-B (en n_nec=1 es v142g exacto);
  baterías copiadas `bateria_v15_boca2.py` y `bateria_generaliza_v15_boca2.py` con entrada campo a campo contra la del tronco (regla 14) y humo
  que escribe su JSON (ERR-42).
- **Identidad con la perilla apagada** (arnés modelo `identidad_v15_dE5.py`, 68/68): boca2=0 ≡ `organismo_v142` bit a bit (vivo=0, n_nec=1) y
  ≡ `organismo_vivo_rep2` (desambiguar=0); boca2=1 ≡ boca2=0 con n_nec=1 (inercia, debe ser IDÉNTICO); controles que deben diferir: boca2=1 en
  VIVO y CUELLO_MIN (n_nec=2), VETO_BARAJADO ≠ boca2=1.
- **Sonda ya construida y verificada en esta carpeta** (no es el candidato): `construye_boca2.py` → `organismo_boca2.py` desde
  `mundo_fase10.py` (`84e97674f709a900`), 3 anclas, 0 sorteos; arnés en `identidad_y_mini_boca2.py` (B1–B4 idénticos, C1–C2 difieren).

## 4. Las siete puertas, con v2 y v3 LADO A LADO (declarado: v2 rechaza al propio tronco, ERR-91; v3 no pasó su réplica, CAL-1 0.898 y CAL-4)
| # | medida | letra v2 (CRITERIO_TRONCO_v2) | letra v3 (CRITERIO_TRONCO_v3) | predicción (P pasa v2 / v3) |
|---|---|---|---|---|
| T-A sobrevive | mundo vivo rep2, VIVO y CUELLO_MIN, T = 100 000 | muertes ≤ 1.10× · r ≥ tronco−10 · **A₁₂ pareado ≥ 0.50** (n = 20: el placebo pasa 0.316) | medianas + no inferioridad LI(d) > −10, n = 40 | muertes 0.70–0.95× en VIVO; CUELLO_MIN 0.85–1.0× (el veto no actúa saciado) · 0.55 / 0.80 |
| T-B generaliza | `bateria_generaliza` G1/G2 | G1 ≥ 0.80, G2 ≥ 0.85 | igual | **por identidad** (n_nec = 1, inerte): G1 1.000 como el tronco · 0.97 / 0.97 |
| T-C se desdice | (i) E2 examen; (ii) `invertir_vivo_en` | (i) ≥ 18/20; (ii) **A₁₂ ≥ 0.75 vs apagado** | (i) igual; (ii) no inferioridad LI > −10, n = 40 | (i) por identidad; (ii) neutra (la inversión es comida↔veneno, misma fila; el veto no toca eso): v2 cae · 0.15 / 0.80 |
| T-D sin alias | bloque de la sal 9 ALIAS / 9 LIMPIAS (`corre_sal`: 326…670 / 307…342) | C1, C2, C6 de B-5 | igual (importados) | riesgo: vetar la sal con hambre cambia las mordidas que alimentan B-5 · 0.70 / 0.70 |
| T-E no regresión | examen v3′, conducta por escenario | ≥ 18/20 | igual | por identidad · 0.97 / 0.97 |
| T-F coste | celdas, divisiones, muertes (examen y vivo) | ≤ 1.25× | igual | 0.85 / 0.85 |
| T-G capacidad nueva | **J cruzado** por semilla en el mundo vivo (RENACE, T = 100 000): J_x = rechazo(malo en la OTRA fila \| necesidad activa) + mordida(bueno de la activa) − 1; y R₀ del inmortal en el mundo F10 | la del preregistro | declarar nulo (J_x ON = OFF), margen (+0.30), control **VETO_BARAJADO** (la otra fila de un tipo sorteado con rng propio, misma magnitud sin información) + PLACEBO; n que da 0.95 bajo el nulo y 0.80 en el margen (con la sd de la mini-prueba) | J_x +0.4 a +0.7 sobre OFF; BARAJADO ≤ +0.15 · 0.75 / 0.75 |
| **entero** | | | | **v2 ≈ 0.08 (cae por T-C ii y la moneda de T-A) · v3 ≈ 0.35** |

Refuta H-B2: T-G no supera a VETO_BARAJADO por el margen, o muertes en VIVO > 1.10× (el veto mata de hambre/sed), o el inmortal del mundo
F10 con boca2 sigue por debajo de 0.8 (el muro no era la boca).

## 5. Semillas NUEVAS propuestas (verificadas libres en `experimentos/`, `registro/`, `datos/` el 22-sep; ver INFORME_INTEGRACION §5)
Examen (T-B, T-C i, T-E, T-F) **2521–2540** · T-A **2541–2580** (n = 40; v2 lee las 20 primeras) · T-C ii **2581–2620** · T-G **2621–2660** ·
réplica **2661–2800** con la misma estructura. T-D usa las semillas fijas del bloque de la sal (existentes, no se reservan).

## 6. Coste
Paquete (constructor + gemelo g + dos baterías copiadas + arnés + runner con `--humo`) ≈ una sesión de agente (el de dE5 es la plantilla).
CPU: ≈ 460 corridas de T = 100 000 por serie (~20 s cada una) ≈ 25 min con Pool 7; réplica otro tanto.

## 7. Mini-prueba de un proceso (sonda, 6 corridas, boca2 = 1; OFF del diagnóstico y del humo del repo). PREDICCIONES firmadas ANTES de correrla
| corrida | OFF medido | predicción ON |
|---|---|---|
| M1 mundo vivo fase 9, RENACE s1, T 20 000 | veneno con SED 63/84; R₀ 1.154 | veneno con SED ≤ 0.15 de las exposiciones; agua con SED ≥ 0.80; R₀ ≥ 1.154 (70 %) |
| M2 F10 calib F0, RENACE s1, T 20 000 | veneno con SED 60/68; R₀ 0.065 | veneno con SED ≤ 0.15; R₀ > OFF (80 %) y < 0.8 (80 %) |
| M3 F10 enmienda 1, RENACE s1, T 20 000 | veneno con SED 18/27; R₀ 0.483 | R₀ 0.5–2.0 |
| M4/M5 F10 enmienda 1, RENACE s5/s6, T 100 000 | R₀ 0.306 / 0.214 | R₀ 0.4–1.3; P(mediana ∈ [0.8, 1.3]) = 0.35 |
| M6 F10 enmienda 1, NADA s5, T 100 000 | R₀ 0.146 | 0.15–0.35; P(ON > OFF) = 0.65 |

## 8. Resultado de la mini-prueba (añadido DESPUÉS de correrla; §1–§7 sellados antes: sha `518e5ca1099f2f19`)
Arnés de la sonda **11/11** (B1–B3 idénticos con boca2=0; B4 **inerte con n_nec = 1**; C1–C2 difieren). `datos/humo/mini_boca2_20260922_124015.json` (`09dd2c8c075e3d86`).

| corrida | OFF | ON (boca2 = 1) | mi predicción |
|---|---|---|---|
| M1 vivo fase 9 RENACE s1 | R₀ 1.154; veneno con SED 63/84; exposiciones a lo bueno 243, a lo malo 1 462 | **R₀ 0.045** (desc 1, muertes 21); veneno con SED **2/224**; agua con SED 11/11; exposiciones a lo bueno **73**, a lo malo 1 535 | veto ✓; agua ✓; **R₀ ≥ OFF: REFUTADA** |
| M2 F10 calib F0 RENACE s1 | R₀ 0.065; bueno 145 / malo 465 | R₀ 0.028; veneno con SED 1/20; bueno 53 / malo 870 | veto ✓; **R₀ > OFF: REFUTADA** |
| M3 F10 enm. 1 RENACE s1 | R₀ 0.483; bueno 222 / malo 896 | R₀ 0.600; veneno con SED 0/61; bueno 302 / malo 1 334 | ✓ (0.5–2.0) |
| M4 / M5 F10 enm. 1 RENACE s5 / s6 | 0.306 / 0.214 | 0.478 / 0.173 (mediana 0.33) | M4 ✓, M5 ✗; **ancla no alcanzada** (P 0.35 declarada) |
| M6 F10 enm. 1 NADA s5 | 0.146 | 0.215 | ✓ |

**Lectura (n = 1 por celda; no se declara nada).** El veto hace exactamente lo que dice (deja de morder lo malo de la otra fila: 63/84 → 2/224)
y aun así **hunde al inmortal en el mundo del tronco** (R₀ 1.15 → 0.05): en ese mundo un objeto sólo desaparece si se muerde (o por el
olvido lento), así que lo malo rechazado **ocupa los sitios** y lo bueno se vuelve raro (exposiciones a lo bueno 243 → 73). Es la trampa 3
("el mundo que se come la comida") vista desde el otro lado: **morder el veneno con sed es, en el mundo del tronco, la forma de limpiarlo.**
Donde los sitios se reponen (F10 con `cap 25, regen 50`), el veto ayuda (0.48 → 0.60; 0.31 → 0.48; NADA 0.15 → 0.22) pero no lleva el ancla.
**Consecuencia para el candidato:** con esta forma (VETO), T-A (sobrevive, mundo vivo de rep2) probablemente CAE; la P de §4 baja a
v2 ≈ 0.02 / v3 ≈ 0.10. "La boca" es causa del mordisco, **no** el muro por sí sola: el muro es boca + mundo que no retira lo rechazado
+ cuerpo que no se aleja (decisión 2, exploración). Antes de preregistrar el candidato, decidir el mundo de T-A (ver INFORME §6).
