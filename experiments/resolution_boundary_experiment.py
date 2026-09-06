"""
Feasibility experiment: are resolution-boundary inconsistencies large enough
to matter for 2.5D LiDAR terrain/object/dynamic perception?

Scope: this is a small, targeted synthetic experiment answering ONE question
(per research/resolution_boundary_consistency.md section 9). It is NOT the
SIH pipeline, NOT an architecture choice, and uses NO real dataset and NO
learned model. Pure stdlib (no numpy) -- grid/point counts here are small
enough that plain-Python loops finish in seconds.

Synthetic world (fully documented, all ground truth is an exact closed-form
function -- see World class):
  - flat ground for range x < 8m
  - a smooth ~0.3m height step ("curb") for x in [8,9]
  - flat higher ground for x in [9,14]
  - a further gentle continuous slope (+0.2m over 6m) for x in [14,20]
  - a semantic boundary at y=0 ("A" for y<0, "B" for y>=0), deliberately
    NOT aligned with the (range-based) resolution-tier boundary
  - static thin poles (obstacles) at documented positions relative to the
    resolution boundary, at three radii (thin/medium/large)
  - one moving object crossing the resolution boundary at constant velocity

Sensor model (documented simplification): a forward-looking multi-channel
scanning range sensor at the origin, height 1.6m. Ground/terrain points are
generated on a fixed (azimuth, elevation-channel) ray grid, intersected with
a *flat reference plane* at height 0 to get each ray's ground range (real
sensor: channel elevation angles are evenly spaced, so ground-point spacing
grows with range -- exactly the well-known real-LiDAR ground-density falloff
this project's own literature review flagged, e.g. Cylinder3D's coordinate-
frame effect). This is an approximation for gently-sloped terrain and is
documented as such, not claimed as full ray-tracing physics. Obstacle
(pole) points are sampled directly on each pole's surface with a point
count that falls off with range (1/r, floor of 3 points), a documented
proxy for the same real angular-resolution falloff, rather than full
ray-cylinder intersection. Both point families receive independent
Gaussian noise on position/height (the swept "sensor noise" parameter).

Representations compared (see cell_id_* functions):
  U  Uniform      -- single fixed cell size everywhere.
  N  Naive tier   -- hard range cutoff at R_b: fine inside, coarse outside.
     This matches the default behavior confirmed absent of any consistency
     mechanism in the literature review (e.g. arXiv:1602.04800).
  C  Consistency  -- N, plus one intermediate resolution tier inserted in a
     band straddling R_b, bounding the adjacent-cell size ratio at each
     interface to sqrt(k) instead of k. This is a simplified, explicitly
     documented proxy for the "2:1 balance constraint" idea found in the
     FEM/AMR literature (resolution_boundary_consistency.md section 6) --
     NOT a literal reproduction of octree 2:1-balancing.

Run: `python3 resolution_boundary_experiment.py`
Outputs: prints a summary to stdout and writes
`results/resolution_boundary_experiment_results.json` (full numeric results,
one block per swept configuration) alongside this script.
"""

import math
import random
import statistics
import time
import json
import os
from collections import Counter

# ---------------------------------------------------------------------------
# Synthetic world
# ---------------------------------------------------------------------------

class World:
    def __init__(self):
        self.poles = []  # list of dict(x, y, radius, height, name)

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

    def semantic(self, x, y):
        # Offset (0.13, not 0) deliberately so this boundary does not sit
        # exactly on a grid line for any of the tested cell sizes -- a class
        # boundary aligned with the grid could never be "split" by a single
        # cell, which would make semantic-mixing structurally untestable.
        return "A" if y < 0.13 else "B"

    def add_pole(self, x, y, radius, height, name):
        self.poles.append({"x": x, "y": y, "radius": radius, "height": height, "name": name})

    def pole_at(self, x, y):
        for p in self.poles:
            if (x - p["x"]) ** 2 + (y - p["y"]) ** 2 <= p["radius"] ** 2:
                return p
        return None


