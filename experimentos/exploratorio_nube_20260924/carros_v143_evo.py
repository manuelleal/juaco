"""carros_v143_evo.py — EXPLORATORIO, no es dato (nube, 24-sep-2026). El candidato v14.3 con las perillas que SELECCIONÓ ECO.

ECO v1.1 (serie 19401–19420, HAY ALGO MODESTO por la letra; réplica en curso) seleccionó, contra 8 sombras, alpha (+, 20/20) y aversion
(+, 15/20). Mediana del banco en el corte (log(g/G0), exponenciada), brazo CEREBRO (sólo mutan las 15 perillas del cerebro, como en la
carrera, donde la historia de vida la fija la pista): alpha ×1.61, aversion ×1.29, eta_s ×1.26 (tau_e ×0.85; el resto ≈ 1).
Pregunta: ¿el organismo con las perillas que eligió la selección en el mundo de flujo fijo (pista v2 × 10) vive mejor en la pista de la
carrera (pista v1, otro mundo)? Sin tocar V143.py: subclase que multiplica ALPHA, AVERSION y ETA_S tras el __init__ de V143 (ninguno se
usa en el __init__ ni consume rng). Con todos los factores en 1 == V143 bit a bit (brazo WE143 del arnés).
Control de dirección: ANTI (alpha ÷1.61). También sobre FABRICA (FAB_EVO3), para ver si la ganancia es del cerebro de fábrica o de v14.3.
"""
import types
import carros_v143_reserva as CVR
import carros_reserva as CR

V = CVR.V
F_ALPHA, F_AVERSION, F_ETA_S = 1.61, 1.29, 1.26


def _aplica(self, cfg):
    self.ALPHA = self.ALPHA * cfg.get('alpha', 1.0)
    self.AVERSION = self.AVERSION * cfg.get('aversion', 1.0)
    self.ETA_S = self.ETA_S * cfg.get('eta_s', 1.0)


class CarroV143Evo(V.Carro):
    def __init__(self, ctx, cfg):
        super().__init__(ctx)
        self.cfg = dict(cfg)
        _aplica(self, self.cfg)


class CarroFabEvo(CR._FAB.Carro):
    def __init__(self, ctx, cfg):
        super().__init__(ctx)
        self.cfg = dict(cfg)
        _aplica(self, self.cfg)


def modulo(nombre, clase=CarroV143Evo, **cfg):
    mm = types.ModuleType('carro_' + nombre)
    mm.crea = lambda ctx, _c=dict(cfg), _k=clase: _k(ctx, _c)
    return mm


EVO3 = dict(alpha=F_ALPHA, aversion=F_AVERSION, eta_s=F_ETA_S)
BRAZOS = {
    'WE143': (lambda: modulo('WE143'), 'subclase evo con factores 1 (== V143)'),
    'WEFAB': (lambda: modulo('WEFAB', clase=CarroFabEvo), 'subclase evo de FABRICA con factores 1 (== FABRICA)'),
    'V143_EVO3': (lambda: modulo('V143_EVO3', **EVO3), 'V143 con alpha x1.61, aversion x1.29, eta_s x1.26 (lo que eligió ECO)'),
    'V143_ALPHA': (lambda: modulo('V143_ALPHA', alpha=F_ALPHA), 'V143 con alpha x1.61 (el gen elegido 20/20)'),
    'V143_ANTI': (lambda: modulo('V143_ANTI', alpha=1 / F_ALPHA), 'control de dirección: V143 con alpha /1.61'),
    'FAB_EVO3': (lambda: modulo('FAB_EVO3', clase=CarroFabEvo, **EVO3), 'FABRICA con las tres perillas de ECO'),
}
