# Independent commercial route assessment — 2026-10-09

## Decision

**fal `fal-ai/trellis-2` is a practical documented same-model-family alternate for acquiring an image-conditioned textured GLB, conditional on paid access and acceptance of a provider change. It is not a demonstrated exact reproduction of the Microsoft Space.** All explicitly inherited sampling and export values fit the current public OpenAPI fields. The provider exposes seed and UV controls and returns a GLB. Public docs do not establish exact loaded checkpoint, identical preprocessing, exact export implementation, all PBR channels, or separable generation/export checkpoints. No user inference or export was run.

**Meshy is a relevant contemporary workflow comparator**, because its current API takes the same single photograph and returns textured GLB with documented PBR options. Pin `meshy-7.1` rather than mutable `latest` (currently an alias for Meshy 7.1). Its paid-account/key and prepaid-API-credit requirements are explicit. It is a different model and cannot inherit TRELLIS.2 seed/sampler semantics. Documentation alone cannot establish which asset is more usable for this car-door task.

**Tripo remains unassessed in this bounded review.** The saved direct docs/pricing fetches are identical 689-byte HTML shells. HTTP 200 is evidence of page reachability, not evidence of model behavior, usable pricing, export support or account access. No fourth provider was considered.

## Scope and unchanged authoring objective

Inputs read: `config/INHERITED_AUTHORING_INTENT.md` and `config/PREVIOUS_GENERATION_PLAN.json`. The image is the user's 516×387 Citroën photograph, with SHA-256 `b5b9ed4aece1359a0d291e89149634499583102e27f177aadb4c60f327e996e1`. Neither image bytes nor derived images were transmitted in this review.

A relevant asset must support conventional authoring of the visible front cabin door with frame, glass, handle and lining moving coherently; other parts fixed; 0/30/60-degree poses; reversible continuous motion; and credible exposed edge, aperture and cabin. Required views remain whole-car front/near-side at about 1440×960 plus close-up. Door segmentation, hinge correctness, hidden surfaces and usable interior are not promised by either generation API. Local cuts, thickness/interior completion and material repair remain part of the original bounded authoring work. Runtime, human effort and visual acceptance are different measurements.

The inherited plan expressly disallows paid services and allows at most one successful candidate, with no favorable-output selection. Commercial-document research does not amend those execution constraints. At most one paid-route candidate would be a future acquisition alternative; executing both providers would require a separately authorized comparison design and attempt budget. This review creates no generation job, account, payment, credential or input upload.

## fal evidence

Official sources saved before review:

- Model and exact per-request prices: <https://fal.ai/models/fal-ai/trellis-2> (`../fal_trellis2.txt`, original fetch receipt alongside it).
- Endpoint/interface: <https://fal.ai/models/fal-ai/trellis-2/api> (`../fal_trellis2_api.txt`).

New read-only source receipts in this directory:

- Exact machine-readable schema: <https://fal.ai/api/openapi/queue/openapi.json?endpoint_id=fal-ai/trellis-2> (`fal_schema.json`, `fal_schema.fetch.json`).
- Billing rules: <https://fal.ai/docs/documentation/model-apis/pricing.md> (`fal_model_api_pricing.md` and receipt).
- General price table: <https://fal.ai/pricing> (`fal_pricing.txt` and receipt).
- Quickstart and overview: `fal_quickstart.md`, `fal_overview.md`, receipts.
- Read-only account billing API documentation: `fal_account_billing.md` and receipt. The account API itself was not called.

### Input, output, material facts

`image_url` is required; the docs permit a publicly accessible URL or base64 data URI and describe optional fal-managed storage upload. A local path alone is not API input. The playground accepts jpg/jpeg/png/webp/gif/avif/heic/heif; the inherited JPEG fits the documented types.

Output is required `model_glb`, a file object with required URL and optional name, MIME type and size. This is the final GLB response, with no documented shape/texture latent fields. UV unwrap and texture-baking controls establish a documented textured-mesh export path. **The endpoint schema does not specify metallic/roughness/normal/alpha channel guarantees or the internal GLB material structure.** Do not infer full PBR preservation merely from GLB container support. Check a future raw GLB's UV attributes, textures, material factors/maps, alpha mode, normals and import/export appearance before authoring.

### Control parity and limitations

Static `fal_parameter_mapping.json` confirms that all 16 inherited numeric controls are exposed and within schema bounds: seed 42, resolution 1024, 12 sampler controls, decimation target 300000 and texture size 2048. The file also has an intentionally unusable image placeholder and was not submitted. Actual OpenAPI `resolution` and `texture_size` enums are integers, even though the human page sometimes prints quoted values.

