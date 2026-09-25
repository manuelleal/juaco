"""identidad_ohno.py — ARNES de OHNO SOBRE BASE VIVA. Un proceso (los dos subprocesos de (O2) corren uno tras otro), sin Pool. Opus A, 24-sep-2026.

MISION: llegar a la AGI por este camino.

  (C)  construye_ohno.py --verifica: motor, carro, gramatica_def y conducta son copias BYTE A BYTE de gramatica/ (sha fijado).
  (O1) con la mutacion de la gramatica APAGADA, VIDA == FIJO:filtra0 bit a bit (todo el JSON salvo brazo y segundos), en el mundo de OHNO.
  (O2) con los fundadores AL AZAR (GRAM_VIDA) y el quimiostato de ECO (0.03), corre_ohno == corre_gramatica (brazo VIDA) en toda la fisica
       y en la gramatica (banco real y sombras, corte, entregas, errores). Cada runner en su propio subproceso.
  (W)  el quimiostato de OHNO llega al motor (r_paso = R_REP * 30) y cambia la trayectoria respecto de 0.03.
  (O1b/O1c) (O1) pasado el corte en el mundo pobre y con el quimiostato de ECO (ERR-126: la 1a corrida no tenia partos).
  (D1)-(D3) en el quimiostato de ECO (0.03): mismo codigo, muchos partos.
  (D1) PIEZA DUPLICACION: una copia IDENTICA de filtra0 (origen 1) es fisicamente neutra: [filtra0 + filtra0*] == [filtra0] en la fisica.
  (D2) PIEZA DIVERGENCIA: si la copia deriva (nacer/sin0/VECINO/copiar*), la trayectoria cambia, el motor entrega al vecino, y la
       conducta del ORIGINAL sigue igual (las celdas nacer/hijo de conducta.py son las de filtra0): la copia deriva y el original trabaja.
  (D3) en VIDA con duplicacion alta (p_dup 0.3, T 10 000) el banco trae genomas con un slot de origen 1 que YA DIVERGIO de filtra0 y el
       slot original (origen 0) intacto: la maquinaria de Ohno ocurre en el mundo.
  (N9) nube-9: la guardia de ERR-60 dentro de trabajo() queda en el JSON ('abortado') y no lanza.
  (V)  la letra en entradas sinteticas (FUNCIONA-Ohno, MODESTO, NO, techo, inviable).
  (R)  banderas malas abortan con codigo 2.
Escribe identidad_ohno_salida.txt.
"""
import json, os, subprocess, sys, tempfile, time
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
GRAMD = os.path.join(os.path.dirname(AQUI), 'gramatica')
sys.path.insert(0, AQUI)
R_ = []; OUT = []
SEM = 25002; T_ = 10000; TC = 8000
FIS = ('persiste', 'vivos_T', 't_ext', 'n_nac', 'n_refund', 'n_banco', 'nac_post', 'r0_post', 'n_coh_post', 'tam_total', 'max_vivos', 'bloqueados')
GRAMK = FIS + ('g_nmut', 'entregas', 'final_banco_gr', 'final_banco_gs', 'max_nac_linaje')


def pr(s):
    print(s, flush=True); OUT.append(s)


def chk(nombre, ok, det=''):
    R_.append(bool(ok)); pr(f"  {'OK ' if ok else 'MAL'} {nombre} {det}")


J = lambda x: json.dumps(x, sort_keys=True, default=str)


