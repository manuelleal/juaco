# PREREGISTRO — valores_sim (5-oct-2026). Escrito ANTES de calcular un solo rendimiento

Misión: llegar a la AGI por este camino. Pregunta del director: ¿un sistema chico (colonia de células) puede ganar
centavos de dólar en valores? Esto es un **laboratorio de simulación con datos históricos**. Cero dinero real, cero
cuentas, cero órdenes, cero claves. **No es consejo de inversión.** Sólo mide si hay señal.

Lo único que vi de los datos antes de escribir esto: las 3 primeras líneas del CSV (cabecera y dos filas de MMM de
2006) y el conteo de filas por símbolo (31 símbolos, 3019–3020 días, sin celdas vacías en Close/Volume).

## 1. Datos
- **Pedido**: stooq.com. **Falló**: `https://stooq.com/q/d/l/?s=spy.us&i=d` (y stooq.pl) devuelve una página de
  verificación de navegador con JavaScript (796 bytes, no CSV). No la esquivo. Yahoo `v7/finance/download` → 401.
  FRED `fredgraph.csv` → conexión reiniciada.
- **Usado**: `https://raw.githubusercontent.com/szrlee/Stock-Time-Series-Analysis/master/data/all_stocks_2006-01-01_to_2018-01-01.csv`
  descargado el 2026-10-05, 4 478 864 bytes, sha256
  `d796906ae3797b950d23cea8e4839072c4bde60a6b97886ee6fede9b793e191c`. Copia pública del conjunto "DJIA 30 Stock
  Time Series": 31 acciones grandes de EE. UU. (las 30 del Dow de 2017 + AABA/AMZN/GOOGL según el archivo),
  diario, 2006-01-03 a 2017-12-29 (12 años), columnas Date, Open, High, Low, Close, Volume, Name.
- **Límites conocidos de estos datos, declarados antes**: (i) sesgo de supervivencia (son las que en 2017 eran
  grandes: favorece a comprar y mantener y a todo lo largo); (ii) cierre SIN dividendos (perjudica a lo largo ~2 %/año
  y favorece a lo corto; se compensa cobrando a los cortos, ver costos); (iii) terminan en 2017: no hay 2018–2026;
  (iv) no hay fondos índice, sólo acciones; (v) fuente de tercera mano sin verificar contra el mercado.
- Limpieza (regla fija): calendario = unión de fechas; un cierre faltante se rellena con el anterior (rendimiento 0,
  volumen = el anterior). Un rendimiento diario con |r| > 40 % se trata como error de dato: se pone en 0 y se lista.
- **Serie sintética** (además, porque la fuente pedida falló y para validar el instrumento): 31 instrumentos × 3020
  días, factor de mercado + ruido propio (vol diaria total ≈ 1.5 %), deriva 4 pb/día. Versión SIN señal y versión CON
  señal plantada: E[r(t+1)] = deriva − 15 pb · clip(z5(t), −2, 2), con z5 = rendimiento de 5 días dividido por su
  desviación (reversión plantada, correlación diaria ≈ 0.1). Semilla 20261005.

## 2. Reloj y auditoría de fuga
- Decisión al cierre del día t con datos hasta el cierre de t (incluido). Posición p(i,t) ∈ {−1, 0, +1} por
  instrumento. Se cobra p(i,t) · r(i,t+1), con r(i,t+1) = C(t+1)/C(t) − 1. Supuesto estándar declarado: se puede operar
  al cierre de t con la señal de ese cierre. **Variante con retardo** (secundaria): la posición decidida en t se toma al
  cierre de t+1 y cobra r(t+2).
- Todo rasgo usa sólo pasado: medias/desvíos móviles hasta t. La colonia aprende del resultado de t sólo después del
  cierre de t y antes de decidir t (fase "aprende lo de ayer", luego fase "decide hoy" SIN aprender: una decisión no
  puede ver el resultado de otro instrumento del mismo día).
- **Auditoría 1 (truncado, bit a bit)**: las posiciones de todos los brazos calculadas con los datos cortados en un
  día T deben ser idénticas a las posiciones hasta T calculadas con todos los datos. Si no, hay fuga y se para.
- **Auditoría 2 (barajada)**: los días de cada instrumento se permutan (cada instrumento su permutación; rendimiento y
  volumen juntos) y a cada instrumento se le resta su media: toda regla tiene ganancia BRUTA esperada 0. 5 semillas de
  barajado. Pasa si para todo brazo activo la media bruta diaria (5 semillas juntas) tiene |t| < 3 y |bruto anual| < 3 %.
