"""identidad_eco_rapido_fam.py — ARNES del GEMELO COMPILADO motor_eco_rapido_fam.py (FABRICA / FABRICA_ECO / FAMB_RES0_ECO).
Un proceso, sin Pool. Nube, 24-sep-2026 (compilador de gemelos).

MISION: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Un gemelo que no sea BIT A BIT identico SOLO EXPLORA, nunca confirma (regla 9 de registro/EQUIPO.md).

SEMILLAS: SOLO de practica, 19901-19909 y 10001-10011 (las de convive). Ninguna de las series ni de las baterias selladas.

QUE SE COMPARA (gemelo contra motor_eco.run_solapadas, el original en Python, en el mismo proceso):
  (0) ORIGEN: sha de motor_eco / FABRICA_ECO / FAMB_RES0_ECO / FABRICA / pista2 == los fijados en el gemelo; el carro de la familia
      en disco es el que construye construye_eco_familia.py.
  (P) PRIMITIVAS: bucle np.exp == np.exp; BLAS de numba == BLAS de NumPy; Generator; suma de 6; la FILA DE LA SORPRESA del nodo
      (.sum(1) de NumPy en (m, 6), m = 1..400) == de izquierda a derecha desde 0.0; top-3 con y sin empate. CONTROLES que deben
      fallar: libm != np.exp, suma ingenua != ddot, la fila sumada como 'primero + resto' != .sum(1).
  (N) NACIMIENTO AISLADO: crea(ctx) + nace(info) del carro FAMB_RES0_ECO (genoma y tabla al azar) == _crea + _nace + _nace_fam del
      gemelo (Wl, KW, activa, Wps, Wns, nodo, lecturas, lect_div, recibido y los DOS Generators); lo mismo con la variante SIN0 = 0
      (tablas de hasta 8 entradas: 400 filas). al_parir del carro == _tabla_padre del gemelo con mordidas y nodos al azar.
      CONTROLES: sin leer el nodo y con el empate al primero, distintos.
  (I) E1 eco=None con FAMB_RES0_ECO (y mezclas con FABRICA / FABRICA_ECO), varias configuraciones x varias semillas. En CADA
      corrida: salida COMPLETA (todas las claves, d['carro'] incluido), TRAYECTORIA (cada actua), PESOS y lo de la FAMILIA de cada
      cuerpo vivo al final (Wl ... zn, contadores, codigos, rechazo, SU Generator, el nodo, lo vivido por clave, la tabla que
      daria al_parir, lecturas, lect_div, _n10), CADA NACIMIENTO tras nace() (t, linaje, k, recibido, lecturas, lect_div, Wps y
      Wns tras la lectura del nodo) y el MUNDO final en orden.
  (M) muere() NO SE OBSERVA en la pista v2: el original con muere() anulado da la MISMA salida (por eso el gemelo no la compila).
  (E) E2 eco=dict con FAMB_RES0_ECO: los 4 brazos de corre_eco (VIDA, CEREBRO, AZAR, MUT0) en esc 30 y esc 90, refunda=0, genoma
      no entero, divisiones, NK 8 y 90, memoria_rechazo 5 y 80, tope, lectura extrema (eta_s, clip_s, aversion, lam), mezcla
      con FABRICA_ECO, banco < n. Lo mismo que (I) + las filas de ind_cb con su genoma.
  (C) CHECKPOINT: estado COMPLETO del original == del gemelo (cuerpos, cerebros, FAMILIA, genomas, sombras, mundo, rng, banco);
      cortado y reanudado == seguido; firmas ajenas (otra corrida, el original, el gemelo VIEJO) abortan.
  (X) EL MUNDO DE LA SERIE (esc 90, 90 FAMB_RES0_ECO, tope 3000, muestra 1000): VIDA, CEREBRO, AZAR, MUT0; salida completa.
  (J) corre_eco SIN cambiar su letra (CR.ME = el gemelo; MUNDO['carro'] = FAMB_RES0_ECO SOLO en este proceso): juez con G0 y con
      un banco real; trabajo() con checkpoint, cortado y reanudado; y el juez con FABRICA_ECO (regresion).
  (L) LARGO: pista v2 9 FAMB T 60 000 y eco VIDA esc 9 T 40 000: salida completa.
  (R) REGRESION FABRICA / FABRICA_ECO (lo que ya compilaba motor_eco_rapido.py): contra el original, y contra el gemelo VIEJO en
      corridas largas (T 100 000 y el mundo de la serie a 30 000).
  (K) CONTROLES que DEBEN fallar: semilla vecina; exp de libm; suma ingenua; turno fijo; FAMB contra FABRICA_ECO; VIDA contra MUT0;
      AZAR contra VIDA; inmediata contra fija. Y los tres de la familia, barridos sobre TODAS las corridas FAMB guardadas de (I),
      (E) y (L), con su prediccion exacta: sin SIN0 difiere en toda corrida con alguna tabla con entradas neutras; sin leer el
      nodo, en toda corrida con alguna tabla no vacia; con el empate al PRIMER indice, en toda corrida con alguna tabla de UNA
      entrada (lect_div). Donde la prediccion no obliga, se informa cuantas difieren (el empate entre filas copia de la misma
      entrada, o de necesidades distintas, no cambia la fisica: hallazgo de este arnes).
  (G) GUARDIAS del original (mismos mensajes) y del gemelo (lo que no compila aborta).
  (D) DETERMINISMO.  (Z) CACHE: un proceso NUEVO carga la cache (0 compilaciones) y reproduce 3 corridas del original.
  (V) ACELERACION (mismo mundo, mismo proceso; la maquina corre otros procesos: tiempos con carga).
Uso: /root/venv-juaco/bin/python experimentos/juaco_eco/identidad_eco_rapido_fam.py   (escribe identidad_eco_rapido_fam_salida.txt
     desde el arranque; la ultima linea es RESULTADO: N/N)
"""
import copy, importlib.util, json, os, pickle, shutil, subprocess, sys, tempfile, time
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')]
import motor_eco as ME
import pista2 as P
import motor_eco_rapido_fam as MF
import corre_eco as CR
import construye_eco_familia as CFAM

N = lambda x: json.dumps(x, default=str, sort_keys=True)
OK = [0, 0]
SAL = open(os.path.join(AQUI, 'identidad_eco_rapido_fam_salida.txt'), 'w', encoding='utf-8')
T00 = time.time()
PRACTICA = set(range(19901, 19910)) | set(range(10001, 10012))


def out(s=''):
    print(s, flush=True); SAL.write(s + '\n'); SAL.flush()


def di(et, ok, extra=''):
    OK[1] += 1; OK[0] += int(bool(ok))
    out(f"  [{'OK ' if ok else 'FALLA'}] ({OK[1]}) {et}{(' · ' + extra) if extra else ''}")


def seccion(s):
    out(f"{s}   [{time.strftime('%H:%M:%S')}, {round(time.time() - T00)} s]")


def aborta(f):
    try: f()
    except SystemExit as e: return 'SystemExit: ' + str(e)
    except ValueError as e: return 'ValueError: ' + str(e)
    return None


def sem(s):
    assert s in PRACTICA, f"semilla {s} fuera de la practica"
    return s


FAB = P.carga_carro('FABRICA'); FE = ME.carga_eco('FABRICA_ECO'); FM = ME.carga_eco('FAMB_RES0_ECO')
CF = P.cfg_fabrica(); G0 = ME.genoma0(CF); LO, HI = ME.rangos(G0); NLEE = int(CF['kw']['nodo_lee'])
HX = lambda a: np.ascontiguousarray(a).tobytes().hex()
EST = lambda r: r.bit_generator.state
LET = 'ABCD'
out(f"IDENTIDAD motor_eco_rapido_fam · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {np.__version__} · "
    f"numba {__import__('numba').__version__} · gemelo {MF._h16(MF.__file__)} · arnes {MF._h16(os.path.abspath(__file__))}")


# ================================================================ el carro ESPIA (misma conducta; registra instancias y actua)
class Registro:
    def __init__(self): self.REG = []; self.TRZ = []; self.NAC = []; self.MEM = []; self.vista = None


