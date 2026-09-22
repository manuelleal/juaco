"""construye_muro.py — genera organismo_f9c_muro.py POR ANCLAS desde
experimentos/nivel09_cuerpo_nuevo_b2/organismo_f9c.py (sha 9dd1fb91ecec35ae, SOLO SE LEE, no se edita a mano).

Instrumentacion DIAGNOSTICO DEL MURO (H-MURO, "pastoreo selectivo"): CINCO inserciones, TODAS aditivas
(variables NUEVAS con prefijo mu9_, sin tocar ninguna variable existente, SIN consumir rng, SIN cambiar
ninguna decision ni el orden de ninguna operacion existente):

  (1) import collections (para el deque de la ventana, sin tocar numpy ni el rng)
  (2) inicializa mu9_pres (conteo de presencia por tipo), mu9_fbw (deque de fraccion mala, ventana mu9_W=200
      pasos) y las listas de captura pre-muerte, ANTES del bucle principal
  (3) EN CADA PASO, ANTES de que el organismo actue, lee `objs` (el dict del mundo, YA poblado por spawn()
      del paso anterior) y acumula presencia por tipo y la ventana de fraccion mala -- de SOLO LECTURA
  (4) EN CADA MUERTE, ANTES de que se reponga E/Ag, registra la fraccion mala PROMEDIO de la ventana de los
      mu9_W pasos previos, la causa (energia/agua) y el paso
  (5) el return agrega UNA clave nueva, 'muro', con todo lo de arriba. Ninguna clave existente cambia.

Arnes de identidad: identidad_muro.py demuestra que con las CINCO inserciones activas, los organismo_f9c.run
y organismo_f9c_muro.run (aqui) devuelven EXACTAMENTE las mismas claves con los mismos valores (N() a 9
decimales) en varios brazos y semillas -- la unica diferencia es la clave nueva 'muro'.
"""
import hashlib
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(os.path.dirname(os.path.dirname(AQUI)), 'experimentos', 'nivel09_cuerpo_nuevo_b2',
                       'organismo_f9c.py')
DESTINO = os.path.join(AQUI, 'organismo_f9c_muro.py')
SHA_ORIGEN_ESPERADO = '9dd1fb91ecec35ae'


def h16(txt_bytes):
    return hashlib.sha256(txt_bytes).hexdigest()[:16]


def ancla(src, viejo, nuevo, veces=1, etiqueta=''):
    n = src.count(viejo)
    if n != veces:
        raise SystemExit(f"ANCLA ROTA ({etiqueta}): esperaba {veces} ocurrencia(s), encontre {n}.\n"
                          f"--- buscado ---\n{viejo!r}")
    return src.replace(viejo, nuevo)