# ---------------------------------------------------------------------------
# Sensor model
#
# Documented simplification: ground/terrain coverage is generated from a
# dense (azimuth x radius) polar grid rather than a literal multi-channel
# ray-cast. Azimuth spacing is held constant (as in a real scanning sensor),
# so lateral point spacing grows linearly with range; radial spacing is
# held constant and fine enough to avoid sampling gaps, trading off some
# physical-sensor realism for reliable, gap-free ground-truth coverage
# across the whole evaluated extent. The resulting areal point density
# still falls off approximately as 1/r, matching the range-dependent
# LiDAR sparsity this project's literature review repeatedly documents
# (e.g. Cylinder3D's coordinate-frame density argument).
#
# Obstacle (pole) point counts are derived from the angular width the pole
# actually subtends at the sensor (2*radius/r) divided by the azimuth step,
# so -- unlike a fixed per-object point budget -- small/thin/far objects can
# legitimately receive very few or zero points, exactly the failure mode
# the "small/distant object loss" literature describes. This makes missed
# detection possible in this experiment, not guaranteed away by design.
# ---------------------------------------------------------------------------

AZ_MIN, AZ_MAX, AZ_STEP_DEG = -30.0, 30.0, 0.3
R_MIN, R_MAX, R_STEP = 3.0, 22.0, 0.25
OCC_MIN_PTS = 2  # cell must contain at least this many obstacle points to register occupied


def background_scan(world, noise_sigma, rng):
    """Dense ground/terrain point cloud (see sensor-model note above)."""
    pts = []
    az = AZ_MIN
    while az <= AZ_MAX + 1e-9:
        az_rad = math.radians(az)
        r = R_MIN
        while r <= R_MAX + 1e-9:
            x = r * math.cos(az_rad)
            y = r * math.sin(az_rad)
            z_true = world.height(x, y)
            x_n = x + rng.gauss(0, noise_sigma * 0.3)
            y_n = y + rng.gauss(0, noise_sigma * 0.3)
            z_n = z_true + rng.gauss(0, noise_sigma)
            pts.append({"x": x_n, "y": y_n, "z": z_n, "obstacle": False})
            r += R_STEP
        az += AZ_STEP_DEG
    return pts


def pole_points(pole, robot=(0.0, 0.0), noise_sigma=0.0, rng=None):
    """Surface points sampled on a pole; count derived from subtended angle (see note above)."""
    r = math.hypot(pole["x"] - robot[0], pole["y"] - robot[1])
    az_step_rad = math.radians(AZ_STEP_DEG)
    subtended_rad = 2 * pole["radius"] / max(r, 0.5)
    n_rays = subtended_rad / az_step_rad
    points_per_ray = 4  # vertical spread sampled per intercepting ray
    n = max(0, round(n_rays * points_per_ray))
    pts = []
    for _ in range(n):
        ang = rng.uniform(0, 2 * math.pi)
        h_frac = rng.uniform(0.3, 1.0)
        x = pole["x"] + pole["radius"] * math.cos(ang)
        y = pole["y"] + pole["radius"] * math.sin(ang)
        z = world_ground_placeholder_height + pole["height"] * h_frac  # patched below
        x_n = x + rng.gauss(0, noise_sigma * 0.3)
        y_n = y + rng.gauss(0, noise_sigma * 0.3)
        z_n = z + rng.gauss(0, noise_sigma)
        pts.append({"x": x_n, "y": y_n, "z": z_n, "obstacle": True})
    return pts


world_ground_placeholder_height = 0.0  # set per-call before invoking pole_points


def make_pole_points(world, pole, robot, noise_sigma, rng):
    global world_ground_placeholder_height
    world_ground_placeholder_height = world.height(pole["x"], pole["y"])
    return pole_points(pole, robot, noise_sigma, rng)


# ---------------------------------------------------------------------------
# Representations
# ---------------------------------------------------------------------------

def cell_uniform(x, y, h_fine):
    return ("U", math.floor(x / h_fine), math.floor(y / h_fine))


def cell_naive(x, y, h_fine, h_coarse, r_b):
    r = math.hypot(x, y)
    h = h_fine if r < r_b else h_coarse
    tier = "F" if h == h_fine else "C"
    return (tier, math.floor(x / h), math.floor(y / h))


def cell_consistency(x, y, h_fine, h_mid, h_coarse, r_lo, r_hi):
    r = math.hypot(x, y)
    if r < r_lo:
        h, tier = h_fine, "F"
    elif r < r_hi:
        h, tier = h_mid, "M"
    else:
        h, tier = h_coarse, "C"
    return (tier, math.floor(x / h), math.floor(y / h))


