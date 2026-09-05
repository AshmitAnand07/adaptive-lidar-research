# External Literature — Structured Inventory

Status: Phase 2 (external literature research) complete. This is a compact,
comparable index across all external papers found; full per-paper detail
(page/section citations, evidence labels, exact quotes) lives in the five
group files this indexes. Use this file to compare external papers directly
against the 8 supplied papers in `../evidence/citations.md` — the column set
mirrors the same dimensions used in the Phase 1 per-paper analyses
(`../research/papers/`).

**Total external papers analyzed in depth: ~104** (24 in Group A, 28 in Group
B, 16 in Group C, 23 in Group D, 19 in Group E, minus ~6 cross-group
duplicates — see "Cross-Group Duplicates" below). This count excludes papers
listed only in each group's "Papers Considered But Excluded" section (snippet
leads not independently verified) and patents (listed for context, not counted
as literature).

Legend — **Res.** = resolution strategy (Fixed / Adaptive); **Adaptive
category** uses the six-category taxonomy: *AcqSens* (adaptive sensor
acquisition), *Sens* (adaptive sensing, broader), *NeurComp* (adaptive neural
computation), *AttnROI* (adaptive attention/ROI), *CompRepr* (adaptive
computational representation), *MapRes* (adaptive map resolution — the
persistent-map category most relevant to the SIH problem). **Repr.** = 2D /
2.5D / 3D. Cells marked "—" mean not addressed/not applicable per the source
paper. Confidence flags (full text / abstract / snippet) are in the group
files, not repeated here — treat any number in this table as being at the
confidence level recorded in the linked source.

---

## Group A — Adaptive Resolution & Hierarchical Mapping
Full detail: `group_a_adaptive_resolution_hierarchical.md` (H1, H5, H6)

