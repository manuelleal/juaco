"""construye_eco_org.py — CONSTRUYE POR ANCLAS el instrumento de ECO v2, ÓRGANOS COMO GENES (nube, 24-sep-2026). No se edita a mano.

MISION: llegar a la AGI por este camino.

Orígenes (SOLO se LEEN; sha fijado):
  experimentos/juaco_eco/motor_eco.py            bca3033878b59622 -> motor_eco2.py
  experimentos/juaco_eco/carros/FAMB_RES0_ECO.py  94ea78589bc2ce24 -> carros/FAMB_ORG_ECO.py
motor_eco2 = motor_eco + DOS GENES DE ÓRGANO al final del genoma (los 18 de antes no cambian de sitio):
  'ensena'  : el padre pasa su tabla en el parto (el órgano de subida_n10b / FAMB_RES);
  'filtra0' : el hijo descarta las entradas neutras (R == 0) de la tabla recibida (el filtro de subida_n10c).
  Cada órgano es un rasgo con UMBRAL (modelo de umbral de la genética cuantitativa): un número que muta como los demás (log-normal,
  sigma 0.15, rango [G0/4, 4 G0]) y el órgano se EXPRESA si el número es >= UMBRAL_ORG = 1.0. G0 = 0.9: todos nacen APAGADOS; una
  mutación lo prende con p ~ 0.24 (P(z > ln(1/0.9)/0.15)). Las 8 sombras lo llevan y derivan igual: el control de la deriva no cambia.
  Sin eco (eco=None) el ctx no trae los genes y el carro los toma apagados.
FAMB_ORG_ECO = FAMB_RES0_ECO con los dos órganos leídos del genoma del CUERPO (ctx['fabrica']['kw']):
  al_parir: sin 'ensena' expresado devuelve None (como FABRICA); con él, la tabla (como FAMB_RES).
  nace:     con 'filtra0' expresado (el del HIJO) quita las neutras; si no, instala la tabla completa.
Con los dos órganos apagados es FABRICA_ECO en toda la física; con los dos prendidos, FAMB_RES0_ECO (arnés identidad_eco_org.py).
Uso: python experimentos/juaco_eco/construye_eco_org.py [--verifica]
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
import construye_eco as CE

ORIG_MOTOR = os.path.join(AQUI, 'motor_eco.py'); SHA_MOTOR = 'bca3033878b59622'
ORIG_CARRO = os.path.join(AQUI, 'carros', 'FAMB_RES0_ECO.py'); SHA_CARRO = '94ea78589bc2ce24'
DEST_MOTOR = os.path.join(AQUI, 'motor_eco2.py')
DEST_CARRO = os.path.join(AQUI, 'carros', 'FAMB_ORG_ECO.py')

GENES_ULT = "         ('dote', 'dote', 0, 0.15, 1.2), ('rep_umbral', 'rep_umbral', 0, 0.5, 1.45), ('rep_X', 'rep_X', 1, 100, 2000))\n"
ANCLAS_MOTOR = [
    ('"""motor_eco.py', '"""motor_eco2.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco_org.py desde motor_eco.py, sha '
                        f'{SHA_MOTOR}; NO editar a mano). ECO v2: + los genes de organo ensena y filtra0 al final del genoma\n'
                        '(rasgos con umbral: se expresan si valen >= UMBRAL_ORG). Lo que sigue es el docstring del origen.\n\nmotor_eco.py'),
    (GENES_ULT,
     "         ('dote', 'dote', 0, 0.15, 1.2), ('rep_umbral', 'rep_umbral', 0, 0.5, 1.45), ('rep_X', 'rep_X', 1, 100, 2000),\n"
     "         ('ensena', 'kw', 0, 0.05, 10.0), ('filtra0', 'kw', 0, 0.05, 10.0))   # ECO v2: ORGANOS COMO GENES (umbral UMBRAL_ORG)\n"
     "ORG_G0 = {'ensena': 0.9, 'filtra0': 0.9}   # ECO v2: los organos nacen APAGADOS (0.9 < UMBRAL_ORG)\n"
     "UMBRAL_ORG = 1.0\n"),
    ("        v.append(float(CF['NK'] if dest == 'NK' else kw[nom]))\n",
     "        v.append(float(CF['NK'] if dest == 'NK' else (kw[nom] if nom in kw else ORG_G0[nom])))   # ECO v2: organos fuera del ctx de fabrica\n"),
]

ANCLAS_CARRO = [
    ('"""carros/FAMB_RES0_ECO.py', '"""carros/FAMB_ORG_ECO.py (CONSTRUIDO por experimentos/juaco_eco/construye_eco_org.py desde '
                                   f'carros/FAMB_RES0_ECO.py, sha {SHA_CARRO}; NO editar a mano).\nECO v2: los organos ensena (el padre pasa '
                                   'la tabla) y filtra0 (el hijo quita lo neutro) se leen del genoma del cuerpo (umbral 1.0). Lo que sigue\n'
                                   'es el docstring del origen.\n\ncarros/FAMB_RES0_ECO.py'),
    ("        self.ALMA_MUERTES = kw['alma_muertes']; self.MOTIVO = kw['alma_motivo']; self.KW0 = kw\n",
     "        self.ALMA_MUERTES = kw['alma_muertes']; self.MOTIVO = kw['alma_motivo']; self.KW0 = kw\n"
     "        self.ENSENA = float(kw.get('ensena', 0.9)) >= 1.0; self.FILTRA0 = float(kw.get('filtra0', 0.9)) >= 1.0   # ECO v2: ORGANOS\n"),
    ("        if MODO == 'nada': return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)\n",
     "        if MODO == 'nada' or not self.ENSENA: return None   # ECO v2: sin el organo 'ensena', el hijo no se lleva nada (FABRICA)\n"),
    ("        if SIN0 and _mem:   # ECO v1.2 = subida_n10c RES_SIN0: sin lo neutro, ANTES de todo lo demas\n",
     "        if self.FILTRA0 and _mem:   # ECO v2: el organo 'filtra0' DEL HIJO decide si quita lo neutro (subida_n10c)\n"),
]


def textos():
    if CE.h16(ORIG_MOTOR) != SHA_MOTOR: raise SystemExit(f"CONSTRUYE: motor_eco.py cambio ({CE.h16(ORIG_MOTOR)})")
    if CE.h16(ORIG_CARRO) != SHA_CARRO: raise SystemExit(f"CONSTRUYE: FAMB_RES0_ECO.py cambio ({CE.h16(ORIG_CARRO)})")
    m = CE.aplica(open(ORIG_MOTOR, encoding='utf-8').read(), ANCLAS_MOTOR, 'motor_eco2')
    c = CE.aplica(open(ORIG_CARRO, encoding='utf-8').read(), ANCLAS_CARRO, 'FAMB_ORG_ECO')
    return {DEST_MOTOR: m, DEST_CARRO: c}


if __name__ == '__main__':
    arts = textos()
    if '--verifica' in sys.argv[1:]:
        ok = all(os.path.exists(p) and open(p, encoding='utf-8').read() == s for p, s in arts.items())
        print('VERIFICA', 'OK' if ok else 'FALLA'); sys.exit(0 if ok else 1)
    if set(sys.argv[1:]) - {'--verifica'}: raise SystemExit(f"CONSTRUYE: banderas desconocidas {sys.argv[1:]}")
    for p, s in arts.items():
        with open(p, 'w', encoding='utf-8', newline='\n') as f: f.write(s)
        print(os.path.relpath(p, RAIZ), CE.h16s(s))
