# ENCARGO NUBE — ECO_SEL LARGO: sólo verificar, correr, auditar y registrar (28-sep-2026, creador en el PC, para el coordinador)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas). El método manda sobre el cómo. Principio del director: que la evolución construya el órgano, no nosotros.

Reemplaza la parte de CONSTRUCCIÓN de `experimentos/organelos/eco_sel/ENCARGO_NUBE_largo.md`: **el instrumento ya existe y está
preregistrado.** Esta sesión NO diseña, NO construye y NO cambia ni una letra del preregistro. Sólo verifica, corre, audita y registra.

## 0. Qué hay y de dónde sale
- La construcción la hizo una sesión de la nube el 28-sep (20:40–21:07 UTC) en la rama **`nube/eco-sel-largo-20260928`**, commit
  **`c08dc32`** (base `organelos` 87d82b2), carpeta `experimentos/organelos/eco_sel_largo/`:
  - `construye_eco_sel_largo.py` 65b5d9f5b5f98f73 → `nucleo_eco_sel_largo.py` 69f2b652ac46cd1b (por anclas B1–B10 desde
    `eco_sel/nucleo_eco_sel.py` 6a36e47ce61db3e1);
  - `corre_eco_sel_largo.py` 69db795b7d952d93 (runner y letra);
  - `identidad_eco_sel_largo.py` 277e42c5f8f535e9 (arnés; salida de la nube e8c54bf85cb8660d: **65/65**);
  - **`PREREGISTRO_eco_sel_largo.md` 9a7f1029c7dc8b61**, commiteado y empujado ANTES de toda serie (21:07 UTC). Es la letra.
- **Auditoría en el PC (28-sep, 17:00–17:20 hora local, creador; copia extraída con `git archive`, sin tocar el repo):**
  - `--verifica` de los dos constructores: IGUAL.
  - Arnés de la nube corrido en el PC (Windows, Python 3.14.2, con el sustituto de `resource` de §5): **65/65** en 442 s; su salida
    (`auditoria_pc/identidad_eco_sel_largo_salida_PC.txt`, d582ac7a8074beef) == la de la nube línea por línea salvo hora, versión de
    Python, segundos y el sha del preregistro (que la nube completó después del arnés, como declara su §11).
  - **(X1) cruce de máquina:** el humo de la nube (45491, T 200 000, 5 brazos) repetido en el PC == el JSON de la nube en TODAS las
    claves de las 5 corridas salvo `seg`.
  - **(X2) ancla contra datos commiteados:** SEL_C, semilla 45301, T = 1e6, con el núcleo LARGO == el JSON commiteado de la serie de
    eco_sel (`eco_sel/datos/eco_sel_serie_s45301-45320/SEL_C_s45301.json`) en TODAS sus claves salvo `seg`; la única clave nueva es
    `ventanas`; K 39.489 == 39.489.
  - Semillas 45401–45440 y 45491–45499: grep en el árbol local y en las 10 ramas remotas (`*.py *.md *.txt *.log` y nombres de
    archivo): sólo aparecen en el encargo, en el paquete de esta rama y en su humo. Libres.

## 1. Pasos (en este orden; si uno falla, te detienes y lo escribes)
1. `git fetch && git checkout nube/eco-sel-largo-20260928 && git pull`. Si ya existe `experimentos/organelos/eco_sel_largo/datos/eco_sel_largo_serie_s45401-45420/`
   con JSON, **no se relanza nada desde cero**: se sigue con `--reanuda` (sólo corre lo que falta).
2. `git merge origin/organelos` (commit de merge, sólo agrega; no toca `eco_sel_largo/`, y los orígenes `frio/`, `eco_sel/`,
   `juaco_eco/`, `generaciones/` no cambiaron entre 87d82b2 y a46d53c: verificado con `git diff --stat`). Sirve para que el PR no choque.
