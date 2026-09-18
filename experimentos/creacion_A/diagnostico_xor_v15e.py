"""CREADOR A — diagnostico (NO es un modo nuevo, no cambia nada): por que v15e 'suma' da xor01 0.250 en la semilla 141 del humo.

Reproduce el punto de la sonda a priori del mundo de regla (T = 200 000, fase 2 en T/2) corriendo T = 100 000 con
`fase2_en = 99 999`: la fase de entrenamiento es identica (mismo flujo del rng), la sonda cae un paso antes, y el estado
final del run es el estado en la sonda. Para cada patron de TEST imprime: valencia, lectura total (la que puntua), lectura
lineal sola, residuo de la casilla ganadora, si la puerta lo declara familiar (alias de codigo) y el signo de cada parte.
Uso: python diagnostico_xor_v15e.py [semilla] [regla]      (un proceso; por defecto 141 xor01)
"""
import sys, os
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]
import organismo_v15ge as m

KW14 = dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)


def acc(W, test, vr, medio):
    f = [1.0 if W[k] > 0 else (medio if W[k] == 0 else 0.0) for k in test if vr[k] == 'comida']
    p = [1.0 if W[k] < 0 else (medio if W[k] == 0 else 0.0) for k in test if vr[k] == 'veneno']
    return 0.5 * float(np.mean(f)) + 0.5 * float(np.mean(p))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 141
    regla = sys.argv[2] if len(sys.argv) > 2 else 'xor01'
    pats, tren, test, vr = m.split_regla(seed, regla)
    for mem in ('suma', None):
        r = m.run(seed, T=100000, mundo='regla', regla=regla, fase2_en=99999, memoria_pares=mem, **KW14)
        W = r['W_apriori']; lin = r['W_lenta']; tab = r['W_tabla'] or {}; fam = r['mem_fam'] or {}
        print(f"\n=== semilla {seed} {regla} memoria={mem}: acc registro {acc(W, test, vr, 0.5):.3f} / estricta {acc(W, test, vr, 0.0):.3f}"
              f"  ganadora {r['mem_ganadora']}  cobertura {r['mem_cobertura']}  celdas {r['celdas']} splits {r['splits']}")
        print(f"  lineal Wps-Wns = {np.round(np.array(r['Wps']) - np.array(r['Wns']), 2).tolist()}")
        print(f"  {'patron':8s} {'val':7s} {'TOTAL':>7s} {'lineal':>7s} {'residuo':>8s}  familiar  ok?")
        for k in test:
            ok = (W[k] > 0) == (vr[k] == 'comida') and W[k] != 0
            print(f"  {k:8s} {vr[k]:7s} {W[k]:+7.2f} {lin[k]:+7.2f} {tab.get(k, float('nan')):+8.2f}  {str(fam.get(k)):8s}  {'si' if ok else 'NO'}   {'(TEST)'}")
        for k in tren:
            print(f"  {k:8s} {vr[k]:7s} {W[k]:+7.2f} {lin[k]:+7.2f} {tab.get(k, float('nan')):+8.2f}  {str(fam.get(k)):8s}        (train)")
        if mem is not None:
            print("  Lectura: en los TEST la casilla ganadora aporta el residuo que dejo el ULTIMO patron de entrenamiento con esa combinacion,")
            print("  y la lineal aporta su lectura del patron nuevo: si la lineal no puede con la regla, la diferencia entre las dos lineales")
            print("  (la del patron guardado y la del nuevo) es junk y cambia el signo.")
