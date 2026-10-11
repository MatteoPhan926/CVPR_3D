"""Partition all current payload files into two independently inspectable ZIPs.

Previous checkpoint archives/receipts remain separate; payload coverage is exact.
"""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
plan=ROOT/'config/FINAL_ARCHIVE_PLAN.json'
assert not plan.exists()
plan.write_text('{}\n')
files=sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and not p.is_symlink() and 'checkpoints' not in p.relative_to(ROOT).parts)
def main(name):
    return ('/' not in name or name.startswith(('config/','inputs/','source/','research/','logs/'))
       or name in ['artifacts/authoring_A_v1/car_door_authored.blend','artifacts/authoring_A_v1/car_door_authored.glb','artifacts/authoring_A_v1/authoring.json','artifacts/viewer/car_door_standalone.html','artifacts/viewer/car_door_standalone.build.json']
       or name.startswith('artifacts/reopened_A_v1/') and not name.endswith('.blend'))
groups={'05_final_delivery':[p for p in files if main(p)],'06_supporting_evidence':[p for p in files if not main(p)]}
assert len(set(sum(groups.values(),[])))==len(files)
plan.write_text(json.dumps({'all_non_checkpoint_files':len(files),'groups':groups,'recovery':'Extract both ZIPs into the same NEW directory. Each includes its own CHECKPOINT_CONTENTS.json; sidecar manifests distinguish groups. No original payload path overlaps. Prior checkpoints and final post-package receipts remain in Git.','excluded':['checkpoints/ (already immutable, separately indexed)','external installed dependencies/model weights','unexposed server-held state']},indent=2)+'\n')
for name,paths in groups.items():
    cmd=[sys.executable,str(ROOT/'source/checkpoint.py'),'pack',name]
    for p in paths:cmd.extend(['--include-prefix',p])
    subprocess.run(cmd,check=True)
    archive=ROOT/'checkpoints'/(name+'.zip')
    assert archive.stat().st_size<95*1024*1024,'Archive too large for planned Git delivery; preserve it and create a new grouping, do not delete.'
print(json.dumps({'payload_files':len(files),'groups':{n:len(p) for n,p in groups.items()}}))
