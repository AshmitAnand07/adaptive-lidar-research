# Lightweight 2.5D SLAM with Dynamic Map Refinement and Height-Aware Encoding for Resource-Constrained Indoor Robots — Deep Analysis

**Source file:** `papers/sensors-26-04765.pdf`
**Analyzed:** Phase 1 (supplied-paper analysis), single-paper deep read.

## 1. Problem being solved

The paper addresses SLAM for **indoor mobile robots equipped with low-cost, sparse sensors** (a single-line LiDAR, sparse ToF, wheel odometry, IMU), which suffer from two specific problems: (a) **limited vertical perception** because the primary ranging sensor is planar/single-line, and (b) **dynamic residual artifacts** (pedestrian footprints, transient objects, short-term ToF reflections) that persist in the accumulated global map after mapping. The proposed system is explicitly framed as a **system-level integration/deployment contribution** — adapting existing mature SLAM modules (ESKF, NDT, pose-graph optimization) to a sparse-sensing low-cost platform, adding an offline artifact-cleanup stage, and adding a compact height-aware export format — rather than a new SLAM algorithm or a new dynamic-object theory. DIRECT EVIDENCE (Abstract, p.1; Introduction p.2-3; explicitly restated p.3: "the novelty of this work is therefore positioned at the system level... this work does not claim a new general-purpose SLAM optimizer or a new dynamic SLAM theory").

## 2. Sensors and input data

- STL-06p LDS: single-line, 360° planar laser distance sensor (main ranging sensor). DIRECT EVIDENCE (p.3, Fig 1b).
- Cleaner01F1 linear ToF module: described as providing "sparse vertical observations." DIRECT EVIDENCE (p.3).
- A9 IMU (300 Hz). DIRECT EVIDENCE (p.3, Fig 3).
- Wheel odometry (50 Hz), used for motion estimation/state correction. DIRECT EVIDENCE (p.3, Fig 3).
- Compute: Sunrise X3 embedded processor, quad-core ARM Cortex-A53 CPU, 4 GB memory, 5 TOPS. DIRECT EVIDENCE (p.3, Fig 1b).
- Public datasets M2DGR and KITTI are used, but explicitly only as **odometry-backbone reference experiments**; the paper states their sensor configurations, motion conditions, and scenarios differ from the proposed LDS–ToF–odometry–IMU platform and are not used as benchmarks for the 2.5D mapping/refinement/encoding contributions. DIRECT EVIDENCE (p.12).
- Effective raw acquisition rates during embedded tests: LDS ≈10 Hz, ToF ≈10 Hz, IMU 300 Hz, odometry 50 Hz. DIRECT EVIDENCE (p.17, Table 5 context text).

## 3. Input representation

Asynchronous multi-sensor streams are timestamp-aligned around the LDS scan reference time (Eq 1, interpolation Eq 2, Fig 3), producing a synchronized per-frame set. Frames are motion-distortion corrected using IMU-propagated pose estimates (Eq 3) to yield a corrected 3D point cloud per keyframe. This corrected keyframe point cloud, together with its optimized pose, is the core stored unit reused by NDT registration, global map fusion, dynamic-artifact removal, and height-aware encoding. DIRECT EVIDENCE (p.5-7, Section 2.3; Fig 2 front-end block: "Time synchronization → Coordinate transformation → 3D point cloud synthesis → Down sampling").

## 4. 2D / 2.5D / 3D representation

The paper explicitly and consistently defines "2.5D" as **"a 2D grid map with discretized vertical occupancy bins for each grid cell, rather than a full continuous 3D reconstruction"** (Abstract, p.1; restated Section 2.6, p.8). This definition is verified directly against Figure 6, which shows the pipeline "1) 3D point cloud → 2) 2D grid projection (Δxy planar resolution) → 3) Vertical bin discretization (24 height bins, Δz_bin height-bin interval)" — i.e., the intermediate representation is a fused 3D point cloud (from SLAM back-end), which is then **projected down to a 2D planar grid**, with each planar cell assigned a fixed-length 24-element binary vertical-occupancy vector. This confirms the abstract's definition is accurate: the exported map is 2.5D (2D grid + discretized per-cell vertical bins), not a full unrestricted 3D volumetric/point structure, and not a plain 2D occupancy grid (which the paper also produces separately, Fig 2 output, Fig 17a) since that discards all height information. DIRECT EVIDENCE (p.1, p.8-9, Fig 6, Eqs 11-15).

