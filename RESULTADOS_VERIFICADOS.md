# Verified results

Only results that are **closed and replicated** appear here. Each one had a preregistration committed before any data,
a bit-for-bit identity harness, a series and an independent replication on new seeds, and an independent audit that
recomputed the numbers from the raw files. The hash is `sha256[:16]` of the verdict/summary file. Each result
carries one sentence stating what it does **not** show.

Full history, including every negative result and every numbered error, is in
`registro/REGISTRO_etapas_1_2.md`. Error numbers run from ERR-1 to ERR-153, with gaps. 126 numbers are defined and
120 of them are genuine errors; the tabulation is in `informe/errores.csv`.

---

Terms (world, founder, nursery, R0, K, ECO, race track) are defined in the README, section "The world in brief".

### 1. Natural selection assembles a rejection rule from composable parts (BLOQUES, 28-sep-2026)
- **What:** in a world where there is no nursery and no founder replacement, each organism carries a variable-length
  genome of rules assembled from primitive blocks (a sensor, a comparator, an action, a weight). Rules can mutate,
  duplicate, be deleted, or be copied from a neighbour. Under selection alone, the population fixes an **"organ"**.
  Here "organ" means a heritable rejection rule: "don't bite if the object shows this pixel". The rule separates poison
  and salt from food and water exactly, and it appears **duplicated** 2–3 times.
- **Numbers** (series 48411–48430 / replication 48431–48450):
  - lineage persists: 19/20 and 19/20 with rule blocks; 14/20 and 13/20 with 15 fixed brain genes; 1/20 and 0/20 without
    inheritance;
  - the "organ" is present in ≥ 50 % of the survivors in 19/20 and 18/20 seeds.
- **Data:**
  - `experimentos/organelos/bloques/opusM/datos/serie_s48411-48430_T500000/VEREDICTO.json` (`86c36f933da2543c`);
  - `…/serie_s48431-48450_T500000/VEREDICTO.json` (`49228926d48a63f5`);
  - preregistration `experimentos/organelos/bloques/opusM/PREREGISTRO_bloques.md` §10.
- **Does NOT show:** learning. The "organ" is a heritable *instinct* tied to fixed letter identities, in one simulated
  world (ECO).

### 2. Selection lowers the number of founders a lineage needs, with naïve offspring (ECO_SEL_ING, 28-sep-2026)
- **What:** offspring inherit genes but not the family's learned table, so every organism is born knowing nothing.
  Selection on 15 brain genes still reduces the founders a lineage needs by **31–32 %**, and raises carrying capacity.
  Without inheritance neither happens.
- **Numbers:**
  - founders replaced in the second half of the run: 128.6k in the baseline vs 86.8k / 88.6k with selection
    (20/20 paired, in both runs);
  - capacity K: 96.3 → 101.0.
- **Data:**
  - `experimentos/organelos/eco_sel_ing/datos/eco_sel_ing_serie_s46101-46120_T1000000/RESUMEN.json` (`edb11fcca4972c98`);
  - `…_s46121-46140_T1000000/RESUMEN.json` (`6d4f5cdf63c7fc0c`).
- **Does NOT show:** that the evolved genome helps elsewhere. Transplanted into a different world (the "race track"), it
  made founders worse.

### 3. Selection raises a lineage's carrying capacity that nobody designed (ECO_SEL, 28-sep-2026)
- **What:** on top of a lineage that already sustains itself, heritable mutation of a reproduction threshold, or of 15
  brain genes, raises the number of living bodies the same food flow supports. The same genes without inheritance
  lower it.
- **Numbers:**
  - K: 30.9 baseline vs 34.9 (threshold) and 38.9 (brain), 20/20 paired in series and replication;
  - poison + salt deaths fall from ~82 % to 2–3.5 % with the brain genes (descriptive).
- **Data:**
  - `experimentos/organelos/eco_sel/datos/eco_sel_serie_s45301-45320/RESUMEN.json` (`282c3b48a8491cd5`);
  - `…/eco_sel_serie_s45321-45340/RESUMEN.json` (`36d4b467ee0a8106`).
- **Does NOT show:** open-ended improvement. With 10× more time, K does not keep rising (cloud run, series only).

### 4. A lineage sustains itself from a cold start with no nursery (F1, 25-sep-2026)
- **What:** a family that passes down only what had consequences keeps the lineage alive for 10⁶ steps from t = 1, with
  no nursery and no founder replacement.
- **Numbers:**
  - 20/20 in series and replication;
  - controls: shuffled table 1/20 ×2; no family 0/20 ×2.
- **Data:**
  - `experimentos/organelos/frio/datos/frio_serie_s35001-35020/RESUMEN.json` (`e60f6928f17d67d9`);
  - `…/frio_serie_s35021-35040/RESUMEN.json` (`7837f7fe571f3aaf`).
- **Does NOT show:** transfer. The same mechanism does not help on the race track.

### 5. The frozen reference organism passes the project's preregistered criterion (v14.3, criterion v4, 24-sep-2026)
- **What:** the frozen reference organism v14.3 passes every gate of the project's preregistered trunk criterion, in
  series and replication. It is the control that every other organism is compared against.
  - Among the gates is composition: how many repeated stimuli it can still add up correctly. It reaches 8, where the
    previous reference reached 1.
  - It does not regress on any other gate.
- **Data:**
  - `experimentos/tronco_v14_3_examen/datos/examen_v143_serie_20260924_124413.json` (`d39303e1d6ae3949`);
  - `…/examen_v143_replica_20260924_131427.json` (`55b42f360a51951a`).
- **Does NOT show:** better survival on the race track. The scale gate (T-H) was not measured.
