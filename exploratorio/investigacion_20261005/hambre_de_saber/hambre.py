# -*- coding: utf-8 -*-
"""
HAMBRE DE SABER — un modelo con curiosidad que ESCOGE que fuente leer o mirar, pone lo leido en cuarentena,
amarra texto con video, detecta copias y mentirosos, y consolida ("sueño").  Simulacion sintetica, numpy puro.

Mundo oculto: NF hechos (cada uno un valor de V), agrupados en NT temas; algunos cambian con el tiempo.
Fuentes: fiables, ruidosas, mentirosas (sistematicas), repetidas (copian a otra), especializadas, obsoletas;
         de dos modalidades (texto = simbolo exacto; video = cuadros ruidosos que un decodificador congelado lee).
Presupuesto: K items por paso. El sistema decide que fuente mirar (y, con 'preguntas', sobre que hecho).

Brazos:  grandes (lee al azar, cree lo ultimo) · mayoria (lee al azar, cree lo mas repetido) · curios (curiosidad, mayoria)
         cuar (azar + cuarentena) · completo (curiosidad + cuarentena + amarre) · sin_amarre · barajado (apetito barajado)
         oraculo (conoce la calidad; cuarentena) · preguntas (completo + busca refutacion dirigida) · sueno_fijo / sueno_decide
Uso:     python hambre.py --semillas 10 --regimen honesto --out datos/honesto.json
"""
import argparse, json, time, sys
import numpy as np

# ================================================================ mundo
class Mundo:
    def __init__(self, rng, NF=60, V=8, NT=4, T=600, cambios=(200, 400), frac_cambio=0.15):
        self.NF, self.V, self.NT, self.T = NF, V, NT, T
        self.verdad = rng.integers(0, V, NF)
        self.verdad0 = self.verdad.copy()
        self.tema = np.arange(NF) % NT
        self.cambios, self.frac = cambios, frac_cambio
        self.eventos = []                      # (t, f, viejo, nuevo)
        self.rng = rng; self.version = 0; self.cambiados = []

    def paso(self, t):
        if t in self.cambios:
            fs = self.rng.choice(self.NF, int(self.NF * self.frac), replace=False)
            self.version += 1; self.cambiados = list(map(int, fs))
            for f in fs:
                viejo = self.verdad[f]
                nuevo = (viejo + self.rng.integers(1, self.V)) % self.V
                self.verdad[f] = nuevo
                self.eventos.append((t, int(f), int(viejo), int(nuevo)))

# ================================================================ fuentes
class Fuente:
    """tabla de afirmaciones por hecho; se refresca cada `refresco` pasos (errores nuevos). Las copias devuelven la tabla
    de su original (identicas: por eso NO cuentan como confirmacion independiente). Mentirosa: valor FALSO fijo en sus
    hechos mentidos, correcta en el resto. Obsoleta: tabla congelada al t=0 (no se entera de los cambios)."""
    R = 8   # "estilos" posibles de una afirmacion (redaccion / angulo de camara); la copia reproduce el del original
    def __init__(self, i, tipo, mod, cobertura, p_ok, mundo, rng, mentiras=None, copia_de=None, obsoleta=False, refresco=300):
        self.i, self.tipo, self.mod, self.cob, self.p_ok = i, tipo, mod, np.array(cobertura), p_ok
        self.mentiras = mentiras or {}
        self.copia_de, self.obsoleta, self.refresco = copia_de, obsoleta, refresco
        self.rng, self.mundo = rng, mundo; self.peso = 1.0
        self.tabla = None; self.t_tabla = -10**9; self.version = 0

    def _regen(self, t):
        m = self.mundo
        base = m.verdad0 if self.obsoleta else m.verdad
        tab = base.copy()
        err = self.rng.random(m.NF) > self.p_ok
        tab[err] = (base[err] + self.rng.integers(1, m.V, err.sum())) % m.V
        for f, v in self.mentiras.items(): tab[f] = v
        self.tabla, self.t_tabla = tab, t
        self.rasgo = self.rng.integers(0, self.R, m.NF); self.version = m.version

    def _actualiza(self):
        """el mundo cambio: una fuente al dia corrige los hechos cambiados (con su tasa de error); la obsoleta no"""
        m = self.mundo
        for f in m.cambiados:
            if f in self.mentiras: continue
            self.tabla[f] = m.verdad[f] if self.rng.random() < self.p_ok else (m.verdad[f] + self.rng.integers(1, m.V)) % m.V
            self.rasgo[f] = self.rng.integers(0, self.R)
        self.version = m.version

    def dice(self, f, t):
        if self.copia_de is not None: return self.copia_de.dice(f, t)
        if self.tabla is None or (not self.obsoleta and t - self.t_tabla >= self.refresco): self._regen(t)
        elif not self.obsoleta and self.version != self.mundo.version: self._actualiza()
        return int(self.tabla[f]), int(self.rasgo[f])

    def hecho_al_azar(self):
        return int(self.rng.choice(self.cob))

