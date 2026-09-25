"""humo_largo.py — HUMO DE COSTO a largo completo de la serie (T 120 000, corte 60 000), semilla de PRACTICA 21901, VIDA y FIJO:ensena,
UN proceso, 2 corridas. Sirve para medir segundos por corrida (costo de la serie) y para ver que el camino largo (checkpoints cada 10 000,
corte, banco final) escribe su JSON. Numeros de PRACTICA: no deciden nada. Opus A, 24-sep-2026.

MISION: llegar a la AGI por este camino.
"""
import os, sys, time
from collections import Counter
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_gramatica as CG, gramatica_def as GD


def main():
    ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(CG.DATOS, 'humo', f"gramatica_humo_largo_{ts}"); os.makedirs(carpeta, exist_ok=True)
    print(f"[{time.strftime('%H:%M:%S')}] HUMO LARGO (practica 21901) · {CG.SERIE} · shas {CG.SHAS()}", flush=True)
    for b in ('VIDA', 'FIJO:ensena'):
        x = CG.trabajo((21901, b, CG.SERIE['T'], CG.SERIE['t_corte'], CG.SERIE['r0_margen'], carpeta, False))
        ban = x.get('final_banco_gr') or []
        cc = Counter(GD.texto(GD.activos(CG._tup(g))) if GD.activos(CG._tup(g)) else '[silencioso]' for g in ban)
        cz = Counter(GD.texto(GD.activos(CG._tup(g))) if GD.activos(CG._tup(g)) else '[silencioso]' for g in ((x.get('corte_gr') or {}).get('banco_gr') or []))
        print(f"[{time.strftime('%H:%M:%S')}] {b}: {x['seg']} s · abortado {x['abortado']} · persiste {x.get('persiste')} (vivos {x.get('vivos_T')}, "
              f"max {x.get('max_vivos')}) · r0 {x.get('r0_post')} (n {x.get('n_coh_post')}) · errores {x.get('g_nmut')} · max_nac_linaje "
              f"{x.get('max_nac_linaje')}\n    banco en el corte (top 4): {cz.most_common(4)}\n    banco final (top 4): {cc.most_common(4)}", flush=True)
    print(f"HUMO LARGO: numeros de PRACTICA · {os.path.relpath(carpeta, CG.RAIZ)}")


if __name__ == '__main__':
    main()
