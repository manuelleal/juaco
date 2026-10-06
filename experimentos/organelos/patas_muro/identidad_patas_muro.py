"""identidad_patas_muro.py — ARNES del confirmatorio TERMO + PATAS (un proceso; ANTES de mirar numeros). Salida ENTERA ->
identidad_patas_muro_salida.txt (se escribe aqui mismo, linea a linea).

MISION: llegar a la AGI por este camino.
  (K1) shas FIJADOS de todo lo que corre (corre_patas_muro.SHAS) y los carros REUSADOS de dinamita/termo por sha
  (K2) TPATAS en disco == construye_patas.todas() (por anclas desde V143_TERMO 3db639cab75641fb; NO escribe) y su sha == el que el arnes
       de la ola 3 de dinamita dejo escrito (identidad_dinamita_salida_ola3.txt)
  (a)  pc, pu, pd, pi con PATAS = 0 == V143_TERMO, salida ENTERA (N 9, fundador limpio; s 52691 T 2000 los cuatro; s 52692 T 5000 pc)
  (b)  pc, pu, pd, pi ACTUAN (telemetria 'cambia' > 0) y la fisica != TERMO (s 52691, T 2000); determinismo de pc
  (c)  ENTRADA campo a campo (regla 14): corre_patas_muro.tarea == corre_v143.tarea (V143 y V143_TERMO, s 52691, T 2000) y
       == explora_dinamita.tarea para pc (el runner confirmatorio corre lo mismo que la ola 3), todo salvo 'seg' y lo agregado
  (d)  ESTADO por worker: tras correr pi, pu y pd en el mismo proceso y ESTROPEAR a mano PATAS de pc (= 0), trabajo() de pc re-fija PATAS 3,
       lo escribe en 'estado' y da lo mismo que una corrida limpia de pc
  (e)  --largo: corre_patas_muro.tarea('pc', 39201, T 100 000) == JSON de la ola 3 de dinamita (pc_s39201: linajes, pista, R0_pista)
Uso: python experimentos/organelos/patas_muro/identidad_patas_muro.py [--largo]
"""
import json, os, shutil, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_patas_muro as R
CV = R.CV; P = R.P
sys.path.insert(0, R.DINAD)
import construye_patas as CPT
import explora_dinamita as ED
N = lambda x: json.loads(json.dumps(x, default=str))
SAL = open(os.path.join(AQUI, 'identidad_patas_muro_salida' + ('_largo' if '--largo' in sys.argv else '') + '.txt'), 'w', encoding='utf-8')


def out(s):
    print(s, flush=True); SAL.write(s + '\n'); SAL.flush()


