"""
Semantic-resolution temporal-stability test: does distance+semantic
adaptive resolution remain useful when the semantic input is realistically
noisy and changes frame-to-frame, or does it need a stabilization
mechanism -- and if so, how simple can that mechanism be?

Extends experiments/driver_ablation_experiment.py (same world, terrain,
critical patch, pole, sensor model) rather than building a new framework.
Isolates ONE variable: whether the semantic PREDICTION for the same static
scene is perfect/stable or noisy/frame-to-frame-changing. The scene itself
and the underlying point cloud are held fixed across frames so that any
churn measured is attributable to semantic-label noise alone, not to new
sensor data or robot motion (temporal effects from robot motion/tier
boundaries were already covered in resolution_boundary_experiment.py).

Noise model (documented, not a trained network): each coarse-tier
candidate cell's predicted semantic label is correct with probability
P_CORRECT, independently redrawn every frame. P_CORRECT is calibrated to
a real reported LiDAR semantic-segmentation accuracy figure already in
this project's own evidence base (LVCA-Net: 91.79% overall accuracy on
SemanticKITTI, research/05_candidate_solution_analysis.md Sec 1.10) --
DERIVED calibration, not an invented number. An independent (IID) per-frame
flip is the *harder*, more adversarial case than a realistic classifier's
actual (spatially/temporally correlated) error pattern would be, so this
is a deliberate stress test, not an optimistic one.

Policies compared:
  A        distance-only (never uses semantics)
  B        distance + PERFECT/stable semantic labels (ground truth every frame)
  C_raw    distance + noisy semantic labels, used directly, no smoothing
  C_hystK  distance + noisy semantic labels, passed through a simple
           symmetric hysteresis/persistence counter requiring K consecutive
           same-valued predictions before a cell's tier switches

Run: `python3 semantic_noise_stability_experiment.py`
"""

import math
import random
import statistics
import time
import json
import os

from driver_ablation_experiment import (
    World, background_scan, pole_points, cell_stats, H_FINE, H_COARSE, R_B, POLE,
)

WORLD = World()
P_CORRECT_REALISTIC = 0.90  # DERIVED: calibrated to LVCA-Net's 91.79% reported overall accuracy
P_CORRECT_OPTIMISTIC = 0.95
N_FRAMES = 30
HYSTERESIS_K_VALUES = (3, 5)


def coarse_cell_id(x, y):
    return (math.floor(x / H_COARSE), math.floor(y / H_COARSE))


def candidate_coarse_cells(points):
    """All coarse-tier cells that actually receive sensor points beyond
    R_B -- the set a real classifier would be asked to label each frame."""
    cells = set()
    for p in points:
        if math.hypot(p["x"], p["y"]) >= R_B:
            cells.add(coarse_cell_id(p["x"], p["y"]))
    return cells


def true_critical_coarse_cells(candidates):
    out = set()
    for cid in candidates:
        cx, cy = (cid[0] + 0.5) * H_COARSE, (cid[1] + 0.5) * H_COARSE
        if WORLD.is_critical_semantic(cx, cy):
            out.add(cid)
    return out


def pole_coarse_cell():
    return coarse_cell_id(POLE["x"], POLE["y"])


def build_grid_for_frame(points, fine_coarse_cells):
    """fine_coarse_cells: set of coarse-cell-ids that should be treated as
    fine this frame (distance-fine points are always fine regardless)."""
    grid = {}
    for p in points:
        r = math.hypot(p["x"], p["y"])
        if r < R_B:
            fine = True
        else:
            fine = coarse_cell_id(p["x"], p["y"]) in fine_coarse_cells
        h = H_FINE if fine else H_COARSE
        cid = ("F" if fine else "C", math.floor(p["x"] / h), math.floor(p["y"] / h))
        cell = grid.setdefault(cid, {"ground_z": [], "obst_n": 0})
        if p["obstacle"]:
            cell["obst_n"] += 1
        else:
            cell["ground_z"].append(p["z"])
    return grid


