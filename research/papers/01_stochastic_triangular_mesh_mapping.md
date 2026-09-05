# Stochastic Triangular Mesh Mapping: A Terrain Mapping Technique for Autonomous Mobile Robots — Deep Analysis

**Source file:** `papers/1910.03644.pdf`
**Analyzed:** Phase 1 (supplied-paper analysis), single-paper deep read.

Full document read (39 pages, all rendered/viewed, including all figures, tables, and the reference list), in three chunks (pp.1-15, 16-30, 31-39).

---

## 1. Problem being solved

The paper addresses **online dense metric mapping for autonomous mobile robots operating in initially unknown, general environments** (p.2, Introduction). The authors frame the requirements for an effective dense map (following Guizilini & Ramos) as: reasoning under uncertainty, incremental updates, efficient update/query, and representing environmental structure (p.2). DIRECT EVIDENCE (p.2).

Two specific sub-problems are targeted: (1) how to account for **robot pose (localisation) uncertainty** when building a dense map without expensive retroactive map correction on loop closure, and (2) how to model **statistical dependence/continuity between neighbouring map elements** at tractable (linear) computational cost, which most existing dense-mapping techniques assume away (p.2). DIRECT EVIDENCE.

The paper explicitly is about **terrain/surface mapping**, not object detection, semantic understanding, or dynamic-scene perception. DIRECT EVIDENCE (Title, Abstract, p.1).

## 2. Sensors and input data

Sensors: **LiDAR and stereo cameras** (Abstract, p.1: "sensors that generate point measurements, such as light detection and ranging (LiDAR) sensors and stereo cameras"). DIRECT EVIDENCE.

Practical experiments used:
- A stereo rig of two 1.3MP FLIR Flea3 GigE cameras, 18cm baseline, with disparity computed via LIBELAS stereo matching, then converted to noisy 3-D point measurements via the unscented transform; 525,331 point measurements from three stereo image pairs (Section 6.4, p.32). DIRECT EVIDENCE.
- LiDAR data from the "box_met" Canadian planetary emulation terrain dataset (Tong et al. 2013): ~19.04×10^6 LiDAR measurements from 112 poses, aligned with a differential GPS (DGPS) (Section 6.5, p.32). DIRECT EVIDENCE.
- Synthetic data generated with Perlin noise for simulated 2-D and 3-D surfaces, with simulated Gaussian-noise measurements (Section 6.1-6.3, pp.27-31). DIRECT EVIDENCE.

## 3. Input representation

Input is a sequence of **noisy 3-D point measurements** ("Noisy 3-D point measurements" in the Graphical Abstract, p.1), modelled via a generic sensor beam model: a measurement z^B is a noisy observation of an actual surface point m^B in the robot body reference frame (Eq. 5, p.9). No raw range images, occupancy voxels, or images are used internally — sensors are only required to "produce point measurements" (p.36, Conclusions) for the technique to apply. DIRECT EVIDENCE.

## 4. 2D / 2.5D / 3D representation

The paper explicitly states, and the model structurally confirms, a **2.5-D representation**: "a 2.5-D representation of the surface of the environment using a continuous mesh of triangular surface elements" (Abstract, p.1). This is structurally verified, not just asserted in prose, by Eq. (9) (p.13): a surface point is γ = f(α,β,h) + ε — a single scalar height value γ per horizontal-plane coordinate (α,β), with ε a stochastic (homoscedastic) deviation. This single-height-per-location constraint is the defining property of 2.5D (cannot represent overhangs/multiple height values at one planar location). DIRECT EVIDENCE (Eq. 9, p.13; Fig. 4b, Fig. 6, Fig. 7 all show single-valued height-field meshes, not volumetric/point-cloud data).

Note (INFERENCE): the "horizontal plane" here is the **submap's own (α,β) plane**, spanned by vectors **a**, **b** derived from three landmarks (Eq. 3-4, p.8), which need not be gravity-horizontal in the global frame — each submap can be tilted arbitrarily. So it is 2.5D relative to a locally-defined plane, not necessarily a global horizontal plane.

