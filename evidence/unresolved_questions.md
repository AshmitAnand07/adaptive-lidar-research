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
