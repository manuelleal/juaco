"""corre_mmr.py — CONDICIONES / LA MONEDA DEL MURO, REPLICA (1-oct-2026, creador). Preregistro: PREREGISTRO_moneda_muro_rep.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE ES: la REPLICA de condiciones/moneda_muro (EXPLORA: CONSERVA en el umbral, commit 857bbb87). El MISMO instrumento, IMPORTADO por sha
(corre_mm.py d45a5ed42e8514df: trabajo, cadena, carga, elige, siembra_L; no se copia ni se toca), con SEMILLAS NUEVAS y n = 10 cadenas
por brazo. Lo unico que este archivo agrega: el modo (semillas, n), LA LETRA de la replica (dos lecturas declaradas + el cruce de la
prueba final como CO-PRINCIPAL), los candados y el bloque contra el explora.

ENTRADA (regla 14): TODA corrida ES corre_mm.trabajo((brazo, i, carpeta, modo)) con el modo registrado en corre_mm.MODOS (mismas llaves
que 'explora'; solo cambian ind, base_pas y base_pru). Con el modo 'explora' (semillas viejas) este runner ES corre_mm (arnes F).

BRAZOS: moneda_L (CANDIDATO) · neutra_L (CONTROL que puede fallar), los de moneda_muro.
SEMILLAS NUEVAS (grep 1-oct: \\b647[123]dd\\b no aparece en ningun .py ni .md de PROYECTOS/JUACO):
  pasaje p del indice i (1..10): 647100 + 10 i + p (647110-647205), LAS MISMAS en los dos brazos (pareado)
  prueba final del indice i: 647300 + i (647301-647310), LA MISMA en los dos brazos (pareado; NUEVAS: el cruce es co-principal)
  humo: indice 14 (pasajes 647240-647241, prueba 647390) · arnes: indice 15 (647250.., prueba 647395)
Pool: MAXIMO 2. --reanuda sigue la ultima carpeta serie_* y REINTENTA los JSON con aborto (los buenos no se recorren). ERR-115.

  python experimentos/organelos/condiciones/moneda_muro_rep/identidad_mmr.py                 # arnes (escribe identidad_mmr_salida.txt)
  python experimentos/organelos/condiciones/moneda_muro_rep/corre_mmr.py --humo              # 1 proceso, 6 corridas, 160 000 pasos
  python experimentos/organelos/condiciones/moneda_muro_rep/corre_mmr.py --serie --pool 2    # 20 cadenas (6 x 100k) + 20 pruebas 100k
  python experimentos/organelos/condiciones/moneda_muro_rep/corre_mmr.py --serie --pool 2 --reanuda
  python experimentos/organelos/condiciones/moneda_muro_rep/corre_mmr.py --lee datos/serie_<fecha>
"""
import argparse, hashlib, json, os, platform, statistics as st, subprocess, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
MMD = os.path.join(RAIZ, 'experimentos', 'organelos', 'condiciones', 'moneda_muro')
for _d in (AQUI, MMD):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_mm as MM   # el instrumento del explora (se IMPORTA, no se toca; sha fijado)
MU = MM.MU; M = MM.M

PRERREGISTRO = 'PREREGISTRO_moneda_muro_rep.md'
DATOS = os.path.join(AQUI, 'datos')
SHAS = {os.path.join(MMD, 'corre_mm.py'): 'd45a5ed42e8514df', os.path.join(MMD, 'identidad_mm.py'): 'e9e3a7a5b6576f30',
        os.path.join(MMD, 'sim_mm.py'): 'ae805f42e2e6f26c'}
# GUARDADO del explora (commit 857bbb87): su lectura (bloque) y el pasaje moneda_L i1 p0 (arnes F: reproduccion bit a bit)
EXPL = os.path.join(MMD, 'datos', 'explora_20260930_224403')
REF_EXPL = (os.path.join(EXPL, 'lectura_mm.json'), '1697a7d2bdc5dbd3')
REF_PAS = (os.path.join(EXPL, 'pasaje_moneda_L_i1_p0.json'), '45285799cd2a5c52')

BRAZOS = ('moneda_L', 'neutra_L')
MODOS = {'serie': dict(ind=list(range(1, 11)), npas=6, T_pas=100000, T_pru=100000, base_pas=647100, base_pru=647300, brazos=BRAZOS),
         'humo': dict(ind=[14], npas=2, T_pas=30000, T_pru=20000, base_pas=647100, base_pru=647376, brazos=BRAZOS)}
