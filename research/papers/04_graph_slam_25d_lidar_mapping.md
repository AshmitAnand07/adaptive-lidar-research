# Graph SLAM-Based 2.5D LIDAR Mapping Module for Autonomous Vehicles — Deep Analysis

**Source file:** `papers/Graph_SLAM-Based_25D_LIDAR_Mapping_Module_for_Auto.pdf` (byte-identical duplicate: `papers/remotesensing-13-05066.pdf`)
**Analyzed:** Phase 1 (supplied-paper analysis), single-paper deep read.

## 1. Problem being solved
The paper addresses map-generation error, not perception/detection. GNSS/INS-RTK (GIR) systems suffer relative-position drift in challenging environments (tunnels, dense trees, tall buildings, railway bridges) because satellite signals are deflected/obstructed. This produces "ghosting" — duplicated road landmarks in the XY plane — and virtual bumps/slope errors in the Z plane. The paper proposes a Graph SLAM (GS) framework (GS-XYZ) that corrects these relative- and global-position errors to generate an accurate 2.5D (intensity + elevation) map of the road surface in the Absolute Coordinate System (ACS). DIRECT EVIDENCE (p.1, Abstract; p.1, Introduction; Figure 1, p.2).

## 2. Sensors and input data
- Velodyne LIDAR 64, 360° mechanical spinning scanner, mounted on vehicle roof. DIRECT EVIDENCE (p.8, Section 4.1; Figure 7, p.9).
- GNSS/INS-RTK system, specifically POSLV 220, mounted in the trunk, providing position, acceleration, velocity and angular measurements, post-processed to produce vehicle trajectories. DIRECT EVIDENCE (p.8, Section 4.1).
- Vehicle dead-reckoning (DR) velocity/time integration is used as a secondary position estimator between GIR updates (Equation 1). DIRECT EVIDENCE (p.4).
- No camera is used as an input to the mapping pipeline itself; camera images appear only as illustrative ground-truth-scene photos in figures (e.g., Figure 2, Figure 8). DERIVED (p.3, p.9).

## 3. Input representation
Raw Velodyne point clouds are first cut ("Z-cut") at a fixed 0.3 m height threshold, producing a "LIDAR-frame" of fixed image size 512×512 pixels. DIRECT EVIDENCE (p.4, Section 2.1; p.8, Section 4.1). This cut frame is then converted into two per-frame images: (a) a grayscale intensity ("road-surface") image built from LIDAR reflectivity, and (b) a floating-point elevation-value matrix carrying the Z (height) value for the same pixels. DIRECT EVIDENCE (p.4, Figure 3a,b). Frames are accumulated via DR-based positioning (Equation 1) into a growing image until it forms a "node."

## 4. 2D / 2.5D / 3D representation
The paper is explicitly 2.5D, not full 3D, as directly observed in Figure 3: each node is represented as a 2D grayscale intensity image (XY grid) plus a separate co-registered elevation matrix carrying one height value per pixel (Figure 3a,b) — a 2D array with an attached height attribute, not an unrestricted 3D voxel/point volume. DIRECT EVIDENCE (p.4, Figure 3; p.8, Section 4.1, "direct save of the altitudinal information in a floating matrix"). No voxels, no multi-return per-column height distributions, and no full 3D mesh are used anywhere in the described pipeline. INFERENCE, but strongly grounded in Figure 3/4/6 imagery which show only flat image tiles and single-valued elevation renderings (e.g., the 3D-looking colored plot in Figure 3b is a 2.5D height-as-color surface rendering of the single-valued elevation matrix, not a 3D volumetric structure).

## 5. Spatial/map representation
The map is represented as a graph of "nodes," where each node is a rectangular image tile (intensity image + elevation matrix pair) anchored in the ACS by its top-left corner XY coordinate and an average Z value. DIRECT EVIDENCE (p.4, Section 2.1; Figure 3a). Nodes are connected by a pose-graph of sequential, anchoring (GPS), and loop-closure (image) edges (Figure 5a; Equations 2–4). The final map is produced by optimizing node positions (translation offsets in XY, Equation 6; Z-offsets, Equation 8) and re-assembling the node images into ACS.

