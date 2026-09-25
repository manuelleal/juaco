# INFORME — CÓDIGO GENÉTICO v0 (Opus, equipo organelos, 24-sep-2026). Misión: llegar a la AGI por este camino.

**Veredicto del trabajo: FUNCIONA como instrumento. La pregunta (evolucionabilidad) todavía NO está contestada.**
- El código existe y se replica: una cinta que el cuerpo LEE al nacer y el parto COPIA con errores que la propia cinta regula (TASA por
  tramo y SOS que lee lo vivido por el padre).
- Arranca desde lo más evolucionado (filtra0), con identidad bit a bit. El arnés da **26/26**.
- En la exploratoria (3 semillas, T corto) **la cinta NO se recupera mejor que las perillas.** Ningún linaje se recupera: el cambio
  comida↔veneno mata a todos los brazos por igual. **Mi predicción para la serie es NO (0.55).**

## Lo que dice la investigación (lo mínimo para que un código «se replique y diga dónde evolucionar»)
1. **Von Neumann:** una sola descripción se usa dos veces. El constructor la INTERPRETA y el copiador la COPIA sin interpretarla. La
   descripción incluye al constructor y al copiador ([Wikipedia](https://en.wikipedia.org/wiki/Von_Neumann_universal_constructor);
   [Burks 1969](https://fab.cba.mit.edu/classes/865.18/replication/Burks.pdf)).
2. Lo mínimo es, entonces, separar LEER de COPIAR y que las reglas de la copia estén ESCRITAS en la cinta.
3. **Avida:** el genoma es un programa. EQU apareció sólo cuando las funciones simples intermedias también se premiaban, y a veces por
   mutaciones antes dañinas ([Lenski et al. 2003](https://www.nature.com/articles/nature01568)). La variación sola no basta: hacen falta
   PELDAÑOS en el mundo.
4. **Codificación indirecta** (CPPN; [Stanley 2007](https://link.springer.com/article/10.1007/s10710-007-9028-8)): un genoma chico que se
   REUSA da regularidad. Un gen maestro cambia la estructura entera.
5. En la cinta, lo indirecto necesita repetición y llamada, y que duplicar un tramo duplique una estructura.
6. **La tasa como gen:** los mutadores barren junto con las mutaciones buenas que generan (Sniegowski, Gerrish y Lenski 1997).
7. **Mutación por estrés:** facilita adaptarse a condiciones que cambian
   ([Am. Nat. 2019](https://www.journals.uchicago.edu/doi/10.1086/703457)), pero la evidencia es mixta: la SOS no aceleró la adaptación a
   ciprofloxacina en 200 generaciones ([PMC4614765](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4614765/)).
8. **Robustez:** la mayoría de las mutaciones neutras forman redes por las que se explora sin perder la función
   ([Wagner 2008](https://royalsocietypublishing.org/rspb/article/275/1630/91/76655/Robustness-and-evolvability-a-paradox-resolved)).
9. **Mínimo:**
   - una cinta lineal de largo variable (cambio, inserción, borrado y duplicación);
   - un lector con reuso;
   - un copiador que lee su tasa de la cinta y una señal de lo vivido;
   - **y un mundo que premie los pasos intermedios.**
10. Lo último es lo que hoy nos falta. La cinta dice DÓNDE variar, pero es el mundo el que dice QUÉ variación sirve.

## Qué construí (`experimentos/organelos/codigo/`; no toqué nada fuera de esta carpeta)
- **`codigo_def.py`** tiene tres partes.
  - La cinta: 9 operaciones, `SUM`, `EJE` (pleiotropía, 4 rasgos), `ORG`, `REP`, `DEF`/`LLAMA` (gen maestro), `FIN`, `TASA` y `SOS`.
  - El lector: de la cinta a las 18 perillas de `motor_gramatica` más el órgano de la gramática.
  - El copiador: cambio, borrado, inserción y duplicación en tándem, con la tasa por tramo de la cinta y la SOS según la fracción de
    mordidas malas en las últimas 20 del padre, leída de la física del mundo.
- **`construye_codigo.py` → `motor_codigo.py`**: 25 anclas sobre `motor_gramatica`. Agrega la cinta en el cuerpo, la copia y el
  desarrollo en el parto y en el vivero, el registro de lo vivido y el **mundo que cambia**: `eco['cambio'] = (t, 'A', 'B')` intercambia
  VAL_VIVO. Es el cambio mínimo que el motor permite. Las copias del carro y de `gramatica_def` son byte a byte.
- **`CINTA0`** se compiló desde FIJO:filtra0 en G0. Tiene 30 instrucciones: zona del copiador en 0.002, zona del cuerpo en 0.04 (≈ 1.12
  errores por copia, igual a la carga de PERILLAS) y SOS con umbral 0.3 ×3. El umbral se calibró sólo con el mundo viejo; está declarado.
- **`corre_codigo.py`**: humo, exploratoria por bloques, `--lee` y la serie con Pool. Brazos: CODIGO, PERILLAS, CODIGO_SIN_SOS, AZAR,
  MUT0 y **QUIETO** (descriptivo, sin cambio del mundo).
- **`PREREGISTRO_codigo.md`**: la letra, predicciones con rango, P por veredicto y controles que pueden fallar. Se escribió (sha
  3a7fdec10124627f, 19:58) ANTES del primer número de la exploratoria.

## Identidad: `identidad_codigo.py` → **26/26** (`identidad_codigo_salida.txt`)
- **I2, la pedida:** CINTA0 desarrollada y sin errores da **bit a bit** la misma corrida que `motor_gramatica` con filtra0 fijo (salida
  entera, 314 desarrollos).
- **I2b:** con el copiador prendido en TASA 0 también. El rng de la copia no toca el mundo.
- **I1:** sin código == `motor_gramatica`.
- **I3:** el cambio no toca nada antes de t y después invierte los signos de A y B.
- **I5:** reanudar desde el checkpoint después del cambio da lo mismo.
- **P0–P12:** cada instrucción cambia algo medible y la SOS sube la tasa ×3.0 sólo cuando debe.

## Lo que se vio (EXPLORATORIO: 27901–27903, T 40 000, cambio 10 000, corte 25 000; no es serie)
| brazo | persisten (T) | R0 final solo (mediana) | nacimientos tras el cambio vs antes | SOS antes → después |
|---|---|---|---|---|
| CODIGO | 0/3 | 0.22 | ~50 → 9–17, vuelve a ~20–25 (27903 sí: 40–63) | 0.02–0.04 → **0.20–0.35** |
| PERILLAS | 1/3 (1 cuerpo) | 0.23 | igual | — |
| CODIGO_SIN_SOS | 0/3 | 0.15 | igual | 0 |
| AZAR | 1/3 (1 cuerpo) | 0.00 | igual | sube |
| MUT0 | 0/3 | 0.24 | igual | 0 |
| **QUIETO** (sin cambio) | **3/3** | **0.78** | ~50 → ~50 | — |

- **Lo que mata es el cambio, no el corte.** La tabla heredada vieja (A = +1, B = −3) y lo aprendido no se reescriben lo bastante rápido
  en ~15 000 pasos. En w30 no alcanzan las generaciones para que la selección arregle nada.
- **La SOS sí «lee lo vivido»**: se prende sola tras el cambio en 3/3.
- **Robustez de CODIGO:** de los hijos con error, el 50 % son neutros (el mismo fenotipo), el 13 % cambian y dejan hijos, y el 35 %
  cambian y no dejan. Con 0 errores, el 36 % de los hijos deja hijos. Las mutaciones que se expresan son suavemente dañinas.
- **Largo de la cinta:** 30–33.5 de media; máximo 40.
- ERR-140 (tras el humo 1: el cambio va DENTRO del vivero y la recuperación se mide en nacimientos).
- ERR-141 (tras la exploratoria):
  - t_rec se mide dentro del vivero, porque el derrumbe post-corte se comía la medida;
  - se suma QUIETO, descriptivo;
  - la letra y las predicciones NO cambian.

## Costo de la serie (medido: ~85 s por corrida a T 40 000 con cambio; QUIETO ~141 s)
| bloque | Pool 3 | Pool 6 |
|---|---|---|
| serie (20 semillas × 6 brazos, T 80 000) | ≈ 1.8 h | ≈ 0.9 h |
| réplica | ≈ 1.8 h | ≈ 0.9 h |
| **todo** | **≈ 3.6 h** | **≈ 1.8 h** |

Comandos (SOLO el coordinador):
```
python experimentos/organelos/codigo/identidad_codigo.py
python experimentos/organelos/codigo/corre_codigo.py --serie --ventana serie --pool 3
python experimentos/organelos/codigo/corre_codigo.py --serie --ventana replica --pool 3
python experimentos/organelos/codigo/corre_codigo.py --lee experimentos/organelos/codigo/datos/codigo_serie_s27011-27030
```

## Mis predicciones refutadas y lo que no verifiqué
- **Refutadas en la exploratoria** (3 semillas; se declaran, no se corrigen):
  - «t_rec 2 000–16 000 en todos»: quedó censurado 14/15.
  - «persistencia 6–16/20 por brazo»: 0–1/3.
  - «R0 final 0.4–0.95»: medianas de 0.00–0.24.
  - Mi supuesto de diseño en ERR-140 («el fundador limpio del vivero rescata a todos»): no rescata.
  - **Se cumplió:** la SOS se prende (3/3), la robustez neutra quedó en 0.45–0.70 y el largo en 29–36.
- **No verifiqué:**
  - la serie ni Pool;
  - si con T más largo alguien se recupera;
  - QUÉ cambios de cinta se seleccionan: solo guardo las cintas de los vivos en T, y casi todos se extinguen.
- **Qué sigue si sale NO:** la investigación dice que falta el PELDAÑO, no el código.
  - Probar un cambio GRADUAL (A pierde valor por etapas) o un mundo que alterne (Reina Roja), donde recuperarse rápido pague y la SOS
    tenga tiempo de pagar.
  - Hay que guardar la cinta del banco en el corte para leer qué variación eligió la selección.
