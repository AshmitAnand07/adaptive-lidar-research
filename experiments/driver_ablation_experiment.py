"""
Driver-count ablation: does each additional resolution driver (distance ->
distance+semantic -> distance+semantic+uncertainty) provide enough measured
benefit to justify its added complexity?

Scope: a small, targeted synthetic experiment (per
research/05_candidate_solution_analysis.md Part 1). NOT the SIH pipeline,
NOT an architecture choice, no learned arbitration -- every policy below is
a simple deterministic rule, as instructed.

Synthetic world (documented, closed-form ground truth):
  - Same terrain profile as experiments/resolution_boundary_experiment.py
    (flat ground, a curb step at x in [8,9], flat higher ground, a
    continuous slope for x in [14,20]) -- reused for continuity with this
    project's prior experiment rather than re-derived.
  - A "critical" semantic patch at x in [13,15], y in [-1,1] -- beyond the
    distance-only tier boundary (R_b=10m), so a distance-only policy
    coarsens it by default. A medium pole (radius 0.15m) sits inside it,
    at (14, 0) -- the object a semantic-aware policy should preserve that
    a distance-only policy should lose or degrade.
  - An independent "sensor-noise anomaly" patch at x in [17,19], y in
    [-4,-2] -- also beyond R_b, NOT the critical semantic class, where
    ground points receive elevated measurement noise (4x baseline sigma),
    simulating a real degraded-return region (e.g. a reflective/absorptive
    surface) unrelated to either distance or semantics. Only an
    uncertainty-aware policy should refine this region.

Three deterministic policies (no learned arbitration):
  A. Distance-only  -- fine within R_b, coarse beyond.
  B. Distance + semantic -- A, plus: force fine inside the critical
     semantic patch regardless of distance.
  C. Distance + semantic + uncertainty -- B, plus: force fine inside any
     coarse-sized candidate cell whose sampled-point height variance
     exceeds a fixed threshold (a deterministic proxy for "this region's
     measurements disagree with each other," not a learned signal).

Run: `python3 driver_ablation_experiment.py`
"""

import math
import random
import statistics
import time
import json
import os
from collections import Counter

# ---------------------------------------------------------------------------
# World
# ---------------------------------------------------------------------------

class World:
    def height(self, x, y):
        if x < 8.0:
            return 0.0
        if x < 9.0:
            t = x - 8.0
            return 0.3 * (t - math.sin(2 * math.pi * t) / (2 * math.pi))
        if x < 14.0:
            return 0.3
        if x < 20.0:
            return 0.3 + 0.2 * (x - 14.0) / 6.0
        return 0.5

    def is_critical_semantic(self, x, y):
        return 13.0 <= x <= 15.0 and -1.0 <= y <= 1.0

    def is_noise_anomaly(self, x, y):
        return 17.0 <= x <= 19.0 and -4.0 <= y <= -2.0


WORLD = World()
POLE = {"x": 14.0, "y": 0.0, "radius": 0.15, "height": 1.0}

# ---------------------------------------------------------------------------
# Sensor model (reused conventions from resolution_boundary_experiment.py)
# ---------------------------------------------------------------------------

AZ_MIN, AZ_MAX, AZ_STEP_DEG = -30.0, 30.0, 0.3
R_MIN, R_MAX, R_STEP = 3.0, 22.0, 0.25
BASE_NOISE = 0.02
ANOMALY_NOISE = 0.08  # 4x baseline, confined to the noise-anomaly patch
OCC_MIN_PTS = 2
H_FINE = 0.2
K = 4
H_COARSE = H_FINE * K
R_B = 10.0
VARIANCE_THRESHOLD = (BASE_NOISE * 2.5) ** 2  # candidate coarse cell flagged "uncertain" above this height-variance


def background_scan(rng):
    pts = []
    az = AZ_MIN
    while az <= AZ_MAX + 1e-9:
        az_rad = math.radians(az)
        r = R_MIN
        while r <= R_MAX + 1e-9:
            x = r * math.cos(az_rad)
            y = r * math.sin(az_rad)
            sigma = ANOMALY_NOISE if WORLD.is_noise_anomaly(x, y) else BASE_NOISE
            z_true = WORLD.height(x, y)
            pts.append({
                "x": x + rng.gauss(0, sigma * 0.3),
                "y": y + rng.gauss(0, sigma * 0.3),
                "z": z_true + rng.gauss(0, sigma),
                "obstacle": False,
            })
            r += R_STEP
        az += AZ_STEP_DEG
    return pts


