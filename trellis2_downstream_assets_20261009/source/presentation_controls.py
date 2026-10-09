import bpy, sys, json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
label=sys.argv[sys.argv.index('--')+1]
base=ROOT/'artifacts'/'raw_inspection'/(label+'_v2')
out=ROOT/'artifacts'/'presentation_controls'/label
out.mkdir(parents=True,exist_ok=False)
bpy.ops.wm.open_mainfile(filepath=str(base/'native_import.blend'))
scene=bpy.context.scene
scene.render.threads=2
cam=scene.camera
info=json.loads((base/'inspection.json').read_text())
center=Vector(info['center']);size=info['size']
def render(name,offset):
    cam.location=center+Vector(offset)*size*2
    cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
render('side_native',(0,-1,0))
for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    tree=mat.node_tree
    principled=next((n for n in tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
    output=next(n for n in tree.nodes if n.type=='OUTPUT_MATERIAL')
    emission=tree.nodes.new('ShaderNodeEmission')
    if principled and principled.inputs['Base Color'].links:
        tree.links.new(principled.inputs['Base Color'].links[0].from_socket,emission.inputs['Color'])
    tree.links.new(emission.outputs[0],output.inputs['Surface'])
render('q1_basecolor',(1,-1,.65))
render('side_basecolor',(0,-1,0))
clay=bpy.data.materials.new('Diagnostic clay');clay.diffuse_color=(.32,.32,.32,1);clay.use_nodes=True
clay.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.32,.32,.32,1)
clay.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.65
scene.view_layers[0].material_override=clay
render('side_clay',(0,-1,0))
render('q1_clay',(1,-1,.65))
(out/'controls.json').write_text(json.dumps({'label':label,'source':'Native imported blend; overrides in transient copy only','native_material_edit':False,'controls':['unlit base color via emission, still AgX display transform','uniform clay override under same lights'],'side_projection':{'center':list(center),'ortho_scale':cam.data.ortho_scale,'width':scene.render.resolution_x,'height':scene.render.resolution_y,'screen_x':'world +X','screen_up':'world +Z'},'scope':'Discriminates geometry/texture/shading appearance; not an optimized material repair or objective fidelity measure'},indent=2))
