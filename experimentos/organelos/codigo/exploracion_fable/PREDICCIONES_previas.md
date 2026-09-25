# EXPLORATORIO, no es dato

# Predicciones del explorador Fable ANTES de ver la tanda 1 y 2 (24-sep-2026, 20:50)

TL corto: T 36 000, cambio 8 000, corte 24 000, margen 4 000. Semillas 28001–28003. CODIGO vs PERILLAS pareado por semilla.
Aviso de honestidad: con 3 semillas, «gana 2/3» pasa por azar la mitad de las veces; «3/3» pasa 1/8. Sólo un 3/3 se re-prueba con 28004–28006.

| mundo | predicción (nac post/pre, persistencia) | P(CODIGO gana R0 final en ≥ 2/3) |
|---|---|---|
| golpe (control) | nadie se recupera (post/pre < 0.5); persisten 0–1/3 en cada brazo; replica a Opus | 0.45 (= azar) |
| gradual8k, gradual16k | los dos suben (post/pre 0.5–0.9) porque A pica poco al principio; persistencia 1–3/3 | 0.35 |
| alterna4k, alterna8k | nacimientos en dientes de sierra; persistencia 0–1/3; la SOS se prende en cada vuelta | 0.35 |
| onda8k | mejor que alterna (sin saltos); persistencia 1–2/3 | 0.35 |
| suave (A neutro, B +0.4) | los dos viven; post/pre 0.6–1.0 | 0.35 |
| bonanza (B comida, A sigue) | los dos viven, post/pre ≥ 1; PERILLAS explota B antes (llega a «invertir» 13× más seguido por p_campo) | 0.30 |
| medio_veneno (A −0.2, B +0.8) | intermedio entre golpe y suave; persistencia 0–2/3 | 0.40 |
| zona_mitad | los dos viven a medias (la otra mitad del anillo es el mundo viejo) | 0.40 |
| escalera4 | como gradual8k | 0.35 |
| deriva8k | como suave pero lento | 0.35 |
| reina | 2–4 intercambios antes del corte; extinción casi segura después del corte | 0.40 |
| alterna2k | el peor: nadie aprende nada; extinción antes del corte | 0.40 |

Global: P(encontrar 2–3 mundos con CODIGO ganando en la mayoría de 3 semillas) ≈ 0.35, y la mitad de esos serán azar.
Mecanismo que creo que se selecciona si algo gana: el ORG con `como = invertir` (la tabla heredada al revés) o `que = reciente`.
