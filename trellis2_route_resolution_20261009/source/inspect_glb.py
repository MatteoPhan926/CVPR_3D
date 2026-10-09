#!/usr/bin/env python3
"""Inspect actual GLB properties without rewriting geometry or materials."""
import argparse, hashlib, json, struct
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('input'); p.add_argument('--output', required=True)
args = p.parse_args()
source, dest = Path(args.input), Path(args.output)
data = source.read_bytes()
magic, version, total = struct.unpack_from('<4sII', data)
assert magic == b'glTF' and version == 2 and total == len(data)
offset = 12; chunks = []; document = None
while offset < total:
    size, kind = struct.unpack_from('<II', data, offset); offset += 8
    chunk = data[offset:offset+size]; assert len(chunk) == size
    if kind == 0x4e4f534a: document = json.loads(chunk)
    chunks.append({'type': hex(kind), 'bytes': size}); offset += size
assert offset == total and document is not None
accessors = document.get('accessors', [])
primitives = []
for mi, mesh in enumerate(document.get('meshes', [])):
    for pi, primitive in enumerate(mesh['primitives']):
        attrs = primitive.get('attributes', {})
        n = accessors[attrs['POSITION']]['count']
        count = accessors[primitive['indices']]['count'] if 'indices' in primitive else n
        mode = primitive.get('mode', 4)
        primitives.append({'mesh': mi, 'primitive': pi, 'vertices': n, 'mode': mode,
            'triangles': count // 3 if mode == 4 else None,
            'attribute_accessors': attrs, 'material': primitive.get('material'),
            'has_uv0': 'TEXCOORD_0' in attrs, 'has_normals': 'NORMAL' in attrs})
images = []
for i, item in enumerate(document.get('images', [])):
    row = {'index': i, 'mime_type': item.get('mimeType'), 'embedded': 'bufferView' in item,
           'has_uri': 'uri' in item}
    if 'bufferView' in item: row['bytes'] = document['bufferViews'][item['bufferView']]['byteLength']
    images.append(row)
result = {'input': str(source), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
          'container_version': version, 'asset_metadata': document.get('asset'), 'chunks': chunks,
          'extensions_used': document.get('extensionsUsed', []),
          'extensions_required': document.get('extensionsRequired', []),
          'meshes': len(document.get('meshes', [])), 'nodes': len(document.get('nodes', [])),
          'primitives': primitives, 'materials': document.get('materials', []),
          'textures': document.get('textures', []), 'images': images,
          'animation_count': len(document.get('animations', [])),
          'scope': 'Observed container/material structure only; no attribution to user car, model revision, visual quality or authoring success.'}
with dest.open('x') as f: json.dump(result, f, indent=2)
print(json.dumps({'sha256': result['sha256'], 'primitives': primitives, 'materials': result['materials'],
                  'extensions_required': result['extensions_required'], 'images': images}, indent=2))
