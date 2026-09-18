# SALA 2 — ángulo `grafo_tokens`: **EL CÓDIGO ES EL TOKEN, LA PALABRA ES GRAFO** (diseño de v16 desde v14.1)

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales (sin backprop en el
runtime) que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. Primero la frontera;
segundo, que viva. El método manda sobre el cómo (`EQUIPO.md` 1–14, `CLAUDE.md`).

Creador de la sala 2, 18 sep 2026 (mañana). **Nada de lo de abajo se ha corrido en serie**; no se editó ningún archivo del
repo; no hay `Pool`; no hay commits. Lo que sí se midió (y se declara): tres diagnósticos ESTRUCTURALES que construyen `KW`
como el tronco y leen códigos sin simular (`sala2/diagnostico_variantes.py`, `diagnostico_familias4.py`,
`diagnostico_mundo.py`; semillas 1201–1400, milisegundos) y **UNA corrida de un proceso** del tronco v14.1
(`organismo_v14.run(1201, T=50000)`, 2 s) para leer los pesos reales de la vía lenta. Por eso la serie propuesta empieza en
**1211** (la 1201 ya se vio).

**Hipótesis del director (18 sep 09:40, textual):** *"la tokenización y la representación de algo: si sal es sal será número
uno, lo guardo, lo vectoriza; y después sal rosa lo vectoriza, marca como sal y lo plantea como una variable de lo mismo — eso
es lenguaje. Ahora, si pensamos en el aprendizaje, y ya lo hemos visto, que puede aprender y desaprender."* Y a las 05:10:
*"la palabra es grafo, no vectorización"*.

**Traducción operativa (lo que este diseño mide, sin metáforas):** el **token** es el código exacto de Kenyon (3 celdas de
90: la clave que el tronco ya usa en `ncod`); un token es un **nodo**; su **valor vive en sus celdas** (`Wp−Wn`, como hoy).
"Sal rosa" es una retina nueva que cae en **otro** token (medido: el 97 % de las veces); la **arista** es la relación "es
variante de" entre dos nodos: nace **tentativa** por cercanía de imagen (la vectorización sólo como soporte: L1 ≤ 2 en la
retina), se **confirma** por misma consecuencia (la primera mordida da el mismo signo que el token), y se **corta** cuando la
consecuencia contradice a un token estable. Mientras la arista vive, la variable **lee el valor del token y le aporta su
evidencia** (no duplica huella: "lo marca como sal"); cuando se corta, la variable recibe nodo propio y aprende sola. Eso es
"aprender y desaprender" **a nivel de relación**, encima del aprender/desaprender de celdas que el tronco ya tiene. Colisión
de código (misma clave, distinta consecuencia con `R = 0`): la resuelve B-5 (división por `R = 0`), que se compone aquí como
perilla `desambiguar` (inerte en todos los mundos de este bloque: `R ∈ {+1, −3}`).

---

## 1. Qué bloquea (lectura del registro, con evidencia)

| bloqueo | evidencia (registro / medido aquí) | qué le falta al tronco |
|---|---|---|
| **B1. El valor vive en celdas que se comparten por accidente del código, no por decisión.** | Bloque de la sal (08:16): con el mismo código la sal hereda −1.45 y el veneno pierde la mitad del miedo (−1.45 contra −3.0), evitación ×7; B-5 negativo: algún par con el mismo código en 9 % de las semillas (4 estímulos), ≥ 2/3 en 64 %; mundo de regla: 170/200 semillas con pares idénticos, **291 fugas (115 de valencia opuesta)**. Medido aquí: una variante a un movimiento comparte ≥ 2 celdas con su base sólo el **32 %** de las veces, 1 celda 47 %, 0 celdas 21.5 %; código idéntico 2.6 %. | Una relación explícita entre tokens: "este token es variante de aquél" no puede leerse del solapamiento de celdas (demasiado grueso y demasiado azaroso). |
| **B2. La generalización del tronco es LINEAL y COMPARTIDA por píxeles: no sabe a qué palabra pertenece un cambio.** | Etapa 3 cerrada con la vía lenta (G1 1.000 px0); XOR cerrada por identificabilidad (ERR-35: prior de pares o 14 ejemplos). Medido aquí con el proxy que reproduce exactamente los pesos reales de la lenta (`Wps−Wns = [−0.5, 0.75, −1.25, 0.75, −1.25, 0]` en la corrida 1201): **si UNA variante de A se vuelve veneno, la lectura lineal a priori de 2–4 de los 4 hermanos nunca vistos se voltea o se anula** (010101 → −2.00 en los cuatro; 011100 → 010101 −0.00 y 010110 −1.00), mientras **A conserva +1.00** (la fisión de v11 la protege). | Localizar el cambio: que un nodo se separe **sin arrastrar a la familia**. Hoy la vía rápida protege al token (fisión) pero la vía lenta, que es la que lee lo nunca visto, contamina a los hermanos. |
| **B3. La puerta exige 5 mordidas por código exacto; la evidencia no se hereda entre tokens.** | Canje puerta/capacidad (v13 35/60 contra v11 50; v14 51); PATC 5 mordidas y 1 celda consolidada; el código de un patrón cambia al dividir y su evidencia vuelve a cero (implícito en `ncod` por clave). Mundo vivo: tabla en ~11 exposiciones. | "Exposiciones hasta asociar" (decisión 05:10 B) = 0 para una variable de un token conocido; y que la evidencia de la variable **sume al token** en vez de empezar de cero. |
| **B4. Las memorias tabulares del 18 sep no se desdicen o pierden identificabilidad.** | v15d: E2 0/20 (la tabla de un golpe no se desdice), E1 0/20 (la lenta exacta mata de mordidas a la rápida — corregido en v15e con "cada vía su error"); v15e: la tabla de residuos pierde la identificabilidad (xor01 0.250 < OFF). | Que lo que se desdice sea la **relación** (arista), no una casilla; y que cada vía conserve su error (lección de v15e, que se respeta aquí: la vía lenta no se toca). |
| **B5. No hay olvido dirigido; la retención de lo ausente es 0.67 por interferencia.** | HANDOFF §13 nivel 4: "olvido dirigido" en la columna *falta*; mundo largo 0.67/0.50 (interferencia, no inversión); creador B: 46–55 de 90 celdas sin valor legible (huellas redundantes). | Dos olvidos con dirección: cortar la relación que contradice; **no formar** la huella propia de lo que el token ya explica. |
| **B6. La retina de 6 px limita lo que cualquier mundo puede medir (teorema de la retina, ERR-32–34).** | Medido aquí: con las CUATRO bases del mundo vivo, 13 de los 16 patrones de peso 3 quedan a la misma distancia de ≥ 2 bases (sólo 3 variantes puras). Con DOS bases hay 10 variantes puras (5 por familia). | Por eso el mundo de este bloque es de dos familias; el alcance es un **escalón** hacia una retina mayor (mundo 2D), no una demostración de lenguaje. |

