#!/usr/bin/env python3
"""Preserve existing artifact bytes. Does not import or run experiment code."""
import hashlib, json, os, shutil, stat, subprocess, sys, time, zipfile
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parent
WS=Path("/workspace")
SNAP=ROOT/"snapshot"
SNAP.mkdir(exist_ok=False)
META=SNAP/"recovery_metadata"
META.mkdir()
SOURCE_ROOTS=[
 "research_decision_20261008",
 "image_to_usable_car_probe_20261007",
 "generated3d_authoring_clean_20261006",
 "attachments",
 "bentley-onboarding",
]
excluded={
 "image_to_usable_car_probe_20261007/environment/venv":"Replaceable installed Python packages; installed versions recorded separately.",
 "image_to_usable_car_probe_20261007/environment/remote-client":"Replaceable remote-client Python environment; installed versions recorded separately.",
 "image_to_usable_car_probe_20261007/environment/pip-cache":"Downloaded dependency cache.",
 "image_to_usable_car_probe_20261007/environment/huggingface-cache":"Downloaded upstream model weights/configuration cache. Pinned acquisition receipts retained in probe logs; no generated latent is excluded by this rule.",
 "image_to_usable_car_probe_20261007/environment/rembg-cache":"Downloaded U2Net model weights; acquisition provenance remains in probe.",
 "image_to_usable_car_probe_20261007/environment/cache":"ONNX runtime device/telemetry cache.",
 "image_to_usable_car_probe_20261007/environment/remote-huggingface-cache":"Client harness cache, not experimental output.",
 "image_to_usable_car_probe_20261007/environment/dependencies/TripoSR/.git":"Dependency Git metadata; HEAD/status/diff separately recorded.",
 "image_to_usable_car_probe_20261007/environment/dependencies/torchmcubes/.git":"Dependency Git metadata; HEAD/status/diff separately recorded.",
 "image_to_usable_car_probe_20261007/environment/dependencies/torchmcubes/build":"Rebuildable compiled extension build directory.",
 "generated3d_authoring_clean_20261006/environment/venv":"Replaceable installed Python packages; installed versions recorded separately.",
 "generated3d_authoring_clean_20261006/environment/pip-cache":"Downloaded dependency cache.",
 "generated3d_authoring_clean_20261006/environment/npm-cache":"Downloaded dependency cache.",
 "generated3d_authoring_clean_20261006/environment/chromium-cache":"Replaceable browser runtime cache; onboarding-browser screenshots and reports ARE retained.",
 "generated3d_authoring_clean_20261006/source/project/preview/node_modules":"Installed npm packages; lockfile and compiled browser bundle ARE retained.",
}
entries=[]; errors=[]; skipped=[]; directories=[]
def digest(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
 return h.hexdigest()
def copy(p):
 rel=p.relative_to(WS).as_posix(); target=SNAP/rel
 if rel in excluded:
  skipped.append({"path":rel,"reason":excluded[rel],"source_present":True});return
 before=p.lstat()
 if stat.S_ISDIR(before.st_mode):
  target.mkdir(parents=True,exist_ok=False);directories.append(rel)
  for child in sorted(p.iterdir()):copy(child)
 elif stat.S_ISREG(before.st_mode):
  target.parent.mkdir(parents=True,exist_ok=True)
  with p.open("rb") as src, target.open("xb") as dst:shutil.copyfileobj(src,dst,1024*1024)
  shutil.copystat(p,target,follow_symlinks=False)
  after=p.stat()
  copied_hash=digest(target); source_hash=digest(p)
  stable=(before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns and copied_hash==source_hash)
  entries.append({"path":rel,"type":"file","bytes":target.stat().st_size,"sha256":copied_hash,"source_mtime_ns":before.st_mtime_ns,"mode":stat.S_IMODE(before.st_mode),"source_matches_snapshot":stable,"execution_status":"preserved_as_found_not_rerun"})
  if not stable:errors.append({"path":rel,"error":"Source changed or differs from snapshot; first bytes retained."})
 elif stat.S_ISLNK(before.st_mode):
  link=os.readlink(p);target.parent.mkdir(parents=True,exist_ok=True);target.symlink_to(link)
  entries.append({"path":rel,"type":"symlink","target":link,"source_matches_snapshot":True})
 else:errors.append({"path":rel,"error":"Special file not copied."})
for name in SOURCE_ROOTS:
 try:copy(WS/name)
 except Exception as exc:errors.append({"path":name,"error":repr(exc)})

# Store Git evidence, avoiding optional index writes and credential-bearing remote dumps.
git_records=[]
for name in ["CVPR_3D","image_to_usable_car_probe_20261007/environment/dependencies/TripoSR","image_to_usable_car_probe_20261007/environment/dependencies/torchmcubes"]:
 path=WS/name
 for args in [["rev-parse","--verify","HEAD^{commit}"],["status","--porcelain=v1","--untracked-files=all"],["diff","--binary"],["diff","--cached","--binary"],["show-ref"]]:
  result=subprocess.run(["git","-C",str(path),*args],capture_output=True,text=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS="0"),timeout=30)
  git_records.append({"repository":name,"args":args,"returncode":result.returncode,"stdout":result.stdout,"stderr":result.stderr})
