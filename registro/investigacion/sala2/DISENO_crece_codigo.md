# SALA 2 — ángulo `crece_codigo`: EL ORGANISMO CONSTRUYE SU PROPIO RASGO (diseño v16c desde v14.1)

**Misión (primero, siempre):** llegar a la AGI por este camino — un organismo mínimo con reglas locales, sin retropropagación
en el runtime, que aprende, desaprende, generaliza, sobrevive y se reproduce, con evidencia preregistrada. Primero la
frontera; segundo, que viva. El método manda sobre el cómo (`registro/EQUIPO.md` 1–14, `CLAUDE.md`).

**Creador de la sala 2, 18 sep 2026 (~10:00).** Este archivo es DISEÑO + borrador de preregistro. No toca ningún archivo del
repositorio; no corre `Pool` (v15e está en marcha); no construye instrumentos: los describe por anclas sobre
`organismo/organismo_v14.py` (v14.1, `feefc88b1fd8d434`, líneas citadas por número) para que un implementador los construya y
el coordinador los corra. Lo único que calculé es un dato estructural sin simular (§4.5, `coactividad_tren_xor01.py`, en esta
carpeta).

**En una frase.** Hoy el único mecanismo que cruza XOR con 8 ejemplos es una tabla de **15 celdas pre-enumeradas** (M3, un
prior de pares declarado) y todo intento de meterla en el tronco cayó (v15c/d/e). Propongo que el organismo **no traiga las
15 celdas de fábrica**: que **recluta un nodo conjuntivo** sobre los dos píxeles co-activos cuando la vía lenta se sorprende
**dos veces** con la misma pareja, que ese nodo **nace leyendo lo que lee su padre** (la lineal) y sólo lo sustituye si
**reduce su error**, que **sobrescribe** su casilla en una mordida (se desdice) y que **muere** si deja de reducir el error
(poda). Con la perilla apagada es v14.1 bit a bit.

---

## 1. Qué bloquea (lectura del registro, con evidencia)

| # | bloqueo | evidencia (registro, 18 sep) |
|---|---|---|
| B1 | **Con 8 ejemplos nadie selecciona el rasgo conjuntivo con reglas locales.** 9 de 15 productos `P_i·P_j` ajustan el tren con residuo 0 y sólo uno generaliza; gradiente exacto 0.562, retropropagación 0.531; la criba de A no pasa nada con 8 (residuo 2/20, pureza 10/20, fisión de v11 **0/20**, control nulo 1/20) y pasa uno con 14. | `PUENTE_creacion.md` A12–A14; `REGISTRO` ERR-35 |
| B2 | **Lo único que cruza con 8 es un PRIOR ESTRUCTURAL pre-enumerado:** M3 = 15 celdas fijas (una por par) × 4 casillas, escritas de un golpe, leídas por menor error propio → 1.000 / 1.000, n\* = 7–10, replicado 121–140 y 141–160. Declarado como prior, no como aprendizaje. Y el sintetizador de la sala lo dijo: *"15 pares son 15, pero C(n,2) no lo es: ninguno escala"*. | `ENJAMBRE_xor_20260918.md` §5–§6; `REGISTRO` "LÍNEA XOR CERRADA" |
| B3 | **Llevar la tabla al tronco cayó tres veces, y cada caída enseña una restricción del diseño:** v15c (V1 sin medir; ERR-38/41/42); **v15d** *no se desdice* (E2 0/20) y *mata de mordidas a la vía rápida* (E1 0/20) por **doble cuenta** (la lenta lee 1.45·R en una mordida); **v15e** arregla E1/E2 (lectura exacta tras una mordida, se desdice en una) pero **pierde XOR** (humo xor01 0.250 < OFF 0.375): una tabla que guarda *lo que a la lineal le falta* hereda el fracaso de la lineal y **pierde la identificabilidad** (gana (2,4), no (0,1)). A16 concluye: la casilla debe guardar **R crudo**, con **sobrescritura** y **relevo** a la lineal, **cada vía con su error**. | `PREREGISTRO_v15e.md` §1, §8; `PUENTE` A16; `REGISTRO` v15d |
| B4 | **El organismo no tiene ningún mecanismo que construya estructura del lado de la retina.** Su único órgano estructural es la división de v11 (lado Kenyon), y como creadora de rasgos está en el azar (B1). La vía lenta es un lector lineal fijo de 6 números: no puede nacerle una conjunción. Es el cuello que la misión nombra: *construir el rasgo desde los píxeles sin prior* (HANDOFF 15.8.7: "sigue sin mecanismo"). | `PUENTE` A13; `HANDOFF` §15.8.7 |
| B5 | **La medida que manda es exposiciones hasta asociar** (director, 05:10): el tronco necesita > 600 en xor01 y 150–200 con rasgos dados; sólo la tabla de un golpe baja a 7–10, y sólo pre-enumerada. | `PLAN.md` 05:10; `REGISTRO` bloque 3/3 |
| B6 | **Techo de muestreo** (no lo arregla ningún lector): clase XOR sin mordidas en 6/20 semillas (C midió 01 → 0 mordidas); 2–4/20 semillas sin una clase en las series de M3. Lo declaro como cláusula, no lo ataco. | `PUENTE` A6; `REGISTRO` bloque 3/3 (cláusula de muestreo) |

**Lo que se deduce para el diseño (restricciones, no gustos):** (i) el rasgo tiene que ser una **tabla de 2 bits sobre un
par** (es lo único que rompe el empate de 9/15: B1–B2); (ii) tiene que guardar **R crudo** y **sobrescribir** (B3, v15e);
(iii) tiene que **relevar** a la lineal, no sumarse a ella (B3, v15d); (iv) tiene que **nacer** del lado de la retina, por
un criterio local distinto de la fisión de v11 (B4, A13: la fisión no propone (0,1)); (v) tiene que **medirse en exposiciones**
(B5) y con los controles de la línea (`px0`, `azar` en banda, puntuación estricta, desempate al azar).

