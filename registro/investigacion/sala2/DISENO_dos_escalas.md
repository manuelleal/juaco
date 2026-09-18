# DISEÑO — sala 2, ángulo «dos escalas»: v16 = v14.1 + tabla episódica con relevo (v15f) + CONSOLIDACIÓN LENTA (la casilla que gana se vuelve palabra de la regla) + APRENDER SIN MORDER (el episodio enseña a la regla en cada encuentro)

**Creador de la sala 2 (ángulo dos_escalas), 18 sep 2026, ~10:00.** Misión primero: llegar a la AGI por este camino — un organismo
mínimo con reglas locales, sin retropropagación en el runtime, que aprende, desaprende, generaliza, sobrevive y se reproduce, con
evidencia preregistrada. Primero la frontera; segundo, que viva.

**Reglas cumplidas.** No edité ningún archivo del repo; este es el único archivo que creé. No corrí el organismo ni ningún `Pool`
(hay uno vivo). Leí, además de las fuentes del encargo, los datos de v15e que terminaron a las 09:36 (`datos/v15e_s141-160_20260918_092921`,
`examen_v15e_20260918_093053`, `regresion_generaliza_v15e_organismo_v15e_on_20260918_093352`) y el humo de **v15f** del creador A
(`datos/v15f_humo_20260918_094706`, 09:47–09:50; `PREREGISTRO_v15f.md` 09:50), que es la base literal de este diseño. Dos cálculos
estructurales de sólo lectura (reparto tren/test de `split_regla`, sin simular un paso). Lo que digo "derivado del código" lo digo así.
Este documento **no es un preregistro**: es el diseño y el preregistro *propuesto* para que el coordinador lo convierta en bloque.

---

## 0. La respuesta en una página

**Qué bloquea (mi lectura).** El organismo tiene dos memorias de valor con **una sola constante de tiempo cada una** y **sin puente
entre ellas**: la rápida (Kenyon, 0.09 del error por mordida, ≈ 24 mordidas) y la lenta (lineal en 6 px, 0.45 por mordida). Toda la
línea XOR de la mañana añadió una tercera —la tabla de pares que escribe de un golpe— y cada versión perdió una mitad: v15d identifica y
no se desdice (E1 0/20, E2 0/20), v15e se desdice y no identifica (E2 20/20, xor01 0.500 con (0,1) ganando 20/20), v15f (humo 09:47:
xor01 1.000, E1/E2 sí) recupera las dos… **y sigue sin puente**: lo que la tabla sabe no llega nunca a la regla salvo por las mismas
mordidas de siempre, y cuando el episodio se pierde (60 casillas sobrescritas por 20 patrones, o una muerte que borre) la regla sabe lo
que las mordidas le enseñaron en ~150 exposiciones (A-4), no lo que la tabla aprendió en 7. Y los 5 740 encuentros por corrida con veneno
`00` en los que hoy no se aprende nada (PLAN (3)) siguen sin usarse.

**Qué propongo (una línea, tres piezas locales, apagada ≡ v14.1 bit a bit).**
1. **Escala 1 — episodio:** la tabla de pares de v15f tal cual (R crudo, sobrescritura, relevo a la lineal cuando la casilla no se vio,
   cada vía con su error). Es el *nodo* del director: "sal es sal, número uno, lo guardo".
2. **Escala 2 — consolidación:** cuando la competencia entre las 15 celdas está **decidida** (una única ganadora durante `consolida = 10`
   mordidas seguidas), el par ganador se vuelve **una entrada más de la regla lineal** (`P_i·P_j`, dos canales, la misma regla delta, el
   mismo drenaje y tope). Es la *palabra*: lo que el episodio identificó queda en la regla, y sobrevive al episodio.
3. **Aprender sin morder:** en cada **encuentro sin mordida** de un patrón cuyo código exacto ya se mordió (el token existe en `ncod`,
   memoria que ya tiene v14.1), la regla lineal (+palabra) da un paso delta hacia lo que la tabla guarda para ese patrón. No entra
   información nueva (C8 tiene razón: la única fuente es la mordida); entra **repetición sin morder**: la regla se consolida con los
   encuentros, no con los bocados.

**Capacidad NUEVA y medible.** *Conserva lo que el episodio enseñó cuando el episodio ya no está*: en xor01 con 8 ejemplos, la lectura de
la vía lenta **sin la tabla** (lineal + palabra, leída en la misma sonda a priori) acierta ≥ 0.75 en los nunca vistos, donde v14.1 da
0.44 y la tabla sola (v15f) volvería a 0.44 al perderla; y lo logra con **la mitad de mordidas** que sin replay. Todo lo demás (E1/E2,
G1/G2, xor01 con tabla, n\* 7–12) lo hereda de v15f y se re-mide con la misma letra. Vocabulario si pasa: *"la regla lenta se queda con
el par que el episodio identificó, y lo aprende de los encuentros sin morder"*. Prohibido: "aprende XOR" (sigue siendo prior de pares),
"lenguaje", "entiende".

