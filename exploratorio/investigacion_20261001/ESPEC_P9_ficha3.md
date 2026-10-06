# ESPECIFICACIÓN CERRADA — P9 ficha 3: planear con traza por tiempo y competencia (1-oct-2026)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con controles y réplicas).

Autor: creador en modo papel. **No se corrió nada** (ni motor, ni humo, ni arnés): todo sale de leer código. Origen: `ENTREGA_2_planear_componer.md`, ficha 3.
Abreviaturas: `E\` = `organelos\experimentos\organelos\escalera\` · `PLAN.py` = `E\carros\O1_LUGAR_PLAN.py` (sus líneas sin la marca "escalera p9" son las de O1_LUGAR) · `pista.py` = `organelos\experimentos\carrera_escuderias\pista.py`.

**Lo que el constructor debe saber antes de empezar (cuatro hallazgos de papel que cambian la ficha):**
1. **Sin muestreo, K nunca se aprende.** O1 muerde una letra neutra una sola vez por instancia (`PLAN.py:84`) y después nunca (`:72` devuelve 0; `:94` no es costeable). Un linaje establecido no tiene fundadores nuevos, así que tendría una sola oportunidad de emparejar K con el bocado. Se añade una regla de muestreo: una mordida "de paso" por vida (sec. 1.4). Es mecanismo nuevo y va en los tres brazos con módulo.
2. **El umbral (b) ≥ 0.6 es inalcanzable con p_x 0.03 y ventana corta**, por oferta de K (sec. 6.3). Queda atado al oráculo de la sonda.
3. **El umbral (c) "≥ 50 % en dos vidas" es inalcanzable** con una regla delta estable (sec. 6.3). Se redefine por cuartos de T; "dos vidas" queda como descriptivo con predicción de fallo.
4. **El brazo hábito tal como lo define el encargo no tiene por qué perder en (a) ni en (c)**: comparte la regla de aprendizaje con `plan` y sólo difiere en dos compuertas de uso. Es la duda D1 (sec. 9). Se construyen las dos variantes; por defecto corre la literal.

---

## 0. Formato fijo de la propuesta

- **Hipótesis:** con el crédito repartido por elegibilidad temporal y en competencia con la memoria de lugar, la letra K adquiere valor sólo por lo que habilita (el plus del bocado dentro del oasis), y el cuerpo la busca cuando no la lleva.
- **Mecanismo mínimo y memoria nueva:** regla delta local (sec. 1). Memoria nueva: `hab` (un float por letra conocida, ≤ 5, del linaje) y `_p3_tu` (un entero por letra, ≤ 5, del cuerpo: tiempo de su última mordida). Nada más.
- **Instrumento y anclas:** carpeta nueva `E\p9f3\`. `construye_p9f3.py` (13 anclas sobre el texto de O1_LUGAR de `construye_p1`, sha fijado), `mundo_p9.py` (subclase del oasis de `E\sondas\mundo_plus.py`; cero anclas nuevas sobre la pista), `corre_p9f3.py`, `identidad_p9f3.py`.
- **Predicción numérica:** sec. 6.
- **Control que puede fallar:** `azar` (crédito a letra equivocada) y `hab` (sin estado).
- **Qué lo refuta:** tabla de desenlaces, sec. 6.5.
- **Mini-prueba de un proceso con números:** NO corrida (restricción del encargo). Se entrega el vector de prueba calculado a mano (sec. 1.6) y el plan de humos (sec. 8).
- **Semillas NUEVAS:** bloque 745xxx y 746xxx (grep de hoy sobre `*.py` y `*.md` de `PROYECTOS\JUACO`: cero apariciones). Detalle en sec. 8.4.

---

## 1. Mecanismo: ecuaciones y orden exacto

### 1.1 Constantes (línea nueva tras `LG_VIAJA`, patrón de `construye_c.py:126-128`)

| nombre | valor | justificación |
|---|---|---|
| `PLAN3` | 1 / 0 | promotor. 0 = O1_LUGAR bit a bit |
| `PLAN_W` | 1.0 | igual que el P9 viejo (`construye_c.py:37`); 0.0 = nunca valora |
| `PL_ETA` | 0.3 | con plus 0.4 y traza 0.8, una sola pareja da Δhab ≈ 0.096 > `PL_MIN`: una pareja basta para empezar a buscar K. Con 0.2 (el `PL_LAM` viejo) daba 0.064, al borde |
| `PL_TAU` | `PENDIENTE_SONDA: tau` = `d_plus` del mundo (provisional 200) | con τ = ventana, la traza al cierre de la ventana vale e⁻¹; así "llave en mano" (sec. 2) coincide con la ventana del mundo sin leerla. Es una constante de diseño que pone el ingeniero, como `LG_NB`; se declara |
| `PL_EMANO` | 0.36787944117144233 (= e⁻¹) | "en mano" ⟺ traza ≥ e⁻¹ ⟺ Δt ≤ τ |
| `PL_EMIN` | 0.01 | por debajo, la traza no acredita (Δt > 4.6 τ) |
| `PL_MIN` | 0.05 | igual que el P9 viejo y que `LG_MIN` |
| `PL_HMAX` | 2.0 | recorte de `hab` a [−2, 2]; lo más que un bocado da de más en una necesidad es extra 0.8 + plus |
| `PL_SITIO` | 1 | compuerta "hay un sitio recordado" |
| `PL_MANO` | 1 | compuerta "la llave no está en mano" |
| `PL_COMPITE` | 1 | lugar y traza comparten el mismo error |
| `PL_AZAR` | 0 | 1 = el crédito va a una letra al azar con la misma masa |
| `PL_PASO` | 1 | muestreo: una mordida de paso por vida a letras neutras |

### 1.2 Estado y valores iniciales (`_p3_init`, llamado desde `__init__`, ancla en `PLAN.py:54`)

```
self.hab = {}        # LINAJE: letra -> float (0.0 si falta)
self._p3_tu = {}     # CUERPO: letra -> t de la última mordida de ESTA vida
self._p3_t = 0       # reloj local: el obs['t'] del paso en curso
self._p3_ph = 0.0    # predicción de la traza en la mordida en curso (la lee _lg_apr)
self.st['p3_val'] = 0; self.st['p3_apr'] = 0; self.st['p3_paso'] = 0
self.st['p3_no_sitio'] = 0; self.st['p3_en_mano'] = 0; self.st['p3_masa'] = 0.0
```

### 1.3 Traza y predicción

```
e(k, t)  = exp(-(t - _p3_tu[k]) / PL_TAU)   si k está en _p3_tu;  0.0 si no
ph(t)    = Σ_k e(k, t) · hab[k]             (escalar; se suma igual a E y a Ag)
```

### 1.4 Uso (en `actua` y `_quiere`)

Al entrar a `actua` (ancla en `PLAN.py:105`): `self._p3_t = int(obs['t'])`.

```
def _p3_sitio(self):                       # sin efectos laterales (no llamar a _lg_meta: cuenta lg_viajes, PLAN.py:238)
    return bool((self.lugar.sum(1) > LG_MIN).any())

def _p3_e(self, k, t):
    tu = self._p3_tu.get(k)
    return 0.0 if tu is None else float(np.exp(-(t - tu) / PL_TAU))   # np ya está importado: sin import nuevo

def _p3_v(self, v, k):                     # reemplaza al _pl_v viejo (PLAN.py:256-261)
    h = self.hab.get(k, 0.0)
    if h <= PL_MIN or (v < 0).any(): return v
    if PL_SITIO and not self._p3_sitio(): self.st['p3_no_sitio'] += 1; return v
    if PL_MANO and self._p3_e(k, self._p3_t) >= PL_EMANO: self.st['p3_en_mano'] += 1; return v
    self.st['p3_val'] += 1
    return v + PLAN_W * h                  # en las dos necesidades, como el P9 viejo

