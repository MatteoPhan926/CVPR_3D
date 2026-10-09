"""Read-only raw sample geometry diagnostic prompted by validator/import differences."""
import hashlib, json, struct
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1]
source=root/'research/public_fal_sample/official_public_example.glb'
data=source.read_bytes(); pos=12; doc=None; binary=None
while pos<len(data):
    n,t=struct.unpack_from('<II',data,pos);pos+=8
    if t==0x4e4f534a:doc=json.loads(data[pos:pos+n])
    elif t==0x004e4942:binary=data[pos:pos+n]
    pos+=n
def accessor(index):
    a=doc['accessors'][index];v=doc['bufferViews'][a['bufferView']]
    assert v['buffer']==0 and 'sparse' not in a
    dtype=np.dtype({5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']])
    width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    stride=v.get('byteStride',width*dtype.itemsize)
    return np.ndarray((a['count'],width),dtype=dtype,buffer=binary,
        offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(stride,dtype.itemsize))
p=doc['meshes'][0]['primitives'][0];assert p.get('mode',4)==4
vertices=accessor(p['attributes']['POSITION']).astype(np.float64)
normals=accessor(p['attributes']['NORMAL']).astype(np.float64)
faces=accessor(p['indices']).reshape(-1,3)
lengths=np.linalg.norm(normals,axis=1)
repeated=(faces[:,0]==faces[:,1])|(faces[:,1]==faces[:,2])|(faces[:,0]==faces[:,2])
cross=np.cross(vertices[faces[:,1]]-vertices[faces[:,0]],vertices[faces[:,2]]-vertices[faces[:,0]])
twice_area=np.linalg.norm(cross,axis=1)
blender=json.loads((root/'research/public_fal_sample/blender_import.json').read_text())
result={'input_sha256':hashlib.sha256(data).hexdigest(),'raw_vertices':len(vertices),'raw_triangles':len(faces),
    'normals_below_1e_minus_6':int((lengths<1e-6).sum()),'nonfinite_normals':int((~np.isfinite(normals)).sum()),
    'triangles_with_repeated_vertex_indices':int(repeated.sum()),'exact_zero_area_triangles':int((twice_area==0).sum()),
    'triangles_with_double_area_at_most_1e_minus_15':int((twice_area<=1e-15).sum()),
    'imported_polygons':sum(m['polygons'] for m in blender['meshes']),
    'triangle_polygon_count_difference':int(len(faces)-sum(m['polygons'] for m in blender['meshes'])),
    'interpretation':'Read-only numeric diagnostics of one public example. Count agreement alone does not prove which faces the importer changed. No repair, export, render, car-quality or general model conclusion.'}
with (root/'research/public_fal_sample/normal_and_face_diagnostic.json').open('x') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
