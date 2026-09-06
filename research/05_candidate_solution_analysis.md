# 05 — Candidate Solution Analysis

Status: Synthesis + targeted supplementary research. Built primarily from
research already completed (`02_technical_taxonomy.md`,
`03_paper_vs_sih_matrix.md`, `04_paper_vs_paper_matrix.md`,
`evidence/claims.md`, `evidence/unresolved_questions.md`,
`external_literature/00_inventory.md`, and
`resolution_boundary_consistency.md`), supplemented with targeted new
research (not a repeat of the broad Phase 2 sweep) into three specific
gaps: object-aware/dynamic-object-aware adaptive resolution, lightweight-
vs-learned perception trade-offs, and driver-count/persistent-vs-transient
ablation evidence. **No architecture is selected or recommended in this
file.** No SIH pipeline is implemented.

---

## 0. Scope and method

Ten candidate directions (as specified) are each assessed against the same
fixed checklist. Evidence is drawn first from this project's own completed
research (cited by paper name, consistent with `03_paper_vs_sih_matrix.md`
and `04_paper_vs_paper_matrix.md`); new evidence gathered specifically for
this phase is marked **[NEW]** and tagged with its own evidence level.
Evidence-level tags follow `CLAUDE.md`: DIRECT EVIDENCE / DERIVED /
INFERENCE / HYPOTHESIS / WEB VERIFIED.

---

## 1. Candidate Approaches

### 1. Distance/range-driven variable-resolution mapping
Resolution is a function of distance from the sensor/robot: fine near,
coarse far — the SIH problem statement's own literal example. Best-evidenced
and cheapest of all ten directions.

### 2. Uncertainty/variance-driven adaptive resolution
Resolution refines wherever the map's own confidence is low (SDF variance,
registration disagreement, sparse coverage), independent of raw distance.

### 3. Semantic-aware adaptive resolution
Resolution is driven by detected/declared semantic class or content
importance — fine detail preserved on functionally important classes
(curbs, poles, pedestrians-relevant terrain), coarse elsewhere.

### 4. Object-aware adaptive resolution
Resolution is refined in a region-of-interest around a detected object
(any object, not necessarily in motion), independent of whether that region
happens to be near or far.

### 5. Dynamic-object-aware representation
A representation (fixed- or adaptive-resolution) specifically built to
detect, segment, and track *moving* objects, as distinct from static-scene
content — the MOS/DOGMa/scene-flow research families.

### 6. Multi-driver adaptive resolution
A single resolution policy combining 2 or more of the above criteria (e.g.
distance + semantics, or semantic + geometric complexity + compute budget).

### 7. Persistent adaptive maps vs. transient adaptive representations
Whether resolution adaptivity applies to a map that is built, retained, and
updated across the whole trajectory ("persistent"), or to a representation
rebuilt fresh each inference cycle with no cross-frame memory ("transient").

### 8. 2.5D elevation/occupancy representations vs. sparse 3D alternatives
Whether the fundamental spatial representation is 2.5D (height per 2D cell)
or full 3D (unrestricted volumetric/point representation).

### 9. Different data structures for nonuniform spatial representation
Given a decision to adapt resolution, which underlying structure holds it:
octree/quadtree, sparse voxel hash, wavelet-hierarchical field, or a small
number of discrete regular-grid tiers (no tree at all).

### 10. Lightweight vs. learned perception components
For each of the three perception sub-problems (terrain/traversability,
static/semantic, dynamic-object), whether a classical/geometric method or a
learned/neural method is used, and whether a hybrid (learned offline,
classical at runtime) captures most of the benefit of either extreme.

---

## 2. Evidence For Each