def espia(base, reg, muere_nulo=False):
    class Carro(base.Carro):
        def actua(self, obs):
            if reg.vista is None: reg.vista = obs['objs']
            a = base.Carro.actua(self, obs)
            reg.TRZ.append((obs['t'], self._lin_espia, obs['pos'], obs['E'], obs['Ag'], int(a['mov']), int(bool(a['muerde']))))
            return a

        def nace(self, info):
            base.Carro.nace(self, info)
            n10 = getattr(self, '_n10', None); mem = info.get('memoria') or []
            reg.NAC.append((info['t'], self._lin_espia, info['k'], (n10['recibido'] if n10 is not None else -1), int(self._nlec),
                            int(self._ldiv), HX(self.Wps), HX(self.Wns)))
            reg.MEM.append((len(mem), sum(1 for e in mem if float(e[1]) == 0.0), (n10['recibido'] // max(1, NLEE) if n10 is not None else -1)))

        if muere_nulo:
            def muere(self, info): return None

    class Mod:
        __file__ = base.__file__

        @staticmethod
        def crea(ctx):
            c = Carro(ctx); c._lin_espia = ctx['indice']; reg.REG.append((ctx['id'], ctx['indice'], c)); return c
    return Mod


def carros_espia(carros, reg, eco, muere_nulo=False):
    res = []
    for c in carros:
        e, m = (c, (P.carga_carro(c) if eco is None else ME.carga_eco(c))) if isinstance(c, str) else c
        res.append((e, espia(m, reg, muere_nulo)))
    return res


# ================================================================ cerebros y estados canonicos (con lo de la FAMILIA)
def fam_orig(c):
    md = {}
    for _t, k9, n9, R9 in c._mordh: md[(int(n9), LET.index(k9))] = float(R9)
    d = dict(md=[[n, k, R] for (n, k), R in sorted(md.items())], nodo=c._nodo, nlec=int(c._nlec), ldiv=int(c._ldiv))
    if hasattr(c, '_n10'):
        c2 = copy.copy(c); c2._n10 = copy.deepcopy(c._n10)
        d.update(n10=dict(recibido=c._n10['recibido'], partos=c._n10['partos'], dado=c._n10['dado'][:50]),
                 tabla=c2.al_parir(dict(t=-1, k=-1)))
    return d


def fam_gem(st, s):
    bi = st['bi'][s]; esfam = bool(st['LFAM'][int(bi[MF.I_LIN])])
    d = dict(md=[[n, k, R] for n, k, R in MF._tabla_py(st, s, 'md')], nodo=MF._nodo_py(st, s, NLEE),
             nlec=int(bi[MF.I_NLEC]), ldiv=int(bi[MF.I_LDIV]))
    if esfam:
        npa = int(bi[MF.I_NPART])
        d.update(n10=dict(recibido=int(bi[MF.I_RECIB]), partos=npa, dado=[int(x) for x in st['dado'][s, :min(npa, MF.DADO)]]),
                 tabla=MF._tabla_padre_py(st, s))
    return d


def cerebro_orig(c, t):
    return dict(Wl=HX(c.Wl), el=HX(c.el), tr=HX(c.tr), KW=HX(c.KW), activa=HX(c.activa), Wp=HX(c.Wp), Wn=HX(c.Wn),
                Wps=HX(c.Wps), Wns=HX(c.Wns), err=HX(c.err), mu=HX(c.mu), mup=HX(c.mup), mun=HX(c.mun), zp=HX(c.zp), zn=HX(c.zn),
                splits=c.splits, split_t=[list(x) for x in c.split_t], err_max=float(c.err_max), t_conflicto=c.t_conflicto,
                t_techo=c.t_techo, n_techo=c.n_techo, gpa=c._gpa, gpn=c._gpn, na=int(c._na), nm=int(c._nm), R=float(c._R),
                Rp=float(c._Rp), hambre=float(c._hambre), sin_objetivo=list(c.sin_objetivo),
                ncod=[[sorted(k), v] for k, v in c.ncod.items()], rech=sorted((x, v) for x, v in c._rech.items() if v >= t),
                rng=EST(c.rng), familia=fam_orig(c))


def cerebro_gem(st, s, t):
    bi = st['bi'][s]; bf = st['bf'][s]; b = MF.NKMAX + 1
    ncod = [[sorted([int(k) // (b * b) - 1, (int(k) // b) % b - 1, int(k) % b - 1]), int(v)]
            for k, v in zip(st['nck'][s][:bi[MF.I_NCN]], st['ncc'][s][:bi[MF.I_NCN]])]
    return dict(Wl=HX(st['Wl'][s]), el=HX(st['el'][s]), tr=HX(st['tr'][s]), KW=HX(st['KW'][s]), activa=HX(st['act'][s]),
                Wp=HX(st['Wp'][s]), Wn=HX(st['Wn'][s]), Wps=HX(st['Wps'][s]), Wns=HX(st['Wns'][s]), err=HX(st['err'][s]),
                mu=HX(st['mu'][s]), mup=HX(st['mup'][s]), mun=HX(st['mun'][s]), zp=HX(st['zp'][s]), zn=HX(st['zn'][s]),
                splits=int(bi[MF.I_SPL]), split_t=[[int(st['stt'][s][i]), P.TIPOS[int(st['stk'][s][i])]] for i in range(bi[MF.I_NST])],
                err_max=float(bf[MF.F_ERRMAX]), t_conflicto=(None if bi[MF.I_TCON] < 0 else int(bi[MF.I_TCON])),
                t_techo=(None if bi[MF.I_TTEC] < 0 else int(bi[MF.I_TTEC])), n_techo=int(bi[MF.I_NTEC]), gpa=int(bi[MF.I_GPA]),
                gpn=int(bi[MF.I_GPN]), na=int(bi[MF.I_NA]), nm=int(bi[MF.I_NM]), R=float(bf[MF.F_R]), Rp=float(bf[MF.F_RP]),
                hambre=float(bf[MF.F_HAMB]), sin_objetivo=[int(bi[MF.I_SO0 + q]) for q in range(4)], ncod=ncod,
                rech=sorted((int(x), int(v)) for x, v in zip(st['rpos'][s][:bi[MF.I_RN]], st['rexp'][s][:bi[MF.I_RN]]) if v >= t),
                rng=EST(st['GL'][int(s)]), familia=fam_gem(st, s))


def mundo_gem(st):
    wi = st['wi']
    return [(int(st['seqpos'][q]), P.TIPOS[int(st['grid'][st['seqpos'][q]])]) for q in range(int(wi[MF.W_NSEQ])) if st['seqpos'][q] >= 0]


def es_canon(ES):
    d = {k: v for k, v in ES.items() if k != 'banco'}
    d['banco'] = [[HX(g), HX(s)] for g, s in ES['banco']]
    return d


def canon_orig(blob):
    st = pickle.loads(blob); t = st['t']
    cs = []
    for b in st['cuerpos']:
        cs.append(dict(lin=b.lin, k=b.k, gen=b.gen, padre=b.padre, tn=b.tn, pos=b.pos, E=float(b.E), Ag=float(b.Ag), gv=b.gv,
                       tB=b.tB, tD=b.tD, vol={None: -1, 'B': 1, 'D': 3}[b.vol_kk], hijos=b.hijos, fund=b.fund,
                       g=HX(b.g), s=HX(b.s), cerebro=cerebro_orig(b.c, t)))
    lin = [dict(mord=l.mord, vis=l.vis, deaths=l.deaths, mnec=l.mnec, causas=l.causas, mvol=l.muertes_vol, fund=l.fund,
                tfund=l.tfund, desc=l.desc, nac=l.nac, bloq=l.bloq, vidas=l.vidas, ind=l.ind, vivos=l.vivos, tam=l.tam, pv=l.pv)
           for l in st['lin']]
    return dict(t=t, cuerpos=cs, mundo=list(st['objs'].items()), rng=EST(st['rng']), pista=EST(st['rng_pista']),
                fund=[EST(r) for r in st['rngs_fund']], muerte=[EST(r) for r in st['rngs_muerte']], quimio=st['banco'][0],
                pisos=st['pisos'][0], llegadas=st['llegadas'][0], perdidas=st['perdidas'][0], olv=st['olv_n'], comp=st['comp'],
                nsuma=st['nobj_suma'], total=st['total'], maxv=st['max_vivos'], ttope=st['t_tope'], tamtot=st['tam_total'],
                lin=lin, ES=es_canon(st['ES']))


def canon_gem(blob, muestra):
    B = pickle.loads(blob); st = B['st']; t = B['t']; wi = st['wi']; li = st['li']
    nsamp = (t - 1) // muestra + 1
    cs = []
    for s in [int(x) for x in st['cuer'][:wi[MF.W_NCUER]]]:
        bi = st['bi'][s]; bf = st['bf'][s]
        cs.append(dict(lin=int(bi[MF.I_LIN]), k=int(bi[MF.I_K]), gen=int(bi[MF.I_GEN]), padre=int(bi[MF.I_PADRE]),
                       tn=int(bi[MF.I_TN]), pos=int(bi[MF.I_POS]), E=float(bf[MF.F_E]), Ag=float(bf[MF.F_AG]), gv=int(bi[MF.I_GV]),
                       tB=int(bi[MF.I_TB]), tD=int(bi[MF.I_TD]), vol=int(bi[MF.I_VOL]), hijos=int(bi[MF.I_HIJ]),
                       fund=int(bi[MF.I_FUND]), g=HX(st['G'][s]), s=HX(st['SH'][s]), cerebro=cerebro_gem(st, s, t)))
    lin = []
    for i in range(li.shape[0]):
        lv = li[i]
        lin.append(dict(mord={x: [int(v) for v in st['mord'][i, j]] for j, x in enumerate(P.TIPOS)},
                        vis={x: [int(v) for v in st['vis'][i, j]] for j, x in enumerate(P.TIPOS)},
                        deaths=int(lv[MF.L_DEATHS]), mnec=[int(lv[MF.L_MN0]), int(lv[MF.L_MN1])],
                        causas={x: int(lv[MF.L_CZ0 + j]) for j, x in enumerate(ME.CAUSAS)}, mvol=int(lv[MF.L_MVOL]),
                        fund=int(lv[MF.L_FUND]), tfund=[int(x) for x in st['tfund'][i, :lv[MF.L_NTF]]], desc=int(lv[MF.L_DESC]),
                        nac=int(lv[MF.L_NAC]), bloq=int(lv[MF.L_BLOQ]), vidas=B['lin_py'][i]['vidas'], ind=B['lin_py'][i]['ind'],
                        vivos=int(lv[MF.L_VIVOS]), tam=[int(x) for x in st['tam'][:nsamp, i]], pv=int(lv[MF.L_PV])))
    return dict(t=t, cuerpos=cs, mundo=mundo_gem(st), rng=EST(st['rng']), pista=EST(st['rng_pista']),
                fund=[EST(r) for r in st['FUND']], muerte=[EST(r) for r in st['MUE']], quimio=float(st['wf'][0]),
                pisos=int(wi[MF.W_PISOS]), llegadas=int(wi[MF.W_LLEG]), perdidas=int(wi[MF.W_PERD]), olv=int(wi[MF.W_OLV]),
                comp={x: int(wi[MF.W_COMP0 + j]) for j, x in enumerate(P.TIPOS)}, nsuma=int(wi[MF.W_NSUMA]),
                total=int(wi[MF.W_TOTAL]), maxv=int(wi[MF.W_MAXV]), ttope=(None if wi[MF.W_TTOPE] < 0 else int(wi[MF.W_TTOPE])),
                tamtot=[int(x) for x in st['tamtot'][:nsamp]], lin=lin, ES=es_canon(B['ES']))


def claves_distintas(a, b):
    d = [k for k in sorted(set(a) | set(b)) if k not in ('linajes', 'pista', 'eco') and N(a.get(k)) != N(b.get(k))]
    d += ['pista.' + k for k in sorted(set(a['pista']) | set(b['pista'])) if N(a['pista'].get(k)) != N(b['pista'].get(k))]
    for i, (la, lb) in enumerate(zip(a['linajes'], b['linajes'])):
        d += [f'lin{i}.{k}' for k in sorted(set(la) | set(lb)) if N(la.get(k)) != N(lb.get(k))]
    if 'eco' in a or 'eco' in b:
        ea, eb = a.get('eco', {}), b.get('eco', {})
        d += ['eco.' + k for k in sorted(set(ea) | set(eb)) if N(ea.get(k)) != N(eb.get(k))]
    return d


def compara(seed, carros, kw, eco=None, modo=None, filas=True):
    """UNA corrida: original (con el carro espia) contra gemelo (con el carro real). Salida, filas ind_cb, trayectoria,
    cerebros + familia de los vivos al final y mundo final. Devuelve (dict de igualdades, info, salida original, tiempos)."""
    reg = Registro(); fo, fg = [], []
    eo = eg = None
    if eco is not None:
        eo = dict(eco); eg = dict(eco)
        if filas:
            eo['ind_cb'] = lambda li, row, g: fo.append((li, list(row), HX(g)))
            eg['ind_cb'] = lambda li, row, g: fg.append((li, list(row), HX(g)))
    t0 = time.time(); a = ME.run_solapadas(sem(seed), carros_espia(carros, reg, eco), eco=eo, **kw); ta = time.time() - t0
    trz = []; fin = {}; trn = []
    t0 = time.time(); b = MF.run_solapadas(seed, carros, eco=eg, _traza=trz, _modo=modo, _estado_final=fin, _traza_nac=trn, **kw); tb = time.time() - t0
    st = fin['st']; tfin = fin['t']
    dif = claves_distintas(a, b)
    ids = a['pista']['ids']; porid = {}
    for ident, i, c in reg.REG: porid[(i, ident)] = c
    malos = []; nviv = 0
    for s in fin['vivos']:
        i = int(st['bi'][s, MF.I_LIN]); k = int(st['bi'][s, MF.I_K]); fu = int(st['bi'][s, MF.I_FUND])
        c = porid.get((i, ids[i] if fu else f"{ids[i]}/{k}"))
        nviv += 1
        if c is None or N(cerebro_orig(c, tfin)) != N(cerebro_gem(st, s, tfin)): malos.append((i, k))
    res = dict(salida=not dif, filas=(N(fo) == N(fg)), traza=(N(reg.TRZ) == N(trz)), cerebros=not malos,
               mundo=(N(list(reg.vista.items())) == N(mundo_gem(st))), nacimientos=(N(reg.NAC) == N(trn)))
    # la familia en el original: tablas instaladas (hijos con _n10) por tamano (tras SIN0), generacion maxima
    tam = {}
    for _, _, c in reg.REG:
        if hasattr(c, '_n10') and c._n10['recibido'] >= 0:
            m = c._n10['recibido'] // max(1, NLEE); tam[m] = tam.get(m, 0) + 1
    filas_ = [r for l in a['linajes'] for r in l['individuos']] + [(r[1]) for r in fo]
    info = dict(dif=dif[:5], malos=malos[:4], nviv=nviv, ntraza=len(trz), ties=int(st['wi'][MF.W_NTIES]),
                mv=a['pista']['max_vivos'], muertes=sum(l['deaths'] for l in a['linajes']),
                nac=sum(l['descendientes'] for l in a['linajes']), pisos=a['pista']['pisos'], bloq=a['pista']['bloqueados'],
                splits=sum(c.splits for _, _, c in reg.REG), filas=len(fo), tablas=dict(sorted(tam.items())),
                gmax=max([int(r[1]) for r in filas_], default=0), nnac=len(trn),
                neutras=sum(1 for m_, n0_, i_ in reg.MEM if n0_ > 0), no_vacias=sum(1 for m_, n0_, i_ in reg.MEM if i_ > 0),
                una=sum(1 for m_, n0_, i_ in reg.MEM if i_ == 1))
    if modo is None and (any(isinstance(c_, tuple) and os.path.basename(c_[1].__file__) == MF.FAMILIA for c_ in carros) or
                         any(isinstance(c_, str) and c_ == 'FAMB_RES0_ECO' for c_ in carros)):
        GUARDA.append(dict(seed=seed, carros=carros, kw=kw, eco=eco, filas=(eco is not None and filas), a=N(a), fo=N(fo), nac=N(reg.NAC),
                           neutras=info['neutras'], no_vacias=info['no_vacias'], una=info['una'], modo=modo))
    return res, info, a, (ta, tb)


GUARDA = []   # corridas FAMB del original (salida, filas y nacimientos) para barrer los controles de la familia en (K)


def reporta(et, res, info, tt, eco=False):
    ok = all(res.values())
    ext = (f"salida {'=' if res['salida'] else '!='} · traza {info['ntraza']} {'=' if res['traza'] else '!='} · "
           f"nacimientos {info['nnac']} {'=' if res['nacimientos'] else '!='} · "
           f"cerebros+familia {info['nviv']} vivos {'=' if res['cerebros'] else '!='} · mundo {'=' if res['mundo'] else '!='}"
           + (f" · filas {info['filas']} {'=' if res['filas'] else '!='}" if eco else '')
           + f" · max_vivos {info['mv']} muertes {info['muertes']} partos {info['nac']} gen_max {info['gmax']} divisiones {info['splits']}"
           + (f" · tablas por tamano {info['tablas']}" if info['tablas'] else '')
           + (f" pisos {info['pisos']}" if info['pisos'] else '') + (f" bloqueados {info['bloq']}" if info['bloq'] else '')
           + (f" empates_top3 {info['ties']}" if info['ties'] else '')
           + f" · {tt[0]:.1f} s / {tt[1]:.2f} s" + ('' if ok else f" · DIFIERE {res} {info['dif']} {info['malos']}"))
    di(et, ok, ext)


# ================================================================================================ (0)
seccion('(0) ORIGEN (sha fijados en el gemelo)')
for p, h in MF.SHA.items():
    di(f"{os.path.relpath(p, RAIZ)} sha {h}", MF._h16(p) == h)
di("el carro FAMB_RES0_ECO en disco es el que construye construye_eco_familia.py (SIN0 = 1)",
   open(CFAM.DESTINO, encoding='utf-8').read() == CFAM.texto(1) and FM.MODO == 'res' and FM.SIN0 == 1)

# ================================================================================================ (P)
seccion('(P) PRIMITIVAS delegadas a NumPy (y tres controles que deben fallar)')
rng = np.random.default_rng(19901)
xs = np.concatenate([rng.uniform(-40, 40, 250000), rng.normal(0, 2, 250000)])
ref = np.exp(xs); B = MF._bufs_exp(); got = np.empty_like(xs)
for i in range(xs.size):
    got[i] = MF._exp1(xs[i], MF.EXP_LOOP, B[0], B[1], B[3], B[5], 0)
di("exp del gemelo (bucle 1-D de np.exp por ctypes) == np.exp, 500 000 argumentos", np.array_equal(ref.view(np.int64), got.view(np.int64)))
libm = np.array([MF._exp1(x, MF.EXP_LOOP, B[0], B[1], B[3], B[5], 1) for x in xs[:200000]])
nd = int((libm.view(np.int64) != ref[:200000].view(np.int64)).sum())
di("CONTROL (debe fallar): exp de libm != np.exp en esta maquina", nd > 0, f"distintos {nd}/200000 ({100 * nd / 200000:.2f} %)")
malos = 0; nd_ing = 0
for rep in range(100000):
    a = rng.normal(0, 1, 90); b = rng.normal(0, 1, 90)
    if float(a @ b) != MF._dot(a, b, 90, 0): malos += 1
    if float(a @ b) != MF._dot(a, b, 90, 1): nd_ing += 1
    k3 = np.zeros(90); k3[rng.choice(90, 3, replace=False)] = 1.0
    if float(a @ k3) != MF._dot(a, k3, 90, 0): malos += 1
    c6 = rng.uniform(-10, 10, 6); d6 = np.array(CF['PAT'][LET[rep % 4]], float)
    if float(c6 @ d6) != MF._dot(c6, d6, 6, 0): malos += 1
di("BLAS de numba == BLAS de NumPy (ddot 90 denso, ddot 90 con 3 unos, ddot 6 con un patron), 300 000 casos", malos == 0, f"distintos {malos}")
di("CONTROL (debe fallar): suma de izquierda a derecha != ddot de BLAS (90 denso)", nd_ing > 0, f"distintos {nd_ing}/100000")


def mv(A, x): return A @ x


from numba import njit
mv_nb = njit(mv)
malos = 0
for rep in range(30000):
    A = rng.uniform(0, 1, (90, 6)); x = rng.uniform(0, 1, 6)
    if not np.array_equal(A @ x, mv_nb(A, x)): malos += 1
    A2 = rng.uniform(0, 1.5, (2, 9)); x2 = rng.uniform(0, 1.5, 9)
    if not np.array_equal(A2 @ x2, mv_nb(A2, x2)): malos += 1
di("BLAS de numba == BLAS de NumPy (dgemv 90x6 @ 6 y 2x9 @ 9), 60 000 casos", malos == 0, f"distintos {malos}")


@njit
def _gen_nb(r, n, L, k, sig):
    acc = []
    for i in range(n):
        p = r.permutation(k + (i % 7)); acc.append(float(p.sum()) + p[0] * 1000.0)
        acc.append(float(r.integers(0, L))); acc.append(float(r.integers(0, 4))); acc.append(r.random())
        z = r.normal(0, .3, 2); acc.append(z[0]); acc.append(z[1])
        u = r.uniform(.1, .4, (2, 9)); acc.append(u[1, 8]); v = r.uniform(0, 1, (7, 6)); acc.append(v[6, 5])
    return acc


def _gen_py(r, n, L, k, sig):
    acc = []
    for i in range(n):
        p = r.permutation(k + (i % 7)); acc.append(float(p.sum()) + p[0] * 1000.0)
        acc.append(float(int(r.integers(L)))); acc.append(float(int(r.integers(4)))); acc.append(r.random())
        z = r.normal(0, .3, 2); acc.append(z[0]); acc.append(z[1])
        u = r.uniform(.1, .4, (2, 9)); acc.append(u[1, 8]); v = r.uniform(0, 1, (7, 6)); acc.append(v[6, 5])
    return acc


malos = 0
for s in range(10):
    for L in (40, 360, 1200, 3600):
        a1 = np.random.default_rng([19902, s, 11, 0]); a2 = np.random.default_rng([19902, s, 11, 0])
        if _gen_nb(a1, 200, L, 2 + s, 0.15) != _gen_py(a2, 200, L, 2 + s, 0.15) or EST(a1) != EST(a2): malos += 1
di("Generator en numba (permutation, integers, random, normal, uniform) == NumPy: flujo y estado final, 40 flujos", malos == 0, f"distintos {malos}")
M6 = rng.uniform(0, 1, (100000, 6)) * rng.uniform(0.001, 1, (100000, 1)); malos = 0
for r6 in M6:
    acc = 0.0
    for v in r6: acc += v
    malos += int(acc != r6.sum())
di("suma de 6 (mu[c].sum()) de izquierda a derecha desde 0.0 == NumPy, 100 000 filas", malos == 0, f"distintos {malos}")


@njit
def _fila_l2r(W, n, P6):   # la fila de la sorpresa, como _nace_fam
    acc = 0.0
    for q in range(6): acc += (W[0, n, q] - W[1, n, q]) * P6[q]
    return acc


@njit
def _fila_1r(W, n, P6):    # CONTROL: 'primero + resto' (lo que haria copiar el primer elemento y sumar el resto)
    acc = 0.0
    for q in range(1, 6): acc += (W[0, n, q] - W[1, n, q]) * P6[q]
    return (W[0, n, 0] - W[1, n, 0]) * P6[0] + acc


PATM = np.array([CF['PAT'][x] for x in P.TIPOS], float)
malos = 0; nd1 = 0; tot = 0
for rep in range(6000):
    Wps = rng.uniform(0, 10, (2, 6)) * (rng.random((2, 6)) < .7); Wns = rng.uniform(0, 10, (2, 6)) * (rng.random((2, 6)) < .7)
    m = int(rng.integers(1, 401)); Nn = rng.integers(0, 2, m); Kk = rng.integers(0, 4, m); Pm = PATM[Kk]
    sref = ((Wps[Nn] - Wns[Nn]) * Pm).sum(1); W2 = np.stack([Wps, Wns])
    for i in range(0, m, max(1, m // 25)):
        tot += 1
        malos += int(_fila_l2r(W2, Nn[i], PATM[Kk[i]]) != sref[i]); nd1 += int(_fila_1r(W2, Nn[i], PATM[Kk[i]]) != sref[i])
di(f"fila de la sorpresa del nodo: ((Wps[N] - Wns[N]) * P).sum(1) de NumPy en (m, 6), m = 1..400 == de izquierda a derecha desde 0.0, {tot} filas",
   malos == 0, f"distintos {malos}")
di("CONTROL (debe fallar): la fila sumada como 'primero + resto' != .sum(1) de NumPy", nd1 > 0, f"distintos {nd1}/{tot}")
KWt = np.zeros((1, MF.NKMAX, 6)); act = np.zeros((1, MF.NKMAX), np.bool_); cc = np.zeros((1, 4, 3), np.int64)
cv = np.zeros((1, 4), np.bool_); wb = np.zeros(MF.NKMAX); wit = np.zeros(MF.NWI, np.int64)
malos = 0; nemp = 0
for rep in range(20000):
    nk = int(rng.integers(8, 91)); KWt[:] = 0; act[:] = False
    KWt[0, :nk] = rng.uniform(0, 1, (nk, 6)); act[0, :nk] = True
    if rep % 2:
        src = rng.integers(0, nk, 4); dst = rng.integers(0, nk, 4); KWt[0, dst] = KWt[0, src]
        if rep % 4 == 1: KWt[0, :nk] = np.round(KWt[0, :nk], 1)
    p = int(rng.integers(0, 4)); cv[:] = False; e0 = int(wit[MF.W_NTIES])
    MF._code3(0, p, KWt, act, PATM, cc, cv, wb, 0, wit)
    v = np.where(act[0], KWt[0] @ PATM[p], -1e9)
    if sorted(cc[0, p]) != sorted(int(z) for z in np.argsort(v)[-3:]): malos += 1
    nemp += int(wit[MF.W_NTIES]) - e0
di("codigo de Kenyon: top-3 del gemelo == set(np.argsort(...)[-3:]) del original, 20 000 casos", malos == 0 and nemp > 100,
   f"distintos {malos}; con empate en la frontera (a NumPy por objmode) {nemp}")

# ================================================================================================ (N)
seccion('(N) NACIMIENTO AISLADO y al_parir: carro FAMB_RES0_ECO (crea + nace) contra _crea + _nace + _nace_fam del gemelo')
tmpv = tempfile.mkdtemp(prefix='famb_sin0_0_')
p0 = os.path.join(tmpv, 'FAMB_RES0_ECO.py'); open(p0, 'w', encoding='utf-8').write(CFAM.texto(0))   # la variante SIN0 = 0 (mismo nombre)
_sp = importlib.util.spec_from_file_location('famb_sin0_0', p0); F0 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(F0)
RVd = {(n, k): (1.0 if v > 0 else (-3.0 if v < 0 else 0.0)) for k in range(4) for n, v in enumerate(CF['EFECTO'][CF['VAL_VIVO'][LET[k]]])}
rgn = np.random.default_rng([19903, 1])


def ctx_n(g, r):
    d = dict(id='x', indice=0, n_linajes=1, T=1000, L=40, PAT={k: v.copy() for k, v in CF['PAT'].items()}, rng=r, dote=0.6,
             rep_umbral=1.0, costo=0.001, costo_a=0.001, rep_X=500, cupo=P.CUPO, ancho=P.ANCHO, fabrica=P.cfg_fabrica())
    return ME.ctx_genoma(d, g)


def genoma_azar(rep):
    if rep % 5 == 0: return G0.copy()
    g = np.array([rgn.uniform(LO[j], HI[j]) for j in range(len(G0))])
    for j, gg in enumerate(ME.GENES):
        if gg[2] and rep % 2: g[j] = float(round(g[j]))   # enteros redondos o no (ctx_genoma redondea)
    for nom in ('lam', 'eta_s', 'clip_s', 'aversion'):   # a veces en los extremos del rango
        j = ME.NOMBRES.index(nom); u = rgn.random()
        if u < 0.15: g[j] = LO[j]
        elif u < 0.3: g[j] = HI[j]
    return g


def nace_uno(mod, sin0, rep, nodo=0):
    g = genoma_azar(rep)
    sub = [(n, k) for n in range(2) for k in range(4) if rgn.random() < 0.6]
    tabla = [(n, k, (RVd[(n, k)] if rep % 2 else float(rgn.choice([1.0, 0.0, -3.0])))) for n, k in sub]
    mem = [[[float(z) for z in CF['PAT'][LET[k]]], R, n] for n, k, R in tabla]
    s1, s2 = [19903, rep, 1], [19903, rep, 2]
    c = mod.crea(ctx_n(g, np.random.default_rng(s1))); rh = np.random.default_rng(s2)
    c.nace(dict(t=0, k=1, fundador=False, memoria=mem, rng_hijo=rh, padre='x'))
    r1 = np.random.default_rng(s1); r2 = np.random.default_rng(s2)
    st = MF._nace_aislado(g, r1, r2, tabla, sin0=sin0, nodo=nodo)
    a = dict(Wl=HX(c.Wl), KW=HX(c.KW), act=HX(c.activa), Wps=HX(c.Wps), Wns=HX(c.Wns), nlec=c._nlec, ldiv=c._ldiv,
             rec=c._n10['recibido'], nodo=N(c._nodo), r1=EST(c.rng), r2=EST(rh), Wp=HX(c.Wp), Wn=HX(c.Wn))
    b = dict(Wl=HX(st['Wl'][0]), KW=HX(st['KW'][0]), act=HX(st['act'][0]), Wps=HX(st['Wps'][0]), Wns=HX(st['Wns'][0]),
             nlec=int(st['bi'][0, MF.I_NLEC]), ldiv=int(st['bi'][0, MF.I_LDIV]), rec=int(st['bi'][0, MF.I_RECIB]),
             nodo=N(MF._nodo_py(st, 0, NLEE)), r1=EST(r1), r2=EST(r2), Wp=HX(st['Wp'][0]), Wn=HX(st['Wn'][0]))
    return [k for k in a if a[k] != b[k]], len(tabla), sum(1 for _n, _k, R in tabla if R != 0.0)


for mod, s0, nn, et in ((FM, 1, 2500, 'SIN0 = 1 (el carro)'), (F0, 0, 1000, 'SIN0 = 0 (variante construida, tablas de hasta 8 entradas)')):
    malos = 0; tams = {}
    for rep in range(nn):
        d, m, m0 = nace_uno(mod, s0, rep); k_ = m if not s0 else m0; tams[k_] = tams.get(k_, 0) + 1
        malos += int(bool(d))
    di(f"nace del carro {et} == gemelo (Wl, KW, activa, Wp, Wn, Wps, Wns, nodo, lecturas, lect_div, recibido y los dos Generators), {nn} "
       "genomas y tablas al azar", malos == 0, f"distintos {malos}; entradas leidas por caso {dict(sorted(tams.items()))}")
for nodo, et in ((1, 'sin leer el nodo'), (2, 'empate al PRIMER indice')):
    malos = 0
    for rep in range(500): malos += int(bool(nace_uno(FM, 1, 10000 + rep, nodo=nodo)[0]))
    di(f"CONTROL (debe fallar): gemelo {et} != carro", malos > 0, f"distintos {malos}/500")
# al_parir: mordidas y nodos al azar
malos = 0
for rep in range(3000):
    c = FM.crea(ctx_n(G0, np.random.default_rng([19904, rep])))
    st = MF._cuerpos_vacios(1, len(ME.GENES), 0); st['PATM'] = PATM
    tb = [(n, k, float(rgn.choice([1.0, -3.0, 0.0]))) for n in range(2) for k in range(4) if rgn.random() < 0.4]
    c._nodo = [[[float(z) for z in CF['PAT'][LET[k]]], R, n] for n, k, R in tb] * NLEE
    for n, k, R in tb: st['tbH'][0, n, k] = True; st['tbR'][0, n, k] = R
    c._mordh = []
    for q in range(int(rgn.integers(0, 12))):
        n = int(rgn.integers(0, 2)); k = int(rgn.integers(0, 4)); R = (RVd[(n, k)] if rep % 2 else float(rgn.choice([1.0, -3.0, 0.0])))
        c._mordh.append([q, LET[k], n, R]); st['mdH'][0, n, k] = True; st['mdR'][0, n, k] = R
    malos += int(N(c.al_parir(dict(t=0, k=1))) != N(MF._tabla_padre_py(st, 0)))
di("al_parir del carro (nodo + mordidas al azar) == _tabla_padre del gemelo (entradas, R, orden), 3000 casos", malos == 0, f"distintos {malos}")
shutil.rmtree(tmpv)

# ================================================================================================ (I)
seccion('(I) E1: eco=None con FAMB_RES0_ECO: salida + trayectoria + pesos + familia + mundo')
FT = ('FAMB_RES0_ECO', FM)
CASOS_I = [('9 FAMB fija T=5000', s, [FT] * 9, dict(T=5000)) for s in (10001, 10002, 10003, 19901, 19902)]
CASOS_I += [
    ('9 FAMB inmediata T=3000', 10004, [FT] * 9, dict(T=3000, reposicion='inmediata')),
    ('9 FAMB mundo_n=5 (esc < n)', 10005, [FT] * 9, dict(T=3000, mundo_n=5)),
    ('3 FAMB mundo_n=9 (esc > n)', 10006, [FT] * 3, dict(T=6000, mundo_n=9)),
    ('9 FAMB rep_acum=1', 10007, [FT] * 9, dict(T=4000, rep_acum=1)),
    ('9 FAMB tope 12 (bloqueados)', 10008, [FT] * 9, dict(T=4000, tope_cuerpos=12)),
    ('9 FAMB muestra 37', 10009, [FT] * 9, dict(T=3000, muestra=37)),
    ('9 FAMB r_rep 0.002 (pisos)', 10010, [FT] * 9, dict(T=3000, r_rep=0.002)),
    ('1 FAMB (n = 1: turno sin permutacion)', 10011, [FT], dict(T=10000)),
    ('3 FAMB escala=0 (L = 40)', 19903, [FT] * 3, dict(T=5000, escala=0)),
    ('mezcla 3 FAMB + 3 FABRICA_ECO + 3 FABRICA', 19904, [FT] * 3 + [('FABRICA_ECO', FE)] * 3 + ['FABRICA'] * 3, dict(T=5000)),
    ('etiqueta O3 con cerebro FAMB (VOL_DECL) y etiqueta FAMB_RES', 19905, [('O3', FM)] * 2 + [('FAMB_RES', FM)] * 2, dict(T=5000)),
    ('9 FAMB T=20000 (generaciones: la tabla viaja)', 19906, [FT] * 9, dict(T=20000)),
    ('9 FAMB pizarra=0', 19907, [FT] * 9, dict(T=3000, pizarra=0)),
]
SALIDAS = {}
for et, s, car, kw in CASOS_I:
    res, info, a, tt = compara(s, car, dict(kw, diag=0))
    reporta(f"{et} s{s}", res, info, tt)
    SALIDAS[(et, s)] = a
reg = Registro()
a0 = ME.run_solapadas(10001, [FT] * 9, T=5000, diag=0)
a1 = ME.run_solapadas(10001, carros_espia([FT] * 9, reg, None), T=5000, diag=0)
di("el carro espia es INERTE (original con espia == original sin espia)", N(a0) == N(a1))

# ================================================================================================ (M)
seccion('(M) muere() NO SE OBSERVA en la pista v2 (por eso el gemelo no la compila)')
reg = Registro()
am = ME.run_solapadas(10001, carros_espia([FT] * 9, reg, None, muere_nulo=True), T=5000, diag=0)
di("eco=None, 9 FAMB T=5000: el original con muere() ANULADO da la misma salida que el original", N(am) == N(a0),
   f"muertes {sum(l['deaths'] for l in a0['linajes'])}")
eM = CR.eco_cfg('VIDA', 2000)
a2 = ME.run_solapadas(19908, ['FAMB_RES0_ECO'] * 30, T=4000, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=500, eco=eM)
a3 = ME.run_solapadas(19908, carros_espia(['FAMB_RES0_ECO'] * 30, Registro(), eM, muere_nulo=True), T=4000, diag=0, mundo_n=30,
                      tope_cuerpos=3000, muestra=500, eco=eM)
di("eco VIDA esc 30, T=4000: el original con muere() ANULADO da la misma salida", N(a2) == N(a3),
   f"muertes {sum(l['deaths'] for l in a2['linajes'])}, nacidos {a2['eco']['n_nac']}")

# ================================================================================================ (E)
seccion('(E) E2: eco=dict con FAMB_RES0_ECO: brazos, genoma, mutacion, sombras, banco, vivero, corte, refunda, ind_cb')


def GEN(**kw):
    g = G0.copy()
    for k, v in kw.items(): g[ME.NOMBRES.index(k)] = v
    assert ((g >= LO - 1e-12) & (g <= HI + 1e-12)).all(), kw
    return list(g)


rg = np.random.default_rng([19909, 77])
GX = np.array([rg.uniform(LO[j], HI[j]) for j in range(len(G0))])   # genoma explicito NO entero
GXF = GX.copy()   # NO entero y FERTIL: historia de vida de fabrica, cerebro al azar (NK y memoria_rechazo con decimales)
for _nom in ('dote', 'rep_umbral', 'rep_X', 'hambre_boca', 'alpha'): GXF[ME.NOMBRES.index(_nom)] = G0[ME.NOMBRES.index(_nom)]
GXL = []   # UN genoma distinto por linaje (9), NO enteros, fertiles
for _i in range(9):
    _g = np.array([rg.uniform(max(LO[j], G0[j] / 2), min(HI[j], G0[j] * 2)) for j in range(len(G0))])
    for _nom in ('dote', 'rep_umbral', 'rep_X'): _g[ME.NOMBRES.index(_nom)] = G0[ME.NOMBRES.index(_nom)]
    GXL.append(list(_g))
K30 = dict(T=6000, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=500)
K9 = lambda T: dict(T=T, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=500)
K18 = dict(T=6000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500)
K90 = dict(T=3000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000)
CASOS_E = [
    ('brazo VIDA esc 30, corte 3000', (10001, 19901), ['FAMB_RES0_ECO'] * 30, K30, CR.eco_cfg('VIDA', 3000)),
    ('brazo CEREBRO esc 30, corte 3000', (10002,), ['FAMB_RES0_ECO'] * 30, K30, CR.eco_cfg('CEREBRO', 3000)),
    ('brazo AZAR esc 30 (p_mut 0.3), corte 3000', (10003,), ['FAMB_RES0_ECO'] * 30, K30, dict(CR.eco_cfg('AZAR', 3000), p_mut=0.3)),
    ('brazo MUT0 esc 30, corte 3000', (10004,), ['FAMB_RES0_ECO'] * 30, K30, CR.eco_cfg('MUT0', 3000)),
    ('(R) refunda=0: si todo muere, muere', (10005,), ['FAMB_RES0_ECO'] * 9, dict(K9(8000), muestra=100), dict(refunda=0)),
    ('genoma explicito NO entero, sin sombras', (10006,), ['FAMB_RES0_ECO'] * 9, K9(5000),
     dict(refunda=1, genoma=list(GX), p_mut=0.2, n_sombra=0, cada_gen=700, banco=30)),
    ('genoma NO entero y FERTIL (cerebro al azar), p_mut 0.2, 2 sombras', (19905,), ['FAMB_RES0_ECO'] * 9, K9(6000),
     dict(refunda=1, genoma=list(GXF), p_mut=0.2, n_sombra=2, cada_gen=1000, banco=30)),
    ('un genoma NO entero distinto por linaje (LAM, ETA_S, AVERSION, CLIP_S por cuerpo)', (19906,), ['FAMB_RES0_ECO'] * 9, K9(6000),
     dict(refunda=1, genoma=GXL, p_mut=0.1, banco=30)),
    ('DIVIDE: eta x4, NK 12', (10007,), ['FAMB_RES0_ECO'] * 9, K9(6000), dict(refunda=1, genoma=GEN(eta=0.12, NK=12))),
    ('NK 90 (sin division) y memoria_rechazo 80, eta x4', (10008,), ['FAMB_RES0_ECO'] * 9, K9(5000),
     dict(refunda=1, genoma=GEN(NK=90, memoria_rechazo=80, eta=0.12))),
    ('NK 8, memoria_rechazo 5, eta x4', (10009,), ['FAMB_RES0_ECO'] * 9, K9(5000), dict(refunda=1, genoma=GEN(NK=8, memoria_rechazo=5, eta=0.12))),
    ('tope 25 con eco (bloqueados)', (10010,), ['FAMB_RES0_ECO'] * 18, dict(K18, tope_cuerpos=25),
     dict(refunda=1, p_mut=0.1, n_sombra=2, banco=40, cada_gen=1500)),
    ('lectura extrema: eta_s x4, clip_s /4, aversion x4, lam x4', (10011,), ['FAMB_RES0_ECO'] * 18, K18,
     dict(refunda=1, genoma=GEN(eta_s=0.6, clip_s=2.5, aversion=4.0, lam=0.2), p_mut=0.1, banco=50)),
    ('lectura suave: eta_s /4, aversion /4, lam /4, del_s x4', (19902,), ['FAMB_RES0_ECO'] * 18, K18,
     dict(refunda=1, genoma=GEN(eta_s=0.0375, aversion=0.25, lam=0.0125, del_s=1.0), p_mut=0.1, banco=50)),
    ('mezcla con eco: 9 FAMB + 9 FABRICA_ECO (VIDA)', (19903,), ['FAMB_RES0_ECO'] * 9 + ['FABRICA_ECO'] * 9, K18, CR.eco_cfg('VIDA', 3000)),
    ('VIDA con banco 5 < n (p_mut 0.3)', (19904,), ['FAMB_RES0_ECO'] * 18, K18, dict(CR.eco_cfg('VIDA', 3000), banco=5, p_mut=0.3)),
    ('brazo VIDA esc 90, corte 2000', (19905,), ['FAMB_RES0_ECO'] * 90, K90, CR.eco_cfg('VIDA', 2000)),
    ('brazo CEREBRO esc 90, corte 2000', (19906,), ['FAMB_RES0_ECO'] * 90, K90, CR.eco_cfg('CEREBRO', 2000)),
    ('brazo AZAR esc 90, corte 2000', (19907,), ['FAMB_RES0_ECO'] * 90, K90, CR.eco_cfg('AZAR', 2000)),
    ('brazo MUT0 esc 90, corte 2000', (19908,), ['FAMB_RES0_ECO'] * 90, K90, CR.eco_cfg('MUT0', 2000)),
]
SAL_E = {}
for et, seeds, car, kw, eco in CASOS_E:
    for s in seeds:
        res, info, a, tt = compara(s, car, kw, eco=eco)
        E_ = a['eco']; SAL_E[(et, s)] = a
        reporta(f"{et} s{s}", res, info, tt, eco=True)
        out(f"        eco: nacidos {E_['n_nac']} · mutaciones {E_['n_mut']} (sombras {E_['n_mut_s']}) · fundadores del banco {E_['n_banco']}"
            f" · refundados {E_['n_refund']} · t_ext {E_['t_ext']} · corte {E_['corte'] and E_['corte']['vivos']} · gen_t {len(E_['gen_t'])}")
fg = []
ind = MF.run_solapadas(10005, ['FAMB_RES0_ECO'] * 9, eco=dict(refunda=1, ind_cb=lambda li, row, g: fg.append((li, row))), **dict(K9(6000), muestra=100))
di("(S) flujo de individuos del gemelo: filas == muertes + vivos y l.ind vacio",
   len(fg) == sum(l['deaths'] + l['vivos_final'] for l in ind['linajes']) and all(l['individuos'] == [] for l in ind['linajes']),
   f"filas {len(fg)}")

# ================================================================================================ (C)
seccion('(C) CHECKPOINT: estado completo del original == estado del gemelo; cortado y reanudado; firmas')
CKS = {}
for et, s, car, kw, eco in (('VIDA esc 30, corte 2500, p_mut 0.1, 4 sombras', 19908, ['FAMB_RES0_ECO'] * 30,
                             dict(T=4000, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=500),
                             dict(refunda=1, t_corte=2500, p_mut=0.1, banco=100, n_sombra=4, cada_gen=500)),
                            ('AZAR esc 90, tope 3000, muestra 1000', 19909, ['FAMB_RES0_ECO'] * 90,
                             dict(T=3000, diag=0, mundo_n=90, tope_cuerpos=3000, muestra=1000), dict(CR.eco_cfg('AZAR', 2000), p_mut=0.2))):
    cko, ckg = {}, {}
    so = ME.run_solapadas(sem(s), car, eco=dict(eco, ckpt_cada=1000, ckpt_fn=lambda t, b: cko.__setitem__(t, b)), **kw)
    sg = MF.run_solapadas(s, car, eco=dict(eco, ckpt_cada=1000, ckpt_fn=lambda t, b: ckg.__setitem__(t, b)), **kw)
    CKS[s] = (cko, ckg, so)
    di(f"{et} s{s}: seguida con checkpoints, gemelo == original (toda la salida)", N(so) == N(sg), f"checkpoints {sorted(cko)} / {sorted(ckg)}")
    for tt in sorted(cko):
        co = canon_orig(cko[tt]); cg = canon_gem(ckg[tt], kw['muestra'])
        dk = [k for k in co if N(co[k]) != N(cg.get(k))]
        nt = sum(1 for c in co['cuerpos'] if c['cerebro']['familia'].get('n10', {}).get('recibido', -1) > 0)
        di(f"{et}: ESTADO COMPLETO en t={tt} (cuerpos, cerebros, familia, genomas, mundo, rng, banco, contadores)", not dk,
           f"{len(co['cuerpos'])} cuerpos ({nt} con tabla), {len(co['mundo'])} objetos, banco {len(co['ES']['banco'])}; "
           f"pickle {len(cko[tt]) // 1024} KB / {len(ckg[tt]) // 1024} KB" + (f" · DIFIERE {dk}" if dk else ''))
    for tt in sorted(ckg):
        blob = pickle.loads(pickle.dumps(ckg[tt]))
        r = MF.run_solapadas(s, car, eco=dict(eco, estado=blob), **kw)
        di(f"{et}: gemelo cortado en t={tt} y reanudado == original seguido (toda la salida)", N(r) == N(so))
ecc = dict(refunda=1, t_corte=2500, p_mut=0.1, banco=100, n_sombra=4, cada_gen=500)
kwc = dict(T=4000, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=500)
cko, ckg, _so = CKS[19908]
m = aborta(lambda: MF.run_solapadas(10001, ['FAMB_RES0_ECO'] * 30, eco=dict(ecc, estado=ckg[2000]), **kwc))
di("checkpoint del gemelo de OTRA corrida aborta", m is not None and 'firma' in m, str(m))
m = aborta(lambda: MF.run_solapadas(19908, ['FAMB_RES0_ECO'] * 30, eco=dict(ecc, estado=cko[2000]), **kwc))
di("checkpoint del ORIGINAL en el gemelo aborta (formato propio; declarado)", m is not None and 'firma' in m, str(m))
m = aborta(lambda: ME.run_solapadas(19908, ['FAMB_RES0_ECO'] * 30, eco=dict(ecc, estado=ckg[2000]), **kwc))
di("checkpoint del GEMELO en el original aborta", m is not None and 'firma' in m, str(m))
m = aborta(lambda: MF.run_solapadas(19908, [('FAMB_RES0_ECO', FE)] * 30, eco=dict(ecc, estado=ckg[2000]), **kwc))
di("checkpoint de FAMB reanudado con las MISMAS etiquetas y el cerebro FABRICA_ECO aborta", m is not None and 'cerebros distintos' in m, str(m))
import motor_eco_rapido as MRV   # el gemelo VIEJO (FABRICA / FABRICA_ECO), solo se LEE
ckv = {}
MRV.run_solapadas(19908, ['FABRICA_ECO'] * 30, eco=dict(ecc, ckpt_cada=2000, ckpt_fn=lambda t, b: ckv.__setitem__(t, b)), **kwc)
ckn = {}
MF.run_solapadas(19908, ['FABRICA_ECO'] * 30, eco=dict(ecc, ckpt_cada=2000, ckpt_fn=lambda t, b: ckn.__setitem__(t, b)), **kwc)
m = aborta(lambda: MF.run_solapadas(19908, ['FABRICA_ECO'] * 30, eco=dict(ecc, estado=ckv[2000]), **kwc))
di("checkpoint del gemelo VIEJO en el gemelo nuevo aborta (firma)", m is not None and 'firma' in m, str(m))
m = aborta(lambda: MRV.run_solapadas(19908, ['FABRICA_ECO'] * 30, eco=dict(ecc, estado=ckn[2000]), **kwc))
di("checkpoint del gemelo nuevo en el gemelo VIEJO aborta (firma)", m is not None and 'firma' in m, str(m))

# ================================================================================================ (X)
seccion('(X) EL MUNDO DE LA SERIE con la familia (esc 90, 90 FAMB_RES0_ECO, tope 3000, muestra 1000)')
KWX = lambda T: dict(T=T, diag=0, mundo_n=CR.MUNDO['esc'], tope_cuerpos=CR.MUNDO['tope'], muestra=CR.MUNDO['muestra'])
VEL = {}; SAL_X = {}
for et, s, T, eco in (('VIDA, corte 3000', 19901, 4000, CR.eco_cfg('VIDA', 3000)), ('CEREBRO, corte 3000', 19902, 4000, CR.eco_cfg('CEREBRO', 3000)),
                      ('AZAR, corte 3000', 19903, 4000, CR.eco_cfg('AZAR', 3000)), ('MUT0, corte 3000', 19904, 4000, CR.eco_cfg('MUT0', 3000))):
    t0 = time.time(); a = ME.run_solapadas(sem(s), ['FAMB_RES0_ECO'] * CR.MUNDO['n0'], eco=eco, **KWX(T)); ta = time.time() - t0
    MF.run_solapadas(s, ['FAMB_RES0_ECO'] * CR.MUNDO['n0'], eco=eco, **KWX(200))   # caliente
    t0 = time.time(); b = MF.run_solapadas(s, ['FAMB_RES0_ECO'] * CR.MUNDO['n0'], eco=eco, **KWX(T)); tb = time.time() - t0
    cm = float(np.mean(a['pista']['tam_total'])); VEL[et] = (T, ta, tb, cm); SAL_X[et] = a
    di(f"{et} s{s} T={T}: toda la salida", N(a) == N(b),
       f"cuerpos medios {cm:.1f}, max {a['pista']['max_vivos']}, nacidos {a['eco']['n_nac']}, refundados {a['eco']['n_refund']}, vivos en T "
       f"{len(a['eco']['vivos_final'])}; original {ta:.1f} s ({T / ta:.0f} pasos/s), gemelo {tb:.2f} s ({T / tb:.0f} pasos/s), x{ta / tb:.0f}"
       + ('' if N(a) == N(b) else f" · DIFIERE {claves_distintas(a, b)[:5]}"))

# ================================================================================================ (J)
seccion("(J) corre_eco SIN cambiar su letra: CR.ME = gemelo (como corre_eco_rapido) y MUNDO['carro'] = FAMB_RES0_ECO en este proceso")
import types
ME_ORIG = ME
ME_GEM = types.ModuleType('motor_eco_gemelo_fam')
ME_GEM.__dict__.update({k: v for k, v in ME.__dict__.items() if not k.startswith('__')})
ME_GEM.run_solapadas = MF.run_solapadas


JUEZ_PRACTICA = dict(CR.JUEZ, semillas=(19907, 19908))   # trabajo() llama al juez con JUEZ['semillas']: aqui, SOLO de practica


def con(motor, carro, f, *a):
    viejo = CR.ME; vc = CR.MUNDO['carro']; vj = CR.JUEZ; CR.ME = motor; CR.MUNDO['carro'] = carro; CR.JUEZ = JUEZ_PRACTICA
    try: return f(*a)
    finally: CR.ME = viejo; CR.MUNDO['carro'] = vc; CR.JUEZ = vj


jo = con(ME_ORIG, 'FAMB_RES0_ECO', CR.juez, list(G0), (19901, 19902), 20000)
jg = con(ME_GEM, 'FAMB_RES0_ECO', CR.juez, list(G0), (19901, 19902), 20000)
di("juez con FAMB_RES0_ECO: bateria de G0 (esc 9, 9 fundadores, sin mutacion ni reposicion, T_b 20000), 2 semillas de practica",
   N(jo) == N(jg), str([(d['vive'], d['nac']) for d in jo]))
banco = CKS[19908][2]['eco']['corte']['banco']   # el banco REAL en el corte de la corrida (C) (FAMB, VIDA-like, p_mut 0.1)
jo = con(ME_ORIG, 'FAMB_RES0_ECO', CR.juez, banco, (19903, 19904), 8000)
jg = con(ME_GEM, 'FAMB_RES0_ECO', CR.juez, banco, (19903, 19904), 8000)
di(f"juez con FAMB_RES0_ECO: banco REAL del corte ({len(banco)} genomas, 9 al azar por semilla), T_b 8000", N(jo) == N(jg),
   str([(d['vive'], d['nac']) for d in jo]))
jo = con(ME_ORIG, 'FABRICA_ECO', CR.juez, list(G0), (19905,), 10000)
jg = con(ME_GEM, 'FABRICA_ECO', CR.juez, list(G0), (19905,), 10000)
di("juez con FABRICA_ECO (el MUNDO de v1, regresion): G0, T_b 10000", N(jo) == N(jg), str([(d['vive'], d['nac']) for d in jo]))
tmp = tempfile.mkdtemp(prefix='eco_rapido_fam_')
try:
    args = lambda d, re: (19906, 'VIDA', 12000, 8000, d, 1, 3000, re)
    da, db, dc = (os.path.join(tmp, x) for x in 'abc')
    for d in (da, db, dc): os.makedirs(d)
    t0 = time.time(); ro = con(ME_ORIG, 'FAMB_RES0_ECO', CR.trabajo, args(da, False)); to = time.time() - t0
    t0 = time.time(); rg_ = con(ME_GEM, 'FAMB_RES0_ECO', CR.trabajo, args(db, False)); tg = time.time() - t0
    sin = lambda r: {k: v for k, v in r.items() if k != 'seg'}
    ja = json.load(open(os.path.join(da, 'VIDA_s19906.json'), encoding='utf-8')); jb = json.load(open(os.path.join(db, 'VIDA_s19906.json'), encoding='utf-8'))
    di("trabajo(19906, VIDA, T 12000, corte 8000, juez 1x3000 en la semilla de practica 19907) con FAMB: resultado y JSON == original (salvo 'seg')",
       N(sin(ro)) == N(sin(rg_)) and N(sin(ja)) == N(sin(jb)),
       f"persiste {ro['persiste']} t_ext {ro['t_ext']} nacidos {ro['n_nac']} vivos_T {ro['vivos_T']} juez "
       f"{[d['vive'] for d in ro['juez']['bateria']] if ro['juez'] else None}; original {to:.1f} s, gemelo {tg:.1f} s")

    class Corte(Exception): pass

    def corta(*a, **k):
        fn = k['eco']['ckpt_fn']

        def f2(t, blob): fn(t, blob); raise Corte(t)
        k['eco'] = dict(k['eco'], ckpt_fn=f2)
        return MF.run_solapadas(*a, **k)
    ME_GEM.run_solapadas = corta
    try: con(ME_GEM, 'FAMB_RES0_ECO', CR.trabajo, args(dc, False)); cortado = None
    except Corte as e: cortado = e.args[0]
    finally: ME_GEM.run_solapadas = MF.run_solapadas
    rr = con(ME_GEM, 'FAMB_RES0_ECO', CR.trabajo, args(dc, True))
    di("trabajo con FAMB cortado ('corte de luz' tras el checkpoint) y reanudado con reanuda=True == original seguido",
       cortado == 10000 and N(sin(rr)) == N(sin(ro)), f"cortado en t={cortado}")
finally:
    shutil.rmtree(tmp)
di("el MUNDO y el JUEZ de corre_eco quedan como estaban (FABRICA_ECO, 19201-19220) y CR.ME es el original",
   CR.MUNDO['carro'] == 'FABRICA_ECO' and CR.JUEZ['semillas'] == tuple(range(19201, 19221)) and CR.ME is ME_ORIG)

# ================================================================================================ (L)
seccion('(L) LARGO: pista v2 con 9 FAMB a T 60 000 y eco VIDA esc 9 a T 40 000 (eventos raros: empates, divisiones, tablas)')
for et, s, car, kw, eco in (('9 FAMB eco=None T=60000', 19907, [FT] * 9, dict(T=60000, diag=0), None),
                            ('eco VIDA esc 9 T=40000, corte 20000', 19909, ['FAMB_RES0_ECO'] * 9, dict(T=40000, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=1000),
                             CR.eco_cfg('VIDA', 20000))):
    res, info, a, tt = compara(s, car, kw, eco=eco)
    reporta(f"{et} s{s}", res, info, tt, eco=eco is not None)

# ================================================================================================ (R)
seccion('(R) REGRESION FABRICA / FABRICA_ECO: contra el original y contra el gemelo VIEJO (motor_eco_rapido, 120/120)')
KWM = dict(T=6000, diag=0, mundo_n=18, tope_cuerpos=3000, muestra=500)
for et, s, car, kw, eco in (('9 FABRICA fija T=3000', 10001, ['FABRICA'] * 9, dict(T=3000, diag=0), None),
                            ('9 FABRICA_ECO (tupla) T=3000', 10002, [('FABRICA_ECO', FE)] * 9, dict(T=3000, diag=0), None),
                            ('9 FABRICA inmediata T=2000', 10003, ['FABRICA'] * 9, dict(T=2000, diag=0, reposicion='inmediata'), None),
                            ('eco VIDA esc 18 FABRICA_ECO, corte 3000', 19901, ['FABRICA_ECO'] * 18, KWM, CR.eco_cfg('VIDA', 3000)),
                            ('eco AZAR esc 18 FABRICA_ECO (p_mut 0.3)', 19902, ['FABRICA_ECO'] * 18, KWM, dict(CR.eco_cfg('AZAR', 3000), p_mut=0.3)),
                            ('eco DIVIDE FABRICA_ECO: eta x4, NK 12', 10004, ['FABRICA_ECO'] * 9, dict(T=5000, diag=0, mundo_n=9, tope_cuerpos=3000, muestra=500),
                             dict(refunda=1, genoma=GEN(eta=0.12, NK=12)))):
    res, info, a, tt = compara(s, car, kw, eco=eco)
    reporta(f"{et} s{s}", res, info, tt, eco=eco is not None)
    SALIDAS[(et, s)] = a
for et, s, car, kw, eco in (('9 FABRICA eco=None T=100000', 10005, ['FABRICA'] * 9, dict(T=100000, diag=0), None),
                            ('mundo de la serie, 90 FABRICA_ECO, VIDA T=30000, corte 20000', 19903, ['FABRICA_ECO'] * 90, KWX(30000),
                             CR.eco_cfg('VIDA', 20000))):
    t0 = time.time(); v = MRV.run_solapadas(sem(s), car, eco=eco, **kw); tv = time.time() - t0
    t0 = time.time(); w = MF.run_solapadas(s, car, eco=eco, **kw); tw = time.time() - t0
    di(f"{et} s{s}: gemelo nuevo == gemelo VIEJO (toda la salida)", N(v) == N(w),
       f"partos {sum(l['descendientes'] for l in v['linajes'])}, max_vivos {v['pista']['max_vivos']}; viejo {tv:.1f} s, nuevo {tw:.1f} s")

# ================================================================================================ (K)
seccion('(K) CONTROLES que DEBEN fallar (si nada cambia, nada controla: ERR-38)')
base = SALIDAS[('9 FAMB T=20000 (generaciones: la tabla viaja)', 19906)]
g = MF.run_solapadas(19907, [FT] * 9, T=20000, diag=0)
di("gemelo con la semilla vecina != original", N(g) != N(base))

def gemelo_como(G, modo):
    """El gemelo con un CONTROL, en las condiciones exactas de una corrida guardada: (salida, filas, nacimientos) distintos?"""
    fg = []; trn = []
    eg = None if G['eco'] is None else dict(G['eco'])
    if G['filas']: eg['ind_cb'] = lambda li, row, g: fg.append((li, list(row), HX(g)))
    b = MF.run_solapadas(G['seed'], G['carros'], eco=eg, _modo=modo, _traza_nac=trn, **G['kw'])
    return N(b) != G['a'], N(fg) != G['fo'], N(trn) != G['nac']


out(f"  barrido de los controles de la familia sobre {len(GUARDA)} corridas FAMB guardadas del original ((I), (E), (L))")
for et, modo, clave, qu in (("SIN el filtro SIN0 (instala las neutras)", dict(sin0=0), 'neutras', 'con alguna tabla con entradas neutras'),
                            ("que NO lee el nodo", dict(nodo=1), 'no_vacias', 'con alguna tabla no vacia'),
                            ("con el empate de la lectura al PRIMER indice", dict(nodo=2), 'una', 'con alguna tabla de UNA entrada')):
    pred = [G for G in GUARDA if G[clave] > 0]; resto = [G for G in GUARDA if G[clave] == 0]
    dp = [gemelo_como(G, modo) for G in pred]; dr = [gemelo_como(G, modo) for G in resto]
    npf = sum(1 for x in dp if any(x)); nrf = sum(1 for x in dr if any(x)); nfis = sum(1 for x in dp + dr if x[0] or x[1])
    di(f"CONTROL (debe fallar): gemelo {et} != original en TODA corrida {qu}", len(pred) > 0 and npf == len(pred),
       f"distintas {npf}/{len(pred)} (en nacimientos {sum(1 for x in dp if x[2])}); en las otras {len(resto)}: distintas {nrf}; "
       f"con la FISICA (salida o filas) distinta: {nfis}/{len(GUARDA)}")
for et, modo in (("gemelo con exp de libm (sin el bucle de NumPy)", dict(exp=1)), ("gemelo con suma ingenua (sin BLAS)", dict(dot=1)),
                 ("gemelo con turno fijo (mismo consumo de azar)", dict(turno=1))):
    res, info, a, tt = compara(10001, [FT] * 9, dict(T=5000, diag=0), modo=modo)
    di(f"{et} != original (trayectoria o pesos)", not (res['traza'] and res['cerebros']),
       f"salida {'=' if res['salida'] else '!='} · traza {'=' if res['traza'] else '!='} · cerebros {'=' if res['cerebros'] else '!='}")
fe = MF.run_solapadas(19906, [('FAMB_RES0_ECO', FE)] * 9, T=20000, diag=0)
di("FAMB contra FABRICA_ECO (misma semilla y etiqueta): la familia cambia la fisica", N(fe['linajes'][0]['tam']) != N(base['linajes'][0]['tam'])
   or N([l['individuos'] for l in fe['linajes']]) != N([l['individuos'] for l in base['linajes']]),
   f"partos {sum(l['descendientes'] for l in fe['linajes'])} / {sum(l['descendientes'] for l in base['linajes'])}")
e1 = MF.run_solapadas(10001, ['FAMB_RES0_ECO'] * 30, eco=CR.eco_cfg('VIDA', 3000), **K30)
e2 = MF.run_solapadas(10001, ['FAMB_RES0_ECO'] * 30, eco=CR.eco_cfg('MUT0', 3000), **K30)
e3 = MF.run_solapadas(10001, ['FAMB_RES0_ECO'] * 30, eco=CR.eco_cfg('AZAR', 3000), **K30)
di("brazo VIDA != MUT0 (misma semilla, FAMB)", N(e1) != N(e2), f"mutaciones {e1['eco']['n_mut']} / {e2['eco']['n_mut']}")
di("brazo AZAR != VIDA (misma semilla, FAMB)", N(e1['eco']['gen_t']) != N(e3['eco']['gen_t']))
di("reposicion inmediata != fija (FAMB)", N(MF.run_solapadas(10004, [FT] * 9, T=3000, diag=0)) != N(SALIDAS[('9 FAMB inmediata T=3000', 10004)]))

# ================================================================================================ (G)
seccion('(G) GUARDIAS: las del original con el mismo mensaje; las del gemelo (lo que no compila aborta)')
for et, kw in (("10 linajes con eco=None", dict(seed=1, carros=[FT] * 10, T=10, diag=0)),
               ("diag=1", dict(seed=1, carros=[FT], T=10)),
               ("compat=1", dict(seed=1, carros=[FT], T=10, diag=0, compat=1)),
               ("rep_acum=2", dict(seed=1, carros=[FT], T=10, diag=0, rep_acum=2)),
               ("tope_cuerpos < n", dict(seed=1, carros=[FT] * 3, T=10, diag=0, tope_cuerpos=2)),
               ("reposicion invalida", dict(seed=1, carros=[FT], T=10, diag=0, reposicion='otra')),
               ("mundo_n fuera de rango", dict(seed=1, carros=[FT], T=10, diag=0, mundo_n=10)),
               ("'FAMB_RES0_ECO' como texto con eco=None (no es carro de la carrera)", dict(seed=1, carros=['FAMB_RES0_ECO'], T=10, diag=0)),
               ("clave eco desconocida", dict(seed=1, carros=['FAMB_RES0_ECO'], T=10, diag=0, eco=dict(refnda=0))),
               ("genoma fuera de rango", dict(seed=1, carros=['FAMB_RES0_ECO'], T=10, diag=0, eco=dict(genoma=list(G0 * 10)))),
               ("t_corte sin vivero", dict(seed=1, carros=['FAMB_RES0_ECO'], T=10, diag=0, eco=dict(refunda=0, t_corte=5))),
               ("mundo_n fuera de rango con eco", dict(seed=1, carros=['FAMB_RES0_ECO'], T=10, diag=0, mundo_n=2001, eco=dict(refunda=1))),
               ("401 linajes con eco", dict(seed=1, carros=['FAMB_RES0_ECO'] * 401, T=10, diag=0, eco=dict(refunda=1)))):
    mo = aborta(lambda: ME.run_solapadas(**kw)); mg = aborta(lambda: MF.run_solapadas(**kw))
    di(f"{et}: aborta igual que el original", mo is not None and mo == mg, str(mg)[:110])
tmpv = tempfile.mkdtemp(prefix='famb_var_')
try:
    pv0 = os.path.join(tmpv, 'FAMB_RES0_ECO.py'); open(pv0, 'w', encoding='utf-8').write(CFAM.texto(0))
    _sp = importlib.util.spec_from_file_location('famb_var0', pv0); V0 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(V0)
    for et, kw in (("carro FAMB con SIN0 = 0 (variante construida, mismo nombre de archivo)", dict(seed=1, carros=[('FAMB_RES0_ECO', V0)] * 3, T=10, diag=0)),
                   ("carro O2 (no es un cerebro compilado)", dict(seed=1, carros=['O2'] * 3, T=10, diag=0)),
                   ("T = 3 (el original divide por T // 4 = 0)", dict(seed=1, carros=[FT] * 3, T=3, diag=0)),
                   ("carro APR_ECO con eco", dict(seed=1, carros=['APR_ECO'] * 3, T=10, diag=0, eco=dict(refunda=1)))):
        mg = aborta(lambda: MF.run_solapadas(**kw))
        di(f"{et}: el gemelo aborta (fuera de alcance)", mg is not None and mg.startswith('ValueError'), str(mg)[:120])
finally:
    shutil.rmtree(tmpv)

# ================================================================================================ (D)
seccion('(D) DETERMINISMO')
e1b = MF.run_solapadas(10001, ['FAMB_RES0_ECO'] * 30, eco=CR.eco_cfg('VIDA', 3000), **K30)
di("dos llamadas iguales del gemelo (FAMB, eco VIDA con mutacion) dan la misma salida", N(e1) == N(e1b))

# ================================================================================================ (Z)
seccion('(Z) CACHE: un proceso NUEVO carga la cache de numba y reproduce corridas del original')
tmp = tempfile.mkdtemp(prefix='eco_rapido_fam_cache_')
try:
    ref = os.path.join(tmp, 'ref.json')
    refs = {'I': SALIDAS[('9 FAMB fija T=5000', 10001)], 'E': SAL_X['VIDA, corte 3000'],   # (X): el original SIN ind_cb
            'R': SALIDAS[('9 FABRICA_ECO (tupla) T=3000', 10002)]}
    json.dump(dict(refs={k: N(v) for k, v in refs.items()}, eco=CR.eco_cfg('VIDA', 3000), kx=KWX(4000)), open(ref, 'w'))
    hijo = r'''
import json, sys, time, os
t0 = time.time()
sys.path[:0] = [sys.argv[2], os.path.join(os.path.dirname(os.path.dirname(sys.argv[2])), 'experimentos', 'generaciones')]
import motor_eco_rapido_fam as MF
import motor_eco as ME
from numba.core.registry import CPUDispatcher
t1 = time.time()
R = json.load(open(sys.argv[1])); N = lambda x: json.dumps(x, default=str, sort_keys=True)
FM = ME.carga_eco('FAMB_RES0_ECO'); FE = ME.carga_eco('FABRICA_ECO')
ok = []; tiempos = []
for tipo in ('I', 'E', 'R'):
    t2 = time.time()
    if tipo == 'I': r = MF.run_solapadas(10001, [('FAMB_RES0_ECO', FM)] * 9, T=5000, diag=0)
    elif tipo == 'E': r = MF.run_solapadas(19901, ['FAMB_RES0_ECO'] * 90, eco=R['eco'], **R['kx'])
    else: r = MF.run_solapadas(10002, [('FABRICA_ECO', FE)] * 9, T=3000, diag=0)
    tiempos.append(round(time.time() - t2, 2)); ok.append(N(r) == R['refs'][tipo])
hits = miss = 0
for nom in dir(MF):
    f = getattr(MF, nom)
    if isinstance(f, CPUDispatcher):
        hits += sum(f.stats.cache_hits.values()); miss += sum(f.stats.cache_misses.values())
print(json.dumps(dict(ok=ok, import_s=round(t1 - t0, 2), tiempos=tiempos, hits=hits, miss=miss)))
'''
    p = subprocess.run([sys.executable, '-c', hijo, ref, AQUI], capture_output=True, text=True, timeout=1800)
    try: z = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception: z = dict(ok=[False], hits=0, miss=-1, import_s=None, tiempos=None, err=p.stderr[-600:])
    di("proceso NUEVO: lee la cache (0 compilaciones) y reproduce 3 corridas del original bit a bit (FAMB eco=None; FAMB eco VIDA, esc 90; FABRICA_ECO)",
       all(z['ok']) and len(z['ok']) == 3 and z['miss'] == 0 and z['hits'] > 0,
       f"identicas {z['ok']}; funciones cargadas de la cache {z['hits']}, compiladas {z['miss']}; import {z['import_s']} s; "
       f"corridas {z['tiempos']} s" + (f" · {z.get('err')}" if z.get('err') else ''))
finally:
    shutil.rmtree(tmp)

# ================================================================================================ (V)
seccion('(V) ACELERACION (mismo mundo, mismo proceso; la maquina corre otros 3 procesos: tiempos con carga)')
for et, (T, ta, tb, cm) in VEL.items():
    out(f"  mundo ECO esc 90 con FAMB_RES0_ECO, {et}: T={T}, {cm:.1f} cuerpos de media · original {T / ta:.0f} pasos/s "
        f"({ta / T / cm * 1e6:.1f} us por cuerpo y paso) · gemelo {T / tb:.0f} pasos/s ({tb / T / cm * 1e6:.2f} us por cuerpo y paso) · x{ta / tb:.0f}")
a = SALIDAS[('9 FAMB T=20000 (generaciones: la tabla viaja)', 19906)]
t0 = time.time(); ME.run_solapadas(19906, [FT] * 9, T=20000, diag=0); ta = time.time() - t0
t0 = time.time(); MF.run_solapadas(19906, [FT] * 9, T=20000, diag=0); tb = time.time() - t0
cm = float(np.mean(a['pista']['tam_total']))
out(f"  pista v2, 9 FAMB_RES0_ECO, T=20000: {cm:.1f} cuerpos de media · original {20000 / ta:.0f} pasos/s · gemelo {20000 / tb:.0f} pasos/s · x{ta / tb:.0f}")
out(f"tiempo {round(time.time() - T00)} s")
out(f"RESULTADO: {OK[0]}/{OK[1]}")
SAL.close()
