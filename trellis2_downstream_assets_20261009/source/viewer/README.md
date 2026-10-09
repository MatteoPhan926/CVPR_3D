# Portable authored-asset viewer

`build.cjs` bundles the existing Three.js 0.170.0 / esbuild 0.24.2 installation and embeds an explicit GLB input as base64. The output HTML opens directly from disk, without a server, CDN, API, or network connection. It refuses missing input and existing output paths and checks a 50 MiB maximum. The source paths in the build script locate installed dependencies only; no old project asset path is loaded.

Build only after the final authored GLB is ready:

```sh
node source/viewer/build.cjs --input artifacts/authoring_A_v1/car_door_authored.glb --output artifacts/viewer/car_door_standalone.html
```

From the new phase root, verify with a Python interpreter providing Playwright, NumPy and Pillow:

```sh
python source/viewer/verify_viewer.py --html artifacts/viewer/car_door_standalone.html --output research/viewer/verification
```

The viewer preserves GLTFLoader native PBR materials and embedded textures. A slider maps 0–60° to the first two seconds of the baked animation, and playback traverses that interval forward and backward in a four-second cycle. If no animation exists, motion controls remain disabled. `FrontDoor_Control` tracks are preferred when choosing a clip. Source metadata, added geometry, lighting and scope are visible in the viewer; lighting values are also recorded by `assetViewer.getState()`.

The fixed source label identifies supplied asset A (`sample_2026-10-09T183055.354.glb`) and the specified authoring additions. This is a viewer for that authored deliverable, not an arbitrary-asset provenance classifier. The dependency's full MIT license is embedded in the HTML. Test output includes closed/half/open/side screenshots and transform/material checks; browser evidence does not establish artist acceptance or mechanical collision safety.
