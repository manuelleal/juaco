# PREREGISTRO — C-P6: N2 POR PREDICCIÓN en el mundo mínimo decidible. ¿Aprende el receptor, o sólo obedece?

**Escrito ANTES de correr la serie, 18 sep 2026. Creador C, encargo del coordinador.** 20 semillas no cierran un nivel
del brief: cierran o refutan **este** mecanismo. Nada se declara sin que el coordinador lo corra, lo replique y lo
registre.

---

## 1. Pregunta única

> **Un receptor que aprende, con su propio cuerpo, QUÉ VA A SENTIR cuando el emisor muerde o rechaza, ¿se queda con
> lo aprendido cuando el emisor calla — o sólo estaba obedeciendo?**

El registro ya sabe que con la escala **innata** el receptor de N3d **obedece y no aprende** (mudo 0.503). Aquí el
significado **no se da**: se aprende. La pregunta es si eso cambia la retención.

## 2. Mecanismo (2 escalares de memoria)

```
u[c]  = lo que el receptor PREDICE que va a SENTIR cuando la conducta ajena sobre ese patron fue c (0 rechaza, 1 muerde)
al MORDER un patron del que oyo c hace <= tau_pred:   u[c] <- u[c] + eta_sym * (E_VAL[valencia] - u[c])
al OIR c sobre un patron, SIN morderlo:               R_hat = (R_VAL/E_VAL) * u[c]   y aprende el valor con factor gamma_pred
```
Las constantes de conversión son las **del mundo** (+0.8→+1.0, −0.4→−3.0): **ningún parámetro libre**. Puerta opcional
`theta_a` (no escuchar si ya sabe). `eta_sym = 0.05`, `gamma_pred = 1/3 = f_vicaria` de N3d, `tau_pred = 400`.

## 3. Instrumento y mundo

`experimentos/creacion_C/mundo_social_pred.py` (sha `277b6978ad47a492`), **por anclas** desde
`experimentos/etapa5_comunicacion/mundo_social_n3.py` (`ef227f833c5bf46a`, sólo se lee), constructor
`construye_n2pred.py`. Selección de patrones: `experimentos/creacion_C/mundo_vd.py` (sha `d670fd65c53e4310`).

**El mundo mínimo decidible (corrige ERR-32, y usa los arreglos de ERR-33 y ERR-34):**
- **8 objetos con las 8 vistas del receptor TODAS DISTINTAS**, emparejados sobre el cubo Q3 a distancia de Hamming 1,
  4 comida / 4 veneno, `px0` (la regla) bajo la máscara del receptor. **Hay dónde escribir** lo aprendido — que es lo
  que N3d hacía imposible (ERR-32: los dos miembros de cada pareja tenían la misma retina enmascarada).
- **`regen_en_fijos = True` (ERR-33):** el flujo (`regen_rota`, `vida = 100`) sortea **dentro** del conjunto fijo. Sin
  esto, `regen_rota` descartaba `tipos_fijos` y el montaje se destruía.
- **`nobj_total = 8` (ERR-34):** **todos** los brazos ven el mismo número de objetos. Sin esto, `nobj = nobj_por_org·n`
  hacía que la línea base (n = 1) viera 4 objetos y los brazos sociales (n = 2) vieran 8.
- Resto como N3d: `regla = px0`, máscaras MR `[0,0,0,1,1,1]` / ME `[1,1,1,0,0,0]`, `regen = 50`, `d_senal = 5`,
  sólo el receptor escucha (`escucha = False` en el emisor), acierto **balanceado** (`acierto_q4` de `corre_N3d.py`,
  copiada literal). **T = 200 000**, mudo desde **T/2**. **Semillas 121–140** (nuevas).

**Identidades** (`identidad_n2pred.py`, las SIETE condiciones de N3d × 3 semillas, T = 20 000, todas las claves de los
n organismos): **L1 21/21** (perillas apagadas ≡ original) · **L2 21/21** (la sonda de exposiciones sólo lee) ·
**L3 21/21** (`u[c]` aprendiéndose sin usarse). Las perillas de montaje nuevas están **apagadas** en L1–L3.

## 4. Brazos