(META/"git_state_before_recovery.json").write_text(json.dumps(git_records,indent=2))
versions=[]
for name in ["image_to_usable_car_probe_20261007/environment/venv","image_to_usable_car_probe_20261007/environment/remote-client","generated3d_authoring_clean_20261006/environment/venv"]:
 packages=[]
 for p in sorted((WS/name).glob("lib/python*/site-packages/*.dist-info/METADATA")):
  lines=p.read_text(errors="replace").splitlines()
  packages.append({k:next((line[len(k)+2:] for line in lines if line.startswith(k+": ")),"") for k in ["Name","Version"]})
 versions.append({"environment":name,"installed_distributions":packages})
(META/"installed_versions.json").write_text(json.dumps(versions,indent=2))
config=ROOT/"configuration_snapshot.json"
if config.exists():shutil.copy2(config,META/config.name)
shutil.copy2(Path(__file__),META/"preserve.py")
manifest={
 "checkpoint_id":ROOT.name,"created_at_utc":datetime.now(timezone.utc).isoformat(),
 "status":"LOCAL_ONLY","source_roots":SOURCE_ROOTS,
 "coverage":"Every file in research_decision_20261008, plus old probe and Bentley unique evidence, environment mesh arrays, input attachments, logs, actual dependency source and non-secret configuration.",
 "originals_modified":False,"experiments_run":False,
 "directories":directories,"files":entries,
 "excluded":skipped,"errors":errors,
 "source_file_count":sum(e["type"]=="file" for e in entries),
 "source_bytes":sum(e.get("bytes",0) for e in entries),
 "latent_paths":[e["path"] for e in entries if e["path"].endswith("scene_codes.pt")],
 "upstream_model":{"source_commit":"107cefdc244c39106fa830359024f6a2f1c78871","model_revision":"5b521936b01fbe1890f6f9baed0254ab6351c04a","model_ckpt_sha256_historical":"429e2c6b22a0923967459de24d67f05962b235f79cde6b032aa7ed2ffcd970ee"},
}
(ROOT/"source_manifest.json").write_text(json.dumps(manifest,indent=2))
shutil.copy2(ROOT/"source_manifest.json",META/"source_manifest.json")
all_files=[]
for p in sorted(SNAP.rglob("*")):
 if p.is_symlink():raise RuntimeError("Unexpected symlink: requires explicit safe archive handling: "+str(p))
 if p.is_file():all_files.append({"path":p.relative_to(SNAP).as_posix(),"bytes":p.stat().st_size,"sha256":digest(p)})
full_manifest={"checkpoint_id":ROOT.name,"format":"zip","payload_file_count":len(all_files),"payload_bytes":sum(e["bytes"] for e in all_files),"files":all_files,"empty_directories":[p.relative_to(SNAP).as_posix() for p in sorted(SNAP.rglob("*")) if p.is_dir() and not any(p.iterdir())]}
(ROOT/"MANIFEST_SHA256.json").write_text(json.dumps(full_manifest,indent=2))
archive=ROOT/"research_recovery_evidence.zip"
with zipfile.ZipFile(archive,"x",compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
 for e in all_files:z.write(SNAP/e["path"],arcname=e["path"])
 for d in full_manifest["empty_directories"]:z.writestr(d+"/",b"")
 z.write(ROOT/"MANIFEST_SHA256.json",arcname="MANIFEST_SHA256.json")
with zipfile.ZipFile(archive) as z:
 for e in all_files:
  if hashlib.sha256(z.read(e["path"])).hexdigest()!=e["sha256"]:raise RuntimeError("Local archive mismatch: "+e["path"])
parts=[]; partdir=ROOT/"archive_parts";partdir.mkdir()
with archive.open("rb") as f:
 idx=1
 while block:=f.read(90*1024*1024):
  part=partdir/("research_recovery_evidence.zip.part%03d"%idx)
  with part.open("xb") as out:out.write(block)
  parts.append({"filename":part.name,"bytes":len(block),"sha256":digest(part)});idx+=1
summary={"checkpoint_id":ROOT.name,"status":"LOCAL_ONLY","archive":{"filename":archive.name,"bytes":archive.stat().st_size,"sha256":digest(archive)},"parts":parts,"source_file_count":manifest["source_file_count"],"source_bytes":manifest["source_bytes"],"payload_file_count":len(all_files),"latent_paths":manifest["latent_paths"],"errors":errors,"external_verification":"NOT_YET_DONE"}
(ROOT/"checkpoint.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2),flush=True)
if errors:sys.exit(2)

