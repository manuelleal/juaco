import re
p='construye_molde.py'; s=open(p,encoding='utf-8').read()
def uno(a, b):
    global s
    n = s.count(a); assert n == 1, (n, a[:60]); s = s.replace(a, b)
# 1) constantes: insertar tras la linea de BARRE_FRAC (buscada por regex)
m = re.search(r"\n(     'BARRE_FRAC = 0\.8;[^\n]*\n)", s); assert m, 'no BARRE_FRAC'
lin = m.group(1)
uno(lin, lin + "     'BARRE_V2 = 0; BARRE_CADA = 200   # dosis 2: muerde solo si el mundo esta tapado EN ESTE PASO, fuera de la ventana de parto y a lo sumo una vez cada BARRE_CADA pasos\n'\n")
# 2) estado
uno("t_primera_lectura=None, ads_cult=0, tapado=0, barre_obj=0, barridas=0)",
    "t_primera_lectura=None, ads_cult=0, tapado=0, barre_obj=0, barridas=0, barre_veto_ventana=0)\n        self._mol_tap = False; self._mol_tb = -10 ** 9")
# 3) _mol_barre registra tapado y respeta la ventana en dosis 2
uno("""        obst = self._v3o
        if not obst or not objs: return d, k, left
        nb = sum(1 for v in objs.values() if v in obst)
        if nb < BARRE_FRAC * len(objs): return d, k, left
        self._mol['tapado'] += 1""",
"""        obst = self._v3o; self._mol_tap = False
        if not obst or not objs: return d, k, left
        nb = sum(1 for v in objs.values() if v in obst)
        if nb < BARRE_FRAC * len(objs): return d, k, left
        self._mol['tapado'] += 1; self._mol_tap = True
        if BARRE_V2 and (E >= self.rep_umbral and Ag >= self.rep_umbral): return d, k, left   # dosis 2: la ventana de parto manda""")
# 4) la mordida de destape
uno("""        if v[1] < 0 and Ag < BARRE_RES: return False
        return True""",
"""        if v[1] < 0 and Ag < BARRE_RES: return False
        return True

    def _mol_barre_boca(self, kk, E, Ag, t):
        \"\"\"La mordida de destape. Dosis 1 (BARRE_V2 = 0): basta la reserva. Dosis 2: ademas el mundo tapado en este paso, fuera de la
        ventana de parto y con refractario BARRE_CADA.\"\"\"
        if not self._mol_puede(kk, E, Ag): return False
        if BARRE_V2:
            if not self._mol_tap or t - self._mol_tb < BARRE_CADA: return False
            if E >= self.rep_umbral and Ag >= self.rep_umbral: self._mol['barre_veto_ventana'] += 1; return False
        self._mol_tb = t; self._mol['barridas'] += 1
        return True""")
# 5) ancla de la boca
m2 = re.search(r"\n(     \"                if MOLDE and BARRE and self\._mol_puede\(kk, E, Ag\): mordio = True; self\._mol\['barridas'\] \+= 1[^\n]*\n)", s); assert m2, 'no ancla boca'
uno(m2.group(1), "     \"                if MOLDE and BARRE and self._mol_barre_boca(kk, E, Ag, t): mordio = True   # MOLDE BARRE: destapa el mundo\n\"),\n")
open(p,'w',encoding='utf-8').write(s)
q='corre_molde.py'; r=open(q,encoding='utf-8').read()
def uno2(a,b):
    global r
    assert r.count(a)==1, a[:50]; r=r.replace(a,b)
uno2("PERILLAS = ('PIZ', 'PIZ_BAR', 'PIZ_FUND', 'IMITA', 'ESPERA', 'PIZ_ADS', 'BARRE')","PERILLAS = ('PIZ', 'PIZ_BAR', 'PIZ_FUND', 'IMITA', 'ESPERA', 'PIZ_ADS', 'BARRE', 'BARRE_V2')")
uno2("    'o1':       None,\n","    # ola 3 (tras leer barre s38002: la dosis 1 limpia el mundo y esteriliza: desc 0)\n    'barre2':     dict(BARRE=1, BARRE_V2=1),\n    'piz_barre2': dict(PIZ=1, BARRE=1, BARRE_V2=1),\n    'o1':       None,\n")
uno2("barridas {sum(x['barridas'] for x in mol)} ·","barridas {sum(x['barridas'] for x in mol)} veto_vent {sum(x['barre_veto_ventana'] for x in mol)} · desc {sum(d['descendientes'] for d in r['linajes'])} ·")
uno2("for br in ('piz', 'imita', 'espera', 'piz_ads', 'piz_barre', 'piz_ads_barre'):","for br in ('piz', 'imita', 'espera', 'piz_ads', 'piz_barre', 'piz_ads_barre', 'barre2', 'piz_barre2'):")
open(q,'w',encoding='utf-8').write(r); print('parche ok')
