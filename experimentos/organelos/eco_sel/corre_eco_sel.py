"""corre_eco_sel.py — RUNNER y LETRA de ECO_SEL: F1 ARRANQUE EN FRIO + SELECCION NATURAL ENCIMA (frente 2; 28-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

Preregistro: PREREGISTRO_eco_sel.md (la letra esta AQUI, en veredicto(), y alli, §6).
La corrida es nucleo_eco_sel.trabajo (construido POR ANCLAS desde frio/corre_frio.py, sha 3ba8b0f5cf1fbbfa, por construye_eco_sel.py):
mismo mundo que F1 (ECO w90: esc 90, 90 fundadores, quimiostato, tope 3000), mismo carro de la familia (FAMB_RES0_ECO), frio en TODOS
los brazos (t_corte = 1: sin vivero, sin fundadores repuestos), T = 1e6, el gemelo motor_frio_rapido (arnes de F1 46/46) importado sin
tocar. Solo cambia la genetica:
  F1     MUT0          sin mutacion (== RES0_FRIO de F1 bit a bit; arnes (A))
  SEL_M  MARGEN        rep_umbral heredable con mutacion (p 0.05, sigma 0.15): el margen m = 1 - rep_umbral
  AZA_M  MARGEN_AZAR   el mismo gen SIN herencia (re-sorteo del banco: donante 'azar')
  SEL_C  CEREBRO       los 15 genes del cerebro heredables con mutacion (dote, rep_umbral, rep_X fijos)
  AZA_C  CEREBRO_AZAR  los mismos 15 genes SIN herencia
DOS PREGUNTAS, DOS VEREDICTOS (no se combinan): M (el margen, la sugerida por el director) y C (el cerebro).

Uso (ERR-115: banderas desconocidas o abreviadas abortan; --help no existe; SOLO el coordinador lanza --serie):
  python experimentos/organelos/eco_sel/corre_eco_sel.py --humo                                   # 1 proceso, 45395, 5 brazos, T 200 000
  python experimentos/organelos/eco_sel/corre_eco_sel.py --serie --desde 45301 --n 20 --pool 6    # serie
  python experimentos/organelos/eco_sel/corre_eco_sel.py --serie --desde 45321 --n 20 --pool 6    # replica
  python experimentos/organelos/eco_sel/corre_eco_sel.py --serie --desde 45301 --n 20 --pool 6 --reanuda
  python experimentos/organelos/eco_sel/corre_eco_sel.py --lee <carpeta de la serie>
"""
import argparse, glob, hashlib, json, os, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import nucleo_eco_sel as N      # inserta en sys.path juaco_eco y frio; CR.ME = motor Python hasta usa_gemelo()
CR = N.CR
RAIZ = N.RAIZ
MUNDO = N.MUNDO
BRAZOS = N.BRAZOS
DATOS = os.path.join(AQUI, 'datos')
# las dos preguntas: (brazo con herencia, brazo sin herencia, genes cuya firma se busca contra sombras)
# (C: los tres genes que la seleccion movio en ECO v1, brazo CEREBRO, 19101-19120: alpha + 19/20, aversion + 16/20, tau_e - 15/20)
PREG = {'M': ('SEL_M', 'AZA_M', ('rep_umbral',)),
        'C': ('SEL_C', 'AZA_C', ('alpha', 'aversion', 'tau_e'))}
UMB = dict(V1=17, V3_mut=18, P1_lo=3.5, P1_hi=6.5, P2_n=15, P2_d=1.5, P3_n=15)   # §6 del preregistro
BANDA = (0.60, 0.90)   # descriptivo: la banda de TERMO (consigna rep_umbral + 0.10 .. + 0.40) vista como rep_umbral = 1 - m


class BanderaMala(SystemExit):
    pass


def usa_gemelo():
    return N.usa_gemelo()


def trabajo(args):
    return N.trabajo(args)


def kbar(x, T):
    """Capacidad del linaje: media de los cuerpos vivos (tam_total, cada MUESTRA pasos) en [T/2, T]; tras la extincion cuenta 0."""
    tt = x.get('tam_total')
    if tt is None: return None
    m = MUNDO['muestra']; n = T // m + 1; i0 = (T // 2) // m
    v = (list(tt) + [0] * max(0, n - len(tt)))[i0:n]
    return float(np.mean(v))


