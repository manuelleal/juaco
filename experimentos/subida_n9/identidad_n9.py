"""identidad_n9.py — ARNES DE IDENTIDAD del bloque "el modelo de si es causal" (subida del nivel 9). Un proceso, sin Pool.

MISION: llegar a la AGI por este camino.

Comprueba, ANTES de mirar ningun numero:
  (0) shas de los originales leidos (pista, juez, revisa_carro, O3, organismo_f9c) y que los carros en disco son
      exactamente lo que construye_n9.py produce (construccion por anclas reproducible).
  (E) chequeo estatico de la carrera (revisa_carro, ERR-96) de los cinco carros: PASA.
  (F) identidad corta del juez: FABRICA solo == organismo_f9c REL bit a bit (s=1, T=5000).
  (I) O3_LES_OFF (instrumento con las dos perillas en False) == O3 BIT A BIT en TODA la salida de pista.run (fisica +
      telemetria del carro + rng), monocultivo de 9, fundador limpio (ENMIENDA 5), en semillas del arnes 13392-13394,
      y en una pista MIXTA (4 O3 + 5 O3_LES_OFF) == 9 O3. Se exige ademas que TERMINAL se haya disparado en el arnes
      (cuerpos_term > 0) para que el camino de la muerte declarada quede cubierto.
  (C) CTRL_O3_SINTERM de esta carpeta == el de experimentos/generaciones (mismo sha) [en (0)].
  (N) NO inerte: O3_LES_SI, O3_TERM_CIEGO y O3_LES_COLA difieren de O3 en la fisica (si no, la lesion no lesiona nada).
  (M) marginal: con la lesion, la media del estado usado se parece a la del estado real (|diferencia| <= 0.05 en E y Ag;
      <= 0.5 en cola_est) y, en L-COLA, los pasos en TERMINAL con la cola usada / con la verdadera quedan en [0.8, 1.25]
      (misma TASA de muerte programada, otro MOMENTO: el control de ERR-102/103). Es una lesion de MOMENTO, no de nivel.
      Primera version (historia desde el nacimiento del cuerpo) FALLO este chequeo (E 0.91/1.01; cola 1.44/2.72; TERMINAL
      5516/27006): se cambio a la ventana de los ultimos 2000 pasos del linaje ANTES de cualquier humo. Con la ventana, L-SI
      pasa y L-COLA sigue fallando (TERMINAL 0.33 de la tasa real: sorteada paso a paso la muerte programada parpadea):
      L-COLA queda DESCARTADA como brazo (se reporta, no cuenta en N/N) y la reserva se lesiona con O3_TERM_CIEGO.
Semillas del arnes: 13392-13394 (nuevas; no se usan en la serie 13301-13340 ni en el humo 13391).
Uso: python experimentos/subida_n9/identidad_n9.py   (escribe identidad_n9_salida.txt al lado)
"""
import os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import comun_n9 as K   # noqa: E402

T_ARNES = 12000
SEM_ARNES = (13392, 13393, 13394)


