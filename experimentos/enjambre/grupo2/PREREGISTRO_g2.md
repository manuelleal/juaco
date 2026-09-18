# PREREGISTRO (borrador) — MINI-EQUIPO 2 (enjambre): M2, fisión de la vía lenta por conflicto de signo

Escrito el 18-sep-2026 por MINI-EQUIPO 2 tras el piloto de 3 semillas (§5). **Los números de §5 y §6 están
MEDIDOS (mini-prueba de un proceso, semillas 1-3, "humo" en el sentido del protocolo: no reemplaza una serie de
20 semillas nuevas con `Pool`). Todo lo de §4 es la predicción ORIGINAL del jefe de investigación, escrita ANTES
de correr.** No se recalibra ningún criterio después de ver los datos: donde el piloto contradice la predicción,
se declara contradicho, no se ajusta el umbral.

## 1. De dónde viene

Tronco v14.1 (`organismo/organismo_v14.py`) y el mundo de regla XOR de `experimentos/creacion_A`
(`organismo_v13q5.py`, control positivo con gradiente exacto: 1.000 en xor01 con los rasgos correctos
{P0,P1,P0·P1,1}, 0.562 con los rasgos cuadráticos del organismo). El cuello declarado el 18-sep es que el
organismo **no construye por sí mismo** el rasgo conjuntivo; el bloque A-4 movió las constantes de la vía lenta
(`eta_s` 0.15, `clip_s` 10) y llegó a 1.000 CON los rasgos dados, pero con rasgos propios sigue en 0.50-0.63.

## 2. Hipótesis (M2)

**H-M2.** El organismo ya tiene, en la vía RÁPIDA, un principio para crear estructura por conflicto de signo
(v11: `Wb[c]*R<0` divide una celda de Kenyon). La firma de XOR es un conflicto de signo por canal (el píxel 0 es
a veces comida y a veces veneno). Si la vía LENTA usa el MISMO principio —nacer una celda de dos canales cuando
un canal muestra ese conflicto—, el rasgo conjuntivo debería **construirse** en vez de elegirse de una base
cuadrática prefijada. Fuentes citadas por el jefe: Bicknell & Häusser 2021 (regla derivada, sólo señales locales,
resuelve feature-binding en dendritas); Moldwin, Kalmenson & Segev 2021 (clusterón: reagrupación sináptica por
plasticidad estructural local); Devaud et al. 2015 (el cuerpo fungiforme es necesario para negative patterning,
no para positive patterning: la representación configural es aguas arriba del lector).

## 3. Instrumento y memoria

- **Instrumento:** `experimentos/enjambre/grupo2/organismo_g2.py`, construido POR ANCLAS (`construye_grupo2.py`,
  5 anclas) desde `experimentos/creacion_A/organismo_v13q5.py` (`fae9c32b146fdbb4`, SOLO LEÍDO, sin editar).
  Perilla nueva: `fision=None|'conflicto'`, `fis_umbral=3.0`, `fis_rho=0.05`.
- **Identidad (perilla apagada), reportada ANTES de mirar números de M2:** `identidad_g2.py`, 3 reglas
  (xor01/px0/azar) × 3 semillas (1-3), T=30000, TODAS las claves del original comparadas
  (`fis_celdas`/`fis_ganadora`/`fis_n` excluidas por ser nuevas) →
  **`organismo_g2(fision=None) == organismo_v13q5: 9/9 IDÉNTICO`.**
- **Memoria de M2:** 6 celdas iniciales de un canal ({P_i,1}, 2 pesos c/u) que PUEDEN parir, como máximo una vez
  cada una (tope duro 6 hijas → máx. 12 celdas), una hija de dos canales ({P_i,P_j,P_i·P_j,1}, 4 pesos). Más 6
  contadores de masa por canal y signo (`_Fmp`,`_Fmn`) y una matriz 6×6 de sumas de patrones por signo
  (`_Fsp`,`_Fsn`) con sus contadores (`_Fcp`,`_Fcn`) — misma familia de estadístico que `err`/`mu` del tronco,
  indexada por canal en vez de por celda de Kenyon. Un error EMA por celda (`_FE`, inicializado en 1e9) decide
  cuál celda LEE la vía lenta (`_FG` = índice de menor `_FE`).
