# ENCARGO NUBE — ¿la selección encuentra el termostato sola? (28-sep-2026, coordinador, aprobado por el director)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas). El método manda sobre el cómo. Principio del director: que la evolución construya el órgano, no nosotros.

## 0. Contexto (leer primero)
- `NUBE.md` (entorno, Pool 3, `/root/venv-juaco/bin/python`, presupuesto), `CLAUDE.md`, `registro/EQUIPO.md`.
- Rama base: **`organelos`** (commit `556b297` o posterior). Trabaja en una rama nueva **`nube/termo-evo-20260928`** y en esta carpeta.
- `experimentos/organelos/boca_buena/INFORME.md` y `carros/HIBB.py`: en la pista de la carrera, v14.3 (V143) se queda en R0 real ~0.41–0.63.
  Le basta una pieza de boca, un **termostato**, para cruzar: sobre lo bueno ya conocido, muerde si alguna necesidad que la letra sube está bajo
  una consigna `S = rep_umbral + margen`. El margen decide:
  - margen 0 → 0.000, extinción en 10/10 semillas;
  - margen 0.10 → 0.921;
  - margen 0.25 (el de O1) → 0.928;
  - margen 0.40 → 0.951;
  - leer la necesidad equivocada → 0.000–0.106.
  - Todo EXPLORATORIO (semillas 39001–39010).
- En el PC, el mismo día, se corre la serie confirmatoria de TERMO (margen puesto a mano, s/2), semillas 39101–39140. **No uses esas semillas.**

## 1. Pregunta
Si el margen deja de ser una constante de diseño y pasa a ser un **gen heredable con mutación**, ¿la selección natural lo lleva sola a la
banda que funciona (≈ 0.10–0.45) y con eso el linaje cruza el R0 real de 0.90, partiendo de márgenes letales o casi letales?

## 2. Diseño mínimo (el creador puede ajustarlo y lo declara en el preregistro)
- **Carro EVO**, construido sobre `HIBB` en modo termostato, igual que `m10`/`m40`: lo desconocido y lo malo los decide V143. La única
  diferencia es que el margen es un valor `g` por cuerpo:
  - el fundador lo sortea de una distribución inicial;
  - el hijo hereda `g` del padre más una mutación gaussiana chica (σ declarada, por ejemplo 0.03), recortada a [−0.2, 1.0];
  - sin memoria nueva aparte de `g`.
- **Distribución inicial:**
  - brazo principal `EVO_BAJO`: g ~ U[−0.10, 0.10], centrado en la zona letal;
  - brazo `EVO_ANCHO`: g ~ U[−0.10, 0.60].
- **Control `EVO_SINHER`:** misma física, pero el hijo NO hereda; sortea `g` de nuevo de la distribución inicial. Así no hay selección
  acumulable.
- **Anclas:** `v143` (base), `m40` (techo diseñado) y `o1` (techo).
- **Primero hay que averiguar cómo nace un hijo en la pista** (`carrera/`, la `pista` que usa `corre_muro2.py`): dónde se entera el carro de
  un parto padre→hijo.
  - Si el carro guarda estado por cuerpo, se hereda por cuerpo.
  - Si NO hay forma de heredar padre→hijo sin tocar la pista, **no toques la pista**. Declara la unidad heredable que sí exista (por ejemplo,
    el linaje/carro que se refunda) y justifica que sigue siendo selección y no diseño. Si ni eso existe, detente y reporta.
- **Medidas:**
  - principal: R0 real (juez `cruza_real`, igual que el muro);
  - la trayectoria de `g` (media y cuantiles de `g` en cuerpos vivos y en padres que parieron, por ventana de tiempo);
  - pareados por semilla contra v143 y contra el control.
- **Duración:** T 100 000 como el muro. Si el presupuesto alcanza, una T 300 000 en el brazo principal para ver más generaciones.

## 3. Protocolo (obligatorio, `registro/EQUIPO.md`)
1. **Construcción.** El carro EVO; el arnés de identidad:
   - EVO con σ = 0 y g fijo = 0.40 **==** HIBB `m40`, bit a bit;
   - EVO_SINHER == EVO en el primer fundador;
   - determinismo;
   - el sha de cada carro se fija ANTES de correr.
2. **Humo** de un proceso.
3. **`PREREGISTRO_termo_evo.md`, escrito y commiteado ANTES de la serie.** Debe incluir:
   - predicción numérica con p;
   - las puertas:
     - EVO cruza (mayoría de linajes con R0 real ≥ 0.90 en ≥ 15/20 semillas);
     - EVO le gana a EVO_SINHER en ≥ 15/20;
     - la media de `g` en padres sube desde la zona letal y termina dentro de [0.10, 0.60];
   - validez: o1 gana, v143 en rango, la pieza actúa.
4. **Semillas:** usa un rango nuevo; propuesta 41001–41020 (serie) y 41021–41040 (réplica). **Antes de usarlas, haz grep en el repo para
   confirmar que no chocan.**
5. **Serie** con Pool 3. **Réplica** en semillas nuevas si la serie no da NO.
6. **Registro** con veredicto FUNCIONA / HAY ALGO MODESTO / NO / NO SE LEE, en una línea primero: REGISTRO, HANDOFF, y la línea para
   CLAUDE.md. Después commit y push a la rama `nube/termo-evo-20260928`.

## 4. Límites
- No tocar el tronco congelado ni la pista. Nunca `manifiesto.py` sin `--check`.
- A lo sumo un creador (Opus) y un auditor. Nada de enjambres: cuida el crédito.
- Vocabulario: "evoluciona" sólo con la medida de `g` al lado. Nada de "especie" ni "entiende".
- Umbral cambiado tras ver datos = ERR numerado (regla 11). El siguiente ERR libre, según `CLAUDE.md`, es ERR-149.
- Decisiones difíciles: tómalas y escríbelas con hora, opción tomada, alternativa descartada y porqué.

## 5. Entregable
`experimentos/organelos/termo_evo/INFORME.md` con:
- el veredicto en una línea;
- tabla por brazo;
- la curva de `g` (tabla por ventana de tiempo);
- errores de instrumento declarados.

Además, rama empujada y pull request contra `organelos`, sin mergear.
