# DISEÑO — sala 2, ángulo VIVIR: **v16 = v14.1 + población** (muerte de verdad, herencia del código con su valor, reproducción pagada, selección sin GA)

**Creador de la sala 2, 18 sep 2026, ~09:55.** Misión primero: llegar a la AGI por este camino — un organismo mínimo con
reglas locales (sin backprop en el runtime) que aprende, desaprende, generaliza, **sobrevive y se reproduce**, con evidencia
preregistrada. Primero la frontera; segundo, que viva. Este archivo es un DISEÑO con preregistro propuesto; **nada de lo de
abajo está construido ni medido con `Pool`**. La decisión de construirlo y correrlo es del coordinador; la de tronco, del director.

**Reglas cumplidas.** No edité ningún archivo del repo; este es el único archivo que creé en `registro/investigacion/sala2/`
(la carpeta ya existía con los cuatro `DIAG_*.md` de la sala). No ejecuté `Pool` (hay uno vivo: `corre_vivo_rep2.py --desde 261`).
**Corrí exactamente UNA corrida de un proceso, T = 50 000** (§0.2, declarada con sus números; script y JSON en mi scratchpad,
no en `datos/`). Sin commit. Fuentes leídas en el orden del encargo: `CLAUDE.md` (día 7), `PLAN.md`, `HANDOFF.md` §13 y
§15.7–15.8, el registro desde ERR-35 hasta el final (incluida la entrada de v15e y ERR-43 escritas mientras leía),
`ENJAMBRE_xor_20260918.md`, `PUENTE_creacion.md` (A12–A16, B-5), `PREREGISTRO_v15e.md`, `PREREGISTRO_mundo_vivo.md`,
`PREREGISTRO_reproduccion.md` y `_2.md`, `organismo/organismo_v14.py` entero, `organismo_vivo_rep.py` entero, `EQUIPO.md`,
`DISENO_mundo_vivo_20260918.md`, el bloque H de la Etapa 4 (registro), `dia1_exploracion/poblacion2.py`, y los cuatro
diagnósticos de la sala (`DIAG_mundo.md` §3 propone el mismo bloque: digo en §2.8 dónde coincido y dónde no, y por qué).

---

## 0. Si fuera mi creación: cómo le daría vida (respuesta al director, en diez líneas)

1. **Que muera de verdad.** Hoy la muerte es `E=.6; pos=azar` con la memoria intacta (`organismo_v14.py`, línea `if E<=0:`):
   un cuerpo inmortal con reset. Sin muerte que borre, "sobrevive" es un contador y "se reproduce" no puede ser resultado.
2. **Que nazca de verdad.** Cuando un cuerpo lleva 500 pasos saciado (la ventana ya medida, `rep_X=500, rep_umbral=1.0`),
   **paga** media reserva (`dote = 0.5` de E y de Ag) y nace un segundo cuerpo **en el mismo anillo**, en su sitio, con
   0.5/0.5. Nada es gratis: lo que recibe el hijo lo pierde el padre (ERR-40 nació de un renacer regalado).
3. **Que herede el código CON su valor.** El hijo recibe `KW`, `activa`, `Wp/Wn` (token y lo que vale), la lineal `Wps/Wns`
   (el vector), las patas `Wl`, `ncod` (la evidencia por token) y el árbol madre→hija de las celdas. Los controles
   desmontan la herencia pieza a pieza (sólo el vector, sólo el token, barajada, un escalar, nada).
4. **Que compitan por la misma comida** (mismo anillo `L = 40`, `nobj = 4`: el mundo del tronco, sin tocar). La selección es
   la física: quien no come muere y se lleva su memoria; quien está saciado 500 pasos se duplica. **Sin función de aptitud,
   sin generaciones, sin torneo, sin cruce**: ni GA global ni backprop.
5. **Que el propósito sea un gen.** La lectura pesimista saciado (`CUELLO_MIN`, que "sobra" como órgano diseñado) pasa a ser un
   rasgo heredable continuo `g_pes ∈ [0, 1]` con mutación al nacer. Si la selección lo sube, el propósito **se mide** como
   frecuencia alélica y como supervivencia del linaje; si no, se dice.
6. **Medida de éxito ligada a la supervivencia por construcción:** tiempo hasta la extinción del linaje, cuerpos vivos a T,
   hijos que llegan vivos a 2 000 pasos. Un muerto no cuenta, no reproduce y no financia nada.
7. **Apagado ≡ v14.1 bit a bit**, y en el mundo vivo ≡ `organismo_vivo_rep` bit a bit, con arnés (I1–I7, §2.7).
8. **Lo que sale de la frontera y se puede medir:** un linaje que vive más que cualquier cuerpo (punto 14 del brief, criterio
   de emergencia, literal), qué memoria es portable entre cuerpos (vector contra token: la pregunta "grafo o vector" del
   director medida en población), selección de un rasgo sin GA, y desaprender a escala de linaje.
9. **Lo que NO promete:** no toca XOR, ni la construcción del rasgo, ni la capacidad; el examen del tronco no lo mide (como B-5).
10. **Coste:** un constructor por anclas (dos archivos), un arnés, un runner; ~340 corridas de ≤ 50 s ≈ 10–12 min de `Pool(14)`
    por serie; réplica igual.

### 0.2 La única corrida (declarada): el mundo no se arregla haciéndolo más rico

`organismo_vivo_rep2.py` (96feb4918dc5d694), CUELLO_MIN (el cuerpo que la población debería seleccionar), semilla 1,
**T = 50 000, un proceso, `nobj = 12`** (tres veces el tronco), todo lo demás como el bloque 2 de reproducción. Resultado:
**descendientes 56, muertes 71** [31 energía, 40 agua] (a `nobj = 4` y T = 100 000 la misma semilla da 67 / 64: **el anillo rico
mata el doble por unidad de tiempo**), `r = −15`, **vida mediana 582 pasos** (= 0.6/0.001: la mitad de los renacidos no
encuentran comida Y agua antes de agotar el regalo), vida máxima 4 571, exposiciones A/B/C/D **452 / 6 487 / 489 / 4 282** (el
anillo está lleno de lo que nadie come: trampa 3), pasos viables 38 552 / 50 000, tabla 2 × 4 exacta, 35 celdas, 5 divisiones.
Consecuencias para este diseño: (a) el mundo de la población es **el del tronco** (`nobj = 4`), no uno más rico; (b) la
mortalidad infantil es una **cantidad a medir**, no un supuesto; (c) un mundo B más grande (no más denso) queda predeclarado
como rama de contingencia (§4.6), nunca como recalibración.

---

## 1. Qué bloquea (con evidencia del registro)

