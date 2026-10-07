"""Verify the real checkpoint loads on CPU without generating a substitute asset."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
os.environ['HF_HOME'] = str(ROOT / 'environment/huggingface-cache')
os.environ['XDG_CACHE_HOME'] = str(ROOT / 'environment/cache')
os.environ['OMP_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '4'
sys.path.insert(0, str(ROOT / 'environment/dependencies/TripoSR'))
from huggingface_hub import hf_hub_download
from huggingface_hub.utils import logging as hub_logging
import torch
from tsr.system import TSR

hub_logging.set_verbosity_error()
torch.set_num_threads(4)
acquisition = json.loads((ROOT / 'logs/model-acquisition.json').read_text())
assert acquisition['status'] == 'passed', 'Model acquisition must pass first'
checkpoint = next(x for x in acquisition['artifacts'] if x['filename'] == 'model.ckpt')
path = Path(checkpoint['path'])
with path.open('rb') as file:
    digest = hashlib.file_digest(file, 'sha256').hexdigest()
assert digest == '429e2c6b22a0923967459de24d67f05962b235f79cde6b032aa7ed2ffcd970ee'
# Upstream's tokenizer requests the default ref; prime it and verify it still
# resolves to the exact configuration already recorded for this attempt.
dino = Path(hf_hub_download('facebook/dino-vitb16', 'config.json'))
assert dino.parent.name == 'f205d5d8e640a89a2b8ef0369670dfc37cc07fc2'
assert hashlib.sha256(dino.read_bytes()).hexdigest() == 'b87c0270b97db085fd82cf114a761fd0f62ae7914fbd407c752a2260646b689c'
start = time.monotonic()
model = TSR.from_pretrained(str(path.parent), config_name='config.yaml', weight_name='model.ckpt')
model.renderer.set_chunk_size(4096)
model.to('cpu').eval()
report = {
    'status': 'passed',
    'timestamp_utc': datetime.now(timezone.utc).isoformat(),
    'checkpoint_sha256': digest,
    'checkpoint_revision': checkpoint['revision'],
    'torch_version': torch.__version__,
    'devices': sorted({str(p.device) for p in model.parameters()}),
    'parameter_count': sum(p.numel() for p in model.parameters()),
    'initialization_wall_seconds': time.monotonic() - start,
    'process_max_rss_mib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
    'image_inference_executed': False,
}
assert report['devices'] == ['cpu']
(ROOT / 'logs/model-initialization.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
