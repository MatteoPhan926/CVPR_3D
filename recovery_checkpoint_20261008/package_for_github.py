#!/usr/bin/env python3
import hashlib,json,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SNAP=ROOT/"snapshot"
DEST=Path("/workspace/CVPR_3D/recovery_checkpoint_20261008")
DEST.mkdir(exist_ok=False)
(DEST/"archives").mkdir()
(DEST/"evidence").mkdir()
manifest=json.loads((ROOT/"MANIFEST_SHA256.json").read_text())
groups={name:[] for name in ["01_research_generation","02_research_controls_and_holdouts","03_car_probe","04_dependency_source_and_metadata","05_bentley"]}
def group(rel):
 if rel.startswith("research_decision_20261008/generation_execution/"):return "01_research_generation"
 if rel.startswith("research_decision_20261008/"):return "02_research_controls_and_holdouts"
 if rel.startswith("image_to_usable_car_probe_20261007/environment/"):return "04_dependency_source_and_metadata"
 if rel.startswith("image_to_usable_car_probe_20261007/"):return "03_car_probe"
 if rel.startswith("generated3d_authoring_clean_20261006/"):return "05_bentley"
 return "04_dependency_source_and_metadata"
for e in manifest["files"]:groups[group(e["path"])].append(e)
def digest(p):return hashlib.file_digest(p.open("rb"),"sha256").hexdigest()
archives=[]
for name,entries in groups.items():
 p=DEST/"archives"/(name+".zip")
 with zipfile.ZipFile(p,"x",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for e in entries:z.write(SNAP/e["path"],arcname=e["path"])
  if name=="02_research_controls_and_holdouts":
   for d in manifest["empty_directories"]:z.writestr(d+"/",b"")
  z.writestr("CHECKPOINT_ARCHIVE_MANIFEST.json",json.dumps({"checkpoint_id":ROOT.name,"archive":p.name,"files":entries},indent=2))
 assert p.stat().st_size<90*1024*1024,(name,p.stat().st_size)
 archives.append({"path":"archives/"+p.name,"bytes":p.stat().st_size,"sha256":digest(p),"payload_files":len(entries),"role":name})
for name in ["MANIFEST_SHA256.json","source_manifest.json","preservation.log"]:
 shutil.copy2(ROOT/name,DEST/name)
shutil.copy2(ROOT/"preserve.py",DEST/"preserve.py")
shutil.copy2(Path(__file__),DEST/"package_for_github.py")
# Independently browsable evidence; large binary artifacts remain in complete ZIPs.
extensions={".py",".json",".md",".log",".tsv",".txt",".yaml",".yml",".sh",".html",".css",".js",".toml",".adoc"}
contact_names={"controlled_comparison.png","appearance_controls.png","hero_controls.png","selection_and_additions.png","selection_overlay.png","comparison.png"}
for e in manifest["files"]:
 rel=e["path"];p=SNAP/rel
 if rel.startswith("research_decision_20261008/") and (p.suffix in extensions or p.name in contact_names):
  target=DEST/"evidence"/p.relative_to(SNAP/"research_decision_20261008")
  target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
for name in ["configuration_snapshot.json","installed_versions.json","git_state_before_recovery.json"]:
 shutil.copy2(SNAP/"recovery_metadata"/name,DEST/name)
checkpoint={
 "checkpoint_id":ROOT.name,"status":"PREPARED_LOCAL_AWAITING_EXTERNAL_VERIFICATION",
 "base_commit":"6b99f54997c17e5d1f26bab89e1b2ecdaab2f838",
 "branch":ROOT.name,"archives":archives,"manifest":"MANIFEST_SHA256.json",
 "source_file_count":808,"payload_file_count":manifest["payload_file_count"],
 "research_scope":"All files found under research_decision_20261008, without rerunning any experiment.",
 "all_three_latents_included":True,
 "excluded":"See source_manifest.json. Installed dependencies and upstream model caches omitted; generated mesh arrays and latents included.",
 "last_known_external_checkpoint":"Old car probe at base_commit; this checkpoint still requires upload and read-back.",
 "verification_receipt":"See EXTERNAL_VERIFICATION.json when published. This initial checkpoint status records packaging time and is not modified retroactively."
}
(DEST/"CHECKPOINT.json").write_text(json.dumps(checkpoint,indent=2))
print(json.dumps({"directory":str(DEST),"archives":archives},indent=2))

