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

## Format for future entries

As external literature is added (Phase 2 of `01_research_plan.md`), append
rows here in the same table format, and tag each with the evidence level
(Direct / Web verified) used to obtain the metadata.
