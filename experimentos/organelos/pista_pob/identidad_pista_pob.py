"""identidad_pista_pob.py — ARNES de pista_pob (29-sep-2026, creador). Un proceso, sin Pool. Escribe identidad_pista_pob_salida.txt ENTERA.

MISION: llegar a la AGI por este camino. Se corre ANTES de mirar cualquier numero del humo o de la exploracion.
  (0) shas fijados + run_gen construido por ANCLAS desde pista.py (cada ancla una vez).
  I1  K = 1 == pista.run BIT A BIT (salida ENTERA): FABRICA compat=1 pizarra 0 T 5000 s 1 (el ancla de juez.identidad_corta; y su
      vista plana == organismo_f9c REL); 9 x O1, 9 x V143_TERMO, 9 x V143_BQ2 a T 20 000 (fundador limpio, pizarra 1), modo 'sel'
      (con K = 1 no hay otra copia: la camara esta puesta y no puede actuar). BQ2: tambien el estado de MODULO (_BQ_BANCO, _BQ_TEL).
  I2  K = 2 SIN migracion (modo 'nada'): copia c == pista.run(semilla_copia(seed, c)) BIT A BIT (+ estado de modulo). CONTROL que DEBE
      fallar: con UN modulo compartido por las dos copias (canal oculto abierto) la copia 1 != pista.run (prueba que el canal existe y
      que carga_modulo lo cierra).
  I3  CONTABILIDAD (K = 2, V143_BQ2, T 20 000, sel y neutro): fundadores == migrantes + limpios por copia y linaje; depositos ==
      descendientes; pool final == min(depositos, tope); ninguna migracion desde la propia copia; juez: contabilidad fisica coherente
      y t_fund reconstruible; migrantes > 0; sel != nada, neutro != nada, sel != neutro (la migracion ACTUA); siembra <= 50 por linaje
      y sin listas vacias; determinismo (sel K = 2 T 3000 dos veces).
  I4  REGLA 14 (entrada campo a campo): la medida del runner (corre_pista_pob.prueba) == corre_bp.tarea (T 3000, con siembra); y las
      REFERENCIAS guardadas se REPRODUCEN hoy bit a bit (menos 'seg'): bloq2 s59201 y bloq_pas s59201 (siembra = bancos finales de
      pasajes_Tp25000_np4/bloq_c1_p3_s59223.json), T 100 000 -> los JSON de explora_T100000 son pareables con estos shas.
    python experimentos/organelos/pista_pob/identidad_pista_pob.py [--sin_i4]
"""
import argparse, copy, json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_pista_pob as R
PP = R.PP; P = R.P; J = R.J; CB = R.CB
N = lambda x: json.loads(json.dumps(x, default=str))
SEM_I1 = 59892; SEM_I2 = 59893
RUTA = dict(FABRICA=os.path.join(R.PISTAD, 'carros', 'FABRICA.py'), O1=os.path.join(R.PISTAD, 'carros', 'O1.py'),
            V143_TERMO=os.path.join(R.TERMOD, 'carros', 'V143_TERMO.py'), V143_BQ2=R.CARRO_BQ2)


def estado_bq(m):
    return N(dict(banco=m._BQ_BANCO, cnt=m._BQ_CNT, tel=m._BQ_TEL))


def vieja(seed, ident, T, n=9, **kw):
    """pista.run con un modulo NUEVO del carro (preparado como en la ronda 2 si es BQ2)."""
    m = PP.carga_modulo(RUTA[ident], f"carro_{ident}_viejo_{seed}_{time.time_ns()}")
    if ident == 'V143_BQ2': R.prepara_bq(m, 0, seed)
    return N(P.run(seed, [(ident, m)] * n, T=T, **kw)), m


