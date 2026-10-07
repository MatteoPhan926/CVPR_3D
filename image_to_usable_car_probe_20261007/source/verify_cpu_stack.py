"""Exercise CPU meshing and colored GLB serialization, without model inference."""
from pathlib import Path
from datetime import datetime, timezone
import io
import json
import torch
import trimesh
from torchmcubes import marching_cubes, grid_interp

torch.set_num_threads(4)
a = torch.linspace(-1, 1, 24)
z, y, x = torch.meshgrid(a, a, a, indexing='ij')
field = (x*x + y*y + z*z).contiguous()
vertices, faces = marching_cubes(field, 0.5)
assert len(vertices) > 0 and len(faces) > 0
rgb = torch.stack([(x+1)*0.5, (y+1)*0.5, (z+1)*0.5]).contiguous()
colors = grid_interp(rgb, vertices)
assert colors.shape == (len(vertices), 3) and torch.isfinite(colors).all()
mesh = trimesh.Trimesh(vertices=vertices.numpy(), faces=faces.numpy(), vertex_colors=colors.numpy(), process=False)
glb = mesh.export(file_type='glb')
loaded = trimesh.load(io.BytesIO(glb), file_type='glb', force='mesh')
assert len(loaded.vertices) == len(vertices) and len(loaded.faces) == len(faces)
assert loaded.visual.kind == 'vertex'
result = {
    'status': 'passed',
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'torch': torch.__version__,
    'cuda_available': torch.cuda.is_available(),
    'smoke_input': 'synthetic 24-cubed sphere scalar field; NOT the user car or a generated candidate',
    'marching_cubes_vertices': len(vertices),
    'marching_cubes_faces': len(faces),
    'glb_bytes': len(glb),
    'glb_roundtrip_preserved_counts': True,
    'glb_roundtrip_visual_kind': loaded.visual.kind,
    'model_inference_executed': False,
}
root = Path(__file__).resolve().parents[1]
(root / 'logs/cpu-functional-smoke.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
