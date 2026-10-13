"""REGLA 14 (EQUIPO.md, ERR-38) para V4-CAL — los kwargs de cada brazo, CAMPO A CAMPO contra el montaje del tronco.
No corre ninguna simulacion. V4-CAL no copia baterias: importa corre_vivo_rep2.BRAZOS y mini_vivo.BRAZOS. Cada brazo
debe ser el montaje del tronco + EXACTAMENTE los campos declarados en PREREGISTRO_calibracion_v4.md §4:
  OFF       desambiguar=1, placebo=0                  (+ invertir_vivo_en = T/2 en T-C ii)
  TRONCO_B  IDENTICO a OFF campo a campo (lo unico distinto es la semilla, s + 100000)
  PLACEBO   OFF + placebo = 1
  PEOR      OFF + costo = costo_a = 0.001 x 1.5

    python experimentos/criterio_v4/regla14_v4.py
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_criterio_v4 as R
import corre_vivo_rep2 as CR2
import mini_vivo as MV

malo = 0


def compara(titulo, base, cand, declarados):
    global malo
    print(f"\n{titulo}  ({len(base)} campos del tronco)")
    for k in base:
        if k in declarados:
            print(f"  {k:16s} {str(base[k]):>10s} -> {str(cand.get(k)):>10s}   DECLARADO")
            continue
        ok = k in cand and cand[k] == base[k]
        malo += not ok
        print(f"  {k:16s} {str(base[k]):>10s}    {str(cand.get(k)):>10s}   {'SI' if ok else '*** NO ***'}")
    extra = {k: cand[k] for k in cand if k not in base}
    nd = set(extra) - set(declarados)
    print(f"  campos de mas: {extra if extra else 'ninguno'}")
    if nd:
        malo += len(nd); print(f"  *** NO DECLARADOS: {sorted(nd)}")


if __name__ == '__main__':
    T = R.T
    DEC = {'OFF': {'desambiguar', 'placebo'}, 'TRONCO_B': {'desambiguar', 'placebo'},
           'PLACEBO': {'desambiguar', 'placebo'}, 'PEOR': {'desambiguar', 'placebo', 'costo', 'costo_a'}}
    for b in R.BRAZOS_TA:
        for a in R.ARMS:
            compara(f"T-A {b} / {a}", dict(CR2.BRAZOS[b]), R.kw_vivo(b, a), DEC[a])
    for a in R.ARMS:
        compara(f"T-C (ii) / {a}", dict(MV.BRAZOS['VIVO']), R.kw_rev(a), DEC[a] | {'invertir_vivo_en'})
    for b in R.BRAZOS_TA:
        off = R.kw_vivo(b, 'OFF')
        tb = R.kw_vivo(b, 'TRONCO_B'); pl = R.kw_vivo(b, 'PLACEBO'); pe = R.kw_vivo(b, 'PEOR')
        c1 = tb == off
        c2 = {k for k in pl if pl[k] != off.get(k)} == {'placebo'} and pl['placebo'] == R.U.K_PLACEBO and off['placebo'] == 0
        c3 = ({k for k in pe if pe[k] != off.get(k)} == {'costo', 'costo_a'}
              and abs(pe['costo'] - R.C0 * R.M_PEOR) < 1e-12 and abs(pe['costo_a'] - R.C0 * R.M_PEOR) < 1e-12)
        c4 = R.semilla_real(2841, 'TRONCO_B') == 2841 + R.DESPL and R.semilla_real(2841, 'OFF') == 2841
        print(f"\n{b}: TRONCO_B == OFF campo a campo: {c1} | PLACEBO difiere solo en placebo=1: {c2} | "
              f"PEOR solo en costo/costo_a x{R.M_PEOR}: {c3} | semilla TRONCO_B = s+{R.DESPL}: {c4}")
        malo += (not c1) + (not c2) + (not c3) + (not c4)
    print(f"\nREGLA 14 v4: {'OK' if malo == 0 else '*** FALLA ***'}")
    sys.exit(0 if malo == 0 else 1)
