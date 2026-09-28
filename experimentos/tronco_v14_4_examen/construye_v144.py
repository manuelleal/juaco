"""construye_v144.py -- CONSTRUCTOR POR ANCLAS del candidato v14.4 = v14.3 (TRONCO) + TERMO (termostato de boca).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). TERMO fue HAY ALGO MODESTO x2 en la pista de la carrera (REGISTRO 28-sep, experimentos/organelos/termo/)
sobre el CARRO V143 (FABRICA + B-5 + FILTRO + APR). Aqui se traslada la PIEZA, y solo la pieza, al ORGANISMO del tronco v14.3.

No corre nada. Los origenes SOLO se leen; el sha de cada uno se verifica ANTES de escribir (si uno cambio, no se escribe nada).

LA PIEZA (letra de V143_TERMO._tm_boca, carrera; aqui una funcion de modulo SIN estado, `termo_letra`, identica en los tres
organismos):
    sobre un estimulo k que el organismo ya mordio, con s = media del dS SENTIDO al morderlo (sin componentes negativas y con
    alguna positiva), la decision de morder la toma la pieza:   muerde <=> existe j con s_j > 0 y nivel_j < U + s_j / 2
    (U = rep_umbral; nivel = E, Ag). Lo desconocido y lo sentido malo (o nulo): la boca de v14.3 tal cual. Sin rng: el sorteo
    de la boca se consume igual; la pieza solo decide despues.
    CONTROL TERMOINV (termo = 2, solo con dos necesidades): la misma regla leyendo el nivel de la necesidad que la letra NO sube.
QUE NO TRASLADA SIN DECLARAR (PREREGISTRO_examen_v144.md sec. 2 y 7; candidatos a ERR):
  (a) MEMORIA NUEVA. En el carro, s sale de `_adS` de APR (ya estaba). El tronco v14.3 NO tiene APR: aqui `_adS` es memoria
      NUEVA del organismo: por estimulo mordido, la suma del dS nominal por necesidad y el numero de mordidas (2 o 3 numeros por
      estimulo). Se acumula igual que APR._apr_dS (suma sin olvido).
  (b) LA CONSIGNA U. En el carro U = ctx['rep_umbral'] = 1.0. En el mundo vivo U = el kwarg rep_umbral (defecto 1.0; el mismo
      valor en T-A, T-C (ii) y T-D). En los mundos de UNA necesidad (examen v3', mundo de regla) no hay parto: se agrega el
      kwarg `rep_umbral=1.0` (constante fijada por la pista y el mundo vivo, no se ajusta) y j recorre la unica necesidad.
  (c) TERMOINV no existe con una necesidad (no hay "la otra"): termo = 2 aborta alli.

Escribe en ESTA carpeta (experimentos/tronco_v14_4_examen/):
  organismo_v144.py          <- organismo/organismo_v143.py            (2cebc0ab0c38b70f, CONGELADO)   [a CONGELADOS si pasa]
  organismo_v144g.py         <- organismo/organismo_v143g.py           (c20fccaa9107fb89, CONGELADO)   [a CONGELADOS si pasa]
  bateria_v144.py            <- organismo/bateria_v143.py              (9daa88a90a2fd7b1, CONGELADA)   [a CONGELADOS si pasa]
  bateria_generaliza_v144.py <- organismo/bateria_generaliza_v143.py   (a894101fd1e6db93, CONGELADA)   [a CONGELADOS si pasa]
  organismo_v144cal.py       <- experimentos/tronco_v14_3_examen/organismo_v143cal.py (1169f54ef0a19de1)  [instrumento]
Con termo = 0 cada organismo es su origen v14.3 BIT A BIT (arnes identidad_v144ex.py, bloque A).
Baterias: el modulo examinado, los nombres de salida y, en la identidad interna de bateria_v144 contra v11/v10 (tarea_id),
`termo=0` junto a las otras perillas que ya se apagan alli (sin eso la identidad de la regla 1 compararia TERMO encendido
contra v11). Umbrales, etapas y CRIT intactos. bateria_generaliza_v144: UNA entrada nueva campo a campo (regla 14).

    python experimentos/tronco_v14_4_examen/construye_v144.py              (escribe; imprime los sha)
    python experimentos/tronco_v14_4_examen/construye_v144.py --verifica   (no escribe; sale 1 si algo en disco != construccion)
"""
import hashlib, os, re, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
V143EX = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3_examen')
TERMO = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')

