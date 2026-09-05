# 3D Environment Mapping with a Variable Resolution NDT Method — Deep Analysis

**Source file:** `papers/machines-10-01200-v2.pdf`
**Analyzed:** Phase 1 (supplied-paper analysis), single-paper deep read.

## 1. Problem being solved
The paper addresses unbounded growth of point-cloud map size during long-duration 3D LiDAR mapping caused by repeated scanning of the same space, which eventually bottlenecks online mapping runtime/memory. DIRECT EVIDENCE (Abstract, p.1; Introduction, p.1-2). The proposed fix is a scan-to-map NDT registration pipeline combined with a "variable resolution" map-update strategy that adaptively limits per-voxel point density according to local curvature. DIRECT EVIDENCE (Abstract, p.1).

## 2. Sensors and input data
A 16-line rotating LiDAR (Velodyne VLP-16) mounted on a mobile ground robot, mechanically spun about the vehicle's X-axis to enlarge the field of view (270° FOV, 10 Hz scan frequency, 0.2 Hz X-axis rotation, 0.006 m system accuracy at 5 m range). DIRECT EVIDENCE (p.7, Table 1; Figure 2a). Ground truth for accuracy evaluation was captured by a separate portable single-line laser scanner (Hokuyo UST-30LX, 270° FOV, 40 Hz, rotated ±180° about its Z-axis, 0.003 m accuracy at 5 m range). DIRECT EVIDENCE (p.7-8, Table 2; Figure 2b). No camera, IMU (beyond an implicit motion model), or other sensing modality is used as input to the mapping algorithm itself.

## 3. Input representation
Raw input is a 3D point cloud per LiDAR frame, denoted ᴸᵏC = {ᴸᵏp₀, ᴸᵏp₁, …}, ᴸᵏpᵢ ∈ ℝ³. DIRECT EVIDENCE (p.3-4, notation section). Each scan is first passed through a distance filter (removing near-range points with large error induced by the vehicle body) and then corrected for motion distortion using a constant-turn-rate-velocity (CTRV) model, producing ᴸᵏC′. DIRECT EVIDENCE (p.4, Figure 1, Section 3.1).

## 4. 2D / 2.5D / 3D representation
This is a full 3D representation, not 2.5D. Points remain unrestricted ℝ³ vectors throughout (raw scan, registration, and global map), and the global map is organized as 3D voxels holding a full 3D mean vector and 3×3 covariance matrix (Equations 6-7, p.5). There is no projection/collapse of height into a 2D grid cell and no single height-per-cell field. DIRECT EVIDENCE (p.3-5, notation and Eq. 6-7). The title's claim of "3D Environment Mapping" is corroborated by the actual method (Octree global map of 3D voxels, ℝ³ points, ℝ^{3×3} covariances) — DERIVED from Sections 3.1-3.3.

## 5. Spatial/map representation
The global map ᴹC is a merged 3D point cloud managed by an Octree [31] for efficient voxel queries; per-voxel properties (mean, covariance of local points, curvature, point count) are cached in a hash table H for fast lookup during NDT registration and map maintenance. DIRECT EVIDENCE (p.4, Section 3.1, citing Octree [31] and hash table method [32]). This is a voxelized-point-cloud hybrid: individual points are retained (for map merging/visualization/error evaluation) while voxel-level Gaussian statistics (NDT cells) are additionally maintained for registration.

## 6. Resolution strategy
Voxel edge length L is fixed (used directly in Eq. 19, nₘₐₓ_i = ρ_lim_i·L³); what varies is the maximum permitted point density (and therefore point count) inside each voxel, not the voxel size itself. DIRECT EVIDENCE (p.6, Eq. 17-19). So "variable resolution" here means variable point density per fixed-size voxel, i.e., an adaptive point-cloud downsampling/thinning strategy layered on a fixed-size octree/voxel grid, rather than variable/hierarchical voxel sizing (e.g., not an adaptive octree depth per region as far as reported). INFERENCE — the paper never states voxel edge length L itself changes.

