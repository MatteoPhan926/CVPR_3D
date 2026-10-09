"""Native-material studio inspection; no geometry/material editing of imported asset."""
import bpy, sys, json, math, time, hashlib
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[1]
label=sys.argv[sys.argv.index('--')+1]
source=ROOT/'inputs'/({'A':'sample_2026-10-09T183055.354.glb','B':'sample_2026-10-09T183324.855.glb'}[label])
out=ROOT/'artifacts'/'raw_inspection'/label
out.mkdir(parents=True,exist_ok=False)
t=time.monotonic()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(source))
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
points=[o.matrix_world @ Vector(p) for o in objects for p in o.bound_box]
lo=Vector(tuple(min(p[k] for p in points) for k in range(3)))
hi=Vector(tuple(max(p[k] for p in points) for k in range(3)))
center=(lo+hi)/2; size=max(hi-lo)
scene=bpy.context.scene
scene.render.engine='CYCLES'; scene.cycles.samples=24
scene.cycles.use_denoising=True
scene.render.threads_mode='FIXED';scene.render.threads=3
scene.render.resolution_x=900;scene.render.resolution_y=600;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'
scene.world=bpy.data.worlds.new('Neutral studio');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.45,0.45,0.45,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.6
for name,offset,power,scale in [('Key',(-1,-1,2),180,1.5),('Fill',(1,-.5,1),90,1.2),('Rim',(0,1,1.8),160,1)]:
    data=bpy.data.lights.new(name,'AREA');data.energy=power*size*size;data.shape='DISK';data.size=scale*size
    obj=bpy.data.objects.new(name,data);scene.collection.objects.link(obj)
    obj.location=center+Vector(offset)*size
    obj.rotation_euler=(center-obj.location).to_track_quat('-Z','Y').to_euler()
camera=bpy.data.objects.new('Inspection camera',bpy.data.cameras.new('Inspection camera'));scene.collection.objects.link(camera)
scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=size*1.42
scene.render.image_settings.file_format='PNG'
views={}
for name,offset in [('q1',(1,-1,.65)),('q2',(-1,-1,.65)),('q3',(-1,1,.65)),('q4',(1,1,.65)),('side_pos_x',(1,0,.12))]:
    camera.location=center+Vector(offset)*size*2
    camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(name+'.png'))
    bpy.ops.render.render(write_still=True)
    views[name]={'offset':offset,'camera_matrix':[list(row) for row in camera.matrix_world]}
bpy.ops.wm.save_as_mainfile(filepath=str(out/'native_import.blend'))
record={'label':label,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'blender_version':bpy.app.version_string,'bounds':[list(lo),list(hi)],'center':list(center),'size':size,'vertices':sum(len(o.data.vertices) for o in objects),'polygons':sum(len(o.data.polygons) for o in objects),'views':views,'elapsed_seconds':time.monotonic()-t,'native_materials_untouched':True,'scope':'Standard studio presentation inspection; no generation fidelity metric or artist acceptance.'}
(out/'inspection.json').write_text(json.dumps(record,indent=2))
print('INSPECTION_COMPLETE '+json.dumps(record))
