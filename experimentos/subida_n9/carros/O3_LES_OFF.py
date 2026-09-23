"""O3_LES_OFF (construido por experimentos/subida_n9/construye_n9.py desde carrera_escuderias/carros/O3.py sha 0442c2884fcb0e11; instrumento de LESION del modelo de si, perillas LESION_SI / LESION_COLA; las dos False = O3 bit a bit). carros/O3.py — escuderia O3 (combo Opus: disenador + biologo + critico). Carrera de escuderias, RONDA 2 (ENMIENDA 5).

MISION: llegar a la AGI por este camino.

BASE: copia de carros/O1.py (sha 99436afa2715f028). Con M1 = M3 = TERMINAL = False el carro es O1 decision a decision
(arnes de identidad en bitacoras/O3.md). Los mecanismos los PROPUSO EL BIOLOGO del equipo; el disenador los implemento.

M1. FUNDADOR QUE NO SE CONGELA (sin memoria nueva; solo cuenta letras en obs['objs'], que la pista da a todos).
   - La letra desconocida a probar se elige por RAREZA en el mundo (la mas escasa primero), no por cercania.
   - Una letra desconocida ABUNDANTE (>= ABUND de los objetos) es PRESUNTA MALA: solo se prueba con reserva
     (min(E, Ag) >= RESERVA). Inferencia ecologica: lo que escasea es lo que alguien consume. Falla si la regla del mundo
     cambia; no lee la tabla verdadera.
   - DESESPERACION: si la necesidad mas baja no tiene ninguna letra conocida que la suba en el mundo y min(lev) <= PRUEBA,
     prueba igual la letra desconocida mas escasa si es RARA (<= RARA de los objetos). Quieto muere seguro.
   - Si no hay ninguna letra desconocida permitida, espera en el hueco (como O1).
   - v2 (DISENADOR, tras refutarse el humo 1: la regla de abundancia se auto-cumplia -los O3 mordian C y D, que se
     volvian raras, y A quedaba 'presunta mala' para siempre: 0 hijos, muertes de hambre a los 600 pasos): si la
     necesidad mas baja no tiene fuente conocida en el mundo, prueba la desconocida MAS ESCASA sin importar su abundancia
     ni el nivel. La abundancia solo ordena y solo difiere la prueba cuando hay fuente conocida.
M3. CUANDO MORDER LO MALO SEGUN LA COLA (historia de vida). cola_est = info['cola'] + 1 en cada parto (quiere_parir, nunca
   veta), -1 cuando nace un hijo de la cola.
   (a) cola_est < 3: limpieza de O1 (solo si no hay nada util; no rompe la ventana de parto).
   (b) cola_est >= 3: LIMPIEZA POR EXISTENCIAS: si en el mundo hay < STOCK objetos buenos conocidos para la necesidad mas
       baja, muerde lo malo costeable (golpe en la necesidad mas llena, piso PISO, aunque rompa la ventana).
   (c) TERMINAL: cuerpo con >= PARTOS_TERM partos propios (v3: 2; el biologo propuso 4) y cola_est >= 4: deja de morder lo bueno y solo limpia lo malo que cae en
       la necesidad mas llena, sin piso, hasta morir. DECLARADO: sube las muertes a proposito (el coordinador decide si
       es historia de vida o juego de la metrica; se apaga con TERMINAL = False).
No escribe ni lee la pizarra (M2 del biologo NO implementado en esta version).

v4 FINAL (DISENADOR, sobre la critica del CRITICO-PROBADOR; perillas nuevas, las dos False = v3 exacto):
R1. RESERVA (critica 2, pista mixta): con cola_est <= COLA_RES el cuerpo es la ultima reserva del linaje. La limpieza de O1 no
   baja la necesidad golpeada de PISO_RES (en vez de PISO = 0.2) cuando la ventana de parto no corre; si corre, no la rompe
   (igual que O1). Evidencia: en mix 9052/9053 buena parte de los cuerpos sin parir mueren por veneno/sal (limpiar hasta 0.2 deja
   200 pasos para hallar comida en un mundo sin buenos el 23-31 % de los pasos). NO se adopto MARGEN 0.5 (ver bitacora).
R2. ESPERA DEL QUE PRUEBA (critica 4): en desesperacion (sin fuente conocida para la necesidad mas baja) una letra desconocida
   ABUNDANTE (>= ABUND) solo se prueba con min(E, Ag) <= PRUEBA_ULT; mientras tanto espera en el hueco a que aparezca una letra
   rara. PRUEBA_ULT = 0.45 y no 0.3 (propuesta del critico): con 0.3 una mordida de B (-0.4) mata en el acto.
"""
import numpy as np

