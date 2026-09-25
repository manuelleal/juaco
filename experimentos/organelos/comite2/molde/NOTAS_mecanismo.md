# EXPLORATORIO, no es dato

# NOTAS de mecanismo (explorador Fable 2, 25-sep-2026) — lo que se lee en la telemetría, escrito mientras corren las olas

## 1. La métrica, escrita como cuenta del linaje
Con fundador limpio y un cuerpo vivo por linaje, cada muerte es o un nacimiento real (cola no vacía) o un fundador:
**R0 real = (D − F)/(D + 1)** (D muertes, F fundadores). En `trasplantes/datos/v143_s33001`: los linajes con F = 0 dan 0.957 y 0.973;
con F = 5 → 0.82; F = 20 → 0.65; F = 48 → 0.34; F ≈ 700 → 0.02. O1: mediana de F = 0. **Todo el hueco entre V143 y O1 está en F**, y F se
paga casi entero antes de t ≈ 1500 (t_fund de los linajes que después se establecen: 599–1300).
Consecuencias: (a) vetar partos ("vivir más, parir menos") baja D y con él R0 real, salvo que evite extinciones; (b) acelerar muertes con
la cola llena sube R0 sin que el linaje sea más estable (ERR-102: lo de O3); (c) "hermanos vivos del mismo carro" no existe en esta pista.

## 2. Por qué muere el fundador de V143 a los ~45 pasos (leído del código, V143.py:189-195, y de los números)
Nace a 0.6/0.6 sin saber nada; hambre 0.4; boca Vb = 1.2·w + 2·hambre + 0.5 → con w = 0, p(morder) = 0.99: muerde lo primero que pisa.
Mitad de las letras son malas → 0.2. Tras UNA mordida de B la vía lenta le da w(B) = −1.35, pero el hambre ya vale 0.8 (+1.6):
Vb = −1.62 + 1.6 + 0.5 = 0.48 → p = 0.83 de re-morder B. El FILTRO con META no lo salva porque META exige conocer algo bueno y todavía
no conoce nada. Por eso el fundador muerde B/D tres veces más que A/C (mord B 1020 contra A 318 en un linaje de 740 fundadores).

## 3. Lo que hizo la cultura pública (`piz`) y por qué fracasó (s38001, s38002)
- Funciona como información: los fundadores leen la pizarra en su primer paso, conocen A/C/B/D, el FILTRO se enciende y dejan de morder
  B/D (mord B+D por linaje cae a ~100 contra ~230 en la misma semilla de v143, y la letra propia `_adS` sólo tiene A y C).
- Pero el mundo se TAPA: composición media A 0.68 / C 1.19 / B 18.0 / D 16.1 de 36 objetos (v143 misma semilla: A 1.54 / C 1.55);
  pasos sin nada bueno en el mundo 12.4 % (v143: 2.8 %); por cuerpo, 42 % de pasos sin bueno para su necesidad (v143: 21 %).
  Los cuerpos mueren a los 600 pasos exactos = de hambre desde la dote sin comer nada. Fundadores 50–70 por linaje.
- Lectura: en v143 **quien destapa el mundo es el fundador ignorante al morir** (sus 100–300 mordidas malas por linaje son la única
  limpieza sostenida; APR aporta 20–160). En este mundo lo bueno se come en ~10 pasos y lo malo sólo sale por mordida u olvido
  (9 × 0.003 por paso). Cuenta de servilleta: 9 cuerpos comen ~0.09 buenos por paso → nacen ~0.045 malos por paso; el olvido saca 0.027;
  el resto (~0.018 por paso = ~200 mordidas malas por linaje cada 10⁵ pasos) lo tiene que morder alguien. Sin fundadores ciegos, nadie.
- Además la cultura CIEGA a la opción aprendida de v14.3 (APR): sólo considera limpiar letras que el linaje SINTIÓ malas (`_adS`), y con
  cultura nunca las siente. De ahí las perillas de la ola 2: `PIZ_ADS` (la cultura también llena `_adS`) y `BARRE` (regla de nicho).
- Es el mismo hallazgo del carril B (ECO): "el veneno tapa el mundo"; y la misma razón por la que O1 necesita su limpieza (S-SIN-LIMPIEZA
  murió de hambre y sed con vida 600).

## 4. `espera` (vetar el parto con cola ≥ 3): por qué se hunde (s38002: 0.076 contra 0.544)
La cola nunca pasa de 3; el hijo deja 0.89 hijos (v143: 1.0–1.24) y vive 890 (v143: 1180); cada racha de hijos sin parir vacía la cola
y el linaje se extingue (fund 120–518 por linaje). En v143 la cola llega a 11–16: **la profundidad de la cola es la reserva del linaje**.
El veto quita el seguro. Predicción P9 acertó en el signo y falló en la magnitud.

## 5. `imita` (aprender de la foto de los otros): por qué se hunde (0.19, 0.24)
Al principio todos son ciegos y muerden de todo: la imitación reparte +1 a todas las letras. La señal "parado sin morder" (−1) llega tarde
y mezclada con rechazos de A/C por saciedad. Aprende ruido, y ese ruido tapa la aversión propia. Fundadores 108–127 por linaje.