**Lo que NO bloquea (y no se vende como novedad):** generalizar el **signo** a una variante nunca vista con dos bases. La
vía lenta ya lo hace 10/10 a la primera (corrida real). El grafo sólo puede aportar **magnitud exacta** ahí (|v| ≥ 0.5 en
10/10 contra 6/10) y eso apenas cambia la conducta (la boca de v14 muerde todo lo que no sea negativo: enmienda 1 del mundo
vivo, "el impulso tapa el valor cero").

---

## 2. Mecanismo: v16 = v14.1 + `grafo` (+ `desambiguar` de B-5), por anclas sobre `organismo/organismo_v14.py` (feefc88b1fd8d434)

### 2.1 Estado nuevo (sólo existe con `grafo=1`; con `grafo=0` ninguna línea nueva se ejecuta ni toca el rng)

```
_img  : dict  código (frozenset de 3 celdas) -> imagen P (6 floats) de la PRIMERA vez que ese token se vio en la boca
_np   : dict  código -> código padre (la arista "es variante de") o None (raíz)
_est  : dict  código -> 'tent' (arista tentativa, sin mordida) | 'conf' (confirmada) | 'corte' | 'solo' (sin candidato)
_ultR : dict  código -> última consecuencia R recibida por ESE token (para saber si el token está estable)
_gc   : dict  contadores de sólo lectura: tent, conf, corte, pool, mig, abst
```
Memoria: por token 6 + 3 escalares; sin pesos nuevos, sin tasas nuevas, sin tope nuevo. **Constantes nuevas: `g_sol = 2.0`**
(radio L1 de la arista tentativa = exactamente "un movimiento" de un patrón de 3 píxeles; la otra base queda a ≥ 4 por
construcción del mundo, así que no hay aristas equivocadas ni empates entre familias — medido, no ajustado) y el umbral de
consolidación **0.2, que es el de v11** (no es nuevo). Perillas de control: `g_shuf` (barajado), `g_esc` (escalar),
`g_corte` (ablación sin corte). B-5: `desambiguar` con sus anclas literales de `experimentos/creacion_B/construye_codigo.py`
(f94aa0a2f714c28d), que no se solapan con las de aquí.

### 2.2 Funciones locales (se insertan tras `_fam`; ninguna consume rng; empates por orden de creación, como `_ord`)