---

## 2. Mecanismo: "reclutar por sorpresa, leer si reduce el error, sobrescribir, podar"

### 2.1 Idea en cuatro reglas locales (todo se lee en la mordida presente; nada mira al futuro; nada usa gradiente)

1. **Sorpresa.** En cada mordida la vía lenta ya calcula su error (`R − _ws`, L117 de v14.1). Si `|R − _ws| > g_theta`
   (1.5 = la mitad de la consecuencia más fuerte, |−3|/2), la mordida es una **sorpresa** de la vía lenta.
2. **Hebb en la sorpresa (reclutar).** Cada par de píxeles **co-activos** en la retina de esa mordida (un patrón de 3 px
   tiene 3 pares) suma 1 en su traza `S[i,j]`. Cuando una pareja llega a `g_rec = 2` sorpresas ("repetida") y no tiene nodo,
   **nace un nodo** con padres `(i,j)`: una tabla de 4 casillas (una por combinación de sus dos bits), vacía salvo la casilla
   de la mordida que lo creó, que guarda **R crudo**. El nodo **nace con el error de su padre** (su primera "lectura" es la
   de la lineal en esa mordida): es *"una variable de lo mismo"* hasta que su propia consistencia lo separe.
3. **Leer por relevo (competencia).** La vía lenta lee **un solo nodo**: el de **menor error propio** entre los que (a) ya
   vieron la casilla de este patrón y (b) tienen error **menor que el de la lineal**. Si ninguno cumple, lee la lineal (el
   padre). Empates: por **boleto de nacimiento** (un número aleatorio fijado al nacer con un generador propio), nunca por
   índice (ENJAMBRE §4.1: el índice 0 *es* (0,1)). Se registra la multiplicidad del empate.
4. **Sobrescribir y podar (desaprender).** En cada mordida **todos** los nodos vivos actualizan su error propio con lo que
   *habrían* leído (su casilla si la vieron; si no, la lineal) y sobrescriben la casilla con **R crudo** (`mem_alfa = 1`:
   la casilla sigue a la última recompensa → se desdice en UNA mordida). Un nodo con `≥ g_min_vis = 6` visitas cuyo error
   propio **no es menor** que el de la lineal **muere** (libera el hueco; su traza vuelve a 0): *el rasgo sobrevive sólo si
   reduce error*. La lineal aprende de **su propio** error (`R − lineal`, D2 de v15e) y la rápida del suyo (L115, intacta).

**Qué es esto en las palabras del director (05:10 y 09:40), sin inflar:** cada nodo es un **token con padres** (`(i,j)`, una
arista explícita entre dos nodos de la retina): **grafo, no vector** (la proyección de Kenyon sigue siendo el soporte de la
vía rápida, no se toca). La variante nace como *"variable de lo mismo"*: lee lo que lee su padre hasta que su propia tabla
la distingue (abstención al padre, no a 0). **Aprender** = escribir la casilla de un golpe; **desaprender** = sobrescribirla
(una mordida) o **podar** el nodo (deja de reducir error). Vocabulario permitido si el criterio lo respalda: *recluta un
nodo conjuntivo sobre dos píxeles co-activos cuando la sorpresa se repite; lo lee si reduce el error y si no lee al padre;
sobrescribe en una mordida; poda lo que no ayuda*. **Prohibido:** "token", "lenguaje", "entiende la combinación",
"construye conceptos", "aprende XOR" (ERR-35: con 8 ejemplos es prior; aquí el prior queda **declarado en §2.6**).

**Qué NO es.** No es la fisión de v11 (ésa actúa en el código Kenyon por conflicto de signo y propone (0,1) en 0/20: A13);
no es v15d (no hay suma: relevo); no es v15e (R crudo, no residuo); no es M3/v15f tal cual (no hay 15 celdas de fábrica:
hay reclutamiento y poda; FIJO15 es un brazo de control, §4.2). Nivel 2 (nodos cuyos padres son nodos: "sal rosa fina")
queda como perilla futura `g_nivel = 2`, **no construida y sin predicción** en este preregistro.

### 2.2 Estado nuevo y constantes (fijadas aquí por argumento; ningún barrido; cambiarlas después = ERR numerado)

| nombre | valor | por qué ese valor (no otro) | memoria |
|---|---|---|---|
| `crece` | 0 / 1 | perilla maestra; 0 ≡ v14.1 bit a bit (§2.4) | — |
| `g_theta` | 1.5 | *"la lectura se equivoca en más de la mitad de la consecuencia más fuerte"* (|R| máx = 3). Con lectura 0, la comida (+1) **no** sorprende y el veneno (−3) sí: la asimetría del mundo, heredada, no diseñada | — |
| `g_rec` | 2 | *"repetida"*: la primera sorpresa es noticia, la segunda es patrón. Derivación para el tronco en §2.5 | — |
| `g_max` | 15 | = C(6,2): el tope natural; **no** es presupuesto: la ocupación es la MEDIDA (P3) | — |
| `g_min_vis` | 6 | 4 casillas + 2: un nodo sólo se juzga cuando pudo ver cada casilla al menos una vez con margen | — |
| `g_rho` | 0.02 | la meseta que halló la búsqueda ciega de M4 (ENJAMBRE §4.2: el top-10 comparte `rho = 0.02`); mismo valor que `mem_rho` de v15e | — |
| `g_ctrl` | `None` / `'escalar'` / `'barajado'` / `'fijo15'` | los tres controles de §4.2, dentro del mismo instrumento; valor mal escrito → `ValueError` (convención v15e L56) | — |
| `g_curva` | 0 / 1 | instrumentación de sólo lectura (n\*): registra la lectura lenta sobre los patrones de test en cada mordida de tren; no consume rng (identidad I5) | — |
| `_GP` | lista de padres `(i,j)` | un par por nodo vivo | 2 × ≤ 15 |
| `_GT`, `_GV` | tablas (15 × 4) de R crudo y de visitas por casilla | la memoria de un golpe de M3, sobrescribible | 8 × ≤ 15 |
| `_GE`, `_GN`, `_GQ`, `_GA` | error propio (EMA), visitas totales, boleto de nacimiento, vivo | competencia y desempate | 4 × ≤ 15 |
| `_GS` | traza Hebb-en-la-sorpresa por par | 15 contadores | 15 |
| `_EL` | error propio de la lineal (EMA, `g_rho`) | el padre contra el que compite todo nodo | 1 |
| `_rg` | `default_rng(seed + 800000)` sólo si `crece` | boleto de nacimiento, orden de reclutas empatados, pares de BARAJADO; **nunca en la lectura** (convención `v13s`/mundo vivo) | — |

