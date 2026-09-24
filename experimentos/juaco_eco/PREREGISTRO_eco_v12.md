# PREREGISTRO — JUACO-ECO v1.2: selección y FAMILIA (el hijo recibe la tabla del padre sin lo neutro) en el mundo de ECO (24-sep-2026, coordinador de la nube; antes de cualquier serie de v1.2)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/juaco_eco/`. Nivel: **10 (JUACO-ECO)**. Frente 2 del plan vigente.
No es candidato a tronco. Ningún archivo del PC se toca: v1.2 son archivos nuevos. Escrito bajo la regla 12; el director puede
rechazarlo. Los veredictos de ECO v1 (NO EVALUABLE ×2) y v1.1 (HAY ALGO MODESTO ×2; L: NO PERSISTE LARGO ×2) quedan como están.

## 0. Instrumento (sha a 16; se completa en el commit que sube este archivo)
- Runner y juez: `corre_eco_v12.py` (el sha va en el log y en `RESUMEN.json`). Importa sin tocar `corre_eco.py`, `corre_eco_v11.py`
  (fundadores con flujo 7/8, `med_bat`), `motor_eco.py`.
- Carro nuevo: `carros/FAMB_RES0_ECO.py` (94ea78589bc2ce24), construido por `construye_eco_familia.py` desde
  `subida_n10b/carros/FAMB_RES.py` (2addb7ca5b9d031d). Arnés `identidad_eco_familia.py` **7/7**: con SIN0 = 1 es **bit a bit** el
  RES_SIN0 de subida_n10c (FUNCIONA ×2 en la nube); con SIN0 = 0 es FAMB_RES; checkpoint y reanudación iguales.
- Motor de la serie: el gemelo `motor_eco_rapido_fam.py` (en construcción por el compilador). **Sin su arnés N/N no hay serie.** El humo
  corre con el motor Python.

## 1. Por qué v1.2 (hallazgo del 24-sep, 10:50, antes de ver datos de v1.2)
- En la pista v2 (el mundo de ECO) cada cuerpo nuevo es una instancia nueva del carro y FABRICA pasa `memoria=None`: **el hijo nace sin
  nada del linaje**. En ECO v1/v1.1 la selección sólo pudo mover perillas; aun así llevó el R0 de la cohorte tras el corte a 0.91–0.99,
  y los linajes seleccionados persisten en el filo (L de v1.1: VIDA 7 y 5 de 20 a 1e6; AZAR 0 y 0).
- subida_n10c midió en la pista v2 con flujo fijo que la familia que pasa su tabla sin las entradas neutras da R0 de los nacidos ≥ 0.90
  (0.941 y 0.946) con las perillas de fábrica y sin selección.
- **Hipótesis de v1.2:** las dos piezas juntas (perillas seleccionadas + tabla de la familia) pasan el filo: el linaje del bicho real
  persiste 940 000 pasos tras el corte, sin comida regalada (ERR-104) ni fundadores repuestos (ERR-118).

## 2. Qué cambia respecto de v1.1 (un cambio de mecanismo; el resto igual)
- **Igual:** mundo (esc 90, L 3600, quimiostato 2.7 objetos por paso, 90 fundadores, tope 3000), vivero con banco de 200 y 8 sombras,
  mutación (p 0.05, σ 0.15), corte en 60 000, T = 1 000 000, el cálculo de selección contra sombras, el juez v2 pareado con placebo.
- **Cambia:** el carro de tres brazos es FAMB_RES0_ECO.

| brazo | genética (corre_eco.BRAZOS) | carro | papel |
|---|---|---|---|
| **VIDA_T** | VIDA (18 genes, del padre) | FAMB_RES0_ECO | hipótesis |
| AZAR_T | AZAR (18 genes, del banco al azar) | FAMB_RES0_ECO | control de la selección con familia |
| MUT0_T | MUT0 (sin mutación) | FAMB_RES0_ECO | control: la familia sola, sin variación genética |
| VIDA | VIDA | FABRICA_ECO | referencia: el v1.1 sin familia, en las mismas semillas |

- **Juez (F3):** colonia de 9 del banco de VIDA_T contra la de AZAR_T de la misma semilla, **con el carro de la familia**, en una
  batería sellada NUEVA **19801–19820**, con **T_b = 100 000** (en v1.1 era 20 000). Por qué, escrito antes de ver datos: con la familia las
  colonias pueden vivir más de 20 000 pasos y empatar en el techo; un empate no cuenta como victoria. Placebo igual que v1.1 (flujo 8,
  válido en [5, 15]).

## 3. Semillas NUEVAS (grep del 24-sep en `*.py` y `*.md`: ninguna 197xx–199xx en uso)
- Serie **19701–19720**; réplica **19721–19740**; batería sellada **19801–19820**.
- Práctica **19901–19909** (humo 19905; prueba del Pool 19902–19903; el arnés del gemelo usa 19901–19909).

## 4. Medidas
- **persiste:** cuerpos vivos en T = 1e6 (y descriptivo: en 120 000, como v1).
- Descriptivo: R0 de la cohorte nacida tras el corte (en [60 000, T − 20 000]), cuerpos vivos en T, cuerpos vivos cada 50 000 pasos
  tras el corte, `max_vivos`, bloqueados.
- Selección contra sombras en VIDA_T (como P2 de v1); falsos positivos en AZAR_T.