| # | bloqueo | evidencia | consecuencia |
|---|---|---|---|
| B1 | **Muerte sin olvido.** El único cuerpo renace con toda su memoria; la muerte regala 600 pasos y un sitio nuevo | `organismo_v14.py` línea `if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))`; ERR-40 ("el renacer regala 600 pasos de drenaje y un escape del anillo atascado"); humo rep2: el regalo financia el 65–77 % de las ventanas de ESCALAR | ninguna medida sobre un inmortal mide viabilidad; la selección no tiene sobre qué actuar |
| B2 | **Nada nace.** Dos medidas de reproducción, ninguna instancia un descendiente | P-R1 se tiró (09:16; A₁₂ VIVO > ESCALAR 0.007); `r = desc − muertes` es contabilidad elegida mirando el dato (`PREREGISTRO_reproduccion_2.md` §5) y su §2 dice "qué se hereda: NADA"; el diseño del mundo vivo §7 y `PREREGISTRO_reproduccion.md` §2 aplazan la población: "exige `Pool` y una hipótesis propia" | ésta es la hipótesis propia; y la población cabe en **un proceso** (§2.1): `Pool` sólo reparte semillas |
| B3 | **El propósito es una regla escrita a mano.** La tercera necesidad sobra (P-R5b: CUELLO_MIN 65.5 > 55, A₁₂ 0.146); CUELLO_MIN es una lectura que el diseñador puso | REGISTRO 09:16; `PREREGISTRO_reproduccion_2.md` §2 | "propósito" sólo significa algo si un rasgo puede **perderse o conservarse** por lo que cuesta vivir |
| B4 | **El mundo se come la comida y se llena de lo rechazado** (trampa 3) y castiga la riqueza | exposiciones B 5 253 contra A 831 (mini vivo); mi corrida: `nobj = 12` → 71 muertes en 50 000 pasos | la selección en este mundo será dura; un mundo más rico no la afloja: la afloja el tamaño, no la densidad |
| B5 | **Herencia medida sólo en un cuerpo y una vez** (Etapa 4, bloque H): heredar el valor ahorra el 80 % del veneno inicial (6.5 contra 30.5, 20/20); en mundo invertido la desventaja va en la dirección predicha pero no consistente (H4 12/20) | REGISTRO Etapa 4 (`etapa4_v9_20260916_170519`) | hay un precedente de herencia útil y uno de herencia que estorba: los dos son predicciones de población, no resultados de población |
| B6 | **Ser dos cuesta** (+34 % de muertes en N1, día 4) y el único código de población es del día 1 (`poblacion2.py`: cuatro "grupos" por constantes, `KW` común "a la especie", sin herencia, sin resultado en el registro) | CLAUDE.md día 4; `experimentos/dia1_exploracion/poblacion2.py` | no hay instrumento de población con identidad con el tronco |
| B7 | **Un proceso = un cuerpo.** El bucle `for t in range(T)` de `run()` lleva todo el estado en locales; los runners paralelizan semillas | `organismo_v14.py`; `EQUIPO.md` regla 3 | la población tiene que vivir DENTRO de `run()` sin reescribirlo: §2.1 |

Lo que **no** bloquea y no toco: el nivel 3 (XOR: cerrado por ERR-35; prior de pares), la construcción del rasgo (cuello real
de la misión, creador A), la capacidad. Este ángulo no los mueve y no lo finge.

---

## 2. Mecanismo: v16 por anclas sobre `organismo/organismo_v14.py` (feefc88b1fd8d434)

### 2.1 Arquitectura en dos líneas
1. **El cuerpo es el `run()` de v14.1 convertido en generador** (`_vida`): el mismo texto, con un `yield` al final de cada
   paso **sólo si `pob`**, un `break` en la muerte **sólo si `pob`**, y un bloque de herencia **sólo si `_estado`**. Con
   `pob = 0`, un envoltorio `run()` agota el generador y devuelve su dict: **las mismas operaciones, en el mismo orden, con
   el mismo rng** (identidad I1).
2. **El planificador `_run_pob`** crea el fundador, y en cada paso avanza a todos los cuerpos vivos **en orden al azar**
   (rng del mundo, `seed + 600000`, que no toca el del fundador), sobre un **único dict de objetos compartido** (`_mundo`).
   Un cuerpo que pide nacimiento entrega una copia de su estado; el planificador aplica el modo de herencia, muta los
   genes con el rng del hijo (`seed + 800000 + k`) y lo mete al mundo en el paso siguiente. Un cuerpo que muere sale con su
   dict final; si no queda ninguno, `t_ext = t` y la corrida termina.

### 2.2 Anclas literales (copiadas de `organismo_v14.py`; en `organismo_vivo_rep.py` las equivalentes, §2.8)

