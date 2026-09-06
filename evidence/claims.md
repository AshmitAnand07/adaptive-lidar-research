# Claims Ledger

Status: Empty scaffold. No papers have been analyzed yet — do not add claims
until a paper or external source has actually been read in full.

## Purpose

Track factual claims extracted during literature analysis (Phase 1) and
external research (Phase 2), each tagged with its evidence level per
`CLAUDE.md`:

- **Direct** — explicitly demonstrated by a source.
- **Derived** — logically derived from reported results.
- **Inference** — interpretation based on evidence.
- **Hypothesis** — not yet demonstrated.
- **Web verified** — verified using current external sources.

Never record a claim without a source and an evidence level. Never upgrade a
claim's evidence level without re-checking the source.

## Entry format

```
### <short claim title>

- Claim:
- Source: <filename or external citation> (page/section if applicable)
- Evidence level: Direct | Derived | Inference | Hypothesis | Web verified
- Notes:
```

## Claims

Populated from Phase 1 (supplied-paper deep analysis, 8/8 unique papers).
Full per-claim citations (page/figure/equation) live in each paper's file
under `../research/papers/`; this ledger holds only the headline,
cross-paper-relevant claims.

### No supplied paper implements distance-based adaptive map resolution

- Claim: Across all 8 unique papers, none implements the "fine resolution near the robot, coarser farther away" adaptive grid the SIH problem statement gives as an example. Resolution is either fixed/uniform (papers #1, #2, #4, #5, #6, #8), adaptive but curvature-driven and map-side (#7), or adaptive but achieved entirely via sensor-side rotation control, not map resolution (#3).
- Source: `01_stochastic_triangular_mesh_mapping.md`, `02_realtime_metric_semantic_mapping.md`, `04_graph_slam_25d_lidar_mapping.md`, `05_detection_tracking_25d_motion_grids.md`, `06_evidential_grids_dynamic_object_detection.md`, `07_variable_resolution_ndt_mapping.md`, `08_lightweight_25d_slam_height_aware.md`, `03_alidar_adaptive_panoramic.md`
- Evidence level: DERIVED (cross-paper synthesis of per-paper DIRECT EVIDENCE findings)
- Notes: This is a real gap, not an assumption — see `unresolved_questions.md`, "Is distance-only adaptive resolution sufficient?". None of the supplied papers can answer this; it must come from Phase 2 (external literature).

### Adaptive sensing and adaptive map/computational resolution are cleanly separated in the supplied set — no paper does both

- Claim: αLiDAR (#3) is pure adaptive sensing (physically re-aims/rotates the LiDAR toward a task-specified ROI via an Adaptive Rotation Planning optimizer); the variable-resolution NDT paper (#7) is pure adaptive map resolution (curvature-driven per-voxel point-density capping applied after registration, on a sensor that scans at a constant fixed rate). No supplied paper combines both.
- Source: `03_alidar_adaptive_panoramic.md` (§6-7), `07_variable_resolution_ndt_mapping.md` (§6-7)
- Evidence level: DIRECT EVIDENCE (each paper individually) / DERIVED (the "no paper does both" synthesis)
- Notes: Confirms CLAUDE.md's instruction to keep these two problems distinct — they are empirically distinct in the literature reviewed so far, not just conceptually.

### The only measured map-size-reduction numbers in the supplied set come from one paper, and even there accuracy effects are mixed

- Claim: The NDT paper (#7) reports point-count reduction to 36–80% of baseline across 4 environments (room 61.02%, corridor 62.67%, outdoor 79.86%, conference-room long-run 36.43%), but per-region mapping accuracy (MAE) improves in most but not all regions — two regions (outdoor area 18, conference-room area 16) got slightly worse under variable resolution, a nuance the source paper itself does not discuss further.
- Source: `07_variable_resolution_ndt_mapping.md` (§21, Table 6)
- Evidence level: DIRECT EVIDENCE (the numbers) / DERIVED (that this contradicts a blanket "resolution reduction never costs accuracy" assumption)
- Notes: Directly relevant to CLAUDE.md's caution: "Do not assume that fewer map cells automatically means faster computation" — here it's map size, not computation, that's reduced, and even that isn't uniformly beneficial. No paper in the set reports end-to-end computation/latency change vs. resolution.

### 2.5D and full-3D choices split roughly evenly across the 8 papers, independent of resolution adaptivity

- Claim: Confirmed 2.5D (single height or discretized height-bin per 2D cell): STM (#1), Graph SLAM mapping (#4), motion grids (#5), evidential grids (#6), lightweight SLAM (#8). Confirmed full 3D (no height/Z collapse): metric-semantic mapping (#2, TSDF voxel volumetric mesh), αLiDAR (#3, unrestricted 3D points), variable-resolution NDT (#7, 3D voxels with full covariance).
- Source: item 4 of each paper's analysis file
- Evidence level: DIRECT EVIDENCE (per paper) / DERIVED (the aggregate split)
- Notes: The metric-semantic mapping paper (#2) explicitly self-distinguishes its volumetric 3D choice from "2.5D elevation-map" methods in its own related-work discussion — this is the one supplied paper that argues for 3D over 2.5D, and is worth revisiting in Phase 4 (gap analysis).

### Only one supplied paper performs genuine semantic terrain-traversability analysis, and it shows a concrete failure mode when semantics are removed

- Claim: Metric-semantic mapping (#2) combines geometric mesh features (height-difference, steepness, roughness) with semantic class filtering for traversability, and reports an explicit failure case where grassland is misclassified as traversable when semantic information is excluded (Fig. 8/9).
- Source: `02_realtime_metric_semantic_mapping.md` (§11, §25)
- Evidence level: DIRECT EVIDENCE
- Notes: Direct evidence relevant to CLAUDE.md's disconfirming-evidence question on whether purely geometric (non-semantic) terrain analysis is sufficient — here, in at least one demonstrated case, it is not.

### Dynamic-object handling in the supplied set is either absent, offline/qualitative, or explicitly deferred

- Claim: Dedicated DATMO papers (#5, #6) use fixed-resolution 2.5D grids and are evaluated only qualitatively/offline on KITTI (no FPS, no memory, no quantitative ground-truth metrics reported for #5; #6 reports AP=91.23% on one 114-frame sequence only). Lightweight SLAM (#8) treats dynamics as offline post-hoc map cleanup, not real-time detection/tracking. STM (#1) and the NDT paper (#7) explicitly name dynamic-environment handling as unaddressed future work. αLiDAR (#3) and Graph SLAM mapping (#4) show or filter out moving objects only incidentally, not as a solved capability.
- Source: `05_detection_tracking_25d_motion_grids.md`, `06_evidential_grids_dynamic_object_detection.md`, `08_lightweight_25d_slam_height_aware.md`, `01_stochastic_triangular_mesh_mapping.md`, `07_variable_resolution_ndt_mapping.md`, `03_alidar_adaptive_panoramic.md`, `04_graph_slam_25d_lidar_mapping.md`
- Evidence level: DIRECT EVIDENCE (per paper) / DERIVED (aggregate pattern)
- Notes: No paper in the supplied set demonstrates real-time dynamic-object detection combined with any form of adaptive resolution — this combination does not yet exist as demonstrated evidence anywhere in this set.

### Learned/neural-network components are rare in the supplied set

- Claim: Of the 8 unique papers, only metric-semantic mapping (#2) uses a learned component (a semantic segmentation network, referenced but not detailed in the paper itself). All other 7 papers are purely classical/geometric/probabilistic methods (Bayesian message passing, Kalman filtering, NDT/ICP-style registration, Dempster-Shafer evidence theory, Graph SLAM pose-graph optimization).
- Source: item 18 of each paper's analysis file
- Evidence level: DIRECT EVIDENCE (per paper) / DERIVED (aggregate)
- Notes: Relevant context for Phase 5 (competing solution approaches) — the supplied set alone under-represents learning-based approaches relative to what Phase 2 external literature may contain; do not conclude from this set alone that classical methods dominate the field. **Update after Phase 2:** confirmed — external literature is dominated by learned methods (nearly every paper in Groups B/D/E), so the supplied set's classical skew is a property of that specific 8-paper sample, not of the field.

---

## Phase 2 — External Literature: Hypothesis Verdicts

Six Phase-1-derived hypotheses were adversarially stress-tested against ~100 external papers (see `../external_literature/00_inventory.md` for the full list, and `../external_literature/group_{a..e}_*.md` for full per-paper detail with page/section citations). Each was assigned to 1-3 independent research groups searching different literature families. Verdicts below are consolidated across groups where more than one tested the same hypothesis.

### H1 — "Distance-based adaptive resolution [in LiDAR mapping] is largely unexplored"

- **Verdict: Disproved.**
- Source: `external_literature/group_a_adaptive_resolution_hierarchical.md`
- Evidence level: DIRECT EVIDENCE (multiple independent papers, verbatim abstracts/full text)
- Key counter-evidence: **Adaptive-LIO** (2025, arXiv:2503.05077) explicitly "adjusts map resolution adaptively using multi-resolution voxel maps based on the distance from the LiDAR center" — a persistent map, not merely a proposal. **VoxelMap** (2021, arXiv:2109.07082) established coarse-to-fine voxel mapping as a mainstream LIO backbone, reused across many follow-on systems. **RoadRunner M&M** (2024, arXiv:2409.10940 — found independently by Group C) ships two explicit distance-keyed resolution tiers (0.2 m at ±50 m, 0.8 m at ±100 m) in a real, vehicle-tested 2.5D terrain map. Range-based point-cloud density optimization (2023, arXiv:2306.05663) shows explicit distance-driven density adaptation at the detector-input level, validated across 4 detectors and 2 datasets.
- Nuance: distance is less common as the *sole* driver of a *persistent map's* resolution than geometry/occupancy-homogeneity (OctoMap) or semantics (MAP-ADAPT) — but "largely unexplored" is false regardless.

### H2 — "No existing work combines dynamic-object perception with adaptive resolution"

- **Verdict: Weakened — not disproved, not fully survived.**
- Source: `external_literature/group_d_dynamic_temporal_perception.md`
- Evidence level: DIRECT EVIDENCE for individual mechanisms; DERIVED for the overall pattern (23 papers examined, 48 search queries)
- The large majority of dynamic-perception literature (dynamic DOGMa lineage, LiDAR-MOS lineage LMNet→4DMOS→MambaMOS→SegNet4D, scene-flow lineage PointPWC-Net→SeFlow→Flow4D→SemanticFlow) confirms **fixed spatial resolution** — a repeated, direct finding.
- Two near-misses, neither a clean counterexample: **AdaOcc** (2024, arXiv:2408.13454) has genuine spatially-variable persistent occupancy resolution (fine ROI point-cloud detail vs. coarse background grid) but whether its ROIs are tied to *moving* objects specifically (vs. any detected foreground object) could not be confirmed from accessible text. **MURAL** (2026, arXiv:2607.08391) combines resolution scaling with downstream Kalman-filter dynamic-object tracking, but its resolution adaptation is **temporal/deadline-driven and spatially uniform per frame** — the opposite of the SIH's spatial near/far pattern.
- **Funk et al.** (2021, arXiv:2010.07929) is flagged as the cleanest pure adaptive-map-resolution example found in the entire project (real-time, RA-L, octree-based) — but it explicitly has zero dynamic-object handling, reinforcing that these two capabilities have developed on separate tracks.
- Unresolved lead: **DynORecon** (2024, arXiv:2409.19928) does genuine per-object dynamic reconstruction but its resolution strategy (fixed vs. adaptive) could not be determined from accessible sources — flagged for a follow-up full-text read if this gap becomes decision-relevant.

### H3 — "Semantic-aware adaptive resolution may be an unexplored opportunity"

- **Verdict: Disproved as a general claim; Weakened (narrow gap remains) for the SIH's specific ground-vehicle/2.5D setting.**
- Source: `external_literature/group_b_attention_uncertainty_realtime.md`, `external_literature/group_c_25d_semantic_terrain.md`
- Evidence level: DIRECT EVIDENCE (full-text read for the two central papers)
- **Larsson, Asgharivaskasi, Lim, Atanasov, Tsiotras, "Information-Theoretic Abstraction of Semantic Octree Models"** (2022, arXiv:2209.10035) formalizes an explicit objective letting a robot declare semantic classes "relevant" (weight β) vs. "irrelevant" (weight γ), pruning/expanding octree nodes accordingly — direct, demonstrated semantic-class-driven adaptive resolution, three-plus years before this project, independently confirmed by **Stache et al.** (2021-22, arXiv:2203.01642, UAV altitude tied to detected target-class pixel ratio) in a completely different domain and research group.
- Also relevant: **PointSplit** (arXiv:2504.03654, semantics-aware biased point sampling for on-device 3D detection), **E2-BKI** (arXiv:2509.11964, geometry-adaptive kernels fused with semantic-confidence uncertainty), **FOVEA** (ICCV 2021, saliency-driven variable resolution, camera domain).
- Gap that survives: none of these operate in the SIH's exact target setting — a **persistent 2.5D map for a ground robot** whose resolution is driven by an **explicit semantic-class rule**. Larsson et al. and the SSMI lineage are full unbounded 3D octrees; Stache et al. is flat 2D UAV imagery with no elevation channel. This narrower combination was **not found in the literature searched** (not the same as "does not exist").

### H4 — "2.5D + adaptive resolution + semantic perception may represent a useful gap"

- **Verdict: Weakened, not disproved.**
- Source: `external_literature/group_c_25d_semantic_terrain.md`
- Evidence level: DIRECT EVIDENCE (full-text read for all cited papers)
- The three-way combination (2.5D representation + spatially variable resolution + semantic-driven adaptation) was **not found in the literature searched**, but every pairwise combination exists independently:
  - 2.5D + variable resolution, no semantics: **RoadRunner M&M** (distance-tier-driven), **Multi-Resolution Elevation Mapping for Planetary Rotorcraft** (arXiv:2111.06271, sensing-density/pixel-footprint-driven "dynamic LoD").
  - Variable resolution + semantics, not 2.5D: **Larsson et al.** (full 3D octree, class-weighted).
  - 2.5D + semantics, fixed resolution only: **MEM** (arXiv:2309.16818, uniform 4 cm grid), **RoadRunner** (fixed 20 cm grid, semantics used only for training-label generation, not at runtime).
- Because each pairwise ingredient is independently well-established (especially the very close analogues in Larsson et al. 2022 and RoadRunner M&M 2024), the missing three-way combination reads as a **plausible, low-hanging extension of existing work**, not a deep unexplored frontier — a materially different framing than "nobody has considered any piece of this."

### H5 — "Adaptive map resolution can provide meaningful computational/memory benefits"

- **Verdict: Weakened/Refined — real and demonstrated, but conditional, not automatic.**
- Source: `external_literature/group_a_adaptive_resolution_hierarchical.md`, `external_literature/group_b_attention_uncertainty_realtime.md`, `external_literature/group_e_sparse_representations.md`
- Evidence level: DIRECT EVIDENCE (multiple full-text-verified papers with measured numbers) with significant disconfirming evidence also DIRECT
- **Memory benefits are well-evidenced**: OctoMap, wavemap, Adaptive Patched Grid Mapping, Communication-Aware Hierarchical Map Compression, RoadRunner M&M — all report real memory reduction.
- **Compute benefits are real but hardware- and scale-conditional, not automatic** — this is the load-bearing nuance:
  - **MrHash** (2025, TOG, arXiv:2511.21459) is the clearest genuine *persistent adaptive-map-resolution* example: ~4x memory reduction, up to 13x speedup vs. fixed-resolution baseline, driven by SDF-variance (uncertainty-like), not distance.
  - **DFPS** (2025, Sensors, arXiv/DOI 10.3390/s25144279, full text read) reports up to ~9,278x speedup on real terrain LiDAR data — but its own text states the adaptive-hierarchy overhead **erases the benefit for small point clouds**, and the baseline was non-GPU-accelerated FPS (likely overstating the advantage).
  - **Agile3D** (MobiSys 2025) shows up to +7% accuracy over static detectors at matched latency on real Jetson hardware — but resolution is one of five bundled adaptive knobs on per-frame detection, not an isolated persistent-map effect.
  - **SPADE, FSD, SPS-Conv, SPVNAS** (Group E) show large, hardware-measured compute savings (36-89% reduction, 2.4-10.9x speedup) from **sparsity exploitation** specifically (a related but distinct mechanism from map-resolution adaptivity).
  - **Direct disconfirming evidence**: **FALO** (2025, arXiv:2506.04499) shows sparse convolution *losing* to a re-engineered dense alternative on Jetson Orin GPU and Hexagon NPU — nominally-efficient sparsity can be measurably *slower* on real edge hardware. **SPVNAS** shows a 7.6x theoretical compute reduction yielding only 2.7x measured speedup. A 2026 survey (Pangaliman et al., arXiv:2604.16482, full text read) explicitly found **no rigorous overhead accounting** in the spatial-memory-representation literature it covers, and does not confirm hierarchical structures win once traversal/management overhead is included.
- **Net assessment**: H5 is directionally true and repeatedly demonstrated under the right conditions (matched hardware, sufficient scale, well-chosen adaptivity criterion), but the unconditional version is not supported — this corroborates rather than refutes CLAUDE.md's caution that "fewer map cells" does not automatically mean "faster computation."

### H6 — "Existing adaptive LiDAR work mainly concerns sensing rather than map representation"

- **Verdict: Disproved — with an important internal refinement.**
- Source: `external_literature/group_a_adaptive_resolution_hierarchical.md`, `external_literature/group_e_sparse_representations.md`
- Evidence level: DIRECT EVIDENCE (mechanism/lineage) / DERIVED (aggregate population comparison)
- Map/computation-representation-side adaptive work is far larger and older than sensing-side work in what was found: a continuous lineage from OctoMap (2013) and Langerwisch & Wagner (2013) through wavemap, VoxelMap, D-Map, MAP-ADAPT, Adaptive-LIO (2025), plus the entire sparse-3D-CNN lineage (submanifold sparse conv 2017 → MinkowskiEngine 2019 → SECOND/PointPillars → SPADE/SPS-Conv/SPVNAS/FALO 2022-2025). Sensing-side work (Tasneem et al. 2020 fovea, αLiDAR, MEMS-adaptive LiDAR) is real but smaller and more recent in this sample.
- **Important refinement surfaced by Group E**: within that large non-sensing body of work, a further split matters — **"adaptive computational representation"** (sparsity/pruning on a *fixed*-resolution grid, e.g. nearly all of Group E's sparse-conv papers) vastly outnumbers genuine **"adaptive map resolution"** (a *persistent*, spatially-varying-resolution structure). Only MrHash, OctNet, Funk et al., Adaptive-LIO, D-Map, wavemap, and AdaOcc are real examples of the latter across the entire ~100-paper search. So while H6 as literally stated is false, the truer picture is three populations of very different sizes: sensing-side adaptivity (smallest, found only in Group A/B), computation/representation-side adaptivity on fixed grids (largest, dominates Group E), and genuine persistent adaptive-map-resolution (small but real — consistent with it being a genuine, still-open niche rather than a solved or over-explored problem).

---

## Synthesis Checkpoint (2026-09-06) — Gap Map Claims

Built entirely from Phase 1 + Phase 2 research already completed; no new
literature search performed. Full reasoning, per-paper evidence, and the
complete 16-requirement Gap Map live in `../research/03_paper_vs_sih_matrix.md`;
lineage/competing-approach analysis lives in `../research/04_paper_vs_paper_matrix.md`.
This section holds only the headline, sourced claims.

### Sixteen SIH requirements — state of the literature

- Claim: Of the 16 SIH requirement dimensions assessed, 2.5D representation, elevation/height, and memory reduction are **well solved**; terrain/drivability, semantic perception, static obstacles, dynamic objects, temporal consistency, adaptive resolution (as a general capability), persistent adaptive maps, semantic-driven adaptation, uncertainty-driven adaptation, and real-time computation are **partially solved**; long-range representation is **weakly solved**; multi-driver adaptation and resolution-boundary consistency are **apparently underexplored**.
- Source: `../research/03_paper_vs_sih_matrix.md`, "GAP MAP" section (per-requirement justification and citations)
- Evidence level: DERIVED (aggregated from ~112 papers' DIRECT EVIDENCE findings)
- Notes: "Apparently underexplored" is explicitly not "does not exist" — see the two entries below for the strongest instances of this distinction mattering.

### Resolution-boundary consistency is the single most unaddressed requirement found in the entire project

- Claim: Across all ~112 papers reviewed (8 supplied + ~104 external), zero were found to explicitly analyze, measure, or discuss artifacts/discontinuities at the transition between fine and coarse resolution regions — including RoadRunner M&M, which has exactly such a boundary (two discrete distance tiers) but does not discuss it in the accessible text.
- Source: `../research/03_paper_vs_sih_matrix.md`, "Resolution-boundary consistency" entry
- Evidence level: DERIVED (absence across the full reviewed set) — stated per this project's rule as "not identified in the literature searched," not as "does not exist" or "is a non-issue."
- Notes: Flagged as potentially more technically interesting than the three gaps Phase 2 originally surfaced, precisely because it is a checkable failure mode nobody examined at all (positive or negative), not merely an unassembled combination of existing solved pieces.

### The three Phase-2-flagged gaps, re-classified after paper-vs-paper analysis

- Claim: Gap 1 ("persistent 2.5D map + explicit semantic-class-driven resolution for a ground robot") is classified **likely genuine gap** — the two nearest analogues (Larsson et al. 2022; Stache et al. 2021/22) each fail on a specific, identifiable dimension (full 3D not 2.5D; flat 2D UAV not ground-vehicle) rather than being loosely similar, which raises confidence this is a real gap and not a search-coverage artifact. Gap 2 ("one unified mechanism combining adaptive resolution with dynamic-object perception") is classified **potentially genuine gap** — weaker than Gap 1 because AdaOcc's failure to confirm the dynamic-object half is an access limitation (two failed PDF fetches), not a confirmed absence in the paper itself; a full-text read could change this classification. Gap 3 ("multi-driver resolution policy") is classified **likely integration gap, not a fundamental barrier** — MAP-ADAPT and Agile3D already demonstrate that combining 2-3 drivers is tractable in adjacent settings, so the missing distance+semantic/uncertainty combination reads as an unassembled combination of already-solved parts.
- Source: `../research/03_paper_vs_sih_matrix.md`, "The Three Flagged Gaps — Scrutinized"; `../research/04_paper_vs_paper_matrix.md` §3 (complementary-pair analysis)
- Evidence level: DERIVED (classification reasoning) grounded in DIRECT EVIDENCE per cited paper
- Notes: None of these three classifications is "confirmed genuine gap" — the strongest is "likely," reflecting the standing caution against equating "not found in the literature searched" with "does not exist."

### Driver-conflict arbitration has no identified precedent

- Claim: No paper across the entire search was found to discuss what happens when two adaptivity criteria (e.g., a distance-based rule and a semantic-based rule) disagree about whether a given region should be fine or coarse resolution.
- Source: `../research/03_paper_vs_sih_matrix.md`, "Other gaps that may be more technically interesting than the three flagged," item 2
- Evidence level: DERIVED (absence across the reviewed set)
- Notes: Classified as **insufficient evidence** rather than "underexplored," since no paper was found either solving or explicitly raising this as a named problem — a stronger absence than the other gaps, which at least have papers gesturing toward the combined idea.

## Resolution-Boundary Consistency Investigation (2026-09-06)

Full detail, per-source evidence table, and the full confidence breakdown live in
`../research/resolution_boundary_consistency.md`. This section holds only the
headline, sourced claims — including an explicit revision of the prior
synthesis-checkpoint classification.

### Revision: resolution-boundary consistency is not "apparently underexplored" — it is identified in isolated instances, ad hoc mitigated, but unmeasured for this project's specific use case

- Claim: A focused follow-up search found one 2.5D elevation-mapping paper (JPL/planetary-rotorcraft landing-site detection, arXiv:2111.06271, IROS 2021) that explicitly names resolution-boundary "artifacts" in its own primary text and judges them acceptable only for its specific flat-terrain safety task — directly contradicting the prior claim that literally zero papers discuss this. Two further robotics mapping/planning papers (Funk et al., arXiv:2010.07929; Schleich & Behnke, arXiv:2103.14607) independently engineered explicit mitigation mechanisms for a related scale-transition effect, without naming or quantifying it as a general phenomenon.
- Source: `../research/resolution_boundary_consistency.md`, §2a (L1, L2, L3) and §4-5
- Evidence level: DIRECT (verbatim quotes, independently verified via full-text fetch, in two of the three cases re-verified twice)
- Notes: **This explicitly changes the prior conclusion** recorded above ("resolution-boundary consistency is the single most unaddressed requirement found in the entire project"). The correct, revised statement is: the problem is identified in isolated LiDAR/robotics-adjacent instances and is ad hoc engineered around without being named, characterized, or measured as a general phenomenon — and it has never been evaluated for 2.5D ground-vehicle terrain/object/dynamic perception specifically, which remains a genuine gap in measurement, not in awareness.

### Cross-domain fields that have used multi-resolution spatial representations longer than LiDAR robotics already treat boundary artifacts as a named, actively-solved problem

- Claim: Computer-graphics terrain-LOD rendering ("T-junctions"/"cracks," fixed via seam geometry, skirts, or forced splitting) and finite-element adaptive mesh refinement ("hanging nodes," fixed via constraint equations or a "2:1 balance constraint" argued necessary to avoid "numerical errors and instabilities") both treat this class of problem as real, named, and requiring an explicit engineered solution.
- Source: `../research/resolution_boundary_consistency.md`, §2b
- Evidence level: DIRECT for the graphics-domain definitions and named fixes (via a secondary source); DERIVED for the FEM/AMR "numerical instabilities" framing (search-summary convergence across multiple sources, not independently confirmed by reading one primary text in full)
- Notes: Cross-domain evidence only — explicitly not proof that the same effect occurs, or occurs with the same severity, in a LiDAR occupancy/elevation grid. The "2:1 balance constraint" is flagged as the most structurally transferable candidate found (purely topological, does not require a mesh or basis functions), but this transferability is itself unproven, not assumed.

### The naive default boundary-handling behavior of a hierarchical spatial structure does not automatically avoid the problem — and most robotics papers using such structures never checked

- Claim: A directly-adjacent representation (octree/sparse-voxel learned 3D perception) was found to need an explicit fix — "interpolation-aware padding" (Yang et al., ICCV 2021, arXiv:2108.06925) — because the standard built-in octree/zero-padding scheme produced measurably corrupted point-wise features near the edge of populated regions. Separately, a direct re-verification of a robotics multi-scale path-planning paper (arXiv:1602.04800) that has sections literally titled around cross-resolution neighbor-finding confirmed its neighbor-finding logic is purely geometric/algorithmic and never addresses occupancy-value aggregation, consistency constraints, or artifacts across a resolution boundary at all.
- Source: `../research/resolution_boundary_consistency.md`, §2a (L10) and §2c (interpolation-aware padding entry)
- Evidence level: DIRECT (both independently re-verified via full-text WebFetch in this investigation, not taken from a search snippet)
- Notes: This directly answers the caution that "a hierarchy existing does not prove boundary consistency was considered" — in the one case checked in full, it was not considered at all, despite section titles that strongly suggested it would be.

## Resolution-Boundary Consistency Feasibility Experiment (2026-09-06)

A small synthetic experiment was designed and run (not merely designed) to
test whether boundary effects are large enough to matter. Full metrics,
per-configuration tables, and the practical-significance verdict per
downstream task live in `../research/resolution_boundary_consistency.md`
§9; code and raw results in `../experiments/resolution_boundary_experiment.py`
and `../experiments/results/resolution_boundary_experiment_results.json`.
Evidence level for every claim below: **DIRECT EVIDENCE — this project's
own synthetic experiment** (explicitly distinct from DIRECT EVIDENCE
sourced from published external literature elsewhere in this file).

### Resolution-boundary effects are real and measurable, but modest in magnitude across every metric tested

- Claim: A controlled synthetic experiment (uniform vs. naive two-tier vs. a graduated three-tier "consistency" representation) found a nonzero, boundary-localized effect in every metric category tested (elevation, occupancy, semantic label, static-object fragmentation, temporal tracking), but every effect stayed modest: elevation error differences ≤~2cm across all 7 swept configurations; occupancy/semantic mismatch in the boundary band 0.5-4.6%; zero missed static-object detections across 105 offset×size×config combinations; temporal velocity-estimate error at a moving object's boundary-crossing (up to 113% of true speed in the worst configuration) was in every configuration smaller than or comparable to the jitter already produced by tracking the same object with coarse cells far from any boundary.
- Source: `../research/resolution_boundary_consistency.md` §9d-e
- Evidence level: DIRECT EVIDENCE (own experiment)
- Notes: The single largest-magnitude effect found (temporal instability) was consistently a secondary contributor on top of an already-present coarse-resolution tracking-jitter artifact unrelated to any boundary — i.e., much of what appears as a "boundary" problem is downstream of the more fundamental fact that coarse cells are imprecise in general, not something exotic to the transition itself.

### The tested naive consistency mechanism gives mixed, not uniformly positive, results — and measurably worsens semantic accuracy in most configurations

- Claim: A lightweight graduated-tier consistency mechanism (one intermediate resolution level bounding the adjacent-cell size ratio to √k instead of k) reduced boundary-band occupancy mismatch in 5 of 7 tested configurations (by 37-61% relative to the naive representation) but *increased* semantic-label mismatch in 6 of 7 configurations, and showed no reliable effect on temporal-tracking instability. It added no measurable compute-time or memory overhead in any configuration.
- Source: `../research/resolution_boundary_consistency.md` §9d
- Evidence level: DIRECT EVIDENCE (own experiment)
- Notes: This corroborates, with a concrete demonstrated instance, the literature-review finding (`resolution_boundary_consistency.md` §6-7) that effective boundary-consistency fixes in adjacent domains (interpolation-aware padding, dual-scale hysteresis) are more sophisticated than simple resolution subdivision — "just add another tier" is not a general-purpose or safe-by-default fix, and can regress an unrelated metric (semantics) while helping another (occupancy).

### Revision: resolution-boundary consistency is downgraded from a candidate central research contribution to a secondary-priority design constraint

- Claim: Given the modest measured magnitudes above and the mixed (not uniformly beneficial) behavior of the simplest tested fix, resolution-boundary consistency should not be pursued as this project's primary technical contribution or central research focus. It remains worth carrying forward as a documented design constraint for the eventual architecture (avoid naive hard-cutoff resolution transitions in the near-horizon band; verify any added consistency mechanism does not regress semantic or other accuracy before adopting it).
- Source: `../research/resolution_boundary_consistency.md` §9f, §11
- Evidence level: DERIVED (synthesis of the own-experiment DIRECT EVIDENCE above, not a new independent measurement)
- Notes: This is an explicit revision of the confidence level recorded in the two prior entries above ("resolution-boundary consistency is not apparently underexplored..." and the cross-domain/hierarchical-structure entries) — those established the phenomenon is real and identified elsewhere; this experiment adds that, at the magnitudes actually measured for a 2.5D ground-vehicle-style setup, it is not severe enough to justify being the project's main technical bet.

## Candidate Solution Analysis (2026-09-06)

Full detail, per-direction evidence tables, and the 5 scored system-level
candidates live in `../research/05_candidate_solution_analysis.md`. This
section holds only the headline, sourced claims from the targeted new
research commissioned for this phase (distinct from the broad Phase 2
sweep).

### AdaOcc ROI mechanism resolved — object-aware, not motion-aware

- Claim: AdaOcc's (arXiv:2408.13454) object-centric ROI/high-resolution mechanism is object-detection-driven (DETR-style 900-box regression) and prioritizes by proximity + foreground/background — it applies to all 10 nuScenes classes including explicitly static ones (barrier, traffic cone, construction vehicle), and never uses "dynamic," "moving," "static," or "motion" anywhere in its text.
- Source: `../research/05_candidate_solution_analysis.md` §1.4, full text obtained via `arxiv.org/html/2408.13454`
- Evidence level: DIRECT EVIDENCE (full-text-verified, resolving a Phase-2/3-flagged access limitation)
- Notes: **This revises the earlier synthesis-checkpoint classification of Gap 2** ("potentially genuine gap," with AdaOcc as the reason for hedging toward "possibly already addressed") back toward a firmer **genuine gap** — the most promising near-miss is now confirmed not to solve the dynamic-object tie. No paper found in either search pass ties spatial (not temporal) resolution adaptation specifically to a moving/dynamic object's location or predicted trajectory, evaluated on real LiDAR data.

### Classical Kalman-filter tracking matches or beats a learned tracker on real benchmarks, at a fraction of the compute

- Claim: Two independent, full-text-verified 2024 papers (RobMOT, arXiv:2405.11536; Spb3DTracker, arXiv:2408.05940) each directly benchmark a classical Kalman-filter-family tracker against a learned tracker (PolarMOT) on the same real dataset (KITTI/Waymo) and the classical method matches or beats it on the reported metrics. RobMOT runs at 3,221 FPS on a single CPU core, no GPU.
- Source: `../research/05_candidate_solution_analysis.md` §1.10
- Evidence level: DIRECT EVIDENCE
- Notes: The strongest "lightweight achieves the learned benefit at a fraction of the cost" finding identified anywhere in this project — but specific to *tracking-given-detections*; both trackers still consume deep-learning-produced detections as input, and both required real engineering (adaptive covariance, dynamic UKF) beyond a textbook Kalman filter. Object *detection* itself shows the opposite lean (classical clustering self-limited to sparse/simple scenes; classical features shown additive to, not a substitute for, a deep detector — EG-PointPillar, +3.88% mAP).

### Motion-awareness and resolution-adaptivity are separable design choices

- Claim: S3PM (MDPI Sensors 2026, PMC12845740) builds a motion/dynamics-aware risk field from optical flow around moving objects (measured on real embedded hardware: Raspberry Pi 5 + Hailo-8 NPU, 25-30 Hz, 18-27% higher IoU and 30-45% fewer collisions vs. OctoMap+RRT*) while deliberately never varying spatial resolution.
- Source: `../research/05_candidate_solution_analysis.md` §1.4
- Evidence level: DIRECT EVIDENCE
- Notes: Directly supports this document's own candidate-system design choice (§10, all 5 candidates) of keeping dynamic-object perception as a separate, non-resolution-adaptive subsystem rather than attempting a unified adaptive-resolution+dynamic-object mechanism from scratch (Gap 2).

## Architecture-Selection Evidence Checkpoint (2026-09-06)

Full detail, metrics tables, and reasoning in
`../research/05_candidate_solution_analysis.md` §11. Code and raw results:
`../experiments/driver_ablation_experiment.py`,
`../experiments/results/driver_ablation_results.json`.

### Adding a semantic driver on top of distance is justified; adding an uncertainty-refinement driver on top of that is not

- Claim: In a controlled synthetic ablation (policy A: distance-only; B: +semantic; C: +uncertainty), B corrected resolution allocation in a semantically-critical distant region from 0% to 100% correct and tightened a test object's positional cell size 4x (0.8m→0.2m), for a 5.7% memory and ~20% latency cost, with 100% of its added fine cells landing on genuinely important content. C caught a genuinely non-redundant sensor-noise anomaly (0.88 allocation-correct rate) at a comparable marginal cost (+6.2% cells, +30% latency over B), but made the elevation estimate in that region *worse* (0.0098m→0.0423m MAE, from reduced per-cell noise-averaging at finer resolution) and had a lower targeting-efficiency rate (79.8% vs. B's 100%).
- Source: `../research/05_candidate_solution_analysis.md` §11, Part 1
- Evidence level: DIRECT EVIDENCE (own experiment)
- Notes: **Driver C (uncertainty-driven spatial resolution refinement, as tested) is eliminated from further consideration for the core resolution policy.** This does not eliminate uncertainty-awareness as a concept — only the specific "refine resolution when uncertain" mechanism tested; a different response (e.g. flagging for re-observation rather than subdividing) was not tested. The distance-vs-uncertainty correlation measured in the normal (non-anomalous) part of the synthetic map was weak (−0.197) — INFERENCE-level for generalization beyond this one synthetic terrain, not a general claim about real LiDAR data.

### Semantic-driven 2.5D adaptive resolution is mechanically feasible without a hierarchical data structure — now demonstrated, not only inferred

- Claim: A flat, non-tree, dict-keyed 2.5D grid with a simple binary semantic-override rule ("force fine resolution inside a designated important region, regardless of distance") successfully preserved detail on distant important content in a synthetic experiment, at bounded, modest memory cost (+5.7% cells for a patch covering a small fraction of the map).
- Source: `../research/05_candidate_solution_analysis.md` §11, Part 2
- Evidence level: DIRECT EVIDENCE (own experiment) for the mechanical demonstration; INFERENCE for generalization to a real classifier or full-scale deployment
- Notes: **This upgrades Gap 1's classification** from "likely genuine gap, mechanically plausible per inference from Larsson et al.'s own description" to "mechanically demonstrated feasible at small/synthetic scale, with two specific open items remaining: temporal stability under a real (noisy) classifier, and joint operation with a separate dynamic-object subsystem." Neither open item was tested this phase.

### Classical-vs-learned static-object detection: evidence is insufficient for a confident general claim

- Claim: No paper was found in either research pass that directly benchmarks a classical clustering-based LiDAR detector against a deep 3D detector on the same dataset with both accuracy and latency reported. Existing evidence supports only a narrower claim: classical clustering achieves real measured performance (94.47% recall, 20 FPS) but is self-limited by its own authors to sparse/simple scenes, and classical geometric features added to a deep detector improve accuracy (+3.88% mAP, EG-PointPillar) rather than being redundant with it.
- Source: `../research/05_candidate_solution_analysis.md` §11, Part 3 (synthesized from §1.10, no new search this phase)
- Evidence level: DERIVED (synthesis of DIRECT EVIDENCE already gathered) for the narrower claim; explicitly **insufficient evidence** for the general claim either way
- Notes: This is distinct from *tracking*, where evidence is strong (RobMOT/Spb3DTracker). Conclusion: a hybrid (classical preprocessing + learned detection) is the evidence-backed default over a pure-classical choice, with moderate confidence — not because classical is proven insufficient, but because its proven scope of sufficiency (sparse/simple scenes) is narrower than the SIH's likely full operating envelope.

## Semantic-Resolution Temporal-Stability Checkpoint (2026-09-06)

Full detail, metrics table, and reasoning in
`../research/05_candidate_solution_analysis.md` §12. Code and raw results:
`../experiments/semantic_noise_stability_experiment.py`,
`../experiments/results/semantic_noise_stability_results.json`.

### Raw (unsmoothed) noisy semantic-driven resolution is not viable — it causes substantial memory bloat and per-frame churn

- Claim: In a 30-frame synthetic simulation with per-cell semantic-prediction noise calibrated to a real reported LiDAR segmentation accuracy (90% correct, independently redrawn each frame), unsmoothed noisy semantic-driven resolution inflated mean map size 24% above the perfect-label case (2,010 vs. 1,617 cells, std 70.5) and caused 17.7% of candidate cells to change resolution tier on every single frame transition, with only 53.3% of frames correctly covering the full true-critical region.
- Source: `../research/05_candidate_solution_analysis.md` §12
- Evidence level: DIRECT EVIDENCE (own experiment); the noise-rate calibration itself is DERIVED from a previously-gathered real accuracy figure (LVCA-Net, 91.79% SemanticKITTI)
- Notes: The observed 53.3% full-region-correct rate matches the theoretical prediction (0.9⁶=53.1%) almost exactly, confirming the simulation behaves as designed. This noise model is an intentional worst-case stress test (independent per-frame flips), not a validated model of real classifier error correlation — see the open question below.

### A simple symmetric K=3 persistence counter (hysteresis) resolves the instability at negligible cost

- Claim: Passing the same noisy per-frame semantic predictions through a per-cell counter requiring 3 consecutive same-valued predictions before switching tier reduced tier flips ~77x (17.7%→0.23% per transition), reduced the false-positive rate ~26x (9.75%→0.37% of normal cells), and brought mean memory use within 0.5% of the perfect-label case (1,626 vs. 1,617 cells) — while still correctly covering the true-critical region in 83.3% of frames and the test object in 93.3%, at a measured build-time cost of +9% (10.3ms→11.3ms).
- Source: `../research/05_candidate_solution_analysis.md` §12
- Evidence level: DIRECT EVIDENCE (own experiment)
- Notes: K=5 was also tested and over-smooths (lower coverage, longer delay, no meaningfully better stability than K=3) — K=3 is the better-justified simple mechanism of the two. **This revises Candidate 3's specification**: it must include this hysteresis component as a required part of the design, not an optional refinement; a bare semantic override (as tested without noise in the prior checkpoint) is now known to be insufficient for a real, noisy classifier.

### Research-transparency note: a targeted sub-search was interrupted by a platform rate limit and is reported as incomplete, not answered

- Claim: A commissioned search for (a) direct driver-count ablations isolating each added resolution-driver's marginal contribution and (b) persistent-vs-transient map trade-off literature was interrupted mid-task by a session rate limit before returning a result.
- Source: `../research/05_candidate_solution_analysis.md` §6 (research-transparency note), §7
- Evidence level: N/A — explicitly unresolved, not a finding
- Notes: Per this project's evidence-discipline rules, this is recorded as an open item rather than papered over or guessed at. The simple-vs-advanced ladder (§6) and persistent-vs-transient reasoning (§1.7) in the candidate-solution analysis rest on evidence already gathered in Phase 2 (where no such ablation was found either), not on a completed dedicated search for this phase.
