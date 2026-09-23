# EXPLORATORIO, no es dato. Busqueda del tesoro: plano 2D, estaciones con pruebas de bits,
# pizarra comun. Python puro, un proceso. Uso: python tesoro.py [--humo]
import random, json, sys, statistics as st

TAREAS = ['AND', 'XOR', 'OR', 'SUMA', 'XNOR']  # SUMA = medio sumador: 4 clases (acarreo,suma)
NRESP = {'AND': 2, 'XOR': 2, 'OR': 2, 'SUMA': 4, 'XNOR': 2}

def correcta(t, a, b):
    if t == 'AND': return a & b
    if t == 'XOR': return a ^ b
    if t == 'OR': return a | b
    if t == 'XNOR': return 1 - (a ^ b)
    return 2 * (a & b) + (a ^ b)

L = 20; E0 = 30.0; C_MOV = 0.25; C_INT = 0.3; R_OK = 0.15; R_MAL = -0.4
R_EST = 6.0; RACHA = 4; ETA = 0.2; EPS = 0.1

class Bact:
    def __init__(s, rng, pos):
        s.rng = rng; s.x, s.y = pos; s.E = E0; s.k = 0; s.racha = 0
        s.vivo = True; s.llego = None; s.w = {}  # (k, rasgo, resp) -> peso
        s.usos_piz = 0; s.usos_piz_ok = 0; s.intentos = 0
    def val(s, fs, r, k):
        return sum(s.w.get((k, f, r), 0.0) for f in fs) + s.w.get(('P', r), 0.0) * 0  # (placeholder)
    def elige(s, k, fs, sug, n):
        if s.rng.random() < EPS: return s.rng.randrange(n)
        v = [sum(s.w.get((k, f, r), 0.0) for f in fs) + (s.w.get('confia', 0.0) if sug == r else 0.0) for r in range(n)]
        m = max(v); c = [r for r in range(n) if v[r] == m]
        return s.rng.choice(c)
    def aprende(s, k, fs, r, rec, sug):
        # IND: cada rasgo aprende por separado hacia la recompensa (1 acierto / 0 fallo)
        for f in fs:
            key = (k, f, r); s.w[key] = s.w.get(key, 0.0) + ETA * (rec - s.w.get(key, 0.0))
        if sug is not None and sug == r:  # confianza en la pizarra: aprendida, compartida entre estaciones
            s.w['confia'] = s.w.get('confia', 0.0) + ETA * (rec - s.w.get('confia', 0.0))

def corre(brazo, semilla, N=12, T=3000):
    rng = random.Random(semilla)
    # estaciones en cadena, sitios al azar por semilla (no fijos), separadas >= 6
    est = []
    while len(est) < 5:
        p = (rng.randrange(L), rng.randrange(L))
        if all(abs(p[0]-q[0]) + abs(p[1]-q[1]) >= 6 for q in est): est.append(p)
    meta = est[-1]  # tras la ultima estacion: comida infinita en ese mismo punto al resolverla
    tareas = TAREAS[:]; rng.shuffle(tareas)
    bs = [Bact(random.Random(rng.random()), (rng.randrange(L), rng.randrange(L))) for _ in range(N)]
    piz = {}  # (k,a,b) -> respuesta escrita por quien acerto
    primera = None; hist_llegada = []
    for t in range(T):
        activos = [b for b in bs if b.vivo and b.llego is None]
        if not activos: break
        for b in activos:
            tx, ty = est[b.k]
            if (b.x, b.y) != (tx, ty):  # el mundo le muestra la direccion a la estacion abierta
                if b.x != tx and (b.y == ty or b.rng.random() < 0.5): b.x += 1 if tx > b.x else -1
                else: b.y += 1 if ty > b.y else -1
                b.E -= C_MOV
            else:
                tarea = tareas[b.k]; n = NRESP[tarea]
                a, c = rng.randrange(2), rng.randrange(2)
                fs = ('sesgo', 'a%d' % a, 'b%d' % c, 'p%d%d' % (a, c))
                if brazo == 'CANAL': sug = piz.get((b.k, a, c))
                elif brazo == 'RUIDO': sug = rng.randrange(n) if piz.get((b.k, a, c)) is not None else None
                else: sug = None
                r = b.elige(b.k, fs, sug, n)
                if sug is not None:
                    b.usos_piz += 1
                    if r == sug: b.usos_piz_ok += 1
                ok = (r == correcta(tarea, a, c)); b.intentos += 1
                b.aprende(b.k, fs, r, 1.0 if ok else 0.0, sug)
                b.E += (R_OK if ok else R_MAL) - C_INT
                if ok:
                    if brazo != 'SIN': piz.setdefault((b.k, a, c), r)  # escribe lo que le dio comida
                    b.racha += 1
                    if b.racha >= RACHA:
                        b.racha = 0; b.E += R_EST; b.k += 1
                        if b.k == len(est):
                            b.llego = t; hist_llegada.append(t)
                            if primera is None: primera = t
                else: b.racha = 0
            if b.E <= 0: b.vivo = False
    llegan = [b for b in bs if b.llego is not None]
    tardias = [b for b in llegan if b.llego != primera]
    return dict(brazo=brazo, semilla=semilla, llegan=len(llegan), primera=primera,
                est_mediana=st.median([b.k for b in bs]),
                intentos_med=st.median([b.intentos for b in bs]),
                usos_piz_tardias=(st.mean([b.usos_piz for b in tardias]) if tardias else None),
                sigue_piz_tardias=(st.mean([b.usos_piz_ok / b.usos_piz for b in tardias if b.usos_piz]) if any(b.usos_piz for b in tardias) else None),
                confia_final=st.mean([b.w.get('confia', 0.0) for b in bs]))