3. Python: `/root/venv-juaco/bin/python` en TODOS los comandos (3.13.12, numpy 2.4.3, numba 0.67.0). Pool = 3.
4. Verificar el paquete (sin esto no hay serie):
   ```
   P=/root/venv-juaco/bin/python; D=experimentos/organelos/eco_sel_largo
   sha256sum $D/*.py $D/PREREGISTRO_eco_sel_largo.md | cut -c1-16     # deben dar los shas de §0
   $P $D/construye_eco_sel_largo.py --verifica                         # IGUAL
   $P $D/identidad_eco_sel_largo.py                                    # RESULTADO: 65/65 (~5 min)
   ```
   El arnés reescribe `identidad_eco_sel_largo_salida.txt`; compara con la de c08dc32 (salvo horas y segundos). Si no da 65/65: alto.
5. Serie (en segundo plano, con log; latido cada 5 min en `progreso.log`):
   ```
   nohup $P $D/corre_eco_sel_largo.py --serie --desde 45401 --n 20 --pool 3 > $D/serie_pool3.log 2>&1 &
   ```
   - Cada ~60 min: `git add $D/datos/eco_sel_largo_serie_s45401-45420/*.json $D/datos/eco_sel_largo_serie_s45401-45420/progreso.log`
     (**nunca** la carpeta `ckpt/`: son pickles de 3–15 MB), commit y push. Si la sesión se corta, la siguiente hace `git pull` y
     relanza la misma línea con `--reanuda`.
   - Al terminar, el runner imprime VEREDICTOS L y MC y escribe `RESUMEN.json`.
6. **Réplica** si la serie NO da NO en alguna de las dos preguntas: lo mismo con `--desde 45421`. Si las dos dan NO, no hay réplica.
7. Auditor (un agente, sólo lectura) sobre el resultado: recalcula desde los JSON, sin importar el runner, K base
   (media de `tam_total[500:1001]`), K final (`tam_total[9000:10001]`, relleno con 0 si se extinguió), dK, los conteos pareados de
   L-1/L-2/L-3 y MC-1/MC-2, V1, V2, V3 y bloqueados; y compara con `RESUMEN.json`. Cualquier diferencia se escribe.
8. Registro (ver §3) y **pull request contra `organelos`, sin mergear**.

## 2. Costo (medido; para planear la noche)
- PC (Windows, CPU compartida con otras series del coordinador: tiempos pesimistas): SEL_C a T = 1e6 = 45.4 s (arnés) y 49.8 s (X2);
  en la serie de eco_sel con Pool 6, 44.2 s. Nube (su arnés, CPU compartida): SEL_C 41.5 s, F1 32 s a 1e6.
- Relación de costo entre brazos (humo de la nube a 2·10⁵): SEL_C 1 · SEL_MC 1.0 · F1 0.87 · SEL_M 0.81 · AZA_MC 0.69 → 4.4 SEL_C por semilla.
- A 1e7 la población es estacionaria: el costo por paso es constante; el checkpoint crece con t (blob 2.6–4.1 MB a ≤ 1e6, ≈ 13–20 MB a
  1e7, `guarda` 0.005–0.024 s a ≤ 1e6) y suma < 5 %.
- **SEL_C a 1e7 en la nube ≈ 4–7 min** (PC ×10 ÷ 1.3–2.2, o nube ×10). **Serie (100 corridas, Pool 3) ≈ 2–3.5 h; réplica igual;
  total ≈ 4–7 h** más 5 min de arnés.
- Memoria: 224 MB pico por proceso a 1e6 (PC); a 1e7 crecen `filas`/`coh`/`gen_t` (≈ 175 000 nacidos): < 1 GB por trabajador. Cabe.
- Disco: JSON ≈ 0.25 MB a 1e6 → **≈ 0.8 MB a 1e7** (260 filas de `gen_t`): ≈ 80 MB por serie, ≈ 160 MB serie + réplica. Se commitean
  (son los datos; el auditor recalcula K desde ellos).