## 6. Resolution strategy
Resolution is FIXED, not variable, at every level described:
- Z-cut threshold for building the road-surface frame: fixed 0.3 m. DIRECT EVIDENCE (p.4, Section 2.1).
- Node accumulation stops once node area (W×H) exceeds a fixed 1,000,000-pixel (1 M-pixel) threshold. DIRECT EVIDENCE (p.4, Section 2.1; p.8, Section 4.1).
- Pixel resolution: 0.125 m/pixel in the intensity image; 0.01 m/pixel (per floating value) in the elevation image. DIRECT EVIDENCE (p.8, Section 4.1).
- Single incoming LIDAR-frame size: fixed 512×512 pixels. DIRECT EVIDENCE (p.8, Section 4.1).
No distance-dependent, semantic-dependent, or uncertainty-dependent variation in any of these parameters is described or shown anywhere in the text or figures.

## 7. Whether resolution is adaptive and how
Not adaptive. This is confirmed directly: every resolution-determining parameter (the 0.3 m Z-cut, 1 M-pixel node-size threshold, 0.125 m intensity pixel size, 0.01 m elevation pixel size, 512×512 frame size) is stated as a single fixed constant used uniformly across the entire 34 km course, both in open-sky and tunnel segments. DIRECT EVIDENCE (p.4, p.8). There is no mechanism in the cost function (Equations 2–8), the node strategy (Section 2.1), or the experimental setup (Section 4.1) that changes resolution based on distance from the vehicle, object type, terrain, or estimated uncertainty. DERIVED. Regarding the ADAPTIVE SENSING vs ADAPTIVE COMPUTATIONAL/MAP RESOLUTION distinction: this paper does NEITHER. The Velodyne 64 performs a fixed, non-configurable 360° mechanical scan (no adaptive sensing), and the map/node representation uses fixed pixel and threshold sizes throughout (no adaptive computational/map resolution). DIRECT EVIDENCE / DERIVED.

## 8. Spatial data structure
A pose-graph of fixed-size raster-image nodes. Each node is a dense 2D array (intensity image) with a parallel dense 2D array of floats (elevation), not a tree, octree, quadtree, or hash grid. DIRECT EVIDENCE (Figure 3, Figure 4a, Figure 5a). Nodes are linked by edges (sequential, anchoring/GPS, loop-closure/image) forming the graph structure optimized by Equations 5–8. DIRECT EVIDENCE (p.5–8).

## 9. Height/elevation representation
Per-pixel single Z (height) value stored in a floating-point "elevation image" matrix, at 0.01 m resolution, aligned pixel-for-pixel with the intensity image. DIRECT EVIDENCE (p.4, Section 2.1; p.8, Section 4.1; Figure 3b). Node-level Z position (for the graph) is the average pixel value of the node's elevation image. DIRECT EVIDENCE (p.4, Section 2.1). This is a single-valued 2.5D elevation representation — no height distributions, multi-layer surfaces, or overhang/multi-return handling are described. DERIVED.

## 10. Semantic information
None. The intensity image encodes only LIDAR reflectivity (grayscale value), and the elevation image encodes only height. DIRECT EVIDENCE (p.4). The 0.3 m Z-cut is stated to be "designated to encode curbs, road edges, painted landmarks and lower parts of poles, barriers, trees, traffic lights, etc." (p.4) but this is a geometric height filter, not a semantic classifier — no object class labels, no segmentation, and no per-pixel semantic category are produced anywhere in the pipeline. DERIVED.

## 11. Terrain analysis
Not established from the paper. There is no drivable/non-drivable classification, slope classification, or traversability analysis performed. The paper only generates elevation/intensity maps and notes (as motivation/related applications, not as something this paper itself performs) that 2.5D elevation maps "can be used to enable... pitch and roll angle calculations" (p.3, citing external references [3,14]) and to "estimate pitch and roll angles" from Z data in general (p.1, Introduction). The paper itself does not compute pitch/roll or terrain traversability as an output/result. DIRECT EVIDENCE that this capability is only cited as a downstream application, not demonstrated (p.3).

