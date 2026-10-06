import numpy as np


class Carro:
    banco = {}

    def __init__(self, ctx):
        self.rng = ctx['rng']
        self.e = self.rng.bit_generator.state

    def actua(self, obs): return dict(mov=1, muerde=False, escribe=None)
    def resultado(self, res): pass
    def fin_paso(self, info): pass
    def muere(self, info): pass
    def nace(self, info): pass
    def al_parir(self, info): return None


def crea(ctx):
    return Carro(ctx)
