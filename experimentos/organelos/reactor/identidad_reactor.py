"""identidad_reactor.py — ARNES de la sonda del Reactor (1-oct-2026). Un proceso, sin Pool.

(K) shas de lo importado. (I) la envoltura sonda_reactor.corre_reactor a esc 90, n0 90, tope 3000 (el MUNDO original de BLOQUES) con
los ganchos de telemetria PUESTOS reproduce corre_bloques.corre() a la misma semilla: el JSON M_* (lo que escribe corre_bloques) y el
JSON del nucleo (tam_total, gen_t, vivos_final, ...) son iguales campo a campo salvo 'seg' (reloj de pared). (C) el comparador
detecta una diferencia (control que debe fallar: el mismo dict con un campo cambiado). (G) los ganchos se llamaron (hijo y fund > 0)
y el espejo del banco no se desincronizo. (M) MUNDO queda restaurado.
Uso: python identidad_reactor.py [--T 200000] [--semilla 49701]
"""
import argparse, hashlib, json, os, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import sonda_reactor as SR   # noqa: E402

CB = SR.CB; NS = SR.NS
OK = [0, 0]


def chk(nombre, cond, extra=''):
    OK[1] += 1; OK[0] += int(bool(cond))
    print(f"  [{'PASA' if cond else 'FALLA'}] {nombre} {extra}", flush=True)


def canon(d, fuera=('seg',)):
    return hashlib.sha256(json.dumps({k: v for k, v in d.items() if k not in fuera}, sort_keys=True).encode()).hexdigest()[:16]


def difs(a, b, fuera=('seg',)):
    return sorted(k for k in set(a) | set(b) if k not in fuera and json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True))


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--T', type=int, default=200000); ap.add_argument('--semilla', type=int, default=49701)
    ap.add_argument('--brazo', default='BLOQ_V')
    a, resto = ap.parse_known_args()
    if resto: raise SystemExit(f'banderas desconocidas: {resto}')
    T = a.T; s = a.semilla; br = a.brazo
    print(f"identidad_reactor · {time.strftime('%Y-%m-%d %H:%M:%S')} · semilla {s} · brazo {br} · T {T}")
    print('(K) shas')
    SR.verifica()
    for p, h in list(CB.SHAS.items()) + list(SR.SHAS.items()): chk(os.path.basename(p), SR.h16(p) == h, h)
    print(f"      sonda_reactor.py {SR.h16(os.path.join(AQUI, 'sonda_reactor.py'))} · identidad_reactor.py {SR.h16(os.path.abspath(__file__))}")
    m0 = dict(NS.MUNDO)
    print(f'      MUNDO original: {m0}')
    chk('MUNDO original de BLOQUES es esc 90, n0 90, tope 3000', (m0['esc'], m0['n0'], m0['tope']) == (90, 90, 3000))
    cA = os.path.join(SR.DATOS, 'arnes', 'A_corre_bloques'); cB = os.path.join(SR.DATOS, 'arnes', 'B_envoltura')
    print('(I) corre_bloques.corre() [A] == sonda_reactor.corre_reactor(esc 90, n0 90, tope 3000, ganchos puestos) [B]')
    t0 = time.time(); oA = CB.corre(s, br, T, cA); tA = time.time() - t0
    nA = json.load(open(os.path.join(cA, f'{br}_s{s}.json'), encoding='utf-8'))
    t0 = time.time(); oB, R = SR.corre_reactor(s, br, T, 90, 90, cB, tope=3000); tB = time.time() - t0
    nB = json.load(open(os.path.join(cB, f'{br}_s{s}.json'), encoding='utf-8'))
    mA = json.load(open(os.path.join(cA, f'M_{br}_s{s}.json'), encoding='utf-8'))
    mB = json.load(open(os.path.join(cB, f'M_{br}_s{s}.json'), encoding='utf-8'))
    print(f"      A {tA:.1f} s · B {tB:.1f} s · A: K {oA['K']} persiste {oA['persiste']} n_nac {oA['n_nac']} vivos_T {nA.get('vivos_T')}")
    chk('M_*.json igual (todas las claves menos seg)', canon(mA) == canon(mB), f'{canon(mA)} / {canon(mB)} dif {difs(mA, mB)} · {len(mA)} claves')
    chk('JSON del nucleo igual (todas las claves menos seg)', canon(nA) == canon(nB), f'{canon(nA)} / {canon(nB)} dif {difs(nA, nB)} · {len(nA)} claves')
    chk('la corrida no es trivial (hubo nacimientos, reglas y vivos al final)', (oA['n_nac'] or 0) > 100 and bool(oA['bloques']['vivos_T'])
        and oA['bloques']['n_ins'] > 0, f"n_nac {oA['n_nac']} ins {oA['bloques']['n_ins']} vivos {len(oA['bloques']['vivos_T'])}")
    print('(C) control que debe fallar: el comparador ve un cambio de un campo')
    mC = json.loads(json.dumps(mB)); mC['K'] = (mC['K'] or 0) + 1e-9
    chk('K + 1e-9 -> distinto', canon(mA) != canon(mC) and difs(mA, mC) == ['K'])
    nC = json.loads(json.dumps(nB)); nC['tam_total'][-1] += 1
    chk('tam_total[-1] + 1 -> distinto', canon(nA) != canon(nC) and difs(nA, nC) == ['tam_total'])
    print('(G) ganchos')
    g = R['ganchos']
    chk('gancho de parto llamado == n_hijos del motor', g['hijo'] == oB['bloques']['n_hijos'] and g['hijo'] > 0, f"{g['hijo']} / {oB['bloques']['n_hijos']}")
    chk('gancho de fundador llamado == n_fund del motor', g['fund'] == oB['bloques']['n_fund'] and g['fund'] > 0, f"{g['fund']} / {oB['bloques']['n_fund']}")
    chk('espejo del banco sincronizado', g['desinc'] == 0, str(g['desinc']))
    rj = R['relojes']
    chk('genealogia completa (ninguna fila faltante en la ascendencia)', rj['sin_fila'] == 0, f"sin_fila {rj['sin_fila']} de {rj['n_cuerpos']} cuerpos")
    evs = sum(SR.TEL['EV'].values()); ops = sum(oB['bloques'][k] for k in ('n_campo', 'n_dup', 'n_del', 'n_ins', 'n_hgt'))
    chk('eventos contados por los ganchos == operadores del motor', evs == ops, f'{evs} / {ops}')
    print('(M) MUNDO restaurado')
    chk('MUNDO == original', dict(NS.MUNDO) == m0)
    print(SR.linea(R))
    print(f"RESULTADO: {OK[0]}/{OK[1]} {'PASA' if OK[0] == OK[1] else 'FALLA'}")


if __name__ == '__main__':
    main()
