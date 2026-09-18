# N3d — sentidos complementarios con un receptor ciego POR CONSTRUCCIÓN (escrito ANTES de correr; semillas 61–80)

**17 sep 2026, noche del día 5.** N3c (`N3c_s41-60_20260917_195528`) fue **montaje inválido** (S4): en el mundo con
reaparición en el mismo sitio, el receptor que ve sólo los píxeles 3–5 llega **solo** a 0.997, porque con 8 objetos
fijos memoriza sus 8 vistas y ya no necesita la regla (la vista 3–5 lleva información parcial de `px0` y con 8 objetos
suele bastar). Lo que sí quedó: la conducta ajena **manda** en la boca del receptor (barajada 0.683 y emisor que no
sabe 0.689, los dos con 20/20 pareados contra la honesta 0.957). Falta la pregunta limpia: ¿le sirve al que **no puede
saber**?

## Único cambio: los 8 objetos son 4 PAREJAS con la misma vista para el receptor y valencia opuesta

Para cada semilla se eligen 4 vistas de los píxeles 3–5 (de las 6 posibles con uno o dos píxeles activos) y para cada
vista un patrón **comida** (`px0 = 1`) y un patrón **veneno** (`px0 = 0`) de peso 3 con exactamente esa vista. Knob
`tipos_fijos` (los 8 tipos iniciales en vez de sortearlos; con `regen` no entra ningún otro tipo). Por construcción, la
vista del receptor **no distingue** comida de veneno: SOLO_R debe quedar ≈ 0.50 (validez S4 por construcción, no por
resultado). El emisor ve 0–2 y sí distingue (`px0`). Todo lo demás es N3c.

## Criterios (los de N3b/N3c) y predicción

S1: CONV ≥ 0.80 y > SOLO_R pareado ≥ 15/20 · S2: > SHUF ≥ 15/20 · S3: > SACIEDAD ≥ 15/20 · S4: SOLO_R ≤ 0.75, TECHO y
SOLO_E ≥ 0.80, emisor en CONV ≥ 0.90 · S5: N0 no > SOLO_R en ≥ 15/20. **Predicción:** pasan S1–S5: con visitas
equilibradas y vista inútil, la conducta del que ve es la única fuente y el receptor la usa (≥ 0.80). **Refutación:** S1
falla (el receptor no llega a 0.80 o no supera a su versión sola). Si pasa: "*transferencia entre sensores por
conducta*" queda demostrada en 20 semillas; réplica en 81–100 antes de cerrar. Sin recalibrar después.
