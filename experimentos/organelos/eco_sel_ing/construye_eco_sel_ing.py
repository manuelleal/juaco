"""construye_eco_sel_ing.py — construye POR ANCLAS nucleo_eco_sel_ing.py desde experimentos/organelos/eco_sel/nucleo_eco_sel.py (sha fijado).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

ECO_SEL_ING: la MISMA genetica y la MISMA medida que ECO_SEL, pero el hijo NO hereda la tabla de la familia: cada cuerpo nace
INGENUO (carro FABRICA_ECO = FAMB_RES0_ECO sin la tabla; en el gemelo, LFAM = 0 salta _tabla_padre y _nace_fam y nada mas). Como el
linaje ingenuo NO persiste en frio (FAB_FRIO de F1: 0/20) ni tras un vivero finito (MUT0 de ECO v1.1: 0/20 x2 a 1e6), la base minima
que persiste es el VIVERO PERMANENTE (t_corte = T: un linaje extinto se refunda desde el banco en todo t < T). Cambios, cada ancla
exacta UNA vez:
  B1 cabecera del docstring (el del origen queda debajo).
  B2 BRAZOS: los cinco de ECO_SEL SIN TOCAR (el arnes los compara con nucleo_eco_sel) + ING_F1 / ING_SEL_C / ING_AZA_C (carro
     FABRICA_ECO, t_corte None = T); ING = los de la serie; VENTANAS / PRACTICA / HUMO de ECO_SEL_ING (semillas 461xx).
  B3 trabajo(): + k2 = (tn, tm, fund) de todo cuerpo vivo en algun momento de [T/2, T] (K de nacidos y de fundadores).
  B4 cb(): + k2.
  B5/B6 el checkpoint guarda y recupera k2.
  B7 res.update(...): + **_extra_ing(k2, T, P).
  B8 al final: _extra_ing() (K_nac, K_fund con el MISMO muestreo que tam_total; fund_2a = fundadores repuestos en la 2a mitad).
Con los brazos de ECO_SEL trabajo() da las MISMAS claves que nucleo_eco_sel.trabajo + las de _extra_ing (arnes (A)).

Uso: python construye_eco_sel_ing.py            # escribe nucleo_eco_sel_ing.py
     python construye_eco_sel_ing.py --verifica # el de disco == el construido (y el origen con su sha)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'eco_sel', 'nucleo_eco_sel.py')
SHA_ORIGEN = '6a36e47ce61db3e1'
DESTINO = os.path.join(AQUI, 'nucleo_eco_sel_ing.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


B1_OLD = ('"""nucleo_eco_sel.py (CONSTRUIDO por experimentos/organelos/eco_sel/construye_eco_sel.py desde experimentos/organelos/frio/'
          'corre_frio.py,\n')
B1_NEW = ('"""nucleo_eco_sel_ing.py (CONSTRUIDO por experimentos/organelos/eco_sel_ing/construye_eco_sel_ing.py desde experimentos/organelos/'
          'eco_sel/\nnucleo_eco_sel.py, sha 6a36e47ce61db3e1; NO editar a mano). ECO_SEL_ING: la genetica y la medida de ECO_SEL con el hijo '
          'INGENUO\n(carro FABRICA_ECO: sin la tabla de la familia) y VIVERO PERMANENTE (t_corte = T), la base minima en que el linaje '
          'ingenuo\npersiste. Cambios: brazos ING_*, k2 (cuerpos vivos en [T/2, T]) y _extra_ing (K_nac, K_fund, fund_2a). La LETRA esta en\n'
          'corre_eco_sel_ing.py. Lo que sigue es el docstring del origen.\n\n'
          'nucleo_eco_sel.py (CONSTRUIDO por experimentos/organelos/eco_sel/construye_eco_sel.py desde experimentos/organelos/frio/'
          'corre_frio.py,\n')

B2_OLD = ("BRAZOS = {'F1': ('MUT0', FAM, 1), 'SEL_M': ('MARGEN', FAM, 1), 'AZA_M': ('MARGEN_AZAR', FAM, 1),\n"
          "          'SEL_C': ('CEREBRO', FAM, 1), 'AZA_C': ('CEREBRO_AZAR', FAM, 1)}\n"
          "FRIOS = tuple(BRAZOS)\n"
          "VENTANAS = (45301, 45321)                 # ECO_SEL: serie y replica\n"
          "PRACTICA = tuple(range(45391, 45400))    # ECO_SEL: humo 45395; el arnes usa 45391-45394\n"
          "HUMO = dict(semilla=45395, T=200000)\n")
B2_NEW = ("BRAZOS = {'F1': ('MUT0', FAM, 1), 'SEL_M': ('MARGEN', FAM, 1), 'AZA_M': ('MARGEN_AZAR', FAM, 1),\n"
          "          'SEL_C': ('CEREBRO', FAM, 1), 'AZA_C': ('CEREBRO_AZAR', FAM, 1),\n"
          "          # ECO_SEL_ING: el hijo nace INGENUO (FABRICA_ECO: sin tabla de la familia); t_corte None = T (vivero permanente)\n"
          "          'ING_F1': ('MUT0', FAB, None), 'ING_SEL_C': ('CEREBRO', FAB, None), 'ING_AZA_C': ('CEREBRO_AZAR', FAB, None)}\n"
          "FRIOS = tuple(BRAZOS)\n"
          "ING = ('ING_F1', 'ING_SEL_C', 'ING_AZA_C')   # ECO_SEL_ING: los brazos de la serie\n"
          "VENTANAS = (46101, 46121)                 # ECO_SEL_ING: serie y replica\n"
          "PRACTICA = tuple(range(46191, 46200))    # ECO_SEL_ING: humo 46195; el arnes usa 46191-46194\n"
          "HUMO = dict(semilla=46195, T=200000)\n"
          "\n\n"
          "def tc_de(brazo, T):\n"
          "    \"\"\"ECO_SEL_ING: el t_corte del brazo (None = T: vivero permanente, se refunda en todo t < T).\"\"\"\n"
          "    tc = BRAZOS[brazo][2]\n"
          "    return T if tc is None else tc\n")

