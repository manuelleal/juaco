"""corre_molde.py — EXPLORATORIO, no es dato. UNA corrida por proceso: 9 carros iguales en la PISTA DE LA CARRERA (pista.py importado tal
cual, solo lectura), fundador limpio, T 100 000, pizarra encendida, juez.resumen_linaje (solo fisica). Las perillas del carro MOLDE se ponen
por brazo antes de crear los carros. MISION: llegar a la AGI por este camino.
    python corre_molde.py --brazo piz --semilla 38001 [--T 100000]
    python corre_molde.py --identidad          (MOLDE con perillas 0 == V143 en la pista, fisica entera, s 38901 T 3000; y revisa_carro)
Escribe datos/<brazo>_s<semilla>_T<T>.json. Semillas solo 38001-38999. Sin Pool."""
import argparse, hashlib, importlib.util, json, os, sys, time

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
PISTA = r'C:\Users\User\Documents\PROYECTOS\JUACO\bundle\experimentos\carrera_escuderias'
V143 = r'C:\Users\User\Documents\PROYECTOS\JUACO\bundle\experimentos\tronco_v14_3\carros_v143\V143.py'
sys.path[:0] = [PISTA]
import pista as P
import juez as J
import revisa_carro as RC

DATOS = os.path.join(AQUI, 'datos')
_MODS = {}
PERILLAS = ('PIZ', 'PIZ_BAR', 'PIZ_FUND', 'IMITA', 'ESPERA', 'PIZ_ADS', 'BARRE', 'BARRE_V2')

BRAZOS = {
    'v143':     dict(),
    'piz':      dict(PIZ=1),
    'piz_bar':  dict(PIZ=1, PIZ_BAR=1),
    'piz_fund': dict(PIZ=1, PIZ_FUND=1),
    'imita':    dict(IMITA=1),
    'espera':   dict(ESPERA=1),
    # ola 2 (tras leer piz s38001: la cultura destapa el fundador pero nadie limpia el mundo)
    'piz_ads':   dict(PIZ=1, PIZ_ADS=1),
    'barre':     dict(BARRE=1),
    'piz_barre': dict(PIZ=1, BARRE=1),
    'piz_ads_barre': dict(PIZ=1, PIZ_ADS=1, BARRE=1),
    # ola 3 (tras leer barre s38002: la dosis 1 limpia el mundo y esteriliza: desc 0)
    'barre2':     dict(BARRE=1, BARRE_V2=1),
    'piz_barre2': dict(PIZ=1, BARRE=1, BARRE_V2=1),
    'o1':       None,
}


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def modulo(nombre, ruta):
    if nombre not in _MODS:
        spec = importlib.util.spec_from_file_location(nombre, ruta)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); _MODS[nombre] = m
    return _MODS[nombre]


def carro(brazo):
    if brazo == 'o1': return ('O1', P.carga_carro('O1'))
    m = modulo('carro_MOLDE', os.path.join(AQUI, 'carros', 'MOLDE.py'))
    for k in PERILLAS: setattr_mod(m, k, int(BRAZOS[brazo].get(k, 0)))
    return ('MOLDE', m)


def setattr_mod(m, k, v):
    m.__dict__[k] = v