def rango(x, g, t=None):
    """Rango (1..9; empates a medias) de la media del gen g en el BANCO real entre ella y sus 8 sombras, en la fila de gen_t de t = T_SEL
    (log(g/G0), columnas [6] y [7] de motor_eco._muestra_gen). Sin fila, sin banco o sin sombras: 5.0 (lo que espera la nula)."""
    t = N.T_SEL if t is None else t
    f = next((r for r in (x.get('gen_t') or []) if r[0] == t), None)
    if f is None or len(f) < 8 or f[6] is None or not f[7]: return 5.0
    j = x['genes'].index(g); r = f[6][j]; S = [s[j] for s in f[7]]
    return 1.0 + sum(1 for v in S if v < r) + 0.5 * sum(1 for v in S if v == r)


def _gen_T(x, g):
    gv = x.get('genes_vivos_T')
    return None if not gv or g not in gv else gv[g]


# ================================================================================ LA LETRA (PREREGISTRO_eco_sel.md §6)
def veredicto(R, n_esperado=20, T_esperado=None):
    T_esperado = N.FRIO['T'] if T_esperado is None else T_esperado
    L = []; by = {b: sorted([x for x in R if x['brazo'] == b], key=lambda x: x['seed']) for b in BRAZOS}
    n = {b: len(v) for b, v in by.items()}
    pers = {b: sum(int(x.get('persiste') or 0) for x in v) for b, v in by.items()}
    abortos = [(x['brazo'], x['seed'], x.get('aborto')) for x in R if x.get('aborto')]   # a 1e9 la guardia no puede disparar: todo aborto cuenta
    tc_mal = [(x['brazo'], x['seed']) for x in R if x.get('t_corte') != BRAZOS[x['brazo']][2]]
    sem = {b: tuple(x['seed'] for x in v) for b, v in by.items()}
    completo = (all(n[b] == n_esperado for b in BRAZOS) and all(x['T'] == T_esperado for x in R) and not abortos and not tc_mal
                and len({(x['brazo'], x['seed']) for x in R}) == len(R) and len(set(sem.values())) == 1)
    bloq = sum(int(x.get('bloqueados') or 0) for x in R)
    sucio = [(x['brazo'], x['seed'], x.get('n_refund'), x.get('fundadores_rep')) for x in R
             if x.get('n_refund') != 0 or x.get('fundadores_rep') != 0]
    K = {b: {x['seed']: kbar(x, T_esperado) for x in v} for b, v in by.items()}
    L.append(f"semillas por brazo: {n}; persiste en T = {T_esperado}: {pers}; abortos: {abortos[:5]}; t_corte distinto de 1: {tc_mal[:5]}; "
             f"bloqueados: {bloq}")
    medK = {b: (round(float(np.median([k for k in d.values() if k is not None])), 2) if d else None) for b, d in K.items()}
    L.append(f"CAPACIDAD K (media de cuerpos vivos en [T/2, T], extincion = 0), mediana sobre semillas: {medK}")
    # V3: la genetica es la declarada
    esperado = {b: (list(N.GENETICAS[BRAZOS[b][0]]['mutables'] or []) if N.GENETICAS[BRAZOS[b][0]]['p'] else []) for b in BRAZOS}
    v3 = {}
    for b, v in by.items():
        mal_mut = [x['seed'] for x in v if x.get('mutables') is not None and list(x['mutables']) != esperado[b]]
        fuera = [x['seed'] for x in v if (x.get('fuera_mutables') or 0) != 0]
        con_mut = sum(1 for x in v if (x.get('tasa_mut') or 0) > 0)
        ok = not mal_mut and not fuera and (con_mut == 0 if b == 'F1' else con_mut >= UMB['V3_mut'])
        v3[b] = (ok, mal_mut[:3], fuera[:3], con_mut)
    V1 = pers['F1'] >= UMB['V1']
    V2 = not sucio
    L.append(f"V1 ancla F1 persiste >= {UMB['V1']}/20: {'SE CUMPLE' if V1 else 'NO'} ({pers['F1']}) · V2 frio limpio (0 refundados, 0 fundadores "
             f"repuestos, los 5 brazos): {'SE CUMPLE' if V2 else 'NO'} {sucio[:5]}")
    L.append(f"V3 genetica declarada (mutables, 0 genes fuera de los mutables movidos, mutacion en >= {UMB['V3_mut']}/20; F1 sin mutacion): "
             f"{ {b: v3[b] for b in BRAZOS} }")
    if not completo: base = 'NO EVALUABLE (serie incompleta, abortos, T, t_corte o semillas distintas)'
    elif bloq > 0: base = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq})'
    elif not V2: base = 'NO EVALUABLE (un brazo tuvo fundadores repuestos: el frio no es frio)'
    elif not V1: base = 'NO EVALUABLE (el ancla F1 no reproduce F1: < 17/20)'
    else: base = None
    out = {}; D = dict(completo=completo, bloq=bloq, V1=V1, V2=V2, pers=pers, medK=medK, v3=v3, abortos=abortos, sucio=sucio)
    for q, (bs, ba, genes) in PREG.items():
        def rangos(b):   # rango medio (sobre las semillas) de cada gen de la pregunta contra sus 8 sombras en t = T_SEL
            return {g: (round(float(np.mean([rango(x, g) for x in by[b]])), 3) if by[b] else None) for g in genes}
        def cuenta(b):   # descriptivo: la prueba de ECO (fuera de sus 8 sombras) en T_SEL, (+, -) por gen
            c = {}
            for g in genes:
                pos = neg = 0
                for x in by[b]:
                    s = x.get('sel_100k')
                    if not s: continue
                    j = x['genes'].index(g)
                    pos += int(s[j] > 0); neg += int(s[j] < 0)
                c[g] = (pos, neg)
            return c
        rS, rA = rangos(bs), rangos(ba)
        sale = lambda r: r is not None and (r <= UMB['P1_lo'] or r >= UMB['P1_hi'])
        P1 = any(sale(r) for r in rS.values())
        G4 = not any(sale(r) for r in rA.values())
        cS, cA = cuenta(bs), cuenta(ba)
        mejor = [(g, r) for g, r in rS.items() if sale(r)]
        ss = sorted(set(K[bs]) & set(K['F1']) & set(K[ba]))
        dF = [K[bs][s] - K['F1'][s] for s in ss if K[bs][s] is not None and K['F1'][s] is not None]
        dA = [K[bs][s] - K[ba][s] for s in ss if K[bs][s] is not None and K[ba][s] is not None]
        nF = sum(1 for d in dF if d > 0); mF = (float(np.median(dF)) if dF else None)
        nA = sum(1 for d in dA if d > 0); mA = (float(np.median(dA)) if dA else None)
        P2 = nF >= UMB['P2_n'] and mF is not None and mF >= UMB['P2_d']
        P3 = nA >= UMB['P3_n']
        V3q = v3[bs][0] and v3[ba][0] and v3['F1'][0]
        L.append(f"[{q}] P1 firma del gen contra sus 8 sombras en t = {N.T_SEL}: rango medio (1..9, nula 5) <= {UMB['P1_lo']} o >= "
                 f"{UMB['P1_hi']} en algun gen de {list(genes)} en {bs}: {'SE CUMPLE' if P1 else 'NO'} ({rS}; salen {mejor}) · guardia: en {ba} "
                 f"ningun gen sale: {'SE CUMPLE' if G4 else 'NO'} ({rA}) · descriptivo, prueba de ECO (fuera de las 8 sombras, +/-): {bs} {cS} · {ba} {cA}")
        L.append(f"[{q}] P2 {bs} > F1 en K, pareado >= {UMB['P2_n']}/20 y mediana de la diferencia >= +{UMB['P2_d']}: {'SE CUMPLE' if P2 else 'NO'} "
                 f"({nF}/{len(dF)}, mediana {None if mF is None else round(mF, 2)}) · P3 {bs} > {ba} en K, pareado >= {UMB['P3_n']}/20 (el mismo gen "
                 f"sin herencia): {'SE CUMPLE' if P3 else 'NO'} ({nA}/{len(dA)}, mediana {None if mA is None else round(mA, 2)})")
        if base is not None: v = base
        elif not V3q: v = f'NO EVALUABLE (la genetica de {bs}/{ba} no es la declarada)'
        elif not G4: v = f'NO EVALUABLE (el control sin herencia {ba} sale de sus sombras: la prueba contra sombras no vale)'
        elif P1 and P2 and P3:
            v = (f'FUNCIONA: LA SELECCION MUEVE {"EL MARGEN" if q == "M" else "EL CEREBRO"} Y SUBE LA CAPACIDAD DEL LINAJE SOBRE F1; '
                 f'EL MISMO GEN SIN HERENCIA NO (en esta serie)')
        elif P2 and P3: v = 'HAY ALGO MODESTO: LA HERENCIA SUBE LA CAPACIDAD SOBRE F1, SIN FIRMA DEL GEN CONTRA SOMBRAS (en esta serie)'
        elif P1 and P3: v = 'HAY ALGO MODESTO: LA SELECCION MUEVE EL GEN Y GANA A SU CONTROL SIN HERENCIA, PERO NO SUPERA A F1 (en esta serie)'
        else: v = 'NO (en esta serie)'
        L.append(f"VEREDICTO {q} POR LA LETRA (una serie; el del bloque exige serie + replica con el mismo veredicto): {v}")
        out[q] = v
        D[q] = dict(P1=P1, G4=G4, P2=P2, P3=P3, V3=V3q, mejor=mejor, rS=rS, rA=rA, cS=cS, cA=cA, nF=nF, mF=mF, nA=nA, mA=mA, n_pares=len(dF))
    # ---- descriptivo (no decide)
    def med(b, f):
        v = [f(x) for x in by[b]]; v = [z for z in v if z is not None]
        return (round(float(np.median(v)), 4) if v else None)
    L.append("descriptivo, genes en los vivos en T (mediana sobre semillas de la media por semilla): "
             f"rep_umbral SEL_M {med('SEL_M', lambda x: _gen_T(x, 'rep_umbral'))} · AZA_M {med('AZA_M', lambda x: _gen_T(x, 'rep_umbral'))}; "
             f"alpha SEL_C {med('SEL_C', lambda x: _gen_T(x, 'alpha'))} · AZA_C {med('AZA_C', lambda x: _gen_T(x, 'alpha'))}; "
             f"aversion SEL_C {med('SEL_C', lambda x: _gen_T(x, 'aversion'))} · AZA_C {med('AZA_C', lambda x: _gen_T(x, 'aversion'))}")
    enb = {b: sum(1 for x in by[b] if _gen_T(x, 'rep_umbral') is not None and BANDA[0] <= _gen_T(x, 'rep_umbral') <= BANDA[1]) for b in ('SEL_M', 'AZA_M')}
    L.append(f"descriptivo, TERMO: semillas con la media de rep_umbral de los vivos en T dentro de {BANDA} (margen m = 1 - rep_umbral en "
             f"[0.10, 0.40]): {enb}")
    L.append("descriptivo, NACIDOS en la segunda mitad (mediana): nacimientos "
             f"{ {b: med(b, lambda x: x.get('nac_2a')) for b in BRAZOS} }; vida media de los muertos "
             f"{ {b: med(b, lambda x: x.get('vida_media_muertos_2a')) for b in BRAZOS} }; fraccion de muertes por veneno + sal "
             f"{ {b: med(b, lambda x: ((x['causas_2a'][2] + x['causas_2a'][3]) / max(1, sum(x['causas_2a']))) if x.get('causas_2a') else None) for b in BRAZOS} }; "
             f"R0 de nacidos { {b: med(b, lambda x: x.get('r0_nac')) for b in BRAZOS} } (en el quimiostato ~1 por construccion: no informa)")
    return out, L, D


