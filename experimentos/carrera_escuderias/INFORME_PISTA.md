# INFORME — la pista de la carrera de escuderías · 22-sep-2026 (v2, tras la auditoría y la ENMIENDA 1)

**Veredicto: HAY ALGO MODESTO.** ERR-96 está cerrado con test (30/30), el chequeo estático está en el juez y la identidad da 35/35. La ENMIENDA 1 está implementada en la pista, pero **el humo escalado NO se corrió**: FABRICA depende de L (condición técnica) y hace falta una decisión aparte. Además, **la explicación que di de la ronda 0 queda refutada**: el mundo de un carro SOLO ya es 88–92 % veneno y sal.

## Qué cambió (v2)
- **ERR-96:**
  - La salida de un linaje tiene dos espacios de nombres. En el primer nivel está SOLO la verdad física que escribe `pista.py`; lo que devuelve `salida()` va en `d['carro']`.
  - `juez.resumen_linaje` lee una lista cerrada de claves físicas y verifica que la contabilidad física cierre (`coherente`).
  - `pista.plano()` (solo para el arnés) aborta si el carro intenta usar una clave física.
- **`revisa_carro.py`:**
  - Tokens prohibidos, en el texto crudo: `_getframe`, `inspect`, `gc`, `globals(`/`locals(`/`vars(`, dunders, frames, `importlib`, `exec(`/`eval(`/`compile(`, `open(`, `getattr(`, `np.random`, `default_rng`.
  - Lista blanca de imports: numpy, math, collections, itertools, functools, heapq, bisect, statistics, copy, dataclasses, typing, enum y operator.
  - Prohíbe métodos de escritura de archivos y exige `crea()`.
  - El juez lo corre antes de cada ronda y aborta si un carro no pasa.
- **H-4:** `pista.cfg_fabrica()` deriva en tiempo de ejecución toda la configuración (firma de `organismo_f9c.run` + `BRAZOS['REL']` + L/NK/PAT/EFECTO del monolito). FABRICA no tiene ninguna constante escrita a mano, y aborta si una perilla de rama no tiene el valor portado (`RAMAS`).
- **ENMIENDA 1:** `escala=1` por defecto (L = 40·N, nobj = 4·N). Con N = 1 es idéntico a la pista original (arnés I1).
- **Pizarra completa aparte:** `pizarra_log` sin tope; el juez la escribe en `<prefijo>_pizarra.jsonl.gz`.
- **Composición del mundo** registrada por cuarto de T.

## Pruebas
- `identidad_pista_salida.txt`: **35/35**.
  - Los 25 de antes con los mismos números (6+2+2 anclas bit a bit contra organismo_f9c con el mismo estado final del rng).
  - (I) escala: N = 1 igual; N = 9 da L = 360 y nobj = 36; pizarra completa (1800/1800); FABRICA aborta en la pista escalada.
  - (J) H-4: la configuración derivada coincide; 4 ramas ajenas abortan; `eta` distinta cambia la corrida.
- `test_tramposo_salida.txt`: **30/30**.
  - Un carro que declara 999999 hijos saca en el juez exactamente el R0 del honesto (0.36 y 0.3103).
  - Mutar `obs`/`res`/`info` no cambia la física, y `objs` no se puede escribir.
  - Se rechazan 20 fuentes tramposas y FABRICA pasa.
  - El juez aborta la ronda con un carro rechazado. Queda un log `datos/carrera_humo_rondatest_tramposo_*.log`.

## Condición técnica de la ENMIENDA 1: FABRICA SÍ depende de L y de nobj (no se adaptó)
- `carros/FABRICA.py` usa `L` en `see()` (distancias `% L`) y en la posición tras moverse (`(pos + mov) % L`). Con L = 360 calcularía mal las distancias y mordería donde no está.
- `see()` recorre TODOS los objetos: con N = 9 vería 36, no 4.
- Hoy aborta si `ctx['L'] != 40`.
- Opciones para decidir aparte (todas dan identidad con N = 1):
  - **A.** FABRICA toma L de `ctx` (un cambio) y conserva la visión global. Con la misma densidad, el objeto más cercano se comporta casi igual. La diferencia: el 1.0 % de los pasos no hay ningún objeto a ≤ 20 celdas (estimación estática C(319,36)/C(360,36)), y el carro iría a uno más lejano, cosa imposible en L = 40.
  - **B.** La pista entrega solo los objetos a ≤ 20 celdas (el campo del original) y FABRICA usa `ctx['L']`. Necesita una regla para la ventana vacía (~1 % de los pasos, en que `see()` fallaría). Si la regla es «el más cercano fuera de la ventana», B = A salvo en el filtro de rechazo.
  - **C.** No escalar: la ronda 0 queda en 0.272 con L = 40 y nobj = 4.