## 7. Whether resolution is adaptive and how
Yes, adaptive — but the adaptivity is CURVATURE-DRIVEN, not distance-driven, and it is entirely MAP/REPRESENTATION-SIDE, not sensor-side.
- Mechanism (map-side): For each voxel Vᵢ in the changed-voxel set, curvature αᵢ = λ₀ᵢ/(λ₀ᵢ+λ₁ᵢ+λ₂ᵢ) is computed from the eigenvalues (λ₀ᵢ≤λ₁ᵢ≤λ₂ᵢ) of the covariance matrix of the points inside that voxel (Eq. 17, p.6). A density upper limit ρ_lim_i is then computed as a piecewise function of αᵢ: clamped to ρ_min below a curvature threshold α_min, clamped to ρ_max above α_max, and linearly interpolated (η·αᵢ) in between (Eq. 18, p.6). The max point count nₘₐₓ_i = ρ_lim_i·L³ (Eq. 19). If the current point count nᵢ exceeds nₘₐₓ_i, the top γ·nₘₐₓ_i points by NDT probability-density value are kept, plus (1-γ)·nₘₐₓ_i more points chosen randomly from the remainder; all other points are discarded (Algorithm 1, p.7). Higher local curvature (edges/corners/complex geometry) → higher permitted density; low curvature (flat planes: floors, ceilings, walls) → lower permitted density. DIRECT EVIDENCE (p.6-7, Eq. 17-19, Algorithm 1; confirmed visually in Figures 4, 7, 10, 13 where flat surfaces are visibly sparser and complex objects denser after variable-resolution processing).
- Confirmation this is NOT sensor-side: the LiDAR's own scanning is unaffected by scene curvature — the VLP-16 spins about the X-axis at a constant, fixed 0.2 Hz regardless of scene content (Table 1, p.8), and there is no mention of adjusting FOV, scan rate, or beam pattern based on the environment. The curvature computation and density limiting operate strictly on the accumulated global-map voxels after scan-to-map registration (Section 3.3, "Map Maintenance"), i.e., post-sensing. DIRECT EVIDENCE (p.7-8, Table 1; p.6, Section 3.3 header and content) / DERIVED (explicit sensor/map separation).
- Also explicitly NOT distance-based: no distance-to-sensor term appears anywhere in Eq. 17-19; the sole adaptivity variable is curvature. DIRECT EVIDENCE (p.6, Eq. 17-18 contain only αᵢ, not range/distance).

## 8. Spatial data structure
Octree (global map indexing, cited to Meagher 1980 [31]) combined with a hash table H (cited to Maurer & Lewis 1975 [32]) that caches per-voxel mean, covariance, curvature, and point count for O(1)-ish lookup during registration and maintenance. DIRECT EVIDENCE (p.4, Section 3.1). During scan-to-map registration, only a local sub-map (the reference voxel Vᵢ plus its 26 adjacent voxels, i.e., a single-layer 3×3×3 neighborhood expansion in the Octree) is queried rather than the whole global map, to bound computation. DIRECT EVIDENCE (p.5, Section 3.2.1).

## 9. Height/elevation representation
Height is simply the z-component of full 3D points (ᴹp ∈ ℝ³) and of the 3D voxel means/covariances; there is no separate/compressed elevation field, no 2D grid-with-height-value structure, and no ground-plane height model. DIRECT EVIDENCE (p.3-6, point/voxel definitions). This confirms the representation is full 3D, not 2.5D (see item 4).

## 10. Semantic information
None. DIRECT EVIDENCE (absence) — no semantic classes, labels, or segmentation appear anywhere in the method (Sections 3.1-3.3). The region labels used in the evaluation tables (e.g., "ceiling," "wall," "floor," "desk," "railing," "car," "tree," "chair," "table" in Tables 3-5,7 and Figures 5,8,11,14) are manually/visually selected by the authors purely to organize the mapping-error (MAE) evaluation; they are not detected, classified, or used by the mapping algorithm itself. DIRECT EVIDENCE (p.10,12,14,17 — "we randomly select some areas," "we selected N areas … to calculate the mapping error").

## 11. Terrain analysis
Not established from the paper. There is no drivable/non-drivable classification, no ground-plane extraction, no traversability or slope estimation anywhere in the method or experiments.

## 12. Static-object perception
Not established as an explicit task. The method registers and maps whole static scenes (room, corridor, outdoor road with parked cars, conference room) as one undifferentiated 3D point cloud/voxel map; there is no per-object segmentation, detection, or bounding-box output. INFERENCE — insofar as the system produces an accurate static 3D geometric map of walls/floors/furniture/parked vehicles/trees, it implicitly supports downstream static-object perception, but the paper itself does not perform object-level static perception.

