# 2.5D Evidential Grids for Dynamic Object Detection — Deep Analysis

**Source file:** `papers/islandora_164656.pdf`
**Analyzed:** Phase 1 (supplied-paper analysis), single-paper deep read.

**Citation:** Laghmara, H., Josso-Laurain, T., Cudel, C., Lauffenburger, J.-P., "2.5D Evidential Grids for Dynamic Object Detection," 22nd International Conference on Information Fusion (FUSION), Ottawa, Canada, Jul 2019.

**Page-numbering note:** the PDF has 9 pages total: p.1 = HAL cover sheet, p.2 = ResearchGate cover sheet, p.3–p.9 = the actual paper (unnumbered in print). All page citations below use the PDF's own page numbers (as passed to the `pages` parameter), i.e. "PDF p.3" is the paper's page 1 ("Introduction" title page), through "PDF p.9" (end of references).

---

## 1. Problem being solved
Detection of multiple dynamic (moving) objects in a vehicle's local environment from LiDAR data, using an evidential (Dempster-Shafer) 2.5D occupancy-grid representation, with the environment map also encoding navigable/occupied space. DIRECT EVIDENCE — Abstract, PDF p.3: "This paper proposes a method for dynamic object detection using Evidential 2.5D Occupancy Grids... The description of the dynamic behavior of objects in a scene is related to the conflict issued after the temporal fusion." The stated context is Intelligent Transportation Systems (ITS) / autonomous vehicle perception, assuming the vehicle's pose is known (PDF p.3).

## 2. Sensors and input data
A single 3D multi-echo LiDAR: Velodyne HDL-64, 64 horizontal layers, 360° horizontal FOV, 26.9° vertical FOV (DIRECT EVIDENCE, PDF p.7, Sec. IV-A). Vehicle pose is obtained from GPS/IMU data provided with the dataset (DIRECT EVIDENCE, PDF p.7: "The GPS data is also used to obtain the vehicle's pose"). Camera images are present in the dataset but explicitly stated to be used only for visualization, not for detection (DIRECT EVIDENCE, PDF p.7: "The images are not exploited for this application but are used for visualization"). No radar or stereo vision is used in this paper's own experiments (only mentioned in related-work survey, PDF p.3).

## 3. Input representation
Raw 3D point cloud from the Velodyne, described per-point/per-beam as range r_i and angle θ_i (polar/spherical parameters), per Fig. 3 (DIRECT EVIDENCE, PDF p.5, Sec. III-B). From this, an intermediate polar "Scan Grid" (SG) is built (rows = angular sectors Θ, columns/cells = range intervals R), and a Cartesian "2.5D grid" is separately built by discretizing the covered ground-plane area into fixed-size cells and averaging point heights per cell (Eq. 1, DIRECT EVIDENCE, PDF p.4).

## 4. 2D / 2.5D / 3D representation
The paper explicitly and consistently uses a **2.5D** representation, not full 3D. DIRECT EVIDENCE: Fig. 2 (PDF p.4) shows a 3D LiDAR point cloud (top) reduced to a 2.5D grid (bottom) — a 2D array of cells each holding a single scalar "average height" value (bar height in the plot); Eq. 1 defines G(i,j) as a single scalar per cell (either 0 or the average height μ_i,j), confirming one height value per (i,j) cell, not a voxel column or full point set. The polar Scan Grid (Fig. 3) used for the occupancy/evidential update is itself 2D (range × angle) with no per-cell height field described in Eqs. 2–5. So the persistent map ("Map Grid," MG) is 2.5D: 2D grid indexed (i,j)/(p,q), each cell carrying (a) one elevation scalar and (b) a Dempster-Shafer occupancy-state mass vector. No voxel grid, octree, or unrestricted 3D volumetric structure appears anywhere in the figures or equations (DIRECT EVIDENCE, absence confirmed by inspection of all figures/equations).

## 5. Spatial/map representation
A single regular 2D Cartesian occupancy grid ("Map Grid," MG) over a fixed rectangular area around the ego-vehicle, each cell storing: an elevation value (Eq. 1) and a Dempster-Shafer belief-mass tuple over {Free (F), Occupied (O), unknown (Ω=F∪O), conflict (∅)} (Eqs. 2–10). The grid is recursively updated over time by transforming the previous Map Grid into the current vehicle frame and fusing it with a newly built Scan Grid from the current LiDAR frame (Fig. 4, DIRECT EVIDENCE, PDF p.5).

