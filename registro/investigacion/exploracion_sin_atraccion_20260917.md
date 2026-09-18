# Exploración sin atracción: mecanismos locales para el canje del mapa (nivel 8)

**17 sep 2026. Investigación web (2010–2026 y clásicos), sin correr ni editar nada (regla 8 de `EQUIPO.md`). Rol
investigador. Contexto:** el canje explotación/exploración de `M` sigue abierto tras dos candidatos refutados
(curiosidad por progreso; novedad de sitio, dosis 0.6 y 1.8) por un problema de **escala**: `valor()` de un patrón
veneno aprendido llega a `≈ −3` (indexado por PATRÓN en `Wp`/`Wn`, no por sitio) y ninguna atracción de `+0.6…+1.8`
lo compensa sin cobrar comida; además la suma de hasta `H_M=20` términos descontados en `_sesgo_M()` **crece con
cada sitio-veneno cercano que `M` recuerda** (hasta 8 sitios posibles), así que el desbalance puede ser peor que "un
−3 contra un +0.6". Dato de arquitectura clave: `valor()` sólo cambia al MORDER; pisar sin morder actualiza
`_Mpat`/`_Mset` pero no lo aprendido — un mecanismo que "no toque el aprendizaje" (como se exigió en novedad de
sitio) sólo puede cambiar CUÁNTO CUENTA `M`, no CUÁNTO VALE lo recordado.

## 1. Habituación / olvido del valor recordado en ausencia
Exige un reloj de última confirmación por posición y un apagado. JUACO ya tiene ambas piezas: `t_visita[pos]`
(preregistrado en novedad de sitio) y el precedente v9 (`memoria_rechazo=20`, confirmado en tronco: "no es objetivo
por N pasos"). Regla local mínima: si `t − t_visita[pos] > tau_olvido`, `_Mset[pos] = False` — el sitio deja de
sumar en `_sesgo_M()`, sin `gamma` nuevo. Predicción (`mundo_largo.py`, 20 semillas nuevas, `tau_olvido=T_nuevo=4000`):
brazo `MAPA_OLVIDO` solo, adquisición (≤30 vistos) mediana ≈ 0.78 [0.72–0.84] (no pasa P1 solo) pero comida Q4
≥ 0.98× MAPA en ≥17/20 (pasa P2 con más margen que cualquier dosis de novedad). Combinado `+NOV(0.6)` (la dosis
barata ya preregistrada, no la 1.8 cerrada por la enmienda 1): adquisición mediana ≥ 0.85 y comida ≥ 0.95× MAPA en
≥15/20 — donde la dosis 1.8 sola sólo llegó a 9/20. Riesgo: una perilla (`tau_olvido`) sin barrer; corta = converge
a V13 y pierde la comida; larga = no se distingue de MAPA.

## 2. Saturación / normalización del valor en la lectura
Exige acotar `_sesgo_M()` para que ningún número de sitios-veneno recordados supere lo que aporta un solo
sitio-comida. Extremo "signo, no magnitud": `gamma_M · signo([_bi,_bd])`. Suave (divisiva, Louie–Khaw–Glimcher):
`_bi/(σ+|_bi|+|_bd|)`. Es el cambio más barato de los cinco: función de dos números ya calculados, cero memoria
nueva en las 40 posiciones. Predicción (forma signo): adquisición mediana ≈ 0.75–0.80 sola (mismo techo que (1):
tampoco atrae activamente) pero comida Q4 ≥ 0.95× MAPA (el signo del sesgo no cambia; lo que deja de pasar es que
3–4 venenos cercanos sumen a −8 o más). Riesgo: pierde toda la información de distancia (1 paso pesa igual que 20);
puede sobre-frenar cerca y no distinguir lejos — medirlo con equilibrio de visitas, no sólo adquisición.

## 3. Optimismo ante lo incierto, con escala acotada
Exige NO sumar un bono creciente (misma familia que "novedad", ya refutada) sino MULTIPLICAR la confianza en cada
entrada de `M` por evidencia acumulada: reusar `n_visitas[pos]` (ya existe, sólo lectura) y pesar el término por
`min(1, n_visitas[pos]/n0)` — un solo mordisco pesa poco hasta confirmarse. Cabe como regla local (contador ya
existente). Predicción (`n0=2`): adquisición mediana ≈ 0.74–0.79 sola; comida Q4 ≈ MAPA (no toca el signo). Riesgo:
el más alto de quedar en NO-OP — **paradoja de exposición**: confirmar exige acercarse, y acercarse es justo lo que
el mapa impide (mismo problema que en 5).

## 4. Forrajeo bajo incertidumbre: teorema del valor marginal / giving-up density
El "parche" de JUACO no es multi-mordida, así que MVT no dicta cuándo IRSE sino cuándo vale la pena la DESVIACIÓN
hacia un sitio viejo: sólo si el costo esperado es menor que la tasa de recompensa propia `ρ` (EMA de `R` por paso,
un escalar único, más barato que cualquier cosa por posición). Cabe como regla local (global, no por posición):
`gamma_M` deja de ser constante y se modula por `ρ`. Predicción: efecto pequeño y distinto en forma — adquisición
mediana ≈ 0.70–0.72 (≈ MAPA, no pasa P1 solo) pero el rango intercuartílico entre semillas se estrecha (≤0.7× el de
MAPA), porque el sesgo queda atado a la historia de cada semilla. Riesgo: el más débil de los cinco solo; sirve como
ajuste fino sobre (1) o (2), no como candidato único.

## 5. Lo que hacen los roedores con lugares que fueron peligrosos: extinción del miedo contextual
La extinción no borra el valor: es aprendizaje NUEVO, específico de contexto, que compite con el original, y sólo
ocurre con EXPOSICIÓN repetida — nunca sólo con el paso del tiempo. Por la arquitectura de JUACO (§0) esto exige
tocar `Wp`/`Wn` al RECHAZAR, no sólo al morder: la única de las cinco que rompe la promesa de "no tocar el
aprendizaje", y la más cercana a lo que v9 (`_rech`) ya hace a corto plazo sin tocarlo. Predicción (brazo
exploratorio, no decisorio por regla 4): `Wn −= lam_ext·(Wn>0)` en cada rechazo sobre sitio conocido (`lam_ext=0.02
< lam=0.05`, a propósito, para no repetir la escalada que la enmienda 1 ya cerró), adquisición mediana ≈ 0.80–0.86 y
comida Q4 ≈ 0.85–0.90× MAPA (paga más que (1)–(2): sí se acerca lo suficiente para varias mordidas de confirmación),
con recuperación gradual en cientos de pasos y recaída rápida si el sitio vuelve a ser veneno (como la renovación
del miedo fuera de contexto). Riesgo: el más peligroso para regla 6 (parece que el organismo "decide" exponerse) y
comparte la paradoja de exposición de (3).

