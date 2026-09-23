"""identidad_n9b.py — ARNES de identidad de subida_n9b (se corre ANTES de mirar cualquier numero de las lesiones).

MISION: llegar a la AGI por este camino.
Verifica: shas de origen; construccion por anclas reproducible; chequeo estatico; identidad corta del juez; APR (copia) con
OPCION 0 == FABRICA; APR_LES_OFF == APR BIT A BIT en toda la salida de pista.run (N 9, dos semillas); con ALFA_Q = 0 las tres
lesiones == APR (la lesion solo entra por lo aprendido); lesiones NO inertes con Q aprendido y cada una toca solo lo suyo;
determinismo; entrada del runner campo a campo (regla 14); mini identidad del runner; el parser del runner ABORTA ante
banderas desconocidas / abreviadas / con '=' / --help (ERR-115) sin correr nada.
Semillas del arnes: 13592-13594 (mini del runner 13599). Salida: identidad_n9b_salida.txt.
Uso: python experimentos/subida_n9b/identidad_n9b.py   (aborta ante cualquier argumento)
"""
import io, json, os, sys, time, contextlib

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun_n9b as K   # noqa: E402
import corre_n9b as CR  # noqa: E402
P, J, RC = K.P, K.J, K.RC
KW = dict(pizarra=1, rep_acum=0, escala=1, mundo_n=None)