def make_cell_fn(kind, h_fine, k, r_b):
    h_coarse = h_fine * k
    if kind == "U":
        return lambda x, y: cell_uniform(x, y, h_fine)
    if kind == "N":
        return lambda x, y: cell_naive(x, y, h_fine, h_coarse, r_b)
    if kind == "C":
        h_mid = h_fine * math.sqrt(k)
        band_half = h_mid
        r_lo, r_hi = r_b - band_half, r_b + band_half
        return lambda x, y: cell_consistency(x, y, h_fine, h_mid, h_coarse, r_lo, r_hi)
    raise ValueError(kind)


def build_grid(points, cell_fn):
    """cell_id -> {'ground_z': [...], 'sem': Counter, 'obst_n': int}"""
    grid = {}
    for p in points:
        cid = cell_fn(p["x"], p["y"])
        cell = grid.setdefault(cid, {"ground_z": [], "sem": Counter(), "obst_n": 0})
        if p["obstacle"]:
            cell["obst_n"] += 1
        else:
            cell["ground_z"].append(p["z"])
            cell["sem"][WORLD.semantic(p["x"], p["y"])] += 1
    return grid


def cell_stats(cell):
    """occupied requires >= OCC_MIN_PTS obstacle points, not a bare any-hit rule
    (an any-hit rule would make missed detection structurally impossible)."""
    mean_z = statistics.fmean(cell["ground_z"]) if cell["ground_z"] else None
    sem = cell["sem"].most_common(1)[0][0] if cell["sem"] else None
    occ = cell["obst_n"] >= OCC_MIN_PTS
    return mean_z, sem, occ


WORLD = None  # set in main()

# ---------------------------------------------------------------------------
# Spatial metrics (elevation / occupancy / semantic vs. exact ground truth)
# ---------------------------------------------------------------------------

def spatial_metrics(world, grids, r_b, k, h_fine, band_half):
    """Evaluate on a dense query grid, binning by distance to r_b."""
    boundary_band = band_half + h_fine  # generous band definition for binning
    bins = {"boundary": {}, "interior_fine": {}, "interior_coarse": {}}
    for name in grids:
        for b in bins.values():
            b[name] = {"elev_err": [], "occ_mismatch": [], "sem_mismatch": [], "empty": 0, "n": 0}

    eval_step = h_fine
    x = 0.3
    while x < 21.0:
        y = -5.5
        while y < 5.5:
            r = math.hypot(x, y)
            if abs(r - r_b) <= boundary_band:
                bkey = "boundary"
            elif r < r_b:
                bkey = "interior_fine"
            else:
                bkey = "interior_coarse"

            true_z = world.height(x, y)
            true_pole = world.pole_at(x, y)
            true_occ = true_pole is not None
            true_sem = world.semantic(x, y)

            for name, (grid, cell_fn) in grids.items():
                cid = cell_fn(x, y)
                cell = grid.get(cid)
                rec = bins[bkey][name]
                rec["n"] += 1
                if cell is None:
                    rec["empty"] += 1
                    continue
                mean_z, sem, occ = cell_stats(cell)
                if (not true_occ) and mean_z is not None:
                    rec["elev_err"].append(abs(mean_z - true_z))
                rec["occ_mismatch"].append(1 if occ != true_occ else 0)
                if sem is not None:
                    rec["sem_mismatch"].append(1 if sem != true_sem else 0)
            y += eval_step
        x += eval_step

    out = {}
    for bkey, per_name in bins.items():
        out[bkey] = {}
        for name, rec in per_name.items():
            out[bkey][name] = {
                "elev_mae": round(statistics.fmean(rec["elev_err"]), 4) if rec["elev_err"] else None,
                "elev_max": round(max(rec["elev_err"]), 4) if rec["elev_err"] else None,
                "occ_mismatch_rate": round(statistics.fmean(rec["occ_mismatch"]), 4) if rec["occ_mismatch"] else None,
                "sem_mismatch_rate": round(statistics.fmean(rec["sem_mismatch"]), 4) if rec["sem_mismatch"] else None,
                "empty_frac": round(rec["empty"] / rec["n"], 4) if rec["n"] else None,
                "n": rec["n"],
            }
    return out