**Lo que me tumba.** (a) `acc_sin_tabla` xor01 < 0.65 de mediana → la palabra no sostiene XOR sin la tabla: las dos escalas no se
conectan con esta regla. (b) `n*_lineal` con replay ≥ 0.8 × sin replay → el replay no compra mordidas (la refutación de C8 se generaliza).
(c) `azar` fuera de [0.35, 0.65] en la lectura sin tabla → el replay por token filtra valores ajenos: fuga. (d) V1 con un subcriterio
≤ 18/20 → el canje "el que acierta a la primera no repite" es real y se reporta.

---

## 1. Qué bloquea, con evidencia del registro

| # | bloqueo | evidencia (archivo, entrada, número) | qué toca este diseño |
|---|---|---|---|
| B1 | **Dos memorias, una lectura: cada candidato de la tabla de pares perdió una mitad.** | v15d `suma`: xor01 0.875, G1 1.000 pero E1 0/20, E2 0/20 (lee 1.45·R, la rápida se queda sin mordidas; registro 08:38). v15e: E2 **20/20**, E1 W_B≈−3 20/20, G1 1.000, pero xor01 **0.500** [0.06, 0.88] con (0,1) ganadora **20/20** (`v15e_s141-160`: la identificación está resuelta; lo que falla es la LECTURA lineal + residuo). v15f (humo s141): R crudo + relevo → xor01 **1.000/1.000**, ba 0.999, (0,1); E1/E2 s101–102 pasan salvo "venenoQ4<Q1" en s101. | Parte de v15f sin cambiar una línea suya. |
| B2 | **No hay puente entre el episodio y la regla.** La lineal sólo aprende en `if mordio:` (L107) con su error (L117–120); la tabla también. Lo que la tabla identifica en 7 mordidas la regla lo necesita en 150–200 (A-4: 1.000 con rasgos dados a 150 exposiciones; A-6: 14 ejemplos, n\* 200). Sin puente, "consolidación" no existe: la tabla es la única que sabe XOR, y es una tabla de 60 casillas sobrescribibles. | La palabra (escala 2) y el replay. |
| B3 | **5 740 encuentros por corrida en los que no se aprende nada** (PLAN (3), creador A). C8 midió que la codificación predictiva no baja mordidas (1.59 ×) porque "la consolidación redistribuye lo que las mordidas ya enseñaron"; correcto y exactamente lo que aquí se pide: redistribuir del episodio a la regla. DIAG_metodo (bloqueo 2) lo formula como suelo duro: no baja de una mordida por estímulo. Este diseño no baja ese suelo (una mordida por token sigue haciendo falta); baja las mordidas **de la regla**. | Replay en el encuentro. |
| B4 | **La frontera declarada** (HANDOFF 15.8.7): "construir el rasgo desde píxeles sin prior sigue sin mecanismo". Cerrado por ERR-35: con 8 ejemplos 9 de 15 hipótesis empatan; el prior de pares (M3) rompe el empate. **Nadie ha hecho que el prior se vuelva rasgo permanente de la regla.** | La palabra: el prior elige, la regla se lo queda. Sigue siendo prior de pares; se declara así. |
| B5 | **El canje del que acierta a la primera** (A §6a): leer R exacto tras una mordida aplana la curva de Q1 y quita mordidas a la rápida. v15e: E1 "venenoQ4<Q1" **19/20** (s110: 14 = 14), E2I "W_C≤−2.5" **19/20** (s102: −2.41, C mordida 18 veces). v15f humo: s101 venQ4<Q1 NO (mordidas B [2,16,14,9]; v14.1 [27,11,8,1]). DIAG_dinamica B3: el examen castiga por una semilla al que aprende rápido. | No lo resuelve (la rápida no se toca). Lo declara, lo mide (mordidas de C Q3+Q4 y `comp['C']` ON/OFF) y deja la regla 12 como única salida. |
| B6 | **Retención de lo ausente 0.67** (mundo largo; A-2 refutada) y **la muerte no borra nada** (DIAG_mundo bloqueo 1: `E=.6` y sigue). Sin una segunda escala que retenga sin el episodio, "que viva" —herencia, población— no tiene qué heredar que no sea todo o nada. | La sonda "sin tabla" es la primera muerte medible de UNA memoria: lo que queda es lo heredable. |
| B7 | **Método:** tres runners copiados en `creacion_A/` trajeron tres defectos en una hora (ERR-41, ERR-42 y el candidato ERR-43 de DIAG_metodo §2.3: `corre_v15e.py` L199 leyó `azar 20.000` y marcó V2a NO cuando la batería dijo PASA G1 1.000 / G2 0.997). | Instrumentos por anclas desde v15f (no desde cero); el runner copia el booleano de la batería y aborta si difiere. |

**La hipótesis del director, traducida a lo que este ángulo mide.** *"Sal es sal, número uno, lo guardo"* = la casilla (par, combinación)
escribe R crudo de un golpe la primera vez (M3/v15f). *"Sal rosa lo vectoriza, marca como sal y lo plantea como variable de lo mismo"* = un
patrón nunca visto que comparte la combinación del par ganador **lee el nodo antes de morder** (relevo): eso es la predicción de la
consecuencia sin morder, y es lo que M3 mide como 1.000 en los 12 nunca vistos. *"Grafo, no vector"* = la lectura autoritativa es el nodo
discreto; el vector (lineal) es el soporte cuando no hay nodo, **y** el sitio donde el nodo recurrente se consolida como palabra.
*"Aprender y desaprender"* = sobrescritura en una mordida en el nodo (v15e/v15f: E2 20/20) y regla delta en la palabra; la diferencia de
velocidad entre las dos escalas es medible (n\* de la tabla ≈ 7–12; n\*_lineal con replay, a medir). Lo que NO se afirma: que esto sea
lenguaje. B-4 midió que en el mundo del tronco "el parecido contradice el valor"; por eso aquí la variante se define por **combinación
del par ganador**, no por parecido de píxeles, y en `azar` debe fallar (control).