| Paper (year) | Venue | Repr. | Res. / driver | Adaptive category | Semantic | Terrain | Dynamic-obj | Uncertainty | Computational evidence |
|---|---|---|---|---|---|---|---|---|---|
| D-Map (2023) | T-RO | 3D | Adaptive, occupancy-structure-driven | MapRes | — | — | Static-world assumption | — | Qualitative only |
| ROG-Map (2023) | arXiv | 3D | **Fixed**, robocentric bounded window | none (contrast case) | — | — | — | Standard occupancy | 5.96ms/20ms frame @ 50Hz |
| Ada3D (2023) | ICCV | 3D voxel+BEV | Fixed map; per-frame input filtering | NeurComp + CompRepr | — | — | — | — | 5x compute/memory cut, 1.5x latency |
| Hierarchical Adaptive Voxel-Guided Sampling (2023) | arXiv | Point | Per-frame sampling, not map | CompRepr | — | — | — | — | >100x faster than FPS |
| AVS-Net (2024) | arXiv | Point/voxel | Per-frame adaptive voxel size | CompRepr | — | — | — | — | Qualitative |
| VoxelMap (2021) | RA-L | 3D voxel | Adaptive, coarse-to-fine (geometry/planarity) | MapRes | — | — | — | Probabilistic (IEKF) | Qualitative |
| **Adaptive-LIO (2025)** | arXiv | 3D voxel | **Adaptive, distance-from-sensor-driven** | MapRes (+ AcqSens elements) | — | — | — | — | Qualitative |
| Adaptive Patched Grid Mapping (2023) | arXiv | 2D/2.5D multi-layer | Adaptive, request/planning-horizon-driven | MapRes | — | plausible (unconfirmed) | plausible (unconfirmed) | — | "Significant" memory cut (unquantified) |
| A-OctoMap (2024) | arXiv | 3D octree | Adaptive/hierarchical | MapRes + CompRepr | — | — | — | — | Qualitative, simulation-only |
| wavemap (2023) | arXiv | 3D wavelet-hierarchical | Adaptive, wavelet-coefficient-driven | MapRes | — | — | — | Enables uncertainty-aware sensor models | Qualitative |
| OctoMap (2013) | Auton. Robots | 3D octree | Adaptive, occupancy-homogeneity-driven | MapRes | — | — | Weak (re-observable) | Log-odds probabilistic | Not retrieved |
| Langerwisch & Wagner (2013) | IROS | 2D quadtree | Adaptive, sensor-error-bound-driven | MapRes | — | — | — | Bounded-error (interval) | Not retrieved |
| Li/Ruichek stereo quadtree (~2013) | IEEE | 2D quadtree | Adaptive | MapRes | — | — | — | — | Not retrieved |
| MAP-ADAPT (2024) | ECCV | 3D semantic mesh | Adaptive, semantic+geometry-driven | MapRes | Yes, class-driven | — | — | — | "Significantly reduces" (unquantified) |
| Efficient Semantic-Aware TSDF w/ Adaptive Res. (2023) | RAAI conf. | TSDF voxel | Adaptive, semantic-driven | MapRes | Yes | — | — | — | Not retrieved (metadata only) |
| Comm.-Aware Hierarchical Map Compression (2025) | arXiv | Occupancy grid | Adaptive, rate-distortion-optimized | MapRes | — | — | Yes, explicit (static+dynamic) | Probabilistic occupancy | Not quantified |
| G-VOM (2021) | arXiv | 3D voxel | **Fixed** (contrast case) | none | — | Rich (slope, roughness, obstacles) | — | — | 10Hz update, real vehicles |
| HOTFormerLoc (2025) | CVPR | 3D octree+transformer | Adaptive, octree-depth multi-scale | MapRes + AttnROI | — | — | — | — | Not retrieved |
| Adaptive Fovea for Scanning Depth Sensors (2020) | IJRR | Raw scan | Adaptive, info-theoretic scan control | **AcqSens** (pure sensing contrast case) | — | — | — | — | Not retrieved |
| Multi-Scale Dynamic Sparse Voxelization (2024) | Sensors | Voxel→BEV | Sparse + multi-scale FPN | CompRepr + NeurComp | — | — | Detection only, no tracking | — | 45 FPS; +5.9-7.6% ped. mAP |
| Range-Based Point Cloud Density Optimization (2023) | arXiv | Point cloud | **Adaptive, explicit range-driven** (input-level) | CompRepr | — | — | — | — | Improves 4 detectors, 2 datasets |
| Survey of Spatial Memory Representations (2026) | arXiv (survey) | survey | N/A | N/A | — | — | — | — | **Found no rigorous overhead accounting in the field** |
| DFPS (2025, snippet-only in A) | Sensors | Point cloud | Adaptive, terrain-complexity-driven | CompRepr | — | Yes (driver) | — | — | Blocked (see Group B full read) |

## Group B — Attention/Foveated, Uncertainty & Risk-Aware, Real-Time
Full detail: `group_b_attention_uncertainty_realtime.md` (H3, H5)

