"""carros_limpia.py — EXPLORATORIO, no es dato (nube, 24-sep-2026). Tema (i), tercera vuelta: LIMPIEZA COSTEABLE.

Lo que enseñó i2: si el bicho deja de morder lo malo (MAL), el mundo se tapa de malo (hasta 18 % de pasos sin nada bueno en
todo el mundo) y muere de hambre a los 200 pasos; si lo muerde todo (FABRICA), el mundo queda limpio pero él muere joven.
Morder lo malo LIMPIA (la pista repone al instante una letra al azar): es un bien público. O1 lo resuelve limpiando SÓLO
cuando no queda nada útil y el golpe es costeable. Aquí la misma lógica con el VALOR APRENDIDO del bicho, no con la tabla de O1:
  limpieza costeable (fuerza la mordida de algo MALO conocido) si
    (a) en todo el mundo no hay ningún objeto de letra que el cuerpo marque BUENA (max_n valor_n >= U1), y
    (b) el golpe lo aguanta: para cada necesidad j que la letra daña, nivel_j - golpe_j >= piso (piso = 1.0 si la ventana de
        parto corre, E y Ag >= 1.0; si no, 0.2), y el golpe cae en la necesidad MÁS llena.
  golpe_j = el mayor |dS_j| negativo que ESTE cuerpo ha sentido (res['dS'] llega al carro en resultado()); sin golpe sentido,
  no limpia (un recién nacido no sabe cuánto duele).
  en cualquier otro caso, lo malo conocido NO se muerde (MAL) y lo desconocido se prueba sólo si r >= neo (NEO).
Memoria nueva: 2 números por cuerpo (el golpe sentido por necesidad). Con todo apagado == FABRICA (arnés WL).
"""
import types
import numpy as np
import carros_reserva as CR
import carros_ver as CV

TOT = CR.TOT
PISO = 0.2


class CarroLimpia(CV.CarroVer):
    def __init__(self, ctx, cfg):
        super().__init__(ctx, cfg)
        self._golpe = np.zeros(2)

    def resultado(self, res):
        if res.get('mordio') and res.get('dS') is not None:
            for j, x in enumerate(res['dS']):
                if x < 0: self._golpe[j] = max(self._golpe[j], -float(x))
        return super().resultado(res)

    def nace(self, info):
        super().nace(info)
        self._golpe[:] = 0.0

    def _valores_letras(self):
        vals = {}
        for k, Pk in self.PAT.items():
            kc = self._kenyon(Pk)
            vals[k] = [self._vnec(n, Pk, kc) for n in range(self.N_NEC)]
        return vals

    def actua(self, obs):
        if self.cfg.get('ver'):
            vals = self._valores_letras()
            self._malas = {k for k, v in vals.items() if min(v) <= -CR.U1}
        out = CR._FAB.Carro.actua(self, obs)       # la boca de FABRICA (con _see de VER si ver=True); mismo rng
        if self._enc is None:
            return out
        pos, kk, kc, _Wb, _wf, _ws = self._enc
        lev = (float(obs['E']), float(obs['Ag'])); r = min(lev)
        Pk = self.PAT[kk]
        v = [self._vnec(n, Pk, kc) for n in range(self.N_NEC)]
        fam = any(self._fam(kc, n) for n in range(self.N_NEC))
        desc = (not fam) and max(abs(x) for x in v) < CR.U0
        malo = min(v) <= -CR.U1
        neo, mal, limc = self.cfg.get('neo'), self.cfg.get('mal'), self.cfg.get('limc')
        TOT['enc'] += 1; TOT['desc'] += int(desc); TOT['malo'] += int(malo)
        costeable = False
        if malo and limc:
            vals = vals if self.cfg.get('ver') else self._valores_letras()
            buenas = {k for k, vv in vals.items() if max(vv) >= CR.U1}
            nada_util = not any(k2 in buenas for k2 in obs['objs'].values())
            piso = 1.0 if (lev[0] >= 1.0 and lev[1] >= 1.0) else PISO
            dania = [j for j in range(2) if v[j] <= -CR.U1]
            costeable = nada_util and bool(dania) and all(
                self._golpe[j] > 0 and lev[j] - self._golpe[j] >= piso and lev[j] >= lev[1 - j] for j in dania)
        veto = False; fuerza = False
        if out['muerde']:
            if neo is not None and desc and r < neo: veto = True; TOT['vetos_desc'] += 1
            elif mal and malo and not costeable: veto = True; TOT['vetos_malo'] += 1
        elif costeable:
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


def modulo(nombre, **cfg):
    m = types.ModuleType('carro_' + nombre)
    m.crea = lambda ctx, _c=dict(cfg): CarroLimpia(ctx, _c)
    return m


BRAZOS = {
    'WL': (lambda: modulo('WL'), 'CarroLimpia sin reglas (== FABRICA)'),
    'LIMC': (lambda: modulo('LIMC', limc=True), 'FABRICA + limpieza costeable (sin vetar lo malo fuera de ella)'),
    'MALC': (lambda: modulo('MALC', mal=True, limc=True), 'no muerde lo malo salvo limpieza costeable'),
    'RESC': (lambda: modulo('RESC', neo=0.5, mal=True, limc=True), 'REGLA DE LA RESERVA: prueba si r>=0.5; lo malo sólo como limpieza costeable'),
    'VER_RESC': (lambda: modulo('VER_RESC', ver=True, neo=0.5, mal=True, limc=True), 'RESC + el objetivo lo elige el valor'),
}