ORIGENES = {   # tripwire: si un origen cambio, no se escribe nada
    os.path.join(ORG, 'organismo_v143.py'): '2cebc0ab0c38b70f',
    os.path.join(ORG, 'organismo_v143g.py'): 'c20fccaa9107fb89',
    os.path.join(ORG, 'bateria_v143.py'): '9daa88a90a2fd7b1',
    os.path.join(ORG, 'bateria_generaliza_v143.py'): 'a894101fd1e6db93',
    os.path.join(V143EX, 'organismo_v143cal.py'): '1169f54ef0a19de1',
    os.path.join(TERMO, 'carros', 'V143_TERMO.py'): '3db639cab75641fb',      # la LETRA de la pieza (solo se lee)
    os.path.join(TERMO, 'construye_termo.py'): '23f57933c51c64e8',
}
# fragmentos LITERALES de la letra en el carro de la carrera (se exige que esten; la funcion de abajo los traduce sin estado)
LETRA_CARRO = (
    "if m is None or m[2] <= 0: return mf",
    "s = (m[0] / m[2], m[1] / m[2])",
    "if s[0] < 0 or s[1] < 0 or not (s[0] > 0 or s[1] > 0): return mf",
    "lev = (float(E), float(Ag))",
    "if TERMO == 1: b = any(s[j] > 0 and lev[j] < self._tmU + s[j] / 2 for j in (0, 1))",
    "else:          b = any(s[j] > 0 and lev[1 - j] < self._tmU + s[j] / 2 for j in (0, 1))",
    "g = self._tm; g['dec'] += 1; g['a_no'] += int(mf and not b); g['a_si'] += int(b and not mf); g['mord'] += int(b)",
    "m[0] += float(dS[0]); m[1] += float(dS[1]); m[2] += 1",
    "if TERMO: mordio = self._tm_boca(kk, E, Ag, mordio)",
)


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


def verifica_letra_carro():
    t = origen(os.path.join(TERMO, 'carros', 'V143_TERMO.py')).replace('\r\n', '\n')
    for frag in LETRA_CARRO:
        sust(t, frag, frag, etq=f'V143_TERMO: {frag[:50]}')


