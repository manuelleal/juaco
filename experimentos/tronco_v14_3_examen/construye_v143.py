"""construye_v143.py -- CONSTRUCTOR POR ANCLAS del candidato v14.3 = v14.2 + REPARACION N (norm_lenta, subida_n7).

MISION: llegar a la AGI por este camino. v14.3 no es un organo nuevo: es devolverle al tronco la composicion que A-4
(v14.1) le quito sin que nadie lo midiera (subida_n7, FUNCIONA x2: el tronco v14.2 compone hasta K_max 1; con N, hasta 8).

No corre nada. Los origenes SOLO se leen; el sha de cada uno se verifica ANTES de escribir (si uno cambio, no se escribe
nada). Escribe en ESTA carpeta (experimentos/tronco_v14_3_examen/):

  organismo_v143.py          <- organismo/organismo_v142.py            (17528d767fcebaf6, CONGELADO)   [a CONGELADOS si pasa]
  organismo_v143g.py         <- organismo/organismo_v142g.py           (9e5f566cd6a7a4d2, CONGELADO)   [a CONGELADOS si pasa]
  bateria_v143.py            <- organismo/bateria_v142.py              (6375d90e531b06e6, CONGELADA)   [a CONGELADOS si pasa]
  bateria_generaliza_v143.py <- organismo/bateria_generaliza_v142.py   (e5929942647756a5, CONGELADA)   [a CONGELADOS si pasa]
  organismo_v143cal.py       <- experimentos/criterio_v3/organismo_v3cal.py (148014f68cb01785)          [instrumento del examen]

QUE CAMBIA (y nada mas):
  organismos: la firma gana `norm_lenta=1` y el paso de la VIA LENTA se multiplica por M0/(P.P), M0 = 3.0:
      _Pl = P*(3.0/float(P@P)) if norm_lenta else P
  Es el MISMO texto de experimentos/subida_n7/construye_n7.py (9f5851b9e8ec1ec5); el constructor comprueba que el cuerpo
  de organismo_v143(g) es EXACTAMENTE el de subida_n7/organismo_v142N(gN) (b5bcff0a4b01c812 / d05fc32504cb5517) con el
  defecto movido (0 -> 1). En organismo_v143cal hay DOS sitios (la necesidad activa y las otras): los dos se reparan.
  Memoria nueva: CERO. Constante nueva: M0 = 3.0 (la masa de UN estimulo en todos los mundos del tronco; no se ajusta).
  baterias: solo el modulo al que apuntan y los nombres de salida (examen) / UNA entrada nueva en INSTRUMENTOS campo a
  campo igual a la de organismo_v142 (generalizacion; regla 14). Umbrales, etapas y CRIT intactos.

Las cuatro primeras viven en organismo/ tras congelar (el coordinador las COPIA byte a byte y verifica el sha); aqui el
examen solo IMPORTA sus funciones `tarea` (su __main__ lee sha de organismo_v11/v10 y escribe en datos/ relativo a su
carpeta: necesita estar en organismo/, ERR-42).

Uso:
  python experimentos/tronco_v14_3_examen/construye_v143.py              (escribe; imprime los sha)
  python experimentos/tronco_v14_3_examen/construye_v143.py --verifica   (no escribe; sale 1 si algo en disco != construccion)
"""
import hashlib, os, re, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
V3 = os.path.join(RAIZ, 'experimentos', 'criterio_v3')
N7 = os.path.join(RAIZ, 'experimentos', 'subida_n7')

ORIGENES = {   # tripwire: si un origen cambio, no se escribe nada
    os.path.join(ORG, 'organismo_v142.py'): '17528d767fcebaf6',
    os.path.join(ORG, 'organismo_v142g.py'): '9e5f566cd6a7a4d2',
    os.path.join(ORG, 'bateria_v142.py'): '6375d90e531b06e6',
    os.path.join(ORG, 'bateria_generaliza_v142.py'): 'e5929942647756a5',
    os.path.join(V3, 'organismo_v3cal.py'): '148014f68cb01785',
    os.path.join(N7, 'organismo_v142N.py'): 'b5bcff0a4b01c812',
    os.path.join(N7, 'organismo_v142gN.py'): 'd05fc32504cb5517',
    os.path.join(N7, 'construye_n7.py'): '9f5851b9e8ec1ec5',
}
M0 = 3.0   # la unica constante nueva (se escribe literal como en subida_n7: "3.0")


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def h16t(t):
    return hashlib.sha256(t.encode('utf-8')).hexdigest()[:16]