**Cuenta honesta de memoria:** por nodo 13 números (2 + 4 + 4 + 1 + 1 + 1); tope 15 nodos → 195 + 15 + 1 = **211 en el peor
caso** (M3/v15f: 135 fijos). No es menos memoria en el peor caso: es memoria **que sólo se gasta donde hubo sorpresa** y que
**crece con las sorpresas, no con C(n,2)**. En la retina de 6 px la ventaja se mide como ocupación (P3); la escalabilidad
a retinas grandes queda como proyección, **no como medida** de este bloque.

### 2.3 Pseudocódigo por anclas sobre `organismo/organismo_v14.py` (v14.1). Sólo se lee; la copia la genera `construye_v16c.py`

**Ancla A — firma (L39).** Añadir al final de los kwargs, con estos valores por defecto:
`crece=0, g_theta=1.5, g_rec=2, g_max=15, g_min_vis=6, g_rho=0.02, g_ctrl=None, g_curva=0`.

**Ancla B — estado (tras L50, `Wps=np.zeros(6); Wns=np.zeros(6)`):**
```python
if g_ctrl not in (None,'escalar','barajado','fijo15'): raise ValueError(f"g_ctrl={g_ctrl!r}")
_PAR=[(i,j) for i in range(6) for j in range(i+1,6)]                      # los 15 pares posibles (sólo fijo15/barajado los enumeran)
_GP=[None]*g_max; _GA=np.zeros(g_max,bool); _GT=np.zeros((g_max,4)); _GV=np.zeros((g_max,4),int)
_GE=np.full(g_max,np.inf); _GN=np.zeros(g_max,int); _GQ=np.zeros(g_max); _GS=np.zeros((6,6)); _EL=np.inf
_rg=np.random.default_rng(seed+800000) if crece else None                  # generador PROPIO: el rng del organismo no se toca
g_reclutas=0; g_podas=0; g_reclutas_t=[]; g_podas_t=[]; g_sorp_q=[0]*4; g_emp=[]; g_curva_l=[]
def _lin(P): return float((Wps-Wns)@P)                                     # la lectura lineal de v14.1, literal
def _cas(P,i,j): return int(P[i])*2+int(P[j])                              # casilla = 2 bits de los padres
def _lector(P):                                                            # el nodo que lee, o None; y la multiplicidad del empate
    best=None; m=np.inf; emp=0
    for n in np.flatnonzero(_GA):
        i,j=_GP[n]; c=_cas(P,i,j)
        if g_ctrl=='escalar' and c!=3: continue                            # ESCALAR: el producto sólo sabe de la casilla 11
        if _GV[n,c]==0 or not (_GE[n]<_EL): continue                       # relevo: sin casilla vista, o sin reducir el error del padre, no lee
        if _GE[n]<m-1e-12: best=int(n); m=float(_GE[n]); emp=1
        elif abs(_GE[n]-m)<=1e-12:
            emp+=1
            if _GQ[n]>_GQ[best]: best=int(n)                                # desempate por boleto de nacimiento, nunca por índice
    return best,emp
def _lenta(P):                                                             # la vía lenta que usa la boca
    if not crece: return float((Wps-Wns)@P)                                # APAGADA: la expresión de v14.1, bit a bit
    n,emp=_lector(P)
    if n is None: return _lin(P)                                           # abstención AL PADRE, no a 0
    i,j=_GP[n]; return float(_GT[n,_cas(P,i,j)])
def _nace(i,j,P,R,_lb):
    n=int(np.flatnonzero(~_GA)[0]); _GA[n]=True; _GP[n]=(i,j); _GT[n]=0.; _GV[n]=0
    _GT[n,_cas(P,i,j)]=R; _GV[n,_cas(P,i,j)]=1                            # nace con la casilla de la sorpresa que lo creó, R CRUDO
    _GE[n]=(R-_lb)**2; _GN[n]=1; _GQ[n]=float(_rg.random()); _GS[i,j]=0.  # hereda el error del padre en esta mordida
    return n
if g_ctrl=='fijo15':                                                       # control de Occam: las 15 de fábrica, sin reclutar
    for (i,j) in _PAR: n=int(np.flatnonzero(~_GA)[0]); _GA[n]=True; _GP[n]=(i,j); _GQ[n]=float(_rg.random())
```

**Ancla C — `valor(P)` (L62–64):** `_s=float((Wps-Wns)@P)` → `_s=_lenta(P)`. (Apagada: la misma expresión.)

**Ancla D — la boca (L101):** `_ws=float((Wps-Wns)@PAT[kk])` → `_ws=_lenta(PAT[kk])`. L102–103 intactas.

