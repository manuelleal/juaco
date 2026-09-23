"""EXPLORATORIO, no es dato. (1) Pareado SOLA vs SABIA por semilla (t85 y acierto primeros 100).
(2) Sabia que se va TEMPRANO (a los 50, 100, 200 ensayos): examen sin sabia al irse vs SOLA al mismo ensayo.
Uso: python extra.py [--bits]"""
import sys, json, os
import escuela as E

E.TAREA = 'BITS' if '--bits' in sys.argv else 'CLASES'
SEM = list(range(7001, 7031))
L = ['EXPLORATORIO, no es dato. TAREA=%s, 30 semillas 7001-7030' % E.TAREA]


def q(x):
    x = sorted(x)
    return '%s [%s-%s]' % (x[len(x) // 2], x[len(x) // 4], x[3 * len(x) // 4])


for regla in ['RW', 'IND', 'LIN']:
    so = [E.corre(regla, 'SOLA', s) for s in SEM]
    sa = [E.corre(regla, 'SABIA', s) for s in SEM]
    BIG = 10 ** 6
    ts = [r['t90'] if r['t90'] is not None else BIG for r in so]
    ta = [r['t90'] if r['t90'] is not None else BIG for r in sa]
    gana = sum(1 for x, y in zip(ts, ta) if y < x)
    empata = sum(1 for x, y in zip(ts, ta) if y == x)
    L.append('%-4s t85 SOLA mediana[IQR]=%s  SABIA=%s  sabia mas rapida en %d/30 (empates %d)' % (
        regla, q(ts), q(ta), gana, empata))
    b1s = sum(r['bloques'][0] for r in so) / 30
    b1a = sum(r['bloques'][0] for r in sa) / 30
    L.append('     acierto primeros 100: SOLA=%.2f SABIA=%.2f' % (b1s, b1a))
    for ret in [50, 100, 200]:
        rr = [E.corre(regla, 'SABIA_RETIRO', s, N=ret + 1, retiro=ret) for s in SEM]
        # SOLA examinada en el mismo ensayo: corre N=ret y examina al final
        ss = [E.corre(regla, 'SOLA', s, N=ret) for s in SEM]
        ex_r = sum(sum(r['examen_retiro'].values()) / 4 for r in rr) / 30
        ex_s = sum(sum(r['examen_final'].values()) / 4 for r in ss) / 30
        L.append('     sabia se va en ensayo %3d: examen sin sabia EX-ALUMNA=%.2f  vs SOLA mismo ensayo=%.2f' % (ret, ex_r, ex_s))
txt = '\n'.join(L)
print(txt)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'extra_%s.txt' % E.TAREA), 'w', encoding='utf-8') as fh:
    fh.write(txt + '\n')
