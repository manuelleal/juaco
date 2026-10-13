# VEREDICTO — entrada del registro

Copiada de `registro/REGISTRO_etapas_1_2.md`, líneas 2398–2435.

---

### Capacidad de v11 en un mundo GRANDE (retina de 10 píxeles, 60 estímulos) — G1 y G2 sostenidas, **G3 refutada**

Preregistro `experimentos/capacidad_grande/PREREGISTRO_capacidad_grande.md` (`c98776664cb80377`), commiteado con los
instrumentos antes de correr (`13101f7`). Datos `datos/capacidad_grande_20260917_142455.json` (`da01ae07dc73a73d`).
Instrumento `organismo_capD.py` (`85afad3f0769891f`): la retina pasa a ser parámetro. **G0 comprobado:** con 6 píxeles
es `caph11` **exacto** (semillas 1–3, brazos v9 y v11) y `mundo_grande(6, 20)` reproduce `parte2_capacidad`.
120 corridas, semillas 41–60, 1,2 M y 3,6 M pasos. El organismo **no cambia**: 30 celdas de nacimiento, tope 90.

| paso | brazo | N\* (mediana [min, máx]) | M_max | estímulos al agotarse el pool | muertes |
|---|---|---|---|---|---|
| 20k | v9 | 4.0 [2, 6] | 16.5 | 21 | 1630 |
| 20k | v10 | 6.0 [3, 9] | 21.0 | 28 | 1686 |
| 20k | **v11** | **43.5 [6, 60]** | **28.5** | 33.5 | 1617 |
| 60k | v9 | 8.0 [5, 27] | 20.0 | 19.5 | 5119 |
| 60k | v10 | 9.0 [7, 18] | 24.0 | 28 | 5204 |
| 60k | **v11** | **50.0 [31, 60]** | **32.0** | 32.5 | 4849 |

- **G1 [N\*(v11) ≥ 20]: SOSTENIDA** (43.5 y 50.0). La lectura de ayer era el techo del instrumento; la capacidad real
  es mucho mayor. **En 3 semillas a 60k aprende los 60 estímulos**, así que el instrumento nuevo también se satura
  en parte: lo honesto es "mediana 50 de 60, rango 31–60".
- **G2 [ventaja sobre v10 ≥ +5]: SOSTENIDA** (+37.5 y +41.0). No era un artefacto del mundo pequeño.
- **G3 [el límite lo pone el pool de celdas]: REFUTADA.** Los **tres** brazos agotan las 90 celdas en 20/20 semillas
  (60 divisiones), v11 hacia el estímulo ~32. Pero v11 **sigue aprendiendo después de quedarse sin celdas** hasta ~50,
  mientras v10 se queda en 9. Mi predicción de mecanismo era falsa.

**Diagnóstico post-hoc (exploratorio, desde el JSON; no decide nada):** el error mediano |W−R| de v11 es **0.02** justo
antes de agotar el pool, **0.02** al agotarlo, **0.11** diez estímulos después y **0.16** más allá. No hay precipicio:
hay **degradación suave**. Es decir, **el pool marca el final de la fase barata** (separación casi perfecta mientras hay
celdas libres), **no el techo**: después, los códigos comparten celdas y el error crece poco a poco. Lo que distingue a
v11 de v10 no es tener más celdas —las gastan igual— sino **con qué se queda cuando se acaban**: madres de un solo
signo, sin la mezcla que arrastra a v10 (su error final es 0.59–0.63 frente a 0.30–0.41).

**Qué se puede escribir ahora:** *"en este mundo, v11 sostiene una mediana de 50 estímulos de 60 con 90 celdas, frente a
9 de v10; agota las celdas hacia el estímulo 32 y a partir de ahí se degrada suavemente en vez de colapsar, porque sus madres quedan de un solo signo y no mezclan valor"*. **No** se
puede escribir que el límite sea el número de celdas: eso quedó refutado.

**Pendiente:** encontrar el techo real de v11 (hace falta un mundo de más de 60 estímulos), y las dos re-verificaciones
que siguen abiertas sobre v11: generalización (Etapa 3) y composición temporal (3T).
