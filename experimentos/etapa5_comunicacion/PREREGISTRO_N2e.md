# Etapa 5, N2e — quinto intento: el significado también se aprende por ALINEACIÓN con lo que uno ya sabe

**Escrito ANTES de modificar el instrumento y ANTES de correr. 17 sep 2026, noche del día 5.** Regla 12.

## 0. Por qué se anula la cláusula de cierre de N2d

N2d (`N2d_s1-20_20260917_184830`): E1 13/20, E3 12/20 ✅, **E4 pareado 15/20** (CONV mejor que N0 en 15 semillas; mediana
249 = 0.79 × N0), E5 ✅, pero **E2 1/20** (contraste −0.34 / +0.27). La cláusula de N2d decía "si E2 < 10/20 con E1 ≥ 13/20
se cierra la línea por hoy". Se anula porque un diagnóstico instrumentado (semilla 4, sin tocar el mecanismo) encontró
una causa que la cláusula **no anticipó** y que no está en el organismo sino en el **muestreo del mundo**:

| | veneno | comida |
|---|---|---|
| emisiones del experto (estado 0 / 1) | **36.365** | **564** |
| símbolos oídos por el novato | 10.092 (s=0) | **88** (s=1) |
| actualizaciones de `M` por consecuencia propia | 19 (s=0 → mordió veneno) | **8** en total para s=1 (2 comida, **6 veneno**) |

La comida **se come y desaparece** (una visita, una emisión); el veneno **se rechaza y se queda**, y el experto lo vuelve
a pisar miles de veces. El novato oye "positivo" 113 veces en 200.000 pasos y sólo muerde algo después de un "positivo"
**8 veces**; con 8 muestras (y 6 de ellas venenos por sus propios errores) `M[positivo]` queda en −1.1 y el contraste en
±0.7. **La convención es perfecta (consistencia 1.00) y el receptor no tiene con qué aprenderla.** No es un problema de
umbral ni del emisor.

## 1. Qué cambia (una cosa, derivada del diagnóstico)

**Alineación:** al oír el símbolo `s` sobre un patrón `kk` que el receptor **ya conoce por experiencia** (familiar a su
vía rápida: ≥ 3 celdas consolidadas, la prueba de la puerta), `M[s] += eta_m · (valor_propio(kk) − M[s])`. Es decir, el
símbolo toma el valor de lo que ya sé. Se conserva el aprendizaje por consecuencia (N2). Local, sin constante nueva
(`eta_m = 0.1`, la misma). Es aprendizaje cruzado de situaciones: oír "peligroso" sobre lo que ya sé que es peligroso.
Todo lo demás igual que N2d.

## 2. Criterios: los mismos de N2–N2d, sin tocar un umbral. Réplica en 21–40 si pasa.

## 3. Predicción
- **E2 sube:** con ~10.000 oídas de "negativo" sobre venenos conocidos y ~90 de "positivo" sobre comidas conocidas,
  `M → [−3, +1]` y el contraste a ±2 en **≥ 12/20** (E2). **E4 ≤ 0.7 × N0** (el sesgo pasa de ±0.4 a ±2 y el novato rechaza
  lo señalado como negativo antes de morderlo). **E1 ≥ 15/20** (el emisor recibe más refuerzo diferencial).
- **Refutación:** si E2 < 10/20, la alineación no basta y el cuello es la escasez de "positivos" (el mundo); entonces
  la línea N2 se cierra con "emerge en signo, no en magnitud, por asimetría del muestreo del mundo", y el siguiente
  mundo debe equilibrar visitas (comida que no desaparece al morderla, o veneno que sí). Nada se recalibra.
