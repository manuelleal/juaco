"""carros_v143_reserva.py — EXPLORATORIO, no es dato (nube, 24-sep-2026). Tema (i) sobre el candidato v14.3 (frente 1).

El creador de v14.3 dejó escrita la pieza que cree que falta (experimentos/tronco_v14_3/INFORME_v143.md, "Qué queda"):
  "neofobia regulada por la reserva: la boca se contiene ante un código poco familiar (ncod bajo y valor lento ~ 0) cuando
   min(E, Ag) es bajo. Cero memoria nueva, un umbral."
Aquí se prueba SIN tocar V143.py (se carga por ruta, como corre_v143.py) con una subclase que sólo corrige la decisión ya tomada
por la boca de V143 (no consume rng; con neo = None es V143 bit a bit: brazo WV143 del arnés de corre_explora.py).

  NEO  (literal del creador, por CUERPO): no muerde si la letra es DESCONOCIDA para el cuerpo (ninguna fila la tiene familiar por
        la vía rápida y |valor| < U0 = 0.3 en las dos filas) y r = min(E, Ag) < neo.
  NEOL (por LINAJE): no muerde si la letra nunca fue sentida por el linaje (no está en _adS, la tabla de dS sentido de APR que
        el carro conserva entre cuerpos; un fundador limpio es instancia nueva y la tiene vacía) y r < neo.
En los dos, si la letra es MALA CONOCIDA para el linaje decide la opción TD de APR (_opcion): la regla no la pisa (su registro
semi-Markov quedaría incoherente). FILTRO de V143 actúa antes (si veta, aquí no hay nada que vetar).
"""
import importlib.util, os, types
import carros_reserva as CR

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
RUTA_V143 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143', 'V143.py')
_spec = importlib.util.spec_from_file_location('carro_V143_explora', RUTA_V143)
V = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(V)

U0 = 0.3
TOT = CR.TOT   # el mismo contador que corre_explora.corre() limpia y guarda


class CarroV143Res(V.Carro):
    def __init__(self, ctx, cfg):
        super().__init__(ctx)
        self.cfg = dict(cfg)

    def actua(self, obs):
        out = super().actua(obs)
        neo = self.cfg.get('neo')
        if neo is None or self._enc is None:
            return out
        pos, kk, kc, _Wb, _wf, _ws = self._enc
        TOT['enc'] += 1
        m = self._adS.get(kk)
        if m is not None and (m[0] < 0 or m[1] < 0):      # malo conocido del linaje: decide la opción TD (no se pisa)
            TOT['td'] += 1
            return out
        if self.cfg.get('linaje'):
            desc = m is None
        else:
            Pk = self.PAT[kk]
            v = [self._vnec(n, Pk, kc) for n in range(self.N_NEC)]
            fam = any(self._fam(kc, n) for n in range(self.N_NEC))
            desc = (not fam) and max(abs(x) for x in v) < U0
        TOT['desc'] += int(desc)
        r = min(float(obs['E']), float(obs['Ag']))
        if out['muerde'] and desc and r < neo:
            TOT['vetos_desc'] += 1
            out = dict(out, muerde=False)
            if self.MEMORIA_RECHAZO:
                self._rech[pos] = obs['t'] + self.MEMORIA_RECHAZO
        if out['muerde']:
            TOT['mord'] += 1; TOT['mord_desc'] += int(desc)
        return out


def modulo(nombre, **cfg):
    mm = types.ModuleType('carro_' + nombre)
    mm.crea = lambda ctx, _c=dict(cfg): CarroV143Res(ctx, _c)
    return mm


def _v143():
    mm = types.ModuleType('carro_V143')
    mm.crea = V.crea
    return mm


BRAZOS = {
    'V143': (_v143, 'V143 del PC sin tocar (cargado por ruta)'),
    'WV143': (lambda: modulo('WV143'), 'subclase sin reglas (== V143)'),
    'V143_NEO5': (lambda: modulo('V143_NEO5', neo=0.5), 'V143 + neofobia por cuerpo (literal del creador), r < 0.5'),
    'V143_NEOL5': (lambda: modulo('V143_NEOL5', neo=0.5, linaje=True), 'V143 + neofobia por linaje (letra nunca sentida), r < 0.5'),
    'V143_NEOINF': (lambda: modulo('V143_NEOINF', neo=9.9), 'V143 + neofobia por cuerpo SIEMPRE (control: sin reserva)'),
}
