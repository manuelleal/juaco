"""3T — evalua los criterios PREREGISTRADOS sobre el CSV de corre_3T.py. No recalibra nada."""
import sys, os, csv, glob
import numpy as np
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))


def carga(path=None, tag='3T'):
    path = path or sorted(glob.glob(os.path.join(AQUI, f'{tag}_*.csv')))[-1]
    with open(path, encoding='utf-8') as fh:
        lin = [l for l in fh if not l.startswith('#')]
    F = list(csv.DictReader(lin))
    for f in F:
        for k, v in list(f.items()):
            if k == 'arm': continue
            if v in ('', 'None'): f[k] = None
            else:
                try: f[k] = float(v)
                except ValueError: pass
    return path, F


def m(F, c):
    v = [f[c] for f in F if f[c] is not None]
    return (float(np.median(v)), float(min(v)), float(max(v))) if v else (None,) * 3


def fmt(t, d=3):
    return 'NA' if t[0] is None else f"{t[0]:.{d}f} [{t[1]:.{d}f}, {t[2]:.{d}f}]"


def por(F, a): return [f for f in F if f['arm'] == a]


def main():
    path, F = carga()
    print(f"fuente: {os.path.basename(path)}  n={len(F)}\n")
    arms = ['C1', 'C1p', 'C2', 'C2b', 'C3', 'C3C']

    # ---- 0. control de instrumento: C2b debe reproducir C1 campo a campo ----
    print("== 0. CONTROL DE INSTRUMENTO: C2b vs C1 (deben ser identicos) ==")
    c1 = {f['seed']: f for f in por(F, 'C1')}; c2b = {f['seed']: f for f in por(F, 'C2b')}
    campos = [c for c in F[0] if c not in ('arm',)]
    dif = [(s, c) for s in c1 for c in campos if c1[s][c] != c2b[s][c]]
    print(f"  semillas comparadas: {len(c1)}   campos por semilla: {len(campos)}")
    print(f"  discrepancias: {len(dif)}" + ("  -> PASA (identidad exacta)" if not dif else f"  -> FALLA: {dif[:8]}"))

    # ---- 1. requisito de diseno 50/50 en ventana temprana ----
    print("\n== 1. REQUISITO DE DISENO: frecuencia ~50/50 en t<5000 (criterio: acc en [0.40,0.60]) ==")
    for a in arms:
        t = m(por(F, a), 'early_acc'); n = m(por(F, a), 'early_nbit')
        ok = 'OK' if t[0] is not None and 0.40 <= t[0] <= 0.60 else 'FUERA'
        print(f"  {a:4} acc_early {fmt(t)}  mordidas_early {n[0]:.0f}  -> {ok}")

    # ---- 2. tabla principal ----
    print("\n== 2. TABLA PRINCIPAL (mediana [min, max], 20 semillas) ==")
    filas = [('sep = W_AB - W_AA', 'sep', 3), ('W_AB', 'W_AB', 3), ('W_AA', 'W_AA', 3),
             ('Wp(A|A)', 'Wp_AA', 2), ('Wn(A|A)', 'Wn_AA', 2),
             ('solap_A final (3=ciego)', 'solap_A', 1), ('acc_q4', 'acc_q4', 3),
             ('base_q4', 'base_q4', 3), ('lift_q4  <-- PRIMARIA', 'lift_q4', 3),
             ('rho_s4 (peso temporal)', 'rho_s4', 3), ('rho_cod_s4', 'rho_cod_s4', 3),
             ('splits', 'splits', 0), ('celdas', 'celdas', 0), ('t_pool', 't_pool', 0),
             ('fracTemp_med division', 'fracTemp_med', 3),
             ('nAA_q4 (venenos)', 'nAA_q4', 0), ('nAB_q4 (comidas)', 'nAB_q4', 0),
             ('muertes', 'deaths', 0), ('Rtot', 'Rtot', 0)]
    anc = 24
    print(' ' * anc + ''.join(f"{a:>22}" for a in arms))
    for et, c, d in filas:
        print(f"{et:<{anc}}" + ''.join(f"{fmt(m(por(F, a), c), d):>22}" for a in arms))

    # ---- 3. criterios preregistrados ----
    print("\n== 3. CRITERIOS PREREGISTRADOS ==")
    def cnt(a, c, f): return sum(1 for x in por(F, a) if x[c] is not None and f(x[c]))

    print(" C1 (prediccion: NO lo resuelve)")
    print(f"   sep == 0 exacto en {cnt('C1','sep',lambda v: v==0)}/20        -> {'PASA' if cnt('C1','sep',lambda v: v==0)==20 else 'FALLA'}")
    print(f"   solap_A == 3 en {cnt('C1','solap_A',lambda v: v==3)}/20       -> {'PASA' if cnt('C1','solap_A',lambda v: v==3)==20 else 'FALLA'}")
    t = m(por(F, 'C1'), 'lift_q4')
    print(f"   mediana lift_q4 = {t[0]:.4f} < 0.05 -> {'PASA' if t[0] < 0.05 else 'FALLA'}; "
          f"semillas con lift_q4>0.10: {cnt('C1','lift_q4',lambda v: v>0.10)}/20 (criterio <=2) -> "
          f"{'PASA' if cnt('C1','lift_q4',lambda v: v>0.10)<=2 else 'FALLA'}")

    print(" C2 (prediccion: lo resuelve)")
    a, b = m(por(F, 'C2'), 'W_AB'), m(por(F, 'C2'), 'W_AA')
    print(f"   mediana W_AB={a[0]:.3f} >= 0.80 -> {'PASA' if a[0]>=0.80 else 'FALLA'}")
    print(f"   mediana W_AA={b[0]:.3f} <= -2.00 -> {'PASA' if b[0]<=-2.0 else 'FALLA'}")
    print(f"   sep>=2.8 en {cnt('C2','sep',lambda v: v>=2.8)}/20 (criterio >=18) -> {'PASA' if cnt('C2','sep',lambda v: v>=2.8)>=18 else 'FALLA'}")
    t = m(por(F, 'C2'), 'lift_q4')
    print(f"   mediana lift_q4={t[0]:.3f} >= 0.30 -> {'PASA' if t[0]>=0.30 else 'FALLA'}")
    q1 = m(por(F, 'C2'), 'nAA_q1')[0]; q4 = m(por(F, 'C2'), 'nAA_q4')[0]
    print(f"   venenos Q4/Q1 = {q4:.0f}/{q1:.0f} = {q4/q1:.2f} < 0.30 -> {'PASA' if q4/q1<0.30 else 'FALLA'}")

    print(" C3 — LA PREGUNTA (las 4 condiciones deben cumplirse para veredicto SI)")
    s = m(por(F, 'C3'), 'solap_A'); n1 = cnt('C3', 'solap_A', lambda v: v <= 1)
    c1_ok = s[0] <= 1 and n1 >= 15
    print(f"   (1) REPRESENTACION: mediana solap_A={s[0]:.1f} <=1 y {n1}/20 semillas <=1 (crit >=15) -> {'CUMPLE' if c1_ok else 'NO CUMPLE'}")
    sp = m(por(F, 'C3'), 'sep'); c2_ok = sp[0] >= 1.0
    print(f"   (2) VALOR: mediana sep={sp[0]:.3f} >= 1.0 -> {'CUMPLE' if c2_ok else 'NO CUMPLE'}")
    lf = m(por(F, 'C3'), 'lift_q4'); c3_ok = lf[0] >= 0.15
    print(f"   (3) CONDUCTA: mediana lift_q4={lf[0]:.4f} >= 0.15 -> {'CUMPLE' if c3_ok else 'NO CUMPLE'}")
    nc = cnt('C3C', 'solap_A', lambda v: v <= 1); c4_ok = nc <= 5
    print(f"   (4) NO-ARTEFACTO: control C3C con solap_A<=1 en {nc}/20 (crit <=5) -> {'CUMPLE' if c4_ok else 'NO CUMPLE'}")
    ver = c1_ok and c2_ok and c3_ok and c4_ok
    print(f"\n   >>> VEREDICTO PREREGISTRADO: {'SI' if ver else 'NO'} <<<")

    print("\n== 4. CONFUSORES PREREGISTRADOS (anticipados en el PREREGISTRO, no a posteriori) ==")
    for a in ('C1p', 'C3', 'C3C'):
        tp = m(por(F, a), 't_pool'); ce = m(por(F, a), 'celdas')
        print(f"   {a:4} pool agotado en {cnt(a,'t_pool',lambda v: v is not None)}/20 semillas, "
              f"t_pool {fmt(tp,0)}, celdas {fmt(ce,0)}")
    print(f"   Saturacion de canales: Wp(A|A) {fmt(m(por(F,'C3'),'Wp_AA'),2)} / Wn(A|A) {fmt(m(por(F,'C3'),'Wn_AA'),2)} en C3")
    print(f"                          Wp(A|A) {fmt(m(por(F,'C1'),'Wp_AA'),2)} / Wn(A|A) {fmt(m(por(F,'C1'),'Wn_AA'),2)} en C1")
    print(f"   fracTemp de la division: C3 {fmt(m(por(F,'C3'),'fracTemp_med'))} vs C3C {fmt(m(por(F,'C3C'),'fracTemp_med'))}"
          "   (si son iguales, la regla NO distingue canal informativo de ruido)")
    print(f"   solap_A: C3 {fmt(m(por(F,'C3'),'solap_A'),1)} vs C3C(ruido) {fmt(m(por(F,'C3C'),'solap_A'),1)}"
          "   (el control separa MAS que el real)")


if __name__ == '__main__':
    main()
