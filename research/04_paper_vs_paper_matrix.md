# 04 — Paper × Paper Matrix

Status: Synthesis checkpoint, built entirely from Phase 1 + Phase 2 research
already completed. No new literature search performed. No architecture is
selected or recommended.

## Scoping note

A literal full pairwise grid across all ~112 papers (supplied + external)
would be ~12,000 cells, the overwhelming majority of which would be "no
relationship" — that format would bury the signal, not surface it. Instead,
this file compares papers directly against each other in three ways that
actually answer "how does paper A relate to paper B":

1. **Lineage clusters** — which papers build on, extend, or directly compete
   with which others (this is where genuine paper-to-paper structure exists).
2. **Closest-analogue table** — for each load-bearing paper (the ones
   bolded across `03_paper_vs_sih_matrix.md`), its nearest neighbor(s) and
   the specific dimension(s) on which they differ.
3. **Complementary-pair analysis for the three flagged gaps** — which
   specific pairs (or triples) of papers, if their distinct traits were
   combined, would substantially close each gap.

---

## 1. Lineage Clusters

### Cluster A — Classic hierarchical occupancy mapping
`Occupancy Grids (Elfes, 1990)` → `OctoMap (2013)` → `A-OctoMap (2024)`,
`SSMI (2021/23)`, `Larsson et al. (2022)`. Elfes established the Bayesian
occupancy-grid formalism; OctoMap added octree-based multi-resolution
compression via occupancy homogeneity; the SSMI/Larsson line (same research
group lineage, Asgharivaskasi & Atanasov + collaborators) added semantic
per-voxel distributions and, in Larsson et al., explicit semantic-class-
weighted pruning — the direct technical ancestor chain for Gap 1's
semantic-driven-resolution ingredient.

### Cluster B — Voxel-map LiDAR-inertial odometry
`Voxel Hashing (Nießner, 2013)` → `VoxelMap (2021)` → `Adaptive-LIO (2025)`.
Nießner's flat spatial hash table for sparse allocation is the direct
ancestor of VoxelMap's probabilistic voxel map (adds plane/edge features +
coarse-to-fine geometry-driven resolution), which Adaptive-LIO then extends
with an explicit distance-from-sensor resolution rule. This is the cleanest
"building on" chain found for the distance-driven adaptive-map-resolution
ingredient (Gap 1/3).

### Cluster C — Sparse 3D CNN / efficient detection
`Submanifold Sparse Conv (2017)` → `Minkowski Engine (2019)` →
`SECOND (2018, parallel)` → `PointPillars (2018/19, parallel/competing)` →
`SPVNAS (2020)`, `Focal Sparse Conv (2022)`, `SPS-Conv (2022)` →
`SPADE (2023)`, `SD-Conv/SPADE+ (2024)`, `FALO (2025)`, `Spira (2025)`. This
is the largest, most continuous lineage found — nine years of incremental
efficiency improvements on the same underlying idea (skip computation on
empty/unimportant sites). **FALO is the notable lineage-breaker**: it
explicitly reverses this entire line's core assumption (skip sparse sites)
in favor of dense, hardware-regular computation, and wins on certain edge
silicon — the clearest within-lineage disconfirming result in the whole
project.

### Cluster D — LiDAR moving-object segmentation (MOS)
`LMNet (2021)` → `4DMOS (2022)` → `MambaMOS (2024)` → `SegNet4D (2025)`. A
direct, linear "how do we fuse temporal information better" lineage:
range-image residuals (LMNet) → sparse 4D convolutions with receding-horizon
refinement (4DMOS) → state-space-model temporal-spatial coupling (MambaMOS)
→ efficient BEV-residual motion features with instance-awareness (SegNet4D).
All four share the same SemanticKITTI-MOS benchmark and — notably — the same
fixed-spatial-resolution assumption; none of the four architectural
generations changed this, which is itself evidence the field has not
considered resolution adaptivity a priority within this specific lineage.

### Cluster E — LiDAR scene flow
`PointPWC-Net (2019/20)` → `SeFlow (2024)`, `Flow4D (2024/25)`,
`SemanticFlow (2025)`. PointPWC-Net's coarse-to-fine feature pyramid (a
per-inference computation pattern, not persistent map resolution) is the
architectural template every later scene-flow paper still uses internally.
SeFlow adds explicit static/dynamic classification; Flow4D adds full 4D
voxel fusion across 5 frames; SemanticFlow adds joint instance segmentation.

### Cluster F — Elevation/terrain mapping for off-road ground vehicles
`Fankhauser et al. (2014/18)` → `MEM (2023)` → `RoadRunner (2024)` →
`RoadRunner M&M (2024)`. The clearest, most direct "building on" chain in
the terrain/2.5D space: classical Kalman-filtered elevation mapping →
adding multi-modal semantic fusion → replacing hand-designed features with
end-to-end learning → adding distance-tiered multi-resolution. This cluster
is the single strongest existing foundation for closing Gap 1 (it already
has 2.5D + semantics-in-some-form + adaptive-resolution-in-some-form,
just never all three at once in one paper — see §3 below).

