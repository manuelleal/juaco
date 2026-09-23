# PREREGISTRO H1 — Escudería Haiku, Ronda 1

**Fecha:** 22-sep-2026 (antes de humo)  
**Autor/Modelo:** H1 (Claude Haiku 4.5)  
**Hipótesis:** Reducir confusión generacional y vetar partos en crisis extrema mejora R0 en competencia.

## 1. Hipótesis central

Con 9 cuerpos vivos a la vez, cada linaje vive ~192 pasos (vs 600+ SOLO). La palanca principal es "llegar al primer hijo" (500 pasos con saciedad ≥ 1.0), pero 87% muere antes sin reproducirse.

**Problema identificado:**
- El nodo FABRICA (NODO_LEE=50) hereda las últimas 50 mordidas del padre.
- En competencia extrema, muchas de esas mordidas son de estrés o robo, que dejan trauma.
- Los hijos heredan ese trauma y no tienen tiempo de aprender nada mejor en 192 pasos.

**Solución minimalista:**
1. **NODO_LEE = 0:** cada hijo nace sin memorias complejas (pizarra limpia).
2. **quiere_parir():** vetar reproducción si E < 0.7 o Ag < 0.7 (condiciones de muerte segura).

La separación generacional reduce confusión. El veto evita hijos condenados.

## 2. Mecanismo mínimo y memoria nueva

**Código:**
- `NODO_LEE = 0` en `__init__()` (línea 56).
- `quiere_parir(info)` retorna `E >= 0.7 and Ag >= 0.7`.
- `nace()` ya respeta `NODO_LEE` (línea 248: `if self.NODO_LEE > 0`).

**Memoria nueva:** Cero. Solo lógica condicional.

**Justificación:**
- FABRICA ya usa `hereda='nada'`, así que el hijo no lleva memoria del padre en la dote.
- Lo único que heredaba era el nodo (últimas mordidas). Al establecer NODO_LEE=0, los hijos leen cero memorias.
- El veto es una línea condicional: si hay mucha hambre O sed, no reproducirse.

## 3. Instrumento y anclas

**Instrumento:**
- `corre_H1_humo.py`: corre H1 + FABRICA (2 cuerpos), semilla 4151, T=10000.
- Compara R0 de H1 vs FABRICA en la misma condición.
- Si H1 R0 > FABRICA R0, hipótesis sostenida; si < FABRICA R0, refutada.

**Anclas:**
- Mismo mundo (`escala=0`, L=40, nobj=4).
- Mismo T=10000 (suficiente para 2-3 generaciones en 192 pasos cada una).
- Determinista: mismo seed 4151 para ambos carros.

## 4. Predicción numérica

Con 2 cuerpos en competencia (N=2 vs N=9):
- Cada linaje vive ~400-450 pasos (vs 192 con 9 cuerpos).
- R0 FABRICA (N=2): **0.40–0.50** (estimado, interpolando desde SOLO 0.5 y 9-cuerpos 0.27).
- **R0 H1 (N=2): 0.42–0.55** (con la reducción de confusión + veto de crisis).

**Rango de éxito:** H1 >= FABRICA en ≥70% de los pasos, o H1 R0 ≥ 0.48.

## 5. Control que puede fallar

**Control 1:** Nodo sin leer (NODO_LEE=0) es más puro pero potencialmente más lento para converger.  
**Posible fallo:** los hijos necesitaban el nodo para adaptarse rápido. Si H1 R0 < FABRICA, el nodo tenía valor neto positivo.

**Control 2:** El veto a reproducción en crisis (E < 0.7) es conservador.  
**Posible fallo:** vetar reproducción puede ser contraproducente; mejor tener hijos mala-adaptados que ningún hijo. Si H1 muere más joven, hipótesis refutada.

## 6. Qué lo refuta

- **R0 H1 < R0 FABRICA en humo (4151, N=2).** Significa que el nodo tenía valor y el veto es innecesario.
- **H1 muere más joven que FABRICA (vida mediana < FABRICA).** Significa que el veto mata linajes demasiado pronto.
- **Coherencia física falla en H1.** Bug en el código.

## 7. Mini-prueba de un proceso

(Pendiente: correr `corre_H1_humo.py` una vez, semilla 4151.)

Predicción antes de correr:
- H1 descendientes: 3–5
- H1 muertes: 8–10
- H1 R0: 0.45–0.50
- H1 vida mediana: 400–450
- H1 vs FABRICA: H1 > FABRICA en descendientes (por menos pérdida de hijos en crisis).

## 8. Semillas NUEVAS propuestas

Para la serie (ronda 1):
- Semillas de práctica: **4151–4170** (20 semillas, no usadas antes).
- Confirmar con ≥15/20 linajes de H1 con R0 ≥ 0.90 (meta fuerte).
- Si no se alcanza en práctica, hacer ajustes antes de sellar.

## Notas

- H1 pasa `revisa_carro.py` (sin acceso a rng, no toca pista, solo lógica).
- Código idéntico a FABRICA excepto NODO_LEE y quiere_parir() (diff ~10 líneas).
- El nodo se sigue registrando en `salida()` para telemetría (ERR-96: va a `d['carro']`, no afecta R0).
