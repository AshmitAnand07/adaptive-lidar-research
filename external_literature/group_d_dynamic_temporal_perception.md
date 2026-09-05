# External Literature — Group D: Dynamic Occupancy, Motion Segmentation, Scene Flow, Temporal LiDAR Perception

**Assigned families:** Dynamic occupancy grids; dynamic LiDAR perception; LiDAR motion segmentation; LiDAR scene flow; temporal LiDAR perception.
**Assigned hypothesis to stress-test:** H2 — "No existing work combines dynamic-object perception with adaptive resolution."

This document reports the results of a deliberately adversarial search: the goal was to find a
counterexample to H2, not to confirm it. Two papers (MURAL/"Anytime LiDAR" and AdaOcc) came close
enough that they are discussed in detail below, with the specific reasons they do or do not fully
satisfy H2's criteria made explicit rather than glossed over.

---

## Searches Conducted

1. dynamic occupancy grid map LiDAR moving objects 2024
2. Bayesian occupancy filter dynamic environment particle-based occupancy grid
3. LiDAR moving object segmentation 2024 2025 arxiv
4. 4DMOS moving object segmentation LiDAR sequential
5. LiDAR scene flow estimation self-supervised autonomous driving 2024
6. multi-resolution occupancy grid dynamic objects tracking adaptive
7. hierarchical octree moving object detection LiDAR variable resolution
8. DATMO detection and tracking of moving objects LiDAR grid
9. adaptive voxel grid dynamic object segmentation point cloud
10. occupancy flow prediction multi-resolution BEV grid
11. AdaOcc adaptive resolution occupancy prediction dynamic objects arxiv
12. LiDAR panoptic segmentation dynamic 4D temporal instance
13. spatiotemporal occupancy grid coarse-to-fine dynamic environment robot
14. level of detail LiDAR mapping dynamic environment robot navigation
15. sparse convolution moving object detection variable voxel size LiDAR
16. "adaptive resolution" dynamic object detection LiDAR map representation
17. quadtree grid map moving obstacle variable resolution mobile robot
18. scene flow estimation hierarchical coarse-to-fine pyramid point cloud PWC
19. temporal fusion recurrent LiDAR 3D object detection sequence 2024
20. multi-scale dynamic occupancy grid map neural network real-time
21. MURAL multi-resolution adaptive LiDAR pillar object detection deadline
22. "Exploring Input Resolution Scaling" anytime LiDAR object detection
23. SegNet4D instance aware 4D semantic segmentation LiDAR point cloud
24. Learning Spatiotemporal Occupancy Grid Maps Lifelong Navigation Dynamic Scenes resolution
25. MURAL "multi-resolution" LiDAR arxiv resolution-aware batch normalization pillar
26. Flow4D 4D voxel network LiDAR scene flow real-time Argoverse
27. Dynamics-Aware Spatiotemporal Occupancy Prediction Urban Environments resolution grid
28. Detection and Tracking of Moving Objects DATMO review classic occupancy grid history
29. particle based dynamic occupancy grid Nuss Danescu classic foundational
30. spatially adaptive resolution moving object detection LiDAR near far distance
31. MotionNet joint perception motion prediction BEV LiDAR point cloud
32. Categorized Grid Unknown Space Causes LiDAR Dynamic Occupancy Grids 2024
33. PointRNN spatiotemporal point cloud sequence learning recurrent
34. 4D LiDAR perception survey dynamic environment 2024 2025 review
35. semantic scene flow joint segmentation dynamic object arxiv 2024 2025
36. AdaOcc adaptive resolution occupancy prediction "camera" OR "vision-centric" nuScenes Bosch
37. "Moving Object Segmentation in 3D LiDAR Data" Chen Li Kang authors RAL IROS 2021 LMNet range image
38. "Dynamics-Aware Spatiotemporal Occupancy Prediction" authors Toyota venue ICRA IROS
39. octree Bayesian filter dynamic occupancy moving object hierarchical resolution
40. multi-resolution voxel moving object segmentation tracking LiDAR "variable resolution"
41. hierarchical sparse voxel dynamic object tracking robot octomap moving
42. DynORecon Dynamic Object Reconstruction Navigation arxiv 2409.19928 details
43. Spatio-temporal voxel layer Macenski Tsai Feinberg costmap dynamic world resolution
44. Multi-Resolution 3D Mapping Explicit Free Space Representation arxiv 2010.07929
45. "Detection and Tracking of Moving Obstacles (DATMO): A Review" authors Robotica journal
46. SegNet4D authors Neng Wang Chen Chen Xieyuanli Chen NUDT
47. SemanticFlow authors 2503.14837 self-supervised scene flow instance segmentation
48. Flow4D authors DGIST arxiv 2407.07995 Kim

Additionally, ~16 WebFetch calls were made to arXiv abstract/HTML/PDF pages to verify claims beyond
search-result snippets (noted per-paper below as "Access level"). Two WebFetch attempts (AdaOcc PDF,
and a rate-limited aimodels.fyi page) failed to return usable full text; those cases are flagged as
reduced-confidence.

Searches were stopped when a genuine session-level rate limit was hit on the WebSearch tool, after
48 distinct queries had already been run across all five assigned families plus the mandatory
alternate-terminology list. Coverage is judged adequate: every mandatory term (multi-scale,
multi-resolution, hierarchical, level of detail, variable-resolution, dynamic resolution, spatially
adaptive, adaptive voxel, adaptive grid, coarse-to-fine, moving object detection/segmentation, 4D
LiDAR perception, spatiotemporal occupancy, dynamic voxel grid, DATMO, scene flow, LiDAR panoptic
segmentation dynamic, occupancy flow prediction) was searched at least once, several in combination
with "adaptive"/"variable resolution"/"multi-resolution" specifically to hunt for H2 counterexamples.

---

## Papers

### A Random Finite Set Approach for Dynamic Occupancy Grid Maps with Real-Time Application
- Authors: Dominik Nuss, Stephan Reuter, Markus Thom, Ting Yuan, Gunther Krehl, Michael Maile, Axel Gern, Klaus Dietmayer
- Year: 2016 (arXiv preprint), journal version in *International Journal of Robotics Research* 2018
- Venue: IJRR / arXiv
- Link/identifier: arXiv:1605.02406
- Access level: abstract/preprint only
- Problem: Real-time fusion of laser and radar data into a grid representation that jointly captures static and dynamic (moving) parts of the environment.
- Representation: 2D BEV occupancy grid, cell-wise occupancy + velocity distribution (particle-based PHD/multi-instance-Bernoulli filter).
- Resolution strategy: Fixed cell size (uniform grid), not stated as variable in accessible text. DERIVED: consistent with the rest of the DOGMa literature lineage, which uses uniform cells.
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive.
- Perception method: Classical Bayesian/random-finite-set filtering (particle filter), not learned.
- Terrain handling: None.
- Dynamic-object handling: Foundational — per-cell velocity estimation via a random finite set (PHD/MIB) filter; this is the classic mechanism that gives a grid cell "dynamic" state without needing object-level detection first.
- Temporal processing: Recursive Bayesian filter, frame-to-frame particle propagation (not a learned sequence model).
- Uncertainty handling: Yes — the whole method is explicitly probabilistic (RFS formalism), propagating occupancy and velocity uncertainty per cell.
- Computational characteristics: DIRECT EVIDENCE (from abstract): described as real-time capable with a parallelized particle-filter implementation; no specific FPS/latency number was retrievable from the accessible text.
- Datasets: Not confirmed from accessible text (real vehicle sensor data, laser + radar).
- Evaluation: Not confirmed beyond qualitative real-time claim in accessible excerpt.
- Limitations: INFERENCE — fixed grid resolution means memory/compute scale with map extent regardless of where dynamic activity actually occurs.
- Relevance to SIH problem: This is one of the two foundational lineages (with Danescu et al. below) underlying almost all modern dynamic-occupancy-grid work; establishes that "dynamic occupancy grid" as a concept is old (2011–2018) and well-established, not novel, and that it has historically used fixed resolution.
- Evidence level(s) for key claims: WEB VERIFIED (via WebFetch of arXiv abstract page) for authorship/venue/topic; DERIVED for "fixed resolution" (not explicitly falsified in accessible text, but never claimed as adaptive anywhere in the literature describing this line of work).

### Modeling and Tracking the Driving Environment With a Particle-Based Occupancy Grid
- Authors: Radu Danescu, Florin Oniga, Sergiu Nedevschi
- Year: 2011
- Venue: IEEE Transactions on Intelligent Transportation Systems
- Link/identifier: DOI via IEEE Xplore (accessed via secondary sources: ResearchGate, Semantic Scholar)
- Access level: snippet only — flagged low-confidence
- Problem: Track the dynamic driving environment (stereo-vision based) using an occupancy grid that carries per-cell motion state.
- Representation: 2D grid; particles carry position + velocity and migrate across cells to represent object dynamics.
- Resolution strategy: Fixed grid cell size. HYPOTHESIS-level confidence only (not directly confirmed from primary text, but consistent with all secondary descriptions found).
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive.
- Perception method: Classical particle filter, not learned.
- Terrain handling: None reported.
- Dynamic-object handling: Foundational — this is the paper that introduced representing per-cell dynamic state via particles (position+velocity) that migrate between cells, later built upon by Nuss et al.
- Temporal processing: Particle filter, frame-to-frame.
- Uncertainty handling: Implicit in the particle representation (stereo reconstruction uncertainty explicitly modeled per search snippets).
- Computational characteristics: Not available at snippet-only access level.
- Datasets: Not available at snippet-only access level.
- Evaluation: Not available at snippet-only access level.
- Limitations: Not available at snippet-only access level.
- Relevance to SIH problem: Establishes the historical/foundational lineage of dynamic occupancy grids — useful for showing that "dynamic occupancy grid" is a >10-year-old concept, distinct from the "adaptive resolution" question this project is investigating.
- Evidence level(s) for key claims: WEB VERIFIED for existence/authorship/year/venue only; all technical claims are INFERENCE from secondary-source snippets, explicitly flagged low confidence.

