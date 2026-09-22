# PREREGISTRO — BACTERIA C (carrera hacia la fase 10, 21-sep-2026 noche)

Misión: llegar a la AGI por este camino (organismo mínimo, reglas locales, sin retropropagación, peldaños
preregistrados con controles y réplicas). Carrera: acercar el organismo a la fase 10 — un linaje mortal que se
sostiene y acumula. Reglas de la nave: `experimentos/carrera_fase10/MISION.md`.

**Todo lo de este archivo está escrito ANTES de mirar un número de mis ejecuciones.** Lo único corrido antes es
el arnés del gemelo ajeno (`identidad_f9_rapido.py --T 4000`: 138/138, 12/12 controles difieren, ×45), que no
mide organismo sino instrumento.

---

## 0. Sesgo de partida y por qué lo corrijo antes de gastar CPU

Mi sesgo asignado era **linaje en ecología abierta**: varios cuerpos a la vez, herencia con variación, muerte
real, interacción por tres palancas, ningún guion. Lo mantengo como destino, pero lo pongo **después** del
diagnóstico, por una razón aritmética que se puede escribir antes de correr:

- Meter varios cuerpos en el mismo mundo **baja** R₀ (compiten por la misma comida). Si R₀ ≤ 0.5 con un cuerpo,
  con N cuerpos es peor. La competencia es un coste, no un regalo.
- M-1 pide R₀ ≥ 1. Sin sostén no hay linaje que sea abierto: no hay sobre qué seleccionar.

Así que el orden es: **(1) localizar el muro, (2) intentar cruzarlo con una herencia que nadie probó,
(3) sólo entonces la ecología.** Si los datos me dicen otra cosa, lo escribo en `BITACORA.md` y cambio.

## 1. Lo medido que uso como punto de partida (no lo repito)

- H-1 (18-sep, ×2): con muerte real, **heredar TODA la memoria no cambia nada**: R₀ 0.148 (nada), 0.160 (valores),
  0.153 (valores + tabla), 0.146 (barajado); inmortal 0.87–0.98. ERR-62.
- Fase 9 bloque 1 (21-sep): el nodo por relevancia viva lleva la vida de 94 → 598.5 (×6.37) y R₀ de 0.141 → 0.384
  (0.494 con `rep_acum=1`), con p1 0.962 y c1 1.0. **Ningún brazo cruza 0.9.**
- Fase 9 bloque 2: **ni el nodo ORÁCULO** (tabla verdadera) cruza R₀ 0.90 (0.508 / 0.557). *El muro es el mundo.*

**Lo que NINGÚN brazo ha heredado nunca.** En `organismo_f9.py`, dentro de `_nace`, está escrito literalmente:

    Wl[:]=_rh.uniform(.1,.4,(2,9)); el[:]=0; tr[:]=0   # la politica de locomocion NO se hereda en ningun brazo

