# Unresolved Questions

Status: Seeded from the disconfirming-evidence checklist in `CLAUDE.md`.
These are open research questions, not conclusions — none has been
investigated yet.

## Purpose

Track questions that must be answered with evidence (not assumed) before any
architecture is selected. Each question should eventually be resolved by a
finding in `claims.md` (with its evidence level) or remain explicitly open.

## Entry format

```
### <question>

- Status: Open | Partially answered | Resolved
- Relevant claims: [[claims.md#...]] (once populated)
- Notes:
```

## Questions carried over from CLAUDE.md (Research Principles §2)

### Is distance-only adaptive resolution sufficient?
- Status: Partially answered — evidence points toward "often necessary but not sufficient alone."
- Relevant claims: [[claims#h1--distance-based-adaptive-resolution-in-lidar-mapping-is-largely-unexplored]]
- Notes: Phase 2 found distance-based adaptive resolution is well-explored and works (Adaptive-LIO, VoxelMap, RoadRunner M&M), disproving "unexplored." But sufficiency is separately in question: the embedded voxel-efficiency paper (arXiv:2105.10316) found models restricted to near-field already "fail to detect distant small objects" — meaning some reported distance-restriction "savings" are partly a byproduct of already-missed detections, not efficient handling. PointPillars' own stated limitation is exactly "distant/small-object information loss" under its fixed-resolution pillar grid. Cylinder3D shows a coordinate-system choice can implicitly produce a distance-correlated resolution gradient "for free" without an explicit adaptive rule — a genuine alternative to hand-engineered distance-based adaptivity worth weighing. Still open: whether a *deliberate* distance-based policy (not fixed, not implicit) avoids the small/distant-object failure mode better than semantic- or uncertainty-driven alternatives.

### Is a 2.5D representation sufficient, or does it lose information 3D would keep?
- Status: Partially answered
- Relevant claims: [[claims#25d-and-full-3d-choices-split-roughly-evenly-across-the-8-papers-independent-of-resolution-adaptivity]]
- Notes: The metric-semantic mapping paper (#2) explicitly chose full 3D over 2.5D elevation maps and argues for it in its own related-work discussion — DIRECT EVIDENCE that at least one paper considers 2.5D insufficient for its use case (large-scale outdoor semantic navigation). Still open whether this generalizes to the SIH problem's specific requirements.

### Does coarse distant resolution lose important objects (small, thin, or distant)?
- Status: Open

### Do adaptive grids actually reduce end-to-end computation, or only nominal memory?
- Status: Partially answered — yes, conditionally, not automatically.
- Relevant claims: [[claims#the-only-measured-map-size-reduction-numbers-in-the-supplied-set-come-from-one-paper-and-even-there-accuracy-effects-are-mixed]], [[claims#h5--adaptive-map-resolution-can-provide-meaningful-computationalmemory-benefits]]
- Notes: Phase 2 found real, hardware-measured compute reductions from adaptive/sparse structures (MrHash: 13x speedup; SPADE: 1.3-10.9x on custom silicon, 4.1-28.8x vs. GPU; SPS-Conv: >50% GFLOPs cut with no accuracy loss). But the benefit is NOT automatic: FALO shows sparse convolution losing to a re-engineered dense alternative on real edge GPU/NPU hardware; SPVNAS shows 7.6x theoretical FLOPs reduction yielding only 2.7x measured speedup; DFPS's own text admits its overhead cancels the benefit for small point clouds; a 2026 survey (arXiv:2604.16482) explicitly found no rigorous overhead accounting across the spatial-memory-representation literature it reviewed. Net: the answer depends on matching the adaptivity mechanism to the target hardware/software stack and operating at sufficient scale — there is no general guarantee.

### Do hierarchical/sparse structures introduce excessive overhead that offsets their savings?
- Status: Open

### Is semantic-aware or uncertainty-aware adaptation better than purely geometric/distance-based adaptation?
- Status: Partially answered
- Relevant claims: [[claims#only-one-supplied-paper-performs-genuine-semantic-terrain-traversability-analysis-and-it-shows-a-concrete-failure-mode-when-semantics-are-removed]]
- Notes: DIRECT EVIDENCE from paper #2 that removing semantic information causes a concrete misclassification failure (grass marked traversable). This is about terrain classification accuracy, not about resolution adaptation specifically — no supplied paper ties semantic or uncertainty information to a resolution-adaptivity decision, so the resolution-policy half of this question remains open.

### Is there a more appropriate representation than 2.5D/variable-resolution grids for this problem?
- Status: Open

## Questions carried over from CLAUDE.md (Important Technical Questions)

### Distance-based vs. semantic/uncertainty/risk/terrain-aware resolution — which is better justified?
- Status: Open

### How much information is lost at resolution transitions (grid-cell boundaries between fine and coarse regions)?
- Status: Open

### How are small and distant objects handled under variable resolution?
- Status: Partially answered — poorly, by default, unless specifically compensated for.
- Relevant claims: [[claims#h1--distance-based-adaptive-resolution-in-lidar-mapping-is-largely-unexplored]]
- Notes: Multiple independent Phase 2 findings converge here: PointPillars' own stated limitation is losing "spatial information... especially for distant objects or points on the edges of objects" under its fixed pillar resolution; the embedded voxel-efficiency paper (arXiv:2105.10316) found full-range models already "fail to detect distant small objects," meaning naive range-restriction "savings" partly reflect objects already being missed rather than efficiently handled; SPVNAS was built specifically because coarse voxelization disproportionately hurts small/thin dynamic-relevant classes (bicyclists, motorcyclists) and had to add a parallel full-resolution point branch to compensate. Consistent pattern: distant/small/thin objects are a real, repeatedly-documented failure mode of coarse resolution, not a hypothetical one — any resolution policy for the SIH problem needs an explicit mitigation, not just an assumption that "coarser far away" is safe.

### How are thin structures (poles, rails, thin walls) handled?
- Status: Open

### How are dynamic objects handled differently from static terrain/objects?
- Status: Open

### How are terrain boundaries (drivable/non-drivable transitions) represented and detected?
- Status: Open

### How do sparse LiDAR returns (long range, occlusion) affect the chosen representation?
- Status: Open

### How does localization error propagate into map/resolution errors?
- Status: Open

### How temporally stable is the representation across frames (flicker, resolution churn)?
- Status: Open

### Does the approach actually reduce memory, or only nominal cell count?
- Status: Open

### What is the actual end-to-end latency (not just per-module latency)?
- Status: Open

### What is CPU/GPU efficiency in practice vs. in theory?
- Status: Open

### What is the effective spatial resolution vs. the nominal (advertised) resolution?
- Status: Partially answered.
- Notes: Cylinder3D (CVPR 2021) demonstrates that a coordinate-system choice (cylindrical vs. Cartesian voxel binning) implicitly creates a distance-correlated effective-resolution gradient — equal angular/radial steps span a larger physical footprint at range — without any explicit "if far then coarsen" rule. This means nominal cell size alone can be a misleading proxy for effective resolution; the coordinate frame itself matters. Relevant precedent to weigh before hand-engineering an explicit adaptive-resolution rule: part of the desired effect may be obtainable "for free" via representation/coordinate-system choice.

## Meta-question

### Does fewer map cells actually mean faster computation for this class of method?
- Status: Partially answered — CLAUDE.md's caution is corroborated by Phase 2, not resolved into a simple yes/no.
- Relevant claims: [[claims#h5--adaptive-map-resolution-can-provide-meaningful-computationalmemory-benefits]]
- Notes: SPVNAS provides a direct quantified counter-example within a single paper: 7.6x compute (MACs) reduction produced only 2.7x measured wall-clock speedup — theoretical compute reduction does not translate 1:1 into speed. FALO shows the gap can go further: fewer active sites can be *slower* in wall-clock terms on hardware not designed for irregular sparse access. This is now a well-evidenced caution, not an assumption — any Phase 8 feasibility experiment on a candidate architecture should measure wall-clock time on the actual target hardware, not infer it from cell/FLOP counts.

## Synthesis Checkpoint (2026-09-06) — Five Most Important Open Questions

Carried forward from the paper-vs-paper synthesis (`../research/03_paper_vs_sih_matrix.md`,
`../research/04_paper_vs_paper_matrix.md`). These are judged the highest-priority
unresolved items for deciding how to proceed into Phase 3/4, not a
restatement of every open item above.

### Can a semantic-class-weighted resolution objective (Larsson et al. 2022's β/γ formalism) be adapted from a full 3D octree to a 2.5D grid/quadtree for ground-vehicle terrain data?
- Status: Open — insufficient evidence; no paper found attempting this.
- Relevant claims: [[claims#the-three-phase-2-flagged-gaps-re-classified-after-paper-vs-paper-analysis]]
- Notes: This is the specific mechanical question behind Gap 1's "likely genuine gap" classification. The objective function is not intrinsically 3D-specific per its own description, which is why the gap reads as plausible-but-unattempted rather than fundamentally blocked — but this is inference from reading the paper's formalism, not a demonstrated result.

### Does AdaOcc's object-centric ROI mechanism key on moving/dynamic objects specifically, or on any detected foreground object regardless of motion state?
- Status: **Resolved (2026-09-06).** Confirmed: any detected foreground object, regardless of motion state — not dynamic-object-specific.
- Relevant claims: [[claims#adaocc-roi-mechanism-resolved--object-aware-not-motion-aware]]
- Notes: Full text obtained via `arxiv.org/html/2408.13454` (HTML rendering succeeded where two prior PDF-fetch attempts had failed). The paper never uses "dynamic," "moving," "static," or "motion" anywhere in its text; its DETR-style 900-box regression covers all 10 nuScenes classes, including static ones (barrier, traffic cone, construction vehicle); prioritization is explicitly proximity + foreground/background, not motion state. This **upgrades Gap 2 back toward "genuine gap"** rather than "potentially already addressed" — the most promising near-miss is now confirmed not to solve the dynamic-object tie. See `research/05_candidate_solution_analysis.md` §1.4 for the fuller follow-up search this prompted.

### When two adaptivity drivers (e.g., a distance-based rule and a semantic-based rule) disagree about whether a region should be fine or coarse, is there any principled precedent for arbitrating the conflict?
- Status: Open — insufficient evidence; no paper was found either solving or explicitly raising this as a named problem.
- Relevant claims: [[claims#driver-conflict-arbitration-has-no-identified-precedent]]
- Notes: This is a stronger absence than Gaps 1-3, which at least have papers gesturing toward the combined idea (MAP-ADAPT, Agile3D). No comparable gesture was found here at all.

### Does resolution-boundary consistency (artifacts at fine/coarse transitions) matter in practice for terrain/object perception, or has it simply never been written about?
- Status: **Substantially answered** — a small synthetic feasibility experiment was designed and run (`../research/resolution_boundary_consistency.md` §9); the effect is real and measurable but modest in magnitude, not "never written about" and not negligible either.
- Relevant claims: [[claims#resolution-boundary-effects-are-real-and-measurable-but-modest-in-magnitude-across-every-metric-tested]], [[claims#revision-resolution-boundary-consistency-is-downgraded-from-a-candidate-central-research-contribution-to-a-secondary-priority-design-constraint]]
- Notes: A 2.5D elevation-mapping paper (JPL, arXiv:2111.06271) had already named the artifact in its own primary text (literature phase). The follow-up experiment then measured it directly on synthetic data: elevation error differences ≤~2cm, occupancy/semantic mismatch 0.5-4.6% in the boundary band, zero missed static-object detections in 105 tests, and a temporal-tracking instability at boundary-crossing that was in every tested configuration smaller than or comparable to the jitter already caused by coarse-resolution tracking alone. **This question is now resolved to the extent a small synthetic experiment can resolve it** — remaining uncertainty is whether real (non-synthetic) LiDAR data and a real target architecture would show the same modest magnitudes, which would require a later, architecture-specific validation, not further literature search or a bigger version of this same synthetic test.

### Does a naive resolution-boundary "consistency mechanism" (e.g. adding an intermediate resolution tier) reliably fix the problem, or can it introduce new costs?
- Status: **Answered — it does not reliably help, and can measurably hurt.**
- Relevant claims: [[claims#the-tested-naive-consistency-mechanism-gives-mixed-not-uniformly-positive-results--and-measurably-worsens-semantic-accuracy-in-most-configurations]]
- Notes: The one lightweight mechanism tested (a graduated intermediate tier, a simplified proxy for the FEM "2:1 balance" idea) reduced boundary-band occupancy mismatch in 5 of 7 configurations but *increased* semantic-label mismatch in 6 of 7 configurations, with no reliable effect on temporal instability. This corroborates the literature finding that effective fixes elsewhere (interpolation-aware padding, dual-scale hysteresis) are more sophisticated than simple tier subdivision — a naive fix is not a safe default.

## Candidate Solution Analysis (2026-09-06)

### Does uncertainty-driven adaptive resolution add measurable benefit beyond what distance-driven adaptation already captures for a ground vehicle?
- Status: Open — insufficient evidence; a dedicated search was attempted but interrupted by a platform rate limit before completing.
- Relevant claims: [[claims#research-transparency-note-a-targeted-sub-search-was-interrupted-by-a-platform-rate-limit-and-is-reported-as-incomplete-not-answered]]
- Notes: MrHash's strong quantified result (~4x memory, up to 13x speedup) is from a different domain (general 3D SDF reconstruction); for a ground vehicle, distance and measurement uncertainty are plausibly correlated via sensor geometry, so B may substantially duplicate A's benefit. No ablation isolating this was found in Phase 2, and this phase's attempt to search further was cut short — carried forward as open, not resolved either way. See `research/05_candidate_solution_analysis.md` §6.

### Is there any published ablation isolating the marginal benefit of adding a second (or third) resolution driver to an existing single-driver system?
- Status: Open — search interrupted, incomplete.
- Relevant claims: [[claims#research-transparency-note-a-targeted-sub-search-was-interrupted-by-a-platform-rate-limit-and-is-reported-as-incomplete-not-answered]]
- Notes: This phase attempted to re-check MAP-ADAPT, Agile3D, and Larsson et al. specifically for a driver-isolating ablation; the search agent located a relevant PDF and was interrupted before reading it. No ablation of this kind was found in the original Phase 2 review either, but that is a weaker basis than a completed dedicated search would provide.

## Architecture-Selection Evidence Checkpoint (2026-09-06)

### Does uncertainty-driven adaptive resolution add measurable benefit beyond what distance-driven adaptation already captures for a ground vehicle?
- Status: **Substantially answered for the specific mechanism tested — no, and it is now eliminated.** (Supersedes, but does not fully replace, the "Open — insufficient evidence" entry below, which still applies to untested alternative uncertainty-response mechanisms.)
- Relevant claims: [[claims#adding-a-semantic-driver-on-top-of-distance-is-justified-adding-an-uncertainty-refinement-driver-on-top-of-that-is-not]]
- Notes: A controlled experiment found spatial resolution refinement in response to elevated local variance caught a genuine anomaly (0.88 allocation-correct) but made the elevation estimate there *worse* (fewer points per fine cell average out noise less) and had a lower targeting-efficiency rate than the semantic driver. Eliminated from the core resolution policy. Still open: whether a non-refinement uncertainty-response (e.g. flagging for re-observation) would fare better — not tested.

### Is semantic-driven adaptive resolution mechanically feasible in a persistent 2.5D ground-vehicle map, without a complex hierarchical structure?
- Status: **Answered — yes, at basic/synthetic scale, now demonstrated rather than only inferred.**
- Relevant claims: [[claims#semantic-driven-25d-adaptive-resolution-is-mechanically-feasible-without-a-hierarchical-data-structure--now-demonstrated-not-only-inferred]]
- Notes: A flat, non-tree grid with a simple binary semantic-override rule worked mechanically, with bounded, modest memory growth. Two items remain untested and open: temporal stability under a real (noisy, frame-to-frame) classifier rather than static ground-truth labels, and joint operation with a separate dynamic-object subsystem.

### Is a lightweight classical pipeline competitive with a learned LiDAR detector for static-object perception specifically?
- Status: **Answered as "insufficient evidence for a confident general claim" — this is itself the answer, not a placeholder.**
- Relevant claims: [[claims#classical-vs-learned-static-object-detection-evidence-is-insufficient-for-a-confident-general-claim]]
- Notes: No direct controlled comparison (same dataset, both accuracy and latency) was found for classical clustering vs. a deep 3D detector. Classical clustering is self-limited by its own authors to sparse/simple scenes; classical geometric features added to a deep detector improve accuracy rather than being redundant with it (EG-PointPillar, +3.88% mAP). Conclusion drawn: a hybrid is the evidence-backed default over a pure-classical choice, moderate confidence — this is distinct from *tracking*, where classical evidence was strong (RobMOT/Spb3DTracker).

## Semantic-Resolution Temporal-Stability Checkpoint (2026-09-06)

### Does semantic-driven adaptive resolution remain useful when the semantic input is realistically noisy and changes frame-to-frame?
- Status: **Answered — not without stabilization, but viable with a simple one.**
- Relevant claims: [[claims#raw-unsmoothed-noisy-semantic-driven-resolution-is-not-viable--it-causes-substantial-memory-bloat-and-per-frame-churn]], [[claims#a-simple-symmetric-k3-persistence-counter-hysteresis-resolves-the-instability-at-negligible-cost]]
- Notes: Unsmoothed noisy semantic predictions (90% per-frame accuracy, IID noise) caused 24% memory bloat and 17.7%-per-transition tier churn. A simple K=3 consecutive-frame hysteresis counter fixed this (0.23% churn, within 0.5% of ideal memory) at +9% latency. Candidate 3 remains viable but must now specify this hysteresis component as required, not optional.

### Does hysteresis-based stabilization work as well under spatially/temporally correlated semantic-classifier errors as it did under independent (IID) per-frame noise?
- Status: Open — untested; flagged as the most important remaining uncertainty before Candidate 3's stabilization mechanism can be trusted with a real classifier.
- Relevant claims: [[claims#a-simple-symmetric-k3-persistence-counter-hysteresis-resolves-the-instability-at-negligible-cost]]
- Notes: This checkpoint deliberately tested the harder IID-flip case as a stress test. A real classifier's errors are plausibly correlated (confidently wrong for several consecutive frames on a genuinely ambiguous input) — under that error pattern, a persistence counter could lock onto an *incorrect* state for longer than under IID noise, rather than filtering out a brief, uncorrelated glitch. Resolving this would require either real semantic-segmentation model output (not a statistical proxy) or a documented, evidence-grounded correlated-noise model — neither was done in this checkpoint.

### Does the literature directly compare persistent (accumulated) vs. transient (per-frame) map representations for combining terrain/static perception with dynamic-object perception?
- Status: Open — search interrupted, incomplete; existing evidence is indirect only.
- Relevant claims: [[claims#research-transparency-note-a-targeted-sub-search-was-interrupted-by-a-platform-rate-limit-and-is-reported-as-incomplete-not-answered]]
- Notes: Existing evidence (Gap Map's "Persistent adaptive maps" section, Axis 9) establishes that persistent adaptive maps are a minority pattern (fewer than 15 of ~104 external papers) and that every mature dynamic-object system reviewed uses a fixed-resolution, largely transient-per-window representation — but no paper was found in either search pass directly arguing for one architecture over the other with measured trade-off numbers (e.g. map staleness/ghosting cost vs. persistence benefit). This gap directly motivated this document's design choice (§10) to keep dynamic-object perception as a separate subsystem in every candidate.

### Does a hierarchical spatial data structure (octree/quadtree) inherently avoid resolution-boundary consistency problems through its own representation, or must an explicit mechanism be added?
- Status: Partially answered.
- Relevant claims: [[claims#the-naive-default-boundary-handling-behavior-of-a-hierarchical-spatial-structure-does-not-automatically-avoid-the-problem--and-most-robotics-papers-using-such-structures-never-checked]]
- Notes: In every case checked in full text, the naive/default behavior did NOT automatically avoid the problem: octree-based learned 3D perception needed an explicit "interpolation-aware padding" fix (ICCV 2021) because standard zero-padding corrupted boundary features; a robotics multi-scale path-planning paper with neighbor-finding as a core topic (arXiv:1602.04800) was directly verified to never address value-aggregation or consistency across a resolution boundary at all, despite its hierarchical structure. Caution confirmed: the mere presence of a hierarchy/adaptive structure in a paper does not mean boundary consistency was considered — several robotics octree papers use words like "consistency" or "balance" to mean something unrelated (obstacle-edge alignment, query efficiency), not geometric neighbor-consistency (see `../research/resolution_boundary_consistency.md` §3 for the confirmed terminology false-leads).

### Given FALO/SPVNAS's disconfirming evidence that theoretical compute reduction does not reliably predict measured speedup, what target hardware should this project assume before any computational claim can be evaluated?
- Status: Open — this is a project-scoping question, not a literature gap; the literature's answer is "it depends on the hardware," which is itself the finding.
- Relevant claims: [[claims#h5--adaptive-map-resolution-can-provide-meaningful-computationalmemory-benefits]]
- Notes: Directly blocks any meaningful "is adaptive resolution worth it computationally" claim for this project's own candidate architecture until a target deployment platform (embedded GPU? CPU-only? custom accelerator?) is specified — the same mechanism has been shown to help substantially on one platform (SPADE on custom silicon) and hurt on another (FALO on Jetson Orin/Hexagon NPU).