## 5. Spatial/map representation

The system's outputs (Fig 2, "Output" box) are: (1) optimized odometry/poses, (2) a fused global 3D point cloud, (3) a standard 2D occupancy grid, (4) a 2.5D height-bin map, and (5) a 24-bit RGB-encoded PNG image of the height-bin map; when offline refinement is enabled, a refined global point cloud and refined 24-bit map are also produced. DIRECT EVIDENCE (p.4, Fig 2). The 2.5D grid is formally defined as a set of cells G(i,j), 0≤i<Nx, 0≤j<Ny (Eq 11), each holding a 24-bit vector b0..b23 (Eq 12), with grid extents computed from the point cloud's bounding box and a single planar resolution parameter Δxy (Eq 13).

## 6. Resolution strategy

Both the horizontal and vertical resolutions are **single global constants applied uniformly across the entire map**:
- Horizontal: one planar resolution value Δxy used to compute Nx, Ny for the whole grid (Eq 13-14). DIRECT EVIDENCE.
- Vertical: the global z-range [z_min, z_max] of the whole fused point cloud is uniformly divided into 24 equal-width bins, with bin index k = clip(⌊24·(z−z_min)/(z_max−z_min)⌋, 0, 23) applied identically to every grid cell (Eq 15). DIRECT EVIDENCE.

No spatially varying cell size, no distance-dependent bin width, and no per-region resolution parameter is described anywhere in Sections 2.6–2.7 or in Appendix A's configuration table (Table A1), which lists only fixed thresholds (voxel size, ratios, cluster sizes) for the *dynamic-refinement* module, not for spatial resolution of the 2.5D grid itself. DIRECT EVIDENCE (absence confirmed by full read of Section 2.6 and Appendix A).

## 7. Whether resolution is adaptive and how

**Resolution is fixed/uniform in this paper, not spatially adaptive.** Both the planar grid resolution (Δxy) and the vertical bin scheme (24 uniform bins over the global height range) are single global parameters (Eqs 13, 15) with no mechanism described for varying cell size or bin count by distance from the robot, by region, by semantic class, or by uncertainty. DIRECT EVIDENCE.

The term "adaptive" appears in the paper **only in the Discussion/Limitations and Conclusions as future work**: "Future work will focus on adaptive height-bin encoding, larger dynamic indoor datasets, parameter adaptation, and tighter integration with downstream robot planning modules" (p.22, Discussion) and again in the Conclusions ("Future work will investigate adaptive height-bin encoding, larger dynamic indoor datasets, and integration with downstream robot planning," p.22). This is DIRECT EVIDENCE that adaptive/variable-resolution height-bin encoding is **explicitly not implemented** in the current system — it is an acknowledged gap, not a claimed capability.

Distinguishing adaptive sensing vs. adaptive computation (as required): there is no adaptive **sensing** either — the LDS is a fixed-rate, fixed-FOV 360° single-line planar scanner and the ToF module provides a sparse, fixed vertical sampling pattern; no controllable FOV, active scan pattern, or mechanical scanning adjustment is described. DIRECT EVIDENCE (Section 2.1, p.3; no contrary evidence found elsewhere).

## 8. Spatial data structure

- Final 2.5D map: a dense 2D array/grid G(i,j) with a fixed-length 24-bit vector per cell (Eq 11-12) — a simple flat grid, not a hierarchical, sparse, octree, or KD-tree structure. DIRECT EVIDENCE.
- NDT registration: point cloud divided into voxels, each voxel modeled as a Gaussian (mean/covariance), incrementally updated (Eqs 7-8) — a voxel grid used only internally for scan registration, not exported as the map product. DIRECT EVIDENCE (p.7-8, Section 2.5).
- Dynamic-artifact removal: a separate temporal-support voxel grid with voxel size 0.10 m (Appendix A, Table A1) is used to count how many keyframes observed each voxel (Eq 18) — again an internal/auxiliary structure distinct from the final 2.5D export grid. DIRECT EVIDENCE (p.11, Appendix A).
No octree (e.g., OctoMap-style) or other hierarchical spatial structure is used for the proposed system's own map; OctoMap and multi-layer grids are mentioned only in the Introduction as related work being contrasted against (p.2-3). DIRECT EVIDENCE.