**Ancla E — aprendizaje de la vía lenta (L115–120).** L115 (`dlt=R-_wt if puerta is None else R-_wf`) **intacta**. Dentro de
`if eta_s:` (L116; el grafo es parte de la vía lenta: **la lenta apagada apaga su grafo**, y así el control 3′ del examen —
`eta_s=0, puerta=None` — sigue midiendo la rápida sola):
```python
_lb=_lin(PAT[kk]); _ds=dlt if puerta is None else R-_lb                    # D2 (v15e): la lineal aprende de SU error; apagada: _lb == _ws, misma expresión
... L118–L120 intactas (drenaje, Wps/Wns) ...
if crece: _crece_paso(PAT[kk],R,_ws,_lb)                                    # después del paso de la lineal
```
```python
def _crece_paso(P,R,_ws_boca,_lb):
    nonlocal _EL,g_reclutas,g_podas                                        # cierres de run(): nonlocal, como los contadores de v14.1
    e=R-_ws_boca                                                           # sorpresa sobre lo que la boca leyó por la vía lenta (nodo o lineal)
    el=(R-_lb)**2; _EL=el if not np.isfinite(_EL) else (1-g_rho)*_EL+g_rho*el
    for n in np.flatnonzero(_GA):                                          # TODOS los nodos vivos escriben en cada mordida (M3)
        i,j=_GP[n]; c=_cas(P,i,j)
        if g_ctrl=='escalar' and c!=3: pred=_lb
        else: pred=float(_GT[n,c]) if _GV[n,c]>0 else _lb                  # lo que ESE nodo habría leído (relevo al padre)
        en=(R-pred)**2; _GE[n]=en if _GN[n]==0 else (1-g_rho)*_GE[n]+g_rho*en
        if not (g_ctrl=='escalar' and c!=3): _GT[n,c]=R; _GV[n,c]+=1      # SOBRESCRITURA con R crudo: se desdice en una mordida
        _GN[n]+=1
        if _GN[n]>=g_min_vis and _GE[n]>=_EL:                              # PODA: sobrevive sólo si reduce el error del padre
            _GA[n]=False; _GS[i,j]=0.; g_podas+=1; g_podas_t.append((t,(i,j)))
    if g_ctrl=='fijo15': return                                            # sin reclutamiento
    if abs(e)>g_theta:
        g_sorp_q[q(t)]+=1
        act=[k for k in range(6) if P[k]>0]; pares=[(a,b) for a in act for b in act if a<b]   # co-activos: Hebb en la sorpresa
        if g_ctrl=='barajado': pares=[_PAR[k] for k in _rg.choice(15,size=len(pares),replace=False)]   # control: pares al azar
        for (i,j) in pares: _GS[i,j]+=1
        vivos={_GP[n] for n in np.flatnonzero(_GA)}
        listos=[p for p in pares if _GS[p]>=g_rec and p not in vivos]
        if len(listos)>1: listos=sorted(listos,key=lambda p:(-_GS[p],_rg.random()))   # orden por traza; empates al azar (rng propio)
        for (i,j) in listos:
            if (~_GA).any(): _nace(i,j,P,R,_lb); g_reclutas+=1; g_reclutas_t.append((t,(i,j),kk))
```

**Ancla F — salida (L164–165):** claves nuevas de sólo lectura: `crece, g_ctrl, g_nodos` (padres vivos al final),
`g_reclutas, g_podas, g_reclutas_t, g_podas_t, g_sorp_q, g_emp` (multiplicidades de empate al leer, si se registran),
`W_grafo` (`_lenta(PAT[k])` por patrón), `g_lector` (nodo que lee cada patrón al final). Todas en `NUEV` del arnés.

**Gemelo del mundo de regla (`organismo_v16gc.py` ← `organismo/organismo_v14g.py`, `1f1318480cd34cde`):** las mismas
anclas A–F más: (G1) en la sonda a priori (`t==fase2_en`): `W_lenta_apriori={k:_lenta(P_[k])}`, `g_lector_apriori`
(nodo ganador y multiplicidad por patrón de test), `g_nodos_apriori` (padres vivos en la sonda), `g_cobertura_apriori`
(casillas vistas del ganador); (G2) perilla `invertir_regla_en=None` (≡ v14g): en ese paso
`val={k:('comida' if v=='veneno' else 'veneno') for k,v in val.items()}` (P8); (G3) `g_curva=1`: tras cada mordida de tren
antes de la sonda (y tras la inversión, si la hay) añade `(n_mordidas_tren, acc_registro, acc_estricta)` de la lectura
lenta sobre los patrones de test — **lectura pura**: no toca estado ni rng (identidad I5). El acierto es balanceado y con
las dos puntuaciones de la línea (registro: 0 exacto = 0.5; estricta: 0 = fallo).

### 2.4 Apagado ≡ v14.1 bit a bit (cómo, y cómo se comprueba)

Con `crece=0`: `_lenta(P)` devuelve **literalmente** `float((Wps-Wns)@P)` (la expresión de v14.1 en L63 y L101); la lineal
aprende con `R-_lb` donde `_lb` es esa misma expresión (v15e ya verificó esta identidad 24/24); ninguna rama de `_crece_paso`
se ejecuta; `_rg` no se crea; el `rng` del organismo no recibe ninguna llamada nueva; la salida sólo añade claves nuevas.
Se comprueba con `identidad_v16c.py` (§5): I1 24/24 ≡ v14.1 (los 12 escenarios de `identidad_v15e.py`), I2 rng no consumido
a T = 120 000, I3 6/6 ≡ v14g con los kwargs EXACTOS de la entrada `'organismo_v14'` (regla 14), **I7 `crece=1, g_max=0`** ≡
v14.1 salvo claves nuevas (el relevo con cero nodos devuelve la lineal exacta y no toca el rng).

### 2.5 ¿Actúa en el tronco? Sí, y por eso el examen lo mide (derivación escrita antes de medir)