## 13. Dynamic-object perception
Not established from the paper / effectively absent. All four test environments (room, corridor, outdoor road, conference room) appear to be static or quasi-static scenes; parked cars in the outdoor scene are stationary, not moving. DIRECT EVIDENCE (p.12, "several cars are parked on the road"). The CTRV motion model used in the pipeline corrects distortion caused by the *robot's own* motion during a single scan (ego-motion compensation), not motion of external dynamic objects in the scene. DIRECT EVIDENCE (p.4, Section 3.1) / DERIVED (no dynamic-object filtering, detection, or removal logic appears in Sections 3.1-3.3). The Conclusions explicitly flag this as unaddressed future work ("we may study LiDAR mapping in large-scale dynamic environments," p.18) — DIRECT EVIDENCE that dynamic environments are outside current scope.

## 14. Temporal processing
Limited to sequential frame-to-map registration: each new scan ᴸᵏC is registered against the accumulated global map using a pose prediction from the previous two frames' relative transform (Eq. 2-3, constant-velocity/CTRV-style prediction) followed by NDT optimization refinement (Eq. 10-13). DIRECT EVIDENCE (p.4-6). There is no temporal filtering/smoothing of scene content itself (e.g., no Kalman filtering of object states, no change detection across time beyond map density control) — the "long-time running experiment" (Section 4.4) evaluates map-size growth over time, not temporal object-level reasoning.

## 15. Tracking
Not established from the paper. No object-level tracking (data association, state estimation of moving entities) is present.

## 16. Uncertainty handling
Uncertainty is handled only at the registration/point level, via NDT's per-voxel Gaussian probability density function ξ(p) built from each voxel's mean μᵢ and covariance Σᵢ (Eq. 7, p.5), and via a robust mixture-model objective (Eq. 8-9) that down-weights points with low probability density (treated as outliers) using a normal+uniform mixture with tunable constants d₁, d₂ (p.5, referencing Magnusson 2009 [34] for details). DIRECT EVIDENCE (p.5, Eq. 4-9). This is registration-level/geometric uncertainty (how well a point fits the local Gaussian surface model), not perception-level uncertainty such as occupancy probability, semantic confidence, or map-cell existence probability — none of the latter are reported. Probability density values are also reused in the variable-resolution point-selection step (retaining high-probability-density points preferentially, Algorithm 1, p.7) — DIRECT EVIDENCE.

## 17. Localization / SLAM dependency
The paper's own pipeline performs the localization: scan-to-map NDT registration estimates the robot's frame-to-global-map transform ᴹ_{Lₖ}T (Eq. 4-13) using a CTRV-based initial guess corrected by Newton-method optimization (Eq. 10-11). DIRECT EVIDENCE (p.4-6, Sections 3.1-3.2). This is scan-to-map registration/odometry-style localization; no loop-closure detection, pose-graph optimization, or global back-end SLAM component is mentioned or evaluated anywhere in the paper (references to loop closure [21,33] appear only in the Related Work discussion of other papers' sub-map fusion strategies, not as part of this method). DERIVED (absence in Sections 3-4). So the method is self-contained for local pose estimation but does not claim or demonstrate full SLAM with global consistency/loop closure.

## 18. Learning/neural-network components
None. DIRECT EVIDENCE (absence) — the entire pipeline (distance filter, CTRV motion prediction, NDT scan-to-map registration via Newton optimization, Octree/hash-table map maintenance, curvature-based variable-resolution voxel density control) is purely geometric/probabilistic, with no neural network, learned feature, or data-driven model anywhere in Sections 3.1-3.3.

## 19. Computational requirements
Not reported. No CPU/GPU specification, processor model, memory hardware, or software/runtime environment for the mapping algorithm is given anywhere in the paper (Tables 1-2 describe only sensor hardware, not compute hardware).

## 20. Runtime/FPS/latency if reported
Not reported as an algorithm processing rate/latency metric. The only frequency figures given are sensor acquisition rates (VLP-16: 10 Hz scan frequency, 0.2 Hz X-axis rotation; Hokuyo ground-truth scanner: 40 Hz) (Table 1-2, p.8) — these describe sensing hardware, not the mapping algorithm's compute throughput. Figure 15 (p.17) plots map size against elapsed wall-clock time (0-120 s) for the long-time experiment, but this shows map-size growth over experiment duration, not per-scan processing latency or an FPS figure for the algorithm itself.

## 21. Memory/map-size results if reported
Reported explicitly, DIRECT EVIDENCE, Table 6 (p.15) and text (p.14-16):
- Room environment: 6,173,086 points (without variable resolution) → 3,767,088 points (with) = 61.02% of baseline size.
- Corridor environment: 10,355,562 → 6,490,328 points = 62.67% of baseline.
- Outdoor environment: 10,986,566 → 8,774,072 points = 79.86% of baseline (smaller reduction attributed to fewer low-curvature/planar areas outdoors, p.14-15).
- Conference-room long-time experiment: 17,677,016 → 6,438,981 points = 36.43% of baseline (p.16).
Figure 15 (p.17) additionally shows that without the variable-resolution strategy, map size (point count) grows roughly linearly/unboundedly with time over the 120 s test (red curve), whereas with the strategy the map size grows then plateaus once the physical space has been fully covered (~90 s onward), i.e., map size scales with explored space rather than elapsed time (blue curve). DIRECT EVIDENCE (p.17, Figure 15 and accompanying text).

## 22. Dataset and experimental setup
Self-collected data (no public/benchmark dataset used; "Data Availability Statement: Not applicable," p.18). Four experimental environments, all on/around the authors' campus: (1) a laboratory room with furniture (Figure 3, p.8); (2) a U-shaped indoor corridor with walls on one side and railings on the other (Figure 6, p.10); (3) an outdoor campus road scene with parked cars, trees, and a flower bed (Figure 9, p.12); (4) a conference room with tables/chairs and a non-planar multi-tier ceiling, used for a long-duration repeated-mapping test (Figure 12, p.15). DIRECT EVIDENCE. Ground truth for the first three environments was obtained via the portable Hokuyo scanner rotated on a tripod at multiple stationary positions (Table 2; note in Figure 10's outdoor ground truth there are visible circular gaps because the scanner cannot see under itself and adjacent scan positions were spaced apart, p.12) and aligned to the LiDAR-built map using CloudCompare software (p.10).

