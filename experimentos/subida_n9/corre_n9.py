"""corre_n9.py — RUNNER del bloque "el modelo de si es causal" (subida del nivel 9). PREREGISTRO_n9.md manda.

MISION: llegar a la AGI por este camino.

Cuatro monocultivos de 9 en la pista de la ronda 2 (ENMIENDA 5: fundador limpio; ENMIENDA 6: persistencia), T = 100000:
  O3               referencia (gano la ronda 2 y se replico en la sellada; aqui corre en semillas NUEVAS)
  O3_LES_SI        lesion del ESTADO PROPIO: toda decision lee (E, Ag) de un paso pasado al azar (ultimos 2000 pasos del linaje)
  O3_TERM_CIEGO    lesion de la RESERVA DEL LINAJE en la muerte programada: TERMINAL a los 2 partos sin mirar la cola
  CTRL_O3_SINTERM  sin muerte programada (el control de generaciones, mismo sha)
El juez es el de la carrera (juez.py 6a68f640a7832f12, solo se IMPORTA): resumen_linaje (solo fisica, ERR-96), ENMIENDA 5
(R0 de nacimientos reales, fundador limpio, mayoria por semilla, gana >= 15/20) y ENMIENDA 6 (persistencia). Encima, las
comparaciones pareadas por semilla y las predicciones firmadas del PREREGISTRO_n9.md con SE CUMPLE / NO.

Antes de correr (si algo falla, NO corre): shas de los originales, construccion por anclas reproducible, chequeo estatico,
identidad corta del juez (FABRICA == organismo_f9c) y mini identidad O3_LES_OFF == O3 (s13399, T=3000).

  python experimentos/subida_n9/corre_n9.py --humo                       (UN proceso: semilla 13391, T=12000, 4 brazos; JSON en datos/humo/)
  python experimentos/subida_n9/corre_n9.py --serie --desde 13301 --n 20 --pool 6    (SOLO el coordinador)
  python experimentos/subida_n9/corre_n9.py --serie --desde 13321 --n 20 --pool 6    (replica, SOLO el coordinador)
POOL: --pool o JUACO_POOL; 0 = un proceso. Los agentes no corren Pool. ERR-54: el crudo se escribe ANTES de resumir.
VOCABULARIO: "linaje", "cuerpo", "lee su propio estado", "lesion"; prohibido "sabe que va a morir", "quiere", "se sacrifica",
"coopera", "poblacion", "evoluciona".
"""
import argparse, json, os, platform, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun_n9 as K   # noqa: E402  (fija P.CARROS / RC.CARROS en esta carpeta, tambien en los procesos hijos)

P, J = K.P, K.J
DATOS = os.path.join(AQUI, 'datos'); HUMO = os.path.join(DATOS, 'humo')
DESDE = 13301; N_DEF = 20; T_DEF = 100000
SEM_HUMO = 13391; T_HUMO = 12000; SEM_MINI = 13399; T_MINI = 3000
MARGEN_PERSISTE = 15      # "pierde por persistencia": O3 persiste en >= 15 linajes-semilla mas (de 180) que el brazo lesionado
REF = 'O3'
VM_TOL = 0.10             # V-M: |media usada - media real| de E y de Ag en O3_LES_SI (enmienda 1). El humo dio 0.149 / 0.103; un
                          # primer tope de 0.15 quedaba justo encima del humo (ajustado al dato): se fija 0.10, el doble del arnes (0.05)


def tarea(args):
    seed, brazo, T = args
    t0 = time.time()
    r = P.run(seed, [brazo] * 9, T=T, pizarra=1, fundador_limpio=1)
    L = [J.resumen_linaje(d, seed) for d in r['linajes']]
    for x in L:
        tf, qf, nr = J.t_fund_reconstruido(x['telem']['vidas'], x['telem']['desc_por_vida'])
        x['t_fund_rec_ok'] = bool(tf[:200] == x['telem']['t_fund'] and qf == x['cola_final'] and nr == x['nac_reales'])
    les = [(d.get('carro') or {}).get('lesion') for d in r['linajes']]
    sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
    return dict(seed=seed, brazo=brazo, seg=round(time.time() - t0, 1), linajes=L, pista=r['pista'],
                R0_pista=round(sd / (sm + len(L)), 4), n_pizarra=len(r['pizarra_log']), lesion=les)


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def por_semilla(R):
    """semilla -> dict(persisten, R0 real eval mediana, cruza por mayoria, descendientes mediana)"""
    out = {}
    for c in R:
        xs = c['linajes']
        out[c['seed']] = dict(persisten=sum(x['persiste'] for x in xs), R0r=med([x['R0_real_eval'] for x in xs]),
                              cruza=bool(sum(x['cruza_real'] for x in xs) * 2 > len(xs)), desc=med([x['descendientes'] for x in xs]),
                              muertes=sum(x['muertes'] for x in xs), eval=sum(x['evaluable'] for x in xs))
    return out


