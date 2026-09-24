"""carros_apr_reserva.py — EXPLORATORIO, no es dato (nube, 24-sep-2026). La regla de la reserva (carros_extra.aplica) sobre APR
(FABRICA + opción aprendida de morder lo malo conocido, aprende_barrer). APR.py no se toca: subclase; con todo en None == APR."""
import types
import carros_reserva as CR
import carros_extra as CX

_APR = CR.P.carga_carro('APR')


class CarroAPRRes(_APR.Carro):
    def __init__(self, ctx, cfg):
        super().__init__(ctx)
        self.cfg = dict(cfg)

    def actua(self, obs):
        return CX.aplica(self, obs, super().actua(obs))


def modulo(nombre, **cfg):
    m = types.ModuleType('carro_' + nombre)
    m.crea = lambda ctx, _c=dict(cfg): CarroAPRRes(ctx, _c)
    return m


BRAZOS = {
    'WA': (lambda: modulo('WA'), 'APR por la subclase sin reglas (== APR)'),
    'APR_RES': (lambda: modulo('APR_RES', neo=0.5, vmal=1.45, lim=1.45), 'APR + regla completa de la reserva'),
    'APR_MAL': (lambda: modulo('APR_MAL', vmal=1.45), 'APR + no muerde lo malo bajo 1.45'),
}
