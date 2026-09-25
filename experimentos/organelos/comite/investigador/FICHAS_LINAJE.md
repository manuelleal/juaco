# FICHAS_LINAJE — comité de exploración, investigador (Opus, 25-sep-2026)
Transcrito por el coordinador desde la respuesta del agente (sus reglas le impiden escribir archivos). Solo lectura; sin Pool ni commits.
Rutas: [B] = PROYECTOS\JUACO\bundle\ · [O] = PROYECTOS\JUACO\organelos\

## 1. Diagnóstico (10 líneas)
1. Lo que funcionó siempre le da al RECIÉN NACIDO, desde que nace, lo que tuvo consecuencia:
   - O1 guarda la media de lo mordido por letra, en la memoria del linaje ([B]experimentos/carrera_escuderias/carros/O1.py:6-19);
   - RES_SIN0 da R0 de nacidos 0.950 y 0.946 ([O]registro/NUBE_BITACORA_20260924.md:196,232);
   - ORA_SIN0 da 0.997;
   - `ensena` prendido en el 97–99 % del banco.
   La otra forma de éxito es decidir con el estado presente: O3 cae de 0.968 a 0.072 si lee su estado desfasado.
2. Todo lo que pidió a la variación ENCONTRAR o CREAR cayó por lo mismo: cruce, gramática, Ohno, código, Prometeo y anfitrión. Con 1–30
   cuerpos tras el corte, N·s < 1 y la mutación es carga.
3. Sólo se fija lo de efecto enorme: el OJO en niebla, 7/10 contra 0/10. En w90 la carga baja de 0.67 a 0.83, pero no paga.
4. El cuello demográfico es q0, morir antes del primer parto (61–87 %). Con q0 = 0, R0 pasaría de 0.46 a 1.06 ([B]REGISTRO:6147).
5. En el quimiostato, un linaje que persiste tiene R0 ≈ 1 por construcción. Lo que decide es sobrevivir a los cuellos (el arranque y el
   corte): es un Galton–Watson crítico.
6. Los mundos no son intercambiables:
   - en la carrera, el carro es el cerebro del linaje;
   - en la pista v2 y en ECO, el hijo nace vacío;
   - la tabla de la familia daña en la carrera (−0.19) y salva en la v2 (0.67 → 0.95).
7. Probablemente "ni el oráculo cruza" (fase 9) fue en buena parte efecto de las entradas NEUTRAS. Sin ellas, el oráculo da 0.981–0.997.
   (Sin verificar.)
8. Dato no recogido: en ECO v1.2, MUT0_T (familia sin neutras, sin mutación) persiste 20/20 a 1e6 (predicho 0–10). Quedó descriptivo
   por ERR-60.
9. Nunca se midió el ARRANQUE EN FRÍO. Toda persistencia del bicho real pasó por un vivero (≥ 77 % de los cuerpos) o por refundación.
10. Patrón: el problema no es crear órganos, es que el recién nacido no sabe qué es qué, y lo que sí funciona nunca se probó sin
    andamio. Camino corto: quitarle el andamio a lo ya replicado.

## 2. Fichas (orden: probabilidad / costo)

**F1. ARRANQUE EN FRÍO: v14.3 más la tabla de la familia sin neutras (RES0), en ECO, sin vivero desde t = 0.**
- Memoria nueva: ninguna. Sólo cambia `t_corte = 1` (refunda 0).
- Brazos (w90, 90 fundadores, T 1e6, 20 semillas más réplica):
  - RES0_FRIO;
  - RES0_10k (dosis de vivero);
  - RES0_60k (ancla: reproduce MUT0_T ≥ 17/20);
  - BAR0_FRIO (tabla con las R permutadas);
  - FAB_FRIO (sin familia).
- Predicción:
  - RES0_FRIO vivos en 1e6 ≥ 15/20, en serie y en réplica;
  - R0 real de nacidos (sin los 90 fundadores, cohorte [1e4, T−2e4]) con mediana ≥ 0.90;
  - FAB_FRIO ≤ 2/20;
  - BAR0_FRIO ≤ 5/20;
  - fundadores repuestos = 0 (arnés).
