"""juez.py — EL JUEZ DE LA CARRERA DE ESCUDERIAS (REGLAMENTO sec. 7). Fijo: se commitea antes de la ronda 0.

MISION: llegar a la AGI por este camino. Corre una RONDA (lista de carros, semillas, T) en pista.py y
calcula por linaje, con la definicion de H-1 (corre_f9.py:193-207):
  R0 = descendientes / (muertes + 1) · vida mediana (vidas_h1, la ultima truncada en T, como corre_f9)
  muertes · descendientes · fundadores · causas de muerte (hambre / sed / veneno / sal; veneno = murio por
  energia habiendo mordido B en sus ultimos W_CAUSA=400 pasos; sal = idem por agua con D) · p1/c1 (F9)
  · ERR-99 (ENMIENDA 2): evaluable (>= 5 muertes) / casi inmortal, R0 evaluable, t_fund, fundadores tras t = 10000,
  nacimientos reales, cruza (R0 >= 0.90 y 0 fundadores tras t = 10000); por escuderia: cruzan, evaluables, casi inmortales,
  semillas que cruza y "gana" (>= 15/20); monocultivo y SOLO con el criterio de la ENMIENDA 3; predicciones firmadas al lado.
    python .../juez.py --ronda 1 | 1mono | 1solo   (atajos; o --carros O1,S1,H1,FABRICA*6)   ·   --recalcula <crudo viejo>
  ENMIENDA 4: --mundo_N M (N carros en el mundo de M) · --ronda sellada_mono | sellada_sologrande | sellada_sinlimpia | sellada_fab
  (semillas 5001-5020 por defecto) · mecanismo: limpiezas por cuerpo, buenos que reaparecen por ellas, pasos sin ningun bueno.
  ERR-100: al lado del R0 preregistrado, el R0 de NACIMIENTOS REALES = nac_reales / (muertes + 1), su mediana sobre evaluables y
  'cruza_real' (SOLO se reporta; el criterio no cambia). ERR-101: --ronda sellada_fundborra (9 CTRL_O1_FUNDBORRA, 5021-5040).
  ENMIENDA 5 (ronda 2): --ronda r2mono --equipo X | r2mix3 | r2fab --equipo X | r2o1mono; fundador limpio; 9101-9120 (replica --desde 9121);
  cruza = R0 de NACIMIENTOS REALES >= 0.90 y 0 fundadores tras t=10000; gana = cruza en >= 15/20 semillas. Humos: humo_equipo.py.
  ENMIENDA 6 / ERR-102 (co-principal): PERSISTENCIA (0 fundadores tras t=10000 y >= 5 nacimientos reales; estabiliza > 1/2 de los
  linajes por semilla, >= 15/20 semillas) y MUERTES VOLUNTARIAS fisicas por equipo (lo que declara el carro solo se muestra).
  · exposiciones a A y C · escrituras por linaje (hasta 3000 en la telemetria). La pizarra COMPLETA se guarda
  aparte en <prefijo>_pizarra.jsonl.gz (una linea [semilla, t, id, contenido] por escritura publicada).
Y de la pista: R0_pista = sum(descendientes) / (sum(muertes) + n_linajes) · composicion del mundo por cuarto de T.
ERR-96: TODO sale de las claves FISICAS de primer nivel que escribe pista.py (resumen_linaje); lo que devuelve
el carro (d['carro']) no se lee; la contabilidad fisica tiene que cerrar (coherente). Test: test_tramposo.py.
ENMIENDA 1: --escala 1 por defecto (L = 40N, nobj = 4N; con N = 1 es la pista original).

Antes de correr, el juez comprueba (0) el CHEQUEO ESTATICO de cada carro (revisa_carro.py; si uno falla, NO
corre), (1) el sha de organismo_f9c.py y (2) la IDENTIDAD CORTA: FABRICA solo, compat=1, pizarra 0 ==
organismo_f9c REL bit a bit (s=1, T=5000). Si falla, NO corre (el arnes completo es identidad_pista.py).
Registra el sha de cada carro: la ronda queda atada a esas versiones.

    python experimentos/carrera_escuderias/juez.py --humo                          (UN proceso: ronda 0, 9 FABRICA, 4001-4002)
    python experimentos/carrera_escuderias/juez.py --ronda 1 --carros O1,O2,...,H3 --desde 4001 --n 20 --pool 6   (SOLO el coordinador)

POOL (ERR-86): --pool o JUACO_POOL; 0 = un proceso. Los agentes no corren Pool (regla 3).
ERR-54: el crudo se escribe ANTES de resumir. VOCABULARIO: "linaje", "cuerpo", "R0 del linaje"; no
"poblacion", "generacion", "evoluciona", "coopera" (REGLAMENTO sec. 6).
"""
import argparse, gzip, json, os, platform, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
import pista as P
import revisa_carro as RC

DATOS = os.path.join(AQUI, 'datos')
REF_REL = dict(R0=0.395, R0_acum1=0.483, fuente='bloque 2, replica 1601-1620, un cuerpo a la vez (REGLAMENTO sec. 1)')
PRED_RONDA0 = {0: (0.15, 0.35),   # prediccion firmada del organizador, pista SIN escalar (REGLAMENTO sec. 1)
               1: (0.35, 0.55)}   # ENMIENDA 1: pista escalada L=40N, nobj=4N (firmada por el coordinador)
T_DEF = 100000
# ---- ENMIENDA 2 (ERR-99) y ENMIENDA 3 (REGLAMENTO), letra fijada ANTES de la ronda 1
MIN_NAC_PERSISTE = 5     # ENMIENDA 6: persiste = 0 fundadores tras T_CORTE y >= 5 nacimientos reales (hay recambio)
MIN_MUERTES = 5          # R0 evaluable solo con >= 5 muertes; si no, "casi inmortal" (no cuenta ni a favor ni en contra)
R0_CRUCE = 0.90          # cruza: R0 evaluable >= 0.90 Y 0 fundadores despues de T_CORTE
T_CORTE = 10000
GANA_FRAC = 0.75         # gana la ronda: cruza en >= 15/20 semillas
MONO_FRAC_SIN_FUND = 0.75  # monocultivo (ii): >= 75 % de los evaluables sin fundadores tras T_CORTE
MONO_FRAC_EVAL = 120 / 180  # monocultivo (iii): >= 120 de 180 linajes-semilla evaluables
# ---- alineaciones por linea de comandos (--ronda); --carros explicito manda sobre el atajo
ALINEACIONES = {'0': ['FABRICA'] * 9, '1': ['O1', 'S1', 'H1'] + ['FABRICA'] * 6, '1mono': ['O1'] * 9, '1solo': ['O1'],
                # ENMIENDA 4: serie SELLADA (semillas 5001-5020 por defecto), todas con el criterio de la ENMIENDA 3
                'sellada_mono': ['O1'] * 9, 'sellada_sologrande': ['O1'], 'sellada_sinlimpia': ['CTRL_O1_SINLIMPIA'] * 9,
                'sellada_fab': ['FABRICA'] * 9, 'sellada_fundborra': ['CTRL_O1_FUNDBORRA'] * 9}
