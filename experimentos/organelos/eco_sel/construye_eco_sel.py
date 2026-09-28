"""construye_eco_sel.py — construye POR ANCLAS nucleo_eco_sel.py desde experimentos/organelos/frio/corre_frio.py (sha fijado).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

ECO_SEL (frente 2): F1 ARRANQUE EN FRIO + seleccion natural encima, sin vivero y sin fundadores repuestos. Lo que se copia es la parte
de corre_frio.py que CORRE (imports, constantes, usa_gemelo, trabajo, _lim_nac); su letra (veredicto, lee, humo, main, parsea) NO se
copia: la letra de ECO_SEL vive en corre_eco_sel.py. Cambios, cada ancla exacta UNA vez:
  A1 cabecera del docstring (el del origen queda debajo).
  A2 sys.path: + experimentos/organelos/frio (motor_frio_rapido, el gemelo de F1, se IMPORTA sin tocar; sha fijado).
  A3 BRAZOS / FRIOS / VENTANAS / PRACTICA / HUMO de ECO_SEL + GENETICAS + eco_de() (la expresion de corre_eco.eco_cfg con la genetica
     del brazo) + _SIGMA / _PMUT (SOLO el arnes los fija).
  A4 cb(): + vid = (tn, tm, causa) de los NACIDOS con tn >= T // 2 (vida y causas de la segunda mitad; descriptivo).
  A5/A6 el checkpoint guarda y recupera vid.
  A7 trabajo(): eco=eco_de(...) en vez de eco=CR.eco_cfg(...).
  A8 res.update(...): + **_extra_sel(vid, T, E).
  A9 al final: T_SEL y _extra_sel() (seleccion contra sombras en T_SEL y en T, genes de los vivos, genes fuera de los mutables).
Con el brazo F1 (MUT0, t_corte 1) trabajo() da las MISMAS claves que corre_frio.trabajo(RES0_FRIO) bit a bit (arnes (A)).

Uso: python construye_eco_sel.py            # escribe nucleo_eco_sel.py
     python construye_eco_sel.py --verifica # el de disco == el construido (y los origenes con su sha)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'frio', 'corre_frio.py')
SHA_ORIGEN = '3ba8b0f5cf1fbbfa'
DESTINO = os.path.join(AQUI, 'nucleo_eco_sel.py')
CORTE = '# ================================================================================ LA LETRA (PREREGISTRO_frio.md §6)\n'


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


A1_OLD = '"""corre_frio.py — RUNNER y LETRA de F1 ARRANQUE EN FRIO (comite de linaje, ficha F1; 25-sep-2026).\n'
A1_NEW = ('"""nucleo_eco_sel.py (CONSTRUIDO por experimentos/organelos/eco_sel/construye_eco_sel.py desde experimentos/organelos/frio/'
          'corre_frio.py,\nsha 3ba8b0f5cf1fbbfa; NO editar a mano). ECO_SEL: F1 ARRANQUE EN FRIO + SELECCION NATURAL ENCIMA (sin vivero, sin '
          'fundadores\nrepuestos). Cambios: brazos y genetica de ECO_SEL (eco_de), vida y causas de la segunda mitad (vid), seleccion contra '
          'sombras\nen T_SEL y en T (_extra_sel). La LETRA de ECO_SEL esta en corre_eco_sel.py; el uso y la letra que describe el docstring '
          'del\norigen (abajo) NO rigen aqui. Lo que sigue es el docstring del origen.\n\n'
          'corre_frio.py — RUNNER y LETRA de F1 ARRANQUE EN FRIO (comite de linaje, ficha F1; 25-sep-2026).\n')

A2_OLD = "ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')\nfor _d in (ECO, AQUI):\n"
A2_NEW = ("ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')\n"
          "FRIO_DIR = os.path.join(RAIZ, 'experimentos', 'organelos', 'frio')   # ECO_SEL: el gemelo de F1 (motor_frio_rapido) se IMPORTA de alli\n"
          "for _d in (ECO, FRIO_DIR, AQUI):\n")

A3_OLD = ("BRAZOS = {'RES0_FRIO': ('MUT0', FAM, 1), 'RES0_10k': ('MUT0', FAM, 10000), 'RES0_60k': ('MUT0', FAM, 60000),\n"
          "          'BAR0_FRIO': ('MUT0', BAR, 1), 'FAB_FRIO': ('MUT0', FAB, 1)}\n"
          "FRIOS = ('RES0_FRIO', 'BAR0_FRIO', 'FAB_FRIO')\n"
          "VENTANAS = (35001, 35021)                 # serie y replica\n"
          "PRACTICA = tuple(range(35901, 35910))    # humo 35905; el arnes usa 35901-35904\n"
          "HUMO = dict(semilla=35905, T=200000)\n")
