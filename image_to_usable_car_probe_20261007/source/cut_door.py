"""One asset-specific convex cut. Preserve source triangles by exact partition.

No Bentley coordinates, masks or geometry are used. Frame and contour were
chosen from this generated car's inspected side view. No generator retry.
"""
from pathlib import Path
import json, hashlib
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
raw=ROOT/'raw/car_raw.glb'
scene=trimesh.load(raw,force='scene',process=False)
mesh=scene.dump(concatenate=True)
a=np.array([.8009595898216262,.5987184108349871,0.])
b=np.array([.5987184108349871,-.8009595898216262,0.])
R=np.array([b,a,[0,0,1.]])
v=np.asarray(mesh.vertices)@R.T
c=np.asarray(mesh.visual.vertex_colors,dtype=float)/255
f=np.asarray(mesh.faces)
# Counterclockwise in (longitudinal +Y, vertical +Z).
outline=np.array([[-.195,-.075],[.025,-.065],[.02,.145],[-.02,.242],[-.187,.253]])
planes=[]
for p,q in zip(outline,np.roll(outline,-1,axis=0)):
    d=q-p
    n=np.array([0.,-d[1],d[0]])
    planes.append((n,-np.dot(n,[0,*p])))
planes.append((np.array([1.,0.,0.]),-.10))
config={'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
 'frame':'+X camera-facing side, +Y front, +Z up; arbitrary generated units',
 'rotation_native_to_car':R.tolist(),'door_outline_yz':outline.tolist(),
 'near_side_min_x':.10,'pivot':[.255,-.19,.085],'axis_blender':[0,0,-1],
 'angle_range_degrees':[0,60], 'door_inward_thickness':.018,
 'jamb_inward_depth':.042,
 'selection_basis':'Approximate visible front cabin door, inferred from this raw mesh and input; contour not recovered as ground truth.',
 'completion':'Offset opaque inner door skin, cut-edge strips, recessed jamb strips and simple dark cabin/seat proxies. Generated windows remain opaque. No global shape or color repair.'}
(ROOT/'config/door-authoring.json').write_text(json.dumps(config,indent=2)+'\n')

def clip(poly,n,d,inside):
    out=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        dp=np.dot(p[:3],n)+d;dq=np.dot(q[:3],n)+d
        ip=dp>=-1e-12 if inside else dp<=1e-12
        iq=dq>=-1e-12 if inside else dq<=1e-12
        if ip:out.append(p)
        if ip != iq:
            out.append(p+(q-p)*(dp/(dp-dq)))
    return out

class Builder:
    def __init__(self):self.v=[];self.c=[];self.f=[];self.lookup={}
    def polygon(self,p):
        if len(p)<3:return
        ids=[]
        for row in p:
            key=tuple(np.round(row,10))
            if key not in self.lookup:
                self.lookup[key]=len(self.v);self.v.append(row[:3]);self.c.append(row[3:])
            ids.append(self.lookup[key])
        for i in range(1,len(ids)-1):
            face=[ids[0],ids[i],ids[i+1]]
            if len(set(face))==3:
                tri=np.array([self.v[j] for j in face])
                if np.linalg.norm(np.cross(tri[1]-tri[0],tri[2]-tri[0]))>1e-15:self.f.append(face)
    def arrays(self):return np.array(self.v),np.array(self.f),np.array(self.c)

fixed=Builder();door=Builder()
rows=np.concatenate([v,c],axis=1)
for face in f:
    poly=list(rows[face])
    for n,d in planes:
        distances=np.array([np.dot(p[:3],n)+d for p in poly])
        if (distances>=-1e-12).all():continue
        if (distances<=0).all():fixed.polygon(poly);poly=[];break
        fixed.polygon(clip(poly,n,d,False))
        poly=clip(poly,n,d,True)
        if len(poly)<3:break
    door.polygon(poly)
fv,ff,fc=fixed.arrays();dv,df,dc=door.arrays()
edge_counts={};edge_oriented={}
for face in df:
    for i,j in zip(face,np.roll(face,-1)):
        key=tuple(sorted([int(i),int(j)]));edge_counts[key]=edge_counts.get(key,0)+1;edge_oriented[key]=(int(i),int(j))
boundary=np.array([edge_oriented[k] for k,count in edge_counts.items() if count==1])
def area(vertices,faces):
    t=vertices[faces];return float(np.linalg.norm(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]),axis=1).sum()/2)
raw_area=area(v,f);fixed_area=area(fv,ff);door_area=area(dv,df)
assert len(df)>0 and len(ff)>0
assert abs(fixed_area+door_area-raw_area)/raw_area<1e-8
np.savez_compressed(ROOT/'artifacts/door_parts.npz',fixed_v=fv,fixed_f=ff,fixed_c=fc,door_v=dv,door_f=df,door_c=dc,boundary=boundary)
result={'raw_triangles':len(f),'fixed_triangles':len(ff),'door_triangles':len(df),'door_vertices':len(dv),'boundary_edges':len(boundary),'raw_area':raw_area,'fixed_area':fixed_area,'door_area':door_area,'area_partition_relative_error':abs(fixed_area+door_area-raw_area)/raw_area,'original_raw_hash_unchanged':hashlib.sha256(raw.read_bytes()).hexdigest()==config['raw_sha256'],'closed_source_surface_preserved':True,'note':'Partition area checks arithmetic preservation, not physical clearance or visual quality.'}
(ROOT/'logs/cut-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
