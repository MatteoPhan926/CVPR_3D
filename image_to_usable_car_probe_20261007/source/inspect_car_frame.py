"""Inspect a display-normalized car frame: +X near side, +Y front, +Z up."""
import bpy, math, json
from mathutils import Matrix,Vector
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/car-frame';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'artifacts/raw-color-inspection/inspection.blend'))
angle=math.atan2(.8009595898216262,.5987184108349871)
R=Matrix.Rotation(angle,4,'Z')
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
roots=set()
for o in objects:
    while o.parent is not None:o=o.parent
    roots.add(o)
for o in roots:o.matrix_world=R@o.matrix_world
bpy.context.view_layer.update()
points=[o.matrix_world@Vector(c) for o in objects for c in o.bound_box]
lo=Vector([min(p[i] for p in points) for i in range(3)]);hi=Vector([max(p[i] for p in points) for i in range(3)])
scene=bpy.context.scene;camera=scene.camera
scene.render.resolution_x=1200;scene.render.resolution_y=800;scene.cycles.samples=16
center=(lo+hi)/2
camera.data.ortho_scale=1.12
for name,location,target in [('near_side',(2,0,.08),(0,0,.08)),('near_hero',(1.8,1.7,1.0),(0,0,.03)),('front',(0,2,.08),(0,0,.08)),('near_door',(2,-.12,.13),(0,-.12,.13))]:
    camera.location=Vector(location);camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.ortho_scale=.6 if name=='near_door' else (1.35 if name=='near_hero' else 1.12)
    scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
inventory={'frame':'display-only rotation to +X camera-facing side,+Y front,+Z up','rotation_z_degrees':math.degrees(angle),'source_front_native':[.8009595898216262,.5987184108349871,0],'source_near_native':[.5987184108349871,-.8009595898216262,0],'bounds':[list(lo),list(hi)]}
(OUT/'frame.json').write_text(json.dumps(inventory,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'car_frame.blend'))
print(json.dumps(inventory,indent=2))
