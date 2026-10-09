#!/usr/bin/env python3
"""One persistent official TRELLIS.2 session with inspected/checkpointed stage gates."""
import os
os.environ["HF_HUB_DISABLE_TELEMETRY"]="1"
os.environ["PYTHONDONTWRITEBYTECODE"]="1"
import base64,hashlib,json,re,shutil,struct,sys,time,traceback
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import TimeoutError as FutureTimeout
from huggingface_hub import get_token
from gradio_client import Client,handle_file

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"raw/hosted-attempt001"
OUT.mkdir(exist_ok=False)
PLAN_BYTES=(ROOT/"config/generation_plan.json").read_bytes()
PLAN_SHA256=hashlib.sha256(PLAN_BYTES).hexdigest()
PLAN=json.loads(PLAN_BYTES)
STARTED=time.monotonic()
report={"phase":ROOT.name,"started_utc":datetime.now(timezone.utc).isoformat(),"status":"starting","events":[],"generation_requests":0,"export_requests":0,"successful_generation_returns":0,"downloaded_glbs":0}
def sha(p):
 with p.open("rb") as f:return hashlib.file_digest(f,"sha256").hexdigest()
def record(stage,**values):
 report["status"]=stage
 event={"stage":stage,"utc":datetime.now(timezone.utc).isoformat(),**values}
 report["events"].append(event)
 tmp=OUT/"attempt.json.tmp"
 tmp.write_text(json.dumps(report,indent=2))
 tmp.replace(OUT/"attempt.json")
 print(json.dumps(event),flush=True)
def gate(name,required):
 path=ROOT/"config"/name
 record("awaiting_"+name,required=required)
 deadline=time.monotonic()+PLAN["budget"]["checkpoint_gate_seconds"]
 while not path.exists():
  if time.monotonic()>deadline:raise TimeoutError("Checkpoint gate not satisfied: "+name)
  time.sleep(1)
 value=json.loads(path.read_text())
 assert value.get("externally_verified") is True,path
 assert re.fullmatch(r"[0-9a-f]{40}",value.get("checkpoint_commit","")),path
 for key,expected in required.items():assert value.get(key)==expected,(name,key)
 return value
def call(api,timeout,**kwargs):
 assert (ROOT/"config/generation_plan.json").read_bytes()==PLAN_BYTES,"Plan changed during live session"
 record("call_started",api=api,budget_seconds=timeout)
 started=time.monotonic()
 job=client.submit(api_name=api,**kwargs)
 last=None
 while True:
  try:
   value=job.result(timeout=min(10,max(.01,timeout-(time.monotonic()-started))))
   record("call_returned",api=api,elapsed_seconds=time.monotonic()-started)
   return value
  except FutureTimeout:
   if time.monotonic()-started>=timeout:
    cancelled=job.cancel()
    record("call_timeout_outcome_unknown",api=api,cancel_requested=True,cancel_return=cancelled)
    raise TimeoutError("Timed out at "+api+"; remote outcome unknown, do not automatically resubmit")
   state=job.status()
   status=str(getattr(state,"code",state))
   if status!=last:
    record("call_progress",api=api,status=status,elapsed_seconds=time.monotonic()-started)
    last=status
def path_of(value):
 if isinstance(value,dict):return Path(value["path"])
 return Path(value)
