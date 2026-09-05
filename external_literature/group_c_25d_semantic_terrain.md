# External Literature — Group C: 2.5D/Elevation Mapping, Semantic Mapping, Terrain/Traversability

**Assigned families:** 2.5D and elevation mapping; semantic elevation maps; semantic LiDAR mapping; terrain/traversability mapping.
**Assigned hypotheses to stress-test:** H3, H4.

---

## Searches Conducted

1. semantic elevation mapping robot 2024 2025 traversability
2. variable resolution elevation map semantic robot LiDAR
3. multi-resolution elevation mapping quadtree robot navigation
4. semantic LiDAR mapping autonomous driving 2024 2025 survey
5. traversability estimation LiDAR off-road terrain classification 2024
6. Fankhauser robot-centric elevation mapping
7. semantic octree mapping variable resolution robot exploration
8. hierarchical semantic terrain map multi-resolution off-road autonomous
9. semantic occupancy grid map autonomous driving BEV segmentation fixed grid resolution
10. geometric-semantic fusion mapping robot navigation costmap
11. "semantic" "multi-resolution" OR "variable resolution" elevation map traversability arxiv
12. elevation mapping cupy semantic layers GPU ETH robotic systems lab
13. quadtree semantic elevation map variable resolution navigation robot 2024 2025
14. probabilistic quadtrees variable resolution mapping large environments Einhorn OR Yguel classic
15. Wellington Stentz online adaptive rough terrain navigation vegetation classification classic
16. Bayesian traversability estimation survey classic mobile robot rough terrain
17. semantic OctoMap bandwidth compression multi-resolution class prioritization multi-robot
18. "Resolution-adaptive Quadtrees for Semantic Segmentation Mapping" UAV
19. Popovic Stachniss "Resolution-adaptive Quadtrees" semantic segmentation mapping UAV pdf
20. ipb.uni-bonn.de papercite quadtree semantic segmentation UAV pdf koval OR popovic 2022
21. Multi-Resolution Elevation Mapping Safe Landing Site Detection Planetary Rotorcraft resolution mechanism

In addition to these WebSearch queries, every paper judged important below was followed up with a direct WebFetch of its arXiv abstract page, ar5iv/HTML full text, IEEE Xplore page, publisher page, or institutional PDF, so claims are grounded in the actual paper text wherever "full paper read" or "abstract read in full" is marked. Several fetch attempts on paywalled or binary-PDF sources failed (IEEE Xplore 403, ResearchGate 403, raw PDF binary streams that could not be parsed as text) — these are explicitly flagged as reduced-confidence below rather than silently omitted.

Mandatory alternate-terminology coverage: multi-resolution (queries 2,3,9,11), hierarchical (7,8), level of detail (21 — "dynamic Level of Detail"), variable-resolution (2,3,14,18), dynamic resolution (implicit in 21), spatially adaptive / adaptive grid (13,14), coarse-to-fine (covered via octree pruning/expansion mechanism in queries 7,17), importance/content-aware resolution (17,18 — "class prioritization"), elevation map robotics / height map (1,2,3,6,12), digital elevation model robotics (21), traversability estimation (5,15,16), semantic terrain classification (8,15), semantic occupancy grid (9), BEV semantic segmentation (9), cost map navigation (10), geometric-semantic fusion mapping (10).

---

## Papers

### MEM: Multi-Modal Elevation Mapping for Robotics and Learning
- Authors: Gian Erni, Jonas Frey, Takahiro Miki, Matias Mattamala, Marco Hutter
- Year: 2023
- Venue: arXiv preprint (built on the ANYbotics/ETH `elevation_mapping_cupy` line of work)
- Link/identifier: arXiv:2309.16818
- Access level: full paper read (HTML)
- Problem: Extend classical geometry-only 2.5D elevation mapping to fuse multi-modal data (semantic class probabilities, RGB color, arbitrary high-dimensional learned features) into the same map, for robotics and downstream learning.
- Representation: **2.5D**, explicitly: "discretize the horizontal plane into cells, but store a continuous height value for each cell" (robot-centric grid).
- Resolution strategy: **Fixed/uniform.** Their own performance benchmark uses "a 10 m×10 m grid with a resolution of 4 cm resulting in a grid of 250×250 cells." No spatially variable resolution mechanism exists anywhere in the paper.
- Adaptive mechanism categor(y/ies): **None — fixed resolution, not adaptive.** This is an explicit, direct negative case: a 2023 paper that adds a full semantic layer to a 2.5D elevation map and does not couple that semantic information to resolution at all.
- Perception method: Learned semantic segmentation (Detectron2, Lite R-ASPP/MobileNetV3) feeding class probabilities into the map; fusion into the map itself is classical Bayesian (Dirichlet posterior update, closed form: α_{j,t} = α_{j,t-1} + Σm_i), plus alternative fusion modes (latest-value, exponential averaging, Gaussian Bayesian inference for continuous features).
- Terrain handling: A "traversability" layer is mentioned as a downstream plugin/consumer of the map but its classification methodology is not detailed in this paper (deferred to prior work).
- Dynamic-object handling: Not addressed; processes instantaneous sensor data with no tracking.
- Temporal processing: Multiple fusion modes accumulate across frames (exponential averaging weights recent data more; Dirichlet/Bayesian modes accumulate posteriors over time).
- Uncertainty handling: Gaussian Bayesian inference maintains explicit per-cell variance for continuous features; Dirichlet fusion yields class probability distributions (a genuine uncertainty measure); the paper explicitly notes exponential averaging is *not* probabilistic ("the information stored cannot be regarded as a probability measure").
- Computational characteristics (DIRECT, verbatim/paraphrased from paper): RTX 4090 — 2.596±0.260 ms per update (≈385 Hz); Jetson Orin (embedded) — 23.635±2.754 ms (≈42 Hz), processing 230,400 points per cloud; ~1.6 MB additional memory for multi-modal layers on a 200×200 grid. Implemented in CuPy/CUDA.
- Datasets: No formal benchmark; three qualitative application demonstrations (outdoor colorization on ANYmal C; 2.5D semantic segmentation for human detection in agriculture; vineyard tree-line detection).
- Evaluation: Qualitative demonstrations plus quantitative runtime/memory microbenchmarks; no accuracy benchmark against a labeled ground truth.
- Limitations (paper-stated and inferable): Fixed grid resolution does not adapt to information density; applications are qualitative, not quantitatively benchmarked against alternative fusion baselines; extensibility relies on user-defined plugins rather than a standard toolkit.
- Relevance to SIH problem: Directly on-point for the "2.5D + semantic" half of H4 — shows this combination is already mature and open-sourced (ETH/ANYbotics lineage) — but confirms the map resolution itself is not adapted to anything, which is exactly the missing ingredient H4 asks about.
- Evidence level(s): DIRECT for representation, resolution, fusion algorithm, and all quoted numbers (full text read); INFERENCE for "no traversability methodology" (based on absence in this paper, deferred to a cited prior work not separately verified here).