B3_OLD = "    vid = []        # ECO_SEL: (tn, tm, causa) de los NACIDOS (fund == 0) con tn >= T // 2 (vida y causas; descriptivo)\n"
B3_NEW = (B3_OLD + "    k2 = []         # ECO_SEL_ING: (tn, tm, fund) de TODO cuerpo vivo en algun momento de [T/2, T] (tm < 0: vivo al final)\n")

B4_OLD = "        if row[3] >= T // 2 and not row[6]: vid.append((row[3], row[4], row[7]))   # ECO_SEL\n"
B4_NEW = (B4_OLD + "        if row[4] < 0 or row[4] >= T // 2: k2.append((row[3], row[4], row[6]))   # ECO_SEL_ING\n")

B5_OLD = "coh=coh, vid=vid), f, protocol=pickle.HIGHEST_PROTOCOL)"
B5_NEW = "coh=coh, vid=vid, k2=k2), f, protocol=pickle.HIGHEST_PROTOCOL)"

B6_OLD = "vid[:] = d['vid']\n"
B6_NEW = "vid[:] = d['vid']; k2[:] = d['k2']\n"

B7_OLD = "**_extra_sel(vid, T, E))   # ECO_SEL\n"
B7_NEW = "**_extra_sel(vid, T, E), **_extra_ing(k2, T))   # ECO_SEL + ECO_SEL_ING\n"

B8_ADD = '''

# ================================================================================ ECO_SEL_ING (anadido por construye_eco_sel_ing.py)
def _extra_ing(k2, T):
    """ECO_SEL_ING: con el MISMO muestreo que tam_total (se cuenta al INICIO del paso t: vivo en t si tn < t y (tm >= t o sigue vivo);
    motor_eco.run_solapadas), la media en [T/2, T] (los mismos indices que kbar del runner) de los cuerpos NACIDOS (K_nac) y de los
    FUNDADORES (K_fund; con vivero permanente, los repuestos). fund_2a = fundadores con tn >= T/2 (repuestos en la segunda mitad: lo que
    cuesta establecerse). K_nac + K_fund == K (arnes)."""
    m = MUNDO['muestra']; i0 = (T // 2) // m; n = T // m + 1
    ts = np.arange(i0, n, dtype=np.int64) * m
    out = {}
    for nom, f in (('K_nac', 0), ('K_fund', 1)):
        tn = np.sort(np.array([a for a, b, c in k2 if int(c) == f], dtype=np.int64))
        tm = np.sort(np.array([b for a, b, c in k2 if int(c) == f and b >= 0], dtype=np.int64))
        cnt = np.searchsorted(tn, ts, side='left') - np.searchsorted(tm, ts, side='left')
        out[nom] = round(float(np.mean(cnt)), 6) if len(ts) else None
    out['fund_2a'] = int(sum(1 for a, b, c in k2 if int(c) == 1 and a >= T // 2 and a > 0))
    out['n_k2'] = len(k2)
    return out
'''

ANCLAS = [('B1', B1_OLD, B1_NEW), ('B2', B2_OLD, B2_NEW), ('B3', B3_OLD, B3_NEW), ('B4', B4_OLD, B4_NEW), ('B5', B5_OLD, B5_NEW),
          ('B6', B6_OLD, B6_NEW), ('B7', B7_OLD, B7_NEW)]


def construye():
    sh = h16(ORIGEN)
    if sh != SHA_ORIGEN: raise SystemExit(f"construye_eco_sel_ing: {ORIGEN} tiene sha {sh}, se esperaba {SHA_ORIGEN}")
    txt = open(ORIGEN, encoding='utf-8', newline='').read()
    for nom, old, new in ANCLAS:
        n = txt.count(old)
        if n != 1: raise SystemExit(f"construye_eco_sel_ing: el ancla {nom} aparece {n} veces (se espera 1)")
        txt = txt.replace(old, new)
    return txt.rstrip('\n') + '\n' + B8_ADD


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    txt = construye()
    if '--verifica' in argv:
        ok = os.path.exists(DESTINO) and open(DESTINO, encoding='utf-8', newline='').read() == txt
        print(f"construye_eco_sel_ing --verifica: {'IGUAL' if ok else 'DISTINTO'} (origen {SHA_ORIGEN}; destino "
              f"{h16(DESTINO) if os.path.exists(DESTINO) else None})")
        return ok
    with open(DESTINO, 'w', encoding='utf-8', newline='') as f: f.write(txt)
    print(f"escrito {DESTINO} (sha {h16(DESTINO)}) desde {ORIGEN} ({SHA_ORIGEN}); anclas {[a[0] for a in ANCLAS]} + B8")
    return True


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
