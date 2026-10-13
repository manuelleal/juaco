# -*- coding: utf-8 -*-
"""CUERPO CONGELADO del Frankenstein v0: un modelo abierto real (Qwen2.5-1.5B-Instruct, GGUF q4_k_m)
servido por el binario oficial de llama.cpp (llama-server, CPU) en localhost.

- Un solo proceso servidor, hijo de este proceso, con 4 hilos. Se cierra con terminate() sobre
  SU PROPIO manejador (nunca taskkill, nunca por nombre).
- Sin torch, sin dependencias: sólo biblioteca estándar (urllib, subprocess, json).
- Temperatura 0 y semilla fija: la misma petición da el mismo texto. Caché en disco por petición
  (guarda también los segundos de la primera vez, para no medir tiempos de caché).
"""
import hashlib
import json
import os
import socket
import subprocess
import time
import urllib.request

RAIZ_MODELOS = r"C:\Users\User\Documents\PROYECTOS\JUACO-MODELOS"
SERVIDOR = os.path.join(RAIZ_MODELOS, "llama_cpp", "llama-server.exe")
MODELO = os.path.join(RAIZ_MODELOS, "modelos", "qwen2.5-1.5b-instruct-q4_k_m.gguf")
HILOS = 4
AQUI = os.path.dirname(os.path.abspath(__file__))


def _puerto_libre():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Cuerpo:
    def __init__(self, cache=None, hilos=HILOS, ctx=4096, verboso=False):
        self.hilos = min(int(hilos), 4)
        self.ctx = ctx
        self.proc = None
        self.puerto = None
        self.verboso = verboso
        self.cache_ruta = cache
        self.cache = {}
        self.n_llamadas = 0
        self.n_cache = 0
        if cache and os.path.exists(cache):
            with open(cache, "r", encoding="utf-8") as f:
                for linea in f:
                    try:
                        d = json.loads(linea)
                        self.cache[d["k"]] = d["v"]
                    except Exception:
                        pass
        self._fcache = open(cache, "a", encoding="utf-8") if cache else None

    # ---------- vida del servidor ----------
    def __enter__(self):
        self.puerto = _puerto_libre()
        self._log = open(os.path.join(AQUI, "datos", "servidor.log"), "w", encoding="utf-8", errors="replace")
        cmd = [SERVIDOR, "-m", MODELO, "--host", "127.0.0.1", "--port", str(self.puerto),
               "-t", str(self.hilos), "-tb", str(self.hilos), "-c", str(self.ctx), "-np", "1",
               "--no-webui", "--seed", "1"]
        self.proc = subprocess.Popen(cmd, stdout=self._log, stderr=subprocess.STDOUT,
                                     cwd=os.path.dirname(SERVIDOR))
        t0 = time.time()
        while time.time() - t0 < 180:
            if self.proc.poll() is not None:
                raise RuntimeError("llama-server terminó al arrancar; ver datos/servidor.log")
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{self.puerto}/health", timeout=2) as r:
                    if json.loads(r.read()).get("status") == "ok":
                        self.seg_carga = time.time() - t0
                        return self
            except Exception:
                time.sleep(0.5)
        self.__exit__(None, None, None)
        raise RuntimeError("llama-server no respondió en 180 s")

    def __exit__(self, *a):
        if self.proc is not None and self.proc.poll() is None:
            self.proc.terminate()          # sólo nuestro hijo, por manejador
            try:
                self.proc.wait(timeout=20)
            except Exception:
                pass
        if self._fcache:
            self._fcache.close()
        try:
            self._log.close()
        except Exception:
            pass
        return False

    # ---------- llamada ----------
    def _post(self, ruta, cuerpo):
        req = urllib.request.Request(f"http://127.0.0.1:{self.puerto}{ruta}",
                                     data=json.dumps(cuerpo).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read().decode("utf-8"))

    def chat(self, mensajes, max_tokens=48, esquema=None, usar_cache=True):
        """Devuelve dict: texto, seg (de la primera vez), n_prompt, n_gen, tps_gen, p_min, p_media
        (probabilidad mínima y media de los tokens generados: la señal de DUDA del cuerpo)."""
        pet = {"messages": mensajes, "temperature": 0.0, "seed": 1, "max_tokens": max_tokens,
               "logprobs": True, "top_logprobs": 1, "cache_prompt": True}
        if esquema is not None:
            pet["response_format"] = {"type": "json_schema",
                                      "json_schema": {"name": "s", "strict": True, "schema": esquema}}
        k = hashlib.sha256(json.dumps(pet, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
        self.n_llamadas += 1
        if usar_cache and k in self.cache:
            self.n_cache += 1
            return dict(self.cache[k], de_cache=True)
        t0 = time.time()
        r = self._post("/v1/chat/completions", pet)
        seg = time.time() - t0
        ch = r["choices"][0]
        texto = ch["message"]["content"] or ""
        lp = [c["logprob"] for c in ((ch.get("logprobs") or {}).get("content") or [])]
        import math
        ps = [math.exp(x) for x in lp] or [0.0]
        tim = r.get("timings", {})
        v = {"texto": texto.strip(), "seg": round(seg, 3),
             "n_prompt": r.get("usage", {}).get("prompt_tokens"),
             "n_gen": r.get("usage", {}).get("completion_tokens"),
             "tps_gen": tim.get("predicted_per_second"), "tps_prompt": tim.get("prompt_per_second"),
             "p_min": round(min(ps), 4), "p_media": round(sum(ps) / len(ps), 4),
             "p_tokens": [round(p, 3) for p in ps[:24]]}
        if usar_cache:
            self.cache[k] = v
            if self._fcache:
                self._fcache.write(json.dumps({"k": k, "v": v}, ensure_ascii=False) + "\n")
                self._fcache.flush()
        return dict(v, de_cache=False)


def mide_velocidad():
    """Tokens por segundo: 3 generaciones largas sin caché."""
    out = []
    with Cuerpo() as c:
        print(f"carga del modelo: {c.seg_carga:.1f} s; hilos {c.hilos}")
        for p in ["Explica en un párrafo qué es la fotosíntesis.",
                  "Escribe cinco frases sobre los ríos de Colombia.",
                  "Cuenta del 1 al 60 separando con comas."]:
            r = c.chat([{"role": "user", "content": p}], max_tokens=160, usar_cache=False)
            out.append(r)
            print(f"  gen {r['n_gen']} tok a {r['tps_gen']:.1f} tok/s; prompt {r['n_prompt']} tok a "
                  f"{r['tps_prompt']:.1f} tok/s; {r['seg']:.2f} s | {r['texto'][:90]!r}")
    g = sorted(x["tps_gen"] for x in out)
    res = {"tps_gen_mediana": g[1], "tps_gen_min": g[0], "tps_gen_max": g[2],
           "tps_prompt": [x["tps_prompt"] for x in out], "hilos": HILOS, "seg_carga": c.seg_carga}
    with open(os.path.join(AQUI, "datos", "velocidad.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print(res)


if __name__ == "__main__":
    mide_velocidad()