def lee(carpeta, n_esperado=20):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    v, L, d = veredicto(R, n_esperado)
    for l in L: print(l, flush=True)
    return v, L, d, R


def SHAS():
    f = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    ECO = N.ECO; FR = N.FRIO_DIR
    ps = {'corre_eco_sel.py': os.path.join(AQUI, 'corre_eco_sel.py'), 'nucleo_eco_sel.py': os.path.join(AQUI, 'nucleo_eco_sel.py'),
          'construye_eco_sel.py': os.path.join(AQUI, 'construye_eco_sel.py'), 'PREREGISTRO_eco_sel.md': os.path.join(AQUI, 'PREREGISTRO_eco_sel.md'),
          'frio/corre_frio.py': os.path.join(FR, 'corre_frio.py'), 'frio/motor_frio_rapido.py': os.path.join(FR, 'motor_frio_rapido.py'),
          'juaco_eco/corre_eco_v12.py': os.path.join(ECO, 'corre_eco_v12.py'), 'juaco_eco/corre_eco.py': os.path.join(ECO, 'corre_eco.py'),
          'juaco_eco/motor_eco.py': os.path.join(ECO, 'motor_eco.py'), 'juaco_eco/carros/FAMB_RES0_ECO.py': os.path.join(ECO, 'carros', 'FAMB_RES0_ECO.py')}
    return {k: f(p) for k, p in ps.items() if os.path.exists(p)}


