#!/usr/bin/env bash
set -euo pipefail

# Keep the selected checkout unchanged; unpack the working session beside it.
cd /workspace/CVPR_3D
sha256sum -c SHA256SUMS.txt
python3 - <<'PY'
import hashlib
import os
from pathlib import Path, PurePosixPath
import stat
import tempfile
from zipfile import ZipFile

workspace = Path('/workspace')
archive = workspace / 'CVPR_3D/Bentley_authoring_session.zip'
session_name = 'generated3d_authoring_clean_20261006'
session = workspace / session_name
archive_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
marker = session / 'environment/onboarding-archive.sha256'
if session.exists():
    if not marker.is_file() or marker.read_text().strip() != archive_hash:
        raise SystemExit('Existing session has no matching onboarding marker; preserve it and inspect before continuing.')
    print('Reusing existing session without extracting over local files.')
else:
    with tempfile.TemporaryDirectory(prefix='bentley-unpack-', dir=workspace) as tmp:
        with ZipFile(archive) as bundle:
            for entry in bundle.infolist():
                path = PurePosixPath(entry.filename)
                if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] != session_name:
                    raise SystemExit('Unsafe archive path: ' + entry.filename)
                mode = entry.external_attr >> 16
                if stat.S_ISLNK(mode):
                    raise SystemExit('Archive symlinks are not supported: ' + entry.filename)
            bundle.extractall(tmp)
        extracted = Path(tmp) / session_name
        lines = (extracted / 'PROVENANCE_SHA256SUMS.txt').read_text().splitlines()
        for line in lines:
            expected, relative = line.split('  ', 1)
            path = PurePosixPath(relative)
            if path.is_absolute() or '..' in path.parts:
                raise SystemExit('Unsafe manifest path: ' + relative)
            actual = hashlib.sha256((extracted / relative).read_bytes()).hexdigest()
            if actual != expected:
                raise SystemExit('Manifest checksum mismatch: ' + relative)
        print(f'Verified all {len(lines)} manifest checksums before installation.')
        (extracted / 'environment').mkdir(exist_ok=True)
        (extracted / 'environment/onboarding-archive.sha256').write_text(archive_hash + '\n')
        # zipfile does not restore executable mode; restore only the documented launcher.
        launcher = extracted / 'launch.sh'
        launcher.chmod(launcher.stat().st_mode | stat.S_IXUSR)
        os.rename(extracted, session)
PY

python3 -c 'import sys; assert sys.version_info[:2] == (3, 12), "Python 3.12 is required by the documented toolchain"'
node -e 'if (process.versions.node.split(".")[0] !== "24") throw new Error("Node 24 is required by the documented toolchain")'
command -v blender chromium >/dev/null
cd /workspace/generated3d_authoring_clean_20261006
mkdir -p environment/onboarding-logs environment/blender-config environment/chromium-cache
bash source/project/scripts/setup.sh
environment/venv/bin/python -m pip --cache-dir "$PWD/environment/pip-cache" check
git -C /workspace/CVPR_3D diff --exit-code

# Refresh the retained, completed car probe without repeating generation.
PROBE_ROOT=/workspace/image_to_usable_car_probe_20261007
if [[ -d "$PROBE_ROOT" ]]; then
  cd "$PROBE_ROOT"
  if [[ ! -x environment/venv/bin/python ]]; then
    bash source/setup_cpu.sh
    environment/venv/bin/python source/acquire_models.py
  fi
  environment/venv/bin/python -m pip check
  cd source/viewer
  NODE_PATH=/workspace/generated3d_authoring_clean_20261006/source/project/preview/node_modules \
    /workspace/generated3d_authoring_clean_20261006/source/project/preview/node_modules/.bin/esbuild \
    src/main.js --bundle --minify --sourcemap --outfile=dist/app.js --target=es2020
fi
git -C /workspace/CVPR_3D diff --exit-code