## 9. Height/elevation representation

The representation is **not** a classical single-value elevation map (one height/z per cell). Instead, each cell stores a 24-bit **binary occupancy vector** across discretized vertical bins (Eq 12), where bit k = 1 only if at least one observed point falls in that height interval for that cell (p.9, "b_k(i,j)=1 indicates that the k-th height bin of grid cell (i,j) is occupied by at least one point"). The paper explicitly contrasts this with "downward-filled elevation maps," stating its own encoding "sets a height-bin bit to one only when the corresponding height interval is directly occupied by observed points. Therefore, suspended or discontinuous vertical structures can be preserved instead of being converted into solid columns" (p.10). This is verified visually in Figure 7, which shows a vertical column with only bins {2, 9, 18} marked occupied (non-contiguous), packed into BGR = (4,2,4), and decoded back losslessly. DIRECT EVIDENCE (p.9-11, Fig 7, Eqs 12, 16-17).

## 10. Semantic information

Not reported. No semantic segmentation, object classification, or semantic labeling module is described anywhere in the Methods, Results, or Discussion. The entire pipeline (SLAM backbone, 2.5D encoding, dynamic refinement) operates purely on geometric/occupancy criteria (temporal support, cluster size, spans, ratios) with no semantic class information at any stage. DIRECT EVIDENCE (absence, confirmed across full read of Sections 2–4).

## 11. Terrain analysis

Not reported. There is no drivability classification, slope/traversability estimation, or ground/non-ground segmentation module described. The 2.5D height-bin grid and 24-bit encoding are presented purely as a compact map-storage/export format, and their possible use is limited to "an auxiliary height-aware layer for obstacle checking or downstream navigation modules" as a forward-looking remark, not a demonstrated terrain-analysis capability (p.21: "tighter integration with planning layers is left for future work"). DIRECT EVIDENCE that terrain analysis is not performed; the obstacle-checking use is HYPOTHESIS/未demonstrated (explicitly deferred).

## 12. Static-object perception

There is no dedicated static-object detection/classification module. "Static" structure is handled implicitly through the dynamic-refinement module's preservation criteria: voxels/clusters with high temporal support across keyframes or "stable LDS-supported structures" are protected from removal (Section 2.7, p.11: "stable LDS-supported voxels are protected, and a cluster is removed only when temporal inconsistency and geometric artifact constraints are satisfied simultaneously"). Walls, room boundaries, and furniture-like structures appear preserved in the mapping outputs (Fig 13, Fig 15b, Fig 16d). DERIVED — static-object "perception" here is a byproduct of a persistence-based filter, not an explicit object-level static-detection system.

## 13. Dynamic-object perception

The system does **not** perform online/real-time dynamic-object detection, classification, or tracking of moving entities (e.g., no per-frame moving-object segmentation). Instead it implements an **offline, post-hoc map-refinement module** applied after global map fusion, explicitly described as "a conservative offline post-processing refinement for residual artifacts in the fused global map, rather than a general online dynamic-object SLAM method" (p.11, Section 2.7). It works by: computing temporal voxel support S(q) across all keyframes (Eq 18), extracting low-support candidate regions, Euclidean clustering of candidates, and filtering by geometric constraints (cluster size, horizontal/vertical span, low-support ratio, ToF-only ratio, stable-LDS-support ratio) plus an isolated-point removal step near the robot trajectory in "full mode" (p.11, Appendix A Table A1). DIRECT EVIDENCE. This targets **residual artifacts** (footprints, transient reflections) left behind by past dynamic objects in the accumulated map — not detection of currently-moving objects as distinct entities, and not object-type discrimination (pedestrian vs. vehicle vs. pole, etc., is never made).

## 14. Temporal processing

Temporal processing is limited to: (a) keyframe-based motion-triggered sampling (Section 2.3.2, Fig 4: time interval >0.3 s, translation >0.15 m, or rotation >10°), and (b) the offline temporal-voxel-support statistic S(q) = Σ_{k=1}^N 𝟙(q ∈ V_k), counting in how many of the N keyframes a voxel was observed (Eq 18, p.11). This is a **batch/offline** temporal statistic computed after all keyframes are collected, not an online recursive temporal filter (e.g., no Kalman/particle filter over object state, no online forgetting/decay model). DIRECT EVIDENCE.

