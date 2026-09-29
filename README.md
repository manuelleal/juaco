# JUACO

JUACO is an artificial-life research project. It studies minimal digital organisms that follow local rules, with no
backpropagation, as they live, eat, reproduce and evolve in simulated worlds. It asks how far natural selection can go
at building capabilities that nobody designed.

It is also an experiment in method. One researcher directs a team of LLM agents under a strict protocol:
- preregistration before any data;
- bit-for-bit identity harnesses;
- controls that can fail;
- replication on new seeds;
- independent audit.

Every error is numbered and kept.

## The world in brief
- **Objects:** a ring-shaped world holds four kinds of objects. Food (A) and water (C) feed an organism's two needs,
  energy and water. Poison (B) and salt (D) look similar and harm it when bitten.
- **Organism and lineage:** an organism moves, bites, dies of hunger, thirst, poison or salt, and gives birth when both
  reserves are high enough. A lineage is one organism and all its descendants.
- **Founder:** the first organism of a lineage, born knowing nothing.
  - **Founder replacement:** when a lineage dies out, the simulator inserts a fresh founder.
  - **Nursery:** a period during which founders are supplied from outside. "No nursery" means that after the start
    (or after a cut-off) no one is put in, so the lineage lives or dies on its own.
- **R0:** real births per death in a lineage. Founders put in from outside do not count. Near 1 means the lineage
  replaces itself; the project's bar is 0.90.
- **K:** carrying capacity, the average number of living organisms in the second half of a run.
- **Worlds:**
  - **ECO:** the evolution world. Offspring inherit genes with mutation, and many founders can coexist.
  - **Race track:** a separate, harder test world. Nine lineages share it, with one living body per lineage at a time.

## Verified results
Closed and replicated, with data files, hashes and what each one does *not* show: see
[`RESULTADOS_VERIFICADOS.md`](RESULTADOS_VERIFICADOS.md).

1. **Natural selection assembles a rejection rule from composable parts.** Given rule "blocks", selection alone fixes an
   "organ": a heritable rejection rule ("don't bite what shows this pixel"). It also duplicates the rule. The lineage
   survives without a nursery in 19/20 seeds, twice (vs 14 and 13/20 with fixed genes; 1 and 0/20 without inheritance).
2. **Selection lowers the founders a lineage needs by 31–32 %,** even when every organism is born knowing nothing.
3. **Selection raises a lineage's carrying capacity** (K 31 → 39), 20/20 paired, in series and replication.
4. **A lineage sustains itself from a cold start** for 10⁶ steps, with no nursery (20/20 twice).
5. **The frozen reference organism (v14.3) passes the project's preregistered trunk criterion** in series and
   replication. It is the control that every other organism is compared against.

## Reproduce
Requires Python 3.13–3.14 and `pip install -r requirements.txt` (numpy, numba, llvmlite, scipy; exact versions pinned).

```bash
# Trunk check (~3 min):
cd organismo && python bateria_v143.py 6 && python bateria_generaliza_v143.py organismo_v143 20 --desde 101

# Result 1 (BLOQUES), series; ~12 min with --pool 6 on a 16-core PC; its verdict prints at the end:
python experimentos/organelos/bloques/opusM/corre_bloques.py --serie --desde 48411 --n 20 --T 500000 --pool 6
```

Run the identity harness of an experiment before trusting a new machine. Bits can change with library versions.

Reproduced by the author on 29 Sep 2026 on a Windows 11 PC (AMD Ryzen 7 5700), with Python 3.14.2 installed from
`requirements.txt`. The trunk check passes. Result 1 is bit-identical to the archived run: 161 files, where only the
wall-clock time field differs.

## What is NOT demonstrated
- No general intelligence, no language, no planning. The "organ" in result 1 is a heritable instinct, not learning.
- Results hold in the simulated worlds where they were measured. Evolved genomes transplanted to another world did not
  help (negative, registered).
- The "race track" wall (a founder must establish its lineage, R0 ≥ 0.90 in ≥ 15/20 seeds) has **not** been crossed by
  our own organisms. "O1" crosses it. O1 is a policy hand-written by an LLM agent; the name is an internal label,
  unrelated to OpenAI's o1 model. Our best designed rule matches O1's median but not the strict gate.
- With fixed genes, selection plateaus quickly. Open-ended evolution has not been shown.
- Single researcher, single project, small scale. Part of the registry was written by the agents themselves.

## Use of AI
The research direction, the questions, the go/no-go decisions and the final wording are the author's.

The code, the runs, the preregistrations and most of the registry were produced by LLM agents (Anthropic Claude models,
through Claude Code), working in fixed roles:
- **coordinator:** runs every series;
- **creators:** design and build, with no series and no commits;
- **independent read-only auditors:** check before and after every series;
- **chronicler:** drafts registry entries;
- **cheap testers.**

Every claim above was recomputed from raw files by an auditor agent. Every agent error is numbered in the registry.

## Structure
- `CLAUDE.md`: rules of the project.
- `registro/`:
  - `ESTADO.md`: current state, one page;
  - `REGISTRO_etapas_1_2.md`: full log;
  - `HANDOFF.md`: narrative;
  - `EQUIPO.md`: agent rules;
  - `RUTA.md`: publication route.
- `organismo/`: frozen trunk (`manifiesto.py --check`).
- `experimentos/`: every experiment with its preregistration, harness and data.

## License and citation
Code: MIT ([`LICENSE`](LICENSE)). Texts and data: CC BY 4.0 ([`LICENSE-DATA`](LICENSE-DATA)). How to cite:
[`CITATION.cff`](CITATION.cff).

Author: **Christiam Manuel Puentes Leal**, Independent researcher, Colombia.
ORCID: [0009-0002-2570-3397](https://orcid.org/0009-0002-2570-3397). Contact: [TU CORREO PERSONAL].