`Wl` es la política de locomoción y **se aprende** (`Wl=np.clip(Wl+eta*(1+2*hambre)*(max(R,0)+Rp)*el,0,1.5)`,
con `Rp=0.2` por acercarse al objetivo). Todo lo heredado hasta hoy es **qué vale** (valor, tabla, nodo);
nunca **cómo llegar**. El encargo del mundo de la fase 10 pide exactamente esa disociación (§2.1.2: "saber dónde
vale tanto como saber qué"), y aquí sale gratis: el rasgo ya existe en el cuerpo.

## 2. Hipótesis

**H-C1 (diagnóstico).** El recién nacido que ya sabe qué comer (REL / ORÁCULO) sigue muriendo de hambre y sed,
no de veneno, y una parte no trivial de su vida se le va antes de su primera mordida buena.

**H-C2 (la apuesta).** El muro del linaje mortal es **motor**, no de valor: el hijo nace con patas al azar.
Heredar la política de locomoción del padre (con mutación pequeña) alarga la vida y sube R₀ por encima de lo que
compra cualquier herencia de valor.

**H-C3 (la conjunción, §2.1.2 del encargo).** Sólo los dos juntos: *valor sin patas* (REL, `hereda_wl=0`) y
*patas sin valor* (`NADA` + `hereda_wl=1`) quedan por debajo; `REL + hereda_wl=1` es el único que sube.

**H-C4 (ecología, condicional).** Si H-C2 se sostiene, `Wl` heredada **con mutación σ > 0** es un rasgo continuo
heredable bajo selección real (muerte y ventana de reproducción): es el mínimo linaje con variación, sin guion.

## 3. Mecanismo y memoria nueva

Instrumento `organismo_c.py`, construido por anclas por `construye_c.py` desde
`experimentos/nivel09_cuerpo_nuevo/organismo_f9.py` (`3a821884394d66c9`; cadena verificada hasta el tronco
congelado `organismo_v14.py` `feefc88b1fd8d434`). Nada de `organismo/` se toca. Perillas nuevas:

| perilla | 0 (apagada) | encendida |
|---|---|---|
| `hereda_wl` | `organismo_f9` BIT A BIT | 1 = el hijo nace con la `Wl` del padre congelada **en el parto** (no en la muerte); 2 = **BARAJADA**: las 9 columnas de `Wl` permutadas con rng propio `SEM_WL(seed)=880000+1000000*seed` (misma magnitud, entradas equivocadas) |
| `mut_wl` | 0.0 = copia exacta | σ > 0: ruido gaussiano N(0,σ) sobre la `Wl` heredada, rng propio `SEM_MUT(seed,k)=890000+1000000*seed+k`, recortado a [0, 1.5] (el mismo clip del aprendizaje) |
| `c_diag` | no aparece ninguna clave | medidas de **SOLO LECTURA** por cuerpo: pasos saciados, primer paso saciado desde el nacimiento, `|Wl|` al nacer y al morir, mordidas buenas/malas |

**Memoria nueva del organismo: CERO.** `Wl` ya existe y ya se aprende; el diccionario del parto (`_snap`) ya
existe. No se añade ninguna estructura que el cuerpo consulte para decidir. `c_diag` son contadores de lectura.

Ninguna inserción consume el rng del mundo (los rng nuevos son propios, en rangos libres 880000/890000; los
ocupados son 700000 hijo, 800000 baraja-herencia, 850000 alma, 860000 baraja-nodo, 870000 acceso).

## 4. Arnés (antes de mirar números)

`identidad_c.py`: con `hereda_wl=0` y `mut_wl=0` y `c_diag=0`, `organismo_c.run` debe ser **bit a bit**
(todas las claves, ida y vuelta por JSON) igual a `organismo_f9.run` en los 9 brazos × 2 niveles de `rep_acum`
del runner de la fase 9, más la cadena apagada (v14, v13, vivo, reproducción, CUELLO/CUELLO_MIN, muerte real
con vivo=0). **Controles que DEBEN diferir (≥ 7):** `hereda_wl=1 ≠ 0`; `hereda_wl=2 ≠ 1`; `mut_wl>0 ≠ mut_wl=0`;
`hereda_wl` con `muerte_real=0` es inerte (**debe ser idéntico**: es guardia, no control); `c_diag=1` añade
claves y no cambia ninguna vieja; semilla vecina difiere; `REL ≠ REC` sigue difiriendo; `NADA ≠ M1`.

## 5. Brazos (factorial 2×2 + controles)

Cuerpo idéntico al de la fase 9 (`corre_f9.CUERPO`: CUELLO_MIN + rep2 + h1 + muerte_real + dote 0.6). **No se
cambia ni una constante del mundo** (ERR-62 ya refutó las rampas de dote, umbral, objetos y coste).

| brazo | nodo | `hereda_wl` | papel |
|---|---|---|---|
| RENACE | — | — | ancla superior (inmortal subsidiado) |
| NADA | no | 0 | ancla inferior |
| REL | relevancia viva | 0 | el mejor de la fase 9: **valor sin patas** |
| WL | no | 1 | **patas sin valor** |
| REL_WL | relevancia viva | 1 | **los dos juntos** ← el candidato |
| REL_WLBAR | relevancia viva | 2 | control de CONTENIDO: misma magnitud, columnas permutadas |
| REL_WLMUT | relevancia viva | 1, σ = 0.05 | variación heredable pequeña |
| REL_WLMUTG | relevancia viva | 1, σ = 0.30 | dosis destructiva (debe caer) |

## 6. Predicción numérica FIRMADA (antes de la ejecución 1)

- **P-C0 (ancla).** Semillas 3201–3203, T = 100 000, `rep_acum=0`: R₀(NADA) ∈ [0.10, 0.22], vida(NADA) ∈ [90, 170],
  R₀(RENACE) ∈ [0.70, 1.40], R₀(REL) ∈ [0.28, 0.48], vida(REL) ∈ [300, 900]. **Prob. de acertar las cinco: 70 %.**
- **P-C1 (diagnóstico).** En REL, la mediana de `t_ok` ≥ 15 pasos, y las muertes se reparten entre hambre y sed
  (ninguna de las dos < 20 % del total): el cuerpo que ya sabe qué no comer muere por no conseguir recurso.
  **Prob. 75 %.**
- **P-C2 (la apuesta).** REL_WL frente a REL: vida mediana ≥ 1.30× y R₀ ≥ 1.25×, con A₁₂ pareado ≥ 0.75.
  **Prob. 45 %.**
- **P-C3 (el control que puede fallar).** REL_WLBAR ≤ 1.10 × REL en vida. Si REL_WLBAR iguala a REL_WL, lo
  heredado es MAGNITUD de movimiento y no política, y P-C2 queda **anulada**. **Prob. de que el control sea
  inerte (o sea, de que yo no me refute aquí): 55 %.**
- **P-C4 (M-1, contra mí mismo).** **Predigo que NINGÚN brazo mío cruza R₀ ≥ 1.0 en este mundo**, ni con herencia
  motora. Mejor brazo esperado con `rep_acum=1`: R₀ ∈ [0.45, 0.85]. **Prob. que le doy a cruzar 1.0: 15 %.**
  Lo firmo así a propósito: si P-C2 pasa y aun así no se cruza 1.0, el resultado que entrego es que el muro es
  la **tasa de reproducción** (ventana de 500 pasos seguidos + dote de 0.6+0.6 que casi mata al padre), no el
  conocimiento ni la locomoción.
- **P-C5 (M-2).** Con este mundo (4 patrones) la letra de M-2 (familia × variante × sitio) **no es medible**.
  Mido un **proxy declarado**: fracción de las 4 celdas útiles (A|hambre, C|sed correctas; B|hambre, D|sed
  rechazadas) resueltas **en el primer encuentro** por el cuerpo n del linaje, n = 1 contra n ≥ 5.
  Predicción: REL_WL gen ≥ 5 ≥ 1.8 × gen 1; REL_WLBAR ≤ 1.2 ×. **Prob. 40 %.**
- **P-C6 (M-3).** Sin puerta: reporto lo que aparezca y si se repite en otra semilla.

## 7. Qué me refuta

- P-C2: si A₁₂(vida REL_WL > REL) < 0.65 o la razón < 1.15, **la herencia motora no es el muro** y lo declaro.
- P-C3: si REL_WLBAR ≈ REL_WL, mi mecanismo no es contenido sino magnitud → P-C2 anulada aunque "gane".
- H-C3: si WL (patas sin valor) sube tanto como REL_WL, la conjunción es falsa y el nodo sobra.
- Si `hereda_wl=1` resulta **inerte** (ERR-38: mismos números que `hereda_wl=0`), la perilla no está conectada
  y no se lee nada.

## 8. Las cuatro trampas

1. **Canal simétrico:** no hay canal social aquí; el nodo del linaje es del cuerpo que MURIÓ al que NACE
   (asimétrico por construcción, ya auditado en la fase 9).
2. **Acierto sin balancear:** toda tasa va con su par. `p1` (rechaza lo malo) **nunca** se lee sin `c1` (sigue
   comiendo) ni sin la saciedad. Un cuerpo cauto sube p1, hunde c1 y se muere de hambre.
3. **El mundo que se come la comida:** se reportan exposiciones por estímulo en cada brazo; si un brazo ve
   menos comida que otro, la comparación de conducta no se lee.
4. **Sitios fijos:** el mundo del tronco sortea la posición de cada objeto al aparecer (`spawn`) y la posición
   del cuerpo al morir; no hay sitio memorizable. `Wl` no codifica posiciones absolutas: sus entradas son el
   patrón visto, el lado y "estoy encima" — por eso heredarla no es heredar un mapa de sitios.

## 9. Presupuesto y semillas

Hasta 10 ejecuciones, un proceso, sin `Pool`, ≤ 12 corridas y ≤ 300 000 pasos por ejecución. Semillas NUEVAS
**3201–3299** (verificadas libres con grep el 21-sep). Ejecución 1: 3201–3203. Réplicas: bloques siguientes.

## 10. Vocabulario

Permitido: *cuerpo, linaje, nodo del linaje, política de locomoción heredada, R₀ del linaje, ventana de
viabilidad*. **Prohibido sin la prueba:** población, generación (uso "cuerpo n del linaje"), evoluciona,
cultura, enseña, planifica, quiere.
