"""Read-only provenance arithmetic; writes results beside this script only."""
from pathlib import Path
import hashlib
import json
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
INPUT = ROOT / 'artifacts/authoring_A_v1/cut_arrays.npz'
RECORD = ROOT / 'artifacts/authoring_A_v1/authoring.json'
record = json.loads(RECORD.read_text())
cfg = record['config']
data = np.load(INPUT)
door, fixed = data['door'], data['fixed']
ds, fs = data['door_source'], data['fixed_source']
assert door.shape[1:] == (3, 8) and fixed.shape[1:] == (3, 8)
assert len(ds) == len(door) and len(fs) == len(fixed)
xyz = door[:, :, :3]
cross = np.cross(xyz[:, 1] - xyz[:, 0], xyz[:, 2] - xyz[:, 0])
twice_area = np.linalg.norm(cross, axis=1)
areas = twice_area / 2
centers = xyz.mean(axis=1)
normal_dot = -cross[:, 1] / np.maximum(twice_area, 1e-30)
shared = np.isin(ds, np.unique(fs))
total_area = float(areas.sum())

def quantiles(values, weights):
    ix = np.argsort(values)
    c = np.cumsum(weights[ix])
    if not len(c) or c[-1] <= 0:
        return None
    c /= c[-1]
    return {str(q): float(np.interp(q, c, values[ix])) for q in [.0, .1, .25, .5, .75, .9, 1.]}

normal_masks = {
    'faces_toward_near_side_dot_ge_0_5': normal_dot >= .5,
    'oblique_or_tangent_abs_dot_lt_0_5': np.abs(normal_dot) < .5,
    'faces_away_from_near_side_dot_le_minus_0_5': normal_dot <= -.5,
}
depth_bins = [-.2, -.18, -.165, -.15, -.13, -.115, -.1 + 1e-9]

def basic(mask):
    a = float(areas[mask].sum())
    if not mask.any():
        return {'triangles': 0, 'area': 0.0, 'area_fraction_of_total_door': 0.0}
    return {
        'triangles': int(mask.sum()),
        'source_faces': int(len(np.unique(ds[mask]))),
        'area': a,
        'area_fraction_of_total_door': a / total_area,
        'vertex_bounds_xyz': [xyz[mask].min(axis=(0, 1)).tolist(), xyz[mask].max(axis=(0, 1)).tolist()],
        'area_weighted_centroid_y_quantiles': quantiles(centers[mask, 1], areas[mask]),
        'area_weighted_mean_geometric_normal_dot_minus_y': float(np.sum(areas[mask] * normal_dot[mask]) / a),
    }

def summary(mask):
    result = basic(mask)
    result['normal_categories'] = {name: basic(mask & n) for name, n in normal_masks.items()}
    result['centroid_y_bins'] = [
        {'min_y_inclusive': lo, 'max_y_exclusive': hi, **basic(mask & (centers[:, 1] >= lo) & (centers[:, 1] < hi))}
        for lo, hi in zip(depth_bins[:-1], depth_bins[1:])
    ]
    return result

# Match authoring's geometry-only edge accounting: 7-decimal position weld,
# deliberately ignoring UV/normal seams. This is a diagnostic convention.
vertices, vertex_ids = np.unique(np.round(xyz.reshape(-1, 3), 7), axis=0, return_inverse=True)
faces = vertex_ids.reshape(-1, 3)
edges = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
edge_faces = np.tile(np.arange(len(faces)), 3)
_, edge_inverse, edge_counts = np.unique(np.sort(edges, axis=1), axis=0, return_inverse=True, return_counts=True)
boundary_mask = edge_counts[edge_inverse] == 1
boundary_pairs = edges[boundary_mask]
boundary_faces = edge_faces[boundary_mask]
boundary_xyz = vertices[boundary_pairs]
lengths = np.linalg.norm(boundary_xyz[:, 1] - boundary_xyz[:, 0], axis=1)
polygon = np.array(cfg['polygon_xz'])
planes = []
for p, q in zip(polygon, np.roll(polygon, -1, axis=0)):
    delta = q - p
    n = np.array([-delta[1], 0, delta[0]])
    n /= np.linalg.norm(n)
    planes.append((n, float(n @ np.array([p[0], 0, p[1]]))))
tol = 2e-6
plane_distances = np.stack([np.max(np.abs(boundary_xyz @ n - c), axis=1) for n, c in planes], axis=1)
on_xz = (plane_distances <= tol).any(axis=1)
on_y = np.max(np.abs(boundary_xyz[:, :, 1] - cfg['side_y_max']), axis=1) <= tol

def edge_summary(mask):
    return {
        'edges': int(mask.sum()),
        'length': float(lengths[mask].sum()),
        'length_fraction_of_all_boundary': float(lengths[mask].sum() / lengths.sum()),
        'incident_door_triangles_from_shared_source': int(shared[boundary_faces[mask]].sum()),
        'length_incident_to_shared_source': float(lengths[mask & shared[boundary_faces]].sum()),
        'edge_midpoint_y_range': [float(boundary_xyz[mask].mean(axis=1)[:, 1].min()), float(boundary_xyz[mask].mean(axis=1)[:, 1].max())] if mask.any() else None,
    }

# Edge-connected components identify detached regions without labeling them
# semantically. A component can detach because of selection, seams, or source.
parent = np.arange(len(faces))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return int(x)
def union(a, b):
    a, b = find(int(a)), find(int(b))
    if a != b:
        parent[b] = a
