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

The viewer preserves GLTFLoader native PBR materials and embedded textures. A slider maps 0–60° to the first two seconds beginning at the baked animation's first key timestamp, and playback traverses that interval forward and backward in a four-second cycle. The authored GLB starts at 1/30 second; including that origin avoids a one-degree sampling error. If no animation exists, motion controls remain disabled and verification fails. `FrontDoor_Control` tracks are preferred when choosing a clip. Source metadata, added geometry, lighting and scope are visible in the viewer; lighting values and the animation origin are also recorded by `assetViewer.getState()`.

The current cloud Chromium managed policy blocks `file://` navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. Keep that failed test as evidence; do not change the managed policy. For independent functional checks, the verifier supports an explicitly distinguished fallback:

```sh
python source/viewer/verify_viewer.py --html artifacts/viewer/car_door_standalone.html --output research/viewer/verification_local_http --chromium /usr/bin/chromium --transport local-http
```

This serves only the HTML from an ephemeral loopback server. Only the initial document request is permitted; every subsequent HTTP(S) request is blocked. The report records `file_protocol_verified: false`, so a successful fallback does **not** establish direct file launch. The default `file` mode must be run in a browser environment permitting local-file navigation to validate that requirement. Python, Playwright, NumPy and Pillow are already available in the current `python`; no new installation is needed. The viewer itself requires no running server after download when opened in a browser that permits local HTML.

The fixed source label identifies supplied asset A (`sample_2026-10-09T183055.354.glb`) and the specified authoring additions. This is a viewer for that authored deliverable, not an arbitrary-asset provenance classifier. The dependency's full MIT license is embedded in the HTML. Test output includes closed/half/open/side screenshots and transform/material checks; browser evidence does not establish artist acceptance or mechanical collision safety.
