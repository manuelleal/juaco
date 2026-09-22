"""carros/O2.py — escuderia O2 (combo Opus: disenador + biologo + critico). Carrera de escuderias, RONDA 2.

MISION: llegar a la AGI por este camino.

BASE: carros/O1.py (sha 99436afa2715f028), todo lo de O1 igual SALVO la regla de prueba de letras desconocidas (M2) y el
riesgo del ultimo cuerpo del linaje (M1). Mecanismos propuestos por el BIOLOGO del equipo; implementados por el disenador.

M2 · FUNDADOR QUE PRUEBA LO RARO PRIMERO Y PRUEBA POR DESESPERACION (sin memoria nueva: un conteo por paso sobre obs['objs']).
  frac_k = objetos con letra k / objetos en el mundo (lo que todo cuerpo ve; no se lee rng ni tabla).
  - SENAL de rareza: alguna letra presente con frac < RARA. Sin senal (mundo casi uniforme): regla de O1 (prueba con
    min(E, Ag) > PRUEBA).
  - Con senal: una letra DESCONOCIDA rara (frac < RARA) se prueba con CUALQUIER nivel (blanco: la rara de menor frac,
    el objeto mas cercano); una desconocida ABUNDANTE solo si el cuerpo NO es el ultimo del linaje y min(E, Ag) > VETERANO.
  - DESESPERACION: si para la necesidad mas baja no se conoce ninguna letra que la suba y le quedan < DESESP pasos
    (nivel/costo < DESESP), prueba la desconocida mas cercana (cualquier frecuencia).
  DECLARADO (trampa 'mundo que se come la comida', usada a favor): en ESTE mundo lo bueno escasea porque se come; la
  regla usa esa regularidad. La valencia se sigue MEMORIZANDO al morder (resultado()); en otro mundo seria neutra o danina.

M1 · EL ULTIMO DEL LINAJE NO ARRIESGA (memoria nueva: un entero self.cola = hijos esperando en la fila del linaje).
  Sube en al_parir, baja en nace (hijo de la cola), se sincroniza con info['cola'] en quiere_parir; instancia nueva = 0.
  ULTIMO = (cola == 0): si muere, el mundo pone un fundador (extincion). Si ULTIMO:
    (1) no limpia (nunca muerde lo malo conocido); (2) solo prueba desconocidas raras o por desesperacion;
    (3) con la racha de parto corriendo no prueba nada desconocido (lo que no conoce podria romperla).
  Si cola >= 1: O1 (limpia con PISO) + M2.
No escribe ni lee la pizarra. Nunca veta el parto. La tabla por letra es del linaje (pasa al hijo por al_parir/nace);
con fundador limpio (ENMIENDA 5) la instancia nueva arranca sin nada.
Perillas de control: USA_M1, USA_M2. v2 (humo 2 de la bitacora): USA_M1 = 0 (M1 empeoro en s9001), USA_M2 = 1.

v3 (FINAL, disenador, sobre la critica del CRITICO-PROBADOR del equipo; sin memoria nueva). Tres arreglos, cada uno con su perilla
(las tres en 0 = v2 bit a bit, arnes en la bitacora):
  K1 USA_DISP · LIMPIA CUANDO EL BUENO ESTA DISPUTADO (critica 1, 2 y 5): si el blanco bueno lo tiene mas cerca otro cuerpo, cuenta
     como 'nada util para mi': puede limpiar (misma regla _costeable de O1: golpe en la necesidad mas llena, PISO) y, si hay un malo
     costeable MAS CERCA que ese bueno, va a limpiarlo. Lo que muerde sigue siendo solo lo costeable: no se suicida (NO es M3).
  K2 USA_SINSENAL · SIN SENAL DE RAREZA NO PRUEBA A CIEGAS (critica 4): sin ninguna letra < RARA, una desconocida solo se prueba si
     esta por debajo de la fraccion uniforme (fr < FR_UNI) y min(E, Ag) > PRUEBA (la menos frecuente primero); una abundante solo con
     min(E, Ag) > VETERANO. Con A y C ausentes (mundo B/D ~50/50) el fundador de 0.6 ya no muerde B/D y muere a 200.
  K3 USA_DESESP_RARA · LA DESESPERACION CONSERVA LA PRIORIDAD DE LO RARO (critica 3): desesperado, solo prueba desconocidas con
     fr < FR_UNI, con clave de rareza (0, fr, d); nunca la abundante mas cercana (en un mundo 85 % B + D era veneno o sal).
"""
import numpy as np

