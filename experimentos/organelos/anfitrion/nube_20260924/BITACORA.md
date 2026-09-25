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
- Terminó a las 02:56:08: 100/100 corridas en 3877 s de pared, con errores 0, bloqueados 0 y trinquete 0.
- Resultado leído por `--lee` sobre los JSON; coincide con el del runner.

### VEREDICTO POR LA LETRA: **NO** (cae todo; se necesitaba ≥ 15/20 pareadas)

| Prueba | Resultado | Letra |
|---|---|---|
| **PC** (CONTROL > SIN_CONTROL en cuerpos tras el corte) | **9/20** | cae |
| **P1a** (CONTROL > SIN_TRAGAR en persistencia) | **5/20** (15/20 al revés) | cae |
| **P1b** (CONTROL > INERTE) | **7/20** | cae |
| **P2a** (R0 de los nacidos portadores, CONTROL > SIN_TRAGAR) | **10/20** (20 evaluables) | cae |
| **P2b** (CONTROL portadores > INERTE portadores) | **12/20** (20 evaluables) | cae |

Medianas:
- Área tras el corte: CONTROL 138.5 · SIN_CONTROL 157.0 · INERTE 183.5 · SIN_TRAGAR 238.0 · AZAR 141.0.
- Persisten en T: CONTROL 7 · SIN_CONTROL 7 · INERTE 10 · SIN_TRAGAR 13 · AZAR 11.
- R0 de los portadores: CONTROL 0.252 · SIN_CONTROL 0.245 · INERTE 0.215 · AZAR 0.103; SIN_TRAGAR (todos) 0.238.

Descriptivo:
- **tx** sí se mueve: el banco de CONTROL le gana a AZAR 18/20, con mediana 0.970 contra 0.892.
- **san** no sube: CONTROL 0.031, AZAR 0.169; 4/20 contra AZAR.
- Sanciones (mediana): CONTROL 35, AZAR 298.
- La selección bajó la sanción en vez de subirla.

Lectura, sin declarar nada:
- El control genético sobre el simbionte no compra supervivencia ni reproducción.
- Portar sigue costando: SIN_TRAGAR persiste más, 15/20, como en la endosimbiosis ×2.
- Apuesta del creador: NO (P 0.45). Acertó.

### Réplica 26021–26040: **NO SE CORRE** (regla escrita: si la serie da NO por la letra, no hay réplica)