| # | ancla (texto literal, aparece 1 vez) | inserción / sustitución | apagado (`pob=0`) |
|---|---|---|---|
| A1 | `def run(seed,T=100000,` … `puerta_pat=5,pat_shuf=0,pat_min=1):` | `def _vida(` … `pat_min=1,pob=0,rep_X=500,rep_umbral=1.0,dote=0.5,genes=0,g0=0.5,gen_activo=1,sd_mut=0.1,_mundo=None,_meta=None,_rng=None,_estado=None,_pos0=None,_id=0,_t0=0):` | perillas nuevas con valor inerte |
| A2 | `    rng=np.random.default_rng(seed)` | `    rng=np.random.default_rng(seed) if _rng is None else _rng` | `_rng` es `None` |
| A3 | `    while not cond(): KW[objetivo_AB:NK]=rng.uniform(0,1,(NK-objetivo_AB,6))` | `    while ('KW' not in (_estado or {})) and not cond(): KW[...]=rng.uniform(...)` (un hijo con `KW` heredado no vuelve a sortear el código: las divisiones ya rompieron `A∩B=0`) | `_estado` es `None` → misma condición |
| A4 | `    Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA…` | + `    madre=np.full(NKMAX,-1); _g=dict(g_pes=g0,g_nul=g0); _gv=0; _evento=None; _muerto=None   # POB: arbol de celdas (solo lectura), genes, ventana` | estado nuevo que nadie lee |
| A5 | `    pos=0; E=1.0; objs={}; val={'A':'comida','B':'veneno'}` | antes: `    if _estado is not None: Wl=_estado.get('Wl',Wl); KW=_estado.get('KW',KW); activa=_estado.get('activa',activa); Wp=_estado.get('Wp',Wp); Wn=_estado.get('Wn',Wn); err=…; mu=…; Wps=…; Wns=…; mup=…; mun=…; zp=…; zn=…; madre=…; ncod=dict(_estado.get('ncod',{})); _ord=list(_estado.get('_ord',[])); _g=dict(_estado.get('genes',_g))` · la línea: `    pos=(0 if _pos0 is None else _pos0); E=(1.0 if _t0==0 else dote); objs=({} if _mundo is None else _mundo); val={'A':'comida','B':'veneno'}` | `_estado`/`_pos0`/`_mundo` `None`, `_t0=0` |
| A6 | `                                    j=int(np.where(~activa)[0][0]); activa[j]=True; KW[j]=kj` | + `; madre[j]=c   # G-1: arista madre->hija` (y lo mismo en la rama v10 `elif err[c]>theta`) | un entero por celda; ningún número cambia |
| A7 | `        E-=costo` | + `        if pob:   # POB: ventana de viabilidad -> nacimiento pagado` `            _gv=_gv+1 if E>=rep_umbral else 0` `            if _gv>=rep_X: _gv=0; E-=dote; _evento=dict(t=t,pos=pos,Wl=Wl.copy(),KW=KW.copy(),activa=activa.copy(),Wp=Wp.copy(),Wn=Wn.copy(),err=err.copy(),mu=mu.copy(),Wps=Wps.copy(),Wns=Wns.copy(),mup=mup.copy(),mun=mun.copy(),zp=zp.copy(),zn=zn.copy(),madre=madre.copy(),ncod=dict(ncod),_ord=list(_ord),genes=dict(_g))` | rama muerta |
| A8 | `        if rng.random()<.003 and objs:` | `        if (not pob or _meta['stir']==_id) and rng.random()<.003 and objs:` (el olvido de objetos lo ejecuta UN solo cuerpo —el más viejo vivo—, si no el mundo se renovaría N veces más rápido con N cuerpos: artefacto) | `not pob` es `True`: se evalúa `rng.random()` igual que hoy |
| A9 | `        if E<=0: deaths+=1; E=.6; pos=int(rng.integers(L))` | antes: `        if pob and E<=0: deaths+=1; _muerto=_t0+t; break   # POB: MUERTE DE VERDAD: el cuerpo sale con su memoria` | rama muerta |
| A10 | `        if log_cada and t%log_cada==0: log.append(…)` | + `        if pob: _ev0=_evento; _evento=None; yield (t,_ev0)   # POB: el planificador avanza a los demas` | nunca cede: el generador corre entero |
| A11 | `    return dict(sobre=sobre,` … `Wns=[round(float(x),3) for x in Wns])` | `    _fin=dict(…)` + `    if pob: _fin.update(id=_id,t_nac=_t0,t_muerte=_muerto,genes=dict(_g),arbol=madre[activa].tolist(),profundidad=_prof(madre,activa))` + `    return _fin` | claves viejas idénticas; ninguna nueva |
| A12 | (final del archivo) | `def run(seed,**kw):` `    if not kw.get('pob',0):` `        g=_vida(seed,**kw)` `        try:` `            while True: next(g)` `        except StopIteration as e: return e.value` `    return _run_pob(seed,**kw)` + `def _hereda(ev,modo,olvido,rng_h,sd_mut,genes)` + `def _run_pob(...)` (§2.3) | `run(seed)` devuelve el dict de v14.1 |

**Detalle que importa para la identidad:** una función con `yield` es generador entera; por eso el `return dict(...)` del
tronco pasa a ser el `value` de `StopIteration` y el envoltorio lo devuelve. Ningún cálculo se mueve de sitio, ninguna
llamada al rng cambia de orden. Identidad esperable: **exacta** (no aproximada), y se exige en el arnés.

### 2.3 El planificador `_run_pob` (pseudocódigo; todo nuevo, detrás de `pob=1`)

```
def _run_pob(seed, T=100000, hereda='todo', olvido_hijo=0.0, genes=0, gen_activo=1, sd_mut=0.1, g0=0.5,
             x_viab=2000, n_abort=16, invertir_en=None, **kw):
    mundo = {}; meta = {'stir': 0}; rng_m = np.random.default_rng(seed + 600000)     # sólo orden de los cuerpos por paso
    nuevo = lambda k, t0, est, pos0, rng_h: _vida(seed, T=T - t0, pob=1, _mundo=mundo, _meta=meta, _rng=rng_h, _estado=est,
                 _pos0=pos0, _id=k, _t0=t0, genes=genes, g0=g0, gen_activo=gen_activo,
                 invertir_en=(None if invertir_en is None else max(0, invertir_en - t0)), **kw)
    cuerpos = [dict(id=0, g=nuevo(0, 0, None, None, None), madre=-1, t_nac=0, hijos=0)]   # el fundador usa el rng del tronco
    fin = []; nac = 0; espera = []; arbol = [(0, -1, 0, None)]; g_traj = []; t_ext = None
    for t in range(T):
        if not cuerpos: t_ext = t; break
        meta['stir'] = min(c['id'] for c in cuerpos)                        # el más viejo vivo renueva el mundo
        for i in rng_m.permutation(len(cuerpos)):                           # orden al azar: sin ventaja por índice
            c = cuerpos[i]
            try: _, ev = next(c['g'])
            except StopIteration as e: c['fin'] = e.value; c['muerto'] = True; fin.append(c); continue
            if ev is not None:                                              # nacimiento pedido (el padre YA pagó la dote)
                nac += 1; k = nac; rng_h = np.random.default_rng(seed + 800000 + k)
                est = _hereda(ev, hereda, olvido_hijo, rng_h, sd_mut, genes)   # None en BLANCO; genes mutados con rng_h
                espera.append(dict(id=k, g=nuevo(k, t + 1, est, ev['pos'], rng_h), madre=c['id'], t_nac=t + 1, hijos=0))
                c['hijos'] += 1; arbol.append((k, c['id'], t + 1, None))
        cuerpos = [c for c in cuerpos if not c.get('muerto')] + espera; espera = []
        if len(cuerpos) > n_abort: aborto = t; break                        # límite del INSTRUMENTO: si muerde, se reporta y el mundo es demasiado rico
        if t % 5000 == 0: g_traj.append((t, len(cuerpos), media(g_pes), media(g_nul), frac_veneno(mundo)))
    # al llegar a T todos los vivos devuelven su dict (t_muerte=None): se recogen igual
    viables = sum(1 for c in fin + cuerpos if c['t_nac'] > 0 and (edad(c) >= x_viab))
    return dict(pob=1, t_ext=(T if t_ext is None else t_ext), pob_T=len(cuerpos), nac=nac, viables=viables,
                mort_inf=(None if nac == 0 else 1 - viables / nac), gen_max=profundidad(arbol), vidas=[...],
                arbol=arbol, g_traj=g_traj, fundador_sin_hijos=(nac == 0), aborto=aborto, cuerpos=[c['fin'] for c in ...])
```

