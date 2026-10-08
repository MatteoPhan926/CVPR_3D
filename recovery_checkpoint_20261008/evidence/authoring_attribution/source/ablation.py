"""One-pass diagnostic renders of existing source; no saved source edits.

Run: blender -b -t 2 --python source/ablation.py
All factors and views are fixed before rendering. This is not aesthetic tuning.
"""
from pathlib import Path
import bpy, json, hashlib, math, numpy as np
from mathutils import Vector, Matrix

OUT=Path(__file__).resolve().parents[1]
ROOT=Path('/workspace/image_to_usable_car_probe_20261007')
cfg=json.loads((ROOT/'config/door-authoring.json').read_text())
raw_path=ROOT/'raw/car_raw.glb'
raw_hash=hashlib.sha256(raw_path.read_bytes()).hexdigest()
assert raw_hash==cfg['raw_sha256']
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.render.fps=30
bpy.ops.import_scene.gltf(filepath=str(raw_path))
raw=[o for o in scene.objects if o.type=='MESH']
assert len(raw)==1
raw=raw[0]
R=Matrix(cfg['rotation_native_to_car']).to_4x4()
raw.data.transform(R @ Matrix.Rotation(-math.pi/2,4,'X') @ raw.matrix_world)
raw.parent=None
raw.matrix_world=Matrix.Identity(4)
raw.name='RAW_CANONICAL'
inventory={'raw_sha256_before':raw_hash,'blender_version':bpy.app.version_string,
 'raw_import':{'vertices':len(raw.data.vertices),'triangles':len(raw.data.polygons),
 'smooth_polygons':sum(p.use_smooth for p in raw.data.polygons),'materials':list(raw.data.materials.keys()),
 'color_attributes':[(a.name,a.domain,a.data_type) for a in raw.data.color_attributes],
 'custom_normals':raw.data.has_custom_normals}}

def vcolmat(name,metal=1.,rough=1.,single=False):
    mat=bpy.data.materials.new(name);mat.use_nodes=True
    nodes=mat.node_tree.nodes;links=mat.node_tree.links
    bsdf=nodes.get('Principled BSDF')
    bsdf.inputs['Metallic'].default_value=metal
    bsdf.inputs['Roughness'].default_value=rough
    color=nodes.new('ShaderNodeVertexColor');color.layer_name='Color'
    links.new(color.outputs['Color'],bsdf.inputs['Base Color'])
    if single:
        # Cycles ignores viewport backface culling. Explicitly remove backfaces.
        geom=nodes.new('ShaderNodeNewGeometry');mix=nodes.new('ShaderNodeMixShader')
        trans=nodes.new('ShaderNodeBsdfTransparent')
        links.new(geom.outputs['Backfacing'],mix.inputs[0]);links.new(bsdf.outputs[0],mix.inputs[1])
        links.new(trans.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],nodes.get('Material Output').inputs['Surface'])
    return mat

raw_double=vcolmat('Raw_glTF_PBR_defaults_double')
raw_single=vcolmat('Raw_glTF_PBR_defaults_single',single=True)
raw_historical=vcolmat('Prior_raw_inspection_material',0.,.8)
raw.data.materials.clear();raw.data.materials.append(raw_double)
before=set(scene.objects)
bpy.ops.import_scene.gltf(filepath=str(ROOT/'artifacts/car_authored.glb'))
auth=[o for o in scene.objects if o not in before and o.type=='MESH']
generated=[o for o in auth if o.name in ['Body_fixed_generated_surface','Door_generated_outer_surface']]
additions=[o for o in auth if o not in generated]
pivot=bpy.data.objects['DoorPivot']
outer=bpy.data.objects['Door_generated_outer_surface']
fixed=bpy.data.objects['Body_fixed_generated_surface']
scene.frame_set(1);bpy.context.view_layer.update()
original_smooth={o.name:[p.use_smooth for p in o.data.polygons] for o in generated}
inventory['authored_import']=[{'name':o.name,'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),
 'smooth_polygons':sum(p.use_smooth for p in o.data.polygons),'custom_normals':o.data.has_custom_normals,
 'parent':o.parent.name if o.parent else None,'materials':list(o.data.materials.keys())} for o in auth]