## 12. Static-object perception
Not perception in the detection/classification sense. Static structures (curbs, road edges, poles, barriers, trees, traffic lights) are implicitly retained only insofar as their lower parts (below 0.3 m) fall inside the road-surface frame used for matching; there is no explicit static-object detection, bounding box, or classification output. DIRECT EVIDENCE for the Z-cut mechanism (p.4); DERIVED that this does not constitute object perception since no object-level output is produced.

## 13. Dynamic-object perception
The framework explicitly removes, rather than detects or perceives, dynamic objects: "This cutting threshold ... prevents the moving road users from being presented in the map" (p.4, Section 2.1). Figure 2b additionally shows how stopped cars at a traffic signal can still corrupt matching by masking real stationary features, which the paper identifies as a source of error rather than something it solves with object-level dynamic detection. DIRECT EVIDENCE (p.3, Figure 2b; p.4). There is no dynamic-object detection, classification, or removal algorithm beyond the fixed-height geometric cut. DERIVED.

## 14. Temporal processing
Frames are accumulated over time into nodes using dead-reckoning (DR) integration of vehicle velocity (Equation 1), synchronized with GIR measurements via timestamps (LIDAR frame every 100 ms, GIR measurement every 10 ms). DIRECT EVIDENCE (p.4, Equation 1; p.8, Section 4.1). Beyond this accumulation/synchronization, there is no temporal filtering, no motion model for tracked entities, and no multi-frame temporal fusion beyond node image assembly. DERIVED.

## 15. Tracking
Not reported. No object tracking (static or dynamic) is performed; the paper tracks/optimizes only node poses (map segments) in the Graph SLAM sense, not individual objects.

## 16. Uncertainty handling
Uncertainty is handled only in the Graph SLAM edge-covariance sense, used to weight the pose-graph optimization:
- Σ: standard deviation of vehicle velocity, used as the covariance for sequential (DR) edges (Equation 2). DIRECT EVIDENCE (p.5–6).
- Γ: covariance error of the GIR position, used for anchoring (GPS) edges (Equation 3). DIRECT EVIDENCE (p.6).
- Ω: covariance/correlation matrix derived from the phase-correlation (PhC) matching score, used for image (loop-closure) edges (Equation 4); explicitly stated that PhC "provides a correlation matrix that can be significantly employed to estimate the covariance error Ω" (p.7). DIRECT EVIDENCE.
- For the Z-plane graph (GS-Z), the paper states the covariance of the elevation edge Z^img "can be set to a constant scalar for the entire altitudinal edges in the map" (p.11), i.e., elevation-edge uncertainty is NOT data-derived per edge but fixed. DIRECT EVIDENCE.
This is pose/edge-confidence uncertainty for SLAM optimization, not per-cell occupancy, semantic, or object-detection uncertainty. DERIVED.

## 17. Localization / SLAM dependency
Total dependency. The entire framework is a Graph SLAM method; it fundamentally requires (a) a GIR (GNSS/INS-RTK) system for absolute anchoring edges and initial trajectory, (b) dead reckoning for smooth intra-node positioning, and (c) phase correlation for loop-closure edge estimation. DIRECT EVIDENCE (p.4–7, Equations 1–4). The stated purpose of the whole paper is to compensate for GIR localization errors in the map, meaning the method exists specifically to fix a SLAM/localization problem rather than to perform independent perception. DIRECT EVIDENCE (p.1, Abstract).

## 18. Learning/neural-network components
None. The pipeline uses classical algorithms only: dead reckoning integration, Graph SLAM optimization (H-matrix linear system, Equation 6), and phase correlation via FFT (FFTW library) for image matching. DIRECT EVIDENCE (p.7–9). No neural network, learned feature extractor, or learned classifier is used anywhere.

## 19. Computational requirements
Processing unit: Intel Core i7-6700 CPU @ 3.40 GHz, 64 GB RAM, Windows 10 64-bit, implemented in VS-2010 C++ with OpenCV 2.3.1 and Eigen libraries; FFTW library integrated for PhC/FFT computation. DIRECT EVIDENCE (p.8, Section 4.1).