`_hereda(ev, modo, …)` devuelve el `_estado` del hijo (§2.5); `'nada'` devuelve `None` y el hijo se inicializa como un
tronco nuevo con su propio rng (`Wl`, `KW` al azar, `W = 0`), en la posición del padre y con `E = dote`.

### 2.4 Estado y constantes nuevas (todas fijadas por argumento, ninguna por barrido)

| nombre | valor | de dónde sale |
|---|---|---|
| `rep_X`, `rep_umbral` | 500, 1.0 | la ventana del bloque 1 de reproducción (medida en 221–240: VIVO 20, CUELLO_MIN 65.5 por 100 000) |
| `dote` | 0.5 (de E; en el mundo vivo también de Ag) | la mitad de la saciedad; conserva la suma: padre ≥ 0.5, hijo 0.5; con `costo = 0.001` el hijo tiene 500 pasos para comer y beber |
| `x_viab` | 2 000 pasos | cuatro ventanas de drenaje del hijo; un hijo que llega ahí comió y bebió por su cuenta |
| `g0`, `sd_mut` | 0.5, 0.1 | fundador a medio camino entre VIVO (0) y CUELLO_MIN (1); paso de mutación de una décima |
| `n_abort` | 16 | límite de cómputo del instrumento (16 × ~5 s por 100 000 pasos); si muerde, se reporta |
| memoria por cuerpo | la de v14.1 + `madre` (90 enteros) + 2 genes | por nacimiento: una copia (~1 200 flotantes) |
| rng | fundador: el del tronco; mundo: `seed+600000`; hijo k: `seed+800000+k` | convención de `v13s`/`organismo_vivo` (`seed+900000`): ninguna línea nueva toca el rng del fundador |

### 2.5 Modos de herencia (`hereda=`; `Wl` —las patas— va en todos salvo BLANCO y PATAS lo lleva solo)

| modo | qué recibe el hijo | qué mide |
|---|---|---|
| `'todo'` **HEREDA** | `Wl, KW, activa, mu, err, mup, mun, zp, zn, madre, Wp, Wn, Wps, Wns, ncod, _ord`; valores × `(1 − olvido_hijo)` | la línea |
| `'lenta'` **SOLO_LENTA** | `Wl, Wps, Wns` (el vector sobre la retina; `KW` nuevo, `W = 0`, `ncod` vacío) | ¿la regla lineal es portable entre cuerpos con códigos distintos? |
| `'rapida'` **SOLO_RAPIDA** | `Wl, KW, activa, mu, madre, Wp, Wn, ncod, _ord` (el token con su valor; `Wps = Wns = 0`) | ¿basta la memoria indexada por token? |
| `'baraja'` **BARAJA** | todo, pero `Wp/Wn` **permutados entre las celdas activas** y `Wps/Wns` **permutados entre píxeles** (rng del hijo) | la misma cantidad de memoria con el contenido roto: el control decisivo |
| `'escalar'` **ESCALAR** | `Wl, KW, activa`; `Wn = media(Wn_padre[activa])` en todas las celdas activas, `Wns = media(Wns_padre)` en los 6 px; `Wp = Wps = 0` | "sabe cuánto miedo, no a qué" |
| `'patas'` **PATAS** | sólo `Wl` | andar sin saber |
| `'nada'` **BLANCO** | nada: un tronco nuevo con su rng | el cuerpo que aprende desde cero y muere antes |

### 2.6 El gen del propósito (sólo en el mundo vivo, sobre `organismo_vivo_rep.py`)

Ancla literal (aparece 1 vez): `            if _cue2: _wt=min(_wt,_vnec(1-_na,PAT[kk],kc))` →
`            if _cue2: _wt=(min(_wt,_vnec(1-_na,PAT[kk],kc)) if not (pob and genes) else (1-_gp)*_wt+_gp*min(_wt,_vnec(1-_na,PAT[kk],kc)))`
con `_gp=(_g['g_pes'] if gen_activo else g0)` calculado en la línea anterior. Lectura: `g_pes = 0` ≡ VIVO (fila activa),
`g_pes = 1` ≡ CUELLO_MIN (mínimo de las dos filas), entre medias una mezcla. `g_nul` se hereda y muta igual y **no lo lee
nadie**: es el control de deriva dentro de la misma corrida. En `GEN_INERTE` (`gen_activo = 0`) los dos genes derivan y la
boca usa `g0` fijo: su conducta es la de `FIJO_05` (identidad I6). Exige `rep_cuello = 2` y `puerta` (como CUELLO_MIN).

### 2.7 Apagado ≡ v14.1 bit a bit: arnés `identidad_pob.py` (un proceso, T = 20 000, semillas 1–3; se entrega con su salida)

| caso | qué compara | debe |
|---|---|---|
| I1 | `organismo_v16v.run(pob=0)` contra `organismo_v14.run` en las **24 configuraciones** del arnés de v15e (E1, E2, inversión, `nuevo`, `solap`, linaje v13, sin puerta, `plast=False`…), todas las claves | idéntico 24/24 |
| I2 | rng no consumido con `pob=0` a T = 120 000 (2 casos) | idéntico |
| I3 | `organismo_vivo_pob.run(pob=0)` contra `organismo_vivo_rep.run` en los **9 brazos** del bloque 1 de reproducción, todas las claves (incluidas las `rep`) | idéntico 9/9 × 3 |
| I4 | cadena: `organismo_vivo_pob(vivo=0, n_nec=1, pob=0)` contra `organismo_v14` | idéntico |
| I5 | `pob=1` con `costo=0` y `rep_X=T+1` (nadie muere, nadie nace): las claves del cuerpo 0 contra `pob=0` | idéntico (el planificador no toca al fundador) |
| I6 | `GEN_INERTE` contra `FIJO_05`: claves de conducta idénticas (los genes derivan, la boca no los lee) | idéntico salvo `genes` |
| I7 | **debe fallar**: `pob=1` con nacimientos y muertes ≠ `pob=0` | difiere |

### 2.8 Relación con lo que ya existe y con la sala

- **B-5 (`desambiguar`, candidato a v15).** Sus anclas están en la línea de división (`if Wb[c]*R<0 …`); las mías tocan el
  nacimiento de la hija (`madre[j]=c`), la muerte, el drenaje, el olvido de objetos y el cierre. **Son compatibles**: el
  constructor se escribe contra v14.1 y se re-ancla contra v15 si el director lo congela (mismo texto de anclas; B-5 no lo
  altera). Si `desambiguar` entra, "sal rosa" nace como hija de "sal" con `madre[j]=c` y el linaje **hereda el árbol**.
