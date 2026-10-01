# Auditoría de ESPEC_P9_ficha3.md (1-oct-2026) — leer junto con la espec

Autor: juaco-auditor (solo lectura; no se corrió nada, solo aritmética). La espec NO se modificó con estos hallazgos.
Rutas: `E\` = `C:\Users\User\Documents\PROYECTOS\JUACO\organelos\experimentos\organelos\escalera\`; `Espec` = `ESPEC_P9_ficha3.md` en esta carpeta.

**VEREDICTO: SE SOSTIENE CON RESERVAS.** El mecanismo y la identidad están bien armados. Pero (1) los datos de la sonda que ya existen contradicen el supuesto de que hay mundo que construir, (2) MA tiene un nulo que da falsos positivos, (3) MB y XA/XB puede pasarlas un brazo sin secuencia, y (4) "planear" no está probado por ninguna puerta. Ningún hallazgo cambia un veredicto registrado.

## Hallazgos

**H-1 (candidato a ERR). La sonda ya tiene números y apuntan a aborto.** La espec dice que no los leyó (`Espec:433`). Con la regla de aborto de `Espec:437` y `E\sondas\PREREGISTRO_sondas.md:20`:
- Mundo del encargo, d_plus 600 (humo_s1_1/2): piso 8 cruces y 12 establecidos; techo (oráculo) 6 cruces; regalo (cota dura) 6 cruces. "Cota − piso ≥ +4" falla con −2.
- Ganancia efectiva regalo/piso 2.8777/2.6134 = 1.10; techo/piso 1.083. Plus efectivo/nominal ≈ 0.25: el mundo apenas paga la llave.
- extra_sin 0.4: piso 7 cruces, regalo 7. extra_sin 0.2: piso con 3 establecidos (muerto). Solo se ha corrido p_x 0.03.
- Por la regla escrita, esto es ESPACIO NO / aborto. Construir sin decisión explícita del coordinador contradice el preregistro de las sondas.
- Consecuencia: XA/XB inalcanzables (con regalo ≤ piso en cruces nadie suma +10 sobre `lug`). Q9 = 0.30 y Q10 = 0.25 (`Espec:421-423`) están inflados.
- AVISO: son humos; el coordinador dice que la sonda sigue corriendo. Lectura provisional.

**H-2 (candidato a ERR). MB no es puerta por la propia regla de la espec.** `Espec:445`: si frac_llave_orac − piso < 0.20, MB no es puerta. Humo 1: oráculo 0.1508, piso 0.0093, diferencia 0.141. El azar de la sonda (K por moneda, sin estado) da 0.1336 > 0.75 × 0.1508 = 0.113: un brazo ciego a la llave pasa `umbral_b`.
- Techo de frac_llave rehecho: oferta de K ≈ 34 mordidas por linaje-corrida; cobertura ≈ 34·d/1e5: d = 600 da 0.20 (medido 0.15); d = 200 da 0.068. La aritmética de la espec (0.05–0.15) es correcta; el límite es la oferta total de K, no "p_x por reposición".
- Con p_x 0.03 y d = 200 la regla de `Espec:440` es imposible; "umbral_b se ajusta" no tiene regla: grado de libertad.
- Veredicto de MB: demasiado fácil en su parte absoluta. Cambio: borrar "plan ≥ umbral_b"; dejar `plan − azar_sonda` pareado por semilla ≥ margen preregistrado, y exigir H-6.

**H-3 (candidato a ERR). MA da falsos positivos por heterogeneidad** (`Espec:324-329`). El barajado conserva n_K, duración de vida y F, pero no dónde y cuándo muerde K el cuerpo. K se muerde con hambre; la mitad de las K nacen dentro del oasis (dens 0.5) y el linaje pasa el 63 % del tiempo dentro. Cualquier brazo que muerda K en el oasis tiene "K → bocado" por construcción.
- Estimación sin dato: un brazo sin mecanismo con 75 % de K seguidas de bocado y p0 = 0.45 da C = 1.67 y C_n = 0.55: pasa C_n ≥ 0.5.
- La espec ya admite que `azar` puede empatar en MA (`Espec:387`): MA es prueba de sanidad.
- Cambio: calcular C también solo con K de `dentro=0` y exigir que ese número gane a `azar` y a `lug`. Llamar a MA "sanidad", no "contraste".

**H-4. Dos fuentes para la rama de MA** (`Espec:365` vs `:446`): mediana del techo de plan, o techo del oráculo en el humo 0. Con 2728 bocados dentro por corrida (≈ 330 pasos entre bocados), Poisson: V = 200 da p0 = 0.455 y techo 2.2; V = 60 da 6.0; V = 600 da 1.19. C ≥ 2 equivale a C_n = 1/(techo − 1): 0.50 con techo 3, 0.33 con techo 4: la regla toma el umbral menor, fácil con techo alto. Fijar UNA fuente (el oráculo del humo 0) antes de la serie.

**H-5 (candidato a ERR). Canal espurio para hab_K.** Un K mordido dentro del oasis erosiona la memoria de lugar (`O1_LUGAR_PLAN.py:221-224`, copiado en `Espec:127`): `lugar[b]` se reduce a la mitad; el siguiente bocado A/C del mismo bin recibe δ más positivo, que se acredita a K (Δhab ≈ 0.024 por mordida; con ≈ 17 K dentro por corrida, del orden de PL_MIN = 0.05). hab_K puede subir sin que la llave pague nada. Cambio: control "plan en el mundo con plus = 0" (humo, 2 corridas); si hab_K ≥ 0.05 allí, MA, MB y MC no se leen o se corrigen.

**H-6. XB no aísla el contenido** (`Espec:346`). La cantidad de K mordida difiere entre plan y azar. En la sonda, K por moneda llega a 35 K por linaje-corrida, igual que el oráculo, con 6 cruces: lo que paga es la cantidad de K, no el orden. Añadir `O1_LUGAR_AZAR` de la sonda como 5.º brazo (+20 corridas), reportar K por 1000 pasos por brazo y exigir plan > azar con K igualadas. Además el ORAC de la sonda tiene OR_D = 600 fijo (`carros\O1_LUGAR_ORAC.py:43`): medir con otro d_plus exige una variante nueva que la espec no prevé.

**H-7 (D1).** El hábito literal comparte `_p3_apr` y COMPITE = 1 con plan (`Espec:206`); solo difieren las compuertas (`Espec:82-83`). PL_SITIO es inerte en linajes establecidos; solo actúa PL_MANO.
- "Empata en papel" tiene matiz: en `hab`, que re-muerde K con la llave en mano, hab_K baja ≈ 0.07 por re-mordida: hab ≤ plan, no igual. La dirección no está garantizada.
- HABNC puede perder en (c) de verdad, pero por un sesgo estructural (confunde sitio con llave), no por "no planear". Control legítimo pero estrecho: nombrarlo "ablación de la competencia (bloqueo)", no "hábito". Perder en MC solo prueba que la competencia es necesaria.
- Lo que distingue a plan de azar es el destino del crédito; de HABNC, la competencia; de hab, solo "no re-muerde con llave en mano". Eso NO es "secuencia de dos pasos": el azar de la sonda ya hace K → oasis sin estado.
- **Vocabulario:** ni con MC pasando se puede decir "planea". (c) mide extinción por re-experiencia (regla delta), no sensibilidad a la devaluación sin experiencia. Máximo permitido: "crédito temporal con competencia".

**H-8. MC (`Espec:367`) está mal montada.**
- Falta control temporal: el bloque de devaluación solo corre plan y hábito (`Espec:474`), sin `lug` ni plan sin devaluación; cualquier deriva Q2 → Q4 cuenta como "caída". Cambio: caída_dev − caída_sin_dev, o correr `lug` en el bloque.
- Sin regla de réplica por semillas: definir unidad y n/10.
- "Establecido" tras la devaluación selecciona por resultado: redefinir en [10k, t_dev).
- ≈ 5 vidas por cuarto, ≈ 8 K por linaje en Q2: el cociente por linaje es muy ruidoso; usar la suma por brazo.
- "11 episodios / inalcanzable" (`Espec:380`) vale si un K = un episodio, pero el código acredita cada bocado dentro de la ventana de traza (≈ 5 por K): "dos vidas" podría ser alcanzable; Q7 (p = 0.15) sesgada a la baja. No declarar "inalcanzable".
- Veredicto de MC: legítima pero débil; a 25k pasos de la devaluación cualquier regla delta se extingue: no discrimina plan de hab.

**H-9. hab bloqueado en 0: no por diseño.** Equilibrio de Rescorla-Wagner hab* ≈ 0.55 sin lugar; el lugar lo reduce, no lo anula. La regla es local. Defecto numérico: `nor` suma e² de todas las letras con traza viva (incluidas B y D): Δhab_K ≈ 0.03–0.05 < PL_MIN; "una pareja basta" (`Espec:37`) no se cumple. Exigir N mínimo de establecidos por brazo para leer MA/MB/MC (propuesta: ≥ 60/180 serie, ≥ 40/90 bloque dev); si no, NO SE LEE.

**H-10 (identidad).** Las 13 anclas y 14 comprobaciones bastan para el camino lógico (con PLAN3 = 0 todo queda fuera; PL_PASO no consume rng; PL_AZAR solo `self.rng`). Falta: (i) que `p3_val`/`p3_en_mano` cuenten decisiones y no evaluaciones por objeto (`Espec:113`); (ii) `PLAN_W=0.0` en MUDO cambia −0.0 por +0.0: I3 con tolerancia de signo de cero; (iii) comprobación de `revisa_carro` con `self.rng` (`Espec:512`); (iv) arnés propio para ORAC con otro d_plus.

**H-11. PENDIENTE_SONDA con grados de libertad a posteriori:** `p_x` (`Espec:440`), `frac_K_dentro` (`:448`), `techo_contraste` (dos fuentes), `t_viaje` (mediana truncada: subestima), `d_plus` ∈ [60, 600]. Cada uno debe reducirse a una fórmula o a "aborto". Las reglas de plus, extra_sin, aborto y azar_sonda sí están cerradas.

**Verificado a mano:** el vector de la sec. 1.6 (e = 0.7788, hab_K = 0.0935, ΔhabK = 0.02154, etc.), binomial P(≥ 13/20) = 0.1316, decaimiento 11.1–12.5 episodios, cobertura 0.068/0.204, p0 y techo, conversión C ↔ C_n.

## Cambios concretos
1. Antes de construir: decisión explícita sobre ESPACIO (H-1), o correr la sonda con p_x 0.06–0.10 y d_plus 200.
2. MB: quitar umbral absoluto; plan − azar_sonda pareado ≥ margen preregistrado.
3. MA: llamarla "sanidad"; calcular también con K de dentro = 0 y comparar entre brazos; una sola fuente del techo.
4. Añadir: plan en mundo con plus = 0; azar_sonda como 5.º brazo; `lug` o plan-sin-dev como línea base de MC, y regla n/N.
5. XA/XB: bajar a descriptivas si regalo − piso < +2; corregir Q9/Q10.
6. Vocabulario: prohibir "planea" y "entiende"; permitir solo "crédito temporal con competencia".

## No verificado
- Cualquier valor de MA/MB/MC con d_plus = 200 (la sonda no lo corrió ni guarda tiempos por evento).
- frac_K_dentro (no está en los JSON de la sonda); la estimación de C_n de un brazo ciego es de orden de magnitud.
- Magnitud de la erosión del lugar (H-5), velocidad de extinción (H-8) y efecto de `nor` (H-9): papel, sin corrida.
- construye_p1.py, construye_c.py, corre_c.py, identidad_c.py, corre_v143.tarea, revisa_carro.
- Las referencias de la BITÁCORA a P1b y P9 viejo no se contrastaron una a una.