def compara(Rref, Rx):
    """pareado por semilla: O3 contra el brazo X"""
    a = por_semilla(Rref); b = por_semilla(Rx); sem = sorted(set(a) & set(b))
    gp = sum(1 for s in sem if a[s]['persisten'] > b[s]['persisten']); pp = sum(1 for s in sem if a[s]['persisten'] < b[s]['persisten'])
    pr = [(a[s]['R0r'], b[s]['R0r']) for s in sem if a[s]['R0r'] is not None and b[s]['R0r'] is not None]
    gr = sum(1 for u, v in pr if u > v); prr = sum(1 for u, v in pr if u < v)
    return dict(semillas=len(sem), persiste_O3_gana=gp, persiste_X_gana=pp, persiste_empata=len(sem) - gp - pp,
                dif_persisten=sum(a[s]['persisten'] for s in sem) - sum(b[s]['persisten'] for s in sem),
                R0r_pares=len(pr), R0r_O3_gana=gr, R0r_X_gana=prr, R0r_dif_mediana=med([u - v for u, v in pr]),
                desc_dif_mediana=med([a[s]['desc'] - b[s]['desc'] for s in sem if a[s]['desc'] is not None and b[s]['desc'] is not None]))


def fila(R):
    xs = [x for c in R for x in c['linajes']]; ps = por_semilla(R); ns = len(R)
    les = [z for c in R for z in c['lesion'] if z and z.get('n')]
    lz = None
    if les:
        nn = sum(z['n'] for z in les)
        lz = dict(pasos=nn, E_real=round(sum(z['lev_real'][0] for z in les) / nn, 4), E_usado=round(sum(z['lev_usado'][0] for z in les) / nn, 4),
                  Ag_real=round(sum(z['lev_real'][1] for z in les) / nn, 4), Ag_usado=round(sum(z['lev_usado'][1] for z in les) / nn, 4),
                  dlev=round(sum(z['dlev'] for z in les) / nn, 4))
    return dict(semillas=ns, linajes_semilla=len(xs), evaluables=sum(x['evaluable'] for x in xs), casi_inmortales=sum(x['casi_inmortal'] for x in xs),
                R0_real_eval_med=med([x['R0_real_eval'] for x in xs]), R0_eval_med=med([x['R0_eval'] for x in xs]),
                sem_cruza_mayoria=sum(1 for v in ps.values() if v['cruza']), gana=bool(sum(1 for v in ps.values() if v['cruza']) >= 0.75 * ns),
                persisten=sum(x['persiste'] for x in xs),
                sem_estabiliza=sum(1 for c in R if sum(x['persiste'] for x in c['linajes']) * 2 > len(c['linajes'])),
                estabiliza=bool(sum(1 for c in R if sum(x['persiste'] for x in c['linajes']) * 2 > len(c['linajes'])) >= 0.75 * ns),
                muertes_med=med([x['muertes'] for x in xs]), nac_reales_med=med([x['nac_reales'] for x in xs]),
                descendientes_med=med([x['descendientes'] for x in xs]), fund_post10k_med=med([x['fund_post10k'] for x in xs]),
                sin_parir_med=med([x['frac_muere_sin_parir'] for x in xs]), vida_med=med([x['vida_med'] for x in xs]),
                muertes_vol=sum((x.get('muertes_vol') or 0) for x in xs), muertes=sum(x['muertes'] for x in xs),
                coherente=sum(x['coherente'] for x in xs), t_fund_rec_ok=sum(x['t_fund_rec_ok'] for x in xs),
                causas={k: sum(x['causas'][k] for x in xs) for k in ('hambre', 'sed', 'veneno', 'sal')}, lesion=lz)