---

## 2. Mecanismo, por anclas sobre `organismo/organismo_v14.py` (feefc88b1fd8d434, sólo lectura)

### 2.1 Las tres lecturas de la vía lenta y el error de cada una

| lectura | qué devuelve | aprende de | cuándo la usa la boca (con la puerta de v14.1 intacta) |
|---|---|---|---|
| **tabla** (episodio) | R crudo de la casilla del par ganador para P | R de la propia mordida (sobrescritura) | patrón no familiar y casilla vista |
| **lineal + palabra** (regla) | `(Wps−Wns)@P + (Wpf−Wnf)·P_i·P_j` | su propio error `R − regla(P)` al morder; y `R_tabla(P) − regla(P)` en encuentros sin morder de tokens conocidos | patrón no familiar y casilla NO vista; y siempre en la sonda "sin tabla" |
| **rápida** (Kenyon) | `(Wp−Wn)@kenyon(P)` | su propio error `R − _wf` (L115, sin tocar) | patrón familiar (`_fam`, L58–60, sin tocar) |

### 2.2 Estado nuevo y constantes

| pieza | estado | constante | argumento (no barrido) |
|---|---|---|---|
| tabla de pares (v15f) | `_MMv` 15×4 (R crudo), `_MNv` 15×4 (visitas), `_MEv` 15 (error propio, EMA), `_MGv` (ganadora) = 135 números | `mem_rho = 0.02` | el de M3 (sala, `rho = 0.02` en el top-10 de la búsqueda ciega de M4) |
| consolidación | `_MWv` (racha de victorias únicas de la misma celda: 1 entero), `_FEAT` (par consolidado: 1 entero o None), `Wpf, Wnf` (2 flotantes) | `consolida = 10` racha; `F_max = 1` (estructural) | 10 ≈ n\* de M3 (7–10): a esa altura la competencia ya está decidida; una sola palabra por vida en este bloque |
| replay | ninguno (usa `ncod`, que ya existe) | `replay = 1`; tasa = `eta_s` (sin constante nueva) | la misma regla y tasa que la lineal ya usa |
| instrumento (sólo lectura) | `curva` (sonda periódica), `n_replay`, `n_consolida`, `t_consolida`, `sobrescrituras_cruzadas` | `sonda_cada = 2000`; `borrar_en = None` | C8 sondeó cada 2 000; `borrar_en` sólo en el brazo de lesión |

Total nuevo respecto de v14.1: 135 + 4 números y cuatro perillas apagadas por defecto. Nada en la rápida, la puerta, la hija dispersa, `KW`, `Wl`.

### 2.3 Pseudocódigo por anclas

**A1–A6 son las anclas de v15f** (`experimentos/creacion_A/construye_v15f.py` → `organismo_v15f.py` 96fc5c5262107850; identidad 32/32 medida
09:48). Las repito en una línea cada una para que el constructor de v16 parta de ellas; **A7–A10 son nuevas**. `PP` = `PAT` en el tronco,
`P_` en el mundo de regla (`organismo_v14g.py` 1f1318480cd34cde). Todo lo nuevo vive bajo `if memoria_pares is not None` o bajo perillas
que por defecto valen `None`/`0`, y **ninguna línea nueva consume el rng con la perilla apagada**.

```
FIRMA   ...,pat_shuf=0,pat_min=1):  →  ...,pat_shuf=0,pat_min=1,memoria_pares=None,mem_rho=0.02,consolida=0,replay=0,sonda_cada=None,borrar_en=None):
        (mundo de regla: idem sobre ",pat_shuf=0,pat_min=0):")
```

