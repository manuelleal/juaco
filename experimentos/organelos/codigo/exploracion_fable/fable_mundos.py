# EXPLORATORIO, no es dato
"""fable_mundos.py — CATALOGO DE MUNDOS QUE CAMBIAN para la exploracion del codigo genetico (Fable, equipo organelos, 24-sep-2026).

MISION: llegar a la AGI por este camino.

La idea (Lenski 2003, Avida): la complejidad aparece cuando el mundo premia PASOS INTERMEDIOS. El cambio de golpe (A<->B) no los tiene.
Aqui cada mundo es un dict `spec` que motor_fable.py lee en cada paso: efecto(spec, t, EF0, L) devuelve una funcion (letra, pos) -> (dE, dAg).
EF0 = tabla de fabrica {'A': (+0.8, 0), 'B': (-0.4, 0), 'C': (0, +0.8), 'D': (0, -0.4)}.

Tipos:
  golpe     t0: en t0 se intercambian X e Y (identico al cambio de corre_codigo; sirve de control del instrumento).
  gradual   t0, dur: el valor de X va LINEALMENTE del suyo al de Y (y al reves) en `dur` pasos. Hay pasos intermedios continuos.
  escalera  t0, dur, n: lo mismo pero en n peldanos discretos (cada dur/n pasos).
  alterna   t0, periodo: desde t0, X e Y se intercambian cada `periodo` pasos (estacional cuadrado). La memoria heredada se vuelve
            alternativamente util e inutil: aqui la SOS y la transmision podrian brillar o hundirse.
  onda      t0, periodo: estacional SUAVE (coseno): X va de su valor al de Y y vuelve, sin saltos.
  fijo      t0, tabla: en t0 la tabla pasa a ser `tabla` (letras no nombradas: fabrica). Sirve para 'suave' (A a neutro), 'bonanza'
            (B se vuelve comida sin que A cambie: una oportunidad nueva, sin perdida) y cualquier otra.
  zona      t0, frac: el intercambio X<->Y rige SOLO en las posiciones [0, frac*L) del anillo; el resto es el mundo viejo (parcial).
  deriva    t0, dur: como gradual, pero X termina en NEUTRO (0, 0) y Y sube solo a la mitad del valor de X: perdida parcial.
"""
import math

LETRAS = ('A', 'B', 'C', 'D')


def _lerp(a, b, f):
    return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f)


def _swap(EF0, X, Y):
    d = dict(EF0); d[X], d[Y] = EF0[Y], EF0[X]; return d


def valida(spec):
    if not isinstance(spec, dict) or 'tipo' not in spec or 't' not in spec: raise SystemExit('FABLE: spec = dict(tipo=..., t=...)')
    X, Y = spec.get('X', 'A'), spec.get('Y', 'B')
    if X not in LETRAS or Y not in LETRAS or X == Y: raise SystemExit('FABLE: X, Y letras distintas')
    if spec['tipo'] not in ('golpe', 'gradual', 'escalera', 'alterna', 'onda', 'fijo', 'zona', 'deriva', 'reina'): raise SystemExit(f"FABLE: tipo {spec['tipo']}")
    return spec


def tabla_en(spec, t, EF0):
    """La tabla letra -> (dE, dAg) vigente en t (sin zona). Es pura: no consume rng."""
    tipo = spec['tipo']; t0 = int(spec['t']); X = spec.get('X', 'A'); Y = spec.get('Y', 'B')
    if t < t0: return EF0
    if tipo in ('golpe', 'zona'): return _swap(EF0, X, Y)
    if tipo == 'gradual' or tipo == 'escalera':
        f = min(1.0, (t - t0) / float(spec['dur']))
        if tipo == 'escalera':
            n = int(spec['n']); f = math.floor(f * n + 1e-9) / n
        d = dict(EF0); d[X] = _lerp(EF0[X], EF0[Y], f); d[Y] = _lerp(EF0[Y], EF0[X], f); return d
    if tipo == 'deriva':
        f = min(1.0, (t - t0) / float(spec['dur']))
        d = dict(EF0); d[X] = _lerp(EF0[X], (0.0, 0.0), f); d[Y] = _lerp(EF0[Y], (EF0[X][0] * 0.5, EF0[X][1] * 0.5), f); return d
    if tipo == 'alterna':
        k = (t - t0) // int(spec['periodo'])
        return _swap(EF0, X, Y) if k % 2 == 0 else EF0
    if tipo == 'onda':
        f = (1.0 - math.cos(2.0 * math.pi * (t - t0) / float(spec['periodo']))) / 2.0
        d = dict(EF0); d[X] = _lerp(EF0[X], EF0[Y], f); d[Y] = _lerp(EF0[Y], EF0[X], f); return d
    if tipo == 'fijo':
        d = dict(EF0); d.update({k: tuple(v) for k, v in spec['tabla'].items()}); return d
    raise SystemExit(tipo)


