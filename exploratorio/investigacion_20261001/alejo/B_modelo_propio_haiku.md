# Alejo, perspectiva B — modelo propio, chico y especializado (explorador Haiku, 1-oct-2026)

**Aviso del coordinador:** informe de un explorador ligero, guardado tal cual. Es un mapa para saber dónde mirar, NO una fuente: varias cifras parecen imprecisas o mal atribuidas y hay que abrir cada enlace antes de citarlo. Dudosas a primera vista: "Forward-Forward (Hinton 2024)" (el original es de 2022; el enlace es otro trabajo), "TRM supera a o3-mini/Gemini 2.5 Pro" (comparación en ARC, discutida), "Lottery Ticket: 6.7× convergencia", "GUANE-1 60+ TFlops/Watt", "ARC-AGI-2 55.5 %".

## 1. Modelos pequeños especializados en nicho
- Tiny Recursive Model (TRM, 7M parámetros, Samsung SAIL): 45 % en ARC-AGI-1, 8 % en ARC-AGI-2. https://the-decoder.com/tiny-ai-model-outperforms-o3-mini-and-gemini-2-5-pro-in-arc-agi-benchmark/
- Modelos ajustados de 3B–13B que superan a modelos generales en tareas específicas (ley, medicina, código). https://www.flowhunt.io/blog/how-a-7-million-parameter-model-is-beating-frontier-ai-models/
- Costo: la especialización renuncia a la universalidad; el dato vale en dominios acotados.

## 2. Aprendizaje sin retropropagación a escala
- Forward-Forward y derivados. https://arxiv.org/abs/2404.08573
- Codificación predictiva y equilibrium propagation a escala ImageNet; se degradan con más de 5–7 capas. https://arxiv.org/pdf/2606.03584
- SoftHebb: hebbiano local sin supervisión, 2–3 capas, robusto a ruido (ICLR 2023).
- Redes de impulsos y chips neuromórficos (SpiNNaker 2, Loihi 2): ventajas de energía en casos concretos; un trabajo de 2024 las relativiza al contar memoria y accesos. https://arxiv.org/abs/2409.08290

## 3. Redes que crecen y se podan
- HyperNCA: crecimiento por autómatas celulares; Lunar Lander y locomoción de cuadrúpedo (ICLR 2022). https://arxiv.org/pdf/2204.11674
- Developmental Graph Cellular Automata. https://arxiv.org/pdf/2607.15726
- Lottery Ticket (Frankle y Carbin 2019): subredes podadas que entrenan igual o mejor. https://arxiv.org/pdf/1803.03635

## 4. Pruebas pequeñas para decisiones y aprendizaje continuo
- ARC-AGI-1 y ARC-AGI-2. https://www.alphaxiv.org/overview/2412.04604
- CORe50 (164k imágenes, 50 objetos, aprendizaje continuo). https://arxiv.org/pdf/1705.03550
- MiniGrid / BabyAI (19 niveles de lenguaje + navegación). https://service.tib.eu/ldmservice/dataset/minigrid-and-babyai-environments
- Bandidos contextuales. https://papers.neurips.cc/paper/2020/hash/033cc385728c51d97360020ed57776f0-Abstract.html

## 5. Contexto latinoamericano
- LatamGPT (CENIA, Chile; 30+ instituciones). https://www.cnnchile.com/pais/que-es-como-funcionara-latam-gpt-el-modelo-inteligencia-artificial-desarrollado-chile_20250213/
- SC3-UIS (Santander, Colombia), supercomputador GUANE-1. https://www.xataka.com.co/otros-dispositivos/la-supercomputadora-mas-rapida-de-colombia-se-encuentra-en-santander
- LaRedCCA, RedCLARA, SCALAC: redes de cómputo académico.
- "Talento en la Nube" (becas de computación en la nube). https://www.portafolio.co/tendencias/entregaran-20-000-becas-para-capacitaciones-en-cloud-computing-586277

## 6. El hueco, según el explorador
Nadie ha juntado las tres cosas: modelo diminuto especializado + aprendizaje local sin retropropagación + red que crece sola, entrenadas juntas. Alejo como prototipo portátil, iterable sin GPU cara.
