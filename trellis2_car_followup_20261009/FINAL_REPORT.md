# TRELLIS.2 car follow-up: hosted request documented, asset experiment still blocked

**Decision:** keep the missing TRELLIS.2 car experiment as the next research decision point, but stop this attempt at the confirmed service-access blocker. Do not infer a model-quality limitation or propose a contribution from this failure. No new 3D asset was obtained, so the requested end-to-end use test remains incomplete.

## What actually ran

All times below are UTC, 9 October 2026. [RUN_LEDGER.json](RUN_LEDGER.json) derives counts and timings from the retained attempt, rather than a proposed plan.

| Stage | Observed result | Evidence |
|---|---|---|
| Workspace and tools | Shell, filesystem, HTTPS Git push/download and existing client interpreter work. No NVIDIA device exposed; no existing HF authentication resolves. | [runtime_readiness.json](research/runtime_readiness.json), [external checkpoint receipt](checkpoints/04_admission_blocked.verification.json) |
| Initial local client launch | Failed on missing Pillow before client construction or any API call. Dependency removed, imports checked, original failure retained. | [startup correction](research/client_startup_correction.json), [original log](logs/hosted-attempt001.log) |
| Corrected client | Same persistent Gradio client, frozen plan, one generation request, no automatic retries. Independent source/API review found no concrete parameter mismatch. | [client](source/hosted_followup.py), [review](research/CLIENT_REVIEW.md) |
| `/start_session` | Returned successfully. | [attempt.json](raw/hosted-attempt001/attempt.json) |
| `/preprocess_image` | Returned in 5.109 seconds. Actual 428 × 428 RGB PNG inspected; exactly matches historical official preprocessing bytes. | [image](inputs/hosted_preprocessed.png), [review](config/preprocessing_review.json) |
| `/image_to_3d` | One request at 05:21:10.417271; service `AppError` at 05:21:11.308907, approximately 0.892 seconds later. | [attempt](raw/hosted-attempt001/attempt.json), [traceback](raw/hosted-attempt001/failure_traceback.txt) |
| Generation return / export | **0 successful generation returns, 0 export requests, 0 GLBs.** No native preview returned. | [ledger](RUN_LEDGER.json) |
| Preparation / door / visual evaluation | **Unrun: no TRELLIS.2 asset available.** No artist acceptance or quality–cost improvement measured. | [frozen use plan](config/generation_plan.json) |

The exact service message was:

> You have exceeded your ZeroGPU quota (120s requested vs. 176s left). Try again in 0:55:19. Authenticate with a Hugging Face token for more quota - https://huggingface.co/settings/tokens

The 75.541-second client lifetime includes checkpoint waits; it is **not inference runtime**. The initial import failure was not another hosted generation attempt.

## Attribution and alternatives

**Observation:** this is a service-reported ZeroGPU admission rejection. The quick response and `@spaces.GPU(duration=120)` wrapper are consistent with that attribution. Server inference telemetry was unavailable, so we cannot independently prove that no internal inference work began. No model output reached this workspace.

**Strongest alternative explanation for the blocker:** hidden admission policy, inconsistent accounting or a misleading diagnostic, rather than literal exhaustion of the displayed quota. The displayed 120 seconds requested is less than 176 seconds remaining; the old rejection similarly displayed 120 versus 180. Neither the countdown nor authentication is proven sufficient to fix the problem. We did not wait and retry unchanged.

**Implementation checks:** saved API metadata, pinned Space source and installed Gradio client agree on parameter names and hidden state handling. Seed 42, `1024` → `1024_cascade`, official preprocessing exactly once, and same-client export are intentional. This removes identified client mistakes as a current explanation; it does not validate the still-unexecuted generation/export path. The first real local failure was fixed instead of being attributed to the model.

**Future input/preparation confounds:** official preprocessing crops the bumper/body close to the image boundaries. That is a possible confound for a future asset defect, not an explanation for this access error. Historical TripoSR authoring scripts reconstruct vertex-color geometry and would discard UV/PBR properties; applying them unchanged to a future TRELLIS.2 output would contaminate the comparison. The old visual failure cannot by itself identify generation, selection, material transfer or completion as the unique bottleneck.

## Contract and provenance

- Same user-supplied grass photograph: `b5b9ed4aece1359a0d291e89149634499583102e27f177aadb4c60f327e996e1`. No Bentley geometry, replacement image or different model was used.
- Returned official preprocessing: `d0fdf0cc4d37250ee692f2373459679e2e792f1f9a5e4a2dc67bc8db59771e86`. Actual source uses BRIA-RMBG-2.0 and a square black composite. We retained that input after visual inspection.
- Space source revision observed before and after the attempt: `ebf60b20fc5a4607f90a1c11c0aab0ceeda5429d`. Post-attempt metadata still reports RUNNING, which does not establish GPU admission. [Receipt](research/space_after_attempt_receipt.json).
- Space source declares `microsoft/TRELLIS.2-4B` without a weight revision pin. Observed model-repository tip `af44b45f2e35a493886929c6d786e563ec68364d` is not proof of server-loaded weights.
- [Original intent](config/INHERITED_AUTHORING_INTENT.md): visible front cabin door, coherent frame/glass/handle/lining, reversible 0–60° motion with fixed body, recognizable convincing CGI at 1440 × 960 hero/side views and exposed-edge/cabin close-up. Ordinary local preparation and plausible unseen completion are allowed. The new plan explicitly clarifies two seconds opening plus two closing, matching the historical demonstration.
- This phase is distinct from the completed TripoSR probe. Metadata of the other separately mentioned car experiment remains unknown. The proposed non-car revision study remains unstarted.

## Preservation and next decision

Executed stages through the rejection were pushed and independently downloaded before continuation. Checkpoints 01–04 retain the initial, corrected-client, preprocessing and rejected-attempt archives, payload manifests and verification receipts. The final delivery is indexed in [DOWNLOADS.md](DOWNLOADS.md); its later external verification receipt is stored alongside, rather than inside its own archive. Four critical old artifacts—original image, raw TripoSR GLB, saved latent and authored GLB—were rehashed and match their previous recorded hashes ([check](research/original_evidence_recheck.json)). This is not a claim of a fresh full recheck of all 813 earlier files.

The public hosted API does not expose its internal shape/texture latent state. No latent was returned in this attempt. A future preview must be checkpointed before the separately GPU-decorated export call, and export must use the same live session. Any unexposed server state remains unprotected; do not describe it as backed up.

**Minimum continuation requirement:** materially changed, usable admission to both official GPU stages. First try a securely configured HF account with sufficient allocation, or independently restored service access; validate actual admission instead of assuming it. The local host cannot run the official GPU pipeline as provisioned (official requirements specify NVIDIA ≥24 GB). No paid endpoint, substitute model or CPU fallback was invoked.

The onboarding draft now declares `HF_TOKEN` for `huggingface.co` and `microsoft-trellis-2.hf.space` and preserves recovery-first startup instructions. Draft read-back matched. The token is **not supplied**, authenticated execution is **not tested**, and publication is **not verified**. The user must enter the secret securely, review/save the environment settings and publish as requested by the platform. [Configuration receipt](research/onboarding_update.json).

After that prerequisite changes, create a new unique attempt directory and checkpoint its source/config; never overwrite attempt001. Obtain one candidate under this same contract. If it returns, preserve untouched export and native preview, check import/export appearance with UV/PBR intact, then perform bounded conventional door preparation and independently assess motion and visual use. Only evidence from that complete path can justify continuing, reframing or closing a research mechanism. No publishable contribution is established by this phase.
