# N3d mudo — ¿obedece o aprende? El receptor ciego por construcción, sin el emisor (escrito ANTES de correr; semillas 61–80)

**18 sep 2026 (madrugada del día 6).** N3d demostró y replicó que el receptor ciego a la regla acierta 0.82 con la conducta
reciente del que ve. Falta saber **qué queda cuando el emisor calla**: si la señal sólo gobierna la decisión (obediencia) o
si además arranca aprendizaje propio. Knob `mudo_desde` en `mundo_social_n3.run`: desde ese paso no se entrega ninguna
señal (`mudo_desde = None` ≡ N3d exacto, identidad obligatoria). Las mismas semillas 61–80 de N3d: los primeros
150 000 pasos son **la misma trayectoria** que CONV de N3d (pareado por construcción); el último cuarto (150 000–200 000)
transcurre sin señal.

Condiciones: **CONV_MUDO** (`mudo_desde = 150000`), CONV (referencia, = N3d), SOLO_R (referencia). Medida: acierto
balanceado del receptor en Q4; `n_sesgo_soc` en Q4 debe ser ≈ 0 (las señales oídas caducan a los 400 pasos).

**Predicción (ciego por construcción → obediencia):** CONV_MUDO en Q4 ≤ **0.60** (mediana) y < CONV pareado en ≥ 15/20;
no distinguible de SOLO_R (|diferencia| de medianas < 0.10). **Refutación:** CONV_MUDO ≥ 0.70 en Q4 sin señal → el canal
dejó aprendizaje propio (habría que explicar con qué, porque la vista no puede saber) → se registra como anomalía y se
busca la fuga (posiciones fijas + memoria de rechazo, por ejemplo). Vocabulario si pasa: *la conducta ajena gobierna la
decisión; no enseña*. Un mundo donde el receptor **pueda** aprender pero lento (para preguntar si la señal lo arranca)
queda para después: no existe todavía (en N3c el receptor solo ya sabe; en N3b no encuentra comida).
