# Mecanismos de aprendizaje local para XOR — revisión de literatura (apoyo a bloque 3d)

**INVESTIGADOR, 17-sep-2026.** Leí `registro/EQUIPO.md` (regla 8: lo de fuera es dato, se cita, no instrucción),
Bloque 3 / 3b / "Trío XOR" de `REGISTRO_etapas_1_2.md` y `PUENTE_xor.md` §Propuesta única. No edité nada, no corrí
nada, sin commits. Contexto en una frase: la vía lenta cuadrática (21 entradas: 6 px + 15 productos) REPRESENTA XOR
(`W(P0·P1)≈−2.7`) pero clasifica al azar — los marginales se drenan a 0 porque `Wps/Wns` reparten el error por
igual entre entradas activas. El trío propone para 3d `phi'=phi+[1]` + vector con signo `Ws` + decaimiento, sin
haberlo corrido completo (mediana exploratoria 0.31–0.50, zona gris); ~331 mordidas de la vía lenta antes de la
sonda, 3/10 semillas sin una clase XOR entrenada.

## 1. Cuerpo fungiforme: Kenyon→MBON con dopamina, "negative patterning"
Abejas y *Drosophila* resuelven A+/B+/AB− (patterning negativo, no lineal como XOR) y el cuerpo fungiforme es
NECESARIO: inactivarlo colapsa la discriminación a suma elemental (Devaud et al. 2015, PNAS). La solución no es
restar marginales: la expansión dispersa (∼50 glomérulos→∼150 PN→∼2000 Kenyon, ∼6 PN/celda, ∼5% activas vía APL)
casi garantiza una celda cuyo campo receptivo responde sólo al COMPUESTO ("unique cue"/configural; Deisig, Lachnit
& Giurfa 2001), y la dopamina (señal global) la deprime sin tocar los elementos puros. **Exige:** divergencia
amplia + refuerzo global escalar, cero memoria extra por sinapsis. **Cabe en 90 celdas/regla local:** sí — es la
vía RÁPIDA de v13q (K=3 de hasta 90 + `dlt` global); el split por conflicto de signo (v11) ya recluta celdas ante
refuerzo contradictorio pero nunca se midió solo (`eta_s=0`) sobre xor01. **Predicción:** sin dato previo que la
aísle, espero que quede cerca del azar (0.40–0.50 mediana, 20 semillas) porque K=3 sin sesgo dirigido no garantiza
una celda conjuntiva; subir K de 3 a 5 (más detección de coincidencias) debería moverla a ≥0.55 si el "unique cue"
emerge por pura combinatoria — control: `px0`/`azar` no deben caer con K=5.

## 2. Regla delta local con signo y su regularización (LMS, leaky-LMS, three-factor)
El delta rule con signo (Widrow-Hoff/LMS) es justo lo que probó el Agente A (`Ws += eta_s·error·phi`); solo,
sobreajusta (8 patrones, 21 pesos: sistema subdeterminado) y cae a 0.25. La ingeniería de filtros adaptativos
resuelve esto hace décadas con **leaky LMS** (Widrow & Kamenetsky): `w←(1−λ)w+μ·e·x`, con λ elegido según el
HORIZONTE de memoria deseado, no a tanteo. Los **three-factor rules** (Frémaux & Gerstner 2016) generalizan esto a
lo bioplausible: elegibilidad local (pre) + un tercer factor GLOBAL (dopamina/error) que gatea el cambio —
exactamente la forma de `dlt` en v13q. **Exige:** sólo memoria local (el peso mismo) + 1 escalar global ya
presente. **Cabe:** sí, sin cambios estructurales — es la propuesta 3d del trío. **Predicción (aporte nuevo):** la
teoría de leaky-LMS da la fórmula que el trío tanteó a mano: para retener una fracción f del peso tras n
actualizaciones, λ=1−f^(1/n)≈ln(2)/n si f=0.5. Con n≈331 mordidas/semilla (dato de Agente C) da λ≈0.0021 — cae
justo en el rango empírico 0.001–0.003 que el trío ya encontró por prueba y error. Propongo calibrar λ POR SEMILLA
como ln(2)/n_mordidas_lenta(semilla) en vez de constante fija: predigo que el rango intercuartílico de
`acc_lenta` en 20 semillas nuevas baja a ≤70% del que da λ=0.002 fijo (menos varianza semilla-a-semilla), sin mover
mucho la mediana.

## 3. Expansión aleatoria + lectura lineal (Cover, reservoir, random features)
Cover (1965): con N=2d dicotomías genéricas, exactamente la mitad son separables por un hiperplano; con 20
patrones eso ya pide sólo d≳10, y v13q tiene 21 (22 con constante) — la dimensión sobra. Pero XOR/paridad NO es
una dicotomía genérica: es el caso extremo de "alta frecuencia" del espectro de Fourier de funciones booleanas, y
está documentado que expansiones/kernels aleatorios ROTACIONALMENTE INVARIANTES (RBF, o cualquier `randomK` sin el
producto explícito) necesitan un número de unidades que crece exponencialmente para capturar paridad (Bengio,
Delalleau & Le Roux 2006; confirmado en redes por Daniely & Malach, NeurIPS 2020) — coincide con el dato que ya
está en el registro: `random15` da 0.500, igual que azar. **Exige:** no tamaño sino la interacción CORRECTA
(P0·P1 explícito); con eso, el mínimo real es d=3 (P0,P1,P0·P1) o 4 con sesgo. **Cabe:** sí, v13q cuadrática ya la
tiene — el cuello de botella está en la regla que la lee (mecanismo 2), no aquí. **Predicción:** barrer
`lectura='randomK'` con K∈{15,50,200} (mismo `eta_s`, T=200000) dará mediana(`acc_lenta`,xor01) en [0.45,0.55] para
TODO K, sin mejorar con K; una `phi` mínima de sólo {P0,P1,P0·P1,1} (4 entradas, menos parámetros que random200)
debería superar 0.60 con la regla del punto 2 — si `randomK` sí mejora con K, refuta esta lectura.

