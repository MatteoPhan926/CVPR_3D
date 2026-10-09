"""Conventional convex-prism cut, carrying native UVs and corner normals.

No model inference or mesh replacement. All additions are labelled in the scene.
"""
import bpy, numpy as np, sys, json, time, math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'artifacts'/'authoring_A_v1'
out.mkdir(parents=True,exist_ok=False)
started=time.monotonic()
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'artifacts/raw_inspection/A_v2/native_import.blend'))
scene=bpy.context.scene;scene.render.threads=3
obj=next(o for o in scene.objects if o.type=='MESH');mesh=obj.data
assert all(len(p.vertices)==3 for p in mesh.polygons)
positions=np.array([obj.matrix_world@v.co for v in mesh.vertices],dtype=np.float64)
indices=np.array([p.vertices[:] for p in mesh.polygons],dtype=np.int32)
uv=np.array([v.uv[:] for v in mesh.uv_layers.active.data],dtype=np.float64).reshape(-1,3,2)
normals=np.array([n.vector[:] for n in mesh.corner_normals],dtype=np.float64).reshape(-1,3,3)
corners=np.concatenate([positions[indices],uv,normals],axis=2)
material=obj.active_material
cfg=json.loads((ROOT/'config/door_A.json').read_text())
polygon=np.array(cfg['polygon_xz'],dtype=float)
planes=[]
for p,q in zip(polygon,np.roll(polygon,-1,axis=0)):
    d=q-p;n=np.array([-d[1],0,d[0]]);n/=np.linalg.norm(n)
    planes.append((n,float(n@np.array([p[0],0,p[1]]))))
planes.append((np.array([0.,-1,0]),-cfg['side_y_max']))
def area(tris):
    return float(np.linalg.norm(np.cross(tris[:,1,:3]-tris[:,0,:3],tris[:,2,:3]-tris[:,0,:3]),axis=1).sum()/2)
distance=np.stack([corners[:,:,:3]@n-c for n,c in planes],axis=2)
fully_inside=(distance>=-1e-10).all(axis=(1,2))
fully_outside=(distance < -1e-10).all(axis=1).any(axis=1)
boundary=np.where(~fully_inside & ~fully_outside)[0]
inside=[*corners[fully_inside]];outside=[*corners[fully_outside]]
inside_source=[*np.where(fully_inside)[0]];outside_source=[*np.where(fully_outside)[0]]
def triangulate(poly,dest,sources,index):
    for j in range(1,len(poly)-1):
        tri=np.array([poly[0],poly[j],poly[j+1]])
        if np.linalg.norm(np.cross(tri[1,:3]-tri[0,:3],tri[2,:3]-tri[0,:3]))>1e-15:
            dest.append(tri);sources.append(index)
def split(poly,n,c):
    a=[];b=[]
    for s,e in zip(poly,np.roll(poly,-1,axis=0)):
        ds=float(s[:3]@n-c);de=float(e[:3]@n-c)
        sin=ds>=0;ein=de>=0
        (a if sin else b).append(s)
        if sin != ein:
            v=s+(e-s)*(ds/(ds-de));a.append(v);b.append(v)
    return a,b
for idx in boundary:
    poly=corners[idx]
    for n,c in planes:
        if len(poly)<3:break
        poly,reject=split(np.array(poly),n,c)
        if len(reject)>=3:triangulate(reject,outside,outside_source,int(idx))
    if len(poly)>=3:triangulate(poly,inside,inside_source,int(idx))