| Paper (year) | Venue | Repr. | Res. / driver | Adaptive category | Semantic | Terrain | Dynamic-obj | Uncertainty | Computational evidence |
|---|---|---|---|---|---|---|---|---|---|
| FOVEA (2021) | ICCV | 2D camera | Adaptive, saliency/task-driven | AttnROI | Indirect | — | Indirect (temporal prior) | — | Streaming AP 17.8→23.0, no compute increase |
| Adaptive Fovea (2020, dup of A) | IJRR | Raw scan | Adaptive, hardware scan-pattern | AcqSens | — | — | — | — | Qualitative (snippet) |
| Towards a MEMS-based Adaptive LiDAR (2020) | 3DV | Raw sparse depth | Adaptive, MEMS scan-pattern | AcqSens | — | — | — | — | Not reported |
| Fast Attention-Based Simplification of LiDAR PCs (2026) | arXiv | Point cloud | Adaptive, learned attention | AttnROI | — | — | — | — | Faster than FPS |
| PointSplit (2023/2025) | IPSN | Point (RGB-D) | **Adaptive, semantics-driven biased sampling** | AttnROI + CompRepr | Yes, explicit driver | — | — | — | 24.7x faster, similar accuracy |
| DH-V2 (2026) | arXiv | 2D camera | **Fixed** geometric foveation (contrast case) | AcqSens (weak) | — | — | — | — | 0.52ms/frame, 1433x compression |
| Space-variant/active vision survey (2023) | Auton. Robots | survey (camera) | Survey | AcqSens + AttnROI | — | — | — | — | Not retrieved |
| Occupancy Grids (Elfes, 1990) | UAI | 2D/3D grid | **Fixed** (foundational) | none | — | — | — | Founding Bayesian occupancy | N/A (1990) |
| Gaussian Process Occupancy Maps (2012) | IJRR | Continuous field | Adaptive, query-time/"anytime" | CompRepr | — | — | — | Native GP variance | Limited by GP scalability (per follow-on lit.) |
| Deep ISM Priors for Evidential Occupancy (2020) | arXiv/IV | Grid (radar) | Fixed | none | — | — | — | Evidential (bounded confidence) | Not reported |
| EviLOG (2021) | GitHub/arXiv | Grid | Fixed | none | — | — | — | Evidential (belief/disbelief/uncertainty) | Not reported |
| E2-BKI (2025/26) | RA-L | Kernel-based Gaussian, 2.5D/3D | **Adaptive, scene-geometry-driven** | CompRepr (borderline MapRes) | Yes, semantic-confidence uncertainty | Off-road relevant | — | Semantic-prediction uncertainty | "Real-time" (unquantified) |
| ContraMap (2026) | arXiv | Kernel-based | Fixed | CompRepr | — | — | — | Learned contrastive "uncertainty class" | "Substantially more efficient" (unquantified) |
| Uncertainty-Aware VI-SLAM (2024/25) | ICRA | Volumetric submaps | Not stated | none | — | — | — | Depth-prediction + registration-fit | Not reported |
| SOGMP/SOGMP++ (2023) | CoRL | Occupancy grid | Not confirmed variable | CompRepr (weak) | — | — | **Central — predicts future dynamic occupancy** | Predictive/aleatoric (VAE distribution) | Not reported |
| Uncertainty-driven Planner (2022) | arXiv | Predicted occupancy | Fixed | none | — | — | — | Epistemic, over predicted regions | Not reported |
| RAMP (2022/23) | ICRA | **2.5D** | Fixed grid; risk in planning horizon, not resolution | none (contrast case) | — | Central (CVaR terrain risk) | — | Known-free/occupied/unknown distinction | Not reported |
| EVORA (2023/24) | arXiv | Terrain patches | Not spatially variable | none | — | Central | — | **Aleatoric + epistemic, separately routed** | Not reported |
| STEP + SubT results (2021/23) | Field Robotics | Not detailed | Not addressed | none | — | Central (field-tested caves/mines) | — | CVaR tail-risk | Not reported |
| RiskMap (2024) | arXiv | Continuous risk field | Not addressed | none | — | Urban on-road | Implied (traffic participants) | Sensor-noise (visualized) | Not reported |
| CVaR-MPPI (2022) | arXiv | **No spatial map** (contrast case) | N/A | none | — | — | — | Trajectory-outcome risk only | 80Hz on GPU |
| Risk-aware planetary rover path planning (2023) | ICRA | Not detailed | Not addressed | none | — | Central (heterogeneous terrain) | — | Multimodal slip-distribution fusion | Not reported |
| Is Semantic SLAM Ready for Embedded? (2025) | arXiv (survey) | Geometric/NeRF/Gaussian Splatting | N/A | N/A | Compared | — | — | — | Jetson AGX Orin; NeRF/GS not embedded-ready |
| SPAQ-DL-SLAM (2024) | ICARCV | DROID-SLAM (learned) | Fixed; static compression only | model compression (not adaptive) | — | — | — | — | 18.9% FLOPs cut, 79.8% size cut, ATE improved 10.5% |
| Voxel-Based 3D Detection Efficiency Analysis (2021) | ICETCI | Voxel | Diagnostic (motivates distance-restriction) | motivates MapRes | — | — | — | — | **40-60% speedup, but "fail to detect distant small objects"** |
| **Agile3D (2025)** | MobiSys | Point cloud, multi-branch | **Adaptive, content+contention-driven, per-frame** | NeurComp + CompRepr | — | — | — | — | +7% acc. over static, matched latency, real Jetson |
| DaDe (2022/23) | VISAPP | 2D camera | N/A (temporal forecasting) | NeurComp | — | — | Stream objects (not persistent map) | — | Not quantified |
| Are We Ready for Real-Time LiDAR Sem. Seg.? (2024) | IROS workshop | Standard segmentation nets | Fixed (benchmark paper) | N/A | Standard classes | — | Related MOS models named | — | Most models NOT real-time on Jetson |
| Mixture-of-Experts Edge 3D Detection (2025) | ICCV | LiDAR+camera | Multi-scale + **distance/content-aware routing** | NeurComp | — | — | — | — | +3.58% acc., +159% Jetson speedup |
| DFPS (2025, full read) | Sensors | Point cloud | **Adaptive, density/terrain-complexity-driven** | CompRepr | — | Yes (driver) | — | — | Up to ~9,278x speedup; **overhead cancels benefit at small scale** |