def origen(ruta):
    s = h16(ruta)
    if s != ORIGENES[ruta]:
        raise SystemExit(f'*** ORIGEN {os.path.relpath(ruta, RAIZ)}: sha {s}, se esperaba {ORIGENES[ruta]}. No se escribe nada.')
    return open(ruta, 'rb').read().decode('utf-8')


def sust(t, a, b, n=1, etq=''):
    c = t.count(a)
    if c != n:
        raise SystemExit(f'*** ancla {etq!r} aparece {c} veces, se esperaban {n}. No se escribe nada.')
    return t.replace(a, b)


# ---------------------------------------------------------------- las anclas de subida_n7 (texto LITERAL de construye_n7.py)
def anclas_n7(pvar):
    viejo = (f"                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*{pvar},0,clip_s)\n"
             f"                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*{pvar},0,clip_s)\n")
    nuevo = (f"                        _Pl={pvar}*(3.0/float({pvar}@{pvar})) if norm_lenta else {pvar}   # n7: norm_lenta\n"
             f"                        if _ds>0: Wps=np.clip(Wps+eta_s*_ds*_Pl,0,clip_s)\n"
             f"                        else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*_Pl,0,clip_s)\n")
    return viejo, nuevo


def verifica_texto_n7():
    """Las anclas de arriba tienen que estar LITERALES en construye_n7.py (reuso, no reescritura)."""
    t = origen(os.path.join(N7, 'construye_n7.py'))
    for frag in ('_Pl={pvar}*(3.0/float({pvar}@{pvar})) if norm_lenta else {pvar}   # n7: norm_lenta',
                 'if _ds>0: Wps=np.clip(Wps+eta_s*_ds*_Pl,0,clip_s)',
                 'else:     Wns=np.clip(Wns+eta_s*aversion*(-_ds)*_Pl,0,clip_s)',
                 'u = sust(u, "desambiguar=1):", "desambiguar=1,norm_lenta=0):")'):
        sust(t, frag, frag, etq=f'construye_n7: {frag[:40]}')


def cuerpo_sin_cabecera(t, lineas):
    return t.split('\n', lineas)[lineas]


CAB_143 = '''"""organismo_v143 = v14.3 = TRONCO v14.2 + REPARACION N (norm_lenta, nivel 7). Candidato del 23-sep-2026; entra al
tronco SOLO si pasa el examen del CRITERIO DE TRONCO v4 en serie y replica (experimentos/tronco_v14_3_examen/, REGISTRO).
v14.2 = organismo/organismo_v142.py (17528d767fcebaf6, CONGELADO: solo se leyo).
N (experimentos/subida_n7, FUNCIONA x2, serie 7701-7720 y replica 7721-7740): el paso de la VIA LENTA se multiplica por
M0/(P.P), M0 = 3.0 = la masa de UN estimulo en todos los mundos del tronco. Memoria nueva: CERO. Constante nueva: M0 = 3.0
(fijada por el tronco, no se ajusta). El rng no se toca.
LO UNICO QUE CAMBIA respecto de v14.2: tres lineas de la via lenta y el defecto `norm_lenta=1`. Con norm_lenta=0 es
organismo_v142 EXACTO bit a bit. En los mundos del tronco P.P = 3 y el factor es 1.0 exacto: INERTE POR CONSTRUCCION.
Donde SI actua (P.P != 3; p. ej. 3T-k, masa 3(k+1)): devuelve la composicion que A-4 (v14.1) habia quitado; en 3T-k el
tronco v14.2 compone hasta K_max 1 y con N hasta K_max 8 (dos series).
Generado POR ANCLAS desde organismo/organismo_v142.py por experimentos/tronco_v14_3_examen/construye_v143.py, con el
texto de subida_n7/construye_n7.py (cuerpo == subida_n7/organismo_v142N.py con el defecto movido). NO editar a mano.
Arnes: experimentos/tronco_v14_3_examen/identidad_v143ex.py."""
'''