```
_kvec(q)        : vector de 90 con unos en las celdas de q
_raiz(q)        : sigue _np hasta un nodo con padre None (a lo sumo len(_img) saltos)
_vnodo(r)       : (Wp-Wn)@_kvec(r) si _fam(_kvec(r)) (el token es familiar por la puerta de v14.1), si no None
_estable(r)     : _ultR[r] existe, _vnodo(r) no es None y _ultR[r]*_vnodo(r) > 0   # la última consecuencia del token concuerda con su valor
_busca(q,P)     : candidatos = nodos p != q con imagen; d = L1(P, _img[p]); quedan los d <= g_sol; se toma el mínimo;
                  si hay empate y todos tienen la misma raíz o el mismo signo de _vnodo(raíz) -> el primero creado;
                  si el empate mezcla signos -> gana la RAÍZ con más nodos colgando (tamaño de familia = nº de nodos cuya
                  _raiz es ella; prior declarado: "ante la duda, la palabra con más variantes conocidas"); a tamaño igual
                  -> ABSTIENE (None, _est='solo', _gc['abst']+=1); si no hay candidatos -> None.
                  [Por qué no por mordidas: en el mundo de regla la comida se muerde más que el veneno y ese desempate
                  sesgaría hacia "comida" todo lo nuevo; el tamaño de familia cuenta tokens, no mordidas.]
                  [g_shuf=1: el padre es el nodo creado DESPUÉS del más cercano (rotación por orden, como pat_shuf)]
                  [g_esc=1: el padre es el símbolo 'ESC': lee la MEDIA de _vnodo de todas las raíces familiares]
_lee(kc,P,_wf,_ws,escribe): q=_key(kc)
                  si q no tiene imagen y escribe: _img[q]=P.copy(); _np[q]=_busca(q,P); _est[q]='tent' si _np[q] else 'solo'
                  v=_vnodo(_raiz(q)) (o la media si 'ESC')
                  devuelve v si v no es None; si no, (_wf if _fam(kc) else _ws)      # <- v14.1 exacto como respaldo
_gbite(q,P,R)   : (en la mordida) _ultR[q]=R; p=_np.get(q); si p es None -> devuelve None (raíz: aprende sola, v14.1)
                  r=_raiz(q); v=_vnodo(r); si v es None -> None (el token aún no tiene valor: aprende sola)
                  acuerdo = (R>0 and v>0) or (R<0 and v<0)
                  si acuerdo:                       _est[q]='conf'; _gc['conf']+=1;  devuelve r      # CONFIRMA y APORTA al token
                  si _est[q]=='conf' y not _estable(r) y g_corte: _gc['pool']+=1;    devuelve r      # la FAMILIA cambia: la variable aporta
                  si g_corte:  _np[q]=None; _est[q]='corte'; _gc['corte']+=1;        devuelve None   # CORTE: nodo propio, aprende sola
                  si no (ablación SIN_CORTE):                                         devuelve r
_gmig(q,P)      : tras la plasticidad, q2=_key(kenyon(P)); si q2!=q: _img[q2]=P.copy(); _np[q2]=_np[q]; _est[q2]=_est[q];
                  _ultR[q2]=_ultR[q]; _np[q]=q2 (el token viejo difiere al nuevo: la palabra sigue); _gc['mig']+=1
```

### 2.3 Anclas (texto literal del tronco → sustitución). Con `grafo=0` cada expresión es la original bit a bit

| # | ancla en `organismo_v14.py` (única) | cambio |
|---|---|---|
| A0 | `,puerta_pat=5,pat_shuf=0,pat_min=1):` | `,puerta_pat=5,pat_shuf=0,pat_min=1,grafo=0,g_sol=2.0,g_shuf=0,g_esc=0,g_corte=1,desambiguar=0):` |
| A1 | `ncod={}; _ord=[]   # B: evidencia del CODIGO EXACTO ...` | añade `_img={}; _np={}; _est={}; _ultR={}; _gc=dict(tent=0,conf=0,corte=0,pool=0,mig=0,abst=0)` |
| A2 | tras la definición de `_fam` | define `_kvec, _raiz, _vnodo, _estable, _busca, _lee, _gbite, _gmig` (§2.2) |
| A3 | en `valor(P)`: `return _f+_s if puerta is None else (_f if _fam(_k) else _s)` | `return _f+_s if puerta is None else (_lee(_k,P,_f,_s,False) if grafo else (_f if _fam(_k) else _s))` (lectura sin escribir nodos) |
| A4 | boca: `_wt=_wf+_ws if puerta is None else (_wf if _fam(kc) else _ws)` | `_wt=_wf+_ws if puerta is None else (_lee(kc,PAT[kk],_wf,_ws,True) if grafo else (_wf if _fam(kc) else _ws))` — **primera vista = nodo + arista tentativa; el valor a priori de la variable es el del token** |
| A5 | tras `ncod[_ky]=ncod.get(_ky,0)+1   # B: evidencia del codigo exacto` | `_gr=_gbite(_ky,PAT[kk],R) if grafo else None` |
| A6 | antes de `dlt=R-_wt if puerta is None else R-_wf` (dentro de `if learn:`) | `if grafo and _gr is not None: kc=_kvec(_gr); _wf=float(Wb@kc)` — **la mordida de la variable actualiza las celdas del TOKEN** (delta, drenaje, techo, `err/mu/mup/mun`, división: las mismas líneas de v14.1, sobre las celdas de la raíz y con la imagen `P` de la variable). La vía lenta sigue aprendiendo de SU error con la imagen de la variable (línea intacta: lección de v15e) |
| A7 | tras la última línea de la rama `elif err[c]>theta` (`Wp[j]=Wp[c]; Wn[j]=Wn[c]; mu[j]=mu[c].copy(); ...`), al nivel de `if plast:` | `if grafo and plast: _gmig(_ky,PAT[kk]); ` y si hubo aporte `_gmig(_gr,_img[_gr])` (si el token cambió de código al dividir, la palabra migra) |
| A8 | `return dict(sobre=sobre,` | `return dict(grafo=grafo,g_nodos=len(_img),g_cont=_gc,g_arbol={...},sobre=sobre,` (sólo lectura) |
| B-5 | `if Wb[c]*R<0 and abs(float(Wb[c]))>0.2 and float(kj@P)>float(KW[c]@P) and (~activa).any():` y la fisión | las dos sustituciones literales de `construye_codigo.py` (COND_A→COND_B, FIS_A→FIS_B) |

