"""mundo_familia.py — EL MUNDO DEL TRAMO D de la escalera ("SEXO Y FAMILIA", idea del director 30-sep noche): motor_eco.run_solapadas
(JUACO-ECO: poblacion, parto real, genoma por cuerpo, quimiostato) + CUATRO perillas de FISICA del mundo, cada una apagada = bit a bit.
30-sep-2026, ingeniero genetico Fable, MODO RAFAGA. Plan: ESCALERA.md (tramo D). Runner: corre_d.py. Arnes: identidad_d.py.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE ES: experimentos/juaco_eco/motor_eco.py (sha SHA_MOTOR, NO se toca: se extrae run_solapadas y se aplican ANCLAS, cada una exactamente
una vez; el codigo transformado corre con los globales de motor_eco) con el kwarg nuevo familia=None | dict(...):
  sexo (D1, 0/1): cada cuerpo tiene un TIPO X/Y (fundadores: indice del linaje mod 2; refundados igual; el hijo toma el tipo de la madre o del
       padre con p 0.5, rng [seed, i, 22, k]). Un cuerpo que completa su ventana SOLO pare si hay PAREJA: un cuerpo vivo del mismo carro
       (misma etiqueta), del OTRO tipo, a distancia <= r_par. Sin pareja la ventana se reinicia (sin_pareja). Evitar no es gratis.
  recombina (D1, 0/1; exige sexo y eco): el genoma del hijo = por gen, el de la madre o el del padre con p 0.5 (rng [seed, i, 20, k]) y
       DESPUES la mutacion de siempre del motor. Con 0: clon de la madre con pareja obligatoria (el control de D1: mismo costo).
  pareja (D2, 'azar' | 'fuerte'; exige sexo): entre las parejas posibles, 'azar' sortea una (rng [seed, i, 21, k]); 'fuerte' toma la de
       MAYOR reserva real E + Ag (senal honesta: es el estado fisico, no una declaracion del carro; empates: la primera en el orden de la lista).
  dote_doble (D3, 0/1; exige sexo): los dos padres pagan la dote por mitades; el hijo recibe lo mismo.
  camada (D4, 0/1): en la fase B, un cuerpo con E o Ag < u_cam y >= 2 hijos vivos a <= r_par: el hijo MAS DEBIL (menor E + Ag) muere (E = Ag = 0;
       el motor lo cuenta como hambre/sed: declarado; aqui se cuenta 'trofico') y su reserva pasa al padre (a_quien 'padre') o al hermano mas
       fuerte ('hermano'). Regla local sin rng.
NIETOS (la moneda que pide el director) se leen de la fisica que el motor ya escribe (individuos: gen >= 2), en corre_d.
SALIDA NUEVA (solo con familia): d['_carrera']['familia'] por linaje y pista['familia'].
"""
import hashlib, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ECO_D = os.path.join(RAIZ, 'experimentos', 'juaco_eco'); GEN_D = os.path.join(RAIZ, 'experimentos', 'generaciones')
for _d in (ECO_D, GEN_D):
    if _d not in sys.path: sys.path.insert(0, _d)
import motor_eco as MEC

SHAS = dict(motor_eco='bca3033878b59622')   # motor_eco.py medido el 30-sep (construido por construye_eco.py desde motor_convive d10cb9021f5d0f41)
ETQ_SEXO = 20; ETQ_PAREJA = 21; ETQ_TIPO = 22
FAM_DEF = dict(sexo=0, recombina=0, pareja='azar', r_par=10, dote_doble=0, camada=0, u_cam=0.4, a_quien='padre')

FIRMA_VIEJA = ("def run_solapadas(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None,\n"
               "                  fundador_limpio=0, tope_cuerpos=TOPE_DEF, muestra=MUESTRA, reposicion='fija', r_rep=R_REP, eco=None):")
