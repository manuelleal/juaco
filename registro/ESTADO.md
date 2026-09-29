> **Ruta de publicación:** ver `registro/RUTA.md` (casilla actual y siguiente paso).

# ESTADO: una página que se reescribe en cada cierre (skill `/juaco-cierre`)

> Última reescritura: **29-sep-2026, ~10:45** (antes: 28-sep ~21:45), por el coordinador. Es el cierre del día 28-sep, trabajado en la rama `organelos`
> (sin merge a `main` todavía; lo decide el director). El detalle está en `REGISTRO_etapas_1_2.md` (entradas del 28-sep) y la narrativa
> en `HANDOFF.md`. La página del 25-sep queda en el historial de git.

## Tronco
**v14.3** (tag `v14.3-tronco`, `40f9350`, 24-sep) sigue siendo el tronco. Tiene 24 archivos congelados, intactos.
Candidato a v14.4: **TERMO′** (v14.3 + termostato de boca con memoria que olvida). Con ERR-150 pasa T-A, T-B, T-C, T-D, T-F y T-G;
**sólo cae T-E**, por conducta real: muerde más veneno que v14.3 en los escenarios de v3′.

## Hitos del 28-sep (serie + réplica preregistradas, auditadas desde los crudos)
1. **★★ BLOQUES = FUNCIONA ×2** (`experimentos/organelos/bloques/opusM/`).
   - Montaje: genoma de reglas componibles y duplicables (sentido/píxel, comparador, acción, peso; mutar, duplicar, borrar, HGT),
     en ECO, con hijo ingenuo y vivero finito.
   - La selección natural fija **sola un órgano de rechazo heredable (instinto)** y lo **duplica** (Ohno).
   - Con ese órgano el linaje se sostiene sin vivero: 19/20 ×2, contra 14/13 de los 15 genes y 1/0 sin herencia.
   - **Es el primer órgano construido por la selección en JUACO.**
2. **★ ECO_SEL = FUNCIONA ×2.** La selección sobre el linaje de F1 frío sube la capacidad de carga K de ~31 a ~39.
3. **★ ECO_SEL_ING = FUNCIONA ×2.** Con hijos ingenuos, la selección baja 31–32 % los fundadores que el linaje necesita.
4. **TERMO = HAY ALGO MODESTO ×2** en la carrera: R0 real 0.93, pareado con O1; P1 13–14/20.

## El muro de la carrera (H-1): NO cae, pero quedó mapeado
- **La palanca es el ESTABLECIMIENTO**: fundadores por linaje. O1 usa ~1; v143, 15.
- **No es que el fundador ignore el veneno.** En la pista el anillo es ~90 % veneno + sal, y morder lo malo LIMPIA el camino a la comida:
  - el órgano de rechazo de ECO puesto en TERMO hunde el linaje (0.87 → 0.13; el fundador muere de hambre);
  - O1 también pierde el 97 % de sus fundadores por veneno y aun así se establece.
- **El muro es decidir cuándo limpiar y cuándo comer.**
- NO, exploratorios: trasplantar genomas de ECO a la pista (×2); termo_organo; BLOQUES_PISTA (con 9 cuerpos y 100k la selección no fija
  nada; es deriva).
- **Modesto:** con pasajes en la pista, la selección lleva el gen del termostato de la zona letal al nivel de TERMO por sí sola
  (pasg empata con TERMO 6/12 y gana a v143 12/12).

## Lectura del día (cuatro fuentes coinciden)
- Con perillas fijas, la selección llega rápido a un techo: 10× más tiempo no lo mueve (nube eco_sel_largo L = NO) y los pasajes quedan
  planos.
- Más perillas lo suben poco: 25 = 47 genes; con 50, la historia de vida se dispara.
- **Piezas que se pueden armar y duplicar rompen el techo** (BLOQUES ×2).
- Con un kit más grande aparecen órganos nuevos no diseñados (memoria, sociales), pero diluyen al mejor (exploratorio).
- **La frontera la pone lo que el organismo puede construir, no el tiempo.**

## Nube (crédito ~20 USD, vence el 5-nov)
- `nube/eco-sel-largo-20260928`: serie L = NO, MC = FUNCIONA. La réplica se sugirió pararla y correrla en el PC.
- `nube/termo-banco-20260928`: serie en curso al cierre. El creador predice NO.
- **Regla sugerida:** la nube sólo para lo que el PC no alcanza de noche.

