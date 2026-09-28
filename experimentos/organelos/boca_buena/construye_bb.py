# EXPLORATORIO, no es dato
"""construye_bb.py — construye por ANCLAS el instrumento del diagnostico boca_buena (creador, 28-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados).

Origen (solo se LEE, sha fijado): experimentos/organelos/comite2/puenteo/carros/{HIB,O1P,V143P}.py (commit e255a0e).
  - O1P.py y V143P.py se COPIAN tal cual (sha verificado antes y despues).
  - HIB.py -> carros/HIBB.py con anclas (cada una exacta UNA vez). Lo que se agrega:
      BB = 'ref'  (perilla de ablacion de la boca_buena; 'ref' == el puente boca_buena del puenteo, bit a bit en la fisica)
      _bb()       decide la mordida final sobre letras NO malas para O1 segun BB (ver HIBB.BB_MODOS)
      telemetria SOLO LECTURA de la direccion de la discrepancia O1 vs V143 (veto / fuerza; conocida / desconocida; nivel)
Uso: python construye_bb.py            (escribe carros/)
     python construye_bb.py --verifica (reconstruye en memoria y compara con disco; no escribe)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(os.path.dirname(AQUI), 'comite2', 'puenteo', 'carros')
DEST = os.path.join(AQUI, 'carros')
SHAS = {'HIB.py': '8dbae3522c01517b', 'O1P.py': '94861fe2d6ba8c45', 'V143P.py': '98823206dbb6a27d'}

sha = lambda b: hashlib.sha256(b).hexdigest()[:16]

ANCLAS = [
    # 1. encabezado
    ('# EXPLORATORIO, no es dato\n"""HIB.py',
     '# EXPLORATORIO, no es dato\n# GENERADO por experimentos/organelos/boca_buena/construye_bb.py desde comite2/puenteo/carros/HIB.py (sha 8dbae3522c01517b). NO editar a mano.\n'
     '# Unica diferencia de conducta: la perilla BB (ablaciones de la boca_buena). BB = \'ref\' == HIB del puenteo en la fisica.\n"""HIB.py'),
    # 2. perilla
    ("MEM_REPS = 5    # memoria:",
     "BB = 'ref'      # boca_buena (diagnostico 28-sep): el runner la fija ANTES de pista.run. Ver BB_MODOS.\n"
     "BB_MODOS = ('ref', 'veto', 'fuerza', 'sinprueba', 'soloprueba', 'm0', 'vetom0', 'glotu', 'todo', 'vetoc', 'fuerzac', 'm10', 'm40', 'ventana', 'tinv', 'tinv40')\n"
     "MEM_REPS = 5    # memoria:"),
    # 3. telemetria nueva en __init__
    ("boca_buena_dec=0, boca_buena_dif=0, mem_lecciones=0, mem_nacidos=0, cuerpos=1)",
     "boca_buena_dec=0, boca_buena_dif=0, mem_lecciones=0, mem_nacidos=0, cuerpos=1)\n"
     "        if BB not in BB_MODOS: raise SystemExit(f\"HIBB: BB invalido {BB!r}\")\n"
     "        self.BB = BB; self.U = float(ctx['rep_umbral'])\n"
     "        self.X = float(ctx['rep_X']); self.C = (float(ctx['costo']), float(ctx['costo_a']))   # ventana: cantidades del mundo que el carro ya recibe\n"
     "        self.bbt = dict(desc_dec=0, desc_veto=0, desc_fuerza=0, bue_dec=0, bue_veto=0, bue_fuerza=0,\n"
     "                        bue_veto_rel=0, bue_veto_norel=0, bue_fuerza_bajoU=0, bue_fuerza_margen=0, bue_fuerza_filtro=0,\n"
     "                        bue_fuerza_nosirve_act=0, cambia=0, mord_final_bue=0)"),
    # 4. la decision puenteada pasa por _bb
    ("            if (malo and P['boca_mala']) or ((not malo) and P['boca_buena']):\n"
     "                st['boca_puenteada'] += int(mo != mordio); mordio = mo\n",
     "            if (not malo) and P['boca_buena']: self._bb_tel(k, od['lev'], mo, mordio)   # boca_buena: telemetria (solo lectura)\n"
     "            if (malo and P['boca_mala']) or ((not malo) and P['boca_buena']):\n"
     "                if not malo: mo = self._bb(k, od['lev'], mo, mordio)   # boca_buena: ablacion (BB = 'ref' -> mo tal cual)\n"
     "                st['boca_puenteada'] += int(mo != mordio); mordio = mo\n"
     "                if not malo: self.bbt['mord_final_bue'] += int(mordio)\n"),
    # 5. funciones nuevas antes de resultado
    ("    def resultado(self, res):\n        self.v.resultado(res); self.o.resultado(res)\n",
     "    # ---------------------------------------------------------------- boca_buena: ablaciones (diagnostico 28-sep)\n"
     "    def _sirve(self, v, lev, umbral):\n"
     "        \"\"\"True si la letra de valor v (O1 la cree NO mala) sube alguna necesidad j con lev[j] < umbral.\"\"\"\n"
     "        return any(v[j] > 0 and lev[j] < umbral for j in (0, 1))\n"
     "\n"
     "    def _bb(self, k, lev, mo, mv):\n"
     "        \"\"\"Mordida final sobre letra NO mala para O1. mo = O1 (MARGEN + PRUEBA), mv = V143 (boca + FILTRO + APR).\"\"\"\n"
     "        B = self.BB; con = k in self.o.n\n"
     "        if B == 'ref': return mo\n"
     "        if B == 'veto': return bool(mo and mv)                  # O1 solo puede decir NO\n"
     "        if B == 'fuerza': return bool(mo or mv)                 # O1 solo puede decir SI\n"
     "        if B == 'sinprueba': return mo if con else mv           # sin neofobia: lo desconocido lo decide V143\n"
     "        if B == 'soloprueba': return mv if con else mo          # solo neofobia: lo conocido lo decide V143\n"
     "        if B == 'vetoc': return bool(mo and mv) if con else mv  # O1 solo dice NO, y solo sobre lo conocido (sin neofobia)\n"
     "        if B == 'fuerzac': return bool(mo or mv) if con else mv # O1 solo dice SI, y solo sobre lo conocido (sin neofobia)\n"
     "        if B in ('m10', 'm40', 'ventana', 'tinv', 'tinv40') and not con: return mv   # barrido del margen: lo desconocido lo decide V143\n"
     "        if B == 'm10': return self._sirve(self.o._val(k), lev, self.U + 0.10)   # barrido: margen 0.10 sobre rep_umbral\n"
     "        if B == 'm40': return self._sirve(self.o._val(k), lev, self.U + 0.40)   # barrido: margen 0.40 sobre rep_umbral\n"
     "        if B == 'ventana':   # muerde si alguna necesidad que sube NO alcanza a cubrir lo que falta de la ventana de parto\n"
     "            v = self.o._val(k); falta = max(self.X - self.v._avent, 0.0)\n"
     "            return any(v[j] > 0 and (lev[j] - self.U) < falta * self.C[j] for j in (0, 1))\n"
     "        if B == 'tinv':      # CONTROL desfasado del termostato (margen 0.25): lee el nivel de la necesidad que la letra NO sube\n"
     "            v = self.o._val(k)\n"
     "            return any(v[j] > 0 and lev[1 - j] < self.U + 0.25 for j in (0, 1))\n"
     "        if B == 'tinv40':    # CONTROL desfasado del termostato U + g/2 (= m40 en esta pista): lee la necesidad que la letra NO sube\n"
     "            v = self.o._val(k)\n"
     "            return any(v[j] > 0 and lev[1 - j] < self.U + v[j] / 2 for j in (0, 1))\n"
     "        v = self.o._val(k) if con else None\n"
     "        if B == 'm0': return (self._sirve(v, lev, self.U) if con else mo)            # MARGEN 0: umbral = rep_umbral\n"
     "        if B == 'todo': return (any(v[j] > 0 for j in (0, 1)) if con else mo)       # sin umbral: todo lo bueno conocido (PRUEBA igual)\n"
     "        if B == 'vetom0': return bool(mv and (self._sirve(v, lev, self.U) if con else True))   # solo veto, umbral rep_umbral, sin neofobia\n"
     "        if B == 'glotu':   # GLOTU (muro) en el marco del hibrido: veta lo que solo sube la necesidad MAS llena ya en rep_umbral\n"
     "            if not con: return mv\n"
     "            js = [j for j in (0, 1) if v[j] > 0]\n"
     "            if len(js) == 1 and not (v[1 - js[0]] > 0):\n"
     "                j = js[0]\n"
     "                if lev[j] >= self.U and lev[j] > lev[1 - j]: return False\n"
     "            return mv\n"
     "        raise SystemExit(f'HIBB: BB {B!r}')\n"
     "\n"
     "    def _bb_tel(self, k, lev, mo, mv):\n"
     "        \"\"\"SOLO LECTURA: direccion de la discrepancia O1 (mo) vs V143 (mv) sobre letras no malas, con la decision CRUDA de O1.\"\"\"\n"
     "        t = self.bbt; con = k in self.o.n\n"
     "        if not con:\n"
     "            t['desc_dec'] += 1; t['desc_veto'] += int(mv and not mo); t['desc_fuerza'] += int(mo and not mv); return\n"
     "        v = self.o._val(k); t['bue_dec'] += 1\n"
     "        if mv and not mo:\n"
     "            t['bue_veto'] += 1\n"
     "            js = [j for j in (0, 1) if v[j] > 0]\n"
     "            rel = len(js) == 1 and lev[js[0]] > lev[1 - js[0]]\n"
     "            t['bue_veto_rel' if rel else 'bue_veto_norel'] += 1\n"
     "        if mo and not mv:\n"
     "            t['bue_fuerza'] += 1\n"
     "            t['bue_fuerza_bajoU' if self._sirve(v, lev, self.U) else 'bue_fuerza_margen'] += 1\n"
     "            t['bue_fuerza_filtro'] += int(k in self.v._v3o)\n"
     "            t['bue_fuerza_nosirve_act'] += int(not (v[self.v._na] > 0))\n"
     "\n"
     "    def resultado(self, res):\n        self.v.resultado(res); self.o.resultado(res)\n"),
    # 6. salida
    ("        return dict(puentes=dict(self.P), mem_reps=MEM_REPS, hib=dict(self.st), v143=self.v.salida(), o1=self.o.salida())",
     "        return dict(puentes=dict(self.P), mem_reps=MEM_REPS, hib=dict(self.st), v143=self.v.salida(), o1=self.o.salida(),\n"
     "                    bb=self.BB, bbt=dict(self.bbt))"),
]


