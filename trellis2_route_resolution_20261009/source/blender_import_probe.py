"""One import-only DCC probe of a separately labelled public example; no renders/edits."""
import argparse, hashlib, json, sys, time
from pathlib import Path
import bpy

p = argparse.ArgumentParser()
p.add_argument('--input', required=True); p.add_argument('--output', required=True)
a = p.parse_args(sys.argv[sys.argv.index('--')+1:])
source, dest = Path(a.input), Path(a.output)
if dest.exists(): raise RuntimeError('Refusing to replace an earlier result')
before = hashlib.sha256(source.read_bytes()).hexdigest()
t = time.monotonic()
bpy.ops.wm.read_factory_settings(use_empty=True)
result = bpy.ops.import_scene.gltf(filepath=str(source))
assert result == {'FINISHED'}, result
meshes = []
for obj in bpy.data.objects:
    if obj.type != 'MESH': continue
    mesh = obj.data
    meshes.append({'object':obj.name, 'vertices':len(mesh.vertices), 'polygons':len(mesh.polygons),
       'uv_layers':[layer.name for layer in mesh.uv_layers],
       'material_slots':[slot.material.name if slot.material else None for slot in obj.material_slots],
       'has_custom_normals':mesh.has_custom_normals})
materials = []
for mat in bpy.data.materials:
    nodes = mat.node_tree.nodes if mat.use_nodes else []
    links = mat.node_tree.links if mat.use_nodes else []
    materials.append({'name':mat.name, 'use_nodes':mat.use_nodes,
        'nodes':[{'name':n.name,'type':n.type,'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None} for n in nodes],
        'links':[{'from':link.from_node.name+'.'+link.from_socket.name,'to':link.to_node.name+'.'+link.to_socket.name} for link in links]})
images = [{'name':im.name,'size':list(im.size),'channels':im.channels,'has_data':im.has_data,
           'colorspace':im.colorspace_settings.name} for im in bpy.data.images]
assert hashlib.sha256(source.read_bytes()).hexdigest() == before
assert meshes and all(m['uv_layers'] for m in meshes)
assert len(images)>=2 and all(i['has_data'] and all(i['size']) for i in images)
record = {'status':'import_passed','blender_version':bpy.app.version_string,'input_sha256':before,
    'original_file_unchanged':True,'elapsed_seconds':time.monotonic()-t,
    'meshes':meshes,'materials':materials,'images':images,
    'scope':'Public fal example import-only test; not user car generation, no render/appearance judgment, no export, no repair, no door authoring or artist acceptance.'}
with dest.open('x') as f: json.dump(record,f,indent=2)
print('IMPORT_PROBE_RESULT '+json.dumps({'status':record['status'],'meshes':len(meshes),'images':len(images),'elapsed_seconds':record['elapsed_seconds']}))
