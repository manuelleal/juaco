"""motor_convive.py — PISTA v2 CON GENERACIONES SOLAPADAS (pista2.run(..., solapadas=1)).

MISION: llegar a la AGI por este camino.

Pedido del director (22-sep): un mundo donde las generaciones CONVIVAN. En la pista v1 hay UN cuerpo vivo por linaje y
el hijo espera en una cola hasta que muere el padre; para que haya generaciones el padre tiene que morir (ERR-102).

EL MUNDO ES EL MISMO: L = 40*esc, nobj = 4*esc, esc sorteos de olvido por paso (ERR-98), mismos objetos, mismos
efectos, mismos costos (0.001 por necesidad y paso), ventana de reproduccion (E y Ag >= 1.0 durante 500 pasos), dote 0.6.
Con esc = numero de linajes fundadores (9 en monocultivo: L = 360, 36 objetos), FIJO durante toda la corrida.

REGLAS NUEVAS (las unicas):
 P1 PARTO REAL. Cuando un cuerpo completa la ventana (y no la veta con quiere_parir), paga la dote (E -= 0.6, Ag -= 0.6)
    y el hijo NACE EN ESE PASO como cuerpo vivo, en la MISMA CELDA del padre (sin rng), con E = Ag = dote. No hay cola.
    Actua desde el paso siguiente (como el cuerpo que nacia de la cola en v1). Pueden vivir a la vez varios cuerpos del
    mismo linaje.
 P2 CEREBRO POR CUERPO. Cada cuerpo es una INSTANCIA del carro: crea(ctx) con su propio rng de cuerpo
    [seed, linaje, 12, k] (k = numero de cuerpo en el linaje, k >= 1) y en seguida nace(info) con
    info = dict(t, k, fundador=False, memoria=<lo que devolvio al_parir del padre>, rng_hijo=[seed, linaje, 13, k], padre).
    La herencia viaja SOLO por al_parir/nace (lo que el carro declara). ctx['id'] = '<linaje>/<k>' (unico por cuerpo).
 P3 EXTINCION. Si muere el ULTIMO cuerpo vivo de un linaje, el mundo pone un FUNDADOR LIMPIO (ENMIENDA 5): instancia nueva
    crea(ctx) con el rng de fundadores del linaje [seed, linaje, 12, 0] (el mismo de v1), SIN nace(), posicion del rng de
    muerte del linaje [seed, linaje, 14, 0], E = Ag = dote, id = el del linaje. Toma el LUGAR del muerto en la lista de
    turno (con eso, sin partos, v2 == v1 con fundador_limpio=1 BIT A BIT: arnes (S)). Se cuenta como fundador.
 P4 CAPACIDAD DE CARGA: NINGUN tope de cuerpos por linaje. La densidad la regulan los recursos: la comida y el agua son
    los mismos 4*esc objetos (el mundo repone al azar lo que se muerde y olvida); con mas cuerpos cada uno llega a menos
    objetos buenos, tarda mas en juntar 500 pasos saciado (menos partos) y muere mas (dependencia de la densidad).
    TOPE DE SEGURIDAD COMPUTACIONAL (declarado, no biologico): tope_cuerpos (por defecto 300) cuerpos vivos EN TODA LA
    PISTA. Al alcanzarlo, una ventana completa NO produce hijo: no se paga la dote, la ventana se reinicia y se cuenta
    en 'bloqueados' (por linaje) y 't_tope' (primer paso con el tope alcanzado). Si bloqueados > 0 la corrida queda
    MARCADA: la densidad no la regulo el mundo.
 P5 quiere_parir(info): info['cola'] = cuerpos vivos del linaje SIN contar al que pare (la 'reserva viva': en v1 la cola
    era la reserva de hijos del linaje; en v2 esa reserva esta viva en el mundo). Tambien vivos_linaje y hijos_vivos
    (hijos vivos de ESE cuerpo). Asi la muerte programada de O3 (TERMINAL, cola_est >= 4) y O4 (senescencia, cola >= 6)
    sigue disponible con la misma letra.
 P7 REPOSICION DEL MUNDO (opcion reposicion; MEDIDO en el humo de 10001, T=5000: con la regla de v1 NO hay capacidad de
    carga para quien limpia: 9 O2 pasan de 9 a 128 cuerpos y siguen creciendo; ver INFORME_CONVIVE.md):
    'inmediata' = v1: lo mordido u olvidado se repone AL INSTANTE con una letra al azar. Cada mordida de B/D fabrica
       ~0.5 objetos buenos: limpiar es una bomba de energia y el flujo de comida CRECE con el numero de cuerpos.
    'fija' (por defecto con solapadas=1) = QUIMIOSTATO: lo mordido u olvidado desaparece y el mundo repone a tasa FIJA
       r = r_rep * esc objetos por paso (r_rep = 0.03: la reposicion medida del mundo SOLO de v1 con un FABRICA,
       0.0316 por paso en 10001-10004, T=20000), a lo sumo 1 objeto pendiente (banco <= 1 + r) y hasta nobj objetos,
       en celda libre al azar con letra al azar (rng del mundo). Piso: si un paso deja el mundo SIN objetos, se pone uno
       al instante (los carros de v1 no estan escritos para un mundo vacio; se cuenta en 'pisos'). Con demanda < r
       el mundo es casi el de v1; con demanda > r el flujo de comida queda FIJO -> capacidad de carga
       K <= (r/2 * 0.8) / 0.001 por necesidad (~54 cuerpos con esc = 9, cota sin perdidas).
 P6 turno: permutacion nueva cada paso sobre los cuerpos vivos (rng de la pista [seed, 0, 15, 0], como v1).
    Lista de turno: vivos en su orden + nacidos en el paso al final; un fundador ocupa el lugar del muerto.

NO SE PORTAN (declarado): compat=1, diag=1 (el diagnostico de robos/boca de v1), exposiciones/xor/p1/c1 (telemetria F9).
El clasificador fisico de muertes voluntarias (ENMIENDA 6) se conserva, pero NO discrimina (ERR-103): la cifra que vale
es la DECLARADA por el carro (VOL_DECL: O3 'cuerpos_term', O4 'senescentes'), leida de salida() de la instancia al morir.

SALIDA: dict(linajes=[...], pista=..., pizarra_log=[...]). Por linaje, en primer nivel SOLO fisica (ERR-96):
individuos = [[k, gen, padre, t_nace, t_muere(-1 si vive en T), hijos, fundador, causa, vol_decl], ...]; tam = cuerpos vivos
del linaje cada MUESTRA pasos (al inicio del paso; mas el valor final). Lo del carro va en d['carro'].
"""
import math, os, sys, types
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)

