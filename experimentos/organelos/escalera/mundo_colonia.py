"""mundo_colonia.py — EL MUNDO DEL PELDANO 2 de la escalera: COLONIA CLONAL QUE SE QUEDA PEGADA y un CUELLO que premia el tamano
(30-sep-2026, ingeniero genetico Fable, MODO RAFAGA). Plan: ESCALERA.md (P2). Runner: corre_p2.py. Arnes: identidad_p2.py.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Transicion mayor 1 (Maynard Smith y Szathmary 1995; Ratcliff et al. 2012 PNAS, "snowflake yeast"): de celulas
sueltas a un grupo clonal que no se separa al dividirse, en un mundo donde el tamano paga.

QUE ES: la PISTA v2 CON GENERACIONES SOLAPADAS (experimentos/generaciones/motor_convive.py, sha SHA_MOTOR, NO se toca: parto real, cuerpo por
instancia, quimiostato, fundador limpio al extinguirse; es el motor debajo de JUACO-ECO) con TRES perillas nuevas:
  pega     (0/1): al parir, la hija NACE PEGADA a la madre: entra al GRUPO de la madre (si la madre no tenia grupo, lo funda y es la CABEZA).
           El grupo ocupa la celda de la cabeza: en su turno cada miembro actua con su propia cabeza (mov y muerde, como siempre), muerde
           donde llega (la celda de la cabeza o una vecina: la colonia tiene tantas bocas como miembros y un radio de 1) y AL FINAL de la
           fase A vuelve a la celda de la cabeza (el grupo se mueve como UNO: a donde va la cabeza). Si la cabeza muere, el miembro mas
           viejo hereda la cabeza. Un cuerpo suelto (sin grupo) es exactamente el de motor_convive. Con pega = 0 nadie se pega.
  cuello   (entero, 0 = apagado): cada `cuello` pasos, SEDIMENTACION: cada cuerpo muere con probabilidad p_suelto / k, con k = tamano de su
           grupo (1 si esta suelto). El grupo grande se queda; el suelto pasa el cuello a p_suelto. Es la seleccion por tamano de Ratcliff
           (el matraz que se deja sedimentar). La muerte por cuello pone E = 0: el cuerpo muere en la fase B de ese paso y el juez la cuenta
           como 'hambre' (declarado; se reporta aparte en _carrera['colonia']). rng NUEVA [seed, 0, ETQ_CUELLO=19, 0] (motor_convive usa
           11-15; ECO 16-17; escalera p1 18): no toca ninguna corriente del motor.
  p_suelto (0.5 de fabrica).
POR QUE ASI: "el mundo tiene que pagar cada capacidad y evitar no es gratis" (ESTADO 29-sep). Pegarse CUESTA (los miembros comparten el
vecindario de la cabeza y compiten por lo mismo; el quimiostato repone a tasa fija) y solo PAGA si hay cuello. Los controles que pueden
fallar: pega 1 SIN cuello (debe perder o empatar con suelto) y suelto CON cuello (debe perder con pegado).
Con pega = 0 y cuello = 0: run() ES motor_convive.run_solapadas BIT A BIT (arnes I1: _co = None, ningun gancho actua).

CONSTRUCCION POR ANCLAS (patron de mundo_escalera.py / pista_grande.py): construye() lee motor_convive.py (sha SHA_MOTOR), extrae
run_solapadas() y aplica ANCLAS (cada una EXACTAMENTE una vez): firma nueva, la colonia (_co) en el alta, la muestra, la reunion al final
de la fase A, el cuello antes de la fase B, la muerte, el parto y la salida. Todo lo demas es el de motor_convive: el codigo transformado
se ejecuta con los globales de motor_convive.
SALIDA NUEVA (solo con pega o cuello): pista['colonia'] y por linaje d['_carrera']['colonia'] (fisica de solo lectura: muertes por cuello,
tamano medio del grupo de sus cuerpos cada `muestra` pasos, grupos fundados, tamano maximo).
"""
import hashlib, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
GEN_D = os.path.join(RAIZ, 'experimentos', 'generaciones')
if GEN_D not in sys.path: sys.path.insert(0, GEN_D)
import motor_convive as MC

SHA_MOTOR = 'd10cb9021f5d0f41'   # motor_convive.py (el origen de motor_eco.py)
ETQ_CUELLO = 19
P_SUELTO = 0.5
FABRICA_MUNDO = dict(pega=0, cuello=0, p_suelto=P_SUELTO)

FIRMA_VIEJA = ("def run_solapadas(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None,\n"
               "                  fundador_limpio=0, tope_cuerpos=TOPE_DEF, muestra=MUESTRA, reposicion='fija', r_rep=R_REP):")