def _p3_paso(self, v, k, lev):             # muestreo: sólo en _quiere (sin desvío: el cuerpo ya pisa la celda)
    return bool(PL_PASO and k not in self._p3_tu and not v.any() and min(lev) > PRUEBA)
```

- `_p3_v` se llama en los dos sitios donde hoy se llama `_pl_v`: `PLAN.py:85` (`_quiere`) y `:113` (bucle de `actua`), siempre ANTES de `_lg_v`.
- `_p3_paso` se llama sólo en `_quiere`, después de `if v is None: return min(lev) > PRUEBA` (`:84`) y antes de `_p3_v`: `if PLAN3 and self._p3_paso(v, k, lev): self.st['p3_paso'] += 1; return True`. `v` es el valor crudo de la letra. "Neutra" = media exactamente (0, 0); K lo cumple porque con cerrojo 0 el mundo devuelve su dS sin tocar (`mundo_tramo_c.py:148-151`).
- La predicción `ph` se usa SÓLO en el error. No se suma al valor de A o C cuando se lleva llave (uso hacia adelante): es otra pieza y no entra.
- Las compuertas son genéricas por letra: ninguna línea del carro nombra a 'K'.

### 1.5 Aprendizaje (en `resultado`, una llamada ANTES de `_lg_apr`, ancla en `PLAN.py:158`)

```
def _p3_apr(self, t, x, k, dS):
    self._p3_ph = 0.0
    v = self._val(k)                                   # media de la letra ANTES de esta mordida (PLAN.py:160 va después)
    if v is not None:                                  # la primera mordida de una letra no enseña (como P1)
        es = {j: self._p3_e(j, t) for j in self._p3_tu}
        es = {j: z for j, z in es.items() if z >= PL_EMIN}
        if es:
            ph = sum(z * self.hab.get(j, 0.0) for j, z in es.items())
            d = dS - v - ph                            # vector (E, Ag)
            if PL_COMPITE: d = d - self.lugar[self._lg_bin(x)]     # bin VERDADERO, valor crudo, ANTES de _lg_apr
            db = float(d.sum()) / 2.0
            nor = max(1.0, sum(z * z for z in es.values()))
            if PL_AZAR:
                m = PL_ETA * db * sum(es.values()) / nor
                ks = sorted(self.n); z = ks[int(self.rng.integers(len(ks)))]
                self.hab[z] = min(PL_HMAX, max(-PL_HMAX, self.hab.get(z, 0.0) + m)); self.st['p3_masa'] += abs(m)
            else:
                for j in sorted(es):
                    m = PL_ETA * es[j] * db / nor
                    self.hab[j] = min(PL_HMAX, max(-PL_HMAX, self.hab.get(j, 0.0) + m)); self.st['p3_masa'] += abs(m)
            self.st['p3_apr'] += 1
            if PL_COMPITE: self._p3_ph = ph
    self._p3_tu[k] = int(t)                            # AL FINAL: una mordida no se acredita a sí misma
```

Y en `_lg_apr` (`PLAN.py:224`) la línea única pasa a tres (con `PLAN3 = 0` las operaciones y su orden son las de hoy):

```
        _d = (dS - v) - self.lugar[b]
        if PLAN3 and PL_COMPITE: _d = _d - self._p3_ph   # ficha 3: lugar y traza comparten el error
        self.lugar[b] += LG_ETA * _d; self.nl[b] += 1; self.st['lg_apr'] += 1