def arma_fuentes(mundo, rng, regimen):
    """mezcla de fuentes por regimen. Devuelve lista de Fuente."""
    NF, V, NT = mundo.NF, mundo.V, mundo.NT
    todo = np.arange(NF)
    fs = []
    def add(tipo, mod, cob, p_ok, **kw):
        fs.append(Fuente(len(fs), tipo, mod, cob, p_ok, mundo, rng, **kw)); return fs[-1]
    def mentiras(n_frac, compartidas=None):
        if compartidas is not None: return dict(compartidas)
        hechos = rng.choice(NF, int(NF * n_frac), replace=False)
        return {int(f): int((mundo.verdad0[f] + rng.integers(1, V)) % V) for f in hechos}
    if regimen in ('honesto', 'cartel'):
        for k in range(6): add('fiable', 'texto' if k % 2 == 0 else 'video', todo, 0.95)
        for k in range(8): add('ruidosa', 'texto' if k % 2 == 0 else 'video', todo, 0.6)
        cartel = mentiras(0.5) if regimen == 'cartel' else None
        ments = [add('mentirosa', 'texto' if k % 2 == 0 else 'video', todo, 0.95, mentiras=mentiras(0.5, cartel)) for k in range(4)]
        for k in range(NT):
            cob = todo[mundo.tema == k]
            add('especial', 'texto', cob, 0.98); add('especial', 'video', cob, 0.98)
        for k in range(4): add('obsoleta', 'texto' if k % 2 == 0 else 'video', todo, 0.95, obsoleta=True)
        # repetidas (copias): en cartel 8 copias de mentirosas; en honesto 4 copias de mentirosas + 4 de fiables/ruidosas
        n_cop_m = 8 if regimen == 'cartel' else 4
        for k in range(n_cop_m): add('copia_m', ments[k % 4].mod, todo, 0.0, copia_de=ments[k % 4])
        if regimen == 'honesto':
            add('copia_f', fs[0].mod, todo, 0, copia_de=fs[0]); add('copia_f', fs[1].mod, todo, 0, copia_de=fs[1])
            add('copia_r', fs[6].mod, todo, 0, copia_de=fs[6]); add('copia_r', fs[7].mod, todo, 0, copia_de=fs[7])
        else:
            add('copia_f', fs[0].mod, todo, 0, copia_de=fs[0]); add('copia_f', fs[1].mod, todo, 0, copia_de=fs[1])
    elif regimen == 'dieta':     # solo fuentes malas: cartel de mentirosas + copias + ruidosas flojas; dos fiables de un solo tema
        cartel = mentiras(0.5)
        ments = [add('mentirosa', 'texto' if k % 2 == 0 else 'video', todo, 0.95, mentiras=dict(cartel)) for k in range(6)]
        for k in range(10): add('ruidosa', 'texto' if k % 2 == 0 else 'video', todo, 0.5)
        for k in range(10): add('copia_m', ments[k % 6].mod, todo, 0, copia_de=ments[k % 6])
        for k in range(6): add('obsoleta', 'texto' if k % 2 == 0 else 'video', todo, 0.7, obsoleta=True)
        cob = todo[mundo.tema == 0]
        add('especial', 'texto', cob, 0.98); add('especial', 'video', cob, 0.98)
    else:
        raise ValueError(regimen)
    return fs

