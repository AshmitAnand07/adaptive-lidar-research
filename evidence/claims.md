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
