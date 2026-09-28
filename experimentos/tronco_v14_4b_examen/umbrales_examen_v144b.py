"""UMBRALES, SEMILLAS y PREDICCIONES del examen del CRITERIO DE TRONCO v4 sobre v14.4b = v14.3 + TERMO' (TERMO con memoria que
olvida) -- un solo modulo (ERR-31). LA LETRA, la T-G y los brazos se IMPORTAN de experimentos/tronco_v14_4_examen/umbrales_examen_v144.py
(que a su vez importa la del examen de v14.3): MISMA letra, SIN cambios. Aqui solo cambian las semillas (nuevas), el arnes esperado y
las predicciones. Ningun numero se toca despues de correr.
"""
import os, sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
_V144 = os.path.join(os.path.dirname(os.path.dirname(_AQUI)), 'experimentos', 'tronco_v14_4_examen')
if _V144 not in sys.path:
    sys.path.append(_V144)   # AL FINAL: no tapa nada
import umbrales_examen_v144 as U144   # sha fijado en corre_examen_v144b.ANCLAS

LETRA = dict(U144.LETRA); NUM = dict(U144.NUM); ERR122 = U144.ERR122; TG = dict(U144.TG)
ARMS_VIVO = list(U144.ARMS_VIVO); ARMS_TA = list(U144.ARMS_TA); BRAZOS_TA = list(U144.BRAZOS_TA); ARMS_SAL = list(U144.ARMS_SAL)
ORGS_EX = list(U144.ORGS_EX); SEIS = list(U144.SEIS); REGLAS_TB = list(U144.REGLAS_TB)
T_VIVO = U144.T_VIVO; T_HUMO = U144.T_HUMO; DESPL_TRONCO_B = U144.DESPL_TRONCO_B

# ---------------------------------------------------------------- SEMILLAS NUEVAS (busca_semillas_v144b.py, 28-sep-2026: 44 040 archivos;
# en 49000-49999 y 149000-149999 solo fragmentos de sha; 50000 si aparece como semilla (ECO): no se usa). Exploratorio de TERMO'
# (ya usado): 49001, 49002, 49011-49015, 49099. Carrera de TERMO': 49941-49994 (PREREGISTRO_termop.md).
_r = lambda a, b: list(range(a, b + 1))
SEMILLAS = {
    'serie': dict(EX=_r(49101, 49120), VIVO=_r(49201, 49280), TD_rango=(49501, 49999),
                  ALIAS=[49509, 49528, 49563, 49597, 49621, 49652, 49718, 49756, 49871],
                  LIMPIAS=[49502, 49516, 49518, 49519, 49521, 49526, 49543, 49564, 49566]),
    'replica': dict(EX=_r(49121, 49140), VIVO=_r(49301, 49380), TD_rango=(149501, 149999),
                    ALIAS=[149519, 149541, 149592, 149657, 149658, 149666, 149670, 149715, 149719],
                    LIMPIAS=[149504, 149507, 149514, 149522, 149532, 149536, 149547, 149550, 149556]),
    'reserva': dict(VIVO=_r(49401, 49480)),
    'humo': [49901, 49902, 49903],
    'identidad': [49905, 49906, 49907],
}

ARNES_ESPERADO = 'RESULTADO: 129/129'   # (0) 8 (A) 21 (A') 5 (P) 10 (L) 6 (X) 2 (D) 7 (R) 41 (J) 10 (K) 19

# PREREGISTRO_examen_v144b.md sec. 5; escritas ANTES del humo, con el EXPLORATORIO de TERMO' a la vista (declarado: 2 semillas,
# 49001-49002; E2 muerde A en Q4 5 y 7 contra 10 y 11 del tronco; T-C ii rev 22 y 2 contra 38 y 30; muertes 77 y 87 contra 102).
PRED = {
    'legible': dict(p=0.97, frase="las tareas calibradas de V4-CAL, como en v14.3 y v14.4"),
    'T-A': dict(p=0.55, frase="sin reversion TERMO' == TERMO salvo empates de coma flotante: lo mismo que TERMO (ver PREREGISTRO_examen_v144 sec. 5)"),
    'T-B': dict(p=0.90, frase="igual que TERMO: la conducta de primer encuentro no la toca la pieza"),
    'T-C': dict(p=0.15, frase="(i) come B Q4 >= 50 en >= 18/20 con p 0.85; (ii) rev CAND mediana 0-30 (OFF ~ 42): el termostato come MENOS B "
                              "(163 y 121 contra 198 y 197) y rev cuenta mordidas absolutas: LI > -12.5 con p 0.2"),
    'T-D': dict(p=0.85, frase="como TERMO: no gobierna B ni D"),
    'T-E': dict(p=0.60, frase="E2 'muerde A Q4 <= 1.10 x tronco' ahora pasa (la memoria de A cruza 0 en ~22 mordidas); riesgo: E1/E2L 'come A Q4 >= 0.8 x'"),
    'T-F': dict(p=0.75, frase="muertes de T-C ii por debajo del tronco (77, 87 contra 102); examen como TERMO"),
    'T-G': dict(p=0.25, frase="sin reversion es TERMO: G-1 p 0.25, G-2 p 0.95"),
    'serie': dict(p=0.02, frase="VEREDICTO previsto NO PASA (p ~ 0.95), sobre todo por T-C (ii) (comer menos, no la reversion) y T-G"),
}