## 15. Tracking

Not reported. No tracking of individual dynamic objects (no ID association, trajectory estimation, or velocity estimation of moving objects) is described. The only "tracking" in the system is robot self-pose estimation/tracking via the SLAM backbone (ESKF + NDT + pose graph), which is a localization function, not object tracking. DIRECT EVIDENCE (absence).

## 16. Uncertainty handling

Uncertainty/covariance modeling is present only at the **pose/registration level**, not in the final map representation:
- ESKF splits state into nominal state, true state, and error state (Eq 4), propagating and correcting error covariance from IMU/odometry/LiDAR registration (Section 2.4, p.7).
- NDT models per-voxel point distributions as Gaussians with incrementally updated mean μ and covariance Σ (Eqs 7-8).
- Pose-graph loop-closure optimization minimizes a Mahalanobis-type residual weighted by measurement covariance Σ_ij (Eq 6, Fig 5).
DIRECT EVIDENCE (p.7-8). By contrast, the final 2.5D height-bin map stores **binary** occupancy bits (0/1, Eq 12) with no probability, confidence, or variance per cell, and the dynamic-refinement decision is a deterministic threshold/rule-based classification (Table A1), not a probabilistic dynamic/static confidence score. DERIVED (from absence of any probabilistic map-cell field in Section 2.6-2.7).

## 17. Localization / SLAM dependency

The 2.5D mapping, dynamic refinement, and height-aware encoding are all **entirely dependent on a working, pose-consistent SLAM backbone**. The pipeline requires: multi-sensor synchronization → motion distortion correction → ESKF state estimation → incremental NDT scan-to-map registration → keyframe selection → pose-graph optimization with loop-closure detection → global point-cloud fusion using optimized poses (Fig 2; Sections 2.3-2.5). The paper states the backend "provides a pose-consistent map foundation for the proposed map refinement and compact height-aware map representation" (p.8). DIRECT EVIDENCE — this is a full SLAM-dependent system, not a SLAM-independent mapping/perception module.

## 18. Learning/neural-network components

None. Every component described — ESKF, incremental NDT, factor-graph/pose-graph optimization, Euclidean clustering, geometric threshold rules, bitwise encoding — is a classical, non-learned algorithm. No neural network, deep-learning model, or learned feature extractor appears anywhere in the Methods, Results, or Appendices. DIRECT EVIDENCE (absence, confirmed across full read).

## 19. Computational requirements

Hardware: Sunrise X3 embedded processor, quad-core ARM Cortex-A53 CPU, 4 GB memory, 5 TOPS compute capability (p.3). Under the full (Mode 3) configuration (Table 5, p.17): CPU usage 145.0–173.2 (short loop/room scenes) up to ~156% (long loop) — noted as able to exceed 100% because it is measured as process CPU time across multiple cores; peak memory 130.0–155.99 MB across the three test scenes (short loop, room, long loop). DIRECT EVIDENCE (Table 5).

## 20. Runtime/FPS/latency if reported

Two separate runtime measurements are reported and appear on different scales, which is noted here without reconciling:
- Figure 10 + accompanying text (p.14): front-end processing time rises across frames and plateaus around 0.6–0.9 s/frame (average ≈0.88 s); back-end processing time rises and plateaus around 2.10–2.24 s (average ≈2.21 s), described as "module-level processing cost on the embedded platform," with back-end timing measured only after a keyframe is accepted. DIRECT EVIDENCE (p.14, Fig 10).
- Table 5 (p.17): under the full Mode-3 configuration, "Backend Latency (ms)" is reported as 190.7–244.2 ms and "Backend Freq (Hz)" as 4.1–5.2 Hz, with sensor input rate ≈9.3–9.6 Hz. DIRECT EVIDENCE (Table 5).
Both are DIRECT EVIDENCE as stated in the paper, but the ~2.2 s backend average in Fig 10/text and the ~0.19–0.24 s backend latency in Table 5 do not obviously correspond to the same quantity; the paper does not explain the discrepancy, so it is reported here as-is rather than reconciled. Additional per-stage costs (Table 5): dynamic-refinement processing 733–1213 ms, PCD export 149–247 ms, 2D PNG export 19.6–48.7 ms, 24-bit PNG export 143.6–235.8 ms — all explicitly executed as offline/post-processing steps, not per-frame online costs (p.15, 17).