FIRMA_NUEVA = FIRMA_VIEJA[:-2] + ", familia=None):"
ANCLAS = [
    (FIRMA_VIEJA, FIRMA_NUEVA),
    ("    orden = list(range(len(cuerpos)))\n",
     "    orden = list(range(len(cuerpos)))\n"
     "    _fa = (Familia(seed, n, familia, E_, lin, cuerpos, L) if familia else None)\n"),
    ("                cuerpos[j] = F; b = F; c = cnew; l.vivos = 1; total += 1; id2lin[F.id] = i\n",
     "                cuerpos[j] = F; b = F; c = cnew; l.vivos = 1; total += 1; id2lin[F.id] = i\n"
     "                if _fa is not None: _fa.fundador(F)\n"),
    ("                elif total >= tope_cuerpos:\n                    b.gv = 0; l.bloq += 1\n                    if t_tope is None: t_tope = t\n                else:\n",
     "                elif total >= tope_cuerpos:\n                    b.gv = 0; l.bloq += 1\n                    if t_tope is None: t_tope = t\n"
     "                elif _fa is not None and _fa.sexo and (_par := _fa.pareja(b, cuerpos, l.nac + 1)) is None:   # D1: sin pareja no hay hijo\n"
     "                    b.gv = 0; _fa.sin_pareja[i] += 1\n"
     "                else:\n"),
    ("                    _dt = M['dote'] if b.g is None else float(b.g[I_DOTE])\n                    b.E -= _dt; b.Ag -= _dt\n",
     "                    _dt = M['dote'] if b.g is None else float(b.g[I_DOTE])\n"
     "                    if _fa is not None and _fa.dote_doble: _fa.paga(b, _par, _dt)   # D3: los dos pagan\n"
     "                    else: b.E -= _dt; b.Ag -= _dt\n"),
    ("                        _dg, _ds = b.g, b.s\n",
     "                        _dg, _ds = b.g, b.s\n"
     "                        if _fa is not None and _fa.recombina: _dg = _fa.recombina_g(b, _par, i, k)   # D1: mitad y mitad\n"),
    ("                    H = Cuerpo(i, k, b.gen + 1, b.k, t, ch, hid, vista, b.pos, _dt, 0, pc=b); H.g = _gh; H.s = _sh\n",
     "                    H = Cuerpo(i, k, b.gen + 1, b.k, t, ch, hid, vista, b.pos, _dt, 0, pc=b); H.g = _gh; H.s = _sh\n"
     "                    if _fa is not None: _fa.nace(H, b, (_par if _fa.sexo else None), i, k)\n"),
    ("            c.fin_paso(dict(t=t, olvido=olv))\n            if b.E <= 0 or b.Ag <= 0:\n",
     "            c.fin_paso(dict(t=t, olvido=olv))\n"
     "            if _fa is not None and _fa.camada: _fa.reduce(b, cuerpos)   # D4: reduccion de camada\n"
     "            if b.E <= 0 or b.Ag <= 0:\n"),
    ("                id2lin.pop(b.id, None); b.c = None; b.obs = None   # libera el cerebro del muerto\n",
     "                id2lin.pop(b.id, None); b.c = None; b.obs = None   # libera el cerebro del muerto\n"
     "                if _fa is not None: _fa.muere(b)\n"),
    ("        d['carro'] = car\n        out.append(d)\n",
     "        d['carro'] = car\n"
     "        if _fa is not None: d['_carrera']['familia'] = _fa.salida(i)\n"
     "        out.append(d)\n"),
    ("    return dict(linajes=out, pizarra_log=piz_log,\n", "    _ret = dict(linajes=out, pizarra_log=piz_log,\n"),
    ("                    gen_t=ES['gen_t'], vivos_final=[[b.lin, b.k, b.gen, b.tn] + [round(float(x), 6) for x in b.g] for b in cuerpos if b.vivo]))))\n",
     "                    gen_t=ES['gen_t'], vivos_final=[[b.lin, b.k, b.gen, b.tn] + [round(float(x), 6) for x in b.g] for b in cuerpos if b.vivo]))))\n"
     "    if _fa is not None: _ret['pista']['familia'] = _fa.info()\n"
     "    return _ret\n"),
]
_RUN = [None]


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def h16s(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


class Familia:
    """Las cuatro perillas del tramo D como FISICA del mundo (reglas locales; rng propios por hijo, etiquetas 20-22; el motor usa 11-19)."""

    def __init__(self, seed, n, cfg, E_, lin, cuerpos, L):
        mal = set(cfg) - set(FAM_DEF)
        if mal: raise SystemExit(f"MUNDO_FAMILIA: claves desconocidas {sorted(mal)}")
        c = dict(FAM_DEF); c.update(cfg)
        self.sexo = int(bool(c['sexo'])); self.recombina = int(bool(c['recombina'])); self.modo_pareja = c['pareja']; self.r_par = int(c['r_par'])
        self.dote_doble = int(bool(c['dote_doble'])); self.camada = int(bool(c['camada'])); self.u_cam = float(c['u_cam']); self.a_quien = c['a_quien']
        if self.modo_pareja not in ('azar', 'fuerte') or self.a_quien not in ('padre', 'hermano'): raise SystemExit("MUNDO_FAMILIA: pareja 'azar'|'fuerte'; a_quien 'padre'|'hermano'")
        if (self.recombina or self.dote_doble) and not self.sexo: raise SystemExit("MUNDO_FAMILIA: recombina y dote_doble exigen sexo 1")
        if self.recombina and E_ is None: raise SystemExit("MUNDO_FAMILIA: recombina exige eco=dict (genoma por cuerpo)")
        if self.r_par < 0 or not 0 <= self.u_cam <= 1.5: raise SystemExit("MUNDO_FAMILIA: r_par >= 0, u_cam en [0, 1.5]")
        self.seed = int(seed); self.n = n; self.lin = lin; self.L = int(L); self.cfg = c
        self.tipo = {}
        for b in cuerpos: self.tipo[b.id] = b.lin % 2
        z = lambda: [0] * n
        self.sin_pareja = z(); self.con_pareja = z(); self.recomb = z(); self.pagos = z(); self.trofico = z(); self.recibido = z()
        self.fuerza = [0.0] * n; self.candidatos = z(); self.tipos_nac = [[0, 0] for _ in range(n)]

    def _dist(self, a, b):
        d = (b - a) % self.L; return min(d, self.L - d)

    def fundador(self, F): self.tipo[F.id] = F.lin % 2

    def muere(self, b): self.tipo.pop(b.id, None)

    def pareja(self, b, cuerpos, k):
        """la pareja de b: viva, mismo carro (etiqueta), OTRO tipo, a <= r_par; 'fuerte' = mayor E + Ag; 'azar' = sorteo [seed, i, 21, k]."""
        et = self.lin[b.lin].etq; tb = self.tipo[b.id]
        cands = [x for x in cuerpos if x.vivo and x is not b and self.tipo.get(x.id) is not None and self.tipo[x.id] != tb
                 and self.lin[x.lin].etq == et and self._dist(x.pos, b.pos) <= self.r_par]
        self.candidatos[b.lin] += len(cands)
        if not cands: return None
        if self.modo_pareja == 'fuerte':
            p = cands[0]
            for x in cands[1:]:
                if x.E + x.Ag > p.E + p.Ag: p = x
        else:
            p = cands[int(np.random.default_rng([self.seed, b.lin, ETQ_PAREJA, int(k)]).integers(len(cands)))]
        self.con_pareja[b.lin] += 1; self.fuerza[b.lin] += float(p.E + p.Ag)
        return p

    def paga(self, b, par, dt):
        b.E -= dt / 2; b.Ag -= dt / 2; par.E -= dt / 2; par.Ag -= dt / 2; self.pagos[b.lin] += 1

    def recombina_g(self, b, par, i, k):
        r = np.random.default_rng([self.seed, int(i), ETQ_SEXO, int(k)])
        m = r.random(len(b.g)) < 0.5
        self.recomb[i] += 1
        return np.where(m, b.g, par.g)

    def nace(self, H, b, par, i, k):
        if par is None: t = b.lin % 2
        else: t = self.tipo[b.id] if np.random.default_rng([self.seed, int(i), ETQ_TIPO, int(k)]).random() < 0.5 else self.tipo[par.id]
        self.tipo[H.id] = t; self.tipos_nac[i][t] += 1

    def reduce(self, b, cuerpos):
        """D4: con necesidad y >= 2 hijos vivos cerca, el mas debil muere y su reserva pasa al padre (o al hermano mas fuerte)."""
        if not b.vivo or not (b.E < self.u_cam or b.Ag < self.u_cam): return
        hijos = [x for x in cuerpos if x.vivo and x.pc is b and x.E > 0 and x.Ag > 0 and self._dist(x.pos, b.pos) <= self.r_par]
        if len(hijos) < 2: return
        w = hijos[0]; f = hijos[0]
        for x in hijos[1:]:
            if x.E + x.Ag < w.E + w.Ag: w = x
            if x.E + x.Ag > f.E + f.Ag: f = x
        dest = b if self.a_quien == 'padre' else f
        dest.E = min(dest.E + w.E, 1.5); dest.Ag = min(dest.Ag + w.Ag, 1.5)
        w.E = 0.0; w.Ag = 0.0
        self.trofico[w.lin] += 1; self.recibido[dest.lin] += 1

    def salida(self, i):
        return dict(sin_pareja=self.sin_pareja[i], con_pareja=self.con_pareja[i], candidatos=self.candidatos[i], recombinaciones=self.recomb[i],
                    pagos_dobles=self.pagos[i], trofico=self.trofico[i], recibido=self.recibido[i], tipos_nacidos=list(self.tipos_nac[i]),
                    fuerza_pareja_media=(round(self.fuerza[i] / self.con_pareja[i], 4) if self.con_pareja[i] else None))

    def info(self):
        return dict(self.cfg, sin_pareja=sum(self.sin_pareja), con_pareja=sum(self.con_pareja), recombinaciones=sum(self.recomb), pagos_dobles=sum(self.pagos),
                    trofico=sum(self.trofico), tipos_vivos=[sum(1 for v in self.tipo.values() if v == 0), sum(1 for v in self.tipo.values() if v == 1)])


def construye():
    if _RUN[0] is not None: return _RUN[0]
    rp = os.path.join(ECO_D, 'motor_eco.py'); sp = h16(rp)
    if SHAS['motor_eco'] is not None and sp != SHAS['motor_eco']: raise SystemExit(f"MUNDO_FAMILIA: motor_eco.py sha {sp} != fijado {SHAS['motor_eco']}")
    if os.path.abspath(MEC.__file__) != os.path.abspath(rp): raise SystemExit(f"MUNDO_FAMILIA: 'motor_eco' importado de {MEC.__file__}")
    txt = open(rp, encoding='utf-8').read()
    a = txt.index("def run_solapadas(seed, carros,"); src = txt[a:]
    if not src.endswith("\n"): src += "\n"
    for viejo, nuevo in ANCLAS:
        k = src.count(viejo)
        if k != 1: raise SystemExit(f"MUNDO_FAMILIA: el ancla aparece {k} veces (debe ser 1): {viejo[:70]!r}")
        src = src.replace(viejo, nuevo)
    ns = dict(vars(MEC)); ns.update(Familia=Familia)
    exec(compile(src, '<mundo_familia.run desde motor_eco.py>', 'exec'), ns)
    _RUN[0] = (ns['run_solapadas'], dict(sha_motor_eco=sp, sha_fuente_transformada=h16s(src), anclas=len(ANCLAS)))
    return _RUN[0]


def run(*a, **k):
    return construye()[0](*a, **k)


if __name__ == '__main__':
    print(construye()[1])
