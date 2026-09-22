# CARRERA DE BACTERIAS — tres Opus sueltas a la vez hacia la fase 10 (21-sep-2026, noche; pedido del director)

Misión de fondo: llegar a la AGI por este camino (organismo mínimo con reglas locales, sin retropropagación, peldaños preregistrados con
controles y réplicas); el método manda sobre el cómo. Misión de la carrera: **acercar el organismo a la fase 10 (un linaje mortal que se
sostiene y acumula) con lo que hay en el repo, cada bacteria por su camino, sin esperar al coordinador.** Al final revisamos las tres y nos
quedamos con lo que ayude a empezar de verdad.

## Lo que hay medido (leer `registro/ESTADO.md` y `registro/investigacion/ENCARGO_mundo_fase10_20260921.md`; ése es el problema)
El organismo aprende, se desdice, generaliza, transmite y hereda en menos de una vida (fase 9, declarada). Lo que nunca pasó: que un linaje
mortal se sostenga (R₀ ≥ 1) ni que acumule entre generaciones. El 21-sep se midió que **ni un nodo con la tabla verdadera cruza R₀ 0.9: el
muro es el mundo**, no la herencia. El cuello de fondo: el organismo no construye representaciones nuevas desde los píxeles sin prior.

## Caja de herramientas (todo por anclas; sha fijado; nada congelado se toca)
- Tronco `organismo/organismo_v142.py` (17528d767fcebaf6) y sus baterías; identidad `organismo/identidad_v142.py`.
- Mundo vivo con dos necesidades y muerte real: `experimentos/nivel11_mundo_vivo/`, `organismo_vivo_rep2`.
- Nodo por relevancia (fase 9): `experimentos/nivel09_cuerpo_nuevo/organismo_f9.py` + **gemelo numba bit a bit ×46** `organismo_f9_rapido.py`
  (arnés `identidad_f9_rapido.py`); bloque 2 `nivel09_cuerpo_nuevo_b2/organismo_f9c.py` + `organismo_f9c_rapido.py`.
- Mapa y mundo 2D con geometría sorteada: `experimentos/nivel6_*`, `nivel06_rodeo_obligado/mundo_muralla.py`.
- Familias y variantes: `experimentos/nivel12_mundo_familias/`, `junta_fase5/`, `nivel05_familia_variante_BAv/`.
- Alma y linaje: `experimentos/nivel13_alma/`; evolución guiada: `experimentos/evo/` (JUACO-EVO).
- Criterio con placebo: `experimentos/criterio_v3/` (usa v2 y v3 lado a lado; el v3 no está aprobado).
- Reglas: `registro/EQUIPO.md` 1–15; errores ERR-01..93 en el registro (los repetidos: ERR-38 perilla inerte, ERR-42 humo sin JSON,
  ERR-87 lee_json, ERR-89 puerta sin juez, ERR-91 umbral en el nulo).

## Reglas de la carrera (la nave)
1. Cada bacteria trabaja SÓLO en `experimentos/carrera_fase10/<letra>/`. No toca los archivos de otra ni nada fuera.
2. **Hasta 10 ejecuciones propias**, cada una de UN proceso (sin `Pool`), ≤ 12 corridas y ≤ 300 000 pasos por ejecución; con el gemelo numba
   eso alcanza para generaciones enteras. Cada ejecución escribe su JSON en su carpeta y una línea en `BITACORA.md`: idea → prueba →
   resultado → lección → qué corrige. Lo que ya falló no se repite sin razón escrita.
3. Sin commits, sin matar procesos, sin tocar congelados (`python manifiesto.py --check`).
4. Identidad bit a bit con perillas apagadas contra su ancla ANTES de mirar números; controles que DEBEN diferir.
5. Vocabulario: lo que se declara es lo que se midió. "Población", "evoluciona", "cultura", "planifica" prohibidas salvo con la prueba.
6. Cada bacteria firma una **predicción numérica** antes de su primera ejecución y la juzga al final, con las que se le cayeron.

## Meta medible de la carrera (la misma para las tres; cada una decide el camino)
Un mundo + un linaje donde, con las reglas locales del tronco:
- **M-1** R₀ ≥ 1.0 con herencia (nodo, mapa, estructura o lo que la bacteria proponga) y R₀ < 0.5 sin herencia y con herencia barajada.
- **M-2** la generación 5 come lo que la generación 1 no podía (≥ 2× combinaciones explotadas, pareado por semilla).
- **M-3** algo que ninguna de nosotras diseñó aparece y se repite en otra semilla (novedad). Se reporta aunque no llegue a puerta.
Semillas: 3001–3099 para A, 3101–3199 para B, 3201–3299 para C (libres al 21-sep; verificar con grep).

## Entregable de cada bacteria (`<letra>/INFORME.md`, ≤ 2 páginas)
Camino elegido y por qué · mundo y mecanismo (memoria nueva declarada) · arnés N/N · tabla de las ejecuciones (hasta 10) con R₀, muertes,
acumulación, novedad · M-1/M-2/M-3 medidos contra la predicción firmada · qué se le cayó · qué haría con Pool y 40 semillas · **una frase
al director: qué de lo suyo ayuda a empezar de verdad**.
