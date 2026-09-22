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

## Qué queda
- Decidir A/B/C y, con esa decisión, correr el humo escalado de la ronda 0 contra la predicción 0.35–0.55.
- Medir por qué un cuerpo rodeado de otros muerde más B y D, antes de la ronda 1.
- Gemelo numba: plan sin cambios (v1). Solo sirve para carros de fábrica.
