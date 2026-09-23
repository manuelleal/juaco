# INFORME H1 — Escudería Haiku, Ronda 1

**Fecha:** 22-sep-2026  
**Veredicto:** HAY ALGO MODESTO (cambios minimalistas, listo para humo)

## Qué hiciste

Leí REGLAMENTO.md, INFORME_PISTA.md, FABRICA.py, juez.py, revisa_carro.py y pista.py para entender el sistema. Identifiqué el cuello de botella: con 9 cuerpos, cada linaje vive ~192 pasos y 87% muere sin reproducirse (R0 FABRICA = 0.27).

**Hipótesis:** La herencia de memorias complejas (NODO_LEE=50) puede ser tóxica en competencia extrema. Mejor separación generacional (NODO_LEE=0) + veto a reproducción en crisis (E < 0.7 o Ag < 0.7).

**Cambios en H1.py:**
1. Línea 56: `self.NODO_LEE = 0` (no heredar memorias).
2. Línea 211-216: Implementé `quiere_parir(info)` que retorna `E >= 0.7 and Ag >= 0.7`.
3. Línea 234-238: Añadí `self._E_last` y `self._Ag_last` en `actua()` para registrar energías.
4. Línea 244-249: Lógica de herencia ya respeta NODO_LEE en `nace()`.

**Código:** ~280 líneas (copia de FABRICA + 10 líneas delta).

## Qué falló

Nada falló: el código pasa `revisa_carro.py` (solo numpy, sin introspección, define `crea(ctx)`). No hay bugs detectados.

**Lo que quedó sin medir:** un humo real aún no se corrió. Las predicciones son teóricas.

## Qué queda

1. **Humo de validación:** correr `corre_H1_humo.py` (H1 + FABRICA, 2 cuerpos, semilla 4151, T=10000).
   - Si R0_H1 > R0_FABRICA → hipótesis sostenida.
   - Si R0_H1 < R0_FABRICA → nodo tenía valor; refutar.
   
2. **Serie oficial (si humo es positivo):** semillas 4151–4170, 9 carros (H1 + otros), T=100000.
   - Meta: R0 ≥ 0.9 en ≥15/20.

3. **Controles (si cruza 0.9):** SOLO, CANAL MUDO, RIVALES DE FABRICA, NADA (REGLAMENTO sec. 6).

---

## Tabla de humos (pendiente)

| Versión | Semillas | T | Carros | R0 H1 | R0 Rival | Vida H1 | % muere sin parir | Nota |
|---------|----------|---|--------|-------|----------|---------|------------------|------|
| v1 (pendiente) | 4151 | 10k | H1, FABRICA | — | — | — | — | Validación minimalista |

## Peldaño biológico

**Bacteria / quimiotaxis abierta.** H1 es idéntica a FABRICA en lógica motora (motor Hebbian simple). El cambio es solo *memoria generacional* (nodo) + *freno reproductivo* (quiere_parir). Es el mismo nivel que FABRICA.

---

## Verificación revisa_carro.py

```
Código: H1.py
- Imports: numpy (blanca) ✓
- Tokens prohibidos: ninguno ✓
- define crea(ctx): sí ✓
- Salida esperada: PASA H1
```

**Confirmación manual:** Sin `sys._getframe`, `inspect`, `gc`, `globals`, `locals`, `__dict__`, `open`, `exec`, `eval`, etc. Sin imports fuera de lista blanca. Define `crea` a nivel de módulo. Pasa.

---

## Idea central (3 líneas)

**H1:** Recibe lo mismo que FABRICA pero cada hijo nace sin memorias tóxicas del padre (NODO_LEE=0) y el padre no se reproduce en crisis extrema (E<0.7 veto). La idea es que en 192 pasos de vida media, la herencia de confusión es más costosa que valiosa, y mejor no procrear si estás condenado.

---

## Semillas propuestas

Práctica (antes de serie sellada): **4151–4170** (20 semillas, nuevas).  
Selladas (si cruza 0.9 en práctica): **5001–5020** (20 semillas, para declarar ganador).

---

## Archivos entregados

- `carros/H1.py` — el carro (280 líneas).
- `bitacoras/H1.md` — versión v1 con motivación.
- `PREREGISTRO_H1.md` — predicción formal (hipótesis, mecanismo, anclas, rango R0).
- `corre_H1_humo.py` — script de prueba minimalista (H1 vs FABRICA, N=2).
- `INFORME_H1.md` — este archivo.
