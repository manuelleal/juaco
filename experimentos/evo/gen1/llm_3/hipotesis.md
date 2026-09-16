# gen1 / llm_3 — REPASO por celda con puerta de edad (clase: REPASO / REHEARSAL)

**Operador:** LLM (Claude Fable 5.1). **Padre:** `experimentos/v10_direccion_division/organismo_v10m.py` (v10 = v9 + K5).
**Hijo:** `organismo.py` en esta carpeta. **12 líneas cambiadas** (métrica `lineas_cambiadas` de `evalua.py`): 12 añadidas, 0 quitadas.
Sin llamadas nuevas al RNG del organismo. Misma interfaz `run(...)` y mismas claves devueltas (`estado` no cambia de forma).
Escrito antes de evaluar. Sólo se hicieron las dos corridas de humo del final (§6).

## 1. Mecanismo

Cada celda de Kenyon guarda dos escalares propios además de `mu[c]` (que ya existía en el padre):
- `Rc[c]`: el **último R** recibido por una mordida cuyo código incluía a `c` (vale +1 o −3 una vez mordida).
- `tc[c]`: el **paso de la última mordida** que la activó (`T` = nunca).

Cada `R_REP = 50` pasos, si hay aprendizaje (`_ap`), se elige por turno (índice `_ir`, sin RNG) una celda activa que
(i) lleve más de `EDAD_REP = 5000` pasos sin ser mordida y (ii) tenga `mu[c]` no nulo. Esa celda **reconstruye su patrón
desde `mu[c]`** (sólo importa la dirección: `code()` es invariante a la escala), calcula el **código actual** de ese patrón
con la `KW` de hoy, y aplica **una** actualización Rescorla-Wagner sobre ese código con objetivo `Rc[c]`, tasa `eta/3`, con
el drenaje `lam` de la parte común (BUG-01). Sin morder, sin energía, sin RNG, sin tocar `err` ni `mu`, sin divisiones.
Al dividir, madre e hija se reinician (`tc = T`): no repasan hasta volver a ser mordidas.

Por qué así y no K4 ni K6 tal cual:
- **K6 (objetivo `3·(Wp[c]−Wn[c])`)** supone que las tres celdas del código reparten el valor por igual. En el compromiso
  que resuelve E2J/E2K y el bloque M (privada de B a −3, compartidas a 0, privada de D a +1) eso es falso: la privada
  enseñaría −9 y empujaría todo al techo (régimen BUG-01). `Rc` es acotado (+1 / −3) y no tiene ese problema.
- **`mu` contaminada (riesgo 3 de la ESPEC K6):** una celda que D está mordiendo está *fresca* y no repasa; sólo repasan
  las celdas que nadie ha mordido en 5000 pasos, y ésas no han visto el patrón nuevo, así que su `mu` apunta a su patrón
  viejo. La puerta de edad es lo que impide enseñar híbridos. El reinicio en la división cubre el caso de `mu` mezclada
  por dos patrones que compartían código (E2L): esas celdas se dividen y quedan reiniciadas.
- **Rigidez en E2 (riesgo 1):** tras la inversión, A se sigue mordiendo (fresca, no repasa); B se repasa a −3 sólo
  mientras ya vale −3 (`dlt = 0`, no-op); en cuanto B se muerde, `Rc = +1`, y si vuelve a envejecer, el repaso va en la
  dirección correcta. No se repasa lo que se está aprendiendo: no acelera E1 ni E2, a diferencia de K4.
- **K4 (almacén de pares patrón→R):** funciona (17–20/20) pero es un almacén externo y repasa también lo presente
  (muertes +6/+10 en M, un fallo de E2 con r=50). Aquí la traza es por celda, se reconstruye desde el prototipo que la
  celda ya tiene, y sólo se repasa lo que no se ha probado en mucho tiempo.

Tasa efectiva: en la ausencia del bloque M repasan las 6 celdas de A y B (3 cada uno; sin divisiones en la fase 1) y, a
ratos, las de C cuando ya se evita: por patrón, ~una actualización a `eta` cada 300–450 pasos, comparable a K4 r=100
(una a `eta` cada 400), que dio 20/20 en v9.

## 2. Hipótesis (una línea)

La memoria de A y B en la ausencia se conserva si las celdas que no se muerden re-enseñan cada pocos cientos de pasos su
último resultado al código actual de su prototipo; eso cierra la deriva de valor en las celdas compartidas y re-entrena a
las hijas que usurpan el código, sin frenar lo que se está aprendiendo.

## 3. Predicción numérica (semillas 1–10; refutación explícita)