def fisica(r):
    """Solo las claves fisicas de cada linaje + pista (sin 'carro'), serializable."""
    return json.loads(json.dumps(dict(linajes=[{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']],
                                      pista={k: v for k, v in r['pista'].items() if k != 'ids'}), default=str))


def identidad():
    s, T = 38901, 3000
    v = modulo('carro_V143', V143)
    a = fisica(P.run(s, [('V143', v)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, fundador_limpio=1))
    m = ('V143', carro('v143')[1])   # misma etiqueta: solo cambia el cerebro
    b = fisica(P.run(s, [m] * 9, T=T, pizarra=1, rep_acum=0, escala=1, fundador_limpio=1))
    ok = a == b
    print(f"IDENTIDAD MOLDE(0) == V143 en la pista (9 carros, fundador limpio, s {s}, T {T}): {'OK' if ok else 'FALLA'}")
    if not ok:
        for i, (x, y) in enumerate(zip(a['linajes'], b['linajes'])):
            for k in x:
                if x[k] != y.get(k): print('  dif linaje', i, k)
        for k in a['pista']:
            if a['pista'][k] != b['pista'].get(k): print('  dif pista', k)
    src = open(os.path.join(AQUI, 'carros', 'MOLDE.py'), encoding='utf-8').read()
    viol = RC.revisa_fuente(src, 'MOLDE')
    print(f"revisa_carro MOLDE: {'PASA' if not viol else 'RECHAZADO'}", *viol, sep='\n  ')
    # humo de que las perillas hacen algo: piz escribe y lee; imita manda mensajes; espera veta
    for br in ('piz', 'imita', 'espera', 'piz_ads', 'piz_barre', 'piz_ads_barre', 'barre2', 'piz_barre2'):
        r = P.run(s, [carro(br)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, fundador_limpio=1)
        mol = [d['carro']['molde'] for d in r['linajes']]
        print(f"  {br}: pizarra_n {len(r['pizarra_log'])} · escritos {sum(x['escritos'] for x in mol)} leidos {sum(x['leidos'] for x in mol)} "
              f"msgs {sum(x['msgs'] for x in mol)} imit {sum(x['imit_msgs'] for x in mol)} vetos {sum(x['vetos'] for x in mol)} "
              f"(fisicos {sum(d['_carrera']['vetos'] for d in r['linajes'])}) · ads_cult {sum(x['ads_cult'] for x in mol)} tapado {sum(x['tapado'] for x in mol)} barre_obj {sum(x['barre_obj'] for x in mol)} barridas {sum(x['barridas'] for x in mol)} veto_vent {sum(x['barre_veto_ventana'] for x in mol)} · desc {sum(d['descendientes'] for d in r['linajes'])} · comp {r['pista']['comp_mundo']} · muertes {[d['deaths'] for d in r['linajes']]} "
              f"· fund {[d['fundadores'] for d in r['linajes']]}")
    return 0 if (ok and not viol) else 1


def corre(brazo, seed, T):
    c = carro(brazo)
    r = P.run(seed, [c] * 9, T=T, pizarra=1, rep_acum=0, escala=1, fundador_limpio=1)
    L = [J.resumen_linaje(d, seed) for d in r['linajes']]
    for x in L:
        tf, qf, nr = J.t_fund_reconstruido(x['telem']['vidas'], x['telem']['desc_por_vida'])
        x['t_fund_rec_ok'] = bool(tf[:200] == x['telem']['t_fund'] and qf == x['cola_final'] and nr == x['nac_reales'])
        dg = x.pop('diag', None) or {}
        x['diag_corto'] = {k: dg.get(k) for k in ('robos', 'frac_sin_bueno', 'limpiezas', 'mordidas_malas')}
    tel = [dict(molde=d['carro'].get('molde'), v143=d['carro'].get('v143'),
                letras=(d['carro'].get('apr') or {}).get('letras'), apr_pol=(d['carro'].get('apr') or {}).get('politica'),
                o1=({k: d['carro'].get(k) for k in ('tabla', 'n', 'pruebas', 'limpias', 'cuerpos')} if brazo == 'o1' else None))
           for d in r['linajes']]
    sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
    return dict(brazo=brazo, seed=seed, T=T, perillas=BRAZOS[brazo], linajes=L, pista=r['pista'],
                R0_pista=round(sd / (sm + len(L)), 4), pizarra_n=len(r['pizarra_log']), tel=tel)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--brazo'); ap.add_argument('--semilla', type=int); ap.add_argument('--T', type=int, default=100000)
    ap.add_argument('--identidad', action='store_true')
    a = ap.parse_args()
    if a.identidad: return identidad()
    if a.brazo is None or a.semilla is None: raise SystemExit('--brazo y --semilla')
    if not 38001 <= a.semilla <= 38999: raise SystemExit('semillas solo 38001-38999')
    if a.brazo not in BRAZOS: raise SystemExit(f"brazo desconocido {a.brazo}; validos {list(BRAZOS)}")
    os.makedirs(DATOS, exist_ok=True)
    out = os.path.join(DATOS, f"{a.brazo}_s{a.semilla}_T{a.T}.json")
    t0 = time.time()
    r = corre(a.brazo, a.semilla, a.T)
    r['seg'] = round(time.time() - t0, 1)
    r['sha'] = dict(pista=h16(os.path.join(PISTA, 'pista.py')), juez=h16(os.path.join(PISTA, 'juez.py')),
                    carro=h16(os.path.join(AQUI, 'carros', 'MOLDE.py')) if a.brazo != 'o1' else h16(os.path.join(PISTA, 'carros', 'O1.py')),
                    corre=h16(os.path.abspath(__file__)))
    json.dump(r, open(out, 'w', encoding='utf-8'), default=str)
    import statistics as st
    R0 = [l['R0_real'] for l in r['linajes']]
    print(f"{a.brazo} s{a.semilla} T{a.T} {r['seg']}s · R0 real med {st.median(R0):.3f} · cruzan {sum(l['cruza_real'] for l in r['linajes'])}/9 · "
          f"persisten {sum(l['persiste'] for l in r['linajes'])}/9 · fund med {st.median([l['fundadores'] for l in r['linajes']])} · "
          f"vida {st.median([l['vida_med'] for l in r['linajes']])} · pizarra {r['pizarra_n']} · {out}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
