# Authoring session — Blue Train Bentley

Date: 6 October 2026 (Asia/Bangkok). Workspace: `generated3d_authoring_clean_20261006`.

## Result

A launchable offline preview and an animated GLB turn the supplied static Bentley into a virtual object with one continuously opening cabin door. The control spans 0–65 degrees; glass, mirror, handles, trim and interior lining move together. The remainder of the car stays fixed. Original materials and all 24 embedded image payloads are preserved exactly. The export was reopened and exercised in both Blender and Chromium/Three.js.

Run `./launch.sh` from the session root. It serves the preview on port 8765; the server root opens the application. Python 3 and a WebGL2 browser are sufficient for the bundled result. `README.md` includes rebuilding and validation commands.

The core visual-authoring task is complete. Physical clearance is incomplete: original interior lining intersects the sill during partial opening, and local rear trim/hinge surfaces intersect near the hinge. User acceptance remains unassessed until the user inspects the result. No novelty assessment, estimator reopening or CVPR contribution claim is made.

## Isolation, inputs and provenance

A fresh HTTPS clone of `MatteoPhan926/CVPR_3D` was created at `source/project`. The upstream repository was empty. The authored source is now a local commit, `d55cdbc55ac4847e8e4ed5e4944e4c02dd1c0431`; it was not pushed. `provenance/source.bundle` preserves that complete local history. Package sources can be used directly; `git clone provenance/source.bundle recovered_source` recovers the revision.

The session has its own Python virtual environment, npm dependencies, caches, Blender configuration directory, outputs and logs. This is application/dependency isolation on the supplied cloud host; a separate VM was not provisioned. The old `/workspace/CVPR_3D` checkout and uploaded originals were not modified. All four uploaded files and their read-only session copies were rehashed successfully.

The sole execution input is `inputs/blue_train_bentley.glb`, 25,976,404 bytes, SHA-256:

`a1156efc2aa8aca3c37eef570b1ca7c3d8cf3676a5f6e07e2d059154af2edd79`

Final export SHA-256:

`565f0d8ce70c1f6bf23ca370bb879e2d0a167b24d7381cae0bf75dff1b44ac14`

The discovery document, old reproduction report and chunking patch were retained only as reference attachments and hashed. The old report/patch were not execution instructions, applied patches or prerequisites. No historical mutable source tree, checkpoint, orientation, asset path or scientific conclusion was reused. No prediction or model inference ran. The asset's original generator metadata identifies Khronos glTF Blender I/O v4.3.47; no upstream asset-author identity was supplied.

## Intentions and disclosed authoring edits

`AUTHORING_INTENT.md` was written before viewing predictions or authored motion. The intended moving part was one visible cabin door; all remaining vehicle parts were fixed. An initial provisional forward hinge was revised after inspecting the original rest geometry: the handle is toward the front and the model has rear hinge barrels. The selected side is Blender +X, with front −Y and up +Z. These axes were established from this asset alone.

Manual geometry inspection identified existing door glass, mirror, handles, lining and trim components. Large body triangles crossed the visible door seam, so whole-component separation alone was insufficient. The implementation clips the relevant body, interior and long trim triangles to a contour derived from existing trim. New boundary vertices interpolate source UVs and normals. It retains the complete roof-rail cross section between the front and rear door boundaries. No generated replacement geometry, texture generation, recoloring, new interior proxy or model training was used.

The convex cut approximates the front trim curve by at most 0.009409 original coordinate units. Physical scale was not independently established. Source units and geometry were retained. The lining's existing lower overhang was retained, which contributes to the clearance limitation below.

The chosen rear hinge passes through modeled barrel centers `(0.6551, 0.8555, 0.6477)` and `(0.6221, 0.8555, 1.2831)` in Blender coordinates, about 2.97 degrees from vertical. This is an authored alignment of visual hardware, not recovered physical ground truth. `source/project/authoring_config.json` records both Blender and glTF coordinates; `selection.json` records exact source triangle selections and clipping regions.

The final GLB contains four moving material meshes under `DoorPivot`, twelve fixed meshes, and one two-second rotation animation. Any intermediate opening is supported, and reversing the clip closes it.

## What ran and what was corrected

- Fresh clone and isolated Python/npm setup; pinned tools and dependencies are recorded in `provenance/toolchain.json`, `requirements-lock.txt` and `preview/package-lock.json`.
- Blender rest inspection, connected-component analysis and renders. All twelve original GLB triangle index sequences were checked against Blender polygon indices and coordinates: exact match, maximum difference 0.
- Direct GLB triangle partitioning, UV/normal interpolation, hinge parenting and animation export.
- Khronos glTF Validator on both input and output; material/image, surface-area and animation checks on the written output.
- Independent Blender reimport and stored-animation evaluation, then independent Chromium/Three.js loading and UI testing.
- Surface-triangle intersection diagnostics and an independent geometry review of open/intermediate renders.
- Full setup refresh, which exited 0 in 5.76 seconds and reproduced a byte-identical GLB.

The first Blender render failed because this build lacks OpenImageDenoise. Rendering was rerun with denoising off; geometry and package/TLS verification were unaffected. Final renders use Cycles CPU, four threads and 48 samples.