## 21. Memory/map-size results if reported

- Figure 11 (p.14): a relative memory-usage bar chart comparing "Cartographer," "RTAB-Map," and "Ours," each normalized so Cartographer/RTAB-Map = 100%; the proposed system shows 82%, 80%, 85%, 86%, and 83% across five labeled test conditions ("First" through "Fifth" — the mapping of these labels to specific scenes is not stated in the accompanying text). DIRECT EVIDENCE for the percentage values; the exact scene identity behind each bar is not established from the paper.
- Table 9 (p.21): storage comparison across three scenes — raw PCD size 298.1–494.8 KB; standard 2D occupancy PNG 0.98–3.84 KB; proposed 24-bit height-aware PNG 3.46–8.66 KB; 2D map grid sizes 293×205, 87×153, 312×356; 24 height bins in all cases. The paper explicitly notes the 24-bit PNG is "not theoretically more compact than a raw 24-bit bitmask with the same grid size" — its advantage is claimed to be standard image-format compatibility and much smaller size vs. raw point-cloud export, not being a minimal-size representation (p.21). DIRECT EVIDENCE.

## 22. Dataset and experimental setup

- Public datasets (odometry-backbone reference only, not matched to the proposed sensor suite): M2DGR (6 sequences: room_01/02, gate_01, circle_01, door_01/02) and KITTI (sequences 00, 06, 07, 08). DIRECT EVIDENCE (p.12-13, Tables 2-3).
- Self-collected data, Group 1 (static map-consistency evaluation): IEC/ASTM 62885-7 coverage test-bed scene, and a household environment scene with multiple room-like regions (Fig 12). DIRECT EVIDENCE (p.14-16).
- Self-collected data, Group 2 (dynamic-artifact evaluation): a long-loop sequence and a short-loop sequence collected in the same indoor loop scene (Fig 14), plus reuse of the (nearly static) IEC/ASTM test-bed scene for cross-scene conservativeness validation. DIRECT EVIDENCE (p.16, 19).
- All experiments run on the described embedded hardware (Sunrise X3) except where explicitly noted as public-dataset odometry references (which the paper does not tie to a specific compute platform in the text reviewed).

## 23. Evaluation metrics

- Absolute Trajectory Error (ATE): RMSE and MEAN, computed from Euclidean distance between estimated and reference positions after timestamp association, same script for all compared methods (p.12, Tables 2-3).
- Mapping-area accuracy: generated occupancy-map area vs. measured/actual scene area, reported as % inaccuracy (Table 4).
- Resource metrics: CPU usage (%), peak memory (MB), backend latency (ms)/frequency (Hz), per-stage export times (ms) (Table 5).
- Dynamic-refinement quantitative metrics: input/output point counts, point variation (%), candidate points, candidate clusters, removed clusters, removed isolated points (Tables 6, 8); ROI-based manually segmented residual-point counts and % reduction in two marked regions of interest (Table 7) — explicitly stated as not a substitute for full-scene precision/recall/F1 because dense point-level ground truth is unavailable (p.19).
- Storage size (KB) for PCD, 2D PNG, and 24-bit PNG exports, plus grid dimensions and bin count (Table 9).
- Relative memory-usage percentage vs. two baseline SLAM systems (Fig 11).
- One-at-a-time parameter-perturbation sensitivity: removed points, removed ratio (%), removed clusters, runtime (ms) for two parameters (Table A2, Appendix B).
DIRECT EVIDENCE.

## 24. Baselines and ablations

