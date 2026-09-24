# ================================================================ FRANKENSTEIN -- los seis organos (fragmento; NO se importa solo)
# Este archivo es TEXTO FUENTE que construye_frankenstein.py pega en organismo_frankenstein.py, antes de `class Carro`.
# Los marcadores <<APR_CONSTANTES>> y <<APR_METODOS>> se sustituyen por los bloques VERBATIM de carros/APR.py (sha fijado).
# EXPLORATORIO -- no es dato. Mision: llegar a la AGI por este camino.
#
# PERILLAS (todas 0 == FABRICA bit a bit; b5 = la unica pieza de v14.2 que FABRICA (v14.1) no tiene):
#   b5          B-5 de v14.2 (organismo/organismo_v142.py:162-166): la division por conflicto se dispara tambien con R == 0.
#   mapa        1. MAPA leido por gradiente + FILTRO: campo de valor (lo que el tronco sabe) sobre los objetos del anillo; el
#                  cuerpo va hacia el lado de mayor campo; lo recordado malo (valor < -0.2) es PARED: el campo no pasa.
#                  Sin meta buena conocida -> lo de FABRICA (el objeto mas cercano). (subida_n6: grad + filtro, portado a 1D.)
#   curiosidad  2. CURIOSIDAD CON PRESUPUESTO: lo que la puerta no reconoce y ESTE cuerpo no probo se lee NEUTRO (0) en vez de
#                  con el a priori negativo de la via lenta; PRES lecturas por cuerpo, solo si el cuerpo aguanta (subida_n8b).
#   modelo      3. MODELO DE SI QUE PREDICE: la opcion de APR (aprende_barrer) VERBATIM: sobre lo malo conocido, la boca de
#                  FABRICA + una correccion aprendida por TD con el rasgo post = nivel predicho de la necesidad tras morder,
#                  calculado con lo SENTIDO (subida_n9b). Heredada.
#   lenta       4. MEMORIA LENTA CON REPASO (prototipo propio, CLS): Wc (N_NEC x 6), del LINAJE; cada REPASO pasos, si el
#                  cuerpo vivio mordidas, repasa UNA letra reciente y consolida lo que la memoria rapida dice de ella
#                  (delta con ETA_C). Se consulta cuando la puerta esta cerrada y habla mas fuerte que la via lenta del cuerpo.
#   herencia    5. HERENCIA DE LO VIVIDO: el padre VIVO pasa en el parto su TABLA (R mas reciente vivida por (letra,
#                  necesidad), y lo heredado para lo no vivido); el hijo la lee como nodo (subida_n10b, modo 'res', verbatim).
#   interruptor 6. INTERRUPTOR EXPLORAR/EXPLOTAR por necesidad: u = min(E, Ag). PELIGRO (u < PELIGRO): se cuida -> veta
#                  morder lo que SINTIO malo para su necesidad mas baja, y no prueba; HAMBRE (PELIGRO <= u < umbral): arriesga
#                  (la boca de hambre del tronco, sin veto, sin pruebas); SACIADO (u >= umbral): explora (solo aqui prueba).
import numpy as np

ORGANOS = ('mapa', 'curiosidad', 'modelo', 'lenta', 'herencia', 'interruptor')
PERILLAS = ('b5',) + ORGANOS
TODO = dict((k, 1) for k in PERILLAS)
LAMBDA_MAPA = 20.0     # mapa: el campo decae con exp(-d / 20) (20 = la mayor distancia del anillo original L = 40)
UMBRAL_META = 0.2      # mapa: meta = valor > 0.2 (el umbral de consolidacion del tronco)
UMBRAL_PARED = 0.2     # mapa: pared = valor < -0.2
PRES = 2               # curiosidad: lecturas neutras por cuerpo
PRUEBA_MIN = 0.5       # curiosidad sin interruptor: solo si min(E, Ag) > 0.5 (lo que O1 llama PRUEBA)
REPASO = 10            # lenta: un repaso cada 10 pasos
ETA_C = 0.02           # lenta: tasa de consolidacion
VENT_REPASO = 20       # lenta: repasa entre las ultimas 20 mordidas del cuerpo (= NODO_K)
PELIGRO = 0.3          # interruptor: por debajo, se cuida

# <<APR_CONSTANTES>>


def _perillas(p):
    if p is None: p = TODO
    malas = [k for k in p if k not in PERILLAS]
    if malas: raise SystemExit(f"FRANKENSTEIN: perillas desconocidas {malas}")
    return dict((k, int(p.get(k, 0))) for k in PERILLAS)