## 20. Runtime/FPS/latency if reported
- A LIDAR-frame is generated every 100 ms; GIR measurements arrive every 10 ms (these are sensor output rates, not algorithm processing times). DIRECT EVIDENCE (p.8).
- The processing time to estimate the relative position between two nodes using PhC is "around 20 ms." DIRECT EVIDENCE (p.9, Section 4.1, citing [29]).
- No end-to-end pipeline frame rate, total map-generation time for the 34 km course, or full-system FPS is reported. DERIVED (absence noted after reviewing all text).

## 21. Memory/map-size results if reported
No numeric memory or map file size (MB/GB) is reported. The paper only makes a qualitative claim that 2.5D maps "reduce the storing size ... compared to 3D point cloud maps" (p.3) without quantification. Node/point-cloud counts are reported as a proxy for data volume: first scan = 283 nodes from 16,041 point clouds; second scan = 285 nodes from 15,473 point clouds. DIRECT EVIDENCE (p.10, Section 5.1). No byte-size, compression ratio, or RAM footprint figures are given.

## 22. Dataset and experimental setup
Custom, non-public data collected by the authors' own robotics platform (Toyota Alphard-type vehicle, Figure 7) equipped with Velodyne 64 and POSLV 220 GIR. DIRECT EVIDENCE (p.9, Figure 7; p.14, Data Availability Statement — data is proprietary to Kanazawa University, available only on request). Test course: Yamate Tunnel, Tokyo — an 18.2 km highway tunnel ending at Ohashii Junction, 30 m underground depth, two tubes each with two lanes; course extended by starting from Yono Junction, giving a 34 km total course including a substantial open-sky segment before tunnel entry. DIRECT EVIDENCE (p.9, Section 4.2, Figure 8a). The single-direction tube was driven twice at different velocities to create two independent scans for loop-closure/comparison testing. DIRECT EVIDENCE (p.9).

## 23. Evaluation metrics
- XY common-area coordinate differences ("edge diff") between matched nodes of the two scans, compared for PhC-based estimate vs. raw GIR-based estimate (Figure 9a), in meters. DIRECT EVIDENCE (p.10).
- GS-XY top-left-corner Y- and X-offsets per node ID across the course (Figure 9b,c). DIRECT EVIDENCE (p.10).
- Qualitative visual comparison of merged node images (presence/absence of ghosting) for GIR vs. GS-XY (Figures 8f,g; 10; 11). DIRECT EVIDENCE.
- GIR standard deviation in Z across node IDs (Figure 12a) and elevation error (m) between common areas: GIR (red) vs. GS-Z (green) profiles (Figure 12b). DIRECT EVIDENCE.
- Altitudinal position/trajectory comparison at specific loop-closure edges (nodes 225/227, 276/277) and elevation difference across the entire trajectory point-by-point (Figure 13c–e). DIRECT EVIDENCE.
No standard SLAM benchmark metrics (e.g., ATE/RPE against independent ground truth other than the GIR system itself) are used; GIR is itself treated as the accuracy reference in open-sky regions and as the thing being corrected inside the tunnel. INFERENCE.

## 24. Baselines and ablations
The main comparison baseline throughout is the raw GIR (GNSS/INS-RTK) system output, used both as a presumed "ground truth" in open-sky conditions (where GS-offsets are shown to match GIR closely, Figure 9b,c) and as the flawed system being corrected inside the tunnel (large deviations up to ~4 m in XY, Figure 9a; up to 1.2 m elevation error in Z, Figures 12b, 13a). DIRECT EVIDENCE (p.10–13). A secondary implicit ablation is "PhC alone" vs. "GS-XY," shown failing in wide, feature-sparse roads (Figure 6a) and in tunnels/bridges with repetitive patterns (Figure 11c), then corrected by the full GS-XY optimization (Figure 6b, 11e). DIRECT EVIDENCE. No comparison against other published SLAM methods (e.g., LOAM/LeGO-LOAM/ISAM, all cited in the Introduction) is performed. DERIVED (absence noted).