MUNDO_ATAJO = {'sellada_sologrande': 9}   # MUNDO FORZADO: 1 O1 en el mundo dimensionado para 9 (L=360, 36 objetos, olvido x9)
DESDE_SELLADA = 5001
PRED_ENM4 = {'sellada_mono': [("S-MONO cruza (p 0.75)", lambda cm: cm['cruza'])],
             'sellada_sologrande': [("S-SOLO-GRANDE cruza o queda casi inmortal (p 0.60)", lambda cm: cm['cruza'] or cm['casi_inmortal_grupo'])],
             'sellada_sinlimpia': [("S-SIN-LIMPIEZA NO cruza (p 0.50)", lambda cm: not cm['cruza'])],
             'sellada_fab': [("S-FAB NO cruza (p 0.97)", lambda cm: not cm['cruza'])],
             # AUDITORIA DE LA SERIE SELLADA (ERR-101): S-FUNDBORRA, semillas selladas NUEVAS 5021-5040
             'sellada_fundborra': [("S-FUNDBORRA cruza por la letra (ENMIENDA 3) (p 0.55)", lambda cm: cm['cruza']),
                                   ("S-FUNDBORRA: mediana del R0 de NACIMIENTOS REALES sobre evaluables >= 0.90 (p 0.35)",
                                    lambda cm: cm['mediana_R0_real_eval'] is not None and cm['mediana_R0_real_eval'] >= R0_CRUCE)]}
DESDE_ATAJO = {'sellada_fundborra': 5021}
# ---- ENMIENDA 5 (RONDA 2): fundador limpio impuesto por la pista; decide el R0 de NACIMIENTOS REALES
EQUIPOS_R2 = ('O2', 'O3', 'O4')
DESDE_R2 = 9101           # serie oficial 9101-9120; replica sellada con --desde 9121
def alineacion_r2(ronda, equipo):
    """Atajos de la ronda 2 (todos con --fundador_limpio). Devuelve la lista de carros o aborta con un error claro."""
    if ronda in ('r2mono', 'r2fab') and not equipo:
        raise SystemExit(f"JUEZ: --ronda {ronda} exige --equipo X (O2, O3, O4 u O1)")
    al = {'r2mono': [equipo] * 9, 'r2mix3': ['O2'] * 3 + ['O3'] * 3 + ['O4'] * 3,
          'r2fab': [equipo] * 3 + ['FABRICA'] * 6, 'r2o1mono': ['O1'] * 9}[ronda]
    falta = sorted({c for c in al if not os.path.exists(os.path.join(P.CARROS, c + '.py'))})
    if falta:
        raise SystemExit(f"JUEZ: la ronda {ronda} necesita {', '.join('carros/' + c + '.py' for c in falta)} y NO EXISTE "
                         f"(el equipo todavia no entrego su carro). No se corre nada.")
    return al
PRED_R2 = ["al menos un equipo gana la ronda 2 en monocultivo (p 0.50)",
           "en pista mixta con 6 FABRICA gana alguno (p 0.25)",
           "O1 con fundador limpio cruza en monocultivo con R0 real (p 0.60)"]
R2_SEMILLA = 'mayoria'   # un equipo cruza EN UNA SEMILLA si MAS DE LA MITAD de sus linajes en esa semilla cruzan (ver resumen_r2)
PRED_ENM = {   # predicciones FIRMADAS del coordinador (ENMIENDAS 2 y 3), se imprimen al lado de lo medido
    'oficial': ["H1: R0 mediano dentro de +-0.10 de la mediana de los FABRICA", "FABRICA: R0 mediano 0.28-0.45",
                "O1: cruza en >= 10/20 semillas (p 0.55); gana la ronda >= 15/20 (p 0.30)",
                "al menos un linaje O1-semilla 'casi inmortal' (p 0.80); O1 'casi inmortal' en >= 10/20 (p 0.75)",
                "S1 no cruza (p 0.95)"],
    'mono': ["monocultivo O1 CRUZA (p 0.55)"],
    'solo': ["SOLO O1 NO cruza: mediana < 0.90 (p 0.90)"],
}


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 3) if xs else None


def frac(xs):
    ys = [x for x in xs if x >= 0]
    return round(sum(ys) / len(ys), 4) if ys else None


def identidad_corta():
    sys.path[:0] = [os.path.join(RAIZ, 'experimentos', d) for d in
                    ('nivel09_cuerpo_nuevo_b2', 'nivel09_cuerpo_nuevo', 'nivel13_alma', 'nivel11_mundo_vivo')] + [os.path.join(RAIZ, 'organismo')]
    _a = sys.argv; sys.argv = [sys.argv[0]]
    import corre_bloque2 as CB, organismo_f9c as F9C
    sys.argv = _a
    N = lambda x: json.loads(json.dumps(x, default=str))
    sha = P.h16(P.ORIGEN)
    a = F9C.run(1, T=5000, **CB.BRAZOS['REL'])
    b = P.plano(P.run(1, ['FABRICA'], T=5000, pizarra=0, compat=1)['linajes'][0])
    dif = [k for k in a if k not in b or N(a[k]) != N(b[k])] + [k for k in b if k not in a]
    return dict(sha_f9c=sha, sha_ok=(sha == P.SHA_F9C), dif=dif, ok=(sha == P.SHA_F9C and not dif))


FISICAS = ('descendientes', 'deaths', 'vidas_h1', 'fundadores', 'muertes_nec', 'exposiciones', 'mord', 'pasos_viables',
           'T_efectivo', 'cola_final', 'desc_por_vida', 'nacimientos', 'origen_cuerpo', 'xor_mord', 'xor_enc', 't_fund',
           'cola_desborde', '_carrera')


def resumen_linaje(d, seed):
    """ERR-96: SOLO la verdad FISICA de la pista (claves de primer nivel escritas por pista.py). d['carro'] (lo
    que devuelve el carro) NO se lee. Ademas la contabilidad fisica tiene que cerrar (coherente)."""
    f = {k: d[k] for k in FISICAS}
    c = f['_carrera']; p1 = c['p1']; c1 = c['c1']; mu = f['deaths']; v = f['vidas_h1']
    coh = (f['nacimientos'] == mu and len(v) == mu + 1 and len(f['desc_por_vida']) == mu + 1
           and sum(v) == f['T_efectivo'] and sum(f['desc_por_vida']) == f['descendientes']
           and len(f['origen_cuerpo']) == mu + 1 and f['fundadores'] + 1 == sum(1 for g in f['origen_cuerpo'] if not g)
           and sum(c['causas'].values()) == mu)
    return dict(id=c['id'], indice=c['indice'], seed=seed, descendientes=f['descendientes'], muertes=mu,
                R0=round(f['descendientes'] / (mu + 1), 4), r=f['descendientes'] - mu,
                vida_med=med(v), cuerpos=len(v), fundadores=f['fundadores'], coherente=bool(coh),
                causas=c['causas'], muertes_nec=f['muertes_nec'], p1=frac(p1), c1=frac(c1),
                exp_A=f['exposiciones']['A'], exp_C=f['exposiciones']['C'],
                mord={k: sum(x) for k, x in f['mord'].items()}, pasos_viables=f['pasos_viables'],
                sac_frac=round(f['pasos_viables'] / f['T_efectivo'], 4), cola_final=f['cola_final'],
                escrituras=c['escrituras'], vetos=c['vetos'], diag=c.get('diag'), xor_mord=f['xor_mord'], xor_enc=f['xor_enc'],
                muertes_vol=c.get('muertes_vol'),   # ENMIENDA 6: FISICA (la que cuenta); None en crudos anteriores
                carro_declara=({k: d['carro'][k] for k in ('cuerpos_term', 'senescentes') if isinstance(d.get('carro'), dict) and k in d['carro']}
                               or None),   # SOLO SE MUESTRA (ERR-96: no puntua); con fundador limpio es solo la ULTIMA instancia
                telem=dict(vidas=v, desc_por_vida=f['desc_por_vida'], causa_cuerpo=c['causa_cuerpo'], escr=c['escr'],
                           t_fund=f['t_fund'], origen=f['origen_cuerpo']),
                **err99(mu, f['fundadores'], f['t_fund'], f['descendientes'], f['T_efectivo'], v, f['desc_por_vida'],
                        nac_reales=sum(f['origen_cuerpo']), cola_final=f['cola_final']))