## Noche del 28-sep (22:00–23:00), EXPLORATORIOS, todos NO, cada uno con su lección
- **BLOQUES_PISTA ronda 2 (T 300k):** NO. **La pista tiene N_MAX 9 y 1 cuerpo vivo por linaje**: no hay población sobre la que seleccionar.
  **Evolucionar en la pista exige una pista con población por linaje**, es decir, tocar la carrera. Es decisión del director.
- **Mundo que cambia** (inversión cada 20k–100k): ningún linaje con reglas persiste. La selección prefiere MEMORIA (4/6), pero la memoria
  no olvida.
- **Olvidar/reprobar (reglas)** y **olvidar el cerebro** (gen λ): NO. La selección APAGA el olvido (λ 1e-7..3e-6). El hijo nace ingenuo
  y la selección "ve vidas, no siglos".
- **Inversión dentro de una vida** (500–10 000): NO. Nadie sobrevive; λ sube apenas (8.6e-6).
- **Lección repetida 3 veces en el día:** no olvidar mata (TERMO en T-C, la memoria de las reglas, el cerebro). Pero la selección no paga el
  olvido si el cambio es raro, y si es muy frecuente el mundo es imposible. Hay que buscar la banda intermedia o una pieza distinta.

## Cerrado el 29-sep (mañana), leído desde los crudos
- **★ TERMOSTATO EN LA PISTA = FUNCIONA ×2** (`reunion/opusB/`, commits `2e59aa05`, `68d2821b`). La selección lleva sola g de la zona letal a la
  banda en 20/20 ×2; pasg gana a v143 (20/20, 18/20) y al control sin transferencia (19/20, 20/20). **No dice:** ≈ TERMO (8/20 ×2); mayorías
  10 y 12/20 contra O1 19: no cruza la letra del muro. La serie se cortó por apagado y se reanudó sin pérdida.
- **dinamita (intento #4) = SE CIERRA SIN INFORME.** VETO/LIMPIA NO (0/10); PATAS exploratorio (pc 8/10) sin confirmar; ola 4 8/80. ERR-154, ERR-155.
- **pista_pob preregistrada** (`21a63ff5`, preregistro sha `68c78af5`): pista NUEVA versionada (K = 8 copias de la pista vieja, migración sólo
  al fundar); pista.py y juez.py sin tocar; arnés PASA; auditor LISTO tras 2 cambios antes de datos. **Explora corriendo, pool 6.**

## Plan para mañana (propuesta del coordinador; decide el director)
1. **El muro con bloques y población.** BLOQUES en la pista con más cuerpos o tiempo, o un mundo intermedio, y sentidos para "¿hay algo
   bueno a la vista? / reservas", para que la selección arme la decisión "limpiar o comer".
2. ~~Confirmar "la selección encuentra el termostato en la pista"~~ **HECHO 29-sep: FUNCIONA ×2.**
3. **Subir de procariota:** un mundo que cambia (lo bueno se vuelve malo), donde la memoria y lo social deberían ganarle al instinto
   fijo. Después, depredadores y parásitos que coevolucionen: la vía clásica a la evolución abierta.
3b. **Mundo enriquecido** (idea del director, 28-sep ~22:00, a partir de lo que leyó sobre chimpancés en cautiverio: sin estímulo no
   desarrollan nada; aprenden de otros; hacen tareas con orden). Tareas con SECUENCIA (comida que sólo se abre con A y después B),
   aprendizaje SOCIAL que pague (copiar al vecino que sabe), memoria. Se conecta con la escuela de abejas (23-sep) y con los órganos de
   memoria y sociales que aparecieron el 28-sep en el kit grande.
4. **Tronco:** TERMO′ debe morder menos veneno en los escenarios de T-E. No se toca la letra.

## Niveles (los fija el director)
Propuesta: niveles 10–13 (ECO), de ~10 % a **+15–20**, por ECO_SEL ×2, ECO_SEL_ING ×2 y **BLOQUES ×2**.
**29-sep:** el director aceptó la recomendación del coordinador: sumar **+2** (total +17–22) por el termostato-en-la-pista ×2, primera
pieza evolucionada DENTRO de la pista (modesto: empata con TERMO y no cruza el muro). +1 más sólo si pista_pob mueve el establecimiento.

## ERR
ERR-149 a ERR-153 se usaron el 28-sep (ERR-151 está reservado para la rama nube/eco-sel-largo). ERR-154 y ERR-155 el 29-sep (dinamita).
**El siguiente libre es ERR-156.**

## Decisiones para el director (máximo 2)
1. Qué hacer según el veredicto de pista_pob (si FUNCIONA: serie n=20 + réplica, ~5–6 h cada una).
2. El merge de `organelos` a `main`.