## 23. Evaluation metrics
(a) Mapping accuracy: Mean Absolute Error (MAE, in meters) computed by point-to-point comparison between the built map and the ground-truth scan, calculated over manually selected planar/object regions (Tables 3,4,5,7; Figures 5,8,11,14). DIRECT EVIDENCE (p.10). (b) Map size: raw point count of the global map (Table 6, and the time-series in Figure 15). DIRECT EVIDENCE (p.14-17). No other metrics (e.g., no completeness/coverage metric, no runtime/FPS metric, no localization-error/ATE-RPE metric) are reported.

## 24. Baselines and ablations
The only comparison performed is an internal ablation of the paper's own pipeline: "without variable resolution" (scan-to-map NDT mapping alone) vs. "with variable resolution" (the same pipeline plus the proposed curvature-based density control), applied identically across all four environments (Tables 3-7). DIRECT EVIDENCE. No comparison against any other published mapping/compression method cited in the Related Work section (e.g., [18]-[29]) is carried out experimentally. DERIVED (absence of any such comparison in Section 4).

## 25. Failure cases
The variable-resolution strategy does not uniformly reduce error in every tested region. DIRECT EVIDENCE:
- Outdoor environment (Table 5, p.14): of 30 regions, the text states 28 improved; inspecting the reported numbers directly shows area 16 (flower bed) is essentially unchanged (0.0327 m both with and without), and area 18 (a parked car) is worse with variable resolution than without (0.0287 m vs. 0.0277 m without).
- Conference-room environment (Table 7, p.17): of 18 regions, the text states 17 improved; area 16 (a table) is worse with variable resolution than without (0.0107 m vs. 0.0055 m without).
These exceptions are not discussed or explained by the authors beyond the aggregate improvement statement. INFERENCE: the random-selection component of Algorithm 1 (discarding (1-γ) of over-limit points at random rather than by density) could occasionally remove informative points in certain high-curvature or object regions, degrading local accuracy — this specific causal explanation is not stated in the paper and is offered only as a plausible interpretation (HYPOTHESIS).

## 26. Explicit limitations
The paper does not contain a dedicated "Limitations" subsection. The only self-acknowledged scope gap appears in the Conclusions: the method has been demonstrated in static/quasi-static room, corridor, outdoor, and conference-room scenes, and the authors state that large-scale dynamic environments are left to future study, implying the current method is not shown to handle dynamic environments. DIRECT EVIDENCE (p.18, Conclusions).

## 27. Future work
"In the future, we may study LiDAR mapping in large-scale dynamic environments." DIRECT EVIDENCE (p.18, Conclusions, final sentence of Section 5). No other future-work directions are given.

