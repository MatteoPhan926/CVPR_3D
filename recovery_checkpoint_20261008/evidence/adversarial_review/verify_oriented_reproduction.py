"""Read-only cross-check of saved car reproduction, including winding/multiplicity."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import struct

OUT = Path(__file__).resolve().parent
PATHS = {
    "raw": Path("/workspace/image_to_usable_car_probe_20261007/raw/car_raw.glb"),
    "reproduced": Path("/workspace/research_decision_20261008/generation_execution/r256_t25.glb"),
}

def read(path):
    payload = path.read_bytes()
    assert struct.unpack_from("<4sII", payload) == (b"glTF", 2, len(payload))
    offset = 12
    doc = binary = None
    while offset < len(payload):
        n, kind = struct.unpack_from("<II", payload, offset)
        chunk = payload[offset + 8:offset + 8 + n]
        if kind == 0x4E4F534A:
            doc = json.loads(chunk)
        elif kind == 0x004E4942:
            binary = chunk
        offset += 8 + n
    def accessor(i):
        a = doc["accessors"][i]
        assert "sparse" not in a
        view = doc["bufferViews"][a["bufferView"]]
        width = {"SCALAR": 1, "VEC3": 3, "VEC4": 4}[a["type"]]
        fmt = "<" + {5121: "B", 5123: "H", 5125: "I", 5126: "f"}[a["componentType"]] * width
        size = struct.calcsize(fmt)
        base = view.get("byteOffset", 0) + a.get("byteOffset", 0)
        stride = view.get("byteStride", size)
        return [struct.unpack_from(fmt, binary, base + j * stride) for j in range(a["count"])]
    assert len(doc["meshes"]) == 1
    assert len(doc["meshes"][0]["primitives"]) == 1
    p = doc["meshes"][0]["primitives"][0]
    assert p.get("mode", 4) == 4
    verts = accessor(p["attributes"]["POSITION"])
    colors = accessor(p["attributes"]["COLOR_0"])
    indices = [v[0] for v in accessor(p["indices"])]
    faces = list(zip(indices[::3], indices[1::3], indices[2::3]))
    # Both saved files must be in the identity scene transform, so accessor
    # comparison also compares the mesh frame used by the existing diagnostics.
    transforms = [{k: n[k] for k in ("matrix", "translation", "rotation", "scale") if k in n}
                  for n in doc.get("nodes", [])]
    for n in transforms:
        assert n.get("matrix", [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]) == [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
        assert n.get("translation", [0, 0, 0]) == [0, 0, 0]
        assert n.get("rotation", [0, 0, 0, 1]) == [0, 0, 0, 1]
        assert n.get("scale", [1, 1, 1]) == [1, 1, 1]
    return verts, colors, faces, hashlib.sha256(payload).hexdigest()

def oriented(f):
    a, b, c = f
    return min((a, b, c), (b, c, a), (c, a, b))

a, b = (read(PATHS[k]) for k in ("raw", "reproduced"))
va, ca, fa, ha = a
vb, cb, fb, hb = b
lookup = {v: i for i, v in enumerate(va)}
assert len(lookup) == len(va)
mapping = [lookup[v] for v in vb]
assert len(set(mapping)) == len(va) == len(vb)
count_a = Counter(oriented(f) for f in fa)
count_b = Counter(oriented(tuple(mapping[i] for i in f)) for f in fb)
report = {
    "scope": "Independent exact accessor/identity-transform comparison; no inference or mesh edits.",
    "raw_sha256": ha,
    "reproduced_sha256": hb,
    "vertices": len(va),
    "triangles": len(fa),
    "exact_vertex_bijection": True,
    "oriented_triangle_multisets_equal": count_a == count_b,
    "max_duplicate_oriented_triangle_count_raw": max(count_a.values()),
    "exact_corresponding_RGBA": all(cb[i] == ca[j] for i, j in enumerate(mapping)),
}
(OUT / "oriented_reproduction.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
