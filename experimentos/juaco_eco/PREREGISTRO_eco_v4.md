# PREREGISTRO — JUACO-ECO v4: EL PAQUETE enseñar (herencia) + interruptor, en los mundos de v3 (24-sep-2026, coordinador de la nube; antes de cualquier serie)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/juaco_eco/`. Nivel 10, frente 2. Aprobado por el director (~17:00 UTC):
*"sí, abre el paquete de enseñar + herencia + interruptor"*. Archivos nuevos; nada del PC se toca; el Frankenstein se importa sin tocarlo.

## 0. Qué se corrigió de la propuesta ANTES de escribir esto (se le dice al director)
- **Enseñar y herencia son el MISMO órgano.** `ensena` de ECO v2/v2.1 (`carros/FAMB_ORG_ECO.py`:258, "el padre pasa la tabla") y
  `herencia` del Frankenstein (`experimentos/frankenstein/organismo_frankenstein.py`:66 y 230, "subida_n10b modo 'res' (verbatim)") son el
  órgano de subida_n10b implementado en dos carros. El paquete queda en **dos órganos: herencia (= enseñar) + interruptor**.
- **"Partir de los genomas ya seleccionados" se retira.** `motor_eco3` no tiene un gancho para sembrar a los fundadores con genomas de
  otro banco (su `donante` es padre o azar); los bancos de v2.1 son de otro cuerpo (FAMB, 20 genes); y sembrar con los órganos prendidos
  cambiaría la nula de O1\*/O2 (que supone órganos que nacen apagados). Construirlo con arnés cuesta más de lo que aporta hoy. Todo nace de
  fábrica, como en v2.1 y v3.

## 1. Instrumento (sha a 16)
- Motor `motor_eco3.py` (2eec9830792d9822) + `carros/FRANK_ECO.py` (92a22cbd1fe314c3) + `organismo_frankenstein.py` (baff124177d44e90),
  sin tocar (arnés `identidad_eco_frank.py` 9/9). Python: el Frankenstein no tiene gemelo.
- Runner `corre_eco_v4.py` (**9c059741accd0489**) = `corre_eco_v3.py` (7bb44da802508b37) con tres cambios y nada más:
  (a) sólo MUTAN las 18 perillas + `herencia` + `interruptor` (el parámetro `mutables` de motor_eco3, igual en VIDA y AZAR); los 5 órganos
  FIJOS (`b5`, `mapa`, `curiosidad`, `modelo`, `lenta`) quedan en 0.9, apagados, en el genoma real y en las 8 sombras;
  (b) los DOS mundos de v3, **w30** (esc 30, 30 fundadores) y **w9** (esc 9, 9 fundadores), tope 3 000. *Se pensó en w90 (el de v2.1,
  donde la selección fue más fuerte), pero el primer arnés midió el costo del Frankenstein en Python ahí: ~19 ms por paso con ~100 cuerpos,
  unas 12 h por serie con Pool 3. En w30 + w9, v3 tardó 80 min por serie. El cambio se hizo antes de cualquier serie; no hay datos de v4.*;
  (c) la letra del paquete (§6).
- Arnés `identidad_eco_v4.py`, 20 comprobaciones: (M) constantes; (T) ×4 medidas a mano en w30 y w9, VIDA y AZAR, con el motor
  informando como mutables EXACTAMENTE los 20 y los fijos apagados; (K) la mutación alcanza a los 2 del paquete y a ninguno de los 5 fijos
  (real y 8 sombras en 0.0); (S) la expresión del corte sale del checkpoint y coincide con el banco del motor; (V) ×11 la letra; (R) ×2
  banderas. Primera versión (w90; runner 9c059741accd0489, arnés 8d2da40f7b4db8a4): 18/18. **Versión que corre: §9.**

## 2. Pregunta
¿La selección **arma el paquete**? ¿Prende a la vez el órgano de enseñar y el interruptor (explorar/explotar por necesidad) en un mismo
mundo, cuando son los únicos órganos que puede prender? Es una ablación de v3: los mismos mundos, sin los 5 órganos que la selección tiraba
o dejaba neutros.

**Datos vistos antes de escribir esto (declarados):** ECO v2.1 (`ensena` ELEGIDO en w90 ×2: O1\* 20/20 y 20/20, O2 20/20 y 18/20); ECO v3
(`herencia` en w30: O1\* 19 y 16/20, O2 14 y 14/20; `interruptor`: w9 "sube" y ELEGIDO, w30 11/11 y 14/14). Las predicciones salen de ahí.

## 3. Diseño
- Igual que v3: vivero con banco de 200 y 8 sombras, mutación (p 0.05, σ 0.15), corte en 60 000, T = 120 000, brazos VIDA (selección) y
  AZAR (deriva: el banco guarda el genoma NUEVO, `motor_eco3.py`:438 y 477), salvo lo de §1.
- **Semillas nuevas** (grep del 24-sep: sin usos 20310–20399): serie **20311–20330**, réplica **20331–20350**; práctica 20391–20399
  (humo 20396, prueba del Pool 20397–20398, arnés 20398–20399).

## 4. Medidas
Por órgano del paquete, en el banco del corte: O1\* (fracción que expresa en el real contra la media de sus 8 sombras, del checkpoint), O2
(fracción en VIDA contra AZAR, pareado por semilla); vivos en T con el órgano. Descriptivo: perillas seleccionadas, persistencia en T.

