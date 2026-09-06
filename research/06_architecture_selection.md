# 06 — Architecture Selection Analysis

Status: Final pre-implementation decision analysis. Built entirely from
research already completed (`02_technical_taxonomy.md` through
`05_candidate_solution_analysis.md`, `resolution_boundary_consistency.md`,
`evidence/claims.md`, `evidence/unresolved_questions.md`,
`external_literature/00_inventory.md`). No new literature search, no new
experiment, no implementation. This is a decision document, not the final
architecture specification — that follows a later, separate phase.

---

## 1. Candidates under evaluation

- **Candidate 1 — Distance-tiered 2.5D baseline.** Persistent 2.5D grid,
  2-3 discrete distance tiers, no tree structure. Pure classical
  perception throughout (geometric terrain classification, clustering-
  based static/dynamic detection, Kalman-filter tracking).
- **Candidate 2 — Distance + narrow semantic refinement, hybrid
  perception.** Same 2.5D backbone and distance-only resolution as
  Candidate 1. Adds one semantic segmentation model used to (a) fix the
  one clearly-evidenced classical terrain failure mode (vegetation vs.
  rigid obstacle ambiguity) and (b) assist static-object detection in
  dense scenes, per the hybrid pattern Part 3 of the previous checkpoint
  found best-evidenced. Semantics does **not** drive resolution.
- **Candidate 3 — Semantic-driven adaptive 2.5D resolution.** Everything
  in Candidate 2, plus resolution is driven by distance (prior) **and** a
  binary semantic-class override (force-fine on designated important
  content), stabilized by a mandatory K≈3 hysteresis counter. Directly
  targets Gap 1 (persistent 2.5D + semantic-driven resolution for a ground
  robot) — the best-evidenced genuine gap identified across the ~112-paper
  literature review.

All three share, by design, the same resolution to Gap 2 (adaptive
resolution + dynamic-object perception): dynamic-object detection/tracking
remains a **separate subsystem**, never fused into the terrain/static
adaptive-resolution mechanism. No paper reviewed validates a unified
mechanism, and this project's own research found no reason the SIH
requirements demand one — a separate subsystem satisfies "detect and track
dynamic objects" without inheriting an unsolved research problem.

---

## 2. Evaluation against SIH requirements

