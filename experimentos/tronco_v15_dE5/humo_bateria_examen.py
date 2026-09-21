"""HUMO de `bateria_v15_dE5.py` SIN Pool y con <= 3 corridas (regla 3 de EQUIPO.md: un agente no abre `Pool`).

Por que no se corre la bateria entera: su criterio 5 hace 2 x 7 x 6 = 84 comparaciones = 168 corridas de T=100000
ANTES del examen, sin importar cuantas semillas se pidan. Eso excede el limite de un agente (6 corridas). Asi que
aqui se ejercita, en UN proceso, exactamente lo que ERR-42 y ERR-28 pueden romper en una bateria COPIADA:

  1. la bateria importa y apunta al modulo del CANDIDATO (no al del tronco), con la dosis encendida;
  2. `tarea_id` (criterio 5) corre y compara contra `organismo_v11` leido de organismo/ (ERR-28: rutas);
  3. `tarea` corre una etapa y devuelve las claves que el veredicto usa;
  4. la RUTA de salida del JSON existe y es ESCRIBIBLE en el sitio exacto donde la bateria lo escribira
     (se crea y se borra un archivo de prueba con el mismo prefijo y carpeta) — este es el fallo de ERR-42.

El humo COMPLETO de la bateria (el que llega a escribir `datos/examen_dE5_<sello>.json` de verdad) lo tiene que
correr el coordinador, porque abre Pool:   python bateria_v15_dE5.py 1 --desde 2001 --log
(o `--sin-pool` para hacerlo en un proceso: la bandera esta puesta, pero siguen siendo ~170 corridas).

    python experimentos/tronco_v15_dE5/humo_bateria_examen.py
"""
import sys, os, json, time, importlib.util

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]


def carga(nom, ruta):
    sp = importlib.util.spec_from_file_location(nom, ruta)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


if __name__ == '__main__':
    t0 = time.time()
    B = carga('bat_de5', os.path.join(AQUI, 'bateria_v15_dE5.py'))
    ok = []
    # 1) apunta al candidato y RAIZ es el bundle
    txt = open(os.path.join(AQUI, 'bateria_v15_dE5.py'), encoding='utf-8').read()
    ok.append(('apunta a organismo_v15_dE5_on (2 veces)', txt.count('import organismo_v15_dE5_on as v13') == 2))
    ok.append(('RAIZ es el bundle', os.path.basename(B.RAIZ) == 'bundle' and os.path.isdir(os.path.join(B.RAIZ, 'datos'))))
    ok.append(('las SEIS etapas y los umbrales v3\' intactos', B.SEIS == ['E1', 'E2', 'E2I', 'E2J', 'E2K', 'E2L'] and len(B.ETAPAS) == 9))
    import organismo_v15_dE5_on as ON
    import inspect
    fir = inspect.signature(ON.run).parameters
    ok.append(('la dosis esta ENCENDIDA por defecto en el modulo examinado',
               fir['eta_pred'].default == 0.03 and fir['k_sorp'].default == 5.0 and fir['desambiguar'].default == 1))
    # 2) criterio 5 (una comparacion: 2 corridas)
    r_id = B.tarea_id(('v11', 'E1', 1))
    ok.append(('criterio 5 corre y es IDENTICO en (v11, E1, s1)', bool(r_id['identico'])))
    print(f"  criterio 5 (v11, E1, s1): identico={r_id['identico']}  difieren={r_id.get('difieren')}")
    # 3) una corrida del examen (1 corrida)
    r = B.tarea(('E1', 2001))
    ok.append(('tarea() devuelve las claves del veredicto',
               all(k in r for k in ('etapa', 'seed', 'mord', 'vis', 'W', 'celdas', 'splits', 'deaths'))))
    print(f"  examen E1 s2001 (dosis ON): W={r['W']}  mord B={r['mord']['B']}  celdas={r['celdas']}  splits={r['splits']}  muertes={r['deaths']}")
    # 4) ERR-42: la ruta exacta del JSON existe y es escribible
    stamp = time.strftime('%Y%m%d_%H%M%S')
    prueba = os.path.join(B.RAIZ, 'datos', f'examen_dE5_PRUEBA_ESCRITURA_{stamp}.json')
    try:
        json.dump(dict(prueba=True), open(prueba, 'w', encoding='utf-8'))
        escribible = os.path.exists(prueba)
        os.remove(prueba)
    except Exception as e:
        escribible = False
        print(f"  *** no se puede escribir en {prueba}: {e}")
    ok.append(('ERR-42: datos/examen_dE5_<sello>.json es escribible', escribible))
    print()
    for n, v in ok:
        print(f"  {'OK  ' if v else '*** FALLA'} {n}")
    print(f"\nHUMO bateria del examen: {sum(v for _, v in ok)}/{len(ok)}  ({time.time()-t0:.0f}s, 3 corridas, sin Pool)")
    sys.exit(0 if all(v for _, v in ok) else 1)
