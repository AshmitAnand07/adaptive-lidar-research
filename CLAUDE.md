# CLAUDE.md

## Project

This repository is for research on the SIH problem:

**Adaptive Variable Resolution 2.5D LiDAR Mapping for Dynamic Environment
Perception**

The goal is to determine the strongest technically justified solution for:

1. Terrain analysis — drivable vs non-drivable terrain.
2. Object detection — static and dynamic objects such as walls, poles,
   pedestrians and vehicles.
3. Adaptive spatial representation — a variable-resolution 2.5D map/elevation
   representation that preserves useful height and semantic information while
   reducing computational and memory cost.

The SIH problem mentions fine resolution near the robot and progressively
coarser resolution farther away, but this is an example/requirement to
investigate, not an architecture that has already been chosen.

---

## Current Phase: Research

We are currently in the **research phase**, not the final implementation phase.

The architecture must emerge from the research.

Do NOT prematurely choose:

- neural network architecture
- point/voxel/BEV/range representation
- grid structure
- resolution policy
- spatial data structure
- dynamic-object method
- terrain-analysis method
- temporal model
- uncertainty model
- dataset
- hardware configuration

Small prototypes or experiments are allowed when they answer a specific
research question. Do not begin full production implementation until the
research phase is complete.

---

## Research Principles

### 1. Evidence over assumptions

Do not assume that the initial idea is correct.

Compare multiple technically different approaches and determine which is best
from the evidence.

### 2. Search for disconfirming evidence

Actively look for research showing that proposed approaches may fail.

In particular, investigate whether:

- distance-only adaptive resolution is sufficient
- 2.5D is sufficient
- coarse distant resolution loses important objects
- adaptive grids actually reduce end-to-end computation
- hierarchical/sparse structures introduce excessive overhead
- semantic-aware or uncertainty-aware adaptation is better
- another representation is more appropriate

### 3. Distinguish evidence levels

Clearly distinguish:

- **Direct evidence** — explicitly demonstrated by a source.
- **Derived** — logically derived from reported results.
- **Inference** — interpretation based on evidence.
- **Hypothesis** — not yet demonstrated.
- **Web verified** — verified using current external sources.

Never present an inference or hypothesis as an established fact.

### 4. No fabricated information

Do not invent:

- benchmark results
- FPS/latency
- memory usage
- datasets
- citations
- architecture details
- experimental results
- limitations

If something cannot be verified, say so.

---

## Literature Research

Deeply analyze all papers in `papers/`, not only their abstracts.

For each important paper, determine:

- problem
- sensors
- input representation
- 2D/2.5D/3D representation
- spatial data structure
- resolution strategy
- elevation/height representation
- semantic information
- terrain analysis
- dynamic-object handling
- temporal processing
- uncertainty
- localization/SLAM requirements
- neural network/method
- computational requirements
- datasets
- evaluation metrics
- limitations and failure cases
- relevance to the SIH problem

Search external literature, especially recent work from 2023–2026, covering:

- adaptive/variable-resolution LiDAR mapping
- multi-resolution representations
- 2.5D/elevation mapping
- semantic LiDAR perception
- dynamic-object perception
- terrain/traversability mapping
- sparse LiDAR perception
- hierarchical spatial structures
- adaptive voxelization
- uncertainty-aware mapping
- real-time LiDAR systems

Always distinguish **adaptive sensing** from **adaptive computational/map
representation**. They are not the same problem.

---

## Architecture Selection

Do not select an architecture simply because it is popular or easy to
implement.

Before selecting the final architecture:

1. Analyze the supplied papers.
2. Research relevant external literature.
3. Identify what existing methods already solve.
4. Identify genuine technical gaps.
5. Generate multiple competing solution approaches.
6. Compare their accuracy, memory, latency, robustness, complexity and
   implementation feasibility.
7. Perform a prior-art/novelty check.
8. Red-team the leading approach.
9. Run targeted feasibility experiments where necessary.
10. Only then recommend the final architecture.

The final recommendation must explain why it is preferable to the strongest
alternatives.

---

## Important Technical Questions

Pay particular attention to:

- distance-based vs semantic/uncertainty/risk/terrain-aware resolution
- information loss at resolution transitions
- small and distant objects
- thin structures
- dynamic objects
- terrain boundaries
- sparse LiDAR returns
- localization error
- temporal stability
- memory reduction
- actual end-to-end latency
- CPU/GPU efficiency
- effective vs nominal spatial resolution

Do not assume that fewer map cells automatically means faster computation.

---

## Research Artifacts

Maintain research work separately from implementation.

Recommended structure:

```text
papers/
external_literature/
research/
experiments/
datasets/
scripts/