## 25. Failure cases
- PhC alone gives inaccurate lateral (XY) matching in wide, feature-sparse roads because there are insufficient distinguishing landmarks. DIRECT EVIDENCE (p.7, Figure 6a).
- PhC alone gives wrong longitudinal matching in tunnels/bridges where the road pattern is nearly identical in the driving direction, and the paper shows a corresponding "spiking peak" in the open-sky XY-edge-difference plot (Figure 9a, roughly edges 40–120) and a dedicated wrong-match example (Figure 11c). DIRECT EVIDENCE (p.10–12).
- Stopped/queued vehicles at a traffic signal can be encoded as if they were stationary environmental features, corrupting matching on a repeat visit if the parked-vehicle pattern differs between visits. DIRECT EVIDENCE (p.3, Figure 2b) — noted as a known failure mode, not solved by the 0.3 m Z-cut since stopped cars can still exceed/interact with the cut region.
- GIR itself shows large XY deviations up to ~4 m and elevation errors up to ~1.2 m specifically inside the 30 m-deep tunnel due to satellite signal loss. DIRECT EVIDENCE (p.10, Figure 9a; p.13, Figure 12a,b, 13a).

## 26. Explicit limitations
The paper explicitly states PhC-specific limitations: it "may provide inaccurate lateral matching results in wide roads, where the shared landmarks are not sufficient" and gives "wrong correspondences in the longitudinal direction between nodes of critical environments, such as tunnels, where the road pattern is identical" (p.7, Section 3.3). These are presented as motivating the two-stage GS-XY→GS-Z design (which reuses GS-XY's corrected offsets to fix GS-Z's dependence on raw PhC), rather than as unresolved limitations of the full GS-XYZ framework. No other explicit limitations (e.g., scalability beyond 34 km, applicability to non-tunnel dynamic urban traffic, sensitivity to the fixed 0.3 m cut in non-flat terrain) are stated in the text. DERIVED (absence noted after full read).

## 27. Future work
Not reported. The paper has no dedicated "Future Work" section; Section 6 ("Conclusions") only summarizes the achieved results and states the framework "increases the scalability of the mapping module to represent the real world precisely." No forward-looking research directions are stated. (Section 7 "Patents" instead notes the work was patented in Japan in 2020, patent number 2020-090099 — an IP disclosure, not future-work content.) DIRECT EVIDENCE (p.14).

## 28. What the method does NOT solve
- Does not perform object detection, classification, or semantic segmentation of any kind (static or dynamic).
- Does not perform terrain traversability/drivability analysis (only cites pitch/roll estimation as a possible downstream use of elevation data, not something it computes).
- Does not track dynamic objects — it removes them via a fixed height cut rather than modeling or perceiving them.
- Does not use or evaluate any adaptive/variable spatial resolution — every resolution parameter is fixed.
- Does not report full end-to-end runtime/FPS or memory footprint for the whole mapping pipeline.
- Does not compare against other published SLAM/mapping baselines, only against the raw GIR system and raw PhC.
- Does not address non-tunnel dynamic urban environments with significant moving traffic beyond the single stopped-car example (Figure 2b), and does not resolve that specific failure case.
DERIVED, compiled from the absence of any evidence for these items across the full document.

## 29. Relevance to the fixed SIH problem
Terrain analysis: Low direct relevance — the paper produces elevation data that could theoretically feed a terrain-analysis stage (pitch/roll/slope), but performs no traversability classification itself; this is only a cited potential downstream use (p.3), not a capability demonstrated in this paper. INFERENCE.
Static/dynamic object detection: Low/negative relevance — the paper actively discards dynamic objects via a fixed 0.3 m geometric height cut rather than detecting, classifying, or tracking them, and performs no static-object recognition; it treats dynamic road users purely as map-corruption noise to be removed. DIRECT EVIDENCE-derived observation (p.4).
Adaptive variable-resolution 2.5D spatial representation: The paper's spatial representation IS 2.5D (per-pixel single-valued elevation + co-registered intensity image, Section 4), which is architecturally relevant as one concrete existing example of a 2.5D map representation. However, resolution in this paper is uniformly FIXED (0.125 m intensity pixels, 0.01 m elevation values, 1 M-pixel node threshold, 0.3 m Z-cut) across the entire map regardless of distance, semantics, or uncertainty — it contains no adaptive/variable-resolution mechanism of any kind, and therefore does not address the SIH problem's core "adaptive variable-resolution" requirement. It is relevant mainly as a precedent for how a fixed-resolution 2.5D intensity+elevation map can be built and corrected via Graph SLAM in a driving context, and as an illustration that a highly effective 2.5D mapping/localization pipeline can exist with zero object-level semantics and zero adaptivity. DIRECT EVIDENCE for the fixed-resolution claim; INFERENCE for the relevance characterization.

