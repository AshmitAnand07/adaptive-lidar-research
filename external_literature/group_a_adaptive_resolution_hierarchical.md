# External Literature — Group A: Adaptive Resolution & Hierarchical Mapping

**Assigned families:** Adaptive/variable-resolution LiDAR mapping; multi-resolution spatial representations; hierarchical LiDAR maps; adaptive voxelization; multi-resolution BEV representations.
**Assigned hypotheses to stress-test:** H1, H5, H6 (see below).

---

## Searches Conducted

1. adaptive resolution LiDAR mapping robot 2024 2025
2. variable resolution occupancy grid mapping LiDAR
3. multi-resolution 2.5D elevation mapping robot navigation
4. hierarchical octree mapping LiDAR SLAM
5. adaptive voxelization point cloud 3D object detection
6. multi-resolution bird's eye view BEV representation LiDAR detection
7. foveated LiDAR perception saliency-aware scanning
8. distance-based adaptive resolution point cloud downsampling autonomous driving
9. coarse-to-fine sparse 3D detection point cloud efficient
10. level of detail terrain mapping robot LOD
11. uncertainty-aware adaptive resolution mapping robotics
12. quadtree occupancy grid mapping mobile robot classic
13. semantic-aware adaptive resolution mapping LiDAR
14. wavelet compression point cloud map robotics
15. multi-scale feature pyramid BEV 3D object detection autonomous driving 2024
16. adaptive grid resolution robot exploration frontier
17. sparse convolution octree neural network 3D perception efficient
18. multi-resolution voxel grid autonomous vehicle mapping memory reduction
19. "Building Variable Resolution Occupancy Maps" IROS 2013 (title/author lookup)
20. MAP-ADAPT arxiv real-time quality-adaptive semantic 3D maps
21. Langerwisch Wagner variable resolution occupancy quadtree abstract sensor error bound
22. "adaptive resolution" survey LiDAR sensing versus mapping representation review
23. adaptive resolution grid map does not improve computation overhead cost analysis
24. early-exit dynamic depth neural network point cloud LiDAR adaptive computation
25. hierarchical BEV pooling multi-resolution efficient 3D detection sparse
26. Yguel multi-resolution wavelet occupancy grid classic robotics
27. content-aware dynamic resolution neural network 3D object detection distance-adaptive
28. importance-aware point cloud sampling attention region of interest LiDAR robotics
29. multi-resolution occupancy grid map fixed uniform grid limitation robotics thesis
30. "sparse representation" LiDAR map robot efficient memory 2024
31. dynamic resolution LiDAR scanning adaptive robot terrain traversability
32. octree map overhead traversal cost versus uniform grid real-time performance comparison
33. "adaptive sensing" versus "adaptive mapping" LiDAR distinction robotics

Each substantive lead surfaced by these searches was followed with a direct WebFetch of the arXiv abstract/HTML page (preferred over raw PDF binary, which frequently failed to parse — noted per-paper below), publisher page, or project page, so that claims below are grounded in actual abstract/paper text rather than search snippets, except where explicitly flagged "snippet only."

---

## Papers

### D-Map: Occupancy Grid Mapping without Ray-Casting for High-Resolution LiDAR Sensors
- Authors: Yixi Cai, Fanze Kong, Yunfan Ren, Fangcheng Zhu, Jiarong Lin, Fu Zhang (HKU MaRS Lab)
- Year: 2023 (arXiv), accepted IEEE Transactions on Robotics (T-RO)
- Venue: IEEE T-RO
- Link/identifier: arXiv:2307.08493
- Access level: abstract read in full (verbatim), full PDF not text-extractable via tooling
- Problem: High-resolution LiDARs (>1M pts/sec) make traditional ray-casting occupancy mapping too slow.
- Representation: 3D, tree-based occupancy map (octree-family structure; exact tree type not stated in abstract).
- Resolution strategy: Variable/hierarchical — tree structure avoids "redundant visits to small cells." Driven by scene occupancy structure and depth-image projection, not explicitly by distance from robot.
- Adaptive mechanism categor(y/ies): Adaptive map resolution (persistent occupancy tree); secondarily adaptive computational representation (decremental "known-cell removal" shrinks map over time).
- Perception method: Classical/geometric — depth-image projection replaces ray-casting; theoretical accuracy/complexity analysis provided.
- Terrain handling: Not addressed (general occupancy, not terrain-specific).
- Dynamic-object handling: Not addressed in abstract; the "decremental" known-cell removal exploits LiDAR's low false-alarm rate, which is a static-world assumption and could be a liability under moving objects (INFERENCE).
- Temporal processing: Incremental per-scan updates.
- Uncertainty handling: Not stated in abstract.
- Computational characteristics: Abstract claims "superior efficiency... while maintaining comparable mapping accuracy and high memory efficiency," demonstrated on a handheld device and an aerial platform in real time — but no concrete FPS/ms/MB numbers appear in the abstract itself (DIRECT for qualitative claim, not reported for numbers).
- Datasets: "Various LiDAR sensors in both public and private datasets" (unnamed in abstract).
- Evaluation: Benchmark comparison against SOTA occupancy-mapping methods; two real-world deployments.
- Limitations: Not stated in the accessible text; open-sourced on GitHub for verification.
- Relevance to SIH problem: Directly relevant to the "adaptive spatial representation" pillar — demonstrates a persistent hierarchical map structure explicitly designed to reduce redundant updates for high-rate LiDAR, which is close to the SIH's core computational-efficiency motivation, though it does not by itself address terrain semantics or dynamic objects.
- Evidence level(s): DIRECT for representation/mechanism/qualitative efficiency claim (verbatim abstract); numeric performance NOT REPORTED in text accessible to this review (would require full-PDF read, which the fetch tool could not parse).

### ROG-Map: An Efficient Robocentric Occupancy Grid Map for Large-Scene and High-Resolution LiDAR-Based Motion Planning
- Authors: (HKUST-affiliated team; not fully resolved from abstract)
- Year: 2023
- Venue: arXiv preprint / robotics venue (ROS package release)
- Link/identifier: arXiv:2302.14819
- Access level: abstract read in full (verbatim)
- Problem: Integrating high-resolution LiDAR with occupancy grid maps (OGMs) for real-time quadrotor motion planning at large scale.
- Representation: 3D, "uniform grid-based OGM."
- Resolution strategy: **Explicitly fixed/uniform**, not spatially variable — the paper's own abstract states ROG-Map is "a uniform grid-based OGM." Efficiency instead comes from a robocentric local map that moves with the robot (bounding map extent), not from varying cell size. **Important correction:** an earlier automated pass over this paper mis-summarized it as distance-based variable resolution; the verbatim abstract shows this is incorrect — flagged explicitly per this project's evidence-labeling requirement.
- Adaptive mechanism categor(y/ies): None of the six categories strictly apply to resolution — this is a fixed-resolution, robocentric (spatially-bounded, not spatially-variable-resolution) map. Included here specifically as a **negative/contrast case**: it shows a recent (2023), competitive, real-flight-tested LiDAR OGM that deliberately chose uniform resolution over adaptive resolution.
- Perception method: Classical probabilistic occupancy grid with incremental obstacle inflation.
- Terrain handling: Not addressed.
- Dynamic-object handling: Not mentioned in abstract.
- Temporal processing: Incremental, per-frame map update at 50 Hz.
- Uncertainty handling: Standard probabilistic occupancy update (not detailed further in abstract).
- Computational characteristics (DIRECT, verbatim from abstract): "real-world flight tests with a 0.05 m resolution local map and 30m×30m×12m local map size, ROG-Map takes only 29.8% of frame time on average to update the map at a frame rate of 50 Hz (i.e., 5.96 ms in 20 ms), including 0.33% (i.e., 0.66 ms) to perform obstacle inflation."
- Datasets: "Various public datasets" (unnamed) plus real-world quadrotor flight tests.
- Evaluation: Outperforms SOTA baselines on public datasets; integrated into a full quadrotor system.
- Limitations: Not stated in abstract.
- Relevance to SIH problem: Important counter-evidence for the assumption that adaptive resolution is necessary — a SOTA, real-time, real-flight LiDAR OGM achieves strong performance with **uniform** resolution plus a robocentric (bounded, moving) window, suggesting that map *scoping* (local vs. global extent) is a distinct and independently effective efficiency lever from spatially varying resolution.
- Evidence level(s): DIRECT (verbatim abstract) for resolution strategy and reported numbers.

