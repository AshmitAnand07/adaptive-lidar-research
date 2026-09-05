# Real-Time Metric-Semantic Mapping for Autonomous Navigation in Outdoor Environments — Deep Analysis

**Source file:** `papers/2412.00291v1.pdf`
**Analyzed:** Phase 1 (supplied-paper analysis), single-paper deep read.

Full 12 pages read and visually inspected (rendered pages, all figures/tables/equations), not text-extraction only.

---

## 1. Problem being solved

The paper addresses **online metric-semantic mapping for autonomous ground-robot navigation in large-scale, unstructured outdoor environments**, and its downstream use for traversability assessment and point-to-point navigation. Stated desiderata: accuracy, efficiency (real-time), and versatility (support localization, planning, environment understanding). DIRECT EVIDENCE (p.1 abstract, p.2 §I-B "Challenges"). The authors frame existing real-time metric-semantic mapping systems (e.g., Kimera) as confined to indoor settings, and position their contribution as extending this to outdoor, GPU-accelerated, large-scale settings integrated with a real navigation stack. DIRECT EVIDENCE (p.1 abstract; p.3 §II-B, "closest work... Kimera... mainly focusing on indoor settings").

## 2. Sensors and input data

- **LiDAR-Visual-Inertial (LVI)** sensor suite. DIRECT EVIDENCE (p.3 §III-A).
- Mapping/data-collection rig (Fig. 4a, p.6): Ouster OS1 LiDAR (128×1024 resolution), two FLIR BFS-U3-31S4C global-shutter color cameras, one STIM300 IMU; sensors synchronized via an FPGA using a GPS PPS trigger. DIRECT EVIDENCE (p.6 §V-A; p.4 §IV-C synchronization/calibration text).
- Real-world test vehicle (Fig. 4b, p.6): four 16-beam LiDARs plus one Livox Mid-70 LiDAR. DIRECT EVIDENCE (p.6, Fig. 4 caption).
- Cameras supply RGB images for semantic segmentation; IMU supplies high-rate linear acceleration/angular velocity for motion propagation in the state estimator; LiDAR supplies 3D point clouds for geometry. DIRECT EVIDENCE (p.3 §III-A).

## 3. Input representation

Raw LiDAR point clouds are re-projected per frame, using the known LiDAR angular resolution (Δφ, Δθ) and start angle θ₀, into a structured **depth image D** and **height image H** (Eq. 3, p.5): D(u,v)=Fr, H(u,v)=F(z+O). This range-image representation is described as "very lightweight (100KB vs. 10MB)" relative to storing the raw point cloud. DIRECT EVIDENCE (p.5 §IV-C-1). Camera RGB images are fed to a 2D CNN producing per-pixel class labels and a per-pixel class-probability map. DIRECT EVIDENCE (p.4 §IV-B). IMU raw measurements feed the ESIKF pose estimator. These per-frame representations (D, H, RGB, IMU) are intermediate inputs to the pipeline, distinct from the persistent map representation (see §4-5 below).

## 4. 2D / 2.5D / 3D representation

The persistent, global map is a **full 3D volumetric TSDF representation**, extracted into a **3D triangle mesh** via marching cubes. DIRECT EVIDENCE (p.5 §IV-C-2; p.3 Table I, "Map Representation" column = "TSDF" for "Ours"). The per-frame depth/height image (Eq. 3) is a 2D range-image encoding used only to compute local surface normals feeding the non-projective distance calculation (Fig. 3, p.5) — it is not itself the stored map. A **2D occupancy grid** is a separate, derived, planning-time product: mesh vertices of the filtered traversable mesh are projected onto a 2D grid, and a cell is "drivable" if its occupancy probability is zero. DIRECT EVIDENCE (p.6 §IV-E). The related-work section explicitly distinguishes the "2.5D elevation map... stores height as a Gaussian variable per grid but falls short in multi-layered scenarios and constraining 6-DoF motions" (describing prior work, ref. [23]) from volumetric approaches "facilitating parallel GPU implementation," and states "our approach leverages the TSDF... utilizing GPU parallelization." DIRECT EVIDENCE (p.2 §II-A). **Conclusion: this paper's core map is full 3D (voxel/mesh), not 2.5D** — the 2.5D-vs-3D question is justified here by inspecting the map data structures/equations directly (voxel hash + marching-cubes mesh with unrestricted vertex Z, Eq. 4-6, Table I), not merely by the authors' prose label ("mesh map"). The only place a 2D/height-collapsed structure appears is the derived planning occupancy grid, which discards height rather than representing it in a bounded/compressed form.

