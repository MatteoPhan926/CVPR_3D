#!/usr/bin/env bash
set -euo pipefail
PROBE_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$PROBE_ROOT/environment/pip-cache" "$PROBE_ROOT/environment/dependencies"
python3 -m venv "$PROBE_ROOT/environment/venv"
PROBE_PY="$PROBE_ROOT/environment/venv/bin/python"
export PIP_CACHE_DIR="$PROBE_ROOT/environment/pip-cache"
export HF_HOME="$PROBE_ROOT/environment/huggingface-cache"
export XDG_CACHE_HOME="$PROBE_ROOT/environment/cache"
export U2NET_HOME="$PROBE_ROOT/environment/rembg-cache"
export PATH="$PROBE_ROOT/environment/venv/bin:$PATH"
export CMAKE_BUILD_PARALLEL_LEVEL=2
export MAX_JOBS=2
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++

fetch_dependency() {
    local url="$1" destination="$2" revision="$3"
    if [[ ! -d "$destination" ]]; then
        git clone --no-checkout "$url" "$destination"
        git -C "$destination" checkout --detach "$revision"
    fi
    [[ "$(git -C "$destination" rev-parse HEAD)" == "$revision" ]] || {
        echo "Existing dependency checkout differs; preserve it and inspect: $destination" >&2
        return 1
    }
    git -C "$destination" diff --exit-code
}

fetch_dependency https://github.com/VAST-AI-Research/TripoSR.git "$PROBE_ROOT/environment/dependencies/TripoSR" 107cefdc244c39106fa830359024f6a2f1c78871
fetch_dependency https://github.com/tatsy/torchmcubes.git "$PROBE_ROOT/environment/dependencies/torchmcubes" 879926d0ef58e6ce0ac2630fdecb5e53af7ed3ff

"$PROBE_PY" -m pip install --disable-pip-version-check --index-url https://download.pytorch.org/whl/cpu 'torch==2.5.1+cpu'
"$PROBE_PY" -m pip install --disable-pip-version-check -r "$PROBE_ROOT/config/requirements-cli.in"
"$PROBE_PY" -m pip install --disable-pip-version-check --no-build-isolation "$PROBE_ROOT/environment/dependencies/torchmcubes"
"$PROBE_PY" -m pip check
"$PROBE_PY" -m pip freeze > "$PROBE_ROOT/config/installed-cpu-packages.txt"
cd "$PROBE_ROOT/environment/dependencies/TripoSR"
"$PROBE_PY" run.py --help