def pole_points(pole, rng):
    r = math.hypot(pole["x"], pole["y"])
    az_step_rad = math.radians(AZ_STEP_DEG)
    subtended_rad = 2 * pole["radius"] / max(r, 0.5)
    n = max(0, round((subtended_rad / az_step_rad) * 4))
    pts = []
    z_ground = WORLD.height(pole["x"], pole["y"])
    for _ in range(n):
        ang = rng.uniform(0, 2 * math.pi)
        x = pole["x"] + pole["radius"] * math.cos(ang)
        y = pole["y"] + pole["radius"] * math.sin(ang)
        z = z_ground + pole["height"] * rng.uniform(0.3, 1.0)
        pts.append({
            "x": x + rng.gauss(0, BASE_NOISE * 0.3),
            "y": y + rng.gauss(0, BASE_NOISE * 0.3),
            "z": z + rng.gauss(0, BASE_NOISE),
            "obstacle": True,
        })
    return pts


# ---------------------------------------------------------------------------
# Deterministic resolution policies
# ---------------------------------------------------------------------------

def coarse_cell_id(x, y):
    return (math.floor(x / H_COARSE), math.floor(y / H_COARSE))


def compute_uncertain_coarse_cells(points):
    """Deterministic proxy: a coarse cell is 'uncertain' if its sampled
    ground-point heights have variance above VARIANCE_THRESHOLD. No
    learning involved -- this is a fixed statistical rule over the points
    already collected."""
    by_cell = {}
    for p in points:
        if p["obstacle"]:
            continue
        cid = coarse_cell_id(p["x"], p["y"])
        by_cell.setdefault(cid, []).append(p["z"])
    uncertain = set()
    for cid, zs in by_cell.items():
        if len(zs) >= 3 and statistics.pvariance(zs) > VARIANCE_THRESHOLD:
            uncertain.add(cid)
    return uncertain


def make_cell_fn(policy, uncertain_cells=None):
    def fine_by_distance(x, y):
        return math.hypot(x, y) < R_B

    def cell_fn(x, y):
        fine = fine_by_distance(x, y)
        if policy in ("B", "C") and WORLD.is_critical_semantic(x, y):
            fine = True
        if policy == "C" and uncertain_cells is not None and coarse_cell_id(x, y) in uncertain_cells:
            fine = True
        h = H_FINE if fine else H_COARSE
        return ("F" if fine else "C", math.floor(x / h), math.floor(y / h))

    return cell_fn


def build_grid(points, cell_fn):
    grid = {}
    for p in points:
        cid = cell_fn(p["x"], p["y"])
        cell = grid.setdefault(cid, {"ground_z": [], "obst_n": 0})
        if p["obstacle"]:
            cell["obst_n"] += 1
        else:
            cell["ground_z"].append(p["z"])
    return grid


def cell_stats(cell):
    mean_z = statistics.fmean(cell["ground_z"]) if cell["ground_z"] else None
    occ = cell["obst_n"] >= OCC_MIN_PTS
    return mean_z, occ


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def elevation_and_semantic_metrics(grid, cell_fn, region):
    """region: 'critical', 'anomaly', or 'overall'. Semantic accuracy is
    measured as whether a cell's OWN resolution choice matches the ground-
    truth importance of its content (fine cell over critical/anomalous
    content = correct; coarse cell over such content = a miss) -- the
    direct, representation-level meaning of 'semantic accuracy' for a
    resolution policy, as opposed to a downstream classifier's accuracy."""
    errs = []
    correct_alloc, total_alloc = 0, 0
    x, y = 0.3, -5.5
    step = H_FINE
    xs = []
    xv = 0.3
    while xv < 21.0:
        xs.append(xv)
        xv += step
    ys = []
    yv = -5.5
    while yv < 5.5:
        ys.append(yv)
        yv += step

    for x in xs:
        for y in ys:
            in_region = {
                "critical": WORLD.is_critical_semantic(x, y),
                "anomaly": WORLD.is_noise_anomaly(x, y),
                "overall": True,
            }[region]
            if not in_region:
                continue
            cid = cell_fn(x, y)
            is_fine = cid[0] == "F"
            total_alloc += 1
            important = WORLD.is_critical_semantic(x, y) or WORLD.is_noise_anomaly(x, y)
            if is_fine == important or (region == "overall" and not important and not is_fine):
                correct_alloc += 1
            cell = grid.get(cid)
            if cell is None:
                continue
            mean_z, occ = cell_stats(cell)
            if mean_z is not None and not occ:
                errs.append(abs(mean_z - WORLD.height(x, y)))
    return {
        "elevation_mae": round(statistics.fmean(errs), 4) if errs else None,
        "n_elev_samples": len(errs),
        "allocation_correct_rate": round(correct_alloc / total_alloc, 4) if total_alloc else None,
    }