def seam_jump_metrics(world, grids, r_b, eps=0.05):
    """
    Directly targeted "elevation discontinuity AT the boundary" metric,
    distinct from the band-averaged MAE above: for several lateral offsets,
    compare the representation's own height estimate just inside r_b vs
    just outside it (eps=0.05m apart -- true terrain height differs
    negligibly over that gap at every r_b tested). A representation with no
    real resolution change (U) still shows some jump from noise/sampling
    alone; the excess for N/C beyond U's own jump is the boundary-specific
    artifact this experiment is asking about.
    """
    # Sample along the actual radial direction (tier is a function of range
    # r = hypot(x,y), not of x alone) so the two probe points genuinely
    # straddle the range-based tier boundary.
    az_samples_deg = [-20.0, -10.0, 10.0, 20.0]
    out = {name: [] for name in grids}
    for az_deg in az_samples_deg:
        az = math.radians(az_deg)
        r_in, r_out = r_b - eps, r_b + eps
        x_in, y_in = r_in * math.cos(az), r_in * math.sin(az)
        x_out, y_out = r_out * math.cos(az), r_out * math.sin(az)
        for name, (grid, cell_fn) in grids.items():
            cin = grid.get(cell_fn(x_in, y_in))
            cout = grid.get(cell_fn(x_out, y_out))
            if cin is None or cout is None:
                continue
            zin, _, _ = cell_stats(cin)
            zout, _, _ = cell_stats(cout)
            if zin is None or zout is None:
                continue
            out[name].append(abs(zout - zin))
    return {
        name: {
            "mean_seam_jump": round(statistics.fmean(vals), 4) if vals else None,
            "max_seam_jump": round(max(vals), 4) if vals else None,
            "n_samples": len(vals),
        }
        for name, vals in out.items()
    }


# ---------------------------------------------------------------------------
# Object (static pole) metrics: detection / fragmentation / size / localization
# ---------------------------------------------------------------------------

def merged_cell(background_grid, extra_points, cell_fn, cid):
    """Combine cached background cell content with a handful of extra points, for one cell id only."""
    base = background_grid.get(cid)
    ground_z = list(base["ground_z"]) if base else []
    sem = Counter(base["sem"]) if base else Counter()
    obst_n = base["obst_n"] if base else 0
    for p in extra_points:
        if cell_fn(p["x"], p["y"]) != cid:
            continue
        if p["obstacle"]:
            obst_n += 1
        else:
            ground_z.append(p["z"])
            sem[WORLD.semantic(p["x"], p["y"])] += 1
    return {"ground_z": ground_z, "sem": sem, "obst_n": obst_n}


def object_metrics(world, backgrounds, cell_fns, pole, robot, noise_sigma, rng):
    extra = make_pole_points(world, pole, robot, noise_sigma, rng)
    results = {}
    for name, cell_fn in cell_fns.items():
        touched = sorted(set(cell_fn(p["x"], p["y"]) for p in extra))
        occ_cells = []
        for cid in touched:
            cell = merged_cell(backgrounds[name], extra, cell_fn, cid)
            _, _, occ = cell_stats(cell)
            if occ:
                occ_cells.append(cid)
        detected = len(occ_cells) > 0
        # fragmentation: are the occupied cell footprints touching (share a
        # grid coordinate within 1 step in the same tier) or split apart?
        fragmented = False
        if len(occ_cells) > 1:
            tiers = set(c[0] for c in occ_cells)
            if len(tiers) > 1:
                fragmented = True
            else:
                coords = [(c[1], c[2]) for c in occ_cells]
                coords.sort()
                for i in range(1, len(coords)):
                    if abs(coords[i][0] - coords[i - 1][0]) > 1 or abs(coords[i][1] - coords[i - 1][1]) > 1:
                        fragmented = True
                        break
        results[name] = {"detected": detected, "fragmented": fragmented, "occ_cell_count": len(occ_cells)}
    return results


# ---------------------------------------------------------------------------
# Temporal metrics: object crossing the resolution boundary
# ---------------------------------------------------------------------------

def _tier_cell_size(name, tier, h_fine, k):
    if name == "U":
        return h_fine
    if tier == "F":
        return h_fine
    if tier == "M":
        return h_fine * math.sqrt(k)
    return h_fine * k  # 'C' (coarse) tier


