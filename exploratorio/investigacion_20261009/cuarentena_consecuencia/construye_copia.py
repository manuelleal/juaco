# -*- coding: utf-8 -*-
"""Construye las copias por ANCLA desde Frankenstein v1 (sha256 fijado). No edita nada: copia bit a bit.
  python -B construye_copia.py          copia (si falta) y verifica
  python -B construye_copia.py --verifica   sólo verifica
El origen no se toca. Todo lo nuevo vive en mundo_q.py / memorias_q.py / linea.py (archivos propios)."""
import hashlib
import os
import shutil
import sys

ORIGEN = r"C:\Users\User\Documents\PROYECTOS\JUACO\investigacion_20261005\frankenstein_v1"
AQUI = os.path.dirname(os.path.abspath(__file__))
ANCLAS = {
    "cuerpo.py": "6631934a13ba1f1e3e77b20362f487614a750661fd887f0ce6d21dcb8f116570",
    "colonia.py": "03e101ac420b64ff4cdda172a4b1bf285b515cb05996c116503ad52968c7ddf9",
    "mundo.py": "7012d444f4442c023c6619abe65b2b0c81cdb902a154ee1b5faa3ffe2c36f79a",
    "frank.py": "3c34665262011879cf5b587e93c8b65f16cc32f4ee07b12ade3acba83180fafc",
}


def sha(ruta):
    with open(ruta, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    solo = "--verifica" in sys.argv
    os.makedirs(os.path.join(AQUI, "datos"), exist_ok=True)
    ok = True
    for nombre, ancla in ANCLAS.items():
        o, d = os.path.join(ORIGEN, nombre), os.path.join(AQUI, nombre)
        so = sha(o)
        if so != ancla:
            print(f"ORIGEN CAMBIÓ  {nombre}: {so} != ancla {ancla}")
            ok = False
            continue
        if not os.path.exists(d) and not solo:
            shutil.copyfile(o, d)
        sd = sha(d) if os.path.exists(d) else "FALTA"
        igual = sd == ancla
        ok &= igual
        print(f"{'IDENTICO' if igual else 'DISTINTO'}  {nombre}  origen {so[:16]}  copia {sd[:16]}")
    print("COPIAS POR ANCLA:", "BIEN (bit a bit)" if ok else "MAL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