# ================================================================ union-find para grupos de copias
class UF:
    def __init__(self, n): self.p = list(range(n))
    def find(self, a):
        while self.p[a] != a: self.p[a] = self.p[self.p[a]]; a = self.p[a]
        return a
    def union(self, a, b): self.p[self.find(a)] = self.find(b)

# ================================================================ el sistema (todas las variantes en una clase con banderas)
class Sistema:
    """memoria + eleccion de fuente.
    memoria: 'ultimo' (cree lo ultimo), 'mayoria' (cuenta de afirmaciones), 'cuarentena' (confirmaciones independientes)
    eleccion: 'azar', 'apetito', 'oraculo'
    amarre: texto+video de acuerdo suman una confirmacion extra; preguntas: busca refutacion dirigida;
    barajado: las actualizaciones del apetito van a una fuente al azar; sueno: None / 'fijo' / 'decide'"""
    def __init__(self, mundo, fuentes, rng, memoria='cuarentena', eleccion='apetito', amarre=True, preguntas=False,
                 barajado=False, sueno=None, K=3, k_val=2.0, W=150, p_dec=0.85, tau=0.3, eps=0.15, rep0=0.8, ancla=False, tipos=None):
        self.m, self.fs, self.rng = mundo, fuentes, rng
        self.memoria, self.eleccion, self.amarre, self.preguntas, self.barajado, self.sueno = memoria, eleccion, amarre, preguntas, barajado, sueno
        self.K, self.k_val, self.W, self.p_dec, self.tau, self.eps, self.ancla = K, k_val, W, p_dec, tau, eps, ancla
        S, NF, V = len(fuentes), mundo.NF, mundo.V
        self.S, self.NF, self.V = S, NF, V
        # base congelada: sabe 40 % de los hechos, y de esos el 20 % mal (desactualizados)
        self.base = -np.ones(NF, int)
        sabe = rng.random(NF) < 0.4
        self.base[sabe] = mundo.verdad0[sabe]
        mal = sabe & (rng.random(NF) < 0.2)
        self.base[mal] = (mundo.verdad0[mal] + rng.integers(1, V, mal.sum())) % V
        self.base0 = self.base.copy()
        # memorias
        self.ultimo = -np.ones(NF, int)
        self.cuenta = np.zeros((NF, V))                    # mayoria (cada afirmacion cuenta)
        self.apoyo = [dict() for _ in range(NF)]           # cuarentena: f -> {v: {grupo: (t, mods)}}
        self.rep = np.full(S, rep0)                        # reputacion por fuente (rep0 bajo = esceptico: hay que ganarse la confianza)
        self.apetito = np.full(S, 0.5)
        self.pend = [[] for _ in range(S)]                 # creditos pendientes (f, v, t, base_sabia)
        self.log = -np.ones((S, NF), int); self.log_t = -np.ones((S, NF), int); self.log_r = -np.ones((S, NF), int)   # ultima afirmacion por fuente/hecho
        self.uf = UF(S); self.grupo_desde = {}; self.n_grupos_falsos = 0
        self.consumo = np.zeros(S, int); self.consumo_rec = []
        self.t_rep_baja = -np.ones(S, int)
        self.t_validado = {}                               # f -> t de la primera validacion correcta
        self.primera_fuente_cambio = {}
        self.n_suenos = 0; self.consolidadas = 0; self.sin_consolidar = set()
        self.t_valid_hist = []                             # (f, t_nace_hipotesis, t_valida, bimodal)
        self.t_nace = {}
        self.cob_mask = np.zeros((S, NF), bool)
        for s in fuentes: self.cob_mask[s.i, s.cob] = True
        self.tipos = tipos

    # ---------- creencia
    def eff(self, f, t):
        """peso efectivo por valor (suma de reputaciones de los grupos que lo apoyan recientemente, + amarre)"""
        out = {}
        for v, gs in self.apoyo[f].items():
            w = 0.0; mods = set()
            for g, (tg, mg) in list(gs.items()):
                if t - tg > self.W: del gs[g]; continue
                w += self.rep_grupo(g); mods |= mg
            if self.amarre and len(mods) >= 2: w += 1.0
            if w > 0: out[v] = w
        return out

    def rep_grupo(self, g):
        return self.rep[g] * self.fs[g].peso        # la reputacion del representante del grupo (peso>1 = confianza ciega)

    def validado(self, f, t):
        e = self.eff(f, t)
        cand = [(w, v) for v, w in e.items() if w >= self.k_val]
        if not cand: return -1
        return max(cand)[1]

    def respuesta(self, f, t):
        if self.memoria == 'ultimo': return int(self.ultimo[f]) if self.ultimo[f] >= 0 else int(self.base[f])
        if self.memoria == 'mayoria':
            if self.cuenta[f].sum() == 0: return int(self.base[f])
            return int(np.argmax(self.cuenta[f]))
        v = self.validado(f, t)
        return v if v >= 0 else int(self.base[f])

    def respuestas(self, t):
        return np.array([self.respuesta(f, t) for f in range(self.NF)])

    # ---------- eleccion de fuente
    def elige(self, t):
        S = self.S
        if self.eleccion == 'azar': return list(self.rng.integers(0, S, self.K))
        if self.eleccion == 'oraculo':
            buenos = [s.i for s in self.fs if s.tipo in ('fiable', 'especial')]
            return list(self.rng.choice(buenos, self.K))
        a = self.apetito.copy()
        if self.barajado is None: pass
        p = np.exp((a - a.max()) / self.tau); p /= p.sum()
        out = []
        for _ in range(self.K):
            if self.rng.random() < self.eps: out.append(int(self.rng.integers(0, S)))
            else: out.append(int(self.rng.choice(S, p=p)))
        return out

    def pregunta_dirigida(self, t):
        """busca una hipotesis con apoyo pero sin validar y una fuente INDEPENDIENTE (otro grupo) y de OTRA modalidad
        que la cubra: es buscar la refutacion/confirmacion que falta, no leer lo que venga."""
        mejor = None
        for f in range(self.NF):
            e = self.eff(f, t)
            if not e: continue
            v, w = max(e.items(), key=lambda kv: kv[1])
            if w >= self.k_val: continue
            if mejor is None or w > mejor[0]: mejor = (w, f, v)
        if mejor is None: return None
        w, f, v = mejor
        grupos = set(self.apoyo[f][v].keys()); mods = set()
        for g, (tg, mg) in self.apoyo[f][v].items(): mods |= mg
        cands = []
        for s in self.fs:
            if not self.cob_mask[s.i, f] or self.uf.find(s.i) in grupos: continue
            bono = 0.3 if s.mod not in mods else 0.0
            cands.append((self.apetito[s.i] + bono + 0.01 * self.rng.random(), s.i))
        if not cands: return None
        return max(cands)[1], f

    # ---------- consumir un item
    def consume(self, s_i, f, t, dirigido=False):
        s = self.fs[s_i]
        v, rasgo = s.dice(f, t)
        if v < 0:                                                        # la fuente no sabe (otra colonia que se abstiene)
            self.consumo[s_i] += 1; self.consumo_rec.append((t, s_i)); self._upd_apetito(s_i, -0.02); return
        if s.mod == 'video' and self.rng.random() > self.p_dec:      # el decodificador congelado lee mal el cuadro
            v = int((v + self.rng.integers(1, self.V)) % self.V)
        self.consumo[s_i] += 1; self.consumo_rec.append((t, s_i))
        self.log[s_i, f] = v; self.log_t[s_i, f] = t; self.log_r[s_i, f] = rasgo
        self.ultimo[f] = v; self.cuenta[f, v] += 1
        if self.memoria != 'cuarentena':
            self._apetito_simple(s_i, f, v, t); return
        g = self.uf.find(s_i)
        if self.ancla and self.base0[f] >= 0:                               # leccion R1: solo premia lo verificable por la base
            self.rep[s_i] = float(np.clip(self.rep[s_i] + (0.05 if v == self.base0[f] else -0.10), 0, 1))
        antes = self.validado(f, t)
        # un grupo que cambia de opinion retira su apoyo anterior en ese hecho
        for v2 in list(self.apoyo[f].keys()):
            if v2 != v and g in self.apoyo[f][v2]: del self.apoyo[f][v2][g]
        ent = self.apoyo[f].setdefault(v, {})
        if g in ent: ent[g] = (t, ent[g][1] | {s.mod})
        else: ent[g] = (t, {s.mod})
        self.t_nace.setdefault((f, v), t)
        despues = self.validado(f, t)
        # --- apetito y reputacion
        if antes >= 0 and antes == v:
            self._upd_apetito(s_i, -0.02)                                  # no aporta: ya lo sabia validado
            if not self.ancla: self.rep[s_i] = min(1, self.rep[s_i] + 0.02)
        elif antes >= 0 and antes != v:
            self._upd_apetito(s_i, -0.12)                                  # contradice lo validado: miente (o el mundo cambio)
            if not self.ancla: self.rep[s_i] = max(0, self.rep[s_i] - 0.10)
            self.pend[s_i].append((f, v, t, int(self.base[f])))
        else:
            self.pend[s_i].append((f, v, t, int(self.base[f])))
        if despues >= 0 and despues != antes:                              # se valido (o cambio) un hecho: credito a quien lo dijo
            self._valida(f, despues, t)
        # repetida: si la fuente esta en un grupo con otra ya leida, no aporta
        if self.uf.find(s_i) != s_i or any(self.uf.find(o) == g and o != s_i and self.consumo[o] > 0 for o in range(self.S)):
            self._upd_apetito(s_i, -0.15)

    def _valida(self, f, v, t):
        nuevo = self.base[f] != v
        if v == self.m.verdad[f] and f not in self.t_validado: self.t_validado[f] = t
        if (f, v) in self.t_nace:
            mods = set()
            for g, (tg, mg) in self.apoyo[f][v].items(): mods |= mg
            self.t_valid_hist.append((f, self.t_nace[(f, v)], t, len(mods) >= 2))
        self.sin_consolidar.add(f)
        for ev in self.m.eventos:
            if ev[1] == f and ev[3] == v and f not in self.primera_fuente_cambio:
                # ¿que tipo de fuente dio la primera afirmacion del valor nuevo?
                cand = [(self.log_t[s, f], s) for s in range(self.S) if self.log[s, f] == v and self.log_t[s, f] >= ev[0]]
                if cand: self.primera_fuente_cambio[f] = self.fs[min(cand)[1]].tipo
        for s in range(self.S):
            keep = []
            for (ff, vv, tt, b) in self.pend[s]:
                if ff != f: keep.append((ff, vv, tt, b)); continue
                if vv == v:
                    self._upd_apetito(s, 0.20 if nuevo else 0.03)
                    if not self.ancla: self.rep[s] = min(1, self.rep[s] + 0.05)
                else:
                    self._upd_apetito(s, -0.15)
                    if not self.ancla: self.rep[s] = max(0, self.rep[s] - 0.10)
            self.pend[s] = keep
        for s in range(self.S):
            if self.rep[s] < 0.4 and self.t_rep_baja[s] < 0: self.t_rep_baja[s] = t

    def _apetito_simple(self, s_i, f, v, t):
        """curiosidad SIN cuarentena: sube si trae algo nuevo o coincide con la mayoria, baja si la contradice o repite"""
        c = self.cuenta[f]
        if c.sum() <= 1: self._upd_apetito(s_i, 0.10); return
        may = int(np.argmax(c))
        if v == may: self._upd_apetito(s_i, 0.03 if c[v] < 4 else -0.03)
        else: self._upd_apetito(s_i, -0.10)

    def _upd_apetito(self, s_i, d):
        if self.barajado: s_i = int(self.rng.integers(0, self.S))
        self.apetito[s_i] = float(np.clip(self.apetito[s_i] + d, 0, 1))

    # ---------- deteccion de copias
    def detecta_copias(self, t):
        S = self.S
        for a in range(S):
            for b in range(a + 1, S):
                if self.uf.find(a) == self.uf.find(b): continue
                comp = (self.log[a] >= 0) & (self.log[b] >= 0) & (np.abs(self.log_t[a] - self.log_t[b]) < 300)
                n = comp.sum()
                if n < 4: continue
                if np.array_equal(self.log[a][comp], self.log[b][comp]) and np.array_equal(self.log_r[a][comp], self.log_r[b][comp]):
                    self.uf.union(a, b)
                    self.grupo_desde[(a, b)] = t
                    fa, fb = self.fs[a], self.fs[b]
                    es_copia = (fa.copia_de is fb) or (fb.copia_de is fa) or (fa.copia_de is not None and fa.copia_de is fb.copia_de)
                    if not es_copia: self.n_grupos_falsos += 1
                    # reputacion del grupo = la del representante: se la pasamos
                    r = self.uf.find(a); self.rep[r] = min(self.rep[a], self.rep[b])

    # ---------- sueno
    def duerme(self, t):
        for f in list(self.sin_consolidar):
            v = self.validado(f, t)
            if v >= 0: self.base[f] = v; self.consolidadas += 1
        self.sin_consolidar = set(); self.n_suenos += 1

    # ---------- un paso
    def paso(self, t):
        fuentes = self.elige(t)
        if self.preguntas and self.memoria == 'cuarentena':
            q = self.pregunta_dirigida(t)
            if q is not None:
                s_i, f = q; fuentes = fuentes[:-1]
                self.consume(s_i, f, t, dirigido=True)
        for s_i in fuentes:
            self.consume(s_i, self.fs[s_i].hecho_al_azar(), t)
        if self.memoria == 'cuarentena' and t % 10 == 9: self.detecta_copias(t)
        if self.sueno == 'fijo' and t % 100 == 99: self.duerme(t)
        if self.sueno == 'decide' and len(self.sin_consolidar) >= 10: self.duerme(t)

