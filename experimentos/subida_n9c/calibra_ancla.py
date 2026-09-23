"""calibra_ancla.py — CALIBRACION DECLARADA del ancla V-ANCLA de subida_n9c (ERR-116: el ancla se calibra sobre datos YA
medidos del mismo brazo en el mismo mundo, ANTES de correr semillas nuevas). No corre ninguna simulacion: solo LEE.

MISION: llegar a la AGI por este camino.

Fuente: subida_n10, serie 12301-12320 (sha del JSON fijado abajo), brazo NADA (= FABRICA bit a bit en la pista v2 con
quimiostato; N9C_NADA es FABRICA bit a bit tambien: arnes identidad_n9c.py). Medida: R0_nacidos por semilla (hijos por
cuerpo NACIDO, cohorte t <= T/2), calculada con la MISMA formula que corre_n9c.py.
Metodo: intervalo de prediccion al 99 % de la MEDIANA de 20 semillas nuevas = bootstrap de DOS etapas (1: se remuestrean los
20 valores medidos con reemplazo = una poblacion plausible; 2: de esa poblacion se sacan 20 semillas 'nuevas' con reemplazo y
se toma su mediana; 200 000 replicas, rng 20260923). Asi entra la incertidumbre de la serie medida Y la de la serie nueva.
Redondeado hacia afuera a 0.005.
Persistencia: FABRICA no persiste en ninguna semilla en dos series de v2 (generaciones 10101-10120: 0/20; n10 NADA: 0/20).
Uso: python experimentos/subida_n9c/calibra_ancla.py        (sin argumentos; imprime el ancla y su sha de entrada)
"""
import hashlib, json, math, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
FUENTE = os.path.join(RAIZ, 'experimentos', 'subida_n10', 'datos', 'n10_serie_s12301-12320_T100000_20260923_161438.json')
SHA_FUENTE = 'bbc9291c9a1059e6'
N_REP = 200000; SEMILLA_RNG = 20260923; NIVEL = 0.99


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def calibra():
    if h16(FUENTE) != SHA_FUENTE: raise SystemExit(f"calibra_ancla: la fuente cambio ({h16(FUENTE)} != {SHA_FUENTE})")
    d = json.load(open(FUENTE, encoding='utf-8'))
    xs = np.array(sorted(c['estr']['NADA']['R0_nacidos'] for c in d['por_semilla'] if c['brazo'] == 'NADA'), float)
    pc = sum(bool(c['estr']['NADA']['persiste_carro']) for c in d['por_semilla'] if c['brazo'] == 'NADA')
    rng = np.random.default_rng(SEMILLA_RNG)
    pob = xs[rng.integers(0, len(xs), (N_REP, len(xs)))]                       # etapa 1: poblacion plausible
    nue = np.take_along_axis(pob, rng.integers(0, len(xs), (N_REP, len(xs))), 1)   # etapa 2: 20 semillas nuevas
    meds = np.median(nue, axis=1)
    lo, hi = np.quantile(meds, [(1 - NIVEL) / 2, 1 - (1 - NIVEL) / 2])
    lo_r = math.floor(lo / 0.005) * 0.005; hi_r = math.ceil(hi / 0.005) * 0.005
    return dict(n=len(xs), mediana=float(np.median(xs)), minimo=float(xs.min()), maximo=float(xs.max()),
                q_lo=round(float(lo), 4), q_hi=round(float(hi), 4), ancla=(round(lo_r, 3), round(hi_r, 3)), persiste_carro=pc)


if __name__ == '__main__':
    if len(sys.argv) > 1: raise SystemExit(f"calibra_ancla: no acepta argumentos ({sys.argv[1:]})")
    r = calibra()
    print(f"fuente {os.path.basename(FUENTE)} sha {SHA_FUENTE} · NADA R0_nacidos n={r['n']} mediana {r['mediana']:.4f} "
          f"[{r['minimo']:.4f}, {r['maximo']:.4f}] · persiste_carro {r['persiste_carro']}/{r['n']}")
    print(f"bootstrap {N_REP} replicas, rng {SEMILLA_RNG}: IP {NIVEL:.0%} de la mediana de 20 nuevas = [{r['q_lo']}, {r['q_hi']}]")
    print(f"ANCLA V-ANCLA: mediana R0_nacidos de N9C_NADA en [{r['ancla'][0]:.3f}, {r['ancla'][1]:.3f}]")