A3_NEW = ("# ECO_SEL: los cinco brazos, TODOS en frio (t_corte = 1) con el carro de la familia (FAMB_RES0_ECO); solo cambia la genetica.\n"
          "BRAZOS = {'F1': ('MUT0', FAM, 1), 'SEL_M': ('MARGEN', FAM, 1), 'AZA_M': ('MARGEN_AZAR', FAM, 1),\n"
          "          'SEL_C': ('CEREBRO', FAM, 1), 'AZA_C': ('CEREBRO_AZAR', FAM, 1)}\n"
          "FRIOS = tuple(BRAZOS)\n"
          "VENTANAS = (45301, 45321)                 # ECO_SEL: serie y replica\n"
          "PRACTICA = tuple(range(45391, 45400))    # ECO_SEL: humo 45395; el arnes usa 45391-45394\n"
          "HUMO = dict(semilla=45395, T=200000)\n"
          "# ECO_SEL: la genetica de cada brazo; la expresion es la de corre_eco.eco_cfg (banco 200, 8 sombras, p_mut 0.05, sigma 0.15, genes\n"
          "# cada 2000). MUT0 = corre_eco.BRAZOS['MUT0'] (el F1). CEREBRO = corre_eco.BRAZOS['CEREBRO'] (15 genes: todos menos dote, rep_umbral\n"
          "# y rep_X). MARGEN = SOLO rep_umbral: el margen m = 1 - rep_umbral entre la consigna del hambre del carro (hambre = clip(1 - E)) y el\n"
          "# umbral de parto. *_AZAR = el mismo gen sin herencia: el genoma de todo cuerpo nuevo sale de una entrada AL AZAR del banco, mutada\n"
          "# (donante 'azar' de motor_eco: el banco guarda el genoma NUEVO; el genoma nunca influye en su propia copia).\n"
          "GENETICAS = {'MUT0': dict(mutables=None, donante='padre', p=False),\n"
          "             'MARGEN': dict(mutables=('rep_umbral',), donante='padre', p=True),\n"
          "             'MARGEN_AZAR': dict(mutables=('rep_umbral',), donante='azar', p=True),\n"
          "             'CEREBRO': dict(mutables=CR.BRAZOS['CEREBRO']['mutables'], donante='padre', p=True),\n"
          "             'CEREBRO_AZAR': dict(mutables=CR.BRAZOS['CEREBRO']['mutables'], donante='azar', p=True)}\n"
          "_SIGMA = [None]   # ECO_SEL: SOLO el arnes lo fija (sigma 0 -> el gen fijo == F1 bit a bit); None = SERIE['sigma']\n"
          "_PMUT = [None]    # ECO_SEL: SOLO el arnes lo fija (p_mut 1 -> prueba de herencia); None = SERIE['p_mut']\n"
          "\n"
          "\n"
          "def eco_de(gen, t_corte, **extra):\n"
          "    \"\"\"ECO_SEL: la expresion de corre_eco.eco_cfg con la genetica GENETICAS[gen] (arnes: == eco_cfg en MUT0 y CEREBRO).\"\"\"\n"
          "    b = GENETICAS[gen]\n"
          "    pm = SERIE['p_mut'] if _PMUT[0] is None else float(_PMUT[0])\n"
          "    return dict(refunda=1, t_corte=t_corte, p_mut=(pm if b['p'] else 0.0), sigma=(SERIE['sigma'] if _SIGMA[0] is None else float(_SIGMA[0])),\n"
          "                banco=SERIE['banco'], n_sombra=SERIE['n_sombra'], cada_gen=SERIE['cada_gen'], mutables=b['mutables'],\n"
          "                donante=b['donante'], **extra)\n")

A4_OLD = ("    c0 = FRIO['coh_desde']\n\n    def cb(li, row, g):\n        if row[3] >= t_corte: filas.append([li] + row)\n"
          "        if row[3] >= c0 and not row[6]: coh.append((row[3], row[5]))\n")
A4_NEW = ("    c0 = FRIO['coh_desde']\n"
          "    vid = []        # ECO_SEL: (tn, tm, causa) de los NACIDOS (fund == 0) con tn >= T // 2 (vida y causas; descriptivo)\n\n"
          "    def cb(li, row, g):\n        if row[3] >= t_corte: filas.append([li] + row)\n"
          "        if row[3] >= c0 and not row[6]: coh.append((row[3], row[5]))\n"
          "        if row[3] >= T // 2 and not row[6]: vid.append((row[3], row[4], row[7]))   # ECO_SEL\n")

A5_OLD = "pickle.dump(dict(t=t, blob=blob, filas=filas, coh=coh), f, protocol=pickle.HIGHEST_PROTOCOL)"
A5_NEW = "pickle.dump(dict(t=t, blob=blob, filas=filas, coh=coh, vid=vid), f, protocol=pickle.HIGHEST_PROTOCOL)"

A6_OLD = "d = pickle.load(open(ck, 'rb')); estado = d['blob']; filas[:] = d['filas']; coh[:] = d['coh']"
A6_NEW = "d = pickle.load(open(ck, 'rb')); estado = d['blob']; filas[:] = d['filas']; coh[:] = d['coh']; vid[:] = d['vid']"