def t_fund_reconstruido(vidas, dpv, cola_max=200):
    """Reconstruye EXACTAMENTE los instantes de fundacion (y la cola final) desde la telemetria por cuerpo: el cuerpo i
    muere en sum(vidas[:i+1]); sus hijos entran a la cola antes de su muerte; al morir nace el primero de la cola, o un
    FUNDADOR si esta vacia. Sirve para recalcular crudos viejos sin t_fund; en los nuevos se VERIFICA contra t_fund."""
    q = 0; t = 0; tf = []; nr = 0
    for i in range(len(vidas) - 1):
        q = min(q + dpv[i], cola_max); t += vidas[i]
        if q > 0: q -= 1; nr += 1
        else: tf.append(t)
    return tf, min(q + dpv[-1], cola_max), nr


def err99(mu, fund, tf, desc, T, vidas, dpv, nac_reales, cola_final, t_fund_fuente='fisica'):
    """ENMIENDA 2 / ERR-99 por linaje-semilla (SOLO fisica). Si t_fund se trunco (tope 200 de la pista) y el ultimo
    registrado es <= T_CORTE, los que faltan se cuentan como POSTERIORES (conservador contra el cruce) y se marca."""
    pre = sum(1 for x in tf if x <= T_CORTE); post = fund - pre
    incierto = len(tf) < fund and (not tf or tf[-1] <= T_CORTE)
    ev = mu >= MIN_MUERTES
    R0 = round(desc / (mu + 1), 4)
    muertos = dpv[:-1]
    R0r = round(nac_reales / (mu + 1), 4)   # ERR-100: R0 de NACIMIENTOS REALES (sin los hijos que esperan en la cola)
    persiste = bool(post == 0 and nac_reales >= MIN_NAC_PERSISTE)   # ENMIENDA 6: PERSISTENCIA (sin exigir >= 5 muertes)
    return dict(evaluable=ev, casi_inmortal=not ev, R0_eval=(R0 if ev else None), fund_post10k=post, persiste=persiste,
                R0_real=R0r, R0_real_eval=(R0r if ev else None), cruza_real=bool(ev and R0r >= R0_CRUCE and post == 0),
                fund_post_incierto=bool(incierto), cruza=bool(ev and R0 >= R0_CRUCE and post == 0),
                nac_reales=nac_reales, t_fund_fuente=t_fund_fuente,   # cola_final ya esta en el resumen (no se duplica)
                fund_por_1e5=round(fund / T * 1e5, 2),
                frac_muere_sin_parir=(round(sum(1 for x in muertos if x == 0) / len(muertos), 4) if muertos else None),
                t_fund_n=len(tf))


def tarea(args):
    seed, carros, T, pizarra, rep_acum, escala = args[:6]; mundo_n = args[6] if len(args) > 6 else None
    fl = args[7] if len(args) > 7 else 0
    t0 = time.time()
    r = P.run(seed, carros, T=T, pizarra=pizarra, rep_acum=rep_acum, escala=escala, mundo_n=mundo_n, fundador_limpio=fl)
    L = [resumen_linaje(d, seed) for d in r['linajes']]
    sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
    for x in L:   # la reconstruccion de t_fund (para crudos viejos) se VERIFICA contra la fisica en cada corrida nueva
        tf, qf, nr = t_fund_reconstruido(x['telem']['vidas'], x['telem']['desc_por_vida'])
        x['t_fund_rec_ok'] = bool(tf[:200] == x['telem']['t_fund'] and qf == x['cola_final'] and nr == x['nac_reales'])
    return dict(seed=seed, seg=round(time.time() - t0, 1), linajes=L, pista=r['pista'],
                R0_pista=round(sd / (sm + len(L)), 4), pizarra_log=r['pizarra_log'])


def agrega(R):
    ids = R[0]['pista']['ids']
    tab = []
    for i, ident in enumerate(ids):
        xs = [c['linajes'][i] for c in R]
        cz = {k: sum(x['causas'][k] for x in xs) for k in ('hambre', 'sed', 'veneno', 'sal')}
        tab.append(dict(id=ident, R0_med=med([x['R0'] for x in xs]), R0=[x['R0'] for x in xs],
                        vida_med=med([x['vida_med'] for x in xs]), muertes=med([x['muertes'] for x in xs]),
                        descendientes=med([x['descendientes'] for x in xs]), fundadores=med([x['fundadores'] for x in xs]),
                        p1=med([x['p1'] for x in xs]), c1=med([x['c1'] for x in xs]), exp_A=med([x['exp_A'] for x in xs]),
                        sac_frac=med([x['sac_frac'] for x in xs]), causas=cz,
                        cruza_09=sum(1 for x in xs if x['R0'] >= 0.9), n=len(xs)))
    return tab, med([c['R0_pista'] for c in R])


