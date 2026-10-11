# Portable viewer verification

Prepared and tested 2026-10-10 in Chromium 151.0.7922.173 using the existing Node, Python, Playwright, NumPy and Pillow installations. No dependency installation, paid calls, model calls, asset edits, material edits or Git operations were performed.

## Deliverable and status

`artifacts/viewer/car_door_standalone.html` is a 15,193,218-byte standalone package containing Three.js 0.170.0, the authored GLB, its two embedded images and the dependency license. HTML SHA-256: `2130623ce41a1412785ed053e26b14b38a337a1ed63f29ae35af81f7c2b703ed`.

The embedded GLB is byte-identical to `artifacts/authoring_A_v1/car_door_authored.glb`, SHA-256 `7884da938b8461c0edb0638efc12d5e1c47c1192ea6da2a0d7f225417f21c03c`. The package has no external image/buffer URIs. See `static_package_checks.json` and the accompanying `.build.json`.

Functional browser verification **passed through loopback HTTP with all subsequent HTTP(S) requests blocked**. Direct `file://` launch was **blocked and remains unverified**. These are distinct outcomes; the fallback is not an offline file-launch pass.

## Browser evidence

`verification_attempt_03_local_http/verification.json` records the successful run against the final HTML hash. Only the initial local document request was permitted; no other HTTP(S) requests were attempted. JavaScript errors and console errors were empty.

- Slider states 0°, 30° and 60° rendered; measured hinge changes were 30.000007843° and 59.999996927°.
- The hinge, native door, inner lining and edge thickness moved. The exterior body, fixed jamb, floor, seat and dashboard remained fixed.
- Reset restored all recorded transforms exactly (maximum matrix delta 0), plus the default view.
- Continuous playback was observed opening, reversing toward closed, and opening again; pause, closed/open buttons and the side view passed.
- 27,208 viewport pixels changed beyond eight channel levels between closed and open screenshots.
- Four browser-loaded `MeshStandardMaterial` instances match the GLB's base-color, metallic and roughness factors and texture-binding presence. Native base color uses sRGB; metallic/roughness data uses a non-color texture space. See `native_pbr_checks.json`.

Screenshots in `verification_attempt_03_local_http/`: `closed.png`, `half.png`, `open.png`, `open_side.png`. Visual inspection confirms the native textured exterior and authored opening/interior are visible. Irregular source surfaces and the proxy interior remain visible; this is not an artist acceptance or collision-safety judgment.

Playback is configured as two seconds opening and two seconds closing. This headless SwiftShader run is not a smoothness or FPS benchmark. The reversal observation sequence took 23.175 seconds including browser calls; that value does not establish an accurately measured four-second wall-clock cycle or interactive hardware performance.

## Retained failures and correction

1. `verification_attempt_01.log` / `.run.json`: Chromium rejected the initial `file://` navigation with `net::ERR_BLOCKED_BY_ADMINISTRATOR`, before loading the viewer. `/etc/chromium/policies/managed/urls.json` sets `URLBlocklist: ["*"]` and allows HTTP(S)/WSS plus selected browser pages, without a `file://` exception. The managed policy was left intact.
2. `verification_attempt_02_local_http.log` / `.run.json`, with screenshots: the first viewer build sampled from time zero, but this GLB's first animation key is at 0.033333335 seconds. The 30° slider therefore measured 29.000000736°. This assertion failure was retained.
3. `source/viewer/main.js` now samples from the first native key timestamp plus the requested opening interval. The original HTML/build record remains as `artifacts/viewer/car_door_standalone_attempt_01.html` and `.build.json`; its hash is `99262aee92f075a009451d89108769a1f0c324b96d3887e06f860c3c67bd4c01`. Original output paths recorded inside earlier build logs refer to the pre-retention name. The final HTML passed the meaningful angle assertions without changing the GLB.

`source/viewer/verify_viewer.py` retains direct-file verification as its default and adds an explicit `--transport local-http` fallback. Its report identifies the transport and records `file_protocol_verified: false` for that fallback. Missing animation fails verification; it is never treated as success. Reproduction commands and the managed-policy limitation are documented in `source/viewer/README.md`.

The remaining check is to run the default file transport in a browser environment whose policy permits local HTML. No cloud setup configuration fields were changed: the existing tools sufficed, and the temporary verification server stopped when the successful run ended.