### RoadRunner: Learning Traversability Estimation for Autonomous Off-road Driving
- Authors: Jonas Frey, Shehryar Khattak, Manthan Patel, Deegan Atha, Julian Nubert, Curtis Padgett, Marco Hutter, Patrick Spieler
- Year: 2024
- Venue: arXiv preprint (JPL/Caltech + ETH Zurich)
- Link/identifier: arXiv:2402.19341
- Access level: full paper read (HTML v2)
- Problem: Predict dense traversability cost and elevation directly from camera+LiDAR at low latency for high-speed off-road driving, replacing a slower multi-stage semantic-segmentation-based pipeline ("X-Racer").
- Representation: **2.5D** — a gravity-aligned grid map storing both continuous elevation and continuous traversability cost per cell; underlying 3D occupancy voxelization at 20 cm isotropic resolution is used only as an intermediate LiDAR representation, not the output map.
- Resolution strategy: **Fixed**, uniform 20 cm over a 100 m × 100 m map. No spatial variation.
- Adaptive mechanism categor(y/ies): **None — fixed resolution, not adaptive.**
- Perception method: End-to-end learned network (EfficientNet-B0 image encoder + Lift-Splat-Shoot-style camera-to-BEV lifting, fused with a LiDAR voxel-map branch), trained **self-supervised** on hindsight-derived labels. Notably, the baseline it replaces (X-Racer) *does* use an explicit semantic segmentation model (SegFormer, classes: trail/ground/vegetation/rock/sky) to build training labels, but RoadRunner's own runtime network is explicitly trained "in contrast to existing methods" **without** using semantic classes at inference — semantics are only in the label-generation pipeline, not the deployed model.
- Terrain handling: Continuous traversability cost via Conditional Value at Risk (CVaR) framing (0 = safe, 1 = unsafe) plus continuous elevation; not a discrete drivable/non-drivable classifier.
- Dynamic-object handling: Explicitly **not** correctly handled — paper states dynamic obstacles "are not correctly handled in the ground truth generation pipeline."
- Temporal processing: Minimal — previous elevation estimate is transformed into the new robot frame and used as a prior, but no recurrent/temporal network memory.
- Uncertainty handling: **Not provided**; paper explicitly lists "a better understanding of the uncertainty of the prediction would be beneficial" as future work.
- Computational characteristics (DIRECT): 131.85 ± 2.5 ms latency on a single RTX 3080 (24M parameters) vs. >500 ms for the multi-stage X-Racer baseline (~4× speedup).
- Datasets: Custom, 16.5 km of off-road driving at Halter Ranch, Paso Robles, CA (21,158 samples, 80/20 split, held-out test location).
- Evaluation: Traversability — MSE, weighted MSE, precision/recall/F1 for hazard detection; Elevation — MAE, weighted MAE. Reports 52.3% improvement in traversability MSE and 36.0% improvement in elevation MAE vs. X-Racer.
- Limitations (paper-stated): small/single-region dataset limiting generalization; quality bounded by noisy hindsight labels; no temporal memory (cannot retain out-of-view hazards); no uncertainty quantification; frame-misalignment artifacts under rotation; no formal safety guarantees.
- Relevance to SIH problem: A strong, recent (2024), real-vehicle-tested example of fixed-resolution 2.5D terrain/traversability mapping that deliberately drops explicit semantic classification at runtime in favor of end-to-end self-supervision — useful counter-evidence that state-of-the-art off-road traversability systems do not necessarily need (or use) semantic-class labels at all, let alone couple them to resolution.
- Evidence level(s): DIRECT for representation, resolution, architecture, numbers, limitations (full text read).

