"""carros_v143_familia.py — EXPLORATORIO, no es dato (nube, 24-sep-2026). Lo que n10c validó, puesto sobre el candidato v14.3.

subida_n10c (nube, FUNCIONA ×2, sin auditar por el PC) midió en la pista v2 que la familia que pasa su tabla EN EL PARTO sin las
entradas neutras (R = 0: H-NEUTRAS) da R0 de los nacidos >= 0.90. V143 ya tiene un canal de linaje: el NODO de FABRICA (se llena con
las últimas 20 mordidas de cada cuerpo al MORIR y el que nace lo lee por la vía lenta). Aquí, sin tocar V143.py (cargado por ruta):
  N0   : el nodo del linaje SIN neutras (se filtran las R == 0 antes de cada lectura al nacer). Cero memoria nueva.
  RES  : en el parto el padre VIVO pasa su tabla (por (patrón, necesidad) la R más reciente vivida; si no la vivió, la del nodo), y el
         hijo la lee como su nodo (NODO_LEE copias), como FAMB_RES de subida_n10b. Con neutras.
  RES0 : RES sin las entradas neutras (el brazo RES_SIN0 de n10c).
  BAR0 : control de CONTENIDO: RES0 con las R permutadas entre las entradas (rng propio [860001, t, k]; no toca ningún rng del mundo).
al_parir llama primero al de V143 (la opción TD de APR siente el parto). Con todo apagado == V143 bit a bit (brazo WF143 del arnés).
"""
import os, types
import numpy as np
import carros_v143_reserva as CVR

V = CVR.V
TOT = CVR.TOT


class CarroV143Fam(V.Carro):
    def __init__(self, ctx, cfg):
        super().__init__(ctx)
        self.cfg = dict(cfg)

    def _tabla(self):
        tab = {}
        for p7, r7, n7 in self._nodo: tab[(tuple(float(z) for z in p7), int(n7))] = float(r7)
        for _t9, k9, n9, R9 in self._mordh: tab[(tuple(float(z) for z in self.PAT[k9]), int(n9))] = float(R9)
        o7 = {tuple(float(z) for z in self.PAT[q]): i for i, q in enumerate('ABCD')}
        return [[list(c[0]), tab[c], c[1]] for c in sorted(tab, key=lambda c: (c[1], o7.get(c[0], 99), c[0]))]

    def al_parir(self, info):
        base = super().al_parir(info)
        if not self.cfg.get('res'):
            return base
        msg = self._tabla()
        TOT['partos'] += 1; TOT['entradas'] += len(msg); TOT['neutras'] += sum(1 for e in msg if e[1] == 0.0)
        if self.cfg.get('sin0'):
            msg = [e for e in msg if e[1] != 0.0]
        if self.cfg.get('bar') and len(msg) > 1:
            rb = np.random.default_rng([860001, int(info.get('t', 0)), int(info.get('k', 0))])
            pn = rb.permutation(len(msg))
            msg = [[list(msg[i][0]), float(msg[int(pn[i])][1]), int(msg[i][2])] for i in range(len(msg))]
        return msg

    def nace(self, info):
        mem = info.get('memoria')
        if self.cfg.get('res') and mem is not None:
            self._nodo = [[list(e[0]), float(e[1]), int(e[2])] for e in mem] * max(1, self.NODO_LEE)
            TOT['nace_con_tabla'] += 1
        elif self.cfg.get('nodo_sin0'):
            antes = len(self._nodo)
            self._nodo = [e for e in self._nodo if e[1] != 0.0]
            TOT['nodo_neutras_quitadas'] += antes - len(self._nodo)
        return super().nace(info)


def modulo(nombre, **cfg):
    mm = types.ModuleType('carro_' + nombre)
    mm.crea = lambda ctx, _c=dict(cfg): CarroV143Fam(ctx, _c)
    return mm


BRAZOS = {
    'WF143': (lambda: modulo('WF143'), 'subclase familia sin reglas (== V143)'),
    'V143_N0': (lambda: modulo('V143_N0', nodo_sin0=True), 'V143 con el nodo del linaje sin neutras (H-NEUTRAS; cero memoria nueva)'),
    'V143_RES': (lambda: modulo('V143_RES', res=True), 'V143 + la tabla del padre vivo en el parto (FAMB_RES de n10b), con neutras'),
    'V143_RES0': (lambda: modulo('V143_RES0', res=True, sin0=True), 'V143 + la tabla del padre sin neutras (RES_SIN0 de n10c)'),
    'V143_BAR0': (lambda: modulo('V143_BAR0', res=True, sin0=True, bar=True), 'control de contenido: RES0 con las R permutadas'),
}
