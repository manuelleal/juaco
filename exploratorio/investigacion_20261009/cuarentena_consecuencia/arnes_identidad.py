# -*- coding: utf-8 -*-
"""ARNÉS DE IDENTIDAD (antes de mirar números). Sin modelo, un proceso, segundos.
  python -B arnes_identidad.py [semillas]      por defecto 0,1,2,3,4 (calibración)
Comprueba, con la línea de tiempo intercalada (4 rondas) y la extracción regalada:
 (0) las copias por ancla son bit a bit iguales al origen (sha256);
 (1) q con las perillas APAGADAS (probación 1.0, sin oráculo, sin muerte) == c (Colonia k=2 de v1): mismo estado,
     mismas células con voz y sin voz en CADA consulta de CADA ronda;
 (2) bv2+LN y bv2+LN+V sin revelaciones == bv2 (MemoriaVoto(minimo=2) de v1): misma tripleta en cada consulta;
 (3) el oráculo es el mismo dado para todos: depende sólo de (semilla, ronda, hecho);
 (4) instrumento (no es resultado): fusión de células (falsas confirmaciones / partidas) y compuerta
     (cada pregunta recupera sólo frases de SU hecho; margen ajena / propia). Si la compuerta trae frases ajenas,
     el oráculo culparía a un inocente: debe dar 0.
NO imprime ninguna medida de resultado (envenenadas, aciertos)."""
import sys

import time

import construye_copia
import mundo_q
from colonia import Colonia, MemoriaVoto, parecido_pregunta, UMBRAL_Q
from memorias_q import ColoniaQ, MemoriaVotoLN

# (5) la memoización de rapido.py no cambia nada: ronda 1 de la semilla 0, sin y con
def _huella():
    m = mundo_q.construye(0, "A")
    c, bv = Colonia(k=2), MemoriaVoto(minimo=2)
    for e in [x for x in m["eventos"] if x["ronda"] == 1]:
        for M in (c, bv):
            M.ensena(e["fuente"], e["frase"], e["valor"], mundo_q.CLAVE[m["hechos"][e["hecho"]]["tipo"]])
    out = []
    for hid in m["orden"][1]:
        q = m["hechos"][hid]["pregunta"]
        a = c.consulta(q)
        out.append((a[0], [x.id for x in a[1]], [x.id for x in a[2]], a[3], repr(bv.consulta(q))))
    return out


t0 = time.time()
h_lento = _huella()
t1 = time.time()
import rapido  # noqa: E402,F401
h_rapido = _huella()
print(f"MEMOIZACIÓN rapido.py: {len(h_lento)} consultas, idénticas sin/con: {h_lento == h_rapido} "
      f"({t1 - t0:.1f} s sin, {time.time() - t1:.1f} s con)")
sems = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [0, 1, 2, 3, 4]
mal = construye_copia.main() | (h_lento != h_rapido)
total = {"q_vs_c": [0, 0], "ln_vs_bv2": [0, 0], "lnv_vs_bv2": [0, 0]}
for s in sems:
    m = mundo_q.construye(s, "A")
    H = m["hechos"]
    c, qa = Colonia(k=2), ColoniaQ(probacion=1.0, T=10 ** 9)
    bv, ln, lnv = MemoriaVoto(minimo=2), MemoriaVotoLN(minimo=2), MemoriaVotoLN(minimo=2, guarda_verificado=True)
    hecho_de = {e["frase"]: e["hecho"] for e in m["eventos"]}
    ajenas = 0
    max_ajena, min_propia = 0.0, 9.0
    for ronda in range(1, mundo_q.RONDAS + 1):
        for e in [x for x in m["eventos"] if x["ronda"] == ronda]:
            v, at = e["valor"], mundo_q.CLAVE[H[e["hecho"]]["tipo"]]
            for M in (c, qa, bv, ln, lnv):
                M.ensena(e["fuente"], e["frase"], v, at)
        for hid in m["orden"][ronda]:
            q = H[hid]["pregunta"]
            a, b = c.consulta(q), qa.consulta(q)
            igual = (a[0] == b[0] and [x.id for x in a[1]] == [x.id for x in b[1]]
                     and [x.id for x in a[2]] == [x.id for x in b[2]] and a[3] == b[3])
            total["q_vs_c"][0] += igual
            total["q_vs_c"][1] += 1
            t0 = bv.consulta(q)
            for nombre, M in (("ln_vs_bv2", ln), ("lnv_vs_bv2", lnv)):
                total[nombre][0] += (M.consulta(q) == t0)
                total[nombre][1] += 1
            for _, cc in c.candidatas(q):
                ajenas += any(hecho_de[f] != hid for _, f in cc.frases)
            for e in m["eventos"]:
                if e["ronda"] <= ronda:
                    p = parecido_pregunta(c.idx, q, e["frase"])
                    if e["hecho"] == hid:
                        min_propia = min(min_propia, p)
                    else:
                        max_ajena = max(max_ajena, p)
        qa.fin_ronda(ronda)
    de, afirm = {}, {}
    par = {e["frase"]: (e["hecho"], e["valor"]) for e in m["eventos"]}
    for cc in c.celulas:
        for _, f in cc.frases:
            de.setdefault(cc.id, set()).add(par[f])
    for cid, hs in de.items():
        for x in hs:
            afirm.setdefault(x, set()).add(cid)
    dados = [mundo_q.oraculo(s, r, i) for r in m["orden"] for i in m["orden"][r]]
    dados2 = [mundo_q.oraculo(s, r, i) for r in m["orden"] for i in m["orden"][r]]
    print(f"semilla {s}: eventos {len(m['eventos'])}, preguntas {len(dados)}, revelaciones {sum(dados)} "
          f"(dado repetible: {dados == dados2}); células {len(c.celulas)}, afirmaciones {len(afirm)}, "
          f"falsas confirmaciones {sum(len(h) > 1 for h in de.values())}, partidas {sum(len(x) > 1 for x in afirm.values())}; "
          f"compuerta: candidatas AJENAS {ajenas}, máx ajena {max_ajena:.2f}, mín propia {min_propia:.2f} (umbral {UMBRAL_Q})")
for k, (a, b) in total.items():
    print(f"IDENTIDAD {k}: {a}/{b} consultas idénticas" + (" (BIT A BIT)" if a == b else "  <-- DIFERENCIA"))
    mal |= (a != b)
print("ARNÉS:", "BIEN" if not mal else "MAL")
sys.exit(1 if mal else 0)