## 3. Registro sin conflictos
- El PC está editando `registro/` hoy (otros creadores activos). Por eso, igual que NUBE.md §2b: **no edites** `registro/REGISTRO_etapas_1_2.md`,
  `registro/HANDOFF.md`, `registro/ESTADO.md` ni `CLAUDE.md`. Escribe:
  - `experimentos/organelos/eco_sel_largo/INFORME.md`: primera línea = veredicto L y veredicto MC (FUNCIONA / HAY ALGO MODESTO / NO /
    NO EVALUABLE, por la letra, serie y réplica); tabla por brazo (K base, K final, dK, persistencia); la curva de K por ventana; la
    tabla de genes por ventana; veneno + sal por ventana; lo que dijo el auditor; errores de instrumento; y, al final, **las líneas
    listas para pegar** en REGISTRO, HANDOFF y CLAUDE.md.
  - `registro/NUBE_BITACORA_20260928_eco_sel_largo.md`: hora, comando, sha y veredicto de cada paso; decisiones con porqué.
- **Numeración de ERR (hallazgo de la auditoría):** el §11 del preregistro llama **ERR-150** al caso de arnés «σ = 0 == F1» (genes
  enteros). En `organelos`, **ERR-150 ya está usado** (T-C ii del examen v14.4c, commit e7a4394; el siguiente libre es ERR-151). No
  edites el preregistro (cambia su sha): en INFORME y bitácora escribe «el ERR-150 de c08dc32 es el **ERR-151** de organelos (colisión de
  numeración; el coordinador lo confirma)».
- Vocabulario: prohibidos «aprende», «evoluciona» sin la medida, «especie», «entiende», «evolución abierta» como logro. Permitido: «la
  selección natural sube K», con la medida al lado; «sigue subiendo / se estanca», con la ventana.

## 4. Límites
- Nada de diseño nuevo ni de brazos nuevos; los umbrales son los del preregistro 9a7f1029c7dc8b61 (cambiar uno después = ERR, regla 11).
- No tocar el tronco congelado, `frio/`, `juaco_eco/` ni `eco_sel/`; nunca `manifiesto.py` sin `--check`.
- A lo sumo un agente auditor; nada de enjambres.
- Decisiones difíciles: tomarlas y escribirlas con hora, opción tomada, alternativa descartada y porqué.

## 5. Lo que la auditoría del PC deja anotado (no bloquea; decláralo en el INFORME)
- **Portabilidad:** el arnés y `--humo` importan `resource` (sólo Unix). En Windows fallan al importar; en el PC se corrieron con un
  módulo sustituto por PYTHONPATH que sólo lee la memoria pico. `--serie` y `--lee` no lo importan. En la nube no afecta.
- **Letra, sesgo menor declarado:** una semilla con `bloqueados` cuenta como fallo en toda puerta, también en L-2a (el control «AZA_MC
  NO sube»), donde excluirla favorece a la hipótesis. E15 da `bloqueados` > 0 en p = 0.03: si ocurre, el INFORME dice en qué brazo y
  recalcula L-2a con la semilla contada como «sube».
- **SEL_M es descriptivo pero entra en la validez:** un aborto o un bloqueo de SEL_M anula o recorta la serie entera (la letra exige
  los 5 brazos). Es conservador; se declara.
- **Dato previo, para leer L con cuidado (JSON commiteados de eco_sel, 40 semillas, ventanas de 10⁵):** SEL_C llega a ≈ 38.7 en
  2·10⁵ y sube lento hasta ≈ 39.3 en 1e6 (K[0.9–1e6] − K[0.5–0.6e6] > 0 en 25/40, mediana +0.14); F1 plano (18/40, −0.25). Si la
  subida es logarítmica, dK de 1e6 a 1e7 ≈ +0.5–1: L-1b (+2) es difícil y MODESTO es el resultado más probable si hay subida.