- **`DIAG_mundo.md` §3 (misma sala) propone el mismo bloque.** Coincido en: muerte que borra, nacimiento por ventana pagada,
  `olvido_hijo`, "selección: ninguna programada — sólo la física", `t_ext` y R₀, y "la tercera necesidad vuelve como prueba".
  **Difiero en tres cosas, con razón:** (1) **mundo**: propone `L = 40·N, nobj = 4·N` (misma densidad por cuerpo → N linajes
  casi independientes, sin competencia); yo dejo el anillo del tronco (`L = 40, nobj = 4`) porque la competencia por la misma
  comida ES la presión de selección y porque mi corrida (§0.2) muestra que la densidad no ayuda; un mundo más **grande**
  (`L = 80, nobj = 8`) queda como rama de contingencia predeclarada (§4.6). (2) **barajada**: propone "memoria de un cuerpo de
  otra semilla" — pero la lineal `Wps/Wns` vive sobre la retina, que es la misma en todas las semillas: esa herencia
  **transfiere la regla correcta** y no destruye nada (sería un hallazgo, no un control). Mi BARAJA permuta el valor dentro
  del propio hijo: misma cantidad, contenido roto. (3) **umbrales**: "sobrevive a T en ≥ 15/20" no tiene ningún número
  medido detrás y el mundo del tronco mata 64–100 veces por 100 000 pasos; hago decisivos los **contrastes** (A₁₂) y reporto
  la persistencia absoluta con banda ancha.
- **`DIAG_metodo.md` G-1 (árbol de fisión como grafo)** es exactamente `madre[j]=c`: aquí entra como estado heredable, no sólo
  como lectura. **`DIAG_dinamica.md` (trampa "la herencia de miedo se protege a sí misma")** es la razón de V3 (§4.4).

---

## 3. Por qué sale de la frontera: capacidades NUEVAS y MEDIBLES

1. **Un linaje que vive más que cualquier cuerpo.** Hoy no existe ningún cuerpo mortal: el brazo UN_CUERPO (mortal, sin
   reproducción) da por primera vez **la vida de un individuo** (predicción: mediana < 10 000 pasos; ninguno llega a T). Si
   HEREDA persiste ≥ 5 × eso y BLANCO/BARAJA no, se cumple **literalmente** el criterio de emergencia del punto 14 del brief:
   ausente en el individuo (muere), presente en el grupo, no programada (BLANCO enseña que reproducirse no basta),
   reproducible (20 semillas + réplica) y que desaparece al romper la estructura (BARAJA).
2. **Qué memoria es portable entre cuerpos: el vector o el token.** SOLO_LENTA (vector sobre la retina) contra SOLO_RAPIDA
   (token con su valor, indexado por celdas): es la pregunta "grafo o vector" del director medida en población, con un
   número (`t_ext`, `viables`) y sin símbolo. Predicción falsable: las dos bastan y BARAJA no.
3. **Selección de un rasgo sin GA.** Un gen continuo que sube o no sube en 100 000 pasos por muertes y nacimientos locales,
   contra un gen que nadie lee y contra el mismo gen desconectado. Es la salida que el director dejó escrita en el criterio
   de parada del 04:55 ("evolución del organismo entero") con un primer rasgo, y con controles que pueden hacerla caer.
4. **Desaprender a escala de linaje.** Cuando el mundo cambia (inversión a 50 000), lo heredado se vuelve veneno: la muerte
   selecciona entre linajes que heredan todo y linajes que olvidan la mitad. Etapa 4 lo dejó a 12/20 en un cuerpo (H4);
   aquí la medida es la que mata.

Lo que NO cambia: XOR con 8 ejemplos, la construcción del rasgo conjuntivo, la capacidad, el examen v3′ (que **no mide** este
candidato: con `pob=0` es v14.1; como B-5, lo mide su propio bloque y así se congelaría, si se congela).

---

## 4. Preregistro propuesto (semillas nuevas; un `Pool` a la vez; el coordinador corre)

**Estadística (lecciones de ERR-37):** `t_ext`, `pob_T`, `nac`, `viables`, `mort_inf`, `vidas`, `g_*_T` son integrales de
trayectoria → **A₁₂ sin parear** (400 pares), razón de medianas y cuartiles; pareado por semilla sólo lo aprendido (tabla 2 × 4 del
cuerpo más viejo). `t_ext` censurado en T cuenta como T y se reporta la fracción censurada. Un `None` (sin nacimientos) nunca
cuenta como victoria. Ningún umbral en la mediana esperada del propio efecto; ningún `max`. Regla 12: un veredicto a ±1 semilla
dispara réplica en el rango siguiente. Regla 10: el runner calcula los **alias estructurales** (los cinco solapamientos de K = 3
con cuatro estímulos, `diagnostico_codigos.py`, sin simular) al arrancar y reporta el conjunto completo y las LIMPIAS.

**Semillas** (vírgenes; la sala usó 1101–1140 y 1201 en diagnósticos estructurales, se evitan): V0 **1301–1320**, V1
**1321–1340**, V2 **1341–1360**, V3 **1361–1380**; réplicas **1401–1420 / 1421–1440 / 1441–1460 / 1461–1480**. T = 100 000.

### 4.1 V0 — humo de identidad + el mundo del tronco (`organismo_v16v.py`: una necesidad, comida/veneno, `nobj=4`, `costo=0.002`)
Brazos: UN_CUERPO (`pob=1, rep_X=T+1`), HEREDA, BLANCO. 60 corridas.

| # | predicción | refuta |
|---|---|---|
| **P-V0** | A₁₂(`t_ext` HEREDA > BLANCO) **≥ 0.90**; razón de medianas ≥ 5; BLANCO `t_ext` ≤ 10 000 en ≥ 16/20; UN_CUERPO muere antes de T 20/20 | A₁₂ < 0.70: heredar no sostiene un linaje ni en el mundo más simple → la línea se cierra aquí y V1 no se corre |

### 4.2 V1 — herencia en el mundo vivo (`organismo_vivo_pob.py`, `rep_cuello=2`, sin genes; VIVO 2 necesidades, 4 estímulos, `costo=costo_a=0.001`)
Brazos (§2.5): UN_CUERPO, HEREDA, SOLO_LENTA, SOLO_RAPIDA, BARAJA, ESCALAR, PATAS, BLANCO. 160 corridas.

