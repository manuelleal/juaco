"""adaptador_claude.py — el MISMO proveedor de OpenEvolve (`claude_code`: el CLI de Claude Code con la sesion del
director, sin clave), con cuatro arreglos para este PC. No se toca el paquete instalado: se engancha por `init_client`.

Por que hace falta (medido el 5-oct-2026, ver INFORME.md):
  1. El proveedor de fabrica lanza `claude` a secas; en Windows con instalacion npm eso es `claude.cmd` y Python no lo
     encuentra (FileNotFoundError WinError 2). Aqui se lanza el ejecutable real (claude.exe) por ruta.
  2. El de fabrica pasa TODO el prompt como argumento de linea de comandos (tope de Windows: 32767 caracteres).
     Aqui el prompt va por la entrada estandar.
  3. El de fabrica deja al modelo con herramientas, memoria y agentes del usuario: podria LEER el repo JUACO (O1.py) o
     recibir memoria del proyecto. Aqui: sin herramientas, modo seguro (sin CLAUDE.md, memoria, agentes, MCP, skills)
     y carpeta de trabajo vacia.
  4. El de fabrica no registra tokens. Aqui se pide la salida en JSON y se anota cada llamada en registro/llamadas.jsonl
     (prompt completo, respuesta completa, tokens, costo equivalente, segundos).
"""
import asyncio, json, os, shutil, subprocess, tempfile, time
from typing import Dict, List
from openevolve.llm.base import LLMInterface

AQUI = os.path.dirname(os.path.abspath(__file__))
REG = os.environ.get("JUACO_OE_REGISTRO", os.path.join(AQUI, "registro"))
CWD = os.path.join(AQUI, "cwd_neutro")
TOPE = int(os.environ.get("JUACO_OE_TOPE_LLAMADAS", "0"))   # 0 = sin tope propio (manda max_iterations)


def _exe():
    npm = os.path.join(os.environ.get("APPDATA", ""), "npm", "node_modules", "@anthropic-ai", "claude-code", "bin", "claude.exe")
    if os.path.exists(npm): return npm
    x = shutil.which("claude.exe") or shutil.which("claude")
    if not x: raise RuntimeError("no encuentro el CLI de Claude Code (claude.exe)")
    return x


def _n_llamadas():
    p = os.path.join(REG, "llamadas.jsonl")
    return sum(1 for _ in open(p, encoding="utf-8")) if os.path.exists(p) else 0


class ClaudeCLI(LLMInterface):
    def __init__(self, model_cfg=None):
        g = lambda k, d: (getattr(model_cfg, k, None) if model_cfg is not None else None) or d
        self.model = g("name", "sonnet"); self.system_message = g("system_message", None)
        self.timeout = g("timeout", 600); self.retries = g("retries", 1); self.retry_delay = g("retry_delay", 5)
        self.weight = g("weight", 1.0); self.max_budget_usd = g("max_budget_usd", 2.0)
        self.last_usage = None

    async def generate(self, prompt: str, **kw) -> str:
        return await self.generate_with_context(kw.pop("system_message", self.system_message) or "",
                                                [{"role": "user", "content": prompt}], **kw)

    async def generate_with_context(self, system_message: str, messages: List[Dict[str, str]], **kw) -> str:
        user = "\n\n".join(m.get("content", "") for m in messages if m.get("role") == "user")
        loop = asyncio.get_event_loop(); err = None
        for intento in range(self.retries + 1):
            try:
                return await loop.run_in_executor(None, lambda: self._llama(system_message, user, intento))
            except Exception as e:
                err = e; await asyncio.sleep(self.retry_delay)
        raise err

    def _llama(self, sistema, user, intento):
        os.makedirs(REG, exist_ok=True); os.makedirs(CWD, exist_ok=True)
        if TOPE and _n_llamadas() >= TOPE:
            raise RuntimeError(f"TOPE de llamadas al modelo alcanzado ({TOPE}): no se llama mas")
        fd, fs = tempfile.mkstemp(suffix=".txt", dir=REG, prefix="_sistema_"); os.close(fd)
        with open(fs, "w", encoding="utf-8") as fh: fh.write(sistema or "Eres un asistente.")
        cmd = [_exe(), "-p", "--model", self.model, "--no-session-persistence", "--output-format", "json",
               "--safe-mode", "--tools", "", "--strict-mcp-config", "--disable-slash-commands",
               "--system-prompt-file", fs, "--max-budget-usd", str(self.max_budget_usd)]
        t0 = time.time()
        reg = dict(t=time.strftime("%Y-%m-%d %H:%M:%S"), modelo=self.model, intento=intento,
                   sistema=sistema, usuario=user, car_sistema=len(sistema or ""), car_usuario=len(user))
        try:
            r = subprocess.run(cmd, input=user, capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=self.timeout, cwd=CWD)
            reg["seg"] = round(time.time() - t0, 1); reg["codigo"] = r.returncode
            try: j = json.loads(r.stdout)
            except Exception: j = None
            if j is None or j.get("is_error") or not j.get("result"):
                reg["error"] = (r.stdout[:1500] + " || " + r.stderr[:1500])
                raise RuntimeError("CLI de Claude sin respuesta util: " + reg["error"][:400])
            u = j.get("usage") or {}
            reg.update(respuesta=j["result"], tokens_entrada=u.get("input_tokens"), tokens_salida=u.get("output_tokens"),
                       tokens_cache_escr=u.get("cache_creation_input_tokens"), tokens_cache_lect=u.get("cache_read_input_tokens"),
                       costo_usd_equiv=j.get("total_cost_usd"), turnos=j.get("num_turns"),
                       modelos=list((j.get("modelUsage") or {}).keys()), ms_api=j.get("duration_api_ms"))
            self.last_usage = dict(prompt_tokens=u.get("input_tokens"), completion_tokens=u.get("output_tokens"))
            return j["result"].strip()
        except subprocess.TimeoutExpired:
            reg["seg"] = round(time.time() - t0, 1); reg["error"] = "timeout"
            raise RuntimeError("CLI de Claude: timeout")
        finally:
            try: os.remove(fs)
            except OSError: pass
            with open(os.path.join(REG, "llamadas.jsonl"), "a", encoding="utf-8") as fh:
                fh.write(json.dumps(reg, ensure_ascii=False) + "\n")


def init_client(model_cfg):
    return ClaudeCLI(model_cfg)
