"""codigo_def.py — EL CODIGO GENETICO v0 del bicho: LA CINTA, EL LECTOR y EL COPIADOR (Opus, equipo organelos, 24-sep-2026). Codigo NUEVO.

MISION: llegar a la AGI por este camino.

Idea (von Neumann 1966, desde la REPLICA y no desde la biologia): una sola descripcion, la CINTA, se usa DOS veces.
  1. el LECTOR (el "ribosoma", desarrolla()) la INTERPRETA al nacer y construye el fenotipo: las 18 perillas del cerebro/historia de
     vida del mundo ECO y el organo de transmision de la gramatica (gramatica_def.py);
  2. el COPIADOR (copia()) la COPIA sin interpretarla en el parto, con errores. Pero el copiador tambien LEE la cinta: las
     instrucciones TASA y SOS de la propia cinta dicen cuanto error poner en cada tramo y cuando subirlo (SOS: si el padre venia
     mordiendo cosas malas). Asi la cinta describe al constructor Y al copiador.

ALFABETO (una instruccion = tupla (OP, args...); 9 operaciones):
  SUM j d     perilla j (0..17) += d * PASO_LOG (d en -3..3; en espacio log, relativo a G0)             [efecto DIRECTO, 1 rasgo]
  EJE k d     eje k (0..2) += d * PASO_LOG sobre VARIOS rasgos con signo (EJES)                          [PLEIOTROPIA: 1 instruccion, 4 rasgos]
  ORG c q w m agrega un slot (cuando, que, quien, como, origen 0) al organo de transmision (tope 4)      [construye ESTRUCTURA]
  REP n       repite n veces (1..3) el bloque hasta su FIN                                              [repeticion]
  DEF m       define la subrutina m (0..2) hasta su FIN (no se ejecuta en linea; la ULTIMA definicion gana)
  LLAMA m     ejecuta la subrutina m (gen MAESTRO: cambiar el DEF cambia todas sus llamadas)
  FIN         cierra el REP/DEF abierto mas interno (un FIN suelto se ignora; un bloque sin FIN cierra al final)
  TASA r      desde aqui (en orden LINEAL de la cinta) la tasa de error por instruccion y por copia es TASAS[r] (r 0..4)
  SOS u f     regla de estres: si la fraccion de mordidas MALAS (dS < 0) entre las ultimas 20 del PADRE es >= U_SOS[u], toda la copia
              usa la tasa x F_SOS[f]. Vale la PRIMERA SOS de la cinta. (lee lo vivido: estado presente del padre, fisica del mundo)
TASA y SOS no tocan el fenotipo; SUM/EJE/ORG/REP/DEF/LLAMA/FIN no tocan la copia (salvo por su posicion en las zonas).

ERRORES DE COPIA (copia()): por instruccion i, con prob p_i = min(TASAS[zona(i)] * (F_SOS si SOS activa), P_MAX):
  cambio 0.55 (0.3: la instruccion entera se reemplaza por una al azar; 0.7: UN argumento cambia: d en +-1, categoricos a otro valor),
  borrado 0.20, insercion de una instruccion al azar despues 0.15, duplicacion en TANDEM de un tramo de 1..4 instrucciones 0.10.
  Tope de largo 200 (lo que pase se corta). rng propio por parto [seed, linaje, 23, k]: no toca ningun rng del mundo.
"""
import math
import numpy as np

OPS = ('SUM', 'EJE', 'ORG', 'REP', 'DEF', 'LLAMA', 'FIN', 'TASA', 'SOS')
N_RASGOS = 18                     # GENES[0..17] de motor_gramatica (sin los pseudogenes ensena/filtra0)
PASO_LOG = 0.15                   # = sigma de la mutacion numerica de hoy
EJES = (  # (rasgo, signo); nombres por los GENES de motor_gramatica.py:88-94
    ((0, 1), (9, 1), (6, 1), (5, 1)),          # 0 'aprender': eta, eta_s, paso, ema
    ((2, 1), (4, 1), (3, -1), (8, 1)),         # 1 'cautela': alpha, aversion, -hambre_boca, memoria_rechazo
    ((15, 1), (16, 1), (17, 1), (1, 1)),       # 2 'vida lenta': dote, rep_umbral, rep_X, tau_e
)
TASAS = (0.0, 0.002, 0.01, 0.04, 0.1)
U_SOS = (0.1, 0.2, 0.3, 0.4, 0.5)
F_SOS = (1, 2, 3, 5)
P_MAX = 0.5
TASA_DEF = 1                      # zona antes de la primera TASA
TOPE_CINTA = 200
TOPE_PASOS = 2000                 # pasos del lector (seguridad)
PROF_MAX = 4                      # anidamiento de LLAMA
TOPE_ORG = 4
ALF_ORG = (4, 5, 3, 4)            # cuando, que, quien, como (con 'olvidar': el mundo CAMBIA)
P_TIPO = (0.55, 0.75, 0.90)       # cambio | borrado | insercion | duplicacion


