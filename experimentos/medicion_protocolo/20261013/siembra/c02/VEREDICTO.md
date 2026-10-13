# VEREDICTO — entrada del registro

Copiada de `registro/REGISTRO_etapas_1_2.md`, líneas 2225–2267.

---

### DECISIÓN DELEGADA (dirección: "decide tú") — v10 = v9 + dirección de división con `mu` normalizada

Preregistro `experimentos/v10_direccion_division/PREREGISTRO_v10.md` (`0e035dc12f3fffd3`, commit `296d1ac`).
Instrumentos commiteados antes de correr (`51de86d`): `organismo_v10.py` `219d5033fe15b5b9` (diff funcional con v9:
la firma y **una** línea), `bateria_v10.py` `d354813d3fa9d0f1` (23 líneas de nombres, ningún criterio), `v10m`
`c33253b850570308`. Datos: `datos/v10_confirmatorio_20260916_175557.json` (`ea0fd051edf61d0a`),
`datos/examen_v10_20260916_175716.json` (`d2f6de7350514291`) y sus `.log`.

| criterio | veredicto | cifra |
|---|---|---|
| Q0 identidad | ✅ | `v10(mu_norm=False)` ≡ v9 42/42; `v10m` ≡ v10 6/6 |
| **Q1** examen criterio v3 | ✅ **8/8**, seis etapas 20/20 | |
| **Q2** economía de la plasticidad | ✅ | **E2 y E2L terminan con exactamente 3 divisiones en 20/20** (v9: medianas 5 y 6) |
| **Q3** vía estructural (semillas 21–40) | ❌ **REFUTADA como está escrita** | hijas en B: v9 14/20 ✅, **v10 6/20 (pedía ≤ 5)**; ΔW_B v10 < v9 en **11/20 (pedía ≥ 12)**; v10 peor por > 0.5 en **1 semilla (pedía 0)** |
| Q4 retención, con guarda | ✅ | `W_B ≤ −2`: v9 7/20 → v10 **12/20**; `W_C`, `W_D` aprendidos 20/20 |
| Q5 regresión | ✅ | `bateria_v9.py 6` cumple; 8 congelados intactos |

**Por la letra del preregistro, v10 NO se congela.** Nada se recalibra.

**Descriptivo, que importa:** ΔW_B mediana +2.24 (v9) → **+0.86** (v10); `W_B` al volver −0.69 → **−2.06**; celdas hijas en
el código de B: 32 → **8**; muerde B al reencuentro 9 → 5; divisiones en la corrida 6 → 3.

### ERR-17 — los tres subcriterios de Q3 estaban mal escritos, cada uno por una razón distinta

Diagnóstico desde el JSON (`scratchpad`, sin simular), regla 5:
1. **Los empates contaban como fallo.** `mu_norm` sólo actúa **al dividir**. En **6/20** semillas ninguno de los dos
   brazos dividió durante la ausencia, así que ΔW_B es **idéntico por construcción** (v10 = v9 exacto). Entre los 14
   pares no empatados, v10 es menor en **11/14**. El criterio "≥ 12/20" exigía que v10 ganara también donde no
   podía diferir. Es la familia de ERR-11/16: un criterio que no puede cumplirse por construcción en parte de la
   muestra.
2. **El umbral de hijas contradecía la evidencia declarada.** Escribí "v10 ≤ 5/20" habiendo declarado en §0 que la
   exploración daba "0 hijas en 11/20", es decir, **hijas en 9/20**. El umbral era inconsistente con mi propio prior.
3. **Tolerancia cero sobre una diferencia pareada estocástica** ("nunca > v9 + 0.5"). Con 20 pares y una cola larga
   de divisiones (v9 llega a 19 divisiones en una semilla), un caso al revés no refuta nada. Es ERR-14 otra vez (banda
   más estrecha que el ruido).

**Qué se decide, antes de volver a correr (regla 3):**
- v10 sigue **sin congelar**. El examen (Q1, Q2) y Q4 valen y no se repiten.
- Criterio Q3 corregido, para una **réplica en semillas nuevas 41–60**, escrito desde el mecanismo y no desde las
  cifras de 21–40: (a) entre los pares **no empatados**, v10 < v9 en ≥ **70%**; (b) semillas con ≥ 1 hija en el código
  de B: v10 ≤ **la mitad** de v9 (pareado en recuento) y ≤ 9/20; (c) v10 peor por > 0.5 en ≤ **2/20**. Se corre sólo
  si dirección decide seguir; si pasa, v10 se congela.
- Se declara que los datos de 21–40 se vieron antes de escribir (a)–(c).