- **Regla local, verificada con el mismo código que corre dentro del organismo** (ver §6.3, `replay_coincide=True`
  en las 9 corridas): por mordida (P, R) — (a) por canal i con P_i=1, acumula masa/suma bajo el signo de R; (b)
  CADA celda existente actualiza con su propio residuo `d_c = R − W_c·a_c` (su propia base `a_c`) vía delta rule
  (`eta_s`, `clip_s`); (c) si un canal i (no parido, con cupo) cruza `fis_umbral` en AMBOS signos, nace una hija
  con j = el canal que más separa comida/veneno bajo i; (d) la vía lenta pasa a leer la celda de menor `_FE`.

## 4. Predicción numérica ORIGINAL (del jefe, antes de correr el piloto)

- xor01: acc_lenta mediana ≥ 0.75, ≥0.75 en ≥9/20 semillas nuevas (121-140); ganadora=(0,1) en ≥14/20.
- px0: acc_lenta = 1.000 en las tres reglas (control: el canal 0 no tiene conflicto en px0, así que NO debería
  parir, pero la ganadora debe seguir siendo el canal 0 con acc 1.000).
- azar: acc_lenta en [0.35, 0.65] (control negativo: ni demasiado alto ni demasiado bajo).
- n* (exposiciones hasta 0.75) ≤ 400; número de celdas ≤ 20 en las tres reglas.
- **Refutación explícita escrita por el jefe:** si nacen más de 20 celdas en azar, o la ganadora es (0,1) en
  menos de 12/20, M2 cae.

**Nota de diseño detectada en el piloto:** la propia especificación de M2 fija un **tope duro de 6 hijas** (una
por canal) → máximo 12 celdas SIEMPRE, en cualquier regla. El criterio "≤20 celdas" no puede violarse por
construcción; no discrimina nada (se reporta igual, en §5, pero no cuenta como evidencia).

## 5. Mini-prueba (MEDIDO): 3 semillas, T=100000

Un proceso, sin `Pool`. `mundo='regla'`, `puerta=3`, `constante=True`, `regla_lenta='delta_signo'`,
`lam_lenta=0`, `lectura='cuadratica'` (inerte: con `fision` activo cada celda lee su propia base fija, no
`phi(P)`), `eta_s=0.15`, `clip_s=10` (constantes de v14.1/A-4), `fis_umbral=3.0`, `fis_rho=0.05`. `acc_lenta` =
acierto balanceado por signo (`signo_acc`, la fórmula del registro) de `W_lenta_apriori` en la sonda a priori
(`t == fase2_en == T//2`) sobre los patrones NUNCA VISTOS. 91.5 s en total, 9 corridas.

| regla | semilla | acc_lenta | ganadora (fin de run) | fis_n | splits | celdas Kenyon | deaths | n_pre |
|---|---|---|---|---|---|---|---|---|
| xor01 | 1 | 0.500 | (0,1) | 12 | 33 | 63 | 115 | 257 |
| xor01 | 2 | 0.188 | (0,1) | 12 | 24 | 54 | 103 | 258 |
| xor01 | 3 | 0.313 | (0,1) | 12 | 43 | 73 | 110 | 275 |
| px0 | 1 | 1.000 | (0) | 11 | 30 | 60 | 116 | 253 |
| px0 | 2 | 1.000 | (0) | 11 | 23 | 53 | 131 | 283 |
| px0 | 3 | 1.000 | (0) | 11 | 26 | 56 | 149 | 300 |
| azar | 1 | 0.400 | (1) | 12 | 34 | 64 | 151 | 333 |
| azar | 2 | 0.800 | (5,2) | 12 | 29 | 59 | 140 | 298 |
| azar | 3 | 0.500 | (2,3) | 12 | 35 | 65 | 154 | 218 |

