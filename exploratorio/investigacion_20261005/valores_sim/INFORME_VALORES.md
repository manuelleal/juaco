# INFORME VALORES — ¿una colonia de células gana centavos en valores? (5-oct-2026, simulación, preregistrado, tramo sellado abierto una vez)

**NO.** En el tramo sellado (2015-01-02 a 2017-12-29, 31 acciones grandes de EE. UU., 755 días), ninguna de las cuatro colonias supera a comprar y mantener ni al azar con la misma frecuencia, netas de costos: las dos que operan pierden contra mantener (−7.3 y −2.8 puntos por año) y empatan con el azar; las dos con cuarentena no operan y son comprar y mantener. Repite INFORME_DERIVA: con ruido, lo mejor que hace la célula es callarse.

**Esto es una simulación con datos históricos. No es consejo de inversión. Cero dinero real, cuentas, órdenes o claves.**

## Tabla del tramo sellado (rendimiento anual en %, peso igual; costo base 7.5 pb por lado + 1 pb/día en corto)
| brazo | costo 0 | costo base [IC95] | costo doble | Sharpe | caída máx | meses + | operaciones | centavos netos por operación por 100 USD (0 / base / doble) | pisa |
|---|---|---|---|---|---|---|---|---|---|
| (a) comprar y mantener | +12.4 | +12.4 [+0.5, +23.8] | +12.3 | 1.03 | 13.3 % | 0.72 | 31 | +3715 / +3700 / +3685 | — |
| (b1) momento 250 d | +5.0 | +3.2 [−2.9, +9.4] | +1.5 | 0.58 | 11.3 % | 0.61 | 602 | +76.8 / +49.7 / +22.6 | — |
| (b2) reversión 5 d | +6.8 | −2.7 [−9.2, +4.1] | −12.1 | −0.32 | 14.0 % | 0.44 | 5010 | +12.6 / −5.0 / −22.5 | — |
| (d) colonia original | +9.5 | +5.0 [−5.5, +15.2] | +0.5 | 0.48 | 15.9 % | 0.61 | 2680 | +32.8 / +17.4 / +1.9 | 7.9 % |
| (e) cuarentena original | +12.4 | +12.3 [+0.5, +23.8] | +12.3 | 1.03 | 13.3 % | 0.72 | 35 | +3290 / +3275 / +3260 | 0.01 % |
| (f) colonia de dinero (enmienda) | +11.4 | +9.5 [−1.4, +20.1] | +7.7 | 0.85 | 12.5 % | 0.72 | 1114 | +95.1 / +79.6 / +64.0 | 2.7 % |
| (g) dinero + cuarentena (enmienda) | +12.4 | +12.4 [+0.5, +23.8] | +12.3 | 1.03 | 13.3 % | 0.72 | 31 | = (a) | 0 % |
| control: (d) con pago barajado | +10.0 | +5.5 [−4.9, +15.8] | +0.9 | 0.53 | 15.9 % | 0.58 | 2726 | +34.1 / +18.6 / +3.1 | — |

Los "centavos por operación" positivos de (d) y (f) NO son señal: están largas 92–97 % del tiempo en un mercado que subió; el azar con la misma frecuencia da lo mismo.

**Comparaciones primarias (8, Bonferroni 99.375 %), costo base, puntos por año:**
| | menos mantener | menos azar (500 sorteos) | p del azar |
|---|---|---|---|
| (d) | −7.34, IC95 [−12.13, −1.81], corregido [−14.31, +0.96] | −1.28, IC95 [−5.82, +3.67], corregido [−8.01, +6.22] | 0.914 |
| (e) | −0.01 [−0.08, +0.04] | −0.00 [−0.07, +0.05] | 0.500 |
| (f) | −2.81, IC95 [−5.06, −0.80], corregido [−5.93, +0.01] | −0.30, IC95 [−2.30, +1.50], corregido [−3.17, +2.16] | 0.676 |
| (g) | 0 (no operó) | 0 | 1.000 |

A costo 0 tampoco: (d) −2.9 [−7.7, +2.8] y (f) −1.0 [−3.1, +1.0] contra mantener. Al pisar, (d) acierta la clase 33.6 % y el base fallaba 55.5 % de esas veces contra 55.3 % global: la célula no elige mejor que el azar dónde pisar. Pago barajado ≈ (d): no hay mecanismo que barajar. Acierto de signo de todos los brazos: 50.6–51.4 %. Con un día de retardo: (d) +3.0, (f) +7.3, momento +2.9, reversión −5.9. Nada cayó en "sospechoso de error".

