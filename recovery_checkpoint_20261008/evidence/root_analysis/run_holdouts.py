"""New registered non-car export controls. Never modifies the audited car run."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,hashlib,os,sys,time,random
ROOT=Path(__file__).resolve().parent
OLD=Path('/workspace/image_to_usable_car_probe_20261007')
for key,sub in [('HF_HOME','huggingface-cache'),('U2NET_HOME','rembg-cache'),('XDG_CACHE_HOME','cache')]:os.environ[key]=str(OLD/'environment'/sub)
os.environ.update(OMP_NUM_THREADS='2',MKL_NUM_THREADS='2',HF_HUB_OFFLINE='1')
sys.path.insert(0,str(OLD/'environment/dependencies/TripoSR'))
import numpy as np,torch,rembg,onnxruntime as ort
from PIL import Image
from tsr.system import TSR
from tsr.utils import remove_background,resize_foreground
parser=argparse.ArgumentParser();parser.add_argument('--generate',action='store_true');args=parser.parse_args()
contract=json.loads((ROOT/'holdout_contract.json').read_text());torch.set_num_threads(2)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if not args.generate:
    session=rembg.new_session('u2net',providers=['CPUExecutionProvider'])
    for name in contract['cases']:
        out=ROOT/'holdouts'/Path(name).stem;out.mkdir(parents=True,exist_ok=True)
        source=OLD/'environment/dependencies/TripoSR/examples'/name
        (out/name).write_bytes(source.read_bytes())
        im=Image.open(source);cut=remove_background(im,session);cut.save(out/'cutout.png')
        fit=resize_foreground(cut,.85);fit.save(out/'fitted_rgba.png')
        a=np.array(fit).astype(np.float32)/255;rgb=a[:,:,:3]*a[:,:,3:4]+(1-a[:,:,3:4])*.5
        Image.fromarray((rgb*255).astype(np.uint8)).save(out/'processed.png')
        (out/'preprocess.json').write_text(json.dumps({'input':name,'source_mode':im.mode,'source_size':im.size,'input_sha256':digest(source),'processed_sha256':digest(out/'processed.png')},indent=2)+'\n')
        print(name,'prepared',flush=True)
    raise SystemExit(0)
assert (ROOT/'holdout_preprocessing_review.json').exists()
review=json.loads((ROOT/'holdout_preprocessing_review.json').read_text())
for name in contract['cases']:
    out=ROOT/'holdouts'/Path(name).stem
    assert not (out/'inference_started.json').exists(),'Single-inference guard'
    assert review[Path(name).stem]['processed_sha256']==digest(out/'processed.png')
acq=json.loads((OLD/'logs/model-acquisition.json').read_text())
checkpoint=Path(next(x['path'] for x in acq['artifacts'] if x['filename']=='model.ckpt'))
assert digest(checkpoint)==contract['model_sha256']
model=TSR.from_pretrained(str(checkpoint.parent),config_name='config.yaml',weight_name='model.ckpt').to('cpu').eval()
model.renderer.set_chunk_size(4096)
for name in contract['cases']:
    out=ROOT/'holdouts'/Path(name).stem
    random.seed(42);np.random.seed(42);torch.manual_seed(42)
    stamp={'utc':datetime.now(timezone.utc).isoformat(),'input_sha256':digest(out/name),'processed_sha256':digest(out/'processed.png'),'contract_sha256':digest(ROOT/'holdout_contract.json')}
    (out/'inference_started.json').write_text(json.dumps(stamp,indent=2)+'\n')
    start=time.monotonic()
    with torch.no_grad():latent=model([Image.open(out/'processed.png')],device='cpu')
    inference=time.monotonic()-start;torch.save(latent,out/'scene_codes.pt')
    extract=time.monotonic();mesh=model.extract_mesh(latent,True,resolution=256)[0];mesh.export(str(out/'raw.glb'))
    result={'status':'passed','generation_calls':1,'inference_seconds':inference,'extraction_seconds':time.monotonic()-extract,'raw_sha256':digest(out/'raw.glb'),'latent_sha256':digest(out/'scene_codes.pt'),'vertices':len(mesh.vertices),'faces':len(mesh.faces)}
    (out/'execution.json').write_text(json.dumps(result,indent=2)+'\n');print(name,json.dumps(result),flush=True)
