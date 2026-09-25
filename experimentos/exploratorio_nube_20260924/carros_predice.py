"""carros_predice.py — EXPLORATORIO, no es dato (nube, 24-sep-2026). Tema (ii): "aprender prediciendo".

Un órgano LOCAL que en CADA PASO predice lo que verá y aprende del error, sin morder:
  para cada objeto que el cuerpo ve (FABRICA ya mira el mundo entero: _see recorre obs['objs']), predice si seguirá ahí en
  el paso siguiente. Error = (desapareció sin que yo lo mordiera) - predicción; regla delta por patrón (EMA, eta_h).
  La tasa de desaparición por patrón, relativa a la media de todos, es rho_k = H[k] / Hbar.
Por qué podría servir para vivir con comida limitada: en la pista, lo que los otros comen desaparece y lo que evitan se
queda (olvido aparte, que es igual para todas las letras). Predecir el mundo da una pista del valor SIN MORDER.
Uso en la boca (sobre la regla de la reserva, CarroRes2):
  lo DESCONOCIDO con reserva baja (r < neo), que la regla vetaría, se prueba si rho_k >= RHO_HI (los otros lo comen);
  lo DESCONOCIDO con reserva alta, que se probaría, se veta si rho_k <= RHO_LO (los otros lo dejan).
Memoria nueva: 2 números por patrón visto + 1 media, por CUERPO (se borra al nacer: aprende en vida, no hereda).
Control de contenido PRED_BAR: la misma cuenta, pero leída con las letras permutadas (A<-B, B<-C, C<-D, D<-A).
"""
import types
import carros_reserva as CR
import carros_extra as CX

TOT = CR.TOT
ETA_H = 0.01
RHO_HI = 1.25
RHO_LO = 0.80
PERM = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'A'}


class CarroPred(CX.CarroRes2):
    def __init__(self, ctx, cfg):
        super().__init__(ctx, cfg)
        self._H = {}; self._Hbar = None; self._prev = None; self._yo_mordi = None

    def _observa(self, objs):
        """Aprende del error de predicción de TODOS los objetos del paso anterior."""
        if self._prev is not None:
            for x, k in self._prev.items():
                if x == self._yo_mordi:
                    continue
                y = 1.0 if objs.get(x) != k else 0.0
                h = self._H.get(k, 0.0 if self._Hbar is None else self._Hbar)
                self._H[k] = h + ETA_H * (y - h)
                self._Hbar = y if self._Hbar is None else self._Hbar + 0.2 * ETA_H * (y - self._Hbar)
                TOT['obs'] += 1; TOT['desap'] += int(y)
        self._prev = dict(objs); self._yo_mordi = None

    def _rho(self, k):
        if self.cfg.get('bar'):
            k = PERM[k]
        if self._Hbar is None or self._Hbar <= 0 or k not in self._H:
            return None
        return self._H[k] / self._Hbar

    def actua(self, obs):
        self._observa(obs['objs'])
        out = CR._FAB.Carro.actua(self, obs)     # la decisión de FABRICA (mismo consumo del rng)
        if self._enc is None:
            return out
        pos, kk, kc, _Wb, _wf, _ws = self._enc
        r = min(float(obs['E']), float(obs['Ag']))
        Pk = self.PAT[kk]
        v = [self._vnec(n, Pk, kc) for n in range(self.N_NEC)]
        fam = any(self._fam(kc, n) for n in range(self.N_NEC))
        desc = (not fam) and max(abs(x) for x in v) < CR.U0
        malo = min(v) <= -CR.U1
        rho = self._rho(kk) if self.cfg.get('pred') else None
        neo, vmal, lim = self.cfg.get('neo'), self.cfg.get('vmal'), self.cfg.get('lim')
        TOT['enc'] += 1; TOT['desc'] += int(desc); TOT['malo'] += int(malo)
        veto = False; fuerza = False
        if out['muerde']:
            if neo is not None and desc and r < neo:
                if rho is not None and rho >= RHO_HI: TOT['pred_permite'] += 1     # los otros lo comen: deja la mordida
                else: veto = True; TOT['vetos_desc'] += 1
            elif neo is not None and desc and rho is not None and rho <= RHO_LO:
                veto = True; TOT['pred_veta'] += 1                                   # los otros lo dejan: no lo prueba
            elif vmal is not None and malo and r < vmal:
                veto = True; TOT['vetos_malo'] += 1
        elif lim is not None and malo and r >= lim:
            fuerza = True; TOT['limpias'] += 1
        if veto:
            out = dict(out, muerde=False)
            if self.MEMORIA_RECHAZO:
                self._rech[pos] = obs['t'] + self.MEMORIA_RECHAZO
        elif fuerza:
            out = dict(out, muerde=True); self._rech.pop(pos, None)
        if out['muerde']:
            self._yo_mordi = pos
            TOT['mord'] += 1; TOT['mord_desc'] += int(desc); TOT['mord_malo'] += int(malo)
        return out

    def nace(self, info):
        super().nace(info)
        self._H = {}; self._Hbar = None; self._prev = None; self._yo_mordi = None


def modulo(nombre, **cfg):
    m = types.ModuleType('carro_' + nombre)
    m.crea = lambda ctx, _c=dict(cfg): CarroPred(ctx, _c)
    return m


BRAZOS = {
    'WP': (lambda: modulo('WP'), 'CarroPred sin reglas ni lectura (== FABRICA; el órgano observa pero no actúa)'),
    'RESP': (lambda: modulo('RESP', neo=0.5, vmal=1.45, lim=1.45), 'RES por CarroPred con el órgano observando pero sin leerlo (== RES)'),
    'PRED': (lambda: modulo('PRED', neo=0.5, vmal=1.45, lim=1.45, pred=True), 'RES + predicción de lo que desaparece (prueba lo que los otros comen)'),
    'PRED_BAR': (lambda: modulo('PRED_BAR', neo=0.5, vmal=1.45, lim=1.45, pred=True, bar=True), 'PRED con las letras permutadas (control de contenido)'),
}