def informe(R, meta, log):
    tab, r0p = agrega(R)
    log(f"\nRESUMEN · {meta['etiqueta']} · semillas {meta['semillas']} · T={meta['T']} · pizarra {meta['pizarra']} · rep_acum {meta['rep_acum']}")
    log(f"  {'linaje':12s} {'R0 med':>7} {'R0 por semilla':>22} {'vida':>7} {'muert':>6} {'desc':>5} {'fund':>5} "
        f"{'p1':>5} {'c1':>5} {'expA':>6} {'sac':>6}  causas (hambre/sed/veneno/sal)  >=0.9")
    for x in tab:
        cz = x['causas']; tot = max(1, sum(cz.values()))
        log(f"  {x['id']:12s} {str(x['R0_med']):>7} {str(x['R0']):>22} {str(x['vida_med']):>7} {str(x['muertes']):>6} "
            f"{str(x['descendientes']):>5} {str(x['fundadores']):>5} {str(x['p1']):>5} {str(x['c1']):>5} {str(x['exp_A']):>6} "
            f"{str(x['sac_frac']):>6}  {cz['hambre']}/{cz['sed']}/{cz['veneno']}/{cz['sal']} "
            f"({cz['hambre']/tot:.0%}/{cz['sed']/tot:.0%}/{cz['veneno']/tot:.0%}/{cz['sal']/tot:.0%})  {x['cruza_09']}/{x['n']}")
    log(f"  R0 de la pista (mediana por semilla de sum desc / (sum muertes + n)): {r0p} · por semilla {[c['R0_pista'] for c in R]}")
    for c in R:
        fq = [round((q['B'] + q['D']) / max(1e-9, sum(q.values())), 3) for q in c['pista']['comp_mundo_q']]
        log(f"  semilla {c['seed']}: fraccion B+D del mundo por cuarto de T {fq} · L {c['pista']['L']} nobj {c['pista']['nobj']}")
    dg = [l['diag'] for c in R for l in c['linajes'] if l.get('diag')]
    if dg:
        def md(k): return med([x[k] for x in dg])
        log(f"  DIAGNOSTICO (mediana sobre {len(dg)} linajes-semilla; ventana {dg[0]['W']} pasos tras perder el objetivo bueno):")
        log(f"    robos por linaje {md('robos')} · perdidas por olvido {md('perdidas_olvido')} · "
            f"B/D tras robo {md('bd_tras_robo')} vs tras olvido {md('bd_tras_olvido')} vs base {md('bd_base')} · "
            f"A/C tras robo {md('ac_tras_robo')} vs base {md('ac_base')}")
        log(f"    distancia media al bueno mas cercano {md('dist_bueno_media')} · frac pasos sin bueno en el mundo {md('frac_sin_bueno')} · "
            f"frac pasos sin NINGUN objeto a <= 20 {md('frac_sin_obj20')} (max {max(x['frac_sin_obj20'] for x in dg)})")
    if dg and 'limpiezas' in dg[0]:
        fsm = [c['pista'].get('frac_sin_bueno_mundo') for c in R]
        sl = sum(x['limpiezas'] for x in dg); sb = sum(x['buenos_por_limpieza'] for x in dg)
        sm_ = sum(x['mordidas_malas'] for x in dg); smb = sum(x['buenos_por_mala'] for x in dg)
        log(f"  MECANISMO (ENMIENDA 4; desde la fisica: 'limpieza' = mordida de B/D A SABIENDAS -letra ya mordida por el linaje- con el golpe "
            f"en la necesidad MAS llena):")
        log(f"    limpiezas por linaje-semilla (mediana) {md('limpiezas')} · por cuerpo {md('limpiezas_por_cuerpo')} · total {sl} · "
            f"objetos buenos que reaparecen por ellas {sb} ({round(sb / sl, 3) if sl else None} por limpieza)")
        log(f"    todas las mordidas malas {sm_} -> buenos que reaparecen {smb} · fraccion de pasos SIN ningun objeto bueno en el mundo "
            f"por semilla {fsm} (mediana {med(fsm)})")
    if dg and 'boca' in dg[0]:
        tot = {}
        for x in dg:
            for k, v in x['boca'].items():
                t_ = tot.setdefault(k, [0, 0, 0.0, 0.0]); t_[0] += v['dec']; t_[1] += v['mord']
                t_[2] += (v['def_dec'] or 0) * v['dec']; t_[3] += (v['def_mord'] or 0) * v['mord']
        log("  HAMBRE -> BOCA (suma de todos los linajes-semilla; H = manda el hambre, S = manda la sed; deficit = el de la necesidad activa):")
        for k in ('AH', 'AS', 'BH', 'BS', 'CH', 'CS', 'DH', 'DS'):
            if k in tot:
                d_, m_, sd, sm = tot[k]
                log(f"    {k}: decisiones {d_:6d} mordidas {m_:6d} tasa {m_/d_ if d_ else 0:.3f} · deficit medio al decidir {sd/d_ if d_ else 0:.3f} "
                    f"al morder {sm/m_ if m_ else 0:.3f}")
        hb = [sum(x['hist_def_bd'][i] for x in dg) for i in range(10)]; ha = [sum(x['hist_def_ac'][i] for x in dg) for i in range(10)]
        mb = sum((i + .5) / 10 * h for i, h in enumerate(hb)) / max(1, sum(hb)); ma = sum((i + .5) / 10 * h for i, h in enumerate(ha)) / max(1, sum(ha))
        log(f"    deficit en mordidas B/D (bins de 0.1) {hb} (media ~{mb:.3f}) · en mordidas A/C {ha} (media ~{ma:.3f})")
        log(f"    mordidas B/D con un robo en los {dg[0]['W']} pasos previos {md('bd_con_robo_prev')} vs pasos cubiertos asi {md('pasos_con_robo_prev')} · "
            f"deficit en B/D con robo previo {md('def_bd_con_robo')} vs sin {md('def_bd_sin_robo')}")
        xm = [[sum(l['xor_mord'][n][j] for c in R for l in c['linajes']) for j in range(4)] for n in range(2)]
        xe = [[sum(l['xor_enc'][n][j] for c in R for l in c['linajes']) for j in range(4)] for n in range(2)]
        log(f"    formato H-BOCA (mordidas / exposiciones): veneno con SED {xm[1][1]}/{xe[1][1]} · veneno con HAMBRE {xm[0][1]}/{xe[0][1]} · "
            f"sal con HAMBRE {xm[0][3]}/{xe[0][3]} · sal con SED {xm[1][3]}/{xe[1][3]}")
    log(f"  contabilidad fisica coherente: {sum(l['coherente'] for c in R for l in c['linajes'])}/{sum(len(c['linajes']) for c in R)} · "
        f"t_fund reconstruible desde telem == fisica: {sum(l.get('t_fund_rec_ok', False) for c in R for l in c['linajes'])}/{sum(len(c['linajes']) for c in R)}")
    log(f"  mundo: objetos medios por tipo (A comida, B veneno, C agua, D sal; nobj={R[0]['pista']['nobj']}) por semilla "
        f"{[c['pista']['comp_mundo'] for c in R]} · olvidos {[c['pista']['olvidos'] for c in R]}")
    ms = [{k: sum(l['mord'][k] for l in c['linajes']) for k in 'ABCD'} for c in R]
    log(f"  mordidas totales por tipo por semilla {ms}")
    log(f"  referencia UN cuerpo a la vez: REL {REF_REL['R0']} (acum 1: {REF_REL['R0_acum1']}) -- {REF_REL['fuente']}")
    return tab, r0p


def etiqueta_de(ident):
    return ident.split('#')[0]


def modo_de(ids):
    et = [etiqueta_de(c) for c in ids]
    if len(et) == 1: return 'solo'
    if len(set(et)) == 1 and len(et) == 9 and et[0] != 'FABRICA': return 'mono'
    if sorted(set(et)) == ['FABRICA', 'H1', 'O1', 'S1']: return 'oficial'
    return 'otro'


