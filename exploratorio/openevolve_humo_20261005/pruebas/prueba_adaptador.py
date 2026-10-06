"""Prueba 2: el adaptador (mismo CLI de Claude, misma sesion) con una pregunta minima. Mira tambien el aislamiento."""
import asyncio, json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
os.environ["JUACO_OE_REGISTRO"] = os.path.join(AQUI, "registro_prueba")
import adaptador_claude as A
from openevolve.config import LLMModelConfig
m = A.init_client(LLMModelConfig(name="sonnet", timeout=180, retries=0, retry_delay=1))
t0 = time.time()
r = asyncio.run(m.generate_with_context(
    "Responde en una sola linea, sin adornos.",
    [{"role": "user", "content": "Dime: (1) la palabra listo; (2) que herramientas tienes disponibles (nombres) o ninguna; "
                                 "(3) si en tu contexto actual aparece algo llamado JUACO, si o no."}]))
print("RESPUESTA:", r); print("seg", round(time.time() - t0, 1))
d = json.loads(open(os.path.join(A.REG, "llamadas.jsonl"), encoding="utf-8").read().splitlines()[-1])
print({k: v for k, v in d.items() if k not in ("sistema", "usuario", "respuesta")})