- Control que puede ganar: BAR0_FRIO (BAR_SIN0 dio 0.828 en un humo).
- Instrumento:
  - `corre_eco_v12.py` (envoltorio nuevo por anclas, con `t_corte` por brazo), `motor_eco_rapido_fam.py` (gemelo 132/132), `carros/FAMB_RES0_ECO.py`;
  - BAR0 sale de `subida_n10c/carros_n10c.py`;
  - arreglar antes nube-9/ERR-60: atrapar el SystemExit, y "guardia disparada = persistente", declarado antes de correr.
- Costo: ~200 corridas, 0.6–1.7 h con Pool 6.
- Probabilidad: FUNCIONA 0.35, MODESTO 0.30, NO 0.35.
- Referencias: Lande 1993 (Am. Nat. 142:911); Ackley y Littman 1994.

**F2. La selección prende la familia y la sostiene a 1e6** (FAMB_ORG_ECO, ECO v2.1 a T 1e6).
- Brazos: VIDA_ORG, AZAR_ORG, MUT0 y ORG_FRIO (órganos apagados, sin vivero).
- Predicción: VIDA_ORG ≥ 15/20; AZAR_ORG ≤ 8/20; `ensena` ≥ 0.95 entre los vivos; ORG_FRIO ≥ 5/20.
- Costo: ~0.7–1.2 h.
- Probabilidad: 0.50 con vivero, 0.10 en frío.

**F3 (rara). TUMBAS QUE ENSEÑAN (estigmergia).**
- Al morir, el cuerpo deja en su celda sus entradas con R ≠ 0 durante K = 5000 pasos. Al nacer, el hijo lee la tumba más cercana
  dentro de un radio r.
- Brazos: TUMBA, TUMBA+RES0, TUMBA_BAR, FAB_FRIO y RES0_FRIO.
- Predicción: TUMBA ≥ 8/20; TUMBA+RES0 ≥ RES0_FRIO + 4; TUMBA_BAR ≤ FAB_FRIO + 2.
- Costo: 1 día más ~1.5 h.
- Probabilidad: 0.25.
- Referencia: Theraulaz y Bonabeau 1999.

**F4. ASIMILACIÓN GENÉTICA (Baldwin).**
- 8 genes de valencia inicial por letra y necesidad. Se crían con vivero y después siembran un arranque en frío.
- Predicción:
  - signo correcto contra las sombras ≥ 15/20 en INN, y ≤ 10/20 en INN_RES0 (ocultamiento);
  - en frío con el banco INN, ≥ 12/20 persisten, contra ≤ 2/20 del G0.
- Probabilidad: 0.30 para el signo; 0.20 para el frío.

**F5 (rara, ecología). DESCOMPONEDOR:** un replicador libre que come B y D (de `simbiontes.py`). Baja la fracción de mordidas malas de
~0.85 a ≤ 0.60. Predicción: FAB_FRIO ≥ 8/20. Cambia el mundo, no el organismo. Probabilidad: 0.20.

**F6. REFUGIOS:** w90 partido en 4 parches con corredores (Hanski 1998). Predicción: el tiempo de extinción de FAB_FRIO se multiplica
por ≥ 2. Probabilidad: 0.20.

**Descartadas:** rep_acum, neofobia sobre V143 y las perillas de ECO sobre V143 (ya probadas).

## 3. Recomendación
**F1 primero.** Junta dos piezas replicadas o medidas (n10c ×2 y MUT0_T 20/20), el instrumento y el gemelo ya existen, cuesta ~1 h de
Pool 6, y si falla, la dosis de vivero (1 / 10k / 60k) mide cuánto andamio hace falta.

## No verificado
- Que el cerebro de FABRICA_ECO sea el de v14.3 en la pista v2 (masas de las letras de ECO).
- Los JSON de MUT0_T de v1.2.
- Que `t_corte = 1` funcione en el gemelo sin efectos laterales, y si ERR-60 dispara en frío.
- Los costos.
- Las entradas neutras del oráculo de la fase 9.
- Los resultados de organelos, citados desde los mensajes de commit.