# ================================================================ brazos
BRAZOS = {
    'grandes':    dict(memoria='ultimo', eleccion='azar'),
    'mayoria':    dict(memoria='mayoria', eleccion='azar'),
    'curios':     dict(memoria='mayoria', eleccion='apetito'),
    'cuar':       dict(memoria='cuarentena', eleccion='azar'),
    'completo':   dict(memoria='cuarentena', eleccion='apetito'),
    'sin_amarre': dict(memoria='cuarentena', eleccion='apetito', amarre=False),
    'barajado':   dict(memoria='cuarentena', eleccion='apetito', barajado=True),
    'oraculo':    dict(memoria='cuarentena', eleccion='oraculo'),
    'preguntas':  dict(memoria='cuarentena', eleccion='apetito', preguntas=True),
    'sueno_fijo': dict(memoria='cuarentena', eleccion='apetito', sueno='fijo'),
    'sueno_decide': dict(memoria='cuarentena', eleccion='apetito', sueno='decide'),
    'ancla':      dict(memoria='cuarentena', eleccion='apetito', ancla=True, rep0=0.3),
    'ancla_sueno': dict(memoria='cuarentena', eleccion='apetito', ancla=True, rep0=0.3, sueno='decide'),
}

# ================================================================ medidas
def mide(sis, mundo, fuentes, curva, t_final):
    NF = mundo.NF
    r = sis.respuestas(t_final)
    verdad = mundo.verdad
    ok = r == verdad
    abst = r < 0
    # mentiras creidas: respuesta erronea que coincide con la mentira sistematica de alguna fuente
    ment = np.zeros(NF, bool)
    for s in fuentes:
        for f, v in s.mentiras.items():
            if r[f] == v and v != verdad[f]: ment[f] = True
    # verdades nuevas: correctas al final que no estaban correctas en la base inicial
    nuevas = int((ok & (sis.base0 != verdad)).sum())
    items = int(sis.consumo.sum())
    tipos = sorted(set(s.tipo for s in fuentes))
    # preferencias en los ultimos 100 pasos
    rec = [s for (tt, s) in sis.consumo_rec if tt >= t_final - 100]
    pref = {tp: round(sum(1 for s in rec if fuentes[s].tipo == tp) / max(1, len(rec)), 3) for tp in tipos}
    n_tipo = {tp: sum(1 for s in fuentes if s.tipo == tp) for tp in tipos}
    pref_rel = {tp: round(pref[tp] / (n_tipo[tp] / len(fuentes)), 2) for tp in tipos}   # 1 = como al azar
    # mentirosas detectadas (rep < 0.4)
    ments = [s.i for s in fuentes if s.tipo == 'mentirosa']
    fiab = [s.i for s in fuentes if s.tipo in ('fiable', 'especial')]
    t_det = [int(sis.t_rep_baja[i]) for i in ments if sis.t_rep_baja[i] >= 0]
    falsas = int(sum(1 for i in fiab if sis.rep[i] < 0.4))
    # copias: pares (copia, original)
    pares = [(s.i, s.copia_de.i) for s in fuentes if s.copia_de is not None]
    det = [sis.grupo_desde.get((min(a, b), max(a, b))) for a, b in pares]
    det_ok = [sis.uf.find(a) == sis.uf.find(b) for a, b in pares]
    # cambios: pasos hasta que la respuesta es el valor nuevo (medido en la curva de respuestas guardada)
    t_cambio = []; via = []
    for (t0, f, viejo, nuevo) in mundo.eventos:
        tt = next((tc for (tc, rr) in curva if tc >= t0 and rr[f] == nuevo), None)
        t_cambio.append((tt - t0) if tt is not None else (t_final - t0))
        via.append(sis.primera_fuente_cambio.get(f, '-'))
    # amarre: tiempo hasta validar por hecho (bimodal vs no)
    tv_bi = [tv - tn for (f, tn, tv, bi) in sis.t_valid_hist if bi]
    tv_no = [tv - tn for (f, tn, tv, bi) in sis.t_valid_hist if not bi]
    apet = {tp: round(float(np.mean([sis.apetito[s.i] for s in fuentes if s.tipo == tp])), 2) for tp in tipos}
    repu = {tp: round(float(np.mean([sis.rep[s.i] for s in fuentes if s.tipo == tp])), 2) for tp in tipos}
    return dict(acierto=float(ok.mean()), apetito=apet, reputacion=repu, errores=float((~ok & ~abst).mean()), abstiene=float(abst.mean()),
                mentiras=int(ment.sum()), nuevas=nuevas, items=items, efic=round(nuevas / items * 100, 3),
                pref=pref, pref_rel=pref_rel, t_det_mentirosa=(int(np.median(t_det)) if t_det else None),
                n_ment_det=len(t_det), n_ment=len(ments), falsas_alarmas=falsas,
                t_det_copia=(int(np.median([d for d in det if d is not None])) if any(d is not None for d in det) else None),
                copias_det=int(sum(det_ok)), copias=len(pares), grupos_falsos=int(sis.n_grupos_falsos),
                t_cambio=(float(np.median(t_cambio)) if t_cambio else None), t_cambio_lista=t_cambio, via_cambio=via,
                tv_bimodal=(float(np.median(tv_bi)) if tv_bi else None), tv_unimodal=(float(np.median(tv_no)) if tv_no else None),
                n_bimodal=len(tv_bi), n_unimodal=len(tv_no), suenos=sis.n_suenos, consolidadas=sis.consolidadas,
                base_ok_fin=float((sis.base == verdad).mean()))