## Figures/Tables/Equations Directly Consulted
- Figure 1 (p.2): (a) Ghosting — duplicated road landmarks from GIR relative-position error, with a "matching matrix" inset and multiple false matching-pattern lines; (b) same segment mapped without ghosting, with clean single matching peak.
- Figure 2 (p.3): (a) Point-cloud view of a featureless wide road showing sparse/absent vertical (Z-direction) features useful for matching; (b) point-cloud view at a traffic signal where stopped/queued cars (colored clusters) occupy the space where static features should be encoded.
- Figure 3 (p.4): (a) Bird's-eye intensity image of an accumulated node showing the road surface, curbs, a road barrier, and the top-left-corner identification tactic with min/max vehicle-position markers; (b) a colored 3D-style rendering of the elevation matrix (height encoded as color) for the same node, showing raised structures (bridge/overpass) along the route.
- Figure 4 (p.5): Four-panel diagram of node-level GS: (a) two nodes (A, B) with intensity+elevation image pairs at a loop closure; (b) 3D schematic showing XY deviation and wrong altitudinal error P1(z)−P2(z) between GIR-placed nodes; (c) after GS-XY, nodes aligned in XY with corrected altitudinal-error calculation; (d) after GS-Z, nodes brought to a common Z-level.
- Figure 5 (p.6): (a) Node-graph schematic showing sequential (E^Seq), anchoring (E^GPS), and loop-closure (E^Loop-closure) edges around a chain of nodes N0…Nt+2; (b) two node intensity images (N3, Nt) with a highlighted common area, and a merged/overlaid image showing accurate matching without ghosting after PhC.
- Figure 6 (p.8): (a) Two node images incorrectly merged by PhC alone (visible double/offset road pattern); (b) same two nodes correctly merged using GS-XY-guided projection; (c) block diagram of the GS-Z framework showing projection of common areas between nodes using GS-XY results, including one "wrong estimation by PhC" callout.
- Figure 7 (p.9): Photograph of the instrumented vehicle (minivan) with labeled GNSS/INS-RTK antennas and roof-mounted Velodyne LIDAR.
- Figure 8 (p.9): (a) Map/route graphic of the two-times-scanned course from Yono Junction through Yamate Tunnel with tunnel entrance/end marked; (b) top-left corner scatter plot of course nodes with loop-closure lines; (c–g) three loop-closure events shown as rows (camera image, first-scan patch, second-scan patch, GIR-merged result with visible ghosting circled, PhC-merged result without ghosting).
- Figure 9 (p.10): (a) Line plot of XY common-area coordinate differences (x and y, PhC vs GIR) across edge ID 0–440, flat near zero in open sky with visible "spiking peaks" around edge 40–120, then large divergence (up to a few meters) inside the tunnel (edge ~300–440); (b) GS Y-offset per node ID, near-zero in open sky, large swings inside tunnel; (c) GS X-offset per node ID, similar pattern.
- Figure 10 (p.11): 2×5 grid of tunnel-segment node images — top row showing visibly doubled/ghosted road markings from GIR combination, bottom row showing the same segments cleanly combined by GS-XY.
- Figure 11 (p.12): Five-panel comparison — (a,b) first/second scan node images (labeled "Sparse"/"Sparse" then "Dense"/"Dense"), (c) an incorrectly phase-correlation-matched overlay circled in red showing lateral/longitudinal mismatch, (d) accurate GIR-based combination, (e) accurate GS-XY-based combination.
- Figure 12 (p.12): (a) Line plot of GIR standard deviation in Z vs. node ID for both scans, near-zero in open sky, rising sharply (up to ~3+ m) around node 200–290 (tunnel region); (b) elevation-error line plot (edge ID) comparing GIR (red, large excursion up to ~1.2 m inside tunnel) vs GS-Z (green, stays near zero throughout).
- Figure 13 (p.13): (a,b) paired node images at two specific loop-closure edges (IDs 340 and 433) with reference/projected trajectories and common-area boxes overlaid; (c,d) altitudinal-position line plots per trajectory point comparing GS-Z vs GIR for each node pair; (e) elevation-difference plot (GS-Z green vs GIR red) across the entire trajectory (point-cloud ID 0–16,200), flat/small for GS-Z, with a large red excursion in the tunnel region.
- Equation (1) (p.4): Dead-reckoning position update X_t^DR = X_{t-1}^DR + ve_t·Δt.
- Equation (2) (p.5): Sequential edge cost term E^DR based on squared Mahalanobis-style distance between consecutive node top-left corners.
- Equation (3) (p.6): Anchoring edge cost term E^GPS tying a node position to its GIR-observed position, weighted by covariance Γ.
- Equation (4) (p.6): Image (loop-closure) edge cost term E^Img based on PhC-estimated relative position X^img, weighted by Ω.
- Equation (5) (p.7): Overall GS-XY cost function — sum of E^DR, E^Img, E^GPS terms, minimized over node positions X.
- Equation (6) (p.7): Linearized solve ΔX = −H⁻¹b for the GS-XY optimization.
- Equation (7) (p.7): Loop-closure elevation edge Z^img_{Ni,Nj} as the average pixel-wise altitudinal difference over a common U×V area between two nodes' elevation images.
- Equation (8) (p.8): Overall GS-Z cost function, structurally analogous to Equation 5 but in the Z domain.

