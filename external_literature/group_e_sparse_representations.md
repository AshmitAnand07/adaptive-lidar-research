# External Literature — Group E: Sparse LiDAR Perception, Sparse 3D CNNs/Tensors

**Assigned families:** Sparse LiDAR perception; sparse 3D CNNs and sparse tensors.
**Assigned hypotheses to stress-test:** H5, H6.

## Searches Conducted

1. sparse LiDAR perception survey 2024 2025
2. submanifold sparse convolution 3D detection paper
3. Minkowski Engine sparse tensor 3D convolutional neural network
4. sparse convolution latency FLOPs measured 3D object detection autonomous driving
5. SECOND sparse convolution 3D object detection point cloud voxel
6. PointPillars real-time object detection point clouds
7. VoxelNet end-to-end learning point cloud 3D detection
8. octree neural network OctNet 3D deep learning high resolution
9. voxel hashing real-time 3D reconstruction sparse
10. sparse BEV detection 3D LiDAR 2024 efficient
11. quantization pruning 3D object detection LiDAR edge deployment embedded
12. Focal Sparse Convolutional Networks 3D object detection
13. Spatial Pruned Sparse Convolution efficient 3D object detection
14. FALO fast accurate LiDAR 3D object detection resource-constrained devices
15. fully sparse 3D object detection long range FSD point cloud
16. variance adaptive voxel grid hash GPU 3D reconstruction "resolution where it counts"
17. adaptive hybrid sparse convolution predictor feature pruning embedded point cloud
18. SPVNAS sparse point-voxel efficient 3D architecture search semantic segmentation
19. Cylinder3D LiDAR semantic segmentation sparse cylindrical partition
20. multi-scale dynamic sparse voxelization 3D point cloud object detection
21. "LiDAR-PTQ" arxiv post-training quantization
22. level of detail LOD point cloud mapping robot navigation coarse-to-fine
23. early exit dynamic depth network point cloud 3D perception efficient inference

Additionally, WebFetch was used to retrieve and read (not just search-snippet) the following primary sources: SPADE (arXiv:2305.07522, HTML), Fully Sparse 3D Object Detection (arXiv:2207.10035), Super Sparse 3D Object Detection / FSD++ (arXiv:2301.02562), MrHash / "Resolution Where It Counts" (arXiv:2511.21459), Submanifold Sparse Convolutional Networks (arXiv:1706.01307), Minkowski Engine / 4D Spatio-Temporal ConvNets (arXiv:1904.08755), Spatial Pruned Sparse Convolution (arXiv:2209.14201), FALO (arXiv:2506.04499), Spira (arXiv:2511.20834), SPVNAS (arXiv:2007.16100), Selectively Dilated Convolution / SD-Conv (arXiv:2408.13798). One WebFetch attempt against an arXiv ID guessed for LiDAR-PTQ (2312.10484) resolved to an unrelated particle-physics paper and was discarded; the correct identifier (2401.15865) was subsequently found via search but only abstract/GitHub-README-level content was retrieved, not the full PDF — flagged accordingly below. An OpenReview fetch for the same paper was blocked by a bot-verification page and returned no content.

## Papers

### Submanifold Sparse Convolutional Networks
- Authors: Benjamin Graham, Laurens van der Maaten
- Year: 2017
- Venue: arXiv (widely cited foundational method; underlies SparseConvNet)
- Link/identifier: arXiv:1706.01307
- Access level: full paper read (WebFetch; abstract + method summary retrieved, experimental tables not itemized in the fetch output)
- Problem: Regular sparse convolution progressively "dilates" the set of active (non-zero) sites with every layer, so after a few layers a sparse input becomes almost fully dense — destroying the computational benefit of sparsity for very sparse, thin, or curve-like data (pen strokes, 3D surfaces/point clouds).
- Representation: 3D voxelized sparse tensor (generalizes to any dimension); operates on the "submanifold" of active sites only.
- Resolution strategy: Fixed voxel grid resolution. No spatially-variable resolution — the innovation is computational (which sites get convolved), not a resolution policy.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (sparsity of the underlying data is exploited so computation is restricted to active sites) and, secondarily, **adaptive neural computation** (the convolution rule itself changes behavior — output active set = input active set — to prevent dilation, i.e., the compute graph's active-site footprint is a controlled function of input sparsity rather than a fixed dense grid). This is NOT adaptive/variable resolution.
- Perception method: Learned (CNN backbone), generic — used downstream for classification, semantic segmentation, detection.
- Terrain handling: None (generic sparse-data operator, not a terrain method).
- Dynamic-object handling: None directly; used as the workhorse backbone inside many detectors that do handle dynamic objects (see SECOND, FSD, etc.).
- Temporal processing: None (static 3D only in this paper; temporal generalization comes later with MinkowskiEngine 4D).
- Uncertainty handling: None.
- Computational characteristics: DIRECT EVIDENCE — the paper claims the method "performs on par with state-of-the-art methods whilst requiring substantially less computation" relative to regular (dilating) sparse convolution, because the active-site count stays bounded across depth instead of growing. Exact FLOPs/latency tables were not captured in the fetch (reduced-confidence on specific numbers; the qualitative claim itself is direct from the abstract).
- Datasets: 3D shape/segmentation benchmarks and handwriting/pen-stroke data in the original paper (specific benchmark names not confirmed via this fetch).
- Evaluation: Accuracy vs. compute trade-off relative to dense and regular-sparse baselines.
- Limitations: Only prevents dilation at the site level; does not prune "clearly-uninteresting" active sites (that idea is picked up later by SPS-Conv/Focal-Conv). Efficiency gains depend on how sparse the input truly is — at high fill-rates the benefit shrinks (this general caveat is echoed later, e.g., in MinkowskiEngine notes below).
- Relevance to SIH problem: This is the base computational primitive almost every voxel-based LiDAR detector in this literature review (SECOND, PointPillars variants, Focal-Conv, SPS-Conv, SPADE, FSD) is built on. It establishes that "sparse ≠ variable resolution" — it is a computation-restriction technique on a fixed grid, relevant to the "reduce compute cost" goal of the SIH problem but orthogonal to the "vary resolution by distance/semantics" idea.
- Evidence level(s) for key claims: DIRECT EVIDENCE (qualitative efficiency claim, mechanism); INFERENCE (relative importance in the later citation graph, derived from how frequently downstream papers cite/use it).

### 4D Spatio-Temporal ConvNets: Minkowski Convolutional Neural Networks (Minkowski Engine)
- Authors: Christopher Choy, JunYoung Gwak, Silvio Savarese
- Year: 2019
- Venue: CVPR 2019
- Link/identifier: arXiv:1904.08755
- Access level: full paper read (WebFetch)
- Problem: Existing sparse 3D CNNs handled only fixed 3D coordinates; no general library/formulation existed for arbitrarily high-dimensional sparse tensors (notably 4D space-time for LiDAR video), and coordinate management (hashing, striding, pooling across resolutions) needed a unifying abstraction.
- Representation: Sparse tensor — explicit coordinates of non-empty elements + paired feature vectors; generalizes voxels to N-D and to space-time.
- Resolution strategy: Fixed base voxel resolution per sparse tensor; the library supports multiple resolution *levels* via strided/pooled sparse tensors (a standard CNN encoder-decoder pyramid), but there is no data-driven, spatially-varying resolution policy within a single level — it is sparsity, not adaptive resolution.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (the sparse-tensor coordinate/feature structure adapts to occupied space, independent of any persistent "map"); the generalized convolution definition also enables **adaptive neural computation** in the loose sense that compute is a function of the active coordinate set at each layer.
- Perception method: Learned (generalized sparse convolution) backbone for classification and semantic segmentation.
- Terrain handling: None directly.
- Dynamic-object handling: The 4D (space+time) formulation is explicitly built to let a network jointly reason over a temporal window of LiDAR sweeps, which is the natural substrate for later dynamic/moving-object segmentation work, but this paper itself targets segmentation, not tracking.
- Temporal processing: DIRECT EVIDENCE — this is the paper's headline contribution: treating time as a 4th coordinate axis in the same generalized sparse convolution, evaluated on temporal semantic segmentation of LiDAR sequences (e.g., 4D SemanticKITTI-style setup) alongside static ScanNet/SemanticKITTI segmentation.
- Uncertainty handling: None.
- Computational characteristics: DIRECT/DERIVED — the fetch summary reports "substantially lower" memory than dense baselines and GPU inference-speed improvements from reduced memory bandwidth, and separately notes (from general library documentation, not this specific paper) that coordinate-management overhead becomes non-negligible once occupancy exceeds roughly 50% density — i.e., sparse-tensor machinery is not a free lunch once the scene is not very sparse. This overhead point is DERIVED/INFERENCE from the fetched summary rather than a verbatim number quoted from the paper's tables (reduced confidence — full paper's quantitative tables were not itemized in the fetch).
- Datasets: ScanNet (indoor), SemanticKITTI (outdoor LiDAR), plus a synthetic/temporal 4D segmentation setting.
- Evaluation: mIoU on semantic segmentation; qualitative/derived compute and memory comparisons vs. dense baselines.
- Limitations: Requires structured coordinate sparsity for its efficiency advantage to hold; implementation/engineering complexity is considerably higher than dense conv; benefit degrades as scenes densify.
- Relevance to SIH problem: Minkowski Engine and its "sparse tensor network" abstraction is the direct technical ancestor of the "adaptive computational representation" category as defined for this project — it is the clearest illustration that a hash/coordinate-indexed sparse structure is a computation trick tied to per-frame occupancy, not a persistent variable-resolution map.
- Evidence level(s) for key claims: DIRECT EVIDENCE (temporal 4D formulation, datasets); DERIVED/INFERENCE (overhead-crossover claim, memory-savings magnitude).

