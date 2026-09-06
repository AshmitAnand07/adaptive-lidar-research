# Resolution-Boundary Consistency — Focused Research Note

Status: Literature investigation (§1-8) plus a small feasibility experiment
(§9, now run and reported) complete for this pass. No architecture chosen,
no SIH pipeline implemented — see §9c and §11.

## 1. Research question

"Does changing spatial resolution between neighboring regions create
measurable geometric, semantic, temporal, or object-perception problems in
adaptive 2.5D LiDAR representations?" — and, as a follow-up narrowing:
"Has the LiDAR/robotics literature already identified, measured, or solved
resolution-transition/boundary problems in adaptive spatial representations?"

This is a focused follow-up to the synthesis checkpoint
(`03_paper_vs_sih_matrix.md`'s Gap Map), which classified resolution-boundary
consistency as "apparently underexplored" based on the ~112 papers already
reviewed in Phase 1/2. **That classification is revised by this
investigation — see §11.**

## 2. Literature evidence

Three background searches were run, kept strictly separate by domain, plus
two targeted direct follow-up fetches by the main investigation (not a
subagent) to resolve specific access gaps flagged by the searches.

### 2a. LiDAR/robotics-mapping-native evidence

| # | Source | Sensor/representation | Access | What it shows |
|---|---|---|---|---|
| L1 | Schoppmann, Proença, Delaune, Pantic, Hinzmann, Matthies, Siegwart, Brockers, "Multi-Resolution Elevation Mapping and Safe Landing Site Detection... Planetary Rotorcraft," IROS 2021, arXiv:2111.06271 | 2.5D elevation map; **monocular SfM depth, not LiDAR** | Full text (verified twice) | **DIRECT, verbatim**: *"Artifacts can occur in the areas within the map where the resolution changes between neighboring cells. However, since this is only the case in non-flat areas of the map, we can ignore those artifacts for the purpose of landing site detection."* |
| L2 | Funk, Tarrio, Papatheodorou, Popovic, Alcantarilla, Leutenegger, "Multi-Resolution 3D Mapping with Explicit Free Space Representation for Fast and Accurate Mobile Robot Motion Planning," ICRA 2021 / RA-L, arXiv:2010.07929 | Persistent multi-resolution 3D octree; **input is a "depth image" (RGB-D-style), not confirmed as LiDAR** | Full text (ar5iv) | **DIRECT**: an explicit dual-scale hysteresis + max-pooling propagation mechanism, whose stated purpose is to "reduce artefacts by smoothing values during initialisation" of a scale change; a figure is captioned to show "lack of artefacts in the transition." No before/after magnitude quantified. |
| L3 | Schleich & Behnke, "Search-based Planning of Dynamic MAV Trajectories Using Local Multiresolution State Lattices," ICRA 2021, arXiv:2103.14607 | Multiresolution **state lattice** for MAV trajectory planning — a planning representation, not a sensor-derived occupancy/elevation map | Full text (ar5iv) | **DIRECT**: at a level transition, a motion primitive's end-state velocity is snapped to the coarser grid and "might not match," with correction deferred to successor-state generation — an explicit, named cross-resolution mismatch requiring a designed workaround. |
| L4 | Rytz et al. (ASL/ETH), "wavemap," arXiv:2306.01279 | Octree + Haar wavelets; **LiDAR + RGB-D** | Full text (checked twice, targeted prompts) | Discusses only *temporal* update consistency across octree levels ("no redundant coefficients that can go out of sync"). **Does not discuss spatial artifacts, seams, or discontinuities between coarse/fine regions of the same map.** Searched, not discussed. |
| L5 | Hornung et al., OctoMap, Autonomous Robots 2013 | Octree occupancy grid; **LiDAR-common, sensor-agnostic framework** | Full text inaccessible (paywalled/binary on every route tried) | Secondary snippets only (DERIVED/INFERENCE, not verified): inner-node pruning supports multi-resolution *queries* (querying the same tree at a coarser depth than stored). This is a query-time convenience, **not** evidence about what happens when two *neighboring* leaves of different depth interact during raycasting/collision-checking. That specific question remains **unresolved**, not answered either way. |
| L6 | Duberg & Jensfelt, UFOMap, arXiv:2003.04749 | Octree occupancy grid; LiDAR-common | Full text | Does not discuss cross-resolution boundary behavior; focuses on occupancy-probability semantics and update speed. Searched, not discussed. |
| L7 | A-OctoMap, arXiv:2406.13910v2 | Adaptive octree; robotics-native | Full text | Introduces a "SplitBoundary" attribute and claims "geometric consistency," but this refers to grid cells aligning to **obstacle edges**, not to neighbor-node resolution-transition handling. **Terminology false-lead** — flagged explicitly, matching the caution that a hierarchy existing (or even a paper using the word "consistency") does not prove boundary consistency was considered. |
| L8 | ECO, arXiv:2607.05092 | Octree; robotics-native | Full text | Discusses "tree balance" and "structural inconsistency" only in the sense of query-efficiency/AABB-refit after point-stream updates — **not** the geometric hanging-node sense. Another terminology false-lead. |
| L9 | MISO, arXiv:2504.19104 | Submap fusion; robotics-native | Full text | Discusses submap alignment/weighted-feature averaging, not resolution-boundary artifacts. Searched, not discussed. |
| L10 | "Reduced Complexity Multi-Scale Path-Planning on Probabilistic Maps," arXiv:1602.04800 | Quadtree/octree occupancy-probability map for robot-arm configuration-space planning; **map source is synthetic/randomly generated in the reported experiments** (RGB-D/OctoMap mentioned only in the intro as motivating context, not as the actual data source) | Full text (ar5iv, independently re-verified by direct WebFetch in this session) | **Directly confirms the user's caution.** The paper has sections literally titled around same-size/larger/smaller neighbor-finding, which sounds like exactly the right topic — but on direct verification: neighbor-finding is **purely geometric/algorithmic** (tree traversal to locate adjacent nodes). It does **not** describe how occupancy values are aggregated or interpolated across a resolution boundary, imposes **no 2:1-balance or consistency constraint** (arbitrary depth differences between neighbors are explicitly permitted), does **not** identify or discuss artifacts/discontinuities, and its experiments (runtime/success-rate benchmarks) do not measure resolution-boundary effects at all. **This is a clean, verified example of "hierarchy exists, boundary consistency not considered."** |
| L11 | Nguyen et al., "Variable-Resolution Virtual Maps for Autonomous Exploration with USVs," arXiv:2603.22667 (2026) | Adaptive quadtree map, uncertainty-valued; USV (surface vehicle), sensor modality not confirmed in accessible text | Full text | **DIRECT**: names a "split-invariance" problem — naive aggregation of an uncertainty statistic over an adaptive quadtree is biased purely by how finely a region happens to be split ("dividing a coarse leaf into several finer leaves with similar covariances increases the total... simply because the number of terms increases, which can bias decisions"). This is a **decision-bias** artifact from non-uniform resolution, mechanistically distinct from a geometric seam, but part of the same underlying family (resolution non-uniformity → inconsistent downstream conclusions). Confirmed (by direct question to the source) to **not** be about cell-boundary geometric discontinuities. |
| L12 | 2:1-balance / hanging-node terminology (Sundar/Sampath/Biros lineage, Oden Institute PADAS group) | FEM/AMR octree balancing | Snippet-only (PDF fetch failed twice; DERIVED/INFERENCE level) | The formally rigorous terminology for this class of problem ("hanging node," "2:1 balance") comes from finite-element/PDE meshing. **No robotics/LiDAR-mapping paper found in this search imports this terminology** — robotics octree papers that mention "tree balance" (A-OctoMap, ECO, above) mean something different (query efficiency / obstacle-edge alignment), not the geometric-consistency sense. |

### 2b. Cross-domain evidence (explicitly NOT LiDAR/robotics — transferability is an open question in every entry, not asserted)

| Domain | Source(s) | Named mechanism / finding | Category | Evidence level |
|---|---|---|---|---|
| Terrain rendering (graphics) | Geometry clipmaps (Losasso & Hoppe 2004); ROAM (Duchaineau et al. 1997); geomipmapping (de Boer 2000) | "T-junctions"/"cracks" at LOD boundaries; fixed via seam/stitching geometry, forced splitting, or per-edge index buffers | A + C | DIRECT (clipmaps, via secondary source) / DERIVED (ROAM, geomipmapping, via search summaries) |
| Terrain rendering (graphics) | "Skirts" technique (practitioner sources) | Hides (does not repair) the seam via hidden vertical geometry; introduces its own secondary artifacts | C, with a documented downside | DIRECT |
| Mesh/LOD terminology (graphics) | T-vertices (Wikipedia, citing mesh-simplification literature) | Same geometric phenomenon as T-junctions; breaks downstream mesh algorithms (e.g., subdivision) outright | A + E | DIRECT (definition) |
| FEM / adaptive mesh refinement | deal.II docs; Dendro/DENDRO-KT lineage (Sundar, Sampath, Biros) | Hanging nodes → constraint equations (interpolate from coarser element's basis functions); "2:1 balance constraint" claimed necessary to avoid "numerical errors and instabilities" | A + C | DERIVED (no primary text independently read in full; convergent across multiple secondary sources) |
| Multigrid numerical methods | Briggs, Henson, McCormick, "A Multigrid Tutorial" (2nd ed.) | Restriction/prolongation operator accuracy order must match PDE order; boundary/interface regions documented as higher-error zones | D | DERIVED |
| Real-time rendering (general LOD) | Wikipedia "Popping (computer graphics)," citing Chover et al. 2009, Luebke et al. 2002 | "Popping" = abrupt visible LOD-switch artifact; fixed via alpha cross-fade (costly, causes ghosting) or geomorphing (interpolate vertex positions over a transition window) | A + C | DIRECT (definitions), DERIVED (mechanism transfer to LiDAR unconfirmed) |
| Real-time rendering (game engines) | Unreal/Godot/DigitalRune/three.js LOD-hysteresis docs | "Hysteresis" — asymmetric switch-up/switch-down distance thresholds to prevent oscillation/flicker near an LOD boundary | C | DIRECT (engineering docs, not peer-reviewed) |
| Image processing | Laplacian/multi-band pyramid blending (Brown & Lowe / Burt & Adelson lineage, via secondary sources) | Blends at each spatial-frequency band with a band-appropriate blend width, avoiding a single sharp seam | C | DERIVED; **the Burt & Adelson 1983 citation itself was not independently re-verified this session** |
| Signal/image processing | Gibbs phenomenon (wavelet/Fourier reconstruction literature) | Spurious oscillation near discontinuities in orthogonal-basis reconstruction | E, weakly relevant | DERIVED, judged low-moderate relevance — flagged as possibly a different phenomenon than the spatial-seam question |

### 2c. Semantic/object-perception-adjacent evidence (mixed: some LiDAR-adjacent, most from 2D vision — domain flagged per row)

| Domain | Source | Finding | Category | Evidence level |
|---|---|---|---|---|
| 2D semantic segmentation (medical/satellite imagery) | Reina et al., Frontiers in Neuroscience 2020, PMC7020775 | Quantified: tiled inference Dice 0.873 vs. whole-image 0.918 (SpaceNet-Vegas); 0.8599 vs. 0.8743 (BraTS); root cause is translation-variant pooling, errors concentrate "along the tumor borders" | A | DIRECT (quantified) |
| 2D object detection (UAV imagery) | "Group Evidence Matters," arXiv:2509.10779 | Naive tiling raises recall to 0.793 but drops precision to 0.499 via duplicate/spurious boxes clustering at tile boundaries; fixed via a DBSCAN-based spatial+semantic gate | A + C | DIRECT (quantified ablation) |
| 2D biomedical image segmentation | SWITi, arXiv:2607.18990 | Introduces quantified metrics (FRT/ASV) that detect seam artifacts via gradient-statistic permutation tests across tile boundaries — confirms the artifact is measurable | A | DIRECT |
| **Octree/sparse-voxel learned 3D perception** (point clouds — closest cross-check to LiDAR-style data of any "measured" result found) | Yang et al., "Interpolation-Aware Padding," ICCV 2021, arXiv:2108.06925 | Standard octree/zero-padding at the edge of populated sparse-voxel regions fills missing neighbors with zero-valued features, corrupting trilinear point-feature interpolation near boundaries; fixed via "interpolation-aware 1-ring padding," improving fine-grained-task accuracy | A + C | DIRECT — **the single strongest piece of evidence that naive default octree boundary-handling is measurably insufficient**, though evaluated on 3D-shape/scene datasets, not confirmed as raw outdoor automotive LiDAR streams specifically |
| LiDAR-native 3D object detection | SASA, arXiv:2201.01976 | Uniform/geometric downsampling loses foreground/small-object information; fixed via semantics-augmented sampling | A | DERIVED (search-summary level, not independently re-verified full text) — about downsampling generality, not resolution-tier-boundary specifically |
| General motion detection | US Patent 11,803,973 | Multi-resolution detection grids explicitly **exclude** boxes found only in the higher-resolution grid, reasoning that "higher resolution grids may detect noise rather than actual motion" — treats cross-tier disagreement as expected and requiring arbitration | D | DIRECT (patent text; not peer-reviewed) |
| — | OctNet, O-CNN, Adaptive O-CNN abstracts | None foreground neighbor-consistency between differently-sized octree cells as a concern | (absence, informative) | Abstract-level only; full text not accessible |
| — | DATMO/grid-based moving-object tracking + resolution-tier boundaries | **No directly relevant evidence was identified in the literature searched.** Two IEEE-hosted DATMO papers were paywalled/inaccessible — this is an access gap, not a confirmed absence. | — | — |
| — | Einhorn ND-tree variable-resolution occupancy quadtree | Discusses memory-compression benefits; **no passage found** addressing objects spanning a fine/coarse boundary | — | — |

## 3. Terminology discovered

- **In LiDAR/robotics mapping**: no single settled term. Papers that touch the issue describe it in plain language ("artifacts... where resolution changes between neighboring cells" — JPL) or solve it without naming it (Funk et al.'s dual-scale hysteresis; Schleich & Behnke's deferred velocity correction). "Split-invariance" (Nguyen et al. 2026) names a related but mechanistically distinct decision-bias effect.
- **In computer graphics**: "T-junction" / "T-vertex," "crack," "popping," "geomorphing," "hysteresis," "skirts," "seam stitching."
- **In FEM/AMR**: "hanging node," "2:1 balance constraint," "conforming mesh," "constraint equations."
- **In multigrid**: "restriction/prolongation operator order," boundary/interface error.
- **In 2D vision**: "tiling artifact," "boundary blur," "intra-class inconsistency."
- **Confirmed false leads** (same words, different meaning — directly relevant to the user's caution): A-OctoMap's "geometric consistency" (means obstacle-edge alignment, not neighbor-resolution consistency); ECO's "tree balance"/"structural inconsistency" (means query efficiency, not geometric hanging-nodes); BADet's "boundary" (means object/instance edges, not grid/resolution boundaries). None of these were stretched into supporting evidence.

## 4. Evidence that the problem exists

Strongest, most directly applicable:
- **L1 (JPL, 2.5D elevation mapping)** — the only source found that is both (a) in the 2.5D/elevation-mapping domain this project cares about and (b) explicitly names the phenomenon as real, in the accessible primary text (not a secondary summary).
- **S-Interpolation-Aware-Padding (ICCV 2021)** — the only source found that *quantifiably* demonstrates a naive octree/sparse-voxel default boundary-handling scheme is insufficient and requires a fix, in a point-cloud/octree representation structurally close to (though not confirmed identical to) LiDAR occupancy octrees.
- **L2 (Funk et al.) and L3 (Schleich & Behnke)** — both engineered explicit, non-trivial mechanisms specifically to manage a scale-transition effect they treated as real enough to design around, in robotics 3D-mapping/planning contexts.
- **Cross-domain convergence** — the same class of problem is independently named, demonstrated, and actively mitigated across at least four unrelated fields (terrain rendering, FEM/AMR, multigrid, 2D tiled vision) that have needed multi-resolution representations for longer than LiDAR robotics has. This does not prove the LiDAR case, but it is a strong prior that the phenomenon is a structural consequence of multi-resolution representations in general, not an artifact specific to one field's data.

## 5. Evidence against the problem (i.e., that it is negligible or absent)

- **L1 itself is also the best evidence for "negligible under some conditions"**: the JPL authors explicitly judge the artifacts acceptable *for their specific task* (flat-terrain safety classification), because the artifacts are confined to non-flat areas which are irrelevant to their decision. This is a scoped, task-dependent negligibility claim, not a general one.
- No source was found claiming the problem is negligible *in general* (Category B was otherwise empty across all three searches).
- Several representation-level designs (OctoMap/UFOMap's multi-resolution query aggregation; wavelet orthogonality in wavemap) do provide *some* principled way to query a multi-resolution structure consistently — but none of these were confirmed to address the specific *neighbor-to-neighbor* case at a resolution boundary; they address *querying-the-same-tree-at-different-depths*, a related but distinct property.

## 6. Existing implicit/explicit solutions

| Mechanism | Source | What it actually does | Structural requirement |
|---|---|---|---|
| Dual-scale hysteresis + max-pooling propagation | Funk et al. | Maintains both old and new scale during a transition window, switching over only once a condition is met | Requires temporary dual storage; representation-agnostic in principle |
| Deferred/corrected velocity at level transition | Schleich & Behnke | Tolerates a temporary mismatch, corrects at the next planning step | Planning-representation-specific (motion primitives) |
| Interpolation-aware 1-ring padding | Yang et al. (ICCV 2021) | Pads empty neighbor voxels near a sparse-region edge with interpolation-aware values instead of zeros | Requires a defined interpolation/feature space around each voxel — likely portable to any voxelized occupancy/feature grid |
| 2:1 balance constraint | FEM/AMR lineage (cross-domain) | Restricts any two adjacent cells to differ by at most one refinement level, structurally bounding the size of any possible discontinuity | **Purely topological** — does not require a mesh or basis functions, making it the most structurally transferable candidate found to a raw octree/quadtree occupancy or elevation grid |
| Hanging-node constraint equations | FEM/AMR (cross-domain) | Expresses a boundary node's value as an interpolation of the coarser element's basis functions | Requires a defined continuous field with basis functions — less obviously portable to a discrete occupancy grid |
| LOD hysteresis | Game engines (cross-domain) | Asymmetric switch-up/switch-down thresholds prevent flicker from small back-and-forth motion near a boundary | Purely a thresholding rule — plausibly portable to any distance/criterion-driven resolution-tier switch, including a temporal (frame-to-frame) one |
| Seam/skirt/stitch geometry | Terrain rendering (cross-domain) | Explicit mesh-level triangulation or hidden geometry closing a visual gap | Requires a continuous triangulated mesh surface — **not obviously portable** to a voxel/grid occupancy representation with no mesh |
| Multi-band pyramid blending | Image processing (cross-domain) | Blends at a width proportional to spatial frequency | Addresses photometric continuity across an *overlapping* region, not a discrete sampling-density change — **weakest transfer candidate** |

## 7. Why existing solutions may or may not be sufficient

- **Sufficiency evidence is task-scoped, not general.** The one LiDAR/robotics-mapping-domain source that explicitly discusses this (L1) only argues sufficiency ("we can ignore those artifacts") for a specific downstream task (flat-terrain landing safety). It does not claim — and this note does not claim on its behalf — that the same artifacts would be negligible for terrain-boundary detection, thin-object detection, or dynamic-object tracking, which are exactly this project's SIH requirements.
- **No mechanism found has been validated on 2.5D LiDAR ground-vehicle data.** Every candidate mechanism in §6 comes from a different representation (dense mesh, finite-element field, sparse-voxel learned features, rendering thresholds) or a different task (drone trajectory planning, aerial landing-site safety). None has measured before/after error magnitude in the specific setting this project cares about.
- **The most structurally promising candidate (2:1 balance) is unproven for this use case.** It is attractive because it is purely topological and therefore representation-agnostic in principle, but no source — LiDAR-native or cross-domain — was found demonstrating it applied to, or shown necessary for, an occupancy/elevation/semantic LiDAR grid. Its "numerical errors and instabilities" justification is itself DERIVED-level evidence (not independently confirmed via primary-text reading in this search), so its own strength should not be overstated.
- **Ad hoc fixes address specific symptoms, not the general problem.** Dual-scale hysteresis (Funk et al.) addresses temporal transition smoothing during a scale change at one point but was not evaluated for cross-neighbor geometric consistency between two simultaneously-present resolution tiers (the SIH's "near = fine, far = coarse" scenario, where the boundary is spatial and persistent, not merely a transient update event). Interpolation-aware padding addresses feature-interpolation correctness in a learned pipeline but says nothing about geometry (elevation/slope) consistency.

## 8. Applicability to our SIH problem

The following is first-principles technical reasoning grounded in the representation properties already documented for this project's own candidate mechanisms (distance-tiered 2.5D grids per RoadRunner M&M; semantic/uncertainty-weighted octrees per Larsson et al.; SDF-variance-driven adaptive maps per MrHash). **This section is INFERENCE/HYPOTHESIS, not literature-demonstrated for the SIH case specifically** — it explains *why* the evidence in §2–§7 is plausibly relevant, not that the effects have been measured for this project's exact setup.

1. **Geometry** — A coarse cell storing one height/slope value over the same physical footprint that several fine cells describe individually will, by construction, produce a discontinuous slope/roughness estimate exactly at the tier boundary whenever the underlying terrain is not perfectly flat there — this is a logical consequence of quantization, not a hypothesis requiring new data to establish existence; L1 corroborates that this occurs on real terrain and is confined to non-flat regions. What remains unmeasured for this project is the *magnitude* relative to real terrain variation, and whether it fools a downstream traversability classifier.
2. **Semantics** — A coarse cell spanning two real semantic classes must resolve to a single label or a distribution; a class boundary that falls inside a coarse cell gets geometrically "snapped" to the coarse cell's edge, which will generally not align with the resolution-tier boundary. §2c's tile-boundary segmentation evidence (Reina et al., quantified Dice drop specifically "along... borders") is the closest measured analogue, though from 2D vision, not 2.5D LiDAR semantics.
3. **Object perception** — An object straddling a tier boundary can be split between a fine-side partial representation and a coarse-side absorbed representation; §2c's tile-based object-detection evidence (arXiv:2509.10779, quantified precision drop from boundary-clustered duplicate/fragmented detections) is a directly analogous, though 2D and non-LiDAR, measured precedent. Whether the LiDAR-side outcome is fragmentation, a missed object, or a duplicate detection would depend on the specific fusion/aggregation rule used at the boundary — none of which has been specified or chosen for this project yet.
4. **Dynamic perception** — If the resolution-tier boundary is itself robot-relative (as in the SIH's stated "fine near robot, coarse far away" example), a static object near the boundary can flip between fine and coarse representation purely from robot motion, independent of any real-world change. This is the clearest candidate for a genuinely temporal artifact (analogous to graphics "popping"/flicker, §2b), and the hysteresis mechanism found in that literature is the most directly portable candidate mitigation — but no source found has tested hysteresis for a spatially-defined (rather than distance-to-camera) resolution boundary in a mapping context.
5. **Mapping** — Aggregating multiple fine "occupied" cells into one coarse cell requires an aggregation rule (any-occupied? majority? probabilistic fusion?); if this rule is applied inconsistently at partially-observed boundary regions versus fully-interior coarse regions, an inconsistency specific to the boundary band could result. This is exactly the class of problem the FEM 2:1-balance/hanging-node literature was built to solve for continuous fields — whether an occupancy grid's discrete probability values have an analogous continuity requirement is the open question flagged in §7.
6. **Navigation** — A resolution-induced false slope/roughness discontinuity (item 1) could register as a false obstacle or false ledge under a naive traversability classifier; conversely a real small hazard entirely inside a coarse cell near the transition (arguably the worst place for this to happen, since it is also the near-horizon region a planner is about to act on) could be smoothed away. If tier boundaries move with the robot, a path planner could see a cell's traversability cost change from pure resolution reassignment rather than new evidence, a mechanism structurally similar to the "false replanning trigger" risk implied by Schleich & Behnke's need to tolerate transition mismatches in a planning context.

## 9. Feasibility experiment — design, implementation, and results

**Question tested:** "Are resolution-boundary inconsistencies large enough
to materially affect a 2.5D LiDAR terrain/object/dynamic-perception
system?" This is a small, targeted synthetic experiment answering that one
question — it is not the SIH pipeline, uses no learned model, no real
dataset, and does not choose an architecture. Full code:
`../experiments/resolution_boundary_experiment.py`; full numeric output:
`../experiments/results/resolution_boundary_experiment_results.json`.
Reproducible via `python3 experiments/resolution_boundary_experiment.py`
(pure stdlib, no dependencies, runs in well under a minute).

### 9a. Design (as originally proposed, now implemented)

**Goal:** determine whether resolution-boundary artifacts are measurable in a 2.5D LiDAR-style representation, and whether a lightweight consistency mechanism reduces them, before any architecture commitment.

**Conditions (minimum three, matching the request):**
- **(A) Uniform-resolution baseline** — single fixed cell size across the whole mapped extent.
- **(B) Naive adaptive resolution** — the same map with a simple distance-based (or other single-driver) resolution tier boundary, no explicit consistency mechanism at the transition (matching the default behavior confirmed absent in L10, and structurally similar to RoadRunner M&M's two-tier approach).
- **(C) Adaptive resolution + consistency mechanism** — one or more candidate mechanisms from §6, chosen for structural fit to a grid representation: a 2:1-balance-style constraint on tier-depth difference between neighbors, and/or a hysteresis band on tier-boundary reassignment if the boundary is robot-relative.

**Test scenarios:**
- Static-scene pass: a single (or temporally-averaged) map of a scene with known ground-truth geometry/semantics, to isolate geometric/semantic boundary effects from temporal ones.
- Dynamic-object pass: an object crossing the spatial resolution-tier boundary, to isolate object-perception/fragmentation effects.
- Robot-motion pass: a static object or terrain feature observed over many frames while a robot-relative boundary moves past it, to isolate temporal-flicker effects.

**Metrics (mapped from the user's list to concrete measurement procedures):**
| Metric | Procedure |
|---|---|
| Elevation/slope discontinuity | Compare per-cell elevation/slope error against a common high-resolution reference, split into "boundary-band cells" vs. "interior cells at the same tier"; a systematic gap between the two is the signal. |
| Occupancy consistency | Compare occupancy-probability disagreement between physically-adjacent cell pairs that differ in tier vs. pairs that share a tier. |
| Semantic consistency | Same comparison for a semantic-label/distribution field, if present. |
| Object retention | Detection rate for known small/thin test objects as a function of distance to the tier boundary — looking specifically for a sharp drop at the transition, distinct from the already-documented smooth coarse-resolution falloff. |
| Object localization error | Centroid/bounding-region error for boundary-straddling objects vs. non-straddling objects at the same tier. |
| Boundary-crossing error (boundary-specific) | For a single tracked object crossing the boundary, the discontinuity in its own estimated state at crossing time vs. its own smooth trajectory elsewhere. |
| Temporal stability | Variance/flicker rate of per-cell values for cells that pass through a moving boundary vs. cells that remain in one tier throughout. |
| Traversability consistency | False traversability-class flips localized to boundary bands when fed through a simple slope/roughness classifier, benchmarked against the uniform-resolution condition (A), which has no boundary and therefore no such artifact by construction. |
| Memory | Total map footprint per condition — checking whether mechanism (C) erodes the memory savings already documented for adaptive maps in general (per `03_paper_vs_sih_matrix.md`). |
| Latency | Per-frame update/query time per condition — testing whether the consistency mechanism's likely added cross-tier lookups cost meaningful wall-clock time, directly connected to this project's already-flagged FALO/SPVNAS caution that theoretical overhead does not reliably predict measured cost. |

### 9b. Dataset / data-generation method (documented synthetic construction)

A fully synthetic, closed-form 2.5D world (`World` class): flat ground for
range x&lt;8m; a smooth ~0.3m height step ("curb") over x∈[8,9]; flat higher
ground for x∈[9,14]; a further gentle continuous slope (+0.2m over 6m) for
x∈[14,20]. A semantic class boundary at y=0.13 (offset deliberately so it
never sits exactly on a grid line at any tested cell size — a class
boundary aligned with the grid could never be split by a single cell,
making semantic mixing structurally untestable). Static thin poles (radius
0.05/0.15/0.4m, height 1m) placed at documented offsets from the
resolution-tier boundary R_b. One moving object (radius 0.15m) crossing R_b
at constant 1.0 m/s.

Ground points are sampled from a dense (azimuth × radius) polar grid
(azimuth −30°..30° step 0.3°; radius 3..22m step 0.25m) rather than a
literal multi-channel ray-cast — a documented simplification that still
reproduces the real, literature-cited property that lateral point spacing
(and hence areal point density, ≈1/r) grows with range, because azimuth
spacing is held constant while radius spacing is not. Obstacle (pole)
point counts are derived from the angular width the pole actually subtends
at the sensor (2×radius / r) divided by the azimuth step, not from a fixed
per-object budget — so small/thin/far objects can receive very few or zero
points, rather than detection being guaranteed by construction. Both point
families receive independent Gaussian noise (the swept "sensor noise"
parameter). Occupancy requires ≥2 obstacle points in a cell (not a bare
any-hit rule, which would make missed detection structurally impossible).

### 9c. Representations compared

- **U (uniform)** — single fixed cell size (0.2m) everywhere; serves as
  the resolution ceiling / ground-truth-tracking reference.
- **N (naive tier)** — hard range cutoff at R_b: fine (0.2m) inside,
  coarse (0.2m×k) outside, no consistency mechanism. Matches the default
  behavior directly confirmed absent of any consistency mechanism in the
  literature review (§2a, source L10).
- **C (consistency mechanism)** — N, plus one intermediate resolution
  tier (cell size 0.2m×√k) inserted in a band straddling R_b, bounding the
  adjacent-cell size ratio at each interface to √k instead of k. This is a
  simplified, explicitly documented proxy for the "2:1 balance constraint"
  idea from the FEM/AMR literature (§6) — not a literal reproduction of
  octree 2:1-balancing.

### 9d. Metrics and results

All figures below are exact output from the actual script run (not
estimated), evidence-labeled **DIRECT EVIDENCE — this project's own
synthetic experiment** (to be kept distinct from DIRECT EVIDENCE sourced
from published external papers elsewhere in this project). Baseline
configuration: R_b=10m, k=4, sensor noise σ=0.02m, h_fine=0.2m.

**Elevation error** (mean absolute error vs. exact ground truth, meters;
interior_fine / boundary-band / interior_coarse):

| Config | U | N | C |
|---|---|---|---|
| baseline | 0.0097 / 0.0108 / 0.0113 | 0.0097 / 0.0082 / 0.0051 | 0.0097 / 0.0086 / 0.0051 |
| noise=0.0 | 0.0028 / 0.0023 / 0.0009 | 0.0028 / 0.0033 / 0.0037 | 0.0028 / 0.0039 / 0.0037 |
| noise=0.05 | 0.0212 / 0.0251 / 0.0289 | 0.0212 / 0.0162 / 0.0083 | 0.0212 / 0.0157 / 0.0083 |

All differences across every configuration tested stay under ~2cm. At zero
noise, N/C's boundary-band error (0.0033-0.0039) is comparable to their own
interior_coarse error (0.0037) — i.e. not distinctly worse right at the
transition. At noise&gt;0, coarse cells (N/C) show *lower* error than fine
(U) in the interior, because averaging more noisy points reduces variance
more than coarse quantization adds bias on this gently-curved terrain — a
real, legitimate bias-variance effect, not a boundary artifact, and a
useful reminder that "coarser is always less accurate" is not a safe
assumption to build an architecture on.

**Seam-jump** (a targeted metric added during this experiment, distinct
from the band-averaged error above: the discontinuity in a representation's
own height estimate immediately either side of the interface, eps=0.05m —
truer to "elevation discontinuity at the boundary" as literally asked):

| Config | U (noise-floor reference) | N (naive) | C (at nominal R_b) |
|---|---|---|---|
| baseline (R_b=10, flat terrain there) | 0.0016 | 0.0086 (5.4×) | 0.0 |
| R_b=6 (flat terrain there) | 0.0139 | 0.0129 | 0.0037 |
| R_b=14 (right at the start of the slope) | 0.0187 | 0.0094 | 0.0040 |
| k=2 | 0.0016 | 0.0119 (7.4×) | 0.0 |
| k=8 | 0.0016 | 0.0089 (5.6×) | 0.0 |
| noise=0.0 | 0.0 | 0.0 | 0.0 |
| noise=0.05 | 0.0140 | 0.0217 (1.55×) | 0.0 |

N's excess jump over U's own noise-floor is clearest specifically when the
boundary sits on otherwise-flat terrain (baseline, k=2, k=8: 5.4-7.4× the
noise floor); when the boundary happens to sit on genuinely curved terrain
(R_b=6, R_b=14), the terrain's own curvature already produces a large
"floor" jump even under uniform fine resolution, and the naive tier switch
adds comparatively little on top of it. **C shows zero excess jump at the
nominal R_b in every configuration — but this is partly by construction**:
a supplementary direct probe of C's own *actual* interfaces (relocated to
R_b±0.4m for k=4) found jumps up to 0.0256m, comparable to or larger than
N's single jump. **The consistency mechanism relocates the discontinuity to
two smaller-ratio interfaces; it does not reliably shrink the worst-case
jump magnitude.**

**Occupancy mismatch** (fraction of query locations where a representation's
occupancy disagrees with exact ground truth; boundary-band / interior_coarse):

| Config | N | C |
|---|---|---|
| baseline | 0.0255 / 0.016 | 0.0159 / 0.016 |
| R_b=6 | 0.005 / 0.0137 | 0.0383 / 0.0137 |
| R_b=14 | 0.0459 / 0.0221 | 0.0179 / 0.0221 |
| k=2 | 0.0082 / 0.0046 | 0.0094 / 0.0046 |
| k=8 | 0.0323 / 0.0363 | 0.0145 / 0.0363 |
| noise=0.0 | 0.0281 / 0.016 | 0.0159 / 0.016 |
| noise=0.05 | 0.0251 / 0.016 | 0.0159 / 0.016 |

(U is 0.0 everywhere — the fine-resolution reference essentially reproduces
ground truth.) In 5 of 7 configurations, N's boundary-band mismatch exceeds
its own interior_coarse mismatch (a genuine boundary-localized excess, up
to ~2.1× at R_b=14); at k=8, the general coarse-smearing effect
(interior_coarse=0.0363) actually exceeds the boundary-specific rate,
showing the boundary effect is not always the dominant one at extreme
ratios. **C reduces the boundary rate relative to N in 5 of 7
configurations** (baseline: −38%; R_b=14: −61%; k=8: −55%; both noise
configs: −37% to −44%) **but is worse than N at R_b=6** (0.0383 vs.
0.005) **and roughly tied at k=2** (0.0094 vs. 0.0082) — a real, mixed
result, not a uniform win.

**Semantic-label mismatch** (same structure, against the y=0.13 class
boundary):

| Config | N | C |
|---|---|---|
| baseline | 0.0096 | 0.0159 |
| R_b=6 | 0.0152 | 0.0253 |
| R_b=14 | 0.0092 | 0.0149 |
| k=2 | 0.0082 | 0.0 |
| k=8 | 0.0099 | 0.0169 |
| noise=0.0 | 0.0105 | 0.0159 |
| noise=0.05 | 0.0094 | 0.0159 |

**C is worse than N in 6 of 7 configurations** — the graduated
intermediate-resolution tier, as implemented, *increases* semantic
boundary-mismatch rather than reducing it, in the large majority of tested
settings. This is a real, demonstrated cost of this specific mechanism, not
merely an absence of benefit, and should not be downplayed.

**Object detection / fragmentation** (static poles at offsets ±2.4m
[well clear of the boundary] and ±0.4m/0.0m [near/at it] × 3 sizes):
across the entire sweep (7 configs × 15 offset/size combinations = 105
tests), **zero missed detections** occurred under the ≥2-point occupancy
threshold within the tested range (up to ~22m) and size range (down to
0.05m radius). A supplementary probe confirmed misses are structurally
possible in this model (a 0.03m-radius pole at 21m yields only 2 points,
right at the threshold) but did not occur within the parameters actually
swept — a boundary condition of this test, not evidence that misses cannot
happen. A concrete, qualitative fragmentation instance was found repeatedly
near the boundary, e.g. baseline, offset=−0.4m, medium object: U=not
fragmented, **N=fragmented**, C=not fragmented — a real case where the
naive representation splits a single object into disconnected occupied
cells that both the fine reference and the consistency mechanism avoid.
However, *aggregate* fragmentation counts across all 9 near-boundary
combinations per config are low and noisy (0-4 out of 9, e.g. R_b=6: U=3,
N=1, C=4 — N shows *fewer* fragmented cases than U there), so this
experiment's sample size is too small to establish a reliable aggregate
fragmentation *rate*, even though the individual qualitative case is real.

**Temporal instability** (frame-to-frame velocity-estimate deviation from
the object's true 1.0 m/s, derived from the occupied cells' own geometric
centers, not from ground truth; at-crossing / deep-coarse-side /
deep-fine-side):

| Config | U | N | C |
|---|---|---|---|
| baseline | 0.20 / 0.48 / 0.28 | 0.40 / 2.20 / 0.28 | 0.40 / 2.20 / 0.28 |
| R_b=6 | 0.20 / 0.47 / 0.28 | 1.13 / 1.13 / 0.28 | 1.13 / 1.13 / 0.33 |
| R_b=14 | 0.20 / 0.48 / 0.27 | 1.13 / 1.13 / 0.27 | 1.13 / 1.13 / 0.33 |
| k=2 | 0.20 / 0.36 / 0.33 | 0.60 / 0.60 / 0.33 | 0.69 / 0.60 / 0.39 |
| k=8 | 0.12 / 0.40 / 0.28 | 1.00 / 2.20 / 0.28 | 1.00 / 2.20 / 0.28 |
| noise=0.0 | 0.20 / 0.41 / 0.36 | 1.13 / 2.20 / 0.36 | 1.13 / 2.20 / 0.36 |
| noise=0.05 | 0.20 / 0.40 / 0.36 | 0.60 / 2.20 / 0.36 | 0.40 / 2.20 / 0.36 |

The deep-fine-side jitter (0.27-0.39 m/s) is a pure quantization floor,
identical across U/N/C (expected — same fine-cell geometry). Crossing the
boundary adds a real, measurable excess over that floor for N/C
(1.4×-4×), but this excess is generally *smaller than or comparable to*
the deep-coarse-side jitter ceiling (0.36-2.20 m/s) that arises simply from
tracking a moving object with large coarse cells, far from any boundary.
**The single largest source of temporal instability in this experiment is
ordinary coarse-resolution quantization, not the boundary crossing itself.**
C shows no reliable improvement over N (identical in 5 of 7 configs,
marginally worse in 1, marginally better in 1).

**Overhead** (grid-build time, ms, for ~15,000-20,000 points; cell count):
C's build time is statistically indistinguishable from N's across all 7
configurations (both in the 24-38ms range with no systematic ordering),
and C's cell count is consistently *at or below* N's in every configuration
(e.g. baseline: N=1542, C=1488; k=8: N=1282, C=1180). **This lightweight
consistency mechanism adds no measurable compute or memory cost** — a
genuinely positive, uncomplicated finding, in contrast to the heavier
mechanisms found in the literature (interpolation-aware padding, dual-scale
hysteresis), which carry documented implementation cost.

### 9e. Sensitivity analysis (one-at-a-time from the baseline)

Swept: boundary location R_b∈{6,10,14}, resolution ratio k∈{2,4,8}, sensor
noise σ∈{0.0,0.02,0.05}. (Object size and object-distance-from-boundary are
swept jointly within every configuration via the 3-size × 5-offset object
grid, not as separate top-level configs.) Effects found:
- **Boundary location matters less than expected on its own** — what
  matters more is whether the boundary happens to coincide with genuinely
  curved terrain (R_b=14) vs. flat terrain (R_b=6, R_b=10): the seam-jump
  "excess" is clearest on flat terrain, and the terrain's own curvature can
  dominate when the two coincide.
- **Larger resolution ratio (k=8) increases the general coarse-smearing
  effect enough to rival or exceed the boundary-specific excess** — at
  k=8, interior_coarse occupancy mismatch (0.0363) exceeds the boundary-band
  rate (0.0323), the only configuration where this happens.
- **Sensor noise scales elevation error roughly proportionally** (noise=0
  → sub-mm to ~4mm boundary error; noise=0.05 → 1.6-2.9cm) but does not
  change the qualitative pattern of which bin is worst.
- **The consistency mechanism's behavior is not monotonic in any single
  swept parameter** — it helps occupancy mismatch in most configurations,
  hurts semantic mismatch in most configurations, and has no reliable
  effect on temporal instability, regardless of R_b, k, or noise.

### 9f. Practical significance (per downstream task)

| Task | Effect found | Magnitude | Practically significant? |
|---|---|---|---|
| Terrain/slope analysis (elevation) | Real but small | ≤~2cm across every config tested | **Low** — below typical real-LiDAR ranging noise (~2-3cm) and typical slope-classification thresholds (5-15cm) |
| Occupancy-based obstacle mapping | Real, boundary-localized excess in most configs | 0.5-4.6% of boundary-band locations | **Moderate** — modest per-query, but concentrated in a zone a robot-relative scheme keeps re-approaching |
| Semantic terrain classification | Real, boundary-localized; naive consistency fix makes it *worse* | 0.8-2.5% mismatch; consistency mechanism regresses it in 6/7 configs | **Moderate**, plus a concrete caution against assuming "add resolution levels" fixes semantics |
| Static object detection (fragmentation) | Real, concrete individual instances found | Case-level: yes, occurs; aggregate rate: unresolved (sample too small) | **Moderate but unresolved** — needs a larger-scale test to quantify a rate |
| Static object detection (missed detection) | Not observed in tested range | 0/105 tests | **Not demonstrated at tested scales**; structurally possible at smaller/farther extremes not reached here |
| Dynamic object tracking (temporal) | Real, secondary to coarse-tracking jitter | Up to 100%+ of true speed as instantaneous error, but ≤ the pre-existing coarse-jitter ceiling in every config | **Moderate** — relevant if a tracker trusts single-frame velocity naively |
| Compute/memory overhead of the tested fix | Not observed | Statistically indistinguishable build time; equal-or-lower cell count | **Not significant** for this lightweight mechanism shape |

## 10. What result would falsify the hypothesis

The working hypothesis is: *"resolution-boundary transitions cause a measurable, boundary-localized excess error/inconsistency beyond what coarse resolution alone already causes, in at least one of the six effect categories."*

This would be falsified by:
- Boundary-band error/inconsistency statistically indistinguishable from same-tier interior error, across all measured categories — would support "exists in principle but negligible in this representation" (Category B), consistent with L1's own scoped negligibility finding.
- Object detection/retention showing a smooth, boundary-agnostic falloff with distance, with no extra drop concentrated at the transition itself — would falsify a *boundary-specific* effect as distinct from the already-well-documented general coarse-resolution small-object-loss effect.
- Condition (B) (naive adaptive, no consistency mechanism) performing statistically the same as condition (C) (with a consistency mechanism) on every metric — would falsify the need for a dedicated mechanism, suggesting the representation's natural query/interpolation behavior already avoids the issue (Category C: implicitly solved).

**Experiment outcome (§9): partially falsified, partially confirmed — the hypothesis survives only in a qualified form.** Boundary-band error was NOT statistically indistinguishable from interior error in most metrics/configurations (elevation error was the closest to indistinguishable, at sub-2cm gaps; occupancy and semantic mismatch showed a real, if modest, 40-100%+ boundary-localized excess in most configurations); no missed detections occurred within the tested range/size sweep (an inconclusive result for that specific sub-question, not a falsification, since a supplementary probe confirmed misses remain structurally possible outside the tested range); and condition (C) did **not** perform the same as condition (B) on every metric — it differed, but inconsistently (helping occupancy mismatch in most configs, *hurting* semantic mismatch in most configs), which is itself informative: it falsifies "a naive consistency mechanism straightforwardly fixes the problem," without falsifying "the problem exists."

## 11. Current confidence level

**Revised twice now: first upward from the prior synthesis checkpoint's "apparently underexplored" framing (after the literature search, §1-8), and now sharpened from literature-based plausibility to measured-but-modest magnitude (after the experiment, §9). Both revisions are recorded in `evidence/claims.md`.**

- Confidence that resolution-boundary effects are a **real, structurally-expected phenomenon**: **high**. Supported by the literature (§1-8) and now directly measured in a controlled synthetic experiment (§9): every metric category tested (elevation, occupancy, semantic, fragmentation, temporal) showed a nonzero boundary-localized effect in at least some configurations.
- Confidence that the magnitude is **large enough to be a dominant or severe problem** for 2.5D ground-vehicle LiDAR terrain/object/dynamic perception: **low**. Every measured effect was modest (sub-2cm elevation; 0.5-4.6% occupancy/semantic mismatch; temporal instability bounded by the pre-existing coarse-resolution tracking-jitter ceiling in every configuration; zero missed detections in 105 tests). The single largest-magnitude effect found (temporal instability at crossing) was consistently smaller than or comparable to an already-present artifact of coarse resolution *by itself*, unrelated to any boundary.
- Confidence that a **naive fix (a simple extra resolution tier) reliably helps**: **low**. It reduced boundary-band occupancy mismatch in 5 of 7 tested configurations, but *increased* semantic mismatch in 6 of 7 — a real, demonstrated cost, not merely an absent benefit. This directly corroborates the literature finding (§6-7) that effective fixes in adjacent domains (interpolation-aware padding, dual-scale hysteresis) are more sophisticated than simple subdivision.
- Confidence that existing mechanisms from other domains (2:1 balance, hysteresis, interpolation-aware padding) would **transfer without modification**: still **low** — untested here; this experiment tested only one simplified, self-designed proxy mechanism, not those specific published techniques.
- **This is not, and should not be treated as, a novel research contribution or a primary project focus.** Per this project's own explicit instruction, the measured magnitudes support **downgrading** resolution-boundary consistency from "candidate central research contribution" to **a real, secondary-priority design constraint** — worth a documented design note for the eventual architecture (avoid naive hard-cutoff transitions in the near-horizon band; if a consistency mechanism is added, verify it does not regress semantic accuracy, as the lightweight mechanism tested here did) — not worth pursuing as this project's main technical direction. See `evidence/claims.md` for the sourced, itemized version of this downgrade decision.

## Reproducibility note

Literature findings (§1-8) are either (a) a directly quoted/verified passage from a primary source (WebFetch), tagged DIRECT, or (b) a search-engine-synthesized summary not independently confirmed against full primary text, tagged DERIVED/INFERENCE — per-row in §2. Two access-limited items (OctoMap's neighbor-interaction behavior; the Burt & Adelson 1983 primary citation) are explicitly flagged as unverified and should not be cited elsewhere in this project as confirmed.

Experiment findings (§9) are DIRECT EVIDENCE from this project's own synthetic feasibility experiment — a distinct evidence source from the external literature above, and one that used no real LiDAR data. Every number in §9d-f is exact script output, not estimated; the full run (all 7 configurations, all metrics) is preserved in `../experiments/results/resolution_boundary_experiment_results.json` and is exactly reproducible by re-running `../experiments/resolution_boundary_experiment.py`. Two implementation bugs were caught and fixed during development (an occupancy rule that made missed detection structurally impossible; a temporal-position estimator that read from ground truth instead of the representation) — both are noted in the script's own history and are called out here so the reported results are understood to be the corrected, not the first-draft, run.
