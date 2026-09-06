# 02 — Technical Taxonomy

Status: Synthesis checkpoint. Built entirely from research already completed
— Phase 1 (8 supplied papers, `research/papers/*.md`) and Phase 2 (~104
external papers, `external_literature/group_{a..e}_*.md` and
`external_literature/00_inventory.md`). **No new literature search was
performed for this update.** No architecture is selected or recommended.

This supersedes the shorter Phase-2-only taxonomy previously in this file;
that content is preserved and expanded below along the 9 axes requested for
this checkpoint. Evidence levels (DIRECT EVIDENCE / DERIVED / INFERENCE /
HYPOTHESIS / WEB VERIFIED) follow each paper's own analysis file — this
document does not re-assert a paper's technical claims without that backing.

---

## Axis 1 — Spatial Representation

| Representation | Supplied papers | External papers (representative) |
|---|---|---|
| **2D** (no height) | — | Elfes occupancy grids; DOGMa lineage (Nuss, Danescu, Schreiber, Jang); MotionNet; Kraetzschmar quadtree; Stache et al. UAV (flat field) |
| **2.5D** (height/elevation per 2D cell) | STM (#1), Graph SLAM mapping (#4), motion grids (#5), evidential grids (#6), lightweight SLAM (#8) — 5 of 8 | MEM; RoadRunner; **RoadRunner M&M**; Fankhauser elevation mapping; Multi-Res. Elevation Mapping (Planetary Rotorcraft); Adaptive Patched Grid Mapping; PointPillars' pillar pseudo-image (height folded into learned feature) |
| **3D** (unrestricted) | Metric-semantic mapping (#2), αLiDAR (#3), Variable-Resolution NDT (#7) — 3 of 8 | VoxelNet, SECOND, MinkowskiEngine base; SSMI; Larsson et al.; OctoMap; wavemap; Adaptive-LIO; VoxelMap; D-Map; MrHash |
| **Mesh** | STM (triangular surface mesh) | Metric-semantic mapping's marching-cubes-extracted mesh (supplied #2, listed here for representation type though counted as 3D above) |
| **NDT (Normal Distributions Transform)** | Variable-Resolution NDT (#7) | — (no external NDT-specific paper found; VoxelMap uses plane/edge features, a related but distinct geometric-primitive map) |
| **BEV / pseudo-image** | — | PointPillars, MotionNet, SegNet4D, dynamic OGM w/ BEVFusion, MURAL, Agile3D |
| **Range image** | — | LMNet (spherical projection) |
| **Cylindrical / polar** | — | Cylinder3D (cylindrical voxel binning) |
| **Octree / quadtree** | — (Variable-Resolution NDT uses an Octree for indexing, but the *resolution policy* is curvature-driven point-density capping, not tree-depth adaptivity per se) | OctoMap; A-OctoMap; SSMI; Larsson et al.; Langerwisch & Wagner; Kraetzschmar; Funk et al.; wavemap (wavelet-hierarchical, octree-adjacent) |
| **Sparse voxel hash** | — | Voxel Hashing (Nießner 2013); Spatio-Temporal Voxel Layer; MrHash |

**Observation**: the supplied set is 2.5D-heavy (5/8) with no full-3D-vs-2.5D
consensus; the external set spans every representation family with roughly
even weight, and includes representation types (cylindrical/polar, sparse
hash) entirely absent from the supplied set.

## Axis 2 — Resolution / Adaptation Driver

| Driver | Supplied | External (representative) |
|---|---|---|
| **Fixed (no adaptation)** | 6 of 8 (all except Variable-Res. NDT #7, which is curvature-driven) | Majority of both Group C (terrain/semantic mapping) and Group D (dynamic perception) — this remains the empirical default even in 2024-2025 systems |
| **Distance-based** | — | **Adaptive-LIO**; **RoadRunner M&M** (2 discrete tiers); range-based point-cloud density optimization; Cylinder3D (implicit, via coordinate system) |
| **Curvature / geometry-based** | Variable-Resolution NDT (#7) | VoxelMap (plane/edge); OctNet (occupancy geometry) |
| **Semantic-based** | — | **Larsson et al.** (explicit class-weighted objective); Stache et al. (UAV altitude tied to class-pixel ratio); MAP-ADAPT (semantic+geometry); TSDF Adaptive-Res. paper |
| **Uncertainty/variance-based** | — | **MrHash** (SDF variance); Langerwisch & Wagner (sensor-error bounds); Variable-Resolution Virtual Maps USV (SLAM uncertainty) |
| **Object-based (ROI around detected objects)** | — | AdaOcc (fine detail in object-centric ROIs) |
| **Risk-based** | — | None found where *risk* (as opposed to uncertainty) drives *resolution* — RAMP/STEP/EVORA/RiskMap all use risk to shape planning/cost, not cell size (see Axis 5 note) |
| **System-load / deadline-based** | — | **MURAL** (deadline-driven, temporally not spatially adaptive); Agile3D (contention+content jointly) |
| **Learned (importance/attention)** | — | Focal Sparse Conv; SD-Conv; PointSplit; FOVEA; Fast Attention-Based Simplification |
| **Hybrid / multi-driver** | — | MAP-ADAPT (semantic + geometric complexity + available compute — the most multi-driver example found); Agile3D (content + system contention) |

**Observation**: at least 8 structurally distinct drivers have independent
published precedent (up from the 6 the SIH problem statement anticipates).
No paper combines more than 2-3 drivers; a policy combining distance (coarse
prior) with semantic/uncertainty refinement was not identified in the
literature searched.

## Axis 3 — Perception

| Type | Supplied | External (representative) |
|---|---|---|
| **Classical / geometric** | 7 of 8 (all except metric-semantic mapping #2) | OctoMap, wavemap, VoxelMap, D-Map, Funk et al., MrHash, Voxel Hashing, G-VOM, RAMP, STEP, Elfes occupancy grids |
| **Semantic segmentation (learned)** | Metric-semantic mapping (#2) only | MEM, RoadRunner (training-time only), MAP-ADAPT, Larsson et al., SSMI, Terrain-Aware Semantic Mapping (subterranean), SegNet4D, Cylinder3D |
| **Object detection (learned)** | — | VoxelNet, SECOND, PointPillars, SPVNAS, FSD, Focal Sparse Conv, SPS-Conv, Agile3D, MURAL, AdaOcc, Mixture-of-Experts edge detection |
| **Terrain / traversability** | STM (#1, roughness modeling), metric-semantic mapping (#2, central) | RoadRunner, RoadRunner M&M, G-VOM, Terrain-Aware Semantic Mapping, RAMP, EVORA, STEP, Watch Your STEPP, Wellington & Stentz, Multi-Res. Elevation Mapping (Planetary Rotorcraft) |
| **Dynamic-object perception** | Motion grids (#5), evidential grids (#6) — dedicated but offline/qualitative | LMNet, 4DMOS, MambaMOS, SegNet4D (MOS lineage); PointPWC-Net, SeFlow, Flow4D, SemanticFlow (scene-flow lineage); Nuss/Danescu/Schreiber (DOGMa lineage); MotionNet; DynORecon |

**Observation**: the supplied set has essentially one learned-perception
example (metric-semantic mapping) against seven classical methods; the
external set is dominated by learned methods across every perception type.
Dynamic-object perception is the one capability with a large, mature,
independent external literature (MOS + scene-flow + DOGMa lineages) that was
almost entirely absent from the supplied set's actual demonstrated
capability (motion grids and evidential grids are dedicated DATMO papers but
both offline/qualitative-only).

## Axis 4 — Temporal / Dynamic Handling

| Mechanism | Supplied | External (representative) |
|---|---|---|
| Incremental frame-to-map/frame-to-frame fusion (no explicit dynamics model) | STM, Graph SLAM mapping, metric-semantic mapping, Variable-Res. NDT, lightweight SLAM — the majority | OctoMap, wavemap, VoxelMap, D-Map, Funk et al. |
| Kalman/particle-filter object tracking | Motion grids (#5) | Nuss/Danescu DOGMa lineage, DynORecon, MURAL's downstream tracker |
| Recurrent/sequence-native learned temporal fusion | — | 4DMOS (sparse 4D conv, receding horizon), MambaMOS (state-space model), Flow4D (5-frame 4D voxel fusion), PointRNN |
| Predictive/forecasting of future state | — | SOGMP/SOGMP++, "Learning Spatiotemporal OGMs for Lifelong Navigation" |
| Evidential/belief-based temporal fusion | Evidential grids (#6) | EviLOG |
| Offline post-hoc temporal refinement (not real-time) | Lightweight SLAM (#8) | — |

**Observation**: no supplied paper does learned sequence-native temporal
fusion (4DMOS/MambaMOS/Flow4D-style); this entire sub-family exists only in
the external literature.

## Axis 5 — Uncertainty (five distinct sub-types found; do not treat as one thing)

1. **Sensor/measurement noise** — Elfes-lineage occupancy grids, EviLOG, Langerwisch & Wagner (bounded-error model). Supplied: implicit in Graph SLAM mapping's GNSS/INS-RTK error correction.
2. **Occupancy-state probability itself** — all classic Bayesian occupancy grids, evidential grids (#6, supplied).
3. **Semantic-classification confidence** — E2-BKI. No supplied-paper analogue (metric-semantic mapping #2 does not report calibrated semantic confidence).
4. **Model/epistemic confidence over predicted/extrapolated regions** — SOGMP, Uncertainty-driven Planner. No supplied-paper analogue.
5. **Registration/alignment-fit uncertainty** — Uncertainty-Aware VI-SLAM's submap alignment; **the supplied Variable-Resolution NDT paper's (#7) NDT probability-density mixture model is a direct instance of this type.**
6. **Terrain-surface-shape uncertainty** — a sixth type, found in the supplied set: STM's (#1) Bayesian message-passing/loopy-BP inference over the mesh is a genuine, distinct uncertainty type not matching any of the five external-literature types above cleanly (closest to type 1, but modeling the *inferred surface* rather than raw sensor noise).

**Related, frequently conflated concept — risk**: a decision-theoretic
property of planning consequences (CVaR tail-risk in STEP/EVORA/RAMP/
CVaR-MPPI), not a property of the spatial representation itself. The
clearest illustration is CVaR-MPPI, which is rigorously risk-aware with no
spatial map at all.

## Axis 6 — Spatial Data Structures

| Structure | Supplied | External (representative) |
|---|---|---|
| Regular grid (uniform cells) | Graph SLAM mapping (2D intensity/elevation images), motion grids, evidential grids | Elfes grids, DOGMa lineage, PointPillars, MEM, RoadRunner |
| Triangular mesh | STM | Metric-semantic mapping's marching-cubes mesh (supplied #2) |
| Voxel grid (dense) | Metric-semantic mapping (TSDF), αLiDAR (implicit) | VoxelNet, G-VOM |
| Voxel grid (sparse/hashed) | — | Voxel Hashing, MrHash, Spatio-Temporal Voxel Layer, SECOND, MinkowskiEngine |
| Octree | Variable-Resolution NDT (indexing only) | OctoMap, A-OctoMap, SSMI, Larsson et al., Funk et al., HOTFormerLoc |
| Quadtree | — | Kraetzschmar, Langerwisch & Wagner, Variable-Resolution Virtual Maps (USV) |
| Wavelet-hierarchical | — | wavemap |
| Continuous/non-parametric field | — | Gaussian Process Occupancy Maps, E2-BKI (kernel-based) |
| Hybrid grid-of-octrees | — | OctNet |
| Cylindrical partition | — | Cylinder3D |

## Axis 7 — Computational Efficiency (measured, not theoretical, evidence only)

| Evidence pattern | Supplied | External (representative) |
|---|---|---|
| Explicit real-time claim with hardware, quantified | Metric-semantic mapping (<7ms/frame, GPU), αLiDAR (~37ms) | MEM (2.6-23.6ms), Agile3D (85-476ms Jetson), FSD (2.4x vs. dense at 200m), Flow4D (15.1 FPS RTX3090) |
| Compute reduction reported but no accuracy/hardware caveat given | Variable-Resolution NDT (memory only, not compute) | SPADE (36-89% compute cut) |
| **Direct evidence that FLOPs/cell reduction ≠ measured speedup** | — | SPVNAS (7.6x theoretical → 2.7x measured), FALO (sparse *losing* to dense on real edge silicon) |
| No computational figures reported at all | STM, Graph SLAM mapping, motion grids, evidential grids | Majority of Group C/D papers (RoadRunner reports latency; most terrain/dynamic papers do not) |

## Axis 8 — Memory Efficiency (measured, not theoretical, evidence only)

| Evidence pattern | Supplied | External (representative) |
|---|---|---|
| Quantified memory reduction vs. a stated baseline | Variable-Resolution NDT (36-80% of baseline, 4 environments) | **MrHash (~4x reduction)**, RoadRunner M&M's own reduced footprint (not separately quantified from latency), SPADE (custom silicon) |
| Quantified absolute memory footprint (not a reduction ratio) | Lightweight SLAM (130-133MB peak, embedded) | MEM (~1.6MB additional multi-modal layers) |
| Qualitative "reduces memory" claim only | — | Adaptive Patched Grid Mapping, wavemap, MAP-ADAPT |
| Memory-bound / explicit limitation | Metric-semantic mapping (GPU-memory-bound, explicit limitation) | — |

## Axis 9 — Localization / SLAM Dependence

| Pattern | Supplied | External (representative) |
|---|---|---|
| Paper performs its own localization/odometry (SLAM/LIO) | Graph SLAM mapping (Graph SLAM), Variable-Resolution NDT (scan-to-map NDT, no loop closure) | VoxelMap, Adaptive-LIO, D-Map (implicit), Funk et al. |
| Paper depends on externally-supplied pose (GPS/IMU, no self-localization) | Motion grids, evidential grids (external GPS/IMU) | SSMI, Larsson et al. (exploration context, pose assumed) |
| Paper's core contribution *is* localization/pose estimation | αLiDAR (pointwise-uncertainty-aware LIO) | Uncertainty-Aware VI-SLAM, SPAQ-DL-SLAM |
| Localization not applicable / not addressed | STM (uses landmark-relative submaps + demo poses from ArUco/DGPS, not a general SLAM front-end) | RoadRunner/RoadRunner M&M (pose assumed from separate stack), MEM |
| Metric-semantic mapping (#2) | Integrates with an external LiDAR-Visual-Inertial system; performs mapping given that pose | — |

---

## Cross-Cutting Finding: Resolution-Boundary Consistency (2026-09-06)

A focused follow-up investigation (`resolution_boundary_consistency.md`)
searched LiDAR/robotics-mapping literature, cross-domain literature (computer
graphics terrain LOD, FEM/adaptive mesh refinement, multigrid, image
processing), and semantic/object-perception-adjacent literature specifically
for evidence on what happens at the transition between differently-resolved
neighboring regions — a question that cuts across Axes 1, 2, 4, and 6 above
rather than fitting cleanly into any single axis.

Headline result: one 2.5D elevation-mapping paper (JPL planetary-rotorcraft
landing-site detection, arXiv:2111.06271) explicitly names "artifacts...
where resolution changes between neighboring cells" and judges them
acceptable only for its own flat-terrain safety task; two robotics
mapping/planning papers (Funk et al., arXiv:2010.07929; Schleich & Behnke,
arXiv:2103.14607) engineered ad hoc mitigations without quantifying the
underlying effect; a rigorously-named, structurally transferable candidate
("2:1 balance constraint") exists in the FEM/AMR literature but has not been
found imported into any robotics/LiDAR paper searched; and a directly
adjacent representation (octree/sparse-voxel learned 3D perception) was
found to require an explicit fix (interpolation-aware padding, ICCV 2021)
because its naive default boundary handling was measurably insufficient.
**This revises the prior classification of resolution-boundary consistency
from "apparently underexplored" to "identified in isolated instances and
engineered around ad hoc, but not rigorously measured for 2.5D LiDAR ground-
vehicle perception specifically."** See `resolution_boundary_consistency.md`
§11 for the full, category-by-category confidence breakdown and
`evidence/claims.md` for the sourced claims.

---

## Next Steps

This taxonomy feeds directly into `03_paper_vs_sih_matrix.md` (per-paper
coverage of each SIH requirement and the resulting Gap Map) and
`04_paper_vs_paper_matrix.md` (direct paper-to-paper comparison). See those
files for the requirement-level state classification, intersection analysis,
and the gap-survival assessment for the three candidate gaps flagged at the
end of Phase 2. `resolution_boundary_consistency.md` holds the dedicated
deep-dive on the single gap judged most interesting at that checkpoint.
