#!/usr/bin/env python3
"""Download and byte-verify a recovery checkpoint, without executing research code."""
import argparse, hashlib, json, re, shutil, stat, urllib.request, zipfile
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone

def digest(path):
 with path.open("rb") as stream:return hashlib.file_digest(stream,"sha256").hexdigest()
def safe_rel(name):
 p=PurePosixPath(name)
 if p.is_absolute() or ".." in p.parts or "\\" in name or not p.parts:raise ValueError("Unsafe archive path")
 return p
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--commit",required=True)
 parser.add_argument("--destination",required=True)
 args=parser.parse_args()
 if not re.fullmatch(r"[0-9a-f]{40}",args.commit):raise ValueError("Use the full verified Git commit SHA.")
 dest=Path(args.destination).resolve()
 dest.mkdir(parents=True,exist_ok=False)
 downloads=dest/"downloaded";downloads.mkdir()
 restored=dest/"restored";restored.mkdir()
 base="https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/"+args.commit+"/recovery_checkpoint_20261008/"
 receipts=[]
 def download(relative):
  safe_rel(relative)
  target=downloads/relative;target.parent.mkdir(parents=True,exist_ok=True)
  url=base+relative
  req=urllib.request.Request(url,headers={"User-Agent":"CVPR3D-Recovery-Verification/1.0","Cache-Control":"no-cache"})
  with urllib.request.urlopen(req,timeout=120) as response,target.open("xb") as out:
   if response.status!=200:raise RuntimeError("Unexpected HTTP status")
   shutil.copyfileobj(response,out,1024*1024)
  receipts.append({"path":relative,"url":url,"bytes":target.stat().st_size,"sha256":digest(target),"http_status":200})
  print("Downloaded "+relative,flush=True)
  return target
 index=json.loads(download("CHECKPOINT.json").read_text())
 manifest=json.loads(download("MANIFEST_SHA256.json").read_text())
 expected={e["path"]:e for e in manifest["files"]}
 if len(expected)!=len(manifest["files"]):raise ValueError("Duplicate global manifest entry.")
 seen=set()
 for archive in index["archives"]:
  path=download(archive["path"])
  if path.stat().st_size!=archive["bytes"] or digest(path)!=archive["sha256"]:raise ValueError("Archive hash/size mismatch: "+archive["path"])
  with zipfile.ZipFile(path) as z:
   if len(z.namelist())!=len(set(z.namelist())):raise ValueError("Duplicate archive entry")
   inner=json.loads(z.read("CHECKPOINT_ARCHIVE_MANIFEST.json"))
   subset={e["path"]:e for e in inner["files"]}
   if len(subset)!=len(inner["files"]):raise ValueError("Duplicate inner manifest entry")
   for e in inner["files"]:
    if expected.get(e["path"])!=e:raise ValueError("Inner/global manifest mismatch")
   payload_names={i.filename for i in z.infolist() if not i.is_dir() and i.filename!="CHECKPOINT_ARCHIVE_MANIFEST.json"}
   if payload_names!=set(subset):raise ValueError("Archive membership mismatch")
   for info in z.infolist():
    if info.filename=="CHECKPOINT_ARCHIVE_MANIFEST.json":continue
    rel=safe_rel(info.filename)
    if stat.S_ISLNK(info.external_attr>>16):raise ValueError("Symlink extraction not allowed")
    target=restored.joinpath(*rel.parts)
    if info.is_dir():
     if str(rel) not in manifest["empty_directories"]:raise ValueError("Unexpected directory")
     target.mkdir(parents=True,exist_ok=True);continue
    if info.filename in seen:raise ValueError("Overlapping archive payload")
    e=expected[info.filename]
    if info.file_size!=e["bytes"]:raise ValueError("Archive member size mismatch")
    target.parent.mkdir(parents=True,exist_ok=True)
    with z.open(info) as src,target.open("xb") as out:shutil.copyfileobj(src,out,1024*1024)
    if digest(target)!=e["sha256"]:raise ValueError("Extracted payload hash mismatch")
    target.chmod((info.external_attr>>16)&0o777 or 0o644)
    seen.add(info.filename)
 if seen!=set(expected):raise ValueError("Missing payload files.")
 for name in manifest["empty_directories"]:
  if not restored.joinpath(*safe_rel(name).parts).is_dir():raise ValueError("Missing empty directory")
 source=json.loads((restored/"recovery_metadata/source_manifest.json").read_text())
 receipt={
  "status":"EXTERNALLY_VERIFIED","checkpoint_id":index["checkpoint_id"],"data_commit":args.commit,
  "verified_at_utc":datetime.now(timezone.utc).isoformat(),"method":"Fresh HTTPS downloads into a new directory; archive SHA256 and size; safe extraction; every payload file checked against global and per-archive manifests.",
  "files_verified":len(seen),"bytes_verified":sum(e["bytes"] for e in manifest["files"]),
  "source_files_preserved":source["source_file_count"],"source_errors":source["errors"],
  "latents_verified":[e for e in manifest["files"] if e["path"].endswith("scene_codes.pt")],
  "empty_directories_verified":manifest["empty_directories"],"downloads":receipts,
  "experiments_run":False,"source_files_modified":False,
  "excluded_from_portable_backup":source["excluded"],
  "unprotected_in_scope_files":source["errors"],
  "limitations":"Downloaded upstream model weights and replaceable installed dependency caches are explicitly excluded. This verifies recovered bytes, not scientific correctness or current application readiness.",
 }
 (dest/"EXTERNAL_VERIFICATION.json").write_text(json.dumps(receipt,indent=2))
 print(json.dumps({"status":receipt["status"],"data_commit":args.commit,"files_verified":len(seen),"receipt":str(dest/"EXTERNAL_VERIFICATION.json")},indent=2),flush=True)
if __name__=="__main__":main()