### Ada3D: Exploiting the Spatial Redundancy with Adaptive Inference for Efficient 3D Object Detection
- Authors: Tianchen Zhao et al. (Ada3D team — full author list not resolved from abstract alone)
- Year: 2023
- Venue: ICCV 2023
- Link/identifier: arXiv:2307.08209
- Access level: abstract read in full (verbatim)
- Problem: Voxel-based 3D detectors carry heavy compute/memory cost from redundant background points in LiDAR scans.
- Representation: 3D voxels and 2D BEV feature maps.
- Resolution strategy: Not a persistent-map resolution scheme — this is **per-frame, input-level adaptive filtering** guided by a learned importance predictor, plus "Sparsity Preserving Batch Normalization" for BEV features.
- Adaptive mechanism categor(y/ies): **Adaptive neural computation** (network processes a filtered/sparsified input) and **adaptive computational representation** (voxel/BEV sparsity level changes per input). NOT adaptive map resolution — there is no persistent map here.
- Perception method: Learned 3D object detection (voxel/BEV backbone).
- Terrain handling: Not addressed.
- Dynamic-object handling: Not addressed (generic 3D detection benchmark).
- Temporal processing: Single-frame (no persistent temporal map).
- Uncertainty handling: Not addressed.
- Computational characteristics (DIRECT, verbatim from abstract): "achieve 40% reduction for 3D voxels and decrease the density of 2D BEV feature maps from 100% to 20% without sacrificing accuracy. Ada3D reduces the model computational and memory cost by 5x, and achieves 1.52x/1.45x end-to-end GPU latency and 1.5x/4.5x GPU peak memory optimization for the 3D and 2D backbone respectively."
- Datasets: Not named in the accessible abstract (standard AD 3D detection benchmarks implied).
- Evaluation: Accuracy-preserving comparison against dense baseline at matched detection accuracy.
- Limitations: Abstract does not enumerate; operates purely at inference time, no persistent map maintained between frames (INFERENCE, from problem framing).
- Relevance to SIH problem: A clean example distinguishing *adaptive computation* from *adaptive map representation* — directly useful for classifying literature under the SIH's "adaptive spatial representation" pillar as something distinct from this kind of inference-time redundancy exploitation.
- Evidence level(s): DIRECT (verbatim abstract) for mechanism and all numeric claims.

### Hierarchical Adaptive Voxel-Guided Sampling for Real-Time Applications in Large-Scale Point Clouds
- Authors: Not fully resolved from abstract (published under this title on arXiv)
- Year: 2023
- Venue: arXiv preprint
- Link/identifier: arXiv:2305.14306
- Access level: abstract read in full (verbatim)
- Problem: Farthest Point Sampling (FPS) is accurate but too slow for real-time scene-level point cloud processing; random sampling is fast but hurts accuracy.
- Representation: Point cloud (pre-network sampling stage), not a persistent map.
- Resolution strategy: Hierarchical, voxel-guided sampling grid ensuring even point spacing — a per-frame sampling scheme, not a map resolution scheme.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** / **adaptive attention-ROI adjacent** (selects which points to keep for downstream processing). Not adaptive map resolution.
- Perception method: Feeds into point-based detection/segmentation networks (method-agnostic sampler).
- Terrain/Dynamic/Temporal/Uncertainty: Not addressed — this is a sampling-layer contribution, orthogonal to these concerns.
- Computational characteristics (DIRECT, verbatim from abstract): ">100× faster" than FPS at "competitive performance," and "20∼80% reduction in runtime" when integrated into existing models.
- Datasets: "Large-scale point cloud detection and segmentation" benchmarks (not named in abstract).
- Evaluation: Runtime and accuracy comparison vs. FPS and random sampling.
- Limitations: Abstract does not state; aggressive sampling in sparse regions could lose geometric detail (INFERENCE).
- Relevance to SIH problem: Relevant to distinguishing preprocessing-level "adaptive sampling" from true adaptive map representation — a common terminology conflation risk for this project (see Terminology Notes).
- Evidence level(s): DIRECT (verbatim abstract).

### AVS-Net: Point Sampling with Adaptive Voxel Size for 3D Scene Understanding
- Authors: Not fully resolved from abstract
- Year: 2024
- Venue: arXiv preprint
- Link/identifier: arXiv:2402.17521
- Access level: abstract read in full (verbatim)
- Problem: Existing downsampling methods either cost too much compute or lose fine geometric detail.
- Representation: Point cloud, voxel-centroid-based sampling.
- Resolution strategy: A "Voxel Adaptation Module" adaptively sets voxel size referenced to a target downsampling ratio — per-scene/per-frame adaptive, not a persistent map.
- Adaptive mechanism categor(y/ies): Adaptive computational representation (sampling-stage voxel size varies).
- Perception method: Learned network compatible with arbitrary voxel sizes; evaluated on 3D object detection and 3D semantic segmentation.
- Terrain/Dynamic/Temporal/Uncertainty: Not addressed.
- Computational characteristics: Abstract claims "better accuracy... with promising efficiency" vs. SOTA but does not give concrete numbers in the accessible text.
- Datasets (DIRECT, verbatim): Waymo (outdoor) and ScanNet (indoor).
- Evaluation: Accuracy comparison on detection/segmentation vs. SOTA downsampling methods.
- Limitations: Not stated in abstract.
- Relevance to SIH problem: Another adaptive-computational-representation example (not persistent map); useful negative case to keep separate from "adaptive map resolution."
- Evidence level(s): DIRECT (verbatim abstract).

### Efficient and Probabilistic Adaptive Voxel Mapping for Accurate Online LiDAR Odometry (VoxelMap)
- Authors: Chongjian Yuan, Wei Xu, Xiyuan Liu, Xiaoping Hong, Fu Zhang (HKU MaRS Lab)
- Year: 2021 (arXiv); published RA-L/ICRA-affiliated work
- Venue: IEEE Robotics and Automation Letters (RA-L)
- Link/identifier: arXiv:2109.07082
- Access level: abstract read in full (verbatim)
- Problem: Accurate, efficient online LiDAR odometry needs a map representation that supports fast, reliable scan registration.
- Representation: 3D voxel map, each voxel holding a plane (or edge) feature — a probabilistic geometric-primitive map, not raw occupancy.
- Resolution strategy: Explicitly **coarse-to-fine voxel mapping** ("we further analyze the need for coarse-to-fine voxel mapping"), organized via a hash table plus octrees for efficient build/update.
- Adaptive mechanism categor(y/ies): Adaptive map resolution (persistent, incrementally built/updated voxel map with hierarchical octree organization).
- Perception method: Classical/geometric — plane/edge feature extraction per voxel feeding an iterated extended Kalman filter (IEKF) for pose estimation (MAP formulation).
- Terrain handling: Not addressed directly (odometry-focused, not terrain classification).
- Dynamic-object handling: Not addressed in abstract.
- Temporal processing: Incremental map build/update per LiDAR scan, tightly coupled with odometry.
- Uncertainty handling: Probabilistic voxel representation with plane/edge fitting; used inside an IEKF (implies uncertainty propagation, DERIVED from "probabilistic representation" + "IEKF" framing).
- Computational characteristics: Abstract claims "high accuracy and efficiency... compared to other SOTA methods" on KITTI; no concrete FPS/ms numbers appear in the accessible abstract text.
- Datasets (DIRECT): KITTI (public); additional outdoor unstructured-environment tests with non-repetitive-scan LiDARs.
- Evaluation: Accuracy/efficiency comparison vs. SOTA LiDAR odometry methods.
- Limitations: Not stated in abstract; only tested on driving/outdoor-odometry-style scenes as described.
- Relevance to SIH problem: A widely cited (this is the well-known "VoxelMap" LIO backbone used across many later LIO systems, including several found in this search, e.g. FAST-LIVO-style pipelines) example of coarse-to-fine adaptive voxel resolution as a mainstream, effective technique in LiDAR-inertial mapping — strong evidence against the idea that adaptive map resolution is a fringe/unexplored idea.
- Evidence level(s): DIRECT (verbatim abstract) for representation/mechanism; exact driver of "coarse-to-fine" split (geometric planarity vs. distance) NOT fully specified in the abstract text accessible — INFERENCE that it is geometry/residual-driven rather than pure distance, given the paper's plane-fitting framing; would need full-text confirmation.

