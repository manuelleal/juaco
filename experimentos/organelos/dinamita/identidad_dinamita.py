"""identidad_dinamita.py — ARNES del bloque DINAMITA (un proceso; ANTES de mirar numeros). Salida -> identidad_dinamita_salida.txt.

MISION: llegar a la AGI por este camino.
  (K) construye_dinamita --verifica: carros en disco == construidos por anclas desde termo/carros/V143_TERMO.py (sha 3db639cab75641fb)
  (a) TVETO con VETO = 0 == V143_TERMO, salida ENTERA (N 9, fundador limpio; s 39921 T 2000 y s 39922 T 5000)
  (b) cada modo VETO 1..5 ACTUA (telemetria a_no > 0) y cambia la fisica respecto de TERMO (s 39921 T 5000); determinismo
  (c) ENTRADA campo a campo (regla 14): explora_dinamita.tarea == corre_v143.tarea (TERMO, s 39921 T 2000), salvo 'seg' y lo agregado
  (d) --largo: explora_dinamita.tarea('termo', 39101, T 100000) reproduce los linajes del JSON confirmatorio de TERMO (serie 39101) bit
      a bit (todo salvo 'seg'): el runner exploratorio ES el de la serie
Uso: python experimentos/organelos/dinamita/identidad_dinamita.py [--largo]
"""
import glob, json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import construye_dinamita as CD
import construye_patas as CPT
import explora_dinamita as ED
CV = ED.CV; P = ED.P
N = lambda x: json.loads(json.dumps(x, default=str))


def sin(r, claves):
    out = dict(r); out['linajes'] = [{k: v for k, v in d.items() if k not in claves} for d in r['linajes']]; return out


def main():
    ok = True; t0 = time.time()

    def chk(nombre, cond):
        nonlocal ok; ok &= bool(cond); print(f"  {'OK   ' if cond else 'FALLA'} {nombre}", flush=True)

    chk("(K) construye_dinamita --verifica (TVETO == anclas desde V143_TERMO 3db639cab75641fb)", CD.main(['--verifica']) == 0)
    chk("(K) construye_patas --verifica (TPATAS == anclas desde V143_TERMO 3db639cab75641fb)", CPT.main(['--verifica']) == 0)
    TM = CV._MODS[ED.registra('termo')]
    MV = {b: CV._MODS[ED.registra(b)] for b in list(ED.VETOS) + list(ED.PATASB)}
    AT = lambda b: 'VETO' if b in ED.VETOS else 'PATAS'
    run = lambda m, s, T: N(P.run(s, [('C', m)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1))
    for s, T in ((39921, 2000), (39922, 5000)):
        base = run(TM, s, T)
        for b, m in MV.items():
            g = getattr(m, AT(b))
            try:
                setattr(m, AT(b), 0); x = run(m, s, T)
            finally:
                setattr(m, AT(b), g)
            chk(f"(a) {b} con {AT(b)} = 0 == V143_TERMO, salida ENTERA (N 9, s {s}, T {T}, fundador limpio)", x == base)
    fis = lambda r: sin(r, ('carro',))
    bt = run(TM, 39921, 5000)
    for b, m in MV.items():
        r = run(m, 39921, 5000)
        tel = [d['carro'].get('veto') or d['carro'].get('patas') or {} for d in r['linajes']]
        a_no = sum(t.get('a_no', 0) + t.get('a_si', 0) + t.get('cambia', 0) for t in tel); obst = sum(t.get('obst', 0) for t in tel)
        chk(f"(b) {b} ({AT(b)} {getattr(m, AT(b))}) ACTUA: cambios {a_no} obst {obst} > 0 y la fisica != TERMO (s 39921, T 5000)",
            (a_no + obst) > 0 and fis(r) != fis(bt))
        if b in ('vu', 'pu'): chk(f"(b) determinismo: {b} dos corridas iguales (s 39921, T 5000)", run(m, 39921, 5000) == r)
    x = ED.tarea(39921, 'termo', 2000); y = CV.tarea((39921, 'V143_TERMO', 2000))
    for k in ('tel_dinamita', 'brazo', 'T'): x.pop(k, None)
    y.pop('pizarra_log', None)
    e14 = N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in y.items() if k != 'seg'})
    chk("(c) ENTRADA campo a campo (regla 14): explora_dinamita.tarea == corre_v143.tarea (TERMO, s 39921, T 2000)", e14)
    if '--largo' in sys.argv:
        ref = glob.glob(os.path.join(os.path.dirname(AQUI), 'termo', 'datos', 'termo_s39101-39120_T100000_*', 'termo_s39101.json'))
        d0 = json.load(open(ref[0], encoding='utf-8'))
        z = N(ED.tarea(39101, 'termo', 100000))
        igual = z['linajes'] == d0['linajes'] and z['pista'] == d0['pista'] and z['R0_pista'] == d0['R0_pista']
        chk(f"(d) --largo: termo s39101 T 100000 == JSON confirmatorio de la serie TERMO (linajes, pista, R0_pista) [{os.path.basename(os.path.dirname(ref[0]))}]", igual)
    print(f"ARNES {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
