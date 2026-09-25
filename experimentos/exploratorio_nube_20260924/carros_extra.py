"""carros_extra.py — EXPLORATORIO, no es dato (nube, 24-sep-2026). Tema (i), segunda vuelta.

Hallazgo al leer la boca de FABRICA (no medido aún como tal): con la vía rápida CERRADA (la puerta pide 5 mordidas del mismo
código), el valor sale de la vía lenta; tras UNA mordida de B vale ~ -1.35 y con hambre 1 la boca muerde igual:
Vb = 1.2*(-1.35) + 2*1 + 0.5 = 0.88 -> p = sigmoide(0.88/0.3) ~ 0.95. El hambre empuja a morder lo que ya sabe malo (H-BOCA).
Por eso la regla de la reserva se extiende a lo MALO CONOCIDO:
  neo : no prueba lo DESCONOCIDO si r = min(E, Ag) < neo                    (como carros_reserva)
  vmal: no muerde lo MALO conocido si r < vmal (el golpe no se aguanta)      (NUEVA)
  lim : muerde lo MALO conocido (limpia) si r >= lim                         (como carros_reserva)
Todo con la subclase de FABRICA (mismo consumo de rng; con todo en None == FABRICA, lo comprueba --identidad vía W0).
"""
import types
import carros_reserva as CR

TOT = CR.TOT


def aplica(self, obs, out):
    """La regla de la reserva sobre la decisión ya tomada por la boca del carro base (FABRICA o APR). Sin rng."""
    if self._enc is None:
        return out
    pos, kk, kc, _Wb, _wf, _ws = self._enc
    r = min(float(obs['E']), float(obs['Ag']))
    Pk = self.PAT[kk]
    v = [self._vnec(n, Pk, kc) for n in range(self.N_NEC)]
    fam = any(self._fam(kc, n) for n in range(self.N_NEC))
    desc = (not fam) and max(abs(x) for x in v) < CR.U0
    malo = min(v) <= -CR.U1
    TOT['enc'] += 1; TOT['desc'] += int(desc); TOT['malo'] += int(malo)
    neo, vmal, lim = self.cfg.get('neo'), self.cfg.get('vmal'), self.cfg.get('lim')
    veto = False; fuerza = False
    if out['muerde']:
        if neo is not None and desc and r < neo: veto = True; TOT['vetos_desc'] += 1
        elif vmal is not None and malo and r < vmal: veto = True; TOT['vetos_malo'] += 1
    elif lim is not None and malo and r >= lim:
        fuerza = True; TOT['limpias'] += 1
    if veto:
        out = dict(out, muerde=False)
        if self.MEMORIA_RECHAZO:
            self._rech[pos] = obs['t'] + self.MEMORIA_RECHAZO
    elif fuerza:
        out = dict(out, muerde=True); self._rech.pop(pos, None)
    if out['muerde']:
        TOT['mord'] += 1; TOT['mord_desc'] += int(desc); TOT['mord_malo'] += int(malo)
    return out


class CarroRes2(CR._FAB.Carro):
    def __init__(self, ctx, cfg):
        super().__init__(ctx)
        self.cfg = dict(cfg)

    def actua(self, obs):
        return aplica(self, obs, super().actua(obs))


def modulo(nombre, **cfg):
    m = types.ModuleType('carro_' + nombre)
    m.crea = lambda ctx, _c=dict(cfg): CarroRes2(ctx, _c)
    return m


BRAZOS = {
    'W2': (lambda: modulo('W2'), 'CarroRes2 sin reglas (== FABRICA)'),
    'MAL14': (lambda: modulo('MAL14', vmal=1.4), 'no muerde lo malo conocido si min(E,Ag) < 1.4'),
    'MALINF': (lambda: modulo('MALINF', vmal=9.9), 'no muerde NUNCA lo malo conocido (control: sin reserva, sin limpieza)'),
    'NEO5_MAL14': (lambda: modulo('NEO5_MAL14', neo=0.5, vmal=1.4), 'neofobia 0.5 + no muerde lo malo bajo 1.4'),
    'RES': (lambda: modulo('RES', neo=0.5, vmal=1.45, lim=1.45), 'REGLA COMPLETA: prueba si r>=0.5, lo malo sólo para limpiar con r>=1.45'),
    'RES14': (lambda: modulo('RES14', neo=0.5, vmal=1.4, lim=1.4), 'regla completa con limpieza desde 1.4 (rompe la ventana de parto)'),
    'RES_LIM10': (lambda: modulo('RES_LIM10', neo=0.5, vmal=1.0, lim=1.0), 'regla completa con umbral de limpieza 1.0'),
}
