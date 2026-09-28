"""lee_posthoc.py — LECTURA POST-HOC (NO preregistrada; no entra en la letra) del bloque TERMO_EVO. Auditoría H-6 del 28-sep.

MISION: llegar a la AGI por este camino.
Definición (tomada DESPUÉS de ver la serie): linaje ESTABLECIDO = fund_post10k == 0 (la misma cantidad del juez que usa cruza_real).
Por brazo con gen (evo, ancho) y por linaje: R0 real, y media de g de los padres que parieron en la última ventana [0.9 T, T).
Sesgo de supervivencia declarado: "establecido" selecciona por construcción los linajes que ya iban bien; por eso se imprime también el
g de los NO establecidos y el de todos juntos, y las cifras NO se usan como puerta.
Uso: python experimentos/organelos/termo_evo/lee_posthoc.py <carpeta de datos de la serie o de la larga>
"""
import glob, json, os, statistics as st, sys


def med(xs): return round(st.median(xs), 4) if xs else None


def main(carpeta):
    for b in ('evo', 'ancho', 'sinher'):
        fs = sorted(glob.glob(os.path.join(carpeta, f'{b}_s*.json')))
        if not fs: continue
        E = dict(r0=[], g=[], n=0); N = dict(r0=[], g=[], n=0); gtodos = []
        for f in fs:
            x = json.load(open(f, encoding='utf-8')); T = x['pista']['T']; tel = x['tel_evo']['tel']
            for i, l in enumerate(x['linajes']):
                pp = [g for t, g in tel[str(i)]['partos'] if t >= T - T // 10]
                D = E if l['fund_post10k'] == 0 else N
                D['n'] += 1; D['r0'].append(l['R0_real'])
                if pp: D['g'].append(st.mean(pp)); gtodos.append(st.mean(pp))
        print(f"{b} ({len(fs)} corridas): ESTABLECIDOS {E['n']} linajes · R0 real mediana {med(E['r0'])} · g padres ult. ventana mediana "
              f"{med(E['g'])} (n {len(E['g'])}) || NO establecidos {N['n']} · R0 {med(N['r0'])} · g {med(N['g'])} (n {len(N['g'])}) "
              f"|| todos los linajes con partos: g mediana {med(gtodos)} (n {len(gtodos)})")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