### Adaptive-LIO: Enhancing Robustness and Precision through Environmental Adaptation in LiDAR Inertial Odometry
- Authors: Not fully resolved from abstract (GitHub-released open-source system)
- Year: 2025
- Venue: arXiv preprint
- Link/identifier: arXiv:2503.05077
- Access level: abstract read in full (verbatim)
- Problem: Current LiDAR-inertial SLAM systems lack adaptability: point-cloud accuracy degrades with longer frame intervals, erroneous IMU data couples in during IMU saturation, and **localization accuracy decreases due to fixed-resolution maps during indoor-outdoor scene transitions.**
- Representation: 3D, multi-resolution voxel map.
- Resolution strategy (DIRECT, verbatim): "adjusts map resolution adaptively using multi-resolution voxel maps **based on the distance from the LiDAR center**."
- Adaptive mechanism categor(y/ies): Adaptive map resolution (persistent, distance-driven voxel map), plus adaptive sensing/state-estimation elements (adaptive segmentation, IMU-saturation/fault adaptation) — this paper spans multiple categories.
- Perception method: Classical/geometric LiDAR-inertial odometry (LIO) pipeline.
- Terrain handling: Not addressed directly.
- Dynamic-object handling: Not detailed in abstract (motion-modality adaptation targets IMU faults, not moving obstacles).
- Temporal processing: Incremental LIO with adaptive segmentation for map updates.
- Uncertainty handling: Not detailed in abstract beyond IMU saturation/fault detection.
- Computational characteristics: Not reported numerically in the abstract.
- Datasets: Not named in abstract; "tested in various challenging scenarios."
- Evaluation: Qualitative claim of improved robustness/precision across scenario transitions; code open-sourced.
- Limitations: Not stated in abstract.
- Relevance to SIH problem: **This is the single strongest, most direct piece of evidence found against H1.** It is an explicit, 2025, distance-from-sensor-driven, multi-resolution voxel *map* (not just sensing) built specifically because a fixed-resolution map was found to *fail* during scene-scale transitions — directly on-point for the SIH's stated example of "fine near the robot, coarse far away," and shows this exact idea already implemented and evaluated, not merely proposed.
- Evidence level(s): DIRECT (verbatim abstract) for the central resolution-strategy claim.

### Adaptive Patched Grid Mapping
- Authors: Not fully resolved from abstract (automotive-perception-oriented team)
- Year: 2023
- Venue: arXiv preprint / automotive perception venue
- Link/identifier: arXiv:2308.03416
- Access level: abstract read in full (verbatim)
- Problem: Standard grid maps waste memory when environment information is unevenly/sporadically available across an autonomous vehicle's surroundings.
- Representation: Multi-layer 2D/2.5D grid map ("Adaptive Patched Grid Map"), with different information types (layers) held at independently variable resolutions.
- Resolution strategy: Layer-wise dynamically changing cell sizes, reconciled via a novel "spatial cell fusion" approach that resamples layers to cope with mismatched resolutions across layers; adaptation also responds to **external, dynamically changing requirements** (e.g., a stated "cell resolution specification" or planning "horizon target"), not purely to sensor geometry.
- Adaptive mechanism categor(y/ies): Adaptive map resolution (persistent, multi-layer grid).
- Perception method: Sensor/data fusion framework (not a learned detector); classical grid fusion.
- Terrain handling: Not explicitly stated but plausible given "unstructured environment" framing (INFERENCE).
- Dynamic-object handling: Not detailed; layered separation of information types could support it but this is not demonstrated in the abstract (INFERENCE, low confidence).
- Temporal processing: Continuous fusion across driving scenarios; layers must be "resampled during the fusion process to cope with dynamically changing cell sizes."
- Uncertainty handling: Not addressed in abstract.
- Computational characteristics (DIRECT, verbatim): evaluated with "real-world data... recorded from an autonomous vehicle driving through various traffic situations," comparing "memory efficiency... to other approaches" and measuring "fusion execution times"; abstract states results "confirm... a significant memory usage reduction" but does not give the specific percentage/figure in the accessible text.
- Datasets: Proprietary real-world AV driving recordings (not a public benchmark name).
- Evaluation: Memory-efficiency and execution-time comparison against unspecified baseline approaches.
- Limitations: Not explicitly stated in abstract.
- Relevance to SIH problem: Directly on-point for the "adaptive spatial representation" pillar in an automotive context — demonstrates that request-driven (not just distance-driven) adaptive resolution is also an active idea, i.e., resolution can be driven by downstream task/planning-horizon needs rather than only sensor geometry.
- Evidence level(s): DIRECT (verbatim abstract) for mechanism and qualitative memory claim; exact quantitative savings NOT REPORTED in accessible text.

### A-OctoMap: An Adaptive OctoMap for Online Path Planning
- Authors: Not fully resolved from abstract
- Year: 2024
- Venue: arXiv preprint
- Link/identifier: arXiv:2406.13910
- Access level: abstract read in full (verbatim)
- Problem: Standard downsampling loses geometric information needed for path planning; fixed-resolution graph-search planners (e.g., JPS) struggle with obstacle detection accuracy in complex scenes.
- Representation: 3D, hierarchical octree ("adaptive OctoMap... utilizes a hierarchical data structure").
- Resolution strategy: Hierarchical/adaptive, explicitly designed to "preserve key geometric information during downsampling" while keeping a "more flexible representation for pathfinding within fixed-resolution maps." (Note: phrasing in the abstract is somewhat internally ambiguous about whether the underlying map stays fixed-resolution while only the *query/planning* structure is adaptive, or whether the map itself is variable-resolution — flagged as a genuine ambiguity, not resolved from the abstract alone.)
- Adaptive mechanism categor(y/ies): Adaptive map resolution (primary claim) with adaptive computational representation elements (downsampling stage).
- Perception method: Not a learned perception method — a classical mapping/planning data structure paper.
- Terrain/Dynamic/Temporal/Uncertainty: Not addressed.
- Computational characteristics: Abstract claims (DIRECT, verbatim) "significant improvements in reducing information loss, enhancing precision, and boosting the computational efficiency of map reconstruction compared to state-of-the-art methods," and for path planning, "increasing the success rate of pathfinding and reducing path lengths" — but no concrete numeric values are given in the accessible abstract.
- Datasets: "Simulations" only; no named public dataset or real-robot platform stated in abstract.
- Evaluation: Simulation-based comparison against SOTA octree/downsampling and against baseline JPS.
- Limitations: Abstract does not state; simulation-only validation (as far as the accessible abstract shows) is itself a notable limitation (DERIVED).
- Relevance to SIH problem: Reinforces that hierarchical/adaptive octree structures for LiDAR-derived maps remain an active 2024 research area specifically for the memory/precision trade-off central to the SIH's "adaptive spatial representation" pillar.
- Evidence level(s): DIRECT (verbatim abstract) for claims; quantitative results NOT REPORTED in accessible text; simulation-only status is DERIVED.

### Efficient Volumetric Mapping of Multi-Scale Environments Using Wavelet-Based Compression (wavemap)
- Authors: Victor Reijgwart et al. (ETH Zürich ASL — based on GitHub org "ethz-asl/wavemap")
- Year: 2023
- Venue: arXiv preprint (robotics venue)
- Link/identifier: arXiv:2306.01279
- Access level: abstract read in full (verbatim)
- Problem: Volumetric maps must scale with increasingly dense, precise sensor data (RGB-D and 3D LiDAR) without becoming computationally/memory prohibitive.
- Representation: Hierarchical volumetric occupancy map built via wavelet decomposition.
- Resolution strategy: Multi-resolution by construction — the paper frames the desired mapping properties "through the lens of multi-resolution analysis" and argues wavelets are "a natural foundation for hierarchical and multi-resolution volumetric mapping." Driver of resolution variation is the map's own multi-scale wavelet coefficient structure (information content), not distance from robot per se.
- Adaptive mechanism categor(y/ies): Adaptive map resolution (persistent, hierarchical volumetric map).
- Perception method: Classical/probabilistic occupancy mapping (not a learned perception network); supports "uncertainty-aware sensor models."
- Terrain handling: Not addressed specifically.
- Dynamic-object handling: Not addressed in abstract.
- Temporal processing: Incremental map updates (implied by "mapping system," not detailed further in abstract).
- Uncertainty handling (DIRECT, verbatim): "The efficiency of the system enables the use of uncertainty-aware sensor models, improving the quality of the maps" — i.e., uncertainty-aware sensing is *enabled by* the compute savings from wavelet multi-resolution, an interesting causal claim.
- Computational characteristics: Abstract states "mapping accuracy and runtime performance comparisons with state-of-the-art methods" were conducted but does not report concrete figures in the accessible text.
- Datasets: "Synthetic and real-world data," tested on both RGB-D and 3D LiDAR (sensor names/benchmarks not specified in abstract).
- Evaluation: Comparative accuracy/runtime vs. SOTA volumetric mapping methods.
- Limitations: Not stated in abstract; open-sourced (ethz-asl/wavemap) for verification.
- Relevance to SIH problem: A rigorous, principled (multi-resolution-analysis-grounded) example of adaptive map resolution directly targeting the memory/compute trade-off central to the SIH problem, and explicitly linking resolution adaptivity to enabling richer uncertainty modeling — relevant to the SIH's uncertainty and adaptive-representation concerns simultaneously.
- Evidence level(s): DIRECT (verbatim abstract) for mechanism and uncertainty-enablement claim; quantitative performance NOT REPORTED in accessible text.

