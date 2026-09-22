# INFORME DE INTEGRACIÓN — el mundo de la fase 10 (resultado externo de JUACO-EXO), 22-sep-2026

**HAY ALGO MODESTO.** El instrumento externo de F0 está en el repo y verificado aquí (tripwire de 15 shas; arnés 79/79 dos veces). El fenómeno
central se reproduce: con sed, la boca muerde el veneno que ya sabe malo. Pero hay dos cosas que NO salen. La calibración de F1 no conserva el
ancla en el instrumento de F0 (RENACE 0.26). Y quitar el mordisco con un veto no rescata al linaje: en el mundo del tronco lo hunde. La boca no
es el muro por sí sola. **No correr la serie con esta letra.**

Misión: llegar a la AGI por este camino; lo externo es hipótesis. Sin Pool, sin commits. Seis procesos en total, todos de uno en uno: dos
arneses, un humo, un diagnóstico, un arnés con mini-prueba y el constructor.

## 1. Qué hice (en orden del encargo)
| paso | resultado | archivo |
|---|---|---|
| 1 copia + rutas relativas | `construye_*`, `identidad_*`, `corre_*` de F0 con `JUACO = AQUI/../..`. Originales intactos en `externo/`, con F1, la evaluación y el caso | esta carpeta |
| 1 tripwire | Pasa: origen `3a821884394d66c9` + 7 de cadena + 7 donantes = 15 shas. El `mundo_fase10.py` regenerado es **byte a byte** el de F0 (`84e97674f709a900`). Aborta si se altera el sha del origen o el de un donante (lo probé las dos veces) | `construye_salida.txt` |
| 1 identidad (sin mirar números) | **79/79** con la letra de F0 (254 s) y **79/79** con la ENMIENDA 1 (238 s). Las líneas de casos son idénticas a las de F0; sólo cambian los shas del runner y el conteo de D5 (3 → 1 cambios). La salida está pegada en el Anexo A | `identidad_mundo_fase10_salida_{F0calib,enmienda1}.txt` |
| 2 enmienda | ENMIENDA 1 en PREREGISTRO §12, sellada antes del humo (sha `29cb585e1156b198`). Cambia `cap` 5→25, `regen` 30→50 y `cambia_cada` 5000→12500; `parches` se queda en 6. **Aquí va el ERR (`ERR-? pendiente`, Anexo B-6)** | `PREREGISTRO_mundo_fase10.md` §12–§13 |
| 3 humo | 6 corridas, un proceso, identidad interna 5/5, HH1/HH2/HH6 SÍ. **NADA 0.146/0.150 (mediana 0.148): dentro de 0.10–0.30. RENACE 0.306/0.214 (mediana 0.26): FUERA de 0.80–1.30 → el ancla NO se conserva** | `datos/humo/mundo_fase10_humo_20260922_123306.json` (`340d9414b4822ed8`) |
| 5 diagnóstico | 6 corridas, un proceso. Criterio de reproducción escrito en el script antes de correr | `datos/humo/diagnostico_boca_mapa_20260922_123508.json` (`299352724963a791`) |
| 6 sonda del candidato | `organismo_boca2.py` por anclas desde `mundo_fase10` (0 sorteos). Arnés 11/11: apagada idéntica; **inerte con n_nec = 1**. Mini-prueba de 6 corridas con predicciones selladas antes | `ESBOZO_PREREGISTRO_boca_dos_filas.md` (§1–§7 `518e5ca1099f2f19`), `datos/humo/mini_boca2_20260922_124015.json` (`09dd2c8c075e3d86`) |

## 2. Hallazgo central: ¿se reproduce?
Mordidas / exposiciones, sólo en los tipos que no cambiaron de valencia. Criterio: la tasa de "veneno con SED" y la de "sal con HAMBRE" tienen
que ser cada una al menos el doble que la de la otra necesidad, con al menos 10 exposiciones.

| corrida (RENACE, s1, T 20 000) | veneno con SED | veneno con HAMBRE | sal con HAMBRE | sal con SED | externo (F0) |
|---|---|---|---|---|---|
| mundo vivo del tronco (fase 9, v14.2) | **63/84 (0.75)** | 2/763 | **77/487 (0.16)** | 4/128 | 75/83 · 101/508 |
| F10, letra F0 | **60/68 (0.88)** | 6/174 | **44/101 (0.44)** | 6/122 | 57/63 · 85/259 |
| F10, letra F0 sin cambios | 71/79 (0.90) | 13/268 | 102/324 (0.31) | 8/239 | — |
| F10, ENMIENDA 1 | 18/27 (0.67) | 5/469 | 121/353 (0.34) | 5/47 | — |

