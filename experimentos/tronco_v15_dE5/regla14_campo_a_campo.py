"""REGLA 14 (EQUIPO.md, ERR-38) — la entrada nueva de la bateria copiada, CAMPO A CAMPO contra la del tronco v14.2.
No corre ninguna simulacion: solo carga los dos modulos y compara los diccionarios de INSTRUMENTOS.

    python experimentos/tronco_v15_dE5/regla14_campo_a_campo.py
"""
import sys, os, importlib.util

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
sys.path[:0] = [ORG, AQUI]


def carga(nom, ruta):
    sp = importlib.util.spec_from_file_location(nom, ruta)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


if __name__ == '__main__':
    T = carga('bg142', os.path.join(ORG, 'bateria_generaliza_v142.py'))
    C = carga('bgde5', os.path.join(AQUI, 'bateria_generaliza_v15_dE5.py'))
    tr_inst, tr_kw = T.INSTRUMENTOS['organismo_v142']
    print(f"TRONCO   organismo_v142 -> {tr_inst}   ({len(tr_kw)} campos)")
    malo = 0
    for nom in ('organismo_v15_dE5_on', 'organismo_v15_dE5'):
        ci, ck = C.INSTRUMENTOS[nom]
        print(f"\nCANDIDATO {nom} -> {ci}")
        print(f"  {'campo':12s} {'tronco':>10s} {'candidato':>12s}   igual")
        for k in tr_kw:
            ok = k in ck and ck[k] == tr_kw[k]
            malo += (not ok)
            print(f"  {k:12s} {str(tr_kw[k]):>10s} {str(ck.get(k, '(FALTA)')):>12s}   {'SI' if ok else '*** NO ***'}")
        print("  campos de MAS (declarados en PREREGISTRO_dE5_v2.md §2): "
              + ', '.join(f'{k}={ck[k]}' for k in ck if k not in tr_kw))
        faltan = [k for k in tr_kw if k not in ck]
        print(f"  campos que FALTAN: {faltan if faltan else 'ninguno'}")
        malo += len(faltan)
    igual_tronco = C.INSTRUMENTOS['organismo_v142'] == T.INSTRUMENTOS['organismo_v142']
    igual_todas = all(C.INSTRUMENTOS[k] == T.INSTRUMENTOS[k] for k in T.INSTRUMENTOS)
    umbrales = open(os.path.join(AQUI, 'bateria_generaliza_v15_dE5.py'), encoding='utf-8').read().count(
        "V['G1_valor'] = mpx >= 0.65 and 0.35 <= maz <= 0.65 and par1 >= 0.7 * S") == 1
    print(f"\nla entrada del tronco en la COPIA es identica a la del original: {igual_tronco}")
    print(f"todas las entradas del original siguen intactas: {igual_todas}")
    print(f"umbrales G1/G2/K de la copia sin tocar: {umbrales}")
    print(f"\nREGLA 14: {'OK' if (malo == 0 and igual_tronco and igual_todas and umbrales) else '*** FALLA ***'}")
    sys.exit(0 if (malo == 0 and igual_tronco and igual_todas and umbrales) else 1)