def main():
    if len(sys.argv) > 1: raise SystemExit(f"identidad_n9b.py no acepta argumentos: {sys.argv[1:]}")
    out = open(os.path.join(AQUI, 'identidad_n9b_salida.txt'), 'w', encoding='utf-8'); t0 = time.time(); r = []

    def log(s=''):
        print(s, flush=True); out.write(s + '\n'); out.flush()

    def chk(nombre, cond, det=''):
        r.append(bool(cond)); log(f"  [{'OK ' if cond else 'FALLA'}] {nombre}" + (f" · {det}" if det else ''))

    log(f"IDENTIDAD_N9B · {time.strftime('%Y-%m-%d %H:%M:%S')} · identidad_n9b.py {K.h16(os.path.abspath(__file__))} · corre_n9b.py {K.h16(CR.__file__)}")
    log("(0) shas de origen")
    for ru, m, f, ok in K.verifica_shas(): chk(f"sha {ru}", ok, f"{m} (fijado {f})")
    log("(1) construccion por anclas")
    esp, med, ok = K.verifica_construccion(); chk("carros en disco == construye_n9b.construye()", ok, str(med))
    chk("APR copia verbatim (mismo sha que el origen)", med['APR'] == '4402aa5142065c72' and med['FABRICA'] == '2ebee3e99ea5a33a')
    log("(2) chequeo estatico (revisa_carro de la carrera)")
    for c in ('APR', 'FABRICA', 'APR_LES_OFF', 'APR_LES_PLANA', 'APR_LES_CRUZ', 'APR_LES_MUNDO'):
        v = RC.revisa(c); chk(f"revisa {c}", not v, 'PASA' if not v else str(v[:3]))
    log("(3) identidad corta del juez")
    ide = J.identidad_corta(); chk("FABRICA solo == organismo_f9c REL (s 1, T 5000)", ide['ok'], f"dif {ide['dif'][:3]}")
    log("(4) APR (copia) con OPCION 0 == FABRICA (N 9, s 13592, T 3000)")
    m0 = P.carga_carro('APR'); m0.OPCION = 0
    a = P.run(13592, [('C', P.carga_carro('FABRICA'))] * 9, T=3000, **KW); b = P.run(13592, [('C', m0)] * 9, T=3000, **KW)
    chk("APR OPCION 0 == FABRICA en toda la salida", K.normaliza(a) == K.normaliza(b))
    log("(5) APR_LES_OFF == APR BIT A BIT (toda la salida de pista.run, N 9, T 8000)")
    for sd in (13592, 13593):
        a = P.run(sd, ['APR'] * 9, T=8000, **KW); b = P.run(sd, ['APR_LES_OFF'] * 9, T=8000, **KW)
        opp = sum(sum(x['carro']['apr']['opp_q']) for x in a['linajes'])
        chk(f"s {sd}: APR_LES_OFF == APR", K.normaliza(a) == K.normaliza(b, 'APR_LES_OFF'),
            f"decisiones de la opcion {opp} · sin clave 'lesion' en OFF: {all('lesion' not in x['carro']['apr'] for x in b['linajes'])}")
    log("(6) con ALFA_Q = 0 (Q no aprende) las tres lesiones == APR: la lesion solo entra por lo aprendido")
    def con_alfa0(ident):
        m = P.carga_carro(ident); m.ALFA_Q = 0.0; return m
    # los contadores de telemetria que se AGRUPAN por post o por g0 (rasgos lesionados) se excluyen de la comparacion;
    # la fisica, las decisiones, el rng y el resto de la salida tienen que ser identicos.
    POR_RASGO = ('opp_post', 'mord_post', 'opp_g0', 'mord_g0', 'anad_g0', 'quit_g0', 'lesion')
    def sin_rasgo(x):
        for d in x['linajes']:
            for k in POR_RASGO: d['carro']['apr'].pop(k, None)
        return K.normaliza(x)
    base = P.run(13594, [('C', con_alfa0('APR'))] * 9, T=4000, **KW); nb = sin_rasgo(base)
    for les in ('APR_LES_PLANA', 'APR_LES_CRUZ', 'APR_LES_MUNDO'):
        x = P.run(13594, [('C', con_alfa0(les))] * 9, T=4000, **KW)
        chk(f"ALFA_Q 0: {les} == APR (sin los contadores agrupados por el rasgo lesionado)", sin_rasgo(x) == nb)
    log("(7) lesiones NO inertes con Q aprendido (s 13594, T 8000) y cada una toca SOLO lo suyo")
    a = P.run(13594, ['APR'] * 9, T=8000, **KW); na = K.normaliza(a)
    for les, toca in (('APR_LES_PLANA', 'post'), ('APR_LES_CRUZ', 'post'), ('APR_LES_MUNDO', 'mundo')):
        x = P.run(13594, [les] * 9, T=8000, **KW)
        ls = [d['carro']['apr']['lesion'] for d in x['linajes']]; n = sum(s['n'] for s in ls)
        cp = sum(s['cambia_post'] for s in ls); cmu = sum(s['cambia_mundo'] for s in ls)
        pr = sum(s['post_real'] for s in ls) / max(1, n); pu = sum(s['post_usado'] for s in ls) / max(1, n)
        solo = (cp > 0 and cmu == 0) if toca == 'post' else (cmu > 0 and cp == 0)
        chk(f"{les} difiere de APR y toca solo '{toca}'", K.normaliza(x, les) != na and solo,
            f"decisiones {n} · cambia post {cp} ({cp/max(1,n):.3f}) · cambia mundo {cmu} ({cmu/max(1,n):.3f}) · post real {pr:.3f} / usado {pu:.3f} "
            f"· caida real {sum(s['caida_real'] for s in ls)/max(1,n):.3f} / usada {sum(s['caida_usada'] for s in ls)/max(1,n):.3f}")
        if les == 'APR_LES_PLANA':
            y = P.run(13594, [les] * 9, T=8000, **KW); chk("determinismo APR_LES_PLANA (dos corridas iguales)", K.normaliza(x) == K.normaliza(y))
    log("(8) runner: entrada campo a campo y mini identidad")
    chk("corre_n9b.tarea == juez.tarea (regla 14)", CR.entrada_campo_a_campo(log))
    chk("corre_n9b.mini_identidad (APR_LES_OFF == APR, s 13599)", CR.mini_identidad(log))
    log("(9) parser del runner (ERR-115): lo malo ABORTA sin correr; lo valido parsea (solo se parsea, NO se corre)")
    malos = [['--help'], ['-h'], ['--humo', '--help'], ['--se'], ['--serie', '--desde', '13501', '--n', '20', '--pool=6'],
             ['--serie', '--desde', '13501', '--n', '20', '--pool', '6', '--help'], ['--serie', '--desde', '13501', '--n', '20'],
             ['--humo', '--pool', '6'], ['--humo', '--desde', '13501'], ['--humo', '--n', '3', '--T', '30000'],
             ['--serie', '--desde', '13301', '--n', '20', '--pool', '6'], ['--humo', '--humo'], ['--foo'], [],
             ['--humo', '--brazos', 'apr,xyz'], ['--serie', '--desde', '13501', '--n', '20', '--pool', '6', '--T', '5000']]
    for m in malos:
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf): CR.parsea(m)
            chk(f"aborta {m}", False, 'NO aborto')
        except SystemExit as e:
            chk(f"aborta {m}", isinstance(e, CR.BanderaMala), str(e)[:90])
    buenos = [['--humo'], ['--humo', '--desde', '13591', '--n', '1', '--T', '20000'], ['--serie', '--desde', '13501', '--n', '20', '--pool', '6'],
              ['--serie', '--desde', '13521', '--n', '20', '--pool', '6'], ['--veredicto', 'a.json,b.json']]
    for m in buenos:
        try: CR.parsea(m); chk(f"parsea {m}", True)
        except SystemExit as e: chk(f"parsea {m}", False, str(e)[:90])
    log(f"RESULTADO: {sum(r)}/{len(r)} en {time.time()-t0:.1f}s")
    return 0 if all(r) else 1


if __name__ == '__main__':
    sys.exit(main())
