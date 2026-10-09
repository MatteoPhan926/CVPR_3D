"""Fresh Blender import diagnostics, no source changes and no scene save."""
import argparse, hashlib, json, sys, time
from pathlib import Path
import bpy

p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--output',required=True);p.add_argument('--export')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(a.input);dest=Path(a.output)
assert not dest.exists();digest=hashlib.sha256(src.read_bytes()).hexdigest();started=time.monotonic()
bpy.ops.wm.read_factory_settings(use_empty=True)
assert bpy.ops.import_scene.gltf(filepath=str(src))=={'FINISHED'}
meshes=[]
for obj in bpy.data.objects:
    if obj.type!='MESH':continue
    mesh=obj.data
    meshes.append({'object':obj.name,'vertices':len(mesh.vertices),'polygons':len(mesh.polygons),
      'uv_layers':[x.name for x in mesh.uv_layers],'material_slots':[x.material.name if x.material else None for x in obj.material_slots],
      'custom_normals':mesh.has_custom_normals,'location':list(obj.location),'rotation_quaternion':list(obj.rotation_quaternion),
      'scale':list(obj.scale),'dimensions':list(obj.dimensions)})
materials=[]
for mat in bpy.data.materials:
    tree=mat.node_tree
    materials.append({'name':mat.name,'use_nodes':mat.use_nodes,
      'nodes':[{'name':n.name,'type':n.type,'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None} for n in tree.nodes],
      'links':[{'from':x.from_node.name+'.'+x.from_socket.name,'to':x.to_node.name+'.'+x.to_socket.name} for x in tree.links],
      'principled_inputs':[{key:list(n.inputs[key].default_value) if key=='Base Color' else n.inputs[key].default_value for key in ['Base Color','Metallic','Roughness','Alpha']} for n in tree.nodes if n.type=='BSDF_PRINCIPLED']})
images=[{'name':im.name,'size':list(im.size),'channels':im.channels,'has_data':im.has_data,'colorspace':im.colorspace_settings.name,
         'file_format':im.file_format,'packed':bool(im.packed_file)} for im in bpy.data.images]
assert meshes and all(m['uv_layers'] for m in meshes)
assert len(images)==2 and all(i['has_data'] and i['size']==[2048,2048] for i in images)
assert hashlib.sha256(src.read_bytes()).hexdigest()==digest
report={'status':'import_passed','input':str(src),'sha256':digest,'blender_version':bpy.app.version_string,
 'elapsed_seconds':time.monotonic()-started,'original_file_unchanged':True,'meshes':meshes,'materials':materials,'images':images,
 'scope':'Actual Blender import/material wiring check. No render, scene save, export, repair, or visual-quality judgment.'}
if a.export:
    export=Path(a.export);assert not export.exists()
    export_start=time.monotonic()
    options={'filepath':str(export),'export_format':'GLB','export_image_format':'AUTO',
      'export_texcoords':True,'export_normals':True,'export_materials':'EXPORT','export_animations':False}
    assert bpy.ops.export_scene.gltf(**options)=={'FINISHED'}
    assert export.is_file() and hashlib.sha256(src.read_bytes()).hexdigest()==digest
    report['export']={'path':str(export),'sha256':hashlib.sha256(export.read_bytes()).hexdigest(),
      'bytes':export.stat().st_size,'options':options,'elapsed_seconds':time.monotonic()-export_start}
    report['scope']='Actual import and unmodified export in a new file. No render, repair, visual-quality or authoring judgment.'
with dest.open('x') as f:json.dump(report,f,indent=2)
print('IMPORT_DIAGNOSTICS '+json.dumps({'status':report['status'],'seconds':report['elapsed_seconds'],'images':images}))
