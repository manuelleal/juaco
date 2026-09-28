# PREREGISTRO — TERMO′ en la pista de la carrera (creador, 28-sep-2026, escrito ANTES del humo)

Misión: llegar a la AGI por este camino. Encargo del coordinador: TERMO′ = TERMO con memoria que olvida; ¿conserva el efecto de TERMO en
la carrera?

## 1. Pieza
- Es la de `PREREGISTRO_examen_v144b.md` sec. 2.
- En el carro, la memoria es **propia** (`_tmM`): la `_adS` de APR no se toca. Es del linaje: no se borra al nacer, igual que `_adS`.
- Constante: ema_c = 0.05 de FABRICA. Constantes nuevas: cero.
- Carros por anclas (`construye_termop.py`):
  - `V143_TERMOP` (`edf5dfc9c5e498da`), desde V143_TERMO (`3db639cab75641fb`);
  - `V143_TERMOPINV` (`63edcafcc569a0d7`), desde V143_TERMOINV (`da106a995b18bafd`).

## 2. EXPLORATORIO previo (declarado; `datos/explora_termop_carrera_20260928_124836.json`, `388aedd874941dbe`)
Semillas 49011–49015, T 100 000, 9 carros iguales, Pool 2.

| semilla | TERMO R0 real (mediana) | TERMO′ R0 real | mayoría que cruza | ¿corridas idénticas? |
|---|---|---|---|---|
| 49011 | 0.862 | 0.862 | no / no | **sí** |
| 49012 | 0.796 | 0.796 | no / no | **sí** |
| 49013 | 0.780 | 0.780 | no / no | **sí** |
| 49014 | 0.933 | 0.933 | sí / sí | **sí** |
| 49015 | 0.821 | 0.821 | no / no | **sí** |

**TERMO′ == TERMO bit a bit en 5/5**, en todas las claves de los 9 linajes salvo el nombre. La pista es quieta (el dS de cada letra no
cambia), así que la media móvil vale exactamente el dS desde la primera mordida.

## 3. Instrumento
- `corre_termop.py`: por anclas desde `termo/corre_termo.py` (`66f1f2539f1030ef`), con `construye_carrera_termop.py --verifica`.
  **Misma pista, misma letra** (`lee_serie`: V1–V4, P1–P3, FUNCIONA / HAY ALGO MODESTO / NO / NO SE LEE; bloque = el menor).
- Brazos: v143 (base), **termop** (CANDIDATO), **termopinv** (CONTROL), o1 (techo y ancla).
- Arnés `identidad_termop.py`: **PASA** (143 s). Comprueba:
  - carros == anclas;
  - TERMO = 0 == V143 en la salida entera (2 semillas);
  - **TERMOP == TERMO en la física, en la pista quieta** (s 49993 T 5 000 y s 49994 T 20 000);
  - TERMOPINV == TERMOINV;
  - la pieza actúa;
  - determinismo;
  - la memoria se desdice (tras 20 × +0.8 y 30 × −0.4 vale −0.142; la de TERMO seguiría en +0.080);
  - shas fijados;
  - `valida()`;
  - ERR-115;
  - la letra en 10 casos sintéticos.

## 4. Predicción
La pista es quieta, así que la serie **debe reproducir a TERMO**:
- R0 real mediano del candidato 0.90–0.95;
- mayoría que cruza 11–16/20;
- gana a V143 ≥ 18/20;
- control ≤ 0.2.

| veredicto | FUNCIONA | HAY ALGO MODESTO | NO | NO SE LEE |
|---|---|---|---|---|
| por serie | 0.25 | 0.55 | 0.05 | 0.15 |

**Refuta** la equivalencia cualquier diferencia de física entre TERMOP y TERMO en la pista quieta. Si aparece, es un error de
instrumento y se para.

## 5. Semillas NUEVAS (busca_semillas_v144b)
Serie 49941–49960 · réplica 49961–49980 · práctica/humo 49991–49992 · arnés 49993–49994.

## 6. Comandos (sólo el coordinador)
```
python experimentos/tronco_v14_4b_examen/corre_termop.py --serie --desde 49941 --n 20 --pool 6
python experimentos/tronco_v14_4b_examen/corre_termop.py --serie --desde 49961 --n 20 --pool 6
python experimentos/tronco_v14_4b_examen/corre_termop.py --bloque <resumen serie>,<resumen replica>
```
Son 80 corridas por serie; en el exploratorio, 140–160 s por corrida con Pool 2, así que unos 35–45 min con Pool 6.

## 7. Humo — escrito DESPUÉS
(pendiente)
