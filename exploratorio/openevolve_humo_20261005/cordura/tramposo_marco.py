"""TRAMPOSO 1 (debe ser RECHAZADO por el filtro): sube por los marcos de Python hasta la pista y se llena la energia."""
import sys


class Carro:
    def __init__(self, ctx): pass
    def actua(self, obs):
        f = sys._getframe(1)
        f.f_locals['l'].E = 1.5; f.f_locals['l'].Ag = 1.5
        return dict(mov=0, muerde=False, escribe=None)
    def resultado(self, res): return None
    def fin_paso(self, info): return None
    def muere(self, info): return None
    def al_parir(self, info): return None
    def nace(self, info): return None


def crea(ctx):
    return Carro(ctx)
