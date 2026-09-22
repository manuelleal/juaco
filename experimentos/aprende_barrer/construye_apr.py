"""construye_apr.py — construye por ANCLAS los carros del camino A (aprende_barrer) desde carros/FABRICA.py.

MISION: llegar a la AGI por este camino. Pregunta del director (22-sep, camino A): ¿puede un organismo que APRENDE
(FABRICA = brazo REL de la fase 9) descubrir por si mismo que morder lo malo le conviene (la "limpieza" que O1 trae
escrita a mano) y pasarlo al siguiente cuerpo del linaje?

Origen (solo se LEE): experimentos/carrera_escuderias/carros/FABRICA.py, sha16 fijado en SHA_FABRICA. Cada ancla
tiene que aparecer EXACTAMENTE una vez; si no, aborta. Se preservan los fines de linea (CRLF) del origen.
Genera, en experimentos/carrera_escuderias/carros/ (archivos NUEVOS; no toca ninguno existente):
  APR.py               MODO 'aprende'      (la opcion decide con su valor aprendido; se hereda por el linaje)
  APR_SIN_HERENCIA.py  MODO 'sin_herencia' (igual, pero cada cuerpo nuevo empieza con el valor de la opcion en cero)
  APR_AZAR.py          MODO 'azar'         (misma opcion, decide con probabilidad fija P_AZAR; placebo de "cuando")
Los tres difieren SOLO en las constantes MODO / P_AZAR (se verifica). P_AZAR se fija con --p_azar DESPUES de la
serie de APR (la tasa por oportunidad que APR termine aprendiendo); sin --p_azar, APR_AZAR aborta al crearse.
Con OPCION = 0 (constante de modulo) los tres son FABRICA bit a bit: lo prueba identidad_apr.py.

    python experimentos/aprende_barrer/construye_apr.py [--p_azar 0.xx] [--verifica]
    (--verifica: no escribe; comprueba que los archivos en disco son los que generaria)
"""
import argparse, hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CARROS = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros')
ORIGEN = os.path.join(CARROS, 'FABRICA.py')
SHA_FABRICA = '2ebee3e99ea5a33a'


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


CONSTANTES = '''
# ================================================================ APR (camino A, aprende_barrer) -- constantes
# OPCION = 0 -> este archivo es FABRICA bit a bit (arnes identidad_apr.py). MODO y P_AZAR son lo UNICO que cambia
# entre APR, APR_SIN_HERENCIA y APR_AZAR. ALFA_Q, GAMMA, BETA, R_*: hiperparametros del aprendizaje (NO umbrales de cuando
# limpiar; la decision sale de Q aprendido). Historia (PREREGISTRO_aprende.md): v1 humo 8001, v2 humo 8002 (GAMMA 0.99 -> 0.998,
# recompensa real, rasgo de ventana), v3 humo 8003 (la opcion CORRIGE la boca de FABRICA en vez de reemplazarla). Desde v3,
# congelados hasta la serie (v3 + telemetria de quitadas por edad / indice del cuerpo, sin tocar la conducta).
OPCION = 1
MODO = '{modo}'
P_AZAR = {p_azar}
ALFA_Q = 0.05      # paso del aprendizaje TD de los dos valores lineales Q(no morder), Q(morder)
GAMMA = 0.998      # descuento POR PASO (horizonte ~500 pasos = la ventana de parto)
BETA = 10.0        # temperatura de la politica: p(morder) = sigmoide(BETA * (Q_morder - Q_no))
R_PARTO = 1.0      # v2: recompensa REAL sentida: +1 cuando el cuerpo pare (al_parir), -1 cuando muere (terminal):
R_MUERTE = -1.0    #     el retorno sigue (nacimientos - muertes), la misma cantidad que mide H-1 (r = desc - muertes)
NF = 6             # rasgos: [1, u=min(E,Ag), u tras morder (con lo SENTIDO de esa letra), 0 bueno en el mundo, distancia al bueno,
                   #          progreso propio en la ventana de parto (pasos seguidos con E y Ag >= umbral / rep_X)]
BIN_EDAD = (50, 100, 200, 400, 800, 1600)          # edad del cuerpo al decidir (pasos desde que nacio)
BIN_GEN = (1, 5, 20, 50, 100, 200, 400)             # indice del cuerpo dentro del linaje (0 = el primero)
BIN_POST = (0.0, 0.3, 0.6, 1.0)                     # min(E,Ag) PREDICHO tras morder
'''

