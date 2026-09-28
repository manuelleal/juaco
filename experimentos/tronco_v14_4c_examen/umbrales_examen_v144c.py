"""UMBRALES, SEMILLAS y PREDICCIONES del examen v14.4c: el CRITERIO DE TRONCO v4 sobre v14.4b = v14.3 + TERMO' (el MISMO
organismo que el examen v14.4b, sin tocar), con UNA sola enmienda de la letra: T-C (ii) POR VISITA (ERR-150). Un solo modulo (ERR-31).

Todo lo demas se IMPORTA de experimentos/tronco_v14_4b_examen/umbrales_examen_v144b.py (sha fijado en corre_examen_v144c.ANCLAS),
que a su vez importa la de v14.4 y la de v14.3: T-A, T-B (ERR-122), T-C (i), T-D, T-E, T-F, T-G y T-H SIN un numero cambiado.
La letra vieja de T-C (ii) (rev absoluto, margen 12.5) se sigue CALCULANDO y se REPORTA al lado; ya no decide en este examen.
Ningun numero de aqui se toca despues de correr; un cambio lleva ERR y fecha.
"""
import os, sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
_V144B = os.path.join(os.path.dirname(os.path.dirname(_AQUI)), 'experimentos', 'tronco_v14_4b_examen')
if _V144B not in sys.path:
    sys.path.append(_V144B)   # AL FINAL: no tapa nada
import umbrales_examen_v144b as U144B   # sha fijado en corre_examen_v144c.ANCLAS

NUM = dict(U144B.NUM); ERR122 = U144B.ERR122; TG = dict(U144B.TG)
ARMS_VIVO = list(U144B.ARMS_VIVO); ARMS_TA = list(U144B.ARMS_TA); BRAZOS_TA = list(U144B.BRAZOS_TA); ARMS_SAL = list(U144B.ARMS_SAL)
ORGS_EX = list(U144B.ORGS_EX); SEIS = list(U144B.SEIS); REGLAS_TB = list(U144B.REGLAS_TB)
T_VIVO = U144B.T_VIVO; T_HUMO = U144B.T_HUMO; DESPL_TRONCO_B = U144B.DESPL_TRONCO_B

# ---------------------------------------------------------------- ERR-150: la letra de T-C (ii) POR VISITA
# Nulo, margen y anti-TERMO: analiza_nulo_err150.py sobre los crudos YA EXISTENTES (examenes de v14.3 serie/replica y de v14.4 serie,
# OFF + TRONCO_B, 480 corridas; V4-CAL serie/replica, 320 mas; A-CAL para PLACEBO y PEOR). Ningun dato de TERMO'.
# JSON experimentos/tronco_v14_4c_examen/datos/nulo_err150_20260928_161728.json (sha a394a03bf9241b40).
ERR150 = dict(
    frase=("T-C (ii) POR VISITA (ERR-150): p_X[q] = (mordidas_X[q] + 1) / (visitas_X[q] + 2); S4 = p_B[Q4] / (p_A[Q4] + p_B[Q4]) "
           "(despues de la reversion, preferencia por lo que AHORA es bueno); S2 = p_A[Q2] / (p_A[Q2] + p_B[Q2]) (la misma, antes); "
           "C = S4 - S2 (cuanto se desdice, contra si mismo). PASA si (a) no inferioridad de una cola al 95 % (z 1.645) sobre "
           "d = C_cand - C_tronco, pareado nominal por semilla, con margen 0.125 (LI > -0.125), n = 80, Y (b) mediana de S4 del "
           "candidato > 0.5"),
    margen=0.125, z=1.645, n=80, suelo_S4=0.5, laplace=(1.0, 2.0), cuarto_antes=1, cuarto_despues=3,
    margen_regla="0.30 x (mediana de S4 del nulo 0.9136 - 0.5) = 0.1241 -> 0.125 (la equivalencia relativa de ERR-94: 12.5 ~ 30 % de rev)",
    nulo=dict(fuente='experimentos/tronco_v14_4c_examen/datos/nulo_err150_20260928_161728.json', sha='a394a03bf9241b40',
              P_pasa_nulo_min=1.0, P_pasa_delta_menos_m_max=0.0552, P_pasa_delta_menos_1_6m_max=0.0, sd_d_max=0.0391, techo_sd=0.3398,
              mediana_S4=0.9136, mediana_C=0.0035),
    anti_TERMO=dict(S2=0.8201, S4=0.3421, C_mediana=-0.4733, media_d=-0.4688, LI=-0.4819, P_pasa_bootstrap=0.0, tumba=True),
    rev_v4_solo_informe=U144B.LETRA['T-C_ii'],
)
LETRA = dict(U144B.LETRA)
LETRA['T-C_ii'] = ERR150['frase']
LETRA_TC_ii_REV_V4 = U144B.LETRA['T-C_ii']   # la vieja: se calcula y se REPORTA, no decide (ERR-150)

