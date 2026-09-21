"""estructura_q2.py -- CALCULO ESTRUCTURAL (T = 0, NO simula nada, no consume presupuesto de corridas).

Pregunta: en el candidato `BA-v` (`dos_tipos=1, var_cubre=1, memoria_variante=0`), el tipo VARIANTE son 3 pares
MIXTOS (un pixel de forma + un pixel de variante), uno por pixel de variante, y su direccion es el BIN DE 2 BITS
de ese par. Para el REFERENTE X y su HERMANA H (misma familia, otra variante):

   bin_(i,q)(X) == bin_(i,q)(H)   <=>   P_X[i]==P_H[i]  y  P_X[q]==P_H[q]

Si alguno de los 3 pares mixtos ganadores le da a X y a H LA MISMA casilla, el +R que el mensaje escribio en la
casilla de X **tambien lo lee la hermana**: el canal de variante queda CONTAMINADO por el propio mensaje.

Esto se calcula con los patrones del mundo (escala_codigo.catalogo), sin correr el organismo.
Salida: por semilla, cuantos pixeles de variante COINCIDEN entre X y H, cuantos de los pares mixtos colisionan,
y el cruce con `dist` medido en la serie 961-980.
"""
import json, os, sys, glob

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, '..', '..', '..'))
BAV = os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv')
JBA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'BA')
JA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A')
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [BAV, JBA, JA, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]
import numpy as np
import corre_familias_b6 as B6R

XNEG, BAR, PATS = B6R.XNEG, B6R.BAR, B6R.PATS
D, NVAR = 12, 3
VARPX = list(range(D - NVAR, D))            # 9, 10, 11
MIXTAS = [(i, j) for i in range(D) for j in range(i + 1, D)
          if min(i, j) < D - NVAR <= max(i, j)]
FORMA = [(i, j) for i in range(D) for j in range(i + 1, D) if max(i, j) < D - NVAR]

CRUDO = os.path.join(BAV, 'serie_bav_s961-980_20260921_145002_crudo.json')


def bin4(par, P):
    return int(P[par[0]]) * 2 + int(P[par[1]])


def main():
    d = json.load(open(CRUDO, 'r', encoding='utf-8'))
    dist = {}
    for r in d['brazos']:
        if r['cel'] == 'BA-v' and r['base'] == 'PAR':
            dist[r['seed']] = r['B4']['dist']
    ganvar = {}
    for r in d['brazos']:
        if r['cel'] == 'BA-v' and r['base'] == 'PAR' and r['gan_var']:
            ganvar[r['seed']] = [tuple(x) for x in r['gan_var']]

    print('Referente X = %s   Hermana H = %s   Otro token TK = %s' % (XNEG, BAR['neg']['H'], BAR['neg']['TK']))
    print('pares de FORMA: %d   pares MIXTOS (tipo VARIANTE): %d   px de variante: %s'
          % (len(FORMA), len(MIXTAS), VARPX))
    print()
    print('%-6s %-5s %-9s %-9s %-10s %-12s %-30s' %
          ('seed', 'dist', 'dHam(X,H)', 'px_var=', 'mixtas_col', 'forma_col', 'ganadoras VARIANTE (par: col?)'))
    tot = {0: [], 1: [], 2: [], 3: []}
    for s in sorted(dist):
        P = PATS(s)
        X, H = P[XNEG], P[BAR['neg']['H']]
        dham = int(sum(1 for k in range(D) if int(X[k]) != int(H[k])))
        igual_var = [q for q in VARPX if int(X[q]) == int(H[q])]
        mix_col = [p for p in MIXTAS if bin4(p, X) == bin4(p, H)]
        for_col = [p for p in FORMA if bin4(p, X) == bin4(p, H)]
        gv = ganvar.get(s, [])
        gtxt = ' '.join('%s:%s' % (p, 'COLISIONA' if bin4(p, X) == bin4(p, H) else 'separa') for p in gv)
        ncol_gan = sum(1 for p in gv if bin4(p, X) == bin4(p, H))
        tot[ncol_gan].append((s, dist[s]))
        print('%-6d %-5s %-9d %-9s %-10s %-12s %s'
              % (s, dist[s], dham, ''.join(str(q) for q in igual_var) or '-',
                 '%d/%d' % (len(mix_col), len(MIXTAS)), '%d/%d' % (len(for_col), len(FORMA)), gtxt))

    print()
    print('--- CRUCE: cuantas de las 3 ganadoras de VARIANTE le dan a X y a H LA MISMA casilla ---')
    for k in sorted(tot):
        if not tot[k]:
            continue
        v = [x[1] for x in tot[k]]
        print('  %d ganadora(s) que COLISIONAN: n = %-3d dist = %d/%d   semillas %s'
              % (k, len(v), int(sum(v)), len(v), [x[0] for x in tot[k]]))

    print()
    print('--- Lo mismo con el SUFIJO encendido (b6suf: direccion = bin x firma de 3 px): control ---')
    ncol = 0
    for s in sorted(dist):
        P = PATS(s)
        X, H = P[XNEG], P[BAR['neg']['H']]
        fx = tuple(int(X[q]) for q in VARPX)
        fh = tuple(int(H[q]) for q in VARPX)
        if fx == fh:
            ncol += 1
    print('  semillas donde la FIRMA de 3 px de X y H coincide (y el sufijo tampoco separaria): %d/%d'
          % (ncol, len(dist)))


if __name__ == '__main__':
    main()
