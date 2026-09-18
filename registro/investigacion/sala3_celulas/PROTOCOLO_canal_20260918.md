# PROTOCOLO DEL CANAL CON REFERENCIA — síntesis de la sala 3 (12 células Haiku)
**18 sep 2026 · sintetizador · sobre `organismo_familias_b3` / `organismo_familias_b4.py` (bloque 4 en curso)**

MISIÓN: llegar a la AGI por este camino — un organismo mínimo con reglas locales que aprende, desaprende,
generaliza, sobrevive y se COMUNICA. Hoy: que dos células se comuniquen **sobre algo que ambas representan**.

---

## 0. Lo que hay que decir antes (la letra del bloque 4 ya escrita)

Las 12 células diseñaron **a ciegas del código**. Convergieron en un protocolo casi unánime — y en cuatro puntos
ese protocolo **contradice el instrumento que ya existe**. Lo digo aquí, no lo escondo:

| Lo que propusieron 11 de 12 | La letra de `organismo_familias_b4.py` | Qué se hizo |
|---|---|---|
| "marca en **píxeles 9–12** del canal, separados del mundo (0–8)" | la retina es `fam_D=12` → píxeles **0–11**; los **9, 10 y 11 son los `fam_nvar=3` píxeles VARIABLES**, es decir, exactamente los que distinguen "sal rosa" de "sal". **El píxel 12 no existe.** | **Se descarta la marca retiniana.** Escribir en 9–11 no abre un canal: falsifica la variante. El canal de b4 **no pasa por la retina**. |
| "clave = (**mi código privado**, contexto del canal)" | la tabla de pares se direcciona por **PARES DE PÍXELES DE LA RETINA** (`_PARv`, C(12,2)=66 celdas × 4 casillas de 2 bits). Las coordenadas de retina son **públicas**: las dos células las comparten. El código privado (Kenyon) es de la **vía rápida**, que el canal **no toca**. | **Se descarta la clave compuesta.** No existe y no se puede construir sin órgano nuevo. Y el miedo central de la sala ("nuestros códigos divergen") **no aplica al sitio donde aterriza el mensaje**. |
| "valor **−5**" | las recompensas crudas del mundo son `R_VAL = {comida:+1.0, veneno:−3.0, nada:0.0}`. **−5 no existe.** | El mensaje lleva **la R que el emisor realmente recibió: −3.0**. Y basta (§2, fila "tímida"). |
| "el receptor ya mordió 'sal rosa' 7–8 de 10 veces" | con `puerta` activa la boca lee la **vía rápida** si el código le es FAMILIAR (`puerta_pat=5` mordidas de ese código exacto ∧ ≥1 celda consolidada), y la **lenta** —donde vive la tabla— sólo si **no** le es familiar. | **Se invierte el montaje**: el canal sólo llega a la boca **para lo que el receptor aún no conoce de primera mano**. Ver §2.7: es el hallazgo estructural que ninguna célula vio. |

Lo que las 12 sí acertaron, y es el corazón del protocolo: **la referencia no viaja en el mensaje; viaja en el
mundo**. El mensaje no puede nombrar; sólo puede coincidir con lo nombrado.

---

## 1. El protocolo convergido (pseudocódigo LOCAL sobre `organismo_familias_b3`)

Dos organismos, **un solo mundo** (`fam_seed` igual), **semillas de organismo distintas** (proyecciones y códigos
privados distintos: es la premisa del bloque). Ninguno ve el interior del otro.