MARGEN = 0.25      # muerde lo bueno si la necesidad que sube esta bajo rep_umbral + MARGEN
PRUEBA = 0.5       # prueba una letra desconocida (no abundante) si E y Ag > PRUEBA
PEN_OTRO = 0.35    # factor al blanco si otro cuerpo esta estrictamente mas cerca
D0 = 3.0           # suavizado de la distancia en el puntaje
PISO = 0.2         # la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)

# ---- perillas de O3 (todas False = O1 exacto)
M1 = True
M1_V2 = True       # v2 (disenador, tras refutar el humo 1): la abundancia no bloquea la prueba si no hay fuente conocida
M3 = True
TERMINAL = True
ABUND = 0.25       # M1: fraccion del mundo desde la que una letra desconocida es presunta mala
RARA = 0.12        # M1: fraccion hasta la que se prueba por desesperacion
RESERVA = 0.95     # M1: min(E, Ag) para probar una letra abundante
COLA_EXIST = 3     # M3(b)
STOCK = 2          # M3(b): limpia si hay menos de STOCK buenos conocidos para la necesidad mas baja
COLA_TERM = 4      # M3(c)
PARTOS_TERM = 2    # M3(c) v3 (disenador, tras el humo 2): era 4 (propuesta del biologo); con 4 la vida es ~6000 y d ~5 en 30000
RESERVA_COLA = True  # v4 R1 (critico 2): False = v3
COLA_RES = 2       # R1: modo reserva con cola_est <= COLA_RES
PISO_RES = 0.5     # R1: piso de la limpieza en modo reserva (ventana parada)
ESPERA_PRUEBA = True  # v4 R2 (critico 4): False = v3
PRUEBA_ULT = 0.45  # R2: nivel desde el que se prueba una letra desconocida abundante en desesperacion
# ---- LESIONES (subida_n9; instrumento, no mecanismo; las dos False = O3 bit a bit, arnes identidad_n9.py)
LESION_SI = False    # L-SI: las decisiones leen (E, Ag) de un paso PASADO al azar del linaje (ventana VENTANA_LES)
LESION_COLA = False  # L-COLA: las decisiones leen cola_est de un paso PASADO al azar del linaje (ventana VENTANA_LES)
VENTANA_LES = 2000   # el paso pasado sale de los ultimos VENTANA_LES pasos del LINAJE (misma marginal, otro momento)


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.yo = ctx['id']
        self.suma = {}; self.n = {}          # memoria del LINAJE: letra -> suma de dS, numero de mordidas
        self.blanco = None
        self.cola_est = 0; self.partos_cuerpo = 0; self._modo = 'o1'; self._prueba = None
        self._hlev = []; self._hcola = []; self._ilev = 0; self._icola = 0; self._cola_dec = 0; self._term_ult = False
        self._les = dict(n=0, dlev=0.0, dcola=0.0, lev_real=[0.0, 0.0], lev_usado=[0.0, 0.0], cola_real=0.0, cola_usada=0.0, cambia_term=0, term_real=0, term_usado=0)
        self.st = dict(mord={}, pruebas=0, sin_blanco=0, pasos=0, cuerpos=0, partos=0, limpias=0,
                       pruebas_desesp=0, pruebas_abund=0, limp_exist=0, limp_term=0, pasos_term=0, cuerpos_term=0, esperas=0)

    # ------------------------------------------------------------ memoria
    def _val(self, k):
        if k not in self.n: return None
        return self.suma[k] / self.n[k]

    def _dist(self, a, b):
        d = (b - a) % self.L; return min(d, self.L - d)

    def _dir(self, a, b):
        if a == b: return 0
        d = (b - a) % self.L; return 1 if d <= self.L - d else -1

    def _gana(self, v, lev):
        """ganancia ponderada por urgencia de morder una letra de valor v con niveles lev=(E, Ag); None si dania."""
        if v is None: return None
        if (v < 0).any() or not (v > 0).any(): return 0.0
        g = 0.0
        for j in (0, 1):
            if v[j] <= 0: continue
            x = lev[j]
            if x >= self.U + MARGEN: continue
            u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)
            g += u * min(v[j], self.U + 0.5 - x)
        return g

    def _quiere(self, k, lev, limpia=False, term=False):
        v = self._val(k)
        if v is None:
            if M1: return k == self._prueba
            return min(lev) > PRUEBA
        g = 0.0 if term else self._gana(v, lev)
        if g: return True
        return limpia and self._costeable(v, lev)

    def _costeable(self, v, lev):
        """LIMPIEZA: morder algo que dania solo si el golpe cae en la necesidad MAS llena. Modo o1: si la ventana de
        parto corre no la rompe, si no corre no baja de PISO. Modo exist: piso PISO siempre. Modo term: sin piso."""
        if not (v < 0).any(): return False
        for j in (0, 1):
            if v[j] < 0:
                if self._modo == 'term': piso = -1e9
                elif self._modo == 'exist': piso = PISO
                else:
                    piso = PISO_RES if (RESERVA_COLA and self._cola_dec <= COLA_RES) else PISO
                    piso = self.U if min(lev) >= self.U else piso
                if lev[j] + v[j] < piso: return False
            if v[j] < 0 and lev[j] < lev[1 - j]: return False   # el golpe va a la necesidad MAS llena
        return True

    def _sube(self, v, j):
        return v is not None and v[j] > 0 and not (v < 0).any()

    # ------------------------------------------------------------ M1
    def _elige_prueba(self, pos, objs, lev):
        """letra desconocida a probar (por rareza) y el objeto mas cercano de esa letra; None si ninguna permitida."""
        cnt = {}
        for k in objs.values(): cnt[k] = cnt.get(k, 0) + 1
        ntot = max(len(objs), 1)
        j = 0 if lev[0] <= lev[1] else 1
        hay_fuente = any(self._sube(self._val(k), j) for k in cnt)
        if M1_V2:   # v2 (disenador, tras el humo 1): sin fuente conocida para la necesidad mas baja -> prueba la mas escasa,
            desesp = not hay_fuente   # SEA CUAL SEA su abundancia y el nivel (la abundancia solo ordena)
        else:
            desesp = min(lev) <= PRUEBA and not hay_fuente
        cand = []
        for k, c in cnt.items():
            if k in self.n: continue
            f = c / ntot
            if M1_V2 and desesp:
                ok = not (ESPERA_PRUEBA and f >= ABUND and min(lev) > PRUEBA_ULT); tipo = 'desesp'
                if not ok: self.st['esperas'] += 1
            elif f >= ABUND: ok = min(lev) >= RESERVA; tipo = 'abund'
            elif min(lev) > PRUEBA: ok = True; tipo = 'normal'
            else: ok = desesp and f <= RARA; tipo = 'desesp'
            if ok: cand.append((f, k, tipo))
        if not cand: return None, desesp
        f, k, tipo = min(cand)
        best = None
        for x, kk in objs.items():
            if kk != k: continue
            d = self._dist(pos, x)
            if best is None or d < best[0]: best = (d, x)
        return (best[0], best[1], k, tipo), desesp

    # ------------------------------------------------------------ INTERFAZ
    def actua(self, obs):
        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']
        self._cola_dec = self.cola_est
        if LESION_SI or LESION_COLA: lev = self._lesiona(lev)
        self.st['pasos'] += 1
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        term = TERMINAL and self.partos_cuerpo >= PARTOS_TERM and self._cola_dec >= COLA_TERM
        if LESION_COLA: self._cuenta_term(term)
        self._term_ult = term
        if term: self.st['pasos_term'] += 1
        mejor = None; desc = None
        for x, k in objs.items():
            d = self._dist(pos, x); v = self._val(k)
            if v is None:
                if not M1 and min(lev) > PRUEBA and (desc is None or d < desc[0]): desc = (d, x)
                continue
            g = 0.0 if term else self._gana(v, lev)
            if not g: continue
            s = g / (d + D0)
            if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO
            if mejor is None or s > mejor[0]: mejor = (s, x)
        desesp = False; tipo = None; self._prueba = None
        if M1 and not term:
            pr, desesp = self._elige_prueba(pos, objs, lev)
            if pr is not None:
                desc = (pr[0], pr[1]); self._prueba = pr[2]; tipo = pr[3]
        # limpieza: o1 / por existencias / terminal
        if term:
            self._modo = 'term'; limpia = True
        elif M3 and self._cola_dec >= COLA_EXIST and min(lev) < self.U + MARGEN:
            self._modo = 'exist'
            j = 0 if lev[0] <= lev[1] else 1
            stock = sum(1 for k in objs.values() if self._sube(self._val(k), j))
            limpia = stock < STOCK
        else:
            self._modo = 'o1'
            limpia = mejor is None and min(lev) < self.U + MARGEN
        sucio = None
        if limpia:
            for x, k in objs.items():
                v = self._val(k)
                if v is not None and self._costeable(v, lev):
                    d = self._dist(pos, x)
                    if sucio is None or d < sucio[0]: sucio = (d, x)
        if desesp and desc is not None: tgt = desc[1]          # M1: la necesidad critica no tiene fuente conocida
        elif mejor is not None: tgt = mejor[1]
        elif desc is not None: tgt = desc[1]
        elif sucio is not None: tgt = sucio[1]
        else:
            tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1
        self.blanco = tgt
        mov = self._dir(pos, tgt)
        p2 = (pos + mov) % self.L
        muerde = False
        if p2 in objs:
            k2 = objs[p2]
            muerde = bool(self._quiere(k2, lev, limpia, term))
            if muerde and k2 not in self.n:
                self.st['pruebas'] += 1
                if tipo == 'desesp': self.st['pruebas_desesp'] += 1
                elif tipo == 'abund': self.st['pruebas_abund'] += 1
            v2 = self._val(k2)
            if muerde and limpia and v2 is not None and (v2 < 0).any():
                self.st['limpias'] += 1
                if self._modo == 'exist': self.st['limp_exist'] += 1
                elif self._modo == 'term': self.st['limp_term'] += 1
        return dict(mov=mov, muerde=muerde, escribe=None)

    def _lesiona(self, lev):
        """LESION (subida_n9). L-SI: devuelve el (E, Ag) de un paso al azar entre los ultimos VENTANA_LES pasos del LINAJE
        (incluido el actual, a traves de sus cuerpos). L-COLA: fija self._cola_dec a la cola_est de un paso al azar de la misma
        ventana. Ventana del linaje y no historia del cuerpo: el arnes midio que sortear desde el nacimiento sesga la marginal
        hacia la juventud (E 0.91 contra 1.01; cola 1.44 contra 2.72; TERMINAL 5516 contra 27006 pasos). Un sorteo por lesion
        activa y por paso, del rng de cuerpo que la pista entrega al carro. Telemetria en self._les (no puntua)."""
        lu = lev
        if LESION_SI:
            self._ilev = self._anillo(self._hlev, self._ilev, lev); lu = self._hlev[int(self.rng.integers(len(self._hlev)))]
        if LESION_COLA:
            self._icola = self._anillo(self._hcola, self._icola, self.cola_est)
            self._cola_dec = self._hcola[int(self.rng.integers(len(self._hcola)))]
        s = self._les; s['n'] += 1
        s['dlev'] += abs(lu[0] - lev[0]) + abs(lu[1] - lev[1]); s['dcola'] += abs(self._cola_dec - self.cola_est)
        for j in (0, 1):
            s['lev_real'][j] += lev[j]; s['lev_usado'][j] += lu[j]
        s['cola_real'] += self.cola_est; s['cola_usada'] += self._cola_dec
        return lu

    @staticmethod
    def _anillo(h, i, x):
        """guarda x en el anillo h (ultimos VENTANA_LES pasos del linaje); devuelve el indice de escritura siguiente"""
        if len(h) < VENTANA_LES:
            h.append(x); return i
        h[i] = x; return (i + 1) % VENTANA_LES

    def _cuenta_term(self, term):
        s = self._les; real = TERMINAL and self.partos_cuerpo >= PARTOS_TERM and self.cola_est >= COLA_TERM
        s['term_real'] += int(real); s['term_usado'] += int(term); s['cambia_term'] += int(real != term)

    def _hueco(self, pos, otros):
        if not otros: return pos
        ps = sorted(set(otros)); best = None
        for i, a in enumerate(ps):
            b = ps[(i + 1) % len(ps)]; g = (b - a) % self.L or self.L
            if best is None or g > best[0]: best = (g, (a + g // 2) % self.L)
        return best[1]

    def resultado(self, res):
        if not res['mordio']: return
        k = res['letra']; dS = np.asarray(res['dS'], float)
        self.suma[k] = self.suma.get(k, np.zeros(2)) + dS; self.n[k] = self.n.get(k, 0) + 1
        self.st['mord'][k] = self.st['mord'].get(k, 0) + 1

    def fin_paso(self, info):
        return None

    def muere(self, info):
        if (self._term_ult if LESION_COLA else (TERMINAL and self.partos_cuerpo >= PARTOS_TERM and self.cola_est >= COLA_TERM)): self.st['cuerpos_term'] += 1
        return None

    def al_parir(self, info):
        self.st['partos'] += 1
        return {k: (self.suma[k].copy(), self.n[k]) for k in self.n}

    def nace(self, info):
        self.st['cuerpos'] += 1; self.blanco = None
        self.partos_cuerpo = 0
        m = info.get('memoria')
        if m:
            self.cola_est = max(self.cola_est - 1, 0)
            for k, (s, n) in m.items():
                if k not in self.n: self.suma[k] = np.asarray(s, float).copy(); self.n[k] = int(n)

    def quiere_parir(self, info):
        self.cola_est = min(int(info['cola']) + 1, 200); self.partos_cuerpo += 1
        return True

    def salida(self):
        return dict(tabla={k: [round(float(z), 3) for z in self._val(k)] for k in self.n}, n={k: int(v) for k, v in self.n.items()},
                    cola_est=int(self.cola_est), perillas=dict(M1=M1, M1_V2=M1_V2, M3=M3, TERMINAL=TERMINAL,
                                                                  RESERVA_COLA=RESERVA_COLA, ESPERA_PRUEBA=ESPERA_PRUEBA),
                    **{k: v for k, v in self.st.items()}, **({'lesion': dict(self._les)} if (LESION_SI or LESION_COLA) else {}))


def crea(ctx):
    return Carro(ctx)