## 6. Resolution strategy
A single, fixed, uniform cell size is used everywhere in the mapped area: 0.4 m × 0.4 m (DIRECT EVIDENCE, Fig. 2 caption and body text, PDF p.4). The grid covers a fixed rectangular window: 40 m ahead, 20 m behind, and 20 m to each side of the vehicle (DIRECT EVIDENCE, PDF p.4). No other resolution value or region-dependent cell size is reported anywhere in the paper.

## 7. Whether resolution is adaptive and how
Not adaptive. DIRECT EVIDENCE (by exhaustive absence across the text, Fig. 1–7, Eqs. 1–12, Algorithm 1): the same 0.4×0.4 m cell size is used across the entire covered area regardless of distance from the ego-vehicle, object presence, semantics, or uncertainty. No mechanism for varying cell size, merging/splitting cells, or hierarchical refinement is described.
- **Adaptive sensing:** Not present. The Velodyne HDL-64 is used as a fixed mechanically-rotating multi-beam sensor with a constant 360°×26.9° field of view (PDF p.7); no controllable FOV, active scan pattern, or beam-steering is described.
- **Adaptive computational/map resolution:** Not present. The map/grid resolution is fixed and uniform, independent of how the sensor scanned.
- The paper's "evidential" (Dempster-Shafer) contribution addresses **occupancy-state uncertainty** at a fixed resolution — it is a distinct axis from resolution adaptivity, not a substitute for it (INFERENCE, consistent with the CLAUDE.md instruction to distinguish these).

