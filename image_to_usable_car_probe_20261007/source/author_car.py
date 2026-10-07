"""Build a bounded door demonstration from cut_door.py output; Blender 4.3."""
from pathlib import Path
import bpy, numpy as np, json, math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
parts=np.load(ROOT/'artifacts/door_parts.npz')
cfg=json.loads((ROOT/'config/door-authoring.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene;scene.render.fps=30;scene.frame_start=1;scene.frame_end=121

def material(name,color=None,vertex=False):
    m=bpy.data.materials.new(name);m.use_nodes=True
    shader=m.node_tree.nodes.get('Principled BSDF');shader.inputs['Roughness'].default_value=.8
    if vertex:
        node=m.node_tree.nodes.new('ShaderNodeVertexColor');node.layer_name='Color'
        m.node_tree.links.new(node.outputs['Color'],shader.inputs['Base Color'])
    else:shader.inputs['Base Color'].default_value=(*color,1)
    return m
rawmat=material('Generated_vertex_colors_explicit_material',vertex=True)
rawshader=rawmat.node_tree.nodes.get('Principled BSDF')
rawshader.inputs['Metallic'].default_value=1
rawshader.inputs['Roughness'].default_value=1
lining=material('Added_dark_door_lining',(.018,.021,.023))
jambmat=material('Added_jamb_and_edge',(.025,.029,.031))
seatmat=material('Added_cabin_proxy',(.028,.023,.019))

def mesh_object(name,v,f,mat,colors=None):
    m=bpy.data.meshes.new(name);m.from_pydata(v.tolist(),[],f.tolist());m.update()
    o=bpy.data.objects.new(name,m);scene.collection.objects.link(o);m.materials.append(mat)
    if colors is not None:
        for poly in m.polygons:poly.use_smooth=True
        attr=m.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='POINT')
        attr.data.foreach_set('color',colors.astype(np.float32).ravel())
    return o

fixed=mesh_object('Body_fixed_generated_surface',parts['fixed_v'],parts['fixed_f'],rawmat,parts['fixed_c'])
dv,df=parts['door_v'],parts['door_f'];n=len(dv);edges=parts['boundary']
pivot=bpy.data.objects.new('DoorPivot',None);scene.collection.objects.link(pivot);pivot.location=cfg['pivot'];pivot.rotation_mode='XYZ'
def moving(obj):obj.parent=pivot;obj.location=-Vector(cfg['pivot'])
moving(mesh_object('Door_generated_outer_surface',dv,df,rawmat,parts['door_c']))
iv=dv.copy();iv[:,0]-=cfg['door_inward_thickness']
moving(mesh_object('Door_added_inner_lining',iv,df[:,::-1],lining))
edgeverts=np.concatenate([dv,iv]);edgefaces=[]
for i,j in edges:edgefaces.extend([[int(i),int(j),int(j+n)],[int(i),int(j+n),int(i+n)]])
moving(mesh_object('Door_added_edge_thickness',edgeverts,np.array(edgefaces),jambmat))
jv=dv.copy();jv[:,0]-=cfg['jamb_inward_depth']
mesh_object('Body_added_recessed_jamb',np.concatenate([dv,jv]),np.array(edgefaces)[:,::-1],jambmat)

def box(name,center,scale,mat):
    bpy.ops.mesh.primitive_cube_add(size=1,location=center);o=bpy.context.object;o.name=name;o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
    return o
# Explicitly authored local completion; no claim to a recovered vehicle interior.
box('Cabin_added_floor_proxy',(.09,-.10,-.043),(.22,.18,.010),lining)
box('Cabin_added_inner_wall_proxy',(-.02,-.10,.067),(.008,.18,.22),lining)
box('Cabin_added_seat_cushion_proxy',(.075,-.13,-.018),(.17,.075,.030),seatmat)
box('Cabin_added_seat_back_proxy',(.075,-.173,.045),(.17,.018,.15),seatmat)
for frame,angle in [(1,0),(61,60),(121,0)]:
    pivot.rotation_euler.z=-math.radians(angle);pivot.keyframe_insert('rotation_euler',frame=frame)
pivot.animation_data.action.name='DoorOpenClose_0_60'
for curve in pivot.animation_data.action.fcurves:
    for key in curve.keyframe_points:key.interpolation='LINEAR'
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'artifacts/car_authored.blend'))
bpy.ops.export_scene.gltf(filepath=str(ROOT/'artifacts/car_authored.glb'),export_format='GLB',export_animations=True,export_frame_range=True,export_force_sampling=True,export_materials='EXPORT',export_normals=True,export_yup=True)
print('SAVED',ROOT/'artifacts/car_authored.glb')
