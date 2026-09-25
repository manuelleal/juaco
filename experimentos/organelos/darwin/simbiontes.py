"""simbiontes.py — ENDOSIMBIOSIS, escalon 1 (equipo organelos, Opus B, 24-sep-2026). Codigo NUEVO (no es copia de nada).

MISION: llegar a la AGI por este camino.

Lo usa motor_endo.py (construido por anclas desde juaco_eco/motor_eco3.py con construye_endo.py) a traves de ganchos. Con simb=None
el motor no crea esta ecologia y es motor_eco3 BIT A BIT (arnes identidad_endosimbiosis.py).

EL MUNDO GANA UN SEGUNDO HABITANTE: REPLICADORES LIBRES (proto-organelos). Nadie los disena como organos del bicho.
  R1 GENOMA: g en R^6 (el mismo espacio de la retina del mundo: los 4 patrones PAT de 6 pixeles). Memoria nueva por replicador: 6 numeros
     + energia + posicion. Nacen con g ~ N(0, 1) por componente (rng propio del mundo de simbiontes [seed, 0, 30, 0]).
  R2 NICHO LIBRE: se pegan a los objetos del mundo SIN comerselos (no quitan ni ponen objetos: el mundo del bicho no cambia; arnes (C)).
     Afinidad por el objeto de su celda a = sigmoide(g . PAT[letra]). Si estan sobre un objeto se quedan con probabilidad a; si no, dan
     un paso de +-1. Ganan F * a / m (m = replicadores en esa celda: el exudado se reparte) y pagan c0 + c2 * |g|^2 por paso.
     CORREGIDO tras los humos (prediccion mia REFUTADA): yo escribi que el nicho libre no distingue letras porque las LLEGADAS son
     uniformes. Lo que QUEDA en el mundo no lo es: el bicho se come A y C y rechaza B y D, asi que las existencias se cargan de veneno y
     sal, y los libres se adaptan a eso (I medio de los libres entre -0.1 y -0.3 en los humos). El nicho libre empuja al simbionte EN
     CONTRA de lo que le serviria al bicho: domesticarlo es remar contra su vida libre.
  R3 SE COPIAN CON ERRORES: con e >= e_rep se parten en dos (misma celda, e/2 cada uno); el hijo muta cada componente con p_mut
     (N(0, sigma)). Mueren con e <= 0 o con p_muerte por paso. Tope de SEGURIDAD computacional (declarado): tope_por_esc * esc libres;
     con el tope alcanzado una particion no ocurre y se cuenta ('bloq_libres').
ENDOSIMBIOSIS (reglas locales, por contacto):
  S1 TRAGAR: un cuerpo del bicho en la celda de uno o mas libres traga a uno (al azar entre los de su celda) con probabilidad p_trag por
     paso. Con p_queda el tragado SIGUE VIVO adentro (si el cuerpo no tiene ya uno: un solo simbionte por cuerpo); si no, lo DIGIERE
     (E += e_dig, tope 1.5 como la comida).
  S2 COSTO DE ALOJAR: un cuerpo con simbionte paga costo_h de E por paso (la fusion tiene que pagarse sola).
  S3 PERDIDA: el simbionte de adentro muere con p_pierde por paso; en el parto no pasa al hijo con p_falla.
  S4 HERENCIA VERTICAL: en el parto el hijo recibe una COPIA del simbionte del padre (el padre conserva el suyo), MUTADA con las mismas
     p_mut y sigma de la vida libre: el genoma de adentro sigue mutando.
  S5 CANAL (generico, declarado, simetrico en signo): el simbionte lee el patron del objeto que el cuerpo tiene en la boca y SUMA
     k_canal * tanh(g . PAT[letra]) a la entrada de la boca del cerebro (Vb del carro FABRICA_SIMB, antes de la sigmoide). No codifica
     la respuesta: el signo y la letra salen del genoma del simbionte, que viene de la vida libre, donde el nicho no distingue letras.
  S6 VIVERO (antes de t_corte): el banco de donantes del motor guarda, alineado con cada genoma de padre, el simbionte del padre; el
     fundador que sale de esa entrada del banco hereda ese simbionte mutado (o ninguno). Desde t_corte nadie repone nada.
BRAZOS (en todos el bicho evoluciona como VIDA de ECO: donante 'padre', p_mut 0.05 en sus 25 genes):
  VIDA_S     todo lo de arriba.
  INERTE     igual, pero el canal NO actua (el simbionte se traga, se queda, cuesta y se hereda; no toca la boca).
  BARAJADO   igual que VIDA_S, pero en cada parto (y en cada fundador del vivero) el GENOMA del simbionte heredado se sustituye por el de
             un libre AL AZAR (la presencia si se hereda). Sin libres vivos se conserva el del padre y se cuenta ('baraja_sin_libres').
  SIN_TRAGAR p_trag = 0 (los libres viven igual; el bicho es motor_eco3 bit a bit en la fisica: arnes (C)).
  AZAR_S     herencia SIN seleccion: el estado del simbionte de cada cuerpo nuevo (presencia y genoma) sale de una entrada AL AZAR de un
             anillo de los ultimos banco_s estados NUEVOS (el de cada cuerpo nuevo, el de cada simbionte adquirido al tragar y un 'ninguno'
             por cada perdida interna: el flujo en los dos sentidos), mutada.
             El exito del cuerpo nunca decide la copia de su simbionte (el anillo guarda el estado NUEVO, como donante='azar' de ECO).
RNG: TODO lo de esta ecologia sale de UN generador [seed, 0, 30, 0]; ningun rng del mundo, de la pista, de los cuerpos ni del genoma se
toca (arnes (C): con p_trag = 0 el bicho es motor_eco3 bit a bit).
"""
import math
import numpy as np

