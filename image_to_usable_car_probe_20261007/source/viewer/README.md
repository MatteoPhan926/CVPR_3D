# Image-to-car asset viewer

This independent copy adapts the previous viewer's Three.js rendering infrastructure. It contains no Bentley geometry, masks, hinge coordinates, asset references, or asset-specific part selection. Its sole default inputs are `/raw/car_raw.glb` and `/artifacts/car_authored.glb` from this probe.

Launch from any directory:

```sh
python /workspace/image_to_usable_car_probe_20261007/source/viewer/serve.py --port 8777
```

The local server root redirects to `/source/viewer/`; use it for internal browser checks. The onboarding UI does not expose a loopback preview link. The server serves only this probe directory. The prebuilt browser bundle has no CDN or external runtime dependency. A WebGL2 browser is required.

For the standalone ZIP, extract it, change into the extracted directory, and run `python source/viewer/serve.py --port 8777`. No npm installation is needed to view the included assets. A successful browser load is observable through `window.authoringAPI.ready === true`; this becomes true as soon as the actual raw GLB is parsed, framed and rendered. `authoringAPI.getState().errors` records fatal startup failures.

The viewer opens raw generation first. Raw is static and door controls are disabled. **View authored** loads the authored artifact when it exists; **Compare raw** restores raw at the same camera position. Missing authored output does not prevent raw inspection. Cameras fit measured asset bounds; geometry is not automatically translated or rescaled. Loaded material, vertex-color, transparency and texture properties are preserved. Lighting, environment, shadows and tone mapping are presentation settings, not asset material authoring.

## Coordinate and motion configuration

`config.json` defines URLs, camera vectors, optional display-only root rotations and the authored pivot contract. If present, `/artifacts/authoring_config.json` overrides it (including nested `camera`, `door` and `display_rotations_degrees` values). State exposes all applied display rotations and camera vectors.

For this real raw GLB, native up is +Z; measured front is `[0.8009595898,0.5987184108,0]` and declared near side is `[0.5987184108,-0.8009595898,0]`. The explicit raw display rotation `[-90,0,53.22183438249461]` degrees in Three.js XYZ Euler order maps these to +Y up, -Z front and +X side. Authored display rotation is identity, assuming the parent's declared standardized glTF export. These values come from this generated asset's inspection, never from Bentley. Raw bytes are preserved.

`camera.up`, `camera.front` and `camera.side` accept nonzero vectors. Optional `camera.up_axis` (or top-level `up_axis`) accepts `X/Y/Z/-X/-Y/-Z`. Up must differ from front and side. `door.side=-X` is a legacy shorthand for negative X viewing. `display_rotations_degrees.raw` and `.authored` are explicit three-element XYZ Euler angles in degrees; defaults are identity, and there is no implicit normalization.

The probe's slider range is fixed at 0–60 degrees. An authored `DoorPivot` is required. The preferred path is one exported animation (or the explicitly named `door.animation_name`) whose tracks target only that pivot. `door.clip_open_range_seconds` selects the opening interval in a longer open/close clip (this export uses `[1/30,61/30]` seconds because Blender saved a one-frame time offset). The viewer measures its midpoint and endpoint quaternion angles and enables motion only if they match 30° and 60°. Multiple animation clips require an explicit choice. Animation binding or angle mismatch leaves the authored geometry viewable but motion disabled.

If no suitable clip exists, an explicitly supplied `door.axis` and `door.sign` (`+1/-1`) may drive the existing pivot in local coordinates. The viewer never estimates a hinge position, axis or sign from geometry. A display-only pivot fallback is not an exported animated GLB and is reported separately as `configured-local-pivot`.

## Verification