### Cluster G — Off-road risk-aware traversability (MIT/ARL lineage)
`RAMP (2022/23)`, `STEP (2021, + SubT results 2023/24)`, `EVORA (2023/24)` —
overlapping authorship (Sharma, Fan, Cai, Ancha and collaborators), all
addressing risk/uncertainty-aware terrain traversability for fast off-road
navigation, but via three different formalisms: RAMP embeds risk in
planning-horizon depth; STEP uses CVaR tail-risk statistics; EVORA
decomposes aleatoric vs. epistemic uncertainty via evidential deep learning.
These three are best read as **competing approaches to the same sub-problem**
(see §4) rather than a linear lineage.

### Cluster H — Semantic-driven adaptive resolution (independent co-discovery)
`Larsson et al. (2022)` and `Stache et al. (2021/22)` are **not** a lineage
(different research groups, different domains — ground-robot exploration vs.
UAV agriculture) but independently arrived at the same core idea
(resolution allocation driven by detected/declared semantic content) within
one year of each other. This independent co-discovery is itself evidence
that semantic-driven adaptive resolution is a "ready idea" in the research
community's shared idea-space, not a fringe notion — relevant context for
judging Gap 1's difficulty.

---

## 2. Closest-Analogue Table (load-bearing papers)

| Paper | Closest analogue(s) | Shared | Key difference |
|---|---|---|---|
| Variable-Resolution NDT (supplied #7) | VoxelMap, MrHash | All three: persistent adaptive voxel map | NDT paper is curvature-driven with only memory (not compute) measured; VoxelMap is geometry/plane-driven for odometry; MrHash is variance-driven with both memory *and* speed measured |
| Adaptive-LIO | RoadRunner M&M | Both: explicit distance-from-sensor-driven persistent map resolution | Adaptive-LIO is full 3D LIO-focused (no terrain/semantic output); RoadRunner M&M is 2.5D terrain/traversability-focused with only 2 discrete tiers vs. Adaptive-LIO's continuous distance function |
| Larsson et al. | Stache et al. | Both: semantic-content drives resolution allocation | Larsson et al. is full 3D octree with an explicit formal objective (β/γ weights); Stache et al. is flat 2D UAV imagery driven by altitude changes (sensing-side mechanism producing a map-side effect) |
| MrHash | OctNet | Both: variable-resolution structure driven by a non-distance, non-semantic criterion | MrHash uses SDF variance in a persistent, GPU-hashed map with measured speed+memory gains; OctNet uses raw occupancy/density in a per-inference (not maintained) hybrid octree structure for classification tasks |
| RoadRunner M&M | Multi-Res. Elevation Mapping (Planetary Rotorcraft) | Both: 2.5D + genuinely spatially-variable resolution + terrain-safety output | RoadRunner M&M uses two discrete distance tiers (learned network); Planetary Rotorcraft uses continuous per-measurement pixel-footprint LoD (classical SfM-based) |
| MEM | RoadRunner | Both: 2.5D + semantic fusion into a persistent elevation map, same research lineage (ETH/JPL) | MEM is geometry-only fusion of externally-computed semantic probabilities (fixed resolution); RoadRunner replaces semantic labels with an end-to-end learned cost, also fixed resolution — neither adapts resolution |
| AdaOcc | MURAL | Both: 2024-2026, closest near-misses for Gap 2 (adaptive resolution + dynamic objects) | AdaOcc has genuine spatial resolution variability (ROI vs. background) but unconfirmed dynamic-object tie; MURAL has confirmed dynamic-object tracking (via downstream Kalman filter) but its resolution adaptation is temporal/deadline-driven and spatially uniform, not spatially variable |
| Funk et al. | AdaOcc | Both: genuine persistent adaptive map resolution | Funk et al. is confirmed to have **zero** dynamic-object handling (explicit static/quasi-static scope); AdaOcc's dynamic-object tie is unconfirmed (access-limited), not confirmed absent — a meaningfully different epistemic status |
| SPADE | Agile3D | Both: real, hardware-measured (embedded/accelerator) adaptive efficiency systems with large reported speedups | SPADE's speedups are largely custom-silicon-specific (its GPU-only comparison, 4-29x, is the more transferable figure); Agile3D's gains are demonstrated on commodity embedded GPUs (Jetson Orin/Xavier) under realistic multi-task contention, a more directly relevant validation context for a real robot |
| FALO | SPVNAS | Both: direct, measured evidence against "sparser/fewer active cells = automatically faster" | FALO shows sparse *losing* to a re-engineered dense alternative on specific edge silicon; SPVNAS shows sparse *winning* but at a much smaller measured-speedup ratio (2.7x) than its theoretical compute-reduction ratio (7.6x) would suggest — together they bound how much to trust any single reported multiplier without knowing the target hardware |
| G-VOM | RAMP | Both: fixed-resolution 3D/2.5D terrain analysis for fast ground-vehicle navigation | G-VOM is purely geometric (slope/roughness/obstacle detection, no risk formalism); RAMP adds explicit known-free/occupied/unknown risk categories and variable planning-horizon depth, but neither adapts map cell resolution |

---

## 3. Complementary-Pair Analysis for the Three Flagged Gaps

### Gap 1 — Persistent 2.5D map + explicit semantic-class-driven resolution, ground robot

The clearest hypothetical combination the existing literature suggests:
**Larsson et al.'s** explicit semantic-class-weighted pruning objective
(β/γ-weighted, applied to octree nodes) **+** **RoadRunner M&M's** (or
Fankhauser/MEM's) 2.5D ground-vehicle elevation-grid representation. Larsson
et al.'s objective function is not intrinsically tied to a full 3D octree —
it operates on tree nodes generically — so in principle an analogous pruning
rule could be defined over a 2.5D grid/quadtree instead. This is exactly
why Gap 1 was classified "likely genuine gap" rather than "fundamental
barrier": the combination looks mechanically plausible from the two papers'
own descriptions, but **no paper was found actually attempting it** — this
is an inference about feasibility, not a validated result, and would need a
Phase 8 feasibility check before being relied upon.

### Gap 2 — Adaptive resolution + dynamic-object perception, unified mechanism

Two candidate combinations, neither validated:
- **Funk et al.'s** real-time, region-automatic, persistent octree-resolution
  mechanism **+** any mature MOS system (**SegNet4D** is the most complete
  dynamic-perception candidate: semantic + dynamic + instance-aware, already
  real-time-oriented). Funk et al.'s mechanism operates on occupancy
  log-odds, which is compatible in principle with the occupancy-style grids
  SegNet4D-adjacent systems use, but the two have never been combined in
  any paper found.
- **MrHash's** variance-driven persistent map **+** a DOGMa-style per-cell
  velocity estimator (e.g., **Nuss et al.**'s random-finite-set filter or
  **Schreiber et al.**'s learned RNN DOGMa). MrHash's variance criterion is
  domain-agnostic (SDF variance in its original use, but the underlying
  mechanism — flag high-disagreement regions for finer resolution — could
  plausibly generalize to velocity-estimate disagreement as the adaptivity
  signal for a dynamic scene, though this is speculative synthesis, not a
  demonstrated result).

### Gap 3 — Multi-driver resolution policy (distance + semantics/uncertainty/terrain)

**MAP-ADAPT** is the existing paper closest to already solving this (it
combines semantic + geometric-complexity + available-compute drivers) — the
missing piece relative to the SIH's framing is simply adding **distance**
as an explicit fourth term, or swapping in **Adaptive-LIO's** distance rule
as MAP-ADAPT's "base" driver with semantic/geometric terms as refinements.
**Agile3D's** reinforcement-learning controller (which already jointly
selects spatial resolution based on both scene content and system
contention) is a second existing template for how a multi-driver decision
function could be learned rather than hand-specified — though Agile3D
operates on per-frame detection, not a persistent map, so adapting its
controller framework to a persistent-map setting is itself an open
integration question, not a solved one.

---

## 4. Competing Approaches to the Same Sub-Problem

These are pairs/groups of papers that are **not** a lineage but independently
solve the same narrow problem differently — directly relevant to Phase 5
(competing solution approaches), though no comparison or recommendation is
made here.

- **Adaptive map-resolution data structures**: OctoMap (occupancy-homogeneity
  octree) vs. wavemap (wavelet-hierarchical) vs. MrHash (variance-driven flat
  hash) vs. Larsson et al. (semantic-weighted octree) — four structurally
  different answers to "how should a map's resolution vary," each validated
  in a different application context, none compared head-to-head against
  each other in any single paper found.
- **Risk/uncertainty-aware terrain traversability**: RAMP (planning-horizon
  risk) vs. STEP (CVaR tail-risk) vs. EVORA (aleatoric/epistemic evidential
  decomposition) — three different formalisms for the same off-road
  navigation problem, from overlapping research groups, none of which
  adapts map resolution.
- **LiDAR moving-object segmentation representation choice**: LMNet (range
  image) vs. 4DMOS (sparse 4D voxel) vs. MambaMOS (raw point + state-space
  model) vs. SegNet4D (BEV image) — four different spatial representations
  for the identical MOS task on the identical benchmark (SemanticKITTI-MOS),
  none resolution-adaptive.
- **Sparse-computation efficiency on embedded hardware**: SPADE/SD-Conv
  (custom accelerator, exploit sparsity) vs. FALO (reject sparsity, go dense
  and regular) — directly opposing engineering philosophies for the same
  deployment target class (embedded/edge silicon), with real measured
  evidence on each side.

---

Next: `evidence/claims.md` and `evidence/unresolved_questions.md` carry the
sourced, evidence-labeled version of the claims made in this file and
`03_paper_vs_sih_matrix.md`.