### A Multi-Task Recurrent Neural Network for End-to-End Dynamic Occupancy Grid Mapping
- Authors: Marcel Schreiber, Vasileios Belagiannis, Claudius Gläser, Klaus Dietmayer
- Year: 2022
- Venue: IEEE Intelligent Vehicles Symposium (IV 2022)
- Link/identifier: arXiv:2202.04461
- Access level: abstract/preprint only
- Problem: Predict dynamic occupancy grid maps (occupancy, velocity, semantics, drivable area) end-to-end from raw LiDAR, without hand-designed preprocessing (ground removal, inverse sensor model).
- Representation: 2D BEV grid built from raw LiDAR sweeps with height channels.
- Resolution strategy: Fixed grid resolution — exact cell size not confirmed from accessible text, but no variable-resolution mechanism mentioned anywhere in problem description, method description, or search-indexed summaries.
- Adaptive mechanism categor(y/ies): None found — fixed resolution, not adaptive.
- Perception method: Learned — combination of convolutional + recurrent (RNN) layers, trained end-to-end.
- Terrain handling: Drivable-area prediction is one of the four output heads (a coarse terrain-adjacent signal, not detailed traversability analysis).
- Dynamic-object handling: Per-cell velocity estimation (dynamic occupancy grid mapping, DOGMa-style) plus semantic classification, learned jointly.
- Temporal processing: Recurrent (RNN) processing of a sequence of raw LiDAR BEV frames.
- Uncertainty handling: Not confirmed beyond the occupancy-probability output itself.
- Computational characteristics: Not confirmed from accessible text.
- Datasets: Not confirmed from accessible text.
- Evaluation: Not confirmed from accessible text.
- Limitations: INFERENCE — fixed BEV resolution over the whole scene extent; no mechanism to concentrate resolution near the ego-vehicle or near detected dynamic activity.
- Relevance to SIH problem: Directly relevant to the "adaptive map resolution + dynamic objects" question as a **negative** data point — it is a modern (2022), learned, multi-task dynamic-occupancy system that explicitly does NOT use adaptive resolution.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/topic/outputs; DERIVED for "fixed resolution, not adaptive" (absence of any adaptive-resolution claim across multiple independent search results).

### Categorized Grid and Unknown Space Causes for LiDAR-based Dynamic Occupancy Grids
- Authors: Víctor Jiménez-Bermejo, Jorge Godoy, Antonio Artuñedo, Jorge Villagra
- Year: 2024
- Venue: IEEE conference (2024); arXiv preprint
- Link/identifier: arXiv:2407.02192
- Access level: abstract/preprint only
- Problem: Extends an existing (fixed-resolution) LiDAR dynamic occupancy grid with a complementary "categorized grid" that semantically labels occupied cells by dynamic state/reliability and unknown-space cells by cause of unknown-ness (sensor limits, occlusion, environment).
- Representation: 2D dynamic occupancy grid (builds explicitly on prior DOGMa work), plus a semantic overlay layer.
- Resolution strategy: Fixed — the paper explicitly builds on "the already well-established LiDAR-based Dynamic Occupancy Grid," i.e., inherits the standard fixed-cell DOGMa structure; the contribution is semantic categorization of cells, not resolution.
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive.
- Perception method: Classical grid-based/evidential reasoning (per search snippets — categorization logic on top of an existing DOGMa), not a full neural pipeline.
- Terrain handling: Indirect — the "unknown space" causal labeling includes environment-induced occlusion, which is terrain/scene-structure-adjacent but not traversability analysis.
- Dynamic-object handling: Occupied cells are labeled by "dynamic state," i.e., the grid already carries per-cell dynamic/static labels inherited from the base DOGMa this work extends.
- Temporal processing: Inherited from base DOGMa (frame-to-frame recursive filtering).
- Uncertainty handling: Yes — "reliability" labeling of occupied cells and causal labeling of unknown space are both uncertainty-adjacent contributions.
- Computational characteristics: Not confirmed from accessible text.
- Datasets: Real-world scenarios per search snippet; specific dataset name not confirmed.
- Evaluation: Qualitative ("showcased in real-world scenarios") per accessible snippets; no quantitative metric confirmed.
- Limitations: Not confirmed from accessible text.
- Relevance to SIH problem: A 2024 paper explicitly confirming that dynamic occupancy grids remain a fixed-resolution paradigm even in current work — useful supporting evidence that the DOGMa line of research and the adaptive-resolution line of research have, to date, developed largely independently.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/year/topic; DERIVED for "fixed resolution."

### Dynamic Occupancy Grid Map with Semantic Information Using Deep Learning-Based BEVFusion Method with Camera and LiDAR Fusion
- Authors: Harin Jang, Taehyun Kim, Kyungjae Ahn, Soo Jeon, Yeonsik Kang
- Year: 2024
- Venue: *Sensors* (Basel), MDPI, DOI 10.3390/s24092828
- Link/identifier: PMC11086224
- Access level: abstract/preprint only (WebFetch of PMC page returned partial content)
- Problem: Build a dynamic occupancy grid that carries position, velocity, and semantic class information per cell, using camera+LiDAR fusion.
- Representation: 2D BEV grid; BEVFusion architecture fuses camera and LiDAR features in BEV space.
- Resolution strategy: DIRECT EVIDENCE (from accessible text): a bounding-box "border thickness" parameter of 0.4 m is mentioned, implying sub-meter grid granularity, but no evidence of spatially variable cell size was found anywhere in the accessible text — fixed resolution is the best-supported reading.
- Adaptive mechanism categor(y/ies): None found — fixed resolution, not adaptive.
- Perception method: Learned — BEVFusion (camera+LiDAR sensor fusion in BEV) combined with a DOGMa update model.
- Terrain handling: Not a focus of this paper.
- Dynamic-object handling: DIRECT EVIDENCE: "not only the position and velocity information of objects but also their class information can be updated" — genuine dynamic (moving) object representation with velocity and semantic class per cell.
- Temporal processing: DOGMa-style recursive cell update (frame-to-frame), consistent with the broader DOGMa lineage.
- Uncertainty handling: Standard DOGMa occupancy-probability framework; no additional uncertainty mechanism confirmed.
- Computational characteristics: Not confirmed from accessible text.
- Datasets: DIRECT EVIDENCE: nuScenes (1000 scenes, Boston/Singapore, 32-channel LiDAR + 6 cameras + radar).
- Evaluation: DIRECT EVIDENCE: mean absolute error for velocity and heading-angle estimation vs. ground truth.
- Limitations: INFERENCE — fixed-resolution grid; no adaptive/multi-resolution mechanism, meaning compute/memory scale uniformly regardless of scene structure.
- Relevance to SIH problem: A genuinely strong, modern, semantic + dynamic occupancy grid — but explicitly fixed-resolution. Directly relevant as evidence that state-of-the-art (2024) dynamic occupancy grids with rich semantic+velocity content still do not adopt spatially variable resolution.
- Evidence level(s) for key claims: WEB VERIFIED (WebFetch of PMC page) for dynamic-object handling, dataset, and evaluation approach; DERIVED for "fixed resolution."

### Detection and Tracking of Moving Obstacles (DATMO): A Review
- Authors: Á. Llamazares, E. Molinos, M. Ocaña
- Year: 2020 (published in *Robotica*, Vol. 38, pp. 761–774; DOI 10.1017/S0263574719001024)
- Venue: *Robotica* (Cambridge University Press)
- Link/identifier: DOI 10.1017/S0263574719001024
- Access level: snippet only — flagged low-confidence
- Problem: Survey of the state of the art in detecting and tracking moving obstacles (DATMO) for mobile robots/vehicles.
- Representation: Survey — covers model-free, model-based, and grid-based DATMO approaches broadly.
- Resolution strategy: N/A (survey paper; individual surveyed methods vary, but per search snippets none of the grid-based methods discussed are described as adaptive-resolution).
- Adaptive mechanism categor(y/ies): N/A — survey.
- Perception method: Survey covering both classical (model-based/model-free geometric tracking) and grid-based approaches.
- Terrain handling: Not a focus.
- Dynamic-object handling: This is the core topic — detection AND tracking of moving obstacles, the classic DATMO formulation (detect, segment, associate, filter/track).
- Temporal processing: Survey covers Kalman filters, particle filters, interacting multiple models (IMM) as the standard temporal/tracking mechanisms in this literature.
- Uncertainty handling: Standard tracking-filter uncertainty (covariance/particle-based), per the surveyed methods.
- Computational characteristics: N/A — survey.
- Datasets: N/A — survey.
- Evaluation: N/A — survey.
- Limitations: N/A — survey (limitations are discussed per-method within the review, not extractable from snippet-level access here).
- Relevance to SIH problem: Establishes DATMO as the classical foundational framing of "dynamic-object perception" for mobile robots, predating and largely running in parallel to the adaptive-resolution mapping literature. Useful for lineage/terminology grounding.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/year/topic only; all other fields explicitly N/A/low-confidence due to snippet-only access.