A7_OLD = "eco=CR.eco_cfg(gen_brazo, t_corte, ckpt_cada=SERIE['ckpt_cada'], ckpt_fn=guarda, estado=estado, ind_cb=cb))"
A7_NEW = "eco=eco_de(gen_brazo, t_corte, ckpt_cada=SERIE['ckpt_cada'], ckpt_fn=guarda, estado=estado, ind_cb=cb))   # ECO_SEL"

A8_OLD = "vivos_1k=[int(x) for x in P['tam_total'][:11]], lim_nac=_lim_nac())"
A8_NEW = "vivos_1k=[int(x) for x in P['tam_total'][:11]], lim_nac=_lim_nac(), **_extra_sel(vid, T, E))   # ECO_SEL"

A9_ADD = '''

# ================================================================================ ECO_SEL (anadido por construye_eco_sel.py)
T_SEL = 100000   # la prueba contra sombras se lee en t = 100 000 (~60 generaciones); a 1e6 la deriva de las sombras llena el rango


def _extra_sel(vid, T, E):
    """ECO_SEL: vida y causas de los NACIDOS en la segunda mitad; seleccion del BANCO contra sus 8 sombras (corre_eco.sel_genes) en T_SEL y
    en T; media de los genes mutables en los vivos en T; cuantos valores de genes NO mutables difieren de G0 en los vivos (debe ser 0)."""
    G = list(E['genes']); mut = list(E['mutables']); g0r = [round(float(x), 6) for x in E['G0']]
    fil = {f[0]: f for f in E['gen_t']}
    muertos = [tm - tn for tn, tm, c in vid if tm >= 0]
    cz = [0, 0, 0, 0]
    for tn, tm, c in vid:
        if tm >= 0 and 0 <= c < 4: cz[c] += 1
    V = [v[4:] for v in E['vivos_final']]
    fuera = sum(1 for g in V for j in range(len(G)) if G[j] not in mut and g[j] != g0r[j])
    movidos = sum(1 for g in V for j in range(len(G)) if G[j] in mut and g[j] != g0r[j])
    med = ({G[j]: round(float(np.mean([g[j] for g in V])), 6) for j in range(len(G)) if G[j] in mut} if V else None)
    return dict(mutables=mut, p_mut=E['p_mut'], sigma=E['sigma'], donante=E['donante'], n_mut=E['n_mut'],
                nac_2a=len(vid), vida_media_muertos_2a=(round(float(np.mean(muertos)), 1) if muertos else None),
                vivos_T_de_2a=sum(1 for tn, tm, c in vid if tm < 0), causas_2a=cz,
                sel_100k=CR.sel_genes(fil.get(T_SEL)), sel_T=CR.sel_genes(fil.get(T)),
                genes_vivos_T=med, fuera_mutables=int(fuera), movidos_mutables=int(movidos))
'''

ANCLAS = [('A1', A1_OLD, A1_NEW), ('A2', A2_OLD, A2_NEW), ('A3', A3_OLD, A3_NEW), ('A4', A4_OLD, A4_NEW), ('A5', A5_OLD, A5_NEW),
          ('A6', A6_OLD, A6_NEW), ('A7', A7_OLD, A7_NEW), ('A8', A8_OLD, A8_NEW)]


def construye():
    sh = h16(ORIGEN)
    if sh != SHA_ORIGEN: raise SystemExit(f"construye_eco_sel: {ORIGEN} tiene sha {sh}, se esperaba {SHA_ORIGEN}")
    txt = open(ORIGEN, encoding='utf-8', newline='').read()
    if txt.count(CORTE) != 1: raise SystemExit('construye_eco_sel: el corte (LA LETRA) no esta exactamente una vez')
    txt = txt[:txt.index(CORTE)].rstrip('\n') + '\n'
    for nom, old, new in ANCLAS:
        n = txt.count(old)
        if n != 1: raise SystemExit(f"construye_eco_sel: el ancla {nom} aparece {n} veces (se espera 1)")
        txt = txt.replace(old, new)
    return txt + A9_ADD


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    txt = construye()
    if '--verifica' in argv:
        ok = os.path.exists(DESTINO) and open(DESTINO, encoding='utf-8', newline='').read() == txt
        print(f"construye_eco_sel --verifica: {'IGUAL' if ok else 'DISTINTO'} (origen {SHA_ORIGEN}; destino "
              f"{h16(DESTINO) if os.path.exists(DESTINO) else None})")
        return ok
    with open(DESTINO, 'w', encoding='utf-8', newline='') as f: f.write(txt)
    print(f"escrito {DESTINO} (sha {h16(DESTINO)}) desde {ORIGEN} ({SHA_ORIGEN}); anclas {[a[0] for a in ANCLAS]} + A9")
    return True


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