| # | predicción (1321–1340) | de dónde sale | refuta |
|---|---|---|---|
| **P-V1** emergencia | UN_CUERPO: vida mediana **≤ 10 000**, 20/20 mueren antes de T (vidas máximas medidas: 4 571–8 697). HEREDA: `t_ext` mediana **≥ 5 ×** vida de UN_CUERPO; A₁₂(HEREDA `t_ext` > UN_CUERPO vida) **≥ 0.90** | vidas de rep2 y §0.2; H1 (80 % menos veneno inicial) | A₁₂ < 0.75: el linaje no vive más que un cuerpo |
| **P-V2** contenido | A₁₂(`t_ext` HEREDA > BARAJA) **≥ 0.90** y (HEREDA > BLANCO) **≥ 0.90**; BARAJA ≤ 1.5 × BLANCO (razón de medianas); ESCALAR y PATAS ≤ 2 × BLANCO | el barajado destruye en todo el proyecto (N1, mundo vivo, B-5) | A₁₂ < 0.70, o BARAJA ≥ 3 × BLANCO (persiste por la cantidad, no por el contenido) |
| **P-V3** vector contra token | SOLO_LENTA y SOLO_RAPIDA: cada una ≥ 0.5 × HEREDA en `t_ext` (medianas) y A₁₂ contra BLANCO **≥ 0.85**; **orden (blanda)**: A₁₂(SOLO_LENTA > SOLO_RAPIDA) ≥ 0.55 (el vector generaliza y no depende de que el código del hijo sea el del padre; en un mundo de 4 patrones puede empatar) | v13/v14: la lenta generaliza 1.000; la puerta cierra sin `ncod` | alguna de las dos ≤ BLANCO (A₁₂ < 0.60): esa memoria sola no se hereda |
| **P-V4** descendencia condicionada a supervivencia (ERR-40) | `viables` HEREDA mediana **≥ 5** y A₁₂(HEREDA > BLANCO) **≥ 0.95** con BLANCO mediana 0; `mort_inf` HEREDA **≤ 0.6**, BLANCO **≥ 0.9**; **la que puede fallar limpio**: en los 7 contrastes contra BLANCO, A₁₂ en `viables` y en `t_ext` tienen el mismo signo (la medida ordena como la supervivencia) | un hijo BLANCO muerde lo primero que pisa (`W=0 → pb 0.99` con déficit 0.5) y el anillo es 85 % veneno/sal | `mort_inf` HEREDA ≥ 0.8: los hijos nacen para morir (la dote no alcanza; se reporta, no se recalibra); o un contraste con signos opuestos: la medida se tira por tercera vez |

Se reporta además, sin umbral: `pob_T` y fracción de linajes vivos a T por brazo; `fundador_sin_hijos`; `gen_max`; `vidas`
(ahora vidas de verdad); tabla 2 × 4 estricta del cuerpo más viejo a T (¿el linaje conserva el conocimiento?);
`frac_veneno` del anillo cada 5 000 pasos (¿N cuerpos lo atascan más?); `aborto` (nunca debe morder).

### 4.3 V2 — el propósito como gen (mundo vivo, `hereda='todo'`)
Brazos: FIJO_0 (`rep_cuello=0`: lectura VIVO), FIJO_05 (`g0=0.5`, `genes=0`), FIJO_1 (`rep_cuello=2`, `genes=0`: CUELLO_MIN),
GENES (`genes=1, gen_activo=1`), GEN_INERTE (`genes=1, gen_activo=0`). 100 corridas.

| # | predicción (1341–1360) | de dónde sale | refuta |
|---|---|---|---|
| **P-V5** selección | GENES: `g_pes_T` (media de los vivos a T, o de los vivos en `t_ext − 1`) mediana **≥ 0.75** y > 0.5 en **≥ 16/20**; GEN_INERTE > 0.5 en **[5, 15]/20** (banda binomial del azar); A₁₂(`g_pes_T` GENES > GEN_INERTE) **≥ 0.85**; dentro de GENES, `g_pes_T − g_nul_T > 0` en **≥ 15/20** | CUELLO_MIN muere menos (76 contra 100) y hace 3 × más ventanas: los cuerpos con `g` alto se duplican más y mueren menos | GENES > 0.5 en ≤ 13/20, o A₁₂ < 0.65: la selección no sube el gen en 100 000 pasos (el linaje muere antes de que actúe, o el rasgo no paga en población) |
| **P-V6** el propósito paga en supervivencia | `t_ext`: A₁₂(FIJO_1 > FIJO_0) **≥ 0.80**; A₁₂(GENES > FIJO_05) **≥ 0.70**; A₁₂(FIJO_1 > GENES) ∈ **[0.45, 0.85]** (la selección se acerca al rasgo fijo, no lo supera) | r −13 contra −80 en 221–240 | A₁₂(FIJO_1 > FIJO_0) < 0.60: con muerte real la lectura pesimista no compra nada; entonces "propósito" vuelve a ser una lectura y se dice |

### 4.4 V3 — desaprender en el linaje (mundo vivo, inversión comida↔veneno en el paso 50 000; `hereda='todo'`)
Brazos: HEREDA (`olvido_hijo=0`), HEREDA_OLV (`olvido_hijo=0.5`). 40 corridas. Sólo entre semillas con linaje vivo a 50 000.

| # | predicción (1361–1380) | de dónde sale | refuta |
|---|---|---|---|
| **P-V7** | HEREDA: muertes por cuerpo-paso en [50 000, 55 000] **≥ 2 ×** las de [45 000, 50 000] (A₁₂ ≥ 0.80); a T, entre los linajes vivos, la tabla del cuerpo más viejo tiene los **signos nuevos** en A y B en ≥ 12/15; HEREDA_OLV: pico menor, A₁₂(HEREDA pico > HEREDA_OLV pico) **≥ 0.65** (blanda: precedente H4 12/20 y la trampa de `DIAG_dinamica`: el miedo heredado se protege a sí mismo) | E2 de v14.1 20/20 en un cuerpo; H4 | sin pico (el linaje no llevaba el valor viejo, luego no heredaba nada útil) o tabla vieja a T (el linaje no se desdice) |

### 4.5 Controles, en el lenguaje del encargo
**Barajado**: BARAJA (§2.5) y `g_nul`. **Escalar**: ESCALAR y PATAS (cantidad sin contenido). **Apagado**: `pob=0` (I1–I4),
GEN_INERTE (el gen desconectado), FIJO_05 (≡ GEN_INERTE en conducta). **Azar**: orden de los cuerpos al azar por paso; banda
binomial para el gen neutro; alias estructurales reportados aparte. **Regresión**: `bateria_v16.py 6` y
`bateria_generaliza_v16.py organismo_v16v 20 --desde 101` con la entrada **comparada campo a campo** con la del tronco
(`eta_s=0.15, clip_s=10.0` explícitos; regla 14) — esperado idéntico por identidad, y se corre igual.

