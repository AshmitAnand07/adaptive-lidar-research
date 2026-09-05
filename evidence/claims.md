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
- Notes: Relevant context for Phase 5 (competing solution approaches) — the supplied set alone under-represents learning-based approaches relative to what Phase 2 external literature may contain; do not conclude from this set alone that classical methods dominate the field.