**A1 (L50, estado)** ancla `Wps=np.zeros(6); Wns=np.zeros(6)   # v13: via LENTA...` → tras ella:
```
_PARv=[(i,j) for i in range(6) for j in range(i+1,6)]                       # 15 celdas = pares
_MMv=zeros(15,4); _MNv=zeros(15,4); _MEv=full(15,1e9); _MGv=0                # v15f
_MWv=0; _FEAT=None; Wpf=0.0; Wnf=0.0; n_cons=0; t_cons=None                 # v16: palabra
n_replay=0; cruz=0; curva=[]                                                 # v16: sólo lectura
def _cas(c,P): i,j=_PARv[c]; return int(P[i])*2+int(P[j])
def _feat(P): return 0.0 if _FEAT is None else float(P[_PARv[_FEAT][0]]*P[_PARv[_FEAT][1]])
def _regla(P): return float((Wps-Wns)@P) + ((Wpf-Wnf)*_feat(P) if _FEAT is not None else 0.0)   # lineal + palabra
def _tabla(P): c=_cas(_MGv,P); return (True,float(_MMv[_MGv,c])) if _MNv[_MGv,c]>0 else (False,0.0)
def _lenta(P):
    if memoria_pares is None: return float((Wps-Wns)@P)      # la expresión literal de v14.1 (identidad)
    v,r=_tabla(P); return r if v else _regla(P)              # RELEVO: nodo si lo conoce, regla si no
```
**A2 (L63, `valor()`)** `_s=float((Wps-Wns)@P)` → `_s=_lenta(P)`.
**A3 (L101, mordida)** `_ws=float((Wps-Wns)@PP[kk])` → `_ws=_lenta(PP[kk])`.
**A4 (L117, error de la lineal)** `_ds=dlt if puerta is None else R-_ws` → `_lb=_regla(PP[kk]) if memoria_pares is not None else _ws; _ds=dlt if puerta is None else R-_lb`
(apagada: `_lb == _ws`, misma expresión, bit a bit).
**A5 (L119–120, paso de la lineal)** las dos líneas `Wps=np.clip(...)`/`Wns=np.clip(...)` quedan; **inmediatamente después**, bajo la perilla:
```
if memoria_pares is not None:
    if _FEAT is not None and _feat(PP[kk])>0:                  # la palabra aprende con la MISMA regla, drenaje y tope
        m=min(Wpf,Wnf); Wpf-=lam*m; Wnf-=lam*m
        if _ds>0: Wpf=min(Wpf+eta_s*_ds,clip_s)
        else:     Wnf=min(Wnf+eta_s*aversion*(-_ds),clip_s)
    P=PP[kk]
    for c in range(15):                                        # v15f: error propio de la CASILLA sola (criterio M3), R crudo, sobrescritura
        k=_cas(c,P); pred=_MMv[c,k] if _MNv[c,k]>0 else 0.0; e=R-pred
        _MEv[c]= e*e if _MNv[c].sum()==0 else (1-mem_rho)*_MEv[c]+mem_rho*e*e
        if _MNv[c,k]>0 and _MMv[c,k]*R<0: cruz+=1              # v16 lectura: otra combinación con otro signo pisó esta casilla
        _MMv[c,k]=R; _MNv[c,k]+=1
    mn=_MEv.min(); emp=where(_MEv<=mn+1e-12)
    g=emp[0] if len(emp)==1 else emp[rng.integers(len(emp))]   # desempate al azar: consume rng SÓLO con la perilla ON y empate real
    _MWv = _MWv+1 if (len(emp)==1 and g==_MGv) else (1 if len(emp)==1 else 0)   # v16: racha de victorias ÚNICAS
    _MGv=g
    if consolida and _FEAT is None and _MWv>=consolida:        # v16: CONSOLIDACIÓN — la competencia está decidida
        _FEAT=_MGv; Wpf=Wnf=0.0; n_cons+=1; t_cons=t
```
**A6 (L164, return)** añade, bajo la perilla (None si apagada): `mem_ganadora, mem_tabla, mem_vistas, mem_cobertura, mem_err_tabla, W_tabla,
palabra=(_PARv[_FEAT] o None), W_palabra=(Wpf,Wnf), n_consolida, t_consolida, n_replay, sobrescrituras_cruzadas, curva, W_regla={k:_regla(P)}`.

**A7 (L106, el encuentro sin mordida) — APRENDER SIN MORDER.** Ancla `if memoria_rechazo and not mordio: _rech[pos]=t+memoria_rechazo`;
tras ella:
```
if memoria_pares is not None and replay and learn and eta_s and not mordio and _ev(kc)>=1:   # token conocido (ncod, memoria de v14.1)
    v,rt=_tabla(PP[kk])
    if v:                                                      # el nodo tiene qué enseñar; la regla da SU paso hacia él
        dr=rt-_regla(PP[kk]); n_replay+=1
        [el mismo bloque de A5 para Wps/Wns y para la palabra, con dr en lugar de _ds: drenaje lam, eta_s, clip_s]
```
Local: ve la retina presente, su tabla y su propia lectura. No toca la rápida, no toca `ncod`, no consume rng. En `plast=False`/`eta_s=0`
no actúa (mismas guardas que la lineal).

**A8 (línea `if invertir_en is not None and t==invertir_en: ...`) — LESIÓN DEL EPISODIO (instrumento).**
```
if borrar_en is not None and t==borrar_en: _MNv[:]=0; _MEv[:]=1e9; _MWv=0     # la tabla se pierde; la palabra y la lineal quedan
```
**A9 (mundo de regla, `organismo_v14g.py` L113–116, `W_apriori={...}` antes de `tipos.extend(test)`) — LA SONDA SIN TABLA.** Junto a `W_apriori` (valor total, como hoy) se leen, sólo lectura:
`W_apriori_regla={k:_regla(P_[k])}`, `W_apriori_tabla={k:(_tabla(P_[k])[1] si vista else None)}`, `ganadora_sonda`, `empate_sonda`, `palabra_sonda`.
**A10 (línea `if log_cada and t%log_cada==0:`) — CURVA.** `if sonda_cada and mundo!='AB' and t<fase2_en and t%sonda_cada==0:
curva.append((t, mordidas_tren_acumuladas, acc_estricta(valor, test), acc_estricta(_regla, test)))` — sólo lectura; de ahí `n*` (con tabla)
y `n*_lineal` (sin tabla) en **mordidas de patrones de entrenamiento** hasta la primera sonda ≥ 0.75.

