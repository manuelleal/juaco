"""ancla_1e6.py — ANCLA DE MAQUINA de F1 FRIO (SOLO el coordinador: 1e6 pasos pasa del limite de 200 000 de un creador).

MISION: llegar a la AGI por este camino.

Corre corre_frio.trabajo(RES0_60k) en la semilla 19701 a T = 1e6 (un proceso, ~1 min) y lo compara con el JSON GUARDADO de ECO v1.2
(juaco_eco/datos/eco_v12_serie_s19701-19720/MUT0_T_s19701.json, nube, gemelo motor_eco_rapido_fam) en TODAS las claves salvo brazo, seg
y motor. Si da IGUAL: el envoltorio, el motor copiado (con la guardia a 1e9, ERR-146) y ESTA maquina reproducen el MUT0_T de v1.2 a
longitud completa. No escribe en datos/ (usa un directorio temporal). Uso: python experimentos/organelos/frio/ancla_1e6.py
"""
import json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_frio as F


def main():
    ruta = os.path.join(F.ECO, 'datos', 'eco_v12_serie_s19701-19720', 'MUT0_T_s19701.json')
    x = json.load(open(ruta, encoding='utf-8'))
    F.usa_gemelo()
    t0 = time.time()
    y = F.trabajo((19701, 'RES0_60k', F.FRIO['T'], 60000, F.FRIO['T_lect'], tempfile.mkdtemp(prefix='frio_ancla_'), False))
    J = lambda v: json.dumps(v, sort_keys=True, default=str)
    dist = [k for k in x if k not in ('brazo', 'seg', 'motor') and J(x[k]) != J(y.get(k))]
    print(f"ANCLA 1e6 s19701: {'IGUAL' if not dist else 'DISTINTO'} · distintas {dist} · persiste {y['persiste']} · vivos_T {y['vivos_T']} "
          f"(guardado {x['vivos_T']}) · n_nac {y['n_nac']} · r0_nac {y['r0_nac']} · {time.time() - t0:.1f} s en esta maquina "
          f"(guardado {x['seg']} s en la nube)")
    return not dist


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