class _Organos:
    # ------------------------------------------------------------ comun
    def _fk_init(self, ctx):
        self._FK = any(self.PK.values()); self._B5 = bool(self.PK['b5'])
        self._fk_des = 0
        if not self._FK: return
        self._apr_init(ctx)                               # APR: _adS (lo SENTIDO por letra, del linaje), Q, contadores
        self._fk_vivido = False; self._fk_modo = 'hambre'; self._fk_cue2 = False
        self._fk_tgt = None; self._fk_cache = None; self._fk_sucio = True
        self._fk_pres = PRES; self._fk_probadas = set()
        self._fkWc = np.zeros((self.N_NEC, 6)); self._fk_tick = 0
        self._fk_st = dict(pasos_mapa=0, rodeos_mapa=0, pruebas=0, vetos_peligro=0, lenta_usa=0, repasos=0,
                           modo_pasos=dict(peligro=0, hambre=0, saciado=0),
                           mord_modo=dict(peligro=dict(), hambre=dict(), saciado=dict()), paquetes=0, recibidos=0)

    def _fk_paso(self, E, Ag, cue2):
        self._apr_paso(E, Ag)
        u = min(E, Ag)
        self._fk_modo = 'peligro' if u < PELIGRO else ('saciado' if u >= self._aU else 'hambre')
        self._fk_st['modo_pasos'][self._fk_modo] += 1
        self._fk_cue2 = cue2; self._fk_vivido = True

    def _fk_val(self, n, k):
        P = self.PAT[k]; kc = self._kenyon(P); fam = self._fam(kc, n)
        v = float((self.Wp[n] - self.Wn[n]) @ kc) if fam else float((self.Wps[n] - self.Wns[n]) @ P)
        if self.PK['lenta'] and not fam:
            wc = float(self._fkWc[n] @ P)
            if abs(wc) > abs(v): v = wc
        return v

    def _fk_vals(self):
        clave = (self._nm, self._fk_cue2)
        if self._fk_sucio or self._fk_cache is None or self._fk_cache[0] != clave:
            if self._fk_cue2: val = dict((k, min(self._fk_val(0, k), self._fk_val(1, k))) for k in 'ABCD')
            else: val = dict((k, self._fk_val(self._nm, k)) for k in 'ABCD')
            self._fk_cache = (clave, val); self._fk_sucio = False
        return self._fk_cache[1]

    # ------------------------------------------------------------ 1. MAPA (gradiente + filtro)
    def _fk_mapa(self, pos, objs, t, base):
        val = self._fk_vals(); L = self.L; wr = L; wl = L
        for x, k in objs.items():                         # FILTRO: la pared mas cercana a cada lado (lo recordado malo)
            if val[k] < -UMBRAL_PARED:
                dr = (x - pos) % L; dl = (pos - x) % L
                if dr and dr < wr: wr = dr
                if dl and dl < wl: wl = dl
        best = None
        for x, k in objs.items():                         # CAMPO: v * exp(-d / LAMBDA) por el lado que la pared no corta
            v = val[k]
            if v <= UMBRAL_META: continue
            if self.MEMORIA_RECHAZO and self._rech.get(x, -1) > t: continue
            dr = (x - pos) % L; dl = (pos - x) % L
            if dr == 0:
                cand = ((v, 0, False),)
            else:
                cand = tuple((v * np.exp(-dd / LAMBDA_MAPA), dd, izq) for dd, izq in ((dr, False), (dl, True)) if dd < (wl if izq else wr))
            for s, dd, izq in cand:
                if best is None or s > best[0]: best = (s, dd, izq, x, k, min(dr, dl))
        if best is None:
            self._fk_tgt = None; return base
        self._fk_tgt = best[3]; self._fk_st['pasos_mapa'] += 1
        if best[1] > best[5]: self._fk_st['rodeos_mapa'] += 1   # va por el lado LARGO: el corto tenia pared
        return (best[1], best[4], best[2])

    def _fk_d2(self, pos, objs, t):
        x = self._fk_tgt
        if x is not None and x in objs:
            L = self.L; return min((pos - x) % L, (x - pos) % L)
        return self._see(pos, objs, t)[0]

    # ------------------------------------------------------------ 2 + 4. lectura de la boca
    def _fk_lee(self, kk, kc, fa9, wt, na, E, Ag):
        P = self.PAT[kk]
        if self.PK['lenta'] and not fa9:
            wc = float(self._fkWc[na] @ P)
            if abs(wc) > abs(wt): wt = wc; self._fk_st['lenta_usa'] += 1
        if self.PK['curiosidad'] and not fa9 and wt < 0 and kk not in self._fk_probadas and self._fk_pres > 0:
            ok = (self._fk_modo == 'saciado') if self.PK['interruptor'] else (min(E, Ag) > PRUEBA_MIN)
            if ok: wt = 0.0; self._fk_pres -= 1; self._fk_st['pruebas'] += 1
        return wt

    # ------------------------------------------------------------ 3 + 6. la boca
    def _fk_boca(self, obs, kk, mordio, u9, pb):
        if self.PK['modelo']: mordio = self._opcion(obs, kk, mordio, u9, pb)
        if self.PK['interruptor'] and mordio and self._fk_modo == 'peligro':
            m = self._adS.get(kk)
            if m is not None:
                j = 0 if float(obs['E']) <= float(obs['Ag']) else 1
                if m[j] / m[2] < 0: mordio = False; self._fk_st['vetos_peligro'] += 1
        if mordio:
            mm = self._fk_st['mord_modo'][self._fk_modo]; mm[kk] = mm.get(kk, 0) + 1
        return mordio

    def _fk_dS(self, k, dS):
        self._apr_dS(k, dS); self._fk_probadas.add(k); self._fk_sucio = True

    # ------------------------------------------------------------ 4. repaso (consolidacion en la memoria lenta del linaje)
    def _fk_fin(self, info):
        if not self.PK['lenta']: return
        self._fk_tick += 1
        if self._fk_tick % REPASO or not self._mordh: return
        letras = sorted(set(z[1] for z in self._mordh[-VENT_REPASO:]))
        k = letras[(self._fk_tick // REPASO) % len(letras)]
        P = self.PAT[k]; kc = self._kenyon(P)
        for n in range(self.N_NEC):
            tgt = self._vnec(n, P, kc)
            self._fkWc[n] = self._fkWc[n] + ETA_C * (tgt - float(self._fkWc[n] @ P)) * P
        self._fk_st['repasos'] += 1; self._fk_sucio = True

    # ------------------------------------------------------------ vida y parto
    def _fk_muere(self, info):
        if self.PK['modelo']: self._apr_muere(info)

    def _fk_parir(self, info):
        if self.PK['modelo']: self._areal += R_PARTO; self._avent = 0   # APR v2: parir se SIENTE (+1)
        pk = {}
        if self.PK['herencia']:   # subida_n10b modo 'res' (verbatim): tabla (vivido + heredado)
            _tab = {}
            for _p7, _r7, _n7 in self._nodo: _tab[(tuple(float(_z) for _z in _p7), int(_n7))] = float(_r7)
            for _t9, _k9, _n9, _R9 in self._mordh: _tab[(tuple(float(_z9) for _z9 in self.PAT[_k9]), int(_n9))] = float(_R9)
            _o7 = {tuple(float(_z) for _z in self.PAT[_q7]): _i7 for _i7, _q7 in enumerate('ABCD')}
            pk['tabla'] = [[list(_c7[0]), _tab[_c7], _c7[1]] for _c7 in sorted(_tab, key=lambda _c7: (_c7[1], _o7.get(_c7[0], 99), _c7[0]))]
        if self.PK['modelo']: pk['Q'] = self._aw.copy()
        if self.PK['modelo'] or self.PK['interruptor']: pk['sentido'] = dict((k, list(v)) for k, v in self._adS.items())
        if self.PK['lenta']: pk['Wc'] = self._fkWc.copy()
        if not pk: return None
        self._fk_st['paquetes'] += 1
        return pk

    def _fk_nace(self, info):
        if self.PK['modelo']: self._apr_nace(info)
        self._fk_pres = PRES; self._fk_probadas = set(); self._fk_sucio = True; self._fk_tgt = None; self._fk_tick = 0
        mem = info.get('memoria')
        if not self._fk_vivido and isinstance(mem, dict):   # instancia NUEVA (pista v2: un cerebro por cuerpo): recibe del padre
            if 'Q' in mem and self.PK['modelo']: self._aw = np.array(mem['Q'], float)
            if 'sentido' in mem: self._adS = dict((k, list(v)) for k, v in mem['sentido'].items())
            if 'Wc' in mem and self.PK['lenta']: self._fkWc = np.array(mem['Wc'], float)
            self._fk_st['recibidos'] += 1
        # en la pista v1 el objeto ES el cerebro del linaje (como el nodo de FABRICA): Q, lo sentido y Wc siguen donde estaban

    def _fk_nodo(self, info):
        _mem = info.get('memoria')
        if self.PK['herencia'] and isinstance(_mem, dict) and 'tabla' in _mem:   # subida_n10b 'res' (verbatim): NODO_LEE copias
            _tb = [[list(_p7), float(_r7), int(_n7)] for _p7, _r7, _n7 in _mem['tabla']]
            self._nodo = [[list(_e7[0]), _e7[1], _e7[2]] for _e7 in _tb] * max(1, self.NODO_LEE)

    def _fk_salida(self):
        st = dict(self._fk_st) if self._FK else {}
        out = dict(perillas=dict(self.PK), des_splits=self._fk_des, **st)
        if self._FK:
            out['sentido'] = dict((k, [round(z[0] / z[2], 3), round(z[1] / z[2], 3), int(z[2])]) for k, z in sorted(self._adS.items()))
            out['Wc'] = [[round(float(v), 3) for v in f] for f in self._fkWc]
            if self.PK['modelo']: out['apr'] = self._apr_salida()
        return out

# <<APR_METODOS>>
