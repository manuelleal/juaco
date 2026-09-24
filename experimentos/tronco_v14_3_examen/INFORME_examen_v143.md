# INFORME — examen del criterio v4 sobre v14.3 (creador, 23-sep-2026, noche). Una página

**Estado: LISTO PARA SERIE (la corre el coordinador el 24-sep).** Pero la letra tiene un riesgo que conviene decidir ANTES de
correr (§7 del preregistro): con la letra tal cual, el resultado más probable es **NO PASA por T-B**, y no sería culpa de N.
**ERR-122 (23-sep ~21:10, antes de la serie; el director: "corrige la banda"):** T-B decide azar G2 con [0.31, 0.60] (nulo real del tronco: T-B pasa 0.957); la banda vieja [0.42, 0.58] se reporta para CAND y TRONCO y no decide; arnés 114/114; P(PASA) por serie 0.82–0.91, serie + réplica 0.67–0.82 (antes 0.47–0.52 y 0.22–0.27).

## Qué hice
1. **El candidato, por anclas** (`construye_v143.py`): `organismo_v143` y `organismo_v143g` desde los congelados de v14.2, con el
   texto de subida_n7 (el constructor comprueba que el cuerpo es `organismo_v142N/gN` con `norm_lenta=1` por defecto);
   `bateria_v143` y `bateria_generaliza_v143` (una entrada nueva, campo a campo); `organismo_v143cal` (v14.3 en el mundo vivo, dos
   sitios de la vía lenta). **Memoria nueva: cero. Constante nueva: M0 = 3.0.**
2. **Hallazgo que ordena el examen:** todos los mundos de T-A…T-F tienen estímulos de masa 3, así que N es 1.0 exacto: **en esas
   puertas v14.3 ES v14.2 bit a bit** (el arnés lo comprueba en 46 comparaciones). El examen v4 no ve a N salvo en T-G (3T-k).
3. **Runner** `corre_examen_v143.py` (argparse sin abreviaturas; `--pool 1..6` obligatorio; aborta ante banderas desconocidas):
   reusa por import la letra **calibrada** de V4-CAL, la de dE5 para T-B/T-C i/T-E/T-F, C1/C2/C6 de B-5 y la de subida_n7 para
   T-G; cuenta la inercia (CAND == tronco) por puerta; imprime una línea por puerta y el VEREDICTO; `--combina` da el del examen.
4. **Probabilidades con datos reales** (`analiza_potencia_v143.py`, sin simular): por serie T-A 1.00, T-B **0.55**, T-C 0.97,
   T-D 0.95, T-E 0.97, T-F 1.00, T-G 1.00, legible 0.97 → **P(PASA serie) ≈ 0.47–0.52; serie + réplica ≈ 0.22–0.27.**

## Arnés y humo (antes de cualquier número de serie)
```
identidad_v143ex.py  (0) 6/6  (A) 12/12  (I) 12/12  (B) 6/6  (C) 11/11  (D) 5/5  (E) 4/4  (R) 32/32  (J) 5/5  (K) 13/13
RESULTADO: 106/106   (190 s; datos/humo/identidad_v143ex_20260923_204757.json 9a5c9055bb741098)
```
(E) N encendido reproduce bit a bit el crudo de subida_n7 (s7701, k = 1/5/8 y T142 k = 5). (J) el juez reproduce el veredicto
registrado de dE5 (T-E cae 13/15/9/5/4/9), de V4-CAL (PEOR NO, TRONCO_B LI −4.152) y de subida_n7 (K_max 1/8/0).
Humo (12.6 s, 6 corridas): T-A VIVO CAND == OFF bit a bit (r −22); E2 come B 88; T-G N k = 5 lift 0.216; el juez dice SI al
candidato idéntico y NO al sintético malo (cae T-A, T-B, T-C, T-D, T-G). `datos/humo/examen_v143_humo_20260923_204303.json`
(`1c419a0eb2b1a308`). No es dato.

## Qué falló o amenaza (declarado)
- **Predicción mía refutada antes de correr:** esperaba que un candidato inerte pasara el examen con ~0.9. El cálculo con 40
  semillas reales del tronco lo tumba: **la banda de azar de G2 de T-B, [0.42, 0.58], rechaza al propio tronco ~45 % de las veces
  por serie** (su mediana es 0.434; las dos series históricas dieron 0.437 y 0.434, al borde). Patrón ERR-91. No cambié nada:
  propuse en §7 un ERR candidato (banda [0.31, 0.60] con el nulo real: T-B pasa 0.957 bajo el nulo), que sólo vale si se decide
  antes de la serie.
- T-H (escala) no se mide: su instrumento no existe. Es la única puerta donde N actuaría.
- El examen es ciego a N donde la masa ≠ 3, fuera de 3T-k (familias/variantes, mundo grande): no se verificó que no regresione ahí.
- Nombre: "v14.3" aquí es v14.2 + N (decisión de las 19:30). El paquete `tronco_v14_3` (FILTRO + boca TD) es otro candidato;
  si pasa, tendría que ser v14.4 o componerse con este antes de congelar.
- Primer arnés 105/105; añadí un control (bandera desconocida con modo válido) y exigí el código 2 de argparse: 106/106. Los
  controles del parser pasaron de subprocesos a llamar sólo a `argumentos()`: así el arnés no puede lanzar una serie.

## Qué queda (sólo el coordinador)
- Decidir §7 (T-B) antes de correr. Luego: nube `/root/venv-juaco/bin/python experimentos/tronco_v14_3_examen/corre_examen_v143.py --serie --pool 3`
  y `--replica --pool 3 --con <JSON de la serie>`; PC igual con `python` y `--pool 6`.
- Costo: 1 796 corridas por serie, 2.8–4.2 h de CPU, 30–50 min de pared; serie + réplica 5.6–8.4 h de CPU.
- Si PASA: congelado por §10 (4 archivos a `organismo/` byte a byte, 24 congelados con `JUACO_CONGELAR=1`, regla 1 nueva
  `cd organismo && python bateria_v143.py 6 && python bateria_generaliza_v143.py organismo_v143 20 --desde 101`, tag `v14.3-tronco`).
- Brújula: **mosca**. N es una normalización del paso por la carga de entrada. Una ganancia dividida por la actividad total se
  ve ya en el lóbulo antenal de *Drosophila*.