def pierde(fr, fx, cmp_):
    """X PIERDE contra O3 (PREREGISTRO_n9.md §5): (a) O3 gana la ENMIENDA 5 y X no, o (b) O3 persiste en >= 15 linajes-semilla mas."""
    a = bool(fr['gana'] and not fx['gana']); b = bool(cmp_['dif_persisten'] >= MARGEN_PERSISTE)
    return dict(pierde=a or b, por_enm5=a, por_persistencia=b)


def predicciones(F, C, serie):
    """Las predicciones firmadas del PREREGISTRO_n9.md §4 (solo se leen en una SERIE de 20; en el humo se imprimen sin valor)."""
    o, si, ci, sn = F.get('O3'), F.get('O3_LES_SI'), F.get('O3_TERM_CIEGO'), F.get('CTRL_O3_SINTERM')
    P_ = []
    def p(cod, txt, cond):
        P_.append((cod, txt, None if cond is None else bool(cond)))
    if o:
        p('P1', "ANCLA: O3 gana la ENMIENDA 5 (>= 15/20) con R0 real eval mediana en [0.95, 0.99] y persisten >= 170/180",
          o['gana'] and o['R0_real_eval_med'] is not None and 0.95 <= o['R0_real_eval_med'] <= 0.99 and o['persisten'] >= 170)
    if o and si:
        p('P2', "L-SI: O3_LES_SI R0 real eval mediana en [0.55, 0.88], no gana (<= 5/20 por mayoria) y persisten <= 60/180",
          si['R0_real_eval_med'] is not None and 0.55 <= si['R0_real_eval_med'] <= 0.88 and si['sem_cruza_mayoria'] <= 5 and si['persisten'] <= 60)
        p('P3', "L-SI pareado: O3 persiste mas que O3_LES_SI en >= 17/20 semillas", C['O3_LES_SI']['persiste_O3_gana'] >= 17)
    if o and ci:
        p('P4', "L-RES (puede fallar; el creador la da por REFUTADA con p 0.55): O3_TERM_CIEGO PIERDE contra O3 (§5)",
          C['O3_TERM_CIEGO']['pierde']['pierde'])
        p('P5', "L-RES: O3_TERM_CIEGO muere mas que O3 (mediana de muertes por linaje-semilla >= 1.2x la de O3)",
          ci['muertes_med'] is not None and o['muertes_med'] and ci['muertes_med'] >= 1.2 * o['muertes_med'])
    if o and sn:
        p('P6', "SIN TERMINAL: CTRL_O3_SINTERM tiene 100-175 de 180 linajes-semilla evaluables (>= 5 muertes)",
          100 <= sn['evaluables'] <= 175)
        p('P7', "SIN TERMINAL: CTRL_O3_SINTERM R0 real eval mediana >= 0.90 (p 0.5; puede fallar en cualquiera de los dos sentidos)",
          sn['R0_real_eval_med'] is not None and sn['R0_real_eval_med'] >= 0.90)
    return P_


def veredicto(F, C):
    """§6 del preregistro, POR SERIE (la declaracion exige serie Y replica con el mismo veredicto)."""
    o = F.get('O3')
    if not o or not o['gana']: return 'NO EVALUABLE (el ancla O3 no gana la ENMIENDA 5 en estas semillas)'
    hsi = C.get('O3_LES_SI', {}).get('pierde', {}).get('pierde'); hres = C.get('O3_TERM_CIEGO', {}).get('pierde', {}).get('pierde')
    if hsi and hres: return 'FUNCIONA en esta serie (H-SI y H-RES: las dos lesiones pierden)'
    if hsi: return 'HAY ALGO MODESTO en esta serie (H-SI: pierde la lesion del estado propio; H-RES no: la reserva no hace falta)'
    if hres: return 'HAY ALGO MODESTO en esta serie (H-RES: pierde la lesion de la reserva; H-SI no)'
    return 'NO en esta serie (ninguna lesion pierde: el cruce no depende de leer el estado propio ni la reserva)'