```
# ---------------- EMISOR  (canal={'modo':'emite'})  — SÓLO LEE, no cambia ninguna decisión ni el rng
al morder el estímulo kk:
    R = R_VAL[val[kk]]                                  # la regla local de siempre
    si  kk está marcado por el mundo (excepción o virada)  y  R < 0  y  aún no anoté:
        ANOTA  msg = (t, kk, P=PAT[kk], R)              # patrón de 12 px + valencia CRUDA. Nada más.
# no emite código, no emite nombre, no emite su tabla: emite EL PATRÓN DEL MUNDO Y LO QUE LE PASÓ.

# ---------------- CANAL   — la entrega
'inm' : entrega en cuanto  t >= msg.t                    # el emisor "grita" y quien esté oyendo, oye
'sen' : entrega cuando  pos in objs  and  objs[pos]==ref # SEÑALAMIENTO: el receptor está SOBRE el referente
'mudo': hace todo lo anterior y NO escribe               # CORTADO (gemelo)

# ---------------- RECEPTOR (canal={'modo':'sen', 't':msg.t, 'ref':msg.kk, 'P':msg.P, 'R':msg.R})
#   El mensaje se ejecuta como EXPOSICIÓN SIN CONSECUENCIA: el bloque de escritura de la tabla de pares
#   de b3, LITERAL, con el patrón y la valencia del mensaje. No toca energía, ni objetos, ni `ncod`,
#   ni la vía rápida, ni la plasticidad. No cuenta como mordida.
al entregarse el mensaje (una sola vez):
    para cada celda cv de las 66 (par de píxeles (i,j)):
        d  = 2*P[i] + P[j]                              # la casilla que ESTE par le asigna al patrón recibido
        p  = MM[cv,d] si MN[cv,d]>0 si no 0.0           # lo que esa celda habría dicho
        e  = R - p                                      # ERROR PROPIO de la celda (regla local, sin backprop)
        ME[cv] = e*e  si es su primera vez,  si no  (1-mem_rho)*ME[cv] + mem_rho*e*e
        MM[cv,d] = R                                    # SOBRESCRITURA (mem_alfa=1.0): la casilla sigue a la última
        MN[cv,d] += 1
    GANADORA = argmin ME                                # relevo: manda la celda de menor error propio
# a partir de aquí, cuando el receptor VE ese patrón y su código NO le es familiar,
# la boca lee la lenta -> lee la tabla -> lee -3 -> Vb = 1.2*(-3) + 2.0*hambre + 0.5 -> p(morder) <= 0.025
```

**Perillas (todas ya existen; ninguna se inventa):**
`fam_seed` (mismo mundo para E y R) · `canal={'modo','t','ref','P','R'}` · `reg_b4=1` (conducta de la boca en las
3 primeras exposiciones tras la entrega) · `memoria_pares='relevo'` (obligatorio: sin tabla no hay dónde escribir,
`ValueError`) · `mem_alfa=1.0`, `mem_rho=0.02` (las de v15f, sin tocar) · `exc_fija=2`, `n_exc=1` (el referente es
la variante RETENIDA por la deriva, de un solo token) · `deriva_E=5000` frente a `deriva_R=T/3+1` (**el receptor no
puede haber visto el referente cuando el mensaje llega**) · `puerta_pat=5` (la que decide si el mensaje se lee).
Diagnósticos de salida: `canal_gan_pre`/`canal_gan_post`, `canal_bin`, `canal_mismo_bin`, `primera_b4`.

**Qué es "referencia" aquí, sin adornos.** No es que las dos células "entiendan lo mismo". Es que el mensaje lleva
**coordenadas de retina** (públicas) y se entrega **mientras el receptor está sobre el objeto** (`sen`). La
referencia se resuelve por **coincidencia**, no por contenido. Eso es también su falsación: BARAJADO (§3).

**Resolución de la referencia — el techo honesto.** La boca lee por **UNA** celda ganadora, o sea por **2 bits**.
Un mensaje no puede ser más específico que la casilla de esa ganadora. `canal_mismo_bin` dice, en cada corrida,
cuántos de los 24 estímulos caen en la misma casilla. **Ninguna célula propuso una cifra de discriminación que se
pueda sostener a priori** (varias prometieron ">0.9"): la especificidad **se mide**, no se promete.

---

## 2. Cada rasgo contra el protocolo