Con `eta_s = 0.15` la lectura lineal de un patrón de 3 px se mueve `0.45·e` por mordida. Estímulo nuevo veneno (E1, B):
errores −3.00 → −1.65 → −0.91: **dos sorpresas** (> 1.5) → con `g_rec = 2` **se reclutan los 3 pares de B en su segunda
mordida** y la vía lenta lee **−3.00 exacto desde esa mordida** (v14.1 tarda ~5). Inversión (E2): A +1 → −3: errores −4.00,
−2.20, −1.21 (dos sorpresas; las casillas de A se sobrescriben en la primera mordida tras el cambio); B −3 → +1: +4.00,
+2.20, +1.21 (dos). **Por tanto el mecanismo NO es inerte en el tronco** y el examen v3′ **sí mide al candidato** (a
diferencia de B-5, donde el tronco no lo medía). Lo que compra: la lenta acierta a la primera repetición; lo que arriesga
(y decide V1): que la lectura exacta temprana quite mordidas a la vía rápida (v15e midió que **no**: con lectura exacta
desde la primera mordida la rápida recibió 49–58 mordidas de B contra 47–51 en v14.1 y consolidó −2.97/−2.99) y que en E2L
la lectura exacta temprana retrase la división del código compartido (criterio 4d: "E2L divide y termina antes de 25 000").
Con `g_rec = 3` el tronco sería inerte por construcción (ningún estímulo nuevo produce 3 sorpresas); **elijo 2** porque la
misión pide *aprender en pocas exposiciones* y porque un candidato que el examen no mide es un candidato a medias.

### 2.6 Identificabilidad: qué prior queda con 8 ejemplos y por qué con 14 no hace falta (declaración, no metáfora)

| ejemplos de tren | clase de hipótesis | identificable | quién lo midió | qué predice este diseño |
|---|---|---|---|---|
| 8 | lineal en 6 px | no representa XOR | 3b (0.50), A6 | OFF ≤ 0.55 |
| 8 | lineal + **un producto** `P_i·P_j` | **no**: 9/15 con residuo 0 | A12–A14 (ideal 3/20; WTA 1–2/3) | **ESCALAR ≤ 0.65** (P4) |
| 8 | **tabla de 2 bits** sobre un par, leída por consistencia, abstención | **sí** en ≥ 19/20 | M3 (20/20 + 19/20 con desempate al azar) | **CRECE ≥ 0.875 estricta** (P1) |
| 14 | lineal + un producto (competencia) | sí: 1/15 con residuo 0 | A-6 (1.000, n\* = 200) | ESCALAR ≥ 0.90, n\* ≤ 200 (P6) |
| 14 | tabla de 2 bits | sí (redundante) | M3_NTR14 (1.000, n\* = 7) | CRECE 1.000, n\* ≤ 15 (P6) |

**Prior mínimo que queda con 8, declarado:** *el rasgo es una función arbitraria de 2 bits de dos nodos de la retina,
se elige por consistencia (menor error propio) y abstiene hacia su padre*. Lo que el crecimiento **quita** del prior de M3
es la pre-enumeración (*qué* pares existen); lo que **añade** es el criterio local de nacimiento (co-actividad en la
sorpresa). BARAJADO (P5) mide si ese criterio compra algo (exposiciones y ocupación) o es decorativo; ESCALAR (P4) mide
que el empate lo rompe la **tabla**, no el **par**. Con 14 ejemplos el producto basta (A-6) y el crecimiento sólo compra
exposiciones (200 → ≤ 15): **ahí no hace falta ningún prior** y lo que se declara es velocidad, no capacidad.

---

## 3. Por qué sale de la frontera: capacidad NUEVA y MEDIBLE

| capacidad | cómo se mide (clave del JSON) | frontera hoy | este diseño (predicción) |
|---|---|---|---|
| **Construye su propio rasgo conjuntivo** | en la sonda, el nodo que lee los patrones de test tiene padres (0,1) y **nació de una sorpresa** (`g_reclutas_t` lo registra con paso y patrón), no de fábrica | M3: 15 celdas de fábrica; fisión de v11: 0/20 | ganador (0,1) reclutado por co-actividad en ≥ 17/20 (P1) |
| **Crece sólo donde la lineal falla y se apaga sola** | `g_nodos_apriori` en xor01 / px0 / azar; sorpresas por cuarto (`g_sorp_q`); reclutas tras completar el ganador | no existe (memoria fija) | xor01 ≤ 10 de 15; px0 ≤ 5 y todos con el píxel 0; sorpresas Q2 ≤ 10 % de Q1 (P3) |
| **Exposiciones hasta asociar con 8 ejemplos** | n\* = primera mordida de tren con acc estricta ≥ 0.75 (`g_curva`) | OFF > 600; M3 7–10 (pre-enumerado) | CRECE ≤ 15 (P2) |
| **Desaprende estructura** | tras invertir la regla: mordidas hasta re-asociar; nodos podados vs sobrescritos | v15d: no se desdice; v14.1: la lineal re-aprende en decenas de mordidas | ≤ 10 mordidas, ≤ 0.5 × OFF, podas ≤ 2 (P8) |
| **Vive en el tronco sin coste** | examen v3′ 8/8 con la perilla ON (E1 "W_B ≈ −3", E2 reversión explícitas); `bateria_generaliza` ON | v15c/d/e: ninguno entró | 8/8; G1 1.000 / G2 ≥ 0.95 (P7) |

Nivel del brief que toca: **3 (no lineal)** — pasa de *"prior de pares pre-enumerado"* a *"prior de tabla de 2 bits que el
organismo instancia por sorpresa"*, con la misma letra de ERR-35 (con 8 sigue habiendo prior; con 14 no); **8 (aprendizaje
abierto)** — estructura que nace y muere por error; **4** de rebote (un nodo sobre la retina no puede tener alias: dos
patrones distintos difieren en algún píxel) — **no se declara** aquí, se anota como pregunta.

---

## 4. Preregistro (borrador para el coordinador; §4.1–4.6 escritos antes de construir nada)

### 4.1 Instrumento, mundos y semillas

`organismo_v16c` (perilla `crece`, apagada ≡ v14.1) y `organismo_v16gc` (mundo de regla, apagada ≡ v14g). Mundo de regla
con los **kwargs EXACTOS** de la entrada `'organismo_v14'` de `bateria_generaliza.py` (regla 14 / ERR-41): `eta_s=0.15,
clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1`, T = 200 000,
sonda en T/2. **Semillas:** V1 y V2a en **101–120** (las del criterio del tronco); V2b en **1101–1120** (vírgenes; cualquier
veredicto a ±1 semilla del umbral → réplica automática en **1121–1140**, regla 12). Ninguna semilla se elige mirando datos.

