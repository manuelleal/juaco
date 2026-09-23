"""construye_n9b.py — construye POR ANCLAS los carros de la segunda tanda del nivel 9 (subida_n9b): lesiones de la
PREDICCION DE SI aprendida por APR.

MISION: llegar a la AGI por este camino.

Origen (solo se LEE): experimentos/carrera_escuderias/carros/APR.py, sha fijado SHA_APR (FABRICA + la correccion de la boca
aprendida por TD, heredada; serie 8101-8120 y replica 8121-8140). Se trabaja en BYTES (APR.py tiene fines de linea CRLF).

Salidas en experimentos/subida_n9b/carros/:
  APR.py            copia VERBATIM (mismo sha).
  APR_LES_OFF.py    APR + el INSTRUMENTO de lesion con las perillas apagadas: tiene que ser APR BIT A BIT (identidad_n9b.py).
  APR_LES_PLANA.py  LES_PRED = 'plana': el rasgo post (min(E,Ag) predicho tras morder, con lo que el linaje SINTIO de esa
                    letra) se reemplaza por u = min(E,Ag) actual: "morder no me cambia". Sin rng.
  APR_LES_CRUZ.py   LES_PRED = 'cruz': post = min(E + dAg_k, Ag + dE_k): el efecto sentido de la letra aplicado a la OTRA
                    necesidad. Sin rng.
  APR_LES_MUNDO.py  LES_MUNDO = True: los rasgos del MUNDO (g0: no hay nada bueno; dist: distancia al bueno) se calculan con
                    lo bueno para la necesidad NO activa. Control de especificidad. Sin rng.
  FABRICA.py        copia VERBATIM (2ebee3e99ea5a33a): piso y la identidad corta del juez.
Uso: python experimentos/subida_n9b/construye_n9b.py   (reescribe carros/; sin argumentos; aborta ante cualquier argumento)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CARRERA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros')
ORIGEN = os.path.join(CARRERA, 'APR.py'); SHA_APR = '4402aa5142065c72'
ORIGEN_FAB = os.path.join(CARRERA, 'FABRICA.py'); SHA_FAB = '2ebee3e99ea5a33a'
DEST = os.path.join(AQUI, 'carros')
N = b'\r\n'

CAB = ('"""carros/APR.py — APR (camino A'.encode(),
       b'"""@@NOMBRE@@ (construido por experimentos/subida_n9b/construye_n9b.py desde carrera_escuderias/carros/APR.py sha '
       + SHA_APR.encode() + b'; instrumento de LESION de la prediccion de si, perillas LES_PRED / LES_MUNDO; apagadas = APR '
       b'bit a bit). ' + 'carros/APR.py — APR (camino A'.encode())