def criterio_mono(xs):
    """ENMIENDA 3: (i) mediana del R0 sobre evaluables >= 0.90; (ii) >= 75 % de evaluables sin fundadores tras t=10000;
    (iii) >= 120/180 (= 2/3) de los linajes-semilla evaluables. Se aplica igual al SOLO (con sus n linajes-semilla)."""
    ev = [x for x in xs if x['evaluable']]
    m = med([x['R0_eval'] for x in ev])
    fs = (sum(1 for x in ev if x['fund_post10k'] == 0) / len(ev)) if ev else 0.0
    fe = len(ev) / len(xs) if xs else 0.0
    c = dict(i=bool(m is not None and m >= R0_CRUCE), ii=bool(fs >= MONO_FRAC_SIN_FUND), iii=bool(fe >= MONO_FRAC_EVAL - 1e-12))
    mr = med([x['R0_real_eval'] for x in ev])
    cr = dict(c, i=bool(mr is not None and mr >= R0_CRUCE))
    return dict(mediana_R0_eval=m, frac_eval_sin_fund=round(fs, 4), evaluables=len(ev), n=len(xs), frac_eval=round(fe, 4),
                mediana_R0_real_eval=mr, cruza_con_R0_real=all(cr.values()), cruzan_real_linajes=sum(1 for x in xs if x['cruza_real']),
                cola_sobre_desc_med=med([x['cola_final'] / x['descendientes'] for x in xs if x['descendientes']]),
                condiciones=c, cruza=all(c.values()), casi_inmortales=sum(1 for x in xs if x['casi_inmortal']),
                cruzan_linajes=sum(1 for x in xs if x['cruza']))


def resumen_err99(R, log, ronda=None):
    """Por escuderia (ENMIENDA 2), monocultivo y SOLO (ENMIENDA 3), con las predicciones firmadas al lado.
    Series SELLADAS (ENMIENDA 4): criterio de la ENMIENDA 3 y predicciones de la ENMIENDA 4."""
    ns = len(R); ids = R[0]['pista']['ids'] if 'pista' in R[0] else [l['id'] for l in R[0]['linajes']]
    modo = ronda if ronda in PRED_ENM4 else ('r2' if (ronda or '').startswith('r2') else modo_de(ids))
    esc = {}
    for c in R:
        for l in c['linajes']: esc.setdefault(etiqueta_de(l['id']), []).append(l)
    log(f"\nERR-99 / ENMIENDA 2 (evaluable = >= {MIN_MUERTES} muertes; cruza = R0 >= {R0_CRUCE} y 0 fundadores tras t = {T_CORTE}) · modo {modo}")
    log(f"  {'escuderia':10s} {'lin-sem':>7} {'cruzan':>6} {'evaluab':>7} {'casi inm':>8} {'R0 eval med':>11} {'sem. que cruza':>14} "
        f"{'nac reales':>10} {'fund>10k med':>12} {'sin parir':>9} {'R0 REAL eval med':>16} {'cruzan real':>11}  gana")
    out = {}
    for e, xs in esc.items():
        por_sem = {}
        for x in xs: por_sem.setdefault(x['seed'], []).append(x['cruza'])
        sem_cruza = sum(1 for v in por_sem.values() if any(v))
        uno = all(len(v) == 1 for v in por_sem.values())
        gana = (sem_cruza >= GANA_FRAC * ns) if uno else None
        inc = sum(1 for x in xs if x['fund_post_incierto'])
        o = dict(linajes_semilla=len(xs), cruzan=sum(x['cruza'] for x in xs), evaluables=sum(x['evaluable'] for x in xs),
                 casi_inmortales=sum(x['casi_inmortal'] for x in xs), R0_eval_med=med([x['R0_eval'] for x in xs]),
                 R0_med_todos=med([x['R0'] for x in xs]), semillas_que_cruza=sem_cruza, semillas=ns, gana=gana,
                 nac_reales_med=med([x['nac_reales'] for x in xs]), fund_post_med=med([x['fund_post10k'] for x in xs]),
                 sin_parir_med=med([x['frac_muere_sin_parir'] for x in xs]), fund_post_incierto=inc,
                 casi_inmortal_semillas=len({x['seed'] for x in xs if x['casi_inmortal']}),
                 R0_real_eval_med=med([x['R0_real_eval'] for x in xs]), cruzan_real=sum(x['cruza_real'] for x in xs))
        out[e] = o
        log(f"  {e:10s} {o['linajes_semilla']:7d} {o['cruzan']:6d} {o['evaluables']:7d} {o['casi_inmortales']:8d} {str(o['R0_eval_med']):>11} "
            f"{str(sem_cruza) + '/' + str(ns):>14} {str(o['nac_reales_med']):>10} {str(o['fund_post_med']):>12} {str(o['sin_parir_med']):>9} "
            f"{str(o['R0_real_eval_med']):>16} {o['cruzan_real']:>11}  "
            f"{('SI' if gana else 'no') if gana is not None else '-- (varios linajes por semilla)'}"
            f"{'  [t_fund truncado e incierto en ' + str(inc) + ']' if inc else ''}")
    todos = [l for c in R for l in c['linajes']]
    res = dict(modo=modo, escuderias=out)
    if modo in ('mono', 'solo') or modo in PRED_ENM4:
        cm = criterio_mono(todos); res['criterio_enm3'] = cm
        cm['casi_inmortal_grupo'] = bool(cm['casi_inmortales'] > len(todos) - MONO_FRAC_EVAL * len(todos) + 1e-9)
        log(f"  {'MONOCULTIVO' if modo == 'mono' else ('SOLO' if modo == 'solo' else modo.upper())} (criterio ENMIENDA 3): (i) mediana R0 evaluables {cm['mediana_R0_eval']} >= {R0_CRUCE}: "
            f"{'si' if cm['condiciones']['i'] else 'no'} · (ii) evaluables sin fundadores tras t={T_CORTE} {cm['frac_eval_sin_fund']} >= "
            f"{MONO_FRAC_SIN_FUND}: {'si' if cm['condiciones']['ii'] else 'no'} · (iii) evaluables {cm['evaluables']}/{cm['n']} "
            f"(>= {MONO_FRAC_EVAL:.3f}): {'si' if cm['condiciones']['iii'] else 'no'} -> {'CRUZA' if cm['cruza'] else 'NO CRUZA'}")
        log(f"    ERR-100 (SOLO SE REPORTA; el criterio preregistrado no cambia): mediana del R0 de NACIMIENTOS REALES sobre evaluables "
            f"{cm['mediana_R0_real_eval']} · con esa mediana en (i) el grupo {'CRUZARIA' if cm['cruza_con_R0_real'] else 'NO cruzaria'} · "
            f"linajes-semilla que cruzan con R0 real {cm['cruzan_real_linajes']}/{cm['n']} · mediana cola_final/descendientes {cm['cola_sobre_desc_med']}")
    log("  PREDICCIONES FIRMADAS (ENMIENDAS 2 y 3) y lo medido:")
    if modo == 'oficial':
        fab = out.get('FABRICA', {}); h1 = out.get('H1', {}); o1 = out.get('O1', {}); s1 = out.get('S1', {})
        fm = fab.get('R0_med_todos'); hm = h1.get('R0_med_todos')
        med_ = [
            f"H1 {hm} vs FABRICA {fm} (diferencia {round(hm - fm, 3) if hm is not None and fm is not None else None}; "
            f"{'dentro' if hm is not None and fm is not None and abs(hm - fm) <= 0.10 else 'FUERA'} de +-0.10)",
            f"FABRICA {fm} ({'dentro' if fm is not None and 0.28 <= fm <= 0.45 else 'FUERA'} de 0.28-0.45)",
            f"O1 cruza en {o1.get('semillas_que_cruza')}/{ns} ({'>= 10' if (o1.get('semillas_que_cruza') or 0) >= 10 * ns / 20 else '< 10'} por 20); "
            f"gana: {'SI' if o1.get('gana') else 'no'}",
            f"O1 casi inmortal en {o1.get('casi_inmortal_semillas')}/{ns} semillas ({'>= 1' if o1.get('casi_inmortales') else 'ninguno'}; "
            f"{'>= 10' if (o1.get('casi_inmortal_semillas') or 0) >= 10 * ns / 20 else '< 10'} por 20)",
            f"S1 cruza en {s1.get('semillas_que_cruza')}/{ns} ({'NO cruza' if not s1.get('cruzan') else 'CRUZA en alguna'})"]
        for p_, m_ in zip(PRED_ENM['oficial'], med_): log(f"    - {p_}  ->  medido: {m_}")
        res['predicciones'] = list(zip(PRED_ENM['oficial'], med_))
    elif modo in PRED_ENM4:
        cm = res['criterio_enm3']; res['predicciones'] = []
        for txt, f in PRED_ENM4[modo]:
            m_ = (f"{'CRUZA' if cm['cruza'] else 'NO CRUZA'} (mediana R0 evaluables {cm['mediana_R0_eval']}; R0 REAL {cm['mediana_R0_real_eval']}; "
                  f"evaluables {cm['evaluables']}/{cm['n']}; casi inmortales {cm['casi_inmortales']}/{cm['n']}"
                  + (f"; 'queda casi inmortal' = los casi inmortales hacen caer (iii) (> 1/3): {'SI' if cm['casi_inmortal_grupo'] else 'no'}" if modo == 'sellada_sologrande' else '')
                  + f") -> la prediccion {'SE CUMPLE' if f(cm) else 'NO se cumple'}")
            log(f"    - {txt}  ->  medido: {m_}"); res['predicciones'].append((txt, m_))
    elif modo in ('mono', 'solo'):
        cm = res['criterio_enm3']
        m_ = f"{'CRUZA' if cm['cruza'] else 'NO CRUZA'} (mediana R0 evaluables {cm['mediana_R0_eval']})"
        log(f"    - {PRED_ENM[modo][0]}  ->  medido: {m_}"); res['predicciones'] = [(PRED_ENM[modo][0], m_)]
    elif modo == 'r2':
        log("    (ronda 2: el criterio y las predicciones que deciden estan en el bloque RONDA 2 / ENMIENDA 5 de abajo)")
    else:
        log("    (esta alineacion no tiene prediccion firmada)")
    return res


