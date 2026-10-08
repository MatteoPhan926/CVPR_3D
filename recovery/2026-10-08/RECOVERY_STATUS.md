# Recovery status — research decision 2026-10-08

**Status: RECOVERY_NOTES_ONLY — NEW RESEARCH ARTIFACTS NOT RECOVERED.**

This document preserves the recovery handoff and identifiers available outside the failed research executor. It is not a backup of the research files, a verified research report, or evidence that the original filesystem was recovered.

## Provenance and scope

- Prepared on 2026-10-08 from the user's exported conversation, the latest onboarding revision-9 report, and read-only GitHub checks.
- The two uploaded handoff copies were byte-identical. Their SHA-256 was `054ee201ad2ea9ec3fbd4845765e40734d98f83c2fd74e01719149c9b429379e`.
- No inference, rendering, setup, workspace reset, or modification of the failed executor was performed to create this document.
- The recovery-review runtime cannot read the four original executor directories below. Absence in this separate runtime does not establish deletion from the original executor.
- The original environment identifier and chat link should be obtained from the user's private handoff when contacting support. They are intentionally not republished here.

## Last known externally saved artifact set

Repository: https://github.com/MatteoPhan926/CVPR_3D

Immediately before creating this notes branch, the GitHub branch list contained:

| Branch | Head commit |
| --- | --- |
| `bentley-download-20261006` | `a04ddf538c72a3b34904845474395feccc31458a` |
| `image-to-usable-car-20261007` | `6b99f54997c17e5d1f26bab89e1b2ecdaab2f838` |

No GitHub releases were returned by the repository releases endpoint. The recursively listed tree of the car commit was complete and did not contain `research_decision_20261008`.

The old car probe remains available at the pinned commit:

- [Artifact tree](https://github.com/MatteoPhan926/CVPR_3D/tree/6b99f54997c17e5d1f26bab89e1b2ecdaab2f838/image_to_usable_car_probe_20261007)
- [Old evidence ZIP](https://github.com/MatteoPhan926/CVPR_3D/raw/6b99f54997c17e5d1f26bab89e1b2ecdaab2f838/image_to_usable_car_probe_20261007/IMAGE_TO_USABLE_CAR_PROBE_20261007_evidence.zip)

Recorded ZIP size: 18,645,267 bytes. SHA-256:

```text
ecd681e17c180177fadfa930a341ff050239bfccd213e1628c328672ccfd89bb
```

That ZIP was independently inspected during the earlier audit. This GitHub notes update rechecked repository metadata, not a new download of the ZIP. **The ZIP excludes the new 2026-10-08 research and the original car latent.**

## Original executor paths to recover

| Path | Recorded role |
| --- | --- |
| `/workspace/research_decision_20261008` | New research; no externally verified artifact backup has been identified. Preserve the complete tree, including unfinished outputs. |
| `/workspace/image_to_usable_car_probe_20261007` | Completed TripoSR car probe, original image, raw mesh, latent, authoring files, logs and CPU runtime. Some files were omitted from the old evidence ZIP. |
| `/workspace/generated3d_authoring_clean_20261006` | Bentley authoring session, history, Blender/browser tooling and shared dependencies. Preserve post-checkpoint edits if present. |
| `/workspace/CVPR_3D` | Git checkout; inspect actual HEAD, tracked/staged/untracked changes and refs rather than assuming the last reported state. |

These are **reported original paths**, not proof of their current existence.

## New-research inventory from the handoff

All paths in this section are relative to `/workspace/research_decision_20261008/`. This is a recovery search list, not a fresh filesystem inventory.

| Directory | Reported files and contents to preserve |
| --- | --- |
| `inputs/` | Supplied `IMAGE_TO_USABLE_CAR_EXECUTION_AUDIT_2026-10-08.md` |
| `generation_execution/` | `provenance_check.py`, `provenance_results.json`, `field_diagnostics.py`, `field_results.json`, `interpolation_check.py`, `interpolation_results.json`, `per_vertex_interpolation.npz`, density grids at 128/256, mesh variants, logs and controlled render comparisons |
| `authoring_attribution/` | Source ablation/selection/summary scripts, inventory/design/pixel/selection measurements, logs, renders A–K, contact sheets and `SHA256SUMS.json` |
| `history_opportunities/` | `HISTORY_OPPORTUNITIES.md`, asset inventory, GLB contract audit and measurements |
| `root_analysis/` | Holdout contract, generation/preprocessing scripts and logs, `export_variants.py`, `verify_saved_forward.py`, possible saved-forward completion output |
| `root_analysis/holdouts/teapot/` and `hamburger/` | Source image, mask/composites, preprocessing metadata, inference-start record, `scene_codes.pt`, `raw.glb`, `execution.json` |
| `root_analysis/exports/` | Raw/unlit/PBR color export variants, validation records and logs |
| `root_analysis/browser/` | HTML, JavaScript source/bundle, verification script and all server/verification logs, including failures |
| `root_analysis/specification/` | Saved glTF/unlit source documentation and provenance receipt |
| `extraction_control/` | Edge-refinement and verification scripts, `results.json`, `verification_and_aggregate.json`, `crossed_controls.tsv`, arrays, refined meshes, renders and logs |
| `adversarial_review/` | Draft `REVIEW.md`, oriented-reproduction script/result, prior-art source and receipt |

Keep files not named in this list too. Do not discard latents, arrays, failed checks or incomplete outputs as disposable caches.

## Reported work versus unverified completion

The earlier executor reported decoder-to-mesh reproduction, controlled rendering/authoring checks, two TripoSR holdouts (teapot/hamburger), numerical edge-refinement comparisons, and a prior-art audit. **These are handoff claims until their actual files are recovered and checked.** No new CVPR/ICCV contribution is certified by this recovery document.

The handoff explicitly left these items incomplete or unverified:

- Browser validation of exported color/material variants.
- Completed forward replay from the original car image and its final latent comparison.
- Log-density interpolation comparator.
- Final aggregate interpretation and adversarial review.
- Final research report, artifact archive, and external delivery.

Teapot/hamburger were export/extraction checks, not the proposed artist-revision experiment. The separately mentioned car experiment still has no verified identifying metadata in this handoff.

## Recorded fingerprints for recovered files

These values were reported before the executor became inaccessible; do not label them newly recomputed.

| Item | SHA-256 |
| --- | --- |
| Original car image | `b5b9ed4aece1359a0d291e89149634499583102e27f177aadb4c60f327e996e1` |
| Car processed image | `d8bfea522456e376988d98cbdfd8cdde7eb35e7454bd51ade8cf166b29fbdb06` |
| Car raw GLB | `5bd4ab3776084c5586201abd0d3be36416b3331cb28295d8d066ac7ac7beac3d` |
| Car latent | `a57eab70b278aaf888020cd916e3562985300026c9973399a1a81625cbf42b00` |
| Car authored GLB | `a94dd03d1c425832c2879c242ac7dd1f571c05c308ea27fceccbfe30285853a6` |
| Teapot raw GLB | `dea230ae9549e39368498a93839cde1c67289e7ea586aa5d60f057980b45b5c4` |
| Teapot latent | `dee41aab2f83db0a9365f0711acbce23aefa2e089cd2a41b224b1a608bb988a9` |
| Hamburger raw GLB | `1cddedab568b5ab34e4537d946f9e750282f149325fd4d22f31dd28599f12984` |
| Hamburger latent | `4368164c10e789bbab771b68e3a63ac42ac56fb1f30258e73d50119e6bf08ad9` |
| TripoSR checkpoint | `429e2c6b22a0923967459de24d67f05962b235f79cde6b032aa7ed2ffcd970ee` |

TripoSR source: `107cefdc244c39106fa830359024f6a2f1c78871`.
Model revision: `5b521936b01fbe1890f6f9baed0254ab6351c04a`.

## Onboarding revision 9: reported configuration change only

The user supplied a report stating that revision 9 was saved/read back with these rules: read-only startup; preservation before setup/repair; external checkpoints after results; verification by read/download and checksum; stop costly work when external persistence fails; restore into a new directory without overwriting existing work.

The report says `requires_publish: true` and that Review/Save followed by Publish is needed to apply the draft. **This reviewing session has not inspected or published that configuration.** Publishing configuration is not recovery of artifact bytes and is not a verified fix for the executor startup failure.

Reported blocker: `failed to query executor configuration capabilities`. An earlier attempt also reported `exec-server connection attempt failed: managed environment readiness timed out`. Neither message establishes that the original files have been deleted.

## Recovery procedure when access returns

1. Confirm access to the original executor or an identified snapshot. Read applicable project instructions, list the roots, and inspect Git state without setup/build/inference.
2. Preserve the available new research and required inputs into a new destination before repair. Inventory actual files, sizes and hashes; record missing/unreadable files. A narrative or checksum cannot reconstruct absent bytes.
3. Keep an untouched recovery copy. Do not overwrite the source, reset/clean it, or run experiments to replace the historical evidence.
4. Publish the preserved artifact set to durable storage outside that executor, with a manifest and checksums. Preserve code/configuration/reports on an appropriately named branch. Large artifacts require actual uploaded bytes, not just pointers or local archives.
5. Read/download the remote copy and verify it. Record exact commit, artifact URLs, manifest coverage, exclusions and remaining gaps.
6. Only then resume research. If the old executor cannot be reached, preserve its private identifiers/chat link and request platform recovery assistance; do not present a fresh clone as restoration of unpushed work.

## Meaning of this branch

The branch protects **this recovery record and the old Git history it is based on**. It does not protect or recover the absent new meshes, latents, arrays, images, logs or source files. A later recovery update must state exactly which bytes were recovered and independently verified.

