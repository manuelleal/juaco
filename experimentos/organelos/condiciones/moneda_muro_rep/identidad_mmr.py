"""identidad_mmr.py — ARNES de la REPLICA de la moneda del muro (1-oct-2026, creador). Escribe su salida ENTERA en
identidad_mmr_salida.txt (la cita el runner: sin 'ARNES: PASA' con los shas actuales, --serie no corre).

MISION: llegar a la AGI por este camino. Un proceso, sin Pool. 6 corridas, 105 000 pasos:
  1 de T 100 000 a la SEMILLA VIEJA 638110 (pasaje moneda_L i1 p0 del explora GUARDADO: debe salir BIT A BIT por el trabajo() de este runner)
  5 de T 1 000 (cadena corta por este runner contra corre_mm.trabajo, y un reintento de aborto).
Ademas, SIN corridas: las 10 cadenas guardadas del explora releidas por el trabajo() de este runner (no recorre nada y da sus numeros).

  python experimentos/organelos/condiciones/moneda_muro_rep/identidad_mmr.py
"""
import json, os, shutil, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_mmr as R   # noqa: E402
MM = R.MM; MU = R.MU; M = R.M
SALIDA = os.path.join(AQUI, 'identidad_mmr_salida.txt')
IGN = {'seg', 'seg_trabajo'}
CORRIDAS = [0, 0]   # corridas, pasos (contados a mano en cada bloque)


def iguales(a, b, ign=IGN): return all(a.get(k) == b.get(k) for k in (set(a) | set(b)) - ign)
def J(f): return json.load(open(f, encoding='utf-8'))


