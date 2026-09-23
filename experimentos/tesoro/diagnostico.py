# EXPLORATORIO, no es dato. Que las detuvo: muertes por tarea, y sensibilidad a la energia inicial.
import sys, collections, statistics as st, json
import tesoro as T

def causa(E0):
    T.E0 = E0
    out = {}
    for brazo in ('SIN', 'CANAL', 'RUIDO'):
        muertas = collections.Counter(); vivas_atasc = 0; lleg = []
        for s in range(7101, 7121):
            # re-corre copiando la logica: capturamos las bacterias parcheando Bact
            creadas = []
            orig = T.Bact.__init__
            def init(self, rng, pos, _o=orig):
                _o(self, rng, pos); creadas.append(self)
            T.Bact.__init__ = init
            import random
            rng = random.Random(s); r = T.corre(brazo, s)
            T.Bact.__init__ = orig
            # reconstruir orden de tareas igual que corre()
            rng = random.Random(s); est = []
            while len(est) < 5:
                p = (rng.randrange(T.L), rng.randrange(T.L))
                if all(abs(p[0]-q[0]) + abs(p[1]-q[1]) >= 6 for q in est): est.append(p)
            tareas = T.TAREAS[:]; rng.shuffle(tareas)
            for b in creadas:
                if b.llego is not None: continue
                if b.vivo: vivas_atasc += 1
                else: muertas[tareas[b.k]] += 1
            lleg.append(r['llegan'])
        out[brazo] = dict(muertas_por_tarea=dict(muertas), vivas_sin_llegar=vivas_atasc, llegan_mediana=st.median(lleg))
        print(E0, brazo, out[brazo])
    return out

res = {e: causa(e) for e in (30.0, 45.0)}
json.dump(dict(EXPLORATORIO='no es dato', res=res), open('diagnostico.json', 'w'), indent=1)
