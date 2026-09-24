# PREREGISTRO — JUACO-ECO v2: ÓRGANOS COMO GENES, en tres mundos a la vez (24-sep-2026, coordinador de la nube; antes de cualquier serie)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/juaco_eco/`. Nivel: **10 (JUACO-ECO)**, frente 2. Aprobado por el director
el 24-sep (~11:35 UTC): *"sí, arranca ECO v2 con órganos como genes"*, con tres pedidos: que audite yo, que use modelos baratos cuando no haga
falta un experto, y que corra tres mundos a la vez con capacidades distintas. Archivos nuevos; no se toca nada del PC.

## 0. Instrumento (sha a 16)
- `construye_eco_org.py` (ff5531748aa4bd6a) construye por anclas `motor_eco2.py` (0921ee3a50ce7f7a) desde `motor_eco.py` (bca3033878b59622)
  y `carros/FAMB_ORG_ECO.py` (75d5f4118079ff15) desde `carros/FAMB_RES0_ECO.py` (94ea78589bc2ce24).
- Arnés Python `identidad_eco_org.py`: **9/9** — órganos apagados = FABRICA_ECO en toda la física; los dos prendidos = FAMB_RES0_ECO;
  `ensena` sí y `filtra0` no = FAMB_RES con el `_see` de ECO; la expresión sigue al gen en cada cuerpo; la mutación prende órganos;
  checkpoint y reanudación iguales.
- Runner `corre_eco_v2.py` (**41fd6280607d4f4f**; el sha va también en el log y en `RESUMEN.json`) y su arnés `identidad_eco_v2.py` (**7fe082aeb5738186**):
  **15/16** antes del gemelo — (M) mundos y brazos; (T) las medidas de los órganos calculadas a mano en los tres mundos; (V) 8 ramas de la
  letra; (R) banderas. Falta (G): gemelo == Python en los tres mundos y los dos brazos. **Con (G) debe dar 22/22.**
  **12:28 — con el gemelo (motor_eco_rapido_org, 99/99): 21/21** (decía 22/22: conté mal los casos; la letra no cambia). Prueba del Pool
  (20092–20093, T 4 000) a las 12:30: corre y escribe su RESUMEN.
- Motor de la serie: el gemelo `motor_eco_rapido_org.py` (lo construye el compilador). **Sin su arnés N/N no hay serie.**

## 1. Pregunta
¿La selección PRENDE un órgano que nadie le puso? Hasta ECO v1.1 la selección sólo movía perillas (alpha, aversion). Aquí dos órganos
que ya existen y están medidos pasan a ser genes:
- **`ensena`** (lo expresa el PADRE): pasa su tabla al hijo en el parto (el órgano de subida_n10b);
- **`filtra0`** (lo expresa el HIJO): quita de la tabla recibida las entradas neutras (el filtro de subida_n10c, FUNCIONA ×2).
Cada uno es un rasgo con umbral: un número que muta como los demás y el órgano se expresa si vale ≥ 1.0. Todos nacen en 0.9 (APAGADOS);
una mutación lo prende con p ≈ 0.24. Las 8 sombras de cada cuerpo lo llevan y derivan igual: el control de la deriva es el de siempre.
Si enseñar sirve, los hijos de los que enseñan viven más y el gen se extiende; en AZAR (el genoma de todo cuerpo nuevo sale del banco al
azar) no puede extenderse por eso.

## 2. Diseño
- **Igual que ECO v1:** vivero con banco de 200 y 8 sombras, mutación (p 0.05, σ 0.15), corte en 60 000, **T = 120 000**, carro de la
  familia para todos los cuerpos (con los órganos que diga su genoma).
- **Tres mundos a la vez** (lo pidió el director), de capacidad distinta:

| mundo | esc | L | fundadores | quimiostato (objetos por paso) | tope |
|---|---|---|---|---|---|
| w30 | 30 | 1 200 | 30 | 0.9 | 3 000 |
| w90 | 90 | 3 600 | 90 | 2.7 | 3 000 |
| w270 | 270 | 10 800 | 270 | 8.1 | 9 000 |

- **Brazos:** VIDA (el hijo copia el genoma del padre, mutado) y AZAR (control de deriva). Mismas semillas en los tres mundos.
- **Semillas nuevas** (grep del 24-sep: sin usos 20011–20099): serie **20011–20030**, réplica **20031–20050**, práctica **20091–20099**.
- Sin juez de colonias: la pregunta se lee en el banco del corte.

## 3. Medidas (sólo física y genoma)
- **Selección contra sombras** en el corte (como P2 de v1): por gen, +1 si la media del banco (log g/G0) supera a sus 8 sombras.
- **Fracción del banco con el órgano expresado** (gen ≥ 1.0) en el corte; y entre los vivos en T (descriptivo).
- Descriptivo: persistencia en T, R0 de la cohorte tras el corte, otros genes seleccionados.