# ---------------------------------------------------------------- SEMILLAS NUEVAS (busca_semillas_v144c.py, 28-sep-2026; salida en
# busca_semillas_v144c_salida.txt). Rango 53000-53999 y 153000-153999. T-D recalculada con diagnostico_codigos (D&B >= 3 / == 0).
_r = lambda a, b: list(range(a, b + 1))
SEMILLAS = {
    'serie': dict(EX=_r(53101, 53120), VIVO=_r(53201, 53280), TD_rango=(53501, 53999),
                  ALIAS=[53567, 53569, 53574, 53580, 53591, 53597, 53609, 53675, 53682],
                  LIMPIAS=[53503, 53506, 53510, 53516, 53522, 53534, 53536, 53547, 53558]),
    'replica': dict(EX=_r(53121, 53140), VIVO=_r(53301, 53380), TD_rango=(153501, 153999),
                    ALIAS=[153526, 153562, 153594, 153611, 153617, 153649, 153669, 153673, 153682],
                    LIMPIAS=[153515, 153522, 153527, 153532, 153533, 153536, 153545, 153556, 153568]),
    'reserva': dict(VIVO=_r(53401, 53480)),
    'humo': [53951, 53952, 53953],
    'identidad': [53955, 53956, 53957],
}

ARNES_ESPERADO = 'RESULTADO: 144/144'

# PREREGISTRO_examen_v144c.md sec. 5; escritas ANTES del humo. A la vista: el EXPLORATORIO de TERMO' del examen v14.4b (49001-49002,
# SIN visitas: rev 22 y 2; muerde A en Q4 141 y 119) y los crudos de TERMO (v14.4: S2 0.820, pA2 0.386, pB2 0.083). La serie del
# examen v14.4b corria mientras se escribia esto: NO se miro.
PRED = {
    'legible': dict(p=0.97, frase="TRONCO_B pasa T-A, T-C (ii) por visita (P nulo 1.000) y T-F"),
    'T-A': dict(p=0.55, frase="igual que en v14.4b (mismo organismo, semillas nuevas)"),
    'T-B': dict(p=0.90, frase="igual que en v14.4b"),
    'T-C': dict(p=0.50, frase="(i) p 0.85; (ii) POR VISITA p 0.60: antes de la reversion TERMO' es TERMO (S2 ~ 0.82: rechaza lo bueno cuando "
                              "esta lleno, pA2 ~ 0.39); en Q4 la memoria de B ya es positiva y la de A negativa: por simetria S4 ~ S2 -> "
                              "C mediana en [-0.08, +0.03] (OFF ~ 0.00), S4 mediana en [0.70, 0.90]. Riesgo: A en Q4 muerde 141 y 119 en el "
                              "exploratorio (tronco ~160 con ~1700 visitas): si las visitas de A son pocas, pA4 sube y C cae"),
    'T-C_ii_rev_informe': dict(p=0.2, frase="la letra VIEJA (rev absoluto) sigue cayendo: rev mediana 0-30 (se reporta, no decide)"),
    'T-D': dict(p=0.85, frase="igual que en v14.4b"),
    'T-E': dict(p=0.60, frase="igual que en v14.4b (E2 muerde A Q4 <= 1.10 x tronco)"),
    'T-F': dict(p=0.75, frase="igual que en v14.4b"),
    'T-G': dict(p=0.25, frase="igual que en v14.4b (G-1 p 0.25)"),
    'serie': dict(p=0.05, frase="VEREDICTO previsto NO PASA (p ~ 0.95), sobre todo por T-G y T-E; T-C (ii) por visita pasa con p 0.6"),
}
