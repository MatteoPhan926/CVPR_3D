import bpy, numpy as np, json, sys, time
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'artifacts'/'reopened_A_v1';out.mkdir(exist_ok=False)
asset=ROOT/'artifacts/authoring_A_v1/car_door_authored.glb'
# Load the exact inspection studio, then remove all imported geometry before GLB import.
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'artifacts/raw_inspection/A_v2/native_import.blend'))
s=bpy.context.scene;s.render.fps=30;s.render.threads=3
for obj in list(s.objects):
 if obj.type not in {'LIGHT','CAMERA'}:bpy.data.objects.remove(obj,do_unlink=True)
bpy.ops.import_scene.gltf(filepath=str(asset))
hinge=bpy.data.objects.get('FrontDoor_Control');assert hinge
body=bpy.data.objects.get('Generated exterior - fixed');assert body
door=bpy.data.objects.get('Generated front door - native UV PBR');assert door
actions=[{'name':a.name,'frame_range':list(a.frame_range),'fcurves':len(a.fcurves)} for a in bpy.data.actions]
assert actions,'No animation after reimport'
action=hinge.animation_data.action if hinge.animation_data else None
assert action,'Hinge has no animation action after GLB reimport'
start,end=action.frame_range;assert abs((end-start)/s.render.fps-4)<1e-4
records=[];body_ref=None;hinge_mats=[]
for i in range(121):
 s.frame_set(round(start+i));bpy.context.view_layer.update()
 b=np.array(body.matrix_world);h=np.array(hinge.matrix_world);d=np.array(door.matrix_world)
 if body_ref is None:body_ref=b.copy()
 assert np.max(np.abs(b-body_ref))<1e-7
 hinge_mats.append(h)
 records.append({'seconds':i/30,'frame':int(start+i),'hinge_matrix':h.tolist(),'door_matrix':d.tolist()})
reverse=max(float(np.max(np.abs(hinge_mats[i]-hinge_mats[120-i]))) for i in range(61))
assert reverse<2e-6,reverse
rotation_delta=[]
for i in [0,30,60,90,120]:
 r=Matrix(hinge_mats[i][:3,:3].tolist());q=r.to_quaternion()
 r0=Matrix(hinge_mats[0][:3,:3].tolist()).to_quaternion()
 rotation_delta.append(float(q.rotation_difference(r0).angle*180/np.pi))
assert max(abs(a-b) for a,b in zip(rotation_delta,[0,30,60,30,0]))<.001,rotation_delta
mesh_info=[]
for obj in s.objects:
 if obj.type=='MESH':mesh_info.append({'name':obj.name,'faces':len(obj.data.polygons),'uv_layers':[l.name for l in obj.data.uv_layers],'parent':obj.parent.name if obj.parent else None,'material_names':[m.name for m in obj.data.materials]})
assert door.parent==hinge
moving=[o.name for o in s.objects if o.parent==hinge]
assert len(moving)==3,moving
record={'status':'reimport_motion_pass','input':str(asset.relative_to(ROOT)),'actions':actions,'duration_seconds':4,'frame_count_checked':121,'angle_at_0_1_2_3_4_sec':rotation_delta,'max_forward_reverse_matrix_error':reverse,'fixed_body_matrix_max_error':0,'moving_children':moving,'meshes':mesh_info,'trajectory':records,'limits':'Tests exported motion and transforms; not collision certification, semantic glass existence, visual quality or human usability.'}
(out/'motion_verification.json').write_text(json.dumps(record,indent=2))
s.render.resolution_x=1440;s.render.resolution_y=960;s.cycles.samples=32
def render(name,seconds,offset,target=(.000474,-.003251,-.000433),scale=1.42,exposure=0):
 s.frame_set(round(start+seconds*30));c=Vector(target);cam=s.camera;cam.data.type='ORTHO';cam.data.ortho_scale=scale
 cam.location=c+Vector(offset)*2;cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler()
 s.view_settings.exposure=exposure;s.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
for sec,angle in [(0,0),(1,30),(2,60)]:
 render(f'hero_{angle:02d}',sec,(1,-1,.4))
 render(f'side_{angle:02d}',sec,(0,-1,.12))
render('edge_cabin_60',2,(.6,-1,.6),(.015,-.16,.015),.50)
render('hero_60_exposure_minus1p5',2,(1,-1,.4),exposure=-1.5)
s.frame_set(round(start));s.view_settings.exposure=0
bpy.ops.wm.save_as_mainfile(filepath=str(out/'export_reopened.blend'))
print('REOPENED_VERIFIED',json.dumps({k:v for k,v in record.items() if k!='trajectory'}))