- Recomiendo **A** (mínima y transparente), declarada como un cambio del carro de fábrica con su propio arnés. El director decide.

## SOLO en la pista escalada, N = 1 (`datos/carrera_humo_ronda0_SOLO_escalada_N1_20260922_131228.*`)
- R0 0.5154 / 0.4366: idéntico al SOLO anterior.
- **Fracción B+D del mundo por cuarto de T:** 0.911 / 0.914 / 0.905 / 0.883 (s=4001) y 0.883 / 0.918 / 0.906 / 0.914 (s=4002).
- Causas: 0–2 muertes de hambre; el resto veneno (≈43 %) y sal (≈57 %).

## Predicción mía refutada (declarada)
- En v1 escribí que el 86 % de B/D con 9 cuerpos era «el mundo se come la comida» por la competencia. **Falso.** Un cuerpo solo deja el mundo en ~90 % B/D: come A y C, el spawn repone un tipo al azar y B y D solo salen por olvido. La composición **no** distingue SOLO de carrera.
- Lo que sí distingue: con 9 cuerpos cada linaje muerde ≈40 % más B y D con las mismas A y C, y vive ≈3× menos. El mecanismo de eso **no está medido**.
- Consecuencia: el motivo escrito en la ENMIENDA 1 («la causa medida fue la escasez») venía de mi inferencia y no se sostiene. Escalar L y nobj mantiene la densidad por cuerpo, pero no cambia la composición. Sugiero corregir el texto (ERR nuevo, lo decide el coordinador).

## v3: opción A implementada, humo escalado y diagnóstico (22-sep, tarde)
**Veredicto v3: NO. Escalar la pista no devuelve el R0 del SOLO.** La predicción firmada (0.35–0.55) cae.

- **Opción A:** FABRICA toma `ctx['L']` y sigue viendo el mundo entero. Arnés **39/39**:
  - Los 35 de antes con los mismos números.
  - (K1) con N = 9 y L = 360 la boca decide sobre la celda real: 2455 decisiones, 0 desajustes.
  - (K2) determinista y contabilidad 9/9.
  - (L) el diagnóstico es solo lectura en 3 configuraciones.
  - Además, a T = 100000, el humo sin escalar con diagnóstico reproduce el 0.272 bit a bit.
- **Pasos sin ningún objeto a ≤ 20 celdas con N = 9:** mediana **4.4 %**, máximo 5.2 %. La estimación estática era 1.0 %: la medida es 4× mayor.

| 9 FABRICA, 4001–4002, T = 100000 | R0 por linaje (mediana, mín–máx) | R0 pista | B+D del mundo por cuarto de T | causas (veneno/sal) | vida | saciedad |
|---|---|---|---|---|---|---|
| **escalada** L = 360, nobj = 36 (`..._escalada_20260922_131931`) | **0.269** (0.219–0.322), 0/18 ≥ 0.9 | 0.267 / 0.268 | 0.853 / 0.850 / 0.854 / 0.855 · 0.837 / 0.862 / 0.850 / 0.842 | 42 % / 58 % (hambre 2, sed 0) | ≈192 | 0.45 |
| sin escalar L = 40 (`..._sin_escalar_diag_20260922_132544`) | 0.272 (0.234–0.359) | 0.268 / 0.288 | 0.863 / 0.868 / 0.871 / 0.862 · 0.846 / 0.858 / 0.868 / 0.860 | 44 % / 56 % | ≈185 | 0.45 |
| SOLO N = 1 (`..._SOLO_diag_20260922_133041`) | 0.5154 / 0.4366 | — | 0.911 / 0.914 / 0.905 / 0.883 · 0.883 / 0.918 / 0.906 / 0.914 | 43 % / 57 % | 600–646 | 0.55 |