- Odometry baselines: FAST-LIO and LIO-SAM on M2DGR (Table 2); LOAM and LeGO-LOAM on KITTI (Table 3). DIRECT EVIDENCE.
- 2D-mapping-area baseline: Gmapping evaluated on the IEC/ASTM test-bed scene using LDS + wheel odometry only, reported as text (not a table): 19.81 m² mapped vs. 20.00 m² actual (0.95% error), vs. the proposed method's 19.93 m² (0.4% error) (p.16). DIRECT EVIDENCE.
- Memory baselines: Cartographer and RTAB-Map (Fig 11). DIRECT EVIDENCE.
- Ablation modes for dynamic-artifact removal (Table 1): Mode 0 = no cleanup (baseline); Mode 1 = geometry-only filtering; Mode 2 = temporal support + geometry; Mode 3 = full method (adds isolated-point removal). Evaluated quantitatively in Table 6 (long-loop scene) and Table 8 (cross-scene: long-loop, short-loop, IEC/ASTM test-bed), and visually in Figures 15-16. DIRECT EVIDENCE.
- Parameter-sensitivity ablation (Appendix B, Table A2): one-at-a-time variation of `temporal_support_min_frames` (1,2,3) and `artifact_cluster_tolerance` (0.08, 0.10, 0.12 m) on the long-loop sequence, explicitly framed as testing local robustness around the chosen configuration, not a full generalization study across scenes/speeds/keyframe densities/ToF FOV (p.23-24). DIRECT EVIDENCE.

## 25. Failure cases

The only explicitly labeled failure case in the paper is a **baseline comparison method's** divergence: LeGO-LOAM on KITTI sequence 00 is reported with an asterisk, RMSE 504.935 / MEAN 438.832, with the paper stating this "denotes a divergence case observed under the same initialization, coordinate transformation, timestamp alignment, and ATE evaluation script used for the other KITTI runs; therefore, this value is retained to explicitly report the failure case rather than being treated as a normal successful run" (p.12, Table 3). DIRECT EVIDENCE. No explicit failure case of the **proposed method itself** (a scene/condition where it clearly fails) is reported in the text reviewed; this is "Not reported" beyond the general limitations discussed in Section 4/Appendix.

## 26. Explicit limitations

Stated directly in the Discussion (p.22): (1) the framework is a system-level deployment, not a new general-purpose SLAM optimizer or dynamic-SLAM theory; (2) public datasets serve only as odometry references and are not matched to the proposed sparse sensor suite — platform-specific claims rest only on self-collected sequences; (3) dynamic-refinement evaluation relies on ROI-based residual counts and static-scene preservation analysis rather than dense full-scene point-level ground truth (no precision/recall/F1 possible); (4) the front-end runs online at the keyframe level, while refinement and map export are offline post-processing steps, and queue latency and power consumption were not separately logged/measured; (5) the 24-bit encoding preserves discretized height-bin occupancy but not continuous 3D point coordinates. DIRECT EVIDENCE (p.22).

## 27. Future work

Explicitly stated (p.21-22): adaptive height-bin encoding; larger dynamic indoor datasets; parameter adaptation; tighter integration of the height-aware representation with downstream robot planning modules. DIRECT EVIDENCE.

## 28. What the method does NOT solve

Based on explicit statements and confirmed absences across the full read: semantic segmentation/classification of objects or terrain; terrain traversability/drivability analysis; online/real-time detection of moving objects (only offline, post-hoc residual-artifact removal from an already-fused static map); tracking of individual dynamic objects; adaptive or spatially variable map resolution (both planar cell size and vertical bin scheme are fixed global constants; adaptive encoding is explicitly future work); probabilistic/uncertainty-aware map cells (final occupancy bits are deterministic binary values); full continuous 3D reconstruction (by design, replaced with discretized 2.5D bins); and dense, full-scene quantitative validation of the dynamic-refinement module (only ROI-based counts and a static-scene preservation ratio are reported). DERIVED from Sections 2, 3, 4, and Appendix A/B taken together.

## 29. Relevance to the fixed SIH problem

