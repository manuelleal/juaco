# ENCARGO NUBE — ECO_SEL LARGO: ¿la selección sigue subiendo o se estanca? (28-sep-2026, coordinador, aprobado por el director)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas). El método manda sobre el cómo. Principio del director: que la evolución construya el órgano, no nosotros.

## 0. Contexto (leer primero)
- `NUBE.md` (entorno, Pool 3, `/root/venv-juaco/bin/python`, presupuesto), `CLAUDE.md` y `registro/EQUIPO.md`.
- Rama base: **`organelos`** (commit `0860d26` o posterior). Trabaja en la rama nueva **`nube/eco-sel-largo-20260928`**, en
  `experimentos/organelos/eco_sel_largo/`.
- **Hito del 28-sep:** ECO_SEL = FUNCIONA ×2 en M y en C. Ver:
  - la última entrada de `registro/REGISTRO_etapas_1_2.md`;
  - `experimentos/organelos/eco_sel/PREREGISTRO_eco_sel.md`, `corre_eco_sel.py`, `nucleo_eco_sel.py` e `identidad_eco_sel.py`.

  Resultado: en el linaje de F1 frío (ECO w90, sin vivero ni fundadores repuestos), la selección natural sube la capacidad de carga
  K (media de vivos en [T/2, T]) con T = 1e6:
  - F1: ~31 → SEL_M (margen `rep_umbral` heredable): ~35 → SEL_C (15 genes del cerebro heredables): ~39;
  - 20/20 ×4 contra F1;
  - el mismo gen sin herencia (AZA) queda por debajo de F1;
  - descriptivo: en SEL_C, las muertes por veneno + sal caen de 82 % a 2–3.5 %.

## 1. Preguntas (dos, con veredictos separados)
- **L (larga):** con 10× más tiempo (T = 1e7), ¿K sigue subiendo, o se estanca en el valor de T = 1e6?
  Es la pregunta de evolución abierta: si hay techo o no.
- **MC (combinado):** si mutan a la vez el margen y el cerebro (16 genes; la historia de vida, salvo `rep_umbral`, sigue fija),
  ¿K supera a SEL_C sola?

## 2. Diseño mínimo (el creador puede ajustarlo y lo declara en el preregistro)
- Reutiliza el núcleo, la genética y el carro de `eco_sel/` **sin cambios**. Sólo agrega:
  - el brazo `SEL_MC`: muta `rep_umbral` + los 15 del cerebro, con herencia;
  - el brazo `AZA_MC`: lo mismo sin herencia (`donante='azar'`);
  - T = 1e7;
  - telemetría por ventanas de 1e6 pasos: K por ventana, media y cuantiles de cada gen en vivos, y causas de muerte por ventana.
- **Brazos:** `F1`, `SEL_C`, `SEL_MC` y `AZA_MC`. Si el presupuesto alcanza, también `SEL_M`.
- **Arnés:**
  - con T = 1e6, los brazos compartidos (F1, SEL_C) == `eco_sel` bit a bit (mismas claves);
  - `SEL_MC` con σ = 0 == F1;
  - `AZA_MC` no hereda (el caso H de ERR-149: sólo hijos de padre no fundador);
  - determinismo;
  - shas fijados antes de correr.
- **Costo:** ~20–30 s por corrida a 1e6 en el PC, así que a 1e7 son ~3–5 min por corrida en la nube. Con 4 brazos × 20 semillas y
  Pool 3, ~1.5–2.5 h por serie.

## 3. Puertas sugeridas (el creador las fija en el preregistro ANTES de la serie; umbral cambiado después = ERR, regla 11)
- **L-1 (sigue subiendo):** en `SEL_C`, K de la última ventana [9e6, 1e7] > K de la ventana [0.5e6, 1e6], en ≥ 15/20 semillas, con
  mediana de la diferencia ≥ +2 cuerpos.
- **L-2 (no es deriva):** lo mismo NO se cumple en `AZA_MC`; es el control que puede fallar.
- **MC-1:** K(`SEL_MC`) > K(`SEL_C`) en la ventana final, en ≥ 15/20 semillas, con mediana ≥ +1.5.
- **MC-2:** K(`SEL_MC`) > K(`AZA_MC`) en ≥ 15/20.
- **Validez:**
  - F1 persiste ≥ 17/20;
  - frío limpio (0 refundados);
  - genética la declarada;
  - bloqueados = 0 (si se alcanza el tope de cuerpos, esa semilla es NO EVALUABLE; decláralo).
- **Veredictos:** FUNCIONA / HAY ALGO MODESTO / NO / NO EVALUABLE para L y para MC por separado, con la misma lógica que `eco_sel`.
- **Descriptivo obligatorio:**
  - la curva de K por ventana (mediana y cuantiles por brazo);
  - qué genes se mueven y cuándo;
  - las causas de muerte por ventana.

## 4. Protocolo (obligatorio)
1. Construcción, arnés N/N y humo de 1 proceso.
2. **`PREREGISTRO_eco_sel_largo.md` escrito y commiteado ANTES de la serie**, con predicción numérica y p.
3. **Semillas nuevas:** propuesta 45401–45420 (serie) y 45421–45440 (réplica), humo 45491–45499. **Grep en el repo y en las ramas
   remotas antes de usarlas.**
4. Serie con Pool 3. **Réplica si la serie no da NO** en alguna de las dos preguntas.
5. Auditor (solo lectura) antes de la serie, y otra vez sobre el resultado: que recalcule K desde los JSON.
6. **Registro:** INFORME.md con el veredicto en una línea primero; REGISTRO, HANDOFF y la línea para CLAUDE.md. Commit y push a
   `nube/eco-sel-largo-20260928`, y **pull request contra `organelos` sin mergear**.

## 5. Límites
- No tocar el tronco congelado ni `frio/`, `juaco_eco/` o `eco_sel/` (sólo importar). Nunca `manifiesto.py` sin `--check`.
- A lo sumo un creador (Opus) y un auditor. Nada de enjambres: cuida el crédito.
- Vocabulario: prohibidos "aprende", "evoluciona" sin la medida, "especie" y "entiende". Permitido: "la selección natural sube K",
  con la medida al lado.
- El siguiente ERR libre es **ERR-150** (verifícalo en `registro/`).
- Decisiones difíciles: tómalas y escríbelas con hora, opción tomada, alternativa descartada y porqué.

## 6. Entregable
`experimentos/organelos/eco_sel_largo/INFORME.md` con:
- veredicto L y veredicto MC;
- tabla por brazo;
- la curva de K por ventana;
- la tabla de genes por ventana;
- errores de instrumento declarados.

Además, rama empujada y pull request contra `organelos`.