### 2.4 Apagado ≡ v14.1 bit a bit, y qué se predice con la perilla ENCENDIDA en el tronco

- `memoria_pares=None`: `_lenta` es la expresión literal de v14.1; A4 usa `_ws`; A5/A7/A8/A9/A10 no se ejecutan; ninguna línea nueva toca
  el rng → **I1 24/24 ≡ v14.1, I2 rng no consumido 2/2, I3 6/6 ≡ v14g con los kwargs exactos del tronco** (el arnés de v15f, 32/32, se
  copia y se amplía).
- **I4 (inercia predicha, se mide, no se supone):** con la perilla ON en el tronco, la consolidación **no actúa** en E1, E2, E2J, E2K, E2L,
  CTRL, CTRL2 (`n_consolida = 0` en 140/140): A y B sólo comparten casilla en el par (0,5), así que **14 celdas empatan a error exactamente
  igual** (misma aritmética, mismas visitas) y nunca hay ganadora única. Derivado del código y del arnés de v15f (ganadora [1,2] y [2,5]
  en dos semillas: cambia al azar). En E2I / E2I-misma la celda (2,3) queda **única** desde la primera mordida de C (C y B comparten esa
  casilla con la misma valencia: error 0; las otras 13 reciben una casilla nueva: +9·0.02; (1,4) hereda la de A con valencia opuesta: +16·0.02)
  y **se consolida** ~10 mordidas después; su producto `P2·P3` vale 0 en A, B y C → la palabra es silenciosa: `W_regla[k] == W_lenta[k]`
  para A, B, C dentro de la misma corrida (se mide: `n_consolida = 1` y esa igualdad, 20/20). En E2J/E2K la D comparte 6 casillas con B
  con valencia opuesta (error 16) y ninguna con A: las 8 restantes empatan → `n_consolida = 0`.
- El replay SÍ actúa en el tronco (tokens conocidos rechazados: B con hambre baja) y empuja la lineal hacia lo que la tabla ya dice
  (−3 para B, +1 para A): no cambia la lectura de la boca (que lee la tabla o la rápida).

### 2.5 Lo que NO hay
Suma ni residuos (v15e), tasa de sobrescritura, decaimiento de la tabla, más de una palabra, cambio en la rápida / puerta / hija dispersa /
`KW` / `Wl`, retorno aleatorio, ninguna constante buscada tras ver datos.

---

## 3. Por qué sale de la frontera: la capacidad nueva, medible

| capacidad | v14.1 | v15f (tabla sola) | **v16** | cómo se mide |
|---|---|---|---|---|
| XOR con 8 ejemplos, con el episodio | 0.44 | 1.000 (humo s141) | = v15f | `acc` estricta de `W_apriori` en los 12 nunca vistos |
| **XOR con 8 ejemplos, SIN el episodio** (lo que queda cuando la tabla se pierde) | 0.44 | **≈ 0.44** (la lineal) | **≥ 0.75** | `acc` estricta de `W_apriori_regla`; y brazo `borrar_en` (conducta al primer encuentro sin tabla) |
| mordidas de la regla hasta 0.75 sin tabla | > 600 (8 ej.); 150 con rasgos dados | no aplica | **≤ 0.5 × sin replay** | `n*_lineal` de `curva` |
| se desdice | rápida ≈ 24 mordidas + hambre; lineal 2–4 | nodo: 1 | nodo 1; regla por replay sin morder | E2 (letra) + `W_lenta` al final |
| encuentros sin mordida que mueven un valor | **0 por construcción** (DIAG_dinamica §4) | 0 | **miles** (`n_replay`) | contador |

Es la primera vez que el organismo **conserva** una regla no lineal después de perder la memoria que la identificó, y la primera vez que un
encuentro sin mordida cambia un valor. En términos del brief: nivel 3 (no lineal) deja de depender de una tabla de 60 casillas; nivel 4
(memoria persistente) gana una segunda escala; nivel 8 (retención de lo ausente) gana el instrumento que le faltaba (la lesión de una
memoria). En términos del director: el nodo se escribe de un golpe, la variante lo lee sin morder, y la palabra —lo que el nodo identificó—
pasa a la regla y **es lo heredable**. "Que viva" empieza donde una muerte puede borrar la tabla y el hijo se queda con la palabra: eso
no se corre aquí (mundo de población, DIAG_mundo bloqueo 1), pero por primera vez hay qué heredar que no sea todo.

Honestidad de la frontera: **no** sale del prior de pares (ERR-35 sigue: con 8 ejemplos nadie selecciona sin prior). Sale de "el prior vive
en una tabla" a "el prior elige y la regla se queda con lo elegido". Y "aprender sin morder" aquí es transferencia entre escalas, no una
fuente de información nueva (DIAG_metodo bloqueo 2 sigue en pie: eso exige otra consecuencia observable o otro organismo).

---

## 4. Preregistro propuesto (para que el coordinador lo fije antes de correr)

