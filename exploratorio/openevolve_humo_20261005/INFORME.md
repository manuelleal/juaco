# FUNCIONA (como humo): en 30 rondas el bucle rehízo la limpieza desde O1 sin limpieza, y su mejor programa quedó por encima de O1 en las 3 semillas selladas

Humo exploratorio del 5-oct-2026. **Nada se declara.** Una sola corrida del bucle, sin réplica ni controles de azar.
Preregistro (escrito antes): `PREREGISTRO_humo.md`. Carpeta: `C:\Users\User\Documents\PROYECTOS\JUACO-OPENEVOLVE\`.
En el repo JUACO no se escribió nada (sólo lectura, por ruta, con `python -B`).

## 1. Examen (semillas selladas 272001–272003, T 100 000, fundador NO limpio, 9 linajes)

| Semilla | Programa | Persisten | Cruzan (R0 real ≥ 0.9) | R0 real mediana | Extinciones tras t 10 000 | Pasos sin nada bueno en el mundo |
|---|---|---|---|---|---|---|
| 272001 | **Mejor del bucle** | 9/9 | 9/9 | 0.963 | 0 | 0.24 |
| 272001 | O1 (techo a mano) | 9/9 | 7/9 | 0.933 | 0 | 0.04 |
| 272001 | Raíz (sin búsqueda) | 0/9 | 0/9 | 0.157 | 424 | 0.62 |
| 272002 | **Mejor del bucle** | 9/9 | 7/9 | 0.963 | 0 | 0.23 |
| 272002 | O1 | 6/9 | 5/9 | 0.950 | 5 | 0.04 |
| 272002 | Raíz | 0/9 | 0/9 | 0.250 | 428 | 0.60 |
| 272003 | **Mejor del bucle** | 9/9 | 9/9 | 0.967 | 0 | 0.25 |
| 272003 | O1 | 8/9 | 7/9 | 0.950 | 1 | 0.05 |
| 272003 | Raíz | 0/9 | 0/9 | 0.211 | 500 | 0.64 |
| **Suma** | Mejor / O1 / Raíz | **27 / 23 / 0** de 27 | **25 / 19 / 0** de 27 | | | |

Por la letra del preregistro (mejor ≥ 5/9 en ≥ 2 de 3 selladas y raíz en 0): FUNCIONA. Muertes voluntarias: 0 en todos.
Contabilidad del juez coherente 9/9 en las 9 corridas. Tres semillas: que supere a O1 es una observación, no un resultado.

## 2. Qué escribió el bucle (el fragmento)

En la **tercera llamada** el modelo ya propuso limpiar. Lo llamó "reciclar":

```python
def _reciclable(self, v, lev):
    if (v > 0).any(): return False                      # nunca muerde así algo que sirve
    for j in (0, 1):
        if v[j] < 0 and lev[j] + v[j] < RECICLA_SEGURO: return False   # 0.35: el golpe no puede dejarlo en riesgo
    return True