def temporal_metrics(world, backgrounds, cell_fns, r_b, k, h_fine, noise_sigma, rng):
    """Estimated position is derived from occupied cells' own geometric
    centers (not from ground truth) -- otherwise this metric cannot reveal
    any representation-induced error by construction."""
    y_obj = 2.5
    speed = 1.0  # m/s, moving toward the robot (decreasing x)
    dt = 0.25
    x_start, x_end = r_b + 6.0, r_b - 6.0
    n_frames = int((x_start - x_end) / (speed * dt))
    t_cross = None
    series = {name: [] for name in cell_fns}

    for i in range(n_frames + 1):
        t = i * dt
        x_true = x_start - speed * t
        if t_cross is None and x_true <= r_b:
            t_cross = i
        pole = {"x": x_true, "y": y_obj, "radius": 0.15, "height": 1.0, "name": "moving"}
        extra = make_pole_points(world, pole, (0.0, 0.0), noise_sigma, rng)
        for name, cell_fn in cell_fns.items():
            touched = sorted(set(cell_fn(p["x"], p["y"]) for p in extra))
            xs = []
            for cid in touched:
                cell = merged_cell(backgrounds[name], extra, cell_fn, cid)
                _, _, occ = cell_stats(cell)
                if occ:
                    h = _tier_cell_size(name, cid[0], h_fine, k)
                    xs.append((cid[1] + 0.5) * h)  # occupied cell's own geometric center
            series[name].append(statistics.fmean(xs) if xs else None)

    out = {}
    for name, xs in series.items():
        # "away" is split by side: deep-coarse (object still far, before
        # crossing) vs deep-fine (object already near, after crossing).
        # Blending them would hide the comparison of interest, since
        # deep-coarse quantization alone already produces large per-frame
        # jumps (coarse cell width / frame step) unrelated to the boundary.
        vel_dev_cross, vel_dev_away_coarse, vel_dev_away_fine = [], [], []
        for i in range(1, len(xs)):
            if xs[i] is None or xs[i - 1] is None:
                continue
            v_est = (xs[i] - xs[i - 1]) / dt
            dev = abs(v_est - (-speed))
            if t_cross is not None and abs(i - t_cross) <= 2:
                vel_dev_cross.append(dev)
            elif t_cross is not None and i < t_cross - 2:
                vel_dev_away_coarse.append(dev)
            else:
                vel_dev_away_fine.append(dev)
        out[name] = {
            "max_vel_dev_at_crossing": round(max(vel_dev_cross), 4) if vel_dev_cross else None,
            "max_vel_dev_away_coarse_side": round(max(vel_dev_away_coarse), 4) if vel_dev_away_coarse else None,
            "max_vel_dev_away_fine_side": round(max(vel_dev_away_fine), 4) if vel_dev_away_fine else None,
            "n_missed_frames": sum(1 for v in xs if v is None),
            "n_frames": len(xs),
        }
    return out


# ---------------------------------------------------------------------------
# Overhead (build time / cell count)
# ---------------------------------------------------------------------------

def overhead_metrics(cell_fns, points, repeats=5):
    out = {}
    for name, cell_fn in cell_fns.items():
        t0 = time.perf_counter()
        for _ in range(repeats):
            g = build_grid(points, cell_fn)
        dt = (time.perf_counter() - t0) / repeats
        out[name] = {"build_ms": round(dt * 1000, 3), "cell_count": len(g)}
    return out


# ---------------------------------------------------------------------------
# One full configuration run
# ---------------------------------------------------------------------------

def run_config(world, r_b, k, noise_sigma, h_fine=0.2, seed=42, label=""):
    rng = random.Random(seed)
    world.poles = []  # persistent poles for this config's spatial (dense-grid) evaluation only
    fine_off = -min(5.0, r_b - (R_MIN + 1.0))
    for off, name in ((fine_off, "persist_fine"), (0.0, "persist_boundary"), (5.0, "persist_coarse")):
        world.add_pole(r_b + off, 4.0, radius=0.15, height=1.0, name=name)

    bg_points = background_scan(world, noise_sigma, rng)
    for p in world.poles:
        bg_points.extend(make_pole_points(world, p, (0.0, 0.0), noise_sigma, rng))

    cell_fns = {
        "U": make_cell_fn("U", h_fine, k, r_b),
        "N": make_cell_fn("N", h_fine, k, r_b),
        "C": make_cell_fn("C", h_fine, k, r_b),
    }
    backgrounds = {name: build_grid(bg_points, fn) for name, fn in cell_fns.items()}
    grids_for_spatial = {name: (backgrounds[name], cell_fns[name]) for name in cell_fns}

    h_mid = h_fine * math.sqrt(k)
    spatial = spatial_metrics(world, grids_for_spatial, r_b, k, h_fine, band_half=h_mid)
    seam = seam_jump_metrics(world, grids_for_spatial, r_b)

    # static-pole sweep: distance-from-boundary x object-size
    offsets_m = [-3 * h_fine * k, -0.5 * h_fine * k, 0.0, 0.5 * h_fine * k, 3 * h_fine * k]
    radii = {"thin": 0.05, "medium": 0.15, "large": 0.4}
    pole_results = {}
    for off in offsets_m:
        x_pole = r_b + off
        for size_name, radius in radii.items():
            pole = {"x": x_pole, "y": -3.0, "radius": radius, "height": 1.0, "name": f"{off:+.1f}_{size_name}"}
            key = f"offset={off:+.2f}m,size={size_name}"
            pole_results[key] = object_metrics(world, backgrounds, cell_fns, pole, (0.0, 0.0), noise_sigma, rng)

    temporal = temporal_metrics(world, backgrounds, cell_fns, r_b, k, h_fine, noise_sigma, rng)
    overhead = overhead_metrics(cell_fns, bg_points)

    return {
        "label": label,
        "params": {"r_b": r_b, "k": k, "noise_sigma": noise_sigma, "h_fine": h_fine},
        "spatial": spatial,
        "seam_jump": seam,
        "objects": pole_results,
        "temporal": temporal,
        "overhead": overhead,
    }