ETQ_SIMB = 30
LETRAS = ('A', 'B', 'C', 'D')
IDX = {k: i for i, k in enumerate(LETRAS)}
BRAZOS = ('VIDA_S', 'INERTE', 'BARAJADO', 'SIN_TRAGAR', 'AZAR_S')
# Valores de la ecologia libre (F, c0, c2, e0, tope) y de adquisicion (p_trag, p_queda) fijados en una exploracion de VIABILIDAD de un
# proceso (semillas de practica 22990, 22996, 22997; declarada en el preregistro): con F 0.02 / c ~0.002 los libres llenan el tope; con
# F 0.01 / c ~0.004 se extinguen en 1000 pasos; con c0 0.001 se extinguieron en el humo 1 (22990, t ~4000 y ~13000). Version 2 (esta):
# c0 0.0003, c2 0.0001 (un libre sin comer dura ~1000 pasos), tope 60*esc, p_trag 0.005. Se fijo ANTES del humo final.
SIMB_DEF = dict(brazo='VIDA_S', n0_por_esc=4, tope_por_esc=60, F=0.01, c0=0.0003, c2=0.0001, e0=0.9, e_rep=1.0, p_muerte=0.001,
                p_mut=0.25, sigma=0.3, p_trag=0.005, p_queda=0.25, e_dig=0.02, costo_h=0.0001, p_pierde=1e-4, p_falla=0.05,
                k_canal=1.0, banco_s=200, max_ind=200000)


def indice(g, PATM):
    """I(g) = (tanh(g.A) + tanh(g.C) - tanh(g.B) - tanh(g.D)) / 4: cuanto EMPUJA el simbionte a morder lo bueno (A comida, C agua) y a
    no morder lo malo (B veneno, D sal). Balanceado: 2 letras buenas y 2 malas, mezcla uniforme. SOLO instrumento de lectura."""
    s = np.tanh(PATM @ np.asarray(g, float))
    return float((s[0] + s[2] - s[1] - s[3]) / 4.0)


