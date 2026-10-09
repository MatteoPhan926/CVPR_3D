#!/usr/bin/env python3
"""Snapshot this phase; independently download and hash every archived member."""
import argparse, hashlib, io, json, re, tempfile, urllib.request, zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D'
def digest(data): return hashlib.sha256(data).hexdigest()
def dump(path, data):
    with path.open('x') as f: json.dump(data, f, indent=2)

p = argparse.ArgumentParser()
p.add_argument('operation', choices=['pack', 'verify'])
p.add_argument('name')
p.add_argument('--commit')
args = p.parse_args()
assert re.fullmatch(r'[a-z0-9_-]+', args.name)
cp = ROOT / 'checkpoints'
cp.mkdir(exist_ok=True)
archive = cp / (args.name + '.zip')
manifest_path = cp / (args.name + '.manifest.json')
if args.operation == 'pack':
    entries = []
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        for f in sorted(ROOT.rglob('*')):
            if not f.is_file() or f.is_symlink() or 'checkpoints' in f.relative_to(ROOT).parts:
                continue
            data = f.read_bytes()
            name = f.relative_to(ROOT).as_posix()
            z.writestr(name, data)
            assert f.read_bytes() == data, 'Source changed during snapshot: ' + name
            entries.append({'path': name, 'bytes': len(data), 'sha256': digest(data)})
        z.writestr('CHECKPOINT_CONTENTS.json', json.dumps(entries, indent=2))
    data = archive.read_bytes()
    dump(manifest_path, {'name': args.name, 'utc': datetime.now(timezone.utc).isoformat(),
         'archive': archive.name, 'archive_bytes': len(data), 'archive_sha256': digest(data),
         'payload_files': entries, 'excluded': ['Prior checkpoint ZIPs/manifests/receipts (retained separately in Git history)', 'External installed environments/model weights', 'Server-held unexposed latent state'],
         'original_evidence': 'Original probe and prior research remain unchanged and separately checkpointed.'})
    print(json.dumps({'archive': str(archive), 'files': len(entries), 'bytes': len(data), 'sha256': digest(data)}))
else:
    assert args.commit and re.fullmatch(r'[0-9a-f]{40}', args.commit)
    base = BASE + '/' + args.commit + '/' + ROOT.name + '/checkpoints/'
    folder = Path(tempfile.mkdtemp(prefix='trellis-readback-', dir='/tmp'))
    def read(name):
        data = urllib.request.urlopen(base + name, timeout=90).read()
        (folder / name).write_bytes(data)
        return data
    remote_manifest = read(manifest_path.name)
    assert remote_manifest == manifest_path.read_bytes(), 'Manifest remote mismatch'
    m = json.loads(remote_manifest)
    data = read(archive.name)
    assert len(data) == m['archive_bytes'] and digest(data) == m['archive_sha256']
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = z.namelist()
        assert len(names) == len(set(names))
        assert set(names) == {e['path'] for e in m['payload_files']} | {'CHECKPOINT_CONTENTS.json'}
        assert json.loads(z.read('CHECKPOINT_CONTENTS.json')) == m['payload_files']
        for entry in m['payload_files']:
            path = Path(entry['path'])
            assert not path.is_absolute() and '..' not in path.parts
            content = z.read(entry['path'])
            assert len(content) == entry['bytes'] and digest(content) == entry['sha256']
            dest = folder / 'extracted' / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
            assert digest(dest.read_bytes()) == entry['sha256']
    receipt = {'externally_verified': True, 'checkpoint_commit': args.commit,
       'utc': datetime.now(timezone.utc).isoformat(), 'archive_url': base + archive.name,
       'manifest_url': base + manifest_path.name, 'archive_sha256': digest(data),
       'verified_payload_files': len(m['payload_files']), 'fresh_download_directory': str(folder),
       'verification': 'Fresh immutable HTTPS downloads; archive and every member SHA-256; safe extraction and reread.'}
    dump(cp / (args.name + '.verification.json'), receipt)
    print(json.dumps(receipt))
