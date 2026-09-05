# 02 — Technical Taxonomy

Status: Built from Phase 1 (8 supplied papers) + Phase 2 (~104 external
papers). This is a synthesis document — it organizes what has been found
along the dimensions CLAUDE.md specifies, so gaps and competing approaches
(Phases 4-5) can be identified from evidence rather than assumption. **No
architecture is selected or recommended here.**

Sources: `../evidence/citations.md`, `../research/papers/*.md` (supplied),
`../external_literature/00_inventory.md` and `group_{a..e}_*.md` (external).

---

## Axis 1 — The Six Adaptive-Mechanism Categories

CLAUDE.md and this project's Phase 2 briefs require distinguishing six
mechanisms that the word "adaptive" gets applied to indiscriminately in the
literature. This axis is the single most important finding-organizer from
Phase 2.

| Category | Definition | Example papers (supplied + external) |
|---|---|---|
| **Adaptive sensor acquisition** | The physical sensor/scan pattern itself changes | αLiDAR (supplied #3, pure example); Adaptive Fovea (Tasneem 2020); MEMS-based Adaptive LiDAR (Pittaluga 2020); Stache et al. UAV (2021/22, altitude change) |
| **Adaptive sensing** (broader) | Sensing-side adaptivity not limited to scan pattern | Space-variant/active vision survey (2023) |
| **Adaptive neural computation** | A network's compute graph/inference cost adapts per input | Ada3D; Focal Sparse Conv; SPS-Conv; Agile3D; MURAL; Mixture-of-Experts edge detection |
| **Adaptive attention/ROI** | Learned/rule-based attention reallocates processing effort | FOVEA; PointSplit; Fast Attention-Based Simplification; HOTFormerLoc (partial) |
| **Adaptive computational representation** | Internal data structure adapts (e.g. sparse tensors), independent of a persistent map | Nearly all of Group E (SECOND, Minkowski Engine, SPVNAS, Spira, SD-Conv); AVS-Net; DFPS |
| **Adaptive map resolution** | The **persistent** map/grid/voxel structure has spatially varying resolution | Variable-resolution NDT (supplied #7); Adaptive-LIO; VoxelMap; D-Map; wavemap; OctoMap; MAP-ADAPT; Larsson et al.; RoadRunner M&M; Funk et al.; **MrHash** (cleanest example in the whole search); AdaOcc (partial) |

**Key finding**: the category that matters most for the SIH problem
("adaptive spatial representation") is the last one, **adaptive map
resolution** — and it is real but comparatively rare. Across the entire
Phase 2 search (~104 papers), fewer than 15 papers are genuine, persistent,
spatially-varying-resolution *maps*; the great majority of "adaptive LiDAR"
literature is either sensing-side or transient per-inference computation
(sparsity, attention, conditional compute) that never persists as a map.

## Axis 2 — Resolution Drivers (what decides where resolution is finer/coarser)

| Driver | Example papers | Notes |
|---|---|---|
| **Distance from sensor/robot** | Adaptive-LIO; RoadRunner M&M (2 fixed tiers); range-based density optimization; Cylinder3D (implicit, via coordinate system) | The SIH problem statement's own example. Well-precedented (disproves H1) but several papers (PointPillars' own limitation, the embedded voxel-efficiency paper) show distance-only coarsening is exactly where small/distant objects get lost. |
| **Geometric complexity / curvature** | Variable-resolution NDT (supplied #7, curvature-driven); VoxelMap (plane/edge-driven) | Ignores semantics — a flat but important sign gets the same treatment as a flat unimportant wall. |
| **Occupancy homogeneity** | OctoMap; SSMI; A-OctoMap | The oldest, most classic driver (OctoMap 2013). |
| **Semantic class** | **Larsson et al. (2022)** — the clearest, most direct example; Stache et al. (2021/22, via altitude); MAP-ADAPT; TSDF Adaptive-Res. paper | Directly disproves H3 as a general claim; gap is the *combination* with 2.5D + ground-vehicle setting (see Axis 4). |
| **Uncertainty / variance** | **MrHash** (SDF variance); Langerwisch & Wagner (sensor error bounds); Variable-Resolution Virtual Maps USV (SLAM uncertainty) | MrHash is the strongest evidence that a non-distance, non-semantic criterion can outperform fixed resolution by a wide, measured margin. |
| **Sensing density / pixel footprint** | Multi-Resolution Elevation Mapping, Planetary Rotorcraft | Continuous analog of the distance-tier idea, driven by per-measurement geometry rather than a discrete rule. |
| **System load / latency deadline** | Agile3D; MURAL | A driver the SIH problem statement does not mention at all — resolution adapted to available compute/contention, not to the scene. Time-varying, not spatially-varying (MURAL is explicitly uniform-per-frame). |
| **Task/planning-horizon request** | Adaptive Patched Grid Mapping | Resolution driven by what a downstream consumer (planner) asks for, not sensor geometry or scene content. |
| **Fixed / none** | The large majority: 6 of 8 supplied papers; ROG-Map; G-VOM; MEM; RoadRunner; nearly all of Groups D and E | Still the empirical default even in recent (2024-2025), competitive, published systems. |

**Key finding**: at least seven structurally distinct resolution drivers have
independent published precedent. No paper found combines more than two of
them (e.g., MAP-ADAPT combines semantic + geometric complexity; RoadRunner
M&M's tiers are distance-only). A resolution policy that deliberately
combines drivers (e.g., distance as a coarse prior, refined by semantic
importance and local uncertainty) was **not found in the literature
searched** — this is a candidate gap for Phase 4, not yet a confirmed one.

## Axis 3 — Representation Type × Resolution Adaptivity

|  | **Fixed resolution** | **Adaptive resolution** |
|---|---|---|
| **2D** (no height) | Elfes occupancy grids; most DOGMa lineage (Nuss, Schreiber, Jang); BEV detectors (PointPillars, MotionNet) | Kraetzschmar quadtree (2004); Stache et al. UAV (semantic-driven, flat field only) |
| **2.5D** (height/elevation per cell) | 6 of 8 supplied papers (STM, Graph SLAM ×2, motion grids, evidential grids, lightweight SLAM); MEM; RoadRunner; Fankhauser elevation mapping | **RoadRunner M&M** (distance-tier); Multi-Res. Elevation Mapping Planetary Rotorcraft (measurement-density); Adaptive Patched Grid Mapping (request-driven, multi-layer) |
| **3D** (unrestricted) | VoxelNet; most sparse-conv lineage (SECOND, MinkowskiEngine base); metric-semantic mapping (supplied #2); αLiDAR (supplied #3) | Variable-resolution NDT (supplied #7, curvature); Adaptive-LIO; VoxelMap; D-Map; OctoMap; wavemap; Larsson et al.; SSMI; **MrHash** |

**Key finding — directly relevant to the SIH's "2.5D" framing**: the 2.5D ×
adaptive-resolution cell is populated (RoadRunner M&M, planetary rotorcraft
mapping, Adaptive Patched Grid Mapping), so 2.5D adaptive-resolution mapping
is **not itself novel** (this weakens any claim that the SIH's basic framing
is new). What is genuinely sparse across the entire search is the 2.5D ×
adaptive-resolution × **semantic-driven** intersection specifically — every
paper in the 2.5D-adaptive cell above uses a geometric driver (distance or
measurement density), never semantics. This is the most precise, evidence-
grounded statement of where a real (if narrow) gap sits.

## Axis 4 — Perception Capability Coverage

This axis checks which papers combine resolution adaptivity (any kind) with
each of the SIH's three core sub-problems.

| Combination | Found? | Strongest example(s) |
|---|---|---|
| Adaptive resolution + terrain analysis | **Yes** | RoadRunner M&M (distance-tier + CVaR traversability); Multi-Res. Elevation Mapping Planetary Rotorcraft (measurement-density + landing-site safety) |
| Adaptive resolution + semantic perception | **Yes** | Larsson et al. (class-weighted octree pruning); MAP-ADAPT; Stache et al. |
| Adaptive resolution + static-object perception | **Yes, incidentally** | AdaOcc (object-centric ROI detail); most octree/voxel mapping implicitly supports downstream static perception |
| Adaptive resolution + dynamic-object perception | **No clean example** | AdaOcc (resolution adaptive, dynamic-object tie unconfirmed) and MURAL (dynamic-object tie confirmed via downstream tracker, but resolution adaptation is temporal/uniform, not spatial) are the two closest near-misses — see H2 verdict in `../evidence/claims.md` |
| Adaptive resolution + uncertainty-driven policy | **Yes** | MrHash (SDF variance); Langerwisch & Wagner (sensor-error bounds); Variable-Resolution Virtual Maps USV (SLAM uncertainty) |
| 2.5D + semantic + terrain (any resolution) | **Yes, fixed-resolution only** | MEM (semantic 2.5D, fixed); RoadRunner (semantic-informed training, fixed 2.5D runtime map) |
| 2.5D + adaptive resolution + semantic (all three) | **Not found in the literature searched** | Nearest analogues: RoadRunner M&M (2.5D+adaptive, no semantics) and Larsson et al. (adaptive+semantic, not 2.5D) — see H4 in `../evidence/claims.md` |
| Real-time, embedded-hardware-validated adaptive resolution | **Yes, but conditional** | Agile3D (Jetson Orin/Xavier); MrHash (GPU); DFPS (CPU, but overhead caveat); FALO shows the *opposite* result is also real (sparse losing to dense on real edge silicon) |

## Axis 5 — Uncertainty Sub-Types (do not treat "uncertainty" as one thing)

Phase 2 (Group B in particular) found "uncertainty" used for at least five
mechanically distinct things across this literature. Any future architecture
decision that claims to be "uncertainty-aware" must specify which of these it
means:

1. **Sensor/measurement noise** — Elfes-lineage occupancy grids, EviLOG.
2. **Occupancy-state probability itself** — all classic Bayesian occupancy grids.
3. **Semantic-classification confidence** — E2-BKI.
4. **Model/epistemic confidence over predicted or extrapolated regions** — SOGMP's future-occupancy prediction, Uncertainty-driven Planner.
5. **Registration/alignment-fit uncertainty** — Uncertainty-Aware VI-SLAM's submap alignment; the NDT probability-density mixture model in the supplied variable-resolution NDT paper (#7).

A sixth, related but distinct concept — **risk** (a decision-theoretic
property, e.g. CVaR tail-risk in STEP/EVORA/RAMP) — is frequently conflated
with "uncertainty" in paper abstracts but is a property of *planning/decision
consequences*, not of the *representation* itself (the CVaR-MPPI paper is the
clearest illustration: genuinely risk-aware, with no spatial map at all).

## Axis 6 — Consolidated Hypothesis Status (see `../evidence/claims.md` for full sourcing)

| Hypothesis | Verdict |
|---|---|
| H1 — distance-based adaptive resolution is largely unexplored | **Disproved** |
| H2 — no work combines dynamic-object perception with adaptive resolution | **Weakened** (two near-misses, no clean counterexample) |
| H3 — semantic-aware adaptive resolution is unexplored | **Disproved generally; weakened for the SIH's exact setting** |
| H4 — 2.5D + adaptive resolution + semantic perception is a useful gap | **Weakened** (three-way combo not found; every pairwise combo exists) |
| H5 — adaptive map resolution gives meaningful compute/memory benefit | **Weakened/refined** (real, but hardware- and scale-conditional, not automatic) |
| H6 — adaptive LiDAR work mainly concerns sensing, not map representation | **Disproved**, with the refinement that "adaptive computational representation" (transient) vastly outnumbers genuine "adaptive map resolution" (persistent) within the non-sensing majority |

## What This Taxonomy Does Not Yet Do

This is Phase 2's taxonomy — built to organize findings and stress-test
Phase 1's hypotheses. It does **not**:

- Perform the formal gap analysis (Phase 4) — that requires explicitly
  weighing which of the "not found" combinations above are worth pursuing
  vs. worth explaining away.
- Generate or compare competing solution architectures (Phase 5).
- Recommend any representation, resolution policy, or method.

Next: Phase 3 (deepen this taxonomy if needed) and Phase 4 (gap analysis)
per `01_research_plan.md`.
