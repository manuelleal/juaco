"""construye_cruce.py — construye POR ANCLAS el motor y el carro del bloque organelos/cruce.

MISION: llegar a la AGI por este camino. Pregunta (director, 24-sep): ¿el bicho REAL (v14.3 en la pista, sin tocar su cerebro) cruza
R0 real >= 0.90 en la pista de la carrera POR SELECCION NATURAL de GENES DE CABLEADO (senales internas presentes -> decisiones que el
cuerpo ya tiene), sin politica escrita a mano ni por un LLM?

ORIGENES (solo se LEEN; sha16 fijados; cada ancla debe aparecer EXACTAMENTE una vez o el constructor ABORTA):
  experimentos/carrera_escuderias/pista.py            (SHA_PISTA)  -> motor_cruce.py  (la pista de la carrera + genoma por cuerpo,
                                                                     error de copia en el parto, vivero hasta el corte)
  experimentos/tronco_v14_3/carros_v143/V143.py        (SHA_V143)   -> carros/CRUCE.py (v14.3 en la pista + lectura del genoma)
Con cruce=None el motor es la pista BIT A BIT; con el genoma en 0 (o sin ctx['cruce']) el carro es V143 BIT A BIT
(identidad_cruce.py). Nada fuera de experimentos/organelos/cruce/ se escribe.

    python experimentos/organelos/cruce/construye_cruce.py [--verifica]
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIG_PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'pista.py')
ORIG_V143 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143', 'V143.py')
SHA_PISTA = '9f47c65e438e0ff4'
SHA_V143 = '2a03048a7f1525e5'
SAL_MOTOR = os.path.join(AQUI, 'motor_cruce.py')
SAL_CARRO = os.path.join(AQUI, 'carros', 'CRUCE.py')


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


def aplica(txt, cambios, nombre):
    for i, (ancla, nuevo) in enumerate(cambios):
        c = txt.count(ancla)
        if c != 1: raise SystemExit(f"CONSTRUYE {nombre}: el ancla {i} aparece {c} veces (debe ser 1): {ancla[:90]!r}")
        txt = txt.replace(ancla, nuevo)
    return txt


# =================================================================================================== MOTOR (desde pista.py)
DOC_MOTOR = '''"""motor_cruce.py — CONSTRUIDO por experimentos/organelos/cruce/construye_cruce.py desde experimentos/carrera_escuderias/pista.py
(sha 9f47c65e438e0ff4). NO editar a mano. Con cruce=None es la PISTA DE LA CARRERA BIT A BIT (arnes identidad_cruce.py).

CRUCE (organelos/cruce, 24-sep): con cruce=dict(...) la pista agrega, y SOLO esto:
 C1 GENOMA POR CUERPO. Cada cuerpo lleva un genoma de NG enteros en [-g_max, g_max] (genes de CABLEADO; los lee el carro CRUCE)
    y n_sombra genomas SOMBRA que mutan igual y viajan por la misma genealogia pero NUNCA se expresan (la deriva de referencia).
    Todos los fundadores de t = 0 nacen con el genoma en 0 (APAGADO) salvo genoma0 (SOLO el arnes).
 C2 ERROR DE COPIA EN EL PARTO. En cada parto el hijo que entra a la cola lleva muta(genoma del padre) (rng propio [seed, i, 16, k],
    k = numero de parto del linaje); cada gen cambia +-1 con probabilidad p_mut. Cuando el hijo nace de la cola, su genoma es ese.
    Con donante='azar' (control AZAR: mutacion SIN seleccion) el genoma del hijo sale de una entrada AL AZAR del banco, mutada, y el
    banco guarda el genoma NUEVO: el genoma nunca influye en su propia copia (la regla de motor_eco3, sin la version con vivos).
 C3 VIVERO = CRIA (declarado), SOLO con t < t_corte: si un linaje se extingue, el fundador (instancia nueva, ENMIENDA 5) lleva un
    genoma sacado del BANCO (anillo de los ultimos banco_max genomas DONANTES de un parto: el del PADRE con 'padre'), mutado.
    Desde t_corte NADIE repone nada del banco: el fundador que la pista pone es el limpio de siempre (instancia NUEVA, sin memoria
    del linaje) con el GENOTIPO de su linaje (el del ultimo cuerpo), igual que el fundador de O1 es una instancia nueva del codigo O1.
    genomas_ini (la LECTURA): los linajes arrancan con esos genomas (una muestra del banco del corte) en vez de 0.
 C4 LESION (control DESFASADO): lesion_desde viaja al carro; el carro decide con senales internas de un paso pasado al azar.
 La seleccion es SOLO la de la pista: el que vive y pare llena la cola (FIFO) de su linaje y el banco (antes del corte).
 Telemetria: salida['cruce'] (mutaciones, distancia hijo-padre, foto del genoma cada `cada` pasos, banco y sombras en el corte y al final).
