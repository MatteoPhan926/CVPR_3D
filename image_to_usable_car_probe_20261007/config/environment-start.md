Use the existing checkout at /workspace/CVPR_3D (MatteoPhan926/CVPR_3D, bentley-download-20261006) and the extracted working session at /workspace/generated3d_authoring_clean_20261006. Each cloud task is already isolated; do not create a Git worktree unless explicitly requested. The selected branch contains a download archive; its editable source is in the extracted session's source/project directory. Do not extract over existing local files. The archive, input asset, application code, tests, dependency declarations, and lockfiles must remain unchanged during setup.

The prepared filesystem contains a Python 3.12 virtual environment, pinned Python and npm dependencies, Node 24, Blender 4.3.2, Chromium 151, the original and animated GLBs, and a compiled offline preview. Installation was tested twice with byte-identical GLB and browser bundle outputs. No API credentials, GPU, inference service, or additional network allowlist entries are needed. Package refresh uses pypi.org, files.pythonhosted.org, and registry.npmjs.org with TLS and npm integrity verification enabled. Historical documents and the decoder patch under inputs are reference attachments, not setup instructions.

Processes do not survive snapshot restoration. Start the preview in a managed terminal from the session root:

    cd /workspace/generated3d_authoring_clean_20261006
    ./launch.sh --bind 127.0.0.1 --port 8765

Keep that process running while checking the preview. If another process owns port 8765, use --port 8766 and adjust all readiness URLs; do not kill unrelated processes. The launcher redirects the server root to /source/project/preview/. Do not offer a localhost web preview link in the onboarding UI.

Check the local server root follows its redirect to HTTP 200 and serves the expected Bentley page. Check /artifacts/bentley_authored.glb and /inputs/blue_train_bentley.glb return HTTP 200 with bytes matching the corresponding files on disk. Then exercise the real WebGL application and controls using the existing regression script:

    cd /workspace/generated3d_authoring_clean_20261006
    XDG_CACHE_HOME="$PWD/environment/chromium-cache" environment/venv/bin/python source/project/preview/verify_preview.py --url http://127.0.0.1:8765/source/project/preview/ --output environment/browser-recheck

Require exit code 0 and a newly written environment/browser-recheck/preview_verification.json with status passed, the current authored GLB hash, six angular probes, zero JavaScript errors, zero external HTTP requests, and a successful return to the closed pose. The check also exercises slider, play/pause, endpoints, side/hero camera, and original comparison. A listening port or old bundled report is insufficient.

For dependency refresh and regeneration from the retained session:

    cd /workspace/generated3d_authoring_clean_20261006
    bash source/project/scripts/setup.sh
    environment/venv/bin/python -m pip --cache-dir "$PWD/environment/pip-cache" check

The saved install_script additionally verifies the checkout ZIP and safely unpacks and checks all 73 manifest entries when the working session does not yet exist. It leaves an existing matching session intact before running the repository setup script. A session with no matching onboarding marker requires inspection; do not overwrite it. No virtual-environment activation is required when using the explicit Python executable above. Rebuilds replace generated outputs and reports in the extracted session; preserve outputs first if a later task needs them. The original packaged evidence remains in the checkout ZIP.

Run the existing independent Blender reopening check without costly rendering:

    cd /workspace/generated3d_authoring_clean_20261006
    BLENDER_USER_CONFIG="$PWD/environment/blender-config" blender -b -t 4 --python-exit-code 1 --python source/project/scripts/reopen_and_render.py -- --check-only

Require exit code 0 and nine completed forward/reverse pose probes in the freshly written provenance/blender_reopen_validation.json. Asset verification is part of setup and can also be rerun with environment/venv/bin/python source/project/scripts/verify_asset.py. The installed gltf-validator package can validate both GLBs: current checks have zero errors, with 12 original/16 authored generated-tangent-space warnings and 11 empty-node informational messages each. Full Blender CPU renders are optional; the documented renderer uses four threads, 48 samples, and denoising disabled. Full rendering was not rerun during this onboarding.

