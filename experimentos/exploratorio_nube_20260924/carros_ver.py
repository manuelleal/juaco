"""carros_ver.py — EXPLORATORIO, no es dato (nube, 24-sep-2026). Tema (iii), elección propia.

Diagnóstico (tanda i1, semilla 24001, T 30000): el 72 % de los encuentros de FABRICA son con objetos que su propio valor ya
marca como MALOS (17 706 de 24 682). FABRICA elige su objetivo por DISTANCIA (_see: el más cercano no rechazado en los
últimos 20 pasos), así que gasta la vida yendo a lo malo, y con hambre termina mordiéndolo (H-BOCA).
Pieza local, cero memoria nueva: el objetivo lo elige el VALOR que el cuerpo ya tiene. _see salta los objetos cuya letra
el cuerpo marca mala (min_n valor_n <= -U1); si todo lo visible es malo o rechazado, vuelve a FABRICA (el más cercano).
Es lo que O1 hace escrito a mano ("rechazar sin alejarse no sirve: VA a lo bueno"), pero con el valor aprendido del bicho.
Se combina con la regla de la reserva (CarroRes2). Con ver=False es CarroRes2 exacto.
"""
import types
import carros_reserva as CR
import carros_extra as CX

TOT = CR.TOT


class CarroVer(CX.CarroRes2):
    def __init__(self, ctx, cfg):
        super().__init__(ctx, cfg)
        self._malas = None

    def _see(self, pos, objs, t, contar=False):
        if not self.cfg.get('ver') or self._malas is None:
            return super()._see(pos, objs, t, contar)
        L = self.L; best = None
        for x, k in objs.items():
            if k in self._malas: continue
            if self.MEMORIA_RECHAZO and self._rech.get(x, -1) > t: continue
            dl = (pos - x) % L; dr = (x - pos) % L; d = min(dl, dr)
            if best is None or d < best[0]: best = (d, k, dl < dr)
        if best is None:
            TOT['ver_sin_blanco'] += int(contar)
            return super()._see(pos, objs, t, contar)
        TOT['ver_blanco'] += int(contar)
        return best

    def actua(self, obs):
        if self.cfg.get('ver'):
            self._malas = set()
            for k, Pk in self.PAT.items():
                kc = self._kenyon(Pk)
                if min(self._vnec(n, Pk, kc) for n in range(self.N_NEC)) <= -CR.U1:
                    self._malas.add(k)
        return super().actua(obs)


def modulo(nombre, **cfg):
    m = types.ModuleType('carro_' + nombre)
    m.crea = lambda ctx, _c=dict(cfg): CarroVer(ctx, _c)
    return m


BRAZOS = {
    'WV': (lambda: modulo('WV'), 'CarroVer sin reglas (== FABRICA)'),
    'VER': (lambda: modulo('VER', ver=True), 'el objetivo lo elige el valor: salta lo que sabe malo'),
    'VER_RES': (lambda: modulo('VER_RES', ver=True, neo=0.5, vmal=1.45, lim=1.45), 'VER + regla completa de la reserva'),
    'VER_MAL': (lambda: modulo('VER_MAL', ver=True, vmal=1.45), 'VER + no muerde lo malo bajo 1.45 (sin neofobia ni limpieza)'),
}