FIJOS = {'frio/corre_frio.py': '3ba8b0f5cf1fbbfa', 'frio/motor_frio_rapido.py': 'ff9d890a5cce9dec',
         'juaco_eco/corre_eco_v12.py': '1340d268e1fd93d8', 'juaco_eco/corre_eco.py': '47d9cee4d6462116',
         'juaco_eco/motor_eco.py': 'bca3033878b59622', 'juaco_eco/carros/FAMB_RES0_ECO.py': '94ea78589bc2ce24'}


def verifica():
    """Antes de correr: el nucleo en disco == el construido por anclas y los origenes con su sha (si no, no se corre nada)."""
    import construye_eco_sel as CE
    sh = SHAS()
    mal = {k: (sh.get(k), v) for k, v in FIJOS.items() if sh.get(k) != v}
    if mal: raise SystemExit(f"ECO_SEL: origenes con otro sha {mal}")
    if not CE.main(['--verifica']): raise SystemExit('ECO_SEL: nucleo_eco_sel.py no es el construido por anclas')
    return sh


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--lee', default=None)
    ap.add_argument('--desde', type=int); ap.add_argument('--n', type=int); ap.add_argument('--pool', type=int)
    ap.add_argument('--reanuda', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('ECO_SEL: banderas mal formadas')
    if resto: raise BanderaMala(f"ECO_SEL: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('ECO_SEL: sin la forma --bandera=valor')
    if len(argv) != len(set(x for x in argv if x.startswith('--'))) + sum(1 for x in argv if not x.startswith('--')):
        raise BanderaMala('ECO_SEL: bandera repetida')
    modos = int(a.humo) + int(a.serie) + int(a.lee is not None)
    if modos != 1: raise BanderaMala('ECO_SEL: exactamente uno de --humo, --serie, --lee')
    if a.humo and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda): raise BanderaMala('ECO_SEL: --humo va solo')
    if a.lee is not None and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda):
        raise BanderaMala('ECO_SEL: --lee va solo')
    if a.serie and (a.desde not in N.VENTANAS or a.n != 20 or a.pool is None or not 1 <= a.pool <= 6):
        raise BanderaMala(f"ECO_SEL: --serie --desde {N.VENTANAS[0]} (serie) o {N.VENTANAS[1]} (replica) --n 20 --pool 1..6")
    return a