**Diagnóstico** (solo medida, nada arreglado; mediana por linaje-semilla):
- Definiciones:
  - «Objetivo» = el objeto bueno más cercano para la necesidad activa (A con hambre, C con sed) al inicio del paso. Es un proxy: FABRICA en realidad va al objeto más cercano de cualquier tipo que no haya rechazado.
  - «Robo» = otro cuerpo lo muerde en ese paso.
  - Ventana = 50 pasos.

| | pérdidas de objetivo por 100k pasos (robo + olvido) | B/D en 50 pasos tras robo | tras olvido | tasa de base de B/D | A/C tras robo / base | distancia al bueno más cercano | pasos sin bueno en el mundo |
|---|---|---|---|---|---|---|---|
| SOLO | 0 + 16 | — | 1.01 | **0.42** | — / 0.57 | 10.2 | 83 % |
| 9, L = 40 | **3808** + 17 | 0.69 | 0.66 | **0.57** | 0.73 / 0.59 | 10.3 | 76 % |
| 9, L = 360 | **1612** + 6 | 0.59 | 0.60 | **0.57** | 0.40 / 0.58 | 61.6 | 7 % |

- **Lo medido:**
  - Rodeado de otros, un cuerpo muerde B/D a una tasa de base +36 % (0.57 contra 0.42), igual con o sin escala.
  - Pierde su objetivo bueno cientos de veces más a menudo (1600–3800 robos contra 16 olvidos).
  - Tras perderlo, sube su tasa de B/D (L = 40: 0.69 contra 0.57). Pero un robo no pesa más que un olvido (0.69 contra 0.66), y en L = 360 casi no hay efecto (0.59 contra 0.57).
  - La saciedad baja de 0.55 a 0.45.
- **Hipótesis, no medida:** robos frecuentes → más hambre → la boca, empujada por `hambre_boca`, muerde lo que tenga delante. Lo que queda sin medir es el vínculo hambre→B/D en el momento de morder.
- La distancia en L = 360 (61.6) no es comparable: allí casi siempre existe un bueno, pero lejos. En L = 40 muchas veces no existe ninguno (76–83 % de los pasos).
- **Observación de escala (no corregida):** el olvido es de 0.003 por paso para TODO el mundo, así que con nobj = 36 cada objeto se olvida 9× menos que en L = 40. La ENMIENDA 1 no lo escaló. Lo decide el coordinador.

## Comando de la serie de la ronda 0 (solo el coordinador)
`python experimentos/carrera_escuderias/juez.py --ronda 0 --desde 4003 --n 20 --pool 6`
- Valores por defecto: 9 FABRICA, `escala=1`, `pizarra=1`, `rep_acum=0`, `T=100000`.
- Tiempo: ≈180 s por semilla en un proceso. Son 4 tandas con Pool 6: **≈12–16 min**.
- La ruta con Pool no la probé (regla 3).

## Qué queda
- Decidir si la serie se corre así, dado que el humo ya cae por debajo de la predicción.
- Medir el vínculo hambre→B/D en el momento de morder.
- Decidir si el olvido se escala con N.

## v4: ERR-98 (olvido escalado), humo corregido y hambre → boca (22-sep, tarde)
**Veredicto v4: HAY ALGO MODESTO.** Con el olvido corregido, R0 por linaje sube de 0.269 a **0.349**. La predicción (0.35–0.55, sin reajustar) **no se cumple por muy poco**: 0.349 queda justo por debajo.

- **ERR-98:**
  - `esc` sorteos de olvido por paso (N con `escala=1`), cada uno con p = 0.003. La tasa por objeto queda igual que en L = 40, y con N = 1 hay un solo sorteo, como en el monolito.
  - Arnés **40/40**. Caso nuevo (M): tasa por objeto con N = 1 de 0.000742 y con N = 9 de 0.000767, razón 1.034, ambas a < 1.3 σ de 0.00075.
  - `test_tramposo` sigue 30/30.
