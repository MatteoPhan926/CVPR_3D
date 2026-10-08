"""Standard glTF appearance baselines, preserving POSITION/indices bytes."""
from pathlib import Path
import json,struct,copy,hashlib
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parent
OLD=Path('/workspace/image_to_usable_car_probe_20261007')
def read_glb(path):
    b=path.read_bytes();assert b[:4]==b'glTF'
    n,typ=struct.unpack_from('<II',b,12);assert typ==0x4e4f534a
    d=json.loads(b[20:20+n]);pos=20+n;length,typ=struct.unpack_from('<II',b,pos);assert typ==0x004e4942
    return d,bytearray(b[pos+8:pos+8+length])
def accessor(d,b,i):
    a=d['accessors'][i];view=d['bufferViews'][a['bufferView']]
    channels={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']]
    dtype={5121:np.uint8,5123:np.uint16,5125:np.uint32,5126:np.float32}[a['componentType']]
    offset=view.get('byteOffset',0)+a.get('byteOffset',0)
    x=np.frombuffer(b,dtype=dtype,count=a['count']*channels,offset=offset).reshape(-1,channels).copy()
    if a.get('normalized'):x=x.astype(np.float32)/np.iinfo(dtype).max
    return x
def append(d,b,x,kind):
    while len(b)%4:b.append(0)
    i=len(d['bufferViews']);d['bufferViews'].append({'buffer':0,'byteOffset':len(b),'byteLength':x.nbytes,'target':34962});b.extend(x.astype('<f4').tobytes())
    a=len(d['accessors']);d['accessors'].append({'bufferView':i,'componentType':5126,'count':len(x),'type':kind});return a
def write(path,d,b):
    d['buffers'][0]['byteLength']=len(b)
    j=json.dumps(d,separators=(',',':')).encode();j+=b' '*((-len(j))%4);b+=b'\0'*((-len(b))%4)
    path.write_bytes(struct.pack('<III',0x46546c67,2,12+8+len(j)+8+len(b))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(b),0x004e4942)+b)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
sources={'car':OLD/'raw/car_raw.glb',**{k:ROOT/'holdouts'/k/'raw.glb' for k in ['teapot','hamburger']}}
report={}
for case,path in sources.items():
    out=ROOT/'exports'/case;out.mkdir(parents=True,exist_ok=True)
    d,b=read_glb(path);p=d['meshes'][0]['primitives'][0]
    colors=accessor(d,b,p['attributes']['COLOR_0']).astype(np.float32)
    linear=colors.copy();rgb=linear[:,:3];linear[:,:3]=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
    (out/'raw.glb').write_bytes(path.read_bytes())
    report[case]={'raw_sha256':digest(path),'variants':{}}
    for name,convert,unlit in [('unlit_direct',False,True),('unlit_corrected',True,True),('pbr_corrected',True,False)]:
        dd=copy.deepcopy(d);bb=bytearray(b);pp=dd['meshes'][0]['primitives'][0]
        pp['attributes']['COLOR_0']=append(dd,bb,linear if convert else colors,'VEC4')
        material={'name':name,'doubleSided':False,'pbrMetallicRoughness':{'baseColorFactor':[1,1,1,1],'metallicFactor':0,'roughnessFactor':1}}
        if unlit:material['extensions']={'KHR_materials_unlit':{}};dd['extensionsUsed']=['KHR_materials_unlit']
        else:
            mesh=trimesh.load(path,force='mesh',process=False)
            pp['attributes']['NORMAL']=append(dd,bb,np.asarray(mesh.vertex_normals,dtype=np.float32),'VEC3')
        dd['materials']=[material];pp['material']=0
        dest=out/(name+'.glb');write(dest,dd,bb)
        od,ob=read_glb(dest);op=od['meshes'][0]['primitives'][0]
        assert np.array_equal(accessor(d,b,p['attributes']['POSITION']),accessor(od,ob,op['attributes']['POSITION']))
        assert np.array_equal(accessor(d,b,p['indices']),accessor(od,ob,op['indices']))
        report[case]['variants'][name]={'sha256':digest(dest),'positions_exact':True,'indices_exact':True,'unlit':unlit,'inverse_srgb':convert,'added_smooth_normals':not unlit,'double_sided':False}
(ROOT/'exports/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