def humo():
    """UN proceso, sin Pool: semilla de practica 45395, los 5 brazos, T 200 000 (regla 3: <= 6 corridas, <= 200 000 pasos). Escribe su JSON."""
    sh = verifica()
    usa_gemelo()
    os.makedirs(os.path.join(DATOS, 'humo'), exist_ok=True)
    ts = time.strftime('%Y%m%d_%H%M%S'); etq = f"eco_sel_humo_s{N.HUMO['semilla']}_T{N.HUMO['T']}_{ts}"
    carpeta = os.path.join(DATOS, 'humo', etq); os.makedirs(carpeta, exist_ok=True); t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] HUMO ECO_SEL (gemelo motor_frio_rapido, 1 proceso) · shas {sh}", flush=True)
    R = []
    for b, (gen, carro, tc) in BRAZOS.items():
        r = trabajo((N.HUMO['semilla'], b, N.HUMO['T'], tc, N.FRIO['T_lect'], carpeta, False))
        R.append(r)
        print(f"[{time.strftime('%H:%M:%S')}] {b} ({gen}) s{r['seed']}: {r['seg']} s · persiste {r['persiste']} (vivos {r.get('vivos_T')}) · "
              f"K [T/2, T] {None if r.get('tam_total') is None else round(kbar(r, N.HUMO['T']), 2)} · n_nac {r.get('n_nac')} · "
              f"refundados {r.get('n_refund')} · fundadores_rep {r.get('fundadores_rep')} · tasa_mut {r.get('tasa_mut')} · mutables {r.get('mutables')} · "
              f"fuera {r.get('fuera_mutables')} · movidos {r.get('movidos_mutables')} · genes vivos T {r.get('genes_vivos_T')} · "
              f"sel_100k {r.get('sel_100k')} · vida 2a {r.get('vida_media_muertos_2a')} · causas 2a {r.get('causas_2a')} · r0_nac {r.get('r0_nac')} · "
              f"aborto {r.get('aborto')}", flush=True)
    v, L, d = veredicto(R, n_esperado=20, T_esperado=N.HUMO['T'])
    for l in L: print('  ' + l, flush=True)
    ruta = os.path.join(DATOS, 'humo', etq + '.json')
    json.dump(dict(humo=N.HUMO, FRIO=N.FRIO, BRAZOS=BRAZOS, GENETICAS={k: dict(v_, mutables=list(v_['mutables'] or [])) for k, v_ in N.GENETICAS.items()},
                   R=R, veredicto_de_prueba=v, lineas=L, seg=round(time.time() - t0, 1), seg_por_brazo={x['brazo']: x['seg'] for x in R}, shas=sh),
              open(ruta, 'w', encoding='utf-8'), default=str)
    print(f"  JSON: {os.path.relpath(ruta, RAIZ)}  ({round(time.time() - t0, 1)} s)")
    print(f"VEREDICTO (humo, una semilla, T corto: no decide): {v}")
    return ruta


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.humo: return humo()
    if a.lee is not None:
        lee(a.lee); return
    sh = verifica()
    usa_gemelo()
    T, tl = N.FRIO['T'], N.FRIO['T_lect']
    etq = f"eco_sel_serie_s{a.desde}-{a.desde + a.n - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"ECO_SEL: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ECO_SEL {etq} · T {T} · brazos {BRAZOS} · pool {a.pool} · motor GEMELO motor_frio_rapido · shas {sh}")
    orden = ('SEL_C', 'SEL_M', 'F1', 'AZA_M', 'AZA_C')   # los caros primero
    jobs = [(s, b, T, BRAZOS[b][2], tl, carpeta, a.reanuda) for b in orden for s in range(a.desde, a.desde + a.n)]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool, initializer=usa_gemelo) as pool:
        for k, r in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] {r['brazo']} s{r['seed']}: persiste {r['persiste']} (vivos {r.get('vivos_T')}) · K "
                f"{None if r.get('tam_total') is None else round(kbar(r, T), 2)} · t_ext {r.get('t_ext')} · refundados {r.get('n_refund')} · "
                f"n_nac {r.get('n_nac')} · genes vivos T {r.get('genes_vivos_T') if r['brazo'] in ('SEL_M', 'AZA_M') else '-'} · aborto {r.get('aborto')} "
                f"({r['seg']} s; {round(time.time() - t0)} s)")
    v, L, d, R = lee(carpeta, a.n)
    for l in L: flog.write(l + '\n')
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d=d, seg=round(time.time() - t0), MUNDO=MUNDO, SERIE=N.SERIE, FRIO=N.FRIO,
                   BRAZOS=BRAZOS, UMB=UMB, shas=sh), open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    log(f"VEREDICTOS: {v}")
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