**Cómo queda apagado ≡ v14.1 bit a bit:** todo lo nuevo vive detrás de `if grafo` / `if desambiguar`; A3 y A4 devuelven la
expresión original cuando `grafo=0`; ninguna función nueva llama a `rng`; los empates se rompen por orden de creación. Arnés
`identidad_v16tok.py`: **I1** 12 escenarios × 2 semillas (T = 30 000) ≡ v14.1 con las dos perillas apagadas; **I2** rng no consumido
a T = 120 000; **I3** mundo de regla 3 reglas × 2 ≡ `organismo_v14g`; **I4 (predicción de inercia, como la I5 de B-5):** con
`grafo=1` los escenarios **E1, E2, E2I, E2L, CTRL, CTRL2 y E2I-misma son v14.1 bit a bit** (en ellos ningún nodo cae a L1 ≤ 2 de
otro: A y B distan 4; C dista 4 de ambas; en E2L y E2I-misma los aliados son el MISMO nodo) — y **E2J/E2K deben diferir** (D dista
2 de B: arista tentativa D→B, apuesta equivocada, corte en la primera mordida) — un control que debe fallar dentro del arnés;
**I5** `desambiguar=1, grafo=0` ≡ `organismo_v14_codigo_on` (2f7794d92e68cc89); **I6** el mundo de familias con las perillas
apagadas ≡ `organismo_v14g` en las mismas fases.

### 2.4 Lo que hace, en cuatro frases medibles
1. **Primera vista:** una retina nueva a un movimiento de un token conocido lee el valor del token (exacto: +1 / −3), sin morder.
2. **Confirmación:** su primera mordida concuerda → la arista se confirma y **desde entonces sus mordidas aportan a las celdas del
   token** (no forma huella propia: olvido dirigido por redundancia; la evidencia de la familia se suma en un solo lugar).
3. **Corte:** si su mordida contradice a un token **estable** (la última consecuencia del token concuerda con su valor) → corte:
   nodo propio, aprende sola con las líneas de v14.1 (la fisión protege al token, como hoy). Los hermanos siguen leyendo el token.
4. **Propagación:** si contradice a un token **inestable** (el propio token acaba de recibir lo contrario: la familia cambia) → no
   corta: aporta al token, y **toda la familia se desdice a la vez** cuando el token cruza el cero.

---

## 3. Por qué sale de la frontera: capacidad NUEVA y MEDIBLE

| capacidad | hoy (v14.1) | con el grafo | cómo se mide (número) |
|---|---|---|---|
| **C1 Localización del cambio** ("un nodo se separa sin arrastrar a la palabra") | la vía lenta reparte el cambio de una variante entre los píxeles: los **hermanos nunca vistos** heredan la contaminación (proxy: 2–4 de 4 hermanos con signo volteado o nulo) | el corte aísla a la variante; los hermanos nuevos leen el token intacto | acierto de signo a priori (puntuación G1: 1 / 0.5 / 0) en las variantes introducidas **después** del cambio, ON contra OFF, pareado por semilla |
| **C2 Propagación del cambio por la familia** ("una mordida de sal enseña a sal rosa") | cada variante familiar tiene celdas propias y se desdice por su cuenta (3–11 mordidas cada una) | las variables aportan al token y leen el token: la familia se desdice cuando el token cruza el cero | mordidas de veneno de toda la familia tras la inversión de la familia, ON contra OFF (razón de medianas, A₁₂: integrales de trayectoria, ERR-37b) |
| **C3 Asociación sin morder, exacta** | signo correcto a la primera (10/10) pero débil (|v| ≥ 0.5 sólo en 6/10) | +1 / −3 exactos a la primera en 10/10 | `exp_asoc` (exposiciones hasta signo correcto y |v| ≥ 0.5): ON 0; OFF ≥ 1 en las variantes débiles |
| **C4 No duplicar huella** | cada variante consolida 1–3 celdas propias; 46–55 de 90 celdas sin valor legible en composición | las variables confirmadas no consolidan celdas propias | celdas con \|Wp−Wn\| > 0.2 y divisiones al final, ON ≤ OFF |
| **C5 Aprender y desaprender la RELACIÓN** | no existe la relación | tentativa → confirmada → corte, contadas | `g_cont` por corrida: en el mundo de familias, confirmadas = 4/4 variantes tempranas y cortes = 2 (las dos Vf) en ≥ 18/20; en AZAR cortes ≈ la mitad |

Lo que sigue **igual** y se dice: la separación de la propia variante que cambia (Vf) la hace la fisión de v11 en ON y en OFF
(≈ 3–5 mordidas para cruzar el cero: el corte no acelera ni frena ese paso; predicción de igualdad, §4 P2); el token base
conserva su valor en los dos (la fisión). La novedad está en **los demás miembros de la familia**: hermanos nuevos (C1) y
hermanos familiares (C2).

