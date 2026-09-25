# EXPLORATORIO, no es dato

# PROMETEO: la cinta con su kit de órganos, sin juez (Opus, 24-sep-2026, 21:50–23:20)

**Misión:** llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).

**Veredicto: HAY ALGO MODESTO.** La cinta sí se armó órganos que no escribimos, y la selección llevó varios a más del 50 % del banco.
Casi todos son slots del **órgano de transmisión**, y ese slot ya estaba en el alfabeto v0: CODIGO_SIN_SOS también los arma.
Los cables nuevos del kit (estado → decisión) casi nunca ganan: pasa en 2 casos de 16.
PROMETEO deja más nacimientos sin reponedor que CODIGO_SIN_SOS y PERILLAS, pero en `onda8k` el resultado lo arrastra una sola semilla. Con n = 8 no es dato.

## 1. Qué construí (`experimentos/organelos/prometeo/`; solo copias; semillas 30001–30008)
- **`construye_prometeo.py`** genera dos archivos por anclas de texto, sin tocar los originales:
  - `codigo_prometeo.py`, desde `codigo_def.py`;
  - `motor_prometeo.py`, desde `motor_fable.py`.
  La física del mundo no cambia. El cuerpo es FAMB_GRAM_ECO arrancado desde filtra0, con la misma cinta v0 (`CD.compila()`).
- **La SOS no se lee.** La instrucción SOS queda en la cinta como basura neutra, igual que en CODIGO_SIN_SOS.
- **El KIT** entra en el alfabeto de las instrucciones al azar (inserción y cambio entero). La cinta inicial no lo trae: nace AUSENTE.
  - **`CABLE s d w`** conecta una señal presente a una decisión con un peso w de −3 a 3. Es el cableado de `cruce/CRUCE.py`, llevado al motor.
    - Señales: sesgo, reserva, la otra reserva, ventana de parto, edad e hijos vivos.
    - Decisiones: boca, patas y parto.
    - Lo interpreta el lector, así que REP, DEF y LLAMA lo multiplican.
    - Boca y patas: un sesgo exponencial empuja la decisión del carro hacia un lado.
    - Parto: la ventana de parto se veta si la suma ponderada `W·s` es menor que 0.
  - **`HGT p l`** es la transferencia horizontal. Al nacer, con probabilidad {0.02, 0.05, 0.10, 0.25}, el hijo inserta en su cinta un tramo de 1, 2, 4 u 8 instrucciones.
    - El tramo viene del **vecino vivo más cercano, de cualquier linaje**.
    - Manda la primera HGT de la cinta, igual que con la SOS.
    - La HGT puede copiar también instrucciones HGT y CABLE.
  - **Slot de transmisión:** ORG (cuándo, qué, a quién, cómo) ya existía en v0. No se agregó; se cuenta como órgano nuevo todo slot distinto de filtra0.
  - **Simbionte: NO ENTRÓ.** En este motor no hay nada que tragar ni retener. Recorte declarado.
- **Seguridad:** la cinta es un lenguaje cerrado con tuplas validadas. No hay `eval` ni `exec`, y la cinta no toca archivos ni red.
- **`corre_prometeo.py`** reutiliza `corre_codigo.trabajo()` sin modificarlo. Guarda la cinta de todo el banco en el corte y al final.
- **`lee_prometeo.py`** marca como **INERTE** (`~`) lo que no puede cambiar ninguna decisión:
  - cables de parto con todos los pesos ≥ 0, porque las 6 señales son ≥ 0 y nunca vetan;
  - slots ORG con `cuando = nunca`.
  Lo inerte sirve de **control neutro interno**: muestra qué se fija por deriva.

**Por qué esto es "misión: evolucionar" sin ser un juez.** No hay función de puntaje. Solo decide quién deja hijos en el mundo.
La misión son dos mecanismos que **generan variación**: la duplicación, que ya estaba, y la HGT. La cantidad de variación la escribe cada cinta, y esas cifras se heredan.
Si compartir tramos rinde, la instrucción HGT sube por arrastre en los linajes que dejan más hijos. Si no rinde, se pierde. Nadie la premia.
Es la lección de Woese: en la evolución temprana, el genoma fue comunal. Aquí se le da al organismo **la posibilidad** de ser comunal, no la orden de serlo.

## 2. Identidad (`identidad_prometeo_salida.txt`: 8/8)
- **IP1:** kit ausente del alfabeto y de la cinta, sin HGT → CODIGO_SIN_SOS de prometeo == el de `motor_fable`, **bit a bit** (onda8k, T 6000).
- **IP2:** lo mismo con PERILLAS: bit a bit.
- **IP3:** alfabeto con kit, cinta sin kit y copia apagada → == MUT0, bit a bit.
- **Arnés por pieza:**
  - IK1: `CABLE(reserva→parto, −3)` lleva los nacimientos a 0 (v0: 82).
  - IK2: `CABLE(sesgo→boca, −3)` baja las mordidas de 4 295 a 2 419.
  - IK3: `CABLE(sesgo→patas, +3)` da 30 626 pasos forzados.
  - IK4: `HGT(0.25, 8)` produce 21 transferencias y cintas de 31 a 45 instrucciones; sin HGT hay 0.
  - IK5: un cable de peso 0 deja la dinámica bit a bit igual.