## Mecanismo → mínimo cambio → predicción → riesgo

| mecanismo | mínimo cambio en JUACO | predicción (adq. ≤30 / comida Q4) | riesgo principal |
|---|---|---|---|
| 1. Olvido de `M` | `_Mset[pos]=False` si `t−t_visita>4000` | 0.78 sola / ≥0.98×MAPA · **+NOV(0.6): ≥0.85 / ≥0.95×MAPA** | `tau_olvido` sin barrer |
| 2. Normalización | `_sesgo_M` → signo o entre Σ\|·\| | 0.75–0.80 / ≥0.95×MAPA | pierde información de distancia |
| 3. Confianza por evidencia | pesar por `min(1,n_visitas/n0)` | 0.74–0.79 / ≈MAPA | paradoja de exposición (NO-OP) |
| 4. Umbral tipo MVT (`ρ`) | `gamma_M` modulado por EMA de `R` | 0.70–0.72 / ≈MAPA, menos varianza | demasiado débil solo |
| 5. Extinción contextual | `Wn` decae al rechazar (toca aprendizaje) | 0.80–0.86 / 0.85–0.90×MAPA, con recaída | infla vocabulario; paradoja de exposición |

## Tres fuentes más útiles

- Bracis, Gurarie, Van Moorter & Goodwin (2015), "Memory Effects on Movement Behavior in Animal Foraging," PLOS ONE
  10(8):e0136057 — decaimiento exponencial de memoria en forrajeo (mecanismo 1).
  https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0136057
- Louie, Khaw & Glimcher (2013), "Normalization is a general neural mechanism for context-dependent decision
  making," PNAS 110(15):6139–6144 — fórmula de normalización divisiva del valor (mecanismo 2), trasladable a
  `_sesgo_M()`. https://pmc.ncbi.nlm.nih.gov/articles/PMC3625302/
- Niv, Daw, Joel & Dayan (2007), "Tonic dopamine: opportunity costs and the control of response vigor,"
  Psychopharmacology 191:507–520 — ata el umbral de MVT a un escalar local `ρ` (mecanismo 4).
  https://pubmed.ncbi.nlm.nih.gov/17031711/
