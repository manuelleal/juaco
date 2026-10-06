# -*- coding: utf-8 -*-
"""SOCIEDAD de colonias (idea c): 3 sistemas completos leen el mismo mundo; la colonia 0 vive a DIETA (solo fuentes malas),
las 1 y 2 en el regimen honesto; cada colonia lee a las otras dos como una fuente mas ('colonia').
  mutua:    lo que dice otra colonia es UNA voz mas en cuarentena (peso 1).
  ciega:    lo que dice otra colonia se cree casi directo (peso 2.5 >= umbral de validacion).
  sola:     cada colonia sin leer a las otras.
Pregunta: ¿se propaga la mentira del cartel de la colonia 0 a las sanas? ¿mejora la enferma al leer a las sanas?
Uso: python sociedad.py --semillas 10 --out datos/sociedad.json"""
import argparse, json, time, sys
import numpy as np
from hambre import Mundo, Fuente, Sistema, arma_fuentes, mide

class FuenteColonia(Fuente):
    def __init__(self, i, otra, mundo, rng):
        super().__init__(i, 'colonia', 'texto', np.arange(mundo.NF), 1.0, mundo, rng)
        self.otra = otra; self.t_act = -1
    def dice(self, f, t):
        v = self.otra.respuesta(f, t)
        return int(v), 0

def corre(seed, modo, T=600, K=3, log=print):
    rng = np.random.default_rng(seed)
    mundo = Mundo(rng, T=T)
    fuentes = [arma_fuentes(mundo, np.random.default_rng(seed + 1000 + j), 'dieta' if j == 0 else 'honesto') for j in range(3)]
    sis = []
    for j in range(3):
        sis.append(Sistema(mundo, fuentes[j], np.random.default_rng(seed + 2000 + j), memoria='cuarentena', eleccion='apetito', K=K))
    if modo != 'sola':
        for j in range(3):
            for o in range(3):
                if o == j: continue
                fc = FuenteColonia(len(fuentes[j]), sis[o], mundo, np.random.default_rng(seed + 3000 + 10 * j + o))
                fc.peso = 2.5 if modo == 'ciega' else 1.0
                fuentes[j].append(fc)
            # el sistema ya copio la lista: reconstruimos sus estructuras por fuente
            S = len(fuentes[j]); s = sis[j]
            s.fs = fuentes[j]; s.S = S
            s.rep = np.full(S, 0.8); s.apetito = np.full(S, 0.5); s.pend = [[] for _ in range(S)]
            s.log = -np.ones((S, mundo.NF), int); s.log_t = -np.ones((S, mundo.NF), int); s.log_r = -np.ones((S, mundo.NF), int)
            from hambre import UF; s.uf = UF(S); s.consumo = np.zeros(S, int); s.t_rep_baja = -np.ones(S, int)
            s.cob_mask = np.zeros((S, mundo.NF), bool)
            for f in fuentes[j]: s.cob_mask[f.i, f.cob] = True
    curvas = [[] for _ in range(3)]
    for t in range(T):
        mundo.paso(t)
        for j in range(3): sis[j].paso(t)
        if t % 10 == 9 or t in mundo.cambios or t + 1 in mundo.cambios:
            for j in range(3): curvas[j].append((t, sis[j].respuestas(t)))
    out = {}
    for j in range(3):
        m = mide(sis[j], mundo, fuentes[j], curvas[j], T - 1)
        m['curva'] = [(tc, float((rr == mundo.verdad).mean())) for (tc, rr) in curvas[j]]
        m['acierto_medio'] = float(np.mean([a for (_, a) in m['curva']]))
        # ¿cuanto le leyo a las otras colonias y con que apetito acabo?
        m['lee_colonias'] = float(sum(1 for (tt, s) in sis[j].consumo_rec if fuentes[j][s].tipo == 'colonia') / max(1, len(sis[j].consumo_rec)))
        out[f'col{j}'] = m
        log(f"  s{seed} {modo:6s} col{j} ({'dieta' if j == 0 else 'honesto'}) acierto {m['acierto']:.2f} err {m['errores']:.2f} abst {m['abstiene']:.2f} "
            f"mentiras {m['mentiras']:2d} lee_colonias {m['lee_colonias']:.2f} apetito_colonia {m['apetito'].get('colonia')} rep_colonia {m['reputacion'].get('colonia')}")
    return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--semillas', type=int, default=10); ap.add_argument('--out', default=None)
    a = ap.parse_args(); t0 = time.time(); lineas = []
    def log(s): print(s); lineas.append(s); sys.stdout.flush()
    todo = {}
    for seed in range(a.semillas):
        todo[seed] = {modo: corre(seed, modo, log=log) for modo in ('sola', 'mutua', 'ciega')}
    log(f"CPU {time.time() - t0:.0f} s")
    if a.out:
        json.dump({str(k): v for k, v in todo.items()}, open(a.out, 'w', encoding='utf-8'))
        open(a.out.replace('.json', '.txt'), 'w', encoding='utf-8').write('\n'.join(lineas))