**Brazos del mundo de regla** (`organismo_v16g`, kwargs EXACTOS del tronco, regla 14; T = 200 000, sonda en T/2):
OFF (`memoria_pares=None` ≡ v14.1) · TABLA_SOLA (`'relevo'`, consolida 0, replay 0 ≡ v15f) · SIN_REPLAY (consolida 10, replay 0) ·
**ON** (consolida 10, replay 1) · CONS_SHUF (ON, pero la palabra es un par **al azar distinto de la ganadora**, `Generator` propio `seed+800000`,
sólo en xor01) · REPLAY_SHUF (ON, pero el replay enseña la R de **otra casilla vista** al azar, mismo `Generator`, sólo en xor01) ·
ON+BORRAR (`borrar_en = fase2_en − 1`, sólo en xor01). Reglas px0, xor01, azar. **Semillas 181–200** (vírgenes en el mundo de regla: 41–160
gastadas; 161–180 las usa v15f); réplica 201–220.
**Examen y generalización:** `bateria_v16.py` (← `bateria_v14.py` 72216f5415de0c86, sobre `organismo_v16_on`, sha de v11/v10 desde
`organismo/`) y `bateria_generaliza_v16.py` (← 9cf72581ebae7dea, entrada campo a campo = tronco) en **101–120** (la letra del tronco).
**Cláusula de muestreo (calculable antes):** en 181–200 los 40/40 repartos xor01 tienen ≥ 1 patrón `11` en el tren (la palabra `P0·P1`
sólo aprende su peso en ellos) y 39/40 tienen ≥ 1 `00`; la semilla sin `00` se reporta aparte (regla 10), no se excluye.

| # | predicción (umbral) | mi número | refutación (qué diría) |
|---|---|---|---|
| **P1** examen v3′ ON, 101–120 | **8/8**, con E1 "W_B≈−3", E2 reversión (3 sub), E2J/E2K/E2L, 2, 3′, 3″, 4a–4d a la letra 20/20 | como v15e (E2 20/20, W_B 20/20); **E1 "venenoQ4<Q1" y E2I "W_C≤−2.5": 19–20/20** (declarado: v15e 19/20 y 19/20; v15f humo 1/2) | 19/20 en uno → regla 12 (réplica 121–140, misma letra); **≤ 18/20** → el canje "acierta a la primera y no repite" es real: se reporta con `mordidas de C Q3+Q4` y `comp['C']` ON/OFF; no se parchea |
| **P2** generalización ON, 101–120 | G1 ≥ 0.80, G2 ≥ 0.85, K 20/20, azar en banda | G1 1.000 (v15e 1.000), G2 ≥ 0.97 (v15e 0.997) | < umbral → la palabra o el replay dañan la lineal (P6 dirá cuál) |
| **P3** xor01 CON tabla (ON) | ESTRICTA mediana ≥ 0.75; (0,1) ganadora en la sonda ≥ 18/20; `n*` ≤ 20 mordidas de tren | 0.85–1.00 (v15f s141 1.000; v15c/d 0.81–0.88); (0,1) 20/20; n\* 7–12 | < 0.75 → v15f no replica en serie: el relevo no basta (techo por alias de la puerta) |
| **P4 (la nueva)** xor01 SIN tabla | `acc` estricta de `W_apriori_regla`: **mediana ≥ 0.75 y ≥ 0.75 en ≥ 16/20** (ON); palabra = (0,1) en ≥ 16/20; `t_consolida` ≤ 40 mordidas de tren (mediana); TABLA_SOLA ≤ 0.55 de mediana | ON 0.80–0.90; TABLA_SOLA 0.44 (= OFF); CONS_SHUF ≤ 0.60 | **mediana < 0.65 o < 12/20** → la palabra no sostiene XOR sin la tabla; las dos escalas no se conectan con esta regla. Si CONS_SHUF ≥ ON → la palabra no es lo que importa (fuga por el replay) |
| **P4b** conducta sin tabla (ON+BORRAR) | `ba` al primer encuentro ≥ 0.65 (mediana); y `mord` Q1–Q2 **idénticos** a ON en 20/20 (pre-lesión bit a bit) | 0.70–0.85; identidad 20/20 | ba < 0.55 → el valor se conserva pero la boca no lo usa (fallo de política, regla 4); identidad < 20/20 → instrumento roto (`borrar_en` toca algo antes de t) |
| **P5** aprender sin morder | `n*_lineal` ON ≤ **0.5 ×** SIN_REPLAY (mediana; pareado ≥ 14/20); `n_replay` ≥ 1 000 por corrida (mediana) | 40–80 contra 150–300 (A-4: 150 con rasgos dados; C8: 995 encuentros / 104 mordidas) | **≥ 0.8 ×** → el replay no compra mordidas: C8 se generaliza a la tabla como maestra; `n_replay` < 200 → los tokens rechazados no existen como se creía (trampa 3 al revés) |
| **P6** controles | px0: ON ≥ OFF (mediana registro; pareado ≥ 16/20), `acc` sin tabla ≥ 0.90 (la lineal de v14.1), palabra consolidada en px0 ≤ 3/20 (empate de 5 celdas (0,j)); **azar ∈ [0.35, 0.65] en las TRES lecturas** (con tabla, sin tabla, `ba`) en ON; REPLAY_SHUF: `acc` sin tabla xor01 ≤ 0.60 | px0 1.000/1.000/0 consolidaciones; azar 0.45–0.55; REPLAY_SHUF 0.45 | px0 sin tabla < 0.90 → daño a la lineal; palabra en px0 > 3/20 → la consolidación no espera a que la competencia se decida (reescribir A5, ERR); **azar fuera de banda** → fuga (el replay por token enseña valores de variantes ajenas: siguiente candidato = replay sólo por casilla propia, preregistro nuevo) |
| **P7** inercia en el tronco (ON) | `n_consolida = 0` en E1/E2/E2J/E2K/E2L/CTRL/CTRL2 (140/140); en E2I y E2I-misma `n_consolida = 1` con palabra (2,3) en ≥ 18/20 y `W_regla[k] == W_lenta[k]` (A, B, C) en 20/20 (palabra silenciosa) | 140/140; E2I (2,3) 20/20, silenciosa | > 0 donde se predijo 0, o palabra ≠ (2,3) en E2I, o `W_regla ≠ W_lenta` → la regla de racha no significa "competencia decidida" (o la palabra no es silenciosa): ERR y reescritura antes de leer P4 |
| **P8** coste (V4) | px0: celdas y `splits` ±10 % de OFF; xor01: por abajo no refuta, por arriba se cuenta (v15e +9 % / +18 %); muertes pareadas no peores en px0 | xor01 celdas ±10 %, splits ≤ +20 %; muertes ≈ OFF | no decide la entrada; se pesa |

