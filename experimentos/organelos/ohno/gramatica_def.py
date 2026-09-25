"""gramatica_def.py — LA GRAMATICA DEL ORGANO DE TRANSMISION (equipo organelos, Opus A, 24-sep-2026). Codigo NUEVO (no es copia).

MISION: llegar a la AGI por este camino.

Un organo de transmision es una TUPLA DE SLOTS (0..TOPE_SLOTS). Cada slot es una tupla de 5 enteros:
  (cuando, que, quien, como, origen)
  cuando : 0 nunca (silencioso: el slot existe y no se expresa) | 1 al nacer (en el parto) | 2 en vida (cada PER_VIDA pasos de edad)
           | 3 al morir
  que    : 0 todo | 1 solo lo de signo negativo (veneno/sal) | 2 solo lo de signo positivo | 3 sin lo neutro (magnitud > 0; = filtra0)
           | 4 solo lo reciente (las ultimas NODO_K mordidas VIVIDAS; nada heredado)
  quien  : 0 hijo | 1 hermano (del emisor: mismo linaje y mismo padre) | 2 vecino (el cuerpo vivo mas cercano en el anillo, cualquier linaje)
  como   : 0 copiar | 1 promediar (con lo que el receptor ya cree: (R + v_lenta)/2) | 2 invertir (-R)
           | 3 olvidar (el receptor descarta lo recibido que contradice lo que el VIVIO)
  origen : 0 linea original | 1 nacio por DUPLICACION (se hereda; NO se expresa; sirve para leer la palanca 2)
Con 'hijo' y 'nacer' el paquete viaja por al_parir/nace (el camino de FAMB_ORG_ECO); los demas los entrega el motor.
El como lo aplica el RECEPTOR (promediar y olvidar dependen de su estado), pero es un gen del EMISOR (viaja en el paquete).

'magnitud alta' (pedido) se CONTRAE en este mundo: con R en {+1, -3, 0} un umbral entre 0 y 1 es 'sin0' (= filtra0) y uno entre 1 y 3 es
'neg'. Queda 'sin0'. 'olvidar' se implementa, pero el arnes por pieza decide si entra al alfabeto de la serie (ver PREREGISTRO §2).

MUTACION = ERRORES DE COPIA, en cada parto (y en cada fundador del vivero que sale del banco), con un rng propio (etiquetas nuevas):
  (1) duplicacion con p_dup: un slot al azar se copia en tandem (justo despues del original), la copia con origen = 1 (si hay < tope);
  (2) borrado con p_del: un slot al azar desaparece (puede quedar el organo vacio: estado absorbente, declarado);
  (3) por slot y por campo, con p_campo: el campo pasa a OTRO valor del alfabeto, al azar.
Consumo de numeros FIJO por llamada (3 + 4*tope uniformes + 2 + 4*tope uniformes), haya o no mutacion.
"""
import numpy as np

CUANDO = ('nunca', 'nacer', 'vida', 'morir')
QUE = ('todo', 'neg', 'pos', 'sin0', 'reciente')
QUIEN = ('hijo', 'hermano', 'vecino')
COMO = ('copiar', 'promediar', 'invertir', 'olvidar')
CAMPOS = (CUANDO, QUE, QUIEN, COMO)
NOMBRE_CAMPO = ('cuando', 'que', 'quien', 'como')
PER_VIDA = 500          # 'en vida' = cada 500 pasos de edad (= rep_X de fabrica, el reloj natural del mundo); declarado, no ajustado
TOPE_SLOTS = 4
ALFABETO_TODO = tuple(tuple(range(len(c))) for c in CAMPOS)

ENSENA = ((1, 0, 0, 0, 0),)          # el disenado de ECO v2/v2.1: al nacer, todo, al hijo, copiar
FILTRA0 = ((1, 3, 0, 0, 0),)         # ensena + filtra0 del hijo: al nacer, sin lo neutro, al hijo, copiar
NULO = ()                            # no transmite
DISENADOS = dict(nulo=NULO, ensena=ENSENA, filtra0=FILTRA0)


def valida(gr, tope=TOPE_SLOTS):
    gr = tuple(tuple(int(v) for v in s) for s in gr)
    if len(gr) > tope: raise SystemExit(f"GRAMATICA: {len(gr)} slots > tope {tope}")
    for s in gr:
        if len(s) != 5: raise SystemExit(f"GRAMATICA: slot {s} no tiene 5 campos")
        for f in range(4):
            if not 0 <= s[f] < len(CAMPOS[f]): raise SystemExit(f"GRAMATICA: slot {s} fuera de rango en {NOMBRE_CAMPO[f]}")
        if s[4] not in (0, 1): raise SystemExit(f"GRAMATICA: origen {s[4]} (0 o 1)")
    return gr


def activos(gr):
    """Los slots que se EXPRESAN (cuando != nunca), sin la marca de origen."""
    return tuple(s[:4] for s in gr if s[0] != 0)


def texto(gr):
    a = [s for s in gr]
    if not a: return '[]'
    return '[' + ' + '.join(f"{CUANDO[s[0]]}/{QUE[s[1]]}/{QUIEN[s[2]]}/{COMO[s[3]]}{'*' if len(s) > 4 and s[4] else ''}" for s in a) + ']'


def muta_gram(gr, r, p_campo, p_dup, p_del, tope, alfabeto):
    """Errores de copia. Devuelve (gramatica nueva, numero de errores). Consumo fijo de numeros del rng r."""
    u = r.random(3 + 4 * tope); w = r.random(2 + 4 * tope)
    g = list(gr); nm = 0
    if u[0] < p_dup and 0 < len(g) < tope:
        i = int(w[0] * len(g)); s = g[i]; g.insert(i + 1, (s[0], s[1], s[2], s[3], 1)); nm += 1
    if u[1] < p_del and len(g) > 0:
        i = int(w[1] * len(g)); del g[i]; nm += 1
    for si in range(min(len(g), tope)):
        s = list(g[si])
        for f in range(4):
            if u[3 + 4 * si + f] < p_campo:
                ops = [x for x in alfabeto[f] if x != s[f]]
                if ops: s[f] = ops[int(w[2 + 4 * si + f] * len(ops))]; nm += 1
        g[si] = tuple(s)
    return tuple(g), nm


def fundadores_silenciosos(seed, n, alfabeto):
    """Un slot SILENCIOSO por fundador (cuando = nunca) con que/quien/como al azar del alfabeto (rng [seed, i, 22, 0]): variacion
    criptica sin sesgo hacia los disenados."""
    out = []
    for i in range(n):
        r = np.random.default_rng([seed, i, 22, 0]); x = r.random(3)
        q = alfabeto[1][int(x[0] * len(alfabeto[1]))]; a = alfabeto[2][int(x[1] * len(alfabeto[2]))]; c = alfabeto[3][int(x[2] * len(alfabeto[3]))]
        out.append(((0, q, a, c, 0),))
    return out


def un_slot_todos(alfabeto, sin_nunca=True):
    """Todas las gramaticas de UN slot del alfabeto (la fuerza bruta), en orden fijo."""
    out = []
    for c in alfabeto[0]:
        if sin_nunca and c == 0: continue
        for q in alfabeto[1]:
            for a in alfabeto[2]:
                for m in alfabeto[3]:
                    out.append(((c, q, a, m, 0),))
    return out
