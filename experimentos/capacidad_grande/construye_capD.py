"""Genera experimentos/capacidad_grande/organismo_capD.py = organismo_caph11.py (a34d3309221cc6c7) con la RETINA
de tamano variable (D pixeles, deducido de los patrones). Anclas con conteo exacto.

Cinco anclas, todas del mismo tipo: donde el codigo escribia el literal 6 (dimension de la retina) o 9 (entradas de
las patas = 6 + 3 senales de rumbo/contacto), ahora escribe D y D+3, con D=len(primer patron). Con patrones de 6
pixeles, TODAS las llamadas al RNG conservan forma y orden, asi que capD(D=6) es organismo_caph11 exacto (control G0).
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'v11_evo_division', 'organismo_caph11.py')
SHA_ORIGEN = 'a34d3309221cc6c7'


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:50]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN: sha {h16(ORIGEN)}, se esperaba {SHA_ORIGEN}. Abortado.")
    s = open(ORIGEN, encoding='utf-8').read()
    s = sust(s, "    pats=PAT if pats is None else pats\n",
             "    pats=PAT if pats is None else pats\n"
             "    D=len(next(iter(pats.values())))   # capD: tamano de la retina (6 = organismo_caph11 exacto)\n",
             etiqueta='D de la retina')
    s = sust(s, "Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True",
             "Wl=rng.uniform(.1,.4,(2,D+3)); KW=np.zeros((NKMAX,D)); activa=np.zeros(NKMAX,bool); KW[:NK]=rng.uniform(0,1,(NK,D)); activa[:NK]=True",
             etiqueta='estado inicial')
    s = sust(s, "    while not cond(): KW[0:NK]=rng.uniform(0,1,(NK,6))\n",
             "    while not cond(): KW[0:NK]=rng.uniform(0,1,(NK,D))\n", etiqueta='sorteo de codigos')
    s = sust(s, "mu=np.zeros((NKMAX,6)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(9)",
             "mu=np.zeros((NKMAX,D)); splits=0; el=np.zeros_like(Wl); tr=np.zeros(D+3)", etiqueta='mu y traza')
    cab = ('"""organismo_capD = organismo_caph11.py (a34d3309221cc6c7) con la retina de tamano variable (D pixeles).\n'
           'Generado por construye_capD.py. NO editar. Con patrones de 6 pixeles es organismo_caph11 exacto (control G0).\n'
           'Hereda de caph11 los interruptores mu_norm (v10) y div_signo (v11); ambos False = caph9 = v9."""\n')
    d = os.path.join(AQUI, 'organismo_capD.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):50s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