## Group C — 2.5D/Elevation, Semantic Mapping, Terrain/Traversability
Full detail: `group_c_25d_semantic_terrain.md` (H3, H4)

| Paper (year) | Venue | Repr. | Res. / driver | Adaptive category | Semantic | Terrain | Dynamic-obj | Uncertainty | Computational evidence |
|---|---|---|---|---|---|---|---|---|---|
| MEM (2023) | arXiv | **2.5D** | **Fixed** (4cm uniform) | none | Yes (Detectron2/Lite R-ASPP) | Plugin-deferred | — | Gaussian Bayesian + Dirichlet | 2.6ms RTX4090, 23.6ms Jetson Orin |
| RoadRunner (2024) | arXiv | **2.5D** | **Fixed** (20cm) | none | Not at runtime (label-gen only) | Central (CVaR cost) | Explicitly NOT handled | Not provided (future work) | 131.85ms, ~4x vs. baseline |
| **RoadRunner M&M (2024)** | RA-L | **2.5D** | **Adaptive, distance-tier (2 fixed tiers)** | MapRes | Not in own model | Central | Not addressed | Not provided | ~100ms; ~50%/~30% improvement over RoadRunner |
| SSMI (2021/23) | T-RO | **3D** octree | Adaptive, occupancy/log-odds homogeneity | MapRes | Yes, per-voxel categorical | — | Static-world | Dirichlet-style categorical | Compressed leaf count ~indep. of resolution |
| **Larsson et al. (2022)** | arXiv | **3D** octree | **Adaptive, explicit semantic-class-weighted** | MapRes | **Yes, central driver** | Not (generic classes) | Static-world | Probabilistic (per-leaf categorical) | Planning 10% faster, 60% less variance |
| Asgharivaskasi & Atanasov multi-robot (2024) | arXiv | 3D octree | Adaptive, consensus/compression-driven | MapRes | Yes | — | — | Bayesian consensus | Not reported |
| Stache et al. UAV path planning (2021/22) | ECMR/journal | Flat 2D | **Adaptive, explicit semantic-content-driven (via altitude)** | AcqSens → produces MapRes | **Yes, central driver** | Not (flat-field agri.) | — | GP posterior variance | mIoU + mission time vs. fixed-altitude |
| Resolution-adaptive Quadtrees UAV (2022, snippet) | IEEE | 2D quadtree (likely) | Adaptive, observation-resolution-keyed | MapRes | Likely | — | — | — | Not verified |
| Terrain-Aware Semantic Mapping Subterranean (2023) | Frontiers Robotics AI | 3D octree | **Fixed** (5cm base) | weak CompRepr | Yes (3 independent layers) | Central (slope+curvature+stairs) | — | Log-odds, bounded for dynamics | 7 bits/voxel; DARPA SubT 3rd place |
| Watch Your STEPP (2025) | arXiv | Dense image-space | Fixed (tied to image res.) | none | Self-supervised (no labels) | Central (reconstruction-error-based) | — | Implicit (reconstruction error) | Not reported |
| Fankhauser et al. elevation mapping (2014/18) | CLAWAR/RA-L | **2.5D** (foundational) | **Fixed** | none | No (base method) | General geometry | — | Per-cell Kalman variance | Not verified (secondary) |
| Kraetzschmar et al. quadtree (2004) | IFAC/IEEE | 2D | Adaptive (foundational) | MapRes | — | — | — | — | "10-50x" memory compression (snippet) |
| Wellington & Stentz (2004) | ICRA | Grid (likely 2.5D) | Not confirmed | perception-adaptive (not resolution) | No (binary height-correction) | Central (vegetation vs. load-bearing) | — | — | Not confirmed |
| Survey of Traversability Estimation (2022) | arXiv | survey | N/A | N/A | — | Central topic | — | — | Does not surface adaptive-resolution as a live axis |
| Variable-Resolution Virtual Maps USV (2026) | arXiv | 2D quadtree | **Adaptive, SLAM-uncertainty/info-density-driven** | MapRes | — | N/A (water) | — | **Central driver** | Not reported |
| Multi-Res. Elevation Mapping, Planetary Rotorcraft (2021) | IROS | **2.5D** | **Adaptive, pixel-footprint/measurement-density-driven** | MapRes | — | Central (landing safety) | — | Probabilistic fusion framework | "Efficient" (unquantified) |