| magnitud | padre (v10, `gen0/padre_train.json`, semillas 1–10) | predicción hijo | refuta si |
|---|---|---|---|
| `R` (W_B(100k) ≤ −2 y W_A(100k) ≥ 0.5) | 0.3 (3/10; retenidas 11–20: 0.4) | **≥ 0.8** | `R < 0.6` |
| mediana W_B(100k) / W_A(100k) | −1.23 / +0.88 | ≤ −2.7 / ≈ +1.0 | |
| guarda H3 (W_C ≤ −2.5 y W_D ≥ 0.85) | 10/10 | ≥ 9/10, W_D mediana ≥ 0.95 | < 8/10 (tira y afloja en las compartidas) |
| E2 (W_A→−3, W_B→+1, mordidas B Q4 ≥ 50) | 10/10 | ≥ 9/10; mordidas B Q4 dentro de ±15% del padre | ≥ 2/10 fallan (rigidez) |
| E1, E2I, E2J, E2K, E2L | 10/10 | ≥ 9/10 cada una | |
| CTRL (debe fallar) | falla 10/10 | falla 10/10 (con `plast=False`, `mu = 0`: el repaso nunca se activa; CTRL es idéntico al padre) | |
| celdas (H2) | ≤ 45 | ≤ 45; `splits_M` mediana ≤ 2 (padre 3.5) | |
| `S` (muertes E1) | 0.3625 (127.5 muertes) | 0.34–0.39 (igual al padre ± 5 muertes) | |
| `E` (divisiones E2L) | 3 → 0.667 | 3 → 0.667 (igual: en E2L las celdas están frescas hasta separarse) | |
| `C` | 0 | 12/15 = 0.8 | |
| retenidas 11–20 | 0.4 | ≥ 0.7 (nada se ajustó por semilla; la regla exige ≥ 0.3) | cae por debajo de 0.3 → "sobreajustado" |

Efectos secundarios esperados: (a) en E2 la reversión de A no se acelera ni se frena de forma medible (A se muerde, no
repasa); (b) en E2J/E2K el repaso de B a −3 sobre la celda compartida con D empuja a D a resolver por división o por celda
privada: W_D ≥ 0.8 igual que el padre, quizá una división más; (c) ningún efecto en E1 salvo repasos no-op de B.

## 4. Estado nuevo añadido (declarado con todas las letras)

`Rc` (90 flotantes), `tc` (90 enteros), `_ir` (un contador). Es una **traza episódica distribuida por celda**: un segundo
valor por celda (`Rc`) que **no sufre interferencia** (sólo lo sobreescribe una mordida que active a esa celda), más la
fecha de la última mordida. El patrón se reconstruye desde `mu[c]`, que ya existía. **La retención de A y B durante la
ausencia vive en (`mu`, `Rc`, `tc`) de sus celdas no mordidas, no en `Wp/Wn`: el repaso la copia a `Wp/Wn` cada ciclo.**
Comparado con K4: no hay almacén con n casillas ni patrones guardados; escala con las celdas mordidas, no con un n fijo
(relevante para el mundo de capacidad de la ESPEC K6). No se hereda por `estado_inicial` (arranca en "nunca mordida").

## 5. Qué lo haría pasar por la razón equivocada

1. **Retener por no aprender C y D.** Lo atrapa H3. Predicción explícita arriba (≥ 9/10).
2. **Retener por suprimir divisiones** (menos hijas, menos toma de código) y no por re-enseñanza. K4c mostró que esa vía
   sola se queda en ~9/20 (nivel `plast=False`). Señal: si `splits_M` cae a ~0 y `R ≈ 0.5`, el efecto es indirecto; si
   `R ≥ 0.8` con `splits_M > 0`, es la re-enseñanza.
3. **La memoria está en la traza, no en la consolidación.** Es así por construcción y queda declarado en §4. Controles que
   propongo (no corridos): (a) `tc[:] = T` en cada cambio de fase (análogo de K4c) — predigo caída al nivel del padre;
   (b) `EDAD_REP ≥ 50000` — sin efecto en M. Si (a) no cae, la memoria está en otra parte y hay que buscarla.
4. **Repaso oportuno frente a la sonda.** La sonda de 100k se toma antes de la primera mordida nueva; el repaso es continuo
   (cada 50 pasos desde ~55k), así que no infla la sonda más que a cualquier otro instante.
5. **Lo que el evaluador no mide y podría ocultar un coste:** `t90` de la reversión en E2 (sólo se mira el final), y las
   muertes en el bloque M (sólo se puntúan las de E1).

## 6. Humo (seed 1; las únicas dos corridas hechas)

- `run(1, T=20000, invertir_en=10000)`: W = A −2.45, B +1.00; mordidas B por cuarto [18, 4, 34, 37]; 24 muertes; 6
  divisiones (3 de B en 10745, 3 de A en 12111); 36 celdas; solap AB 0. La reversión ocurre (A aún bajando con sólo 10k
  pasos invertidos).
- `run(1, T=30000, fases={10000: C veneno + D comida; 20000: vuelven A y B})`: sonda 10k A +0.99, B −2.62; sonda 20k
  (fin de la ausencia) **A +1.00, B −2.77** (retiene; B más negativa que al inicio de la ausencia), C −2.44, D +0.55 con
  sólo 10k pasos de aprendizaje. Códigos de A `[10,18,28]` y B `[3,12,25]` **idénticos en 10k y 20k** aunque la celda 25
  la compartían C y D al entrar, que dividieron 4 veces y se fueron a hijas (C `[1,30,32]`, D `[30,31,33]`). Final 30k:
  A +1.00, B −2.85, C −3.07, D +0.78; 38 muertes; 34 celdas.
