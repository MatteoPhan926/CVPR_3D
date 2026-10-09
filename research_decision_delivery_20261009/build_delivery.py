#!/usr/bin/env python3
"""Package the final report and selected existing evidence, without experiments."""
import hashlib,json,re,zipfile
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent
ARCHIVE="RESEARCH_DECISION_OUTPUT_20261009.zip"
def sha(p):
 with p.open("rb") as stream:return hashlib.file_digest(stream,"sha256").hexdigest()
def main():
 sources=json.loads((ROOT/"SOURCE_FILES_SHA256.json").read_text())["copied_files"]
 for e in sources:
  assert sha(ROOT/e["path"])==e["sha256"],e["path"]
  assert sha(Path(e["source_path"]))==e["sha256"],e["source_path"]
 for p in ROOT.glob("*.md"):
  for raw in re.findall(r"\]\(([^)]+)\)",p.read_text()):
   target=raw.split("#",1)[0]
   if not target or "://" in target:continue
   assert (p.parent/target).exists(),(p.name,target)
 omitted={ARCHIVE,"DELIVERY_MANIFEST.json","DELIVERY_PACKAGE.json","DELIVERY_VERIFICATION.json","DELIVERY_VERIFICATION.log"}
 files=[{"path":p.relative_to(ROOT).as_posix(),"bytes":p.stat().st_size,"sha256":sha(p)} for p in sorted(ROOT.rglob("*")) if p.is_file() and p.name not in omitted]
 manifest={"package":"research_decision_delivery_20261009","created_at_utc":datetime.now(timezone.utc).isoformat(),"scope":"Final research-decision report, secretary handoff, derived arithmetic, independent reviews, selected verbatim evidence and immutable full-artifact download index.","full_artifacts_included":False,"full_artifact_index":"FULL_EVIDENCE.json","payload_files":files,"source_files_checked":len(sources),"experiments_rerun":False}
 with (ROOT/"DELIVERY_MANIFEST.json").open("x") as f:json.dump(manifest,f,indent=2)
 with zipfile.ZipFile(ROOT/ARCHIVE,"x",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for e in files:z.write(ROOT/e["path"],arcname=ROOT.name+"/"+e["path"])
  z.write(ROOT/"DELIVERY_MANIFEST.json",arcname=ROOT.name+"/DELIVERY_MANIFEST.json")
 with zipfile.ZipFile(ROOT/ARCHIVE) as z:
  for e in files:assert hashlib.sha256(z.read(ROOT.name+"/"+e["path"])).hexdigest()==e["sha256"],e["path"]
 summary={"status_at_creation":"LOCAL_PACKAGED_AWAITING_EXTERNAL_READBACK","archive":ARCHIVE,"bytes":(ROOT/ARCHIVE).stat().st_size,"sha256":sha(ROOT/ARCHIVE),"payload_file_count":len(files),"manifest_sha256":sha(ROOT/"DELIVERY_MANIFEST.json"),"external_verification":"See DELIVERY_VERIFICATION.json in the published branch after read-back.","baseline_recovery_commit":"5c72b2bf61b00af67ace1ebd11bbda03d3015095"}
 with (ROOT/"DELIVERY_PACKAGE.json").open("x") as f:json.dump(summary,f,indent=2)
 print(json.dumps(summary,indent=2))
if __name__=="__main__":main()

