"""identidad_cruce.py — ARNES del bloque organelos/cruce. Se corre ANTES de mirar cualquier numero de conducta. Un proceso, sin Pool.

MISION: llegar a la AGI por este camino. Comprueba:
 (0) shas de los origenes; motor y carro en disco == construye_cruce; revisa_carro PASA; el carro no nombra la tabla verdadera.
 (1) motor_cruce con cruce=None == pista.py BIT A BIT (salida completa, incluido el estado final del rng del mundo): 9 V143 y 9 O1.
 (2) GENES APAGADOS == v14.3 EN LA PISTA: 9 CRUCE (sin cruce) == 9 V143 bit a bit; y la lectura v143 de este corredor ==
     corre_v143.tarea('V143') del bloque tronco_v14_3 campo a campo (regla 14), 2 semillas.
 (3) MUT0: la cria con toda la maquinaria (genes, banco, sombras) y p_mut 0 == v14.3 bit a bit; la lectura mut0 == la lectura v143.
 (4) LECTURA: el genotipo se conserva (hijos y fundadores llevan el del linaje); DESF difiere de VIDA con los mismos genomas, lee
     senales pasadas y la historia del linaje pasa al fundador; la muestra del banco es determinista y el placebo es otra muestra.
 (5) CRIA: los genes MUTAN, se HEREDAN (distancia hijo-padre = error de copia) y AZAR no copia al padre; determinismo.
 (6) los genes CAMBIAN LA CONDUCTA (genoma forzado, SOLO el arnes): boca, parto, patas y un gen que lee el estado.
 (7) el control desfasado lee senales pasadas con marginal parecida a la presente.
 (8) la letra (veredicto) da FUNCIONA / MODESTO / NO / NO SE LEE en casos sinteticos.
 (9) nube-9: SystemExit dentro de la tarea vuelve como error; el corredor aborta ante banderas desconocidas o abreviadas, semillas
     ajenas, humo con Pool o > 200 000 pasos, serie sin Pool y cria/lectura no preregistradas; N (subida_n7) es inerte (masa 3).
Ultima linea: "RESULTADO: N/N". JSON en datos/humo/.

    python experimentos/organelos/cruce/identidad_cruce.py
"""
import hashlib, importlib.util, json, os, sys, time
import numpy as np

sys.dont_write_bytecode = True   # no deja __pycache__ en carpetas ajenas (pista, juez, tronco_v14_3 se importan solo para leer)
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_cruce as C
MC, J, RC, CC = C.MC, C.J, C.RC, C.CC
sys.path.insert(0, C.PISTA)
import pista as P
TV3 = os.path.join(C.RAIZ, 'experimentos', 'tronco_v14_3')

OK = []; FILAS = []
def chk(nombre, cond, extra=''):
    OK.append(bool(cond)); FILAS.append(dict(n=len(OK), prueba=nombre, ok=bool(cond), extra=str(extra)[:400]))
    print(f"  [{len(OK):2d}] {'OK   ' if cond else 'FALLA'} {nombre}{(' · ' + str(extra)) if extra else ''}", flush=True)

N = lambda x: json.loads(json.dumps(x, default=str))


def sin_cruce(r):
    r = N(r); r.pop('cruce', None)
    for l in r['linajes']: l['carro'].pop('cruce', None)
    return r


