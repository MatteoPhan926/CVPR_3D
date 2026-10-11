# Downloads and recovery

This pre-package index will be updated with immutable data-commit URLs and successful fresh-download receipts after publication. The links below name the final archives; do not call their recovery verified until the final receipts are present.

- [Main delivery ZIP](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/trellis2-downstream-assets-20261009/trellis2_downstream_assets_20261009/checkpoints/05_final_delivery.zip): original uploads, final GLB/Blend/viewer, required reopened views, reports, source, configs and research logs.
- [Supporting evidence ZIP](https://raw.githubusercontent.com/MatteoPhan926/CVPR_3D/trellis2-downstream-assets-20261009/trellis2_downstream_assets_20261009/checkpoints/06_supporting_evidence.zip): raw inspection scenes, intermediate arrays/partition-only output and retained first viewer build.

Extract both into the same NEW directory for all payload files. Neither includes previous checkpoint ZIPs or subsequent receipts. Original filenames and hierarchy are preserved. Both sidecar manifests enumerate every payload SHA-256. The final GitHub copy of this index contains immutable commit links.

The existing milestones are already externally downloaded, extracted and verified: 01_originals at 228ef1b23df2660e3bfa36096cce4b4f12bee57e; 02_inspection_preparation at 8a12a4bc38bd11ff1cddd1792e337e198f55a2e6; 03_authored_baseline at 83611b83a46a7b44dee44ec0931e6ee43ad18828; 04_verified_downstream at b8fe4ff97592a4d3abce661fd56a63d9c578efd5. Corresponding receipts are retained in checkpoints/. Viewer and final handoff were committed separately before final packaging.

Use source/restore_verified_checkpoint.py with the exact final data commit and a NEW/empty destination. It verifies both ZIPs and every member before writing, then rereads restored bytes. It refuses a nonempty destination; --check-existing only reports matching, missing and changed files without replacing them. No generation, build or setup is run.

Older phases remain separately preserved in recovery_checkpoint_20261008, research_decision_delivery_20261009, trellis2_car_followup_20261009 and trellis2_route_resolution_20261009 on GitHub. Do not conflate their model runs or use their access-blocked status to disregard the new supplied GLBs.