### 4.2 Brazos (un cambio por brazo)

| brazo | perillas sobre `organismo_v16gc` | qué mide |
|---|---|---|
| **OFF** | `crece=0` | ≡ v14.1 (identidad I3); la referencia |
| **CRECE** | `crece=1` | el candidato |
| **FIJO15** | `crece=1, g_ctrl='fijo15'` | **Occam**: las 15 de fábrica con la misma lectura y poda (= v15f de A16 dentro de este instrumento). Si rinde igual y la ocupación de CRECE no es menor, el crecimiento sobra |
| **ESCALAR** | `crece=1, g_ctrl='escalar'` | el nodo es un **producto** (una casilla) en vez de una tabla de 2 bits: ¿el empate lo rompe la tabla o el par? |
| **BARAJADO** | `crece=1, g_ctrl='barajado'` | los pares reclutados son **al azar**, no los co-activos: ¿qué compra Hebb-en-la-sorpresa? |
| **NTR14** | CRECE / ESCALAR / OFF con `ntr=(8,6)` | control de prior (ERR-35): con 14 nadie necesita prior |
| **INV** | CRECE / OFF, `regla='px0', invertir_regla_en=150000` | desaprender: sobrescribir contra re-aprender |

Reglas: `xor01` (8 tren / 12 test), `px0` (10/10), `azar` (10/10, en banda). Las tres en OFF, CRECE, FIJO15, ESCALAR y
BARAJADO; NTR14 sólo en xor01; INV sólo en px0.

### 4.3 Predicciones numéricas (todas escritas antes; umbrales fuera de la mediana esperada del efecto — ERR-37a; lo aprendido se parea por semilla, las integrales de trayectoria —ocupación, sorpresas, mordidas— se comparan por medianas y A₁₂ — ERR-37b)

| # | predicción | control | umbral que decide | qué diría que cayera |
|---|---|---|---|---|
| **P1** | **XOR con 8, prior declarado.** CRECE `acc_lenta` xor01 **estricta** mediana ≥ 0.875 y ≥ 0.75 en ≥ 16/20; **el lector en la sonda tiene padres (0,1) en ≥ 17/20** y aparece en `g_reclutas_t` (nació de una sorpresa) | OFF ≤ 0.55 (pareado CRECE > OFF ≥ 18/20); `azar` mediana ∈ [0.35, 0.65]; `px0` mediana ≥ OFF | mediana estricta < 0.75, o (0,1) < 14/20 | el reclutamiento por sorpresa no instancia el nodo correcto o la competencia no lo elige: la línea vuelve a FIJO15/v15f |
| **P2** | **Exposiciones.** n\* (primera mordida de tren con estricta ≥ 0.75) mediana ≤ 15, ≤ 30 en ≥ 15/20 | FIJO15 n\* 7–10 (referencia M3); OFF > 600 | n\* > 40 | reclutar cuesta más exposiciones de las que ahorra: el precio del crecimiento supera al de pre-enumerar |
| **P3** | **Ocupación y auto-límite.** xor01: nodos vivos en la sonda mediana ≤ 10 y < FIJO15 (15) con A₁₂ ≥ 0.90; reclutas después de que el ganador tenga sus 4 casillas ≤ 1 (mediana); sorpresas en Q2 ≤ 10 % de las de Q1. px0: nodos vivos en la sonda ≤ 5 y **todos contienen el píxel 0** en ≥ 18/20; podas ≥ 1 en ≥ 15/20. azar: acierto en banda (sin predicción de ocupación) | FIJO15 (15 fijos); BARAJADO (ocupación ≥ CRECE + 3, A₁₂ ≥ 0.75) | xor01 mediana ≥ 13, o px0 con un nodo sin el píxel 0 en ≥ 5/20 | crecer ≈ pre-enumerar con pasos de más → Occam: FIJO15 es el mecanismo, no éste |
| **P4** | **El prior mínimo es la tabla, no el par.** ESCALAR xor01 estricta mediana ≤ 0.65 y lector (0,1) ≤ 8/20 | CRECE (P1) en las mismas semillas | ESCALAR ≥ 0.80 | mi lectura de la identificabilidad (9/15 productos empatados) está mal: el producto sí selecciona con 8 y el prior declarado en §2.6 sobra |
| **P5** | **Hebb en la sorpresa compra exposiciones.** BARAJADO n\* mediana ≥ 1.5 × CRECE y ocupación ≥ CRECE + 3 (A₁₂ ≥ 0.75). **Declarado:** el acierto en la sonda puede ser igual (con 15 huecos, el azar también acaba reclutando (0,1)) | CRECE | n\* BARAJADO / CRECE < 1.2 y ocupación no mayor | la co-actividad es decorativa: el diseño se reduce a "reclutar pares al azar cuando hay sorpresa" y se dice |
| **P6** | **Con 14 no hace falta prior.** NTR14: CRECE 1.000 con n\* ≤ 15; ESCALAR ≥ 0.90; OFF ≤ 0.60 (la lineal no representa XOR) | A-6: producto + competencia 1.000 con n\* = 200 | CRECE < 0.90 con 14, o ESCALAR < 0.75 | si CRECE sube con 8 y no con 14: ajuste al régimen (ERR-35), se dice y no entra |
| **P7** | **Tronco y generalización.** V1 examen v3′ **8/8 en 101–120 con `crece=1`**, explícitos E1 "W_B ≈ −3" 20/20 y E2 "W_A → −3 / W_B → +1 / come B Q4" 20/20, 4d (E2L divide antes de 25 000) 20/20; V2a G1 ≥ 0.80 (predigo 1.000), G2 ≥ 0.85 (predigo ≥ 0.95), K 20/20; nodos en E1 ≤ 6 (mediana); mordidas de B en E1 ≥ 0.8 × v14.1 (mediana) | v14.1 (examen guardado); azar en banda | cualquier etapa < 20/20 (19/20 → regla 12) o G1 < 0.80 | la lectura exacta temprana quita mordidas a la rápida o retrasa la división: el grafo no puede vivir en la vía lenta del tronco con esta dosis (se reporta; no se recalibra) |
| **P8** | **Desaprender.** INV px0: mordidas tras la inversión hasta que la lectura lenta acierte ≥ 0.75 sobre los 20 patrones: CRECE mediana ≤ 10 y ≤ 0.5 × OFF (A₁₂ ≥ 0.80); podas tras la inversión ≤ 2 (mediana): el grafo se desdice **sobrescribiendo**, no muriendo | OFF (la lineal re-aprende) | CRECE ≥ OFF, o podas ≥ 5 | desaprende matando nodos (caro) o no desaprende: v15d otra vez, con otro nombre |