- **Auditoría 3 (señal plantada)**: en la sintética CON señal la reversión simple debe ganar neto (> 0, intervalo que
  excluya 0) y en la sintética SIN señal ningún brazo activo debe superar a comprar y mantener con intervalo que
  excluya 0. Se reporta además si la colonia detecta o no la señal plantada (si no la detecta, un NO en datos reales
  habla de la colonia y no sólo del mercado; se dirá así).

## 3. Costos (por lado = por cada unidad de cambio de posición; pasar de +1 a −1 son 2 lados)
- Base: **7.5 pb por lado** = comisión 1 pb + medio diferencial 2.5 pb + deslizamiento 4 pb.
- Cortos: además 1 pb por día en corto (dividendo que el corto paga + préstamo), escalado con el nivel de costo.
- Se repite con **costo 0** y **costo doble (15 pb por lado, 2 pb/día en corto)**. Las posiciones son las de la
  corrida base (congeladas); sólo se recalcula el cobro. El costo de entrada inicial y de cierre final se cobra.
- Sin apalancamiento: capital repartido a partes iguales, 100 USD nocionales por instrumento.

## 4. Tramos
- Calentamiento: primeros 250 días (rasgos). Desarrollo: desde el día 250 hasta 2011-12-30.
- **Validación**: 2012-01-03 a 2014-12-31 (aquí se eligen TODAS las perillas).
- **SELLADO**: 2015-01-02 a 2017-12-29 (3 años, ~755 días). El código corta físicamente los datos en 2014-12-31
  salvo con `--abrir-sellado`, que exige `datos/CONGELADO.json` (sha256 del código y perillas elegidas) y se niega si
  el código cambió o si `datos/sellado.json` ya existe. Se abre **una sola vez**. Nada se ajusta después.
- La colonia sigue aprendiendo en línea dentro del sellado (eso es avance en el tiempo legítimo); sus perillas no cambian.

## 5. Brazos
- **(a) comprar y mantener**: +1 en todo, siempre (peso igual, sin rebalanceo de costos más que entrada y salida).
- **(b1) momento simple**: p = signo del rendimiento de los últimos n días; n ∈ {20, 60, 120, 250} elegido en validación.
- **(b2) reversión simple**: p = −signo del rendimiento de los últimos n días; n ∈ {1, 5} elegido en validación.
- **(c) azar con la misma frecuencia**: la matriz de posiciones del brazo (d) [y aparte la de (e)] en el tramo
  evaluado, con los instrumentos permutados y cada columna desplazada circularmente un número al azar de días
  (≥ 20): misma cantidad de operaciones, mismas duraciones, misma fracción larga/corta/fuera; sin relación con el
  día. 500 sorteos. Controla que "ganar" no sea sólo estar largo en un mercado que sube.
- **(d) colonia**: la clase `Colonia` de `..\mini_llm\mini_llm.py` SIN modificar (importada), con la estructura
  "células correctoras de un base congelado" de `..\decision\decision.py` (`Bloque`: mismas reglas; allí la similitud
  es gaussiana sobre casillas, aquí coseno sobre rasgos, que es la versión general que ya trae `Colonia`).
  - Base congelado ("pan") = comprar y mantener: predice siempre SUBE.
  - Clases del día siguiente: SUBE si r > +u, BAJA si r < −u, NADA si |r| ≤ u, con u = 15 pb (ida y vuelta al costo
    base): **acertar el signo neto de costos**.
  - Clave de la célula = vector unitario de 12 rasgos del instrumento al cierre de t (todos pasados, estandarizados
    con ventana móvil de 250 días, recortados a ±3): rendimiento 1/5/20/60 días sobre su volatilidad; rendimiento del
    mercado (media de los 31) 1/5/20 días; rendimiento relativo al mercado 5/20 días; volatilidad 20 d / 250 d;
    volumen / media 20 d; distancia al máximo de 250 días.
  - Reglas (las de la hamburguesa, tal cual): nace una célula donde el base falla y nadie pisó, con valor = la clase
    que salió; pisa si coseno > θ, su valor difiere del base y tiene confianza; cobra si pisó y acertó donde el base
    fallaba; muere si pisó donde el base acertaba; corrige su valor si fallan los dos; paga por existir; con cupo
    lleno muere la más pobre. Valor BAJA → posición −1; NADA → 0; nadie pisa → +1 (el base).
  - Una colonia compartida por los 31 instrumentos (cupo C = 200). Perillas en validación: θ ∈ {0.8, 0.9, 0.95},
    c_exist ∈ {0.002, 0.01}, adaptativa ∈ {no, sí} (12 configuraciones). Resto por defecto del original.
