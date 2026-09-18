"""MUNDO MÍNIMO DECIDIBLE (ERR-32) — selección de patrones para N2 por predicción. Creador C, 18 sep 2026.

**No toca ningún instrumento.** El montaje entero es una elección distinta de `tipos_fijos`, así que
`mundo_social_pred.py` (fc306b8fcddabe15) se usa **sin cambiar una línea** y su identidad con `mundo_social_n3.py`
sigue siendo la misma. Es la corrección más barata posible de ERR-32.

EL PROBLEMA (ERR-32, derivado, no medido). En N3d las parejas se agrupan por `k[3:]` y la máscara del receptor es
`[0,0,0,1,1,1]`: **los dos miembros de una pareja tienen la MISMA retina para el receptor**, luego el mismo código de
Kenyon y el mismo `valor(kk)`. Ninguna regla local puede escribir una distinción en un código idéntico ⇒ el montaje
sólo puede medir OBEDIENCIA, nunca retención.

LA CORRECCIÓN, y lo que se conserva. El receptor sigue siendo **ciego por construcción al rasgo que decide**: la regla
es `px0` (comida si `px0 = 1`) y su máscara lo tapa. Lo que cambia es que ahora **cada objeto tiene una vista distinta
para el receptor**, así que existe un código donde escribir lo aprendido. La ceguera pasa de *"no puede representar el
objeto"* a *"no puede inferir la regla"*, que es la que hace falta para que el canal social tenga algo que aportar.

CONSTRUCCIÓN (4 parejas, 8 objetos, 4 comida / 4 veneno):
  - vista del receptor = el subconjunto de {3,4,5} activo. Hay 8 vistas y los 8 objetos usan **las 8, todas distintas**.
  - cada pareja es (comida, veneno) con vistas a **distancia de Hamming 1** en {3,4,5}: lo más confundibles que pueden
    ser **sin ser idénticas**. Emparejamiento sobre el cubo Q3: ∅–{3} · {3,4}–{4} · {3,5}–{5} · {4,5}–{3,4,5}.
  - vistas forzadas por el espacio (patrones de peso 3): ∅ sólo existe como `111000` (px0=1 ⇒ COMIDA) y {3,4,5} sólo
    como `000111` (px0=0 ⇒ VENENO). De ahí salen forzadas {3} = veneno y {4,5} = comida.
  - las dos parejas libres ({3,4}–{4} y {3,5}–{5}) reparten comida/veneno **al azar por semilla**, y cuando una vista
    va a comida se sortea cuál de sus dos patrones candidatos la realiza. RNG PROPIO (`seed + 810000`).
  ⇒ el mapa vista → valencia es **arbitrario por semilla**: el receptor no puede inferirlo, sólo memorizarlo objeto a
  objeto (mordiendo) o recibirlo del emisor (sin morder). Balanceado 4/4 por construcción.

PUERTAS DE VALIDEZ DE N3d QUE SE MANTIENEN: receptor ciego al rasgo que decide (`px0` bajo máscara) · acierto
BALANCEADO (4 comida / 4 veneno) · canal asimétrico (sólo el receptor escucha, `escucha=False` en el emisor) ·
`regen = 50` · las mismas máscaras MR/ME.
"""
import numpy as np

MR = [0, 0, 0, 1, 1, 1.]   # el receptor ve px 3,4,5
ME = [1, 1, 1, 0, 0, 0.]   # el emisor ve px 0,1,2 (donde está px0, el rasgo que decide)

# Emparejamiento sobre el cubo Q3 de las vistas del receptor; '' es la vista vacia.
PAREJAS_VISTA = [('', '3'), ('34', '4'), ('35', '5'), ('45', '345')]
FORZADAS = {'': 'comida', '345': 'veneno'}   # unicas realizaciones: 111000 (px0=1) y 000111 (px0=0)


def _vista(k):
    """La vista del receptor: que px de {3,4,5} estan activos, como cadena ordenada ('' , '3', '34', '345', ...)."""
    return ''.join(c for c in '345' if k[int(c)] == '1')


def parejas_vd(seed, pats, val):
    """Devuelve los 8 nombres de patron del montaje minimo decidible. `pats` y `val` vienen de split_regla(seed,'px0')."""
    r = np.random.default_rng(seed + 810000)
    por_vista = {}
    for k in pats:
        por_vista.setdefault(_vista(k), []).append(k)
    quiere = dict(FORZADAS)
    for a, b in PAREJAS_VISTA:                       # las dos parejas libres reparten comida/veneno al azar
        if a in quiere or b in quiere:
            continue
        if int(r.integers(2)):
            quiere[a], quiere[b] = 'comida', 'veneno'
        else:
            quiere[a], quiere[b] = 'veneno', 'comida'
    for a, b in PAREJAS_VISTA:                       # completa el lado forzado de cada pareja
        if a in quiere and b not in quiere:
            quiere[b] = 'veneno' if quiere[a] == 'comida' else 'comida'
        elif b in quiere and a not in quiere:
            quiere[a] = 'veneno' if quiere[b] == 'comida' else 'comida'
    tipos = []
    for v in sorted(quiere):
        cand = [k for k in sorted(por_vista[v]) if val[k] == quiere[v]]
        if not cand:
            raise SystemExit(f"montaje VD: la vista {v!r} no tiene candidato {quiere[v]} (semilla {seed}).")
        tipos.append(cand[int(r.integers(len(cand)))])
    return tipos


def comprueba(seed, pats, val, tipos):
    """Las cuatro puertas del montaje, comprobables sin correr el organismo."""
    vistas = [_vista(k) for k in tipos]
    n_com = sum(1 for k in tipos if val[k] == 'comida')
    g = dict(
        ocho_objetos=len(tipos) == 8,
        vistas_distintas=len(set(vistas)) == 8,                       # hay DONDE escribir: un codigo por objeto
        balanceado=n_com == 4,                                        # acierto balanceado valido
        parejas_hamming1=all(abs(len(a) - len(b)) == 1 and set(min(a, b, key=len)) <= set(max(a, b, key=len))
                             for a, b in PAREJAS_VISTA),              # confundibles pero distintos
        valencias_opuestas_por_pareja=all(
            val[tipos[sorted(set(vistas)).index(a)]] != val[tipos[sorted(set(vistas)).index(b)]]
            for a, b in PAREJAS_VISTA),
        ciego_al_rasgo=all(MR[0] == 0 for _ in [0]),                  # px0 (la regla) esta bajo mascara
    )
    return g
