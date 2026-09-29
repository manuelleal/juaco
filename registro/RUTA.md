# RUTA de publicación (creada 29-sep-2026, a pedido del director)

> Al inicio de cada sesión, `/juaco-estado` dice en qué casilla vamos y cuál es **el siguiente paso concreto (uno solo)**.
> Motivo del director: hay una empresa que trabaja en lo mismo. Publicar con fecha y DOI deja constancia del método y de los resultados.

**Tesis (aprobada por el director, 29-sep):**
> Un protocolo de preregistro, identidad bit a bit, réplica y auditoría independiente permite que un investigador dirija agentes LLM en
> investigación computacional confiable: en 120 errores registrados, el protocolo atrapó 105 (88 %) antes de que alteraran una conclusión, y
> produjo resultados replicados de vida artificial, como un órgano construido por selección natural.
> (X = 105 de 120 sale del Paso A, `informe/errores.csv`. Rango de sensibilidad: 104–110; sin los ERR-1..4 reconstruidos,
> 101/116. La versión estricta, "atrapados antes de correr la serie", da 49. Pendiente: la verificación del director con la muestra de 20.)
> Nota: los números llegan a ERR-153, pero 27 no se usaron y 6 son reservas o cláusulas; sólo 120 son errores reales.

**Segunda frase de la tesis (el alma; del director, 29-sep):**
> El error más costoso no lo cometió un agente sino el director: diez fases persiguiendo el techo de benchmarks propios, hasta
> que el registro mostró que la capacidad no aparecía por escalar la vara sino por darle a la selección piezas con qué construir.
>
> *EN:* "The costliest error was not an agent's but the director's: ten phases chasing the ceilings of our own benchmarks, until
> the registry showed that capability did not come from raising the bar but from giving selection parts to build with."

**Palabras del director, en bruto (29-sep), para la sección de lecciones:**
> "Yo protocolicé 10 fases buscando incansablemente el techo de esas fases, pues pretendía que el organismo llegando ahí se
> convertiría en AGI. Cuando me di cuenta de que estaba peleado con benchmarks y no con la evolución de verdad, comencé a ver el
> proyecto desde otro punto de vista. No es sólo la interacción: es cómo pensar los problemas desde afuera puede ayudar a
> solucionar cosas que no tienen nada que ver."

- Ideas conectadas: la ley de Goodhart; los datos del 28-sep (con perillas fijas la selección se estanca; con piezas componibles
  construye); las analogías que destrabaron trabajo (chimpancés y el mundo enriquecido, Minecraft y los bloques, las bacterias y los
  pasajes seriados).

## Casillas
- [ ] **(1) Informe técnico del protocolo**, en inglés (arXiv cs.AI).
  - Paso A: `informe/errores.csv`.
  - Paso B: preclasificación con Jev y acuerdo.
  - ALTO: el director verifica 20 a mano.
  - Paso C: `informe/borrador.md`, verificado por el auditor.
  - ALTO: el director lo reescribe con su voz.
- [ ] **(2) Zenodo y arXiv:**
  - repo archivado con DOI (`.zenodo.json`);
  - versión LaTeX para Overleaf;
  - 5 posibles avaladores de arXiv cs.AI;
  - borrador del correo de aval. **Los envíos los hace el director.**
- [ ] **(3) Difusión:** un post y 2–3 correos. Los envía el director.
- [ ] **(4) Notas cortas** por cada resultado cerrado (ver `RESULTADOS_VERIFICADOS.md`).

## Higiene del repo público (previa a todo)
- [x] Regla 1 (29-sep): batería v14.3 PASA, generalización PASA, manifiesto 24/24 intacto.
- [x] `organelos` integrada en `main` (fast-forward a `8e18fd3`, 29-sep; decisión del director).
- [x] LICENSE (MIT) · LICENSE-DATA (CC BY 4.0) · CITATION.cff (ORCID y correo pendientes) · `.gitignore` con claves.
- [x] `RESULTADOS_VERIFICADOS.md` y README nuevo, revisados por el director (7 ajustes). Faltan el ORCID y el correo.
- [ ] Jev en la rama `jev-triaje`. Pendiente de verificar qué es y cómo se instala; ningún paquete desconocido se instala sin verificar.

## Avisos de arXiv (director, 29-sep)
- arXiv pide el **código fuente LaTeX**, no sólo el PDF. El informe se entrega como carpeta, lista para subir, con los .tex, las
  figuras y la bibliografía (.bib).
- **Todo lo que se publica es permanente.** Antes del envío hay que revisar que no quede nada privado en los archivos,
  **incluidos los comentarios dentro del LaTeX**: claves, correos privados, rutas locales, notas internas.
- Categoría: por defecto cs.NE en la cuenta; **el informe va en cs.AI**. No se inicia ningún envío hasta tener el informe terminado
  y el aval.

## Reproducción del autor (29-sep)
Windows 11, AMD Ryzen 7 5700, Python 3.14.2 instalado desde `requirements.txt`, en una terminal aislada.
- Chequeo del tronco: PASA.
- BLOQUES serie 48411–48430: VEREDICTO FUNCIONA, `VEREDICTO.json` con el mismo sha (`86c36f933da2543c`). 161 JSON idénticos campo a
  campo salvo `seg` (el tiempo).
- Los crudos del repo se dejaron como estaban: la corrida del autor sólo difería en `seg`.

## Siguiente paso concreto
ALTO del paso 4A: el director llena la columna `clasificacion_director` de `informe/muestra_20.csv` (20 errores). Después: acuerdo
y paso 4B (Jev).