FIRMA_NUEVA = ("def run_solapadas(seed, carros, T=100000, pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=1, mundo_n=None,\n"
               "                  fundador_limpio=0, tope_cuerpos=TOPE_DEF, muestra=MUESTRA, reposicion='fija', r_rep=R_REP,\n"
               "                  pega=0, cuello=0, p_suelto=P_SUELTO, solo_sueltos=0):")
# REAPERTURA (30-sep, tras 3 humos sin senal con O1): solo_sueltos (0/1): el cuello mata SOLO a los sueltos (k = 1) con p_suelto; un cuerpo
# pegado (k >= 2) lo pasa siempre. Con 0 es la regla p_suelto / k de antes (bit a bit). "Cuello suave" = p_suelto 0.2 (perilla ya existente).
ANCLAS = [
    (FIRMA_VIEJA, FIRMA_NUEVA),
    ("    orden = list(range(len(cuerpos)))\n",
     "    orden = list(range(len(cuerpos)))\n"
     "    _co = (Colonia(seed, n, pega, cuello, p_suelto, solo_sueltos) if (pega or cuello) else None)\n"),
    ("        if t % muestra == 0:\n            for l in lin: l.tam.append(l.vivos)\n",
     "        if t % muestra == 0:\n            for l in lin: l.tam.append(l.vivos)\n"
     "            if _co is not None: _co.muestra(cuerpos)\n"),
    ("        # ---------------- costos\n        for b in cuerpos:\n            b.E -= M['costo']; b.Ag -= M['costo_a']\n",
     "        if _co is not None: _co.junta(cuerpos)   # P2: los miembros vuelven a la celda de su cabeza\n"
     "        # ---------------- costos\n        for b in cuerpos:\n            b.E -= M['costo']; b.Ag -= M['costo_a']\n"),
    ("        # ---------------- fase B\n        nuevos = []; muertos = False\n",
     "        if _co is not None and cuello and t > 0 and t % cuello == 0: _co.sedimenta(cuerpos, t)   # P2: el cuello (E = 0 a quien no pasa)\n"
     "        # ---------------- fase B\n        nuevos = []; muertos = False\n"),
    ("                b.vivo = False; l.vivos -= 1; total -= 1; muertos = True\n",
     "                b.vivo = False; l.vivos -= 1; total -= 1; muertos = True\n"
     "                if _co is not None: _co.muere(b)\n"),
    ("                    nuevos.append(H); l.vivos += 1; total += 1; id2lin[hid] = i\n",
     "                    nuevos.append(H); l.vivos += 1; total += 1; id2lin[hid] = i\n"
     "                    if _co is not None: _co.nace(H, b)   # P2: la hija nace pegada a la madre (si pega)\n"),
    ("        d['carro'] = car\n        out.append(d)\n",
     "        d['carro'] = car\n"
     "        if _co is not None: d['_carrera']['colonia'] = _co.salida(i)\n"
     "        out.append(d)\n"),
    ("    return dict(linajes=out, pizarra_log=piz_log,\n",
     "    _ret = dict(linajes=out, pizarra_log=piz_log,\n"),
    ("                           rng_mundo_estado=P._estado(rng)))\n",
     "                           rng_mundo_estado=P._estado(rng)))\n"
     "    if _co is not None: _ret['pista']['colonia'] = _co.info()\n"
     "    return _ret\n"),
]
_RUN = [None]


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def h16s(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


class Colonia:
    """Grupos de cuerpos pegados (reglas LOCALES: madre-hija, cabeza-miembro) y el cuello. Los cuerpos se identifican por su id (unico
    entre vivos: '<linaje>/<k>'); el fundador limpio lleva el id del linaje y nunca esta en un grupo hasta que pare."""

    def __init__(self, seed, n, pega, cuello, p_suelto, solo_sueltos=0):
        self.pega = int(bool(pega)); self.cuello = int(cuello); self.p_suelto = float(p_suelto); self.solo_sueltos = int(bool(solo_sueltos))
        if self.cuello < 0 or not 0 <= self.p_suelto <= 1: raise SystemExit("MUNDO_COLONIA: cuello >= 0 y p_suelto en [0, 1]")
        self.rng = np.random.default_rng([int(seed), 0, ETQ_CUELLO, 0]) if self.cuello else None
        self.gid = {}          # id del cuerpo -> id de grupo
        self.grupos = {}       # id de grupo -> [ids de cuerpos, el primero es la cabeza]
        self.cuerpo = {}       # id del cuerpo -> objeto Cuerpo (solo los que estan en un grupo)
        self.n_grupos = 0
        z = lambda: [0] * n
        self.m_cuello = z(); self.m_cuello_grupo = z(); self.fundados = z(); self.tam_max = z()
        self.tam_suma = z(); self.tam_n = z(); self.pasos_pegado = z(); self.cuellos = 0; self.candidatos = 0

    def k_de(self, b):
        g = self.gid.get(b.id)
        return len(self.grupos[g]) if g is not None else 1

    def nace(self, H, b):
        if not self.pega: return
        g = self.gid.get(b.id)
        if g is None:
            self.n_grupos += 1; g = self.n_grupos; self.grupos[g] = [b.id]; self.gid[b.id] = g; self.cuerpo[b.id] = b
            self.fundados[b.lin] += 1
        self.grupos[g].append(H.id); self.gid[H.id] = g; self.cuerpo[H.id] = H
        self.tam_max[b.lin] = max(self.tam_max[b.lin], len(self.grupos[g]))

    def muere(self, b):
        g = self.gid.pop(b.id, None)
        if g is None: return
        self.cuerpo.pop(b.id, None)
        m = self.grupos[g]; m.remove(b.id)
        if not m: del self.grupos[g]          # si queda uno solo, sigue siendo un grupo de 1 = suelto para el cuello

    def junta(self, cuerpos):
        """Al final de la fase A: cada miembro vuelve a la celda de su cabeza (el grupo se mueve como uno)."""
        for g, m in self.grupos.items():
            cab = self.cuerpo[m[0]]
            for cid in m[1:]:
                self.cuerpo[cid].pos = cab.pos
        for b in cuerpos:
            if b.id in self.gid and len(self.grupos[self.gid[b.id]]) > 1: self.pasos_pegado[b.lin] += 1

    def sedimenta(self, cuerpos, t):
        """El cuello: cada cuerpo muere con probabilidad p_suelto / k (k = tamano de su grupo). Sorteo por cuerpo en el orden de la lista."""
        self.cuellos += 1
        for b in cuerpos:
            if not b.vivo: continue
            self.candidatos += 1
            k = self.k_de(b)
            p = (self.p_suelto if k == 1 else 0.0) if self.solo_sueltos else self.p_suelto / k   # reapertura: solo_sueltos
            if self.rng.random() < p:
                b.E = 0.0; self.m_cuello[b.lin] += 1
                if k > 1: self.m_cuello_grupo[b.lin] += 1

    def muestra(self, cuerpos):
        for b in cuerpos:
            self.tam_suma[b.lin] += self.k_de(b); self.tam_n[b.lin] += 1

    def salida(self, i):
        return dict(muertes_cuello=self.m_cuello[i], muertes_cuello_pegado=self.m_cuello_grupo[i], grupos_fundados=self.fundados[i],
                    tam_max=self.tam_max[i], tam_medio=(round(self.tam_suma[i] / self.tam_n[i], 3) if self.tam_n[i] else None),
                    pasos_pegado=self.pasos_pegado[i])

    def info(self):
        return dict(pega=self.pega, cuello=self.cuello, p_suelto=self.p_suelto, solo_sueltos=self.solo_sueltos, cuellos=self.cuellos, candidatos=self.candidatos,
                    muertes_cuello=sum(self.m_cuello), grupos_vivos=len(self.grupos),
                    tam_grupos_vivos=sorted((len(m) for m in self.grupos.values()), reverse=True)[:20])


def construye():
    """-> (run, info). Aborta si un sha o un ancla no calzan."""
    if _RUN[0] is not None: return _RUN[0]
    rp = os.path.join(GEN_D, 'motor_convive.py'); sp = h16(rp)
    if sp != SHA_MOTOR: raise SystemExit(f"MUNDO_COLONIA: motor_convive.py sha {sp} != fijado {SHA_MOTOR}")
    if os.path.abspath(MC.__file__) != os.path.abspath(rp): raise SystemExit(f"MUNDO_COLONIA: 'motor_convive' importado de {MC.__file__}")
    txt = open(rp, encoding='utf-8').read()
    a = txt.index("def run_solapadas(seed, carros,"); b = txt.index("\n    return dict(linajes=out, pizarra_log=piz_log,")
    c = txt.index("\n\n", b) if "\n\n" in txt[b:] else len(txt)
    src = txt[a:c] + "\n"
    for viejo, nuevo in ANCLAS:
        k = src.count(viejo)
        if k != 1: raise SystemExit(f"MUNDO_COLONIA: el ancla aparece {k} veces (debe ser 1): {viejo[:70]!r}")
        src = src.replace(viejo, nuevo)
    ns = dict(vars(MC)); ns.update(Colonia=Colonia, P_SUELTO=P_SUELTO)
    exec(compile(src, '<mundo_colonia.run desde motor_convive.py>', 'exec'), ns)
    _RUN[0] = (ns['run_solapadas'], dict(sha_motor=sp, sha_fuente_transformada=h16s(src), anclas=len(ANCLAS)))
    return _RUN[0]


def run(*a, **k):
    return construye()[0](*a, **k)


if __name__ == '__main__':
    print(construye()[1])