## Group D — Dynamic Occupancy, Motion Segmentation, Scene Flow, Temporal
Full detail: `group_d_dynamic_temporal_perception.md` (H2)

| Paper (year) | Venue | Repr. | Res. / driver | Adaptive category | Semantic | Terrain | Dynamic-obj | Uncertainty | Computational evidence |
|---|---|---|---|---|---|---|---|---|---|
| Nuss et al. RFS DOGMa (2016/18) | IJRR | 2D BEV grid | **Fixed** | none | — | — | Foundational (PHD/MIB filter velocity) | Probabilistic (RFS) | Real-time (unquantified) |
| Danescu et al. (2011) | T-ITS | 2D grid | Fixed (inferred) | none | — | — | Foundational (particle position+velocity) | Implicit | Not available |
| Schreiber et al. RNN DOGMa (2022) | IV | 2D BEV grid | **Fixed** | none | Yes (joint output head) | Drivable-area head | Per-cell velocity, learned E2E | Occupancy-probability only | Not confirmed |
| Categorized Grid (2024) | IEEE/arXiv | 2D DOGMa + overlay | **Fixed** (inherited) | none | Cell-state labels | Occlusion-cause labeling | Inherited dynamic labels | Reliability/cause labeling | Not confirmed |
| Dynamic OGM w/ BEVFusion (2024) | Sensors | 2D BEV grid | **Fixed** | none | Yes (per-cell class) | — | Position+velocity+class per cell | Standard DOGMa | nuScenes; MAE velocity/heading |
| DATMO Review (2020) | Robotica | survey | N/A | N/A | — | — | Core topic | Filter-based | N/A |
| MotionNet (2020) | CVPR | 2D BEV grid | **Fixed** (feature pyramid ≠ map res.) | NeurComp (feature pyramid only) | — | — | Joint category+motion, single pass | — | 53 Hz (reduced confidence) |
| Dynamics-Aware Spatiotemporal Occ. Pred. (2022) | IROS | Occupancy grid | **Fixed** | none | — | — | Explicit static/dynamic segmentation stage | — | Not confirmed |
| Learning Spatiotemporal OGM Lifelong Nav (2021/22) | ICRA | 2D time-stamped grids | **Fixed** | none | Possibly (3D backend) | — | Explicit, self-supervised future-state | — | Not confirmed |
| DynORecon (2024/25) | ICRA (sub.) | Volumetric (unspecified) | **Unclear — flagged gap** | Cannot determine | — | Free-space only | **Explicit, per-object, incremental** | — | ~20 FPS, ~10cm accuracy |
| Spatio-Temporal Voxel Layer (2020) | IJARS/ROS | Sparse voxel (OpenVDB) | **Fixed** (sparse ≠ adaptive) | CompRepr (sparse, not adaptive) | — | — | Dynamic-world-aware clearing (map-level) | — | ~400% less CPU vs. standard ROS layer |
| LMNet (2021) | RA-L/IROS | Range image | **Fixed** | none | — | — | Foundational learned MOS | — | Faster than sensor frame rate |
| 4DMOS (2022) | RA-L | Sparse 4D voxel | **Fixed** (sparse ≠ adaptive) | CompRepr | — | — | Receding-horizon, sequence-native | Binary Bayesian filter | "Time/memory efficient" (unquantified) |
| MambaMOS (2024) | ACM MM | Point cloud (temporal) | Not adaptive | none | — | — | State-space motion-aware fusion | — | Not confirmed |
| SegNet4D (2025) | T-ASE | BEV (sequential) | **Fixed** | none | Yes (multi-class) | Implicit (standard classes) | Rich — class + dynamic + instance | — | Real-time-oriented (unquantified) |
| PointPWC-Net (2019/20) | ECCV | Point (feature pyramid) | Coarse-to-fine = **feature pyramid, not map res.** | NeurComp | — | — | Dense per-point flow | — | Not confirmed |
| SeFlow (2024) | ECCV | Not confirmed | Not adaptive (inferred) | none | — | — | **Explicit static/dynamic classification** | — | "Real-time capable" |
| Flow4D (2024/25) | RA-L | 4D voxel | **Fixed** | none | — | — | Dense multi-frame motion field | — | 15.1 FPS RTX3090; +45.9% vs. SOTA |
| SemanticFlow (2025) | arXiv | Full-res. point cloud | Coarse-to-fine = **prediction refinement, not map res.** | NeurComp | Instance seg. | — | Joint flow+instance segmentation | — | +8.7-65.5% flow, +3.6-11.9% seg. |
| PointRNN (2019) | arXiv | Raw points | N/A | N/A | — | — | Foundational point-level motion prediction | — | Not confirmed |
| **Funk et al. (2021)** | RA-L | 3D log-odds octree | **Adaptive, real-time, region-automatic** | **MapRes (cleanest pure example)** | — | Not dedicated | **None — explicitly static/quasi-static scope** | Log-odds occupancy | "Unprecedented speed" (unquantified) |
| **MURAL (2026)** | arXiv | Pillar/voxel | **Adaptive, deadline-driven, spatially UNIFORM per frame** | NeurComp | — | — | Via downstream classical tracker only | — | mAP 0.499-0.564 @ 100-248ms; 0/30 collisions |
| **AdaOcc (2024)** | arXiv | Grid + point-cloud ROI hybrid | **Adaptive, spatially variable (ROI vs. background)** | MapRes/CompRepr | — | — | **Unconfirmed — critical open gap** | — | +13% IoU, +40% Hausdorff (close-range) |