The authors themselves state as an explicit limitation that STM is 2.5D and NOT a general 3D representation: "An STM map is a 2.5-D representation of the surface of the environment; however, to handle 3-D general environments, future work will look at extending the representation accordingly" (p.36). DIRECT EVIDENCE.

## 5. Spatial/map representation

The map is a **continuous stochastic triangular mesh (STM)**: a collection of triangular surface elements ("surfels"), each modelling a mean plane plus a homoscedastic planar-deviation (roughness) term, joined at shared vertex heights so that the mean mesh is continuous across element boundaries (Section 4, Fig. 4, Fig. 7, pp.12-14). DIRECT EVIDENCE. This sits inside a **submapping** scheme (Hybrid Metric Map / HYMM, extended to 3-D by the authors): the environment is partitioned into triangular regions demarcated by SLAM-derived landmarks, each submap having its own relative inertial reference frame (IRF) (Section 3, Fig. 1, pp.7-8). DIRECT EVIDENCE.

## 6. Resolution strategy

Each triangular submap is recursively subdivided into equisized triangular grid elements down to a chosen fixed grid-element size (Fig. 5, p.13). This target size is chosen **a priori**, e.g., "based on the dimensions and physical capability of the robot" (p.12). DIRECT EVIDENCE. Resolution is **uniform within a submap** (not distance-based, not per-region), and is chosen once before mapping, not varied during operation. DIRECT EVIDENCE (p.12; confirmed by Section 6.1-6.3 experiments where "grid division depth" is a fixed experimental parameter applied uniformly).

## 7. Whether resolution is adaptive and how

**Not adaptive.** The paper explicitly states the current implementation uses fixed grid-element sizes and that adaptive subdivision is **future work, not implemented**: "Depending on the application, this could be simply chosen based on the dimensions and physical capability of the robot. In general, it would be more sensible to perform this partitioning in an adaptive manner, although we do not address this in the current implementation, but will discuss in future work" (p.12). This is reiterated in Section 7.1 (Future Work, p.36): "future work will look at adaptively subdividing the grid. Surfels with very low planar deviations could be grouped into a coarser resolution and, conversely, surfels with high planar deviations could be subdivided into a finer resolution. This, however, would add complexity to the inference process." DIRECT EVIDENCE.

**ADAPTIVE SENSING vs ADAPTIVE MAP RESOLUTION:** Neither is implemented. Sensing is passive/fixed (stereo camera and LiDAR used as generic point-measurement sources with no controllable FOV/scan-pattern discussion). The proposed (unimplemented) future adaptivity would be **map/computational resolution** adaptation driven by the *planar-deviation (roughness) statistic* of the surfel — i.e., a surface-uncertainty/roughness-driven criterion, NOT a distance-from-robot criterion. INFERENCE/DERIVED from p.36 text (the future-work text names planar deviation, not range, as the adaptivity signal).

## 8. Spatial data structure

A **continuous triangular mesh**, built by (a) a landmark-triangulation network (Delaunay-like triangulation over SLAM landmarks) defining submap regions (Fig. 1a, p.8), and (b) recursive equisized subdivision of each triangular submap into finer triangular grid elements (Fig. 5, p.13), each holding one surfel. This is not a regular square/cubic grid, not an octree, not a k-d tree, and not a point cloud/voxel grid. DIRECT EVIDENCE (Section 3, Section 4, Fig. 1, Fig. 5).

## 9. Height/elevation representation

Each grid element's surfel is parameterised by θ = [h, ν]ᵀ: **h** = [h₀, h_α, h_β]ᵀ, the heights at the three triangle vertices defining a mean plane, and **ν**, a scalar homoscedastic planar-deviation (variance) term describing the stochastic roughness of the actual surface about that plane (Eq. 9-10, Fig. 6, pp.12-13). DIRECT EVIDENCE. Heights are modelled as **Gaussian-distributed** random variables and planar deviation as **inverse-gamma distributed** (p.13-14, confirmed in the PGM/inference derivation, Eq. 25-26, p.18). Adjacent surfels share vertex heights, enforcing C⁰ continuity of the mean mesh (Fig. 7a, p.14) — but planar deviations between adjacent surfels are NOT constrained to be continuous/equal (p.14). DIRECT EVIDENCE.

