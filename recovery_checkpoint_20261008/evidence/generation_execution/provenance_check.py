"""Query saved TripoSR scene, without encoder invocation or original mutations."""
import os
os.environ['OMP_NUM_THREADS']='2'
os.environ['MKL_NUM_THREADS']='2'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import json, sys, hashlib, time
from pathlib import Path
import numpy as np
import torch
import trimesh
from omegaconf import OmegaConf

ROOT=Path('/workspace/image_to_usable_car_probe_20261007')
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'environment/dependencies/TripoSR'))
from tsr.models.network_utils import NeRFMLP
from tsr.models.nerf_renderer import TriplaneNeRFRenderer

def load_field():
    torch.set_num_threads(2)
    acquisition=json.loads((ROOT/'logs/model-acquisition.json').read_text())
    checkpoint=Path(next(x['path'] for x in acquisition['artifacts'] if x['filename']=='model.ckpt'))
    cfg=OmegaConf.load(checkpoint.parent/'config.yaml')
    decoder=NeRFMLP(cfg.decoder).eval()
    weights=torch.load(checkpoint,map_location='cpu',weights_only=True,mmap=True)
    decoder.load_state_dict({k.removeprefix('decoder.'):v for k,v in weights.items() if k.startswith('decoder.')})
    renderer=TriplaneNeRFRenderer(cfg.renderer).eval()
    renderer.set_chunk_size(4096)
    latent=torch.load(ROOT/'raw/cpu-attempt001/scene_codes.pt',map_location='cpu',weights_only=True)[0]
    return decoder,renderer,latent

def summary(x):
    x=np.asarray(x)
    return {'min':float(np.min(x)),'q01':float(np.quantile(x,.01)),'q10':float(np.quantile(x,.1)),'median':float(np.median(x)),'q90':float(np.quantile(x,.9)),'q99':float(np.quantile(x,.99)),'max':float(np.max(x)),'mean':float(np.mean(x))}

if __name__=='__main__':
    started=time.monotonic()
    decoder,renderer,latent=load_field()
    mesh=trimesh.load(ROOT/'raw/car_raw.glb',force='mesh',process=False)
    with torch.no_grad():
        q=renderer.query_triplane(decoder,torch.tensor(mesh.vertices,dtype=torch.float32),latent)
    color=q['color'].numpy()
    decoded_uint8=np.round(color*255).astype(np.uint8)
    exported=np.asarray(mesh.visual.vertex_colors)[:,:3]
    err=np.abs(color-exported/255)
    source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'raw/car_raw.glb',ROOT/'raw/cpu-attempt001/scene_codes.pt',ROOT/'inputs/cpu_preprocessed.png']}
    report={'threads':2,'encoder_inference_calls':0,'source_hashes':source_hashes,
        'vertices':len(mesh.vertices),'faces':len(mesh.faces),
        'raw_density_at_vertices':summary(q['density_act'].numpy()),
        'raw_decoder_rgb':summary(color),'exported_rgb':summary(exported/255),
        'decoded_rgb_export_absolute_error':summary(err),
        'exact_quantized_rgb_match_fraction':float(np.mean(np.all(decoded_uint8==exported,axis=1))),
        'bounds':mesh.bounds.tolist(),'is_watertight':bool(mesh.is_watertight),
        'body_count':int(mesh.body_count),'euler_number':int(mesh.euler_number),
        'area':float(mesh.area),'volume':float(mesh.volume),'elapsed_seconds':time.monotonic()-started}
    (OUT/'provenance_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
