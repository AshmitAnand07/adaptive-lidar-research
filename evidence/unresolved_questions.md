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
- Status: Open
- Relevant claims: [[claims#no-supplied-paper-implements-distance-based-adaptive-map-resolution]]
- Notes: Phase 1 found zero supplied papers implementing distance-based adaptive resolution at all (fixed-resolution, curvature-driven, or sensor-side-ROI-driven only). Cannot be answered from the supplied set — must come from Phase 2 external literature.

### Is a 2.5D representation sufficient, or does it lose information 3D would keep?
- Status: Partially answered
- Relevant claims: [[claims#25d-and-full-3d-choices-split-roughly-evenly-across-the-8-papers-independent-of-resolution-adaptivity]]
- Notes: The metric-semantic mapping paper (#2) explicitly chose full 3D over 2.5D elevation maps and argues for it in its own related-work discussion — DIRECT EVIDENCE that at least one paper considers 2.5D insufficient for its use case (large-scale outdoor semantic navigation). Still open whether this generalizes to the SIH problem's specific requirements.

### Does coarse distant resolution lose important objects (small, thin, or distant)?
- Status: Open

### Do adaptive grids actually reduce end-to-end computation, or only nominal memory?
- Status: Partially answered
- Relevant claims: [[claims#the-only-measured-map-size-reduction-numbers-in-the-supplied-set-come-from-one-paper-and-even-there-accuracy-effects-are-mixed]]
- Notes: The one supplied paper with adaptive map resolution (#7) reports memory/map-size reduction only — no end-to-end computation, runtime, or FPS figures anywhere in that paper. So even the strongest available evidence in this set cannot answer the computation question, only the memory question.

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
- Status: Open

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
- Status: Open

## Meta-question

### Does fewer map cells actually mean faster computation for this class of method?
- Status: Open — explicitly flagged in CLAUDE.md as an assumption not to make.
- Relevant claims: [[claims#the-only-measured-map-size-reduction-numbers-in-the-supplied-set-come-from-one-paper-and-even-there-accuracy-effects-are-mixed]]
- Notes: No supplied paper measures computation/latency as a function of map size or resolution, so this remains entirely open from Phase 1 — must be addressed via Phase 2 literature or a Phase 8 feasibility experiment.