- **Terrain analysis (drivable vs. non-drivable):** Not addressed by this paper at all — no traversability, slope, or terrain-classification method is present. The height-bin occupancy substrate could in principle be an input to a future terrain-analysis stage, but this is not demonstrated here. HYPOTHESIS (explicitly unaddressed).
- **Static/dynamic object detection (walls, poles, pedestrians, vehicles):** The paper's only dynamic-object-related mechanism is an **offline, map-level temporal-persistence filter** (Eq 18) that separates high-persistence ("static") from low-persistence ("transient/artifact") voxels/clusters after full map fusion, using purely geometric/statistical rules, with no object classification (no distinction among pedestrian/vehicle/pole types) and no real-time/online detection or tracking capability. This is relevant as one concrete example of a persistence-based static/dynamic discrimination technique operating on an accumulated map, but it does not match the SIH requirement for (likely online) detection and discrimination of walls, poles, pedestrians, and vehicles as distinct object categories. DERIVED/INFERENCE.
- **Adaptive variable-resolution 2.5D spatial representation:** This paper is directly relevant as a working example of a **fixed-resolution** 2.5D representation — a 2D grid with a per-cell discretized vertical occupancy vector (24 uniform bins) — and of one compact encoding/export strategy (24-bit RGB bit-packing) with quantified storage trade-offs (Table 9) relative to raw point clouds and plain 2D occupancy grids. However, it provides **no evidence** on adaptive or variable spatial resolution, distance-based resolution scaling, or semantic/uncertainty-aware resolution adaptation — the paper's own authors identify "adaptive height-bin encoding" as unresolved future work (p.21-22). Consequently, this paper answers "what is a plausible 2.5D fixed-resolution baseline and its storage cost," but leaves the SIH's central adaptive-resolution question entirely open. DIRECT EVIDENCE for what is implemented; DERIVED for the relevance gap.

## Figures/Tables/Equations Directly Consulted

- Figure 1 (p.4): robot platform photo and hardware connection block diagram (Sunrise X3 ↔ LDS/ToF/IMU via TCP/USB/UART; STM32 ↔ motors/encoders via CAN).
- Figure 2 (p.4): overall system block diagram — Frontend (sync → transform → 3D point synthesis → downsample; ESKF ↔ incremental NDT ↔ fusion motion estimation) and Backend (keyframe determination → probability map / loop closure / updated keyframe maps → global map optimization+conversion → global point cloud fusion → offline dynamic artifact removal + 24-bit height-aware map export branches) with listed outputs.
- Figure 3 (p.5): timestamp-alignment timing diagrams for IMU(300Hz)/Odom(50Hz)/ToF(10Hz)/Lidar(10Hz) before (a) and after (b) alignment.
- Figure 4 (p.6): 3D coordinate-frame diagram illustrating pose transformation between keyframe k and frame k+1.
- Figure 5 (p.7): factor-graph diagram with variable nodes (poses x_i), factor nodes (odometry u_i, landmark m_i, loop-closure c_i), and landmark nodes l_i.
- Figure 6 (p.9): three-panel diagram — 3D point cloud → 2D grid projection (Δxy resolution) → vertical bin discretization into 24 height bins per column (orange=occupied, white=free).
- Figure 7 (p.10): 4-step diagram of 24-bit encoding for one example column (occupied bins {2,9,18}) into B/G/R channels and lossless decoding back to the same bins.
- Figure 8 (p.13): M2DGR trajectory comparison — 3D trajectory plot (a) and per-axis x/y/z vs. time plots (b) for room_02, comparing LIO-SAM, FAST-LIO, and "Ours" against ground truth.
- Figure 9 (p.13): KITTI trajectory comparison — 3D plots for sequence 00 (a) and sequence 08 (b), comparing LOAM, LeGO-LOAM, and "Ours."
- Figure 10 (p.14): two line plots — front-end processing time (~0.6-0.9s, rising then plateauing over ~50 frames) and back-end processing time (~2.10-2.24s, rising then plateauing).
- Figure 11 (p.14): grouped bar chart, relative memory usage (%) for Cartographer/RTAB-Map (both 100%) vs. "Ours" (82,80,85,86,83%) across five unlabeled test conditions ("First"-"Fifth").
- Figure 12 (p.15): photos of two standard indoor scenes — IEC/ASTM 62885-7 coverage test-bed (a) and household environment with marked regions a-d (b).
- Figure 13 (p.15): top-down point-cloud/occupancy map outputs with on-image distance annotations for the two standard scenes.
- Figure 14 (p.16): photo of the dynamic indoor loop scene (lobby-like area with furniture).
- Figure 15 (p.17): two grayscale 2D occupancy grids (long-loop scene) before (a) and after (b) dynamic-artifact removal, with red circles marking suppressed artifacts.
- Figure 16 (p.18): four 3D point-cloud renderings (baseline, geometry-only, temporal+geometry, full method) with red circles marking footprint-like residual artifacts progressively removed.
- Figure 17 (p.20): four-panel figure — standard 2D occupancy grid (a), 2.5D height-aware map render (b), encoded 24-bit map with a marked pillar cell (c), and a reverse-decoding panel showing stored BGR=(255,7,0) decoding to occupied bins 0-10 (d).
- Table 1 (p.12): four dynamic-cleanup ablation modes and their purposes.
- Tables 2-3 (p.13): ATE RMSE/MEAN vs. FAST-LIO/LIO-SAM (M2DGR) and LOAM/LeGO-LOAM (KITTI), including the asterisked LeGO-LOAM divergence value.
- Table 4 (p.16): mapping area vs. actual area, % inaccuracy, five scenes.
- Table 5 (p.17): per-scene runtime/resource statistics (sensor rate, backend latency/frequency, CPU%, peak memory, dynamic-refinement/PCD/PNG export times) under full Mode-3 configuration.
- Table 6 (p.18): long-loop ablation — input/output points, point variation %, candidate points/clusters, removed clusters/isolated points per method.
- Table 7 (p.18): ROI-based residual point counts and % reduction per method.
- Table 8 (p.19): cross-scene validation (long-loop, short-loop, IEC/ASTM test-bed) baseline vs. full method.
- Table 9 (p.21): storage comparison (PCD/2D PNG/24-bit PNG sizes, grid size, bin count) across three scenes.
- Table A1 (p.23): full configuration-parameter list for offline dynamic-artifact removal (14 parameters with values/descriptions).
- Table A2 (p.23): one-at-a-time perturbation results for `temporal_support_min_frames` and `artifact_cluster_tolerance`.
- Equations 1-18 (pp.5-11): timestamp matching/interpolation (1-2), motion-distortion correction (3), ESKF state composition (4), loop-closure factor and least-squares objective (5-6), incremental NDT mean/covariance update (7-8), pose composition (9), NDT registration objective (10), grid definition/cell vector (11-12), grid dimensions/indexing (13-14), height-bin index (15), channel/24-bit encoding (16-17), temporal voxel support (18).