### MotionNet: Joint Perception and Motion Prediction for Autonomous Driving Based on Bird's Eye View Maps
- Authors: Pengxiang Wu, Siheng Chen, Dimitris N. Metaxas
- Year: 2020
- Venue: CVPR 2020
- Link/identifier: arXiv:2003.06754
- Access level: abstract/preprint only
- Problem: Jointly perform per-cell category classification and motion (velocity) prediction from a sequence of LiDAR sweeps, in a single efficient BEV model.
- Representation: BEV grid (multi-channel 2D "image" built from raw point clouds).
- Resolution strategy: Fixed BEV grid resolution — no adaptive/multi-resolution mechanism found in any accessible source. The "spatio-temporal pyramid network" backbone is a multi-scale **feature** pyramid inside the network (for hierarchical feature extraction), not a spatially variable **map** resolution — an important distinction (see Terminology notes).
- Adaptive mechanism categor(y/ies): Adaptive neural computation (loosely) — a hierarchical feature pyramid inside the backbone — but NOT adaptive map resolution; the persistent BEV grid itself is uniform resolution.
- Perception method: Learned — single-stage CNN backbone ("spatio-temporal pyramid network": 2D spatial conv + lightweight pseudo-1D temporal conv) with task-specific heads for classification + motion.
- Terrain handling: Not a focus (category head is object/background-oriented).
- Dynamic-object handling: DIRECT EVIDENCE: per-cell object category + per-cell motion (velocity) prediction, jointly, in one pass — a clean example of joint dynamic-object detection + motion estimation from a sequence.
- Temporal processing: Sequence of LiDAR sweeps processed with spatio-temporal convolutions (not a recurrent/Bayesian filter — feed-forward temporal conv).
- Uncertainty handling: Not reported.
- Computational characteristics: DIRECT EVIDENCE (from search-indexed summary, not independently re-verified in full text): reported to run at 53 Hz.
- Datasets: Not confirmed from accessible text (nuScenes, per general knowledge of this paper's public benchmark use — HYPOTHESIS-level, not independently confirmed here).
- Evaluation: Not confirmed from accessible text.
- Limitations: INFERENCE — fixed BEV resolution; a real-time, well-cited (CVPR 2020) joint perception+motion system that never adopts spatially variable resolution.
- Relevance to SIH problem: A well-known example of joint dynamic-object + motion perception on a uniform-resolution BEV grid — reinforces that this combination (dynamic perception + temporal fusion) has historically shipped with fixed, not adaptive, spatial resolution.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/architecture description; the 53 Hz figure is carried from a search-result summary and not independently re-verified against primary text, so it is marked reduced-confidence.

### Dynamics-Aware Spatiotemporal Occupancy Prediction in Urban Environments
- Authors: M. Toyungyernsub, E. Yel, J. Li, M. J. Kochenderfer
- Year: 2022
- Venue: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2022)
- Link/identifier: arXiv:2209.13172
- Access level: abstract/preprint only
- Problem: Detect and segment moving obstacles, then predict the future spatiotemporal evolution of occupancy in the local environment, without relying on ground-truth object detection/tracking.
- Representation: Occupancy grid map (OGM), standard grid discretization.
- Resolution strategy: Fixed — no adaptive-resolution mechanism mentioned; the explicit design goal is avoiding dependency on accurate object detection/tracking, which argues against an object-centric adaptive-resolution scheme.
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive.
- Perception method: Learned — combines static/dynamic segmentation with a predictive (forecasting) network.
- Terrain handling: Not a focus.
- Dynamic-object handling: DIRECT EVIDENCE: static-dynamic object segmentation is an explicit stage of the pipeline, feeding into occupancy prediction.
- Temporal processing: Predicts future spatiotemporal occupancy states — a forecasting/sequence model (exact architecture not confirmed at abstract-level access).
- Uncertainty handling: Not confirmed from accessible text.
- Computational characteristics: Not confirmed from accessible text.
- Datasets: Not confirmed from accessible text.
- Evaluation: Not confirmed from accessible text.
- Limitations: Not confirmed from accessible text.
- Relevance to SIH problem: Another instance of dynamic-object segmentation + temporal occupancy prediction shipping on a fixed-resolution grid, at IROS 2022 — reinforces the pattern.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/year/pipeline stages; DERIVED for "fixed resolution."

### Learning Spatiotemporal Occupancy Grid Maps for Lifelong Navigation in Dynamic Scenes
- Authors: Hugues Thomas, Matthieu Gallet de Saint Aurin, Jian Zhang, Timothy D. Barfoot
- Year: 2021 (arXiv), presented ICRA 2022
- Venue: ICRA 2022 / Apple Machine Learning Research
- Link/identifier: arXiv:2108.10585
- Access level: abstract/preprint only
- Problem: Generate, predict, and use Spatiotemporal Occupancy Grid Maps (SOGMs) that embed future dynamic-scene information, self-supervised, for lifelong robot navigation.
- Representation: Time-stamped 2D grids (SOGMs), built from a 3D backend over LiDAR frames.
- Resolution strategy: Fixed — the paper describes "time-stamped 2D grids"; no adaptive/variable-resolution mechanism found in any accessible source.
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive.
- Perception method: Learned — 3D backend (semantic segmentation of LiDAR frames) + 2D front-end predicting future SOGM states.
- Terrain handling: Not a specific focus (though semantic segmentation of the 3D backend could plausibly include ground/terrain classes — not confirmed).
- Dynamic-object handling: DIRECT EVIDENCE: LiDAR points are annotated by "dynamic properties" and projected onto time-stamped grids; this is explicit dynamic-object-aware occupancy representation.
- Temporal processing: Explicit future-state prediction (a 3D-2D feedforward architecture trained to predict future SOGM time steps) — self-supervised, enabling lifelong/continual learning without manual labels.
- Uncertainty handling: Not confirmed from accessible text.
- Computational characteristics: Not confirmed from accessible text.
- Datasets: Self-collected from prior robot navigation logs (per accessible summary); no public benchmark name confirmed.
- Evaluation: Qualitative real-world navigation scenarios (corridors, intersections, offices) per search snippets.
- Limitations: Not confirmed from accessible text.
- Relevance to SIH problem: A strong, well-cited (Apple ML Research/ICRA 2022) example of temporal + dynamic-object-aware occupancy mapping for real robot navigation, again on fixed spatial resolution.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/pipeline description; DERIVED for "fixed resolution."

