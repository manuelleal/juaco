# EXPLORATORIO, no es dato

# PREDICCIONES previas — comité 2, EXPLORADOR FABLE 2, carril "salir del molde: el LINAJE como unidad" (25-sep-2026, firmadas antes de correr)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).

## 0. Diagnóstico previo (leído de `comite/trasplantes/datos/v143_s33001_T100000.json`, no medido por mí)
- En la pista con fundador limpio, **R0 real = (D − F)/(D + 1)** por construcción: cada muerte es un nacimiento real (cola no vacía) o un fundador.
  Los linajes V143 "establecidos" con R0 0.65–0.86 tienen F = 5–48 fundadores, TODOS antes de t ≈ 1500. Los dos con F = 0 dan 0.957 y 0.973.
  O1: mediana de fundadores 0. **La pieza que le falta a V143 en esta pista es el FUNDADOR, no el hijo.**
- El fundador V143 muere a los ~45 pasos: tras la primera mordida mala (E 0.2, hambre 0.8) la aversión de la vía lenta (−1.35) no le gana al
  empuje del hambre (+1.6): re-muerde B con p ≈ 0.83. El FILTRO con META está apagado porque no conoce nada bueno.
- "Hermanos vivos del mismo carro" NO existe en esta pista (un cuerpo vivo por linaje): compartir energía entre hermanos es imposible por construcción.
- "Vivir más y parir menos" (vetar partos) BAJA R0 real por construcción si no evita extinciones (menos muertes = menos nacimientos).

## 1. Ideas (todas reglas locales del carro, sin retropropagación; ninguna copia la regla de O1 ni la de O3)
| brazo | qué es |
|---|---|
| `v143` | el bicho real (MOLDE con perillas 0 == V143; no lee ni escribe la pizarra) |
| `o1` | techo (política escrita por un LLM) |
| `piz` | **CULTURA PÚBLICA**: cada cuerpo publica en la pizarra, cada 50 pasos o cuando cambia, su tabla SENTIDA (8 números: dE, dAg medios por letra, 0 = no probada). Todo cuerpo lee las entradas nuevas de OTROS cada paso y las mete por la VÍA LENTA con la misma rutina con que FABRICA lee el nodo (R = +1 / −3 por signo). El fundador limpio nace sin memoria pero con cultura. Nada de la tabla verdadera. |
| `piz_bar` | control de CONTENIDO: lee la pizarra con las letras cruzadas por parejas (A↔B, C↔D): aprende las valencias al revés |
| `piz_fund` | dosis: lee la pizarra SOLO mientras el carro no ha sentido nada propio (el fundador ignorante); el hijo no la usa |
| `imita` | **IMITACIÓN sin canal**: de la foto `obs['cuerpos']` (letra bajo el cuerpo, letra mordida el paso anterior) de los otros: mordió X → mensaje +1 para X en las dos filas; parado sobre X sin morder → −1. Con tasa chica (ETA_IMIT 0.05). Sin pizarra. |
| `espera` | historia de vida "vivir más, parir menos": veta el parto si la cola real ≥ 3 (info['cola'] de quiere_parir). Prueba de mi lectura de la métrica. |

Pista: `carrera_escuderias/pista.py` tal cual (importada), 9 carros iguales, fundador limpio, T 100 000, pizarra encendida, juez.resumen_linaje.
Semillas 38001–38005 (barrido); confirmación 38006–38010 si algo da ≥ 0.85 en ≥ 3/5. Máximo 4 procesos. Medida principal: mediana por semilla
del R0 real de los 9 linajes; mediana sobre semillas; pareado CON contra SIN (v143) con la misma semilla.