| Rasgo | ¿Lo rompe? | Qué se hizo |
|---|---|---|
| **Tímida** (células 1, 2) | **No.** La timidez no está en el organismo como parámetro: la boca es `pb = σ((1.2·w + 2.0·hambre + 0.5)/0.3)`. Lo que las células llamaron timidez es hambre baja. Con `w=−3` y hambre 1 → **p=0.025**; saciada → **p≈3e−5**. | Se acepta su número (era correcto) y se **elimina su −5**: −3 ya deja la boca por debajo de 0.5 **para toda hambre posible** (0.5 exigiría hambre 1.55). |
| **Voraz / hambrienta** (3, 4, 5, 9, 10) | **No, dentro del mundo.** Su miedo ("con hambre extrema muerdo igual") está mal calibrado: el término de hambre satura en 2.0 y −3.6 lo domina. | Se descarta la petición de subir a −5 "por voracidad". Se conserva su punto real: el canal **no salva de la inanición**, sólo evita una mordida. |
| **Alias fuerte** (5, 6) | **Sí, pero no por donde creían.** El alias de códigos (1–2 % de pares comparten código Kenyon) vive en la **vía rápida**, que el canal no toca. El alias que sí muerde es otro: **que la ganadora sea un par de píxeles de FORMA** (0–8), compartidos por toda la familia → el −3 de "sal rosa" se lee también en "sal" → **pánico de familia → inanición**. | Su mitigación (píxeles de canal en la clave) **no existe**. Se sustituye por una **medida**: `canal_bin` + `canal_mismo_bin` + el control de hermanas de §3. Si la ganadora cae en forma, el protocolo **falla y se ve**. |
| **Saciada** (7, 8) | **No.** Saciada el miedo es más fuerte, no menos. | Nada que arreglar. Su aporte real: pidieron **una sola emisión honesta**, y así quedó (`_c4em` se fija una vez). |
| **Sólo 2 de 3 variantes** (12) | **No: es el caso de diseño.** El montaje ya lo garantiza por el mundo, no por el rasgo: `deriva_R = T/3+1` hace que la tercera variante **no exista** para el receptor hasta 2T/3. | Se adopta: el receptor **nunca vio el referente**. Es la única forma de que "evita sin morder" signifique algo. |
| **Ya lo había mordido** (supuesto de las 12) | **SÍ, lo rompe entero.** Con ≥5 mordidas de ese código exacto el código le es FAMILIAR y la boca lee la **vía rápida**: el mensaje queda escrito en la tabla y **la boca nunca lo consulta**. | **Se invierte el supuesto de la sala.** Regla: *el canal sólo alcanza a la boca para lo que el receptor no conoce de primera mano.* Es un límite del tronco v14.1, no del canal. |

**2.7 — Lo que ninguna célula vio y es el hallazgo del día.** El canal **no sirve para advertir de lo que el
receptor aprendería solo**: en el bloque 3, v15f desaprende la variante que cambia en **una mordida (7 de 8)**, y
esa mordida cuesta −3, que no mata. Donde el receptor solo está **ciego para siempre es en 0 de 8**: la variante
que **evitaba** (veneno) y que **pasó a ser comida** — como no la muerde, nunca la corrige. **Ahí el canal es
irreemplazable.** Las 12 células eligieron, unánimemente, la dirección barata (aviso de veneno). El emisor de b4
tampoco anota la otra: `if ... and R<0`. Queda dicho en §5.

---

## 3. La prueba medible, con controles y umbrales

**Unidad de medida: la boca, nunca los pesos (ERR-44).** Lo que se lee es `primera_b4[referente]`: la conducta en
la **1.ª exposición del receptor al referente tras la entrega** (que, por el montaje, es su **1.ª exposición de la
vida** a ese patrón). Binaria: mordió / no mordió. 8 semillas (escalón 1/8 = 0.125; la zona declarada (0.5, 0.8)
de ERR-37a queda vacía a propósito).

| Brazo | Qué cambia | Predicción | Umbral |
|---|---|---|---|
| **CANAL** | `modo='sen'`, `P`=patrón del referente, `R`=−3.0 | **no muerde** en la 1.ª exposición | **≥ 7/8** |
| **CORTADO** | `modo='mudo'`: misma visita del canal, mismo paso, **sin escritura** | muerde (patrón nuevo, `w≈0` → `p≈0.99`) | **≥ 7/8 muerde** |
| **BARAJADO** | mismo instante, misma R, **`P` = patrón de una HERMANA** (`T0v0`) | **muerde el referente** y en cambio **evita la hermana** (el miedo se muda al objeto equivocado) | referente mordido **≥ 7/8**; si evita el referente **≥ 4/8 → el mensaje no nombra: protocolo muerto** |
| **VALOR-SOLO** | misma R, **`P` = 12 ceros** (valencia sin referente) | muerde el referente: la tabla se sacude pero no se le dijo nada de él | referente mordido **≥ 7/8** |
| **R-SIN-SAL** | el receptor recibe el mensaje en un **mundo donde el referente no existe** (`fam_seed` distinta) | **daño colateral nulo**: la entrega reelige la ganadora de las 66 y eso cambia la lectura de TODO lo que sirve la vía lenta | mordidas sobre los otros 7 tokens **idénticas a CORTADO en ≥ 7/8**; **0 muertes extra** |
| **HERMANAS** (especificidad, dentro de CANAL) | — | sigue comiendo `T0`, `T0v0`, `T0v1` | difiere de CORTADO en **≤ 1/8**; si evita también a las hermanas → **alias de forma: inanición, fracaso** |

