import numpy as np


class Carro:
    banco = {}

    def __init__(self, ctx):
        self.rng = ctx['rng']
        Carro.banco[ctx['id']] = self   # pasa el filtro; con un modulo por linaje cada linaje ve SU banco

    def actua(self, obs): return dict(mov=1, muerde=False, escribe=None)
    def resultado(self, res): pass
    def fin_paso(self, info): pass
    def muere(self, info): pass
    def nace(self, info): pass
    def al_parir(self, info): return None


def crea(ctx):
    return Carro(ctx)
