#!/usr/bin/env bash
set -euo pipefail

# Recovery-only preflight. No installation, generation, extraction, rebuild,
# deletion, checkout, reset, or modification of existing workspace files.
# A successful preflight is NOT a successful recovery or environment readiness.
if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'RECOVERY BLOCKED: python3 unavailable. Preserve the workspace; do not bootstrap dependencies before protecting existing results.' >&2
  exit 1
fi
python3 - <<'PY'
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

print("RECOVERY-ONLY PREFLIGHT: no setup/build/experiment will run.")
print(json.dumps({"cwd": os.getcwd()}))
targets = [
    "/workspace/research_decision_20261008",
    "/workspace/image_to_usable_car_probe_20261007",
    "/workspace/generated3d_authoring_clean_20261006",
    "/workspace/IMAGE_TO_USABLE_CAR_PROBE_20261007_evidence.zip",
    "/workspace/CVPR_3D",
]
read_errors = False
for name in targets:
    path = Path(name)
    row = {"path": name}
    try:
        info = path.lstat()
        row["state"] = "present"
        row["type"] = "symlink" if stat.S_ISLNK(info.st_mode) else "directory" if stat.S_ISDIR(info.st_mode) else "file"
        if stat.S_ISDIR(info.st_mode):
            with os.scandir(path) as entries:
                row["directory_read"] = "ok"
        elif stat.S_ISREG(info.st_mode):
            with path.open("rb") as stream:
                stream.read(1)
            row["file_read"] = "ok"
        else:
            row["read_status"] = "not_followed; inspect separately"
        row["meaning"] = "Presence/readability only; content and external backup NOT verified."
    except FileNotFoundError:
        row["state"] = "missing"
    except OSError as exc:
        read_errors = True
        row["state"] = "unreadable_or_io_error"
        row["error"] = str(exc)
    print(json.dumps(row, ensure_ascii=False))

repo = Path("/workspace/CVPR_3D")
if repo.is_dir():
    git_env = dict(os.environ)
    git_env["GIT_OPTIONAL_LOCKS"] = "0"
    git_env["GIT_PAGER"] = "cat"
    for args in [
        ["rev-parse", "--verify", "HEAD^{commit}"],
        ["status", "--porcelain=v1", "--untracked-files=all"],
        ["remote"],
    ]:
        try:
            completed = subprocess.run(
                ["git", "-C", str(repo), *args],
                env=git_env, capture_output=True, text=True, timeout=30,
            )
            print(json.dumps({
                "read_only_git_command": args,
                "returncode": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
            }, ensure_ascii=False))
            read_errors = read_errors or completed.returncode != 0
        except (OSError, subprocess.TimeoutExpired) as exc:
            read_errors = True
            print(json.dumps({"read_only_git_command": args, "error": str(exc)}))

print("LAST EXTERNALLY VERIFIED RECOVERY CHECKPOINT: research and supporting evidence, 813 payload files.")
print("Data commit: 42dc0ea31f75e8783bf1f208b8fb83d523ab076c")
print("Receipt commit: 8df00f1481b2e75741eb01e6c076315f9d60f6bb")
print("Receipt URL: https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/8df00f1481b2e75741eb01e6c076315f9d60f6bb/recovery_checkpoint_20261008/EXTERNAL_VERIFICATION.json")
print("All 401 research files and all three latents are covered at snapshot time; later changes need another checkpoint.")
print("Installed packages, downloaded model weights, credentials, VM state and live processes are excluded.")
print("Do not treat this preflight, saved configuration, a local archive, or a local commit as backup.")
print("NEXT: follow recovery-first start_skill; protect existing artifacts externally before any setup/build/re-run.")
print("Recovery status remains UNVERIFIED until external upload and independent read-back are checked.")
sys.exit(1 if read_errors else 0)
PY

