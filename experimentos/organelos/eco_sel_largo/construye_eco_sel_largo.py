"""construye_eco_sel_largo.py — construye POR ANCLAS nucleo_eco_sel_largo.py desde experimentos/organelos/eco_sel/nucleo_eco_sel.py
(sha fijado; ese nucleo es a su vez el construido por anclas desde frio/corre_frio.py y se verifica con construye_eco_sel --verifica).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

ECO_SEL LARGO (frente 2, 28-sep-2026): las dos preguntas del ENCARGO_NUBE_largo.md — L (con T = 1e7, ¿K sigue subiendo o se estanca?) y
MC (margen + cerebro heredables a la vez, ¿K supera a SEL_C?). El nucleo, el mundo, el carro, el gemelo y la genetica de eco_sel NO
cambian. Cambios, cada ancla exacta UNA vez:
  B1 cabecera del docstring (el de nucleo_eco_sel queda debajo).
  B2 BRAZOS: + SEL_MC (genetica MC) y AZA_MC (MC_AZAR). Los cinco de eco_sel quedan como estaban.
  B3 VENTANAS (45401 serie, 45421 replica) / PRACTICA (45491-45499) / HUMO (45491, T 200 000).
  B4 GENETICAS: + MC (rep_umbral + los 15 del cerebro, en el orden de motor_eco.NOMBRES, con herencia) y MC_AZAR (lo mismo, donante
     'azar'). Misma p (SERIE['p_mut'] = 0.05) y sigma (0.15) por gen que eco_sel: la expresion es eco_de() sin tocar.
  B5 trabajo(): + tel = _Tel(T) (telemetria por ventanas de T/10: vivos y genes en el borde de cada ventana, nacimientos, muertes por
     causa y vida media por ventana), alimentada desde el MISMO cb (ind_cb) que ya ve a todo individuo al morir o vivo en T.
  B6/B7 el checkpoint guarda y recupera tel.
  B8 checkpoint cada CKPT_LARGO = 100 000 pasos (eco_sel: SERIE['ckpt_cada'] = 10 000). Multiplo de cada_gen (2000): los tramos del gemelo
     son los mismos (arnes: F1 y SEL_C == eco_sel bit a bit a T 1e6). Porque: el blob crece con gen_t (una fila cada 2000 pasos) y con
     filas/coh; a 1e7 escribir 1000 blobs crecientes costaria O(T^2).
  B9 res.update(...): + **_extra_largo(tel, E).
  B10 al final: CKPT_LARGO, N_VENT, _Tel y _extra_largo().
Con los brazos de eco_sel, trabajo() da TODAS las claves de nucleo_eco_sel.trabajo bit a bit (arnes (A)) mas la clave 'ventanas'.

Uso: python construye_eco_sel_largo.py            # escribe nucleo_eco_sel_largo.py
     python construye_eco_sel_largo.py --verifica # el de disco == el construido (y el origen con su sha)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'eco_sel', 'nucleo_eco_sel.py')
SHA_ORIGEN = '6a36e47ce61db3e1'
DESTINO = os.path.join(AQUI, 'nucleo_eco_sel_largo.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


B1_OLD = '"""nucleo_eco_sel.py (CONSTRUIDO por experimentos/organelos/eco_sel/construye_eco_sel.py desde'
B1_NEW = ('"""nucleo_eco_sel_largo.py (CONSTRUIDO por experimentos/organelos/eco_sel_largo/construye_eco_sel_largo.py desde\n'
          'experimentos/organelos/eco_sel/nucleo_eco_sel.py, sha 6a36e47ce61db3e1; NO editar a mano). ECO_SEL LARGO: + brazos SEL_MC y AZA_MC\n'
          '(rep_umbral + 15 genes del cerebro, con y sin herencia), telemetria por ventanas de T/10 (_Tel, _extra_largo) y checkpoint cada\n'
          '100 000 pasos. La LETRA esta en corre_eco_sel_largo.py; la del docstring de abajo NO rige aqui. Lo que sigue es el docstring del origen.\n\n'
          'nucleo_eco_sel.py (CONSTRUIDO por experimentos/organelos/eco_sel/construye_eco_sel.py desde')

B2_OLD = "          'SEL_C': ('CEREBRO', FAM, 1), 'AZA_C': ('CEREBRO_AZAR', FAM, 1)}\n"
B2_NEW = ("          'SEL_C': ('CEREBRO', FAM, 1), 'AZA_C': ('CEREBRO_AZAR', FAM, 1),\n"
          "          'SEL_MC': ('MC', FAM, 1), 'AZA_MC': ('MC_AZAR', FAM, 1)}   # LARGO: margen + cerebro, con y sin herencia\n")

B3_OLD = ("VENTANAS = (45301, 45321)                 # ECO_SEL: serie y replica\n"
          "PRACTICA = tuple(range(45391, 45400))    # ECO_SEL: humo 45395; el arnes usa 45391-45394\n"
          "HUMO = dict(semilla=45395, T=200000)\n")
B3_NEW = ("VENTANAS = (45401, 45421)                 # LARGO: serie y replica\n"
          "PRACTICA = tuple(range(45491, 45500))    # LARGO: humo 45491; el arnes usa 45492-45496\n"
          "HUMO = dict(semilla=45491, T=200000)\n")

B4_OLD = "             'CEREBRO_AZAR': dict(mutables=CR.BRAZOS['CEREBRO']['mutables'], donante='azar', p=True)}\n"
B4_NEW = ("             'CEREBRO_AZAR': dict(mutables=CR.BRAZOS['CEREBRO']['mutables'], donante='azar', p=True),\n"
          "             # LARGO: MC = rep_umbral + los 15 del cerebro (dote y rep_X fijos), en el orden de motor_eco.NOMBRES\n"
          "             'MC': dict(mutables=tuple(g for g in CR.ME.NOMBRES if g not in ('dote', 'rep_X')), donante='padre', p=True),\n"
          "             'MC_AZAR': dict(mutables=tuple(g for g in CR.ME.NOMBRES if g not in ('dote', 'rep_X')), donante='azar', p=True)}\n")

B5_OLD = "    vid = []        # ECO_SEL: (tn, tm, causa) de los NACIDOS (fund == 0) con tn >= T // 2 (vida y causas; descriptivo)\n"
B5_NEW = (B5_OLD + "    tel = _Tel(T)   # LARGO: telemetria por ventanas de T/10\n")
B5b_OLD = "        if row[3] >= T // 2 and not row[6]: vid.append((row[3], row[4], row[7]))   # ECO_SEL\n"
B5b_NEW = B5b_OLD + "        tel.cb(row, g)   # LARGO\n"

B6_OLD = "pickle.dump(dict(t=t, blob=blob, filas=filas, coh=coh, vid=vid), f, protocol=pickle.HIGHEST_PROTOCOL)"
B6_NEW = "pickle.dump(dict(t=t, blob=blob, filas=filas, coh=coh, vid=vid, tel=tel.estado()), f, protocol=pickle.HIGHEST_PROTOCOL)"
B7_OLD = "filas[:] = d['filas']; coh[:] = d['coh']; vid[:] = d['vid']\n"
B7_NEW = "filas[:] = d['filas']; coh[:] = d['coh']; vid[:] = d['vid']; tel.carga(d['tel'])   # LARGO\n"

B8_OLD = "eco=eco_de(gen_brazo, t_corte, ckpt_cada=SERIE['ckpt_cada'], ckpt_fn=guarda,"
B8_NEW = "eco=eco_de(gen_brazo, t_corte, ckpt_cada=CKPT_LARGO, ckpt_fn=guarda,"

B9_OLD = "lim_nac=_lim_nac(), **_extra_sel(vid, T, E))   # ECO_SEL\n"
B9_NEW = "lim_nac=_lim_nac(), **_extra_sel(vid, T, E), **_extra_largo(tel, E))   # ECO_SEL + LARGO\n"

B10_ADD = r'''

# ================================================================================ ECO_SEL LARGO (anadido por construye_eco_sel_largo.py)
CKPT_LARGO = 100000   # checkpoint cada 100 000 pasos (multiplo de cada_gen 2000: mismos tramos del gemelo)
N_VENT = 10           # ventanas de T/10 (a T = 1e7: ventanas de 1e6)


class _Tel:
    """Telemetria por ventanas, alimentada por ind_cb (cada individuo pasa UNA vez: al morir, o vivo en T con tm = -1).
    Ventana k (1..N_VENT) = pasos [W_{k-1}, W_k - 1], W_k = k*T/N_VENT. 'Vivo en el borde W' = el estado tras el paso W - 1 (el mismo
    instante que la fila de gen_t de t = W y que tam_total[W // muestra]): tn <= W - 1 y (tm == -1 o tm >= W).
    Guarda: genomas de los vivos en cada borde; nacimientos (fund == 0) por ventana de tn; muertes por causa y suma de vidas por ventana
    de tm (todo cuerpo, fundadores incluidos)."""

    def __init__(self, T):
        if T % N_VENT: raise SystemExit(f"LARGO: T = {T} no es multiplo de {N_VENT}")
        self.T = int(T); self.V = self.T // N_VENT
        self.W = [self.V * k for k in range(1, N_VENT + 1)]
        self.viv = [[] for _ in self.W]
        self.nac = [0] * N_VENT
        self.mue = [[0, 0, 0, 0] for _ in self.W]
        self.vida = [0] * N_VENT

    def cb(self, row, g):
        tn, tm, fund, cz = int(row[3]), int(row[4]), int(row[6]), int(row[7])
        if not fund and 0 <= tn < self.T: self.nac[tn // self.V] += 1
        if tm >= 0:
            k = min(tm // self.V, N_VENT - 1)
            if 0 <= cz < 4: self.mue[k][cz] += 1
            self.vida[k] += tm - tn
        for k, W in enumerate(self.W):
            if tn <= W - 1 and (tm == -1 or tm >= W): self.viv[k].append([float(x) for x in g])

    def estado(self):
        return dict(T=self.T, viv=self.viv, nac=self.nac, mue=self.mue, vida=self.vida)

    def carga(self, d):
        if d['T'] != self.T: raise SystemExit('LARGO: checkpoint de otro T')
        self.viv = d['viv']; self.nac = d['nac']; self.mue = d['mue']; self.vida = d['vida']


def _extra_largo(tel, E):
    """LARGO: la telemetria por ventana. Genes: SOLO los mutables del brazo (los demas son G0 por construccion; V3 lo comprueba), en valor
    crudo: media y cuantiles 10/50/90 (np.quantile, lineal) sobre los vivos en el borde; media_log = media de log(g/G0) de los 18 genes
    (la misma cantidad que la columna [4] de gen_t en t = W: el arnes la compara). Sin vivos: None."""
    G = list(E['genes']); mut = list(E['mutables']); G0 = np.array(E['G0'], float)
    genes = {g: dict(media=[], q10=[], q50=[], q90=[]) for g in mut}
    media_log = []
    for V in tel.viv:
        A = np.array(V, float) if V else None
        media_log.append([round(float(x), 5) for x in np.log(A / G0).mean(0)] if V else None)
        for g in mut:
            j = G.index(g)
            if V:
                q = np.quantile(A[:, j], [0.1, 0.5, 0.9])
                genes[g]['media'].append(round(float(A[:, j].mean()), 6))
                genes[g]['q10'].append(round(float(q[0]), 6)); genes[g]['q50'].append(round(float(q[1]), 6)); genes[g]['q90'].append(round(float(q[2]), 6))
            else:
                for c in ('media', 'q10', 'q50', 'q90'): genes[g][c].append(None)
    nm = [sum(m) for m in tel.mue]
    return dict(ventanas=dict(W=list(tel.W), vivos=[len(V) for V in tel.viv], nac=list(tel.nac), muertes=[list(m) for m in tel.mue],
                              vida_media=[(round(tel.vida[k] / nm[k], 1) if nm[k] else None) for k in range(N_VENT)],
                              genes=genes, media_log=media_log))
'''

ANCLAS = [('B1', B1_OLD, B1_NEW), ('B2', B2_OLD, B2_NEW), ('B3', B3_OLD, B3_NEW), ('B4', B4_OLD, B4_NEW), ('B5', B5_OLD, B5_NEW),
          ('B5b', B5b_OLD, B5b_NEW), ('B6', B6_OLD, B6_NEW), ('B7', B7_OLD, B7_NEW), ('B8', B8_OLD, B8_NEW), ('B9', B9_OLD, B9_NEW)]


def construye():
    sh = h16(ORIGEN)
    if sh != SHA_ORIGEN: raise SystemExit(f"construye_eco_sel_largo: {ORIGEN} tiene sha {sh}, se esperaba {SHA_ORIGEN}")
    txt = open(ORIGEN, encoding='utf-8', newline='').read()
    for nom, old, new in ANCLAS:
        n = txt.count(old)
        if n != 1: raise SystemExit(f"construye_eco_sel_largo: el ancla {nom} aparece {n} veces (se espera 1)")
        txt = txt.replace(old, new)
    return txt.rstrip('\n') + '\n' + B10_ADD


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    txt = construye()
    if '--verifica' in argv:
        ok = os.path.exists(DESTINO) and open(DESTINO, encoding='utf-8', newline='').read() == txt
        print(f"construye_eco_sel_largo --verifica: {'IGUAL' if ok else 'DISTINTO'} (origen {SHA_ORIGEN}; destino "
              f"{h16(DESTINO) if os.path.exists(DESTINO) else None})")
        return ok
    with open(DESTINO, 'w', encoding='utf-8', newline='') as f: f.write(txt)
    print(f"escrito {DESTINO} (sha {h16(DESTINO)}) desde {ORIGEN} ({SHA_ORIGEN}); anclas {[a[0] for a in ANCLAS]} + B10")
    return True


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