Lo que sigue es el docstring del origen.

'''

PREP_MOTOR = '''
# ============================================================================ CRUCE (organelos/cruce) -- solo con cruce=dict
ETQ.update(mut=16, sombra=17, banco=18, donante=19, cable=20, mutf=21, sombraf=22)
CRUCE_DEF = dict(NG=None, p_mut=0.0, t_corte=None, banco_max=0, donante='padre', n_sombra=0, lesion_desde=None, genoma0=None,
                 g_max=4, cada=10000, genomas_ini=None)


def _cruce_prep(cruce, n, fundador_limpio, T):
    if cruce is None: return None
    mal = sorted(set(cruce) - set(CRUCE_DEF))
    if mal: raise SystemExit(f"CRUCE: claves desconocidas {mal}")
    CR = dict(CRUCE_DEF); CR.update(cruce)
    if not fundador_limpio: raise SystemExit("CRUCE: exige fundador_limpio=1 (ENMIENDA 5)")
    if not isinstance(CR['NG'], int) or CR['NG'] < 1: raise SystemExit(f"CRUCE: NG invalido {CR['NG']!r}")
    if CR['donante'] not in ('padre', 'azar'): raise SystemExit(f"CRUCE: donante invalido {CR['donante']!r}")
    if CR['t_corte'] is None or not 0 <= int(CR['t_corte']) <= T: raise SystemExit(f"CRUCE: t_corte invalido {CR['t_corte']!r}")
    if not 0.0 <= float(CR['p_mut']) <= 1.0: raise SystemExit("CRUCE: p_mut fuera de [0, 1]")
    if CR['lesion_desde'] is not None and not 0 <= int(CR['lesion_desde']) <= T: raise SystemExit("CRUCE: lesion_desde invalido")
    if CR['genoma0'] is not None and len(CR['genoma0']) != CR['NG']: raise SystemExit("CRUCE: genoma0 de largo distinto a NG")
    gi = CR['genomas_ini']
    if gi is not None and (len(gi) != n or any(len(g) != CR['NG'] for g in gi)): raise SystemExit("CRUCE: genomas_ini debe traer n genomas de NG genes")
    CR.update(banco=[], ncable=[0] * n, n_mut=0, n_mut_s=0, n_partos=0, n_refund=0, n_fund_post=0, ham=[0] * 12,
              corte=None, gen_t=[], tel=[dict() for _ in range(n)], buf=[None] * n)
    return CR


def _muta(g, r, p, gmax):
    """Error de copia: cada gen cambia +-1 (mitad y mitad) con probabilidad p, dentro de [-gmax, gmax]. Consume SIEMPRE 2*NG numeros."""
    u = r.random(len(g)); z = r.random(len(g))
    h = np.clip(g + (u < p) * np.where(z < 0.5, 1, -1), -gmax, gmax).astype(np.int64)
    return h, int((h != g).sum())