class Ecologia:
    def __init__(self, seed, L, esc, simb, E_, PAT):
        mal = set(simb) - set(SIMB_DEF)
        if mal: raise SystemExit(f"SIMB: claves desconocidas {sorted(mal)}")
        C = dict(SIMB_DEF); C.update(simb); self.C = C
        if C['brazo'] not in BRAZOS: raise SystemExit(f"SIMB: brazo {C['brazo']!r} no es uno de {BRAZOS}")
        if E_ is None: raise SystemExit("SIMB: la endosimbiosis exige eco=dict(...)")
        if E_['donante'] != 'padre': raise SystemExit("SIMB: el bicho hereda de su padre (donante='padre'); AZAR es del simbionte (AZAR_S)")
        if E_['ckpt_cada'] or E_['estado'] is not None: raise SystemExit("SIMB: sin checkpoints (el estado de los simbiontes no va en el pickle)")
        self.rs = np.random.default_rng([seed, 0, ETQ_SIMB, 0])
        self.L = L; self.esc = esc; self.E_ = E_; self.tc = E_['t_corte']
        self.PATM = np.array([PAT[k] for k in LETRAS], float)
        self.canal_on = C['brazo'] in ('VIDA_S', 'BARAJADO', 'AZAR_S')
        self.p_trag = 0.0 if C['brazo'] == 'SIN_TRAGAR' else float(C['p_trag'])
        n0 = int(C['n0_por_esc'] * esc); self.tope = int(C['tope_por_esc'] * esc)
        rs = self.rs
        self.pos = rs.integers(L, size=n0).astype(np.int64)
        self.g = rs.normal(0.0, 1.0, (n0, 6))
        self.e = np.full(n0, float(C['e0']))
        self.bank_p = []          # alineado con ES['banco'] del motor: simbionte del padre (None o genoma)
        self.anillo = []          # AZAR_S: estados NUEVOS (None o genoma)
        self.ev = dict(tragados=0, digeridos=0, quedan=0, rechazo_lleno=0, herencias=0, herencias_mutadas=0, fallas_herencia=0,
                       perdidas_internas=0, muertes_con_huesped=0, fundadores_con_simb=0, barajados=0, baraja_sin_libres=0,
                       azar_sorteos=0, nac_libres=0, muertes_libres=0, bloq_libres=0, decisiones_canal=0, decisiones_sin_canal=0,
                       contactos=0, libres_extintos_t=None)
        self.dec = {q: {k: [0, 0] for k in LETRAS} for q in ('con', 'sin')}   # decisiones de boca: [vistos, mordidos]
        self.serie = []           # [t, cuerpos, con_simb, libres, I_libres, I_dentro, g_libres(6), g_dentro(6)]
        self.ind = []             # nacidos desde t_corte: [lin, k, t_nace, t_muere, hijos, simb_al_nacer, simb_al_morir, I_nac]
        self.don = []             # cada cuerpo nuevo: [t, I del genoma que DE VERDAD se transmite (antes de mutar) o None, es_parto]
        self.err60 = None

    # ------------------------------------------------------------------ genoma
    def _muta(self, g):
        rs = self.rs; C = self.C
        u = rs.random(6); z = rs.normal(0.0, C['sigma'], 6)
        h = np.where(u < C['p_mut'], g + z, g)
        return h, int((u < C['p_mut']).any())

    def _sm(self, g):
        """estado del simbionte de un cuerpo: (genoma, canal por letra, I)"""
        d = np.tanh(self.PATM @ g) * float(self.C['k_canal'])
        return (g, {k: float(d[i]) for i, k in enumerate(LETRAS)}, indice(g, self.PATM))

    def canal(self, b):
        if not self.canal_on or b.sm is None: return None
        return b.sm[1]

    def decision(self, b, kk, mordio):
        q = 'con' if (self.canal_on and b.sm is not None) else 'sin'
        self.dec[q][kk][0] += 1; self.dec[q][kk][1] += int(mordio)
        if q == 'con': self.ev['decisiones_canal'] += 1
        else: self.ev['decisiones_sin_canal'] += 1

    # ------------------------------------------------------------------ banco del vivero (alineado con ES['banco'])
    def banco_ini(self, n):
        self.bank_p = [None] * n

    def _anillo_push(self, st):
        self.anillo.append(None if st is None else st.copy())
        if len(self.anillo) > int(self.C['banco_s']): self.anillo.pop(0)

    def _hereda(self, g_donante, t, es_parto):
        """genoma del simbionte de un cuerpo nuevo a partir del genoma donante (None -> ninguno), segun el brazo.
        Registra TODA transmision: [t, I de lo que de verdad pasa (antes de mutar) o None, 1 si es parto / 0 si es fundador del vivero]."""
        C = self.C; rs = self.rs
        if g_donante is None:
            self.don.append([int(t), None, int(es_parto)])
            return None
        if rs.random() < C['p_falla']:
            self.ev['fallas_herencia'] += 1
            self.don.append([int(t), None, int(es_parto)])
            return None
        g0 = g_donante
        if C['brazo'] == 'BARAJADO':
            if len(self.e): g0 = self.g[int(rs.integers(len(self.e)))].copy(); self.ev['barajados'] += 1
            else: self.ev['baraja_sin_libres'] += 1
        self.don.append([int(t), round(indice(g0, self.PATM), 6), int(es_parto)])   # lo que DE VERDAD se transmite (antes de mutar)
        h, m = self._muta(g0); self.ev['herencias'] += 1; self.ev['herencias_mutadas'] += m
        return h

    def parto(self, b, H, t):
        """gancho del motor tras crear al hijo H del padre b (y tras el append del banco de genomas del motor)."""
        E_ = self.E_
        if E_['banco']:
            self.bank_p.append(None if b.sm is None else b.sm[0].copy())
            if len(self.bank_p) > E_['banco']: self.bank_p.pop(0)
        if self.C['brazo'] == 'AZAR_S':
            don = None
            if self.anillo: don = self.anillo[int(self.rs.integers(len(self.anillo)))]; self.ev['azar_sorteos'] += 1
            h = self._hereda(don, t, 1)
            self._anillo_push(h)
        else:
            h = self._hereda(None if b.sm is None else b.sm[0], t, 1)
        H.sm = None if h is None else self._sm(h)
        H.sm_nac = int(H.sm is not None); H.sm0 = (None if H.sm is None else H.sm[2])

    def funda(self, F, ib, t):
        """gancho del motor tras poner un fundador del vivero desde la entrada ib del banco (None: banco vacio -> sin simbionte)."""
        if self.C['brazo'] == 'AZAR_S':
            don = None
            if self.anillo: don = self.anillo[int(self.rs.integers(len(self.anillo)))]; self.ev['azar_sorteos'] += 1
            h = self._hereda(don, t, 0); self._anillo_push(h)
        else:
            don = None if ib is None else self.bank_p[ib]
            h = self._hereda(don, t, 0)
        F.sm = None if h is None else self._sm(h)
        F.sm_nac = int(F.sm is not None); F.sm0 = (None if F.sm is None else F.sm[2])
        self.ev['fundadores_con_simb'] += F.sm_nac

    # ------------------------------------------------------------------ un paso del mundo de los simbiontes
    def paso(self, t, objs, cuerpos):
        C = self.C; rs = self.rs; L = self.L; PATM = self.PATM
        lett = np.full(L, -1, np.int64)
        for x, k in objs.items(): lett[x] = IDX[k]
        n = len(self.e)
        if n:
            lp = lett[self.pos]; on = lp >= 0
            aff = np.zeros(n)
            if on.any(): aff[on] = 1.0 / (1.0 + np.exp(-(self.g[on] * PATM[lp[on]]).sum(1)))
            u = rs.random(n); mv = rs.integers(0, 2, n) * 2 - 1
            quieto = on & (u < aff)
            self.pos = np.where(quieto, self.pos, (self.pos + mv) % L)
            lp = lett[self.pos]; on = lp >= 0
            occ = np.bincount(self.pos, minlength=L)
            gan = np.zeros(n)
            if on.any():
                a2 = 1.0 / (1.0 + np.exp(-(self.g[on] * PATM[lp[on]]).sum(1)))
                gan[on] = C['F'] * a2 / occ[self.pos[on]]
            self.e = self.e + gan - (C['c0'] + C['c2'] * (self.g * self.g).sum(1))
            muere = (self.e <= 0) | (rs.random(n) < C['p_muerte'])
            nm = int(muere.sum())
            if nm:
                vive = ~muere; self.pos = self.pos[vive]; self.g = self.g[vive]; self.e = self.e[vive]; self.ev['muertes_libres'] += nm
            n = len(self.e)
            rep = np.flatnonzero(self.e >= C['e_rep'])
            if len(rep):
                cupo = max(0, self.tope - n)
                if len(rep) > cupo: self.ev['bloq_libres'] += len(rep) - cupo; rep = rep[:cupo]
                if len(rep):
                    self.e[rep] = self.e[rep] / 2.0
                    u = rs.random((len(rep), 6)); z = rs.normal(0.0, C['sigma'], (len(rep), 6))
                    gh = np.where(u < C['p_mut'], self.g[rep] + z, self.g[rep])
                    self.pos = np.concatenate([self.pos, self.pos[rep]]); self.g = np.concatenate([self.g, gh])
                    self.e = np.concatenate([self.e, self.e[rep]]); self.ev['nac_libres'] += len(rep)
            if len(self.e) == 0 and self.ev['libres_extintos_t'] is None: self.ev['libres_extintos_t'] = int(t)
        # S1 tragar (por contacto), en el orden de la lista de cuerpos
        if self.p_trag > 0 and len(self.e):
            occ = np.bincount(self.pos, minlength=L)
            quitar = []
            for b in cuerpos:
                if not b.vivo or occ[b.pos] == 0: continue
                self.ev['contactos'] += 1
                if rs.random() >= self.p_trag: continue
                idx = [i for i in np.flatnonzero(self.pos == b.pos) if i not in quitar]
                if not idx: continue
                i = int(idx[int(rs.integers(len(idx)))]); quitar.append(i); occ[b.pos] -= 1
                self.ev['tragados'] += 1
                if b.sm is None and rs.random() < C['p_queda']:
                    b.sm = self._sm(self.g[i].copy()); self.ev['quedan'] += 1
                    if C['brazo'] == 'AZAR_S': self._anillo_push(b.sm[0])
                else:
                    if b.sm is not None: self.ev['rechazo_lleno'] += 1
                    b.E = min(b.E + C['e_dig'], 1.5); self.ev['digeridos'] += 1
            if quitar:
                vive = np.ones(len(self.e), bool); vive[quitar] = False
                self.pos = self.pos[vive]; self.g = self.g[vive]; self.e = self.e[vive]
                if len(self.e) == 0 and self.ev['libres_extintos_t'] is None: self.ev['libres_extintos_t'] = int(t)
        # S2 costo de alojar y S3 perdida interna
        con = [b for b in cuerpos if b.vivo and b.sm is not None]
        if con:
            u = rs.random(len(con))
            for b, x in zip(con, u):
                b.E -= C['costo_h']
                if x < C['p_pierde']:
                    b.sm = None; self.ev['perdidas_internas'] += 1
                    if C['brazo'] == 'AZAR_S': self._anillo_push(None)   # el anillo registra el flujo en los dos sentidos

    # ------------------------------------------------------------------ registro
    def registra(self, b, tm):
        if b.sm is not None and tm >= 0: self.ev['muertes_con_huesped'] += 1
        if self.tc is not None and b.tn >= self.tc and len(self.ind) < int(self.C['max_ind']):
            self.ind.append([int(b.lin), int(b.k), int(b.tn), int(tm), int(b.hijos), int(b.sm_nac), int(b.sm is not None),
                             (None if not b.sm_nac or b.sm0 is None else round(b.sm0, 6))])

    def muestra(self, t, cuerpos):
        vv = [b for b in cuerpos if b.vivo]
        dentro = [b.sm[0] for b in vv if b.sm is not None]
        R = lambda v: [round(float(x), 5) for x in v]
        Il = (round(float(np.mean([indice(x, self.PATM) for x in self.g])), 6) if len(self.e) else None)
        Id = (round(float(np.mean([indice(x, self.PATM) for x in dentro])), 6) if dentro else None)
        self.serie.append([int(t), len(vv), len(dentro), int(len(self.e)), Il, Id,
                           (R(self.g.mean(0)) if len(self.e) else None), (R(np.mean(dentro, 0)) if dentro else None)])

    def salida(self, t_fin, cuerpos, ES):
        vv = [b for b in cuerpos if b.vivo]
        dentro = [[int(b.lin), int(b.k), int(b.gen)] + [round(float(x), 5) for x in b.sm[0]] for b in vv if b.sm is not None]
        libres = [[round(float(x), 5) for x in gg] for gg in self.g[:300]]
        return dict(cfg=dict(self.C), canal_on=int(self.canal_on), p_trag_efectiva=self.p_trag, eventos=dict(self.ev),
                    decisiones=self.dec, serie=self.serie, ind=self.ind, ind_trunc=int(len(self.ind) >= int(self.C['max_ind'])),
                    don=self.don, dentro_final=dentro, libres_final=libres, n_libres_final=int(len(self.e)),
                    I_libres_final=([round(indice(x, self.PATM), 6) for x in self.g[:300]]),
                    I_dentro_final=[round(indice(np.array(d[3:]), self.PATM), 6) for d in dentro],
                    err60=ES.get('err60'), t_trunc=ES.get('t_trunc'), banco_alineado=int(len(self.bank_p) == len(ES['banco'])))
