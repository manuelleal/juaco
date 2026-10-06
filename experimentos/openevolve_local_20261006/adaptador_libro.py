"""adaptador_libro.py — el adaptador ORIGINAL del humo del 5-oct, SIN TOCAR, mas un libro de gasto por llamada.

Mision: llegar a la AGI por este camino. ERR-194: en la nube el adaptador se reconstruyo y el proponente devolvio ~1 800 tokens por
llamada contra ~15 900 del humo. Aqui NO se reconstruye nada:
  - se carga por ruta el archivo original  C:\\Users\\User\\Documents\\PROYECTOS\\JUACO-OPENEVOLVE\\adaptador_claude.py  (sha b1ae88ae6b769bfb),
    con lo que el CLI corre con las MISMAS banderas, el mismo ejecutable y la MISMA carpeta de trabajo vacia (JUACO-OPENEVOLVE\\cwd_neutro,
    fuera del repo) que en el humo. Si el sha no coincide, aborta. (Testigo en esta carpeta: adaptador_claude_ORIGINAL.py.)
  - esta clase solo ANADE, alrededor de la llamada original: tope global de gasto (JUACO_OE_TOPE_USD sobre JUACO_OE_LIBRO) y una linea por
    llamada en el libro comun (corrida, modelo real, tokens, costo equivalente, segundos), sin el texto del prompt.
El registro completo (prompt y respuesta) lo sigue escribiendo el original en <salida>/registro_llm/llamadas.jsonl.
"""
import hashlib, importlib.util, json, os, time

ORIGINAL = os.environ.get("JUACO_OE_ADAPTADOR", r"C:\Users\User\Documents\PROYECTOS\JUACO-OPENEVOLVE\adaptador_claude.py")
SHA_ORIGINAL = "b1ae88ae6b769bfb"
_sha = hashlib.sha256(open(ORIGINAL, "rb").read().replace(b"\r\n", b"\n")).hexdigest()[:16]
if _sha != SHA_ORIGINAL:
    raise SystemExit(f"ADAPTADOR: {ORIGINAL} tiene sha {_sha}, no {SHA_ORIGINAL}: no es el original del humo; no se corre")
_spec = importlib.util.spec_from_file_location("adaptador_claude_original", ORIGINAL)
O = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(O)

LIBRO = os.environ["JUACO_OE_LIBRO"]                 # obligatorio
TOPE_USD = float(os.environ["JUACO_OE_TOPE_USD"])    # obligatorio (equivalente en USD que reporta el CLI; se paga con la suscripcion)
CORRIDA = os.environ.get("JUACO_OE_CORRIDA", "?")


def gasto_total():
    if not os.path.exists(LIBRO): return 0.0
    s = 0.0
    with open(LIBRO, encoding="utf-8") as fh:
        for l in fh:
            if l.strip(): s += float(json.loads(l).get("usd") or 0.0)
    return s


def _ultima():
    p = os.path.join(O.REG, "llamadas.jsonl")
    if not os.path.exists(p): return {}
    u = None
    with open(p, encoding="utf-8") as fh:
        for l in fh:
            if l.strip(): u = l
    return json.loads(u) if u else {}


class ConLibro(O.ClaudeCLI):
    def _llama(self, sistema, user, intento):
        g = gasto_total()
        if g + float(self.max_budget_usd) > TOPE_USD:
            raise RuntimeError(f"TOPE DE GASTO global: gastado {g:.3f} USD equiv + {self.max_budget_usd} por llamada > {TOPE_USD}")
        n0 = O._n_llamadas()
        try:
            return super()._llama(sistema, user, intento)
        finally:
            if O._n_llamadas() > n0:
                r = _ultima()
                fila = dict(corrida=CORRIDA, n=n0 + 1, t=r.get("t"), modelo=r.get("modelo"), modelos=r.get("modelos"), intento=r.get("intento"),
                            usd=r.get("costo_usd_equiv") or 0.0, seg=r.get("seg"), in_tok=r.get("tokens_entrada"),
                            cache_crea=r.get("tokens_cache_escr"), cache_lee=r.get("tokens_cache_lect"), out_tok=r.get("tokens_salida"),
                            car_sistema=r.get("car_sistema"), car_usuario=r.get("car_usuario"), car_respuesta=len(r.get("respuesta") or ""),
                            error=(r.get("error") or "")[:300] or None, esfuerzo_env=os.environ.get("CLAUDE_EFFORT"),
                            adaptador=_sha, anotado=time.strftime("%Y-%m-%d %H:%M:%S"))
                os.makedirs(os.path.dirname(os.path.abspath(LIBRO)), exist_ok=True)
                with open(LIBRO, "a", encoding="utf-8") as fh: fh.write(json.dumps(fila, ensure_ascii=False) + "\n")


def init_client(model_cfg):
    return ConLibro(model_cfg)