### OctoMap: An Efficient Probabilistic 3D Mapping Framework Based on Octrees
- Authors: A. Hornung, K. M. Wurm, M. Bennewitz, C. Stachniss, W. Burgard
- Year: 2013
- Venue: Autonomous Robots (journal)
- Link/identifier: DOI 10.1007/s10514-012-9321-0; project page octomap.github.io
- Access level: project/documentation page read; original journal paper not independently re-fetched (WEB VERIFIED via project page + citation, not full-paper read — flagged reduced confidence for specifics beyond what the project page states)
- Problem: Provide a general-purpose, memory-efficient, probabilistic 3D occupancy map usable by planners at multiple levels of abstraction.
- Representation: 3D occupancy octree.
- Resolution strategy: Multi-resolution by tree depth — "a high-level planner [can] use a coarse map, while a local planner may operate using fine resolution" (DIRECT, project page). Critically, the resolution/compression driver is **occupancy homogeneity** (large uniformly-free or uniformly-unknown regions are merged into big leaf nodes), **not distance from the robot** — an important structural contrast with the distance-driven papers above.
- Adaptive mechanism categor(y/ies): Adaptive map resolution (the canonical, most widely used example in robotics).
- Perception method: Classical Bayesian occupancy update; sensor-agnostic (works with any range sensor, including LiDAR).
- Terrain handling: Not terrain-specific by design; general occupancy only.
- Dynamic-object handling: Supports remapping/re-observation via updatable probabilistic integration but has no explicit dynamic-object model (DERIVED from "updatable... accommodating sensor noise and dynamic environments" framing on project page — this is a fairly weak, generic claim, not a dedicated dynamic-object method).
- Temporal processing: Incremental Bayesian updates over time.
- Uncertainty handling: Native probabilistic occupancy (log-odds) representation.
- Computational characteristics: Project page claims efficient memory use ("both in memory and on disk") and supports lossy/lossless compression for bandwidth-constrained multi-robot map sharing; no specific runtime/memory numbers were retrieved from the accessible project page text (would require the original 2013 journal paper for numbers).
- Datasets: Not specified on project page (original paper uses multiple robot platforms per broader literature knowledge — not independently verified here).
- Evaluation: Not detailed on project page.
- Limitations: Not detailed on project page; separately, external search results (see H5 discussion below) indicate octree map operations have O(log n) complexity vs. O(1) for uniform grids, i.e., a per-access computational cost that a pure "map size" story omits.
- Relevance to SIH problem: The most important **classic, foundational** touchstone for the entire "adaptive map resolution" family — establishes that hierarchical/multi-resolution 3D occupancy mapping has been mainstream, citable, and widely deployed since at least 2013, which is directly relevant to assessing whether adaptive/hierarchical mapping generally (not only distance-driven variants) is "unexplored."
- Evidence level(s): WEB VERIFIED (project page) for representation/mechanism; DIRECT quotation from project page; original journal-paper numeric results NOT independently retrieved in this pass — reduced confidence flagged.

### Building Variable Resolution Occupancy Maps Assuming Unknown But Bounded Sensor Errors
- Authors: Marco Langerwisch, Bernardo Wagner (Leibniz Universität Hannover)
- Year: 2013
- Venue: IEEE/RSJ IROS 2013
- Link/identifier: IEEE Xplore (conference proceedings); PDF mirror at vigir.missouri.edu
- Access level: **snippet/search-result only** — direct PDF fetch failed (binary/compressed stream not parseable by the fetch tool), and the ResearchGate abstract page returned HTTP 403. Confidence lowered accordingly; claims below are DERIVED from search-engine synthesis of the abstract, not a direct read.
- Problem (DERIVED): Building occupancy maps with a quadtree that varies resolution, under an *unknown-but-bounded* (interval, non-probabilistic) sensor error model rather than a standard probabilistic error model.
- Representation: 2D quadtree occupancy map.
- Resolution strategy (DERIVED): Variable resolution via quadtree splitting; per search synthesis, "the majority of possible types of sensor errors can be covered much better by bounded error models than by probabilistic models," with "a novel inverse sensor model... incorporat[ing] measurement and pose uncertainty using interval analysis" driving cell subdivision — i.e., resolution appears driven by **sensor-uncertainty bounds**, not purely by distance (though sensor uncertainty typically correlates with range for laser rangefinders, so distance is an indirect factor — INFERENCE).
- Adaptive mechanism categor(y/ies): Adaptive map resolution.
- Perception method: Classical/geometric — interval-analysis-based inverse sensor model, laser rangefinder input.
- Terrain/Dynamic/Temporal: Not established from available snippets.
- Uncertainty handling: Central to the paper — explicit bounded-error (interval) uncertainty model rather than a Bayesian probabilistic one.
- Computational characteristics: Not established from available snippets.
- Datasets: Not established from available snippets.
- Evaluation: Not established from available snippets.
- Limitations: Not established from available snippets.
- Relevance to SIH problem: A **2013, laser-rangefinder-era, uncertainty-driven variable-resolution quadtree** — important lineage evidence that uncertainty-aware adaptive resolution (one of the six CLAUDE.md-flagged "important technical questions") is not a new idea, predating this project's Phase 1 observations by over a decade.
- Evidence level(s): DERIVED/low-confidence throughout (search-snippet synthesis only; direct fetch failed twice). Explicitly flagged per instructions as reduced-confidence.

### Building Variable Resolution Occupancy Grid Map from Stereoscopic System — A Quadtree Based Approach
- Authors: Not fully resolved (search snippet attributes to "Li, Ruichek" among others)
- Year: ~2013 (IEEE conference, exact year not independently confirmed)
- Venue: IEEE conference (IEEE Xplore document 6629556)
- Link/identifier: IEEE Xplore 6629556
- Access level: **snippet only** — not fetched directly; included for completeness because it repeatedly surfaced across multiple distinct queries.
- Problem (DERIVED from title/snippet): Building a variable-resolution occupancy grid from stereo-camera (not LiDAR) range data using a quadtree.
- Representation: 2D quadtree occupancy grid.
- Resolution strategy: Quadtree-based variable resolution (details of the driving variable not confirmed from snippet).
- Adaptive mechanism categor(y/ies): Adaptive map resolution.
- Note on sensor modality: This is a **stereo-vision**, not LiDAR, system — included only as lineage/terminology evidence that "variable-resolution occupancy quadtree" is a long-standing cross-modality concept, not evidence specific to LiDAR.
- Relevance to SIH problem: Low-to-moderate — same conceptual family as Langerwisch & Wagner above but different sensor; strengthens the general "this idea is old" case without being LiDAR-specific.
- Evidence level(s): Snippet only, low confidence — flagged explicitly, not used to support strong claims.