## 5. Predicciones firmadas
| cantidad | rango | probabilidad |
|---|---|---|
| `herencia` ELEGIDO en w30 (v3: O1\* 19 y 16, O2 14 y 14) | O1\* 15–20, O2 12–18 | 0.45 |
| `interruptor` ELEGIDO en w9 (v3: 17/12 y 15/15) | O1\* 12–19, O2 11–17 | 0.45 |
| `interruptor` ELEGIDO en w30 — **la que decide FUNCIONA** | O1\* 8–17 | 0.25 |
| `herencia` ELEGIDO en w9 (v3: 6/4 y 10/6) | O1\* 4–12 | 0.10 |
| guardia de AZAR disparada | — | 0.05 |
| veredicto | FUNCIONA 0.15 · MODESTO 0.55 · NO 0.25 · NO EVALUABLE 0.05 | — |

## 6. Criterio por la letra (`corre_eco_v4.veredicto`; se imprime al final)
Por órgano g del paquete y mundo m (20 semillas): **ELEGIDO** = O1\* ≥ 15/20 **y** O2 ≥ 15/20 (estrictos); "sube" = uno de los dos.
- **NO EVALUABLE:** serie incompleta; bloqueados > 0; un órgano FIJO expresado en algún banco o vivo; AZAR con > 8/20 en algún gen (media
  contra sombras) o con ≥ 15/20 de expresión sobre sombras en un órgano del paquete.
- **FUNCIONA — LA SELECCIÓN ARMA EL PAQUETE:** `herencia` e `interruptor` ELEGIDOS en un MISMO mundo.
- **HAY ALGO MODESTO:** alguno de los dos ELEGIDO en algún mundo, o los dos "suben" en un mismo mundo.
- **NO:** otro caso.
El bloque se declara sólo si serie y réplica dan el mismo veredicto; si no, vale el menor.
Vocabulario: «la selección arma/prende el paquete», «linaje», «cuerpos vivos (N = …)»; prohibido «evoluciona», «especie», «cultura».

## 7. Qué refuta
- **H (la selección arma el paquete):** no hay un mundo con los dos ELEGIDOS. **H-herencia** (el órgano de enseñar se prende también en
  el cuerpo del Frankenstein): `herencia` no queda ELEGIDO en w30.
- **El instrumento:** guardia de AZAR, o un órgano fijo expresado.

## 8. Auditoría propia (antes de correr)
1. **Herencia = ensena:** si `herencia` sale ELEGIDO, es la REPLICACIÓN de v2.1 en otro cuerpo, no algo nuevo. Lo nuevo es el
   interruptor y el par.
2. **Cinco órganos fijos:** en AZAR la deriva sólo prende `herencia` e `interruptor`; para esos dos la nula es la de v3 (~0.4 por semilla
   para O1\*; P(≥ 15/20) ≈ 1e−3).
3. **O2 conservador:** AZAR prende órganos por deriva sin filtro (v3 §7.6); O2 queda sesgado en contra de VIDA.
4. **Corrección de una nota mía (bitácora, 15:40):** escribí que en AZAR "el banco también lo llenan padres que se reprodujeron, así que no
   es deriva pura". Es falso: en AZAR el banco guarda el genoma NUEVO del hijo, sacado al azar del banco (`motor_eco3.py`:438 y 477); es
   deriva pura. El 14/20 de AZAR en w30 de la réplica de v2.1 es azar (P ≈ 0.02 por prueba, entre ~12 pruebas de AZAR). Corregido en la
   bitácora.
5. **Epistasis:** el interruptor podría servir sólo con la herencia prendida; la letra pide los dos en el mismo mundo; la co-expresión por
   semilla queda en los JSON (descriptivo, no decide).
6. **Tope:** el Frankenstein en w30 llegó a 97 vivos (v3). Tope 3 000: lejos. A T = 120 000 ningún linaje se acerca a los 100 000 cuerpos
   de la guardia de ERR-60 (la que colgó ECO v1.2 a T = 1e6: nube-9). Si un trabajo muriera así, el Pool se colgaría en silencio: los
   check-ins de la cola lo vigilan.
7. **Ablación de v3, no réplica:** mismos mundos y misma letra por órgano; cambia que sólo mutan 2 órganos. Si sale igual que v3, los 5
   órganos quitados no pesaban; si cambia, pesaban.

## 9. Arnés y costo (completado ANTES de la serie, 24-sep ~17:40 UTC)
- Runner **`corre_eco_v4.py` f7ba5d77cfd7f725** (w30 + w9) y arnés **`identidad_eco_v4.py` cebaba9218a5cbe4: 20/20** (58 s; salida en
  `identidad_eco_v4_salida.txt`). (K) en AZAR w30 a T 12 000: (paquete real + suma de sombras: {'herencia': 1.065, 'interruptor': 0.86}; nacidos 149, 37.3 s); los 5 fijos en 0.0 en el real y en las 8 sombras.
- Costo: como v3 (80 min por serie con Pool 3 en w30 + w9); serie y réplica ~2 h 40 min. La primera versión en w90 costaba ~6× por paso
  (T 3 000: 47 s contra 8 s en w30).

## 10. Puntos
Ninguno declarado aquí; los decide el director.
