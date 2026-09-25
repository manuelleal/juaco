"""construye_anf.py — CONSTRUYE POR ANCLAS el motor del paquete CONTROL DEL ANFITRION (organelos, Opus B, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Origen (SOLO se LEE; sha fijado): experimentos/organelos/darwin/motor_endo.py  7e10329cf0cb9fd0  -> anfitrion/motor_anf.py
motor_anf = motor_endo + 4 cambios:
  A1 importa control_anfitrion como SIM (reexporta simbiontes y define Ecologia con el control; con brazos de hoy es simbiontes.Ecologia);
  A2 los carros de darwin (FABRICA_SIMB) se buscan en darwin/carros;
  A3 Cuerpo gana la ranura ctl (los dos genes de control del anfitrion; None fuera de los brazos del paquete);
  A4 gancho siembra(cuerpos) justo despues de banco_ini (simbiontes sembrados y control inicial de los fundadores).
Uso: python experimentos/organelos/anfitrion/construye_anf.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
ORIG = os.path.join(os.path.dirname(AQUI), 'darwin', 'motor_endo.py'); SHA = '7e10329cf0cb9fd0'
DEST = os.path.join(AQUI, 'motor_anf.py')


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def h16s(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


def aplica(txt, anclas):
    for i, (a, b) in enumerate(anclas):
        n = txt.count(a)
        if n != 1: raise SystemExit(f"CONSTRUYE motor_anf: ancla {i} aparece {n} veces: {a[:70]!r}")
        txt = txt.replace(a, b)
    return txt


ANCLAS = [
    ('"""motor_endo.py (CONSTRUIDO',
     '"""motor_anf.py (CONSTRUIDO por experimentos/organelos/anfitrion/construye_anf.py desde darwin/motor_endo.py, sha ' + SHA +
     '; NO editar a mano).\nCONTROL DEL ANFITRION: SIM = control_anfitrion; ranura ctl; gancho siembra. Lo que sigue es el docstring del origen.\n\n'
     'motor_endo.py (CONSTRUIDO'),
    ("import simbiontes as SIM   # ENDO G3\n",
     "import control_anfitrion as SIM   # ANF A1 (reexporta simbiontes; Ecologia con el control del anfitrion)\n"),
    ("CARROS_ECO = os.path.join(AQUI, 'carros')\n",
     "CARROS_ECO = os.path.join(os.path.dirname(AQUI), 'darwin', 'carros')   # ANF A2: FABRICA_SIMB\n"),
    ("'sm', 'sm_nac', 'sm0')   # ENDO G2", "'sm', 'sm_nac', 'sm0', 'ctl')   # ENDO G2 + ANF A3"),
    ("self.sm0 = None   # ENDO G2", "self.sm0 = None; self.ctl = None   # ENDO G2 + ANF A3"),
    ("    if SB is not None: SB.banco_ini(len(ES['banco']))   # ENDO G4: banco de simbiontes alineado con el de genomas\n",
     "    if SB is not None: SB.banco_ini(len(ES['banco']))   # ENDO G4: banco de simbiontes alineado con el de genomas\n"
     "    if SB is not None: SB.siembra(cuerpos)   # ANF A4: simbiontes sembrados y control inicial (no hace nada con los brazos de hoy)\n"),
]


def texto():
    if h16(ORIG) != SHA: raise SystemExit(f"CONSTRUYE: motor_endo.py cambio ({h16(ORIG)})")
    return aplica(open(ORIG, encoding='utf-8').read(), ANCLAS)


if __name__ == '__main__':
    s = texto()
    if '--verifica' in sys.argv[1:]:
        ok = os.path.exists(DEST) and open(DEST, encoding='utf-8').read() == s
        print('VERIFICA', 'OK' if ok else 'FALLA'); sys.exit(0 if ok else 1)
    if set(sys.argv[1:]) - {'--verifica'}: raise SystemExit(f"CONSTRUYE: banderas desconocidas {sys.argv[1:]}")
    with open(DEST, 'w', encoding='utf-8', newline='\n') as f: f.write(s)
    print(os.path.relpath(DEST, RAIZ), h16s(s))