## Prueba de fuga
- **Truncado bit a bit: pasa.** Rasgos y posiciones de los 7 brazos idénticos con los datos cortados 150 días antes; una regla con fuga plantada sí es detectada.
- **Barajada original: FALLÓ para momento** (bruto −3.0 %/año, t = −3.6; los demás |t| < 0.4). Es fallo de mi auditor (restar la media de toda la muestra a una permutación crea reversión artificial), de signo contrario a una fuga a favor. **Barajada con signo al azar (enmienda 2b): pasa** para todos (bruto entre −0.6 y +0.7 %/año, |t| < 0.9). La regla con fuga da +307 %/año: la auditoría ve.
- **Señal plantada (sintética)**: la reversión simple la detecta (+12.0 %/año neto, IC95 [+1.4, +21.6]; no excluye 0 al 98.75 %). **Ninguna colonia la detecta**: (d) −4.5 contra mantener, (e) 0 pisadas, (f) y (g) empatan (p del azar 0.05–0.07). Sin señal, nadie gana. Por la regla del preregistro, el NO se lee como **"la colonia no sirve de detector"**, no como "no hay señal en el mercado".

## Qué falló
- **stooq.com no dio CSV** (devuelve verificación de navegador con JavaScript; no la esquivé); Yahoo 401; FRED sin conexión. Usé una copia pública en GitHub del conjunto "DJIA 30 Stock Time Series" (URL, fecha y sha256 en PREREGISTRO §1): termina en 2017, sin fondos índice, sin dividendos, con sesgo de supervivencia.
- **Enmienda 1 antes de abrir el sellado** (texto en PREREGISTRO, copias previas en `datos/*_v1.json`): vistas la validación y la sintética, añadí (f), (g), la auditoría 2b y subí Bonferroni de 4 a 8. Es un cambio después de mirar validación; el sellado no se había leído.
- La regla de limpieza anuló un movimiento real (AABA +48 % el 2008-02-01); se dejó como estaba escrito.
- (e) no puede validar casi nada por construcción cuando 31 instrumentos comparten el mismo día (los fallos cuentan todos, las confirmaciones una por semana); en sombra acierta 45 %.
- Mis predicciones refutadas: (d) pisaría 15–60 % (pisó 7.9 %); centavos por operación de (d) en [−25, +5] (salió +17.4, por exposición larga); que alguna colonia detectara la señal plantada (p 0.15–0.40: ninguna). Cumplidas: NO (p 0.85), rangos de (a), (b1), (b2), (e), (f), (g), barajada ≈ (d).

## Qué no se verificó
Un solo tramo sellado y un solo mercado/periodo (sin réplica independiente); datos de tercera mano sin cotejar; costos supuestos, sin impacto ni disponibilidad de cortos; operar al cierre con la señal del mismo cierre; rivales mínimos (sin regresión ni árboles); 12 rasgos fijos de precio y volumen; perillas internas de (f)/(g) (E0, t ≥ 2, 3 nacimientos/día) sin barrido; la señal plantada es una sola forma (reversión lineal).

## Qué haría falta para el siguiente peldaño
1. Antes que nada, que la colonia detecte una señal plantada: hoy no ve una correlación de 0.1 que una regla de una línea sí ve. Sin eso, noticias o un modelo de lenguaje no cambian el resultado.
2. Datos con fecha y hora de publicación verificables (noticias, resultados), con la hora en que fueron públicos, para que el reloj siga siendo estricto; precios ajustados por dividendos, con las empresas que salieron del índice, hasta 2026.
3. Modelo de lenguaje local congelado con fecha de corte de entrenamiento ANTERIOR al tramo sellado (si no, el modelo ya "leyó" el futuro: fuga por memoria); su salida entraría como rasgo, y el rival obligatorio sería una regresión sobre ese mismo rasgo.
4. Mi recomendación: no seguir esta línea con la colonia tal como está; el antecedente (DERIVA) y este resultado dicen lo mismo.

Archivos: `PREREGISTRO.md`, `valores.py` (`--humo`, `--etapa valida|auditoria|sintetica`, `--congela`, `--abrir-sellado`), `analiza.py`, `datos/` (`sellado.json`, `validacion.json`, `auditoria.json`, `sintetica.json`, `humo.json`, `CONGELADO.json`, `tablas.txt`, `*_v1.*`, `csv/`). Un proceso, numpy puro, ≈ 12 min de CPU en total.