**Cláusula.** Si P1 o P2 caen (≤ 18/20 en cualquier subcriterio, o G1/G2 bajo umbral), v16 no entra al tronco. Si P3 cae, la base (v15f)
no replica y v16 no se lee. **P4 es lo que se declara** (y P5 lo que lo explica); P6–P7 son los controles que pueden tumbarlo. Un 19/20 en
cualquier umbral → réplica automática (regla 12) en 201–220 (regla) / 121–140 (examen). Sin modos intermedios; `consolida = 10`,
`mem_rho = 0.02`, `F_max = 1`, replay a `eta_s` quedan fijados aquí; todo cambio posterior lleva ERR.
**Vocabulario si pasa:** *"la regla lenta se queda con el par que el episodio identificó y lo aprende de los encuentros sin morder; sin el
episodio sigue acertando los nunca vistos"*. **Prohibido:** "aprende XOR", "construye el rasgo sin prior", "lenguaje", "entiende".

---

## 5. Coste e instrumentos

| pieza | origen (sha, sólo lectura) | qué cambia | identidad |
|---|---|---|---|
| `construye_v16.py` → `organismo_v16.py` / `_on` | `organismo_v14.py` feefc88b1fd8d434 (A1–A6 copiadas de `construye_v15f.py`; A7, A8, A10 nuevas) | firma + 4 anclas nuevas | I1 24/24 ≡ v14.1; I2 rng 2/2 |
| `organismo_v16g.py` / `_on` | `organismo_v14g.py` 1f1318480cd34cde (+ A9) | sonda sin tabla, curva, borrar | I3 6/6 ≡ v14g con kwargs del tronco |
| `bateria_v16.py` | `bateria_v14.py` 72216f5415de0c86 sobre `_on`; sha v11/v10 desde `organismo/` (ERR-42) | sólo el módulo | humo que ESCRIBE el JSON antes de la serie (regla 14) |
| `bateria_generaliza_v16.py` | `bateria_generaliza.py` 9cf72581ebae7dea | UNA entrada, **campo a campo** = `'organismo_v14'` (regla 14 / ERR-38) | verificada por el constructor |
| `identidad_v16.py` | `identidad_v15f.py` | + I4 inercia ON en E1 (P7: `n_consolida = 0`, T = 30 000, 2 semillas) + I5 ON+BORRAR ≡ ON en `mord` antes de `borrar_en` (2 semillas) | 32/32 + 2 + 2 = 36/36 exigidas |
| `corre_v16.py` | `corre_v15f.py` | brazos de §4; **copia el booleano del JSON de cada batería y aborta si su relectura difiere** (ERR-43) | `--humo` un proceso |
| `analiza_v16.py` | nuevo | `acc` sin tabla, n\*, n\*_lineal, pareados, desde los JSON (regla 10) | — |

**Pool (uno a la vez, coordinador):** identidad 3 min (un proceso) · V1 examen ≈ 3 min · V2a ≈ 1 min · V2b: 4 brazos × 3 reglas + 3 brazos × xor01
= 300 corridas de T = 200 000 ≈ 22 min con Pool(14) · total ≈ 30 min; réplica igual. **Personas/agentes:** un implementador (2–3 h: partir de
`construye_v15f.py`, no de cero), un auditor (30 min: anclas, regla 14, rng), el coordinador. **Memoria del organismo:** +139 números.
**Gemelo numba:** después, si entra. **Orden respecto de la cola:** v15f primero (es la base y ya está montado: `corre_v15f.py`); v16 sólo
si v15f pasa P3 (xor01 ≥ 0.75) — si v15f cae por px0 < OFF, v16 hereda el mismo fallo y no se corre sin rediseño del relevo.

---

## 6. Humo y espejos: cómo podría engañarnos y cómo se evita

