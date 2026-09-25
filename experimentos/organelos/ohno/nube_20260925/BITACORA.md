# Bitácora nube: OHNO SOBRE BASE VIVA (25-sep-2026, madrugada)

Rama `nube/ohno-20260924` sale de `organelos` @ 887c4c1 (el paquete llegó en ff120c4). `organelos` no se toca. Nada va a main.

**Entorno:** 4 CPU, 15 GB de RAM, Python 3.11.15, numpy 2.4.3, numba 0.67.0.

## 1. Comprobaciones previas
- `construye_ohno.py --verifica`: **VERIFICA OK**.
- `manifiesto.py --check`: 20 congelados intactos.
- `identidad_ohno.py`: **12/12 en 473 s** (el PC tardó 864 s). Salida en `identidad_ohno_salida_nube.txt`; la del PC queda intacta.
- `--prueba_pool --pool 2`: corre 6/6, sin abortos, ~29 s por corrida a T corto. Salida en `prueba_pool.txt`.

## 2. Auditoría (juaco-auditor, sólo lectura): LISTO CON CORRECCIONES
- **ERR-133 [fondo, interpretación]:** bajo el quimiostato, R0 ≈ 1 para toda población que persiste.
  - Un NO en G1 es ambiguo: puede ser falta de ventaja o una ventaja que el quimiostato borra.
  - La letra se aplica tal cual.
- **ERR-134 [protocolo]:** la duplicación no se ejercita con `r_rep` 0.006.
- **ERR-126** (el umbral de O1b bajado a ≥ 5) se acepta.
- Calibración sin sesgo: se hizo sólo con FIJO, en las semillas 25901–25918, y la regla de §3b se aplicó tal cual.
- Detalle en `ERR_133-134_ohno.md`, commiteado antes de cualquier semilla de serie.

## 3. Serie 25011–25030 (Pool 3): lanzada a las ~03:20
- Terminó a las 04:00:44: 60/60 corridas en 2463 s de pared (~120 s por corrida), sin abortos.
- Resultado leído por `--lee`; coincide con el del runner.

### VEREDICTO POR LA LETRA: **NO**

| Prueba | Resultado | Letra |
|---|---|---|
| **G1** R0 pareado VIDA > FIJO:filtra0 | **8/20** (VIDA < FIJO 7) | cae (≥ 15) |
| **G2** persiste VIDA ≥ FIJO | **False** (9 contra 13) | cae |
| **G3** modal de VIDA no diseñada | **0/20** | cae |
| **P-OHNO** modal con duplicado divergente | **0/20**; banco con Ohno real > sombras 0/20 | cae |
| TECHO / INVIABLE | no se disparan (FIJO persiste 13/20; AZAR 0/20) | ventana evaluable |

**Descriptivo prometido en ERR-133** (`descriptivo_ERR133.txt`):

| Brazo | R0 tras el corte (mediana, rango) | Nacidos tras el corte (mediana) | Nacidos antes del corte (mediana) |
|---|---|---|---|
| VIDA | 0.880 (0–1.375) | 20.5 | 6 |
| FIJO | 1.081 (0–1.235) | 188.5 | 6 |
| AZAR | 0 | 4.5 | 11 |

**Persistencia pareada:**
- Ambos persisten: 9.
- **Sólo VIDA: 0.**
- **Sólo FIJO: 4.**
- Ninguno: 7.

**Lectura, sin declarar nada:**
- La mutación de la gramática fue **carga pura** en este mundo. VIDA no sobrevivió nunca donde FIJO murió, y FIJO sí sobrevivió 4 veces donde VIDA murió.
- Con 6 nacimientos antes del corte, la selección no puede ganarle a la deriva.
- En las 8 semillas de VIDA que persisten con organismo expresado, la selección **vuelve a filtra0**: 8 de 10 tienen modal filtra0 y 2 derivan a `ensena`, que también es diseñado.
- Un NO en G1 queda ambiguo por ERR-133, pero G2 y la persistencia pareada no lo son: la variación costó.

### Réplica 25031–25050: **NO SE CORRE** (regla del director: si la serie da NO, no hay réplica)