### 4.6 Cláusulas escritas ahora
1. Si **P-V0** cae, V1–V3 no se corren: la línea "vivir por herencia" queda cerrada para este tronco con ese dato.
2. Si en V1 los contrastes pasan pero HEREDA se extingue antes de T en **≥ 18/20**, se declara *"el mundo del tronco no
   sostiene un linaje mortal, pero heredar lo alarga ×k"* y se corre **una vez** la rama de contingencia **MUNDO_B**
   (`L = 80, nobj = 8`: el doble de anillo, la misma densidad; un solo cambio, ERR numerado por el coordinador) con la
   **misma letra** de P-V1–P-V4 en 1481–1500. Nada más se toca.
3. Si `aborto` muerde en alguna semilla, el mundo es demasiado rico para el instrumento: se reporta y no se compara esa semilla.
4. Ningún umbral se mueve tras ver datos; modos de herencia intermedios (`olvido_hijo` distinto de 0 y 0.5, dotes, `rep_X`)
   sólo con preregistro nuevo.
5. **Qué se declara si pasa todo, y sólo entonces:** *"en el anillo del tronco un cuerpo mortal vive < 10 000 pasos y un linaje
   que hereda el código con su valor vive ≥ 5 × más; la herencia barajada, un escalar o nada no lo sostienen; el vector sobre
   la retina y el token con su valor son portables por separado; la lectura pesimista saciado sube como gen por muerte y
   nacimiento locales y alarga el linaje; tras la inversión el linaje paga lo heredado y se desdice"*. Vocabulario permitido:
   *hereda, linaje, persiste, se extingue, selección (frecuencia alélica), desaprende*. **Prohibido**: "evoluciona
   inteligencia", "quiere", "propósito" sin la medida alélica, "lenguaje", "población inteligente".

---

## 5. Coste e instrumentos (por anclas; congelados sólo leídos; `manifiesto.py --check` tras construir)

| archivo (en `experimentos/nivel12_poblacion/`) | origen (sha) | qué es |
|---|---|---|
| `construye_pob.py` | — | escribe **`organismo_v16v.py`** (v = vivir; el nombre `organismo_v16.py` ya lo usa en esta carpeta el instrumento TOKEN del creador radical, que no es candidato; la etiqueta "v16" la da el director) ← `organismo/organismo_v14.py` (feefc88b1fd8d434) y **`organismo_vivo_pob.py`** ← `experimentos/nivel11_mundo_vivo/organismo_vivo_rep.py` (aa823d56c2d4213c); anclas A1–A12 (+ A-CUELLO §2.6 y las tres anclas del mundo vivo: muerte `if E<=0 or (vivo and Ag<=0):`, ventana `_desc+=1; _dq[q(t)]+=1; _gv=0`, `Ag=A_ini`); aborta si un ancla no aparece exactamente una vez; comprueba que ninguna inserción nombra `rng` salvo A2/A8 (declaradas) |
| `identidad_pob.py` | arnés de v15e (058e15147f05ef27) como modelo | I1–I7 (§2.7); salida a `datos/pob_identidad_*.log` |
| `bateria_v16.py` | `organismo/bateria_v14.py` (72216f5415de0c86) | examina `organismo_v16v` con `pob=0`; sha de v11/v10 leídos desde `organismo/` (ERR-42); humo que ESCRIBE su JSON antes de la serie (regla 14) |
| `bateria_generaliza_v16.py` | `organismo/bateria_generaliza.py` (9cf72581ebae7dea) | entrada `'organismo_v16v'` comparada campo a campo con `'organismo_v14'` por el constructor (regla 14 / ERR-38) |
| `corre_pob.py` | `corre_vivo_rep2.py` (10ab45355883d98d) como modelo | etapas V0 → V1 → V2 → V3, identidad dentro del runner (7 casos × 3 semillas: si no es 21/21 no corre nada), `--humo` de un proceso, alias estructurales al arrancar, JSON desde el arranque, línea de progreso cada 20 corridas, `Pool(14)` una etapa a la vez, lee los campos de la batería y no reconstruye del log (ERR-43) |
| `PREREGISTRO_pob.md` | §4 de este archivo | con las cifras del humo añadidas DESPUÉS y dichas |

**Cómputo.** v14.1 corre a ~4 s por 100 000 pasos; el mundo vivo a 5–7 s (medido: 3.3 s por 50 000 con el `Pool` de v15e
vivo). Una corrida de población cuesta `Σ pasos vividos por todos los cuerpos`: cota superior `n_abort × T` (≈ 80 s), típica
(extinción o 2–6 cuerpos) 10–30 s. V0 60 + V1 160 + V2 100 + V3 40 = **360 corridas ≈ 6 000–9 000 s de CPU → 8–11 min con
`Pool(14)`**; réplica igual; identidad ~3 min; examen + generalización ~8 min. Sin gemelo numba (regla 9: los instrumentos del
mundo vivo no lo tienen; si el bloque se replica y se barre, el gemelo del planificador es lo primero que hay que pagar).
**Del `Pool` exige** una cosa nueva: corridas de duración muy desigual (extinción temprana contra 8 cuerpos hasta T) → `imap_unordered`
y progreso por corrida terminada, no por índice. Nunca dos `Pool`; el de v15e/rep2 termina antes.

**Humo (un proceso, ≤ 6 corridas de T = 100 000, semillas 1–2, escrito ANTES de lanzarlo):** H-1 identidad 21/21 dentro del runner;
H-2 UN_CUERPO muere antes de 20 000 en 2/2; H-3 HEREDA `nac ≥ 3` y `t_ext` > UN_CUERPO en 2/2; H-4 BLANCO `t_ext` < HEREDA en 2/2;
H-5 GENES con ≥ 3 nacimientos muestra `g_pes` distinto de 0.5 en algún hijo (la mutación actúa). Si H-1 falla no se corre nada;
los demás fallos se escriben y el bloque corre con esta letra.

---

## 6. Humo y espejos: cómo podría engañarnos y cómo se evita