| brazo | qué es |
|---|---|
| **N0** | dos organismos, mismo mundo, **sin canal**. **Es la línea base** (SOLO_R tiene n = 1 y otro flujo de azar del mundo) |
| SOLO_R | el receptor solo, n = 1. Línea base secundaria, se informa |
| **INNATO** | N3d tal cual: la conducta ajena se traduce a R = +1 / −3 **por construcción** |
| **PRED** | **la hipótesis**: `u[c]` aprendido con el propio cuerpo |
| SHUF | control: emisor barajado (la conducta no informa) |
| SACIEDAD | control: emisor que no sabe (`alpha = 0`) |

Cada brazo se corre **dos veces**: con el emisor hablando todo el rato y con **`mudo_desde = T/2`**.

## 5. Predicción numérica (escrita antes; entre paréntesis, el humo de diseño en semillas 1–3, T = 100 000, declarado)

- **N6 [PRINCIPAL — ¿aprende o obedece?]** con el emisor **mudo** desde T/2, mediana de `acierto_q4` de **PRED ≥ 0.65
  y ≥ mediana(N0) + 0.10**, y pareado (PRED mudo > N0) en **≥ 14/20**. *(humo: **0.996** contra N0 0.712)*.
- **N6b [y digo antes que discrepo del pronóstico del coordinador]** **INNATO también retiene**: su mediana muda
  **≥ 0.65**. *(humo: 0.978)*. En este mundo los dos escriben en códigos distintos, así que la retención no es lo que
  los separa; lo que los separa es que PRED **se ganó** el significado. **Si INNATO cae a ≈ 0.50 y PRED no, ése es el
  resultado grande y se registra como tal** — y mi lectura de por qué estaba mal.
- **N1 [aprende el significado]** `u[1] ≥ +0.5` y `u[0] ≤ −0.15` en **≥ 15/20**. *(humo: 0.798–0.800 y −0.264…−0.334)*.
- **N2′ [menos mordidas]** mediana de `mord_crit` de PRED **≤ 0.70 ×** la de N0, pareado ≥ 14/20. **Cláusula de
  censura (la que me faltó dos veces):** una semilla en la que un brazo **no alcanza** el criterio cuenta como **peor**
  que cualquier valor finito, nunca se salta. *(humo: PRED [129, 110, 96] contra N0 [510, 153, 89] → 2/3)*.
- **N3 [con canal no es peor que el innato]** mediana de `acierto_q4` de PRED **≥ 0.85** y **≥ INNATO − 0.10**.
  *(humo: 0.970 contra 0.991)*.
- **N4 [los controles caen]** SHUF y SACIEDAD **no superan a N0** mientras el emisor habla (≤ N0 + 0.02) **y**
  `u[1] − u[0] ≤ 0.3`, en **≥ 18/20**. *(humo SHUF: 0.697 contra N0 0.712, y `u[1]−u[0]` = −0.72 / −0.97 / −0.75:
  el canal barajado no sólo no informa, **estorba**)*.
- **N5 [cuánto cuesta el significado]** mediana de `mord_crit` de PRED **≥** la de INNATO. Es el número que el brazo
  innato no puede dar. *(humo: [129, 110, 96] contra [105, 74, 122] → 2/3)*.

## 6. Guardas de validez (se miran ANTES; si una cae, el contraste es nulo y va ERR numerado)

- **G-a [identidades]** L1, L2, L3 al 100 % **dentro del runner**; si no, aborta.
- **G-b [K3, los patrones fluyen]** los **8** objetos presentes en Q4 en **todos** los brazos, ≥ 18/20 semillas.
  *(humo: 8/8 en los cinco brazos)*. Es la puerta que mató dos de mis cuatro montajes.
- **G-c [banda de la línea base]** mediana de `acierto_q4` de **N0 en [0.60, 0.85]**. Por debajo, el mundo es
  imposible (ERR-32) y sólo mide obediencia; por encima, la línea base lo resuelve sola y el canal no puede aportar.
  *(humo: N0 0.712, SOLO_R 0.747)*. **Esta guarda es el resultado de C10 convertido en criterio.**