**Medianas (n=3, NO reemplaza 20 semillas):** xor01 = **0.313** (rango 0.188-0.500); px0 = **1.000** (3/3);
azar = **0.500** (rango 0.400-0.800).

**Exposiciones (n\*, replay externo de la MISMA regla sobre `lenta_eventos`, igual método que
`corre_xor_4.py`/`banco_lab.py`, rejilla 10..1500):**
- px0: n\*(≥0.75) = 10, 40, 20 (3/3 semillas alcanzan 0.75; mediana n\*=20).
- xor01: n\*(≥0.75) = ninguna semilla lo alcanza hasta n=1500 (0/3); tampoco ≥0.65 (0/3).
- azar: n\*(≥0.75) = 60 en la semilla 2 (1/3); las otras dos no alcanzan 0.75 ni 0.65 hasta n=1500.

**"¿Abre el rasgo conjuntivo?" (ganadora de DOS canales, al FINAL del run, t=T):** xor01 3/3, azar 2/3, px0 0/3
(correcto: el canal 0 de px0 no tiene conflicto de signo por diseño de la regla, así que no debe parir — y no
pare: `fis_n=11` en los tres, exactamente 6 iniciales + 5 hijas de los canales 1-5, nunca del canal 0).

## 6. Lo que el piloto CONFIRMA y lo que CONTRADICE de §4

1. **px0 = 1.000 en 3/3: CONFIRMADO exactamente**, incluida la razón estructural (canal 0 nunca pare).
2. **Ganadora=(0,1) en xor01: CONFIRMADO en 3/3** (piloto pequeño, pero 100% de tasa, y coherente con que la
   pareja (0,1) nace TEMPRANO: en la semilla 1, nace en el evento pre-sonda **#15 de 257** — no es un problema
   de que tarde en aparecer).