def pob(seed, K, ident, T, modo, n=9, guarda=None, **kw):
    mods = []
    def prep(m, c, sc):
        if ident == 'V143_BQ2': R.prepara_bq(m, c, sc)
        mods.append(m)
    bq = ident == 'V143_BQ2'
    r = PP.run(seed, K, RUTA[ident], T, modo=modo, ident=ident, prepara=prep, ref_vivo=(PP.ref_reglas_bq if bq else None),
               muta=(PP.muta_bq if bq else None), n=n, **kw)
    return r, mods


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--sin_i4', action='store_true'); a = ap.parse_args()
    LOGF = open(R.SALIDA_ARNES, 'w', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t00 = time.time(); ok = True
    log(f"ARNES pista_pob · {time.strftime('%Y-%m-%d %H:%M:%S')} · pista_pob.py {R.h16(os.path.join(R.PISTAD, 'pista_pob.py'))} · "
        f"corre_pista_pob.py {R.h16(os.path.join(AQUI, 'corre_pista_pob.py'))} · identidad_pista_pob.py {R.h16(os.path.abspath(__file__))}")
    log("(0) shas fijados y run_gen por anclas")
    v = R.verifica(log); ok &= v
    log(f"  CFG (tasas BQ_C ronda 2) {R.cfg()}")

    log("I1  K = 1 == pista.run BIT A BIT (salida ENTERA)")
    t0 = time.time()
    r, _ = pob(1, 1, 'FABRICA', 5000, 'sel', n=1, pizarra=0, compat=1, fundador_limpio=0)
    b = N(P.run(1, ['FABRICA'], T=5000, pizarra=0, compat=1))
    i = N(r['copias'][0]) == b; ok &= i
    ic = J.identidad_corta()   # F9C REL == pista compat (el ancla del juez) ...
    import organismo_f9c as F9C, corre_bloque2 as CB2
    fa = F9C.run(1, T=5000, **CB2.BRAZOS['REL']); pl = P.plano(r['copias'][0]['linajes'][0])
    dif = [k for k in fa if k not in pl or N(fa[k]) != N(pl[k])] + [k for k in pl if k not in fa]
    ok &= ic['ok'] and not dif
    log(f"  FABRICA compat=1 T 5000 s 1: pista_pob K=1 == pista.run: {'OK' if i else 'FALLA'} · juez.identidad_corta {'OK' if ic['ok'] else 'FALLA'} · "
        f"plano(pista_pob) == organismo_f9c REL: {'OK' if not dif else 'FALLA ' + str(dif[:5])} ({time.time() - t0:.0f}s)")
    for ident in ('O1', 'V143_TERMO', 'V143_BQ2'):
        t0 = time.time()
        b, mb = vieja(SEM_I1, ident, 20000, pizarra=1, fundador_limpio=1)
        r, mods = pob(SEM_I1, 1, ident, 20000, 'sel', pizarra=1, fundador_limpio=1)
        i = N(r['copias'][0]) == b
        if ident == 'V143_BQ2': i = i and estado_bq(mods[0]) == estado_bq(mb)
        ok &= i
        L = [J.resumen_linaje(d, SEM_I1) for d in b['linajes']]
        log(f"  9 x {ident} s {SEM_I1} T 20000 fundador limpio: {'OK' if i else 'FALLA'}{' (salida + estado de modulo)' if ident == 'V143_BQ2' else ''} · "
            f"fundadores {sum(l['fundadores'] for l in L)} · migrantes {sum(map(sum, r['camara']['migrantes']))} · depositos "
            f"{sum(r['camara']['depositos'])} ({time.time() - t0:.0f}s)")

    log("I2  K = 2 SIN migracion (modo 'nada'): copia c == pista.run(semilla_copia) BIT A BIT; control con modulo compartido")
    t0 = time.time()
    r, mods = pob(SEM_I2, 2, 'V143_BQ2', 20000, 'nada', pizarra=1, fundador_limpio=1)
    for c in range(2):
        sc = PP.semilla_copia(SEM_I2, c)
        b, mb = vieja(sc, 'V143_BQ2', 20000, pizarra=1, fundador_limpio=1)
        i = N(r['copias'][c]) == b and estado_bq(mods[c]) == estado_bq(mb); ok &= i
        log(f"  copia {c} (semilla {sc}) == pista.run: {'OK' if i else 'FALLA'} (salida + estado de modulo) · migrantes "
            f"{sum(r['camara']['migrantes'][c])} · limpios {sum(r['camara']['limpios'][c])}")
        if c == 1: b1 = b
    ro, _ = pob(SEM_I2, 2, 'V143_BQ2', 20000, 'nada', pizarra=1, fundador_limpio=1, _compartir_modulo=True)
    d = N(ro['copias'][1]) != b1; ok &= d
    log(f"  CONTROL canal oculto (UN modulo para las 2 copias): copia 1 != pista.run: {'OK (difiere: el canal existe y carga_modulo lo cierra)' if d else 'FALLA (igual)'} "
        f"({time.time() - t0:.0f}s)")
    rnada = r

    log("I3  CONTABILIDAD (K = 2, V143_BQ2, s %d, T 20000)" % SEM_I2)
    t0 = time.time(); salidas = {'nada': N(rnada['copias'])}
    for modo in ('sel', 'neutro'):
        r, _ = pob(SEM_I2, 2, 'V143_BQ2', 20000, modo, pizarra=1, fundador_limpio=1)
        cam = r['camara']; salidas[modo] = N(r['copias']); fallas = []
        for c, o in enumerate(r['copias']):
            sc = PP.semilla_copia(SEM_I2, c)
            for i_, dd in enumerate(o['linajes']):
                x = J.resumen_linaje(dd, sc)
                tf, qf, nr = J.t_fund_reconstruido(x['telem']['vidas'], x['telem']['desc_por_vida'])
                if x['fundadores'] != cam['migrantes'][c][i_] + cam['limpios'][c][i_]: fallas.append(('fund != mig + limpios', c, i_))
                if cam['dep_por_copia'][c][i_] != x['descendientes']: fallas.append(('depositos != descendientes', c, i_))
                if not x['coherente']: fallas.append(('juez incoherente', c, i_))
                if not (tf[:200] == x['telem']['t_fund'] and qf == x['cola_final'] and nr == x['nac_reales']): fallas.append(('t_fund', c, i_))
        for i_ in range(9):
            if cam['pool_final'][i_] != min(cam['depositos'][i_], cam['tope']): fallas.append(('pool final', i_))
            if sum(cam['origen_mig'][c][i_][c] for c in range(2)) != 0: fallas.append(('origen propio', i_))
        if cam['malas_marcas'] != 0: fallas.append(('malas marcas', cam['malas_marcas']))
        nm = sum(map(sum, cam['migrantes']))
        if nm == 0: fallas.append(('0 migrantes',))
        sb = r['siembra']; por = cam['siembra_por_linaje']
        if any(p > PP.N_SIEMBRA for p in por) or any(len(x) == 0 for x in sb) or len(sb) != sum(por): fallas.append(('siembra',))
        ok &= not fallas
        log(f"  {modo}: migrantes {nm} · limpios {sum(map(sum, cam['limpios']))} · fundadores {sum(sum(l['fundadores'] for l in o['linajes']) for o in salidas[modo])} · "
            f"depositos {sum(cam['depositos'])} · pool final {cam['pool_final']} (tope {cam['tope']}) · muestras {cam['t_muestras']} · "
            f"siembra {len(sb)} ({por}) -> {'OK' if not fallas else 'FALLA ' + str(fallas[:5])}")
    dd = [salidas['sel'] != salidas['nada'], salidas['neutro'] != salidas['nada'], salidas['sel'] != salidas['neutro']]
    ok &= all(dd)
    log(f"  DEBEN DIFERIR: sel != nada {dd[0]} · neutro != nada {dd[1]} · sel != neutro {dd[2]} -> {'OK' if all(dd) else 'FALLA'}")
    x1, _ = pob(SEM_I2, 2, 'V143_BQ2', 3000, 'sel'); x2, _ = pob(SEM_I2, 2, 'V143_BQ2', 3000, 'sel')
    x1['meta'].pop('seg'); x2['meta'].pop('seg'); d = N(x1) == N(x2); ok &= d
    log(f"  determinismo (sel, K 2, T 3000, dos veces, salida + camara + siembra): {'OK' if d else 'FALLA'} ({time.time() - t0:.0f}s)")

    log("I4  REGLA 14: la medida del runner == corre_bp.tarea; referencias guardadas reproducidas hoy")
    t0 = time.time()
    ev = R.evoluciona(SEM_I2, 'sel', 2, 3000); sb = ev['siembra']
    x = N(R.prueba(SEM_I2, sb, 3000)); y = N(CB.tarea(SEM_I2, 'bloq2', 3000, siembra=copy.deepcopy(sb)))
    ks = sorted((set(x) | set(y)) - {'seg'}); e = all(x.get(k) == y.get(k) for k in ks); ok &= e
    log(f"  prueba() == corre_bp.tarea(s, 'bloq2', T, siembra) campo a campo ({len(ks)} campos, siembra {len(sb)}): {'OK' if e else 'FALLA ' + str([k for k in ks if x.get(k) != y.get(k)][:5])} ({time.time() - t0:.0f}s)")
    if a.sin_i4:
        log("  (--sin_i4: referencias a T 100 000 NO reproducidas en esta corrida)")
    else:
        for nombre, sbr in (('bloq2', None), ('bloq_pas', 'bloq_c1_p3_s59223.json')):
            t0 = time.time()
            with open(os.path.join(R.REFS, f"{nombre}_s59201.json"), encoding='utf-8') as fh: g = json.load(fh)
            if sbr:
                with open(os.path.join(R.BPD, 'datos', 'pasajes_Tp25000_np4', sbr), encoding='utf-8') as fh: siem = CB.siembra_de(json.load(fh))
                h = N(CB.tarea(59201, 'bloq', 100000, siembra=siem)); h['siembra_n'] = len(siem)
            else:
                h = N(CB.tarea(59201, 'bloq2', 100000))
            h['brazo'] = nombre; h['aborto'] = None
            ks = sorted((set(g) | set(h)) - {'seg'}); dif = [k for k in ks if g.get(k) != h.get(k)]; ok &= not dif
            log(f"  {nombre} s59201 T 100000 reproducido == JSON guardado ({len(ks)} campos, menos 'seg'): {'OK' if not dif else 'FALLA ' + str(dif[:6])} "
                f"({time.time() - t0:.0f}s)")
    log(f"ARNES pista_pob: {'PASA' if ok else 'FALLA'} ({time.time() - t00:.0f}s)")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
