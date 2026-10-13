# -*- coding: utf-8 -*-
"""Memoización de dos funciones PURAS de las copias (colonia._igual y norm). No edita los archivos copiados:
envuelve en memoria. Mismo resultado, sin repetir difflib. `arnes_identidad.py` comprueba que con y sin esto las
consultas son idénticas. Se activa al importar."""
import functools

import colonia
import mundo

if not getattr(colonia, "_rapido", False):
    _norm = functools.lru_cache(maxsize=None)(mundo.norm)
    mundo.norm = _norm
    colonia.norm = _norm
    colonia._igual = functools.lru_cache(maxsize=None)(colonia._igual)
    colonia._rapido = True
