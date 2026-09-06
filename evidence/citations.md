# Citations — Paper Inventory

Status: Bibliographic inventory only. No content analysis performed yet.

Metadata source: `pdfinfo` (Poppler) for page counts/embedded metadata, cross-
checked against the rendered first page of each PDF where metadata was
missing or incomplete. All fields below are **Web verified / Direct evidence**
(read directly off the document) unless marked otherwise.

| # | Filename | Title | Authors | Year | Venue | Pages | Analysis file |
|---|---|---|---|---|---|---|---|
| 1 | `1910.03644.pdf` | Stochastic Triangular Mesh Mapping: A Terrain Mapping Technique for Autonomous Mobile Robots | Clint D. Lombard, Corné E. van Daalen | 2019/2020 (v2) | arXiv preprint (arXiv:1910.03644v2 [cs.RO]); header states "submitted to Robotics and Autonomous Systems" — journal publication status not verified | 39 | `research/papers/01_stochastic_triangular_mesh_mapping.md` |
| 2 | `2412.00291v1.pdf` | Real-Time Metric-Semantic Mapping for Autonomous Navigation in Outdoor Environments | Jianhao Jiao, Ruoyu Geng, Yuanhang Li, Ren Xin, Bowen Yang, Jin Wu, Lujia Wang, Ming Liu, Rui Fan, Dimitrios Kanoulas | 2024 | arXiv preprint (arXiv:2412.00291v1 [cs.RO]) | 12 | `research/papers/02_realtime_metric_semantic_mapping.md` |
| 3 | `3636534.3690708.pdf` | αLiDAR: An Adaptive High-Resolution Panoramic LiDAR System | Jiahe Cui, Yuze He, Jianwei Niu, Zhenchao Ouyang, Guoliang Xing | 2024 | ACM MobiCom '24 (International Conference on Mobile Computing and Networking), Washington D.C., USA | 17 | `research/papers/03_alidar_adaptive_panoramic.md` |
| 4 | `Graph_SLAM-Based_25D_LIDAR_Mapping_Module_for_Auto.pdf` | Graph SLAM-Based 2.5D LIDAR Mapping Module for Autonomous Vehicles | Mohammad Aldibaja, Naoki Suganuma | 2021 | Remote Sensing (MDPI), 13, 5066 | 16 | `research/papers/04_graph_slam_25d_lidar_mapping.md` |
| 5 | `PID3780167.pdf` | Detection and Tracking of Moving Objects Using 2.5D Motion Grids | Alireza Asvadi, Paulo Peixoto, Urbano Nunes | 2015 (from PDF CreationDate; not printed on page 1) | Not stated on the rendered title page — venue unverified, do not assume | 6 | `research/papers/05_detection_tracking_25d_motion_grids.md` |
| 6 | `islandora_164656.pdf` | 2.5D Evidential Grids for Dynamic Object Detection | Hind Laghmara, Thomas Josso-Laurain, Christophe Cudel, Jean-Philippe Lauffenburger | 2019 | 22nd International Conference on Information Fusion (FUSION 2019), Ottawa, Canada. DOI: 10.23919/FUSION43075.2019.9011417 (HAL id hal-04131742) | 9 | `research/papers/06_evidential_grids_dynamic_object_detection.md` |
| 7 | `machines-10-01200-v2.pdf` | 3D Environment Mapping with a Variable Resolution NDT Method | Yang Feng, Zhiyuan Gao, Jinghan Zhang, Hang Shi, Yangmin Xie | 2022 | Machines (MDPI), 10, 1200 | 20 | `research/papers/07_variable_resolution_ndt_mapping.md` |
| 8 | `remotesensing-13-05066.pdf` | **Duplicate of #4** (byte-identical, confirmed via SHA-256) | Mohammad Aldibaja, Naoki Suganuma | 2021 | Remote Sensing (MDPI), 13, 5066 | 16 | Not separately analyzed — see #4 |
| 9 | `sensors-26-04765.pdf` | Lightweight 2.5D SLAM with Dynamic Map Refinement and Height-Aware Encoding for Resource-Constrained Indoor Robots | Guitao Yu, Yuping Zhang, Zhiao Qi, Kui Yang, Yang He, Dongtai Liang | 2026 | Sensors (MDPI), 26, 4765 | 25 | `research/papers/08_lightweight_25d_slam_height_aware.md` |

**Phase 1 status (2026-09-05): 8/8 unique papers fully analyzed** (per-paper deep-read files above, each covering the full document — text, figures, tables, equations — with evidence-tagged findings).

## Flags