def construye():
    out = {}
    for n in SHAS:
        b = open(os.path.join(ORIG, n), 'rb').read()
        if sha(b) != SHAS[n]: raise SystemExit(f"CONSTRUYE: {n} sha {sha(b)} != {SHAS[n]}")
        out[n] = b
    src = out['HIB.py'].decode('utf-8')
    for a, b in ANCLAS:
        c = src.count(a)
        if c != 1: raise SystemExit(f"CONSTRUYE: ancla {a[:50]!r} aparece {c} veces")
        src = src.replace(a, b)
    return {'HIBB.py': src.encode('utf-8'), 'O1P.py': out['O1P.py'], 'V143P.py': out['V143P.py']}


def main():
    fs = construye()
    if '--verifica' in sys.argv[1:]:
        ok = all(open(os.path.join(DEST, n), 'rb').read() == b for n, b in fs.items())
        for n, b in fs.items(): print(f"  {n} {sha(b)}")
        print('VERIFICA', 'OK' if ok else 'FALLA'); return 0 if ok else 1
    os.makedirs(DEST, exist_ok=True)
    for n, b in fs.items():
        tmp = os.path.join(DEST, n + '.tmp')   # escritura atomica: hay colas leyendo carros/ entre corridas
        with open(tmp, 'wb') as fh: fh.write(b)
        os.replace(tmp, os.path.join(DEST, n))
        print(f"  escrito carros/{n} {sha(b)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
