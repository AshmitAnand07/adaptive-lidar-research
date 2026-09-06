# 03 — Paper × SIH Requirement Matrix, and Gap Map

Status: Synthesis checkpoint, built entirely from Phase 1 + Phase 2 research
already completed. No new literature search performed. No architecture is
selected or recommended.

## Methodology and caveats

Each paper (8 supplied + ~104 external, from `evidence/citations.md` and
`external_literature/00_inventory.md`) is scored against the 16 SIH
requirement dimensions specified for this checkpoint. Symbols:

- **Y** — central/direct evidence the paper addresses this requirement (per
  its own analysis file's DIRECT EVIDENCE / full-text-verified claims).
- **P** — partial, incidental, weak, or lower-confidence evidence (e.g. the
  paper touches the requirement as a side effect, or access was snippet-only).
- **?** — explicitly could not be determined from any accessible source
  (flagged as an open gap in the source material itself, not scored as
  either present or absent).
- *(blank)* — not addressed / no evidence found in this paper.

Columns: **2.5D** representation · **Elev** elevation/height · **Terr**
terrain/drivability · **Sem** semantic perception · **Static** static
obstacles · **Dyn** dynamic objects · **Temp** temporal consistency ·
**AdRes** adaptive resolution (any driver) · **PersMap** persistent adaptive
map (resolution adaptivity that survives across frames, not per-inference
only) · **SemAd** semantic-*driven* adaptation (semantics changes the
resolution, not just labels content) · **UncAd** uncertainty/variance-*driven*
adaptation · **MultiD** multi-driver adaptation (2+ combined criteria) ·
**MemRed** memory reduction (quantified or clearly claimed) · **RT**
real-time computation (quantified latency/FPS, or explicit hardware-validated
claim) · **LongR** long-range representation (explicit long-range design
goal/result) · **BoundC** resolution-boundary consistency (explicit treatment
of fine/coarse transition artifacts).

A cell being blank means "not addressed in this paper" — per this project's
standing rule, this is evidence of absence **in the reviewed literature**,
not proof of non-existence elsewhere.

---

## Supplied Papers (Phase 1)

| # | Paper | 2.5D | Elev | Terr | Sem | Static | Dyn | Temp | AdRes | PersMap | SemAd | UncAd | MultiD | MemRed | RT | LongR | BoundC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Stochastic Triangular Mesh Mapping | Y | Y | P | | P | | P | | | | | | P | | | |
| 2 | Real-Time Metric-Semantic Mapping | | | Y | Y | P | | | | | | | | | Y | | |
| 3 | αLiDAR | | | | | P | | P | P* | | | | | | Y | | |
| 4 | Graph SLAM 2.5D LIDAR Mapping | Y | Y | P | | P | | P | | | | | | | | P | |
| 5 | 2.5D Motion Grids (DATMO) | Y | Y | | | P | Y | Y | | | | | | | | | |
| 6 | 2.5D Evidential Grids | Y | P | | | P | Y | Y | | | | | | | | | |
| 7 | Variable-Resolution NDT | | | | | P | | P | Y | Y | | | | Y | | | |
| 8 | Lightweight 2.5D SLAM | Y | Y | | | P | P | P | | | | | | Y | P | | |

\* αLiDAR's "AdRes" is adaptive **sensing**, not adaptive map resolution — flagged, not counted toward the map-side requirement.

**Supplied-set summary**: 5/8 use 2.5D; only 1/8 (#7) has any adaptive
resolution, and it is single-driver (curvature) with no semantic/uncertainty/
multi-driver adaptation, no persistent-map-plus-dynamic-object combination
anywhere, and zero papers address resolution-boundary consistency.

---

## External Papers — Group A (Adaptive Resolution & Hierarchical Mapping)

| Paper | 2.5D | Elev | Terr | Sem | Static | Dyn | Temp | AdRes | PersMap | SemAd | UncAd | MultiD | MemRed | RT | LongR | BoundC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D-Map | | | | | P | | P | Y | Y | | | | P | P | | |
| ROG-Map | | | | | P | | P | | | | | | | Y | | |
| Ada3D | | | | | P | | | | | | | | Y | Y | | |
| Hier. Adaptive Voxel-Guided Sampling | | | | | | | | | | | | | | P | | |
| AVS-Net | | | | | | | | | | | | | | | | |
| VoxelMap | | | | | P | | P | Y | Y | | | | | | | |
| **Adaptive-LIO** | | | | | | | P | Y | Y | | | | | | | |
| Adaptive Patched Grid Mapping | Y | Y | P | | | P | P | Y | Y | | | P | P | P | | |
| A-OctoMap | | | | | | | | Y | P | | | | P | | | |
| wavemap | | | | | | | | Y | Y | | P | | P | | | |
| OctoMap | | | | | | P | P | Y | Y | | | | | | | |
| Langerwisch & Wagner | | | | | | | | Y | Y | | Y | | | | | |
| Li/Ruichek stereo quadtree | | | | | | | | Y | P | | | | | | | |
| MAP-ADAPT | | | | Y | | | P | Y | Y | Y | | **Y** | P | | | |
| TSDF Adaptive-Res. (RAAI) | | | | P | | | | P | P | P | | | | | | |
| Comm.-Aware Hierarchical Map Compression | | | | | | Y | Y | Y | Y | | | | P | | | |
| G-VOM | | | Y | | P | | | | | | | | | Y | | |
| HOTFormerLoc | | | | | | | | P | P | | | | | | | |
| Adaptive Fovea (scanning depth sensors) | | | | | | | | P* | | | | | | | | |
| Multi-Scale Dynamic Sparse Voxelization | | | | | P | P | | | | | | | | Y | | |
| Range-Based Point Cloud Density Optimization | | | | | | | | P* | | | | | | | | |
| Survey of Spatial Memory Representations (survey) | | | | | | | | | | | | | | | | |

\* Adaptive Fovea and Range-Based Density Optimization are marked P because
their adaptivity is sensing-side or input-level, not persistent map
resolution — noted per CLAUDE.md's sensing-vs-representation distinction.

## External Papers — Group B (Attention/Foveated, Uncertainty & Risk-Aware, Real-Time)

| Paper | 2.5D | Elev | Terr | Sem | Static | Dyn | Temp | AdRes | PersMap | SemAd | UncAd | MultiD | MemRed | RT | LongR | BoundC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FOVEA (camera) | | | | | | P | P | P | | | | | | Y | | |
| MEMS-based Adaptive LiDAR | | | | | | | | P | | | | | | | | |
| Fast Attention-Based Simplification | | | | | | | | P | | | | | | P | | |
| PointSplit | | | | Y | P | | | P | | Y | | | | Y | | |
| DH-V2 (fixed foveation, contrast case) | | | | | | | | | | | | | Y | Y | | |
| Space-variant/active vision survey | | | | | | | | | | | | | | | | |
| Occupancy Grids (Elfes, foundational) | | | | | | | P | | | | | | | | | |
| Gaussian Process Occupancy Maps | | | | | | | | P | P | | P | | | | | |
| Deep ISM Priors (radar) | | | | | | | | | | | | | | | | |
| EviLOG | | | | | | | | | | | | | | | | |
| E2-BKI | P | | P | Y | | | | Y | P | | P | | | P | | |
| ContraMap | | | | | | | | | | | | | | P | | |
| Uncertainty-Aware VI-SLAM | | | | | | | | | | | | | | | | |
| SOGMP / SOGMP++ | | | | | | Y | Y | | | | | | | | | |
| Uncertainty-driven Planner | | | | | | | | | | | | | | | | |
| RAMP | Y | Y | Y | | | | Y | | | | | | | | | |
| EVORA | | | Y | | | | | | | | | | | | | |
| STEP + SubT results | | | Y | | | | | | | | | | | | | |
| RiskMap | | | | | | P | | | | | | | | | | |
| CVaR-MPPI (no map, contrast case) | | | | | | | | | | | | | | Y | | |
| Risk-aware planetary rover planning | | | Y | | | | | | | | | | | | | |
| Is Semantic SLAM Ready for Embedded? (survey) | | | | P | | | | | | | | | | P | | |
| SPAQ-DL-SLAM | | | | | | | | | | | | | Y | Y | | |
| Voxel-Based 3D Detection Efficiency Analysis | | | | | | | | P | | | | | | P | ✗* | |
| **Agile3D** | | | | | | | | Y | | | | **Y** | | Y | | |
| DaDe | | | | | P | P | | | | | | | | | | |
| Are We Ready for Real-Time LiDAR Sem. Seg.? (benchmark) | | | | P | | | | | | | | | | P✗* | | |
| Mixture-of-Experts Edge 3D Detection | | | | | | | | Y | | | | **Y** | | Y | | |
| DFPS (full read) | | | Y | | | | | Y | | | | | | Y | | |

\* "✗" marks an explicit **disconfirming** finding, not merely an absence:
the voxel-efficiency paper found full-range models already "fail to detect
distant small objects," and the real-time LiDAR segmentation benchmark found
most models are NOT real-time on embedded hardware. Both are direct evidence
against an assumption, not neutral gaps.

## External Papers — Group C (2.5D/Elevation, Semantic Mapping, Terrain/Traversability)

| Paper | 2.5D | Elev | Terr | Sem | Static | Dyn | Temp | AdRes | PersMap | SemAd | UncAd | MultiD | MemRed | RT | LongR | BoundC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MEM | Y | Y | P | Y | | | | | | | | | P | Y | | |
| RoadRunner | Y | Y | Y | | | | | | | | | | | Y | | |
| **RoadRunner M&M** | Y | Y | Y | | | | | Y | Y | | | | | Y | P | |
| SSMI | | | | Y | | | P | Y | Y | | | | | | | |
| **Larsson et al.** | | | | Y | | | P | Y | Y | **Y** | | P | | P | | |
| Asgharivaskasi & Atanasov multi-robot | | | | Y | | | | Y | Y | | | | | | | |
| Stache et al. UAV | | | | Y | | | | P | P | **Y** | | | | | | |
| Resolution-adaptive Quadtrees UAV (snippet) | | | | P | | | | P | P | | | | | | | |
| Terrain-Aware Semantic Mapping (subterranean) | | | Y | Y | Y | P | P | | | | | | Y | | | |
| Watch Your STEPP | | | Y | | | | | | | | | | | | | |
| Fankhauser elevation mapping (foundational) | Y | Y | P | | | | | | | | | | | | | |
| Kraetzschmar quadtree (foundational) | | | | | | | | Y | Y | | | | P | | | |
| Wellington & Stentz (foundational) | P | | Y | | | | Y | | | | | | | | | |
| Survey of Traversability Estimation (survey) | | | P✗* | | | | | | | | | | | | | |
| Variable-Resolution Virtual Maps (USV) | | | | | | | | Y | Y | | **Y** | | | | | |
| Multi-Res. Elevation Mapping (Planetary Rotorcraft) | Y | Y | Y | | | | | Y | Y | | | | | | | |

\* The traversability-estimation survey explicitly does **not** surface
adaptive/multi-resolution mapping as a live research axis at the level
accessible — a disconfirming signal about how connected these two research
threads currently are, not neutral silence.

## External Papers — Group D (Dynamic Occupancy, Motion Segmentation, Scene Flow, Temporal)

| Paper | 2.5D | Elev | Terr | Sem | Static | Dyn | Temp | AdRes | PersMap | SemAd | UncAd | MultiD | MemRed | RT | LongR | BoundC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Nuss et al. RFS DOGMa (foundational) | | | | | | Y | Y | | | | | | | | | |
| Danescu et al. (foundational) | | | | | | Y | Y | | | | | | | | | |
| Schreiber RNN DOGMa | | | P | Y | | Y | Y | | | | | | | | | |
| Categorized Grid | | | | | | P | P | | | | | | | | | |
| Dynamic OGM w/ BEVFusion | | | | Y | | Y | P | | | | | | | | | |
| DATMO Review (survey) | | | | | | P | | | | | | | | | | |
| MotionNet | | | | | | Y | P | | | | | | | P | | |
| Dynamics-Aware Spatiotemporal Occ. Pred. | | | | | | Y | Y | | | | | | | | | |
| Learning Spatiotemporal OGM Lifelong Nav | | | | | | Y | Y | | | | | | | | | |
| DynORecon | | | | | | Y | Y | ? | ? | | | | | Y | | |
| Spatio-Temporal Voxel Layer | | | | | | Y | | | | | | | P | Y | | |
| LMNet | | | | | | Y | | | | | | | | Y | | |
| 4DMOS | | | | | | Y | Y | | | | | | | P | | |
| MambaMOS | | | | | | Y | Y | | | | | | | | | |
| SegNet4D | | | | Y | | Y | Y | | | | | | | P | | |
| PointPWC-Net | | | | | | Y | | | | | | | | | | |
| SeFlow | | | | | | Y | | | | | | | | P | | |
| Flow4D | | | | | | Y | Y | | | | | | | Y | | |
| SemanticFlow | | | | Y | | Y | | | | | | | | | | |
| PointRNN (foundational) | | | | | | P | Y | | | | | | | | | |
| **Funk et al.** | | | | | | ✗* | P | Y | Y | | | | | P | | |
| **MURAL** | | | | | | Y | P | Y** | | | | | | Y | | |
| **AdaOcc** | | | | | P | ? | | Y | Y | | | | | | | |

\* Funk et al. is the cleanest pure adaptive-map-resolution example in the
entire Phase 2 search, and is explicitly, confirmedly **absent** of any
dynamic-object handling (static/quasi-static scope stated by the authors) —
marked with "✗" rather than blank to distinguish "confirmed absent" from
"not checked."
\*\* MURAL's AdRes is confirmed **temporal/deadline-driven, spatially uniform
per frame** — not the spatial near/far pattern the SIH problem describes.
Marked Y for "adaptive resolution exists" but this is the paper most
responsible for the H2 "weakened, not disproved" verdict — see
`04_paper_vs_paper_matrix.md`.

## External Papers — Group E (Sparse LiDAR Perception, Sparse 3D CNNs/Tensors)

| Paper | 2.5D | Elev | Terr | Sem | Static | Dyn | Temp | AdRes | PersMap | SemAd | UncAd | MultiD | MemRed | RT | LongR | BoundC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Submanifold Sparse Conv (foundational) | | | | | | | | | | | | | | | | |
| Minkowski Engine | | | | | | | Y | | | | | | | | | |
| VoxelNet (dense baseline) | | | | | P | | | | | | | | | | | |
| SECOND | | | | | P | | | | | | | | | Y | | |
| PointPillars | Y | | | | P | | | | | | | | | Y | ✗* | |
| OctNet | | | | | | | | Y | P | | | | Y | | | |
| Voxel Hashing (foundational) | | | | | | | | | | | | | P | | | |
| SPADE | | | | | P | | | | | | | | P | Y | | |
| FSD | | | | | P | | | | | | | | | Y | Y | |
| FSD++ / Super Sparse | | | | | | P | Y | | | | | | | | Y | |
| Focal Sparse Conv | | | | | | | | | | | | | | P | | |
| SPS-Conv | | | | | | | | | | | | | | Y | | |
| FALO (disconfirming case) | | | | | | | | | | | | | | Y** | | |
| LiDAR-PTQ | | | | | | | | | | | | | | Y | | |
| SPVNAS | | | | | P | Y | | | | | | | Y | Y*** | | |
| Cylinder3D | | | | Y | P | P | | P† | | | | | | | | |
| **MrHash** | | | | | | | | Y | Y | | **Y** | | Y | Y | | |
| Spira | | | | | | | | | | | | | | Y | | |
| SD-Conv / SPADE+ | | | | | | | | | | | | | | Y | | |

\* PointPillars' own stated limitation is losing distant/small-object detail
— explicit disconfirming evidence, not silence.
\*\* FALO's "RT: Y" is a **disconfirming** result: it demonstrates sparse
convolution *losing* to a dense re-engineered alternative on real edge
silicon, not a confirmation that sparsity helps.
\*\*\* SPVNAS's "RT: Y" comes with a key nuance: 7.6x theoretical compute
reduction produced only 2.7x measured speedup — direct evidence that
compute-reduction and wall-clock speedup are not the same claim.
† Cylinder3D's adaptivity is an *implicit*, geometry-side-effect of
coordinate-system choice, not a deliberate policy.

---

## GAP MAP

For each SIH requirement below: state classification, justification, and
source. Classification levels: **Well solved** / **Partially solved** /
**Weakly solved** / **Apparently underexplored** / **Unknown**.

### 2.5D representation
**Well solved.** 5/8 supplied papers and at least 9 external papers (MEM,
RoadRunner, RoadRunner M&M, Fankhauser, Planetary Rotorcraft mapping,
PointPillars' pillar representation, Adaptive Patched Grid Mapping, RAMP)
demonstrate working 2.5D representations across multiple domains (ground
robots, off-road vehicles, planetary rotorcraft, automotive). Evidence level:
DIRECT EVIDENCE (multiple full-text-verified papers).

### Elevation/height
**Well solved.** Same evidence base as above; Fankhauser et al. is the
foundational reference (2014/2018) with per-cell Kalman-filtered height and
variance, extended by MEM (semantic layers) and RoadRunner M&M (multi-range).
Evidence level: DIRECT EVIDENCE.

### Terrain/drivability
**Partially solved.** Multiple independent, mature systems exist
(RoadRunner/M&M, G-VOM, EVORA, STEP, RAMP, Terrain-Aware Semantic Mapping) —
but each solves a different sub-problem (learned continuous cost, classical
geometric slope/roughness, evidential risk, CVaR tail-risk) with no
consensus method, and **only metric-semantic mapping (supplied #2)**
demonstrates a documented failure mode (grass misclassified as traversable
without semantics) — meaning the field has multiple competing solutions but
limited cross-validated failure-mode analysis. Evidence level: DIRECT
EVIDENCE for individual systems; DERIVED for the "no consensus" observation.

### Semantic perception
**Partially solved for static/generic classes; weakly solved for the
specific classes an SIH terrain/object system needs.** Semantic segmentation
of generic outdoor classes is mature (MAP-ADAPT, Larsson et al., SSMI,
Terrain-Aware Semantic Mapping, MEM, Cylinder3D, SegNet4D) — but
purpose-built terrain-traversability semantic classes with validated failure
analysis exist in only one paper found (metric-semantic mapping, supplied
#2). Evidence level: DIRECT EVIDENCE.

### Static obstacles
**Partially solved.** Generic 3D object detection (VoxelNet, SECOND,
PointPillars, SPVNAS, FSD, and descendants) reliably detects static-capable
classes (parked vehicles) at maturity, and structural static-obstacle
detection (walls, stairways) exists in Terrain-Aware Semantic Mapping
(subterranean). But this is scattered across separate systems, none of which
also handle dynamic discrimination or adaptive resolution simultaneously.
Evidence level: DIRECT EVIDENCE.

### Dynamic objects
**Partially solved for detection/segmentation/tracking in isolation; weakly
solved when required alongside a persistent spatial representation.** The
MOS lineage (LMNet→4DMOS→MambaMOS→SegNet4D), scene-flow lineage
(PointPWC-Net→SeFlow→Flow4D→SemanticFlow), and DOGMa lineage (Nuss,
Danescu, Schreiber, Jang) are all mature, real-time-capable (several with
measured FPS), and well-benchmarked (SemanticKITTI-MOS, Argoverse 2) — but
**every one of these uses fixed spatial resolution**, a repeated, direct
finding across 23 papers in Group D. Evidence level: DIRECT EVIDENCE (per
paper) / DERIVED (the aggregate fixed-resolution pattern).

### Temporal consistency
**Partially solved.** Sequence-native learned temporal fusion (4DMOS,
MambaMOS, Flow4D) and Bayesian/particle-filter temporal fusion (DOGMa
lineage, evidential grids) are both mature and demonstrated, but always on
fixed-resolution representations — temporal consistency has not been jointly
studied with map resolution changes over time. Evidence level: DIRECT
EVIDENCE.

### Adaptive resolution (any driver)
**Well solved as a general capability; weakly solved for any single specific
driver combination the SIH problem needs.** At least 8 distinct drivers have
independent, multiply-replicated precedent (distance, curvature, occupancy-
homogeneity, semantics, uncertainty/variance, object-ROI, system-load, and
implicit coordinate-system effects). Evidence level: DIRECT EVIDENCE (>20
papers).

### Persistent adaptive maps
**Partially solved, but genuinely less common than "adaptive resolution" in
general.** Real, persistent (multi-frame, maintained) adaptive-resolution
maps exist: Adaptive-LIO, VoxelMap, D-Map, OctoMap, wavemap, MAP-ADAPT,
Larsson et al., RoadRunner M&M, Funk et al., and — the cleanest example in
the entire search — MrHash. But across ~104 external papers, fewer than 15
are genuine examples of this specific category (most "adaptive" work is
transient, per-inference computation that never persists as a map).
Evidence level: DIRECT EVIDENCE (per paper) / DERIVED (relative rarity).

### Semantic-driven adaptation
**Partially solved, narrowly.** Larsson et al. (2022) and Stache et al.
(2021/22) are direct, independent, demonstrated examples — this concept is
not new. But both operate outside the SIH's specific setting (full 3D or
flat 2D, not 2.5D; UAV or generic exploration, not ground-vehicle terrain
perception). Evidence level: DIRECT EVIDENCE for the general mechanism;
**apparently underexplored** for the specific ground-vehicle/2.5D
combination — "not identified in the literature searched," not "does not
exist."

### Uncertainty-driven adaptation
**Partially solved.** MrHash (SDF variance), Langerwisch & Wagner (sensor-
error bounds), and Variable-Resolution Virtual Maps/USV (SLAM/information-
density) are three independent, structurally different examples. MrHash in
particular gives strong, recent (2025), rigorously measured evidence this
approach can outperform fixed-resolution baselines. Evidence level: DIRECT
EVIDENCE (MrHash, full text); DERIVED/lower-confidence for the two older
examples (snippet-level access).

### Multi-driver adaptation
**Apparently underexplored.** Only MAP-ADAPT (semantic + geometric
complexity + available compute) and Agile3D / Mixture-of-Experts edge
detection (content + system load, but per-frame not persistent map) combine
more than one driver, and none combine more than two-three. A policy
deliberately combining distance (coarse global prior) with semantic or
uncertainty refinement was **not identified in the literature searched**.
Evidence level: DIRECT EVIDENCE for the few examples that exist; the "gap"
claim itself is DERIVED from their scarcity, not a proven absence.

### Memory reduction
**Well solved.** Quantified, measured memory reduction is reported across
many independent papers and mechanisms (MrHash ~4x; SPVNAS 1.7-8.3x model
size; Variable-Resolution NDT 36-80% of baseline; OctNet 32³→256³ at
comparable memory; SPAQ-DL-SLAM 79.8% size cut). Evidence level: DIRECT
EVIDENCE (multiple, cross-validated by mechanism).

### Real-time computation
**Partially solved, hardware- and mechanism-conditional.** Many papers
report real, measured real-time performance (Ada3D, SECOND, PointPillars,
SPADE, Flow4D, MrHash, Agile3D) — but FALO and SPVNAS are direct evidence
that theoretical efficiency does not reliably translate to measured speedup,
and depends heavily on target hardware. Evidence level: DIRECT EVIDENCE on
both the positive and disconfirming sides.

### Long-range representation
**Weakly solved.** Only FSD/FSD++ (explicit 200m-range design goal, linear-
not-quadratic scaling) and RoadRunner M&M (100m, two-tier) directly target
long range as a first-class design constraint; most other papers operate at
typical automotive/indoor ranges (20-100m) without discussing range scaling
as such. Evidence level: DIRECT EVIDENCE for the two examples; **apparently
underexplored** as a general design axis in the rest of the literature
reviewed.

### Resolution-boundary consistency
**Apparently underexplored — the weakest-covered requirement of all 16.**
Zero papers across the entire ~112-paper set (supplied + external) were
found to explicitly analyze or measure artifacts, discontinuities, or
consistency issues at the transition between fine and coarse resolution
regions — including RoadRunner M&M, which has exactly such a boundary (its
two discrete distance tiers) but does not discuss it in what was accessed.
Evidence level: **absence across the entire reviewed set** — stated
explicitly as "not identified in the literature searched," not as "does not
exist" or "is not a real concern."

---

## Intersections

For each requested pairwise intersection: whether it's addressed, how
completely, and by which paper(s).

| Intersection | Addressed? | Completeness | Example(s) |
|---|---|---|---|
| 2.5D + adaptive resolution | Yes | Moderate — several examples, all single-driver | RoadRunner M&M (distance), Multi-Res. Elevation Mapping/Planetary Rotorcraft (measurement-density), Adaptive Patched Grid Mapping (request-driven) |
| 2.5D + semantic adaptation | **Not identified** | — | Nearest: MEM (2.5D+semantic, fixed res.) and Larsson et al. (semantic-adaptive, not 2.5D) exist separately; no paper combines both |
| 2.5D + dynamic objects | Weak | Only within the supplied set, and only offline/qualitative | Motion grids (#5), evidential grids (#6) — both supplied, both offline/qualitative-only; no external paper found combining 2.5D with dynamic-object perception |
| Adaptive resolution + dynamic objects | **Weakened, not solved** | Two near-misses, no clean example | AdaOcc (resolution-adaptive, dynamic-tie unconfirmed), MURAL (dynamic-object-capable via downstream tracker, resolution adaptation temporal not spatial); Funk et al. is adaptive-resolution but confirmed *no* dynamic-object handling |
| Adaptive resolution + uncertainty | Yes | Good — a clean, recent, well-measured example exists | MrHash (SDF variance-driven); also Langerwisch & Wagner, Variable-Resolution Virtual Maps/USV |
| Adaptive resolution + terrain | Yes | Good | RoadRunner M&M (distance-tier + CVaR terrain risk); Multi-Res. Elevation Mapping/Planetary Rotorcraft (measurement-density + landing safety) |
| Semantic + dynamic + adaptive resolution (all three) | **Not identified** | — | No paper combines all three; closest partial coverage is scattered across separate papers (SegNet4D: semantic+dynamic, fixed res.; MAP-ADAPT: semantic+adaptive, no dynamic) |
| Distance + semantic adaptation | **Not identified** | — | RoadRunner M&M (distance) and Larsson et al./Stache et al. (semantic) are each single-driver; no paper combines distance with semantics as joint drivers |
| Distance + uncertainty adaptation | **Not identified** | — | Adaptive-LIO (distance) and MrHash (variance) are each single-driver; no combination found |
| Distance + terrain adaptation | Yes, partially | RoadRunner M&M's distance-tiered resolution directly feeds a terrain/traversability map — this is the closest existing example to a "distance drives resolution, terrain is the perception target" pattern, though the terrain-cost estimation itself does not additionally modulate the resolution (it is a one-way relationship: distance → resolution → terrain map, not terrain content feeding back into resolution) | RoadRunner M&M |

---

## The Three Flagged Gaps — Scrutinized

### Gap 1: "Persistent 2.5D map + explicit semantic-class-driven resolution for a ground robot"

- **Classification: Likely genuine gap** (within the scope of what was searched).
- Reasoning: Every individual ingredient is independently well-established
  (2.5D mapping: Fankhauser lineage, MEM, RoadRunner; semantic-class-driven
  adaptive resolution: Larsson et al., Stache et al.) but the *combination*
  was not identified anywhere in ~104 papers across five independently-
  searched research families, several of which (Group C specifically)
  targeted this exact combination adversarially. The two nearest analogues
  (Larsson et al. — full 3D, not 2.5D; Stache et al. — flat 2D, no
  elevation, UAV not ground-vehicle) each fail on a different, specific,
  identifiable dimension rather than being loosely "kind of similar," which
  increases confidence this is a real gap rather than a search-coverage
  artifact.
- Caution: "likely," not "confirmed" — the search was thorough but not
  exhaustive, and 2.5D-adaptive-semantic mapping could exist in venues or
  terminology not covered (e.g., non-English-language literature, patents,
  or unindexed technical reports).

### Gap 2: "One unified mechanism combining spatially variable resolution with genuine dynamic-object detection/tracking"

- **Classification: Potentially genuine gap.**
- Reasoning: This is weaker than Gap 1's "likely" because two 2024-2026
  papers (AdaOcc, MURAL) came close enough that the honest verdict is
  "weakened, not disproved, not confirmed" (see `evidence/claims.md`, H2).
  AdaOcc's failure to confirm the dynamic-object half is an **access
  limitation** (PDF fetch failed twice), not a confirmed absence in the
  paper itself — meaning this could resolve to "already substantially
  addressed" pending a full-text read that this project has not yet
  obtained. MURAL is a confirmed near-miss on a specific, well-understood
  dimension (temporal/uniform vs. spatial/variable), which is closer to
  **likely integration gap** than "genuine gap" in the deepest sense — the
  pieces (adaptive resolution, dynamic-object tracking) individually exist
  and are mature; what's missing is someone connecting them in one spatial
  (not temporal) mechanism.
- Given the two different sub-readings above, this gap is reported as
  **potentially genuine**, with an explicit, actionable follow-up (a
  full-text read of AdaOcc) that could change the classification.

### Gap 3: "A resolution policy combining multiple drivers such as distance + semantics/uncertainty/terrain"

- **Classification: Likely integration gap** (not a deep conceptual gap).
- Reasoning: Each individual driver (distance, semantics, uncertainty,
  terrain-complexity) has strong, independent, multiply-replicated evidence
  of working in isolation. Two papers (MAP-ADAPT: semantic+geometry+compute;
  Agile3D: content+system-load) already demonstrate that combining 2-3
  drivers is technically tractable and beneficial in adjacent settings. The
  absence of a distance+semantic (or distance+uncertainty) combination
  specifically reads as an unassembled combination of already-solved parts,
  not a fundamental technical barrier — consistent with how Phase 2's H4
  verdict characterized the analogous 2.5D+adaptive+semantic three-way gap
  ("a plausible, low-hanging extension of existing work rather than a deep
  unexplored frontier").
- Caution: "likely integration gap" is itself a claim requiring feasibility
  validation (Phase 8) before being treated as low-risk — combining drivers
  that each work alone does not guarantee the combination is trivial (e.g.,
  drivers could conflict: a semantically-important-but-geometrically-simple
  object at long range might get contradictory resolution signals from a
  distance-driven rule vs. a semantic-driven rule, and no paper found
  discusses how to arbitrate that conflict).

### Other gaps that may be more technically interesting than the three flagged

1. **Resolution-boundary consistency** — the single most universally
   unaddressed requirement in the entire matrix (zero papers, including ones
   with an explicit discrete-tier boundary like RoadRunner M&M). This may be
   more technically interesting than Gaps 1-3 because it's not merely
   "nobody combined X and Y" — it's a specific, checkable failure mode
   (discontinuity/artifact at a resolution transition) that no paper
   examined at all, positive or negative. **Apparently underexplored**,
   arguably the strongest candidate for a genuinely novel contribution among
   everything surfaced.
2. **Driver-conflict arbitration** — no paper found discusses what happens
   when two adaptivity criteria (e.g., distance says "coarsen," semantics
   says "keep fine") disagree for the same region. This is implicit in Gap
   3 but is really a distinct, more fundamental question: not "has anyone
   combined drivers" but "does anyone have a principled way to combine them
   when they conflict." **Insufficient evidence** — no paper was found
   either solving or explicitly raising this as a problem.
3. **Measured (not theoretical) computational cost of maintaining a
   persistent adaptive map over long deployments**, as opposed to per-scan
   or single-experiment benchmarks. Most compute/memory numbers in this
   review are single-session or short-duration (Variable-Resolution NDT's
   longest test is a repeated conference-room scan; MrHash's evaluation
   duration is not detailed at the access level obtained). Long-duration
   drift in adaptive-resolution overhead (e.g., does fragmentation or
   re-partitioning cost grow over a multi-hour deployment?) is
   **apparently underexplored**.

---

Next: `04_paper_vs_paper_matrix.md` for direct paper-to-paper comparison
(lineage, closest analogues, and which paper-pairs would jointly satisfy
each gap above if combined).