**Adaptive sensing vs. adaptive computational/map resolution:** Neither is present. The LiDARs used (OS1, 16-beam units, Livox Mid-70) are used with their standard fixed scan patterns; no controllable FOV, adaptive scan density, or active sensing behavior is described. DERIVED (no such mechanism mentioned anywhere in §III-A, §IV-A, or §V-A). The map's voxel resolution is a single fixed global value per mapping run (see §6-7).

## 5. Spatial/map representation

TSDF-based volumetric map: each voxel Vᵢ stores a truncated signed distance Dᵢ, a weight Wᵢ, and a normalized gradient vector 𝐠ᵢ (p.5 §IV-C-2). Semantic voxels additionally store a discrete probability distribution over the label set 𝓛 (Eq. 6). The map is periodically converted to a metric-semantic **polygon mesh** (vertices, edges, faces, per-vertex label) via marching cubes; face normals support terrain analysis (p.6 §IV-D-1). For navigation, vertices are further extracted into a global point cloud (for localization) and a 2D occupancy grid (for planning). DIRECT EVIDENCE (p.6 §IV-E).

## 6. Resolution strategy

A **single, fixed, uniform voxel size ν per mapping run**, manually set per dataset from Table II (p.6): ν = 0.3 m for SemanticKITTI sequences 00, 02, 08 ("since the scope is very large and GPU memory is limited to store all voxels"), and ν = 0.25 m for all other sequences. Truncation distance τ = 5ν. DIRECT EVIDENCE (p.6, Table II and footnote). This is a global, offline, per-sequence parameter choice driven by scene scale and GPU memory budget — not a within-map spatially-varying resolution.

## 7. Whether resolution is adaptive and how

**Not adaptive**, in either sense distinguished by this task:
- ADAPTIVE SENSING: no — sensors operate with fixed, standard scan patterns (see §4). DERIVED.
- ADAPTIVE COMPUTATIONAL/MAP RESOLUTION: no — voxel size is uniform across the entire map for a given run; the only variation observed is a manually pre-selected global parameter that differs *between* dataset sequences (0.25 m vs. 0.3 m) due to scale/GPU-memory constraints, decided before mapping begins, not automatically adjusted at runtime based on distance from sensor, semantics, or uncertainty. DIRECT EVIDENCE (Table II, p.6) / DERIVED (no runtime adaptation logic described anywhere in §IV).

## 8. Spatial data structure

Two-level voxel-hashing hierarchy, following NvBlox/Voxblox-style design: a global hash table maps 3D grid indices to **VoxelBlocks**, each block densely holding 8×8×8 voxels contiguously in GPU memory; the hash table is queried from GPU kernels via the `stdgpu` library. DIRECT EVIDENCE (p.5 §IV-C-2, citing refs [35],[36]).

## 9. Height/elevation representation

