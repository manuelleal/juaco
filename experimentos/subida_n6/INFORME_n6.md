# INFORME — subida_n6 (creador, nivel 6; 23-sep-2026). Una página

**Veredicto del paquete: LISTO PARA SERIE.** Todavía no hay resultado: un humo de una semilla no es dato.
Misión: llegar a la AGI por este camino; el método manda sobre el cómo.

## Qué hice
1. **Elegí el bloque "rodeo robusto en 2D".** Es la brecha más grande del nivel. El 21-sep, en el mundo muralla con
   geometría sorteada, el nivel 6 CAYÓ 5/10.
2. **Hallé por qué ese mundo no medía rodeo** (candidato a ERR). Una fila de veneno en un toro no lo parte: queda un
   cilindro. En 240 de los 400 episodios *rodeo*, alejarse daba la vuelta al toro y era más corto que cruzar la
   muralla, y era un camino limpio.
   - De ahí salieron 124 de los 144 «limpio» de CAMINO.
   - En los 160 rodeos de verdad (sólo por el hueco): CAMINO 0.125, CIEGO 0.006, PLACEBO 0.156.
   - Hay además 4 episodios que arrancan sobre la comida.
   - Lo calcula `analiza_vuelta_toro.py` sobre el JSON sellado `99dc2e86b833fc29`.
3. **Diagnóstico analítico** de por qué el campo difundido no rodea:
   - su gradiente entre vecinos (~0.05) queda tapado por el ruido motor (0.3);
   - con la retina a `r_vis = 1`, el mapa se calla al costear la muralla y la retina atrae al veneno.
4. **Construí el instrumento por anclas.** `construye_subida.py` genera `mundo_subida.py` (`484e34db8f2150da`) desde
   `mundo_muralla.py` (`6e515713c86d8bf4`), con cero memoria nueva persistente y el organismo v13 sin tocar:
   - `grad`: signo del gradiente local del campo;
   - `filtro`: el veneno recordado es obstáculo, sólo si hay meta recordada;
   - `brujula`: control en el que el veneno no bloquea el campo;
   - `prueba['cierre']`: segunda muralla entera, que sí parte el toro.
5. **Arnés `identidad_subida.py`: IDENTIDAD 42/42.** Son 30 identidades bit a bit con las perillas apagadas (anillo
   v13, mapa, 2d, rodeo y los 6 brazos de la muralla) y 12 controles que deben diferir.
   JSON: `datos/humo/identidad_subida_20260923_153614.json` (`16d15f6dcbfd2d8a`).
6. **Runner `corre_subida.py`.** Tiene 11 brazos y 13 puertas; las de R-1a a V1 conservan la letra del 21-sep.
   Verifica el sha del mundo y compara las entradas campo a campo contra `corre_muralla` (regla 14). Aplica la
   regla 10 automática y escribe su JSON.
7. **Humo** (`--humo`, semilla 6641, T = 20 000, 6 corridas, 30 s). JSON en
   `experimentos/subida_n6/datos/humo/subida_humo_20260923_153753.json` (`ce1249637262520a`).

| brazo | limpio(rodeo) | limpio(atajo) | pisa(rodeo) | comida |
|---|---|---|---|---|
| GF (candidato) | 0.95 | 0.90 | 0.05 | 365 |
| BRÚJULA | 0.0 | 0.1 | 1.0 | 367 |
| CIEGO / CAMINO / BARAJADO / INVERTIDO | 0.0 | 0.0 | 1.0 | 113 / 161 / 365 / 365 |

## Qué falló (declarado)
- **Mi primera versión del filtro bloqueaba la comida.** Con `valor(A) < 0` al principio de la vida, la comida
  quedaba filtrada para siempre (v_A −0.226 fijo). Lo corregí antes del humo, condicionando el filtro a que haya
  meta. Lo vi en una corrida de depuración con la semilla 6642, del arnés.
- **Mi primer humo midió la vuelta del toro, no el rodeo.** GF dio 1.0 en 4.4 pasos en el mundo viejo. Eso llevó a
  `cierre`, y a partir de ahí el mundo es otro, declarado.
- **Rompí una regla sin querer y lo reparé.** Corrí `python manifiesto.py` sin `--check`: regeneró `MANIFEST.txt`
  (archivo del tronco, fuera de mi carpeta). Lo restauré con `git checkout -- MANIFEST.txt`. Los 20 congelados están
  intactos.
- **Uso de cómputo:** usé 5 corridas de depuración más un humo de 6. Ninguna usa semillas de la serie ni de la
  réplica.

## Qué queda
- **Serie y réplica** (las corre el coordinador; §11 del preregistro). Cada una son 220 corridas, ≈ 1.6 h de CPU,
  ≈ 17 min de pared con Pool 6.
- **Propuesta de puntos** (decide el director): FUNCIONA 50 → 70 % (75 % si pasa la escala); ALGO MODESTO
  55–60 %; NO 50 %, más el ERR del toro.
- **Para el 100 %:** dos metas en 2D, port a v14.2, mapa que se corrige dentro del episodio, y rodeos compuestos
  más allá de `H_M`.
- **No verificado:**
  - la n que pasa con probabilidad ≥ 0.95 bajo el nulo (regla 15);
  - el tiempo real del mundo E;
  - PLACEBO, GRAD y FILTRO sin humo;
  - BARAJADO puede conservar el mapa bajo la lectura por signo (riesgo declarado en §5–6).