def _reina(spec, t, EF0):
    """REINA ROJA (con estado, en la COPIA del spec de esta corrida): el veneno es un linaje que 'muta' hacia la comida cuando la poblacion
    aprendio a evitarlo. Cada `cada` pasos (desde t0, y al menos `gap` pasos despues del ultimo cambio) se mira la fraccion de mordidas
    al veneno actual entre las mordidas a A y B de esa ventana; si es < umbral, A y B se intercambian. La mordida se cuenta en el
    invocable que devuelve efecto() (se llama EXACTAMENTE una vez por mordida)."""
    # Version 2 (la 1 miraba la fraccion de mordidas al veneno; en la exploratoria de Opus la poblacion muerde B casi tanto como A
    # (0.46 antes, 0.48 despues del cambio), asi que esa senal no existe). Aqui el disparador es la RECUPERACION: el total de
    # mordidas por ventana `cada` (proxy fisico de cuanta poblacion sana hay) vuelve a >= umbral x la ventana de referencia (la
    # anterior a t0). El mundo castiga recuperarse: Reina Roja.
    st = spec.get('_st')
    if st is None: st = spec['_st'] = dict(swap=0, tc=-10 ** 9, n=0, ref=None, cambios=[], vent=[])
    t0 = int(spec['t']); cada = int(spec.get('cada', 1000)); gap = int(spec.get('gap', 2000)); u = float(spec.get('umbral', 0.8))
    if t > 0 and t % cada == 0:
        if t == t0: st['ref'] = st['n']; st['swap'] = 1; st['tc'] = t; st['cambios'].append(t)   # el primer cambio es el golpe en t0
        elif t > t0 and st['ref'] and t - st['tc'] >= gap and st['n'] >= u * st['ref']:
            st['swap'] ^= 1; st['tc'] = t; st['cambios'].append(t)
        if len(st['vent']) < 200: st['vent'].append([t, st['n']])
        st['n'] = 0
    tab = _swap(EF0, 'A', 'B') if st['swap'] else EF0
    def f(kk, pos):
        st['n'] += 1
        return tab[kk]
    return f


def efecto(spec, t, EF0, L):
    """(letra, pos) -> (dE, dAg) vigente en t."""
    if spec['tipo'] == 'reina': return _reina(spec, t, EF0)
    tab = tabla_en(spec, t, EF0)
    if spec['tipo'] == 'zona':
        lim = int(float(spec['frac']) * L)
        return lambda kk, pos: tab[kk] if pos < lim else EF0[kk]
    return lambda kk, pos: tab[kk]


# ------------------------------------------------------------------ el catalogo (t0 = t_cambio del TL; se fija en corre_fable)
def catalogo(t0):
    C = {}
    C['quieto'] = dict(tipo='fijo', t=t0, tabla={})   # CONTROL: el mundo NO cambia (linea de base CODIGO vs PERILLAS sin cambio)
    C['golpe'] = dict(tipo='golpe', t=t0)
    C['gradual8k'] = dict(tipo='gradual', t=t0, dur=8000)
    C['gradual16k'] = dict(tipo='gradual', t=t0, dur=16000)
    C['escalera4'] = dict(tipo='escalera', t=t0, dur=8000, n=4)
    C['alterna2k'] = dict(tipo='alterna', t=t0, periodo=2000)
    C['alterna4k'] = dict(tipo='alterna', t=t0, periodo=4000)
    C['alterna8k'] = dict(tipo='alterna', t=t0, periodo=8000)
    C['onda8k'] = dict(tipo='onda', t=t0, periodo=8000)
    C['onda16k'] = dict(tipo='onda', t=t0, periodo=16000)
    C['suave'] = dict(tipo='fijo', t=t0, tabla={'A': (0.0, 0.0), 'B': (0.4, 0.0)})          # A deja de alimentar, B alimenta a medias
    C['bonanza'] = dict(tipo='fijo', t=t0, tabla={'B': (0.8, 0.0)})                         # B se vuelve comida; A sigue siendo comida
    C['medio_veneno'] = dict(tipo='fijo', t=t0, tabla={'A': (-0.2, 0.0), 'B': (0.8, 0.0)})  # intercambio a medias: A pica poco
    C['zona_mitad'] = dict(tipo='zona', t=t0, frac=0.5)
    C['deriva8k'] = dict(tipo='deriva', t=t0, dur=8000)
    C['reina'] = dict(tipo='reina', t=t0, cada=1000, gap=2000, umbral=0.8)       # cuando las mordidas vuelven al 80 %, A<->B otra vez
    C['reina_lenta'] = dict(tipo='reina', t=t0, cada=1000, gap=6000, umbral=0.8)
    return C
