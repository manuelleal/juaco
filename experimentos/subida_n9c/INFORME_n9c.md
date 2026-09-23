# INFORME — subida_n9c (nivel 9, tanda 3: persistir con capacidad de carga), creador, 23-sep-2026

**Veredicto del trabajo: NO.** No hay hoy un candidato del organismo propio que persista con flujo fijo de comida. Probé dos
diseños y los dos quedaron refutados en práctica.

**HAY ALGO MODESTO en el diagnóstico**, que es solo lectura de datos sellados:
- por qué O1 persiste y O3 no;
- que el organismo propio falla de dos formas opuestas.

El paquete (v2) queda preregistrado, con arnés 43/43, para cerrar esa línea con réplica. Su veredicto esperado es NO.

## Qué hice
1. **Leí las series selladas.**
   - En la pista v2 un linaje extinto se repone con un fundador ingenuo. «Persistir» mide entonces cuánto les ganan los descendientes a esos fundadores.
   - O1: fundadores con R0 0.019 (mueren a los 200 pasos por su propia regla de prueba) contra nacidos con 0.897.
   - O3: fundadores 0.560 contra nacidos 0.743. Sin esa asimetría, los 9 linajes derivan y se extinguen.
   - O2 limpia más que nadie y persiste en 0/20: limpiar no basta.
2. **v1, en práctica** (`practica_v1/`, humo 14191).
   - Diseño: boca que suma las dos filas de valor pesadas por el déficit + copia de los pesos del padre.
   - Resultado: el R0 de los nacidos sube de 0.16 a 0.25, pero el 100 % sigue muriendo por veneno o sal, y el control cruzado casi empata.
   - Causa: el valor que deja una mordida (−1.35) es chico frente al sesgo de hambre de la boca.
3. **v2, lo preregistrado.** La boca predice su propio estado tras morder, con la media de dS sentida por letra (modelo directo del cuerpo),
   y usa el código de recompensa del tronco sobre el cambio de déficit. El padre vivo hereda esa memoria (4×3). Controles:
   - PRED (sin herencia);
   - CRUZ (dE y dAg intercambiados);
   - NADA (== FABRICA).
   - Ancla calibrada antes de las semillas nuevas: [0.090, 0.155] (`calibra_ancla.py`, bootstrap de dos etapas, ERR-116).
   - Lector aparte para H-NICHO: `lee_nicho.py`.
4. **Humo v2** (14192, solo CAND, T = 50000, 55 s): 4 nacimientos, el mundo con 30.7 de 36 objetos malos y 5070 de 13 500 llegadas
   perdidas. Protegerse tapa el mundo: el nicho se destruye y los cuerpos mueren de hambre.

## Arnés (`identidad_n9c_salida.txt`, 101 s)
```
(0) shas FABRICA/pista2/motor/juez/fuente de calibracion OK · 4 carros == construccion por anclas · revisa_carro 4/4
(I) N9C_NADA == FABRICA bit a bit: v2 fija x2, v2 inmediata, v1 diag, v1 fundador_limpio, v1 compat=1  6/6
(P) T=450 sin partos: PRED == CAND == CRUZ · (B) canal 8/8 · (M) boca con el mismo uniforme 4/4
(D) determinismo · (C) en marcha 4/4 · (E) regla 14 campo a campo contra corre_convive.tarea · (G) ERR-115 3/3 · (V) letra 2/2
RESULTADO: 43/43
```

## Predicciones refutadas (mías)
- En v1 creí que leer las dos filas le quitaba el veneno al recién nacido. Refutado en el humo 14191: el 100 % de las muertes siguió siendo por B/D.
- En v2 creí que un descendiente informado que no muerde lo malo sería viable. Refutado en el humo 14192: el mundo se tapa y los cuerpos mueren a los 600 pasos.
- La idea del encargo «limpiar = ingeniería del nicho que sube la capacidad de carga» es solo parcial: O2 limpia y no persiste. Lo que decide es la asimetría entre fundadores y descendientes.

## Candidatos a ERR (los numera el coordinador)
- **(a) Instrumento.** «Persiste el carro» en v2 confunde la calidad del linaje con la inviabilidad de los fundadores que repone el mundo (P3). El 14/20 de O1 depende de que su regla de prueba mate a sus propios fundadores. Antes de fijar el 100 % del nivel 9, la medida debería comparar contra fundadores viables o contar sin reposición.
- **(b) Procedimiento.** Cambié el diseño (v1 → v2) después de un humo de práctica y antes del preregistro. Tiene precedente (aprende_barrer v1→v3), pero queda declarado.

## Qué queda
- **Comandos (solo el coordinador).** Costo ≈ 9 200 s de CPU por serie (4 brazos × 20 × ~115 s): **~26 min con Pool 6; ~52 min serie + réplica.**
  ```
  python experimentos/subida_n9c/identidad_n9c.py                                        # 43/43
  python experimentos/subida_n9c/corre_n9c.py --serie --desde 14101 --n 20 --pool 6
  python experimentos/subida_n9c/corre_n9c.py --serie --desde 14121 --n 20 --pool 6      # replica
  python experimentos/subida_n9c/corre_n9c.py --veredicto <serie.json>,<replica.json>
  python experimentos/subida_n9c/lee_nicho.py <serie.json>     (y la replica)
  ```
- **Prioridad baja:** va después de subida_n9 y subida_n9b.
- **Puntos:** 0 para el nivel 9 si sale lo esperado (NO + H-NICHO); 50 → 80 solo si FUNCIONA ×2, con probabilidad ≤ 0.03.
- **La tanda 4 del nivel 9 necesita tres piezas a la vez**, con su propio presupuesto de humo:
  1. limpiar a la tasa justa (hoy es un bien público; el TD individual de APR no la descubrió en v1);
  2. ir hacia lo valioso en vez de hacia lo más cercano;
  3. la memoria de efectos heredada.
  Es la receta de O1, pero aprendida.
- **No verificado:**
  - PRED y CRUZ nunca corrieron un humo; tampoco NADA con la v2 en 14192.
  - `lee_nicho.py` se probó por unidad con datos fabricados, fuera del arnés.
  - El costo de CPU de PRED y CRUZ se extrapoló del de CAND.
