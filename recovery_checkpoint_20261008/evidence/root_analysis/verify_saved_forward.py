"""Numerical replay of the audited forward, no mesh extraction or new car asset."""
from pathlib import Path
import os,sys,json,hashlib,time,random
OLD=Path('/workspace/image_to_usable_car_probe_20261007');OUT=Path(__file__).resolve().parent
for key,sub in [('HF_HOME','huggingface-cache'),('XDG_CACHE_HOME','cache')]:os.environ[key]=str(OLD/'environment'/sub)
os.environ.update(OMP_NUM_THREADS='4',MKL_NUM_THREADS='4',HF_HUB_OFFLINE='1')
sys.path.insert(0,str(OLD/'environment/dependencies/TripoSR'))
import torch,numpy as np
from PIL import Image
from tsr.system import TSR
torch.set_num_threads(4);random.seed(42);np.random.seed(42);torch.manual_seed(42)
acq=json.loads((OLD/'logs/model-acquisition.json').read_text());weight=Path(next(a['path'] for a in acq['artifacts'] if a['filename']=='model.ckpt'))
weight_hash=hashlib.sha256(weight.read_bytes()).hexdigest();assert weight_hash=='429e2c6b22a0923967459de24d67f05962b235f79cde6b032aa7ed2ffcd970ee'
model=TSR.from_pretrained(str(weight.parent),config_name='config.yaml',weight_name='model.ckpt').to('cpu').eval()
image=OLD/'inputs/cpu_preprocessed.png';saved=OLD/'raw/cpu-attempt001/scene_codes.pt'
start=time.monotonic()
with torch.no_grad():actual=model([Image.open(image)],device='cpu')
elapsed=time.monotonic()-start;expected=torch.load(saved,map_location='cpu',weights_only=True)
error=(actual-expected).abs();result={'purpose':'Independent replay of the audited exact processed input; no new GLB candidate, no extraction or selection.','forward_replays':1,'new_car_mesh_candidates':0,'torch':torch.__version__,'threads':4,'seed':42,'weight_sha256':weight_hash,'processed_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'saved_latent_sha256':hashlib.sha256(saved.read_bytes()).hexdigest(),'shape':list(actual.shape),'exact_tensor_equal':torch.equal(actual,expected),'max_abs_error':float(error.max()),'mean_abs_error':float(error.mean()),'forward_seconds':elapsed}
(OUT/'saved_forward_reproduction.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
assert torch.equal(actual,expected)