def main():
    humo = '--humo' in sys.argv
    semillas = [7101, 7102] if humo else list(range(7101, 7121))
    res = []
    for brazo in ('SIN', 'CANAL', 'RUIDO'):
        for s in semillas: res.append(corre(brazo, s))
    out = []
    for brazo in ('SIN', 'CANAL', 'RUIDO'):
        R = [r for r in res if r['brazo'] == brazo]
        pr = [r['primera'] for r in R if r['primera'] is not None]
        conf = [r['confia_final'] for r in R]
        line = dict(brazo=brazo, semillas=len(R),
                    semillas_con_llegada=sum(r['llegan'] > 0 for r in R),
                    llegan_mediana=st.median([r['llegan'] for r in R]),
                    llegan_rango=(min(r['llegan'] for r in R), max(r['llegan'] for r in R)),
                    primera_mediana=(st.median(pr) if pr else None),
                    estacion_mediana=st.median([r['est_mediana'] for r in R]),
                    intentos_mediana=st.median([r['intentos_med'] for r in R]),
                    sigue_piz_tardias=(round(st.mean([r['sigue_piz_tardias'] for r in R if r['sigue_piz_tardias'] is not None]), 3) if any(r['sigue_piz_tardias'] is not None for r in R) else None),
                    confia_final=round(st.mean(conf), 3))
        out.append(line); print(line)
    # pareado por semilla: CANAL vs SIN en numero de llegadas
    S = {r['semilla']: r for r in res if r['brazo'] == 'SIN'}
    C = {r['semilla']: r for r in res if r['brazo'] == 'CANAL'}
    Rr = {r['semilla']: r for r in res if r['brazo'] == 'RUIDO'}
    gana = sum(C[s]['llegan'] > S[s]['llegan'] for s in semillas); emp = sum(C[s]['llegan'] == S[s]['llegan'] for s in semillas)
    gana_r = sum(C[s]['llegan'] > Rr[s]['llegan'] for s in semillas); emp_r = sum(C[s]['llegan'] == Rr[s]['llegan'] for s in semillas)
    par = dict(canal_gana_a_sin=gana, empates_sin=emp, canal_gana_a_ruido=gana_r, empates_ruido=emp_r, n=len(semillas))
    print(par)
    nombre = 'resultados_humo.json' if humo else 'resultados.json'
    json.dump(dict(EXPLORATORIO='no es dato', parametros=dict(L=L, E0=E0, C_MOV=C_MOV, C_INT=C_INT, R_OK=R_OK, R_MAL=R_MAL, R_EST=R_EST, RACHA=RACHA, ETA=ETA, EPS=EPS),
                   resumen=out, pareado=par, corridas=res), open(nombre, 'w'), indent=1)

if __name__ == '__main__':
    main()
