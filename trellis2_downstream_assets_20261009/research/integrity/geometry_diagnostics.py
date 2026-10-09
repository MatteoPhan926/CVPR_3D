"""Read-only GLB geometry/native texture diagnostics. Writes only the named new JSON."""
import argparse, hashlib, io, json, struct
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components

def read_glb(path):
    raw=Path(path).read_bytes()
    magic,version,total=struct.unpack_from('<4sII',raw)
    assert magic==b'glTF' and version==2 and total==len(raw)
    at=12; doc=None; binary=None
    while at<total:
        size,kind=struct.unpack_from('<II',raw,at); at+=8
        chunk=raw[at:at+size]; at+=size
        if kind==0x4e4f534a: doc=json.loads(chunk)
        elif kind==0x004e4942: binary=chunk
    return raw,doc,binary

def accessor(doc,binary,index):
    a=doc['accessors'][index]; b=doc['bufferViews'][a['bufferView']]
    assert 'sparse' not in a and b['buffer']==0
    dtype=np.dtype({5120:'i1',5121:'u1',5122:'<i2',5123:'<u2',5125:'<u4',5126:'<f4'}[a['componentType']])
    dims={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    offset=b.get('byteOffset',0)+a.get('byteOffset',0)
    return np.ndarray((a['count'],dims),dtype=dtype,buffer=binary,offset=offset,strides=(b.get('byteStride',dims*dtype.itemsize),dtype.itemsize)).copy()

def quantiles(x):
    return {str(q):float(v) for q,v in zip([0,1,10,50,90,99,100],np.percentile(x,[0,1,10,50,90,99,100]))}

def topology(pos,faces,areas,details=False):
    edges=np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]])
    keys=np.sort(edges,axis=1)
    unique,inv,counts=np.unique(keys,axis=0,return_inverse=True,return_counts=True)
    orientation=np.bincount(inv,weights=np.where(edges[:,0]<edges[:,1],1,-1))
    graph=coo_matrix((np.ones(len(unique)),(unique[:,0],unique[:,1])),shape=(len(pos),len(pos))).tocsr()
    ncomp,labels=connected_components(graph,directed=False)
    face_labels=labels[faces[:,0]]
    facecounts=np.bincount(face_labels,minlength=ncomp)
    comareas=np.bincount(face_labels,weights=areas,minlength=ncomp)
    order=np.argsort(facecounts)[::-1]
    result={'vertices':len(pos),'edges':len(unique),'faces':len(faces),'components_with_faces':int(np.count_nonzero(facecounts)),
      'unused_vertices':int(len(pos)-len(np.unique(faces))), 'boundary_edges':int(np.sum(counts==1)),
      'nonmanifold_edges_more_than_two_faces':int(np.sum(counts>2)),
      'two_face_edges_same_direction':int(np.sum((counts==2)&(orientation!=0))),
      'edge_incidence_max':int(counts.max()),'euler_characteristic':int(len(pos)-len(unique)+len(faces)),
      'duplicate_unoriented_faces':int(len(faces)-len(np.unique(np.sort(faces,axis=1),axis=0))),
      'largest_component_face_fraction':float(facecounts[order[0]]/len(faces)),
      'largest_component_area_fraction':float(comareas[order[0]]/areas.sum()),
      'component_face_counts_top20':facecounts[order[:20]].tolist()}
    if details:
        result['components_top20']=[]
        for lab in order[:20]:
            cp=pos[labels==lab]
            result['components_top20'].append({'component':int(lab),'faces':int(facecounts[lab]),'area':float(comareas[lab]),
              'bounds_min':cp.min(0).tolist(),'bounds_max':cp.max(0).tolist(),'extents':np.ptp(cp,axis=0).tolist()})
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('output');a=p.parse_args()
    raw,doc,binary=read_glb(a.input)
    assert len(doc['meshes'])==1 and len(doc['meshes'][0]['primitives'])==1
    prim=doc['meshes'][0]['primitives'][0]; attrs=prim['attributes']
    pos=accessor(doc,binary,attrs['POSITION']).astype(np.float64)
    uv=accessor(doc,binary,attrs['TEXCOORD_0']).astype(np.float64)
    normals=accessor(doc,binary,attrs['NORMAL']).astype(np.float64)
    faces=accessor(doc,binary,prim['indices']).reshape(-1,3)
    assert np.isfinite(pos).all() and np.isfinite(uv).all() and np.isfinite(normals).all()
    cross=np.cross(pos[faces[:,1]]-pos[faces[:,0]],pos[faces[:,2]]-pos[faces[:,0]])
    areas=np.linalg.norm(cross,axis=1)/2
    e1=uv[faces[:,1]]-uv[faces[:,0]];e2=uv[faces[:,2]]-uv[faces[:,0]]
    signed_uvarea=(e1[:,0]*e2[:,1]-e1[:,1]*e2[:,0])/2
    welded,inverse=np.unique(pos,axis=0,return_inverse=True)
    # Exact-position welding is diagnostic only: no source geometry is changed.
    dot=np.einsum('ij,ij->i',cross,normals[faces].mean(1))
    report={'input':a.input,'sha256':hashlib.sha256(raw).hexdigest(),
      'scope':'Diagnostic only. No geometric edits; exact weld is a measured topology view, not a repair. No provenance or controlled comparison inference.',
      'nodes':doc.get('nodes',[]),'bounds_min':pos.min(0).tolist(),'bounds_max':pos.max(0).tolist(),
      'extents':np.ptp(pos,axis=0).tolist(),'surface_area':float(areas.sum()),
      'area_quantiles':quantiles(areas),'zero_area_triangles':int(np.sum(areas==0)),
      'triangles_area_le_1e-12':int(np.sum(areas<=1e-12)),
      'normal_length_quantiles':quantiles(np.linalg.norm(normals,axis=1)),
      'faces_average_vertex_normal_opposes_geometric_normal':int(np.sum(dot<0)),
      'area_fraction_average_vertex_normal_opposes_geometric_normal':float(areas[dot<0].sum()/areas.sum()),
      'uv':{'min':uv.min(0).tolist(),'max':uv.max(0).tolist(),
        'vertices_outside_unit_square':int(np.sum(np.any((uv<0)|(uv>1),axis=1))),
        'zero_uv_area_triangles':int(np.sum(signed_uvarea==0)),
        'geometric_area_fraction_zero_uv_area':float(areas[signed_uvarea==0].sum()/areas.sum()),
        'sum_absolute_triangle_uv_area':float(np.abs(signed_uvarea).sum()),
        'positive_uv_orientation_faces':int(np.sum(signed_uvarea>0)),
        'negative_uv_orientation_faces':int(np.sum(signed_uvarea<0)),
        'note':'Sum of triangle UV areas is not an overlap-free atlas occupancy metric.'},
      'native_index_topology':topology(pos,faces,areas),
      'exact_position_weld_topology':topology(welded,inverse[faces],areas,True),
      'images':[]}
    for ii,im in enumerate(doc.get('images',[])):
        b=doc['bufferViews'][im['bufferView']];o=b.get('byteOffset',0)
        encoded=binary[o:o+b['byteLength']];img=Image.open(io.BytesIO(encoded));arr=np.asarray(img)
        role='baseColor' if ii==0 else 'metallicRoughness (G roughness, B metallic)'
        report['images'].append({'index':ii,'role':role,'size':list(img.size),'mode':img.mode,
          'encoded_sha256':hashlib.sha256(encoded).hexdigest(),'decoded_pixel_sha256':hashlib.sha256(arr.tobytes()).hexdigest(),
          'channels':{name:{'quantiles':quantiles(arr[...,ch]),'mean':float(arr[...,ch].mean()),'standard_deviation':float(arr[...,ch].std())} for ch,name in enumerate(img.getbands())},
          'note':'Image-wide stats include atlas padding; channel values are untransformed 8-bit decoded bytes.'})
    with open(a.output,'x') as f:json.dump(report,f,indent=2)
    assert hashlib.sha256(Path(a.input).read_bytes()).hexdigest()==report['sha256']
    print(json.dumps({'input':a.input,'bounds':report['extents'],'welded_topology':report['exact_position_weld_topology'],'uv':report['uv']},indent=2))

if __name__=='__main__':main()
