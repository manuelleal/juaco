# PREREGISTRO — JUACO-ECO v2.1: ¿la selección PRENDE el órgano de enseñar? con la prueba de EXPRESIÓN contra sombras (24-sep-2026, coordinador de la nube; antes de cualquier serie de v2.1)

Misión: llegar a la AGI por este camino. Carpeta: `experimentos/juaco_eco/`. Nivel 10, frente 2. Archivos nuevos; nada del PC se toca.
ECO v2 (serie 20011–20030) quedó HAY ALGO MODESTO por la letra (su réplica 20031–20050 corre con la misma letra y no se recalifica). Esta
versión corrige el instrumento que falló (candidato nube-8) y se corre en **semillas nuevas**.

## 0. Instrumento (sha a 16)
- Mismo motor, carro y gemelo que v2: `motor_eco2.py` (0921ee3a50ce7f7a), `carros/FAMB_ORG_ECO.py` (75d5f4118079ff15), gemelo
  `motor_eco_rapido_org.py` (024f0a8ea5e12c7d; arnés 99/99).
- Runner `corre_eco_v21.py` (= `corre_eco_v2.py` + la captura de la expresión en el corte + la letra de §6; el sha va en el log) y su arnés
  `identidad_eco_v21.py`: (M) mundos, brazos, ventanas; (T) medidas a mano; **(S)** la expresión del corte sale del checkpoint y el real
  coincide con el banco del motor; **(G)** gemelo == Python en los tres mundos y los dos brazos, con la expresión incluida; (V) la letra;
  (R) banderas.

## 1. Qué falló en v2 y qué cambia (sólo el instrumento)
- **nube-8:** O1 de v2 comparaba la MEDIA del gen en el banco con la de sus 8 sombras. Para un rasgo con umbral la selección sólo necesita
  pasar 1.0; las sombras neutrales derivan libres. En la serie de v2, con el 98–99 % del banco de VIDA expresando `ensena` (AZAR 41–43 %) y
  ~100 % de los vivos, O1 dio 12 y 13/20 en w90 y w270.
- **v2.1:** el checkpoint del corte (t = 60 000) trae el estado completo, con el banco de pares (genoma, 8 sombras). El runner calcula la
  fracción del banco que EXPRESA cada órgano en el genoma real y en cada sombra. **O1\*:** en VIDA la fracción real supera a la MEDIA de las
  8 fracciones sombra (estricto) en ≥ 15/20. Bajo la nula (real y sombras intercambiables; ~35–45 % de las sombras quedan prendidas por
  deriva) pasa con p ≈ 0.4 por semilla: P(≥ 15/20) ≈ 1e−3. Guardia nueva: si AZAR supera así a sus sombras en ≥ 15/20, NO EVALUABLE.
- Todo lo demás igual que v2: tres mundos (esc 30, 90, 270), VIDA y AZAR, corte 60 000, T 120 000, O2 (VIDA expresa más que AZAR).

**Dato visto antes de escribir esto (declarado):** la serie de v2 (arriba). La predicción sale de ahí; el umbral, de la nula.

## 2. Semillas NUEVAS (grep del 24-sep: sin usos 20200–20299)
Serie **20211–20230**; réplica **20231–20250**; práctica 20291–20299 (humo 20291; prueba del Pool 20292–20293; arnés 20294).

## 3. Predicciones firmadas
| cantidad | rango | probabilidad |
|---|---|---|
| **O1\* `ensena` en VIDA, por mundo — la que puede fallar** | 15–20 /20 | 0.80 por mundo |
| O2 (banco VIDA > AZAR), por mundo | 15–20 /20 | 0.85 por mundo |
| O1\* `filtra0` en VIDA, por mundo | 8–18 /20 | 0.35 |
| veredicto | FUNCIONA 0.75 · MODESTO 0.15 · NO 0.05 · NO EVALUABLE 0.05 | — |

## 4. Qué refuta
- **H (la selección prende el órgano de enseñar):** O1\* o O2 caen en 2 de los 3 mundos.
- **El instrumento:** AZAR supera a sus sombras (O1\*) en ≥ 15/20, o saca genes de sus sombras (> 8/20).

## 5. Auditoría propia (antes de correr)
1. La captura del corte depende de que el corte caiga en un múltiplo del paso de checkpoint (60 000 y 10 000): se verifica en el arnés (S).
2. O1\* no cuenta empates como victoria (si real y media de sombras son iguales, no gana): conservador.
3. El banco de VIDA es de pocos padres (casi clonal): la fracción real es casi 0 ó 1 por semilla; la media de 8 sombras independientes de la
   misma genealogía es la referencia justa para ese mismo banco.
4. O2 sigue sesgado EN CONTRA de VIDA (§7.6 de v2): conservador.

## 6. Criterio por la letra (`corre_eco_v21.veredicto`)
Por mundo m: **O1\*_m** (arriba) y **O2_m** (banco de VIDA expresa `ensena` más que el de AZAR, pareado, estricto, ≥ 15/20).
- **NO EVALUABLE:** serie incompleta; bloqueados > 0; AZAR con > 8/20 en algún gen contra sombras (media) o con O1\* ≥ 15/20.
- **FUNCIONA — LA SELECCIÓN PRENDE EL ÓRGANO DE ENSEÑAR:** O1\* y O2 en ≥ 2 de 3 mundos.
- **HAY ALGO MODESTO:** O1\* y O2 en 1 mundo, o alguno de los dos en ≥ 2.
- **NO:** otro caso.
El bloque se declara sólo si serie y réplica dan el mismo veredicto; si no, vale el menor. `filtra0` es secundario.
Vocabulario: «la selección prende el órgano»; prohibido «evoluciona», «cultura», «especie».

## 7. Costo
Igual que v2 con el gemelo: ~15 min de pared por serie con Pool 3.
