"""identidad_veto_muro.py — ARNES del confirmatorio TERMO + PATAS + VETO POR RESERVAS (un proceso; ANTES de mirar numeros). Salida ENTERA ->
identidad_veto_muro_salida.txt (o _largo.txt), escrita aqui mismo linea a linea.

MISION: llegar a la AGI por este camino.
  (K1) shas FIJADOS de todo lo que corre (corre_veto_muro.SHAS)
  (K2) TVPISO en disco == construye_veto_muro.todas() (por anclas desde TPATAS 1b6272ef4616af8b; NO escribe) y TPATAS en disco ==
       construye_patas.todas() (por anclas desde V143_TERMO 3db639cab75641fb)
  (K3) tpv, tv, vinv, pc son instancias de modulo DISTINTAS con las perillas del preregistro
  (a)  PERILLAS APAGADAS, salida ENTERA (N 9, fundador limpio): tpv y vinv con VETOP = 0 == TPATAS PATAS 3; tv con VETOP = 0 == V143_TERMO;
       los tres con VETOP = PATAS = 0 == V143_TERMO (s 53791 T 2000; y s 53792 T 5000 para tpv)
  (b)  CONTROLES QUE DEBEN DIFERIR: tpv, tv y vinv ACTUAN (vetos > 0) y su fisica != su base (tpv != pc, tv != termo, vinv != pc) y vinv != tpv;
       determinismo de tpv
  (c)  ENTRADA campo a campo (regla 14): corre_veto_muro.tarea == corre_v143.tarea (V143 y V143_TERMO) y tarea('pc') == corre_patas_muro.tarea('pc')
       (el pc de este bloque es el mismo pc de patas_muro), todo salvo 'seg' y lo agregado; imprime los campos comparados
  (d)  ESTADO por worker: tras correr tv, vinv y pc en el mismo proceso y ESTROPEAR a mano VETOP y PATAS de tpv (= 0), trabajo() de tpv re-fija
       PATAS 3 y VETOP 1, lo escribe en 'estado' y da lo mismo que una corrida limpia; --reanuda salta lo escrito
  (f)  LA PIEZA en casos sinteticos (sin pista): veneno s = (-0.4, 0) y sal s = (0, -0.4) con niveles fuera y dentro de la ventana, PISO y PISOINV
  (e)  --largo: corre_veto_muro.tarea('pc', 39201, T 100 000) == JSON de la ola 3 de dinamita (pc_s39201: linajes, pista, R0_pista)
Uso: python experimentos/organelos/veto_muro/identidad_veto_muro.py [--largo]
"""
import json, os, shutil, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_veto_muro as R
CV = R.CV; P = R.P
import construye_veto_muro as CVM
sys.path.insert(0, R.DINAD)
import construye_patas as CPT
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), 'patas_muro'))
import corre_patas_muro as RP          # SOLO se importa su tarea() para la regla 14 (no escribe nada, no corre sus semillas)
N = lambda x: json.loads(json.dumps(x, default=str))
SAL = open(os.path.join(AQUI, 'identidad_veto_muro_salida' + ('_largo' if '--largo' in sys.argv else '') + '.txt'), 'w', encoding='utf-8')


def out(s):
    print(s, flush=True); SAL.write(s + '\n'); SAL.flush()


