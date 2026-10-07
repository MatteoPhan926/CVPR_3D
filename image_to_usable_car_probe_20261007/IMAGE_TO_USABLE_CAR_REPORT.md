# Image → usable car probe

7 October 2026 (UTC). **Completed: informative partial result.** The supplied photograph produced a raw GLB, and an authored copy has a reversible 0–60° front-door-region animation and a working comparison viewer. **The declared convincing CGI asset target was not met.** The output remains visibly distorted, and the cut/window edges and exposed cabin are crude.

The most consequential finding is that this one accessible CPU generation already has substantial appearance deficits before door authoring. Controllable motion is achievable, but successful motion alone does not make this candidate a convincing car. This does not establish a topology bottleneck, failure of TRELLIS.2, or a CVPR contribution.

## Input and generation

The exact `images.jpg` from the user's `images.rar` is preserved as [original.jpg](inputs/original.jpg): 516×387 RGB, SHA-256 `b5b9ed4aece1359a0d291e89149634499583102e27f177aadb4c60f327e996e1`. It is the latest grass photograph, replacing the earlier road photograph before inference. Original bytes, the archive, normal cutouts/composites, and preprocessing review records are retained. No manual mask correction or substitute car was used.

This host has five logical CPUs, about 33 GiB RAM and no NVIDIA GPU. Local TRELLIS.2 was infeasible. One official hosted TRELLIS.2 request, after successful inspected preprocessing, was rejected by ZeroGPU quota before any candidate was produced. Its exact error is in [the hosted attempt](raw/hosted-attempt001/attempt.json); no retry or paid service followed. TRELLIS.2 asset quality was therefore **not tested**.

The predeclared accessible fallback was TripoSR CPU: source `107cefdc244c39106fa830359024f6a2f1c78871`, model revision `5b521936b01fbe1890f6f9baed0254ab6351c04a`, publisher-checksum-verified weights, seed 42, four CPU threads, marching-cubes resolution 256, chunk size 4096, vertex colors. Standard U2Net/rembg, foreground ratio 0.85 and gray composite were inspected before inference. **Exactly one successful generated candidate** was retained; no favorable-output selection, training or generation retry. [Actual execution record](raw/cpu-attempt001/attempt.json): 12.64 s inference + 29.83 s extraction = 42.47 s; peak process RSS about 3881 MiB. Runtime is not human labor.

[Raw GLB](raw/car_raw.glb) has 53,904 vertices and 107,608 triangles; SHA-256 `5bd4ab3776084c5586201abd0d3be36416b3331cb28295d8d066ac7ac7beac3d`. Its five components/non-watertightness are numerical observations, not an established cause of task failure. Roof terracing, warped wheels/body, smeared grille/trim and ambiguous window/door boundaries are visible across views. There is no recovered usable interior.

## Bounded authoring

[Intent](config/AUTHORING_INTENT.md) was recorded before authoring: camera-facing front cabin door, 0/30/60° poses, whole-car three-quarter/side and exposed-interior close-up. A new asset-specific contour and rear-edge pivot partitioned the generated surface. No Bentley geometry, masks or hinge coordinates were transferred. The original raw bytes remain unchanged. The cut conserves source surface area within floating-point tolerance; this does not validate semantic door selection or clearance.

Added work: opaque offset inner skin, edge thickness, recessed jamb strips and four simple cabin/seat proxies; an explicit vertex-color PBR material; smoothed exterior normals; animation and viewer controls. Raw RGB values were not repainted. Generated glass remains opaque. The first proxy layout visibly protruded through the windshield/lower silhouette; **one local revision** reduced/repositioned those boxes. Both authored versions and failed checks are retained. The approximate cut still gives ragged window/front-edge boundaries, visible surface interference around the window/windshield, a gap below the cabin completion and unconvincing exposed surfaces. Door semantics, glass/frame fidelity and realistic fit are not solved by this demonstration.

The viewer uses raw glTF defaults (metallic=1, roughness=1, flat shading when NORMAL is absent), with explicit display-only axis alignment. Authored material keeps those PBR values but adds smooth normals. Earlier Blender raw-inspection images used a display material with metallic=0/roughness=0.8 after the initial material-less import appeared white; they are not exact color comparisons. Use the viewer's matching raw/authored views, and do not attribute all shading differences to generated paint.

## Evidence and limits

[Final GLB](artifacts/car_authored.glb), [editable Blender scene](artifacts/car_authored.blend), [viewer instructions](source/viewer/README.md), [pose renders](artifacts/authored-inspection/), and source/configuration are retained. Final GLB SHA-256: `a94dd03d1c425832c2879c242ac7dd1f571c05c308ea27fceccbfe30285853a6`.

Mechanical checks reopen the saved GLB, sample exported 0/30/60° poses, require static body transforms and exact return to closed. Browser checks exercise slider, play/pause, view changes and same-camera raw comparison; validator checks cover both GLBs. All these final checks passed; both GLBs have zero validator errors/warnings. Results and hashes are in `logs/authored-reopen-validation.json` and `source/viewer/verification/final/`. A viewer timing failure was corrected by mapping the slider to the opening half of the exported open/close clip. Visual assessment is separate from these mechanical checks: the convincing appearance target fails. Physical clearance, unseen-side accuracy, exact hinge construction and user acceptance are unestablished.

Two independent assistants supported CPU-route/viewer verification and visual review; conclusions remain bounded to the observed candidate. No broad survey or repeated remodeling was undertaken. The original repository remains unchanged. The prepared environment and saved configuration support this workflow; publication/restoration into a new task has not been tested. No further user input is needed to complete this bounded probe.
