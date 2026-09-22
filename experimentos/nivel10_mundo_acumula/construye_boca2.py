"""Construye organismo_boca2.py POR ANCLAS desde mundo_fase10.py (84e97674f709a900). SONDA para el ESBOZO del candidato al tronco
"la boca lee las dos filas" (ESBOZO_PREREGISTRO_boca_dos_filas.md). NO es el candidato: el candidato se construye desde
organismo_vivo_rep2 + B-5 como dE5 (experimentos/tronco_v15_dE5/construye_v15_dE5.py), con su gemelo g para T-B.

MISION: llegar a la AGI por este camino. Una perilla, memoria nueva CERO, regla de aprendizaje nueva NINGUNA.

PERILLA boca2 (0 = apagada = mundo_fase10 BIT A BIT):
  boca2=1  VETO POR CUALQUIER NECESIDAD. Con dos necesidades y fuera de CUELLO_MIN, la boca decide con
           _wt(fila activa) + min(0, v(fila de la OTRA necesidad)): la fila activa conserva su atraccion; la otra solo puede
           VETAR. `_vnec` ya existia (solo lectura, mismo ruteo puerta/lenta que la boca). No consume rng.
  Con n_nec = 1 (examen v3', baterias del tronco) no hay otra fila: INERTE por construccion.
Uso: python construye_boca2.py
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(AQUI, 'mundo_fase10.py')
DESTINO = os.path.join(AQUI, 'organismo_boca2.py')
SHA_ORIGEN = '84e97674f709a900'


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


A_FIRMA = "cambia_cada=0,cambia_fam=4,f10=0):"
N_FIRMA = "cambia_cada=0,cambia_fam=4,f10=0,boca2=0):"
A_CUE = "            if _cue2: _wt=min(_wt,_vnec(1-_na,PAT[kk],kc))"
N_BOCA = ("            if boca2==1 and n_nec==2 and not _cue2: _wt=_wt+min(0.0,_vnec(1-_na,PAT[kk],kc))   # BOCA2 VETO: la OTRA necesidad solo puede vetar (lectura de su fila, sin memoria nueva, sin sorteos)\n")
A_EXT = "    if rep_acum: _ext.update(rep_acum=1)"
N_EXT = "    if boca2: _ext.update(boca2=int(boca2))   # BOCA2: clave nueva SOLO con la perilla encendida\n"


def main():
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != {SHA_ORIGEN}. Abortado.")
    t = open(ORIGEN, encoding='utf-8').read()
    for a in (A_FIRMA, A_CUE, A_EXT):
        if t.count(a) != 1:
            raise SystemExit(f"ANCLA {a[:60]!r}: {t.count(a)} apariciones. Abortado.")
    t = t.replace(A_FIRMA, N_FIRMA)
    i = t.index(A_CUE); j = t.index('\n', i) + 1
    t = t[:j] + N_BOCA + t[j:]
    i = t.index(A_EXT); j = t.index('\n', i) + 1
    t = t[:j] + N_EXT + t[j:]
    t = t.replace('"""mundo_fase10 = ', '"""organismo_boca2 = mundo_fase10 (84e97674f709a900) + perilla boca2 (construye_boca2.py). mundo_fase10 = ', 1)
    if 'rng.' in N_BOCA or 'rng.' in N_EXT or 'random' in N_BOCA:
        raise SystemExit('la insercion consume rng. Abortado.')
    compile(t, DESTINO, 'exec')
    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(t)
    print(f"ESCRITO {DESTINO} sha {h16(DESTINO)} desde mundo_fase10.py {SHA_ORIGEN}: 3 anclas (firma, boca, salida), 0 rng, compila OK")


if __name__ == '__main__':
    main()