**Cláusulas fijadas ahora.** (a) Si **P1 o P7** caen, v16c **no entra al tronco**; si P3 cae por ≥ 13, entra como mucho
FIJO15 (Occam) con su propio preregistro. (b) **Muestreo (regla 10):** se reporta el conjunto completo y, al lado, el
subconjunto de semillas con ≥ 2 mordidas sorprendentes de patrones "11" antes de la sonda (las únicas donde (0,1) puede
nacer por co-actividad) y el de semillas con las 4 clases mordidas; **el conjunto completo manda**. (c) Dos puntuaciones
siempre (registro y estricta); decide la estricta. (d) Multiplicidad de empates al leer reportada; si > 1 en ≥ 3/20
semillas se reporta el subconjunto sin empates. (e) Nada se recalibra: `g_theta`, `g_rec`, `g_min_vis`, `g_rho`, `g_max`
quedan como en §2.2; toda enmienda lleva ERR (regla 11).

### 4.4 Qué me refuta, en una línea cada uno
- **P1 < 0.75:** el organismo no construye el rasgo por sorpresa; declaro que el prior debe seguir pre-enumerado (M3/v15f).
- **P4 ≥ 0.80:** mi diagnóstico de identificabilidad (tabla ≠ producto) es falso.
- **P7 E1/E2 < 20/20:** el grafo en la vía lenta rompe el tronco por el mismo canje que v15d (mordidas de la rápida) o por 4d.
- **P3 ≥ 13 y P5 sin efecto:** el crecimiento es pre-enumeración con pasos de más: Occam, FIJO15.
- **P8 ≥ OFF:** no desaprende mejor que la lineal; el "se desdice en una mordida" no llega a la conducta.

### 4.5 Dato estructural ya calculado (sin simular; `coactividad_tren_xor01.py`, salida `coactividad_tren_xor01_s1101-1140.json`)
En 1101–1140 **todas** las semillas tienen ≥ 1 patrón "11" en el tren de xor01 (mediana 2; 4/40 con uno solo): ninguna
queda excluida a priori de P1. Los pares co-activos en el tren son **12–15 de 15** (mediana 13): **la ocupación no puede
quedar baja por falta de pares** — sólo por el auto-límite (la sorpresa se apaga cuando el ganador lee) y por `g_rec`. Por
eso P3 es una predicción de mecanismo, no de mundo, y puede fallar limpio.

### 4.6 Vocabulario si pasa (y sólo entonces)
*"Cuando la vía lenta se sorprende dos veces con la misma pareja de píxeles, el organismo recluta un nodo de 2 bits sobre
ella que nace leyendo como su padre; lo lee sólo si reduce el error; con 8 ejemplos de XOR el nodo (0,1) nace de la
sorpresa y acierta los nunca vistos en ≤ 15 exposiciones (prior de tabla de 2 bits, declarado); el nodo se desdice en una
mordida y muere si deja de ayudar; el tronco no paga."* Nada de "aprende XOR", "lenguaje", "token", "entiende".

---

## 5. Coste e instrumentos (todo por anclas; congelados sólo se leen; `manifiesto.py --check` 16/16 al terminar)

| archivo (nuevo, en `experimentos/sala2_crece/`) | origen (sha) | qué es |
|---|---|---|
| `construye_v16c.py` | — | genera todo lo de abajo por sustitución de anclas (A–F, G1–G3); imprime cada ancla hallada 1 vez o aborta |
| `organismo_v16c.py` / `_on.py` | `organismo/organismo_v14.py` feefc88b1fd8d434 | el candidato; `_on` = `crece=1` por defecto (para la batería congelada) |
| `organismo_v16gc.py` / `_on.py` | `organismo/organismo_v14g.py` 1f1318480cd34cde | mundo de regla + G1–G3 |
| `bateria_v16c.py` | `organismo/bateria_v14.py` 72216f5415de0c86 | examen v3′ sobre `_on`; **lee los sha de `organismo_v11/v10` desde `organismo/`** (ERR-42) |
| `bateria_generaliza_v16c.py` | `organismo/bateria_generaliza.py` 9cf72581ebae7dea | entrada `'organismo_v16c_on'` **comparada campo a campo por el constructor** con `'organismo_v14'` (regla 14 / ERR-38): `eta_s=0.15, clip_s=10.0` explícitos + `crece=1` y los `g_*` |
| `identidad_v16c.py` | plantilla `identidad_v15e.py` | I1 24/24 · I2 2/2 · I3 6/6 · I4 ON sin excepción con `puerta_pat=5` en 12 escenarios · I5 `g_curva` on/off idénticas salvo la curva (2 semillas, xor01) · I6 FIJO15 ≠ CRECE (debe fallar) · I7 `crece=1, g_max=0` ≡ v14.1 salvo claves nuevas. **Todo 100 % o no se corre nada** |
| `corre_v16c.py` | plantilla `corre_v15e.py` | subprocesos SECUENCIALES: identidad → V1 (`bateria_v16c.py 20 --desde 101 --log`) → V2a (`bateria_generaliza_v16c.py organismo_v16c_on 20 --desde 101 --log`) → V2b (Pool aquí) → umbrales de §4.3 y JSON; `--humo` de UN proceso; regla 10 (log desde el arranque, `datos/` desde el primer minuto); regla 11 (lista los python vivos antes del Pool); **humo que llegue a ESCRIBIR su JSON** antes de la serie (ERR-42) |
| `PREREGISTRO_v16c.md` | este §4, firmado por el coordinador antes de correr | — |