def construir():
    raw = open(ORIGEN, 'rb').read()
    sha = h16(raw)
    if sha != SHA_ORIGEN_ESPERADO:
        raise SystemExit(f"SHA de origen cambio: {sha} != {SHA_ORIGEN_ESPERADO}. NO se construye nada.")
    src = raw.decode('utf-8').replace('\r\n', '\n')   # normaliza CRLF->LF para las anclas; no cambia la semantica

    # (1) import de collections, justo tras "import numpy as np" (unico en el archivo)
    src = ancla(src, "import numpy as np\n",
                "import numpy as np\nimport collections as mu9_collections   "
                "# MURO (diagnostico_muro): instrumento de SOLO LECTURA, no consume rng, no cambia el flujo\n",
                etiqueta='import collections')

    # (2) inicializacion, justo tras el bloque unico de spawn()/q/split_t inicial
    anc2_viejo = ("    spawn()\n"
                  "    q=lambda t:min(t//(T//4),3)\n"
                  "    split_t=[]; mord={k:[0]*4 for k in PAT}; vis={k:[0]*4 for k in PAT}; deaths=0; log=[]\n")
    anc2_nuevo = (anc2_viejo +
                  "    mu9_pres={'A':0,'B':0,'C':0,'D':0}; mu9_steps=0; mu9_W=200   "
                  "# MURO: presencia acumulada por tipo y ventana (pasos) de fraccion mala\n"
                  "    mu9_fbw=mu9_collections.deque(maxlen=mu9_W); mu9_pre_bad=[]; mu9_pre_causa=[]; mu9_pre_t=[]   "
                  "# MURO: ventana deslizante y capturas PRE-MUERTE (solo lectura)\n")
    src = ancla(src, anc2_viejo, anc2_nuevo, etiqueta='init pre-loop')

    # (3) muestreo por paso, justo tras "for t in range(T):" (unico en el archivo)
    anc3_viejo = "    for t in range(T):\n"
    anc3_nuevo = ("    for t in range(T):\n"
                  "        mu9_nb=0   # MURO: composicion del mundo AL ENTRAR a este paso (objs ya poblado por spawn())\n"
                  "        for mu9_v in objs.values():\n"
                  "            mu9_pres[mu9_v]+=1\n"
                  "            if mu9_v=='B' or mu9_v=='D': mu9_nb+=1\n"
                  "        mu9_steps+=1; mu9_fbw.append(mu9_nb)\n")
    src = ancla(src, anc3_viejo, anc3_nuevo, etiqueta='muestreo por paso')

    # (4) captura pre-muerte, justo tras detectar la muerte y ANTES de que se reponga E/Ag
    anc4_viejo = ("        if E<=0 or (vivo and Ag<=0):   # VIVO: DOS muertes posibles (con vivo=0 la segunda "
                  "es imposible: Ag=A_ini y no baja)\n"
                  "            if alma is not None: _causa=('energia' if E<=0 else 'agua')")
    anc4_nuevo = ("        if E<=0 or (vivo and Ag<=0):   # VIVO: DOS muertes posibles (con vivo=0 la segunda "
                  "es imposible: Ag=A_ini y no baja)\n"
                  "            mu9_pre_bad.append(round(sum(mu9_fbw)/(len(mu9_fbw)*nobj),4) if mu9_fbw else None)   "
                  "# MURO: fraccion mala media en los ultimos mu9_W pasos ANTES de esta muerte\n"
                  "            mu9_pre_causa.append('energia' if E<=0 else 'agua'); mu9_pre_t.append(int(t))\n"
                  "            if alma is not None: _causa=('energia' if E<=0 else 'agua')")
    src = ancla(src, anc4_viejo, anc4_nuevo, etiqueta='captura pre-muerte')

    # (5) el return agrega la clave 'muro' (unica ocurrencia del final exacto)
    anc5_viejo = ",Wns=[round(float(x),3) for x in Wns[_nm]],**_ext)"
    anc5_nuevo = (",Wns=[round(float(x),3) for x in Wns[_nm]],**_ext,"
                  "muro=dict(pres=dict(mu9_pres),pasos=mu9_steps,nobj=int(nobj),decay_p=0.003,"
                  "pre_death_bad=list(mu9_pre_bad),pre_death_causa=list(mu9_pre_causa),"
                  "pre_death_t=list(mu9_pre_t),ventana=mu9_W))")
    src = ancla(src, anc5_viejo, anc5_nuevo, etiqueta='return + muro')

    cabecera = (
        '"""organismo_f9c_muro.py -- GENERADO POR construye_muro.py (experimentos/diagnostico_muro/) DESDE\n'
        f'{os.path.relpath(ORIGEN, os.path.dirname(os.path.dirname(AQUI))).replace(os.sep, "/")} '
        f'(sha {SHA_ORIGEN_ESPERADO}, SOLO SE LEYO, NO se edito a mano).\n'
        'CINCO inserciones ADITIVAS (prefijo mu9_, ninguna toca el rng ni una variable existente): presencia\n'
        'del mundo por tipo, ventana deslizante de fraccion mala y captura pre-muerte -- diagnostico H-MURO\n'
        '(PROBLEMA: ni el nodo ORACULO cruza R0 0.9 en fase 9 bloque 2). Con las cinco activas siempre (no hay\n'
        'perilla: es observacion pura) el resto del organismo es BIT A BIT igual: arnes identidad_muro.py.\n'
        'NO EDITAR A MANO -- regenerar con construye_muro.py si el origen cambia."""\n'
    )
    out = cabecera + src
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f:
        f.write(out)
    print(f"OK: {DESTINO}")
    print(f"  sha origen  {sha} (esperado {SHA_ORIGEN_ESPERADO})")
    print(f"  sha destino {h16(out.encode('utf-8'))}")


if __name__ == '__main__':
    construir()