| Stage | strength | rescale | steps | rescale_t |
|---|---:|---:|---:|---:|
| Sparse structure (`ss`) | 7.5 | 0.7 | 12 | 5 |
| Shape (`shape_slat`) | 7.5 | 0.5 | 12 | 3 |
| Texture (`tex_slat`) | 1 | 0 | 12 | 3 |

Strength range is 0–10; guidance rescale 0–1; sampling steps 1–50; rescale_t 1–6. Resolution options are 512,1024,1536; texture sizes 1024,2048,4096. `decimation_target` ranges 5000–2000000, default 500000; fal describes it as a **vertex** target, so do not equate it to Meshy's **face** target.

Additional fal fields/defaults, absent as explicit choices in the inherited plan: sparse and shape guidance intervals 0.6–1; texture guidance interval 0.6–0.9; remesh=true; remesh_band=1; remesh_project=0; UV chart angle 90°; UV refine iterations 0; global iterations 1; smooth strength 1. The exact schema preserves allowed ranges. These defaults are not proof of parity with Microsoft Space internals.

No exposed `pipeline_type` or checkpoint/revision selector is documented. Resolution 1024 does not prove the exact `1024_cascade` implementation. No exposed preprocessing toggle/configuration establishes BRIA-RMBG-2.0, identical square crop and black compositing, or avoidance of reprocessing an already processed input. For the original JPEG, object isolation/background removal could differ from the official Space. For the previously processed black-background PNG, a second crop or background-removal pass could alter foreground scale, framing or masks; no schema field promises a bypass. Preserve both image hashes and label any chosen input/preprocessing change explicitly in a future run. Exact same seed across provider implementations does not guarantee identical geometry. The single response also does not provide the original plan's separate processed-image gate and generation-preview-before-export checkpoint. These are substantive provenance/checkpoint limitations, not image-quality findings.

### Price and prerequisites

Exact model page quote: “Your request will cost 0.25 $ for 512p resolution, 0.3 $ for 1024p resolution and 0.35 $ for 1536p resolution.” Thus the inherited 1024 setting is advertised at **USD 0.30 per request**. The general pricing table separately lists TRELLIS.2 at **USD 0.05 per billing unit**; it does **not** say a complete 1024 generation costs $0.05. Prefer the model's resolution-specific total. No authenticated estimate, invoice or charged run was observed; taxes, purchase minimum and account-specific balance/discounts are unverified.

fal Model APIs use prepaid credits; successful outputs are billed, server errors HTTP 500+ and queue waiting are not billed. Account/key and a sufficient spendable credit balance are prerequisites. `FAL_KEY` is the documented runtime binding; raw HTTP uses `Authorization: Key ...`. A paid serverless GPU deployment is not required to call this hosted model. This review did not inspect an account balance or make a purchase. Runtime credential status is independently rechecked by the parent task; this review makes no new credential-availability claim.

## Meshy evidence

Original saved sources:

- <https://docs.meshy.ai/en/api/image-to-3d> (`../meshy_image_to_3d.txt`).
- <https://docs.meshy.ai/en/api/pricing> (`../meshy_api_pricing.txt`).
- <https://www.meshy.ai/pricing> (`../meshy_pricing.txt`).

New official sources and fetch receipts:

- <https://docs.meshy.ai/en/api/quick-start> (`meshy_quickstart.txt`).
- <https://docs.meshy.ai/en/api/authentication> (`meshy_auth.txt`).

### Input and proposed comparison settings (not submitted)

API is `POST https://api.meshy.ai/openapi/v1/image-to-3d`; status/result is retrieved using the returned task ID. `image_url` supports jpg/jpeg/png public URLs or base64 data URIs; alternatively `input_task_id` accepts a qualifying single-image Meshy API generation task. Using another generated image would change this comparison, so use only the original photograph in a future authorized test.

For a contemporary standard image-to-3D comparator, a reviewable configuration would specify `model_type: standard`, `ai_model: meshy-7.1`, `geometry_resolution: standard`, `should_texture: true`, `enable_pbr: true`, `texture_resolution: 2k`, `image_enhancement: false`, `should_remesh: false`, and `target_formats: [glb]`. These are a proposed design, not a tested payload. `image_enhancement` defaults true; explicitly disabling it reduces undocumented style processing of the source photograph. No extra text/image texture prompt is needed. No exposed sampler/seed gives TRELLIS.2 parity. No physical scale is established by the photo; leave `auto_size` false. `remove_lighting` is documented only for meshy-6, not the proposed 7.1.

