# INFORME — muro (creador, 25-sep-2026, 15:40–16:50). LISTO PARA SERIE. Tiro largo, y lo digo de entrada. Sin serie, sin Pool, sin git.

Misión: llegar a la AGI por este camino. Preregistro: `PREREGISTRO_muro.md` (sha 35fe4a7a2942102d, escrito antes del humo).

**Veredicto del trabajo de la tarde: NO HAY un candidato con señal.** Ninguna pieza sola le ganó a V143 en ≥ 4/5 en lo exploratorio. Entrego
el mejor de una sola pieza, **GLOTU**, que ganó 3/5 con +0.016. Espero NO (p 0.75).

**Qué hice**
- **Diagnóstico** (serie frio_carrera, O1 contra V143 en los mismos mundos, más una traza propia de mordidas):
  - el fundador de V143 muere a los ~45 pasos; O1 a los 200;
  - el fundador de V143, sin meta y con hambre, vuelve a morder B sabiendo que le quita energía: 461 de 668 decisiones en s37901, T 30 000;
  - el hijo de V143 muerde poco malo y muerde A sediento a tasa ≈ 1 (O1 0.09).
- **Cinco familias de una pieza.** Todas se construyen por anclas desde V143.py (2a03048a7f1525e5), nacen inertes (== V143 bit a bit) y
  se probaron con 5 semillas de práctica (37901–37905), T 100 000, un proceso por corrida y ≤ 8 a la vez. Tabla en §8 del preregistro:
  - contención de lo malo: PAGA / CONT / SINEST por filas; CTA / LIMPIA / SINEST / DESF por lo sentido → todas hunden, de −0.28 a −0.71;
  - GLOT: no comer lo que sólo sirve a la necesidad no activa → 0/5, −0.09 (mata de hambre);
  - PATAS: las patas van a lo que sirve a la necesidad activa → 1/5, −0.02 (casi inerte: las filas generalizan);
  - **GLOTU**: no comer lo que sólo sube la necesidad MÁS llena cuando ya pasó el umbral de parto → **3/5, +0.016**; vida 1448 contra 600;
    A+C 537 contra 812.
- **Paquete** (en `experimentos/organelos/muro/`):
  - `construye_muro.py` (ad607c6ad4f9ced9);
  - `corre_muro.py` (503b531ea1213c59): la corrida ES `corre_v143.tarea`; nube-9, `--reanuda`, ERR-115; la letra está en `lee_serie`;
  - `identidad_muro.py` → **108/108** (`identidad_muro_salida.txt`, 110 s);
  - `explora_muro.py` (sólo exploratorio). Brazos de la serie: V143, GLOTU (CANDIDATO), GLOTUINV (CONTROL desfasado) y O1.
- **Humo** (1 proceso, 6 corridas, T 20 000, 302 s; JSON en `datos/humo/…163923/`):
  - regla 14 OK ×2; identidades del juez y de v14.3 OK;
  - GLOTU 0.303, V143 0.50 (pierde 2/2 a T corto), GLOTUINV 0.000, O1 0.667;
  - V4 (la pieza actúa) True; no se lee.

**Costo:** 80 corridas por serie, **35–45 min con Pool 6**; la réplica cuesta lo mismo.

**Comandos (el coordinador)**
```
python experimentos/organelos/muro/construye_muro.py --verifica
python experimentos/organelos/muro/identidad_muro.py                                     # 108/108, ~2 min
python experimentos/organelos/muro/corre_muro.py --serie --desde 37001 --n 20 --pool 6
python experimentos/organelos/muro/corre_muro.py --serie --desde 37021 --n 20 --pool 6     # replica
python experimentos/organelos/muro/corre_muro.py --bloque <resumen serie>,<resumen replica>
```

**Lo que aprendí (exploratorio, no dato)**
- **Todo lo que le quita al fundador la mordida "desesperada" de lo malo baja el establecimiento** (de 32/45 a 3–23/45). En esta pista,
  morder lo malo sin meta repone el mundo; no es sólo suicidio.
- **Comer menos, sólo, no basta.** GLOTU come un 34 % menos y vive 2.4× más, pero el R0 real apenas se mueve.
- **Segundo intento (22:00), si el coordinador quiere:** GLOTU + PATAS ganó 4/5 (+0.03, por semilla 0.69–0.88). Son dos piezas, así que
  NO lo preregistré. El carro `V143_GLOTUPATAS` está construido y pasa el arnés; necesitaría su propia línea de preregistro.

**Qué falló / declaraciones**
- **Un caso del arnés estaba mal diseñado antes del humo:** exigía PATAS != V143 a T 3000. En s37908 PATAS es físicamente == V143 hasta
  T 3000. Lo corregí a informativo.
- El exploratorio de las rondas 2–5 se corrió con carros de sha anterior. Después sólo cambié el texto del encabezado y la línea de
  perillas (GLOT/PATAS = 0); la física es la misma por construcción. No lo re-corrí.
- El log del humo imprime "PAGA = GLOT = TELEM = 0" en la identidad corta; el código también pone PATAS = 0. Es cosmético y no lo toqué.
- Al pasar de la ronda 3 a la 4 pudo haber 9 procesos durante unos segundos: la espera era de 9 de 10 archivos. Lo declaro.
- ERR: ninguno tras el humo (no cambié nada después).

**Predicciones refutadas (mías, del día):**
- que la contención de lo malo (CTA) ayudaría al fundador;
- que GLOT (glotonería por identidad) le ganaría a V143;
- que PATAS movería algo.

**No verificado:**
- Pool/spawn en Windows (es el patrón de `corre_v143`, sin probar aquí);
- el control GLOTUINV en más de 2 semillas;
- `comite2/puenteo/` con más de una semilla (seguía corriendo).

---
## SEGUNDO INTENTO (GLOTU + PATAS), 16:45–17:00. LISTO PARA SERIE. Preregistro `PREREGISTRO_muro2.md` (firmado sha 4098ff690c556ee5 + adenda)
- **Instrumentos.** No toqué los de la serie 1 (corre_muro 503b531ea1213c59, construye_muro ad607c6ad4f9ced9).
  - `construye_muro2.py` genera sólo el control `V143_GLOTUPATASDESF`.
  - `corre_muro2.py` importa corre_muro y cambia en memoria brazos, semillas, humo y carpeta; la letra es la misma.
  - Arnés `identidad_muro2.py` **66/66**.
- **Humo2** OK (regla 14, identidades); no se lee.
- **Brazos:** v143, glotupatas (CANDIDATO), glotupatasdesf (CONTROL: GLOTU + patas a lo que sirve a la OTRA necesidad) y o1.
- **Semillas:** 37101–37120 y 37121–37140.
- **Puenteo** (4 semillas): las piezas de O1 solas dan 0.949 (patas) y 0.907 (boca_buena), contra 0.651 de V143. **No contradice la
  dirección de la combinación, pero sí la dosis.** Mis traducciones solas suben +0.016 y −0.02: no capturan el ingrediente activo, que es,
  sobre todo, no llevar el cuerpo encima de lo malo sin meta. Espero NO (p 0.72).
- **Exploratorio del control, después de firmar:** candidato > control 5/5 (+0.07). Q4 (control ≈ candidato) probablemente refutada.