NOMBRE = {'serie': 'rep_serie', 'humo': 'rep_humo'}   # como se llaman dentro de corre_mm.MODOS (no pisan 'explora' ni 'humo' de alli)
POOL_MAX = 2
# LA LETRA (PREREGISTRO sec. 5). DECIDE la lectura ESTRICTA (b): moneda_L > neutra_L, empates en contra.
CONSERVA_K = 7; CONSERVA_MED = 0.40; PURGA_K = 8; MITAD = 0.5; RESPALDO_MAX = 0.25; FIJA = 0.95; PIERDE = 0.05
CRUCE_K = 7; CRUCE_D = 9      # co-principal: gana (estricto) en >= 7/10 Y suma de diferencias >= 9 (de 90)
VEREDICTOS = ('CONSERVA', 'PURGA', 'INDETERMINADO')


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def registra_modos():
    for k, v in MODOS.items(): MM.MODOS[NOMBRE[k]] = dict(v)
registra_modos()
def sem_pas(m, i, p): return MM.sem_pas(m, i, p)
def sem_pru(m, i): return MM.sem_pru(m, i)


def trabajo(args):
    """UN trabajo = una cadena (brazo, indice) = corre_mm.trabajo con el modo de la replica. Se registra en CADA worker."""
    brazo, i, carpeta, modo = args
    registra_modos()
    return MM.trabajo((brazo, i, carpeta, NOMBRE.get(modo, modo)))


# ------------------------------------------------------------------ LA LETRA
def _med(xs):
    xs = [x for x in xs if x is not None]; return round(float(st.median(xs)), 4) if xs else None


def lectura_frac(mo, ne, ind):
    """mo, ne: {i: fraccion A final}. Las DOS lecturas declaradas y la que decide (estricta)."""
    I = [i for i in ind if i in mo and i in ne]
    ge = sum(1 for i in I if mo[i] >= ne[i]); gt = sum(1 for i in I if mo[i] > ne[i]); eq = sum(1 for i in I if mo[i] == ne[i])
    mitad = sum(1 for i in I if ne[i] > 0 and mo[i] <= MITAD * ne[i])
    med = _med([mo[i] for i in I]); I5 = I[:5]; med5 = _med([mo[i] for i in I5]); ge5 = sum(1 for i in I5 if mo[i] >= ne[i])
    return dict(n=len(I), ge=ge, gt=gt, empates=eq, empates_arriba=sum(1 for i in I if mo[i] == ne[i] and mo[i] >= FIJA), mitad=mitad,
                mediana=med, estricta_b=bool(gt >= CONSERVA_K and med is not None and med >= CONSERVA_MED),
                original_a10=bool(len(I) > 0 and ge == len(I) and len(I) == len(ind) and med is not None and med >= CONSERVA_MED),
                original_a5=bool(len(I5) == 5 and ge5 == 5 and med5 is not None and med5 >= CONSERVA_MED),
                estricta_8=bool(gt >= CONSERVA_K + 1 and med is not None and med >= CONSERVA_MED))


def lectura_cruce(cm, cn, ind):
    """cm, cn: {i: cruzan de 9 en la prueba final}. Pareado; empates en contra de los dos lados."""
    I = [i for i in ind if i in cm and i in cn]
    g = sum(1 for i in I if cm[i] > cn[i]); p = sum(1 for i in I if cm[i] < cn[i]); D = sum(cm[i] - cn[i] for i in I)
    if g >= CRUCE_K and D >= CRUCE_D: v = 'CRUZA MAS'
    elif p >= CRUCE_K and -D >= CRUCE_D: v = 'CRUZA MENOS'
    else: v = 'SIN DIFERENCIA'
    um = (g in (CRUCE_K - 1, CRUCE_K) and D > 0) or (p in (CRUCE_K - 1, CRUCE_K) and D < 0)
    return dict(n=len(I), gana=g, pierde=p, empata=len(I) - g - p, D=D, suma_moneda_L=sum(cm[i] for i in I), suma_neutra_L=sum(cn[i] for i in I),
                veredicto=v, en_umbral=bool(um))