# ---------------------------------------------------------------------------
# Main: baseline + one-at-a-time sensitivity sweep
# ---------------------------------------------------------------------------

def build_world():
    w = World()
    return w


def main():
    global WORLD
    WORLD = build_world()

    baseline = dict(r_b=10.0, k=4, noise_sigma=0.02, h_fine=0.2, seed=42)
    configs = [dict(baseline, label="baseline")]
    for r_b in (6.0, 14.0):
        configs.append(dict(baseline, r_b=r_b, label=f"sens_r_b={r_b}"))
    for k in (2, 8):
        configs.append(dict(baseline, k=k, label=f"sens_k={k}"))
    for noise in (0.0, 0.05):
        configs.append(dict(baseline, noise_sigma=noise, label=f"sens_noise={noise}"))

    all_results = []
    for cfg in configs:
        label = cfg.pop("label")
        print(f"Running config: {label} {cfg}")
        res = run_config(WORLD, label=label, **cfg)
        all_results.append(res)

    out_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "resolution_boundary_experiment_results.json")
    with open(out_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nWrote full results to {out_path}")

    # ---- condensed console summary ----
    print("\n=== BASELINE spatial metrics (elevation MAE in meters) ===")
    base = all_results[0]
    for bkey in ("interior_fine", "boundary", "interior_coarse"):
        row = base["spatial"][bkey]
        print(f"  {bkey:15s}", {n: row[n]["elev_mae"] for n in ("U", "N", "C")})

    print("\n=== BASELINE spatial metrics (occupancy mismatch rate) ===")
    for bkey in ("interior_fine", "boundary", "interior_coarse"):
        row = base["spatial"][bkey]
        print(f"  {bkey:15s}", {n: row[n]["occ_mismatch_rate"] for n in ("U", "N", "C")})

    print("\n=== BASELINE seam-jump at the boundary (meters; excess vs U reveals a boundary-specific artifact) ===")
    print("  ", {n: base["seam_jump"][n]["mean_seam_jump"] for n in ("U", "N", "C")})

    print("\n=== BASELINE spatial metrics (semantic mismatch rate) ===")
    for bkey in ("interior_fine", "boundary", "interior_coarse"):
        row = base["spatial"][bkey]
        print(f"  {bkey:15s}", {n: row[n]["sem_mismatch_rate"] for n in ("U", "N", "C")})

    print("\n=== BASELINE object detection/fragmentation (offset relative to R_b) ===")
    for key, res in base["objects"].items():
        print(f"  {key:30s}", {n: (res[n]["detected"], res[n]["fragmented"], res[n]["occ_cell_count"]) for n in ("U", "N", "C")})

    print("\n=== BASELINE temporal (velocity deviation, m/s) ===")
    for n, rec in base["temporal"].items():
        print(f"  {n}: at-crossing={rec['max_vel_dev_at_crossing']} away_coarse_side={rec['max_vel_dev_away_coarse_side']} away_fine_side={rec['max_vel_dev_away_fine_side']} missed={rec['n_missed_frames']}/{rec['n_frames']}")

    print("\n=== BASELINE overhead ===")
    for n, rec in base["overhead"].items():
        print(f"  {n}: build_ms={rec['build_ms']} cell_count={rec['cell_count']}")


if __name__ == "__main__":
    main()