## Uninterpretable / Uncertain Sections

1. Figure 11 (p.14): the x-axis category labels are "First," "Second," "Third," "Fourth," "Fifth" with no accompanying text mapping these to specific named scenes/sequences, so the exact scene identity behind each of the five memory-usage bars could not be reliably determined beyond the numeric percentages themselves.
2. The apparent scale mismatch between Figure 10's text-stated averages (front-end ≈0.88 s, back-end ≈2.21 s per the plot) and Table 5's "Backend Latency (ms)" column (190.7-244.2 ms) could not be reliably reconciled from the text provided — both values are reported in the paper, but it is not clear whether they measure the same processing stage under the same conditions; this is reported as an open inconsistency rather than resolved by inference.

Aside from these two points, all other figures, tables, and equations reviewed were legible and interpretable at the resolution provided.

## Summary Assessment

This paper is a systems-integration contribution: it wires classical SLAM components (ESKF, incremental NDT, pose-graph optimization) to a low-cost single-line-LiDAR + ToF + IMU + odometry indoor robot, adds an **offline, temporal-persistence-based map-cleanup module** for transient artifacts, and adds a **compact bit-packed export encoding** for a fixed-resolution 2.5D height-bin grid (DIRECT EVIDENCE, pp.1-11). The paper's own definition of "2.5D" — a 2D grid with per-cell discretized vertical occupancy bins, not continuous elevation and not full 3D — is confirmed by direct inspection of Figures 6-7 and Equations 11-17 (DIRECT EVIDENCE). Critically for the adaptive-resolution question: **resolution in this system is fixed and globally uniform**, both horizontally (single Δxy) and vertically (24 uniform bins over the whole point cloud's z-range); adaptive/variable resolution is explicitly named only as unimplemented future work (DIRECT EVIDENCE, p.21-22). The paper contains no semantic perception, no terrain/traversability analysis, no online dynamic-object detection or tracking, and no learned/neural components anywhere (DIRECT EVIDENCE/absence, confirmed by full read). Evaluation is a mix of odometry-reference experiments on mismatched public datasets and resource/mapping/refinement experiments on self-collected sequences, with dynamic-refinement quantification limited to ROI-based counts and a static-scene preservation ratio rather than dense full-scene ground truth (DIRECT EVIDENCE, p.19, p.22).