## 10. Semantic information

**Not reported.** No semantic class labels, object categories, or learned semantic features are produced or consumed anywhere in the paper. The only "semantic-like" signal is the scalar planar-deviation (roughness) value per surfel, which the authors suggest — but do not demonstrate — "could be used as a measure of terrain drivability" (p.32). This is explicitly flagged by the authors themselves as undemonstrated: "Although we propose the terrain roughness as a possible metric for drivability analysis, we do not demonstrate this" (p.36, Future Work). HYPOTHESIS (per the authors' own framing), not demonstrated capability.

## 11. Terrain analysis

**Not solved/demonstrated**, only motivated as a potential future use. The map's planar-deviation ("roughness") field is qualitatively shown to correlate with visually rough terrain features (gravel heap, rock outlines) in Figs. 16 and 17 (pp.33-35) — DIRECT EVIDENCE that roughness correlates visually with terrain irregularity in the demonstrated scenes. However, no traversability classification, no drivable/non-drivable labelling, no thresholding, and no quantitative terrain-analysis evaluation is performed anywhere in the paper. The authors explicitly state this is future work requiring "specialised planning algorithms to exploit the rich environment representation" (p.36). DIRECT EVIDENCE that terrain analysis as a task is NOT solved by this paper.

## 12. Static-object perception

**Not addressed as a distinct task.** The STM map represents the terrain surface as a continuous height field; static objects appearing as bumps/depressions in that height field (e.g., rocks, a gravel heap, a container/manhole-like structure in Fig. 16b/16f/16j, small rocks in Fig. 17a-d) are visible as geometric features in the mesh, but there is **no object detection, segmentation, bounding-box extraction, or classification** performed. INFERENCE from visual inspection of Figs. 16-17 combined with DIRECT EVIDENCE that the method only outputs a continuous height/roughness surface (Section 4).

## 13. Dynamic-object perception

**Not addressed; explicitly out of scope.** The method assumes a **static environment** throughout — this is confirmed as an explicit stated limitation: "As most environments with practical significance are not static, it would be desirable to relax the static environment assumption. Future work will look at incorporating temporal information into the map to facilitate this" (p.36, Section 7.1). DIRECT EVIDENCE. No dynamic-object detection, segmentation, or filtering mechanism exists in the current method.

## 14. Temporal processing

Limited to **incremental batch updating of a single (assumed static) map** over successive measurement batches/time steps, using a sliding window of the W most-recent measurement batches, after which older-measurement messages are folded into the prior and discarded to bound storage (Section 5.3, "Incremental updating," p.25). DIRECT EVIDENCE. This is temporal incorporation of *more evidence about a static scene*, not temporal modelling of scene *change* — no motion model, no filtering of moving entities, no per-timestep dynamic-state estimate. DERIVED.

## 15. Tracking

**Not reported.** No object-level or feature-level tracking is performed. (SLAM-derived landmark tracking for pose estimation is assumed as an external input, not part of the STM contribution itself — see item 17.)

## 16. Uncertainty handling

This is a central, deeply developed contribution. The paper models uncertainty from **two sources**: (a) measurement/sensor uncertainty (heterogeneous, sensor-model-derived noise covariances, Section 3.2, Eq. 5-8) and (b) robot pose/SLAM uncertainty, which is handled by transforming measurements into a **landmark-relative IRF**, exploiting the empirical near-perfect correlation between nearby SLAM landmark positions to approximately decouple map inference from pose belief (Section 3, Fig. 2, Fig. 3, pp.7-12). DIRECT EVIDENCE, including a validation using real stereo-vision SLAM data showing near-zero residual correlation between pose/landmark states and the relative-frame surface points (Fig. 3a-b, p.11).

Surfel parameters (heights, planar deviation) are treated as Bayesian random variables with explicit priors and posteriors (Gaussian for heights, inverse-gamma for planar deviation), inferred via a hybrid **variational message passing (VMP) + loopy belief propagation (LBP)** scheme over a cluster-graph probabilistic graphical model (Sections 5.1-5.3, pp.15-26). The approximate inference is validated against MCMC (Metropolis-Hastings) ground-truth posteriors for representative stereo-like and LiDAR-like sensor noise regimes, showing close agreement (Fig. 9, p.22), except when "measurement uncertainty is unreasonably high," where linearisation errors cause noticeable divergence from the exact belief (p.21, footnote 16). DIRECT EVIDENCE.

## 17. Localization / SLAM dependency

**Strong dependency.** The method requires an external SLAM system to supply a **sparse landmark map** (with its own belief/uncertainty) that (a) triangulates the submap regions and (b) defines each submap's relative IRF (Section 3, p.7-8). DIRECT EVIDENCE. The authors explicitly flag as an open problem that landmarks must be "robustly and persistently identifiable" in general environments, which "is still ... an open problem for general environments" (p.8). DIRECT EVIDENCE. In the practical demonstrations, this dependency was **not exercised with a real online SLAM pipeline**: Section 6.4 used manually placed ArUco fiducial markers as landmarks (not naturally-extracted SLAM landmarks) (p.32), and Section 6.5 used poses given directly by differential GPS, bypassing SLAM landmark estimation entirely (p.32). DIRECT EVIDENCE that no experiment demonstrates the full pipeline with live, naturally-extracted SLAM landmarks feeding the relative-IRF submapping. INFERENCE: this leaves the core "landmark identifiability" assumption experimentally unvalidated for general/unstructured environments.

## 18. Learning/neural-network components

**None.** The method is a classical **probabilistic graphical model** (Bayesian network / factor graph / cluster graph) with analytic Bayesian inference (variational message passing and loopy belief propagation over Gaussian and inverse-gamma distributions), not a learned/neural approach (Section 5, pp.15-26). DIRECT EVIDENCE.

## 19. Computational requirements

Asymptotic complexity is stated as **O(KN)**, where K is the number of message-passing iterations to convergence (empirically observed to be roughly constant with respect to N) and N is the total number of measurements incorporated — so the algorithm is "approximately linear in N" (p.26, Section 5.3, "Computational complexity"). DIRECT EVIDENCE. This is empirically supported (not just asserted) by two simulated cost-of-inference experiments measuring the number of messages passed under (a) a shrinking newly-observed region (linearly decreasing message count, near-constant when normalised per new measurement, Fig. 12, p.29) and (b) a repeatedly-observed fixed region (exponentially decreasing message count as belief converges, Fig. 13, p.30). Message/factor dimensionality is stated to be low (at most 6-D) and is argued not to be a computational bottleneck (p.28). DIRECT EVIDENCE.

## 20. Runtime/FPS/latency if reported

Only a single approximate figure is reported: an **unoptimised Python implementation takes ≈3 ms per measurement** to update an STM map, based on a later experiment (Section 6.5) that used 19 million measurements (p.28, footnote 20). DIRECT EVIDENCE. No FPS number, no end-to-end system latency (sensing→map-ready), and no CPU/GPU hardware specification are reported anywhere in the paper. This is explicitly caveated by the authors as a preliminary number: "we expect significantly faster results with an efficient implementation" (p.28).

## 21. Memory/map-size results if reported

No byte/MB memory-footprint figures are reported anywhere. Map sizes are reported only in **surfel counts**: 1024 surfels for the single-submap 2-D/3-D simulation experiments (Sections 6.1-6.3); 256 surfels per submap (two submaps) for the practical stereo-camera experiment (Section 6.4, p.32-33); and 65,536 surfels per submap (two submaps) for the practical global-IRF LiDAR experiment (Section 6.5, p.32). DIRECT EVIDENCE for surfel counts; "Not reported" for absolute memory usage or any memory comparison against alternative mapping techniques (e.g., occupancy grids/OctoMap).

## 22. Dataset and experimental setup

Three experimental regimes, all described in Section 6 (pp.27-35):
1. **Simulated 2-D/3-D surfaces** generated via Perlin noise, with synthetic point measurements and heterogeneous, randomly-rotated Gaussian noise, used to study (a) prior-correlation effects (Section 6.1, Fig. 11), (b) inference cost under two motion scenarios — advancing push-broom sampling and repeated re-observation (Section 6.2, Figs. 12-13), and (c) STM-vs-elevation-map accuracy across grid division depths, including a 10-environment batch 3-D study (Section 6.3, Figs. 14-15). DIRECT EVIDENCE.
2. **Practical stereo-camera dataset**: 3 pairs of stereo images (FLIR Flea3 GigE, 1.3MP, 18cm baseline), LIBELAS disparity, unscented-transform 3-D point extraction, ArUco fiducial markers as landmarks, 525,331 point measurements, two submaps of 256 surfels (Section 6.4, Fig. 16). DIRECT EVIDENCE.
3. **Practical LiDAR dataset**: the "box_met" Canadian planetary emulation terrain 3-D mapping dataset (Tong et al. 2013), a 60×120 m outdoor Mars-emulation area, ~19.04×10^6 LiDAR points from 112 DGPS-aligned poses, mapped in a **global** (not relative) IRF, two submaps of 65,536 surfels each (Section 6.5, Fig. 17). DIRECT EVIDENCE.

## 23. Evaluation metrics

- Mean squared error (MSE) of the mapped surface against ground truth (Section 6.3, Figs. 14a, 15a). DIRECT EVIDENCE.
- Log-likelihood ratio between the STM map and the elevation-map baseline along the ground-truth surface (Figs. 14b, 15b). DIRECT EVIDENCE.
- Message-passing count as a proxy for computational cost (Figs. 12b, 13). DIRECT EVIDENCE.
- Pearson correlation coefficient (matrix visualisations) to demonstrate the statistical decoupling achieved by the relative-IRF transform (Figs. 2, 3a-b). DIRECT EVIDENCE.
- Exclusive KL divergence, used both (a) as the message-passing convergence criterion (Section 5.3) and (b) to visualise incremental belief change across the map over time (Fig. 12c). DIRECT EVIDENCE.
- Qualitative visual/contour comparison of the approximate inference algorithm's surfel belief against MCMC (Metropolis-Hastings) samples of the exact belief (Fig. 9) — this is a qualitative/visual check, not a single scalar metric. DIRECT EVIDENCE.

## 24. Baselines and ablations

The only quantitative baseline comparison is against a **standard elevation map** (each cell height updated with a 1-D Kalman filter, following Triebel et al. and Fankhauser et al.), performed in Section 6.3 across a range of grid-division depths, in both 2-D (Fig. 14) and a 10-environment 3-D batch (Fig. 15). DIRECT EVIDENCE. The authors justify this narrow baseline choice: NDT mapping does not model measurement uncertainty and GP mapping is computationally intractable online, so only elevation mapping is a "suitable candidate" for comparison (p.29). No experimental comparison is made against occupancy grids, OctoMap, SDF/KinectFusion-style maps, Hilbert maps, or GP maps — these are discussed only qualitatively in the related-work survey (Section 2, Table 1). No formal ablation study (e.g., removing the continuity constraint, varying window size W, or varying the prior correlation ρ as a controlled ablation) is reported; Fig. 11's variation of ρ is an illustrative sensitivity plot rather than a performance ablation.

## 25. Failure cases

Two degradation modes are explicitly documented:
1. When measurement uncertainty is large relative to the grid-element size, the linearised VMP approximation "differs noticeably from the exact belief" compared to MCMC ground truth (p.21, Section 5.1.3, and footnote 16: "too fine a grid division could result in a measurement distribution that spans several grid elements"). DIRECT EVIDENCE.
2. Both STM and elevation-map accuracy **degrade past a certain grid-division depth** (MSE increases for grid divisions >6 for STM, >7 for elevation maps in the 2-D experiment), attributed to measurement noise becoming large relative to grid-element size and fewer measurements falling per element (p.30, Section 6.3, visible in Fig. 14a/14c at depth 8). DIRECT EVIDENCE.

## 26. Explicit limitations

Stated directly by the authors (Section 7, Conclusions and Future Work, p.36):
- Fixed-size grid elements are "an inefficient use of storage" for large homogeneous regions (motivating unimplemented future adaptive gridding).
- The static-environment assumption is unrealistic for most practically significant environments.
- Submaps are treated independently, and because each submap lies on a different landmark-defined plane, "the partitioning of 3-D space between neighbouring submaps will contain overlapping- or dead-zones," unhandled in the current work.
- STM is fundamentally a **2.5-D** representation; extending to general 3-D is left to future work, and the authors note a fully probabilistic 3-D triangular meshing approach "will most likely be intractable" for online use.
- LBP-based inference has **no proven convergence guarantee** (only VMP is guaranteed to converge); convergence was only supported empirically, not proven.
- Landmark identifiability for defining relative IRFs "is still ... an open problem for general environments" (p.8).
All DIRECT EVIDENCE.

## 27. Future work

Explicitly listed in Section 7.1 (p.36):
1. Adaptive grid subdivision driven by surfel planar deviation (coarser for low-roughness regions, finer for high-roughness regions), noted to add inference complexity.
2. Incorporating temporal information to relax the static-environment assumption.
3. Developing specialised planning algorithms to exploit the STM representation (e.g., using roughness for drivability) for navigation — not yet done.
4. Handling overlapping/dead zones at submap boundaries.
5. Extending the representation to general 3-D (e.g., via 3-D triangular meshing), flagged as likely intractable online if done in a fully probabilistic manner.
6. A principled convergence analysis of the hybrid VMP+LBP inference algorithm.
All DIRECT EVIDENCE.

## 28. What the method does NOT solve

- Object detection or classification of any kind (static or dynamic).
- Semantic labelling/segmentation.
- Dynamic-object detection, motion estimation, or tracking (explicitly assumes a static scene).
- Terrain traversability/drivability classification (only motivated, not demonstrated; explicitly flagged by the authors as undemonstrated).
- Adaptive/variable spatial resolution (explicitly deferred to future work).
- General (non-2.5D) 3-D geometry, e.g., overhangs, tunnels, or multi-valued height regions.
- Automatic, general-environment landmark extraction feeding the relative-IRF submapping (practical demos used artificial fiducial markers or externally-supplied DGPS poses instead of a live SLAM landmark pipeline).
- Path planning or collision-avoidance algorithms (mentioned only as motivating context, e.g., citing [40, 41]).
- Proven convergence of its own inference algorithm.
DIRECT EVIDENCE / DERIVED, consolidated from items 10-17, 25-27 above.

## 29. Relevance to the fixed SIH problem

(Relevance only — no architecture recommendation.)

- **Terrain analysis:** Low direct relevance. The paper produces a continuous surface + a roughness (planar-deviation) statistic that visually correlates with rough terrain in the demonstrated scenes (Figs. 16-17), but explicitly does **not** perform drivable/non-drivable classification or any traversability evaluation — this remains an undemonstrated hypothesis in the source paper itself (p.36). INFERENCE: this technique could, at most, supply a *roughness feature* as one possible input to a terrain-analysis module, but is not itself a terrain-analysis solution.
- **Static/dynamic object detection:** Essentially no relevance. The paper has no object-level representation, detection, or classification mechanism, and explicitly assumes a static environment throughout, with dynamic-object handling named only as unaddressed future work (p.36). It offers no method transferable to detecting walls, poles, pedestrians, or vehicles.
- **Adaptive variable-resolution 2.5D spatial representation:** This is the pillar of the SIH problem to which the paper is most relevant, but only partially: STM is confirmed to be a genuine **2.5D** map representation (structurally, via Eq. 9, not just by prose) using a continuous triangular mesh with explicit per-element uncertainty (height + planar deviation) — a concrete alternative to elevation maps/occupancy grids for representing 2.5D surfaces with continuity and calibrated uncertainty. However, the paper's resolution is **fixed and uniform**, not adaptive; adaptive (roughness-driven, not distance-driven) resolution is explicitly proposed but **not implemented or evaluated** (p.12, p.36). It therefore illustrates one candidate spatial data structure and uncertainty-handling approach relevant to the representation pillar, and separately illustrates (via the submapping/relative-IRF mechanism) a technique for decoupling pose (localisation) uncertainty from map-element uncertainty — relevant background for any localisation-dependent variable-resolution scheme — but it does not itself solve, or experimentally validate, adaptive resolution.

## Figures/Tables/Equations Directly Consulted

- **Table 1** (p.6) — comparison of 7 existing mapping techniques (Polygonal Mesh, Occupancy Grid, Elevation, SDF, NDT, GP, Hilbert) plus STM across 5 attributes (uncertainty, incremental updates, update efficiency, statistical dependencies, explicit surface).
- **Fig. 1** (p.8) — (a) HYMM landmark-triangulation submapping network with a robot inside one triangular submap; (b) 3-D relative-IRF construction diagram showing point **m** expressed via basis vectors a, b, n from landmarks l₀, l_α, l_β.
- **Fig. 2** (p.10) — four scatter/ellipse plots showing how Pearson correlation ρ (0, 0.5, 0.95, 1) affects consistency of sampled triangle shapes for 3 correlated 2-D landmarks.
- **Fig. 3** (p.11) — (a),(b) correlation-coefficient heatmaps for B(x,L,M) vs B(x,L,Mᴿ) showing decoupling after relative-IRF transform; (c) scatter/ellipse comparison of belief uncertainty (relative vs ideal vs global-transformed) on real stereo data.
- **Fig. 4** (p.12) — (a) cartoon hill/house/tree environment; (b) corresponding STM mesh coloured by planar deviation.
- **Fig. 5** (p.13) — recursive triangular-grid subdivision diagram, depths 0-2.
- **Fig. 6** (p.13) — surfel model: 3-D triangular grid element with mean-plane heights h₀,h_α,h_β and planar deviation; 2-D slice showing shaded ±1-std band around orange mean vs green "actual" wiggly surface.
- **Fig. 7** (p.14) — (a) mean-mesh graph with landmark triangulation overlay; (b) 1-D slice of a multi-element STM map (orange mean ± std band) vs green ground-truth curve, showing continuity across surfels.
- **Fig. 8** (p.16) — (a) Bayesian network for the surfel model with plate notation; (b) equivalent factor graph; (c) equivalent cluster graph with message/potential notation.
- **Fig. 9** (p.22) — 2×3 grid of scatter/contour plots comparing VMP-approximated surfel belief (orange) vs MCMC ground-truth samples (blue) for stereo-like (a-c) and LiDAR-like (d-f) noise regimes.
- **Fig. 10** (p.24) — (a) zoomed section of the full-map cluster graph showing sepset/cluster connectivity over the triangular mesh; (b) detailed message-flow diagram around one surfel's cluster potential.
- **Algorithm 1** (p.26) — full pseudocode for STM map inference (message initialisation, LBP incoming-message update, VMP likelihood-cluster update, outgoing-message update, convergence loop).
- **Fig. 11** (p.28) — mean-mesh height profile extrapolation beyond an observed region for a range of prior correlation coefficients ρ (color-coded).
- **Fig. 12** (p.29) — (a) triangular time-step diagram of shrinking sampling regions; (b) message-count and normalised message-count vs time step; (c) KL-divergence heatmaps over the triangular map at t0, t5, t10, t15.
- **Fig. 13** (p.30) — message count vs time step for repeated observation of the same region, showing exponential decay.
- **Fig. 14** (p.31) — (a) MSE vs grid-division depth, STM vs elevation map; (b) log-likelihood ratio vs grid-division depth; (c) 4-panel visual comparison (ground truth, STM, elevation map) at depths 0, 4, 6, 8.
- **Fig. 15** (p.31) — 3-D batch (n=10) MSE and log-likelihood-ratio vs grid-division depth, with error bars, STM vs elevation map.
- **Fig. 16** (p.33) — (a) 3-panel top-down map of measurement count, planar deviation, and height for the stereo-camera experiment; (b)-(m) 3 rows (front/side/rear viewpoints) × 4 columns (photo, measurement-count map, planar-deviation map, height map), showing occlusion effects per viewpoint.
- **Fig. 17** (pp.34-35) — (a) satellite/aerial photo of the Mars-emulation test area with 5 labelled zoom regions (A-E); (b) full-area height-mesh map; (c) full-area planar-deviation map; (d) 5 paired 3-D rendered zoom-ins (height mesh | planar-deviation mesh) for regions A-E.
- **Key equations directly used in the analysis:** Eq. (1)-(4) (2-D/3-D relative IRF definitions), Eq. (5)-(8) (belief factorisation and pose/map decoupling), Eq. (9)-(10) (surfel stochastic-process/height model — the direct evidence for 2.5D), Eq. (13)-(21) (PGM factorisation, message passing, VMP), Eq. (55)-(56) (planar-deviation inverse-gamma update), Eq. (70) (correlated height-prior covariance).

## Uninterpretable / Uncertain Sections

1. Fig. 16(b), (f), (j) (p.33) — the three greyscale outdoor photographs (front/side/rear viewpoints) are legible in overall layout (gravel heap, asphalt path, ArUco markers) but fine details such as individual marker IDs or exact surface micro-texture cannot be reliably verified at the rendered resolution.
2. Fig. 17(a) (p.34) — the satellite/aerial photo's five labelled zoom regions (A-E) and general terrain layout are legible, but very fine details explicitly claimed in the text (e.g., "even small rocks" being visible in the map belief) could not be independently cross-verified pixel-for-pixel against the satellite image at the rendered resolution.
3. Numeric axis-tick values in Fig. 9 (p.22) are deliberately omitted by the authors ("we do not show the axis ticks, as we are only concerned with the relative difference," per caption) — this is a stated design choice by the authors, not a rendering failure, but it means no absolute numeric values can be read from that figure.

Aside from the above (which do not affect the correctness of the structural/technical claims drawn), no page, figure, table, or equation was unreadable.

## Summary Assessment

STM mapping is a **2.5-D, uniform-resolution, non-learned, Bayesian dense terrain-surface mapping technique** built on a continuous triangular mesh, whose principal demonstrated contributions are (1) modelling statistical continuity between neighbouring map elements at linear computational cost via a hybrid VMP+LBP message-passing inference scheme, validated against MCMC and shown more accurate than a standard elevation-map baseline by MSE and log-likelihood on both simulated and practical stereo/LiDAR data (DIRECT EVIDENCE, Sections 5-6), and (2) a landmark-relative submapping scheme that empirically decouples dense-map inference from robot-pose/SLAM uncertainty (DIRECT EVIDENCE, Section 3). It explicitly does **not** address adaptive/variable resolution, semantic information, terrain traversability classification, or any form of static/dynamic object detection or tracking — all of these are either absent or named as unimplemented future work by the authors themselves (DIRECT EVIDENCE, Section 7). Its practical validation of the core landmark-relative-IRF mechanism also relied on artificial fiducial markers or externally-supplied GPS poses rather than a live, general-environment SLAM landmark pipeline, leaving the "robust landmark identifiability" assumption unvalidated for unstructured environments (DERIVED, Sections 6.4-6.5). For the SIH problem, this paper is best read as a candidate reference for the "2.5D map representation with explicit uncertainty and continuity" and "pose-uncertainty decoupling via submapping" sub-problems, not as a solution to terrain analysis, object detection, or adaptive resolution (INFERENCE).