```

**Orden por paso, completo:**

| momento | qué pasa | dónde |
|---|---|---|
| `actua(obs)` | `_p3_t = obs['t']`; valoración con `_p3_v`; decisión de morder con `_p3_paso` y `_p3_v` | `PLAN.py:105, 113, 84-86` |
| al morder (`resultado`, `mordio`) | 1) `_p3_apr`: trazas, `ph`, error con `lugar` viejo, actualiza `hab`, marca `_p3_tu[k]` · 2) `_lg_apr` con `ph` restado · 3) tabla por letra | `PLAN.py:158-160` |
| "al pagar" | no hay evento aparte: el pago ES el `dS` de `resultado()` del mismo paso (`pista.py:298-299`). Todo ocurre en la fila anterior | — |
| al parir (`al_parir`) | `_m['_plan3'] = dict(self.hab)` | `PLAN.py:172-173` |
| al nacer un hijo (`nace`) | `self._p3_tu = {}` (la traza es del cuerpo); `hab` se conserva; `_p3_hereda` sólo si `hab` está vacío | `PLAN.py:177, 179-180` |
| al morir | nada: `muere()` no se toca. Entre `muere` y `nace` no hay pasos (`pista.py:329-351`) | — |
| al refundar (fundador limpio) | instancia nueva: `hab = {}` y `_p3_tu = {}` | `pista.py:347-348` |
| no muerde | `resultado` retorna en `:156`; nada cambia. La traza decae sola porque se calcula del reloj | — |

Relojes: el carro usa `res['t']` y `obs['t']` (`pista.py:240, 251`). El mundo usa `self.t`, que va una unidad adelante (`mundo_tramo_c.py:128-131`), pero la diferencia entre dos mordidas es la misma en los dos relojes. Por eso `Δt ≤ d_plus` del mundo (`mundo_plus.py:58`) equivale a `e ≥ e⁻¹` del carro cuando `PL_TAU = d_plus`.

### 1.6 Vector de prueba (calculado a mano; el arnés lo reproduce con `resultado()` sintético)

τ = 200, η = 0.3. Para aislar la regla, la tabla de A se fija en v(A) = (0.5, 0.3) con `suma = (500, 300)`, `n = 1000` (la media casi no se mueve). `lugar[b] = (0.3, 0.5)`, `hab = {}`.
1. t = 100: mordida de K (conocida, v = (0, 0)) en un bin con `lugar = 0`: sin trazas, no aprende; `_p3_tu = {K: 100}`.
2. t = 150: A en el bin b, dS = (1.2, 1.2). e(K) = exp(−0.25) = 0.7788; ph = 0; d = (0.4, 0.4); db = 0.4; nor = 1. **hab[K] = 0.0935**. `lugar[b]` → (0.5, 0.7) (tolerancia 1e-3 por el corrimiento de la media).
3. t = 170: A en b, dS = (1.2, 1.2). e(K) = 0.7047, e(A) = 0.9048; ph = 0.0659; d = (0.134, 0.134); nor = 1.3153. **Δhab[K] = +0.0216 → 0.1150; hab[A] = +0.0277**.
4. Con `PL_AZAR = 1` y las mismas entradas, `p3_masa` tras el paso 3 es la misma (0.0935 + 0.0493 = 0.1427) y cae en una sola letra por evento.

### 1.7 Qué es del linaje y qué del cuerpo; cómo sobrevive `hab`

- **Del linaje:** `hab`. Vive en el objeto carro, que la pista reutiliza para todos los hijos de la cola (`pista.py:350` llama `nace` sobre el mismo `c`), y viaja además en `al_parir`/`nace` como `_plan3` (para que una sonda pueda reconstruir el carro con `nace(memoria)`).
- **Del cuerpo:** `_p3_tu`. Se borra en `nace`. Aviso: el P9 viejo NO borraba `_pl_last` al morir (`PLAN.py:176-183` no lo toca): la "última letra" cruzaba de un cuerpo al siguiente. Aquí se corrige.
- **Refundación limpia:** `hab` NO sobrevive (`pista.py:347-348`: `crea(ctx)` otra vez, sin `nace`). No hay truco: nada de variables de módulo ni de clase (rompería la enmienda 5 y `revisa_carro`). `hab` sobrevive por tres vías legítimas: (i) el mundo de la ficha 1 deja vivir a la base, así que los linajes establecidos no refundan (P1b: 16/18 establecidos, `BITACORA.md:8`); (ii) `PL_ETA` 0.3 hace que una pareja baste para pasar `PL_MIN`; (iii) el muestreo de paso da una oportunidad de pareja por vida, de modo que un fundador limpio reaprende sin esperar. Todas las medidas de mecanismo se leen sólo en linajes establecidos (0 fundadores tras t = 10 000) y se reporta `hab_K` por linaje junto con sus fundadores.

---

## 2. Información LOCAL: "lleva llave" y "hay un sitio recordado"

| condición | cómo la sabe el carro | variable | ¿existe hoy? |
|---|---|---|---|
| lleva llave | recuerda cuándo mordió él mismo esa letra (`res['t']` en `resultado`, `pista.py:251, 299`) y compara con el reloj que recibe (`obs['t']`, `pista.py:240`): `e(k, t) ≥ PL_EMANO` | `_p3_tu[k]` | **No.** Es la memoria nueva del cuerpo (≤ 5 enteros). El P9 viejo no guardaba nada parecido (`PLAN.py:253`) |
| hay un sitio recordado | algún bin de su memoria de lugar suma más que `LG_MIN` | `self.lugar` (`PLAN.py:199`), con el mismo criterio de `_lg_meta` (`PLAN.py:231-237`) | **Sí.** Cero memoria nueva |

El carro nunca lee `_oz`, `t_k`, `celdas` ni `d_plus`. `PL_TAU` es una constante que escribe el ingeniero; que coincida con la ventana del mundo es una decisión de diseño declarada, no una lectura.

---

## 3. Diff conceptual

### 3.1 Carro: `E\p9f3\construye_p9f3.py` (nuevo; NO se edita `construye_c.py`)

Por qué no editar `construye_c.py`: `corre_c.py:62, 236-237` compara todos los carros de `CC.todas()` con el disco, y `E\juntos\construye_juntos.py` importa sus anclas; cambiarlo movería shas ajenos.

Base: `C1.construye('O1_LUGAR', 1, 0)` con `verifica_origen()` copiado de `construye_c.py:179-184` y los mismos shas (`SHA_CONSTRUYE_P1 = '90dc1b6f848fac80'`, `SHA_O1_LUGAR = '49eee6bb278ea097'`, `construye_c.py:36`). Cada ancla debe aparecer exactamente una vez (`construye_c.py:190-193`).

| # | ancla (texto de O1_LUGAR) | línea en `PLAN.py` | patrón en `construye_c.py` | qué se inserta |
|---|---|---|---|---|
| 1 | docstring de cabecera | 1-4 | 116-118 | cabecera nueva |
| 2 | línea `LG_VIAJA = …` | 41 | 119, 126-128 | las constantes de 1.1 (sin import nuevo: la traza usa `np.exp`) |
| 3 | `if LUGAR: self._lg_init(ctx)` | 54 | 129-130 | `if PLAN3: self._p3_init()` |
| 4 | `self.st['pasos'] += 1` | 105 | 154-155 (lo usa PREG) | `if PLAN3: self._p3_t = int(obs['t'])` |
| 5 | `if LUGAR: v = self._lg_v(v, self._lgx)` | 86 | 131-133 | antes: `_p3_paso` (retorna True) y `v = self._p3_v(v, k)` |
| 6 | `g = self._gana(self._lg_v(v, x) if LUGAR else v, lev)` | 114 | 134-135 | antes: `if PLAN3: v = self._p3_v(v, k)` |
| 7 | `if LUGAR: self._lg_apr(res['pos'], k, dS)` | 158 | 136-138 | **antes** (no después, como el viejo): `if PLAN3: self._p3_apr(int(res['t']), res['pos'], k, dS)` |
| 8 | `self.lugar[b] += LG_ETA * ((dS - v) - self.lugar[b]); self.nl[b] += 1; self.st['lg_apr'] += 1` | 224 | (nueva) | las tres líneas de 1.5 |
| 9 | `if LUGAR: _m['_lugar'] = …` | 172 | 139-141 | `if PLAN3: _m['_plan3'] = dict(self.hab)` |
| 10 | `self.st['cuerpos'] += 1; self.blanco = None` | 177 | (la usa `sondas\construye_orac.py:76`) | `if PLAN3: self._p3_tu = {}` |
| 11 | `if LUGAR and m and '_lugar' in m: …` | 179 | 142-144 | `if PLAN3 and m and '_plan3' in m: m = dict(m); self._p3_hereda(m.pop('_plan3'))` |
| 12 | `if LUGAR: return dict(self._salida_o1(), **self._lg_salida())` | 190 | 145-147 | `if PLAN3: return dict(self._salida_o1(), **self._lg_salida(), **self._p3_salida())` |
| 13 | `\n\ndef crea(ctx):` | 280 | 170-171 | los métodos `_p3_*` |

`_p3_hereda(m)`: `if not self.hab: self.hab = {k: float(v) for k, v in m.items()}`.
`_p3_salida()`: `dict(plan3=dict(W=PLAN_W, eta=PL_ETA, tau=PL_TAU, sitio=PL_SITIO, mano=PL_MANO, compite=PL_COMPITE, azar=PL_AZAR, paso=PL_PASO, hab={k: round(float(v), 4) for k, v in self.hab.items()}))`. Los contadores `p3_*` salen solos por `self.st` (`PLAN.py:194-195`).

Variantes que genera (en `E\p9f3\carros\`):

| archivo | PLAN3 | PLAN_W | SITIO | MANO | COMPITE | AZAR | PASO | uso |
|---|---|---|---|---|---|---|---|---|
| `O1_LUGAR_P3` | 1 | 1.0 | 1 | 1 | 1 | 0 | 1 | brazo `plan` |
| `O1_LUGAR_P3_HAB` | 1 | 1.0 | 0 | 0 | 1 | 0 | 1 | brazo `hab` (literal del encargo) |
| `O1_LUGAR_P3_AZAR` | 1 | 1.0 | 1 | 1 | 1 | 1 | 1 | brazo `azar` |
| `O1_LUGAR_P3_HABNC` | 1 | 1.0 | 0 | 0 | 0 | 0 | 1 | reserva para la duda D1 |
| `O1_LUGAR_P3_PASO` | 1 | 0.0 | 1 | 1 | 1 | 0 | 1 | sólo humo: muestrea y aprende, nunca valora (tamaño del efecto de limpiar K) |
| `O1_LUGAR_P3_MUDO` | 1 | 0.0 | 1 | 1 | 0 | 0 | 0 | sólo arnés |
| `O1_LUGAR_P30` | 0 | 1.0 | 1 | 1 | 1 | 0 | 1 | sólo arnés |

### 3.2 Anclas de identidad bit a bit (arnés `identidad_p9f3.py`, ANTES de mirar números)

Patrón: `corre_c.py:272-283` (salida ENTERA normalizada por JSON, N 9, T 1200, semilla de arnés).

| # | comprobación | por qué debe dar igual |
|---|---|---|
| I1 | `O1_LUGAR_P30` == O1_LUGAR en `mundo_escalera`, salida entera | promotor 0: ningún `if PLAN3` se ejecuta y `_lg_apr` hace las mismas operaciones en el mismo orden |
| I2 | `O1_LUGAR_P30` == O1_LUGAR en `mundo_p9` con K y plus encendidos | igual, en el mundo de la serie |
| I3 | `O1_LUGAR_P3_MUDO` == O1_LUGAR en `mundo_p9` con K y plus, en toda la salida salvo las claves `plan3` y `p3_*` de `d['carro']` | el módulo aprende pero nada lee `hab`: W 0, sin paso, sin competencia, sin rng |
| I4 | `mundo_p9` con todo apagado == `mundo_tramo_c` == `mundo_escalera`, salida entera y estado del rng | cadena de identidad del mundo |
| I5 | `mundo_p9` con `eventos = 1`, `t_dev = None` == `mundo_plus` con las mismas perillas, salvo la clave `p9` del oasis; mismo estado del rng | el registro es de sólo lectura |
| I6 | `mundo_p9` con `t_dev = T` (nunca llega) == `t_dev = None` | la devaluación no toca nada antes de su hora |
| I7 | regla 14: la entrada de `corre_p9f3.tarea` contra `corre_c.tarea` (`corre_c.py:72-91`) campo a campo; cada corrida ES `corre_v143.tarea` | batería copiada |
| I8 | texto construido == disco para las 7 variantes; cada ancla aparece 1 vez | constructor |
| I9 | vector de prueba de 1.6 (tolerancia 1e-3) y `p3_masa` igual en `plan` y `azar` con las mismas entradas | la regla es la escrita; misma masa |
| I10 | los brazos difieren entre sí: `plan` ≠ `hab` ≠ `azar` ≠ `lug` en mordidas de K a T 3000 | los flags actúan |
| I11 | `_p3_tu` vacío tras `nace`; `hab` intacto tras `nace`; instancia nueva con `hab == {}` | 1.7 |
| I12 | con `t_dev` activo, un bocado A/C dentro con llave paga exactamente lo mismo que sin llave, y los contadores de fase 1 se llenan | devaluación |
| I13 | barajado: caso sintético con respuesta conocida (K siempre 10 pasos antes de cada bocado → C alto; K uniforme → C ≈ 1 ± 0.1) y `E` exacto == media de 1000 permutaciones ± 3 % | la medida (a) |
| I14 | guardas del runner: ≤ 6 corridas y ≤ 200 000 pasos en un proceso; `--pool` se niega fuera de `--serie` | `corre_c.py:52, 201, 208` |

La salida del arnés se pega entera en el informe del constructor.

### 3.3 Mundo: `E\p9f3\mundo_p9.py` (nuevo)

No toca `mundo_tramo_c.py` (sha fijado en P7 y P10) ni `mundo_plus.py`. Patrón: `mundo_k.py:17-55` y `mundo_plus.py:91-105`: mismas anclas `ME.ANCLAS + MC.ANCLAS_C`, sólo cambia la clase que se inyecta como `OasisC`. Se fija el sha de `mundo_plus.py` (`PENDIENTE_SONDA: sha_mundo_plus`, cuando la sesión de sondas lo cierre).

`class OasisP9(mundo_plus.OasisPlus)` con dos perillas de módulo más (`eventos = 0`, `t_dev = None`) fijadas con `fija()` como en `mundo_plus.py:83-88`:
- `__init__`: `self.vida = [0]*n; self.t_ini = [0]*n; self.vidas = [[] for _ in range(n)]; self.ev_k = [[] …]; self.ev_ac = [[] …]; self.dev_con = [0]*n; self.dev_sin = [0]*n`.
- `muerde(l, kk, pos, dS)`: sec. 4.1. La rama a cambiar frente al P9 viejo es `mundo_tramo_c.py:152-157` (allí el cerrojo QUITA el extra); aquí cerrojo 0 y la llave sólo AGREGA (`mundo_plus.py:53-63`).
- `muere(l)`: cierra la vida (sec. 4.1) y llama a `super().muere(l)` (`mundo_plus.py:67-68` borra `t_k`; `mundo_tramo_c.py:185-186`).
- `salida(i)`, `info()`: agregan `p9` (sec. 4.2).

### 3.4 Runner: `E\p9f3\corre_p9f3.py` (copia de `corre_c.py` reducida a un peldaño)

- `tarea` = `corre_c.py:72-91` con `RUN[0] = mundo_p9.run`. **Cambio obligado en `:88`:** el filtro de telemetría del carro sólo deja pasar claves `pl_`, `pg_`, `plan`, `pregunta`, `mord`; hay que añadir `p3_` y `plan3` o `hab` no llega al JSON.
- `fila` = `corre_c.py:94-97` más el bloque de sec. 4.3 en lugar de `:106-112`.
- `senal` (`corre_c.py:177`) se reemplaza por la letra de sec. 6. La puerta vieja exigía cruce en un mundo donde nadie cruzaba.
- `P.run` acepta lista de carros (`corre_c.py:277`) pero `CV.tarea` recibe un solo nombre (`:81`): todo es monocultivo de 9, como P1.
- Modos: `--identidad`, `--humo`, `--explora` (un proceso), `--serie`, `--replica`, `--dev`, `--lee`. `--pool` sólo en `--serie/--replica/--dev` y sólo lo usa el coordinador.

---

## 4. Telemetría nueva

### 4.1 Eventos que registra el mundo (física de sólo lectura; el carro no los ve)

En `OasisP9.muerde`, con `tw = self.t` (reloj del mundo) e `i = l.i`:

```
dentro = pos in self.celdas
llave  = (tw - self.t_k[i] <= self.d_plus)          # ANTES de super(): la llave que YA llevaba
dev    = self.t_dev is not None and tw >= self.t_dev
if dev and kk in ('A', 'C') and dentro and self.act_plus:
    r = MC.OasisC.muerde(self, l, kk, pos, dS)       # el oasis de P1, sin plus
    if self.extra_sin is not None:                   # como mundo_plus.py:55-57
        j = 1 if kk == 'A' else 0; z = [r[0], r[1]]; z[j] += self.extra_sin - self.extra; r = (z[0], z[1])
    (self.dev_con if llave else self.dev_sin)[i] += 1
    self.g_nom[i] += r[0] + r[1]; self.g_ef[i] += _ef(l, r)      # como mundo_plus.py:64