## Group E — Sparse LiDAR Perception, Sparse 3D CNNs/Tensors
Full detail: `group_e_sparse_representations.md` (H5, H6)

| Paper (year) | Venue | Repr. | Res. / driver | Adaptive category | Semantic | Terrain | Dynamic-obj | Uncertainty | Computational evidence |
|---|---|---|---|---|---|---|---|---|---|
| Submanifold Sparse Conv (2017) | arXiv (foundational) | 3D sparse tensor | **Fixed** (sparsity ≠ resolution) | CompRepr + NeurComp | — | — | — | — | Qualitative ("less computation") |
| Minkowski Engine (2019) | CVPR | Sparse tensor (N-D, 4D) | **Fixed** per level; multi-level via pooling | CompRepr + NeurComp | — | — | Enables (not itself) | — | "Substantially lower" memory (qual.) |
| VoxelNet (2017/18) | CVPR | Dense 3D voxel (baseline) | **Fixed** | none (dense baseline) | — | — | — | — | Expensive (dense 3D conv) |
| SECOND (2018) | Sensors | 3D voxel, sparse | **Fixed** (sparsity) | CompRepr | — | — | — | — | 4x train / 3x inference speedup vs. dense |
| PointPillars (2018/19) | CVPR | 2.5D pseudo-image | **Fixed** pillar grid | none (base) | — | — | — | — | 62-105 Hz; **own limitation: loses distant/small-object detail** |
| OctNet (2016/17) | CVPR | Hybrid grid-of-octrees | **Adaptive, occupancy/density-driven** | CompRepr (bordering MapRes) | — | — | — | — | 32³→256³ resolution at comparable memory |
| Voxel Hashing (2013) | SIGGRAPH Asia | Sparse hash-block volume | **Fixed** within blocks (sparse allocation) | CompRepr | — | — | — | — | Real-time large-scale (qual.) |
| SPADE (2023) | arXiv (accelerator) | Pillar BEV | **Fixed** grid; hardware sparsity exploitation | CompRepr + NeurComp | — | — | — | — | **36-89% compute cut; 1.3-28.8x speedup (hw-dependent)** |
| FSD (2022) | NeurIPS | Sparse point/voxel | **Fixed** voxel; never densifies | CompRepr | — | — | Generic detection | — | **Linear not quadratic scaling w/ range; 2.4x vs. dense at 200m** |
| FSD++/Super Sparse (2023) | TPAMI | Sparse + temporal | Fixed; temporal sparsification | CompRepr | — | — | Residual-point change detection (proxy) | — | SOTA (numbers not retrieved) |
| Focal Sparse Conv (2022) | CVPR (Oral) | Voxel sparse tensor | Fixed grid; **learned per-site importance/dilation** | NeurComp + AttnROI | — | — | — | — | Not itemized |
| SPS-Conv (2022) | NeurIPS | Voxel sparse tensor | Fixed grid; magnitude-based pruning | NeurComp | — | — | — | — | **>50% GFLOPs cut, no accuracy loss** |
| FALO (2025) | arXiv | Voxel, serialized dense | **Deliberately dense** (disconfirming case) | (reverses CompRepr) | — | — | — | — | 25-30 IPS Jetson Orin vs. single-digit for sparse baseline |
| LiDAR-PTQ (2024) | ICLR | Voxel sparse tensor, quantized | Fixed; numeric precision only | NeurComp (narrow) | — | — | — | — | 3x speedup, INT8≈FP32 accuracy |
| **SPVNAS (2020)** | ECCV | Hybrid sparse-voxel+point | Fixed (fusion of 2 fixed-res. branches) | CompRepr + NeurComp | — | — | **Explicit gain on bicyclist/motorcyclist classes** | — | 7.6x compute cut → only **2.7x measured speedup** |
| Cylinder3D (2020/21) | CVPR | Cylindrical voxel | **Implicitly distance-adaptive** (coordinate-system side-effect) | CompRepr (implicit MapRes) | Standard classes | Indirect | Indirect | — | "Improved efficiency/accuracy" (qual.) |
| **MrHash (2025)** | TOG | Flat hash, per-region resolution | **Adaptive, SDF-variance/uncertainty-driven** | **MapRes (cleanest true example, whole search)** | — | — | — | **Central driver** | **~4x memory, up to 13x speedup vs. fixed baseline** |
| Spira (2025) | arXiv | Voxel sparse tensor | Fixed; locality-optimized kernel | CompRepr (engineering) | — | — | — | — | 2.8x faster than TorchSparse++ |
| SD-Conv/SPADE+ (2024) | CVPR workshop | Pillar BEV, accelerator | Fixed grid; per-pillar selective dilation | NeurComp + AttnROI | — | — | — | — | **16.2x speedup, 18.1x compute cut (custom silicon)** |