def corre(seed, regimen, brazos, T=600, K=3, log=print, extra=None):
    rng_m = np.random.default_rng(seed)
    out = {}
    for b in brazos:
        # mismo mundo y mismas fuentes por semilla (reconstruidos con la misma semilla) para que los brazos sean pareados
        rng = np.random.default_rng(seed)
        mundo = Mundo(rng, T=T)
        fuentes = arma_fuentes(mundo, np.random.default_rng(seed + 1000), regimen)
        cfg = dict(BRAZOS[b]); cfg.update(extra or {})
        sis = Sistema(mundo, fuentes, np.random.default_rng(seed + 2000), K=K, **cfg)
        curva = []; acc = []
        for t in range(T):
            mundo.paso(t)
            sis.paso(t)
            if t % 10 == 9 or t in mundo.cambios or t + 1 in mundo.cambios:
                rr = sis.respuestas(t); curva.append((t, rr)); acc.append((t, float((rr == mundo.verdad).mean()), int(((rr >= 0) & (rr != mundo.verdad)).sum())))
        m = mide(sis, mundo, fuentes, curva, T - 1)
        m['curva'] = acc
        # acierto medio a lo largo de la vida (verdades por item acumuladas) y pasos hasta 0.7
        m['acierto_medio'] = float(np.mean([a for (_, a, _) in acc]))
        m['t_070'] = next((tt for (tt, a, _) in acc if a >= 0.7), None)
        m['errores_medio'] = float(np.mean([e for (_, _, e) in acc]))
        out[b] = m
        log(f"  s{seed} {regimen:8s} {b:12s} acierto {m['acierto']:.2f} err {m['errores']:.2f} abst {m['abstiene']:.2f} mentiras {m['mentiras']:2d} "
            f"nuevas {m['nuevas']:2d} t_ment {m['t_det_mentirosa']} copias {m['copias_det']}/{m['copias']} (falsos {m['grupos_falsos']}) "
            f"t_cambio {m['t_cambio']} bi/uni {m['tv_bimodal']}/{m['tv_unimodal']} pref {m['pref_rel']}")
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--semillas', type=int, default=10); ap.add_argument('--regimen', default='honesto')
    ap.add_argument('--brazos', default='grandes,mayoria,curios,cuar,completo,sin_amarre,barajado,oraculo')
    ap.add_argument('--T', type=int, default=600); ap.add_argument('--K', type=int, default=3)
    ap.add_argument('--out', default=None); ap.add_argument('--humo', action='store_true')
    ap.add_argument('--extra', default='')     # p.ej. "k_val=3.0,W=100"
    a = ap.parse_args()
    extra = {}
    for kv in a.extra.split(','):
        if '=' in kv:
            k, v = kv.split('='); extra[k] = float(v) if '.' in v else int(v)
    brazos = a.brazos.split(',')
    t0 = time.time()
    todo = {}
    semillas = [0] if a.humo else list(range(a.semillas))
    lineas = []
    def log(s): print(s); lineas.append(s); sys.stdout.flush()
    for seed in semillas:
        todo[seed] = corre(seed, a.regimen, brazos, T=a.T, K=a.K, log=log, extra=extra)
    log(f"CPU {time.time() - t0:.0f} s")
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as fh: json.dump(dict(regimen=a.regimen, brazos=brazos, T=a.T, K=a.K, extra=extra, res={str(k): v for k, v in todo.items()}), fh)
        with open(a.out.replace('.json', '.txt'), 'w', encoding='utf-8') as fh: fh.write('\n'.join(lineas))

if __name__ == '__main__':
    main()