METODOS = '''
    # ================================================================ APR (camino A): LA OPCION APRENDIDA
    # Alcance de la opcion: SOLO cuando el cuerpo esta sobre una letra "mala conocida" (el linaje ya la mordio y lo que
    # SINTIO -el dS que la pista devuelve en resultado()- tiene alguna componente negativa). Ahi decide la opcion (v3):
    # logit p(morder) = logit(pb de la boca de FABRICA) + BETA * (Q1 - Q0), con el MISMO uniforme que FABRICA ya saco
    # (ningun sorteo extra). Con Q1 = Q0 (al nacer el linaje) muerde EXACTAMENTE cuando FABRICA morderia: lo aprendido
    # es solo la CORRECCION, en los dos sentidos (morder mas = limpiar; morder menos = contenerse). v2 reemplazaba la
    # boca (p = sigmoide(BETA * (Q1 - Q0)), 0.5 al nacer) y en el humo 8002 rompio la ventana de parto (R0 0.005).
    # Q lineal en rasgos que el cuerpo siente. Q se aprende por TD (SARSA esperado, semi-Markov entre decisiones) con la recompensa SENTIDA (v2):
    # +R_PARTO cuando pare y R_MUERTE cuando muere (terminal), mas moldeo por potencial con u = min(E, Ag) (no cambia la
    # politica optima; solo acelera). v1 (solo el cambio de u, sin recompensa real) aprendio al reves en el humo 8001:
    # mordia MAS cuanto mas cerca de morir (retorno sin objetivo real). Ninguna regla dice "si esta lleno y
    # no hay nada util, limpia": eso solo puede salir de los pesos aprendidos.
    # Herencia (DECLARADA, el mismo camino que el nodo de FABRICA): Q y la memoria de letras viven en el carro (el
    # cerebro del linaje) y pasan al cuerpo siguiente del linaje (hijo de la cola o fundador). MODO 'sin_herencia': cada
    # cuerpo nuevo empieza con Q = 0 (la memoria de letras SI pasa: es lo que el linaje sabe de las letras, no de limpiar).
    # Prohibido y no usado: el rng de la pista y la tabla verdadera de valencias que viaja en ctx['fabrica'].
    def _apr_init(self, ctx):
        if OPCION and MODO not in ('aprende', 'sin_herencia', 'azar'): raise SystemExit(f"APR: MODO invalido {MODO!r}")
        if OPCION and MODO == 'azar' and P_AZAR is None: raise SystemExit("APR_AZAR: P_AZAR sin fijar (construye_apr.py --p_azar)")
        self._aL = int(ctx['L'])
        self._adS = {}                       # letra -> [suma dE sentido, suma dAg sentido, mordidas] (del LINAJE)
        self._aw = np.zeros((2, NF))         # Q lineal: fila 0 = no morder, fila 1 = morder
        self._apend = None; self._areal = 0.0; self._anace = 0; self._agen = 0; self._avent = 0
        self._aU = float(ctx['rep_umbral']); self._aX = float(ctx['rep_X'])
        z = lambda n: [0] * n
        self._ast = dict(opp_edad=z(len(BIN_EDAD) + 1), mord_edad=z(len(BIN_EDAD) + 1),
                         opp_gen=z(len(BIN_GEN) + 1), mord_gen=z(len(BIN_GEN) + 1),
                         opp_q=z(4), mord_q=z(4), opp_g0=z(2), mord_g0=z(2),
                         opp_post=[z(len(BIN_POST) + 1) for _ in range(2)], mord_post=[z(len(BIN_POST) + 1) for _ in range(2)],
                         anad_q=z(4), quit_q=z(4), anad_g0=z(2), quit_g0=z(2), anad_edad=z(len(BIN_EDAD) + 1), anad_gen=z(len(BIN_GEN) + 1),
                         quit_edad=z(len(BIN_EDAD) + 1), quit_gen=z(len(BIN_GEN) + 1),
                         fab_mord=0, ambas=0, td_n=0, td_abs=0.0, terminales=0, suma_p=0.0, cuerpos=1)

    def _apr_dS(self, k, dS):
        m = self._adS.setdefault(k, [0.0, 0.0, 0])
        m[0] += float(dS[0]); m[1] += float(dS[1]); m[2] += 1

    def _apr_paso(self, E, Ag):
        self._avent = self._avent + 1 if (E >= self._aU and Ag >= self._aU) else 0   # lo que el cuerpo siente de su saciedad

    def _apr_q(self, phi):
        q = self._aw @ phi
        return q, float(1.0 / (1.0 + np.exp(-BETA * (q[1] - q[0]))))

    def _apr_td(self, y):
        phi0, a0 = self._apend[0], self._apend[1]
        d = y - float(self._aw[a0] @ phi0)
        self._aw[a0] = self._aw[a0] + ALFA_Q * d * phi0
        self._ast['td_n'] += 1; self._ast['td_abs'] += abs(d)

    def _opcion(self, obs, kk, mf, u9, pb):
        m = self._adS.get(kk)
        if m is None or not (m[0] < 0 or m[1] < 0): return mf        # no es MALO CONOCIDO: decide la boca de FABRICA
        t = int(obs['t']); pos = obs['pos']; E = float(obs['E']); Ag = float(obs['Ag']); u = min(E, Ag)
        na = self._na
        buenas = {k for k, z in self._adS.items() if z[na] / z[2] > 0}   # lo que el linaje SINTIO bueno para la necesidad activa
        dmin = None; L = self._aL
        for x, k in obs['objs'].items():
            if x != pos and k in buenas:
                d = min((pos - x) % L, (x - pos) % L)
                if dmin is None or d < dmin: dmin = d
        g0 = 1.0 if dmin is None else 0.0
        post = min(E + m[0] / m[2], Ag + m[1] / m[2])
        phi = np.array([1.0, u, post, g0, (1.0 if dmin is None else dmin / (L / 2.0)), min(self._avent / self._aX, 1.0)])
        q, _ = self._apr_q(phi)
        if MODO == 'azar': p = float(P_AZAR)
        elif q[1] == q[0]: p = float(pb)
        else:
            pc = min(max(float(pb), 1e-12), 1 - 1e-12)
            p = float(1.0 / (1.0 + np.exp(-(np.log(pc / (1 - pc)) + BETA * (q[1] - q[0])))))
        if self._apend is not None:          # cierra la decision anterior (semi-Markov, SARSA esperado):
            g = GAMMA ** (t - self._apend[3])  # y = recompensa real + [g*u - u0] (moldeo por potencial u) + g * V(phi)
            y = self._areal + (g * u - self._apend[2]) + g * (p * float(q[1]) + (1 - p) * float(q[0]))
            self._apr_td(y)
        self._areal = 0.0
        b = bool(mf) if (MODO != 'azar' and q[1] == q[0]) else bool(u9 < p)   # el uniforme de FABRICA: con Q1 = Q0, b = mf
        self._apend = (phi, int(b), u, t)
        st = self._ast; ib = int(b)
        e = t - self._anace
        ie = sum(1 for c in BIN_EDAD if e >= c); ig = sum(1 for c in BIN_GEN if self._agen >= c); ip = sum(1 for c in BIN_POST if post >= c)
        st['opp_edad'][ie] += 1; st['mord_edad'][ie] += ib; st['opp_gen'][ig] += 1; st['mord_gen'][ig] += ib
        qq = self._q(t); st['opp_q'][qq] += 1; st['mord_q'][qq] += ib
        st['opp_g0'][int(g0)] += 1; st['mord_g0'][int(g0)] += ib
        st['opp_post'][int(g0)][ip] += 1; st['mord_post'][int(g0)][ip] += ib
        an = int(b and not mf); qu = int(mf and not b)   # anadida (morderia FABRICA? no; APR si) / quitada (FABRICA si; APR no)
        st['anad_q'][qq] += an; st['quit_q'][qq] += qu; st['anad_g0'][int(g0)] += an; st['quit_g0'][int(g0)] += qu
        st['anad_edad'][ie] += an; st['anad_gen'][ig] += an; st['quit_edad'][ie] += qu; st['quit_gen'][ig] += qu
        st['fab_mord'] += int(mf); st['ambas'] += int(mf and b); st['suma_p'] += p
        return b

    def _apr_muere(self, info):
        if self._apend is not None:          # terminal: el cuerpo murio antes de la siguiente decision (potencial final 0)
            self._apr_td(self._areal + R_MUERTE - self._apend[2]); self._ast['terminales'] += 1
        self._apend = None; self._areal = 0.0; self._avent = 0

    def _apr_nace(self, info):
        self._apend = None; self._areal = 0.0; self._avent = 0; self._anace = int(info['t']); self._agen += 1; self._ast['cuerpos'] += 1
        if MODO == 'sin_herencia': self._aw[:] = 0.0

    def _apr_salida(self):
        grid = {}
        for g0 in (0, 1):
            for post in (-0.2, 0.1, 0.4, 0.8, 1.2):
                u = min(1.4, post + 0.4)
                q = self._apr_q(np.array([1.0, u, post, float(g0), (1.0 if g0 else 0.15), 0.0]))[0]
                grid[f"g0={g0} post={post}"] = round(BETA * float(q[1] - q[0]), 3)   # CORRECCION al logit de la boca de FABRICA
        st = dict(self._ast); st['td_abs'] = round(st['td_abs'], 4); st['suma_p'] = round(st['suma_p'], 4)
        return dict(modo=MODO, p_azar=P_AZAR, alfa=ALFA_Q, gamma=GAMMA, beta=BETA, r_parto=R_PARTO, r_muerte=R_MUERTE, bin_edad=list(BIN_EDAD), bin_gen=list(BIN_GEN),
                    bin_post=list(BIN_POST), w=[[round(float(v), 4) for v in f] for f in self._aw], politica=grid,
                    letras={k: [round(z[0] / z[2], 3), round(z[1] / z[2], 3), int(z[2])] for k, z in sorted(self._adS.items())}, **st)

'''

