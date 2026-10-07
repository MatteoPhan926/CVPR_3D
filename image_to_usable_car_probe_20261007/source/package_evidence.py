"""Package retained probe evidence without large replaceable model environments."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json,html

ROOT=Path(__file__).resolve().parents[1]
destination=ROOT.parent/'IMAGE_TO_USABLE_CAR_PROBE_20261007_evidence.zip'
panels=[
 ('Exact user photograph','inputs/original.jpg'),
 ('Normal CPU preprocessing','inputs/cpu_preprocessed.png'),
 ('Raw generation — browser','source/viewer/verification/final/raw_comparison.png'),
 ('Authored closed — same browser camera','source/viewer/verification/final/authored_comparison_closed.png'),
 ('Authored 30° — browser','source/viewer/verification/final/authored_intermediate.png'),
 ('Authored 60° — browser','source/viewer/verification/final/authored_open.png'),
 ('Closed side — reopened GLB, Blender','artifacts/authored-inspection/closed_side.png'),
 ('Open side — reopened GLB, Blender','artifacts/authored-inspection/open_side.png'),
 ('Newly exposed surfaces at 60° — Blender','artifacts/authored-inspection/open_exposed.png'),
]
gallery='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Image to car — observed evidence</title><style>body{font:16px system-ui;max-width:1440px;margin:32px auto;padding:0 24px;background:#f4f4f2;color:#222}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px}figure{margin:0;background:white;padding:12px}img{width:100%;height:300px;object-fit:contain}figcaption{font-weight:600;padding:12px 0}a{color:#174e78}</style>
<h1>One image → one generated car → bounded door authoring</h1>
<p><strong>Informative partial: mechanical motion passes; convincing CGI appearance fails.</strong> Exact original image, raw output and both authoring revisions are retained. No replacement car or favorable candidate selection.</p>
<p>Browser raw/closed images use the same camera and lighting; authored exterior normals were smoothed. Blender uses a separate neutral studio setup. The jagged window edges, exposed cavity and incomplete floor remain visible. These are observed images from saved assets, without image-generation retouching.</p>
<p><a href="IMAGE_TO_USABLE_CAR_REPORT.md">Report</a> · <a href="raw/car_raw.glb">Raw GLB</a> · <a href="artifacts/car_authored.glb">Authored GLB</a> · <a href="source/viewer/README.md">Viewer instructions</a></p><main>'''
for label,relative in panels:
    assert (ROOT/relative).is_file(),relative
    gallery+=f'<figure><a href="{html.escape(relative)}"><img src="{html.escape(relative)}" alt="{html.escape(label)}"></a><figcaption>{html.escape(label)}</figcaption></figure>\n'
gallery+='</main><p>The original geometry and screenshot files are linked above; no physical clearance or unseen-surface accuracy is certified.</p></html>\n'
(ROOT/'EVIDENCE.html').write_text(gallery)

files=[]
for folder in ['inputs','config','source','research','raw','logs']:
    for p in (ROOT/folder).rglob('*'):
        if not p.is_file() or p.is_symlink():continue
        if any(x in p.parts for x in ['node_modules','__pycache__']):continue
        if p.name in ['viewer-server.log','package-result.json','scene_codes.pt','raw_generated.glb'] or p.suffix=='.zip':continue
        if 'verification' in p.parts and p.suffix=='.png' and 'final' not in p.parts:continue
        files.append(p)
for name in ['car_authored.glb','car_authored.blend']:
    files.append(ROOT/'artifacts'/name)
for folder in ['authored-inspection','raw-color-inspection','car-frame']:
    files.extend(p for p in (ROOT/'artifacts'/folder).glob('*.json'))
for name in ['closed_side.png','open_side.png','open_exposed.png']:
    files.append(ROOT/'artifacts/authored-inspection'/name)
files.extend(p for p in (ROOT/'artifacts/authoring-v1').glob('*') if p.is_file() and p.suffix in ['.glb','.json','.py'])
files.append(ROOT/'artifacts/authoring-v1/inspection/closed_hero.png')
for name in ['IMAGE_TO_USABLE_CAR_REPORT.md','RESUME.md','EVIDENCE.html']:
    files.append(ROOT/name)
files=sorted(set(files))
manifest={str(p.relative_to(ROOT)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files}
manifest_path=ROOT/'MANIFEST_SHA256.json';manifest_path.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
with ZipFile(destination,'w',ZIP_DEFLATED,compresslevel=6) as z:
    for p in files+[manifest_path]:z.write(p,str(p.relative_to(ROOT)))
with ZipFile(destination) as z:
    assert z.testzip() is None
    for name,metadata in manifest.items():assert hashlib.sha256(z.read(name)).hexdigest()==metadata['sha256'],name
archive_hash=hashlib.sha256(destination.read_bytes()).hexdigest()
destination.with_suffix('.zip.sha256').write_text(archive_hash+'  '+destination.name+'\n')
print(json.dumps({'archive':str(destination),'files':len(files)+1,'bytes':destination.stat().st_size,'sha256':archive_hash,'manifest_verified':True},indent=2))