def _args_rango(op):
    return {'SUM': ((0, N_RASGOS - 1), (-3, 3)), 'EJE': ((0, len(EJES) - 1), (-3, 3)),
            'ORG': tuple((0, a - 1) for a in ALF_ORG), 'REP': ((1, 3),), 'DEF': ((0, 2),), 'LLAMA': ((0, 2),), 'FIN': (),
            'TASA': ((0, len(TASAS) - 1),), 'SOS': ((0, len(U_SOS) - 1), (0, len(F_SOS) - 1))}[op]


NUMERICO = {('SUM', 1), ('EJE', 1)}   # argumentos que mutan en +-1 (los demas son categoricos)


def valida(cinta):
    c = []
    for ins in cinta:
        ins = tuple(ins)
        if not ins or ins[0] not in OPS: raise SystemExit(f"CODIGO: instruccion {ins}")
        rg = _args_rango(ins[0])
        if len(ins) - 1 != len(rg): raise SystemExit(f"CODIGO: aridad {ins}")
        for a, (lo, hi) in zip(ins[1:], rg):
            if not (isinstance(a, (int, np.integer)) and lo <= int(a) <= hi): raise SystemExit(f"CODIGO: argumento fuera de rango {ins}")
        c.append((ins[0],) + tuple(int(a) for a in ins[1:]))
    if len(c) > TOPE_CINTA: raise SystemExit("CODIGO: cinta mas larga que el tope")
    return tuple(c)


# ================================================================= EL LECTOR (desarrollo)
def _parsea(cinta):
    """Arbol: nodos ('i', ins) | ('rep', n, cuerpo) | ('def', m, cuerpo). FIN cierra el bloque abierto mas interno."""
    raiz = []; pila = [raiz]; abiertos = []
    for ins in cinta:
        op = ins[0]
        if op == 'REP' or op == 'DEF':
            nodo = ['rep' if op == 'REP' else 'def', ins[1], []]; pila[-1].append(nodo); pila.append(nodo[2]); abiertos.append(nodo)
        elif op == 'FIN':
            if abiertos: abiertos.pop(); pila.pop()
        else: pila[-1].append(('i', ins))
    return raiz


def _defs(arbol, out):
    for n in arbol:
        if n[0] == 'def': out[n[1]] = n[2]
        if n[0] in ('rep', 'def'): _defs(n[2], out)
    return out


def desarrolla(cinta, G0, lo, hi, enteros):
    """La cinta -> (g: los 20 valores de GENES de motor_gramatica, gram: tupla de slots). Con todo d = 0 y los ORG de filtra0, da
    EXACTAMENTE G0 (los rasgos con x == 0 no se tocan: bit a bit) y ((1, 3, 0, 0, 0),). Devuelve tambien la traza (conteos)."""
    arbol = _parsea(cinta); defs = _defs(arbol, {})
    x = [0.0] * N_RASGOS; gram = []; st = dict(pasos=0, llamadas=0, corte=0)

    def ejecuta(nodos, prof):
        for n in nodos:
            if st['pasos'] >= TOPE_PASOS: st['corte'] = 1; return
            st['pasos'] += 1
            if n[0] == 'def': continue
            if n[0] == 'rep':
                for _ in range(n[1]): ejecuta(n[2], prof)
                continue
            ins = n[1]; op = ins[0]
            if op == 'SUM':
                if ins[2]: x[ins[1]] += ins[2] * PASO_LOG
            elif op == 'EJE':
                if ins[2]:
                    for j, s in EJES[ins[1]]: x[j] += s * ins[2] * PASO_LOG
            elif op == 'ORG':
                if len(gram) < TOPE_ORG: gram.append((ins[1], ins[2], ins[3], ins[4], 0))
            elif op == 'LLAMA':
                if ins[1] in defs and prof < PROF_MAX: st['llamadas'] += 1; ejecuta(defs[ins[1]], prof + 1)
    ejecuta(arbol, 0)
    g = np.array(G0, float).copy()
    for j in range(N_RASGOS):
        if x[j] != 0.0:
            v = float(G0[j]) * math.exp(x[j])
            if enteros[j]: v = float(round(v))
            g[j] = min(max(v, float(lo[j])), float(hi[j]))
    return g, tuple(gram), st