def object_metrics(grid, cell_fn, pole):
    touched = set()
    x0, y0, r0 = pole["x"], pole["y"], pole["radius"] + H_COARSE
    xv = x0 - r0
    while xv <= x0 + r0:
        yv = y0 - r0
        while yv <= y0 + r0:
            if (xv - x0) ** 2 + (yv - y0) ** 2 <= (pole["radius"] * 1.5) ** 2:
                touched.add(cell_fn(xv, yv))
            yv += 0.05
        xv += 0.05
    occ_cells = []
    for cid in touched:
        cell = grid.get(cid)
        if cell is None:
            continue
        _, occ = cell_stats(cell)
        if occ:
            occ_cells.append(cid)
    return {"detected": len(occ_cells) > 0, "occ_cell_count": len(occ_cells)}


def overhead_metrics(points, cell_fn, repeats=5):
    t0 = time.perf_counter()
    for _ in range(repeats):
        g = build_grid(points, cell_fn)
    dt = (time.perf_counter() - t0) / repeats
    return {"build_ms": round(dt * 1000, 3), "cell_count": len(g)}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run():
    rng = random.Random(7)
    bg = background_scan(rng)
    pole_pts = pole_points(POLE, rng)
    all_points = bg + pole_pts

    uncertain_cells = compute_uncertain_coarse_cells(bg)

    results = {}
    for policy in ("A", "B", "C"):
        cell_fn = make_cell_fn(policy, uncertain_cells if policy == "C" else None)
        grid = build_grid(all_points, cell_fn)
        overall = elevation_and_semantic_metrics(grid, cell_fn, "overall")
        critical = elevation_and_semantic_metrics(grid, cell_fn, "critical")
        anomaly = elevation_and_semantic_metrics(grid, cell_fn, "anomaly")
        obj = object_metrics(grid, cell_fn, POLE)
        overhead = overhead_metrics(all_points, cell_fn)
        results[policy] = {
            "overall": overall,
            "critical_region": critical,
            "anomaly_region": anomaly,
            "object": obj,
            "overhead": overhead,
        }

    # resolution efficiency: of the EXTRA fine cells a policy uses beyond
    # policy A's fine-cell count, what fraction actually overlap
    # ground-truth-important content (critical patch or anomaly patch)?
    def fine_cell_ids(policy):
        cell_fn = make_cell_fn(policy, uncertain_cells if policy == "C" else None)
        grid = build_grid(all_points, cell_fn)
        return set(cid for cid in grid if cid[0] == "F"), cell_fn

    fine_a, fn_a = fine_cell_ids("A")
    fine_b, fn_b = fine_cell_ids("B")
    fine_c, fn_c = fine_cell_ids("C")

    def important_fraction(extra_cells, h):
        if not extra_cells:
            return None
        important = 0
        for cid in extra_cells:
            cx, cy = (cid[1] + 0.5) * h, (cid[2] + 0.5) * h
            if WORLD.is_critical_semantic(cx, cy) or WORLD.is_noise_anomaly(cx, cy):
                important += 1
        return round(important / len(extra_cells), 4)

    extra_b = fine_b - fine_a
    extra_c = fine_c - fine_b
    efficiency = {
        "B_extra_fine_cells_over_A": len(extra_b),
        "B_extra_cells_on_important_content": important_fraction(extra_b, H_FINE),
        "C_extra_fine_cells_over_B": len(extra_c),
        "C_extra_cells_on_important_content": important_fraction(extra_c, H_FINE),
    }

    # distance-vs-uncertainty correlation in the NORMAL (non-anomalous) map:
    # does variance already increase with range, i.e. is uncertainty
    # partly redundant with distance even before the deliberate anomaly?
    by_cell = {}
    for p in bg:
        cid = coarse_cell_id(p["x"], p["y"])
        by_cell.setdefault(cid, []).append(p)
    rows = []
    for cid, pts in by_cell.items():
        if len(pts) < 3:
            continue
        cx = statistics.fmean(p["x"] for p in pts)
        cy = statistics.fmean(p["y"] for p in pts)
        if WORLD.is_noise_anomaly(cx, cy):
            continue  # exclude the deliberate anomaly from the "normal" correlation
        r = math.hypot(cx, cy)
        var = statistics.pvariance(p["z"] for p in pts)
        rows.append((r, var))
    if len(rows) > 2:
        rs = [r for r, _ in rows]
        vs = [v for _, v in rows]
        mr, mv = statistics.fmean(rs), statistics.fmean(vs)
        cov = statistics.fmean((r - mr) * (v - mv) for r, v in rows)
        sr = statistics.pstdev(rs)
        sv = statistics.pstdev(vs)
        corr = cov / (sr * sv) if sr > 0 and sv > 0 else None
    else:
        corr = None

    out = {
        "policies": results,
        "resolution_efficiency": efficiency,
        "distance_uncertainty_correlation_normal_map": round(corr, 4) if corr is not None else None,
        "n_uncertain_coarse_cells_flagged": len(uncertain_cells),
    }

    out_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "driver_ablation_results.json"), "w") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    run()