def carga(ruta, nom):
    spec = importlib.util.spec_from_file_location(nom, ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main():
    t0 = time.time()
    print(f"IDENTIDAD organelos/cruce · {time.strftime('%Y-%m-%d %H:%M:%S')} · corre_cruce {C.h16(os.path.join(AQUI, 'corre_cruce.py'))} · "
          f"construye_cruce {C.h16(os.path.join(AQUI, 'construye_cruce.py'))} · motor {C.h16(os.path.join(AQUI, 'motor_cruce.py'))} · "
          f"carro {C.h16(os.path.join(AQUI, 'carros', 'CRUCE.py'))}")
    # (0)
    malos = [os.path.relpath(r, C.RAIZ) for r, s in C.SHAS.items() if C.h16(r) != s]
    chk("(0a) shas de pista, juez, O1, revisa_carro, V143 y corre_v143 (origenes, solo se leen)", not malos, malos or 'todos OK')
    outs = CC.todas(); dif = [os.path.relpath(r, AQUI) for r, b in outs.items() if open(r, 'rb').read() != b]
    chk("(0b) motor_cruce.py y carros/CRUCE.py en disco == construye_cruce (por anclas)", not dif, dif or {os.path.relpath(r, AQUI): CC.h16b(b) for r, b in outs.items()})
    src = open(os.path.join(AQUI, 'carros', 'CRUCE.py'), encoding='utf-8').read()
    v = RC.revisa_fuente(src, 'CRUCE'); chk("(0c) revisa_carro PASA carros/CRUCE.py (chequeo estatico de la carrera)", not v, v[:2])
    tok = [t for t in ('VAL_VIVO', 'EFECTO', 'rng_mundo', 'default_rng') if t in src]
    chk("(0d) el carro no nombra la tabla verdadera ni crea rng propios", not tok, tok)
    CR = C.modulo('CRUCE'); O1 = C.modulo('O1'); V3 = carga(os.path.join(TV3, 'carros_v143', 'V143.py'), 'carro_V143_orig')
    NOM = CR.NOMBRES_GEN
    chk("(0e) genoma: 36 genes (boca 3 contextos x 6 senales + pata 2 filas x 6 + parto 6), nombres unicos", CR.NG == 36 and len(set(NOM)) == 36, CR.NG)
    # (1) motor(cruce=None) == pista
    for s, mod, et in ((24401, V3, 'V143'), (24402, O1, 'O1')):
        a = P.run(s, [(et, mod)] * 9, T=2500, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
        b = MC.run(s, [(et, mod)] * 9, T=2500, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
        chk(f"(1) motor_cruce(cruce=None) == pista.py, 9 {et}, s{s}, T 2500, salida completa + rng del mundo", N(a) == N(b),
            a['pista']['rng_mundo_estado'] == b['pista']['rng_mundo_estado'])
    # (2) genes apagados == v14.3 en la pista
    for s in (24401, 24403):
        a = P.run(s, [('V143', V3)] * 9, T=4000, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
        b = MC.run(s, [('V143', CR)] * 9, T=4000, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
        chk(f"(2a) 9 CRUCE sin cruce == 9 V143 en la pista, s{s}, T 4000 (salida completa: fisica + telemetria del carro)", N(a) == N(b),
            f"muertes {sum(l['deaths'] for l in a['linajes'])} partos {sum(l['descendientes'] for l in a['linajes'])}")
    sys.path.insert(0, TV3); CV3 = carga(os.path.join(TV3, 'corre_v143.py'), 'corre_v143_orig')
    for s in (24402, 24404):
        x = CV3.tarea((s + C.OFF_LECT, 'V143', 3000)); y = C.tarea(('lee', s, 'v143', 3000, None))
        telx = [t['v143'] for t in x['tel']]; tely = [t['v143'] for t in y['tel']]
        chk(f"(2b) regla 14: lectura v143 de corre_cruce == corre_v143.tarea('V143') campo a campo, s{s}+{C.OFF_LECT} (linajes, pista, R0 pista, telemetria v143)",
            N(x['linajes']) == N(y['linajes']) and N(x['pista']) == N(y['pista']) and x['R0_pista'] == y['R0_pista'] and N(telx) == N(tely) and y['error'] is None,
            f"R0 pista {x['R0_pista']} / {y['R0_pista']}")
    # (3) MUT0
    for s in (24401, 24402):
        a = MC.run(s, [('V143', CR)] * 9, T=4000, fundador_limpio=1)
        b = MC.run(s, [('V143', CR)] * 9, T=4000, fundador_limpio=1, cruce=C.cfg_cria('mut0', 4000))
        chk(f"(3a) cria MUT0 (genes, banco, sombras, p_mut 0) == v14.3 bit a bit, s{s}, T 4000", N(a) == sin_cruce(b),
            f"partos {b['cruce']['n_partos']} refundados {b['cruce']['n_refund']} mut {b['cruce']['n_mut']} banco !=0 {sum(1 for g in b['cruce']['final']['banco'] if any(g))}")
    m = C.tarea(('lee', 24403, 'mut0', 4000, [[0] * CR.NG] * 9)); w = C.tarea(('lee', 24403, 'v143', 4000, None))
    chk("(3b) lectura mut0 (genomas 0 con la maquinaria) == lectura v143 (fisica de los 9 linajes, s24403, T 4000)", C.fisica(m) == C.fisica(w) and m['error'] is None)
    # (4) LECTURA
    gq = [0] * CR.NG; gq[NOM.index('boca_bueno_reserva')] = -4; gq[NOM.index('boca_malo_otra')] = 4
    gr = [0] * CR.NG; gr[NOM.index('boca_neutro_sesgo')] = -2; gr[NOM.index('pata_act_reserva')] = 2
    G9 = [gq if i % 2 == 0 else gr for i in range(9)]
    lv = C.tarea(('lee', 24401, 'vida', 12000, G9))
    fin = lv['cruce']['final']['vivos']; nf = sum(l['fundadores'] for l in lv['linajes'])
    chk("(4a) LECTURA: el genotipo se conserva: al final cada linaje lleva SU genoma inicial (hijos copian sin error, el fundador lleva el del linaje)",
        fin == G9 and nf > 0 and sum(lv['cruce']['ham'][1:]) == 0, f"fundadores {nf} · partos {lv['cruce']['n_partos']} · hist {lv['cruce']['ham'][:3]}")
    sp = {'con_buf': 0, 'fund': 0}; orig_init = CR.Carro._cr_init
    def espia_init(self, ctx):
        orig_init(self, ctx); c = ctx.get('cruce') or {}
        if c.get('buf') is not None: sp['fund'] += 1; sp['con_buf'] += int(len(self._buf) > 0)
    CR.Carro._cr_init = espia_init
    try:
        ld = C.tarea(('lee', 24401, 'desf', 12000, G9))
    finally:
        CR.Carro._cr_init = orig_init
    lec = sum(t['cruce'].get('lesion_lecturas', 0) for t in ld['tel']); lecv = sum(t['cruce'].get('lesion_lecturas', 0) for t in lv['tel'])
    chk("(4b) DESF (mismos genomas) difiere de VIDA en la lectura; solo DESF lee senales pasadas; la historia de senales del linaje pasa al fundador",
        C.fisica(ld) != C.fisica(lv) and lec > 0 and lecv == 0 and sp['fund'] > 0 and sp['con_buf'] == sp['fund'],
        f"lecturas desfasadas {lec} · fundadores con historia {sp['con_buf']}/{sp['fund']}")
    bk = [[j % 5 - 2 if k == j % 36 else 0 for k in range(36)] for j in range(200)]
    m1 = C.muestra(bk, 24601, 0); m1b = C.muestra(bk, 24601, 0); m2 = C.muestra(bk, 24601, 1)
    ix = lambda mm: sorted(bk.index(g) for g in mm)
    chk("(4c) la muestra del banco es determinista, de 9 SIN reemplazo, y el placebo (k = 1) es otra muestra del mismo banco",
        m1 == m1b and len(set(map(tuple, m1))) == 9 and ix(m1) != ix(m2), f"{ix(m1)} / {ix(m2)}")
    # (5) CRIA
    a = MC.run(24401, [('V143', CR)] * 9, T=12000, fundador_limpio=1, cruce=C.cfg_cria('vida', 12000))
    a2 = MC.run(24401, [('V143', CR)] * 9, T=12000, fundador_limpio=1, cruce=C.cfg_cria('vida', 12000))
    chk("(5a) determinista: la misma cria VIDA dos veces es identica", N(a) == N(a2))
    cr = a['cruce']; ham = cr['ham']; nz_b = sum(1 for g in cr['corte']['banco'] if any(g))
    chk("(5b) CRIA VIDA: los genes MUTAN (reales y sombras) y el banco del corte lleva genomas != 0; el corte es la foto en t = T",
        cr['n_mut'] > 0 and cr['n_mut_sombra'] > 0 and nz_b > 0 and cr['corte']['t'] == 12000,
        f"n_mut {cr['n_mut']} sombras {cr['n_mut_sombra']} partos {cr['n_partos']} refundados {cr['n_refund']} banco !=0 {nz_b}/{cr['corte']['banco_n']}")
    ma = sum(j * x for j, x in enumerate(ham)) / max(1, sum(ham)); esper = C.P_MUT * CR.NG
    chk("(5c) CRIA VIDA: HERENCIA: distancia media hijo-padre = el error de copia esperado (p_mut x NG, +-50 %), no la de un genoma nuevo",
        0.5 * esper <= ma <= 1.5 * esper, f"media {ma:.2f} esperada {esper:.2f} hist {ham}")
    z = MC.run(24401, [('V143', CR)] * 9, T=12000, fundador_limpio=1, cruce=C.cfg_cria('azar', 12000))
    hz = z['cruce']['ham']; mz = sum(j * x for j, x in enumerate(hz)) / max(1, sum(hz))
    chk("(5d) CRIA AZAR: el genoma del hijo NO es copia del padre (distancia media hijo-padre mayor que en VIDA)", mz > ma, f"AZAR {mz:.2f} VIDA {ma:.2f} hist {hz}")
    # (6) los genes cambian la conducta (genoma forzado; SOLO el arnes)
    base = MC.run(24402, [('V143', CR)] * 9, T=6000, fundador_limpio=1, cruce=C.cfg_cria('mut0', 6000))
    BD = lambda r: sum(sum(l['mord']['B']) + sum(l['mord']['D']) for l in r['linajes'])
    def forzado(**genes):
        g = [0] * CR.NG
        for k, x in genes.items(): g[NOM.index(k)] = x
        return MC.run(24402, [('V143', CR)] * 9, T=6000, fundador_limpio=1, cruce=dict(C.cfg_cria('mut0', 6000), genoma0=g))
    f1 = forzado(boca_malo_sesgo=-4, boca_neutro_sesgo=-2); t1 = f1['cruce']['tel_carro']; bd = sum(t['boca_dif'] for t in t1)
    chk("(6a) genes de BOCA: con boca_malo_sesgo -4 la boca cambia decisiones y las mordidas de B+D cambian", bd > 0 and BD(f1) != BD(base),
        f"boca_dif {bd} de {sum(t['boca_dec'] for t in t1)} · B+D {BD(base)} -> {BD(f1)}")
    f2 = forzado(parto_sesgo=-1); vt = sum(t['vetos_parto'] for t in f2['cruce']['tel_carro'])
    chk("(6b) gen de PARTO: con parto_sesgo -1 el cuerpo veta sus ventanas (0 partos) y la pista cuenta los vetos",
        vt > 0 and sum(l['descendientes'] for l in f2['linajes']) == 0 and sum(l['_carrera']['vetos'] for l in f2['linajes']) == vt, f"vetos {vt}")
    f3 = forzado(pata_act_sesgo=4); pd = sum(t['pata_dif'] for t in f3['cruce']['tel_carro'])
    chk("(6c) genes de PATA: con ganancia sobre el valor de la fila activa las patas eligen otro objetivo que el mas cercano", pd > 0,
        f"pata_dif {pd} de {sum(t['pata_dec'] for t in f3['cruce']['tel_carro'])}")
    f4 = forzado(boca_bueno_reserva=-4); d4 = sum(t['boca_dif'] for t in f4['cruce']['tel_carro'])
    chk("(6d) un gen que multiplica una senal (reserva) cambia la conducta segun el estado", d4 > 0, d4)
    # (7) marginal del desfasado
    senales = {'pres': [], 'desf': []}; orig = CR.Carro._desfasa
    def espia(self, t, s):
        r = orig(self, t, s)
        if self._on and t >= self._les: senales['pres'].append(s); senales['desf'].append(r)
        return r
    CR.Carro._desfasa = espia
    try:
        C.tarea(('lee', 24403, 'desf', 8000, G9))
    finally:
        CR.Carro._desfasa = orig
    p = np.array(senales['pres']); d = np.array(senales['desf'])
    dm = np.abs(p.mean(0) - d.mean(0)) if len(p) else np.ones(6); igual = float((p == d).all(1).mean()) if len(p) else 1.0
    chk("(7) DESFASADO: marginal de las 6 senales parecida a la presente (|dif de medias| <= 0.10) y el paso leido casi nunca es el presente",
        len(p) > 1000 and dm.max() <= 0.10 and igual < 0.2, f"n {len(p)} dif medias {np.round(dm, 3).tolist()} iguales {igual:.3f}")
    # (8) la letra en casos sinteticos
    def sint(v, az, v3, de, vp, o1, e5=True):
        res = {'vida': dict(R0_real_med=v, gana_e5=e5), 'v143': dict(R0_real_med=0.55), 'o1': dict(R0_real_med=o1)}
        pr = {'vida-azar': dict(gana=az, dif_med=0.2), 'vida-v143': dict(gana=v3, dif_med=0.2), 'vida-desf': dict(gana=de, dif_med=0.2),
              'vida-vida_p': dict(gana=vp, dif_med=0.0)}
        return C.veredicto(res, pr, True, 0, 20)['veredicto']
    casos = [(sint(0.93, 18, 20, 17, 10, 0.94), 'FUNCIONA'), (sint(0.93, 18, 20, 9, 10, 0.94), 'HAY ALGO MODESTO (cruza'),
             (sint(0.70, 16, 19, 12, 11, 0.94), 'HAY ALGO MODESTO'), (sint(0.60, 12, 19, 12, 11, 0.94), 'NO'),
             (sint(0.93, 18, 20, 17, 17, 0.94), 'NO SE LEE'), (sint(0.93, 18, 20, 17, 10, 0.70), 'NO SE LEE'), (sint(0.93, 18, 20, 17, 10, 0.94, False), 'HAY ALGO MODESTO')]
    chk("(8) la letra: FUNCIONA / MODESTO (cruza sin que caiga desf) / MODESTO / NO / NO SE LEE (placebo, ancla O1) / sin ENMIENDA 5 no cruza, en casos sinteticos",
        all(x.startswith(y) for x, y in casos) and casos[6][0] == 'HAY ALGO MODESTO', [x[:24] for x, _ in casos])
    # (9) nube-9, banderas, N inerte
    orig_run = MC.run
    MC.run = lambda *a, **k: (_ for _ in ()).throw(SystemExit('PISTA2: mas de 100000 cuerpos en un linaje (ERR-60) [simulado]'))
    try:
        e = C.tarea(('cria', 24401, 'vida', 100))
    finally:
        MC.run = orig_run
    chk("(9a) nube-9: SystemExit dentro de la tarea se ATRAPA y vuelve como registro de error (no cuelga el Pool)",
        isinstance(e, dict) and e.get('error', '').startswith('SystemExit'), e.get('error'))
    import multiprocessing   # el arnes NUNCA abre un Pool: si una bandera pasara por error, esto aborta en vez de lanzar una serie
    multiprocessing.Pool = lambda *a, **k: (_ for _ in ()).throw(RuntimeError('Pool prohibido en el arnes'))
    malos = []
    for argv in (['--humo', '--semila', '24401'], ['--hum'], ['--humo', '--semilla', '24601'], ['--humo', '--pool', '2'],
                 ['--serie', '--desde', '24601', '--n', '20'], ['--serie', '--desde', '24001', '--n', '2', '--pool', '2'],
                 ['--humo', '--tc', '90000'], ['--serie', '--desde', '24601', '--n', '2', '--pool', '2', '--tc', '1000'],
                 ['--serie', '--desde', '24615', '--n', '10', '--pool', '2']):
        try:
            C.main(argv); malos.append(argv)
        except SystemExit:
            pass
        except RuntimeError:
            malos.append(argv)
    chk("(9b) el corredor ABORTA ante banderas desconocidas/abreviadas, semillas ajenas o que se salen de la serie, humo con Pool, humo > 200 000 pasos, "
        "serie sin Pool y cria/lectura no preregistradas", not malos, malos)
    PAT = P.cfg_fabrica()['PAT']
    chk("(9c) N de subida_n7 es INERTE en la pista: todas las letras tienen masa 3 (M0 = 3): v14.2+N == v14.2 aqui",
        all(float(v.sum()) == 3.0 for v in PAT.values()), {k: float(v.sum()) for k, v in PAT.items()})
    n = len(OK); k = sum(OK)
    os.makedirs(C.DATOS_HUMO, exist_ok=True)
    ruta = os.path.join(C.DATOS_HUMO, f"identidad_cruce_{time.strftime('%Y%m%d_%H%M%S')}.json")
    b = json.dumps(dict(filas=FILAS, n=n, ok=k, seg=round(time.time() - t0, 1)), default=str).encode('utf-8'); open(ruta, 'wb').write(b)
    print(f"  JSON {os.path.relpath(ruta, C.RAIZ)} ({hashlib.sha256(b).hexdigest()[:16]}) · {time.time() - t0:.0f} s")
    print(f"RESULTADO: {k}/{n}")
    return k == n


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