def resumen_r2(R, log, ronda):
    """ENMIENDA 5. Un LINAJE-semilla cruza si su R0 de NACIMIENTOS REALES >= 0.90 y 0 fundadores tras t=10000 (= cruza_real; sigue
    exigiendo >= 5 muertes: ERR-99 no se derogo, un casi inmortal no cuenta ni a favor ni en contra). Un EQUIPO cruza en una
    SEMILLA si mas de la mitad de sus linajes en esa semilla cruzan (R2_SEMILLA='mayoria'; la ENMIENDA 5 no fija la regla por
    semilla con varios linajes del mismo equipo: se reporta tambien 'todos'). GANA si cruza en >= 15/20 semillas."""
    ns = len(R); esc = {}
    for c in R:
        for l in c['linajes']: esc.setdefault(etiqueta_de(l['id']), {}).setdefault(c['seed'], []).append(l)
    log(f"\nRONDA 2 / ENMIENDA 5 (fundador limpio {'SI' if R[0]['pista'].get('fundador_limpio') else 'NO (!)'}; cruza = R0 de NACIMIENTOS REALES "
        f">= {R0_CRUCE} y 0 fundadores tras t = {T_CORTE}, con >= {MIN_MUERTES} muertes) · {ronda}")
    log(f"  {'equipo':10s} {'lin-sem':>7} {'cruzan':>6} {'evaluab':>7} {'casi inm':>8} {'R0 REAL eval med':>16} {'R0 prereg med':>13} "
        f"{'sem cruza (mayoria)':>19} {'(todos)':>8}  gana")
    out = {}
    for e, por in esc.items():
        xs = [x for v in por.values() for x in v]
        sm = sum(1 for v in por.values() if sum(x['cruza_real'] for x in v) * 2 > len(v))
        st_ = sum(1 for v in por.values() if all(x['cruza_real'] for x in v))
        o = dict(linajes_semilla=len(xs), cruzan=sum(x['cruza_real'] for x in xs), evaluables=sum(x['evaluable'] for x in xs),
                 casi_inmortales=sum(x['casi_inmortal'] for x in xs), R0_real_eval_med=med([x['R0_real_eval'] for x in xs]),
                 R0_eval_med=med([x['R0_eval'] for x in xs]), semillas_cruza_mayoria=sm, semillas_cruza_todos=st_, semillas=ns,
                 gana=bool(sm >= GANA_FRAC * ns))
        out[e] = o
        log(f"  {e:10s} {o['linajes_semilla']:7d} {o['cruzan']:6d} {o['evaluables']:7d} {o['casi_inmortales']:8d} {str(o['R0_real_eval_med']):>16} "
            f"{str(o['R0_eval_med']):>13} {str(sm) + '/' + str(ns):>19} {str(st_) + '/' + str(ns):>8}  {'SI' if o['gana'] else 'no'}"
            f"{'  (FABRICA: piso, no compite)' if e == 'FABRICA' else ''}")
    log("  PREDICCIONES FIRMADAS (ENMIENDA 5) -- se leen sobre el conjunto de series; lo de esta serie:")
    eq = [e for e in out if e != 'FABRICA']
    txt = {'r2mono': f"monocultivo de {eq}: gana {'SI' if any(out[e]['gana'] for e in eq) else 'no'}",
           'r2fab': f"pista con 6 FABRICA, equipo {eq}: gana {'SI' if any(out[e]['gana'] for e in eq) else 'no'}",
           'r2mix3': f"pista mixta O2/O3/O4: ganan {[e for e in eq if out[e]['gana']] or 'ninguno'}",
           'r2o1mono': f"O1 con fundador limpio en monocultivo: cruza en {out.get('O1', {}).get('semillas_cruza_mayoria')}/{ns} semillas -> "
                       f"{'SE CUMPLE (cruza)' if out.get('O1', {}).get('gana') else 'no cruza'}"}.get(ronda.split('_')[0], '')
    for p_ in PRED_R2: log(f"    - {p_}")
    log(f"    medido en esta serie: {txt}")
    per = persistencia_r2(R, log, ronda)
    return dict(ronda=ronda, equipos=out, regla_semilla=R2_SEMILLA, medido=txt, persistencia=per)


PRED_E6 = {('O2', 'mono'): 0.45, ('O2', 'fab'): 0.15, ('O3', 'mono'): 0.50, ('O4', 'mono'): 0.35, ('O1', 'mono'): 0.55}