**Conexión con la misión:** menos mordidas para asociar (C3, C2), generalizar sin contaminar (C1), desaprender con dirección
(C5), memoria sin huellas redundantes (C4). Y una representación en grafo real —nodos = tokens, aristas = "es variante de"—
sobre la que se puede preguntar después por composición (nodos que cuelgan de dos) y por transmisión (enviar el nombre del
token, no la retina), sin haber tocado la vía rápida ni la lenta.

---

## 4. Preregistro (borrador para el coordinador; se corre sólo si él lo convierte en bloque)

### 4.1 Mundos (instrumento `organismo_v16tok_f.py`, por anclas desde `organismo_v16tok_g.py` ← `organismo_v14g.py` 1f1318480cd34cde, `mundo='familias'`)

Bases: **A** `110100` comida, **B** `101010` veneno (las del tronco). Variantes a un movimiento (peso 3, L1 = 2 de su base, ≥ 4 de
la otra), elegidas **estructuralmente** antes de correr y declaradas aquí:

| familia | Vf (cambia en F3) | V2 (entra en F2, hermano temprano) | V4 (entran en F4, nunca vistas antes) |
|---|---|---|---|
| A (+) | `010101` | `011100` | `010110`, `100101`, `110001` |
| B (−) | `001011` | `011010` | `001110`, `100011`, `101001` |

(B es la imagen de A bajo la permutación de píxeles 1↔2, 3↔4; sus variantes se eligen con la misma permutación.)
**Por qué esta Vf (hecho estructural, medido en `diagnostico_mundo.py`):** la contaminación lineal cae sobre los hermanos
que comparten píxeles con la variante cambiada, es decir **los que están a L1 = 2 de ella**; los hermanos a L1 = 4 no se
contaminan (proxy +1.00). Vf = `010101` es la única variante de A con los cuatro hermanos a L1 = 2 → el proxy los deja a los
cuatro en **−2.00** (todos volteados). Y esos hermanos quedan a la vez a L1 = 2 de A (raíz, +) y de Vf (cortada, −): **empate
de signos**, que el grafo resuelve por tamaño de familia (A ≥ 2 nodos contra Vf 1) — la regla existe para este caso y se
declara aquí. `T = 200 000`; fases: F1 [0, 50k) bases; F2 [50k, 100k) entran Vf y V2 con la valencia de su familia; F3
[100k, 150k) **Vf cambia de valencia** (A-Vf → veneno, B-Vf → comida); F4 [150k, 200k) entran los V4 con la valencia de su
familia. Mundo **FRONTERA**: igual pero **sin V2** (en F2 sólo entra Vf): en F4 el empate es 1:1 (A contra Vf) → el grafo
abstiene y lee la lenta como v14.1 → predicción de **igualdad** (P7): sin hermanos conocidos, el grafo no decide.
Mundo **INV** (`mundo='familias_inv'`): F2 igual; en 100k **toda la familia** cambia (A y sus variantes → veneno, B y las suyas →
comida); no hay F4. Mundo **AZAR** (`familias_azar`): las 8 variantes reciben valencia por moneda propia (`rng` propio
`seed+800000`, balanceada 4/4), independiente de la familia. Objetos, spawn, boca, energía: los de v14g (sin tocar). Medidas por
patrón, de sólo lectura, copiadas del mundo vivo (`_exp`, `crit_exp=0.5`) y de v14g (`primer`, `W_apriori` en cada fase):
`primer[k]` (W, pb, mordió al primer encuentro), `exp_asoc[k]`, `W_fase[f][k]`, mordidas por fase y tipo, `g_cont`.

### 4.2 Brazos (un cambio por brazo)

| brazo | perillas / mundo | para qué |
|---|---|---|
| **OFF** | `grafo=0` (v14.1 en el mundo de familias) | **la ruta vectorial**: la lenta lee lo nunca visto |
| **ON** | `grafo=1` | el candidato |
| BARAJADO | `grafo=1, g_shuf=1` | el padre no es el más cercano: el contenido de la arista lo es todo |
| ESCALAR | `grafo=1, g_esc=1` | un prior escalar (la media de los tokens) en vez de la relación específica |
| SIN_CORTE | `grafo=1, g_corte=0` | **control que debe fallar**: sin corte, Vf sigue leyendo al token y no se separa |
| AZAR-ON / AZAR-OFF | mundo `familias_azar` | la arista no puede ayudar; mide su **coste** (apuestas equivocadas) |
| FRONTERA-ON / -OFF | mundo `familias` sin V2 (empate 1:1 en F4) | el grafo abstiene por empate: predicción de igualdad |
| INV-ON / INV-OFF | mundo `familias_inv` | propagación por la familia (C2) |

### 4.3 Predicciones numéricas (escritas antes de construir; semillas **1211–1230**, réplica **1231–1250**; T = 200 000)

