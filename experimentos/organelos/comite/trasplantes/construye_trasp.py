"""construye_trasp.py — EXPLORATORIO, no es dato. Construye carros/TRASP.py POR ANCLAS de texto desde organelos/cruce/carros/CRUCE.py
(sólo se LEE). Agrega la perilla ENSENA (módulo): 0 = CRUCE bit a bit (nada nuevo corre); 1 = el hijo nace con las DOS FILAS LENTAS del
padre (Wps, Wns: lo que el linaje sabe de cada letra) copiadas en al_parir; 2 = el hijo nace con TODO el cerebro aprendido del padre
(filas lentas + Kenyon KW/activa + Wp/Wn + ncod/_ord + mu/mup/mun/zp/zn/err + patas Wl). Es `nacer/todo/hijo/copiar` (ensena) de la
cinta, puesto a mano. El fundador limpio NO recibe nada (instancia nueva, sin nace()): igual que O1.
MISION: llegar a la AGI por este camino."""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ORIGEN = os.path.normpath(os.path.join(AQUI, '..', '..', 'cruce', 'carros', 'CRUCE.py'))
SALIDA = os.path.join(AQUI, 'carros', 'TRASP.py')


def h16b(b): return hashlib.sha256(b).hexdigest()[:16]


def construye():
    src = open(ORIGEN, encoding='utf-8').read()
    anclas = [
        # 1) cabecera + perilla
        ('"""CRUCE.py — organelos/cruce:',
         '"""TRASP.py — comite/trasplantes (EXPLORATORIO, no es dato): CRUCE.py + perilla ENSENA (0 = CRUCE bit a bit).\n'
         'CONSTRUIDO por comite/trasplantes/construye_trasp.py. NO editar a mano. Sigue el docstring del origen.\n\nCRUCE.py — organelos/cruce:'),
        ('BUF_LES = 2000      # control DESFASADO',
         'ENSENA = 0          # TRASPLANTE: 0 nada (CRUCE bit a bit) · 1 filas lentas del padre · 2 todo el cerebro aprendido del padre\n'
         'BUF_LES = 2000      # control DESFASADO'),
        # 2) al_parir: lo que se lleva el hijo
        ("        return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)",
         "        if ENSENA: return self._ensena_parir()   # TRASPLANTE ensena: el hijo se lleva lo aprendido\n"
         "        return None   # hereda='nada': el hijo no se lleva memoria (la dote la pone la pista)"),
        # 3) nace: al final (tras el nodo), el hijo recibe lo del padre
        ("            self._ldiv += int(len(self._nodo) > self.NODO_LEE or (_sel9 != sorted(_sel9)))\n",
         "            self._ldiv += int(len(self._nodo) > self.NODO_LEE or (_sel9 != sorted(_sel9)))\n"
         "        if ENSENA and info.get('memoria') is not None: self._ensena_nace(info['memoria'])   # TRASPLANTE ensena\n"),
        # 4) los metodos
        ("    # ================================================================ CRUCE: lectura del genoma",
         "    # ================================================================ TRASPLANTE ensena (comite/trasplantes)\n"
         "    def _ensena_parir(self):\n"
         "        m = dict(Wps=self.Wps.copy(), Wns=self.Wns.copy())\n"
         "        if ENSENA >= 2:\n"
         "            m.update(KW=self.KW.copy(), activa=self.activa.copy(), Wp=self.Wp.copy(), Wn=self.Wn.copy(), ncod=dict(self.ncod), ord=list(self._ord),\n"
         "                     mu=self.mu.copy(), mup=self.mup.copy(), mun=self.mun.copy(), zp=self.zp.copy(), zn=self.zn.copy(), err=self.err.copy(), Wl=self.Wl.copy())\n"
         "        self._ens['partos'] += 1\n"
         "        return m\n\n"
         "    def _ensena_nace(self, m):\n"
         "        self.Wps[:] = m['Wps']; self.Wns[:] = m['Wns']; self._ens['hijos'] += 1\n"
         "        if ENSENA >= 2 and 'KW' in m:\n"
         "            self.KW[:] = m['KW']; self.activa[:] = m['activa']; self.Wp[:] = m['Wp']; self.Wn[:] = m['Wn']\n"
         "            self.ncod.clear(); self.ncod.update(m['ncod']); self._ord[:] = list(m['ord'])\n"
         "            self.mu[:] = m['mu']; self.mup[:] = m['mup']; self.mun[:] = m['mun']; self.zp[:] = m['zp']; self.zn[:] = m['zn']; self.err[:] = m['err']\n"
         "            self.Wl[:] = m['Wl']\n"
         "        self._v3c = None\n\n"
         "    # ================================================================ CRUCE: lectura del genoma"),
        # 5) contador
        ("        self._cr_init(ctx)   # CRUCE\n",
         "        self._cr_init(ctx)   # CRUCE\n        self._ens = dict(ensena=ENSENA, partos=0, hijos=0)   # TRASPLANTE\n"),
        # 6) telemetria propia
        ("            **({'cruce': self._cr_salida()} if self._cr is not None else {}))",
         "            **({'cruce': self._cr_salida()} if self._cr is not None else {}), ensena=dict(self._ens))"),
    ]
    out = src
    for a, b in anclas:
        if out.count(a) != 1: raise SystemExit(f"ancla no unica ({out.count(a)}): {a[:70]!r}")
        out = out.replace(a, b)
    return out.encode('utf-8')


if __name__ == '__main__':
    b = construye()
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    open(SALIDA, 'wb').write(b)
    print(f"origen CRUCE.py {h16b(open(ORIGEN, 'rb').read())} -> {SALIDA} {h16b(b)}")
