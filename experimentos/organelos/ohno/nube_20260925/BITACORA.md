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