order = np.argsort(edge_inverse)
sorted_groups = edge_inverse[order]
starts = np.r_[0, np.where(np.diff(sorted_groups))[0] + 1]
ends = np.r_[starts[1:], len(order)]
for start, end in zip(starts, ends):
    if end - start > 1:
        incident = edge_faces[order[start:end]]
        for other in incident[1:]:
            union(incident[0], other)
roots = np.array([find(i) for i in range(len(faces))])
component_ids = np.unique(roots)
components = []
for cid in component_ids:
    mask = roots == cid
    components.append({'component_id': int(cid), **basic(mask), 'shared_source_area_fraction_of_component': float(areas[mask & shared].sum() / areas[mask].sum()), 'normal_categories': {name: basic(mask & n) for name, n in normal_masks.items()}})
components.sort(key=lambda x: x['area'], reverse=True)

unique_ds, ds_counts = np.unique(ds, return_counts=True)
result = {
    'input_npz': str(INPUT.relative_to(ROOT)),
    'input_npz_sha256': hashlib.sha256(INPUT.read_bytes()).hexdigest(),
    'authoring_record_sha256': hashlib.sha256(RECORD.read_bytes()).hexdigest(),
    'config_from_executed_authoring_record': cfg,
    'schema': {k: {'shape': list(data[k].shape), 'dtype': str(data[k].dtype)} for k in data.files},
    'definitions': {
        'exclusive_to_door_source': 'Original source triangle ID occurs only in door output; operational wholly-inside provenance. One output triangle per source supports an uncut original face, but original source coordinates were not independently reloaded.',
        'shared_with_fixed_source': 'Original source triangle ID occurs in both door and fixed output, so selected triangles are pieces from a partitioned source triangle.',
        'normal_categories': 'Area-weighted geometric face winding dot with (0,-1,0), not stored shading normals. Tangent faces can be legitimate frame/edge surfaces; inward-facing faces are not automatically defects.',
        'depth': 'Native normalized units; centroid Y is a coarse location proxy, not a reliable semantic outer-skin classifier.',
        'boundary': 'Geometry vertices welded by rounding XYZ to 7 decimals. Edge occurs once in selected output. Plane tests require both endpoints within 2e-6, matching authoring tolerance.',
        'off_plane_boundary': 'Not on an XZ polygon or depth clipping plane. Compatible with pre-existing openings or source discontinuities; this test alone does not establish origin or visual failure.',
    },
    'all_door': summary(np.ones(len(door), dtype=bool)),
    'exclusive_to_door_source': summary(~shared),
    'shared_with_fixed_source': summary(shared),
    'source_face_counts': {
        'distinct_door_source_faces': int(len(unique_ds)),
        'shared_source_faces': int(len(np.intersect1d(ds, fs))),
        'exclusive_source_faces_with_multiple_output_triangles': int(((ds_counts > 1) & ~np.isin(unique_ds, fs)).sum()),
    },
    'boundary': {
        'all': edge_summary(np.ones(len(boundary_pairs), dtype=bool)),
        'xz_planes_only': edge_summary(on_xz & ~on_y),
        'depth_y_plane_only': edge_summary(on_y & ~on_xz),
        'xz_and_depth_planes': edge_summary(on_xz & on_y),
        'neither_plane_family': edge_summary(~on_xz & ~on_y),
        'by_xz_polygon_edge': [{'polygon_edge_index': i, 'endpoints_xz': [polygon[i].tolist(), polygon[(i + 1) % len(polygon)].tolist()], **edge_summary(plane_distances[:, i] <= tol)} for i in range(len(planes))],
        'geometric_edges_with_incidence_gt_2': int((edge_counts > 2).sum()),
    },
    'edge_connected_components': {'count': len(components), 'largest_20': components[:20]},
    'limits': [
        'No asset modification, rendering, semantic segmentation, source-quality judgment, or collision test.',
        'The single depth-prism selection may retain original internal/back-facing sheets. Original provenance does not make an undesired moving region an intrinsic generator failure.',
        'Whether visible ragged regions correspond to retained original faces or cut pieces needs the parent provenance render; area dominance alone does not identify screen-space defects.',
        'Small geometric plane/rounding thresholds affect boundary counting and connectedness; this diagnostic does not certify topology.',
    ],
}
(OUT / 'selection_provenance.json').write_text(json.dumps(result, indent=2) + '\n')
np.savez_compressed(OUT / 'door_diagnostic_labels.npz', source_face_id=ds, shared_with_fixed_source=shared, triangle_area=areas, geometric_normal_dot_minus_y=normal_dot, centroid_y=centers[:, 1], component_id=roots, boundary_xyz=boundary_xyz, boundary_incident_triangle=boundary_faces, boundary_on_xz_plane=on_xz, boundary_on_depth_plane=on_y)
print(json.dumps({k: result[k] for k in ['source_face_counts']}, indent=2))
for key in ['all_door', 'exclusive_to_door_source', 'shared_with_fixed_source']:
    r = result[key]
    print(key, json.dumps({k: r[k] for k in ['triangles', 'source_faces', 'area', 'area_fraction_of_total_door']}))
    print('normal_area', json.dumps({k: v['area_fraction_of_total_door'] for k, v in r['normal_categories'].items()}))
print('boundary', json.dumps(result['boundary'], indent=2))
print('components', len(components), [(r['triangles'], r['area_fraction_of_total_door']) for r in components[:8]])