- **(e) colonia con cuarentena**: clase `Cuarentena` del mismo archivo SIN modificar: la célula nace hipótesis y
  sólo pisa tras k confirmaciones netas en sombra en apariciones independientes; si falla al pisar vuelve a
  hipótesis. Perillas en validación: k ∈ {2, 5, 10} × θ ∈ {0.8, 0.9, 0.95} (9 configuraciones); plazo = 60 días
  (1860 pasos); independencia = más de 5 días (se fija la constante de módulo `L` = 155 pasos; única adaptación).
- Controles de mecanismo (informativos, no cuentan para el veredicto): (d) con pago barajado (`barajar=True`).
- Criterio de elección en validación (para b1, b2, d, e): mayor rendimiento medio diario NETO al costo base en el
  tramo de validación. Empates: la primera de la lista.

## 6. Medidas (todas netas de costos, en el tramo evaluado)
Rendimiento anualizado (media diaria × 252), Sharpe (media/desvío × √252, tasa libre 0), caída máxima, fracción de
meses positivos, número de operaciones (una operación = un tramo de posición no nula y constante en un instrumento),
**ganancia neta media por operación en centavos por cada 100 USD** (neto total del brazo en centavos sobre 100 USD por
instrumento, dividido por el número de operaciones), fracción de días-instrumento pisados (colonias).
- Intervalos: remuestreo circular en bloques de 20 días, 5000 remuestras, semilla 12345.
- **Comparaciones primarias (4)**: (d)−(a), (d)−(c), (e)−(a), (e)−(c), sobre la diferencia de rendimiento diario neto
  (anualizada); (c) = media de los 500 sorteos día a día. **Corrección por comparaciones múltiples: Bonferroni,
  intervalos al 98.75 %** (también se da el de 95 % sin corregir). Secundaria: diferencia de Sharpe con el mismo
  remuestreo. Los brazos (b1), (b2) se reportan con intervalo de 95 % contra (a) y se marcan como no corregidos.
- Valor p del azar: fracción de los 500 sorteos con neto ≥ el de la colonia.

## 7. Predicción numérica (mía, antes de mirar)
- Veredicto: **NO** con p = 0.85; HAY ALGO MODESTO p = 0.12; FUNCIONA p = 0.03.
- (d) en sellado, neto al costo base: Sharpe en [−1.5, +0.6]; (d)−(a) anualizado en [−25 %, +3 %]; pisa en 15–60 %
  de los días-instrumento; ganancia por operación en [−25, +5] centavos por 100 USD.
- (e) en sellado: pisa en < 15 % de los días-instrumento; (e)−(a) en [−6 %, +2 %] anual; es decir, "casi igual a
  comprar y mantener" (repite INFORME_DERIVA: con ruido, lo mejor que hace la célula es callarse).
- (d) vs azar: intervalo que incluye 0 (p = 0.8).
- (a) en sellado: +5 % a +16 % anual sin dividendos, Sharpe 0.4–1.3.
- (b1) momento neto: Sharpe en [−0.6, +0.6]. (b2) reversión neta al costo base: negativa (entre −40 % y −2 % anual);
  a costo 0 la reversión de 1 día puede ser positiva.
- Pago barajado: no distinguible de (d) (p = 0.7), porque (d) ya no distingue nada.
- Sintética con señal: la reversión la detecta (p = 0.95); la colonia (d) la detecta con p = 0.4, (e) con p = 0.35.

## 8. Criterio (fijo)
- **FUNCIONA**: (d) o (e) supera a (a) **y** a (c), netos al costo base en el tramo sellado, con los dos intervalos
  Bonferroni excluyendo 0, las tres auditorías de fuga pasadas y sin caer en "sospechoso".
- **HAY ALGO MODESTO**: (d) o (e) supera a (a) y a (c) con intervalos de 95 % sin corregir que excluyen 0 pero no los
  corregidos; o supera sólo a (c) con intervalo corregido y no pierde contra (a) (intervalo de (x)−(a) incluye 0 con
  estimación ≥ 0).
- **NO**: cualquier otro caso. Se dice así.
- **Sospechoso de error (primero se busca la fuga, no se celebra)**: cualquier brazo activo con Sharpe neto > 2.0 en
  el sellado, o exceso sobre (a) > +15 % anual, o ganancia neta por operación > +50 centavos por 100 USD con más de
  200 operaciones, o acierto de signo > 56 %, o cualquier auditoría de fuga fallida.
- Si la auditoría 3 muestra que la colonia no detecta una señal plantada que la reversión simple sí detecta, el NO se
  redacta como "la colonia no sirve de detector" y no como "no hay señal en el mercado".

## 9. Las cuatro trampas, revisadas
- Canal simétrico: el pago de la célula no entra en la medida; la medida es dinero simulado con r(t+1) ajeno a la colonia.
- Acierto sin balancear: sube ~53 % de los días; por eso el base es "siempre sube" y se compara contra comprar y
  mantener y contra azar con la misma exposición, no contra 50 %.