def main():
    ok = True; t0 = time.time()

    def chk(nombre, cond):
        nonlocal ok; ok &= bool(cond); out(f"  {'OK   ' if cond else 'FALLA'} {nombre}")

    out(f"ARNES identidad_patas_muro · corre_patas_muro.py {R.h16(R.__file__)} · identidad_patas_muro.py {R.h16(os.path.abspath(__file__))} · "
        f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
    for ruta, sha in R.SHAS.items():
        s = R.h16(ruta); chk(f"(K1) sha {os.path.relpath(ruta, R.RAIZ)} {s} == {sha}", s == sha)
    b = CPT.todas()['TPATAS']
    chk(f"(K2) TPATAS en disco == construye_patas.todas() (sha construido {CPT.h16b(b)}; no escribe)", open(R.TPATAS_PY, 'rb').read() == b)
    ola3 = open(os.path.join(R.DINAD, 'identidad_dinamita_salida_ola3.txt'), encoding='utf-8').read()
    chk("(K2) sha TPATAS == el del arnes de la ola 3 de dinamita ('TPATAS sha 1b6272ef4616af8b == disco: True')",
        'TPATAS sha 1b6272ef4616af8b == disco: True' in ola3 and R.SHAS[R.TPATAS_PY] == '1b6272ef4616af8b')
    M = {br: CV._MODS[R.fija(br)['carro']] for br in ('termo',) + R.PATAS_BRAZOS}
    chk("(K3) pc, pu, pd, pi son instancias de modulo DISTINTAS del mismo archivo, con PATAS 3/2/1/4",
        len({id(M[x]) for x in R.PATAS_BRAZOS}) == 4 and [M[x].PATAS for x in R.PATAS_BRAZOS] == [3, 2, 1, 4]
        and all(os.path.abspath(M[x].__file__) == os.path.abspath(R.TPATAS_PY) for x in R.PATAS_BRAZOS))
    run = lambda m, s, T: N(P.run(s, [('C', m)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1))
    s0, s1 = R.ARNES
    for s, T, brs in ((s0, 2000, R.PATAS_BRAZOS), (s1, 5000, ('pc',))):
        base = run(M['termo'], s, T)
        for br in brs:
            m = M[br]
            try:
                m.PATAS = 0; x = run(m, s, T)
            finally:
                R.fija(br)
            chk(f"(a) {br} con PATAS = 0 == V143_TERMO, salida ENTERA (N 9, s {s}, T {T}, fundador limpio)", x == base)
    fis = lambda r: {k: v for k, v in r.items() if k != 'linajes'} | {'linajes': [{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']]}
    bt = run(M['termo'], s0, 2000)
    for br in R.PATAS_BRAZOS:
        r = run(M[br], s0, 2000)
        c = sum((d['carro'].get('patas') or {}).get('cambia', 0) for d in r['linajes'])
        chk(f"(b) {br} (PATAS {M[br].PATAS}) ACTUA: cambios de paso {c} > 0 y la fisica != TERMO (s {s0}, T 2000)", c > 0 and fis(r) != fis(bt))
        if br == 'pc': chk("(b) determinismo: pc dos corridas iguales (s 52691, T 2000)", run(M['pc'], s0, 2000) == r)
    sin = lambda z, extra: N({k: v for k, v in z.items() if k not in ('seg',) + extra})
    x = R.tarea((s0, 'v143', 2000)); y = CV.tarea((s0, 'V143', 2000))
    chk("(c) ENTRADA campo a campo (regla 14): corre_patas_muro.tarea == corre_v143.tarea (V143, s 52691, T 2000)",
        sin(x, ('tel_patas', 'estado')) == sin(y, ()))
    x = R.tarea((s0, 'termo', 2000)); y = CV.tarea((s0, 'V143_TERMO', 2000))
    chk("(c) ENTRADA campo a campo (regla 14): corre_patas_muro.tarea == corre_v143.tarea (V143_TERMO, s 52691, T 2000)",
        sin(x, ('tel_patas', 'estado')) == sin(y, ()))
    x = R.tarea((s0, 'pc', 2000)); y = ED.tarea(s0, 'pc', 2000); R.fija('pc')
    chk("(c) corre_patas_muro.tarea('pc') == explora_dinamita.tarea('pc') de la ola 3 (s 52691, T 2000; linajes, pista, R0_pista, tel)",
        sin(x, ('tel_patas', 'estado', 'pizarra_log')) == sin(y, ('tel_dinamita', 'brazo', 'T'))   # explora_dinamita quita pizarra_log
        and [t['patas'] for t in x['tel_patas']] == [t['patas'] for t in y['tel_dinamita']])
    tmp = tempfile.mkdtemp(prefix='patas_arnes_')
    try:
        limpio = R.trabajo((s0, 'pc', 2000, tmp, False)); os.remove(os.path.join(tmp, f"pc_s{s0}.json"))
        R.trabajo((s0, 'pi', 2000, tmp, False)); R.trabajo((s0, 'pu', 2000, tmp, False)); R.trabajo((s0, 'pd', 2000, tmp, False))
        CV._MODS['TPATAS_3'].PATAS = 0           # se ESTROPEA a mano el estado del proceso
        z = R.trabajo((s0, 'pc', 2000, tmp, False))
        chk("(d) ESTADO por worker: trabajo() re-fija PATAS 3 aunque el proceso lo tenga en 0, lo escribe en 'estado' y da lo mismo que limpio",
            z['estado'] == dict(carro='TPATAS_3', sha='1b6272ef4616af8b', PATAS=3, TERMO=1) and CV._MODS['TPATAS_3'].PATAS == 3
            and sin(z, ()) == sin(limpio, ()))
        z2 = R.trabajo((s0, 'pc', 2000, tmp, True))
        chk("(d) --reanuda salta el JSON ya escrito sin aborto (devuelve el guardado)", sin(z2, ()) == sin(z, ()))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if '--largo' in sys.argv:
        ref = os.path.join(R.DINAD, 'datos', 'explora', 'pc_s39201_T100000.json')
        d0 = json.load(open(ref, encoding='utf-8'))
        z = N(R.tarea((39201, 'pc', 100000)))
        chk("(e) --largo: pc s39201 T 100000 == JSON de la ola 3 de dinamita (linajes, pista, R0_pista) [pc_s39201_T100000.json]",
            z['linajes'] == d0['linajes'] and z['pista'] == d0['pista'] and z['R0_pista'] == d0['R0_pista'])
    out(f"ARNES {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