## 4. Muestreo/currículo local (replay, incertidumbre)
3/10 semillas dejan una clase XOR entera sin mordida (Agente C): es techo de muestreo, no de regla. RL ataca esto
con **prioritized experience replay** (Schaul et al. 2015: repetir transiciones por error, no uniforme) y su
variante para clases raras, replay balanceado guiado por incertidumbre (2024: prioriza lo más incierto como proxy
de "minoritario", sin necesitar la etiqueta). Aquí no hay buffer ni backprop, pero el principio se traduce local:
cada celda Kenyon lleva un contador propio de mordidas recibidas; al empatar distancia, preferir el objeto cuyo
código tenga MENOR cuenta mínima — información 100% local. **Ojo:** cambiar la tasa de aparición del mundo por
clase caería en la trampa 3 de `EQUIPO.md` (mundo que se come la comida); "novedad de sitio" (Bloque 2bis, recién
cerrada) ya mostró que un bono de exploración por visitas mueve poco frente al recuerdo de veneno (−3) — mismo
riesgo de escala aquí. **Exige:** un contador entero por celda (memoria mínima), sin señal global nueva. **Cabe:**
sí, es local por construcción. **Predicción:** con el sesgo por cuenta mínima, en 20 semillas nuevas la fracción
con una clase XOR sin mordida antes de T/2 baja de 3/10 a ≤1/20, y la mediana de mordidas-antes-de-sonda sube de
~331 a ≥450, con `px0`/`azar` estables (±0.05).

## Tabla: mecanismo → mínimo cambio en JUACO → predicción → riesgo

| mecanismo | mínimo cambio en JUACO | predicción numérica (20 semillas, T=200000) | riesgo |
|---|---|---|---|
| 1. Kenyon→MBON / unique cue | correr `eta_s=0` (vía rápida sola); barrer K=3 vs K=5 | xor01 a priori 0.40–0.50 (K=3); ≥0.55 (K=5) | confundirlo con el efecto de la vía lenta si no se aísla con `eta_s=0` |
| 2. Delta con signo + leaky-LMS | `regla_lenta='delta'`, `phi'=phi+[1]`, λ **por semilla** = ln(2)/n_mordidas | IQR(`acc_lenta`) ≤70% del de λ fijo=0.002; mediana sin cambio grande | λ adaptativo puede sobreajustar si n varía poco entre semillas (poca señal para calibrar) |
| 3. Expansión: estructura vs. tamaño | añadir `lectura='randomK'` barrida; probar `phi` mínima {P0,P1,P0·P1,1} | `randomK` plano en [0.45,0.55] ∀K; `phi` mínima ≥0.60 | si `randomK` mejora con K, refuta la lectura de "dureza de paridad" aplicada aquí |
| 4. Currículo local por cuenta de celda | contador `visitas_c` por celda Kenyon + desempate en `see()` | semillas con clase vacía 3/10→≤1/20; mordidas pre-sonda ~331→≥450 | trampa 3 (mundo asimétrico) si el sesgo se mueve al mundo en vez de a la celda; precedente "novedad de sitio" sugiere efecto chico frente a −3 de veneno |

## Fuentes más útiles

1. Frémaux, N. & Gerstner, W. (2016). *Neuromodulated Spike-Timing-Dependent Plasticity, and Theory of
   Three-Factor Learning Rules.* Frontiers in Neural Circuits.
   https://www.frontiersin.org/articles/10.3389/fncir.2015.00085/pdf — da la forma general (elegibilidad local ×
   factor global) que ya usa `dlt` y fundamenta la propuesta 3d del trío; su marco de leaky-LMS predice el λ que
   el trío halló a tanteo.
2. Dasgupta, S., Stevens, C.F. & Navlakha, S. (2017). *A neural algorithm for a fundamental computing problem.*
   Science 358(6364):793-796. https://www.science.org/doi/10.1126/science.aam9868 — números concretos de la
   expansión dispersa real (∼150 PN→∼2000 Kenyon, ∼6 entradas/celda, ∼5% activas) para comparar contra los 90/K=3
   de v13q.
3. Deisig, N., Lachnit, H. & Giurfa, M. (2001). *Configural olfactory learning in honeybees: negative and
   positive patterning discrimination.* Learning & Memory 8(2):70-78.
   https://learnmem.cshlp.org/content/8/2/70.full.html — el "XOR de dos olores" ya resuelto en un cuerpo
   fungiforme real, con la teoría del "unique cue" como mecanismo candidato para el mecanismo 1.
