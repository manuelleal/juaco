"""construye.py — CONSTRUYE POR ANCLAS el instrumento del bloque MURO MINIMO PIEZA (13-oct-2026). Mision: llegar a la AGI por este camino.

Nada se escribe a mano salvo los parches de anclas de abajo. Cada archivo sale de su ORIGEN con sha fijado (sha256[:16] del texto LF):

  COPIAS SIN REEMPLAZOS (esta carpeta esta a la misma profundidad que experimentos/openevolve_serie: las rutas relativas valen)
    experimentos/openevolve_serie/corre_carro.py                    -> corre_carro.py          (pista y juez sin tocar, fundador NO limpio)
    experimentos/openevolve_serie/evaluador.py                      -> evaluador.py            (solo su filtro _revisa)
    experimentos/muro_minimo_20261008/programas/MINIMO.py           -> programas/MINIMO.py     (control bajo; el MISMO texto del bloque anterior)
    experimentos/openevolve_serie/examen/programas/HUMO.py          -> programas/HUMO.py       (control alto)
    experimentos/openevolve_serie/diseccion/programas/KO_PIZARRA.py -> programas/KO_PIZARRA.py (solo para la identidad de AUX_TRES)
    ../../METODO/herramientas/coteja_preregistro.py                 -> coteja_preregistro.py   (cotejo preregistro <-> runner)

  VARIANTES (desde MINIMO; cada trozo nuevo sale de HUMO.py por ancla y se comprueba que esta en HUMO, salvo la llave P_*)
    programas/M_PIZARRA.py   MINIMO + pieza 1 de §2 (la pizarra de HUMO: escucha y difunde)          llave P_PIZARRA
    programas/M_RADIO.py     MINIMO + pieza 2 de §2 (RADIO_BANCO 45 y D0_BANCO 0.6 cerca de criar)    llave P_RADIO
    programas/M_RECICLA.py   MINIMO + pieza 3 de §2 (RECIC_UTIL 0.6: limpiar compite por distancia)    llave P_RECICLA
    programas/M_URGENCIA.py  MINIMO + pieza 4 de §2 (urgencia 1.3 sobre el umbral)                    llave P_URGENCIA
    programas/AUX_TRES.py    MINIMO + piezas 2, 3, 4  (NO es brazo: identidad contra KO_PIZARRA)
    programas/AUX_TODAS.py   MINIMO + piezas 1-4      (NO es brazo: identidad contra HUMO)
  Con la llave en 0 cada variante debe ser MINIMO bit a bit (identidad.py). AUX_TODAS encendida debe ser HUMO bit a bit: si lo es,
  la lista de §2 del bloque anterior es COMPLETA (no hay quinta diferencia escondida).

  RUNNER (por anclas desde el del bloque anterior)
    experimentos/muro_minimo_20261008/corre_examen.py (sha d202bd621d2eb4ba) -> corre_examen.py   (reemplazos de construye_examen.py)

Uso:  python -B construye.py            (escribe)        python -B construye.py --check   (solo compara; sale con 1 si algo difiere)
"""
import hashlib, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(AQUI))
SER = os.path.join(REPO, "experimentos", "openevolve_serie")
ANT = os.path.join(REPO, "experimentos", "muro_minimo_20261008")
PISTA = os.path.join(REPO, "experimentos", "carrera_escuderias")
METODO = os.path.normpath(os.path.join(REPO, "..", "..", "METODO", "herramientas"))

COPIAS = [  # (origen, destino relativo, sha16 del texto LF)
    (os.path.join(SER, "corre_carro.py"), "corre_carro.py", "ddcfd0f06a7acc87"),
    (os.path.join(SER, "evaluador.py"), "evaluador.py", "6736985f4f42cdc5"),
    (os.path.join(ANT, "programas", "MINIMO.py"), os.path.join("programas", "MINIMO.py"), "b9cfbb3bb7cb3de6"),
    (os.path.join(SER, "examen", "programas", "HUMO.py"), os.path.join("programas", "HUMO.py"), "69fcfcb2473fdbf6"),
    (os.path.join(SER, "diseccion", "programas", "KO_PIZARRA.py"), os.path.join("programas", "KO_PIZARRA.py"), "965aaec1e366a098"),
    (os.path.join(METODO, "coteja_preregistro.py"), "coteja_preregistro.py", "2fdae186bf60b492"),
]
EXTERNOS = {"coteja_preregistro.py"}   # si su origen no esta en esta maquina, vale la copia local con el sha fijado
SOLO_LEE = [  # no se copian; se fija su sha binario
    (os.path.join(PISTA, "carros", "O1.py"), "99436afa2715f028"),
    (os.path.join(PISTA, "pista.py"), "9f47c65e438e0ff4"),
    (os.path.join(PISTA, "juez.py"), "6a68f640a7832f12"),
    (os.path.join(PISTA, "revisa_carro.py"), "1c8a789f7427ab96"),
]
ORIGEN_EXAMEN = (os.path.join(ANT, "corre_examen.py"), "d202bd621d2eb4ba")