### RoadRunner M&M: Learning Multi-range Multi-resolution Traversability Maps for Autonomous Off-road Navigation
- Authors: Manthan Patel, Jonas Frey, Deegan Atha, Patrick Spieler, Marco Hutter, Shehryar Khattak
- Year: 2024
- Venue: IEEE RA-L (submitted; arXiv preprint at time of writing)
- Link/identifier: arXiv:2409.10940
- Access level: full paper read (HTML)
- Problem: Extend RoadRunner to longer-range (100 m), multi-resolution traversability + elevation prediction so a high-speed off-road vehicle gets both fine near-field detail and coarse far-field awareness within a real-time budget.
- Representation: **2.5D** elevation + traversability grids, predicted at two concentric ranges.
- Resolution strategy: **Spatially variable, but purely distance/range-driven**, not content- or semantics-driven. Verbatim: the "micro range" map covers ±50 m at 0.2 m resolution and the "short range" [outer] map covers ±100 m at 0.8 m resolution — a fixed, pre-defined two-tier hierarchy keyed only to distance from the vehicle, decided at design time, not adapted online to scene content.
- Adaptive mechanism categor(y/ies): **Adaptive map resolution** (the persistent output map has two explicit, distance-keyed resolution tiers) — but the trigger is purely geometric distance, not semantics, uncertainty, or importance. This is important disconfirming context for H3/H4: a 2024 paper that *is* multi-resolution and 2.5D explicitly chose distance as the sole driver and did not use semantics anywhere in its own network (semantic segmentation, via Segmenter, appears only in the older X-Racer baseline used to generate training data, not in RoadRunner M&M's own model).
- Perception method: Learned, end-to-end: EfficientNet-B0 shared across 4 cameras + FPN for multi-scale image features; PointPillars-style backbone for the LiDAR voxel map; U-Net-style hierarchical decoder producing per-range traversability/elevation heads via 1×1 convolutions.
- Terrain handling: Continuous traversability + elevation, same CVaR-style framing as RoadRunner.
- Dynamic-object handling: Not addressed.
- Temporal processing: Single-frame at the network level; temporal aggregation happens only in the older X-Racer voxel-map pipeline used for supervision, not at inference.
- Uncertainty handling: Not included; paper again lists uncertainty estimation as future work.
- Computational characteristics (DIRECT): ~100 ms average inference latency, vs. >500 ms for the multi-step X-Racer stack.
- Datasets: Same custom 27 km off-road corpus (Halter Ranch, Paso Robles, CA); no public benchmark.
- Evaluation: Reports ~50% improvement in elevation mapping and ~30% in traversability estimation over the original RoadRunner, and prediction in 30% more of the scene than X-Racer.
- Limitations: No formal limitations section; paper acknowledges risk predictions are imperfectly localized and that image features contribute less than the LiDAR voxel map.
- Relevance to SIH problem: **Directly relevant, high-value counter-evidence.** It is essentially the closest published system to "2.5D + spatially variable resolution" for exactly the ground-vehicle terrain-perception problem the SIH describes — and it confirms the resolution driver used in practice is plain distance, with no semantic or uncertainty coupling. This both validates that distance-based 2.5D multi-resolution mapping is realistic/deployed (undercutting any claim that adaptive 2.5D mapping is impractical) and leaves the semantic-driven variant of the same idea empirically untested by its authors.
- Evidence level(s): DIRECT for representation, resolution mechanism, architecture, and all numbers (full text read). DERIVED: the inference that "resolution is not content-adaptive" follows from the explicit fixed-range/fixed-resolution description, not from an explicit disclaimer.

### Semantic OcTree Mapping and Shannon Mutual Information Computation for Robot Exploration (SSMI)
- Authors: Arash Asgharivaskasi, Nikolay Atanasov
- Year: 2021 (arXiv), revised 2023; also appears as "Active Bayesian Multi-class Mapping from Range and Semantic Segmentation Observations" (arXiv:2101.01831 is a closely related earlier version by the same authors)
- Venue: IEEE Transactions on Robotics (per IEEE Xplore listing) / arXiv preprint
- Link/identifier: arXiv:2112.04063
- Access level: full paper read (ar5iv HTML)
- Problem: Efficient, information-theoretically-guided autonomous exploration and mapping using an octree that stores a full categorical distribution over semantic classes per voxel, from range + semantic-segmentation observations.
- Representation: **Full 3D** octree (not 2.5D) — "8 octants of the Euclidean 3-D coordinate system"; the paper does project the most likely map onto a z=0 plane for 2D path planning, but the stored representation itself is volumetric, unrestricted in height.
- Resolution strategy: **Variable**, via classic octree pruning/expansion. Exact rule (DIRECT, verbatim): a node is pruned "if [it] has 8 children, its children do not have any children of their own, and its children all have equal multi-class log-odds"; conversely, "if the observation demands an update, the leaf node is recursively expanded to the smallest resolution." Crucially, **this pruning criterion is purely geometric/statistical homogeneity across sibling cells — not weighted by which semantic class is present.** All classes are treated identically for the purpose of deciding resolution.
- Adaptive mechanism categor(y/ies): **Adaptive map resolution** (persistent octree, occupancy/semantic-log-odds-driven pruning), but NOT semantic-class-weighted — this is an important nuance: an octree with per-voxel semantic labels is not automatically "semantic-aware adaptive resolution" in the sense of deliberately keeping some classes finer than others (contrast with Larsson et al. below).
- Perception method: Bayesian multi-class occupancy mapping; semantic input comes from an external semantic segmentation of range/visual observations (method for that segmentation not detailed in the excerpt obtained); exploration objective is a closed-form lower bound on Shannon mutual information between the map and future range-category measurements, using "semantic run-length encoding" of sensor rays for tractability.
- Terrain handling: Not addressed — this is a generic multi-class occupancy/exploration paper, not terrain-specific.
- Dynamic-object handling: Not addressed (static-world assumption implicit in occupancy mapping).
- Temporal processing: Standard incremental per-scan Bayesian updates; no explicit dynamic/temporal model.
- Uncertainty handling: Core to the method — each leaf holds a categorical (Dirichlet-style) distribution over classes; thresholding near-certain probabilities is used for compression, and the paper explicitly notes this "causes loss of information near p(m_i=k)=1" as a controllable trade-off.
- Computational characteristics: Paper reports (DIRECT, qualitative) that compressed leaf/partition count Q becomes "effectively independent of map resolution" while uncompressed cell count N grows linearly, i.e., a compression benefit that scales with resolution; also states memory of the semantic octree was compared against an uncompressed voxel grid, but exact ratios were not present in the retrieved excerpt (flagged reduced-confidence for exact numbers).
- Datasets: Procedurally generated and hand-designed 2D environments, a photorealistic Unity 3D simulation, a real-world ~6-acre outdoor forested area, and a real-world indoor office environment.
- Evaluation: Simulated and real-world exploration experiments; comparison of information-gain bound tightness and exploration efficiency against baseline exploration methods (e.g., frontier-based/TARE, referenced elsewhere in the paper).
- Limitations: Thresholding-induced information loss near-certain probabilities (explicit); mutual-information evaluation across many candidate trajectories is computationally heavier than purely local-trajectory methods like TARE, limiting exploration horizon in real time (DIRECT, paraphrased).
- Relevance to SIH problem: Establishes that semantic-labeled, variable-resolution 3D octree mapping is a well-established (2021-2023) technique for exploration — relevant lineage for the "adaptive map resolution + semantics" half of H3, though NOT 2.5D and NOT explicitly class-weighted, so it only partially engages H3/H4.
- Evidence level(s): DIRECT for pruning rule, representation, and uncertainty formulation (full text read); reduced confidence on exact compression/memory numbers (excerpt truncated before that data appeared in full).

### Information-Theoretic Abstraction of Semantic Octree Models for Integrated Perception and Planning
- Authors: Daniel T. Larsson, Arash Asgharivaskasi, Jaein Lim, Nikolay Atanasov, Panagiotis Tsiotras
- Year: 2022
- Venue: arXiv preprint (cs.RO), 2209.10035 — not confirmed published in a peer-reviewed venue at time of retrieval
- Link/identifier: arXiv:2209.10035
- Access level: full paper read (ar5iv HTML)
- Problem: Build and *compress* a semantic 3-D map so that only task-relevant semantic information is retained at fine resolution while irrelevant information is aggressively abstracted away, for combined perception-and-planning use.
- Representation: **Full 3D**, unbounded octree — explicitly "a three-dimensional (3-D) multi-resolution octree representation of 𝒲 ⊂ ℝ³," standard 8-children-per-node octree, not height-restricted/2.5D.
- Resolution strategy: **Variable, and explicitly semantic-class-weighted** — this is the single most important finding of this review for H3. The paper defines an objective (DIRECT, from the paper): maximize Σ β_i · I_{Y_i}(𝒯) − Σ γ_j · I_{Z_j}(𝒯) − α · I_X(𝒯), where Y_i are semantic classes the user has declared *relevant* (weight β_i), Z_j are classes declared *irrelevant* (weight γ_j), and the third term penalizes tree size for compression. Concretely: "allows robots to prioritize individual semantic classes when generating the compressed trees, so as to design multi-resolution representations that retain the relevant semantic information while simultaneously discarding unwanted semantic categories." A node is pruned when a computed one-step "reward" for keeping it expanded (based on Jensen-Shannon divergence of each class's conditional distribution across the node's children, weighted by β/γ) falls below zero.
- Adaptive mechanism categor(y/ies): **Adaptive map resolution**, explicitly and deliberately **semantic-class-driven** — this is direct prior art for the concept described in H3 ("semantic-aware adaptive resolution"), dated 2022.
- Perception method: FCHarDNet, pretrained on the RUGD off-road dataset, provides 24-class semantic segmentation of the input point cloud; each octree leaf stores a truncated distribution over the top-3 most likely classes plus one aggregate "other" bucket (an explicit approximation, not a full categorical distribution, to keep memory bounded).
- Terrain handling: **Not addressed as traversability** — classes are generic outdoor semantic categories (buildings, vegetation, roads, sky, etc.) used for planning-relevant abstraction, not a drivable/non-drivable or slope/roughness terrain analysis.
- Dynamic-object handling: Not addressed; static-environment assumption.
- Temporal processing: Minimal — incremental point-cloud-by-point-cloud tree updates, no explicit temporal/motion model.
- Uncertainty handling: Probabilistic — explicit statement: "our approach is probabilistic and incorporates the uncertainty in semantic classification inherent in real-world environments," via per-leaf categorical distributions over semantic class.
- Computational characteristics (DIRECT): In a path-planning application built on the compressed tree, the optimal path was found "about 10% faster on average," and planning-time standard deviation was reduced by 60% versus a Halton-sequence baseline graph. No explicit memory/compression-ratio percentage or wall-clock mapping runtime is reported in the retrieved text.
- Datasets: A single custom outdoor environment (asphalt/dirt/gravel roads, grass, trees, buildings, sky); the semantic classifier (FCHarDNet) was itself trained on RUGD. No standard 3D benchmark (e.g., SemanticKITTI) was used for evaluation.
- Evaluation: Per-class normalized information-retention plots, normalized leaf-node count vs. compression level, and planning-time statistics over 50 search instances; qualitative path visualizations.
- Limitations (paper-stated or directly inferable): the truncated per-leaf class distribution means true marginal probabilities for "relevant"/"irrelevant" class groups can't be recovered exactly from the tree and require a maximum-entropy assumption for missing children; the class-importance weights (β, γ, α) must be **manually specified**, with no automatic/learned tuning; evaluated in only a single outdoor environment, so generalization is untested; no real-time or dynamic-scene claims are made.
- Relevance to SIH problem: **Central to the H3 stress test.** This paper is direct, explicit, verified evidence that "semantic-aware adaptive [map] resolution" is not a novel idea — it was formalized and demonstrated (with a real information-theoretic objective, not just a hand-wavy heuristic) in 2022, three-plus years before this project. It does not, however, address 2.5D terrain representation, ground-vehicle traversability, dynamic objects, or real-time operation, so it does not by itself close the more specific H4 gap (2.5D + variable resolution + semantics, for terrain/dynamic-object perception).
- Evidence level(s): DIRECT for problem framing, objective function, pruning rule, semantic-segmentation source, uncertainty formulation, and reported numbers (full text read via ar5iv). INFERENCE: that the manual weight-tuning requirement and single-environment evaluation constitute practical limitations for deployment (not explicitly labeled "Limitations" by the authors, but directly supported by the paper's own stated assumptions).

### Distributed Optimization with Consensus Constraint for Multi-Robot Semantic Octree Mapping
- Authors: Arash Asgharivaskasi, Nikolay Atanasov
- Year: 2024
- Venue: arXiv preprint (cs.RO); no separate peer-reviewed venue confirmed from the accessible page
- Link/identifier: arXiv:2402.08867
- Access level: abstract read in full (verbatim); full PDF not retrieved
- Problem: Multi-robot 3D semantic mapping from streaming range + visual observations under single-hop-communication bandwidth constraints, building one consensus multi-class map across robots.
- Representation: **Full 3D** octree (continuation of the SSMI/Asgharivaskasi-Atanasov line above).
- Resolution strategy: **Variable**, explicitly termed "adaptive-resolution" in the abstract: "we utilize an octree data structure that compresses the multi-class map distribution using adaptive-resolution" specifically to reduce inter-robot communication volume.
- Adaptive mechanism categor(y/ies): **Adaptive map resolution**, driven by a distributed consensus/compression objective rather than by task-declared semantic importance (the abstract does not describe class-weighted prioritization the way Larsson et al. 2022 does — this looks closer to the generic homogeneity-based pruning of SSMI, extended to a distributed multi-robot consensus setting, though the exact pruning criterion could not be confirmed from the abstract alone).
- Perception method: Gradient-based optimization of per-robot observation log-likelihood under a map-consensus constraint; update rule described as resembling "Bayes rule with one-hop prior averaging."
- Terrain handling: Not addressed (generic multi-class mapping).
- Dynamic-object handling: Not addressed in the accessible abstract.
- Temporal processing: Streaming, incremental updates as robots move and communicate; no explicit dynamic-object temporal model described.
- Uncertainty handling: Implicit in the Bayesian/log-likelihood consensus formulation; not elaborated further in the abstract.
- Computational characteristics: **Not reported** in the accessible abstract (no bandwidth-reduction percentage, robot count, or runtime numbers were present in the text retrieved — flagged explicitly per this project's no-fabrication rule).
- Datasets: Not stated in the abstract.
- Evaluation: Not stated in the abstract.
- Limitations: Not stated in the abstract.
- Relevance to SIH problem: Further, more recent (2024) confirmation that "adaptive-resolution" semantic octree mapping is an active, continuing research line, reinforcing that this general idea is not unexplored — but again in a full-3D, multi-robot-communication context, not the SIH's single ground-vehicle 2.5D terrain-perception setting.
- Evidence level(s): DIRECT for the quoted abstract sentence (verbatim); everything else NOT REPORTED at the access level obtained (abstract only) — explicitly flagged low-confidence rather than inferred or fabricated.

### Adaptive Path Planning for UAVs for Multi-Resolution Semantic Segmentation
- Authors: Felix Stache, Jonas Westheider, Federico Magistri, Cyrill Stachniss, Marija Popović
- Year: 2021 (ECMR conference version), 2022 (arXiv / journal extension)
- Venue: European Conference on Mobile Robotics (ECMR) 2021, extended in Robotics and Autonomous Systems journal
- Link/identifier: arXiv:2203.01642
- Access level: full paper read (ar5iv HTML)
- Problem: Plan UAV flight paths that produce a semantic segmentation map with just enough resolution where it matters (e.g., precise crop/weed boundaries), while keeping overall flight time and image count low.
- Representation: **Flat 2D** map only — explicitly, "our problem setup considers a UAV surveying a flat field of known size" and "a UAV flying above a 2D terrain." **No elevation/height channel** — this is a semantic map, not an elevation map, and therefore does not itself satisfy the "2.5D" criterion of H4, even though it is a clean semantic + adaptive-resolution combination.
- Resolution strategy: **Spatially variable**, driven directly by detected semantic content. Mechanism (DIRECT, verbatim/paraphrased): for each segmented image, compute σ = (pixels belonging to the target class) / (total pixels); "we decide whether the current region contains enough semantic value for more detailed re-observation at a higher image resolution" — high σ triggers a lower-altitude (higher ground-sample-resolution) revisit of that region. A Gaussian Process regresses the relationship between altitude change Δh and resulting change in measured semantic ratio Δσ, to decide how much lower to fly.
- Adaptive mechanism categor(y/ies): This is best classified as **adaptive sensor acquisition** (the UAV physically changes flight altitude, changing the sensor's ground sample distance) that **produces** a map with **adaptive map resolution** as its output artifact (regions revisited at lower altitude end up represented at finer effective resolution in the accumulated segmentation map). It is explicitly and directly **semantic-content-driven**, unlike RoadRunner M&M's purely distance-driven scheme above.
- Perception method: Learned semantic segmentation, ERFNet (via the Bonnetal real-time-inference framework); classes are dataset-dependent — WeedMap: crop/weed(/soil); RIT-18: asphalt/beach/vegetation/water/building.
- Terrain handling: Not addressed — flat-field assumption explicitly stated; no slope/roughness/traversability analysis (this is agricultural/remote-sensing semantic mapping, not ground-vehicle terrain analysis).
- Dynamic-object handling: Not addressed; static scenes only.
- Temporal processing: Sequential waypoint/replanning decisions during a single mission; no explicit modeling of scene change over time.
- Uncertainty handling: Gaussian Process posterior variance over the altitude→accuracy relationship (σ*² = K(X*,X*) − K(X*,X)K(X,X)⁻¹K(X,X*)) provides a genuine uncertainty estimate, though the paper does not detail an explicit uncertainty threshold used for replanning decisions.
- Computational characteristics: No explicit planning-computation runtime is reported; only total mission execution time (flight + segmentation + planning) is compared between strategies.
- Datasets: Real-world only — WeedMap (5 RGB agricultural fields, crop/weed) and RIT-18 (multi-spectral aerial orthomosaics); no simulation.
- Evaluation: Mean Intersection-over-Union (mIoU) and mission execution time; reports that the adaptive strategy achieves better segmentation accuracy than fixed-altitude "lawnmower" coverage patterns while keeping execution time competitive, particularly "when the target class is not dominating the scene."
- Limitations (paper-stated or directly inferable): requires pre-labeled data from a separate field to initialize the Gaussian Process decision function; explicit flat-terrain assumption limits applicability to non-flat environments; the paper does not compare against other multi-resolution planning/mapping methods.
- Relevance to SIH problem: **Central to the H3 stress test alongside Larsson et al. (2022) above.** This is a second, independent (different research group, different domain — UAV agricultural remote sensing vs. ground-robot exploration) demonstration that resolution can be, and has been, driven directly by detected semantic content rather than by distance alone. It substantially weakens any claim that "semantic-aware adaptive resolution" is a novel/unexplored idea in the broader robotics-mapping literature. It does **not** resolve H4, because the representation here is flat 2D (no elevation), the domain is aerial crop mapping (not ground-vehicle terrain/dynamic-object perception), and there is no persistent multi-resolution *map data structure* per se — the "map" is the accumulated set of segmented images at whatever resolution they were captured.
- Evidence level(s): DIRECT for problem, resolution mechanism, network, uncertainty formulation, datasets, and evaluation approach (full text read via ar5iv). INFERENCE: classification of the mechanism as "adaptive sensor acquisition producing an adaptive-resolution map" is this reviewer's synthesis, not the paper's own terminology.

### Resolution-adaptive Quadtrees for Semantic Segmentation Mapping in UAV Applications
- Authors: Not fully confirmed from accessible sources — appears to be from the same Bonn PhenoRob/Stachniss-Popović research group as the Stache et al. path-planning paper above, based on shared subject matter and citation pattern (**unconfirmed** — flagged low-confidence)
- Year: 2022
- Venue: IEEE conference (per IEEE Xplore listing)
- Link/identifier: IEEE Xplore document 9843498
- Access level: **snippet only — flagged low-confidence.** IEEE Xplore returned HTTP 403 (paywalled) and ResearchGate also returned HTTP 403; all information below comes from WebSearch result snippets, not the paper itself.
- Problem (from snippets): UAV mapping using variable-resolution tree structures (octrees/quadtrees), addressing the specific problem that standard octree/quadtree implementations "insert values into the deepest level of the tree, regardless of the position of the UAV and the resulting image resolution" — i.e., naive trees don't account for the fact that a UAV's images have different real-world ground resolution at different altitudes.
- Representation: Likely 2D quadtree map of semantic segmentation (companion/mapping counterpart to the Stache et al. path-planning paper); not confirmed whether elevation is included (**not verified — snippet only**).
- Resolution strategy: Variable, explicitly "considers the resolution of the observations when calculating insertion indices" — i.e., resolution is tied to sensing ground-sample-distance, and by extension (via the companion path-planning paper) to detected semantic content driving altitude changes.
- Adaptive mechanism categor(y/ies): Adaptive map resolution (probabilistic quadtree/octree insertion keyed to observation resolution).
- Perception method, terrain handling, dynamic objects, temporal processing, uncertainty handling, computational characteristics, datasets, evaluation, limitations: **Not verifiable from available snippets — full text inaccessible.** Not reported here to avoid fabrication.
- Relevance to SIH problem: Likely the mapping-side companion to the Stache et al. (2022) semantic-driven adaptive-resolution UAV system above; included because its title alone is directly on-point for H3, but its specific technical claims must be treated as unverified until full text is obtained.
- Evidence level(s): **Snippet only, low confidence** for everything except the title and the one-sentence paraphrase of its stated problem (which itself is WEB VERIFIED only insofar as multiple independent search snippets agreed on the wording).

### Terrain-Aware Semantic Mapping for Cooperative Subterranean Exploration
- Authors: Michael J. Miles, Harel Biggie, Christoffer Heckman
- Year: 2023
- Venue: Frontiers in Robotics and AI
- Link/identifier: doi 10.3389/frobt.2023.1249586 (Team MARBLE, DARPA SubT Challenge)
- Access level: full paper read (via WebFetch of the published HTML)
- Problem: Bandwidth-constrained, multi-robot semantic grid mapping for subterranean exploration, encoding occupancy, traversability, and stairway presence in a form cheap enough to share across a robot fleet with limited communication.
- Representation: **3D** octree-based volumetric grid (each voxel = one octree node), pre-filtered to a uniform 5 cm point-cloud resolution before insertion.
- Resolution strategy: **Fixed base resolution (5 cm)**, with the octree providing hierarchical (but not semantically-driven) spatial compression above that base resolution. Not spatially variable by design intent — the 5 cm figure is a uniform pre-processing filter, and the octree's coarser levels exist for storage/communication compression, not for a deliberate near/far or semantic resolution policy.
- Adaptive mechanism categor(y/ies): Weak/incidental **adaptive computational representation** (octree compression for bandwidth) rather than a deliberate adaptive *map resolution* policy; essentially fixed-resolution semantics for practical purposes.
- Perception method: Classical/geometric — traversability from slope + surface curvature via least-squares plane fitting (weighted sum with slope penalty 20.0, curvature penalty 2.0); stairways detected via graph-based segmentation of tread/riser/rail regions. Occupancy, traversability, and stairway-presence are three **independently** computed layers, not a joint learned semantic segmentation network.
- Terrain handling: Explicit continuous traversability cost (0–1) from geometry, plus a specific binary stairway detector — a genuinely terrain-specific (not generic-object) semantic layer.
- Dynamic-object handling: Not addressed; static-terrain focus.
- Temporal processing: Exponential-moving-average fusion of new measurements, tuned to "incorporate new measurements more readily when the probability of occupancy is low."
- Uncertainty handling: Binary Bayes filter in log-odds form for both occupancy and stair probability, with bounded log-odds "to improve performance in dynamic environments" (a mitigation, not a full dynamic-object model).
- Computational characteristics (DIRECT): Compact per-voxel encoding — 2 bits occupancy + 4 bits traversability + 1 bit stair-presence = 7 bits/voxel, with differential map-sharing between robots to reduce transmission overhead; deployed on ClearPath Husky A200 (wheeled, AMD Threadripper 3990X + dual GTX 1650) and Boston Dynamics Spot (quadruped, AMD Ryzen 5800U).
- Datasets: DARPA SubT Simulator (Gazebo-based) and the physical DARPA SubT Final Challenge (Team MARBLE placed third).
- Evaluation: Field-deployed, multi-robot, real competition environment rather than an offline benchmark.
- Limitations (paper-stated): Difficulty observing/mapping descending stairways because the LiDAR's field of view doesn't cover the ground directly in front of a descending robot; inability to reliably detect thin obstacles (cables, fencing).
- Relevance to SIH problem: Good example of a real, field-proven, LiDAR-based 3D terrain-semantic map (occupancy + traversability + a structural class) built for exactly the kind of resource-constrained mobile-robot setting the SIH targets, but with fixed base resolution and no distance/semantic-driven resolution adaptation — reinforces that "fixed resolution" remains the norm even in recent (2023), competition-grade, terrain-semantic mapping systems.
- Evidence level(s): DIRECT for representation, resolution, algorithms, encoding, platform, and limitations (full text read).

### Watch Your STEPP: Semantic Traversability Estimation using Pose Projected Features
- Authors: Sebastian Ægidius et al. (UCL Robotics and Perception Lab)
- Year: 2025
- Venue: arXiv preprint
- Link/identifier: arXiv:2501.17594
- Access level: abstract/summary read (not full PDF text)
- Problem: Self-supervised traversability estimation for legged-robot navigation in unstructured natural terrain, learning "familiar vs. hazardous" terrain from the robot's own walking demonstrations.
- Representation: Dense, pixel-wise (image-space) feature embeddings rather than an explicit persistent grid/elevation map — resolution is that of the underlying image/feature map, not a separately defined world-frame grid.
- Resolution strategy: Effectively fixed (tied to sensor/image and feature-map resolution); no explicit spatially variable map-resolution mechanism described.
- Adaptive mechanism categor(y/ies): None described — fixed resolution, not adaptive, at least at the level of detail available from the abstract/summary.
- Perception method: Learned — DINOv2 vision-transformer features, with an encoder-decoder that reconstructs expected features for the terrain the robot has walked on; traversability signal comes from **reconstruction error** (self-supervised anomaly-style detection), not a supervised semantic class label.
- Terrain handling: Familiar/hazardous distinction derived implicitly from reconstruction error magnitude, not explicit terrain-class labels (e.g., not "grass" vs. "rock" but "seen-before" vs. "novel/risky").
- Dynamic-object handling: Not addressed in the accessible summary.
- Temporal processing: Not described; appears to be single-frame at inference.
- Uncertainty handling: Implicit, via reconstruction-error magnitude as a proxy for uncertainty/novelty.
- Computational characteristics: Not specified in the accessible content.
- Datasets: Real-world indoor and outdoor experiments on the ANYmal legged robot; no named public benchmark.
- Evaluation: Field demonstrations rather than a quantitative public-benchmark comparison (from the accessible summary).
- Limitations: Not explicitly stated in the accessible summary — flagged as reduced confidence since full text was not retrieved.
- Relevance to SIH problem: Useful contrast case showing a fully self-supervised, non-semantic-labeled approach to terrain traversability (foundation-model features + reconstruction error) as an alternative research direction to explicit semantic segmentation, relevant when comparing "semantic-aware" against "self-supervised/anomaly-based" traversability strategies.
- Evidence level(s): WEB VERIFIED / abstract-level only, explicitly lower confidence — full PDF was not parsed; numeric/architectural claims beyond what is stated above should not be assumed.

### Robot-Centric Elevation Mapping with Uncertainty Estimates (foundational/classic)
- Authors: Péter Fankhauser, Michael Bloesch, Christian Gehring, Marco Hutter, Roland Siegwart
- Year: 2014 (CLAWAR); extended as "Probabilistic Terrain Mapping for Mobile Robots with Uncertain Localization," IEEE RA-L, 2018
- Venue: International Conference on Climbing and Walking Robots (CLAWAR) 2014 / IEEE RA-L 2018
- Link/identifier: widely cited; open-source implementation at github.com/ANYbotics/elevation_mapping
- Access level: **snippet/secondary-source level** — information below is drawn from search-result summaries and the project's own documentation/README, not a full read of the original paper PDF; flagged accordingly.
- Problem: Build a terrain elevation map from onboard range sensing and (drifting) robot pose estimation, explicitly modeling and propagating pose and sensor uncertainty into the map, for legged-robot rough-terrain locomotion.
- Representation: **2.5D** — "represents the terrain as a regular grid, with the height of each cell updated ... through a Kalman filter" (per-cell scalar height + variance).
- Resolution strategy: **Fixed, uniform grid** — this is the foundational reference point establishing that fixed-resolution 2.5D elevation mapping with per-cell uncertainty is the classical/default approach against which any adaptive-resolution scheme should be compared.
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive. Foundational baseline.
- Perception method: Classical/probabilistic — per-cell Kalman filtering of height using range-sensor measurement uncertainty and full 6-DoF robot pose covariance; no learned semantic component in the original formulation.
- Terrain handling: General rough-terrain height/geometry only in the base method; no semantic classification (this came later via the MEM/`elevation_mapping_cupy` extensions covered above).
- Dynamic-object handling: Not addressed in the base formulation.
- Temporal processing: Incremental Kalman-filter updates per new sensor scan.
- Uncertainty handling: Central contribution — explicit per-cell variance derived from sensor noise and robot pose covariance, and explicit handling of robot pose drift (rather than assuming perfect localization).
- Computational characteristics: Not verified at this access level (not reported here to avoid fabrication).
- Datasets: Original evaluation on legged robots (StarlETH, later ANYmal) in laboratory rough-terrain settings (per widely-repeated secondary descriptions); not independently verified from primary text in this review.
- Evaluation: Not verified at this access level.
- Limitations: Not verified at this access level.
- Relevance to SIH problem: The canonical, foundational reference for "2.5D elevation mapping" as a representation choice — establishes that fixed-resolution, uncertainty-aware 2.5D elevation mapping is roughly a decade old (2014-2018) and forms the base layer that later semantic (MEM) and multi-resolution (RoadRunner M&M, planetary-rotorcraft) extensions build on. Important for lineage, not for adaptive resolution itself.
- Evidence level(s): **WEB VERIFIED (secondary sources) / snippet-level only** — flagged explicitly as reduced confidence; no primary-text quote is claimed here.

### Probabilistic Quadtrees for Variable-Resolution Mapping of Large Environments (foundational/classic)
- Authors: Gerhard K. Kraetzschmar, Gaurav P. Gassull, Kai Uhl
- Year: 2004
- Venue: 5th IFAC/EURON Symposium on Intelligent Autonomous Vehicles (2004); a related, more citable version appears as an IEEE conference paper "A probabilistic, variable-resolution and effective quadtree representation for mapping of large environments" (IEEE Xplore document 7251518)
- Link/identifier: IEEE Xplore 7251518; also academia.edu preprint
- Access level: **snippet only** — IEEE Xplore full text was not fetched in this review; claims below are from search-result summaries.
- Problem: Occupancy-grid mapping of large environments becomes memory-prohibitive at fine, uniform resolution (search snippet cites up to ~300 GB for detailed large-scale grids); need a variable-resolution alternative.
- Representation: **2D** probabilistic occupancy quadtree (not 2.5D/elevation, not semantic).
- Resolution strategy: **Variable**, via quadtree subdivision — finer cells only where occupancy detail is needed, coarse merged cells for large uniform (typically free) regions.
- Adaptive mechanism categor(y/ies): **Adaptive map resolution** — this is one of the foundational, classical (pre-2010) instances of the general "adaptive map resolution" concept for 2D occupancy grids, establishing that the core idea long predates any LiDAR-specific or learned-perception framing.
- Perception method: Classical probabilistic occupancy-grid mapping; no semantic component.
- Terrain handling: Not addressed (generic occupancy, not terrain-specific).
- Dynamic-object handling, temporal processing, uncertainty handling beyond standard occupancy probabilities: Not verifiable at this access level.
- Computational characteristics: Search snippets report "memory compression ratios of 10 to 50 times smaller than traditional [uniform] grids" — WEB VERIFIED only insofar as multiple snippets independently repeated this figure; not confirmed against primary text in this review.
- Datasets/Evaluation/Limitations: Not verifiable at this access level.
- Relevance to SIH problem: Establishes that "adaptive map resolution" for occupancy-style maps is a two-decade-old, well-established idea — directly useful for calibrating how much true novelty exists in any general "variable-resolution mapping" claim, independent of the semantic question that is this project's specific H3/H4 focus.
- Evidence level(s): **Snippet only, low confidence** for all quantitative claims; the general problem/representation/mechanism description is corroborated by multiple independent secondary sources (moderate confidence) but not primary-text verified.

### Online Adaptive Rough-Terrain Navigation in Vegetation (foundational/classic)
- Authors: Carl Wellington, Anthony (Tony) Stentz
- Year: 2004
- Venue: IEEE International Conference on Robotics and Automation (ICRA) 2004
- Link/identifier: CMU Robotics Institute publication (PDF fetch attempted but returned unparseable binary; information below is from WebSearch snippet only)
- Access level: **snippet only — flagged low-confidence**; PDF could not be parsed as text by available tooling.
- Problem: Vegetation hides the true load-bearing ground surface from range sensors, causing a rough-terrain-navigating vehicle to either misjudge obstacles or overestimate hazards; the paper proposes learning the true load-bearing surface online from experience.
- Representation: Grid-based terrain map (exact 2D vs. 2.5D not confirmed at this access level, though the "load-bearing surface height" framing strongly suggests an elevation-like, 2.5D-style representation — **INFERENCE**, not directly confirmed).
- Resolution strategy: Not confirmed at this access level (not reported to avoid fabrication).
- Adaptive mechanism categor(y/ies): Not classifiable with confidence at this access level; the "adaptive" in the title refers to *online learning of a sensor-to-ground-height mapping*, which is a form of adaptive perception/estimation, not necessarily adaptive map *resolution* — these should not be conflated (an explicit terminology note, since this project's brief warns against exactly this kind of confusion).
- Perception method: Classical — locally weighted learning (regression) mapping range-sensor features to predicted true ground height, trained online using the vehicle's own subsequent driving-over-the-terrain as ground truth feedback.
- Terrain handling: Distinguishes "load-bearing surface" (drivable) from vegetation/canopy above it — an early (2004), pre-deep-learning form of terrain/traversability-relevant classification, though binary/continuous height-correction rather than a multi-class "semantic" label set in the modern sense.
- Dynamic-object handling: Not addressed (this is a static-vegetation/terrain problem).
- Temporal processing: Explicitly online/incremental — the whole point of the method is that the model updates during operation as the vehicle gathers more experience.
- Uncertainty handling: Not confirmed at this access level.
- Computational characteristics: Not confirmed at this access level.
- Datasets/platform: Implemented and tested on an autonomous tractor in a farm setting (per search snippet), demonstrating obstacle-finding, improved roll prediction in vegetation, and adaptation to new vegetation conditions.
- Limitations: Not confirmed at this access level.
- Relevance to SIH problem: Historically important as one of the earliest (2004) examples of terrain-class-aware (vegetation vs. load-bearing ground) adaptive perception for off-road ground-vehicle navigation — good lineage evidence that "terrain-class-aware" reasoning about drivability predates modern deep-learning semantic segmentation by roughly two decades, even though it is not "semantic segmentation" in the modern multi-class-labeling sense.
- Evidence level(s): **Snippet only, low confidence** — PDF unreadable by available tooling; all claims above are HYPOTHESIS/INFERENCE-adjacent except where explicitly marked as coming from the search snippet.

### A Survey of Traversability Estimation for Mobile Robots
- Authors: Christos Sevastopoulos, Stasinos Konstantopoulos
- Year: 2022
- Venue: arXiv preprint (cs.RO); reported to also appear in IEEE Access per some secondary listings (not independently confirmed here)
- Link/identifier: arXiv:2204.10883
- Access level: abstract read in full (verbatim); full text not retrieved
- Problem: Survey the evolution of traversability-estimation methods for mobile robots, from early non-learned/classical approaches through modern deep learning.
- Representation: Survey — not applicable to a single representation; covers multiple representations across the surveyed literature (not detailed at abstract-only access level).
- Resolution strategy: Not addressed in the accessible abstract; the abstract text obtained does not discuss map resolution or multi-resolution mapping as a survey axis.
- Adaptive mechanism categor(y/ies): Not applicable (survey paper).
- Perception method: Explicitly organizes the field into "non-trainable and machine-learning methods," tracing the progression toward deep-learning-based traversability estimation and noting the recent shift toward self-supervised approaches.
- Terrain handling: Central topic of the survey — traversability defined as "the difficulty of driving through a specific region" based on physical terrain properties (slope, roughness, surface condition).
- Dynamic-object handling, temporal processing, uncertainty handling: Not detailed at the abstract-only access level obtained.
- Computational characteristics: Not addressed at this access level.
- Datasets: Survey covers multiple datasets across the surveyed literature; none individually confirmed here.
- Evaluation: N/A (survey).
- Limitations/gaps identified: The abstract explicitly frames deep learning as having "created an opportunity for radical improvement" while flagging "the increased need for large-scale datasets" and growing interest in self-supervised solutions as open challenges — but does not, at the accessible abstract level, identify "semantic-aware adaptive resolution" or "2.5D + variable resolution + semantics" as a named gap.
- Relevance to SIH problem: A useful, recent (2022) survey anchor for the state of the terrain-traversability field generally; notably, at the level accessible in this review, it does **not** surface adaptive/multi-resolution mapping as a live research axis at all — consistent with this review's broader finding that resolution strategy and traversability/semantic perception are usually treated as separate research questions in the literature, rather than jointly.
- Evidence level(s): DIRECT for the quoted abstract sentences; NOT REPORTED for anything requiring full-text access (explicitly flagged rather than inferred).

### Variable-Resolution Virtual Maps for Autonomous Exploration with Unmanned Surface Vehicles (USVs)
- Authors: Ye Li, Yewei Huang, Wenlong Gao (surname concatenation in source uncertain — rendered as "Wenlong GaoZhang" in the fetched metadata, likely two authors merged; **flagged low-confidence on exact author segmentation**), Alberto Quattrini Li, Brendan Englot, Yuanchang Liu
- Year: 2026 (arXiv submission dated March 2026)
- Venue: arXiv preprint (cs.RO)
- Link/identifier: arXiv:2603.22667
- Access level: abstract read in full (verbatim/paraphrased)
- Problem: Autonomous USV exploration of near-shore waters where GNSS is degraded, localization is uncertain, and computational resources are limited, making fixed-resolution mapping scale poorly.
- Representation: **2D** workspace discretized via an adaptive quadtree, with bivariate Gaussian "virtual landmarks" placed in cells (not 2.5D/elevation — a water-surface exploration/SLAM map, not a terrain height map).
- Resolution strategy: **Variable**, explicitly **uncertainty-driven, not semantic**: "adaptive quadtree enables an area-weighted uncertainty representation that keeps coarse, far-field virtual landmarks deliberately uncertain while allocating higher resolution to information-dense regions."
- Adaptive mechanism categor(y/ies): **Adaptive map resolution**, driven by localization/SLAM uncertainty and information density — a clean, recent (2026) example of the "uncertainty-aware adaptation" family named in this project's brief, offered here as a contrast case: uncertainty-driven ≠ semantic-driven adaptive resolution, and this paper is squarely the former, with **no semantic perception component at all**.
- Perception method: Factor-graph SLAM with a map-uncertainty criterion; an expectation-maximization-style planner balances exploration/exploitation.
- Terrain handling: Not applicable (water-surface navigation, not ground terrain).
- Dynamic-object handling: Not discussed in the accessible abstract.
- Temporal processing: Implicit in factor-graph SLAM's incremental structure; not elaborated as an explicit dynamic-temporal model.
- Uncertainty handling: Core mechanism — the entire resolution-allocation policy is driven by mapped uncertainty.
- Computational characteristics: Not reported in the accessible abstract.
- Datasets: VRX Gazebo simulator, marina-like near-shore environments of varying difficulty.
- Evaluation: Simulation-based; specific metrics not detailed at abstract-only access level.
- Limitations: Explicitly acknowledges a risk of overvaluing feature-sparse open-water regions, which could lead to SLAM failure; designed specifically for GNSS-degraded near-shore conditions rather than general-purpose use.
- Relevance to SIH problem: Useful negative/contrast case for H3 — confirms that "variable resolution driven by something other than distance" is an active 2026 research direction (uncertainty/information-density), but that when researchers do this, they generally still do **not** reach for semantics as the driving signal, reinforcing that a genuinely semantic-driven adaptive-resolution *map* (as opposed to sensor-acquisition-triggering, as in the UAV papers above) for ground/vehicle terrain perception remains rare-to-absent in the papers surveyed.
- Evidence level(s): DIRECT for the quoted mechanism sentence and representation (abstract read in full); NOT REPORTED for computational numbers and detailed evaluation (abstract-only access).

### Multi-Resolution Elevation Mapping and Safe Landing Site Detection with Applications to Planetary Rotorcraft
- Authors: Pascal Schoppmann, Pedro F. Proença, Jeff Delaune, Michael Pantic, Timo Hinzmann, Larry Matthies, Roland Siegwart, Roland Brockers
- Year: 2021
- Venue: IEEE/RSJ IROS 2021
- Link/identifier: arXiv:2111.06271
- Access level: abstract + search-summary level read (full PDF not parsed); moderate confidence.
- Problem: Detect safe landing sites on-board a size/weight/power-constrained planetary rotorcraft (e.g., Mars helicopter-class vehicle), from monocular Structure-from-Motion depth, without the compute/memory budget for a fine uniform-resolution map over a large area.
- Representation: **2.5D**, robot-centric elevation map, built incrementally from monocular-SfM depth + onboard visual-odometry poses.
- Resolution strategy: **Variable**, via a "dynamic Level of Detail" (LoD) mechanism explicitly driven by each depth measurement's own lateral surface resolution ("pixel-footprint") — measurements are fused into the map at whatever resolution their originating pixel actually supports, so near/well-observed terrain is finer and far/obliquely-viewed or sparsely-observed terrain is coarser, purely as a function of sensing geometry (distance, viewing angle, measurement density) — **not semantics**.
- Adaptive mechanism categor(y/ies): **Adaptive map resolution**, geometry/sensing-density-driven (a close relative of, but independent origin from, RoadRunner M&M's distance-tier approach — this one is continuous/measurement-driven rather than two discrete tiers).
- Perception method: Classical geometric — Structure-from-Motion from monocular images + visual odometry; no learned semantic segmentation component.
- Terrain handling: Landing-site safety scored from slope, roughness, and reconstructed-surface quality — geometric traversability/safety analysis, not semantic classification.
- Dynamic-object handling: Not addressed (static planetary-terrain assumption).
- Temporal processing: Incremental map aggregation from a sequence of monocular frames and associated VO poses.
- Uncertainty handling: A "probabilistic framework" is explicitly mentioned for fusing depth measurements of varying resolution, implying some form of per-measurement confidence weighting, though the precise formulation was not confirmed at this access level.
- Computational characteristics: Framed as "memory and computationally efficient" (qualitative, DIRECT) suited to a size/weight/power-constrained rotorcraft; no specific runtime/memory numbers were retrieved at this access level (not reported here to avoid fabrication).
- Datasets: Not confirmed at this access level.
- Evaluation: Not confirmed at this access level.
- Limitations: Not confirmed at this access level.
- Relevance to SIH problem: A clean, 2021, non-semantic example of exactly the "2.5D + variable resolution" pairing named in H4 — geometry/sensing-driven rather than distance-tier-driven (contrast with RoadRunner M&M) or semantic-driven (contrast with Larsson et al. / Stache et al.). Reinforces that the "2.5D + variable resolution" pair alone is well-established (at least since 2021, likely earlier in other domains), so the specific novelty question in H4 rests entirely on whether *semantics* is also folded in — which, per this review, it is not, in any 2.5D paper found.
- Evidence level(s): DIRECT for the quoted/paraphrased LoD mechanism and representation (from a combination of the arXiv abstract and consistent, multiply-corroborated search summaries); NOT REPORTED for detailed numbers, datasets, and limitations (full PDF not parsed — flagged reduced confidence).

---

## Hypothesis Verdicts

### H3: "Semantic-aware adaptive resolution may be an unexplored opportunity"
- **Verdict: Disproved, as a general claim — but only Weakened for the SIH's specific ground-vehicle/2.5D setting.**
- Justification: Direct, full-text-verified evidence shows semantic-class-driven adaptive map resolution has existed in the literature since at least 2021-2022, independently discovered by at least two different research groups in two different domains:
  1. **Larsson, Asgharivaskasi, Lim, Atanasov, Tsiotras, "Information-Theoretic Abstraction of Semantic Octree Models" (arXiv:2209.10035, 2022)** formalizes an explicit objective that lets a robot declare certain semantic classes "relevant" (weight β) vs. "irrelevant" (weight γ) and prunes/expands octree nodes accordingly — this is precisely "semantic-aware adaptive resolution," directly demonstrated, not hypothetical, three-plus years before this project.
  2. **Stache, Westheider, Magistri, Stachniss, Popović, "Adaptive Path Planning for UAVs for Multi-Resolution Semantic Segmentation" (arXiv:2203.01642, 2021-2022)** independently ties resolution (via UAV flight altitude) directly to the fraction of target-class pixels detected in imagery — again, semantic content is the explicit trigger for finer resolution.
  3. **Asgharivaskasi & Atanasov, "Distributed Optimization ... Multi-Robot Semantic Octree Mapping" (arXiv:2402.08867, 2024)** shows this lineage continuing into 2024 with "adaptive-resolution" semantic octree compression.
  - However, all three of these are either (a) full unbounded 3D octrees rather than 2.5D, or (b) flat 2D UAV/agricultural imagery rather than a ground-vehicle terrain/dynamic-object perception map. **None** operate in the SIH's specific target setting (ground robot/vehicle, real-time, 2.5D terrain representation, dynamic-object-aware). So while H3 as literally stated ("semantic-aware adaptive resolution... unexplored") is disproved by direct prior art, a narrower, more defensible version — "semantic-aware adaptive resolution specifically for real-time ground-vehicle 2.5D terrain/dynamic-object perception" — remains not directly demonstrated in anything this review found, i.e., weakened rather than fully disproved at that narrower scope.

### H4: "2.5D + adaptive resolution + semantic perception may represent a useful gap"
- **Verdict: Weakened, not disproved** — the three-way combination was **not found in the literature I searched**, but each pairwise combination of the three ingredients was found separately, which narrows (rather than eliminates) the claimed gap:
  - **2.5D + variable resolution, no semantics:** RoadRunner M&M (arXiv:2409.10940, distance-tier-driven) and the Planetary Rotorcraft paper (arXiv:2111.06271, sensing-density-driven "dynamic LoD").
  - **Variable resolution + semantics, not 2.5D:** Larsson et al. (arXiv:2209.10035, full 3D octree, class-weighted) and the SSMI/Asgharivaskasi-Atanasov line (arXiv:2112.04063, 2402.08867, full 3D octree, semantic but not class-weighted).
  - **2.5D + semantics, fixed resolution only:** MEM (arXiv:2309.16818, explicit uniform 4 cm grid) and RoadRunner (arXiv:2402.19341, fixed 20 cm grid, semantics used only for label generation, not at runtime).
  - **Semantic-driven adaptive resolution, flat 2D (no elevation):** Stache et al. (arXiv:2203.01642).
  - No paper found here combines all three — a **2.5D grid that both varies its resolution AND ties that variation to semantic content or perception confidence** — in any domain, let alone the SIH's ground-vehicle terrain/dynamic-object setting. This is stated explicitly as **"not found in the literature I searched," which is not the same as "does not exist"** — a genuinely thorough search across the assigned families and mandatory alternate terms did not surface it, but the existence of each pairwise combination (especially the very close analogues in Larsson et al. 2022 and RoadRunner M&M 2024) suggests the missing three-way combination is a plausible, low-hanging extension of already-published work rather than a deep unexplored frontier — a meaningfully different framing than "nobody has thought about any piece of this."

---

## Terminology/Concept Notes

- **Adaptive sensing vs. adaptive map representation, revisited for this group's papers:** The Stache et al. UAV paper (arXiv:2203.01642) is a clear example of the distinction the project brief warns about: the *sensor acquisition* is adapted (UAV changes altitude), and this happens to *produce* a map artifact whose resolution is spatially variable as a side effect — but there is no persistent map data structure whose internal resolution policy is separately, explicitly adaptive the way an octree/quadtree's pruning rule is. Classify this paper primarily under **adaptive sensor acquisition**, with adaptive map resolution as a secondary, derived consequence — not the other way around.
- **"Semantic octree" ≠ "semantic-class-weighted adaptive resolution":** Multiple octree-based semantic mapping papers (SSMI/Asgharivaskasi-Atanasov 2021-2024) store per-voxel semantic distributions and use octree pruning for compression, but the pruning criterion in most of these is generic statistical/occupancy homogeneity across sibling cells — *not* a deliberate policy of keeping specific semantic classes at finer resolution than others. Only Larsson et al. (2022) explicitly formalizes class-weighted pruning. This distinction matters a great deal for accurately assessing H3: "has a semantic label" and "resolution is semantically driven" are two different, commonly-conflated properties, and most of the "semantic octree" literature has the former without the latter.
- **"2.5D" boundary case:** Several papers in this family (SSMI, Larsson et al., Miles/Biggie/Heckman subterranean mapping) use full 3D octrees but *project* the map to a 2D or 2.5D plane for path planning. Per this project's definition (2.5D = single height value per 2D cell, not full unrestricted 3D), these octree papers are **not** 2.5D representations even though their planning consumers sometimes flatten them — the underlying map itself stores full 3D volumetric information and should not be counted as 2.5D evidence for H4.
- **Distance-driven vs. density/geometry-driven vs. uncertainty-driven vs. semantic-driven resolution are four distinct, independently-published mechanisms** found across this group's papers (RoadRunner M&M = distance-tier; Planetary Rotorcraft = pixel-footprint/measurement-density; USV Variable-Resolution Virtual Maps = SLAM-uncertainty/information-density; Larsson et al. and Stache et al. = semantic-content). The project brief's instruction not to treat these as equivalent is well-supported by this group's findings — they are genuinely different design choices with different papers each committing to exactly one.
- **"Fixed resolution is still the norm," even in 2023-2024 semantic/terrain-specific systems:** Of the ground-vehicle-oriented, terrain-semantic-aware systems found in this review (MEM, RoadRunner, Miles/Biggie/Heckman subterranean mapping), all three use fixed/uniform base resolution. The only ground-vehicle-relevant system with genuine spatial resolution variation (RoadRunner M&M) does not use semantics. This is a real, direct-evidence-supported pattern, not an assumption.

---

## Papers Considered But Excluded

- **N-QGN: Navigation Map from a Monocular Camera using Quadtree Generating Networks** (arXiv:2202.11982) — surfaced in quadtree-navigation searches; focused on learned quadtree generation from monocular depth for navigation cost, not clearly semantic or terrain-specific from the title/snippet; not pursued further given time budget and lower apparent relevance to the assigned families.
- **Seeing Through the Grass: Semantic Pointcloud Filter for Support Surface Learning** (arXiv:2305.07995) — surfaced as a strong lead (semantic + support-surface/terrain relevance) but not fetched in full due to time constraints; flagged for potential follow-up in a later research pass rather than included here on snippet-only evidence.
- **Few-shot Semantic Learning for Robust Multi-Biome 3D Semantic Mapping in Off-Road Environments** (arXiv:2411.06632) — relevant off-road semantic mapping lead, but appeared to be primarily about few-shot learning/generalization across biomes rather than resolution strategy; deprioritized given the assigned hypothesis focus on resolution.
- **STONE Dataset: A Scalable Multi-Modal Surround-View 3D Traversability Dataset** (arXiv:2603.09175) — a dataset paper rather than a method paper; noted for completeness but not written up as a full entry since it does not itself propose a representation/resolution strategy.
- **IRisPath, Learning-based Traversability Costmap for Autonomous Off-road Navigation** (arXiv:2406.08187), **Mars Traversability Prediction** (arXiv:2509.11082) — all surfaced as relevant costmap/traversability leads but not fetched in full; each appeared, from title/snippet, to use standard fixed-resolution BEV/grid costmaps without a distinguishing resolution-adaptation or semantic-resolution-coupling claim, so they were deprioritized in favor of papers more directly bearing on H3/H4.
- **"Resolution-adaptive Quadtrees for Semantic Segmentation Mapping in UAV Applications"** — included above as a snippet-only entry rather than excluded, because its title is directly on-point for H3, but flagged prominently as unverified due to paywall access failures (IEEE Xplore and ResearchGate both returned HTTP 403).
- **GA-Nav, TE-NeXt, RoadRunner M&M's own X-Racer baseline stack, TERP** — surfaced repeatedly as adjacent off-road semantic/traversability systems but not independently fetched, since their relevant technical content (semantic segmentation feeding traversability, no resolution adaptation) is already well-represented by the RoadRunner/RoadRunner M&M and Larsson et al. entries above; included by reference only to avoid redundant, shallow entries.