'''

BLOQUE_RUN = '''
    # ======== CRUCE (organelos/cruce): genes de cableado por cuerpo, error de copia en el parto, vivero (cria) hasta t_corte.
    # cruce=None -> NINGUNA linea de este bloque cambia nada: la pista es la de la carrera BIT A BIT (arnes identidad_cruce.py).
    CR = _cruce_prep(cruce, n, fundador_limpio, T)
    if CR is not None:
        for l in lin:
            l.G = np.zeros(CR['NG'], np.int64); l.S = np.zeros((int(CR['n_sombra']), CR['NG']), np.int64)
            if CR['genoma0'] is not None: l.G[:] = CR['genoma0']
            if CR['genomas_ini'] is not None: l.G[:] = CR['genomas_ini'][l.i]
        if CR['banco_max']: CR['banco'] = [(l.G.copy(), l.S.copy()) for l in lin]

    def _cx(i, t0):
        if CR is None: return {}
        CR['ncable'][i] += 1
        return {'cruce': dict(genoma=[int(x) for x in lin[i].G], t0=int(t0), lesion_desde=CR['lesion_desde'],
                              rng_cable=SS(i, 'cable', CR['ncable'][i]), buf=CR['buf'][i])}

    def _info_gen(i):
        return {} if CR is None else {'genoma': [int(x) for x in lin[i].G]}

    def _al_banco(g, s):
        CR['banco'].append((g.copy(), s.copy()))
        if len(CR['banco']) > CR['banco_max']: CR['banco'].pop(0)

    def _sombras(sd, rs):
        s = sd.copy()
        for q in range(s.shape[0]):
            s[q], _nm = _muta(sd[q], rs, float(CR['p_mut']), CR['g_max']); CR['n_mut_s'] += _nm
        return s

    def _parto(i, l, t):
        if CR is None: return {}
        k = l.desc
        if CR['donante'] == 'azar' and CR['banco']:
            gd, sd = CR['banco'][int(SS(i, 'donante', k).integers(len(CR['banco'])))]
        else: gd, sd = l.G, l.S
        g, nm = _muta(gd, SS(i, 'mut', k), float(CR['p_mut']), CR['g_max'])
        s = _sombras(sd, SS(i, 'sombra', k))
        CR['n_mut'] += nm; CR['n_partos'] += 1
        CR['ham'][min(int((g != l.G).sum()), 11)] += 1          # distancia hijo-padre (herencia: casi siempre 0-2 con 'padre')
        if CR['banco_max']: _al_banco(gd, sd) if CR['donante'] == 'padre' else _al_banco(g, s)
        return {'G': g, 'S': s}

    def _gen_nace(i, l, _m, t, c):
        _v = getattr(c, '_crs', None)                            # telemetria del carro que se va (fundador limpio = instancia nueva)
        if _m is None and _v:
            for _k, _x in _v.items(): CR['tel'][i][_k] = CR['tel'][i].get(_k, 0) + _x
        if _m is None and CR['lesion_desde'] is not None:   # control DESFASADO: la historia de senales es del LINAJE (pasa al fundador)
            CR['buf'][i] = (list(getattr(c, '_buf', [])), int(getattr(c, '_bi', 0)))
        if _m is not None:
            l.G = _m['G']; l.S = _m['S']; return
        if t < CR['t_corte'] and CR['banco']:                    # C3 VIVERO (cria): fundador con genoma del banco, mutado
            gb, sb = CR['banco'][int(SS(i, 'banco', l.nac).integers(len(CR['banco'])))]
            l.G, nm = _muta(gb, SS(i, 'mutf', l.nac), float(CR['p_mut']), CR['g_max']); CR['n_mut'] += nm
            l.S = _sombras(sb, SS(i, 'sombraf', l.nac)); CR['n_refund'] += 1
            if CR['donante'] == 'azar' and CR['banco_max']: _al_banco(l.G, l.S)
        elif t < CR['t_corte']:                                  # cria sin banco (no se usa en el corredor): genoma inicial
            l.G = np.zeros(CR['NG'], np.int64); l.S = np.zeros((int(CR['n_sombra']), CR['NG']), np.int64)
            if CR['genoma0'] is not None: l.G[:] = CR['genoma0']
        else:                                                    # desde el corte: fundador limpio con el GENOTIPO del linaje
            CR['n_fund_post'] += 1                               # (l.G y l.S quedan los del ultimo cuerpo; nadie repone del banco)

    def _foto(tt, banco):
        G = np.array([l.G for l in lin], float); f = dict(t=int(tt), vivos=[[int(x) for x in l.G] for l in lin],
                                                            vivos_media=[round(float(x), 4) for x in G.mean(0)])
        if banco and CR['banco']:
            B = np.array([g for g, _ in CR['banco']], float); S = np.array([s for _, s in CR['banco']], float)
            f.update(banco_n=len(CR['banco']), banco=[[int(x) for x in g] for g, _ in CR['banco']],
                     banco_media=[round(float(x), 4) for x in B.mean(0)], banco_nz=[round(float(x), 4) for x in (B != 0).mean(0)])
            if S.size:
                f.update(sombra_media=[[round(float(x), 4) for x in S[:, q, :].mean(0)] for q in range(S.shape[1])],
                         sombra_nz=[[round(float(x), 4) for x in (S[:, q, :] != 0).mean(0)] for q in range(S.shape[1])])
        return f

    def _cruce_out():
        if CR is None: return {}
        tel = []
        for i, c in enumerate(cars):
            d = dict(CR['tel'][i])
            for _k, _x in (getattr(c, '_crs', None) or {}).items(): d[_k] = d.get(_k, 0) + _x
            tel.append(d)
        return {'cruce': dict(cfg={k: CR[k] for k in CRUCE_DEF if k != 'genoma0'}, genoma0=(None if CR['genoma0'] is None else list(CR['genoma0'])),
                              n_mut=CR['n_mut'], n_mut_sombra=CR['n_mut_s'], n_partos=CR['n_partos'], n_refund=CR['n_refund'],
                              n_fund_post=CR['n_fund_post'], ham=list(CR['ham']), corte=CR['corte'], gen_t=CR['gen_t'],
                              final=_foto(T, True), tel_carro=tel)}
