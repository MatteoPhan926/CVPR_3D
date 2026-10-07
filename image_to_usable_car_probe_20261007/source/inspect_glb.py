"""Blender reimport, actual geometry inventory, and six bounded orthographic views."""
import bpy
from mathutils import Vector, Matrix
from pathlib import Path
import argparse
import json
import math
import sys

parser=argparse.ArgumentParser()
parser.add_argument('--input',required=True)
parser.add_argument('--output',required=True)
parser.add_argument('--samples',type=int,default=12)
parser.add_argument('--native-z-up',action='store_true')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:])
out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(Path(args.input).resolve()))
if args.native_z_up:
    rotation=Matrix.Rotation(-math.pi/2,4,'X')
    for obj in list(bpy.context.scene.objects):
        if obj.parent is None:obj.matrix_world=rotation@obj.matrix_world
    bpy.context.view_layer.update()
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
for obj in objects:
    if not obj.data.materials and obj.data.color_attributes:
        # Blender's importer leaves material-less COLOR_0 meshes unshaded.
        # Display the stored color attribute without changing the source GLB.
        material=bpy.data.materials.new('RawVertexColorDisplay');material.use_nodes=True
        shader=material.node_tree.nodes.get('Principled BSDF')
        attribute=material.node_tree.nodes.new('ShaderNodeVertexColor');attribute.layer_name=obj.data.color_attributes[0].name
        material.node_tree.links.new(attribute.outputs['Color'],shader.inputs['Base Color'])
        shader.inputs['Roughness'].default_value=.8
        obj.data.materials.append(material)
points=[o.matrix_world@Vector(corner) for o in objects for corner in o.bound_box]
lo=Vector([min(p[i] for p in points) for i in range(3)])
hi=Vector([max(p[i] for p in points) for i in range(3)])
center=(lo+hi)/2;size=max(hi-lo)
inventory={'input':str(Path(args.input).resolve()),'blender_version':bpy.app.version_string,'native_z_up_display_rotation':args.native_z_up,'bounds_blender':[list(lo),list(hi)],'objects':[{'name':o.name,'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'materials':[m.name for m in o.data.materials],'color_attributes':[a.name for a in o.data.color_attributes]} for o in objects]}
(out/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=args.samples;scene.cycles.use_denoising=False
scene.render.resolution_x=640;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.view_settings.view_transform='Standard'
scene.world=bpy.data.worlds.new('InspectionWorld');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.65,.65,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.8
for direction,power in [((2,-3,4),35),((-3,2,3),25),((0,0,-3),10)]:
    bpy.ops.object.light_add(type='AREA',location=center+Vector(direction).normalized()*size*2)
    light=bpy.context.object;light.data.energy=power*size*size;light.data.shape='DISK';light.data.size=size*2
    light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();camera=bpy.context.object;scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=size*1.2
for name,direction in [('x_pos',(1,0,.03)),('x_neg',(-1,0,.03)),('y_pos',(0,1,.03)),('y_neg',(0,-1,.03)),('z_pos',(.03,0,1)),('z_neg',(.03,0,-1))]:
    camera.location=center+Vector(direction).normalized()*size*3
    camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'inspection.blend'))
print(json.dumps(inventory,indent=2))