- Mundo que se come la comida: aquí es el costo; por eso todo es neto y se repite a 0 y al doble.
- Sitios fijos: 31 acciones fijas de un solo país y periodo; no se puede corregir con estos datos; declarado.

## 10. Lo que este diseño NO puede decir
Nada sobre ejecución real (impacto, horarios, cortos no disponibles), ni sobre 2018–2026, ni sobre otros mercados;
una sola partición temporal (un solo tramo sellado = una sola "semilla" de mercado; no hay réplica independiente).

---
## ENMIENDA 1 (5-oct-2026, ANTES de abrir el tramo sellado; el sellado sigue sin leerse: el código corta en 2014-12-31)

Lo que ya vi al escribir esto (todo sin el sellado; copias en `datos/*_v1.json`): la rejilla de validación 2012–2014,
la sintética y las auditorías. Hechos:
1. **(e) cuarentena original queda muda**: 0 pisadas en validación y en la sintética, incluso CON señal plantada
   (5–7 células validadas de ~27 000 nacidas; en sombra acierta 43–46 %). (e) ≡ comprar y mantener.
2. **(d) colonia original no detecta la señal plantada** que la reversión simple sí detecta (reversión +12.0 %/año neto,
   IC95 [+1.4, +21.6]; (d) −4.5 % contra mantener, p_azar 0.98). Sus reglas matan a la célula al primer fallo: sirven
   para hechos deterministas, no para una ventaja estadística. Según §8, el NO de (d)/(e) hablará de la colonia.
3. **La auditoría 2 (barajada) FALLÓ para momento-250** según su criterio escrito (bruto −3.0 %/año, t = −3.6; los demás
   pasan, |t| < 0.4). Causa: fallo de mi auditor, no fuga a favor: restar la media de TODA la muestra a una permutación
   (muestreo sin reemplazo) vuelve negativa la correlación entre la suma pasada y el futuro. Se reporta como fallo.
4. Regla de limpieza: marcó AABA 2008-02-01 (+48 %) como error; es un movimiento real (oferta de Microsoft). Se deja
   como estaba escrito (afecta a 2008, igual para todos los brazos) y se declara.

Cambios (para buscar la versión más fuerte; nada se quita, los brazos (a)–(e) quedan como estaban):
- **(f) colonia de dinero** y **(g) colonia de dinero con cuarentena**: mismas ideas (nace donde el base falla y nadie
  cubre; clave = los mismos 12 rasgos; coseno > θ; valor BAJA → −1, NADA → 0; paga por existir; cupo 200, muere la
  más pobre) pero el pago es **dinero simulado** y tolera ruido: cada día en que la célula aparece (algún instrumento
  dentro de su radio) su ventaja a = media de [(v−1)·r − 2·|v−1|·7.5 pb − 1 pb si corto] (lo que gana su posición
  frente al base, cobrando ida y vuelta completa cada día: pesimista). Un día = una observación (no cuenta 31 veces
  el mismo día de mercado). Energía E0 = 2 % ; E += a si opera; E −= 1 pb por día; muere si E < 0.
  (f) opera desde que nace. (g) nace hipótesis y sólo opera tras **k días de sombra** con t = media/(desvío/√n) ≥ 2;
  vuelve a hipótesis si t < 1; la hipótesis muere si n ≥ k y t < 0. Hasta 3 nacimientos por día (los peores r).
  Perillas en validación: (f) θ ∈ {0.8, 0.9, 0.95}; (g) k ∈ {5, 10, 20} × θ ∈ {0.8, 0.9, 0.95}. Mismo criterio de elección.
- **Comparaciones primarias pasan de 4 a 8** ((d),(e),(f),(g) × (a),(c)); **Bonferroni a 99.375 %**. El criterio de §8
  se lee con "(d), (e), (f) o (g)" y el intervalo corregido nuevo. Todo lo demás de §8 igual.
- **Auditoría 2b (barajada con signo al azar)**: tras permutar los días, cada rendimiento se multiplica por ±1 al azar
  (sin restar medias): toda regla tiene bruto esperado exactamente 0. Mismo umbral (|t| < 3 y |bruto| < 3 %/año).
  La 2 original se sigue reportando como fallida.
- Auditoría 3 ampliada: se reporta si (f) y (g) detectan la señal plantada.
- Predicción (antes de correr f, g): en la sintética con señal (g) la detecta con p = 0.25 y (f) con p = 0.15 (una
  célula local ve sólo su cono y necesita ~cientos de días para t ≥ 2; la regla lineal junta todos los datos). En el
  sellado real: (g) pisa < 5 % y queda en [−3 %, +1 %] contra mantener; (f) en [−20 %, +2 %]. Veredicto global: NO, p = 0.88.