def chequeos(log):
    ok = True
    for r, m, s, b in K.verifica_shas():
        log(f"  sha {r} {m} {'OK' if b else 'DISTINTO de ' + s}"); ok &= b
    esp, medido, b = K.verifica_construccion(); log(f"  construccion por anclas reproducible: {'OK' if b else 'FALLA ' + str(medido)}"); ok &= b
    for n in K.BRAZOS + K.ARNES:
        v = K.RC.revisa(n); log(f"  chequeo estatico {n}: {'PASA' if not v else 'RECHAZADO ' + str(v[:2])}"); ok &= not v
    ide = J.identidad_corta(); log(f"  identidad corta del juez (FABRICA == organismo_f9c REL, s=1, T=5000): {'OK' if ide['ok'] else 'FALLA'}"); ok &= ide['ok']
    a = P.run(SEM_MINI, ['O3'] * 9, T=T_MINI, pizarra=1, fundador_limpio=1)
    b2 = P.run(SEM_MINI, ['O3_LES_OFF'] * 9, T=T_MINI, pizarra=1, fundador_limpio=1)
    mi = K.normaliza(a) == K.normaliza(b2, 'O3_LES_OFF'); log(f"  mini identidad O3_LES_OFF == O3 (s{SEM_MINI}, T={T_MINI}): {'OK' if mi else 'FALLA'}"); ok &= mi
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--desde', type=int, default=DESDE); ap.add_argument('--n', type=int, default=N_DEF)
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--brazos', default=','.join(K.BRAZOS))
    ap.add_argument('--pool', type=int, default=int(os.environ.get('JUACO_POOL', 0)))
    a = ap.parse_args()
    if a.humo == a.serie: raise SystemExit('corre_n9: elegir --humo o --serie')
    brazos = [b for b in a.brazos.split(',') if b]
    if REF not in brazos or any(b not in K.BRAZOS for b in brazos): raise SystemExit(f'corre_n9: brazos validos {K.BRAZOS}, con O3')
    if a.humo:
        semillas = [SEM_HUMO]; T = a.T or T_HUMO; pool = 0; dest = HUMO; et = f"n9_humo_s{SEM_HUMO}_T{T}"
    else:
        semillas = list(range(a.desde, a.desde + a.n)); T = a.T or T_DEF; pool = a.pool; dest = DATOS
        et = f"n9_serie_s{semillas[0]}-{semillas[-1]}_T{T}"
    os.makedirs(dest, exist_ok=True)
    sel = time.strftime('%Y%m%d_%H%M%S'); pre = os.path.join(dest, f"{et}_{sel}")
    LOGF = open(pre + '.log', 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    log(f"corre_n9 · {et} · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'}")
    log(f"  brazos {brazos} · semillas {semillas[0]}-{semillas[-1]} · T={T} · monocultivo de 9 · fundador limpio 1 · pizarra 1")
    if not chequeos(log):
        log('  UN CHEQUEO FALLA -> NO se corre nada.'); return 1
    tareas = [(s, b, T) for b in brazos for s in semillas]
    R = []
    if pool and pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as PL:
            for x in PL.imap_unordered(tarea, tareas):
                R.append(x); log(f"  [{time.time() - t0:7.1f}s] {x['brazo']:16s} s{x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']}")
    else:
        for tk in tareas:
            x = tarea(tk); R.append(x)
            log(f"  [{time.time() - t0:7.1f}s] {x['brazo']:16s} s{x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']} · muertes "
                f"{sum(l['muertes'] for l in x['linajes'])} · persisten {sum(l['persiste'] for l in x['linajes'])}/9 · R0 real "
                f"{[l['R0_real'] for l in x['linajes']]}")
    R.sort(key=lambda x: (x['brazo'], x['seed']))
    meta = dict(etiqueta=et, sello=sel, semillas=semillas, T=T, brazos=brazos, pool=pool, humo=a.humo,
                sha_carros={b: K.h16(os.path.join(K.CARROS_N9, b + '.py')) for b in brazos + list(K.ARNES)},
                sha_originales={r: m for r, m, s, ok in K.verifica_shas()}, sha_runner=K.h16(os.path.abspath(__file__)),
                sha_comun=K.h16(os.path.join(AQUI, 'comun_n9.py')), margen_persiste=MARGEN_PERSISTE, preregistro='PREREGISTRO_n9.md')
    crudo = pre + '.json'
    json.dump(dict(meta=meta, corridas=R), open(crudo, 'w', encoding='utf-8'), ensure_ascii=False)   # ERR-54: crudo ANTES de resumir
    log(f"  CRUDO {crudo} (sha {K.h16(crudo)})")
    por = {b: [c for c in R if c['brazo'] == b] for b in brazos}
    juez = {}
    for b in brazos:   # la letra de la carrera, tal cual (ENMIENDA 5 y 6)
        e = J.resumen_err99(por[b], log, f"r2mono_{b}"); e['ronda2'] = J.resumen_r2(por[b], log, f"r2mono_{b}"); juez[b] = e
    F = {b: fila(por[b]) for b in brazos}
    C = {}
    for b in brazos:
        if b == REF: continue
        c = compara(por[REF], por[b]); c['pierde'] = pierde(F[REF], F[b], c); C[b] = c
    log(f"\nTABLA n9 · {et}")
    log(f"  {'brazo':16s} {'gana(E5)':>9} {'estab(E6)':>9} {'R0real med':>10} {'persisten':>9} {'evaluab':>7} {'muertes med':>11} "
        f"{'nac reales':>10} {'desc med':>8} {'sin parir':>9} {'vida med':>8}  causas h/s/v/sal")
    for b in brazos:
        f = F[b]; cz = f['causas']
        log(f"  {b:16s} {str(f['sem_cruza_mayoria']) + '/' + str(f['semillas']):>9} {str(f['sem_estabiliza']) + '/' + str(f['semillas']):>9} "
            f"{str(f['R0_real_eval_med']):>10} {str(f['persisten']) + '/' + str(f['linajes_semilla']):>9} {f['evaluables']:>7} "
            f"{str(f['muertes_med']):>11} {str(f['nac_reales_med']):>10} {str(f['descendientes_med']):>8} {str(f['sin_parir_med']):>9} "
            f"{str(f['vida_med']):>8}  {cz['hambre']}/{cz['sed']}/{cz['veneno']}/{cz['sal']}"
            f"{'  lesion ' + str(f['lesion']) if f['lesion'] else ''}")
    for b, c in C.items():
        log(f"  O3 contra {b}: persistencia pareada O3 gana/X gana/empate {c['persiste_O3_gana']}/{c['persiste_X_gana']}/{c['persiste_empata']} "
            f"(dif {c['dif_persisten']}) · R0 real pareado O3/X {c['R0r_O3_gana']}/{c['R0r_X_gana']} de {c['R0r_pares']} (dif mediana "
            f"{c['R0r_dif_mediana']}) · descendientes dif mediana {c['desc_dif_mediana']} -> X {'PIERDE' if c['pierde']['pierde'] else 'NO pierde'} "
            f"(por E5 {c['pierde']['por_enm5']}, por persistencia {c['pierde']['por_persistencia']})")
    PR = predicciones(F, C, not a.humo)
    log(f"\nPREDICCIONES FIRMADAS (PREREGISTRO_n9.md §4){' -- HUMO de una semilla: SIN VALOR, solo se imprimen' if a.humo else ''}")
    for cod, txt, v in PR:
        log(f"  {cod} {txt} -> {'(humo)' if a.humo else ('SE CUMPLE' if v else 'NO se cumple')}{' [medido: ' + ('si' if v else 'no') + ']' if a.humo else ''}")
    ver = veredicto(F, C)
    lz = (F.get('O3_LES_SI') or {}).get('lesion')
    if lz:   # V-M (enmienda 1 del preregistro, tras el humo y antes de la serie): condicion de LECTURA de H-SI, no puerta
        dE = abs(lz['E_usado'] - lz['E_real']); dA = abs(lz['Ag_usado'] - lz['Ag_real']); vm = dE <= VM_TOL and dA <= VM_TOL
        ver += (f" · V-M {'se cumple' if vm else 'NO se cumple'} (|dE| {dE:.3f}, |dAg| {dA:.3f}, tope {VM_TOL}): H-SI se lee como "
                + ("'estado propio de otro momento, misma distribucion'" if vm else "'estado propio desfasado y SESGADO hacia estados anteriores'"))
    log(f"\nVEREDICTO {'(HUMO: sin valor) ' if a.humo else ''}{ver}")
    log(f"  coherencia fisica {sum(F[b]['coherente'] for b in brazos)}/{sum(F[b]['linajes_semilla'] for b in brazos)} · t_fund reconstruible "
        f"{sum(F[b]['t_fund_rec_ok'] for b in brazos)}/{sum(F[b]['linajes_semilla'] for b in brazos)} · escrituras en pizarra {sum(c['n_pizarra'] for c in R)}")
    res = pre + '_resumen.json'
    json.dump(dict(meta=meta, tabla=F, comparaciones=C, predicciones=PR, veredicto=ver, juez=juez), open(res, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1, default=str)
    log(f"  RESUMEN {res}")
    log(f"\nTerminado en {time.time() - t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