def persistencia_r2(R, log, ronda):
    """ENMIENDA 6 / ERR-102, co-principal: un linaje-semilla PERSISTE si 0 fundadores tras t=10000 y >= 5 nacimientos reales;
    un equipo ESTABILIZA en una semilla si persiste MAS DE LA MITAD de sus linajes; ESTABILIZA LA RONDA con >= 15/20 semillas.
    Muertes voluntarias FISICAS (la que cuenta): muere en el paso en que mordio una letra mala ya mordida por su linaje y cuyo efecto
    cae en la necesidad por la que muere. Lo que declara el carro se muestra al lado y no cuenta."""
    ns = len(R); esc = {}
    for c in R:
        for l in c['linajes']: esc.setdefault(etiqueta_de(l['id']), {}).setdefault(c['seed'], []).append(l)
    base = ronda.split('_')[0]; modo = {'r2mono': 'mono', 'r2o1mono': 'mono', 'r2fab': 'fab', 'r2mix3': 'mix'}.get(base, base)
    log(f"\nPERSISTENCIA / ENMIENDA 6 (co-principal; persiste = 0 fundadores tras t = {T_CORTE} y >= {MIN_NAC_PERSISTE} nacimientos reales; "
        f"estabiliza en una semilla si persiste > 1/2 de sus linajes; estabiliza la ronda con >= {int(GANA_FRAC * 20)}/20)")
    log(f"  {'equipo':10s} {'lin-sem':>7} {'persisten':>9} {'nac reales med':>14} {'sem estabiliza':>14}  estabiliza   "
        f"muertes voluntarias FISICAS (fraccion)   declaradas por el carro (no cuentan)")
    out = {}
    for e, por in esc.items():
        xs = [x for v in por.values() for x in v]
        se = sum(1 for v in por.values() if sum(x['persiste'] for x in v) * 2 > len(v))
        mv = [x.get('muertes_vol') for x in xs]; mu = sum(x['muertes'] for x in xs)
        vol = (sum(mv) if all(v is not None for v in mv) else None)
        dec = {}
        for x in xs:
            for k, v in (x.get('carro_declara') or {}).items(): dec[k] = dec.get(k, 0) + v
        o = dict(persisten=sum(x['persiste'] for x in xs), linajes_semilla=len(xs), nac_reales_med=med([x['nac_reales'] for x in xs]),
                 semillas_estabiliza=se, estabiliza=bool(se >= GANA_FRAC * ns), muertes=mu, muertes_vol=vol,
                 frac_vol=(round(vol / mu, 4) if vol is not None and mu else None), carro_declara=dec or None)
        out[e] = o
        log(f"  {e:10s} {o['linajes_semilla']:7d} {o['persisten']:9d} {str(o['nac_reales_med']):>14} {str(se) + '/' + str(ns):>14}  "
            f"{'SI' if o['estabiliza'] else 'no':10s}  {str(vol) + '/' + str(mu) if vol is not None else 'no disponible (crudo anterior)'} "
            f"({o['frac_vol']})   {dec or '-'}{'  (FABRICA: piso)' if e == 'FABRICA' else ''}"
            f"{'  -> con muerte programada' if o['estabiliza'] and o['frac_vol'] else ''}")
    log("  PREDICCIONES FIRMADAS (ENMIENDA 6, persistencia) y lo medido en esta serie:")
    hay = False
    for (eq, md_), p_ in PRED_E6.items():
        if md_ == modo and eq in out:
            hay = True
            log(f"    - {eq} estabiliza en {md_} (p {p_})  ->  medido: {'ESTABILIZA' if out[eq]['estabiliza'] else 'NO estabiliza'} "
                f"({out[eq]['semillas_estabiliza']}/{ns} semillas)")
    if not hay: log("    (ninguna prediccion de persistencia para esta alineacion)")
    return out


def recalcula(ruta, log=print):
    """Aplica la letra de ERR-99 a un CRUDO viejo (sin t_fund): reconstruye t_fund y la cola final desde telem y
    VERIFICA contra fundadores y cola_final del crudo. Si no verifica, lo dice y no inventa."""
    d = json.load(open(ruta, encoding='utf-8'))
    T = d['meta']['T']; R = d['corridas']; nover = 0
    for c in R:
        for l in c['linajes']:
            te = l.get('telem') or {}
            if 'vidas' not in te or 'desc_por_vida' not in te:
                raise SystemExit(f"RECALCULA: {ruta} no guarda vidas/desc_por_vida por cuerpo: NO se puede aplicar ERR-99")
            tf, qf, nr = t_fund_reconstruido(te['vidas'], te['desc_por_vida'])
            ok = (len(tf) == l['fundadores'] and qf == l['cola_final'])
            nover += int(not ok)
            l.update(err99(l['muertes'], l['fundadores'], tf, l['descendientes'], T, te['vidas'], te['desc_por_vida'],
                           nac_reales=nr, cola_final=l['cola_final'], t_fund_fuente='reconstruido' + ('' if ok else ' SIN VERIFICAR')))
            l['t_fund_rec'] = tf
    nt = sum(len(c['linajes']) for c in R)
    log(f"RECALCULO ERR-99 de {os.path.basename(ruta)} · T={T} · carros {d['meta']['carros']} · semillas {d['meta']['semillas']}")
    log(f"  t_fund reconstruido desde telem (vidas + hijos por cuerpo): verificado contra fundadores y cola_final en {nt - nover}/{nt} linajes-semilla")
    for c in R:
        for l in c['linajes']:
            log(f"  s{c['seed']} {l['id']:8s} muertes {l['muertes']:3d} desc {l['descendientes']:3d} R0 {l['R0']:<7} evaluable {int(l['evaluable'])} "
                f"fund {l['fundadores']} t_fund {l['t_fund_rec']} fund>10k {l['fund_post10k']} nac reales {l['nac_reales']} cola {l['cola_final']} "
                f"R0 real {l['R0_real']} -> cruza {int(l['cruza'])} · cruza_real {int(l['cruza_real'])}")
    if T != T_DEF: log(f"  OJO: T = {T} (no {T_DEF}): la letra de ERR-99 esta escrita para T = {T_DEF}; se aplica igual, a titulo informativo")
    e = resumen_err99(R, log, d['meta'].get('ronda'))
    if (d['meta'].get('ronda') or '').startswith('r2'): e['ronda2'] = resumen_r2(R, log, d['meta']['ronda'])
    return e