door=np.array(inside);fixed=np.array(outside)
assert abs(area(door)+area(fixed)-area(corners))<1e-7
np.savez_compressed(out/'cut_arrays.npz',door=door,fixed=fixed,door_source=np.array(inside_source),fixed_source=np.array(outside_source))
def surface(name,data,mat,custom=True):
    # Deduplicate complete corner tuples, preserving UV and shading seams.
    flat=data.reshape(-1,8)
    vertices,inv=np.unique(flat,axis=0,return_inverse=True)
    m=bpy.data.meshes.new(name);m.from_pydata(vertices[:,:3].tolist(),[],inv.reshape(-1,3).tolist());m.update()
    o=bpy.data.objects.new(name,m);scene.collection.objects.link(o);m.materials.append(mat)
    layer=m.uv_layers.new(name='UVMap');layer.data.foreach_set('uv',flat[:,3:5].astype(np.float32).ravel())
    for p in m.polygons:p.use_smooth=True
    if custom:
        ns=flat[:,5:8];ns=ns/np.maximum(np.linalg.norm(ns,axis=1,keepdims=True),1e-15)
        m.normals_split_custom_set(ns.tolist())
    return o
body=surface('Generated exterior - fixed',fixed,material)
panel=surface('Generated front door - native UV PBR',door,material)
bpy.data.objects.remove(obj,do_unlink=True)
if mesh.users==0:bpy.data.meshes.remove(mesh)
hinge=bpy.data.objects.new('FrontDoor_Control',None);scene.collection.objects.link(hinge)
hinge.location=cfg['hinge_xyz'];hinge.empty_display_type='ARROWS';hinge.empty_display_size=.07
def parent_keep(o,p):
    matrix=o.matrix_world.copy();o.parent=p;o.matrix_world=matrix
parent_keep(panel,hinge)
hinge['open_degrees']=0.;hinge.id_properties_ui('open_degrees').update(min=0,max=60,description='Front door opening; 0 closed, 60 fully open. Slider evaluated in Blender.')
driver=hinge.driver_add('rotation_euler',2).driver;driver.type='SCRIPTED'
var=driver.variables.new();var.name='angle';var.type='SINGLE_PROP';var.targets[0].id=hinge;var.targets[0].data_path='["open_degrees"]'
driver.expression='-angle * 0.017453292519943295'
def pose(deg):
    hinge['open_degrees']=float(deg);hinge.update_tag();bpy.context.view_layer.update()
def camera(offset,target=None,scale=1.42):
    center=Vector((.000474,-.003251,-.000433)) if target is None else Vector(target)
    cam=scene.camera;cam.data.type='ORTHO';cam.data.ortho_scale=scale
    cam.location=center+Vector(offset)*2
    cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
def render(name,offset=(1,-1,.4),target=None,scale=1.42):
    camera(offset,target,scale);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
pose(0)
scene.render.resolution_x=1440;scene.render.resolution_y=960;scene.cycles.samples=32
render('partition_only_closed')
bpy.ops.wm.save_as_mainfile(filepath=str(out/'partition_only.blend'))
pose(60);render('partition_only_open60')
pose(0)
def plain(name,color,roughness=.65):
    mat=bpy.data.materials.new(name);mat.use_nodes=True
    node=mat.node_tree.nodes['Principled BSDF'];node.inputs['Base Color'].default_value=(*color,1);node.inputs['Roughness'].default_value=roughness
    return mat
liningmat=plain('ADDED dark door lining',(.023,.019,.016))
edgemat=plain('ADDED dark painted cut edges',(.012,.018,.021),.45)
interiormat=plain('ADDED plausible interior upholstery',(.032,.025,.021))
# Back of selected source surface, translated inward; fixed UV/PBR exterior untouched.
lining=door.copy();lining[:,:,:3]+=np.array([0,.006,0]);lining=lining[:,[0,2,1],:];lining[:,:,5:8]*=-1
liner=surface('ADDED door inner lining',lining,liningmat);parent_keep(liner,hinge)
# Geometrically shared edge accounting ignores native UV seams.
xyz=door[:,:,:3].reshape(-1,3)
keys=np.round(xyz,7)
unique,vi=np.unique(keys,axis=0,return_inverse=True)
face=vi.reshape(-1,3);edges=np.concatenate([face[:,[0,1]],face[:,[1,2]],face[:,[2,0]]])
sortededges=np.sort(edges,axis=1);_,ei,counts=np.unique(sortededges,axis=0,return_index=True,return_counts=True)
boundary_edges=edges[ei[counts==1]]
def strips(name,edgepairs,offset,mat):
    verts=[];faces=[]
    for ia,ib in edgepairs:
        a=unique[ia];b=unique[ib];i=len(verts);verts.extend([a,b,b+offset,a+offset]);faces.append((i,i+1,i+2,i+3))
    m=bpy.data.meshes.new(name);m.from_pydata(verts,[],faces);m.materials.append(mat);m.update()
    o=bpy.data.objects.new(name,m);scene.collection.objects.link(o);return o