| # | predicción | umbral | qué me refuta |
|---|---|---|---|
| **P1** (C3) | `exp_asoc` de las 4 variantes de F2: ON mediana **0** en 4/4; OFF ≥ 1 en la débil de A (`011100`; lenta real +0.25; las otras tres leen fuerte: +1.50, −1.75, −2.50) | ON = 0 en ≥ 19/20; OFF ≥ 1 en ≥ 16/20 para `011100` | ON > 0: la arista tentativa no lee al token (el token no es familiar a tiempo, o el radio falla) |
| **P2** (igualdad) | separación de Vf en F3: mordidas de Vf hasta que la boca lee el signo nuevo | ON y OFF medianas ≤ 6; \|ON − OFF\| ≤ 2 en ≥ 16/20; A y B conservan +1 ± 0.15 / −3 ± 0.3 al final en ≥ 19/20 en ambos | ON ≫ OFF: el corte llega tarde (el token parece inestable); A cae en ON: el aporte de la variable dañó al token antes del corte |
| **P3** (C1, **decisiva**) | acierto a priori (G1: 1 / 0.5 / 0 por patrón) en los 6 V4 al primer encuentro en F4 | ON mediana **1.000** (≥ 0.92 en ≥ 18/20); OFF mediana **≤ 0.60** (proxy: los cuatro hermanos de cada familia a −2.00 / +2.00, es decir 0.0; la lenta real será menos extrema porque deja de moverse cuando Vf se evita); ON ≥ OFF pareado 20/20 y ON > OFF en ≥ 14/20 | ON > OFF en < 10/20: la lenta real no se contamina como el proxy → el grafo no aporta nada medible en 6 px y la línea se cierra así; ON < 0.92: la migración, el empate por familia o la lectura del token fallan |
| **P4** (C4) | celdas con \|Wp−Wn\| > 0.2 y divisiones al final (mundo familias) | ON ≤ OFF en medianas; celdas ON ≤ 45 en 20/20 | ON > OFF + 10 %: el aporte al token genera divisiones de más (el precio del pool) |
| **P5** (C2) | INV: mordidas de veneno de la familia (8 patrones) en [100k, 200k) | ON ≤ **0.6 ×** OFF (razón de medianas); A₁₂(ON < OFF) ≥ 0.75; cortes en ON ≤ 2 (mediana) | ≥ 0.9 ×: los cortes por `_ultR` obsoleto (variables mordidas antes que el token) anulan la propagación; entonces C2 se retira y C1 se sostiene sola |
| **P6** (controles) | BARAJADO y ESCALAR: G1 en V4 | medianas en [0.35, 0.65] y < ON en ≥ 16/20 | fuera de banda: la ventaja de ON no viene del contenido de la arista |
| **P6b** (coste) | AZAR-ON: G1 en V4 en [0.35, 0.65]; mordidas de veneno ON − OFF por semilla | mediana ≤ +5 (≤ 1 por apuesta equivocada) | > +5: cada apuesta cuesta más de una mordida (el corte no cierra la apuesta en una) |
| **P7** (frontera) | FRONTERA (sin V2): G1 en V4, ON contra OFF; abstenciones | \|ON − OFF\| ≤ 0.10 en mediana; `abst` = 3 de 3 por familia en ≥ 18/20 | ON > OFF: el empate 1:1 no abstiene como está escrito (instrumento); ON < OFF: el grafo daña cuando abstiene (imposible por construcción: si ocurre, ERR) |
| **P8** (tronco) | examen v3′ ON (`bateria_v16tok.py 20 --desde 101 --log`) y generalización ON (`bateria_generaliza_v16tok.py organismo_v16tok_on 20 --desde 101 --log`) | **8/8**, con E1/E2/E2I/E2L/CTRL/CTRL2/E2I-misma **idénticos** a `examen_v14_e015c10_20260918_053452` (listas `splits`), E2J/E2K 20/20 con ≥ 1 corte D→B en ≥ 18/20; **G1 ≥ 0.80** (predigo ≥ 0.90; v14.1 1.000), **G2 ≥ 0.85**, K 20/20; celdas/divisiones del mundo de regla dentro de ±10 % | cualquier caída: **no entra**; G1 < OFF − 0.05: las familias por valencia del mundo de regla cuelgan patrones de prueba de la familia equivocada (se reporta como coste del prior) |
| SIN_CORTE | Vf en F3 | mordidas de veneno de Vf en F3 ≥ 3 × ON y valor de Vf al final con el signo viejo en ≥ 16/20 | si SIN_CORTE separa igual, el corte no es la pieza que localiza |

**Subconjunto preregistrado (regla 10):** LIMPIAS = semillas en las que ninguna variante tiene el código exacto de la base de la
OTRA familia (2.5 % de los pares; `diagnostico_variantes.py --desde 1211 --n 40`, antes de correr); se reporta el conjunto completo
y al lado las LIMPIAS con los mismos umbrales. **Regla 12:** un veredicto a ±1 semilla dispara la réplica 1231–1250.
**Cláusula:** si P8 cae, v16 no entra al tronco; si P3 cae, la línea grafo_tokens se cierra en esta retina con la letra *"la
palabra-grafo no supera a la lectura lineal en 6 px"*; **no se buscan radios ni modos después de ver datos** (`g_sol = 2.0` fijo).

