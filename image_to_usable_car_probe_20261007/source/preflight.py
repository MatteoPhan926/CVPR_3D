#!/usr/bin/env python3
"""Preserve an exact supplied image and collect non-destructive access evidence.

This does not perform inference or pretend to reproduce an unavailable generator.
Run from any directory; all outputs are kept inside this probe workspace.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
from urllib.error import HTTPError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--image', type=Path, help='Original user-uploaded image, not a screenshot or substitute')
parser.add_argument('--check-network', action='store_true', help='Retry only after a network-policy change')
args = parser.parse_args()
timestamp = datetime.now(timezone.utc)
report = {
    'timestamp_utc': timestamp.isoformat(),
    'python': platform.python_version(),
    'platform': platform.platform(),
    'cpu_count': os.cpu_count(),
    'nvidia_smi': shutil.which('nvidia-smi'),
    'nvcc': shutil.which('nvcc'),
    'nvidia_device_nodes': [str(p) for p in Path('/dev').glob('nvidia*')],
    'inference_executed': False,
    'network': [],
}
if args.image:
    from PIL import Image
    source = args.image.resolve(strict=True)
    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    with Image.open(source) as image:
        image.verify()
    with Image.open(source) as image:
        metadata = {'width': image.width, 'height': image.height, 'mode': image.mode, 'format': image.format}
    destination = ROOT / 'inputs' / ('original' + source.suffix.lower())
    if destination.exists() and destination.read_bytes() != raw:
        raise SystemExit('Refusing to replace an existing different original image.')
    if not destination.exists():
        destination.write_bytes(raw)
    report['input'] = {'source_path': str(source), 'preserved_path': str(destination), 'sha256': digest, **metadata}
    (ROOT / 'inputs/original_metadata.json').write_text(json.dumps(report['input'], indent=2) + '\n')
else:
    report['input'] = {'status': 'Original image bytes not supplied to this script; chat-visible image is not substituted.'}
if args.check_network:
    for url in [
        'https://huggingface.co/api/spaces/microsoft/TRELLIS.2',
        'https://huggingface.co/microsoft/TRELLIS.2-4B/resolve/main/pipeline.json',
        'https://huggingface.co/stabilityai/TripoSR/resolve/main/config.yaml',
    ]:
        observation = {'url': url}
        try:
            request = Request(url, headers={'User-Agent': 'Codex-ImageTo3D-Probe/1.0'})
            with urlopen(request, timeout=25) as response:
                data = response.read(1024 * 1024)
                observation.update(status=response.status, final_url=response.url, bytes_read=len(data), sha256=hashlib.sha256(data).hexdigest())
        except HTTPError as error:
            observation.update(status=error.code, error=str(error))
        except Exception as error:
            observation['error'] = str(error)
        report['network'].append(observation)
output = ROOT / 'logs' / ('preflight-' + timestamp.strftime('%Y%m%dT%H%M%S%fZ') + '.json')
output.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
print('Evidence written:', output)
