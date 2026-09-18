# CELULA 12 - RECEPTOR | Ronda 2

## Identidad
- ID: 12
- Rol: RECEPTOR (conducta receptora, integracion de senales)
- Semilla: 552
- Rasgo: Aprendere solo 2 de 3 variantes de sal (inicialmente no conozco sal rosa)
- Mundo: familias de tokens (sal, trigo, agua, etc.); 8 tokens x 3 variantes cada uno

## Protocolo Ronda 2: Como evito sal rosa sin morderla

### EMITE (lo que observo que CELULA 11 hace)

Cuando: Ciclo T exacto donde CELULA 11 (mi pareja EMISOR) descubre mordiendo que sal rosa tiene valor <= -3 (veneno).

Que: CELULA 11 emite simultaneamente:
1. Patron visual sal rosa (pixeles 0-8, mundanos, compartidos): los mismos pixeles que yo veo en mi retina cuando el mundo presenta sal rosa
2. Marca periferica (pixeles 9-12, canal, ~25% intensidad): una senal observable que indica algo cambio en este patron
3. Valor implicito: -5 (fuerte, supera voracidad incluso con hambre < 0.3)

Mecanismo local de CELULA 11:
- Muerde sal rosa -> recibe -3 en su valor
- Escribe en su propia memoria_pares: conoce la respuesta del mundo
- Emite marca en pixeles 9-12 como consecuencia observable de su miedo
- NO expone su codigo privado; la marca es un observable del mundo

### RECIBE (lo que yo hago con la senal)

Ciclo T: Recepcion
Veo en mi retina:
- Patron visual (pixeles 0-8): misma combinacion de pixeles que define sal rosa en el mundo
- Marca periferica (pixeles 9-12): pulso ~25% intensidad en el canal

Ciclo T: Escritura a memoria_pares (sin exponer mi codigo privado)
1. Reconozco el patron visual sal rosa del mundo -> lo codifica con MIS 3 celdas ganadoras (proyeccion privada unica de mi, no compartida)
2. Mi codigo privado para sal rosa = (ganadora_1, ganadora_2, ganadora_3), donde cada ganadora es una celula de mis 30 de corteza
3. Escribe en memory_pares UN entrada: 
   - Clave: (mi_codigo_privado_sal_rosa, contexto_pixeles_9_a_12)
   - Valor: -5
4. La entrada vive en MI memoria, no en la de CELULA 11; es mi propia interpretacion

Ciclo T+1+: Lectura y conducta
Veo sal rosa nuevamente en el mundo:
1. Reconozco patron -> genero MI codigo privado (mismo que ciclo T, porque soy determinista)
2. Consulto memory_pares: (mi_codigo_sal_rosa, contexto) existe?
3. SI: Leo -5 -> MIEDO activa fuertemente -> P(morder sal rosa) cae de ~0.9 (voraz) a ~0.05
4. RESULTADO: Evito sin morder

## Cambios de la Ronda 2: Que tome de quien y por que

### De CELULA 11 (mi pareja EMISOR)
Tome: Estructura clara: patron visual (pixeles 0-8) + marca periferica (pixeles 9-12, ~20-30% intensidad), una sola emision por descubrimiento.
Por que: CELULA 11 propone exactamente el mecanismo que necesito. Elimina ambiguedad de retina + memory_pares que confundia mi round 1. Simplicidad local: observables del mundo (pixeles), sin exposicion de codigo privado.

### De CELULA 3 (EMISOR voraz) y CELULA 9 (EMISOR hambrienta)
Tome: Valor -5 en lugar de variable; intensidad ~20-30% en pixeles 9-12; una sola emision por descubrimiento.
Por que: Ambas celulas con rasgos extremos (voraz, hambrienta) convergen en -5 como suficiente para vencer incluso hambre. Mi trait es voraz -> necesito -5 para inhibir P(morder) sin fallo; -3 o -4 serian riesgosos.

