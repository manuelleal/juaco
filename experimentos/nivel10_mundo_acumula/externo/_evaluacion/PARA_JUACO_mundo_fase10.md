# PARA JUACO — El mundo de la fase 10: qué se encontró, qué mundo usar y qué decidir (21-sep-2026, 21:00)

De: el árbitro de alefast (Claude Fable, sesión de JUACO-EXO), a partir de tres brazos independientes que resolvieron el
`ENCARGO_mundo_fase10_20260921.md` sin tocar el repo de JUACO, y de una auditoría independiente que volvió a correr sus arneses,
verificó los 15 shas de anclas contra JUACO y reconstruyó los mundos con sha idéntico. Todo el material está en
`C:\Users\User\Documents\PROYECTOS\JUACO-EXO\equipos\fase10\` (rama `autonomo-fase3-4`). Este archivo es autocontenido: con él y esa
carpeta el coordinador de JUACO puede actuar sin leer nada más.

---

## 1. Veredicto (una línea)

**NO: el mundo de la fase 10 se puede construir, anclar y verificar (dos paquetes con arnés 79/79 y humo con JSON), pero el tronco
v14.2 con el nodo de la fase 9 y el mapa de nivel 6, sin tocarlo a mano, no lo cruza; el muro está en la boca del organismo, no en el
conocimiento heredado. No gastar la serie con la letra actual.**

## 2. El hallazgo central (los dos brazos de Fable lo midieron por separado y coinciden en el fenómeno)

**El conocimiento llega al recién nacido y no se usa.**
- F0 (Fable solo): cobertura del signo de la tabla en los cuerpos 5..12 del linaje = 0.94 / 0.69 contra 0.50 en NADA. La transmisión
  llena la tabla. Y aun así REL R₀ 0.046–0.065, ORÁCULO 0.058.
- F+ (Fable + poderes): índice J del recién nacido con nodo = 0.43 contra 0.03 sin nodo (sabe QUÉ desde su primer encuentro). Y aun así
  REL R₀ 0.503 = el mismo techo que el ORÁCULO de la fase 9 (0.51–0.56).

**El mapa de nivel 6 como canal del DÓNDE no compra nada, o empeora.**
- F0: ORÁCULO con mapa 0.058 contra ORÁCULO sin mapa 0.086.
- F+: MAPA 0.237 / 0.294 contra REL (sólo QUÉ) 0.503, indistinguible del control NODO_BARAJADO 0.245. El sesgo difuso lleva al cuerpo a
  sitios agotados o virados. (Coincide con lo ya medido en el nivel 6: "no rodea de forma fiable", ENCARGO §7.)

**Dónde está el muro (la atribución difiere y por eso vale leer las dos).**
- F0 lo pone en el **organismo**, en dos líneas: la boca decide con `Wp[_nm]-Wn[_nm]` de la fila de la **necesidad activa** y muerde el
  veneno cuando tiene sed (inmortal: veneno con SED 57/63 exposiciones; sal con HAMBRE 85/259); **en el mundo del tronco pasa lo mismo**
  (75/83 y 101/508) y sobrevive porque ve todo el anillo y come el doble de bueno. Y con retina vacía casi no se mueve (p ≈ 0.005): no
  explora, el mapa sólo devuelve lo ya visto. Por eso en su mundo (que cobra "dónde") ni el inmortal se sostiene: RENACE 0.063.
- F+ lo pone en el **instrumento del DÓNDE**: su mundo sí conserva el ancla del mundo vivo (NADA 0.111, INMORTAL 0.915), el linaje que
  transmite QUÉ vive, y lo que falla es la vía por la que entra el sitio.
- Lectura del árbitro: no se contradicen. F+ muestra que con la calibración correcta el mundo es jugable y QUÉ se transmite; F0 muestra
  por qué QUÉ no basta y por qué el DÓNDE no puede entrar por el mapa: la boca no lo consulta cuando manda la otra necesidad.

## 3. El mundo que recomiendo llevar a `experimentos/nivel10_mundo_acumula/`

**Instrumento de F0 con la calibración de F+** (recomendación del auditor, con la evidencia de ambos):
- **Instrumento (F0):** `equipos/fase10/F0_fable_solo/` — `construye_mundo_fase10.py` (48 anclas desde `organismo_f9.py`
  `3a821884394d66c9` + cadena de 7 shas hasta v14.1 + B-5 de v14.2 + 7 donantes literales: `organismo_v142`, `organismo_vivo_codigo`,
  `f9c` (ORÁCULO), `mundo_mapa` `207d6a1954336b18`, `v3cal` (placebo), familias, muralla; guardia de líneas perdidas),
  `identidad_mundo_fase10.py` (10 familias de identidad, 13 controles que deben diferir, 5 guardias; 79/79 reproducido por el auditor),
  `corre_mundo_fase10.py` (12 brazos, V-1..V-6 + M10-1..5 + PLAC, una línea por puerta, `lee_json` con sello). 16 tipos en 10 px
  (4 familias × 4 variantes one-hot), visión limitada `r_vis`, parches que se agotan y se mudan, cambios no avisados.
- **Calibración (F+):** los parámetros con los que el ancla §2.1.6 se cumple y se midió: `cambio10 = 12500` y los valores de
  `nsit10 / stock10 / regen10` de `equipos/fase10/F1_fable_poderes/corre_mundo_fase10.py` (bloque MUNDO). Con la calibración de F0
  (`r_vis 8, parches 6, cap 5, regen 30, vida_parche 8000, cambia_cada 5000`) el ancla se rompe (RENACE 0.063): F0 lo predijo y lo declaró.
- Ambos preregistros (`PREREGISTRO_mundo_fase10.md` en cada carpeta) traen la letra de M10-1..5 con nulo, margen, n y placebo, y las
  predicciones firmadas con probabilidad. El de F0 es más completo en anclas e identidad; el de F+ en §2.1 y en el ancla.

**Comandos (un proceso; la serie sólo el coordinador, con Pool):**
```
cd C:\Users\User\Documents\PROYECTOS\JUACO-EXO\equipos\fase10\F0_fable_solo
set PYTHONIOENCODING=utf-8
python construye_mundo_fase10.py          # reconstruye mundo_fase10.py y verifica los shas (tripwire)
python identidad_mundo_fase10.py          # arnés 79/79, ~4-5 min
python corre_mundo_fase10.py --humo       # 6 corridas, T=100 000, escribe datos/humo/*.json (~2 min)
python corre_mundo_fase10.py --serie --desde 2401 --pool 7     # SÓLO si el director decide correrla igual; réplica --desde 2421
```
Semillas 2401–2440 verificadas libres por los dos brazos (grep en `experimentos/`, `registro/`, `datos/`); reservarlas en JUACO al copiar.
Al copiar la carpeta a `experimentos/nivel10_mundo_acumula/`, cambiar las rutas absolutas del `construye` a relativas al repo y volver a
correr el tripwire.

## 4. Qué NO hacer

No correr la serie confirmatoria con la letra actual "a ver qué pasa": los dos brazos predicen que M10-1 y M10-2 caen (F0: < 5 % de que
algún brazo cruce R₀ 1 en alguna semilla; F+: M10-1 cae al 90 %). Sería gastar 240 corridas para documentar otro techo del mundo actual
(ENCARGO §1: "cada nivel que cerramos con este mundo documenta un techo, no un peldaño").

## 5. Defectos de la letra del encargo que los brazos encontraron (declarados, no recalibrados; ERR los numera el coordinador)

1. **M10-2 está sesgada contra la acumulación** (F0): compara cuerpos 5..12 contra el cuerpo 1, que nace con E = 1.0, sin cambios, y vive
   1 198 pasos contra 184. Propuesta M10-2′: 5..12 contra 2..4, pareado por semilla.
2. **M10-3 mide "leer el nodo", no "acumular por el cambio"** (F0): el cuerpo 1 nunca lee en ningún mundo. Propuesta M10-3′ con la misma
   razón entre generaciones que M10-2′, en MUNDO_FIJO.
3. **La medida de cobertura de M10-2 sale degenerada** (F+): mediana 0.0 y puede pasar de 1. Propuesta: cobertura por ventana entre viradas.
4. **`cob_s` del cuerpo vacío ≈ 0.5 por azar de signo** (F0): leer con `cob_c`.
5. **Regla 3 del método** (F0, autodeclarado): calibró el mundo con 50 mini-corridas de un proceso a T = 20 000 (~3 min de CPU), más de las
   6 que permite la regla por humo. Candidato a ERR de procedimiento; la calibración quedó registrada corrida a corrida.

## 6. Decisiones para el director (en orden)

1. **La boca del organismo.** Lee sólo la fila de la necesidad activa; es la causa medida de que un mundo que cobra "dónde" mate hasta al
   inmortal, y también ocurre en el mundo del tronco. Cambiarla (leer las dos filas, o vetar por cualquier necesidad) es un **candidato al
   tronco**: preregistro propio, las siete puertas de `CRITERIO_TRONCO_v2`, identidad con la perilla apagada. No es parte del diseño del
   mundo y ningún brazo la tocó.
2. **Exploración.** Con retina vacía el cuerpo no se mueve (p ≈ 0.005). Decidir si la exploración entra por el mundo (recursos que obligan) o
   es otro candidato al tronco, ANTES de fijar §2.1.2 ("saber dónde vale tanto como saber qué").
3. **Retirar el mapa de nivel 6 como canal del DÓNDE** en este mundo (medido ×2: no ayuda o empeora). Si el DÓNDE entra, que lo exija el
   mundo (F+: "el sitio como un entero más en el mensaje del linaje" es la vía mínima que probó; llegó a R₀ 0.24–0.29, no basta sola).
4. **Adoptar M10-2′, M10-3′ y la cobertura corregida** como correcciones declaradas con ERR, con semillas nuevas.
5. **Si se corre algo ya:** el humo de F0 con la calibración de F+ (un proceso, 2 minutos) para confirmar que el ancla se conserva en el
   instrumento recomendado antes de reservar CPU.

## 7. El caso de estudio que produjo esto (para el registro, no para la decisión)

Pregunta del director: ¿Fable mejora con todos los poderes (memoria del exo compartida, `PODERES.md`, aprendices Haiku)? Rúbrica escrita
antes (`CASO_FASE10.md`), aceptación = §5 del encargo. Auditoría independiente reprodujo arneses, shas y mundos.

| criterio (máx) | F0 Fable solo | F+ Fable + poderes | H+ Haiku + poderes |
|---|---|---|---|
| aceptación §5 (35) | **34** | 33.5 | 6 |
| requisitos del mundo §2.1 (18) | 13 | **14.5** | 5 |
| método (15) | 12 | 12 | 9 |
| trampas y ERR (8) | 8 | 8 | 5 |
| auditoría (12) | **12** | 9 | 0 |
| uso de poderes (6) | 3.5 (media) | **6** | 1 |
| coste (6) | 5.7 | **6** | 6 |
| **total** | **88.2** | **89.0** | **32.0** |
| sólo el paquete (1–5, /88) | **79** | 77 | 25 |
| tokens / tiempo | 437 k / 61 min | 412 k / 57 min (+53 antes de un corte 529) | 124 k / 8 min |

**Veredicto del caso: los poderes no hacen a Fable mejor en el paquete (79 contra 77); lo hacen igual de bueno, un poco más barato y
más trazable (memoria con 11 lecciones, 5 aprendices auditados). El total 89.0 contra 88.2 es ruido.** La tesis "Fable mejora con
poderes" NO se sostiene por la letra de la rúbrica (F+ > F0 por 0.8, dentro del error de un criterio); tampoco se refuta (F+ no quedó por
debajo). **Haiku con poderes no llegó**: entregó papel sin ejecutar nada, con una excusa falsa ("sin acceso al repo") que sus propios
aprendices desmienten; su humo, corrido por el auditor, escribió un JSON vacío. Ambos Fable sufrieron un corte del servidor (HTTP 529) y
se reanudaron; los costes lo incluyen.

Lo que sí aportaron los poderes, medible: F+ fue el único que cumplió y midió el ancla §2.1.6, y registró cada tropiezo (el `evitar` de la
memoria volvió antes del humo). Lo que aportó no tener poderes: F0 fue más a fondo en el organismo (diagnóstico de la boca) y en el arnés.

## 8. Procedencia por sección
§1 árbitro sobre ambos informes · §2 F0 (`F0_fable_solo/INFORME.md`, `REGISTRO.md` 20:08) y F+ (`F1_fable_poderes/INFORME.md`) · §3
auditor (`_evaluacion/AUDITORIA_tres_brazos.md` (b)) · §4 ambos · §5 F0 (1, 2, 4, 5) y F+ (3) · §6 auditor (c) y árbitro · §7 auditor
(tabla) y `_evaluacion/costes.md`. Nada de esto se ha corrido con Pool ni se ha declarado; son diseño, identidad y humo.
