# -*- coding: utf-8 -*-
"""Punto 5: CLAVE POR ESTADO INTERNO DEL CUERPO contra la clave LÉXICA. Medición, no brazo.

Un segundo proceso llama-server (mismo modelo, modo --embeddings, pooling mean, otro puerto, hijo de este
proceso, 4 hilos; se cierra solo) da el estado interno promediado de cada frase y de cada pregunta. Se centra
(restar la media de las frases oídas: los cosenos crudos salen todos en 0.94–0.99) y se mide:
  (1) RECUPERACIÓN: para cada pregunta de un hecho enseñado, ¿la frase más cercana es de su hecho? (recall@1) y el
      margen mínimo (mejor propia − mejor ajena); lo mismo con la clave léxica de la colonia (parecido_pregunta).
  (2) FUSIÓN: cosenos entre pares de frases del mismo hecho y mismo valor (confirmación), mismo hecho y distinto
      valor (rival) y hechos distintos: ¿separa "misma afirmación" de "rival"? (la léxica v1 lo hace por firma).
Uso: python -B claves.py --semillas 31,32,33 [--plantillas B]    -> datos/claves_embeddings.json
Se corre DESPUÉS de la prueba principal (no comparte CPU con ella)."""
import argparse
import json
import math
import os
import socket
import subprocess
import time
import urllib.request

import mundo
from colonia import Indice, parecido_pregunta, tokens
from cuerpo import SERVIDOR, MODELO, AQUI


def _puerto_libre():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class CuerpoEmbeddings:
    def __enter__(self):
        self.puerto = _puerto_libre()
        self._log = open(os.path.join(AQUI, "datos", "servidor_emb.log"), "w", encoding="utf-8", errors="replace")
        cmd = [SERVIDOR, "-m", MODELO, "--host", "127.0.0.1", "--port", str(self.puerto), "-t", "4", "-tb", "4",
               "-c", "1024", "-np", "1", "--no-webui", "--embeddings", "--pooling", "mean", "--seed", "1"]
        self.proc = subprocess.Popen(cmd, stdout=self._log, stderr=subprocess.STDOUT, cwd=os.path.dirname(SERVIDOR))
        t0 = time.time()
        while time.time() - t0 < 180:
            if self.proc.poll() is not None:
                raise RuntimeError("llama-server (embeddings) terminó al arrancar; ver datos/servidor_emb.log")
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{self.puerto}/health", timeout=2) as r:
                    if json.loads(r.read()).get("status") == "ok":
                        return self
            except Exception:
                time.sleep(0.5)
        self.__exit__(None, None, None)
        raise RuntimeError("llama-server (embeddings) no respondió")

    def __exit__(self, *a):
        if self.proc.poll() is None:
            self.proc.terminate()          # sólo nuestro hijo, por manejador
            try:
                self.proc.wait(timeout=20)
            except Exception:
                pass
        self._log.close()
        return False

    def embed(self, textos):
        out = []
        for i in range(0, len(textos), 16):
            req = urllib.request.Request(f"http://127.0.0.1:{self.puerto}/v1/embeddings",
                                         data=json.dumps({"input": textos[i:i + 16]}).encode("utf-8"),
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=600) as r:
                d = json.loads(r.read().decode("utf-8"))
            out += [x["embedding"] for x in sorted(d["data"], key=lambda x: x["index"])]
        return out


def _cos(a, b):
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
    return sum(x * y for x, y in zip(a, b)) / (na * nb) if na and nb else 0.0


def _centra(vs, media):
    return [[x - m for x, m in zip(v, media)] for v in vs]


def mide(semilla, plantillas, emb):
    m = mundo.construye(semilla, plantillas)
    ev = m["eventos"]
    frases = [e["frase"] for e in ev]
    pregs = [h for h in m["preguntas"] if h["clase"] not in ("NN", "CTRL")]
    t0 = time.time()
    E = emb.embed(frases + [h["pregunta"] for h in pregs])
    seg = time.time() - t0
    media = [sum(v[j] for v in E[:len(frases)]) / len(frases) for j in range(len(E[0]))]
    Ec = _centra(E, media)
    EF, EQ = Ec[:len(frases)], Ec[len(frases):]
    idx = Indice()
    for f in frases:
        idx.agrega(tokens(f))
    res = {"emb": {"recall1": 0, "margenes": []}, "lex": {"recall1": 0, "margenes": []}, "n": len(pregs)}
    for q, eq in zip(pregs, EQ):
        propias = [i for i, e in enumerate(ev) if e["hecho"] == q["id"]]
        ajenas = [i for i, e in enumerate(ev) if e["hecho"] != q["id"]]
        for nombre, sim in (("emb", lambda i: _cos(eq, EF[i])), ("lex", lambda i: parecido_pregunta(idx, q["pregunta"], frases[i]))):
            sp = [sim(i) for i in propias]
            sa = [sim(i) for i in ajenas]
            res[nombre]["recall1"] += int(max(sp) > max(sa))
            res[nombre]["margenes"].append(round(max(sp) - max(sa), 4))
    # fusión: pares de frases
    pares = {"misma_afirmacion": [], "rival": [], "otro_hecho": []}
    for i in range(len(ev)):
        for j in range(i + 1, len(ev)):
            if ev[i]["hecho"] == ev[j]["hecho"]:
                k = "misma_afirmacion" if ev[i]["valor"] == ev[j]["valor"] else "rival"
            else:
                k = "otro_hecho"
            pares[k].append(_cos(EF[i], EF[j]))
    def q(xs, p):
        xs = sorted(xs)
        return round(xs[min(len(xs) - 1, int(p * len(xs)))], 3) if xs else None
    out = {"semilla": semilla, "plantillas": plantillas, "n_preguntas": len(pregs), "seg_embeddings": round(seg, 1), "dim": len(E[0]),
           "recuperacion": {k: {"recall1": f"{v['recall1']}/{len(pregs)}", "margen_min": min(v["margenes"]), "margen_mediana": q(v["margenes"], 0.5)}
                            for k, v in res.items() if k != "n"},
           "fusion_cos": {k: {"n": len(v), "p10": q(v, 0.1), "mediana": q(v, 0.5), "p90": q(v, 0.9)} for k, v in pares.items()},
           "separa_misma_de_rival": round(sum(1 for a in pares["misma_afirmacion"] if a > q(pares["rival"], 0.9)) / max(1, len(pares["misma_afirmacion"])), 3)}
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--semillas", default="31,32,33")
    ap.add_argument("--plantillas", default="B")
    a = ap.parse_args()
    res = []
    with CuerpoEmbeddings() as emb:
        for s in [int(x) for x in a.semillas.split(",")]:
            r = mide(s, a.plantillas, emb)
            res.append(r)
            print(json.dumps(r, ensure_ascii=False))
    json.dump(res, open(os.path.join(AQUI, "datos", "claves_embeddings.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("escrito datos/claves_embeddings.json")