---

## 5. Coste e instrumentos

Sufijo `tok` en todos los instrumentos de esta línea: en `sala2/` ya existen `organismo_v16.py` y `construye_v16.py` de otro
creador (09:54); nada de eso se toca ni se importa. Carpeta propuesta: `experimentos/sala2_tok/` (la crea el implementador;
este creador no ha construido ningún instrumento: sólo los tres diagnósticos estructurales de `registro/investigacion/sala2/`).

| pieza | origen (sólo lectura, sha verificado al construir) | nota |
|---|---|---|
| `construye_v16tok.py` → `organismo_v16tok.py` / `_on` | `organismo/organismo_v14.py` feefc88b1fd8d434 + anclas B-5 de `construye_codigo.py` f94aa0a2f714c28d | `_on` = `grafo=1, desambiguar=1` por defecto (lo examinan las baterías) |
| `organismo_v16tok_g.py` / `_on` | `organismo/organismo_v14g.py` 1f1318480cd34cde | mundo de regla (batería de generalización) |
| `organismo_v16tok_f.py` | ← `organismo_v16tok_g.py` (+ fases, `familias`/`_inv`/`_azar`/`frontera`, medidas de sólo lectura copiadas del mundo vivo) | con `mundo='AB'` y perillas apagadas ≡ v14.1 (I6) |
| `bateria_v16tok.py` | `organismo/bateria_v14.py` 72216f5415de0c86 sobre `_on` | los sha de `organismo_v11/v10` se leen desde `organismo/` (ERR-42); **humo que ESCRIBA su JSON antes de la serie** (regla 14) |
| `bateria_generaliza_v16tok.py` | `organismo/bateria_generaliza.py` 9cf72581ebae7dea | la entrada nueva se compara **campo a campo** con `'organismo_v14'` por el constructor: `eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1` + `grafo=1, desambiguar=1` (ERR-38/ERR-41: nada "por defecto") |
| `identidad_v16tok.py` | I1–I6 (§2.3) | un proceso, T = 30 000 (≈ 3–4 min); I4 incluye el control que debe fallar (E2J/E2K) |
| `corre_v16tok.py` | subprocesos SECUENCIALES: identidad → P8 examen → P8 generalización → familias (5 brazos × 20) → AZAR, FRONTERA, INV (2 brazos × 20 cada uno) | `--humo` de un proceso (semilla 1211, ON/OFF, T = 200 000): 4 corridas ≈ 40 s; **el `Pool` sólo lo lanza el coordinador, y nunca con v15e corriendo** |

Pared estimada con `Pool(14)` (referencias de hoy): examen ≈ 4 min; generalización ≈ 1 min; familias 100 corridas × 200 000 ≈
1.5 min; AZAR/FRONTERA/INV 120 corridas ≈ 1.5 min; identidad ≈ 4 min en un proceso. **Total ≈ 12 min** (220 corridas de mundo +
las de las baterías), réplica ≈ 5 min.
Gemelo numba: no en este bloque (los instrumentos nuevos de la mañana tampoco lo tuvieron); antes de congelar, sí (regla 9).
Lo que este creador gastó: 3 diagnósticos estructurales (ms) y UNA corrida de un proceso T = 50 000; ningún `Pool`.

---

## 6. Humo y espejos: cómo podría engañarnos y cómo se evita

1. **"Acierta a la primera" que ya acertaba.** La lenta lee el signo correcto 10/10 en dos bases (medido). Si alguien reporta
   sólo el acierto de signo en F2, el grafo "gana" sin aportar nada. Evitación: P1 se reporta con `exp_asoc` (signo **y** |v| ≥ 0.5)
   y se declara que en signo no hay diferencia esperada; la decisiva es P3 (V4 después del cambio), no F2.
2. **El impulso tapa el valor.** La boca muerde todo lo ≥ 0 (`Vb = 1.2·W + 2·hambre + 0.5`): diferencias de VALOR pueden ser
   invisibles en CONDUCTA. Se reportan las dos (W a priori y `pb` al primer encuentro, como G1/G2), y ninguna predicción de
   conducta se vende como conocimiento.
3. **El proxy no es la lenta.** La contaminación de P3 sale de un proxy de mínima norma (exacto para dos bases en la corrida real,
   pero no incluye dos canales, drenaje ni mordidas desbalanceadas: tras evitar a Vf la lenta deja de moverse). Por eso OFF ≤ 0.85
   es una **predicción que puede fallar**, y si falla la línea se cierra con esa letra, sin recalibrar.
4. **Un mundo diseñado para que la lenta falle.** Sí: como XOR. Se declara: Vf elegida estructuralmente (antes de datos) como
   la variante que más contamina a sus hermanos en el proxy; y el brazo FRONTERA (sin hermanos conocidos) va con predicción
   de **igualdad**: el grafo abstiene. Al principio yo había escrito la tabla al revés (Vf con hermanos lejanos) por un error
   de distancias; corregido antes de construir nada y sin ver datos de ninguna serie; queda dicho.
