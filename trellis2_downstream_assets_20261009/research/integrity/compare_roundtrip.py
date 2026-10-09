"""Compare each original with an unmodified Blender GLB export, without rewriting either."""
import argparse,hashlib,io,json
from pathlib import Path
import numpy as np
from PIL import Image
from geometry_diagnostics import read_glb,accessor,quantiles

p=argparse.ArgumentParser();p.add_argument('original');p.add_argument('export');p.add_argument('output');a=p.parse_args()
ra,da,ba=read_glb(a.original);rb,db,bb=read_glb(a.export)
pa=da['meshes'][0]['primitives'][0];pb=db['meshes'][0]['primitives'][0]
fa=accessor(da,ba,pa['indices']).reshape(-1,3);fb=accessor(db,bb,pb['indices']).reshape(-1,3)
assert fa.shape==fb.shape
attrs={}
for key in ['POSITION','TEXCOORD_0','NORMAL']:
    xa=accessor(da,ba,pa['attributes'][key])[fa].astype(np.float64)
    xb=accessor(db,bb,pb['attributes'][key])[fb].astype(np.float64)
    attrs[key]={'all_face_corners_exactly_equal':bool(np.array_equal(xa,xb)),
      'max_absolute_component_difference':float(np.abs(xa-xb).max()),
      'face_corners_any_component_changed':int(np.sum(np.any(xa!=xb,axis=-1))),
      'original_face_corner_sha256':hashlib.sha256(xa.tobytes()).hexdigest(),
      'export_face_corner_sha256':hashlib.sha256(xb.tobytes()).hexdigest()}
    if key=='POSITION':
        areas=np.linalg.norm(np.cross(xa[:,1]-xa[:,0],xa[:,2]-xa[:,0]),axis=1)/2
        positions=xa
    elif key=='NORMAL':
        ua=xa/np.linalg.norm(xa,axis=-1,keepdims=True);ub=xb/np.linalg.norm(xb,axis=-1,keepdims=True)
        angles=np.degrees(np.arccos(np.clip(np.sum(ua*ub,axis=-1),-1,1)))
        attrs[key]['angle_degrees_quantiles']=quantiles(angles)
        attrs[key]['angle_thresholds']={str(t):{'corners':int(np.sum(angles>t)),
          'faces_any_corner':int(np.sum(np.any(angles>t,axis=1))),
          'fraction_total_geometric_area_faces_any_corner':float(areas[np.any(angles>t,axis=1)].sum()/areas.sum())}
          for t in [0.01,0.1,1,5,10,30]}
        worst=np.unravel_index(np.argmax(angles),angles.shape)
        attrs[key]['maximum_angle_corner']={'face_index':int(worst[0]),'corner_index':int(worst[1]),
          'position':positions[worst].tolist(),'source_normal':xa[worst].tolist(),'export_normal':xb[worst].tolist(),
          'face_area':float(areas[worst[0]])}
textures=[]
for i in range(len(da['images'])):
    def decode(doc,binary):
        im=doc['images'][i];view=doc['bufferViews'][im['bufferView']];off=view.get('byteOffset',0)
        raw=binary[off:off+view['byteLength']];image=Image.open(io.BytesIO(raw));arr=np.asarray(image.convert('RGBA'))
        return raw,arr,im,image
    ea,ia,ma,ima=decode(da,ba);eb,ib,mb,imb=decode(db,bb)
    textures.append({'image_index':i,'original_mime':ma['mimeType'],'export_mime':mb['mimeType'],
      'original_mode':ima.mode,'export_mode':imb.mode,'encoded_bytes_identical':ea==eb,
      'decoded_rgba_pixels_identical':bool(np.array_equal(ia,ib)),
      'original_encoded_sha256':hashlib.sha256(ea).hexdigest(),'export_encoded_sha256':hashlib.sha256(eb).hexdigest(),
      'max_decoded_pixel_component_difference':int(np.abs(ia.astype(np.int16)-ib.astype(np.int16)).max())})
def effective_material(doc):
    m=doc['materials'][0];r=m.get('pbrMetallicRoughness',{})
    return {'baseColorFactor':r.get('baseColorFactor',[1,1,1,1]),'metallicFactor':r.get('metallicFactor',1),
      'roughnessFactor':r.get('roughnessFactor',1),'alphaMode':m.get('alphaMode','OPAQUE'),
      'doubleSided':m.get('doubleSided',False),'baseColorTexture':r.get('baseColorTexture'),
      'metallicRoughnessTexture':r.get('metallicRoughnessTexture')}
report={'original':a.original,'export':a.export,'original_sha256':hashlib.sha256(ra).hexdigest(),'export_sha256':hashlib.sha256(rb).hexdigest(),
 'triangle_count_original':len(fa),'triangle_count_export':len(fb),
 'vertex_count_original':da['accessors'][pa['attributes']['POSITION']]['count'],
 'vertex_count_export':db['accessors'][pb['attributes']['POSITION']]['count'],
 'direct_ordered_oriented_triangle_positions_identical':attrs['POSITION']['all_face_corners_exactly_equal'],
 'oriented_triangle_position_multiset_identical':attrs['POSITION']['all_face_corners_exactly_equal'],
 'comparison_method':'Expand indexed attributes to ordered face corners. Identical ordered positions are a stronger result than multiset equality; no tolerance, nearest match, or welding used.',
 'attribute_comparison':attrs,'texture_comparison':textures,
 'effective_material_values_identical':effective_material(da)==effective_material(db),
 'effective_material_original':effective_material(da),'effective_material_export':effective_material(db),
 'extensions_required_original':da.get('extensionsRequired',[]),'extensions_required_export':db.get('extensionsRequired',[]),
 'scope':'Same input and unmodified Blender export control. Establishes recorded preservation/drift only; no visual equivalence, semantic authoring success, or generation provenance inferred.'}
with open(a.output,'x') as f:json.dump(report,f,indent=2)
assert hashlib.sha256(Path(a.original).read_bytes()).hexdigest()==report['original_sha256']
print(json.dumps(report,indent=2))