'''

CAMBIOS_MOTOR = [
    ('"""pista.py — LA PISTA DE LA CARRERA', DOC_MOTOR + 'pista.py — LA PISTA DE LA CARRERA'),
    ("def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, fundador_limpio=0):",
     PREP_MOTOR.lstrip('\n') + "\n" +
     "def run(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None, fundador_limpio=0, cruce=None):"),
    ("    lin = [Linaje(i, ids[i], T, M, rep_acum) for i in range(n)]\n",
     "    lin = [Linaje(i, ids[i], T, M, rep_acum) for i in range(n)]\n" + BLOQUE_RUN),
    ("    def ctx_de(i):\n", "    def ctx_de(i, t0=0):\n"),
    ("cupo=CUPO, ancho=ANCHO, fabrica=cfg_fabrica())", "cupo=CUPO, ancho=ANCHO, fabrica=cfg_fabrica(), **_cx(i, t0))"),
    ("                if l.esfund and fundador_limpio:   # ENMIENDA 5",
     "                if CR is not None: _gen_nace(i, l, _m, t, c)   # CRUCE: genoma del que nace (cola, banco o 0)\n"
     "                if l.esfund and fundador_limpio:   # ENMIENDA 5"),
    ("cars[i] = mods[i][1].crea(ctx_de(i)); c = cars[i]; instancias[i] += 1",
     "cars[i] = mods[i][1].crea(ctx_de(i, t)); c = cars[i]; instancias[i] += 1"),
    ("rng_hijo=hijo(i, l.nac)))", "rng_hijo=hijo(i, l.nac), **_info_gen(i)))"),
    ("l.cola.append(dict(dote=M['dote'], mem=c.al_parir(dict(t=t, k=l.desc))))",
     "l.cola.append(dict(dote=M['dote'], mem=c.al_parir(dict(t=t, k=l.desc)), **_parto(i, l, t)))"),
    ("        # ---------------- pizarra\n",
     "        if CR is not None:   # CRUCE: foto del genoma cada `cada` pasos y en el corte (lo que examina el runner)\n"
     "            if CR['cada'] and (t + 1) % CR['cada'] == 0: CR['gen_t'].append(_foto(t + 1, False))\n"
     "            if t + 1 == CR['t_corte']: CR['corte'] = _foto(t + 1, True)\n"
     "        # ---------------- pizarra\n"),
    ("    return dict(linajes=out, pizarra_log=piz_log,", "    return dict(linajes=out, pizarra_log=piz_log, **_cruce_out(),"),
]

# =================================================================================================== CARRO (desde V143.py)
DOC_CARRO = '''"""CRUCE.py — organelos/cruce: v14.3 EN LA PISTA (V143, sin tocar su cerebro) + GENES DE CABLEADO que la seleccion puede prender.
CONSTRUIDO por experimentos/organelos/cruce/construye_cruce.py desde experimentos/tronco_v14_3/carros_v143/V143.py (sha 2a03048a7f1525e5).
NO editar a mano. Sin ctx['cruce'] o con el genoma en 0 NINGUNA linea nueva se ejecuta: es V143 BIT A BIT (identidad_cruce.py).

EL CABLEADO (generico, nace APAGADO): tres decisiones que el cuerpo YA tiene reciben una suma lineal de SEIS senales internas
PRESENTES, con pesos enteros (genes) en [-4, 4]:
  senales s = (sesgo 1, reserva min(E,Ag)/1.5, la otra max(E,Ag)/1.5, ventana de parto recorrida, edad del cuerpo /2000, hijos en cola /4)
  contexto  = como el organismo VALORA la letra con sus propias dos filas (la MISMA lectura del FILTRO de v14.3):
              bueno (valor > 0 en la fila activa) / malo (algun valor < 0 y no bueno) / neutro (el resto, incluye lo desconocido)
  BOCA : logit de morder  += PASO_BOCA * gen_boca[contexto de la letra que pisa] . s
  PATAS: objetivo = el de menor distancia - PASO_PATA * [(gen_pata_act . s) * valor(letra, fila activa) + (gen_pata_otra . s) * valor(letra,
         la otra fila)]: la atraccion por lo que el propio organismo valora, con una ganancia que depende del estado (genes 0: el mas cercano)
  PARTO: pare en esta ventana si gen_parto . s >= 0 (con genes 0: siempre, como V143)
Ninguna regla de O1 ni de O3 esta escrita: no hay MARGEN, PRUEBA, PISO, huecos, rareza, penalizacion por vecinos ni muerte programada;
todas las combinaciones de signo son igual de alcanzables por la mutacion (+-1). Lo que el genoma haga lo elige la pista.
CONTROL DESFASADO (lesion_desde): desde ese paso las SEIS senales se leen de un paso pasado al azar (ultimos 2000 del linaje, como
subida_n9; la historia pasa al fundador del mismo linaje); el contexto (la valoracion de la letra) sigue presente. Si el ganador
cruza por leer su estado presente, debe caer.
Lo que sigue es el docstring del origen.

'''

CONST_CARRO = '''
# ================================================================ CRUCE (organelos/cruce) -- GENES DE CABLEADO (nacen en 0)
SEN = ('sesgo', 'reserva', 'otra', 'ventana', 'edad', 'cola')
CTX = ('bueno', 'neutro', 'malo')
NS = len(SEN); NC = len(CTX)
FILAS = ('act', 'otra')              # patas: ganancia sobre el valor de la letra en la fila activa y en la otra
NG = NC * NS + 2 * NS + NS            # boca[ctx][sen] + pata[fila][sen] + parto[sen] = 36
NOMBRES_GEN = tuple([f"boca_{c}_{s}" for c in CTX for s in SEN] + [f"pata_{f}_{s}" for f in FILAS for s in SEN] +
                    [f"parto_{s}" for s in SEN])
PASO_BOCA = 1.0     # logit de morder por unidad de gen y de senal
PASO_PATA = 8.0     # celdas de cercania que gana (o pierde) un objetivo por unidad de gen, de senal y de valor
NIV_ESC = 1.5       # techo de E y Ag en la pista (min(., 1.5))
EDAD_ESC = 2000.0   # la edad satura en 1 a los 2000 pasos
COLA_ESC = 4.0      # los hijos en cola saturan en 1 con 4
BUF_LES = 2000      # control DESFASADO: ventana del linaje de la que se sortea el paso pasado (como subida_n9)
'''

METODOS_CARRO = '''
    # ================================================================ CRUCE: lectura del genoma (nada de esto corre con el genoma en 0)
    def _cr_init(self, ctx):
        c = ctx.get('cruce')
        self._cr = c; self._on = False; self._crp = None; self._crs = None; self._cola = 0
        if c is None: return
        self._t0 = int(c['t0']); self._les = c['lesion_desde']; self._rc = c['rng_cable']; self._buf = []; self._bi = 0
        if c.get('buf'): self._buf = list(c['buf'][0]); self._bi = int(c['buf'][1])   # DESFASADO: la historia del linaje
        self._crs = dict(cuerpos=1, cuerpos_on=0, pasos_on=0, boca_dec=0, boca_dif=0, pata_dec=0, pata_dif=0, partos_dec=0,
                         vetos_parto=0, lesion_lecturas=0)
        self._pon(c['genoma'])

    def _pon(self, g):
        g = [int(x) for x in g]; self._g = g; self._on = any(g); self._crp = None
        self._wb = [g[c * NS:(c + 1) * NS] for c in range(NC)]
        self._wp = [g[NC * NS + f * NS:NC * NS + (f + 1) * NS] for f in range(2)]
        self._wv = g[NC * NS + 2 * NS:]
        self._boca_on = any(any(w) for w in self._wb); self._pata_on = any(any(w) for w in self._wp); self._parto_on = any(self._wv)
        if self._on: self._crs['cuerpos_on'] += 1

    def _senal(self, t, E, Ag):
        lo = min(E, Ag); hi = max(E, Ag)
        return (1.0, min(max(lo, 0.0), NIV_ESC) / NIV_ESC, min(max(hi, 0.0), NIV_ESC) / NIV_ESC, min(self._avent / self._aX, 1.0),
                min(max(t - self._t0, 0) / EDAD_ESC, 1.0), min(self._cola, COLA_ESC) / COLA_ESC)

    def _desfasa(self, t, s):
        """CONTROL DESFASADO: guarda la senal presente del linaje (siempre) y, desde lesion_desde y solo si el genoma lee algo,
        devuelve la de un paso pasado al azar de los ultimos BUF_LES del linaje."""
        if t >= self._les - BUF_LES:
            if len(self._buf) < BUF_LES: self._buf.append(s)
            else: self._buf[self._bi] = s; self._bi = (self._bi + 1) % BUF_LES
        if self._on and t >= self._les and self._buf:
            self._crs['lesion_lecturas'] += 1
            return self._buf[int(self._rc.integers(len(self._buf)))]
        return s

    def _cr_paso(self, obs, na):
        t = int(obs['t']); s = self._senal(t, float(obs['E']), float(obs['Ag']))
        if self._les is not None: s = self._desfasa(t, s)
        if not self._on: return
        self._crs['pasos_on'] += 1; v = self._v3v
        cx = {k: (0 if v[k][na] > 0 else (2 if min(v[k]) < 0 else 1)) for k in self.PAT}
        self._cx = cx
        if self._pata_on:
            ga, go = [PASO_PATA * sum(w[j] * s[j] for j in range(NS)) for w in self._wp]
            self._crp = {k: ga * v[k][na] + go * v[k][1 - na] for k in self.PAT}
        if self._boca_on: self._db = [PASO_BOCA * sum(w[j] * s[j] for j in range(NS)) for w in self._wb]

    def _cr_pb(self, Vb, kk):
        pb0 = 1 / (1 + np.exp(-Vb / .3)); self._pb0 = pb0
        if not self._boca_on: return pb0
        self._crs['boca_dec'] += 1
        return 1 / (1 + np.exp(-(Vb / .3 + self._db[self._cx[kk]])))

    def _see_cr(self, pos, objs, t, contar):
        """_see de V143 con el objetivo elegido por (distancia - bono del cableado); mismos filtros y mismo orden de respaldo."""
        L = self.L; bono = self._crp; best = None; nn = None   # nn = lo que V143 habria elegido (el mas cercano, mismo orden)
        for x, k in objs.items():
            if self.MEMORIA_RECHAZO and self._rech.get(x, -1) > t: continue
            if FILTRO and k in self._v3o: continue
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr); sc = d - bono[k]
            if best is None or sc < best[3]: best = (d, k, dl < dr, sc, x)
            if nn is None or d < nn[0]: nn = (d, k, dl < dr, d, x)
        if best is None:
            if contar: self.sin_objetivo[self._q(t)] += 1
            for x, k in objs.items():
                if FILTRO and k in self._v3o: continue
                dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr); sc = d - bono[k]
                if best is None or sc < best[3]: best = (d, k, dl < dr, sc, x)
                if nn is None or d < nn[0]: nn = (d, k, dl < dr, d, x)
        if best is None and FILTRO:
            self._v3['todo_obst'] += 1
            for x, k in objs.items():
                dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
                if best is None or d < best[0]: best = (d, k, dl < dr, d, x)
            nn = best
        if best is None: return None
        if contar: self._crs['pata_dec'] += 1; self._crs['pata_dif'] += int(best[4] != nn[4])   # otro objeto que el de V143
        return best[:3]

    def quiere_parir(self, info):
        """CRUCE: parir en esta ventana o esperar. Sin genes de parto: SIEMPRE (== V143, que no la define)."""
        self._cola = int(info['cola'])
        if self._cr is None or not self._on or not self._parto_on:
            self._cola += 1; return True
        t = int(info['t']); s = self._senal(t, float(info['E']), float(info['Ag']))
        if self._les is not None and t >= self._les and self._buf:
            self._crs['lesion_lecturas'] += 1; s = self._buf[int(self._rc.integers(len(self._buf)))]
        ok = sum(self._wv[j] * s[j] for j in range(NS)) >= 0
        self._crs['partos_dec'] += 1; self._crs['vetos_parto'] += int(not ok); self._cola += int(ok)
        return ok

    def _cr_nace(self, info):
        self._cola = max(0, self._cola - 1)
        if self._cr is None: return
        self._t0 = int(info['t']); self._crs['cuerpos'] += 1
        self._pon(info['genoma'])

    def _cr_salida(self):
        return dict(genoma=list(self._g), on=bool(self._on), nombres=list(NOMBRES_GEN), **self._crs)

'''

CAMBIOS_CARRO = [
    ('"""V143.py — tronco_v14_3', DOC_CARRO + 'V143.py — tronco_v14_3'),
    ("CACHE = 1   # tras el humo: las dos filas por letra solo cambian al morder o al nacer -> se guardan hasta entonces (arnes: CACHE 0 == 1 bit a bit)\n",
     "CACHE = 1   # tras el humo: las dos filas por letra solo cambian al morder o al nacer -> se guardan hasta entonces (arnes: CACHE 0 == 1 bit a bit)\n"
     + CONST_CARRO),
    ("        self._v3_init(ctx)\n", "        self._v3_init(ctx)\n        self._cr_init(ctx)   # CRUCE\n"),
    ("    def _see(self, pos, objs, t, contar=False):\n        L = self.L; best = None\n",
     "    def _see(self, pos, objs, t, contar=False):\n        if self._crp is not None: return self._see_cr(pos, objs, t, contar)   # CRUCE: genes de pata prendidos\n"
     "        L = self.L; best = None\n"),
    ("        if FILTRO: self._v3_prep(objs, _na)\n",
     "        if FILTRO: self._v3_prep(objs, _na)\n"
     "        if self._cr is not None and (self._on or self._les is not None): self._cr_paso(obs, _na)   # CRUCE\n"),
    ("            pb = 1 / (1 + np.exp(-Vb / .3)); _u9 = rng.random(); mordio = bool(_u9 < pb)\n",
     "            pb = (self._cr_pb(Vb, kk) if self._on else 1 / (1 + np.exp(-Vb / .3))); _u9 = rng.random(); mordio = bool(_u9 < pb)   # CRUCE: boca\n"
     "            if self._on and self._boca_on: self._crs['boca_dif'] += int((_u9 < self._pb0) != mordio)\n"),
    ("        if OPCION: self._apr_nace(info)\n", "        if OPCION: self._apr_nace(info)\n        self._cr_nace(info)   # CRUCE\n"),
    ("    # ================================================================ APR (camino A): LA OPCION APRENDIDA\n",
     METODOS_CARRO.lstrip('\n') + "    # ================================================================ APR (camino A): LA OPCION APRENDIDA\n"),
    ("            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {}))",
     "            **({'v143': self._v3_salida()} if (DESAMB or FILTRO) else {}),\n"
     "            **({'cruce': self._cr_salida()} if self._cr is not None else {}))"),
]