## 5. Predicciones firmadas (coordinador de la nube)
| cantidad | rango | probabilidad |
|---|---|---|
| **VIDA_T persiste en 1e6 /20 — la que puede fallar** | 10–20 | F1 (≥ 15) con 0.50 |
| VIDA (sin familia) persiste en 1e6 /20 | 3–9 | — |
| VIDA_T − VIDA en 1e6 | 3–15 | F2 (≥ 6) con 0.60 |
| AZAR_T persiste en 1e6 /20 | 2–14 | — |
| MUT0_T persiste en 1e6 /20 | 0–10 | — |
| VIDA_T > AZAR_T en el juez /20 | 11–19 | F3 con 0.45 |
| gen seleccionado en VIDA_T (alpha +) /20 | 15–20 | F4 con 0.85 |
| placebo en [5, 15] en los dos brazos | — | 0.97 |
| veredicto | MODESTO 0.45 · FUNCIONA 0.20 · NO 0.28 · NO EVALUABLE 0.07 | — |

## 6. Criterio por la letra (`corre_eco_v12.veredicto`; se imprime al final)
**Predicciones**
- **F1:** VIDA_T persiste en 1e6 en ≥ 15/20.
- **F2:** VIDA_T − VIDA ≥ 6 semillas persistentes en 1e6 (la familia suma sobre la selección sola).
- **F3:** VIDA_T > AZAR_T en el juez (pareado, estricto) en ≥ 15/20 (P = 0.021 bajo la nula).
- **F4:** algún gen del banco de VIDA_T queda fuera de sus 8 sombras con el mismo signo en ≥ 15/20.
- **C (descriptivo, no decide):** MUT0_T y AZAR_T en 1e6. Si MUT0_T ≈ VIDA_T, la familia basta sin selección; se dice así.

**Veredicto**
- **NO EVALUABLE** si: la serie está incompleta o T ≠ 1e6; hay bloqueados; AZAR_T da > 8/20 en algún gen; el placebo sale de [5, 15].
- **FUNCIONA:** F1 + F2 + F3 + F4.
- **HAY ALGO MODESTO: PERSISTE CON FAMILIA:** F1 + F2 (sin F3 + F4).
- **HAY ALGO MODESTO: SELECCIÓN CON FAMILIA:** F3 + F4 (sin F1 + F2).
- **NO:** cualquier otro caso.

El bloque se declara sólo si **serie y réplica dan el mismo veredicto**; si no, vale el menor (dos MODESTO distintos cuentan como
MODESTO, con las dos lecturas escritas).

**Vocabulario**
- Permitido: «linaje», «cuerpos vivos del brazo (N = …)», «la familia pasa su tabla», «persiste 940 000 pasos tras el corte».
- Prohibido: «población» sin la medida; «evoluciona», «especie», «vida artificial abierta», «cultura» (se dice «la tabla de la familia»).

## 7. Qué refuta
- **H (persistencia con familia):** F1 cae (el bicho con familia y selección no persiste 940 000 pasos en ≥ 15/20).
- **"La familia suma":** F2 cae (VIDA_T no persiste más que VIDA).
- **"La selección suma con familia":** F3 cae con el placebo válido.

## 8. Puntos
Los de `PREREGISTRO_eco.md` §9 y los decide el director; la nube no declara porcentajes.

## 9. Costo
Gemelo: se mide en su arnés y en el humo del gemelo; con la familia los linajes pueden sostener más cuerpos (humo Python 19601: 116
contra 68 de media), así que una corrida de 1e6 puede costar varios minutos. Python: ~60 µs por cuerpo y paso (una serie ~6.5 h a
120 000 pasos; inviable a 1e6).

## 10. Humo, arnés y enmiendas (24-sep, UTC; números sin valor)
- **Arnés `identidad_eco_v12.py`: 18/19 antes del gemelo** (la parte Python completa): (J) el juez con FABRICA_ECO y flujo 7 = el de
  v1.1; (C) el brazo VIDA de v1.2 = el VIDA de v1.1 en todas sus claves; (F) VIDA_T usa la familia y su física difiere; (V) 11 ramas de
  la letra; (R) banderas. **(G) gemelo == Python: pendiente; sin (G) no hay serie** (el arnés completo debe dar 19/19).
- **Humo Python 10:58** (`corre_eco_v12.py --humo`; 19905, VIDA_T y AZAR_T, T 30 000, corte 8 000, juez 2 semillas T_b 6 000): 240 s.
  VIDA_T 43 cuerpos vivos en 12 000 (máximo 189), AZAR_T 25 (máximo 169); los dos juicios del humo tocan el techo de 6 000.
  JSON `datos/humo/eco_v12_humo_s19905_python_20260924_105806.json`. La letra corre (NO EVALUABLE con una semilla, como debe).
- Enmiendas tras el humo: ninguna.
- **12:30 — con el gemelo (motor_eco_rapido_fam, 132/132): arnés `identidad_eco_v12.py` 22/22** (el preregistro decía "19/19": conté mal los
  casos; no cambia nada de la letra). Antes, el arnés pasó el juez a semillas de práctica (19903–19904) por aviso del compilador: tocaba
  las dos primeras de la batería sellada. Prueba del Pool (19902–19903): corre; su juez sí usa 19801–19802 con bancos de práctica y
  T_b 2 000 (candidato nube-7, menor: no informa ningún resultado de la serie, pero rompe la letra de "sellada").