else:
    r = super().muerde(l, kk, pos, dS)
if self.eventos:
    if kk == self.X:                 self.ev_k[i].append([tw, self.vida[i], int(dentro), int(llave)])
    elif kk in ('A', 'C') and dentro: self.ev_ac[i].append([tw, self.vida[i], int(llave), int(dev)])
return r
```

En `OasisP9.muere(l)` (el gancho corre en `pista.py:325`, antes de que `esfund` cambie en `:341`, así que `l.esfund` es el del cuerpo que acaba de morir):

```
self.vidas[i].append([self.t_ini[i], self.t, int(l.esfund)]); self.vida[i] += 1; self.t_ini[i] = self.t
super().muere(l)
```

En `salida(i)` se cierra la vida abierta con `[t_ini, self.t, esfund_desconocido = -1]`.

Eventos: tiempo (reloj del mundo), linaje (índice de la lista), vida (índice dentro del linaje), letra (lista `k` o lista `ac`), dentro/fuera (campo en `k`; `ac` sólo guarda los de dentro; los de fuera van como conteo), con/sin llave (campo), fase de devaluación (campo). Sin tope de longitud: truncar rompería la medida; el humo reporta el tamaño del JSON.

### 4.2 Formato del JSON (por linaje, en `d['_carrera']['oasis']['p9']`)

```
{"vidas": [[t_ini, t_fin, esfund], ...],
 "k":     [[t, vida, dentro, en_mano], ...],
 "ac":    [[t, vida, con_llave, fase], ...],
 "ac_fuera": <int>,
 "dev":   {"con": <int>, "sin": <int>}}