| Requirement | Candidate 1 | Candidate 2 | Candidate 3 |
|---|---|---|---|
| Terrain analysis | **Moderate** — classical geometry only; the one clearly-evidenced classical failure mode (vegetation vs. rigid obstacle) is unaddressed (metric-semantic mapping's own ablation, DIRECT EVIDENCE) | **High** — semantic layer directly patches that failure mode | **High** — same terrain approach as C2; resolution mechanism doesn't independently improve terrain classification quality |
| Static obstacle detection | **Moderate-Low** — pure classical clustering, self-limited by its own authors to sparse/simple scenes (94.47% recall there; PMC11359795) | **High** — hybrid, matches EG-PointPillar's +3.88% mAP additive evidence | **High**, plus a measured edge for objects in semantically-flagged classes: 4x tighter positional resolution (0.8m→0.2m cell) demonstrated in the driver-ablation experiment |
| Dynamic object detection | **Moderate** — tracking-given-detections is strongly evidenced classical (RobMOT: 3,221 FPS CPU-only, matches/beats a learned tracker), but detection itself inherits C1's classical-detection risk | **Moderate-High** — same tracking, hybrid detection | **Moderate-High** — identical to C2 (dynamic-object handling does not differ across candidates by design) |
| Adaptive spatial representation | Present, single-driver (distance only) | **Same as C1** — resolution is still distance-only in C2, by design | **Most capable** — distance + semantic, the only candidate matching the SIH's full "adaptive spatial representation" ambition beyond the literal distance example |
| 2.5D elevation information | High — tie | High — tie | High — tie |
| Memory reduction | Good, proven pattern | Same as C1 (semantics doesn't add cells) | Slightly higher footprint than C1/C2: +5.7% cells measured for the semantic override in the driver-ablation experiment — a small, quantified, bounded cost, not a large one |
| Computational efficiency | **Best** — no semantic model required anywhere | Moderate — one semantic model, resolution logic stays cheap | Moderate — same semantic-model cost as C2, plus a measured +20% latency for the semantic resolution driver and +9% for hysteresis on top of that (own experiments) — real but small increments, not order-of-magnitude |
| Real-time operation | Best-positioned, most precedent (RoadRunner M&M, Adaptive-LIO, RobMOT) | Good — depends on the chosen semantic model's real-time performance; this project's own research found viable real-time LiDAR segmentation models exist (20-80ms range) | Same dependency as C2, plus the smallest additional margin of the three — most components stacked, least slack |
| Visualization | Simple, clean (heightmap/occupancy grid) | Simple + semantic overlay | **Most demo-compelling** — a resolution-tier overlay showing fine/coarse regions and *why* is a genuinely more interesting visual story for the SIH's adaptive-representation pitch |
| Measurable evaluation | Straightforward (elevation accuracy, detection recall, memory) | Straightforward + semantic mIoU | **Best-prepared** — this project's own two experiments already define and validate the exact metrics needed (allocation-correctness, tier-churn rate, memory-vs-benefit efficiency) — a ready-made evaluation methodology, not one still to be invented |
| Implementation feasibility | **Highest** — fewest components, most precedent | High — one additional, well-precedented component | Moderate — most components, but each is individually de-risked by this project's own two working synthetic prototypes (an unusual advantage) |
| Technical depth | Low-Moderate | Moderate | **High** — a validated multi-driver resolution policy with a measured, working stabilization mechanism, which no paper reviewed in this project's search has published for this exact combination |
| Novelty/technical contribution | Low — a well-trodden pattern | Low-Moderate — solid integration, not a novel combination | **High** — directly closes Gap 1, the single best-evidenced genuine gap in the entire ~112-paper review, now with a working feasibility demonstration rather than only a plausibility argument |
| Failure risk | **Lowest engineering/integration risk**, but carries a *known, documented* performance risk in dense/complex scenes (pure-classical detection) | Low-Moderate — one additional, well-understood risk (semantic-model real-time performance, per this project's own FALO/SPVNAS hardware-dependence caution) | Moderate — C2's risk, plus one specifically-identified, honestly-flagged open item: the K≈3 hysteresis was validated only under independent (IID) semantic-noise, not the spatially/temporally *correlated* error pattern a real classifier likely produces |
| Demo/judge explainability | Very easy ("map gets coarser far away") | Easy, one more concept (semantics helps classify tricky content) | More to explain, but the strongest evidence-backed story: every design choice (including the specific K=3 parameter) is backed by this project's own measured data, not intuition |

---

## 3. Complexity discipline — essential / optional / unnecessary

### Candidate 1
- **Essential:** LiDAR ingestion; 2-3 discrete distance tiers (flat, non-hierarchical grid); classical ground-segmentation + slope/roughness terrain classifier; classical clustering for static/dynamic candidates; Kalman-filter tracking; basic visualization.
- **Optional:** a third distance tier for extra granularity (2 tiers already suffice per RoadRunner M&M's own precedent).
- **Unnecessary (rejected):** any semantic model, uncertainty-driven resolution, hierarchical tree structure, learned arbitration, multiple deep-learning models.

### Candidate 2
- **Essential:** everything in Candidate 1's backbone; **one** lightweight, real-time-capable semantic segmentation model, reused for both terrain-disambiguation and detection-assist (not two separate models); hybrid static-object detection (classical + semantic-assisted); Kalman-filter tracking (unchanged from C1).
- **Optional:** a second, specialized detector for a specific object class if a particular demo scenario needs it — not evidenced as generally necessary.
- **Unnecessary (rejected):** resolution-driving semantics (that is C3's differentiator, not evidenced as required for C2's scope); uncertainty-driven resolution; hierarchical tree structure; a second independent deep model; learned arbitration.

### Candidate 3
- **Essential:** everything in Candidate 2; a binary semantic-class override on the resolution rule (force-fine on designated important content) — **the simplest version tested is sufficient**; Larsson et al.'s full continuous β/γ-weighted formalism was never shown necessary and is explicitly not adopted; a K≈3 symmetric hysteresis/persistence counter on the semantic-driven resolution decision — **mandatory**, not optional, per the temporal-stability checkpoint's direct evidence that raw noisy semantic control is unusable without it.
- **Optional:** multiple "importance tiers" of semantic classes with different force-fine thresholds — not evidenced as necessary; add only if a specific validated need arises.
- **Unnecessary (rejected, with the evidence that eliminated each):** uncertainty-driven resolution refinement (eliminated with direct experimental evidence — it degraded elevation accuracy and had a worse targeting-efficiency rate than the semantic driver); learned/RL resolution arbitration (Agile3D-style — no evidence justifies this added complexity for a persistent-map setting it was never validated on); a full octree/quadtree hierarchy (the flat, discrete-tier design was directly demonstrated sufficient in both of this project's experiments, and a tree structure would import the unresolved neighbor-consistency risks this project's own boundary-consistency investigation found — no evidence a tree performs better here); multiple independent semantic models (one shared model suffices, per the measured cost structure); a weighted/learned arbitration between distance and semantic drivers.

**A structural note worth making explicit:** because Candidate 3's rule is a simple **override** ("fine if distance says fine, OR semantics says fine" — never a competing vote), it does not need to solve the driver-conflict-arbitration problem this project's research flagged as having *zero* published precedent anywhere. It **sidesteps** that gap by construction rather than solving it. A design that instead tried to let distance and semantics each argue for a *different* resolution (e.g., semantics arguing to coarsen a region distance would keep fine) would re-open that unsolved problem — and is correctly excluded here.

---

## 4. Architecture composition — the two strongest candidates

Candidates 2 and 3 are the strongest per §2 (Candidate 1 is a clean, low-
risk floor, but its one differentiating trait — pure-classical perception
— is the one component this project's own research found *not* well-
evidenced as a confident default). Both are specified below at a
conceptual level; no libraries or frameworks are selected.

| # | Component | Candidate 2 | Candidate 3 | Why present / evidence tag |
|---|---|---|---|---|
| 1 | LiDAR input | Raw 3D point cloud, per-frame | Same | **Required by SIH** — the problem is explicitly LiDAR-based |
| 2 | Perception / semantic processing | One lightweight, real-time-capable semantic segmentation model, producing per-point/per-cell class labels | Same model, additionally consumed by the resolution policy | **Supported by literature** (metric-semantic mapping's ablation; real-time LiDAR segmentation examples found in Part 3 research) + **engineering choice** for the specific model |
| 3 | Terrain representation | Classical geometric ground-segmentation, refined by the semantic vegetation/rigid distinction | Same | **Required by SIH** + **supported by literature** (Patchwork++ numbers; metric-semantic mapping's failure-mode evidence) |
| 4 | Adaptive-resolution policy | Distance-only (fine near, coarse far) | Distance (prior) + binary semantic override + K≈3 hysteresis | **Required by SIH** (explicit distance example; "adaptive spatial representation" listed separately) + for C3, **strongly supported by our own experiments** — this is the single most experimentally-validated component in either architecture |
| 5 | 2.5D map data structure | Flat, non-hierarchical, 2-3 discrete distance tiers | Same structure, one additional tier state (hysteresis-locked fine/coarse per cell) | **Engineering choice**, directly **supported by our experiments** (both implemented and measured exactly this) and by literature (RoadRunner M&M's own choice of discrete tiers over a tree) |
| 6 | Static-object handling | Classical clustering + semantic-assisted classification (hybrid) | Same | **Required by SIH** + **supported by literature** (EG-PointPillar's additive +3.88% mAP finding) |
| 7 | Dynamic-object handling/tracking | Classical clustering-based detection + Kalman-filter-family tracking, run as a separate subsystem | Same, unchanged | **Required by SIH** + **strongly supported by literature** (RobMOT/Spb3DTracker: classical tracking matches/beats a learned tracker at a fraction of the compute) + **engineering choice** to keep it separate (no validated unified mechanism exists — Gap 2) |
| 8 | Temporal update | Incremental frame-to-map fusion for the persistent map; independent Kalman predict/update for tracked objects | Same, plus the per-cell hysteresis streak-counter must persist and update every frame | **Required by SIH** (implicit, for a working mapping system) + for C3's addition, **directly required by and validated in our own experiment** |
| 9 | Visualization | 2.5D heightmap/occupancy grid, semantic overlay, tracked-object overlays | Same, plus a resolution-tier overlay (fine/coarse regions, and which driver caused each) | **Required by SIH** (explicitly listed) + **engineering choice** for rendering specifics |
| 10 | Evaluation metrics | Elevation accuracy, semantic mIoU, static-object precision/recall, dynamic-object tracking accuracy, memory footprint, latency | Everything in C2, plus resolution allocation-correctness, tier-churn rate, and memory-vs-benefit efficiency | **Required by SIH** (explicitly listed) + for C3's additions, **directly supported by our own experiments** — the metric definitions transfer as-is from the two experiment scripts already in this repository |

---

## 5. Decision matrix — transparent, not optimized for a winner

| Dimension | C1 | C2 | C3 |
|---|---|---|---|
| SIH fit | Moderate | High | High |
| Technical depth | Low | Moderate | High |
| Expected performance | Moderate (bounded by classical-only detection risk) | High | High, with a small added margin for semantically-important content |
| Computational feasibility | High | Moderate-High | Moderate |
| Implementation complexity | Low | Moderate | Moderate-High |
| Novelty potential | Low | Low-Moderate | High |
| Risk | Low engineering risk, moderate *performance* risk | Low-Moderate, well-understood | Moderate, one specific open item honestly flagged |

**This matrix does not collapse to a single winner by design** — it
surfaces a genuine three-way trade-off between safety, depth, and novelty
that the evidence does not resolve for the user; the recommendation below
distinguishes three different senses of "best" rather than forcing one.

---

## 6. Recommendation, split by what "best" means

- **Best research/technical contribution: Candidate 3.** It is the only
  candidate that closes a named, well-evidenced gap (Gap 1), and it is the
  only one backed by two rounds of this project's own working experimental
  validation (mechanical feasibility, then temporal-stability under
  realistic noise) rather than literature inference alone.
- **Best low-risk implementation: Candidate 2.** Not Candidate 1 —
  Candidate 1's simplicity comes at the cost of a *specifically
  documented* weakness (pure-classical static/dynamic detection, self-
  limited by its own literature's authors to sparse/simple scenes) that
  could cause a visible, embarrassing failure mode in a real demo with
  dense or occluded scenes. Candidate 2 removes that one clear risk at a
  modest, well-understood, well-precedented cost (one semantic model), and
  adds no other risk beyond it.
- **Best overall SIH choice: Candidate 3, conditionally.** If the
  implementation team has the capacity to build the (moderate, not
  extreme) additional complexity — one semantic model, a binary resolution
  override, a K≈3 hysteresis layer, all individually de-risked by this
  project's own experiments — Candidate 3 offers the strongest combination
  of a working system and a genuine, defensible technical contribution,
  which matters for a competition explicitly evaluating novelty alongside
  correctness. **If implementation time or capacity is a binding
  constraint, Candidate 2 is the honestly safer choice and should be
  preferred without hesitation** — it is not a lesser system, it is a
  lower-novelty one, and this document does not treat those as the same
  thing.

---

## 7. Final report

**1. Final comparison.** See §2 and §5. No candidate dominates on every
dimension; Candidate 1 is safest on raw simplicity but carries a
documented performance risk, Candidate 2 removes that risk at modest cost,
Candidate 3 adds a validated, evidence-backed novel contribution at a
further modest cost and one honestly-flagged open risk.

**2. Recommended architecture candidate: Candidate 3**, with Candidate 2
explicitly named as the correct fallback if implementation capacity is
constrained (§6).

**3. Why it wins (as the primary recommendation).** It is the only
candidate addressing the SIH's full "adaptive spatial representation"
ambition (not just the literal distance example), it closes this
project's best-evidenced identified gap, and — unusually — every one of
its distinguishing design choices (the binary semantic rule instead of a
weighted formalism, the K≈3 hysteresis parameter, the decision to keep
dynamic-object handling separate) is backed by this project's own measured
experimental data rather than assumption.

**4. What we deliberately did NOT include.** Uncertainty-driven resolution
refinement (eliminated with direct evidence); learned or RL-based
resolution arbitration; a hierarchical tree/octree/quadtree structure;
multiple independent deep-learning models; a unified adaptive-resolution +
dynamic-object mechanism (Gap 2 was left as a separate subsystem, not
attempted from scratch); Larsson et al.'s full continuous semantic-
weighting formalism (the simpler binary override was shown sufficient);
any resolution-boundary-consistency mechanism beyond what the discrete-tier
structure already provides (the effect was measured as real but modest —
a secondary engineering constraint, not requiring a dedicated fix at this
stage).

**5. Main technical contribution(s).** A persistent, non-hierarchical 2.5D
adaptive-resolution map combining a distance prior with a semantic-class
override, stabilized against realistic classifier noise by a validated,
minimal (K≈3) hysteresis mechanism — closing Gap 1 with a design that also
structurally avoids the unsolved driver-conflict-arbitration problem by
using an override rule rather than competing votes.

**6. Main risks.** (a) The hysteresis mechanism's robustness was validated
only under independent (IID) semantic-noise, not the spatially/temporally
correlated error pattern a real classifier likely produces — the single
most important open item. (b) Real-time performance depends on the chosen
semantic model and target hardware, consistent with this project's own
repeated finding (SPVNAS/FALO) that theoretical efficiency does not
reliably predict measured speedup. (c) The classical-vs-learned gap for
static-object detection in dense/occluded scenes remains only partially
evidenced, mitigated but not eliminated by the hybrid design.

**7. What should be frozen now.** 2.5D representation (not 3D); the
persistent-map + separate-dynamic-subsystem architectural split; distance
as the base resolution driver; a flat, non-hierarchical, discrete-tier
data structure (no tree); exclusion of uncertainty-driven resolution and
learned arbitration; classical Kalman-filter-family tracking for dynamic
objects; and, if Candidate 3 is confirmed, the binary semantic-override
rule with mandatory K≈3 hysteresis.

**8. What remains intentionally flexible.** The specific semantic
segmentation model/architecture; classical clustering algorithm and
parameters; the exact number of distance tiers (2 vs. 3); the precise K
value for hysteresis (3 was validated as a good starting point, but should
be re-checked once real classifier error correlation is known); whether a
future, separate uncertainty-*awareness* mechanism (flagging rather than
resolution refinement) is worth adding later; visualization rendering
choices; and the specific evaluation dataset/benchmark.

**9. First implementation phase after architecture freeze.** Build and
validate the shared backbone first, on real (not synthetic) LiDAR data,
before adding any differentiating component: the persistent 2.5D grid with
distance-only tiers, classical terrain classification, and basic
visualization — i.e., a working Candidate-1-equivalent core. This
establishes a real-data baseline against which the semantic layer (Part 2
work) and, if pursued, the semantic-driven resolution + hysteresis layer
(Part 3 work) can each be added and measured incrementally, rather than
building the full target architecture in one pass.

No architecture is implemented by this document. No further research was
performed to produce it — this is a synthesis of decisions already earned
by evidence gathered in `01`-`05` and the two feasibility experiments.
