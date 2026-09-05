# External Literature — Group B: Attention/Foveated, Uncertainty & Risk-Aware, Real-Time/Resource-Constrained

**Assigned families:** Foveated/attention-based LiDAR representations; uncertainty-aware mapping; risk-aware spatial representations; real-time/resource-constrained LiDAR mapping and perception.
**Assigned hypotheses to stress-test:** H3 ("semantic-aware adaptive resolution may be an unexplored opportunity"), H5 ("adaptive map resolution can provide meaningful computational/memory benefits").

**Access-tooling caveat (applies to the whole file):** all sources below were located via WebSearch and then verified via WebFetch against the arXiv/publisher page. In most cases the fetch tool successfully returned clean abstract-page text; in several cases the fetch tool was pointed at a raw PDF binary and could only parse fragments (noted per-paper as reduced confidence), and a few publisher pages (ACM DL, Springer/IDP, one journal) returned 403/redirect-to-login and could not be read at all (noted as "abstract/snippet only via search" or excluded). No paper below is described from search-snippet text alone without that being explicitly flagged.

---

## Searches Conducted

1. foveated LiDAR perception saliency-aware scanning robot 2024
2. attention-guided point cloud downsampling efficient 3D object detection
3. active perception next-best-view LiDAR mobile robot 2023 2024
4. uncertainty-aware occupancy grid mapping LiDAR robot
5. evidential deep learning LiDAR occupancy mapping uncertainty
6. risk-aware terrain traversability mapping autonomous ground vehicle
7. real-time embedded LiDAR SLAM resource-constrained platform
8. anytime perception algorithm robotics computation budget
9. foveated vision classic active perception biologically inspired sensing
10. Bayesian occupancy grid Elfes Thrun uncertainty classic robotics
11. Gaussian process occupancy mapping uncertainty continuous representation robot
12. risk-aware spatial representation motion planning cost map autonomous vehicle
13. conditional computation early-exit dynamic network point cloud LiDAR efficient
14. edge device LiDAR 3D object detection latency embedded GPU real-time 2024
15. region of interest ROI LiDAR point cloud processing autonomous driving efficient
16. semantic uncertainty aware mapping robot 2024 2025 confidence occupancy
17. STEP Stochastic Traversability Evaluation and Planning risk-aware off-road navigation arxiv
18. "space-variant" OR foveated robotic vision survey resource-constrained review open access pdf
19. Zhanteng Xie stochastic occupancy grid map prediction dynamic scenes CoRL 2023
20. content-aware 3D object detection embedded GPUs mobisys 2025
21. solid-state LiDAR region of interest adaptive scan pattern MEMS foveated hardware
22. conditional value at risk CVaR occupancy map robot navigation uncertainty
23. embedded Jetson real-time LiDAR semantic segmentation point cloud latency benchmark 2024 2025
24. adaptive resolution point cloud does not reduce computation overhead evaluation
25. FOVEA foveated image magnification autonomous navigation arxiv
26. Agile3D arxiv Wang Liu Bagchi Xu Chaterji 3D object detection embedded GPU
27. Gaussian Process Occupancy Maps O'Callaghan Ramos ICRA 2012 abstract

Each substantive lead was followed by a direct WebFetch of the arXiv abstract page, publisher page, GitHub README, or a press release, so claims below are grounded in that fetched text rather than raw search snippets, except where a paper is explicitly marked "abstract/snippet only."

---

## Papers

### FOVEA: Foveated Image Magnification for Autonomous Navigation
- Authors: Chittesh Thavamani, Mengtian Li, Nicolas Cebron, Deva Ramanan (CMU / Argo AI)
- Year: 2021
- Venue: ICCV 2021
- Link/identifier: arXiv:2108.12102
- Access level: abstract read in full (verbatim), via arXiv abstract page
- Problem: High-res video must be downsampled for real-time autonomous-driving perception, but naive downsampling destroys small/distant objects.
- Representation: 2D camera image, differentiably resampled into a fixed-size "magnified" canvas (not LiDAR).
- Resolution strategy: **Variable/content-driven** — a differentiable warping layer allocates more output pixels ("foveal magnification") to salient regions, driven by "cheap... dataset-specific spatial priors or temporal priors computed from object predictions in the recent past" — i.e., saliency/task-relevance, not raw sensor distance.
- Adaptive mechanism categor(y/ies): **Adaptive attention/ROI** (a learned/rule-driven warp reallocates processing resolution before the detector runs); not a persistent map.
- Perception method: Learned — differentiable resampling + standard object detector (Faster R-CNN), trained end-to-end including the backward unmapping of predictions.
- Terrain handling: Not addressed.
- Dynamic-object handling: Indirect — temporal saliency prior uses "object predictions in the recent past," implicitly favoring regions with recently-seen moving objects.
- Temporal processing: Yes, for the temporal-prior saliency cue only, not for map persistence.
- Uncertainty handling: Not addressed.
- Computational characteristics (DIRECT, verbatim): small-object detection accuracy improved "by over 2x" without harming large-object accuracy; streaming-AP metric rose "from 17.8 to 23.0 on a GTX 1080 Ti GPU," with gains stated as achieved "without any noticeable increase in compute."
- Datasets: Argoverse-HD, BDD100K.
- Evaluation: Streaming-accuracy-under-latency benchmark (streaming AP), small-vs-large object AP breakdown.
- Limitations: Not enumerated in the accessible text; abstract does not discuss failure modes.
- Relevance to SIH problem: **This is the single clearest piece of evidence bearing on H3.** It is a fully worked, quantitatively validated, saliency/task-driven variable-resolution perception pipeline from 2021 — i.e., "content-aware adaptive resolution" is not a novel idea in perception generally. It is camera-only, so it does not by itself disprove a LiDAR-specific or map-persistent version of H3, but it establishes that the general mechanism (reallocate resolution by content/saliency rather than distance) has prior art with measured benefit.
- Evidence level(s): DIRECT for mechanism and all quantitative claims (verbatim abstract); INFERENCE that the principle "could" transfer to LiDAR range images (not stated by the authors — the fetched text explicitly says the paper contains no mention of LiDAR or cross-modal applicability).

