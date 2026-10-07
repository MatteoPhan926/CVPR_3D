"""One CPU TripoSR candidate using upstream preprocessing and extraction."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import random
import resource
import shutil
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
for name, folder in [('HF_HOME','huggingface-cache'),('XDG_CACHE_HOME','cache'),('U2NET_HOME','rembg-cache')]:
    os.environ[name] = str(ROOT / 'environment' / folder)
os.environ['OMP_NUM_THREADS'] = '4'
os.environ['MKL_NUM_THREADS'] = '4'
sys.path.insert(0, str(ROOT/'environment/dependencies/TripoSR'))
import numpy as np
from PIL import Image
import rembg
import torch
from tsr.system import TSR
from tsr.utils import remove_background, resize_foreground

OUT = ROOT/'raw/cpu-attempt001'
OUT.mkdir(parents=True, exist_ok=True)
plan = json.loads((ROOT/'config/generation-plan.json').read_text())
report = {'route':'TripoSR CPU','status':'starting','events':[],'generation_calls':0}
def record(stage, **values):
    report['status']=stage
    report['events'].append({'stage':stage,'timestamp_utc':datetime.now(timezone.utc).isoformat(),**values})
    (OUT/'attempt.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['events'][-1]),flush=True)

try:
    torch.set_num_threads(4)
    random.seed(plan['seed']);np.random.seed(plan['seed']);torch.manual_seed(plan['seed'])
    cutout=remove_background(Image.open(ROOT/'inputs/original.jpg'),rembg.new_session('u2net',providers=['CPUExecutionProvider']))
    cutout.save(ROOT/'inputs/cpu_cutout.png')
    fitted=resize_foreground(cutout,plan['preprocessing']['foreground_ratio'])
    fitted.save(ROOT/'inputs/cpu_fitted_rgba.png')
    values=np.array(fitted).astype(np.float32)/255.0
    values=values[:,:,:3]*values[:,:,3:4]+(1-values[:,:,3:4])*0.5
    processed=Image.fromarray((values*255.0).astype(np.uint8))
    processed_path=ROOT/'inputs/cpu_preprocessed.png';processed.save(processed_path)
    processed_hash=hashlib.sha256(processed_path.read_bytes()).hexdigest()
    record('awaiting_preprocessing_inspection',processed_path=str(processed_path),processed_sha256=processed_hash)
    marker=ROOT/'config/cpu-preprocessing-reviewed.json'
    deadline=time.monotonic()+300
    while not marker.exists():
        if time.monotonic()>deadline:raise TimeoutError('No local preprocessing inspection record; inference not run')
        time.sleep(1)
    review=json.loads(marker.read_text())
    assert review['processed_sha256']==processed_hash and review['proceed'] is True
    acquisition=json.loads((ROOT/'logs/model-acquisition.json').read_text())
    checkpoint=Path(next(x['path'] for x in acquisition['artifacts'] if x['filename']=='model.ckpt'))
    with checkpoint.open('rb') as file:assert hashlib.file_digest(file,'sha256').hexdigest()==plan['model_sha256']
    model=TSR.from_pretrained(str(checkpoint.parent),config_name='config.yaml',weight_name='model.ckpt')
    model.renderer.set_chunk_size(plan['chunk_size']);model.to('cpu').eval()
    with (OUT/'inference-started.json').open('x') as file:json.dump(plan,file,indent=2)
    report['generation_calls']=1
    started=time.monotonic();record('inference_started')
    with torch.no_grad():scene_codes=model([processed],device='cpu')
    record('inference_finished',wall_seconds=time.monotonic()-started,scene_code_shape=list(scene_codes.shape))
    torch.save(scene_codes,OUT/'scene_codes.pt')
    record('mesh_extraction_started',resolution=plan['marching_cubes_resolution'],chunk_size=plan['chunk_size'])
    extraction=time.monotonic()
    meshes=model.extract_mesh(scene_codes,True,resolution=plan['marching_cubes_resolution'])
    assert len(meshes)==1
    mesh=meshes[0];raw=OUT/'raw_generated.glb';mesh.export(str(raw))
    shutil.copy2(raw,ROOT/'raw/car_raw.glb')
    record('passed',vertices=len(mesh.vertices),faces=len(mesh.faces),bounds=mesh.bounds.tolist(),visual_kind=mesh.visual.kind,raw_glb=str(raw),sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),extraction_seconds=time.monotonic()-extraction,total_generation_seconds=time.monotonic()-started,process_max_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
except Exception as error:
    record('failed',error_type=type(error).__name__,message=str(error))
    raise
