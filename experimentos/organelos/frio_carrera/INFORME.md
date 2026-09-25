# INFORME — frio_carrera: F1 en la pista de la carrera (creador, 25-sep-2026, ~13:50–15:05). LISTO PARA SERIE; sin serie, sin Pool, sin git

Misión: llegar a la AGI por este camino. Preregistro: `PREREGISTRO_frio_carrera.md` (§0–§10 escritos antes del humo, sha ddec01d81ab7b140).

**Qué hice**
- **Traducción.** En la carrera el nacido hereda el NODO del linaje: las últimas 20 mordidas de cada cuerpo muerto, leídas por la vía lenta.
  - `V143_RES0` lee una copia del nodo sin las entradas R = 0. Memoria nueva: cero.
  - `V143_BAR0` hace lo mismo y además permuta las R entre entradas en cada lectura, con un splitmix64 propio: el carro no puede usar
    `np.random` y no consume ningún rng.
  - `V143_TEL` es V143 con telemetría; sólo para el arnés y el humo.
  - Los tres salen de `construye_frio_carrera.py` por anclas desde `V143.py` (2a03048a7f1525e5) y pasan `revisa_carro`.
- **La traducción tiene objeto:** el nodo SÍ tiene neutras (cada letra es neutra en una necesidad). En V143 son el 50 % de las entradas
  y el 47 % de las leídas (humo, 65 lecturas).
- **`corre_frio_carrera.py`** (49de4dd28a8f3c3a):
  - cada corrida ES `corre_v143.tarea` (importada; regla 14 verificada campo a campo);
  - la letra está en `lee_serie`;
  - nube-9 atrapado; JSON por corrida; `--reanuda`; `--bloque`;
  - descriptivo de ESTABLECIMIENTO (propuesta del explorador de trasplantes).

**Arnés `identidad_frio_carrera.py` → 58/58** (56 s; `identidad_frio_carrera_salida.txt`):
```
(K) construye == disco; shas; revisa_carro PASA x3 · (A) RES0/BAR0/TEL con perillas 0 == V143, salida ENTERA (N 9, fundador limpio) x4
(B) TELEM es solo lectura (todo igual salvo d['carro']['frio_carrera']); V143: 61/167 entradas del nodo neutras (s36901, T5000)
(C) runner.tarea == corre_v143.tarea campo a campo (V143, y V143_RES0 apagado salvo la etiqueta del linaje); P.run restaurado
(D) quita exactamente las neutras; el nodo guardado no cambia; en la pista 0 neutras leidas; RES0 no es inerte
(E) BAR: multiconjunto igual, patron/necesidad en su sitio, determinista, no toca el rng del cuerpo; cambia R en 161/200 y 3/3 en pista
(G) determinismo · (F) SystemExit (guardia ERR-60) atrapado + JSON; --reanuda; 1 aborto -> NO SE LEE · (H) ERR-115 10/10 · (V) letra 19/19
```

**Humo** (1 proceso, 6 corridas, T 20 000, 140 s; JSON escritos; no se lee):
- V143 0.182, RES0 0.115 (pierde 2/2), BAR0 0.048, O1 0.500.
- 88 nacidos leen el nodo; 870 fundadores limpios nacen con el nodo vacío.

**Costo:** por serie, 80 corridas ≈ 13 600 s de CPU, **25–45 min con Pool 6**. La réplica cuesta lo mismo.

**Comandos (el coordinador)**
```
python experimentos/organelos/frio_carrera/construye_frio_carrera.py --verifica
python experimentos/organelos/frio_carrera/identidad_frio_carrera.py                                  # 58/58, ~1 min
python experimentos/organelos/frio_carrera/corre_frio_carrera.py --serie --desde 36001 --n 20 --pool 6
python experimentos/organelos/frio_carrera/corre_frio_carrera.py --serie --desde 36021 --n 20 --pool 6   # replica
python experimentos/organelos/frio_carrera/corre_frio_carrera.py --bloque <resumen serie>,<resumen replica>
```

**¿Tiene sentido F1 en la carrera? Poco, y lo digo con evidencia (no forcé nada, pero el paquete está listo para cerrar el nulo)**
1. **Casi nadie lo recibe.** Con fundador limpio, el filtro sólo toca a los hijos de la cola: 88 contra 870 fundadores en el humo, y
   ~4 200 contra ~34 000 en la serie 14301.
2. **El hijo no muere de ignorancia.** En trasplantes, ENSEÑA (el hijo recibe todo el cerebro del padre) da 0.61–0.68 contra 0.596.
   Si recibir TODO no mueve el R0, cambiar la mitad de 20 entradas difícilmente lo hará.
3. **Lo mismo, medido en la nube** (exploratorio, 6 semillas): el nodo sin neutras dio −0.009 (gana 3/6) y la tabla del padre sin neutras
   −0.19 (gana 0/6).
4. **"Lo neutro no pesa al DECIDIR" ya está en v14.3, y su versión absoluta mata.**
   - El FILTRO con META no apunta ni muerde lo que tuvo consecuencia mala cuando hay meta. Es la pieza que más pesa: V143 le gana a
     SINFILTRO +0.40 y +0.48, 20/20 ×2.
   - Sin la condición de meta (SIEMPRE) el R0 da 0.000 ×2.
   - Los cables de boca de trasplantes (nomalo 0.18; limpia +0.006) repiten el patrón.
   - El filtro en la decisión que propone el coordinador ya está medido en tres dosis. Otra más no es la prueba más cercana, es una repetición.
5. **Lo que sí distingue a O1** es que su linaje establecido no se extingue: establecido da 0.95, contra 0.82–0.84 de V143. **Propuesta
   (no construida):** atacar el ESTABLECIMIENTO, es decir, que el linaje con hijos no se quede sin cola. La métrica ya va como descriptivo
   en este runner.

**Mi recomendación:** correr serie y réplica (~1–1.5 h) sólo para cerrar con protocolo la pregunta del director ("¿F1 transfiere?").
Espero NO ×2 (p 0.85). Si el coordinador prefiere no gastar CPU en un nulo esperado, el paquete puede quedar archivado sin correr.

**Qué falló / ERR**
- **ERR-148:** tras el humo corregí el texto de la fila V2 de los nulos. O1 cruzó 18/20 en 14301, no 19/20. El umbral no cambia.
- **Dos casos del arnés mal diseñados antes del humo:** (C2) comparaba también la etiqueta del linaje, y (E6) miraba sólo la última
  instancia. Los corregí antes del humo; runner y carros sin cambios.

**Predicciones refutadas:** ninguna por serie (no corrí la serie). El humo ya contradice mi rango de neutras en el nodo: firmé 0.25–0.45 y
mide 0.50 / 0.47. No lo toco.

**No verificado:**
- la ruta Pool/spawn en Windows (es el patrón de `corre_v143`, sin probar aquí);
- T = 100 000 (el humo llegó a 20 000);
- V4 con telemetría de la última instancia de cada linaje en una serie real;
- que el splitmix64 no correlacione entre linajes de una misma semilla (siembra por índice, t y k).
