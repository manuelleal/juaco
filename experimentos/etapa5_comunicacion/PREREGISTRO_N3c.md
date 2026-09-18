# N3c — sentidos complementarios en un mundo que no se come la pregunta (escrito ANTES de correr; semillas 41–60)

**17 sep 2026, noche del día 5. Escrito mientras corre N3b y antes de ver su veredicto.** El humo de N3b (semilla 22)
ya muestra el problema siguiente, que no es del organismo ni del canal sino del **mundo**: el receptor visitó **210
comidas y 9 617 venenos** en el último cuarto. El emisor se come la comida en cuanto reaparece (al azar, en otro
sitio) y el veneno se queda; el receptor casi nunca llega a probar una comida de la que acaba de oír "+". Es la misma
asimetría que cerró N2 ("reabrir sólo cambiando el mundo: comida que no desaparece, o veneno que sí").

## Cambio de mundo (instrumento `mundo_social_n3.py`, knob `regen`; `regen = None` ≡ N3b exacto)

Los objetos **reaparecen en el mismo sitio con el mismo tipo** `regen = 50` pasos después de morderlos (o del olvido de
v9); ya no reaparecen al azar. Con 8 objetos fijos (4 por organismo) las visitas a comida y a veneno se equilibran, y
lo que el emisor mordió vuelve a estar donde el receptor puede probarlo tras oírlo. Todo lo demás es N3b: regla `px0`,
emisor ve 0–2 y **no escucha**, receptor ve 3–5 y escucha (`gamma_soc = 1.5`, `tau_soc = 400`), acierto **balanceado**,
`d_senal = 5`, `f_vicaria = 1/3`, T = 200 000. Identidad: `regen = None` ≡ N3b (todas las claves, semillas 1–3, n = 1 y n = 2).

## Criterios (idénticos a N3b) y predicción

S1: CONV ≥ 0.80 y > SOLO_R pareado ≥ 15/20 · S2: > SHUF ≥ 15/20 · S3: > SACIEDAD ≥ 15/20 · S4: SOLO_R ≤ 0.75, TECHO,
SOLO_E ≥ 0.80, emisor en CONV ≥ 0.90 · S5: N0 no > SOLO_R en ≥ 15/20. **Predicción:** con visitas equilibradas, S1–S5
pasan. Si N3b ya pasara, N3c es la réplica en otro mundo; si N3b falla y N3c también, la transferencia por conducta
**no** basta para un receptor estructuralmente ciego y se cierra la línea social por hoy con eso escrito. Nada se
recalibra después.
