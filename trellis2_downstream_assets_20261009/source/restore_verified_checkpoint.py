"""Restore the two final archives into a NEW/empty directory, never over changes.

Pass the exact externally verified data commit from DOWNLOADS.md. No setup,
generation, authoring, credentials, git mutation or dependency install occurs.
"""
import argparse,hashlib,io,json,re,tempfile,urllib.request,zipfile
from datetime import datetime,timezone
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--commit',required=True)
p.add_argument('--destination',type=Path,required=True)
p.add_argument('--receipt',type=Path,required=True)
p.add_argument('--check-existing',action='store_true',help='Read manifests and report matching/missing/changed files; no payload writes')
a=p.parse_args()
assert re.fullmatch('[0-9a-f]{40}',a.commit),'Need exact data commit'
assert not a.receipt.exists(),'Refuse overwriting a receipt'
destination=a.destination.absolute()
assert not destination.is_symlink(),'Refuse a symlink destination'
if not a.check_existing and destination.exists() and any(destination.iterdir()):
    raise SystemExit('Destination is not empty. Existing work is preserved. Use --check-existing to report differences or choose a NEW destination.')
base=f'https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/{a.commit}/trellis2_downstream_assets_20261009/checkpoints/'
scratch=Path(tempfile.mkdtemp(prefix='trellis-final-restore-'))
def sha(b):return hashlib.sha256(b).hexdigest()
def fetch(name):
    data=urllib.request.urlopen(base+name,timeout=90).read()
    (scratch/name).write_bytes(data)
    return data
archives=[];entries={};contents={}
for name in ['05_final_delivery','06_supporting_evidence']:
    m=json.loads(fetch(name+'.manifest.json'))
    for entry in m['payload_files']:
        rel=Path(entry['path'])
        assert not rel.is_absolute() and '..' not in rel.parts
        assert entry['path'] not in entries,'Overlapping payload path'
        entries[entry['path']]=entry
    if not a.check_existing:
        blob=fetch(m['archive'])
        assert len(blob)==m['archive_bytes'] and sha(blob)==m['archive_sha256']
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            names=z.namelist();assert len(names)==len(set(names))
            assert set(names)=={e['path'] for e in m['payload_files']}|{'CHECKPOINT_CONTENTS.json'}
            assert json.loads(z.read('CHECKPOINT_CONTENTS.json'))==m['payload_files']
            for entry in m['payload_files']:
                data=z.read(entry['path'])
                assert len(data)==entry['bytes'] and sha(data)==entry['sha256'],entry['path']
                contents[entry['path']]=data
    archives.append({'name':name,'url':base+m['archive'],'manifest_url':base+name+'.manifest.json','sha256':m['archive_sha256'],'bytes':m['archive_bytes'],'payload_files':len(m['payload_files'])})
missing=[];changed=[];matched=[]
if a.check_existing:
    for rel,entry in entries.items():
        target=destination/rel
        if not target.exists():missing.append(rel)
        elif target.is_symlink() or not target.is_file() or sha(target.read_bytes())!=entry['sha256']:changed.append(rel)
        else:matched.append(rel)
else:
    # Both remote archives and every member verified before restoring any file.
    destination.mkdir(parents=True,exist_ok=True)
    for rel,data in contents.items():
        target=destination/rel;target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as f:f.write(data)
        assert sha(target.read_bytes())==entries[rel]['sha256'],rel
        matched.append(rel)
record={'operation':'check_existing' if a.check_existing else 'restore_into_new_directory','commit':a.commit,'utc':datetime.now(timezone.utc).isoformat(),'externally_downloaded_archives_verified':not a.check_existing,'archives':archives,'payload_files':len(entries),'matched_files':len(matched),'missing_files':missing,'changed_or_unsafe_files':changed,'destination':str(destination),'fresh_download_directory':str(scratch),'existing_work_overwritten':False,'limits':'Excludes historical checkpoint archives and later delivery/configuration receipts. Generator metadata and unexposed server latents remain unavailable.'}
a.receipt.parent.mkdir(parents=True,exist_ok=True)
with a.receipt.open('x') as f:json.dump(record,f,indent=2)
print(json.dumps(record,indent=2))
if missing or changed:raise SystemExit(2)