- **Cambio de criterio declarado.** La primera pasada dio 6/8 por fallas del arnés, no del mecanismo:
  - IK4 miraba las cintas de los vivos en T, que eran fundadores repuestos; ahora mira el banco.
  - IK5 incluía `cod_nac`, que guarda el largo de la cinta; ahora usa la firma de la dinámica.
- **Ojo:** PROMETEO no es v0 bit a bit una vez que el kit entra al alfabeto. Con 11 operaciones en vez de 9, cada inserción al azar ya es otra.

## 3. Qué pasó
Condiciones: T 60 000, cambio en 8 000, corte en 44 000, 8 semillas por brazo, 64 corridas, 7–8 procesos a la vez.
"nac solo" = nacimientos después del corte, sin reponedor.

| mundo | brazo | persiste | nac solo (suma · mediana) | vs CODIGO_SIN_SOS (nac solo, pareado) | largo de cinta (t 0 → corte → final) | banco con órgano FUNCIONAL / INERTE / HGT en el corte |
|---|---|---|---|---|---|---|
| quieto | PROMETEO | 8/8 | 1 548 · 158 | gana 5/8 | 30.3 → 36.5 → 37.3 | 0.46 / 0.25 / 0.31 |
| quieto | PROMETEO_SIN_HGT | 7/8 | 1 081 · 118 | 4/8 | 30.4 → 33.8 → 32.4 | 0.31 / 0.28 / 0 |
| quieto | CODIGO_SIN_SOS | 8/8 | 1 216 · 148 | — | 30.4 → 33.7 → 33.9 | 0.41 / 0.10 / 0 |
| quieto | PERILLAS | 8/8 | 834 · 98 | CODIGO_SIN_SOS le gana 5/8 | — | — |
| onda8k | PROMETEO | **1/8** | **3 938** · 166 | gana **6/8** | 30.3 → 37.5 → 37.2 | 0.51 / 0.08 / 0.35 |
| onda8k | PROMETEO_SIN_HGT | 2/8 | 1 292 · 98 | 6/8 | 30.4 → 36.1 → 37.6 | 0.23 / 0.20 / 0 |
| onda8k | CODIGO_SIN_SOS | **4/8** | 1 356 · 53 | — | 30.4 → 37.2 → 36.1 | 0.35 / 0.07 / 0 |
| onda8k | PERILLAS | 0/8 | 356 · 48 | CODIGO_SIN_SOS le gana 6/8 | — | — |

- **¿Aparecen órganos que la cinta armó sola?** Sí, en las 16 corridas de PROMETEO. Los cables aparecen en todas: las correcciones que imponen se cuentan por cientos o miles en cada corrida.
- **Los que eligió la selección** (más del 50 % del banco):
  - Slots de transmisión: en casi todas las semillas de todos los brazos con cinta, incluido **CODIGO_SIN_SOS**, sin kit.
  - Cables:
    - **1/8 en quieto:** `reserva → boca −`, al 97–100 %;
    - **1/8 en onda8k, en SIN_HGT:** `sesgo/ventana → patas +`, al 76–78 %, solo al final.
  - La instrucción HGT supera el 50 % del banco en el corte en 3/8 (quieto) y en 2/8 (onda8k); al final, en 3/8 (onda8k). En onda8k s30003 llega al 100 %.
- **Parecido con lo que diseñamos:**
  - `nacer/todo/hijo/copiar` **es `ensena`, redescubierto**: 0.65 del banco en onda8k s30005 y el 100 % de los vivos en quieto SIN_HGT s30006.
  - `nacer/pos/hijo/copiar` y `nacer/neg/hijo/copiar` son filtra0 partido por signo.
  - **Nuevos:**
    - `vida/pos/hijo/promediar`: enseña al hijo durante toda la vida;
    - `reserva → boca −`: saciedad; se parece a O3, pero lee el estado para la BOCA, no para el parto.
- **El largo de la cinta:** crece en todos los brazos con cinta, de 30 a 34–38 instrucciones, por duplicación e inserción.
  Con HGT crece unas 3 instrucciones más (quieto: 36.5 contra 33.8). En onda8k s30003 llegó a **60**.
- **¿La HGT ayuda o estorba?** No hay señal consistente. PROMETEO le gana a SIN_HGT en 4/8 (quieto) y 3/8 (onda8k).
  La HGT sube en el banco, pero puede ser arrastre: se copia a sí misma y viaja con lo que gana.
  **Confusión declarada:** el vivero ya reparte cintas entre linajes, porque repone fundadores desde el banco común. Eso es "HGT gratis" para todos los brazos.