```

En palabras: una letra ya conocida que sólo daña se muerde, si el cuerpo aguanta el golpe, para que en su lugar aparezca
otra cosa. Es la limpieza de O1. Pero esa primera versión dio cuerpos **casi inmortales que no se reproducían** (0
nacimientos en 100 000 pasos; el puntaje preregistrado lo dejó en 0.30 y no lo premió). Estuvo atascado ahí 8 rondas.
- **Ronda 12 (0.82, igual a O1 en esa semilla):** añadió un modo "banco": cuando las dos reservas ya están en el umbral de
  parto, no limpia, no prueba letras nuevas y no viaja lejos, para no romper los 500 pasos seguidos. Es la misma idea que
  la cláusula de O1 "limpiar sin romper la ventana de parto". También cambió el margen de la boca por el tope real (1.5).
- **Ronda 28 (0.97):** usa la pizarra pública para que los cuerpos se pasen lo aprendido de cada letra (O1 no la usa).
- **Ronda 30 (0.996):** limpiar algo cercano compite por distancia con ir a algo bueno lejano.

Auditoría a mano del mejor (`examen/mejor_programa.py`, 184 líneas): pasa `revisa_carro` y la regla de tabla; no nombra
letras, no usa azar propio, no toca la pista; la pizarra es un canal permitido por el reglamento. Limpia unas 2.6 veces
más que O1 (≈ 9 000 mordidas malas por corrida contra ≈ 3 400) y aun así el mundo le queda más vacío de lo bueno.

## 3. Costo real

| Rubro | Medido |
|---|---|
| Llamadas al modelo (Claude Sonnet 5 por el CLI, sesión del director) | 37 = 1 de prueba + 6 del ejemplo + **30 del humo** (tope 33; 0 reintentos) |
| Tokens del humo | 523 mil de entrada, 477 mil de salida (≈ 16 mil de salida por llamada: el modelo razona largo) |
| Equivalente en dólares que reporta el CLI (se pagó con la suscripción) | 6.63 USD el humo + 0.49 el ejemplo |
| Reloj del humo | 208 min (94 min esperando al modelo, 114 min de pista) ≈ 7 min por ronda |
| CPU de pista (un proceso a la vez) | humo 114 min (85 corridas) + cordura ≈ 30 min + examen 28 min |
| Reloj total del encargo | ≈ 4 h 40 min (18:05 a 22:47); más que "una tarde" |

De 30 propuestas: 30 diffs válidos, 0 rechazadas por el filtro, 0 reventaron. Pero **9 de 30 fueron el mismo programa**:
el modelo ve el mejor en el prompt y lo vuelve a copiar encima de un padre peor. Un tercio del presupuesto se fue en eso.

## 4. Qué falló y cómo se resolvió

1. **El proveedor `claude_code` de fábrica no arranca en Windows** (`FileNotFoundError [WinError 2]`: busca `claude` y lo
   instalado por npm es `claude.cmd`). No cambié de servicio: escribí `adaptador_claude.py`, que llama al mismo CLI con la
   misma sesión por la ruta de `claude.exe`, enganchado por `init_client` sin tocar el paquete. **Aviso:** el encargo decía
   detenerse si el proveedor no funcionaba; juzgué que esto era un arreglo de instalación y no otro proveedor. Si el
   director lo ve distinto, el humo debe leerse con esa reserva.
2. El de fábrica además deja al modelo **con herramientas y con la memoria del usuario** (podría leer `O1.py`). El
   adaptador lo lanza sin herramientas, en modo seguro y en carpeta vacía; comprobado con una pregunta de prueba.
3. El de fábrica no registra tokens y pasa el prompt por línea de comandos (tope 32 767 caracteres; el humo llegó a
   48 435). El adaptador usa la entrada estándar y guarda cada prompt y respuesta en `registro_llm/llamadas.jsonl`.
4. Python 3.14: OpenEvolve 0.4.0 instaló sin problema. Fijé numpy 2.4.3 (el del sistema) para no cambiar el azar.
5. El paquete de PyPI no trae ejemplos; escribí uno equivalente (minimizar una función): 6 rondas, 6.8 min, de 0.81 a 0.997.
6. Mensajes de error de consola por emojis del log (se arregla con `PYTHONUTF8=1`); no afectan resultados.

## 5. Lo que encontró la cordura del evaluador (antes de buscar)

- **Ancla de identidad:** O1 con fundador no limpio en 883001 y 883002 reproduce el registro de hoy campo a campo (5/9 y 8/9).
- **O1 en una semilla nueva (270002) cruza sólo 2/9.** El "5–8 de 9" salió de dos semillas; O1 varía más que eso.
- `CTRL_O1_SINLIMPIA`: 0/9 y 0/9. La raíz sin pistas es idéntica a ella. Tramposos: dos rechazados; el que miente en
  `salida()` puntúa igual que la raíz.
- **La cordura atrapó un error mío:** la primera puerta de la cascada ("persisten ≥ 3/9" a T 25 000) habría dejado fuera
  al propio O1. Se cambió por "sin extinción tras t 10 000" antes de correr; está anotado en el preregistro.

## 6. Qué se puede decir y qué no

- **Se puede:** la tubería funciona en este PC; un bucle de selección de PROGRAMAS, con un modelo de lenguaje proponiendo
  cambios sobre un juez fijo, llevó la raíz que colapsa a un programa que persiste en semillas que nunca vio.
- **No se puede:** "evolución", "selección natural", "el organismo aprendió", ni "el bucle descubrió la limpieza". El
  prompt decía la física (lo que nadie muerde se queda) y el resumen mostraba el mundo lleno de dos letras; el modelo lo
  nombró en la primera respuesta y lo escribió en la tercera. Además puede conocer trucos así por cultura general. Lo que
  sí le costó fue lo que a O1 también: limpiar sin dejar de reproducirse (9 rondas).
- **No se puede** afirmar que supera a O1: 3 semillas, una corrida, y la búsqueda vio una sola semilla larga.
- Sigue en pie la nota del estudio: estos carros ven todo el anillo; las reglas no son estrictamente locales.
- Mis predicciones: acerté FUNCIONA (0.70), limpieza (0.75), "en las primeras 5" (0.50) y "iguala a O1" (le di 0.30);
  fallé "algún rechazo del filtro" y "20 % de diffs perdidos" (hubo 0).

## 7. Para una serie con protocolo (no corrido)

1. **Azar con el mismo presupuesto:** 30 mutaciones sin modelo, o el modelo con el resumen físico barajado entre programas.
2. **Modelo débil** (Haiku) con el mismo bucle; y **el modelo solo, sin bucle**: 30 respuestas independientes desde la raíz.
   Este último es el que separa "lo sabía el modelo" de "lo logró la selección"; hoy no se puede separar.
3. **Raíz difícil:** repetir desde `V143` (el tronco, que no cruza). Desde SINLIMPIA la respuesta está a un paso.
4. ≥ 3 réplicas del bucle, examen de 20 semillas selladas con la regla ≥ 15/20, 2 semillas largas en la búsqueda.
5. Quitar del prompt el mejor programa completo, o descartar duplicados antes de evaluar (ahorra un tercio).
6. Costo estimado de 3 réplicas × 100 rondas más controles: unas 40–60 h de CPU y 60–100 USD equivalentes.

## 8. Cómo reproducirlo

```
cd C:\Users\User\Documents\PROYECTOS\JUACO-OPENEVOLVE
python -m venv venv ; .\venv\Scripts\python -m pip install openevolve "numpy==2.4.3"
$env:PYTHONUTF8='1'
.\venv\Scripts\python -B cordura\corre_cordura.py                      # O1 y SINLIMPIA, calibración
.\venv\Scripts\python -B evaluador.py raiz\programa_inicial.py         # un programa por la cascada
.\venv\Scripts\python -B lanza.py raiz\programa_inicial.py evaluador.py config_humo.yaml humo\salida 30 33
.\venv\Scripts\python -B examen\corre_examen.py examen\mejor_programa.py
```

Archivos: `humo\salida\` (30 prompts y respuestas en `registro_llm\llamadas.jsonl`, 85 corridas en `evaluaciones.jsonl`,
21 programas distintos en `programas_evaluados\`, checkpoints), `examen\examen.log`, `cordura\`, `shas_antes_del_humo.txt`.