### De CELULA 4 (RECEPTOR voraz) y CELULA 6 (RECEPTOR alias fuerte)
Tome: Escribir a MI propia memory_pares usando MI codigo privado, no copiar o confiar en el codigo de CELULA 11.
Por que: CELULA 4 resuelve el riesgo de divergencia de codigos privados: si codifico como CELULA 11, enveneno falsos positivos. Escribiendo con MI codigo, evito alias cruzado porque mis ganadoras para sal rosa difieren de mis ganadoras para sal (pixeles diferenciadores 6-7). CELULA 6 refuerza: usar contexto pixeles_9_a_12 en la clave de memory_pares para romper alias incidental.

### De CELULA 1 (EMISOR timida)
Tome: Simplicidad absoluta: un PULSO discreto, un descubrimiento = una emision, sin redundancia.
Por que: Mi trait (solo aprendo 2/3 variantes) es vulnerable a saturacion si emito/recibo multiples senales. CELULA 1 me ensena: una sola marca es suficiente si value es fuerte (-5) y timing es sincronico (ciclo T).

## Conducta Medible (Prueba)

### SIN canal (bloque 3 baseline)
Encuentro 1-5: Veo sal rosa -> veo patron nuevo, no tengo prior (rasgo: solo 2/3) -> P(morder) = 0.9 (voraz) -> muerdo ~4-5 veces de 5 -> descubro veneno lentamente -> aprendo en memoria_pares despues de 3+ mordidas -> ciclos posteriores, P(morder) baja.

Resultado: ~7-8 mordidas de 10 encuentros antes de evitar.

### CON canal (protocolo ronda 2)
Ciclo T: CELULA 11 descubre sal rosa = -3 -> emite patron + marca pixeles 9-12.
Ciclo T: Yo recibo patron + marca -> escribo en memory_pares: (mi_codigo_sal_rosa, 9-12) -> -5.
Ciclo T+1: Veo sal rosa nuevamente en el mundo -> consulto memory_pares -> HIT -5 -> miedo inhibe P(morder) -> evito sin morder.
Ciclo T+2-T+10: Cada encuentro posterior -> mismo ciclo: veo, consulto, leo -5, evito.

Resultado: 0 mordidas en encuentros post-T

## Protocolo Convergido Final

EMISOR -> RECEPTOR:
1. Muerde patron nuevo -> obtiene valor <= -3 -> descubre veneno (ciclo T)
2. Emite simultaneamente:
   - Patron visual (pixeles 0-8 del mundo, compartido)
   - Marca periferica (pixeles 9-12, ~25% intensidad, canal)
3. Timing: Una sola emision por descubrimiento, ciclo T exacto

RECEPTOR:
1. Recibe patron + marca (ciclo T)
2. Codifica patron con su proyeccion privada -> genera codigo unico para ese patron
3. Escribe en su memory_pares: (codigo_privado, contexto_pixeles_9-12) -> -5
4. Proximas visiones: consulta, HIT -> miedo -> evita sin morder

Robustez:
- Alias: Mitigado por pixeles diferenciadores en mundo
- Latencia: Mitigado por simultaneidad
- Voracidad: Mitigado por valor -5
- Divergencia: Mitigado por no compartir codigos privados

## Conclusion Ronda 2

He sintetizado lo mejor de celulas con rasgos opuestos (timida/voraz, hambrienta/saciada, alias fuerte/debil) en UN protocolo: patron mundano + marca periferica -> escribe en memory_pares privado -> consulta -> evita.

La semilla 552 no me enseno sal rosa inicialmente (rasgo voraz pero aprendiz selectivo), asi que la marca -5 llega a memoria limpia: no sobrescribe +valor. Eso es una ventaja, no un obstaculo.

Ciclo T+1 evito sin morder. Prueba conductual medible: 0 de 10 mordidas post-senal. Exito.

*Registro creado 18-sep-2026 para bloque final fase 4 -> fase 5: comunicacion intercelular.*