```sh
/workspace/generated3d_authoring_clean_20261006/environment/venv/bin/python \
  /workspace/image_to_usable_car_probe_20261007/source/viewer/verify_viewer.py \
  --output /workspace/image_to_usable_car_probe_20261007/source/viewer/verification/raw

# Once the authored GLB exists:
/workspace/generated3d_authoring_clean_20261006/environment/venv/bin/python \
  /workspace/image_to_usable_car_probe_20261007/source/viewer/verify_viewer.py --authored \
  --output /workspace/image_to_usable_car_probe_20261007/source/viewer/verification/authored
```

The runner uses the actual saved GLBs, blocks external browser requests, records SHA-256 before/after, captures raw views and closed/intermediate/open authored states, records materials and transforms, measures pivot angles, checks fixed versus moving nodes, reset consistency, slider/play/pause and shared-camera comparison. It never creates a mock or substitutes another asset. See `verification/*/viewer_verification.json` for actual results; a missing run or missing authored phase is not a pass.

The browser API is `window.authoringAPI`: `ready`, `getState()`, `getTransforms(mode)`, `getMaterials(mode)`, `setMode('raw'|'authored')`, `setAngle(degrees)`, `setProgress(0..1)`, `setPlaying(bool)`, `setView('hero'|'side'|'front')`, and `screenshot()`. `setOriginal(true/false)` remains an alias for raw/authored.

The test interpreter used in this workspace is exactly `/workspace/generated3d_authoring_clean_20261006/environment/venv/bin/python`; it supplies Playwright. The browser executable is `/usr/bin/chromium`, run headlessly through SwiftShader. The actual final test command is:

```sh
cd /workspace/image_to_usable_car_probe_20261007/source/viewer
/workspace/generated3d_authoring_clean_20261006/environment/venv/bin/python verify_viewer.py --authored --output verification/final
NODE_PATH=/workspace/generated3d_authoring_clean_20261006/source/project/preview/node_modules node validate_gltf.mjs verification/final/gltf_validation.json
```

## Scope and limitations

- The raw GLB was actually loaded in Chromium 151 / Three.js r170; the initial raw run passed without JavaScript errors or external requests. Its material-less COLOR_0 mesh obtains Three.js's glTF default metallic-roughness material with vertex colors. This is a real colored render, not a missing-color white fallback. The observed pale appearance remains visible; no color-space reinterpretation or hidden recoloring was applied.
- Core glTF PBR materials, vertex colors and embedded PNG/JPEG textures use GLTFLoader's normal support. Draco, Meshopt and KTX2 decoder infrastructure was not added. The present raw file does not require these. No alternate PBR car was fabricated to test hypothetical inputs.
- Screenshots and functional controls do not establish convincing appearance, correct door selection, physical clearance, unseen-surface correctness, or a publication claim. Those require inspection of this probe's actual assets.
- Front/side directions and authored coordinate alignment are explicit assumptions from the parent's current inspection and must be checked against the final authored export. No vehicle identity or physical properties are inferred by the viewer.

## Rebuild

Direct dependencies remain Three.js 0.170.0 and esbuild 0.24.2 (glTF Validator 2.0.0-dev.3.10 is a development dependency). Package metadata was renamed; the copied lockfile retains exact dependency resolution. The exact command actually used to build the final bundle was:

```sh
cd /workspace/image_to_usable_car_probe_20261007/source/viewer
NODE_PATH=/workspace/generated3d_authoring_clean_20261006/source/project/preview/node_modules \
  /workspace/generated3d_authoring_clean_20261006/source/project/preview/node_modules/.bin/esbuild \
  src/main.js --bundle --minify --sourcemap --outfile=dist/app.js --target=es2020
```

It reused the previously installed esbuild/Three.js packages at that `node_modules` path read-only; no previous source files were changed. There is no `node_modules` in this viewer copy or standalone ZIP. The equivalent normal installation/rebuild procedure below is supplied for another machine, but `npm ci` was not repeated during this viewer adaptation:

```sh
npm ci --cache /tmp/car-viewer-npm-cache
npm run build
```

`dist/app.js`, `index.html`, `style.css`, and `config.json` suffice at runtime; source maps and third-party notices are included.