Optional remeshing exposes triangle or quad-dominant topology, and face targets 100–300000 (default 30000); `decimation_mode` overrides `target_polycount`. `save_pre_remeshed_model: true` adds original GLB only when remesh is also enabled. Meshy T2 (`smart-topology`) is a different optional model with documented separated parts and 100–15000 target faces; it is not silently substituted for standard 7.1 here, and “separated parts” does not establish a correctly isolated Citroën door.

### GLB/PBR/export facts

`target_formats` can request glb,obj,fbx,stl,usdz,3mf. Omitted format fields are not generated outputs; request GLB explicitly. The task object documents downloadable `model_urls.glb` and texture maps. With `enable_pbr: true`, documented extra maps are metallic, roughness and normal alongside base color. Meshy 7.1/latest does not produce emission; meshy-6 may, except at 8K. PBR defaults **false**, so accepting all defaults would miss this requirement. Texture size options 2K/4K/8K are 2048/4096/8192 pixels.

Textured GLB and downloadable texture maps make UV/material inspection feasible, but chart layout, seams, topology, disconnected parts, transparency/glass quality and PBR import fidelity remain untested. The endpoint does not expose detailed UV unwrap controls. A separate UV Unwrap API exists and costs 5 credits; adding that operation would be extra processing and needs its own rationale/budget. The task result has expiry and signed URLs, so a future run must promptly preserve GLB plus maps and provenance.

### Current documented pricing and account requirements

Meshy API pricing is **prepaid API credits**. For image-to-3D, the tables include selected texture option:

| Model | Mesh only | 2K texture | 4K texture | 8K texture |
|---|---:|---:|---:|---:|
| meshy-7.1 / current latest | 20 | 30 | 30 | 35 |
| meshy-6 | 20 | 30 | 30 | 35 |
| meshy-6-lite | 5 | 15 | unsupported | unsupported |
| meshy-t2 | 5 | 15 | 15 | 20 |

Meshy 7.1 Ultra geometry (`geometry_resolution: 2k` or `4k`) adds 5 credits. Standard geometry with 2K textures is therefore **30 credits/request**; the published price table does not list an extra PBR surcharge. Do not convert that into a dollar price without an evidenced API credit purchase rate. The saved public pages do not establish the exact dollar checkout amount, minimum API purchase, or applicable paid-plan fee. Standalone remesh and UV unwrap are each 5 credits; convert is 1; neither is necessary merely to request the image-to-3D GLB.

Quickstart explicitly says **creating/managing API keys requires a paid plan**. Free accounts have a dedicated built-in key for Playground testing but cannot create/manage their own keys. A usable standalone API route thus needs an account with the required paid-plan entitlement, API key, and enough prepaid API credits, with a sufficient key spending limit. Authentication is `Authorization: Bearer ...`; official shell examples use `MESHY_API_KEY`. The web app's advertised 100 free credits/month is not evidence of an independently usable funded API key.

Task schema says `consumed_credits` returns 0 for FAILED tasks, with credits refunded on failure. Deleting an IN_PROGRESS task fails with 409 and does not cancel execution/refund its credits. Future automated submission must not be repeated merely because a client waits too long.

## Untested claims and stop condition

No service capacity, authorized generation, successful model run, latency, charge, GLB content, PBR integrity, UV layout, import/export fidelity, vehicle recognizability, door editability, moving-surface coherence, aperture/interior quality or artist acceptance was tested. Public page HTTP 200 and schemas do not establish those outcomes. A blocked acquisition is not a model-quality or research-gap result.

The minimum external enabling condition for fal is authorization to use a paid provider with the source image, a valid bound fal key and sufficient prepaid balance, plus acceptance/recording of the changed preprocessing/provenance/checkpoint contract. For Meshy it also includes paid-plan API entitlement and sufficient prepaid API credits. Those conditions are not supplied by this document; the inherited free-only/no-paid execution rule remains controlling unless the user explicitly changes it.

Only this new `review/` subtree was written. Existing artifacts were preserved. Fetch receipts contain URLs, statuses, hashes and UTC timestamps. A guessed legacy fal billing URL returned 404 (`fal_billing.fetch.json`); the later successful official linked pricing page is the billing evidence used above.
