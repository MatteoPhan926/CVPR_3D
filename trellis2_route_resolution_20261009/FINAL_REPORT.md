# TRELLIS.2 route resolution: concrete alternatives prepared; user-car acquisition still blocked

**Decision:** retain the original image and front-door use test. The official route currently fails authentication; a documented fal TRELLIS.2 alternative is prepared but needs authorized paid access. No new car-generation request, user-image upload or paid request ran in this phase. This is an execution/access finding, not a TRELLIS.2 quality result or a CVPR/ICCV contribution.

The work goes beyond a route proposal: current authentication was exercised, exact deployed library source was inspected, a conditional explanation of the old quota message was reproduced locally, a real public GLB was downloaded/validated/imported, and an exact-image request was prepared and schema-checked. [RUN_LEDGER.json](RUN_LEDGER.json) separates these activities from unrun car acquisition and authoring.

## Current access, checked after reconnects

At **22:16 on 9 October 2026, Asia/Bangkok**, `HF_TOKEN` was present and resolved through the existing Hugging Face client. The official `HfApi.whoami` request nevertheless returned **HTTP 401**, `Invalid username or password.` It had also returned 401 before and after the earlier restart. No identity or secret value was saved. The configured binding exists, lists both required hosts, and exposes no configuration error; that metadata does not prove the effective credential path works. [Latest check](research/access_after_second_reconnect.json), [earlier check](research/access_after_restart.json), [reusable read-only checker](source/check_access.py).

This narrows the immediate blocker to the effective authentication path. It does **not** isolate invalid/revoked token contents from binding replacement, proxy handling or propagation. Correcting that path and observing a successful identity check is a meaningful reason for a new bounded attempt. It still would not guarantee either GPU allocation or export.

The current host exposes no NVIDIA devices. `FAL_KEY`, `MESHY_API_KEY`, `TRIPO_API_KEY`, Replicate and RunPod credential variables were absent in the checked instance. This is a checked configuration observation, not a claim that the user has no such accounts. Public official Space/API metadata was accessible. RUNNING/public status does not establish this caller's GPU admission. No anonymous quota retry was made.

## A stronger explanation of the old quota message

The public Space metadata reports `spaces==0.50.2`. The exact PyPI wheel was downloaded, SHA-256 checked and inspected without installing or importing it. Its Blackwell/non-`xlarge` branch applies a **1.5 duration factor** before scheduling, while its quota-error message displays the original declared duration. Thus a declared 120-second function can ask the scheduler for **180 seconds** but display **120 seconds**. Under that condition, 176 seconds remaining is insufficient. [Independent source review](research/access_policy/review/FINDINGS.md), [source](research/access_policy/review/spaces_0_50_2_source/spaces/zero/client.py), [local arithmetic result](research/access_policy/review/duration_arithmetic_result.json).

This is a source-supported **conditional explanation**, not a verified remote root cause: the actual server hardware/configuration and scheduler comparison were unavailable. It does not settle the older `120 vs. 180` equality. Documentation and runtime messages also disagree on some quota totals, so neither is a live budget guarantee.

The public API has no reviewed read-only endpoint that guarantees both allocations. The package's internal `POST /schedule` reserves work and was not used as a harmless quota query. Generation and export are separate GPU-decorated functions requiring the same live session. Current docs also say eligible paid accounts can automatically consume prepaid credits after included quota; a future run must respect the user's spending authorization rather than assuming all hosted execution is free.

## Routes selected by relevant capabilities and access

| Route | Evidence for this task | Current dependency / limit |
|---|---|---|
| Official Microsoft TRELLIS.2 Space | Same previously inspected preprocessing and generation/export interface; original contract retained | Current identity check 401; both GPU stages still need admission. No guarantee that authentication or waiting fixes quota |
| **fal `fal-ai/trellis-2`** | Single-image input; all 16 inherited numeric controls exposed; downloadable textured GLB and UV controls. **$0.30/request at 1024** advertised on the specific model page | No key or paid authorization. Needs valid `FAL_KEY` and sufficient prepaid balance; purchase minimum/total account setup cost unknown. Model revision, preprocessing and export implementation parity unverified |
| **Meshy 7.1**, proposed comparator | Same original photograph can feed a current image-to-3D workflow; GLB and PBR options documented. Standard geometry + 2K textures: **30 API credits** | Paid-plan API-key entitlement plus prepaid API credits required. No key, trial or output. Dollar conversion/minimum purchase unverified |
| Tripo | Official pages were reached, but saved responses were application shells | Insufficient retrieved evidence; no claim about capability, price, quality or inferiority |