No persistent single-valued elevation-per-cell field is maintained as the core map (i.e., not a classic 2.5D elevation grid). Height appears in two other forms: (a) a transient per-frame **height image** H(u,v) = F(z+O) (Eq. 3) used only to help compute local surface normals for the non-projective TSDF distance calculation; and (b) full 3D vertex z-coordinates in the extracted mesh, from which a **height-difference terrain feature** v_hd = max‖vᵢ−vⱼ‖ over vertex pairs in a local ball of radius r is computed for traversability filtering (p.6 §IV-D-1). DIRECT EVIDENCE for both. There is no bounded/compressed height channel comparable to a Gaussian-per-grid-cell elevation map (contrast with the elevation-map category the authors themselves describe on p.2 as a different, prior approach).

## 10. Semantic information

Dense semantic labeling at voxel/mesh-vertex granularity. A 2D CNN (off-the-shelf backbone [31], described as HRNet-style "deep high-resolution representation learning," plus a customized segmentation head and a confidence head) predicts per-pixel class label and probability distribution, plus pixel-wise aleatoric uncertainty; full architecture detail is deferred to a separate reference [33], not reproduced in this paper. DIRECT EVIDENCE (p.4 §IV-B). Labels are back-projected onto visible voxels within the camera frustum by raycasting; each voxel keeps a full discrete probability distribution over label set 𝓛 (initialized uniform), fused over time via a recursive Bayesian update (Eq. 6, p.5). Final per-vertex label = the class with highest fused probability, assigned during marching-cubes extraction. The custom outdoor campus dataset's class legend (Fig. 5, p.7) includes at least: Building, Curb, Sky, Vegetation, Sidewalk, Road, Traffic Sign, Bike Path, Road Marking, Wall, River, Fence, Road Block, Lane (14 classes shown). DIRECT EVIDENCE.

## 11. Terrain analysis