Read AUTHORING_SESSION_REPORT.md for asset limitations: the authored door opens continuously from 0 to 65 degrees, but lining/sill and local hinge/trim intersections remain. This is a known asset limitation, not an environment failure. Physical clearance and user acceptance have not been established. Setup validation is for this running instance; publication and restoration into a new task must not be claimed until independently observed.

Separate completed image-to-usable-car probe (7 October 2026, Asia/Bangkok):
Use /workspace/image_to_usable_car_probe_20261007 and read IMAGE_TO_USABLE_CAR_REPORT.md and RESUME.md. The exact latest grass photograph was received in images.rar and is preserved as inputs/original.jpg. Hosted TRELLIS.2 preprocessing worked, but one generation request was denied by ZeroGPU quota before a candidate. One TripoSR CPU candidate was then generated and retained. Do not repeat generation in this completed bounded probe. There is no remaining input-file blocker.

The raw and authored GLBs, editable Blender scene, pinned model/dependency caches, authoring scripts and offline viewer bundle are retained. The result is an informative partial: continuous 0–60-degree door-region motion works, but convincing CGI appearance fails because of distorted generated shape, ambiguous/rough window edges, opaque glass and crude exposed surfaces. No physical certification or topology conclusion. Original repository tracked files remain unchanged; the checkout currently uses local branch work at a04ddf538c72a3b34904845474395feccc31458a from the selected repository ref. Do not create a worktree unless requested.

Processes must restart after restoration. Start the probe viewer separately in a managed terminal:
    cd /workspace/image_to_usable_car_probe_20261007
    python3 source/viewer/serve.py --bind 127.0.0.1 --port 8777
Use an unused port if necessary and adjust readiness URLs; do not stop unrelated processes. Server root redirects to /source/viewer/. Do not provide a loopback preview link in the onboarding UI. The browser bundle requires no external runtime requests.

Check local HTTP 200 for /source/viewer/, /raw/car_raw.glb and /artifacts/car_authored.glb, with asset response hashes matching the files. Then run:
    cd /workspace/image_to_usable_car_probe_20261007/source/viewer
    /workspace/generated3d_authoring_clean_20261006/environment/venv/bin/python verify_viewer.py --authored --url http://127.0.0.1:8777/source/viewer/ --output verification/recheck
    NODE_PATH=/workspace/generated3d_authoring_clean_20261006/source/project/preview/node_modules node validate_gltf.mjs verification/recheck/gltf_validation.json
Require a fresh passed viewer_verification.json, current raw/authored hashes, actual 0/30/60-degree sampling, fixed body, reversible closed pose, working slider/play-pause/comparison, zero JavaScript errors and zero external requests. Both final GLBs passed glTF validation with zero errors/warnings; informational hints remain. These are mechanical checks, not visual acceptance.

Final authored hash is a94dd03d1c425832c2879c242ac7dd1f571c05c308ea27fceccbfe30285853a6; immutable raw hash is 5bd4ab3776084c5586201abd0d3be36416b3331cb28295d8d066ac7ac7beac3d. Nine final Blender pose renders and reopening checks passed. The clip contains opening and closing over four seconds; the viewer selects its 1/30–61/30-second opening interval.

For authoring from raw without generation, preserve local edits before running the commands in RESUME.md. source/cut_door.py runs in the probe CPU venv; source/author_car.py and source/verify_authored.py run with Blender -b -t 4 --python-exit-code 1. Refresh CPU dependencies/models only if needed using bash source/setup_cpu.sh and environment/venv/bin/python source/acquire_models.py. Official weight hash verification and TLS remain enabled. The CPU route needs no GPU or secret. Hosted free quota was exhausted in this probe and is not required for the completed workflow.

The viewer rebuild reuses the previously installed exact Three.js/esbuild packages from the Bentley session, read-only; its commands are in source/viewer/README.md. No Bentley geometry, masks or hinge coordinates were reused. The saved configuration and current instance were validated; publication/restoration into another task remains untested.