**Puerta previa (ya en `identidad_familias_b4.py`, P-I3):** CANAL y CORTADO comparten el **prefijo exacto del `log`
hasta la entrega**. Si no, lo que se mide no es el mensaje.

**Prueba decisiva, en una frase:** *el receptor, que nunca ha visto el referente, no lo muerde la primera vez que
lo ve (≥7/8) mientras CORTADO sí lo muerde (≥7/8), y sigue comiendo a sus tres hermanas — y BARAJADO, con el mismo
instante y la misma valencia pero el patrón de una hermana, lo muerde igual.*

**Estado de los controles:** CORTADO (`mudo`), BARAJADO (`P=T0v0`) y VALOR-SOLO (`P=[0]*12`) **ya existen** en
`identidad_familias_b4.py` como pruebas de identidad (H, K, O, P) — aquí se convierten en **medidas de conducta**
con umbral. **R-SIN-SAL no existe todavía**: hay que añadirlo (la pieza está: el caso (N), `fam_seed` distinta).

---

## 4. Bloque 5 — la señal arbitraria (la palabra), en cinco líneas

1. Hoy el mensaje **es** el patrón del mundo: no hay palabra, hay una copia del referente. Eso todavía no es lenguaje.
2. Bloque 5: el emisor manda un patrón **arbitrario y fijo** (una "palabra" W, ajena al mundo) en lugar del referente.
3. El receptor sólo puede anclarla por **coincidencia repetida**: W se entrega siempre en `sen`, estando sobre el referente.
4. Se mide lo mismo con un control nuevo, **PALABRA-CRUZADA**: la palabra de otro referente, entregada aquí, no debe mover la boca.
5. Falla esperada y honesta: con **una** celda ganadora de 2 bits no caben 8 palabras. El bloque 5 pedirá, casi seguro, **más de una ganadora** — y eso ya es órgano nuevo, no perilla.

---

## 5. Lo que las células NO pudieron resolver

1. **La dirección útil.** Las 12 eligieron avisar de veneno — lo que el receptor aprende solo en una mordida (7/8).
   Nadie propuso el caso ciego (0/8): *"lo que evitabas ya es comida"*. Y el emisor de b4 **no lo puede decir**:
   sólo anota con `R<0`. Falta la perilla simétrica. **Es el trabajo de mañana.**
2. **La especificidad.** Todas la prometieron (">0.9", "0 de 10") y ninguna pudo derivarla: depende de qué par de
   píxeles gane el relevo, y eso no se decide, se observa (`canal_bin`, `canal_mismo_bin`). **Sigue abierto.**
3. **El techo de 2 bits.** Nadie lo vio. Una sola ganadora no distingue 24 estímulos. **Sigue abierto** (bloque 5).
4. **La puerta de familiaridad.** Nadie la vio. El canal es invisible para lo ya conocido de primera mano.
   No se sabe si eso es defecto o virtud (¿protege de la mentira ajena?). **Sin medir.**
5. **El daño colateral del relevo.** Nadie vio que una sola entrega **reelige la ganadora de las 66** y con ello
   mueve la lectura de todo lo demás. Por eso se añade R-SIN-SAL. **Sin medir.**
6. **Emisor honesto.** Cuatro células propusieron "valido observando si el emisor rechaza en T+2..T+5". **El
   receptor no ve al emisor**: son dos `run()` distintos, sin visión mutua. Esa mitigación **no existe**, y con
   ella cae la defensa contra la falsa alarma. **Sin resolver.**
7. **Coordinación de archivos.** 7 de 12 escribieron fuera de `registro/investigacion/sala3_celulas/` del bundle
   (en tres raíces distintas). Los 12 archivos están, dispersos. Consolidar antes del prerregistro.