def todas():
    for ruta, sha in ((ORIG_PISTA, SHA_PISTA), (ORIG_V143, SHA_V143)):
        b = open(ruta, 'rb').read()
        if h16b(b) != sha: raise SystemExit(f"CONSTRUYE: {ruta} sha {h16b(b)} != {sha} (el origen cambio)")
    motor = aplica(open(ORIG_PISTA, encoding='utf-8').read(), CAMBIOS_MOTOR, 'motor')
    carro = aplica(open(ORIG_V143, encoding='utf-8').read(), CAMBIOS_CARRO, 'carro')
    # El motor se importa desde ESTA carpeta: sus rutas a la carrera (cfg_fabrica, carros) deben seguir apuntando a carrera_escuderias.
    motor = aplica(motor, [("AQUI = os.path.dirname(os.path.abspath(__file__))\nRAIZ = os.path.dirname(os.path.dirname(AQUI))\n",
                            "AQUI = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "
                            "'experimentos', 'carrera_escuderias')   # CRUCE: la carrera (solo se LEE)\nRAIZ = os.path.dirname(os.path.dirname(AQUI))\n")],
                   'motor-rutas')
    return {SAL_MOTOR: motor.encode('utf-8'), SAL_CARRO: carro.encode('utf-8')}


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args()
    outs = todas()
    if a.verifica:
        dif = [os.path.relpath(r, AQUI) for r, b in outs.items() if not os.path.exists(r) or open(r, 'rb').read() != b]
        print('VERIFICA:', 'OK' if not dif else f'DIFIEREN {dif}'); sys.exit(1 if dif else 0)
    for r, b in outs.items():
        os.makedirs(os.path.dirname(r), exist_ok=True); open(r, 'wb').write(b)
        print(f"escrito {os.path.relpath(r, AQUI)} sha {h16b(b)} ({len(b)} bytes)")


if __name__ == '__main__':
    main()