def main():
    t0 = time.time(); ok = []; lineas = []

    def log(s=''):
        print(s, flush=True); lineas.append(s)

    def chk(nombre, cond, det=''):
        ok.append(bool(cond)); log(f"  [{'OK' if cond else 'FALLA'}] {nombre}{(' · ' + det) if det else ''}")

    log(f"ARNES identidad_n9 · {time.strftime('%Y-%m-%d %H:%M:%S')} · T={T_ARNES} · semillas {SEM_ARNES}")
    log("(0) shas y construccion")
    for r, m, s, b in K.verifica_shas(): chk(f"sha {r}", b, f"{m} (fijado {s})")
    esp, med, b = K.verifica_construccion()
    chk("carros en disco == construye_n9.py", b, str(med))
    log("(E) chequeo estatico (revisa_carro)")
    for n in K.BRAZOS + K.ARNES:
        v = K.RC.revisa(n); chk(f"revisa {n}", not v, 'PASA' if not v else str(v[:3]))
    log("(F) identidad corta del juez")
    ide = K.J.identidad_corta(); chk("FABRICA solo == organismo_f9c REL (s=1, T=5000)", ide['ok'], f"sha f9c {ide['sha_f9c']} dif {ide['dif'][:3]}")
    log("(I) O3_LES_OFF == O3 bit a bit (salida completa de pista.run, fundador limpio)")
    ref = {}; term = 0
    for s in SEM_ARNES:
        a = K.P.run(s, ['O3'] * 9, T=T_ARNES, pizarra=1, fundador_limpio=1); ref[s] = a
        b = K.P.run(s, ['O3_LES_OFF'] * 9, T=T_ARNES, pizarra=1, fundador_limpio=1)
        term += sum(int((l.get('carro') or {}).get('cuerpos_term', 0)) for l in a['linajes'])
        chk(f"mono s{s}", K.normaliza(a) == K.normaliza(b, 'O3_LES_OFF'),
            f"muertes {sum(l['deaths'] for l in a['linajes'])} nac {sum(sum(l['origen_cuerpo']) for l in a['linajes'])}")
    s = SEM_ARNES[0]
    m = K.P.run(s, ['O3'] * 4 + ['O3_LES_OFF'] * 5, T=T_ARNES, pizarra=1, fundador_limpio=1)
    chk(f"mixta 4 O3 + 5 O3_LES_OFF == 9 O3 (s{s})", K.normaliza(ref[s]) == K.normaliza(m, 'O3_LES_OFF'))
    chk("TERMINAL se disparo en el arnes (camino de muerte declarada cubierto)", term > 0, f"cuerpos_term (ultima instancia) {term}")
    log("(N) no inerte y (M) marginal")
    c = K.P.run(s, ['O3_TERM_CIEGO'] * 9, T=T_ARNES, pizarra=1, fundador_limpio=1)
    fis0 = lambda x, e: K.normaliza([{k: v for k, v in l.items() if k != 'carro'} for l in x['linajes']], e)
    chk(f"O3_TERM_CIEGO difiere de O3 en la fisica (s{s})", fis0(c, 'O3_TERM_CIEGO') != fis0(ref[s], None),
        f"muertes {sum(l['deaths'] for l in c['linajes'])} vs {sum(l['deaths'] for l in ref[s]['linajes'])} · cuerpos_term (ultima instancia) "
        f"{sum(int((l.get('carro') or {}).get('cuerpos_term', 0)) for l in c['linajes'])}")
    for n in ('O3_LES_SI', 'O3_LES_COLA'):
        c = K.P.run(s, [n] * 9, T=T_ARNES, pizarra=1, fundador_limpio=1)
        fis = lambda x: K.normaliza([{k: v for k, v in l.items() if k != 'carro'} for l in x['linajes']], n)
        chk(f"{n} difiere de O3 en la fisica (s{s})", fis(c) != fis(ref[s]),
            f"muertes {sum(l['deaths'] for l in c['linajes'])} vs {sum(l['deaths'] for l in ref[s]['linajes'])}")
        les = [(l.get('carro') or {}).get('lesion') for l in c['linajes']]; les = [x for x in les if x and x['n']]
        nn = sum(x['n'] for x in les)
        mr = [sum(x['lev_real'][j] for x in les) / nn for j in (0, 1)]; mu = [sum(x['lev_usado'][j] for x in les) / nn for j in (0, 1)]
        cr = sum(x['cola_real'] for x in les) / nn; cu = sum(x['cola_usada'] for x in les) / nn
        dl = sum(x['dlev'] for x in les) / nn; dc = sum(x['dcola'] for x in les) / nn
        ct = sum(x['cambia_term'] for x in les); tr = sum(x['term_real'] for x in les); tu = sum(x['term_usado'] for x in les)
        rt = (tu / tr) if tr else None
        okm = abs(mr[0] - mu[0]) <= 0.05 and abs(mr[1] - mu[1]) <= 0.05 and abs(cr - cu) <= 0.5
        det = (f"E {mr[0]:.3f}/{mu[0]:.3f} Ag {mr[1]:.3f}/{mu[1]:.3f} cola {cr:.2f}/{cu:.2f} · |dlev| medio {dl:.3f} · |dcola| medio {dc:.2f}"
               f" · TERMINAL real/usado/cambiado {tr}/{tu}/{ct} (pasos, ultima instancia; usado/real {rt if rt is None else round(rt, 3)}) · pasos {nn}")
        if n == 'O3_LES_COLA':   # DESCARTADA: se reporta, no cuenta en N/N (no corre en la serie)
            okm = okm and rt is not None and 0.8 <= rt <= 1.25
            log(f"  [{'pasaria' if okm else 'DESCARTADA'} -- no cuenta] {n} marginal (TERMINAL usado/real en [0.8, 1.25]) · {det}")
        else:
            chk(f"{n} marginal (media usada ~ real)", okm, det)
    n_ok = sum(ok)
    log(f"RESULTADO: {n_ok}/{len(ok)} · {time.time() - t0:.1f}s")
    open(os.path.join(AQUI, 'identidad_n9_salida.txt'), 'w', encoding='utf-8').write('\n'.join(lineas) + '\n')
    return 0 if n_ok == len(ok) else 1


if __name__ == '__main__':
    sys.exit(main())
