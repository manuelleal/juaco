# EXPLORATORIO, no es dato
# GENERADO por experimentos/organelos/boca_buena/construye_bb.py desde comite2/puenteo/carros/HIB.py (sha 8dbae3522c01517b). NO editar a mano.
# Unica diferencia de conducta: la perilla BB (ablaciones de la boca_buena). BB = 'ref' == HIB del puenteo en la fisica.
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
BB = 'ref'      # boca_buena (diagnostico 28-sep): el runner la fija ANTES de pista.run. Ver BB_MODOS.
BB_MODOS = ('ref', 'veto', 'fuerza', 'sinprueba', 'soloprueba', 'm0', 'vetom0', 'glotu', 'todo', 'vetoc', 'fuerzac', 'm10', 'm40', 'ventana', 'tinv', 'tinv40')
MEM_REPS = 5    # memoria: repeticiones de cada leccion (letra, necesidad) por la via lenta (el nodo lee hasta 50 entradas)


class Carro:
    def __init__(self, ctx):
        self.P = {k: int(v) for k, v in PUENTES.items()}
        self.v = V.Carro(ctx); self.o = O.Carro(ctx)
        self.L = int(ctx['L'])
        self.st = dict(pasos=0, mov_dif=0, mov_puenteado=0, boca_dec=0, boca_dif=0, boca_puenteada=0, boca_mala_dec=0, boca_mala_dif=0,
                       boca_buena_dec=0, boca_buena_dif=0, mem_lecciones=0, mem_nacidos=0, cuerpos=1)
        if BB not in BB_MODOS: raise SystemExit(f"HIBB: BB invalido {BB!r}")
        self.BB = BB; self.U = float(ctx['rep_umbral'])
        self.X = float(ctx['rep_X']); self.C = (float(ctx['costo']), float(ctx['costo_a']))   # ventana: cantidades del mundo que el carro ya recibe
        self.bbt = dict(desc_dec=0, desc_veto=0, desc_fuerza=0, bue_dec=0, bue_veto=0, bue_fuerza=0,
                        bue_veto_rel=0, bue_veto_norel=0, bue_fuerza_bajoU=0, bue_fuerza_margen=0, bue_fuerza_filtro=0,
                        bue_fuerza_nosirve_act=0, cambia=0, mord_final_bue=0)

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
            if (not malo) and P['boca_buena']: self._bb_tel(k, od['lev'], mo, mordio)   # boca_buena: telemetria (solo lectura)
            if (malo and P['boca_mala']) or ((not malo) and P['boca_buena']):
                if not malo: mo = self._bb(k, od['lev'], mo, mordio)   # boca_buena: ablacion (BB = 'ref' -> mo tal cual)
                st['boca_puenteada'] += int(mo != mordio); mordio = mo
                if not malo: self.bbt['mord_final_bue'] += int(mordio)
            self.v.actua_cierra(obs, pos, k, mordio)
        return dict(mov=mov, muerde=mordio, escribe=None)

    # ---------------------------------------------------------------- boca_buena: ablaciones (diagnostico 28-sep)
    def _sirve(self, v, lev, umbral):
        """True si la letra de valor v (O1 la cree NO mala) sube alguna necesidad j con lev[j] < umbral."""
        return any(v[j] > 0 and lev[j] < umbral for j in (0, 1))

    def _bb(self, k, lev, mo, mv):
        """Mordida final sobre letra NO mala para O1. mo = O1 (MARGEN + PRUEBA), mv = V143 (boca + FILTRO + APR)."""
        B = self.BB; con = k in self.o.n
        if B == 'ref': return mo
        if B == 'veto': return bool(mo and mv)                  # O1 solo puede decir NO
        if B == 'fuerza': return bool(mo or mv)                 # O1 solo puede decir SI
        if B == 'sinprueba': return mo if con else mv           # sin neofobia: lo desconocido lo decide V143
        if B == 'soloprueba': return mv if con else mo          # solo neofobia: lo conocido lo decide V143
        if B == 'vetoc': return bool(mo and mv) if con else mv  # O1 solo dice NO, y solo sobre lo conocido (sin neofobia)
        if B == 'fuerzac': return bool(mo or mv) if con else mv # O1 solo dice SI, y solo sobre lo conocido (sin neofobia)
        if B in ('m10', 'm40', 'ventana', 'tinv', 'tinv40') and not con: return mv   # barrido del margen: lo desconocido lo decide V143
        if B == 'm10': return self._sirve(self.o._val(k), lev, self.U + 0.10)   # barrido: margen 0.10 sobre rep_umbral
        if B == 'm40': return self._sirve(self.o._val(k), lev, self.U + 0.40)   # barrido: margen 0.40 sobre rep_umbral
        if B == 'ventana':   # muerde si alguna necesidad que sube NO alcanza a cubrir lo que falta de la ventana de parto
            v = self.o._val(k); falta = max(self.X - self.v._avent, 0.0)
            return any(v[j] > 0 and (lev[j] - self.U) < falta * self.C[j] for j in (0, 1))
        if B == 'tinv':      # CONTROL desfasado del termostato (margen 0.25): lee el nivel de la necesidad que la letra NO sube
            v = self.o._val(k)
            return any(v[j] > 0 and lev[1 - j] < self.U + 0.25 for j in (0, 1))
        if B == 'tinv40':    # CONTROL desfasado del termostato U + g/2 (= m40 en esta pista): lee la necesidad que la letra NO sube
            v = self.o._val(k)
            return any(v[j] > 0 and lev[1 - j] < self.U + v[j] / 2 for j in (0, 1))
        v = self.o._val(k) if con else None
        if B == 'm0': return (self._sirve(v, lev, self.U) if con else mo)            # MARGEN 0: umbral = rep_umbral
        if B == 'todo': return (any(v[j] > 0 for j in (0, 1)) if con else mo)       # sin umbral: todo lo bueno conocido (PRUEBA igual)
        if B == 'vetom0': return bool(mv and (self._sirve(v, lev, self.U) if con else True))   # solo veto, umbral rep_umbral, sin neofobia
        if B == 'glotu':   # GLOTU (muro) en el marco del hibrido: veta lo que solo sube la necesidad MAS llena ya en rep_umbral
            if not con: return mv
            js = [j for j in (0, 1) if v[j] > 0]
            if len(js) == 1 and not (v[1 - js[0]] > 0):
                j = js[0]
                if lev[j] >= self.U and lev[j] > lev[1 - j]: return False
            return mv
        raise SystemExit(f'HIBB: BB {B!r}')

    def _bb_tel(self, k, lev, mo, mv):
        """SOLO LECTURA: direccion de la discrepancia O1 (mo) vs V143 (mv) sobre letras no malas, con la decision CRUDA de O1."""
        t = self.bbt; con = k in self.o.n
        if not con:
            t['desc_dec'] += 1; t['desc_veto'] += int(mv and not mo); t['desc_fuerza'] += int(mo and not mv); return
        v = self.o._val(k); t['bue_dec'] += 1
        if mv and not mo:
            t['bue_veto'] += 1
            js = [j for j in (0, 1) if v[j] > 0]
            rel = len(js) == 1 and lev[js[0]] > lev[1 - js[0]]
            t['bue_veto_rel' if rel else 'bue_veto_norel'] += 1
        if mo and not mv:
            t['bue_fuerza'] += 1
            t['bue_fuerza_bajoU' if self._sirve(v, lev, self.U) else 'bue_fuerza_margen'] += 1
            t['bue_fuerza_filtro'] += int(k in self.v._v3o)
            t['bue_fuerza_nosirve_act'] += int(not (v[self.v._na] > 0))

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
        return dict(puentes=dict(self.P), mem_reps=MEM_REPS, hib=dict(self.st), v143=self.v.salida(), o1=self.o.salida(),
                    bb=self.BB, bbt=dict(self.bbt))


def crea(ctx):
    return Carro(ctx)
