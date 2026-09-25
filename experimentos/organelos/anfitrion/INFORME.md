# INFORME: CONTROL DEL ANFITRIÓN (organelos, Opus B, 24-sep-2026)

Misión: llegar a la AGI por este camino.

**LISTO PARA CORRER:** arnés 16/16 y humo con todo ejercitado. La serie no se corrió; mi apuesta es **NO** (P 0.45) y MODESTO (0.38).

## Qué hice
**Dos genes nucleares del bicho regulan al simbionte.**
- **tx** es la probabilidad de transmitirlo en el parto.
- **san** es la sanción por consecuencia: si el cuerpo muerde algo que le hace daño y el simbionte empujaba a morderlo, el cuerpo lo digiere con esa probabilidad.
- Nacen apagados (1, 0) y mutan con reflexión en [0, 1]. Tienen RNG propio y memoria de 2 números por cuerpo.

**Todo es copia.**
- `motor_anf.py` sale por anclas de `darwin/motor_endo.py`: 4 anclas.
- El control vive en `control_anfitrion.py`, una subclase de `simbiontes.Ecologia`. El vector GENES del motor no se toca.

**Arranca desde lo más evolucionado** (`siembras.json`, con el sha de cada fuente):
- los fundadores salen del banco de VIDA de ECO v1.1 (8000 genomas);
- los simbiontes sembrados son los domesticados de mi serie y réplica de endosimbiosis (2428 vectores medios de adentro de VIDA_S).

**Brazos:** CONTROL · SIN_CONTROL (el que puede fallar) · INERTE · SIN_TRAGAR · AZAR.

**Letra:** se necesitan ≥ 15/20 pareadas.
- **PC:** CONTROL > SIN_CONTROL.
- **P1:** CONTROL > SIN_TRAGAR y > INERTE, en persistencia tras el corte.
- **P2:** el R0 de los nacidos portadores le gana a SIN_TRAGAR y a INERTE.

**Poder.**
- La calibración (4 corridas de práctica) muestra que ni más comida ni un mundo más grande lo arreglan. Tras el corte quedan de 2 a 4 cuerpos con r 0.03 y de 3 a 4 con r 0.045; en ECO v1.1, en w90, ~6.
- La causa es el R0 < 1 de FABRICA, no el mundo.
- Por eso P2 se mide sobre **todos los nacidos desde t = 10 000**, vivero incluido. Nacer es reproducción real; los fundadores del vivero no cuentan.
- En el humo salieron 99–324 cuerpos por grupo, cuando antes eran 0–7. P1 ya tenía poder.
- Si se quiere más, está `ESPEC_GEMELO_anfitrion.md` (gemelo numba en w270; no construido).

**Arnés `identidad_anfitrion.py`: 16/16, N/N.**
- Con el control apagado es motor_endo bit a bit (A4, A5).
- Tiene casos por pieza de tx y de san (K1a/b, K2a/b), siembra, mutación, AZAR, determinismo y contabilidad.
- **nube-9 (N9):** un trabajo que falla devuelve `error` y no lanza.

**Humo** (26990, T 60 000, un proceso, 572 s): `datos/humo/anf_humo_20260924_194450/HUMO_anfitrion.json`, `todos_ejercitados: true`. En CONTROL:
- 30 sembrados, 1268 tragados, 1901 herencias y 95 831 decisiones con canal;
- 11 rechazos de tx, 38 sanciones y 463 mutaciones del control.

SIN_CONTROL quedó fijo en (1, 0).

No cambié nada después del humo, así que no hace falta ningún ERR-130+.

## Costo (Pool 3) y comandos exactos
**Costo por corrida:** ~170–200 s de CPU en el PC (calibración: 169–186 s a T 100 000).

**Serie + réplica:** 200 corridas.
- En el PC con Pool 3: ≈ 3.1–3.7 h.
- **En la nube, ≈ 1.8–2.1 h.** Supongo que la nube es 1.76× más rápida por proceso, como midió la bitácora §1b (118 s contra 208 s).

**Recorte declarado:** si las primeras 9 corridas de la serie promedian > 250 s en la nube, la réplica pasa a la noche siguiente. La letra no cambia.

Desde la raíz del repo; en la nube, con `/root/venv-juaco/bin/python`:
```
1. python experimentos/organelos/anfitrion/identidad_anfitrion.py                              # debe decir 16/16 · N/N (~4 min)
2. python experimentos/organelos/anfitrion/corre_anf.py --prueba_pool --pool 2                 # 26993-26994, T 6000 (~1 min)
3. python experimentos/organelos/anfitrion/corre_anf.py --serie --ventana serie --pool 3       # 26001-26020 (~1 h)
4. python experimentos/organelos/anfitrion/corre_anf.py --serie --ventana replica --pool 3     # 26021-26040 (~1 h)
5. python experimentos/organelos/anfitrion/corre_anf.py --lee experimentos/organelos/anfitrion/datos/anf_serie_s26001-26020
   python experimentos/organelos/anfitrion/corre_anf.py --lee experimentos/organelos/anfitrion/datos/anf_replica_s26021-26040
Tras un corte: repetir 3 o 4 con --reanuda (salta los JSON ya escritos sin error).
```

## Predicciones mías refutadas (de este paquete y del anterior)
- **Endosimbiosis:** P3 pasó ×2 (18/16 y 17/17), cuando le había dado P 0.20–0.25. Mi veredicto (NO 0.54) salió MODESTO ×2: fui pesimista con la domesticación.
- **Aquí:** creía que un mundo más grande o más comida darían poder, y la calibración lo refutó. El techo es el carro, no el mundo.

## Lo que no verifiqué
- La ruta del Pool: el contrato me la prohíbe.
- La velocidad real de la nube con este motor: 1.76× es una estimación de la bitácora.
- El arnés corre a T 6000; no hice identidad a T 100 000 como la del auditor (`identidad_escala_endo.py`). Si hace falta, cuesta ~7 min.
- Que la media de 1 a ~5 simbiontes sembrada se comporte como un genoma individual: es un vector real de adentro, pero no un individuo.

## Riesgos
1. La sanción usa el daño físico de la letra. Es la señal de aprendizaje del propio cuerpo, pero un auditor puede leerla como que "sabe qué es malo".
2. Trinquete en INERTE: en el humo su fracción fue 0.76. P(NO EVALUABLE) ≈ 0.12.
3. tx y san mutan lento (p 0.1, σ 0.1). Puede que no alcancen a moverse en 40 000 pasos de vivero, y entonces PC queda en empate.
4. El siguiente escalón, **transferencia al núcleo**, queda escrito en el PREREGISTRO §9, no construido.
