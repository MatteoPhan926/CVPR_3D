"""One staged official TRELLIS.2 request; pause for local preprocessing inspection."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import time

ROOT = Path(__file__).resolve().parents[1]
os.environ['HF_HOME'] = str(ROOT / 'environment/remote-huggingface-cache')
os.environ['XDG_CACHE_HOME'] = str(ROOT / 'environment/remote-cache')
from gradio_client import Client, handle_file

OUT = ROOT / 'raw/hosted-attempt001'
OUT.mkdir(parents=True, exist_ok=True)
plan = json.loads((ROOT / 'config/hosted-generation-plan.json').read_text())
report = {'route': 'microsoft/TRELLIS.2', 'started_utc': datetime.now(timezone.utc).isoformat(), 'status': 'starting', 'events': [], 'generation_requests': 0}
def record(stage, **values):
    report['status'] = stage
    report['events'].append({'stage': stage, 'timestamp_utc': datetime.now(timezone.utc).isoformat(), **values})
    (OUT / 'attempt.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['events'][-1]), flush=True)

try:
    client = Client('https://microsoft-trellis-2.hf.space', download_files=str(OUT / 'downloads'), verbose=False)
    client.predict(api_name='/start_session')
    record('preprocessing_requested', original_sha256=hashlib.sha256((ROOT/'inputs/original.jpg').read_bytes()).hexdigest())
    result = client.predict(handle_file(str(ROOT / 'inputs/original.jpg')), api_name='/preprocess_image')
    source = Path(result['path'] if isinstance(result, dict) else result)
    dest = ROOT / 'inputs' / ('hosted_preprocessed' + source.suffix)
    shutil.copy2(source, dest)
    record('awaiting_preprocessing_inspection', processed_path=str(dest), processed_sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
    marker = ROOT / 'config/hosted-preprocessing-reviewed.json'
    deadline = time.monotonic() + 300
    while not marker.exists():
        if time.monotonic() > deadline:
            raise TimeoutError('No local preprocessing inspection record within five minutes; generation not requested')
        time.sleep(1)
    review = json.loads(marker.read_text())
    assert review['processed_sha256'] == hashlib.sha256(dest.read_bytes()).hexdigest()
    assert review['proceed'] is True
    guard = OUT / 'generation-requested.json'
    with guard.open('x') as file:
        json.dump({'requested_utc': datetime.now(timezone.utc).isoformat(), 'configuration': plan}, file, indent=2)
    report['generation_requests'] = 1
    record('generation_requested', seed=plan['seed'], resolution=plan['resolution'])
    result = client.predict(
        image=handle_file(str(dest)), seed=plan['seed'], resolution=plan['resolution'],
        ss_guidance_strength=plan['sparse_structure']['guidance_strength'],
        ss_guidance_rescale=plan['sparse_structure']['guidance_rescale'],
        ss_sampling_steps=plan['sparse_structure']['steps'],
        ss_rescale_t=plan['sparse_structure']['rescale_t'],
        shape_slat_guidance_strength=plan['shape']['guidance_strength'],
        shape_slat_guidance_rescale=plan['shape']['guidance_rescale'],
        shape_slat_sampling_steps=plan['shape']['steps'],
        shape_slat_rescale_t=plan['shape']['rescale_t'],
        tex_slat_guidance_strength=plan['texture']['guidance_strength'],
        tex_slat_guidance_rescale=plan['texture']['guidance_rescale'],
        tex_slat_sampling_steps=plan['texture']['steps'],
        tex_slat_rescale_t=plan['texture']['rescale_t'],
        api_name='/image_to_3d',
    )
    (OUT / 'generated-preview.html').write_text(str(result))
    record('generation_returned')
    result = client.predict(decimation_target=plan['decimation_target'], texture_size=plan['texture_size'], api_name='/extract_glb')
    paths = result if isinstance(result, (tuple, list)) else [result]
    source = Path(paths[0])
    destination = OUT / 'raw_generated.glb'
    shutil.copy2(source, destination)
    record('passed', raw_glb=str(destination), bytes=destination.stat().st_size, sha256=hashlib.sha256(destination.read_bytes()).hexdigest())
except Exception as error:
    record('failed', error_type=type(error).__name__, message=str(error))
    raise
