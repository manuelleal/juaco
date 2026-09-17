# v13 como TRONCO — confirmatorio de congelación (examen criterio v3 + regresión de generalización + regresiones)

**Escrito ANTES de construir `organismo/organismo_v13.py` y antes de correr. 17 sep 2026, día 5.**

## 0. Qué se sabe

`v13_dos_vias_20260917_160541`: el punto **`puerta = 3`, `eta_s = 0.015`** rompe el canje —retención 20/20 y acierto
0.850 en patrones nunca vistos— en semillas 61–80 (confirmatorio de un punto elegido en 41–60), con E1, E2 y E2L 20/20.
**Es candidato; para ser tronco tiene que pasar lo que pasaron v8, v9 y v11, más lo que ERR-20 añadió.**

## 1. Instrumentos (anclas; orígenes por sha)

- **`organismo/organismo_v13.py`:** el genoma explorado (`experimentos/v13_dos_vias/organismo_v13.py`, mismas anclas
  sobre `organismo_v11.py` `f69e24063be1b194`) con **los defectos fijados en el punto confirmado**: `eta_s = 0.015`,
  `puerta = 3`, `clip_s = 3.0`. Con `eta_s = 0` y `puerta = None` es v11 exacto; con eso y `div_signo = False`, v10 exacto.
- **`organismo/bateria_v13.py`:** desde `bateria_v11.py` (`17179642ad02269c`, congelado) con sustituciones contadas:
  identidades `v13(eta_s=0, puerta=None)` ≡ v11 y `v13(eta_s=0, puerta=None, div_signo=False)` ≡ v10; ningún criterio ni
  umbral cambia; 4a' se mantiene.
- **`organismo/bateria_generaliza.py`:** entrada `organismo_v13 → (organismo_v13g, eta_s=0.015, puerta=3)`.

## 2. Criterios (todos ya escritos en sus preregistros; ninguno se toca)

- **Q0 [instrumentos]:** identidades de la batería 42/42 + 42/42; `organismo_v13` (tronco) ≡ genoma explorado con
  `eta_s=0.015, puerta=3` en E1, E2, E2L × semillas 1–3.
- **X1 [examen]:** `bateria_v13.py 20 --desde 81 --log` cumple el criterio v3 **8/8** (semillas 81–100, nunca usadas).
- **X2 [ERR-20]:** `bateria_generaliza.py organismo_v13 20 --desde 81 --log`: **G1 PASA, G2 PASA**, cobertura OK.
- **X3 [regresión]:** `bateria_v11.py 6` y `bateria_v9.py 6` cumplen; `manifiesto.py --check` intacto.
- **Predicciones:** X1 8/8; X2 acierto 0.80–0.90, conducta ≥ 0.75; X3 sí.

## 3. Qué se decide

- **Q0, X1, X2, X3 pasan:** **v13 se congela como tronco** (tag `v13-tronco`; `organismo_v13.py` y `bateria_v13.py` a
  CONGELADOS). **Etapa 3 y Etapa 4 quedan cerradas a la vez, sobre el mismo tronco**, y se registra como tal. Queda
  **pendiente y obligatoria antes de decir "todo sobrevive"**: la re-verificación 3T sobre v13 (instrumento nuevo,
  porque la vía lenta tiene que leer las 12 entradas del mundo temporal) y la de capacidad. Hasta entonces, el
  registro dice "3T y capacidad: medidos sobre v11, pendientes sobre v13".
- **Falla X1 o X2:** v13 **no** se congela; v11 sigue; se registra qué etapa rompe y se diagnostica antes de tocar nada.
- **Falla Q0:** se para y se arregla el instrumento.

## 4. Qué NO prueba

Nada sobre XOR (sigue fallando por diseño), 3T ni capacidad. Ni que la vía lenta lineal sea la única posible.

---

## ENMIENDA 1 (17 sep, tras el examen en 81–100; ERR-21) — criterio 3 desdoblado y confirmatorio en semillas NUEVAS

**Lo que pasó.** En 81–100 v13 pasó 7/8 y **falló el control negativo** (criterio 3): sin plasticidad separa A∩B=3
igual, porque la vía lenta lee píxeles y A y B difieren en cuatro. Diagnóstico medido (`control3_v13_20260917_164836`):
la vía rápida sola sin plasticidad **falla 0/20** (como v11); la lenta sola **pasa 20/20**. El criterio mezclaba dos
preguntas. Decisión de dirección (delegada): **se adopta el criterio v3'** y **se repite el examen completo en
semillas 101–120, nunca usadas, con el criterio ya fijado**. Sólo ese examen decide.

**Criterio v3' = criterio v3 con el 3 desdoblado:**
- **3' [la vía rápida necesita plasticidad]:** `CTRL` = `solap_AB=3, plast=False, eta_s=0, puerta=None` (literalmente el
  control de v11): pasan E2L **≤ 1/20**.
- **3'' [la vía lenta separa por píxeles]:** `CTRL2` = `solap_AB=3, plast=False` (lenta activa): pasan **≥ 19/20**.
Todo lo demás (1, 2, 4a', 4b, 4c, 4d, 5) **sin tocar**.

**Confirmatorio de congelación (101–120):** `bateria_v13.py 20 --desde 101 --log` **8/8 con v3'**, y
`bateria_generaliza.py organismo_v13 20 --desde 101 --log` **G1 y G2 PASAN**, y regresiones (`bateria_v11.py 6`,
`bateria_v9.py 6`, `manifiesto.py --check`).

**Predicción:** 8/8 (3' 0/20, 3'' 20/20), G1 ≈ 0.85–0.90, G2 ≈ 0.85–0.92. **Si algo falla, v13 no se congela y se registra.**
**Si pasa:** v13 = tronco (tag `v13-tronco`), CONGELADOS += `organismo_v13.py`, `bateria_v13.py`; Etapas 3 y 4 cerradas
sobre el mismo tronco; pendientes declarados: 3T y capacidad sobre v13.
