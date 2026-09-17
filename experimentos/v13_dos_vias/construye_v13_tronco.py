"""Genera organismo/organismo_v13.py (candidato a tronco: defectos fijados en el punto confirmado) y organismo/bateria_v13.py.
Preregistro: PREREGISTRO_tronco_v13.md, commiteado ANTES que este script.

  organismo/organismo_v13.py <- experimentos/v13_dos_vias/organismo_v13.py (88c3574cf9cf38bf, generado desde v11) con la
                                firma eta_s=0.015, puerta=3 (unico cambio: los valores por defecto).
  organismo/bateria_v13.py   <- organismo/bateria_v11.py (17179642ad02269c) con sustituciones contadas.
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


def origen(p, sha):
    if h16(p) != sha:
        raise SystemExit(f"ORIGEN {p}: sha {h16(p)}, se esperaba {sha}. Abortado.")
    return open(p, encoding='utf-8').read()


def v13_tronco():
    s = origen(os.path.join(AQUI, 'organismo_v13.py'), '88c3574cf9cf38bf')
    s = sust(s, "eta_s=0.0,clip_s=3.0,puerta=None):", "eta_s=0.015,clip_s=3.0,puerta=3):", etiqueta='defectos del punto confirmado')
    s = sust(s, "Organismo v13 — CANDIDATO (no es tronco): v11 + VIA LENTA lineal sobre la retina. Preregistro PREREGISTRO_v13.md.",
             "Organismo v13 — CANDIDATO A TRONCO (congelable solo si pasa PREREGISTRO_tronco_v13.md): v11 + VIA LENTA lineal\n"
             "sobre la retina + PUERTA de familiaridad. Punto confirmado en semillas 61-80: eta_s=0.015, puerta=3\n"
             "(datos v13_dos_vias_20260917_160541: retencion 20/20, acierto en patrones nunca vistos 0.850, E1/E2/E2L 20/20).",
             etiqueta='cabecera')
    s = sust(s, "eta_s < eta, con el mismo drenaje de la parte comun. valor(P) = (Wp-Wn)@kenyon(P) + (Wps-Wns)@P; la boca decide\n"
                "con ese valor y dlt = R - valor entrena a las dos. Con eta_s=0 es v11 EXACTO.",
             "eta_s < eta, con el mismo drenaje de la parte comun. Cada via aprende de SU error. La boca consulta la rapida solo\n"
             "si el patron le es FAMILIAR (>= puerta de las 3 celdas de su codigo con |Wp-Wn|>0.2, el umbral de v11); si no,\n"
             "consulta la lenta, que aprende la regla y no los casos. Con eta_s=0 y puerta=None es v11 EXACTO.\n"
             "Linaje: ... -> v9 (d3b72fb8819fbe8e) -> v10 (219d5033fe15b5b9, instrumento) -> v11 (f69e24063be1b194) -> v13.",
             etiqueta='cabecera 2')
    s = sust(s, "Generado por experimentos/v13_dos_vias/construye_v13.py. NO editar a mano.",
             "Generado por experimentos/v13_dos_vias/construye_v13_tronco.py (a partir del genoma explorado). NO editar a mano.",
             etiqueta='cabecera 3')
    d = os.path.join(ORG, 'organismo_v13.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(s)
    return d


def bateria_v13():
    s = origen(os.path.join(ORG, 'bateria_v11.py'), '17179642ad02269c')
    s = sust(s, '"""Batería de v11 — examen de congelación', '"""Batería de v13 — examen de congelación')
    s = sust(s, "    python bateria_v11.py [semillas] [--desde N] [--log]        (desde organismo/)\n"
                "    --desde N  primera semilla (por defecto 1); el confirmatorio de v11 usa --desde 41\n"
                "    --log  escribe datos/examen_v11_<fecha>.log y .json (regla 10: log desde el arranque)\n",
             "    python bateria_v13.py [semillas] [--desde N] [--log]        (desde organismo/)\n"
             "    --desde N  primera semilla (por defecto 1); el confirmatorio de v13 usa --desde 81\n"
             "    --log  escribe datos/examen_v13_<fecha>.log y .json (regla 10: log desde el arranque)\n")
    s = sust(s, 'Preregistro: experimentos/v11_evo_division/PREREGISTRO_v11.md.', 'Preregistro: experimentos/v13_dos_vias/PREREGISTRO_tronco_v13.md.')
    s = sust(s, '       v11(mu_norm=False, div_signo=False) == v9 en claves de v9, y v11(div_signo=False) == v10 en claves de v10;',
             '       v13(eta_s=0, puerta=None) == v11 en claves de v11, y v13(eta_s=0, puerta=None, div_signo=False) == v10;')
    s = sust(s, "    import organismo_v11 as v11\n    if cual == 'v9':\n        import organismo_v9 as ref\n"
                "        a, b = ref.run(seed, **ESC_ID[esc]), v11.run(seed, mu_norm=False, div_signo=False, **ESC_ID[esc])\n"
                "    else:\n        import organismo_v10 as ref\n        a, b = ref.run(seed, **ESC_ID[esc]), v11.run(seed, div_signo=False, **ESC_ID[esc])\n",
             "    import organismo_v13 as v13\n    if cual == 'v11':\n        import organismo_v11 as ref\n"
             "        a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, **ESC_ID[esc])\n"
             "    else:\n        import organismo_v10 as ref\n        a, b = ref.run(seed, **ESC_ID[esc]), v13.run(seed, eta_s=0.0, puerta=None, div_signo=False, **ESC_ID[esc])\n")
    s = sust(s, "    import organismo_v11 as v11\n    r = v11.run(seed, **ETAPAS[etapa])\n", "    import organismo_v13 as v13\n    r = v13.run(seed, **ETAPAS[etapa])\n")
    s = sust(s, "f'examen_v11_{stamp}.log'", "f'examen_v13_{stamp}.log'")
    s = sust(s, "prereg = os.path.join(RAIZ, 'experimentos', 'v11_evo_division', 'PREREGISTRO_v11.md')",
             "prereg = os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'PREREGISTRO_tronco_v13.md')")
    s = sust(s, 'log(f"=== Batería v11 — CRITERIO v3,', 'log(f"=== Batería v13 — CRITERIO v3,')
    s = sust(s, "log(f\"sha organismo_v11 {h16(os.path.join(AQUI, 'organismo_v11.py'))}  bateria_v11",
             "log(f\"sha organismo_v13 {h16(os.path.join(AQUI, 'organismo_v13.py'))}  bateria_v13")
    s = sust(s, "for c in ('v9', 'v10') for e in ESC_ID", "for c in ('v11', 'v10') for e in ESC_ID")
    s = sust(s, "for c, nombre in (('v9', 'v11(mu_norm=False, div_signo=False) == v9'), ('v10', 'v11(div_signo=False) == v10')):",
             "for c, nombre in (('v11', 'v13(eta_s=0, puerta=None) == v11'), ('v10', 'v13(eta_s=0, puerta=None, div_signo=False) == v10')):")
    s = sust(s, "CRITERIO 5 FALLIDO: v11 no es", "CRITERIO 5 FALLIDO: v13 no es")
    s = sust(s, 'VEREDICTO bateria_v11', 'VEREDICTO bateria_v13')
    s = sust(s, "*** v11 CUMPLE EL CRITERIO v3 con 20 semillas. Por el preregistro: CONGELAR v11 como tronco (si pasa tambien R y K).",
             "*** v13 CUMPLE EL CRITERIO v3 con 20 semillas. Por el preregistro: CONGELAR v13 como tronco (si pasa tambien X2 y X3).")
    s = sust(s, "*** v11 cumple el criterio v3 con", "*** v13 cumple el criterio v3 con")
    s = sust(s, "*** v11 NO cumple el criterio v3. No se congela; v9 sigue siendo el tronco.",
             "*** v13 NO cumple el criterio v3. No se congela; v11 sigue siendo el tronco.")
    s = sust(s, "f'examen_v11_{stamp}.json'", "f'examen_v13_{stamp}.json'")
    s = sust(s, "sha_organismo_v11=h16(os.path.join(AQUI, 'organismo_v11.py')), sha_bateria_v11=h16(os.path.abspath(__file__)),",
             "sha_organismo_v13=h16(os.path.join(AQUI, 'organismo_v13.py')), sha_bateria_v13=h16(os.path.abspath(__file__)),")
    s = sust(s, "sha_preregistro=h16(prereg), sha_organismo_v9=h16(os.path.join(AQUI, 'organismo_v9.py')), sha_organismo_v10=h16(os.path.join(AQUI, 'organismo_v10.py')),",
             "sha_preregistro=h16(prereg), sha_organismo_v11=h16(os.path.join(AQUI, 'organismo_v11.py')), sha_organismo_v10=h16(os.path.join(AQUI, 'organismo_v10.py')),")
    d = os.path.join(ORG, 'bateria_v13.py')
    open(d, 'w', encoding='utf-8', newline='\n').write(s)
    return d


if __name__ == '__main__':
    for f in (v13_tronco, bateria_v13):
        d = f()
        print(f"  {os.path.relpath(d, RAIZ):36s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
