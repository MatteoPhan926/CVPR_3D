"""Component orientation audit of the original saved partition, read-only."""
import numpy as np,json
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]
p=np.load('/workspace/image_to_usable_car_probe_20261007/artifacts/door_parts.npz')
v=p['door_v'];f=p['door_f'];parent=np.arange(len(v))
def root(i):
    while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
    return i
for face in f:
    for a,b in zip(face,face[1:]):parent[root(int(a))]=root(int(b))
groups={}
for i,face in enumerate(f):groups.setdefault(root(int(face[0])),[]).append(i)
result=[]
for ids in groups.values():
    t=v[f[ids]];cross=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0])
    areas=np.linalg.norm(cross,axis=1)/2;normal=cross/(2*areas[:,None])
    result.append({'triangles':len(ids),'area':float(areas.sum()),
      'area_weighted_abs_normal_xyz':np.average(np.abs(normal),weights=areas,axis=0).tolist(),
      'area_fraction_nearly_horizontal_abs_nz_gt_0.8':float(areas[np.abs(normal[:,2])>.8].sum()/areas.sum()),
      'area_fraction_nearly_vertical_abs_nz_lt_0.2':float(areas[np.abs(normal[:,2])<.2].sum()/areas.sum()),
      'bounds':[t.reshape(-1,3).min(0).tolist(),t.reshape(-1,3).max(0).tolist()]})
(OUT/'measurements/selection_components.json').write_text(json.dumps(sorted(result,key=lambda x:-x['area']),indent=2)+'\n')
