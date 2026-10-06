"""adaptador_claude.py — RECONSTRUCCION para la serie de la nube (6-oct-2026).

El adaptador original del humo (sha b1ae88ae6b769bfb) NO esta en el repositorio. Este lo reemplaza, declarado en
PREREGISTRO_serie.md. Lo que garantiza, igual que el humo describe en su preregistro sec. 2:
  - el modelo corre por el CLI de Claude Code (`claude -p`), SIN herramientas (--tools ""), sin MCP, sin skills, sin
    persistencia de sesion, con el system prompt del YAML en lugar del de Claude Code, y en una CARPETA VACIA (no ve el repo
    ni su CLAUDE.md);
  - el prompt va por stdin (no por argv: evita el limite de largo de un argumento);
  - tope duro de llamadas por corrida (JUACO_OE_TOPE_LLAMADAS) y TOPE DURO DE GASTO GLOBAL (JUACO_OE_TOPE_USD, sumado
    sobre el libro comun JUACO_OE_LIBRO de TODAS las corridas, con candado de archivo). Al cruzarlo, toda llamada nueva falla;
  - cada llamada queda en <salida>/registro_llm/llamadas.jsonl (modelo, costo, tokens, segundos) y en el libro comun.
Lo que NO se sabe del original: si pasaba el prompt igual, con que banderas exactas y con que tope de gasto por llamada.
"""
import asyncio, fcntl, json, logging, os, subprocess, time

from openevolve.llm.claude_code import ClaudeCodeLLM

log = logging.getLogger(__name__)
VACIO = os.environ.get("JUACO_OE_VACIO") or os.path.join(os.environ.get("JUACO_OE_SALIDA", "."), "carpeta_vacia")
REG = os.environ.get("JUACO_OE_REGISTRO", "registro_llm")
LIBRO = os.environ["JUACO_OE_LIBRO"]                    # libro de gasto comun a todas las corridas (obligatorio)
TOPE_USD = float(os.environ["JUACO_OE_TOPE_USD"])       # tope global de gasto en llamadas al modelo (obligatorio)
TOPE_LLAM = int(os.environ.get("JUACO_OE_TOPE_LLAMADAS", "33"))
CORRIDA = os.environ.get("JUACO_OE_CORRIDA", "?")
POR_LLAMADA = float(os.environ.get("JUACO_OE_USD_POR_LLAMADA", "1.0"))   # --max-budget-usd de cada llamada


def gasto_total():
    if not os.path.exists(LIBRO): return 0.0
    s = 0.0
    with open(LIBRO, encoding="utf-8") as fh:
        for l in fh:
            if l.strip(): s += float(json.loads(l).get("usd", 0.0))
    return s


def _anota_libro(reg):
    os.makedirs(os.path.dirname(os.path.abspath(LIBRO)), exist_ok=True)
    with open(LIBRO, "a", encoding="utf-8") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX); fh.write(json.dumps(reg, ensure_ascii=False) + "\n"); fh.flush(); fcntl.flock(fh, fcntl.LOCK_UN)
    os.makedirs(REG, exist_ok=True)
    with open(os.path.join(REG, "llamadas.jsonl"), "a", encoding="utf-8") as fh: fh.write(json.dumps(reg, ensure_ascii=False) + "\n")


class LLMJuaco(ClaudeCodeLLM):
    n_llamadas = 0

    async def generate_with_context(self, system_message, messages, **kwargs):
        user = "\n\n".join(m.get("content", "") for m in messages if m.get("role") == "user")
        loop = asyncio.get_event_loop()
        return await asyncio.wait_for(loop.run_in_executor(None, lambda: self._llama(system_message or "", user)),
                                      timeout=self.timeout + 60)

    def _llama(self, sysmsg, user):
        f = os.path.join(REG, "llamadas.jsonl")   # el contador vive en disco: vale aunque OpenEvolve llame desde otro proceso
        LLMJuaco.n_llamadas = sum(1 for _ in open(f, encoding="utf-8")) if os.path.exists(f) else 0
        if LLMJuaco.n_llamadas >= TOPE_LLAM:
            raise RuntimeError(f"TOPE DE LLAMADAS de la corrida ({TOPE_LLAM}) alcanzado")
        g = gasto_total()
        if g + POR_LLAMADA > TOPE_USD:
            raise RuntimeError(f"TOPE DE GASTO global: gastado {g:.3f} USD + {POR_LLAMADA} por llamada > {TOPE_USD}")
        LLMJuaco.n_llamadas += 1
        os.makedirs(VACIO, exist_ok=True)
        cmd = ["claude", "-p", "--model", self.model, "--no-session-persistence", "--tools", "", "--strict-mcp-config",
               "--disable-slash-commands", "--output-format", "json", "--max-budget-usd", str(POR_LLAMADA),
               "--system-prompt", sysmsg]
        t0 = time.time()
        try:
            r = subprocess.run(cmd, input=user, capture_output=True, text=True, timeout=self.timeout, cwd=VACIO)
        except subprocess.TimeoutExpired:
            _anota_libro(dict(corrida=CORRIDA, n=LLMJuaco.n_llamadas, modelo=self.model, usd=0.0, error="timeout", seg=self.timeout,
                              nota="costo de una llamada cortada por tiempo: desconocido (no lo devuelve el CLI)"))
            raise asyncio.TimeoutError("claude -p: tiempo limite")
        seg = round(time.time() - t0, 1)
        try:
            d = json.loads(r.stdout)
        except Exception:
            _anota_libro(dict(corrida=CORRIDA, n=LLMJuaco.n_llamadas, modelo=self.model, usd=0.0, error=(r.stderr or r.stdout)[-400:], seg=seg))
            raise RuntimeError(f"claude -p no devolvio JSON: {(r.stderr or r.stdout)[-400:]}")
        usd = float(d.get("total_cost_usd") or 0.0); u = d.get("usage", {})
        _anota_libro(dict(corrida=CORRIDA, n=LLMJuaco.n_llamadas, modelo=self.model, modelos=list((d.get("modelUsage") or {}).keys()),
                          usd=usd, seg=seg, in_tok=u.get("input_tokens"), cache_crea=u.get("cache_creation_input_tokens"),
                          cache_lee=u.get("cache_read_input_tokens"), out_tok=u.get("output_tokens"),
                          subtipo=d.get("subtype"), es_error=d.get("is_error"), t=time.strftime("%H:%M:%S")))
        txt = d.get("result") or ""
        if d.get("is_error") or not txt.strip():
            raise RuntimeError(f"claude -p error o vacio: {d.get('subtype')} {str(txt)[:300]}")
        return txt


def init_client(model_cfg):
    return LLMJuaco(model_cfg)
