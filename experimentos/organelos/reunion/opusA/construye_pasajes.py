"""construye_pasajes.py — construye POR ANCLAS nucleo_pasajes.py desde experimentos/organelos/eco_sel_ing/nucleo_eco_sel_ing.py (sha fijado).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como. Principio del director: que la evolucion construya el organo, solo con seleccion.

PASAJES SERIADOS en ECO (reunion 28-sep, Opus A; EXPLORATORIO). El nucleo es el de ECO_SEL_ING (hijo ingenuo, vivero permanente) con
UNA sola puerta nueva: trabajo() acepta un 8.o argumento opcional `genoma` (90 x 18) que se pasa a motor_eco como eco['genoma'] (los
genomas de los 90 fundadores; el banco arranca con ellos: E9 del motor). Sin ese argumento (o None) todo es == nucleo_eco_sel_ing.
Anclas (cada una exacta UNA vez):
  A1 cabecera del docstring.
  A2 trabajo(): desempaca args[:7] y `genoma` = args[7] si existe.
  A3 la llamada a eco_de(...) pasa genoma=genoma (None = el default de motor_eco.ECO_DEF: identico).
  A5 RAIZ: la copia vive en reunion/opusA/ (un nivel mas abajo que eco_sel_ing/).
  A4 al final: la genetica CEREBRO_M (los 15 del cerebro + rep_umbral) y los brazos PAS_* (carro FABRICA_ECO, vivero permanente).
Uso: python construye_pasajes.py | python construye_pasajes.py --verifica
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'organelos', 'eco_sel_ing', 'nucleo_eco_sel_ing.py')
SHA_ORIGEN = 'c2189f9d22b72386'
DESTINO = os.path.join(AQUI, 'nucleo_pasajes.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


A1_OLD = '"""nucleo_eco_sel_ing.py (CONSTRUIDO por experimentos/organelos/eco_sel_ing/construye_eco_sel_ing.py desde'
A1_NEW = ('"""nucleo_pasajes.py (CONSTRUIDO por experimentos/organelos/reunion/opusA/construye_pasajes.py desde experimentos/organelos/'
          'eco_sel_ing/\nnucleo_eco_sel_ing.py, sha c2189f9d22b72386; NO editar a mano). PASAJES SERIADOS: + argumento `genoma` en trabajo() y '
          'brazos PAS_*.\nLo que sigue es el docstring del origen.\n\n'
          'nucleo_eco_sel_ing.py (CONSTRUIDO por experimentos/organelos/eco_sel_ing/construye_eco_sel_ing.py desde')

A2_OLD = "    seed, brazo, T, t_corte, T_lect, carpeta, reanuda = args\n"
A2_NEW = ("    seed, brazo, T, t_corte, T_lect, carpeta, reanuda = args[:7]\n"
          "    genoma = args[7] if len(args) > 7 else None   # PASAJES: los genomas de los fundadores (None = G0, como el origen)\n")

A3_OLD = "eco=eco_de(gen_brazo, t_corte, ckpt_cada=SERIE['ckpt_cada'],"
A3_NEW = "eco=eco_de(gen_brazo, t_corte, genoma=genoma, ckpt_cada=SERIE['ckpt_cada'],"

A4_ADD = '''

# ================================================================================ PASAJES (anadido por construye_pasajes.py)
# CEREBRO_M = los 15 genes del cerebro + rep_umbral (el margen). Brazos de los pasajes: todos con el hijo INGENUO (FABRICA_ECO) y el
# vivero permanente de ECO_SEL_ING; lo que cambia entre pasajes lo pone el runner (corre_pasajes.py) con el argumento `genoma`.
GENETICAS['CEREBRO_M'] = dict(mutables=tuple(CR.BRAZOS['CEREBRO']['mutables']) + ('rep_umbral',), donante='padre', p=True)
BRAZOS.update({'PAS_SEL': ('CEREBRO', FAB, None), 'PAS_RES': ('CEREBRO', FAB, None), 'PAS_AZA': ('CEREBRO_AZAR', FAB, None),
               'PAS_SELM': ('CEREBRO_M', FAB, None), 'PAS_F1': ('MUT0', FAB, None)})
PAS = ('PAS_SEL', 'PAS_RES', 'PAS_AZA', 'PAS_SELM', 'PAS_F1')
'''

A5_OLD = "RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))\n"
A5_NEW = "RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))   # PASAJES: la copia vive un nivel mas abajo\n"

ANCLAS = [('A1', A1_OLD, A1_NEW), ('A2', A2_OLD, A2_NEW), ('A3', A3_OLD, A3_NEW), ('A5', A5_OLD, A5_NEW)]


def construye():
    sh = h16(ORIGEN)
    if sh != SHA_ORIGEN: raise SystemExit(f"construye_pasajes: {ORIGEN} tiene sha {sh}, se esperaba {SHA_ORIGEN}")
    txt = open(ORIGEN, encoding='utf-8', newline='').read()
    for nom, old, new in ANCLAS:
        n = txt.count(old)
        if n != 1: raise SystemExit(f"construye_pasajes: el ancla {nom} aparece {n} veces (se espera 1)")
        txt = txt.replace(old, new)
    return txt.rstrip('\n') + '\n' + A4_ADD


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    txt = construye()
    if '--verifica' in argv:
        ok = os.path.exists(DESTINO) and open(DESTINO, encoding='utf-8', newline='').read() == txt
        print(f"construye_pasajes --verifica: {'IGUAL' if ok else 'DISTINTO'} (origen {SHA_ORIGEN}; destino "
              f"{h16(DESTINO) if os.path.exists(DESTINO) else None})")
        return ok
    with open(DESTINO, 'w', encoding='utf-8', newline='') as f: f.write(txt)
    print(f"escrito {DESTINO} (sha {h16(DESTINO)}) desde {ORIGEN} ({SHA_ORIGEN}); anclas {[a[0] for a in ANCLAS]} + A4")
    return True


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