inventory['authored_materials']={}
for mat in {m for o in auth for m in o.data.materials}:
    bsdf=mat.node_tree.nodes.get('Principled BSDF')
    inventory['authored_materials'][mat.name]={'metallic':bsdf.inputs['Metallic'].default_value,
      'roughness':bsdf.inputs['Roughness'].default_value,'use_backface_culling':mat.use_backface_culling}

def mesh_arrays(obj):
    v=np.array([obj.matrix_world@p.co for p in obj.data.vertices],float)
    faces=np.array([p.vertices[:] for p in obj.data.polygons],int)
    return v,faces

def mesh_area(v,f):
    tri=v[f];return float(np.linalg.norm(np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]),axis=1).sum()/2)

rv,rf=mesh_arrays(raw);fv,ff=mesh_arrays(fixed);dv,df=mesh_arrays(outer)
inventory['geometry']={'raw_area':mesh_area(rv,rf),'fixed_area':mesh_area(fv,ff),'moving_generated_area':mesh_area(dv,df),
 'raw_bounds':[rv.min(0).tolist(),rv.max(0).tolist()],
 'moving_generated_bounds':[dv.min(0).tolist(),dv.max(0).tolist()],
 'door_fraction_source_area':mesh_area(dv,df)/mesh_area(rv,rf),
 'closed_area_relative_error':abs(mesh_area(fv,ff)+mesh_area(dv,df)-mesh_area(rv,rf))/mesh_area(rv,rf)}
# Uniform vertex correspondences expose any accidental color-space change.
def point_colors(obj):
    attr=obj.data.color_attributes[0]
    if attr.domain=='POINT':return np.array([x.color[:] for x in attr.data])
    result=np.zeros((len(obj.data.vertices),4));count=np.zeros(len(result))
    for loop,x in zip(obj.data.loops,attr.data):result[loop.vertex_index]+=np.array(x.color[:]);count[loop.vertex_index]+=1
    return result/np.maximum(count[:,None],1)
rc=point_colors(raw);fc=point_colors(fixed);dc=point_colors(outer)
lookup={tuple(np.round(v,6)):i for i,v in enumerate(rv)}
diffs=[]
for vv,cc in [(fv,fc),(dv,dc)]:
    for v,c in zip(vv,cc):
        idx=lookup.get(tuple(np.round(v,6)))
        if idx is not None:diffs.append(np.max(np.abs(c-rc[idx])))
inventory['color_correspondences']={'matched_vertices':len(diffs),'max_abs_linear_RGBA_difference':float(max(diffs)),
 'median_abs_linear_RGBA_difference':float(np.median(diffs))}

# Connected components and measured samples clarify what is actually moved.
parent=np.arange(len(dv))
def root(i):
    while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
    return i
for face in df:
    for a,b in zip(face,face[1:]):parent[root(int(a))]=root(int(b))
groups={}
for i,f in enumerate(df):groups.setdefault(root(int(f[0])),[]).append(i)
components=[]
for ids in groups.values():
    faces=df[ids];verts=dv[np.unique(faces)]
    components.append({'triangles':len(ids),'area':mesh_area(dv,faces),'bounds':[verts.min(0).tolist(),verts.max(0).tolist()]})
inventory['selection_components']=sorted(components,key=lambda c:-c['area'])
baseline={o.name:o.matrix_world.copy() for o in auth}
q0=pivot.rotation_quaternion.copy()
inventory['animation_samples']=[]
for frame in [1,31,61,121]:
    scene.frame_set(frame);bpy.context.view_layer.update()
    movingv,_=mesh_arrays(outer)
    inventory['animation_samples'].append({'frame':frame,'angle_degrees':math.degrees(q0.rotation_difference(pivot.rotation_quaternion).angle),
      'max_outer_vertex_displacement':float(np.linalg.norm(movingv-dv,axis=1).max()),
      'fixed_matrix_max_delta':max(abs(fixed.matrix_world[i][j]-baseline[fixed.name][i][j]) for i in range(4) for j in range(4)),
      'all_mesh_matrix_max_delta':max(abs(o.matrix_world[i][j]-baseline[o.name][i][j]) for o in auth for i in range(4) for j in range(4))})
scene.frame_set(1)

