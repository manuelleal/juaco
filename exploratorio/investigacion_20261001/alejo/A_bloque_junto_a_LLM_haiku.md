# Alejo, perspectiva A — bloque pequeño y plástico pegado a un LLM congelado (explorador Haiku, 1-oct-2026)

**Aviso del coordinador:** informe de un explorador ligero, resumido y guardado. Es un mapa para saber dónde mirar, NO una fuente: hay que abrir cada enlace antes de citar. Dudas a primera vista: varios números de arXiv y versiones no los comprobé; el enlace de "SWE-Bench-CL" repite el de LifelongAgentBench; la frase final "Alejo sería el primero" es entusiasmo del explorador, no un hecho verificado.

## 1. Módulos pequeños que trabajan junto a un LLM congelado
| qué | cómo | qué logra | qué le falta |
|---|---|---|---|
| MemGPT / Letta | memoria externa en tres niveles que el agente administra | supera la ventana fija | el módulo no aprende de las interacciones nuevas |
| LoRA | adaptadores de bajo rango, modelo congelado | muchísimos menos parámetros, intercambiables | cada actualización necesita gradientes |
| Adaptación en prueba sin tocar pesos | repondera con un conjunto chico etiquetado | readapta rápido a un dominio nuevo | no maneja cambio continuo |
| Vectores de dirección (activation steering) | suma vectores precalculados dentro del modelo | sin tocar pesos, reversible | poco fiable en casos raros |
| Enrutadores pequeños | un modelo chico elige qué experto responde | menos latencia | no aprende en línea |
| Controlador por refuerzo | una red chica aprende cuándo editar, probar o criticar | acciones discretas, auditable | explora lento |

Enlaces: https://www.noze.it/en/insights/letta-memgpt/ · https://ar5iv.labs.arxiv.org/html/2106.09685 · https://arxiv.org/abs/2602.02633 · https://arxiv.org/html/2505.22637v1 · https://arxiv.org/html/2506.16419v1 · https://www.alphaxiv.org/abs/2607.25415

## 2. Parientes con aprendizaje local, sin retropropagación
- kNN adaptativo: actualización inmediata, costo de guardar ejemplos. https://proceedings.neurips.cc/paper_files/paper/1993/file/5f0f5e5f33945135b874349cfbed4fb9-Paper.pdf
- Redes de Hopfield modernas (memoria asociativa con regla local). https://uwspace.uwaterloo.ca/items/853a9037-f8cc-43ad-8bcb-2c40f877e499/full
- Reglas hebbianas / Oja: en línea y locales, convergen lento. https://arxiv.org/abs/2408.08408
- Bandidos sin gradiente: sólo necesitan un premio escalar. https://research.google/pubs/online-convex-optimization-in-the-bandit-setting-gradient-descent-without-a-gradient/
- Pesos rápidos / hiperredes: dos escalas de tiempo. https://ar5iv.labs.arxiv.org/html/1703.00837

## 3. Pruebas baratas para readaptación y memoria
- LifelongAgentBench. https://arxiv.org/pdf/2505.11942
- CL-Bench. https://arxiv.org/abs/2507.00014
- LTMBenchmark (recuerdo bajo distracción). https://arxiv.org/pdf/2512.13564
- Composición distribuida con premio tipo bandido. https://par.nsf.gov/servlets/purl/10472050

## 4. Modelos abiertos pequeños para PC
TinyLlama 1.1B (~1.2 GB) · Phi-3 Mini 3.8B (~4.9 GB) · Qwen 2B (~1.3 GB) · BitNet b1.58 2B (~0.4 GB) · Llama 3.2 3B (~2 GB). Tamaños cuantizados, sin comprobar.

## 5. El hueco, según el explorador
No encontró un módulo que olvide a propósito (por escasez), aprenda localmente sin gradientes y se verifique contra un LLM congelado. La memoria externa actual guarda de forma pasiva; los adaptadores necesitan gradientes; los bandidos exploran a ciegas; la memoria asociativa recupera lo viejo pero no detecta lo nuevo.

Idea de circuito que propone: el bloque aprende cuándo pedirle ayuda al LLM; el LLM evalúa lo que hace el bloque; el bloque se ajusta con ese premio por reglas locales.