1. **Rigging por índice.** `(0,1)` es el índice 0 de `_PARv`; un empate resuelto por orden le regala la victoria (A §A13: un 17/20 falso).
   Desempate al azar con el rng (v15f) y reportar `empate_sonda`; la racha de consolidación exige ganadora **única**: un empate nunca
   consolida, ni por índice ni por azar.
2. **Fuga de test a la sonda.** La sonda se toma **antes** de `tipos.extend(test)` (`organismo_v14g.py` L113–116): las casillas que leen los nunca
   vistos las escribieron sólo patrones de tren. `W_apriori_regla` se lee en el mismo instante. Verificable: `mem_vistas` ≤ casillas de los
   8 de tren.
3. **La lesión que no lesiona.** `borrar_en` sólo pone `_MNv` a 0: la palabra y la lineal quedan. Se comprueba (P4b) que `mord` Q1–Q2 de
   ON+BORRAR es idéntico a ON; y que el número offline (`W_apriori_regla` en ON) y el online (`W_apriori` en ON+BORRAR) coinciden en ≥ 18/20
   (dos lecturas del mismo objeto; si difieren, instrumento roto).
4. **"Aprender sin morder" como si fuera información nueva.** No lo es (C8); lo que se mide es `n*_lineal` (mordidas de la **regla**),
   no exposiciones hasta asociar del organismo (ese suelo sigue en una mordida por token). El vocabulario lo dice.
5. **La palabra que aprende de la tabla equivocada.** En `azar` la tabla lee mal las variantes; si el replay filtra eso a la lineal, `azar`
   sin tabla cae fuera de banda → se declara fuga. REPLAY_SHUF y CONS_SHUF separan "es la palabra correcta" de "es cualquier palabra".
6. **Prior disfrazado de aprendizaje.** Sigue siendo prior de pares (ERR-35). El control NTR14 no hace falta aquí (la línea está cerrada);
   la declaración es "el prior elige y la regla se lo queda", nunca "aprende XOR".
7. **El examen que castiga al rápido.** E1 "venenoQ4<Q1" y E2I "W_C≤−2.5" pueden caer por una semilla por la propia mecánica (B5). Se
   predice antes (19–20/20), se aplica la regla 12, **no se enmienda la letra** desde este bloque (DIAG_dinamica B3 propone la batería de
   exposiciones; es otra decisión, del director, con ERR).
8. **Instrumentos copiados.** Regla 14 completa: entrada campo a campo, humo que escribe JSON, kwargs del tronco en el mundo de regla
   (ERR-41), runner que copia el booleano de la batería (ERR-43 candidato). Semillas vírgenes en el instrumento donde se usan.
9. **Constantes.** `consolida = 10` y `mem_rho = 0.02` se fijan aquí con argumento; ningún brazo barre constantes; si P7 cae (consolida
   donde no debía), se reescribe la regla con ERR, no la constante.
10. **La semilla insignia.** Ninguna corrida de un proceso decide nada: el humo de v15f (s141) es una semilla; P3/P4 se leen sólo en 20 + 20.
11. **Dos organismos con filas idénticas hasta el último decimal** (ERR-38): TABLA_SOLA y ON deben diferir en `W_apriori_regla` en xor01;
    si no difieren, la palabra/replay no actuaron (perilla mal cableada) y se para antes de leer.

---

## 7. Lo que abre si pasa (sin predicción, no es parte del bloque)
- **Muerte que borra una memoria** (DIAG_mundo bloqueo 1): `olvido_muerte` de la Etapa 4 aplicado sólo a la tabla; lo heredable es la
  palabra + la lineal. Es la forma mínima de "el hijo hereda la regla, no el episodio" para el mundo de población.
- **Mundo vivo:** tabla y palabra por necesidad (una fila por `n_nec`, como `Wps`), por anclas sobre `organismo_vivo.py`; la sal rosa
  (DIAG_representacion 4.6) es la variante natural de la casilla.
- **Más de una palabra** (`F_max` 2–3) en un mundo con dos reglas conjuntivas: si la segunda racha única aparece tras el cambio de regla, la
  regla se desdice también en su vocabulario.

**Fuentes:** `organismo/organismo_v14.py` (L50, L58–63, L101–107, L115–121, L164) · `organismo/organismo_v14g.py` (L125–128) ·
`experimentos/creacion_A/{construye_v15e.py, organismo_v15e.py, PREREGISTRO_v15e.md, PREREGISTRO_v15f.md, identidad_v15e.py, corre_v15e.py}` ·
`datos/v15e_s141-160_20260918_092921`, `examen_v15e_20260918_093053`, `regresion_generaliza_v15e_…_093352`, `v15f_humo_20260918_094706` ·
`registro/REGISTRO_etapas_1_2.md` (ERR-35 → ERR-42; XOR 07:43/07:47; v15c/v15d; B-5; mundo vivo) · `ENJAMBRE_xor_20260918.md` (M3, §4) ·
`PUENTE_creacion.md` (A12–A16, B-4, B-5, C8/C-P5) · `HANDOFF.md` §13, §15.7–15.8 · `PLAN.md` (05:10, 06:45, 07:10) · `EQUIPO.md` 1–14 ·
`sala2/DIAG_{dinamica,metodo,mundo,representacion}.md` y `sala2/coactividad_tren_xor01_s1101-1140.json` (dato estructural; aquí recalculado para 181–200).