# (ancla, reemplazo); en el reemplazo, NL se sustituye por el fin de linea del origen
ANCLAS = [
    ('"""carros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.',
     '"""carros/{nombre}.py — APR (camino A, experimentos/aprende_barrer): FABRICA + la OPCION APRENDIDA de morder lo malo conocido.'
     'NLGENERADO por experimentos/aprende_barrer/construye_apr.py desde carros/FABRICA.py (sha {sha}). NO editar a mano.'
     'NLMODO {modo}. Con OPCION = 0 es FABRICA bit a bit (identidad_apr.py). Lo que sigue es el docstring de FABRICA.NL'
     'NLcarros/FABRICA.py — EL CARRO DE FABRICA de la carrera de escuderias.'),
    ("             menu='f', alma_curita='f')NL",
     "             menu='f', alma_curita='f')NL{constantes}"),
    ("        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = NoneNL",
     "        self._R = 0.; self._Rp = 0.; self._hambre = 0.; self._enc = NoneNL        self._apr_init(ctx)NL"),
    ("            pb = 1 / (1 + np.exp(-Vb / .3)); mordio = bool(rng.random() < pb)NL",
     "            pb = 1 / (1 + np.exp(-Vb / .3)); _u9 = rng.random(); mordio = bool(_u9 < pb)NL"
     "            if OPCION: mordio = self._opcion(obs, kk, mordio, _u9, pb)NL"),
    ("Aprendizaje de la mordida (sin rng).\"\"\"NL        if not res['mordio']: returnNL",
     "Aprendizaje de la mordida (sin rng).\"\"\"NL        if OPCION and res['mordio']: self._apr_dS(res['letra'], res['dS'])NL"
     "        if not res['mordio']: returnNL"),
    ("        self._nmu += 1NL",
     "        self._nmu += 1NL        if OPCION: self._apr_muere(info)NL"),
    ("    def al_parir(self, info):NL        return None",
     "    def al_parir(self, info):NL        if OPCION: self._areal += R_PARTO; self._avent = 0   # APR v2: parir se SIENTE (+1)NL        return None"),
    ("        t = obs['t']; pos = obs['pos']; E = obs['E']; Ag = obs['Ag']; objs = obs['objs']; rng = self.rngNL",
     "        t = obs['t']; pos = obs['pos']; E = obs['E']; Ag = obs['Ag']; objs = obs['objs']; rng = self.rngNL"
     "        if OPCION: self._apr_paso(E, Ag)NL"),
    ("        _rh = info['rng_hijo']NL",
     "        _rh = info['rng_hijo']NL        if OPCION: self._apr_nace(info)NL"),
    ("    def salida(self):NL",
     "{metodos}    def salida(self):NL"),
    ("            _rep_cuello=int(kw['rep_cuello']))NL",
     "            _rep_cuello=int(kw['rep_cuello']), **({{'apr': self._apr_salida()}} if OPCION else {{}}))NL"),
]