## 4. Predicciones firmadas (coordinador; humo Python w30: VIDA 24 % del banco con `ensena`, AZAR 12 %; números sin valor)
| cantidad | rango | probabilidad |
|---|---|---|
| **`ensena` (+) contra sombras en VIDA, w90 — la que puede fallar** | 13–20 /20 | O1 con 0.70 |
| `ensena` (+) en VIDA, w30 / w270 | 9–18 / 14–20 | 0.50 / 0.75 |
| banco con `ensena`: VIDA > AZAR, por mundo | 13–20 /20 | O2 con 0.70 |
| `filtra0` (+) en VIDA, por mundo | 5–16 /20 | 0.35 |
| AZAR con falsos positivos (> 8/20) en algún gen | — | 0.05 |
| veredicto | FUNCIONA 0.55 · MODESTO 0.25 · NO 0.15 · NO EVALUABLE 0.05 | — |

## 5. Qué refuta
- **H (la selección prende el órgano):** `ensena` no sale de sus sombras en VIDA (O1 cae) o el banco de VIDA no lo lleva más que el de AZAR
  (O2 cae), en al menos 2 de los 3 mundos.
- **El instrumento:** AZAR saca genes de sus sombras (> 8/20): la deriva no está controlada.

## 6. Criterio por la letra (`corre_eco_v2.veredicto`; se imprime al final)
Por mundo m ∈ {w30, w90, w270}, con 20 semillas:
- **O1_m:** en VIDA, `ensena` queda por ENCIMA de sus 8 sombras en ≥ 15/20.
- **O2_m:** la fracción del banco con `ensena` expresado es mayor en VIDA que en AZAR (pareado por semilla, estricto) en ≥ 15/20.
- **F_m (secundario, no decide):** `filtra0` por encima de sus sombras en VIDA en ≥ 15/20.
Veredicto de la serie:
- **NO EVALUABLE:** serie incompleta; bloqueados > 0 en alguna corrida; AZAR con > 8/20 en algún gen de algún mundo.
- **FUNCIONA — LA SELECCIÓN PRENDE EL ÓRGANO DE ENSEÑAR:** O1_m y O2_m en ≥ 2 de los 3 mundos.
- **HAY ALGO MODESTO:** O1_m y O2_m en exactamente 1 mundo, o alguno de los dos en ≥ 2 mundos.
- **NO:** cualquier otro caso.
El bloque se declara sólo si serie y réplica dan el mismo veredicto; si no, vale el menor.

### Vocabulario
- Permitido: «la selección prende el órgano», «el gen del órgano sale de sus sombras», «linaje», «cuerpos vivos (N = …)».
- Prohibido: «evoluciona» (la regla del vocabulario la cambia el director), «especie», «cultura», «vida artificial abierta».

## 7. Auditoría propia (el director pidió que audite yo; se hizo ANTES de correr)
Pregunta de siempre: ¿qué escenario haría pasar el criterio por la razón equivocada?
1. **Arrastre genético (hitchhiking):** un `ensena` prendido podría subir por ir pegado a buenas perillas en el mismo linaje. Las sombras
   no lo descartan del todo (derivan con la misma genealogía, así que el arrastre por genealogía también lo tienen); O2 contra AZAR sí lo
   acota. Se reporta además la correlación de `ensena` con alpha en el banco (descriptivo).
2. **Umbral y muestreo:** el gen nace a 0.1 en log del umbral; un "prendido" por deriva pura es posible (AZAR lo mide). Si AZAR llega a
   fracciones altas, O2 lo cubre.
3. **Mundo chico (w30):** con pocos nacimientos la deriva domina; por eso el veredicto pide 2 de 3 mundos y no los 3.
4. **Tope en w270:** si la familia hace crecer la población hasta 9 000, NO EVALUABLE (bloqueados), no un resultado.
5. **El órgano beneficia al hijo, no al padre:** si la selección fuera sólo por fertilidad inmediata (el banco guarda padres), `ensena`
   podría no verse; se lee también en los vivos en T (descriptivo). No se cambia la letra por eso.

6. **(nota añadida a las 12:21, antes de cualquier serie de v2; hallada en el humo de ECO v3) Bancos de composición distinta:** en AZAR
   los órganos se prenden por deriva sin filtro y su fracción en el banco sube con el tiempo; en VIDA el banco son pocos padres. O2
   ("VIDA lleva más `ensena` que AZAR") queda sesgado EN CONTRA de VIDA: es conservador. La letra no cambia.

## 8. Costo
Gemelo: estimado ~8 s (w30), ~30 s (w90) y ~90 s (w270) por corrida → ~80 min de CPU por serie, ~30 min con Pool 3. Python (humo w30,
T 20 000): 22–30 s por brazo.

## 9. Humo (24-sep, 11:48 UTC, Python; números sin valor)
`corre_eco_v2.py --humo` (20091, w30, T 20 000, corte 10 000): 51 s. VIDA persiste (6 vivos, máximo 44), banco con `ensena` 0.24 y
`filtra0` 0.10, 5 de 6 vivos con `ensena`, `ensena` +1 contra sombras; AZAR se extingue, banco 0.12 / 0.17.
Carpeta `datos/humo/eco_v2_humo_python_20260924_114843`.

## 10. Puntos
Ninguno declarado aquí; los decide el director.
