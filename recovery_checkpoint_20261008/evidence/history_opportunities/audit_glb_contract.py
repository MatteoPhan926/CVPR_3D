"""Read-only audit of retained GLBs; writes only into this new research folder."""
from pathlib import Path
import hashlib
import json
import struct
import numpy as np

OUT = Path(__file__).resolve().parent
ASSETS = {
    "bentley_input": Path("/workspace/generated3d_authoring_clean_20261006/inputs/blue_train_bentley.glb"),
    "bentley_authored": Path("/workspace/generated3d_authoring_clean_20261006/artifacts/bentley_authored.glb"),
    "car_raw": Path("/workspace/image_to_usable_car_probe_20261007/raw/car_raw.glb"),
    "car_authored": Path("/workspace/image_to_usable_car_probe_20261007/artifacts/car_authored.glb"),
}

class GLB:
    def __init__(self, path):
        self.path = path
        self.bytes = path.read_bytes()
        self.binary = None
        assert struct.unpack_from("<4sII", self.bytes) == (b"glTF", 2, len(self.bytes))
        offset = 12
        while offset < len(self.bytes):
            length, kind = struct.unpack_from("<II", self.bytes, offset)
            content = self.bytes[offset + 8:offset + 8 + length]
            if kind == 0x4E4F534A:
                self.doc = json.loads(content)
            elif kind == 0x004E4942:
                self.binary = content
            offset += 8 + length

    def read(self, index):
        a = self.doc["accessors"][index]
        assert "sparse" not in a
        b = self.doc["bufferViews"][a["bufferView"]]
        dtype = np.dtype({5120: "i1", 5121: "u1", 5122: "<i2", 5123: "<u2", 5125: "<u4", 5126: "<f4"}[a["componentType"]])
        width = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}[a["type"]]
        offset = b.get("byteOffset", 0) + a.get("byteOffset", 0)
        return np.ndarray((a["count"], width), dtype=dtype, buffer=self.binary, offset=offset,
                          strides=(b.get("byteStride", width * dtype.itemsize), dtype.itemsize)).copy()

    def images(self):
        result = []
        for im in self.doc.get("images", []):
            b = self.doc["bufferViews"][im["bufferView"]]
            data = self.binary[b.get("byteOffset", 0):b.get("byteOffset", 0) + b["byteLength"]]
            result.append(hashlib.sha256(data).hexdigest())
        return result

    @staticmethod
    def matrix(n):
        if "matrix" in n:
            return np.array(n["matrix"], float).reshape(4, 4).T
        x, y, z, w = n.get("rotation", [0, 0, 0, 1])
        r = np.array([[1-2*y*y-2*z*z, 2*x*y-2*z*w, 2*x*z+2*y*w],
                      [2*x*y+2*z*w, 1-2*x*x-2*z*z, 2*y*z-2*x*w],
                      [2*x*z-2*y*w, 2*y*z+2*x*w, 1-2*x*x-2*y*y]])
        result = np.eye(4)
        result[:3, :3] = r @ np.diag(n.get("scale", [1, 1, 1]))
        result[:3, 3] = n.get("translation", [0, 0, 0])
        return result

    def summary(self):
        result = []
        def visit(idx, parent):
            n = self.doc["nodes"][idx]
            world = parent @ self.matrix(n)
            if "mesh" in n:
                for p in self.doc["meshes"][n["mesh"]]["primitives"]:
                    assert p.get("mode", 4) == 4
                    v = self.read(p["attributes"]["POSITION"]).astype(float)
                    v = v @ world[:3, :3].T + world[:3, 3]
                    f = self.read(p["indices"]).reshape(-1, 3)
                    t = v[f]
                    areas = np.linalg.norm(np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]), axis=1)/2
                    result.append({"node": n.get("name"), "triangles": len(f), "vertices": len(v),
                                   "world_rest_area": float(areas.sum()), "attributes": list(p["attributes"]),
                                   "material": p.get("material")})
            for child in n.get("children", []):
                visit(child, world)
        for n in self.doc["scenes"][self.doc.get("scene", 0)]["nodes"]:
            visit(n, np.eye(4))
        return {"path": str(self.path), "sha256": hashlib.sha256(self.bytes).hexdigest(),
                "primitives": result, "triangles": sum(p["triangles"] for p in result),
                "world_rest_area": sum(p["world_rest_area"] for p in result),
                "image_sha256": self.images(), "materials": self.doc.get("materials", []),
                "animations": len(self.doc.get("animations", []))}

g = {key: GLB(path) for key, path in ASSETS.items()}
s = {key: obj.summary() for key, obj in g.items()}
b0, b1 = g["bentley_input"], g["bentley_authored"]
unchanged = []
for n in b0.doc["nodes"]:
    if "mesh" not in n or n.get("name") in {"Object_15", "Object_18", "Object_20", "Object_21"}:
        continue
    m = next(k for k in b1.doc["nodes"] if k.get("name") == n.get("name"))
    p = b0.doc["meshes"][n["mesh"]]["primitives"]
    q = b1.doc["meshes"][m["mesh"]]["primitives"]
    equal = len(p) == len(q) and all(
        set(a["attributes"]) == set(b["attributes"]) and
        all(np.array_equal(b0.read(a["attributes"][x]), b1.read(b["attributes"][x])) for x in a["attributes"]) and
        np.array_equal(b0.read(a["indices"]), b1.read(b["indices"])) for a, b in zip(p, q))
    unchanged.append({"node": n.get("name"), "all_accessor_values_identical": equal})
car = s["car_authored"]["primitives"]
outer = [p for p in car if p["node"] in {"Body_fixed_generated_surface", "Door_generated_outer_surface"}]
added = [p for p in car if p not in outer]
raw_area = s["car_raw"]["world_rest_area"]
metrics = {
    "bentley_material_definitions_identical": b0.doc.get("materials") == b1.doc.get("materials"),
    "bentley_image_payloads_identical": b0.images() == b1.images(),
    "bentley_texture_definitions_identical": b0.doc.get("textures") == b1.doc.get("textures"),
    "bentley_untouched_geometry": unchanged,
    "bentley_total_area_difference": s["bentley_authored"]["world_rest_area"] - s["bentley_input"]["world_rest_area"],
    "car_outer_area_relative_difference": sum(p["world_rest_area"] for p in outer)/raw_area - 1,
    "car_moving_outer_area_fraction": next(p["world_rest_area"] for p in outer if p["node"] == "Door_generated_outer_surface")/raw_area,
    "car_added_area_fraction": sum(p["world_rest_area"] for p in added)/raw_area,
    "car_added_triangle_fraction": sum(p["triangles"] for p in added)/s["car_raw"]["triangles"],
    "car_outer_triangle_increase": sum(p["triangles"] for p in outer)-s["car_raw"]["triangles"],
}
report = {"scope": "Fresh read-only measurements of on-disk exported GLBs on 2026-10-08. No source pipeline re-run, model inference, rendering or user trial.",
          "limits": "Area conservation does not prove semantic ownership, correspondence, geometry identity, usable appearance or clearance. Added-area fraction describes authored surface amount, not workload or effect size.",
          "assets": s, "metrics": metrics}
(OUT/"artifact_contract_measurements.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(metrics, indent=2))
