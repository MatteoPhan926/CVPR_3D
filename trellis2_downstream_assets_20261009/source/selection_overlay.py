import bpy,numpy as np,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'artifacts'/'selection_overlay_A';out.mkdir(exist_ok=False)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'artifacts/authoring_A_v1/partition_only.blend'))
s=bpy.context.scene;s.render.threads=2;s.cycles.samples=16
door=bpy.data.objects['Generated front door - native UV PBR'];hinge=bpy.data.objects['FrontDoor_Control']
data=np.load(ROOT/'artifacts/authoring_A_v1/cut_arrays.npz')
source=data['door_source'];shared=np.isin(source,np.unique(data['fixed_source']))
assert len(source)==len(door.data.polygons)
def mat(name,c):
 m=bpy.data.materials.new(name);m.use_nodes=True;t=m.node_tree;t.nodes.clear();e=t.nodes.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*c,1);o=t.nodes.new('ShaderNodeOutputMaterial');t.links.new(e.outputs[0],o.inputs['Surface']);return m
colors=[mat('DIAGNOSTIC uncut source surface - cyan',(.03,.65,.9)),mat('DIAGNOSTIC clipped boundary children - orange',(1,.15,.01)),mat('DIAGNOSTIC inward original face - magenta',(.9,.02,.45)),mat('DIAGNOSTIC tangent original face - grey',(.22,.22,.22))]
door.data.materials.clear()
for m in colors:door.data.materials.append(m)
body=bpy.data.objects['Generated exterior - fixed'];body.data.materials.clear();body.data.materials.append(mat('DIAGNOSTIC fixed body grey',(.06,.06,.06)))
hinge['open_degrees']=60.;hinge.update_tag();bpy.context.view_layer.update()
c=Vector((.015,-.16,.015));cam=s.camera;cam.data.ortho_scale=.50
cam.location=c+Vector((.6,-1,.6))*2;cam.rotation_euler=(c-cam.location).to_track_quat('-Z','Y').to_euler()
for p,is_shared in zip(door.data.polygons,shared):p.material_index=int(is_shared)
s.render.filepath=str(out/'cut_provenance_60.png');bpy.ops.render.render(write_still=True)
tri=data['door'][:,:,:3];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1,keepdims=True),1e-15)
for p,n in zip(door.data.polygons,normal):p.material_index=0 if n[1]<-.25 else (2 if n[1]>.25 else 3)
s.render.filepath=str(out/'original_orientation_60.png');bpy.ops.render.render(write_still=True)
(out/'legend.json').write_text(json.dumps({'cut_provenance':'cyan=fully inside original source face; orange=children of a source triangle also represented in fixed surface','orientation':'cyan=outward(-Y), magenta=inward(+Y), grey=tangent, threshold .25; frame geometry may legitimately be tangent/inward','limits':'Geometric provenance diagnostic only. No faces removed or authoring output modified; cannot establish semantic correctness or general conventional-workflow limit.'},indent=2))
