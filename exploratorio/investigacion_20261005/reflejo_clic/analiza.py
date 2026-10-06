"""analiza.py — tablas y veredicto mecanico (PREREGISTRO.md). Pareado por semilla, como mini_llm/analiza.py.
uso: python analiza.py datos/principal.json"""
import json, sys, numpy as np

P1 = ['macro_pos', 'macro_etq', '1nn', '1nn_reciente', 'logistica', 'colonia', 'colonia_barajada', 'colonia_v2']
REG = ['sin_cambio', 'reordenar', 'renombrar', 'distractores', 'cambia_y_vuelve']
PRIM = REG + ['ment_inc']
SUMA = ('pasos', 'abst', 'rev', 'irr_prop', 'irr_mal', 'ok', 'autonoma')


def frac(rs, k='autonoma'): return float(np.mean([r[k] for r in rs]))
def suma(rs): return {k: int(sum(r[k] for r in rs)) for k in SUMA} | {'tareas': len(rs)}
def junta(ds):
    o = {k: sum(d[k] for d in ds) for k in SUMA}; o['tareas'] = sum(d.get('tareas', 0) for d in ds); return o
def pct(a, b): return 100.0 * a / b if b else float('nan')


def pares(todo, a, b, cond):
    d = [frac(r['cond'][cond][a]) - frac(r['cond'][cond][b]) for r in todo]
    return sum(x > 1e-9 for x in d), sum(abs(x) <= 1e-9 for x in d), sum(x < -1e-9 for x in d), d


def nn_abst(r, var, conds, objetivo):
    """elige UN umbral por semilla: el de tasa de abstencion mas cercana a `objetivo` sobre `conds`. Devuelve (indice, tasa)."""
    mejor = None
    for i in range(len(r['taus'])):
        t = junta([r['nn_tau'][c][var][i] for c in conds])
        tasa = t['abst'] / max(t['irr_prop'], 1) if var.endswith('irr') else (t['abst'] + t['rev']) / max(t['pasos'], 1)
        if mejor is None or abs(tasa - objetivo) < abs(mejor[1] - objetivo) - 1e-12: mejor = (i, tasa)
    return mejor


