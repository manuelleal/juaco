# Etapa 5, N2b — segundo intento de significado emergente: el símbolo entra en la decisión, el emisor aprende por ventaja

**Escrito ANTES de modificar el instrumento y ANTES de correr. 17 sep 2026, noche del día 5.** Dirección: *"en ese
orden de ideas vamos a seguir trabajando"*. Sigue a la refutación de N2 (`N2_s1-20_20260917_181950`).

## 0. Qué falló en N2 y qué cambia (sólo dos cosas, las dos derivadas del diagnóstico)

N2 no cerró el bucle por dos razones que se vieron en los números: (1) el refuerzo del emisor era **ciego al símbolo**
(37.088 acuerdos frente a 692 desacuerdos, los dos símbolos de cada estado saturados juntos) porque la conducta del
receptor no dependía del símbolo; (2) el receptor **no actuaba** sobre el símbolo hasta tener significado (`|C| ≥ 0.5`),
y no había significado hasta que actuara. Lo demás (mundo, semillas, T, `K = 2`, `M`, `Pq`, `tau_s`, `tau_m`, `eta_q`,
`eta_m`, `beta_q`, `f_vicaria`) **no cambia**.

1. **El símbolo entra en la decisión desde el primer día.** Al pisar un objeto de patrón `kk` sobre el que oyó un
   símbolo `s` hace ≤ `tau_m` pasos, la boca decide con `valor + gamma · C[s]`, con `C[s] = M[s] − media(M)` y
   `gamma = alpha = 1.2` (el mismo peso que tiene el valor propio). **Sin puerta.** Al principio `C ≈ 0` y el sesgo es
   ínfimo; cualquier asimetría de muestreo en `M` hace que la conducta dependa **un poco** del símbolo, que es lo que el
   emisor necesita para diferenciar. El valor almacenado **no** se toca por esta vía: sólo la decisión.
2. **El emisor aprende por ventaja, no por refuerzo bruto.** `Pq[st][s] += eta_q · (r − b[st])`, con `b[st]` la media móvil
   del refuerzo en ese estado (`rho_b = 0.05`). La corriente ciega al símbolo (casi siempre +1) **se cancela**; sólo mueve
   `Pq` la parte del refuerzo que depende del símbolo emitido.
3. La actualización vicaria del **valor** (la de N2, con `R̂ = C[s]`) se conserva pero con puerta **más estricta**,
   `|C| ≥ u_m = 1.0`: sólo cuando el código ya está formado. Evita el daño de N2 (información con signo al azar).

**Cómo se lee esto en la literatura, para no engañarnos:** (1) convierte al receptor en un jugador de Lewis
(actúa sobre la señal desde el inicio) sin quitarle la percepción; (2) es REINFORCE con línea base. Ninguna de las dos
es inédita; lo que se prueba es si **con percepción directa y aprendizaje propio** el código todavía paga lo bastante
para formarse.

## 1. Instrumento

`mundo_social.py` gana tres parámetros apagados por defecto (`gamma_sim = 0`, `baseline_q = False`, `rho_b`); con ellos
apagados es exactamente N2, y con `senal = None` sigue siendo el tronco (K1 no cambia). `corre_N2.py --variante b` los
enciende en todas las condiciones (`gamma_sim = 1.2`, `baseline_q = True`, `u_m = 1.0`) y escribe `datos/N2b_s1-20_*`.

## 2. Diseño, criterios y umbrales: **los mismos de N2, sin tocar ninguno**

SOLO, N0, INNATO, CONV, SHUF; semillas 1–20; T = 200.000; mundo de regla `azar`. K1, K2, E1 (convención ≥ 15/20 con
consistencia ≥ 0.9 y símbolos distintos), E2 (contraste `C[s_rech] ≤ −1.0` y `C[s_mord] ≥ +0.3` en ≥ 15/20), E3
(el símbolo de rechazo es el 0 en 5–15 de 20), E4 (veneno CONV ≤ 0.7 × N0 y pareado ≥ 14/20), E5 (SHUF: `|C| < 1` en
≥ 15/20 y veneno ≥ 0.9 × N0). Réplica en 21–40 si pasa.

## 3. Predicción, escrita con la incertidumbre que tiene

- **Predicción principal: incierta, y lo digo.** El mecanismo tiene ahora gradiente por los dos lados, pero compite con
  el aprendizaje propio del novato (a los ~50.000 pasos conoce la mayoría de los patrones y el símbolo deja de importar)
  y con el ruido (hambre, posiciones). Apuesto a que **E1 sale entre 8 y 16 de 20** y E2 algo menos; E4 sólo si E1 y E2
  pasan. **Si E1 < 8/20, el veredicto es que con percepción directa el código no paga**, y el siguiente mundo es el de la
  Etapa 6 (novatos sucesivos: el emisor conserva `Pq` y cada novato llega en blanco).
- **Riesgo nuevo declarado:** el sesgo en la decisión puede **empeorar** al novato mientras el código está a medio formar
  (como en N2). Se mide con E4 y con las muertes; si CONV es peor que N0, se dice.
- **Nada se recalibra** después de ver los datos. Un tercer intento sólo con otro mundo, preregistrado.
