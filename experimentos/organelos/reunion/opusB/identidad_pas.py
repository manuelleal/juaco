"""identidad_pas.py — ARNES de los PASAJES (Opus B, reunion 28-sep-2026). Se corre ANTES de mirar numeros de cadenas.

(K) carros en disco == construye_pas; shas del origen.
(a) V143_PAS0 (PASAJE 0) == V143_EVO_BAJO: salida ENTERA de pista.run y _TEL (s 58301, T 3000, 9 carros).
(b) regla 14: corre_pas.tarea(V143) == corre_v143.tarea (salvo 'seg'); y con V143_TERMO / O1 igual.
(c) 1 pasaje SIN transferencia == runner de origen: corre_pas.tarea(V143_PAS, siembra None, pmut 0) == corre_evo.tarea(V143_EVO_BAJO)
    de termo_banco en linajes/pista/R0_pista (s 58302, T 4000). Y con pmut 0.05 (ctl real) DIFIERE (el cerebro muta: control que falla).
(d) la transferencia ACTUA: siembra con g = 0.40 hace otra fisica que siembra None (s 58302, T 4000); y los fundadores salen de ella.
(e) la transferencia NO usa fitness: siembra() solo lee vivos_b; alterar partos/muertes/juez no cambia la siembra; y la siembra de un
    run real sale solo de t >= T - 5000.
(f) determinismo: la misma tarea dos veces == (con siembra y mutacion).
"""
import copy, json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_pas as CP
import construye_pas as CB
CV = CP.CV; P = CP.P
TB = os.path.join(CP.RAIZ, 'experimentos', 'organelos', 'termo_banco')
sys.path.insert(0, TB)
import corre_evo as CE   # termo_banco: copia con anclas del runner de TERMO_EVO (se IMPORTA, no se toca)

N = lambda x: json.loads(json.dumps(x, default=str))
OK = True


def chk(nombre, c):
    global OK
    OK &= bool(c); print(f"  {'OK   ' if c else 'FALLA'} {nombre}", flush=True)


def sin_seg(x): return N({k: v for k, v in x.items() if k not in ('seg', 'tel_ps', 'tel_evo')})


t0 = time.time()
print("ARNES identidad_pas.py")
# (K)
for n, b in CB.todas().items():
    chk(f"(K) {n} en disco == construye_pas (sha {CB.h16b(b)})", open(os.path.join(CP.CARROS, n + '.py'), 'rb').read() == b)
for r, s in CP.SHAS.items(): chk(f"(K) sha {os.path.relpath(r, CP.RAIZ)} == {s}", CP.h16(r) == s)
M = CP.registra(); CE.registra()
# (a)
mb = CV._MODS['V143_EVO_BAJO']; m0 = CV._MODS['V143_PAS0']
mb._TEL.clear(); xa = N(P.run(58301, [('C', mb)] * 9, T=3000, fundador_limpio=1)); ta = N(mb._TEL)
m0._TEL.clear(); xb = N(P.run(58301, [('C', m0)] * 9, T=3000, fundador_limpio=1)); tb = N(m0._TEL)
chk("(a) V143_PAS0 == V143_EVO_BAJO salida ENTERA (s 58301, T 3000)", xa == xb)
chk("(a) V143_PAS0 == V143_EVO_BAJO _TEL", ta == tb)
# (b)
for ident in ('V143', 'V143_TERMO', 'O1'):
    x = CP.tarea(58301, ident, 2000); y = CV.tarea((58301, ident, 2000))
    chk(f"(b) regla 14: corre_pas.tarea({ident}) == corre_v143.tarea (s 58301, T 2000)", x.pop('tel_ps') is None and sin_seg(x) == sin_seg(y))
# (c)
x = CP.tarea(58302, 'V143_PAS', 4000, siembra=None, pmut=0.0); y = CE.tarea((58302, 'V143_EVO_BAJO', 4000))
def _sinid(x):   # v2: el nombre del carro va en 'id'/'ids' ('V143_PAS#i' vs 'V143_EVO_BAJO#i'); se normaliza, lo demas se compara
    return json.loads(json.dumps(N(x)).replace('V143_EVO_BAJO#', 'C#').replace('V143_PAS#', 'C#'))
same = lambda u, v: _sinid(u['linajes']) == _sinid(v['linajes']) and u['R0_pista'] == v['R0_pista'] and _sinid(u['pista']) == _sinid(v['pista'])
chk("(c) 1 pasaje sin transferencia, pmut 0 == corre_evo.tarea(V143_EVO_BAJO) (linajes, pista, R0_pista; s 58302, T 4000)", same(x, y))
z = CP.tarea(58302, 'V143_PAS', 4000, siembra=None, pmut=0.05)
chk("(c) control que puede fallar: con pmut 0.05 (el cerebro muta) la fisica DIFIERE", not same(z, y))
fp = [f for v in z['tel_ps'].values() for f in v.get('fund_ps', [])]
chk(f"(c) sin siembra ningun fundador sale de siembra ({sum(f[0] for f in fp)}/{len(fp)})", len(fp) > 0 and sum(f[0] for f in fp) == 0)
# (d)
G0 = CP.g0_fabrica()
S40 = [dict(g=0.40, b=dict(G0))]
w = CP.tarea(58302, 'V143_PAS', 4000, siembra=S40, pmut=0.05)
fw = [f for v in w['tel_ps'].values() for f in v.get('fund_ps', [])]
chk(f"(d) con siembra g 0.40: todos los fundadores de siembra ({sum(f[0] for f in fw)}/{len(fw)}), g medio {round(sum(f[1] for f in fw)/len(fw),3)}",
    len(fw) > 0 and sum(f[0] for f in fw) == len(fw) and abs(sum(f[1] for f in fw) / len(fw) - 0.40) < 0.05)
chk("(d) la transferencia ACTUA: fisica con siembra != sin siembra", not same(w, z))
chk("(d) el modulo queda limpio tras la tarea (SIEMBRA None)", CV._MODS['V143_PAS'].SIEMBRA is None)
# (e)
viv = {i: v.get('vivos_b', []) for i, v in w['tel_ps'].items()}
s1 = CP.siembra(viv, 4000)
tel2 = copy.deepcopy(w['tel_ps'])
for v in tel2.values():
    v['partos'] = []; v['muertes'] = [[0, 9.9, 1, 99, 0]]; v['gbin'] = {}
s2 = CP.siembra({i: v.get('vivos_b', []) for i, v in tel2.items()}, 4000)
chk(f"(e) siembra solo de vivos_b: alterar partos/muertes no la cambia (n {len(s1 or [])})", s1 == s2 and s1 is not None)
chk("(e) siembra toma solo t >= T - 5000 (T 4000: todas; T 2000 con vent 1000: solo t >= 1000)",
    len(CP.siembra(viv, 2000, vent=1000) or []) == sum(1 for v in viv.values() for q in v if q[0] >= 1000))
import inspect
chk("(e) la firma de siembra() es (vivos_b, T, vent)", list(inspect.signature(CP.siembra).parameters) == ['vivos_b', 'T', 'vent'])
# (f)
w2 = CP.tarea(58302, 'V143_PAS', 4000, siembra=S40, pmut=0.05)
chk("(f) determinismo con siembra y mutacion", sin_seg(w) == sin_seg(w2) and N(w['tel_ps']) == N(w2['tel_ps']))
print(f"{'ARNES PASA' if OK else 'ARNES FALLA'}  ({time.time()-t0:.0f}s)")
sys.exit(0 if OK else 1)