def lf(ruta):
    return open(ruta, "rb").read().decode("utf-8").replace("\r\n", "\n")


def s16(txt):
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()[:16]


def origen(ruta, sha):
    t = lf(ruta); h = s16(t)
    if h != sha: raise SystemExit(f"ORIGEN CAMBIO: {ruta} sha {h} != {sha}")
    return t


def uno(txt, ancla, que):
    n = txt.count(ancla)
    if n != 1: raise SystemExit(f"ANCLA {que}: aparece {n} veces (debe ser 1): {ancla[:90]!r}")


def trozo(txt, ini, fin, que):
    """texto desde `ini` (unico) hasta antes de la primera aparicion de `fin` despues de el."""
    uno(txt, ini, que)
    i = txt.index(ini); j = txt.index(fin, i + len(ini))
    return txt[i:j]


def aplica(txt, parches, que):
    for k, (ancla, nuevo) in enumerate(parches):
        uno(txt, ancla, f"{que}#{k}")
        txt = txt.replace(ancla, nuevo)
    return txt


# ------------------------------------------------------------------------------------------------- las piezas de §2
ANCLA_D0 = "D0 = 3.0           # suavizado de la distancia en el puntaje del blanco\n"
ANCLA_IMPORT = "import numpy as np\n"
LLAVE = {1: "P_PIZARRA", 2: "P_RADIO", 3: "P_RECICLA", 4: "P_URGENCIA"}


def parches_pieza(p, H, M):
    """lista de (ancla en el texto que va saliendo de MINIMO, reemplazo). Todo trozo que no es la llave sale de HUMO (H)."""
    if p == 1:
        f_init = trozo(H, "        self.cod_val = {}", "        self.blanco = None\n", "H init pizarra")
        f_codapr = trozo(H, "    def _cod(self, k):", "    def _val(self, k):", "H _cod/_aprende")
        f_val = trozo(H, "    def _val(self, k):", "    def _dist(self, a, b):", "H _val")
        m_val = trozo(M, "    def _val(self, k):", "    def _dist(self, a, b):", "M _val")
        f_escdif = trozo(H, "    def _escucha(self, pizarra):", "    def _hueco(self, pos, otros):", "H _escucha/_difunde")
        f_res = "        self._aprende(k, self.suma[k] / self.n[k])\n"
        f_nace = "        for k in self.n:\n            self._aprende(k, self.suma[k] / self.n[k])\n"
        for t in (f_res, f_nace, "        self._escucha(obs['pizarra'])\n", "escribe=self._difunde())"):
            if t not in H: raise SystemExit(f"PIEZA 1: {t!r} no esta en HUMO")
        a_init = "        self.suma = {}; self.n = {}          # memoria del linaje: letra -> suma de dS, numero de mordidas\n"
        a_obs = "        pos = obs['pos']; lev = (float(obs['E']), float(obs['Ag'])); objs = obs['objs']\n"
        a_res = "        self.suma[k] = self.suma.get(k, np.zeros(2)) + dS; self.n[k] = self.n.get(k, 0) + 1\n"
        a_nace = "                if k not in self.n: self.suma[k] = np.asarray(s, float).copy(); self.n[k] = int(n)\n"
        return [
            (ANCLA_D0, ANCLA_D0 + "P_PIZARRA = 1      # llave de la pieza 1 (pizarra de HUMO: escucha y difunde); 0 = MINIMO\n"),
            (a_init, a_init + f_init),
            (m_val, f_codapr + f_val),
            (a_obs, a_obs + "        if P_PIZARRA: self._escucha(obs['pizarra'])\n"),
            ("escribe=None)", "escribe=self._difunde() if P_PIZARRA else None)"),
            ("    def _hueco(self, pos, otros):\n", f_escdif + "    def _hueco(self, pos, otros):\n"),
            (a_res, a_res + f_res),
            (a_nace, a_nace + f_nace),
        ]
    if p == 2:
        f_const = trozo(H, "D0_BANCO = 0.6", "CAP = 1.5", "H D0_BANCO/RADIO_BANCO")
        for t in ("if banco and d > RADIO_BANCO: continue", "d0 = D0_BANCO if banco else D0", "s = g / (d + d0)"):
            if t not in H: raise SystemExit(f"PIEZA 2: {t!r} no esta en HUMO")
        a_d = "            d = self._dist(pos, x); v = self._val(k)\n"
        return [
            (ANCLA_D0, ANCLA_D0 + f_const + "P_RADIO = 1        # llave de la pieza 2 (radio de banco de HUMO cerca de criar); 0 = MINIMO\n"),
            (a_d, a_d + "            if P_RADIO and criando and d > RADIO_BANCO: continue\n"),
            ("                s = g / (d + D0)\n", "                s = g / (d + (D0_BANCO if P_RADIO and criando else D0))\n"),
        ]
    if p == 3:
        f_const = trozo(H, "RECIC_UTIL = 0.6", "\n\n\nclass Carro", "H RECIC_UTIL") + "\n"
        for t in ("s = RECIC_UTIL / (d + d0)", "if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO",
                  "if mejor is None or s > mejor[0]: mejor = (s, x)"):
            if t not in H: raise SystemExit(f"PIEZA 3: {t!r} no esta en HUMO")
        a_suc = "            elif sucio is None or d < sucio[0]: sucio = (d, x)\n"
        return [
            (ANCLA_D0, ANCLA_D0 + f_const + "P_RECICLA = 1      # llave de la pieza 3 (limpiar compite por distancia con lo bueno); 0 = MINIMO\n"),
            (a_suc, "            elif P_RECICLA:\n"
                    "                s = RECIC_UTIL / (d + D0)\n"
                    "                if otros and min(self._dist(o, x) for o in otros) < d: s *= PEN_OTRO\n"
                    "                if mejor is None or s > mejor[0]: mejor = (s, x)\n" + a_suc),
        ]
    if p == 4:
        if "(2.0 if x < self.U else 1.3)" not in H: raise SystemExit("PIEZA 4: la urgencia 1.3 no esta en HUMO")
        return [
            (ANCLA_D0, ANCLA_D0 + "P_URGENCIA = 1     # llave de la pieza 4 (urgencia 1.3 sobre el umbral); 0 = MINIMO\n"),
            ("            u = 4.0 if x < 0.3 else (2.0 if x < self.U else 1.0)\n",
             "            u = 4.0 if x < 0.3 else (2.0 if x < self.U else (1.3 if P_URGENCIA else 1.0))\n"),
        ]
    raise SystemExit(f"pieza {p}?")


