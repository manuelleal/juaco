# VEREDICTO — entrada del registro

Copiada de `registro/REGISTRO_etapas_1_2.md`, líneas 613–649.

---

### BUG-01, experimento 1 — decaimiento local en Wp/Wn. **REFUTADO**
Preregistro `experimentos/bug01/PREREGISTRO.md`, escrito y cerrado antes de tocar código.
`organismo_v7d.py` = v7 + `Wp[ix]*=(1-lam); Wn[ix]*=(1-lam)` en las celdas activas, sólo al morder.
Diff de 3 líneas funcionales. **Control 1: `lam=0.0` es bit-idéntico a v7, 42/42 escenarios × semillas.**
**Control 2: el bug se reproduce con `lam=0.0`** → `comp=(9.0, 9.0)`, `W=0.0`. λ=0.001 fijado a priori.
400 corridas, 20 semillas, 197 s.

| predicción | veredicto | cifra |
|---|---|---|
| **P1 desbloqueo** | **REFUTADA** | canales por debajo del techo: **0/20**. Con λ=0.001, `Wp=9.00`, `Wn=8.98`, `W=+0.02`. El bloqueo sigue intacto |
| **P2 no regresión** | **SOSTENIDA** | las seis etapas pasan **20/20** con λ = 0.001; el sesgo del 1.1% queda dentro de los criterios |
| P3 precisión | SOSTENIDA | el equilibrio analítico acierta a **3 decimales en los 5 valores de λ** |
| P4 ley de disparo | SOSTENIDA | el patrón de divisiones no cambia en ninguna etapa |

**Y no es cuestión de ajustar λ: la ventana es VACÍA.** Demostración, con `eta=0.03`, `K=3`, `aversion=1`,
clip 3.0/celda (9.0 por código). En el bloqueo `W≈0`, así que `dlt≈R` y el empuje **no se atenúa**:

    crecimiento por mordida de comida (R=+1):  K·eta·|R|            = 0.090
    crecimiento por mordida de veneno (R=−3):  K·eta·aversion·|R|   = 0.270
    con mezcla 50/50:  Wp* = 0.045/λ     Wn* = 0.135/λ

    para que Wn* < 9 (no saturar)                  ->  λ > 0.01500
    para que |W_B + 3| < 0.3 (valor correcto)      ->  λ < 0.01000

**λ tendría que ser a la vez mayor que 0.015 y menor que 0.010. No existe.** Y el criterio que aprieta es
el del veneno: **el mismo factor 3 que hace saturar antes el canal aversivo es el que estrecha la tolerancia**.
El decaimiento uniforme está estructuralmente condenado, no mal calibrado. **No se recalibra λ** (regla 3).

**Lo que sí deja el experimento**: P3 confirma que el mecanismo está entendido — el equilibrio
`W* = 3·eta·R/(3·eta+λ)` predice lo observado a 3 decimales para λ ∈ {0, 0.0003, 0.001, 0.003, 0.01}.
La derivación de arriba se apoya en esa validación, no en intuición.

**Diagnóstico de por qué falla**: el decaimiento uniforme ataca la **magnitud** de los canales, y la patología
no es de magnitud sino de **redundancia** — que los dos canales codifiquen lo mismo a la vez. Pagar en valor
neto (el sesgo del 1.1%) para corregir un exceso que no está en el valor neto es el error de diseño.
Eso apunta al experimento 2, ya nombrado en el preregistro del 1 y sin probar entonces: decaer **sólo la parte
común**, `m = min(Wp, Wn)`, que deja `Wp − Wn` **exactamente** intacto.