```

Y en `pista['oasis']`: `eventos`, `t_dev`, además de `plus`, `d_plus`, `extra_sin`, `regalo` (`mundo_plus.py:79`). El runner copia `_oasis` por linaje (`corre_c.py:85`) y escribe el JSON por corrida (`corre_c.py:127-135`).

### 4.3 Medidas que calcula el runner por corrida (`fila['p9']`)

Sólo linajes establecidos (0 fundadores tras t = 10 000) y sólo eventos con `t < t_corte`, donde `t_corte = t_dev` si hay devaluación y `T` si no.

- **(b) `frac_llave`** = `con / (con + sin)` sobre la lista `ac` (campo `con_llave`).
- **(a) contraste**, con `V = d_plus`:

```
para cada linaje establecido i, para cada vida j con intervalo [a, b) recortado a t < t_corte:
    K = tiempos de la lista k con vida == j        (n_K = len(K); si n_K == 0 se salta)
    F = tiempos de la lista ac con vida == j
    O_j = #{ k en K : existe f en F con k < f <= k + V }
    # esperado EXACTO de barajar K uniforme en [a, b) con F fijo:
    cubierto = medida de la unión de los intervalos [f - V, f) recortados a [a, b)
    p0_j = cubierto / (b - a)
    E_j  = n_K * p0_j