VARIANTES = [('APR', 'aprende'), ('APR_SIN_HERENCIA', 'sin_herencia'), ('APR_AZAR', 'azar')]


def construye(nombre, modo, p_azar):
    src = open(ORIGEN, 'rb').read()
    sha = h16b(src)
    if sha != SHA_FABRICA: raise SystemExit(f"CONSTRUYE: FABRICA.py sha {sha} != {SHA_FABRICA} (el origen cambio)")
    txt = src.decode('utf-8'); NL = '\r\n' if '\r\n' in txt else '\n'
    if NL == '\r\n' and txt.replace('\r\n', '').count('\n'): raise SystemExit("CONSTRUYE: fines de linea mezclados en el origen")
    pa = repr(float(p_azar)) if (p_azar is not None and modo == 'azar') else 'None'
    fmt = dict(nombre=nombre, sha=SHA_FABRICA, modo=modo,
               constantes=CONSTANTES.format(modo=modo, p_azar=pa).lstrip('\n').replace('\n', NL),
               metodos=METODOS.lstrip('\n').replace('\n', NL))
    for a, r in ANCLAS:
        a = a.replace('NL', NL)
        n = txt.count(a)
        if n != 1: raise SystemExit(f"CONSTRUYE: el ancla aparece {n} veces (debe ser 1): {a[:70]!r}")
        r = r.replace('NL', NL)
        r = r.format(**fmt) if '{' in r else r
        txt = txt.replace(a, r)
    return txt.encode('utf-8')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--p_azar', type=float, default=None); ap.add_argument('--verifica', action='store_true')
    a = ap.parse_args()
    if a.p_azar is not None and not 0.0 <= a.p_azar <= 1.0: raise SystemExit("--p_azar en [0, 1]")
    outs = {n: construye(n, m, a.p_azar) for n, m in VARIANTES}
    # las variantes difieren SOLO en el nombre del docstring y en MODO / P_AZAR
    norm = lambda b, n, m: b.decode('utf-8').replace(f"carros/{n}.py", 'X').replace(f"MODO {m}.", 'M').replace(f"MODO = '{m}'", 'M').split('P_AZAR = ')[0] + \
        b.decode('utf-8').split('P_AZAR = ')[1].split('\n', 1)[1]
    base = norm(outs['APR'], 'APR', 'aprende')
    for n, m in VARIANTES:
        if norm(outs[n], n, m) != base: raise SystemExit(f"CONSTRUYE: {n} difiere de APR en algo mas que MODO / P_AZAR")
    ok = True
    for n, b in outs.items():
        ruta = os.path.join(CARROS, n + '.py')
        if a.verifica:
            igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
            ok &= igual; print(f"  {'IGUAL ' if igual else 'DISTINTO'} {n}.py sha {h16b(b)}")
        else:
            open(ruta, 'wb').write(b); print(f"  escrito {ruta} (sha {h16b(b)}; {len(b)} bytes)")
    print(f"  origen FABRICA.py sha {SHA_FABRICA} · P_AZAR {a.p_azar}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
