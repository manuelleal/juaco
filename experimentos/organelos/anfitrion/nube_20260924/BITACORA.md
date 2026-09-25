# Bitácora nube: CONTROL DEL ANFITRIÓN (25-sep-2026, madrugada)

Rama `nube/anfitrion-20260924` sale de `organelos` @ 878074b. `organelos` no se toca. Nada va a main.

## Entorno
- 4 CPU, 15 GB de RAM, Python 3.11.15, numpy 2.4.3, numba 0.67.0, llvmlite 0.49.0 (`requirements.txt`).

## 1. Arnés de identidad (01:40–01:42)
- `identidad_anfitrion.py`: **16/16 · N/N · 144 s** (PC: 218 s, Python 3.14.2).
- Mismos números que el PC caso por caso: nac 57, refund 211, tragados 41, quedan 11, sorteos 274/307, rechazos 59, sanciones 119, mut_ctl 56 y 49.
- Salida: `identidad_anfitrion_salida_nube.txt`. El archivo del PC se deja como estaba.

## 2. Auditoría (juaco-auditor, sólo lectura)
- **Veredicto: LISTO CON CORRECCIONES.** Las correcciones de protocolo están en `ERR_130-132_anfitrion.md`, commiteadas antes de cualquier semilla de serie.
- (a) El cambio de P2 no muestra sesgo: la calibración corrió sólo `SIN_TRAGAR`. El orden no es auditable por commits, porque llegó todo en un commit único (ERR-130).
- (c) La sanción es equivalente bit a bit al daño sentido en este mundo, porque la valencia es fija. El límite queda escrito para mundos con cambio (ERR-132).
- Hashes de las 11 anclas y de las fuentes de `siembras.json`: coinciden.

## 3. Identidad a la duración real (b) (01:46–01:51, 1 proceso)
- `escala_anf.py`, semilla 26995, T 100 000, corte 40 000.
- **A4-escala** (SIN_CONTROL == motor_endo VIDA_S): **True**.
- **A5-escala** (CONTROL con p_mut_ctl 0 == motor_endo): **True**.
- Unos 92 s por corrida. Salida en `escala_anf.txt`.

## 4. Prueba de Pool (01:46–01:47)
- `--prueba_pool --pool 2`: 10/10, errores 0, guardias limpias.
- El veredicto a T 6000 no cuenta. Salida en `prueba_pool.txt`; datos en `datos/anf_prueba_pool/`.

## 5. Serie 26001–26020 (Pool 3): lanzada a las 01:51
- Primeras 9 corridas: **media de ~113 s** (95–121 s), por debajo del umbral de 250 s → la réplica va esta noche, salvo que la serie dé NO.