- **Duplicate**: `Graph_SLAM-Based_25D_LIDAR_Mapping_Module_for_Auto.pdf` (#4) and
  `remotesensing-13-05066.pdf` (#8) are the same paper — confirmed byte-identical
  via SHA-256 checksum (not just matching title/authors/page count). Treated as
  one source; only #4 was analyzed in Phase 1.
- **Unverified venue**: `PID3780167.pdf` (#5) — the rendered title page does
  not print a venue/conference name. Do not infer or fabricate one; if the
  venue is needed later, verify externally (e.g. via the paper's own
  reference list or a search) before citing it as fact.
- **Unverified publication status**: `1910.03644.pdf` (#1) is an arXiv
  preprint whose header says it was "submitted to Robotics and Autonomous
  Systems" — whether it was actually accepted/published there has not been
  checked.

## External Literature (Phase 2)

Phase 2 (external literature research, completed 2026-09-06) analyzed **~104
external papers** across five research-family groups, adversarially
stress-testing six Phase-1-derived hypotheses (see
`../evidence/claims.md` for verdicts). Full bibliographic and technical
detail lives in:

- `../external_literature/00_inventory.md` — structured comparison table
  (one row per paper, same dimensions as the supplied-paper analyses)
- `../external_literature/group_a_adaptive_resolution_hierarchical.md`
- `../external_literature/group_b_attention_uncertainty_realtime.md`
- `../external_literature/group_c_25d_semantic_terrain.md`
- `../external_literature/group_d_dynamic_temporal_perception.md`
- `../external_literature/group_e_sparse_representations.md`

Not duplicated here to avoid maintaining two copies of ~104 citations; this
file remains the authoritative bibliography for the 9 **supplied** papers.

## External Literature (Resolution-Boundary Consistency Investigation, 2026-09-06)

A focused follow-up investigation searched LiDAR/robotics-mapping literature,
cross-domain literature (computer graphics terrain LOD, FEM/adaptive mesh
refinement, multigrid, image processing), and semantic/object-perception-
adjacent literature for evidence on resolution-transition/boundary artifacts.
~30 new sources were consulted (full citations, access levels, and per-source
evidence tags in the table below). Not duplicated here in full per the same
rationale as Phase 2; the authoritative source list is:

- `../research/resolution_boundary_consistency.md` §2a (LiDAR/robotics-native
  evidence — 12 sources), §2b (cross-domain evidence — 9 sources), §2c
  (semantic/object-perception-adjacent evidence — 9 sources)

Key new citations (full detail in the file above): Schoppmann et al., IROS
2021, arXiv:2111.06271 (JPL planetary-rotorcraft elevation mapping); Funk et
al., ICRA 2021/RA-L, arXiv:2010.07929; Schleich & Behnke, ICRA 2021,
arXiv:2103.14607; "Reduced Complexity Multi-Scale Path-Planning on
Probabilistic Maps," arXiv:1602.04800; Nguyen et al. 2026, arXiv:2603.22667;
Yang et al., "Interpolation-Aware Padding," ICCV 2021, arXiv:2108.06925;
Reina et al., Frontiers in Neuroscience 2020, PMC7020775; "Group Evidence
Matters," arXiv:2509.10779; SWITi, arXiv:2607.18990; geometry clipmaps
(Losasso & Hoppe 2004), ROAM (Duchaineau et al. 1997), geomipmapping (de Boer
2000); FEM/AMR 2:1-balance and hanging-node lineage (Sundar, Sampath, Biros;
deal.II documentation); Briggs/Henson/McCormick, "A Multigrid Tutorial."

## Resolution-Boundary Consistency Feasibility Experiment (2026-09-06)

Not an external citation — a reproducibility record for this project's own
synthetic experiment (see `../research/resolution_boundary_consistency.md`
§9 for the full design and results). Source of record:

- `../experiments/resolution_boundary_experiment.py` — full experiment code
  (pure Python stdlib, no external dependencies), documented sensor-model
  and world-generation simplifications inline
- `../experiments/results/resolution_boundary_experiment_results.json` —
  complete raw numeric output for all 7 swept configurations, every metric

Any claim drawn from this experiment elsewhere in this project should be
tagged **DIRECT EVIDENCE — this project's own synthetic experiment**, kept
explicitly distinct from DIRECT EVIDENCE sourced from published external
papers, since it uses no real LiDAR data and no external dataset.

## Candidate Solution Analysis (2026-09-06)

Targeted new research for `../research/05_candidate_solution_analysis.md`,
distinct from the broad Phase 2 sweep. Full citations and evidence levels
in that file, §1.4 and §1.10. Key new sources: AdaOcc full text
(arXiv:2408.13454, via `arxiv.org/html/2408.13454`); WACV 2025 point
selection (arXiv:2508.01980); foreground-modulation paper (arXiv:2604.05780);
S3PM (MDPI Sensors 2026, PMC12845740); Dynamic Lambda-Field
(arXiv:2103.04795); MR3D-Net (arXiv:2408.06137); Patchwork++
(arXiv:2207.11919); ground-segmentation survey (arXiv:2312.16839); RobMOT
(arXiv:2405.11536); Spb3DTracker (arXiv:2408.05940); EG-PointPillar
(ScienceDirect, search-verified). One sub-search (driver-count ablations,
persistent-vs-transient trade-offs) was interrupted by a platform rate
limit and did not complete — reported as incomplete in
`05_candidate_solution_analysis.md` §6, not backfilled with a guess.

## Architecture-Selection Evidence Checkpoint (2026-09-06)

Not an external citation — a reproducibility record for this project's own
driver-count-ablation experiment (see
`../research/05_candidate_solution_analysis.md` §11 for design and results).

- `../experiments/driver_ablation_experiment.py` — full experiment code
  (pure Python stdlib, no dependencies)
- `../experiments/results/driver_ablation_results.json` — complete raw
  numeric output

Part 3 (classical vs. learned static-object perception) drew only on
sources already cited under "Candidate Solution Analysis (2026-09-06)"
above — no new external sources for this checkpoint.

## Semantic-Resolution Temporal-Stability Checkpoint (2026-09-06)

Not an external citation — a reproducibility record for this project's own
semantic-noise-stability experiment (see
`../research/05_candidate_solution_analysis.md` §12). No new external
sources; the noise-rate calibration reuses LVCA-Net's accuracy figure
already cited under "Candidate Solution Analysis (2026-09-06)" above.

- `../experiments/semantic_noise_stability_experiment.py` — full experiment
  code (imports `driver_ablation_experiment.py` directly rather than
  duplicating the world/sensor model)
- `../experiments/results/semantic_noise_stability_results.json` —
  complete raw numeric output, all policies and both noise levels

## Format for future entries

As further external literature is added in later phases, append rows to
`../external_literature/00_inventory.md` in the same table format, and tag
each with the evidence level (Direct / Web verified / Derived / Inference)
used to obtain the metadata.