3. **azar no explota más de 20 celdas: CONFIRMADO**, pero de forma TRIVIAL (tope duro 12; ver nota de §4).
4. **acc_lenta mediana ≥0.75 en xor01: CONTRADICHO.** Mediana medida 0.313, y 0/3 semillas cruzan siquiera 0.65.
   Por la letra exacta de la cláusula de refutación del jefe (§4, "si... la ganadora es (0,1) en <12/20, M2
   cae"), M2 **no cae** todavía porque esa cláusula sólo habla de CUÁL celda gana, no de su acierto — pero el
   criterio numérico de accuracy, escrito en la misma sección, sí falla con claridad.
5. **azar en [0.35,0.65]: parcialmente contradicho** — 2/3 semillas caen dentro (0.400, 0.500) pero la semilla 2
   da 0.800 (por azar, la partición aleatoria de esa semilla resultó más separable por el par que ganó).

### 6.1 Diagnóstico del porqué (medido, no especulado): el piso `_FE=1e9` castiga a las hijas jóvenes

Se trazó la semilla 1 de xor01 evento por evento. La pareja (0,1) nace en el evento #15, pero en el evento #257
(la sonda) su error sigue en `_FE=4279` — Y las 6 celdas de un canal, vivas desde el evento 0, están TODAS
agrupadas en `_FE≈1884-1885`, con la ganadora en 1884.1. Con `fis_rho=0.05`, el piso inicial `1e9` decae como
`(0.95)^n`: en n=257, `(0.95)^257·1e9 ≈ 2630` — **del mismo orden que los `_FE` observados**. Es decir, a los
257 eventos NINGUNA celda ha "olvidado" su arranque en 1e9; y como las 6 originales lo vienen decayendo desde el
evento 0 mientras que la hija sólo lo decae desde el evento 15, la hija arrastra sistemáticamente MÁS piso
residual que las originales durante toda la ventana que importa para la sonda en T//2. Esto favorece a una
celda de un canal como ganadora en la sonda aunque la hija (0,1) ya sea, en sus propios pesos, la que mejor
resolvería XOR. Por el fin del run (t=100000, ≈550-600 eventos totales) el piso ya decayó lo suficiente
((0.95)^550 ≈ 1.7e-12) y la hija SÍ gana en 3/3 — coherente con `fis_ganadora=(0,1)` al final pero no en la
sonda. **Esto no es un fallo de esta implementación: reproduce exactamente lo que pide la especificación de M2
(`_FE=np.full(64,1e9)`); es una propiedad medida del mecanismo tal como está escrito.**

### 6.2 Verificación del replay externo

Las exposiciones se calcularon reproduciendo, FUERA del organismo, la misma regla de M2 sobre la secuencia
`lenta_eventos` (grabada con `lab=True`), igual método que `corre_xor_4.py`/`banco_lab.py`. Se verificó, en las
9 corridas, que el replay con TODOS los eventos pre-sonda reproduce el `acc_lenta` que el organismo calculó por
sí mismo en la sonda (`W_lenta_apriori`): **9/9 coinciden** (columna `replay_coincide_con_organismo` de
`mini_g2.json`).

## 7. Controles que pueden fallar (del jefe + lo que el piloto añade)

Los 6 del jefe siguen en pie (riesgo de flujo del replay, techo de 6/20 semillas sin una clase XOR, coste de
estructura sin medir en 20 semillas, etc.). **Nuevo, del piloto:** el piso `_FE=1e9` con `fis_rho=0.05` es,
medido, la causa más probable de que la sonda en T//2 no vea todavía a la hija ganar aunque ya nació y ya tiene
pesos razonables. No se tocó `fis_rho` ni `_FE` para "arreglarlo": el protocolo prohíbe recalibrar después de
ver datos. Se deja como hallazgo para que el coordinador decida (candidato a ERR si se preregistra una versión
2 de M2 con, por ejemplo, un contador de actualizaciones por celda en vez de un EMA compartido con piso fijo).

## 8. Cláusula de refutación (la del jefe, evaluada con el piloto)

"Si nacen más de 20 celdas en azar, o la ganadora es (0,1) en <12/20, M2 cae." — **Con 3 semillas no se puede
evaluar el umbral de 20 fracciones (12/20)**; el piloto no la refuta ni la confirma por sí solo. Lo que SÍ
mide el piloto, y que no estaba en la cláusula formal pero sí en la predicción numérica de la misma sección, es
que **el criterio de accuracy (mediana ≥0.75 en xor01) falla con margen amplio** (0.313 vs 0.75), con una causa
mecanicista identificada (§6.1), no ruido de semillas.

## 9. Recomendación

**No comprometer 20 semillas nuevas al criterio original tal cual.** El mecanismo SÍ hace lo que promete a nivel
estructural (construye el rasgo conjuntivo correcto, con señal puramente local, y lo hace temprano), que es la
parte más difícil y la razón por la que vale la pena seguir esta línea — pero el criterio de accuracy con el que
se prometió medirlo (sonda en T//2, ganadora por `_FE` con piso 1e9) no es todavía el instrumento correcto para
verlo. Antes de una serie confirmatoria de 20 semillas con `Pool`, sugiero al coordinador decidir entre: (a)
mover la sonda más tarde (no es gratis: cambia qué cuenta como "nunca visto" en el tiempo), o (b) preregistrar
una M2-v2 con una memoria de error que no dependa de un piso compartido en 1e9 (p. ej. contar actualizaciones
por celda y usar el promedio real, no un EMA con arranque enorme). Cualquiera de las dos es una decisión de
diseño nueva, no una recalibración del criterio actual — por eso no se hace aquí.

**`listo_para_preregistrar = false`** por la razón de §9, no por fallas de instrumento (identidad 9/9, replay
verificado 9/9) ni por errores de ejecución.
