"""REGLA 14 (EQUIPO.md, ERR-38) — la entrada de cada brazo del runner, CAMPO A CAMPO contra la del TRONCO.
No corre ninguna simulacion: importa el runner y los montajes originales y compara los diccionarios.

Aqui NO hay bateria copiada (A-CAL no usa baterias: corre T-A y T-C ii, y los montajes se IMPORTAN sin copiar de
corre_vivo_rep2 y mini_vivo). Por eso la regla 14 se aplica a lo que si se copia: LOS KWARGS QUE EL RUNNER PASA.
Cada brazo del runner tiene que ser, campo a campo:
    kwargs del tronco (corre_vivo_rep2.BRAZOS[b] / mini_vivo.BRAZOS['VIVO'])
  + exactamente los campos DECLARADOS en PREREGISTRO_calibracion_v3.md (desambiguar, placebo, invertir_vivo_en,
    y para el brazo PEOR: costo y costo_a con el multiplicador declarado).

    python experimentos/criterio_v3/regla14_campo_a_campo.py
"""
import sys, os

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
NIV11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
sys.path[:0] = [ORG, NIV11, AQUI]

import corre_vivo_rep2 as CR2
import mini_vivo as MV
import corre_criterio_v3 as R
import umbrales_v3 as U

DECLARADOS_TA = {'desambiguar', 'placebo'}
DECLARADOS_TC = {'desambiguar', 'placebo', 'invertir_vivo_en'}
DECLARADOS_PEOR = {'costo', 'costo_a'}


def compara(titulo, base, cand, declarados, malo, overrides=frozenset()):
    """`overrides`: campos del tronco que el brazo cambia A PROPOSITO y que el preregistro declara (el coste de vida
    del brazo PEOR). Se imprimen como DECLARADO y se verifican aparte, con su factor."""
    print(f"\n{titulo}   ({len(base)} campos en el tronco)")
    print(f"  {'campo':16s} {'tronco':>12s} {'brazo':>14s}   igual")
    for k in base:
        ok = k in cand and cand[k] == base[k]
        if k in overrides:
            print(f"  {k:16s} {str(base[k]):>12s} {str(cand.get(k, '(FALTA)')):>14s}   DECLARADO (§4 del preregistro)")
            malo[0] += (k not in cand)
            continue
        malo[0] += (not ok)
        print(f"  {k:16s} {str(base[k]):>12s} {str(cand.get(k, '(FALTA)')):>14s}   {'SI' if ok else '*** NO ***'}")
    extra = {k: cand[k] for k in cand if k not in base}
    print(f"  campos de MAS: " + (', '.join(f'{k}={v}' for k, v in extra.items()) if extra else 'ninguno'))
    no_declarados = set(extra) - declarados
    if no_declarados:
        malo[0] += len(no_declarados); print(f"  *** campos de mas NO DECLARADOS: {sorted(no_declarados)}")
    faltan = [k for k in base if k not in cand]
    if faltan:
        malo[0] += len(faltan); print(f"  *** campos que FALTAN: {faltan}")
    return malo


if __name__ == '__main__':
    malo = [0]
    for b in R.BRAZOS_TA:
        base = dict(CR2.BRAZOS[b])
        for arm in R.ARMS:
            ov = DECLARADOS_PEOR if arm == 'PEOR' else set()
            compara(f"T-A brazo {b} / arm {arm}", base, R.kw_vivo(b, arm), DECLARADOS_TA | ov, malo, ov)
    base_rev = dict(MV.BRAZOS['VIVO'])
    for arm in R.ARMS:
        ov = DECLARADOS_PEOR if arm == 'PEOR' else set()
        compara(f"T-C (ii) / arm {arm}", base_rev, R.kw_rev(arm), DECLARADOS_TC | ov, malo, ov)

    # el brazo PEOR mueve EXACTAMENTE lo declarado y por el factor declarado
    m = U.PEOR['m']; c0 = U.PEOR['costo_base']
    peor = R.kw_vivo('VIVO', 'PEOR'); off = R.kw_vivo('VIVO', 'OFF')
    solo_costo = {k for k in peor if peor[k] != off.get(k)}
    ok_peor = (solo_costo == {'costo', 'costo_a'} and abs(peor['costo'] - c0 * m) < 1e-12
               and abs(peor['costo_a'] - c0 * m) < 1e-12)
    print(f"\nel brazo PEOR difiere de OFF SOLO en {sorted(solo_costo)} y por el factor declarado m = {m}: {ok_peor}")
    malo[0] += (not ok_peor)

    # el PLACEBO difiere de OFF SOLO en la perilla placebo
    pl = R.kw_vivo('VIVO', 'PLACEBO')
    solo_pl = {k for k in pl if pl[k] != off.get(k)}
    ok_pl = (solo_pl == {'placebo'} and pl['placebo'] == R.K_PLACEBO and off['placebo'] == 0)
    print(f"el brazo PLACEBO difiere de OFF SOLO en ['placebo'] y vale k = {R.K_PLACEBO}: {ok_pl}")
    malo[0] += (not ok_pl)

    print(f"\nREGLA 14: {'OK' if malo[0] == 0 else '*** FALLA ***'}")
    sys.exit(0 if malo[0] == 0 else 1)