# ---------------------------------------------------------------- LA PIEZA: el MISMO texto en los tres organismos
FUNCION = '''

def termo_letra(m, lev, U, mf, modo):   # v14.4 TERMO: LA LETRA de V143_TERMO._tm_boca (carrera; experimentos/organelos/termo), SIN estado
    """m = [suma dS_0, ..., suma dS_(n-1), mordidas] SENTIDO por el organismo al morder el estimulo (None si nunca lo mordio);
    lev = niveles presentes, (E,) o (E, Ag); U = consigna (rep_umbral); mf = la decision YA sorteada de la boca de v14.3;
    modo 1 = TERMO; 2 = TERMOINV (control: lee lev[1 - j], la necesidad que el estimulo NO sube). Devuelve (muerde, gobernada)."""
    if m is None or m[-1] <= 0: return mf, False                                   # desconocido: v14.3
    s = tuple(m[_j] / m[-1] for _j in range(len(m) - 1))
    if any(_x < 0 for _x in s) or not any(_x > 0 for _x in s): return mf, False    # sentido malo (o nulo): v14.3
    if modo == 1: return any(s[_j] > 0 and lev[_j] < U + s[_j] / 2 for _j in range(len(s))), True
    return any(s[_j] > 0 and lev[1 - _j] < U + s[_j] / 2 for _j in range(len(s))), True
'''
ANCLA_FUNCION = "R_VAL={'comida':1.0,'veneno':-3.0}; E_VAL={'comida':+0.8,'veneno':-0.4}\n"
ESTADO = ("    _adS={}; _tm=dict(dec=0,a_no=0,a_si=0,mord=0)   # v14.4 TERMO: MEMORIA NUEVA (lo SENTIDO por estimulo mordido: sumas de dS "
          "nominal por necesidad y mordidas; como APR._apr_dS, sin olvido) y contadores de SOLO LECTURA\n"
          "    def _tm_boca(_k,_lev,_mf):   # v14.4 TERMO: decide sobre lo sentido bueno (despues del sorteo de la boca, que no cambia)\n"
          "        _b,_g=termo_letra(_adS.get(_k),_lev,rep_umbral,_mf,termo)\n"
          "        if _g: _tm['dec']+=1; _tm['a_no']+=int(_mf and not _b); _tm['a_si']+=int(_b and not _mf); _tm['mord']+=int(_b)\n"
          "        return _b\n"
          "    ncod={}; _ord=[]")
SALIDA_TM = ("**({'termo':dict(termo=termo,U=rep_umbral,dec=_tm['dec'],a_no=_tm['a_no'],a_si=_tm['a_si'],mord=_tm['mord'],"
             "adS={_k:list(_v) for _k,_v in sorted(_adS.items())})} if termo else {})")


def pieza_una_necesidad(u, etq, pvar):
    """organismo_v143 / organismo_v143g (UNA necesidad: E). Seis anclas, cada una exacta una vez."""
    u = sust(u, "desambiguar=1,norm_lenta=1):", "desambiguar=1,norm_lenta=1,termo=1,rep_umbral=1.0):", etq=f'{etq}: firma')
    u = sust(u, ANCLA_FUNCION, ANCLA_FUNCION + FUNCION, etq=f'{etq}: funcion de modulo')
    u = sust(u, "    rng=np.random.default_rng(seed)\n",
             "    if termo not in (0,1,2): raise SystemExit(f'TERMO: termo es 0, 1 o 2, no {termo!r}')\n"
             "    if termo==2: raise SystemExit('TERMO: TERMOINV (termo=2) lee la necesidad que el estimulo NO sube; con UNA necesidad no existe')\n"
             "    rng=np.random.default_rng(seed)\n", etq=f'{etq}: guardas')
    u = sust(u, "    ncod={}; _ord=[]", ESTADO, etq=f'{etq}: estado')
    u = sust(u, "Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb\n",
             "Vb=alpha*_wt+hambre_boca*hambre+.5; pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb\n"
             "            if termo: mordio=_tm_boca(kk,(float(E),),mordio)   # v14.4 TERMO: manda sobre lo sentido bueno (una necesidad)\n",
             etq=f'{etq}: boca')
    u = sust(u, "R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n",
             "R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5); mord[kk][q(t)]+=1\n"
             "                if termo: _m9=_adS.setdefault(kk,[0.0,0]); _m9[0]+=float(E_VAL[val[kk]]); _m9[1]+=1   # v14.4 TERMO: lo SENTIDO (dS nominal)\n",
             etq=f'{etq}: lo sentido')
    return u