- **H-BOCA ("llega y no se usa porque la boca decide con la fila activa"): REPRODUCIDA EN DIRECCIÓN, 4/4.** Las cifras no son las de F0: F0 no
  dejó ni el script ni el JSON de esas cuentas. La causa está en el código: `EFECTO['veneno'] = (-0.4, 0.0)`, así que la fila de la sed recibe
  R = 0 y nunca aprende que el veneno es malo.
- **"Llega": parcial.** El recién nacido sí lee el nodo (`lect_div` > 0, HH2). La cobertura de ORÁCULO_SIN_MAPA es 0.81 contra 0.25–0.50 de
  NADA, con n = 1.
- **H-MAPA ("el mapa del nivel 6 no sirve como canal del DÓNDE"): CONSISTENTE EN DIRECCIÓN, 2/2 pares, n = 1.** ORÁCULO 0.188 contra
  ORÁCULO_SIN_MAPA 0.265; REL 0.102 contra REL_SIN_MAPA 0.222. Sólo pude probar el mapa del individuo. El canal "sitio en el mensaje" de F1
  no está en este instrumento.
- **Lo nuevo (sonda, n = 1).** El veto de la otra fila quita el mordisco (veneno con SED 63/84 → 2/224). Aun así el inmortal del mundo del
  tronco cae de R₀ 1.154 a **0.045**. Allí lo malo sólo desaparece si se muerde. Lo rechazado se queda ocupando sitio, y las exposiciones a
  lo bueno bajan de 243 a 73. En la ENMIENDA 1, donde los sitios se reponen, el veto sí ayuda (0.48 → 0.60, 0.31 → 0.48, NADA 0.15 → 0.22),
  pero no lleva al ancla (mediana 0.33).

## 3. Predicciones mías refutadas (declaradas)
- Sonda M1: predije R₀ ≥ 1.154 con el veto (70 %). **Salió 0.045.**
- Sonda M2: predije R₀ mayor que sin veto (80 %). **Salió 0.028 contra 0.065.**
- Sonda M5: predije R₀ entre 0.4 y 1.3. **Salió 0.173.**
- Acertadas: la ancla cae (P 0.20 de que se conservara); NADA 0.08–0.35; RENACE 0.25–1.00 (0.26, en el borde); H-MAPA; el veto 4/4; M3, M4 y M6.

## 4. Qué falló o no pude verificar
- **La ENMIENDA 1 queda refutada como calibración.** La calibración de F1 se eligió mirando las semillas 1–4 en otro mundo: 8 tipos, sin
  mudanza por edad del sitio, sin cambio de familia entera, e INMORTAL sin mapa. No se transfiere.
- No verifiqué la exploración con retina vacía (p ≈ 0.005). Tampoco corrí las baterías del tronco: M10-4 queda cubierta por identidad.
- La etiqueta del caso D5 del arnés dice "5000" aunque con la enmienda el valor es 12500. Es sólo el texto: el control sí difiere.
- **Sobre la "desviación de la regla 3":** en los archivos no hay Pool. Lo documentado es exceso de corridas en un solo proceso: F0 lo
  declaró; F1 también lo hizo y no lo declaró (Anexo B-5).

## 5. Semillas
- **Usadas o reservadas:**
  - Repo: hasta 2360.
  - Carrera: 3001–3299. Escuderías: 4001–4199 y 5001–5020.
  - Letra externa: 2401–2440 (reservadas, nunca corridas).
  - Humos externos: 1–2 (F0 y F1) y 1–4 (sondas de F1).
  - H+: 1741 y 1751 (humo), 1761–1780 (propuestas). **Se solapan con el rango del repo: no usarlas.**
  - Mis humos: 1, 5, 6. Ya estaban usadas; un humo no reserva.
- **Propuestas, libres por grep en `experimentos/`, `registro/` y `datos/` el 22-sep:**
  - 2441–2480: letra de la ENMIENDA 1. Asignadas, **no correr** (el ancla cayó) y no reutilizar.
  - 2481–2520: letra corregida M10-2′/M10-3′ y cobertura (serie 2481–2500, réplica 2501–2520).
  - 2521–2800: candidato boca2. Examen 2521–2540, T-A 2541–2580, T-C ii 2581–2620, T-G 2621–2660, réplica 2661–2800.
  - 2801–2840: calibración del mundo, si se hace como bloque propio.

