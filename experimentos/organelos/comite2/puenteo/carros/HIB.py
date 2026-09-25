# EXPLORATORIO, no es dato
"""HIB.py — HIBRIDO DE PUENTEO DIAGNOSTICO (comite2/puenteo, explorador Fable 1, 25-sep-2026).

MISION: llegar a la AGI por este camino. Esto NO es un candidato: es un instrumento para saber DONDE esta la brecha 0.60 -> 0.94.

El carro aloja DOS cerebros que viven la misma vida (mismo obs, mismo resultado(), mismo muere/nace/al_parir):
  self.v = V143P  (el bicho real v14.3, con actua() partido en patas / boca / cierre)
  self.o = O1P    (la politica escrita por un LLM, con actua() partido en decide / boca)
V143 decide TODO, salvo las piezas puenteadas (PUENTES), que decide O1:
  patas       mov = el de O1 (ir al blanco de O1). El motor de V143 igual corre y consume su rng (su m/p aprenden como si
              se hubieran movido a su manera: solo se sustituye el mov ejecutado).
  boca_buena  muerde = lo que dice O1 cuando la letra bajo el cuerpo NO es mala para O1 (desconocida o con dS >= 0 en ambas filas):
              O1 muerde lo bueno solo si le sirve (MARGEN) y prueba lo desconocido solo con cuerpo (PRUEBA).
  boca_mala   muerde = lo que dice O1 cuando la letra ES mala para O1 (algun dS < 0 en su tabla): O1 solo la muerde para LIMPIAR
              (nada util a la vista, necesidad, golpe costeable en la fila mas llena).
  memoria     el nacido NO lee el nodo de V143 (ultimas 20 mordidas por la via lenta); en su lugar recibe la TABLA de linaje de O1
              (letra -> media del dS sentido) como lecciones por la MISMA via lenta (R = +1 / -3 / 0 por signo, MEM_REPS veces).
Con todo en 0: V143 bit a bit (fisica, _carrera y rng del mundo; arnes_puenteo.py). Con patas + boca_buena + boca_mala: O1 bit a bit
en la fisica (O1 no consume el rng del cuerpo: solo lo guarda; arnes_puenteo.py).
El cierre (actua_cierra) aplica sobre la decision FINAL: memoria de rechazo, telemetria del filtro y la accion que aprende la opcion
APR (si la boca fue puenteada, APR aprende sobre lo que el cuerpo HIZO, no sobre lo que habria hecho).
Ni eval ni exec; los dos cerebros se cargan por importlib desde esta carpeta. No escribe ni lee la pizarra.
"""
import importlib.util, os
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))