The first two-key quaternion clip exposed a Blender interpolation difference: at 10% time Blender showed 6.2487 degrees instead of 6.5. Exporting 66 rotation keys at one-degree intervals resolved the measured discrepancy. This fresh export adaptation is independent of the historical chunking patch. Two exactly zero-area triangles introduced by float32 rounding at cut boundaries were removed. Neither change alters the intended rest appearance or rigid path.

No GPU device is exposed on this host. Authoring, rendering and headless-browser testing used CPU, so the 8,188 MiB VRAM constraint was not approached. The final setup refresh's maximum child RSS was about 131 MiB; Blender reported roughly 323 MiB peak during rendering. These are process observations, not a complete system-memory benchmark. No paid service, training or replacement generation was used.

## Verification evidence

| Check | Observed result |
|---|---|
| Original GLB validation | 0 errors; 12 generated-tangent-space warnings |
| Final GLB validation | 0 errors; 16 warnings of the same tangent-space type, one per final primitive; 11 inherited empty-node information messages |
| Texture/material preservation | All 24 image byte payloads, material definitions, textures and samplers identical |
| Unedited geometry | All attributes and indices of eight wholly untouched original meshes identical |
| Surface conservation | Maximum per-material area difference in the actual exported geometry: 2.99×10⁻⁹ model-units² |
| Rotation keys | 66 unit-quaternion keys, 0–2 seconds, 0–65 degrees |
| Blender reopening | Nine forward/reverse pose probes passed; angle errors below 0.001°; fixed transform difference 0 |
| Browser reopening | Six nonzero angle probes passed, maximum error about 0.0000016°; all twelve fixed meshes unchanged; exact return-to-closed transform reset |
| Browser controls | Slider, play/pause, endpoints, camera presets/reset and original comparison passed |
| Browser runtime | No JavaScript errors or external HTTP requests |
| Original versus authored closed view | Identical camera; mean absolute RGB difference 0.0039904/255; 0.0323% of viewport pixels differed by more than two levels |
| Setup repeatability | Exit 0; output SHA-256 identical before and after refresh |

The small closed-view image differences are confined to a very small fraction of pixels and are consistent with retriangulation/shading precision; they are measured differences, not a claim of pixel identity. `provenance/preview_verification.json` and `blender_reopen_validation.json` record the exact final GLB hash. Detailed checks, not just successful process startup, support these results.

## Remaining operation

A collision-free solid mechanism has not been produced. At 65 degrees, 112 triangle crossing pairs remain, all within 0.011911 original coordinate units of the rear hinge line, involving original barrels, rear trim and adjoining belt strips. There are no main door panel, glass or lining crossings at that endpoint.

At intermediate angles the retained original lining intersects the sill/lower body. At 32.5 degrees, 32 lining/body crossing pairs occur near the lower rear edge; at 45 degrees, 22 remain. The precise bounds and component IDs are recorded in `provenance/OPEN_PREVIEW_REVIEW.md` and `intersection_point_bounds.json`. These are actual local triangle crossings, not merely overlapping bounding boxes.

If physical clearance is needed, the next concrete operation is to trim or remodel the low-angle lining/sill region and rear hinge/trim clearances with explicit thickness, then rerun the sweep. The current pivot is retained because it aligns with visible hardware and the reviewed views show a coherent visual articulation. No force model, collision response, watertightness or physical accuracy is claimed. This limitation does not prevent launching or controlling the delivered preview.

## Time accounting and checkpoint

Initial recorded setup ran from 06:52:42 to 06:55:25 Asia/Bangkok, about 2 minutes 42 seconds; initial attachment transfer/inspection preceded that timer. Authoring began at 06:55:25. The first independent reopened renders completed at 07:03:44, about 8 minutes 19 seconds after that authoring start. Dependency installation overlapped the first part of this interval.

The conversation then had a long gap before the user requested continuation. Final verification and packaging resumed in a later activity window around 10:55. The total timestamp span must not be treated as continuous authoring work. End-to-end active agent time was not reliably measured, and no human labor was timed. A separate setup refresh took 5.76 seconds, as recorded above.

At the requested approximately 90-minute exploration checkpoint, the appropriate decision is already clear: retain and deliver the working visual result, with the precise clearance limitation recorded. This was not a continuous 90-minute reproduction run. No extra search or historical research task was opened to consume that budget.

## Delivery and reusable configuration

The compact archive includes the original and animated GLBs, browser before/closed/half/open images, an independent Blender open render, launch script, source/configuration, dependency locks, source Git bundle, provenance and this report. Large environment caches, node_modules and temporary Blender inspection files are excluded. The full working directory retains additional diagnostic renders and editable inspection state.

Reusable `install_script` and `start_skill` fields were saved successfully in the cloud environment draft. They reproduce/refresh dependencies and the model, start the preview, and specify functional readiness checks. No secret or network-policy change was required. Saving the draft did not publish an environment. Review and save it in environment settings, then publish if you want a reusable cloud snapshot. Restoration in a new task has not been independently verified; the source bundle also preserves the local-only revision explicitly.

**User acceptance: unassessed.**