## 2. Predicciones firmadas (pueden fallar)
- **P1** v143: mediana en [0.45, 0.72] (trasplantes 0.596 en 10 semillas).
- **P2** o1 ≥ 0.85 en ≥ 4/5 semillas.
- **P3** `piz` > v143 en ≥ 4/5 pareadas con diferencia mediana ≥ +0.10 (p 0.60). Cumple la regla de parada (≥ 0.85 en ≥ 3/5): p 0.40.
- **P4** `piz`: fundadores por linaje-semilla (mediana) ≤ 3 contra ≥ 10 de v143 (p 0.65). Es el mecanismo declarado: si baja F y no sube R0, mi lectura de la métrica está mal.
- **P5** `piz_bar` < v143 en ≥ 4/5 pareadas (p 0.70): el contenido importa; si `piz_bar` ≈ `piz`, el efecto es de la lectura, no de la cultura, y se descarta.
- **P6** `piz_fund` dentro de ±0.05 de `piz` en la mediana (p 0.55): el hijo no necesita la cultura (ya tiene el nodo).
- **P7** `piz`: la vida mediana del hijo NO cambia (dentro de 1000–2000; v143 ~1400) (p 0.7). El hijo sigue igual.
- **P8** `imita` > v143 en ≥ 3/5 con dif ≥ +0.05 (p 0.45); peor que `piz` (p 0.75): la señal sin consecuencia es ruidosa.
- **P9** `espera` < v143 en ≥ 4/5 (p 0.70): vetar partos baja D y con él R0 real. Si sube, mi lectura de la métrica está mal.
- **P10** ningún brazo llega a ≥ 0.90 en ≥ 3/5 salvo o1 (p 0.65).
- **P11** en `piz`, el cuerpo de t = 0 (todos ciegos, pizarra vacía) sigue muriendo a veces sin parir: fundadores antes de t = 1000 no llegan a 0 en todas (p 0.7).

## 3. Ola 2 (firmadas 17:05, tras leer la ola 1 completa y UNA corrida de `piz_ads` (s38001: 0.217); antes de cualquier `barre` válido)
Motivo: `piz` destapó el fundador (0 fundadores antes de t 1500) y tapó el mundo (A 0.7 / C 1.2 de 36): nadie muerde lo malo.
- **P12** `piz_ads` ≈ `piz` (dentro de ±0.05 en la mediana; p 0.75): la opción aprendida de v14.3 no limpia lo suficiente y cada fundador limpio borra su Q.
- **P13** `piz_barre` > `piz` en 5/5 pareadas con dif ≥ +0.20 (p 0.6); `piz_barre` ≥ 0.85 en ≥ 3/5 (p 0.25); `barre` solo > v143 en ≥ 3/5 (p 0.5).
- **P14** con BARRE el mundo baja de ≥ 90 % a ≤ 80 % de B+D y `frac_sin_bueno_mundo` baja de 0.12 a ≤ 0.05 (p 0.7).
- **P15** el costo de BARRE aparece como muertes por veneno/sal de HIJOS (≥ 30 % de sus causas) y vida del hijo < 1500 (p 0.6).

## 4. Ola 3 (firmadas 16:52, tras el humo T 3000 de la dosis 2 y antes de correrla a T 100 000)
Dosis 1 de BARRE (s38002): limpia el mundo (A 3.8 / C 6.1; 0 % sin bueno) y esteriliza (desc = 0: muerde cada malo que pisa con reserva ≥ 0.8 y nunca
junta 500 pasos ≥ 1.0). Dosis 2 (`BARRE_V2`): sólo si el mundo está tapado en ese paso, fuera de la ventana de parto, refractario 200.
- **P16** `piz_barre2` > `piz` en ≥ 4/5 pareadas (p 0.6) pero < `v143` en ≥ 4/5 (p 0.7): pocas barridas (humo: 10 en 3000 pasos × 9 cuerpos), el mundo sigue tapado.
- **P17** `barre2` dentro de ±0.10 de `v143` (p 0.5): sin cultura el fundador sigue muriendo igual y las barridas son marginales.
- **P18** ninguna dosis de BARRE llega a ≥ 0.85 en ≥ 3/5 (p 0.85).