edge=strips('ADDED door edge thickness',boundary_edges,np.array([0,.006,0]),edgemat);parent_keep(edge,hinge)
jamb=strips('ADDED fixed aperture jamb',boundary_edges,np.array([0,.022,0]),edgemat)
def box(name,location,scale,mat,bevel=.003):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location);o=bpy.context.object;o.name=name;o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
    mod=o.modifiers.new('Conventional bevel','BEVEL');mod.width=bevel;mod.segments=3
    bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
    return o
box('ADDED plausible cabin floor',(-.055,0,-.112),(.34,.25,.013),interiormat)
box('ADDED plausible seat cushion',(-.016,-.035,-.062),(.12,.20,.029),interiormat)
box('ADDED plausible seat back',(-.082,-.035,-.014),(.032,.20,.115),interiormat)
box('ADDED plausible dashboard',(.115,0,.030),(.040,.24,.035),edgemat)
for deg in [0,30,60]:
    pose(deg);render(f'hero_{deg:02d}');render(f'side_{deg:02d}',(0,-1,.12))
pose(60);render('edge_cabin_60',(.6,-1,.6),(.015,-.16,.015),.50)
pose(0)
# Blend slider + a four-second 30fps open/close clip. Export baking handles the driver.
for frame,angle in [(1,0),(61,60),(121,0)]:
    hinge['open_degrees']=float(angle);hinge.keyframe_insert(data_path='["open_degrees"]',frame=frame)
for fcurve in hinge.animation_data.action.fcurves:
    for point in fcurve.keyframe_points:point.interpolation='LINEAR'
scene.frame_start=1;scene.frame_end=121;scene.render.fps=30;scene.frame_set(1)
scene['Usage']='Select FrontDoor_Control. Custom property open_degrees is a 0-60 slider. Clear/mute its animation to pose manually. Frame1/61/121 is closed/open/closed.'
for image in bpy.data.images:
    if image.has_data and image.source!='GENERATED':image.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(out/'car_door_authored.blend'))
# Export only mesh/control objects; omit diagnostic cameras and lights.
bpy.ops.object.select_all(action='DESELECT')
for o in scene.objects:
    if o.type=='MESH' or o==hinge:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(out/'car_door_authored.glb'),export_format='GLB',use_selection=True,export_animations=True,export_force_sampling=True,export_frame_range=True,export_image_format='AUTO',export_extras=True)
record={'status':'authored_exported','source':'A','config':cfg,'elapsed_seconds':time.monotonic()-started,'original_triangles':len(corners),'fully_inside_source_triangles':int(fully_inside.sum()),'fully_outside_source_triangles':int(fully_outside.sum()),'boundary_candidate_triangles':len(boundary),'door_triangles':len(door),'fixed_triangles':len(fixed),'original_area':area(corners),'partition_area':area(door)+area(fixed),'door_area':area(door),'boundary_edges':len(boundary_edges),'material_policy':'Native exterior material and textures unchanged. New lining, edges, jamb, floor, seats and dashboard use labelled simple materials. No source exterior repaint/remesh/replacement.','limits':'Hand-authored polygon and proxy interior; no claim of artist labor, watertightness, recovered hidden geometry, or physical collision certification. Export playback and views require independent verification.'}
(out/'authoring.json').write_text(json.dumps(record,indent=2))
print('AUTHORING_COMPLETE '+json.dumps(record))