def main():
    LOGF = open(SALIDA, 'w', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time(); ok = True
    log(f"ARNES moneda del muro REPLICA · {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  shas: corre_mmr.py {R.h16(os.path.join(AQUI, 'corre_mmr.py'))} · identidad_mmr.py {R.h16(os.path.abspath(__file__))} · sim_mmr.py {R.h16(os.path.join(AQUI, 'sim_mmr.py'))}")
    log("(K) shas fijados (corre_mm, identidad_mm, sim_mm; por corre_mm.verifica: corre_mut, corre_moneda, sentidos_muro, corre_bp, V143_BQ3, pista, juez)")
    ok &= R.verifica(log)

    log("(C) CONFIGURACION: el modo de la serie == el 'explora' de corre_mm salvo indices y semillas; semillas nuevas, pareadas y sin choques")
    ex = MM.MODOS['explora']; se = R.MODOS['serie']; hu = R.MODOS['humo']
    c = all(se[k] == ex[k] for k in ('npas', 'T_pas', 'T_pru', 'brazos')) and set(se) == set(ex) and se['ind'] == list(range(1, 11))
    c &= MM.MODOS[R.NOMBRE['serie']] == se and MM.MODOS[R.NOMBRE['humo']] == hu and MM.MODOS['explora'] is ex and 'rep_serie' not in ('explora', 'humo')
    sp = [R.sem_pas(se, i, p) for i in se['ind'] for p in range(se['npas'])]; sq = [R.sem_pru(se, i) for i in se['ind']]
    vp = [MM.sem_pas(ex, i, p) for i in ex['ind'] for p in range(ex['npas'])] + [MM.sem_pru(ex, i) for i in ex['ind']] + [638180, 638181, 638191, 638193]
    hp = [R.sem_pas(hu, 14, p) for p in range(hu['npas'])] + [R.sem_pru(hu, 14)]
    ar = [647250, 647251, 647395]
    todas = sp + sq + hp + ar
    c &= len(set(todas)) == len(todas) and not (set(todas) & set(vp)) and min(sp) == 647110 and max(sp) == 647205 and sq == list(range(647301, 647311))
    c &= hp == [647240, 647241, 647390] and hu['T_pas'] * hu['npas'] * 2 + hu['T_pru'] * 2 <= 200000 and (hu['npas'] + 1) * 2 <= 6
    c &= R.CONSERVA_K == 7 and R.PURGA_K == 8 and R.CRUCE_K == 7 and R.CRUCE_D == 9 and R.CONSERVA_MED == MM.CONSERVA_MED == 0.40 and R.MITAD == MM.MITAD
    c &= R.RESPALDO_MAX == MM.RESPALDO_MAX and R.POOL_MAX == 2
    ok &= c; log(f"  serie {se} · humo {hu} · pasajes {min(sp)}..{max(sp)} ({len(set(sp))} distintas) · pruebas {sq[0]}..{sq[-1]} · humo {hp} · arnes {ar} · "
                 f"sin choques con las {len(vp)} del explora: {'OK' if c else 'FALLA'}")

    log("(F) IDENTIDAD CON moneda_muro A LAS SEMILLAS VIEJAS, BIT A BIT")
    s = R.h16(R.REF_PAS[0]); i = s == R.REF_PAS[1]; ok &= i; log(f"  sha del pasaje guardado {os.path.basename(R.REF_PAS[0])} {s}: {'OK' if i else 'FALLA'}")
    ref = J(R.REF_PAS[0])
    with tempfile.TemporaryDirectory() as td:
        MM.MODOS['_v1'] = dict(ex, ind=[1], npas=1, sin_prueba=True)
        t1 = time.time(); o = R.trabajo(('moneda_L', 1, td, '_v1')); CORRIDAS[0] += 1; CORRIDAS[1] += ex['T_pas']
        x = J(os.path.join(td, 'pasaje_moneda_L_i1_p0.json')); dif = sorted(k for k in (set(x) | set(ref)) - IGN if x.get(k) != ref.get(k))
        i = not dif and o['aborto'] is None and x['seed'] == ref['seed'] == 638110 and x['T'] == 100000 and o['frac_A'] == [0.5, 0.5714] and len(set(x) - IGN) >= 17
        ok &= i; log(f"  trabajo(moneda_L, i1) de ESTE runner, pasaje p0 (s {x['seed']}, T {x['T']}, {time.time()-t1:.0f}s) == GUARDADO del explora en {len((set(x) | set(ref)) - IGN)} campos "
                     f"(todos menos {sorted(IGN)}); fraccion A {o['frac_A']}: {'OK' if i else 'FALLA ' + str(dif)}")
        del MM.MODOS['_v1']
    with tempfile.TemporaryDirectory() as td:
        fs = [f for f in os.listdir(R.EXPL) if f.startswith('pasaje_') or f.startswith('moneda_L_s') or f.startswith('neutra_L_s')]
        for f in fs: shutil.copy(os.path.join(R.EXPL, f), os.path.join(td, f))
        sh0 = {f: R.h16(os.path.join(td, f)) for f in fs}; LG = J(R.REF_EXPL[0]); t1 = time.time(); i = len(fs) == 70
        for b in R.BRAZOS:
            for k in ex['ind']:
                o = R.trabajo((b, k, td, 'explora'))
                i &= o['aborto'] is None and o['frac_A'] == [0.5] + LG['cadenas'][b][str(k)]['f'] and o['cruzan'] == LG['prueba'][b][str(k)]['cruzan']
        i &= sh0 == {f: R.h16(os.path.join(td, f)) for f in fs} and sorted(os.listdir(td)) == sorted(fs) and time.time() - t1 < 60
        C, P_, _r, ab, _a, _b = MM.carga(td, 'explora'); L = R.letra(C, P_, ex['ind'], ab, True, True); F = L['fraccion']; X = L['cruce']
        i &= not ab and L['final'] == LG['letra']['final'] and (F['ge'], F['gt'], F['empates'], F['mediana']) == (5, 4, 1, 0.8)
        i &= (X['suma_moneda_L'], X['suma_neutra_L'], X['D'], X['gana'], X['empata'], X['pierde']) == (17, 23, -6, 1, 1, 3)
        ok &= i; log(f"  las 10 cadenas GUARDADAS del explora por trabajo() de este runner (modo 'explora'): 0 corridas ({time.time()-t1:.1f}s), {len(fs)} JSON intactos, "
                     f"frac_A y cruzan == lectura_mm.json; finales {L['final']['moneda_L']} / {L['final']['neutra_L']}; >= {F['ge']}/5, > {F['gt']}/5, "
                     f"cruce {X['suma_moneda_L']} vs {X['suma_neutra_L']}: {'OK' if i else 'FALLA'}")
    eok, etx, E = R.explora_guardado()
    i = eok and E['veredicto'] == 'CONSERVA' and E['fraccion']['gt'] == 4 and E['fraccion']['estricta_b'] is False and E['cruce']['D'] == -6 and E['cruce']['veredicto'] == 'SIN DIFERENCIA'
    ok &= i; log(f"  explora_guardado(): {etx} · veredicto alli {E.get('veredicto')} · estricta > {E['fraccion']['gt']}/5 · cruce D {E['cruce']['D']}: {'OK' if i else 'FALLA'}")

    log("(E) regla 14: cadena corta (semillas del arnes, T 1 000) por ESTE runner == corre_mm.trabajo, JSON por JSON; reintento de aborto")
    with tempfile.TemporaryDirectory() as td:
        d1 = os.path.join(td, 'r'); d2 = os.path.join(td, 'm'); os.makedirs(d1); os.makedirs(d2)
        mt = dict(ind=[15], npas=1, T_pas=1000, T_pru=1000, base_pas=647100, base_pru=647380, brazos=R.BRAZOS)
        R.MODOS['_t'] = mt; R.NOMBRE['_t'] = 'rep__t'; MM.MODOS['_tm'] = dict(mt)
        o1 = R.trabajo(('neutra_L', 15, d1, '_t')); o2 = MM.trabajo(('neutra_L', 15, d2, '_tm')); CORRIDAS[0] += 4; CORRIDAS[1] += 4000
        fs = sorted(os.listdir(d2)); i = fs == sorted(os.listdir(d1)) == ['neutra_L_s647395.json', 'pasaje_neutra_L_i15_p0.json']
        i &= all(iguales(J(os.path.join(d1, f)), J(os.path.join(d2, f))) for f in fs) and o1['frac_A'] == o2['frac_A'] and o1['cruzan'] == o2['cruzan'] and o1['aborto'] is None
        x = J(os.path.join(d1, 'pasaje_neutra_L_i15_p0.json')); i &= x['seed'] == 647250 and x['bq']['cfg'] == MM.CFG10 and x['moneda_siembra'] == 'L' and x['frac_A_entra'] == 0.5
        ok &= i; log(f"  neutra_L i15: {len(fs)} JSON campo a campo (menos {sorted(IGN)}), frac_A {o1['frac_A']}, cruzan {o1['cruzan']}; cfg del carro == CFG10; semilla 647250: {'OK' if i else 'FALLA'}")
        f1 = os.path.join(d1, 'neutra_L_s647395.json'); xx = J(f1); bueno = dict(xx); xx['aborto'] = 'simulado'; M._guarda(f1, xx)
        o3 = R.trabajo(('neutra_L', 15, d1, '_t')); CORRIDAS[0] += 1; CORRIDAS[1] += 1000; y = J(f1)
        i = o3['aborto'] is None and o3['frac_A'] == o1['frac_A'] and o3['cruzan'] == o1['cruzan'] and y.get('reintento_de') == 'aborto' and iguales(y, bueno, IGN | {'reintento_de'})
        ok &= i; log(f"  aborto simulado en la prueba y reanuda: solo se recorre la prueba y sale identica: {'OK' if i else 'FALLA'}")
        del R.MODOS['_t']; del R.NOMBRE['_t']; del MM.MODOS['_tm']; MM.MODOS.pop('rep__t', None)

    log("(X) el runner NIEGA pool > 2, pool o reanuda en el humo y --lee de una carpeta que no existe (no se llama a --serie desde el arnes)")
    for argv in (['--serie', '--pool', '3'], ['--humo', '--pool', '2'], ['--humo', '--reanuda'], ['--lee', 'datos/no_existe']):
        try: R.main(argv); i = False
        except SystemExit as e: i = any(t in str(e) for t in ('maximo', 'sin Pool', 'no existe'))
        ok &= i; log(f"  {argv}: {'OK (niega)' if i else 'FALLA'}")

    log("(G) CANDADOS de --serie: veredicto previo, carpeta previa, reanuda sin carpeta, git limpio")
    with tempfile.TemporaryDirectory() as td:
        si = lambda a: None; no = lambda a: 'git: sucio'
        casos = [('vacio + git limpio -> corre', False, si, None), ('vacio + git sucio -> niega', False, no, 'git: sucio'), ('--reanuda sin carpeta -> niega', True, si, 'no hay carpeta')]
        for txt, re_, g, e in casos:
            r = R.guarda(re_, datos=td, git=g); i = (r is None) if e is None else (r is not None and e in r); ok &= i; log(f"  {txt}: {r} {'OK' if i else 'FALLA'}")
        os.makedirs(os.path.join(td, 'humo_x')); r = R.guarda(False, datos=td, git=si); i = r is None; ok &= i; log(f"  una carpeta humo_* no bloquea: {r} {'OK' if i else 'FALLA'}")
        d = os.path.join(td, 'serie_20261001_000000'); os.makedirs(d)
        for txt, re_, e in (('carpeta cortada sin --reanuda -> niega', False, 'solo --reanuda'), ('carpeta cortada con --reanuda -> corre', True, None)):
            r = R.guarda(re_, datos=td, git=si); i = (r is None) if e is None else (r is not None and e in r); ok &= i; log(f"  {txt}: {r} {'OK' if i else 'FALLA'}")
        json.dump(dict(letra=dict(veredicto='NO SE LEE')), open(os.path.join(d, 'lectura_mmr.json'), 'w'))
        r = R.guarda(True, datos=td, git=si); i = r is None; ok &= i; log(f"  NO SE LEE previo con --reanuda -> corre: {r} {'OK' if i else 'FALLA'}")
        for v in R.VEREDICTOS:
            json.dump(dict(letra=dict(veredicto=v)), open(os.path.join(d, 'lectura_mmr.json'), 'w'))
            r = R.guarda(True, datos=td, git=si); i = r is not None and 'ya tiene veredicto' in r; ok &= i; log(f"  veredicto previo {v}, aun con --reanuda -> niega: {'OK' if i else 'FALLA'}")
    r1 = R.git_limpio(list(R.SHAS)); r2 = R.git_limpio([os.path.join(AQUI, 'no_existe_en_git.py')])
    i = r1 is None and r2 is not None and 'commiteado False' in r2; ok &= i
    log(f"  git_limpio REAL: los 3 archivos importados de moneda_muro (commit 857bbb87) -> {r1}; un archivo sin commitear -> niega: {'OK' if i else 'FALLA'}")
    i = all(os.path.basename(f) in ('PREREGISTRO_moneda_muro_rep.md', 'corre_mmr.py', 'identidad_mmr.py', 'identidad_mmr_salida.txt', 'sim_mmr.py', 'corre_mm.py', 'identidad_mm.py', 'sim_mm.py')
            for f in R.ARCHIVOS()) and len(R.ARCHIVOS()) == 8
    ok &= i; log(f"  archivos que el candado exige commiteados: {[os.path.basename(f) for f in R.ARCHIVOS()]}: {'OK' if i else 'FALLA'}")

    log("(L) LA LETRA en casos sinteticos (n = 10; decide la ESTRICTA: > en >= 7/10 y mediana >= 0.40; PURGA >= 8/10; cruce: >= 7/10 y |D| >= 9)")
    ind = list(range(1, 11))
    def cad(f, fi=0.5, sombra=0.3, resp=(False, False)): return dict(f_ini=fi, f=[0.4, f], f_sombra_vieja=[0.45, sombra], respaldo=list(resp), n_ele=[4, 5], cruzan_pas=[4, 4])
    def tb(mo, ne, **kw): return {'moneda_L': {i: cad(mo[i - 1], **kw) for i in ind}, 'neutra_L': {i: cad(ne[i - 1], **kw) for i in ind}}
    def pr(cm, cn, s2=0): return {'moneda_L': {i: dict(seed=647300 + i, cruzan=cm[i - 1]) for i in ind}, 'neutra_L': {i: dict(seed=647300 + i + s2, cruzan=cn[i - 1]) for i in ind}}
    P0 = pr([4] * 10, [4] * 10)
    casos = [('CONSERVA: > en 7/10 y mediana 0.6', tb([.6] * 7 + [0, 0, 0], [.1] * 7 + [.5, .5, .5]), 'CONSERVA'),
             ('en el borde: mediana == 0.40 y 7/10', tb([.4] * 7 + [0, 0, 0], [.1] * 7 + [.5, .5, .5]), 'CONSERVA'),
             ('no CONSERVA con > en 6/10 (aunque >= en 10/10: los empates van en contra)', tb([.6] * 6 + [0, 0, 1, 1], [.1] * 6 + [0, 0, 1, 1]), 'INDETERMINADO'),
             ('el caso del explora duplicado (> 8/10, dos empates 0 = 0)', tb([.8, .5, .996, 0, .8] * 2, [.1429, .33, .0467, 0, .1457] * 2), 'CONSERVA'),
             ('no CONSERVA si la mediana < 0.40 aunque > en 10/10', tb([.3] * 10, [.2] * 10), 'INDETERMINADO'),
             ('PURGA: <= 0.5 neutra en 8/10', tb([.1] * 8 + [1, 1], [.3] * 8 + [.3, .3]), 'PURGA'),
             ('no PURGA con 7/10', tb([.1] * 7 + [1, 1, 1], [.3] * 10), 'INDETERMINADO'),
             ('no PURGA: 0 contra 0 no cuenta', tb([0] * 10, [0] * 6 + [1] * 4), 'INDETERMINADO'),
             ('todas iguales (empates 10/10): INDETERMINADO', tb([.5] * 10, [.5] * 10), 'INDETERMINADO')]
    for txt, C, e in casos:
        L = R.letra(C, P0, ind, [], True, True); i = L['veredicto'] == e and L['cruce']['veredicto'] == 'SIN DIFERENCIA'; ok &= i
        log(f"  {txt}: {L['veredicto']} (espera {e}) {'OK' if i else 'FALLA'}")
    L = R.letra(tb([.6] * 6 + [0, 0, 1, 1], [.1] * 6 + [0, 0, 1, 1]), P0, ind, [], True, True); F = L['fraccion']
    i = F['original_a10'] and not F['estricta_b'] and F['empates'] == 4 and F['empates_arriba'] == 2 and L['en_umbral']; ok &= i
    log(f"  las dos lecturas se separan: original 10/10 {F['original_a10']}, estricta {F['estricta_b']} (empates {F['empates']}, arriba {F['empates_arriba']}), en_umbral {L['en_umbral']}: {'OK' if i else 'FALLA'}")
    L = R.letra(tb([.6] * 5 + [0] * 5, [.1] * 5 + [.5] * 5), P0, ind, [], True, True); F = L['fraccion']
    i = F['original_a5'] and not F['original_a10'] and not F['estricta_b'] and not L['en_umbral']; ok &= i; log(f"  original sobre las 5 primeras True con 5/10 en total (no decide): {'OK' if i else 'FALLA'}")
    CC = tb([.6] * 10, [.1] * 10)
    for txt, P, e, um in (('CRUZA MAS: gana 7/10 y D +9', pr([5] * 6 + [7] + [4] * 3, [4] * 10), 'CRUZA MAS', True),
                          ('no CRUZA MAS: gana 7/10 pero D +7', pr([5] * 7 + [4] * 3, [4] * 10), 'SIN DIFERENCIA', True),
                          ('no CRUZA MAS: D +12 pero gana 6/10', pr([6] * 6 + [4] * 4, [4] * 10), 'SIN DIFERENCIA', True),
                          ('CRUZA MENOS: pierde 8/10 y D -12', pr([3] * 6 + [1, 1] + [4, 4], [4] * 10), 'CRUZA MENOS', False),
                          ('el explora duplicado (D -12, pierde 6, gana 2): SIN DIFERENCIA', pr([3, 5, 2, 4, 3] * 2, [6, 4, 5, 5, 3] * 2), 'SIN DIFERENCIA', True),
                          ('empates 10/10: SIN DIFERENCIA', pr([4] * 10, [4] * 10), 'SIN DIFERENCIA', False)):
        L = R.letra(CC, P, ind, [], True, True); i = L['cruce']['veredicto'] == e and L['cruce']['en_umbral'] == um and L['veredicto'] == 'CONSERVA'; ok &= i
        log(f"  {txt}: {L['cruce']['veredicto']} (D {L['cruce']['D']}, gana {L['cruce']['gana']}, pierde {L['cruce']['pierde']}, umbral {L['cruce']['en_umbral']}) {'OK' if i else 'FALLA'}")
    Pm = pr([4] * 10, [4] * 10); del Pm['neutra_L'][10]
    Cm = tb([.6] * 10, [.1] * 10); del Cm['moneda_L'][3]
    for txt, C, P, ab, kw in (('aborto', CC, P0, ['x'], {}), ('falta una prueba', CC, Pm, [], {}), ('falta una cadena', Cm, P0, [], {}),
                              ('la moneda no actua', {b: {k: dict(c_, f_sombra_vieja=list(c_['f'])) for k, c_ in d.items()} for b, d in CC.items()}, P0, [], {}),
                              ('respaldo en > 25 %', tb([.6] * 10, [.1] * 10, resp=(True, False)), P0, [], {}), ('entrada != 0.5', tb([.6] * 10, [.1] * 10, fi=0.6), P0, [], {}),
                              ('prueba no pareada', CC, pr([4] * 10, [4] * 10, s2=1), [], {}), ('arnes', CC, P0, [], dict(arnes_ok=False)), ('explora sin sha', CC, P0, [], dict(expl_ok=False))):
        k2 = dict(dict(expl_ok=True, arnes_ok=True), **kw); L = R.letra(C, P, ind, ab, k2['expl_ok'], k2['arnes_ok'])
        i = L['veredicto'] == 'NO SE LEE' and L['cruce']['veredicto'] == 'NO SE LEE' and R.bloque(L, E)['titular'] == 'NO SE LEE'; ok &= i
        log(f"  NO SE LEE ({txt}): {L['veredicto']} {'OK' if i else 'FALLA'}")
    log("(B) BLOQUE contra el explora y predicciones (se imprimen sin excepcion en los tres veredictos; H-3 sin 'x2', H-5 umbral en el titular)")
    CU = tb([.6] * 7 + [0, 0, 0], [.1] * 7 + [.5, .5, .5])   # CONSERVA con exactamente 7/10: en el umbral
    for C, P, tit in ((CC, pr([5] * 6 + [7] + [4] * 3, [4] * 10), 'FUNCIONA:'), (CC, P0, 'HAY ALGO MODESTO:'), (CU, P0, 'HAY ALGO MODESTO · EN EL UMBRAL:'),
                      (CU, pr([5] * 6 + [7] + [4] * 3, [4] * 10), 'FUNCIONA · EN EL UMBRAL:'), (tb([.5] * 10, [.5] * 10), P0, 'NO:'), (tb([.1] * 10, [.3] * 10), P0, 'NO:')):
        L = R.letra(C, P, ind, [], True, True); B = R.bloque(L, E); pq = R.predicciones(L)
        i = 'x2' not in str(B) and ('no es declaracion' in B['titular']) == tit.startswith('FUNCIONA') and L['sobre_inicial']['moneda_L'] == sum(1 for c_ in C['moneda_L'].values() if c_['f'][-1] > 0.5)
        i &= B['titular'].startswith(tit) and len(pq) == 13 and abs(sum(q[4] for q in pq[:3]) - 0.97) < 1e-9 and abs(sum(q[4] for q in pq[3:6]) - 0.97) < 1e-9; ok &= i
        log(f"  {L['veredicto']} + {L['cruce']['veredicto']} -> {B['titular']} | {B['fraccion']} | {B['cruce']}: {'OK' if i else 'FALLA'}")
    i = CORRIDAS[0] <= 6 and CORRIDAS[1] <= 200000; ok &= i; log(f"(N) corridas de este arnes: {CORRIDAS[0]} (max 6) · pasos {CORRIDAS[1]} (max 200 000): {'OK' if i else 'FALLA'}")
    log(f"ARNES: {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
