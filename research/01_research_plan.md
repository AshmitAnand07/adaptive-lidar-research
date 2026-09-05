# 01 — Research Plan

Status: Proposed plan only. Nothing below has been executed yet. No
architecture, representation, or method is assumed or recommended by this
document.

## Scope

Research plan for: **Adaptive Variable Resolution 2.5D LiDAR Mapping for
Dynamic Environment Perception** (see `../CLAUDE.md`), covering terrain
analysis, object detection, and adaptive spatial representation. The
architecture must emerge from this process — it is not chosen in advance.

## Phases

### Phase 1 — Supplied Paper Analysis
Deeply analyze all 9 papers in `papers/` (see `../evidence/citations.md` for
inventory), not only abstracts. For each paper, extract: problem, sensors,
input representation, 2D/2.5D/3D representation, spatial data structure,
resolution strategy, elevation/height representation, semantic information,
terrain analysis, dynamic-object handling, temporal processing, uncertainty,
localization/SLAM requirements, method, computational requirements, datasets,
evaluation metrics, and limitations/failure cases.
- Output: one analysis note per paper, plus claims logged in `../evidence/claims.md`.
- Note the duplicate pair (#4/#8) is analyzed once.

### Phase 2 — External Literature Research
Search 2023–2026 literature (and older foundational work as needed) on:
adaptive/variable-resolution LiDAR mapping, multi-resolution representations,
2.5D/elevation mapping, semantic LiDAR perception, dynamic-object perception,
terrain/traversability mapping, sparse LiDAR perception, hierarchical spatial
structures, adaptive voxelization, uncertainty-aware mapping, real-time LiDAR
systems.
- Explicitly distinguish **adaptive sensing** from **adaptive computational/
  map representation** — they are different problems.
- Output: entries appended to `../evidence/citations.md`, claims logged in
  `../evidence/claims.md`, source PDFs/notes stored in `../external_literature/`.

### Phase 3 — Technical Taxonomy
Build a structured taxonomy across all reviewed sources (supplied + external)
along the dimensions used in Phase 1, so approaches can be compared on equal
terms rather than by name/popularity.
- Output: a comparison table (representation × resolution strategy ×
  dynamic-object method × terrain method × evidence level per cell).

### Phase 4 — Gap Analysis
Identify what existing methods already solve vs. genuine technical gaps
relevant to the SIH problem's three sub-problems (terrain analysis, object
detection, adaptive spatial representation).
- Actively search for disconfirming evidence per `../CLAUDE.md` §"Search for
  disconfirming evidence" — see seeded questions in
  `../evidence/unresolved_questions.md`.

### Phase 5 — Competing Solution Approaches
Generate multiple technically different candidate approaches (not limited to
distance-only adaptive grids). Compare on accuracy, memory, latency,
robustness, complexity, and implementation feasibility — using evidence
gathered so far, not assumption.
- Output: a candidates document with side-by-side tradeoffs; no candidate is
  designated "the" solution at this stage.

### Phase 6 — Novelty / Prior-Art Check
For the leading candidate(s) from Phase 5, check what has already been done
in the supplied papers and external literature to avoid reinventing or
misrepresenting prior work as novel.

### Phase 7 — Red-Team Analysis
Actively attack the leading approach(es): find failure modes, edge cases, and
conditions under which they underperform or fail outright (thin structures,
sparse returns, dynamic objects at resolution boundaries, localization error
propagation, etc. — see `../evidence/unresolved_questions.md`).

### Phase 8 — Feasibility Experiments
Where a specific technical question cannot be resolved from literature alone,
run small, targeted prototypes/experiments in `../experiments/` to answer
that one question. Not full implementation — scoped experiments only, each
tied to a specific open question.

### Phase 9 — Final Architecture Selection
Only after Phases 1–8: recommend a final architecture, explicitly justified
against the strongest alternatives identified in Phase 5, referencing the
evidence and gaps from Phases 1–8. Must state which claims are Direct,
Derived, Inference, Hypothesis, or Web verified.

## Explicit Non-Goals (this document)

- No neural network architecture, point/voxel/BEV/range representation, grid
  structure, resolution policy, spatial data structure, dynamic-object
  method, terrain-analysis method, temporal model, uncertainty model,
  dataset, or hardware configuration is chosen here.
- No implementation beyond scoped feasibility experiments (Phase 8).

## Artifact Map

| Directory/File | Purpose |
|---|---|
| `papers/` | Supplied source PDFs (existing) |
| `external_literature/` | External sources gathered in Phase 2 |
| `research/` | Plan and phase-level analysis notes |
| `experiments/` | Phase 8 feasibility prototypes only |
| `datasets/` | Any datasets referenced/used during experiments |
| `scripts/` | Supporting scripts (metadata extraction, analysis tooling) |
| `evidence/claims.md` | Claims ledger with evidence levels |
| `evidence/citations.md` | Bibliographic inventory |
| `evidence/unresolved_questions.md` | Open questions tracked to resolution |