## 6. Las seis decisiones (las 5 de §6 de la evaluación + la 6.ª de su §4), con coste
| # | decisión | evidencia del repo hoy | coste | recomendación |
|---|---|---|---|---|
| 1 | **La boca: candidato "lee las dos filas" (VETO)** | mordisco reproducido 4/4; el veto lo quita, pero el inmortal del mundo del tronco cae de 1.15 a 0.05 (n = 1) | paquete tipo dE5: una sesión de agente + ~25 min de Pool 7 por serie. Esbozo de las siete puertas con v2 y v3 lado a lado en `ESBOZO_*` | **no preregistrar tal cual.** P de entrar: v2 ≈ 0.02 / v3 ≈ 0.10 (T-A caería). Antes, decidir el 2 |
| 2 | Exploración con retina vacía | no verificada. La sonda sugiere que el veto sólo sirve si el cuerpo se aleja de lo rechazado | diagnóstico de un proceso: 15 min | **va antes que el 1**: medir si "veto + alejarse" es un solo mecanismo |
| 3 | Retirar el mapa del nivel 6 como canal del DÓNDE | 4 pares (2 externos y 2 del repo), todos en la misma dirección, n = 1 cada uno | cero: quitar el mapa de los brazos candidatos | sí, provisional (dirección, no declaración) |
| 4 | Adoptar M10-2′, M10-3′ y la cobertura corregida, con ERR | sesgo visible también en el humo del repo: cuerpo 1 con 170–1049 exposiciones contra 2.5–142 de los cuerpos 5..12 | editar el runner + humo: 30 min | sí, pero sólo cuando la serie tenga sentido |
| 5 | Humo de F0 con la calibración de F+ | **HECHO: el ancla cae** (RENACE 0.26) | — | elegir: el instrumento F1 entero (tripwire + arnés + humo, ~40 min) o una calibración del mundo como bloque con semillas 2801+ |
| 6 | Correr la serie con la letra actual | ancla caída + H-BOCA | 240 corridas, ~15 min | **NO** |

## 7. Qué le toca decidir al director
(a) El orden: primero la exploración (2) y después la boca (1), o dejar la línea. (b) El instrumento: F1 entero, o F0 con una calibración
preregistrada y propia (5). (c) Aprobar los ERR del Anexo B.

---
## Anexo A — salida del arnés con la ENMIENDA 1 (la de la letra F0 es idéntica caso a caso; ver el diff en el §1)
```
VEREDICTO identidad_mundo_fase10: PASA  79/79   (238s, un proceso)
I10 1/1 · I1 24/24 (12 escenarios x 2 semillas, T 30 000) · I2 1/1 (T 120 000) · I3 18/18 (9 brazos de corre_f9 x 2) · I4 4/4 · I5 4/4 · I6 2/2 ·
I7 4/4 · I8 1/1 · I9 1/1 · D1–D13 14/14 DIFIEREN · G1–G5 5/5
```
Salida completa, línea por línea: `identidad_mundo_fase10_salida_enmienda1.txt` (sha `039e777d379a95c2`) y `…_F0calib.txt` (`1d58c38149726fbf`).
Arnés de la sonda boca2: `mini_boca2_salida.txt`, 11/11.

## Anexo B — ERR redactados (sin numerar: `ERR-? pendiente`; los numera el coordinador con `/juaco-err`)
**B-1 · ERR-? pendiente — M10-2 sesgada contra la acumulación (F0).** El "cuerpo 1" es el fundador. Nace con E = Ag = 1.0, antes del primer
cambio, y vive 1 198 pasos; los cuerpos 5..12 viven 184 (humo de F0). En el humo del repo las exposiciones son 170–1049 contra 2.5–142. La
razón 5..12 / 1 mide "nacer rico y temprano" y no acumulación. **Corrección M10-2′:** cuerpos 5..12 contra cuerpos 2..4, pareado por semilla
(misma dote y mundo ya cambiante). Se conservan la razón ≥ 2.0, A₁₂ pareado ≥ 0.85 y NODO_BARAJADO ≤ 1.2. Semillas nuevas 2481–2520. No
rejuzga nada: nunca corrió.

