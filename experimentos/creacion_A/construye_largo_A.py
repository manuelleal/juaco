"""CREADOR A — construye `mundo_largo_A.py` = copia por anclas de `experimentos/nivel8_mundo_largo/mundo_largo.py`
+ DOS perillas nuevas, ambas apagadas por defecto (identidad bit a bit obligatoria con las perillas apagadas):

  `beta_m`  METAPLASTICIDAD POR MASA DE CONFLICTO. Por la equivalencia (Wp,Wn) <-> (W = Wp-Wn, m = min(Wp,Wn))
            (ver mi seccion de `registro/investigacion/PUENTE_creacion.md`, A3), `m_c` es la evidencia
            CONTRADICTORIA acumulada en la celda c, y ya existe en el tronco (con olvido `lam`). La perilla la
            usa como metaplasticidad: la ganancia de la celda pasa a ser  g_c = 1/(1 + beta_m*m_c).
            Una celda que sirve a dos patrones de valencia opuesta (codigo compartido) acumula m y se vuelve
            LENTA: deja de ser reescrita, y el error lo absorben las celdas del codigo que no estan en conflicto.
            Memoria extra: CERO (m ya esta). Localidad: total. `beta_m=None` -> g_c = 1.0 exacto -> identidad.

  `m_stats` lectura, no cambia ningun numero: devuelve estadisticos de m al final (para calibrar beta_m).

NO edita el original. Guarda el sha256 corto del origen en la cabecera del generado.
"""
import os, hashlib, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(AQUI, '..', 'nivel8_mundo_largo', 'mundo_largo.py')
DEST = os.path.join(AQUI, 'mundo_largo_A.py')

src = open(ORIG, 'r', encoding='utf-8').read()
sha = hashlib.sha256(open(ORIG, 'rb').read()).hexdigest()[:16]

# ---- ancla 1: firma de run()
A1 = "        pool=None,T_nuevo=None,reciclado=False,invertir_largo=None):   # mapa + largo"
B1 = ("        pool=None,T_nuevo=None,reciclado=False,invertir_largo=None,\n"
      "        beta_m=None,m_stats=False):   # mapa + largo; creacion_A: metaplasticidad por masa de conflicto")
assert src.count(A1) == 1, 'ancla 1'

# ---- ancla 2: la actualizacion del valor de la via rapida
A2 = """                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc,0,3.)
                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc,0,3.)"""
B2 = """                    _gm=1.0 if beta_m is None else 1.0/(1.0+beta_m*np.minimum(Wp,Wn))   # creacion_A: g_c = 1/(1+beta_m*m_c); con beta_m=None es 1.0 exacto (identidad)
                    if dlt>0: Wp=np.clip(Wp+eta*dlt*kc*_gm,0,3.)
                    else:     Wn=np.clip(Wn+eta*aversion*(-dlt)*kc*_gm,0,3.)"""
assert src.count(A2) == 1, 'ancla 2'

# ---- ancla 3: el return (anadir la lectura de m)
A3 = "    return dict(sobre=sobre,"
B3 = ("    _mst=None\n"
      "    if m_stats:   # creacion_A: LECTURA de la masa de conflicto (no cambia ningun numero)\n"
      "        _mm=np.minimum(Wp,Wn)[activa]\n"
      "        _mst=dict(max=float(_mm.max()),media=float(_mm.mean()),p90=float(np.quantile(_mm,0.9)),\n"
      "                  n_pos=int((_mm>0).sum()),n_mayor_02=int((_mm>0.2).sum()),n_celdas=int(_mm.size))\n"
      "    return dict(m_stats=_mst,beta_m=beta_m,sobre=sobre,")
assert src.count(A3) == 1, 'ancla 3'

out = src.replace(A1, B1).replace(A2, B2).replace(A3, B3)
cab = (f'"""mundo_largo_A = mundo_largo.py ({sha}) + perillas `beta_m` (metaplasticidad por masa de conflicto) y\n'
       f'`m_stats` (lectura). Generado por experimentos/creacion_A/construye_largo_A.py. NO editar a mano.\n'
       f'Con beta_m=None y m_stats=False es mundo_largo EXACTO (identidad obligatoria)."""\n')
open(DEST, 'w', encoding='utf-8').write(cab + out)
print(f'origen {ORIG} sha {sha}')
print(f'escrito {DEST} sha {hashlib.sha256(open(DEST,"rb").read()).hexdigest()[:16]}')
