# -*- coding: utf-8 -*-
"""Escritura de entregables comunes: JSON, SHA256.txt y ZIP reproducible."""

import hashlib
import json
import os
import zipfile

ORDEN_ZIP = ["README.md", "PARAMETERS.json", "RESULTS.json",
             "PER_SEED_RESULTS.json", "GENEALOGY.json", "SUMMARY.md"]


def escribir_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, sort_keys=True, ensure_ascii=True)
        f.write("\n")


def escribir_texto(path, texto):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def sha256_de(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()


def escribir_sha256(carpeta, archivos):
    lineas = []
    for nombre in archivos:
        p = os.path.join(carpeta, nombre)
        if os.path.exists(p):
            lineas.append("%s  %s" % (sha256_de(p), nombre))
    escribir_texto(os.path.join(carpeta, "SHA256.txt"), "\n".join(lineas) + "\n")
    return lineas


def empacar_zip(carpeta, nombre_zip, archivos):
    """ZIP reproducible: fecha fija, orden fijo, sin compresion dependiente."""
    destino = os.path.join(carpeta, nombre_zip)
    if os.path.exists(destino):
        os.remove(destino)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for nombre in archivos:
            p = os.path.join(carpeta, nombre)
            if not os.path.exists(p):
                continue
            with open(p, "rb") as f:
                datos = f.read()
            info = zipfile.ZipInfo(nombre, date_time=(2026, 9, 18, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, datos)
    return destino, sha256_de(destino)


def stats(valores):
    """media, desviacion muestral y error estandar."""
    n = len(valores)
    m = sum(valores) / float(n)
    if n < 2:
        return m, 0.0, 0.0
    var = sum((v - m) ** 2 for v in valores) / float(n - 1)
    sd = var ** 0.5
    return m, sd, sd / (n ** 0.5)