# Rendering setup is shared by every row, including raw and reopened authored GLB.
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=24
scene.cycles.use_denoising=False;scene.cycles.seed=19;scene.cycles.use_animated_seed=False
scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=720;scene.render.resolution_y=480;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.render.film_transparent=True
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.view_settings.exposure=0;scene.view_settings.gamma=1
scene.world=bpy.data.worlds.new('Shared_world');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.65,.65,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.8
target=Vector((0,0,.04))
for loc,power in [((2,3,4),50),((-3,-2,3),40),((1,0,-3),8)]:
    bpy.ops.object.light_add(type='AREA',location=loc);light=bpy.context.object
    light.data.energy=power;light.data.shape='DISK';light.data.size=2.5
    light.rotation_euler=(target-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();camera=bpy.context.object;scene.camera=camera;camera.data.type='ORTHO'
views={'side':((2,0,.08),(0,0,.08),1.12),'hero':((1.8,1.7,1.0),(0,0,.03),1.35)}
variants=[
 ('A_raw_flat_single','raw',False,'single',False,1),
 ('B_raw_flat_double','raw',False,'double',False,1),
 ('C_raw_smooth_double','raw',True,'double',False,1),
 ('D_prior_raw_display','raw',False,'historical',False,1),
 ('E_partition_flat','auth',False,None,False,1),
 ('F_partition_authored_normals','auth',True,None,False,1),
 ('G_full_authored_closed','auth',True,None,True,1),
 ('H_full_authored_open','auth',True,None,True,61),
 ('I_partition_open_no_additions','auth',True,None,False,61),
]
design={'variants':variants,'views':views,'samples':24,'seed':19,'resolution':[720,480],
 'principles':'Source hashes fixed; same aligned geometry/camera/lights; no regeneration; no aesthetics tuning.',
 'comparisons':{'A_vs_B':'sidedness only','B_vs_C':'flat versus interpolated raw normals','B_vs_D':'glTF defaults vs prior raw-display material',
 'B_vs_E':'partition with flat normals, no additions','C_vs_F':'partition/split normals with smooth surfaces',
 'F_vs_G':'added geometry, closed','I_vs_H':'added geometry, open'},
 'known_limit':'Single-sided control uses Cycles Backfacing-to-transparent shader, not browser renderer. Metrics describe pixels in these views, not utility or aesthetic acceptance.'}
(OUT/'measurements/design.json').write_text(json.dumps(design,indent=2)+'\n')
(OUT/'measurements/inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
for label,kind,smooth,material,added,frame in variants:
    raw.hide_render=kind!='raw'
    for o in auth:o.hide_render=kind!='auth' or (o in additions and not added)
    if kind=='raw':
        raw.data.materials[0]={'single':raw_single,'double':raw_double,'historical':raw_historical}[material]
        for p in raw.data.polygons:p.use_smooth=smooth
    else:
        for o in generated:
            for p in o.data.polygons:p.use_smooth=original_smooth[o.name][p.index] if smooth else False
    scene.frame_set(frame);bpy.context.view_layer.update()
    for view,(loc,aim,scale) in views.items():
        camera.location=loc;camera.rotation_euler=(Vector(aim)-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=scale
        scene.render.filepath=str(OUT/'renders'/f'{label}_{view}.png')
        bpy.ops.render.render(write_still=True)

def emission(name,color):
    mat=bpy.data.materials.new(name);mat.use_nodes=True;nodes=mat.node_tree.nodes;nodes.clear()
    n=nodes.new('ShaderNodeEmission');n.inputs[0].default_value=(*color,1)
    out=nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(n.outputs[0],out.inputs['Surface']);return mat

raw.hide_render=True
for o in auth:o.hide_render=o in additions
fixed.data.materials[0]=emission('Fixed_gray',(.28,.28,.28))
outer.data.materials[0]=emission('Actual_moving_patch_red',(1,.015,.015))
for o in generated:
    for p in o.data.polygons:p.use_smooth=original_smooth[o.name][p.index]
for label,frame in [('J_selection_closed',1),('K_selection_open',61)]:
    scene.frame_set(frame)
    for view,(loc,aim,scale) in views.items():
        camera.location=loc;camera.rotation_euler=(Vector(aim)-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.ortho_scale=scale
        scene.render.filepath=str(OUT/'renders'/f'{label}_{view}.png');bpy.ops.render.render(write_still=True)
inventory['raw_sha256_after']=hashlib.sha256(raw_path.read_bytes()).hexdigest()
assert inventory['raw_sha256_after']==raw_hash
(OUT/'measurements/inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
print('ABLATION_COMPLETE',str(OUT))