def parse_carros(txt):
    out = []
    for tok in (x.strip() for x in txt.split(',') if x.strip()):
        if '*' in tok:
            a, k = tok.split('*'); out += [a.strip()] * int(k)
        else: out.append(tok)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--ronda', default='0')
    ap.add_argument('--carros', default=None)   # p. ej. O1,S1,H1,FABRICA*6 ; si falta, el atajo de --ronda (ALINEACIONES)
    ap.add_argument('--recalcula', default=None)   # ruta de un crudo viejo: aplica ERR-99 y ERR-100 y termina
    ap.add_argument('--recalcula_json', default=None)   # opcional: escribe el resumen del recalculo
    ap.add_argument('--desde', type=int, default=None)   # por defecto 4001; en las series sellada_* 5001 (SELLADAS)
    ap.add_argument('--fundador_limpio', type=int, default=None)   # ENMIENDA 5; los atajos r2* lo ponen en 1
    ap.add_argument('--equipo', default=None)   # para --ronda r2mono / r2fab
    ap.add_argument('--mundo_N', type=int, default=None)   # ENMIENDA 4: mundo dimensionado para M carros (L=40M, nobj=4M, olvido xM)
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--T', type=int, default=T_DEF)
    ap.add_argument('--pizarra', type=int, default=1)
    ap.add_argument('--rep_acum', type=int, default=0)
    ap.add_argument('--escala', type=int, default=1)   # ENMIENDA 1
    ap.add_argument('--pool', type=int, default=int(os.environ.get('JUACO_POOL', 0)))
    a = ap.parse_args()
    if a.recalcula:
        res = recalcula(a.recalcula)
        if a.recalcula_json: json.dump(res, open(a.recalcula_json, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return 0
    if a.ronda.startswith('r2') and not a.carros: a.carros = ','.join(alineacion_r2(a.ronda, a.equipo))
    if a.fundador_limpio is None: a.fundador_limpio = 1 if a.ronda.startswith('r2') else 0
    if a.ronda.startswith('r2') and not a.fundador_limpio: raise SystemExit('JUEZ: la ronda 2 exige --fundador_limpio 1 (ENMIENDA 5)')
    if a.ronda.startswith('r2') and a.equipo: a.ronda = f"{a.ronda}_{a.equipo}" if a.ronda in ('r2mono', 'r2fab') else a.ronda
    carros = parse_carros(a.carros) if a.carros else list(ALINEACIONES.get(a.ronda, ['FABRICA'] * 9))
    if a.mundo_N is None: a.mundo_N = MUNDO_ATAJO.get(a.ronda)
    if a.desde is None: a.desde = (DESDE_R2 if a.ronda.startswith('r2') else
                                   DESDE_ATAJO.get(a.ronda, DESDE_SELLADA if a.ronda.startswith('sellada') else 4001))
    if a.humo:
        semillas = [4001, 4002]; pool = 0; etiqueta = f"humo_ronda{a.ronda}"
    else:
        semillas = list(range(a.desde, a.desde + a.n)); pool = a.pool; etiqueta = f"ronda{a.ronda}_s{semillas[0]}-{semillas[-1]}"
    os.makedirs(DATOS, exist_ok=True)
    sel = time.strftime('%Y%m%d_%H%M%S'); pre = f"carrera_{etiqueta}_{sel}"
    LOGF = open(os.path.join(DATOS, pre + '.log'), 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    shas = {c: P.h16(os.path.join(P.CARROS, c + '.py')) for c in sorted(set(carros))}
    log(f"JUEZ · {etiqueta} · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'}")
    log(f"  pista.py {P.h16(os.path.join(AQUI,'pista.py'))} · juez.py {P.h16(os.path.abspath(__file__))} · carros {shas}")
    log(f"  carros (orden = indice de linaje): {carros} · semillas {semillas[0]}-{semillas[-1]} · T={a.T} · pizarra {a.pizarra} · rep_acum {a.rep_acum} · escala {a.escala} · mundo_N {a.mundo_N or 'N (el de los carros)'} · fundador_limpio {a.fundador_limpio}")
    rv = {c: RC.revisa(c) for c in sorted(set(carros))}
    for c, v in rv.items():
        log(f"  CHEQUEO ESTATICO {c}: {'PASA' if not v else 'RECHAZADO'}" + ''.join(chr(10) + '     ' + x for x in v))
    if any(rv.values()):
        log("  UN CARRO NO PASA EL CHEQUEO ESTATICO (ERR-96) -> la ronda NO se corre."); return 1
    ide = identidad_corta()
    log(f"  IDENTIDAD CORTA: sha f9c {ide['sha_f9c']} ({'OK' if ide['sha_ok'] else 'DISTINTO'}) · FABRICA solo == organismo_f9c REL "
        f"(s=1, T=5000): {'OK' if not ide['dif'] else 'FALLA ' + str(ide['dif'][:5])}")
    if not ide['ok']:
        log("  IDENTIDAD FALLA -> la ronda NO se corre."); return 1
    tareas = [(s, carros, a.T, a.pizarra, a.rep_acum, a.escala, a.mundo_N, a.fundador_limpio) for s in semillas]
    R = []
    if pool and pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as PL:
            for x in PL.imap_unordered(tarea, tareas):
                R.append(x); log(f"  [{time.time()-t0:7.1f}s] semilla {x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']}")
    else:
        for tk in tareas:
            x = tarea(tk); R.append(x)
            log(f"  [{time.time()-t0:7.1f}s] semilla {x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']} · R0 por linaje "
                f"{[l['R0'] for l in x['linajes']]}")
    R.sort(key=lambda x: x['seed'])
    piz = os.path.join(DATOS, pre + '_pizarra.jsonl.gz')   # ENMIENDA 1: la pizarra COMPLETA, aparte de la telemetria
    with gzip.open(piz, 'wt', encoding='utf-8') as fz:
        for x in R:
            for e in x.pop('pizarra_log'): fz.write(json.dumps([x['seed']] + e) + chr(10))
    meta = dict(etiqueta=etiqueta, ronda=a.ronda, sello=sel, semillas=semillas, T=a.T, pizarra=a.pizarra, rep_acum=a.rep_acum,
                carros=carros, sha_carros=shas, escala=a.escala, mundo_N=a.mundo_N, fundador_limpio=a.fundador_limpio, chequeo_estatico=rv, sha_pista=P.h16(os.path.join(AQUI, 'pista.py')),
                sha_juez=P.h16(os.path.abspath(__file__)), sha_f9c=ide['sha_f9c'], identidad_corta=ide,
                W_CAUSA=P.W_CAUSA, CUPO=P.CUPO, ANCHO=P.ANCHO, ref=REF_REL)
    crudo = os.path.join(DATOS, pre + '.json')     # ERR-54: el crudo ANTES de resumir
    json.dump(dict(meta=meta, corridas=R), open(crudo, 'w', encoding='utf-8'), ensure_ascii=False)
    log(f"  CRUDO {crudo} (sha {P.h16(crudo)})")
    tab, r0p = informe(R, meta, log)
    e99 = resumen_err99(R, log, a.ronda)
    if a.ronda.startswith('r2'): e99['ronda2'] = resumen_r2(R, log, a.ronda)
    log(f"  PIZARRA completa {piz}")
    if carros == ['FABRICA'] * 9:
        todos = [l['R0'] for c in R for l in c['linajes']]
        mr = med(todos); lo, hi = PRED_RONDA0[1 if a.escala else 0]
        log(f"\n  PREDICCION FIRMADA ({'ENMIENDA 1, pista escalada' if a.escala else 'organizador, pista sin escalar'}): con 9 FABRICA "
            f"la mediana del R0 por linaje cae en {lo}-{hi}. Medido: mediana de los {len(todos)} linajes-semilla {mr} "
            f"(min {min(todos)}, max {max(todos)}) -> {'DENTRO del rango' if lo <= mr <= hi else ('DEBAJO del rango' if mr < lo else 'ENCIMA del rango')}")
    res = os.path.join(DATOS, pre + '_resumen.json')
    json.dump(dict(meta=meta, tabla=tab, R0_pista=r0p, err99=e99), open(res, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"  RESUMEN {res}")
    log(f"\nTerminado en {time.time()-t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