CAB_143G = '''"""organismo_v143g = instrumento de MUNDO DE REGLA de v14.3 (lo usa bateria_generaliza_v143.py) = organismo/organismo_v142g.py
(9e5f566cd6a7a4d2, CONGELADO: solo se leyo) + REPARACION N (norm_lenta=1 por defecto, M0 = 3.0; los 20 patrones del
mundo de regla tienen masa 3: inerte por construccion). Con norm_lenta=0 es organismo_v142g EXACTO.
AVISO (regla 14): sus defectos de via lenta siguen siendo eta_s=0.0, clip_s=3.0, puerta=None, mask_rel=0, puerta_pat=0;
la entrada de INSTRUMENTOS los pasa EXPLICITOS, campo a campo como la de organismo_v142.
Generado POR ANCLAS por experimentos/tronco_v14_3_examen/construye_v143.py (cuerpo == subida_n7/organismo_v142gN.py con el
defecto movido). NO editar a mano."""
'''

CAB_143CAL = '''"""organismo_v143cal = v14.3 en el MUNDO VIVO del criterio v4 (instrumento del examen, no se congela con el tronco):
experimentos/criterio_v3/organismo_v3cal.py (148014f68cb01785; el tronco v14.2 en el mundo vivo, instrumento calibrado de
V4-CAL; solo se leyo) + REPARACION N (norm_lenta=1 por defecto) en los DOS sitios de la via lenta: la fila de la necesidad
activa y las filas de las otras necesidades (el mismo bocado ensena a todas). M0 = 3.0; memoria nueva CERO.
En el mundo vivo los cuatro estimulos (PAT A-D) tienen masa 3: INERTE POR CONSTRUCCION (factor 1.0 exacto).
Con norm_lenta=0 es organismo_v3cal EXACTO bit a bit. Generado POR ANCLAS por
experimentos/tronco_v14_3_examen/construye_v143.py. NO editar a mano. Arnes: identidad_v143ex.py."""
'''

CAB_BAT = '''"""bateria_v143 = organismo/bateria_v142.py (6375d90e531b06e6, CONGELADA: solo se leyo) apuntando a **organismo_v143**
(v14.3 = v14.2 + N, norm_lenta=1 por defecto). Las SEIS etapas, los CRIT y los umbrales del criterio v3' quedan
INTACTOS; solo cambian el modulo examinado y los nombres de salida (datos/examen_v143_<fecha>.log/.json).
Vive en organismo/ tras congelar (AQUI == organismo/; ERR-42). Mientras tanto, corre_examen_v143.py solo IMPORTA `tarea`.
    python bateria_v143.py 6                      (regla 1, desde organismo/, tras congelar)
Generado POR ANCLAS por experimentos/tronco_v14_3_examen/construye_v143.py. NO editar a mano."""
'''

CAB_GEN = '''"""bateria_generaliza_v143 = organismo/bateria_generaliza_v142.py (e5929942647756a5, CONGELADA: solo se leyo) con UNA
entrada nueva en INSTRUMENTOS: organismo_v143 -> organismo_v143g, con los kwargs CAMPO A CAMPO iguales a los de la entrada
del tronco organismo_v142 (regla 14; eta_s=0.15 y clip_s=10.0 EXPLICITOS). La entrada de organismo_v142 sigue intacta.
Umbrales G1/G2/K sin tocar. Vive en organismo/ tras congelar (ERR-42); mientras tanto corre_examen_v143.py solo IMPORTA
`tarea`.
    python bateria_generaliza_v143.py organismo_v143 20 --desde 101 --log      (regla 1, desde organismo/, tras congelar)
Generada POR ANCLAS por experimentos/tronco_v14_3_examen/construye_v143.py. NO editar a mano."""
'''