## Uninterpretable / Uncertain Sections
None. All figures, tables, and equations in the 16-page document were legible at the rendered resolution and could be interpreted directly. One caveat: numeric values read off line plots (e.g., the exact magnitude of the "spiking peaks" in Figure 9a, or precise elevation-error values in Figure 12b/13e other than the explicitly stated 1.2 m maximum) are visual estimates from graph curves rather than tabulated exact values, since the paper does not provide a results table with precise numbers for every plotted point — this analysis avoided citing any such un-stated precise figures.

## Summary Assessment
This paper is a Graph SLAM mapping-correction method, not a perception or adaptive-resolution method: it corrects GNSS/INS-RTK-induced ghosting and elevation drift in a fixed-resolution 2.5D (intensity image + single-valued elevation matrix) road-surface map by decomposing optimization into an XY phase-correlation-driven stage (GS-XY) followed by a Z-plane stage (GS-Z) (DIRECT EVIDENCE, p.1, p.4–8). Every resolution parameter — the 0.3 m Z-cut, 1 M-pixel node threshold, 0.125 m intensity and 0.01 m elevation pixel sizes — is fixed and uniform across the entire 34 km test course, and the paper implements neither adaptive sensing nor adaptive computational/map resolution (DIRECT EVIDENCE, p.4, p.8). Dynamic road users are explicitly excluded from the map via the fixed height cut rather than detected, classified, or tracked, and no semantic labeling, terrain-traversability computation, or neural-network component exists anywhere in the pipeline (DIRECT EVIDENCE, p.4; DERIVED for absence of NN/semantics). Demonstrated results are strong for the stated SLAM-correction problem: up to ~4 m of GIR-induced XY drift and ~1.2 m of Z drift inside the 30 m-deep, 18.2 km Yamate Tunnel are shown visually and quantitatively corrected by GS-XYZ (DIRECT EVIDENCE, Figures 9, 12, 13), though no end-to-end runtime, memory footprint, or comparison to other published SLAM baselines is reported (DERIVED, absence noted). Relevance to the SIH problem is limited to serving as one concrete precedent for a fixed-resolution 2.5D map representation and as an illustration that dynamic-object exclusion (not detection) is one simple prior strategy — it does not address adaptive resolution, semantic/terrain analysis, or object perception at all (INFERENCE).