def main():
    import corre_ohno as CO, gramatica_def as GD, conducta as C, motor_gramatica as MG
    t00 = time.time()
    pr(f"IDENTIDAD OHNO · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {sys.version.split()[0]} · numpy {np.__version__} · R_REP {CO.R_REP} · shas {CO.SHAS()}")
    v = subprocess.run([sys.executable, os.path.join(AQUI, 'construye_ohno.py'), '--verifica'], capture_output=True, text=True)
    chk("(C) construye_ohno --verifica (copias byte a byte)", v.returncode == 0 and 'OK' in v.stdout, v.stdout.strip())
    tmp = tempfile.mkdtemp()
    tr = lambda b, rr=CO.R_REP, T=T_, tc=TC, s=SEM: CO.trabajo((s, b, T, tc, 2000, rr, tmp, False))
    # (O1)
    a = tr('VIDA_SINMUT'); b = tr('FIJO:filtra0')
    d = [k for k in a if k not in ('brazo', 'seg') and J(a[k]) != J(b.get(k))]
    chk("(O1) mutacion de la gramatica apagada: VIDA == FIJO:filtra0 bit a bit", not d,
        f"(distintas {d}; nacidos {a['n_nac']}, max vivos {a['max_vivos']}, r_paso {a['r_paso']}, {a['seg']}+{b['seg']} s)")
    FJ = b
    # ERR-126 (candidato, 24-sep 20:35): la 1a corrida del arnes dio 8/10: en el mundo pobre, a T 10 000 hay ~3 nacimientos y (D2)/(D3) no
    # ejercitaban nada (ERR-120 otra vez). Las piezas pasan al mundo de ECO (0.03, mismo codigo, muchos partos) y (O1) se repite PASADO el
    # corte en el mundo pobre, donde si hay partos.
    a = tr('VIDA_SINMUT', T=46000, tc=40000); b = tr('FIJO:filtra0', T=46000, tc=40000)
    d = [k for k in a if k not in ('brazo', 'seg') and J(a[k]) != J(b.get(k))]
    # ERR-126 (2a parte, 20:44): el umbral '> 20 partos' era a ojo; la 2a corrida dio igualdad bit a bit con 9 partos tras el corte (el cuello
    # de botella). Se baja a >= 5 (que haya partos que comparar) y se declara; (O1c) cubre el caso con muchos partos.
    chk("(O1b) idem en el mundo pobre PASADO el corte (T 46 000, corte 40 000), con partos", not d and a['nac_post'] >= 5,
        f"(distintas {d}; nacidos tras el corte {a['nac_post']}; {a['seg']}+{b['seg']} s)")
    a = tr('VIDA_SINMUT', rr=0.03); b = tr('FIJO:filtra0', rr=0.03)
    d = [k for k in a if k not in ('brazo', 'seg') and J(a[k]) != J(b.get(k))]
    chk("(O1c) idem con el quimiostato de ECO (0.03, muchos partos)", not d and a['n_nac'] > 100, f"(distintas {d}; nacidos {a['n_nac']})")
    # (O2) fundadores al azar == corre_gramatica (subprocesos)
    t1 = tempfile.mkdtemp(); t2 = tempfile.mkdtemp()
    cod = ("import sys, json; sys.path.insert(0, r'{d}'); import {m} as X; x = X.trabajo({args}); "
           "json.dump(x, open(r'{o}', 'w'))")
    og = os.path.join(t1, 'g.json'); oo = os.path.join(t2, 'o.json')
    subprocess.run([sys.executable, '-c', cod.format(d=GRAMD, m='corre_gramatica', args=f"({SEM}, 'VIDA', {T_}, {TC}, 2000, r'{t1}', False)", o=og)], check=True)
    subprocess.run([sys.executable, '-c', cod.format(d=AQUI, m='corre_ohno', args=f"({SEM}, 'GRAM_VIDA', {T_}, {TC}, 2000, 0.03, r'{t2}', False)", o=oo)], check=True)
    g = json.load(open(og)); o = json.load(open(oo))
    d = [k for k in GRAMK if J(g.get(k)) != J(o.get(k))] + ([] if J((g.get('corte_gr') or {}).get('banco_gr')) == J((o.get('corte_gr') or {}).get('banco_gr')) else ['corte_gr'])
    chk("(O2) fundadores al azar y quimiostato 0.03: corre_ohno == corre_gramatica (fisica + gramatica, subprocesos)", not d and o['g_nmut'] > 0,
        f"(distintas {d}; errores de copia {o['g_nmut']}; entregas {sum(o['entregas'].values())})")
    # (W)
    w = tr('FIJO:filtra0', rr=0.03)
    chk("(W) el quimiostato de OHNO llega al motor y cambia la trayectoria", abs(FJ['r_paso'] - CO.R_REP * 30) < 1e-12 and J(w['tam_total']) != J(FJ['tam_total']),
        f"(r_paso {FJ['r_paso']} contra {w['r_paso']}; max vivos {FJ['max_vivos']} contra {w['max_vivos']})")
    # (D1)
    d1 = tr('FIJO:1.3.0.0+1.3.0.0*', rr=0.03); d = [k for k in FIS if J(d1[k]) != J(w[k])]
    chk("(D1) duplicado IDENTICO de filtra0 es fisicamente neutro ([filtra0 + filtra0*] == [filtra0]; quimiostato 0.03)", not d and w['n_nac'] > 100 and d1['final_banco_gr'][0] == [[1, 3, 0, 0, 0], [1, 3, 0, 0, 1]],
        f"(distintas {d}; telemetria n10.dado cuenta los dos paquetes: {[(x or {}).get('dado', [])[:2] for x in d1['carro_n10']][:2]})")
    # (D2)
    d2 = tr('FIJO:1.3.0.0+1.3.2.0*', rr=0.03); d = [k for k in FIS if J(d2[k]) != J(w[k])]
    fo = C.firma(((1, 3, 0, 0, 0), (1, 3, 2, 0, 1))); ff = C.firma(GD.FILTRA0)
    hijo_igual = all(np.allclose(fo[k], ff[k]) for k in ff) and set(k for k in fo if k[1] == 'hijo') == set(ff)
    vec = sum(v_ for k_, v_ in d2['entregas'].items() if k_.startswith('nacer/vecino'))
    chk("(D2) la copia DIVERGE (vecino): la trayectoria cambia, el motor entrega al vecino y la conducta del original (nacer/hijo) sigue igual",
        bool(d) and vec > 0 and hijo_igual, f"(fisica distinta en {d[:4]}; entregas al vecino {vec}; celdas nacer/hijo == filtra0: {hijo_igual})")
    # (D3)
    ev = CO.eco_de('VIDA', SEM, TC); ev['g_pdup'] = 0.3
    r = MG.run_solapadas(SEM, [CO.CARRO] * 30, T=T_, diag=0, mundo_n=30, tope_cuerpos=3000, muestra=1000, r_rep=0.03, eco=ev)
    ban = r['gram']['banco_final_gr']
    div = [gg for gg in ban if any(s[4] == 1 and s[:4] != (1, 3, 0, 0) for s in gg) and any(s[4] == 0 and s[:4] == (1, 3, 0, 0) for s in gg)]
    chk("(D3) VIDA con duplicacion alta (quimiostato 0.03): hay genomas con la copia (origen 1) ya divergida y el original filtra0 intacto", len(div) > 0,
        f"({len(div)}/{len(ban)} del banco; ejemplo {GD.texto(div[0]) if div else None}; slots en el banco {sorted(set(len(x) for x in ban))})")
    # (N9)
    orig = MG.run_solapadas

    def falla(*a_, **k_): raise SystemExit('PISTA2: mas de 100000 cuerpos en un linaje: la semilla colisionaria (ERR-60)')
    CO.MG.run_solapadas = falla
    try:
        x = tr('VIDA', s=SEM + 1); ok9 = True
    except BaseException: ok9 = False; x = {}
    finally: CO.MG.run_solapadas = orig
    chk("(N9) nube-9: la guardia de ERR-60 queda en el JSON ('abortado') y no lanza", ok9 and 'ERR-60' in (x.get('abortado') or '')
        and os.path.exists(os.path.join(tmp, f"VIDA_s{SEM + 1}.json")), f"({x.get('abortado')})")

    # (V) la letra
    def sint(r0V, persV, gV, r0F=0.7, persF=12, r0A=0.3):
        R = []
        for s_ in range(20):
            for b_, r0_, p_, g_ in (('VIDA', r0V, persV, gV), ('FIJO:filtra0', r0F, persF, GD.FILTRA0), ('AZAR', r0A, 5, GD.FILTRA0)):
                R.append(dict(seed=s_, brazo=b_, abortado=None, persiste=int(s_ < p_), bloqueados=0, r0_post=r0_,
                              final_banco_gr=[[list(z) for z in g_]] * 5, final_banco_gs=[[[list(z) for z in GD.FILTRA0]] * 8] * 5))
        return R
    nuevo = ((1, 3, 0, 0, 0), (2, 1, 2, 0, 1))
    v1 = CO.veredicto(sint(0.8, 20, nuevo))[0]; v2 = CO.veredicto(sint(0.8, 20, GD.FILTRA0))[0]; v3 = CO.veredicto(sint(0.5, 10, GD.FILTRA0))[0]
    v4 = CO.veredicto(sint(0.8, 20, nuevo, r0F=0.95, persF=20))[0]; v5 = CO.veredicto(sint(0.8, 20, nuevo, persF=1))[0]
    chk("(V) la letra: Ohno -> FUNCIONA; gana sin organo nuevo -> MODESTO; pierde -> NO; techo y mundo inviable -> NO EVALUABLE",
        'Ohno' in v1 and v2.startswith('HAY ALGO MODESTO') and v3 == 'NO' and 'TECHO' in v4 and 'INVIABLE' in v5, f"({v1[:30]} | {v2[:16]} | {v3} | {v4[:25]} | {v5[:25]})")
    rr = [subprocess.run([sys.executable, os.path.join(AQUI, 'corre_ohno.py')] + z, capture_output=True, text=True).returncode
          for z in (['--humo', '--pool', '2'], ['--serie', '--ventana', 'x', '--pool', '3'], ['--calibra', '--rrep', '0.02'], ['--hum'], ['--humo=1'], ['--prueba_pool', '--pool', '3'])]
    chk("(R) banderas malas abortan con codigo 2", rr == [2] * 6, f"({rr})")
    pr(f"RESULTADO: {sum(R_)}/{len(R_)} · {round(time.time() - t00)} s")


if __name__ == '__main__':
    try:
        main()
    finally:
        with open(os.path.join(AQUI, 'identidad_ohno_salida.txt'), 'w', encoding='utf-8') as f: f.write('\n'.join(OUT) + '\n')