---

## Cross-Group Duplicates (same paper found independently by 2+ groups)

- **Adaptive Fovea for Scanning Depth Sensors** (Tasneem et al., 2020) — Groups A and B. Treated as one source; A's entry is snippet-level, B's is also snippet-level (both hit the same 403 access failure independently) — confidence not improved by duplication, noted for completeness.
- **DFPS** (Dong et al. / "efficient downsampling... global feature preservation," Sensors 2025, DOI 10.3390/s25144279) — Group A got a blocked (403, snippet-only) read; Group B independently obtained a full-text read via the PMC open-access mirror. **Use Group B's entry as authoritative**; Group A's entry is superseded.
- **A-OctoMap** and **Probabilistic quadtrees for variable-resolution mapping** — mentioned in passing in Group D's "excluded" list as adjacent to Group A's fuller coverage; not double-counted in the ~104 total.

## How to Use This Inventory Alongside the Supplied-Paper Set

Compare any row above against `../evidence/citations.md` (bibliographic) and
`../research/papers/*.md` (full Phase 1 analyses) using the same dimensions:
representation (2D/2.5D/3D), resolution strategy, adaptive-mechanism category,
semantic/terrain/dynamic-object/uncertainty handling, and computational
evidence. The cross-cutting synthesis of both sets together (which
combinations exist, which don't, and what that means for gap analysis) is in
`../research/02_technical_taxonomy.md`.