MARGEN = 0.25      # muerde lo bueno si la necesidad que sube esta bajo rep_umbral + MARGEN
PRUEBA = 0.5       # regla de O1: prueba una desconocida solo si E y Ag > PRUEBA (sin senal de rareza, o con USA_M2=0)
PEN_OTRO = 0.35    # factor al blanco si otro cuerpo esta estrictamente mas cerca
D0 = 3.0           # suavizado de la distancia en el puntaje
PISO = 0.2         # la limpieza no baja la necesidad golpeada de aqui (si la ventana de parto no corre)
RARA = 0.15        # M2: letra rara si su fraccion en el mundo es < RARA (uniforme = 0.25)
VETERANO = 0.9     # M2: una desconocida abundante solo la prueba un cuerpo con reemplazo y min(E, Ag) > VETERANO
DESESP = 150       # M2: desesperacion si a la necesidad critica le quedan < DESESP pasos
FR_UNI = 0.25      # v3 (K2, K3): fraccion de una letra en un mundo uniforme de 4 letras
USA_M1 = 0
USA_M2 = 1
USA_DISP = 1       # v3 K1
USA_SINSENAL = 1   # v3 K2
USA_DESESP_RARA = 1  # v3 K3


class Carro:
    def __init__(self, ctx):
        self.L = int(ctx['L']); self.U = float(ctx['rep_umbral']); self.rng = ctx['rng']
        self.costo = max(float(ctx['costo']), float(ctx['costo_a']), 1e-9)
        self.yo = ctx['id']
        self.suma = {}; self.n = {}          # memoria del LINAJE: letra -> suma de dS, numero de mordidas
        self.blanco = None
        self.cola = 0                        # M1: instancia nueva = hubo extincion (o es el primer cuerpo): cola vacia
        self.racha = 0                       # M1: pasos seguidos con E y Ag >= rep_umbral (lo que ve el cuerpo)
        self.st = dict(mord={}, pruebas=0, pruebas_raras=0, pruebas_desesp=0, pruebas_abund=0, sin_blanco=0, pasos=0,
                       cuerpos=0, partos=0, limpias=0, pasos_ultimo=0, limpia_disp=0)

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

    def _costeable(self, v, lev):
        """LIMPIEZA (O1 v2): morder algo que dania solo si el golpe cae en la necesidad mas llena, sin romper la
        ventana de parto si corre y sin bajar de PISO si no corre."""
        if not (v < 0).any(): return False
        for j in (0, 1):
            if v[j] < 0:
                piso = self.U if min(lev) >= self.U else PISO
                if lev[j] + v[j] < piso: return False
            if v[j] < 0 and lev[j] < lev[1 - j]: return False
        return True

    # ------------------------------------------------------------ M2 + M1: que desconocida se puede probar
    def _ultimo(self):
        return bool(USA_M1) and self.cola == 0

    def _desesperado(self, lev):
        """la necesidad mas baja no tiene ninguna letra conocida que la suba y le quedan < DESESP pasos."""
        j = 0 if lev[0] <= lev[1] else 1
        if lev[j] / self.costo >= DESESP: return False
        for k in self.n:
            if self._val(k)[j] > 0: return False
        return True

    def _prueba(self, k, lev, fr, senal, desesp):
        """0 = no se prueba; 1 = rara; 2 = abundante (veterano); 3 = desesperacion; 4 = regla de O1."""
        if not USA_M2:
            if self._ultimo() and self.racha > 0: return 0
            return 4 if min(lev) > PRUEBA else 0
        if desesp:
            if not USA_DESESP_RARA: return 3
            if fr.get(k, 0.0) < FR_UNI: return 3
        if self._ultimo() and self.racha > 0: return 0
        if not senal:
            if not USA_SINSENAL: return 4 if min(lev) > PRUEBA else 0
            if fr.get(k, 0.0) < FR_UNI and min(lev) > PRUEBA: return 4
            return 2 if (not self._ultimo() and min(lev) > VETERANO) else 0
        if fr.get(k, 0.0) < RARA: return 1
        if not self._ultimo() and min(lev) > VETERANO: return 2
        return 0

    # ------------------------------------------------------------ INTERFAZ
    def actua(self, obs):
        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']
        self.st['pasos'] += 1
        self.racha = self.racha + 1 if min(lev) >= self.U else 0
        ult = self._ultimo()
        if ult: self.st['pasos_ultimo'] += 1
        otros = [c[1] for c in obs['cuerpos'] if c[0] != self.yo]
        # M2: fraccion de cada letra en el mundo (solo lo que se ve)
        cnt = {}
        for k in objs.values(): cnt[k] = cnt.get(k, 0) + 1
        tot = max(len(objs), 1)
        fr = {k: c / tot for k, c in cnt.items()}
        senal = any(f < RARA for f in fr.values())
        desesp = bool(USA_M2) and self._desesperado(lev)
        mejor = None; desc = None
        for x, k in objs.items():
            d = self._dist(pos, x); v = self._val(k)
            if v is None:
                m = self._prueba(k, lev, fr, senal, desesp)
                if m:
                    if USA_M2 and m == 1: clave = (0, fr.get(k, 0.0), d)
                    elif (USA_DESESP_RARA and m == 3) or (USA_SINSENAL and m == 4 and USA_M2): clave = (0, fr.get(k, 0.0), d)
                    else: clave = (1, 0.0, d)
                    if desc is None or clave < desc[0]: desc = (clave, x)
                continue
            g = self._gana(v, lev)
            if not g: continue
            s = g / (d + D0)
            dis = bool(otros) and min(self._dist(o, x) for o in otros) < d
            if dis: s *= PEN_OTRO
            if mejor is None or s > mejor[0]: mejor = (s, x, dis, d)
        # limpieza de O1 (M1: el ultimo del linaje no limpia); v3 K1: un blanco disputado cuenta como 'nada util para mi'
        nada = mejor is None or (bool(USA_DISP) and mejor[2])
        limpia = (not ult) and nada and min(lev) < self.U + MARGEN
        sucio = None
        if limpia:
            for x, k in objs.items():
                v = self._val(k)
                if v is not None and self._costeable(v, lev):
                    d = self._dist(pos, x)
                    if sucio is None or d < sucio[0]: sucio = (d, x)
        va_limpiar = mejor is not None and bool(USA_DISP) and mejor[2] and sucio is not None and sucio[0] < mejor[3]
        if va_limpiar: self.st['limpia_disp'] += 1
        if mejor is not None and not va_limpiar: tgt = mejor[1]
        elif va_limpiar: tgt = sucio[1]
        elif desc is not None: tgt = desc[1]
        elif sucio is not None: tgt = sucio[1]
        else:
            tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1
        self.blanco = tgt
        mov = self._dir(pos, tgt)
        p2 = (pos + mov) % self.L
        muerde = False
        if p2 in objs:
            k = objs[p2]; v = self._val(k)
            if v is None:
                m = self._prueba(k, lev, fr, senal, desesp)
                muerde = m > 0
                if muerde:
                    self.st['pruebas'] += 1
                    if m == 1: self.st['pruebas_raras'] += 1
                    elif m == 2: self.st['pruebas_abund'] += 1
                    elif m == 3: self.st['pruebas_desesp'] += 1
            elif self._gana(v, lev):
                muerde = True
            elif limpia and self._costeable(v, lev):
                muerde = True; self.st['limpias'] += 1
        return dict(mov=mov, muerde=muerde, escribe=None)

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
        return None

    def al_parir(self, info):
        self.st['partos'] += 1; self.cola += 1
        return {k: (self.suma[k].copy(), self.n[k]) for k in self.n}

    def nace(self, info):
        self.st['cuerpos'] += 1; self.blanco = None; self.racha = 0
        if info.get('fundador'): self.cola = 0
        else: self.cola = max(self.cola - 1, 0)
        m = info.get('memoria')
        if m:
            for k, (s, n) in m.items():
                if k not in self.n: self.suma[k] = np.asarray(s, float).copy(); self.n[k] = int(n)

    def quiere_parir(self, info):
        self.cola = int(info.get('cola', self.cola))
        return True

    def salida(self):
        return dict(tabla={k: [round(float(z), 3) for z in self._val(k)] for k in self.n}, n={k: int(v) for k, v in self.n.items()},
                    cola=int(self.cola), **{k: v for k, v in self.st.items()})


def crea(ctx):
    return Carro(ctx)
