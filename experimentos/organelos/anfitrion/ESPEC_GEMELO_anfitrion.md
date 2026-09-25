# ESPECIFICACIÓN (no construido): gemelo numba del paquete CONTROL DEL ANFITRIÓN

Misión: llegar a la AGI por este camino. Esto lo construye el agente compilador sólo si el coordinador lo pide. Opus B no lo construye.

## Para qué
- El poder de P1 (cuerpos vivos tras el corte) está limitado por el R0 < 1 de FABRICA: tras el corte quedan de 2 a 4 cuerpos en w30 y ~6 en w90 (`calibra_poder_salida.json`; ECO v1.1).
- Más comida no lo arregla: con r 0.045 quedan de 3 a 4.
- La única palanca de tamaño que queda es **w270** (270 fundadores, L 10 800). Ahí ECO v2.1 sostuvo 224 cuerpos en T con otro carro.
- En Python, w270 cuesta ~10–30× por paso; con el gemelo de ECO (×32 en w270) cabría en una noche de nube.

## Qué tiene que portar (sobre `motor_eco_rapido.py`, que ya es el gemelo de motor_eco + FABRICA_ECO, 120/120)
1. **Genoma de 25 genes** (los 18 de motor_eco + 7 órganos en 0.9 sin efecto sobre FABRICA): el orden de consumo de `muta` debe dar 2·25 números por nacimiento, como motor_eco3.
2. **Ecología de libres** (`darwin/simbiontes.py`, `Ecologia.paso`): arreglos pos/g/e; afinidad σ(g·P); quedarse o dar un paso ±1; ganancia F·a/m con m de `bincount`; costo c0 + c2|g|²; muerte; partición con tope.
   - **Mismo generador** [seed, 0, 30, 0] y mismo orden de llamadas: `random(n)`, `integers(0, 2, n)`, `random(n)`, `random((k, 6))`, `normal(0, σ, (k, 6))`.
3. **Tragar** en el orden de la lista de cuerpos, **costo de alojar** y **pérdida interna**, con el mismo generador y el mismo orden que `paso`.
4. **Canal:** `Vb += tanh(g·P[letra])` en la boca de FABRICA, antes de la sigmoide. El sorteo de la boca no cambia.
5. **Herencia del simbionte**, `parto` / `funda` / `_hereda`: falla, BARAJADO, anillo de AZAR_S y el banco de simbiontes alineado con ES['banco'].
6. **Control** (`anfitrion/control_anfitrion.py`): ranura ctl (tx, san); gate de tx con el generador [seed, 0, 32, 0] ANTES de p_falla; sanción en la decisión de boca; mutación con reflexión; anillo de control en AZAR; siembra de huéspedes y simbiontes.
7. **Salida:** las mismas claves de d['simb'] (serie, don, ind, ind10, eventos, decisiones, ctl_final, ctl_banco, serie_ctl), para que `corre_anf.medidas` y `veredicto` lean igual.

## Arnés de aceptación (N/N o no se usa)
- Gemelo == Python **bit a bit** en la salida completa. Cubre los 5 brazos del paquete y los 5 de endosimbiosis, w30 y w90, a T 6000 y a T 100 000 (una semilla), con siembra y sin ella.
- Más los casos por pieza de `identidad_anfitrion.py`: K1a, K1b, K2a, K2b, M y Z.

## Costo estimado de construirlo
Un agente compilador (Opus), ~1 sesión: la ecología de libres es vectorial y el control son ~60 líneas. Se trabaja sobre el gemelo de ECO ya verificado.
