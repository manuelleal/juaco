"""
pilot_dimensionado.py - PILOTO DE INSTRUMENTO, no de hipotesis.
Solo para fijar T, fase2_en y comprobar que el mundo-regla es viable:
  - cuantas visitas recibe cada patron (potencia estadistica de la tasa por visita)
  - muertes (supervivencia)
  - si el valor de los patrones de ENTRENAMIENTO converge (la tarea es aprendible)
  - cuantos codigos se reparten las 30 celdas con 20 patrones
NO se mira ninguna metrica de los patrones de TEST. Declarado en el PREREGISTRO.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import organismo_3k as o3

if __name__ == "__main__":
    for T in (100000, 200000):
        for s in (1, 2, 3):
            r = o3.run(s, T=T, mundo='regla', kenyon_mode='fijo')
            tren, test = r['tren'], r['test']
            vt = {k: sum(r['vis'][k]) for k in tren}
            Wt = {k: r['W_final'][k] for k in tren}
            food = [k for k in tren if o3.valencia_regla(k) == 'comida']
            pois = [k for k in tren if o3.valencia_regla(k) == 'veneno']
            # uso de celdas: cuantos de los 20 patrones activan cada celda
            uso = np.zeros(30, int)
            for k in r['codes_fin']:
                uso[r['codes_fin'][k]] += 1
            print(f"T={T} s={s} muertes={r['deaths']:4d} "
                  f"visitas/patron_tren min={min(vt.values())} med={int(np.median(list(vt.values())))} max={max(vt.values())} "
                  f"| W_tren comida med={np.median([Wt[k] for k in food]):+.2f} "
                  f"veneno med={np.median([Wt[k] for k in pois]):+.2f} "
                  f"| celdas usadas={int((uso>0).sum())}/30 uso max={uso.max()}")
        print()