Section IV-D combines geometric and semantic mesh properties. Geometric: **height difference** v_hd, **steepness** v_s, **roughness** v_r, each computed over a local ball of radius r=0.25 m (Table II); a vertex is filtered out if all three exceed thresholds t_hd=0.6 m, t_v=20°, t_r=30° (note: paper's own subscripts for the thresholds — hd/v/r — do not exactly mirror the value names hd/s/r; likely a minor notational inconsistency in the source, reported faithfully here). DIRECT EVIDENCE (p.6 §IV-D-1, Table II). Semantic: vertices outside camera FOV (unlabeled) are removed; remaining vertices are classified traversable/non-traversable per a robot-specific rule (e.g., "road" drivable for a vehicle, "sidewalk"/"grass" not). DIRECT EVIDENCE (p.6 §IV-D-2). The filtered traversable mesh is projected to a 2D occupancy grid for planning (p.6 §IV-E).

## 12. Static-object perception

Handled purely as **dense semantic classification**, not discrete object detection: buildings, trees, poles/traffic signs, walls, fences, curbs, etc. receive per-voxel/per-vertex class labels (Fig. 1, Fig. 5). There is no bounding-box detection, no instance segmentation, and no object-count/instance output described anywhere in the pipeline (Fig. 2 block diagram, p.4, shows only Semantic Segmentation → Semantic Mapping, no detection/instance module). DERIVED.

## 13. Dynamic-object perception

**Not addressed as a system capability.** The related-work motivation (p.2 §I-A) notes generically that explicit map representations "have difficulty maintaining... long-term consistency... since environments always are changing (e.g., dynamic objects)," but no dedicated dynamic-object detection, segmentation, filtering, or removal module is presented in the proposed system's four components (state estimator, semantic segmentation, metric-semantic mapping, traversability extraction; p.2 §I-C, Fig. 2). The 3-second point-age exclusion in §IV-A applies only to the *local sparse color point cloud used for VIO pose alignment/rendering*, explicitly to reduce memory footprint — it is not described as a mechanism for removing dynamic objects from the persistent global semantic mesh. DIRECT EVIDENCE (p.4 §IV-A) / INFERENCE (that this is not a dynamic-object-handling mechanism, since it is framed purely as a memory-footprint optimization for the odometry-local map). The conclusion (p.9) lists "maintaining semantic features' spatio-temporal consistency" as an unresolved difficulty, consistent with no dynamic-object handling being solved.

## 14. Temporal processing

Temporal **fusion**, not temporal **modeling of motion**: (a) TSDF distance/weight are updated incrementally across frames via a weighted running update (Eq. 5, p.5); (b) per-voxel semantic class probabilities are updated across frames via a recursive Bayesian filter (Eq. 6, p.5) that combines label hypotheses from multiple images/poses over time. DIRECT EVIDENCE. No temporal model of scene dynamics (e.g., motion prediction, optical-flow-based consistency, or change detection) is described.

## 15. Tracking

Not reported. No object tracking, ID assignment, or trajectory estimation of external objects appears anywhere in the pipeline.

## 16. Uncertainty handling

Present in three places, all confined to mapping/training, none used for adaptive resolution: (a) TSDF voxel weight Wᵢ acts as a confidence/observation-count-like measure in geometric fusion (Eq. 5). DIRECT EVIDENCE. (b) The segmentation network's confidence head predicts pixel-wise **aleatoric uncertainty**, stated to "guide the network to pay more attention to areas where predictions are uncertain" during training; full detail is deferred to a separate paper [33]. DIRECT EVIDENCE (p.4 §IV-B) but incompletely specified in this paper. (c) Each voxel retains a full discrete class-probability distribution (not just an argmax label), continuously refined by the Bayesian update — an implicit representation of classification uncertainty. DIRECT EVIDENCE (Eq. 6). No quantitative evaluation of uncertainty calibration or its downstream effect is reported in this paper's own experiments (Table III reports RE/CD/RC/mIoU/Acc/Time only).

## 17. Localization / SLAM dependency

Essential dependency, in two distinct roles. (1) **Mapping-time**: an LiDAR-Visual-Inertial odometry state estimator adapted from R3LIVE, combining LIO and VIO via an error-state iterated Kalman filter (ESIKF, Eq. 1-2), supplies the poses used to fuse every LiDAR scan/image into the map. DIRECT EVIDENCE (p.4 §IV-A). (2) **Navigation-time**: a separate prior-map-based localization method (PALoc, ref. [42]) registers live scans against the point cloud extracted from the built mesh to obtain the real-time global pose used for planning. DIRECT EVIDENCE (p.6 §IV-E). No loop closure is implemented in either stage — explicitly flagged as a limitation (p.9 §VI).

## 18. Learning/neural-network components

(1) A 2D semantic segmentation CNN: off-the-shelf backbone [31] (HRNet-style high-resolution representation learning) + customized segmentation head + confidence head, trained with "prototype learning," pretrained on Cityscapes and the authors' own campus dataset (54.53% mIoU on their own validation split); full network detail deferred to ref. [33]. DIRECT EVIDENCE (p.4 §IV-B; p.6 §V-B). (2) For public LiDAR-only benchmark datasets (SemanticKITTI, SemanticUSL), a pretrained **Cylinder3D** LiDAR-only semantic segmentation network [46] is used to generate semantic measurements for those experiments. DIRECT EVIDENCE (p.7 §V-A/B text). No learned component performs geometry reconstruction, pose estimation (beyond the classical ESIKF), or dynamic-object handling.

## 19. Computational requirements

Mapping pipeline implemented in C++/CUDA; semantic segmentation in Python/PyTorch. Tested on: (a) desktop PC — Intel i9-12900KF, 64 GB RAM, Nvidia RTX 3080Ti; (b) embedded Nvidia Jetson Orin, 32 GB. DIRECT EVIDENCE (p.6 §V-A). Real-time performance depends on GPU-parallel voxel hashing/retrieval (stdgpu-based hash map) for all pipeline stages (measurement preprocessing, metric mapping, semantic mapping) executed in parallel on the GPU. DIRECT EVIDENCE (p.4-5 §IV-C intro).

## 20. Runtime/FPS/latency if reported

Headline claim: "frame processing taking less than 7ms, regardless of scenario scale." DIRECT EVIDENCE (p.1 abstract). Table IV (p.8, SemanticKITTI seq. 00, ~0.24 km²) breaks this down per module, with speedup ratios vs. VoxBlox/VoxField: on the 3080Ti — Normal-image estimation 0.2±0.1 ms (≈31.4× vs. VoxField), Metric mapping 1.0±0.2 ms (≈124.4× vs. VoxBlox), Semantic mapping 1.0±0.2 ms, Mesh generation 32.3±7.7 ms (≈3.1× vs. VoxBlox); on the Jetson ORIN — Normal image 0.7±0.3 ms, Metric map 9.3±0.7 ms, Semantic map 8.0±0.9 ms, Mesh generation 232.3±83.0 ms (a ratio of ≈0.4×, i.e., *slower* than the VoxBlox comparison figure in that specific column on this embedded platform). DIRECT EVIDENCE (Table IV, p.8). Table III (p.8) reports overall per-sequence processing time across all 21 public-dataset sequences for VoxBlox, VoxField, "Ours-Proj," and "Ours," showing baseline methods in the tens-to-low-hundreds of ms per frame versus the proposed method mostly in the single-digit-to-tens of ms range — DIRECT EVIDENCE for the general order-of-magnitude trend, though see the Uninterpretable section below regarding exact digit-level confidence for every table cell.

## 21. Memory/map-size results if reported

No total map memory footprint (e.g., MB per km²) is reported as an explicit metric in the pages read. Only two related data points appear: (a) the per-frame depth+height image representation is "very lightweight (100KB vs. 10MB)" compared to a raw point cloud (p.5 §IV-C-1); (b) GPU memory availability directly constrains the chosen voxel size for large-scope sequences (0.3 m instead of 0.25 m for SemanticKITTI 00/02/08, "since the scope is very large and GPU memory is limited to store all voxels," Table II footnote, p.6), and "GPU memory reliance... challenges city-scale mapping scalability" is explicitly listed as a limitation (p.9 §VI). Not reported: absolute map size in MB/GB for any sequence.

## 22. Dataset and experimental setup

Public benchmarks: **SemanticKITTI** (sequences 00–10, with 00/02/08 using ν=0.3 m due to scale/GPU memory), **SemanticUSL** (sequences 03, 12, 21, 32), **FusionPortable** (Garden_Night, Canteen_Night, Garden_Day, Canteen_Day, Escalator_Day, Building_Day, Campus_Road_Day — 7 sequences; RE/CD/RC only computed here since this dataset lacks semantic ground truth). DIRECT EVIDENCE (p.6-7 §V-A/B, Fig. 6 caption). Self-collected: 2 campus mapping/navigation sequences (seq00, seq01) used for real-vehicle navigation experiments (Fig. 7, Fig. 9), and a separate 15-sequence, 1092-image (2048×1536) segmentation-training dataset (95/5 train/val split), pretrained jointly with Cityscapes, achieving 54.53% mIoU on the authors' own validation split. DIRECT EVIDENCE (p.6 §V-B). Summing sequences (11 KITTI + 4 USL + 7 FusionPortable + 2 self-collected = 24) matches the abstract's stated "24 sequences." DERIVED. Map areas visualized directly range up to 0.67 km² (SemanticKITTI 05) and 0.225 km² (FusionPortable Campus_Road_Day) per Fig. 6 captions (p.7) — DIRECT EVIDENCE of large-scale outdoor operation.

## 23. Evaluation metrics

Reconstruction Error (RE, RMSE-style average point-to-point distance, Eq. 7, p.7), Chamfer Distance (CD, Eq. 8, p.7), Reconstruction Coverage (RC, % of GT points with a nearby reconstructed point), mean Intersection-over-Union (mIoU) and Accuracy of correctly labeled points (Acc) for semantic quality, and per-module Computation Time (ms). DIRECT EVIDENCE (p.7 §V-C-1).

## 24. Baselines and ablations

External baselines: **VoxBlox** and **VoxField** (both CPU-based TSDF mapping methods without semantic mapping or traversability extraction). DIRECT EVIDENCE (p.7 §V-C-2). Internal ablations: **Ours-Proj** (replaces the non-projective distance calculation with the original projective one) and **Ours-wo-Bay** (omits the recursive Bayesian update in semantic mapping), both compared against the full "Ours" in Table III (p.8) — used respectively to attribute RE/CD/time improvements to the non-projective distance method and mIoU/Acc improvements to the Bayesian semantic update. DIRECT EVIDENCE.

## 25. Failure cases

(a) Reconstruction Coverage (RC) is explicitly reported as *lower* for the proposed method than VoxBlox on SemanticKITTI/SemanticUSL, because the non-projective distance method discards LiDAR points lacking a reliable normal or at large incidence angles (especially ground points), leaving some voxels empty/without valid distance values. DIRECT EVIDENCE (p.8 §V-C-3 text). (b) Navigation paths planned on an occupancy grid built *without* semantic information were observed to cross through grassland areas, which — due to uneven terrain — pose a real risk of the vehicle becoming stuck; this is shown by directly contrasting Fig. 8(d)/(i) (with semantics) against Fig. 8(e)/(j) (without semantics, grassland circled and labeled "Grass"). DIRECT EVIDENCE (p.9 §V-D-2 text and Fig. 8 caption, p.10).

## 26. Explicit limitations

Stated in the Conclusion (p.9 §VI): (1) "GPU memory reliance, which challenges city-scale mapping scalability" (potential remedy noted: a submap approach, citing AutoMerge [47]); (2) "the absence of loop correction introduces drift over time" (potential remedy noted: submap techniques and mesh deformation optimizations, citing Kimera [48]); (3) "maintaining semantic features' spatio-temporal consistency poses difficulties" (potential remedy hinted: kernel-based methods, citing ref. [24]). DIRECT EVIDENCE.

## 27. Future work

"Future work will focus on integrating kernel-based methods to improve the map's semantic accuracy" (p.1, Note to Practitioners). The conclusion additionally points toward submap-based memory/loop-closure handling and mesh-deformation-based map correction as future directions (p.9). DIRECT EVIDENCE.

## 28. What the method does NOT solve

No loop closure or global drift correction (explicitly acknowledged). No unbounded/city-scale map scalability — bounded by GPU memory and a single fixed global voxel resolution rather than any hierarchical/adaptive scheme. No dynamic-object detection, segmentation, tracking, or removal from the persistent semantic map. No object-instance-level detection (only per-voxel/vertex semantic class, not discrete tracked object instances). No spatially- or semantically-adaptive/variable map resolution (voxel size is uniform and manually fixed per run). Not a 2.5D representation — the persistent map is full 3D; a 2D occupancy grid appears only as a derived, height-discarding planning product. No quantified uncertainty-aware adaptation of the map (uncertainty signals exist but are not shown driving any resolution or fusion policy change). Semantic spatio-temporal consistency under changing conditions is explicitly flagged as unresolved. DERIVED / DIRECT EVIDENCE as cited above.

## 29. Relevance to the fixed SIH problem

*Relevance only — no architecture is proposed or endorsed here.*

- **Terrain analysis (drivable vs. non-drivable):** Highly relevant as a worked example. Section IV-D demonstrates a concrete, evaluated pipeline combining mesh-geometric features (height difference, steepness, roughness) with semantic class filtering to produce a traversability-filtered map and, from it, a 2D planning occupancy grid — with a directly observed failure mode (grassland traversal) when semantic information is omitted (Fig. 8, p.10). DIRECT EVIDENCE/DERIVED.
- **Static/dynamic object detection:** Only the static/semantic half is addressed — dense outdoor semantic classification (buildings, vegetation, road furniture, etc.) fused probabilistically per-voxel over time is demonstrated at real outdoor campus/KITTI scale. Dynamic-object detection is **not** addressed by this paper at all (see item 13); it remains an open sub-problem the SIH project would need to solve independently of anything shown here. DERIVED.
- **Adaptive variable-resolution 2.5D spatial representation:** Low/negative relevance as a positive precedent for this specific SIH mechanism, and useful as disconfirming-type context. This paper is a real-time, GPU-accelerated, outdoor, large-scale (city-block/campus, up to 0.67 km² visualized) metric-semantic mapping system that deliberately uses a **fixed-resolution, full-3D** voxel-hashed TSDF representation rather than a 2.5D or variable/adaptive-resolution one, and the authors explicitly justify choosing volumetric-over-elevation representations by GPU parallelizability (p.2 §II-A). INFERENCE: this suggests real-time large-scale outdoor metric-semantic mapping does not, in this system's design, strictly require adaptive spatial resolution or a 2.5D restriction to hit low-millisecond per-frame processing — but this paper neither tests nor claims that adaptive/2.5D resolution would be worse; it simply did not use one, and it explicitly hit a GPU-memory/scale ceiling (item 26) that an adaptive or hierarchical resolution scheme might plausibly address (HYPOTHESIS, not demonstrated by this paper).

## Figures/Tables/Equations Directly Consulted

- **Fig. 1** (p.1): Example scenario — a global map with a semantic point-cloud/mesh view color-coded by class (Building, Road, Sidewalk, Grass, Tree, Car) alongside a vehicle-eye photo, illustrating the target use case.
- **Fig. 2** (p.4): Full system block diagram — Camera/LiDAR/IMU → Semantic Segmentation / State Estimator / Measurement Processing → Metric Mapping + Semantic Mapping → Metric-Semantic Traversability Extraction → occupancy map + localization → Motion Planning.
- **Fig. 3** (p.5): Diagram of non-projective distance calculation for flat vs. curved surfaces, showing angle θ (ray-to-gradient), ψᵢ (projective distance), gradient vector 𝐠ᵢ, true distance dᵢ, and curvature radius r.
- **Fig. 4** (p.6): (a) handheld mapping rig (LiDAR + camera) with device-frame axes labeled; (b) autonomous test vehicle with four 16-beam LiDARs and a Livox Mid-70.
- **Fig. 5** (p.7): Campus dataset samples — raw images (top) and pixel-wise semantic annotations (bottom) with a 14-class color legend.
- **Fig. 6** (p.7): Five global map reconstructions (SemanticKITTI 00/05, SemanticUSL 12, FusionPortable Building_Day/Campus_Road_Day) with area sizes labeled, colored by semantic class.
- **Fig. 7** (p.9): Self-collected sequence 00/01 semantic maps aligned to satellite/top-view images with marked navigation goal points.
- **Fig. 8** (p.10): Per-vertex heatmaps of height difference, steepness, roughness for seq. 00/01, plus paired occupancy-grid images with vs. without semantic information (grassland circled in the "without" case), yellow lines showing planned paths.
- **Fig. 9** (p.10): Third-person photo sequences of the real vehicle navigating campus paths for seq. 00 and seq. 01 regions.
- **Table I** (p.3): Comparison of 8 prior semantic-mapping systems (and "Ours") across metric-mapping backbone, processing unit, semantic-update method, map representation, scale, application — confirms "Ours" = NvBlox backbone, GPU, Bayesian update, TSDF representation, Outdoor scale, Navigation application.
- **Table II** (p.6): Experiment parameters — voxel size ν (0.25/0.3 m), truncation distance τ=5ν, traversability radius r=0.25 m, thresholds t_hd=0.6 m, t_v=20°, t_r=30°.
- **Table III** (p.8): RE/CD/RC/mIoU/Acc/Time results across all sequences for VoxBlox, VoxField, Ours-Proj, Ours(-wo-Bay).
- **Table IV** (p.8): Per-module computation time (ms) and speedup ratio vs. VoxField/VoxBlox on SemanticKITTI seq. 00, for both the 3080Ti desktop and Jetson ORIN.
- **Eq. 1-2** (p.4): ESIKF LiDAR residual and VIO photometric-error residual.
- **Eq. 3** (p.5): Depth/height image projection from a raw point cloud.
- **Eq. 4-5** (p.5): Non-projective signed-distance formula and its recursive weighted update.
- **Eq. 6** (p.5): Recursive Bayesian update of per-voxel semantic class probability.
- **Eq. 7-8** (p.7): Reconstruction Error and Chamfer Distance formulas.

## Uninterpretable / Uncertain Sections

1. The **steepness** formula v_s = arccos(𝐧ᵥᵢ) (p.6 §IV-D-1) appears to be missing a second operand for the arccos argument to yield a scalar angle (e.g., a dot product against a reference "up"/gravity vector); the rendered equation shows only the normal vector itself. Could not confirm the complete formula from the visible text.
2. The **roughness** formula v_r = (1/|B|)·Σ_{v∈B} 𝐧ᵥ (p.6 §IV-D-1) is stated as the average of normal vectors within a ball, described in prose as measuring "irregularities and unevenness," but no additional operator (e.g., a norm, variance, or subtraction against a reference direction) that would convert an averaged vector into a conventional "roughness" scalar is clearly visible in the rendered equation. Interpretation of how this yields the described roughness property is uncertain (flagged as INFERENCE in the body text, not asserted as fact).
3. The **height-difference** formula is written with "argmax" (v_hd = argmax‖vᵢ−vⱼ‖, p.6) where the surrounding prose describes a maximum *value*, not an argmax (index pair); this is likely a notational slip in the source paper itself rather than a rendering artifact, but it could not be independently resolved.
4. Exact digit-level values in every cell of **Table III**'s Time[ms] row across all 21 sequences (p.8) were legible but dense/small; the general order-of-magnitude trend (baselines tens-to-hundreds of ms vs. proposed method single-digit-to-tens of ms) is reported with confidence, but individual cell values were not all independently double-checked digit-by-digit and are not exhaustively transcribed here to avoid risk of transcription error.
5. Reference [33] (the paper's own cited source for "the detail of the network," p.4 §IV-B) is not itself available in this document, so the full semantic segmentation network architecture and the precise mechanism of the confidence/aleatoric-uncertainty head could not be verified beyond the one-paragraph summary given here.

## Summary Assessment

This paper presents a GPU-accelerated, real-time (DIRECT EVIDENCE: <7 ms/frame claim, p.1) metric-semantic mapping system for outdoor ground-robot navigation, built on a fixed-voxel-size TSDF volumetric map (not a 2.5D elevation representation) with semantic labels fused per-voxel via a recursive Bayesian filter, and it explicitly chose this volumetric 3D route over 2.5D/radiance-field alternatives for GPU-parallelizability (DIRECT EVIDENCE, p.2). Terrain analysis is handled by a concrete geometric+semantic mesh-filtering pipeline (DIRECT EVIDENCE, p.6 §IV-D) whose value is demonstrated by an explicit failure case (grassland traversal without semantics, Fig. 8/9). The system does not perform dynamic-object detection or tracking, does not implement loop closure, and does not implement any spatially- or semantically-adaptive resolution scheme — resolution is a single fixed value per mapping run, chosen offline based on scene scale and GPU memory (DIRECT EVIDENCE, Table II and its footnote). Its own stated limitations (GPU-memory-bound scalability, drift without loop closure, semantic spatio-temporal consistency) are all explicit (DIRECT EVIDENCE, p.9 Conclusion) and are relevant open gaps for the SIH problem beyond what this paper solves.