## 28. What the method does NOT solve
Based on the above items, the method does not perform: terrain/traversability analysis (item 11); semantic classification or labeling (item 10); object-level static or dynamic object detection/segmentation (items 12-13); object tracking (item 15); dynamic-object handling of any kind (item 13, explicitly deferred to future work); occupancy/semantic-level uncertainty estimation (only geometric/registration uncertainty is modeled, item 16); global SLAM with loop closure (item 17); and it reports no computational-cost, runtime/FPS, or hardware-requirement figures (items 19-20), so its real-time/embedded feasibility is not established from the paper. DERIVED from items 10-20 above.

## 29. Relevance to the fixed SIH problem
Relevance only — no architecture adoption implied.
- **Terrain analysis:** Not relevant as a solved sub-problem; the paper contains no terrain/drivability method. INFERENCE: the underlying curvature signal it computes per voxel (via covariance eigenvalues) is a generic local-geometry descriptor that in principle could distinguish flat ground-like regions from non-flat/vertical structure, but the paper itself never applies it to a terrain/traversability question — this is a structural observation, not a claim the paper solves terrain analysis.
- **Static/dynamic object detection:** Not relevant to dynamic-object detection (explicitly out of scope, deferred to future work, item 13/26-27). For static structure, the method demonstrates that an accurate, size-bounded 3D geometric map of static scenes (rooms, corridors, outdoor roads, furniture, parked vehicles, trees) can be built and maintained without unbounded memory growth — relevant background context for any downstream static-object perception module, but the paper performs no object-level detection itself.
- **Adaptive variable-resolution 2.5D spatial representation:** Directly and specifically relevant as a contrasting/comparison data point for the SIH's core architectural question, precisely because this paper's adaptivity is (a) CURVATURE-driven rather than distance-driven, and (b) applied to a full 3D voxel/point representation rather than a 2.5D elevation representation (items 4, 7, 9). It is one concrete example of "semantic/geometric-aware" (here, curvature-aware) resolution adaptation as an alternative to naive distance-based coarsening, and it demonstrates (within its own ablation, not against external baselines) that such adaptation can reduce map memory substantially (36-80% size reduction across four scenes, item 21) while mostly — but not universally — improving or preserving point-to-point accuracy (items 21, 25). Because it is full 3D rather than 2.5D, it does not directly address the SIH's height/elevation-compression aspect, and because it targets static-only scenes with no reported latency/compute figures, it does not by itself establish real-time feasibility for the SIH's dynamic-environment, adaptive-resolution requirement.