def letra(C, P_, ind, abortos, expl_ok, arnes_ok):
    """PREREGISTRO sec. 5. C[brazo][i] = cadena (corre_mm.cadena); P_[brazo][i] = fila de la prueba final."""
    n = len(ind); mo = 'moneda_L'; ne = 'neutra_L'
    fin = {b: {i: C[b][i]['f'][-1] for i in C.get(b, {})} for b in BRAZOS}
    cz = {b: {i: int(f['cruzan']) for i, f in P_.get(b, {}).items()} for b in BRAZOS}
    pas = [c for b in BRAZOS for c in C.get(b, {}).values()]
    n_pas = sum(len(c['f']) for c in pas); n_resp = sum(sum(c['respaldo']) for c in pas)
    actua = sum(1 for c in pas for a, b in zip(c['f'], c['f_sombra_vieja']) if a != b)
    pareada = all(P_[mo][i]['seed'] == P_[ne][i]['seed'] for i in ind if i in P_.get(mo, {}) and i in P_.get(ne, {}))
    val = dict(abortos_0=(len(abortos) == 0),
               completas=all(len(C.get(b, {})) == n and len(P_.get(b, {})) == n for b in BRAZOS),
               f_ini_05=all(c['f_ini'] == 0.5 for c in pas),
               moneda_actua=(actua > 0),
               respaldo_raro=(n_pas > 0 and n_resp / n_pas <= RESPALDO_MAX),
               prueba_pareada=bool(pareada),
               explora_sha=bool(expl_ok), arnes=bool(arnes_ok))
    valido = all(val.values())
    F = lectura_frac(fin[mo], fin[ne], ind); X = lectura_cruce(cz[mo], cz[ne], ind)
    if not valido: ver = 'NO SE LEE'
    elif F['estricta_b']: ver = 'CONSERVA'
    elif F['mitad'] >= PURGA_K: ver = 'PURGA'
    else: ver = 'INDETERMINADO'
    um = F['gt'] in (CONSERVA_K - 1, CONSERVA_K) or F['mitad'] in (PURGA_K - 1, PURGA_K) or \
        (F['gt'] >= CONSERVA_K and F['mediana'] is not None and abs(F['mediana'] - CONSERVA_MED) <= 0.05)
    def cuenta(b, f): return sum(1 for v in fin[b].values() if f(v))
    def delta(b):
        d = [y - x for c in C.get(b, {}).values() for x, y in zip([c['f_ini']] + c['f'][:-1], c['f']) if 0 < x < 1]
        return round(st.mean(d), 4) if d else None
    def med_ele(b): return _med([v for c in C.get(b, {}).values() for v in c['n_ele']])
    return dict(validez=val, veredicto=ver, en_umbral=bool(um), cruce=dict(X, veredicto=(X['veredicto'] if valido else 'NO SE LEE')),
                fraccion=F, neutra_L_mediana=_med(list(fin[ne].values())),
                sobre_inicial={b: sum(1 for v in fin[b].values() if v > 0.5) for b in BRAZOS},   # descriptivo (H-1): 'moneda sube' o 'neutra baja'

                moneda_L_media=(round(st.mean(fin[mo].values()), 4) if fin[mo] else None),
                neutra_L_media=(round(st.mean(fin[ne].values()), 4) if fin[ne] else None),
                fijadas={b: cuenta(b, lambda v: v >= FIJA) for b in BRAZOS}, perdidas={b: cuenta(b, lambda v: v <= PIERDE) for b in BRAZOS},
                delta_pasaje={b: delta(b) for b in BRAZOS}, elegidos_mediana={b: med_ele(b) for b in BRAZOS},
                cruzan_pasaje_media={b: (round(st.mean([v for c in C[b].values() for v in c['cruzan_pas']]), 3) if C.get(b) else None) for b in BRAZOS},
                pasajes=n_pas, pasajes_con_respaldo=n_resp, pasajes_donde_la_moneda_difiere=actua,
                final={b: {str(i): v for i, v in sorted(d.items())} for b, d in fin.items()},
                cruzan={b: {str(i): v for i, v in sorted(d.items())} for b, d in cz.items()})


