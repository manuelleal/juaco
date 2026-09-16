"""Genera organismo/bateria_v9.py desde organismo/bateria_v8.py (congelado, 8de16b2e97de8312) con sustituciones contadas.

Criterio v3 sin cambiar un umbral: solo cambian el organismo examinado (v9), la identidad (v9 con memoria_rechazo=0 == v8)
y los nombres. El diff bateria_v8 -> bateria_v9 lo demuestra.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'organismo', 'bateria_v8.py')
SHA_ORIGEN = '8de16b2e97de8312'
DESTINO = os.path.join(RAIZ, 'organismo', 'bateria_v9.py')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA: {viejo[:70]!r} aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


if __name__ == '__main__':
    if h16(ORIGEN) != SHA_ORIGEN:
        raise SystemExit(f"ORIGEN: sha {h16(ORIGEN)}, se esperaba {SHA_ORIGEN}. Abortado.")
    s = open(ORIGEN, encoding='utf-8').read()
    s = sust(s, '"""Batería de v8 — examen de congelación (CRITERIO v3) y,',
             '"""Batería de v9 — examen de congelación (CRITERIO v3, sin cambiar un umbral) y,')
    s = sust(s, 'datos/examen_v8_<fecha>', 'datos/examen_v9_<fecha>')
    s = sust(s, 'Preregistro: experimentos/congelacion_v8/PREREGISTRO_congelacion_v8.md (sha d2924e69128fe0f6).',
             'Preregistro: experimentos/v9_memoria_rechazo/PREREGISTRO_v9.md (sha f68841597adb55d8).\n'
             'Criterio v3: experimentos/congelacion_v8/PREREGISTRO_congelacion_v8.md (sha d2924e69128fe0f6).')
    s = sust(s, '       v8 == v7e(lam=0.05) en claves de v7e;  v8(lam=0) == v7 en claves de v7;  7 escenarios x semillas 1..6.',
             '       v9(memoria_rechazo=0) == v8 en claves de v8;  7 escenarios x semillas 1..6.')
    s = sust(s, '  6. (fuera de esta batería) organismo/bateria.py 20 PASA y manifiesto.py --check.',
             '  6. (fuera de esta batería) organismo/bateria_v8.py 6 PASA y manifiesto.py --check.')
    s = sust(s, ("    import organismo_v8 as v8\n"
                 "    if cual == 'v7e':\n"
                 "        import organismo_v7e as ref\n"
                 "        a, b = ref.run(seed, lam=0.05, **ESC_ID[esc]), v8.run(seed, **ESC_ID[esc])\n"
                 "    else:\n"
                 "        import organismo_v7 as ref\n"
                 "        a, b = ref.run(seed, **ESC_ID[esc]), v8.run(seed, lam=0.0, **ESC_ID[esc])\n"),
             ("    import organismo_v8 as ref, organismo_v9 as v9\n"
              "    a, b = ref.run(seed, **ESC_ID[esc]), v9.run(seed, memoria_rechazo=0, **ESC_ID[esc])\n"))
    s = sust(s, "    import organismo_v8 as v8\n    r = v8.run(seed, **ETAPAS[etapa])\n",
             "    import organismo_v9 as v9\n    r = v9.run(seed, **ETAPAS[etapa])\n")
    s = sust(s, "f'examen_v8_{stamp}.log'", "f'examen_v9_{stamp}.log'")
    s = sust(s, "prereg = os.path.join(RAIZ, 'experimentos', 'congelacion_v8', 'PREREGISTRO_congelacion_v8.md')",
             "prereg = os.path.join(RAIZ, 'experimentos', 'v9_memoria_rechazo', 'PREREGISTRO_v9.md')")
    s = sust(s, 'log(f"=== Batería v8 — CRITERIO v3,', 'log(f"=== Batería v9 — CRITERIO v3,')
    s = sust(s, "log(f\"sha organismo_v8 {h16(os.path.join(AQUI, 'organismo_v8.py'))}  bateria_v8",
             "log(f\"sha organismo_v9 {h16(os.path.join(AQUI, 'organismo_v9.py'))}  bateria_v9")
    s = sust(s, "for c in ('v7e', 'v7') for e in ESC_ID", "for c in ('v8',) for e in ESC_ID")
    s = sust(s, "for c, nombre in (('v7e', 'v8 == v7e(lam=0.05)'), ('v7', 'v8(lam=0) == v7')):",
             "for c, nombre in (('v8', 'v9(memoria=0) == v8'),):")
    s = sust(s, "CRITERIO 5 FALLIDO: v8 no es", "CRITERIO 5 FALLIDO: v9 no es")
    s = sust(s, 'VEREDICTO bateria_v8', 'VEREDICTO bateria_v9')
    s = sust(s, "*** v8 CUMPLE EL CRITERIO v3 con 20 semillas. Por el preregistro: CONGELAR v8 como tronco.",
             "*** v9 CUMPLE EL CRITERIO v3 con 20 semillas. Por el preregistro: CONGELAR v9 como tronco (si pasa tambien el confirmatorio).")
    s = sust(s, "*** v8 cumple el criterio v3 con", "*** v9 cumple el criterio v3 con")
    s = sust(s, "*** v8 NO cumple el criterio v3. No se congela; v6 sigue siendo el tronco.",
             "*** v9 NO cumple el criterio v3. No se congela; v8 sigue siendo el tronco.")
    s = sust(s, "f'examen_v8_{stamp}.json'", "f'examen_v9_{stamp}.json'")
    s = sust(s, "sha_organismo_v8=h16(os.path.join(AQUI, 'organismo_v8.py')), sha_bateria_v8=h16(os.path.abspath(__file__)),",
             "sha_organismo_v9=h16(os.path.join(AQUI, 'organismo_v9.py')), sha_bateria_v9=h16(os.path.abspath(__file__)),")
    s = sust(s, "sha_organismo_v7=h16(os.path.join(AQUI, 'organismo_v7.py')),",
             "sha_organismo_v8=h16(os.path.join(AQUI, 'organismo_v8.py')),")
    s = sust(s, "sha_organismo_v7e=h16(os.path.join(RAIZ, 'experimentos', 'bug01', 'organismo_v7e.py')),",
             "sha_criterio_v3=h16(os.path.join(RAIZ, 'experimentos', 'congelacion_v8', 'PREREGISTRO_congelacion_v8.md')),")
    open(DESTINO, 'w', encoding='utf-8', newline='\n').write(s)
    print(f"  organismo/bateria_v9.py  {h16(DESTINO)}")