def _carga(n):
    spec = importlib.util.spec_from_file_location(f"puenteo_{n}", os.path.join(AQUI, n + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


V = _carga('V143P'); O = _carga('O1P')

PUENTES = dict(patas=0, boca_buena=0, boca_mala=0, memoria=0)   # el runner las fija en el modulo ANTES de pista.run (un proceso por corrida)
MEM_REPS = 5    # memoria: repeticiones de cada leccion (letra, necesidad) por la via lenta (el nodo lee hasta 50 entradas)


class Carro:
    def __init__(self, ctx):
        self.P = {k: int(v) for k, v in PUENTES.items()}
        self.v = V.Carro(ctx); self.o = O.Carro(ctx)
        self.L = int(ctx['L'])
        self.st = dict(pasos=0, mov_dif=0, mov_puenteado=0, boca_dec=0, boca_dif=0, boca_puenteada=0, boca_mala_dec=0, boca_mala_dif=0,
                       boca_buena_dec=0, boca_buena_dif=0, mem_lecciones=0, mem_nacidos=0, cuerpos=1)

    # ------------------------------------------------------------ INTERFAZ
    def actua(self, obs):
        P = self.P; objs = obs['objs']; st = self.st; st['pasos'] += 1
        mov_v = self.v.actua_patas(obs)
        od = self.o.decide(obs)
        st['mov_dif'] += int(mov_v != od['mov'])
        if P['patas']: mov = od['mov']; st['mov_puenteado'] += int(mov_v != od['mov'])
        else: mov = mov_v
        pos = (obs['pos'] + mov) % self.L
        mordio = self.v.actua_boca(obs, pos)
        if pos in objs:
            k = objs[pos]
            mo = self.o.boca(k, od['lev'], od['limpia'])
            val = self.o._val(k); malo = val is not None and bool((val < 0).any())
            st['boca_dec'] += 1; st['boca_dif'] += int(mo != mordio)
            if malo: st['boca_mala_dec'] += 1; st['boca_mala_dif'] += int(mo != mordio)
            else: st['boca_buena_dec'] += 1; st['boca_buena_dif'] += int(mo != mordio)
            if (malo and P['boca_mala']) or ((not malo) and P['boca_buena']):
                st['boca_puenteada'] += int(mo != mordio); mordio = mo
            self.v.actua_cierra(obs, pos, k, mordio)
        return dict(mov=mov, muerde=mordio, escribe=None)

    def resultado(self, res):
        self.v.resultado(res); self.o.resultado(res)

    def fin_paso(self, info):
        self.v.fin_paso(info); self.o.fin_paso(info)

    def muere(self, info):
        self.v.muere(info); self.o.muere(info)

    def al_parir(self, info):
        return dict(v=self.v.al_parir(info), o=self.o.al_parir(info))

    def nace(self, info):
        m = info.get('memoria'); self.st['cuerpos'] += 1
        iv = dict(info, memoria=(m['v'] if m else None)); io = dict(info, memoria=(m['o'] if m else None))
        if self.P['memoria']:
            nodo = self.v._nodo; self.v._nodo = []       # el nacido NO lee el nodo...
            try: self.v.nace(iv)
            finally: self.v._nodo = nodo                # (el nodo sigue existiendo; solo no se lee)
            self.o.nace(io)                             # la tabla de O1 llega primero al cerebro de O1...
            self._ensena()                              # ...y de ahi, como lecciones, a la via lenta de V143
        else:
            self.v.nace(iv); self.o.nace(io)

    def _ensena(self):
        """MEMORIA: la tabla de linaje de O1 (letra -> dS medio sentido) entra a la via lenta de V143 con la MISMA regla con que el
        nodo ensena al nacido (organismo_f9c, nodo_rel): R = +1 / -3 / 0 por el signo de cada fila, MEM_REPS veces por leccion."""
        v = self.v; PAT = v.PAT; LAM = v.LAM; ETA_S = v.ETA_S; AVERSION = v.AVERSION; CLIP_S = v.CLIP_S
        if not self.o.n: return
        self.st['mem_nacidos'] += 1
        for k in sorted(self.o.n):
            val = self.o._val(k); Pv = np.asarray(PAT[k], float)
            for n in (0, 1):
                R = 1.0 if val[n] > 0 else (-3.0 if val[n] < 0 else 0.0)
                for _ in range(MEM_REPS):
                    if LAM: mc = np.minimum(v.Wps[n], v.Wns[n]) * (Pv > 0); v.Wps[n] = v.Wps[n] - LAM * mc; v.Wns[n] = v.Wns[n] - LAM * mc
                    ds = R - float((v.Wps[n] - v.Wns[n]) @ Pv)
                    if ds > 0: v.Wps[n] = np.clip(v.Wps[n] + ETA_S * ds * Pv, 0, CLIP_S)
                    else:      v.Wns[n] = np.clip(v.Wns[n] + ETA_S * AVERSION * (-ds) * Pv, 0, CLIP_S)
                    self.st['mem_lecciones'] += 1

    def valor_nec(self, n, letra):
        """SOLO LECTURA (telemetria exp_hasta de la pista): la de V143, para que la fisica sin puentear sea V143 entera."""
        return self.v.valor_nec(n, letra)

    def salida(self):
        return dict(puentes=dict(self.P), mem_reps=MEM_REPS, hib=dict(self.st), v143=self.v.salida(), o1=self.o.salida())


def crea(ctx):
    return Carro(ctx)