### MAP-ADAPT: Real-Time Quality-Adaptive Semantic 3D Maps
- Authors: Jianhao Zheng, Daniel Barath, Marc Pollefeys, Iro Armeni
- Year: 2024
- Venue: ECCV 2024
- Link/identifier: arXiv:2406.05849; project page map-adapt.github.io; code at github.com/GradientSpaces/MAP-ADAPT
- Access level: abstract partially read (verbatim opening sentence) plus WebSearch-synthesized detail; Springer publisher page blocked by an authentication redirect, so full text not retrieved — moderate confidence.
- Problem: Uniform-quality 3D semantic reconstruction wastes compute/storage in regions that don't need fine detail, but some regions (e.g., small/intricate objects relevant to manipulation) do need high resolution.
- Representation: 3D semantic reconstruction (implicit/mesh-adjacent, RGB-D-driven; single map with spatially varying quality/LOD regions).
- Resolution strategy: Variable, driven by **both semantic information and geometric complexity** — described (via search synthesis) as "the first adaptive semantic 3D mapping algorithm that generates directly a single map with regions of different quality based on both semantic information and geometric complexity," and additionally adaptive to **available compute** (can degrade quality on weaker hardware to hold frame rate).
- Adaptive mechanism categor(y/ies): Adaptive map resolution, explicitly **semantic-aware** (this is a directly relevant example for CLAUDE.md's "semantic-aware or uncertainty-aware adaptation" disconfirming-evidence question).
- Perception method: Learned semantic SLAM pipeline (pose + semantic estimation) feeding the adaptive reconstruction.
- Terrain handling: Not stated; general indoor semantic reconstruction (RGB-D), not automotive/robot terrain traversability.
- Dynamic-object handling: Not addressed in available text.
- Temporal processing: Real-time incremental reconstruction (implied by "real-time" framing).
- Uncertainty handling: Not addressed in available text.
- Computational characteristics: Claimed (via search synthesis, not verbatim) to "significantly reduce storage and computation requirements" vs. uniform high-quality mapping; no concrete numbers retrieved.
- Datasets: Not confirmed from accessible text (indoor RGB-D benchmarks implied by method).
- Evaluation: Not confirmed from accessible text.
- Limitations: Not confirmed from accessible text; sensor modality is RGB-D, not LiDAR, which limits direct transferability to the SIH's LiDAR-only framing (INFERENCE/caveat).
- Relevance to SIH problem: **Directly disproves the idea that only distance-driven adaptive resolution has been explored** — this is explicit semantic+geometry-driven adaptive map quality, published at a top vision venue (ECCV) in 2024, i.e., very recent and mainstream, though on RGB-D rather than LiDAR input.
- Evidence level(s): Mixed — DIRECT for the one verbatim sentence retrieved; remainder DERIVED from search-engine synthesis (moderate, not full-paper, confidence) because the publisher page was paywalled/redirected.

### Efficient Semantic-Aware TSDF Mapping with Adaptive Resolutions
- Authors: Weidong Wang, Yu Hu, Wei Xi, Danping Zou, Wenxian Yu
- Year: 2023
- Venue: 2023 3rd International Conference on Robotics, Automation and Artificial Intelligence (RAAI), pp. 39–45
- Link/identifier: DOI 10.1109/RAAI59955.2023.10601297
- Access level: PDF fetched but not text-extractable by tooling (binary/compressed stream) — metadata (title, authors, venue, DOI, page range) confirmed, but body content NOT independently read. Flagged low-to-moderate confidence for anything beyond metadata.
- Problem (DERIVED from title): Efficient 3D reconstruction for robots/MAVs using a Truncated Signed Distance Field (TSDF), where uniform-resolution TSDF voxelization is too costly.
- Representation: TSDF stored in a voxel grid.
- Resolution strategy (DERIVED from title, not confirmed from body): Semantic-segmentation-driven adaptive voxel resolution — finer voxels for semantically important/labeled regions, coarser elsewhere.
- Adaptive mechanism categor(y/ies): Adaptive map resolution, semantic-aware.
- Perception method: Object detection + semantic segmentation feeding the mapping pipeline; targets unmanned ground vehicles and MAVs.
- Terrain/Dynamic/Temporal/Uncertainty: Not confirmed — body text inaccessible.
- Computational characteristics: Not confirmed — body text inaccessible.
- Datasets: Not confirmed — body text inaccessible.
- Evaluation: Not confirmed — body text inaccessible.
- Limitations: Not confirmed — body text inaccessible.
- Relevance to SIH problem: A second, independent (different authors/venue from MAP-ADAPT) 2023 example of semantic-driven adaptive map resolution — corroborates that semantic-aware adaptive resolution is a recognized, multiply-independently-pursued idea, not a one-off. However, because only metadata (not body text) was verifiable here, this should be treated as a weaker corroborating data point pending full-text access.
- Evidence level(s): Metadata WEB VERIFIED (title/authors/venue/DOI confirmed via publisher-hosted PDF); all technical claims DERIVED-from-title/low-confidence, explicitly flagged.

### Communication-Aware Hierarchical Map Compression of Time-Varying Environments for Mobile Robots
- Authors: Not fully resolved from abstract
- Year: 2025
- Venue: arXiv preprint
- Link/identifier: arXiv:2504.10751
- Access level: abstract read in full (verbatim)
- Problem: Multi-robot systems need to compress and share dynamic probabilistic occupancy grids under bandwidth/memory constraints, without knowing the map's dynamics model in advance.
- Representation: Dynamic (time-varying) probabilistic occupancy grid.
- Resolution strategy (DIRECT, verbatim): "a multi-resolution hierarchical encoder that balances the quality of the compressed map (distortion) with its description size" — an explicit rate-distortion optimization over map resolution, not a fixed policy.
- Adaptive mechanism categor(y/ies): Adaptive map resolution, framed as a communication/storage-constrained compression problem.
- Perception method: Not a perception method per se — an information-theoretic map-compression framework layered on top of an existing occupancy grid.
- Terrain handling: Not addressed.
- Dynamic-object handling (DIRECT, verbatim): Explicitly demonstrated "on both static (i.e., non-time varying) and dynamic (time-varying) occupancy maps," and the method "does not require knowledge of the occupancy map dynamics" — a notable robustness property.
- Temporal processing: Central to the paper — "time-sequential compression of dynamic probabilistic occupancy grids."
- Uncertainty handling: Occupancy grids are inherently probabilistic; no additional uncertainty model described beyond that.
- Computational characteristics: Not reported numerically in the abstract.
- Datasets: Simulation-based evaluation (per abstract, "demonstrate... in simulation").
- Evaluation: Rate-distortion trade-off curves (implied by framing); not detailed numerically in abstract.
- Limitations: Not stated in abstract; simulation-only as far as the abstract shows (DERIVED).
- Relevance to SIH problem: Directly relevant to the SIH's "reducing computational and memory cost" goal, reframing adaptive map resolution as a principled rate-distortion trade-off — also one of very few papers here that explicitly targets **dynamic/time-varying** occupancy maps rather than assuming a static world.
- Evidence level(s): DIRECT (verbatim abstract).

### G-VOM: A GPU Accelerated Voxel Off-Road Mapping System
- Authors: Not fully resolved from abstract
- Year: 2021
- Venue: arXiv preprint (also presented at a robotics venue per common citation)
- Link/identifier: arXiv:2109.13176
- Access level: abstract read in full (verbatim)
- Problem: Off-road autonomous ground vehicles need real-time local 3D terrain mapping supporting obstacle and slope/roughness estimation.
- Representation: 3D voxel map via a "3D array lookup table data structure," GPU-accelerated.
- Resolution strategy: **Fixed resolution** (no variable-resolution mechanism described in the abstract) — included here as a **contrast/negative case** directly relevant to terrain analysis.
- Adaptive mechanism categor(y/ies): None of the six categories apply to resolution (fixed-resolution system); relevant instead as a terrain-analysis benchmark.
- Perception method: Classical/geometric voxel-based terrain analysis (hard/soft positive-obstacle detection, negative-obstacle detection, slope estimation, roughness estimation).
- Terrain handling (DIRECT, verbatim, core contribution): "hard and soft positive obstacle detection, negative obstacle detection, slope estimation, and roughness estimation" — directly addresses the SIH's "terrain analysis" pillar.
- Dynamic-object handling: Not addressed in abstract.
- Temporal processing: Online, real-time local mapping (10 Hz).
- Uncertainty handling: Not addressed in abstract.
- Computational characteristics (DIRECT, verbatim): tested on three real vehicles (Clearpath Warthog, Moose, Polaris Ranger) at "4.5 m/s in autonomous operation and 12 m/s in manual operation with a map update rate of 10 Hz."
- Datasets: Real-world field tests on the three named vehicle platforms; comparison against pre-recorded waypoints (not a public benchmark dataset).
- Evaluation: Field trial comparison against recorded waypoints; open-source ROS implementation.
- Limitations: Not detailed in abstract.
- Relevance to SIH problem: Strong terrain-analysis relevance (fixed-resolution but comprehensive terrain feature set: positive/negative obstacles, slope, roughness) — useful as a baseline showing that rich terrain analysis is achievable without any adaptive-resolution mechanism at all, which is a relevant data point when judging whether adaptive resolution is *necessary* vs. merely *helpful* for the terrain-analysis pillar specifically.
- Evidence level(s): DIRECT (verbatim abstract).

### HOTFormerLoc: Hierarchical Octree Transformer for Versatile LiDAR Place Recognition Across Ground and Aerial Views
- Authors: Griffiths et al. (CSIRO Robotics)
- Year: 2025
- Venue: CVPR 2025
- Link/identifier: arXiv:2503.08140
- Access level: abstract read via search synthesis (not independently WebFetched in full) — moderate confidence; core claims cross-corroborated across multiple independent search results (QUT ePrints, GitHub, CVPR open-access page), which raises confidence despite not doing a direct WebFetch read of the PDF text.
- Problem: Large-scale 3D place recognition must work across both ground-to-ground and ground-to-aerial LiDAR view pairs, in both urban and forest environments, where point density varies enormously (spinning LiDAR vs. aerial LiDAR).
- Representation: 3D, octree-organized point cloud processed by a transformer.
- Resolution strategy: Multi-scale by octree depth — "an octree-based structure... a multi-scale attention mechanism that captures spatial and semantic features across granularities," plus "cylindrical octree attention windows" specifically designed to handle the variable point density of spinning LiDAR.
- Adaptive mechanism categor(y/ies): Adaptive map resolution (octree map structure) combined with adaptive attention/ROI (multi-scale attention over octree levels, "relay tokens" for efficient global-local interaction).
- Perception method: Learned — hierarchical octree transformer producing a global descriptor for place recognition (not detection/segmentation).
- Terrain handling: Not addressed (place recognition, not terrain classification).
- Dynamic-object handling: Not addressed in accessible summary.
- Temporal processing: Not addressed (single-query place recognition, not persistent temporal mapping).
- Uncertainty handling: Not addressed in accessible summary.
- Computational characteristics: Not reported in accessible summary (would need full-paper read for FPS/latency/memory numbers).
- Datasets: Standard place-recognition benchmarks plus a new dataset introduced by the authors, **CS-Wild-Places** — a cross-source (aerial + ground LiDAR) dataset from four dense forest sites.
- Evaluation: Global-descriptor retrieval accuracy across ground-ground and ground-aerial query pairs (metric specifics not confirmed from accessible summary).
- Limitations: Not confirmed from accessible summary.
- Relevance to SIH problem: Shows octree-based, explicitly multi-scale/hierarchical LiDAR representations remain state-of-the-art (CVPR 2025) for handling *variable point density* across viewpoints — conceptually adjacent to the SIH's near/far resolution problem, though applied to place recognition rather than terrain/object mapping. Also notable for explicitly engineering around spinning-LiDAR's inherent density variation (cylindrical attention windows), which is directly relevant to the "effective vs. nominal spatial resolution" question flagged in this project's CLAUDE.md.
- Evidence level(s): Mostly WEB VERIFIED/DERIVED via cross-corroborated search synthesis, not a direct full-text read — moderate confidence, flagged.

### Adaptive Fovea for Scanning Depth Sensors
- Authors: Zaid Tasneem, Charuvahan Adhivarahan, Dingkang Wang, Huikai Xie, Karthik Dantu, Sanjeev J. Koppal
- Year: 2020
- Venue: The International Journal of Robotics Research (IJRR)
- Link/identifier: DOI 10.1177/0278364920920931
- Access level: abstract-level detail via search synthesis; full IJRR text not independently fetched — moderate confidence.
- Problem: Fixed-pattern scanning depth sensors waste angular resolution on uninformative regions; the paper asks whether a scanning sensor can *control* its own angular resolution to concentrate sampling where it matters.
- Representation: Raw depth-sensor scan pattern (not a map/representation in the mapping sense).
- Resolution strategy: The sensor's *angular sampling density* itself is adaptively varied over the field of view — "an artificial fovea" that is "adaptively varied to maximize an information theoretic measure," directly analogous to biological foveation.
- Adaptive mechanism categor(y/ies): **Adaptive sensor acquisition** (the physical/scan-pattern behavior of the sensor changes) — this is squarely a sensing-side paper, not a mapping-side paper, and is included specifically as the clearest available example for the H6 sensing-vs-mapping distinction.
- Perception method: Not a learned perception method; an information-theoretic scan-control policy.
- Terrain/Dynamic/Temporal/Uncertainty handling: Not addressed (sensor-control paper, pre-mapping stage).
- Computational characteristics: Not established from accessible summary.
- Datasets: Not established from accessible summary (hardware demonstration paper, per typical IJRR sensor papers — INFERENCE).
- Evaluation: Not established from accessible summary.
- Limitations: Not established from accessible summary.
- Relevance to SIH problem: Important negative/contrast case — this is genuinely **adaptive sensing**, not adaptive map representation, and CLAUDE.md explicitly requires distinguishing the two. Its existence (2020, IJRR, well-cited direction — the search also surfaced multiple 2024–2026 descendants: αLiDAR, AEOS active scanning, adaptive motorized LiDAR scanning with OSM priors) shows the sensing-side adaptive family is real and active, but structurally distinct from map-resolution adaptivity.
- Evidence level(s): DERIVED/moderate confidence from search-synthesized abstract; not independently full-text verified.

### 3D Point Cloud Object Detection Method Based on Multi-Scale Dynamic Sparse Voxelization
- Authors: Jiayu Wang, Ye Liu, Yongjian Zhu, Dong Wang, Yu Zhang
- Year: 2024
- Venue: Sensors (Basel), Vol. 24(6):1804
- Link/identifier: PMC10976182 (open access)
- Access level: full paper read (via PMC open-access mirror)
- Problem: Small, sparse objects (pedestrians, cyclists) are hard to detect in LiDAR point clouds because uniform voxelization wastes resources on empty voxels while under-resolving sparse small objects.
- Representation: Voxel → pseudo-image (BEV-style) pipeline.
- Resolution strategy: Multi-scale, **dynamic sparse voxelization** — processes only non-empty voxels via a windowed-attention "Dynamic Sparse Voxel (DSV) Transformer Block," combined with a multi-scale Feature Pyramid Network (FPN) aggregating features at (H/2,W/2), (H/4,W/4), (H/8,W/8).
- Adaptive mechanism categor(y/ies): Adaptive computational representation (sparse-only voxel processing) + adaptive neural computation (windowed transformer attention scoped to non-empty regions). Not a persistent map — this is single-frame detection.
- Perception method: Learned — transformer-based 3D object detector with SSD-style classification/regression head, focal loss + smooth L1.
- Terrain handling: Not addressed.
- Dynamic-object handling: Addresses detection of dynamic-object classes (pedestrian, cyclist) as a category, but does not track/model motion — this is single-frame detection, not tracking (DERIVED).
- Temporal processing: None (single-frame).
- Uncertainty handling: Not addressed.
- Computational characteristics (DIRECT, from full paper): **45 FPS**; training took ~15 hours on dual NVIDIA RTX 4090 GPUs, 80 epochs.
- Datasets (DIRECT): KITTI — 7,481 train/val samples, 7,581 test samples, Easy/Moderate/Hard difficulty splits.
- Evaluation (DIRECT): Average Precision (AP) in BEV and 3D, IoU thresholds 0.7 (car), 0.5 (pedestrian/cyclist); compared against PointPillars, VoxelNet, PointRCNN, SECOND. Reported gains over PointPillars: pedestrian BEV +5.87–7.55% mAP across difficulty levels, cyclist BEV +2.06–3.81%.
- Limitations (DIRECT, authors' own statement): generalization across diverse target types "needs validation," robustness under varying environmental conditions (lighting, weather) "requires investigation," and "allocation of computing resources across different hardware platforms remains ambiguous."
- Relevance to SIH problem: Concrete, fully-verified evidence that multi-scale/sparse voxelization measurably improves small/sparse dynamic-object detection (pedestrians, cyclists) — directly relevant to the SIH's "small and distant objects" and "dynamic objects" concerns, though it is a detection-time technique, not a persistent map-resolution technique.
- Evidence level(s): DIRECT throughout (full paper read via open-access mirror) — highest-confidence entry in this file.

### Improving LiDAR 3D Object Detection via Range-Based Point Cloud Density Optimization
- Authors: Not fully resolved from abstract
- Year: 2023
- Venue: arXiv preprint
- Link/identifier: arXiv:2306.05663
- Access level: abstract read in full (verbatim)
- Problem: LiDAR 3D detectors systematically perform worse on far-range points because near-sensor regions have much higher natural point density, creating a training-data density bias.
- Representation: Raw point cloud (pre-detector), not a map.
- Resolution strategy (DIRECT, verbatim): "a model-free point cloud density adjustment pre-processing mechanism that uses iterative MCMC optimization to estimate optimal parameters for altering the point density at different distance ranges" — this is **explicitly distance/range-driven density adaptation**, though applied to the *input point cloud for a detector*, not to a persistent map's cell resolution.
- Adaptive mechanism categor(y/ies): Adaptive computational representation (input density adjustment prior to a fixed-architecture detector). Explicitly NOT adaptive map resolution and NOT adaptive neural computation — the authors' stated framing (DIRECT, verbatim) is investigating the problem "from the data perspective instead of detector architecture design... without modifying the detector architecture."
- Perception method: Applied to four SOTA LiDAR 3D object detectors as a plug-in pre-processing step.
- Terrain/Dynamic/Temporal/Uncertainty: Not addressed.
- Computational characteristics: Not reported numerically in the abstract.
- Datasets (DIRECT): Waymo and ONCE.
- Evaluation: Detection-accuracy improvement across four detectors on two public datasets (specific numbers not in accessible abstract text).
- Limitations: Not stated in abstract.
- Relevance to SIH problem: **Directly and explicitly distance/range-driven** adaptive point-density manipulation for LiDAR — strong evidence that "distance-based adaptive resolution" (of the *point cloud*, if not the persistent *map*) is an active, multiply-validated (4 detectors, 2 datasets) 2023 research direction. Important nuance for H1: this shows distance-driven adaptation is well-explored at the *input/detection* level even where it's rarer at the *persistent map* level.
- Evidence level(s): DIRECT (verbatim abstract).

### A Survey of Spatial Memory Representations for Efficient Robot Navigation
- Authors: Ma. Madecheen S. Pangaliman, Steven S. Sison, Erwin P. Quilloy, Rowel O. Atienza (University of the Philippines Diliman)
- Year: 2026 (arXiv, dated April 2026 per arXiv ID)
- Venue: arXiv preprint (survey)
- Link/identifier: arXiv:2604.16482
- Access level: full HTML paper read via WebFetch
- Problem: Survey of how robots should represent spatial memory efficiently for navigation, spanning classical and learned/neural representations.
- Representation: Survey — covers multiple representation families (not a single method); notes level-of-detail (LOD) approaches such as GigaSLAM only tangentially.
- Resolution strategy: The survey does **not** treat adaptive/variable resolution as a first-class organizing axis; it mentions LOD "only tangentially," e.g., noting GigaSLAM "applies LOD [to reduce] active Gaussians; total map persists on disk," without deep analysis.
- Adaptive mechanism categor(y/ies): N/A (survey); implicitly touches adaptive map resolution and adaptive computational representation via the systems it surveys.
- Terrain/Dynamic/Temporal/Uncertainty: Not the survey's focus (navigation-memory representation focus).
- Computational characteristics: The survey explicitly does **not** report a rigorous overhead accounting — DIRECT finding (per this project's own fetch of the paper): it "does NOT thoroughly evaluate whether adaptive structures deliver net benefits after accounting for overhead... provides no comparative overhead factor... or concrete performance data showing whether this approach outperforms alternatives when runtime scaffolding is included."
- Datasets: N/A (survey).
- Evaluation: N/A (survey); qualitative synthesis of the field.
- Limitations (self-noted by the survey, DIRECT): treats hierarchical/streaming approaches as a promising future direction ("toward scalable solutions") rather than an already-resolved question.
- Uncertainty note on sensing-vs-mapping scope (DIRECT, verbatim): the survey **explicitly excludes** sensor-level adaptivity from its scope, stating "We exclude... perception without persistent memory," i.e., it deliberately focuses on the representation/map layer, not sensing.
- Relevance to SIH problem: **This is the single most important piece of evidence for H5.** A 2026 survey, specifically scoped to spatial-memory representations for robot navigation, explicitly finds that the literature it covers does *not* rigorously demonstrate net computational benefit for adaptive/hierarchical representations once overhead is accounted for. This directly substantiates the CLAUDE.md caution: "Do not assume that fewer map cells automatically means faster computation."
- Evidence level(s): DIRECT (full paper read by this reviewer's own tooling) for the overhead-accounting gap and scope-exclusion claims — high confidence, this is the strongest-sourced disconfirming-style finding in this file.

### SparseBEV: High-Performance Sparse 3D Object Detection from Multi-Camera Videos
- Authors: Not fully resolved from search snippet (camera-based, included for terminology/contrast only)
- Year: 2023
- Venue: ICCV 2023 (per common citation; not independently confirmed here)
- Link/identifier: arXiv:2308.09244
- Access level: snippet only — not independently fetched; included briefly for terminology completeness.
- Problem (DERIVED): Fully sparse 3D detection from multi-camera video, avoiding dense BEV grid construction.
- Representation: Sparse BEV queries (camera-based, not LiDAR).
- Resolution strategy: "Scale-adaptive self attention to aggregate features with adaptive receptive field in BEV space," plus adaptive spatio-temporal sampling and adaptive mixing.
- Adaptive mechanism categor(y/ies): Adaptive attention/ROI (query-level adaptive receptive field), not adaptive map resolution — no persistent map/grid is built at all (fully sparse, query-based).
- Computational characteristics (DIRECT, per snippet): "67.5 NDS on the nuScenes test split while maintaining real-time inference speed of 23.5 FPS."
- Relevance to SIH problem: Low-to-moderate — camera-based, not LiDAR, and explicitly *avoids* building a dense/adaptive BEV grid at all (the opposite direction from the SIH's map-representation focus). Included mainly as a terminology-precision example: "adaptive" in BEV detection literature very often means adaptive *attention over queries*, not adaptive *grid resolution*.
- Evidence level(s): Snippet only, low confidence, included for terminology contrast rather than as substantive technical evidence.

### DFPS: An Efficient Downsampling Algorithm for Global Feature Preservation of Large-Scale Point Cloud Data
- Authors: Not resolved (MDPI-hosted; publisher page blocked the fetch, HTTP 403)
- Year: 2025
- Venue: Sensors (MDPI), DOI 10.3390/s25144279
- Link/identifier: DOI 10.3390/s25144279
- Access level: **snippet only** — WebFetch blocked (403) on the publisher page; not independently read.
- Problem (DERIVED from snippet): Efficient downsampling of large-scale point clouds while preserving global geometric features.
- Representation: Point cloud.
- Resolution strategy (DERIVED from snippet): "Adaptive multi-level grid partitioning mechanism that dynamically adjusts computational intensity in accordance with terrain complexity, effectively balancing global feature retention with computational efficiency" — i.e., **terrain-complexity-driven** adaptive grid partitioning, distinct from both distance-driven and semantic-driven variants found elsewhere in this survey.
- Adaptive mechanism categor(y/ies): Adaptive computational representation (downsampling stage, not persistent map).
- Terrain handling: Central to the method's adaptation driver (terrain complexity), though this appears to mean local point-cloud geometric complexity generally, not necessarily robot-terrain-traversability semantics specifically (INFERENCE — ambiguous from snippet alone).
- Relevance to SIH problem: A third independent driver (after distance and semantics) for adaptive resolution/partitioning — terrain/geometric complexity — worth flagging even though access was blocked, since it directly matches the SIH's "terrain analysis" pillar by name.
- Evidence level(s): Snippet only, low confidence — flagged explicitly; full-text access blocked (403) despite two access attempts.

---

## Hypothesis Verdicts

### H1: "Distance-based adaptive resolution [in LiDAR mapping] is largely unexplored"
- **Verdict: Disproved.**
- Justification: Multiple independent, credible sources directly contradict this claim across a wide time span:
  - **Adaptive-LIO (2025, arXiv:2503.05077)** — DIRECT evidence, verbatim abstract: "adjusts map resolution adaptively using multi-resolution voxel maps based on the distance from the LiDAR center." This is exactly the SIH's "fine near the robot, coarse far away" idea, already implemented and evaluated in a persistent LIO map, not merely proposed.
  - **VoxelMap / "Efficient and Probabilistic Adaptive Voxel Mapping" (2021, arXiv:2109.07082)** — DIRECT evidence of coarse-to-fine voxel mapping as a mainstream LIO-backbone technique, widely reused in follow-on systems.
  - **Langerwisch & Wagner (IROS 2013)** and the related stereo quadtree paper (Li/Ruichek, ~2013) — DERIVED/low-confidence (snippet-only access) evidence that uncertainty/error-bound-driven (and, indirectly, range-correlated) variable-resolution quadtree mapping predates this project's Phase 1 by over a decade.
  - **Improving LiDAR 3D Object Detection via Range-based Point Cloud Density Optimization (2023, arXiv:2306.05663)** — DIRECT evidence of explicit distance/range-driven density adaptation, though at the point-cloud/detector-input level rather than the persistent-map level (an important nuance, not a full disproof-equivalent).
  - **Adaptive Patched Grid Mapping (2023)** additionally shows resolution driven by planning-horizon/requirement signals, broadening the "distance-based" family conceptually.
- Nuance: distance-driven adaptation is somewhat less common specifically as the *sole* driver of a *persistent map's* resolution (most persistent-map examples found — MAP-ADAPT, TSDF paper, wavemap, OctoMap — are driven primarily by semantics, geometric complexity, or occupancy homogeneity, not raw distance). But the claim as stated ("largely unexplored") is too strong and is directly falsified by Adaptive-LIO and VoxelMap at minimum.

### H5: "Adaptive map resolution can provide meaningful computational/memory benefits"
- **Verdict: Weakened (survived only partially, with a significant caveat).**
- Justification: **Memory benefits are well-evidenced** across multiple independent papers — Adaptive Patched Grid Mapping reports "significant memory usage reduction" (DIRECT, though unquantified in the accessible abstract); wavemap and OctoMap are both explicitly designed around memory efficiency via hierarchical/wavelet compression, with OctoMap's homogeneous-region merging being a decades-proven, widely deployed memory-reduction mechanism; Communication-aware Hierarchical Map Compression formalizes an explicit distortion-vs-size trade-off. This is DIRECT, multi-source evidence that memory benefits are real and repeatedly demonstrated.
  However, **rigorous, apples-to-apples *computational* (runtime/latency) benefit accounting — net of tree-traversal/management overhead — is largely absent** from what this review could verify:
  - The **2026 survey (Pangaliman et al., arXiv:2604.16482)**, read in full, explicitly states it found **no comparative overhead-factor measurement** in the literature it covers, and does not confirm that hierarchical approaches "outperform alternatives when runtime scaffolding is included" — DIRECT finding from a full-text read, the strongest single piece of evidence here.
  - Independent search synthesis on octree-vs-uniform-grid performance found that octree map operations are commonly cited as O(log n) per access versus O(1) for a uniform grid, with one aggregated source stating uniform grids are "typically several times faster than octree-based methods in map operations" — this is WEB VERIFIED only in the weak sense of being a search-engine synthesis across sources, not a single paper read in full, so it is flagged as lower-confidence, but it is a genuine, non-trivial disconfirming signal that should not be discarded.
  - None of the individual adaptive-map papers surveyed here (D-Map, Adaptive-LIO, A-OctoMap, Adaptive Patched Grid Mapping, wavemap) reported concrete, isolated compute/latency numbers in their abstracts that this review could independently verify — several abstracts make qualitative efficiency claims ("superior efficiency," "boosting computational efficiency") without accompanying figures accessible to this review.
- Conclusion: H5 should be treated as **directionally true for memory, unproven-with-rigor for compute** — this project's own CLAUDE.md caution ("Do not assume that fewer map cells automatically means faster computation") is corroborated, not refuted, by what this search found.

### H6: "Existing adaptive LiDAR work mainly concerns sensing rather than map representation"
- **Verdict: Disproved.**
- Justification: This review found substantially more, and longer-established, adaptive **map-representation** work than adaptive **sensing** work for LiDAR specifically:
  - Map-representation-side: D-Map (2023), Adaptive-LIO (2025), VoxelMap (2021), Adaptive Patched Grid Mapping (2023), A-OctoMap (2024), wavemap (2023), OctoMap (2013), MAP-ADAPT (2024), the TSDF adaptive-resolution paper (2023), Communication-aware Hierarchical Map Compression (2025), Langerwisch & Wagner (2013), HOTFormerLoc's octree map structure (2025) — a dense, continuous lineage from 2013 through 2025.
  - Sensing-side: Adaptive fovea (Tasneem et al., 2020) and its descendants (αLiDAR, AEOS active scanning, adaptive motorized LiDAR scanning with OSM priors, all 2024–2025) — a real and active family, but smaller in this sample and more recent in its LiDAR-specific instantiations (the 2020 fovea paper itself is a general scanning-depth-sensor paper, not LiDAR-specific).
- The map-representation family is not only larger in this sample but demonstrably older (OctoMap 2013, Langerwisch & Wagner 2013 predate the earliest sensing-side LiDAR-specific paper found here by roughly a decade). H6 as stated inverts the actual balance found in this search.

---

## Terminology/Concept Notes

- **"Adaptive" is heavily overloaded.** Within a single query cluster, "adaptive" was found to mean at least six structurally different things (matching the six mechanism categories in the brief): a physical scan pattern (Tasneem et al.), a network's compute graph (Ada3D), a per-frame sampling grid (AVS-Net, Hierarchical Adaptive Voxel-guided Sampling), a query-level attention receptive field (SparseBEV), and a persistent map's cell/voxel size (Adaptive-LIO, D-Map, OctoMap). Any literature claim using the bare word "adaptive" near "LiDAR" needs this disambiguation before it can be counted as evidence for or against a specific SIH-relevant hypothesis — several search-result snippets conflated these before the underlying abstract was checked.
- **"Coarse-to-fine" and "hierarchical" are used both for map structures (OctoMap, wavemap, VoxelMap) and for detection pipelines (POP-RCNN's Point Pyramid, multi-scale FPN in the dynamic-sparse-voxelization paper) — the same term does not imply the same underlying mechanism (persistent map vs. single-frame network feature pyramid).**
- **"Multi-resolution BEV" in the autonomous-driving detection literature (SA-BEV, GraphBEV, LST-BEV, SparseBEV, POP-RCNN) turned out to mean almost exclusively *multi-scale feature-pyramid fusion inside a detector network*, not a persistent, spatially-variable-resolution BEV *map*.** This is an important scope mismatch relative to the SIH problem's "adaptive spatial representation" pillar, which is about a persistent map/representation, not a per-frame detector feature pyramid. Group A's BEV family search did not surface a clear example of a persistent, spatially-variable-resolution BEV *map* (as opposed to a detector feature pyramid) — this may be a genuine gap, or may simply reflect the specific queries run (see "not found" note below).
- **ROG-Map correction:** an initial automated WebFetch summary (before the verbatim abstract was retrieved) mischaracterized ROG-Map as distance-based variable-resolution. Re-fetching the actual abstract text showed this was wrong — ROG-Map is explicitly uniform-resolution. This is flagged here as a caution about not trusting a single automated summarization pass, consistent with this phase's instruction to read actual text rather than rely on snippets/summaries alone.
- **Sensor-uncertainty-driven and range-driven resolution are correlated but distinct.** Langerwisch & Wagner's driver is explicitly *sensor error bounds*, which for a laser rangefinder happens to correlate with range, but the paper's own framing (per available snippets) is about uncertainty, not distance per se — worth keeping separate from the more literally distance-driven Adaptive-LIO.
- **"Not found in the literature I searched":** despite dedicated queries ("multi-resolution bird's eye view BEV representation LiDAR detection," "hierarchical BEV pooling multi-resolution efficient 3D detection sparse," "multi-scale feature pyramid BEV 3D object detection autonomous driving 2024"), this review did not find a clear example of a **persistent, spatially-variable-resolution BEV map** (as distinct from a per-frame detector feature pyramid) specifically for LiDAR. This is explicitly reported as "not found in the literature I searched," not as "does not exist" — the BEV-representation literature is enormous and this review's ~6 targeted BEV queries are not exhaustive of it.

---

## Papers Considered But Excluded

- **US patent documents** (surfaced repeatedly across searches): "Obstacle detection and vehicle navigation using resolution-adaptive fusion of point clouds" (US 11,592,820), "Multi-resolution top-down segmentation" (US 12,482,269 / 11,636,685), "Non-uniform occupancy grid manager" (US 11,625,009), "Variable level-of-detail map rendering" (US 9,672,656), "System and method for adaptive object-oriented sensor fusion for environmental mapping" (US 11,585,933), "Method and system for automatic real-time adaptive scanning with optical ranging systems" (US 11,249,192), "Systems and methods for implementing flexible, input-adaptive deep learning neural networks" (US 12,346,818), "Varying detection sensitivity between detections in LIDAR systems" (US 12,481,037). Excluded per instructions to prefer primary academic sources over patents; noted only as a weak corroborating signal that industry (not just academia) has independently converged on adaptive-resolution LiDAR/mapping concepts, reinforcing the H1/H6 disproof directionally without being counted as literature evidence.
- **Aggregator/explainer sites** used only to find leads, never as technical evidence: aimodels.fyi, emergentmind.com, themoonlight.io, GitHub README pages (used only to identify authors/venues, cross-checked against arXiv/publisher pages where possible).
- **MAP-ADAPT's Springer publisher page** — blocked by an authentication redirect (403/redirect-to-login); the arXiv version and search-engine synthesis were used instead, with reduced confidence flagged in that entry.
- **Efficient Semantic-Aware TSDF Mapping with Adaptive Resolutions** — publisher PDF fetched but body text was not extractable by the tool (binary/compressed stream); only metadata (title/authors/venue/DOI) could be confirmed. Flagged low-confidence for technical claims in its entry above.
- **Langerwisch & Wagner (IROS 2013) and the Li/Ruichek stereo quadtree paper** — both PDF/ResearchGate fetch attempts failed (unparseable binary stream; HTTP 403 respectively); relied on search-engine synthesis only, flagged low-confidence.
- **DFPS (Sensors 2025, DOI 10.3390/s25144279)** — MDPI publisher page returned HTTP 403 on fetch; only the search snippet could be used, flagged low-confidence.
- **Camera/monocular-only adaptive-resolution detection papers** (ZoomNet, DyRA, Depth-conditioned Dynamic Message Propagation, density-aware adaptive thresholding) — surfaced by the "content-aware dynamic resolution" query but excluded from full write-up as out-of-scope (RGB/monocular, not LiDAR); mentioned only in Terminology Notes where relevant.
- **SparseBEV** — included only briefly/at snippet level since it is camera-based (not LiDAR) and represents a different mechanism (adaptive attention over sparse queries, not adaptive grid resolution); kept mainly for terminology-precision purposes.