CAB_144 = '''"""organismo_v144 = v14.4 (CANDIDATO) = TRONCO v14.3 + TERMO (termostato de boca). Entra al tronco SOLO si pasa el examen del
CRITERIO DE TRONCO v4 en serie y replica (experimentos/tronco_v14_4_examen/PREREGISTRO_examen_v144.md).
v14.3 = organismo/organismo_v143.py (2cebc0ab0c38b70f, CONGELADO: solo se leyo).
TERMO (experimentos/organelos/termo, HAY ALGO MODESTO x2 en la carrera, sobre el carro V143): sobre un estimulo ya mordido cuya
media de dS SENTIDO no tiene componentes negativas y tiene alguna positiva, muerde <=> existe j con s_j > 0 y nivel_j < U + s_j/2.
Aqui UNA necesidad (E): j = 0, U = rep_umbral = 1.0 (kwarg nuevo; constante de la pista y del mundo vivo; aqui no hay parto).
MEMORIA NUEVA: `_adS` (por estimulo mordido: suma del dS nominal y mordidas; sin olvido). Constantes nuevas: U = 1.0 y el 1/2
de la pieza (del exploratorio de la carrera, declarado alli). El rng no se toca.
Con termo=0 es organismo_v143 EXACTO bit a bit (identidad_v144ex.py). termo=2 (TERMOINV) no existe con una necesidad.
Generado POR ANCLAS desde organismo/organismo_v143.py por experimentos/tronco_v14_4_examen/construye_v144.py. NO editar a mano."""
'''

CAB_144G = '''"""organismo_v144g = instrumento de MUNDO DE REGLA de v14.4 (lo usa bateria_generaliza_v144.py) = organismo/organismo_v143g.py
(c20fccaa9107fb89, CONGELADO: solo se leyo) + TERMO (termo=1 por defecto; una necesidad; U = rep_umbral = 1.0).
AVISO (regla 14): sus defectos de via lenta siguen siendo los del instrumento (eta_s=0.0, clip_s=3.0, puerta=None, ...); la entrada
de INSTRUMENTOS los pasa EXPLICITOS, campo a campo como la de organismo_v143. Con termo=0 es organismo_v143g EXACTO.
Generado POR ANCLAS por experimentos/tronco_v14_4_examen/construye_v144.py. NO editar a mano."""
'''

CAB_144CAL = '''"""organismo_v144cal = v14.4 en el MUNDO VIVO del criterio v4 (instrumento del examen, no se congela con el tronco):
experimentos/tronco_v14_3_examen/organismo_v143cal.py (1169f54ef0a19de1; v14.3 en el mundo vivo; solo se leyo) + TERMO con DOS
necesidades (E, Ag), exactamente la letra de V143_TERMO de la carrera; U = el kwarg rep_umbral (defecto 1.0, el de T-A).
termo=1 por defecto (CANDIDATO); termo=2 = TERMOINV (CONTROL de T-G; exige vivo=1). MEMORIA NUEVA `_adS` (sumas de dS nominal
por necesidad y mordidas, como APR._apr_dS). Con termo=0 es organismo_v143cal EXACTO bit a bit. Generado POR ANCLAS por
experimentos/tronco_v14_4_examen/construye_v144.py. NO editar a mano. Arnes: identidad_v144ex.py."""
'''

CAB_BAT = '''"""bateria_v144 = organismo/bateria_v143.py (9daa88a90a2fd7b1, CONGELADA: solo se leyo) apuntando a **organismo_v144**
(v14.4 = v14.3 + TERMO, termo=1 por defecto). Las SEIS etapas, los CRIT y los umbrales del criterio v3' quedan INTACTOS; cambian
el modulo examinado, los nombres de salida (datos/examen_v144_<fecha>.log/.json) y, en la identidad interna contra v11/v10
(tarea_id), `termo=0` junto a las perillas que ya se apagaban alli.
Vive en organismo/ tras congelar (AQUI == organismo/; ERR-42). Mientras tanto, corre_examen_v144.py solo IMPORTA `tarea`.
    python bateria_v144.py 6                      (regla 1, desde organismo/, tras congelar)
Generado POR ANCLAS por experimentos/tronco_v14_4_examen/construye_v144.py. NO editar a mano."""
'''