MUESTRA = 100
TOPE_DEF = 300
R_REP = 0.03     # P7: objetos por paso y por unidad de escala (mundo SOLO de v1: 0.0316 medido)
VOL_DECL = {'O3': 'cuerpos_term', 'O4': 'senescentes', 'CTRL_O3_SINTERM': 'cuerpos_term'}   # muerte programada DECLARADA por el carro (bitacoras)
CAUSAS = ('hambre', 'sed', 'veneno', 'sal')


class Cuerpo:
    __slots__ = ('lin', 'k', 'gen', 'padre', 'tn', 'c', 'id', 'obs', 'pos', 'E', 'Ag', 'gv', 'gv0', 'tB', 'tD',
                 'ult_mordida', 'vol_kk', 'hijos', 'fund', 'vivo', 'hvivos', 'pc')

    def __init__(self, lin, k, gen, padre, tn, c, ident, vista, pos, E, fund, pc=None):
        self.lin = lin; self.k = k; self.gen = gen; self.padre = padre; self.tn = tn; self.c = c; self.id = ident
        self.obs = dict(yo=ident, objs=vista); self.pos = pos; self.E = E; self.Ag = E
        self.gv = 0; self.gv0 = 0; self.tB = -10 ** 9; self.tD = -10 ** 9; self.ult_mordida = None; self.vol_kk = None
        self.hijos = 0; self.fund = fund; self.vivo = True; self.hvivos = 0; self.pc = pc   # pc = cuerpo padre (vivo o no)