def main():
    ok = True; t0 = time.time()

    def chk(nombre, cond):
        nonlocal ok; ok &= bool(cond); out(f"  {'OK   ' if cond else 'FALLA'} {nombre}")

    out(f"ARNES identidad_veto_muro · corre_veto_muro.py {R.h16(R.__file__)} · identidad_veto_muro.py {R.h16(os.path.abspath(__file__))} · "
        f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
    for ruta, sha in R.SHAS.items():
        s = R.h16(ruta); chk(f"(K1) sha {os.path.relpath(ruta, R.RAIZ)} {s} == {sha}", s == sha)
    b = CVM.todas()['TVPISO']
    chk(f"(K2) TVPISO en disco == construye_veto_muro.todas() (sha construido {CVM.h16b(b)}; no escribe)", open(R.TVPISO_PY, 'rb').read() == b)
    b2 = CPT.todas()['TPATAS']
    chk(f"(K2) TPATAS en disco == construye_patas.todas() (sha {CPT.h16b(b2)}) == origen fijado {CVM.SHA_TPATAS}",
        open(R.TPATAS_PY, 'rb').read() == b2 and CPT.h16b(b2) == CVM.SHA_TPATAS)
    M = {br: CV._MODS[R.fija(br)['carro']] for br in ('termo', 'pc') + R.VETO_BRAZOS}
    chk("(K3) tpv, tv, vinv, pc son instancias de modulo DISTINTAS; (PATAS, VETOP) = (3,1) (0,1) (3,2) y pc PATAS 3 sin VETOP",
        len({id(M[x]) for x in ('tpv', 'tv', 'vinv', 'pc')}) == 4
        and [(M[x].PATAS, M[x].VETOP) for x in R.VETO_BRAZOS] == [(3, 1), (0, 1), (3, 2)] and M['pc'].PATAS == 3 and not hasattr(M['pc'], 'VETOP')
        and all(os.path.abspath(M[x].__file__) == os.path.abspath(R.TVPISO_PY) for x in R.VETO_BRAZOS))
    run = lambda m, s, T: N(P.run(s, [('C', m)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1))
    s0, s1 = R.ARNES
    for s, T, brs in ((s0, 2000, R.VETO_BRAZOS), (s1, 5000, ('tpv',))):
        bt = run(M['termo'], s, T); bp = run(M['pc'], s, T)
        for br in brs:
            m = M[br]
            try:
                pv = m.PATAS; m.VETOP = 0; x = run(m, s, T)
                chk(f"(a) {br} con VETOP = 0 (PATAS {pv}) == {'TPATAS PATAS 3' if pv == 3 else 'V143_TERMO'}, salida ENTERA (N 9, s {s}, T {T})",
                    x == (bp if pv == 3 else bt))
                m.PATAS = 0; x = run(m, s, T)
                chk(f"(a) {br} con VETOP = 0 y PATAS = 0 == V143_TERMO, salida ENTERA (N 9, s {s}, T {T})", x == bt)
            finally:
                R.fija(br)
    fis = lambda r: {k: v for k, v in r.items() if k != 'linajes'} | {'linajes': [{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']]}
    base = {'tpv': run(M['pc'], s0, 2000), 'tv': run(M['termo'], s0, 2000), 'vinv': run(M['pc'], s0, 2000)}
    rr = {}
    for br in R.VETO_BRAZOS:
        r = rr[br] = run(M[br], s0, 2000)
        c = sum((d['carro'].get('vpiso') or {}).get('a_no', 0) for d in r['linajes'])
        dec = sum((d['carro'].get('vpiso') or {}).get('dec', 0) for d in r['linajes'])
        chk(f"(b) {br} (PATAS {M[br].PATAS}, VETOP {M[br].VETOP}) ACTUA: vetos {c} > 0 (de {dec} decisiones sobre lo sentido malo) y la fisica != su base "
            f"({'pc' if br != 'tv' else 'termo'}) (s {s0}, T 2000)", c > 0 and fis(r) != fis(base[br]))
    chk("(b) CONTROL: vinv != tpv en la fisica (s 53791, T 2000)", fis(rr['vinv']) != fis(rr['tpv']))
    chk("(b) determinismo: tpv dos corridas iguales (s 53791, T 2000)", run(M['tpv'], s0, 2000) == rr['tpv'])
    sin = lambda z, extra: N({k: v for k, v in z.items() if k not in ('seg',) + extra})

    def campo(nombre, x, y):
        ks = sorted(set(x) | set(y)); dif = [k for k in ks if x.get(k) != y.get(k)]
        chk(f"{nombre}: campos {ks} · difieren {dif}", not dif)
    campo("(c) ENTRADA campo a campo (regla 14): corre_veto_muro.tarea == corre_v143.tarea (V143, s 53791, T 2000)",
          sin(R.tarea((s0, 'v143', 2000)), ('tel_vm', 'estado')), sin(CV.tarea((s0, 'V143', 2000)), ()))
    campo("(c) ENTRADA campo a campo (regla 14): corre_veto_muro.tarea == corre_v143.tarea (V143_TERMO, s 53791, T 2000)",
          sin(R.tarea((s0, 'termo', 2000)), ('tel_vm', 'estado')), sin(CV.tarea((s0, 'V143_TERMO', 2000)), ()))
    x = R.tarea((s0, 'pc', 2000)); y = RP.tarea((s0, 'pc', 2000)); R.fija('pc')
    campo("(c) ENTRADA campo a campo: corre_veto_muro.tarea('pc') == corre_patas_muro.tarea('pc') (s 53791, T 2000)",
          sin(x, ('tel_vm', 'estado')), sin(y, ('tel_patas', 'estado')))
    chk("(c) telemetria de patas de pc identica en los dos runners y estado igual salvo VETOP",
        [t['patas'] for t in x['tel_vm']] == [t['patas'] for t in y['tel_patas']]
        and {k: v for k, v in x['estado'].items() if k != 'VETOP'} == y['estado'] and x['estado']['VETOP'] is None)
    tmp = tempfile.mkdtemp(prefix='veto_arnes_')
    try:
        limpio = R.trabajo((s0, 'tpv', 2000, tmp, False)); os.remove(os.path.join(tmp, f"tpv_s{s0}.json"))
        for br in ('tv', 'vinv', 'pc'): R.trabajo((s0, br, 2000, tmp, False))
        CV._MODS['TVPISO_31'].VETOP = 0; CV._MODS['TVPISO_31'].PATAS = 0      # se ESTROPEA a mano el estado del proceso
        z = R.trabajo((s0, 'tpv', 2000, tmp, False))
        chk("(d) ESTADO por worker: trabajo() re-fija PATAS 3 y VETOP 1 aunque el proceso los tenga en 0, lo escribe en 'estado' y da lo mismo que limpio",
            z['estado'] == dict(carro='TVPISO_31', sha=R.SHAS[R.TVPISO_PY], PATAS=3, VETOP=1, TERMO=1)
            and (CV._MODS['TVPISO_31'].PATAS, CV._MODS['TVPISO_31'].VETOP) == (3, 1) and sin(z, ()) == sin(limpio, ()))
        z2 = R.trabajo((s0, 'tpv', 2000, tmp, True))
        chk("(d) --reanuda salta el JSON ya escrito sin aborto (devuelve el guardado)", sin(z2, ()) == sin(z, ()))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # (f) la pieza sola, casos sinteticos (U = 1.0, PISO_V = 0.2). kk 'B' veneno (-0.4, 0), 'D' sal (0, -0.4), 'A' comida (0.8, 0)
    m = M['tpv']
    c = m.Carro.__new__(m.Carro); c._adS = {'B': [-0.8, 0.0, 2], 'D': [0.0, -1.2, 3], 'A': [1.6, 0.0, 2]}; c._vpU = 1.0
    c._vp = dict(dec=0, a_no=0, a_no_vent=0)
    casos = [  # (VETOP, letra, E, Ag, muerde_si_la_boca_quiere)
        (1, 'B', 0.9, 0.5, True),    # fuera de ventana: 0.9 - 0.4 = 0.5 >= 0.2 -> muerde (limpia pagando)
        (1, 'B', 0.5, 0.9, False),   # 0.5 - 0.4 = 0.1 < 0.2 -> veta (el hijo con hambre no se muerde el veneno)
        (1, 'B', 1.2, 1.1, False),   # ventana: 1.2 - 0.4 = 0.8 < 1.0 -> veta (no rompe la ventana de parto)
        (1, 'B', 1.45, 1.0, True),   # ventana: 1.45 - 0.4 = 1.05 >= 1.0 -> muerde
        (1, 'D', 0.5, 0.9, True),    # sal golpea Ag: 0.9 - 0.4 = 0.5 -> muerde
        (1, 'D', 0.9, 0.5, False),
        (1, 'A', 0.1, 0.1, True),    # lo bueno: la pieza no toca
        (2, 'B', 0.5, 0.9, True),    # PISOINV lee Ag para el veneno: 0.9 - 0.4 = 0.5 -> muerde (el control se equivoca a proposito)
        (2, 'B', 0.9, 0.5, False),
        (2, 'D', 0.9, 0.5, True),
    ]
    buenos = []
    try:
        for vp, k, E, Ag, esp in casos:
            m.VETOP = vp; r1 = c._vp_boca(k, E, Ag, True); r0 = c._vp_boca(k, E, Ag, False)
            buenos.append(r1 == esp and r0 is False)
            out(f"      VETOP {vp} letra {k} E {E} Ag {Ag}: boca quiere -> {r1} (esperado {esp}); boca no quiere -> {r0} (nunca fuerza)")
    finally:
        R.fija('tpv')
    chk(f"(f) la pieza en {len(casos)} casos sinteticos (PISO y PISOINV; solo quita, nunca fuerza)", all(buenos))
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