- **Humo** (`datos/carrera_humo_ronda0_escalada_olvido98_20260922_134156.*`; 9 FABRICA, L = 360, nobj = 36, 4001–4002):
  - R0 por linaje mediana 0.349 (0.284–0.409), 0/18 ≥ 0.9; R0 de la pista 0.343 / 0.350.
  - Sin la corrección era 0.269; el SOLO da 0.5154 / 0.4366.
  - Vida ≈195 (SOLO 600–646).
  - B+D por cuarto de T: 0.818 / 0.841 / 0.829 / 0.834 y 0.820 / 0.832 / 0.841 / 0.834.
  - Causas: veneno 39 %, sal 61 %, 0 de hambre o sed.
  - Contabilidad 18/18. Hay 3.7 % de pasos sin ningún objeto a ≤ 20 celdas.
- **Hambre → boca.** Decisión = un paso sobre un objeto; déficit = el de la necesidad activa; H = manda el hambre, S = manda la sed.

| | SOLO (`..._SOLO_boca_*`) | 9 cuerpos, escalada |
|---|---|---|
| tasa de mordida de B con SED / con HAMBRE | 0.517 / 0.012 | **0.650** / 0.015 |
| tasa de mordida de D con HAMBRE / con SED | 0.109 / 0.063 | **0.196** / 0.073 |
| déficit al decidir sobre B con sed / D con hambre | 0.363 / 0.073 | **0.486 / 0.138** |
| déficit medio en mordidas B/D contra A/C | ~0.50 contra ~0.34 | **~0.60** contra ~0.28 |
| formato H-BOCA: veneno con SED · con HAMBRE · sal con HAMBRE · con SED | 701/1236 (0.57) · 109/7086 (0.015) · 742/5521 (0.13) · 130/1659 (0.08) | 8491/12272 (0.69) · 1164/59258 (0.02) · 9241/38254 (0.24) · 997/11120 (0.09) |
| mordidas B/D con un robo en los 50 pasos previos contra los pasos cubiertos así | — | 0.584 contra 0.560 (×1.04) |
| déficit en B/D con robo previo / sin robo previo | — | 0.604 / 0.585 |

- **Respuestas:**
  1. **Sí:** con 9 cuerpos las mordidas malas ocurren con más necesidad acumulada (déficit 0.60 contra 0.50), y los cuerpos llegan a las decisiones más necesitados (0.49 contra 0.36 con B y sed).
  2. **No:** los robos casi no anteceden a esos picos. Solo ×1.04 sobre el azar, con 0.02 más de déficit.
- **Relación con H-BOCA:** el mecanismo es el mismo que en la fase 10. La boca decide con la fila de la necesidad activa: el veneno se muerde con sed (la fila de la sed nunca aprende que B es malo) y la sal con hambre. Con 9 cuerpos, el término `hambre_boca·déficit` es mayor y esas tasas suben (0.57 → 0.69 y 0.13 → 0.24). Lo que la competencia añade es **necesidad acumulada**, no robos puntuales. De dónde sale esa necesidad (más distancia, menos saciedad) no está aislado.

## Comando final de la serie (solo el coordinador; usa ya ERR-98, porque `escala=1` es el valor por defecto)
`python experimentos/carrera_escuderias/juez.py --ronda 0 --desde 4003 --n 20 --pool 6`
- ≈195 s por semilla en un proceso (con Pools ajenos corriendo): 4 tandas → **≈13–17 min**.
- **Ruta con Pool NO corrida por mí.** Mis reglas duras prohíben cualquier Pool, también `--pool 2`. Verificado sin Pool:
  - `tarea` y su resultado se pueden pasar con pickle.
  - `juez` se importa limpio desde otra cwd.
  - La rama `imap_unordered` existe y el archivo tiene la guarda `__main__`.
  - Una tarea real (4003, T = 2000) da L = 360 y 56 olvidos (esperados ≈54).
- Prueba mínima para el coordinador: `python experimentos/carrera_escuderias/juez.py --ronda poolcheck --desde 4003 --n 2 --T 5000 --pool 2`.
