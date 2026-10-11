# Verified downloads — 11 October 2026

**All 175 research payload files were downloaded from GitHub into a fresh directory, verified by SHA-256, restored and reread. No missing or changed payload was found.** Downloaded archives/manifests and restored bytes also match the locally packaged evidence. Recovery refusal on a nonempty directory and missing/changed-file reporting were tested separately without modifying existing research work.

Data commit: **`37da741a3f74f2fbb48528bc8af5e285feb7e58b`**. Branch: `trellis2-downstream-assets-20261009`.

| Archive | Bytes | Payload files | SHA-256 |
|---|---:|---:|---|
| [Main delivery ZIP](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/37da741a3f74f2fbb48528bc8af5e285feb7e58b/trellis2_downstream_assets_20261009/checkpoints/05_final_delivery.zip) | 67,498,434 | 127 | `e6533629189ffb715ae65595c312762e0ed9d50a41ed46829998bbbe60418625` |
| [Supporting evidence ZIP](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/37da741a3f74f2fbb48528bc8af5e285feb7e58b/trellis2_downstream_assets_20261009/checkpoints/06_supporting_evidence.zip) | 86,007,085 | 48 | `fb78f8b69b41ccc8ff6589f16d40d78dc5ac08bd4d2b4d523f7a5a5d644bbcce` |

The main delivery includes both original uploads, final GLB/Blend/viewer, required reopened views, reports, code/configs and research logs. Supporting evidence adds raw inspection scenes, intermediate cut arrays and partition-only results, source/presentation controls and the retained failed viewer build. Extract both into the same NEW directory for the full payload; no original payload path overlaps. Each ZIP's CHECKPOINT_CONTENTS.json is its own manifest, so extract those two metadata files under distinct names if retaining both. Sidecar manifests remain authoritative.

- [Full report](https://github.com/MatteoPhan926/CVPR_3D/blob/37da741a3f74f2fbb48528bc8af5e285feb7e58b/trellis2_downstream_assets_20261009/FINAL_REPORT.md)
- [Secretary handoff](https://github.com/MatteoPhan926/CVPR_3D/blob/37da741a3f74f2fbb48528bc8af5e285feb7e58b/trellis2_downstream_assets_20261009/SECRETARY_HANDOFF.md)
- [Authored GLB](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/37da741a3f74f2fbb48528bc8af5e285feb7e58b/trellis2_downstream_assets_20261009/artifacts/authoring_A_v1/car_door_authored.glb)
- [Blender scene](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/37da741a3f74f2fbb48528bc8af5e285feb7e58b/trellis2_downstream_assets_20261009/artifacts/authoring_A_v1/car_door_authored.blend)
- [Self-contained viewer HTML](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/37da741a3f74f2fbb48528bc8af5e285feb7e58b/trellis2_downstream_assets_20261009/artifacts/viewer/car_door_standalone.html) — use the loopback instructions in README; direct file:// launch was policy-blocked and remains unverified.
- [Fresh download/restore receipt](checkpoints/07_final_restore.verification.json), [restore guard check](checkpoints/08_restore_guard.verification.json), [changed/missing fixture report](checkpoints/08_existing_state_check.json).
- [Payload grouping](config/FINAL_ARCHIVE_PLAN.json); [main manifest](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/37da741a3f74f2fbb48528bc8af5e285feb7e58b/trellis2_downstream_assets_20261009/checkpoints/05_final_delivery.manifest.json); [support manifest](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/37da741a3f74f2fbb48528bc8af5e285feb7e58b/trellis2_downstream_assets_20261009/checkpoints/06_supporting_evidence.manifest.json).

## Recovery without overwriting work

Read the reports and inspect existing Git status first. Use the committed restore script with the exact data commit:

```sh
python3 source/restore_verified_checkpoint.py --commit 37da741a3f74f2fbb48528bc8af5e285feb7e58b --destination /workspace/trellis2-downstream-restored-37da741 --receipt /tmp/trellis2-restore-receipt.json
```

Run from this phase directory. Choose a NEW/empty destination and a receipt path that does not already exist. The script downloads and verifies both ZIPs and every member before restoring, then rereads restored bytes. It refuses nonempty destinations. Use `--check-existing` to report matching/missing/changed files without replacing them; changed or missing files return exit2. Restore mode does not install dependencies, alter Git, or run experiments.

The actual verified restore used `/tmp/trellis2_final_restore_37da741` and matched all175 files. Those local paths are verification evidence, not durable storage. The immutable GitHub URLs above are the external checkpoint.

## Earlier milestones and exact scope

| Milestone | Data commit | Verified scope |
|---|---|---|
|01_originals|228ef1b23df2660e3bfa36096cce4b4f12bee57e|7 files, both originals before processing|
|02_inspection_preparation|8a12a4bc38bd11ff1cddd1792e337e198f55a2e6|78 snapshot files|
|03_authored_baseline|83611b83a46a7b44dee44ec0931e6ee43ad18828|44 snapshot files, actual authored baseline and controls|
|04_verified_downstream|b8fe4ff97592a4d3abce661fd56a63d9c578efd5|46 snapshot files, reopened result and diagnostics|
|Viewer/final-handoff delta|db57d36745e207ef0dafa52775303bb814f9018c|36 changed/new files downloaded and compared|

All receipts, archives and retained failures remain in Git. The two final ZIPs exclude prior checkpoint archives and subsequent publication/configuration receipts; those small later files are separately committed and read back. Their pre-package DOWNLOADS copy intentionally predates the final verification; this GitHub index is the authoritative updated index. No research mesh/array/render/result is omitted from the 175-file payload. No generator latent or generation log was returned with the uploads; server-held state, missing settings and exact conditioning bytes remain unavailable.

The 20261008 recovery and earlier TripoSR/research/route reports remain separately preserved in their existing repository folders and branches. Their executions must not be conflated with these supplied TRELLIS.2 outputs.