stage="initialization"
try:
 original=ROOT/PLAN["input"]
 assert sha(original)==PLAN["input_sha256"],"Original input hash mismatch"
 gate("initial_checkpoint_verified.json",{"input_sha256":sha(original),"plan_sha256":PLAN_SHA256})
 token=get_token()
 record("authentication",existing_hf_auth_resolves=bool(token),credential_values_logged=False)
 client=Client(PLAN["service"],token=token,download_files=str(OUT/"downloads"),verbose=False,analytics_enabled=False,httpx_kwargs={"timeout":300.0})
 stage="start_session"
 call("/start_session",60)
 stage="preprocessing"
 processed_result=call("/preprocess_image",PLAN["budget"]["preprocessing_seconds"],input=handle_file(str(original)))
 source=path_of(processed_result)
 processed=ROOT/"inputs/hosted_preprocessed.png"
 assert not processed.exists()
 shutil.copy2(source,processed)
 png=processed.read_bytes()
 assert png[:8]==b'\x89PNG\r\n\x1a\n' and png[12:16]==b'IHDR',"Expected downloaded PNG"
 width,height,bit_depth,color_type=struct.unpack(">IIBB",png[16:26])
 info={"size":[width,height],"bit_depth":bit_depth,"png_color_type":color_type}
 (OUT/"preprocessing_return.json").write_text(json.dumps({"downloaded_path":str(source),"processed_sha256":sha(processed),**info},indent=2))
 stage="preprocessing_review"
 gate("generation_checkpoint_verified.json",{"input_sha256":sha(original),"processed_sha256":sha(processed),"plan_sha256":PLAN_SHA256})
 review=json.loads((ROOT/"config/preprocessing_review.json").read_text())
 assert review["proceed"] is True and review["processed_sha256"]==sha(processed)
 with (OUT/"generation_requested.json").open("x") as f:json.dump({"utc":datetime.now(timezone.utc).isoformat(),"plan":PLAN,"processed_sha256":sha(processed)},f,indent=2)
 report["generation_requests"]=1
 stage="generation"
 value=call("/image_to_3d",PLAN["budget"]["generation_queue_and_call_seconds"],image=handle_file(str(processed)),seed=PLAN["seed"],resolution=PLAN["resolution"],**PLAN["generation_parameters"])
 assert isinstance(value,str),"Unexpected native preview return type"
 html=OUT/"generated_preview.html"
 with html.open("x") as f:f.write(value)
 report["successful_generation_returns"]=1
 frame_dir=OUT/"native_preview_frames";frame_dir.mkdir()
 frame_records=[]
 for index,(mime,payload) in enumerate(re.findall(r'data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)',value)):
  data=base64.b64decode(payload,validate=True)
  dest=frame_dir/("frame_%03d.%s"%(index,"jpg" if mime=="jpeg" else mime))
  with dest.open("xb") as f:f.write(data)
  frame_records.append({"path":str(dest.relative_to(ROOT)),"bytes":len(data),"sha256":sha(dest)})
 (OUT/"native_preview_manifest.json").write_text(json.dumps({"frames":frame_records,"html_sha256":sha(html),"server_latents":"Not exposed by public API; unavailable for direct download."},indent=2))
 record("generation_preserved",preview_bytes=html.stat().st_size,preview_sha256=sha(html),frames=len(frame_records))
 stage="preview_checkpoint"
 gate("export_checkpoint_verified.json",{"preview_sha256":sha(html)})
 stage="export"
 report["export_requests"]=1
 with (OUT/"export_requested.json").open("x") as f:json.dump({"utc":datetime.now(timezone.utc).isoformat(),"parameters":PLAN["export_parameters"]},f,indent=2)
 value=call("/extract_glb",PLAN["budget"]["export_queue_and_call_seconds"],**PLAN["export_parameters"])
 returned=value if isinstance(value,(list,tuple)) else [value]
 files=[]
 for item in returned:
  p=path_of(item)
  files.append({"downloaded_path":str(p),"bytes":p.stat().st_size,"sha256":sha(p)})
 assert files,"No exported GLB"
 destination=OUT/"untouched_official_export.glb"
 with path_of(returned[0]).open("rb") as src,destination.open("xb") as dst:shutil.copyfileobj(src,dst)
 assert destination.read_bytes()[:4]==b"glTF","Returned file is not a GLB"
 report["downloaded_glbs"]=1
 (OUT/"export_return.json").write_text(json.dumps(files,indent=2))
 record("passed",raw_glb=str(destination.relative_to(ROOT)),bytes=destination.stat().st_size,sha256=sha(destination),elapsed_total_seconds=time.monotonic()-STARTED,server_latents_downloaded=False)
except Exception as exc:
 message=str(exc)
 category="execution_failure"
 if "quota" in message.lower():category="service_admission_blocked"
 elif isinstance(exc,TimeoutError):category="timeout_outcome_unknown_or_local_gate"
 record("failed",failure_stage=stage,classification=category,error_type=type(exc).__name__,message=message,elapsed_total_seconds=time.monotonic()-STARTED)
 (OUT/"failure_traceback.txt").write_text(traceback.format_exc())
 raise

