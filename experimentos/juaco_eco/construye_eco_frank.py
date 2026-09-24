"""construye_eco_frank.py — CONSTRUYE POR ANCLAS el instrumento de ECO v3: LOS ÓRGANOS DEL FRANKENSTEIN COMO GENES (nube, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Origenes (SOLO se LEEN; sha fijado):
  experimentos/juaco_eco/motor_eco.py                       bca3033878b59622 -> motor_eco3.py
  experimentos/frankenstein/organismo_frankenstein.py       baff124177d44e90 (lo IMPORTA el carro; no se copia ni se edita)
motor_eco3 = motor_eco + SIETE GENES DE ORGANO al final del genoma (los 18 de antes no cambian de sitio): las 7 perillas del
Frankenstein del PC (b5, mapa, curiosidad, modelo, lenta, herencia, interruptor). Rasgos con UMBRAL, como en ECO v2: se expresan si el
numero es >= UMBRAL_ORG = 1.0; G0 = 0.9 (todos APAGADOS: el cuerpo nace FABRICA); una mutacion prende uno con p ~ 0.24.
carros/FRANK_ECO.py = el Frankenstein con sus perillas LEIDAS DEL GENOMA DEL CUERPO (ctx['fabrica']['kw'], el mismo camino que las
perillas de fabrica). Con todo apagado es FABRICA bit a bit (arnes del Frankenstein, A1); arnes nuevo: identidad_eco_frank.py.
Uso: python experimentos/juaco_eco/construye_eco_frank.py [--verifica]
"""
import os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
import construye_eco as CE

ORIG_MOTOR = os.path.join(AQUI, 'motor_eco.py'); SHA_MOTOR = 'bca3033878b59622'
ORIG_FRANK = os.path.join(RAIZ, 'experimentos', 'frankenstein', 'organismo_frankenstein.py'); SHA_FRANK = 'baff124177d44e90'
DEST_MOTOR = os.path.join(AQUI, 'motor_eco3.py')
DEST_CARRO = os.path.join(AQUI, 'carros', 'FRANK_ECO.py')
ORGANOS = ('b5', 'mapa', 'curiosidad', 'modelo', 'lenta', 'herencia', 'interruptor')

GENES_ULT = "         ('dote', 'dote', 0, 0.15, 1.2), ('rep_umbral', 'rep_umbral', 0, 0.5, 1.45), ('rep_X', 'rep_X', 1, 100, 2000))\n"
ANCLAS_MOTOR = [
    ('"""motor_eco.py', '"""motor_eco3.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco_frank.py desde motor_eco.py, sha '
                        f'{SHA_MOTOR}; NO editar a mano). ECO v3: + los 7 genes de organo del Frankenstein al final del genoma\n'
                        '(rasgos con umbral: se expresan si valen >= UMBRAL_ORG). Lo que sigue es el docstring del origen.\n\nmotor_eco.py'),
    (GENES_ULT,
     "         ('dote', 'dote', 0, 0.15, 1.2), ('rep_umbral', 'rep_umbral', 0, 0.5, 1.45), ('rep_X', 'rep_X', 1, 100, 2000),\n"
     "         " + ", ".join(f"('{g}', 'kw', 0, 0.05, 10.0)" for g in ORGANOS[:4]) + ",\n"
     "         " + ", ".join(f"('{g}', 'kw', 0, 0.05, 10.0)" for g in ORGANOS[4:]) + ")   # ECO v3: ORGANOS DEL FRANKENSTEIN COMO GENES\n"
     f"ORG_G0 = {{{', '.join(repr(g) + ': 0.9' for g in ORGANOS)}}}   # ECO v3: los organos nacen APAGADOS (0.9 < UMBRAL_ORG)\n"
     "UMBRAL_ORG = 1.0\n"),
    ("        v.append(float(CF['NK'] if dest == 'NK' else kw[nom]))\n",
     "        v.append(float(CF['NK'] if dest == 'NK' else (kw[nom] if nom in kw else ORG_G0[nom])))   # ECO v3: organos fuera del ctx de fabrica\n"),
]

CARRO = f'''"""carros/FRANK_ECO.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco_frank.py; NO editar a mano). ECO v3, nube, 24-sep-2026.

El Frankenstein del PC (experimentos/frankenstein/organismo_frankenstein.py, sha {SHA_FRANK}; se IMPORTA sin tocarlo) con sus 7 perillas
leidas del GENOMA del cuerpo: la perilla k vale 1 si ctx['fabrica']['kw'][k] >= 1.0 (el gen de organo de motor_eco3; sin genoma, 0.9:
apagada). Con todo apagado es FABRICA bit a bit (arnes del Frankenstein, A1). En la pista v2 cada cuerpo es una instancia nueva: lo que
el Frankenstein guarda "del linaje" en el carro (la opcion TD del modelo, Wc de la memoria lenta) vale aqui solo durante una vida; la
herencia (la tabla del padre en el parto) si cruza entre cuerpos.
"""
import hashlib, os, sys

_D = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'frankenstein')
if _D not in sys.path: sys.path.insert(0, _D)
import organismo_frankenstein as OF

SHA_FRANK = '{SHA_FRANK}'
if hashlib.sha256(open(OF.__file__, 'rb').read()).hexdigest()[:16] != SHA_FRANK:
    raise SystemExit(f"FRANK_ECO: organismo_frankenstein.py cambio (sha distinto de {{SHA_FRANK}})")
UMBRAL = 1.0
ORGANOS = {ORGANOS!r}
if tuple(OF.PERILLAS) != ORGANOS: raise SystemExit(f"FRANK_ECO: las perillas del Frankenstein cambiaron: {{OF.PERILLAS}}")


def perillas_de(kw):
    return dict((k, int(float(kw.get(k, 0.9)) >= UMBRAL)) for k in ORGANOS)


def crea(ctx):
    return OF.Carro(ctx, perillas_de(ctx['fabrica']['kw']))
'''


def textos():
    if CE.h16(ORIG_MOTOR) != SHA_MOTOR: raise SystemExit(f"CONSTRUYE: motor_eco.py cambio ({CE.h16(ORIG_MOTOR)})")
    if CE.h16(ORIG_FRANK) != SHA_FRANK: raise SystemExit(f"CONSTRUYE: organismo_frankenstein.py cambio ({CE.h16(ORIG_FRANK)})")
    m = CE.aplica(open(ORIG_MOTOR, encoding='utf-8').read(), ANCLAS_MOTOR, 'motor_eco3')
    return {DEST_MOTOR: m, DEST_CARRO: CARRO}


if __name__ == '__main__':
    arts = textos()
    if '--verifica' in sys.argv[1:]:
        ok = all(os.path.exists(p) and open(p, encoding='utf-8').read() == s for p, s in arts.items())
        print('VERIFICA', 'OK' if ok else 'FALLA'); sys.exit(0 if ok else 1)
    if set(sys.argv[1:]) - {'--verifica'}: raise SystemExit(f"CONSTRUYE: banderas desconocidas {sys.argv[1:]}")
    for p, s in arts.items():
        with open(p, 'w', encoding='utf-8', newline='\n') as f: f.write(s)
        print(os.path.relpath(p, RAIZ), CE.h16s(s))
