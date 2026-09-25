"""construye_v01.py — CONSTRUYE v01/motor_v01.py por ANCLAS desde ../exploracion_fable/motor_fable.py (SOLO LECTURA; sha fijado).

MISION: llegar a la AGI por este camino.

Anclas (cada una debe aparecer exactamente una vez):
 V0 rutas: la carpeta de fable_mundos (exploracion_fable/) entra a sys.path; AQUI sigue siendo codigo/ (carros, codigo_def, gramatica_def).
 V1 telemetria de PERILLAS: en cada PARTO sin cinta (con gramatica) se registra [t, lin, k, k_padre, fenotipo_cambio] (fenotipo = las 20
    perillas + la gramatica; la misma definicion que la de la cinta en _cod). Es la medida con que se CALIBRA PERILLAS_ROBUSTA.
 V2 el banco de CINTAS en el corte (lo que la seleccion dejo al quitar el reponedor).
 V3 salida: d['codigo'] tambien con per_nac y banco_corte (solo lectura; no toca la fisica).
Con todo eso, la FISICA es la de motor_fable bit a bit (arnes I1 de identidad_v01.py: salida entera menos esas dos claves).
"""
import hashlib, os

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.join(os.path.dirname(AQUI), 'exploracion_fable', 'motor_fable.py')
DESTINO = os.path.join(AQUI, 'motor_v01.py')
SHA_ORIGEN = '46750da69ef8cce1'

R = [
 ("_FABLE = os.path.dirname(os.path.abspath(__file__))   # FABLE (F0)\nif _FABLE not in sys.path: sys.path.insert(0, _FABLE)\n"
  "AQUI = os.path.dirname(_FABLE)   # FABLE: la carpeta codigo/\n",
  "_V01 = os.path.dirname(os.path.abspath(__file__))   # v0.1 (V0)\n"
  "_FABLE = os.path.join(os.path.dirname(_V01), 'exploracion_fable')   # FABLE (F0): fable_mundos se IMPORTA de alli, sin copiar\n"
  "if _FABLE not in sys.path: sys.path.insert(0, _FABLE)\n"
  "AQUI = os.path.dirname(_V01)   # la carpeta codigo/\n"),
 ("                        if _CO: _cih, _gh, _grh = _cod(_dci, SE(i, ETQ_CMUT, k), _fmal(b), _dg, _dgr, i, k, t, b.k)   # CODIGO v0 (C3)\n",
  "                        if _CO: _cih, _gh, _grh = _cod(_dci, SE(i, ETQ_CMUT, k), _fmal(b), _dg, _dgr, i, k, t, b.k)   # CODIGO v0 (C3)\n"
  "                        elif _GR: ES.setdefault('per_nac', []).append([t, i, k, b.k, int(not (np.array_equal(_gh, _dg) and tuple(_grh) == tuple(_dgr)))])   # v0.1 (V1)\n"),
 ("vivos_gr=[[z.lin, z.k, z.gen, z.tn, z.gr] for z in _vv])   # ORGANELOS (G4)\n",
  "vivos_gr=[[z.lin, z.k, z.gen, z.tn, z.gr] for z in _vv])   # ORGANELOS (G4)\n"
  "                if _CO: ES['ccorte'] = [[list(x) for x in e[4]] for e in ES['banco']]   # v0.1 (V2): el banco de CINTAS en el corte\n"),
 ("    _cout = {} if not (_CO or _CB is not None) else dict(codigo=dict(   # CODIGO v0 (C6)\n",
  "    _cout = {} if not (_CO or _CB is not None) else dict(codigo=dict(per_nac=ES.get('per_nac', []), banco_corte=ES.get('ccorte'),   # v0.1 (V3)\n"),
]


def main():
    b = open(ORIGEN, 'rb').read(); sha = hashlib.sha256(b).hexdigest()[:16]
    if sha != SHA_ORIGEN: raise SystemExit(f"CONSTRUYE v01: el origen cambio ({sha} != {SHA_ORIGEN})")
    src = b.decode('utf-8').replace('\r\n', '\n')   # motor_fable se escribio con fin de linea de Windows
    for a, n_ in R:
        k = src.count(a)
        if k != 1: raise SystemExit(f"CONSTRUYE v01: ancla aparece {k} veces: {a[:90]!r}")
        src = src.replace(a, n_)
    src = (f'# motor_v01.py: CONSTRUIDO por v01/construye_v01.py desde exploracion_fable/motor_fable.py (sha {SHA_ORIGEN}). NO EDITAR A MANO.\n'
           + src.replace('# EXPLORATORIO, no es dato\n', '', 1))
    with open(DESTINO, 'w', encoding='utf-8', newline='\n') as f: f.write(src)
    print(f"motor_v01.py construido ({len(R)} anclas) sha {hashlib.sha256(open(DESTINO, 'rb').read()).hexdigest()[:16]}")


if __name__ == '__main__':
    main()