**Pool y tiempo de pared (estimación con los tiempos medidos de la mañana, ~8 s por 100 000 pasos con la máquina cargada,
Pool(14)):** V1 180 corridas × 100k ≈ 2 min · V2a 40 × 200k ≈ 1 min · V2b: 5 brazos × 3 reglas × 20 = 300 corridas × 200k
≈ 6 min; NTR14 60 × 200k ≈ 1.5 min; INV 40 × 200k ≈ 1 min → **≈ 12 min por serie; réplica 1121–1140 otros ≈ 10 min**.
Un solo `Pool` a la vez (v15e primero; este bloque después). Identidad: un proceso, ≈ 5 min. Humo (coordinador o
implementador, UN proceso, ≤ 6 corridas): E1/E2 s101 ON (W, lineal, nodos, mordidas de B por trimestre) + xor01/px0/azar
s1101 ON/OFF. Gemelo numba: sólo tras el veredicto (compilador de mundos; arnés 100 % obligatorio, regla 9).
**Coste en tokens de agentes:** un implementador (constructor + arnés + humo) y un auditor; la sala no vuelve a abrirse.

**Orden:** constructor → arnés → preregistro firmado → humo → V1 → V2a → V2b → réplica si regla 12 → registro (cronista) →
gemelo → decisión del director (la entrada al tronco es suya).

---

## 6. Humo y espejos: cómo podría engañarnos y cómo lo evito

| espejo | dónde ya nos engañó | cómo lo cierro aquí |
|---|---|---|
| **Desempate por índice** (el índice 0 *es* (0,1)) | A13 (17/20 falso), ENJAMBRE §4.1 (la semilla insignia de M3) | la lectura desempata por **boleto de nacimiento** aleatorio (rng propio), nunca por índice; se reporta la multiplicidad; el orden de reclutas empatados también es al azar |
| **Fuga en la sonda** (leer test antes de tiempo) | vigilado en M3 (la sonda se toma antes de `tipos.extend`) | `g_curva` y la sonda son **lecturas puras** (I5: on/off bit a bit); los patrones de test no existen en el mundo hasta `fase2_en`; `azar` en banda es el detector de fuga en todos los brazos |
| **Acierto por abstención** (medio punto) | ENJAMBRE §2 (M3 registro 0.81 / estricta 0.625) | dos puntuaciones siempre; decide la **estricta**; la abstención va **al padre** (lineal), así que no hay 0 exacto por diseño salvo lineal 0 |
| **Doble cuenta** (la lenta lee más que R) | v15d (1.45·R → E1/E2 0/20) | **relevo**, no suma; cada vía con su error; V1 mide E1 "W_B ≈ −3" y E2 explícitos; humo con mordidas de B por trimestre |
| **Residuo que hereda el fracaso de la lineal** | v15e (xor01 0.25, gana (2,4)) | la casilla guarda **R crudo**; el error propio del nodo es contra R, no contra el residuo |
| **Un examen que no mide al candidato** | B-5 (inerte en el tronco), v15c (V1 con la perilla apagada) | §2.5: actúa en el tronco (2 sorpresas); la batería examina `_on`; se reporta `g_reclutas` por etapa; si saliera 0 en E1, se dice y la evidencia es sólo el mundo de regla |
| **Batería copiada con "defaults"** | ERR-38 (`eta_s=0` en la copia), ERR-41 (kwargs tipo v13), ERR-42 (JSON perdido) | entrada comparada campo a campo por el constructor; kwargs exactos en V2b; humo que escribe JSON; sha desde `organismo/` |
| **Constantes afinadas mirando datos** | M2 (`fis_umbral` sin ERR), M4 (`rho` 0.05 → 0.02 mirando) | §2.2 fija las cinco con argumento antes del humo; `g_rho = 0.02` es el valor ya publicado por la búsqueda ciega de M4; cambio = ERR |
| **Umbral en la mediana del efecto; pareado de integrales** | ERR-37a/b | umbrales alejados; ocupación/sorpresas/mordidas por medianas y A₁₂; sólo lo aprendido se parea |
| **Ocupación baja por el mundo, no por el mecanismo** | — | §4.5: 12–15 pares co-activos en el tren; si la ocupación sale baja es por el auto-límite, y P3 lo mide con reclutas-tras-ganador y sorpresas por cuarto |
| **Muestreo** (clase sin morder) | A6, cláusula de M3 | subconjuntos preregistrados (regla 10); el completo manda |
| **Vocabulario inflado** ("grafo", "token", "lenguaje") | regla 6 de EQUIPO | §2.1 y §4.6: lo que se declara es lo que se mide; "grafo" aquí = padres explícitos + una arista recorrida; nada más |
| **El crecimiento como pre-enumeración disfrazada** | — | FIJO15 en el mismo instrumento (Occam); P3 y P5 lo deciden |

**Lo que no puedo saber hasta correr (dicho ahora):** si `g_rec = 2` deja demasiadas sorpresas en E2L y retrasa la
división (4d); si en px0 algún nodo inconsistente lee en la sonda antes de que un conflicto lo delate (G1 < 1.000: por eso
el umbral es la letra, 0.80); si BARAJADO empata con CRECE en acierto (declarado) y en exposiciones (no declarado: sería
P5 caída); si la ocupación en xor01 se acerca a 13 (P3 caída: Occam manda).

---

*Archivos de esta sala (todos nuevos, ninguno del repo tocado, sin commits):* `registro/investigacion/sala2/DISENO_crece_codigo.md`
(este), `coactividad_tren_xor01.py`, `coactividad_tren_xor01_s1101-1140.json`.