## 8. Spatial data structure
A dense, uniform 2D array/matrix of cells, indexed (i,j) or (p,q), iterated exhaustively (e.g., Algorithm 1's `for each cell with index (p,q) do` loop over the whole transformed grid, PDF p.6). No hierarchical, sparse, tree-based (quad-tree/octree/k-d tree), or hashed structure is described or shown. DIRECT EVIDENCE (Algorithm 1; Fig. 2/Fig. 6 bar-chart axes labeled "Number of x-side cells" / "Number of y-side cells" up to roughly 100–140 cells per side, consistent with a dense rectangular array).

## 9. Height/elevation representation
Single scalar per cell: the average height (μ_i,j) of all 3D points projecting into that (i,j) cell, subject to a ground-plane filter (Eq. 1, DIRECT EVIDENCE, PDF p.4): if the height variance σ²_i,j is below a threshold tr_σ = 2 cm AND the mean height μ_i,j is below tr_μ = 30 cm, the cell is treated as ground/planar (G(i,j)=0); otherwise G(i,j)=μ_i,j (an elevated-object cell). These threshold values and the method itself are stated to be taken from reference [1] (Asvadi et al.), not derived in this paper. This is a classic single-layer elevation-map cell (2.5D); no multi-layer heights, height distributions, or per-cell height histograms are used beyond this variance-based ground test.

## 10. Semantic information
Not reported. No semantic object-category classification (e.g., car / pedestrian / pole / vegetation) is produced by the method. The only categorical outputs are: (a) per-cell occupancy state (Free / Occupied / Unknown / conflict, via Dempster-Shafer masses) and (b) post-hoc cluster-level Static vs. Dynamic labeling (Fig. 1, third box, PDF p.5). Evaluation is restricted to one implicit class (cars) but this is a dataset/parameter-tuning choice (DBSCAN tuned for cars, PDF p.8), not a semantic classification capability of the method itself.

## 11. Terrain analysis
Limited to a binary ground-vs-elevated height/variance filter (Eq. 1), used only to decide which cells should carry an elevation value for the object-detection pipeline, not to characterize terrain itself. DIRECT EVIDENCE, PDF p.4: "it is necessary to determine all measures that correspond to the ground... to make sure it belongs to the ground surface and not any other planar surface." This method (and its thresholds) is explicitly imported from reference [1], not proposed here. There is no slope/roughness estimation, no drivable/non-drivable classification output, and no discussion of uneven or tilted terrain beyond noting (citing [13]) that such cases "induce errors" (PDF p.4) — this is a stated motivation for the ground filter, not a solved problem. INFERENCE: this does not constitute the kind of terrain-analysis / traversability output required by the SIH problem (item 29 below elaborates).

## 12. Static-object perception
Static objects correspond to grid cells/clusters that are elevated (non-zero G(i,j)) and Occupied but do not exhibit conflict (m(∅)) during temporal fusion — i.e., cells whose occupancy state is stable over time. DIRECT EVIDENCE (Sec. III-C/D reasoning, PDF p.6, and Fig. 6 discussion, PDF p.7, which identifies "static ones like numerous traffic signs or static vehicles behind the ego-car" as elevated but non-conflictual voxels/cells in the example scene).

## 13. Dynamic-object perception
Dynamic ("mobile") cells are elevated, Occupied cells that additionally show conflict during the evidential temporal fusion (mass m(∅) > 0, decomposed into C1 = transition Free→Occupied and C2 = transition Occupied→Free, Eq. 10, DIRECT EVIDENCE PDF p.6). Only the C1-labeled cells (newly occupied) are used to localize the object; C2 cells (newly free, boundary trailing edge) are discarded as uninformative about object shape/presence (DIRECT EVIDENCE, PDF p.6–7, Fig. 5). Both classes of cells (static and dynamic candidates) are clustered by elevation using DBSCAN, then split into static/dynamic sub-groups according to which clusters partially contain conflictual cells (Fig. 1, DIRECT EVIDENCE PDF p.5,7). An oriented/axis bounding box is then built per dynamic cluster (Fig. 1, Fig. 6).

## 14. Temporal processing
A recursive, sequential frame-by-frame evidential grid fusion: the previous Map Grid MG_{t-1} is spatially transformed into the current vehicle coordinate frame using the vehicle pose (rotation R, translation T — Algorithm 1, DIRECT EVIDENCE PDF p.6), then combined with the current frame's Scan Grid SG_t via Dempster's rule of combination (Eqs. 6–9, DIRECT EVIDENCE PDF p.6) to produce MG_t. This is structurally analogous to a Bayesian recursive occupancy filter but using Dempster-Shafer belief-mass combination instead of Bayesian probability update (DERIVED, based on comparison drawn by the authors themselves to BOF-style approaches in the related-work section, PDF p.3–4).

## 15. Tracking
Not implemented in this paper. The abstract and introduction frame the object-level clustering output as intended to support tracking downstream ("achieve an object-level representation according to the detected dynamic cells for tracking purposes," PDF p.3), but no data-association, ID-persistence, Kalman/particle filter, or velocity estimation across frames is performed or evaluated in this work (DIRECT EVIDENCE by absence — no such component appears in Sections III or IV, and the Conclusion, PDF p.8, does not claim tracking results). Multi-Object Tracking (MOT) is discussed only as related/contextual background in the Introduction (PDF p.3).

## 16. Uncertainty handling
Formal Dempster-Shafer / Belief Theory framework: per-cell mass functions over the discernment frame Ω={F,O} and its power set {∅,F,O,{F,O}} (Eqs. 2–5, DIRECT EVIDENCE PDF p.5), combined recursively over time with Dempster's rule (Eqs. 6–9, PDF p.6), explicitly normalized for conflict (K in Eq. 7–8). Sensor imperfection is modeled via a false-alarm probability μ_F and missed-detection probability μ_O in the inverse sensor model (Eqs. 2–5). The paper explicitly motivates this choice by "the uncertainty and imprecision of information" in dynamic-scene modeling (PDF p.3). This uncertainty mechanism operates per fixed-size cell and is analytically independent of the (fixed) resolution — i.e., this paper demonstrates an uncertainty-handling axis (evidential occupancy state) that is orthogonal to spatial-resolution policy, since resolution itself is not varied anywhere in the paper (INFERENCE, directly relevant to the CLAUDE.md item on distinguishing these two axes).

## 17. Localization / SLAM dependency
The method assumes the vehicle pose is known and externally supplied — stated explicitly ("considering that the vehicle's pose is known," PDF p.3) and used directly as an input to the grid-transformation step (Algorithm 1, Fig. 4, "Vehicle Pose" input box, PDF p.5). In the experiments, pose comes from the KITTI dataset's GPS/IMU recordings (DIRECT EVIDENCE, PDF p.7). No SLAM or localization algorithm is proposed, implemented, or evaluated by this paper; localization accuracy/error is not discussed or characterized.

## 18. Learning/neural-network components
None. DIRECT EVIDENCE by exhaustive inspection: ground filtering is a hand-set threshold test (Eq. 1, thresholds imported from [1]); occupancy fusion is a closed-form Dempster-Shafer combination rule (Eqs. 6–9); object extraction uses DBSCAN (PDF p.6), a classical unsupervised density-based clustering algorithm with no training phase. The KITTI dataset is used only for evaluation (ground-truth comparison), not for training any model.

## 19. Computational requirements
Not reported. No CPU/GPU specification, hardware platform, memory-complexity, or algorithmic-complexity (big-O) analysis appears anywhere in the paper.

## 20. Runtime/FPS/latency if reported
Not reported. The paper explicitly states the approach "has been tested offline" (DIRECT EVIDENCE, PDF p.7, Sec. IV: "The presented approach is applied to real data and has been tested offline"). No FPS, frame-processing time, or latency figure is given, and no real-time claim is made.

## 21. Memory/map-size results if reported
Not reported as an explicit memory-footprint number (no bytes/MB figure anywhere). DERIVED (not stated verbatim): given the stated coverage (40 m front + 20 m back = 60 m, ×40 m width) and 0.4×0.4 m cells, the grid would contain on the order of 150×100 ≈ 15,000 cells; this is arithmetic inferred from stated parameters, not a number reported by the authors. Fig. 2 and Fig. 6's bar-chart axes show plotted ranges of roughly up to ~140 cells (x) and ~100–120 cells (y) for the visualized subset, consistent with but not a confirmation of this estimate.

## 22. Dataset and experimental setup
KITTI raw dataset, sequence 17, 114 total frames, of which 59 contain annotated moving cars (DIRECT EVIDENCE, PDF p.7, Sec. IV-A). Ground-truth (GT) object annotations and vehicle pose are available for this sequence and used for both qualitative and quantitative evaluation. Sensor: Velodyne HDL-64 (64 layers, 360°×26.9° FOV); camera images used for visualization only; GPS used for pose.

## 23. Evaluation metrics
Precision = TP/(TP+FP) (Eq. 11, DIRECT EVIDENCE PDF p.7, citing the PASCAL VOC precision definition, ref. [17]). A detected object is counted as a true positive if its bounding-box overlap (IoU-style) with the GT bounding box, a_o = area(B_p∩B_gt)/area(B_p∪B_gt) (Eq. 12), exceeds 50% (DIRECT EVIDENCE PDF p.7). Reported result: total Average Precision (AP) = 91.23% (DIRECT EVIDENCE, PDF p.8), with per-detection overlap ratios shown in Fig. 7 mostly varying between roughly 0.65–0.90 (stated in text, PDF p.8: "most detected objects overlap with true objects at a rate varying between 65%–90%").

## 24. Baselines and ablations
None. No comparison against alternative/prior methods and no ablation study (e.g., with/without evidential fusion, with/without the elevation filter, or across different grid resolutions) is performed. DIRECT EVIDENCE: the Conclusion explicitly lists this as future work — "a comparative study of this work with the state of the art results will be performed" (PDF p.8) — confirming no such comparison exists in this paper.

## 25. Failure cases
Not established from the paper as an explicit analyzed failure-case section. The closest related statement is a claimed strength, not a failure analysis: "the noisy or distant data do not belong to any object" (PDF p.8), attributed to DBSCAN's density requirement discarding sparse/noisy measurements — presented as a benefit, not documented as an observed failure mode with a concrete example. No missed-detection example, false-merge example, or occlusion-failure example is shown in any figure.

## 26. Explicit limitations
Stated directly by the authors (PDF p.8, Conclusion, and PDF p.8 Sec. IV-B): (a) only cars are detected/evaluated in this sequence, with DBSCAN parameters (minPts=4, ε=5 in grid coordinates) tuned specifically for that case ("Considering that we only detect cars in this sequence, the parameters of DBSCAN are minPts=4 and ε=5"); (b) the approach has not been tested on more complex scenarios including occluded objects, explicitly named as a future-work item, implying occlusion is currently unaddressed; (c) no comparison to state-of-the-art methods has yet been performed. DIRECT EVIDENCE.

## 27. Future work
Explicitly stated in the Conclusion (PDF p.8): (1) identify/generalize DBSCAN clustering parameters to detect multiple object classes beyond cars; (2) extend and test the approach on more complex scenarios including occluded objects; (3) perform a comparative study against state-of-the-art results. DIRECT EVIDENCE.

## 28. What the method does NOT solve
DERIVED synthesis from the above: no adaptive/variable spatial resolution (fixed 0.4×0.4 m cells only, everywhere); no semantic object-category classification (only generic occupancy + static/dynamic split, and only cars are evaluated); no object tracking, data association, or velocity estimation (explicitly deferred as downstream/future use); no localization or SLAM (vehicle pose assumed given); no learned/neural component; no real-time or runtime performance characterization (tested offline only, no FPS/latency reported); no explicit handling of occluded objects (named as untested); no baseline/SOTA comparison or ablation study; the grid itself, being 2.5D with one height scalar per cell, cannot represent multiple objects stacked at different heights within the same (i,j) footprint (INFERENCE, following directly from the single-scalar cell definition in Eq. 1).

## 29. Relevance to the fixed SIH problem
- **Terrain analysis (drivable vs. non-drivable):** Only indirectly relevant. The paper's ground/elevated height-variance filter (Eq. 1, imported from ref. [1]) performs a much narrower task — separating ground-plane returns from elevated-object returns for the purpose of building the elevation map — not a drivable/non-drivable terrain classification with slope, roughness, or terrain-type outputs. INFERENCE: this is a necessary but clearly insufficient building block relative to the SIH's terrain-analysis requirement.
- **Static/dynamic object detection:** Directly relevant at the methodological level. The paper's core contribution — conflict-based (Dempster-Shafer) identification of cells whose occupancy state changed over time, followed by DBSCAN clustering into object-level static/dynamic detections with bounding boxes — is a concrete example of a distance-agnostic, uncertainty-aware approach to the SIH's static/dynamic object-detection sub-problem. Its scope is narrow (single object class evaluated, no tracking, no occlusion handling), so it demonstrates one candidate technique family rather than a complete solution (DIRECT EVIDENCE for what was demonstrated; INFERENCE for its bearing on the broader SIH scope).
- **Adaptive variable-resolution 2.5D spatial representation:** Not directly relevant to the resolution-adaptivity question central to the SIH problem, since this paper's grid resolution is fixed and uniform throughout (no distance-based, semantic, or uncertainty-based resolution variation is present or tested). Its relevance is instead as (a) a concrete, evidence-based example of a fixed-resolution 2.5D (not full-3D) elevation-plus-occupancy representation, and (b) a demonstration that formal uncertainty modeling (Dempster-Shafer evidential masses) and spatial-resolution policy are two separate design axes — this paper addresses only the former. This directly informs (without answering) the SIH research question of whether uncertainty-aware adaptation differs from and could complement distance-based resolution adaptation (INFERENCE).

---

## Figures/Tables/Equations Directly Consulted

- **Fig. 1** (PDF p.5) — Block-diagram pipeline: Point Cloud → Pre-processing (grid-area filtering, 2.5D discretization with average height, low-variance/height cell filtering) → 2.5D Grid → Mobile cells labeling (evidential occupancy measure + conflict evaluation, using Vehicle Pose) → Mobile cells → Dynamic Object detection (clustering, static/dynamic classification, bounding box construction).
- **Fig. 2** (PDF p.4) — Top: 3D LiDAR point-cloud scatter plot from KITTI (car-centric polar/radial view). Bottom: corresponding 2.5D grid as a 3D bar chart, axes "Number of x-side cells" / "Number of y-side cells" vs. "Average height," 0.4×0.4 m cells, showing sparse clusters of elevated cells against a mostly-flat (near-zero) ground.
- **Fig. 3** (PDF p.5) — Polar occupancy-map diagram: fan-shaped sensor FOV from the ego-vehicle, color-coded Free (green) / Occupied (red) / Unknown (blue) regions, with R (range) and θ (angular sector) cell boundaries and yellow LiDAR-beam arrows terminating at red occupied cells.
- **Fig. 4** (PDF p.5) — Map Grid Construction block diagram: MG at t−1 → Grid Transformation (using Vehicle Pose) → transformed MG; Point Cloud → Scan Grid (SG) at t; both feed an "Evidential Fusion" block producing Map Grid (MG) at t.
- **Fig. 5** (PDF p.6) — Two vehicle-silhouette diagrams at t−1 (outline only) and t (filled, blue/red), illustrating conflict C1 (red, leading edge — newly occupied) and C2 (blue, trailing edge — newly free) arising from object displacement between frames.
- **Fig. 6** (PDF p.7) — Top: real camera photo of KITTI Sequence 17 frame 40 (urban road, two cars, traffic signs/lights). Middle: corresponding 2.5D grid bar chart (average height per cell). Bottom: polar-grid plot overlaying red "Detections" bounding boxes and green "Ground Truth" bounding boxes for the two visible cars.
- **Fig. 7** (PDF p.8) — Line plot of "Overlap" (y-axis, ~0.3–1.0) vs. "Detection Number" (x-axis, 0–~70), with a horizontal dashed red threshold line (~0.5) marking the minimum eligible overlap; the overlap trace fluctuates mostly between ~0.5 and 1.0.
- **Eq. 1** (PDF p.4) — Piecewise definition of the 2.5D grid cell value G(i,j): 0 if ground/planar (variance and mean-height below thresholds tr_σ=2cm, tr_μ=30cm), else the average height μ_i,j.
- **Eqs. 2–5** (PDF p.5) — Inverse sensor model mass functions m{Θ,R}(∅), m{Θ,R}(O), m{Θ,R}(F), m{Θ,R}(Ω) in terms of false-alarm probability μ_F and missed-detection probability μ_O.
- **Algorithm 1** (PDF p.6) — Grid Transformation to new vehicle coordinates: per-cell rotation/translation and index remapping of the previous Map Grid into the current vehicle frame.
- **Eqs. 6–9** (PDF p.6) — Dempster's rule of combination (general form and normalization constant K), and the resulting combined masses m_MGt(O), m_MGt(F), m_MGt(Ω), m_MGt(∅) for the updated Map Grid.
- **Eq. 10** (PDF p.6) — Decomposition of conflict mass m_MGt(∅) into C1 (Free→Occupied) and C2 (Occupied→Free) components.
- **Eqs. 11–12** (PDF p.7) — Precision metric (TP/(TP+FP)) and bounding-box overlap ratio a_o (intersection-over-union style) used to determine true positives.

## Uninterpretable / Uncertain Sections
None. All figures, tables, and equations in the 9-page PDF rendered legibly and were directly inspected as images; none were too small, cut off, or ambiguous to interpret.

## Summary Assessment
This paper demonstrates a fixed-resolution (0.4×0.4 m, uniform) 2.5D occupancy-grid pipeline that combines a hand-crafted ground/elevation filter (DIRECT EVIDENCE, Eq. 1) with a Dempster-Shafer evidential temporal fusion (DIRECT EVIDENCE, Eqs. 2–10) to flag cells whose occupancy state changes over time (conflict), and then uses DBSCAN clustering to lift these cell-level detections to object-level static/dynamic bounding boxes, evaluated only on cars in one KITTI sequence with 91.23% AP and no runtime/memory figures (DIRECT EVIDENCE, PDF pp.7–8). It contains no adaptive sensing and no adaptive/variable spatial resolution of any kind — the grid resolution is uniform and static throughout (DIRECT EVIDENCE by exhaustive absence). Its principal relevance to the SIH problem is as a worked example of (a) a genuinely 2.5D (single-height-per-cell) representation distinct from full 3D, and (b) a formal, resolution-independent uncertainty-handling mechanism (evidential occupancy masses), which the paper itself never combines with any resolution-adaptivity mechanism (INFERENCE). It leaves tracking, semantic classification, occlusion handling, multi-class detection, terrain traversability analysis, and any efficiency/scalability characterization unaddressed, several of which are explicitly named by the authors themselves as future work (DIRECT EVIDENCE, PDF p.8).