class LinajeV2:
    def __init__(self, i, ident, T, etiqueta):
        self.i = i; self.id = ident; self.T = T; self.etq = etiqueta
        self.mord = {k: [0] * 4 for k in 'ABCD'}; self.vis = {k: [0] * 4 for k in 'ABCD'}
        self.deaths = 0; self.mnec = [0, 0]; self.causas = {k: 0 for k in CAUSAS}; self.muertes_vol = 0
        self.fund = 0; self.tfund = []; self.desc = 0; self.nac = 0; self.vetos = 0; self.bloq = 0
        self.escrituras = 0; self.escr = []; self.vidas = []; self.ind = []; self.vivos = 0; self.tam = []
        self.vol_decl = 0; self.pv = 0

    def q(self, t): return min(t // (self.T // 4), 3)


def run_solapadas(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None,
                  fundador_limpio=0, tope_cuerpos=TOPE_DEF, muestra=MUESTRA, reposicion='fija', r_rep=R_REP):
    import pista2 as P
    n = len(carros)
    if not 1 <= n <= P.N_MAX: raise SystemExit(f"PISTA2: entre 1 y {P.N_MAX} linajes fundadores (hay {n})")
    if compat: raise SystemExit("PISTA2: solapadas=1 no admite compat=1 (el ancla del monolito es de la pista v1)")
    if diag: raise SystemExit("PISTA2: solapadas=1 exige diag=0 (el diagnostico de v1 no se porto; declarado)")
    if rep_acum not in (0, 1): raise SystemExit("PISTA2: rep_acum es 0 o 1")
    if not (isinstance(tope_cuerpos, int) and tope_cuerpos >= n): raise SystemExit("PISTA2: tope_cuerpos entero >= n")
    if reposicion not in ('inmediata', 'fija'): raise SystemExit("PISTA2: reposicion 'inmediata' (v1) o 'fija' (quimiostato)")
    inst = reposicion == 'inmediata'
    # fundador_limpio: en v2 el fundador SIEMPRE es limpio (P3); el argumento se acepta y se ignora (se declara en la salida)
    CF = P.cfg_fabrica(); kw = CF['kw']; VAL_VIVO, EFECTO = CF['VAL_VIVO'], CF['EFECTO']
    if mundo_n is not None and (int(mundo_n) != mundo_n or not 1 <= mundo_n <= P.N_MAX):
        raise SystemExit(f"PISTA2: mundo_n entre 1 y {P.N_MAX}")
    esc = int(mundo_n) if mundo_n is not None else (n if escala else 1)
    L = CF['L'] * esc
    M = dict(nobj=kw['nobj'] * esc, costo=kw['costo'], costo_a=kw['costo_a'], rep_X=kw['rep_X'],
             rep_umbral=kw['rep_umbral'], dote=kw['dote'], olvido=P.OLVIDO)
    mods = [(c, P.carga_carro(c)) if isinstance(c, str) else c for c in carros]
    etiquetas = [e for e, _ in mods]
    ids = [(e if etiquetas.count(e) == 1 else f"{e}#{i}") for i, e in enumerate(etiquetas)]
    SS = lambda i, etq, k: np.random.default_rng([seed, i, P.ETQ[etq], k])
    rng = SS(0, 'mundo', 0)
    rngs_fund = [SS(i, 'cuerpo', 0) for i in range(n)]
    rngs_muerte = [SS(i, 'muerte', 0) for i in range(n)]
    rng_pista = SS(0, 'pista', 0)

    objs = {}; vista = types.MappingProxyType(objs)
    lin = [LinajeV2(i, ids[i], T, etiquetas[i]) for i in range(n)]
    id2lin = {}

    def ctx_de(i, r, ident):
        return dict(id=ident, indice=i, n_linajes=n, T=T, L=L, PAT={k: v.copy() for k, v in CF['PAT'].items()},
                    rng=r, dote=M['dote'], rep_umbral=M['rep_umbral'], costo=M['costo'], costo_a=M['costo_a'],
                    rep_X=M['rep_X'], cupo=P.CUPO, ancho=P.ANCHO, fabrica=P.cfg_fabrica())

    cuerpos = []
    for i, (e, mod) in enumerate(mods):   # los cerebros nacen ANTES del primer spawn (como en v1)
        c = mod.crea(ctx_de(i, rngs_fund[i], ids[i]))
        cuerpos.append(Cuerpo(i, 0, 0, -1, 0, c, ids[i], vista, 0, M['dote'], 1))
        id2lin[ids[i]] = i; lin[i].vivos = 1; lin[i].fund = 0
    for b in cuerpos: b.E = 1.0; b.Ag = kw['A_ini']   # v1 (Linaje.__init__): el primer cuerpo arranca con E = 1.0, Ag = A_ini
    for b in cuerpos: b.pos = int(rng_pista.integers(L))

    def spawn():
        while len(objs) < M['nobj']:
            x = int(rng.integers(L))
            if x not in objs: objs[x] = P.TIPOS[int(rng.integers(len(P.TIPOS)))]
    spawn()
    r_paso = float(r_rep) * esc; banco = [0.0]; pisos = [0]; llegadas = [0]; perdidas = [0]

    def quita(x):   # P7: con 'inmediata' se repone al instante (v1); con 'fija' solo se quita (piso de 1 objeto)
        del objs[x]
        if inst: spawn()
        elif not objs:
            pisos[0] += 1; x2 = int(rng.integers(L)); objs[x2] = P.TIPOS[int(rng.integers(len(P.TIPOS)))]

    from collections import deque
    piz = deque(maxlen=P.CUPO); piz_t = (); n_escr_desc = 0; piz_log = []
    olv_n = 0; comp = {k: 0 for k in P.TIPOS}; nobj_suma = 0
    total = n; max_vivos = n; t_tope = None; tam_total = []
    orden = list(range(len(cuerpos)))

    def registra(b, tm, causa, vd):
        L_ = lin[b.lin]
        L_.ind.append([b.k, b.gen, b.padre, b.tn, tm, b.hijos, b.fund, causa, vd])

    for t in range(T):
        if t % muestra == 0:
            for l in lin: l.tam.append(l.vivos)
            tam_total.append(total)
        for v in objs.values(): comp[v] += 1
        nobj_suma += len(objs)
        nb = len(cuerpos)
        if nb > 1: orden = [int(z) for z in rng_pista.permutation(nb)]
        else: orden = list(range(nb))
        foto = tuple((b.id, b.pos, objs.get(b.pos), b.ult_mordida) for b in cuerpos)
        pend = []
        # ---------------- fase A (igual que v1, sin diag)
        for j in orden:
            b = cuerpos[j]; l = lin[b.lin]; c = b.c; o = b.obs
            b.vol_kk = None
            o['t'] = t; o['pos'] = b.pos; o['E'] = b.E; o['Ag'] = b.Ag; o['cuerpos'] = foto; o['pizarra'] = piz_t
            a = c.actua(o)
            mov = int(a.get('mov', 0))
            if mov not in (-1, 0, 1): raise SystemExit(f"PISTA2: {b.id} mov={mov} (solo -1, 0, +1)")
            es = a.get('escribe')
            if es is not None:
                if pizarra: pend.append((t, b.id, P._valida_escritura(es)))
                else: n_escr_desc += 1
            b.pos = (b.pos + mov) % L; pos = b.pos
            res = dict(t=t, pos=pos, letra=None, mordio=False, dS=None)
            b.ult_mordida = None
            if pos in objs:
                kk = objs[pos]; mordio = bool(a.get('muerde', False)); q = l.q(t)
                l.vis[kk][q] += 1
                res['letra'] = kk
                if mordio:
                    _dS = EFECTO[VAL_VIVO[kk]]
                    b.E = min(b.E + _dS[0], 1.5); b.Ag = min(b.Ag + _dS[1], 1.5)
                    l.mord[kk][q] += 1
                    if kk == 'B': b.tB = t
                    elif kk == 'D': b.tD = t
                    b.ult_mordida = kk
                    if kk in ('B', 'D') and sum(l.mord[kk]) > 1: b.vol_kk = kk   # ENMIENDA 6 (fisica; no discrimina, ERR-103)
                    quita(pos)
                    res['mordio'] = True; res['dS'] = tuple(_dS)
            c.resultado(res)
        # ---------------- costos
        for b in cuerpos:
            b.E -= M['costo']; b.Ag -= M['costo_a']
        # ---------------- olvido (ERR-98: esc sorteos por paso)
        olv = []
        for _o in range(esc):
            if rng.random() < M['olvido'] and objs:
                _dx = list(objs)[int(rng.integers(len(objs)))]; quita(_dx); olv.append(_dx); olv_n += 1
        olv = tuple(olv)
        if not inst:   # P7 quimiostato: llegadas a tasa fija, banco de a lo sumo 1 objeto pendiente
            banco[0] = min(banco[0] + r_paso, 1.0 + r_paso)
            while banco[0] >= 1.0:
                banco[0] -= 1.0
                if len(objs) < M['nobj']:
                    while True:
                        x2 = int(rng.integers(L))
                        if x2 not in objs: objs[x2] = P.TIPOS[int(rng.integers(len(P.TIPOS)))]; break
                    llegadas[0] += 1
                else: perdidas[0] += 1
        # ---------------- fase B
        nuevos = []; muertos = False
        for j in orden:
            b = cuerpos[j]; l = lin[b.lin]; c = b.c; i = b.lin
            c.fin_paso(dict(t=t, olvido=olv))
            if b.E <= 0 or b.Ag <= 0:
                por_E = b.E <= 0
                _causa = ('energia' if por_E else 'agua')
                cz = (('veneno' if t - b.tB < P.W_CAUSA else 'hambre') if por_E else ('sal' if t - b.tD < P.W_CAUSA else 'sed'))
                l.causas[cz] += 1
                if b.vol_kk == ('B' if por_E else 'D'): l.muertes_vol += 1
                l.deaths += 1; l.mnec[0 if por_E else 1] += 1
                edad = t - b.tn
                c.muere(dict(t=t, causa=_causa, causa_juez=cz, edad=edad, hijos=b.hijos))
                vd = 0
                campo = VOL_DECL.get(l.etq)
                if campo is not None and hasattr(c, 'salida'):
                    vd = int(bool(dict(c.salida()).get(campo, 0)))
                l.vol_decl += vd
                if len(l.vidas) < 100000: l.vidas.append(edad)
                registra(b, t, CAUSAS.index(cz), vd)
                b.vivo = False; l.vivos -= 1; total -= 1; muertos = True
                if b.pc is not None: b.pc.hvivos -= 1
                id2lin.pop(b.id, None); b.c = None; b.obs = None   # libera el cerebro del muerto
                if l.vivos > 0: continue
                # P3: extincion -> fundador limpio en el LUGAR del muerto
                l.nac += 1
                if l.nac >= 100000: raise SystemExit('PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)')
                l.fund += 1
                if len(l.tfund) < 200: l.tfund.append(t)
                cnew = mods[i][1].crea(ctx_de(i, rngs_fund[i], ids[i]))
                F = Cuerpo(i, l.nac, 0, -1, t, cnew, ids[i], vista, int(rngs_muerte[i].integers(L)), M['dote'], 1)
                cuerpos[j] = F; b = F; c = cnew; l.vivos = 1; total += 1; id2lin[F.id] = i
            # ventana de viabilidad (reproduccion)
            if b.E >= M['rep_umbral'] and b.Ag >= M['rep_umbral']:
                if b.gv == 0: b.gv0 = t
                b.gv += 1; l.pv += 1
            else: b.gv = (b.gv if rep_acum else 0)
            if b.gv >= M['rep_X']:
                if hasattr(c, 'quiere_parir') and not c.quiere_parir(dict(t=t, E=b.E, Ag=b.Ag, cola=l.vivos - 1,
                                                                       vivos_linaje=l.vivos, hijos_vivos=b.hvivos)):
                    b.gv = 0; l.vetos += 1
                elif total >= tope_cuerpos:
                    b.gv = 0; l.bloq += 1
                    if t_tope is None: t_tope = t
                else:
                    l.desc += 1; b.gv = 0; b.hijos += 1; b.hvivos += 1
                    b.E -= M['dote']; b.Ag -= M['dote']
                    mem = c.al_parir(dict(t=t, k=l.desc))
                    l.nac += 1; k = l.nac
                    if k >= 100000: raise SystemExit('PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)')
                    hid = f"{ids[i]}/{k}"
                    ch = mods[i][1].crea(ctx_de(i, SS(i, 'cuerpo', k), hid))
                    ch.nace(dict(t=t, k=k, fundador=False, memoria=mem, rng_hijo=SS(i, 'hijo', k), padre=b.id))
                    H = Cuerpo(i, k, b.gen + 1, b.k, t, ch, hid, vista, b.pos, M['dote'], 0, pc=b)
                    nuevos.append(H); l.vivos += 1; total += 1; id2lin[hid] = i
                    if total > max_vivos: max_vivos = total
        if muertos or nuevos:
            cuerpos = [b for b in cuerpos if b.vivo] + nuevos
        # ---------------- pizarra
        if pend:
            for e in pend:
                piz.append(e); piz_log.append([e[0], e[1], list(e[2])])
                le = lin[id2lin[e[1]]] if e[1] in id2lin else None
                if le is not None:
                    le.escrituras += 1
                    if telem and len(le.escr) < P.MAX_ESCRITURAS_TELEM: le.escr.append([e[0], list(e[2])])
            piz_t = tuple(piz)

    for l in lin: l.tam.append(l.vivos)
    tam_total.append(total)
    # ---------------------------------------------------------------- salida (ERR-96: fisica ARRIBA, carro en d['carro'])
    vivos_de = {i: [b for b in cuerpos if b.lin == i] for i in range(n)}
    out = []
    for i, l in enumerate(lin):
        vd_vivos = 0
        campo = VOL_DECL.get(l.etq)
        for b in vivos_de[i]:
            v = 0
            if campo is not None and hasattr(b.c, 'salida'): v = int(bool(dict(b.c.salida()).get(campo, 0)))
            vd_vivos += v
            registra(b, -1, -1, v)
        car = {}
        if vivos_de[i] and hasattr(vivos_de[i][0].c, 'salida'): car = dict(vivos_de[i][0].c.salida())
        d = dict(mord=l.mord, vis=l.vis, deaths=l.deaths, muertes_nec=list(l.mnec), descendientes=l.desc,
                 nacimientos=l.desc, fundadores=l.fund, t_fund=list(l.tfund), vetos=l.vetos, bloqueados=l.bloq,
                 pasos_viables=l.pv, vidas_muertos=list(l.vidas), vivos_final=l.vivos, tam=list(l.tam),
                 individuos=l.ind, T_efectivo=T, dote=M['dote'], muerte_real=1)
        d['_carrera'] = dict(id=l.id, indice=i, etiqueta=l.etq, causas=dict(l.causas), escrituras=l.escrituras, escr=l.escr,
                             muertes_vol=l.muertes_vol, muertes_vol_decl=l.vol_decl, vol_decl_vivos_T=vd_vivos,
                             vol_decl_campo=campo)
        d['carro'] = car
        out.append(d)
    return dict(linajes=out, pizarra_log=piz_log,
                pista=dict(seed=seed, T=T, n=n, ids=ids, solapadas=1, compat=0, pizarra=int(pizarra), rep_acum=int(rep_acum),
                           escala=int(escala), L=L, nobj=M['nobj'], olvidos=olv_n, mundo_n=mundo_n,
                           fundador_limpio='siempre (P3)', reposicion=reposicion, r_paso=(None if inst else r_paso),
                           llegadas=llegadas[0], llegadas_perdidas=perdidas[0], pisos=pisos[0], tope_cuerpos=tope_cuerpos, t_tope=t_tope, max_vivos=max_vivos,
                           bloqueados=sum(l.bloq for l in lin), muestra=muestra, tam_total=tam_total,
                           comp_mundo={k: round(comp[k] / T, 4) for k in P.TIPOS}, nobj_medio=round(nobj_suma / T, 3), nobj_final=len(objs),
                           escrituras_descartadas=n_escr_desc, pizarra_n=len(piz_log),
                           pizarra_final=[[e[0], e[1], list(e[2])] for e in piz],
                           rng_mundo_estado=P._estado(rng)))