LESION = [
    # 1. perillas
    (b"P_AZAR = None" + N,
     b"P_AZAR = None" + N +
     b"# ---- LESIONES (subida_n9b; instrumento, no mecanismo; apagadas = APR bit a bit, arnes identidad_n9b.py)" + N +
     b"LES_PRED = None     # None | 'plana' (post = u actual) | 'cruz' (efecto sentido aplicado a la OTRA necesidad)" + N +
     b"LES_MUNDO = False   # True: g0 y dist con lo bueno para la necesidad NO activa (control de especificidad)" + N),
    # 2. telemetria de la lesion (no decide nada)
    (b"self._aL = int(ctx['L'])",
     b"self._aL = int(ctx['L']); self._les = dict(n=0, post_real=0.0, post_usado=0.0, cambia_post=0, caida_real=0, "
     b"caida_usada=0, cambia_mundo=0)"),
    # 3. rasgos del mundo: con LES_MUNDO, lo bueno para la otra necesidad
    (b"if z[na] / z[2] > 0}", b"if z[(1 - na) if LES_MUNDO else na] / z[2] > 0}"),
    # 4. la prediccion de si
    (b"post = min(E + m[0] / m[2], Ag + m[1] / m[2])" + N,
     b"post = min(E + m[0] / m[2], Ag + m[1] / m[2])" + N +
     b"        if LES_PRED or LES_MUNDO: post = self._lesiona(post, E, Ag, u, m, obs, pos, na, dmin)" + N),
    # 5. la lesion
    (b"    def _apr_muere(self, info):",
     b"    def _lesiona(self, post, E, Ag, u, m, obs, pos, na, dmin):" + N +
     b"        \"\"\"LESION (subida_n9b). Devuelve el post que USA la decision (y el TD). plana: u; cruz: el efecto sentido de la" + N +
     b"        letra sobre la OTRA necesidad. Con LES_MUNDO cuenta las decisiones donde g0/dist difieren de los verdaderos.\"\"\"" + N +
     b"        pu = post" + N +
     b"        if LES_PRED == 'plana': pu = u" + N +
     b"        elif LES_PRED == 'cruz': pu = min(E + m[1] / m[2], Ag + m[0] / m[2])" + N +
     b"        elif LES_PRED is not None: raise SystemExit(f\"APR: LES_PRED invalido {LES_PRED!r}\")" + N +
     b"        s = self._les; s['n'] += 1; s['post_real'] += post; s['post_usado'] += pu" + N +
     b"        s['cambia_post'] += int(abs(pu - post) > 1e-12); s['caida_real'] += int(post < u - 1e-9); s['caida_usada'] += int(pu < u - 1e-9)" + N +
     b"        if LES_MUNDO:" + N +
     b"            bv = {k for k, z in self._adS.items() if z[na] / z[2] > 0}; dv = None; L = self._aL" + N +
     b"            for x, k in obs['objs'].items():" + N +
     b"                if x != pos and k in bv:" + N +
     b"                    d = min((pos - x) % L, (x - pos) % L)" + N +
     b"                    if dv is None or d < dv: dv = d" + N +
     b"            s['cambia_mundo'] += int(dv != dmin)" + N +
     b"        return pu" + N +
     N +
     b"    def _apr_muere(self, info):"),
    # 6. salida: la telemetria de la lesion solo con alguna perilla encendida (apagadas: salida identica)
    (b"for k, z in sorted(self._adS.items())}, **st)",
     b"for k, z in sorted(self._adS.items())}, **st, "
     b"**({'lesion': dict(self._les, pred=LES_PRED, mundo=LES_MUNDO)} if (LES_PRED or LES_MUNDO) else {}))"),
]
PERILLAS = {'APR_LES_OFF': (),
            'APR_LES_PLANA': ((b"\nLES_PRED = None     #", b"\nLES_PRED = 'plana'  #"),),
            'APR_LES_CRUZ': ((b"\nLES_PRED = None     #", b"\nLES_PRED = 'cruz'   #"),),
            'APR_LES_MUNDO': ((b"\nLES_MUNDO = False   #", b"\nLES_MUNDO = True    #"),)}
BRAZOS = ('APR', 'FABRICA', 'APR_LES_PLANA', 'APR_LES_CRUZ', 'APR_LES_MUNDO')


def h16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def aplica(src, anclas, nombre):
    out = src
    for i, (a, b) in enumerate(anclas, 1):
        n = out.count(a)
        if n != 1: raise SystemExit(f"CONSTRUYE {nombre}: el ancla {i} aparece {n} veces (tiene que ser 1): {a[:70]!r}")
        out = out.replace(a, b)
    return out


def construye(escribe=True):
    src = open(ORIGEN, 'rb').read(); sha = h16(src)
    if sha != SHA_APR: raise SystemExit(f"CONSTRUYE: APR.py cambio ({sha} != {SHA_APR})")
    fab = open(ORIGEN_FAB, 'rb').read()
    if h16(fab) != SHA_FAB: raise SystemExit(f"CONSTRUYE: FABRICA.py cambio ({h16(fab)} != {SHA_FAB})")
    res = {'APR': src, 'FABRICA': fab}
    base = aplica(src, LESION, 'lesion')
    for nom, per in PERILLAS.items():
        cab = (CAB[0], CAB[1].replace(b'@@NOMBRE@@', nom.encode()))
        res[nom] = aplica(aplica(base, [cab], nom), list(per), nom)
    if escribe:
        os.makedirs(DEST, exist_ok=True)
        for nom, b in res.items():
            open(os.path.join(DEST, nom + '.py'), 'wb').write(b)
    return {n: h16(b) for n, b in res.items()}, res


if __name__ == '__main__':
    if len(sys.argv) > 1: raise SystemExit(f"construye_n9b.py no acepta argumentos: {sys.argv[1:]}")
    shas, _ = construye(escribe=True)
    for n, s in shas.items(): print(f"  {n:15s} {s}")