O = Σ O_j ; E = Σ E_j ; N = Σ n_K
C     = O / E                    (contraste; None si E < 5)
techo = N / E                    (lo más que C puede valer: todos los K seguidos de bocado)
C_n   = (O - E) / (N - E)        (contraste normalizado en [0, 1]; None si N - E < 5)
# nulo por permutación (para el percentil; no cambia C):
rng = np.random.default_rng([746000, semilla_de_la_corrida])
repetir 1000 veces: para cada vida, K* = n_K enteros uniformes en [a, b); O* = Σ pares; guardar O*
pct = fracción de las 1000 con O* < O
```

  Qué se conserva fijo: los tiempos de los bocados dentro, los límites de cada vida y el número de K por vida. Qué se baraja: sólo los tiempos de K, dentro de su vida. Se guarda `O, E, N, C, techo, C_n, pct, n_vidas`.
- **(c) devaluación** (sólo corridas con `t_dev = T/2`): tasa de mordidas de K por 1000 pasos-linaje en Q2 = [T/4, T/2) y en Q4 = [3T/4, T): `caida = 1 − tasa_Q4 / tasa_Q2`. Descriptivo: para cada linaje, K por vida en las dos últimas vidas completas antes de `t_dev` y en las dos primeras completas después (`caida_2v`).
- Descriptivos: `hab` de las cinco letras por linaje (mediana), `p3_val`, `p3_paso`, `p3_no_sitio`, `p3_en_mano`, `p3_masa`, fracción de K con `en_mano = 1`, fracción de K con `dentro = 1`, K por 1000 pasos, mundo A+C, razón de pasos en el oasis, fundadores, vida mediana, `plus_ef/plus_nom` (`mundo_plus.py:73`).

---

## 5. Brazos

| brazo | carro | diferencia de flags frente a `plan` | qué controla |
|---|---|---|---|
| `plan` | `O1_LUGAR_P3` | — | candidato |
| `hab` | `O1_LUGAR_P3_HAB` | `PL_SITIO = 0`, `PL_MANO = 0` | K valorada sin mirar el estado (literal del encargo). **Nota: brazo DESCRIPTIVO; ver "Decisiones del coordinador" al final (DC1)** |
| `azar` | `O1_LUGAR_P3_AZAR` | `PL_AZAR = 1` | el crédito de la traza va a una letra al azar con la misma masa |
| `lug` | `O1_LUGAR` (`49eee6bb278ea097`) | sin módulo | piso |

- **Mismo costo y misma memoria en `plan`, `hab` y `azar`:** los tres llevan `hab` y `_p3_tu`, calculan las mismas trazas, el mismo error y la misma predicción, comparten `PL_ETA`, `PL_TAU`, `PL_COMPITE = 1` y `PL_PASO = 1`. `hab` sólo se salta dos `if`. `azar` sólo cambia el destino del crédito y consume un sorteo de `self.rng` (el rng del cuerpo, `PLAN.py:49`; nadie más lo usa) por evento de aprendizaje, y sólo cuando `plan` también actualizaría.
- **Fuga declarada de `azar` (lección de ERR-170):** el sorteo cae en K una de cada |letras conocidas| veces (≈ 20 %). No hay destino fijo limpio: una rotación de letras fuga por el solape de trazas. Se reporta `hab_K` de `azar`.
- **Limpieza declarada:** los tres brazos con módulo muerden K de paso y `lug` no (`lug` muerde K una vez por instancia). Cada mordida repone un objeto (`pista.py:293`), así que el módulo "limpia" K y puede subir la comida. Por eso `plan > lug` no aísla el contenido; lo aísla `plan > azar` (misma limpieza). El brazo `paso` del humo mide el tamaño de la limpieza.

---

## 6. Predicciones, puertas y desenlaces

Todo se lee en linajes establecidos y, salvo (c), en corridas SIN devaluación (decisión cerrada: la devaluación va en un bloque aparte, sec. 8.3, porque apagar el plus a T/2 diluye el cruce de la misma corrida).

### 6.1 Validez (si una falla: NO SE LEE)
- V1: serie completa, 0 abortos, eventos presentes en todas las corridas.
- V2: el piso vive: `lug` con establecidos ≥ 108/180.
- V3: el mundo actúa: `plus` y `d_plus` escritos; en `lug`, `plus_nom` > 0 en alguna corrida o `con = 0` coherente con sus mordidas de K.
- V4: estado por brazo escrito por cada worker (los flags de la sec. 5).
- V5: `p3_masa` de `azar` dentro de [0.5, 2] × la de `plan` (mediana por semilla).

### 6.2 Puertas

> Nota: los umbrales de MA, MB y MC son PROVISIONALES hasta la auditoría; ver "Decisiones del coordinador" al final (DC4).

| puerta | tipo | definición | umbral |
|---|---|---|---|
| **MA** contraste | mecanismo, contra el nulo | mediana por semilla de `C` en `plan`, y `pct ≥ 0.95` en ≥ 15/20 semillas | `C ≥ 2.0` si la mediana de `techo` de `plan` es ≥ 3.0; si no, `C_n ≥ 0.5` (regla fijada antes de datos) |
| **MB** fracción con llave | mecanismo, contra piso y contra `azar` | mediana de `frac_llave` | `plan ≥ PENDIENTE_SONDA: umbral_b`; `lug ≤ 0.25`; `plan > azar` en ≥ 13/20 |
| **MC** devaluación | mecanismo, contra su propia línea base | mediana de `caida` en `plan` (bloque de devaluación) | `≥ 0.50`, y K por 1000 pasos en Q2 de `plan` ≥ 2 × la de `lug` (si no, no hay nada que devaluar: NO SE LEE MC) |
| **XA** cruce contra el piso | conducta | `plan > lug` en linajes que cruzan | ≥ 13/20 semillas y suma ≥ +10 |
| **XB** cruce contra `azar` | conducta (contenido) | `plan > azar` | ≥ 13/20 y suma ≥ +10 |

Nulo de 13/20 con empates en contra: 0.132 por serie; 0.017 con réplica (`PREREGISTRO_p1.md:77-78`).

### 6.3 Revisión de los umbrales del encargo

| umbral | juicio | razón |
|---|---|---|
| (a) `C ≥ 2.0` | **puede ser inalcanzable** | `C ≤ techo = 1/p0`. Un linaje que pasa ~70 % de sus pasos en el oasis (razón de pasos 6–7.5, `BITACORA.md:8, 16`) come dentro a menudo; si más de la mitad de los instantes al azar ya tienen un bocado dentro en la ventana, `C` no puede llegar a 2 aunque todos los K acierten. Por eso la regla condicional a `techo` y el índice normalizado |
| (b) `plan ≥ 0.6` | **inalcanzable con p_x 0.03 y ventana corta** | las mordidas de K no pueden pasar de p_x por reposición: ~3 % de todas las mordidas. Con ventana de ~200 pasos caben 1–2 bocados por llave, así que `frac_llave` tiene un techo del orden de 0.05–0.15. El 0.6 venía de la ventana de 1500. Se ata al oráculo de la sonda (sec. 7) |
| (b) piso `≤ 0.25` | **trivial** | `lug` no vuelve a morder K tras la prueba; su `frac_llave` esperada es ≤ 0.05. En el mundo viejo dio 0.07–0.21 con ventana 1500 y p_x 0.10 (`BITACORA.md:22, 32, 38`). La comparación que informa es contra `azar` |
| (c) `≥ 50 %` en dos vidas | **inalcanzable** | cada episodio con llave baja `hab` en un factor ≈ (1 − η·e²) ≈ 0.8; de 0.6 a `PL_MIN` hacen falta ~11 episodios, y la oferta de K da 1–3 por vida. Además K sigue valorada mientras `hab > PL_MIN`, así que la tasa no cae gradualmente. Se redefine por cuartos (Q4 contra Q2: 25 000 pasos de margen a T 100k); `caida_2v` queda descriptiva y predigo que NO llega a 0.5 |
| cruce `plan > lug` ≥ 13/20 | razonable pero poco probable | depende de que la sonda encuentre espacio (oráculo − piso ≥ +4 de 18). Si el techo es +4, capturar la mitad da +1 por corrida: 13/20 con empates en contra es exigente |

### 6.4 Qué debe pasar con cada control

| medida | `azar` | `hab` (literal) | `HABNC` (reserva D1) |
|---|---|---|---|
| MA | puede empatar: quien muerde K con hambre y cerca del oasis come después. MA es puerta contra el nulo, no contra controles | **empata en papel** (misma regla de aprendizaje; las compuertas no cambian el orden K → bocado) | empata |
| MB | **debe perder** (`hab_K` chico y repartido) | puede empatar o ganar (renueva la llave aunque la lleve) | puede empatar |
| MC | sin lectura si no llega a valorar K | **empata en papel**: desaprende con la misma regla | **debe perder**: sin competencia, el extra del oasis sigue alimentando `hab_K` y las mordidas de K no caen |
| cruce | **debe perder** contra `plan` (XB) | puede empatar | puede empatar |

El encargo pide que `hab` pierda en (a) y (c). En papel no hay razón para que pierda en ninguna de las dos. Ver D1.

### 6.5 Tabla de desenlaces (serie; el bloque serie + réplica toma el menor; NO SE LEE manda)

> Nota: `hab` literal no decide ningún veredicto; el control de MC es `HABNC`. Ver "Decisiones del coordinador" al final (DC1).

| MA | MB | MC | XA y XB | controles | veredicto |
|---|---|---|---|---|---|
| sí | sí | sí | sí | `azar` pierde MB y XB | **FUNCIONA**: K vale por lo que habilita y paga. Si `hab` empata en todo, el vocabulario se limita a "crédito temporal con competencia"; no se dice "según su estado" |
| sí | sí | sí | no | `azar` pierde MB | **HAY ALGO MODESTO**: el mecanismo se arma y no paga en cruce (techo del mundo o limpieza) |
| sí | sí | no | cualquiera | — | **HAY ALGO MODESTO (hábito)**: apetito aprendido por K que no responde a la devaluación |
| no | sí | cualquiera | cualquiera | — | **NO**: apetito por K sin orden temporal |
| cualquiera | no | cualquiera | no | — | **NO**: el crédito no llega |
| cualquiera | no | cualquiera | sí | — | **NO (gana sin llave: instrumento)**; se audita la limpieza con el brazo `paso` |
| cualquiera | `azar ≥ plan` | cualquiera | cualquiera | `azar` no pierde | **NO**: el destino del crédito no importa |
| sí | sí | sí | XA sí, XB no | `azar` cruza igual | **HAY ALGO MODESTO**: paga morder K, no saber cuál |
| — | — | — | — | falla V1–V5 | **NO SE LEE** |

EN EL UMBRAL: pareado a ±1 de 13, suma a ±1 de 10, `C` a ±0.1, `caida` a ±0.05.

### 6.6 Predicciones firmadas (mías, antes de cualquier dato; rangos anchos porque no hay humo)

| # | predicción | rango | p |
|---|---|---|---|
| Q1 | `hab_K` mediano en `plan` (establecidos, sin devaluación) | [0.15, 0.9] | 0.60 |
| Q2 | `hab_K` de `azar` < 0.5 × el de `plan` | | 0.65 |
| Q3 | \|`hab_A`\| y \|`hab_C`\| en `plan` < 0.5 × `hab_K` (la competencia los bloquea) | | 0.55 |
| Q4 | MA | | 0.45 |
| Q5 | MB (con el umbral fijado por la sonda) | | 0.45 |
| Q6 | MC por cuartos | | 0.50 |
| Q7 | `caida_2v ≥ 0.5` | | 0.15 |
| Q8 | `hab` (literal) empata con `plan` en MA y MC (diferencia < 0.15 en `C_n` y en `caida`) | | 0.70 |
| Q9 | XA | | 0.30 |
| Q10 | XB | | 0.25 |
| Q11 | `plan` no pela el mundo: mundo A+C ≥ 0.9 × el de `lug` | | 0.70 |
| V | FUNCIONA / MODESTO / NO / NO SE LEE | | 0.15 / 0.35 / 0.40 / 0.10 |

Predicción ya refutada en papel: la de la ficha ("hábito debe perder en (a) y (c)") para el brazo literal.

---

## 7. Parámetros que dependen de la sonda

No leí resultados de la sonda. Leí `sondas\mundo_plus.py` y `sondas\PREREGISTRO_sondas.md` como código y diseño, para conocer las perillas.

| marcador | regla para fijarlo |
|---|---|
| `PENDIENTE_SONDA: aborto` | si en ningún mundo sondeado se cumple (piso con establecidos ≥ 12/18) Y (cota dura − piso ≥ +4 cruces de 18) Y (ganancia efectiva cota/piso ≥ 1.10), **no se construye** (regla de `PREREGISTRO_sondas.md:20-21`). Si se cumple con la cota `regalo` pero el oráculo `techo` − piso < +2, se construye sólo hasta el humo y XA/XB dejan de ser puerta (el mundo paga pero nadie puede cobrarlo) |
| `PENDIENTE_SONDA: plus` | el `plus` del mundo que dio ESPACIO SÍ; si varios, el menor |
| `PENDIENTE_SONDA: extra_sin` | el del mismo mundo (None si el espacio se abrió sin bajarlo). Aviso: si es < 0.8, V2 se lee en ese mundo, no en P1b |
| `PENDIENTE_SONDA: p_x` | el menor de {0.03, 0.06, 0.10} que cumpla: piso vivo, mundo A+C del piso ≥ 0.85 × el de P1b sin K, y `frac_llave` del oráculo ≥ 0.30. Si la sonda sólo corrió 0.03, se usa 0.03 y `umbral_b` se ajusta |
| `PENDIENTE_SONDA: t_viaje` | mediana, en el brazo oráculo, de (primer bocado A/C dentro de la misma vida − mordida de K), contando sólo las que llegan en ≤ 600 pasos. **La sonda no lo escribe** (`mundo_plus.py:70-75` no guarda tiempos): lo mide el humo 0 de esta ficha con `sondas\carros\O1_LUGAR_ORAC.py` en `mundo_p9` con `eventos = 1` |
| `PENDIENTE_SONDA: d_plus` | `2 × t_viaje`, redondeado hacia arriba a múltiplo de 10, con piso 60 y techo 600. Provisional 200 (distancia media en un anillo de 360 = 90 pasos) |
| `PENDIENTE_SONDA: tau` | `PL_TAU = d_plus` |
| `PENDIENTE_SONDA: frac_llave_orac` y `frac_llave_piso` | del oráculo y del piso con el `d_plus` final (humo 0 si la sonda usó otra ventana) |
| `PENDIENTE_SONDA: umbral_b` | `min(0.6, 0.75 × frac_llave_orac)`; si `frac_llave_orac − frac_llave_piso < 0.20`, MB no es puerta en ese mundo y hay que subir p_x antes de construir |
| `PENDIENTE_SONDA: techo_contraste` | `N/E` del oráculo en el humo 0; decide cuál de las dos formas de MA aplica (≥ 3.0 → `C ≥ 2.0`) |
| `PENDIENTE_SONDA: azar_sonda` | si el brazo azar de la sonda (K por moneda, sin estado) ≥ techo en cruce, el mundo no exige secuencia: XA y XB dejan de ser puerta y el peldaño se decide sólo por MA, MB y MC (ya previsto en `PREREGISTRO_sondas.md:28-29`) |
| `PENDIENTE_SONDA: frac_K_dentro` | fracción de K mordidas dentro del oasis en el oráculo. Si > 0.5, la "secuencia" es morder K y comer en el mismo sitio; se declara y se considera el ancla de `sondas\mundo_ret.py` (la letra nueva no nace dentro), que NO leí |
| `PENDIENTE_SONDA: sha_mundo_plus` | sha de `mundo_plus.py` cuando la sesión de sondas lo cierre |

---

## 8. Plan de humos y serie

Tiempos ya medidos en el repo (no estimo otros): T 100k, un proceso: `lug` 107–148 s, `o1` 59–68 s (`PREREGISTRO_p1.md:127`); humo de 6 corridas a T 30k ≈ 8 min; exploración de 6 × T 100k ≈ 20 min; serie 20 × 4 × T 100k ≈ 4 h de CPU, 2 h con pool 2 (`ESCALERA.md:61`). El costo del registro de eventos y de las trazas no está medido: lo dice el humo 0.

### 8.1 Antes de cualquier número

> Nota: nada se construye ni se fija hasta que llegue la sonda; ver "Decisiones del coordinador" al final (regla general).
1. `construye_p9f3.py --verifica` y `identidad_p9f3.py` (I1–I14). Se pega la salida.
2. Sólo si pasa todo se corre un humo.

### 8.2 Humos de un proceso (≤ 6 corridas, ≤ 200 000 pasos; cada uno escribe su JSON y una línea en `BITACORA.md`)

| humo | corridas | para qué | se sigue si |
|---|---|---|---|
| 0 instrumento | 2 semillas × {oráculo, `lug`}, T 30k, `eventos = 1` | fijar `t_viaje`, `d_plus`, `tau`, `frac_llave_orac`, `techo_contraste`; tamaño del JSON; segundos por corrida | el JSON se escribe y `techo` ≥ 1.5 |
| 1 mecanismo | 1 semilla × {`plan`, `hab`, `azar`, `lug`, `paso`, `HABNC`}, T 30k | ¿`hab_K` pasa `PL_MIN`? ¿`p3_val` > 0? ¿`plan` muerde más K que `paso`? mundo A+C de `paso` contra `lug` | `hab_K` > 0.05 en algún linaje establecido de `plan` |
| 2 exploración | 2 semillas × {`plan`, `azar`, `lug`}, T 100k | MA, MB, cruce, en pequeño | `C` de `plan` > 1 y `frac_llave` de `plan` > la de `azar` |
| 3 devaluación | 2 semillas × {`plan`, `hab`, `HABNC`}, T 100k, `t_dev = 50 000` | `caida` por cuartos; ¿`hab` y `HABNC` se separan? | — |

Regla de parada: tres humos sin señal de mecanismo (`hab_K` no pasa `PL_MIN`, o `C ≤ 1`) y la ficha se cierra en ráfaga, como el P9 viejo (`BITACORA.md:39`). Los humos pueden mover `PL_ETA` y `p_x`; cada cambio se declara en el preregistro como historia.

### 8.3 Serie (la corre el coordinador; el creador no usa `Pool`)
- **Serie principal:** 20 semillas × 4 brazos (`plan`, `hab`, `azar`, `lug`), T 100k, sin devaluación: 80 corridas, ≈ 4 h de CPU con el costo de P1. Lee MA, MB, XA, XB.
- **Bloque de devaluación:** 10 semillas × 2 brazos (`plan` y el hábito que decida D1; **decidido: `HABNC`, ver "Decisiones del coordinador" al final, DC1**), T 100k, `t_dev = 50 000`: 20 corridas, ≈ 1 h de CPU con el mismo costo. Lee MC.
- **Réplica:** las dos partes en semillas nuevas, sólo si la serie da FUNCIONA, MODESTO o NO en el umbral (regla de `PREREGISTRO_p1.md:86`); mismo sha del runner.
- Antes de la serie: `PREREGISTRO_p9f3.md` con los marcadores resueltos y auditoría.

### 8.4 Semillas (grep de hoy: `74[56]\d\d\d` no aparece en ningún `.py` ni `.md` de `PROYECTOS\JUACO`; el constructor repite el grep)
serie 745001–745020 · réplica 745101–745120 · devaluación 745201–745210 · réplica de devaluación 745301–745310 · exploración 745801–745806 · humos 745900–745919 · arnés 745950–745959 · rng del barajado `[746000, semilla]`.

### 8.5 Las cuatro trampas
- **Canal simétrico:** no hay canal; O1 no lee ni escribe la pizarra.
- **Acierto sin balancear:** MA es una razón contra el barajado dentro de cada vida, con techo reportado; MB se lee contra `azar`, no sola.
- **Mundo que se come la comida:** K sin comer se acumula y tapa (`BITACORA.md:34`); morder K de paso limpia. Se reporta mundo A+C por brazo, el brazo `paso` en humo, y XB (misma limpieza) decide el contenido.
- **Sitios fijos:** el oasis se sortea por semilla (`mundo_escalera.py:95-96`); semillas nuevas.

---

## 9. Riesgos, dudas y lo no verificado

### Dudas para el director o el coordinador

> Nota: D1–D5 están RESUELTAS; ver "Decisiones del coordinador" al final. Donde este texto diga otra cosa (p. ej. "por defecto corre el literal"), manda esa sección.
- **D1 (la más importante). ¿Qué es "hábito"?** El brazo literal (sin las dos compuertas) aprende con la misma regla que `plan`; en papel empata en (a) y (c). Si se quiere un control que pueda perder en (c), el hábito debe ser además sin competencia (`O1_LUGAR_P3_HABNC`: el error de la traza no resta el bono de lugar, así que tras la devaluación el extra del oasis sigue alimentando a K). Por defecto corre el literal, como dice el encargo; cambiarlo es una línea en el diccionario de brazos del runner. Recomiendo `HABNC` en el bloque de devaluación y el literal en la serie principal.
- **D2. Devaluación en bloque aparte** (20 corridas más) en vez de dentro de la serie. Lo cerré así para no diluir el cruce. Si el director prefiere una sola serie con `t_dev = T/2`, XA y XB deben leerse sólo en la primera mitad, y el juez no lo hace hoy.
- **D3. La mordida de paso** (`PL_PASO`) no estaba en la ficha. Sin ella la ficha no arranca. Cambia el mundo (limpia K).
- **D4. Umbrales (b) y (c)** del encargo cambiados por las reglas de 6.2 y 6.3.
- **D5. K dentro del oasis.** En el mundo de la sonda la mitad de lo repuesto nace dentro (`mundo_escalera.py:121-124`, dens 0.5), K incluida. Mantengo el mundo de la sonda tal cual para que piso y techo valgan; si `frac_K_dentro` > 0.5 el orden "ir por la llave y volver" casi no se ejerce.

### Riesgos del mecanismo
- **Morder una letra neutra dentro del oasis baja la memoria de lugar.** Con dS = (0, 0) y v = (0, 0), `_lg_apr` mueve el bin hacia 0 con peso 0.5 (`PLAN.py:224`). Ya pasa hoy en `lug` con B y D; con K buscada a propósito pasa más. Puede hacer que `plan` olvide el oasis. El humo 1 lo mide (bins con bono, razón de pasos).
- **`hab` de A y C.** La traza de A casi siempre está viva al comer dentro; la competencia debería dejar `hab_A` cerca de 0 (Q3). Si no, A se valora de más y el cruce cambia por una vía que no es la llave.
- **La media por letra mezcla dentro y fuera** (`PLAN.py:58-60, 160`): v(A) queda entre lo pobre y lo rico, y el bono de lugar fuera queda negativo. Es de P1; el error compartido lo hereda.
- **El lugar aprende rápido (0.5) y K lento (0.3·e):** en rachas de bocados con llave el lugar absorbe el plus y K recibe poco. `hab_K` puede quedar bajo aunque positivo.
- **Refundación:** en linajes no establecidos `hab` se borra en cada fundador; las medidas los excluyen, pero el cruce no.
- **`azar` con fuga** de ~20 % hacia K.
- **Tamaño del JSON** con eventos sin tope: no medido.

### No verificado
- No se corrió nada: ni arnés, ni humo. Las líneas citadas son de `O1_LUGAR_PLAN.py`. Por grep sobre `carros\O1_LUGAR.py` comprobé que las anclas 4, 8 y 10 aparecen una vez (`:97`, `:211`, `:166`); las otras diez son las que `construye_c.py` ya usa con su chequeo de unicidad. No abrí `construye_p1.py`.
- La identidad bit a bit del ancla 8 (`_lg_apr` en tres líneas) es un argumento de papel.
- No leí `corre_v143.tarea`, `corre_p1.py` (`fila`, `verifica`, `identidad_corta`), `juez.py`, `identidad_c.py`, `sondas\corre_s1.py`, `sondas\mundo_ret.py` ni el cuerpo completo de `sondas\construye_orac.py` (sólo un grep).
- No verifiqué el valor de `costo`, `rep_umbral` ni `dote`; la tasa de bocados por cuerpo que uso en 6.3 es una estimación de orden de magnitud, no un dato.
- No sé si `revisa_carro` acepta el uso de `self.rng` (el rng del cuerpo, `O1_LUGAR.py:43`) en `azar`.
- No leí `CLAUDE.md`, `registro/PLAN.md` ni `registro/EQUIPO.md` del bundle en esta sesión (el encargo acotó la lectura al worktree `organelos` y a la carpeta de investigación).
- Los tiempos de 8 son los de P1; el módulo nuevo y los eventos no están medidos.

---

## Decisiones del coordinador (1-oct-2026)

Esta sección manda sobre el cuerpo donde lo contradiga. No se renumeró ni se reordenó nada.

- **Regla general.** Nada se construye ni se fija hasta que llegue la sonda de piso/techo. Si oráculo − piso < +4 (cruces de 18), **P9 se libera sin construir**. Hasta entonces este documento es especificación en espera: ningún archivo en `E\p9f3\`, ningún sha, ningún umbral fijado.
- **DC1 (D1).** El control del bloque de devaluación es **`HABNC`** (`O1_LUGAR_P3_HABNC`: sin compuertas de estado y sin competencia). Es el control que puede perder en MC. El "hábito" literal (`O1_LUGAR_P3_HAB`) queda como brazo **DESCRIPTIVO** en la serie principal: se corre y se reporta, pero no entra en ninguna puerta ni en la tabla de desenlaces.
  **En papel, el hábito literal empata con `plan` en (a) y en (c).** Por qué: (i) aprende con exactamente la misma regla delta, la misma traza y la misma competencia con el lugar (`PL_COMPITE = 1`); sólo se salta dos `if` al USAR el valor. (ii) En (a), las compuertas no cambian el orden K → bocado: quien muerde K con hambre y cerca del oasis come después, lleve o no la llave; las K "redundantes" (con llave en mano) también van seguidas de bocado. (iii) En (c), tras la devaluación ambos reciben el mismo error negativo en cada bocado con traza viva y desaprenden al mismo ritmo. La única diferencia observable (K mordidas con llave en mano ≈ 0 en `plan`) es cierta por construcción y no es evidencia. Predicción Q8 (p 0.70) se mantiene.
- **DC2 (D2).** La devaluación va en **bloque aparte** (10 semillas × {`plan`, `HABNC`}, `t_dev = T/2`), como en la sec. 8.3. La serie principal no lleva devaluación.
- **DC3 (D3).** Se acepta **`PL_PASO`** (una mordida de paso por vida a letras neutras) en los tres brazos con módulo. **`plan > azar` (XB y MB) decide el contenido**; `plan > lug` (XA) incluye el efecto de limpiar K y no lo aísla.
- **DC4 (D4).** Los umbrales nuevos quedan **PROVISIONALES hasta la auditoría**: (a) MA `C ≥ 2.0` si `techo ≥ 3.0`, si no `C_n ≥ 0.5` — PROVISIONAL; (b) MB `umbral_b = min(0.6, 0.75 × frac_llave_orac)` — PROVISIONAL; (c) MC `caida ≥ 0.50` por cuartos (Q4 contra Q2) — PROVISIONAL. Los del encargo original ((a) ≥ 2.0 a secas, (b) ≥ 0.6, (c) ≥ 50 % en dos vidas) siguen escritos en la sec. 6.3 con mi juicio de papel; el auditor decide cuáles quedan. Ninguno se fija antes de la sonda.
- **DC5 (D5).** Se mantiene el **mundo de la sonda** tal cual (K también nace dentro del oasis, dens 0.5). `frac_K_dentro` se reporta; no se usa el ancla de `mundo_ret`.

Consecuencia sobre los brazos: serie principal = `plan`, `azar`, `lug` (con puertas) + `hab` literal (descriptivo); bloque de devaluación = `plan` + `HABNC`. La fila de la tabla 6.5 "sí/sí/no → MODESTO (hábito)" se lee con `HABNC` como referencia de MC.
