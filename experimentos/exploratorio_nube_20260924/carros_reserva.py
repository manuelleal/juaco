"""carros_reserva.py — EXPLORATORIO, no es dato (nube, 24-sep-2026).

Tema (i) del director: "arriesgar según la reserva": probar lo desconocido y limpiar sólo cuando min(E, Ag) es alto.
Sobre el carro FABRICA de la carrera de escuderías (el bicho real en la pista del 22-sep). FABRICA.py NO se toca: esto es
una SUBCLASE que deja correr su actua() entero (mismo consumo del rng) y sólo corrige la decisión final de la boca.

Dos reglas locales, cero memoria nueva (sólo lee lo que el cuerpo ya tiene: sus valores por necesidad y su E, Ag):
  NEO (neofobia regulada por la reserva): si el código del objeto es DESCONOCIDO (ninguna necesidad lo tiene familiar y
      ninguna le da |valor| >= U0) y la reserva r = min(E, Ag) < neo, la boca no muerde (y lo recuerda como rechazado,
      igual que FABRICA cuando rechaza).
  LIM (limpieza regulada por la reserva): si alguna necesidad marca el objeto como MALO (valor <= -U1) y r >= lim,
      la boca muerde (limpia: morder repone una letra al azar en la pista; ERR-104). lim = 1.4 porque el golpe nominal
      es 0.4 (visible para el carro en res['dS']) y así no rompe la ventana de parto (E, Ag >= 1.0).
Con neo = lim = None el carro es FABRICA bit a bit (lo comprueba corre_explora.py --identidad).
"""
import os, sys, types
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'carrera_escuderias'))
import pista as P

_FAB = P.carga_carro('FABRICA')
U0 = 0.3     # desconocido: max_n |valor_n| < U0 y código no familiar en ninguna necesidad
U1 = 0.5     # malo: min_n valor_n <= -U1
TOT = defaultdict(int)   # acumulador del PROCESO (el corredor lo pone a cero en cada corrida; con fundador limpio hay
                         # varias instancias por linaje y salida() sólo ve la última)


class CarroRes(_FAB.Carro):
    def __init__(self, ctx, cfg):
        super().__init__(ctx)
        self.cfg = dict(cfg)

    def actua(self, obs):
        out = super().actua(obs)
        if self._enc is None:
            return out
        pos, kk, kc, _Wb, _wf, _ws = self._enc
        r = min(float(obs['E']), float(obs['Ag']))
        Pk = self.PAT[kk]
        v = [self._vnec(n, Pk, kc) for n in range(self.N_NEC)]
        fam = any(self._fam(kc, n) for n in range(self.N_NEC))
        desc = (not fam) and max(abs(x) for x in v) < U0
        malo = min(v) <= -U1
        TOT['enc'] += 1; TOT['desc'] += int(desc); TOT['malo'] += int(malo)
        TOT['desc_r_bajo'] += int(desc and r < 0.5)
        neo, lim = self.cfg.get('neo'), self.cfg.get('lim')
        if neo is not None and desc and r < neo and out['muerde']:
            out = dict(out, muerde=False); TOT['vetos'] += 1
            if self.MEMORIA_RECHAZO:
                self._rech[pos] = obs['t'] + self.MEMORIA_RECHAZO
        elif lim is not None and malo and r >= lim and not out['muerde']:
            out = dict(out, muerde=True); TOT['limpias'] += 1
            self._rech.pop(pos, None)
        if out['muerde']:
            TOT['mord'] += 1; TOT['mord_desc'] += int(desc); TOT['mord_malo'] += int(malo)
        return out


def modulo(nombre, **cfg):
    """Módulo-carro para pista.run: expone crea(ctx)."""
    m = types.ModuleType('carro_' + nombre)
    m.crea = lambda ctx, _c=dict(cfg): CarroRes(ctx, _c)
    return m