CAB_GEN = '''"""bateria_generaliza_v144 = organismo/bateria_generaliza_v143.py (a894101fd1e6db93, CONGELADA: solo se leyo) con UNA
entrada nueva en INSTRUMENTOS: organismo_v144 -> organismo_v144g, con los kwargs CAMPO A CAMPO iguales a los de la entrada del
tronco organismo_v143 (regla 14; TERMO por el defecto termo=1 de organismo_v144g, como N por norm_lenta=1 en v14.3). Las
entradas anteriores siguen intactas. Umbrales G1/G2/K sin tocar. Vive en organismo/ tras congelar (ERR-42).
    python bateria_generaliza_v144.py organismo_v144 20 --desde 101 --log      (regla 1, desde organismo/, tras congelar)
Generada POR ANCLAS por experimentos/tronco_v14_4_examen/construye_v144.py. NO editar a mano."""
'''

KW_TRONCO_GEN = ("eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, "
                 "puerta_pat=5, pat_shuf=0, pat_min=1")


def construye():
    """Devuelve {nombre: texto}. No escribe."""
    verifica_letra_carro()
    out = {}
    # ---- 1) organismo_v144 <- organismo_v143
    u = origen(os.path.join(ORG, 'organismo_v143.py'))
    u = pieza_una_necesidad(u, 'v144', 'PAT')
    u = sust(u, "Wns=[round(float(x),3) for x in Wns])", "Wns=[round(float(x),3) for x in Wns]," + SALIDA_TM + ")", etq='v144: salida')
    out['organismo_v144.py'] = CAB_144 + u
    # ---- 2) organismo_v144g <- organismo_v143g
    g = origen(os.path.join(ORG, 'organismo_v143g.py'))
    g = pieza_una_necesidad(g, 'v144g', 'P_')
    g = sust(g, "sonda=_sonda,codigos_fin=_cod_fin)", "sonda=_sonda,codigos_fin=_cod_fin," + SALIDA_TM + ")", etq='v144g: salida')
    out['organismo_v144g.py'] = CAB_144G + g
    # ---- 3) organismo_v144cal <- organismo_v143cal (DOS necesidades: la letra del carro tal cual)
    c = origen(os.path.join(V143EX, 'organismo_v143cal.py'))
    c = sust(c, "placebo=0,norm_lenta=1):", "placebo=0,norm_lenta=1,termo=1):", etq='v144cal: firma')
    c = sust(c, ANCLA_FUNCION, ANCLA_FUNCION + FUNCION, etq='v144cal: funcion de modulo')
    c = sust(c, "    rng=np.random.default_rng(seed)\n",
             "    if termo not in (0,1,2): raise SystemExit(f'TERMO: termo es 0, 1 o 2, no {termo!r}')\n"
             "    if termo==2 and not vivo: raise SystemExit('TERMO: TERMOINV (termo=2) lee la necesidad que el estimulo NO sube; exige vivo=1')\n"
             "    rng=np.random.default_rng(seed)\n", etq='v144cal: guardas')
    c = sust(c, "    ncod={}; _ord=[]", ESTADO, etq='v144cal: estado')
    c = sust(c, "            pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb\n",
             "            pb=1/(1+np.exp(-Vb/.3)); mordio=rng.random()<pb\n"
             "            if termo: mordio=_tm_boca(kk,(float(E),float(Ag)),mordio)   # v14.4 TERMO: manda sobre lo sentido bueno (dos necesidades)\n",
             etq='v144cal: boca')
    c = sust(c, "                else: _dS=(E_VAL[val[kk]],0.0); _Rv=[R_VAL[val[kk]]]; R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5)\n",
             "                else: _dS=(E_VAL[val[kk]],0.0); _Rv=[R_VAL[val[kk]]]; R=R_VAL[val[kk]]; E=min(E+E_VAL[val[kk]],1.5)\n"
             "                if termo: _m9=_adS.setdefault(kk,[0.0,0.0,0]); _m9[0]+=float(_dS[0]); _m9[1]+=float(_dS[1]); _m9[2]+=1   # v14.4 TERMO: lo SENTIDO (dS nominal)\n",
             etq='v144cal: lo sentido')
    c = sust(c, "Wns=[round(float(x),3) for x in Wns[_nm]],**_ext)", "Wns=[round(float(x),3) for x in Wns[_nm]]," + SALIDA_TM + ",**_ext)",
             etq='v144cal: salida')
    out['organismo_v144cal.py'] = CAB_144CAL + c
    # ---- 4) bateria_v144 <- bateria_v143
    b = origen(os.path.join(ORG, 'bateria_v143.py'))
    b = sust(b, 'import organismo_v143 as v13   # v14.3 = v14.2 + N (norm_lenta=1 por defecto)',
             'import organismo_v144 as v13   # v14.4 = v14.3 + TERMO (termo=1 por defecto)', n=2, etq='bat: import')
    b = sust(b, "h16(os.path.join(_D14, 'organismo_v143.py'))", "h16(os.path.join(_D14, 'organismo_v144.py'))", n=2, etq='bat: sha')
    b = sust(b, "f'examen_v143_{stamp}.log'", "f'examen_v144_{stamp}.log'", etq='bat: log')
    b = sust(b, "f'examen_v143_{stamp}.json'", "f'examen_v144_{stamp}.json'", etq='bat: json')
    b = sust(b, "v13.run(seed, eta_s=0.0, puerta=None, **ESC_ID[esc])", "v13.run(seed, eta_s=0.0, puerta=None, termo=0, **ESC_ID[esc])",
             etq='bat: identidad v11')
    b = sust(b, "v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, **ESC_ID[esc])",
             "v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, termo=0, **ESC_ID[esc])", etq='bat: identidad v10')
    out['bateria_v144.py'] = CAB_BAT + b
    # ---- 5) bateria_generaliza_v144 <- bateria_generaliza_v143 (UNA entrada nueva, campo a campo)
    gg = origen(os.path.join(ORG, 'bateria_generaliza_v143.py'))
    m = re.search(r"^ *'organismo_v143': \(.*$", gg, re.M)
    if not m:
        raise SystemExit('*** no encuentro la entrada organismo_v143 en INSTRUMENTOS. No se escribe nada.')
    A = m.group(0)
    kw143 = re.search(r"dict\((.*?)\)\),", A).group(1)
    if kw143.strip() != KW_TRONCO_GEN:   # REGLA 14: la entrada nueva es CAMPO A CAMPO la del tronco
        raise SystemExit(f'*** los kwargs de organismo_v143 cambiaron: {kw143!r}. No se escribe nada.')
    NUEVA = ("    'organismo_v144': ('organismo_v144g', dict(" + KW_TRONCO_GEN + ")),"
             "   # v14.4 = v14.3 + TERMO (termo=1 por defecto en organismo_v144g): kwargs CAMPO A CAMPO iguales a los de organismo_v143 (regla 14)")
    gg = sust(gg, A, A + "\n" + NUEVA, etq='gen: INSTRUMENTOS')
    gg = sust(gg, "_dir = {'organismo_v14g': AQUI, 'organismo_v142g': AQUI, 'organismo_v143g': AQUI,",
              "_dir = {'organismo_v14g': AQUI, 'organismo_v142g': AQUI, 'organismo_v143g': AQUI, 'organismo_v144g': AQUI,", etq='gen: _dir')
    out['bateria_generaliza_v144.py'] = CAB_GEN + gg
    return out


if __name__ == '__main__':
    VERIFICA = '--verifica' in sys.argv
    extra = [a for a in sys.argv[1:] if a != '--verifica']
    if extra:
        raise SystemExit(f'*** banderas desconocidas: {extra} (ERR-115). Uso: construye_v144.py [--verifica]')
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