Sources and independent assessment: [commercial review](research/commercial_routes/review/INDEPENDENT_REVIEW.md), [fal endpoint](https://fal.ai/models/fal-ai/trellis-2), [fal saved OpenAPI](research/commercial_routes/review/fal_schema.json), [Meshy pricing](https://docs.meshy.ai/en/api/pricing), [Meshy key prerequisites](https://docs.meshy.ai/en/api/quick-start). Product claims establish interface/pricing proposals, not task success. Meshy's free web credits do not establish usable API access. Automatic character rigging or generic part claims do not establish a coherent car door.

fal is a documented **same-model-family provider alternative**, not an exact reproduction of the Microsoft pipeline. It exposes no pinned checkpoint, explicit `1024_cascade` selector or preprocessing bypass. Feeding the previously black-composited PNG could process it again. The prepared request therefore preserves the **original JPEG**, with provider preprocessing explicitly unknown. Its final-GLB response also lacks the official route's separate processed-image and preview-before-export checkpoints. This is a declared provenance/checkpoint trade-off; it does not silently change the artist-use task.

## Actual public-file experiment, separate from the user's car

To test more than product claims, the unchanged example GLB linked directly by fal's endpoint documentation was downloaded without authentication. It is **not generated from this user's photograph**, has unknown generating settings/revision and is not used as substitute car geometry. [Receipt](research/public_fal_sample/download_receipt.json), SHA-256 `a8b528d7715ada8dfa5c7dd0ac63abe47c682752db86bfbf4625f516cc443b2a`.

| Check actually performed | Result | Interpretation limit |
|---|---|---|
| Binary GLB inventory | 384,665 vertices; 479,123 triangles; UV0 and normals; embedded base-color and metallic/roughness textures; required `EXT_texture_webp` | One provider-linked sample, not a guarantee for every output; material is OPAQUE, has no normal map or animation |
| glTF validator | **Failed:** 18 non-unit-normal errors; four buffer-target hints; untruncated report | Conformance error, neither a warning-only pass nor proof of DCC unusability |
| Blender 4.3.2 import | **Passed loading:** UVMap, custom normals, two decoded 2048² images; sRGB base color and Non-Color metallic/roughness linked to Principled inputs | No render, re-export, appearance-fidelity or artist-acceptance test |
| Import geometry check | 479,103 imported polygons, **20 fewer** than raw triangles; original GLB bytes unchanged | Import must not be described as geometry-preserving |
| Read-only raw numeric follow-up | 18 near-zero normals; 57 exact-zero-area triangles; no repeated vertex indices | No exact removed-face mapping; the 57 degenerates do not prove which 20 faces changed |

Evidence: [inventory](research/public_fal_sample/glb_inventory.json), [validator](research/public_fal_sample/gltf_validation.json), [Blender result](research/public_fal_sample/blender_import.json), [log](logs/public_sample_blender_import.log), [numeric diagnostic](research/public_fal_sample/normal_and_face_diagnostic.json). Blender logged a read-only extension-cache warning but completed import and decoded both images; no repair was attempted. Possible importer cleanup is an alternative explanation for the face-count difference, not an established mapping. No broad compatibility or normal-preservation claim follows.

This resolves a narrow useful question: the linked textured export can be opened by the installed DCC despite concrete schema defects. It establishes neither the user's car quality nor a new research gap. An ordinary serialization/import issue is a stronger immediate explanation than a dramatic inability to produce usable assets; a fresh car and its authoring task are still needed to test that.

## Concrete preparation and remaining dependency

[Prepared fal request](config/fal_request_prepared_NOT_SUBMITTED.json) contains the exact original image as a local data URI, seed 42, resolution 1024, all twelve inherited sampler parameters, 300000 decimation target and 2048 texture size, plus explicitly recorded provider defaults. [Preparation receipt](research/fal_request_preparation.json) records the source/schema/request hashes. Offline JSON Schema validation passed; decoded image bytes roundtrip exactly, and an incorrect string resolution was rejected. The script contains no network submission. Acceptance, actual price charged and generated output remain untested. The published decimation target is a vertex target, not a promise of triangle count.

Two concrete ways to unblock acquisition remain:

1. **Official route:** inspect/correct the existing secure HF_TOKEN binding or effective authentication path until a fresh official identity check succeeds. No secret in chat. Establish an authorized quota/spending basis for both generation and export; then one separately checkpointed attempt in a new directory, not a replay over old records.
2. **fal alternative:** explicitly authorize **one 1024 request at the advertised $0.30 inference price**, provide a valid `FAL_KEY` through secure environment settings and sufficient prepaid balance, and accept the documented provider/preprocessing/checkpoint differences. A $0.30 minimum top-up is **not** established. Recheck price before submission; a higher price or unknown timeout is not permission for more spend or resubmission. No purchase or secret value was created here.

Once a car result is obtained, download and externally checkpoint the raw GLB and any exposed intermediates first. Inspect its native UV/PBR/materials, then compare raw and DCC import/export appearance before bounded conventional front-door preparation and 0/30/60°/reverse/trajectory/view checks. Do not reuse the TripoSR vertex-color-only cutters unchanged. Server-held latent state is unexposed on these reviewed hosted interfaces; do not claim it backed up. All locally returned latent/array data, if any later exist, must be preserved.

## Research decision and delivery

**Continue the car thread only after one of those access dependencies changes.** fal is a concrete acquisition option, while Meshy is a current comparator worth considering after an actual comparison budget is authorized. The old TripoSR visual failure cannot represent either alternative. No mechanism or publication claim is selected from these infrastructure and sample-format results; quality, cost and control must be measured on the declared artist task. The separate revision study remains unstarted and no unidentified separate car experiment was duplicated.

The strongest unresolved alternatives are (a) token/proxy/binding failure rather than model-service incapacity, (b) a conditional scheduler accounting/display difference rather than arbitrary rejection, and (c) ordinary export/import handling rather than meaningful artist-use failure. A selected public sample is also insufficient evidence of current endpoint reliability or car quality. [Independent adversarial review](research/adversarial_review/FINDINGS.md) challenged these distinctions; its review predates the final import receipt, so the receipt and numeric follow-up support the later observations directly.

Existing evidence was preserved. Full milestone archives and later small-result commits were pushed and read back before further work; [DOWNLOADS.md](DOWNLOADS.md) indexes the final archive and verification receipts. Failed requests/fetches, validator errors, raw sample, decoded diagnostics, source snapshots, scripts, original input and unsubmitted payload are retained. No local generated car or latent is omitted—none was obtained in this phase. Prior car/research backups remain separate.

Only `start_skill` was updated in the onboarding draft; existing credential bindings and install script were preserved. Saved instructions pin verified recovery paths and prohibit automatic paid submissions or overwrites. Read-back matched; runtime auth is still not fixed and future publication/restoration is not verified. The platform requires review/save/publish of the draft for future startup. [Configuration receipt](research/onboarding_update.json).
