"""construye_organo_cond.py — EXTRA POST HOC de la sonda (28-sep, escrito DESPUES de ver que el organo tal cual mata de hambre).
Diagnostico visto: en la pista el anillo es ~90 % B+D (tambien en termo y O1); morder veneno LIMPIA y es la via a la comida; el organo
de ECO (nunca muerdas B/D) deja al fundador sin comida (vida 600 = la dote). Pregunta post hoc (diseno NUESTRO, no evolucion; 3 semillas):
el mismo organo que SOLO actua con necesidad alta (hambre activa > ORG_NEC; saciado se limpia como en V143_TERMO), ¿ayuda al fundador?
ORGANO = 3. Con ORGANO = 0 es V143_TERMO_ORG0 (== V143_TERMO bit a bit, arnes) salvo lineas que no corren.
MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).
ORIGEN (solo se LEE): termo_organo/carros/V143_TERMO_ORG0.py (dda120a17ab10bb5).
"""
import hashlib, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, 'carros', 'V143_TERMO_ORG0.py'); SHA = 'dda120a17ab10bb5'; NL = '\r\n'
VARIANTES = [('V143_TERMO_ORGC0', 0), ('V143_TERMO_ORGCOND', 3)]


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


def construye(nombre, o):
    src = open(ORIGEN, 'rb').read()
    if h16b(src) != SHA: raise SystemExit('origen cambiado')
    txt = src.decode('utf-8')
    A = [('"""V143_TERMO_ORG0.py — organo:', '"""' + nombre + '.py — organo (CONDICIONADO, post hoc; construye_organo_cond.py):'),
         ('ORGANO = 0   # organo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143_TERMO bit a bit; 1 = pixel 1; 2 = DESFASADO pixel 0)' + NL,
          f'ORGANO = {o}   # organo: LA UNICA LINEA QUE CAMBIA ENTRE VARIANTES (0 = V143_TERMO bit a bit; 1 = pixel 1; 2 = DESFASADO pixel 0; 3 = CONDICIONADO)' + NL
          + 'ORG_NEC = 0.5   # post hoc: el organo (pixel 1) solo actua si la necesidad activa (hambre del carro) > ORG_NEC' + NL),
         ('        j = 1 if ORGANO == 1 else 0' + NL, '        j = 1 if ORGANO in (1, 3) else 0' + NL),
         ("        self._org['opp'][kk] += 1" + NL,
          "        self._org['opp'][kk] += 1" + NL + '        if ORGANO == 3 and not self._hambre > ORG_NEC: return 0.0   # post hoc: saciado, V143_TERMO' + NL)]
    for a, r in A:
        if txt.count(a) != 1: raise SystemExit(f'ancla {a[:60]!r} x{txt.count(a)}')
        txt = txt.replace(a, r)
    return txt.encode('utf-8')


if __name__ == '__main__':
    for n, o in VARIANTES:
        b = construye(n, o); ruta = os.path.join(AQUI, 'carros', n + '.py')
        with open(ruta, 'wb') as fh: fh.write(b)
        print(f'  escrito {n} sha {h16b(b)}')