def explora_guardado():
    """La lectura GUARDADA del explora (sha16), releida con la letra de la replica (descriptivo: n = 5)."""
    s = h16(REF_EXPL[0]) if os.path.exists(REF_EXPL[0]) else None
    if s != REF_EXPL[1]: return False, f"lectura_mm.json del explora sha {s} != {REF_EXPL[1]}", {}
    L = json.load(open(REF_EXPL[0], encoding='utf-8')); ind = [1, 2, 3, 4, 5]
    fin = {b: {int(i): v for i, v in L['letra']['final'][b].items()} for b in BRAZOS}
    cz = {b: {int(i): int(f['cruzan']) for i, f in L['prueba'][b].items()} for b in BRAZOS}
    return True, 'sha OK', dict(veredicto=L['letra']['veredicto'], final=L['letra']['final'], fraccion=lectura_frac(fin['moneda_L'], fin['neutra_L'], ind),
                                cruce=lectura_cruce(cz['moneda_L'], cz['neutra_L'], ind), neutra_L_mediana=L['letra']['neutra_L_mediana'])


def bloque(L, E):
    """BLOQUE contra el explora (PREREGISTRO sec. 6). Dos renglones: la fraccion (la letra) y el cruce (co-principal)."""
    v = L['veredicto']; x = L['cruce']['veredicto']
    if v == 'NO SE LEE': return dict(fraccion='NO SE LEE', cruce='NO SE LEE', titular='NO SE LEE')
    um = ' · EN EL UMBRAL' if L['en_umbral'] else ''
    if v == 'CONSERVA': bf = 'REPLICA con letra estricta; el explora estaba en el umbral (4/5 con esta letra)' + um
    elif v == 'PURGA': bf = 'NO REPLICA y se INVIERTE: explora CONSERVA (umbral), replica PURGA'
    else: bf = 'NO REPLICA: explora CONSERVA (umbral), replica INDETERMINADO -> el CONSERVA del explora no se sostiene'
    de = (E.get('cruce') or {}).get('D')
    if x == 'CRUZA MENOS': bx = f"moneda_L NO cruza mas que neutra_L: cruza MENOS (explora D {de} de 45, descriptivo; replica por letra)"
    elif x == 'CRUZA MAS': bx = f"moneda_L cruza MAS en la replica (contra el explora, D {de} de 45): cruce sin replica, no es declaracion"
    else: bx = f"moneda_L NO cruza mas que neutra_L: SIN DIFERENCIA en la replica (explora D {de} de 45, descriptivo)"
    base = 'replica con letra estricta; el explora estaba en el umbral (4/5 con esta letra)'
    if v == 'CONSERVA' and x == 'CRUZA MAS': t = f"FUNCIONA{um}: moneda_L supera a neutra_L y no cae ({base}) y cruza mas; cruce sin replica: no es declaracion"
    elif v == 'CONSERVA': t = f"HAY ALGO MODESTO{um}: moneda_L supera a neutra_L y no cae ({base}); NO cruza mas"
    else: t = 'NO: el CONSERVA del explora no replica'
    return dict(fraccion=bf, cruce=bx, titular=t)


def predicciones(L):
    F = L['fraccion']; X = L['cruce']; v = L['veredicto']; x = X['veredicto']; em = L['elegidos_mediana']
    return [('R1', 'veredicto CONSERVA (lectura estricta, >= 7/10 y mediana >= 0.40)', v, v == 'CONSERVA', 0.45),
            ('R2', 'veredicto INDETERMINADO', v, v == 'INDETERMINADO', 0.47),
            ('R3', 'veredicto PURGA', v, v == 'PURGA', 0.05),
            ('R4', 'cruce: SIN DIFERENCIA', x, x == 'SIN DIFERENCIA', 0.68),
            ('R5', 'cruce: CRUZA MENOS (como apunto el explora)', x, x == 'CRUZA MENOS', 0.25),
            ('R6', 'cruce: CRUZA MAS (la hipotesis del director)', x, x == 'CRUZA MAS', 0.04),
            ('R7', 'neutra_L: mediana de la fraccion A final <= 0.30 (explora 0.14)', L['neutra_L_mediana'],
             L['neutra_L_mediana'] is not None and L['neutra_L_mediana'] <= 0.30, 0.60),
            ('R8', 'moneda_L: mediana de la fraccion A final >= 0.40 (explora 0.80)', F['mediana'], F['mediana'] is not None and F['mediana'] >= 0.40, 0.60),
            ('R9', 'prueba moneda_L: suma de cruzan (de 90) en [30, 50]', X['suma_moneda_L'], 30 <= X['suma_moneda_L'] <= 50, 0.70),
            ('R10', 'suma de diferencias de cruce D (moneda_L - neutra_L) < 0', X['D'], X['D'] < 0, 0.65),
            ('R11', 'elegidos por pasaje (mediana): neutra_L > moneda_L (explora 7 contra 5)', em,
             em['moneda_L'] is not None and em['neutra_L'] is not None and em['neutra_L'] > em['moneda_L'], 0.70),
            ('R12', 'empates exactos de fraccion final <= 2 de 10', F['empates'], F['empates'] <= 2, 0.75),
            ('R13', 'la letra original escalada (>= en 10/10) se cumple', F['original_a10'], bool(F['original_a10']), 0.12)]