**B-2 · ERR-? pendiente — M10-3 mide "leer el nodo", no "acumular por el cambio" (F0).** El cuerpo 1 nunca lee en ningún mundo, así que la
razón 5..12 / 1 en MUNDO_FIJO sale > 1.2 aunque el mundo blando no exija acumular. **Corrección M10-3′:** la misma razón que M10-2′ (5..12 /
2..4), en MUNDO_FIJO, ≤ 1.2×.

**B-3 · ERR-? pendiente — la cobertura de M10-2 sale degenerada (F1; también en F0).** En F1 la mediana es 0.0 y puede pasar de 1. En el
`expl5` de F0 también dominan los ceros: 0.0 en 4 de las 12 corridas de los dos humos, y ≤ 0.08 en 11 de 12. **Corrección:** cobertura por ventana entre viradas. Es
la fracción de combinaciones (tipo bueno × cuarto) buenas en esa ventana que explota el cuerpo vivo en ella. Se acota a ≤ 1 por construcción y
se reporta con las exposiciones de la ventana (trampa 3).

**B-4 · ERR-? pendiente — `cob_s` acierta el signo por azar (F0).** La vía lenta lineal generaliza por píxeles compartidos, así que un cuerpo
sin herencia acierta el signo en ~0.5 de las celdas (humo del repo: NADA 0.25–0.69). V-4 ("una vida < 0.50") queda casi insatisfacible por
azar (familia de ERR-45). **Corrección:** V-4 y toda cobertura se leen con `cob_c` (|v| ≥ 0.5), con nulo = `cob_c` de NADA y un margen
declarado. `cob_s` sólo se reporta.

**B-5 · ERR-? pendiente — regla 3 en la calibración externa (F0 declarado, F1 no declarado).** F0 hizo 50 mini-corridas de T 20 000 en un
proceso (~780 000 pasos). F1 hizo al menos 24 corridas de T 40 000 en `sonda_ancla_cambio` (~960 000 pasos), más barridos de `r_vis` y de
`cambio10`. Además F1 **eligió** `cambio10` mirando el ancla en las semillas 1–4. No hay Pool en ningún archivo: la desviación es de volumen, no
de paralelismo. **Corrección:** una calibración de mundo es un bloque propio (barrido declarado, semillas de calibración separadas de las de
serie, presupuesto de corridas escrito) o la corre el coordinador. Una calibración externa nunca se importa sin volver a medir su ancla en el
instrumento del repo; hoy no se transfirió.

**B-6 · ERR-? pendiente — ENMIENDA 1 (integrador): recalibración del mundo después de ver caer V-6 en el humo de F0.** Es admisible sólo
porque V-6 es de validez del instrumento, ningún umbral cambió y se juzgó en semillas nuevas (5 y 6; la serie en 2441+). **Resultado: el ancla
no se conserva, así que no hay enmienda 2 con estas semillas.**

## Anexo C — texto propuesto (NO editado: lo pega el coordinador)
**REGISTRO_etapas_1_2.md:** "22-sep. Integración del resultado externo de la fase 10 (JUACO-EXO, tres brazos; hipótesis). Instrumento F0 en
`experimentos/nivel10_mundo_acumula/`: tripwire de 15 shas OK, `mundo_fase10.py` byte a byte (`84e97674f709a900`), arnés 79/79 ×2. ENMIENDA 1
(calibración de F1 sobre el instrumento de F0; ERR-?) sellada antes del humo (`29cb585e1156b198`). Humo de un proceso (`340d9414b4822ed8`):
NADA 0.148 dentro del ancla; RENACE 0.26 FUERA, así que la enmienda queda refutada y la serie no se corre. Diagnóstico (`299352724963a791`): la
boca muerde el veneno con sed 0.67–0.90 contra 0.003–0.05 con hambre, 4/4 corridas (hallazgo externo reproducido en dirección). Sonda boca2
(`09dd2c8c075e3d86`, n = 1): el veto quita el mordisco (63/84 → 2/224) pero el inmortal del mundo del tronco cae de 1.15 a 0.05 porque lo
rechazado no se retira del mundo. La boca no es el muro por sí sola. ERR-? ×6 (Anexo B del informe)."
**ESTADO.md (Pendiente):** "Fase 10: instrumento F0 integrado y verificado. El ancla no se conserva con la calibración de F1. Decisión del
director: exploración antes que boca; instrumento F1 o calibración propia. Semillas 2441–2840 asignadas (ver INFORME_INTEGRACION §5)."