def main(f):
    todo = json.load(open(f)); n = len(todo); out = []; w = out.append
    w(f"# {f} — semillas {[r['seed'] for r in todo]}, {todo[0]['n_prueba']} tareas por familia y regimen, C={todo[0]['C']}")
    ne = [x for r in todo for x in r['n_elementos']]; w(f"elementos por pantalla: {min(ne)}–{max(ne)}")
    # ------------------------------------------------ parte 1
    w("\n## Parte 1 — tareas completas (media de semillas; entre corchetes min–max)")
    w("| regimen | " + ' | '.join(P1) + ' |'); w('|---|' + '---|' * len(P1))
    M = {}
    for c in REG + ['cambia_y_vuelve@0', 'cambia_y_vuelve@2', 'ment_inc', 'ment_con']:
        fila = []
        for b in P1:
            v = [frac(r['cond'][c][b]) for r in todo]; M[(c, b)] = float(np.mean(v)); fila.append(f"{np.mean(v):.3f} [{min(v):.2f}–{max(v):.2f}]")
        w(f"| {c} | " + ' | '.join(fila) + ' |')
    w("\n## Pareado por semilla: colonia frente a cada rival (gana/empata/pierde de %d; diferencia media)" % n)
    w("| regimen | " + ' | '.join(b for b in P1 if b != 'colonia') + ' |'); w('|---|' + '---|' * (len(P1) - 1))
    for c in REG:
        fila = []
        for b in P1:
            if b == 'colonia': continue
            g, e, p, d = pares(todo, 'colonia', b, c); fila.append(f"{g}/{e}/{p} ({np.mean(d):+.3f})")
        w(f"| {c} | " + ' | '.join(fila) + ' |')
    w("\nExploratorio (fuera del veredicto): colonia_v2 − 1nn por regimen: " + '; '.join(
        f"{c} {np.mean(pares(todo, 'colonia_v2', '1nn', c)[3]):+.3f} ({pares(todo, 'colonia_v2', '1nn', c)[0]}/{pares(todo, 'colonia_v2', '1nn', c)[1]}/{pares(todo, 'colonia_v2', '1nn', c)[2]})" for c in REG))
    # ------------------------------------------------ parte 2
    w("\n## Parte 2 — irreversibles (suma de las %d semillas)" % n)
    w("irr errados % = clics irreversibles equivocados ejecutados / propuestas de irreversible. abst % = abstenciones / propuestas de irreversible. "
      "pide % = (abstenciones + reversiones) / pasos. completas = sin ayuda.")
    arms2 = ['colonia', 'colonia_v2', 'cuarentena', 'cuar_sin_efecto', 'cuar_sin_k', '1nn', '1nn_abst_irr', '1nn_abst_todo']
    VAR = {'1nn_abst_irr': 'irr', '1nn_abst_todo': 'todo', '1nn_rec_abst_irr': 'rec_irr'}; D1 = 'rec_irr' in todo[0]['nn_tau']['sin_cambio']
    if D1: arms2 += ['1nn_reciente', '1nn_rec_abst_irr']
    def celdas(c_list, calib=PRIM):
        """por brazo: totales sumados sobre semillas y por semilla, con el umbral del 1-NN calibrado por semilla sobre PRIM."""
        tot = {a: [] for a in arms2}
        for r in todo:
            q = junta([suma(r['cond'][c]['cuarentena']) for c in calib])
            obj = dict(irr=q['abst'] / max(q['irr_prop'], 1), todo=(q['abst'] + q['rev']) / max(q['pasos'], 1))
            for a in arms2:
                if a in VAR:
                    var = VAR[a]; i, _ = nn_abst(r, var, calib, obj['irr' if var.endswith('irr') else 'todo'])
                    t = junta([r['nn_tau'][c][var][i] for c in c_list]); t['tareas'] = sum(len(r['cond'][c]['1nn']) for c in c_list)
                else: t = junta([suma(r['cond'][c][a]) for c in c_list])
                tot[a].append(t)
        return tot
    def fila(nombre, tot):
        w(f"\n**{nombre}**\n\n| brazo | irr errados % | errados / propuestas | por 100 tareas | semillas con 0 errados | abst % | pide % | completas | completas o con ayuda |\n|---|---|---|---|---|---|---|---|---|")
        res = {}
        for a in arms2:
            t = junta(tot[a]); res[a] = t
            w(f"| {a} | {pct(t['irr_mal'], t['irr_prop']):.2f} | {t['irr_mal']} / {t['irr_prop']} | {pct(t['irr_mal'], t['tareas']):.2f} | "
              f"{sum(x['irr_mal'] == 0 for x in tot[a])}/{n} | {pct(t['abst'], t['irr_prop']):.1f} | {pct(t['abst'] + t['rev'], t['pasos']):.1f} | "
              f"{t['autonoma'] / t['tareas']:.3f} | {t['ok'] / t['tareas']:.3f} |")
        return res
    prim = celdas(PRIM); Rp = fila("Conjunto primario (5 regimenes honestos + mentiroso inconsistente)", prim)
    hon = celdas(REG); Rh = fila("Solo regimenes honestos (para el costo)", hon)
    for c in PRIM + ['ment_con']: fila(c, celdas([c]))
    Rc = {a: junta(v) for a, v in celdas(['ment_con']).items()}
    DESP = ['reordenar', 'renombrar', 'distractores']
    Rd = fila('POST HOC (D1): solo desplazamiento (reordenar + renombrar + distractores), umbral del 1-NN calibrado ahi mismo', celdas(DESP, DESP))
    Rs = fila('POST HOC (D1): primario SIN mentiroso inconsistente, umbral calibrado ahi mismo', celdas(REG, REG))
    # ------------------------------------------------ costo de computo y colonia
    w("\n## Microsegundos por clic (decision; media de semillas) y memoria al final de la fase A")
    w("| brazo | us/clic | memoria |\n|---|---|---|")
    for b in P1 + ['cuarentena']:
        us = np.mean([np.mean([r['brazos'][k][b]['us_clic'] for k in r['brazos']]) for r in todo]); mem = np.mean([r['brazos']['honesto_A'][b]['memoria'] for r in todo])
        w(f"| {b} | {us:.0f} | {mem:.0f} |")
    for k in ('honesto_A', 'honesto_fin', 'ment_inc', 'ment_con'):
        for b in ('colonia', 'colonia_barajada', 'cuarentena'):
            d = [r['brazos'][k][b] for r in todo]
            w(f"- {k} {b}: " + ', '.join(f"{q} {np.mean([x[q] for x in d]):.1f}" for q in d[0] if q not in ('us_clic', 'n_dec', 'memoria')))
    # ------------------------------------------------ predicciones y criterio de cierre
    w("\n## Predicciones"); si = lambda x: 'CUMPLIDA' if x else 'REFUTADA'
    w(f"- P1 reordenar: colonia {M[('reordenar','colonia')]:.3f} (≥0.80), macro_pos {M[('reordenar','macro_pos')]:.3f} (≤0.30): {si(M[('reordenar','colonia')] >= 0.8 and M[('reordenar','macro_pos')] <= 0.3)}")
    w(f"- P2 distractores: colonia {M[('distractores','colonia')]:.3f} (≥0.80), macro_pos {M[('distractores','macro_pos')]:.3f} (≤0.30): {si(M[('distractores','colonia')] >= 0.8 and M[('distractores','macro_pos')] <= 0.3)}")
    w(f"- P3 renombrar: colonia {M[('renombrar','colonia')]:.3f} (≥0.60), macro_etq {M[('renombrar','macro_etq')]:.3f} (≤0.20): {si(M[('renombrar','colonia')] >= 0.6 and M[('renombrar','macro_etq')] <= 0.2)}")
    w(f"- P4 macro_etq en reordenar {M[('reordenar','macro_etq')]:.3f} (≥0.95): {si(M[('reordenar','macro_etq')] >= 0.95)}")
    g, e, p, d = pares(todo, 'colonia', '1nn', 'cambia_y_vuelve'); p5 = sum(x >= 0.15 for x in d) >= 4
    w(f"- P5 cambia_y_vuelve: colonia − 1nn por semilla {[round(x, 3) for x in d]}; ≥0.15 en {sum(x >= 0.15 for x in d)}/{n}: {si(p5)}")
    q, c0 = Rp['cuarentena'], Rp['colonia']; e_q, e_c = pct(q['irr_mal'], q['irr_prop']), pct(c0['irr_mal'], c0['irr_prop'])
    w(f"- P6 irreversibles errados: cuarentena {e_q:.2f} % (≤1), colonia sin cuarentena {e_c:.2f} % (≥8): {si(e_q <= 1 and e_c >= 8)} (cuarentena ≤1: {si(e_q <= 1)}; colonia ≥8: {si(e_c >= 8)})")
    costo = 100 * (Rh['colonia']['autonoma'] - Rh['cuarentena']['autonoma']) / Rh['colonia']['tareas']
    w(f"- P7 costo: {costo:.1f} puntos (≤15): {si(costo <= 15)}")
    w(f"  - exploratorio: costo frente a colonia_v2 (misma riqueza de celulas): {100 * (Rh['colonia_v2']['autonoma'] - Rh['cuarentena']['autonoma']) / Rh['colonia']['tareas']:.1f} puntos")
    e_mc = pct(Rc['cuarentena']['irr_mal'], Rc['cuarentena']['irr_prop'])
    w(f"- P8 mentiroso consistente atraviesa: cuarentena {e_mc:.1f} % errados (≥50): {si(e_mc >= 50)}")
    cb = [np.mean([frac(r['cond'][c]['colonia']) for c in REG]) - np.mean([frac(r['cond'][c]['colonia_barajada']) for c in REG]) for r in todo]
    w(f"- Control barajada: colonia − barajada por semilla {[round(float(x), 3) for x in cb]}; por delante en {sum(x > 1e-9 for x in cb)}/{n}: {si(sum(x > 1e-9 for x in cb) >= 4)}")
    w("\n## Criterio de cierre")
    g, e, p, d = pares(todo, 'colonia', '1nn', 'renombrar'); gana_ren = np.mean(d) >= 0.05 and g >= 4
    w(f"- renombrar: colonia − 1nn {np.mean(d):+.3f}, por delante en {g}/{n} → {'GANA la colonia' if gana_ren else 'el 1-NN empata o gana'}")
    w(f"- cambia_y_vuelve: P5 → {'GANA la colonia' if p5 else 'el 1-NN empata o gana'}")
    g2, e2, p2, d2 = pares(todo, 'colonia', '1nn_reciente', 'cambia_y_vuelve'); emp_rec = not (np.mean(d2) >= 0.05 and g2 >= 4)
    w(f"  - candado: colonia − 1nn_reciente {np.mean(d2):+.3f}, por delante en {g2}/{n} → {'1nn_reciente EMPATA o gana' if emp_rec else 'la colonia tambien le gana'}")
    mejor = min(pct(Rp[a]['irr_mal'], Rp[a]['irr_prop']) for a in ('1nn_abst_irr', '1nn_abst_todo')); gana_irr = (mejor - e_q) >= 1.0
    w(f"- irreversibles: cuarentena {e_q:.2f} % frente al mejor 1nn_abst {mejor:.2f} % → {'GANA la cuarentena' if gana_irr else 'el 1-NN con abstencion empata o gana'}")
    if D1:
        for nom, R_ in (('primario', Rp), ('primario sin mentiroso', Rs), ('solo desplazamiento', Rd)):
            x = R_['1nn_rec_abst_irr']; y = R_['cuarentena']
            w(f"  - candado D1 ({nom}): cuarentena {pct(y['irr_mal'], y['irr_prop']):.2f} % ({y['irr_mal']}/{y['irr_prop']}, completas {y['autonoma'] / y['tareas']:.3f}) frente a 1nn_rec_abst_irr {pct(x['irr_mal'], x['irr_prop']):.2f} % ({x['irr_mal']}/{x['irr_prop']}, completas {x['autonoma'] / x['tareas']:.3f})")
    k = int(gana_ren) + int(p5) + int(gana_irr)
    if k == 0: v = 'NO (la linea se CIERRA)'
    elif k == 3 and M[('reordenar', 'colonia')] >= 0.8 and M[('distractores', 'colonia')] >= 0.8 and M[('renombrar', 'colonia')] >= 0.6 and e_q <= 1 and e_c >= 8: v = 'FUNCIONA'
    else: v = 'HAY ALGO MODESTO'
    if k == 1 and p5 and emp_rec: v += ' (candado: la unica victoria es contra un 1-NN sin desempate)'
    w(f"\n**VEREDICTO MECANICO: {v}** (victorias de la colonia: {k}/3)")
    txt = '\n'.join(out); print(txt); open(f.replace('.json', '.md'), 'w', encoding='utf-8').write(txt)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8'); main(sys.argv[1] if len(sys.argv) > 1 else 'datos/principal.json')
