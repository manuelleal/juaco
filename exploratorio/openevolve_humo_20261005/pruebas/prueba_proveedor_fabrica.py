"""Prueba 1: el proveedor claude_code DE FABRICA de OpenEvolve 0.4.0, sin tocar, con una pregunta minima."""
import asyncio, time, traceback
from openevolve.config import LLMModelConfig
from openevolve.llm.claude_code import ClaudeCodeLLM
cfg = LLMModelConfig(name="sonnet", provider="claude_code", timeout=120, retries=0, retry_delay=1, max_tokens=200, max_budget_usd=0.5)
m = ClaudeCodeLLM(cfg)
t0 = time.time()
try:
    r = asyncio.run(m.generate_with_context("Responde solo con la palabra pedida.", [{"role": "user", "content": "Escribe la palabra: listo"}]))
    print("RESPUESTA:", repr(r))
except Exception as e:
    print("ERROR:", type(e).__name__, e); traceback.print_exc()
print("segundos", round(time.time() - t0, 1))