5. **Empates.** El sintetizador de la sala cazó un 17/20 falso por desempate por índice (§A13). Aquí el empate de signos se
   resuelve por **tamaño de familia** (nodos, no mordidas: las mordidas sesgarían hacia comida) y a tamaño igual **abstiene**;
   el prior "la palabra con más variantes conocidas" es exactamente lo que P3 mide, así que su coste se mide en AZAR (P6b) y su
   ausencia en FRONTERA (P7); se reporta `abst` por corrida. Nunca se consume rng: identidad. Riesgo declarado para P8: en el
   mundo de regla los patrones de entrenamiento forman familias por valencia y un patrón de prueba puede colgar de la familia
   mayor aunque su valencia sea la otra; por eso G1 ON se predice ≥ 0.90 y no 1.000, con la letra de la batería (≥ 0.80) mandando.
6. **`_ultR` obsoleto.** En INV, una variable mordida antes que su token ve al token "estable" (última R vieja) y corta: pierde
   la propagación. Se predice (cortes ≤ 2) y se cuenta; si domina, C2 se retira (P5) y se dice.
7. **El aporte al token puede dividir de más.** La mordida de la variable actúa sobre las celdas del token con la imagen de la
   variante (`dist ≠ 0`): con conflicto de signo, la fisión de v11 dispara sobre el token. Guardas: celdas ≤ 45 (examen), ±10 % en
   el mundo de regla, P4; y la migración (`_gmig`) para que la palabra siga al código nuevo. Si el precio aparece, cuenta en contra.
8. **Fuga por la puerta.** Una variable confirmada acumula `ncod` y podría hacerse "familiar" con celdas compartidas
   consolidadas; su lectura propia sería parcial (2/3 del token). La prioridad de lectura (arista → propia → lenta) lo evita y es
   una decisión escrita, no un ajuste; se mide su efecto en I4 (E2J/E2K difieren, el resto idéntico).
9. **Alias entre familias** (2.5 % de las variantes con el código exacto de la otra base; B–D/C–D 4 % entre bases del mundo vivo):
   subconjunto LIMPIAS preregistrado; el conjunto completo manda.
10. **El mundo que se come la comida.** Lo rechazado se queda (trampa 3): exposiciones por patrón desiguales. Todas las medidas
    son por exposición y por patrón; se reporta la tabla de exposiciones; nada agregado sobre patrones sin su tabla al lado.
11. **Vocabulario.** Lo permitido si pasa: *"lee el valor del token a la primera"*, *"se separa sin arrastrar a sus hermanos"*,
    *"la familia se desdice con el token"*, *"aprende y corta la relación"*. Prohibido: "entiende", "lenguaje", "palabra" como
    afirmación (aquí es el nombre del nodo raíz y nada más), "generaliza" fuera de los V4 medidos.
12. **Alcance.** `g_sol = 2.0` es "un movimiento" en retinas binarias de peso 3; en retinas continuas o mayores hay que rederivarlo
    estructuralmente (no barrerlo). Con `R` ruidoso, `_estable` puede oscilar (cortes espurios): régimen que hoy no existe.

---

## 7. Resumen para el coordinador (formato fijo del puente)

- **Hipótesis.** El tronco protege al token (fisión) pero contamina a la familia por la vía lenta; una relación explícita
  "es variante de" (tentativa por imagen, confirmada por consecuencia, cortada por contradicción con un token estable, con aporte
  de evidencia al token) localiza el cambio de una variante y propaga el cambio de la familia, con 0 exposiciones para asociar.
- **Mecanismo mínimo y memoria.** 4 diccionarios por token (imagen, padre, estado, última R); 1 constante estructural (`g_sol = 2.0`);
  8 anclas sobre v14.1; vía lenta y vía rápida intactas en sus reglas; B-5 compuesto e inerte.
- **Instrumento.** `experimentos/sala2_tok/construye_v16tok.py` → `organismo_v16tok(_on)`, `_g`, `_f`; baterías copiadas campo a campo;
  `identidad_v16tok.py` con I4 como predicción de inercia + control que debe fallar; `corre_v16tok.py` secuencial.
- **Predicción numérica.** P3: G1 en las 6 variantes nuevas tras el cambio ON 1.000 contra OFF ≤ 0.60, ON > OFF en ≥ 14/20; P5:
  mordidas de veneno de la familia tras la inversión ON ≤ 0.6 × OFF; P1: `exp_asoc` 0 en 4/4; P7: sin hermanos, igualdad; P8:
  examen 8/8 con 7 escenarios idénticos a v14.1 y G1 ≥ 0.90.
- **Control que puede fallar.** OFF sin contaminación real (P3 cae → línea cerrada en 6 px); cortes obsoletos en INV (P5 cae → C2 se
  retira); BARAJADO/ESCALAR fuera de banda (fuga); divisiones de más por el aporte (P4/P8).
- **Mini-prueba con números.** No corrida (regla 3 y `Pool` de v15e vivo). Medido estructuralmente: cobertura de la arista por
  imagen 100 % (por código 32 %), sin aristas equivocadas; lenta real 10/10 en signo y 6/10 fuerte; contaminación proxy 2–4/4.