KW_TRONCO_GEN = ("eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, "
                 "puerta_pat=5, pat_shuf=0, pat_min=1")


def construye():
    """Devuelve {nombre: texto}. No escribe."""
    verifica_texto_n7()
    out = {}
    # ---- 1) organismo_v143 <- organismo_v142 (+ las anclas de subida_n7, defecto 1)
    src = origen(os.path.join(ORG, 'organismo_v142.py'))
    u = sust(src, "desambiguar=1):", "desambiguar=1,norm_lenta=1):", etq='v143: firma')
    viejo, nuevo = anclas_n7('PAT[kk]')
    u = sust(u, viejo, nuevo, etq='v143: via lenta')
    n7 = cuerpo_sin_cabecera(origen(os.path.join(N7, 'organismo_v142N.py')), 4)
    if u != sust(n7, "desambiguar=1,norm_lenta=0):", "desambiguar=1,norm_lenta=1):", etq='v142N: firma'):
        raise SystemExit('*** el cuerpo de organismo_v143 NO es el de subida_n7/organismo_v142N con el defecto movido. No se escribe nada.')
    out['organismo_v143.py'] = CAB_143 + u
    # ---- 2) organismo_v143g <- organismo_v142g
    srcg = origen(os.path.join(ORG, 'organismo_v142g.py'))
    g = sust(srcg, "desambiguar=1):", "desambiguar=1,norm_lenta=1):", etq='v143g: firma')
    viejo, nuevo = anclas_n7('P_[kk]')
    g = sust(g, viejo, nuevo, etq='v143g: via lenta')
    n7g = cuerpo_sin_cabecera(origen(os.path.join(N7, 'organismo_v142gN.py')), 4)
    if g != sust(n7g, "desambiguar=1,norm_lenta=0):", "desambiguar=1,norm_lenta=1):", etq='v142gN: firma'):
        raise SystemExit('*** el cuerpo de organismo_v143g NO es el de subida_n7/organismo_v142gN con el defecto movido. No se escribe nada.')
    out['organismo_v143g.py'] = CAB_143G + g
    # ---- 3) organismo_v143cal <- organismo_v3cal (DOS sitios de la via lenta)
    c = origen(os.path.join(V3, 'organismo_v3cal.py'))
    c = sust(c, "desambiguar=1,invertir_vivo_en=None,placebo=0):", "desambiguar=1,invertir_vivo_en=None,placebo=0,norm_lenta=1):",
             etq='v143cal: firma')
    c = sust(c, "                        if _ds>0: Wps[_nm]=np.clip(Wps[_nm]+eta_s*_ds*PAT[kk],0,clip_s)\n"
                "                        else:     Wns[_nm]=np.clip(Wns[_nm]+eta_s*aversion*(-_ds)*PAT[kk],0,clip_s)\n",
                "                        _Pl=PAT[kk]*(3.0/float(PAT[kk]@PAT[kk])) if norm_lenta else PAT[kk]   # v14.3: norm_lenta (N), necesidad activa\n"
                "                        if _ds>0: Wps[_nm]=np.clip(Wps[_nm]+eta_s*_ds*_Pl,0,clip_s)\n"
                "                        else:     Wns[_nm]=np.clip(Wns[_nm]+eta_s*aversion*(-_ds)*_Pl,0,clip_s)\n",
             etq='v143cal: via lenta, necesidad activa')
    c = sust(c, "                                if _dsn>0: Wps[_n]=np.clip(Wps[_n]+eta_s*_dsn*PAT[kk],0,clip_s)\n"
                "                                else:      Wns[_n]=np.clip(Wns[_n]+eta_s*aversion*(-_dsn)*PAT[kk],0,clip_s)\n",
                "                                _Pl=PAT[kk]*(3.0/float(PAT[kk]@PAT[kk])) if norm_lenta else PAT[kk]   # v14.3: norm_lenta (N), otras necesidades\n"
                "                                if _dsn>0: Wps[_n]=np.clip(Wps[_n]+eta_s*_dsn*_Pl,0,clip_s)\n"
                "                                else:      Wns[_n]=np.clip(Wns[_n]+eta_s*aversion*(-_dsn)*_Pl,0,clip_s)\n",
             etq='v143cal: via lenta, otras necesidades')
    out['organismo_v143cal.py'] = CAB_143CAL + c
    # ---- 4) bateria_v143 <- bateria_v142 (modulo examinado y nombres de salida)
    b = origen(os.path.join(ORG, 'bateria_v142.py'))
    b = sust(b, 'import organismo_v142 as v13   # TRONCO v14.2 = v14.1 + B-5 (desambiguar=1 por defecto)',
             'import organismo_v143 as v13   # v14.3 = v14.2 + N (norm_lenta=1 por defecto)', n=2, etq='bat: import')
    b = sust(b, "h16(os.path.join(_D14, 'organismo_v142.py'))", "h16(os.path.join(_D14, 'organismo_v143.py'))", n=2, etq='bat: sha')
    b = sust(b, "f'examen_v142_{stamp}.log'", "f'examen_v143_{stamp}.log'", etq='bat: log')
    b = sust(b, "f'examen_v142_{stamp}.json'", "f'examen_v143_{stamp}.json'", etq='bat: json')
    out['bateria_v143.py'] = CAB_BAT + b
    # ---- 5) bateria_generaliza_v143 <- bateria_generaliza_v142 (UNA entrada nueva, campo a campo)
    gg = origen(os.path.join(ORG, 'bateria_generaliza_v142.py'))
    m = re.search(r"^ *'organismo_v142': \(.*$", gg, re.M)
    if not m:
        raise SystemExit('*** no encuentro la entrada organismo_v142 en INSTRUMENTOS. No se escribe nada.')
    A = m.group(0)
    kw142 = re.search(r"dict\((.*?)\)\),", A).group(1)
    if kw142.strip() != KW_TRONCO_GEN:   # REGLA 14: la entrada nueva es CAMPO A CAMPO la del tronco
        raise SystemExit(f'*** los kwargs de organismo_v142 cambiaron: {kw142!r}. No se escribe nada.')
    NUEVA = ("    'organismo_v143': ('organismo_v143g', dict(" + KW_TRONCO_GEN + ")),"
             "   # v14.3 = v14.2 + N (norm_lenta=1 por defecto en organismo_v143g): kwargs CAMPO A CAMPO iguales a los de organismo_v142 (regla 14)")
    gg = sust(gg, A, A + "\n" + NUEVA, etq='gen: INSTRUMENTOS')
    gg = sust(gg, "_dir = {'organismo_v14g': AQUI, 'organismo_v142g': AQUI,",
              "_dir = {'organismo_v14g': AQUI, 'organismo_v142g': AQUI, 'organismo_v143g': AQUI,", etq='gen: _dir')
    out['bateria_generaliza_v143.py'] = CAB_GEN + gg
    return out


if __name__ == '__main__':
    VERIFICA = '--verifica' in sys.argv
    extra = [a for a in sys.argv[1:] if a != '--verifica']
    if extra:
        raise SystemExit(f'*** banderas desconocidas: {extra} (ERR-115). Uso: construye_v143.py [--verifica]')
    T = construye()
    malo = 0
    for n, t in T.items():
        p = os.path.join(AQUI, n)
        if VERIFICA:
            en_disco = open(p, 'rb').read().decode('utf-8') if os.path.exists(p) else None
            ok = en_disco == t
            malo += not ok
            print(f"{'OK  ' if ok else 'DIFIERE'} {n:28s} construccion {h16t(t)}  disco {h16(p) if os.path.exists(p) else '(falta)'}")
        else:
            with open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write(t)
            print(f'escrito {n:28s} {h16(p)}')
    print('origenes: ' + '  '.join(f'{os.path.basename(k)} {v}' for k, v in ORIGENES.items()))
    if VERIFICA:
        print(f"VERIFICA: {'todo en disco == construccion' if not malo else f'*** {malo} archivo(s) distintos'}")
        sys.exit(1 if malo else 0)
