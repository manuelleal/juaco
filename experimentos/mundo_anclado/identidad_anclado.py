"""identidad_anclado.py -- arnes de identidad BIT A BIT: organismo_f9c.run (ORIGEN, sin tocar) contra
organismo_anclado.run con las perillas APAGADAS, en los BRAZOS EXACTOS del bloque 2 (corre_bloque2.BRAZOS,
mismo objeto importado: regla 14 por identidad de objeto). Igualdad EXACTA del dict completo (floats con ==,
recursivo), no redondeada. Se corre ANTES de mirar ningun numero del mundo anclado.

  A. olv_mal=0, anc_mide=0          -> dict IDENTICO (mismas claves, mismos valores)
  B. olv_mal=0, anc_mide=1          -> claves viejas identicas + UNA clave nueva 'anclado'
  C. ERR-38 (la perilla no es inerte): olv_mal>0 cambia la corrida; olv_ciego=1 la cambia distinto;
     con olv_mal>0 la presencia media de lo malo BAJA frente a olv_mal=0 (mismo brazo y semilla).

    python experimentos/mundo_anclado/identidad_anclado.py   (UN proceso; escribe identidad_anclado_salida.txt)
"""
import os
import sys
import time
import hashlib

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N09B2 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo_b2')
sys.path[:0] = [N09B2]
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import corre_bloque2 as B2          # inserta sus propias rutas (organismo/ primero, ERR-28)
import organismo_f9c as F9C_ORIG
sys.path.insert(0, AQUI)
import organismo_anclado as ANC

SALIDA = os.path.join(AQUI, 'identidad_anclado_salida.txt')
LINEAS = []


def out(s=''):
    print(s, flush=True)
    LINEAS.append(s)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def igual(a, b, ruta='', difs=None):
    """Igualdad EXACTA recursiva. Devuelve la lista de rutas que difieren."""
    if difs is None:
        difs = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                difs.append(f"{ruta}/{k}(falta)")
            else:
                igual(a[k], b[k], f"{ruta}/{k}", difs)
    elif isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b) or type(a) is not type(b):
            difs.append(f"{ruta}(len/tipo)")
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                igual(x, y, f"{ruta}[{i}]", difs)
    else:
        if type(a) is not type(b):
            difs.append(f"{ruta}(tipo {type(a).__name__}!={type(b).__name__})")
        elif a != a and b != b:   # nan == nan
            pass
        elif a != b:
            difs.append(ruta)
    return difs


def fmala(r):
    p = r['anclado']['pres']; tot = sum(p.values())
    return (p.get('B', 0) + p.get('D', 0)) / tot if tot else None


def main():
    T = 20000
    out(f"IDENTIDAD ANCLADO · organismo_f9c (sha {h16(os.path.join(N09B2, 'organismo_f9c.py'))}) vs organismo_anclado "
        f"(sha {h16(os.path.join(AQUI, 'organismo_anclado.py'))}) · brazos = corre_bloque2.BRAZOS · T={T}")
    t0 = time.time(); ok_total = True
    casos = [('NADA', 1, 0), ('NADA', 2, 0), ('NADA', 1, 1), ('REL', 1, 0), ('REL', 2, 1), ('ORACULO', 1, 0),
             ('ORACULO', 2, 1), ('REL_BAR', 1, 0), ('RENACE', 1, 0), ('RENACE', 1, 1)]
    out("A. perillas apagadas (olv_mal=0, anc_mide=0): dict completo identico")
    for brazo, s, acum in casos:
        kw = dict(B2.BRAZOS[brazo], rep_acum=acum)
        a = F9C_ORIG.run(s, T=T, **kw); b = ANC.run(s, T=T, **kw)
        d = igual(a, b); ok = not d; ok_total &= ok
        out(f"  {'OK  ' if ok else 'FALLA'} {brazo:8s} s{s} acum={acum}  claves={len(a)}  difs={d[:4]}  muertes={a['deaths']} desc={a.get('descendientes')}")
    out("B. solo medida (anc_mide=1): claves viejas identicas + una clave nueva 'anclado'")
    for brazo, s, acum in [('NADA', 1, 0), ('ORACULO', 1, 0), ('RENACE', 1, 1)]:
        kw = dict(B2.BRAZOS[brazo], rep_acum=acum)
        a = F9C_ORIG.run(s, T=T, **kw); b = ANC.run(s, T=T, anc_mide=1, **kw)
        extra = sorted(set(b) - set(a)); bb = {k: v for k, v in b.items() if k != 'anclado'}
        d = igual(a, bb); ok = (not d) and extra == ['anclado'] and b['anclado']['pasos'] == T; ok_total &= ok
        out(f"  {'OK  ' if ok else 'FALLA'} {brazo:8s} s{s} acum={acum}  extra={extra}  difs={d[:4]}  pasos={b['anclado']['pasos']}")
    out("A'. T=100000 (ORACULO s1 acum=0), perillas apagadas")
    kw = dict(B2.BRAZOS['ORACULO'], rep_acum=0)
    a = F9C_ORIG.run(1, T=100000, **kw); b = ANC.run(1, T=100000, **kw)
    d = igual(a, b); ok = not d; ok_total &= ok
    out(f"  {'OK  ' if ok else 'FALLA'} ORACULO  s1 T=100000  difs={d[:4]}  muertes={a['deaths']} desc={a['descendientes']}")
    out("C. ERR-38: la perilla NO es inerte (NADA s1, T=20000, olv_mal=0.004)")
    kw = dict(B2.BRAZOS['NADA'], rep_acum=0)
    r0 = ANC.run(1, T=T, anc_mide=1, **kw)
    r1 = ANC.run(1, T=T, anc_mide=1, olv_mal=0.004, **kw)
    r2 = ANC.run(1, T=T, anc_mide=1, olv_mal=0.004, olv_ciego=1, **kw)
    c1 = bool(igual({k: v for k, v in r0.items() if k != 'anclado'}, {k: v for k, v in r1.items() if k != 'anclado'}))
    c2 = bool(igual({k: v for k, v in r1.items() if k != 'anclado'}, {k: v for k, v in r2.items() if k != 'anclado'}))
    c3 = fmala(r1) < fmala(r0)
    c4 = set(r1['anclado']['rem']) <= {'B', 'D'} and r1['anclado']['eventos'] > 0
    c5 = r2['anclado']['eventos'] > 0 and any(k in r2['anclado']['rem'] for k in ('A', 'C'))
    for nom, v in [('olv_mal cambia la corrida', c1), ('ciego != selectiva', c2),
                   (f"f_mala baja con la dilucion ({fmala(r0):.3f} -> {fmala(r1):.3f}); ciego {fmala(r2):.3f}", c3),
                   (f"selectiva solo quita B/D: rem={r1['anclado']['rem']}", c4),
                   (f"ciego quita tambien A/C: rem={r2['anclado']['rem']}", c5)]:
        ok_total &= v
        out(f"  {'OK  ' if v else 'FALLA'} {nom}")
    out(f"\n{'TODO PASA' if ok_total else 'ALGO FALLA'} en {time.time() - t0:.1f}s")
    with open(SALIDA, 'w', encoding='utf-8') as f:
        f.write('\n'.join(LINEAS) + '\n')
    return 0 if ok_total else 1


if __name__ == '__main__':
    sys.exit(main())
