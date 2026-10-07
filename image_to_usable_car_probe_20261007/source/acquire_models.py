"""Acquire official TripoSR artifacts without disabling TLS or hash verification."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
os.environ['HF_HOME'] = str(ROOT / 'environment/huggingface-cache')
os.environ['XDG_CACHE_HOME'] = str(ROOT / 'environment/cache')
from huggingface_hub import hf_hub_download
from huggingface_hub.utils import logging as hub_logging

# Preserve structured errors below without logging expiring signed redirect URLs.
hub_logging.set_verbosity_error()

items = [
    ('stabilityai/TripoSR', '5b521936b01fbe1890f6f9baed0254ab6351c04a', 'config.yaml', None),
    ('facebook/dino-vitb16', 'f205d5d8e640a89a2b8ef0369670dfc37cc07fc2', 'config.json', None),
    ('stabilityai/TripoSR', '5b521936b01fbe1890f6f9baed0254ab6351c04a', 'model.ckpt', '429e2c6b22a0923967459de24d67f05962b235f79cde6b032aa7ed2ffcd970ee'),
]
report = {'timestamp_utc': datetime.now(timezone.utc).isoformat(), 'artifacts': [], 'status': 'started'}
failed = False
for repo, revision, name, expected_sha in items:
    item = {'repository': repo, 'revision': revision, 'filename': name}
    try:
        path = Path(hf_hub_download(repo, name, revision=revision, resume_download=True))
        digest = hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()
        if expected_sha and digest != expected_sha:
            raise ValueError('Checkpoint checksum differs from publisher LFS SHA-256')
        item.update(status='verified' if expected_sha else 'downloaded', path=str(path), bytes=path.stat().st_size, sha256=digest)
    except Exception as error:
        failed = True
        response = getattr(error, 'response', None)
        request = getattr(error, 'request', None)
        address = urlsplit(getattr(request, 'url', '') or '')
        item.update(status='failed', error_type=type(error).__name__, http_status=getattr(response, 'status_code', None), destination_host=address.hostname, destination_path=address.path, proxy_403='Tunnel connection failed: 403 Forbidden' in str(error))
    report['artifacts'].append(item)
    print(json.dumps(item), flush=True)
report['status'] = 'blocked' if failed else 'passed'
(ROOT / 'logs/model-acquisition.json').write_text(json.dumps(report, indent=2) + '\n')
raise SystemExit(1 if failed else 0)
