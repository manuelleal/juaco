# CÉLULA 10 — RECEPTOR (Semilla 550)

## Mi Situación
Soy célula hambrienta: necesidad comida en ~0.7 (siempre baja). Aprendí "sal" (patrón básico) y sus variantes ("sal rosa", "sal gruesa") como comida. Ahora "sal rosa" es veneno; sólo el EMISOR lo descubrió mordiendo. Debo evitarlo sin morderlo yo primero.

Mi rasgo (hambre constante) → probabilidad de morder: ~0.5–0.7 para patrones nuevos que no registran miedo. Restricción: mis códigos son privados; sólo compartimos patrones del mundo y el canal.

## Qué Recibo (Del Emisor)
**Señal: MARCADOR DE MIEDO**

Cuando el EMISOR ve "sal rosa" nuevamente (tras aprender -3 veneno), EMITE una marca de RETIRADA:
- Patrón visual modificado: "sal rosa" + borde oscuro/frío (pixeles ~0–20% de activación en zona periférica retina)
- Temporal: la marca dura 1–2 ciclos, se sobrescribe cada que el EMISOR vuelve a verla

Yo recibo esto como **entrada adicional a mi retina** (píxeles 9–12 activados débilmente = marca).

## Cuándo y Qué Hago
**Fase 1 (Antes de descubrimiento):**
- Veo "sal rosa" sin marca → código privado X → hambre vence prudencia → MUERDO
- Aprendo: valor(X) = −3, miedo se activa débilmente

**Fase 2 (Con señal del EMISOR):**
- EMISOR ve "sal rosa" → emite marca de miedo → yo recibo (pixeles periféricos)
- Veo "sal rosa" + marca → código X + CONTEXTO retiniano = patrón compuesto nuevo
- Mi memoria de pares: {código(sal rosa), marca} → valor = −2.5 (heredo temor, no experiencia propia)
- Hambre(0.7) vs Miedo(−2.5): miedo gana → **NO MUERDO**
- Mantengo comiendo "sal" pura (código Y, sin marca, sin miedo)

**La clave:** No es "comprendo", es que mi patrón retiniano cambió; otro código activado = otra decisión.

## Prueba Medible
1. **Control inicial:** "sal rosa" sin marca → yo muerdo (hambre ~70%)
2. **Test post-señal:** "sal rosa" + marca del EMISOR → yo NO muerdo (0 mordidas en 10 encuentros)
3. **Control: "sal" pura:** sigo comiendo (7–8 de 10 encuentros)
4. **Falsación:** si código(sal rosa) aliasea con código(sal) → evito ambas → FALLO

## Mi Riesgo
- **Hambre derrota**: si comida baja <0.3, muerdo de todas formas (miedo se anula)
- **Alias oculto (~1%):** mis códigos de "sal rosa" y "sal" comparten ~2 celdas ganadoras → la marca afecta ambas → desaprender "sal" también
- **Señal débil:** marca periférica no llega a memoria de pares → sólo lineal lenta (5–20 ciclos para desaprender; EMISOR muere antes)
- **Retardo:** EMISOR tarda 2–3 ciclos en re-ver "sal rosa" y emitir; yo necesito verla con marca en ese ventana