## Figures/Tables/Equations Directly Consulted
- Figure 1 (p.4) — pipeline block diagram: LiDAR scan → distance filter → distortion correction → scan-to-map NDT registration (using predicted pose + reference cloud selection) → distortion correction (fine-tune) → update global map with variable resolution strategy → global map.
- Figure 2 (p.8) — (a) mobile robot with 16-line rotating LiDAR and coordinate axes; (b) portable rotating laser scanner used for ground truth.
- Table 1 (p.8) — VLP-16 spin-LiDAR parameters: 16 lines, 270° FOV, 10 Hz scan freq, 0.2 Hz X-axis rotation, 0.006 m accuracy.
- Table 2 (p.8) — Hokuyo UST-30LX portable scanner parameters: 1 line, 270° FOV, 40 Hz, 180° Z-axis rotation, 0.003 m accuracy.
- Figure 3 (p.8) — photo of lab room scene used for room-environment mapping test.
- Figure 4 (p.9) — room mapping results: (a-1,a-2) ground truth, (b-1,b-2) without variable resolution, (c-1,c-2) with variable resolution; zoomed insets show visibly denser points on furniture/equipment vs. sparser points on flat ceiling/wall/floor in the variable-resolution result.
- Figure 5 (p.10) — 8 labeled evaluation regions (ceiling ×3, walls ×2, equipment ×1, desks ×2) overlaid on the room point cloud.
- Table 3 (p.10) — room MAE (m) per region, without vs. with variable resolution; all 8 regions improved with variable resolution (largest improvement area 2, 14.58%).
- Figure 6 (p.10) — photo of U-shaped corridor scene.
- Figure 7 (p.11) — corridor mapping results (ground truth / without VR / with VR), zoomed insets showing sparse ceiling/floor vs. dense railing points under variable resolution.
- Figure 8 (p.12) — 16 labeled evaluation regions (ceiling, floor, railings, walls) in the corridor.
- Table 4 (p.12) — corridor MAE (m) per region; all 16 regions improved with variable resolution (largest improvement area 14, 56.65%).
- Figure 9 (p.12) — photo of outdoor campus road scene with parked cars, trees, flower bed.
- Figure 10 (p.13) — outdoor mapping results; ground truth shows circular scan-vacancy gaps (scanner self-occlusion / sparse tripod positions); with-VR result shows sparse ground points, dense tree/car points.
- Figure 11 (p.14) — 30 labeled evaluation regions (ground, flower bed, cars, tall trees, short trees) in the outdoor scene.
- Table 5 (p.14) — outdoor MAE (m) per region; 28/30 regions improved, with two exceptions identified directly from the numeric values: area 16 unchanged (0.0327/0.0327) and area 18 regressed (0.0287 with VR vs. 0.0277 without).
- Table 6 (p.15) — map size (point count) comparison across room/corridor/outdoor: reduced to 61.02%/62.67%/79.86% of baseline respectively with variable resolution.
- Figure 12 (p.15) — photo of conference room scene (tables/chairs, non-planar tiered ceiling) used for long-time experiment.
- Figure 13 (p.16) — conference room mapping results (ground truth / without VR / with VR); with-VR result shows sparse floor/wall points but relatively dense ceiling points (non-planar ceiling has high curvature).
- Figure 14 (p.17) — 18 labeled evaluation regions (ceiling, floor, walls, chairs, tables) in the conference room.
- Table 7 (p.17) — conference-room MAE (m) per region; 17/18 regions improved; area 16 (table) regressed (0.0107 with VR vs. 0.0055 without).
- Figure 15 (p.17) — map size (point count) vs. time (s) line chart, two curves: without variable resolution grows roughly continuously to ~1.8×10⁷ points by 120 s; with variable resolution rises then plateaus near ~6×10⁶ points after ~90 s.
- Figure 16 (p.18) — with-VR conference-room map snapshots at 60 s, 90 s, and final time, showing scene coverage completing by ~90 s with only detail refinement afterward.
- Equations 1-19 (pp.4-7) and Algorithm 1 (p.7) — full scan-to-map NDT registration math (coordinate transforms, CTRV pose prediction, NDT likelihood/PDF, robust mixture objective, Newton-method optimization, pose update) and the curvature-based variable-resolution voxel density control (curvature from covariance eigenvalues, piecewise density-limit function, max-point-count formula, and the density-value-based + random point retention/removal procedure).

## Uninterpretable / Uncertain Sections
1. The zoomed circular inset close-ups in Figures 4, 7, 10, and 13 convey a clear qualitative density difference (visibly sparser vs. denser point clusters) but individual point counts/exact density values within each inset cannot be reliably read off the image alone; these qualitative observations were corroborated using the accompanying body text rather than independently verified from pixel-level inspection.
2. In Table 5 (outdoor MAE), the bold/non-bold typographic emphasis marking which value is smaller was visually ambiguous for a couple of rows at image resolution; this was resolved by directly comparing the printed numeric values rather than relying on the bold formatting, so the conclusions in Items 21/25 are based on the numbers themselves, cross-checked against the text's "28 of 30" claim.
Beyond these two minor caveats (both resolved via text/numeric cross-checking, not guessed), no page, figure, table, or equation was unreadable or omitted.

## Summary Assessment
This paper solves a narrow, well-defined problem — bounding point-cloud map memory growth during long-duration static-scene 3D LiDAR mapping — via scan-to-map NDT registration plus a curvature-driven (not distance-driven) per-voxel point-density cap applied to a full 3D Octree/point-cloud map, not a 2.5D elevation representation (DIRECT EVIDENCE, Eq. 17-19, Section 3.3). It reports substantial, directly-evidenced map-size reductions (36-80% of baseline point count across four static test scenes, Table 6, and a growth-then-plateau size/time curve in Figure 15) together with mostly-improved but not universally-improved point-to-point MAE against ground truth (a small number of individual regions were unchanged or slightly worse, Tables 5 and 7). It contains no semantic information, no terrain analysis, no dynamic-object handling or tracking (explicitly deferred to future work), no neural-network component, and reports no computational-cost or runtime/FPS figures, so its real-time/embedded feasibility is not established from the paper (DERIVED, Items 18-20, 26-27). Its principal relevance to the SIH problem is as a concrete existence-proof of curvature-based (geometry-aware, non-distance) map-resolution adaptation applied to a full 3D representation, offering a useful contrast point rather than a directly transferable terrain/dynamic-object/2.5D solution.