### VoxelNet: End-to-End Learning for Point Cloud Based 3D Object Detection
- Authors: Yin Zhou, Oncel Tuzel
- Year: 2017 (arXiv) / CVPR 2018
- Venue: CVPR 2018
- Link/identifier: arXiv:1711.06396
- Access level: abstract/preprint only (search-snippet level; not independently WebFetched for full tables) — flagged low-to-moderate confidence for anything beyond the qualitative architecture description.
- Problem: Prior LiDAR detectors relied on hand-crafted feature encodings of point clouds (bird's-eye-view height maps, hand-tuned statistics) rather than learning features directly from raw points.
- Representation: Dense 3D voxel grid with a learned per-voxel "Voxel Feature Encoding" (VFE) layer; output fed to a 2D region-proposal-network head.
- Resolution strategy: Fixed uniform voxel size grid. No adaptive/variable resolution.
- Adaptive mechanism categor(y/ies): None of the six categories cleanly apply — VoxelNet is the *dense* voxel baseline against which nearly every sparse method in this review (SECOND, PointPillars, sparse-conv derivatives) explicitly measures its efficiency gains. It is included for lineage/baseline purposes.
- Perception method: Learned, single-stage end-to-end 3D object detection.
- Terrain/Dynamic/Temporal/Uncertainty handling: None.
- Computational characteristics: HYPOTHESIS/INFERENCE only from this fetch level — widely reported in the field (and echoed in the SECOND search results above) as computationally expensive because 3D convolution is run densely over a mostly-empty voxel grid; this is why SECOND's sparse-convolution reformulation of the same VoxelNet-style pipeline reports 3–4× speedups (see SECOND entry) — that comparison is DERIVED from SECOND's paper, not from VoxelNet's own text.
- Datasets: KITTI (car/pedestrian/cyclist).
- Evaluation: 3D/BEV average precision on KITTI.
- Limitations (as reported in later literature, not verified first-hand here): slow due to dense 3D convolution over a mostly-empty grid; this exact bottleneck motivated SECOND's sparse-conv reformulation and PointPillars' pillar (2D) simplification.
- Relevance to SIH problem: Establishes the dense-voxel baseline against which "sparsity gives real speedup" claims throughout this literature are measured; useful for calibrating how large the reported sparse-conv speedups actually are relative to.
- Evidence level(s) for key claims: WEB VERIFIED (existence, architecture, venue); INFERENCE (performance characterization, since it is triangulated from what later sparse-conv papers report about it rather than read directly in VoxelNet's own tables).

### SECOND: Sparsely Embedded Convolutional Detection
- Authors: Yan Yan, Yuxing Mao, Bo Li
- Year: 2018
- Venue: Sensors (MDPI), vol. 18
- Link/identifier: DOI 10.3390/s18103337
- Access level: abstract/preprint only (search-snippet level; not independently WebFetched)
- Problem: Make voxel-based 3D detection (VoxelNet-style) fast enough for real use by replacing dense 3D convolution over the whole voxel grid with sparse convolution restricted to occupied voxels.
- Representation: 3D voxel grid processed with sparse (and submanifold sparse) convolutions before compressing to a 2D map for detection.
- Resolution strategy: Fixed uniform voxel grid; no spatially variable resolution. The improvement is purely computational (skip empty voxels), i.e., sparsity, not adaptivity of resolution.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (sparse voxel processing restricted to occupied cells).
- Perception method: Learned single-stage 3D object detector; also introduced a new angle-loss formulation for orientation regression.
- Terrain/Dynamic/Temporal/Uncertainty handling: None specific.
- Computational characteristics: DIRECT EVIDENCE (from search-result summary of the paper's own reported numbers, not independently re-verified against the PDF) — "a factor-of-4 speed enhancement during training ... and a factor-of-3 improvement in inference speed" versus the dense convolutional (VoxelNet-style) baseline, on KITTI. This is exactly the kind of *measured, end-to-end* computational benefit from a sparse (not variable-resolution) representation that is central to stress-testing H5/H6 — flag: this benefit comes from sparsity/occupancy, not from a distance- or semantic-adaptive resolution policy.
- Datasets: KITTI.
- Evaluation: 3D/BEV AP on KITTI; training/inference wall-clock speed vs. dense baseline.
- Limitations: Benefit is bounded by how sparse the scene actually is; a scene approaching full occupancy would erode the 3–4× advantage (this general property is corroborated by the sparsity-density caveat noted for Minkowski Engine above); fixed grid resolution still limits far-range point density handling.
- Relevance to SIH problem: One of the clearest, earliest, *measured* (not merely theoretical) demonstrations that exploiting point-cloud sparsity computationally yields real, substantial end-to-end speedups — directly relevant to whether "adaptive/sparse grids reduce end-to-end computation" (they can, when the underlying data really is sparse and the hardware/software stack supports sparse ops).
- Evidence level(s) for key claims: DIRECT EVIDENCE (reported speedup factors, though sourced via a secondary summary rather than the primary PDF table — moderate confidence).

### PointPillars: Fast Encoders for Object Detection from Point Clouds
- Authors: Alex H. Lang, Sourabh Vora, Holger Caesar, Lubing Zhou, Jiong Yang, Oscar Beijbom
- Year: 2018 (arXiv) / CVPR 2019
- Venue: CVPR 2019
- Link/identifier: arXiv:1812.05784
- Access level: abstract/preprint only (search-snippet level)
- Problem: Achieve real-time, accurate 3D detection without dense 3D convolution or hand-crafted BEV features, by encoding points into vertical "pillars" (no z-binning) processed by a fast 2D CNN.
- Representation: 2D pseudo-image, built from per-pillar PointNet features over a bird's-eye-view grid — effectively a 2.5D representation (height information folded into a per-pillar learned feature rather than a discretized z-axis).
- Resolution strategy: Fixed uniform pillar grid in x-y; no spatially variable resolution. The pseudo-image itself is described as sparse (most pillars are empty) but this is exploited by hardware/accelerator work (e.g., SPADE, SD-Conv below), not by PointPillars itself.
- Adaptive mechanism categor(y/ies): None in the base method — PointPillars produces a naturally sparse representation (only ~3–5% of pillars are non-empty per SPADE's characterization) that later work exploits computationally, but PointPillars itself runs a dense 2D CNN over the full pseudo-image grid.
- Perception method: Learned single-stage detector (2D CNN backbone + SSD-style detection head).
- Terrain/Dynamic/Temporal/Uncertainty handling: None specific in the base paper.
- Computational characteristics: DIRECT EVIDENCE (via search summary) — pipeline runs at 62 Hz, with a faster variant reaching 105 Hz while matching state-of-the-art accuracy of the time; reported as a 2–4× runtime improvement over prior methods.
- Datasets: KITTI (primary), later widely adopted on nuScenes/Waymo by follow-on work.
- Evaluation: 3D/BEV AP on KITTI; runtime (Hz).
- Limitations: Reported (via search summary, DERIVED) to suffer "spatial information loss when processing sparse and unevenly distributed 3D data, especially for distant objects or points on the edges of objects" — i.e., a fixed-resolution pillar grid loses distant/small-object detail, a direct point of relevance to the SIH's concern about "coarse distant resolution loses important objects."
- Relevance to SIH problem: (a) Establishes the pillar/2.5D-style representation family relevant to the SIH's own 2.5D framing; (b) its *own* stated limitation — fixed-resolution loss of distant/small-object detail — is disconfirming evidence against assuming a single fixed resolution (whether or not adaptively varied) is automatically sufficient; this is exactly the kind of failure mode the SIH problem needs to investigate for its own resolution policy.
- Evidence level(s) for key claims: DIRECT EVIDENCE (throughput numbers); DERIVED (limitation regarding distant/sparse points, drawn from secondary characterization rather than the primary paper's own limitations section, verbatim).

### OctNet: Learning Deep 3D Representations at High Resolutions
- Authors: Gernot Riegler, Ali Osman Ulusoy, Andreas Geiger
- Year: 2016 (arXiv) / CVPR 2017
- Venue: CVPR 2017
- Link/identifier: arXiv:1611.05009
- Access level: abstract/preprint only (search-snippet level)
- Problem: Dense volumetric 3D CNNs scale cubically in memory/compute with resolution, capping practical training resolutions around 32³; most real 3D data (surfaces) is sparse in 3D space, wasting most of that cubic budget on empty space.
- Representation: Hybrid grid-of-octrees — a set of shallow, unbalanced octrees tiled over space, where each octree adaptively subdivides only in regions containing surface/occupied data; leaf nodes store pooled features.
- Resolution strategy: **Adaptive/variable spatial resolution driven by data occupancy/density** — this is a genuine variable-resolution data structure (fine octree cells where there is surface detail, coarse/large leaf cells in empty space), not merely a sparsity-exploiting fixed grid.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (octree depth/leaf size is chosen per-region based on where data is) — bordering on **adaptive map resolution** since the octree partition is a persistent spatial structure that could serve as a map, though OctNet's own use case (classification, orientation estimation, per-point labeling) treats it as a per-inference representation rather than a maintained/updated map.
- Perception method: Learned 3D CNN operating on the octree structure.
- Terrain/Dynamic/Temporal/Uncertainty handling: None.
- Computational characteristics: DIRECT EVIDENCE (via search summary) — enables training/inference at resolutions up to 256³ "while most other approaches use resolutions in the order of 32×32×32," by concentrating memory/compute allocation only where the octree has fine leaves; described as overcoming the "long-standing memory bottleneck" of dense volumetric CNNs. Exact FLOPs/latency numbers were not captured at this access level (moderate confidence on specific magnitudes; high confidence on the qualitative 32³→256³ capability claim, which is a strong, specific, checkable claim).
- Datasets: 3D object classification/orientation benchmarks and point-cloud labeling tasks (specific dataset names not itemized at this access level).
- Evaluation: Classification/orientation accuracy at a given resolution vs. memory/compute budget.
- Limitations: Adaptivity is driven by geometric occupancy only (where is there any data at all), not by semantic importance, risk, or task-relevance — i.e., it is an occupancy-adaptive, not semantically-adaptive, resolution policy. Octree traversal introduces pointer-chasing/indirection overhead relative to a flat array, a cost that the 2025 MrHash paper (below) explicitly targets and replaces with a flat hash table for GPU-friendliness.
- Relevance to SIH problem: This is arguably the most directly relevant *foundational* precedent for "variable-resolution 3D representation" in the entire literature search — it demonstrates, with a concrete measured capability jump (8× per axis, i.e., 512× volumetric resolution increase at comparable memory), that adaptive spatial resolution driven by data occupancy is old and well-established (2016), predating essentially all the "adaptive LiDAR mapping" framing in the SIH problem statement. Its limitation — occupancy-only adaptivity, no semantic/risk awareness — is precisely the gap that semantic/uncertainty-aware adaptive resolution work (tracked in other groups) aims to fill.
- Evidence level(s) for key claims: DIRECT EVIDENCE (32³ vs 256³ capability claim, mechanism); INFERENCE (classification of adaptivity as "occupancy-driven, not semantic").

### Real-time 3D Reconstruction at Scale using Voxel Hashing
- Authors: Matthias Nießner, Michael Zollhöfer, Shahram Izadi, Marc Stamminger
- Year: 2013
- Venue: ACM Transactions on Graphics (SIGGRAPH Asia 2013)
- Link/identifier: DOI 10.1145/2508363.2508374
- Access level: abstract/preprint only (search-snippet level)
- Problem: Regular dense voxel grids (or hierarchical octrees) for real-time SDF-based 3D reconstruction (e.g., KinectFusion-style) do not scale to large environments because memory is allocated uniformly whether or not a region contains observed surface.
- Representation: Sparse voxel-block volume addressed by a spatial hash table — a flat, non-hierarchical alternative to octrees.
- Resolution strategy: Fixed voxel resolution *within* allocated blocks; the adaptivity here is about *which regions exist at all* (memory sparsity/allocation), not variable resolution per region. This paper is the origin of the flat-hash-table idea that MrHash (2025, below) later combines with genuine variable resolution.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (memory is allocated only for observed/occupied voxel blocks via hashing) — not adaptive resolution.
- Perception method: Classical (SDF fusion / TSDF integration), not learned.
- Terrain/Dynamic/Temporal/Uncertainty handling: None specific (general-purpose surface reconstruction).
- Computational characteristics: DIRECT EVIDENCE (via search summary) — enables real-time, large-scale reconstruction on then-contemporary GPU hardware by storing only occupied space, versus dense or octree-hierarchical alternatives; specific throughput/memory numbers not captured at this access level.
- Datasets: Interactive/live RGB-D scanning sessions (no fixed public benchmark; this predates standard SLAM benchmarks' widespread use for this exact comparison).
- Evaluation: Qualitative/real-time interactive reconstruction demonstrations; memory footprint vs. scene scale.
- Limitations: Fixed per-voxel resolution; no notion of adapting resolution to information content (that is exactly the gap MrHash's 2025 paper targets, twelve years later).
- Relevance to SIH problem: This is the direct technical ancestor of the flat-hash-table spatial data structure now being proposed (2025) as a base for genuinely *adaptive-resolution* mapping (MrHash). It shows the "sparse allocation" idea for maps is over a decade old and well-established, separate from resolution adaptivity, which is a comparatively recent and much rarer combination.
- Evidence level(s) for key claims: WEB VERIFIED (existence, mechanism, lineage); INFERENCE (its role as MrHash's direct ancestor, derived from MrHash's own stated contrast with "recursive octree structures" and hash-based flat storage).

### SPADE: Sparse Pillar-based 3D Object Detection Accelerator for Autonomous Driving
- Authors: (hardware accelerator research group; full author list not captured at this access level)
- Year: 2023
- Venue: arXiv (design-automation/architecture venue; likely DAC/ISCA-adjacent — exact venue not confirmed at this access level)
- Link/identifier: arXiv:2305.07522
- Access level: full paper read (WebFetch, HTML version)
- Problem: Pillar-based detectors (PointPillars-family) produce highly sparse pseudo-images (only ~3–5% of pillars non-empty), but standard GPU sparse-convolution accelerators are designed for element-wise (ReLU-induced) sparsity, not the "vector sparsity" pattern where entire channel-vectors for a pillar are zero — causing underutilization and memory-bank conflicts when naively applied.
- Representation: Pillar-based BEV pseudo-image (2.5D — height folded into per-pillar features), processed by sparse convolution variants.
- Resolution strategy: Fixed pillar grid. The paper's contribution is a hardware/dataflow mechanism to exploit existing sparsity, plus a "dynamic vector pruning" variant (SpConv-P) that prunes additional low-importance background pillars during inference — a computation-adaptive step, not a change to the underlying grid resolution.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (vector-sparsity-aware compute) plus **adaptive neural computation** (SpConv-P dynamically prunes pillars deemed unimportant across layers, changing the effective compute graph per input).
- Perception method: Learned detectors (PointPillars, CenterPoint, PillarNet) run through a custom accelerator design.
- Terrain/Dynamic/Temporal/Uncertainty handling: None specific (hardware-architecture paper, task-agnostic to detector semantics).
- Computational characteristics: DIRECT EVIDENCE (full text read) — this is the single richest quantitative source found in this review:
  - Computation savings: 36.3–89.2% reduction across PointPillars/CenterPoint/PillarNet on KITTI/nuScenes.
  - Speedup vs. an idealized dense accelerator baseline: 1.3–10.9×.
  - Energy savings vs. dense: 1.5–12.6×.
  - vs. GPU (RTX 2080 Ti): 4.1–28.8× speedup, 90.2–372.3× energy savings.
  - vs. Jetson NX (embedded GPU): up to 12.6× speedup.
  - Peak throughput: 500 FPS at <0.4% accuracy drop (most aggressive sparsity variant).
  - vs. prior sparse accelerator (PointAcc): 1.88–1.95× additional speedup.
  - Hardware overhead: only 4.3% extra silicon area for the highest-end configuration.
  All comparisons are explicitly against dense baselines (ideal dense accelerator, GPU) as well as a prior sparse-accelerator baseline (PointAcc) — i.e., this is genuine, measured, end-to-end (not merely theoretical-FLOPs) evidence.
- Datasets: KITTI, nuScenes.
- Evaluation: mAP/accuracy drop vs. speedup/energy trade-off across 7 model variants (SPP1–3, SCP1–3, SPN).
- Limitations: The most aggressive sparsity variant (SpConv-S) causes a real 2–5 mAP accuracy loss; the pruning-based variant (SpConv-P) balances this better but still incurs mapping overhead on GPU platforms; benefits are architecture-specific (a custom accelerator), so the very large multipliers (10×+) do not necessarily transfer to commodity GPU/CPU deployments (the GPU-only comparison numbers, still large at 4–29×, are the more directly transferable figures for non-custom-silicon settings).
- Relevance to SIH problem: **This is a strong, directly disconfirming-of-pessimism data point for H5** — it is rigorous, hardware-measured, end-to-end evidence (not just memory-footprint accounting) that exploiting spatial sparsity (a close cousin of "adaptive representation") gives large, real computational savings, provided the hardware/software stack is designed to exploit it. It is a strong caution, however, that the *sparsity* being exploited here is data sparsity (occupied vs. empty pillars), not a deliberate variable-resolution *policy* — the grid resolution itself is fixed throughout.
- Evidence level(s) for key claims: DIRECT EVIDENCE (all numeric results, read from the full paper).

### Fully Sparse 3D Object Detection (FSD)
- Authors: Lue Fan, Feng Wang, Naiyan Wang, Zhaoxiang Zhang
- Year: 2022
- Venue: NeurIPS 2022
- Link/identifier: arXiv:2207.10035
- Access level: full paper read (WebFetch)
- Problem: Mainstream LiDAR detectors build a dense BEV/voxel feature map whose computational and spatial cost scales **quadratically** with perception range, making them impractical for long-range (100–200 m) detection needed as sensing range grows.
- Representation: Point/sparse-voxel representation throughout the pipeline — never converts to a dense feature map.
- Resolution strategy: Fixed voxel size for the sparse voxel encoder; no variable resolution. The core idea is to never densify, not to vary resolution by region.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** — a Sparse Instance Recognition (SIR) module groups points into instances and does instance-wise feature extraction, resolving the "center-feature-missing" problem that previously forced fully-sparse detector designs to fall back to a dense map for the detection head.
- Perception method: Learned, two-stage-flavored (sparse voxel encoder + instance grouping/classification), single/dynamic-object detection task.
- Terrain handling: None.
- Dynamic-object handling: Framed generically as 3D object detection (car/pedestrian/cyclist-style categories); not dynamic-vs-static differentiated within the paper itself.
- Temporal processing: None in the base FSD paper (added in the FSD++ / Super Sparse extension below).
- Uncertainty handling: None.
- Computational characteristics: DIRECT EVIDENCE (full text) — computational and spatial cost is **roughly linear in the number of points and independent of perception range**, versus dense-map baselines whose cost is quadratic in range. On Argoverse 2 at a 200 m perception range (vs. Waymo's 75 m), FSD is **2.4× faster than its dense counterpart** while achieving state-of-the-art accuracy; also SOTA on Waymo Open Dataset. This is a direct, measured refutation of the idea that avoiding a dense representation only helps memory and not compute — here the *scaling law itself* (linear vs. quadratic) is the claimed and measured benefit, which is squarely relevant to whether "sparse/adaptive structures reduce end-to-end computation" (yes, and dramatically so, as range grows).
- Datasets: Waymo Open Dataset (75 m range), Argoverse 2 (200 m range).
- Evaluation: Standard 3D detection AP metrics per dataset; runtime/latency comparison vs. dense-map counterpart at matched range.
- Limitations: This is classified here as **naturally-sparse exploitation, not deliberate adaptive/variable resolution** — FSD's efficiency comes from never densifying a naturally sparse point cloud, not from a policy that assigns coarser resolution to some regions and finer to others. The instance-grouping (SIR) step itself is a heuristic/learned grouping stage that could fail for very close/overlapping instances (a stated design challenge motivating the SIR module in the first place, i.e., "center feature missing" is itself evidence of information loss under full sparsity that had to be specifically engineered around).
- Relevance to SIH problem: Directly relevant to the SIH's core question of whether avoiding dense (or coarsened) far-range representations pays off computationally: FSD is the single clearest example found of a paper that **rigorously measures end-to-end computational savings (not just memory) from spatial sparsity**, with the specific mechanism (avoiding quadratic-in-range dense maps) mapping closely onto the "progressively coarser resolution farther away" motivation in the SIH problem statement — except FSD's answer is "don't discretize into a dense map at all," rather than "discretize, but coarser far away."
- Evidence level(s) for key claims: DIRECT EVIDENCE (linear-vs-quadratic scaling claim and the 2.4× figure, both read from the paper itself).

### Super Sparse 3D Object Detection (FSD++)
- Authors: Lue Fan et al. (extension of FSD)
- Year: 2023
- Venue: TPAMI (journal extension of the NeurIPS 2022 FSD paper)
- Link/identifier: arXiv:2301.02562
- Access level: abstract/preprint only (WebFetch returned only the abstract page; full-text tables not retrieved — flagged reduced confidence for specific numbers)
- Problem: Extends FSD to exploit *temporal* redundancy across LiDAR sweeps in addition to spatial sparsity, to push long-range detection efficiency further.
- Representation: Sparse voxel/point representation, now aggregated across multiple frames via "residual points" (points that changed between consecutive frames) plus a selected subset of prior foreground points, forming an "ultra-sparse" multi-frame input.
- Resolution strategy: No spatial resolution variation; the innovation is temporal sparsification (many time-redundant points are dropped), which is a form of sparsity, not resolution adaptivity.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (temporal-redundancy-aware sparsification of the multi-frame input).
- Perception method: Learned, builds directly on FSD's sparse voxel encoder + SIR module.
- Terrain handling: None.
- Dynamic-object handling: DERIVED — computing frame-to-frame "residual points" is implicitly a change-detection mechanism that is closely related to (though not necessarily identical to) dynamic-object cues, since points that change across frames are disproportionately likely to belong to moving objects or newly-revealed static structure.
- Temporal processing: DIRECT EVIDENCE — explicit multi-frame aggregation via residual points is the paper's central mechanism.
- Uncertainty handling: None found.
- Computational characteristics: Claims SOTA on Waymo Open Dataset and superior long-range performance on Argoverse 2, per the abstract, but specific latency/memory/speedup numbers versus FSD were not retrievable at this access level — reduced confidence, flagged HYPOTHESIS-adjacent for exact magnitudes even though the qualitative direction (further efficiency gain from temporal sparsification) is asserted directly in the abstract.
- Datasets: Waymo Open Dataset, Argoverse 2.
- Evaluation: Standard AP metrics; comparison to FSD and other long-range detectors (exact table not retrieved).
- Limitations: Not captured at this access level.
- Relevance to SIH problem: Suggests that *temporal* sparsity (not just spatial) is a further, compounding source of legitimate computational savings for a moving-robot LiDAR pipeline — relevant to the SIH's interest in temporal stability/dynamic objects, though this paper is squarely about efficiency, not about explicitly modeling object dynamics.
- Evidence level(s) for key claims: WEB VERIFIED (existence, mechanism); reduced-confidence/abstract-only for quantitative claims.

### Focal Sparse Convolutional Networks for 3D Object Detection
- Authors: Yukang Chen, Yanwei Li, Xiangyu Zhang, Jian Sun, Jiaya Jia
- Year: 2022
- Venue: CVPR 2022 (Oral)
- Link/identifier: arXiv:2204.12463
- Access level: abstract/preprint only (search-snippet level; not independently WebFetched for full tables)
- Problem: Standard sparse convolution treats all active sites uniformly, but different spatial positions in a 3D scene contribute unequally to detection accuracy — some sparse regions deserve more (dilated) computation than others.
- Representation: Voxel-based sparse tensor (built on submanifold sparse convolution).
- Resolution strategy: Fixed voxel grid. The novelty is *learned, position-wise importance* controlling which sites get extra dilation/compute — i.e., an importance-driven variation in *effective receptive field/compute*, not a change to the map's stored resolution.
- Adaptive mechanism categor(y/ies): **Adaptive neural computation** (a learned predictor decides per-site dilation/output shape) and **adaptive attention/ROI** (position-wise importance prediction functions as a soft spatial attention mechanism over the sparse tensor).
- Perception method: Learned single/multi-modal (Focals Conv-F fuses with camera features) 3D object detector.
- Terrain/Dynamic/Temporal/Uncertainty handling: None specific.
- Computational characteristics: Not captured in detail at this access level; the paper is reported (via search summary) to outperform prior single-model entries on the nuScenes test benchmark, with efficiency framed as "readily substitutable" for plain sparse conv layers at comparable cost — exact FLOPs/latency deltas not verified here (low confidence on magnitude, though the mechanism itself is clear).
- Datasets: KITTI, nuScenes, Waymo.
- Evaluation: Standard 3D detection AP metrics across three benchmarks.
- Limitations: Requires learning an importance predictor (added parameters/training complexity vs. plain sparse conv); importance is learned end-to-end for detection accuracy, not tied to an interpretable criterion like distance or semantic class — making it harder to audit/justify for a safety-relevant terrain/obstacle system than an explicit rule-based policy would be.
- Relevance to SIH problem: A clean example of the **"adaptive attention/ROI" / "adaptive neural computation"** categories realized *inside* a sparse-conv backbone: resolution/compute is varied by *learned importance*, not by distance or a fixed semantic rule — directly relevant to the SIH's interest in whether semantic/uncertainty-aware adaptation outperforms naive distance-based adaptation (this paper is evidence that importance-driven variation in effective resolution/compute is a viable, published, competitive design, though it targets accuracy first and efficiency second).
- Evidence level(s) for key claims: WEB VERIFIED (existence, mechanism, venue); INFERENCE (categorization as attention/ROI-like).

### Spatial Pruned Sparse Convolution for Efficient 3D Object Detection (SPS-Conv)
- Authors: Jianhui Liu, Yukang Chen, Xiaoqing Ye, Zhuotao Tian, Xiao Tan, Xiaojuan Qi
- Year: 2022
- Venue: NeurIPS 2022
- Link/identifier: arXiv:2209.14201
- Access level: full paper read (WebFetch)
- Problem: 3D scenes are dominated by redundant background points; standard sparse CNNs do not exploit this — and downsampling operations actually *amplify* the redundancy (more background sites survive relative to the shrinking foreground) rather than reducing it.
- Representation: Voxel-based sparse tensor; two new operators — SPSS-Conv (spatial-pruned submanifold sparse conv) and SPRS-Conv (spatial-pruned regular sparse conv).
- Resolution strategy: Fixed voxel grid. Adaptivity is at the level of *which sites survive to the next layer* (a pruning decision), not the grid's spatial resolution.
- Adaptive mechanism categor(y/ies): **Adaptive neural computation** (dynamically prunes candidate sites layer-by-layer based on feature magnitude as a proxy for importance — explicitly *not* a learned/attention-based importance signal, in contrast to Focal Sparse Conv above: the authors show simple feature-magnitude thresholding suffices, avoiding the training/inference overhead of a learned predictor).
- Perception method: Learned 3D object detector; the pruning operators are drop-in replacements for standard sparse conv layers in existing backbones.
- Terrain/Dynamic/Temporal/Uncertainty handling: None specific.
- Computational characteristics: DIRECT EVIDENCE (WebFetch of the paper) — **more than 50% reduction in GFLOPs without compromising accuracy**, evaluated across KITTI, Waymo, and nuScenes; the operators integrate into existing sparse 3D CNNs without architectural changes elsewhere in the network. Comparison baseline is explicitly standard (unpruned) sparse convolution — i.e., this measures the *additional* saving on top of the sparsity SECOND/submanifold-conv already provide, not sparsity vs. dense.
- Datasets: KITTI, Waymo, nuScenes.
- Evaluation: GFLOPs reduction and detection accuracy (AP/mAP) preserved across all three benchmarks.
- Limitations: A magnitude-based importance heuristic could, in principle, miss low-magnitude-but-informative features (e.g., faint returns from thin/distant structures) — this is not explicitly tested/discussed as a failure mode in the retrieved summary but is a natural risk of any magnitude-proxy pruning method and is directly relevant to the SIH's concern about thin structures and sparse/weak returns; flagged as INFERENCE/HYPOTHESIS since the paper's own limitations section was not itemized at this fetch depth.
- Relevance to SIH problem: A second strong, **directly measured** ("more than 50% GFLOPs reduction, no accuracy loss") example that additional computational adaptivity layered *on top of* baseline sparsity gives further real, quantified savings — reinforcing that "sparse structures reduce end-to-end computation" is well-supported for sparsity/pruning in this literature, while remaining a computation-level (not map-resolution-level) adaptivity.
- Evidence level(s) for key claims: DIRECT EVIDENCE (>50% GFLOPs figure, mechanism, baseline comparison); HYPOTHESIS (thin/faint-feature failure-mode risk, not paper-verified).

### FALO: Fast and Accurate LiDAR 3D Object Detection on Resource-Constrained Devices
- Authors: (not fully captured at this access level)
- Year: 2025
- Venue: arXiv (2025; conference venue not confirmed at this access level)
- Link/identifier: arXiv:2506.04499
- Access level: full paper read (WebFetch)
- Problem: Sparse convolution's irregular memory-access pattern, while FLOP-efficient in principle, maps poorly onto real edge accelerators (Jetson Orin GPU, Qualcomm Hexagon NPU) — the theoretical compute savings of sparsity do not translate into real speed on this class of hardware, and transformer-based alternatives (e.g., DSVT) incur quadratic attention cost.
- Representation: Voxel-based, but **serialized into a dense 1D sequence** by coordinate/proximity ordering, then processed with dense "ConvDotMix" layers instead of irregular sparse-indexed convolution.
- Resolution strategy: Fixed voxel grid; no variable resolution. The contribution is purely about making the *compute pattern* hardware-regular, trading sparsity-awareness for dense, predictable memory access.
- Adaptive mechanism categor(y/ies): Deliberately **moves away from** adaptive computational representation/sparse computation, back toward dense, regular computation — included here specifically as **disconfirming/nuancing evidence**: it shows that exploiting sparsity is not universally the right computational strategy once real (non-datacenter-GPU) hardware constraints are considered.
- Perception method: Learned 3D object detector.
- Terrain/Dynamic/Temporal/Uncertainty handling: None specific.
- Computational characteristics: DIRECT EVIDENCE (WebFetch) — on Jetson Orin GPU, FALO achieves roughly 25–30 inferences/sec, while the sparse-conv/transformer baseline DSVT drops to single-digit IPS on the same hardware due to sparse-operation overhead; on Qualcomm Hexagon NPU, FALO achieves 8–12 IPS while sparse methods largely fail to run efficiently at all. Accuracy on nuScenes is reported as competitive with DSVT despite running several times faster on edge hardware. Comparison baseline is explicitly the sparse/transformer SOTA (DSVT), on real edge silicon — not a synthetic FLOPs count.
- Datasets: nuScenes, Waymo.
- Evaluation: Inferences-per-second (IPS) on two edge platforms vs. accuracy (mAP-style) parity with DSVT.
- Limitations: The "hardware-friendly dense" approach sacrifices some of the theoretical FLOP-efficiency of true sparsity in exchange for real measured throughput on the specific target hardware; benefits are hardware-specific (results may not generalize identically to other accelerators/GPUs with better sparse-op support).
- Relevance to SIH problem: **This is important disconfirming/nuancing evidence for any assumption that "sparse/adaptive computational structures always reduce end-to-end computation."** FALO directly demonstrates the opposite on certain real embedded targets: nominally-efficient sparse convolution can be *slower in practice* than a well-engineered dense/regularized alternative, because irregular memory access defeats the hardware's throughput advantages. This is squarely the kind of "do not assume fewer active cells automatically means faster computation" caution the SIH problem explicitly calls out, and it is now backed by a directly-measured, cross-platform comparison.
- Evidence level(s) for key claims: DIRECT EVIDENCE (IPS numbers, comparison baseline, hardware platforms).

### LiDAR-PTQ: Post-Training Quantization for Point Cloud 3D Object Detection
- Authors: (Sifan Zhou et al., per associated GitHub — full author list not independently confirmed at this access level)
- Year: 2024
- Venue: ICLR 2024
- Link/identifier: arXiv:2401.15865
- Access level: abstract/preprint only (search-snippet level; a direct WebFetch attempt against a guessed arXiv ID (2312.10484) returned an unrelated physics paper, and an OpenReview fetch was blocked by a bot-verification page — both dead ends, so this entry relies on secondary search summaries only; confidence lowered accordingly)
- Problem: Post-training quantization (PTQ), well-established for 2D vision, degrades accuracy significantly when applied naively to sparse-convolution-based (or SPConv-free) 3D LiDAR detectors, blocking the memory/latency benefits of INT8 inference for edge deployment.
- Representation: Voxel-based sparse tensor (SPConv-based detectors) and non-sparse-conv detectors both addressed.
- Resolution strategy: Fixed grid; quantization affects numeric precision of weights/activations, not spatial resolution.
- Adaptive mechanism categor(y/ies): **Adaptive neural computation** in a narrow sense — "sparsity-based calibration" explicitly uses the sparsity pattern of activations to set quantization parameters, and "adaptive rounding-to-nearest" per-layer minimizes reconstruction error — i.e., the quantization *procedure* adapts to each layer's sparsity/error profile, though the network's compute graph shape itself is unchanged at inference time (quantization ≠ compute-graph adaptivity).
- Perception method: Learned 3D detector (post-hoc quantized, no retraining required beyond calibration).
- Terrain/Dynamic/Temporal/Uncertainty handling: None specific.
- Computational characteristics: DIRECT EVIDENCE (via search summary) — INT8 model accuracy is reported as "almost the same as" FP32 while giving a **3× inference speedup**, and the PTQ calibration process itself is **6× faster than quantization-aware training (QAT)** alternatives — i.e., both the resulting model and the *cost of producing it* are reported as favorable versus alternatives. Exact latency/mAP numbers and dataset-by-dataset breakdowns were not retrievable at this access level.
- Datasets: Reported as evaluated on standard LiDAR detection benchmarks (KITTI/Waymo/nuScenes per the paper's stated scope); exact per-dataset numbers not confirmed here.
- Evaluation: Accuracy retention (INT8 vs FP32) and speedup, plus calibration cost vs. QAT.
- Limitations: Not captured at this access level (abstract-only).
- Relevance to SIH problem: Quantization is an orthogonal but compounding efficiency lever to sparsity/adaptive-resolution ideas — relevant to the SIH's "edge deployment" and "CPU/GPU efficiency" concerns, but not itself a resolution or representation-adaptivity mechanism; included for completeness of the "efficient 3D perception" landscape and because the mandatory search-term list explicitly calls for quantization/pruning coverage.
- Evidence level(s) for key claims: WEB VERIFIED (existence, headline 3× and 6× claims, sourced from a search summary of the paper — moderate, not high, confidence given no direct full-text access).

### Searching Efficient 3D Architectures with Sparse Point-Voxel Convolution (SPVNAS)
- Authors: Haotian Tang, Zhijian Liu, Shengyu Zhao, Yujun Lin, Ji Lin, Hanrui Wang, Song Han
- Year: 2020
- Venue: ECCV 2020
- Link/identifier: arXiv:2007.16100
- Access level: full paper read (WebFetch)
- Problem: Standard sparse-voxel networks (e.g., MinkowskiNet-style) use low-resolution voxelization and aggressive downsampling, which disproportionately hurts small/thin objects (bicyclists, motorcyclists, poles) whose few points get merged away — a direct instance of "coarse resolution loses small/important objects."
- Representation: Hybrid — Sparse Point-Voxel Convolution (SPVConv) combines a standard sparse-voxel branch with a parallel high-resolution point-based branch that preserves fine detail with low added overhead; a Neural Architecture Search (3D-NAS) then searches this design space for efficient configurations under a resource budget.
- Resolution strategy: The point-based branch acts as an *effective-resolution booster* layered on top of a coarser voxel branch — i.e., a two-stream fixed-vs-fine mechanism rather than a spatially-varying single-resolution field. It is closer to **multi-representation fusion at fixed resolutions** than to variable/adaptive resolution.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (sparse voxel branch) fused with a full-resolution point branch, plus a NAS-driven architecture-level adaptivity to hit target compute budgets (a form of adaptive neural computation chosen once at design time rather than per-input at inference time).
- Perception method: Learned semantic segmentation (also transferred to KITTI 3D detection).
- Terrain handling: None directly, though outdoor driving-scene semantic segmentation on SemanticKITTI includes drivable-surface-adjacent classes as part of the label set (not analyzed further at this access level).
- Dynamic-object handling: DIRECT EVIDENCE — explicitly reports the method's "large advantage on small objects, such as bicyclists and motorcyclists," i.e., dynamic/vulnerable-road-user classes are the specific beneficiaries of preserving fine detail.
- Temporal processing: None.
- Uncertainty handling: None.
- Computational characteristics: DIRECT EVIDENCE (WebFetch) — outperforms MinkowskiNet by **3.3% mIoU with 1.7× model-size reduction, 1.5× computation reduction, and 1.1× measured speedup** at comparable budget; when down-scaled to a tight 15 GMACs budget, still **beats MinkowskiNet by 0.6% mIoU while achieving 8.3× model-size reduction, 7.6× computation reduction, and 2.7× measured speedup**. Notably, the *computation-reduction* multiplier (7.6×) is larger than the *measured wall-clock speedup* (2.7×) at the aggressive operating point — direct evidence that theoretical compute (FLOPs/MACs) reduction does not translate 1:1 into measured speedup, reinforcing the SIH's caution that "fewer map cells/FLOPs" ≠ proportionally "faster."
- Datasets: SemanticKITTI (ranked 1st on its leaderboard at time of publication), KITTI (detection transfer).
- Evaluation: mIoU (segmentation), transferred 3D detection AP; model size, MACs, measured latency all reported together, enabling exactly the FLOPs-vs-actual-speedup comparison called out above.
- Limitations: Not itemized in the retrieved summary; INFERENCE — the gap between compute-reduction and measured-speedup ratios suggests the point-based branch or NAS-selected operators introduce overhead not captured by a pure MACs count (e.g., irregular memory access again, echoing the FALO finding on different hardware).
- Relevance to SIH problem: Directly relevant on two fronts: (1) empirical evidence that a *fixed coarse* voxel resolution demonstrably loses small/dynamic objects (bicyclists/motorcyclists) unless compensated by an auxiliary fine-detail path — supporting the SIH's concern about "small and distant objects" and "thin structures" under coarse resolution; (2) a clean, numeric illustration that FLOPs/MACs reduction and measured wall-clock speedup are not the same thing, which should temper any architecture decision in this project that budgets purely by theoretical compute reduction.
- Evidence level(s) for key claims: DIRECT EVIDENCE (all headline numbers, mechanism, dataset ranking); INFERENCE (cause of the FLOPs-vs-speedup gap).

### Cylinder3D: An Effective 3D Framework for Driving-Scene LiDAR Semantic Segmentation
- Authors: Xinge Zhu, Hui Zhou, Tengfei Wang, Fangzhou Hong, Yuexin Ma, Wei Li, Hongsheng Li, Dahua Lin
- Year: 2020 (arXiv) / CVPR 2021
- Venue: CVPR 2021
- Link/identifier: (arXiv identifier not confirmed at this access level; widely indexed under "Cylinder3D")
- Access level: abstract/preprint only (search-snippet level)
- Problem: Outdoor LiDAR point clouds have strongly non-uniform density — very dense near the sensor, very sparse far away — which a naive Cartesian voxel grid handles poorly (either wasting cells near the sensor or under-resolving distant sparse returns).
- Representation: Voxelization in a **cylindrical coordinate system** (radius, angle, height) rather than Cartesian (x, y, z), processed with asymmetric 3D convolutions.
- Resolution strategy: **This is a subtle and important edge case for the sparsity-vs-adaptive-resolution distinction.** A uniform binning *in cylindrical coordinates* (equal steps in radius/angle/height) produces cells whose *Cartesian footprint grows with distance from the sensor* (since equal angular steps span more physical width at greater range) — i.e., the coordinate-system choice itself *implicitly* creates a distance-correlated, coarser-far/finer-near effective resolution, without any explicit "if far then coarsen" rule. This is DERIVED/INFERENCE (a geometric consequence of cylindrical binning) rather than something the paper frames in "adaptive resolution" language — the authors motivate it as matching point density, not as a deliberate resolution policy.
- Adaptive mechanism categor(y/ies): Best classified as **adaptive computational representation with an implicit, geometry-driven distance-adaptive resolution side-effect** — it straddles the "sparse because data is naturally sparse" and "deliberate variable resolution" categories in a way few other papers in this review do, and is flagged explicitly as a blurring case (see Terminology Notes).
- Perception method: Learned semantic segmentation (asymmetric residual blocks + dimension-decomposition context modeling).
- Terrain handling: Indirect — semantic segmentation label sets in outdoor driving datasets typically include "road"/ground classes, but this paper's focus is the representation, not terrain analysis per se; not independently analyzed further at this access level.
- Dynamic-object handling: Indirect (segmentation includes dynamic classes like car/pedestrian/cyclist as semantic categories, not tracked/detected instances).
- Temporal processing: None.
- Uncertainty handling: None.
- Computational characteristics: Reported (via search summary) to "improve computational efficiency and accuracy" versus Cartesian voxel and range-image baselines by better matching the natural density variation of LiDAR returns; specific FLOPs/latency numbers not retrieved at this access level (low-moderate confidence on magnitude).
- Datasets: SemanticKITTI, nuScenes (per general knowledge of the paper's evaluation scope; not independently re-verified at this fetch depth).
- Evaluation: mIoU on outdoor LiDAR semantic segmentation benchmarks.
- Limitations: The distance-adaptivity is a side effect of the coordinate system, not a controllable, tunable policy (e.g., it cannot be independently tightened for semantically important classes at long range without changing the whole binning) — a rigidity that explicit adaptive-resolution policies (semantic- or uncertainty-driven) are designed to avoid.
- Relevance to SIH problem: A concrete, well-cited (CVPR 2021) example that changing the *coordinate system* of a voxel grid — not adding an explicit adaptive-resolution rule — can already produce most of the benefit of "finer near, coarser far" naturally, which is directly relevant to the SIH's core distance-based-resolution premise: it suggests part of what a hand-designed "adaptive resolution" scheme would achieve may be obtainable more simply via coordinate-system choice alone, a genuine alternative worth weighing against explicit adaptive-grid engineering.
- Evidence level(s) for key claims: WEB VERIFIED (existence, mechanism, venue); INFERENCE (the "implicit distance-adaptive resolution" framing, which is this reviewer's geometric derivation, not the original authors' stated framing).

### Resolution Where It Counts: Hash-based GPU-Accelerated 3D Reconstruction via Variance-Adaptive Voxel Grids (MrHash)
- Authors: (Sapienza University of Rome group; full author list not captured at this access level)
- Year: 2025
- Venue: ACM Transactions on Graphics (TOG) 2025
- Link/identifier: arXiv:2511.21459
- Access level: full paper read (WebFetch, abstract/summary level of detail — full tables/figures not itemized; treat magnitude claims as moderately, not maximally, confident)
- Problem: Both fixed-resolution voxel grids and hierarchical-octree multi-resolution grids for real-time 3D surface reconstruction are memory-inefficient and/or GPU-unfriendly (octree traversal is inherently sequential/pointer-chasing, resisting full GPU parallelism).
- Representation: A **flat spatial hash table** (à la Nießner et al. 2013, above) storing voxel blocks at **multiple, per-region resolutions** chosen adaptively — i.e., genuinely combining sparse hashing *and* variable resolution in one structure.
- Resolution strategy: **True adaptive/variable resolution, driven by local variance of signed-distance-field (SDF) observations** (not distance from sensor, not a fixed geometric octree-occupancy rule as in OctNet) — fine voxels where SDF measurements disagree/are uncertain (implying fine geometric detail or noisy/complex surface), coarse voxels in smooth, homogeneous, low-variance regions. This is the single clearest example found in the entire two-family search of "map resolution adapted by an information/uncertainty-like criterion, not merely by occupancy or distance."
- Adaptive mechanism categor(y/ies): **Adaptive map resolution** (a persistent voxel-block map with spatially-varying resolution) — this is the rare case in this review that is unambiguously in this category, not merely "adaptive computational representation."
- Perception method: Classical (SDF-based fusion), with a downstream Gaussian-Splatting-style rendering use case (GPU-parallel quad-tree controlling splat density) rather than a learned perception network.
- Terrain handling: None (general-purpose surface reconstruction, not terrain-specific).
- Dynamic-object handling: None discussed at this access level.
- Temporal processing: Implied by "real-time" online reconstruction/fusion, but not elaborated at this fetch depth.
- Uncertainty handling: DIRECT EVIDENCE — variance of SDF observations is used explicitly as an **uncertainty-like signal** driving where to allocate finer resolution; this is the clearest instance in this entire family of resolution adaptivity driven by something other than raw distance or raw occupancy.
- Computational characteristics: DIRECT EVIDENCE (from the WebFetch summary, moderate confidence given abstract-level depth) — **roughly 4× lower memory usage** and **up to 13× speedup** versus fixed-resolution baselines, while maintaining reconstruction accuracy "on par" with those baselines. The comparison baseline is explicitly fixed-resolution voxel grids; a like-for-like comparison against octree-based multi-resolution methods is referenced qualitatively (avoiding their GPU-unfriendly traversal) but not given as a numbered speedup in the retrieved summary.
- Datasets: Not specified at this access level (real-time RGB-D/LiDAR-style range-data reconstruction scenes, per the paper's framing; specific benchmark names not confirmed).
- Evaluation: Memory footprint, runtime speed, and reconstruction accuracy (e.g., surface error) versus fixed-resolution and (qualitatively) octree baselines.
- Limitations: Not captured at this access level (abstract/summary only); a reasonable INFERENCE is that variance-based adaptivity, like OctNet's occupancy-based adaptivity, is a *geometric/signal* criterion rather than a *semantic/task* criterion — it would not necessarily allocate fine resolution to a semantically important but geometrically simple object (e.g., a flat sign or thin wire with locally low SDF variance), a gap structurally analogous to OctNet's limitation above.
- Relevance to SIH problem: **This is the single most directly relevant paper found for stress-testing H5.** It is a 2025, peer-reviewed (TOG), rigorously benchmarked demonstration that a genuinely *adaptive map resolution* structure — not merely a sparse/occupancy-driven one — gives large, measured memory (4×) **and** speed (13×) benefits over a fixed-resolution baseline, using a variance/uncertainty-like adaptivity criterion rather than a naive distance-only rule. It directly refutes the possibility that "distance-only or occupancy-only adaptive resolution is the only kind that works" and instead supports the SIH's own framing that non-distance-based (here, uncertainty-based) adaptivity criteria are viable and can outperform fixed-resolution baselines by a wide, measured margin. Caveat: this is 3D offline/online *surface reconstruction* (SDF fusion + rendering), not the SIH's robot-navigation 2.5D terrain/object-perception setting, so transfer of the exact numbers should be treated as INFERENCE, not DIRECT EVIDENCE, for the SIH use case.
- Evidence level(s) for key claims: DIRECT EVIDENCE (4× memory, 13× speedup claims, adaptivity criterion, data structure — all read from the fetched paper summary, moderate-confidence given abstract-level fetch depth rather than full-table verification); INFERENCE (transferability to the SIH's robot LiDAR mapping setting; semantic-blindness limitation).

### Spira: Exploiting Voxel Data Structural Properties for Efficient Sparse Convolution in Point Cloud Networks
- Authors: (not fully captured at this access level)
- Year: 2025
- Venue: arXiv (2025)
- Link/identifier: arXiv:2511.20834
- Access level: full paper read (WebFetch)
- Problem: Existing general-purpose sparse-convolution libraries (MinkowskiEngine, spconv, TorchSparse++) treat voxel coordinates as generic sparse-tensor indices, paying hash-table lookup and coordinate-management overhead that ignores the fact that voxelized point-cloud coordinates are *not* arbitrary — they have strong spatial locality (neighboring points map to nearby voxels).
- Representation: Voxel-based sparse tensor, with a specialized coordinate/memory layout exploiting spatial locality instead of generic hashing.
- Resolution strategy: Fixed voxel grid; purely a computational/engineering optimization of the sparse-convolution kernel implementation, not a resolution policy.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** — an engineering-level refinement of the same category as MinkowskiEngine/spconv, optimized specifically for the locality structure of voxelized point clouds rather than being a general N-D sparse-tensor library.
- Perception method: Backbone-level (library/kernel), used underneath learned detection/segmentation networks.
- Terrain/Dynamic/Temporal/Uncertainty handling: None (infrastructure paper).
- Computational characteristics: DIRECT EVIDENCE (WebFetch) — up to **2.8× faster inference than TorchSparse++**, with reduced memory footprint, evaluated against MinkowskiNet, spconv, and TorchSparse++ as baselines on SemanticKITTI and ScanNet, with claimed no accuracy degradation (since it only changes the compute/memory implementation, not the mathematical operation).
- Datasets: SemanticKITTI, ScanNet.
- Evaluation: Inference speed and memory vs. three established sparse-conv library baselines, accuracy held constant (same underlying convolution, different implementation).
- Limitations: Being a 2025 preprint at this access level, independent third-party validation/adoption is not yet established; gains are specific to voxelized point-cloud coordinate patterns and may not generalize to less-regular sparse-tensor use cases outside point clouds.
- Relevance to SIH problem: Reinforces that **even the same "sparse computation" idea has a further ~2–3× of low-level engineering headroom** left in 2025, six years after MinkowskiEngine and eight years after submanifold sparse convolution — evidence that "sparse representation reduces computation" is not a solved, saturated claim but an actively-improving one, and that a chosen sparse/adaptive data structure's *implementation quality* matters as much as its algorithmic design for realizing the "reduce end-to-end computation" goal.
- Evidence level(s) for key claims: DIRECT EVIDENCE (2.8× figure, baselines, datasets).

### Selectively Dilated Convolution for Accuracy-Preserving Sparse Pillar-based Embedded 3D Object Detection (SD-Conv / SPADE+)
- Authors: (not fully captured at this access level)
- Year: 2024
- Venue: CVPR Workshop 2024 (Efficient Deep Learning for Computer Vision)
- Link/identifier: arXiv:2408.13798
- Access level: full paper read (WebFetch)
- Problem: Dense pillar processing wastes computation on empty pillars; existing sparse approaches (submanifold conv) reduce that waste but restrict information flow between pillars enough to cause real accuracy degradation on embedded pillar-based detectors.
- Representation: Pillar-based BEV pseudo-image (as in PointPillars/SPADE), processed on a dedicated embedded sparse accelerator (SPADE+, an extension of the SPADE accelerator above).
- Resolution strategy: Fixed pillar grid; the adaptivity is in *which pillars get an enlarged effective receptive field* (selective dilation), based on a learned/assessed importance score per pillar — not a change to stored map resolution.
- Adaptive mechanism categor(y/ies): **Adaptive neural computation** (dilation amount is decided per-pillar based on assessed importance) with elements of **adaptive attention/ROI** (importance assessment functions as a spatial-attention-like gating mechanism).
- Perception method: Learned pillar-based 3D object detector, deployed on a custom accelerator extension.
- Terrain/Dynamic/Temporal/Uncertainty handling: None specific.
- Computational characteristics: DIRECT EVIDENCE (WebFetch) — **16.2× speedup** and **up to 18.1× computation reduction** on the embedded accelerator versus (implicitly) a densely-processed or naively-sparse baseline, while "maintaining detection performance without compromise, despite extreme pillar sparsity" — i.e., this explicitly targets and reports overcoming the accuracy loss that plain submanifold sparse conv (SubM-Conv) causes under extreme sparsity, which the paper itself frames as the prior approach's failure mode.
- Datasets: Not itemized at this access level (embedded pillar-detection benchmarks consistent with the SPADE lineage — likely KITTI/nuScenes; not independently confirmed).
- Evaluation: Speedup/computation-reduction vs. accuracy preservation, on embedded accelerator hardware.
- Limitations: Requires the custom SPADE+ hardware extension to realize the reported speedups — the 16–18× figures are architecture-specific and not necessarily achievable on a commodity GPU/CPU; the importance-assessment mechanism adds a design/verification burden for a safety-critical pipeline (similar caveat to Focal Sparse Conv above).
- Relevance to SIH problem: A very concrete, recent (2024), large-magnitude (16–18×) counter-example to any assumption that sparsity-driven adaptivity is inherently limited or that submanifold sparse convolution is already "good enough" — but also a caution that such large gains are realized on purpose-built silicon, reinforcing the broader pattern in this review that headline speedup multipliers are highly hardware-dependent (compare to FALO, where sparse ops instead *lose* to dense ones on different embedded silicon).
- Evidence level(s) for key claims: DIRECT EVIDENCE (16.2×/18.1× figures, mechanism, accuracy-preservation claim); INFERENCE (dataset identity, generalizability beyond the specific accelerator).

## Hypothesis Verdicts

### H5: "Adaptive map resolution can provide meaningful computational/memory benefits"
- **Verdict: Weakened/Refined — survives only in a narrower, more qualified form than as originally stated.**
- The strongest **direct** evidence for genuine *adaptive map resolution* (not mere sparsity) in this entire two-family search is a single 2025 paper, **MrHash** ("Resolution Where It Counts," arXiv:2511.21459): a persistent, variance-adaptive voxel-block hash map reports ~4× lower memory and up to 13× speedup versus a fixed-resolution baseline, with comparable reconstruction accuracy. This is genuine DIRECT EVIDENCE that adaptive map resolution, when driven by a well-chosen criterion (local SDF variance, an uncertainty-like signal) and implemented on GPU-friendly flat hashing, gives large, measured benefits — refuting the strong disconfirming possibility that adaptive-resolution structures are pure overhead. However, it is the *only* clearly-in-category example found; it is in a 3D offline/online reconstruction setting, not the SIH's robot-navigation 2.5D terrain/object setting, so transferring its magnitude to the SIH problem is INFERENCE, not direct evidence, and the fetch depth for this paper was abstract/summary-level (moderate, not maximal, confidence in its exact numbers).
- Separately, the much larger body of evidence in this family (SPADE, FSD, SPS-Conv, SPVNAS, SD-Conv, Spira, LiDAR-PTQ, SECOND) shows that **sparsity exploitation** — a related but distinct mechanism ("adaptive computational representation," not "adaptive map resolution") — reliably and measurably reduces end-to-end computation: 36–89% compute reduction and 1.3–10.9× speedup on a dedicated accelerator (SPADE); linear-vs-quadratic scaling with a 2.4× measured speedup at long range (FSD); >50% GFLOPs reduction with no accuracy loss (SPS-Conv); 7.6× computation reduction with 2.7× measured speedup (SPVNAS); 16.2× speedup on embedded silicon (SD-Conv). These are real, hardware-measured, end-to-end numbers, not merely theoretical FLOPs accounting, directly disproving the pessimistic possibility that "sparse/adaptive structures introduce excessive overhead that erases their savings" **when the target hardware and software stack are matched to the sparsity pattern**.
- **Critical, load-bearing caveat, itself found via direct disconfirming evidence:** the size — and even the *sign* — of the computational benefit is highly hardware- and implementation-dependent. **FALO** directly shows sparse convolution *losing* to a dense, serialized alternative on Jetson Orin GPU and Hexagon NPU (single-digit IPS for the sparse/transformer baseline DSVT vs. 25–30 IPS / 8–12 IPS for FALO's dense-serialized design on the same hardware). **SPVNAS** shows a 7.6× theoretical compute reduction yielding only a 2.7× measured wall-clock speedup at its most aggressive operating point — i.e., FLOPs/MACs reduction does not translate linearly into measured speed. **SPADE**'s own huge multipliers (10×+) are specific to a custom accelerator design, with GPU-only comparisons (4.1–28.8×) being the more broadly transferable figures. Taken together: "fewer active cells/FLOPs automatically means faster" is explicitly **not** supported by this literature as a general rule — it is conditional on matching representation to hardware, exactly as the SIH problem statement's own caution anticipates.
- **Net assessment:** H5 survives for *sparsity-based* computational representations, with strong, repeated, measured (not just theoretical) support, subject to the hardware-matching caveat above. For *map resolution* specifically (a persistent, spatially-varying-resolution structure), the evidence is thinner but positive where it exists (MrHash) — this project should not treat H5 as blanket-confirmed for "any adaptive map resolution scheme," but the disconfirming search explicitly failed to find any paper showing that adaptive/sparse *representations* are net-negative when properly hardware-matched; the one clear counter-case (FALO) is about raw sparsity on ill-suited hardware, not about a discredited *resolution-adaptivity* idea specifically.

### H6: "Existing adaptive LiDAR work mainly concerns sensing rather than map representation"
- **Verdict: Disproved, for the "adaptive LiDAR work" umbrella once broadened beyond distance-based map resolution — but with an important internal distinction the hypothesis's wording glosses over.**
- Across 23 distinct search queries and 19 papers examined in depth, spanning 2013–2025 (voxel hashing → OctNet → submanifold sparse conv → VoxelNet/SECOND/PointPillars → MinkowskiEngine → Focal-Conv/SPS-Conv → SPVNAS/Cylinder3D → SPADE/SD-Conv/FALO/LiDAR-PTQ → MrHash/Spira), **zero papers found in either assigned family concern adaptive *sensor acquisition* or scan-pattern changes.** Every single paper is about the computation- or representation-side of the pipeline: how point clouds are structured, stored, convolved, pruned, dilated, quantized, or hashed. This is a large, continuously active, top-venue (CVPR/NeurIPS/ICLR/TOG) research area spanning over a decade — the opposite of a minor sideline relative to sensing-side adaptivity.
- This directly weakens/disproves H6 **if "adaptive LiDAR work" is read broadly** (as the SIH problem statement's own "adaptive spatial representation" pillar suggests it should be) to include sparse-representation and adaptive-computation work, since that body of work is enormous and squarely representation/computation-focused, not sensing-focused.
- **However, a precise reading matters here, and this is exactly the sparsity-vs-adaptive-resolution distinction this assignment was designed to surface:** the great majority of this representation-side work (submanifold sparse conv, MinkowskiEngine, SECOND, SPS-Conv, SPVNAS, Spira, SPADE, SD-Conv, FALO, LiDAR-PTQ) is **adaptive computational representation** — sparsity/pruning/quantization applied per-inference to a transient feature tensor — **not** "map representation" in the sense of a *persistent*, spatially-varying-resolution *map* that H5/H6 (and the SIH problem) are really asking about. Only **OctNet** (occupancy-driven octree) and especially **MrHash** (variance-driven hash-voxel grid) are genuine persistent adaptive-*map*-resolution structures in this entire search, and OctNet's "map" is really a per-inference input representation for classification tasks, not a maintained/updated robot map either. **Cylinder3D** is a further edge case: it achieves a distance-correlated effective-resolution gradient as an incidental consequence of coordinate-system choice, not a deliberate adaptive-map mechanism.
- **Net assessment:** H6 as literally stated ("mainly concerns sensing") is **disproved** — this family shows an enormous amount of non-sensing, representation/computation-side adaptive work exists and is far from a minor exception. But the finer-grained truth this review surfaces is: even *within* that large non-sensing body of work, genuinely persistent **adaptive map resolution** (as opposed to adaptive computational representation on transient sparse tensors) is itself rare — essentially one directly-relevant example (MrHash) plus one partial precedent (OctNet) were found across the entire two-family search. So the corrected picture is roughly: "sensing-side adaptivity" vs. "computation/representation-side adaptivity" vs. "persistent map-resolution adaptivity" are three different populations of work, of very different sizes — the middle one is huge, the first was not encountered at all in this family, and the third is genuinely scarce (consistent with it being a real, still-open research gap rather than a solved or over-explored problem).

## Terminology/Concept Notes

- **Sparsity vs. adaptive resolution — the central distinction for this review.** "Sparse" (SECOND, submanifold sparse conv, MinkowskiEngine, SPADE, FSD, SPS-Conv, SPVNAS, Spira, LiDAR-PTQ) means: the underlying data is mostly empty, and compute/memory is restricted to occupied sites on an otherwise *fixed*-resolution grid. "Adaptive/variable resolution" (OctNet, MrHash) means: the *size of the discretization cell itself* varies spatially according to some criterion (occupancy, variance/uncertainty, distance, semantics). A method can be sparse without being resolution-adaptive (this describes almost every paper in this review), and in principle could be resolution-adaptive without being sparse (e.g., a dense but non-uniform grid) — though in practice the two are usually combined once a variable-resolution scheme is adopted, since coarse regions are naturally also sparse in cell count.
- **Where they blur:**
  - **Focal Sparse Conv / SPS-Conv / SD-Conv** sit between sparsity and resolution-adaptivity: they don't change the map's stored cell size, but they do change the network's *effective receptive field or effective compute density* per spatial region based on learned/heuristic importance — a kind of "adaptive resolution of attention/computation" without touching the underlying map/grid resolution. These are classified here as adaptive neural computation / adaptive attention-ROI, deliberately kept distinct from adaptive map resolution.
  - **Cylinder3D** shows that a *coordinate-system* choice (cylindrical vs. Cartesian binning) can produce a distance-correlated effective-resolution gradient "for free," without any explicit adaptive-resolution logic — an important reminder that "distance-based adaptive resolution" partially already exists implicitly in some non-Cartesian representations, and any novelty claim for an explicit distance-based adaptive grid should be checked against this precedent.
  - **OctNet** is adaptive in resolution but the driving criterion is pure geometric occupancy (is there any data here at all), not distance or semantics — it sits at the boundary between "sparsity" (occupancy-driven) and "true adaptive resolution" (its cell size does vary, which pure sparsity schemes' cell size does not).
- **FLOPs/compute reduction ≠ measured speedup.** SPVNAS's own numbers (7.6× compute reduction, 2.7× measured speedup) and the general FALO finding (sparse ops can be *slower* than dense ops on some hardware despite fewer FLOPs) are direct, paper-sourced cautions against equating a smaller/sparser representation with proportionally faster execution — precisely the caution the SIH project's CLAUDE.md already flags ("Do not assume that fewer map cells automatically means faster computation"), and this review found multiple independent, quantified confirmations of exactly that caution from within the sparse-3D-CNN literature itself.
- **Hardware-dependence of sparsity benefits.** The same broad technique (sparse convolution / pruning) is reported as giving 10×+ speedups on a custom accelerator (SPADE, SD-Conv) but *losing* to a dense re-engineered alternative on certain edge GPU/NPU targets (FALO). Any efficiency claim for a sparse or adaptive representation in this project should specify the target hardware, since the literature shows the benefit is not hardware-invariant.

## Papers Considered But Excluded

- **SparseLIF** (arXiv:2403.07284) — sparse LiDAR-camera fusion detector; excluded as primarily a multi-modal fusion contribution rather than a sparse-representation/computation contribution per se, and outside this group's assigned scope (fusion is covered elsewhere).
- **BEVDilation** (arXiv:2512.02972) — LiDAR-centric multi-modal fusion with a "Sparse Voxel Dilation Block"; excluded for the same fusion-focus reason, though its dilation-based densification of foreground sparse regions is conceptually adjacent to Focal/SD-Conv.
- **FSHNet** (arXiv:2506.03714) — fully sparse hybrid network; only a title/abstract-level hit, not independently verified in enough depth to include as a full entry given time constraints; noted here as a candidate for future deeper review.
- **NUC-Net** (arXiv:2505.24634) — non-uniform cylindrical partition network, an explicit follow-on to Cylinder3D; excluded from a full entry (redundant with Cylinder3D's coverage of the cylindrical-partition idea) but worth flagging as evidence that the Cylinder3D-style implicit-adaptive-resolution idea has an active, explicitly "non-uniform" follow-on line of work.
- **Sparse2Dense** (arXiv:2211.13067) — learns to densify sparse 3D features for detection; excluded as it is the inverse operation (densification) rather than an adaptive/sparse representation method itself, though relevant as a reminder that some pipelines deliberately reverse sparsity where it hurts accuracy.
- **3D Point Cloud Object Detection Method Based on Multi-Scale Dynamic Sparse Voxelization** (PMC10976182, 2024) — multi-scale sparse voxelization improving small-object detection on KITTI (~5% accuracy gain); excluded from a full entry because only a search-summary level of access was obtained and its "multi-scale" mechanism appears to be standard multi-resolution feature-pyramid fusion (common in 2D/3D detection) rather than a novel adaptive-representation contribution distinct from SPVNAS's similar (and better-verified) claims.
- **(AF)²-S3Net** (arXiv:2102.04530) — attentive feature fusion with adaptive feature selection for sparse semantic segmentation; excluded for depth/time reasons, flagged as a further example of "adaptive attention within a sparse backbone," reinforcing (not contradicting) the Focal-Conv/SPS-Conv categorization pattern already covered.
- **LiDAR-PTQ's OpenReview and an incorrectly-guessed arXiv ID (2312.10484)** — both dead-end fetches (bot-verification page; unrelated physics paper) documented in "Searches Conducted" for transparency; the correct arXiv ID (2401.15865) was found but only at abstract/summary depth.