# ================================================================= EL COPIADOR (lee TASA y SOS de la misma cinta)
def zonas(cinta):
    r = TASA_DEF; out = []
    for ins in cinta:
        if ins[0] == 'TASA': r = ins[1]   # la TASA empieza a regir en SU propia posicion
        out.append(TASAS[r])
    return out


def regla_sos(cinta):
    for ins in cinta:
        if ins[0] == 'SOS': return ins[1], ins[2]
    return None


def al_azar(r):
    op = OPS[int(r.random() * len(OPS))]
    return (op,) + tuple(lo + int(r.random() * (hi - lo + 1)) for lo, hi in _args_rango(op))


def cambia(ins, r):
    if r.random() < 0.3 or len(ins) == 1: return al_azar(r)
    rg = _args_rango(ins[0]); a = int(r.random() * len(rg)); lo, hi = rg[a]; v = ins[1 + a]
    if (ins[0], a) in NUMERICO:
        nv = v + (1 if r.random() < 0.5 else -1)
        if nv < lo or nv > hi: nv = v - (nv - v)
    else:
        ops = [z for z in range(lo, hi + 1) if z != v]
        nv = ops[int(r.random() * len(ops))] if ops else v
    l = list(ins); l[1 + a] = int(nv); return tuple(l)


def copia(cinta, r, frac_mal, sos_on=True, on=True):
    """Copia la cinta con errores. frac_mal = fraccion de mordidas malas del padre (None: fundador, sin SOS).
    Devuelve (cinta nueva, dict(n=errores, sos=0/1, tipos=[cambio, borrado, insercion, duplicacion]))."""
    st = dict(n=0, sos=0, tipos=[0, 0, 0, 0])
    if not on: return cinta, st
    rs = regla_sos(cinta); mult = 1
    if sos_on and rs is not None and frac_mal is not None and frac_mal >= U_SOS[rs[0]]:
        mult = F_SOS[rs[1]]; st['sos'] = 1
    ps = zonas(cinta); out = []
    for i, ins in enumerate(cinta):
        p = min(ps[i] * mult, P_MAX)
        if p > 0.0 and r.random() < p:
            st['n'] += 1; w = r.random()
            if w < P_TIPO[0]: out.append(cambia(ins, r)); st['tipos'][0] += 1
            elif w < P_TIPO[1]: st['tipos'][1] += 1
            elif w < P_TIPO[2]: out.append(ins); out.append(al_azar(r)); st['tipos'][2] += 1
            else:
                L = 1 + int(r.random() * 4); out.extend(cinta[i:i + L]); out.append(ins); st['tipos'][3] += 1   # tramo + (tramo)
        else: out.append(ins)
    return tuple(out[:TOPE_CINTA]), st


# ================================================================= EL COMPILADOR: desde lo MAS EVOLUCIONADO (FIJO:filtra0 en G0)
def compila(gram=((1, 3, 0, 0, 0),), sos=(2, 2), tasa_copiador=1, tasa_cuerpo=3):
    """La cinta inicial: el fenotipo FIJO:filtra0 con las perillas de fabrica (G0).
    Zona 1 (el COPIADOR, tasa baja): TASA, SOS. Zona 2 (el CUERPO, tasa de hoy ~1.1 errores por copia): un gen MAESTRO (DEF 0 con los
    tres ejes, llamado una vez), las 18 perillas SUM j 0 y el organo dentro de un REP 1 (duplicable como estructura)."""
    c = [('TASA', tasa_copiador)]
    if sos is not None: c.append(('SOS', sos[0], sos[1]))
    c += [('TASA', tasa_cuerpo), ('DEF', 0), ('EJE', 0, 0), ('EJE', 1, 0), ('EJE', 2, 0), ('FIN',), ('LLAMA', 0)]
    c += [('SUM', j, 0) for j in range(N_RASGOS)]
    c += [('REP', 1)] + [('ORG',) + tuple(s[:4]) for s in gram] + [('FIN',)]
    return valida(c)


def texto(cinta):
    return ' '.join(f"{i[0]}" + ('' if len(i) == 1 else '(' + ','.join(str(a) for a in i[1:]) + ')') for i in cinta)
