# ENCARGO NUBE — TERMO_BANCO: el linaje guarda su germoplasma (28-sep-2026, creador → coordinador; lo aprueba el director)

Misión: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas). El método manda sobre el cómo. Principio del director: que la evolución construya el órgano, no nosotros.

**Tu trabajo es sólo EJECUTAR:** verificar el arnés, correr la serie y (si toca) la réplica, registrar y abrir un PR contra `organelos`.
**No diseñes, no cambies código, letra ni semillas.** Todo está construido, preregistrado y con los shas fijados.

## 0. Antes de empezar
- Lee `NUBE.md` (entorno, Pool 3, `/root/venv-juaco/bin/python`), `CLAUDE.md` y `registro/EQUIPO.md`.
- Lee **`experimentos/organelos/termo_banco/PREREGISTRO_termo_banco.md`** entero. La letra está en su §6 y en `corre_banco.lee_serie`.
- Rama base: **`organelos`**, en el commit donde el coordinador subió `experimentos/organelos/termo_banco/` con el preregistro.
  Trabaja en una rama nueva **`nube/termo-banco-20260928`**.
- **Condición:** el preregistro (§0) dice que es el **intento n.º 5 contra el muro**, posterior a la declaración de MURO MAPEADO. Si el
  commit del coordinador no dice que el director lo autorizó, **detente y reporta** sin correr la serie.

## 1. Verificar (un proceso; si algo no da OK, DETENTE y reporta: no corras la serie)
```
/root/venv-juaco/bin/python experimentos/organelos/termo_banco/trae_nube.py --verifica
/root/venv-juaco/bin/python experimentos/organelos/termo_banco/construye_banco.py --verifica
/root/venv-juaco/bin/python experimentos/organelos/termo_banco/identidad_banco.py > experimentos/organelos/termo_banco/identidad_banco_salida_nube.txt 2>&1
```
- La última línea del arnés debe ser `ARNES PASA`, con las mismas comprobaciones OK que `identidad_banco_salida.txt` (la del PC, Python
  3.14.2). En el PC tardó ~10 min; en la nube debería tardar menos.
- Humo (un proceso, 6 corridas, T 20 000, semillas de práctica; NO cuenta):
  `/root/venv-juaco/bin/python experimentos/organelos/termo_banco/corre_banco.py --humo`
  Debe terminar con 0 abortos y con la regla 14 OK. Compara sus números con los del humo del PC (`humo_salida.txt`): con numpy 2.4.3 los
  bits deben ser idénticos. Si difieren, detente y reporta.

## 2. Serie (Pool 3)
```
/root/venv-juaco/bin/python experimentos/organelos/termo_banco/corre_banco.py --serie --desde 42001 --n 20 --pool 3 2>&1 | tee experimentos/organelos/termo_banco/serie_pool3.log
```
- Son 120 corridas (6 brazos × 20 semillas, T 100 000). Tiempo estimado: **~2 h** (la serie de TERMO_EVO, del mismo tamaño, tardó 7 194 s).
- Si se corta, relanza con `--reanuda` (salta las corridas que ya tienen su JSON).
- El veredicto sale en la última línea del log (`VEREDICTO DE LA SERIE: ...`) y en `datos/banco_s42001-42020_T100000_<sello>/resumen.json`.

## 3. Réplica (SÓLO si la serie NO dio NO; regla de parada, preregistro §7)
```
/root/venv-juaco/bin/python experimentos/organelos/termo_banco/corre_banco.py --serie --desde 42021 --n 20 --pool 3 2>&1 | tee experimentos/organelos/termo_banco/replica_pool3.log
/root/venv-juaco/bin/python experimentos/organelos/termo_banco/corre_banco.py --bloque <resumen serie>.json,<resumen replica>.json
```
- Otras ~2 h. Si la serie da NO, **no corras la réplica**, aunque sobre tiempo.

## 4. Registrar (en este orden; el veredicto en una línea primero)
- `experimentos/organelos/termo_banco/INFORME.md`. Toma como modelo `origen_nube/INFORME.md` (el de TERMO_EVO) y pon:
  - el veredicto en una línea (FUNCIONA / HAY ALGO MODESTO / NO / NO SE LEE) y el vocabulario (S);
  - la tabla por brazo: R0 real, semillas con mayoría, linajes que cruzan, fundadores, vida;
  - los pareados, y la curva de `g` de `banco`, `bancobar` y `evo`;
  - los fundadores por origen (inicial, banco propio, banco ajeno);
  - las predicciones B1–B13 del preregistro contra el resultado;
  - los errores de instrumento declarados.
- `registro/REGISTRO_etapas_1_2.md` (entrada nueva al final), `registro/HANDOFF.md` y la línea para `CLAUDE.md`.
- Umbral o letra cambiada tras ver datos = ERR numerado (regla 11). El siguiente libre, según `CLAUDE.md`, es **ERR-153**; confírmalo
  con `grep -n "ERR-15" registro/REGISTRO_etapas_1_2.md` antes de usarlo.
- **Vocabulario:**
  - "evoluciona" sólo con la curva de `g` al lado; nada de "especie" ni "entiende";
  - "del propio linaje" sólo si S cumple en serie y réplica;
  - "cruza el muro" sólo con P1.

## 5. Entregable
- Commit y push a `nube/termo-banco-20260928`, con los datos (`datos/`), los logs, el arnés de la nube y el INFORME.
- **Pull request contra `organelos`, sin mergear.** En la descripción: el veredicto primero, la tabla por brazo y cualquier cosa que no
  haya dado OK.

## 6. Límites
- No toques el tronco congelado, la pista, el juez, los carros, el runner ni la letra. Nunca `manifiesto.py` sin `--check`.
- Un solo Pool a la vez (Pool 3). Nada de enjambres: a lo sumo un auditor de solo lectura al final.
- Decisiones difíciles: tómalas y escríbelas con hora, opción tomada, alternativa descartada y porqué.
