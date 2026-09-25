# EXPLORATORIO H-PLANO en pequeño: Ohno en w90 (nube, 25-sep-2026, ~04:35)

**Qué es.** Un exploratorio de 10 semillas pedido por el director para decidir si vale la pena escalarlo en el PC. **No es dato.** Si sale algo, se preregistra en el PC con serie, réplica y ≥ 20 semillas.
**Hipótesis** (`../nube_20260925/SINTESIS_noche_H-PLANO.md`): con N chico la mutación es carga, porque la selección no le gana a la deriva (N·s < 1). Si N crece, la carga se purga.

## Qué cambia (una sola cosa)
- El tamaño del mundo pasa de **w30 a w90**: `MUNDO` pasa de esc 30, n0 30 y tope 3000 a esc 90, n0 90 y tope 9000.
- `r_rep` queda en 0.006, la misma pobreza por celda. La comida por paso se triplica, igual que el espacio y los fundadores.
- Todo lo demás es Ohno tal cual: `corre_ohno.trabajo`, SERIE, GRAM y la sha del runner. No se toca el motor.
- Brazos: VIDA y FIJO:filtra0. Semillas **25101–25110**, sin uso previo. Pool 3.
- El wrapper es `explora_hplano.py`: sólo cambia `MUNDO` antes del fork.

## Control del instrumento (antes de leer w90)
- El wrapper con w30 debe reproducir `ohno_serie_s25011-25030/{VIDA,FIJO_filtra0}_s25011.json` campo a campo, salvo `seg`.
- Si no lo hace, se detiene todo.

## Referencia w30 (serie de esta noche)
- Nacidos antes del corte (mediana): 6.
- Persistencia pareada en 20 semillas: sólo FIJO 4 · sólo VIDA 0 (tasa 0.20 por semilla).
- Nacidos tras el corte, VIDA/FIJO (medianas): 20.5 / 188.5 = 0.11.

## Lectura escrita ANTES de correr
- **M0, manipulación.** La mediana de nacidos antes del corte en w90 debe ser ≥ 18 (3× w30). Si es < 18, el exploratorio es **NO EVALUABLE**: agrandar el mundo no agrandó la cohorte.
- **M1, principal: D = (sólo FIJO) − (sólo VIDA)** en persistencia pareada, 10 semillas.
  - **Sostiene H-PLANO:** D ≤ 0.
  - **Cae:** D ≥ 2 (la tasa de w30).
  - **Ambiguo:** D = 1.
  - **Guardia de techo:** si FIJO y VIDA persisten los dos en ≥ 9/10, M1 no se evalúa y manda M2.
- **M2, secundaria y a prueba de techo: vivos en T pareado**, VIDA ≥ FIJO. Con la misma comida, un genoma cargado sostiene menos cuerpos.
  - **Sostiene:** ≥ 7/10.
  - **Cae:** ≤ 3/10.
  - **Ambiguo:** en medio.
- **Descriptivo:**
  - nacidos tras el corte, VIDA/FIJO (w30: 0.11);
  - modal de VIDA y su frecuencia;
  - R0 tras el corte con su rango (ERR-133).

**Qué haría cada resultado:**
- **Sostiene:** en el PC, serie w90 de 20 semillas más réplica, y después w270 con el gemelo.
- **Cae:** H-PLANO pierde su prueba más barata. El muro no es N, y no se gasta en máquinas más grandes.

Costo estimado: ~3× por corrida frente a w30 (~6 min), 20 corridas en Pool 3, unos 45 min.
