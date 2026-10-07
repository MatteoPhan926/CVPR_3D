"""Reopen the saved GLB, sample its exported animation, render declared poses."""
from pathlib import Path
import bpy, math, json, hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/authored-inspection';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.render.fps=30
bpy.ops.import_scene.gltf(filepath=str(ROOT/'artifacts/car_authored.glb'))
pivot=bpy.data.objects['DoorPivot']
meshes=[o for o in scene.objects if o.type=='MESH']
def is_moving(o):
    while o:
        if o==pivot:return True
        o=o.parent
    return False
fixed=[o for o in meshes if not is_moving(o)]
moving=[o for o in meshes if is_moving(o)]
scene.frame_set(1);bpy.context.view_layer.update()
baseline={o.name:o.matrix_world.copy() for o in meshes}
closed_rotation=pivot.rotation_quaternion.copy() if pivot.rotation_mode=='QUATERNION' else pivot.rotation_euler.to_quaternion()
result={'input_sha256':hashlib.sha256((ROOT/'artifacts/car_authored.glb').read_bytes()).hexdigest(),'blender':bpy.app.version_string,'fps':30,'moving_meshes':[o.name for o in moving],'fixed_meshes':[o.name for o in fixed],'poses':[]}
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=False
scene.render.resolution_x=1440;scene.render.resolution_y=960;scene.render.resolution_percentage=100
scene.view_settings.view_transform='Standard'
scene.world=bpy.data.worlds.new('Neutral_inspection_world');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.65,.65,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.8
center=Vector((0,0,.04))
for location,power in [((2,3,4),50),((-3,-2,3),40),((1,0,-3),8)]:
    bpy.ops.object.light_add(type='AREA',location=location);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=2.5
    o.rotation_euler=(center-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();camera=bpy.context.object;scene.camera=camera;camera.data.type='ORTHO'
for label,frame,expected in [('closed',1,0),('intermediate',31,30),('open',61,60)]:
    scene.frame_set(frame);bpy.context.view_layer.update()
    q=pivot.rotation_quaternion.copy() if pivot.rotation_mode=='QUATERNION' else pivot.rotation_euler.to_quaternion()
    angle=math.degrees(closed_rotation.rotation_difference(q).angle)
    delta=max(abs(o.matrix_world[i][j]-baseline[o.name][i][j]) for o in fixed for i in range(4) for j in range(4))
    assert abs(angle-expected)<.01,(angle,expected)
    assert delta<1e-7,delta
    result['poses'].append({'name':label,'frame':frame,'expected_angle':expected,'actual_angle':angle,'fixed_transform_max_delta':delta})
    for view,location,target,scale in [('hero',(1.8,1.7,1.0),(0,0,.03),1.35),('side',(2,0,.08),(0,0,.08),1.12),('exposed',(1.7,.7,.55),(.1,-.10,.06),.70)]:
        camera.location=Vector(location);camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=scale
        scene.render.filepath=str(OUT/(label+'_'+view+'.png'));bpy.ops.render.render(write_still=True)
scene.frame_set(121);bpy.context.view_layer.update()
result['return_to_closed_max_matrix_delta']=max(abs(o.matrix_world[i][j]-baseline[o.name][i][j]) for o in meshes for i in range(4) for j in range(4))
assert result['return_to_closed_max_matrix_delta']<1e-7
result['status']='passed';result['scope']='Saved-animation angle, static body, reversible pose and render checks; not collision certification or appearance acceptance.'
(ROOT/'logs/authored-reopen-validation.json').write_text(json.dumps(result,indent=2)+'\n')
scene.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'reopened.blend'))
print(json.dumps(result,indent=2))