def arnes_pasado():
    f = os.path.join(AQUI, 'identidad_mmr_salida.txt')
    if not os.path.exists(f): return False, 'sin salida del arnes'
    t = open(f, encoding='utf-8').read()
    need = [h16(os.path.abspath(__file__)), h16(os.path.join(AQUI, 'identidad_mmr.py'))]
    ok = 'ARNES: PASA' in t and all(s in t for s in need)
    return ok, ('PASA con los shas actuales' if ok else f'no PASA o no cita los shas actuales {need}')


def lee(carpeta, log=print, modo=None):
    modo = modo or ('humo' if os.path.basename(os.path.normpath(carpeta)).startswith('humo') else 'serie')
    m = MODOS[modo]; registra_modos()
    C, P_, _refs, abortos, _rok, _rtx = MM.carga(carpeta, NOMBRE[modo])   # la carga del explora (regla 14); sin referencias de mutacion
    aok, atxt = arnes_pasado(); eok, etxt, E = explora_guardado()
    L = letra(C, P_, m['ind'], abortos, eok, aok)
    log(f"\n================ LECTURA moneda del muro REPLICA · {modo} · {carpeta}")
    log(f"  arnes: {atxt} · explora guardado: {etxt} · abortos: {abortos}")
    for b in m['brazos']:
        for i in sorted(C.get(b, {})):
            c = C[b][i]
            log(f"  {b:8s} i{i}: fraccion A  ini {c['f_ini']} -> p0..p{len(c['f'])-1} {c['f']}")
            log(f"  {'':8s}     sombra (moneda vieja) {c['f_sombra_vieja']} · elegidos {c['n_ele']} · establecidos {c['est_n']} · respaldo {[int(r) for r in c['respaldo']]}")
            log(f"  {'':8s}     listas {c['n_listas']} · intacta {c['intacta']} · mutadas (suma) {c['mutadas']} · arrastre>= {c['arrastre']} · partos {c['partos']} · cruzan en el pasaje {c['cruzan_pas']}")
    for i in m['ind']:
        fm = P_['moneda_L'].get(i); fn = P_['neutra_L'].get(i)
        if fm and fn:
            log(f"  prueba i{i} s{fm['seed']}: moneda_L cruzan {fm['cruzan']}/9 (R0 med {fm['R0_med']}, fund med {fm['fund_med']}) · "
                f"neutra_L cruzan {fn['cruzan']}/9 (R0 med {fn['R0_med']}, fund med {fn['fund_med']}) · dif {fm['cruzan'] - fn['cruzan']:+d}")
    F = L['fraccion']; X = L['cruce']
    log(f"  validez: {L['validez']}")
    log(f"  final: {L['final']}")
    log(f"  FRACCION (decide la ESTRICTA): moneda_L > neutra_L en {F['gt']}/{F['n']} (corte {CONSERVA_K}) · mediana moneda_L {F['mediana']} (corte {CONSERVA_MED}) "
        f"· <= 0.5 x neutra en {F['mitad']}/{F['n']} (corte PURGA {PURGA_K}) · empates {F['empates']} (arriba, >= {FIJA}: {F['empates_arriba']})")
    log(f"  lecturas declaradas que NO deciden: original escalada (>= en 10/10 y mediana): {F['original_a10']} ({F['ge']}/{F['n']}) · "
        f"original sobre las 5 primeras (>= en 5/5 y mediana de 5): {F['original_a5']} · estricta en >= {CONSERVA_K + 1}/10: {F['estricta_8']}")
    log(f"  CRUCE (co-principal, pareado): moneda_L {X['suma_moneda_L']} vs neutra_L {X['suma_neutra_L']} (de {9 * X['n']}) · D {X['D']:+d} (corte +-{CRUCE_D}) · "
        f"gana {X['gana']} · empata {X['empata']} · pierde {X['pierde']} (corte {CRUCE_K}) -> {X['veredicto']}{' · EN EL UMBRAL' if X['en_umbral'] else ''}")
    log(f"  DESCRIPTIVO que NO decide (moneda sube o neutra baja): mediana final neutra_L {L['neutra_L_mediana']} · moneda_L {F['mediana']} · "
        f"cadenas que terminan por encima de su 0.50 inicial: moneda_L {L['sobre_inicial']['moneda_L']}/{F['n']} · neutra_L {L['sobre_inicial']['neutra_L']}/{F['n']}")
    for k in ('neutra_L_mediana', 'moneda_L_media', 'neutra_L_media', 'fijadas', 'perdidas', 'delta_pasaje', 'elegidos_mediana', 'cruzan_pasaje_media',
              'pasajes', 'pasajes_con_respaldo', 'pasajes_donde_la_moneda_difiere'):
        log(f"  {k}: {L[k]}")
    pq = predicciones(L) if modo == 'serie' else []
    for q in pq: log(f"  {q[0]} {q[1]} (p {q[4]}): medido {q[2]} -> {'CUMPLE' if q[3] else 'REFUTADA'}")
    B = bloque(L, E)
    if E:
        log(f"  EXPLORA guardado (n 5): veredicto alli {E['veredicto']} · con la lectura estricta: > en {E['fraccion']['gt']}/5, >= en {E['fraccion']['ge']}/5, "
            f"mediana {E['fraccion']['mediana']} (neutra {E['neutra_L_mediana']}) · cruce {E['cruce']['suma_moneda_L']} vs {E['cruce']['suma_neutra_L']} de 45 "
            f"(D {E['cruce']['D']:+d}; gana {E['cruce']['gana']}, empata {E['cruce']['empata']}, pierde {E['cruce']['pierde']})")
    pre = 'HUMO (no cuenta; 1 cadena, 2 pasajes de 30k): ' if modo == 'humo' else ''
    out = os.path.join(carpeta, 'lectura_mmr.json')
    json.dump(dict(modo=modo, letra=L, bloque=(B if modo == 'serie' else None), explora=E,
                   cadenas={b: {str(i): {k: v for k, v in c.items() if k != 'siembra_final'} for i, c in d.items()} for b, d in C.items()},
                   prueba={b: {str(i): f for i, f in d.items()} for b, d in P_.items()}, abortos=abortos,
                   predicciones=[[q[0], q[1], q[2], bool(q[3]), q[4]] for q in pq],
                   preregistro=PRERREGISTRO, sha_runner=h16(os.path.abspath(__file__)), sha_instrumento=SHAS[os.path.join(MMD, 'corre_mm.py')]),
              open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    log(f"  LECTURA {out}")
    log(f"VEREDICTO ({PRERREGISTRO} sec. 5): {pre}fraccion {L['veredicto']}{' (EN EL UMBRAL)' if L['en_umbral'] and L['veredicto'] != 'NO SE LEE' else ''} · cruce {L['cruce']['veredicto']}")
    if modo == 'serie':
        log(f"BLOQUE contra el explora · fraccion: {B['fraccion']}")
        log(f"BLOQUE contra el explora · cruce: {B['cruce']}")
        log(f"TITULAR: {B['titular']}")
    return L


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    log("  -- verifica de corre_mm (corre_mut y, por cascada, corre_moneda, sentidos_muro, corre_bp, V143_BQ3, pista, juez, carros):")
    ok &= MM.verifica(lambda s: log('  ' + s))
    return ok


def git_limpio(archivos, raiz=RAIZ):
    """Candado: cada archivo commiteado y sin cambios contra HEAD. Devuelve None o el texto del fallo."""
    for r in archivos:
        rel = os.path.relpath(r, raiz).replace(os.sep, '/')
        t = subprocess.run(['git', '-C', raiz, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
        c = subprocess.run(['git', '-C', raiz, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
        if not (t and c): return f"git: {rel} commiteado {t} · sin cambios vs HEAD {c} (la serie exige todo commiteado)"
    return None


def ARCHIVOS():
    return [os.path.join(AQUI, f) for f in (PRERREGISTRO, 'corre_mmr.py', 'identidad_mmr.py', 'identidad_mmr_salida.txt', 'sim_mmr.py')] + list(SHAS)


def guarda(reanuda, datos=None, git=git_limpio):
    """Candados de --serie (PREREGISTRO sec. 9): veredicto previo, carpeta previa sin --reanuda, --reanuda sin carpeta, git limpio."""
    datos = datos or DATOS
    previas = sorted(d for d in os.listdir(datos) if d.startswith('serie_') and os.path.isdir(os.path.join(datos, d))) if os.path.isdir(datos) else []
    for d in previas:
        rj = os.path.join(datos, d, 'lectura_mmr.json')
        if os.path.exists(rj):
            v = (json.load(open(rj, encoding='utf-8')).get('letra') or {}).get('veredicto')
            if v in VEREDICTOS: return f"{d}/lectura_mmr.json ya tiene veredicto {v}: no se re-corre"
    if previas and not reanuda: return f"ya existe {previas[-1]}: solo --reanuda (cortada o NO SE LEE)"
    if reanuda and not previas: return "--reanuda: no hay carpeta serie_* que seguir"
    return git(ARCHIVOS())


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--serie', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool: maximo {POOL_MAX}")
    if a.humo and (a.pool or a.reanuda): raise SystemExit("--humo: sin Pool (un proceso) y sin --reanuda")
    if a.lee:
        c = a.lee if os.path.isabs(a.lee) else os.path.join(AQUI, a.lee)
        if not os.path.isdir(c): raise SystemExit(f"--lee: no existe {c}")
        LOGF = open(os.path.join(c, 'lectura.txt'), 'w', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        lee(c, log); return 0
    modo = 'humo' if a.humo else 'serie'
    m = MODOS[modo]; os.makedirs(DATOS, exist_ok=True)
    if modo == 'serie':
        e = guarda(a.reanuda)
        if e: raise SystemExit(f"NO SE CORRE (candado): {e}")
    prev = sorted(d for d in os.listdir(DATOS) if d.startswith(modo + '_') and os.path.isdir(os.path.join(DATOS, d)))
    carpeta = os.path.join(DATOS, prev[-1] if (a.reanuda and prev) else time.strftime(f'{modo}_%Y%m%d_%H%M%S'))
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time()
    log(f"CORRE_MMR · {modo} · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {platform.python_version()} · pool {a.pool or 'NO'} · "
        f"runner {h16(os.path.abspath(__file__))} · instrumento corre_mm {SHAS[os.path.join(MMD, 'corre_mm.py')]} · {PRERREGISTRO} · indices {m['ind']} · "
        f"npas {m['npas']} · T_pas {m['T_pas']} · T_pru {m['T_pru']} · T_EST {MM.T_EST} · pasajes {sem_pas(m, m['ind'][0], 0)}..{sem_pas(m, m['ind'][-1], m['npas'] - 1)} · "
        f"prueba {[sem_pru(m, i) for i in m['ind']]} · CFG10 {MM.CFG10} · {'REANUDA · ' if a.reanuda else ''}{carpeta}")
    if not verifica(log): log("  ALGO FALLA -> no se corre."); return 1
    if modo == 'serie':
        aok, atxt = arnes_pasado(); log(f"  arnes: {atxt}")
        if not aok: log("  el arnes no esta pasado con los shas actuales -> no se corre."); return 1
    tareas = [(b, i, carpeta, modo) for i in m['ind'] for b in m['brazos']]   # pareadas: los dos brazos del mismo indice juntos
    X = []

    def informa(x):
        X.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} i{x['i']} ({x['seg']}s) aborto {x['aborto']} · fraccion A {x.get('frac_A')} · "
                         f"cruzan {x.get('cruzan')}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): informa(x)
    else:
        for t in tareas: informa(trabajo(t))
    log(f"  {len(X)} trabajos · abortos {sum(1 for x in X if x['aborto'])} · {time.time()-t0:.1f}s")
    lee(carpeta, log, modo)
    return 0


if __name__ == '__main__':
    sys.exit(main())
