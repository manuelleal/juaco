"""compara_sinlimpia.py — la contradiccion LIMPIA=0: corre CTRL_O1_SINLIMPIA por el camino CANONICO (corre_v143.tarea, fundador limpio 1)
en la MISMA semilla y T del mapa y lo compara CAMPO A CAMPO (salvo el nombre del carro en los ids) con el JSON fijo_LIMPIA0 del mapa.
Ademas recalcula con fila() el crudo viejo de SINLIMPIA (sellada 5001-5020, fundador NO limpio) que dio 0/180. Un proceso, UNA corrida de 100k.
    python experimentos/organelos/muro_perillas/compara_sinlimpia.py [--seed 883001] [--T 100000]
"""
import argparse, glob, json, os, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'tronco_v14_3'), os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')]
import corre_muro_perillas as R
CV = R.CV; J = R.J


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False); ap.add_argument('--seed', type=int, default=883001); ap.add_argument('--T', type=int, default=100000)
    ap.add_argument('--solo_viejo', action='store_true')   # solo el recalculo del crudo viejo (0 CPU)
    a = ap.parse_args()
    if a.solo_viejo: return viejo()
    npy, ntot = R.python_de_trabajo(); print(f"REGLA DE CPU: python.exe ajenos de trabajo {npy} (totales {ntot}) · tope {R.CPU_TOPE}")
    if npy >= R.CPU_TOPE: print("  >= tope: NO SE CORRE."); return 2
    fj = os.path.join(R.DATOS, 'mapa', f"fijo_LIMPIA0_s{a.seed}_T{a.T}.json")
    x = json.load(open(fj, encoding='utf-8')); print(f"mapa LIMPIA=0 s{a.seed}: cruzan {x['cruzan']}/9 R0 {x['R0_med']} fund {x['fund']} B+D {x['mord_BD']} estado {x['estado']}")
    CV._MODS['CTRL_O1_SINLIMPIA'] = CV.P.carga_carro('CTRL_O1_SINLIMPIA')   # corre_v143.modulo solo carga FABRICA y O1 de la carrera; el control se carga por la pista (mismo CV.tarea -> P.run)
    t0 = time.time(); y = CV.tarea((a.seed, 'CTRL_O1_SINLIMPIA', a.T)); y.pop('pizarra_log', None); y.pop('tel', None)
    f = R.fila(dict(y, tel_ps={}, estado={}), a.T)
    print(f"[{time.time()-t0:.0f}s] CANONICO CTRL_O1_SINLIMPIA (corre_v143.tarea, fundador limpio 1) s{a.seed}: cruzan {f['cruzan']}/9 R0 {f['R0_med']} fund {f['fund']} B+D {f['mord_BD']} causas {f['causas']}")
    campos = ('cruzan', 'R0_real', 'fund', 'fund_post10k', 'establecidos', 'muertes', 'vida_med', 'causas', 'mord_BD', 'mord_AC', 'mundo_AC', 'frac_sin_bueno')
    dif = [k for k in campos if json.dumps(x[k], sort_keys=True) != json.dumps(f[k], sort_keys=True)]
    print(f"  campo a campo (fila): {'IGUALES' if not dif else 'DIFIEREN en ' + str(dif)}")
    ruta_crudo = os.path.join(R.DATOS, 'mapa', f"canonico_CTRL_O1_SINLIMPIA_s{a.seed}_T{a.T}.json")
    json.dump(dict(carro='CTRL_O1_SINLIMPIA', seed=a.seed, T=a.T, fila=f, linajes=y['linajes'], pista=y['pista'], iguales=not dif, dif=dif), open(ruta_crudo, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f"  escrito {ruta_crudo}")
    return viejo()


def viejo():
    """El crudo viejo de SINLIMPIA (sellada 5001-5020; fundador NO limpio; anterior a ERR-100: sin R0_real) releido con err99 + fila()."""
    cr = sorted(f for f in glob.glob(os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'datos', 'carrera_rondasellada_sinlimpia_s5001-5020_*.json'))
                if os.path.basename(f).startswith('carrera_') and not f.endswith('_resumen.json'))   # (12:40: el glob tomaba recalculo_err100_*, sin 'corridas')
    d = json.load(open(cr[-1], encoding='utf-8')); T = d['meta']['T']; out = []
    for c in d['corridas']:
        L = []
        for l in c['linajes']:
            te = l['telem']; tf, qf, nr = J.t_fund_reconstruido(te['vidas'], te['desc_por_vida']); l = dict(l)
            l.update(J.err99(l['muertes'], l['fundadores'], tf, l['descendientes'], T, te['vidas'], te['desc_por_vida'], nac_reales=nr, cola_final=l['cola_final'])); l['t_fund_rec_ok'] = True; L.append(l)
        out.append(R.fila(dict(seed=c['seed'], seg=c['seg'], linajes=L, pista=c['pista'], tel_ps={}, estado={}), T))
    print(f"crudo viejo SINLIMPIA (sellada 5001-5020, fundador_limpio {d['meta'].get('fundador_limpio')}) con fila(): cruzan {[q['cruzan'] for q in out]} suma {sum(q['cruzan'] for q in out)}/180 · "
          f"R0 med {st.median(q['R0_med'] for q in out):.3f} · fund med {st.median(q['fund_med'] for q in out)} · B+D {st.median(q['mord_BD'] for q in out)} · establecidos {sum(q['establecidos'] for q in out)}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