## 4. Tres bichos en humano
1. **onda8k s30003, PROMETEO: el bicho que despegó.** Se armó dos órganos de transmisión:
   - `vida/pos/hijo/promediar`: cada 500 pasos le pasa al hijo lo que sabe que alimenta, promediado;
   - `vida/sin0/hijo/promediar`.
   Además duplicó filtra0 y lleva `HGT(0.02, 4)`.
   - El órgano pasó del 33 % de los nacidos en t 8 000 al 86 % en t 16 000 y al 99 % en t 24 000.
   - Los nacimientos por ventana subieron de ~50 a **~700**, con 11 471 nacimientos y 305 generaciones.
   - Después del corte hubo **2 677 nacimientos solos**, con R0 0.99, y persiste.
   - Cinta de 61 instrucciones.
   Es la única semilla así en 32 corridas de onda8k.
2. **quieto s30006, PROMETEO: el bicho que se sacia.**
   - `CABLE(reserva→boca, −2)`: cuanto más lleno está, más se niega a morder (2 963 negativas).
   - `ORG morir/pos/hermano/copiar`: al morir, le deja al hermano lo que alimenta.
   El cable pasó del 15 % de los nacidos en t 24 000 al 97 % en t 40 000, con solo el 8 % de HGT: llegó por herencia vertical más el banco.
3. **onda8k s30002, PROMETEO: filtra0 partido en dos.** El 72 % del banco final lleva tres slots:
   - `nacer/pos/hijo/copiar`;
   - `nacer/neg/hijo/copiar`;
   - `vida/reciente/hermano/copiar`.
   El órgano de fábrica (filtra0) se perdió: lo reemplazó su versión por signo, más una enseñanza en vida.

## 5. Lectura honesta
- La cinta **sí se arma órganos**, y la selección fija algunos: pasan del 50 %, mientras que lo inerte queda en 0.05–0.40.
- **Pero el material que usa es el de v0** (el slot ORG), no el kit nuevo. Los cables (estado → decisión) casi siempre quedan en 1–15 %; ganan en 2 casos de 16.
- La ventaja de PROMETEO en nacimientos solos es una mediana de 166 contra 53 en onda8k y 158 contra 148 en quieto. Viene sobre todo de una semilla explosiva.
- **Lo que no esperaba:** en onda8k, PROMETEO persiste **menos** que CODIGO_SIN_SOS (1/8 contra 4/8) aunque deja más nacimientos. Parece auge y caída, sin verificar.
- Con 8 semillas, nada de esto es veredicto.

## 6. ¿Merece un preregistro? Sí, uno chico y con otra pregunta
**Pregunta:** ¿los órganos de transmisión que la cinta se arma sola se fijan **por encima de lo neutro**? ¿Y el mundo estacional hace más frecuente el despegue tipo s30003?

- **Medida principal:**
  - fracción del banco en el corte con órgano FUNCIONAL, contra la fracción con órgano INERTE (control neutro interno);
  - frecuencia de despegues: más de 1 000 nacimientos solos.
- **Controles:**
  - AZAR (donante al azar: variación sin selección);
  - CABLE_MUDO (el cable se lee pero no actúa: separa estructura de función);
  - SIN_HGT;
  - VIVERO_POR_LINAJE (el banco se repone solo desde el propio linaje, para quitarle a la HGT su rival gratis).
- **Diseño:** 20 semillas, `quieto` y `onda8k`.
- **Predicción a escribir:** funcional por encima de inerte en al menos 14/20 en los dos mundos, y AZAR ≈ inerte.

## 7. Predicciones refutadas (`PREDICCIONES_previas.md`, firmadas a las 22:02) y lo que no verifiqué
- **Refutadas:**
  - «Si un cable gana, será un veto de PARTO que lee la reserva, y los cables de BOCA estorban». Ganó un cable de **boca** (saciedad), y ningún veto de parto.
  - «PROMETEO ≈ SIN_HGT (diferencia < 25 %)». Las sumas difieren un 43 % y un 205 %, aunque la comparación pareada queda en 4/8 y 3/8.
  - «PROMETEO/CODIGO_SIN_SOS entre 0.8 y 1.25». Da 1.27 en quieto y 2.9 en onda8k, este último por una semilla.
- **Se cumplieron:**
  - aparecen cables en todas las semillas;
  - algún órgano del kit pasa del 50 % en al menos 1 semilla;
  - CODIGO_SIN_SOS > PERILLAS en quieto (5/8);
  - la cinta crece 2–3 instrucciones más con HGT.
- **No verifiqué:**
  - si el despegue de s30003 se debe al órgano o a otra cosa, porque no hubo lesión ni trasplante de la cinta;
  - el auge y caída en onda8k;
  - si la HGT transfiere **entre linajes** lo que gana (guardé los eventos en `hgt_ev`, pero no los leí);
  - el simbionte, que no entró;
  - T > 60 000.