### Adaptive Fovea for Scanning Depth Sensors
- Authors: Zaid Tasneem, Charuvahan Adhivarahan, Dingkang Wang, Huikai Xie, Karthik Dantu, Sanjeev J. Koppal
- Year: 2020
- Venue: The International Journal of Robotics Research (IJRR)
- Link/identifier: DOI 10.1177/0278364920920931
- Access level: **snippet only** — publisher page returned HTTP 403; findings below are drawn from the WebSearch result snippet, not a verified full read. Flagged low-confidence per this project's rules.
- Problem: Fixed uniform-resolution depth/LiDAR-like scanning wastes sensing bandwidth on unimportant regions; biological eyes instead foveate.
- Representation: Sparse/variable-density range data produced directly by the scanning hardware.
- Resolution strategy: Variable, hardware-level — an external signal drives the sensor to "zoom into" a region of interest, changing the physical scan pattern in real time (SPAD-based scanning depth sensor).
- Adaptive mechanism categor(y/ies): **Adaptive sensor acquisition** (the sensor's own scan pattern changes) — this is squarely the "physical sensor/scan pattern changes" category, not a map or software mechanism.
- Perception method: Not detailed at snippet level.
- Terrain/dynamic-object/temporal handling: Not established from the snippet.
- Uncertainty handling: Not established from the snippet.
- Computational characteristics: Not established from the snippet (reported benefit is qualitative: reduced "raw photon data that needs storage and transfer").
- Datasets/Evaluation: Not established from the snippet.
- Limitations: Not established (access failure).
- Relevance to SIH problem: Establishes that hardware-level foveated/adaptive-acquisition depth sensing is an actively studied idea distinct from software/map-side adaptive resolution — important for keeping the "adaptive sensing" vs. "adaptive map representation" distinction sharp per this project's rules. Confidence intentionally kept low pending a full read.
- Evidence level(s): WEB VERIFIED only that the paper exists and its title/venue/general topic match; all technical detail above is SNIPPET-ONLY / reduced confidence.

### Towards a MEMS-based Adaptive LIDAR
- Authors: Francesco Pittaluga, Zaid Tasneem, Justin Folden, Brevin Tilmon, Ayan Chakrabarti, Sanjeev J. Koppal
- Year: 2020
- Venue: International Conference on 3D Vision (3DV) 2020
- Link/identifier: arXiv:2003.09545
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Fixed raster/uniform LiDAR scanning cannot concentrate measurement density where it is most needed; the paper proposes hardware that can.
- Representation: Native sensor-level sparse depth measurements with a dynamically reconfigurable scan pattern (not a post-hoc processed map).
- Resolution strategy: Variable, hardware-level — a scanning MEMS mirror is driven to realize "dynamically specified measurement patterns" rather than a fixed raster.
- Adaptive mechanism categor(y/ies): **Adaptive sensor acquisition** (physical MEMS mirror scan pattern).
- Perception method: A CNN-based depth-map completion network fills in the sparse adaptively-sampled measurements — learned post-processing, but the acquisition-pattern control itself is not stated to be learned in the accessible abstract.
- Terrain/dynamic-object/temporal handling: Not addressed in the abstract.
- Uncertainty handling: Not addressed.
- Computational characteristics: Not reported numerically; validated on "over 75 static and dynamic scenes."
- Datasets/Evaluation: Custom captured scenes (prototype hardware), no public benchmark named.
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: A second, independent hardware-adaptive-acquisition LiDAR example (alongside the Tasneem et al. IJRR paper above), reinforcing that "adaptive sensing" at the physical scan-pattern level is an established research thread separate from adaptive map/computation representation — relevant boundary-drawing for the SIH's "adaptive spatial representation" pillar, which this project's CLAUDE.md explicitly says must not be conflated with adaptive sensing.
- Evidence level(s): DIRECT for mechanism (verbatim abstract); numeric performance NOT REPORTED in accessible text.

### Fast Attention-Based Simplification of LiDAR Point Clouds for Object Detection and Classification
- Authors: Z. Rozsa, Á. Madaras, Q. Wei, X. Lu, M. Golarits, H. Yuan, T. Sziranyi, R. Hamzaoui
- Year: 2026
- Venue: arXiv preprint (cs.CV)
- Link/identifier: arXiv:2603.07593
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Point-cloud simplification methods trade off speed against detection/classification accuracy; very fast methods (random sampling) lose accuracy, accurate methods (farthest point sampling, FPS) are slow.
- Representation: Raw LiDAR point cloud, resampled to a smaller point set.
- Resolution strategy: Variable point density driven by a **learned** importance/attention score, not by distance alone — "a feature embedding module with an attention-based sampling module to prioritize task-relevant regions, trained end-to-end."
- Adaptive mechanism categor(y/ies): **Adaptive attention/ROI** applied to point-cloud pre-processing (per-frame, not a persistent map).
- Perception method: Learned attention-based sampling feeding standard detection/classification networks.
- Terrain/dynamic-object/temporal handling: Not addressed (generic object detection/classification benchmark).
- Uncertainty handling: Not addressed.
- Computational characteristics (DIRECT, verbatim): "consistently faster than FPS," slower than random sampling (RS), with "the largest gains under aggressive downsampling."
- Datasets: KITTI (3D object detection) plus four additional classification datasets (unnamed in the accessible abstract).
- Evaluation: Accuracy/speed comparison against FPS and RS baselines at matched sampling ratios.
- Limitations: Not stated explicitly in the abstract; the only disclosed trade-off is being slower than plain random sampling.
- Relevance to SIH problem: Direct evidence that **learned, task-driven (attention) LiDAR point-density reallocation** — as opposed to purely distance-based downsampling — is an active 2026 research topic with a working KITTI-validated implementation. Relevant to H3's "unexplored" framing, though this operates on raw point clouds for a per-frame detector, not on a persistent adaptive-resolution map.
- Evidence level(s): DIRECT for mechanism and qualitative speed claims (verbatim abstract); no exact latency/ms or accuracy-delta numbers were present in the accessible abstract text.

### PointSplit: Towards On-device 3D Object Detection with Heterogeneous Low-power Accelerators
- Authors: Keondo Park, You Rim Choi, Inhoe Lee, Hyung-Sin Kim
- Year: Originally IPSN 2023; arXiv posting 2025
- Venue: ACM/IEEE IPSN 2023 (pp. 67–81)
- Link/identifier: arXiv:2504.03654
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: 3D object detection from RGB-D-derived point clouds is too heavy for a single low-power edge accelerator; the paper splits work across heterogeneous accelerators (mobile GPU + NPU/EdgeTPU).
- Representation: Point-based 3D representation from RGB-D sensors (not LiDAR specifically, but the same point-cloud processing problem class).
- Resolution strategy: Variable point density via **"2D semantics-aware biased point sampling"** — points are sampled non-uniformly based on 2D semantic-segmentation output, i.e., explicitly semantic-class-driven, not distance-driven.
- Adaptive mechanism categor(y/ies): **Adaptive attention/ROI** (semantics-driven biased sampling) combined with **adaptive computational representation** (role-based group-wise quantization split across heterogeneous accelerators).
- Perception method: Learned 3D detection pipeline with heterogeneous-hardware-aware execution partitioning.
- Terrain/dynamic-object/temporal handling: Not addressed (indoor RGB-D object detection benchmark).
- Uncertainty handling: Not addressed.
- Computational characteristics (DIRECT, verbatim): "24.7 times faster with similar accuracy" versus a full-precision GPU-only baseline.
- Datasets: SUN RGB-D, ScanNet V2.
- Evaluation: Latency/accuracy comparison against a GPU-only full-precision baseline on a mobile-GPU + EdgeTPU testbed (TensorFlow Lite).
- Limitations: Not detailed in the accessible abstract.
- Relevance to SIH problem: **Direct, named counter-evidence against H3's "unexplored" framing** — "semantics-aware biased point sampling" is explicitly semantic-class-driven adaptive spatial density in a real, published, benchmarked on-device 3D detection system. It is RGB-D indoor detection rather than outdoor mobile-robot LiDAR terrain/object mapping, so a gap plausibly remains for the SIH's specific setting, but the general mechanism is demonstrated prior art.
- Evidence level(s): DIRECT for mechanism and headline speedup number (verbatim abstract); dataset-specific accuracy deltas not given in the accessible text.

### Double-Helix Vision (DH-V2): A Geometry-Based Visual Sampler for Bandwidth-Constrained Perception
- Authors: Jinwen Wen
- Year: 2026
- Venue: arXiv preprint (cs.CV)
- Link/identifier: arXiv:2606.14773
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Bandwidth-constrained visual perception needs drastic data reduction without a neural attention model.
- Representation: 2D camera image (not LiDAR), sampled along two phase-shifted golden-ratio-inspired spiral ("double-helix") trajectories.
- Resolution strategy: Fixed **geometric** foveation pattern — dense at the center, sparse at the periphery, mimicking biological foveation, but **not content- or task-adaptive**: the spiral geometry does not change based on scene content, only where the sensor/gaze is pointed.
- Adaptive mechanism categor(y/ies): **Adaptive sensing** in the weak sense that the fovea is spatially non-uniform, but it is a **fixed, hand-designed pattern**, not scene-adaptive — useful as a *contrast* case (classical/geometric foveation vs. learned/content-driven foveation).
- Perception method: Classical/geometric, explicitly "without neural network dependencies."
- Terrain/dynamic-object/temporal handling: Not addressed.
- Uncertainty handling: Not addressed.
- Computational characteristics (DIRECT, verbatim): "0.52 ms per 1080p frame on CPU-only hardware," "2.7 KB JSON packets," "1,433× compression at 4K resolution (99.93% data reduction)."
- Datasets: CIFAR-10 (with an extreme K=128-points-per-helix sampling regime), reporting "6.03% accuracy improvement over uniform random sampling."
- Evaluation: Compression-ratio and downstream-accuracy comparison vs. uniform random sampling.
- Limitations: Abstract provides minimal discussion of failure cases.
- Relevance to SIH problem: Useful lineage/contrast: shows that *fixed* biologically-inspired foveation (no content-awareness at all) already gives large bandwidth savings on CPU-only hardware, which sets a low-cost baseline that any semantic/uncertainty-aware scheme for the SIH problem would need to beat to justify its added complexity.
- Evidence level(s): DIRECT for mechanism and quantitative claims (verbatim abstract); camera-only, CIFAR-10 evaluation is a weak proxy for outdoor mobile-robot LiDAR perception (INFERENCE that transfer is unproven).

### An overview of space-variant and active vision mechanisms for resource-constrained human-inspired robotic vision
- Authors: Not resolved (paywalled; unavailable from accessible text)
- Year: 2023
- Venue: Autonomous Robots (Springer)
- Link/identifier: DOI 10.1007/s10514-023-10107-7
- Access level: **snippet only** — Springer page redirected to an authentication wall (403/redirect-to-IDP) and could not be read; ACM DL mirror likewise not fetched. All content below is from WebSearch result snippets only. Flagged explicitly low-confidence.
- Problem: Survey of biologically-inspired space-variant (foveated) and active vision mechanisms for resource-constrained robots.
- Representation: Camera/vision-based (log-polar and related space-variant image representations); no indication from snippets that LiDAR is covered.
- Resolution strategy: Survey of variable-resolution vision representations, "from low-level hardwired attention vision (foveal vision) to high-level visual attention mechanisms."
- Adaptive mechanism categor(y/ies): Survey spans **adaptive sensing** and **adaptive attention/ROI** mechanisms for cameras.
- Perception method: Survey covering both classical (log-polar transforms) and learned (deep attention) methods per snippet text.
- Terrain/dynamic-object/temporal/uncertainty handling: Not established (access failure).
- Computational characteristics: Snippet states log-polar imaging has "surpassed conventional approaches ... where real-time constraints require resource-economic image representations," but no numbers were retrievable.
- Datasets/Evaluation: Not established (access failure).
- Limitations: Not established (access failure).
- Relevance to SIH problem: If accurately summarized by the snippet, this is a comprehensive 2023 survey establishing that foveated/space-variant vision is a decades-old, well-studied lineage (see log-polar note) for cameras — useful as a "this is not a new idea in the vision domain" data point, but its applicability is explicitly camera-side per the snippet, and it could NOT be verified in full text, so no strong claims are drawn from it.
- Evidence level(s): SNIPPET-ONLY throughout; treat every claim in this entry as reduced-confidence.

### Occupancy Grids: A Stochastic Spatial Representation for Active Robot Perception
- Authors: Alberto Elfes
- Year: 1990 (arXiv posting 2013)
- Venue: Proceedings of the Sixth Conference on Uncertainty in Artificial Intelligence (UAI 1990)
- Link/identifier: arXiv:1304.1098
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Foundational — how to represent spatial occupancy from noisy range sensors in a way that supports incremental fusion, multi-sensor integration, and decision-making.
- Representation: 2D/3D discretized grid; each cell holds a probabilistic occupancy estimate (the canonical "occupancy grid").
- Resolution strategy: Not discussed as spatially variable in the accessible abstract — this is the foundational **fixed-resolution** Bayesian grid that essentially all later adaptive-resolution occupancy work (Group A's D-Map, octree maps, etc.) modifies.
- Adaptive mechanism categor(y/ies): None of the six per-cell resolution categories apply — included as the **root of the lineage** for uncertainty-aware mapping, not as an adaptive-resolution method itself.
- Perception method: Classical Bayesian estimation with stochastic sensor (forward/inverse) models.
- Terrain handling: Not addressed (general spatial occupancy, pre-dates terrain-specific formulations).
- Dynamic-object handling: Not addressed.
- Temporal processing: Incremental multi-view fusion.
- Uncertainty handling: **This is the founding formalism for occupancy-state uncertainty** — Bayesian estimation with explicit sensor-noise modeling; per-cell probability of occupancy is the uncertainty representation itself.
- Computational characteristics: Not applicable/not reported (1990-era, pre-real-time-benchmarking norms).
- Datasets: N/A (era predates standard benchmark datasets).
- Evaluation: Conceptual/demonstrative, not benchmark-based.
- Limitations: A follow-up search finding (Thrun's later "Robotic Mapping: A Survey") notes the classic occupancy-grid formulation's "major shortcoming... is the lack of a method for accommodating pose uncertainty" (DERIVED from a secondary source, not from Elfes' own text).
- Relevance to SIH problem: Establishes that occupancy-state uncertainty representation is over 35 years old and foundational — any "uncertainty-aware mapping" claim in more recent literature (below) should be understood as extending, not inventing, this lineage.
- Evidence level(s): DIRECT for representation and uncertainty-handling description (verbatim abstract); the "pose uncertainty" limitation claim is DERIVED from a separate secondary source (Thrun survey), not Elfes' own abstract.

### Gaussian Process Occupancy Maps
- Authors: Simon T. O'Callaghan, Fabio T. Ramos
- Year: 2012
- Venue: The International Journal of Robotics Research (IJRR), vol. 31, pp. 42–62
- Link/identifier: DOI 10.1177/0278364911421039
- Access level: **snippet only** (search-result summary; publisher full text not fetched) — flagged low-confidence for anything beyond the points below.
- Problem: Standard occupancy grids assume independence between cells and ignore spatial structure/correlation in real environments.
- Representation: Continuous, non-parametric — a modified Gaussian process (GP) classifier over occupancy, rather than a discretized grid.
- Resolution strategy: Notably, per the search summary, the method is described as an **"anytime" algorithm capable of generating accurate representations of large environments at arbitrary resolutions** — i.e., resolution is a query-time choice on a continuous underlying model, not a fixed discretization.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (continuous field queryable at arbitrary resolution) and lineage for **uncertainty-aware mapping** (GP variance gives a native uncertainty surface).
- Perception method: Classical non-parametric Bayesian (GP), not a deep-learned method.
- Terrain/dynamic-object handling: Not addressed (general occupancy, static-world classic setting).
- Temporal processing: Not addressed in the snippet (later extensions, e.g. "Gaussian Process Occupancy Maps for Dynamic Environments," exist as separate follow-on papers per search results, not verified here).
- Uncertainty handling: GP posterior variance provides a **continuous, principled uncertainty surface over occupancy state**, including in occluded/unobserved regions between sensor beams — qualitatively different from a single per-cell probability.
- Computational characteristics: A widely cited later limitation (from related search results on "Efficient Clustering for Continuous Occupancy Mapping" and "Fast Gaussian Process Occupancy Maps") is that GP methods have **high computational complexity that limits large-scale/real-time application** — this is DERIVED from adjacent literature responding to this exact scalability problem, not from the 2012 paper's own text.
- Datasets/Evaluation: Not established from the snippet.
- Limitations: Scalability (see above, DERIVED from follow-on literature that exists specifically to address it).
- Relevance to SIH problem: Important lineage point for both H3 and H5: an "arbitrary resolution, anytime" continuous representation with native uncertainty existed in 2012, well before the SIH's framing — but its real-world adoption has been limited by the well-documented GP scalability problem, which is itself indirect evidence that a mathematically elegant adaptive/uncertainty-aware representation does not automatically translate into a computationally practical one (relevant caution for H5).
- Evidence level(s): SNIPPET-ONLY for direct paper content; DERIVED for the scalability-limitation claim (inferred from why later GP-occupancy papers exist, not stated by O'Callaghan & Ramos themselves).

### Deep Inverse Sensor Models as Priors for Evidential Occupancy Mapping
- Authors: Daniel Bauer, Lars Kuhnert, Lutz Eckstein
- Year: 2020
- Venue: arXiv preprint (cs.RO); IEEE IV 2021 per related listings
- Link/identifier: arXiv:2012.02111
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Occupancy inference from **radar** (not LiDAR) suffers from sparse, environment-dependent noisy returns (multipath reflections); geometric inverse sensor models (ISMs) perform poorly in unobserved-but-inferable areas, and deep-learned ISMs lack calibrated uncertainty/verification.
- Representation: Grid-based occupancy map (2D vs. 2.5D not specified in the accessible abstract).
- Resolution strategy: Not addressed as spatially variable.
- Adaptive mechanism categor(y/ies): Not an adaptive-resolution paper; relevant to this project purely as **uncertainty-handling** lineage (combining classical geometric priors with deep evidential learning).
- Perception method: Hybrid — classical geometric ISM used as a *prior/verification signal* for a learned deep ISM.
- Terrain/dynamic-object/temporal handling: Not addressed.
- Uncertainty handling: Evidential framework distinguishing cells whose occupancy estimate is **learned** vs. **geometrically verified**, with "a lower limit on the deep ISM estimate's certainty together with analytical proofs of convergence" — i.e., a formally bounded confidence measure, not just a softmax probability.
- Computational characteristics: Not reported in the accessible abstract.
- Datasets/Evaluation: Not specified in the accessible abstract.
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: Radar, not LiDAR — relevant mainly as a **methodological template** (evidential fusion of classical geometric certainty with learned occupancy priors) that the same research group (RWTH Aachen ika institute) later applied to LiDAR in the related EviLOG project (below).
- Evidence level(s): DIRECT for problem/mechanism description (verbatim abstract); no numeric results accessible.

### EviLOG: Evidential LiDAR Occupancy Grid Mapping
- Authors: RWTH Aachen ika institute team (individual author list not resolved from the accessible README; related published variant is "A Simulation-based End-to-End Learning Framework for Evidential Occupancy Grid Mapping," arXiv:2102.12718, same research group)
- Year: 2021 (GitHub project; related arXiv paper 2021)
- Venue: GitHub open-source project / associated conference paper
- Link/identifier: github.com/ika-rwth-aachen/EviLOG
- Access level: README read directly; underlying paper (arXiv:2102.12718) not independently re-fetched — treat paper-level claims as **reduced confidence**, README-level claims as DIRECT.
- Problem: Build occupancy grid maps from LiDAR that are (a) learned end-to-end without manual labels and (b) carry quantified uncertainty.
- Representation: LiDAR-derived evidential occupancy grid map; input built from a multi-layer grid of detections/transmissions/intensities from a single scan (per earlier search-result description of the sibling paper).
- Resolution strategy: Not stated as spatially variable in the README.
- Adaptive mechanism categor(y/ies): Not an adaptive-resolution scheme; relevant purely for **uncertainty handling** in a LiDAR occupancy pipeline.
- Perception method: Learned (deep network trained in simulation, per project description) producing an evidential (belief/disbelief/uncertainty-mass) occupancy output rather than a bare probability.
- Terrain/dynamic-object/temporal handling: Not addressed in the README.
- Uncertainty handling: **Evidential-theory occupancy** — output includes an explicit "uncertainty mass" term (in addition to occupied/free belief), distinct from a single scalar probability; designed to be trainable without hand-labeled real data (trained on simulated ground truth).
- Computational characteristics: Not reported in the README.
- Datasets: 10,000 synthetic training / 1,000 validation / 100 test samples, plus 5,224 real-world urban-driving point clouds (~9 minutes) captured with a Velodyne VLP-32C, used for qualitative real-world evaluation.
- Evaluation: Not detailed numerically in the README.
- Limitations: The lineage paper (per earlier evidence) explicitly frames its own motivation around the weakness it fixes: geometric ISMs are poor in unobserved-but-inferable areas, and deep ISMs are hard to train without labels — implying the paper's own remaining limitation is that simulation-to-real transfer quality is not independently guaranteed by the method (INFERENCE).
- Relevance to SIH problem: A concrete, code-released example of **evidential (multi-component) uncertainty specifically for LiDAR occupancy grids**, directly on-topic for the "uncertainty handling" pillar of this project's literature review requirements, and a template the SIH work could compare against if it goes evidential rather than simple-Bayesian.
- Evidence level(s): DIRECT for README-level facts (dataset sizes, sensor, general description); DERIVED/INFERENCE for anything attributed to the underlying paper's method details, since that paper was not independently re-fetched in full.

### E2-BKI: Evidential Ellipsoidal Bayesian Kernel Inference for Uncertainty-aware Gaussian Semantic Mapping
- Authors: Junyoung Kim, Minsik Jeon, Jihong Min, Kiho Kwak, Junwon Seo
- Year: 2025 (submitted Sept 2025; revised Jan 2026)
- Venue: IEEE Robotics and Automation Letters (RA-L)
- Link/identifier: arXiv:2509.11964
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Semantic mapping in outdoor robot environments degrades under multiple simultaneous uncertainty sources (sensor noise, sparse coverage, semantic misclassification).
- Representation: Kernel-based Gaussian semantic map — "geometry-aligned kernels that adapt to complex scene structures" aggregate noisy per-point observations into coherent Gaussian primitives; effectively **2.5D/3D continuous**, not a fixed voxel grid.
- Resolution strategy: **Variable, driven by scene geometry** — kernel shape/extent adapts to local structure rather than using a fixed grid cell size. This is scene-structure-driven, not distance-driven or explicitly semantic-class-driven, though the mapping target is semantic.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (kernel geometry adapts per local scene structure); borderline **adaptive map resolution** in effect, since the persistent map's effective spatial support varies with geometry.
- Perception method: Learned — Evidential Deep Learning supplies per-point semantic-prediction uncertainty, fused via Bayesian Kernel Inference.
- Terrain handling: Evaluated in "off-road ... outdoor environments" per abstract, implying terrain-relevant semantic classes, though not detailed further.
- Dynamic-object handling: Not addressed in the accessible abstract.
- Temporal processing: Not addressed explicitly (appears to be per-scan aggregation into a persistent map, typical of Bayesian Kernel Inference methods, but not confirmed).
- Uncertainty handling: **Semantic-prediction uncertainty specifically** (via Evidential Deep Learning), used to "mitigate the impact of unreliable points" during map fusion — precisely the kind of semantic-confidence uncertainty this project's brief asks to distinguish from sensor-noise or occupancy-state uncertainty.
- Computational characteristics: Abstract states the method maintains "real-time efficiency" but gives no exact latency/FPS/memory figures in the accessible text.
- Datasets: "Diverse off-road and urban outdoor environments" (specific dataset names not given in the accessible abstract).
- Evaluation: Reported improvements in "mapping quality, uncertainty calibration, representational flexibility, and robustness" (qualitative from abstract; no numeric deltas accessible).
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: **One of the strongest available counter-examples to a strict reading of H3.** A 2025/2026 RA-L paper already does geometry/scene-structure-adaptive spatial representation coupled with per-point *semantic*-confidence uncertainty for outdoor semantic mapping — very close to "semantic- and uncertainty-aware adaptive spatial representation." It is kernel-based rather than a discretized adaptive-resolution grid, and its resolution driver is geometric structure rather than an explicit semantic-class rule, so it does not fully collapse H3, but it substantially weakens the "unexplored" claim.
- Evidence level(s): DIRECT for mechanism, uncertainty type, and qualitative claims (verbatim abstract); no exact performance numbers were present in the accessible text (NOT REPORTED, not omitted by this reviewer).

### ContraMap: Contrastive Uncertainty Mapping for Robot Environment Representation
- Authors: Chi Cuong Le, Weiming Zhi
- Year: 2026 (submitted March 2026)
- Venue: arXiv preprint (cs.RO / cs.AI / cs.CV)
- Link/identifier: arXiv:2603.27632
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Robot environment representations need to flag where predictions are unreliable (sparse/missing observations) without paying the cost of full Bayesian inference.
- Representation: Kernel-based discriminative map augmented with an explicit learned "uncertainty class."
- Resolution strategy: Not specified as spatially variable in the accessible abstract.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** — unobserved regions are treated as a distinct contrastive class rather than the map's spatial resolution itself varying.
- Perception method: Hybrid — classical kernel-based map structure, learned contrastive discrimination for the uncertainty class, trained via synthetic noise injection.
- Terrain/dynamic-object/temporal handling: Not detailed in the accessible abstract.
- Uncertainty handling: **Occupancy/observation-sparsity uncertainty**, reframed as a classification problem — "spatial uncertainty estimation in real time without Bayesian inference," with the uncertainty-class probability acting as a distance-aware uncertainty surrogate.
- Computational characteristics: Abstract claims the approach is "substantially more efficient than Bayesian kernel-map baselines," but gives no exact numbers in the accessible text.
- Datasets: 2D occupancy mapping, 3D semantic mapping, and tabletop scene-reconstruction experiments (specific public dataset names not given in the accessible abstract).
- Evaluation: Comparative efficiency/quality against Bayesian kernel-map baselines (qualitative from abstract).
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: A 2026 example of explicitly trading exact Bayesian uncertainty for a cheaper learned proxy — directly relevant to this project's "effective vs. nominal" and "actual end-to-end latency" concerns: it is evidence that even within the uncertainty-aware mapping community, full Bayesian uncertainty is considered too expensive for some real-time settings, motivating cheaper approximations.
- Evidence level(s): DIRECT for mechanism and qualitative efficiency claim (verbatim abstract); no exact numeric benchmark accessible.

### Uncertainty-Aware Visual-Inertial SLAM with Volumetric Occupancy Mapping
- Authors: Jaehyung Jung, Simon Boche, Sebastián Barbas Laina, Stefan Leutenegger
- Year: 2024 (submitted Sept 2024; revised March 2025)
- Venue: ICRA 2025
- Link/identifier: arXiv:2409.12051
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Coupling sparse visual-inertial SLAM with dense volumetric mapping while properly accounting for neural-network depth-prediction uncertainty, rather than treating predicted depth as ground truth.
- Representation: Dense volumetric occupancy map organized as consistent **submaps** at scale (voxel size/fixed-vs-variable not stated in the accessible abstract).
- Resolution strategy: Not stated as spatially variable.
- Adaptive mechanism categor(y/ies): Not an adaptive-resolution paper; relevant as **uncertainty-propagation** lineage.
- Perception method: Hybrid — classical sparse visual-inertial SLAM (reprojection + inertial factors) fused with a learned monocular/multi-baseline depth-and-uncertainty network.
- Terrain/dynamic-object/temporal handling: Not addressed in the accessible abstract.
- Uncertainty handling: **Depth-prediction uncertainty from a neural network**, explicitly propagated in two places: (1) into per-voxel occupancy probabilities, and (2) into the alignment/registration factors between generated dense submaps inside a joint nonlinear-least-squares estimator — i.e., this paper distinguishes and connects *sensor/prediction* uncertainty and *registration-fit* uncertainty, both categories this project's brief explicitly asks to track separately.
- Computational characteristics: Not reported in the accessible abstract.
- Datasets: "Two benchmark datasets" (names not given in the accessible abstract).
- Evaluation: Reported to exceed state-of-the-art localization and mapping accuracy (qualitative only from the accessible text).
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: A clean, recent example of uncertainty propagation chained across depth-prediction → occupancy → registration, useful as a methodological reference for how "uncertainty" can and should be decomposed by type rather than treated as one monolithic quantity, directly matching this project's evidence-labeling philosophy.
- Evidence level(s): DIRECT for the two-place uncertainty-propagation mechanism (verbatim abstract); no numeric results accessible.

### SOGMP / SOGMP++: Stochastic Occupancy Grid Map Prediction in Dynamic Scenes
- Authors: Zhanteng Xie, Philip Dames
- Year: 2023
- Venue: Conference on Robot Learning (CoRL) 2023
- Link/identifier: arXiv:2210.08577; PMLR v229
- Access level: Abstract-page fetch succeeded cleanly; a direct fetch of the PMLR PDF returned a **partially garbled result with the fetch tool itself hedging ("likely," "not clearly stated")** — that PDF-derived detail is explicitly flagged low-confidence and NOT treated as a verified full read.
- Problem: Predicting the **future** state of dynamic occupancy grids so a mobile robot can plan around not-yet-arrived obstacle motion.
- Representation: Occupancy grid (resolution not confirmed from clean-abstract text; PDF-derived claim of "fixed-resolution" is low-confidence).
- Resolution strategy: Not confirmed as variable from the clean abstract.
- Adaptive mechanism categor(y/ies): Best-supported (clean-abstract) classification is **adaptive computational representation** in the weak sense that the VAE learns a latent encoding of possible occupancy futures rather than propagating a single deterministic grid — but this classification is INFERENCE, not stated verbatim by the authors.
- Perception method: Learned — a variational autoencoder (VAE) predicts "a range of possible future states of the environment," incorporating robot ego-motion, dynamic-object motion, and static-scene geometry (DIRECT, verbatim abstract).
- Terrain handling: Not addressed.
- Dynamic-object handling: **Central to the paper** — explicitly models and predicts moving-obstacle occupancy evolution (DIRECT, verbatim abstract), rather than assuming a static world (a notable contrast to the D-Map-style "decremental known-cell removal" static-world assumption flagged in the sibling Group A file).
- Temporal processing: Multi-future-timestep stochastic prediction (DIRECT, verbatim abstract framing); exact horizon length NOT REPORTED in the accessible clean-abstract text.
- Uncertainty handling: **Predictive/aleatoric uncertainty over future occupancy** — the VAE outputs a *distribution* over possible future grids rather than one deterministic prediction, which is a distinct uncertainty type from the sensor-noise or semantic-confidence uncertainty seen in the mapping papers above.
- Computational characteristics: NOT REPORTED in the accessible clean-abstract text; low-confidence PDF-derived attempt could not surface reliable numbers either.
- Datasets: OGM-Turtlebot2 (simulated, moving pedestrians in a lobby), OGM-Jackal, and OGM-Spot (both real-world, collected at UT Austin) — DIRECT, cross-confirmed by both the abstract fetch and the GitHub project page.
- Evaluation: Comparative prediction-accuracy/robustness against other occupancy-prediction baselines (qualitative claim of superiority; no exact metric numbers accessible).
- Limitations: NOT REPORTED in the accessible text (this reviewer explicitly declines to guess, unlike the earlier low-confidence PDF-derived pass which speculated "likely... long-term prediction accuracy" limitations — that speculation is discarded here as unverified).
- Relevance to SIH problem: Directly relevant to the SIH's "dynamic objects" and "temporal stability" pillars — demonstrates that predictive, uncertainty-quantified *future* occupancy (not just current-state occupancy) is an active CoRL-level research direction for exactly the kind of ground-robot dynamic-scene setting the SIH targets.
- Evidence level(s): DIRECT for problem/method/datasets (verbatim clean abstract); explicitly NOT REPORTED for computational numbers and limitations (the earlier PDF-derived guesses are disclosed above but not relied upon).

### Uncertainty-driven Planner for Exploration and Navigation
- Authors: Georgios Georgakis, Bernadette Bucher, Anton Arapin, Karl Schmeckpeper, Nikolai Matni, Kostas Daniilidis
- Year: 2022
- Venue: arXiv preprint (cs.RO)
- Link/identifier: arXiv:2202.11907
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Exploration and point-goal navigation in unseen indoor environments, where a learned occupancy predictor must extrapolate beyond the robot's current field of view.
- Representation: Predicted occupancy maps extending beyond the immediate sensor field of view.
- Resolution strategy: Not addressed as spatially variable.
- Adaptive mechanism categor(y/ies): Hybrid — learned occupancy-prediction network feeding a classical decision rule; not a resolution-adaptive scheme.
- Perception method: Learned occupancy prediction (beyond-FOV completion) + classical planning policy.
- Terrain/dynamic-object/temporal handling: Not addressed (indoor point-goal navigation benchmark, static world assumed).
- Uncertainty handling: **Model (epistemic) uncertainty over predicted, unobserved map regions**, used two ways: an upper-confidence-bound-style rule for navigation, and uncertainty-maximization for exploration — i.e., the *same* uncertainty estimate is consumed differently depending on task.
- Computational characteristics: Not reported in the accessible abstract.
- Datasets: Matterport3D via the Habitat simulator.
- Evaluation: Exploration coverage and navigation success/map-quality metrics vs. baselines (qualitative "improvements" claim; no exact numbers in accessible text).
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: A clean illustration that "uncertainty-aware" can mean uncertainty over *predicted/extrapolated* map content beyond current sensing range — a distinct sub-type from occupancy-state, semantic-confidence, or registration uncertainty seen elsewhere in this file, worth keeping separate when the SIH project later specifies its own uncertainty model.
- Evidence level(s): DIRECT for mechanism (verbatim abstract); no numeric results accessible.

### RAMP: A Risk-Aware Mapping and Planning Pipeline for Fast Off-Road Ground Robot Navigation
- Authors: Lakshay Sharma, Michael Everett, Donggun Lee, Xiaoyi Cai, Philip Osteen, Jonathan P. How
- Year: 2022 (submitted Oct 2022; revised March 2023)
- Venue: ICRA 2023
- Link/identifier: arXiv:2210.06605
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Fast off-road ground-robot navigation needs to balance speed and safety; standard raytraced occupancy grids misrepresent unknown space as either free or unsafe, and standard planners (e.g., MPPI) treat known-free and unknown space identically.
- Representation: **2.5D maps** — 2D occupancy grid augmented with elevation/height information derived from point clouds (DIRECT, verbatim: "2.5D maps (2D representations with additional 3D information)").
- Resolution strategy: Uniform spatial grid resolution (not stated as spatially variable); the *risk-aware variability* in this paper is in the **planning horizon**, not the map cell size — the MPPI-based planner has "embedded variability in horizon, to maximize speed in known free space while retaining cautionary penetration into unknown space."
- Adaptive mechanism categor(y/ies): Not adaptive map resolution — this is a **risk-aware spatial representation** at the map-content level (explicit known-free vs. unknown-space distinction feeding risk-weighted planning) combined with adaptive planning-horizon depth; useful precisely as a case where "risk-aware" does not imply "resolution-adaptive."
- Perception method: Classical geometric mapping (ground-point inflation with persistent spatial memory) + classical MPPI planning.
- Terrain handling: Central — 2.5D elevation-derived risk constraints from 3D terrain geometry (DIRECT, verbatim: "risk constraints arising from 3D terrain").
- Dynamic-object handling: Not detailed in the accessible abstract.
- Temporal processing: Persistent spatial memory across scans (DIRECT, verbatim).
- Uncertainty handling: Distinguishes known-free / known-occupied / unknown space explicitly, treating **unknown-space risk** as a first-class planning input rather than folding it into a single occupancy probability — a form of epistemic/exposure risk rather than sensor-noise uncertainty.
- Computational characteristics: NOT REPORTED in the accessible abstract (no FPS/latency/memory numbers).
- Datasets: Not named; validated via "simulations and hardware demonstrations."
- Evaluation: Simulation and real hardware demonstration (qualitative from accessible text).
- Limitations: Not enumerated in the accessible abstract.
- Relevance to SIH problem: Directly on-topic 2.5D risk-aware terrain representation for a fast ground robot — one of the closest matches in this literature set to the SIH's own "2.5D adaptive spatial representation" framing, though notably its adaptivity is in planning horizon and risk-weighting, not in map cell resolution — a useful reminder that "risk-aware" and "resolution-adaptive" are separable design choices.
- Evidence level(s): DIRECT for representation, mechanism, and terrain/uncertainty handling (verbatim abstract); NOT REPORTED for computational numbers.

### EVORA: Deep Evidential Traversability Learning for Risk-Aware Off-Road Autonomy
- Authors: Xiaoyi Cai, Siddharth Ancha, Lakshay Sharma, et al.
- Year: 2023 (submitted Nov 2023; revised March 2024)
- Venue: arXiv preprint (cs.RO); associated with the MIT/ARL off-road autonomy line of work that includes RAMP and STEP-adjacent authors
- Link/identifier: arXiv:2311.06234
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Off-road terrain-traversability prediction needs calibrated uncertainty (not just a point cost estimate) to support genuinely risk-aware planning; hand-designed terrain costs and naive learned predictors both fail to represent model confidence properly.
- Representation: Learned discrete traction distributions and latent-feature probability densities over terrain patches (evidential/Dirichlet parameterization), not a fixed grid resolution scheme.
- Resolution strategy: Not addressed as spatially variable in the accessible abstract.
- Adaptive mechanism categor(y/ies): Not an adaptive-resolution paper; core contribution is **uncertainty-typed risk representation**.
- Perception method: Learned — evidential deep learning producing Dirichlet-distributed traction predictions.
- Terrain handling: Central — traction/traversability estimation is the entire subject.
- Dynamic-object handling: Not addressed.
- Temporal processing: Not addressed.
- Uncertainty handling: **Explicitly both aleatoric and epistemic**, and crucially, the paper's risk-aware planner treats them differently — "worst-case expected traction" handles aleatoric (inherent terrain variability) uncertainty, while trajectories are separately penalized for high **epistemic** (model-confidence) uncertainty. This aleatoric/epistemic split, and treating them with different planning responses, is a methodologically important and precise example for this project's uncertainty-labeling requirements.
- Computational characteristics: NOT REPORTED in the accessible abstract.
- Datasets: Not named; validated "in simulation and on wheeled and quadruped robots."
- Evaluation: Simulation plus multi-platform real-robot validation (qualitative from accessible text).
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: A precise, recent template for how to decompose "uncertainty" into aleatoric vs. epistemic components and route each to a different risk-planning response — directly useful methodological reference for the SIH's terrain-analysis pillar, independent of any resolution-adaptivity claim.
- Evidence level(s): DIRECT for the aleatoric/epistemic distinction and its differentiated use (verbatim abstract); NOT REPORTED for computational numbers.

### STEP: Stochastic Traversability Evaluation and Planning for Risk-Aware Off-road Navigation (+ DARPA Subterranean Challenge results)
- Authors: Original — Anushri Dixit, David D. Fan, Kyohei Otsu, et al.; DARPA SubT results paper — Anushri Dixit, David D. Fan, Kyohei Otsu, Sharmita Dey, Ali-Akbar Agha-Mohammadi, Joel W. Burdick
- Year: 2021 (original, arXiv:2103.02828); 2023/2024 (SubT results, arXiv:2303.01614, published in Field Robotics)
- Venue: arXiv; Field Robotics journal
- Link/identifier: arXiv:2103.02828, arXiv:2303.01614
- Access level: abstract read (arXiv abstract-page fetch, both versions)
- Problem: Fully autonomous navigation in extreme, previously-unmapped subterranean environments (caves, mines, rubble) under severe perceptual degradation.
- Representation: Uncertainty-aware traversability map (exact grid structure not detailed in the accessible abstracts).
- Resolution strategy: Not addressed as spatially variable in the accessible abstracts.
- Adaptive mechanism categor(y/ies): Not an adaptive-resolution paper; core contributions are (1) **risk-aware spatial representation** via tail-risk statistics and (2) **risk-based behavioral adaptation** (gait changes, recovery behaviors) — the latter is adaptive at the *robot behavior* level, not the map level.
- Perception method: Classical — "rapid uncertainty-aware mapping and traversability evaluation," CVaR-based tail-risk assessment, and SQP-based MPC for planning (no deep-learning component stated in the accessible abstracts).
- Terrain handling: Central — traversability evaluation is the whole system's purpose, field-tested in real caves/mines (Valentine Cave CA, Kentucky Underground, Louisville Mega Cavern).
- Dynamic-object handling: Not addressed in the accessible abstracts.
- Temporal processing: "Fast recovery behaviors" imply online replanning; not otherwise detailed.
- Uncertainty handling: **Tail-risk (Conditional Value-at-Risk, CVaR)** applied to traversability estimates — CVaR quantifies the expected cost in the worst-case tail beyond a probability threshold, a materially different risk formalism from a simple mean-cost or single occupancy probability, and precisely matches this project's "risk-aware spatial representation" family.
- Computational characteristics: NOT REPORTED in the accessible abstracts.
- Datasets: No public benchmark; real-world DARPA Subterranean Challenge field deployments (multiple named cave/mine sites) on wheeled and legged (quadruped) platforms.
- Evaluation: Field-test validation across three real subterranean sites; also risk-based gait adaptation for quadrupeds.
- Limitations: Not stated in the accessible abstracts.
- Relevance to SIH problem: A field-proven (not just simulated) example of CVaR-based tail-risk traversability assessment feeding real-time planning on real ground/legged robots in extreme terrain — strong evidence that risk-aware (not merely probability-aware) spatial representations are mature enough for real deployment, independent of any resolution-adaptivity question.
- Evidence level(s): DIRECT for CVaR mechanism and field-test claims (verbatim abstracts, both versions); NOT REPORTED for computational numbers.

### RiskMap: A Unified Driving Context Representation for Autonomous Motion Planning in Urban Driving Environment
- Authors: Ren Xin, Sheng Wang, Yingbing Chen, Jie Cheng, Ming Liu, Jun Ma
- Year: 2024
- Venue: arXiv preprint (per fetch, "accepted October 2024"; venue name not resolved from accessible abstract)
- Link/identifier: arXiv:2406.04451
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Urban motion planning needs an interpretable, unified representation combining perception, map priors, and prediction into a single "driving cost" prior, rather than hand-tuned heuristic cost stacking.
- Representation: A differentiable **risk field** — a continuous, learned analytical function over the driving scene (exact grid/vector/BEV dimensionality not specified in the accessible abstract).
- Resolution strategy: Not addressed as spatially variable in the accessible abstract.
- Adaptive mechanism categor(y/ies): Not clearly an adaptive-resolution scheme from the accessible text; best characterized as a **risk-aware spatial representation** (learned risk field) rather than any of the six adaptivity categories in a strict sense.
- Perception method: Learned — "empowered by deep neural networks" per the abstract.
- Terrain handling: Not addressed (urban on-road driving context, not off-road terrain).
- Dynamic-object handling: Implied — "encoding statistical understanding of traffic participants" (DIRECT, verbatim), i.e., other vehicles/pedestrians are represented probabilistically within the risk field.
- Temporal processing: Not detailed in the accessible abstract.
- Uncertainty handling: The representation is stated to "visualize sensor noise," implying sensor-noise uncertainty is folded into the risk field, but the exact mechanism is not detailed in the accessible text.
- Computational characteristics: NOT REPORTED in the accessible abstract.
- Datasets/Evaluation: Compared using a sampling-based planner; abstract claims improved "driving safety and smoothness" (qualitative only).
- Limitations: Acknowledged existence of limitations per the fetch, but not detailed in accessible text.
- Relevance to SIH problem: A 2024 example of unifying risk representation with sensor-noise-awareness in a single learned field for urban driving — relevant as a design-pattern reference for "risk-aware spatial representation," though on-road urban driving is a different regime from the SIH's off-road/general mobile-robot terrain setting.
- Evidence level(s): DIRECT for representation type and stated goals (verbatim abstract); NOT REPORTED for computational numbers or exact uncertainty mechanism.

### Risk-Aware Model Predictive Path Integral Control Using Conditional Value-at-Risk
- Authors: Ji Yin, Zhiyuan Zhang, Panagiotis Tsiotras
- Year: 2022
- Venue: arXiv preprint (cs.RO)
- Link/identifier: arXiv:2209.12842
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Enable aggressive, safety-critical robot maneuvers under uncertainty by directly optimizing a tail-risk (CVaR) measure over full nonlinear dynamics, rather than linearizing or restricting cost-function form.
- Representation: **No spatial map representation at all** — this is a pure control-level risk metric applied over sampled trajectory rollouts against a (presumably fixed, externally supplied) environment.
- Resolution strategy: N/A — no spatial resolution concept in this paper.
- Adaptive mechanism categor(y/ies): None of the six categories apply — this is a **negative/contrast case**, included specifically to keep "risk-aware" (a control/decision-theoretic property) distinct from "risk-aware spatial representation" (a mapping/perception property). RAMP, STEP, and EVORA above use risk to shape a spatial/terrain representation; this paper applies risk purely at the trajectory-optimization level and needs no map resolution concept at all.
- Perception method: N/A (pure planning/control paper).
- Terrain/dynamic-object/temporal/uncertainty handling: Uncertainty is over trajectory/dynamics outcomes under a sampling-based (MPPI) rollout, not over any environment representation.
- Computational characteristics (DIRECT, verbatim): "on-line computation at an update frequency of up to 80 Hz, utilizing modern GPUs to multi-thread the generation of trajectories as well as the CVaR values."
- Datasets/Evaluation: Simulation plus real-vehicle experimental validation performing aggressive maneuvers in cluttered environments.
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: Important boundary case for this project's terminology discipline: demonstrates that "risk-aware" work in robotics frequently has **nothing to do with spatial/map representation** at all — a caution against assuming every "risk-aware X" paper found in search results is relevant to the SIH's *representation* question.
- Evidence level(s): DIRECT for mechanism and the 80 Hz figure (verbatim abstract).

### Risk-aware Path Planning via Probabilistic Fusion of Traversability Prediction for Planetary Rovers on Heterogeneous Terrains
- Authors: Masafumi Endo, Tatsunori Taniai, Ryo Yonetani, Genya Ishigami
- Year: 2023
- Venue: IEEE ICRA 2023
- Link/identifier: arXiv:2303.01169
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Planetary rovers on heterogeneous terrain face compounding wheel-slip risk when a single traversability-prediction model is applied across terrain types it was not specialized for.
- Representation: Not detailed as a specific spatial data structure in the accessible abstract.
- Resolution strategy: Not addressed as spatially variable.
- Adaptive mechanism categor(y/ies): Not an adaptive-resolution scheme; relevant as **risk-aware, uncertainty-fused terrain representation**.
- Perception method: Hybrid — multiple ML models (terrain-type classification + slip prediction) whose outputs are fused into a single multimodal probability distribution.
- Terrain handling: Central — heterogeneous terrain classification directly drives risk estimation.
- Dynamic-object handling: Not addressed.
- Temporal processing: Not addressed in the accessible abstract.
- Uncertainty handling: **Probabilistic fusion of multiple model outputs** into a single "multimodal slip distribution accounting for heterogeneous terrains," used for statistical risk assessment — a specific and precise example of combining terrain-classification uncertainty with slip/traction predictive uncertainty.
- Computational characteristics: NOT REPORTED in the accessible abstract.
- Datasets/Evaluation: "Extensive simulation experiments" (specific benchmark not named in the accessible text).
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: A further data point for terrain-risk uncertainty fusion methodology, complementary to EVORA/STEP, reinforcing that multimodal/heterogeneous-terrain risk fusion is an active 2023 research topic relevant to the SIH's terrain-analysis pillar.
- Evidence level(s): DIRECT for mechanism (verbatim abstract); NOT REPORTED for computational numbers.

### Is Semantic SLAM Ready for Embedded Systems? A Comparative Survey
- Authors: Calvin Galagain, Martyna Poreba, François Goulette
- Year: 2025 (submitted May 2025)
- Venue: arXiv preprint (cs.RO)
- Link/identifier: arXiv:2505.12384
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Directly asks whether semantic SLAM is ready for embedded deployment, comparing three fundamentally different architectural families.
- Representation: Comparison across Geometric SLAM, Neural Radiance Fields (NeRF), and 3D Gaussian Splatting.
- Resolution strategy: Not the survey's focus; not discussed as adaptive/variable in the accessible abstract.
- Adaptive mechanism categor(y/ies): N/A (survey, not a method).
- Perception method: Survey spans classical geometric SLAM and two learned/neural-rendering representations.
- Terrain/dynamic-object/temporal/uncertainty handling: Not the survey's focus per the accessible abstract.
- Computational characteristics (DIRECT, verbatim): Testing conducted specifically on **NVIDIA Jetson AGX Orin**, evaluating "trade-offs between accuracy, computing efficiency, and power usage," including "memory usage, and energy consumption" — exact numeric tables were NOT present in the accessible abstract text.
- Key conclusions (DIRECT, verbatim): "NeRF and Gaussian Splatting achieve high semantic detail but demand substantial computing resources, limiting their use on embedded devices," whereas "Semantic Geometric SLAM offers a more practical balance between computational cost and accuracy."
- Datasets/Benchmarks: Not named in the accessible abstract.
- Limitations/gaps identified (DIRECT, verbatim): The survey concludes there is "a need for SLAM algorithms that are better adapted to embedded environments" and recommends "improving their efficiency through algorithm-hardware co-design."
- Relevance to SIH problem: Directly on-topic for the "real-time/resource-constrained" family — a 2025 survey concluding that the most semantically rich representations (NeRF, Gaussian Splatting) are currently **not** embedded-ready, and that classical geometric SLAM with semantics bolted on remains the practical choice — relevant caution against assuming newer, richer representations are automatically deployable on the kind of constrained hardware the SIH problem targets.
- Evidence level(s): DIRECT for conclusions and hardware platform (verbatim abstract); NOT REPORTED for exact numeric benchmark tables (would require full-PDF read).

### SPAQ-DL-SLAM: Towards Optimizing Deep Learning-based SLAM for Resource-Constrained Embedded Platforms
- Authors: Niraj Pudasaini, Muhammad Abdullah Hanif, Muhammad Shafique
- Year: 2024 (submitted Sept 2024)
- Venue: 18th International Conference on Control, Automation, Robotics and Vision (ICARCV 2024), Dubai
- Link/identifier: arXiv:2409.14515
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Deep-learning-based SLAM (specifically DROID-SLAM) is too heavy for real-time onboard computation on resource-constrained embedded robots.
- Representation: DROID-SLAM's dense/recurrent architecture (not a persistent adaptive-resolution map — optimization is purely at the network-compute level).
- Resolution strategy: No spatial-resolution adaptivity; **all optimization is at the neural-network-compute level** (this is explicitly the contrast the accessible abstract supports).
- Adaptive mechanism categor(y/ies): **Adaptive neural computation** is NOT quite right either, since pruning/quantization here are *static, offline* compression choices, not per-input dynamic computation — more precisely this is **model compression for embedded deployment**, a related but distinct efficiency lever from any of the six adaptivity categories (it is a fixed, not input-adaptive, reduction).
- Perception method: Learned (DROID-SLAM base), compressed via structured pruning (20%) with layer-wise sensitivity analysis, plus 8-bit post-training static quantization.
- Terrain/dynamic-object/temporal handling: Not addressed (general SLAM benchmark).
- Uncertainty handling: Not addressed.
- Computational characteristics (DIRECT, verbatim): "18.9% reduction in FLOPs," "79.8% reduction in overall model size," "10.5% average improvement on absolute trajectory error (ATE)" (the accuracy metric reportedly *improved*, not just stayed flat, after compression).
- Datasets: TUM-RGBD, ETH3D SLAM training benchmark, EuRoC (Vicon Room sequences).
- Evaluation: ATE comparison pre/post compression across the three benchmarks.
- Limitations (DIRECT, verbatim): "Performance variance on distinct Vicon Room sequences... captured at high angular velocities," indicating degradation under fast motion.
- Relevance to SIH problem: A concrete, numerically-verified example that static model compression (not dynamic/adaptive computation) can substantially cut compute cost for embedded SLAM — a useful reminder that "resource-constrained efficiency" and "adaptive/variable resolution" are not synonymous; this paper achieves large efficiency gains with **zero** spatial or computational adaptivity at inference time.
- Evidence level(s): DIRECT for all quantitative claims (verbatim abstract).

### Analysis of Voxel-Based 3D Object Detection Methods Efficiency for Real-Time Embedded Systems
- Authors: Illia Oleksiienko, Alexandros Iosifidis
- Year: 2021
- Venue: IEEE ICETCI 2021
- Link/identifier: arXiv:2105.10316
- Access level: **abstract-level only** — the arXiv abstract page yielded a general summary; a direct PDF fetch failed to parse (returned a "corrupted/compressed binary stream" error), so exact per-stage latency numbers and named detector models could **not** be verified and are marked NOT REPORTED rather than guessed.
- Problem: Understand precisely why voxel-based 3D object detectors are computationally expensive on embedded GPUs, to find genuine efficiency levers rather than assuming end-to-end redesign is required.
- Representation: Voxel-based 3D detection (specific detector names not confirmed at abstract level).
- Resolution strategy: Not itself adaptive; the paper's contribution is diagnostic (identifying *where* to apply distance-based restriction), not implementing an adaptive scheme.
- Adaptive mechanism categor(y/ies): The paper's finding motivates (but does not itself implement) **adaptive map/processing resolution driven by distance**.
- Perception method: Diagnostic efficiency analysis of learned voxel-based 3D detectors.
- Terrain/dynamic-object/temporal/uncertainty handling: Not addressed.
- Computational characteristics: Exact hardware/latency numbers NOT REPORTED at the accessible abstract level.
- Key finding (DIRECT, verbatim from the abstract-level summary): models "mostly fail to detect distant small objects" due to point-cloud sparsity, and — critically — "models trained on near objects achieve similar or better performance" than models trained on all objects, implying a potential **"40-60% speed-up"** from restricting processing to nearby regions without sacrificing detection performance.
- Datasets: Not confirmed at the accessible abstract level (KITTI is the field-standard benchmark for this class of study, but this was not independently verified in the accessible text — flagged as unconfirmed, not assumed).
- Evaluation: Comparative accuracy/speed analysis of range-restricted vs. full-range voxel processing.
- Limitations (DIRECT, verbatim): the authors themselves frame the result as revealing "substantial computational inefficiency at distant scene locations that do not contribute to successful detections" — i.e., their own finding is also their stated critique of uniform-range processing.
- Relevance to SIH problem: **Highly relevant, double-edged evidence.** On one hand, it is direct 2021 evidence that near-field-restricted (i.e., a crude form of distance-based adaptive/reduced processing) voxel detection can save significant compute (40-60%) without hurting accuracy — support for the general "distance matters, use it" intuition the SIH problem statement itself proposes. On the other hand, it also directly supports this project's disconfirming-evidence mandate around "coarse distant resolution loses important objects": the same paper states models simply **fail to detect distant small objects** in the first place — meaning the speed-up is partly available *because* distant small objects are already being missed, not because they are being efficiently handled. This is exactly the failure mode CLAUDE.md instructs this research to look for.
- Evidence level(s): DIRECT for the two key quotable findings (from the accessible abstract-level summary); the underlying PDF with exact per-model numbers was NOT verified (fetch failure) — treat exact percentages as reported-in-abstract, not independently re-derived by this reviewer.

### Agile3D: Adaptive Contention- and Content-Aware 3D Object Detection for Embedded GPUs
- Authors: Pengcheng Wang, Zhuoming Liu, Shayok Bagchi, Ran Xu, Saurabh Bagchi, Yin Li, Somali Chaterji
- Year: 2025
- Venue: ACM MobiSys 2025 (23rd Annual International Conference on Mobile Systems, Applications and Services)
- Link/identifier: DOI 10.1145/3711875.3729147; GitHub: github.com/ChulanZhang/Agile3D
- Access level: **Mixed** — the ACM DL and preprint-host PDF pages returned 403/empty; content below is drawn from (a) a direct fetch of the project GitHub README (DIRECT), (b) a Purdue University press release (DIRECT, institutional secondary source), and (c) WebSearch result summaries of the abstract (WEB VERIFIED via multiple independent search snippets, cross-consistent). No claim below rests on a single unverified snippet.
- Problem: LiDAR 3D object detection on shared embedded GPUs (e.g., a robotaxi running camera perception, LiDAR processing, tracking, mapping, and planning concurrently) suffers unpredictable latency from **GPU resource contention**, on top of the usual scene-dependent workload variation — causing stale detections or dropped frames when processing exceeds the sensor's 10-20 Hz update period.
- Representation: LiDAR point clouds processed through a **multi-branch execution framework** with five selectable "control knobs": partitioning format, **spatial resolution**, spatial encoding method, 3D feature extractor, and detection head.
- Resolution strategy: **Explicitly variable and content-driven** — spatial resolution is one of five knobs a reinforcement-learning controller selects *per frame*, jointly based on (a) scene content/complexity and (b) current GPU contention level. This is a rare example where resolution is adapted for reasons that are neither purely distance-based nor purely semantic, but **system-load-aware** as well as content-aware.
- Adaptive mechanism categor(y/ies): **Adaptive neural computation** (branch/model selection changes the compute graph) + **adaptive computational representation** (spatial resolution and encoding format change per frame) — notably NOT "adaptive map resolution" in this project's strict sense, since there is no evidence of a *persistent* map; this is per-frame detection, not map maintenance.
- Perception method: Learned — multiple detector branches selected by a reinforcement-learning controller.
- Terrain/dynamic-object/temporal handling: Not addressed (generic 3D object detection benchmark framing).
- Uncertainty handling: Not addressed — the paper's uncertainty is about *system* state (latency budget, contention level), not about the environment.
- Computational characteristics (DIRECT, from GitHub README figures): under varying contention on Jetson **Orin**, Agile3D achieves accuracy/latency pairs such as 71.72% accuracy at 362 ms, 70.98% at 415 ms, 70.03% at 468 ms, and 68.72% at 476 ms as contention increases; overall the system spans "85-360 ms, 63.71-71.73%" against baseline models ranging "105-850 ms latency with 58.62-71.7% accuracy." Per the press release and cross-confirmed by search summaries: "meets stringent latency objectives while delivering up to +3% accuracy over adaptive controllers and up to +7% over widely used static 3D detectors," tested across "latency budgets of 100 to 500 milliseconds" on **NVIDIA Jetson Orin and Xavier**, "consistently lead[ing] the Pareto frontier."
- Datasets: Not confirmed by name in the accessible README/press-release text (standard AD 3D-detection benchmarks implied by the L2 mAP metric named in the README, consistent with a Waymo-style evaluation, but this project declines to assert the specific dataset name without direct confirmation).
- Evaluation: Latency-vs-accuracy Pareto-frontier comparison against both "adaptive controllers" (i.e., other adaptive baselines) and widely-used static detectors, under multiple real hardware-contention levels on two real embedded GPUs.
- Limitations: Not stated in the accessible README/press-release text.
- Relevance to SIH problem: **The single most directly relevant piece of evidence in this file for H5.** This is a real (not purely simulated), 2025, embedded-GPU-benchmarked system in which resolution is one of several jointly-adapted knobs, and it delivers a measured, non-trivial accuracy improvement (up to +7%) at matched or better latency versus static (fixed-resolution) detectors on real Jetson hardware. It substantively **supports** H5's claim that adaptive resolution (bundled with other adaptive knobs) can provide meaningful computational/accuracy benefit under real embedded constraints. The important caveat for this project: the benefit is demonstrated for resolution *bundled with* four other adaptive knobs and for per-frame detection, not for a persistent map, so it cannot be read as isolating "map resolution adaptivity alone" as the source of the gain.
- Evidence level(s): DIRECT for GitHub README figures and mechanism description; DIRECT (institutional secondary source) for press-release performance claims; WEB VERIFIED (cross-consistent across independent search results) for the abstract-level framing; explicitly NOT independently verified against the primary ACM-hosted PDF (blocked by 403).

### DaDe: Delay-adaptive Detector for Streaming Perception
- Authors: Wonwoo Jo, Kyungshin Lee, Jaewon Baik, Sangsun Lee, Dongho Choi, Hyunkyoo Park
- Year: 2022 (submitted); presented VISAPP 2023
- Venue: VISAPP 2023 (Full Paper, Oral)
- Link/identifier: arXiv:2212.11558
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Streaming perception under processing latency — by the time a detector finishes, the real-world scene has moved on, so the detector should account for that delay rather than reporting a now-stale result.
- Representation: Image-based (camera) perception, not LiDAR or a spatial map.
- Resolution strategy: N/A — this is a temporal-forecasting mechanism, not a spatial-resolution mechanism.
- Adaptive mechanism categor(y/ies): **Adaptive neural computation** in the sense that the model's output adapts to the current delay condition via a "feature queue and feature select module" that lets it "forecast specific time steps without any additional computational cost" (DIRECT, verbatim).
- Perception method: Learned object detector with a delay-forecasting feature-selection mechanism.
- Terrain/dynamic-object/temporal handling: Temporal forecasting of scene state is the paper's central mechanism; "dynamic objects" here means detected objects in a video stream, not a persistent map's dynamic-object handling.
- Uncertainty handling: Not addressed.
- Computational characteristics: NOT REPORTED numerically in the accessible abstract (qualitative claim of exceeding "current state-of-the-art methods" on delayed scenarios).
- Datasets: Argoverse-HD.
- Evaluation: Streaming-accuracy-under-delay benchmark (same family as FOVEA's evaluation protocol above).
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: Relevant to this project's "actual end-to-end latency" and "anytime perception" concerns — demonstrates a concrete mechanism (feature forecasting) for keeping perception outputs valid despite unavoidable processing delay, a real-time systems concern orthogonal to, but compounding with, whatever spatial representation the SIH ultimately chooses.
- Evidence level(s): DIRECT for mechanism (verbatim abstract); NOT REPORTED for exact numeric results.

### Are We Ready for Real-Time LiDAR Semantic Segmentation in Autonomous Driving?
- Authors: Samir Abou Haidar, Alexandre Chariot, Mehdi Darouich, Cyril Joly, Jean-Emmanuel Deschaud
- Year: 2024 (submitted Oct 2024)
- Venue: IROS 2024 PPNIV Workshop
- Link/identifier: arXiv:2410.08365
- Access level: abstract read (arXiv abstract-page fetch); the abstract itself did not contain the detailed per-model latency/mIoU table referenced by secondary WebSearch summaries, so those specific numbers below are marked WEB VERIFIED (search-result-level) rather than DIRECT.
- Problem: Directly benchmarks whether current 3D LiDAR semantic segmentation models can run in real time on embedded automotive-grade hardware.
- Representation: Standard learned 3D/range-based LiDAR semantic segmentation networks (uniform, fixed-resolution inputs, per the framing of the problem — the paper does not propose an adaptive-resolution method).
- Resolution strategy: Not adaptive; this is a benchmarking paper, not a new method.
- Adaptive mechanism categor(y/ies): N/A (benchmark/survey).
- Perception method: Learned semantic segmentation, multiple architectures compared.
- Terrain handling: Not the focus (general semantic segmentation, includes terrain-relevant classes as part of standard driving ontologies).
- Dynamic-object handling: Related benchmark models named in the broader search context (MotionSeg3D, StreamMOS, InsMOS, MF-MOS) address moving-object segmentation specifically — WEB VERIFIED, not independently confirmed against the primary paper's own text.
- Temporal processing: Not detailed in the accessible abstract.
- Uncertainty handling: Not addressed.
- Computational characteristics: The accessible abstract states embedded platforms face "demanding computational requirements" that "hinder real-time semantic analysis" (DIRECT, verbatim) but does not itself give exact numbers in the fetched text. Separately, WebSearch summaries (WEB VERIFIED, not independently re-confirmed against the PDF) reported: on nuScenes at 20 Hz, only SalsaNext runs real-time on both RTX4090 and Jetson AGX Orin, with other models "far from real-time" on Jetson; several moving-object-segmentation models (MotionSeg3D, StreamMOS, InsMOS, MF-MOS) failed a 200 ms latency budget on Jetson; one lightweight model achieved 32 ms latency with 2.3M parameters at mIoU 0.524 (val) / 0.513 (test).
- Datasets: SemanticKITTI, nuScenes (DIRECT, verbatim abstract).
- Evaluation: Embedded benchmark on Jetson AGX Orin and Xavier vs. desktop RTX4090.
- Limitations: Not detailed in the accessible abstract text.
- Relevance to SIH problem: **Directly on-topic, high-value negative evidence** for the "real-time/resource-constrained" family: a late-2024 benchmark concluding that most current LiDAR semantic segmentation models are NOT real-time-capable on embedded automotive hardware, with only the lightest architecture meeting real-time and latency budgets, at reduced accuracy. This is a strong caution against assuming any semantically rich per-point LiDAR method — adaptive-resolution or not — will be embeddable without an efficiency-accuracy trade-off.
- Evidence level(s): DIRECT for the abstract-level framing and dataset names; WEB VERIFIED (search-result level, not independently re-confirmed against full PDF) for the specific numeric latency/mIoU figures — flagged accordingly and should be treated as somewhat lower confidence than a verified full-text read.

### Towards Accurate and Efficient 3D Object Detection for Autonomous Driving: A Mixture of Experts Computing System on Edge
- Authors: Linshen Liu, Boyan Su, Junyue Jiang, Guanlin Wu, Cong Guo, Ceyu Xu, Hao Frank Yang
- Year: 2025
- Venue: ICCV 2025
- Link/identifier: arXiv:2507.04123
- Access level: abstract read (arXiv abstract-page fetch)
- Problem: Achieve both low latency and high accuracy for 3D object detection on autonomous-vehicle edge hardware, beyond what a single fixed model can offer.
- Representation: Multimodal fusion of LiDAR point clouds and camera imagery via an "adaptive multimodal data bridge" performing multi-scale preprocessing.
- Resolution strategy: Multi-scale preprocessing (exact resolution-adaptivity mechanics not detailed in the accessible abstract) feeding a **content- and distance-aware expert-routing** system.
- Adaptive mechanism categor(y/ies): **Adaptive neural computation** — "a scenario-aware routing mechanism that dynamically dispatches features to dedicated expert models based on object visibility and distance" (DIRECT, verbatim) is a mixture-of-experts architecture, i.e., conditional computation driven by scene content and distance jointly.
- Perception method: Learned, multimodal (LiDAR + camera), mixture-of-experts detection.
- Terrain/dynamic-object/temporal handling: Not addressed (generic on-road 3D detection benchmark).
- Uncertainty handling: Not addressed.
- Computational characteristics (DIRECT, verbatim): "3.58% average [accuracy] improvement on KITTI compared to 15 baselines," "159.06% inference speedup on Jetson platforms."
- Datasets: KITTI (primary), nuScenes (validation).
- Evaluation: Accuracy comparison against 15 baselines plus edge-hardware inference-speed comparison.
- Limitations: Not stated in the accessible abstract.
- Relevance to SIH problem: Another 2025 example (alongside Agile3D) of **distance- and content-aware conditional computation** delivering large, quantified real-edge-hardware speedups (159% on Jetson) with simultaneous accuracy gains — reinforces that adaptive *computation* routing (as distinct from adaptive *map resolution*) is a well-supported, high-payoff strategy for the SIH's real-time/resource-constrained pillar.
- Evidence level(s): DIRECT for all quantitative claims (verbatim abstract).

### DFPS: An Efficient Downsampling Algorithm Designed for the Global Feature Preservation of Large-Scale Point Cloud Data
- Authors: Jiahui Dong, Maoyi Tian, Jiayong Yu, Guoyu Li, Yunfei Wang, Yuxin Su
- Year: 2025
- Venue: Sensors (Basel), vol. 25, issue 14, article 4279
- Link/identifier: DOI 10.3390/s25144279 (PMC12298887)
- Access level: full article read (PMC full-text fetch succeeded)
- Problem: Standard farthest-point sampling (FPS) has exponential-ish cost that becomes prohibitive on large-scale point clouds (millions of points); naive alternatives (random, voxel) degrade edge/global feature quality.
- Representation: Point cloud, downsampled via an adaptive multi-level octree-like grid subdivision whose partitioning depth adjusts to local point density and terrain complexity, followed by two-stage (local-then-global) FPS.
- Resolution strategy: **Adaptive/hierarchical, driven by local point density and geometric complexity** — a directly on-topic example of adaptive computational representation applied to raw point-cloud downsampling.
- Adaptive mechanism categor(y/ies): **Adaptive computational representation** (per-region partitioning depth varies with local density/complexity).
- Perception method: Classical/geometric (no neural network); multithreaded parallel implementation.
- Terrain handling: Directly relevant — one of the two real-world evaluation datasets is airborne/marine bathymetric LiDAR terrain survey data.
- Dynamic-object handling: Not addressed (offline downsampling of static scans).
- Temporal processing: Not addressed.
- Uncertainty handling: Not addressed.
- Computational characteristics (DIRECT, measured on Intel i7-9750H, verbatim from the paper's own reported timings): at 1M points and 12.5% sampling rate, plain FPS took ~161,665 seconds vs. DFPS's ~71.6 seconds (~2,260× speedup); at 3.125% sampling rate, plain FPS took ~35,000,000 seconds vs. DFPS's ~3.78 seconds (~9,278× speedup). **Critically, for small point clouds (e.g., 512 points), the paper explicitly states**: "for smaller point clouds, due to unavoidable inherent computational overheads such as hierarchical grid calculations and decomposition, the speed advantage of the adaptive hierarchical grid partitioning sampling logic employed by DFPS is not significant" — and quantifies this overhead as being "at the level of 10⁻¹ milliseconds," which the authors judge negligible for practical engineering use.
- Datasets: Marine bathymetric LiDAR (MAPPER-20kU, 6-8M points), airborne land survey (VSurs-ARL, 8.5M points, partial campus view).
- Evaluation: Chamfer-distance fidelity vs. plain FPS across 2.5%-20% sampling rates, plus wall-clock timing vs. FPS, FPS-with-multithreading-only, voxel downsampling, and uniform downsampling.
- Limitations (DIRECT, verbatim/paraphrased from the paper): the authors state they lack a comparison against GPU-accelerated FPS implementations or other hierarchical sampling baselines beyond their own multithreaded FPS variant, and note the adjustable weighting parameter (β) and threshold formulas require empirical tuning without a general sensitivity analysis.
- Relevance to SIH problem: **The single most quantitatively precise piece of evidence in this file for H5, cutting both ways.** It provides a rare, fully-measured, order-of-magnitude (up to ~9,278×) real speedup from an adaptive/hierarchical spatial data structure over a naive baseline on large real-world LiDAR/terrain data — strong support for "adaptive [computational] resolution reduces computation." But it **explicitly documents the overhead-cancels-benefit failure mode this project's CLAUDE.md specifically asks to check for**: at small scale, the bookkeeping cost of the adaptive hierarchical structure erases the speed advantage. The paper's own mitigation is simply to say the absolute overhead is small in absolute time — which is a reasonable practical answer, but is not the same as proving the *relative* overhead is always negligible (it explicitly is not, at small scale, in their own numbers). Note also this compares against a **naive, unaccelerated FPS baseline**, not a GPU-accelerated or otherwise already-optimized one, which the authors themselves flag as an evaluation gap — meaning the reported multi-thousand-x numbers likely overstate the advantage over a well-engineered non-adaptive baseline.
- Evidence level(s): DIRECT for all timing numbers and the small-cloud-overhead caveat (full text read, verbatim/paraphrased quotes); DERIVED caution about baseline strength (the authors' own stated limitation, generalized by this reviewer into an evaluation-validity caveat).

---

## Hypothesis Verdicts

### H3: "Semantic-aware adaptive resolution may be an unexplored opportunity"
- **Verdict: Weakened.**
- The strict claim that semantic-driven adaptive spatial resolution/density is "unexplored" does not survive this search. At least three papers directly contradict "unexplored" as a literal claim: **PointSplit** (arXiv:2504.03654) implements explicit "2D semantics-aware biased point sampling" for on-device 3D object detection; **E2-BKI** (arXiv:2509.11964, RA-L 2025/2026) uses geometry/scene-structure-adaptive kernels fused with per-point *semantic-confidence* uncertainty for outdoor semantic mapping; and **FOVEA** (ICCV 2021) establishes, in the camera domain, that saliency/task-driven (semantically-flavored) variable-resolution perception with measured accuracy and streaming-AP benefits is a solved, published, half-decade-old idea. **Fast Attention-Based Simplification of LiDAR Point Clouds** (arXiv:2603.07593) further shows a 2026 learned "task-relevant region" attention sampler specifically for LiDAR.
- However, none of these is exactly the SIH's target combination: a **persistent, spatially-varying-resolution 2.5D elevation/occupancy MAP for a mobile ground robot, whose resolution is driven by an explicit semantic-class label** (e.g., "pedestrian → fine, empty road → coarse") rather than by scene geometry, saliency proxies, or a generic point-sampling attention score. PointSplit and the attention-sampling papers operate on the *raw point cloud feeding a per-frame detector*, not a persistent map; E2-BKI's adaptivity is geometry-driven with semantic uncertainty as a downstream *consumer* of the representation rather than the *driver* of its resolution; FOVEA is camera-only. So a **narrower gap plausibly remains** at the intersection of (persistent map) × (explicit semantic-class-driven resolution) × (LiDAR/2.5D ground-robot setting), even though the broader "semantic/content-aware adaptive resolution" concept is well-established elsewhere. This is a genuine narrowing, not a full disproof — "unexplored" should be replaced with something like "the general mechanism is well-precedented; the specific persistent-map, semantic-class-driven, LiDAR/2.5D combination is not directly demonstrated in what was found."

### H5: "Adaptive map resolution can provide meaningful computational/memory benefits"
- **Verdict: Weakened / Survived-with-caveats (not a clean confirmation).**
- Two pieces of strong, numerically-grounded evidence support H5: **Agile3D** (MobiSys 2025) shows a real embedded-GPU (Jetson Orin/Xavier) system where spatial resolution — as one of five jointly-adapted knobs — contributes to measured accuracy gains of up to +7% over static detectors at matched latency budgets under realistic GPU contention; and **DFPS** (Sensors 2025) shows up to ~9,278× real wall-clock speedup from an adaptive hierarchical point-cloud structure on large real-world terrain LiDAR data.
- But both come with explicit caveats that prevent a clean "confirmed" verdict, matching this project's disconfirming-evidence mandate:
  1. **DFPS's own text states the adaptive-hierarchical overhead erases the speed advantage for small point clouds** — the benefit is scale-dependent, not universal, and the authors themselves did not compare against a GPU-accelerated (i.e., already-optimized) non-adaptive baseline, which likely inflates the reported advantage.
  2. **Agile3D's resolution adaptivity is bundled with four other adaptive knobs** (partitioning format, encoding, feature extractor, detection head) and applies to **per-frame detection, not a persistent map** — so it cannot be read as isolating "adaptive map resolution" specifically as the source of benefit; it is evidence for adaptive *processing*, only partially for adaptive *map* resolution as CLAUDE.md's six-category taxonomy defines it.
  3. **The voxel-efficiency embedded-systems paper** (arXiv:2105.10316) shows that a naive form of "adaptive" (distance-restricted) processing gains 40-60% speed partly *because* distant small objects were already being missed by the full-range model — i.e., some claimed adaptive-resolution "benefit" in the literature is really a byproduct of accuracy already being poor at long range, which is precisely the kind of confound this project's brief asks to watch for, and is direct partial support for the disconfirming hypothesis "coarse distant resolution loses important objects."
  4. The classic **Gaussian Process occupancy map** lineage (O'Callaghan & Ramos 2012) shows that an elegant "arbitrary resolution, anytime" representation existed over a decade ago but has been persistently limited in practice by high computational complexity (per the follow-on "Fast/Efficient GP occupancy" literature that exists specifically to fix this) — a cautionary precedent that adaptive/flexible-resolution representations do not automatically translate into practical computational wins.
- Net assessment: genuine, measured computational benefit from adaptivity (of various kinds, not always cleanly "map resolution" in the strict sense) does exist in current (2023-2025) literature, but it is **conditional on scale, on bundling with other adaptive levers, and on comparison against a fairly-optimized baseline** — the unconditional version of H5 is not well supported, while a qualified version ("adaptive resolution/computation can help, under the right conditions and against a fair baseline, but the benefit is not automatic and can evaporate or be confounded") is well supported.

---

## Terminology/Concept Notes

- **"Foveation" spans a hardware/software divide that is easy to blur.** Tasneem et al. (IJRR 2020) and Pittaluga et al. (3DV 2020) both use "foveated"/"adaptive fovea" to mean the **physical sensor's scan pattern changes** (adaptive sensor acquisition), while FOVEA (ICCV 2021) and the attention-based LiDAR point-cloud papers use essentially the same biological metaphor to mean **software-side resampling/attention of already-captured data** (adaptive attention/ROI). Both lineages cite the same biological inspiration and use overlapping vocabulary ("fovea," "saliency," "attention"), but they are mechanically very different and belong to different categories in this project's six-category taxonomy. Any literature search using "foveated" alone will conflate these unless the hardware/software distinction is checked per-paper.
- **"Content-aware" and "adaptive" resolution, in current systems literature (Agile3D), often means "aware of both scene content AND system/hardware state (contention, latency budget)"** — not purely a perception-quality-driven concept. This is a meaningfully different framing from the SIH problem's original "fine near robot, coarse far away" framing, and from a purely semantic/uncertainty-driven framing: it adds a third driver (system load) that this project's six-category taxonomy does not explicitly name, though it fits loosely under "adaptive computational representation" / "adaptive neural computation."
- **"Risk-aware" is frequently a control/planning-level property, not a spatial-representation property.** The CVaR-MPPI paper (Yin, Zhang, Tsiotras 2022) is the clearest example: it is "risk-aware" in a rigorous decision-theoretic sense but has no spatial map or resolution concept whatsoever. RAMP and RiskMap, by contrast, embed risk directly into the spatial/map representation. Searches on "risk-aware X" will surface both kinds indiscriminately; they must be triaged individually, which this file has done.
- **"Uncertainty" fractures into at least five distinct sub-types across this literature**, all labeled the same way in abstracts but meaning different things: (1) sensor/measurement noise (Elfes-lineage occupancy grids, EviLOG's radar/LiDAR ISM work), (2) occupancy-state probability itself (all classic Bayesian occupancy grids), (3) semantic-classification confidence (E2-BKI), (4) model/epistemic confidence over *predicted or extrapolated* regions beyond current sensing (Uncertainty-driven Planner, SOGMP's future-occupancy prediction), and (5) registration/alignment-fit uncertainty (Uncertainty-Aware VI-SLAM's submap alignment factors). This project's brief specifically asks for this level of precision, and it matters: a system that is "uncertainty-aware" in sense (1) says nothing about sense (4) or (5).
- **"Adaptive resolution" vs. "adaptive sampling/downsampling" vs. "adaptive computation/routing" are used almost interchangeably in abstracts but are mechanically distinct** per this project's six-category taxonomy, and the distinction matters a great deal for H5: DFPS and the attention-based LiDAR simplification papers adapt how a **static point cloud is thinned** (a one-shot, offline-ish operation); Agile3D and the Mixture-of-Experts edge-detection paper adapt **which computation graph runs per frame** (no persistent spatial structure at all); RAMP, RiskMap, E2-BKI adapt or use a **persistent representation's content/uncertainty** but not always its resolution in the strict grid-cell-size sense. None of the three families is a substitute evidence source for either of the other two when assessing whether *map resolution specifically* helps.

---

## Papers Considered But Excluded

- **"Lightweight 2.5D SLAM with Dynamic Map Refinement and Height-Aware Encoding for Resource-Constrained Indoor Robots"** (Sensors 2026, vol. 26, issue 15, article 4765) — fetched in full during this search, but its DOI (10.3390/s26154765) and file characteristics exactly match `sensors-26-04765.pdf`, one of the eight papers already supplied in `papers/` and analyzed under Phase 1. Excluded here to avoid double-counting a supplied paper as "external literature"; flagged for the research coordinator in case Phase 1's analysis of this paper should be cross-checked against the following details recovered here: fixed (not spatially variable) planar grid resolution with a uniform 24-bin vertical occupancy encoding; "dynamic map refinement" is explicitly **offline post-processing artifact removal**, not general online dynamic-object SLAM (the authors' own stated limitation); tested on a Sunrise X3 embedded ARM Cortex-A53 board (5 TOPS, 4GB RAM) with front-end ~0.88s and back-end ~2.21s average per keyframe, peak memory 130-133MB.
- **AS-Net: An attention-aware downsampling network for point clouds oriented to classification tasks** (ScienceDirect) — paywalled; only a brief, non-independently-verifiable search snippet was available. Excluded from the main paper list rather than reported as if read; mentioned only in passing in the search-summary discussion above.
- **An overview of space-variant and active vision mechanisms for resource-constrained human-inspired robotic vision** (Autonomous Robots 2023) — included above but explicitly flagged snippet-only; Springer and ACM DL both returned authentication walls (403/redirect) and could not be independently verified.
- **Agile3D primary sources (ACM DL PDF, preprint-host PDF)** — both returned HTTP 403/empty content; substituted with the project's own GitHub README (which does contain concrete numeric results) plus an independent Purdue University press release and cross-consistent WebSearch summaries, all disclosed as such rather than presented as a primary-PDF read.
- **Various USPTO patent documents** (e.g., "Method and system for collaboratively detecting tangible bodies," "Environment sensing method and apparatus using a wide-angle distance sensor," "Image space motion planning of an autonomous vehicle" series, "Multi-beam laser scanner with programmable field of view," "Method of providing interference reduction and a dynamic region of interest in a LIDAR system") — surfaced repeatedly in searches on risk-aware cost maps and adaptive-scan LiDAR hardware. Excluded as non-primary-literature (patents are not peer-reviewed technical evidence and often describe prophetic/aspirational claims rather than demonstrated results); noted only as a signal that adaptive-ROI LiDAR scanning is commercially/IP-relevant, not as technical evidence.
- **Hierarchical Point Attention for Indoor 3D Object Detection** (arXiv:2301.02650) and **Analysis of voxel-based 3D object detection... (2105.10316) full PDF** — surfaced with promising titles but not independently fetched/verified in full (the latter's PDF fetch failed and only abstract-level summary was used, disclosed in its entry above); the former was not fetched at all due to time/scope budget after sufficient paper count was reached for this family — noted here rather than silently omitted.
- **ResearchGate mirror pages** (used to *locate* several papers, e.g. Ada3D, AS-Net, various traversability surveys) — never used as the cited source of technical claims; used only to confirm a paper's existence/venue before locating and fetching the arXiv or publisher original.