| # | Direction | Strongest supporting evidence |
|---|---|---|
| 1 | Distance-driven | **Adaptive-LIO** (arXiv:2503.05077, 2025) — explicit distance-from-sensor multi-resolution voxel map, built specifically because a fixed-resolution map was found to *fail* during indoor-outdoor scene-scale transitions; DIRECT EVIDENCE. **RoadRunner M&M** (arXiv:2409.10940) — 2.5D, two discrete distance tiers, 100m range, real-time-reported; DIRECT EVIDENCE. Cylinder3D shows the same distance-correlated effect can arise "for free" from a coordinate-system choice alone (INFERENCE that this could substitute for or complement an explicit rule). |
| 2 | Uncertainty-driven | **MrHash** (arXiv:2511.21459, TOG 2025) — SDF-variance-driven, persistent, GPU-hashed, ~4x memory reduction + up to 13x measured speedup; DIRECT EVIDENCE, the strongest single quantified result of any driver reviewed in this whole project. Variable-Resolution Virtual Maps/USV (arXiv:2603.22667, 2026) is a second, independent, SLAM-information-density-driven example. |
| 3 | Semantic-aware | **Larsson et al.** (arXiv:2209.10035, 2022) — explicit β/γ semantic-class-weighted octree-pruning objective; DIRECT EVIDENCE. **Stache et al.** (arXiv:2203.01642, 2021/22) — independent co-discovery (UAV altitude tied to semantic-class pixel ratio) within one year, itself evidence this is a "ready idea," not fringe; DIRECT EVIDENCE. MAP-ADAPT (arXiv:2406.05849, ECCV 2024) adds semantics as one of three combined drivers. |
| 4 | Object-aware | **AdaOcc** (arXiv:2408.13454, 2024) — genuinely spatially-variable, ROI-based occupancy resolution around detected objects, now full-text confirmed [NEW]; DIRECT EVIDENCE. **[NEW]** A camera-based foreground-modulation paper (arXiv:2604.05780) shows foreground-focused compute allocation can *simultaneously* cut GFLOPs by 71.9% **and** improve accuracy by +2.35 mIoU vs. dense processing — DIRECT EVIDENCE this is not a pure speed-for-accuracy trade. See §1.4. |
| 5 | Dynamic-object-aware | The MOS lineage (LMNet→4DMOS→MambaMOS→SegNet4D), scene-flow lineage (PointPWC-Net→SeFlow→Flow4D→SemanticFlow), and DOGMa lineage (Nuss/Danescu/Schreiber) are all mature, real-time-capable (several with measured FPS: 4DMOS, Flow4D), and benchmarked on SemanticKITTI-MOS/Argoverse 2; DIRECT EVIDENCE, ~23 papers. **[NEW]** RobMOT (arXiv:2405.11536) and Spb3DTracker (arXiv:2408.05940) independently show a classical Kalman-filter-family tracker matching or beating a learned tracker (PolarMOT) on real KITTI/Waymo benchmarks — RobMOT at **3,221 FPS on a single CPU core** — the strongest "lightweight suffices" evidence found anywhere in this project, for the tracking-given-detections half of dynamic-object perception specifically. |
| 6 | Multi-driver | MAP-ADAPT (semantic+geometry+compute) and **Agile3D** (MobiSys 2025, content+system-contention, real Jetson-measured **+7% accuracy** under realistic multi-task contention) both demonstrate 2-3-driver combination is tractable and beneficial; DIRECT EVIDENCE. |
| 7 | Persistent maps | Adaptive-LIO, VoxelMap, D-Map, OctoMap, wavemap, MAP-ADAPT, Larsson et al., RoadRunner M&M, Funk et al., MrHash — genuine, multi-frame, maintained adaptive-resolution maps with independent, multiply-replicated precedent; DIRECT EVIDENCE. |
| 7 | Transient representations | The entire Cluster C sparse-CNN lineage (SPVNAS, Focal Sparse Conv, SPS-Conv, SPADE, FALO) and the entire MOS/scene-flow lineage adapt *computation* per inference with no persisted map state; this is the numerically dominant pattern (fewer than 15 of ~104 external papers are genuine *persistent* adaptive maps) — DERIVED (relative-frequency observation over the reviewed set). |
| 8 | 2.5D | Well-solved per Gap Map: Fankhauser→MEM→RoadRunner→RoadRunner M&M lineage, plus Planetary Rotorcraft mapping, Adaptive Patched Grid Mapping; DIRECT EVIDENCE, mature across ground/off-road/aerial domains. |
| 8 | Full 3D | Supplied metric-semantic mapping paper (#2) explicitly chose full 3D over 2.5D and argues for it in its own related-work discussion; DIRECT EVIDENCE that at least one system considers 2.5D insufficient for large-scale outdoor semantic navigation. |
| 9 | Octree/quadtree | OctoMap, A-OctoMap, SSMI, Larsson et al., Funk et al. (3D octrees); Kraetzschmar, Langerwisch & Wagner (2D quadtrees) — mature, independently replicated structure choice; DIRECT EVIDENCE. |
| 9 | Discrete-tier regular grid (no tree) | RoadRunner M&M's own actual implementation choice (two discrete distance tiers, no tree); this project's own resolution-boundary experiment (§9 of that note) also implemented a discrete-tier (plus one graduated intermediate tier) scheme in a flat dict-keyed structure and measured it to be fast (24-38ms build time for ~15-20k points) and cheap; DIRECT EVIDENCE (own experiment) + DIRECT EVIDENCE (RoadRunner M&M). |
| 10 | Learned components | Metric-semantic mapping's (#2) own ablation: removing semantics causes a concrete misclassification failure (grass marked traversable) — DIRECT EVIDENCE that a learned semantic component solves a real, demonstrated failure mode. |
| 10 | Lightweight/classical components | 7 of 8 supplied papers use no learned component at all and still address their stated problem (terrain analysis, DATMO, mapping); RoadRunner's own design uses semantics only for *offline label generation*, not runtime inference — DIRECT EVIDENCE that a hybrid captures some learned-quality benefit without paying the runtime learned-inference cost. |

---

## 3. Evidence Against Each

| # | Direction | Strongest disconfirming / weakening evidence |
|---|---|---|
| 1 | Distance-driven | Does not by itself address small/distant-object loss — PointPillars' own stated limitation is exactly "distant/small-object information loss" under its fixed pillar grid, and the embedded voxel-efficiency paper (arXiv:2105.10316) found full-range models already "fail to detect distant small objects" even *before* any explicit coarsening — meaning some reported "savings" from range-restriction partly reflect objects already being missed, not efficiently handled. No paper found runs a controlled ablation isolating exactly how much accuracy distance-adaptivity costs vs. a fixed-fine baseline at the *same* memory budget. |
| 2 | Uncertainty-driven | MrHash's strongest result is from general 3D surface reconstruction (SDF variance), not 2.5D ground-vehicle terrain specifically — domain transfer is unconfirmed. For a ground vehicle, sensor geometry means distance and uncertainty are likely correlated (points sparser/noisier at range for geometric reasons alone), raising an unresolved question: does uncertainty add information *beyond* distance for this specific application, or mostly duplicate it? No direct ablation isolating this was found (see §9 below). |
| 3 | Semantic-aware | Neither Larsson et al. nor Stache et al. operate in the SIH's exact setting (full 3D octree / flat 2D UAV, not 2.5D ground-vehicle) — Gap 1, "likely genuine gap," meaning the *combination* is unvalidated, not just under-published. Running a semantic segmentation model to *decide* resolution creates a circularity risk: the model's own accuracy is itself resolution-dependent, and no paper found addresses running semantic inference at a deliberately coarse "scouting" resolution before committing to a fine allocation. |
| 4 | Object-aware | AdaOcc's dynamic-object tie could not be confirmed even after this phase's targeted follow-up (see §1.4) — the strongest existing example remains only partially characterized. Object-aware adaptivity requires an object detector to run *before* the resolution decision, at whatever resolution is currently available — the same circularity risk as direction 3, arguably worse since small/distant objects are exactly what coarse resolution already tends to miss (a self-defeating loop: coarse resolution may prevent detecting the very object that would justify refining that region). |
| 5 | Dynamic-object-aware | **Every one of the 23 MOS/scene-flow/DOGMa papers reviewed uses fixed spatial resolution** — a repeated, direct finding, not silence (DERIVED from the aggregate pattern). Funk et al. — a genuine persistent adaptive-resolution map — is *confirmed* to have **zero** dynamic-object handling (explicit static/quasi-static scope stated by its own authors), direct disconfirming evidence that at least one prominent adaptive-map system deliberately excluded this. |
| 6 | Multi-driver | **No paper found addresses driver-conflict arbitration** — what happens when distance says "coarsen" and semantics says "stay fine" for the same region has zero identified precedent, a stronger absence than any of the three originally-flagged gaps. MAP-ADAPT and Agile3D combine drivers that are largely complementary (semantic+geometry+compute; content+contention) rather than genuinely *competing* signals for the same cell — meaning even the existing multi-driver evidence may not transfer to a genuinely adversarial-driver scenario. |
| 7 | Persistent maps | This project's own resolution-boundary experiment (`resolution_boundary_consistency.md` §9) found that maintaining a persistent multi-tier map surfaces a real, measurable (if modest) discontinuity/consistency cost at tier transitions that a transient per-frame representation would not need to manage at all (no persisted boundary to become inconsistent over time). Persistent maps also require deciding how to age, decay, or re-partition previously-mapped regions as new data arrives — none of the reviewed persistent-adaptive-map papers report long-duration (multi-hour) overhead numbers (an identified gap in `03_paper_vs_sih_matrix.md`). |
| 8 | 2.5D | The supplied metric-semantic mapping paper's argument for full 3D is domain-specific (large-scale outdoor semantic navigation with presumably more complex vertical structure) — not established to generalize to a ground-robot terrain/object-perception setting where multi-level or overhanging structure is less central. |
| 9 | Octree/quadtree | This project's own literature investigation (`resolution_boundary_consistency.md`) found that a robotics multi-scale path-planning paper with neighbor-finding as a core topic (arXiv:1602.04800, directly re-verified via WebFetch) never addresses value-aggregation or consistency across a resolution boundary at all, despite using a tree structure — a hierarchy existing does not mean its boundary behavior was designed or validated. Real octree/sparse-voxel systems needed an explicit, non-default fix for this (interpolation-aware padding, ICCV 2021) — the "free" consistency sometimes assumed of tree structures is not automatic. |
| 9 | Discrete-tier grid | Coarser flexibility — cannot smoothly vary resolution, only jump between a small, fixed number of tiers; RoadRunner M&M itself only uses 2. This project's own experiment found a *naive* tier-boundary design produces measurable (if modest) elevation/occupancy/semantic artifacts (§9 of `resolution_boundary_consistency.md`), and its own tested consistency-mechanism fix was mixed (helped occupancy, *hurt* semantic mismatch in 6 of 7 configurations) — the simplicity of this structure does not come free of the boundary-consistency question either. |
| 10 | Learned components | RoadRunner's own design explicitly avoids runtime semantic inference (offline-only), and 7 of 8 supplied papers solve their stated problem with zero learned components — direct evidence a large fraction of this problem space does not strictly require learning. [NEW — see §1.10 for a deeper, sub-problem-by-sub-problem version of this comparison.] |
| 10 | Lightweight components | Metric-semantic mapping's own ablation is direct, demonstrated evidence that at least one specific, real failure mode (terrain misclassification) is NOT caught by a purely geometric/classical method — lightweight is not a free win either. **[NEW]** Classical clustering-based detection is explicitly self-limited by its own authors to sparse/simple scenes (parks, suburbs) and documented to weaken in dense/occluded/urban ones; EG-PointPillar shows classical geometric features *added to* a deep detector still improve KITTI mAP by +3.88% — i.e. even where lightweight works, it is often best used as a complement to a learned component, not a full substitute. |

---

## 4. Complexity / Cost Assessment

| # | Direction | Compute cost | Memory implications | Implementation difficulty | Real-time implications |
|---|---|---|---|---|---|
| 1 | Distance-driven | **Low** — a single range lookup/threshold, no extra sensing or model | Proven reduction (Adaptive-LIO, RoadRunner M&M) | **Low** — simplest of all drivers | Good; RoadRunner M&M and Adaptive-LIO both report real-time-capable operation |
| 2 | Uncertainty-driven | **Moderate** — requires maintaining a variance/confidence estimate per cell (extra state + update cost) | Strong proven reduction in its own domain (MrHash ~4x) | **Moderate** — needs a variance model (Kalman, SDF, or density-based proxy) | MrHash: up to 13x measured speedup (different domain); untested for 2.5D ground-vehicle terrain |
| 3 | Semantic-aware | **Moderate-High** — requires a running semantic segmentation model (typically a neural network) before the resolution decision | Not separately quantified in Larsson et al./Stache et al. at the access level obtained | **High** relative to distance — needs a trained/validated segmentation model plus resolution-policy logic on top | Latency only partially reported (Larsson et al.: "P" in the SIH matrix); not reported for Stache et al./MAP-ADAPT |
| 4 | Object-aware | **Moderate-High** — requires an object detector/proposal step before the resolution decision | Not separately quantified for AdaOcc at the access level obtained | **High** — same circularity concern as direction 3, plus object-detection infrastructure | Not reported at the access level obtained |
| 5 | Dynamic-object-aware | **Low-Moderate** for the mature MOS/scene-flow/DOGMa systems reviewed — several report real, measured FPS (4DMOS, Flow4D) on fixed-resolution representations | Not the primary reported metric in this lineage (perception-accuracy-focused, not memory-focused) | **Moderate** — mature, well-documented architectures exist to build from | Good for the mature fixed-resolution systems; unvalidated when combined with a persistent adaptive map (Gap 2) |
| 6 | Multi-driver | **High** — cost of every constituent driver, plus an arbitration/policy layer with no published design for conflicting signals | MAP-ADAPT/Agile3D report benefit, but neither isolates the memory cost of the arbitration layer itself | **Very High** — compounds each driver's own difficulty, plus an unsolved conflict-arbitration problem | Agile3D: real Jetson-measured gains; MAP-ADAPT: not reported at accessible level |
| 7 | Persistent maps | Ongoing per-frame update/merge cost across the whole trajectory | Must be bounded/managed over long deployments — no reviewed paper reports multi-hour overhead numbers (identified gap) | **Moderate-High** — insertion, merging, re-partitioning, and (per this project's own experiment) boundary-consistency logic | Real-time reported for short/typical evaluation windows only; long-duration behavior unvalidated |
| 7 | Transient representations | Recomputed each cycle — no accumulation cost, but also no memory of the past | Bounded by construction (nothing persists) | **Low-Moderate** — no cross-frame state machinery needed | Numerically the dominant pattern in the sparse-CNN and MOS/scene-flow literature, most of which report real-time numbers |
| 8 | 2.5D | Structurally cheaper — one value per (x,y) cell, not a volumetric stack | Structurally cheaper than 3D | **Low-Moderate** — mature, well-documented (Fankhauser lineage) | Good; RoadRunner/RoadRunner M&M report real-time operation |
| 8 | Full 3D | Structurally more expensive | Explicit limitation in metric-semantic mapping (#2): "GPU-memory-bound" | **Moderate-High** | <7ms/frame reported for metric-semantic mapping (#2), but GPU-dependent |
| 9 | Octree/quadtree | Tree traversal/insertion overhead; balancing/neighbor-finding adds real complexity (per this project's boundary-consistency findings) | Efficient once built (proven across OctoMap/MrHash/etc.) | **High** — correct neighbor-consistency handling is not automatic and was found absent-by-default in at least one reviewed system | Mature systems (OctoMap, MrHash) report good real-time numbers once implemented correctly |
| 9 | Discrete-tier grid | Minimal — no tree traversal, just a tier lookup | Less flexible than a full tree, but proven sufficient for RoadRunner M&M's use case | **Low** — this project's own experiment implemented and ran a working version quickly | This project's own experiment: 24-38ms build time for ~15-20k points, pure Python, no optimization |
| 10 | Learned | Highest per-component cost (neural inference); typically GPU-bound | Model weights + activation memory | **High** — training data, validation, generalization risk | Depends heavily on target hardware — this project's Phase 2 research repeatedly found theoretical compute reduction does not reliably predict measured speedup (SPVNAS, FALO) |
| 10 | Lightweight/classical | Lowest per-component cost; typically CPU-feasible | Minimal | **Low** | Predictable, hardware-portable — no learned-inference latency variance |

---

## 5. SIH Requirement Coverage

Columns condensed from the 16-requirement Gap Map to the ones each direction
most directly bears on. **Y** = directly addresses; **P** = partially/
indirectly; blank = not addressed by this direction alone.

| # | Direction | Terrain | Static obj. | Dynamic obj. | Adaptive res. | Memory eff. | Real-time | Novelty potential |
|---|---|---|---|---|---|---|---|---|
| 1 | Distance-driven | P | P | | Y | Y | Y | Low (well-established) |
| 2 | Uncertainty-driven | | P | | Y | Y | P | Moderate (domain transfer to 2.5D terrain untested) |
| 3 | Semantic-aware | Y | P | | Y | P | P | **High** — Gap 1, no 2.5D-ground-vehicle example found |
| 4 | Object-aware | | Y | P (unconfirmed) | Y | P | ? | Moderate-High (Gap 2 territory) |
| 5 | Dynamic-object-aware | | | Y | | | Y | Low (mature field) but **High** if combined with adaptive resolution (Gap 2) |
| 6 | Multi-driver | P | P | | Y | P | P | Moderate — Gap 3, but driver-conflict question unsolved anywhere |
| 7 | Persistent maps | Y | Y | | Y | ? (long-duration unproven) | P | Low standalone; necessary substrate for 1-4, 6 |
| 7 | Transient representations | | Y | Y | P | Y | Y | Low (dominant pattern already) |
| 8 | 2.5D | Y | Y | P | Y | Y | | Low (well-established) |
| 9 | Octree/quadtree | | | | Y | Y | P | Moderate (2.5D quadtree-with-height is itself a gap) |
| 9 | Discrete-tier grid | Y | P | | Y | Y | Y | Low (simple, already proven at RoadRunner M&M scale) |
| 10 | Learned components | Y | Y | Y | | | P | Low-Moderate (well-trodden, but real accuracy gains demonstrated) |
| 10 | Lightweight components | P | P | P | | Y | Y | Low, but demonstrably sufficient for a large fraction of the problem |

---

## 6. Simple-vs-Advanced Comparison

### The A-E ladder (single-driver → multi-driver)

**A. Distance-only adaptation.** Cheapest, best-evidenced (Adaptive-LIO,
RoadRunner M&M), directly matches the SIH's own stated example. Weakness:
does not use semantic or object information at all, so it cannot
distinguish "coarse because far and unimportant" from "coarse because far
but contains a critical thin obstacle."

**B. Uncertainty-only adaptation.** MrHash's result (~4x memory, up to
13x speedup) is the single strongest quantified number for any driver in
this project's entire search — but for a ground vehicle, distance and
uncertainty are plausibly correlated (sensor geometry drives both sparsity
and noise growth with range), so **it is not established that B captures
benefit beyond what A already provides for this specific application.** No
ablation isolating "uncertainty given distance is already known" was found
in the existing literature. **A dedicated search for driver-count
ablations was commissioned for this phase but was interrupted mid-task by
a platform rate limit before it could report a result** (see note at the
end of §6) — this specific question is therefore carried forward as an
open item, not answered either way, rather than assumed. Recommendation-
relevant reading in the meantime: B should be treated as a candidate
*refinement* of A, not a demonstrated independent win, until tested.

**C. Semantic/object-aware adaptation.** Larsson et al./Stache et al./
AdaOcc show this responds to information neither A nor B encode (class
identity, object presence) — the clearest case among all single-driver
options for genuinely *non-redundant* benefit. Cost: the highest of the
three (requires a running semantic/detection model). This is also, not
coincidentally, the direction the Gap Map identifies as the strongest
available novelty opportunity (Gap 1).

**D. Two-driver (e.g., distance + semantic).** MAP-ADAPT and Agile3D show
2-3-driver combination is tractable and beneficial in adjacent settings
(Agile3D: +7% accuracy, real Jetson hardware) — but **no paper combines
distance with semantics specifically**, and no ablation isolating the
second driver's marginal contribution in a directly comparable
adaptive-*mapping* setting was found. The incremental value of moving from
C to D is therefore a genuinely open empirical question, not something
that can be assumed large just because the individual drivers each work.

**E. Multi-driver (3+) policy.** MAP-ADAPT is the only 3-driver example
found, and even it does not include distance. Agile3D's RL-controller is a
template for *learning* the arbitration rather than hand-designing it, but
operates per-frame (transient), not on a persistent map — adapting it to a
persistent-map setting is itself an unvalidated research problem, and its
conflict-handling is implicit in learned weights rather than an
interpretable, checkable rule. **The step from D to E is the single
highest-risk, least-evidenced step in this entire ladder** — no published
work anywhere in this project's search addresses what to do when two
drivers disagree.

### Reading the ladder

Each additional driver's justification weakens as the ladder climbs: A is
necessary and well-justified; C adds evidenced, non-redundant value at a
real but bounded cost; B and D are *plausible* refinements with no direct
evidence of how much they add beyond a simpler alternative already in
place; E requires solving an unsolved problem (driver-conflict arbitration)
that no one has published a solution to. **The evidence does not support
assuming "more drivers is better" — it supports A as a floor, C as the
best-justified single addition, and treating B/D/E as needing their own
dedicated validation before being adopted, not as free upgrades.**

**Research-transparency note:** a targeted search for direct driver-count
ablations (isolating each added driver's marginal contribution within the
same system — e.g. re-checking MAP-ADAPT, Agile3D, and Larsson et al. for
such an ablation) and for persistent-vs-transient trade-off literature was
commissioned for this phase but was **interrupted mid-task by a platform
session rate limit** (it had located a relevant PDF and was about to read
it when it was cut off). Rather than retry immediately into the same limit
or fabricate a plausible-sounding result, this is reported honestly as
**incomplete**. The ladder reasoning above rests on the *absence* of such
an ablation in material already reviewed in Phase 2 (which remains valid —
no ablation of this kind was found there either), not on a confirmed
negative from a completed dedicated search this phase. Section 1.7 below
is likewise built from existing evidence only, not the interrupted new
search. Revisit both with a fresh, focused search in a later phase if
either question becomes load-bearing for the architecture decision.

---

## 7. Candidate Combinations Worth Considering

1. **Distance-tiered 2.5D elevation map (persistent) + a separate,
   fixed-resolution dynamic-object detection/tracking module running
   alongside it.** Matches the supplied papers' own pattern (motion grids
   #5 and evidential grids #6 already run a DATMO layer over/alongside a
   2.5D grid), matches the persistent-vs-transient analysis's natural
   split (§1.7), and is the lowest-risk combination that still satisfies
   the SIH's static+dynamic object-perception requirement. Complexity:
   **low-moderate**. Novelty: **low** (this pattern already exists), but a
   solid, defensible foundation.
2. **(1) + a semantic layer.** Two sub-options with very different risk/
   novelty profiles: (2a) MEM-style fixed-resolution semantic fusion
   (low risk, low novelty, proven pattern) or (2b) a genuinely
   semantic-*driven* resolution rule adapted from Larsson et al. to a 2.5D
   grid/quadtree (moderate-high risk, **high novelty** — this is Gap 1,
   the strongest identified gap in the entire project). (2b) is the
   clearest candidate for "one or two genuinely strong technical
   contributions" the research goal asks for.
3. **A simple discrete-tier structure (2-3 tiers, no full tree), per
   RoadRunner M&M's own choice and this project's own experiment**, rather
   than a full adaptive octree/quadtree. Lower implementation risk, avoids
   the tree-balancing and default-neighbor-consistency problems this
   project's own boundary investigation found unresolved by default in
   comparable tree structures elsewhere.
4. **A cheap feasibility check of a non-Cartesian (cylindrical/polar)
   coordinate frame** (Cylinder3D-style) as a partial, "free" substitute
   for or complement to an explicit distance-tiering rule, before
   committing to more custom logic — low cost, worth ruling in or out
   early.

---

## 8. Combinations That Appear to Be Overengineering

1. **Full multi-driver (distance + semantic + uncertainty + terrain-risk)
   arbitration policy**, attempted without first validating any single
   additional driver's marginal benefit over distance alone. No published
   precedent exists anywhere in this project's search for resolving
   conflicts between disagreeing drivers — this is not "more engineering
   effort," it is an open research problem being taken on as a side
   effect of a mapping-architecture decision.
2. **A full adaptive octree/quadtree combined with a from-scratch
   boundary-consistency mechanism**, when this project's own measured
   experiment found a simple, self-designed consistency mechanism gave
   *mixed* results (helped occupancy mismatch, worsened semantic mismatch
   in 6 of 7 tested configurations) at real implementation cost. Building
   a more elaborate version of a mechanism already shown not to reliably
   help, without new evidence it would behave differently, is exactly the
   kind of "impressive but unjustified" complexity the research goal asks
   to avoid.
3. **Fusing dynamic-object detection into the same adaptive-resolution
   mechanism as the static/terrain map** (Gap 2), attempted as a from-
   scratch unified design. Every existing near-miss either confirms
   exclusion of dynamic objects (Funk et al.), is access-limited/
   unconfirmed (AdaOcc), or is spatially uniform not spatially adaptive
   (MURAL) — there is no existing template to build from, and the SIH
   problem statement does not actually require a *unified* representation,
   only that both static and dynamic perception be solved. A separate-
   subsystem design (§7.1) satisfies the requirement at far lower risk.
4. **A learned (RL or neural) driver-arbitration controller for a
   persistent map**, modeled on Agile3D. Agile3D's own precedent is
   per-frame/transient; adapting its approach to a persistent map is an
   unvalidated research problem layered on top of the already-unvalidated
   multi-driver-arbitration problem — two open research questions taken on
   at once, for a combination whose base-rate benefit (§6, ladder step
   D→E) is itself unestablished.
5. **Full 3D volumetric representation** in place of 2.5D, without a
   SIH-specific justification (e.g., overhangs/tunnels/multi-level
   terrain) — adds substantial memory/compute cost for a capability the
   stated problem does not clearly require.

---

## 9. Strongest Remaining Technical Gaps

1. **Gap 1 — persistent 2.5D map + explicit semantic-class-driven
   resolution for a ground robot** — still the strongest, cleanest,
   best-supported gap (`03_paper_vs_sih_matrix.md`), and the best-evidenced
   candidate for a genuine technical contribution given this phase's
   analysis (§6, §7.2b).
2. **Driver-conflict arbitration** — completely unaddressed anywhere in
   this project's search; a real, structural risk for any multi-driver
   design (ladder step D→E, §6), not merely "more work."
3. **Whether uncertainty-driven adaptation offers benefit beyond what
   distance alone already captures**, for a ground vehicle specifically —
   unresolved; no direct ablation found isolating this (§1.2, §6-B).
4. **The persistent-vs-transient architectural split for combining
   static/terrain and dynamic-object perception has never been directly
   validated** as necessary or sufficient — every existing combination is
   either two glued-together separate systems (supplied papers) or a
   single system missing one side (Funk et al., AdaOcc, MURAL); no paper
   reports the measured cost of the interface between a persistent map and
   a transient dynamic-object module.
5. **Long-duration (multi-hour) overhead of a persistent adaptive map** —
   no reviewed paper reports this; all evaluation windows are short/
   single-session.
6. **This project's own resolution-boundary experiment result** is itself
   now a known, secondary-priority design constraint (not a primary
   research gap) — real, measurable, but modest, and any data-structure
   choice from §1.9 will need to account for it at build time, not treat
   it as solved.
7. See §1.4/§1.10 below for the two items this phase specifically
   targeted with new research.

---

## 1.4 — Targeted Follow-Up: Object-Aware and Dynamic-Object-Aware Adaptive Resolution

**AdaOcc's access gap is now resolved [NEW].** Full text obtained via
`arxiv.org/html/2408.13454` (HTML rendering succeeded where two prior
PDF-fetch attempts had failed). **Confirmed: AdaOcc's ROI mechanism is
object-detection-driven and motion-agnostic** — DIRECT EVIDENCE. It never
uses "dynamic," "moving," "static," or "motion" anywhere in its text; its
DETR-style 900-box regression covers all 10 nuScenes classes, including
explicitly static ones (barrier, traffic cone, construction vehicle);
prioritization is stated as proximity + foreground/background, not motion
state. **This is a real update to the Gap Map, not a neutral clarification:
it moves Gap 2 back toward "genuine gap"** rather than "potentially already
addressed" — the most promising existing near-miss is now confirmed *not*
to solve the dynamic-object tie (see `evidence/claims.md` for the sourced
update).

**Broader search results [NEW]**, kept strictly separate by category:

- **Object-presence-driven, motion-agnostic** (same category as AdaOcc):
  a WACV 2025 point-selection paper (arXiv:2508.01980, LiDAR-native,
  KITTI/nuScenes) biases sampling toward any detected object; a
  camera-based foreground-modulation paper (arXiv:2604.05780) shows a
  *quantified* result worth noting even though not LiDAR-native — DIRECT
  EVIDENCE: 71.9% GFLOPs reduction **and** +2.35 mIoU / +2.50 IoU accuracy
  *improvement* simultaneously versus dense/uniform processing, i.e.
  foreground-focused compute allocation is not a pure accuracy-for-speed
  trade — both moved the same direction in this one ablation.
- **Motion-aware but resolution-fixed — an important boundary case
  [NEW]:** S3PM (MDPI Sensors 2026, PMC12845740, camera/depth-based, real
  embedded-hardware numbers: Raspberry Pi 5 + Hailo-8 NPU, 25-30 Hz,
  18-27% higher IoU and 30-45% fewer collisions vs. OctoMap+RRT*) builds a
  motion/dynamics-aware **risk field** from optical flow around moving
  objects but deliberately never varies spatial resolution. **This is
  direct evidence that motion-awareness and resolution-adaptivity are
  separable design choices, not automatically bundled** — a system can be
  fully dynamic-object-aware without being resolution-adaptive at all, an
  option this project's own candidate-combination analysis (§7.1) already
  leans toward for exactly this reason.
- **Resolution-adaptive but driven by neither objects nor motion:**
  MR3D-Net (arXiv:2408.06137, bandwidth-driven, up to 94% bandwidth
  reduction for collective perception) and MURAL (arXiv:2607.08391,
  deadline/ego-speed-driven, confirmed uniform-per-frame not spatial) — both
  contrast cases confirming multi-resolution LiDAR representations are an
  active research area along axes unrelated to object/motion content.
- **A genuinely disconfirming-adjacent finding:** Dynamic Lambda-Field
  (arXiv:2103.04795) explicitly targets the problem that "the probability
  of collision becomes dependent on the tessellation size" in a standard
  occupancy grid — and its chosen fix is a **continuous, tessellation-
  independent risk field**, i.e. removing resolution-dependence rather
  than embracing adaptive resolution. This is weak circumstantial evidence
  (INFERENCE, not a stated argument against adaptive resolution) that at
  least one research line views grid-resolution-dependence itself as a
  liability to be designed away, not a knob to be tuned.
- **Access-limited residual gap, same category as the original AdaOcc
  problem:** "Adaptive Voxelization Strategy for 3D Object Detection"
  (IEEE doc 9869047) claims object-aware adaptive voxel sizing but remains
  paywalled; not resolved in this phase.
- **Disconfirming-evidence search, explicit result:** no paper was found
  demonstrating object-aware adaptive resolution failing, underperforming,
  or being abandoned for a simpler alternative on real hardware. Reported
  per this project's standing rule as **"not found in the literature
  searched,"** not as proof such evidence doesn't exist — negative results
  are structurally underreported, so this absence is weaker than a
  positive finding would be.

**Net effect on Gap 2 and direction 4/5:** object-aware (direction 4) and
dynamic-object-aware (direction 5) adaptive resolution remain **empirically
un-unified** in the literature searched across two full passes (Phase 2 and
this phase) — every candidate either lacks the motion tie (AdaOcc, the
WACV 2025 paper), lacks the resolution-adaptivity (S3PM), or adapts
resolution for an unrelated reason (MR3D-Net, MURAL). Gap 2 stands as a
genuine gap, now on firmer evidential footing than the "potentially
genuine" classification from the earlier synthesis checkpoint.

## 1.10 — Targeted Follow-Up: Lightweight vs. Learned Perception Components

New research [NEW] was run per sub-problem, with primary-source numbers
where possible (evidence levels per-claim as stated).

**Terrain/traversability — conditionally sufficient with a narrow, well-
defined gap.** Classical geometric ground-segmentation methods are fast and
accurate: Patchwork++ reaches 96.51% F1 at 54.85 Hz (DIRECT EVIDENCE,
arXiv:2207.11919), and ground segmentation alone removes 50-60% of points
before any further processing (DIRECT EVIDENCE, arXiv:2312.16839). The same
survey explicitly argues classical methods generalize *better* out-of-
distribution than learned ones, which risk "catastrophic failure" under
train/test domain shift — a real, cited disconfirming point against
defaulting to learned terrain classification. The one consistently repeated
counter-finding across independent sources: **geometry alone cannot
distinguish compliant vegetation (grass) from rigid obstacles** — directly
consistent with this project's own already-known finding (metric-semantic
mapping's ablation: grass misclassified as traversable without semantics)
and with RoadRunner's resolution of using semantics for *offline* label
generation rather than discarding it. Net: lightweight suffices for the
geometric core; a narrow semantic patch is needed specifically for
vegetation ambiguity, not a wholesale case for either extreme.

**Static-object/semantic segmentation — the weakest direct comparison
found, but a clear structural signal.** Rule-based classification hits
&gt;98.5% accuracy for large, simple, geometrically regular classes
(buildings, poles, vegetation, vehicles — WEB VERIFIED, moderate confidence,
snippet-corroborated not independently opened in full). No controlled
classical-vs-learned mIoU comparison on a shared ground-vehicle benchmark
was found in either search pass — an explicit, honestly-reported gap, not
papered over. The recurring pattern across independent sources is a
**class-conditional hybrid**: rule-based for large/simple structures,
learned for complex/fine-grained classes — not a single global choice.

**Dynamic-object detection + tracking — the sharpest, best-evidenced split
found in this entire project.** Tracking-given-detections: two independent,
recent (2024), full-text-verified papers directly benchmark a classical
Kalman-filter-family tracker against a learned tracker (PolarMOT) on the
same real dataset. **RobMOT** (arXiv:2405.11536) beats or matches PolarMOT
on KITTI/Waymo while running at **3,221 FPS on a single CPU core, no GPU**
— DIRECT EVIDENCE, the single most concrete "lightweight achieves the
learned benefit at a fraction of the cost" finding in this whole project.
**Spb3DTracker** (arXiv:2408.05940) independently confirms the pattern
(sAMOTA 99.27 vs. PolarMOT's 94.08 on KITTI pedestrian tracking). Both
required real engineering beyond a textbook Kalman filter (adaptive
covariance, dynamic UKF) to get there — not a trivial default. Detection
itself shows the opposite lean: classical clustering (DBSCAN-family) is
explicitly self-limited by its own authors to sparse/simple scenes and
documented to struggle in dense/occluded/urban ones; **EG-PointPillar**
shows adding classical geometric features to a deep detector improves KITTI
mAP by +3.88% — evidence that classical signal is a valuable *complement*
to a learned detector, not a substitute for one.

**Cross-sub-problem synthesis:** the evidence does **not** support a single
lightweight-vs-learned answer for this project. It supports a differentiated
design: lightweight-sufficient for terrain geometry and for tracking-given-
detections; a narrow, specific, well-evidenced learned component needed for
vegetation-ambiguity in terrain and for object detection in dense/occluded
scenes; and a genuinely open, unresolved question for general static-object
semantic segmentation (no controlled comparison exists either way in the
literature searched).

---

## 10. Three-to-Five Credible System-Level Solution Candidates

No winner is selected — this is a comparison, not a recommendation. Every
candidate shares two design decisions the evidence above supports across
the board: a **persistent 2.5D representation** for terrain/static content
(§1.8, well-solved, structurally cheaper than 3D, no SIH-specific case for
volumetric representation found) and a **separate, non-unified subsystem
for dynamic-object detection/tracking** (§1.5/1.7/1.4, matching the
supplied papers' own pattern and avoiding Gap 2's unvalidated-unified-
mechanism risk). They differ in how much further they go.

### Candidate 1 — Minimal Distance-Tiered Baseline
Persistent 2.5D elevation/occupancy map with 2-3 discrete distance tiers
(RoadRunner-M&M-style, no tree structure — matches this project's own
resolution-boundary experiment, which found this cheap and fast to build).
Terrain: classical ground-segmentation + slope/roughness (Patchwork++-
style). Static objects: classical clustering. Dynamic objects: classical
clustering + Kalman-filter tracking (RobMOT-style engineering), as a
separate real-time module. No semantic-driven or uncertainty-driven
resolution; no multi-driver arbitration.

### Candidate 2 — Distance + Narrow Semantic Patch
Same backbone as Candidate 1, plus a semantic segmentation model used
RoadRunner-style — to *improve terrain-classification accuracy* (resolving
the one well-evidenced classical failure mode: vegetation vs. rigid
obstacles) and to help dense/occluded-scene object detection — without
using semantics to drive resolution. Resolution stays distance-only.
Dynamic-object tracking still classical (RobMOT-style) on top of a learned
detector.

### Candidate 3 — Semantic-Driven 2.5D Adaptive Resolution (novelty-focused)
Persistent 2.5D grid/quadtree where resolution is driven by **both**
distance (coarse prior) **and** an explicit semantic-class-weighted rule
adapted from Larsson et al.'s objective to a 2.5D structure — directly
targets Gap 1, the strongest identified gap and clearest novelty
opportunity in the entire project. Dynamic objects remain a separate
subsystem (as in all candidates). This is a deliberate two-driver (not
full multi-driver) design, stopping at ladder step D rather than E.

### Candidate 4 — Uncertainty-Refined Adaptive Map
Persistent 2.5D map with distance-based base tiers, refined locally by an
uncertainty/variance signal (MrHash-style, adapted from SDF-variance to
elevation/occupancy-variance) wherever repeated observations disagree.
Directly tests the open question of whether uncertainty adds value beyond
distance for this application (§6-B) rather than assuming it does.

### Candidate 5 — Multi-Driver Adaptive Map with Learned Arbitration (high-risk/advanced)
Distance + semantic + uncertainty combined via a hand-tuned or lightly-
learned arbitration policy (Agile3D-inspired, adapted from its transient/
per-frame origin to a persistent map). Explicitly inherits the two least-
evidenced risks in this document: driver-conflict arbitration (zero
published precedent, §8.1/§9.2) and persistent-map adaptation of a
template only validated in a transient setting (§8.4).

| Candidate | SIH fit | Technical depth | Expected performance | Computational feasibility | Implementation complexity | Novelty potential | Risk |
|---|---|---|---|---|---|---|---|
| 1. Minimal distance-tiered baseline | High — covers every stated requirement at a basic level | Low-Moderate | Solid, bounded by well-understood classical-method limits (dense/occluded scenes, vegetation ambiguity) | High — every component has real, low-cost, CPU-feasible precedent (RobMOT: 3,221 FPS CPU-only) | Low | Low | Low |
| 2. Distance + narrow semantic patch | High | Moderate | Improved over (1) specifically on terrain vegetation-ambiguity and dense-scene detection — both narrow, well-evidenced gaps | Moderate-High — one learned component, GPU desirable but not exotic | Low-Moderate | Low-Moderate | Low |
| 3. Semantic-driven 2.5D adaptive resolution | High, and the only candidate to close a named gap (Gap 1) | High | Unvalidated for this exact combination — mechanically plausible per Larsson et al.'s own description, not demonstrated | Moderate — adds resolution-policy logic on top of an already-required semantic model | Moderate-High | **High** — best-evidenced genuine gap in the project | Moderate — plausible-but-unattempted, not fundamentally blocked per `04_paper_vs_paper_matrix.md` §3 |
| 4. Uncertainty-refined adaptive map | Moderate-High | High | Unvalidated whether it beats (1)/(2) — the central open question of §6-B | Moderate — extra per-cell state and update cost | Moderate-High | Moderate | Moderate — real chance the added mechanism proves redundant with distance for this application |
| 5. Multi-driver + learned arbitration | Moderate — technically comprehensive but unproven where it matters most | Highest | Unknown — no comparable system exists to extrapolate from | Lowest of the five — most moving parts, least precedent | Highest | High, but conflated with high execution risk | **Highest** — compounds two unsolved problems (driver-conflict arbitration, persistent-map controller adaptation) at once |

---

## 11. Architecture-Selection Evidence Checkpoint (2026-09-06)

Resolves three specific evidence gaps this document itself identified
(§6, §9), via one small deterministic experiment (Parts 1-2) plus a
targeted synthesis of research already gathered (Part 3, no new broad
search per the instruction for this checkpoint). No architecture is
selected. No SIH pipeline is implemented.

### Part 1 — Driver-count ablation (own experiment)

**Design.** A single synthetic scenario, three deterministic (non-learned)
policies, no arbitration logic beyond simple rule layering:
- **A (distance-only):** fine within R_b=10m, coarse beyond.
- **B (+semantic):** A, plus force-fine inside a designated "critical"
  semantic patch (x∈[13,15], y∈[-1,1], beyond R_b) containing a test pole.
- **C (+uncertainty):** B, plus force-fine inside any coarse-candidate
  cell whose sampled ground-point height variance exceeds a fixed
  threshold — a deterministic statistical rule, not a learned signal.
  Tested against an independent "sensor-noise anomaly" patch
  (x∈[17,19], y∈[-4,-2], 4x baseline measurement noise) deliberately
  placed outside both the distance-fine region and the semantic-critical
  patch, so only C's own logic can catch it.

Code: `../experiments/driver_ablation_experiment.py`. Raw output:
`../experiments/results/driver_ablation_results.json`. All numbers below
are exact script output — DIRECT EVIDENCE (this project's own experiment).

**Results.**

| Metric | A | B | C |
|---|---|---|---|
| Overall elevation MAE (m) | 0.0065 | 0.0066 | 0.0073 |
| Critical-region allocation-correct rate | 0.0 | **1.0** | 1.0 |
| Critical-region elevation MAE (m) | 0.0042 | 0.0099 | 0.0099 |
| Anomaly-region allocation-correct rate | 0.0 | 0.0 | **0.88** |
| Anomaly-region elevation MAE (m) | 0.0098 | 0.0098 | **0.0423** |
| Test-pole cell size at object location (m) | 0.8 (coarse) | **0.2 (fine)** | 0.2 (fine) |
| Total cell count (memory) | 1,534 | 1,621 (+5.7%) | 1,716 (+6.2% over B) |
| Build time (ms, ~4,600 pts) | 12.55 | 15.11 (+20%) | 19.59 (+30% over B) |
| Extra fine cells landing on genuinely important content | — | **100%** (89/89) | 79.8% (83/104) |

**Reading B (semantic) — real, well-targeted, low-cost benefit.** B fully
corrects the critical region's allocation (0.0→1.0) and tightens the test
object's positional resolution 4x (0.8m→0.2m cell) for a 5.7% memory and
~20% build-time cost, with **100% of its added fine cells landing on
genuinely important content** in this test. **Caveat:** this 100% figure
uses ground-truth semantic labels; a real segmentation model's false-
positive rate would erode it, and is not measured here. Critical-region
elevation MAE actually got *worse* under B (0.0042→0.0099) — fewer points
per fine cell average out sensor noise less than the fewer, bigger coarse
cells did; B's benefit is in allocation-correctness and object-precision,
not raw single-frame elevation accuracy. **Verdict: justified.** The added
complexity (one semantic lookup, layered on the existing distance rule) is
low, and the benefit is real, targeted, and directly relevant to the SIH's
own concern about losing detail on important-but-distant content.

**Reading C (uncertainty) — real but narrow, mixed, and costly enough to
warrant elimination from the core design for now.** C does catch the
anomaly (0.88 allocation-correct) that neither A nor B would — a genuinely
non-redundant signal in this configuration (the normal-map distance-vs-
uncertainty correlation was weak, −0.197, INFERENCE-level for
generalization beyond this one synthetic terrain). But: (a) refining
resolution there made the elevation estimate **worse, not better**
(0.0098→0.0423 MAE) — fewer points per fine cell in a genuinely noisy
patch means less noise-averaging, a real and somewhat counter-intuitive
cost; (b) its targeting efficiency (79.8%) is meaningfully worse than B's
(100%) — a real false-positive rate from a simple variance threshold; (c)
it costs a comparable memory/latency increment to B (+6.2% cells, +30%
build time on top of B) for a benefit that is about *flagging* low-
confidence regions, not improving them. **Verdict: insufficient benefit
to justify inclusion in the core resolution policy as implemented.**
Per the instruction to explicitly eliminate a driver whose evidence doesn't
support it: **driver C (uncertainty-driven resolution *refinement*) is
eliminated from further consideration for this architecture.** This does
not eliminate uncertainty-*awareness* as a concept — it eliminates the
specific mechanism tested (spatial refinement in response to variance) as
an accuracy-improving move; a different mechanism (e.g. flagging a region
for re-observation rather than subdividing it) was not tested and remains
a distinct, untested idea outside this checkpoint's scope.

**Ladder outcome:** A→B is justified; B→C is not, on the evidence gathered
here. This directly answers §6's open question ("does uncertainty add
value beyond distance") for *this specific mechanism* — evidence obtained
this phase — with a qualified no; it does not resolve the general question
for every possible uncertainty-response design.

### Part 2 — Semantic-driven 2.5D feasibility (own experiment + existing research)

The Part 1 experiment is itself a small, working, concrete feasibility
demonstration of exactly this question — not merely a theoretical argument.
Answering the five specified sub-questions directly:

- **What semantic information is actually required?** A single binary
  "functionally important" label per location — not Larsson et al.'s full
  continuous β/γ-weighted pruning objective. The deliberately simplest
  possible rule (`if important: force fine`) was sufficient to demonstrate
  the mechanism works. DIRECT EVIDENCE (own experiment): the simple version
  was not shown to be insufficient, so per the instruction not to invent
  complexity the evidence doesn't require, **the simple binary rule, not
  Larsson et al.'s full formalism, is what this checkpoint recommends
  carrying forward as the starting point.**
- **How does semantic information change resolution?** As an override
  layered on top of the distance rule — not a restructuring of it. Distance
  sets a default; semantics can only push a cell *finer* than the default,
  never coarser, in the design tested.
- **Can it operate without a complex hierarchy?** **Yes — confirmed
  directly.** The implementation is a flat, dict-keyed, non-tree, two-
  (then three-) tier grid. No octree/quadtree was needed. This directly
  answers Gap 1's open mechanical question with a positive, if small-scale,
  DIRECT EVIDENCE result, where before only INFERENCE ("mechanically
  plausible per the paper's own description") was available.
- **Does semantic refinement cause instability or excessive cell growth?**
  Growth was bounded and modest (+5.7% cells for a patch spanning ~2m×2m of
  a 22m×11m world) — proportional to the size of the important region, not
  unbounded. **Temporal instability was not tested** — this experiment
  used static, noise-free ground-truth semantic labels; a real classifier's
  frame-to-frame label noise could cause resolution to flicker in a way
  this experiment cannot speak to. Flagged explicitly as untested, not
  assumed safe.
- **Is the result compatible with terrain, static objects, and dynamic
  objects?** Terrain: yes, demonstrated (elevation still computed per cell
  at whichever resolution applies). Static objects: yes, demonstrated (the
  test pole remained detectable, with tighter positional precision).
  Dynamic objects: **not tested in this experiment** — this checkpoint's
  design keeps dynamic-object perception as a separate subsystem (per §7,
  §10 of this document), so compatibility here means "does the semantic-
  driven static/terrain grid interfere with a separate dynamic-object
  module's ability to run alongside it," which was not directly exercised.
  INFERENCE, not DIRECT EVIDENCE: no structural conflict is apparent, but
  this has not been built and tested.

**Verdict: mechanically feasible, at a basic level, now with a concrete
(if small-scale, synthetic) demonstration rather than only a plausibility
argument.** This resolves Gap 1's central open mechanical question. It
does **not** establish feasibility with a real (non-ground-truth, noisy,
frame-to-frame) semantic classifier, nor joint operation with a real
dynamic-object subsystem — both remain open items for a later, larger-scale
experiment before this becomes a load-bearing architecture decision.

### Part 3 — Classical vs. learned static-object perception

Built from research already gathered in the immediately preceding
candidate-solution-analysis phase (`§1.10` above) — no new broad search was
run for this checkpoint, per the instruction to resolve existing gaps
rather than re-survey.

**The evidence is insufficient to support a confident, general claim
either way — this is stated explicitly, not glossed over.** No paper found
in either research pass directly benchmarks a classical clustering-based
detector against a deep 3D detector on the same LiDAR dataset with both
accuracy and latency reported (§1.10, "Head-to-head" for the detection
sub-problem). What the evidence *does* support, narrowly:
- Classical clustering-based detection (DBSCAN-family) achieves real,
  measured performance (94.47% recall, 20 FPS — PMC11359795) but is
  **self-limited by its own authors** to sparse/simple scenes (parks,
  suburbs, countryside), with an explicit, stated admission of weaker
  performance in dense/occluded/urban settings.
- Classical geometric features **added to** a deep detector (EG-PointPillar)
  improve KITTI mAP by +3.88% over the deep-only baseline — direct evidence
  the classical signal is *complementary*, not redundant with what a deep
  network already learns, which argues against "classical alone matches
  learned" as a general claim.
- This is a different sub-problem from *tracking*, where the evidence was
  strong and direct (RobMOT, Spb3DTracker — §1.10 above): tracking-given-
  detections and static-object detection should not be conflated, and are
  not conflated here.

**Conclusion and confidence: classical-only static-object detection is
plausible for low-complexity deployment scenarios (sparse, open,
suburban/rural-like environments matching the scope its own proponents
claim) but is not evidenced as sufficient for dense or occluded scenes, and
a hybrid (classical geometric preprocessing feeding or complementing a
learned detector) is the more evidence-backed default given the
EG-PointPillar finding.** Confidence in this conclusion: **moderate** — it
rests on real measured numbers, but the absence of any direct controlled
comparison means the true accuracy gap between pure-classical and
pure-learned detection, on a shared benchmark, remains genuinely unknown.
This should not be read as "classical is sufficient" (explicitly the
inference the instructions warned against drawing merely because classical
is cheap) — it is read as "classical's scope of proven sufficiency is
narrower than the SIH's likely full operating envelope, and the safer
evidence-backed default is a hybrid, not a pure choice either way."

### What this checkpoint eliminates and what remains

- **Eliminated:** driver C (uncertainty-driven spatial resolution
  *refinement*, as tested) from the core resolution policy — Part 1.
  Candidate 4 (§10) is downgraded accordingly: it is not eliminated
  outright (a different uncertainty-response mechanism was not tested),
  but its core premise (refine resolution when uncertain) did not survive
  this experiment's evidence.
- **Eliminated:** pure-classical-only static-object detection as a
  *confident, general-purpose* choice — Part 3. Not eliminated as
  infeasible, but no longer a low-risk default; a hybrid is preferred on
  current evidence.
- **Strengthened, not eliminated:** distance+semantic (driver B) as the
  core resolution policy, and Candidate 3 (§10, semantic-driven 2.5D
  adaptive resolution) as the leading novelty-focused candidate — this
  checkpoint provides the first concrete (if small-scale) mechanical
  feasibility evidence for it, upgrading it from "plausible per inference"
  to "demonstrated at basic scale."
- **Still open:** temporal stability of semantic-driven resolution under a
  real (noisy) classifier; joint operation with a separate dynamic-object
  subsystem; the true classical-vs-learned accuracy gap for static-object
  detection on a shared benchmark; whether a non-refinement uncertainty-
  awareness mechanism (e.g. confidence flagging without resolution change)
  would fare better than the one eliminated here.

---

## 12. Semantic-Resolution Temporal-Stability Checkpoint (2026-09-06)

Resolves §11's single remaining open risk for Candidate 3: does distance+
semantic resolution stay useful when the semantic input is realistically
noisy and changes frame-to-frame? One experiment, extending §11's own
script rather than a new framework.

**Design.** Same static world, terrain, critical patch, pole, and sensor
model as `driver_ablation_experiment.py` (imported directly, not
reimplemented). Only one variable changes across 30 simulated frames of
the *same, unmoving* scene: whether the semantic prediction for each
coarse-tier candidate cell (360 cells beyond R_b, 6 of them truly
"critical") is perfect/stable, or noisy and independently redrawn each
frame. Code: `../experiments/semantic_noise_stability_experiment.py`.
Raw output: `../experiments/results/semantic_noise_stability_results.json`.

**Noise model.** Each candidate cell's per-frame predicted label is
correct with probability P_CORRECT, independently redrawn every frame —
**DERIVED**, calibrated to a real reported LiDAR semantic-segmentation
accuracy figure already in this project's evidence base (LVCA-Net, 91.79%
overall accuracy on SemanticKITTI, §1.10 above), not an invented number.
Two levels tested: realistic (P=0.90) and optimistic (P=0.95). This is a
deliberate **worst-case stress test**: independent per-frame flips are
harder to smooth than a real classifier's likely spatially/temporally
*correlated* errors would be — flagged explicitly as a limitation, not
hidden (see "remaining uncertainty" below). No neural network was built;
this is a controlled statistical noise model over an already-computed
ground-truth label, exactly as instructed.

**Results (P=0.90, DIRECT EVIDENCE — own experiment):**

| Policy | Mean fine-cell count | Std (memory instability) | Tier flips / transition / cell | Critical-region correct (all 6 cells, per frame) | Pole correct (per frame) | False-positive rate (normal cells) | Build time (ms) |
|---|---|---|---|---|---|---|---|
| A (distance-only) | 1,543 | 0 | 0 | 0% | 0% | 0% | 10.29 |
| B (perfect semantic) | 1,617 (+4.8%) | 0 | 0 | 100% | 100% | 0% | 10.27 |
| **C_raw (noisy, no smoothing)** | 2,010 (**+24% over B**) | 70.5 | **17.7%** | 53.3% | 93.3% | 9.75% | 10.66 |
| **C_hyst, K=3** | 1,626 (+0.5% over B) | 27.7 | **0.23%** | 83.3% | 93.3% | 0.37% | 11.27 |
| C_hyst, K=5 | 1,604 (−0.8% vs B) | 25.0 | 0.06% | 70.0% | 86.7% | 0% | 11.66 |

(Optimistic P=0.95 shows the same pattern at reduced severity: raw churn
9.6%/transition/cell, K=3 hysteresis brings it to 0.1% with 90%
critical-region and 93.3% pole coverage — full numbers in the JSON.)

**1. How often do cells switch unnecessarily?** Without smoothing, **~1 in
6 candidate cells changes tier on every single frame transition** (17.7%
at P=0.90) — validated against theory: the observed critical-region
"all-6-correct" rate (53.3%) matches 0.9⁶=53.1% almost exactly, confirming
the simulation behaves as designed, not as an artifact.

**2. Memory/cell-count variation this causes.** Raw noisy semantics
inflates mean map size **24% above the perfect-label case** (2,010 vs
1,617 cells) with a large frame-to-frame standard deviation (70.5 cells) —
a real, non-hypothetical memory-stability problem, driven almost entirely
by false positives on cells that were never actually important (9.75% of
normal cells flagged fine per frame, matching the ~10% injected noise rate
almost exactly).

**3. Does semantic noise cause unstable refinement/coarsening?** **Yes,
clearly and substantially**, without mitigation. Raw noisy semantic-driven
resolution is not adequate to use as-is.

**4. Is temporal smoothing/hysteresis necessary?** **Yes** — the evidence
does not support skipping it.

**5. Simplest mechanism that works.** A **symmetric K=3 consecutive-frame
persistence counter** (a cell only switches tier after K same-valued
predictions in a row, in either direction) — the simplest hysteresis
mechanism possible, a plain per-cell integer counter, no learning, no
per-cell probability model. It cut tier flips **~77x** (17.7%→0.23% per
transition), cut the false-positive rate **~26x** (9.75%→0.37%), and
brought mean memory use to within **0.5% of the perfect-label case**
(1,626 vs 1,617 cells), while still catching the true critical region in
83.3% of frames and the pole in 93.3% — at the cost of a small ramp-up
delay (critical region first fully correct at frame 5, pole at frame 2,
out of 30) and a **negligible build-time overhead** (10.3ms→11.3ms, +9%).
K=5 over-smooths: marginally lower churn than K=3 but a real, unnecessary
coverage cost (70.0%/86.7% vs 83.3%/93.3%) and longer delay — **K=3 is the
better-justified choice of the two tested, not K=5.**

**Downstream occupancy/semantic/object effects.** Not re-measured
per-frame in this checkpoint (would have meant re-running §11's full
elevation/occupancy pipeline 30x per policy for limited new insight, given
the scope constraint to keep this experiment small). **INFERENCE**, not
separately measured: since C_hyst(K=3)'s fine-cell count and critical/pole
coverage converge closely to B's, the downstream accuracy effects already
measured for B in §11 (allocation-correctness benefit, no meaningful
elevation-accuracy improvement, tightened object localization) should
transfer approximately — this is an extrapolation from the convergence
shown above, not a separately confirmed result, and is flagged as such.

**7. Added cost of the fix.** Per-cell state: one integer streak-counter
and one boolean streak-value, plus one boolean locked-in state — three
small fields per candidate cell, ~360 cells in this test scenario. Compute:
+9% build time in this synthetic prototype. Both are small relative to the
churn/memory problem they solve.

**8. Does semantic-driven adaptation remain viable?** **Yes — conditionally.**
Raw/unsmoothed semantic-driven resolution is **not** viable (24% memory
bloat, 17.7% per-transition churn, unreliable full-region coverage).
**With a simple K=3 hysteresis layer, it is viable** — the benefit
demonstrated in §11 survives realistic semantic noise, recovering to
within 0.5% of the perfect-label memory footprint at negligible added
compute cost. **Candidate 3 is not downgraded, but its definition is
revised**: it must include temporal hysteresis on the semantic driver as a
required component, not an optional refinement — a bare semantic override
(as tested in §11 Part 1/2, using stable ground-truth labels) is now known
to be insufficient for a real, noisy classifier.

**9. Candidates 1 vs. 2 vs. 3 after this experiment.** Candidate 1
(distance-only) is unaffected — it never touches this risk. Candidate 2
(distance + a narrow, offline/RoadRunner-style semantic patch that does
*not* drive resolution) is also largely unaffected, since it never
translates noisy per-frame semantic predictions into resolution changes in
the first place — this checkpoint is further, if indirect, evidence for
Candidate 2's inherent robustness relative to Candidate 3's added
machinery. **Candidate 3 remains viable but is now more precisely
specified**: distance + semantic-driven resolution **+ a mandatory K≈3
hysteresis stabilizer**, at a documented, small, now-measured cost (+9%
latency, converges to ~+0.5% memory over the no-noise ideal) rather than
the previously-assumed near-zero cost.

**10. Remaining uncertainty.** The noise model tested is **independent
(IID) per-frame flips — a stress test, not a validated model of real
classifier error correlation.** A real semantic segmentation model's
errors are plausibly spatially/temporally *correlated* (a genuinely
ambiguous region may be confidently misclassified for many consecutive
frames, not flicker randomly) — under such correlated errors, hysteresis
could behave differently: it might lock onto an *incorrect* state for an
extended period rather than filtering out a real, short-term signal loss.
**This is untested and is the most important remaining uncertainty before
Candidate 3's stabilization mechanism can be trusted with a real
classifier's actual error pattern**, as opposed to this checkpoint's
statistically-idealized IID noise proxy.