def run_policy_over_frames(points, candidates, true_critical, rng, mode, p_correct=None, k=None):
    """mode: 'A' (never semantic), 'B' (perfect), 'C_raw' (noisy, no smoothing),
    'C_hyst' (noisy + hysteresis, requires k)."""
    pole_cid = pole_coarse_cell()
    streak_val = {c: False for c in candidates}
    streak_len = {c: 0 for c in candidates}
    hyst_state = {c: False for c in candidates}

    prev_tier = None  # cid -> True/False fine, from previous frame, for churn counting
    fine_counts = []
    churn_events = 0
    critical_correct_frames = 0
    pole_correct_frames = 0
    false_positive_frame_fractions = []
    first_critical_fine_frame = None
    first_pole_fine_frame = None
    build_times_ms = []

    for t in range(N_FRAMES):
        if mode == "A":
            fine_set = set()
        elif mode == "B":
            fine_set = set(true_critical)
        else:
            predicted = {}
            for c in candidates:
                correct = rng.random() < p_correct
                predicted[c] = (c in true_critical) if correct else (c not in true_critical)
            if mode == "C_raw":
                fine_set = set(c for c, v in predicted.items() if v)
            elif mode == "C_hyst":
                for c in candidates:
                    v = predicted[c]
                    if streak_val[c] == v:
                        streak_len[c] += 1
                    else:
                        streak_val[c] = v
                        streak_len[c] = 1
                    if streak_len[c] >= k:
                        hyst_state[c] = v
                fine_set = set(c for c, v in hyst_state.items() if v)
            else:
                raise ValueError(mode)

        t0 = time.perf_counter()
        grid = build_grid_for_frame(points, fine_set)
        build_times_ms.append((time.perf_counter() - t0) * 1000)

        cur_tier = {c: (c in fine_set) for c in candidates}
        fine_counts.append(len(grid))
        if prev_tier is not None:
            churn_events += sum(1 for c in candidates if cur_tier[c] != prev_tier[c])
        prev_tier = cur_tier

        if true_critical and all(cur_tier[c] for c in true_critical):
            critical_correct_frames += 1
            if first_critical_fine_frame is None:
                first_critical_fine_frame = t
        if cur_tier.get(pole_cid, False):
            pole_correct_frames += 1
            if first_pole_fine_frame is None:
                first_pole_fine_frame = t

        normal_cells = candidates - true_critical
        fp = sum(1 for c in normal_cells if cur_tier[c]) / len(normal_cells) if normal_cells else 0.0
        false_positive_frame_fractions.append(fp)

    n_transitions = N_FRAMES - 1
    n_candidate_cells = len(candidates)
    return {
        "mean_fine_cell_count": round(statistics.fmean(fine_counts), 2),
        "std_fine_cell_count": round(statistics.pstdev(fine_counts), 2),
        "min_max_fine_cell_count": [min(fine_counts), max(fine_counts)],
        "total_tier_flips": churn_events,
        "flips_per_transition_per_candidate_cell": round(churn_events / (n_transitions * n_candidate_cells), 4) if n_transitions and n_candidate_cells else None,
        "critical_region_correct_frame_fraction": round(critical_correct_frames / N_FRAMES, 4),
        "pole_region_correct_frame_fraction": round(pole_correct_frames / N_FRAMES, 4),
        "mean_false_positive_fraction_of_normal_cells": round(statistics.fmean(false_positive_frame_fractions), 4),
        "first_frame_critical_region_fine": first_critical_fine_frame,
        "first_frame_pole_fine": first_pole_fine_frame,
        "mean_build_ms": round(statistics.fmean(build_times_ms), 3),
    }


def run():
    rng_world = random.Random(11)
    bg = background_scan(rng_world)
    pole_pts = pole_points(POLE, rng_world)
    points = bg + pole_pts

    candidates = candidate_coarse_cells(points)
    true_critical = true_critical_coarse_cells(candidates)

    results = {}
    rng = random.Random(99)
    results["A_distance_only"] = run_policy_over_frames(points, candidates, true_critical, rng, "A")
    results["B_perfect_semantic"] = run_policy_over_frames(points, candidates, true_critical, rng, "B")

    for label, p in (("realistic_p0.90", P_CORRECT_REALISTIC), ("optimistic_p0.95", P_CORRECT_OPTIMISTIC)):
        results[f"C_raw_{label}"] = run_policy_over_frames(points, candidates, true_critical, random.Random(42), "C_raw", p_correct=p)
        for k in HYSTERESIS_K_VALUES:
            results[f"C_hyst_k{k}_{label}"] = run_policy_over_frames(points, candidates, true_critical, random.Random(42), "C_hyst", p_correct=p, k=k)

    out = {
        "n_frames": N_FRAMES,
        "n_candidate_coarse_cells": len(candidates),
        "n_true_critical_coarse_cells": len(true_critical),
        "results": results,
    }

    out_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "semantic_noise_stability_results.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