- **G-e [CONFUSO HALLADO EN EL HUMO — la experiencia propia no está igualada]** mediana de `mord` (mordidas propias
  del receptor) de **PRED ≤ 1.5 ×** la de N0. **En el humo esta guarda YA SALTA** (PRED ≈ 2 100 contra N0 ≈ 1 230,
  razón 1.7; SHUF llega a 3 222). Los brazos con canal **muerden 2–3 × más**, así que "retiene tras el silencio" podría
  ser sólo "mordió más y aprendió solo". Se ve crudo en el humo: **SHUF y SACIEDAD mudos suben a 0.997**, muy por
  encima del 0.712 de N0, y su canal es ruido — no puede ser el canal lo que les enseña.
  **Por eso N6 se lee en su forma emparejada, N6′, y la forma cruda pasa a ser diagnóstico:**
- **N6′ [la predicción principal, emparejada por mordidas]** se lee la curva `curva_rec` (que ya registra
  `(t, exposiciones, mordidas, acierto)`) y se compara el acierto de **PRED mudo en Q4** con el de **N0 al MISMO número
  acumulado de mordidas propias** (interpolación lineal sobre su curva). Criterio: diferencia **≥ +0.10** en mediana y
  pareado en **≥ 14/20**. Si PRED no gana a N0 emparejado por mordidas, **la retención era experiencia propia** y la
  hipótesis se refuta, pasen o no las demás.
- **G-d [el canal se usa]** `senales_recibidas` del receptor > 1 000 en ≥ 18/20 en los brazos con canal.

## 7. Criterio de refutación

- **G-b o G-c caen** → **NULO**: el mundo no es decidible, ERR y mundo nuevo. No se lee ninguna predicción.
- **N6′ falla** (aunque N6 crudo pase) → **REFUTADO**: lo que retenía era la experiencia propia extra, no el canal.
- **N6 falla** → **REFUTADO**: aprender el significado **no** compra retención; el receptor sigue obedeciendo. Se
  registra así, sin reintentos con otro `gamma_pred`.
- **N6 pasa y N6b también** → *el mundo permite retener y los dos mecanismos retienen*; lo que separa a PRED del
  innato es **el coste en mordidas de aprender el significado** (N5), no la retención.
- **N6 pasa y N6b falla** → el resultado grande: **sólo el significado aprendido se retiene**. Pide réplica inmediata.
- **N1 falla** → el receptor no aprende el significado y todo lo demás es ruido.
- **N4 falla** → un control informa cuando no debería: montaje inválido, ERR.
- **N3 falla** → aprender el significado cuesta acierto: canje medido, no mejora.

## 8. Trampas revisadas

| trampa | cómo se evita |
|---|---|
| **el mundo lo resuelve solo** (mi humo 1: SOLO_R 0.998) | **G-c**, banda de la línea base |
| **el mundo no deja representar** (ERR-32) | 8 vistas distintas, comprobado 6/6 en 12 semillas sin correr nada |
| **los patrones no fluyen** (K3 de N2f, S4 de N3c) | **G-b**, y `regen_en_fijos` (ERR-33) |
| **la base y el tratamiento ven mundos distintos** (ERR-34) | `nobj_total = 8` en todos los brazos, y **N0** (n = 2) como línea base |
| obedecer en vez de aprender | **N6′**, el brazo mudo emparejado por mordidas |
| **ganar mordiendo más, no escuchando mejor** | **G-e** y **N6′** (emparejado por mordidas propias). Hallado en el humo |
| acierto sin balancear | `acierto_q4` de `corre_N3d.py` copiada literal; 4 comida / 4 veneno |
| canal simétrico | sólo el receptor escucha |
| base censurada | **cláusula de censura** escrita en N2′ |

## 9. Coste y quién corre qué

**Runner:** `experimentos/creacion_C/corre_n2pred.py` (Pool(14) sólo bajo `__main__`; **lo corre el COORDINADOR**).
Etapas: identidades L1–L3 (aborta si no 100 %) → 6 brazos × 2 (hablando / mudo) × 20 semillas × 200 000.
**Humo del diseñador:** `--humo`, un proceso, semillas 1–3 (ya expuestas en los humos de diseño), T = 100 000.
**Sin commits** (regla 7).