| espejismo | por qué es posible | guardia |
|---|---|---|
| **El inmortal por la puerta de atrás.** Con herencia completa y nacimientos frecuentes, el linaje ES el cuerpo con renacer de antes, rebautizado | el mecanismo copia toda la memoria | la dote se paga (nada se regala); lo aprendido entre el último parto y la muerte **se pierde** (medido: `perdida` = mordidas del cuerpo tras su último hijo); y la comparación decisiva es contra BLANCO/BARAJA con la MISMA física de nacimiento: si esos persisten igual, la persistencia es del mundo, no de la herencia |
| **El mundo lo sostiene todo** (demasiado rico) | `nobj`, dote, `rep_X` mal puestos | BLANCO debe extinguirse (P-V0/P-V2); si BLANCO persiste en ≥ 5/20, el bloque es nulo (no se endurece el mundo sobre esos datos: rama nueva, ERR numerado) |
| **El mundo no sostiene nada** (demasiado duro) y "heredar no sirve" | §0.2: el anillo del tronco mata 64–100 veces por 100 000 | los contrastes deciden, la persistencia absoluta se reporta; MUNDO_B predeclarado (§4.6.2) con un solo cambio |
| **Ventaja por orden de índice** (el fundador come primero) | N cuerpos apuntan al mismo objeto | orden al azar por paso con rng del mundo; el olvido de objetos lo ejecuta un solo cuerpo (A8) para que la renovación no escale con N |
| **Deriva disfrazada de selección** (poblaciones de 2–8: un alelo neutro se fija a menudo) | tamaño efectivo minúsculo | `g_nul` en la misma corrida, GEN_INERTE con la misma mutación, banda binomial [5, 15]/20 para lo neutro, A₁₂ entre brazos; el reflejo en [0, 1] es simétrico para el fundador en 0.5 y compartido por los controles |
| **Descendencia que premia morir** (ERR-40 otra vez) | contar nacimientos | un hijo cuenta sólo vivo a 2 000 pasos; un muerto no reproduce; `t_ext` no se puede ganar muriendo; P-V4 exige que `viables` y `t_ext` ordenen igual o la medida se tira por tercera vez |
| **Censura a T leída como vida eterna** | `t_ext = T` | fracción censurada reportada; la razón de medianas se lee con la censura declarada |
| **Los cuerpos de una semilla tratados como independientes** | pseudo-réplica | toda estadística es entre semillas (20 contra 20); dentro de la semilla sólo se agrega |
| **El fundador muere sin hijos y "hereda" no se probó** | vida mediana 600 del renacer | `fundador_sin_hijos` se reporta aparte; cuenta como extinción (honesto) y su fracción entra en el registro |
| **El examen del tronco "pasa" y se vende como prueba del candidato** | con `pob=0` es v14.1 | se dice como B-5: el examen no mide este candidato; lo miden V0–V3 |
| **Vocabulario** | "vive", "quiere", "evoluciona" | §4.6.5 |

---

## 7. La hipótesis del director en este ángulo (token = código; la variante como variable del mismo; grafo, no vector; aprender y desaprender)

- **"Sal es sal, número uno, lo guardo, lo vectoriza."** En el tronco el token es `code(P)` (3 celdas de 90) con su evidencia
  `ncod`, y el vector es la lineal `Wps − Wns` sobre la retina. **Este diseño hace de la pareja token + valor la unidad de
  herencia**: lo que pasa de padre a hijo es el código con lo que vale (SOLO_RAPIDA) o el vector (SOLO_LENTA), y por primera
  vez se mide **cuál de los dos viaja entre cuerpos**. Predigo que los dos viajan y que barajar el valor sobre el token lo
  mata: "número uno" sin su significado no sirve para vivir.
- **"Sal rosa … variable de lo mismo."** La única relación explícita entre tokens que el tronco puede tener hoy es la arista
  madre → hija de la fisión (v11) y de la división por `R = 0` (B-5): `madre[j]=c` la anota (lectura pura, un entero por celda)
  y el linaje **hereda el árbol**. No es un grafo que se recorra ni una lectura por parentesco (lo dice `DIAG_dinamica`):
  es la estructura mínima para que "sal rosa nace de sal" sea un hecho contable y heredable, no una metáfora. Se reporta
  `profundidad` por linaje; no se predice nada sobre ella (con herencia completa no espero emergencia en el árbol).
- **"Grafo, no vector."** El vector (la lineal) es portable entre cuerpos con códigos distintos porque vive sobre la retina; el
  token no lo es sin su `KW`. V1 lo mide (P-V3). Si SOLO_LENTA ≥ SOLO_RAPIDA, el vector es la memoria de especie y el token la
  memoria del individuo; si al revés, el token con su valor basta. Cualquiera de las dos es un dato para la corrección del
  director del 05:25, no un argumento.
- **"Puede aprender y desaprender."** En un cuerpo ya está medido (E2 20/20; v15e se desdice en una mordida). En un linaje es
  V3: lo heredado se vuelve veneno cuando el mundo cambia, y la muerte hace la cuenta. `olvido_hijo` es la dosis de olvido
  entre generaciones; si la selección lo pidiera como gen, sería el bloque siguiente (no preregistrado aquí).
- **"Eso es lenguaje."** Prohibido hasta que un token compartido prediga entre dos cuerpos (N2 cerrado ×2). Este diseño da la
  condición previa que N2 nunca tuvo: **dos cuerpos que comparten mundo, mueren y heredan**, es decir, algo que transmitir y
  un precio por no transmitirlo.

---

## 8. Lo que este diseño no es

No es el frente único (la construcción del rasgo con reglas locales sigue sin mecanismo y este ángulo no lo toca). No es
"evolución de constantes" todavía: el único gen con efecto es `g_pes`; `hambre_boca`, `alpha`, `eta_s` como genes son el
bloque siguiente si V2 pasa, con su propio preregistro. No declara nada: propone un instrumento con identidad exacta, cuatro
bloques con 8 predicciones que pueden caer y las cláusulas para cerrarlo si caen. Si fuera mi creación, lo construiría hoy,
correría V0 en cuanto el `Pool` quede libre, y no diría "vive" hasta que BARAJA muera y HEREDA no.

---

### Apéndice — la corrida única (§0.2), tal como salió
`calib_nobj12.py` (scratchpad de esta sesión; `organismo/` primero en `sys.path`), `organismo_vivo_rep2.run(1, T=50000, vivo=1,
estims=('A','B','C','D'), costo=0.001, costo_a=0.001, n_nec=2, rep_cuello=2, reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0,
rep_coste=0.0, rep2=1, rep2_regalo=600, nobj=12)` → 3.3 s; `descendientes 56, desc_regalo 36, muertes 71 [31, 40], r −15,
vida_mediana 582, vida_max 4571, vida_final 739, exposiciones {A 452, B 6487, C 489, D 4282}, sac_dec {A 240, B 6320, C 260, D 4513},
sac_mord {A 202, B 2, C 209, D 3}, pasos_viables 38552, W_nec [{A 1.0, B −3.0, C 0, D 0}, {A 0, B 0, C 1.0, D −3.0}], celdas 35,
splits 5`. n = 1, semilla vista: no es evidencia; sirvió para no diseñar un mundo rico.