VARIANTES = {"M_PIZARRA": (1,), "M_RADIO": (2,), "M_RECICLA": (3,), "M_URGENCIA": (4,), "AUX_TRES": (2, 3, 4), "AUX_TODAS": (1, 2, 3, 4)}


def variante(nombre, piezas, M, H):
    cab = (ANCLA_IMPORT + f"# VARIANTE {nombre} (bloque MURO MINIMO PIEZA, 13-oct-2026): MINIMO + pieza(s) {list(piezas)} de §2 del PREREGISTRO de\n"
           f"# muro_minimo_20261008. Escrita por construye.py desde MINIMO (sha b9cfbb3bb7cb3de6); todo trozo nuevo sale de HUMO.py\n"
           f"# (sha 69fcfcb2473fdbf6) salvo las llaves P_*. Con las llaves en 0 es MINIMO bit a bit (identidad.py).\n")
    t = aplica(M, [(ANCLA_IMPORT, cab)], f"{nombre} cabecera")
    for p in piezas:
        t = aplica(t, parches_pieza(p, H, M), f"{nombre} pieza {p}")
    return t


# ------------------------------------------------------------------------------------------------- el runner
def reemplazos_examen(shas12):
    import construye_examen as CE   # los textos largos (nuevo y viejo) viven en su propio modulo, para no inflar este
    return CE.reemplazos(shas12)


def objetivos():
    """{destino relativo: texto} de todo lo que esta carpeta debe contener."""
    out = {}
    for org, dst, sha in COPIAS:
        if os.path.basename(dst) in EXTERNOS and not os.path.exists(org):
            d = os.path.join(AQUI, dst)
            t = lf(d)
            if s16(t) != sha: raise SystemExit(f"{dst}: origen ausente y la copia local no tiene el sha fijado {sha}")
            out[dst] = t; continue
        out[dst] = origen(org, sha)
    M = out[os.path.join("programas", "MINIMO.py")]; H = out[os.path.join("programas", "HUMO.py")]
    for n, piezas in VARIANTES.items():
        out[os.path.join("programas", n + ".py")] = variante(n, piezas, M, H)
    if AQUI not in sys.path: sys.path.insert(0, AQUI)
    shas12 = {n: s16(out[os.path.join("programas", n + ".py")])[:12] for n in VARIANTES if not n.startswith("AUX_")}
    out["corre_examen.py"] = aplica(origen(*ORIGEN_EXAMEN), reemplazos_examen(shas12), "corre_examen")
    return out


def main(check):
    mal = 0
    for dst, t in objetivos().items():
        d = os.path.join(AQUI, dst)
        if check:
            ok = os.path.exists(d) and lf(d) == t
            mal += not ok
            print(f"  {'IGUAL  ' if ok else 'DIFIERE'} {dst}  (sha16 {s16(t)})")
        else:
            os.makedirs(os.path.dirname(d), exist_ok=True)
            with open(d, "w", encoding="utf-8", newline="\n") as fh: fh.write(t)
            print(f"  escrito {dst}  (sha16 {s16(t)})")
    for org, sha in SOLO_LEE:
        h = hashlib.sha256(open(org, "rb").read()).hexdigest()[:16]
        ok = h == sha; mal += not ok
        print(f"  {'IGUAL  ' if ok else 'DIFIERE'} {os.path.relpath(org, REPO)}  sha {h} (fijado {sha})")
    print("CONSTRUYE:", "TODO IGUAL" if not mal else f"{mal} DIFERENCIAS")
    return mal


if __name__ == "__main__":
    sys.exit(1 if main("--check" in sys.argv) else 0)