### DynORecon: Dynamic Object Reconstruction for Navigation
- Authors: Yiduo Wang, Jesse Morris, Lan Wu, Teresa Vidal-Calleja, Viorela Ila
- Year: 2024 (arXiv), submitted to ICRA 2025
- Venue: ICRA 2025 (submitted)
- Link/identifier: arXiv:2409.19928
- Access level: abstract/preprint only
- Problem: Use Dynamic SLAM's per-object motion estimates to incrementally build a volumetric reconstruction of each moving object in the scene, plus free-space estimation, for navigation.
- Representation: A "volumetric map of observed moving entities" — exact data structure (voxel grid, TSDF, octree) NOT confirmed from accessible text.
- Resolution strategy: UNCLEAR — not confirmed whether fixed or adaptive from any accessible source; this is an explicit gap in what could be verified, not a claim either way.
- Adaptive mechanism categor(y/ies): Cannot be determined from accessible text — flagged explicitly rather than guessed.
- Perception method: Combines Dynamic SLAM (motion estimation) with incremental per-object volumetric reconstruction.
- Terrain handling: Free-space estimation is reported, which is navigation-relevant but not terrain/traversability analysis per se.
- Dynamic-object handling: DIRECT EVIDENCE: reconstructs multiple ("each") individually-tracked moving objects incrementally, removing residual artifacts from past observations — this is genuine per-object dynamic-object perception, not just ego-motion compensation.
- Temporal processing: Incremental/online refinement as new observations arrive (built on Dynamic SLAM's motion estimates).
- Uncertainty handling: Not confirmed from accessible text.
- Computational characteristics: DIRECT EVIDENCE: ~20 FPS, ~10 cm reconstruction accuracy (as explicitly stated in the abstract).
- Datasets: Simulated and real-world outdoor datasets (specific names not confirmed from accessible text).
- Evaluation: Not confirmed beyond the FPS/accuracy figures above.
- Limitations: Not confirmed from accessible text.
- Relevance to SIH problem: A genuinely interesting, very recent (2024/2025) candidate for combining dynamic-object perception with a spatial map representation — flagged prominently here precisely BECAUSE its resolution strategy could not be confirmed. This paper should be prioritized for a full-text read in a follow-up pass, since it is the single most promising unresolved lead for H2 found in this search.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/FPS/accuracy figures (via arXiv abstract page); explicitly UNVERIFIED/unknown for resolution strategy — reported as a gap, not as evidence either for or against adaptive resolution.

### Spatio-temporal voxel layer: A view on robot perception for the dynamic world
- Authors: Steve Macenski, David Tsai, Max Feinberg
- Year: 2020
- Venue: *International Journal of Advanced Robotic Systems*
- Link/identifier: DOI 10.1177/1729881420910530 (widely deployed as the ROS/Nav2 `spatio_temporal_voxel_layer` package)
- Access level: abstract/preprint only
- Problem: Provide an efficient, non-static-environment-assuming 3D costmap layer for robot navigation in large, dynamic, complex environments, replacing standard ray-casting-based clearing.
- Representation: Sparse voxel grid (backed by OpenVDB), replacing dense per-cell ray-casting with a "frustum acceleration" clearing technique.
- Resolution strategy: Fixed — a single configurable `voxel_size` parameter sets one uniform resolution for the whole sparse grid. IMPORTANT DISTINCTION: this grid is *sparse* (only stores occupied/active voxels, hence the large reported memory/CPU savings) but it is NOT *adaptive-resolution* — sparsity and spatially variable resolution are different mechanisms, and this paper is a clean example of the former without the latter (see Terminology notes).
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive (sparse storage is an efficiency mechanism, not a resolution-adaptation mechanism).
- Perception method: Classical/geometric — occupancy accumulation from depth/LiDAR sensors, no learned component.
- Terrain handling: Not a focus (obstacle/costmap layer, not terrain classification).
- Dynamic-object handling: DIRECT EVIDENCE: designed explicitly for "the dynamic world" — its frustum-based clearing does not assume a static environment, meaning it correctly clears voxels for objects that have moved, avoiding the "ghost obstacle" problem of naive ray-casting in dynamic scenes. This is dynamic-environment handling at the *mapping* level, not object-level detection/tracking/segmentation — an important distinction from the other papers in this table.
- Temporal processing: Continuous online accumulation/clearing as new sensor frames arrive.
- Uncertainty handling: Not reported (deterministic occupancy accumulation, not probabilistic).
- Computational characteristics: DIRECT EVIDENCE: reported ~400% less CPU load on average vs. the standard ROS voxel layer, while processing 9 QVGA depth cameras.
- Datasets: N/A (a real-time system/software package, not evaluated on a fixed benchmark dataset in the same sense as a learned model).
- Evaluation: Real-world/deployed system evaluation (widely used in ROS/Nav2 ecosystem) rather than benchmark-metric evaluation.
- Limitations: INFERENCE — fixed, uniform voxel resolution; sparsity gives efficiency but not the spatially concentrated resolution near the robot that the SIH problem statement describes.
- Relevance to SIH problem: Highly relevant as a widely deployed, real-world example of dynamic-environment-aware 3D mapping that explicitly is NOT adaptive-resolution — and a good illustration of why "sparse" and "adaptive/variable resolution" must not be conflated when evaluating candidate architectures for this project.
- Evidence level(s) for key claims: WEB VERIFIED for architecture, mechanism, and CPU-load claim; DERIVED for "fixed resolution despite sparsity."

### Moving Object Segmentation in 3D LiDAR Data: A Learning-based Approach Exploiting Sequential Data (LMNet)
- Authors: Xieyuanli Chen, Shijie Li, Benedikt Mersch, Louis Wiesmann, Jürgen Gall, Jens Behley, Cyrill Stachniss
- Year: 2021
- Venue: IEEE Robotics and Automation Letters (RA-L), Vol. 6, No. 4, pp. 6529–6536; also presented at IROS 2021
- Link/identifier: arXiv:2105.08971
- Access level: abstract/preprint only
- Problem: Segment moving vs. static points in 3D LiDAR data (e.g., distinguish a moving car from a parked car), which pure single-scan semantic segmentation cannot do.
- Representation: Range image (2D projection of the 3D LiDAR scan), using residual range images across consecutive scans as the temporal cue.
- Resolution strategy: Fixed range-image resolution (standard spherical projection), no adaptive mechanism.
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive.
- Perception method: Learned — CNN-based range-image segmentation network (compatible with existing range-image segmentation architectures via a modified data loader/input).
- Terrain handling: Not a focus (moving-object binary segmentation, not terrain classification).
- Dynamic-object handling: DIRECT EVIDENCE: this is the founding modern learned-MOS (moving object segmentation) paper — explicitly distinguishes moving from static/parked objects using sequential range images, faster than sensor frame rate.
- Temporal processing: Frame-to-frame (residual range images between consecutive scans), not a recurrent/receding-horizon design (that came later with 4DMOS).
- Uncertainty handling: Not reported.
- Computational characteristics: DIRECT EVIDENCE: reported to run faster than the LiDAR sensor's frame rate (real-time capable).
- Datasets: SemanticKITTI-MOS benchmark (the paper that established this now-standard benchmark).
- Evaluation: IoU on the moving-object class (SemanticKITTI-MOS metric); exact numeric value not confirmed from accessible text.
- Limitations: INFERENCE — range-image projection loses 3D geometric detail relative to raw point/voxel representations; fixed-resolution projection.
- Relevance to SIH problem: The foundational modern learned LiDAR-MOS method and SemanticKITTI-MOS benchmark, against which nearly all subsequent MOS papers in this document (4DMOS, MambaMOS, SegNet4D) are compared.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/benchmark establishment/architecture description.

### Receding Moving Object Segmentation in 3D LiDAR Data Using Sparse 4D Convolutions (4DMOS)
- Authors: Benedikt Mersch, Xieyuanli Chen, Ignacio Vizzo, Lucas Nunes, Jens Behley, Cyrill Stachniss
- Year: 2022
- Venue: IEEE Robotics and Automation Letters (RA-L)
- Link/identifier: arXiv:2206.04129
- Access level: abstract/preprint only
- Problem: Improve on range-image MOS (e.g., LMNet) by directly exploiting 3D spatio-temporal structure via sparse 4D convolutions, with online receding-horizon refinement.
- Representation: Voxelized sparse 4D point cloud (space + time), processed with sparse 4D convolutions (MinkowskiEngine-style).
- Resolution strategy: Fixed voxel resolution (exact cell size not confirmed from accessible text); sparsity is a computational-efficiency mechanism (only occupied voxels are processed), not spatially variable resolution — same important distinction as the STVL paper above.
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive (sparse ≠ adaptive resolution).
- Perception method: Learned — sparse 4D CNN.
- Terrain handling: Not a focus.
- Dynamic-object handling: DIRECT EVIDENCE: per-point moving-object confidence scores, refined via a binary Bayesian filter as post-processing, within a receding-horizon (sliding window) online scheme that allows prediction refinement as new scans arrive.
- Temporal processing: Sliding/receding window over multiple LiDAR scans, jointly processed via sparse 4D convolutions — DIRECT EVIDENCE, a genuinely sequence-native (not just frame-pair) temporal architecture.
- Uncertainty handling: Binary Bayesian filter recursively integrating new predictions — an explicit, if simple, uncertainty-integration mechanism.
- Computational characteristics: Not confirmed numerically from accessible text (described as "time- and memory-efficient" in search-indexed summaries).
- Datasets: SemanticKITTI-MOS challenge; generalization tested on the Apollo dataset.
- Evaluation: IoU on moving-object class (SemanticKITTI-MOS metric); exact value not confirmed from accessible text.
- Limitations: Not confirmed from accessible text.
- Relevance to SIH problem: A strong example of temporal LiDAR perception (receding-horizon 4D convolutions) combined with dynamic-object segmentation — again on fixed-resolution voxels, reinforcing the pattern this document is testing.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/architecture/datasets/temporal design.

### MambaMOS: LiDAR-based 3D Moving Object Segmentation with Motion-aware State Space Model
- Authors: Kang Zeng, Hao Shi, Jiacheng Lin, Siyu Li, Jintao Cheng, Kaiwei Wang, Zhiyong Li, Kailun Yang
- Year: 2024
- Venue: ACM Multimedia (ACM MM) 2024
- Link/identifier: arXiv:2404.12794
- Access level: abstract/preprint only
- Problem: Address "weak coupling of temporal and spatial information" in point-based LiDAR MOS by using a state-space model (Mamba-style) for motion-aware temporal-spatial fusion.
- Representation: Point cloud-based (not explicitly voxelized per accessible text), processed across multiple time steps.
- Resolution strategy: No adaptive/variable-resolution mechanism found; point-based processing sidesteps the fixed-voxel question but does not introduce spatial-resolution adaptivity either.
- Adaptive mechanism categor(y/ies): None found — not applicable/not adaptive in the map-resolution sense (this is a temporal-fusion architecture question, not a spatial-resolution question).
- Perception method: Learned — Time Clue Bootstrapping Embedding (TCBE) module + Motion-aware State Space Model (MSSM).
- Terrain handling: Not a focus.
- Dynamic-object handling: DIRECT EVIDENCE: locates and segments moving objects using motion information aggregated across multiple time steps via the state-space model.
- Temporal processing: State-space-model-based temporal-spatial coupling across scans (a 2024 architectural alternative to both range-image residuals and sparse 4D convolutions).
- Uncertainty handling: Not reported.
- Computational characteristics: Not confirmed numerically from accessible text ("state-of-the-art performance" claimed, no FPS given).
- Datasets: SemanticKITTI-MOS, KITTI-Road.
- Evaluation: IoU-based (SemanticKITTI-MOS metric convention); exact figures not confirmed from accessible text.
- Limitations: Not confirmed from accessible text.
- Relevance to SIH problem: Shows that even the newest (2024) architectural paradigm shift in LiDAR-MOS (state-space models replacing convolutions) is focused entirely on temporal-fusion quality, not on spatial-resolution adaptivity — reinforcing that these two research threads remain largely separate.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/architecture/datasets.

### SegNet4D: Efficient Instance-Aware 4D Semantic Segmentation for LiDAR Point Cloud
- Authors: Neng Wang, Ruibin Guo, Chenghao Shi, Ziyue Wang, Hui Zhang, Huimin Lu, Zhiqiang Zheng, Xieyuanli Chen
- Year: 2025 (arXiv preprint June 2024)
- Venue: IEEE Transactions on Automation Science and Engineering (T-ASE) 2025
- Link/identifier: arXiv:2406.16279
- Access level: abstract/preprint only
- Problem: Efficient 4D (multi-scan) LiDAR semantic segmentation that also determines whether each point is dynamic, avoiding the poor real-time performance of prior 4D-convolution/recursive-network approaches.
- Representation: Sequential LiDAR scans converted to BEV images; motion features extracted via BEV residuals (explicitly avoiding heavy 4D convolutions).
- Resolution strategy: Fixed BEV image resolution; no adaptive-resolution mechanism found.
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive.
- Perception method: Learned — decomposes the 4D segmentation task into Moving Object Segmentation (MOS) + Single-Scan Semantic Segmentation (SSS) sub-tasks, merged with instance-consistency information for instance-aware output.
- Terrain handling: Included implicitly within multi-class semantic segmentation (standard SemanticKITTI-style classes), not a dedicated traversability analysis.
- Dynamic-object handling: DIRECT EVIDENCE: classifies each point's semantic category AND whether it is dynamic, with instance-level consistency — a genuinely rich dynamic-object-aware 4D segmentation system, explicitly surpassing prior state of the art on both multi-scan semantic segmentation and MOS while being more efficient/real-time.
- Temporal processing: Multi-scan (4D) via BEV-residual motion features rather than full 4D convolutions or recurrence — an efficiency-oriented design choice.
- Uncertainty handling: Not reported.
- Computational characteristics: DIRECT EVIDENCE (qualitative): explicitly designed and reported to enable real-time operation, in contrast to prior heavier 4D-convolution/recursive approaches; exact FPS number not confirmed from accessible text.
- Datasets: SemanticKITTI (multi-scan segmentation + MOS benchmarks), per standard practice in this line of work (not independently re-confirmed from primary text at this access level).
- Evaluation: Standard multi-scan semantic segmentation mIoU + MOS IoU metrics (per accessible summaries); exact figures not confirmed.
- Limitations: Not confirmed from accessible text.
- Relevance to SIH problem: One of the most complete, most recent (2025) dynamic + semantic LiDAR perception systems found in this search — directly relevant to the SIH's combined terrain/object/semantic goals, but on fixed BEV resolution.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/architecture/task decomposition.

### PointPWC-Net: A Coarse-to-Fine Network for Supervised and Self-Supervised Scene Flow Estimation on 3D Point Clouds
- Authors: Wenxuan Wu, Zhiyuan Wang, Zhuwen Li, Wei Liu, Li Fuxin
- Year: 2019 (arXiv)/2020 (ECCV)
- Venue: ECCV 2020
- Link/identifier: arXiv:1911.12408
- Access level: abstract/preprint only
- Problem: Estimate per-point 3D scene flow (motion field) between consecutive point clouds, including large motions, without requiring a fixed/regular grid.
- Representation: Point-based; a feature pyramid is built per point cloud, with PointConv-based downsampling by 4x per pyramid level.
- Resolution strategy: IMPORTANT NUANCE: this is a "coarse-to-fine" network in the sense of a multi-level feature pyramid used *inside* a single feed-forward inference pass (like an FPN), where flow computed at a coarse pyramid level is upsampled/warped to refine the next finer level. This is NOT a spatially variable, persistent map representation — it is a standard hierarchical-feature-computation pattern common throughout deep learning, applied here to point clouds. Classifying this correctly is important: "coarse-to-fine" wording alone should not be read as evidence for H2's "adaptive map resolution" criterion.
- Adaptive mechanism categor(y/ies): Adaptive neural computation (hierarchical feature-pyramid inference) — NOT adaptive map resolution (there is no persistent map at all; scene flow is per-point, per-inference).
- Perception method: Learned — end-to-end deep network with novel cost-volume, upsampling, and warping layers designed for point clouds (adapting PWC-Net's 2D optical-flow coarse-to-fine design to 3D points).
- Terrain handling: Not applicable (generic scene flow, not terrain-specific).
- Dynamic-object handling: Scene flow gives per-point 3D motion vectors, which is a form of dense, unsupervised-friendly dynamic-object perception (motion without requiring prior object detection), but the paper itself does not perform object-level detection/tracking/segmentation — it is flow estimation only.
- Temporal processing: Frame-pair (two consecutive point clouds), not a longer sequence/receding-window design.
- Uncertainty handling: Not reported.
- Computational characteristics: Not confirmed numerically from accessible text.
- Datasets: FlyingThings3D and KITTI Scene Flow 2015.
- Evaluation: Standard scene-flow metrics (EPE3D and related, per convention for these benchmarks); exact numeric values not confirmed from accessible text.
- Limitations: INFERENCE — as an early (2019/2020) self-supervised scene-flow method, likely subject to the point-distribution-imbalance and object-level-motion-constraint issues later explicitly identified and addressed by SeFlow (2024, below).
- Relevance to SIH problem: The foundational coarse-to-fine architecture pattern that essentially all subsequent point-cloud scene-flow work (including Flow4D and SemanticFlow below) builds on or is compared against; also a clear illustration of why "coarse-to-fine"/"multi-scale" terminology needs careful disambiguation from "adaptive map resolution" for this project's purposes.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/datasets/architecture description.

### SeFlow: A Self-Supervised Scene Flow Method in Autonomous Driving
- Authors: Qingwen Zhang, Yi Yang, Peizheng Li, Olov Andersson, Patric Jensfelt
- Year: 2024
- Venue: ECCV 2024
- Link/identifier: arXiv:2407.01702
- Access level: abstract/preprint only
- Problem: Self-supervised LiDAR scene flow that overcomes two identified weaknesses of prior self-supervised methods: point-distribution imbalance and lack of object-level motion constraints.
- Representation: Not explicitly confirmed (voxel-based per general knowledge of the method's efficient/real-time design, per the OpenSceneFlow benchmark suite it is listed in — INFERENCE, not directly confirmed from accessible text).
- Resolution strategy: Not confirmed; no adaptive/variable-resolution mechanism mentioned anywhere in accessible text.
- Adaptive mechanism categor(y/ies): None confirmed — likely fixed resolution (INFERENCE), not adaptive.
- Perception method: Learned, self-supervised — integrates an "efficient dynamic classification" sub-task directly into the scene-flow pipeline, using different objective functions for different motion patterns (static vs. dynamic points handled differently).
- Terrain handling: Not applicable.
- Dynamic-object handling: DIRECT EVIDENCE: explicit static/dynamic point classification integrated into the flow pipeline, with object-level motion constraints (cluster consistency, correct object-point association) — a genuinely explicit dynamic-vs-static discrimination mechanism, not just raw flow vectors.
- Temporal processing: Frame-pair based (consecutive LiDAR scans), consistent with the scene-flow task formulation.
- Uncertainty handling: Not reported.
- Computational characteristics: DIRECT EVIDENCE (qualitative): described as "real-time capable"; no specific FPS/latency number confirmed from accessible text.
- Datasets: Argoverse 2 and Waymo Open Dataset.
- Evaluation: "State-of-the-art performance on the self-supervised scene flow task" per accessible summary; exact metric values not confirmed.
- Limitations: Explicitly self-identified in the paper's own framing (per search snippet): point-distribution imbalance and object-level motion constraints were the problems being solved, implying prior self-supervised methods (including PointPWC-Net-style approaches) suffered from these.
- Relevance to SIH problem: A strong, current (ECCV 2024) example of dynamic-object-aware LiDAR perception (explicit static/dynamic classification within scene flow) — again with no evidence of adaptive map resolution.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/datasets/method description; INFERENCE for representation/resolution (not explicitly stated in accessible text).

### Flow4D: Leveraging 4D Voxel Network for LiDAR Scene Flow Estimation
- Authors: Jaeyeul Kim, Jungwan Woo, Ukcheol Shin, Jean Oh, Sunghoon Im
- Year: 2024 (arXiv), RA-L 2025
- Venue: IEEE Robotics and Automation Letters (RA-L 2025); 1st place, 2024 Argoverse 2 Scene Flow Challenge
- Link/identifier: arXiv:2407.07995
- Access level: abstract/preprint only
- Problem: Improve LiDAR scene flow accuracy and efficiency by fusing multiple (5) point clouds temporally through a full 4D voxel network, while keeping real-time speed.
- Representation: 4D voxel grid (space + time), fused after a 3D intra-voxel feature encoder.
- Resolution strategy: Fixed voxel resolution; the "Spatio-Temporal Decomposition Block" (STDB, combining 3D + 1D convolutions instead of full 4D convolutions) is a computational-efficiency mechanism, not a spatial-resolution-adaptation mechanism.
- Adaptive mechanism categor(y/ies): None — fixed resolution, not adaptive.
- Perception method: Learned — 4D voxel network with a factorized (3D+1D) convolution block for efficiency.
- Terrain handling: Not applicable.
- Dynamic-object handling: Dense per-point/per-voxel 3D motion field (scene flow) across a 5-frame temporal window — a rich but object-agnostic dynamic-motion representation (not explicit object detection/tracking).
- Temporal processing: DIRECT EVIDENCE: explicitly fuses 5 point clouds (more temporal context than typical frame-pair flow methods), citing this as a source of the reported accuracy gain.
- Uncertainty handling: Not reported.
- Computational characteristics: DIRECT EVIDENCE: 45.9% higher performance than prior state of the art while running in real-time; 15.1 FPS on an NVIDIA RTX 3090 GPU.
- Datasets: Argoverse 2 (winner of the 2024 Scene Flow Challenge on this dataset).
- Evaluation: Argoverse 2 Scene Flow Challenge metrics (standard scene-flow EPE-style metrics; exact numeric breakdown not confirmed from accessible text).
- Limitations: Not confirmed from accessible text.
- Relevance to SIH problem: A current (RA-L 2025), competition-winning example of temporal LiDAR perception (multi-frame 4D voxel fusion) for motion estimation — on fixed voxel resolution, with efficiency gained via convolution factorization rather than spatial-resolution adaptation. Good evidence that even the most compute-conscious scene-flow work is not reaching for adaptive resolution as its efficiency lever.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/venue/FPS/performance-gain figures/challenge win.

### SemanticFlow: A Self-Supervised Framework for Joint Scene Flow Prediction and Instance Segmentation in Dynamic Environments
- Authors: Yinqi Chen, Meiying Zhang, Qi Hao, Guang Zhou
- Year: 2025
- Venue: arXiv preprint (venue beyond arXiv not confirmed)
- Link/identifier: arXiv:2503.14837
- Access level: abstract/preprint only
- Problem: Jointly predict scene flow AND instance segmentation of full-resolution point clouds, for robust motion + object-instance understanding in dynamic traffic scenes.
- Representation: Full-resolution point cloud (explicitly avoids downsampling to a coarser grid for the final output).
- Resolution strategy: IMPORTANT NUANCE (same caveat as PointPWC-Net above): the paper uses a "coarse-to-fine prediction based multi-task scheme," where an initial coarse background/dynamic-object segmentation provides context that is then refined into full-resolution motion + semantic output. This is a coarse-to-fine *prediction refinement* pipeline (multi-stage inference), not a spatially variable, persistent *map* representation.
- Adaptive mechanism categor(y/ies): Adaptive neural computation (coarse-to-fine multi-task refinement) — NOT adaptive map resolution.
- Perception method: Learned, self-supervised, multi-task (scene flow + instance segmentation jointly, sharing a feature-processing module).
- Terrain handling: Not applicable.
- Dynamic-object handling: DIRECT EVIDENCE: explicit coarse static-background vs. dynamic-object segmentation as an initial stage, refined into full instance segmentation + scene flow — genuinely joint dynamic-object + motion perception.
- Temporal processing: Not confirmed in detail from accessible text (frame-pair or short window, consistent with scene-flow task convention — INFERENCE).
- Uncertainty handling: Not reported.
- Computational characteristics: Not confirmed from accessible text ("computational efficiency" claimed qualitatively as one of the reported improvement areas).
- Datasets: Waymo Open Dataset and Argoverse 2.
- Evaluation: DIRECT EVIDENCE: 8.7–65.5% improvement in scene flow estimation and 3.6–11.9% increase in segmentation accuracy across key metrics (exact metric names not confirmed from accessible text — the percentages themselves are as reported in the accessible summary).
- Limitations: Not confirmed from accessible text.
- Relevance to SIH problem: The most recent (2025) joint scene-flow + instance-segmentation system found — again illustrates that "coarse-to-fine" in this literature almost always means multi-stage *prediction* refinement, not spatially variable *map* resolution, which is a critical terminology distinction for this project going forward.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/datasets/reported improvement percentages; INFERENCE for temporal-processing details.

### PointRNN: Point Recurrent Neural Network for Moving Point Cloud Processing
- Authors: Hehe Fan, Yi Yang
- Year: 2019
- Venue: arXiv preprint (widely cited foundational work; used as a baseline/building block in later point-cloud sequence literature)
- Link/identifier: arXiv:1910.08287
- Access level: abstract/preprint only
- Problem: Process sequences of moving/orderless point clouds recurrently, maintaining a state (coordinates + features) over time, to predict future point-cloud motion.
- Representation: Raw point sets (no grid/voxelization); a point-based spatiotemporally-local correlation mechanism aggregates features/states across time by searching k-nearest-neighbors in the previous time step.
- Resolution strategy: N/A — point-based, no grid resolution concept applies.
- Adaptive mechanism categor(y/ies): N/A — no map/grid representation to be adaptive or fixed.
- Perception method: Learned — recurrent architecture (PointRNN, plus PointGRU and PointLSTM variants).
- Terrain handling: Not applicable.
- Dynamic-object handling: Predicts future point-level trajectories from history — a foundational form of dynamic/motion modeling, though at the raw-point level rather than object level.
- Temporal processing: DIRECT EVIDENCE: this is a foundational sequence/recurrent model specifically for moving point clouds — one of the earliest (2019) examples of applying RNN-style recurrence directly to unordered 3D point sets over time.
- Uncertainty handling: Not reported.
- Computational characteristics: Not confirmed from accessible text.
- Datasets: Not confirmed from accessible text (synthetic moving-point-cloud data per general knowledge of this line of work — HYPOTHESIS-level, not confirmed here).
- Evaluation: Not confirmed from accessible text.
- Limitations: INFERENCE — point-level (not object-level) motion prediction; likely fragile under noisy/sparse real LiDAR returns compared to the synthetic/dense settings such point-recurrent methods are often first validated on.
- Relevance to SIH problem: Foundational lineage for the "temporal LiDAR perception" family — establishes that recurrent processing of raw (non-gridded) point sequences predates and runs alongside the grid/voxel-based DOGMa and BEV lineages, with no resolution-adaptivity question applicable since there is no grid.
- Evidence level(s) for key claims: WEB VERIFIED for authorship/architecture description/variants.

### Multi-Resolution 3D Mapping with Explicit Free Space Representation for Fast and Accurate Mobile Robot Motion Planning
- Authors: Nils Funk, Juan Tarrio, Sotiris Papatheodorou, Marija Popovic, Pablo F. Alcantarilla, Stefan Leutenegger
- Year: 2021 (arXiv:2010.07929), RA-L
- Venue: IEEE Robotics and Automation Letters (RA-L)
- Link/identifier: arXiv:2010.07929
- Access level: abstract/preprint only
- Problem: Fast, accurate motion-planning-oriented 3D mapping that explicitly represents free space (not just occupied/unknown), using adaptive-resolution volumetric mapping integrated with an octree.
- Representation: Occupancy probabilities (log-odds) in an octree, NOT a TSDF — explicitly chosen so that free space can be represented as well as surfaces.
- Resolution strategy: DIRECT EVIDENCE: genuinely adaptive/variable resolution — "the concept of adaptive-resolution volumetric mapping, which naturally integrates with the hierarchical decomposition of space in an octree data structure," with resolution chosen on the fly in real time via multi-scale max-min pooling of the input depth image.
- Adaptive mechanism categor(y/ies): **Adaptive map resolution** — this is one of the few papers found in this entire search where the persistent map/grid structure itself genuinely has spatially varying resolution, chosen automatically per region.
- Perception method: Classical geometric mapping (occupancy log-odds octree), not learned.
- Terrain handling: Not a dedicated focus (general 3D obstacle/free-space mapping for motion planning, not terrain-classification-specific).
- Dynamic-object handling: **None found.** No moving-object detection, tracking, segmentation, or velocity estimation of any kind is mentioned in any accessible source for this paper — it targets static/quasi-static environment mapping for motion planning.
- Temporal processing: Standard incremental map integration as new depth frames arrive; no explicit dynamic-object-aware temporal filtering (e.g., no mechanism to distinguish "this became free because an object moved away" vs. sensor noise, unlike the STVL paper above).
- Uncertainty handling: Log-odds occupancy probability representation (standard probabilistic occupancy mapping).
- Computational characteristics: Reported to enable collision queries "at unprecedented speed," per the paper's own framing (exact numbers not confirmed from accessible text).
- Datasets: Not confirmed from accessible text.
- Evaluation: Not confirmed from accessible text (motion-planning/collision-query speed and map accuracy per the paper's stated goals).
- Limitations: DIRECT EVIDENCE (by omission): the paper's own scope is static/free-space mapping for planning — it does not claim to address dynamic objects at all.
- Relevance to SIH problem: **This is the cleanest example found in this entire search of genuine adaptive map resolution existing as a mature, real-time, real-world (RA-L) capability — but entirely decoupled from dynamic-object perception.** It is presented here specifically as a control/contrast case: it demonstrates that the "adaptive resolution" half of H2's claim is not itself rare or exotic in the mapping literature; what is rare is combining it with dynamic-object perception, which is the actual, narrower gap this search was trying to disprove or confirm.
- Evidence level(s) for key claims: WEB VERIFIED (via search-indexed summary) for adaptive-resolution mechanism, representation choice (log-odds octree vs. TSDF), and absence of any dynamic-object content.

### On Exploring Input Resolution Scaling For Anytime LiDAR Object Detection ("MURAL")
- Authors: Ahmet Soyyigit, Shuochao Yao, Heechul Yun
- Year: 2026 (arXiv, submitted July 2026)
- Venue: arXiv preprint (not yet published in a traditional venue as of access)
- Link/identifier: arXiv:2607.08391 (this paper itself proposes the method referred to as "MURAL" in earlier search-result summaries)
- Access level: preprint, partial full-text (HTML) read — this paper received the deepest verification pass in this search, including direct quotes and numeric results pulled from the rendered HTML, not just the abstract.
- Problem: Enable "anytime computing" for LiDAR 3D object detection in cyber-physical systems — trading off detection latency against accuracy to meet dynamic, per-invocation timing deadlines (e.g., tighter deadlines as the ego-vehicle speeds up).
- Representation: Point clouds encoded as pillars (PointPillars/PillarNet-style) or voxels (CenterPoint-style); the method is demonstrated across both families.
- Resolution strategy: DIRECT EVIDENCE, precisely characterized: resolution scaling is **spatially uniform across the whole scene for a given inference**, adjusting the pillar/voxel size (Vx, Vy) globally per invocation, and is instead **adaptive over time/deadline**, not adaptive over space within one frame. A secondary "region dropping" fallback (cropping the dense input tensor) exists for voxel models under very tight deadlines, but this is described as a fallback, not the primary mechanism. This is the single most important nuance for this project's H2 verdict (see below).
- Adaptive mechanism categor(y/ies): **Adaptive neural computation** (a single trained model, deployed once, whose input resolution and therefore compute cost is dynamically scaled per invocation based on a deadline scheduler) — explicitly NOT adaptive map resolution in the spatially-variable-within-a-scene sense this project's H2 is testing for.
- Perception method: Learned — a single DNN (PillarNet, PointPillars, or CenterPoint backbone) made "resolution-aware" via multi-resolution training with shared weights and resolution-aware batch normalization, plus post-training pillar-size synthesis and a deadline-aware runtime scheduler.
- Terrain handling: Not applicable.
- Dynamic-object handling: DIRECT EVIDENCE, and the key nuance: the detector itself performs **single-frame 3D bounding-box detection only** (of nuScenes object classes, which include inherently dynamic-capable categories such as cars and pedestrians — exact class list not enumerated in accessible text). Velocity estimation and a Kalman-filter-based tracker are used in the paper's **closed-loop driving experiments**, but DIRECT EVIDENCE confirms these are downstream, classical (non-learned, non-resolution-adaptive) components layered on top of MURAL's per-frame detections — i.e., MURAL's own adaptive-resolution mechanism does not itself discriminate moving from static objects or estimate motion; that happens afterward, in a conventional DATMO-style tracking stage.
- Temporal processing: Per-frame detection; temporal continuity is handled entirely by the downstream Kalman-filter tracker, not by MURAL's detector/resolution-scaling mechanism itself.
- Uncertainty handling: Not reported as a distinct mechanism (deadline scheduling uses predicted execution time, not perceptual uncertainty).
- Computational characteristics: DIRECT EVIDENCE (quoted numbers from HTML fetch), PillarNet on Jetson AGX Orin, open-loop: at 0.100² m² pillar size, mAP 0.564 / ~248 ms latency; at 0.128² m², mAP 0.560 / ~172 ms; at 0.200² m², mAP 0.499 / ~100 ms. Closed-loop (Dense Urban scenario): 36.1 s completion time vs. 31.7 s at finest fixed resolution. Closed-loop (Dynamic Hazard scenario): 0/30 collisions at 174.4 ms average latency.
- Datasets: nuScenes (700 training scenes, 75 validation scenes).
- Evaluation: mAP, execution latency (ms), collision counts, completion time, false positive rate; compared against Anytime-LiDAR (prior early-exit + detection-head-scheduling method) and VALO (a forecasting-reliant anytime baseline), outperforming both, particularly VALO under tight deadlines where VALO's reliance on forecasted detections (from processing only a small fraction of input) breaks down.
- Limitations: DERIVED — the resolution adaptation is global/per-frame, not spatially concentrated (e.g., not finer near the ego-vehicle and coarser far away within a single frame); the dynamic-vs-static/tracking capability is entirely bolted on downstream, not part of the adaptive-resolution mechanism itself.
- Relevance to SIH problem: **The closest near-miss for H2 found in this search, and reported prominently per the task instructions.** MURAL genuinely combines (a) a resolution-adaptive learned perception component and (b) a full pipeline (via downstream tracking) that produces dynamic-object outputs (velocity, tracked identity) for inherently dynamic-capable object classes, validated in closed-loop driving scenarios explicitly named "Dynamic Hazard." However, it does NOT satisfy H2's implied stricter reading — a single system where the *same* mechanism that adapts resolution also does the dynamic-object discrimination, and where the adaptation is spatially variable within a scene rather than uniform-but-time-varying. Given the SIH problem's own framing (fine resolution near the robot, coarser farther away — a *spatial* pattern), MURAL's temporal/global resolution scaling is a materially different mechanism from what H2 is really asking about, and this distinction should not be blurred.
- Evidence level(s) for key claims: WEB VERIFIED (direct HTML fetch, quotes and numbers extracted from rendered paper text, not just search snippets) for resolution-scaling mechanism, dynamic-object/tracking architecture split, and all quantitative results reported above.

### AdaOcc: Adaptive-Resolution Occupancy Prediction
- Authors: Chao Chen, Ruoyu Wang, Yuliang Guo, Cheng Zhao, Xinyu Huang, Chen Feng, Liu Ren
- Year: 2024
- Venue: arXiv preprint (affiliations per search-indexed summary: New York University and Bosch Research North America — REDUCED CONFIDENCE, not independently verified from primary text, since the PDF full-text fetch failed and only search-result summaries plus the arXiv abstract page were accessible)
- Link/identifier: arXiv:2408.13454
- Access level: abstract/preprint only — flagged reduced-confidence; a direct PDF full-text fetch attempt failed (binary/unparseable content returned), and a secondary summary-page fetch was blocked by a rate limit, so all claims below rest on the arXiv abstract and independent search-engine summaries only, not a full-text read.
- Problem: Dense 3D occupancy prediction around a vehicle faces a resolution/compute trade-off — uniformly high-resolution grids are accurate but expensive; uniformly low-resolution grids are cheap but lack detail, especially for close-range scene understanding.
- Representation: A hybrid of a holistic occupancy grid (coarser, whole-scene) plus point-cloud-based object-centric 3D reconstruction in regions of interest (ROIs) — the ROI detail is represented as point clouds specifically so it is not constrained by the grid's predefined resolution.
- Resolution strategy: DIRECT EVIDENCE (from the abstract): genuinely spatially variable within a single scene — "performing highly detailed and precise 3D reconstruction only in regions of interest (ROIs)" while the rest of the occupancy grid remains coarser. This is a real example of an adaptive/spatially-variable persistent representation, not merely a multi-scale feature-computation trick.
- Adaptive mechanism categor(y/ies): **Adaptive map resolution / adaptive computational representation** (the ROI-vs-background split is spatially variable and persists as the output representation, not just an intermediate network feature) — this is the strongest candidate found in this search for the "adaptive map resolution" half of H2.
- Perception method: Learned — "multi-modal" prediction approach per the abstract; exact sensor modality (camera-only, LiDAR-only, or camera+LiDAR fusion) could NOT be confirmed from any accessible source in this search, despite a dedicated follow-up search attempt — this is an explicit, acknowledged gap, not a guess.
- Terrain handling: Not confirmed from accessible text.
- Dynamic-object handling: **NOT CONFIRMED — this is the critical gap for H2.** The abstract and all accessible summaries describe ROIs as "object-centric" but do not state that the objects driving ROI placement are specifically moving/dynamic objects (as opposed to any detected foreground object, static or not), and no motion classification, tracking, or velocity estimation is mentioned anywhere in the accessible text. Given the SIH project's own framing that vehicles/pedestrians count as the "dynamic objects" of interest for object detection, it is plausible (INFERENCE only) that AdaOcc's ROIs are frequently vehicle detections and therefore touch dynamic-capable classes — but this is inference, not a demonstrated dynamic-object-perception capability (no evidence of moving-vs-static discrimination, tracking, or scene flow).
- Temporal processing: Not confirmed from accessible text; the framing (per-scene 3D reconstruction accuracy vs. baselines) suggests single-frame evaluation, but this is not directly confirmed.
- Uncertainty handling: Not reported.
- Computational characteristics: Not confirmed from accessible text (the paper's contribution is framed as an accuracy/detail improvement, not an explicit runtime/FPS claim, in everything accessible here).
- Datasets: nuScenes, evaluated in both close-range and long-range scenarios.
- Evaluation: DIRECT EVIDENCE: over 13% IoU improvement and over 40% Hausdorff-distance improvement vs. previous baselines in close-range scenarios.
- Limitations: Explicitly acknowledged here as a reporting limitation of this literature search, not of the paper itself: sensor modality and any dynamic-object-specific claims could not be verified from accessible text after repeated attempts (direct PDF fetch failed with unparseable binary content; a follow-up summary-page fetch was blocked by rate limiting).
- Relevance to SIH problem: **Reported prominently, per the task instructions, as the strongest candidate found for the "adaptive map resolution" half of H2** — genuinely spatially variable, object-centric persistent representation, close-range-vs-long-range validated on nuScenes. It is NOT reported as a confirmed disproof of H2, because the "dynamic-object perception" half (motion/tracking/velocity, as opposed to generic object-centric detail) could not be verified from any source accessed in this search. A full-text read of the PDF (which is saved locally from the failed fetch attempt, at the path reported by the tool during this session) is recommended as a priority follow-up before treating this as either evidence for or against H2.
- Evidence level(s) for key claims: WEB VERIFIED (arXiv abstract page + multiple independent search-engine summaries, cross-checked) for the adaptive-resolution/ROI mechanism, dataset, and IoU/Hausdorff figures; explicitly UNVERIFIED (not merely inferred, but flagged as an open gap) for sensor modality and any dynamic-object-specific claim.

---

## Hypothesis Verdict

### H2: "No existing work combines dynamic-object perception with adaptive resolution"
- **Verdict: Weakened — not disproved, not fully survived.**

Justification: Of the ~23 papers examined in depth across all five assigned families (dynamic occupancy
grids, dynamic LiDAR perception, LiDAR motion segmentation, LiDAR scene flow, temporal LiDAR
perception), the overwhelming majority — including modern (2022–2025) learned dynamic occupancy grids
with rich semantic+velocity output (Jang et al. 2024; Schreiber et al. 2022), the founding and current
state-of-the-art LiDAR moving-object-segmentation lineage (LMNet 2021, 4DMOS 2022, MambaMOS 2024,
SegNet4D 2025), and the founding and current state-of-the-art scene-flow lineage (PointPWC-Net 2020,
SeFlow 2024, Flow4D 2025, SemanticFlow 2025) — use **fixed spatial resolution**. This is a clear,
repeated, direct finding, not an assumption: none of these papers describe or claim any mechanism by
which their map/grid/voxel resolution varies spatially across the scene. Where "coarse-to-fine" or
"multi-scale" language does appear (PointPWC-Net, SemanticFlow), it refers to a hierarchical
feature-computation or multi-stage-refinement pattern internal to a single inference pass, not a
persistent, spatially variable map representation — a distinction this document makes explicit
precisely because it would be easy to over-credit H2's disproof by conflating the two.

However, two 2024–2026 papers came close enough to H2's combination that they must be reported
prominently rather than folded into the "survived" pile:

1. **AdaOcc (Chen et al., 2024, arXiv:2408.13454)** is the strongest candidate for the "adaptive
   resolution" half: it genuinely produces a spatially variable persistent representation (fine,
   point-cloud-based detail in object-centric ROIs; coarser occupancy grid elsewhere), validated on
   nuScenes with substantial IoU/Hausdorff gains. What could **not** be confirmed, despite a dedicated
   search and two failed full-text-access attempts, is whether the "dynamic-object perception" half is
   actually satisfied — i.e., whether AdaOcc's ROIs are specifically tied to moving/dynamic objects
   (with any motion classification, tracking, or velocity signal) or simply to any detected foreground
   object regardless of motion state. This is reported as an open, unresolved lead, not a confirmed
   counterexample.

2. **MURAL / "On Exploring Input Resolution Scaling For Anytime LiDAR Object Detection"
   (Soyyigit, Yao, Yun, 2026, arXiv:2607.08391)** is the strongest candidate for the "dynamic-object
   perception" half in combination with *some* form of resolution adaptivity: it dynamically scales
   LiDAR pillar/voxel resolution to meet timing deadlines, and — via a downstream, non-learned,
   non-resolution-adaptive Kalman-filter tracker — produces genuine dynamic-object tracking, explicitly
   validated in a closed-loop scenario named "Dynamic Hazard." However, on close reading (this paper
   received a full-text HTML fetch, not just an abstract read), its resolution adaptation is
   **spatially uniform within any single frame and adaptive over time/deadline instead** — the opposite
   spatial pattern from what the SIH problem statement (and, by extension, H2) is actually asking about
   (fine near the robot, coarse farther away, within one frame). Its dynamic-object capability is also
   architecturally separate from its resolution-adaptive component, not unified with it.

No paper found in this search unambiguously satisfies **both** halves of H2's criterion within a
**single, unified mechanism**: a system that both (a) genuinely discriminates, tracks, segments, or
estimates the motion of dynamic objects, and (b) does so using or alongside a spatially variable
persistent map/grid/voxel resolution. The pattern observed — adaptive resolution work (Funk et al.
2021 being the cleanest pure example) and dynamic-object-perception work developing along largely
separate, parallel tracks, with only recent (2024–2026) papers starting to touch both — supports
**"Weakened"** rather than **"Survived"**: the absence looks like an unaddressed integration
opportunity rather than a fundamental incompatibility, and the pieces are visibly converging. It does
not support **"Disproved"**, because no single confirmed counterexample was found despite genuinely
adversarial, mandatory-alternate-terminology-inclusive searching across 48 distinct queries.

DynORecon (Wang et al., 2024/2025, arXiv:2409.19928) is flagged separately as an unresolved lead worth
a follow-up full-text read: it performs genuine per-object dynamic reconstruction from Dynamic SLAM,
using an unspecified volumetric representation whose resolution strategy could not be determined from
any accessible source in this search.

---

## Terminology/Concept Notes

- **Sparse ≠ adaptive/variable resolution.** Multiple papers in this search (4DMOS's sparse 4D
  convolutions; the Spatio-Temporal Voxel Layer's OpenVDB-backed sparse grid) achieve large
  efficiency gains by only storing/processing *occupied* cells at a single, uniform resolution. This
  is a different mechanism from a map whose cell size itself varies by location (e.g., fine near the
  robot, coarse far away, or fine near detected objects). Both reduce compute, but only the latter is
  "adaptive resolution" in the sense this project's CLAUDE.md and H2 are using the term. Conflating
  the two would make H2 trivially false (sparsity is everywhere in this literature) in a way that
  would not reflect the actual research question.

- **"Coarse-to-fine"/"multi-scale" inside a single inference pass ≠ adaptive map resolution.**
  PointPWC-Net's feature pyramid and SemanticFlow's coarse-to-fine multi-task refinement are both
  standard hierarchical-computation patterns (analogous to a feature-pyramid network) applied to
  produce a single, uniform-resolution final output. They do not leave behind a spatially variable
  persistent representation. This is the single most common false-positive pattern encountered while
  searching for H2 counterexamples using the mandatory "coarse-to-fine" search term, and is worth
  flagging explicitly for whoever consolidates this Group's findings with the other search groups.

- **Temporal/deadline-adaptive resolution ≠ spatially adaptive resolution.** MURAL adapts input
  resolution over time (per inference, based on a latency deadline) but uniformly across the whole
  scene within any one inference. The SIH problem statement's example (fine near the robot,
  progressively coarser farther away) is a *spatial* pattern. These are genuinely different mechanisms
  that both get called "adaptive resolution" in the literature and in casual search results; this
  project should keep them distinct when synthesizing across all research groups.

- **General object detection of dynamic-capable classes (cars, pedestrians) vs. explicit
  dynamic/motion perception.** Several near-miss papers (MURAL, possibly AdaOcc) detect objects whose
  real-world classes are capable of movement (cars, pedestrians) without the detector itself
  discriminating moving from static instances or estimating motion. This project's own CLAUDE.md frames
  "object detection — static and dynamic objects such as ... pedestrians and vehicles" as one task,
  which is a looser bar than "dynamic-object perception" as used in H2 (which implies actually
  perceiving *that* something is moving and *how*, e.g., via segmentation, tracking, or scene flow).
  Both readings are legitimate depending on how strictly H2 is meant to be interpreted; this document
  reports findings under the stricter reading and flags where the looser reading would change the
  verdict (MURAL, in particular, would arguably satisfy the looser reading given its closed-loop
  Kalman-tracker pipeline).

- **DATMO is the classical ancestor of "dynamic-object perception."** The term predates deep learning
  and originally referred to grid-based/model-based/model-free pipelines for detecting and tracking
  moving obstacles (Llamazares et al. 2020 review); modern LiDAR-MOS, scene-flow, and dynamic-DOGMa
  work are direct intellectual descendants of this line, generally replacing hand-designed detection/
  tracking stages with learned, per-point or per-cell dynamic classification.

---

## Papers Considered But Excluded

The following papers surfaced during searches but were not analyzed in depth above, generally because
they were secondary/duplicate results relative to a more central paper already covered, or because
initial searches suggested they were lower-priority for the specific H2 stress-test. They are listed
here for completeness and as leads for a follow-up pass if deeper Group D coverage is later requested:

- KDMOS: Knowledge Distillation for Motion Segmentation (2025) — efficiency-distillation variant of the LiDAR-MOS line.
- BEVMOSNet: Multimodal Fusion for BEV Moving Object Segmentation (2025).
- CV-MOS: A Cross-View Model for Motion Segmentation (2024).
- MF-MOS, SSF-MOS, MV-MOS, MotionBEV — additional 2024 LiDAR-MOS variants surfaced in search results but not independently verified.
- Unsupervised 4D LiDAR Moving Object Segmentation in Stationary Settings with Multivariate Occupancy Time Series (Kreutz et al., WACV 2023) — unsupervised MOS for static-sensor settings; different problem framing (stationary LiDAR, not a moving robot/vehicle) from this project's scope.
- D-PLS: Decoupled Semantic Segmentation for 4D-Panoptic-LiDAR-Segmentation (2025); Mask4Former (2023); 4D Panoptic LiDAR Segmentation / Dynamic Shifting Network (2021/2022) — 4D panoptic segmentation lineage, relevant to "LiDAR panoptic segmentation dynamic" mandatory term but not deeply analyzed here due to time constraints.
- DoGFlow (2025), UniFlow (2025), CMU-Flownet (2024), DELFlow (2023) — additional scene-flow variants; DoGFlow specifically notable for using 4D radar Doppler as a cross-modal label source for LiDAR flow, a different adaptivity axis (sensor fusion) than resolution.
- LEF: Late-to-Early Temporal Fusion for LiDAR 3D Object Detection (Waymo, 2023/2024) and TimePillars (2023) — temporal-fusion 3D object detection, fixed resolution, adjacent to but not core to the five assigned families.
- Anytime-LiDAR (2022, arXiv:2208.12181) and VALO — prior anytime/deadline-aware LiDAR detection baselines directly compared against by MURAL; not independently deep-dived since MURAL's own paper already reports their comparison.
- OctreeOcc, OctOcc — octree-based occupancy prediction papers surfaced under the octree/hierarchical search; appear to be camera-centric occupancy-prediction efficiency work rather than dynamic-object-focused, not deep-dived.
- A-OctoMap; ECO: Incremental Ego-Centric Octree Update for Point Streams — adaptive/incremental octree mapping systems surfaced under the hierarchical-structure search; not confirmed to address dynamic objects, not deep-dived given time constraints.
- Dynamic Occupancy Grids for Object Detection: A Radar-Centric Approach (arXiv:2402.01488) — excluded as primarily radar-centric rather than LiDAR-centric, though conceptually adjacent to the DOGMa family.
- Probabilistic quadtrees for variable-resolution mapping of large environments — classic (pre-2020) quadtree-based adaptive-resolution mapping; relevant to "adaptive map resolution" lineage generally but not found to address dynamic objects; not deep-dived given the stronger, more recent Funk et al. (2021) example already covered.
